# Import the os module for interacting with environment variables and the operating system
import os

# Import core Flask components:
# - Flask: to create the web application instance
# - render_template: to render HTML template files with dynamic Jinja2 data
# - request: to access incoming HTTP request data (e.g., POST form submissions)
from flask import Flask, render_template, request

# Import inventory data and lookup helpers from inventory.py:
# - devices: the list containing dictionary details for all 9 network/host systems
# - get_device: helper function to look up a single device dictionary by its name
from inventory import devices, get_device

# Import custom network automation functions from config_loopback_test.py:
# - connect_to_system: establishes Netmiko SSH connections using environment credentials
# - create_cisco_loopback: sends IOS commands to build/verify a Loopback interface
from config_loopback_test import (
    connect_to_system,
    create_cisco_loopback
)

# Initialize the main Flask application instance
app = Flask(__name__)

# Define a validation function to verify incoming form inputs before running network tasks
def validate_request(device_name, action):
    # Define a list of actions that our application safely permits
    allowed_actions = ["read", "create", "remove"]
    
    # Query the inventory to see if the submitted device name exists
    device = get_device(device_name)

    # Check if the device lookup returned None (meaning the system is not in inventory)
    if device is None:
        # Return None for the device object and an error message explaining the failure
        return None, "The selected device is not in the FONI inventory."

    # Check if the requested action is missing from our allowed actions list
    if action not in allowed_actions:
        # Return None for the device object and an error message detailing the unsupported action
        return None, "The selected action is not supported."

    # If both checks pass, return the valid device dictionary and None for the error
    return device, None

# Define the route for the device selection page, supporting both GET and POST HTTP methods
@app.route("/device", methods=["GET", "POST"])
def device_form():
    # Check if the browser submitted data using an HTTP POST request
    if request.method == "POST":
        # Extract the selected device name string from the HTML form dropdown
        device_name = request.form.get("device")
        # Extract the selected action string from the HTML form dropdown
        action = request.form.get("action")

        # Run our validation function on the submitted inputs
        device, error = validate_request(device_name, action)

        # If an error string was returned by validation, handle the rejection
        if error:
            # Print the rejection message to the terminal console without connecting to devices
            print(f"Request rejected: {error}")
        else:
            # Print confirmation to the terminal showing a valid request passed validation
            print(f"Valid request for {device['name']}: {action}")

    # For both GET requests and completed POST submissions, render the device_form.html page
    # Pass the full devices list so Jinja2 can dynamically generate the dropdown options
    return render_template(
        "device_form.html",
        devices=devices
    )

# Helper function to iterate over all inventory devices and gather connection/interface statuses
def gather_all_device_results():
    # Initialize an empty list to collect individual device execution results
    results = []

    # Loop through each device dictionary inside the main devices list
    for dev in devices:
        # Construct the connection parameters map required by Netmiko
        data = {
            "name": dev["name"],
            "device_type": dev["type"],
            "host": dev["host"],
            "username_env": dev["username_env"],
            "password_env": dev["password_env"]
        }

        # Use a try block to gracefully handle network timeouts or credential errors
        try:
            # Establish the Netmiko SSH connection to the targeted device
            connection = connect_to_system(data)

            # Check if the device is running Cisco IOS
            if dev["type"] == "cisco_ios":
                # Execute the Cisco loopback creation function and store terminal output
                interface_output = create_cisco_loopback(connection)
                # Define the target interface label for the results table
                target_iface = "Loopback111"
            else:
                # Skip interface creation for non-Cisco Linux hosts
                interface_output = "Linux interface creation skipped."
                # Assign N/A for Linux target interface label
                target_iface = "N/A"

            # Append successful execution results into our results array
            results.append({
                "name": dev["name"],
                "interface": target_iface,
                "stage": "after create",
                "output": interface_output
            })

            # Terminate the SSH session cleanly
            connection.disconnect()

        # Catch connection failures or syntax exceptions
        except Exception as e:
            # Append error details into the results array so the UI displays failure context
            results.append({
                "name": dev["name"],
                "interface": "Error",
                "stage": "connection failed",
                "output": f"Failed to connect or execute command: {str(e)}"
            })

    # Return the aggregated list of results for display on the webpage
    return results

# Define the route for displaying the multi-device interface summary table
@app.route("/interfaces")
def interfaces():
    # Gather execution results across all inventory devices
    all_systems = gather_all_device_results()
    # Render interfaces.html template, passing all system output data into Jinja2
    return render_template("interfaces.html", systems=all_systems)

# Check if this script is executed directly from the command line
if __name__ == "__main__":
    # Start the Flask built-in development web server with debug mode enabled
    app.run(debug=True)