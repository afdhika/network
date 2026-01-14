# Network Monitoring Tool

A Python-based network monitoring tool designed to simulate real-world IT Support and Network Engineer tasks.

## Features
- Ping multiple hosts
- Detect active hosts even when ICMP is blocked
- Scan IP range within a subnet (e.g. 192.168.1.1–254)
- Check service ports (HTTP, MySQL, etc.)
- Log scan results automatically
- Colored CLI output for better readability
- Packaged as Windows executable (.exe)

## Tools & Technologies
- Python 3
- Socket
- Subprocess
- Colorama
- PyInstaller

## How It Works
1. Choose scan mode:
   - Scan predefined hosts from file
   - Scan IP range in a subnet
2. Tool checks:
   - Host availability
   - Open/closed ports
3. Results are displayed and saved to log file

## Use Case
This tool simulates basic network monitoring activities commonly performed by IT Support and Network Engineers in production environments.

## Disclaimer
This tool is intended for educational purposes and should only be used on networks you own or have permission to test.
