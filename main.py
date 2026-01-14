from ping_checker import ping_host
from port_checker import check_port

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
            print(f"[UP]   {host} ({time_ms} ms)")
            for port in PORTS:
                port_status = "OPEN" if check_port(host, port) else "CLOSED"
                print(f"   └─ Port {port}: {port_status}")
        else:
            print(f"[DOWN] {host}")

        print()

if __name__ == "__main__":
    main()
