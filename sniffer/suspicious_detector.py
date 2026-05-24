from collections import defaultdict
from threading import Lock
from sniffer.logger import logger

# Configurable threshold for suspicious activity (e.g., 20 packets from same IP within recent window)
THRESHOLD = 20

# Thread‑safe structures
_ip_counts = defaultdict(int)
_lock = Lock()

def _reset_counts():
    """Optional helper to reset counters (not used in current flow)."""
    global _ip_counts
    with _lock:
        _ip_counts.clear()

def check_suspicious(pkt):
    """Check if the source IP has exceeded the packet count threshold.
    Emits a SocketIO alert if threshold is crossed.
    """
    try:
        src_ip = None
        if pkt.haslayer('IP'):
            src_ip = pkt['IP'].src
        elif pkt.haslayer('ARP'):
            src_ip = pkt['ARP'].psrc
        else:
            return  # Unsupported packet for IP tracking

        with _lock:
            _ip_counts[src_ip] += 1
            count = _ip_counts[src_ip]

        if count == THRESHOLD:
            # Lazy import to avoid circular dependency
            from app import socketio
            alert = {
                "type": "suspicious_traffic",
                "src_ip": src_ip,
                "count": count,
                "message": f"{src_ip} has sent {count} packets (threshold reached).",
            }
            socketio.emit('alert', alert)
            logger.warning(f"Suspicious traffic detected from {src_ip}: {count} packets")
    except Exception as e:
        logger.exception(f"Error in suspicious detection: {e}")
