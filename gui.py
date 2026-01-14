import tkinter as tk
from tkinter import ttk, messagebox
from ping_checker import ping_host
from port_checker import check_port
from ip_scanner import generate_ip_range
from logger import log_result
import threading
import time

PORTS = [80, 3306]
DELAY = 0.1

class NetworkMonitorGUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Network Monitoring Tool")
        self.geometry("700x500")
        self.resizable(False, False)

        self.create_widgets()

    def create_widgets(self):
        frame = ttk.Frame(self, padding=10)
        frame.pack(fill="x")

        ttk.Label(frame, text="Scan Mode:").grid(row=0, column=0, sticky="w")

        self.mode = tk.StringVar(value="range")
        ttk.Radiobutton(frame, text="Hosts File", variable=self.mode, value="file").grid(row=0, column=1)
        ttk.Radiobutton(frame, text="IP Range", variable=self.mode, value="range").grid(row=0, column=2)

        ttk.Label(frame, text="Base IP (for range):").grid(row=1, column=0, sticky="w", pady=5)
        self.base_ip_entry = ttk.Entry(frame)
        self.base_ip_entry.insert(0, "192.168.1")
        self.base_ip_entry.grid(row=1, column=1, columnspan=2, sticky="we")

        self.start_button = ttk.Button(frame, text="Start Scan", command=self.start_scan)
        self.start_button.grid(row=2, column=0, columnspan=3, pady=10)

        self.output = tk.Text(self, height=22, bg="black", fg="white")
        self.output.pack(fill="both", padx=10, pady=5)

    def log(self, text):
        self.output.insert(tk.END, text + "\n")
        self.output.see(tk.END)

    def start_scan(self):
        self.output.delete(1.0, tk.END)
        thread = threading.Thread(target=self.scan)
        thread.start()

    def scan(self):
        if self.mode.get() == "file":
            try:
                with open("hosts.txt") as f:
                    hosts = [line.strip() for line in f if line.strip()]
            except FileNotFoundError:
                messagebox.showerror("Error", "hosts.txt not found")
                return
        else:
            base_ip = self.base_ip_entry.get().strip()
            if not base_ip:
                messagebox.showerror("Error", "Base IP required")
                return
            hosts = generate_ip_range(base_ip)

        self.log("=== Network Monitoring Tool ===")
        self.log("Starting scan...\n")

        for host in hosts:
            status, time_ms = ping_host(host)
            host_active = False

            if status:
                host_active = True
                self.log(f"[UP] {host} ({time_ms} ms)")
            else:
                self.log(f"[PING BLOCKED] {host}")

            for port in PORTS:
                if check_port(host, port):
                    host_active = True
                    self.log(f"   └─ Port {port}: OPEN")
                else:
                    self.log(f"   └─ Port {port}: CLOSED")

            if host_active:
                self.log("   => STATUS: ACTIVE\n")
                log_result(f"{host} ACTIVE")
            else:
                self.log("   => STATUS: INACTIVE\n")
                log_result(f"{host} INACTIVE")

            time.sleep(DELAY)

        self.log("Scan completed.")

if __name__ == "__main__":
    app = NetworkMonitorGUI()
    app.mainloop()
