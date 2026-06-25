def timeline_serializer(time) -> dict:
    return {
        "time_id": str(time["_id"]),
        "timeline_topic": time.get("timeline_topic", ""),
        "program_name": time.get("program_name", "Winter of Code"),
        "start_date": time.get("start_date", ""),
        "end_date": time.get("end_date", ""),
        "timeline_description": time.get("timeline_description", "")
    }
