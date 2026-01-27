import socket
import subprocess
import platform
import re
from tkinter import messagebox

# Try to import psutil, but provide fallback if not available
try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False

class NetworkInfo:
    def __init__(self):
        self.interfaces = []
        self.current_interface = None
        self.refresh_interfaces()
    
    def refresh_interfaces(self):
        """Get all network interfaces"""
        try:
            if HAS_PSUTIL:
                self.interfaces = list(psutil.net_if_addrs().keys())
            else:
                # Fallback: Get interfaces from system commands
                system = platform.system().lower()
                if system == 'windows':
                    result = subprocess.run(['netsh', 'interface', 'show', 'interface'], capture_output=True, text=True)
                    self.interfaces = []
                    for line in result.stdout.split('\n'):
                        if 'Enabled' in line and not line.startswith('Admin'):
                            parts = line.split()
                            if len(parts) >= 4:
                                self.interfaces.append(parts[3])
                else:
                    # Linux/Mac fallback
                    self.interfaces = ['eth0', 'wlan0', 'en0', 'en1']
            
            if not self.interfaces:
                self.interfaces = ['Ethernet', 'Wi-Fi', 'Local Area Connection']
            
            # Auto-select first active interface
            self.current_interface = self.interfaces[0] if self.interfaces else None
        except:
            # Fallback if psutil not available
            self.interfaces = ['Ethernet', 'Wi-Fi', 'Local Area Connection']
            self.current_interface = 'Wi-Fi'
    
    def get_local_ip(self, interface=None):
        """Get local IP address"""
        try:
            # Try to get IP for specific interface if psutil available
            if interface and HAS_PSUTIL:
                addrs = psutil.net_if_addrs().get(interface, [])
                for addr in addrs:
                    if addr.family == socket.AF_INET and not addr.address.startswith('127.'):
                        return addr.address
            
            # Fallback: Create socket and get local IP
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "Unknown"
    
    def get_subnet_mask(self, interface=None):
        """Get subnet mask"""
        try:
            if interface and HAS_PSUTIL:
                addrs = psutil.net_if_addrs().get(interface, [])
                for addr in addrs:
                    if addr.family == socket.AF_INET and addr.netmask:
                        return addr.netmask
            
            # Fallback: Common subnet masks
            ip = self.get_local_ip(interface)
            if ip.startswith('192.168.1'):
                return '255.255.255.0'
            elif ip.startswith('10.0'):
                return '255.0.0.0'
            elif ip.startswith('172.16'):
                return '255.255.0.0'
            return '255.255.255.0'
        except:
            return '255.255.255.0'
    
    def get_default_gateway(self):
        """Get default gateway"""
        try:
            system = platform.system().lower()
            
            if system == 'windows':
                result = subprocess.run(['ipconfig'], capture_output=True, text=True)
                for line in result.stdout.split('\n'):
                    if 'Default Gateway' in line:
                        gateway = line.split(':')[-1].strip()
                        if gateway and gateway != '':
                            return gateway
            
            elif system == 'linux':
                with open('/proc/net/route') as f:
                    for line in f:
                        if line.startswith('00000000'):
                            return socket.inet_ntoa(bytes.fromhex(line.split()[2][::-1]))
            
            elif system == 'darwin':
                result = subprocess.run(['netstat', '-nr'], capture_output=True, text=True)
                for line in result.stdout.split('\n'):
                    if 'default' in line and 'UG' in line:
                        return line.split()[1]
        
        except:
            pass
        
        return "Unknown"
    
    def get_dns_servers(self):
        """Get DNS servers"""
        try:
            system = platform.system().lower()
            dns_servers = []
            
            if system == 'windows':
                result = subprocess.run(['nslookup', 'google.com'], capture_output=True, text=True)
                for line in result.stdout.split('\n'):
                    if 'Server:' in line:
                        dns = line.split(':')[-1].strip()
                        if dns and dns != '':
                            dns_servers.append(dns)
                            break
                
                # Try ipconfig as fallback
                if not dns_servers:
                    result = subprocess.run(['ipconfig', '/all'], capture_output=True, text=True)
                    for line in result.stdout.split('\n'):
                        if 'DNS Servers' in line:
                            dns = line.split(':')[-1].strip()
                            if dns and dns != '':
                                dns_servers.append(dns)
            
            elif system == 'linux':
                with open('/etc/resolv.conf') as f:
                    for line in f:
                        if line.startswith('nameserver'):
                            dns_servers.append(line.split()[1])
            
            elif system == 'darwin':
                result = subprocess.run(['scutil', '--dns'], capture_output=True, text=True)
                for line in result.stdout.split('\n'):
                    if 'nameserver' in line and '[' not in line:
                        dns = line.split(':')[-1].strip()
                        if dns and dns != '':
                            dns_servers.append(dns)
            
            return dns_servers if dns_servers else ['8.8.8.8', '8.8.4.4']  # Fallback to Google DNS
        
        except:
            return ['8.8.8.8', '8.8.4.4']
    
    def get_mac_address(self, interface=None):
        """Get MAC address"""
        try:
            if interface and HAS_PSUTIL:
                addrs = psutil.net_if_addrs().get(interface, [])
                for addr in addrs:
                    if hasattr(addr, 'family') and addr.family == psutil.AF_LINK:
                        return addr.address
            
            # Fallback: Get MAC of default interface
            system = platform.system().lower()
            
            if system == 'windows':
                result = subprocess.run(['getmac', '/v', '/fo', 'csv'], capture_output=True, text=True, timeout=10)
                for line in result.stdout.split('\n'):
                    if ',' in line and not line.startswith('"'):
                        parts = line.split(',')
                        if len(parts) >= 2:
                            mac = parts[0].strip('"')
                            if mac and mac != '':
                                return mac
            
            elif system == 'linux':
                result = subprocess.run(['ip', 'link', 'show'], capture_output=True, text=True, timeout=10)
                for line in result.stdout.split('\n'):
                    if 'link/ether' in line:
                        return line.split()[1]
            
            elif system == 'darwin':
                result = subprocess.run(['ifconfig'], capture_output=True, text=True, timeout=10)
                for line in result.stdout.split('\n'):
                    if 'ether' in line:
                        return line.split()[1]
        
        except:
            pass
        
        return "Unknown"
    
    def get_network_info(self, interface=None):
        """Get complete network information"""
        if not interface:
            interface = self.current_interface
        
        return {
            'interface': interface or 'Unknown',
            'local_ip': self.get_local_ip(interface),
            'subnet_mask': self.get_subnet_mask(interface),
            'gateway': self.get_default_gateway(),
            'dns_servers': self.get_dns_servers(),
            'mac_address': self.get_mac_address(interface)
        }
    
    def get_network_range(self, interface=None):
        """Calculate network range based on IP and subnet"""
        info = self.get_network_info(interface)
        ip = info['local_ip']
        mask = info['subnet_mask']
        
        try:
            if ip == "Unknown" or mask == "Unknown":
                return "Unknown"
            
            # Simple calculation for common subnets
            if mask == '255.255.255.0':
                base_ip = '.'.join(ip.split('.')[:-1])
                return f"{base_ip}.1-254"
            elif mask == '255.0.0.0':
                base_ip = '.'.join(ip.split('.')[:1])
                return f"{base_ip}.1.1.1-254.254.254"
            elif mask == '255.255.0.0':
                base_ip = '.'.join(ip.split('.')[:-1])
                return f"{base_ip}.1-254"
            else:
                return f"{ip}/24 (approximate)"
        except:
            return "Unknown"
    
    def copy_to_clipboard(self, text):
        """Copy text to clipboard"""
        try:
            import pyperclip
            pyperclip.copy(text)
            return True
        except ImportError:
            # Fallback using tkinter
            try:
                import tkinter as tk
                root = tk.Tk()
                root.withdraw()
                root.clipboard_clear()
                root.clipboard_append(text)
                root.update()
                root.destroy()
                return True
            except:
                return False
