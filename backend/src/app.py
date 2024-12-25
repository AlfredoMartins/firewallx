import os
import sys
import concurrent
import queue
from __init__ import app, firewall, config
from flask_socketio import SocketIO

socketio = SocketIO(app, cors_allowed_origins=["http://localhost:5173", "http://192.168.1.77:5173"], manage_session=True)

def handle_notify():
    while True:
        if not queue_thread.empty():
            msg = queue_thread.get()
            if msg is None: 
                break
            socketio.emit('new-blocked', {'msg': msg})

if __name__ == '__main__':
    
    if os.geteuid() != 0:
        print("This script requires root privileges.")
        sys.exit(1)

    queue_thread = queue.Queue()    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future1 = executor.submit(firewall.run)
        future2 = executor.submit(handle_notify)

        socketio.run(app, host=config.HOST, port=config.PORT, debug=config.DEBUG)
        concurrent.futures.wait([future1, future2])

    queue_thread.put(None)