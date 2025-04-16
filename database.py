
# db/database.py - 資料庫操作模組
import sqlite3

conn = sqlite3.connect("ai_stylist.db", check_same_thread=False)
c = conn.cursor()

def init_db():
    c.execute('''CREATE TABLE IF NOT EXISTS wardrobe (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    type TEXT,
                    img_path TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS tryon_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    type TEXT,
                    occasion TEXT,
                    rating TEXT,
                    suggestion TEXT,
                    perfume TEXT,
                    created_at TEXT,
                    img_path TEXT)''')
    conn.commit()

def save_item_to_db(item_type, img_path):
    c.execute("INSERT INTO wardrobe (type, img_path) VALUES (?, ?)", (item_type, img_path))
    conn.commit()

def get_all_items_from_db():
    c.execute("SELECT type, img_path FROM wardrobe")
    return c.fetchall()

def save_tryon_to_db(item_type, occasion, rating, suggestion, perfume, img_path):
    from datetime import datetime
    c.execute("""
        INSERT INTO tryon_history (type, occasion, rating, suggestion, perfume, created_at, img_path)
        VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (item_type, occasion, rating, suggestion, perfume, str(datetime.now()), img_path))
    conn.commit()

def get_latest_tryon_from_db():
    c.execute("SELECT type, occasion, rating, suggestion, perfume, img_path FROM tryon_history ORDER BY created_at DESC LIMIT 1")
    return c.fetchone()
