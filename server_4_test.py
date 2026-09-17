from netmiko import ConnectHandler

# Server 1 configuration
server_4 = {
    'device_type': 'linux',
    'host': '18.189.30.63',
    'username': 'tchellali',  
    'password': 'password101!', 
}

# Connect and execute command
net_connect = ConnectHandler(**server_4)
output = net_connect.send_command('ip -br addr')
print(output)
net_connect.disconnect()