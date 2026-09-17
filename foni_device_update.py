device_name = "C8000V"

devices = ["FONI-Router-1", "FONI-Switch-1","FONI-Router-2"]
print(f"New monitoring target: {devices[2]}")

device_info = {
    "name": "FONI-Router-1",
    "type": "Cisco Router",
    "location": "Operations Center",
    "status": "Down"
}

print(f"Primary device: {device_name}")

print("\nDevices scheduled for monitoring:")
for device in devices:
    print(device)

print(f"\nDevice location: {device_info['location']}")

if device_info["status"] == "UP":
    print("Device is available for automation.")
else:
    print("Device requires operator attention.")