# utils/network_checker.py

from ping3 import ping

def check_connectivity(host="8.8.8.8", timeout=2):
    """
    Returns True if host responds within timeout, else False
    """
    try:
        delay = ping(host, timeout=timeout)
        if delay is not None:
            return True
        else:
            return False
    except Exception:
        return False
