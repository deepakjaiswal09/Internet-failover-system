# utils/logger.py

from datetime import datetime

class Logger:
    @staticmethod
    def log(message):
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}")
