devices = [
    {
        "name": "FONI-Router-01",
        "host": "54.90.112.247",
        "type": "cisco_ios",
        "role": "router",
        "username_env": "CISCO_USERNAME",
        "password_env": "CISCO_PASSWORD"
    },
    {
        "name": "FONI-Radar-01",
        "host": "3.145.195.223",
        "type": "linux",
        "role": "radar-processing",
        "username_env": "LINUX_USERNAME",
        "password_env": "LINUX_PASSWORD"
    },
    {
        "name": "FONI-Radar-02",
        "host": "18.222.205.168",
        "type": "linux",
        "role": "radar-processing",
        "username_env": "LINUX_USERNAME",
        "password_env": "LINUX_PASSWORD"
    },
    {
        "name": "FONI-Monitor-01",
        "host": "3.15.204.243",
        "type": "linux",
        "role": "monitoring",
        "username_env": "LINUX_USERNAME",
        "password_env": "LINUX_PASSWORD"
    },
    {
        "name": "FONI-Monitor-02",
        "host": "3.140.243.241",
        "type": "linux",
        "role": "monitoring",
        "username_env": "LINUX_USERNAME",
        "password_env": "LINUX_PASSWORD"
    },
    {
        "name": "FONI-Ingest-01",
        "host": "18.189.30.63",
        "type": "linux",
        "role": "data-ingest",
        "username_env": "LINUX_USERNAME",
        "password_env": "LINUX_PASSWORD"
    },
    {
        "name": "FONI-Ingest-02",
        "host": "3.137.140.116",
        "type": "linux",
        "role": "data-ingest",
        "username_env": "LINUX_USERNAME",
        "password_env": "LINUX_PASSWORD"
    },
    {
        "name": "FONI-Application-02",
        "host": "3.14.67.101",
        "type": "linux",
        "role": "application",
        "username_env": "LINUX_USERNAME",
        "password_env": "LINUX_PASSWORD"
    },
    {
        "name": "FONI-Application-01",
        "host": "18.117.248.183",
        "type": "linux",
        "role": "application",
        "username_env": "LINUX_USERNAME",
        "password_env": "LINUX_PASSWORD"
    }
]
def get_device(device_name):
    for device in devices:
        if device["name"] == device_name:
            return device

    return None

