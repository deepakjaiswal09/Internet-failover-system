# core/monitor.py

import time
from utils.network_checker import check_connectivity
from utils.interface_manager import InterfaceManager
from utils.logger import Logger
from utils.switch_interface import Switcher


class Monitor:
    def __init__(self, check_interval=5):
        self.check_interval = check_interval
        self.primary_network = "Wi-Fi"
        self.backup_networks = ["MobileHotspot"]
        self.switcher = Switcher(self.primary_network, self.backup_networks)

    def run(self):
        Logger.log(f"Monitoring internet every {self.check_interval} seconds...")
        while True:
            if check_connectivity():
                Logger.log("Internet is working fine.")
            else:
                Logger.log("Internet is down! Initiating failover...")
                success = self.switcher.manual_switch(self.backup_networks[0])
                if success:
                    Logger.log(f"Switched to backup network: {self.backup_networks[0]}")
                else:
                    Logger.log("Failed to switch network. Manual intervention required.")
            time.sleep(self.check_interval)
