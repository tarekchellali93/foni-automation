from netmiko import ConnectHandler

# Server 1 configuration
server_3 = {
    'device_type': 'linux',
    'host': '3.140.243.241',
    'username': 'tchellali',  
    'password': 'password101!', 
}

# Connect and execute command
net_connect = ConnectHandler(**server_3)
output = net_connect.send_command('ip -br addr')
print(output)
net_connect.disconnect()