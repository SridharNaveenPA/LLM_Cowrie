"""
Quick diagnostic: test Paramiko password auth to Kali.
Run: python test_kali_auth.py
"""
import paramiko
import socket
import time

HOST = "192.168.56.102"
PORT = 22
USER = "rootuser"
PASS = "user"

print(f"Testing SSH password auth to {USER}@{HOST}:{PORT}")
print(f"Password being used: '{PASS}'")
print("-" * 50)

# ── Step 1: raw TCP reachability ──────────────────────────────────────────────
print("Step 1: TCP connect test...")
try:
    sock = socket.create_connection((HOST, PORT), timeout=10)
    banner_raw = sock.recv(256)
    banner = banner_raw.decode(errors="replace").strip()
    print(f"  [OK] TCP connected. SSH banner: {banner}")
    sock.close()
except socket.timeout:
    print(f"  [FAIL] TCP timeout — {HOST}:{PORT} not reachable")
    raise SystemExit(1)
except ConnectionRefusedError:
    print(f"  [FAIL] Connection refused — SSH not running on {HOST}:{PORT}")
    raise SystemExit(1)
except Exception as e:
    print(f"  [FAIL] TCP error: {e}")
    raise SystemExit(1)

# ── Step 2: Paramiko auth ─────────────────────────────────────────────────────
print("Step 2: Paramiko password auth...")
time.sleep(1)  # brief pause after banner read

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    client.connect(
        hostname=HOST,
        port=PORT,
        username=USER,
        password=PASS,
        timeout=30,
        banner_timeout=60,     # <-- give SSH server plenty of time
        auth_timeout=30,
        look_for_keys=False,   # <-- only try password, no key files
        allow_agent=False,
    )
    stdin, stdout, stderr = client.exec_command("whoami; id; hostname")
    out = stdout.read().decode().strip()
    err = stderr.read().decode().strip()
    print(f"  [OK] Auth succeeded!")
    print(f"       Output: {out}")
    if err:
        print(f"       stderr: {err}")
    client.close()

except paramiko.AuthenticationException as e:
    print(f"  [FAIL] Wrong password or user doesn't exist: {e}")
    print()
    print("  Fix in Kali terminal:")
    print(f"    sudo passwd {USER}         # reset password")
    print(f"    grep PasswordAuthentication /etc/ssh/sshd_config")
    print(f"    grep {USER} /etc/passwd    # check user exists")

except paramiko.SSHException as e:
    print(f"  [FAIL] SSH handshake error: {e}")
    print()
    print("  This is NOT a password issue — the SSH session failed before auth.")
    print("  Possible causes:")
    print("    - fail2ban or ufw blocking this IP on Kali")
    print("    - /etc/hosts.deny blocking connections")
    print("    - MaxStartups limit hit in sshd_config")
    print()
    print("  Fix in Kali terminal:")
    print("    sudo fail2ban-client status sshd          # check if banned")
    print("    sudo fail2ban-client set sshd unbanip <your_windows_ip>")
    print("    sudo ufw status                           # check firewall")
    print("    sudo grep -E 'MaxStartups|MaxSessions' /etc/ssh/sshd_config")

except socket.timeout:
    print(f"  [FAIL] Paramiko timed out connecting to {HOST}:{PORT}")

except Exception as e:
    print(f"  [FAIL] Unexpected error: {type(e).__name__}: {e}")
