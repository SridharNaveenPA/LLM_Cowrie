"""
log_extractor.py

Clock offset strategy (reliable):
  Cowrie writes log timestamps using the Kali VM's local timezone.
  We detect the offset by asking Kali: "what is your UTC offset in seconds?"
  using `date +%z` which returns e.g. -0400 for EDT.
  This is independent of when the last log entry was written.
"""
import json
from datetime import datetime, timezone, timedelta
from ssh_executor import KaliSSHClient
from config import COWRIE_LOG_PATH, COWRIE_TZ_OFFSET_SECONDS


class CowrieLogExtractor:
    def __init__(self, kali_client: KaliSSHClient):
        self.kali = kali_client
        self._last_offset = 0.0
        self._offset_detected = False

    # ── clock helpers ─────────────────────────────────────────────────────────

    def get_kali_utc_time(self) -> datetime:
        """Read UTC time directly from Kali using epoch seconds."""
        stdout, _ = self.kali.run("date -u +%s", timeout=10)
        try:
            return datetime.fromtimestamp(int(stdout.strip()), tz=timezone.utc)
        except (ValueError, TypeError):
            return datetime.now(timezone.utc)

    def detect_clock_offset(self) -> float:
        """
        Detect Cowrie's clock offset by reading Kali's actual timezone offset.

        Strategy: `date +%z` returns the local timezone as +HHMM or -HHMM.
        e.g. -0400 means UTC-4 (EDT) = -14400 seconds.
        Cowrie writes log timestamps in this timezone.
        So offset = local_tz_seconds (negative for timezones west of UTC).

        This is 100% reliable regardless of log activity.
        """
        # Check config override first
        if COWRIE_TZ_OFFSET_SECONDS is not None:
            print(f"  Using config offset  : {COWRIE_TZ_OFFSET_SECONDS}s ({COWRIE_TZ_OFFSET_SECONDS/3600:.1f}h) [from config.py]")
            return float(COWRIE_TZ_OFFSET_SECONDS)

        # Read Kali's local timezone offset
        stdout, _ = self.kali.run("date +%z", timeout=10)
        tz_str = stdout.strip()  # e.g. "-0400" or "+0530"

        try:
            # Parse ±HHMM → seconds
            sign   = 1 if tz_str[0] == '+' else -1
            hours  = int(tz_str[1:3])
            mins   = int(tz_str[3:5])
            offset = sign * (hours * 3600 + mins * 60)
            print(f"  Kali timezone        : {tz_str} = {offset}s ({offset/3600:.1f}h)")
            return float(offset)
        except (ValueError, IndexError) as e:
            print(f"  [warn] Could not parse timezone '{tz_str}': {e} — using 0")
            return 0.0

    def record_start_marker(self) -> datetime:
        """
        Returns session start in Cowrie's clock space.
        Uses Kali's timezone to convert system UTC → Cowrie log time.
        """
        if not self._offset_detected:
            self._last_offset = self.detect_clock_offset()
            self._offset_detected = True

        kali_now   = self.get_kali_utc_time()
        # Cowrie log time = kali_utc + local_tz_offset
        cowrie_now = kali_now + timedelta(seconds=self._last_offset)
        marker     = cowrie_now - timedelta(seconds=3)
        print(f"  Kali UTC now         : {kali_now.isoformat()}")
        print(f"  Session marker       : {marker.isoformat()} (Cowrie clock)")
        return marker

    # ── health check ──────────────────────────────────────────────────────────

    def check_cowrie_health(self) -> bool:
        stdout, _ = self.kali.run(
            "pgrep -f twistd > /dev/null 2>&1 && echo RUNNING || echo STOPPED",
            timeout=10
        )
        if "STOPPED" in stdout or not stdout.strip():
            print("  [FAIL] Cowrie is NOT running!")
            print("  [FIX]  cd ~/cowrie && source cowrie-env/bin/activate && bin/cowrie start")
            return False
        print("  [OK]   Cowrie process is running")

        stdout, _ = self.kali.run(
            f"test -r {COWRIE_LOG_PATH} && echo READABLE || echo UNREADABLE",
            timeout=10
        )
        if "UNREADABLE" in stdout:
            print(f"  [FAIL] Log file not readable: {COWRIE_LOG_PATH}")
            return False
        print("  [OK]   Log file is readable")
        return True

    # ── log reading ───────────────────────────────────────────────────────────

    def find_active_log(self) -> str:
        return COWRIE_LOG_PATH

    def get_session_logs(self, session_start: datetime, session_end: datetime = None) -> list[dict]:
        """
        Return log entries with timestamp >= session_start.
        Both session_start and session_end must be in Cowrie's clock space
        (i.e. already adjusted by the timezone offset).
        """
        stdout, stderr = self.kali.run(f"cat {COWRIE_LOG_PATH}", timeout=30)

        if "Permission denied" in stdout or "Permission denied" in stderr:
            print(f"  [warn] Permission denied reading log")
            return []
        if not stdout.strip():
            print(f"  [warn] Log file is empty")
            return []

        if session_start.tzinfo is None:
            session_start = session_start.replace(tzinfo=timezone.utc)
        if session_end and session_end.tzinfo is None:
            session_end = session_end.replace(tzinfo=timezone.utc)

        entries = []
        skipped = 0
        total   = 0
        all_ts  = []

        for line in stdout.splitlines():
            line = line.strip().replace("\x00", "")
            if not line:
                continue
            total += 1
            try:
                entry = json.loads(line)
                ts_str = entry.get("timestamp", "")
                if not ts_str:
                    continue
                ts = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
                all_ts.append(ts)

                after_start = ts >= session_start
                before_end  = (session_end is None) or (ts <= session_end)
                if after_start and before_end:
                    entries.append(entry)
            except (json.JSONDecodeError, ValueError):
                skipped += 1

        status = f"{total} total lines, {len(entries)} in session window"
        if skipped:
            status += f", {skipped} unparseable"
        print(f"  Log: {status}")

        if len(entries) == 0 and all_ts:
            earliest = min(all_ts)
            latest   = max(all_ts)
            print(f"  [debug] Log range  : {earliest.isoformat()}  ->  {latest.isoformat()}")
            print(f"  [debug] Window     : {session_start.isoformat()}  ->  {(session_end.isoformat() if session_end else 'open')}")
            gap = (session_start - latest).total_seconds()
            if gap > 0:
                print(f"  [debug] Marker is {gap:.0f}s after latest log entry — Cowrie did not log this session")
                print(f"  [debug] Check: is Cowrie running?  bin/cowrie status")
            else:
                print(f"  [debug] Log entries exist in range but window filter missed them — offset may be wrong")
                print(f"  [debug] Current offset: {self._last_offset:.0f}s — edit COWRIE_TZ_OFFSET_SECONDS in config.py to override")

        return entries

    def rotate_logs(self):
        """No-op — truncating cowrie.json severs its file handle."""
        pass
