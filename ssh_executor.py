import time
import paramiko
from typing import Optional
from rich.console import Console

console = Console()


class CowrieSSHExecutor:
    """
    Connects to Cowrie honeypot via SSH (Paramiko) and executes attacker commands.
    Cowrie accepts any credentials, so this simulates a successful brute-force entry.

    Design: each command gets its own fresh SSH connection + shell channel.
    This ensures a bad command (e.g. nested `ssh`, `exit`, a crashed emulation)
    never leaves the executor in a broken state for the next command.
    """

    def __init__(self, host: str, port: int, username: str, password: str):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.client: Optional[paramiko.SSHClient] = None

    # ── Connection helpers ────────────────────────────────────────────────────

    def connect(self) -> bool:
        """Establish the initial Cowrie SSH connection."""
        return self._new_connection()

    def _new_connection(self) -> bool:
        """Create a fresh Paramiko client connected to Cowrie."""
        # Close any stale client first
        try:
            if self.client:
                self.client.close()
        except Exception:
            pass
        self.client = None

        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(
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
            self.client = client
            return True
        except Exception as e:
            console.print(f"  [red]✗[/red] Cowrie connect failed: {e}")
            self.client = None
            return False

    def _is_alive(self) -> bool:
        """Return True if the current transport is still active."""
        try:
            t = self.client.get_transport() if self.client else None
            return t is not None and t.is_active()
        except Exception:
            return False

    def _ensure_connected(self) -> bool:
        """Reconnect if the current session is dead."""
        if self._is_alive():
            return True
        console.print("  [yellow]⚡[/yellow] Cowrie transport dead — reconnecting...")
        return self._new_connection()

    # ── Command execution ─────────────────────────────────────────────────────

    def execute_commands(self, commands: list[str], delay: float = 1.5) -> list[dict]:
        """
        Execute commands one by one, each in its own fresh shell channel.
        A dead/crashed connection is transparently re-established before each command.
        Returns a list of result dicts: {command, output, success, [error]}.
        """
        if not self.client and not self._new_connection():
            raise RuntimeError("Not connected to Cowrie and reconnect failed.")

        results = []
        for i, cmd in enumerate(commands):
            console.print(f"    [{i+1}/{len(commands)}] Executing: [cyan]{cmd[:80]}[/cyan]")

            # Guarantee a live transport before every command
            if not self._ensure_connected():
                results.append({
                    "command": cmd,
                    "output": "",
                    "success": False,
                    "error": "Could not reconnect to Cowrie",
                })
                continue

            output, success, error = self._run_single(cmd, delay)
            results.append({
                "command": cmd,
                "output":  output,
                "success": success,
                **({"error": error} if error else {}),
            })

        return results

    def _run_single(self, cmd: str, delay: float) -> tuple[str, bool, str]:
        """
        Open a fresh shell channel, run one command, drain output, close channel.
        Returns (output, success, error_msg).

        If the channel/transport dies mid-command (e.g. nested ssh killed it),
        we catch the exception, mark success=False, and let _ensure_connected()
        handle the reconnect on the next call.
        """
        channel = None
        try:
            channel = self.client.invoke_shell()
            channel.settimeout(15)

            # Drain the Cowrie login banner before sending our command
            time.sleep(1.5)
            self._drain(channel)

            channel.send(cmd + "\n")
            time.sleep(delay)
            output = self._drain(channel)
            return output, True, ""

        except paramiko.SSHException as e:
            # The nested ssh / bad command killed the transport — mark dead
            # so the next _ensure_connected() will reconnect.
            console.print(f"    [yellow]⚠[/yellow] SSH channel died during '{cmd[:60]}': {e}")
            try:
                if self.client:
                    self.client.close()
            except Exception:
                pass
            self.client = None
            return "", False, str(e)

        except Exception as e:
            console.print(f"    [yellow]⚠[/yellow] Error during '{cmd[:60]}': {e}")
            return "", False, str(e)

        finally:
            try:
                if channel and not channel.closed:
                    channel.close()
            except Exception:
                pass

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