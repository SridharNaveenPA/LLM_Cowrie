# ─── Ollama (running on Windows host) ────────────────────────────────────────
OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_MODEL    = "llama3.1:8b"

# ─── Cowrie SSH Target (Kali VM) ─────────────────────────────────────────────
# Cowrie listens on port 2222, accepts ANY username/password
COWRIE_HOST     = "192.168.56.102"
COWRIE_PORT     = 2222
COWRIE_USER     = "root"       # any user works — Cowrie accepts all credentials
COWRIE_PASSWORD = "password"   # any password works

# ─── Real SSH into Kali (for log extraction) ─────────────────────────────────
KALI_HOST       = "192.168.56.102"
KALI_PORT       = 22
KALI_USER       = "rootuser"   # your actual Kali login (confirmed via whoami)
KALI_PASSWORD   = "user"       # ← UPDATE THIS to your actual sudo password

# ─── Cowrie Log Path (on Kali, owned by cowrie user) ─────────────────────────
COWRIE_LOG_PATH = "/home/cowrie/cowrie/var/log/cowrie/cowrie.json"
COWRIE_USER_ON_KALI = "cowrie" # the Linux user that owns cowrie's files

# ─── Cowrie clock offset ──────────────────────────────────────────────────────
# Cowrie logs timestamps in the system timezone of the Kali VM.
# We measure this once: Kali system clock says 16:21 UTC but Cowrie logs 12:21 UTC
# → Cowrie is in EDT (UTC-4) = -14400 seconds offset.
# Set to None to auto-detect from Kali's timezone at runtime.
COWRIE_TZ_OFFSET_SECONDS = None  # None = auto-detect, or set e.g. -14400

# ─── Custom Scenario ──────────────────────────────────────────────────────────
# Maximum number of characters the user may enter for a free-text custom scenario.
CUSTOM_SCENARIO_MAX_CHARS = 2000

# ─── Scenarios ────────────────────────────────────────────────────────────────
SCENARIOS = [
    "credential_discovery",
    "lateral_movement",
    "persistence",
    "privilege_escalation",
    "ransomware",
]

REPORTS_DIR   = "reports"
SCENARIOS_DIR = "attack_scenarios"
