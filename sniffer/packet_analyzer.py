from scapy.layers.inet import IP, TCP, UDP, ICMP
from scapy.layers.l2 import ARP
import time

def analyze_packet(pkt):
    """Extract relevant fields from a Scapy packet and return a JSON‑serializable dict.
    Fields: timestamp, src_ip, dst_ip, protocol, length, src_port, dst_port.
    """
    packet_info = {
        "timestamp": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
        "src_ip": None,
        "dst_ip": None,
        "protocol": None,
        "length": len(pkt),
        "src_port": None,
        "dst_port": None,
    }

    if IP in pkt:
        packet_info["src_ip"] = pkt[IP].src
        packet_info["dst_ip"] = pkt[IP].dst
        if TCP in pkt:
            packet_info["protocol"] = "TCP"
            packet_info["src_port"] = pkt[TCP].sport
            packet_info["dst_port"] = pkt[TCP].dport
        elif UDP in pkt:
            packet_info["protocol"] = "UDP"
            packet_info["src_port"] = pkt[UDP].sport
            packet_info["dst_port"] = pkt[UDP].dport
        elif ICMP in pkt:
            packet_info["protocol"] = "ICMP"
        else:
            packet_info["protocol"] = pkt[IP].proto
    elif ARP in pkt:
        packet_info["protocol"] = "ARP"
        packet_info["src_ip"] = pkt[ARP].psrc
        packet_info["dst_ip"] = pkt[ARP].pdst
    else:
        # Unsupported/unknown protocol – leave protocol as None so caller can ignore
        packet_info["protocol"] = "UNKNOWN"

    return packet_info
