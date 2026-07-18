import re
from dataclasses import dataclass


@dataclass(frozen=True)
class ParsedActionItem:
    owner: str | None
    task: str
    deadline: str | None


def parse_meeting_minutes(text: str) -> dict[str, object]:
    normalized_text = normalize_text(text)
    lines = [line.strip() for line in normalized_text.splitlines() if line.strip()]
    sections = split_sections(lines)

    action_items = extract_action_items(lines, sections)

    return {
        "meeting_time": extract_meeting_time(normalized_text, lines),
        "participants": extract_participants(lines),
        "speakers": extract_speakers(lines),
        "topics": extract_topics(lines, sections),
        "conclusions": extract_conclusions(lines, sections),
        "action_items": [item.__dict__ for item in action_items],
        "risks": extract_risks(lines, sections),
        "next_steps": extract_next_steps(lines, sections),
    }


def normalize_text(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n").strip()


def split_sections(lines: list[str]) -> dict[str, list[str]]:
    sections: dict[str, list[str]] = {}
    current_key: str | None = None

    for line in lines:
        heading = match_heading(line)
        if heading:
            sections.setdefault(heading, [])
            inline_content = split_heading_inline_content(line)
            if inline_content:
                sections[heading].append(inline_content)
                current_key = None
            else:
                current_key = heading
            continue

        if current_key:
            sections[current_key].append(clean_list_marker(line))

    return sections


def match_heading(line: str) -> str | None:
    heading_patterns = {
        "topics": r"^(会议议题|议题|议程|讨论事项)",
        "conclusions": r"^(关键结论|会议结论|结论|决议|决定事项)",
        "actions": r"^(待办事项|待办|行动项|TODO|Action Items?|后续待办)",
        "risks": r"^(风险与问题|风险问题|问题与风险|风险|问题)",
        "next_steps": r"^(下一步安排|后续安排|下一步|后续计划|下一步)",
    }
    normalized_line = re.sub(r"^[#\-\s]*", "", line).strip()
    for key, pattern in heading_patterns.items():
        if re.match(pattern, normalized_line, re.IGNORECASE):
            return key
    return None


def split_heading_inline_content(line: str) -> str:
    if "：" in line:
        return line.split("：", 1)[1].strip()
    if ":" in line:
        return line.split(":", 1)[1].strip()
    return ""


def extract_meeting_time(text: str, lines: list[str]) -> str | None:
    labeled_patterns = [
        r"(?:会议时间|时间|日期)\s*[:：]\s*([^\n]+)",
        r"(?:会议召开于|开会时间为)\s*([^\n，。；;]+(?:\s*[上下]午)?(?:\s*\d{1,2}[:：]\d{2})?(?:\s*[-~—至到]\s*\d{1,2}[:：]\d{2})?)",
    ]
    for pattern in labeled_patterns:
        match = re.search(pattern, text)
        if match:
            return strip_trailing_punctuation(match.group(1))

    date_pattern = (
        r"\d{4}年\d{1,2}月\d{1,2}日(?:\s*(?:周[一二三四五六日天]))?"
        r"(?:\s*[上下]午)?(?:\s*\d{1,2}[:：]\d{2})?(?:\s*[-~—至到]\s*\d{1,2}[:：]\d{2})?"
    )
    for line in lines[:8]:
        match = re.search(date_pattern, line)
        if match:
            return strip_trailing_punctuation(match.group(0))
    return None


def extract_participants(lines: list[str]) -> list[str]:
    participants: list[str] = []
    for line in lines:
        match = re.match(r"^(参会人员|参会人|与会人员|与会人|参与人|出席人员)\s*[:：]\s*(.+)$", line)
        if not match:
            continue

        raw_names = re.split(r"[、,，;；/\s]+", match.group(2))
        participants.extend(clean_person_name(name) for name in raw_names if clean_person_name(name))
        break

    return unique_keep_order(participants)


def extract_speakers(lines: list[str]) -> list[str]:
    speakers: list[str] = []
    for line in lines:
        match = re.match(r"^([\u4e00-\u9fa5A-Za-z][\u4e00-\u9fa5A-Za-z0-9_·（）()\-]{1,18})\s*[:：]", line)
        if match and not is_heading_like(match.group(1)):
            speakers.append(clean_person_name(match.group(1)))
    return unique_keep_order([speaker for speaker in speakers if speaker])


def extract_topics(lines: list[str], sections: dict[str, list[str]]) -> list[str]:
    topics = sections.get("topics", [])[:]
    for line in lines:
        match = re.match(r"^(会议议题|议题|主题|讨论事项)\s*[:：]\s*(.+)$", line)
        if match:
            topics.extend(split_semicolon_items(match.group(2)))
    return clean_items(topics)


def extract_conclusions(lines: list[str], sections: dict[str, list[str]]) -> list[str]:
    conclusions = sections.get("conclusions", [])[:]
    for line in lines:
        if re.search(r"(结论|决定|确认|达成一致|最终采用|同意|明确)", line) and not re.match(r"^[\u4e00-\u9fa5A-Za-z0-9_·（）()\-]{1,18}\s*[:：]", line):
            conclusions.append(line)
        speaker_content = extract_speaker_content(line)
        if speaker_content and re.search(r"(结论|决定|确认|达成一致|最终采用|同意|明确)", speaker_content):
            conclusions.append(speaker_content)
    return clean_items(conclusions)


def extract_action_items(lines: list[str], sections: dict[str, list[str]]) -> list[ParsedActionItem]:
    candidates = sections.get("actions", [])[:]
    for line in lines:
        if re.search(r"(待办|行动项|TODO|负责|跟进|完成|提交|输出|整理|上线|修复)", line, re.IGNORECASE):
            content = extract_speaker_content(line) or line
            if not re.match(r"^(待办事项|行动项|TODO|Action Items?)\s*[:：]?\s*$", content, re.IGNORECASE):
                candidates.append(content)

    items: list[ParsedActionItem] = []
    for candidate in clean_items(candidates):
        normalized = re.sub(r"^(待办|行动项|TODO|Action Items?)\s*[:：]\s*", "", candidate, flags=re.IGNORECASE)
        item = parse_action_item(normalized)
        if item and not is_duplicate_action_item(item, items):
            items.append(item)
    return items


def parse_action_item(text: str) -> ParsedActionItem | None:
    content = clean_list_marker(text)
    deadline = extract_deadline(content)
    content_without_deadline = remove_deadline(content, deadline) if deadline else content

    owner_patterns = [
        r"^(?P<owner>[\u4e00-\u9fa5A-Za-z0-9_·、和及/\s]{1,30}?)\s*(?:负责|跟进|完成|提交|输出|整理|推进|修复|确认)\s*(?P<task>.+)$",
        r"^(?:负责人|Owner|owner)\s*[:：]\s*(?P<owner>[^，,；;]+)[，,；;]\s*(?:任务|事项)?\s*[:：]?\s*(?P<task>.+)$",
        r"^(?P<task>.+?)[，,；;]\s*(?:负责人|由)\s*[:：]?\s*(?P<owner>[^，,；;]+)$",
    ]
    for pattern in owner_patterns:
        match = re.match(pattern, content_without_deadline, re.IGNORECASE)
        if match:
            owner = clean_owner(match.group("owner"))
            task = strip_trailing_punctuation(match.group("task"))
            return ParsedActionItem(owner=owner, task=task, deadline=deadline)

    if re.search(r"(负责|跟进|完成|提交|输出|整理|推进|修复|确认)", content_without_deadline):
        return ParsedActionItem(owner=None, task=strip_trailing_punctuation(content_without_deadline), deadline=deadline)
    return None


def extract_risks(lines: list[str], sections: dict[str, list[str]]) -> list[str]:
    risks = sections.get("risks", [])[:]
    for line in lines:
        content = extract_speaker_content(line) or line
        if re.search(r"(风险|问题|阻塞|延期|延迟|依赖|不确定|缺口|瓶颈|异常|来不及)", content):
            risks.append(content)
    return clean_items(risks)


def extract_next_steps(lines: list[str], sections: dict[str, list[str]]) -> list[str]:
    next_steps = sections.get("next_steps", [])[:]
    for line in lines:
        content = extract_speaker_content(line) or line
        if re.search(r"(下一步|后续|下周|明天|会后|本周内|月底前|上线前|复盘|排期)", content):
            next_steps.append(content)
    return clean_items(next_steps)


def extract_speaker_content(line: str) -> str | None:
    match = re.match(r"^[\u4e00-\u9fa5A-Za-z][\u4e00-\u9fa5A-Za-z0-9_·（）()\-]{1,18}\s*[:：]\s*(.+)$", line)
    if match and not is_heading_like(line.split("：", 1)[0].split(":", 1)[0]):
        return match.group(1).strip()
    return None


def extract_deadline(text: str) -> str | None:
    deadline_patterns = [
        r"(?:截止时间|截止|完成时间|DDL|ddl|最晚|计划于|在)\s*[:：]?\s*(\d{4}年\d{1,2}月\d{1,2}日(?:\s*\d{1,2}[:：]\d{2})?)",
        r"(?:截止时间|截止|完成时间|DDL|ddl|最晚|计划于|在)\s*[:：]?\s*(\d{1,2}月\d{1,2}日(?:\s*\d{1,2}[:：]\d{2})?)",
        r"(?:截止时间|截止|完成时间|DDL|ddl|最晚|计划于|在)\s*[:：]?\s*((?:本周|下周)?(?:周[一二三四五六日天]|星期[一二三四五六日天]|[一二三四五六日天])(?:上午|下午|晚上)?(?:\s*\d{1,2}[:：]\d{2})?)",
        r"((?:今天|明天|后天|本周内|本月底|月底前|上线前|会后)完成?)",
    ]
    for pattern in deadline_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return strip_trailing_punctuation(match.group(1))
    return None


def remove_deadline(text: str, deadline: str | None) -> str:
    if not deadline:
        return text
    without_deadline = text.replace(deadline, "")
    without_deadline = re.sub(r"(截止时间|截止|完成时间|DDL|ddl|最晚|计划于|在)\s*[:：]?\s*", "", without_deadline)
    return strip_trailing_punctuation(without_deadline)


def split_semicolon_items(text: str) -> list[str]:
    return [item.strip() for item in re.split(r"[；;]", text) if item.strip()]


def clean_items(items: list[str]) -> list[str]:
    cleaned: list[str] = []
    for item in items:
        for part in split_semicolon_items(item):
            cleaned_item = strip_trailing_punctuation(clean_list_marker(part))
            if cleaned_item and not match_heading(cleaned_item):
                cleaned.append(cleaned_item)
    return unique_keep_order(cleaned)


def clean_list_marker(text: str) -> str:
    return re.sub(r"^\s*(?:[-*•]|\d+[.、）)]|[（(]\d+[）)])\s*", "", text).strip()


def strip_trailing_punctuation(text: str) -> str:
    return text.strip().rstrip("。；;，,").strip()


def clean_person_name(name: str) -> str:
    cleaned = re.sub(r"[（(].*?[）)]", "", name).strip()
    cleaned = re.sub(r"^(主持人|记录人|负责人)[:：]", "", cleaned).strip()
    return cleaned


def clean_owner(owner: str) -> str | None:
    parts = [clean_person_name(part) for part in re.split(r"[、/和及\s]+", owner) if clean_person_name(part)]
    if not parts:
        return None
    return "、".join(parts)


def is_heading_like(text: str) -> bool:
    return bool(
        re.match(
            r"^(会议标题|标题|主题|会议时间|时间|日期|参会人员|参会人|与会人员|与会人|参与人|出席人员|主持人|记录人|会议议题|议题|议程|讨论事项|关键结论|会议结论|结论|决议|决定事项|待办事项|待办|行动项|TODO|Action Items?|后续待办|风险与问题|风险问题|问题与风险|风险|问题|下一步安排|后续安排|下一步|后续计划)$",
            text.strip(),
            re.IGNORECASE,
        )
    )


def unique_keep_order(items: list[str]) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()
    for item in items:
        if item and item not in seen:
            result.append(item)
            seen.add(item)
    return result


def is_duplicate_action_item(item: ParsedActionItem, items: list[ParsedActionItem]) -> bool:
    return any(existing.owner == item.owner and existing.task == item.task and existing.deadline == item.deadline for existing in items)
