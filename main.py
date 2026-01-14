from ping_checker import ping_host
from port_checker import check_port
from logger import log_result

PORTS = [80, 3306]

def load_hosts():
    with open("hosts.txt") as f:
        return [line.strip() for line in f if line.strip()]

def main():
    hosts = load_hosts()

    print("=== Network Monitoring Tool ===\n")

    for host in hosts:
        status, time_ms = ping_host(host)

        if status:
            line = f"[UP] {host} ({time_ms} ms)"
            print(line)
            log_result(line)

            for port in PORTS:
                port_status = "OPEN" if check_port(host, port) else "CLOSED"
                port_line = f"Port {port}: {port_status}"
                print(f"   └─ {port_line}")
                log_result(f"{host} - {port_line}")
        else:
            line = f"[DOWN] {host}"
            print(line)
            log_result(line)


        print()

if __name__ == "__main__":
    main()
