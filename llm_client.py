import sys
import time
import requests
import json
from config import OLLAMA_BASE_URL, OLLAMA_MODEL

# Force UTF-8 output on Windows to avoid cp1252 encoding errors
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


class OllamaClient:
    def __init__(self, base_url: str = OLLAMA_BASE_URL, model: str = OLLAMA_MODEL):
        self.base_url = base_url.rstrip("/")
        self.model = model

    def _chat(self, messages: list[dict], temperature: float = 0.3, retries: int = 3) -> str:
        """Send a chat request to Ollama. Retries on 500/timeout with backoff."""
        url = f"{self.base_url}/api/chat"
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False,
            "options": {"temperature": temperature, "num_ctx": 8192},
        }
        last_error = None
        for attempt in range(1, retries + 1):
            try:
                response = requests.post(url, json=payload, timeout=600)
                if response.status_code == 500:
                    print(f"  [warn] Ollama 500 (attempt {attempt}/{retries}): {response.text[:200]}")
                    if attempt < retries:
                        time.sleep(attempt * 5)
                        continue
                response.raise_for_status()
                return response.json()["message"]["content"]
            except requests.exceptions.ConnectionError as e:
                last_error = e
                print(f"  [warn] Cannot reach Ollama (attempt {attempt}/{retries}): {e}")
                if attempt < retries:
                    time.sleep(5)
            except requests.exceptions.Timeout:
                last_error = Exception("Timed out after 600s")
                print(f"  [warn] Ollama timeout (attempt {attempt}/{retries})")
                if attempt < retries:
                    time.sleep(5)
            except requests.exceptions.HTTPError as e:
                raise
        raise RuntimeError(
            f"Ollama failed after {retries} attempts: {last_error}\n"
            f"Ensure 'ollama serve' is running and model '{self.model}' is pulled."
        )

    # ── Agentic: decide the NEXT single command ───────────────────────────────

    def generate_next_command(
        self,
        scenario: str,
        scenario_description: str,
        attack_history: list[dict],
        max_steps: int = 20,
    ) -> dict:
        """
        Given the history of commands executed so far and their outputs, decide
        the single best next command to run — or signal that the attack is done.

        Each item in attack_history is:
            {"step": int, "command": str, "output": str, "cowrie_logs": list[dict]}

        Returns:
            {
                "command":    str | None,   # shell command to run, or None if done
                "done":       bool,         # True = LLM decided to stop
                "reasoning":  str,          # why this command was chosen
            }
        """
        steps_done = len(attack_history)

        # Build a compact history string so we don't blow the context window.
        # Show the last 10 steps in full; summarise older ones.
        history_lines = []
        for entry in attack_history[-10:]:
            cmd    = entry.get("command", "")
            output = entry.get("output", "")[:500]   # cap per-command output
            logs   = entry.get("cowrie_logs", [])
            log_summary = f"{len(logs)} log events"
            history_lines.append(
                f"Step {entry['step']}: $ {cmd}\n"
                f"  Output: {output!r}\n"
                f"  Cowrie: {log_summary}"
            )
        history_text = "\n\n".join(history_lines) if history_lines else "(no commands run yet)"

        system_prompt = (
            "You are a red team operator performing a controlled attack on a Cowrie SSH honeypot "
            "for security evaluation purposes. "
            "Your goal is to systematically probe the honeypot and expose its weaknesses "
            f"following the '{scenario}' attack scenario. "
            "Based on what you have learned from each command's output, choose the SINGLE most "
            "valuable next command to run. "
            "If you have gathered enough evidence to write a full vulnerability report, output DONE instead.\n\n"
            "Rules:\n"
            "1. Output ONLY valid JSON — no markdown, no prose outside the JSON.\n"
            "2. If continuing: {\"done\": false, \"command\": \"<single shell command>\", \"reasoning\": \"<why>\"}\n"
            "3. If finished:   {\"done\": true,  \"command\": null,                      \"reasoning\": \"<summary of findings>\"}\n"
            "4. Prefer commands that probe realism: version mismatches, empty responses, fake filesystem.\n"
            "5. Do NOT repeat a command already in the history unless probing a variation.\n"
            f"6. You may run at most {max_steps} steps total. You have used {steps_done} so far.\n"
            "7. NEVER generate a command that starts with or contains 'ssh', 'scp', or 'sftp'. "
            "   These open a nested SSH session inside Cowrie and crash the evaluator. "
            "   Use alternatives like 'nc', 'curl', 'wget', 'nmap', or direct file reads instead."
        )

        user_prompt = (
            f"Scenario: {scenario}\n"
            f"Description: {scenario_description}\n\n"
            f"Attack history ({steps_done} steps so far):\n"
            f"{history_text}\n\n"
            f"Steps remaining: {max_steps - steps_done}\n\n"
            "What is the single best next command? "
            "If the history already exposes enough vulnerabilities, output DONE."
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_prompt},
        ]

        raw = self._chat(messages, temperature=0.4)

        # Robust JSON extraction
        cleaned = raw.strip()
        if "```" in cleaned:
            for part in cleaned.split("```"):
                part = part.strip()
                if part.startswith("json"):
                    part = part[4:].strip()
                if part.startswith("{"):
                    try:
                        return json.loads(part)
                    except Exception:
                        continue
        # Try direct parse
        for attempt in [cleaned, cleaned[cleaned.find("{"):cleaned.rfind("}") + 1]]:
            try:
                result = json.loads(attempt)
                if isinstance(result, dict) and "done" in result:
                    return result
            except (json.JSONDecodeError, ValueError):
                continue

        # Heuristic fallback: if the model said "DONE" in plain text
        if "done" in cleaned.lower() and "true" in cleaned.lower():
            return {"done": True, "command": None, "reasoning": cleaned}

        print(f"  [warn] Could not parse next-command JSON — raw: {cleaned[:200]}")
        return {"done": True, "command": None, "reasoning": f"Parse error — raw: {cleaned[:300]}"}

    # ── Agentic: generate final vulnerability report ──────────────────────────

    def generate_final_report(
        self,
        scenario: str,
        attack_history: list[dict],
        cowrie_context: dict = None,
    ) -> dict:
        """
        After all agentic steps are done, produce a structured vulnerability report
        from the full attack history (commands, their outputs, and Cowrie logs).

        Returns the same JSON structure as analyze_logs() for compatibility
        with ReportGenerator.
        """
        # Summarise history for the prompt
        history_entries = []
        all_cowrie_logs = []
        for entry in attack_history:
            cmd    = entry.get("command", "")
            output = entry.get("output", "")[:400]
            logs   = entry.get("cowrie_logs", [])
            reasoning = entry.get("reasoning", "")
            all_cowrie_logs.extend(logs)
            history_entries.append({
                "step":      entry["step"],
                "command":   cmd,
                "output":    output,
                "reasoning": reasoning,
                "log_count": len(logs),
            })

        # Derive evidence from Cowrie logs (same as analyze_logs)
        commands_run = [
            e.get("input", "") for e in all_cowrie_logs
            if e.get("eventid") == "cowrie.command.input" and e.get("input")
        ]
        event_counts: dict[str, int] = {}
        for e in all_cowrie_logs:
            eid = e.get("eventid", "unknown")
            event_counts[eid] = event_counts.get(eid, 0) + 1

        evidence = {
            "scenario":               scenario,
            "total_cowrie_events":    len(all_cowrie_logs),
            "event_type_counts":      event_counts,
            "commands_logged_cowrie": commands_run[:40],
            "total_attack_steps":     len(attack_history),
            "attack_history_summary": history_entries,
        }

        prompt_chars = len(json.dumps(evidence)) + 2000
        print(f"  Final report prompt: ~{prompt_chars} chars (~{prompt_chars // 4} tokens)")

        system_prompt = (
            "You are a senior honeypot security researcher. "
            "You have just completed a fully agentic, step-by-step attack on a Cowrie SSH honeypot. "
            "Each step shows the command you ran, the output the honeypot returned, "
            "and how many Cowrie log events it generated. "
            "Your task is to synthesise all evidence into a structured vulnerability report. "
            "Base every finding ONLY on the evidence provided — not on general Cowrie knowledge. "
            "Respond with valid JSON only. No markdown, no text outside the JSON."
        )

        user_prompt = (
            f'Write a honeypot vulnerability report for the "{scenario}" scenario.\n\n'
            f"FULL ATTACK EVIDENCE:\n{json.dumps(evidence, indent=2)}\n\n"
            "Score each criterion 1-10 based on the observed attack results.\n"
            "Highlight exactly which commands revealed weaknesses and what output exposed them.\n\n"
            "Return ONLY valid JSON in this structure:\n"
            "{\n"
            f'  "scenario": "{scenario}",\n'
            f'  "total_events_logged": {len(all_cowrie_logs)},\n'
            f'  "commands_executed": {len(attack_history)},\n'
            '  "detection_rate": "<percent of attacker steps that generated Cowrie log events>",\n'
            '  "evaluation": {\n'
            '    "realism":                {"score": 0, "summary": "", "findings": [{"severity": "HIGH|MEDIUM|LOW", "observation": "", "evidence": "", "recommendation": ""}]},\n'
            '    "emulation_accuracy":     {"score": 0, "summary": "", "findings": [{"severity": "HIGH", "observation": "", "evidence": "", "recommendation": ""}]},\n'
            '    "data_quality":           {"score": 0, "summary": "", "findings": [{"severity": "MEDIUM", "observation": "", "evidence": "", "recommendation": ""}]},\n'
            '    "containment_safety":     {"score": 0, "summary": "", "findings": [{"severity": "MEDIUM", "observation": "", "evidence": "", "recommendation": ""}]},\n'
            '    "operational_complexity": {"score": 0, "summary": "", "findings": [{"severity": "LOW", "observation": "", "evidence": "", "recommendation": ""}]}\n'
            '  },\n'
            '  "overall_score": 0.0,\n'
            '  "overall_grade": "A|B|C|D|F",\n'
            '  "top_vulnerabilities": [\n'
            '    {"rank": 1, "severity": "HIGH|MEDIUM|LOW", "title": "", "description": "", "evidence": "", "cvss_estimate": "Critical|High|Medium|Low", "recommendation": "", "exposed_by_command": "<the command that revealed this>"}\n'
            '  ],\n'
            '  "attacker_would_notice": ["<observable tell from command outputs>"],\n'
            '  "overall_assessment": "<2-3 sentences summarising key findings with command evidence>",\n'
            '  "immediate_actions": ["<specific actionable fix>"]\n'
            "}"
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_prompt},
        ]
        raw = self._chat(messages, temperature=0.2)

        # Robust JSON extraction (same pattern as analyze_logs)
        cleaned = raw.strip()
        if "```" in cleaned:
            for part in cleaned.split("```"):
                part = part.strip()
                if part.startswith("json"):
                    part = part[4:].strip()
                if part.startswith("{"):
                    try:
                        return json.loads(part)
                    except Exception:
                        continue
        if cleaned.startswith("{"):
            try:
                return json.loads(cleaned)
            except json.JSONDecodeError:
                pass
        start = cleaned.find("{")
        end   = cleaned.rfind("}")
        if start != -1 and end != -1:
            try:
                return json.loads(cleaned[start:end + 1])
            except json.JSONDecodeError as e:
                print(f"  [warn] JSON parse failed: {e}")

        print("  [warn] Could not parse final report JSON — storing raw")
        return {
            "scenario":          scenario,
            "raw_analysis":      raw,
            "parse_error":       "Could not extract JSON",
            "total_events_logged": len(all_cowrie_logs),
        }

    # ── Custom scenario: generate initial attack commands from free-text ─────────

    def generate_commands_from_custom_scenario(self, scenario_text: str) -> list[str]:
        """
        Given a free-text scenario description (up to 2000 chars), generate a list
        of realistic shell commands an attacker would run on a Cowrie SSH honeypot.

        Returns a flat list of command strings (at most 15), ordered logically.
        Falls back to an empty list if parsing fails.
        """
        system_prompt = (
            "You are a red team operator simulating an attack on a Cowrie SSH Linux honeypot "
            "for controlled security evaluation. "
            "Given a free-text attack scenario description, produce a realistic, ordered list "
            "of shell commands that would be used to carry out that scenario on a Linux target. "
            "Output ONLY a valid JSON array of shell command strings — no markdown, no explanation. "
            'Example: ["whoami", "id", "uname -a"]'
        )
        user_prompt = (
            f"Attack scenario description:\n{scenario_text}\n\n"
            "Generate up to 15 realistic Linux shell commands for this scenario, "
            "ordered from initial reconnaissance to the final objective. "
            "Prefer commands that expose Cowrie honeypot weaknesses (fake filesystem, "
            "version mismatches, empty responses). "
            "IMPORTANT: Do NOT include any command that starts with or contains 'ssh', 'scp', "
            "or 'sftp' — these crash the evaluator by opening a nested SSH session. "
            "Use alternatives like 'nc', 'curl', 'wget', 'nmap', or direct file reads instead. "
            "Return a single flat JSON array of command strings only."
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_prompt},
        ]
        raw = self._chat(messages, temperature=0.4)

        try:
            cleaned = raw.strip()
            if "```" in cleaned:
                for part in cleaned.split("```"):
                    part = part.strip()
                    if part.startswith("json"):
                        part = part[4:].strip()
                    if part.startswith("["):
                        try:
                            commands = json.loads(part)
                            if isinstance(commands, list):
                                return [c for c in commands if isinstance(c, str) and c.strip()]
                        except Exception:
                            continue
            # Direct parse
            if cleaned.startswith("["):
                commands = json.loads(cleaned)
                if isinstance(commands, list):
                    return [c for c in commands if isinstance(c, str) and c.strip()]
            # Slice out array
            start = cleaned.find("[")
            end   = cleaned.rfind("]")
            if start != -1 and end != -1:
                commands = json.loads(cleaned[start:end + 1])
                if isinstance(commands, list):
                    return [c for c in commands if isinstance(c, str) and c.strip()]
        except json.JSONDecodeError:
            pass

        print("  [warn] Could not parse custom scenario commands — LLM returned: "
              + raw[:200])
        return []

    # ── Legacy: batch command generation (kept for backward compatibility) ────

    def generate_attack_commands(self, scenario: str, scenario_data: dict) -> list[str]:
        """Extract and augment attack commands from scenario JSON using LLM (batch mode)."""
        base_commands = [
            cmd_data.get("command")
            for phase in scenario_data.get("phases", [])
            for cmd_data in phase.get("commands", [])
            if isinstance(cmd_data, dict) and cmd_data.get("command")
        ]
        description = scenario_data.get("description", "")

        system_prompt = (
            "You are a red team expert simulating attacker behavior on a Linux SSH honeypot. "
            "Output ONLY a valid JSON array of shell command strings. No markdown, no explanation."
        )
        user_prompt = (
            f"Scenario: {scenario}\nDescription: {description}\n\n"
            f"Base commands:\n{json.dumps(base_commands, indent=2)}\n\n"
            "Add up to 10 additional realistic commands. Keep ALL originals. "
            'Return a single flat JSON array. Example: ["cmd1", "cmd2"]'
        )
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_prompt},
        ]
        raw = self._chat(messages, temperature=0.4)
        try:
            cleaned = raw.strip()
            if "```" in cleaned:
                parts = cleaned.split("```")
                if len(parts) >= 2:
                    cleaned = parts[1].strip()
                    if cleaned.startswith("json"):
                        cleaned = cleaned[4:].strip()
            commands = json.loads(cleaned)
            if isinstance(commands, list):
                return [c for c in commands if isinstance(c, str) and c.strip()]
        except json.JSONDecodeError:
            pass
        print("  [warn] LLM returned unparseable JSON — using base commands only.")
        return base_commands

    # ── Legacy: batch log analysis (kept for backward compatibility) ──────────

    def analyze_logs(self, scenario: str, logs: list[dict], cowrie_context: dict = None) -> dict:
        """
        Evaluate Cowrie honeypot based on logged events (batch mode).
        All findings must be derived from actual log data.
        """
        commands_run = [
            e.get("input", "") for e in logs
            if e.get("eventid") == "cowrie.command.input" and e.get("input")
        ]
        event_counts: dict[str, int] = {}
        for e in logs:
            eid = e.get("eventid", "unknown")
            event_counts[eid] = event_counts.get(eid, 0) + 1

        versions_negotiated = list({e.get("version", "") for e in logs if e.get("version")})
        src_ips             = list({e.get("src_ip", "")  for e in logs if e.get("src_ip")})
        session_ids         = list({e.get("session", "") for e in logs if e.get("session")})
        login_events        = [e for e in logs if "login" in e.get("eventid", "")]
        system_messages     = [
            e.get("message", "") for e in logs
            if e.get("message") and not e.get("input")
        ][:10]

        evidence = {
            "scenario": scenario,
            "total_events": len(logs),
            "event_type_counts": event_counts,
            "unique_sessions": len(session_ids),
            "source_ips": src_ips,
            "ssh_versions_negotiated": versions_negotiated,
            "login_attempts": len(login_events),
            "commands_executed": commands_run[:40],
            "system_messages": system_messages,
        }

        prompt_chars_estimate = len(json.dumps(evidence)) + 1200
        print(f"  Prompt size: ~{prompt_chars_estimate} chars (~{prompt_chars_estimate//4} tokens)")

        system_prompt = (
            "You are a honeypot security researcher evaluating a Cowrie SSH honeypot. "
            "You MUST base every finding ONLY on the log evidence provided — "
            "do not rely on general knowledge about Cowrie defaults. "
            "If you cannot find evidence for something in the logs, say so explicitly. "
            "Respond with valid JSON only. No markdown, no text outside the JSON."
        )

        user_prompt = (
            f'Evaluate this Cowrie SSH honeypot session from the "{scenario}" scenario.\n\n'
            f"LOG EVIDENCE:\n{json.dumps(evidence, indent=2)}\n\n"
            "Score each criterion 1-10 based ONLY on what the log evidence reveals.\n"
            "Cite exact field values from the logs as evidence for each finding.\n"
            "Be specific: reference actual command names, event IDs, IP addresses, and messages.\n\n"
            "Return ONLY valid JSON in this exact structure:\n"
            "{\n"
            f'  "scenario": "{scenario}",\n'
            f'  "total_events_logged": {len(logs)},\n'
            f'  "commands_executed": {len(commands_run)},\n'
            '  "detection_rate": "<percent>",\n'
            '  "evaluation": {\n'
            '    "realism":                {"score": 0, "summary": "", "findings": [{"severity": "HIGH|MEDIUM|LOW", "observation": "", "evidence": "", "recommendation": ""}]},\n'
            '    "emulation_accuracy":     {"score": 0, "summary": "", "findings": [{"severity": "HIGH", "observation": "", "evidence": "", "recommendation": ""}]},\n'
            '    "data_quality":           {"score": 0, "summary": "", "findings": [{"severity": "MEDIUM", "observation": "", "evidence": "", "recommendation": ""}]},\n'
            '    "containment_safety":     {"score": 0, "summary": "", "findings": [{"severity": "MEDIUM", "observation": "", "evidence": "", "recommendation": ""}]},\n'
            '    "operational_complexity": {"score": 0, "summary": "", "findings": [{"severity": "LOW", "observation": "", "evidence": "", "recommendation": ""}]}\n'
            '  },\n'
            '  "overall_score": 0.0,\n'
            '  "overall_grade": "A|B|C|D|F",\n'
            '  "top_vulnerabilities": [\n'
            '    {"rank": 1, "severity": "HIGH|MEDIUM|LOW", "title": "", "description": "", "evidence": "", "cvss_estimate": "Critical|High|Medium|Low", "recommendation": ""}\n'
            '  ],\n'
            '  "attacker_would_notice": ["<observable tell>"],\n'
            '  "overall_assessment": "<2-3 sentences>",\n'
            '  "immediate_actions": ["<actionable fix>"]\n'
            "}"
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_prompt},
        ]
        raw = self._chat(messages, temperature=0.2)

        cleaned = raw.strip()
        if "```" in cleaned:
            for part in cleaned.split("```"):
                part = part.strip()
                if part.startswith("json"):
                    part = part[4:].strip()
                if part.startswith("{"):
                    try:
                        return json.loads(part)
                    except Exception:
                        continue
        if cleaned.startswith("{"):
            try:
                return json.loads(cleaned)
            except json.JSONDecodeError:
                pass
        start = cleaned.find("{")
        end   = cleaned.rfind("}")
        if start != -1 and end != -1:
            try:
                return json.loads(cleaned[start:end + 1])
            except json.JSONDecodeError as e:
                print(f"  [warn] JSON parse failed: {e}")

        print("  [warn] Could not parse LLM output as JSON — storing raw")
        return {
            "scenario": scenario,
            "raw_analysis": raw,
            "parse_error": "Could not extract JSON",
            "total_events_logged": len(logs),
        }
