import sqlite3


def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS channels (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        chat_link TEXT
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS keywords (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        keyword TEXT
    )
    ''')
    conn.commit()
    conn.close()

def add_channels(user_id, chat_links):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    for link in chat_links:
        cursor.execute('INSERT INTO channels (user_id, chat_link) VALUES (?, ?)', (user_id, link.strip()))
    conn.commit()
    conn.close()

def remove_channels(user_id, chat_links):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    for link in chat_links:
        cursor.execute('DELETE FROM channels WHERE user_id = ? AND chat_link = ?', (user_id, link.strip()))
    conn.commit()
    conn.close()

def get_channels(user_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT chat_link FROM channels WHERE user_id = ?', (user_id,))
    channels = [row[0] for row in cursor.fetchall()]
    conn.close()
    return channels

def add_keywords(user_id, keywords):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    for keyword in keywords:
        cursor.execute('INSERT INTO keywords (user_id, keyword) VALUES (?, ?)', (user_id, keyword.strip()))
    conn.commit()
    conn.close()

def remove_keywords(user_id, keywords):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    for keyword in keywords:
        cursor.execute('DELETE FROM keywords WHERE user_id = ? AND keyword = ?', (user_id, keyword.strip()))
    conn.commit()
    conn.close()

def get_keywords(user_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT keyword FROM keywords WHERE user_id = ?', (user_id,))
    keywords = [row[0] for row in cursor.fetchall()]
    conn.close()
    return keywords

def get_all_users():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT user_id FROM channels")
    users = cursor.fetchall()
    conn.close()
    return [user[0] for user in users]
