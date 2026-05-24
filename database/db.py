import os
import sqlite3
from datetime import datetime

DB_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'database')
os.makedirs(DB_DIR, exist_ok=True)
DB_PATH = os.path.join(DB_DIR, 'packets.db')

def _get_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = _get_connection()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS packets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            src_ip TEXT,
            dst_ip TEXT,
            protocol TEXT,
            length INTEGER,
            src_port INTEGER,
            dst_port INTEGER
        )
    ''')
    conn.commit()
    conn.close()

# Ensure DB is ready on import
init_db()

def insert_packet(packet):
    """Insert a packet dict into the SQLite database.
    Expected keys: timestamp, src_ip, dst_ip, protocol, length, src_port, dst_port.
    """
    conn = _get_connection()
    c = conn.cursor()
    c.execute('''
        INSERT INTO packets (timestamp, src_ip, dst_ip, protocol, length, src_port, dst_port)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        packet.get('timestamp'),
        packet.get('src_ip'),
        packet.get('dst_ip'),
        packet.get('protocol'),
        packet.get('length'),
        packet.get('src_port'),
        packet.get('dst_port')
    ))
    conn.commit()
    conn.close()

def fetch_latest_packets(limit=50):
    """Return the most recent `limit` packets as a list of dicts ordered by newest first."""
    conn = _get_connection()
    c = conn.cursor()
    c.execute('''
        SELECT timestamp, src_ip, dst_ip, protocol, length, src_port, dst_port
        FROM packets
        ORDER BY id DESC
        LIMIT ?
    ''', (limit,))
    rows = c.fetchall()
    conn.close()
    # Convert Row objects to plain dicts
    return [dict(row) for row in rows]
