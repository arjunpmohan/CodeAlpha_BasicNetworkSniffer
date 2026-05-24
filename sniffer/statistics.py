import threading

# Thread‑safe counters for protocol statistics
_stats_lock = threading.Lock()
_stats = {
    "total": 0,
    "TCP": 0,
    "UDP": 0,
    "ICMP": 0,
    "ARP": 0,
}

def update_stats(pkt):
    """Update global protocol counters based on the captured Scapy packet and emit stats via SocketIO."""
    from sniffer.logger import logger
    from scapy.layers.inet import TCP, UDP, ICMP
    from scapy.layers.l2 import ARP
    # Update counters
    with _stats_lock:
        _stats["total"] += 1
        if pkt.haslayer(TCP):
            _stats["TCP"] += 1
        elif pkt.haslayer(UDP):
            _stats["UDP"] += 1
        elif pkt.haslayer(ICMP):
            _stats["ICMP"] += 1
        elif pkt.haslayer(ARP):
            _stats["ARP"] += 1
    # Emit updated stats
    try:
        from app import socketio
        socketio.emit('stats_update', _stats)
    except Exception as e:
        logger.exception(f"Failed to emit stats: {e}")
def get_stats():
    """Return a copy of the current statistics dictionary."""
    with _stats_lock:
        return dict(_stats)
