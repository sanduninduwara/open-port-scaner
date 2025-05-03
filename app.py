import streamlit as st
import subprocess
import tempfile
import os
from datetime import datetime
from gemini_analyzer import analyze_with_gemini, generate_mock_vulnerabilities

def analyze_results(results_text):
    """Analyze the scan results and provide conclusions"""
    # First try to get analysis from Gemini
    try:
        gemini_analysis = analyze_with_gemini(results_text)
        if "Error" not in gemini_analysis:
            return gemini_analysis
    except Exception as e:
        st.warning(f"Gemini analysis failed: {str(e)}")
    
    # Fallback to mock vulnerabilities if Gemini fails
    # return generate_mock_vulnerabilities(results_text)
    return gemini_analysis

def run_port_scanner(ip_address, deep_scan=False):
    """Run the port scanner and return results"""
    try:
        temp_path = f"./logs/scan_results_{ip_address.replace('.', '_')}.txt"
        
        # Run the port scanner
        process = subprocess.Popen(
            ['python', 'ip_vulnerability_scanner.py'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Send the IP address and deep scan option
        input_data = f"{ip_address}\n{'y' if deep_scan else 'n'}\n"
        stdout, stderr = process.communicate(input=input_data)
        
        if stderr:
            return f"Error: {stderr}"
        
        # Read the results file
        with open(temp_path, 'r') as f:
            results = f.read()
        
        return results
    except Exception as e:
        return f"Error running scanner: {str(e)}"

# Streamlit UI
st.title("IP Port Scanner & Analyzer")
st.write("Enter an IP address to scan for open ports and vulnerabilities")

# Input
ip_address = st.text_input("Enter IP Address:", "145.223.99.15")

# Deep scan checkbox
deep_scan = st.checkbox("Deep Scan (More thorough but slower)")

# Scan button
if st.button("Scan IP"):
    if ip_address:
        with st.spinner("Scanning IP address..."):
            # Run the scanner
            results = run_port_scanner(ip_address, deep_scan)
            
            # Display results
            st.subheader("Scan Results")
            st.text_area("Raw Results", results, height=300)
            
            # Analyze results
            st.subheader("Vulnerability Analysis")
            conclusions = analyze_results(results)
            st.text_area("Analysis", conclusions, height=400)
    else:
        st.error("Please enter an IP address")

# Add some information about the scanner
st.sidebar.title("About")
st.sidebar.info("""
This tool scans IP addresses for:
- Open ports
- Common vulnerabilities
- SSL/TLS issues
- Service information
""")

# Analysis Categories
st.sidebar.title("Analysis Categories")
st.sidebar.markdown("""
### 🔍 IP Address Analysis
- **General Information**
  - Location details
  - Network information
  - Host details

- **DNS Information**
  - Domain records
  - DNS configuration
  - Name server details

- **Network Path**
  - Traceroute data
  - Network hops
  - Routing information

### 🛡️ Security Analysis
- **Port Security**
  - Open ports assessment
  - Service vulnerabilities
  - Port configuration issues

- **IP Security**
  - IP reputation
  - Known vulnerabilities
  - Security history

### 💡 Security Recommendations
- **Network Security**
  - Firewall configurations
  - Network segmentation
  - Access control improvements

- **System Security**
  - OS hardening
  - Patch management
  - System configuration

- **Server Security**
  - Service hardening
  - Server configuration
  - Access controls

- **Application Security**
  - Web application security
  - Service security
  - Application hardening
""")

# Add a separator
st.sidebar.markdown("---")

# Add a note about the analysis
st.sidebar.info("""
**Note:** The analysis provides comprehensive security insights and actionable recommendations to improve your system's security posture.
""")

# st.sidebar.title("Legend")
# st.sidebar.markdown("""
# -about ports security vulnerabilities
# -about ip address security vulnerabilities
# -about the ip address general information
# -about the ip address dns information
# -about the ip address traceroute information

# -suggestions to improve the security for ports and ip address
# -suggestions to improve the security for the whole network
# -suggestions to improve the security for the whole system
# -suggestions to improve the security for the whole server
# -suggestions to improve the security for the whole application
# """) 