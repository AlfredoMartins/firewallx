import threading
import queue
import os
import sys
import time
from collections import defaultdict
from flask import Flask, request, jsonify
from flask_socketio import SocketIO
from flask_cors import CORS
from scapy.all import sniff, IP, TCP  # type: ignore

THRESHOLD = 40
print(f"THRESHOLD: {THRESHOLD}")

def read_ip_file(filename):
    with open(filename, "r+") as file:
        ips = [line.strip() for line in file]
    return set(ips)

def is_nimda_worm(packet):
    if packet.haslayer(TCP) and packet[TCP].dport == 80:
        payload = packet[TCP].payload
        return "GET /scripts/root.exe" in str(payload)
    return False

def log_event(message):
    log_folder = "logs"
    os.makedirs(log_folder, exist_ok=True)
    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
    log_file = os.path.join(log_folder, f"log_{timestamp}.txt")

    with open(log_file, "a+") as file:
        file.write(f"{message}\n")

def block_ip(ip):
    os.system(f"iptables -A INPUT -s {ip} -j DROP")

def unblock_ip(ip):
    os.system(f"iptables -D INPUT -s {ip} -j ACCEPT")

def packet_callback(packet):
    src_ip = packet[IP].src

    if src_ip in whitelist_ips:
        return
    
    if src_ip in blacklist_ips:
        os.system(f"iptables -A INPUT -s {src_ip} -j DROP")
        log_event(f"Blocking blacklisted IP: {src_ip}")
        return
    
    if is_nimda_worm(packet):
        print(f"Blocking Nimda source IP: {src_ip}")
        block_ip(src_ip)
        log_event(f"Blocking Nimda source IP: {src_ip}")
        return
    
    packet_count[src_ip] += 1

    current_time = time.time()
    time_interval = current_time - start_time[0]

    if time_interval >= 1:
        for ip, count in packet_count.items():
            packet_rate = count / time_interval

            if packet_rate > THRESHOLD and ip not in blocked_ips:
                #msg = f"Blocking IP: {ip}, packet rate: {packet_rate}"
                queue_thread.put(ip)
                block_ip(ip)
                log_event(f"Blocking IP: {ip}, packet rate: {packet_rate}")
                blocked_ips.add(ip)

        packet_count.clear()
        start_time[0] = current_time

# API

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

CORS(app, origins=["http://localhost:5173", "http://192.168.1.77:5173"], supports_credentials=True)
socketio = SocketIO(app, cors_allowed_origins=["http://localhost:5173", "http://192.168.1.77:5173"],  manage_session=True)

# SOCKET
@socketio.on('connect')
def handle_connect():
    print("Connection established.")

def handle_notify():
    while True:
        if not queue_thread.empty():
            msg = queue_thread.get()
            if msg is None: 
                break
            socketio.emit('new-blocked', {'msg': msg})

@app.route('/')
def index():
    return "Hi!"

def read_logs():
    filename = "tmp/logs.txt"

    res = []
    with open(filename, 'r') as file:
        for line in file:
            array = line.split('|')
            if len(array) < 4:
                continue  # Skip malformed lines
            obs = {
                "id": array[0].strip(),
                "title": array[1].strip(),
                "message": array[2].strip(),
                "time": array[3].strip(),
            }

            res.append(obs)
    return res

# REST API
@app.route('/logs')
def get_logs():
    res = read_logs()
    return jsonify(res)

@app.route('/blocked_ips/<id>', methods=['DELETE'])
def delete_blocked_ip(id):
    print("IP: ", id)
    unblock_ip(id)
    return 'Blocked IP Logs...'

# PROPERTIES
app.debug = False
LOCALHOST = "0.0.0.0"
MY_IP = "192.168.1.77"
PORT = 5000  # Changed to integer for consistency

def run_api():
    socketio.run(app, host=LOCALHOST, port=PORT)

def run_firewall():
    print("Monitoring network traffic...")
    sniff(filter="ip", prn=packet_callback)

if __name__ == '__main__':
    
    if os.geteuid() != 0:
        print("This script requires root privileges.")
        sys.exit(1)
    
    whitelist_ips = read_ip_file("tmp/whitelist.txt")
    blacklist_ips = read_ip_file("tmp/blacklist.txt")

    packet_count = defaultdict(int)
    start_time = [time.time()]
    blocked_ips = set()

    queue_thread = queue.Queue()
    
    t1 = threading.Thread(target=run_firewall)
    t2 = threading.Thread(target=run_api)
    t3 = threading.Thread(target=handle_notify)

    t1.start()
    t2.start()
    t3.start()

    t1.join()
    t2.join()

    queue_thread.put(None)
    t3.join()
