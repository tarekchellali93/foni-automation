import os
from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoTimeoutException, NetmikoAuthenticationException

# -----------------------------------------------------------------------------
# NINE-SYSTEM INVENTORY
# -----------------------------------------------------------------------------
systems = [
    {"name": "FONII-Router-01", "device_type": "cisco_xe", "host": "54.90.112.247"},
    {"name": "FONII-Radar-01", "device_type": "linux", "host": "3.145.195.223"},
    {"name": "FONII-Radar-02", "device_type": "linux", "host": "18.222.205.160"},
    {"name": "FONII-Monitor-01", "device_type": "linux", "host": "3.15.204.243"},
    {"name": "FONII-Monitor-02", "device_type": "linux", "host": "3.140.243.241"},
    {"name": "FONII-Ingest-01", "device_type": "linux", "host": "18.189.20.63"},
    {"name": "FONII-Ingest-02", "device_type": "linux", "host": "3.137.140.116"},
    {"name": "FONII-Application-02", "device_type": "linux", "host": "3.14.67.101"},
    {"name": "FONII-Application-01", "device_type": "linux", "host": "18.117.248.183"}
]

# -----------------------------------------------------------------------------
# CONNECTION HELPER
# Dynamically pulls credentials from environment variables to keep code secure.
# -----------------------------------------------------------------------------
def connect_to_system(system):
    """Establishes an SSH connection to a device using Netmiko."""
    device_type = system["device_type"]
    host = system["host"]
    
    if device_type == "cisco_xe":
        username = os.getenv("CISCO_USERNAME") 
        password = os.getenv("CISCO_PASSWORD") 
        secret = os.getenv("CISCO_SECRET", password)
    else:
        username = os.getenv("LINUX_USERNAME") 
        password = os.getenv("LINUX_PASSWORD") 
        secret = ""

    device = {
        "device_type": device_type,
        "host": host,
        "username": username,
        "password": password,
        "secret": secret
    }
    return ConnectHandler(**device)

# -----------------------------------------------------------------------------
# PLATFORM POLLING FUNCTIONS
# Opens a connection, gets the raw interface output, disconnects, and returns raw text.
# -----------------------------------------------------------------------------
def poll_cisco(device):
    """Polls a Cisco device using 'show ip interface brief'."""
    connection = connect_to_system(device)
    output = connection.send_command("show ip interface brief")
    connection.disconnect()
    return output

def poll_linux(device):
    """Polls a Linux device using 'ip -br addr'."""
    connection = connect_to_system(device)
    output = connection.send_command("ip -br addr")
    connection.disconnect()
    return output

# -----------------------------------------------------------------------------
# PARSING FUNCTIONS FOR EXACT OUTPUT FORMAT
# Parses the raw text into: Interface Name: Interface Status
# -----------------------------------------------------------------------------
def parse_cisco_interfaces(raw_output):
    """Parses Cisco 'show ip interface brief' into Interface Name: Interface Status."""
    formatted_lines = []
    lines = raw_output.strip().splitlines()
    
    for line in lines:
        if line.startswith("Interface") or "OK?" in line:
            continue  # Skip header line
            
        parts = line.split()
        if len(parts) >= 6:
            intf_name = parts[0]
            status = parts[4]      # e.g., 'up' or 'administratively down'
            protocol = parts[5]    # e.g., 'up' or 'down'
            intf_status = f"{status}/{protocol}"
            
            formatted_lines.append(f"{intf_name}: {intf_status}")
            
    return "\n".join(formatted_lines) if formatted_lines else "No interfaces found"

def parse_linux_interfaces(raw_output):
    """Parses Linux 'ip -br addr' into Interface Name: Interface Status."""
    formatted_lines = []
    lines = raw_output.strip().splitlines()
    
    for line in lines:
        parts = line.split()
        if len(parts) >= 2:
            intf_name = parts[0]
            intf_status = parts[1]  # e.g., 'UP', 'DOWN', or 'UNKNOWN'
            
            formatted_lines.append(f"{intf_name}: {intf_status}")
            
    return "\n".join(formatted_lines) if formatted_lines else "No interfaces found"

# -----------------------------------------------------------------------------
# DIRECT EXECUTION LOOP ACROSS ALL 9 DEVICES (NO MAIN FUNCTION)
# -----------------------------------------------------------------------------
for system in systems:
    device_name = system["name"]
    host_ip = system["host"]
    device_type = system["device_type"]
    
    # OUTPUT FORMAT REQUIREMENT #1: Device Name (Host IP)
    print(f"\n{device_name} ({host_ip})")
    
    try:
        # Determine platform and execute polling
        if device_type == "cisco_xe":
            raw_output = poll_cisco(system)
            parsed_output = parse_cisco_interfaces(raw_output)
        else:
            raw_output = poll_linux(system)
            parsed_output = parse_linux_interfaces(raw_output)
            
        # OUTPUT FORMAT REQUIREMENT #2: Interface Name: Interface Status
        print(parsed_output)

    # ERROR HANDLING: Catches exceptions without stopping the loop
    except NetmikoTimeoutException:
        print("Error: Connection timeout. Host unreachable.")
    except NetmikoAuthenticationException:
        print("Error: Authentication failed.")
    except Exception as e:
        print(f"Error: {str(e)}")