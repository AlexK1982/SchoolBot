from datetime import datetime
from zoneinfo import ZoneInfo

SERVICE_TZ = ZoneInfo("Europe/Moscow")

def now_local() -> datetime:
    return datetime.now(SERVICE_TZ)

def today_local():
    return now_local().date()

def weekday_local() -> int:
    return now_local().weekday()