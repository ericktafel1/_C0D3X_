# FTP

## Overview

Classic file service. Useful for anonymous access, credential reuse, backup leakage, and writable web-root style abuse.

## Default Ports

- 21/tcp, sometimes 20/tcp for active data channels

## Quick Enumeration

```bash
ftp <IP>
nc -nv <IP> 21
nmap --script=ftp-anon,ftp-bounce,ftp-syst -p 21 <target>
wget -m --no-passive ftp://anonymous:anonymous@<IP>
```

## Anonymous and Weak Authentication Checks

```bash
ftp <target>
# try anonymous / anonymous, anonymous / blank, ftp / ftp
hydra -L users.txt -P passwords.txt ftp://<target> -t 4
```

## FTP ANON LOGIN?  (→ ftp_anon.txt)

```bash
for ip in $(cat online); do nmap -p21 --script ftp-anon -Pn "$ip" 2>/dev/null | grep -q "Anonymous FTP login allowed" && echo $ip; done | tee ftp_anon.txt
```

############################################

## FTP

```bash
nmap --script=ftp-anon,ftp-bounce -p 21 <target>
ftp <target>
```

## Anonymous FTP Login (check all default creds)

```bash
ftp <target>
```

---

- Use `binary` mode before downloading executables or archives.
- Test writable directories and any odd traversal behavior manually in the interactive client.

## Operator Notes

- Switch to binary mode before pulling executables or archives.
- Writable shares can expose web roots, backup material, configuration files, and credential-bearing exports.
- Traversal behavior and SITE-specific commands vary widely by implementation; validate manually in the interactive client.

## See Also

- `09 Movement/File Transfers.md`
