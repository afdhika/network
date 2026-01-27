import tkinter as tk
from tkinter import ttk, messagebox
from ping_checker import ping_host
from port_checker import check_ports, parse_port_input, PORT_PROFILES
from ip_scanner import generate_ip_range
from logger import log_result
import threading
import time
import os

DELAY = 0.05

class NetworkMonitorGUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Network Monitoring Tool v2.0")
        self.geometry("800x620")
        
        # Style Configuration
        self.setup_style()
        self.create_widgets()
        
        # Setup Tags untuk warna teks di output
        self.output.tag_config("up", foreground="#4ade80")   # Hijau
        self.output.tag_config("down", foreground="#f87171") # Merah
        self.output.tag_config("port", foreground="#fbbf24") # Kuning
        self.output.tag_config("info", foreground="#60a5fa") # Biru

    def setup_style(self):
        style = ttk.Style(self)
        style.theme_use("clam") # Tema clam lebih fleksibel untuk kustomisasi
        style.configure("TButton", font=("Segoe UI", 9))
        style.configure("Main.TFrame", background="#f3f4f6")

    def create_widgets(self):
        # Container Utama
        main_frame = ttk.Frame(self, padding=20)
        main_frame.pack(fill="both", expand=True)

        # Header/Input Section
        input_group = ttk.LabelFrame(main_frame, text=" Configuration ", padding=10)
        input_group.pack(fill="x", pady=(0, 10))

        ttk.Label(input_group, text="Mode:").grid(row=0, column=0, padx=5, sticky="w")
        self.mode = tk.StringVar(value="range")
        mode_frame = ttk.Frame(input_group)
        mode_frame.grid(row=0, column=1, sticky="w")
        ttk.Radiobutton(mode_frame, text="hosts.txt", variable=self.mode, value="file").pack(side="left", padx=5)
        ttk.Radiobutton(mode_frame, text="IP Range", variable=self.mode, value="range").pack(side="left", padx=5)

        ttk.Label(input_group, text="Base IP:").grid(row=1, column=0, padx=5, sticky="w")
        self.base_ip_entry = ttk.Entry(input_group, width=30)
        self.base_ip_entry.insert(0, "192.168.1")
        self.base_ip_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(input_group, text="Ports:").grid(row=2, column=0, padx=5, sticky="w")
        port_frame = ttk.Frame(input_group)
        port_frame.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        
        self.port_entry = ttk.Entry(port_frame, width=20)
        self.port_entry.insert(0, "80,443,3306")
        self.port_entry.pack(side="left", padx=(0, 5))
        
        self.port_profile = ttk.Combobox(port_frame, width=12, values=list(PORT_PROFILES.keys()))
        self.port_profile.set("custom")
        self.port_profile.pack(side="left")
        self.port_profile.bind("<<ComboboxSelected>>", self.on_port_profile_change)

        # Buttons
        btn_frame = ttk.Frame(input_group)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=10, sticky="w")
        
        self.start_button = ttk.Button(btn_frame, text="▶ Start Scan", command=self.start_scan)
        self.start_button.pack(side="left", padx=5)
        
        ttk.Button(btn_frame, text="🧹 Clear", command=self.clear_output).pack(side="left", padx=5)

        self.status_label = ttk.Label(btn_frame, text="IDLE", font=("Segoe UI", 10, "bold"), foreground="#64748b")
        self.status_label.pack(side="left", padx=20)

        # Progress
        self.progress = ttk.Progressbar(main_frame, orient="horizontal", mode="determinate")
        self.progress.pack(fill="x", pady=5)

        # Output Terminal
        self.output = tk.Text(
            main_frame, height=18, bg="#0f172a", fg="#f8fafc",
            font=("Consolas", 10), padx=10, pady=10, borderwidth=0
        )
        self.output.pack(fill="both", expand=True)

        # Footer
        footer = ttk.Label(self, text="© 2026 Afdhika Syahputra | Pro Version", font=("Segoe UI", 8))
        footer.pack(pady=5)

    def log(self, text, tag=None):
        self.output.insert(tk.END, text + "\n", tag)
        self.output.see(tk.END)

    def clear_output(self):
        self.output.delete(1.0, tk.END)
        self.progress["value"] = 0

    def on_port_profile_change(self, event):
        profile = self.port_profile.get()
        if profile in PORT_PROFILES:
            ports = PORT_PROFILES[profile]
            self.port_entry.delete(0, tk.END)
            self.port_entry.insert(0, ",".join(map(str, ports)))

    def start_scan(self):
        self.start_button.config(state="disabled")
        self.status_label.config(text="SCANNING...", foreground="#059669")
        threading.Thread(target=self.scan_logic, daemon=True).start()

    def scan_logic(self):
        # Get ports
        try:
            port_input = self.port_entry.get().strip()
            if not port_input:
                ports = [80, 443, 3306]  # Default
            else:
                ports = parse_port_input(port_input)
        except Exception as e:
            self.log(f"[ERROR] Invalid port format: {e}", "down")
            self.reset_ui()
            return

        # Ambil Host
        if self.mode.get() == "file":
            if not os.path.exists("hosts.txt"):
                # Auto-create hosts.txt
                with open("hosts.txt", "w") as f:
                    f.write(
                        "8.8.8.8\n"
                        "127.0.0.1\n"
                        "localhost\n"
                    )


                self.log("[INFO] hosts.txt tidak ditemukan, file dibuat otomatis.", "info")

            with open("hosts.txt") as f:
                hosts = [line.strip() for line in f if line.strip()]

            if not hosts:
                self.log("[WARNING] hosts.txt kosong.", "down")
                self.reset_ui()
                return

        else:
            base = self.base_ip_entry.get().strip()
            hosts = generate_ip_range(base)

        self.progress["maximum"] = len(hosts)
        self.log(f"--- Scan Started: {len(hosts)} hosts, {len(ports)} ports ---", "info")

        for i, host in enumerate(hosts, 1):
            is_up, time_ms = ping_host(host)
            active = False

            if is_up:
                active = True
                self.log(f"[UP] {host} ({time_ms}ms)", "up")
            else:
                self.log(f"[DOWN] {host}", "down")

            # Check ports
            port_results = check_ports(host, ports)
            for port, is_open in port_results.items():
                if is_open:
                    active = True
                    self.log(f"  └ Port {port}: OPEN", "port")

            # Logging ke file
            log_result(f"{host} {'ACTIVE' if active else 'INACTIVE'}")
            
            self.progress["value"] = i
            time.sleep(DELAY)

        self.log("--- Scan Completed ---", "info")
        self.reset_ui()

    def reset_ui(self):
        self.status_label.config(text="DONE", foreground="#7c3aed")
        self.start_button.config(state="normal")

if __name__ == "__main__":
    app = NetworkMonitorGUI()
    app.mainloop()
