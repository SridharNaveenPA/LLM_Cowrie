import json
import os
from datetime import datetime, timezone
from config import REPORTS_DIR


class ReportGenerator:
    def __init__(self):
        os.makedirs(REPORTS_DIR, exist_ok=True)

    # ── Agentic report (new) ──────────────────────────────────────────────────

    def generate_agentic(
        self,
        scenario: str,
        attack_history: list[dict],
        all_log_entries: list[dict],
        llm_analysis: dict,
        stopped_early: bool = False,
        custom_scenario_text: str | None = None,
    ) -> str:
        """
        Generate a Markdown report from an agentic attack run.

        attack_history items:
            {"step": int, "command": str, "output": str, "cowrie_logs": list, "reasoning": str}

        custom_scenario_text: When set (custom mode), the user's free-text scenario
            description is included verbatim in the report header.
        """
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H-%M-%S")
        filename  = f"{REPORTS_DIR}/{scenario}_{timestamp}.md"
        md = self._build_agentic_markdown(
            scenario, attack_history, all_log_entries,
            llm_analysis, stopped_early, timestamp,
            custom_scenario_text=custom_scenario_text,
        )
        with open(filename, "w", encoding="utf-8") as f:
            f.write(md)
        return filename

    # ── Legacy batch report (kept for backward compatibility) ─────────────────

    def generate(self, scenario, commands_executed, execution_results,
                 log_entries, llm_analysis) -> str:
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H-%M-%S")
        filename  = f"{REPORTS_DIR}/{scenario}_{timestamp}.md"
        md = self._build_markdown(
            scenario, commands_executed, execution_results,
            log_entries, llm_analysis, timestamp
        )
        with open(filename, "w", encoding="utf-8") as f:
            f.write(md)
        return filename

    # ── Shared helpers ────────────────────────────────────────────────────────

    def _grade_color(self, grade: str) -> str:
        return {"A": "🟢", "B": "🟡", "C": "🟠", "D": "🔴", "F": "⛔"}.get(grade, "⚪")

    def _score_bar(self, score) -> str:
        try:
            s = float(score)
        except (TypeError, ValueError):
            return "N/A"
        filled = round(s)
        bar = "█" * filled + "░" * (10 - filled)
        return f"`{bar}` {s:.1f}/10"

    def _severity_icon(self, sev: str) -> str:
        return {"HIGH": "🔴", "MEDIUM": "🟡", "LOW": "🟢"}.get(sev.upper(), "⚪")

    def _render_criterion(self, key: str, label: str, data: dict) -> str:
        if not data:
            return f"### {label}\n\n_No data available._\n\n"
        score    = data.get("score", "N/A")
        summary  = data.get("summary", "")
        findings = data.get("findings", [])
        md  = f"### {label}\n\n"
        md += f"**Score:** {self._score_bar(score)}\n\n"
        md += f"**Summary:** {summary}\n\n"
        if findings:
            for f in findings:
                sev  = f.get("severity", "LOW")
                icon = self._severity_icon(sev)
                md += f"#### {icon} [{sev}] {f.get('observation', '')}\n\n"
                md += f"- **Evidence:** `{f.get('evidence', 'N/A')}`\n"
                md += f"- **Recommendation:** {f.get('recommendation', '')}\n\n"
        else:
            md += "_No specific findings._\n\n"
        return md

    # ── Agentic report builder ────────────────────────────────────────────────

    def _build_agentic_markdown(
        self,
        scenario: str,
        attack_history: list[dict],
        all_log_entries: list[dict],
        analysis: dict,
        stopped_early: bool,
        timestamp: str,
        custom_scenario_text: str | None = None,
    ) -> str:

        # Handle raw_analysis fallback
        if "raw_analysis" in analysis and "evaluation" not in analysis:
            return self._build_agentic_fallback(
                scenario, attack_history, all_log_entries, analysis, stopped_early, timestamp,
                custom_scenario_text=custom_scenario_text,
            )

        eval_block       = analysis.get("evaluation", {})
        overall          = analysis.get("overall_assessment", "No assessment provided.")
        grade            = analysis.get("overall_grade", "N/A")
        ovr_score        = analysis.get("overall_score", "N/A")
        det_rate         = analysis.get("detection_rate", "N/A")
        top_vulns        = analysis.get("top_vulnerabilities", [])
        attacker_notice  = analysis.get("attacker_would_notice", [])
        immediate        = analysis.get("immediate_actions", [])
        total_ev         = analysis.get("total_events_logged", len(all_log_entries))
        cmds_count       = analysis.get("commands_executed", len(attack_history))
        grade_icon       = self._grade_color(grade)
        stop_reason      = "LLM stopped early (sufficient evidence gathered)" if stopped_early else "Reached maximum steps"

        # ── Header ────────────────────────────────────────────────────────────
        md = f"""# Cowrie Honeypot Evaluation Report — Agentic Mode

| | |
|---|---|
| **Scenario** | `{scenario}` |
| **Generated** | {timestamp} UTC |
| **Mode** | {'Custom (free-text)' if custom_scenario_text else 'Predefined'} Agentic Attack Loop |
| **Model** | Ollama LLM (llama3.1:8b) |
| **Overall Grade** | {grade_icon} **{grade}** ({ovr_score}/10) |
| **Detection Rate** | {det_rate} |
| **Events Captured** | {total_ev} |
| **Attack Steps** | {cmds_count} ({stop_reason}) |

"""
        # ── Custom scenario block ─────────────────────────────────────────────
        if custom_scenario_text:
            md += "## Custom Scenario Description\n\n"
            md += "> This evaluation was driven by a user-supplied attack scenario rather than a\n"
            md += "> predefined scenario file. The full scenario text is reproduced below.\n\n"
            md += "```\n"
            md += custom_scenario_text
            md += "\n```\n\n"
            md += "---\n\n"
        else:
            md += "---\n\n"

        # ── Executive Summary ─────────────────────────────────────────────────
        md += "## Executive Summary\n\n"
        md += f"{overall}\n\n"
        md += "---\n\n"

        # ── Evaluation Scorecard ──────────────────────────────────────────────
        md += "## Evaluation Scorecard\n\n"
        md += "| Criterion | Score | Summary |\n"
        md += "|-----------|-------|---------|\n"

        criteria = [
            ("realism",                "Realism"),
            ("emulation_accuracy",     "Emulation Accuracy"),
            ("data_quality",           "Data Quality & Telemetry"),
            ("containment_safety",     "Containment & Safety"),
            ("operational_complexity", "Operational Complexity"),
        ]
        for key, label in criteria:
            d       = eval_block.get(key, {})
            score   = d.get("score", "N/A")
            summary = d.get("summary", "")[:80]
            bar     = self._score_bar(score)
            md += f"| **{label}** | {bar} | {summary} |\n"

        md += f"\n**Overall Score: {ovr_score}/10 — Grade: {grade_icon} {grade}**\n\n---\n\n"

        # ── Detailed Criteria ─────────────────────────────────────────────────
        md += "## Detailed Evaluation\n\n"
        for key, label in criteria:
            md += self._render_criterion(key, label, eval_block.get(key, {}))
        md += "---\n\n"

        # ── Top Vulnerabilities ───────────────────────────────────────────────
        md += "## Top Vulnerabilities Identified\n\n"
        if top_vulns:
            for v in top_vulns:
                rank     = v.get("rank", "?")
                sev      = v.get("severity", "LOW")
                icon     = self._severity_icon(sev)
                title    = v.get("title", "Untitled")
                desc     = v.get("description", "")
                evid     = v.get("evidence", "N/A")
                cvss     = v.get("cvss_estimate", "N/A")
                rec      = v.get("recommendation", "")
                exposed  = v.get("exposed_by_command", "")

                md += f"### {rank}. {icon} [{sev}] {title}\n\n"
                md += f"**CVSS Estimate:** {cvss}\n\n"
                md += f"{desc}\n\n"
                md += f"**Evidence:** `{evid}`\n\n"
                if exposed:
                    md += f"**Exposed by command:** `{exposed}`\n\n"
                md += f"**Recommendation:** {rec}\n\n"
                md += "---\n\n"
        else:
            md += "_No specific vulnerabilities ranked._\n\n---\n\n"

        # ── Attacker Detection Signals ────────────────────────────────────────
        if attacker_notice:
            md += "## How an Attacker Would Detect This is a Honeypot\n\n"
            md += "> Observable tells that reveal Cowrie's artificial nature, discovered during the agentic attack.\n\n"
            for item in attacker_notice:
                md += f"- {item}\n"
            md += "\n---\n\n"

        # ── Immediate Actions ─────────────────────────────────────────────────
        if immediate:
            md += "## Immediate Remediation Actions\n\n"
            for i, action in enumerate(immediate, 1):
                md += f"{i}. {action}\n"
            md += "\n---\n\n"

        # ── Agentic Attack Trail ──────────────────────────────────────────────
        md += "## Agentic Attack Trail\n\n"
        md += (
            "> This section shows the LLM's decision trail: each command it chose, "
            "its reasoning, the honeypot's response, and how many Cowrie events were triggered.\n\n"
        )
        for entry in attack_history:
            step      = entry.get("step", "?")
            cmd       = entry.get("command", "")
            output    = entry.get("output", "")
            logs      = entry.get("cowrie_logs", [])
            reasoning = entry.get("reasoning", "")
            skipped   = "[SKIPPED" in output

            md += f"### Step {step}: `{cmd}`\n\n"
            if reasoning:
                md += f"**LLM Reasoning:** _{reasoning[:200]}_\n\n"
            if skipped:
                md += f"> ⚠️ Skipped — would terminate SSH session.\n\n"
            else:
                # Cowrie output
                output_display = output[:600].replace("```", "~~~")
                md += f"**Cowrie Response:**\n```\n{output_display}\n```\n\n"
                # Log summary
                log_event_ids = {}
                for le in logs:
                    eid = le.get("eventid", "unknown")
                    log_event_ids[eid] = log_event_ids.get(eid, 0) + 1
                if log_event_ids:
                    md += f"**Cowrie Log Events ({len(logs)} total):**\n"
                    for eid, count in log_event_ids.items():
                        md += f"- `{eid}` × {count}\n"
                    md += "\n"
                else:
                    md += "_No Cowrie log events captured for this step._\n\n"

        md += "---\n\n"

        # ── Full Cowrie Log Sample ────────────────────────────────────────────
        md += "## Full Session Cowrie Log Sample (first 20 events)\n\n```json\n"
        md += json.dumps(all_log_entries[:20], indent=2)
        md += "\n```\n\n"

        md += "---\n*Generated by LLM-based Cowrie Honeypot Evaluator — Agentic Mode*\n"
        return md

    def _build_agentic_fallback(
        self,
        scenario: str,
        attack_history: list[dict],
        all_log_entries: list[dict],
        analysis: dict,
        stopped_early: bool,
        timestamp: str,
        custom_scenario_text: str | None = None,
    ) -> str:
        """Fallback when LLM didn't return structured JSON for final report."""
        md  = f"# Cowrie Evaluation Report — {scenario} (Agentic Mode)\n\n"
        md += f"**Generated:** {timestamp} UTC\n\n"
        if custom_scenario_text:
            md += "## Custom Scenario Description\n\n"
            md += "> User-supplied scenario text:\n\n"
            md += f"```\n{custom_scenario_text}\n```\n\n---\n\n"
        md += "## LLM Analysis\n\n"
        md += "> Note: LLM returned unstructured output. Raw analysis below.\n\n"
        md += analysis.get("raw_analysis", "_No analysis_")
        md += "\n\n---\n\n## Agentic Attack Trail\n\n"
        for entry in attack_history:
            step = entry.get("step", "?")
            cmd  = entry.get("command", "")
            out  = entry.get("output", "")[:300]
            md  += f"**Step {step}:** `{cmd}`\n\n```\n{out}\n```\n\n"
        md += "---\n\n## Log Events Captured\n\n```json\n"
        md += json.dumps(all_log_entries[:20], indent=2)
        md += "\n```\n"
        return md

    # ── Legacy batch report builder (unchanged) ───────────────────────────────

    def _build_markdown(self, scenario, commands, exec_results,
                        logs, analysis, timestamp) -> str:

        if "raw_analysis" in analysis and "evaluation" not in analysis:
            return self._build_fallback_report(
                scenario, commands, exec_results, logs, analysis, timestamp
            )

        eval_block      = analysis.get("evaluation", {})
        overall         = analysis.get("overall_assessment", "No assessment provided.")
        grade           = analysis.get("overall_grade", "N/A")
        ovr_score       = analysis.get("overall_score", "N/A")
        det_rate        = analysis.get("detection_rate", "N/A")
        top_vulns       = analysis.get("top_vulnerabilities", [])
        attacker_notice = analysis.get("attacker_would_notice", [])
        immediate       = analysis.get("immediate_actions", [])
        missed_cmds     = analysis.get("commands_missed", [])
        total_ev        = analysis.get("total_events_logged", len(logs))
        cmds_logged     = analysis.get("commands_logged", "N/A")
        grade_icon      = self._grade_color(grade)

        md = f"""# Cowrie Honeypot Evaluation Report

| | |
|---|---|
| **Scenario** | `{scenario}` |
| **Generated** | {timestamp} UTC |
| **Model** | Ollama LLM (llama3.1:8b) |
| **Overall Grade** | {grade_icon} **{grade}** ({ovr_score}/10) |
| **Detection Rate** | {det_rate} |
| **Events Captured** | {total_ev} |
| **Commands Executed** | {len(commands)} |
| **Commands Logged** | {cmds_logged} |

---

## Executive Summary

{overall}

---

## Evaluation Scorecard

| Criterion | Score | Summary |
|-----------|-------|---------|
"""
        criteria = [
            ("realism",               "Realism"),
            ("emulation_accuracy",    "Emulation Accuracy"),
            ("data_quality",          "Data Quality & Telemetry"),
            ("containment_safety",    "Containment & Safety"),
            ("operational_complexity","Operational Complexity"),
        ]
        for key, label in criteria:
            d = eval_block.get(key, {})
            score   = d.get("score", "N/A")
            summary = d.get("summary", "")[:80]
            bar     = self._score_bar(score)
            md += f"| **{label}** | {bar} | {summary} |\n"

        md += f"\n**Overall Score: {ovr_score}/10 — Grade: {grade_icon} {grade}**\n\n---\n\n"

        md += "## Detailed Evaluation\n\n"
        for key, label in criteria:
            md += self._render_criterion(key, label, eval_block.get(key, {}))
        md += "---\n\n"

        md += "## Top Vulnerabilities\n\n"
        if top_vulns:
            for v in top_vulns:
                rank  = v.get("rank", "?")
                sev   = v.get("severity", "LOW")
                icon  = self._severity_icon(sev)
                title = v.get("title", "Untitled")
                desc  = v.get("description", "")
                evid  = v.get("evidence", "N/A")
                cvss  = v.get("cvss_estimate", "N/A")
                rec   = v.get("recommendation", "")
                md += f"### {rank}. {icon} [{sev}] {title}\n\n"
                md += f"**CVSS Estimate:** {cvss}\n\n"
                md += f"{desc}\n\n"
                md += f"**Evidence:** `{evid}`\n\n"
                md += f"**Recommendation:** {rec}\n\n"
                md += "---\n\n"
        else:
            md += "_No specific vulnerabilities ranked._\n\n---\n\n"

        if attacker_notice:
            md += "## How an Attacker Would Detect This is a Honeypot\n\n"
            md += "> These are the behavioral tells that reveal Cowrie's artificial nature.\n\n"
            for item in attacker_notice:
                md += f"- {item}\n"
            md += "\n---\n\n"

        if missed_cmds:
            md += "## Commands Not Properly Captured\n\n"
            for c in missed_cmds:
                md += f"- `{c}`\n"
            md += "\n---\n\n"

        if immediate:
            md += "## Immediate Remediation Actions\n\n"
            for i, action in enumerate(immediate, 1):
                md += f"{i}. {action}\n"
            md += "\n---\n\n"

        md += "## Attack Commands Executed\n\n```bash\n"
        for cmd in commands:
            md += f"{cmd}\n"
        md += "```\n\n"

        md += "### Command Execution Results\n\n"
        md += "| # | Command | Response (truncated) |\n"
        md += "|---|---------|----------------------|\n"
        for i, r in enumerate(exec_results, 1):
            cmd = r.get("command", "")[:50].replace("|", "\\|")
            out = r.get("output", "")[:80].replace("\n", " ").replace("|", "\\|")
            md += f"| {i} | `{cmd}` | {out} |\n"
        md += "\n---\n\n"

        md += "## Cowrie Log Sample (first 20 events)\n\n```json\n"
        md += json.dumps(logs[:20], indent=2)
        md += "\n```\n\n"

        md += "---\n*Generated by LLM-based Cowrie Honeypot Evaluator*\n"
        return md

    def _build_fallback_report(self, scenario, commands, exec_results,
                                logs, analysis, timestamp) -> str:
        md  = f"# Cowrie Evaluation Report — {scenario}\n\n"
        md += f"**Generated:** {timestamp} UTC\n\n"
        md += "## LLM Analysis\n\n"
        md += "> Note: LLM returned unstructured output. Raw analysis below.\n\n"
        md += analysis.get("raw_analysis", "_No analysis_")
        md += "\n\n---\n\n## Commands Executed\n\n```bash\n"
        for cmd in commands:
            md += f"{cmd}\n"
        md += "```\n\n"
        md += "## Log Events Captured\n\n```json\n"
        md += json.dumps(logs[:20], indent=2)
        md += "\n```\n"
        return md
