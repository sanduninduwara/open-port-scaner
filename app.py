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

def run_port_scanner(ip_address):
    """Run the port scanner and return results"""
    try:
        # Create a temporary file for the results
        # with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
        temp_path = f"./logs/scan_results_{ip_address.replace('.', '_')}.txt"
        
        # Run the port scanner
        process = subprocess.Popen(
            ['python', 'ip_port_scanner.py'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Send the IP address and get the output
        stdout, stderr = process.communicate(input=ip_address + '\n')
        
        if stderr:
            return f"Error: {stderr}"
        
        # Read the results file
        with open(temp_path, 'r') as f:
            results = f.read()
        
        # Clean up
        # os.unlink(temp_path)
        
        return results
    except Exception as e:
        return f"Error running scanner: {str(e)}"

# Streamlit UI
st.title("IP Port Scanner & Analyzer")
st.write("Enter an IP address to scan for open ports and vulnerabilities")

# Input
ip_address = st.text_input("Enter IP Address:", "145.223.99.15")

# Scan button
if st.button("Scan IP"):
    if ip_address:
        with st.spinner("Scanning IP address..."):
            # Run the scanner
            results = run_port_scanner(ip_address)
            
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

st.sidebar.title("Legend")
st.sidebar.markdown("""
🔴 Critical - Immediate attention required
🟡 Warning - Potential security concern
🔵 Info - General information
🟢 Good - No issues detected
""") 