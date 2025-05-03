# Document Chatbot

A Streamlit-based chatbot that can read and answer questions based on uploaded file documents.

## Features

- Upload PDF or text documents
- Ask questions about the documents
- Get accurate answers using AI
- Interactive web interface with Streamlit

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/tan-11/document-chatbot.git
   cd document-chatbot

2. Create and activate a virtual environment ( optional )
    python -m venv venv
    .\venv\Scripts\activate

3. Install dependencies
    pip install -r requirements.txt

4. Environment Variables
    Create a '.env' file in the root folder and add your OpenAI API key, and modify the model name in the llm_helper.py into your API model.

5. OCR setup
    If Tesseract OCR is not found, specify the path manually in the document_helper.py or your environment
    Download Tesseract: https://github.com/tesseract-ocr/tesseract

## Usage
1. Run the Streamlit app
    streamlit run HomePage.py

2. login and upload your document via the interface and start chatting!

```markdown
## Notes

- `.env` is not uploaded for security reasons. You must create it yourself.
- Do not include your `venv/` folder in the repository. It's recommended to use `.gitignore` to exclude it.

document-chatbot/
│
├── HomePage.py         # Main Streamlit app
├── Page/               # streamlit pages
│   ├──	1_login.py
│   └──	2_chatbot.py          
├──	helper/             #utility
│   ├──	db_helper.py
│   ├──	document_helper.py
│   └──	llm_helper.py
├── requirements.txt    #Python dependencies
├──	 config.py
└──	readme.md            
