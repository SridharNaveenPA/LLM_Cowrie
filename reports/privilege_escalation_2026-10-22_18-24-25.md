# Cowrie Honeypot Evaluation Report — Agentic Mode

| | |
|---|---|
| **Scenario** | `privilege_escalation` |
| **Generated** | 2026-10-22_18-24-25 UTC |
| **Mode** | Agentic (step-by-step LLM attack loop) |
| **Model** | Ollama LLM (llama3.1:8b) |
| **Overall Grade** | 🟡 **B** (7.0/10) |
| **Detection Rate** | 100% |
| **Events Captured** | 29 |
| **Attack Steps** | 7 (LLM stopped early (sufficient evidence gathered)) |

---

## Executive Summary

The attacker's actions and commands suggest that the system may be vulnerable to privilege escalation. The Cowrie log events accurately reflect the attacker's actions and commands, indicating that the honeypot is functioning correctly. However, there are some minor issues with the Cowrie log events, and the honeypot's security should be reviewed to ensure that it can withstand potential attacks.

---

## Evaluation Scorecard

| Criterion | Score | Summary |
|-----------|-------|---------|
| **Realism** | `████████░░` 8.0/10 | The attacker's actions and commands are realistic and consistent with a privileg |
| **Emulation Accuracy** | `█████████░` 9.0/10 | The honeypot's emulation accuracy is high, as the attacker's actions and command |
| **Data Quality & Telemetry** | `███████░░░` 7.0/10 | The data quality is good, but there are some minor issues with the Cowrie log ev |
| **Containment & Safety** | `██████░░░░` 6.0/10 | The honeypot's containment safety is moderate, as the attacker's actions could p |
| **Operational Complexity** | `█████░░░░░` 5.0/10 | The operational complexity is low, as the honeypot's configuration and logging m |

**Overall Score: 7.0/10 — Grade: 🟡 B**

---

## Detailed Evaluation

### Realism

**Score:** `████████░░` 8.0/10

**Summary:** The attacker's actions and commands are realistic and consistent with a privilege escalation attack.

#### 🟡 [MEDIUM] The attacker's commands are well-structured and follow a logical sequence.

- **Evidence:** `The commands logged by Cowrie are well-structured and follow a logical sequence.`
- **Recommendation:** The honeypot's configuration and logging mechanism are adequate to detect and record realistic attacker actions.

### Emulation Accuracy

**Score:** `█████████░` 9.0/10

**Summary:** The honeypot's emulation accuracy is high, as the attacker's actions and commands are accurately reflected in the Cowrie log events.

#### 🔴 [HIGH] The honeypot accurately recorded the attacker's commands and output.

- **Evidence:** `The Cowrie log events accurately reflect the attacker's commands and output.`
- **Recommendation:** The honeypot's emulation accuracy is high, indicating that the honeypot is functioning correctly and accurately recording attacker actions.

### Data Quality & Telemetry

**Score:** `███████░░░` 7.0/10

**Summary:** The data quality is good, but there are some minor issues with the Cowrie log events.

#### 🟡 [MEDIUM] Some Cowrie log events are missing or incomplete.

- **Evidence:** `The Cowrie log events for some commands are missing or incomplete.`
- **Recommendation:** The honeypot's logging mechanism should be reviewed to ensure that all relevant data is being recorded.

### Containment & Safety

**Score:** `██████░░░░` 6.0/10

**Summary:** The honeypot's containment safety is moderate, as the attacker's actions could potentially compromise the honeypot's security.

#### 🟡 [MEDIUM] The attacker's commands could potentially compromise the honeypot's security.

- **Evidence:** `The Cowrie log events show that the attacker is attempting to escalate privileges.`
- **Recommendation:** The honeypot's security should be reviewed to ensure that it can withstand potential attacks.

### Operational Complexity

**Score:** `█████░░░░░` 5.0/10

**Summary:** The operational complexity is low, as the honeypot's configuration and logging mechanism are relatively simple.

#### 🟢 [LOW] The honeypot's configuration and logging mechanism are relatively simple.

- **Evidence:** `The Cowrie log events are relatively simple to analyze.`
- **Recommendation:** The honeypot's configuration and logging mechanism should be reviewed to ensure that they are adequate for detecting and recording attacker actions.

---

## Top Vulnerabilities Identified

### 1. 🔴 [HIGH] Potential Privilege Escalation Vulnerability

**CVSS Estimate:** Critical

The attacker's commands suggest that the system may be vulnerable to privilege escalation.

**Evidence:** `The Cowrie log events show that the attacker is attempting to escalate privileges.`

**Exposed by command:** `lsb_release -a`

**Recommendation:** The system should be reviewed to ensure that it is secure and not vulnerable to privilege escalation.

---

## How an Attacker Would Detect This is a Honeypot

> Observable tells that reveal Cowrie's artificial nature, discovered during the agentic attack.

- The system's kernel version and potential vulnerabilities or misconfigurations (uname -a output).
- The absence of the lsb_release command (lsb_release -a output).

---

## Immediate Remediation Actions

1. Review the system's kernel version and potential vulnerabilities or misconfigurations.
2. Check the system for the presence of the lsb_release command.

---

## Agentic Attack Trail

> This section shows the LLM's decision trail: each command it chose, its reasoning, the honeypot's response, and how many Cowrie events were triggered.

### Step 1: `uname -a`

**LLM Reasoning:** _To understand the system's kernel version and potentially identify any known vulnerabilities or misconfigurations._

**Cowrie Response:**
```
uname -a
[4lLinux localhost 6.1.0-21-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.1.90-1 (2024-05-03) x86_64 GNU/Linux
[4hroot@localhost:~# 
```

**Cowrie Log Events (4 total):**
- `cowrie.client.size` × 1
- `cowrie.session.params` × 1
- `cowrie.command.input` × 1
- `cowrie.log.closed` × 1

### Step 2: `lsb_release -a`

**LLM Reasoning:** _The honeypot's uname output suggests it's running a Debian-based system, so checking the LSB (Linux Standard Base) release information can help identify potential vulnerabilities and version mismatche_

**Cowrie Response:**
```
lsb_release -a
-bash: lsb_release: command not found
root@localhost:~# 
```

**Cowrie Log Events (5 total):**
- `cowrie.client.size` × 1
- `cowrie.session.params` × 1
- `cowrie.command.input` × 1
- `cowrie.command.failed` × 1
- `cowrie.log.closed` × 1

### Step 3: `ls /usr/bin | grep -v bin`

**LLM Reasoning:** _The lsb_release command is not found, indicating a potential issue with the system's package management. I'll check if other system utilities are also missing._

**Cowrie Response:**
```
ls /usr/bin | grep -v bin
[4l[4h[4l[4hroot@localhost:~# 
```

**Cowrie Log Events (4 total):**
- `cowrie.client.size` × 1
- `cowrie.session.params` × 1
- `cowrie.command.input` × 1
- `cowrie.log.closed` × 1

### Step 4: `ls /etc/passwd`

**LLM Reasoning:** _The attacker is searching for potential privilege escalation opportunities. The previous command (Step 3) already probed the /usr/bin directory, so the next logical step is to examine the /etc/passwd _

**Cowrie Response:**
```
ls /etc/passwd
[4l/etc/passwd 
[4hroot@localhost:~# 
```

**Cowrie Log Events (4 total):**
- `cowrie.client.size` × 1
- `cowrie.session.params` × 1
- `cowrie.command.input` × 1
- `cowrie.log.closed` × 1

### Step 5: `ls /usr/lib/python*`

**LLM Reasoning:** _The attacker is searching for potential privilege escalation opportunities. In step 2, the lsb_release command was not found, suggesting that the system may be missing certain packages. The attacker m_

**Cowrie Response:**
```
ls /usr/lib/python*
[4lls: cannot access /usr/lib/python*: No such file or directory
[4hroot@localhost:~# 
```

**Cowrie Log Events (4 total):**
- `cowrie.client.size` × 1
- `cowrie.session.params` × 1
- `cowrie.command.input` × 1
- `cowrie.log.closed` × 1

### Step 6: `ls /etc/group`

**LLM Reasoning:** _The attacker has already probed the /etc/passwd file, which is a common location for system files. Now, the attacker can check the /etc/group file to see if there are any suspicious group memberships _

**Cowrie Response:**
```
ls /etc/group
[4l/etc/group 
[4hroot@localhost:~# 
```

**Cowrie Log Events (4 total):**
- `cowrie.client.size` × 1
- `cowrie.session.params` × 1
- `cowrie.command.input` × 1
- `cowrie.log.closed` × 1

### Step 7: `python -c 'import os; print(os.uname())'`

**LLM Reasoning:** _The previous command in step 5 already probed the Python library, so now we'll try to run a Python command to see if the Python interpreter is vulnerable to exploitation. This command will attempt to _

**Cowrie Response:**
```
python -c 'import os; print(os.uname())'
[4l
```

**Cowrie Log Events (4 total):**
- `cowrie.client.size` × 1
- `cowrie.session.params` × 1
- `cowrie.command.input` × 1
- `cowrie.log.closed` × 1

---

## Full Session Cowrie Log Sample (first 20 events)

```json
[
  {
    "session": "5a57879b7568",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 65188,
    "dst_ip": "192.168.56.102",
    "dst_port": 2222,
    "eventid": "cowrie.session.connect",
    "sensor": "kali",
    "uuid": "b7a15396-8fb7-11f1-9021-08002717ff2b",
    "timestamp": "2026-10-22T14:17:14.770941Z",
    "message": "New connection: 192.168.56.1:65188 (192.168.56.102:2222) [session: 5a57879b7568]"
  },
  {
    "session": "5a57879b7568",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 65188,
    "dst_ip": "192.168.56.102",
    "dst_port": 2222,
    "version": "SSH-2.0-paramiko_5.1.0",
    "eventid": "cowrie.client.version",
    "sensor": "kali",
    "uuid": "b7a15396-8fb7-11f1-9021-08002717ff2b",
    "timestamp": "2026-10-22T14:17:14.783196Z",
    "message": "Remote SSH version: SSH-2.0-paramiko_5.1.0"
  },
  {
    "session": "5a57879b7568",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 65188,
    "dst_ip": "192.168.56.102",
    "dst_port": 2222,
    "hassh": "4c94058d5e9e31659879f79fd5b46084",
    "hasshAlgorithms": "mlkem768x25519-sha256,curve25519-sha256@libssh.org,ecdh-sha2-nistp256,ecdh-sha2-nistp384,ecdh-sha2-nistp521,diffie-hellman-group16-sha512,diffie-hellman-group-exchange-sha256,diffie-hellman-group14-sha256,ext-info-c,kex-strict-c-v00@openssh.com;aes128-ctr,aes192-ctr,aes256-ctr,aes128-cbc,aes192-cbc,aes256-cbc,3des-cbc,aes128-gcm@openssh.com,aes256-gcm@openssh.com;hmac-sha2-256,hmac-sha2-512,hmac-sha2-256-etm@openssh.com,hmac-sha2-512-etm@openssh.com,hmac-sha1,hmac-md5,hmac-sha1-96,hmac-md5-96;none",
    "kexAlgs": [
      "mlkem768x25519-sha256",
      "curve25519-sha256@libssh.org",
      "ecdh-sha2-nistp256",
      "ecdh-sha2-nistp384",
      "ecdh-sha2-nistp521",
      "diffie-hellman-group16-sha512",
      "diffie-hellman-group-exchange-sha256",
      "diffie-hellman-group14-sha256",
      "ext-info-c",
      "kex-strict-c-v00@openssh.com"
    ],
    "keyAlgs": [
      "ssh-ed25519",
      "ecdsa-sha2-nistp256",
      "ecdsa-sha2-nistp384",
      "ecdsa-sha2-nistp521",
      "rsa-sha2-512",
      "rsa-sha2-256",
      "ssh-ed25519-cert-v01@openssh.com",
      "ecdsa-sha2-nistp256-cert-v01@openssh.com",
      "ecdsa-sha2-nistp384-cert-v01@openssh.com",
      "ecdsa-sha2-nistp521-cert-v01@openssh.com",
      "rsa-sha2-512-cert-v01@openssh.com",
      "rsa-sha2-256-cert-v01@openssh.com"
    ],
    "encCS": [
      "aes128-ctr",
      "aes192-ctr",
      "aes256-ctr",
      "aes128-cbc",
      "aes192-cbc",
      "aes256-cbc",
      "3des-cbc",
      "aes128-gcm@openssh.com",
      "aes256-gcm@openssh.com"
    ],
    "macCS": [
      "hmac-sha2-256",
      "hmac-sha2-512",
      "hmac-sha2-256-etm@openssh.com",
      "hmac-sha2-512-etm@openssh.com",
      "hmac-sha1",
      "hmac-md5",
      "hmac-sha1-96",
      "hmac-md5-96"
    ],
    "compCS": [
      "none"
    ],
    "langCS": [
      ""
    ],
    "eventid": "cowrie.client.kex",
    "sensor": "kali",
    "uuid": "b7a15396-8fb7-11f1-9021-08002717ff2b",
    "timestamp": "2026-10-22T14:17:14.787931Z",
    "message": "SSH client hassh fingerprint: 4c94058d5e9e31659879f79fd5b46084"
  },
  {
    "session": "5a57879b7568",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 65188,
    "dst_ip": "192.168.56.102",
    "dst_port": 2222,
    "username": "root",
    "password": "password",
    "eventid": "cowrie.login.success",
    "sensor": "kali",
    "uuid": "b7a15396-8fb7-11f1-9021-08002717ff2b",
    "timestamp": "2026-10-22T14:17:14.906745Z",
    "message": "login attempt [root/password] succeeded"
  },
  {
    "session": "5a57879b7568",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 65188,
    "dst_ip": "192.168.56.102",
    "dst_port": 2222,
    "width": 80,
    "height": 24,
    "eventid": "cowrie.client.size",
    "sensor": "kali",
    "uuid": "b7a15396-8fb7-11f1-9021-08002717ff2b",
    "timestamp": "2026-10-22T14:17:31.996936Z",
    "message": "Terminal Size: 80 24"
  },
  {
    "session": "5a57879b7568",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 65188,
    "dst_ip": "192.168.56.102",
    "dst_port": 2222,
    "arch": "linux-x64-lsb",
    "eventid": "cowrie.session.params",
    "sensor": "kali",
    "uuid": "b7a15396-8fb7-11f1-9021-08002717ff2b",
    "timestamp": "2026-10-22T14:17:32.003355Z",
    "message": ""
  },
  {
    "session": "5a57879b7568",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 65188,
    "dst_ip": "192.168.56.102",
    "dst_port": 2222,
    "input": "uname -a",
    "eventid": "cowrie.command.input",
    "sensor": "kali",
    "uuid": "b7a15396-8fb7-11f1-9021-08002717ff2b",
    "timestamp": "2026-10-22T14:17:39.027541Z",
    "message": "CMD: uname -a"
  },
  {
    "session": "5a57879b7568",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 65188,
    "dst_ip": "192.168.56.102",
    "dst_port": 2222,
    "ttylog": "var/lib/cowrie/tty/a5c41ad2a873e7904cb35754bf57108df0b72d5939ba9d9b0a8250affda6285d",
    "size": 443,
    "shasum": "a5c41ad2a873e7904cb35754bf57108df0b72d5939ba9d9b0a8250affda6285d",
    "duplicate": true,
    "duration_ms": 14047,
    "eventid": "cowrie.log.closed",
    "sensor": "kali",
    "uuid": "b7a15396-8fb7-11f1-9021-08002717ff2b",
    "timestamp": "2026-10-22T14:17:46.047152Z",
    "message": "Closing TTY Log: var/lib/cowrie/tty/a5c41ad2a873e7904cb35754bf57108df0b72d5939ba9d9b0a8250affda6285d after 14047 milliseconds"
  },
  {
    "session": "5a57879b7568",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 65188,
    "dst_ip": "192.168.56.102",
    "dst_port": 2222,
    "width": 80,
    "height": 24,
    "eventid": "cowrie.client.size",
    "sensor": "kali",
    "uuid": "b7a15396-8fb7-11f1-9021-08002717ff2b",
    "timestamp": "2026-10-22T14:17:55.931285Z",
    "message": "Terminal Size: 80 24"
  },
  {
    "session": "5a57879b7568",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 65188,
    "dst_ip": "192.168.56.102",
    "dst_port": 2222,
    "arch": "linux-x64-lsb",
    "eventid": "cowrie.session.params",
    "sensor": "kali",
    "uuid": "b7a15396-8fb7-11f1-9021-08002717ff2b",
    "timestamp": "2026-10-22T14:17:55.934010Z",
    "message": ""
  },
  {
    "session": "5a57879b7568",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 65188,
    "dst_ip": "192.168.56.102",
    "dst_port": 2222,
    "input": "lsb_release -a",
    "eventid": "cowrie.command.input",
    "sensor": "kali",
    "uuid": "b7a15396-8fb7-11f1-9021-08002717ff2b",
    "timestamp": "2026-10-22T14:18:02.962489Z",
    "message": "CMD: lsb_release -a"
  },
  {
    "session": "5a57879b7568",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 65188,
    "dst_ip": "192.168.56.102",
    "dst_port": 2222,
    "input": "lsb_release -a",
    "eventid": "cowrie.command.failed",
    "sensor": "kali",
    "uuid": "b7a15396-8fb7-11f1-9021-08002717ff2b",
    "timestamp": "2026-10-22T14:18:02.972702Z",
    "message": "Command not found: lsb_release -a"
  },
  {
    "session": "5a57879b7568",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 65188,
    "dst_ip": "192.168.56.102",
    "dst_port": 2222,
    "ttylog": "var/lib/cowrie/tty/75d3095b96a018db91370d977c85970c2c0accc959de9a00ad4ae89366fc51dd",
    "size": 379,
    "shasum": "75d3095b96a018db91370d977c85970c2c0accc959de9a00ad4ae89366fc51dd",
    "duplicate": false,
    "duration_ms": 14047,
    "eventid": "cowrie.log.closed",
    "sensor": "kali",
    "uuid": "b7a15396-8fb7-11f1-9021-08002717ff2b",
    "timestamp": "2026-10-22T14:18:09.980781Z",
    "message": "Closing TTY Log: var/lib/cowrie/tty/75d3095b96a018db91370d977c85970c2c0accc959de9a00ad4ae89366fc51dd after 14047 milliseconds"
  },
  {
    "session": "5a57879b7568",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 65188,
    "dst_ip": "192.168.56.102",
    "dst_port": 2222,
    "width": 80,
    "height": 24,
    "eventid": "cowrie.client.size",
    "sensor": "kali",
    "uuid": "b7a15396-8fb7-11f1-9021-08002717ff2b",
    "timestamp": "2026-10-22T14:18:19.334987Z",
    "message": "Terminal Size: 80 24"
  },
  {
    "session": "5a57879b7568",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 65188,
    "dst_ip": "192.168.56.102",
    "dst_port": 2222,
    "arch": "linux-x64-lsb",
    "eventid": "cowrie.session.params",
    "sensor": "kali",
    "uuid": "b7a15396-8fb7-11f1-9021-08002717ff2b",
    "timestamp": "2026-10-22T14:18:19.338916Z",
    "message": ""
  },
  {
    "session": "5a57879b7568",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 65188,
    "dst_ip": "192.168.56.102",
    "dst_port": 2222,
    "input": "ls /usr/bin | grep -v bin",
    "eventid": "cowrie.command.input",
    "sensor": "kali",
    "uuid": "b7a15396-8fb7-11f1-9021-08002717ff2b",
    "timestamp": "2026-10-22T14:18:26.368541Z",
    "message": "CMD: ls /usr/bin | grep -v bin"
  },
  {
    "session": "5a57879b7568",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 65188,
    "dst_ip": "192.168.56.102",
    "dst_port": 2222,
    "ttylog": "var/lib/cowrie/tty/cb87325143ff084bdb40d9f8a76d89c04dd510f766023c41bbe5ee7d3a061611",
    "size": 368,
    "shasum": "cb87325143ff084bdb40d9f8a76d89c04dd510f766023c41bbe5ee7d3a061611",
    "duplicate": false,
    "duration_ms": 14043,
    "eventid": "cowrie.log.closed",
    "sensor": "kali",
    "uuid": "b7a15396-8fb7-11f1-9021-08002717ff2b",
    "timestamp": "2026-10-22T14:18:33.380381Z",
    "message": "Closing TTY Log: var/lib/cowrie/tty/cb87325143ff084bdb40d9f8a76d89c04dd510f766023c41bbe5ee7d3a061611 after 14043 milliseconds"
  },
  {
    "session": "5a57879b7568",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 65188,
    "dst_ip": "192.168.56.102",
    "dst_port": 2222,
    "width": 80,
    "height": 24,
    "eventid": "cowrie.client.size",
    "sensor": "kali",
    "uuid": "b7a15396-8fb7-11f1-9021-08002717ff2b",
    "timestamp": "2026-10-22T14:18:46.351506Z",
    "message": "Terminal Size: 80 24"
  },
  {
    "session": "5a57879b7568",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 65188,
    "dst_ip": "192.168.56.102",
    "dst_port": 2222,
    "arch": "linux-x64-lsb",
    "eventid": "cowrie.session.params",
    "sensor": "kali",
    "uuid": "b7a15396-8fb7-11f1-9021-08002717ff2b",
    "timestamp": "2026-10-22T14:18:46.353775Z",
    "message": ""
  },
  {
    "session": "5a57879b7568",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 65188,
    "dst_ip": "192.168.56.102",
    "dst_port": 2222,
    "input": "ls /etc/passwd",
    "eventid": "cowrie.command.input",
    "sensor": "kali",
    "uuid": "b7a15396-8fb7-11f1-9021-08002717ff2b",
    "timestamp": "2026-10-22T14:18:53.377821Z",
    "message": "CMD: ls /etc/passwd"
  }
]
```

---
*Generated by LLM-based Cowrie Honeypot Evaluator — Agentic Mode*
