import subprocess

def get_current_ssid():
    try:
        result = subprocess.check_output("iwgetid -r", shell=True)
        return result.decode('utf-8').strip()
    except subprocess.CalledProcessError:
        # Error occurred while getting SSID
        return None

def connect_to_wifi(ssid, password):
    try:
        subprocess.check_output(f"nmcli d wifi connect {ssid} password {password}", shell=True)
        print(f"Connected to {ssid}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to connect to {ssid}: {e}")

def main():
    desired_ssid = ""
    wifi_password = ""

    current_ssid = get_current_ssid()

    if current_ssid != desired_ssid:
        print(f"Current SSID is {current_ssid}. Connecting to {desired_ssid}...")
        connect_to_wifi(desired_ssid, wifi_password)
    else:
        print(f"Already connected to {desired_ssid}")

if __name__ == "__main__":
    main()
