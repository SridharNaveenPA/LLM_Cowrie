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

    # ── Command generation ────────────────────────────────────────────────────

    def generate_attack_commands(self, scenario: str, scenario_data: dict) -> list[str]:
        """Extract and augment attack commands from scenario JSON using LLM."""
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

    # ── Log analysis ──────────────────────────────────────────────────────────

    def analyze_logs(self, scenario: str, logs: list[dict], cowrie_context: dict = None) -> dict:
        """
        Evaluate Cowrie honeypot based purely on observed log evidence.
        cowrie_context is intentionally NOT passed to the LLM — all findings
        must be derived from actual log data, not pre-supplied knowledge.
        """
        # ── Build evidence from actual log data ───────────────────────────────
        commands_run = [
            e.get("input", "") for e in logs
            if e.get("eventid") == "cowrie.command.input" and e.get("input")
        ]
        event_counts = {}
        for e in logs:
            eid = e.get("eventid", "unknown")
            event_counts[eid] = event_counts.get(eid, 0) + 1

        # Session-level facts observable from logs
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
            "Be specific: reference actual command names, event IDs, IP addresses, and messages from the data.\n\n"
            "Return ONLY valid JSON in this exact structure:\n"
            "{\n"
            f'  "scenario": "{scenario}",\n'
            f'  "total_events_logged": {len(logs)},\n'
            f'  "commands_executed": {len(commands_run)},\n'
            '  "detection_rate": "<percent of attacker actions that generated log entries>",\n'
            '  "evaluation": {\n'
            '    "realism":                {"score": 0, "summary": "<one sentence from log evidence>", "findings": [{"severity": "HIGH|MEDIUM|LOW", "observation": "<what the log shows>", "evidence": "<exact log field/value>", "recommendation": "<specific fix>"}]},\n'
            '    "emulation_accuracy":     {"score": 0, "summary": "<one sentence>", "findings": [{"severity": "HIGH", "observation": "", "evidence": "", "recommendation": ""}]},\n'
            '    "data_quality":           {"score": 0, "summary": "<one sentence>", "findings": [{"severity": "MEDIUM", "observation": "", "evidence": "", "recommendation": ""}]},\n'
            '    "containment_safety":     {"score": 0, "summary": "<one sentence>", "findings": [{"severity": "MEDIUM", "observation": "", "evidence": "", "recommendation": ""}]},\n'
            '    "operational_complexity": {"score": 0, "summary": "<one sentence>", "findings": [{"severity": "LOW", "observation": "", "evidence": "", "recommendation": ""}]}\n'
            '  },\n'
            '  "overall_score": 0.0,\n'
            '  "overall_grade": "A|B|C|D|F",\n'
            '  "top_vulnerabilities": [\n'
            '    {"rank": 1, "severity": "HIGH|MEDIUM|LOW", "title": "", "description": "", "evidence": "<from logs>", "cvss_estimate": "Critical|High|Medium|Low", "recommendation": ""}\n'
            '  ],\n'
            '  "attacker_would_notice": ["<observable tell from the log data>"],\n'
            '  "overall_assessment": "<2-3 sentences citing specific log evidence>",\n'
            '  "immediate_actions": ["<specific actionable fix>"]\n'
            "}"
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_prompt},
        ]
        raw = self._chat(messages, temperature=0.2)

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
