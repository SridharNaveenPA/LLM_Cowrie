"""
debug_logs2.py  —  Read cowrie log directly and show timestamps vs session window.
"""
import sys
import json
import paramiko
from datetime import datetime, timezone, timedelta

sys.path.insert(0, ".")
from config import KALI_HOST, KALI_PORT, KALI_USER, KALI_PASSWORD, COWRIE_LOG_PATH

# ── Connect ───────────────────────────────────────────────────────────────────
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
try:
    client.connect(KALI_HOST, KALI_PORT, KALI_USER, KALI_PASSWORD, timeout=10)
except Exception as e:
    print(f"SSH login failed: {e}")
    print(f"Update KALI_PASSWORD in config.py — current value might be wrong.")
    sys.exit(1)

# ── Read log ──────────────────────────────────────────────────────────────────
stdin, stdout, stderr = client.exec_command(f"cat {COWRIE_LOG_PATH}", timeout=30)
raw = stdout.read().decode(errors="replace")
client.close()

entries = []
for line in raw.splitlines():
    line = line.strip()
    if not line:
        continue
    try:
        entries.append(json.loads(line))
    except Exception:
        continue

print(f"Total entries in log: {len(entries)}")
print()

if not entries:
    print("Log is empty. Cowrie may not have logged the session yet.")
    sys.exit(0)

print("All timestamps in log:")
for e in entries:
    ts  = e.get("timestamp", "N/A")
    eid = e.get("eventid", "")
    inp = e.get("input", e.get("message", ""))[:50]
    print(f"  {ts}  {eid:40s}  {inp}")

print()

# ── Show the window main.py would use ────────────────────────────────────────
# From report filename: credential_discovery_2026-09-09_13-47-07.md
# session_start = when python started, session_end = after commands finish
# Commands took ~54 * 1.5s = ~81 seconds, plus overhead
report_start = datetime.fromisoformat("2026-09-09T13:47:07+00:00")
report_end   = report_start + timedelta(minutes=5)

print(f"Session window used by main.py:")
print(f"  Start : {report_start.isoformat()}")
print(f"  End   : {report_end.isoformat()}")
print()

matched = []
for e in entries:
    ts_str = e.get("timestamp", "")
    if not ts_str:
        continue
    try:
        ts = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
        if report_start <= ts <= report_end:
            matched.append(e)
    except Exception:
        continue

print(f"Entries matching that window: {len(matched)}")

if not matched:
    # Find out where entries actually are
    timestamps = []
    for e in entries:
        ts_str = e.get("timestamp", "")
        if ts_str:
            try:
                timestamps.append(datetime.fromisoformat(ts_str.replace("Z", "+00:00")))
            except Exception:
                pass
    if timestamps:
        earliest = min(timestamps)
        latest   = max(timestamps)
        print(f"\nActual log range: {earliest.isoformat()}  to  {latest.isoformat()}")
        print(f"Window start was: {report_start.isoformat()}")
        gap = (report_start - latest).total_seconds()
        if gap > 0:
            print(f"\n[ROOT CAUSE] Latest log entry is {gap:.0f}s BEFORE window start.")
            print(f"  The log was ROTATED (truncated) after these entries were written,")
            print(f"  then Cowrie wrote NEW entries during the attack — but those new")
            print(f"  entries have different timestamps than expected, OR the log was")
            print(f"  truncated and Cowrie stopped writing to it.")
        elif (earliest - report_start).total_seconds() > 0:
            print(f"\n[ROOT CAUSE] All log entries are AFTER the window end.")
            print(f"  Clock skew: Kali clock may be ahead of Windows clock.")
