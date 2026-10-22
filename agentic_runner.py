"""
agentic_runner.py

Step-by-step agentic attack loop.

Flow per scenario:
  1.  Connect to Kali (real SSH) — record session start time.
  2.  Connect to Cowrie honeypot.
  3.  Loop up to max_steps:
        a. Ask LLM for the single best next command given what it has seen so far.
        b. Execute that command on Cowrie via SSH.
        c. Extract the Cowrie log events triggered by that command.
        d. Feed command + output + logs back to the LLM as context.
        e. If LLM returns {done: true} — stop the loop early.
  4.  Wait for Cowrie to flush, then pull the full session log window.
  5.  Call LLM to generate a structured vulnerability report from the full history.
  6.  Return (attack_history, full_log_entries, llm_report) to main.py.
"""

import time
from datetime import timedelta
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

from config import (
    COWRIE_HOST, COWRIE_PORT, COWRIE_USER, COWRIE_PASSWORD,
    KALI_HOST, KALI_PORT, KALI_USER, KALI_PASSWORD,
)
from llm_client import OllamaClient
from ssh_executor import CowrieSSHExecutor, KaliSSHClient
from log_extractor import CowrieLogExtractor

console = Console()

# Commands that could harm the Kali host or break the Cowrie session —
# Cowrie emulates them safely, but we skip ones that would kill our SSH channel.
BLOCKED_COMMANDS = {
    "exit", "logout", "quit", "reboot", "shutdown", "halt", "poweroff",
}


def _is_safe(command: str) -> bool:
    """Return False if the command would terminate the SSH session."""
    base = command.strip().split()[0].lower() if command.strip() else ""
    return base not in BLOCKED_COMMANDS


class AgenticRunner:
    """
    Orchestrates the agentic attack loop for one scenario.
    """

    def __init__(self, llm: OllamaClient, max_steps: int = 20, step_delay: float = 2.0):
        self.llm = llm
        self.max_steps = max_steps
        self.step_delay = step_delay  # seconds between commands (lets Cowrie flush logs)

    def run(self, scenario_name: str, scenario_description: str) -> dict:
        """
        Execute the full agentic loop for one scenario.

        Returns a dict:
        {
            "scenario":       str,
            "attack_history": list[dict],   # each step: {step, command, output, cowrie_logs, reasoning}
            "all_log_entries": list[dict],  # full Cowrie session log window
            "steps_taken":    int,
            "stopped_early":  bool,         # True if LLM called DONE before max_steps
        }
        """
        console.print(Panel(
            f"[bold cyan]Agentic Attack Loop — {scenario_name}[/bold cyan]\n"
            f"Max steps: {self.max_steps}  |  Step delay: {self.step_delay}s",
            title="AgenticRunner"
        ))

        # ── 1. Connect to Kali ─────────────────────────────────────────────
        console.print("[bold]Step 1:[/bold] Connecting to Kali Linux...")
        kali = KaliSSHClient(KALI_HOST, KALI_PORT, KALI_USER, KALI_PASSWORD)
        if not kali.connect():
            raise RuntimeError("Cannot connect to Kali. Check KALI_HOST/KALI_USER/KALI_PASSWORD in config.py")

        extractor = CowrieLogExtractor(kali)

        # Health check
        console.print("  Checking Cowrie health...")
        if not extractor.check_cowrie_health():
            kali.disconnect()
            raise RuntimeError("Cowrie is not healthy. Restart it in Kali then re-run.")

        # Record session start in Cowrie's clock space
        console.print("  Recording session start time...")
        session_start = extractor.record_start_marker()

        # ── 2. Connect to Cowrie ───────────────────────────────────────────
        console.print("[bold]Step 2:[/bold] Connecting to Cowrie honeypot...")
        cowrie = CowrieSSHExecutor(COWRIE_HOST, COWRIE_PORT, COWRIE_USER, COWRIE_PASSWORD)
        if not cowrie.connect():
            kali.disconnect()
            raise RuntimeError("Cannot connect to Cowrie. Is it running?")

        # ── 3. Agentic attack loop ─────────────────────────────────────────
        console.print(f"[bold]Step 3:[/bold] Starting agentic loop (up to {self.max_steps} steps)...")
        attack_history: list[dict] = []
        stopped_early = False

        for step_num in range(1, self.max_steps + 1):
            console.print(f"\n  [bold yellow]── Step {step_num}/{self.max_steps} ──[/bold yellow]")

            # 3a. Ask LLM for the next command
            console.print("    [dim]Asking LLM for next command...[/dim]")
            decision = self.llm.generate_next_command(
                scenario=scenario_name,
                scenario_description=scenario_description,
                attack_history=attack_history,
                max_steps=self.max_steps,
            )

            reasoning = decision.get("reasoning", "")
            console.print(f"    Reasoning: [italic]{reasoning[:120]}[/italic]")

            # 3e. LLM says it's done
            if decision.get("done", False):
                console.print("    [green]LLM decided attack is complete.[/green]")
                stopped_early = True
                break

            command = decision.get("command", "").strip()
            if not command:
                console.print("    [yellow]LLM returned empty command — stopping.[/yellow]")
                stopped_early = True
                break

            # Safety gate — skip commands that would kill the session
            if not _is_safe(command):
                console.print(f"    [yellow]Skipping unsafe command:[/yellow] {command}")
                attack_history.append({
                    "step":       step_num,
                    "command":    command,
                    "output":     "[SKIPPED — would terminate SSH session]",
                    "cowrie_logs": [],
                    "reasoning":  reasoning,
                })
                continue

            console.print(f"    Executing: [cyan]{command[:80]}[/cyan]")

            # 3b. Execute the command on Cowrie
            #     We record the timestamp *before* the command so we can fetch
            #     exactly its log events in 3c.
            step_start = extractor.record_start_marker()

            results = cowrie.execute_commands([command], delay=self.step_delay)
            result  = results[0] if results else {"command": command, "output": "", "success": False}
            output  = result.get("output", "")

            console.print(f"    Output: [dim]{repr(output[:200])}[/dim]")

            # 3c. Wait briefly, then extract Cowrie logs for just this command
            time.sleep(1.5)  # let Cowrie flush this event
            kali_now   = extractor.get_kali_utc_time()
            step_end   = kali_now + timedelta(seconds=extractor._last_offset + 5)
            step_logs  = extractor.get_session_logs(step_start, step_end)
            console.print(f"    Cowrie logged: [green]{len(step_logs)} events[/green]")

            # 3d. Append to history for the next LLM call
            attack_history.append({
                "step":        step_num,
                "command":     command,
                "output":      output,
                "cowrie_logs": step_logs,
                "reasoning":   reasoning,
            })

        # ── 4. Disconnect Cowrie, pull full log window ─────────────────────
        cowrie.disconnect()
        console.print("\n[bold]Step 4:[/bold] Waiting for Cowrie to flush full session logs (5s)...")
        time.sleep(5)

        kali_now    = extractor.get_kali_utc_time()
        session_end = kali_now + timedelta(seconds=extractor._last_offset + 10)
        all_log_entries = extractor.get_session_logs(session_start, session_end)
        console.print(f"  Full session: [green]{len(all_log_entries)} log events[/green]")
        kali.disconnect()

        steps_taken = len([h for h in attack_history if "[SKIPPED" not in h.get("output", "")])
        console.print(
            f"\n[bold]Loop complete:[/bold] {steps_taken} commands executed, "
            f"{'stopped early by LLM' if stopped_early else 'reached max steps'}."
        )

        return {
            "scenario":        scenario_name,
            "attack_history":  attack_history,
            "all_log_entries": all_log_entries,
            "steps_taken":     steps_taken,
            "stopped_early":   stopped_early,
        }
