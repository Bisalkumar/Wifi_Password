import subprocess
import platform

def get_wifi_profiles():
    """Retrieve WiFi profiles from the system."""
    try:
        output = subprocess.check_output(["netsh", "wlan", "show", "profiles"]).decode("utf-8")
    except UnicodeDecodeError:
        output = subprocess.check_output(["netsh", "wlan", "show", "profiles"]).decode("ISO-8859-1")
    profiles_data = [i.split(":")[1][1:-1] for i in output.split("\n") if "All User Profile" in i]
    return profiles_data


def get_wifi_password(profile_name):
    """Retrieve password for a given WiFi profile."""
    try:
        password_data = subprocess.check_output(
            ["netsh", "wlan", "show", "profile", profile_name, "key=clear"]
        ).decode("utf-8").split("\n")
        
        password_lines = [line.split(":")[1][1:-1] for line in password_data if "Key Content" in line]
        return password_lines[0] if password_lines else None
    except subprocess.CalledProcessError:
        return None

def main():
    # Ensure the script runs on Windows only
    if platform.system() != "Windows":
        print("This script is designed to run on Windows only.")
        return
    
    wifi_profiles = get_wifi_profiles()

    for profile in wifi_profiles:
        password = get_wifi_password(profile)
        if password:
            print(f"{profile:<30} | {password}")
        else:
            print(f"{profile:<30} | No password found")

if __name__ == "__main__":
    main()
