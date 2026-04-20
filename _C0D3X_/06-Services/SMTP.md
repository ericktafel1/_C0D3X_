## SMTP

> Source: `01101100-C0D3X-00110110.md` → `Enumeration > Service Enumeration > SMTP`

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

> Source: `01101100-C0D3X-00110110.md` → `Disable Protection > sendemail`

```
sendemail -f <from_email> -t <to_email> -s <SMTP_IP> -u <SUBJECT> -m <content> -a <attachements> -v
```
