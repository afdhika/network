# Network Monitoring Tool

Network Monitoring Tool is a **Windows-based network monitoring application** built with Python.  
This project is designed as a **portfolio project** to demonstrate real-world skills commonly required for **IT Support, Network Engineer, and Junior System Administrator** roles.

The application started as a CLI-based tool and was gradually improved into a **GUI application**, packaged into a **Windows executable (.exe)**, and finally distributed using a **Windows installer (setup.exe)**.

---

## ✨ Key Features

### 🔍 Network Scanning
- Ping hosts to check device availability on the network
- Scan IP ranges within a subnet (example: `192.168.1.1 – 192.168.1.254`)
- Detect active hosts even when ICMP (ping) is blocked by checking open ports

### 🔌 Port Checking
- Check common service ports such as:
  - HTTP (Port 80)
  - MySQL (Port 3306)
- Identify whether services are **OPEN** or **CLOSED**
- Help simulate basic service availability monitoring

### ⚙️ Performance & Stability
- Uses **multithreading** to prevent GUI freezing during scans
- Configurable delay between scans to avoid network flooding
- Handles basic input validation and runtime errors

### 📝 Logging
- Automatically logs scan results to a log file
- Records whether hosts are ACTIVE or INACTIVE
- Useful for monitoring history and troubleshooting

### 📦 Windows Deployment
- Converted into a standalone Windows executable using **PyInstaller**
- Custom application icon for branding
- Distributed via a **Windows installer (setup.exe)** created with **Inno Setup**
- Installer features:
  - Guided installation wizard
  - Optional desktop shortcut
  - Clean installation directory

---

## 🛠️ Technologies Used

- **Python 3**
- **Tkinter** (GUI development)
- **Socket & Subprocess** (network operations)
- **Multithreading**
- **PyInstaller** (EXE packaging)
- **Inno Setup** (Windows installer creation)

---

## 📂 Project Structure

```
network-monitor/
├── gui.py                # Main GUI application
├── main.py               # CLI version (initial development)
├── ping_checker.py       # Ping functionality
├── port_checker.py       # Port scanning logic
├── ip_scanner.py         # IP range generation
├── logger.py             # Logging system
├── hosts.txt             # Custom hosts list
├── icon.ico              # Application icon
├── README.md             # Project documentation
└── dist/
    └── NetworkMonitor.exe
```

---

## ▶️ How to Run (Development Mode)

Make sure Python 3 is installed:

```bash
python gui.py
```

---

## 🎯 Use Case Scenarios

This application simulates tasks such as:
- Checking active devices in a local network
- Monitoring basic service availability
- Learning subnet scanning concepts
- Practicing network troubleshooting fundamentals

Suitable for:
- IT Support
- Network Engineer (Junior)
- System Administrator (Entry-level)
- Students learning networking concepts

---

## ⚠️ Disclaimer

This tool is created for **educational and portfolio purposes only**.  
Only use this application on networks you own or have explicit permission to test.

---

## 👤 Author

**Afdhika Syahputra**  
Aspiring IT Support / Network Engineer  
Indonesia 🇮🇩
