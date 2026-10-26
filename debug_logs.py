"""
debug_logs.py  —  Diagnose why log extraction returns 0 events.
"""
import sys
import json
import paramiko
from datetime import datetime, timezone, timedelta

sys.path.insert(0, ".")
from config import KALI_HOST, KALI_PORT, KALI_USER, KALI_PASSWORD, COWRIE_LOG_PATH

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(KALI_HOST, KALI_PORT, KALI_USER, KALI_PASSWORD, timeout=10)

print("=" * 60)
print("1. TIMEZONE CHECK")
print("=" * 60)
print(f"   Windows time (UTC)  : {windows_now_utc.isoformat()}")

# Kali time
stdin, stdout, stderr = client.exec_command("date -u +'%Y-%m-%dT%H:%M:%S+00:00'")
kali_utc_str = stdout.read().decode().strip()
print(f"   Kali time (UTC)     : {kali_utc_str}")

try:
    kali_utc = datetime.fromisoformat(kali_utc_str)
    diff = abs((windows_now_utc - kali_utc).total_seconds())
    print(f"   Clock difference    : {diff:.1f} seconds")
    if diff > 30:
        print(f"   [PROBLEM] Clocks are out of sync by {diff:.0f}s — this breaks time-window filtering!")
    else:
        print(f"   [OK] Clocks are in sync")
except Exception as e:
    print(f"   Could not compare: {e}")

print()
print("=" * 60)
print("2. LAST 5 LOG ENTRIES (raw)")
print("=" * 60)

stdin, stdout, stderr = client.exec_command(f"tail -5 {COWRIE_LOG_PATH}")
raw = stdout.read().decode(errors="replace")
print(raw)

print("=" * 60)
print("3. TIMESTAMPS IN LOG (last 10 entries)")
print("=" * 60)

stdin, stdout, stderr = client.exec_command(f"cat {COWRIE_LOG_PATH}")
all_lines = stdout.read().decode(errors="replace").splitlines()

entries = []
for line in all_lines:
    line = line.strip()
    if not line:
        continue
    try:
        e = json.loads(line)
        entries.append(e)
    except Exception:
        continue

print(f"   Total log entries   : {len(entries)}")
if entries:
    print(f"   Earliest timestamp  : {entries[0].get('timestamp', 'N/A')}")
    print(f"   Latest timestamp    : {entries[-1].get('timestamp', 'N/A')}")
    print()
    print("   Last 5 entries:")
    for e in entries[-5:]:
        print(f"     {e.get('timestamp','')}  {e.get('eventid',''):35s}  {e.get('input', e.get('message',''))[:60]}")

print()
print("=" * 60)
print("4. SIMULATED TIME WINDOW (what main.py used)")
print("=" * 60)

# The last run started at approximately 13:47:07 UTC (from report filename)
# Let's check what window it would have used
run_start = datetime.fromisoformat("2026-09-09T13:47:07+00:00")
run_end   = run_start + timedelta(minutes=5)
print(f"   Last run window     : {run_start.isoformat()}  →  {run_end.isoformat()}")
print()

# Count matching entries
matched = []
for e in entries:
    ts_str = e.get("timestamp", "")
    if not ts_str:
        continue
    try:
        ts = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
        if run_start <= ts <= run_end:
            matched.append(e)
    except Exception:
        continue

print(f"   Entries in that window : {len(matched)}")
if not matched and entries:
    # Find closest entry
    last_ts_str = entries[-1].get("timestamp", "")
    if last_ts_str:
        last_ts = datetime.fromisoformat(last_ts_str.replace("Z", "+00:00"))
        gap = (run_start - last_ts).total_seconds()
        print(f"   Latest log entry is {gap:.0f}s BEFORE the window start")
        print(f"   --> Root cause: time zone mismatch or log not updated during run")

client.close()
