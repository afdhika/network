# Network Monitoring Tool

Network Monitoring Tool is a **Windows-based network monitoring application** built with Python.  
This project is designed as a **portfolio project** to demonstrate real-world skills commonly required for **IT Support, Network Engineer, and Junior System Administrator** roles.

The application was developed as a **CLI-based tool**, then packaged into a **Windows executable (.exe)** and distributed using a **Windows installer (setup.exe)**.

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
- Uses **multithreading** to speed up scanning tasks
- Configurable delay between scans to avoid network flooding
- Handles basic input validation and runtime errors

### 📝 Logging
- Automatically logs scan results to a log file
- Records whether hosts are ACTIVE or INACTIVE
- Useful for monitoring history and troubleshooting

---

## 🛠️ Technologies Used

- **Python 3**
- **Socket & Subprocess** (network operations)
- **Multithreading**
- **PyInstaller** (EXE packaging)

---

## ▶️ How to Run

### 🖥️ Run Without Python (Recommended)
This project is already packaged as a Windows executable.

1. Open the `dist` folder  
2. Choose one of the following:
   - `gui.exe` → **GUI version (recommended)**
   - `main.exe` → CLI version  
3. Double-click the file to run the application  

📄 Log files are enabled by default and will be generated automatically.

---

### 🐍 Development Mode (Run with Python)
If you want to run or modify the source code, make sure **Python 3** is installed:

```bash
python main.py
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
