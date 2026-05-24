import os
import threading
from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO

# Import sniffer modules
from sniffer.packet_capture import start_sniffing
from sniffer.statistics import get_stats
from database.db import fetch_latest_packets

app = Flask(__name__)
# Use threading async mode as required
socketio = SocketIO(app, async_mode='threading')

# Ensure logs directory exists (logger will create its own)

# Background thread for packet sniffing
sniff_thread = None

def start_background_sniffing():
    global sniff_thread
    if sniff_thread is None:
        sniff_thread = threading.Thread(target=start_sniffing, daemon=True)
        sniff_thread.start()

@app.route('/')
def index():
    # Render dashboard, initial packet list will be fetched via SocketIO or AJAX
    return render_template('dashboard.html')

@app.route('/api/packets')
def api_packets():
    """Return the latest 50 packets as JSON (used on page load)."""
    packets = fetch_latest_packets(limit=50)
    return jsonify(packets)

@app.route('/api/stats')
def api_stats():
    """Return current protocol statistics."""
    return jsonify(get_stats())

# SocketIO event placeholders (server will emit from sniffer modules)
# Clients will listen to 'new_packet', 'stats_update', and 'alert'

if __name__ == '__main__':
    # Start sniffing before running the web server
    start_background_sniffing()
    # Run Flask development server
    socketio.run(app, host='127.0.0.1', port=5000, debug=True, allow_unsafe_werkzeug=True)
