from collections import defaultdict
from scapy.all import IP, sniff
import os
import time
import utils

class Firewall:
    def __init__(self):
        self.blocked_ips = set()
        self.start_time = time.time()
        self.packet_count = defaultdict(int)
        self.THRESHOLD = 40

        try:
            self.whitelist_ips = utils.read_ip_file("tmp/whitelist.txt")
            self.blacklist_ips = utils.read_ip_file("tmp/blacklist.txt")
        except FileNotFoundError as e:
            print(f"Error loading IP files: {e}")
            self.whitelist_ips = set()
            self.blacklist_ips = set()

    def run(self):
        print("Monitoring network traffic...")
        sniff(filter="ip", prn=self.packet_callback)

    def allow(self, ip):
        os.system(f"iptables -D INPUT -s {ip} -j ACCEPT")

    def deny(self, ip):
        os.system(f"iptables -A INPUT -s {ip} -j DROP")

    def status(self):
        return {
            "blocked_ips": list(self.blocked_ips),
            "whitelist_ips": list(self.whitelist_ips),
            "blacklist_ips": list(self.blacklist_ips)
        }

    def packet_callback(self, packet):
        if not packet.haslayer(IP):
            return

        src_ip = packet[IP].src

        if src_ip in self.whitelist_ips:
            return

        if src_ip in self.blacklist_ips:
            self.deny(src_ip)
            utils.log_event(f"Blocked blacklisted IP: {src_ip}")
            return

        if utils.is_nimda_worm(packet):
            print(f"Blocking Nimda source IP: {src_ip}")
            self.deny(src_ip)
            utils.log_event(f"Blocked Nimda source IP: {src_ip}")
            return

        self.packet_count[src_ip] += 1
        current_time = time.time()
        time_interval = current_time - self.start_time

        if time_interval >= 1:
            for ip, count in self.packet_count.items():
                packet_rate = count / time_interval

                if packet_rate > self.THRESHOLD and ip not in self.blocked_ips:
                    self.deny(ip)
                    utils.log_event(f"Blocked IP: {ip}, packet rate: {packet_rate}")
                    self.blocked_ips.add(ip)

            self.packet_count.clear()
            self.start_time = current_time