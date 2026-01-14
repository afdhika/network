from ping_checker import ping_host
from port_checker import check_port
from logger import log_result
from ip_scanner import generate_ip_range
from colorama import Fore, init
import time

init(autoreset=True)

PORTS = [80, 3306]

def main():
    print(Fore.CYAN + "=== Network Monitoring Tool ===")
    print("1. Scan hosts from hosts.txt")
    print("2. Scan IP range (example: 192.168.1.1 - 254)\n")

    choice = input("Choose mode (1/2): ").strip()

    if choice == "1":
        with open("hosts.txt") as f:
            hosts = [line.strip() for line in f if line.strip()]
    elif choice == "2":
        base_ip = input("Enter base IP (example 192.168.1): ").strip()
        hosts = generate_ip_range(base_ip)
    else:
        print(Fore.RED + "Invalid choice")
        return

    print("\nStarting scan...\n")

    for host in hosts:
        status, time_ms = ping_host(host)
        host_active = False

        if status:
            host_active = True
            print(Fore.GREEN + f"[UP] {host} ({time_ms} ms)")
        else:
            print(Fore.RED + f"[PING BLOCKED] {host}")

        for port in PORTS:
            port_open = check_port(host, port)

            if port_open:
                host_active = True
                print(Fore.YELLOW + f"   └─ Port {port}: OPEN")
            else:
                print(Fore.RED + f"   └─ Port {port}: CLOSED")

        if host_active:
            print(Fore.GREEN + f"   => STATUS: ACTIVE")
            log_result(f"{host} ACTIVE")
        else:
            print(Fore.RED + f"   => STATUS: INACTIVE")
            log_result(f"{host} INACTIVE")

        time.sleep(0.1)

        print()


if __name__ == "__main__":
    main()
