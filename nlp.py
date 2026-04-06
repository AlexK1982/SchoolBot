import re
from datetime import timedelta
from time_utils import now_local

def detect_intent(text: str) -> str:
    text = text.lower().strip()

    if "сейчас" in text:
        return "current"

    if "дальше" in text or "следующий" in text:
        return "next"

    day_words = [
        "понедельник",
        "вторник",
        "среда",
        "четверг",
        "пятница",
        "суббота",
        "сегодня",
        "завтра",
    ]

    if (
        "расписание" in text
        or "что у" in text
        or "что в" in text
        or "что во" in text
        or any(day in text for day in day_words)
    ):
        return "day"

    return "unknown"


def extract_weekday(text: str):
    text = text.lower()

    if "сегодня" in text:
        return now_local().strftime("%A").lower()

    if "завтра" in text:
        return (now_local() + timedelta(days=1)).strftime("%A").lower()

    day_map = {
        "понедельник": "понедельник",
        "пн": "понедельник",
        "вторник": "вторник",
        "вт": "вторник",
        "среда": "среда",
        "ср": "среда",
        "четверг": "четверг",
        "чт": "четверг",
        "пятница": "пятница",
        "пт": "пятница",
        "суббота": "суббота",
        "сб": "суббота",
    }

    for key, value in day_map.items():
        if re.search(rf"\b{re.escape(key)}\b", text):
            return value

    return None


def extract_class_name(text: str):
    text = text.strip().upper()
    match = re.search(r"\b(\d{1,2}\s?[А-ЯA-Z])\b", text)

    if not match:
        return None

    class_name = match.group(1).replace(" ", "")
    class_name = class_name.replace("A", "А").replace("B", "В")
    return class_name