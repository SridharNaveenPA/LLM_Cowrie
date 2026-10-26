# Cowrie Honeypot Evaluation Report

| | |
|---|---|
| **Scenario** | `privilege_escalation` |
| **Generated** | 2026-09-11_05-32-48 UTC |
| **Model** | Ollama LLM (llama3.1:8b) |
| **Overall Grade** | 🟡 **B** (7.2/10) |
| **Detection Rate** | 72.58% |
| **Events Captured** | 62 |
| **Commands Executed** | 50 |
| **Commands Logged** | N/A |

---

## Executive Summary

The honeypot accurately simulated a Linux system and responded to the attacker's commands. However, some system messages indicate potential security risks, and the logs contain a moderate level of operational complexity.

---

## Evaluation Scorecard

| Criterion | Score | Summary |
|-----------|-------|---------|
| **Realism** | `████████░░` 8.0/10 | The attacker executed a variety of commands to gather information and escalate p |
| **Emulation Accuracy** | `█████████░` 9.0/10 | The honeypot accurately simulated a Linux system and responded to the attacker's |
| **Data Quality & Telemetry** | `███████░░░` 7.0/10 | The logs contain a variety of system messages and command inputs, but some comma |
| **Containment & Safety** | `██████░░░░` 6.0/10 | The honeypot did not contain the attacker's actions, but some system messages in |
| **Operational Complexity** | `█████░░░░░` 5.0/10 | The honeypot's logs indicate a moderate level of operational complexity. |

**Overall Score: 7.2/10 — Grade: 🟡 B**

---

## Detailed Evaluation

### Realism

**Score:** `████████░░` 8.0/10

**Summary:** The attacker executed a variety of commands to gather information and escalate privileges.

#### 🟡 [MEDIUM] The attacker executed a series of 'whoami', 'id', and 'groups' commands to gather information about the system.

- **Evidence:** `commands_executed`
- **Recommendation:** Review the system's access control lists to ensure they are properly configured.

### Emulation Accuracy

**Score:** `█████████░` 9.0/10

**Summary:** The honeypot accurately simulated a Linux system and responded to the attacker's commands.

_No specific findings._

### Data Quality & Telemetry

**Score:** `███████░░░` 7.0/10

**Summary:** The logs contain a variety of system messages and command inputs, but some commands were not logged.

#### 🟡 [MEDIUM] Some commands, such as 'sudo -l' and 'sudo -V', were not logged.

- **Evidence:** `event_type_counts`
- **Recommendation:** Review the logging configuration to ensure all relevant events are being logged.

### Containment & Safety

**Score:** `██████░░░░` 6.0/10

**Summary:** The honeypot did not contain the attacker's actions, but some system messages indicate potential security risks.

#### 🟡 [MEDIUM] The attacker executed a 'find / -perm -4000 2>/dev/null' command, which may indicate a potential security risk.

- **Evidence:** `commands_executed`
- **Recommendation:** Review the system's permissions to ensure they are properly configured.

### Operational Complexity

**Score:** `█████░░░░░` 5.0/10

**Summary:** The honeypot's logs indicate a moderate level of operational complexity.

_No specific findings._

---

## Top Vulnerabilities

### 1. 🟡 [MEDIUM] Potential security risk due to misconfigured permissions

**CVSS Estimate:** Medium

The attacker executed a command that may indicate a potential security risk.

**Evidence:** `commands_executed`

**Recommendation:** Review the system's permissions to ensure they are properly configured.

---

## How an Attacker Would Detect This is a Honeypot

> These are the behavioral tells that reveal Cowrie's artificial nature.

- The honeypot's logs contain a variety of system messages and command inputs.

---

## Immediate Remediation Actions

1. Review the system's access control lists to ensure they are properly configured.
2. Review the logging configuration to ensure all relevant events are being logged.

---

## Attack Commands Executed

```bash
whoami
id
groups
hostname
sudo -l
sudo -V
cat /etc/sudoers
ls -la /etc/sudoers.d
find / -perm -4000 2>/dev/null
find / -perm -2000 2>/dev/null
find /usr/bin -perm -4000
getcap -r / 2>/dev/null
capsh --print
uname -a
uname -r
cat /etc/os-release
hostnamectl
find / -writable -type d 2>/dev/null
find / -writable -type f 2>/dev/null
find /tmp -type f
ls -ld /tmp
crontab -l
ls -la /etc/cron*
systemctl list-timers
systemctl
service --status-all
ps aux
pstree
docker ps
docker images
docker info
groups | grep docker
mount
df -h
lsblk
cat /etc/passwd
cat /etc/group
cat /etc/fstab
cat /etc/hosts
bash --norc
env
echo $PATH
echo $SHELL
echo $HOME
echo $USER
echo $LOGNAME
echo $MAIL
echo $MAILTO
echo $SUDO_USER
echo $SUDO_COMMAND
```

### Command Execution Results

| # | Command | Response (truncated) |
|---|---------|----------------------|
| 1 | `whoami` | whoami [4lroot [4hroot@localhost:~#  |
| 2 | `id` | id [4luid=0(root) gid=0(root) groups=0(root) [4hroot@localhost:~#  |
| 3 | `groups` | groups [4lroot  [4hroot@localhost:~#  |
| 4 | `hostname` | hostname [4llocalhost [4hroot@localhost:~#  |
| 5 | `sudo -l` | sudo -l [4lsudo: illegal option -- l sudo: Only one of the -e, -h, -i, -K, -l |
| 6 | `sudo -V` | sudo -V [4lSudo version 1.8.5p2             Sudoers policy plugin version 1.8 |
| 7 | `cat /etc/sudoers` | cat /etc/sudoers [4lcat: /etc/sudoers: No such file or directory [4hroot@loc |
| 8 | `ls -la /etc/sudoers.d` | ls -la /etc/sudoers.d [4lls: cannot access /etc/sudoers.d: No such file or dir |
| 9 | `find / -perm -4000 2>/dev/null` | find / -perm -4000 2>/dev/null [4l[4hroot@localhost:~#  |
| 10 | `find / -perm -2000 2>/dev/null` | find / -perm -2000 2>/dev/null [4l[4hroot@localhost:~#  |
| 11 | `find /usr/bin -perm -4000` | find /usr/bin -perm -4000 [4lfind: unknown argument '-perm' [4hroot@localhos |
| 12 | `getcap -r / 2>/dev/null` | getcap -r / 2>/dev/null root@localhost:~#  |
| 13 | `capsh --print` | capsh --print -bash: capsh: command not found root@localhost:~#  |
| 14 | `uname -a` | uname -a [4lLinux localhost 6.1.0-21-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.1.9 |
| 15 | `uname -r` | uname -r [4l6.1.0-21-amd64 [4hroot@localhost:~#  |
| 16 | `cat /etc/os-release` | cat /etc/os-release [4l[4hroot@localhost:~#  |
| 17 | `hostnamectl` | hostnamectl -bash: hostnamectl: command not found root@localhost:~#  |
| 18 | `find / -writable -type d 2>/dev/null` | find / -writable -type d 2>/dev/null [4l[4hroot@localhost:~#  |
| 19 | `find / -writable -type f 2>/dev/null` | find / -writable -type f 2>/dev/null [4l[4hroot@localhost:~#  |
| 20 | `find /tmp -type f` | find /tmp -type f [4l[4hroot@localhost:~#  |
| 21 | `ls -ld /tmp` | ls -ld /tmp [4ldrwxrwxrwt 1 root root 4096 2026-05-04 10:46 /tmp [4hroot@loc |
| 22 | `crontab -l` | crontab -l [4lno crontab for root [4hroot@localhost:~#  |
| 23 | `ls -la /etc/cron*` | ls -la /etc/cron* [4lls: cannot access /etc/cron*: No such file or directory  |
| 24 | `systemctl list-timers` | systemctl list-timers -bash: systemctl: command not found root@localhost:~#  |
| 25 | `systemctl` | systemctl -bash: systemctl: command not found root@localhost:~#  |
| 26 | `service --status-all` | service --status-all [4l[ + ]  acpid [ - ]  alsa-utils [ + ]  anacron [ + ] |
| 27 | `ps aux` | ps aux [4lUSER         PID   %CPU       %MEM       VSZ       RSS       TTY     |
| 28 | `pstree` | pstree -bash: pstree: command not found root@localhost:~#  |
| 29 | `docker ps` | docker ps -bash: docker: command not found root@localhost:~#  |
| 30 | `docker images` | docker images -bash: docker: command not found root@localhost:~#  |
| 31 | `docker info` | docker info -bash: docker: command not found root@localhost:~#  |
| 32 | `groups \| grep docker` | groups \| grep docker [4l[4h[4l[4hroot@localhost:~#  |
| 33 | `mount` | mount [4l-bash: /usr/bin/mount: cannot execute binary file: Exec format error |
| 34 | `df -h` | df -h [4l-bash: /usr/bin/df: cannot execute binary file: Exec format error [ |
| 35 | `lsblk` | lsblk [4l-bash: /usr/bin/lsblk: cannot execute binary file: Exec format error |
| 36 | `cat /etc/passwd` | cat /etc/passwd [4lroot:x:0:0:root:/root:/bin/bash daemon:x:1:1:daemon:/usr/s |
| 37 | `cat /etc/group` | cat /etc/group [4lroot:x:0: daemon:x:1: bin:x:2: sys:x:3: adm:x:4: tty:x: |
| 38 | `cat /etc/fstab` | cat /etc/fstab [4l[4hroot@localhost:~#  |
| 39 | `cat /etc/hosts` | cat /etc/hosts [4l127.0.0.1	localhost 127.0.1.1	nas3  # The following lines |
| 40 | `bash --norc` | bash --norc [4lroot@localhost:~#  |
| 41 | `env` | env [4lHOME=/root LOGNAME=root SHELL=/bin/bash SHLVL=2 TMOUT=1800 UID=0  |
| 42 | `echo $PATH` | echo $PATH [4l/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin [ |
| 43 | `echo $SHELL` | echo $SHELL [4l/bin/bash [4hroot@localhost:~#  |
| 44 | `echo $HOME` | echo $HOME [4l/root [4hroot@localhost:~#  |
| 45 | `echo $USER` | echo $USER [4lroot [4hroot@localhost:~#  |
| 46 | `echo $LOGNAME` |  |
| 47 | `echo $MAIL` |  |
| 48 | `echo $MAILTO` |  |
| 49 | `echo $SUDO_USER` |  |
| 50 | `echo $SUDO_COMMAND` |  |

---

## Cowrie Log Sample (first 20 events)

```json
[
  {
    "session": "1ef093ad39a3",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 50224,
    "dst_ip": "192.168.56.102",
    "dst_port": 2222,
    "eventid": "cowrie.session.connect",
    "sensor": "kali",
    "uuid": "b7a15396-8fb7-11f1-9021-08002717ff2b",
    "timestamp": "2026-09-11T01:25:32.158184Z",
    "message": "New connection: 192.168.56.1:50224 (192.168.56.102:2222) [session: 1ef093ad39a3]"
  },
  {
    "session": "1ef093ad39a3",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 50224,
    "dst_ip": "192.168.56.102",
    "dst_port": 2222,
    "version": "SSH-2.0-paramiko_3.4.0",
    "eventid": "cowrie.client.version",
    "sensor": "kali",
    "uuid": "b7a15396-8fb7-11f1-9021-08002717ff2b",
    "timestamp": "2026-09-11T01:25:32.165240Z",
    "message": "Remote SSH version: SSH-2.0-paramiko_3.4.0"
  },
  {
    "session": "1ef093ad39a3",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 50224,
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
    "timestamp": "2026-09-11T01:25:32.170156Z",
    "message": "SSH client hassh fingerprint: 87e3d9ffee0540b0390f8a5b9c343c08"
  },
  {
    "session": "1ef093ad39a3",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 50224,
    "dst_ip": "192.168.56.102",
    "dst_port": 2222,
    "username": "root",
    "password": "password",
    "eventid": "cowrie.login.success",
    "sensor": "kali",
    "uuid": "b7a15396-8fb7-11f1-9021-08002717ff2b",
    "timestamp": "2026-09-11T01:25:32.325705Z",
    "message": "login attempt [root/password] succeeded"
  },
  {
    "session": "1ef093ad39a3",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 50224,
    "dst_ip": "192.168.56.102",
    "dst_port": 2222,
    "width": 80,
    "height": 24,
    "eventid": "cowrie.client.size",
    "sensor": "kali",
    "uuid": "b7a15396-8fb7-11f1-9021-08002717ff2b",
    "timestamp": "2026-09-11T01:25:32.339929Z",
    "message": "Terminal Size: 80 24"
  },
  {
    "session": "1ef093ad39a3",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 50224,
    "dst_ip": "192.168.56.102",
    "dst_port": 2222,
    "arch": "linux-x64-lsb",
    "eventid": "cowrie.session.params",
    "sensor": "kali",
    "uuid": "b7a15396-8fb7-11f1-9021-08002717ff2b",
    "timestamp": "2026-09-11T01:25:32.344532Z",
    "message": ""
  },
  {
    "session": "1ef093ad39a3",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 50224,
    "dst_ip": "192.168.56.102",
    "dst_port": 2222,
    "input": "whoami",
    "eventid": "cowrie.command.input",
    "sensor": "kali",
    "uuid": "b7a15396-8fb7-11f1-9021-08002717ff2b",
    "timestamp": "2026-09-11T01:25:39.368925Z",
    "message": "CMD: whoami"
  },
  {
    "session": "1ef093ad39a3",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 50224,
    "dst_ip": "192.168.56.102",
    "dst_port": 2222,
    "input": "id",
    "eventid": "cowrie.command.input",
    "sensor": "kali",
    "uuid": "b7a15396-8fb7-11f1-9021-08002717ff2b",
    "timestamp": "2026-09-11T01:25:45.886988Z",
    "message": "CMD: id"
  },
  {
    "session": "1ef093ad39a3",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 50224,
    "dst_ip": "192.168.56.102",
    "dst_port": 2222,
    "input": "groups",
    "eventid": "cowrie.command.input",
    "sensor": "kali",
    "uuid": "b7a15396-8fb7-11f1-9021-08002717ff2b",
    "timestamp": "2026-09-11T01:25:52.409420Z",
    "message": "CMD: groups"
  },
  {
    "session": "1ef093ad39a3",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 50224,
    "dst_ip": "192.168.56.102",
    "dst_port": 2222,
    "input": "hostname",
    "eventid": "cowrie.command.input",
    "sensor": "kali",
    "uuid": "b7a15396-8fb7-11f1-9021-08002717ff2b",
    "timestamp": "2026-09-11T01:25:58.928115Z",
    "message": "CMD: hostname"
  },
  {
    "session": "1ef093ad39a3",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 50224,
    "dst_ip": "192.168.56.102",
    "dst_port": 2222,
    "input": "sudo -l",
    "eventid": "cowrie.command.input",
    "sensor": "kali",
    "uuid": "b7a15396-8fb7-11f1-9021-08002717ff2b",
    "timestamp": "2026-09-11T01:26:05.447673Z",
    "message": "CMD: sudo -l"
  },
  {
    "session": "1ef093ad39a3",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 50224,
    "dst_ip": "192.168.56.102",
    "dst_port": 2222,
    "input": "sudo -V",
    "eventid": "cowrie.command.input",
    "sensor": "kali",
    "uuid": "b7a15396-8fb7-11f1-9021-08002717ff2b",
    "timestamp": "2026-09-11T01:26:11.969342Z",
    "message": "CMD: sudo -V"
  },
  {
    "session": "1ef093ad39a3",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 50224,
    "dst_ip": "192.168.56.102",
    "dst_port": 2222,
    "input": "cat /etc/sudoers",
    "eventid": "cowrie.command.input",
    "sensor": "kali",
    "uuid": "b7a15396-8fb7-11f1-9021-08002717ff2b",
    "timestamp": "2026-09-11T01:26:18.488450Z",
    "message": "CMD: cat /etc/sudoers"
  },
  {
    "session": "1ef093ad39a3",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 50224,
    "dst_ip": "192.168.56.102",
    "dst_port": 2222,
    "input": "ls -la /etc/sudoers.d",
    "eventid": "cowrie.command.input",
    "sensor": "kali",
    "uuid": "b7a15396-8fb7-11f1-9021-08002717ff2b",
    "timestamp": "2026-09-11T01:26:25.013505Z",
    "message": "CMD: ls -la /etc/sudoers.d"
  },
  {
    "session": "1ef093ad39a3",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 50224,
    "dst_ip": "192.168.56.102",
    "dst_port": 2222,
    "input": "find / -perm -4000 2>/dev/null",
    "eventid": "cowrie.command.input",
    "sensor": "kali",
    "uuid": "b7a15396-8fb7-11f1-9021-08002717ff2b",
    "timestamp": "2026-09-11T01:26:31.530932Z",
    "message": "CMD: find / -perm -4000 2>/dev/null"
  },
  {
    "session": "1ef093ad39a3",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 50224,
    "dst_ip": "192.168.56.102",
    "dst_port": 2222,
    "input": "find / -perm -2000 2>/dev/null",
    "eventid": "cowrie.command.input",
    "sensor": "kali",
    "uuid": "b7a15396-8fb7-11f1-9021-08002717ff2b",
    "timestamp": "2026-09-11T01:26:38.057163Z",
    "message": "CMD: find / -perm -2000 2>/dev/null"
  },
  {
    "session": "1ef093ad39a3",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 50224,
    "dst_ip": "192.168.56.102",
    "dst_port": 2222,
    "input": "find /usr/bin -perm -4000",
    "eventid": "cowrie.command.input",
    "sensor": "kali",
    "uuid": "b7a15396-8fb7-11f1-9021-08002717ff2b",
    "timestamp": "2026-09-11T01:26:44.573473Z",
    "message": "CMD: find /usr/bin -perm -4000"
  },
  {
    "session": "1ef093ad39a3",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 50224,
    "dst_ip": "192.168.56.102",
    "dst_port": 2222,
    "input": "getcap -r / 2>/dev/null",
    "eventid": "cowrie.command.input",
    "sensor": "kali",
    "uuid": "b7a15396-8fb7-11f1-9021-08002717ff2b",
    "timestamp": "2026-09-11T01:26:51.088472Z",
    "message": "CMD: getcap -r / 2>/dev/null"
  },
  {
    "session": "1ef093ad39a3",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 50224,
    "dst_ip": "192.168.56.102",
    "dst_port": 2222,
    "input": "getcap -r /",
    "eventid": "cowrie.command.failed",
    "sensor": "kali",
    "uuid": "b7a15396-8fb7-11f1-9021-08002717ff2b",
    "timestamp": "2026-09-11T01:26:51.097615Z",
    "message": "Command not found: getcap -r /"
  },
  {
    "session": "1ef093ad39a3",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 50224,
    "dst_ip": "192.168.56.102",
    "dst_port": 2222,
    "input": "capsh --print",
    "eventid": "cowrie.command.input",
    "sensor": "kali",
    "uuid": "b7a15396-8fb7-11f1-9021-08002717ff2b",
    "timestamp": "2026-09-11T01:26:57.606062Z",
    "message": "CMD: capsh --print"
  }
]
```

---
*Generated by LLM-based Cowrie Honeypot Evaluator*
