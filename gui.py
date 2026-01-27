import tkinter as tk
from tkinter import ttk, messagebox
from ping_checker import ping_host
from port_checker import check_ports, parse_port_input, PORT_PROFILES
from ip_scanner import generate_ip_range
from logger import log_result
from export_utils import ExportManager
from network_info import NetworkInfo
import threading
import time
import os

DELAY = 0.01  # Faster scanning (10ms per host)

class NetworkMonitorGUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Network Monitoring Tool v2.0")
        self.geometry("800x620")
        
        # Style Configuration
        self.setup_style()
        self.create_widgets()
        
        # Initialize export manager
        self.export_manager = ExportManager()
        
        # Initialize network info
        self.network_info = NetworkInfo()
        
        # Setup Tags untuk warna teks di output
        self.output.tag_config("up", foreground="#4ade80")   # Hijau
        self.output.tag_config("down", foreground="#f87171") # Merah
        self.output.tag_config("port", foreground="#fbbf24") # Kuning
        self.output.tag_config("info", foreground="#60a5fa") # Biru
        
        # Initialize network info after UI is ready
        self.after(100, self.initialize_network_info)

    def setup_style(self):
        style = ttk.Style(self)
        style.theme_use("clam") # Tema clam lebih fleksibel untuk kustomisasi
        style.configure("TButton", font=("Segoe UI", 9))
        style.configure("Main.TFrame", background="#f3f4f6")

    def create_widgets(self):
        # Container Utama
        main_frame = ttk.Frame(self, padding=20)
        main_frame.pack(fill="both", expand=True)

        # Network Information Section
        info_group = ttk.LabelFrame(main_frame, text=" Network Information ", padding=10)
        info_group.pack(fill="x", pady=(0, 10))

        # Interface selection
        interface_frame = ttk.Frame(info_group)
        interface_frame.pack(fill="x", pady=(0, 5))
        
        ttk.Label(interface_frame, text="Interface:").pack(side="left", padx=5)
        self.interface_var = tk.StringVar()
        self.interface_combo = ttk.Combobox(interface_frame, textvariable=self.interface_var, width=20, state="readonly")
        self.interface_combo.pack(side="left", padx=5)
        self.interface_combo.bind("<<ComboboxSelected>>", self.on_interface_change)
        
        ttk.Button(interface_frame, text="🔄 Refresh", command=self.refresh_network_info).pack(side="left", padx=5)
        ttk.Button(interface_frame, text="📋 Copy", command=self.copy_network_info).pack(side="left", padx=5)

        # Network info display
        self.info_text = tk.Text(info_group, height=3, bg="#f8fafc", fg="#1e293b", font=("Consolas", 9), borderwidth=1)
        self.info_text.pack(fill="x", pady=5)
        
        # Configuration Section
        input_group = ttk.LabelFrame(main_frame, text=" Scan Configuration ", padding=10)
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

        ttk.Label(input_group, text="Delay:").grid(row=3, column=0, padx=5, sticky="w")
        delay_frame = ttk.Frame(input_group)
        delay_frame.grid(row=3, column=1, padx=5, pady=5, sticky="w")
        
        self.delay_var = tk.StringVar(value="10")
        self.delay_entry = ttk.Entry(delay_frame, width=5, textvariable=self.delay_var)
        self.delay_entry.pack(side="left", padx=(0, 5))
        
        ttk.Label(delay_frame, text="ms").pack(side="left")

        # Buttons
        btn_frame = ttk.Frame(input_group)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=10, sticky="w")
        
        self.start_button = ttk.Button(btn_frame, text="▶ Start Scan", command=self.start_scan)
        self.start_button.pack(side="left", padx=5)
        
        ttk.Button(btn_frame, text="🧹 Clear", command=self.clear_output).pack(side="left", padx=5)
        
        # Export buttons
        export_frame = ttk.Frame(btn_frame)
        export_frame.pack(side="left", padx=10)
        
        ttk.Button(export_frame, text="📄 CSV", command=self.export_csv).pack(side="left", padx=2)
        ttk.Button(export_frame, text="📋 JSON", command=self.export_json).pack(side="left", padx=2)

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
        self.export_manager.clear_results()

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

            # Save result to export manager
            self.export_manager.add_result(host, time_ms, port_results, 'ACTIVE' if active else 'INACTIVE')

            # Logging ke file
            log_result(f"{host} {'ACTIVE' if active else 'INACTIVE'}")
            
            self.progress["value"] = i
            
            # Use configurable delay
            try:
                delay_ms = float(self.delay_var.get())
                delay_sec = delay_ms / 1000.0
                time.sleep(delay_sec)
            except:
                time.sleep(0.01)  # Fallback to 10ms

        self.log("--- Scan Completed ---", "info")
        self.reset_ui()

    def reset_ui(self):
        self.status_label.config(text="DONE", foreground="#7c3aed")
        self.start_button.config(state="normal")
        
        # Show summary stats
        stats = self.export_manager.get_summary_stats()
        if stats:
            self.log(f"[SUMMARY] Total: {stats['total_hosts']}, Active: {stats['active_hosts']}, Success Rate: {stats['success_rate']}", "info")

    def export_csv(self):
        if self.export_manager.export_csv(self):
            messagebox.showinfo("Export Success", "Results exported to CSV successfully!")
    
    def export_json(self):
        if self.export_manager.export_json(self):
            messagebox.showinfo("Export Success", "Results exported to JSON successfully!")

    def refresh_network_info(self):
        """Refresh network information display"""
        try:
            # Update interface list
            self.network_info.refresh_interfaces()
            self.interface_combo['values'] = self.network_info.interfaces
            
            # Select current interface if not set
            if not self.interface_var.get() and self.network_info.interfaces:
                self.interface_var.set(self.network_info.interfaces[0])
            
            # Get and display network info
            interface = self.interface_var.get() or self.network_info.current_interface
            info = self.network_info.get_network_info(interface)
            
            # Format and display info
            info_text = f"🌐 {info['interface']}\n"
            info_text += f"📍 IP: {info['local_ip']} | 📡 Gateway: {info['gateway']}\n"
            info_text += f"🔍 DNS: {', '.join(info['dns_servers'][:2])} | 📋 MAC: {info['mac_address'][:8]}..."
            
            self.info_text.delete(1.0, tk.END)
            self.info_text.insert(1.0, info_text)
            
            # Auto-fill base IP with local IP range
            if info['local_ip'] != "Unknown":
                base_ip = '.'.join(info['local_ip'].split('.')[:-1])
                self.base_ip_entry.delete(0, tk.END)
                self.base_ip_entry.insert(0, base_ip)
            
        except Exception as e:
            self.info_text.delete(1.0, tk.END)
            self.info_text.insert(1.0, f"❌ Error: {str(e)}")

    def on_interface_change(self, event):
        """Handle interface selection change"""
        self.refresh_network_info()

    def copy_network_info(self):
        """Copy network information to clipboard"""
        try:
            interface = self.interface_var.get() or self.network_info.current_interface
            info = self.network_info.get_network_info(interface)
            
            copy_text = f"""Network Information:
Interface: {info['interface']}
Local IP: {info['local_ip']}
Subnet Mask: {info['subnet_mask']}
Gateway: {info['gateway']}
DNS Servers: {', '.join(info['dns_servers'])}
MAC Address: {info['mac_address']}
Network Range: {self.network_info.get_network_range(interface)}"""
            
            if self.network_info.copy_to_clipboard(copy_text):
                messagebox.showinfo("Success", "Network information copied to clipboard!")
            else:
                messagebox.showwarning("Warning", "Failed to copy to clipboard")
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to copy: {str(e)}")

    def initialize_network_info(self):
        """Initialize network info on startup"""
        self.refresh_network_info()

if __name__ == "__main__":
    app = NetworkMonitorGUI()
    app.mainloop()
