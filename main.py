from ping_checker import ping_host
from port_checker import check_port
from logger import log_result
from ip_scanner import generate_ip_range
from colorama import Fore, init

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

        if status:
            print(Fore.GREEN + f"[UP] {host} ({time_ms} ms)")
            for port in PORTS:
                result = "OPEN" if check_port(host, port) else "CLOSED"
                print(f"   └─ Port {port}: {result}")
                log_result(f"{host} Port {port}: {result}")
        else:
            print(Fore.RED + f"[DOWN] {host}")
            log_result(f"{host} DOWN")

    print(Fore.CYAN + "\nScan completed.")

if __name__ == "__main__":
    main()
