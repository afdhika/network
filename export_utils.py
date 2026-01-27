import csv
import json
import os
from datetime import datetime
from tkinter import messagebox, filedialog

class ExportManager:
    def __init__(self):
        self.scan_results = []
    
    def add_result(self, host, ping_time, ports_status, status):
        """Add scan result to memory"""
        self.scan_results.append({
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'host': host,
            'ping_time_ms': ping_time,
            'status': status,
            'open_ports': [port for port, is_open in ports_status.items() if is_open],
            'total_ports_checked': len(ports_status),
            'open_ports_count': len([port for port, is_open in ports_status.items() if is_open])
        })
    
    def clear_results(self):
        """Clear all stored results"""
        self.scan_results = []
    
    def export_csv(self, parent_window=None):
        """Export results to CSV file"""
        if not self.scan_results:
            messagebox.showwarning("No Data", "No scan results to export!")
            return False
        
        filename = filedialog.asksaveasfilename(
            parent=parent_window,
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialfile=f"network_scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        )
        
        if not filename:
            return False
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = [
                    'timestamp', 'host', 'status', 'ping_time_ms', 
                    'open_ports_count', 'total_ports_checked', 'open_ports'
                ]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                for result in self.scan_results:
                    writer.writerow({
                        'timestamp': result['timestamp'],
                        'host': result['host'],
                        'status': result['status'],
                        'ping_time_ms': result['ping_time_ms'],
                        'open_ports_count': result['open_ports_count'],
                        'total_ports_checked': result['total_ports_checked'],
                        'open_ports': ', '.join(map(str, result['open_ports']))
                    })
            
            return True
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export CSV: {str(e)}")
            return False
    
    def export_json(self, parent_window=None):
        """Export results to JSON file"""
        if not self.scan_results:
            messagebox.showwarning("No Data", "No scan results to export!")
            return False
        
        filename = filedialog.asksaveasfilename(
            parent=parent_window,
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            initialfile=f"network_scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        
        if not filename:
            return False
        
        try:
            export_data = {
                'scan_info': {
                    'exported_at': datetime.now().isoformat(),
                    'total_hosts': len(self.scan_results),
                    'active_hosts': len([r for r in self.scan_results if r['status'] == 'ACTIVE']),
                    'inactive_hosts': len([r for r in self.scan_results if r['status'] == 'INACTIVE'])
                },
                'results': self.scan_results
            }
            
            with open(filename, 'w', encoding='utf-8') as jsonfile:
                json.dump(export_data, jsonfile, indent=2, ensure_ascii=False)
            
            return True
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export JSON: {str(e)}")
            return False
    
    def get_summary_stats(self):
        """Get summary statistics of current results"""
        if not self.scan_results:
            return {}
        
        active_hosts = [r for r in self.scan_results if r['status'] == 'ACTIVE']
        inactive_hosts = [r for r in self.scan_results if r['status'] == 'INACTIVE']
        
        return {
            'total_hosts': len(self.scan_results),
            'active_hosts': len(active_hosts),
            'inactive_hosts': len(inactive_hosts),
            'success_rate': f"{(len(active_hosts) / len(self.scan_results) * 100):.1f}%",
            'total_open_ports': sum(r['open_ports_count'] for r in self.scan_results),
            'avg_ping_time': f"{sum(r['ping_time_ms'] or 0 for r in self.scan_results) / len(self.scan_results):.1f}ms"
        }
