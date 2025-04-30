import socket
import requests
import json
from datetime import datetime
import concurrent.futures
import time

def get_ip_info(ip):
    """Get detailed information about an IP address using ip-api.com"""
    try:
        response = requests.get(f'http://ip-api.com/json/{ip}')
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def scan_port(ip, port):
    """Scan a specific port on the given IP address"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((ip, port))
        sock.close()
        return port if result == 0 else None
    except:
        return None

def scan_ports(ip, start_port=1, end_port=1024):
    """Scan a range of ports on the given IP address"""
    open_ports = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        future_to_port = {executor.submit(scan_port, ip, port): port 
                         for port in range(start_port, end_port + 1)}
        
        for future in concurrent.futures.as_completed(future_to_port):
            port = future.result()
            if port:
                open_ports.append(port)
    
    return sorted(open_ports)

def main():
    # Get IP address from user
    ip = input("Enter the public IP address to scan: ")
    
    print(f"\nScanning IP: {ip}")
    print("This may take a few minutes...\n")
    
    # Get IP information
    ip_info = get_ip_info(ip)
    
    # Scan ports
    start_time = time.time()
    open_ports = scan_ports(ip)
    scan_time = time.time() - start_time
    
    # Prepare results
    results = {
        "scan_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "target_ip": ip,
        "ip_info": ip_info,
        "open_ports": open_ports,
        "scan_duration": f"{scan_time:.2f} seconds"
    }
    
    # Save results to file
    filename = f"./logs/scan_results_{ip.replace('.', '_')}.txt"
    with open(filename, 'w') as f:
        f.write("IP Port Scanner Results\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Scan Date: {results['scan_date']}\n")
        f.write(f"Target IP: {results['target_ip']}\n")
        f.write(f"Scan Duration: {results['scan_duration']}\n\n")
        
        f.write("IP Information:\n")
        f.write("-" * 20 + "\n")
        for key, value in results['ip_info'].items():
            f.write(f"{key}: {value}\n")
        
        f.write("\nOpen Ports:\n")
        f.write("-" * 20 + "\n")
        if open_ports:
            for port in open_ports:
                f.write(f"Port {port} is open\n")
        else:
            f.write("No open ports found in the scanned range\n")
    
    print(f"\nScan completed in {scan_time:.2f} seconds")
    print(f"Results have been saved to {filename}")

if __name__ == "__main__":
    main() 