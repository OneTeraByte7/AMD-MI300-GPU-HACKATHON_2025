from datetime import datetime, timedelta

def merge_intervals(intervals):
    intervals.sort(key=lambda x: x[0])
    merged = []
    for s, e in intervals:
        if not merged or merged[-1][1] < s:
            merged.append([s, e])
        else:
            merged[-1][1] = max(merged[-1][1], e)
    return merged

def find_first_common_slot(busy_dict, duration_min, search_start, search_end, tz):
    one_day = timedelta(days=1)
    # Convert to datetime if strings
    if isinstance(search_start, str):
        search_start = datetime.fromisoformat(search_start)
    if isinstance(search_end, str):
        search_end = datetime.fromisoformat(search_end)
    cursor = search_start
    while cursor < search_end:
        day_end = cursor.replace(hour=23, minute=59, second=59)
        day_busy = []
        for cal in busy_dict.values():
            for b in cal["busy"]:
                day_busy.append([datetime.fromisoformat(b["start"]), datetime.fromisoformat(b["end"])] )
        merged = merge_intervals(day_busy)
        free_pointer = cursor
        for b in merged:
            if (b[0] - free_pointer).total_seconds() / 60 >= duration_min:
                return free_pointer, free_pointer + timedelta(minutes=duration_min)
            free_pointer = max(free_pointer, b[1])
        cursor = (cursor + one_day).replace(hour=search_start.hour, minute=search_start.minute)
    return None, None
