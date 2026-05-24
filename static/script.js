// static/script.js – client‑side SocketIO handling and DOM updates

document.addEventListener('DOMContentLoaded', () => {
    const socket = io(); // Connect to Flask‑SocketIO server
    const packetBody = document.getElementById('packet-body');
    const alertBanner = document.getElementById('alert-banner');

    // Stats elements
    const statsElems = {
        total: document.getElementById('total-count'),
        TCP: document.getElementById('tcp-count'),
        UDP: document.getElementById('udp-count'),
        ICMP: document.getElementById('icmp-count'),
        ARP: document.getElementById('arp-count'),
    };

    // Helper: create a table row for a packet dict
    function createRow(pkt) {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${pkt.timestamp}</td>
            <td>${pkt.src_ip || ''}</td>
            <td>${pkt.dst_ip || ''}</td>
            <td>${pkt.protocol}</td>
            <td>${pkt.length}</td>
            <td>${pkt.src_port || ''}</td>
            <td>${pkt.dst_port || ''}</td>
        `;
        return tr;
    }

    // Add a new packet to the table, keep max 50 rows
    function addPacket(pkt) {
        const row = createRow(pkt);
        packetBody.prepend(row); // newest on top
        // Remove excess rows
        while (packetBody.children.length > 50) {
            packetBody.removeChild(packetBody.lastElementChild);
        }
    }

    // Update stats UI
    function updateStats(stats) {
        Object.keys(statsElems).forEach(key => {
            if (stats[key] !== undefined) {
                statsElems[key].textContent = stats[key];
            }
        });
    }

    // Show alert banner
    function showAlert(data) {
        alertBanner.textContent = data.message || 'Suspicious traffic detected';
        alertBanner.classList.add('visible');
        // Auto‑hide after 8 seconds
        setTimeout(() => {
            alertBanner.classList.remove('visible');
        }, 8000);
    }

    // SocketIO listeners
    socket.on('new_packet', pkt => {
        addPacket(pkt);
    });
    socket.on('stats_update', stats => {
        updateStats(stats);
    });
    socket.on('alert', data => {
        showAlert(data);
    });

    // Initial load – fetch latest packets and stats via REST
    fetch('/api/packets')
        .then(res => res.json())
        .then(packets => {
            setTimeout(() => {
                packets.reverse().forEach(pkt => addPacket(pkt)); // reverse to show newest on top
            }, 1000);
        })
        .catch(err => console.error('Failed to load packets:', err));

    fetch('/api/stats')
        .then(res => res.json())
        .then(stats => updateStats(stats))
        .catch(err => console.error('Failed to load stats:', err));
});
