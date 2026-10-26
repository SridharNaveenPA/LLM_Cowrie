# Cowrie Honeypot Evaluation Report

| | |
|---|---|
| **Scenario** | `privilege_escalation` |
| **Generated** | 2026-09-10_16-00-43 UTC |
| **Model** | Ollama LLM (llama3.1:8b) |
| **Overall Grade** | 🟡 **B** (7.0/10) |
| **Detection Rate** | 75.0% |
| **Events Captured** | 68 |
| **Commands Executed** | 48 |
| **Commands Logged** | N/A |

---

## Executive Summary

The honeypot accurately simulated a Linux system, allowing the attacker to execute various commands. However, some commands executed by the attacker did not generate log entries, and the honeypot did not contain the attacker's actions.

---

## Evaluation Scorecard

| Criterion | Score | Summary |
|-----------|-------|---------|
| **Realism** | `████████░░` 8.0/10 | The attacker executed a variety of commands, including privilege escalation atte |
| **Emulation Accuracy** | `█████████░` 9.0/10 | The honeypot accurately simulated a Linux system, allowing the attacker to execu |
| **Data Quality & Telemetry** | `███████░░░` 7.0/10 | The log data appears to be complete, but some commands executed by the attacker  |
| **Containment & Safety** | `██████░░░░` 6.0/10 | The honeypot did not contain the attacker's actions, allowing them to execute po |
| **Operational Complexity** | `█████░░░░░` 5.0/10 | The honeypot's operational complexity is moderate, with a variety of commands ex |

**Overall Score: 7.0/10 — Grade: 🟡 B**

---

## Detailed Evaluation

### Realism

**Score:** `████████░░` 8.0/10

**Summary:** The attacker executed a variety of commands, including privilege escalation attempts, indicating a realistic simulation.

#### 🟡 [MEDIUM] The attacker attempted to escalate privileges using 'sudo -l' and 'sudo -V' commands.

- **Evidence:** `commands_executed`
- **Recommendation:** Review the system's sudo configuration.

### Emulation Accuracy

**Score:** `█████████░` 9.0/10

**Summary:** The honeypot accurately simulated a Linux system, allowing the attacker to execute various commands.

_No specific findings._

### Data Quality & Telemetry

**Score:** `███████░░░` 7.0/10

**Summary:** The log data appears to be complete, but some commands executed by the attacker did not generate log entries.

#### 🟢 [LOW] Some commands, such as 'bash -c 'echo $BASH_VERSION''

- **Evidence:** `commands_executed`
- **Recommendation:** Review the logging configuration to ensure all relevant events are logged.

### Containment & Safety

**Score:** `██████░░░░` 6.0/10

**Summary:** The honeypot did not contain the attacker's actions, allowing them to execute potentially malicious commands.

#### 🟡 [MEDIUM] The attacker executed commands that could potentially harm the system, such as 'cat /etc/sudoers' and 'find / -perm -4000 2>/dev/null'.

- **Evidence:** `commands_executed`
- **Recommendation:** Implement containment mechanisms to prevent harm to the system.

### Operational Complexity

**Score:** `█████░░░░░` 5.0/10

**Summary:** The honeypot's operational complexity is moderate, with a variety of commands executed by the attacker.

_No specific findings._

---

## Top Vulnerabilities

### 1. 🟡 [MEDIUM] Privilege Escalation Attempts

**CVSS Estimate:** Medium

The attacker attempted to escalate privileges using various commands.

**Evidence:** `commands_executed`

**Recommendation:** Review the system's sudo configuration and implement containment mechanisms.

---

## How an Attacker Would Detect This is a Honeypot

> These are the behavioral tells that reveal Cowrie's artificial nature.

- The honeypot's logging and command execution capabilities would likely be noticeable to an attacker.

---

## Immediate Remediation Actions

1. Review the logging configuration to ensure all relevant events are logged, and implement containment mechanisms to prevent harm to the system.

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
bash -c 'echo $BASH_VERSION'
bash -c 'echo $BASH_VERSINFO'
bash -c 'echo $BASH_VERSION'
bash -c 'echo $SHELL'
bash -c 'echo $PATH'
bash -c 'echo $HOME'
bash -c 'echo $USER'
bash -c 'echo $LOGNAME'
bash -c 'echo $PWD'
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
| 40 | `bash -c 'echo $BASH_VERSION'` | bash -c 'echo $BASH_VERSION' [4l[4l [4hroot@localhost:~#  |
| 41 | `bash -c 'echo $BASH_VERSINFO'` | bash -c 'echo $BASH_VERSINFO' [4l[4l [4hroot@localhost:~#  |
| 42 | `bash -c 'echo $BASH_VERSION'` | bash -c 'echo $BASH_VERSION' [4l[4l [4hroot@localhost:~#  |
| 43 | `bash -c 'echo $SHELL'` | bash -c 'echo $SHELL' [4l[4l/bin/bash [4hroot@localhost:~#  |
| 44 | `bash -c 'echo $PATH'` | bash -c 'echo $PATH' [4l[4l/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin: |
| 45 | `bash -c 'echo $HOME'` | bash -c 'echo $HOME' [4l[4l/root [4hroot@localhost:~#  |
| 46 | `bash -c 'echo $USER'` |  |
| 47 | `bash -c 'echo $LOGNAME'` |  |
| 48 | `bash -c 'echo $PWD'` |  |

---

## Cowrie Log Sample (first 20 events)

```json
[
  {
    "session": "f13ec3d69bef",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 59557,
    "dst_ip": "192.168.56.102",
    "dst_port": 2222,
    "eventid": "cowrie.session.connect",
    "sensor": "kali",
    "uuid": "b7a15396-8fb7-11f1-9021-08002717ff2b",
    "timestamp": "2026-09-10T11:53:26.929760Z",
    "message": "New connection: 192.168.56.1:59557 (192.168.56.102:2222) [session: f13ec3d69bef]"
  },
  {
    "session": "f13ec3d69bef",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 59557,
    "dst_ip": "192.168.56.102",
    "dst_port": 2222,
    "version": "SSH-2.0-paramiko_3.4.0",
    "eventid": "cowrie.client.version",
    "sensor": "kali",
    "uuid": "b7a15396-8fb7-11f1-9021-08002717ff2b",
    "timestamp": "2026-09-10T11:53:26.944728Z",
    "message": "Remote SSH version: SSH-2.0-paramiko_3.4.0"
  },
  {
    "session": "f13ec3d69bef",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 59557,
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
    "timestamp": "2026-09-10T11:53:26.948868Z",
    "message": "SSH client hassh fingerprint: 87e3d9ffee0540b0390f8a5b9c343c08"
  },
  {
    "session": "f13ec3d69bef",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 59557,
    "dst_ip": "192.168.56.102",
    "dst_port": 2222,
    "username": "root",
    "password": "password",
    "eventid": "cowrie.login.success",
    "sensor": "kali",
    "uuid": "b7a15396-8fb7-11f1-9021-08002717ff2b",
    "timestamp": "2026-09-10T11:53:27.119616Z",
    "message": "login attempt [root/password] succeeded"
  },
  {
    "session": "f13ec3d69bef",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 59557,
    "dst_ip": "192.168.56.102",
    "dst_port": 2222,
    "width": 80,
    "height": 24,
    "eventid": "cowrie.client.size",
    "sensor": "kali",
    "uuid": "b7a15396-8fb7-11f1-9021-08002717ff2b",
    "timestamp": "2026-09-10T11:53:27.137455Z",
    "message": "Terminal Size: 80 24"
  },
  {
    "session": "f13ec3d69bef",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 59557,
    "dst_ip": "192.168.56.102",
    "dst_port": 2222,
    "arch": "linux-x64-lsb",
    "eventid": "cowrie.session.params",
    "sensor": "kali",
    "uuid": "b7a15396-8fb7-11f1-9021-08002717ff2b",
    "timestamp": "2026-09-10T11:53:27.149399Z",
    "message": ""
  },
  {
    "session": "f13ec3d69bef",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 59557,
    "dst_ip": "192.168.56.102",
    "dst_port": 2222,
    "input": "whoami",
    "eventid": "cowrie.command.input",
    "sensor": "kali",
    "uuid": "b7a15396-8fb7-11f1-9021-08002717ff2b",
    "timestamp": "2026-09-10T11:53:34.170503Z",
    "message": "CMD: whoami"
  },
  {
    "session": "f13ec3d69bef",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 59557,
    "dst_ip": "192.168.56.102",
    "dst_port": 2222,
    "input": "id",
    "eventid": "cowrie.command.input",
    "sensor": "kali",
    "uuid": "b7a15396-8fb7-11f1-9021-08002717ff2b",
    "timestamp": "2026-09-10T11:53:40.689773Z",
    "message": "CMD: id"
  },
  {
    "session": "f13ec3d69bef",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 59557,
    "dst_ip": "192.168.56.102",
    "dst_port": 2222,
    "input": "groups",
    "eventid": "cowrie.command.input",
    "sensor": "kali",
    "uuid": "b7a15396-8fb7-11f1-9021-08002717ff2b",
    "timestamp": "2026-09-10T11:53:47.205428Z",
    "message": "CMD: groups"
  },
  {
    "session": "f13ec3d69bef",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 59557,
    "dst_ip": "192.168.56.102",
    "dst_port": 2222,
    "input": "hostname",
    "eventid": "cowrie.command.input",
    "sensor": "kali",
    "uuid": "b7a15396-8fb7-11f1-9021-08002717ff2b",
    "timestamp": "2026-09-10T11:53:53.723184Z",
    "message": "CMD: hostname"
  },
  {
    "session": "f13ec3d69bef",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 59557,
    "dst_ip": "192.168.56.102",
    "dst_port": 2222,
    "input": "sudo -l",
    "eventid": "cowrie.command.input",
    "sensor": "kali",
    "uuid": "b7a15396-8fb7-11f1-9021-08002717ff2b",
    "timestamp": "2026-09-10T11:54:00.242714Z",
    "message": "CMD: sudo -l"
  },
  {
    "session": "f13ec3d69bef",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 59557,
    "dst_ip": "192.168.56.102",
    "dst_port": 2222,
    "input": "sudo -V",
    "eventid": "cowrie.command.input",
    "sensor": "kali",
    "uuid": "b7a15396-8fb7-11f1-9021-08002717ff2b",
    "timestamp": "2026-09-10T11:54:06.760026Z",
    "message": "CMD: sudo -V"
  },
  {
    "session": "f13ec3d69bef",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 59557,
    "dst_ip": "192.168.56.102",
    "dst_port": 2222,
    "input": "cat /etc/sudoers",
    "eventid": "cowrie.command.input",
    "sensor": "kali",
    "uuid": "b7a15396-8fb7-11f1-9021-08002717ff2b",
    "timestamp": "2026-09-10T11:54:13.278491Z",
    "message": "CMD: cat /etc/sudoers"
  },
  {
    "session": "f13ec3d69bef",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 59557,
    "dst_ip": "192.168.56.102",
    "dst_port": 2222,
    "input": "ls -la /etc/sudoers.d",
    "eventid": "cowrie.command.input",
    "sensor": "kali",
    "uuid": "b7a15396-8fb7-11f1-9021-08002717ff2b",
    "timestamp": "2026-09-10T11:54:19.803162Z",
    "message": "CMD: ls -la /etc/sudoers.d"
  },
  {
    "session": "f13ec3d69bef",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 59557,
    "dst_ip": "192.168.56.102",
    "dst_port": 2222,
    "input": "find / -perm -4000 2>/dev/null",
    "eventid": "cowrie.command.input",
    "sensor": "kali",
    "uuid": "b7a15396-8fb7-11f1-9021-08002717ff2b",
    "timestamp": "2026-09-10T11:54:26.318094Z",
    "message": "CMD: find / -perm -4000 2>/dev/null"
  },
  {
    "session": "f13ec3d69bef",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 59557,
    "dst_ip": "192.168.56.102",
    "dst_port": 2222,
    "input": "find / -perm -2000 2>/dev/null",
    "eventid": "cowrie.command.input",
    "sensor": "kali",
    "uuid": "b7a15396-8fb7-11f1-9021-08002717ff2b",
    "timestamp": "2026-09-10T11:54:32.846002Z",
    "message": "CMD: find / -perm -2000 2>/dev/null"
  },
  {
    "session": "f13ec3d69bef",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 59557,
    "dst_ip": "192.168.56.102",
    "dst_port": 2222,
    "input": "find /usr/bin -perm -4000",
    "eventid": "cowrie.command.input",
    "sensor": "kali",
    "uuid": "b7a15396-8fb7-11f1-9021-08002717ff2b",
    "timestamp": "2026-09-10T11:54:39.351090Z",
    "message": "CMD: find /usr/bin -perm -4000"
  },
  {
    "session": "f13ec3d69bef",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 59557,
    "dst_ip": "192.168.56.102",
    "dst_port": 2222,
    "input": "getcap -r / 2>/dev/null",
    "eventid": "cowrie.command.input",
    "sensor": "kali",
    "uuid": "b7a15396-8fb7-11f1-9021-08002717ff2b",
    "timestamp": "2026-09-10T11:54:45.868895Z",
    "message": "CMD: getcap -r / 2>/dev/null"
  },
  {
    "session": "f13ec3d69bef",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 59557,
    "dst_ip": "192.168.56.102",
    "dst_port": 2222,
    "input": "getcap -r /",
    "eventid": "cowrie.command.failed",
    "sensor": "kali",
    "uuid": "b7a15396-8fb7-11f1-9021-08002717ff2b",
    "timestamp": "2026-09-10T11:54:45.881128Z",
    "message": "Command not found: getcap -r /"
  },
  {
    "session": "f13ec3d69bef",
    "protocol": "ssh",
    "src_ip": "192.168.56.1",
    "src_port": 59557,
    "dst_ip": "192.168.56.102",
    "dst_port": 2222,
    "input": "capsh --print",
    "eventid": "cowrie.command.input",
    "sensor": "kali",
    "uuid": "b7a15396-8fb7-11f1-9021-08002717ff2b",
    "timestamp": "2026-09-10T11:54:52.386626Z",
    "message": "CMD: capsh --print"
  }
]
```

---
*Generated by LLM-based Cowrie Honeypot Evaluator*
