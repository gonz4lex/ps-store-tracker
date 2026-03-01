import sqlite3
from pathlib import Path
from typing import Dict

import pandas as pd

DB_PATH = Path(__file__).parent.parent.parent / "data" / "purchases.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS purchases (
        order_number TEXT PRIMARY KEY,
        date TEXT,
        total REAL,
        payment_method TEXT
    )
    """)
    c.execute("""
    CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_number TEXT,
        name TEXT,
        price REAL,
        UNIQUE(order_number, name, price),
        FOREIGN KEY(order_number) REFERENCES purchases(order_number)
    )
    """)
    conn.commit()
    conn.close()

def store_purchase(purchase: Dict):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Store purchase
    c.execute("""
        INSERT OR IGNORE INTO purchases(order_number, date, total)
        VALUES (?, ?, ?)
    """, (purchase["order_number"], purchase["date"], purchase["total"]))
    
    # Store items (avoid duplicates)
    for item in purchase["items"]:
        c.execute("""
            INSERT OR IGNORE INTO items(order_number, name, price)
            VALUES (?, ?, ?)
        """, (purchase["order_number"], item["name"], item["price"]))
    
    conn.commit()
    conn.close()

def load_purchases() -> pd.DataFrame:
    """Load all purchases from the DB into a pandas DataFrame."""
    query = """
    SELECT 
        p.order_number,
        p.date,
        p.total AS price,
        p.payment_method,
        i.name AS item_name,
        i.price AS item_price
    FROM purchases p
    LEFT JOIN items i ON p.order_number = i.order_number
    ORDER BY p.date ASC
    """
    
    with sqlite3.connect(DB_PATH) as conn:
        df = pd.read_sql(query, conn)
    
    if not df.empty:
        df['date'] = pd.to_datetime(df['date'], dayfirst=True)
        df['price'] = df['price'].astype(float)
        df['item_price'] = df['item_price'].astype(float)
    
    return df
