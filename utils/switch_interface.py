# core/switcher.py

import time
from utils.logger import Logger
from utils.wifi_manager import WiFiManager

class Switcher:
    def __init__(self, primary_network, backup_networks):
        """
        :param primary_network: Name of the preferred Wi-Fi SSID
        :param backup_networks: List of fallback network SSIDs
        """
        self.primary = primary_network
        self.backups = backup_networks

    def connect_primary(self):
        Logger.log(f"Attempting to connect to primary network: {self.primary}")
        return WiFiManager.connect_to_network(self.primary)

    def connect_backup(self):
        Logger.log("Attempting to connect to backup networks...")
        for ssid in self.backups:
            if WiFiManager.connect_to_network(ssid):
                Logger.log(f"Connected to backup network: {ssid}")
                return True
        Logger.log("Failed to connect to any backup networks.")
        return False

    def disconnect_current(self):
        Logger.log("Disconnecting current Wi-Fi connection...")
        return WiFiManager.disconnect()

    def manual_switch(self, target_ssid):
        Logger.log(f"Manually switching to network: {target_ssid}")
        self.disconnect_current()
        time.sleep(2)  # small delay before reconnect
        return WiFiManager.connect_to_network(target_ssid)

    def auto_switch(self):
        Logger.log("Starting automatic network switch logic...")
        self.disconnect_current()
        time.sleep(2)
        if self.connect_primary():
            Logger.log("Switched to primary network successfully.")
            return
        if self.connect_backup():
            Logger.log("Switched to a backup network successfully.")
            return
        Logger.log("All network switch attempts failed.")
