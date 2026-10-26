import socket

targets = [
    ("192.168.56.100", 22),
    ("192.168.56.100", 2222),
    ("192.168.56.102", 22),
    ("192.168.56.102", 2222),
]

for ip, port in targets:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    result = s.connect_ex((ip, port))
    s.close()
    status = "OPEN  " if result == 0 else "CLOSED"
    label = ""
    if port == 22:   label = "<-- real SSH (Kali)"
    if port == 2222: label = "<-- Cowrie honeypot"
    print(f"  {status}  {ip}:{port}  {label}")
