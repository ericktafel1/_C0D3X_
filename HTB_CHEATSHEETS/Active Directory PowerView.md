| **Command**                                                                                 | **Description**                                                               |     |
| ------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------- | --- |
| `xfreerdp /v:<target IP address> /u:htb-student /p:<password>`                              | RDP to lab target                                                             |     |
|  `Get-DomainPolicy`                                                                         | View the domain password policy                                               |     |
| `.\SharpView.exe ConvertTo-SID -Name sally.jones`                                           | Convert a username to a SID                                                   |     |
| `.\SharpView.exe Convert-ADName -ObjectName S-1-5-21-2974783224-3764228556-2640795941-1724` | Convert a SID to a username                                                   |     |
| `Get-DomainUser harry.jones  \| ConvertFrom-UACValue -showall`                              | List all UAC values                                                           |     |
| `.\SharpView.exe Get-Domain`                                                                | View information about the current domain                                     |     |
| `.\SharpView.exe Get-DomainOU`                                                              | List all OUs                                                                  |     |
| `.\SharpView.exe Get-DomainUser -KerberosPreauthNotRequired`                                | Find ASREPRoastable users                                                     |     |
| `Get-DomainComputer `                                                                       | Get a listing of domain computers                                             |     |
| `.\SharpView.exe Get-DomainGPO  \| findstr displayname`                                     | List all GPO names                                                            |     |
| ` Get-DomainGPO -ComputerIdentity WS01`                                                     | List GPOs on a specific host                                                  |     |
| `Test-AdminAccess -ComputerName SQL01`                                                      | Test local admin access on a remote host                                      |     |
| `.\SharpView.exe Get-NetShare -ComputerName SQL01`                                          | Enumerate open shares on a remote computer                                    |     |
| `Find-DomainUserLocation`                                                                   | Find machines where domain users are logged in                                |     |
| `Get-DomainTrust`                                                                           | View a list of domain trusts                                                  |     |
| `(Get-DomainUser).count`                                                                    | Count all domain users                                                        |     |
| `.\SharpView.exe Get-DomainUser -Help`                                                      | Get help about a SharpView function                                           |     |
| `Get-DomainUser -Properties samaccountname,description \| Where {$_.description -ne $null}` | Find non-blank user description fields                                        |     |
| `.\SharpView.exe Get-DomainUser -SPN`                                                       | Find users with SPNs set                                                      |     |
| `Find-ForeignGroup`                                                                         | Find foreign domain users                                                     |     |
| `Get-DomainGroup -Properties Name`                                                          | List domain groups                                                            |     |
| `.\SharpView.exe Get-DomainGroupMember -Identity 'Help Desk'`                               | Get members of a domain group                                                 |     |
| `.\SharpView.exe Get-DomainGroup -AdminCount`                                               | List protected groups                                                         |     |
| `.\SharpView.exe Find-ManagedSecurityGroups`                                                | List managed security groups                                                  |     |
| `Get-NetLocalGroup -ComputerName WS01`                                                      | Get local groups on a host                                                    |     |
| `.\SharpView.exe Get-NetLocalGroupMember -ComputerName WS01`                                | Get members of a local group                                                  |     |
| `.\SharpView.exe Get-DomainComputer -Unconstrained`                                         | Find computers that allow unconstrained delegation                            |     |
| `Get-DomainComputer -TrustedToAuth`                                                         | Find computers set with constrained delegation                                |     |
| `Get-DomainObjectAcl -Identity harry.jones`                                                 | Enumerate ACLs on a user                                                      |     |
| `Find-InterestingDomainAcl`                                                                 | Find objects in the domain with modification rights over non built-in objects |     |
| `Get-PathAcl "\\SQL01\DB_backups"`                                                          | Find the ACLs set on a directory                                              |     |
| ` gpresult /r /S WS01`                                                                      | Get a report of all GPOs applied to a host                                    |     |
| ` Get-DomainGPO  \| Get-ObjectAcl`                                                          | Find GPO permissions                                                          |     |
| `Get-DomainTrustMapping`                                                                    | Enumerate trusts for our domain/reachable domains                             |     |

## Enumerating Users

```powershell
# Get all users
Get-DomainUser

# Find users with a specific property
Get-DomainUser -Properties samaccountname,description | Where-Object {$_.description -ne $null}

# Convert username to SID
Convert-NameToSid <username>

# Convert SID to username
Convert-SidToName <SID>
```

## Enumerating Groups
```powershell
# Get all groups
Get-DomainGroup

# Get members of a specific group
Get-DomainGroupMember -Identity <group_name>

# Find members of a local group on a specific computer
Find-DomainLocalGroupMember -ComputerName <computer_name> -GroupName <group_name>

Get-DomainGroup -Properties * -Identity 'Citrix Admins' | select cn,managedby
```

## Enumerating Computers
```rust
# Get all domain computers
Get-DomainComputer

# Get detailed info about a specific computer
Get-DomainComputer -Identity <computer_name> -Properties *

# Count domain computers
(Get-DomainComputer).count

# Enumates Discriptions
Get-DomainComputer -Properties description | Where-Object { $_.description -match '\w' }
```

## Enumerating GPOs
```rust
# Get all Group Policy Objects (GPOs)
Get-DomainGPO

# Get GPO applied to a specific computer
Get-DomainGPO -ComputerIdentity <computer_name>

# Find specific GPO by name
Get-DomainGPO -Identity <gpo_name>

```

## Enumerating Trusts
```powershell
# Get all domain trusts
Get-DomainTrust

# Get detailed trust mapping
Get-DomainTrustMapping
```

## ACL & Permissions
```powershell
# Find users with specific rights on an object
(Get-ACL "AD:$((Get-ADUser <username>).distinguishedname)").Access | Where-Object { $_.ActiveDirectoryRights -match "GenericAll" }

# Find users with DCSync rights
$dcsync = Get-ObjectACL "DC=inlanefreight,DC=local" -ResolveGUIDs | ? { ($_.ActiveDirectoryRights -match 'GenericAll') -or ($_.ObjectAceType -match 'Replication-Get')} | Select-Object -ExpandProperty SecurityIdentifier | Select -ExpandProperty value
Convert-SidtoName $dcsync
```

## Enumerating Shares
```rust
# Find all shares on a computer
Get-NetShare -ComputerName <computer_name>
	```

## Domain Policy
```rust
# Get domain password policy 
(Get-DomainPolicy)."SystemAccess"
```

## Find Users with Kerberos Constrained Delegation
```powershell
Get-DomainUser -TrustedToAuth
```

## Check SID for a User
```powershell
Convert-NameToSid <username>
```

## Find Non-Standard Shares
```powershell
Get-NetShare -ComputerName <computer_name> | Where-Object { $_.Name -notmatch "^(ADMIN\$|C\$|IPC\$)$" }
```