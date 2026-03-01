"""Database storage for PlayStation Store purchases.

This module manages SQLite database operations for storing and retrieving
purchase data, including orders and individual items.
"""

import sqlite3
from pathlib import Path
from typing import Dict, Any

import pandas as pd

DB_PATH = Path(__file__).parent.parent.parent / "data" / "purchases.db"


def init_db() -> None:
    """Initialize the SQLite database with required tables.
    
    Creates two tables if they don't exist:
    - purchases: Order metadata (order_number, date, total, source, payment_method)
    - items: Individual items per order (linked via order_number)
    
    Also ensures the data directory exists.
    """
    # Ensure data directory exists
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS purchases (
        order_number TEXT PRIMARY KEY,
        date TEXT,
        total REAL,
        source TEXT DEFAULT 'real',
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


def store_purchase(purchase: Dict[str, Any], source: str = "real") -> None:
    """Store a purchase and its items in the database.
    
    Args:
        purchase: Dictionary with keys:
            - order_number: Unique order identifier
            - date: Purchase date
            - total: Total purchase amount
            - items: List of dicts with 'name' and 'price'
        source: Data source - 'demo' or 'real' (default: 'real')
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Store purchase
    c.execute("""
        INSERT OR IGNORE INTO purchases(order_number, date, total, source)
        VALUES (?, ?, ?, ?)
    """, (purchase["order_number"], purchase["date"], purchase["total"], source))
    
    # Store items (avoid duplicates)
    for item in purchase["items"]:
        c.execute("""
            INSERT OR IGNORE INTO items(order_number, name, price)
            VALUES (?, ?, ?)
        """, (purchase["order_number"], item["name"], item["price"]))
    
    conn.commit()
    conn.close()


def load_purchases(source: str = "real") -> pd.DataFrame:
    """Load all unique items purchased from the database into a pandas DataFrame.
    
    Args:
        source: Data source to load - 'demo' or 'real' (default: 'real')
    
    Returns:
        DataFrame with columns: item_name, date, item_price (one row per unique item).
        Empty DataFrame if no data exists.
    """
    query = """
    SELECT DISTINCT
        i.name AS item_name,
        p.date,
        i.price AS item_price
    FROM items i
    JOIN purchases p ON i.order_number = p.order_number
    WHERE p.source = ?
    ORDER BY p.date ASC
    """
    
    with sqlite3.connect(DB_PATH) as conn:
        df = pd.read_sql(query, conn, params=(source,))
    
    if not df.empty:
        df['date'] = pd.to_datetime(df['date'], dayfirst=True)
        df['item_price'] = df['item_price'].astype(float)
    
    return df


def load_orders(source: str = "real") -> pd.DataFrame:
    """Load all orders from the database into a pandas DataFrame.
    
    Args:
        source: Data source to load - 'demo' or 'real' (default: 'real')
    
    Returns:
        DataFrame with columns: order_number, date, total (order total).
        Empty DataFrame if no data exists.
    """
    query = """
    SELECT 
        order_number,
        date,
        total
    FROM purchases
    WHERE source = ?
    ORDER BY date ASC
    """
    
    with sqlite3.connect(DB_PATH) as conn:
        df = pd.read_sql(query, conn, params=(source,))
    
    if not df.empty:
        df['date'] = pd.to_datetime(df['date'], dayfirst=True)
        df['total'] = df['total'].astype(float)
    
    return df
