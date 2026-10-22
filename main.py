"""
main.py — LLM-based Cowrie Honeypot Evaluator (Agentic Mode)

Flow:
  1. Load the attack scenario description.
  2. Run AgenticRunner: LLM picks one command at a time, executes it on Cowrie,
     reads the output + Cowrie logs, then decides the next command.
  3. After the loop, LLM generates a structured vulnerability report from
     the full attack history.
  4. ReportGenerator writes a Markdown file.
"""

import json
import os
import sys
import argparse
from datetime import datetime, timezone
from rich.console import Console
from rich.panel import Panel

from config import (
    COWRIE_HOST, COWRIE_PORT,
    SCENARIOS, SCENARIOS_DIR, OLLAMA_MODEL,
)
from llm_client import OllamaClient
from agentic_runner import AgenticRunner
from report_generator import ReportGenerator

console = Console()

# Default number of agentic steps per scenario
DEFAULT_MAX_STEPS = 20


def load_scenario(scenario_name: str) -> dict:
    path = os.path.join(SCENARIOS_DIR, f"{scenario_name}.json")
    if not os.path.exists(path):
        console.print(f"[red]Scenario file not found: {path}[/red]")
        sys.exit(1)
    with open(path, "r") as f:
        return json.load(f)


def run_scenario(
    scenario_name: str,
    llm: OllamaClient,
    report_gen: ReportGenerator,
    max_steps: int = DEFAULT_MAX_STEPS,
):
    console.print(Panel(f"[bold cyan]Scenario: {scenario_name}[/bold cyan]"))

    # ── 1. Load scenario description ──────────────────────────────────────
    console.print("[bold]Step 1:[/bold] Loading scenario data...")
    scenario_data   = load_scenario(scenario_name)
    scenario_desc   = scenario_data.get("description", scenario_name)
    console.print(f"  Description: {scenario_desc[:120]}")

    # ── 2. Run the agentic attack loop ─────────────────────────────────────
    console.print(f"[bold]Step 2:[/bold] Running agentic attack loop (max {max_steps} steps)...")
    runner = AgenticRunner(llm=llm, max_steps=max_steps, step_delay=2.0)
    result = runner.run(
        scenario_name=scenario_name,
        scenario_description=scenario_desc,
    )

    attack_history  = result["attack_history"]
    all_log_entries = result["all_log_entries"]
    steps_taken     = result["steps_taken"]
    stopped_early   = result["stopped_early"]

    console.print(
        f"  [green]→[/green] {steps_taken} commands executed, "
        f"{len(all_log_entries)} total Cowrie events captured"
    )

    # ── 3. LLM generates final vulnerability report ────────────────────────
    console.print("[bold]Step 3:[/bold] LLM generating final vulnerability report...")
    analysis = llm.generate_final_report(
        scenario=scenario_name,
        attack_history=attack_history,
    )

    # ── 4. Write Markdown report ───────────────────────────────────────────
    console.print("[bold]Step 4:[/bold] Writing Markdown report...")
    report_path = report_gen.generate_agentic(
        scenario=scenario_name,
        attack_history=attack_history,
        all_log_entries=all_log_entries,
        llm_analysis=analysis,
        stopped_early=stopped_early,
    )
    console.print(f"  [green]Report saved:[/green] {report_path}")
    return report_path


def main():
    parser = argparse.ArgumentParser(
        description="LLM-based Cowrie Honeypot Evaluator — Agentic Mode"
    )
    parser.add_argument(
        "--scenario",
        choices=SCENARIOS + ["all"],
        default="credential_discovery",
        help="Attack scenario to run (or 'all' to run every scenario)",
    )
    parser.add_argument(
        "--max-steps",
        type=int,
        default=DEFAULT_MAX_STEPS,
        dest="max_steps",
        help=f"Maximum agentic attack steps per scenario (default: {DEFAULT_MAX_STEPS})",
    )
    args = parser.parse_args()

    console.print(Panel(
        f"[bold green]Cowrie Honeypot Evaluator — Agentic Mode[/bold green]\n"
        f"Model      : {OLLAMA_MODEL}\n"
        f"Target     : {COWRIE_HOST}:{COWRIE_PORT}\n"
        f"Max steps  : {args.max_steps}",
        title="LLM Honeypot Evaluator v2"
    ))

    llm        = OllamaClient()
    report_gen = ReportGenerator()

    scenarios_to_run = SCENARIOS if args.scenario == "all" else [args.scenario]

    for scenario in scenarios_to_run:
        try:
            run_scenario(scenario, llm, report_gen, max_steps=args.max_steps)
        except Exception as e:
            console.print(f"[red]Error running scenario '{scenario}': {e}[/red]")
            import traceback
            traceback.print_exc()
        console.print()

    console.print("[bold green]All done![/bold green]")


if __name__ == "__main__":
    main()
