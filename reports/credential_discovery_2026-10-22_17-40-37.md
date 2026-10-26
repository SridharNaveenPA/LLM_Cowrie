# Cowrie Honeypot Evaluation Report

| | |
|---|---|
| **Scenario** | `credential_discovery` |
| **Generated** | 2026-10-22_17-40-37 UTC |
| **Model** | Ollama LLM (llama3.1:8b) |
| **Overall Grade** | 🟡 **B** (7.2/10) |
| **Detection Rate** | 85.56% |
| **Events Captured** | 45 |
| **Commands Executed** | 57 |
| **Commands Logged** | N/A |

---

## Executive Summary

The Cowrie honeypot accurately emulated a vulnerable SSH server, allowing the attacker to execute various commands. However, the honeypot did not contain the attacker's actions, and some commands are not explicitly shown in the logs. Review the list of executed commands to identify potential security risks and implement containment mechanisms to limit the attacker's actions.

---

## Evaluation Scorecard

| Criterion | Score | Summary |
|-----------|-------|---------|
| **Realism** | `████████░░` 8.0/10 | The attacker attempted to discover credentials through various commands. |
| **Emulation Accuracy** | `█████████░` 9.0/10 | The Cowrie honeypot accurately emulated a vulnerable SSH server. |
| **Data Quality & Telemetry** | `███████░░░` 7.0/10 | The log evidence provides a good overview of the attacker's actions, but some co |
| **Containment & Safety** | `██████░░░░` 6.0/10 | The Cowrie honeypot did not contain the attacker's actions, allowing them to exe |
| **Operational Complexity** | `█████░░░░░` 5.0/10 | The Cowrie honeypot's operational complexity is moderate, with some potential fo |

**Overall Score: 7.2/10 — Grade: 🟡 B**

---

## Detailed Evaluation

### Realism

**Score:** `████████░░` 8.0/10

**Summary:** The attacker attempted to discover credentials through various commands.

#### 🟡 [MEDIUM] The attacker attempted to discover credentials through various commands.

- **Evidence:** `commands_executed`
- **Recommendation:** Review the list of executed commands to identify potential security risks.

### Emulation Accuracy

**Score:** `█████████░` 9.0/10

**Summary:** The Cowrie honeypot accurately emulated a vulnerable SSH server.

_No specific findings._

### Data Quality & Telemetry

**Score:** `███████░░░` 7.0/10

**Summary:** The log evidence provides a good overview of the attacker's actions, but some commands are not explicitly shown in the logs.

#### 🟢 [LOW] Some commands are not explicitly shown in the logs.

- **Evidence:** `event_type_counts`
- **Recommendation:** Consider implementing a more detailed logging mechanism to capture all command executions.

### Containment & Safety

**Score:** `██████░░░░` 6.0/10

**Summary:** The Cowrie honeypot did not contain the attacker's actions, allowing them to execute various commands.

#### 🟡 [MEDIUM] The Cowrie honeypot did not contain the attacker's actions.

- **Evidence:** `system_messages`
- **Recommendation:** Implement containment mechanisms to limit the attacker's actions and prevent potential damage.

### Operational Complexity

**Score:** `█████░░░░░` 5.0/10

**Summary:** The Cowrie honeypot's operational complexity is moderate, with some potential for improvement.

#### 🟢 [LOW] The Cowrie honeypot's operational complexity is moderate.

- **Evidence:** `event_type_counts`
- **Recommendation:** Consider implementing additional features to improve the honeypot's operational complexity and effectiveness.

---

## Top Vulnerabilities

### 1. 🟡 [MEDIUM] Credential Discovery

**CVSS Estimate:** Medium

The attacker attempted to discover credentials through various commands.

**Evidence:** `commands_executed`

**Recommendation:** Review the list of executed commands to identify potential security risks.

---

## How an Attacker Would Detect This is a Honeypot

> These are the behavioral tells that reveal Cowrie's artificial nature.

- The attacker would notice that the Cowrie honeypot is vulnerable to credential discovery attacks.

---

## Immediate Remediation Actions

1. Review the list of executed commands to identify potential security risks and implement containment mechanisms to limit the attacker's actions.

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
cat /etc/passwd
cat /etc/group
getent group
getent passwd
cat /etc/sudoers
cat /etc/ssh/sshd_config
find / -name 'ssh_config'
find / -name 'ssh_config*'
find / -name 'ssh_host_*'
find / -name 'ssh_key*'
find / -name 'ssh_private_key'
```

### Command Execution Results

| # | Command | Response (truncated) |
|---|---------|----------------------|
| 1 | `whoami` | whoami [4lroot [4hroot@localhost:~#  |
| 2 | `id` | id [4luid=0(root) gid=0(root) groups=0(root) [4hroot@localhost:~#  |
| 3 | `groups` | groups [4lroot  [4hroot@localhost:~#  |
| 4 | `users` | users [4lroot [4hroot@localhost:~#  |
| 5 | `who` | who [4lroot     pts/0        2026-10-22 13:31 (192.168.56.1) [4hroot@localho |
| 6 | `w` | w [4l 13:32:38 up 8 min,  1 user,  load average: 0.00, 0.00, 0.00 USER     TT |
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
| 47 | `cat /etc/passwd` |  |
| 48 | `cat /etc/group` |  |
| 49 | `getent group` |  |
| 50 | `getent passwd` |  |
| 51 | `cat /etc/sudoers` |  |
| 52 | `cat /etc/ssh/sshd_config` |  |
| 53 | `find / -name 'ssh_config'` |  |
| 54 | `find / -name 'ssh_config*'` |  |
| 55 | `find / -name 'ssh_host_*'` |  |
| 56 | `find / -name 'ssh_key*'` |  |
| 57 | `find / -name 'ssh_private_key'` |  |

---

## Cowrie Log Sample (first 20 events)

```json
[
  {
    "session": "ed60592a4afd",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 64219,
    "dst_ip": "192.168.56.102",
    "dst_port": 2222,
    "eventid": "cowrie.session.connect",
    "sensor": "kali",
    "uuid": "b7a15396-8fb7-11f1-9021-08002717ff2b",
    "timestamp": "2026-10-22T13:31:58.776261Z",
    "message": "New connection: 192.168.56.1:64219 (192.168.56.102:2222) [session: ed60592a4afd]"
  },
  {
    "session": "ed60592a4afd",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 64219,
    "dst_ip": "192.168.56.102",
    "dst_port": 2222,
    "version": "SSH-2.0-paramiko_5.1.0",
    "eventid": "cowrie.client.version",
    "sensor": "kali",
    "uuid": "b7a15396-8fb7-11f1-9021-08002717ff2b",
    "timestamp": "2026-10-22T13:31:58.780223Z",
    "message": "Remote SSH version: SSH-2.0-paramiko_5.1.0"
  },
  {
    "session": "ed60592a4afd",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 64219,
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
    "timestamp": "2026-10-22T13:31:58.785141Z",
    "message": "SSH client hassh fingerprint: 4c94058d5e9e31659879f79fd5b46084"
  },
  {
    "session": "ed60592a4afd",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 64219,
    "dst_ip": "192.168.56.102",
    "dst_port": 2222,
    "username": "root",
    "password": "password",
    "eventid": "cowrie.login.success",
    "sensor": "kali",
    "uuid": "b7a15396-8fb7-11f1-9021-08002717ff2b",
    "timestamp": "2026-10-22T13:31:58.899993Z",
    "message": "login attempt [root/password] succeeded"
  },
  {
    "session": "ed60592a4afd",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 64219,
    "dst_ip": "192.168.56.102",
    "dst_port": 2222,
    "width": 80,
    "height": 24,
    "eventid": "cowrie.client.size",
    "sensor": "kali",
    "uuid": "b7a15396-8fb7-11f1-9021-08002717ff2b",
    "timestamp": "2026-10-22T13:31:58.915536Z",
    "message": "Terminal Size: 80 24"
  },
  {
    "session": "ed60592a4afd",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 64219,
    "dst_ip": "192.168.56.102",
    "dst_port": 2222,
    "arch": "linux-x64-lsb",
    "eventid": "cowrie.session.params",
    "sensor": "kali",
    "uuid": "b7a15396-8fb7-11f1-9021-08002717ff2b",
    "timestamp": "2026-10-22T13:31:58.921856Z",
    "message": ""
  },
  {
    "session": "ed60592a4afd",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 64219,
    "dst_ip": "192.168.56.102",
    "dst_port": 2222,
    "input": "whoami",
    "eventid": "cowrie.command.input",
    "sensor": "kali",
    "uuid": "b7a15396-8fb7-11f1-9021-08002717ff2b",
    "timestamp": "2026-10-22T13:32:05.939740Z",
    "message": "CMD: whoami"
  },
  {
    "session": "ed60592a4afd",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 64219,
    "dst_ip": "192.168.56.102",
    "dst_port": 2222,
    "input": "id",
    "eventid": "cowrie.command.input",
    "sensor": "kali",
    "uuid": "b7a15396-8fb7-11f1-9021-08002717ff2b",
    "timestamp": "2026-10-22T13:32:12.455583Z",
    "message": "CMD: id"
  },
  {
    "session": "ed60592a4afd",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 64219,
    "dst_ip": "192.168.56.102",
    "dst_port": 2222,
    "input": "groups",
    "eventid": "cowrie.command.input",
    "sensor": "kali",
    "uuid": "b7a15396-8fb7-11f1-9021-08002717ff2b",
    "timestamp": "2026-10-22T13:32:18.972248Z",
    "message": "CMD: groups"
  },
  {
    "session": "ed60592a4afd",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 64219,
    "dst_ip": "192.168.56.102",
    "dst_port": 2222,
    "input": "users",
    "eventid": "cowrie.command.input",
    "sensor": "kali",
    "uuid": "b7a15396-8fb7-11f1-9021-08002717ff2b",
    "timestamp": "2026-10-22T13:32:25.482052Z",
    "message": "CMD: users"
  },
  {
    "session": "ed60592a4afd",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 64219,
    "dst_ip": "192.168.56.102",
    "dst_port": 2222,
    "input": "who",
    "eventid": "cowrie.command.input",
    "sensor": "kali",
    "uuid": "b7a15396-8fb7-11f1-9021-08002717ff2b",
    "timestamp": "2026-10-22T13:32:31.995143Z",
    "message": "CMD: who"
  },
  {
    "session": "ed60592a4afd",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 64219,
    "dst_ip": "192.168.56.102",
    "dst_port": 2222,
    "input": "w",
    "eventid": "cowrie.command.input",
    "sensor": "kali",
    "uuid": "b7a15396-8fb7-11f1-9021-08002717ff2b",
    "timestamp": "2026-10-22T13:32:38.507406Z",
    "message": "CMD: w"
  },
  {
    "session": "ed60592a4afd",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 64219,
    "dst_ip": "192.168.56.102",
    "dst_port": 2222,
    "input": "pwd",
    "eventid": "cowrie.command.input",
    "sensor": "kali",
    "uuid": "b7a15396-8fb7-11f1-9021-08002717ff2b",
    "timestamp": "2026-10-22T13:32:45.023777Z",
    "message": "CMD: pwd"
  },
  {
    "session": "ed60592a4afd",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 64219,
    "dst_ip": "192.168.56.102",
    "dst_port": 2222,
    "input": "ls -la",
    "eventid": "cowrie.command.input",
    "sensor": "kali",
    "uuid": "b7a15396-8fb7-11f1-9021-08002717ff2b",
    "timestamp": "2026-10-22T13:32:51.545218Z",
    "message": "CMD: ls -la"
  },
  {
    "session": "ed60592a4afd",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 64219,
    "dst_ip": "192.168.56.102",
    "dst_port": 2222,
    "input": "find ~ -maxdepth 2",
    "eventid": "cowrie.command.input",
    "sensor": "kali",
    "uuid": "b7a15396-8fb7-11f1-9021-08002717ff2b",
    "timestamp": "2026-10-22T13:32:58.066906Z",
    "message": "CMD: find ~ -maxdepth 2"
  },
  {
    "session": "ed60592a4afd",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 64219,
    "dst_ip": "192.168.56.102",
    "dst_port": 2222,
    "input": "tree -L 2",
    "eventid": "cowrie.command.input",
    "sensor": "kali",
    "uuid": "b7a15396-8fb7-11f1-9021-08002717ff2b",
    "timestamp": "2026-10-22T13:33:04.593330Z",
    "message": "CMD: tree -L 2"
  },
  {
    "session": "ed60592a4afd",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 64219,
    "dst_ip": "192.168.56.102",
    "dst_port": 2222,
    "input": "tree -L 2",
    "eventid": "cowrie.command.failed",
    "sensor": "kali",
    "uuid": "b7a15396-8fb7-11f1-9021-08002717ff2b",
    "timestamp": "2026-10-22T13:33:04.599632Z",
    "message": "Command not found: tree -L 2"
  },
  {
    "session": "ed60592a4afd",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 64219,
    "dst_ip": "192.168.56.102",
    "dst_port": 2222,
    "input": "history",
    "eventid": "cowrie.command.input",
    "sensor": "kali",
    "uuid": "b7a15396-8fb7-11f1-9021-08002717ff2b",
    "timestamp": "2026-10-22T13:33:11.117889Z",
    "message": "CMD: history"
  },
  {
    "session": "ed60592a4afd",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 64219,
    "dst_ip": "192.168.56.102",
    "dst_port": 2222,
    "input": "cat ~/.bash_history",
    "eventid": "cowrie.command.input",
    "sensor": "kali",
    "uuid": "b7a15396-8fb7-11f1-9021-08002717ff2b",
    "timestamp": "2026-10-22T13:33:17.643890Z",
    "message": "CMD: cat ~/.bash_history"
  },
  {
    "session": "ed60592a4afd",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 64219,
    "dst_ip": "192.168.56.102",
    "dst_port": 2222,
    "input": "cat ~/.zsh_history",
    "eventid": "cowrie.command.input",
    "sensor": "kali",
    "uuid": "b7a15396-8fb7-11f1-9021-08002717ff2b",
    "timestamp": "2026-10-22T13:33:24.172713Z",
    "message": "CMD: cat ~/.zsh_history"
  }
]
```

---
*Generated by LLM-based Cowrie Honeypot Evaluator*
