# Active Directory Overview

* * *

`Active Directory` ( `AD`) is a directory service for Windows network environments. It is a distributed, hierarchical structure that allows for centralized management of an organization’s resources, including users, computers, groups, network devices and file shares, group policies, servers and workstations, and trusts. AD provides authentication and authorization functions within a Windows domain environment. It was first shipped with Windows Server 2000; it has come under increasing attack in recent years. Designed to be backward-compatible, and many features are arguably not “secure by default,” and it can be easily misconfigured.

This can be leveraged to move laterally and vertically within a network and gain unauthorized access. AD is essentially a large database accessible to all users within the domain, regardless of their privilege level. A basic AD user account with no added privileges can be used to enumerate the majority of objects contained within AD, including but not limited to:

- Domain Computers
- Domain Users
- Domain Group Information
- Default Domain Policy
- Domain Functional Levels
- Password Policy
- Group Policy Objects (GPOs)
- Kerberos Delegation
- Domain Trusts
- Access Control Lists (ACLs)

This data will paint a clear picture of the overall security posture of an Active Directory environment. It can be used to quickly identify misconfigurations, overly permissive policies, and other ways of escalating privileges within an AD environment. Many attacks exist that merely leverage AD misconfigurations, bad practices, or poor administration, such as:

- Kerberoasting / ASREPRoasting
- NTLM Relaying
- Network traffic poisoning
- Password spraying
- Kerberos delegation abuse
- Domain trust abuse
- Credential theft
- Object control

Hardening Active Directory, along with a strong patching and configuration management policy, and proper network segmentation should be prioritized. If an environment is tightly managed and an adversary can gain a foothold and bypass EDR or other protections, proper management of AD can prevent them from escalating privileges, moving laterally, and getting to the crown jewels. Proper controls will help slow down an attacker and potentially force them to become noisier and risk detection.

* * *

## Active Directory Structure

Active Directory is arranged in a hierarchical tree structure, with a forest at the top containing one or more domains, which can themselves contain nested subdomains. A forest is the **security boundary** within which all objects are under administrative control. A forest may contain multiple domains, and a domain may contain further child or sub-domains. A domain is a structure within which contained objects (users, computers, and groups) are accessible. Objects are the most basic unit of data in AD.

It contains many built-in `Organizational Units` ( `OU` s), such as “Domain Controllers,” “Users,” and “Computers,” and new `OU` s can be created as required. `OU` s may contain objects and sub-OUs, allowing for assignment of different group policies.

![image](https://academy.hackthebox.com/storage/modules/22/ad_forests1.png)

We can see this structure graphically by opening `Active Directory Users and Computers` on a Domain Controller. In our lab domain `INLANEFREIGHT.LOCAL`, we see various OUs such as `Admin`, `Employees`, `Servers`, `Workstations`, etc. Many of these OUs have OUs nested within them, such as the `Mail Room` OU under `Employees`. This helps maintain a clear and coherent structure within Active Directory, which is especially important as we add Group Policy Objects (GPOs) to enforce settings throughout the domain.

![image](https://academy.hackthebox.com/storage/modules/22/ad_structure.png)

Understanding the structure of Active Directory is paramount to perform proper enumeration and uncover the flaws and misconfigurations that sometimes have gone missed in an environment for many years.

* * *

## Module Exercises

Throughout this module, you will connect to various target hosts via the Remote Desktop Protocol (RDP) to complete the exercises. Any necessary credentials will be provided with each exercise, and the RDP connection can be made via `xfreerdp` from the Pwnbox as follows:

```shell
xfreerdp /v:<target IP address> /u:htb-student /p:<password> /cert-ignore

```

Any necessary tools can be found in the `c:\tools` directory after logging in to the target host.


# Why Enumerate AD?

* * *

As penetration testers, `enumeration` is one of, if not the most important, skills we must master. When starting an assessment in a new network gaining a comprehensive inventory of the environment is extremely important. The information gathered during this phase will inform our later attacks and even post-exploitation. Given the prevalence of AD in corporate networks, we will likely find ourselves in AD environments regularly, and therefore, it is important to hone our enumeration process. There are many tools and techniques to help with AD enumeration, which we will cover in-depth in this module and subsequent modules; however, before using these tools, it is important to understand the reason for performing detailed AD enumeration.

Whether we perform a penetration test or targeted AD assessment, we can always go above and beyond and provide our clients with extra value by giving them a detailed picture of their AD strengths and weaknesses. Corporate environments go through many changes over the years, adding and removing employees and hosts, installing software and applications that require changes in AD, or corporate policies that require GPO changes. These changes can introduce security flaws through misconfiguration, and it is our job as assessors to find these flaws, exploit them, and help our clients fix them.

* * *

## Getting Started

Once we have a foothold in an AD environment, we should start by gathering several key pieces of information, including but not limited to:

- The domain functional level
- The domain password policy
- A full inventory of AD users
- A full inventory of AD computers
- A full inventory of AD groups and memberships
- Domain trust relationships
- Object ACLs
- Group Policy Objects (GPO) information
- Remote access rights

With this information in hand, we can look for any "quick wins" such as our current user or the entire `Domain Users` group having RDP and/or local administrator access to one or more hosts. This is common in large environments for many reasons, one being the improper use of jump hosts and another being Citrix server Remote Desktop Services (RDS) misconfigurations. We should also check what rights our current user has in the domain. Are they a member of any privileged groups? Do they have any special rights delegated? Do they have any control over another domain object such as a user, computer, or GPO?

The enumeration process is iterative. As we move through the AD environment, compromising hosts and users, we will need to perform additional enumeration to see if we have gained any further access to help us reach our goal.


# Rights and Privileges in AD

* * *

AD contains many groups that grant their members powerful rights and privileges. Many of these can be abused to escalate privileges within a domain and ultimately gain Domain Admin or SYSTEM privileges on a Domain Controller (DC). Some of these groups are listed below.

| **Group** | **Description** |
| --- | --- |
| Default Administrators | Domain Admins and Enterprise Admins "super" groups. |
| Server Operators | Members can modify services, access SMB shares, and backup files. |
| Backup Operators | Members are allowed to log onto DCs locally and should be considered Domain Admins. They can make shadow copies of the SAM/NTDS database, read the registry remotely, and access the file system on the DC via SMB. This group is sometimes added to the local Backup Operators group on non-DCs. |
| Print Operators | Members are allowed to logon to DCs locally and "trick" Windows into loading a malicious driver. |
| Hyper-V Administrators | If there are virtual DCs, any virtualization admins, such as members of Hyper-V Administrators, should be considered Domain Admins. |
| Account Operators | Members can modify non-protected accounts and groups in the domain. |
| Remote Desktop Users | Members are not given any useful permissions by default but are often granted additional rights such as _Allow Login Through Remote Desktop Services_ and can move laterally using the RDP protocol. |
| Remote Management Users | Members are allowed to logon to DCs with PSRemoting (This group is sometimes added to the local remote management group on non-DCs). |
| Group Policy Creator Owners | Members can create new GPOs but would need to be delegated additional permissions to link GPOs to a container such as a domain or OU. |
| Schema Admins | Members can modify the Active Directory schema structure and can backdoor any to-be-created Group/GPO by adding a compromised account to the default object ACL. |
| DNS Admins | Members have the ability to load a DLL on a DC but do not have the necessary permissions to restart the DNS server. They can load a malicious DLL and wait for a reboot as a persistence mechanism. Loading a DLL will often result in the service crashing. A more reliable way to exploit this group is to [create a WPAD record](https://web.archive.org/web/20230129100526/https://cube0x0.github.io/Pocing-Beyond-DA/). |

#### Members of "Schema Admins"

```powershell
PS C:\htb> Get-ADGroup -Identity "Schema Admins" -Properties *

adminCount                      : 1
CanonicalName                   : INLANEFREIGHT.LOCAL/Users/Schema Admins
CN                              : Schema Admins
Created                         : 7/26/2020 4:14:37 PM
createTimeStamp                 : 7/26/2020 4:14:37 PM
Deleted                         :
Description                     : Designated administrators of the schema
DisplayName                     :
DistinguishedName               : CN=Schema Admins,CN=Users,DC=INLANEFREIGHT,DC=LOCAL
dSCorePropagationData           : {7/29/2020 11:52:30 PM, 7/29/2020 11:09:16 PM, 7/27/2020 9:45:00 PM, 7/27/2020
                                  9:34:13 PM...}
GroupCategory                   : Security
GroupScope                      : Universal
groupType                       : -2147483640
HomePage                        :
instanceType                    : 4
isCriticalSystemObject          : True
isDeleted                       :
LastKnownParent                 :
ManagedBy                       :
member                          : {CN=Jenna Smith,OU=Server Team,OU=IT,OU=Employees,DC=INLANEFREIGHT,DC=LOCAL,
                                  CN=Administrator,CN=Users,DC=INLANEFREIGHT,DC=LOCAL}
MemberOf                        : {CN=Denied RODC Password Replication Group,CN=Users,DC=INLANEFREIGHT,DC=LOCAL}
Members                         : {CN=Jenna Smith,OU=Server Team,OU=IT,OU=Employees,DC=INLANEFREIGHT,DC=LOCAL,
                                  CN=Administrator,CN=Users,DC=INLANEFREIGHT,DC=LOCAL}
Modified                        : 7/30/2020 2:04:05 PM
modifyTimeStamp                 : 7/30/2020 2:04:05 PM
Name                            : Schema Admins
nTSecurityDescriptor            : System.DirectoryServices.ActiveDirectorySecurity
ObjectCategory                  : CN=Group,CN=Schema,CN=Configuration,DC=INLANEFREIGHT,DC=LOCAL
ObjectClass                     : group
ObjectGUID                      : 36eef5cb-92b1-47d2-a25d-b9d73783ed1e
objectSid                       : S-1-5-21-2974783224-3764228556-2640795941-518
ProtectedFromAccidentalDeletion : False
SamAccountName                  : Schema Admins
sAMAccountType                  : 268435456
sDRightsEffective               : 15
SID                             : S-1-5-21-2974783224-3764228556-2640795941-518
SIDHistory                      : {}
uSNChanged                      : 66825
uSNCreated                      : 12336
whenChanged                     : 7/30/2020 2:04:05 PM
whenCreated                     : 7/26/2020 4:14:37 PM

```

* * *

## User Rights Assignment

Depending on group membership, and other factors such as privileges assigned via Group Policy, users can have various rights assigned to their account. This Microsoft article on [User Rights Assignment](https://docs.microsoft.com/en-us/windows/security/threat-protection/security-policy-settings/user-rights-assignment) provides a detailed explanation of each of the user rights that can be set in Windows.

Typing the command `whoami /priv` will give you a listing of all user rights assigned to your current user. Some rights are only available to administrative users and can only be listed/leveraged when running an elevated cmd or PowerShell session. These concepts of elevated rights and [User Account Control (UAC)](https://docs.microsoft.com/en-us/windows/security/identity-protection/user-account-control/how-user-account-control-works) are security features introduced with Windows Vista to default to restricting applications from running with full permissions unless absolutely necessary. If we compare and contrast the rights available to us as an admin in a non-elevated console vs. an elevated console, we will see that they differ drastically. Let's try this out as the `htb-student` user on the lab machine.

Below are the rights available to a Domain Admin user.

#### User Rights Non-Elevated

We can see the following in a non-elevated console:

```powershell
PS C:\htb> whoami /priv

PRIVILEGES INFORMATION
----------------------

Privilege Name                Description                          State
============================= ==================================== ========
SeShutdownPrivilege           Shut down the system                 Disabled
SeChangeNotifyPrivilege       Bypass traverse checking             Enabled
SeUndockPrivilege             Remove computer from docking station Disabled
SeIncreaseWorkingSetPrivilege Increase a process working set       Disabled
SeTimeZonePrivilege           Change the time zone                 Disabled

```

#### User Rights Elevated

If we run an elevated command (our htb-student user has local admin rights via nested group membership; the Domain Users group is in the local Administrators group), we can see the complete listing of rights available to us:

```powershell
PS C:\htb> whoami /priv

PRIVILEGES INFORMATION
----------------------

Privilege Name                            Description                                                        State
========================================= ================================================================== ========
SeIncreaseQuotaPrivilege                  Adjust memory quotas for a process                                 Disabled
SeMachineAccountPrivilege                 Add workstations to domain                                         Disabled
SeSecurityPrivilege                       Manage auditing and security log                                   Disabled
SeTakeOwnershipPrivilege                  Take ownership of files or other objects                           Disabled
SeLoadDriverPrivilege                     Load and unload device drivers                                     Disabled
SeSystemProfilePrivilege                  Profile system performance                                         Disabled
SeSystemtimePrivilege                     Change the system time                                             Disabled
SeProfileSingleProcessPrivilege           Profile single process                                             Disabled
SeIncreaseBasePriorityPrivilege           Increase scheduling priority                                       Disabled
SeCreatePagefilePrivilege                 Create a pagefile                                                  Disabled
SeBackupPrivilege                         Back up files and directories                                      Disabled
SeRestorePrivilege                        Restore files and directories                                      Disabled
SeShutdownPrivilege                       Shut down the system                                               Disabled
SeDebugPrivilege                          Debug programs                                                     Enabled
SeSystemEnvironmentPrivilege              Modify firmware environment values                                 Disabled
SeChangeNotifyPrivilege                   Bypass traverse checking                                           Enabled
SeRemoteShutdownPrivilege                 Force shutdown from a remote system                                Disabled
SeUndockPrivilege                         Remove computer from docking station                               Disabled
SeEnableDelegationPrivilege               Enable computer and user accounts to be trusted for delegation     Disabled
SeManageVolumePrivilege                   Perform volume maintenance tasks                                   Disabled
SeImpersonatePrivilege                    Impersonate a client after authentication                          Enabled
SeCreateGlobalPrivilege                   Create global objects                                              Enabled
SeIncreaseWorkingSetPrivilege             Increase a process working set                                     Disabled
SeTimeZonePrivilege                       Change the time zone                                               Disabled
SeCreateSymbolicLinkPrivilege             Create symbolic links                                              Disabled
SeDelegateSessionUserImpersonatePrivilege Obtain an impersonation token for another user in the same session Disabled

```

A standard domain user, in contrast, has drastically fewer rights.

#### Domain User Rights

```powershell
PS C:\htb> whoami /priv

PRIVILEGES INFORMATION
----------------------

Privilege Name                Description                    State
============================= ============================== ========
SeChangeNotifyPrivilege       Bypass traverse checking       Enabled
SeIncreaseWorkingSetPrivilege Increase a process working set Disabled

```

User rights increase based on the groups they are placed in and/or their assigned privileges. Below is an example of the rights granted to users in the `Backup Operators` group. Users in this group do have other rights that are currently restricted by UAC. Still, we can see from this command that they have the `SeShutdownPrivilege`, which means that they can shut down a domain controller that could cause a massive service interruption should they log onto a domain controller locally (not via RDP or WinRM).

#### Backup Operator Rights

```powershell
PS C:\htb> whoami /priv

PRIVILEGES INFORMATION
----------------------

Privilege Name                Description                    State
============================= ============================== ========
SeShutdownPrivilege           Shut down the system           Disabled
SeChangeNotifyPrivilege       Bypass traverse checking       Enabled
SeIncreaseWorkingSetPrivilege Increase a process working set Disabled

```

As attackers and defenders, we need to review the membership of these groups. It's not uncommon to find seemingly low privileged users added to one or more of these groups, which can be used to further access or compromise the domain.

Note: When spawning your target, we ask you to wait for 3 minutes until the whole lab with all the configurations is set up so that the connection to your target works flawlessly.


# Microsoft Remote Server Administration Tools (RSAT)

* * *

## RSAT Background

The `Remote Server Administration Tools` ( `RSAT`) have been part of Windows since the days of Windows 2000. RSAT allows systems administrators to remotely manage Windows Server roles and features from a workstation running Windows 10, Windows 8.1, Windows 7, or Windows Vista. `RSAT` can only be installed on Professional or Enterprise editions of Windows. In an enterprise environment, RSAT can remotely manage Active Directory, DNS, and DHCP. RSAT also allows us to manage installed server roles and features, File Services, and Hyper-V. The full listing of tools included with `RSAT` is:

- SMTP Server Tools
- Hyper-V Management Tools
- Hyper-V Module for Windows PowerShell
- Hyper-V GUI Management Tools
- Windows Server Update Services Tools
- API and PowerShell cmdlets
- User Interface Management Console
- Active Directory Users and Computers Snap-in
- Active Directory Sites and Services Snap-in
- Active Directory Domains and Trusts Snap-in
- Active Directory Administrative Center Snap-in
- ADSI Edit Snap-in
- Active Directory Schema Snap-in (Not Registered)
- Active Directory Command Line Tools
- Active Directory Module for Windows PowerShell
- IIS Management Tools
- IIS Management Console
- IIS Management Compatibility
- Feature Tools
- Remote Desktop Services Tools
- Role Tools
- Update Services Tools
- Group Policy Tools

This [script](https://gist.github.com/dually8/558fcfa9156f59504ab36615dfc4856a) can be used to install RSAT in Windows 10 1809, 1903, and 1909. Installation instructions for other versions of Windows, as well as additional information about RSAT, can be found [here](https://support.microsoft.com/en-us/help/2693643/remote-server-administration-tools-rsat-for-windows-operating-systems). RSAT can be installed easily with PowerShell as well.

We can check which, if any, RSAT tools are installed using PowerShell.

#### PowerShell - Available RSAT Tools

```powershell
PS C:\htb>  Get-WindowsCapability -Name RSAT* -Online | Select-Object -Property Name, State

Name                                                          State
----                                                          -----
Rsat.ActiveDirectory.DS-LDS.Tools~~~~0.0.1.0             NotPresent
Rsat.BitLocker.Recovery.Tools~~~~0.0.1.0                 NotPresent
Rsat.CertificateServices.Tools~~~~0.0.1.0                NotPresent
Rsat.DHCP.Tools~~~~0.0.1.0                               NotPresent
Rsat.Dns.Tools~~~~0.0.1.0                                NotPresent
Rsat.FailoverCluster.Management.Tools~~~~0.0.1.0         NotPresent
Rsat.FileServices.Tools~~~~0.0.1.0                       NotPresent
Rsat.GroupPolicy.Management.Tools~~~~0.0.1.0             NotPresent
Rsat.IPAM.Client.Tools~~~~0.0.1.0                        NotPresent
Rsat.LLDP.Tools~~~~0.0.1.0                               NotPresent
Rsat.NetworkController.Tools~~~~0.0.1.0                  NotPresent
Rsat.NetworkLoadBalancing.Tools~~~~0.0.1.0               NotPresent
Rsat.RemoteAccess.Management.Tools~~~~0.0.1.0            NotPresent
Rsat.RemoteDesktop.Services.Tools~~~~0.0.1.0             NotPresent
Rsat.ServerManager.Tools~~~~0.0.1.0                      NotPresent
Rsat.Shielded.VM.Tools~~~~0.0.1.0                        NotPresent
Rsat.StorageMigrationService.Management.Tools~~~~0.0.1.0 NotPresent
Rsat.StorageReplica.Tools~~~~0.0.1.0                     NotPresent
Rsat.SystemInsights.Management.Tools~~~~0.0.1.0          NotPresent
Rsat.VolumeActivation.Tools~~~~0.0.1.0                   NotPresent
Rsat.WSUS.Tools~~~~0.0.1.0                               NotPresent

```

From here, we can choose to install all available tools using the following command:

#### PowerShell - Install All Available RSAT Tools

```powershell
PS C:\htb> Get-WindowsCapability -Name RSAT* -Online | Add-WindowsCapability –Online

```

We can also install tools one at a time as needed.

#### PowerShell - Install an RSAT Tool

```powershell
PS C:\htb> Add-WindowsCapability -Name Rsat.ActiveDirectory.DS-LDS.Tools~~~~0.0.1.0  –Online

```

Once installed, all of the tools will be available under `Administrative Tools` in the `Control Panel`.

![image](https://academy.hackthebox.com/storage/modules/22/RSAT_cp.png)

* * *

## Domain Context for Enumeration

Many tools are missing credential and context parameters and instead get those values directly from the current context. There are a few ways to alter a user's context in Windows if you have access to a password or a hash, such as:

Using " `runas /netonly`" to leverage the built-in [runas.exe](https://docs.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2012-r2-and-2012/cc771525(v=ws.11)) command line tool.

#### CMD - Runas User

```cmd-session
C:\htb> runas /netonly /user:htb.local\jackie.may powershell

```

Other tools that we will discuss in later modules, such as [Rubeus](https://github.com/GhostPack/Rubeus) and [mimikatz](https://github.com/gentilkiwi/mimikatz) can be passed cleartext credentials or an NTLM password hash.

#### CMD - Rubeus.exe Cleartext Credentials

```cmd-session
C:\htb> rubeus.exe asktgt /user:jackie.may /domain:htb.local /dc:10.10.110.100 /rc4:ad11e823e1638def97afa7cb08156a94

```

#### CMD - Mimikatz.exe Cleartext Credentials

```cmd-session
C:\htb> mimikatz.exe sekurlsa::pth /domain:htb.local /user:jackie.may /rc4:ad11e823e1638def97afa7cb08156a94

```

* * *

## Enumeration with RSAT

If we compromise a domain-joined system (or a client has you perform an AD assessment from one of their workstations), we can leverage RSAT to enumerate AD. While RSAT will make GUI tools such as `Active Directory Users and Computers` and `ADSI Edit` available to us, the most important tool we have seen throughout this module is the PowerShell [Active Directory module](https://github.com/MicrosoftDocs/windows-powershell-docs/blob/main/docset/winserver2012-ps/adcsadministration/adcsadministration.md).

Alternatively, we can enumerate the domain from a non-domain joined host (provided that it is in a subnet that communicates with a domain controller) by launching any RSAT snap-ins using " `runas`" from the command line. This is particularly useful if we find ourselves performing an internal assessment, gain valid AD credentials, and would like to perform enumeration from a Windows VM.

![image](https://academy.hackthebox.com/storage/modules/22/rsat_adsi.png)

* * *

We can also open the `MMC Console` from a non-domain joined computer using the following command syntax:

#### CMD - MMC Runas Domain User

```cmd-session
C:\htb> runas /netonly /user:Domain_Name\Domain_USER mmc

```

![image](https://academy.hackthebox.com/storage/modules/22/mmc_non_ad.png)

We can add any of the RSAT snap-ins and enumerate the target domain in the context of the target user `sally.jones` in the `freightlogistics.local` domain. After adding the snap-ins, we will get an error message that the "specified domain either does not exist or could not be contacted." From here, we have to right-click on the `Active Directory Users and Computers` snap-in (or any other chosen snap-in) and choose `Change Domain`.

![image](https://academy.hackthebox.com/storage/modules/22/mmc_change_domain.png)

Type the target domain into the `Change domain` dialogue box, here `freightlogistics.local`. From here, we can now freely enumerate the domain using any of the AD RSAT snapins.

![image](https://academy.hackthebox.com/storage/modules/22/mmc_ad_users_computers.png)

While these graphical tools are useful and easy to use, they are very inefficient when trying to enumerate a large domain. In the next few sections, we will introduce `LDAP` and various types of search filters that we can use to enumerate AD using PowerShell. The topics that we cover in these sections will help us gain a better understanding of how AD works and how to search for information efficiently, which will ultimately better inform us on the usage of the more "automated" tools and scripts that we will cover in the next two `AD Enumeration` modules.


# The Power of NT AUTHORITY\\SYSTEM

* * *

The [LocalSystem account](https://docs.microsoft.com/en-us/windows/win32/services/localsystem-account) `NT AUTHORITY\SYSTEM` is a built-in account in Windows operating systems, used by the service control manager. It has the highest level of access in the OS (and can be made even more powerful with Trusted Installer privileges). This account has more privileges than a local administrator account and is used to run most Windows services. It is also very common for third-party services to run in the context of this account by default. The SYSTEM account has the following [privileges](https://docs.microsoft.com/en-us/windows/win32/secauthz/privilege-constants):

| Privilege | Default State |
| --- | --- |
| SE\_ASSIGNPRIMARYTOKEN\_NAME | disabled |
| SE\_AUDIT\_NAME | enabled |
| SE\_BACKUP\_NAME | disabled |
| SE\_CHANGE\_NOTIFY\_NAME | enabled |
| SE\_CREATE\_GLOBAL\_NAME | enabled |
| SE\_CREATE\_PAGEFILE\_NAME | enabled |
| SE\_CREATE\_PERMANENT\_NAME | enabled |
| SE\_CREATE\_TOKEN\_NAME | disabled |
| SE\_DEBUG\_NAME | enabled |
| SE\_IMPERSONATE\_NAME | enabled |
| SE\_INC\_BASE\_PRIORITY\_NAME | enabled |
| SE\_INCREASE\_QUOTA\_NAME | disabled |
| SE\_LOAD\_DRIVER\_NAME | disabled |
| SE\_LOCK\_MEMORY\_NAME | enabled |
| SE\_MANAGE\_VOLUME\_NAME | disabled |
| SE\_PROF\_SINGLE\_PROCESS\_NAME | enabled |
| SE\_RESTORE\_NAME | disabled |
| SE\_SECURITY\_NAME | disabled |
| SE\_SHUTDOWN\_NAME | disabled |
| SE\_SYSTEM\_ENVIRONMENT\_NAME | disabled |
| SE\_SYSTEMTIME\_NAME | disabled |
| SE\_TAKE\_OWNERSHIP\_NAME | disabled |
| SE\_TCB\_NAME | enabled |
| SE\_UNDOCK\_NAME | disabled |

The SYSTEM account on a domain-joined host can enumerate Active Directory by impersonating the computer account, which is essentially a special user account. If you land on a domain-joined host with SYSTEM privileges during an assessment and cannot find any useful credentials in memory or other data on the machine, there are still many things you can do. Having SYSTEM-level access within a domain environment is nearly equivalent to having a domain user account. The only real limitation is not being able to perform cross-trust Kerberos attacks such as Kerberoasting.

There are several ways to gain SYSTEM-level access on a host, including but not limited to:

- Remote Windows exploits such as EternalBlue or BlueKeep.
- Abusing a service running in the context of the SYSTEM account.
- Abusing SeImpersonate privileges using [RottenPotatoNG](https://github.com/breenmachine/RottenPotatoNG) against older Windows systems, [Juicy Potato](https://github.com/ohpe/juicy-potato), or [PrintSpoofer](https://github.com/itm4n/PrintSpoofer) if targeting [Windows 10/Windows Server 2019](https://itm4n.github.io/printspoofer-abusing-impersonate-privileges/).
- Local privilege escalation flaws in Windows operating systems such as the [Windows 10 Task Scheduler 0day](https://blog.0patch.com/2019/06/another-task-scheduler-0day-another.html).
- PsExec with the `-s` flag

By gaining SYSTEM-level access on a domain-joined host, we will be able to:

- Enumerate the domain and gather data such as information about domain users and groups, local administrator access, domain trusts, ACLs, user and computer properties, etc., using `BloodHound`, and `PowerView`/ `SharpView`.
- Perform Kerberoasting / ASREPRoasting attacks.
- Run tools such as [Inveigh](https://github.com/Kevin-Robertson/Inveigh) to gather Net-NTLM-v2 hashes or perform relay attacks.
- Perform token impersonation to hijack a privileged domain user account.
- Carry out ACL attacks.


# LDAP Overview

* * *

[`Lightweight Directory Access Protocol` ( `LDAP`)](https://en.wikipedia.org/wiki/Lightweight_Directory_Access_Protocol) is an integral part of Active Directory (AD). The latest LDAP specification is Version 3, which is published as [RFC 4511](https://tools.ietf.org/html/rfc4511). A firm understanding of how LDAP works in an AD environment is crucial for both attackers and defenders.

`LDAP` is an open-source and cross-platform protocol used for authentication against various directory services (such as AD). As discussed in the previous section, AD stores user account information and security information such as passwords and facilitates sharing this information with other devices on the network. `LDAP` is the language that applications use to communicate with other servers that also provide directory services. In other words, `LDAP` is a way that systems in the network environment can "speak" to AD.

An `LDAP` session begins by first connecting to an `LDAP` server, also known as a `Directory System Agent`. The Domain Controller in AD actively listens for `LDAP` requests, such as security authentication requests.

![image](https://academy.hackthebox.com/storage/modules/22/NEW_LDAP_auth.png)

The relationship between AD and `LDAP` can be compared to Apache and HTTP. The same way Apache is a web server that uses the HTTP protocol, Active Directory is a directory server that uses the `LDAP` protocol.

While uncommon, you may come across organizations while performing an assessment that does not have AD but does have LDAP, meaning that they most likely use another type of `LDAP` server such as [OpenLDAP](https://en.wikipedia.org/wiki/OpenLDAP).

* * *

## AD LDAP Authentication

`LDAP` is set up to authenticate credentials against AD using a "BIND" operation to set the authentication state for an `LDAP` session. There are two types of `LDAP` authentication.

1. **Simple Authentication:** This includes anonymous authentication, unauthenticated authentication, and username/password authentication. Simple authentication means that a username and password create a BIND request to authenticate to the LDAP server.

2. **SASL Authentication:** The [Simple Authentication and Security Layer (SASL)](https://en.wikipedia.org/wiki/Simple_Authentication_and_Security_Layer) framework uses other authentication services, such as Kerberos, to bind to the `LDAP` server and then uses this authentication service (Kerberos in this example) to authenticate to `LDAP`. The `LDAP` server uses the `LDAP` protocol to send an `LDAP` message to the authorization service which initiates a series of challenge/response messages resulting in either successful or unsuccessful authentication. SASL can provide further security due to the separation of authentication methods from application protocols.


LDAP authentication messages are sent in cleartext by default so anyone can sniff out LDAP messages on the internal network. It is recommended to use TLS encryption or similar to safeguard this information in transit.

* * *

## LDAP Queries

We can communicate with the directory service using `LDAP` queries to ask the service for information. For example, the following query can be used to find all workstations in a network `(objectCategory=computer)` while this query can be used to find all domain controllers: `(&(objectCategory=Computer)(userAccountControl:1.2.840.113556.1.4.803:=8192))`.

LDAP queries can be used to perform user-related searches, such as " `(&(objectCategory=person)(objectClass=user))`" which searches for all users, as well as group related searches such as " `(objectClass=group)`" which returns all groups. Here is one example of a simple query to find all AD groups using the " `Get-ADObject`" cmdlet and the " `LDAPFilter parameter`".

#### LDAP Query - User Related Search

```powershell
PS C:\htb> Get-ADObject -LDAPFilter '(objectClass=group)' | select name

name
--
Administrators
Users
Guests
Print Operators
Backup Operators
Replicator
Remote Desktop Users
Network Configuration Operators
Performance Monitor Users
Performance Log Users
Distributed COM Users
IIS_IUSRS
Cryptographic Operators
Event Log Readers
Certificate Service DCOM Access
RDS Remote Access Servers
RDS Endpoint Servers
RDS Management Servers
Hyper-V Administrators
Access Control Assistance Operators
Remote Management Users

<SNIP>

```

We can also use LDAP queries to perform more detailed searches. This query searches the domain for all administratively disabled accounts.

#### LDAP Query - Detailed Search

```powershell
PS C:\htb> Get-ADObject -LDAPFilter '(&(objectCategory=person)(objectClass=user)(userAccountControl:1.2.840.113556.1.4.803:=2))' -Properties * | select samaccountname,useraccountcontrol

samaccountname                                                         useraccountcontrol
--------------                                                         ------------------
Guest                ACCOUNTDISABLE, PASSWD_NOTREQD, NORMAL_ACCOUNT, DONT_EXPIRE_PASSWORD
DefaultAccount       ACCOUNTDISABLE, PASSWD_NOTREQD, NORMAL_ACCOUNT, DONT_EXPIRE_PASSWORD
krbtgt                               ACCOUNTDISABLE, NORMAL_ACCOUNT, DONT_EXPIRE_PASSWORD
caroline.ali                               ACCOUNTDISABLE, PASSWD_NOTREQD, NORMAL_ACCOUNT
$SH2000-FPNHUU487JP0                       ACCOUNTDISABLE, PASSWD_NOTREQD, NORMAL_ACCOUNT
SM_00390f38b41e488ab                                       ACCOUNTDISABLE, NORMAL_ACCOUNT
SM_e081bc60d79c4597b                                       ACCOUNTDISABLE, NORMAL_ACCOUNT
SM_a9a4eed7ad2d4369a                                       ACCOUNTDISABLE, NORMAL_ACCOUNT
SM_d836f82078bf4cf89                                       ACCOUNTDISABLE, NORMAL_ACCOUNT
SM_6a24f488535649558                                       ACCOUNTDISABLE, NORMAL_ACCOUNT
SM_08a2324990674a87b                                       ACCOUNTDISABLE, NORMAL_ACCOUNT
SM_d1fea2710dc146b1b                                       ACCOUNTDISABLE, NORMAL_ACCOUNT
SM_b56189681baa441db                                       ACCOUNTDISABLE, NORMAL_ACCOUNT
SM_b72a918d27554863b                                       ACCOUNTDISABLE, NORMAL_ACCOUNT

```

More examples of basic and more advanced `LDAP` queries for AD can be found at the following links:

- LDAP queries related to AD [computers](https://ldapwiki.com/wiki/Wiki.jsp?page=Active%20Directory%20Computer%20Related%20LDAP%20Query)
- LDAP queries related to AD [users](https://ldapwiki.com/wiki/Wiki.jsp?page=Active%20Directory%20User%20Related%20Searches)
- LDAP queries related to AD [groups](https://ldapwiki.com/wiki/Wiki.jsp?page=Active%20Directory%20Group%20Related%20Searches)

`LDAP` queries are extremely powerful tools for querying Active Directory. We can harness their power to gather a wide variety of information, map out the AD environment, and hunt for misconfigurations. LDAP queries can be combined with filters to perform even more granular searches. The next two sections will cover both AD and LDAP search filters in-depth to prepare us for introducing a variety of AD enumeration tools in subsequent modules.

Note: When spawning your target, we ask you to wait for 3 minutes until the whole lab with all the configurations is set up so that the connection to your target works flawlessly.


# Active Directory Search Filters

* * *

The next two sections will cover the `Filter` and `LDAPFilter` parameters used by the [ActiveDirectory PowerShell module cmdlets](https://docs.microsoft.com/en-us/powershell/module/activedirectory/?view=windowsserver2022-ps). It is important to know how to build proper filter syntax for querying Active Directory using `PowerShell`. This knowledge gives us a deeper understanding of how our tools such as `PowerView` function under the hood and how we can further harness their power when enumerating Active Directory. It is also useful to understand how to formulate filters if you find yourself in a situation during an assessment without any of your tools available to you. Armed with this knowledge, you will be able to effectively "live off the land" and utilize built-in PowerShell cmdlets to perform your enumeration tasks (albeit slower than using many of the tools we will cover in this module).

* * *

## PowerShell Filters

Filters in PowerShell allow you to process piped output more efficiently and retrieve exactly the information you need from a command. Filters can be used to narrow down specific data in a large result or retrieve data that can then be piped to another command.

We can use filters with the `Filter` parameter. A basic example is querying a computer for installed software:

#### PowerShell - Filter Installed Software

```powershell
PS C:\htb> get-ciminstance win32_product | fl

IdentifyingNumber : {7FED75A1-600C-394B-8376-712E2A8861F2}
Name              : Microsoft Visual C++ 2017 x86 Additional Runtime - 14.12.25810
Vendor            : Microsoft Corporation
Version           : 14.12.25810
Caption           : Microsoft Visual C++ 2017 x86 Additional Runtime - 14.12.25810

IdentifyingNumber : {748D3A12-9B82-4B08-A0FF-CFDE83612E87}
Name              : VMware Tools
Vendor            : VMware, Inc.
Version           : 10.3.2.9925305
Caption           : VMware Tools

IdentifyingNumber : {EA8CB806-C109-4700-96B4-F1F268E5036C}
Name              : Local Administrator Password Solution
Vendor            : Microsoft Corporation
Version           : 6.2.0.0
Caption           : Local Administrator Password Solution

IdentifyingNumber : {2CD849A7-86A1-34A6-B8F9-D72F5B21A9AE}
Name              : Microsoft Visual C++ 2017 x64 Additional Runtime - 14.12.25810
Vendor            : Microsoft Corporation
Version           : 14.12.25810
Caption           : Microsoft Visual C++ 2017 x64 Additional Runtime - 14.12.25810

<SNIP>

```

The above command can provide considerable output. We can use the `Filter` parameter with the `notlike` operator to filter out all Microsoft software (which may be useful when enumerating a system for local privilege escalation vectors).

#### PowerShell - Filter Out Microsoft Software

```powershell
PS C:\htb> get-ciminstance win32_product -Filter "NOT Vendor like '%Microsoft%'" | fl

IdentifyingNumber : {748D3A12-9B82-4B08-A0FF-CFDE83612E87}
Name              : VMware Tools
Vendor            : VMware, Inc.
Version           : 10.3.2.9925305
Caption           : VMware Tools

```

* * *

## Operators

The `Filter` operator requires at least one operator, which can help narrow down search results or reduce a large amount of command output to something more digestible. Filtering properly is important, especially when enumerating large environments and looking for very specific information in the command output. The following operators can be used with the `Filter` parameter:

| **Filter** | **Meaning** |
| --- | --- |
| -eq | Equal to |
| -le | Less than or equal to |
| -ge | Greater than or equal to |
| -ne | Not equal to |
| -lt | Less than |
| -gt | Greater than |
| -approx | Approximately equal to |
| -bor | Bitwise OR |
| -band | Bitwise AND |
| -recursivematch | Recursive match |
| -like | Like |
| -notlike | Not like |
| -and | Boolean AND |
| -or | Boolean OR |
| -not | Boolean NOT |

* * *

## Filter Examples: AD Object Properties

The filter can be used with operators to compare, exclude, search for, etc., a variety of AD object properties. Filters can be wrapped in curly braces, single quotes, parentheses, or double-quotes. For example, the following simple search filter using `Get-ADUser` to find information about the user `Sally Jones` can be written as follows:

#### PowerShell - Filter Examples

```powershell
Get-ADUser -Filter "name -eq 'sally jones'"
Get-ADUser -Filter {name -eq 'sally jones'}
Get-ADUser -Filter 'name -eq "sally jones"'

```

As seen above, the property value (here, `sally jones`) can be wrapped in single or double-quotes. The asterisk ( `*`) can be used as a [wildcard](https://ss64.com/ps/syntax-wildcards.html) when performing queries. The command `Get-ADUser -filter {name -like "joe*"}` using a wildcard would return all domain users whose name start with `joe` (joe, joel, etc.). When using filters, certain characters must be escaped:

| **Character** | **Escaped As** | **Note** |
| --- | --- | --- |
| “ | \`” | Only needed if the data is enclosed in double-quotes. |
| ‘ | \\’ | Only needed if the data is enclosed in single quotes. |
| NUL | \\00 | Standard LDAP escape sequence. |
| \ | \\5c | Standard LDAP escape sequence. |
| \* | \\2a | Escaped automatically, but only in -eq and -ne comparisons. Use -like and -notlike operators for wildcard comparison. |
| ( | /28 | Escaped automatically. |
| ) | /29 | Escaped automatically. |
| / | /2f | Escaped automatically. |

* * *

Let's try out some of these filters to enumerate the `INLANEFREIGHT.LOCAL` domain. We can search all domain computers for interesting hostnames. SQL servers are a particularly juicy target on internal assessments. The below command searches all hosts in the domain using `Get-ADComputer`, filtering on the `DNSHostName` property that contains the word `SQL`.

#### PowerShell - Filter For SQL

```powershell
PS C:\htb> Get-ADComputer  -Filter "DNSHostName -like 'SQL*'"

DistinguishedName : CN=SQL01,OU=SQL Servers,OU=Servers,DC=INLANEFREIGHT,DC=LOCAL
DNSHostName       : SQL01.INLANEFREIGHT.LOCAL
Enabled           : True
Name              : SQL01
ObjectClass       : computer
ObjectGUID        : 42cc9264-1655-4bfa-b5f9-21101afb33d0
SamAccountName    : SQL01$
SID               : S-1-5-21-2974783224-3764228556-2640795941-1104
UserPrincipalName :

```

Next, let's search for administrative groups. We can do this by filtering on the `adminCount` attribute. The group with this attribute set to `1` are protected by [AdminSDHolder](https://docs.microsoft.com/en-us/windows-server/identity/ad-ds/plan/security-best-practices/appendix-c--protected-accounts-and-groups-in-active-directory) and known as protected groups. `AdminSDHolder` is owned by the Domain Admins group. It has the privileges to change the permissions of objects in Active Directory. As discussed above, we can pipe the filtered command output and select just the group names.

#### PowerShell - Filter Administrative Groups

```powershell
PS C:\htb> Get-ADGroup -Filter "adminCount -eq 1" | select Name

Name
----
Administrators
Print Operators
Backup Operators
Replicator
Domain Controllers
Schema Admins
Enterprise Admins
Domain Admins
Server Operators
Account Operators
Read-only Domain Controllers
Security Operations

```

We can also combine filters. Let's search for all administrative users with the `DoesNotRequirePreAuth` attribute set, meaning that they can be ASREPRoasted (this attack will be covered in-depth in later modules). Here we are selecting all domain users and specifying two conditions with the `-eq` operator.

#### PowerShell - Filter Administrative Users

```powershell
PS C:\htb> Get-ADUser -Filter {adminCount -eq '1' -and DoesNotRequirePreAuth -eq 'True'}

DistinguishedName : CN=Jenna Smith,OU=Server Team,OU=IT,OU=Employees,DC=INLANEFREIGHT,DC=LOCAL
GivenName         : jenna
Name              : Jenna Smith
ObjectClass       : user
ObjectGUID        : ea3c930f-aa8e-4fdc-987c-4a9ee1a75409
SamAccountName    : jenna.smith
SID               : S-1-5-21-2974783224-3764228556-2640795941-1999
Surname           : smith
UserPrincipalName : jenna.smith@inlanefreight

```

Finally, let's see an example of combining filters and piping output multiple times to find our desired information. The following command can be used to find all administrative users with the " `servicePrincipalName`" attribute set, meaning that they can likely be subject to a Kerberoasting attack. This example applies the `Filter` parameter to find accounts with the `adminCount` attribute set to `1`, pipes this output to find all accounts with a Service Principal Name (SPN), and finally selects a few attributes about the accounts, including the account name, group membership, and the SPN.

#### PowerShell - Find Administrative Users with the ServicePrincipalName

```powershell
PS C:\htb> Get-ADUser -Filter "adminCount -eq '1'" -Properties * | where servicePrincipalName -ne $null | select SamAccountName,MemberOf,ServicePrincipalName | fl

SamAccountName       : krbtgt
MemberOf             : {CN=Denied RODC Password Replication Group,CN=Users,DC=INLANEFREIGHT,DC=LOCAL}
ServicePrincipalName : {kadmin/changepw}

SamAccountName       : sqlqa
MemberOf             : {CN=Domain Admins,CN=Users,DC=INLANEFREIGHT,DC=LOCAL}
ServicePrincipalName : {MSSQL_svc_qa/inlanefreight.local:1443}

```

It would take an extremely long time to enumerate an Active Directory environment using many combinations of the commands above. This last example could be performed quickly and easily with tools such as `PowerView` or `Rubeus`. Nevertheless, it is important to apply filters competently when enumerating AD as the output from tools like `PowerView` can even be further filtered to provide us with precise results.

Note: When spawning your target, we ask you to wait for 3 minutes until the whole lab with all the configurations is set up so that the connection to your target works flawlessly.


# LDAP Search Filters

* * *

## Basic LDAP Filter Syntax and Operators

The `LDAPFilter` parameter with the same cmdlets lets us use LDAP search filters when searching for information. The syntax for these filters is defined in [RFC 4515 - Lightweight Directory Access Protocol (LDAP): String Representation of Search Filters](https://tools.ietf.org/html/rfc4515).

LDAP filters must have one or more criteria. If more than one criteria exist, they can be concatenated together using logical `AND` or `OR` operators. These operators are always placed in the front of the criteria (operands), which is also referred to as [Polish Notation](https://en.wikipedia.org/wiki/Polish_notation).

Filter rules are enclosed in parentheses and can be grouped by surrounding the group in parentheses and using one of the following comparison operators:

| **Operator** | **Function** |
| --- | --- |
| `&` | and |
| `|` | or |
| `!` | not |

Some example `AND` and `OR` operations are as follows:

`AND` Operation:

- One criteria: `(& (..C1..) (..C2..))`
- More than two criteria: `(& (..C1..) (..C2..) (..C3..))`

`OR` Operation:

- One criteria: `(| (..C1..) (..C2..))`
- More than two criteria: `(| (..C1..) (..C2..) (..C3..))`

We can also have nested operations, for example " `(|(& (..C1..) (..C2..))(& (..C3..) (..C4..)))`" translates to " `(C1 AND C2) OR (C3 AND C4)`".

* * *

## Search Criteria

When writing an LDAP search filter, we need to specify a rule requirement for the LDAP attribute in question (i.e. " `(displayName=william)`"). The following rules can be used to specify our search criteria:

| **Criteria** | **Rule** | **Example** |
| --- | --- | --- |
| Equal to | (attribute=123) | (&(objectclass=user)(displayName=Smith) |
| Not equal to | (!(attribute=123)) | (!objectClass=group) |
| Present | (attribute=\*) | (department=\*) |
| Not present | (!(attribute=\*)) | (!homeDirectory=\*) |
| Greater than | (attribute>=123) | (maxStorage=100000) |
| Less than | (attribute<=123) | (maxStorage<=100000) |
| Approximate match | (attribute~=123) | (sAMAccountName~=Jason) |
| Wildcards | (attribute=\*A) | (givenName=\*Sam) |

This [link](https://docs.bmc.com/docs/fpsc121/ldap-attributes-and-associated-fields-495323340.html) contains a large listing of User Attributes, and the below is a list of all Base Attributes.

Full list of Base Attributes

| **LDAP Display Name** | **CN** | **Attribute ID** |
| --- | --- | --- |
| `accountExpires` | Account-Expires | 1.2.840.113556.1.4.159 |
| `accountNameHistory` | Account-Name-History | 1.2.840.113556.1.4.1307 |
| `aCSAggregateTokenRatePerUser` | ACS-Aggregate-Token-Rate-Per-User | 1.2.840.113556.1.4.760 |
| `aCSAllocableRSVPBandwidth` | ACS-Allocable-RSVP-Bandwidth | 1.2.840.113556.1.4.766 |
| `aCSCacheTimeout` | ACS-Cache-Timeout | 1.2.840.113556.1.4.779 |
| `aCSDirection` | ACS-Direction | 1.2.840.113556.1.4.757 |
| `aCSDSBMDeadTime` | ACS-DSBM-DeadTime | 1.2.840.113556.1.4.778 |
| `aCSDSBMPriority` | ACS-DSBM-Priority | 1.2.840.113556.1.4.776 |
| `aCSDSBMRefresh` | ACS-DSBM-Refresh | 1.2.840.113556.1.4.777 |
| `aCSEnableACSService` | ACS-Enable-ACS-Service | 1.2.840.113556.1.4.770 |
| `aCSEnableRSVPAccounting` | ACS-Enable-RSVP-Accounting | 1.2.840.113556.1.4.899 |
| `aCSEnableRSVPMessageLogging` | ACS-Enable-RSVP-Message-Logging | 1.2.840.113556.1.4.768 |
| `aCSEventLogLevel` | ACS-Event-Log-Level | 1.2.840.113556.1.4.769 |
| `aCSIdentityName` | ACS-Identity-Name | 1.2.840.113556.1.4.784 |
| `aCSMaxAggregatePeakRatePerUser` | ACS-Max-Aggregate-Peak-Rate-Per-User | 1.2.840.113556.1.4.897 |
| `aCSMaxDurationPerFlow` | ACS-Max-Duration-Per-Flow | 1.2.840.113556.1.4.761 |
| `aCSMaximumSDUSize` | ACS-Maximum-SDU-Size | 1.2.840.113556.1.4.1314 |
| `aCSMaxNoOfAccountFiles` | ACS-Max-No-Of-Account-Files | 1.2.840.113556.1.4.901 |
| `aCSMaxNoOfLogFiles` | ACS-Max-No-Of-Log-Files | 1.2.840.113556.1.4.774 |
| `aCSMaxPeakBandwidth` | ACS-Max-Peak-Bandwidth | 1.2.840.113556.1.4.767 |
| `aCSMaxPeakBandwidthPerFlow` | ACS-Max-Peak-Bandwidth-Per-Flow | 1.2.840.113556.1.4.759 |
| `aCSMaxSizeOfRSVPAccountFile` | ACS-Max-Size-Of-RSVP-Account-File | 1.2.840.113556.1.4.902 |
| `aCSMaxSizeOfRSVPLogFile` | ACS-Max-Size-Of-RSVP-Log-File | 1.2.840.113556.1.4.775 |
| `aCSMaxTokenBucketPerFlow` | ACS-Max-Token-Bucket-Per-Flow | 1.2.840.113556.1.4.1313 |
| `aCSMaxTokenRatePerFlow` | ACS-Max-Token-Rate-Per-Flow | 1.2.840.113556.1.4.758 |
| `aCSMinimumDelayVariation` | ACS-Minimum-Delay-Variation | 1.2.840.113556.1.4.1317 |
| `aCSMinimumLatency` | ACS-Minimum-Latency | 1.2.840.113556.1.4.1316 |
| `aCSMinimumPolicedSize` | ACS-Minimum-Policed-Size | 1.2.840.113556.1.4.1315 |
| `aCSNonReservedMaxSDUSize` | ACS-Non-Reserved-Max-SDU-Size | 1.2.840.113556.1.4.1320 |
| `aCSNonReservedMinPolicedSize` | ACS-Non-Reserved-Min-Policed-Size | 1.2.840.113556.1.4.1321 |
| `aCSNonReservedPeakRate` | ACS-Non-Reserved-Peak-Rate | 1.2.840.113556.1.4.1318 |
| `aCSNonReservedTokenSize` | ACS-Non-Reserved-Token-Size | 1.2.840.113556.1.4.1319 |
| `aCSNonReservedTxLimit` | ACS-Non-Reserved-Tx-Limit | 1.2.840.113556.1.4.780 |
| `aCSNonReservedTxSize` | ACS-Non-Reserved-Tx-Size | 1.2.840.113556.1.4.898 |
| `aCSPermissionBits` | ACS-Permission-Bits | 1.2.840.113556.1.4.765 |
| `aCSPolicyName` | ACS-Policy-Name | 1.2.840.113556.1.4.772 |
| `aCSPriority` | ACS-Priority | 1.2.840.113556.1.4.764 |
| `aCSRSVPAccountFilesLocation` | ACS-RSVP-Account-Files-Location | 1.2.840.113556.1.4.900 |
| `aCSRSVPLogFilesLocation` | ACS-RSVP-Log-Files-Location | 1.2.840.113556.1.4.773 |
| `aCSServerList` | ACS-Server-List | 1.2.840.113556.1.4.1312 |
| `aCSServiceType` | ACS-Service-Type | 1.2.840.113556.1.4.762 |
| `aCSTimeOfDay` | ACS-Time-Of-Day | 1.2.840.113556.1.4.756 |
| `aCSTotalNoOfFlows` | ACS-Total-No-Of-Flows | 1.2.840.113556.1.4.763 |
| `additionalTrustedServiceNames` | Additional-Trusted-Service-Names | 1.2.840.113556.1.4.889 |
| `addressBookRoots` | Address-Book-Roots | 1.2.840.113556.1.4.1244 |
| `addressEntryDisplayTable` | Address-Entry-Display-Table | 1.2.840.113556.1.2.324 |
| `addressEntryDisplayTableMSDOS` | Address-Entry-Display-Table-MSDOS | 1.2.840.113556.1.2.400 |
| `addressSyntax` | Address-Syntax | 1.2.840.113556.1.2.255 |
| `addressType` | Address-Type | 1.2.840.113556.1.2.350 |
| `adminContextMenu` | Admin-Context-Menu | 1.2.840.113556.1.4.614 |
| `adminCount` | Admin-Count | 1.2.840.113556.1.4.150 |
| `adminDescription` | Admin-Description | 1.2.840.113556.1.2.226 |
| `adminDisplayName` | Admin-Display-Name | 1.2.840.113556.1.2.194 |
| `adminPropertyPages` | Admin-Property-Pages | 1.2.840.113556.1.4.562 |
| `allowedAttributes` | Allowed-Attributes | 1.2.840.113556.1.4.913 |
| `allowedAttributesEffective` | Allowed-Attributes-Effective | 1.2.840.113556.1.4.914 |
| `allowedChildClasses` | Allowed-Child-Classes | 1.2.840.113556.1.4.911 |
| `allowedChildClassesEffective` | Allowed-Child-Classes-Effective | 1.2.840.113556.1.4.912 |
| `altSecurityIdentities` | Alt-Security-Identities | 1.2.840.113556.1.4.867 |
| `aNR` | ANR | 1.2.840.113556.1.4.1208 |
| `applicationName` | Application-Name | 1.2.840.113556.1.4.218 |
| `appliesTo` | Applies-To | 1.2.840.113556.1.4.341 |
| `appSchemaVersion` | App-Schema-Version | 1.2.840.113556.1.4.848 |
| `assetNumber` | Asset-Number | 1.2.840.113556.1.4.283 |
| `assistant` | Assistant | 1.2.840.113556.1.4.652 |
| `assocNTAccount` | Assoc-NT-Account | 1.2.840.113556.1.4.1213 |
| `attributeDisplayNames` | Attribute-Display-Names | 1.2.840.113556.1.4.748 |
| `attributeID` | Attribute-ID | 1.2.840.113556.1.2.30 |
| `attributeSecurityGUID` | Attribute-Security-GUID | 1.2.840.113556.1.4.149 |
| `attributeSyntax` | Attribute-Syntax | 1.2.840.113556.1.2.32 |
| `attributeTypes` | Attribute-Types | 2.5.21.5 |
| `auditingPolicy` | Auditing-Policy | 1.2.840.113556.1.4.202 |
| `authenticationOptions` | Authentication-Options | 1.2.840.113556.1.4.11 |
| `authorityRevocationList` | Authority-Revocation-List | 2.5.4.38 |
| `auxiliaryClass` | Auxiliary-Class | 1.2.840.113556.1.2.351 |
| `badPasswordTime` | Bad-Password-Time | 1.2.840.113556.1.4.49 |
| `badPwdCount` | Bad-Pwd-Count | 1.2.840.113556.1.4.12 |
| `birthLocation` | Birth-Location | 1.2.840.113556.1.4.332 |
| `bridgeheadServerListBL` | Bridgehead-Server-List-BL | 1.2.840.113556.1.4.820 |
| `bridgeheadTransportList` | Bridgehead-Transport-List | 1.2.840.113556.1.4.819 |
| `builtinCreationTime` | Builtin-Creation-Time | 1.2.840.113556.1.4.13 |
| `builtinModifiedCount` | Builtin-Modified-Count | 1.2.840.113556.1.4.14 |
| `businessCategory` | Business-Category | 2.5.4.15 |
| `bytesPerMinute` | Bytes-Per-Minute | 1.2.840.113556.1.4.284 |
| `c` | Country-Name | 2.5.4.6 |
| `cACertificate` | CA-Certificate | 2.5.4.37 |
| `cACertificateDN` | CA-Certificate-DN | 1.2.840.113556.1.4.697 |
| `cAConnect` | CA-Connect | 1.2.840.113556.1.4.687 |
| `canonicalName` | Canonical-Name | 1.2.840.113556.1.4.916 |
| `canUpgradeScript` | Can-Upgrade-Script | 1.2.840.113556.1.4.815 |
| `catalogs` | Catalogs | 1.2.840.113556.1.4.675 |
| `categories` | Categories | 1.2.840.113556.1.4.672 |
| `categoryId` | Category-Id | 1.2.840.113556.1.4.322 |
| `cAUsages` | CA-Usages | 1.2.840.113556.1.4.690 |
| `cAWEBURL` | CA-WEB-URL | 1.2.840.113556.1.4.688 |
| `certificateAuthorityObject` | Certificate-Authority-Object | 1.2.840.113556.1.4.684 |
| `certificateRevocationList` | Certificate-Revocation-List | 2.5.4.39 |
| `certificateTemplates` | Certificate-Templates | 1.2.840.113556.1.4.823 |
| `classDisplayName` | Class-Display-Name | 1.2.840.113556.1.4.610 |
| `cn` | Common-Name | 2.5.4.3 |
| `co` | Text-Country | 1.2.840.113556.1.2.131 |
| `codePage` | Code-Page | 1.2.840.113556.1.4.16 |
| `cOMClassID` | COM-ClassID | 1.2.840.113556.1.4.19 |
| `cOMCLSID` | COM-CLSID | 1.2.840.113556.1.4.249 |
| `cOMInterfaceID` | COM-InterfaceID | 1.2.840.113556.1.4.20 |
| `comment` | User-Comment | 1.2.840.113556.1.4.156 |
| `cOMOtherProgId` | COM-Other-Prog-Id | 1.2.840.113556.1.4.253 |
| `company` | Company | 1.2.840.113556.1.2.146 |
| `cOMProgID` | COM-ProgID | 1.2.840.113556.1.4.21 |
| `cOMTreatAsClassId` | COM-Treat-As-Class-Id | 1.2.840.113556.1.4.251 |
| `cOMTypelibId` | COM-Typelib-Id | 1.2.840.113556.1.4.254 |
| `cOMUniqueLIBID` | COM-Unique-LIBID | 1.2.840.113556.1.4.250 |
| `contentIndexingAllowed` | Content-Indexing-Allowed | 1.2.840.113556.1.4.24 |
| `contextMenu` | Context-Menu | 1.2.840.113556.1.4.499 |
| `controlAccessRights` | Control-Access-Rights | 1.2.840.113556.1.4.200 |
| `cost` | Cost | 1.2.840.113556.1.2.135 |
| `countryCode` | Country-Code | 1.2.840.113556.1.4.25 |
| `createDialog` | Create-Dialog | 1.2.840.113556.1.4.810 |
| `createTimeStamp` | Create-Time-Stamp | 2.5.18.1 |
| `createWizardExt` | Create-Wizard-Ext | 1.2.840.113556.1.4.812 |
| `creationTime` | Creation-Time | 1.2.840.113556.1.4.26 |
| `creationWizard` | Creation-Wizard | 1.2.840.113556.1.4.498 |
| `creator` | Creator | 1.2.840.113556.1.4.679 |
| `cRLObject` | CRL-Object | 1.2.840.113556.1.4.689 |
| `cRLPartitionedRevocationList` | CRL-Partitioned-Revocation-List | 1.2.840.113556.1.4.683 |
| `crossCertificatePair` | Cross-Certificate-Pair | 2.5.4.40 |
| `currentLocation` | Current-Location | 1.2.840.113556.1.4.335 |
| `currentParentCA` | Current-Parent-CA | 1.2.840.113556.1.4.696 |
| `currentValue` | Current-Value | 1.2.840.113556.1.4.27 |
| `currMachineId` | Curr-Machine-Id | 1.2.840.113556.1.4.337 |
| `dBCSPwd` | DBCS-Pwd | 1.2.840.113556.1.4.55 |
| `dc` | Domain-Component | 0.9.2342.19200300.100.1.25 |
| `defaultClassStore` | Default-Class-Store | 1.2.840.113556.1.4.213 |
| `defaultGroup` | Default-Group | 1.2.840.113556.1.4.480 |
| `defaultHidingValue` | Default-Hiding-Value | 1.2.840.113556.1.4.518 |
| `defaultLocalPolicyObject` | Default-Local-Policy-Object | 1.2.840.113556.1.4.57 |
| `defaultObjectCategory` | Default-Object-Category | 1.2.840.113556.1.4.783 |
| `defaultPriority` | Default-Priority | 1.2.840.113556.1.4.232 |
| `defaultSecurityDescriptor` | Default-Security-Descriptor | 1.2.840.113556.1.4.224 |
| `deltaRevocationList` | Delta-Revocation-List | 2.5.4.53 |
| `department` | Department | 1.2.840.113556.1.2.141 |
| `description` | Description | 2.5.4.13 |
| `desktopProfile` | Desktop-Profile | 1.2.840.113556.1.4.346 |
| `destinationIndicator` | Destination-Indicator | 2.5.4.27 |
| `dhcpClasses` | dhcp-Classes | 1.2.840.113556.1.4.715 |
| `dhcpFlags` | dhcp-Flags | 1.2.840.113556.1.4.700 |
| `dhcpIdentification` | dhcp-Identification | 1.2.840.113556.1.4.701 |
| `dhcpMask` | dhcp-Mask | 1.2.840.113556.1.4.706 |
| `dhcpMaxKey` | dhcp-MaxKey | 1.2.840.113556.1.4.719 |
| `dhcpObjDescription` | dhcp-Obj-Description | 1.2.840.113556.1.4.703 |
| `dhcpObjName` | dhcp-Obj-Name | 1.2.840.113556.1.4.702 |
| `dhcpOptions` | dhcp-Options | 1.2.840.113556.1.4.714 |
| `dhcpProperties` | dhcp-Properties | 1.2.840.113556.1.4.718 |
| `dhcpRanges` | dhcp-Ranges | 1.2.840.113556.1.4.707 |
| `dhcpReservations` | dhcp-Reservations | 1.2.840.113556.1.4.709 |
| `dhcpServers` | dhcp-Servers | 1.2.840.113556.1.4.704 |
| `dhcpSites` | dhcp-Sites | 1.2.840.113556.1.4.708 |
| `dhcpState` | dhcp-State | 1.2.840.113556.1.4.717 |
| `dhcpSubnets` | dhcp-Subnets | 1.2.840.113556.1.4.705 |
| `dhcpType` | dhcp-Type | 1.2.840.113556.1.4.699 |
| `dhcpUniqueKey` | dhcp-Unique-Key | 1.2.840.113556.1.4.698 |
| `dhcpUpdateTime` | dhcp-Update-Time | 1.2.840.113556.1.4.720 |
| `directReports` | Reports | 1.2.840.113556.1.2.436 |
| `displayName` | Display-Name | 1.2.840.113556.1.2.13 |
| `displayNamePrintable` | Display-Name-Printable | 1.2.840.113556.1.2.353 |
| `distinguishedName` | Obj-Dist-Name | 2.5.4.49 |
| `dITContentRules` | DIT-Content-Rules | 2.5.21.2 |
| `division` | Division | 1.2.840.113556.1.4.261 |
| `dMDLocation` | DMD-Location | 1.2.840.113556.1.2.36 |
| `dmdName` | DMD-Name | 1.2.840.113556.1.2.598 |
| `dNReferenceUpdate` | DN-Reference-Update | 1.2.840.113556.1.4.1242 |
| `dnsAllowDynamic` | Dns-Allow-Dynamic | 1.2.840.113556.1.4.378 |
| `dnsAllowXFR` | Dns-Allow-XFR | 1.2.840.113556.1.4.379 |
| `dNSHostName` | DNS-Host-Name | 1.2.840.113556.1.4.619 |
| `dnsNotifySecondaries` | Dns-Notify-Secondaries | 1.2.840.113556.1.4.381 |
| `dNSProperty` | DNS-Property | 1.2.840.113556.1.4.1306 |
| `dnsRecord` | Dns-Record | 1.2.840.113556.1.4.382 |
| `dnsRoot` | Dns-Root | 1.2.840.113556.1.4.28 |
| `dnsSecureSecondaries` | Dns-Secure-Secondaries | 1.2.840.113556.1.4.380 |
| `dNSTombstoned` | DNS-Tombstoned | 1.2.840.113556.1.4.1414 |
| `domainCAs` | Domain-Certificate-Authorities | 1.2.840.113556.1.4.668 |
| `domainCrossRef` | Domain-Cross-Ref | 1.2.840.113556.1.4.472 |
| `domainID` | Domain-ID | 1.2.840.113556.1.4.686 |
| `domainIdentifier` | Domain-Identifier | 1.2.840.113556.1.4.755 |
| `domainPolicyObject` | Domain-Policy-Object | 1.2.840.113556.1.4.32 |
| `domainPolicyReference` | Domain-Policy-Reference | 1.2.840.113556.1.4.422 |
| `domainReplica` | Domain-Replica | 1.2.840.113556.1.4.158 |
| `domainWidePolicy` | Domain-Wide-Policy | 1.2.840.113556.1.4.421 |
| `driverName` | Driver-Name | 1.2.840.113556.1.4.229 |
| `driverVersion` | Driver-Version | 1.2.840.113556.1.4.276 |
| `dSASignature` | DSA-Signature | 1.2.840.113556.1.2.74 |
| `dSCorePropagationData` | DS-Core-Propagation-Data | 1.2.840.113556.1.4.1357 |
| `dSHeuristics` | DS-Heuristics | 1.2.840.113556.1.2.212 |
| `dSUIAdminMaximum` | DS-UI-Admin-Maximum | 1.2.840.113556.1.4.1344 |
| `dSUIAdminNotification` | DS-UI-Admin-Notification | 1.2.840.113556.1.4.1343 |
| `dSUIShellMaximum` | DS-UI-Shell-Maximum | 1.2.840.113556.1.4.1345 |
| `dynamicLDAPServer` | Dynamic-LDAP-Server | 1.2.840.113556.1.4.537 |
| `eFSPolicy` | EFSPolicy | 1.2.840.113556.1.4.268 |
| `employeeID` | Employee-ID | 1.2.840.113556.1.4.35 |
| `employeeNumber` | Employee-Number | 1.2.840.113556.1.2.610 |
| `employeeType` | Employee-Type | 1.2.840.113556.1.2.613 |
| `Enabled` | Enabled | 1.2.840.113556.1.2.557 |
| `enabledConnection` | Enabled-Connection | 1.2.840.113556.1.4.36 |
| `enrollmentProviders` | Enrollment-Providers | 1.2.840.113556.1.4.825 |
| `extendedAttributeInfo` | Extended-Attribute-Info | 1.2.840.113556.1.4.909 |
| `extendedCharsAllowed` | Extended-Chars-Allowed | 1.2.840.113556.1.2.380 |
| `extendedClassInfo` | Extended-Class-Info | 1.2.840.113556.1.4.908 |
| `extensionName` | Extension-Name | 1.2.840.113556.1.2.227 |
| `facsimileTelephoneNumber` | Facsimile-Telephone-Number | 2.5.4.23 |
| `fileExtPriority` | File-Ext-Priority | 1.2.840.113556.1.4.816 |
| `flags` | Flags | 1.2.840.113556.1.4.38 |
| `flatName` | Flat-Name | 1.2.840.113556.1.4.511 |
| `forceLogoff` | Force-Logoff | 1.2.840.113556.1.4.39 |
| `foreignIdentifier` | Foreign-Identifier | 1.2.840.113556.1.4.356 |
| `friendlyNames` | Friendly-Names | 1.2.840.113556.1.4.682 |
| `fromEntry` | From-Entry | 1.2.840.113556.1.4.910 |
| `fromServer` | From-Server | 1.2.840.113556.1.4.40 |
| `frsComputerReference` | Frs-Computer-Reference | 1.2.840.113556.1.4.869 |
| `frsComputerReferenceBL` | Frs-Computer-Reference-BL | 1.2.840.113556.1.4.870 |
| `fRSControlDataCreation` | FRS-Control-Data-Creation | 1.2.840.113556.1.4.871 |
| `fRSControlInboundBacklog` | FRS-Control-Inbound-Backlog | 1.2.840.113556.1.4.872 |
| `fRSControlOutboundBacklog` | FRS-Control-Outbound-Backlog | 1.2.840.113556.1.4.873 |
| `fRSDirectoryFilter` | FRS-Directory-Filter | 1.2.840.113556.1.4.484 |
| `fRSDSPoll` | FRS-DS-Poll | 1.2.840.113556.1.4.490 |
| `fRSExtensions` | FRS-Extensions | 1.2.840.113556.1.4.536 |
| `fRSFaultCondition` | FRS-Fault-Condition | 1.2.840.113556.1.4.491 |
| `fRSFileFilter` | FRS-File-Filter | 1.2.840.113556.1.4.483 |
| `fRSFlags` | FRS-Flags | 1.2.840.113556.1.4.874 |
| `fRSLevelLimit` | FRS-Level-Limit | 1.2.840.113556.1.4.534 |
| `fRSMemberReference` | FRS-Member-Reference | 1.2.840.113556.1.4.875 |
| `fRSMemberReferenceBL` | FRS-Member-Reference-BL | 1.2.840.113556.1.4.876 |
| `fRSPartnerAuthLevel` | FRS-Partner-Auth-Level | 1.2.840.113556.1.4.877 |
| `fRSPrimaryMember` | FRS-Primary-Member | 1.2.840.113556.1.4.878 |
| `fRSReplicaSetGUID` | FRS-Replica-Set-GUID | 1.2.840.113556.1.4.533 |
| `fRSReplicaSetType` | FRS-Replica-Set-Type | 1.2.840.113556.1.4.31 |
| `fRSRootPath` | FRS-Root-Path | 1.2.840.113556.1.4.487 |
| `fRSRootSecurity` | FRS-Root-Security | 1.2.840.113556.1.4.535 |
| `fRSServiceCommand` | FRS-Service-Command | 1.2.840.113556.1.4.500 |
| `fRSServiceCommandStatus` | FRS-Service-Command-Status | 1.2.840.113556.1.4.879 |
| `fRSStagingPath` | FRS-Staging-Path | 1.2.840.113556.1.4.488 |
| `fRSTimeLastCommand` | FRS-Time-Last-Command | 1.2.840.113556.1.4.880 |
| `fRSTimeLastConfigChange` | FRS-Time-Last-Config-Change | 1.2.840.113556.1.4.881 |
| `fRSUpdateTimeout` | FRS-Update-Timeout | 1.2.840.113556.1.4.485 |
| `fRSVersion` | FRS-Version | 1.2.840.113556.1.4.882 |
| `fRSVersionGUID` | FRS-Version-GUID | 1.2.840.113556.1.4.43 |
| `fRSWorkingPath` | FRS-Working-Path | 1.2.840.113556.1.4.486 |
| `fSMORoleOwner` | FSMO-Role-Owner | 1.2.840.113556.1.4.369 |
| `garbageCollPeriod` | Garbage-Coll-Period | 1.2.840.113556.1.2.301 |
| `generatedConnection` | Generated-Connection | 1.2.840.113556.1.4.41 |
| `generationQualifier` | Generation-Qualifier | 2.5.4.44 |
| `givenName` | Given-Name | 2.5.4.42 |
| `globalAddressList` | Global-Address-List | 1.2.840.113556.1.4.1245 |
| `governsID` | Governs-ID | 1.2.840.113556.1.2.22 |
| `gPCFileSysPath` | GPC-File-Sys-Path | 1.2.840.113556.1.4.894 |
| `gPCFunctionalityVersion` | GPC-Functionality-Version | 1.2.840.113556.1.4.893 |
| `gPCMachineExtensionNames` | GPC-Machine-Extension-Names | 1.2.840.113556.1.4.1348 |
| `gPCUserExtensionNames` | GPC-User-Extension-Names | 1.2.840.113556.1.4.1349 |
| `gPLink` | GP-Link | 1.2.840.113556.1.4.891 |
| `gPOptions` | GP-Options | 1.2.840.113556.1.4.892 |
| `groupAttributes` | Group-Attributes | 1.2.840.113556.1.4.152 |
| `groupMembershipSAM` | Group-Membership-SAM | 1.2.840.113556.1.4.166 |
| `groupPriority` | Group-Priority | 1.2.840.113556.1.4.345 |
| `groupsToIgnore` | Groups-to-Ignore | 1.2.840.113556.1.4.344 |
| `groupType` | Group-Type | 1.2.840.113556.1.4.750 |
| `hasMasterNCs` | Has-Master-NCs | 1.2.840.113556.1.2.14 |
| `hasPartialReplicaNCs` | Has-Partial-Replica-NCs | 1.2.840.113556.1.2.15 |
| `helpData16` | Help-Data16 | 1.2.840.113556.1.2.402 |
| `helpData32` | Help-Data32 | 1.2.840.113556.1.2.9 |
| `helpFileName` | Help-File-Name | 1.2.840.113556.1.2.327 |
| `homeDirectory` | Home-Directory | 1.2.840.113556.1.4.44 |
| `homeDrive` | Home-Drive | 1.2.840.113556.1.4.45 |
| `homePhone` | Phone-Home-Primary | 0.9.2342.19200300.100.1.20 |
| `homePostalAddress` | Address-Home | 1.2.840.113556.1.2.617 |
| `iconPath` | Icon-Path | 1.2.840.113556.1.4.219 |
| `implementedCategories` | Implemented-Categories | 1.2.840.113556.1.4.320 |
| `indexedScopes` | IndexedScopes | 1.2.840.113556.1.4.681 |
| `info` | Comment | 1.2.840.113556.1.2.81 |
| `initialAuthIncoming` | Initial-Auth-Incoming | 1.2.840.113556.1.4.539 |
| `initialAuthOutgoing` | Initial-Auth-Outgoing | 1.2.840.113556.1.4.540 |
| `initials` | Initials | 2.5.4.43 |
| `installUiLevel` | Install-Ui-Level | 1.2.840.113556.1.4.847 |
| `instanceType` | Instance-Type | 1.2.840.113556.1.2.1 |
| `internationalISDNNumber` | International-ISDN-Number | 2.5.4.25 |
| `interSiteTopologyFailover` | Inter-Site-Topology-Failover | 1.2.840.113556.1.4.1248 |
| `interSiteTopologyGenerator` | Inter-Site-Topology-Generator | 1.2.840.113556.1.4.1246 |
| `interSiteTopologyRenew` | Inter-Site-Topology-Renew | 1.2.840.113556.1.4.1247 |
| `invocationId` | Invocation-Id | 1.2.840.113556.1.2.115 |
| `ipPhone` | Phone-Ip-Primary | 1.2.840.113556.1.4.721 |
| `ipsecData` | Ipsec-Data | 1.2.840.113556.1.4.623 |
| `ipsecDataType` | Ipsec-Data-Type | 1.2.840.113556.1.4.622 |
| `ipsecFilterReference` | Ipsec-Filter-Reference | 1.2.840.113556.1.4.629 |
| `ipsecID` | Ipsec-ID | 1.2.840.113556.1.4.621 |
| `ipsecISAKMPReference` | Ipsec-ISAKMP-Reference | 1.2.840.113556.1.4.626 |
| `ipsecName` | Ipsec-Name | 1.2.840.113556.1.4.620 |
| `iPSECNegotiationPolicyAction` | IPSEC-Negotiation-Policy-Action | 1.2.840.113556.1.4.888 |
| `ipsecNegotiationPolicyReference` | Ipsec-Negotiation-Policy-Reference | 1.2.840.113556.1.4.628 |
| `iPSECNegotiationPolicyType` | IPSEC-Negotiation-Policy-Type | 1.2.840.113556.1.4.887 |
| `ipsecNFAReference` | Ipsec-NFA-Reference | 1.2.840.113556.1.4.627 |
| `ipsecOwnersReference` | Ipsec-Owners-Reference | 1.2.840.113556.1.4.624 |
| `ipsecPolicyReference` | Ipsec-Policy-Reference | 1.2.840.113556.1.4.517 |
| `isCriticalSystemObject` | Is-Critical-System-Object | 1.2.840.113556.1.4.868 |
| `isDefunct` | Is-Defunct | 1.2.840.113556.1.4.661 |
| `isDeleted` | Is-Deleted | 1.2.840.113556.1.2.48 |
| `isEphemeral` | Is-Ephemeral | 1.2.840.113556.1.4.1212 |
| `isMemberOfPartialAttributeSet` | Is-Member-Of-Partial-Attribute-Set | 1.2.840.113556.1.4.639 |
| `isPrivilegeHolder` | Is-Privilege-Holder | 1.2.840.113556.1.4.638 |
| `isSingleValued` | Is-Single-Valued | 1.2.840.113556.1.2.33 |
| `keywords` | Keywords | 1.2.840.113556.1.4.48 |
| `knowledgeInformation` | Knowledge-Information | 2.5.4.2 |
| `l` | Locality-Name | 2.5.4.7 |
| `lastBackupRestorationTime` | Last-Backup-Restoration-Time | 1.2.840.113556.1.4.519 |
| `lastContentIndexed` | Last-Content-Indexed | 1.2.840.113556.1.4.50 |
| `lastKnownParent` | Last-Known-Parent | 1.2.840.113556.1.4.781 |
| `lastLogoff` | Last-Logoff | 1.2.840.113556.1.4.51 |
| `lastLogon` | Last-Logon | 1.2.840.113556.1.4.52 |
| `lastSetTime` | Last-Set-Time | 1.2.840.113556.1.4.53 |
| `lastUpdateSequence` | Last-Update-Sequence | 1.2.840.113556.1.4.330 |
| `lDAPAdminLimits` | LDAP-Admin-Limits | 1.2.840.113556.1.4.843 |
| `lDAPDisplayName` | LDAP-Display-Name | 1.2.840.113556.1.2.460 |
| `lDAPIPDenyList` | LDAP-IPDeny-List | 1.2.840.113556.1.4.844 |
| `legacyExchangeDN` | Legacy-Exchange-DN | 1.2.840.113556.1.4.655 |
| `linkID` | Link-ID | 1.2.840.113556.1.2.50 |
| `linkTrackSecret` | Link-Track-Secret | 1.2.840.113556.1.4.269 |
| `lmPwdHistory` | Lm-Pwd-History | 1.2.840.113556.1.4.160 |
| `localeID` | Locale-ID | 1.2.840.113556.1.4.58 |
| `localizationDisplayId` | Localization-Display-Id | 1.2.840.113556.1.4.1353 |
| `localizedDescription` | Localized-Description | 1.2.840.113556.1.4.817 |
| `localPolicyFlags` | Local-Policy-Flags | 1.2.840.113556.1.4.56 |
| `localPolicyReference` | Local-Policy-Reference | 1.2.840.113556.1.4.457 |
| `location` | Location | 1.2.840.113556.1.4.222 |
| `lockoutDuration` | Lockout-Duration | 1.2.840.113556.1.4.60 |
| `lockOutObservationWindow` | Lock-Out-Observation-Window | 1.2.840.113556.1.4.61 |
| `lockoutThreshold` | Lockout-Threshold | 1.2.840.113556.1.4.73 |
| `lockoutTime` | Lockout-Time | 1.2.840.113556.1.4.662 |
| `logonCount` | Logon-Count | 1.2.840.113556.1.4.169 |
| `logonHours` | Logon-Hours | 1.2.840.113556.1.4.64 |
| `logonWorkstation` | Logon-Workstation | 1.2.840.113556.1.4.65 |
| `lSACreationTime` | LSA-Creation-Time | 1.2.840.113556.1.4.66 |
| `lSAModifiedCount` | LSA-Modified-Count | 1.2.840.113556.1.4.67 |
| `machineArchitecture` | Machine-Architecture | 1.2.840.113556.1.4.68 |
| `machinePasswordChangeInterval` | Machine-Password-Change-Interval | 1.2.840.113556.1.4.520 |
| `machineRole` | Machine-Role | 1.2.840.113556.1.4.71 |
| `machineWidePolicy` | Machine-Wide-Policy | 1.2.840.113556.1.4.459 |
| `mail` | E-mail-Addresses | 0.9.2342.19200300.100.1.3 |
| `mailAddress` | SMTP-Mail-Address | 1.2.840.113556.1.4.786 |
| `managedBy` | Managed-By | 1.2.840.113556.1.4.653 |
| `managedObjects` | Managed-Objects | 1.2.840.113556.1.4.654 |
| `manager` | Manager | 0.9.2342.19200300.100.1.10 |
| `mAPIID` | MAPI-ID | 1.2.840.113556.1.2.49 |
| `marshalledInterface` | Marshalled-Interface | 1.2.840.113556.1.4.72 |
| `masteredBy` | Mastered-By | 1.2.840.113556.1.4.1409 |
| `maxPwdAge` | Max-Pwd-Age | 1.2.840.113556.1.4.74 |
| `maxRenewAge` | Max-Renew-Age | 1.2.840.113556.1.4.75 |
| `maxStorage` | Max-Storage | 1.2.840.113556.1.4.76 |
| `maxTicketAge` | Max-Ticket-Age | 1.2.840.113556.1.4.77 |
| `mayContain` | May-Contain | 1.2.840.113556.1.2.25 |
| `meetingAdvertiseScope` | meetingAdvertiseScope | 1.2.840.113556.1.4.582 |
| `meetingApplication` | meetingApplication | 1.2.840.113556.1.4.573 |
| `meetingBandwidth` | meetingBandwidth | 1.2.840.113556.1.4.589 |
| `meetingBlob` | meetingBlob | 1.2.840.113556.1.4.590 |
| `meetingContactInfo` | meetingContactInfo | 1.2.840.113556.1.4.578 |
| `meetingDescription` | meetingDescription | 1.2.840.113556.1.4.567 |
| `meetingEndTime` | meetingEndTime | 1.2.840.113556.1.4.588 |
| `meetingID` | meetingID | 1.2.840.113556.1.4.565 |
| `meetingIP` | meetingIP | 1.2.840.113556.1.4.580 |
| `meetingIsEncrypted` | meetingIsEncrypted | 1.2.840.113556.1.4.585 |
| `meetingKeyword` | meetingKeyword | 1.2.840.113556.1.4.568 |
| `meetingLanguage` | meetingLanguage | 1.2.840.113556.1.4.574 |
| `meetingLocation` | meetingLocation | 1.2.840.113556.1.4.569 |
| `meetingMaxParticipants` | meetingMaxParticipants | 1.2.840.113556.1.4.576 |
| `meetingName` | meetingName | 1.2.840.113556.1.4.566 |
| `meetingOriginator` | meetingOriginator | 1.2.840.113556.1.4.577 |
| `meetingOwner` | meetingOwner | 1.2.840.113556.1.4.579 |
| `meetingProtocol` | meetingProtocol | 1.2.840.113556.1.4.570 |
| `meetingRating` | meetingRating | 1.2.840.113556.1.4.584 |
| `meetingRecurrence` | meetingRecurrence | 1.2.840.113556.1.4.586 |
| `meetingScope` | meetingScope | 1.2.840.113556.1.4.581 |
| `meetingStartTime` | meetingStartTime | 1.2.840.113556.1.4.587 |
| `meetingType` | meetingType | 1.2.840.113556.1.4.571 |
| `meetingURL` | meetingURL | 1.2.840.113556.1.4.583 |
| `member` | Member | 2.5.4.31 |
| `memberOf` | Is-Member-Of-DL | 1.2.840.113556.1.2.102 |
| `mhsORAddress` | MHS-OR-Address | 1.2.840.113556.1.4.650 |
| `middleName` | Other-Name | 2.16.840.1.113730.3.1.34 |
| `minPwdAge` | Min-Pwd-Age | 1.2.840.113556.1.4.78 |
| `minPwdLength` | Min-Pwd-Length | 1.2.840.113556.1.4.79 |
| `minTicketAge` | Min-Ticket-Age | 1.2.840.113556.1.4.80 |
| `mobile` | Phone-Mobile-Primary | 0.9.2342.19200300.100.1.41 |
| `modifiedCount` | Modified-Count | 1.2.840.113556.1.4.168 |
| `modifiedCountAtLastProm` | Modified-Count-At-Last-Prom | 1.2.840.113556.1.4.81 |
| `modifyTimeStamp` | Modify-Time-Stamp | 2.5.18.2 |
| `moniker` | Moniker | 1.2.840.113556.1.4.82 |
| `monikerDisplayName` | Moniker-Display-Name | 1.2.840.113556.1.4.83 |
| `moveTreeState` | Move-Tree-State | 1.2.840.113556.1.4.1305 |
| `mscopeId` | Mscope-Id | 1.2.840.113556.1.4.716 |
| `mS-DS-ConsistencyChildCount` | MS-DS-Consistency-Child-Count | 1.2.840.113556.1.4.1361 |
| `mS-DS-ConsistencyGuid` | MS-DS-Consistency-Guid | 1.2.840.113556.1.4.1360 |
| `mS-DS-CreatorSID` | MS-DS-Creator-SID | 1.2.840.113556.1.4.1410 |
| `ms-DS-MachineAccountQuota` | MS-DS-Machine-Account-Quota | 1.2.840.113556.1.4.1411 |
| `mS-DS-ReplicatesNCReason` | MS-DS-Replicates-NC-Reason | 1.2.840.113556.1.4.1408 |
| `msiFileList` | Msi-File-List | 1.2.840.113556.1.4.671 |
| `msiScript` | Msi-Script | 1.2.840.113556.1.4.814 |
| `msiScriptName` | Msi-Script-Name | 1.2.840.113556.1.4.845 |
| `msiScriptPath` | Msi-Script-Path | 1.2.840.113556.1.4.15 |
| `msiScriptSize` | Msi-Script-Size | 1.2.840.113556.1.4.846 |
| `mSMQAuthenticate` | MSMQ-Authenticate | 1.2.840.113556.1.4.923 |
| `mSMQBasePriority` | MSMQ-Base-Priority | 1.2.840.113556.1.4.920 |
| `mSMQComputerType` | MSMQ-Computer-Type | 1.2.840.113556.1.4.933 |
| `mSMQComputerTypeEx` | MSMQ-Computer-Type-Ex | 1.2.840.113556.1.4.1417 |
| `mSMQCost` | MSMQ-Cost | 1.2.840.113556.1.4.946 |
| `mSMQCSPName` | MSMQ-CSP-Name | 1.2.840.113556.1.4.940 |
| `mSMQDependentClientService` | MSMQ-Dependent-Client-Service | 1.2.840.113556.1.4.1239 |
| `mSMQDependentClientServices` | MSMQ-Dependent-Client-Services | 1.2.840.113556.1.4.1226 |
| `mSMQDigests` | MSMQ-Digests | 1.2.840.113556.1.4.948 |
| `mSMQDigestsMig` | MSMQ-Digests-Mig | 1.2.840.113556.1.4.966 |
| `mSMQDsService` | MSMQ-Ds-Service | 1.2.840.113556.1.4.1238 |
| `mSMQDsServices` | MSMQ-Ds-Services | 1.2.840.113556.1.4.1228 |
| `mSMQEncryptKey` | MSMQ-Encrypt-Key | 1.2.840.113556.1.4.936 |
| `mSMQForeign` | MSMQ-Foreign | 1.2.840.113556.1.4.934 |
| `mSMQInRoutingServers` | MSMQ-In-Routing-Servers | 1.2.840.113556.1.4.929 |
| `mSMQInterval1` | MSMQ-Interval1 | 1.2.840.113556.1.4.1308 |
| `mSMQInterval2` | MSMQ-Interval2 | 1.2.840.113556.1.4.1309 |
| `mSMQJournal` | MSMQ-Journal | 1.2.840.113556.1.4.918 |
| `mSMQJournalQuota` | MSMQ-Journal-Quota | 1.2.840.113556.1.4.921 |
| `mSMQLabel` | MSMQ-Label | 1.2.840.113556.1.4.922 |
| `mSMQLabelEx` | MSMQ-Label-Ex | 1.2.840.113556.1.4.1415 |
| `mSMQLongLived` | MSMQ-Long-Lived | 1.2.840.113556.1.4.941 |
| `mSMQMigrated` | MSMQ-Migrated | 1.2.840.113556.1.4.952 |
| `mSMQNameStyle` | MSMQ-Name-Style | 1.2.840.113556.1.4.939 |
| `mSMQNt4Flags` | MSMQ-Nt4-Flags | 1.2.840.113556.1.4.964 |
| `mSMQNt4Stub` | MSMQ-Nt4-Stub | 1.2.840.113556.1.4.960 |
| `mSMQOSType` | MSMQ-OS-Type | 1.2.840.113556.1.4.935 |
| `mSMQOutRoutingServers` | MSMQ-Out-Routing-Servers | 1.2.840.113556.1.4.928 |
| `mSMQOwnerID` | MSMQ-Owner-ID | 1.2.840.113556.1.4.925 |
| `mSMQPrevSiteGates` | MSMQ-Prev-Site-Gates | 1.2.840.113556.1.4.1225 |
| `mSMQPrivacyLevel` | MSMQ-Privacy-Level | 1.2.840.113556.1.4.924 |
| `mSMQQMID` | MSMQ-QM-ID | 1.2.840.113556.1.4.951 |
| `mSMQQueueJournalQuota` | MSMQ-Queue-Journal-Quota | 1.2.840.113556.1.4.963 |
| `mSMQQueueNameExt` | MSMQ-Queue-Name-Ext | 1.2.840.113556.1.4.1243 |
| `mSMQQueueQuota` | MSMQ-Queue-Quota | 1.2.840.113556.1.4.962 |
| `mSMQQueueType` | MSMQ-Queue-Type | 1.2.840.113556.1.4.917 |
| `mSMQQuota` | MSMQ-Quota | 1.2.840.113556.1.4.919 |
| `mSMQRoutingService` | MSMQ-Routing-Service | 1.2.840.113556.1.4.1237 |
| `mSMQRoutingServices` | MSMQ-Routing-Services | 1.2.840.113556.1.4.1227 |
| `mSMQServices` | MSMQ-Services | 1.2.840.113556.1.4.950 |
| `mSMQServiceType` | MSMQ-Service-Type | 1.2.840.113556.1.4.930 |
| `mSMQSignCertificates` | MSMQ-Sign-Certificates | 1.2.840.113556.1.4.947 |
| `mSMQSignCertificatesMig` | MSMQ-Sign-Certificates-Mig | 1.2.840.113556.1.4.967 |
| `mSMQSignKey` | MSMQ-Sign-Key | 1.2.840.113556.1.4.937 |
| `mSMQSite1` | MSMQ-Site-1 | 1.2.840.113556.1.4.943 |
| `mSMQSite2` | MSMQ-Site-2 | 1.2.840.113556.1.4.944 |
| `mSMQSiteForeign` | MSMQ-Site-Foreign | 1.2.840.113556.1.4.961 |
| `mSMQSiteGates` | MSMQ-Site-Gates | 1.2.840.113556.1.4.945 |
| `mSMQSiteGatesMig` | MSMQ-Site-Gates-Mig | 1.2.840.113556.1.4.1310 |
| `mSMQSiteID` | MSMQ-Site-ID | 1.2.840.113556.1.4.953 |
| `mSMQSiteName` | MSMQ-Site-Name | 1.2.840.113556.1.4.965 |
| `mSMQSiteNameEx` | MSMQ-Site-Name-Ex | 1.2.840.113556.1.4.1416 |
| `mSMQSites` | MSMQ-Sites | 1.2.840.113556.1.4.927 |
| `mSMQTransactional` | MSMQ-Transactional | 1.2.840.113556.1.4.926 |
| `mSMQUserSid` | MSMQ-User-Sid | 1.2.840.113556.1.4.1337 |
| `mSMQVersion` | MSMQ-Version | 1.2.840.113556.1.4.942 |
| `msNPAllowDialin` | msNPAllowDialin | 1.2.840.113556.1.4.1119 |
| `msNPCalledStationID` | msNPCalledStationID | 1.2.840.113556.1.4.1123 |
| `msNPCallingStationID` | msNPCallingStationID | 1.2.840.113556.1.4.1124 |
| `msNPSavedCallingStationID` | msNPSavedCallingStationID | 1.2.840.113556.1.4.1130 |
| `msRADIUSCallbackNumber` | msRADIUSCallbackNumber | 1.2.840.113556.1.4.1145 |
| `msRADIUSFramedIPAddress` | msRADIUSFramedIPAddress | 1.2.840.113556.1.4.1153 |
| `msRADIUSFramedRoute` | msRADIUSFramedRoute | 1.2.840.113556.1.4.1158 |
| `msRADIUSServiceType` | msRADIUSServiceType | 1.2.840.113556.1.4.1171 |
| `msRASSavedCallbackNumber` | msRASSavedCallbackNumber | 1.2.840.113556.1.4.1189 |
| `msRASSavedFramedIPAddress` | msRASSavedFramedIPAddress | 1.2.840.113556.1.4.1190 |
| `msRASSavedFramedRoute` | msRASSavedFramedRoute | 1.2.840.113556.1.4.1191 |
| `msRRASAttribute` | ms-RRAS-Attribute | 1.2.840.113556.1.4.884 |
| `msRRASVendorAttributeEntry` | ms-RRAS-Vendor-Attribute-Entry | 1.2.840.113556.1.4.883 |
| `mS-SQL-Alias` | MS-SQL-Alias | 1.2.840.113556.1.4.1395 |
| `mS-SQL-AllowAnonymousSubscription` | MS-SQL-AllowAnonymousSubscription | 1.2.840.113556.1.4.1394 |
| `mS-SQL-AllowImmediateUpdatingSubscription` | MS-SQL-AllowImmediateUpdatingSubscription | 1.2.840.113556.1.4.1404 |
| `mS-SQL-AllowKnownPullSubscription` | MS-SQL-AllowKnownPullSubscription | 1.2.840.113556.1.4.1403 |
| `mS-SQL-AllowQueuedUpdatingSubscription` | MS-SQL-AllowQueuedUpdatingSubscription | 1.2.840.113556.1.4.1405 |
| `mS-SQL-AllowSnapshotFilesFTPDownloading` | MS-SQL-AllowSnapshotFilesFTPDownloading | 1.2.840.113556.1.4.1406 |
| `mS-SQL-AppleTalk` | MS-SQL-AppleTalk | 1.2.840.113556.1.4.1378 |
| `mS-SQL-Applications` | MS-SQL-Applications | 1.2.840.113556.1.4.1400 |
| `mS-SQL-Build` | MS-SQL-Build | 1.2.840.113556.1.4.1368 |
| `mS-SQL-CharacterSet` | MS-SQL-CharacterSet | 1.2.840.113556.1.4.1370 |
| `mS-SQL-Clustered` | MS-SQL-Clustered | 1.2.840.113556.1.4.1373 |
| `mS-SQL-ConnectionURL` | MS-SQL-ConnectionURL | 1.2.840.113556.1.4.1383 |
| `mS-SQL-Contact` | MS-SQL-Contact | 1.2.840.113556.1.4.1365 |
| `mS-SQL-CreationDate` | MS-SQL-CreationDate | 1.2.840.113556.1.4.1397 |
| `mS-SQL-Database` | MS-SQL-Database | 1.2.840.113556.1.4.1393 |
| `mS-SQL-Description` | MS-SQL-Description | 1.2.840.113556.1.4.1390 |
| `mS-SQL-GPSHeight` | MS-SQL-GPSHeight | 1.2.840.113556.1.4.1387 |
| `mS-SQL-GPSLatitude` | MS-SQL-GPSLatitude | 1.2.840.113556.1.4.1385 |
| `mS-SQL-GPSLongitude` | MS-SQL-GPSLongitude | 1.2.840.113556.1.4.1386 |
| `mS-SQL-InformationDirectory` | MS-SQL-InformationDirectory | 1.2.840.113556.1.4.1392 |
| `mS-SQL-InformationURL` | MS-SQL-InformationURL | 1.2.840.113556.1.4.1382 |
| `mS-SQL-Keywords` | MS-SQL-Keywords | 1.2.840.113556.1.4.1401 |
| `mS-SQL-Language` | MS-SQL-Language | 1.2.840.113556.1.4.1389 |
| `mS-SQL-LastBackupDate` | MS-SQL-LastBackupDate | 1.2.840.113556.1.4.1398 |
| `mS-SQL-LastDiagnosticDate` | MS-SQL-LastDiagnosticDate | 1.2.840.113556.1.4.1399 |
| `mS-SQL-LastUpdatedDate` | MS-SQL-LastUpdatedDate | 1.2.840.113556.1.4.1381 |
| `mS-SQL-Location` | MS-SQL-Location | 1.2.840.113556.1.4.1366 |
| `mS-SQL-Memory` | MS-SQL-Memory | 1.2.840.113556.1.4.1367 |
| `mS-SQL-MultiProtocol` | MS-SQL-MultiProtocol | 1.2.840.113556.1.4.1375 |
| `mS-SQL-Name` | MS-SQL-Name | 1.2.840.113556.1.4.1363 |
| `mS-SQL-NamedPipe` | MS-SQL-NamedPipe | 1.2.840.113556.1.4.1374 |
| `mS-SQL-PublicationURL` | MS-SQL-PublicationURL | 1.2.840.113556.1.4.1384 |
| `mS-SQL-Publisher` | MS-SQL-Publisher | 1.2.840.113556.1.4.1402 |
| `mS-SQL-RegisteredOwner` | MS-SQL-RegisteredOwner | 1.2.840.113556.1.4.1364 |
| `mS-SQL-ServiceAccount` | MS-SQL-ServiceAccount | 1.2.840.113556.1.4.1369 |
| `mS-SQL-Size` | MS-SQL-Size | 1.2.840.113556.1.4.1396 |
| `mS-SQL-SortOrder` | MS-SQL-SortOrder | 1.2.840.113556.1.4.1371 |
| `mS-SQL-SPX` | MS-SQL-SPX | 1.2.840.113556.1.4.1376 |
| `mS-SQL-Status` | MS-SQL-Status | 1.2.840.113556.1.4.1380 |
| `mS-SQL-TCPIP` | MS-SQL-TCPIP | 1.2.840.113556.1.4.1377 |
| `mS-SQL-ThirdParty` | MS-SQL-ThirdParty | 1.2.840.113556.1.4.1407 |
| `mS-SQL-Type` | MS-SQL-Type | 1.2.840.113556.1.4.1391 |
| `mS-SQL-UnicodeSortOrder` | MS-SQL-UnicodeSortOrder | 1.2.840.113556.1.4.1372 |
| `mS-SQL-Version` | MS-SQL-Version | 1.2.840.113556.1.4.1388 |
| `mS-SQL-Vines` | MS-SQL-Vines | 1.2.840.113556.1.4.1379 |
| `mustContain` | Must-Contain | 1.2.840.113556.1.2.24 |
| `name` | RDN | 1.2.840.113556.1.4.1 |
| `nameServiceFlags` | Name-Service-Flags | 1.2.840.113556.1.4.753 |
| `nCName` | NC-Name | 1.2.840.113556.1.2.16 |
| `nETBIOSName` | NETBIOS-Name | 1.2.840.113556.1.4.87 |
| `netbootAllowNewClients` | netboot-Allow-New-Clients | 1.2.840.113556.1.4.849 |
| `netbootAnswerOnlyValidClients` | netboot-Answer-Only-Valid-Clients | 1.2.840.113556.1.4.854 |
| `netbootAnswerRequests` | netboot-Answer-Requests | 1.2.840.113556.1.4.853 |
| `netbootCurrentClientCount` | netboot-Current-Client-Count | 1.2.840.113556.1.4.852 |
| `netbootGUID` | Netboot-GUID | 1.2.840.113556.1.4.359 |
| `netbootInitialization` | Netboot-Initialization | 1.2.840.113556.1.4.358 |
| `netbootIntelliMirrorOSes` | netboot-IntelliMirror-OSes | 1.2.840.113556.1.4.857 |
| `netbootLimitClients` | netboot-Limit-Clients | 1.2.840.113556.1.4.850 |
| `netbootLocallyInstalledOSes` | netboot-Locally-Installed-OSes | 1.2.840.113556.1.4.859 |
| `netbootMachineFilePath` | Netboot-Machine-File-Path | 1.2.840.113556.1.4.361 |
| `netbootMaxClients` | netboot-Max-Clients | 1.2.840.113556.1.4.851 |
| `netbootMirrorDataFile` | Netboot-Mirror-Data-File | 1.2.840.113556.1.4.1241 |
| `netbootNewMachineNamingPolicy` | netboot-New-Machine-Naming-Policy | 1.2.840.113556.1.4.855 |
| `netbootNewMachineOU` | netboot-New-Machine-OU | 1.2.840.113556.1.4.856 |
| `netbootSCPBL` | netboot-SCP-BL | 1.2.840.113556.1.4.864 |
| `netbootServer` | netboot-Server | 1.2.840.113556.1.4.860 |
| `netbootSIFFile` | Netboot-SIF-File | 1.2.840.113556.1.4.1240 |
| `netbootTools` | netboot-Tools | 1.2.840.113556.1.4.858 |
| `networkAddress` | Network-Address | 1.2.840.113556.1.2.459 |
| `nextLevelStore` | Next-Level-Store | 1.2.840.113556.1.4.214 |
| `nextRid` | Next-Rid | 1.2.840.113556.1.4.88 |
| `nonSecurityMember` | Non-Security-Member | 1.2.840.113556.1.4.530 |
| `nonSecurityMemberBL` | Non-Security-Member-BL | 1.2.840.113556.1.4.531 |
| `notes` | Additional-Information | 1.2.840.113556.1.4.265 |
| `notificationList` | Notification-List | 1.2.840.113556.1.4.303 |
| `nTGroupMembers` | NT-Group-Members | 1.2.840.113556.1.4.89 |
| `nTMixedDomain` | NT-Mixed-Domain | 1.2.840.113556.1.4.357 |
| `ntPwdHistory` | Nt-Pwd-History | 1.2.840.113556.1.4.94 |
| `nTSecurityDescriptor` | NT-Security-Descriptor | 1.2.840.113556.1.2.281 |
| `o` | Organization-Name | 2.5.4.10 |
| `objectCategory` | Object-Category | 1.2.840.113556.1.4.782 |
| `objectClass` | Object-Class | 2.5.4.0 |
| `objectClassCategory` | Object-Class-Category | 1.2.840.113556.1.2.370 |
| `objectClasses` | Object-Classes | 2.5.21.6 |
| `objectCount` | Object-Count | 1.2.840.113556.1.4.506 |
| `objectGUID` | Object-Guid | 1.2.840.113556.1.4.2 |
| `objectSid` | Object-Sid | 1.2.840.113556.1.4.146 |
| `objectVersion` | Object-Version | 1.2.840.113556.1.2.76 |
| `oEMInformation` | OEM-Information | 1.2.840.113556.1.4.151 |
| `oMObjectClass` | OM-Object-Class | 1.2.840.113556.1.2.218 |
| `oMSyntax` | OM-Syntax | 1.2.840.113556.1.2.231 |
| `oMTGuid` | OMT-Guid | 1.2.840.113556.1.4.505 |
| `oMTIndxGuid` | OMT-Indx-Guid | 1.2.840.113556.1.4.333 |
| `operatingSystem` | Operating-System | 1.2.840.113556.1.4.363 |
| `operatingSystemHotfix` | Operating-System-Hotfix | 1.2.840.113556.1.4.415 |
| `operatingSystemServicePack` | Operating-System-Service-Pack | 1.2.840.113556.1.4.365 |
| `operatingSystemVersion` | Operating-System-Version | 1.2.840.113556.1.4.364 |
| `operatorCount` | Operator-Count | 1.2.840.113556.1.4.144 |
| `optionDescription` | Option-Description | 1.2.840.113556.1.4.712 |
| `options` | Options | 1.2.840.113556.1.4.307 |
| `optionsLocation` | Options-Location | 1.2.840.113556.1.4.713 |
| `originalDisplayTable` | Original-Display-Table | 1.2.840.113556.1.2.445 |
| `originalDisplayTableMSDOS` | Original-Display-Table-MSDOS | 1.2.840.113556.1.2.214 |
| `otherFacsimileTelephoneNumber` | Phone-Fax-Other | 1.2.840.113556.1.4.646 |
| `otherHomePhone` | Phone-Home-Other | 1.2.840.113556.1.2.277 |
| `otherIpPhone` | Phone-Ip-Other | 1.2.840.113556.1.4.722 |
| `otherLoginWorkstations` | Other-Login-Workstations | 1.2.840.113556.1.4.91 |
| `otherMailbox` | Other-Mailbox | 1.2.840.113556.1.4.651 |
| `otherMobile` | Phone-Mobile-Other | 1.2.840.113556.1.4.647 |
| `otherPager` | Phone-Pager-Other | 1.2.840.113556.1.2.118 |
| `otherTelephone` | Phone-Office-Other | 1.2.840.113556.1.2.18 |
| `otherWellKnownObjects` | Other-Well-Known-Objects | 1.2.840.113556.1.4.1359 |
| `ou` | Organizational-Unit-Name | 2.5.4.11 |
| `owner` | Owner | 2.5.4.32 |
| `packageFlags` | Package-Flags | 1.2.840.113556.1.4.327 |
| `packageName` | Package-Name | 1.2.840.113556.1.4.326 |
| `packageType` | Package-Type | 1.2.840.113556.1.4.324 |
| `pager` | Phone-Pager-Primary | 0.9.2342.19200300.100.1.42 |
| `parentCA` | Parent-CA | 1.2.840.113556.1.4.557 |
| `parentCACertificateChain` | Parent-CA-Certificate-Chain | 1.2.840.113556.1.4.685 |
| `parentGUID` | Parent-GUID | 1.2.840.113556.1.4.1224 |
| `partialAttributeDeletionList` | Partial-Attribute-Deletion-List | 1.2.840.113556.1.4.663 |
| `partialAttributeSet` | Partial-Attribute-Set | 1.2.840.113556.1.4.640 |
| `pekKeyChangeInterval` | Pek-Key-Change-Interval | 1.2.840.113556.1.4.866 |
| `pekList` | Pek-List | 1.2.840.113556.1.4.865 |
| `pendingCACertificates` | Pending-CA-Certificates | 1.2.840.113556.1.4.693 |
| `pendingParentCA` | Pending-Parent-CA | 1.2.840.113556.1.4.695 |
| `perMsgDialogDisplayTable` | Per-Msg-Dialog-Display-Table | 1.2.840.113556.1.2.325 |
| `perRecipDialogDisplayTable` | Per-Recip-Dialog-Display-Table | 1.2.840.113556.1.2.326 |
| `personalTitle` | Personal-Title | 1.2.840.113556.1.2.615 |
| `physicalDeliveryOfficeName` | Physical-Delivery-Office-Name | 2.5.4.19 |
| `physicalLocationObject` | Physical-Location-Object | 1.2.840.113556.1.4.514 |
| `pKICriticalExtensions` | PKI-Critical-Extensions | 1.2.840.113556.1.4.1330 |
| `pKIDefaultCSPs` | PKI-Default-CSPs | 1.2.840.113556.1.4.1334 |
| `pKIDefaultKeySpec` | PKI-Default-Key-Spec | 1.2.840.113556.1.4.1327 |
| `pKIEnrollmentAccess` | PKI-Enrollment-Access | 1.2.840.113556.1.4.1335 |
| `pKIExpirationPeriod` | PKI-Expiration-Period | 1.2.840.113556.1.4.1331 |
| `pKIExtendedKeyUsage` | PKI-Extended-Key-Usage | 1.2.840.113556.1.4.1333 |
| `pKIKeyUsage` | PKI-Key-Usage | 1.2.840.113556.1.4.1328 |
| `pKIMaxIssuingDepth` | PKI-Max-Issuing-Depth | 1.2.840.113556.1.4.1329 |
| `pKIOverlapPeriod` | PKI-Overlap-Period | 1.2.840.113556.1.4.1332 |
| `pKT` | PKT | 1.2.840.113556.1.4.206 |
| `pKTGuid` | PKT-Guid | 1.2.840.113556.1.4.205 |
| `policyReplicationFlags` | Policy-Replication-Flags | 1.2.840.113556.1.4.633 |
| `portName` | Port-Name | 1.2.840.113556.1.4.228 |
| `possibleInferiors` | Possible-Inferiors | 1.2.840.113556.1.4.915 |
| `possSuperiors` | Poss-Superiors | 1.2.840.113556.1.2.8 |
| `postalAddress` | Postal-Address | 2.5.4.16 |
| `postalCode` | Postal-Code | 2.5.4.17 |
| `postOfficeBox` | Post-Office-Box | 2.5.4.18 |
| `preferredDeliveryMethod` | Preferred-Delivery-Method | 2.5.4.28 |
| `preferredOU` | Preferred-OU | 1.2.840.113556.1.4.97 |
| `prefixMap` | Prefix-Map | 1.2.840.113556.1.4.538 |
| `presentationAddress` | Presentation-Address | 2.5.4.29 |
| `previousCACertificates` | Previous-CA-Certificates | 1.2.840.113556.1.4.692 |
| `previousParentCA` | Previous-Parent-CA | 1.2.840.113556.1.4.694 |
| `primaryGroupID` | Primary-Group-ID | 1.2.840.113556.1.4.98 |
| `primaryGroupToken` | Primary-Group-Token | 1.2.840.113556.1.4.1412 |
| `primaryInternationalISDNNumber` | Phone-ISDN-Primary | 1.2.840.113556.1.4.649 |
| `primaryTelexNumber` | Telex-Primary | 1.2.840.113556.1.4.648 |
| `printAttributes` | Print-Attributes | 1.2.840.113556.1.4.247 |
| `printBinNames` | Print-Bin-Names | 1.2.840.113556.1.4.237 |
| `printCollate` | Print-Collate | 1.2.840.113556.1.4.242 |
| `printColor` | Print-Color | 1.2.840.113556.1.4.243 |
| `printDuplexSupported` | Print-Duplex-Supported | 1.2.840.113556.1.4.1311 |
| `printEndTime` | Print-End-Time | 1.2.840.113556.1.4.234 |
| `printerName` | Printer-Name | 1.2.840.113556.1.4.300 |
| `printFormName` | Print-Form-Name | 1.2.840.113556.1.4.235 |
| `printKeepPrintedJobs` | Print-Keep-Printed-Jobs | 1.2.840.113556.1.4.275 |
| `printLanguage` | Print-Language | 1.2.840.113556.1.4.246 |
| `printMACAddress` | Print-MAC-Address | 1.2.840.113556.1.4.288 |
| `printMaxCopies` | Print-Max-Copies | 1.2.840.113556.1.4.241 |
| `printMaxResolutionSupported` | Print-Max-Resolution-Supported | 1.2.840.113556.1.4.238 |
| `printMaxXExtent` | Print-Max-X-Extent | 1.2.840.113556.1.4.277 |
| `printMaxYExtent` | Print-Max-Y-Extent | 1.2.840.113556.1.4.278 |
| `printMediaReady` | Print-Media-Ready | 1.2.840.113556.1.4.289 |
| `printMediaSupported` | Print-Media-Supported | 1.2.840.113556.1.4.299 |
| `printMemory` | Print-Memory | 1.2.840.113556.1.4.282 |
| `printMinXExtent` | Print-Min-X-Extent | 1.2.840.113556.1.4.279 |
| `printMinYExtent` | Print-Min-Y-Extent | 1.2.840.113556.1.4.280 |
| `printNetworkAddress` | Print-Network-Address | 1.2.840.113556.1.4.287 |
| `printNotify` | Print-Notify | 1.2.840.113556.1.4.272 |
| `printNumberUp` | Print-Number-Up | 1.2.840.113556.1.4.290 |
| `printOrientationsSupported` | Print-Orientations-Supported | 1.2.840.113556.1.4.240 |
| `printOwner` | Print-Owner | 1.2.840.113556.1.4.271 |
| `printPagesPerMinute` | Print-Pages-Per-Minute | 1.2.840.113556.1.4.631 |
| `printRate` | Print-Rate | 1.2.840.113556.1.4.285 |
| `printRateUnit` | Print-Rate-Unit | 1.2.840.113556.1.4.286 |
| `printSeparatorFile` | Print-Separator-File | 1.2.840.113556.1.4.230 |
| `printShareName` | Print-Share-Name | 1.2.840.113556.1.4.270 |
| `printSpooling` | Print-Spooling | 1.2.840.113556.1.4.274 |
| `printStaplingSupported` | Print-Stapling-Supported | 1.2.840.113556.1.4.281 |
| `printStartTime` | Print-Start-Time | 1.2.840.113556.1.4.233 |
| `printStatus` | Print-Status | 1.2.840.113556.1.4.273 |
| `priority` | Priority | 1.2.840.113556.1.4.231 |
| `priorSetTime` | Prior-Set-Time | 1.2.840.113556.1.4.99 |
| `priorValue` | Prior-Value | 1.2.840.113556.1.4.100 |

* * *

## Object Identifiers (OIDs)

We can also use matching rule [Object Identifiers (OIDs)](https://ldapwiki.com/wiki/Wiki.jsp?page=OID) with LDAP filters as listed in this [Search Filter Syntax](https://docs.microsoft.com/en-us/windows/win32/adsi/search-filter-syntax) document from Microsoft:

| **Matching rule OID** | **String identifier** | **Description** |
| --- | --- | --- |
| [1.2.840.113556.1.4.803](https://ldapwiki.com/wiki/Wiki.jsp?page=1.2.840.113556.1.4.803) | LDAP\_MATCHING\_RULE\_BIT\_AND | A match is found only if all bits from the attribute match the value. This rule is equivalent to a bitwise **AND** operator. |
| [1.2.840.113556.1.4.804](https://ldapwiki.com/wiki/Wiki.jsp?page=1.2.840.113556.1.4.804) | LDAP\_MATCHING\_RULE\_BIT\_OR | A match is found if any bits from the attribute match the value. This rule is equivalent to a bitwise **OR** operator. |
| [1.2.840.113556.1.4.1941](https://ldapwiki.com/wiki/Wiki.jsp?page=1.2.840.113556.1.4.1941) | LDAP\_MATCHING\_RULE\_IN\_CHAIN | This rule is limited to filters that apply to the DN. This is a special "extended" match operator that walks the chain of ancestry in objects all the way to the root until it finds a match. |

We can clarify the above OIDs with some examples. Let's take the following LDAP query:

```powershell
(&(objectCategory=person)(objectClass=user)(userAccountControl:1.2.840.113556.1.4.803:=2))

```

This query will return all administratively disabled user accounts, or [ACCOUNTDISABLE (2)](https://ldapwiki.com/wiki/Wiki.jsp?page=ACCOUNTDISABLE). We can combine this query as an LDAP search filter with the " `Get-ADUser`" cmdlet against our target domain. The LDAP query can be shortened as follows:

#### LDAP Query - Filter Disabled User Accounts

```powershell
PS C:\htb> Get-ADUser -LDAPFilter '(userAccountControl:1.2.840.113556.1.4.803:=2)' | select name

name
----
Guest
DefaultAccount
krbtgt
Exchange Online-ApplicationAccount
SystemMailbox{1f05a927-35b9-4cc9-bbe1-11e28cddb180}
SystemMailbox{bb558c35-97f1-4cb9-8ff7-d53741dc928c}
SystemMailbox{e0dc1c29-89c3-4034-b678-e6c29d823ed9}
DiscoverySearchMailbox {D919BA05-46A6-415f-80AD-7E09334BB852}
Migration.8f3e7716-2011-43e4-96b1-aba62d229136
FederatedEmail.4c1f4d8b-8179-4148-93bf-00a95fa1e042
SystemMailbox{D0E409A0-AF9B-4720-92FE-AAC869B0D201}
SystemMailbox{2CE34405-31BE-455D-89D7-A7C7DA7A0DAA}
SystemMailbox{8cc370d3-822a-4ab8-a926-bb94bd0641a9}

```

Now let's look at an example of the extensible match rule " `1.2.840.113556.1.4.1941`". Consider the following query:

```powershell
(member:1.2.840.113556.1.4.1941:=CN=Harry Jones,OU=Network Ops,OU=IT,OU=Employees,DC=INLANEFREIGHT,DC=LOCAL)

```

This matching rule will find all groups that the user `Harry Jones` (" `CN=Harry Jones,OU=Network Ops,OU=IT,OU=Employees,DC=INLANEFREIGHT,DC=LOCAL`") is a member of. Using this filter with the " `Get-ADGroup`" cmdlet gives us the following output:

#### LDAP Query - Find All Groups

```powershell
PS C:\htb> Get-ADGroup -LDAPFilter '(member:1.2.840.113556.1.4.1941:=CN=Harry Jones,OU=Network Ops,OU=IT,OU=Employees,DC=INLANEFREIGHT,DC=LOCAL)' | select Name

Name
----
Administrators
Backup Operators
Domain Admins
Denied RODC Password Replication Group
LAPS Admins
Security Operations
Help Desk
Network Team

```

* * *

## Filter Types, Item Types & Escaped Characters

With LDAP search [filters](https://ldapwiki.com/wiki/Wiki.jsp?page=LDAP%20SearchFilters), we have the following four filter types:

| **Operator** | **Meaning** |
| --- | --- |
| = | Equal to |
| ~= | Approximately equal to |
| >= | Greater than or equal to |
| <= | Less than or equal to |

* * *

And we have four item types:

| **Type** | **Meaning** |
| --- | --- |
| = | Simple |
| =\* | Present |
| =something\* | Substring |
| Extensible | varies depending on type |

* * *

Finally, the following characters must be escaped if used in an LDAP filter:

| **Character** | **Represented as Hex** |
| --- | --- |
| \* | \\2a |
| ( | \\28 |
| ) | \\29 |
| \ | \\5c |
| NUL | \\00 |

* * *

## Example LDAP Filters

Let's build a few more LDAP filters to use against our test domain.

We can use the filter " `(&(objectCategory=user)(description=*))`" to find all user accounts that do not have a blank `description` field. This is a useful search that should be performed on every internal network assessment as it not uncommon to find passwords for users stored in the user description attribute in AD (which can be read by all AD users).

Combining this with the " `Get-ADUser`" cmdlet, we can search for all domain users that do not have a blank description field and, in this case, find a service account password!

#### LDAP Query - Description Field

```powershell
PS C:\htb> Get-ADUser -Properties * -LDAPFilter '(&(objectCategory=user)(description=*))' | select samaccountname,description

samaccountname description
-------------- -----------
Administrator  Built-in account for administering the computer/domain
Guest          Built-in account for guest access to the computer/domain
DefaultAccount A user account managed by the system.
krbtgt         Key Distribution Center Service Account
svc-sccm       **Do not change password** 03/04/2015 N3ssu$_svc2014!

```

This filter " `(userAccountControl:1.2.840.113556.1.4.803:=524288)`" can be used to find all users or computers marked as `trusted for delegation`, or unconstrained delegation, which will be covered in a later module on Kerberos Attacks. We can enumerate users with the help of this LDAP filter:

#### LDAP Query - Find Trusted Users

```powershell
PS C:\htb> Get-ADUser -Properties * -LDAPFilter '(userAccountControl:1.2.840.113556.1.4.803:=524288)' | select Name,memberof, servicePrincipalName,TrustedForDelegation | fl

Name                 : sqldev
memberof             : {CN=Protected Users,CN=Users,DC=INLANEFREIGHT,DC=LOCAL}
servicePrincipalName : {MSSQL_svc_dev/inlanefreight.local:1443}
TrustedForDelegation : True

```

We can enumerate computers with this setting as well:

#### LDAP Query - Find Trusted Computers

```powershell
PS C:\htb> Get-ADComputer -Properties * -LDAPFilter '(userAccountControl:1.2.840.113556.1.4.803:=524288)' | select DistinguishedName,servicePrincipalName,TrustedForDelegation | fl

DistinguishedName    : CN=DC01,OU=Domain Controllers,DC=INLANEFREIGHT,DC=LOCAL
servicePrincipalName : {exchangeAB/DC01, exchangeAB/DC01.INLANEFREIGHT.LOCAL, TERMSRV/DC01,
                       TERMSRV/DC01.INLANEFREIGHT.LOCAL...}
TrustedForDelegation : True

DistinguishedName    : CN=SQL01,OU=SQL Servers,OU=Servers,DC=INLANEFREIGHT,DC=LOCAL
servicePrincipalName : {MSSQLsvc/SQL01.INLANEFREIGHT.LOCAL:1433, TERMSRV/SQL01, TERMSRV/SQL01.INLANEFREIGHT.LOCAL,
                       RestrictedKrbHost/SQL01...}
TrustedForDelegation : True

```

Lastly, let's search for all users with the " `adminCount`" attribute set to `1` whose " `useraccountcontrol`" attribute is set with the flag " `PASSWD_NOTREQD`," meaning that the account can have a blank password set. To do this, we must combine two LDAP search filters as follows:

```powershell
(&(objectCategory=person)(objectClass=user)(userAccountControl:1.2.840.113556.1.4.803:=32))(adminCount=1)

```

#### LDAP Query - Users With Blank Password

```powershell
PS C:\htb> Get-AdUser -LDAPFilter '(&(objectCategory=person)(objectClass=user)(userAccountControl:1.2.840.113556.1.4.803:=32))(adminCount=1)' -Properties * | select name,memberof | fl

name     : Jenna Smith
memberof : CN=Schema Admins,CN=Users,DC=INLANEFREIGHT,DC=LOCAL

name     : Harry Jones
memberof : {CN=Network Team,CN=Users,DC=INLANEFREIGHT,DC=LOCAL, CN=Help Desk,OU=Microsoft Exchange Security
           Groups,DC=INLANEFREIGHT,DC=LOCAL, CN=Security Operations,CN=Users,DC=INLANEFREIGHT,DC=LOCAL, CN=LAPS
           Admins,CN=Users,DC=INLANEFREIGHT,DC=LOCAL...}

```

While uncommon, we find accounts without a password set from time to time, so it is always important to enumerate accounts with the `PASSWD_NOTREQD` flag set and check to see if they indeed do not have a password set. This could happen intentionally (perhaps as a timesaver) or accidentally if a user with this flag set changes their password via command line and accidentally presses enter before typing in a password. All organizations should perform periodic account audits and remove this flag from any accounts that have no valid business reason to have it set.

Try out building some filters of your own. This guide [Active Directory: LDAP Syntax Filters](https://social.technet.microsoft.com/wiki/contents/articles/5392.active-directory-ldap-syntax-filters.aspx) is a great starting point.

* * *

## Recursive Match

We can use the " `RecursiveMatch`" parameter in a similar way that we use the matching rule OID " `1.2.840.113556.1.4.1941`". A good example of this is to find all of the groups that an AD user is a part of, both directly and indirectly. This is also known as "nested group membership." For example, the user `bob.smith` may not be a direct member of the `Domain Admins` group but has `derivative` Domain Admin rights because the group `Security Operations` is a member of the `Domain Admins` group. We can see this graphically by looking at `Active Directory Computers and Users`.

![image](https://academy.hackthebox.com/storage/modules/22/secops_win.png)

We can enumerate this with PowerShell several ways, one way being the " `Get-ADGroupMember`" cmdlet.

#### PowerShell - Members Of Security Operations

```powershell
PS C:\htb> Get-ADGroupMember -Identity "Security Operations"

distinguishedName : CN=Harry Jones,OU=Network Ops,OU=IT,OU=Employees,DC=INLANEFREIGHT,DC=LOCAL
name              : Harry Jones
objectClass       : user
objectGUID        : f6d9b03e-7056-478b-a737-6c3298d18b9d
SamAccountName    : harry.jones
SID               : S-1-5-21-2974783224-3764228556-2640795941-2040

```

As we can see above, the `Security Operations` group is indeed "nested" within the `Domain Admins` group. Therefore any of its members are effectively Domain Admins.

Searching for a user's group membership using `Get-ADUser` focusing on the property `memberof` will not directly show this information.

#### PowerShell - User's Group Membership

```powershell
PS C:\htb> Get-ADUser -Identity harry.jones -Properties * | select memberof | ft -Wrap

memberof
--------
{CN=Network Team,CN=Users,DC=INLANEFREIGHT,DC=LOCAL, CN=Help Desk,OU=Microsoft Exchange Security
Groups,DC=INLANEFREIGHT,DC=LOCAL, CN=Security Operations,CN=Users,DC=INLANEFREIGHT,DC=LOCAL, CN=LAPS
Admins,CN=Users,DC=INLANEFREIGHT,DC=LOCAL...}

```

We can find nested group membership with the matching rule OID and the `RecursiveMatch` parameter, as seen in the following examples. The first example shows an AD filter and the `RecursiveMatch` to recursively query for all groups that the user `harry.jones` is a member of.

#### PowerShell - All Groups of User

```powershell
PS C:\htb> Get-ADGroup -Filter 'member -RecursiveMatch "CN=Harry Jones,OU=Network Ops,OU=IT,OU=Employees,DC=INLANEFREIGHT,DC=LOCAL"' | select name

name
----
Administrators
Backup Operators
Domain Admins
Denied RODC Password Replication Group
LAPS Admins
Security Operations
Help Desk
Network Team

```

Another way to return this same information is by using an `LDAPFilter` and the matching rule OID.

#### LDAP Query - All Groups of User

```powershell
PS C:\htb> Get-ADGroup -LDAPFilter '(member:1.2.840.113556.1.4.1941:=CN=Harry Jones,OU=Network Ops,OU=IT,OU=Employees,DC=INLANEFREIGHT,DC=LOCAL)' |select Name

Name
----
Administrators
Backup Operators
Domain Admins
Denied RODC Password Replication Group
LAPS Admins
Security Operations
Help Desk
Network Team

```

As shown in the above examples, searching recursively in AD can help us enumerate information that standard search queries do not show. Enumerating nested group membership is very important. We may uncover serious misconfigurations within the target AD environment that would otherwise go unnoticed, especially in large organizations with thousands of objects in AD. We will see other ways to enumerate this information and even ways of presenting it in a graphical format, but `RecursiveMatch` is a powerful search parameter that should not be overlooked.

* * *

## SearchBase and SearchScope Parameters

Even small Active Directory environments can contain hundreds if not thousands of objects. Active Directory can grow very quickly as users, groups, computers, OUs, etc., are added, and ACLs are set up, which creates an increasingly complex web of relationships. We may also find ourselves in a vast environment, 10-20 years old, with 10s of thousands of objects. Enumerating these environments can become an unwieldy task, so we need to refine our searches.

We can improve the performance of our enumeration commands and scripts and reduce the volume of objects returned by scoping our searches using the " `SearchBase`" parameter. This parameter specifies an Active Directory path to search under and allows us to begin searching for a user account in a specific OU. The " `SearchBase`" parameter accepts an OUs distinguished name (DN) such as `"OU=Employees,DC=INLANEFREIGHT,DC=LOCAL"`.

" `SearchScope`" allows us to define how deep into the OU hierarchy we would like to search. This parameter has three levels:

| **Name** | **Level** | **Description** |
| --- | --- | --- |
| Base | 0 | The object is specified as the `SearchBase`. For example, if we ask for all users in an OU defining a base scope, we get no results. If we specify a user or use `Get-ADObject` we get just that user or object returned. |
| OneLevel | 1 | Searches for objects in the container defined by the `SearchBase` but not in any sub-containers. |
| SubTree | 2 | Searches for objects contained by the `SearchBase` and all child containers, including their children, recursively all the way down the AD hierarchy. |

When querying AD using " `SearchScope`" we can specify the name or the number (i.e., `SearchScope Onelevel` is interpreted the same as " `SearchScope 1`".)

![image](https://academy.hackthebox.com/storage/modules/22/OU_structures.png)

In the above example, with the SearchBase set to OU=Employees,DC=INLANEFREIGHT,DC=LOCAL, a `SearchScope` set to `Base` would attempt to query the OU object ( `Employees`) itself. A `SearchScope` set to `OneLevel` would search within the `Employees` OU only. Finally, a `SearchScope` set to `SubTree` would query the `Employees` OU and all of the OUs underneath it, such as `Accounting`, `Contractors`, etc. OUs under those OUs (child containers).

* * *

## SearchBase and Search Scope Parameters Examples

Let's look at some examples to illustrate the difference between `Base`, `OneLevel`, and `Subtree`. For these examples, we will focus on the `Employees` OU. In the screenshot of `Active Directory Users and Computers` below `Employees` is the `Base`, and specifying it with `Get-ADUser` will return nothing. `OneLevel` will return just the user `Amelia Matthews`, and `SubTree` will return all users in all child containers under the `Employees` container.

![image](https://academy.hackthebox.com/storage/modules/22/ou_base.png)

We can confirm these results using PowerShell. For reference purposes, let's get a count of all AD users under the `Employees` OU, which shows 970 users.

#### PowerShell - Count of All AD Users

```powershell
PS C:\htb> (Get-ADUser -SearchBase "OU=Employees,DC=INLANEFREIGHT,DC=LOCAL" -Filter *).count

970

```

As expected, specifying a SearchScope of `Base` will return nothing.

#### PowerShell - SearchScope Base

```powershell
PS C:\htb> Get-ADUser -SearchBase "OU=Employees,DC=INLANEFREIGHT,DC=LOCAL" -SearchScope Base -Filter *
PS C:\htb>

```

However, if we specify " `Base`" with " `Get-ADObject`" we will get just the object (Employees OU) returned to us.

#### PowerShell - SearchScope Base OU Object

```powershell
PS C:\htb> Get-ADObject -SearchBase "OU=Employees,DC=INLANEFREIGHT,DC=LOCAL" -SearchScope Base -Filter *

DistinguishedName                      Name      ObjectClass        ObjectGUID
-----------------                      ----      -----------        ----------
OU=Employees,DC=INLANEFREIGHT,DC=LOCAL Employees organizationalUnit 34f42767-8a2e-493f-afc6-556bdc0b1087

```

If we specify `OneLevel` as the SearchScope, we get one user returned to us, as expected per the image above.

#### PowerShell - Searchscope OneLevel

```powershell
PS C:\htb> Get-ADUser -SearchBase "OU=Employees,DC=INLANEFREIGHT,DC=LOCAL" -SearchScope OneLevel -Filter *

DistinguishedName : CN=Amelia Matthews,OU=Employees,DC=INLANEFREIGHT,DC=LOCAL
Enabled           : True
GivenName         : amelia
Name              : Amelia Matthews
ObjectClass       : user
ObjectGUID        : 3f04328f-eb2e-487c-85fe-58dd598159c0
SamAccountName    : amelia.matthews
SID               : S-1-5-21-2974783224-3764228556-2640795941-1412
Surname           : matthews
UserPrincipalName : amelia.matthews@inlanefreight

```

As stated above, the `SearchScope` values are interchangeable, so the same result is returned when specifying `1` as the `SearchScope` value.

#### PowerShell - Searchscope 1

```powershell
PS C:\htb> Get-ADUser -SearchBase "OU=Employees,DC=INLANEFREIGHT,DC=LOCAL" -SearchScope 1 -Filter *

DistinguishedName : CN=Amelia Matthews,OU=Employees,DC=INLANEFREIGHT,DC=LOCAL
Enabled           : True
GivenName         : amelia
Name              : Amelia Matthews
ObjectClass       : user
ObjectGUID        : 3f04328f-eb2e-487c-85fe-58dd598159c0
SamAccountName    : amelia.matthews
SID               : S-1-5-21-2974783224-3764228556-2640795941-1412
Surname           : matthews
UserPrincipalName : amelia.matthews@inlanefreight

```

Finally, if we specify `Subtree` as the SearchBase, we will get all objects within all child containers, which matches the user count we established above.

#### PowerShell - Searchscope Subtree

```powershell
PS C:\htb> (Get-ADUser -SearchBase "OU=Employees,DC=INLANEFREIGHT,DC=LOCAL" -SearchScope Subtree -Filter *).count

970

```

* * *

## Conclusion

This section, as well as the PowerShell Filters section, covered the many ways we can use search filters combined with built-in AD cmdlets to enhance our enumeration by "living off the land." In later sections, we will cover tools that make enumeration much quicker and easier and be combined with filters to be even more powerful. Regardless of if we are using built-in tools, custom scripts or, third-party tools, it is important to understand what they are doing and to be able to understand and use the output of our enumeration to help us achieve our goal.

Note: When spawning your target, we ask you to wait for 3 minutes until the whole lab with all the configurations is set up so that the connection to your target works flawlessly.


# Enumerating Active Directory with Built-in Tools

* * *

Proper enumeration is key for all penetration testing and red teaming assessments. Enumerating AD, especially large corporate environments with many hosts, users, and services, can be quite a daunting task and provide an overwhelming amount of data. Several built-in Windows tools can be used by sysadmins and pentesters to enumerate AD. Open source tools have been created based on the same enumeration techniques. Many of these tools (such as SharpView, BloodHound, and, PingCastle) can be utilized to expedite the enumeration process and accurately present the data in a consumable and actionable format. Knowledge of multiple tools and "offense in-depth" is important if you must live off the land on an assessment or detections are in place for certain tools.

* * *

## User-Account-Control (UAC) Attributes

User-Account-Control Attributes control the behavior of domain accounts. These values are not to be confused with the Windows User Account Control technology. Many of these UAC attributes have security relevance:

![image](https://academy.hackthebox.com/storage/modules/22/UAC1.png)

We can enumerate these values with built-in AD cmdlets:

#### PowerShell - Built-in AD Cmdlets

```powershell
PS C:\htb> Get-ADUser -Filter {adminCount -gt 0} -Properties admincount,useraccountcontrol | select Name,useraccountcontrol

Name           useraccountcontrol
----           ------------------
Administrator               66048
krbtgt                      66050
daniel.carter                 512
sqlqa                         512
svc-backup                  66048
svc-secops                  66048
cliff.moore                 66048
svc-ata                       512
svc-sccm                      512
mrb3n                         512
sarah.lafferty                512
Jenna Smith               4260384
Harry Jones                 66080
pixis                         512
Cry0l1t3                      512
knightmare                    512

```

We still need to convert the `useraccountcontrol` values into their corresponding flags to interpret them. This can be done with this [script](https://academy.hackthebox.com/storage/resources/Convert-UserAccountControlValues.zip). Let's take the user `Jenna Smith` with `useraccountcontrol` value `4260384` as an example.

#### PowerShell - UAC Values

```powershell
PS C:\htb> .\Convert-UserAccountControlValues.ps1

Please provide the userAccountControl value: : 4260384

Name                           Value
----                           -----
PASSWD_NOTREQD                 32
NORMAL_ACCOUNT                 512
DONT_EXPIRE_PASSWORD           65536
DONT_REQ_PREAUTH               4194304

```

We can also use [PowerView](https://github.com/PowerShellMafia/PowerSploit/blob/dev/Recon/PowerView.ps1) (which will be covered in-depth in subsequent modules) to enumerate these values. We can see that some of the users match the default value of `512` or `Normal_Account` while others would need to be converted. The value for `jenna.smith` does match what our conversion script provided.

`PowerView` can be found in the `c:\tools` directory on the target host. To load the tool, open a PowerShell console, navigate to the tools directory, and import `PowerView` using the command `Import-Module .\PowerView.ps1`.

#### PowerView - Domain Accounts

```powershell
PS C:\htb> Get-DomainUser * -AdminCount | select samaccountname,useraccountcontrol

samaccountname                                                     useraccountcontrol
--------------                                                     ------------------
Administrator                                    NORMAL_ACCOUNT, DONT_EXPIRE_PASSWORD
krbtgt                           ACCOUNTDISABLE, NORMAL_ACCOUNT, DONT_EXPIRE_PASSWORD
daniel.carter                                                          NORMAL_ACCOUNT
sqlqa                                                                  NORMAL_ACCOUNT
svc-backup                                       NORMAL_ACCOUNT, DONT_EXPIRE_PASSWORD
svc-secops                                       NORMAL_ACCOUNT, DONT_EXPIRE_PASSWORD
cliff.moore                                      NORMAL_ACCOUNT, DONT_EXPIRE_PASSWORD
svc-ata                                                                NORMAL_ACCOUNT
svc-sccm                                                               NORMAL_ACCOUNT
mrb3n                                                                  NORMAL_ACCOUNT
sarah.lafferty                                                         NORMAL_ACCOUNT
jenna.smith    PASSWD_NOTREQD, NORMAL_ACCOUNT, DONT_EXPIRE_PASSWORD, DONT_REQ_PREAUTH
harry.jones                      PASSWD_NOTREQD, NORMAL_ACCOUNT, DONT_EXPIRE_PASSWORD
pixis                                                                  NORMAL_ACCOUNT
Cry0l1t3                                                               NORMAL_ACCOUNT
knightmare                                                             NORMAL_ACCOUNT

```

* * *

## Enumeration Using Built-In Tools

Tools that sysadmins are themselves likely to use, such as the PowerShell AD Module, the Sysinternals Suite, and AD DS Tools, are likely to be whitelisted and fly under the radar, especially in more mature environments. Several built-in tools can be leveraged for AD enumeration, including:

`DS Tools` is available by default on all modern Windows operating systems but required domain connectivity to perform enumeration activities.

#### DS Tools

```cmd-session
C:\htb> dsquery user "OU=Employees,DC=inlanefreight,DC=local" -name * -scope subtree -limit 0 | dsget user -samid -
pwdneverexpires | findstr /V no

  samid                  pwdneverexpires
  svc-backup             yes
  svc-scan               yes
  svc-secops             yes
  sql-test               yes
  cliff.moore            yes
  margaret.harris        yes

  <SNIP>

dsget succeeded

```

The `PowerShell Active Directory module` is a group of cmdlets used to manage Active Directory. The installation of the AD PowerShell module requires administrative access.

#### AD PowerShell Module

```powershell
PS C:\htb> Get-ADUser -Filter * -SearchBase 'OU=Admin,DC=inlanefreight,dc=local'

DistinguishedName : CN=wilford.stewart,OU=Admin,DC=INLANEFREIGHT,DC=LOCAL
Enabled           : True
GivenName         :
Name              : wilford.stewart
ObjectClass       : user
ObjectGUID        : 1f54c02c-2fb4-48b6-a89c-38b6b0c54147
SamAccountName    : wilford.stewart
SID               : S-1-5-21-2974783224-3764228556-2640795941-2121
Surname           :
UserPrincipalName :

DistinguishedName : CN=trisha.duran,OU=Admin,DC=INLANEFREIGHT,DC=LOCAL
Enabled           : True
GivenName         :
Name              : trisha.duran
ObjectClass       : user
ObjectGUID        : 7a8db2bb-7b24-4f79-a3fe-7b49408bc7bf
SamAccountName    : trisha.duran
SID               : S-1-5-21-2974783224-3764228556-2640795941-2122
Surname           :
UserPrincipalName :

<SNIP>

```

`Windows Management Instrumentation` (WMI) can also be used to access and query objects in Active Directory. Many scripting languages can interact with the WMI AD provider, but PowerShell makes this very easy.

#### Windows Management Instrumentation (WMI)

```powershell
PS C:\htb> Get-WmiObject -Class win32_group -Filter "Domain='INLANEFREIGHT'" | Select Caption,Name

Caption                                               Name
-------                                               ----
INLANEFREIGHT\Cert Publishers                         Cert Publishers
INLANEFREIGHT\RAS and IAS Servers                     RAS and IAS Servers
INLANEFREIGHT\Allowed RODC Password Replication Group Allowed RODC Password Replication Group
INLANEFREIGHT\Denied RODC Password Replication Group  Denied RODC Password Replication Group
INLANEFREIGHT\DnsAdmins                               DnsAdmins
INLANEFREIGHT\$6I2000-MBUUOKUK1E1O                    $6I2000-MBUUOKUK1E1O
INLANEFREIGHT\Cloneable Domain Controllers            Cloneable Domain Controllers
INLANEFREIGHT\Compliance Management                   Compliance Management
INLANEFREIGHT\Delegated Setup                         Delegated Setup
INLANEFREIGHT\Discovery Management                    Discovery Management
INLANEFREIGHT\DnsUpdateProxy                          DnsUpdateProxy
INLANEFREIGHT\Domain Admins                           Domain Admins
INLANEFREIGHT\Domain Computers                        Domain Computers
INLANEFREIGHT\Domain Controllers                      Domain Controllers
INLANEFREIGHT\Domain Guests                           Domain Guests
INLANEFREIGHT\Domain Users                            Domain Users
INLANEFREIGHT\Enterprise Admins                       Enterprise Admins
INLANEFREIGHT\Enterprise Key Admins                   Enterprise Key Admins
INLANEFREIGHT\Enterprise Read-only Domain Controllers Enterprise Read-only Domain Controllers
INLANEFREIGHT\Exchange Servers                        Exchange Servers
INLANEFREIGHT\Exchange Trusted Subsystem              Exchange Trusted Subsystem
INLANEFREIGHT\Exchange Windows Permissions            Exchange Windows Permissions
INLANEFREIGHT\ExchangeLegacyInterop                   ExchangeLegacyInterop
INLANEFREIGHT\Group Policy Creator Owners             Group Policy Creator Owners
INLANEFREIGHT\Help Desk                               Help Desk
INLANEFREIGHT\Hygiene Management                      Hygiene Management
INLANEFREIGHT\Key Admins                              Key Admins
INLANEFREIGHT\LAPS Admins                             LAPS Admins
INLANEFREIGHT\Managed Availability Servers            Managed Availability Servers
INLANEFREIGHT\Organization Management                 Organization Management
INLANEFREIGHT\Protected Users                         Protected Users

<SNIP>

```

`Active Directory Service Interfaces` (ADSI) is a set of COM interfaces that can query Active Directory. PowerShell again provides an easy way to interact with it.

#### AD Service Interfaces (ADSI)

```powershell
PS C:\htb> ([adsisearcher]"(&(objectClass=Computer))").FindAll() | select Path

Path
----
LDAP://CN=DC01,OU=Domain Controllers,DC=INLANEFREIGHT,DC=LOCAL
LDAP://CN=EXCHG01,OU=Mail Servers,OU=Servers,DC=INLANEFREIGHT,DC=LOCAL
LDAP://CN=SQL01,OU=SQL Servers,OU=Servers,DC=INLANEFREIGHT,DC=LOCAL
LDAP://CN=WS01,OU=Staff Workstations,OU=Workstations,DC=INLANEFREIGHT,DC=LOCAL
LDAP://CN=DC02,OU=Servers,DC=INLANEFREIGHT,DC=LOCAL

```

Note: When spawning your target, we ask you to wait for 3 minutes until the whole lab with all the configurations is set up so that the connection to your target works flawlessly.


# LDAP Anonymous Bind

Lightweight Directory Access Protocol (LDAP) is a protocol that is used for accessing directory services.

* * *

## Leveraging LDAP Anonymous Bind

LDAP anonymous binds allow unauthenticated attackers to retrieve information from the domain, such as a full listing of users, groups, computers, user account attributes, and the domain password policy. Linux hosts running open-source versions of LDAP and Linux vCenter appliances are often configured to allow anonymous binds.

When an LDAP server allows anonymous base binds, an attacker does not need to know a base object to query a considerable amount of information from the domain. This can also be leveraged to mount a password spraying attack or read information such as passwords stored in account description fields. Tools such as [windapsearch](https://github.com/ropnop/windapsearch) and [ldapsearch](https://linux.die.net/man/1/ldapsearch) can be utilized to enumerate domain information via an anonymous LDAP bind. Information that we obtain from an anonymous LDAP bind can be leveraged to mount a password spraying or AS-REPRoasting attack, read information such as passwords stored in account description fields.

We can use `Python` to quickly check if we can interact with LDAP without credentials.

```python
Python 3.8.5 (default, Aug  2 2020, 15:09:07)
[GCC 10.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from ldap3 import *
>>> s = Server('10.129.1.207',get_info = ALL)
>>> c =  Connection(s, '', '')
>>> c.bind()
True
>>> s.info
DSA info (from DSE):
  Supported LDAP versions: 3, 2
  Naming contexts:
    DC=INLANEFREIGHT,DC=LOCAL
    CN=Configuration,DC=INLANEFREIGHT,DC=LOCAL
    CN=Schema,CN=Configuration,DC=INLANEFREIGHT,DC=LOCAL
    DC=DomainDnsZones,DC=INLANEFREIGHT,DC=LOCAL
    DC=ForestDnsZones,DC=INLANEFREIGHT,DC=LOCAL
  Supported controls:

	<SNIP>

  dnsHostName:
    DC01.INLANEFREIGHT.LOCAL
  ldapServiceName:
    INLANEFREIGHT.LOCAL:[email protected]
  serverName:
    CN=DC01,CN=Servers,CN=Default-First-Site-Name,CN=Sites,CN=Configuration,DC=INLANEFREIGHT,DC=LOCAL
  isSynchronized:
    TRUE
  isGlobalCatalogReady:
    TRUE
  domainFunctionality:
    7
  forestFunctionality:
    7
  domainControllerFunctionality:
    7

```

* * *

## Using Ldapsearch

We can confirm anonymous LDAP bind with `ldapsearch` and retrieve all AD objects from LDAP.

```shell
ldapsearch -H ldap://10.129.1.207 -x -b "dc=inlanefreight,dc=local"
# extended LDIF
#
# LDAPv3
# base <dc=inlanefreight,dc=local> with scope subtree
# filter: (objectclass=*)
# requesting: ALL
#

# INLANEFREIGHT.LOCAL
dn: DC=INLANEFREIGHT,DC=LOCAL
objectClass: top
objectClass: domain
objectClass: domainDNS
distinguishedName: DC=INLANEFREIGHT,DC=LOCAL
instanceType: 5
whenCreated: 20200726201343.0Z
whenChanged: 20200827025341.0Z
subRefs: DC=LOGISTICS,DC=INLANEFREIGHT,DC=LOCAL
subRefs: DC=ForestDnsZones,DC=INLANEFREIGHT,DC=LOCAL
subRefs: DC=DomainDnsZones,DC=INLANEFREIGHT,DC=LOCAL
subRefs: CN=Configuration,DC=INLANEFREIGHT,DC=LOCAL

```

## Using Windapsearch

`Windapsearch` is a Python script used to perform anonymous and authenticated LDAP enumeration of AD users, groups, and computers using LDAP queries. It is an alternative to tools such as `ldapsearch`, which require you to craft custom LDAP queries. We can use it to confirm LDAP NULL session authentication but providing a blank username with `-u ""` and add ` --functionality` to confirm the domain functional level.

```shell
python3 windapsearch.py --dc-ip 10.129.1.207 -u "" --functionality
[+] No username provided. Will try anonymous bind.
[+] Using Domain Controller at: 10.129.1.207
[+] Getting defaultNamingContext from Root DSE
[+]	Found: DC=INLANEFREIGHT,DC=LOCAL
[+] Functionality Levels:
[+]	 domainFunctionality: 2016
[+]	 forestFunctionality: 2016
[+]	 domainControllerFunctionality: 2016
[+] Attempting bind
[+]	...success! Binded as:
[+]	 None

[*] Bye!

```

We can pull a listing of all domain users to use in a password spraying attack.

```shell
python3 windapsearch.py --dc-ip 10.129.1.207 -u "" -U
[+] No username provided. Will try anonymous bind.
[+] Using Domain Controller at: 10.129.1.207
[+] Getting defaultNamingContext from Root DSE
[+]	Found: DC=INLANEFREIGHT,DC=LOCAL
[+] Attempting bind
[+]	...success! Binded as:
[+]	 None

[+] Enumerating all AD users
[+]	Found 1024 users:

cn: Guest
cn: DefaultAccount
cn: LOGISTICS$
cn: sqldev
cn: sqlprod
cn: svc-scan

<SNIP>

```

We can obtain information about all domain computers.

```shell
python3 windapsearch.py --dc-ip 10.129.1.207 -u "" -C
[+] No username provided. Will try anonymous bind.
[+] Using Domain Controller at: 10.129.1.207
[+] Getting defaultNamingContext from Root DSE
[+]	Found: DC=INLANEFREIGHT,DC=LOCAL
[+] Attempting bind
[+]	...success! Binded as:
[+]	 None

[+] Enumerating all AD computers
[+]	Found 5 computers:

cn: DC01
operatingSystem: Windows Server 2016 Standard
operatingSystemVersion: 10.0 (14393)
dNSHostName: DC01.INLANEFREIGHT.LOCAL

cn: EXCHG01
operatingSystem: Windows Server 2016 Standard
operatingSystemVersion: 10.0 (14393)
dNSHostName: EXCHG01.INLANEFREIGHT.LOCAL

cn: SQL01
operatingSystem: Windows Server 2016 Standard
operatingSystemVersion: 10.0 (14393)
dNSHostName: SQL01.INLANEFREIGHT.LOCAL

cn: WS01
operatingSystem: Windows Server 2016 Standard
operatingSystemVersion: 10.0 (14393)
dNSHostName: WS01.INLANEFREIGHT.LOCAL

cn: DC02
dNSHostName: DC02.INLANEFREIGHT.LOCAL

[*] Bye!

```

This process can be repeated to pull group information and more detailed information such as unconstrained users and computers, GPO information, user and computer attributes, and more.

* * *

## Other Tools

There are many other tools and helper scripts for retrieving information from LDAP. This script [ldapsearch-ad.py](https://github.com/yaap7/ldapsearch-ad) is similar to `windapsearch`.

```shell
python3 ldapsearch-ad.py -h
usage: ldapsearch-ad.py [-h] -l LDAP_SERVER [-ssl] -t REQUEST_TYPE [-d DOMAIN] [-u USERNAME] [-p PASSWORD]
                        [-s SEARCH_FILTER] [-z SIZE_LIMIT] [-o OUTPUT_FILE] [-v]
                        [search_attributes [search_attributes ...]]

Active Directory LDAP Enumerator

positional arguments:
  search_attributes     LDAP attributes to look for (default is all).

optional arguments:
  -h, --help            show this help message and exit
  -l LDAP_SERVER, --server LDAP_SERVER
                        IP address of the LDAP server.
  -ssl, --ssl           Force an SSL connection?.
  -t REQUEST_TYPE, --type REQUEST_TYPE
                        Request type: info, whoami, search, search-large, trusts, pass-pols, show-admins,
                        show-user, show-user-list, kerberoast, all
  -d DOMAIN, --domain DOMAIN
                        Authentication account's FQDN. Example: "contoso.local".
  -u USERNAME, --username USERNAME
                        Authentication account's username.
  -p PASSWORD, --password PASSWORD
                        Authentication account's password.
  -s SEARCH_FILTER, --search-filter SEARCH_FILTER
                        Search filter (use LDAP format).
  -z SIZE_LIMIT, --size_limit SIZE_LIMIT
                        Size limit (default is 100, or server' own limit).
  -o OUTPUT_FILE, --output OUTPUT_FILE
                        Write results in specified file too.
  -v, --verbose         Turn on debug mode

```

We can use it to pull domain information and confirm a NULL bind. This particular tool requires valid domain user credentials to perform additional enumeration.

```shell
python3 ldapsearch-ad.py -l 10.129.1.207 -t info

### Server infos ###
[+] Forest functionality level = Windows 2016
[+] Domain functionality level = Windows 2016
[+] Domain controller functionality level = Windows 2016
[+] rootDomainNamingContext = DC=INLANEFREIGHT,DC=LOCAL
[+] defaultNamingContext = DC=INLANEFREIGHT,DC=LOCAL
[+] ldapServiceName = INLANEFREIGHT.LOCAL:[email protected]
[+] naming_contexts = ['DC=INLANEFREIGHT,DC=LOCAL', 'CN=Configuration,DC=INLANEFREIGHT,DC=LOCAL', 'CN=Schema,CN=Configuration,DC=INLANEFREIGHT,DC=LOCAL', 'DC=DomainDnsZones,DC=INLANEFREIGHT,DC=LOCAL', 'DC=ForestDnsZones,DC=INLANEFREIGHT,DC=LOCAL']

```

Note: Tools necessary for completing this section can be found in the \`/opt\` directory on the Pwnbox.

Note: When spawning your target, we ask you to wait for 3 minutes until the whole lab with all the configurations is set up so that the connection to your target works flawlessly.


# Credentialed LDAP Enumeration

As with SMB, once we have domain credentials, we can extract a wide variety of information from LDAP, including user, group, computer, trust, GPO info, the domain password policy, etc. `ldapsearch-ad.py` and `windapsearch` are useful for performing this enumeration.

* * *

## Windapsearch

```shell
python3 windapsearch.py --dc-ip 10.129.1.207 -u inlanefreight\\james.cross --da

Password for inlanefreight\james.cross:

[+] Using Domain Controller at: 10.129.1.207
[+] Getting defaultNamingContext from Root DSE
[+]	Found: DC=INLANEFREIGHT,DC=LOCAL
[+] Attempting bind
[+]	...success! Binded as:
[+]	 u:INLANEFREIGHT\james.cross
[+] Attempting to enumerate all Domain Admins
[+] Using DN: CN=Domain Admins,CN=Users.CN=Domain Admins,CN=Users,DC=INLANEFREIGHT,DC=LOCAL
[+]	Found 14 Domain Admins:

cn: Administrator
userPrincipalName: [email protected]

cn: daniel.carter
cn: sqlqa
cn: svc-backup
cn: svc-secops
cn: cliff.moore
cn: svc-ata
cn: svc-sccm
cn: mrb3n
cn: sarah.lafferty

cn: Harry Jones
userPrincipalName: harry.jones@inlanefreight

cn: pixis
cn: Cry0l1t3
cn: knightmare

[+] Using DN: CN=Domain Admins,CN=Users.CN=Domain Admins,CN=Users,DC=INLANEFREIGHT,DC=LOCAL
[+]	Found 14 Domain Admins:

cn: Administrator
userPrincipalName: [email protected]

cn: daniel.carter
cn: sqlqa
cn: svc-backup
cn: svc-secops

<SNIP>

```

Some additional useful options, including pulling users and computers with unconstrained delegation.

```shell
python3 windapsearch.py --dc-ip 10.129.1.207 -d inlanefreight.local -u inlanefreight\\james.cross --unconstrained-users

Password for inlanefreight\james.cross:

[+] Using Domain Controller at: 10.129.1.207
[+] Getting defaultNamingContext from Root DSE
[+]	Found: DC=INLANEFREIGHT,DC=LOCAL
[+] Attempting bind
[+]	...success! Binded as:
[+]	 u:INLANEFREIGHT\james.cross
[+] Attempting to enumerate all user objects with unconstrained delegation
[+]	Found 1 Users with unconstrained delegation:

CN=sqldev,OU=Service Accounts,OU=IT,OU=Employees,DC=INLANEFREIGHT,DC=LOCAL

[*] Bye!

```

* * *

## Ldapsearch-ad

This tool can perform all of the standard enumeration and a few built-in searches to simplify things. We can quickly obtain the password policy.

```shell
python3 ldapsearch-ad.py -l 10.129.1.207 -d inlanefreight -u james.cross -p Summer2020 -t pass-pols

### Result of "pass-pols" command ###
Default password policy:
[+] |___Minimum password length = 7
[+] |___Password complexity = Disabled
[*] |___Lockout threshold = Disabled
[+] No fine grained password policy found (high privileges are required).

```

We can look for users who may be subject to a Kerberoasting attack.

```shell
python3 ldapsearch-ad.py -l 10.129.1.207 -d inlanefreight -u james.cross -p Summer2020 -t kerberoast | grep servicePrincipalName:

    servicePrincipalName: CIFS/roguecomputer.inlanefreight.local
    servicePrincipalName: MSSQLSvc/sql01:1433
    servicePrincipalName: MSSQL_svc_qa/inlanefreight.local:1443
    servicePrincipalName: MSSQL_svc_test/inlanefreight.local:1443
    servicePrincipalName: IIS_dev/inlanefreight.local:80

```

Also, it quickly retrieves users that can be ASREPRoasted.

```shell
python3 ldapsearch-ad.py -l 10.129.1.207 -d inlanefreight -u james.cross -p Summer2020 -t asreproast

### Result of "asreproast" command ###
[*] DN: CN=Amber Smith,OU=Contractors,OU=Employees,DC=INLANEFREIGHT,DC=LOCAL - STATUS: Read - READ TIME: 2020-09-02T17:11:45.572421
    cn: Amber Smith
    sAMAccountName: amber.smith

[*] DN: CN=Jenna Smith,OU=Server Team,OU=IT,OU=Employees,DC=INLANEFREIGHT,DC=LOCAL - STATUS: Read - READ TIME: 2020-09-02T17:11:45.572729
    cn: Jenna Smith
    sAMAccountName: jenna.smith

```

* * *

## LDAP Wrap-up

We can use tools such as the two shown in this section to perform a considerable amount of AD enumeration using LDAP. The tools have many built-in queries to simplify searching and provide us with the most useful and actionable data. We can also combine these tools with the custom LDAP search filters that we learned about earlier in the module. These are great tools to keep in our arsenal, especially when we are in a position where most an AD assessment has to be performed from a Linux attack box.

Note: When spawning your target, we ask you to wait for 3 minutes until the whole lab with all the configurations is set up so that the connection to your target works flawlessly.


# Active Directory LDAP - Skills Assessment

* * *

You have been contracted by the `INLANEFREIGHT` organization to perform an Active Directory security assessment to assess what flaws exist that could potentially be exploited by an attacker who gains internal network access with a standard Domain User account.

Connect to the target host and perform the enumeration tasks listed below to complete this module.

Note: When spawning your target, we ask you to wait for 3-5 minutes until the whole lab with all the configurations is set up so that the connection to your target works flawlessly.


