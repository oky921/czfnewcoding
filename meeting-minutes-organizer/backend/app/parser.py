import re

from app.models import ActionItem, ParseResponse
from app.services.meeting_parser import parse_meeting_minutes


def parse_minutes_text(text: str) -> ParseResponse:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    parsed = parse_meeting_minutes(text)

    action_items = [
        ActionItem(
            owner=item.get("owner"),
            content=str(item.get("task") or ""),
            task=item.get("task"),
            deadline=item.get("deadline"),
        )
        for item in parsed["action_items"]
        if isinstance(item, dict)
    ]

    return ParseResponse(
        title=extract_title(lines),
        meeting_time=as_optional_string(parsed["meeting_time"]),
        participants=as_string_list(parsed["participants"]),
        speakers=as_string_list(parsed["speakers"]),
        topics=as_string_list(parsed["topics"]),
        conclusions=as_string_list(parsed["conclusions"]),
        summary=build_summary(lines),
        action_items=action_items,
        risks=as_string_list(parsed["risks"]),
        next_steps=as_string_list(parsed["next_steps"]),
    )


def extract_title(lines: list[str]) -> str | None:
    for line in lines:
        match = re.match(r"^(会议标题|标题|主题)[:：]\s*(.+)$", line)
        if match:
            return match.group(2).strip()
    return lines[0] if lines else None


def build_summary(lines: list[str]) -> str:
    if not lines:
        return ""
    return "\n".join(lines[:5])


def as_optional_string(value: object) -> str | None:
    return value if isinstance(value, str) else None


def as_string_list(value: object) -> list[str]:
    return value if isinstance(value, list) and all(isinstance(item, str) for item in value) else []
