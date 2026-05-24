import threading
import queue
import time
from scapy.all import sniff
from sniffer.packet_analyzer import analyze_packet
from sniffer.statistics import update_stats
from sniffer.suspicious_detector import check_suspicious
from database.db import insert_packet
from sniffer.logger import logger  # direct logger import

# Lazy import for socketio to avoid circular dependency
def _get_socketio():
    from app import socketio
    return socketio

# Global counter for captured packets
packet_counter = 0
MAX_PACKETS = 50
packet_queue = queue.Queue(maxsize=50)
def packet_callback(pkt):
    global packet_counter
    try:
        packet_info = analyze_packet(pkt)
        # Insert into DB
        insert_packet(packet_info)
        # Update statistics
        update_stats(pkt)
        # Check for suspicious traffic
        check_suspicious(pkt)
        # Emit to clients via SocketIO
        socketio = _get_socketio()
        socketio.emit('new_packet', packet_info)
        # Maintain queue of latest 50 packets (for possible future use)
        if packet_queue.full():
            packet_queue.get()
        packet_queue.put(packet_info)
        packet_counter += 1
        # Stop sniffing after MAX_PACKETS to avoid infinite loop
        if packet_counter >= MAX_PACKETS:
            logger.info(f"Captured {packet_counter} packets, restarting sniffing loop.")
            return True  # stop_filter signals sniff to stop
    except Exception as e:
        logger.exception(f"Error processing packet: {e}")

def start_sniffing(interface=None):
    """Start Scapy sniffing in a background thread.
    Restarts automatically after reaching packet limit.
    """
    global packet_counter
    logger.info("Starting packet sniffing...")
    while True:
        packet_counter = 0
        sniff(prn=packet_callback, store=False, iface=interface, stop_filter=lambda x: packet_counter >= MAX_PACKETS)
        # Small pause before next cycle
        time.sleep(1)
