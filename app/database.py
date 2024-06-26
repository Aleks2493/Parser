import sqlite3
import logging

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS channels (
        user_id INTEGER,
        chat_link TEXT,
        PRIMARY KEY (user_id, chat_link)
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS keywords (
        user_id INTEGER,
        keyword TEXT,
        PRIMARY KEY (user_id, keyword)
    )
    ''')
    conn.commit()
    conn.close()

def add_channels(user_id, chat_links):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    for link in chat_links:
        cursor.execute('INSERT OR IGNORE INTO channels (user_id, chat_link) VALUES (?, ?)', (user_id, link.strip()))
    conn.commit()
    conn.close()

def add_keywords(user_id, keywords):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    for keyword in keywords:
        cursor.execute('INSERT OR IGNORE INTO keywords (user_id, keyword) VALUES (?, ?)', (user_id, keyword.strip()))
    conn.commit()
    conn.close()

def remove_all_channels(user_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM channels WHERE user_id = ?', (user_id,))
    conn.commit()
    conn.close()

def remove_all_keywords(user_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM keywords WHERE user_id = ?', (user_id,))
    conn.commit()
    conn.close()

def get_all_users():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT user_id FROM channels")
    users = cursor.fetchall()
    conn.close()
    logging.info(f"Получены пользователи: {users}")
    return [user[0] for user in users]

def get_channels(user_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT chat_link FROM channels WHERE user_id = ?', (user_id,))
    channels = [row[0] for row in cursor.fetchall()]
    conn.close()
    logging.info(f"Каналы для пользователя {user_id}: {channels}")
    return channels

def get_keywords(user_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT keyword FROM keywords WHERE user_id = ?', (user_id,))
    keywords = [row[0] for row in cursor.fetchall()]
    conn.close()
    logging.info(f"Ключевые слова для пользователя {user_id}: {keywords}")
    return keywords

