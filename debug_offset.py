"""
debug_offset.py — Show exactly what the clock offset detection sees and calculates.
"""
import sys, json, paramiko
from datetime import datetime, timezone, timedelta
sys.path.insert(0, ".")
from config import KALI_HOST, KALI_PORT, KALI_USER, KALI_PASSWORD, COWRIE_LOG_PATH

c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect(KALI_HOST, KALI_PORT, KALI_USER, KALI_PASSWORD, timeout=10)

def run(cmd, timeout=15):
    _, o, e = c.exec_command(cmd, timeout=timeout)
    o.channel.settimeout(timeout)
    return o.read().decode(errors="replace").strip()

# 1. Kali system time
epoch = int(run("date -u +%s"))
kali_now = datetime.fromtimestamp(epoch, tz=timezone.utc)
print(f"Kali system time (UTC) : {kali_now.isoformat()}")

# 2. Last 5 log entries
print("\nLast 5 log entries:")
raw = run(f"tail -n 5 {COWRIE_LOG_PATH}")
entries = []
for line in raw.splitlines():
    line = line.strip().replace("\x00","")
    if not line: continue
    try:
        e = json.loads(line)
        ts = e.get("timestamp","")
        eid = e.get("eventid","")
        inp = e.get("input", e.get("message",""))[:40]
        print(f"  {ts}  {eid:35s}  {inp}")
        entries.append(e)
    except: pass

# 3. Calculate offset from latest entry
if entries:
    latest_ts_str = entries[-1].get("timestamp","")
    latest_ts = datetime.fromisoformat(latest_ts_str.replace("Z","+00:00"))
    offset = (latest_ts - kali_now).total_seconds()
    print(f"\nLatest log ts  : {latest_ts.isoformat()}")
    print(f"Kali now       : {kali_now.isoformat()}")
    print(f"Calculated offset : {offset:.0f}s ({offset/3600:.2f}h)")
    
    # 4. Show what session_start would be
    cowrie_now = kali_now + timedelta(seconds=offset)
    marker = cowrie_now - timedelta(seconds=5)
    print(f"\nSession marker would be : {marker.isoformat()}")
    
    # 5. Count how many log entries fall AFTER this marker
    all_raw = run(f"cat {COWRIE_LOG_PATH}")
    after_marker = 0
    total = 0
    for line in all_raw.splitlines():
        line = line.strip().replace("\x00","")
        if not line: continue
        try:
            e = json.loads(line)
            ts_str = e.get("timestamp","")
            if ts_str:
                total += 1
                ts = datetime.fromisoformat(ts_str.replace("Z","+00:00"))
                if ts >= marker:
                    after_marker += 1
        except: pass
    print(f"Total log entries      : {total}")
    print(f"Entries after marker   : {after_marker}")
    if after_marker == 0:
        print("\n[PROBLEM] Marker is in the FUTURE relative to all log entries.")
        print("This means the latest log entry is OLD — not from the current session.")
        print("The offset is being calculated from a stale log entry, not a fresh one.")

c.close()
