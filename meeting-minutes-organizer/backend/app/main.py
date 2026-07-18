from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.models import ActionItem, MeetingParseRequest, MeetingSummary, ParseRequest, ParseResponse
from app.parser import parse_minutes_text
from app.services.meeting_parser import parse_meeting_minutes

app = FastAPI(title="Meeting Minutes Organizer API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5173", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/minutes/parse")
def parse_minutes(request: ParseRequest) -> ParseResponse:
    return parse_minutes_text(request.text)


@app.post("/api/meetings/parse", response_model=MeetingSummary)
def parse_meeting(request: MeetingParseRequest) -> MeetingSummary:
    parsed = parse_meeting_minutes(request.raw_text)
    return MeetingSummary(
        meeting_time=as_optional_string(parsed["meeting_time"]),
        participants=as_string_list(parsed["participants"]),
        speakers=as_string_list(parsed["speakers"]),
        topics=as_string_list(parsed["topics"]),
        conclusions=as_string_list(parsed["conclusions"]),
        action_items=as_action_items(parsed["action_items"]),
        risks=as_string_list(parsed["risks"]),
        next_steps=as_string_list(parsed["next_steps"]),
    )


def as_optional_string(value: object) -> str | None:
    return value if isinstance(value, str) else None


def as_string_list(value: object) -> list[str]:
    return value if isinstance(value, list) and all(isinstance(item, str) for item in value) else []


def as_action_items(value: object) -> list[ActionItem]:
    if not isinstance(value, list):
        return []

    items: list[ActionItem] = []
    for item in value:
        if not isinstance(item, dict):
            continue
        task = item.get("task")
        if not isinstance(task, str) or not task:
            continue
        items.append(
            ActionItem(
                owner=item.get("owner") if isinstance(item.get("owner"), str) else None,
                task=task,
                deadline=item.get("deadline") if isinstance(item.get("deadline"), str) else None,
                content=task,
            )
        )
    return items
