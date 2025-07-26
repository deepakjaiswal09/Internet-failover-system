# core/monitor.py

import time
from utils.network_checker import check_connectivity
from utils.interface_manager import switch_interface
from utils.logger import Logger


class Monitor:
    def __init__(self, check_interval=5):
        self.check_interval = check_interval
        self.primary_interface = "Wi-Fi"
        self.backup_interface = "MobileHotspot"

    def run(self):
        Logger.log(f"Monitoring internet every {self.check_interval} seconds...")
        while True:
            if check_connectivity():
                Logger.log("Internet is working fine.")
            else:
                Logger.log("Internet is down! Initiating failover...")
                success = switch_interface(self.backup_interface)
                if success:
                    Logger.log(f"Switched to backup interface: {self.backup_interface}")
                else:
                    Logger.log("Failed to switch interface. Manual intervention required.")
            time.sleep(self.check_interval)
