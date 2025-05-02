import sqlite3
import json

def get_connection():
    return sqlite3.connect("chatbot.db", check_same_thread=False)

def create_tables():
    conn = get_connection()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (user_id TEXT PRIMARY KEY)''')
    c.execute('''CREATE TABLE IF NOT EXISTS documents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        file_name TEXT,
        chunks TEXT,
        FOREIGN KEY (user_id) REFERENCES users(user_id))''')
    c.execute('''CREATE TABLE IF NOT EXISTS chat_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        role TEXT,
        content TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(user_id))''')
    conn.commit()
    conn.close()

def save_chat(user_id, role, content):
    conn = get_connection()
    conn.execute("INSERT INTO chat_history (user_id, role, content) VALUES (?, ?, ?)", (user_id, role, content))
    conn.commit()
    conn.close()

def get_chat_history(user_id):
    conn = get_connection()
    cursor = conn.execute("SELECT role, content FROM chat_history WHERE user_id=? ORDER BY timestamp", (user_id,))
    history = [{"role": role, "content": content} for role, content in cursor.fetchall()]
    conn.close()
    
    return history

def save_document(user_id, file_name, chunks):
    conn = get_connection()
    chunks_json = json.dumps(chunks)  
    conn.execute("INSERT INTO documents (user_id, file_name, chunks) VALUES (?, ?, ?)", (user_id, file_name, chunks_json))
    conn.commit()
    conn.close()

def get_documents(user_id):
    conn = get_connection()
    cursor = conn.execute("SELECT file_name, chunks FROM documents WHERE user_id=?", (user_id,))
    docs = {}
    for file_name, chunks_json in cursor.fetchall():
        if chunks_json:
            docs[file_name] = json.loads(chunks_json)
    conn.close()
    return docs

def clean_user_data(user_id):
    conn = get_connection()
    conn.execute("DELETE FROM chat_history WHERE user_id=?", (user_id,))
    conn.execute("DELETE FROM documents WHERE user_id=?", (user_id,))
    conn.execute("DELETE FROM users WHERE user_id=?", (user_id,))
    conn.commit()
    conn.close()

