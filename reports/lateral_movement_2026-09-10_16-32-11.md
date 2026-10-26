# Cowrie Honeypot Evaluation Report

| | |
|---|---|
| **Scenario** | `lateral_movement` |
| **Generated** | 2026-09-10_16-32-11 UTC |
| **Model** | Ollama LLM (llama3.1:8b) |
| **Overall Grade** | 🟠 **C** (6.4/10) |
| **Detection Rate** | 73.0% |
| **Events Captured** | 51 |
| **Commands Executed** | 37 |
| **Commands Logged** | N/A |

---

## Executive Summary

The honeypot appears to be safely contained, but there is some evidence of potential security risks. The attacker executed a variety of system and network reconnaissance commands, which could potentially compromise the system.

---

## Evaluation Scorecard

| Criterion | Score | Summary |
|-----------|-------|---------|
| **Realism** | `████████░░` 8.0/10 | The attacker executed a variety of system and network reconnaissance commands. |
| **Emulation Accuracy** | `░░░░░░░░░░` 0.0/10 | There is no evidence to suggest that the honeypot accurately emulated a real sys |
| **Data Quality & Telemetry** | `█████████░` 9.0/10 | The log data appears to be complete and accurate, with no missing or suspicious  |
| **Containment & Safety** | `██████░░░░` 6.0/10 | The honeypot appears to be safely contained, but there is some evidence of poten |
| **Operational Complexity** | `█░░░░░░░░░` 1.0/10 | The honeypot appears to be relatively simple to operate, with no complex configu |

**Overall Score: 6.4/10 — Grade: 🟠 C**

---

## Detailed Evaluation

### Realism

**Score:** `████████░░` 8.0/10

**Summary:** The attacker executed a variety of system and network reconnaissance commands.

#### 🟡 [MEDIUM] The attacker executed a mix of system and network reconnaissance commands.

- **Evidence:** `commands_executed`
- **Recommendation:** Review the list of executed commands for potential security risks.

### Emulation Accuracy

**Score:** `░░░░░░░░░░` 0.0/10

**Summary:** There is no evidence to suggest that the honeypot accurately emulated a real system.

#### 🔴 [HIGH] 

- **Evidence:** ``
- **Recommendation:** 

### Data Quality & Telemetry

**Score:** `█████████░` 9.0/10

**Summary:** The log data appears to be complete and accurate, with no missing or suspicious entries.

#### 🟢 [LOW] The log data is complete and accurate.

- **Evidence:** `total_events`
- **Recommendation:** No action required.

### Containment & Safety

**Score:** `██████░░░░` 6.0/10

**Summary:** The honeypot appears to be safely contained, but there is some evidence of potential security risks.

#### 🟡 [MEDIUM] The attacker executed commands that could potentially compromise the system.

- **Evidence:** `commands_executed`
- **Recommendation:** Review the list of executed commands for potential security risks.

### Operational Complexity

**Score:** `█░░░░░░░░░` 1.0/10

**Summary:** The honeypot appears to be relatively simple to operate, with no complex configuration or setup required.

#### 🟢 [LOW] The honeypot is relatively simple to operate.

- **Evidence:** ``
- **Recommendation:** 

---

## Top Vulnerabilities

### 1. 🟡 [MEDIUM] Potential security risks from executed commands

**CVSS Estimate:** Medium

The attacker executed a variety of system and network reconnaissance commands.

**Evidence:** `commands_executed`

**Recommendation:** Review the list of executed commands for potential security risks.

---

## How an Attacker Would Detect This is a Honeypot

> These are the behavioral tells that reveal Cowrie's artificial nature.

- The honeypot's log data is complete and accurate.

---

## Immediate Remediation Actions

1. Review the list of executed commands for potential security risks.

---

## Attack Commands Executed

```bash
hostname
hostname -I
ip addr
ip route
arp -a
ss -tulnp
netstat -tulnp
netstat -rn
ls -la ~/.ssh
cat ~/.ssh/config
cat ~/.ssh/known_hosts
cat ~/.ssh/authorized_keys
cat /etc/hosts
cat /etc/resolv.conf
hostnamectl
mount
df -h
lsblk
who
w
last
lastlog
systemctl list-units --type=service
service --status-all
ps aux
history
cat ~/.bash_history
printenv
getent group
getent passwd
cat /etc/sudoers
cat /etc/group
cat /etc/passwd
cat /etc/ssh/sshd_config
cat /etc/ssh/ssh_config
ssh-keygen -l -f /etc/ssh/ssh_host_rsa_key
ssh-keygen -l -f /etc/ssh/ssh_host_ecdsa_key
```

### Command Execution Results

| # | Command | Response (truncated) |
|---|---------|----------------------|
| 1 | `hostname` | hostname [4llocalhost [4hroot@localhost:~#  |
| 2 | `hostname -I` | hostname -I [4l[4hroot@-I:~#  |
| 3 | `ip addr` | ip addr -bash: ip: command not found root@-I:~#  |
| 4 | `ip route` | ip route -bash: ip: command not found root@-I:~#  |
| 5 | `arp -a` | arp -a -bash: arp: command not found root@-I:~#  |
| 6 | `ss -tulnp` | ss -tulnp -bash: ss: command not found root@-I:~#  |
| 7 | `netstat -tulnp` | netstat -tulnp [4lActive Internet connections (w/o servers) Proto Recv-Q Send |
| 8 | `netstat -rn` | netstat -rn [4lKernel IP routing table Destination     Gateway         Genmas |
| 9 | `ls -la ~/.ssh` | ls -la ~/.ssh [4lls: cannot access /root/.ssh: No such file or directory [4h |
| 10 | `cat ~/.ssh/config` | cat ~/.ssh/config [4lcat: ~/.ssh/config: No such file or directory [4hroot@- |
| 11 | `cat ~/.ssh/known_hosts` | cat ~/.ssh/known_hosts [4lcat: ~/.ssh/known_hosts: No such file or directory  |
| 12 | `cat ~/.ssh/authorized_keys` | cat ~/.ssh/authorized_keys [4lcat: ~/.ssh/authorized_keys: No such file or dir |
| 13 | `cat /etc/hosts` | cat /etc/hosts [4l127.0.0.1	localhost 127.0.1.1	nas3  # The following lines |
| 14 | `cat /etc/resolv.conf` | cat /etc/resolv.conf [4lnameserver 8.8.8.8 nameserver 8.8.4.4 [4hroot@-I:~# |
| 15 | `hostnamectl` | hostnamectl -bash: hostnamectl: command not found root@-I:~#  |
| 16 | `mount` | mount [4l-bash: /usr/bin/mount: cannot execute binary file: Exec format error |
| 17 | `df -h` | df -h [4l-bash: /usr/bin/df: cannot execute binary file: Exec format error [ |
| 18 | `lsblk` | lsblk [4l-bash: /usr/bin/lsblk: cannot execute binary file: Exec format error |
| 19 | `who` | who [4lroot     pts/0        2026-09-10 12:25 (192.168.56.1) [4hroot@-I:~#  |
| 20 | `w` | w [4l 12:28:04 up 4 min,  1 user,  load average: 0.00, 0.00, 0.00 USER     TT |
| 21 | `last` | last [4lroot     pts/0        192.168.56.1     Thu Sep 10 12:25   still logged |
| 22 | `lastlog` | lastlog [4l-bash: /usr/bin/lastlog: cannot execute binary file: Exec format er |
| 23 | `systemctl list-units --type=service` | systemctl list-units --type=service -bash: systemctl: command not found root@- |
| 24 | `service --status-all` | service --status-all [4l[ + ]  acpid [ - ]  alsa-utils [ + ]  anacron [ + ] |
| 25 | `ps aux` | ps aux [4lUSER         PID   %CPU       %MEM       VSZ       RSS       TTY     |
| 26 | `history` | history [4l    1  hostname     2  hostname -I     3  ip addr     4  ip rout |
| 27 | `cat ~/.bash_history` | cat ~/.bash_history [4lcat: ~/.bash_history: No such file or directory [4hro |
| 28 | `printenv` | printenv [4l-bash: /usr/bin/printenv: cannot execute binary file: Exec format  |
| 29 | `getent group` | getent group [4l-bash: /usr/bin/getent: cannot execute binary file: Exec forma |
| 30 | `getent passwd` | getent passwd [4l-bash: /usr/bin/getent: cannot execute binary file: Exec form |
| 31 | `cat /etc/sudoers` | cat /etc/sudoers [4lcat: /etc/sudoers: No such file or directory [4hroot@-I: |
| 32 | `cat /etc/group` | cat /etc/group [4lroot:x:0: daemon:x:1: bin:x:2: sys:x:3: adm:x:4: tty:x: |
| 33 | `cat /etc/passwd` | cat /etc/passwd [4lroot:x:0:0:root:/root:/bin/bash daemon:x:1:1:daemon:/usr/s |
| 34 | `cat /etc/ssh/sshd_config` | cat /etc/ssh/sshd_config [4l[4hroot@-I:~#  |
| 35 | `cat /etc/ssh/ssh_config` | cat /etc/ssh/ssh_config [4l[4hroot@-I:~#  |
| 36 | `ssh-keygen -l -f /etc/ssh/ssh_host_rsa_key` | ssh-keygen -l -f /etc/ssh/ssh_host_rsa_key [4l-bash: /usr/bin/ssh-keygen: cann |
| 37 | `ssh-keygen -l -f /etc/ssh/ssh_host_ecdsa_key` | ssh-keygen -l -f /etc/ssh/ssh_host_ecdsa_key [4l-bash: /usr/bin/ssh-keygen: ca |

---

## Cowrie Log Sample (first 20 events)

```json
[
  {
    "session": "f03a33eece1c",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 61272,
    "dst_ip": "192.168.56.102",
    "dst_port": 2222,
    "eventid": "cowrie.session.connect",
    "sensor": "kali",
    "uuid": "b7a15396-8fb7-11f1-9021-08002717ff2b",
    "timestamp": "2026-09-10T12:25:52.952799Z",
    "message": "New connection: 192.168.56.1:61272 (192.168.56.102:2222) [session: f03a33eece1c]"
  },
  {
    "session": "f03a33eece1c",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 61272,
    "dst_ip": "192.168.56.102",
    "dst_port": 2222,
    "version": "SSH-2.0-paramiko_3.4.0",
    "eventid": "cowrie.client.version",
    "sensor": "kali",
    "uuid": "b7a15396-8fb7-11f1-9021-08002717ff2b",
    "timestamp": "2026-09-10T12:25:52.969913Z",
    "message": "Remote SSH version: SSH-2.0-paramiko_3.4.0"
  },
  {
    "session": "f03a33eece1c",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 61272,
    "dst_ip": "192.168.56.102",
    "dst_port": 2222,
    "hassh": "87e3d9ffee0540b0390f8a5b9c343c08",
    "hasshAlgorithms": "curve25519-sha256@libssh.org,ecdh-sha2-nistp256,ecdh-sha2-nistp384,ecdh-sha2-nistp521,diffie-hellman-group16-sha512,diffie-hellman-group-exchange-sha256,diffie-hellman-group14-sha256,diffie-hellman-group-exchange-sha1,diffie-hellman-group14-sha1,diffie-hellman-group1-sha1,ext-info-c,kex-strict-c-v00@openssh.com;aes128-ctr,aes192-ctr,aes256-ctr,aes128-cbc,aes192-cbc,aes256-cbc,3des-cbc;hmac-sha2-256,hmac-sha2-512,hmac-sha2-256-etm@openssh.com,hmac-sha2-512-etm@openssh.com,hmac-sha1,hmac-md5,hmac-sha1-96,hmac-md5-96;none",
    "kexAlgs": [
      "curve25519-sha256@libssh.org",
      "ecdh-sha2-nistp256",
      "ecdh-sha2-nistp384",
      "ecdh-sha2-nistp521",
      "diffie-hellman-group16-sha512",
      "diffie-hellman-group-exchange-sha256",
      "diffie-hellman-group14-sha256",
      "diffie-hellman-group-exchange-sha1",
      "diffie-hellman-group14-sha1",
      "diffie-hellman-group1-sha1",
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
      "ssh-rsa",
      "ssh-dss",
      "ssh-ed25519-cert-v01@openssh.com",
      "ecdsa-sha2-nistp256-cert-v01@openssh.com",
      "ecdsa-sha2-nistp384-cert-v01@openssh.com",
      "ecdsa-sha2-nistp521-cert-v01@openssh.com",
      "rsa-sha2-512-cert-v01@openssh.com",
      "rsa-sha2-256-cert-v01@openssh.com",
      "ssh-rsa-cert-v01@openssh.com",
      "ssh-dss-cert-v01@openssh.com"
    ],
    "encCS": [
      "aes128-ctr",
      "aes192-ctr",
      "aes256-ctr",
      "aes128-cbc",
      "aes192-cbc",
      "aes256-cbc",
      "3des-cbc"
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
    "timestamp": "2026-09-10T12:25:52.971185Z",
    "message": "SSH client hassh fingerprint: 87e3d9ffee0540b0390f8a5b9c343c08"
  },
  {
    "session": "f03a33eece1c",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 61272,
    "dst_ip": "192.168.56.102",
    "dst_port": 2222,
    "username": "root",
    "password": "password",
    "eventid": "cowrie.login.success",
    "sensor": "kali",
    "uuid": "b7a15396-8fb7-11f1-9021-08002717ff2b",
    "timestamp": "2026-09-10T12:25:53.041039Z",
    "message": "login attempt [root/password] succeeded"
  },
  {
    "session": "f03a33eece1c",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 61272,
    "dst_ip": "192.168.56.102",
    "dst_port": 2222,
    "width": 80,
    "height": 24,
    "eventid": "cowrie.client.size",
    "sensor": "kali",
    "uuid": "b7a15396-8fb7-11f1-9021-08002717ff2b",
    "timestamp": "2026-09-10T12:25:53.052379Z",
    "message": "Terminal Size: 80 24"
  },
  {
    "session": "f03a33eece1c",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 61272,
    "dst_ip": "192.168.56.102",
    "dst_port": 2222,
    "arch": "linux-x64-lsb",
    "eventid": "cowrie.session.params",
    "sensor": "kali",
    "uuid": "b7a15396-8fb7-11f1-9021-08002717ff2b",
    "timestamp": "2026-09-10T12:25:53.058089Z",
    "message": ""
  },
  {
    "session": "f03a33eece1c",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 61272,
    "dst_ip": "192.168.56.102",
    "dst_port": 2222,
    "input": "hostname",
    "eventid": "cowrie.command.input",
    "sensor": "kali",
    "uuid": "b7a15396-8fb7-11f1-9021-08002717ff2b",
    "timestamp": "2026-09-10T12:26:00.091497Z",
    "message": "CMD: hostname"
  },
  {
    "session": "f03a33eece1c",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 61272,
    "dst_ip": "192.168.56.102",
    "dst_port": 2222,
    "input": "hostname -I",
    "eventid": "cowrie.command.input",
    "sensor": "kali",
    "uuid": "b7a15396-8fb7-11f1-9021-08002717ff2b",
    "timestamp": "2026-09-10T12:26:06.612032Z",
    "message": "CMD: hostname -I"
  },
  {
    "session": "f03a33eece1c",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 61272,
    "dst_ip": "192.168.56.102",
    "dst_port": 2222,
    "input": "ip addr",
    "eventid": "cowrie.command.input",
    "sensor": "kali",
    "uuid": "b7a15396-8fb7-11f1-9021-08002717ff2b",
    "timestamp": "2026-09-10T12:26:13.143724Z",
    "message": "CMD: ip addr"
  },
  {
    "session": "f03a33eece1c",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 61272,
    "dst_ip": "192.168.56.102",
    "dst_port": 2222,
    "input": "ip addr",
    "eventid": "cowrie.command.failed",
    "sensor": "kali",
    "uuid": "b7a15396-8fb7-11f1-9021-08002717ff2b",
    "timestamp": "2026-09-10T12:26:13.156889Z",
    "message": "Command not found: ip addr"
  },
  {
    "session": "f03a33eece1c",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 61272,
    "dst_ip": "192.168.56.102",
    "dst_port": 2222,
    "input": "ip route",
    "eventid": "cowrie.command.input",
    "sensor": "kali",
    "uuid": "b7a15396-8fb7-11f1-9021-08002717ff2b",
    "timestamp": "2026-09-10T12:26:19.659282Z",
    "message": "CMD: ip route"
  },
  {
    "session": "f03a33eece1c",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 61272,
    "dst_ip": "192.168.56.102",
    "dst_port": 2222,
    "input": "ip route",
    "eventid": "cowrie.command.failed",
    "sensor": "kali",
    "uuid": "b7a15396-8fb7-11f1-9021-08002717ff2b",
    "timestamp": "2026-09-10T12:26:19.676122Z",
    "message": "Command not found: ip route"
  },
  {
    "session": "f03a33eece1c",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 61272,
    "dst_ip": "192.168.56.102",
    "dst_port": 2222,
    "input": "arp -a",
    "eventid": "cowrie.command.input",
    "sensor": "kali",
    "uuid": "b7a15396-8fb7-11f1-9021-08002717ff2b",
    "timestamp": "2026-09-10T12:26:26.187042Z",
    "message": "CMD: arp -a"
  },
  {
    "session": "f03a33eece1c",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 61272,
    "dst_ip": "192.168.56.102",
    "dst_port": 2222,
    "input": "arp -a",
    "eventid": "cowrie.command.failed",
    "sensor": "kali",
    "uuid": "b7a15396-8fb7-11f1-9021-08002717ff2b",
    "timestamp": "2026-09-10T12:26:26.206793Z",
    "message": "Command not found: arp -a"
  },
  {
    "session": "f03a33eece1c",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 61272,
    "dst_ip": "192.168.56.102",
    "dst_port": 2222,
    "input": "ss -tulnp",
    "eventid": "cowrie.command.input",
    "sensor": "kali",
    "uuid": "b7a15396-8fb7-11f1-9021-08002717ff2b",
    "timestamp": "2026-09-10T12:26:32.724787Z",
    "message": "CMD: ss -tulnp"
  },
  {
    "session": "f03a33eece1c",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 61272,
    "dst_ip": "192.168.56.102",
    "dst_port": 2222,
    "input": "ss -tulnp",
    "eventid": "cowrie.command.failed",
    "sensor": "kali",
    "uuid": "b7a15396-8fb7-11f1-9021-08002717ff2b",
    "timestamp": "2026-09-10T12:26:32.738697Z",
    "message": "Command not found: ss -tulnp"
  },
  {
    "session": "f03a33eece1c",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 61272,
    "dst_ip": "192.168.56.102",
    "dst_port": 2222,
    "input": "netstat -tulnp",
    "eventid": "cowrie.command.input",
    "sensor": "kali",
    "uuid": "b7a15396-8fb7-11f1-9021-08002717ff2b",
    "timestamp": "2026-09-10T12:26:39.248248Z",
    "message": "CMD: netstat -tulnp"
  },
  {
    "session": "f03a33eece1c",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 61272,
    "dst_ip": "192.168.56.102",
    "dst_port": 2222,
    "input": "netstat -rn",
    "eventid": "cowrie.command.input",
    "sensor": "kali",
    "uuid": "b7a15396-8fb7-11f1-9021-08002717ff2b",
    "timestamp": "2026-09-10T12:26:45.766311Z",
    "message": "CMD: netstat -rn"
  },
  {
    "session": "f03a33eece1c",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 61272,
    "dst_ip": "192.168.56.102",
    "dst_port": 2222,
    "input": "ls -la ~/.ssh",
    "eventid": "cowrie.command.input",
    "sensor": "kali",
    "uuid": "b7a15396-8fb7-11f1-9021-08002717ff2b",
    "timestamp": "2026-09-10T12:26:52.286999Z",
    "message": "CMD: ls -la ~/.ssh"
  },
  {
    "session": "f03a33eece1c",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 61272,
    "dst_ip": "192.168.56.102",
    "dst_port": 2222,
    "input": "cat ~/.ssh/config",
    "eventid": "cowrie.command.input",
    "sensor": "kali",
    "uuid": "b7a15396-8fb7-11f1-9021-08002717ff2b",
    "timestamp": "2026-09-10T12:26:58.817869Z",
    "message": "CMD: cat ~/.ssh/config"
  }
]
```

---
*Generated by LLM-based Cowrie Honeypot Evaluator*
