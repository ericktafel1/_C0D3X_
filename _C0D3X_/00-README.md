## Folder map

- `00-Index` — README, search guide, manifest
- `01-Enumeration` — host discovery, scans, recon, target and wordlist notes
- `02-Web` — web enumeration, auth, SQLi, uploads, client-side, CMS/API
- `03-Active-Directory` — AD enumeration, Kerberos, LDAP, SMB/RPC, BloodHound/ACLs/ADCS, lateral movement
- `04-Windows` — Windows access, PowerShell, RDP/WinRM, MSSQL, privesc, Defender/UAC/SePrivileges
- `05-Linux` — Linux enum, SSH, NFS, privesc, SUID/caps/cron, shell stabilization
- `06-Network-Services` — DNS, FTP, SMTP, SNMP, IMAP/POP3, IPMI/VNC, non-MSSQL databases
- `07-Credentials-and-Cracking` — spraying, reuse, hash cracking, Kerberos cracking, wordlists
- `08-Post-Exploitation` — looting, secrets, persistence, cleanup, data/shares
- `09-Movement` — file transfers, pivoting, tunneling, Ligolo
- `10-Toolbox` — Nmap, tmux, exploit research, misc utilities
- `11-Reverse-Engineering-and-Exploit-Dev` — payload helpers, msfvenom, BOF/GDB material
- `12-Cloud-and-Resources` — AWS, methodology, links, operator guidance
- `98-Archive` — preserved writeups, templates, bug bounty research
- `99-Fragments` — leftovers or source artifacts that were intentionally preserved outside the main flow

## Notes

- Search is expected to be the main interface. Headings preserve source context so terms like `kerberoast`, `xp_cmdshell`, `AlwaysInstallElevated`, `ligolo`, `wfuzz`, `UNION SELECT`, and `SeImpersonatePrivilege` stay easy to locate.
- Service-specific material was moved out of generic mixed buckets where possible. Example: AD and SMB/RPC live under `03-Active-Directory`, not under web auth.
- Non-text artifacts and duplicate source paths are recorded in `00-Index/Manifest.md`.
