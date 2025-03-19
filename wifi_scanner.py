import subprocess

def scan_wifi():
    # Run the command to scan for WiFi networks
    result = subprocess.run(['nmcli', '-t', '-f', 'SSID', 'dev', 'wifi'], stdout=subprocess.PIPE)

    # Decode the output from bytes to string
    wifi_networks = result.stdout.decode('utf-8').split('\n')

    # Filter out empty SSIDs
    wifi_networks = [ssid for ssid in wifi_networks if ssid]

    return wifi_networks

def connect_to_wifi(ssid, password):
    # Run the command to connect to the WiFi network
    connect_command = ['nmcli', 'dev', 'wifi', 'connect', ssid, 'password', password]
    result = subprocess.run(connect_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Check if the connection was successful
    if result.returncode == 0:
        return True
    else:
        print(f"Failed to connect to {ssid}. Error: {result.stderr.decode('utf-8')}")
        return False

def save_password(ssid, password):
    # Save the SSID and password to a file
    with open('wifi_passwords.txt', 'a') as file:
        file.write(f"SSID: {ssid}, Password: {password}\n")

if __name__ == "__main__":
    networks = scan_wifi()
    if networks:
        print("Available WiFi Networks:")
        for index, ssid in enumerate(networks):
            print(f"{index + 1}. {ssid}")

        try:
            choice = int(input("Select a network to connect to (by number): ")) - 1
            if 0 <= choice < len(networks):
                selected_ssid = networks[choice]
                wifi_password = input(f"Enter password for {selected_ssid}: ")

                if connect_to_wifi(selected_ssid, wifi_password):
                    print(f"Successfully connected to {selected_ssid}.")
                    save_password(selected_ssid, wifi_password)
                else:
                    print("Failed to connect to the network. Please try again.")
            else:
                print("Invalid selection. Please run the script again.")
        except ValueError:
            print("Invalid input. Please enter a number.")
    else:
        print("No WiFi networks found.")