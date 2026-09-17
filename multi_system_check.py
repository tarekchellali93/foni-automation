from netmiko import ConnectHandler
import os

#cisco catalyst 8000v 54.90.112.247
#linux server: 3.145.195.223

devices = [
    {
        "device_type":"cisco_ios",
        "host":os.getenv("CISCO_HOST"),
        "username":os.getenv("CISCO_USERNAME"),
        "password":os.getenv("CISCO_PASSWORD")
    },
    {
        "device_type":"linux",
        "host":os.getenv("LINUX_HOST"),
        "username":os.getenv("LINUX_USERNAME"),
        "password":os.getenv("LINUX_PASSWORD")

    }
]

cisco_commands = [
        'sh ip version',
        'show ip interface brief'
    ]



for device in devices :
    connection = ConnectHandler(**device)
    output = connection.send_command('ip --br addr')
    print(output)
    connection.disconnect()