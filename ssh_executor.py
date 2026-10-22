import time
import paramiko
from typing import Optional
from rich.console import Console

console = Console()


class CowrieSSHExecutor:
    """
    Connects to Cowrie honeypot via SSH (Paramiko) and executes attacker commands.
    Cowrie accepts any credentials, so this simulates a successful brute-force entry.
    """

    def __init__(self, host: str, port: int, username: str, password: str):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.client: Optional[paramiko.SSHClient] = None

    def connect(self) -> bool:
        try:
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.client.connect(
                hostname=self.host,
                port=self.port,
                username=self.username,
                password=self.password,
                timeout=30,
                banner_timeout=30,
                auth_timeout=30,
                look_for_keys=False,
                allow_agent=False,
            )
            console.print(f"  [green]✓[/green] Connected to Cowrie at {self.host}:{self.port}")
            return True
        except Exception as e:
            console.print(f"  [red]✗[/red] Failed to connect to Cowrie: {e}")
            return False

    def execute_commands(self, commands: list[str], delay: float = 1.5) -> list[dict]:
        """
        Execute commands one by one via an interactive shell channel.
        Returns a list of result dicts with command + output.
        """
        if not self.client:
            raise RuntimeError("Not connected. Call connect() first.")

        results = []
        channel = self.client.invoke_shell()
        channel.settimeout(15)

        # Wait for initial banner
        time.sleep(2)
        self._drain(channel)

        for i, cmd in enumerate(commands):
            console.print(f"    [{i+1}/{len(commands)}] Executing: [cyan]{cmd[:60]}[/cyan]")
            try:
                channel.send(cmd + "\n")
                time.sleep(delay)
                output = self._drain(channel)
                results.append({
                    "command": cmd,
                    "output": output,
                    "success": True,
                })
            except Exception as e:
                results.append({
                    "command": cmd,
                    "output": "",
                    "success": False,
                    "error": str(e),
                })

        channel.close()
        return results

    def _drain(self, channel, timeout: float = 5.0) -> str:
        """Read all available output from channel."""
        output = ""
        deadline = time.time() + timeout
        while time.time() < deadline:
            if channel.recv_ready():
                chunk = channel.recv(4096).decode("utf-8", errors="replace")
                output += chunk
            else:
                time.sleep(0.2)
        return output

    def disconnect(self):
        if self.client:
            self.client.close()
            self.client = None


class KaliSSHClient:
    """
    Real SSH into Kali Linux (not Cowrie) to read logs and manage Cowrie.
    """

    def __init__(self, host: str, port: int, username: str, password: str):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.client: Optional[paramiko.SSHClient] = None

    def connect(self) -> bool:
        for attempt in range(1, 4):  # retry up to 3 times
            try:
                self.client = paramiko.SSHClient()
                self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                self.client.connect(
                    hostname=self.host,
                    port=self.port,
                    username=self.username,
                    password=self.password,
                    timeout=30,
                    banner_timeout=30,
                    auth_timeout=30,
                    look_for_keys=False,
                    allow_agent=False,
                )
                # Send keepalive every 30s to prevent idle-timeout drops
                self.client.get_transport().set_keepalive(30)
                console.print(f"  [green]OK[/green] Connected to Kali at {self.host}:{self.port}")
                return True
            except paramiko.AuthenticationException:
                console.print(f"  [red]FAIL[/red] Authentication failed for '{self.username}' at {self.host}:{self.port}")
                console.print(f"  [yellow]Hint:[/yellow] Run in Kali:  echo '{self.username}:YOUR_PASSWORD' | sudo chpasswd")
                return False  # No point retrying wrong password
            except paramiko.SSHException as e:
                if attempt < 3:
                    console.print(f"  [yellow]Warn[/yellow] SSH error on attempt {attempt}/3: {e} — retrying in 3s...")
                    time.sleep(3)
                else:
                    console.print(f"  [red]FAIL[/red] SSH error after 3 attempts: {e}")
                    return False
            except Exception as e:
                console.print(f"  [red]FAIL[/red] Cannot connect to Kali at {self.host}:{self.port}: {e}")
                return False
        return False

    def _is_connected(self) -> bool:
        """Check if the SSH transport is still active."""
        try:
            transport = self.client.get_transport() if self.client else None
            return transport is not None and transport.is_active()
        except Exception:
            return False

    def _reconnect(self) -> bool:
        """Silently reconnect if the session dropped."""
        console.print("  [yellow]Warn[/yellow] Kali SSH session dropped — reconnecting...")
        try:
            if self.client:
                self.client.close()
        except Exception:
            pass
        self.client = None
        return self.connect()

    def run(self, command: str, timeout: int = 30) -> tuple[str, str]:
        """Run a command on Kali, return (stdout, stderr). Auto-reconnects if session dropped."""
        # Reconnect if transport is dead
        if not self._is_connected():
            if not self._reconnect():
                raise RuntimeError("Cannot reconnect to Kali SSH")

        try:
            stdin, stdout, stderr = self.client.exec_command(command, timeout=timeout)
            stdout.channel.settimeout(timeout)
            stderr.channel.settimeout(timeout)
            return stdout.read().decode(errors="replace"), stderr.read().decode(errors="replace")
        except paramiko.ssh_exception.SSHException:
            # Session died mid-call — reconnect and retry once
            if not self._reconnect():
                raise RuntimeError("Cannot reconnect to Kali SSH after session drop")
            stdin, stdout, stderr = self.client.exec_command(command, timeout=timeout)
            stdout.channel.settimeout(timeout)
            stderr.channel.settimeout(timeout)
            return stdout.read().decode(errors="replace"), stderr.read().decode(errors="replace")

    def disconnect(self):
        if self.client:
            self.client.close()