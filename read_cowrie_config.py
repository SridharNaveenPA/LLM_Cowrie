import sys, paramiko, json
sys.path.insert(0, ".")
from config import KALI_HOST, KALI_PORT, KALI_USER, KALI_PASSWORD
c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect(KALI_HOST, KALI_PORT, KALI_USER, KALI_PASSWORD, timeout=10)
def run(cmd):
    _, o, _ = c.exec_command(cmd, timeout=15)
    return o.read().decode(errors="replace").strip()

BASE = "/home/cowrie/cowrie"

print("=== cowrie.cfg.dist (key lines) ===")
print(run(f"grep -v '^#' {BASE}/src/cowrie/data/etc/cowrie.cfg.dist | grep -v '^$' | head -80"))

print("\n=== cmdoutput.json keys ===")
raw = run(f"cat {BASE}/src/cowrie/data/cmdoutput.json")
try:
    d = json.loads(raw)
    for k in list(d.keys())[:30]:
        val = str(d[k])[:60].replace('\n',' ')
        print(f"  {k!r:40s} -> {val}")
    print(f"\n  Total commands: {len(d)}")
except Exception as e:
    print(f"Parse error: {e}")
    print(raw[:500])

print("\n=== lscpu txtcmd ===")
print(run(f"cat {BASE}/src/cowrie/data/txtcmds/usr/bin/lscpu"))

print("\n=== top txtcmd (first 10 lines) ===")
print(run(f"head -10 {BASE}/src/cowrie/data/txtcmds/usr/bin/top"))

c.close()
