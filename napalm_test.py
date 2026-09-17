from napalm import get_network_driver
from pprint import pprint
import os

driver = get_network_driver("ios")

device = driver(
    hostname=os.getenv("CISCO_HOST"),
    username="tchellali",
    password="password101!",
    optional_args={"secret":"password707!"}
)
print(device)
device.open()
pprint(device.get_interfaces())
pprint(device.get_facts())
device.close()
