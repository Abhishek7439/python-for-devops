import argparse
import json
import os
from collections import Counter, defaultdict
from datetime import datetime

# ---------- Helper ----------
def color(text, code):
    return f"\033[{code}m{text}\033[0m"


INFO_C = "37"      # white
WARN_C = "33"      # yellow
ERR_C = "31"       # red
HEAD_C = "36"      # cyan
GOOD_C = "32"      # green


# ---------- Log Analyzer ----------
def analyze_logs(log_file):
    counts = {"INFO": 0, "WARNING": 0, "ERROR": 0}
    hourly_errors = defaultdict(int)
    error_messages = Counter()

    if not os.path.exists(log_file):
        raise FileNotFoundError("Log file not found!")

    with open(log_file, "r", encoding="utf-8") as f:
        lines = f.readlines()
        if not lines:
            return counts, hourly_errors, error_messages

        for line in lines:
            level = None

            if "ERROR" in line:
                level = "ERROR"
                counts["ERROR"] += 1
            elif "WARNING" in line:
                level = "WARNING"
                counts["WARNING"] += 1
            elif "INFO" in line:
                level = "INFO"
                counts["INFO"] += 1

            # Extract timestamp hour if present (YYYY-MM-DD HH:MM:SS)
            if level:
                try:
                    timestamp = line[:19]
                    hour = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S").strftime(
                        "%H:00"
                    )
                    if level == "ERROR":
                        hourly_errors[hour] += 1
                except Exception:
                    pass

            # Collect recurring error messages
            if level == "ERROR":
                error_messages[line.strip()] += 1

    return counts, hourly_errors, error_messages


# ---------- JSON Output ----------
def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    print(color(f"JSON saved → {path}", GOOD_C))


# ---------- HTML Output ----------
def save_html(path, data):
    html = f"""
    <html>
    <head>
        <title>Log Report</title>
        <style>
            body {{ font-family: Arial; background:#0f172a; color:#e5e7eb }}
            .card {{ background:#020617; padding:20px; margin:10px; border-radius:10px }}
            h2 {{ color:#38bdf8 }}
            .error {{ color:#f87171 }}
            .warn {{ color:#facc15 }}
            .info {{ color:#a5f3fc }}
        </style>
    </head>
    <body>
        <h1>Log Analysis Report</h1>

        <div class="card">
            <h2>Counts</h2>
            <p class="info">INFO: {data['counts']['INFO']}</p>
            <p class="warn">WARNING: {data['counts']['WARNING']}</p>
            <p class="error">ERROR: {data['counts']['ERROR']}</p>
        </div>

        <div class="card">
            <h2>Errors Per Hour</h2>
            { "<br>".join([f"{k}: {v}" for k,v in data['hourly_errors'].items()]) }
        </div>

        <div class="card">
            <h2>Top Errors</h2>
            { "<br>".join([f"{m} → {c}" for m,c in data['top_errors']]) }
        </div>
    </body>
    </html>
    """

    with open(path, "w", encoding="utf-8") as f:
        f.write(html)

    print(color(f"HTML saved → {path}", GOOD_C))


# ---------- Terminal Report ----------
def print_report(counts, hourly_errors, error_messages, threshold):
    print(color("\nLOG ANALYSIS REPORT", HEAD_C))
    print("-" * 40)

    print(color(f"INFO     : {counts['INFO']}", INFO_C))
    print(color(f"WARNING  : {counts['WARNING']}", WARN_C))
    print(color(f"ERROR    : {counts['ERROR']}", ERR_C))

    print("\nErrors Per Hour")
    for hour, count in sorted(hourly_errors.items()):
        print(f"{hour} — {count}")

    print("\nTop Error Messages")
    for msg, c in error_messages.most_common(5):
        print(color(f"{c} × {msg}", ERR_C))

    status = (
        color("UNHEALTHY", ERR_C)
        if counts["ERROR"] >= threshold
        else color("HEALTHY", GOOD_C)
    )

    print(f"\nSystem Status: {status}\n")


# ---------- Main ----------
def main():
    parser = argparse.ArgumentParser(description="DevOps Log Analyzer")
    parser.add_argument("--file", required=True, help="Path to log file")
    parser.add_argument("--json", help="Output JSON file")
    parser.add_argument("--html", help="Output HTML dashboard")
    parser.add_argument("--threshold", type=int, default=5, help="Error alert level")

    args = parser.parse_args()

    try:
        counts, hourly_errors, error_messages = analyze_logs(args.file)

        print_report(counts, hourly_errors, error_messages, args.threshold)

        report = {
            "counts": counts,
            "hourly_errors": dict(hourly_errors),
            "top_errors": error_messages.most_common(5),
        }

        if args.json:
            save_json(args.json, report)

        if args.html:
            save_html(args.html, report)

    except Exception as e:
        print(color(f"ERROR: {e}", ERR_C))


if __name__ == "__main__":
    main()
