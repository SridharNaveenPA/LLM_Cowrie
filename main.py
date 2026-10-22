import json
import os
import sys
import time
import argparse
from datetime import datetime, timezone, timedelta
from rich.console import Console
from rich.panel import Panel

from config import (
    COWRIE_HOST, COWRIE_PORT, COWRIE_USER, COWRIE_PASSWORD,
    KALI_HOST, KALI_PORT, KALI_USER, KALI_PASSWORD,
    SCENARIOS, SCENARIOS_DIR, OLLAMA_MODEL,
)
from llm_client import OllamaClient
from ssh_executor import CowrieSSHExecutor, KaliSSHClient
from log_extractor import CowrieLogExtractor
from report_generator import ReportGenerator

console = Console()


def load_scenario(scenario_name: str) -> dict:
    path = os.path.join(SCENARIOS_DIR, f"{scenario_name}.json")
    if not os.path.exists(path):
        console.print(f"[red]Scenario file not found: {path}[/red]")
        sys.exit(1)
    with open(path, "r") as f:
        return json.load(f)


def run_scenario(scenario_name: str, llm: OllamaClient, report_gen: ReportGenerator):
    console.print(Panel(f"[bold cyan]Running Scenario: {scenario_name}[/bold cyan]"))

    # ── 1. Load base scenario ─────────────────────────────────────────────────
    console.print("[bold]Step 1:[/bold] Loading scenario data...")
    scenario_data = load_scenario(scenario_name)

    # ── 2. LLM generates/augments attack commands ─────────────────────────────
    console.print("[bold]Step 2:[/bold] LLM generating attack commands...")
    commands = llm.generate_attack_commands(scenario_name, scenario_data)
    console.print(f"  [green]->[/green] {len(commands)} commands ready")

    # ── 3. Connect to Kali (real SSH) and record start marker ─────────────────
    # IMPORTANT: We read the time FROM Kali directly to avoid Windows/Kali clock
    # skew. We do NOT truncate the log — that breaks Cowrie's file handle.
    console.print("[bold]Step 3:[/bold] Connecting to Kali Linux...")
    kali = KaliSSHClient(KALI_HOST, KALI_PORT, KALI_USER, KALI_PASSWORD)
    if not kali.connect():
        console.print("[red]Cannot connect to Kali. Check KALI_HOST/KALI_USER/KALI_PASSWORD in config.py[/red]")
        return

    extractor = CowrieLogExtractor(kali)

    # ── Health check: verify Cowrie is running and writing logs ───────────────
    console.print("  Checking Cowrie health...")
    if not extractor.check_cowrie_health():
        console.print("[red]Cowrie is not healthy. Restart it in Kali then re-run.[/red]")
        kali.disconnect()
        return

    # Record Kali's current time as our session start marker (before attack begins)
    # record_start_marker() detects Cowrie's clock offset from existing log entries
    console.print("  Recording session start time (detecting Cowrie clock offset)...")
    session_start = extractor.record_start_marker()

    # ── 4. SSH into Cowrie and execute commands ───────────────────────────────
    console.print("[bold]Step 4:[/bold] SSHing into Cowrie honeypot...")
    cowrie = CowrieSSHExecutor(COWRIE_HOST, COWRIE_PORT, COWRIE_USER, COWRIE_PASSWORD)
    if not cowrie.connect():
        console.print("[red]Cannot connect to Cowrie. Is it running? Run: bin/cowrie status (in Kali)[/red]")
        kali.disconnect()
        return

    exec_results = cowrie.execute_commands(commands, delay=1.5)
    cowrie.disconnect()
    console.print(f"  [green]->[/green] Executed {len(exec_results)} commands")

    # ── 5. Extract logs ───────────────────────────────────────────────────────
    console.print("[bold]Step 5:[/bold] Extracting Cowrie logs...")
    # Wait a few seconds for Cowrie to flush buffered log writes
    console.print("  Waiting 5s for Cowrie to flush logs...")
    time.sleep(5)

    # Read session end time — apply same Cowrie clock offset
    kali_now     = extractor.get_kali_utc_time()
    session_end  = kali_now + timedelta(seconds=extractor._last_offset + 10)

    log_entries = extractor.get_session_logs(session_start, session_end)
    console.print(f"  [green]->[/green] {len(log_entries)} log events captured")

    kali.disconnect()

    # ── 6. LLM analyzes logs ──────────────────────────────────────────────────
    console.print("[bold]Step 6:[/bold] LLM analyzing logs for vulnerabilities...")
    if not log_entries:
        console.print("  [yellow]Warning: 0 log entries — Cowrie may not have logged this session.[/yellow]")
        console.print("  [yellow]Check: tail -5 /home/cowrie/cowrie/var/log/cowrie/cowrie.json (in Kali)[/yellow]")

    # Known Cowrie configuration weaknesses — discovered from config inspection.
    # These ground the LLM's analysis in real, observable evidence.
    cowrie_context = {
        "honeypot_type": "Cowrie SSH honeypot (medium-interaction)",
        "cowrie_version": "latest (installed from source)",
        "fake_hostname": "svr04 (or localhost if cfg active)",
        "ssh_banner_version": "SSH-2.0-OpenSSH_9.2p1 Debian-2+deb12u3",
        "shell_kernel_version": "6.1.0-21-amd64",
        "shell_ssh_version": "OpenSSH_7.9p1, OpenSSL 1.1.1a 20 Nov 2018",
        "known_weaknesses": [
            {
                "id": "W1",
                "category": "Realism — Version Mismatch",
                "detail": "SSH banner advertises OpenSSH_9.2p1 (2024) but uname/shell reports OpenSSH_7.9p1 with OpenSSL 1.1.1a (2018). A real attacker running 'ssh -v' or checking $SSH_CLIENT would detect this inconsistency immediately.",
                "severity": "HIGH"
            },
            {
                "id": "W2",
                "category": "Realism — Hypervisor Exposure",
                "detail": "lscpu output contains 'Hypervisor vendor: KVM' and 'Virtualization type: full'. This reveals the system is a virtual machine, which is suspicious for a production server and a classic honeypot indicator.",
                "severity": "HIGH"
            },
            {
                "id": "W3",
                "category": "Emulation Accuracy — Broken top command",
                "detail": "Running 'top' returns 'E82: Cannot allocate any buffer, exiting...' — this is not valid output from any real Linux system. An attacker checking running processes will immediately know the system is fake.",
                "severity": "HIGH"
            },
            {
                "id": "W4",
                "category": "Emulation Accuracy — Sparse command output",
                "detail": "cmdoutput.json contains only 1 emulated command (ps). Almost all attacker commands return empty output or 'command not found', making the system feel hollow and unrealistic.",
                "severity": "MEDIUM"
            },
            {
                "id": "W5",
                "category": "Realism — Generic hostname",
                "detail": "Hostname is 'svr04' with no domain. Real production servers have FQDNs. The prompt shows 'root@svr04' which is a Cowrie default unchanged by the operator.",
                "severity": "MEDIUM"
            },
            {
                "id": "W6",
                "category": "Containment — No credential lockout",
                "detail": "Cowrie accepts ANY username/password combination without lockout. An attacker who intentionally tries 100 wrong passwords and still gets in would suspect a honeypot.",
                "severity": "MEDIUM"
            },
            {
                "id": "W7",
                "category": "Realism — Static command responses",
                "detail": "txtcmds files (df, mount, dmesg) return identical static output on every invocation. Real commands reflect actual system state. An attacker running 'df' twice would get bit-for-bit identical output.",
                "severity": "LOW"
            },
        ],
        "scenario_being_tested": scenario_name,
        "attack_commands_count": len(commands),
        "instructions_for_llm": "Analyze the logs and identify which of the known_weaknesses above were observable during the attack session. Also identify any additional weaknesses not listed. Score each evaluation criterion accordingly."
    }

    analysis = llm.analyze_logs(scenario_name, log_entries, cowrie_context)

    # ── 7. Generate report ────────────────────────────────────────────────────
    console.print("[bold]Step 7:[/bold] Generating Markdown report...")
    report_path = report_gen.generate(
        scenario=scenario_name,
        commands_executed=commands,
        execution_results=exec_results,
        log_entries=log_entries,
        llm_analysis=analysis,
    )
    console.print(f"  [green]Report saved:[/green] {report_path}")
    return report_path


def main():
    parser = argparse.ArgumentParser(description="LLM-based Cowrie Honeypot Evaluator")
    parser.add_argument(
        "--scenario",
        choices=SCENARIOS + ["all"],
        default="credential_discovery",
        help="Attack scenario to run (or 'all' to run every scenario)",
    )
    args = parser.parse_args()

    console.print(Panel(
        f"[bold green]Cowrie Honeypot Evaluator[/bold green]\n"
        f"Model: {OLLAMA_MODEL}\n"
        f"Target: {COWRIE_HOST}:{COWRIE_PORT}",
        title="LLM Honeypot Evaluator"
    ))

    llm = OllamaClient()
    report_gen = ReportGenerator()

    scenarios_to_run = SCENARIOS if args.scenario == "all" else [args.scenario]

    for scenario in scenarios_to_run:
        run_scenario(scenario, llm, report_gen)
        console.print()

    console.print("[bold green]All done![/bold green]")


if __name__ == "__main__":
    main()
