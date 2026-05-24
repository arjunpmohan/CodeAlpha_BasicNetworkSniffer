# Advanced Network Packet Sniffer & Traffic Analyzer

A modular, real-time network sniffer and traffic analysis dashboard built for Windows. This project leverages Python, Flask, Flask-SocketIO, Scapy, and SQLite to capture network traffic in the background and stream it to a modern, dark-themed web interface.

## Features

*   **Real-time Packet Capture**: Uses Scapy to sniff network interfaces asynchronously without blocking the main application.
*   **Live Web Dashboard**: Streams newly captured packets to the browser instantly via WebSockets (Flask-SocketIO).
*   **Protocol Analysis**: Automatically parses and categorizes TCP, UDP, ICMP, and ARP traffic.
*   **Suspicious Traffic Detection**: Built-in alerting system that detects abnormal traffic spikes (e.g., >20 packets from a single IP in a short duration) and displays an alert banner on the UI.
*   **Database Persistence**: Logs all captured packets into a local SQLite database (`packets.db`) so history is maintained across server restarts.
*   **Live Statistics**: Tracks and displays running totals for different network protocols.
*   **Modern UI/UX**: Responsive glassmorphism design with auto-refreshing tables and alert animations.

## Tech Stack

*   **Backend**: Python 3.12, Flask, Flask-SocketIO, Scapy
*   **Frontend**: HTML, Vanilla CSS, Vanilla JavaScript, Socket.IO Client
*   **Database**: SQLite3

## Prerequisites

If you are running this on a **Windows** environment, Scapy requires **Npcap** or WinPcap to capture live network interfaces.

1.  Download and install [Npcap](https://npcap.com/#download).
2.  Make sure to select **"Install Npcap in WinPcap API-compatible Mode"** during installation.
3.  Ensure you have Python 3.12 or newer installed.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/network_sniffer_project.git
    cd network_sniffer_project
    ```

2.  **Create a virtual environment (optional but recommended):**
    ```bash
    python -m venv venv
    venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1.  **Start the server:**
    Run the application using Python (ensure you run this in an administrative terminal if Scapy requires elevated privileges to access network interfaces).
    ```bash
    python app.py
    ```

2.  **Access the Dashboard:**
    Open your web browser and navigate to:
    ```
    http://127.0.0.1:5000
    ```

3.  The dashboard will connect via WebSockets. After a 1-second simulated loading delay, the recent packet history will load, and new incoming packets will stream automatically to the top of the table.

## Project Structure

```text
network_sniffer_project/
├── app.py                      # Main Flask entry point and SocketIO server
├── requirements.txt            # Python dependencies
├── database/
│   └── db.py                   # SQLite schema and query functions
├── sniffer/
│   ├── __init__.py
│   ├── logger.py               # Rotating file logging configuration
│   ├── packet_analyzer.py      # Scapy packet parsing logic
│   ├── packet_capture.py       # Background sniffing thread and loop
│   ├── statistics.py           # Protocol counting and math
│   └── suspicious_detector.py  # Traffic anomaly detection logic
├── static/
│   ├── script.js               # Frontend SocketIO client and DOM updates
│   └── style.css               # Modern dark-theme styling
└── templates/
    └── dashboard.html          # Web dashboard structure
```

## Logging

Application logs and errors are captured locally in the `logs/sniffer.log` file using a rotating file handler. Check this file if you encounter any issues capturing packets.

## Disclaimer

**Educational Purposes Only**: This tool is designed as a cybersecurity internship portfolio piece. Do not use this software to capture traffic on networks you do not own or do not have explicit permission to monitor.
