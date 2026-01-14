import subprocess
import re

def ping_host(host):
    try:
        result = subprocess.run(
            ["ping", "-n", "1", host],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            return False, None

        match = re.search(r"time[=<]\s*(\d+)ms", result.stdout)
        time_ms = match.group(1) if match else None

        return True, time_ms

    except Exception:
        return False, None
