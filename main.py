# internet-failover-system/main.py

from core.monitor import Monitor
from utils.logger import Logger


def main():
    Logger.log("Starting Internet Failover System...")
    monitor = Monitor()
    monitor.run()


if __name__ == "__main__":
    main()
