import paramiko, sys
sys.path.insert(0, ".")
from config import KALI_HOST, KALI_PORT, KALI_USER, KALI_PASSWORD

print(f"Connecting to {KALI_HOST}:{KALI_PORT} as '{KALI_USER}' with password '{KALI_PASSWORD}'")

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
try:
    client.connect(
        hostname=KALI_HOST,
        port=KALI_PORT,
        username=KALI_USER,
        password=KALI_PASSWORD,
        timeout=15,
        banner_timeout=15,
        auth_timeout=15,
        look_for_keys=False,
        allow_agent=False,
    )
    print("SUCCESS - SSH login worked")
    stdin, stdout, stderr = client.exec_command("whoami && date -u")
    print("Output:", stdout.read().decode().strip())
    client.close()
except paramiko.AuthenticationException as e:
    print(f"FAIL - Wrong password: {e}")
    print(f"Fix in Kali: echo '{KALI_USER}:NEW_PASSWORD' | sudo chpasswd")
    print(f"Then update KALI_PASSWORD in config.py")
except paramiko.SSHException as e:
    print(f"FAIL - SSH protocol error: {e}")
    print("This can mean: wrong port, Cowrie answering instead of real SSH, or SSH server issue")
except Exception as e:
    print(f"FAIL - {type(e).__name__}: {e}")
