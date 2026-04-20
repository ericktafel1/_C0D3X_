# SMTP

## Overview

Mail transfer service enumeration, user probing, relay validation, and message-sending helpers.

## Default Ports

- 25/tcp SMTP, 465/tcp SMTPS, 587/tcp submission

## SMTP

```bash
nc -nv <IP> 25
python3 smtp.py <user> <IP>
```

**SMTP Users Enumeration (Python Script):**

```python
#!/usr/bin/python

import socket
import sys

if len(sys.argv) != 3:
        print("Usage: vrfy.py <username> <target_ip>")
        sys.exit(0)

# Create a Socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the Server
ip = sys.argv[2]
connect = s.connect((ip,25))

# Receive the banner
banner = s.recv(1024)

print(banner)

# VRFY a user
user = (sys.argv[1]).encode()
s.send(b'VRFY ' + user + b'\r\n')
result = s.recv(1024)

print(result)

# Close the socket
s.close()
```

More SMTP enumeration tools:

```bash
nmap --script=smtp-enum-users -p 25 <target>
smtp-user-enum -M VRFY -U users.txt -t <target>
```

**From Windows:**

```PowerShell
Test-NetConnection -Port 25 192.168.50.8
```

> **Note:** To use Telnet on Windows, you might need to enable it: `dism /online /Enable-Feature /FeatureName:TelnetClient`

```bash
telnet 192.168.50.8 25
```

## sendemail

```
sendemail -f <from_email> -t <to_email> -s <SMTP_IP> -u <SUBJECT> -m <content> -a <attachements> -v
```

## Useful Additions

```bash
nc -nv <target> 25
telnet <target> 25
nmap --script=smtp-enum-users,smtp-open-relay -p 25,465,587 <target>
```

## Common Attack Paths

- VRFY/EXPN user enumeration where enabled.
- Open relay validation.
- Internal user discovery that feeds spraying, phishing, or mailbox compromise.

## See Also

- `07 Creds and Cracking/Password Spraying and Reuse.md`
