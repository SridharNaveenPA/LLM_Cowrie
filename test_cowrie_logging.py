"""
test_cowrie_logging.py
SSHes into Cowrie, runs 'whoami', waits 5s, then checks if it appeared in the log.
This tells us definitively whether Cowrie is logging our sessions.
"""
import sys
import time
import json
import paramiko
from datetime import datetime, timezone

sys.path.insert(0, ".")
from config import (
    COWRIE_HOST, COWRIE_PORT, COWRIE_USER, COWRIE_PASSWORD,
    KALI_HOST, KALI_PORT, KALI_USER, KALI_PASSWORD,
    COWRIE_LOG_PATH,
)

# ── Step 1: Read Kali time and log line count BEFORE the test ─────────────────
kali = paramiko.SSHClient()
kali.set_missing_host_key_policy(paramiko.AutoAddPolicy())
kali.connect(KALI_HOST, KALI_PORT, KALI_USER, KALI_PASSWORD, timeout=10)

stdin, stdout, _ = kali.exec_command(f"date -u +'%Y-%m-%dT%H:%M:%S+00:00'")
kali_time_before = stdout.read().decode().strip()

stdin, stdout, _ = kali.exec_command(f"wc -l < {COWRIE_LOG_PATH}")
lines_before = int(stdout.read().decode().strip() or "0")

print(f"Kali UTC time before : {kali_time_before}")
print(f"Log lines before     : {lines_before}")
print()

# ── Step 2: SSH into Cowrie and run a test command ────────────────────────────
print(f"SSHing into Cowrie at {COWRIE_HOST}:{COWRIE_PORT}...")
cowrie = paramiko.SSHClient()
cowrie.set_missing_host_key_policy(paramiko.AutoAddPolicy())
cowrie.connect(
    COWRIE_HOST, COWRIE_PORT, COWRIE_USER, COWRIE_PASSWORD,
    timeout=10, look_for_keys=False, allow_agent=False,
)
channel = cowrie.invoke_shell()
channel.settimeout(10)
time.sleep(2)

# Drain banner
buf = b""
try:
    while channel.recv_ready():
        buf += channel.recv(4096)
except Exception:
    pass

# Send a distinctive test command
test_cmd = "whoami"
print(f"Sending command: {test_cmd}")
channel.send(test_cmd + "\n")
time.sleep(3)

# Read response
out = b""
try:
    while channel.recv_ready():
        out += channel.recv(4096)
except Exception:
    pass

print(f"Cowrie response: {out.decode(errors='replace').strip()[:100]!r}")
channel.close()
cowrie.close()

# ── Step 3: Wait and check if the log was updated ─────────────────────────────
print("\nWaiting 5s for Cowrie to flush logs...")
time.sleep(5)

stdin, stdout, _ = kali.exec_command(f"wc -l < {COWRIE_LOG_PATH}")
lines_after = int(stdout.read().decode().strip() or "0")

stdin, stdout, _ = kali.exec_command(f"tail -5 {COWRIE_LOG_PATH}")
tail = stdout.read().decode(errors="replace")

kali.close()

print(f"Log lines after      : {lines_after}")
print(f"New lines added      : {lines_after - lines_before}")
print()

if lines_after > lines_before:
    print("SUCCESS - Cowrie IS logging new sessions!")
    print("Last 5 log entries:")
    for line in tail.strip().splitlines():
        try:
            e = json.loads(line)
            print(f"  {e.get('timestamp','')}  {e.get('eventid',''):35s}  {e.get('input', e.get('message',''))[:50]}")
        except Exception:
            print(f"  {line[:100]}")
else:
    print("FAIL - Cowrie is NOT logging new sessions.")
    print()
    print("Possible causes:")
    print("  1. Cowrie src_ip filter — it may be ignoring connections from 192.168.56.1")
    print("     Check: grep -i 'ignore' ~/cowrie/cowrie/etc/cowrie.cfg")
    print("  2. Cowrie sensor/output plugin not writing to JSON")
    print("     Check: grep -A5 'output_jsonlog' ~/cowrie/cowrie/etc/cowrie.cfg")
    print("  3. Cowrie writing to a DIFFERENT log file than expected")
    print("     Check: ls -lt ~/cowrie/cowrie/var/log/cowrie/")
    print()
    print("Run these in Kali and paste output:")
    print("  grep -n 'output_jsonlog\\|ignore_client\\|sensor_name' /home/cowrie/cowrie/etc/cowrie.cfg")
    print("  ls -lt /home/cowrie/cowrie/var/log/cowrie/")
