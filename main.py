from ping_checker import ping_host
from port_checker import check_port
from logger import log_result
from colorama import Fore, Style, init

init(autoreset=True)

PORTS = [80, 3306]

def load_hosts():
    with open("hosts.txt") as f:
        return [line.strip() for line in f if line.strip()]

def main():
    hosts = load_hosts()

    print(Fore.CYAN + "=== Network Monitoring Tool ===\n")

    for host in hosts:
        status, time_ms = ping_host(host)

        if status:
            line = f"[UP] {host} ({time_ms} ms)"
            print(Fore.GREEN + line)
            log_result(line)

            for port in PORTS:
                port_status = check_port(host, port)
                if port_status:
                    port_line = f"Port {port}: OPEN"
                    print(Fore.YELLOW + f"   └─ {port_line}")
                else:
                    port_line = f"Port {port}: CLOSED"
                    print(Fore.RED + f"   └─ {port_line}")

                log_result(f"{host} - {port_line}")
        else:
            line = f"[DOWN] {host}"
            print(Fore.RED + line)
            log_result(line)

        print()

if __name__ == "__main__":
    main()
