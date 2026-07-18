from pydantic import BaseModel, Field, field_validator


class ParseRequest(BaseModel):
    text: str = Field(min_length=1)


class MeetingParseRequest(BaseModel):
    raw_text: str = Field(alias="rawText")

    @field_validator("raw_text")
    @classmethod
    def validate_raw_text(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("rawText must not be empty")
        return value


class ActionItem(BaseModel):
    owner: str | None = None
    task: str
    deadline: str | None = None
    content: str | None = None


class MeetingSummary(BaseModel):
    meeting_time: str | None = None
    participants: list[str] = Field(default_factory=list)
    speakers: list[str] = Field(default_factory=list)
    topics: list[str] = Field(default_factory=list)
    conclusions: list[str] = Field(default_factory=list)
    action_items: list[ActionItem] = Field(default_factory=list)
    risks: list[str] = Field(default_factory=list)
    next_steps: list[str] = Field(default_factory=list)


class ParseResponse(MeetingSummary):
    title: str | None = None
    summary: str
