"""
find_kali.py  —  Discover the Kali VM's IP and verify SSH + Cowrie connectivity.
Run this before main.py to confirm your config.py has the right IPs.
"""
import socket
import subprocess
import sys

# ── 1. Show Windows network adapters (find VirtualBox subnets) ────────────────
print("=" * 60)
print("STEP 1: Windows network adapters")
print("=" * 60)
result = subprocess.run(
    ["powershell", "-Command",
     "Get-NetIPAddress -AddressFamily IPv4 | "
     "Select-Object InterfaceAlias, IPAddress, PrefixLength | "
     "Format-Table -AutoSize"],
    capture_output=True, text=True
)
print(result.stdout)

# ── 2. Show ARP table — recently contacted IPs (Kali will be here if used) ───
print("=" * 60)
print("STEP 2: ARP table (recently seen devices on your network)")
print("=" * 60)
result = subprocess.run(["arp", "-a"], capture_output=True, text=True)
print(result.stdout)

# ── 3. Scan common VirtualBox host-only ranges for port 22 ────────────────────
print("=" * 60)
print("STEP 3: Scanning for SSH (port 22) on common VM subnets...")
print("=" * 60)

SUBNETS = ["192.168.56", "192.168.99", "10.0.2", "172.28.128"]
PORTS_TO_CHECK = [22, 2222]
found = []

for subnet in SUBNETS:
    for last_octet in range(100, 115):  # VirtualBox DHCP usually starts at .100
        ip = f"{subnet}.{last_octet}"
        for port in PORTS_TO_CHECK:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.3)
            result = sock.connect_ex((ip, port))
            sock.close()
            if result == 0:
                label = "Cowrie?" if port == 2222 else "SSH (real Kali)"
                print(f"  [FOUND] {ip}:{port}  ← {label}")
                found.append((ip, port))

if not found:
    print("  No hosts found on common ranges.")
    print("  --> Run 'ip addr show' in Kali and paste the IP here.")
else:
    print()
    print("=" * 60)
    print("RECOMMENDATION: Update config.py with:")
    print("=" * 60)
    ssh_hosts  = [ip for ip, p in found if p == 22]
    cowrie_hosts = [ip for ip, p in found if p == 2222]
    if ssh_hosts:
        print(f"  KALI_HOST   = '{ssh_hosts[0]}'")
        print(f"  COWRIE_HOST = '{ssh_hosts[0]}'")
    if cowrie_hosts and not ssh_hosts:
        print(f"  COWRIE_HOST = '{cowrie_hosts[0]}'")
    print()

print("=" * 60)
print("STEP 4: Testing current config.py settings")
print("=" * 60)
try:
    sys.path.insert(0, ".")
    from config import KALI_HOST, KALI_PORT, COWRIE_HOST, COWRIE_PORT

    for host, port, label in [
        (KALI_HOST, KALI_PORT, "Kali SSH (real)"),
        (COWRIE_HOST, COWRIE_PORT, "Cowrie SSH (honeypot)"),
    ]:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        result = sock.connect_ex((host, port))
        sock.close()
        status = "REACHABLE" if result == 0 else f"UNREACHABLE (err={result})"
        icon = "[OK]" if result == 0 else "[FAIL]"
        print(f"  {icon} {label:30s} {host}:{port}  →  {status}")
except Exception as e:
    print(f"  Could not load config: {e}")

print()
print("Done. Fix config.py with the correct IPs above, then run main.py.")
