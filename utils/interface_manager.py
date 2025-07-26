# core/interface_manager.py

import subprocess
from utils.logger import Logger

class InterfaceManager:
    def __init__(self):
        self.interfaces = self.get_all_interfaces()

    def get_all_interfaces(self):
        try:
            result = subprocess.check_output("netsh interface show interface", shell=True, text=True)
            lines = result.strip().split("\n")[3:]  # Skip headers
            interfaces = []
            for line in lines:
                parts = line.strip().split()
                if len(parts) >= 4:
                    status, admin_state, state, name = parts[0], parts[1], parts[2], " ".join(parts[3:])
                    interfaces.append({
                        "name": name,
                        "status": status,
                        "admin_state": admin_state,
                        "state": state
                    })
            Logger.log(f"Detected interfaces: {[iface['name'] for iface in interfaces]}")
            return interfaces
        except subprocess.CalledProcessError as e:
            Logger.error(f"Failed to fetch interfaces: {e}")
            return []

    def enable_interface(self, name):
        try:
            subprocess.run(f'netsh interface set interface "{name}" admin=enabled', shell=True, check=True)
            Logger.log(f"Enabled interface: {name}")
        except subprocess.CalledProcessError:
            Logger.error(f"Failed to enable interface: {name}")

    def disable_interface(self, name):
        try:
            subprocess.run(f'netsh interface set interface "{name}" admin=disabled', shell=True, check=True)
            Logger.log(f"Disabled interface: {name}")
        except subprocess.CalledProcessError:
            Logger.error(f"Failed to disable interface: {name}")

    def get_active_interfaces(self):
        self.interfaces = self.get_all_interfaces()
        return [iface["name"] for iface in self.interfaces if iface["status"] == "Connected"]

    def switch_to(self, preferred):
        Logger.log(f"Attempting to switch to preferred interface: {preferred}")
        all_names = [iface["name"] for iface in self.interfaces]
        if preferred not in all_names:
            Logger.error(f"Preferred interface '{preferred}' not found among {all_names}")
            return

        # Disable all others, enable preferred
        for iface in self.interfaces:
            name = iface["name"]
            if name == preferred:
                self.enable_interface(name)
            else:
                self.disable_interface(name)
    
