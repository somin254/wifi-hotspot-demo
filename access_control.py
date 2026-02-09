from datetime import datetime, timedelta

_sessions = {}

def grant_access(mac_address: str, duration_minutes: int):
    """Allow a device to connect for duration_minutes"""
    expires_at = datetime.now() + timedelta(minutes=duration_minutes)
    _sessions[mac_address] = expires_at
    print(f"[ROUTER] Access granted to {mac_address} until {expires_at}")

def has_access(mac_address: str) -> bool:
    """Check if device still has access"""
    expires_at = _sessions.get(mac_address)
    if not expires_at:
        return False
    if datetime.now() < expires_at:
        return True
    revoke_access(mac_address)
    return False

def revoke_access(mac_address: str):
    """Remove device access"""
    if mac_address in _sessions:
        del _sessions[mac_address]
        print(f"[ROUTER] Access revoked for {mac_address}")

def remaining_time(mac_address: str):
    """Return remaining access time"""
    expires_at = _sessions.get(mac_address)
    if not expires_at:
        return None
    remaining = expires_at - datetime.now()
    return remaining if remaining.total_seconds() > 0 else None

