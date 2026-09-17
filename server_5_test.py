from netmiko import ConnectHandler

# Server 1 configuration
server_5 = {
    'device_type': 'linux',
    'host': '3.137.140.116',
    'username': 'tchellali',  
    'password': 'password101!', 
}

# Connect and execute command
net_connect = ConnectHandler(**server_5)
output = net_connect.send_command('ip -br addr')
print(output)
net_connect.disconnect()