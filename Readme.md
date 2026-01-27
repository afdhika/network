# Network Monitoring Tool

Network Monitoring Tool is a **Windows-based network monitoring application** built with Python.  
This project is designed as a **portfolio project** to demonstrate real-world skills commonly required for **IT Support, Network Engineer, and Junior System Administrator** roles.

The application started as a **CLI-based tool**, then evolved into a **GUI-based application**, and finally packaged into **Windows executable (.exe)** files for easier usage without requiring Python.

---

## ✨ Key Features

### 🔍 Network Scanning
- Ping hosts to check device availability on the network
- Scan IP ranges within a subnet (example: `192.168.1.1 – 192.168.1.254`)
- Detect active hosts even when ICMP (ping) is blocked by checking open ports
- Support for both `hosts.txt` file and IP range scanning

### 🔌 **Advanced Port Checking** ⭐ *NEW*
- **Custom Port Profiles**: Pre-configured port sets for specific services:
  - `web`: HTTP/HTTPS ports (80, 443, 8080, 8443)
  - `database`: Database services (3306, 5432, 1433, 6379, 27017)
  - `mail`: Email services (25, 587, 993, 995, 110, 143)
  - `ftp`: File transfer (21, 22)
  - `remote`: Remote access (3389, 22, 5900)
  - `all`: Comprehensive scan of all common ports
- **Flexible Port Input**:
  - Single ports: `80`
  - Multiple ports: `80,443,8080`
  - Port ranges: `8000-8100`
  - Combined: `80,443,8000-8100`
- Real-time port status detection (OPEN/CLOSED)

### 🌐 Network Information Display ⭐ *NEW*
- **Real-time network configuration** - Detect current network settings
- **Multi-interface support** - Switch between Wi-Fi, Ethernet, etc.
- **System integration** - Pulls data from Windows/Linux/Mac network configuration
- **Auto IP detection** - Automatically fills base IP from current network
- **Copy to clipboard** - Easy sharing of network details
- **Cross-platform** - Works on Windows, Linux, and macOS

### 🖥️ Enhanced Graphical User Interface (GUI)
- User-friendly interface built with **Tkinter**
- **Interactive port selection** with dropdown profiles and custom input
- Supports:
  - Hosts scanning from `hosts.txt`
  - IP range scanning
- Real-time scan output with color indicators
- Progress bar and scan status display
- No terminal interaction required
- **Auto-creation** of `hosts.txt` if missing

### ⚙️ Performance & Stability
- Uses **multithreading** to speed up scanning tasks
- Configurable delay between scans to avoid network flooding
- Handles basic input validation and runtime errors
- **Error handling** for invalid port inputs

### 📝 Logging
- Automatically logs scan results to a log file
- Records whether hosts are ACTIVE or INACTIVE
- Useful for monitoring history and troubleshooting

---

## 🛠️ Technologies Used

- **Python 3**
- **Socket & Subprocess** (network operations)
- **Multithreading**
- **Tkinter** (GUI)
- **Colorama** (CLI colors)
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
# Install dependencies (if needed)
pip install colorama

# Run CLI version
python main.py

# Run GUI version
python gui.py
```

---

## 🎯 How to Use

### GUI Version (Recommended)

1. **Choose Scan Mode**:
   - `hosts.txt`: Scan predefined hosts from file
   - `IP Range`: Scan entire subnet (e.g., 192.168.1)

2. **Configure Ports**:
   - Select from dropdown: `web`, `database`, `mail`, `ftp`, `remote`, `all`
   - Or enter custom ports: `80,443,8080` or `8000-8100`

3. **View Network Information**:
   - Check your current network configuration at the top
   - Switch between different network interfaces (Wi-Fi, Ethernet)
   - Copy network details to clipboard for sharing
   - Base IP auto-fills from your current network

4. **Start Scanning**:
   - Click "▶ Start Scan" to begin
   - Monitor real-time results
   - View progress and status

### CLI Version

```bash
python main.py
```

Follow the interactive prompts:
1. Choose scan mode (1/2)
2. Enter ports or select profile
3. Specify IP range if needed
4. View results in real-time

---

## 📊 Port Reference

| Profile | Ports | Services |
|---------|-------|----------|
| `web` | 80, 443, 8080, 8443 | HTTP/HTTPS servers |
| `database` | 3306, 5432, 1433, 6379, 27017 | MySQL, PostgreSQL, MSSQL, Redis, MongoDB |
| `mail` | 25, 587, 993, 995, 110, 143 | SMTP, IMAP, POP3 |
| `ftp` | 21, 22 | FTP, SFTP |
| `remote` | 3389, 22, 5900 | RDP, SSH, VNC |
| `all` | 21, 22, 23, 25, 53, 80, 110, 143, 443, 587, 6379, 3306, 3389, 5432, 8080, 8443, 27017 | All common services |

---

## � Network Information Explained

### 📡 What is Network Information?

The **Network Information Display** shows your **current network configuration**, not scan results. Think of it as your computer's "network ID card."

### 🔍 How It Works

**Data Sources:**
- **System Configuration** - Windows/Linux/Mac network settings
- **Network Adapters** - Physical hardware information
- **Router/ISP** - Gateway and DNS settings
- **IP Protocol** - Socket-based detection

### 📋 What Each Field Means

| Field | Source | Example | Purpose |
|-------|--------|---------|---------|
| **Interface** | Network adapter name | `Wi-Fi`, `Ethernet` | Select which network to use |
| **Local IP** | System IP configuration | `192.168.1.100` | Your computer's address |
| **Gateway** | Router configuration | `192.168.1.1` | Your network's exit point |
| **DNS Servers** | System DNS settings | `8.8.8.8`, `1.1.1.1` | Domain name resolution |
| **MAC Address** | Hardware identifier | `00:11:22:33:44:55` | Unique device ID |

### 🎯 Key Differences

| Network Information | Scan Results |
|-------------------|-------------|
| **Static** configuration | **Dynamic** discovery |
| Your computer's settings | Other devices on network |
| Changes when you move networks | Changes when devices go online/offline |
| Like your home address | Like neighborhood directory |

### 💡 Practical Uses

**Network Information helps you:**
- **Auto-fill IP ranges** - Base IP automatically set
- **Troubleshoot connectivity** - Check gateway/DNS issues
- **Share network details** - Copy for IT support
- **Switch interfaces** - Use Wi-Fi vs Ethernet
- **Verify configuration** - Ensure correct settings

### 🔄 When Does It Change?

**Network info updates when:**
- **Connect to different network** (new Wi-Fi, office, cafe)
- **Switch network adapters** (Wi-Fi ↔ Ethernet)
- **Router restart** (gateway may change)
- **ISP configuration change** (DNS updates)
- **System network reset** (IP reassignment)

**Note:** Network info is **not affected** by scanning other devices. It shows **your** computer's network configuration.

---

## � Use Case Scenarios

This application simulates tasks such as:
- **Network Discovery**: Find active devices in a local network
- **Service Monitoring**: Check availability of web servers, databases, mail servers
- **Security Auditing**: Identify open ports and potential vulnerabilities
- **Troubleshooting**: Diagnose network connectivity issues
- **Learning**: Practice subnet scanning and port scanning concepts

**Perfect for:**
- IT Support Technicians
- Network Engineers (Junior)
- System Administrators (Entry-level)
- Cybersecurity Students
- Network Administrators

---

## 📁 Project Structure

```
network-monitor/
├── main.py              # CLI version
├── gui.py               # GUI version
├── ping_checker.py      # Ping functionality
├── port_checker.py      # Port scanning (NEW: Custom profiles)
├── ip_scanner.py        # IP range generation
├── logger.py            # Logging system
├── hosts.txt            # Host list (auto-created)
├── logs/                # Scan results directory
├── dist/                # Compiled executables
└── README.md            # This file
```

---

## 🚀 Recent Updates (v2.0)

### ✨ New Features:
- **Custom Port Profiles**: Pre-configured port sets for different services
- **Flexible Port Input**: Support for ranges, comma-separated values, and profiles
- **Enhanced GUI**: Interactive port selection with dropdown
- **Network Information Display**: Real-time network configuration detection
- **Export Functionality**: CSV/JSON export with metadata
- **Better Error Handling**: Invalid input detection and user-friendly messages
- **Improved CLI**: Interactive port selection with profile hints

### 🔧 Improvements:
- Faster port scanning with optimized socket operations
- Better memory management for large IP ranges
- Enhanced logging with more detailed information
- Auto-creation of configuration files

---

## ⚠️ Disclaimer

This tool is created for **educational and portfolio purposes only**.  
Only use this application on networks you own or have explicit permission to test.

**Important**: 
- Respect network security policies
- Do not use for unauthorized network scanning
- Follow ethical hacking guidelines

---

## 🤝 Contributing

This is a personal portfolio project, but feel free to:
- Report issues or bugs
- Suggest improvements
- Fork for educational purposes

---

## 👤 Author

**Afdhika Syahputra**  
Aspiring IT Support / Network Engineer  
Indonesia 🇮🇩

📧 Contact: https://afdhikasyahputra.carrd.co  
🔗 GitHub: https://github.com/afdhika  
💼 LinkedIn: https://www.linkedin.com/in/afdhika-syahputra-5b83b6318

---

## 📋 Future Roadmap

- [ ] **Real-time Monitoring**: Auto-scan with desktop notifications
- [ ] **Network Performance Metrics**: Response time graphs and statistics
- [ ] **DNS Tools**: DNS lookup and reverse DNS
- [ ] **Dark/Light Theme**: UI theme customization
- [ ] **Configuration Files**: Save/load scan profiles
- [ ] **Advanced Filters**: Filter scan results by status, ports, etc.
