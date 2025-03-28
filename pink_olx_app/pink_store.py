# Local DB (SQLite) or CSV-based storage

# pink_store.py

import sqlite3
import time

def init_db(db_name="pink_olx_data.db"):
    """
    Initialize the local database (if not exists) and create the table.
    """
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS search_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            listing_id INTEGER,
            title TEXT,
            price REAL,
            state TEXT,
            city TEXT,
            query TEXT,
            timestamp INTEGER
        )
    """)
    conn.commit()
    conn.close()

def save_listings(listings, query, db_name="pink_olx_data.db"):
    """
    Saves current listings into the DB. 
    Includes the search 'query' and a timestamp, so we can track history.
    """
    if not listings:
        return

    timestamp = int(time.time())  # seconds since epoch
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    for item in listings:
        listing_id = item.get("id", 0)
        title = item.get("title", "")
        try:
            price = float(item.get("price", 0) or 0)
        except:
            price = 0
        state = item.get("state", "")
        location_dict = item.get("location") or {}
        city = location_dict.get("city", "")

        c.execute("""
            INSERT INTO search_results (listing_id, title, price, state, city, query, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (listing_id, title, price, state, city, query, timestamp))

    conn.commit()
    conn.close()

def get_history_for_query(query, db_name="pink_olx_data.db"):
    """
    Retrieves historical listing data for a given query. You can do more advanced queries or grouping.
    """
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute("""
        SELECT listing_id, title, price, state, city, query, timestamp 
        FROM search_results
        WHERE query = ?
        ORDER BY timestamp DESC
    """, (query,))

    rows = c.fetchall()
    conn.close()
    return rows
