"""
main.py — LLM-based Cowrie Honeypot Evaluator (Agentic Mode)

Flow:
  1. Load the attack scenario description.
  2. Run AgenticRunner: LLM picks one command at a time, executes it on Cowrie,
     reads the output + Cowrie logs, then decides the next command.
  3. After the loop, LLM generates a structured vulnerability report from
     the full attack history.
  4. ReportGenerator writes a Markdown file.

Custom scenario flow (--custom-scenario / interactive prompt):
  1. User types a free-text attack scenario (up to 2000 characters).
  2. LLM derives the initial command set from that text via
     generate_commands_from_custom_scenario().
  3. Same agentic loop runs — the full custom text is passed as additional
     context so the LLM always has the user's intent in view.
  4. Report header includes the original custom text.
"""

import json
import os
import sys
import argparse
import textwrap
from datetime import datetime, timezone
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm

from config import (
    COWRIE_HOST, COWRIE_PORT,
    SCENARIOS, SCENARIOS_DIR, OLLAMA_MODEL,
    CUSTOM_SCENARIO_MAX_CHARS,
)
from llm_client import OllamaClient
from agentic_runner import AgenticRunner
from report_generator import ReportGenerator

console = Console()

# Default number of agentic steps per scenario
DEFAULT_MAX_STEPS = 15


def load_scenario(scenario_name: str) -> dict:
    path = os.path.join(SCENARIOS_DIR, f"{scenario_name}.json")
    if not os.path.exists(path):
        console.print(f"[red]Scenario file not found: {path}[/red]")
        sys.exit(1)
    with open(path, "r") as f:
        return json.load(f)


def prompt_custom_scenario() -> str:
    """
    Interactively ask the user to enter a free-text attack scenario.
    Enforces the CUSTOM_SCENARIO_MAX_CHARS limit.
    Returns the trimmed text.
    """
    console.print(Panel(
        f"[bold yellow]Custom Scenario Input[/bold yellow]\n"
        f"Describe the attack scenario you want to simulate.\n"
        f"Maximum [bold]{CUSTOM_SCENARIO_MAX_CHARS}[/bold] characters.\n\n"
        "[dim]Enter your scenario text below and press Enter twice (blank line) to confirm.[/dim]",
        title="Custom Scenario"
    ))

    lines = []
    console.print("[bold cyan]>[/bold cyan] ", end="")
    try:
        while True:
            line = input()
            if line == "" and lines and lines[-1] == "":
                # Two consecutive blank lines = done
                break
            lines.append(line)
            if not line:
                console.print("[bold cyan]>[/bold cyan] ", end="")
            # Provide live character count feedback on each non-empty line
            current_text = "\n".join(lines).strip()
            if line:
                remaining = CUSTOM_SCENARIO_MAX_CHARS - len(current_text)
                if remaining < 0:
                    console.print(
                        f"  [red]⚠  Over limit by {-remaining} chars — text will be truncated.[/red]"
                    )
                else:
                    console.print(
                        f"  [dim]{len(current_text)}/{CUSTOM_SCENARIO_MAX_CHARS} chars "
                        f"({remaining} remaining)[/dim]"
                    )
                console.print("[bold cyan]>[/bold cyan] ", end="")
    except EOFError:
        pass  # piped input

    text = "\n".join(lines).strip()

    if not text:
        console.print("[red]No scenario text entered. Exiting.[/red]")
        sys.exit(1)

    # Enforce hard limit
    if len(text) > CUSTOM_SCENARIO_MAX_CHARS:
        console.print(
            f"[yellow]Text exceeds {CUSTOM_SCENARIO_MAX_CHARS} chars "
            f"({len(text)} entered) — truncating.[/yellow]"
        )
        text = text[:CUSTOM_SCENARIO_MAX_CHARS]

    console.print(f"\n[green]✓ Scenario captured ({len(text)} chars)[/green]")
    console.print(Panel(
        textwrap.fill(text, width=80),
        title="Your Scenario",
        border_style="dim"
    ))
    if not Confirm.ask("Proceed with this scenario?", default=True):
        console.print("[yellow]Cancelled.[/yellow]")
        sys.exit(0)

    return text


def run_scenario(
    scenario_name: str,
    llm: OllamaClient,
    report_gen: ReportGenerator,
    max_steps: int = DEFAULT_MAX_STEPS,
    custom_scenario_text: str | None = None,
):
    """
    Run one scenario (predefined or custom) through the full agentic pipeline.

    When custom_scenario_text is provided, scenario_name is 'custom' and the
    description is derived from the first 120 chars of the text.
    """
    console.print(Panel(
        f"[bold cyan]Scenario: {scenario_name}[/bold cyan]"
        + (f"\n[dim]{custom_scenario_text[:120]}…[/dim]" if custom_scenario_text else ""),
    ))

    # ── 1. Load / build scenario description ─────────────────────────────
    console.print("[bold]Step 1:[/bold] Loading scenario data...")
    if custom_scenario_text:
        # For custom scenarios we don't load a JSON file — the text IS the scenario
        scenario_desc = custom_scenario_text[:120].replace("\n", " ")
        console.print(f"  Custom scenario: {scenario_desc}")
    else:
        scenario_data = load_scenario(scenario_name)
        scenario_desc = scenario_data.get("description", scenario_name)
        console.print(f"  Description: {scenario_desc[:120]}")

    # ── 2. Run the agentic attack loop ────────────────────────────────────
    console.print(f"[bold]Step 2:[/bold] Running agentic attack loop (max {max_steps} steps)...")
    runner = AgenticRunner(llm=llm, max_steps=max_steps, step_delay=2.0)
    result = runner.run(
        scenario_name=scenario_name,
        scenario_description=scenario_desc,
        custom_scenario_text=custom_scenario_text,
    )

    attack_history  = result["attack_history"]
    all_log_entries = result["all_log_entries"]
    steps_taken     = result["steps_taken"]
    stopped_early   = result["stopped_early"]

    console.print(
        f"  [green]→[/green] {steps_taken} commands executed, "
        f"{len(all_log_entries)} total Cowrie events captured"
    )

    # ── 3. LLM generates final vulnerability report ───────────────────────
    console.print("[bold]Step 3:[/bold] LLM generating final vulnerability report...")
    analysis = llm.generate_final_report(
        scenario=scenario_name,
        attack_history=attack_history,
    )

    # ── 4. Write Markdown report ──────────────────────────────────────────
    console.print("[bold]Step 4:[/bold] Writing Markdown report...")
    report_path = report_gen.generate_agentic(
        scenario=scenario_name,
        attack_history=attack_history,
        all_log_entries=all_log_entries,
        llm_analysis=analysis,
        stopped_early=stopped_early,
        custom_scenario_text=custom_scenario_text,
    )
    console.print(f"  [green]Report saved:[/green] {report_path}")
    return report_path


def main():
    parser = argparse.ArgumentParser(
        description="LLM-based Cowrie Honeypot Evaluator — Agentic Mode"
    )

    scenario_group = parser.add_mutually_exclusive_group()
    scenario_group.add_argument(
        "--scenario",
        choices=SCENARIOS + ["all"],
        default=None,
        help=(
            "Predefined attack scenario to run (or 'all' to run every scenario). "
            f"Choices: {', '.join(SCENARIOS)}, all"
        ),
    )
    scenario_group.add_argument(
        "--custom-scenario",
        metavar="TEXT",
        default=None,
        dest="custom_scenario",
        help=(
            f"Free-text description of a custom attack scenario "
            f"(max {CUSTOM_SCENARIO_MAX_CHARS} chars). "
            "If you omit the value you will be prompted interactively."
        ),
    )

    parser.add_argument(
        "--max-steps",
        type=int,
        default=DEFAULT_MAX_STEPS,
        dest="max_steps",
        help=f"Maximum agentic attack steps per scenario (default: {DEFAULT_MAX_STEPS})",
    )
    args = parser.parse_args()

    # ── Determine mode ────────────────────────────────────────────────────
    custom_text: str | None = None

    if args.custom_scenario is not None:
        # Flag was explicitly passed — could be empty string (user forgot the value)
        raw = args.custom_scenario.strip()
        if not raw:
            # --custom-scenario was given with no/empty value → prompt interactively
            custom_text = prompt_custom_scenario()
        else:
            if len(raw) > CUSTOM_SCENARIO_MAX_CHARS:
                console.print(
                    f"[yellow]Custom scenario text exceeds {CUSTOM_SCENARIO_MAX_CHARS} chars "
                    f"({len(raw)} given) — truncating.[/yellow]"
                )
                raw = raw[:CUSTOM_SCENARIO_MAX_CHARS]
            custom_text = raw
    elif args.scenario is None:
        # Neither --scenario nor --custom-scenario was given → prompt the user
        # to choose between predefined scenarios or enter a custom one.
        console.print(Panel(
            "[bold green]Select a mode:[/bold green]\n"
            "  [1] Run a predefined attack scenario\n"
            "  [2] Enter a custom scenario (free text)",
            title="Honeypot Evaluator"
        ))
        try:
            choice = input("Enter choice [1/2]: ").strip()
        except EOFError:
            choice = "1"

        if choice == "2":
            custom_text = prompt_custom_scenario()
        else:
            # Show scenario menu
            console.print("\nAvailable scenarios:")
            for i, s in enumerate(SCENARIOS, 1):
                console.print(f"  [{i}] {s}")
            console.print(f"  [0] all")
            try:
                sel = input("Enter number or scenario name: ").strip()
            except EOFError:
                sel = "1"
            if sel == "0" or sel.lower() == "all":
                args.scenario = "all"
            elif sel.isdigit() and 1 <= int(sel) <= len(SCENARIOS):
                args.scenario = SCENARIOS[int(sel) - 1]
            elif sel in SCENARIOS:
                args.scenario = sel
            else:
                console.print(f"[yellow]Unknown selection '{sel}', defaulting to credential_discovery.[/yellow]")
                args.scenario = "credential_discovery"

    console.print(Panel(
        f"[bold green]Cowrie Honeypot Evaluator — Agentic Mode[/bold green]\n"
        f"Model      : {OLLAMA_MODEL}\n"
        f"Target     : {COWRIE_HOST}:{COWRIE_PORT}\n"
        f"Max steps  : {args.max_steps}\n"
        f"Mode       : {'custom scenario' if custom_text else args.scenario}",
        title="LLM Honeypot Evaluator v2"
    ))

    llm        = OllamaClient()
    report_gen = ReportGenerator()

    if custom_text:
        # ── Custom scenario path ──────────────────────────────────────────
        try:
            run_scenario(
                scenario_name="custom",
                llm=llm,
                report_gen=report_gen,
                max_steps=args.max_steps,
                custom_scenario_text=custom_text,
            )
        except Exception as e:
            console.print(f"[red]Error running custom scenario: {e}[/red]")
            import traceback
            traceback.print_exc()
    else:
        # ── Predefined scenario path ──────────────────────────────────────
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
