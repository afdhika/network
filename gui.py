import tkinter as tk
from tkinter import ttk, messagebox
from ping_checker import ping_host
from port_checker import check_port
from ip_scanner import generate_ip_range
from logger import log_result
import threading
import time
import os

PORTS = [80, 3306]
DELAY = 0.1

class NetworkMonitorGUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Network Monitoring Tool")
        self.geometry("780x580")
        self.resizable(False, False)

        if os.path.exists("icon.ico"):
            self.iconbitmap("icon.ico")

        self.setup_style()
        self.create_widgets()

    def setup_style(self):
        style = ttk.Style(self)
        style.theme_use("default")

        style.configure("TButton", padding=6)
        style.configure("Status.TLabel", font=("Segoe UI", 10, "bold"))

    def create_widgets(self):
        top = ttk.Frame(self, padding=10)
        top.pack(fill="x")

        ttk.Label(top, text="Scan Mode:").grid(row=0, column=0, sticky="w")

        self.mode = tk.StringVar(value="range")
        ttk.Radiobutton(top, text="Hosts File", variable=self.mode, value="file").grid(row=0, column=1)
        ttk.Radiobutton(top, text="IP Range", variable=self.mode, value="range").grid(row=0, column=2)

        ttk.Label(top, text="Base IP:").grid(row=1, column=0, sticky="w", pady=5)
        self.base_ip_entry = ttk.Entry(top, width=20)
        self.base_ip_entry.insert(0, "192.168.1")
        self.base_ip_entry.grid(row=1, column=1, columnspan=2, sticky="w")

        self.start_button = ttk.Button(top, text="▶ Start Scan", command=self.start_scan)
        self.start_button.grid(row=2, column=0, pady=10)

        ttk.Button(top, text="🧹 Clear", command=self.clear_output).grid(row=2, column=1)

        self.status_label = ttk.Label(top, text="IDLE", style="Status.TLabel", foreground="blue")
        self.status_label.grid(row=2, column=2)

        self.progress = ttk.Progressbar(self, length=740)
        self.progress.pack(padx=10, pady=5)

        self.output = tk.Text(
            self,
            height=22,
            bg="#020617",
            fg="#e5e7eb",
            insertbackground="white",
            font=("Consolas", 10)
        )
        self.output.pack(fill="both", padx=10, pady=5)

        footer = ttk.Label(
            self,
            text="© 2026 Afdhika Syahputra | Network Monitoring Tool",
            font=("Segoe UI", 9)
        )
        footer.pack(pady=5)

    def log(self, text):
        self.output.insert(tk.END, text + "\n")
        self.output.see(tk.END)

    def clear_output(self):
        self.output.delete(1.0, tk.END)

    def start_scan(self):
        self.clear_output()
        self.start_button.config(state="disabled")
        self.status_label.config(text="RUNNING", foreground="green")

        threading.Thread(target=self.scan, daemon=True).start()

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

        self.progress["maximum"] = len(hosts)
        self.progress["value"] = 0

        self.log("=== Network Monitoring Tool ===")
        self.log("Starting scan...\n")

        for i, host in enumerate(hosts, start=1):
            status, time_ms = ping_host(host)
            active = False

            if status:
                active = True
                self.log(f"[UP] {host} ({time_ms} ms)")
            else:
                self.log(f"[PING BLOCKED] {host}")

            for port in PORTS:
                if check_port(host, port):
                    active = True
                    self.log(f"   └─ Port {port}: OPEN")
                else:
                    self.log(f"   └─ Port {port}: CLOSED")

            if active:
                self.log("   => STATUS: ACTIVE\n")
                log_result(f"{host} ACTIVE")
            else:
                self.log("   => STATUS: INACTIVE\n")
                log_result(f"{host} INACTIVE")

            self.progress["value"] = i
            time.sleep(DELAY)

        self.status_label.config(text="DONE", foreground="purple")
        self.start_button.config(state="normal")
        self.log("Scan completed.")

if __name__ == "__main__":
    app = NetworkMonitorGUI()
    app.mainloop()
