
import json
from utils.calendar_utils import freebusy
from utils.slot_utils import find_first_common_slot

class MeetingAgent:
    def __init__(self, llm_client, model_path):
        self.client = llm_client
        self.model = model_path

    # 1. Parse mail or JSON into structured constraints using function calling
    def parse_meeting_request(self, raw):
        schema = {
            "name": "extract_constraints",
            "description": "Pull participants, date constraints, duration from user message",
            "parameters": {
                "type": "object",
                "properties": {
                    "participants": {"type": "array", "items": {"type": "string"}},
                    "date": {"type": "string"},
                    "duration_minutes": {"type": "integer"}
                },
                "required": ["participants", "duration_minutes"]
            }
        }
        # Prompt the model to always reply with strict JSON if function calling fails
        user_prompt = (
            "Extract meeting constraints from the following request. "
            "If you cannot use function calling, reply ONLY with a valid JSON object containing "
            "participants, date, and duration_minutes. Do not include any explanation or text outside the JSON.\n\n"
            + json.dumps(raw)
        )
        resp = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": user_prompt}],
            functions=[schema],
            function_call="auto"
        )
        choice = resp.choices[0]
        message = getattr(choice, "message", None)
        function_call = getattr(message, "function_call", None) if message else None
        arguments = getattr(function_call, "arguments", None) if function_call else None
        if arguments:
            return json.loads(arguments)
        # Fallback: try to parse the assistant's message content as JSON
        content = getattr(message, "content", None)
        if content:
            content = content.strip()
            if content.startswith("```json"):
                content = content[len("```json"):].strip()
            elif content.startswith("```"):
                content = content[len("```"):].strip()
            if content.endswith("```"):
                content = content[:-3].strip()
            try:
                return json.loads(content)
            except Exception:
                raise ValueError(f"Model did not return function_call.arguments or valid JSON content. Full response: {resp}")
        raise ValueError(f"Model did not return function_call.arguments or valid JSON content. Full response: {resp}")

    # 2. Fetch calendars
    def fetch_attendees_events(self, emails, start, end):
        return freebusy(emails, start.isoformat(), end.isoformat(), tz=start.tzname())

    # 3. Resolve conflicts
    def resolve_conflicts_and_schedule(self, busy_dict, constraints):
        # Check if requested slot is free for all attendees
        requested_start = constraints.get("requested_start")
        duration = constraints["duration_minutes"]
        timezone = constraints["timezone"]
        # Remove timezone info for comparison if present
        if requested_start and "+" in requested_start:
            requested_start = requested_start.split('+')[0]
        try:
            from datetime import datetime, timedelta
            req_start_dt = datetime.fromisoformat(requested_start)
            req_end_dt = req_start_dt + timedelta(minutes=duration)
        except Exception:
            req_start_dt = None
            req_end_dt = None
        slot_is_free = True
        if req_start_dt and req_end_dt:
            for busy_info in busy_dict.values():
                for busy in busy_info["busy"]:
                    busy_start = busy["start"]
                    busy_end = busy["end"]
                    # Remove timezone info for comparison if present
                    if "+" in busy_start:
                        busy_start = busy_start.split('+')[0]
                    if "+" in busy_end:
                        busy_end = busy_end.split('+')[0]
                    try:
                        busy_start_dt = datetime.fromisoformat(busy_start)
                        busy_end_dt = datetime.fromisoformat(busy_end)
                    except Exception:
                        continue
                    # If overlap, slot is not free
                    if (busy_start_dt < req_end_dt and busy_end_dt > req_start_dt):
                        slot_is_free = False
                        break
                if not slot_is_free:
                    break
        else:
            slot_is_free = False

        if slot_is_free and req_start_dt and req_end_dt:
            return {"start": req_start_dt.isoformat(), "end": req_end_dt.isoformat()}
        # Fallback: find next available slot
        s, e = find_first_common_slot(
            busy_dict,
            constraints["duration_minutes"],
            constraints["start_window"],
            constraints["end_window"],
            constraints["timezone"],
        )
        return {"start": s, "end": e}

    # 4. Generate polite email & final JSON
    def generate_output(self, raw_in, scheduled, busy):
        polite_schema = { ... }  # omitted for brevity
        prompt = f"Compose a friendly confirmation. Details: {scheduled}"
        email_resp = self.client.chat.completions.create(...)
        return {
            **raw_in,
            "EventStart": scheduled["start"].isoformat(),
            "EventEnd": scheduled["end"].isoformat(),
            "Duration_mins": raw_in["Duration_mins"],
            "MetaData": {"email_draft": email_resp.choices[0].message.content},
        }
