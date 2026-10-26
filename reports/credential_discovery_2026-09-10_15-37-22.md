# Cowrie Honeypot Evaluation Report

| | |
|---|---|
| **Scenario** | `credential_discovery` |
| **Generated** | 2026-09-10_15-37-22 UTC |
| **Model** | Ollama LLM (llama3.1:8b) |
| **Overall Grade** | 🟠 **C** (6.4/10) |
| **Detection Rate** | 85.56% |
| **Events Captured** | 45 |
| **Commands Executed** | 56 |
| **Commands Logged** | N/A |

---

## Executive Summary

The honeypot appears to be safely contained, but some commands may have been executed. The attacker attempted to discover credentials through various commands. Review the list of executed commands to identify potential security risks.

---

## Evaluation Scorecard

| Criterion | Score | Summary |
|-----------|-------|---------|
| **Realism** | `████████░░` 8.0/10 | The attacker attempted to discover credentials through various commands. |
| **Emulation Accuracy** | `░░░░░░░░░░` 0.0/10 | There is no evidence of the honeypot's emulation accuracy. |
| **Data Quality & Telemetry** | `█████████░` 9.0/10 | The log data appears to be complete and accurate. |
| **Containment & Safety** | `██████░░░░` 6.0/10 | The honeypot appears to be safely contained, but some commands may have been exe |
| **Operational Complexity** | `██░░░░░░░░` 2.0/10 | The honeypot's operational complexity appears to be low. |

**Overall Score: 6.4/10 — Grade: 🟠 C**

---

## Detailed Evaluation

### Realism

**Score:** `████████░░` 8.0/10

**Summary:** The attacker attempted to discover credentials through various commands.

#### 🟡 [MEDIUM] The attacker attempted to discover credentials through various commands.

- **Evidence:** `commands_executed`
- **Recommendation:** Review the list of executed commands to identify potential security risks.

### Emulation Accuracy

**Score:** `░░░░░░░░░░` 0.0/10

**Summary:** There is no evidence of the honeypot's emulation accuracy.

_No specific findings._

### Data Quality & Telemetry

**Score:** `█████████░` 9.0/10

**Summary:** The log data appears to be complete and accurate.

_No specific findings._

### Containment & Safety

**Score:** `██████░░░░` 6.0/10

**Summary:** The honeypot appears to be safely contained, but some commands may have been executed.

#### 🟡 [MEDIUM] The attacker executed commands that may have accessed sensitive files.

- **Evidence:** `commands_executed`
- **Recommendation:** Review the list of executed commands to identify potential security risks.

### Operational Complexity

**Score:** `██░░░░░░░░` 2.0/10

**Summary:** The honeypot's operational complexity appears to be low.

_No specific findings._

---

## Top Vulnerabilities

### 1. 🟡 [MEDIUM] Potential Credential Discovery

**CVSS Estimate:** Medium

The attacker attempted to discover credentials through various commands.

**Evidence:** `commands_executed`

**Recommendation:** Review the list of executed commands to identify potential security risks.

---

## How an Attacker Would Detect This is a Honeypot

> These are the behavioral tells that reveal Cowrie's artificial nature.

- The attacker would notice that the honeypot is safely contained, but some commands may have been executed.

---

## Immediate Remediation Actions

1. Review the list of executed commands to identify potential security risks.

---

## Attack Commands Executed

```bash
whoami
id
groups
users
who
w
pwd
ls -la
find ~ -maxdepth 2
tree -L 2
history
cat ~/.bash_history
cat ~/.zsh_history
grep -i password ~/.bash_history
grep -i ssh ~/.bash_history
ls -la ~/.ssh
cat ~/.ssh/config
cat ~/.ssh/known_hosts
cat ~/.ssh/authorized_keys
find /home -name id_rsa
find /home -name '*.pem'
find /etc -name '*.conf'
find /etc -name '*.cnf'
find /etc -name '*.ini'
grep -Ri password /etc 2>/dev/null
grep -Ri secret /etc 2>/dev/null
env
printenv
echo $PATH
printenv | grep -i token
printenv | grep -i key
printenv | grep -i secret
find /var/www -name '.env'
find /var/www -name 'config.php'
find /var/www -name 'wp-config.php'
find /var/www -name 'settings.py'
find /opt -name '.env'
find / -name my.cnf 2>/dev/null
find / -name pg_hba.conf 2>/dev/null
find / -name redis.conf 2>/dev/null
find / -name '*.db' 2>/dev/null
find /home -iname '*password*'
find /home -iname '*secret*'
find /home -iname '*token*'
find /home -iname '*.kdbx'
find /home -iname '*.ovpn'
cat ~/.bashrc
cat ~/.bash_profile
cat ~/.profile
cat ~/.zprofile
cat ~/.zshrc
find / -name 'ssh_config'
find / -name 'ssh_config.d'
find / -name 'ssh_known_hosts'
find / -name 'ssh_host_*'
find / -name 'ssh_private_key'
```

### Command Execution Results

| # | Command | Response (truncated) |
|---|---------|----------------------|
| 1 | `whoami` | whoami [4lroot [4hroot@localhost:~#  |
| 2 | `id` | id [4luid=0(root) gid=0(root) groups=0(root) [4hroot@localhost:~#  |
| 3 | `groups` | groups [4lroot  [4hroot@localhost:~#  |
| 4 | `users` | users [4lroot [4hroot@localhost:~#  |
| 5 | `who` | who [4lroot     pts/0        2026-09-10 11:29 (192.168.56.1) [4hroot@localho |
| 6 | `w` | w [4l 11:30:05 up 2 min,  1 user,  load average: 0.00, 0.00, 0.00 USER     TT |
| 7 | `pwd` | pwd [4l/root [4hroot@localhost:~#  |
| 8 | `ls -la` | ls -la [4ldrwx------ 1 root root 4096 2024-06-11 20:00 . drwxr-xr-x 1 root ro |
| 9 | `find ~ -maxdepth 2` | find ~ -maxdepth 2 [4l[4hroot@localhost:~#  |
| 10 | `tree -L 2` | tree -L 2 -bash: tree: command not found root@localhost:~#  |
| 11 | `history` | history [4l    1  whoami     2  id     3  groups     4  users     5  who  |
| 12 | `cat ~/.bash_history` | cat ~/.bash_history [4lcat: ~/.bash_history: No such file or directory [4hro |
| 13 | `cat ~/.zsh_history` | cat ~/.zsh_history [4lcat: ~/.zsh_history: No such file or directory [4hroot |
| 14 | `grep -i password ~/.bash_history` | grep -i password ~/.bash_history [4lgrep: /root/.bash_history: No such file or |
| 15 | `grep -i ssh ~/.bash_history` | grep -i ssh ~/.bash_history [4lgrep: /root/.bash_history: No such file or dire |
| 16 | `ls -la ~/.ssh` | ls -la ~/.ssh [4lls: cannot access /root/.ssh: No such file or directory [4h |
| 17 | `cat ~/.ssh/config` | cat ~/.ssh/config [4lcat: ~/.ssh/config: No such file or directory [4hroot@l |
| 18 | `cat ~/.ssh/known_hosts` | cat ~/.ssh/known_hosts [4lcat: ~/.ssh/known_hosts: No such file or directory  |
| 19 | `cat ~/.ssh/authorized_keys` | cat ~/.ssh/authorized_keys [4lcat: ~/.ssh/authorized_keys: No such file or dir |
| 20 | `find /home -name id_rsa` | find /home -name id_rsa [4l[4hroot@localhost:~#  |
| 21 | `find /home -name '*.pem'` | find /home -name '*.pem' [4l[4hroot@localhost:~#  |
| 22 | `find /etc -name '*.conf'` | find /etc -name '*.conf' [4l/etc/xattr.conf /etc/selinux/semanage.conf /etc/ |
| 23 | `find /etc -name '*.cnf'` | find /etc -name '*.cnf' [4l[4hroot@localhost:~#  |
| 24 | `find /etc -name '*.ini'` | find /etc -name '*.ini' [4l[4hroot@localhost:~#  |
| 25 | `grep -Ri password /etc 2>/dev/null` | grep -Ri password /etc 2>/dev/null [4l[4hroot@localhost:~#  |
| 26 | `grep -Ri secret /etc 2>/dev/null` | grep -Ri secret /etc 2>/dev/null [4l[4hroot@localhost:~#  |
| 27 | `env` | env [4lHOME=/root LOGNAME=root SHELL=/bin/bash SHLVL=1 TMOUT=1800 UID=0  |
| 28 | `printenv` | printenv [4l-bash: /usr/bin/printenv: cannot execute binary file: Exec format  |
| 29 | `echo $PATH` | echo $PATH [4l/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin [ |
| 30 | `printenv \| grep -i token` | printenv \| grep -i token [4l-bash: /usr/bin/printenv: cannot execute binary fi |
| 31 | `printenv \| grep -i key` | printenv \| grep -i key [4l-bash: /usr/bin/printenv: cannot execute binary file |
| 32 | `printenv \| grep -i secret` | printenv \| grep -i secret [4l-bash: /usr/bin/printenv: cannot execute binary f |
| 33 | `find /var/www -name '.env'` | find /var/www -name '.env' [4l[4hroot@localhost:~#  |
| 34 | `find /var/www -name 'config.php'` | find /var/www -name 'config.php' [4l[4hroot@localhost:~#  |
| 35 | `find /var/www -name 'wp-config.php'` | find /var/www -name 'wp-config.php' [4l[4hroot@localhost:~#  |
| 36 | `find /var/www -name 'settings.py'` | find /var/www -name 'settings.py' [4l[4hroot@localhost:~#  |
| 37 | `find /opt -name '.env'` | find /opt -name '.env' [4l[4hroot@localhost:~#  |
| 38 | `find / -name my.cnf 2>/dev/null` |  |
| 39 | `find / -name pg_hba.conf 2>/dev/null` |  |
| 40 | `find / -name redis.conf 2>/dev/null` |  |
| 41 | `find / -name '*.db' 2>/dev/null` |  |
| 42 | `find /home -iname '*password*'` |  |
| 43 | `find /home -iname '*secret*'` |  |
| 44 | `find /home -iname '*token*'` |  |
| 45 | `find /home -iname '*.kdbx'` |  |
| 46 | `find /home -iname '*.ovpn'` |  |
| 47 | `cat ~/.bashrc` |  |
| 48 | `cat ~/.bash_profile` |  |
| 49 | `cat ~/.profile` |  |
| 50 | `cat ~/.zprofile` |  |
| 51 | `cat ~/.zshrc` |  |
| 52 | `find / -name 'ssh_config'` |  |
| 53 | `find / -name 'ssh_config.d'` |  |
| 54 | `find / -name 'ssh_known_hosts'` |  |
| 55 | `find / -name 'ssh_host_*'` |  |
| 56 | `find / -name 'ssh_private_key'` |  |

---

## Cowrie Log Sample (first 20 events)

```json
[
  {
    "session": "b7e50489010f",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 53052,
    "dst_ip": "192.168.56.102",
    "dst_port": 2222,
    "eventid": "cowrie.session.connect",
    "sensor": "kali",
    "uuid": "b7a15396-8fb7-11f1-9021-08002717ff2b",
    "timestamp": "2026-09-10T11:29:26.192348Z",
    "message": "New connection: 192.168.56.1:53052 (192.168.56.102:2222) [session: b7e50489010f]"
  },
  {
    "session": "b7e50489010f",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 53052,
    "dst_ip": "192.168.56.102",
    "dst_port": 2222,
    "version": "SSH-2.0-paramiko_3.4.0",
    "eventid": "cowrie.client.version",
    "sensor": "kali",
    "uuid": "b7a15396-8fb7-11f1-9021-08002717ff2b",
    "timestamp": "2026-09-10T11:29:26.203362Z",
    "message": "Remote SSH version: SSH-2.0-paramiko_3.4.0"
  },
  {
    "session": "b7e50489010f",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 53052,
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
    "timestamp": "2026-09-10T11:29:26.210800Z",
    "message": "SSH client hassh fingerprint: 87e3d9ffee0540b0390f8a5b9c343c08"
  },
  {
    "session": "b7e50489010f",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 53052,
    "dst_ip": "192.168.56.102",
    "dst_port": 2222,
    "username": "root",
    "password": "password",
    "eventid": "cowrie.login.success",
    "sensor": "kali",
    "uuid": "b7a15396-8fb7-11f1-9021-08002717ff2b",
    "timestamp": "2026-09-10T11:29:26.314723Z",
    "message": "login attempt [root/password] succeeded"
  },
  {
    "session": "b7e50489010f",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 53052,
    "dst_ip": "192.168.56.102",
    "dst_port": 2222,
    "width": 80,
    "height": 24,
    "eventid": "cowrie.client.size",
    "sensor": "kali",
    "uuid": "b7a15396-8fb7-11f1-9021-08002717ff2b",
    "timestamp": "2026-09-10T11:29:26.330320Z",
    "message": "Terminal Size: 80 24"
  },
  {
    "session": "b7e50489010f",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 53052,
    "dst_ip": "192.168.56.102",
    "dst_port": 2222,
    "arch": "linux-x64-lsb",
    "eventid": "cowrie.session.params",
    "sensor": "kali",
    "uuid": "b7a15396-8fb7-11f1-9021-08002717ff2b",
    "timestamp": "2026-09-10T11:29:26.340095Z",
    "message": ""
  },
  {
    "session": "b7e50489010f",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 53052,
    "dst_ip": "192.168.56.102",
    "dst_port": 2222,
    "input": "whoami",
    "eventid": "cowrie.command.input",
    "sensor": "kali",
    "uuid": "b7a15396-8fb7-11f1-9021-08002717ff2b",
    "timestamp": "2026-09-10T11:29:33.355422Z",
    "message": "CMD: whoami"
  },
  {
    "session": "b7e50489010f",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 53052,
    "dst_ip": "192.168.56.102",
    "dst_port": 2222,
    "input": "id",
    "eventid": "cowrie.command.input",
    "sensor": "kali",
    "uuid": "b7a15396-8fb7-11f1-9021-08002717ff2b",
    "timestamp": "2026-09-10T11:29:39.868241Z",
    "message": "CMD: id"
  },
  {
    "session": "b7e50489010f",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 53052,
    "dst_ip": "192.168.56.102",
    "dst_port": 2222,
    "input": "groups",
    "eventid": "cowrie.command.input",
    "sensor": "kali",
    "uuid": "b7a15396-8fb7-11f1-9021-08002717ff2b",
    "timestamp": "2026-09-10T11:29:46.380183Z",
    "message": "CMD: groups"
  },
  {
    "session": "b7e50489010f",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 53052,
    "dst_ip": "192.168.56.102",
    "dst_port": 2222,
    "input": "users",
    "eventid": "cowrie.command.input",
    "sensor": "kali",
    "uuid": "b7a15396-8fb7-11f1-9021-08002717ff2b",
    "timestamp": "2026-09-10T11:29:52.899457Z",
    "message": "CMD: users"
  },
  {
    "session": "b7e50489010f",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 53052,
    "dst_ip": "192.168.56.102",
    "dst_port": 2222,
    "input": "who",
    "eventid": "cowrie.command.input",
    "sensor": "kali",
    "uuid": "b7a15396-8fb7-11f1-9021-08002717ff2b",
    "timestamp": "2026-09-10T11:29:59.404448Z",
    "message": "CMD: who"
  },
  {
    "session": "b7e50489010f",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 53052,
    "dst_ip": "192.168.56.102",
    "dst_port": 2222,
    "input": "w",
    "eventid": "cowrie.command.input",
    "sensor": "kali",
    "uuid": "b7a15396-8fb7-11f1-9021-08002717ff2b",
    "timestamp": "2026-09-10T11:30:05.913810Z",
    "message": "CMD: w"
  },
  {
    "session": "b7e50489010f",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 53052,
    "dst_ip": "192.168.56.102",
    "dst_port": 2222,
    "input": "pwd",
    "eventid": "cowrie.command.input",
    "sensor": "kali",
    "uuid": "b7a15396-8fb7-11f1-9021-08002717ff2b",
    "timestamp": "2026-09-10T11:30:12.424558Z",
    "message": "CMD: pwd"
  },
  {
    "session": "b7e50489010f",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 53052,
    "dst_ip": "192.168.56.102",
    "dst_port": 2222,
    "input": "ls -la",
    "eventid": "cowrie.command.input",
    "sensor": "kali",
    "uuid": "b7a15396-8fb7-11f1-9021-08002717ff2b",
    "timestamp": "2026-09-10T11:30:18.944683Z",
    "message": "CMD: ls -la"
  },
  {
    "session": "b7e50489010f",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 53052,
    "dst_ip": "192.168.56.102",
    "dst_port": 2222,
    "input": "find ~ -maxdepth 2",
    "eventid": "cowrie.command.input",
    "sensor": "kali",
    "uuid": "b7a15396-8fb7-11f1-9021-08002717ff2b",
    "timestamp": "2026-09-10T11:30:25.450617Z",
    "message": "CMD: find ~ -maxdepth 2"
  },
  {
    "session": "b7e50489010f",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 53052,
    "dst_ip": "192.168.56.102",
    "dst_port": 2222,
    "input": "tree -L 2",
    "eventid": "cowrie.command.input",
    "sensor": "kali",
    "uuid": "b7a15396-8fb7-11f1-9021-08002717ff2b",
    "timestamp": "2026-09-10T11:30:31.966171Z",
    "message": "CMD: tree -L 2"
  },
  {
    "session": "b7e50489010f",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 53052,
    "dst_ip": "192.168.56.102",
    "dst_port": 2222,
    "input": "tree -L 2",
    "eventid": "cowrie.command.failed",
    "sensor": "kali",
    "uuid": "b7a15396-8fb7-11f1-9021-08002717ff2b",
    "timestamp": "2026-09-10T11:30:31.973585Z",
    "message": "Command not found: tree -L 2"
  },
  {
    "session": "b7e50489010f",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 53052,
    "dst_ip": "192.168.56.102",
    "dst_port": 2222,
    "input": "history",
    "eventid": "cowrie.command.input",
    "sensor": "kali",
    "uuid": "b7a15396-8fb7-11f1-9021-08002717ff2b",
    "timestamp": "2026-09-10T11:30:38.477928Z",
    "message": "CMD: history"
  },
  {
    "session": "b7e50489010f",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 53052,
    "dst_ip": "192.168.56.102",
    "dst_port": 2222,
    "input": "cat ~/.bash_history",
    "eventid": "cowrie.command.input",
    "sensor": "kali",
    "uuid": "b7a15396-8fb7-11f1-9021-08002717ff2b",
    "timestamp": "2026-09-10T11:30:44.992494Z",
    "message": "CMD: cat ~/.bash_history"
  },
  {
    "session": "b7e50489010f",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 53052,
    "dst_ip": "192.168.56.102",
    "dst_port": 2222,
    "input": "cat ~/.zsh_history",
    "eventid": "cowrie.command.input",
    "sensor": "kali",
    "uuid": "b7a15396-8fb7-11f1-9021-08002717ff2b",
    "timestamp": "2026-09-10T11:30:51.505461Z",
    "message": "CMD: cat ~/.zsh_history"
  }
]
```

---
*Generated by LLM-based Cowrie Honeypot Evaluator*
