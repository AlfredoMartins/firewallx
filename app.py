import random

def generate_random_ip():
    return f"192.168.1.{random.randint(0, 20)}"

def check_firewall_rules(ip, firewall_rules):
    if ip in firewall_rules:
        return "allowed"
    return "blocked"

def main():
    firewall_rules = {
        "192.168.1.1" : "?",
        "192.168.1.4" : "?",
        "192.168.1.9" : "?",
        "192.168.1.13" : "?",
        "192.168.1.16" : "?",
        "192.168.1.19" : "?"
    }

    for _ in range(12):
        ip_address = generate_random_ip()
        action = check_firewall_rules(ip_address, firewall_rules)
        random_number = random.randint(0, 9999)
        print(f"{'IP:':<10}{ip_address:<15} {'ACTION:':<10}{action:<10} {'RANDOM:':<10}{random_number:<10}")

if __name__ == "__main__":
    main()