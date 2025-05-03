from openai import OpenAI, OpenAIError
from config import Config
import os
from dotenv import load_dotenv
load_dotenv()
system_prompt = Config.SYSTEM_PROMPT
API_KEY = Config.OPENAI_API_KEY

def chat(messages, pdf_context=None):
    
    messages = messages[-4:]
    if pdf_context is not None:
            # Combine selected chunks into a single context message
            
        messages.insert(0, pdf_context)
    else:
        messages.insert(0, {"role": "system", "content": system_prompt})

    try:
        client = OpenAI(
            api_key=API_KEY,
            base_url="https://generativelanguage.googleapis.com/v1beta/"
        )
        print("Messages:", messages)
        completion = client.chat.completions.create(
            model="gemini-2.0-flash",  
            messages=messages,
            temperature=0,
            stream=True
        )
        return completion
        
    except OpenAIError as e:
        print(f"OpenAI API error: {e}")
        return None


# handles stream response back from LLM
def stream_parser(stream):
    if stream is None:
        return None
    for chunk in stream:
        if chunk.choices[0].delta.content != None:
            yield chunk.choices[0].delta.content

