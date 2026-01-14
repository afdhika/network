from datetime import datetime

def log_result(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("network_log.txt", "a") as f:
        f.write(f"[{timestamp}] {message}\n")
