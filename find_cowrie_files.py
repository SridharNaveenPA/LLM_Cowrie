"""
find_cowrie_files.py  —  Map the Cowrie installation to find all editable weakness targets.
"""
import sys
import paramiko

sys.path.insert(0, ".")
from config import KALI_HOST, KALI_PORT, KALI_USER, KALI_PASSWORD

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(KALI_HOST, KALI_PORT, KALI_USER, KALI_PASSWORD, timeout=10)

def run(cmd):
    _, stdout, _ = client.exec_command(cmd, timeout=15)
    return stdout.read().decode(errors="replace").strip()

BASE = "/home/cowrie/cowrie"

print("=" * 60)
print("1. COWRIE CONFIG FILES")
print("=" * 60)
print(run(f"find {BASE} -name '*.cfg' -o -name '*.cfg.dist' 2>/dev/null | sort"))

print("\n" + "=" * 60)
print("2. HONEYFS / FAKE FILESYSTEM")
print("=" * 60)
print(run(f"find {BASE} -name 'honeyfs' -type d 2>/dev/null"))
print(run(f"find {BASE} -path '*/honeyfs/etc*' 2>/dev/null | sort"))
print(run(f"find {BASE} -path '*/honeyfs/proc*' 2>/dev/null | sort"))

print("\n" + "=" * 60)
print("3. TXTCMDS (static command output files)")
print("=" * 60)
txtcmds = run(f"find {BASE} -name 'txtcmds' -type d 2>/dev/null")
print(f"txtcmds dir: {txtcmds}")
if txtcmds:
    print(run(f"find {txtcmds} -type f | sort"))

print("\n" + "=" * 60)
print("4. KEY CONFIG VALUES (cowrie.cfg)")
print("=" * 60)
cfg = run(f"find {BASE}/etc -name 'cowrie.cfg' 2>/dev/null | head -1")
if not cfg:
    cfg = run(f"find {BASE} -name 'cowrie.cfg' 2>/dev/null | head -1")
print(f"Config file: {cfg}")
if cfg:
    print(run(f"grep -E 'hostname|kernel|version|arch|ssh_version|sensor|listen_port' {cfg} 2>/dev/null"))

print("\n" + "=" * 60)
print("5. FAKE /etc/passwd")
print("=" * 60)
passwd = run(f"find {BASE} -path '*/honeyfs/etc/passwd' 2>/dev/null | head -1")
if passwd:
    print(f"Path: {passwd}")
    print(run(f"cat {passwd}"))
else:
    print("Not found — searching deeper...")
    print(run(f"find {BASE} -name 'passwd' 2>/dev/null"))

print("\n" + "=" * 60)
print("6. FAKE /proc/version")
print("=" * 60)
procver = run(f"find {BASE} -path '*/honeyfs/proc/version' 2>/dev/null | head -1")
if procver:
    print(f"Path: {procver}")
    print(run(f"cat {procver}"))
else:
    print("Not found")

print("\n" + "=" * 60)
print("7. SSH BANNER / VERSION STRINGS")
print("=" * 60)
print(run(f"grep -r 'SSH-' {BASE}/etc/ 2>/dev/null | head -5"))
print(run(f"grep -r 'banner\\|version\\|kernel' {BASE}/etc/cowrie.cfg 2>/dev/null | head -10"))

print("\n" + "=" * 60)
print("9. SEARCH IN VAR DIRECTORY")
print("=" * 60)
print(run(f"find {BASE}/var -name 'passwd' -o -name 'cowrie.cfg' 2>/dev/null | sort"))
print(run(f"ls {BASE}/var/ 2>/dev/null"))
print(run(f"find {BASE}/var -maxdepth 4 -type d 2>/dev/null | sort"))

print("\n" + "=" * 60)
print("10. SEARCH ALL PASSWD FILES IN COWRIE")
print("=" * 60)
print(run(f"find {BASE} -name 'passwd' 2>/dev/null | sort"))
print(run(f"find {BASE} -name 'cowrie.cfg' 2>/dev/null | sort"))
print(run(f"find {BASE} -name '*.cfg' ! -path '*/cowrie-env/*' 2>/dev/null | sort"))

print("\n" + "=" * 60)
print("11. COWRIE DATA DIR FULL TREE")
print("=" * 60)
print(run(f"find {BASE}/src/cowrie/data -type f | sort"))

client.close()
