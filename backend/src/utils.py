import os
import time
from scapy.all import TCP

def read_ip_file(filename):
    try:
        with open(filename, "r") as file:
            return {line.strip() for line in file}
    except FileNotFoundError:
        return set()

def is_nimda_worm(packet):
    if packet.haslayer(TCP) and packet[TCP].dport == 80:
        payload = str(packet[TCP].payload)
        return "GET /scripts/root.exe" in payload
    return False

def log_event(message):
    log_folder = "logs"
    os.makedirs(log_folder, exist_ok=True)
    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
    log_file = os.path.join(log_folder, f"log_{timestamp}.txt")

    with open(log_file, "a") as file:
        file.write(f"{message}\n")
