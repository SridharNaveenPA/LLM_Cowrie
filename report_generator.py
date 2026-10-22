import json
import os
from datetime import datetime, timezone
from config import REPORTS_DIR


class ReportGenerator:
    def __init__(self):
        os.makedirs(REPORTS_DIR, exist_ok=True)

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

    # ── helpers ───────────────────────────────────────────────────────────────

    def _grade_color(self, grade: str) -> str:
        return {"A": "🟢", "B": "🟡", "C": "🟠", "D": "🔴", "F": "⛔"}.get(grade, "⚪")

    def _score_bar(self, score) -> str:
        """Convert 1-10 score to a visual bar."""
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

        score   = data.get("score", "N/A")
        summary = data.get("summary", "")
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

    # ── main builder ──────────────────────────────────────────────────────────

    def _build_markdown(self, scenario, commands, exec_results,
                        logs, analysis, timestamp) -> str:

        # Handle raw_analysis fallback (LLM returned non-JSON)
        if "raw_analysis" in analysis and "evaluation" not in analysis:
            return self._build_fallback_report(
                scenario, commands, exec_results, logs, analysis, timestamp
            )

        eval_block  = analysis.get("evaluation", {})
        overall     = analysis.get("overall_assessment", "No assessment provided.")
        grade       = analysis.get("overall_grade", "N/A")
        ovr_score   = analysis.get("overall_score", "N/A")
        det_rate    = analysis.get("detection_rate", "N/A")
        top_vulns   = analysis.get("top_vulnerabilities", [])
        attacker_notice = analysis.get("attacker_would_notice", [])
        immediate   = analysis.get("immediate_actions", [])
        missed_cmds = analysis.get("commands_missed", [])
        total_ev    = analysis.get("total_events_logged", len(logs))
        cmds_logged = analysis.get("commands_logged", "N/A")

        grade_icon  = self._grade_color(grade)

        # ── Header ────────────────────────────────────────────────────────────
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

        # ── Detailed Criteria ─────────────────────────────────────────────────
        md += "## Detailed Evaluation\n\n"
        for key, label in criteria:
            md += self._render_criterion(key, label, eval_block.get(key, {}))

        md += "---\n\n"

        # ── Top Vulnerabilities ───────────────────────────────────────────────
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

        # ── Attacker Detection Signals ────────────────────────────────────────
        if attacker_notice:
            md += "## How an Attacker Would Detect This is a Honeypot\n\n"
            md += "> These are the behavioral tells that reveal Cowrie's artificial nature.\n\n"
            for item in attacker_notice:
                md += f"- {item}\n"
            md += "\n---\n\n"

        # ── Commands Not Logged ───────────────────────────────────────────────
        if missed_cmds:
            md += "## Commands Not Properly Captured\n\n"
            for c in missed_cmds:
                md += f"- `{c}`\n"
            md += "\n---\n\n"

        # ── Immediate Actions ─────────────────────────────────────────────────
        if immediate:
            md += "## Immediate Remediation Actions\n\n"
            for i, action in enumerate(immediate, 1):
                md += f"{i}. {action}\n"
            md += "\n---\n\n"

        # ── Commands Executed ─────────────────────────────────────────────────
        md += "## Attack Commands Executed\n\n```bash\n"
        for cmd in commands:
            md += f"{cmd}\n"
        md += "```\n\n"

        # ── Execution Results Table ───────────────────────────────────────────
        md += "### Command Execution Results\n\n"
        md += "| # | Command | Response (truncated) |\n"
        md += "|---|---------|----------------------|\n"
        for i, r in enumerate(exec_results, 1):
            cmd = r.get("command", "")[:50].replace("|", "\\|")
            out = r.get("output", "")[:80].replace("\n", " ").replace("|", "\\|")
            md += f"| {i} | `{cmd}` | {out} |\n"
        md += "\n---\n\n"

        # ── Raw Log Sample ────────────────────────────────────────────────────
        md += "## Cowrie Log Sample (first 20 events)\n\n```json\n"
        md += json.dumps(logs[:20], indent=2)
        md += "\n```\n\n"

        md += "---\n*Generated by LLM-based Cowrie Honeypot Evaluator*\n"
        return md

    def _build_fallback_report(self, scenario, commands, exec_results,
                                logs, analysis, timestamp) -> str:
        """Fallback when LLM didn't return structured JSON."""
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
