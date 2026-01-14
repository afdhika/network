def generate_ip_range(base_ip):
    """
    base_ip contoh: 192.168.1
    hasil: list IP 192.168.1.1 - 192.168.1.254
    """
    return [f"{base_ip}.{i}" for i in range(1, 255)]
