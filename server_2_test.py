from netmiko import ConnectHandler
from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoTimeoutException, NetmikoAuthenticationException
# Server 2 configuration
server_2 = {
    'device_type': 'linux',
    'host': '3.15.204.243',
    'username': 'tchellali',  
    'password': 'password101!', 
    "conn_timeout": 5
}

# Connect and execute command
net_connect = ConnectHandler(**server_2)
output = net_connect.send_command('ip -br addr')
print(output)
net_connect.disconnect()