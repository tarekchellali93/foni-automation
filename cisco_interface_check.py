from netmiko import ConnectHandler
import os 


# --- Step 2: Build the Cisco Netmiko Connection ---
cisco_device = {
    "device_type": "cisco_ios",
    "host": os.getenv("CISCO_HOST"),
    "username": os.getenv("CISCO_USERNAME"),  #  assigned username
    "password": os.getenv("CISCO_PASSWORD"),  # assigned password
}

print("Connecting to Cisco Catalyst device via Netmiko...")
net_connect = ConnectHandler(**cisco_device)

# --- Step 3: Collect Information From Multiple Commands ---
int_brief_output = net_connect.send_command("show ip interface brief")
version_output = net_connect.send_command("show version")

# Disconnect cleanly after sending commands
net_connect.disconnect()

print("\n================ SHOW IP INTERFACE BRIEF ================")
print(int_brief_output)

print("\n====================== SHOW VERSION ======================")
print(version_output)

# --- Step 4: Separate the Interface Output into Lines ---
interface_lines = int_brief_output.splitlines()

# --- Step 5, 6, & 7: Filter, Extract Fields, and Evaluate Operational Status ---
print("\n================ INTERFACE ANALYSIS REPORT ================")

for line in interface_lines:
    # Step 5: Process only lines containing Loopback interfaces
    if "Loopback" in line:
        # Step 6: Separate the line into individual fields by whitespace
        fields = line.split()

        # Extract specific data by index
        if_name = fields[0]
        ip_addr = fields[1]
        status = fields[-2]
        protocol = fields[-1]

        # Step 7: Determine operational status logic
        if status.lower() == "up" and protocol.lower() == "up":
            op_result = "OPERATIONAL"
        else:
            op_result = "CHECK REQUIRED"

        # Print the formatted result for each matching interface
        print(
            f"Interface: {if_name} | IP: {ip_addr} | Status: {status} | Protocol: {protocol} -> Result: {op_result}"
        )