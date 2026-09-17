from netmiko import ConnectHandler

device = {
    "device_type": "linux",
    "host": "3.145.195.223",
    "username": "tchellali",
    "password": "password101!"
}

connection = ConnectHandler(**device)

output = connection.send_command("ip -br addr")
print(output)

connection.disconnect()