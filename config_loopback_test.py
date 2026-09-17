import os
from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoAuthenticationException, NetmikoTimeoutException

def connect_to_system(system):
    user_key = system.get("username_env", "CISCO_USERNAME")
    pass_key = system.get("password_env", "CISCO_PASSWORD")
    
    connection_info = {
        "device_type": system["device_type"],
        "host": system["host"],
        "username": os.getenv(user_key),
        "password": os.getenv(pass_key),
        "global_delay_factor": 2,  # Increases wait times for SSH responses
    }

    return ConnectHandler(**connection_info)

def create_cisco_loopback(connection):
    commands = [
        "interface Loopback111",
        "description FONI Training Loopback",
        "ip address 192.0.2.111 255.255.255.255",
    ]
    return connection.send_config_set(commands)

def read_cisco_loopback(connection):
    return connection.send_command("do show running-config interface Loopback111")

def remove_cisco_loopback(connection):
    return connection.send_config_set(["no interface Loopback111"])

def create_linux_interface(connection, interface_name="dummy0", ip_cidr="10.0.0.1/32"):
    password = connection.password
    commands = [
        f"echo '{password}' | sudo -S ip link add {interface_name} type dummy",
        f"echo '{password}' | sudo -S ip addr add {ip_cidr} dev {interface_name}",
        f"echo '{password}' | sudo -S ip link set {interface_name} up",
        f"ip addr show {interface_name}"
    ]
    
    output = ""
    for cmd in commands:
        display_cmd = cmd.replace(f"echo '{password}' | ", "")
        output += f"$ {display_cmd}\n"
        # Match any terminal prompt ending in $ or #
        output += connection.send_command(cmd, expect_string=r"[\$#]") + "\n\n"
        
    return output

if __name__ == "__main__":
    from inventory import get_device
    system = get_device("FONI-Router-01")
    system["device_type"] = system["type"]
    
    connection = None
    try:
        connection = connect_to_system(system)
        
        print("CREATE")
        print(create_cisco_loopback(connection))

        print("READ AFTER CREATE")
        print(read_cisco_loopback(connection))

        print("REMOVE")
        print(remove_cisco_loopback(connection))

        print("READ AFTER REMOVE")
        print(read_cisco_loopback(connection))

    except NetmikoAuthenticationException:
        print(f"{system['name']} -> FAILED: AUTHENTICATION")
    except NetmikoTimeoutException:
        print(f"{system['name']} -> FAILED: CONNECTION TIMEOUT")
    finally:
        if connection:
            connection.disconnect()