import json
from typing import Optional

WEEKDAY_MAP = {
    "пн": "monday",
    "понедельник": "monday",
    "вт": "tuesday",
    "вторник": "tuesday",
    "ср": "wednesday",
    "среда": "wednesday",
    "чт": "thursday",
    "четверг": "thursday",
    "пт": "friday",
    "пятница": "friday",
    "сб": "saturday",
    "суббота": "saturday",
    "monday": "monday",
    "tuesday": "tuesday",
    "wednesday": "wednesday",
    "thursday": "thursday",
    "friday": "friday",
    "saturday": "saturday",
}

WEEKDAY_RU = {
    "monday": "понедельник",
    "tuesday": "вторник",
    "wednesday": "среда",
    "thursday": "четверг",
    "friday": "пятница",
    "saturday": "суббота",
    "sunday": "воскресенье",
}


def load_schedule(json_path: str) -> list[dict]:
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)


def normalize_weekday(weekday: str) -> str:
    value = weekday.strip().lower()
    return WEEKDAY_MAP.get(value, value)


def get_schedule_for_day(schedule: list[dict], weekday: str) -> list[dict]:
    weekday_normalized = normalize_weekday(weekday)

    lessons = [
        item for item in schedule
        if item["weekday"] == weekday_normalized and item["slot_type"] == "lesson"
    ]

    lessons.sort(key=lambda x: x["slot_number"])
    return lessons


def format_day_schedule(class_name: str, weekday: str, lessons: list[dict]) -> str:
    weekday_normalized = normalize_weekday(weekday)
    weekday_ru = WEEKDAY_RU.get(weekday_normalized, weekday_normalized)

    if not lessons:
        return f"{class_name} — {weekday_ru}\n\nНа этот день уроков не найдено."

    lines = [f"{class_name} — {weekday_ru}", ""]

    for lesson in lessons:
        lines.append(
            f"{lesson['slot_number']}. {lesson['title']} — {lesson['time_range']}"
        )

    return "\n".join(lines)

import json
from datetime import datetime

def load_schedule(json_path: str) -> list[dict]:
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)


def normalize_weekday(weekday: str) -> str:
    value = weekday.strip().lower()
    return WEEKDAY_MAP.get(value, value)


def get_schedule_for_day(schedule: list[dict], weekday: str) -> list[dict]:
    weekday_normalized = normalize_weekday(weekday)

    lessons = [
        item for item in schedule
        if item["weekday"] == weekday_normalized and item["slot_type"] == "lesson"
    ]

    lessons.sort(key=lambda x: x["slot_number"])
    return lessons


def format_day_schedule(class_name: str, weekday: str, lessons: list[dict]) -> str:
    weekday_normalized = normalize_weekday(weekday)
    weekday_ru = WEEKDAY_RU.get(weekday_normalized, weekday_normalized)

    if not lessons:
        return f"{class_name} — {weekday_ru}\n\nНа этот день уроков не найдено."

    lines = [f"{class_name} — {weekday_ru}", ""]

    for lesson in lessons:
        lines.append(
            f"{lesson['slot_number']}. {lesson['title']} — {lesson['time_range']}"
        )

    return "\n".join(lines)


def parse_time_range(time_range: str) -> tuple[str, str]:
    start_str, end_str = [part.strip() for part in time_range.split("-")]
    return start_str, end_str


def time_to_minutes(time_str: str) -> int:
    dt = datetime.strptime(time_str, "%H:%M")
    return dt.hour * 60 + dt.minute


def get_current_slot(schedule: list[dict], weekday: str, current_time: str) -> Optional[dict]:
    weekday_normalized = normalize_weekday(weekday)
    current_minutes = time_to_minutes(current_time)

    day_slots = [
        item for item in schedule
        if item["weekday"] == weekday_normalized
    ]

    for slot in day_slots:
        start_str, end_str = parse_time_range(slot["time_range"])
        start_minutes = time_to_minutes(start_str)
        end_minutes = time_to_minutes(end_str)

        if start_minutes <= current_minutes < end_minutes:
            return slot

    return None


def format_current_slot(class_name: str, weekday: str, current_slot: Optional[dict]) -> str:
    weekday_normalized = normalize_weekday(weekday)
    weekday_ru = WEEKDAY_RU.get(weekday_normalized, weekday_normalized)

    if current_slot is None:
        return f"{class_name} — {weekday_ru}\n\nСейчас активного слота нет."

    slot_type = current_slot["slot_type"]
    title = current_slot["title"]
    time_range = current_slot["time_range"]

    if slot_type == "lesson":
        return (
            f"{class_name} — {weekday_ru}\n\n"
            f"📚 Сейчас идет {current_slot['slot_number']}-й урок:\n"
            f"{title} — {time_range}"
        )

    if slot_type == "break":
        return (
            f"{class_name} — {weekday_ru}\n\n"
            f"⏸ Сейчас перемена\n"
            f"{time_range}"
        )

    if slot_type == "meal":
        return (
            f"{class_name} — {weekday_ru}\n\n"
            f"🍽 Сейчас {title.lower()}\n"
            f"{time_range}"
        )

    return (
        f"{class_name} — {weekday_ru}\n\n"
        f"Сейчас: {title} — {time_range}"
    )

def parse_time_range(time_range: str):
    start_str, end_str = [part.strip() for part in time_range.split("-")]
    return start_str, end_str


def time_to_minutes(time_str: str) -> int:
    hours, minutes = [int(part.strip()) for part in time_str.split(":")]
    return hours * 60 + minutes


def get_next_lesson(schedule, weekday, current_time):
    weekday_normalized = normalize_weekday(weekday)
    current_minutes = time_to_minutes(current_time)

    day_lessons = [
        item for item in schedule
        if item["weekday"] == weekday_normalized and item["slot_type"] == "lesson"
    ]

    # сортируем по времени начала
    day_lessons.sort(key=lambda item: time_to_minutes(parse_time_range(item["time_range"])[0]))

    current_lesson_index = None

    for i, lesson in enumerate(day_lessons):
        start_str, end_str = parse_time_range(lesson["time_range"])
        start_minutes = time_to_minutes(start_str)
        end_minutes = time_to_minutes(end_str)

        # если сейчас идет этот урок — следующий будет после него
        if start_minutes <= current_minutes < end_minutes:
            current_lesson_index = i
            break

        # если урок еще не начался — это и есть следующий урок
        if current_minutes < start_minutes:
            return lesson

    # если сейчас идет урок, пробуем взять следующий по списку
    if current_lesson_index is not None:
        next_index = current_lesson_index + 1
        if next_index < len(day_lessons):
            return day_lessons[next_index]

    return None


def format_next_lesson(class_name: str, weekday: str, lesson) -> str:
    weekday_normalized = normalize_weekday(weekday)
    weekday_ru = WEEKDAY_RU.get(weekday_normalized, weekday_normalized)

    if lesson is None:
        return f"{class_name} — {weekday_ru}\n\nНа сегодня уроков больше нет."

    return (
        f"{class_name} — {weekday_ru}\n\n"
        f"➡️ Следующий урок:\n"
        f"{lesson['slot_number']}. {lesson['title']} — {lesson['time_range']}"
    )

if __name__ == "__main__":
    schedule = load_schedule("data/schedule.json")

#    lessons = get_schedule_for_day(schedule, "понедельник")
#    print(format_day_schedule("3Б", "понедельник", lessons))

#    print()
#    current_slot = get_current_slot(schedule, "понедельник", "09:45")
#    print(format_current_slot("3Б", "понедельник", current_slot))
