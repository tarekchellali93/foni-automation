from netmiko import ConnectHandler

# Server 1 configuration
server_1 = {
    'device_type': 'linux',
    'host': '18.222.205.168',
    'username': 'tchellali',  
    'password': 'password101!', 
}

# Connect and execute command
net_connect = ConnectHandler(**server_1)
output = net_connect.send_command('ip -br addr')
print(output)
net_connect.disconnect()