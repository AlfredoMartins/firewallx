import os
import sys
import time
from collections import defaultdict
from scapy.all import sniff, IP, TCP  # type: ignore
#import socketio, app, __init__
import threading
import queue
import __init__ 
from flask_socketio import SocketIO

from __init__ import app, config

THRESHOLD = 40
print(f"THRESHOLD: {THRESHOLD}")

# SOCKET

def run_api():
    socketio = SocketIO(app, cors_allowed_origins=["http://localhost:5173", "http://192.168.1.77:5173"],  manage_session=True)
    socketio.init_app(app)
    
    socketio.run(app, host= config.HOST,
            port= config.PORT, 
            debug= config.DEBUG)

def run_firewall():
    print("Monitoring network traffic...")
    sniff(filter="ip", prn=packet_callback)

if __name__ == '__main__':
    
    if os.geteuid() != 0:
        print("This script requires root privileges.")
        sys.exit(1)

    app.run(host= config.HOST, port= config.PORT, debug= config.DEBUG)
        
    from utils import read_ip_file

    whitelist_ips = read_ip_file("tmp/whitelist.txt")
    blacklist_ips = read_ip_file("tmp/blacklist.txt")

    packet_count = defaultdict(int)
    start_time = [time.time()]
    blocked_ips = set()

    queue_thread = queue.Queue()
    
    t1 = threading.Thread(target=run_firewall)
    t2 = threading.Thread(target=run_api)

    from utils import handle_notify

    t3 = threading.Thread(target=handle_notify)

    t1.start()
    t2.start()
    t3.start()

    t1.join()
    t2.join()

    queue_thread.put(None)
    t3.join()