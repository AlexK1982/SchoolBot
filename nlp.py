import re
from datetime import datetime, timedelta


def detect_intent(text: str) -> str:
    text = text.lower()

    if "сейчас" in text:
        return "current"

    if "дальше" in text or "следующий" in text:
        return "next"

    if (
        "расписание" in text
        or "что у" in text
        or "что завтра" in text
        or "что сегодня" in text
    ):
        return "day"

    return "unknown"


def extract_weekday(text: str):
    text = text.lower()

    if "сегодня" in text:
        return datetime.now().strftime("%A").lower()

    if "завтра" in text:
        return (datetime.now() + timedelta(days=1)).strftime("%A").lower()

    days = [
        "понедельник",
        "вторник",
        "среда",
        "четверг",
        "пятница",
        "суббота",
    ]

    for day in days:
        if day in text:
            return day

    return None


def extract_class_name(text: str):
    text = text.strip().upper()
    match = re.search(r"\b(\d{1,2}\s?[А-ЯA-Z])\b", text)

    if not match:
        return None

    class_name = match.group(1).replace(" ", "")
    class_name = class_name.replace("A", "А").replace("B", "В")
    return class_name