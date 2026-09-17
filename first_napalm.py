# Import os so we can read the environment variables from PowerShell.
import os

# Import the NAPALM function used to choose a network-device driver.
from napalm import get_network_driver


# Select the NAPALM driver for Cisco IOS / IOS-XE devices.
driver = get_network_driver("ios")

# Create the device object.
# The credentials are read from environment variables, not written in this file.
device = driver(
    hostname=os.getenv("CISCO_HOST"),
    username=os.getenv("CISCO_USERNAME"),
    password=os.getenv("CISCO_PASSWORD"),

    # Cisco devices may need the enable secret for privileged EXEC access.
    optional_args={"secret": os.getenv("CISCO_SECRET")},
)

# Keep track of whether the connection opened successfully.
connected = False

try:
    # Open the SSH connection to the Cisco device.
    device.open()
    connected = True
    print("Connected to the Cisco device.")

    # Get interface information as a Python dictionary.
    interfaces = device.get_interfaces()
    print("\n--- Interface information ---")
    print(interfaces)

    # Get general device information as a Python dictionary.
    facts = device.get_facts()
    print("\n--- Device facts ---")
    print(facts)

    # Print only one value from the facts dictionary.
    print("\n--- Device hostname ---")
    print(facts["hostname"])

finally:
    # Always close the connection after collecting the information.
    if connected:
        device.close()
        print("\nConnection closed.")
        