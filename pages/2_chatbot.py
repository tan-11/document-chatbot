# chatbot.py
import streamlit as st

if 'new_user_id' not in st.session_state:
    st.warning("You must log in first.")
    st.stop()



from helper.llm_helper import chat, stream_parser
from dotenv import load_dotenv

from helper.document_helper import extract_text_from_pdf, chunk_text, retrieve_relevant_chunks, extract_text_from_docx, preprocess_text, extract_text_from_image, extract_text_from_pptx
from helper.db_helper import create_tables, get_chat_history, save_chat, save_document, get_documents, clean_user_data

load_dotenv()

create_tables()

user_id = st.session_state.new_user_id

if "messages" not in st.session_state:
    st.session_state.messages = []

if "document_chunks" not in st.session_state:
    st.session_state.document_chunks = {}

if "current_user_id" not in st.session_state or st.session_state.current_user_id != user_id:
    st.session_state.current_user_id = user_id
    
    st.session_state.messages.clear()
    st.session_state.document_chunks.clear()

    documents = get_documents(user_id)
    if documents:
        for doc_name, chunks in documents.items():
            st.session_state.document_chunks[doc_name] = chunks

    history = get_chat_history(user_id)
    if history:
        st.session_state.messages = history
print("Loaded messages:", st.session_state.messages) 
print("Loaded document chunks:", st.session_state.document_chunks)   
#######################################

st.set_page_config(
    page_title="Streamlit OpenAI Chatbot",
    initial_sidebar_state="expanded"
)

st.title("AI Chatbot")


file = st.sidebar.file_uploader("Upload Documents", label_visibility="collapsed", key="hidden_uploader")

if "after_cleanup" not in st.session_state:
    st.session_state.after_cleanup = False

# Process uploaded PDFs
if file and st.session_state.after_cleanup is False:
    if "processed_files" not in st.session_state:
        st.session_state.processed_files = set()
    if file.name not in st.session_state.processed_files:
        if file.name.endswith(".pdf"):
            text = extract_text_from_pdf(file)
        elif file.name.endswith(".docx"):
            text = extract_text_from_docx(file)
        elif file.name.endswith((".png", ".jpg", ".jpeg")):
            text = extract_text_from_image(file)
        elif file.name.endswith(".pptx"):
            text = extract_text_from_pptx(file)
        else:
            text = None
            st.sidebar.error("Unsupported file type. Please upload a PDF, DOCX, PNG, JPG, JPEG, PPTX, or DOC file.")

        if text: 
            print(f"Extracted text from {file.name}: {text} ")
            st.session_state.processed_files.add(file.name)
            text = preprocess_text(text)
            chunks = chunk_text(text)
            st.session_state.document_chunks[file.name] = chunks
            st.sidebar.success(f"Uploaded and processed {file.name}")
            save_document(user_id, file.name, chunks)

st.session_state.after_cleanup = False

top_k = st.sidebar.slider("Number of Top Relevant Chunks", min_value=1, max_value=20, value=2, step=1)

# Sidebar: show all uploaded PDFs
st.sidebar.subheader("Uploaded Documents")
for document_name in st.session_state.document_chunks.keys():
    st.sidebar.write(f"- {document_name}")

# Sidebar: combine mode and file selection
combine_mode = st.sidebar.checkbox("Combine multiple PDFs")

selected_documents = []
if combine_mode:
    selected_documents = st.sidebar.multiselect("Select PDFs to combine", options=list(st.session_state.document_chunks.keys()))
else:
    selected_document = st.sidebar.selectbox("Select a Document", options=list(st.session_state.document_chunks.keys()))
    selected_documents = [selected_document]

if st.sidebar.button("Clear All Data"):
    # Clear data from session and database
    st.session_state.messages.clear()
    st.session_state.document_chunks.clear()
    st.session_state.processed_files = set()
    uploaded_file = None
    st.session_state["uploaded_file"] = None
    clean_user_data(user_id)
    st.session_state.after_cleanup = True
    print("uploaded file:",st.session_state["uploaded_file"])
    st.rerun()  # refresh the page 

if st.sidebar.button("Log Out"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.switch_page("pages/1_login.py")  

# Display existing messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if user_prompt := st.chat_input("What questions do you have about the document(s)?"):
    with st.chat_message("user"):
        st.markdown(user_prompt)

    st.session_state.messages.append({"role": "user", "content": user_prompt})
    save_chat(user_id, "user", user_prompt)  # Save user prompt to database
    # Gather selected chunks
    combined_chunks = []
    context_message = ""

    if selected_documents:
        for name in selected_documents:
            combined_chunks.extend(st.session_state.document_chunks.get(name, []))
            print(f"Combined chunks from {name}: {len(st.session_state.document_chunks.get(name, []))} chunks")
            
    else:
        print("No Document selected.")

        # Retrieve relevant chunks
    if combined_chunks:
        retrieved_chunks = retrieve_relevant_chunks(combined_chunks, user_prompt, top_k=top_k)
        context = "\n\n".join(retrieved_chunks)
        print(f"Retrieved chunks: {len(retrieved_chunks)}")
        st.session_state.document_context =  {"role": "system", "content": f"This is relevant Document content:\n{context}"}
    
    # Generate response
    with st.spinner('Generating response...'):
        if 'document_context' in st.session_state:
            print("Using DOCUMENTs context for response generation.")
            llm_response = chat(st.session_state.messages, st.session_state.document_context)
            st.session_state.document_context.clear()
        else:
            llm_response = chat(st.session_state.messages)

        stream_output = st.write_stream(stream_parser(llm_response))
        save_chat(user_id, "assistant", stream_output) 
        print("Stream output:", stream_output)
        if stream_output:
            print(10101010)
            st.session_state.messages.append({"role": "assistant", "content": stream_output})

    # Display response
    last_response = st.session_state.messages[-1]['content']
    if stream_output:
        if str(last_response) != str(stream_output):
            with st.chat_message("assistant"):
                st.markdown(stream_output)