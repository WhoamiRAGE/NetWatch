from collections import deque

MAX_POINTS = 40

ping_history = deque([0.0] * MAX_POINTS, maxlen=MAX_POINTS)


def update_ping(value):
    try:
        ping_history.append(float(value))
    except Exception:
        ping_history.append(0.0)


def render_graph(history, width=40, height=6, label="ms"):
    values = list(history)
    non_zero = [v for v in values if v > 0]

    if not non_zero:
        return "No data yet..."

    max_val = max(non_zero)
    min_val = min(non_zero)
    cur_val = values[-1]

    # Dinamik aralık — dar aralıkta da dalgalanma görünsün
    padding = (max_val - min_val) * 0.2 if max_val != min_val else max_val * 0.1
    range_min = max(0, min_val - padding)
    range_max = max_val + padding
    span = range_max - range_min or 1

    lines = []
    for row in range(height, 0, -1):
        threshold = range_min + span * row / height
        half = span / height / 2
        line = ""
        for v in values:
            if v == 0:
                line += " "
            elif v >= threshold:
                line += "█"
            elif v >= threshold - half:
                line += "▄"
            else:
                line += " "

        axis_val = range_min + span * row / height
        if row == height:
            lines.append(f"│{line}│ {axis_val:.1f}")
        elif row == height // 2:
            lines.append(f"│{line}│ {axis_val:.1f}")
        elif row == 1:
            lines.append(f"│{line}│ {axis_val:.1f}")
        else:
            lines.append(f"│{line}│")

    result = [f"┌{'─' * width}┐"]
    result += lines
    result.append(f"└{'─' * width}┘")
    result.append(f"  cur: {cur_val:.1f}  min: {min_val:.1f}  max: {max_val:.1f}  [{label}]")

    return "\n".join(result)
