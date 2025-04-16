import sqlite3
import os

# 確保資料夾存在
if not os.path.exists("db"):
    os.makedirs("db")

conn = sqlite3.connect("db/ai_stylist.db", check_same_thread=False)
c = conn.cursor()

def init_db():
    c.execute('''CREATE TABLE IF NOT EXISTS wardrobe (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    type TEXT,
                    img_path TEXT)''')
    conn.commit()

def save_item_to_db(item_type, img_path):
    c.execute("INSERT INTO wardrobe (type, img_path) VALUES (?, ?)", (item_type, img_path))
    conn.commit()

def get_all_items_from_db():
    c.execute("SELECT type, img_path FROM wardrobe")
    return c.fetchall()
