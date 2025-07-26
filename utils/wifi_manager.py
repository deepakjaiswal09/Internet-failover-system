# utils/wifi_manager.py

import subprocess
import re
from utils.logger import Logger

class WiFiManager:
    @staticmethod
    def list_available_networks(interface="Wi-Fi"):
        """
        Returns a list of available Wi-Fi SSIDs.
        """
        try:
            result = subprocess.check_output(f'netsh wlan show networks interface="{interface}"', shell=True, text=True)
            ssids = re.findall(r'SSID \d+ : (.+)', result)
            Logger.log(f"Available Networks: {ssids}")
            return ssids
        except Exception as e:
            Logger.log(f"Error listing networks: {e}")
            return []

    @staticmethod
    def connect_to_network(ssid, profile_name=None):
        """
        Connects to a Wi-Fi network using a saved profile.
        """
        try:
            profile = profile_name if profile_name else ssid
            command = f'netsh wlan connect name="{profile}" ssid="{ssid}"'
            subprocess.check_call(command, shell=True)
            Logger.log(f"Connected to network: {ssid}")
            return True
        except Exception as e:
            Logger.log(f"Error connecting to {ssid}: {e}")
            return False

    @staticmethod
    def disconnect():
        """
        Disconnects the current Wi-Fi connection.
        """
        try:
            subprocess.check_call("netsh wlan disconnect", shell=True)
            Logger.log("Disconnected from Wi-Fi")
            return True
        except Exception as e:
            Logger.log(f"Error disconnecting from Wi-Fi: {e}")
            return False
