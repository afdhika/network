from ping_checker import ping_host

def load_hosts():
    with open("hosts.txt") as f:
        return [line.strip() for line in f if line.strip()]

def main():
    hosts = load_hosts()

    print("=== Network Ping Check ===\n")

    for host in hosts:
        status = "UP" if ping_host(host) else "DOWN"
        print(f"[{status}] {host}")

if __name__ == "__main__":
    main()
