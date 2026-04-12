import re
from datetime import timedelta
from time_utils import now_local


WEEKDAY_BY_INDEX = {
    0: "monday",
    1: "tuesday",
    2: "wednesday",
    3: "thursday",
    4: "friday",
    5: "saturday",
    6: "sunday",
}


def detect_intent(text: str) -> str:
    text = text.lower().strip()

    current_patterns = [
        "что сейчас",
        "что идет сейчас",
        "какой сейчас урок",
        "какой урок сейчас",
        "что у меня сейчас",
        "сейчас",
    ]

    next_patterns = [
        "что дальше",
        "что потом",
        "следующий урок",
        "какой следующий урок",
        "что будет дальше",
        "что у меня дальше",
        "дальше",
        "следующий",
    ]

    day_patterns = [
        "что сегодня",
        "что завтра",
        "расписание",
        "какое расписание",
        "какое сегодня расписание",
        "какое завтра расписание",
        "что у",
        "что в",
        "что во",
        "какие уроки",
        "какие сегодня уроки",
        "какие завтра уроки",
        "уроки",
    ]

    if any(pattern in text for pattern in current_patterns):
        return "current"

    if any(pattern in text for pattern in next_patterns):
        return "next"

    day_words = [
        "понедельник",
        "вторник",
        "среда",
        "четверг",
        "пятница",
        "суббота",
        "воскресенье",
        "пн",
        "вт",
        "ср",
        "чт",
        "пт",
        "сб",
        "вс",
        "сегодня",
        "завтра",
    ]

    if any(pattern in text for pattern in day_patterns) or any(
        re.search(rf"\b{re.escape(day)}\b", text) for day in day_words
    ):
        return "day"

    return "unknown"


def extract_weekday(text: str):
    text = text.lower().strip()

    if "сегодня" in text:
        return WEEKDAY_BY_INDEX[now_local().weekday()]

    if "завтра" in text:
        tomorrow = now_local() + timedelta(days=1)
        return WEEKDAY_BY_INDEX[tomorrow.weekday()]

    day_map = {
        "понедельник": "monday",
        "пн": "monday",
        "вторник": "tuesday",
        "вт": "tuesday",
        "среда": "wednesday",
        "ср": "wednesday",
        "четверг": "thursday",
        "чт": "thursday",
        "пятница": "friday",
        "пт": "friday",
        "суббота": "saturday",
        "сб": "saturday",
        "воскресенье": "sunday",
        "вс": "sunday",
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