from ping_checker import ping_host
from port_checker import check_ports, parse_port_input, PORT_PROFILES
from logger import log_result
from ip_scanner import generate_ip_range
from colorama import Fore, init
import time
import os
import sys

def get_base_dir():
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS  # exe
    return os.path.dirname(os.path.abspath(__file__))  # python

BASE_DIR = get_base_dir()
HOSTS_FILE = os.path.join(BASE_DIR, "hosts.txt")
LOG_DIR = os.path.join(os.getcwd(), "logs")

if not os.path.exists(HOSTS_FILE):
    with open(HOSTS_FILE, "w") as f:
        f.write("8.8.8.8\n")

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

init(autoreset=True)

def main():
    print(Fore.CYAN + "=== Network Monitoring Tool ===")
    print("1. Scan hosts from hosts.txt")
    print("2. Scan IP range (example: 192.168.1.1 - 254)\n")

    choice = input("Choose mode (1/2): ").strip()

    # Port selection
    print(f"\nAvailable port profiles: {', '.join(PORT_PROFILES.keys())}")
    port_input = input("Enter ports (e.g: 80,443,3306 or 8000-8100 or 'web'): ").strip()
    
    try:
        if port_input.lower() in PORT_PROFILES:
            ports = PORT_PROFILES[port_input.lower()]
            print(f"Using profile '{port_input}': {ports}")
        else:
            ports = parse_port_input(port_input) if port_input else [80, 443, 3306]
    except Exception as e:
        print(Fore.RED + f"Invalid port format: {e}")
        return

    if choice == "1":
        with open(HOSTS_FILE) as f:
            hosts = [line.strip() for line in f if line.strip()]
    elif choice == "2":
        base_ip = input("Enter base IP (example 192.168.1): ").strip()
        hosts = generate_ip_range(base_ip)
    else:
        print(Fore.RED + "Invalid choice")
        return

    print(f"\nStarting scan: {len(hosts)} hosts, {len(ports)} ports...\n")

    for host in hosts:
        status, time_ms = ping_host(host)
        host_active = False

        if status:
            host_active = True
            print(Fore.GREEN + f"[UP] {host} ({time_ms} ms)")
        else:
            print(Fore.RED + f"[PING BLOCKED] {host}")

        # Check ports
        port_results = check_ports(host, ports)
        for port, is_open in port_results.items():
            if is_open:
                host_active = True
                print(Fore.YELLOW + f"   └─ Port {port}: OPEN")
            else:
                print(Fore.RED + f"   └─ Port {port}: CLOSED")

        if host_active:
            print(Fore.GREEN + "   => STATUS: ACTIVE")
            log_result(f"{host} ACTIVE")
        else:
            print(Fore.RED + "   => STATUS: INACTIVE")
            log_result(f"{host} INACTIVE")

        time.sleep(0.1)
        print()

if __name__ == "__main__":
    main()
