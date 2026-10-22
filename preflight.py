"""
preflight.py  —  Verify all connections work before running main.py
Run: python preflight.py
"""
import sys
import socket

sys.path.insert(0, ".")
from config import (
    OLLAMA_BASE_URL, OLLAMA_MODEL,
    COWRIE_HOST, COWRIE_PORT, COWRIE_USER, COWRIE_PASSWORD,
    KALI_HOST, KALI_PORT, KALI_USER, KALI_PASSWORD,
    COWRIE_LOG_PATH,
)

PASS = "[PASS]"
FAIL = "[FAIL]"
INFO = "[INFO]"

def check_port(host, port, label, timeout=3):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    result = s.connect_ex((host, port))
    s.close()
    ok = result == 0
    print(f"  {PASS if ok else FAIL}  {label:35s}  {host}:{port}")
    return ok

print("=" * 60)
print("PRE-FLIGHT CHECK")
print("=" * 60)

# 1. Ollama
print("\n[1] Ollama API")
try:
    import requests
    r = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=5)
    models = [m["name"] for m in r.json().get("models", [])]
    if OLLAMA_MODEL in models:
        print(f"  {PASS}  Ollama reachable, model '{OLLAMA_MODEL}' found")
    else:
        print(f"  {FAIL}  Ollama reachable but model '{OLLAMA_MODEL}' NOT found")
        print(f"  {INFO}  Available models: {models}")
        print(f"  {INFO}  Fix: run  ollama pull {OLLAMA_MODEL}")
except Exception as e:
    print(f"  {FAIL}  Cannot reach Ollama at {OLLAMA_BASE_URL}: {e}")
    print(f"  {INFO}  Fix: run  ollama serve  in a separate PowerShell window")

# 2. Network ports
print("\n[2] Network Connectivity")
cowrie_ok = check_port(COWRIE_HOST, COWRIE_PORT, "Cowrie honeypot (port 2222)")
kali_ok   = check_port(KALI_HOST,   KALI_PORT,   "Kali real SSH  (port 22)")

# 3. Kali SSH login + log file
print("\n[3] Kali SSH Login & Log File")
if kali_ok:
    try:
        import paramiko
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(KALI_HOST, KALI_PORT, KALI_USER, KALI_PASSWORD, timeout=10)
        print(f"  {PASS}  SSH login as '{KALI_USER}' succeeded")

        # Check log file readable directly
        stdin, stdout, stderr = client.exec_command(f"cat {COWRIE_LOG_PATH} 2>&1 | head -1")
        out = stdout.read().decode(errors="replace").strip()
        err = stderr.read().decode(errors="replace").strip()

        if "Permission denied" in out or "Permission denied" in err:
            print(f"  [WARN] Log file not directly readable (expected — will use sudo)")
            # Try sudo
            cmd = f"echo '{KALI_PASSWORD}' | sudo -S head -1 {COWRIE_LOG_PATH} 2>/dev/null"
            stdin, stdout, stderr = client.exec_command(cmd, timeout=10)
            out = stdout.read().decode(errors="replace").strip()
            if out:
                print(f"  {PASS}  Log readable via sudo. First line: {out[:80]}")
            else:
                print(f"  {FAIL}  Cannot read log even with sudo.")
                print(f"  {INFO}  Fix: sudo usermod -aG cowrie rootuser  (run in Kali)")
        elif "No such file" in out:
            print(f"  {FAIL}  Log file not found at: {COWRIE_LOG_PATH}")
            print(f"  {INFO}  Fix: check path, cowrie may log to a different location")
        elif out:
            print(f"  {PASS}  Log file readable. First line: {out[:80]}")
        else:
            print(f"  [WARN] Log file exists but is empty (OK if Cowrie just started)")

        client.close()
    except Exception as e:
        print(f"  {FAIL}  SSH login failed: {e}")
        print(f"  {INFO}  Check KALI_USER='{KALI_USER}' and KALI_PASSWORD in config.py")
else:
    print(f"  [SKIP] Kali SSH unreachable, skipping login test")

# 4. Cowrie SSH login
print("\n[4] Cowrie Honeypot SSH Login")
if cowrie_ok:
    try:
        import paramiko
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(COWRIE_HOST, COWRIE_PORT, COWRIE_USER, COWRIE_PASSWORD,
                       timeout=10, look_for_keys=False, allow_agent=False)
        channel = client.invoke_shell()
        import time; time.sleep(2)
        banner = b""
        channel.settimeout(3)
        try:
            while True:
                chunk = channel.recv(1024)
                if not chunk:
                    break
                banner += chunk
        except Exception:
            pass
        channel.close()
        client.close()
        banner_str = banner.decode(errors="replace").strip()[:100]
        print(f"  {PASS}  Cowrie login succeeded. Banner: {banner_str!r}")
    except Exception as e:
        print(f"  {FAIL}  Cowrie login failed: {e}")
        print(f"  {INFO}  Check Cowrie is running: bin/cowrie status  (in Kali)")
else:
    print(f"  [SKIP] Cowrie unreachable, skipping login test")

print("\n" + "=" * 60)
print("If all checks show [PASS], run:  python main.py --scenario credential_discovery")
print("=" * 60)
