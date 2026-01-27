import socket

# Common port profiles
PORT_PROFILES = {
    "web": [80, 443, 8080, 8443],
    "database": [3306, 5432, 1433, 6379, 27017],
    "mail": [25, 587, 993, 995, 110, 143],
    "ftp": [21, 22],
    "remote": [3389, 22, 5900],
    "all": [21, 22, 23, 25, 53, 80, 110, 143, 443, 587, 6379, 3306, 3389, 5432, 8080, 8443, 27017]
}

def check_port(host, port, timeout=3):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except Exception:
        return False

def check_ports(host, ports, timeout=3):
    """Check multiple ports, returns dict with port:status"""
    results = {}
    for port in ports:
        results[port] = check_port(host, port, timeout)
    return results

def parse_port_input(port_input):
    """Parse various port input formats"""
    ports = []
    
    if port_input.lower() in PORT_PROFILES:
        return PORT_PROFILES[port_input.lower()]
    
    # Handle comma separated: 80,443,8080
    if ',' in port_input:
        for p in port_input.split(','):
            p = p.strip()
            if '-' in p:
                # Handle range: 8000-8100
                start, end = map(int, p.split('-'))
                ports.extend(range(start, end + 1))
            else:
                ports.append(int(p))
    elif '-' in port_input:
        # Handle single range: 8000-8100
        start, end = map(int, port_input.split('-'))
        ports.extend(range(start, end + 1))
    else:
        # Single port
        ports.append(int(port_input))
    
    return list(set(ports))  # Remove duplicates
