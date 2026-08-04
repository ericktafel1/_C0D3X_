# Introduction

Digital forensics involves examining and analyzing digital evidence to understand user behavior. User behavior analysis is essential in digital forensics, especially when investigating suspicious employee activities and insider threats, or when creating detailed profiles of user identities. These profiles include metadata on activities, preferences, and typical actions, providing a baseline for normal behavior. By analyzing digital artifacts, forensic investigators can reconstruct user actions and determine if any activities deviated from standard behavior patterns, indicating potential misconduct.

According to Wikipedia, [forensic profiling](https://en.wikipedia.org/wiki/Forensic_profiling) involves studying [trace evidence](https://en.wikipedia.org/wiki/Trace_evidence) to gather information that law enforcement can use to identify suspects and secure convictions in court. In information sciences, this process involves uncovering connections between data in databases to identify and represent a subject, whether human or non-human, individual or group. This process is similar to user behavior analysis in digital forensics, especially when examining Windows-based operating systems and conducting registry forensics.

Just as forensic profiling helps create a picture of a suspect's actions and patterns, analyzing Windows registry artifacts can reveal a user's behavior and activities on their computer. The image below illustrates how a user profile is constructed using various registry artifacts.

![User Profile](https://academy.hackthebox.com/storage/modules/248/userprofile.png)

## What is Registry Data?

The Windows Registry is a hierarchical database used by the Windows operating system to store configuration settings, system information, and data about installed software, user profiles, and hardware. It includes settings for the operating system, applications, users, and many other system components. The registry is divided into `keys` and `values`, that resemble folders and files. Keys can contain other keys ( `subkeys`) or values, and values store the actual data, which can be in different formats such as strings, integers, or binary.

### Key Components of the Registry

- `HKEY_LOCAL_MACHINE (HKLM)`: Contains system-wide settings and configurations for the OS and hardware.
- `HKEY_CURRENT_USER (HKCU)`: Contains settings related to the currently logged-in user.
- `HKEY_CLASSES_ROOT (HKCR)`: Contains information about file associations and registered applications.
- `HKEY_USERS (HKU)`: Stores settings for all users on the system.
- `HKEY_CURRENT_CONFIG (HKCC)`: Contains current hardware profile settings.

## How is Registry Data Created?

Registry data is created as a result of user or application interactions with the operating system and activities within local systems, networks, and other digital devices. Analyzing this data can help investigators with a wide range of digital traces, including application usage, file access, web browsing history, and other activities on the system. These artifacts are valuable for forensic investigations and understanding users' actions and intentions within a digital environment.

This eventually can answer key investigative questions such as `who`, `when`, `what`, `where`, `why`, and `how`. Importantly, analysis isn't just about proving that an incident occurred; it can also be used to demonstrate that an event did not take place, highlighting its importance in both confirming and dispelling suspicions.

From the applications users use to the times they log in and out, the Registry captures it all. It's like a digital diary, but one that users may not even be aware of. In this module, we'll discuss some important artifacts that can provide us with insights into user behavior and help create a comprehensive snapshot of how users navigate the digital landscape.

## How Can Registry Data Be Used for User Behavior Forensics?

From a forensic standpoint, the registry can provide valuable insights into a user's behavior and overall system usage. By analyzing registry data, forensic investigators can reconstruct a timeline of events, identify patterns of use, and uncover important details related to system activities, user interactions, and application usage. Much like the correlation of evidence in forensic profiling, the registry speaks volumes about the who, what, and when of digital activities.

Let's take an example of an activity.

- `Activity`: User connects or disconnects a USB device from the system.
- `Potential Threat`: Data exfiltration, unauthorized file transfers.
- `Forensic Artifact`: USB device history in the Windows Registry, i.e., `SYSTEM\CurrentControlSet\Enum\USBSTOR` and `SYSTEM\CurrentControlSet\Control\DeviceClasses`.
  - `Registry Forensics`: The `USBSTOR` registry key stores details of connected USB devices, such as the `device ID` and `serial number`.
  - `Correlation`: Evidence of unauthorized device usage that might indicate data theft or malware spreading via USB drives can be revealed by analyzing these registry keys and correlating them with other forensic artifacts.

The image below shows a breakdown of various user activities and the corresponding artifacts that provide evidence of those actions. Each activity is associated with a potential threat, such as data exfiltration or suspicious actions, and is mapped to the forensic artifact that can uncover or reveal these behaviors.

![image2](https://academy.hackthebox.com/storage/modules/248/ubf-intro.png)

This module focuses on the following artifacts to identify and analyze user actions on Windows-based computers:

- `Shellbags`: Shellbags are registry keys that store information about Windows Explorer folder views, which can help reconstruct a user's folder browsing history. These artifacts are found in `NTUSER.DAT` and `USRCLASS.DAT` and can be examined using tools like Shellbags Explorer.

- `UserAssist`: UserAssist entries record the execution history of programs by a user. They are stored under `HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\UserAssist` and are ROT-13 encoded. These entries can reveal which applications were recently used.

- `Search History in File Explorer`: Search history in File Explorer can be found under `HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\WordWheelQuery`. This registry key stores recent search terms, providing insight into what the user was searching for.

- `JumpLists`: JumpLists are used by Windows to track recently accessed files and applications. They are stored in AutomaticDestinations and CustomDestinations and can be analyzed with tools like JLECmd.

- `LNK Files`: LNK (shortcut) files provide metadata about the files they link to, such as the original file path, access times, and more. LNK files can be parsed with tools like LECmd.

- `Run MRU Forensics`: The Run MRU (Most Recently Used) list records the commands executed via the Run dialog box. This information is stored in the `HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\RunMRU` key.

- `Recent Docs`: The RecentDocs registry key tracks the files and folders recently accessed by the user. It is located under `HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\RecentDocs`.

- `Open/Save Dialog MRUs`: These entries track files and folders accessed through open/save dialog boxes. They are stored in the `HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\ComDlg32\OpenSavePidlMRU` key.

- `TypedPaths`: TypedPaths stores the paths typed into the Windows Explorer address bar, found in `HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\TypedPaths` key.

- `MS Office Accessed Files (File MRU)`: Microsoft Office maintains a list of recently accessed files in `HKEY_CURRENT_USER\Software\Microsoft\Office\16.0\<Application>\File MRU`.

- `User's Sticky Notes Forensics`: Sticky notes created by the user are stored in a SQLite database file called `plum.sqlite`. Analyzing this file can provide insights into the user's notes and reminders.

- `Command-line History Forensics`: The history of commands typed into command-line interfaces, such as PowerShell, is recorded. PowerShell command history can be found in a file named `ConsoleHost_history.txt`.

- `User's Clipboard Data`: Clipboard data can be volatile but might be cached by certain applications. Clipboard forensics involves analyzing this transient data to uncover what was copied or cut by the user.

- `Saved SSH Keys and Server Information (PuTTY)`: PuTTY, a popular SSH client, stores saved session information and SSH host keys in the registry under `HKEY_CURRENT_USER\Software\SimonTatham\PuTTY\SshHostKeys`.

- `User Activity Timeline Analysis`: Windows 10 and later versions have a feature called Activity History, which logs user activities such as app usage and file access. This data is stored in `ActivityCache.db` and can be parsed to understand user actions over time.

- `Terminal Server History (tsclient)`: The Terminal Server Client (RDP) history stores information about remote desktop connections under `HKEY_CURRENT_USER\Software\Microsoft\Terminal Server Client\Default`.

- `Adobe Recent Files`: Adobe applications, like Acrobat Reader, keep a list of recently accessed files in the registry. For Acrobat DC, this is found under `HKEY_CURRENT_USER\Software\Adobe\Adobe Acrobat\DC\AVGeneral\cRecentFiles`.

- `Archive History`: Tools like WinZip maintain a history of recently accessed archives in the registry, found under `HKEY_CURRENT_USER\Software\WinZip\WinZip\mru\archives`.

- `USB Devices`: Information about connected USB devices is stored in the registry and can be found under `HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Enum\USB`.


In the upcoming sections, we'll understand these registry hives, and analyze these artifacts, which helps investigators to reconstruct user activity and detect suspicious behavior.


# Shellbags

Let's navigate to the bottom of this section and click on "Click here to spawn the target system!". Then, let's RDP into the Target IP using the provided credentials. The vast majority of the actions and commands covered from this point up to end of this section can be replicated inside the target, offering a more comprehensive grasp of the topics presented.

* * *

## Introduction

Shellbags are a forensically significant artifact in Windows operating systems. They are part of the Windows Registry and play a crucial role in tracking user navigation patterns within the file system. Essentially, shellbags record information related to user preferences while browsing different locations, including the size and position of folders and files. Microsoft Windows keeps track of the view preferences for folders and the Desktop. This allows the system to recall a folder’s location, view settings, and the positions of items the next time the folder or Desktop is accessed. This information can be invaluable for digital forensic investigations, as it provides insights into a user's interactions with file system locations, helping forensic analysts understand which files and folders have been accessed and when.

* * *

## Location of Shellbags

Within the target (VM), you can locate the evidence and tools at the following paths:

- **KAPE Output location**: `C:\Tools\DFIR-Data\evidence\001.shellbags_data`
- **UsrClass.dat file locations**: `C:\Tools\DFIR-Data\evidence\001.shellbags_data\D\Users\John Doe\AppData\Local\Microsoft\Windows`
- **Shellbag Explorer location**: `C:\Tools\DFIR-Data\Tools\EZ-Tools\net6\ShellBagsExplorer`
- **Registry Explorer location**: `C:\Tools\DFIR-Data\Tools\EZ-Tools\net6\RegistryExplorer`
- **RegRipper**: `C:\Tools\DFIR-Data\Tools\RegRipper\rip.exe`

If you're not able to view the `UsrClass.dat` file, make sure that the hidden files are shown in the file explorer.

In Windows OS, shellbags are stored in the Windows Registry, specifically in the `UsrClass.dat` and `NTUSER.dat` files within a user's profile directory.

The file `NTUSER.dat` is specific to each user, and is loaded when that user logs into the system. This file can be found within each user's profile directory.

- `%UserProfile%\NTUSER.dat`

And the `UsrClass.dat` file is usually located in the below location:

- `%UserProfile%\AppData\Local\Microsoft\Windows\UsrClass.dat`

The specific locations for shellbags within the Registry are:

- `HKEY_CURRENT_USER\Software\Microsoft\Windows\Shell\Bags`
- `HKEY_CURRENT_USER\Software\Microsoft\Windows\Shell\BagMRU`
- `HKEY_CURRENT_USER\Local Settings\Software\Microsoft\Windows\Shell\BagMRU`

Information related to shellbags in the .dat file includes data on folder and file navigation, window size, and position settings. Most of this information is found in the `UsrClass.dat` hive.

These hives contain data in two components:

- Bags
- BagMRU

![shellbags-reg](https://academy.hackthebox.com/storage/modules/248/shellbags-reg.png)

* * *

### Bags (Shellbags)

`Bags` is a term often used to refer to shellbags, a feature of the Windows Registry. Shellbags store data about the size and position of folder and file windows, the timestamps of folder access, and other information related to the user's interactions with the file system.

### BagMRU

`BagMRU` is a component of the Windows Registry that tracks the most recently used (MRU) shellbags. It maintains a list of the shellbags that the user has interacted with recently. `BagMRU` records the order in which shellbags were accessed or viewed by the user. This information can be used to reconstruct a user's navigation history within the file system.

Let's analyze the shellbags and see what valuable information can be extracted from the hives.

* * *

## Analysis of Shellbags

We can use Eric Zimmerman's tool called `Shellbags Explorer`, which is designed for the forensic analysis of shellbags. It allows digital forensic investigators to examine and interpret the information stored in shellbags to reconstruct a user's file system navigation history.

Let's open Shellbags Explorer from the EZ-Tools path as mentioned at the beginning of this section. A prompt for an email address will appear. Click the close button to skip it. Then skip the `options` prompt by clicking the close icon. After this, we are presented with the main program window where we can load the registry hive. The GIF below shows how we skip these prompts and open offline registry hive.

![sb-usrclass](https://academy.hackthebox.com/storage/modules/248/sbags-skip.gif)

Let's browse to the `UsrClass.dat` file using the path mentioned at the beginning of this section.

`C:\Tools\DFIR-Data\evidence\001.shellbags_data\D\Users\John Doe\AppData\Local\Microsoft\Windows`

![sb-usrclass](https://academy.hackthebox.com/storage/modules/248/sb-usrclass-1_.png)

The file is parsed successfully, and the shellbags are found.

![sb-parsed](https://academy.hackthebox.com/storage/modules/248/sb-parsed-1_.png)

In the screenshot below, we can see that some interesting files were accessed by the user.

![sb-files](https://academy.hackthebox.com/storage/modules/248/sb-files_.png)

This can also help reveal any network-related activity. For example, the user has accessed a directory on a network path.

![sb-network](https://academy.hackthebox.com/storage/modules/248/sb-network_.png)

On the right side of Shellbags Explorer, the `Has Explored` checkbox indicates whether the directory was explored by the user.

![sb-explored](https://academy.hackthebox.com/storage/modules/248/sb-explored.png)

### Shellbags analysis using RegRipper

[RegRipper](https://github.com/keydet89/RegRipper3.0) is a tool used in digital forensics for extracting and analyzing data from Windows registry hives. It consists of a collection of Perl scripts (known as plugins) that target specific registry keys and values, allowing for the automated extraction and reporting of important forensic artifacts. The RegRipper tool includes a plugin named `shellbags`, which is specifically designed to analyze ShellBags data. This plugin extracts and interprets the data from the respective registry entries and prints the output in the console.

On the module's target workstation, we can locate RegRipper in the following directory:

`C:\Tools\DFIR-Data\Tools\RegRipper`

Then we'll run RegRipper with the `shellbags` plugin, using the following options:

- `-r`: This flag specifies the registry hive file to be analyzed. In this case, `UsrClass.dat` is the registry hive file we are targeting, which typically stores user-specific settings such as file associations, Windows Explorer view settings, and ShellBags (which track folder views and directory structures the user has interacted with).

- `-p`: It specifies the plugin to be used for the analysis. RegRipper comes with various plugins to parse specific parts of registry hives. In this case, `shellbags` is the plugin that extracts and parses ShellBags data from the specified `UsrClass.dat` file.


The output of the command is shown below:

```cmd-session
C:\Tools\DFIR-Data\Tools\RegRipper\rip.exe -r "C:\Tools\DFIR-Data\evidence\001.shellbags_data\D\Users\John Doe\AppData\Local\Microsoft\Windows\UsrClass.dat" -p shellbags

Launching shellbags v.20200428
shellbags v.20200428
(USRCLASS.DAT) Shell/BagMRU traversal in Win7+ USRCLASS.DAT hives

MRU Time             |Modified             | Accessed             | Created              | Zip_Subfolder        | MFT File Ref |Resource
------------         |------------         | ------------         | ------------         | ------------         | ------------ |------------
                     |                     |                      |                      |                      |              |My Games [Desktop\0\]
                     |                     |                      |                      |                      |              |My Computer [Desktop\1\]
                     |                     |                      |                      |                      |              |My Computer\C:\ [Desktop\1\0\]
2023-11-11 15:47:36  |2023-08-28 09:41:04  | 2023-08-28 09:41:04  | 2019-12-07 09:03:46  |                      | 569/1        |My Computer\C:\Windows [Desktop\1\0\0\]
2023-11-11 15:47:36  |2023-08-28 13:26:44  | 2023-09-07 08:15:52  | 2019-12-07 09:03:46  |                      | 2291/1       |My Computer\C:\Windows\System32 [Desktop\1\0\0\0\]
                     |2023-08-28 12:59:14  | 2023-08-28 12:59:14  | 2019-12-07 09:14:54  |                      | 571/1        |My Computer\C:\Windows\appcompat [Desktop\1\0\0\1\]
2023-09-11 08:02:18  |2023-08-28 09:41:04  | 2023-09-11 08:01:24  | 2019-12-07 09:14:54  |                      | 574/1        |My Computer\C:\Windows\appcompat\Programs [Desktop\1\0\0\1\0\]
                     |2023-09-07 08:01:40  | 2023-09-07 08:01:40  | 2023-09-07 08:01:40  |                      | 92487/2      |My Computer\C:\Temp [Desktop\1\0\1\]
2023-09-10 13:23:33  |2023-09-10 13:23:32  | 2023-09-10 13:23:32  | 2023-09-10 13:23:32  |                      | 98078/1      |My Computer\C:\Temp\discord [Desktop\1\0\1\0\]
                     |2023-09-10 13:22:50  | 2023-09-10 13:22:50  | 2023-09-10 13:22:50  |                      | 90737/2      |My Computer\C:\Tools [Desktop\1\0\2\]
2023-11-07 11:20:13  |2023-09-10 13:22:58  | 2023-09-10 13:22:58  | 2023-09-10 13:22:58  |                      | 95892/1      |My Computer\C:\Tools\API-Monitor [Desktop\1\0\2\0\]
                     |2023-11-04 10:45:28  | 2023-11-04 10:45:28  | 2023-11-04 10:45:28  |                      | 90641/3      |My Computer\C:\Tools\ShellBagsExplorer [Desktop\1\0\2\1\]
                     |2023-08-28 09:41:18  | 2023-11-04 10:15:00  | 2019-12-07 09:03:46  |                      | 512/1        |My Computer\C:\Users [Desktop\1\0\3\]
2023-11-04 10:25:56  |2023-08-28 09:37:24  | 2023-11-04 10:15:00  | 2023-08-28 09:36:56  |                      | 26382/2      |My Computer\C:\Users\John Doe [Desktop\1\0\3\0\]
                     |2023-11-11 14:41:56  | 2023-11-11 14:41:56  | 2023-11-11 14:41:56  |                      | 90654/4      |My Computer\C:\HTBFS01 [Desktop\1\0\4\]
                     |2023-11-11 14:42:20  | 2023-11-11 14:42:20  | 2023-11-11 14:42:20  |                      | 27272/41     |My Computer\C:\HTBFS01\IT [Desktop\1\0\4\0\]
2023-11-11 14:42:56  |2023-11-11 14:42:40  | 2023-11-11 14:42:40  | 2023-11-11 14:42:40  |                      | 90695/9      |My Computer\C:\HTBFS01\Backup [Desktop\1\0\4\1\]
2023-11-11 14:43:01  |2023-11-11 14:42:58  | 2023-11-11 14:42:58  | 2023-11-11 14:42:58  |                      | 90698/9      |My Computer\C:\HTBFS01\Backup\CSV [Desktop\1\0\4\1\0\]
2023-11-11 14:43:08  |2023-11-11 14:43:06  | 2023-11-11 14:43:06  | 2023-11-11 14:43:06  |                      | 90706/10     |My Computer\C:\HTBFS01\Backup\CSV\Logs [Desktop\1\0\4\1\0\0\]

...SNIP...

```

The above output provides useful information about the user's interaction with different folders on the system, network places, and Control Panel items.

### Export Shellbags Data using SBECmd

To export all shellbag data into a CSV file, we can use `SBECmd.exe` which is command-line version of the shellbag explorer tool by Eric Zimmerman. It requires below options:

- `-d <d>`: Directory to look for registry hives. This or -l is required
- `--csv <csv>`: Directory to save CSV formatted results to.

To extract shellbags data from live registry, `-l` is used (Requires Administrator rights). This or -d is required.

```cmd-session

C:\Tools\DFIR-Data\Tools\EZ-Tools\net6\SBECmd.exe -d "C:\Tools\DFIR-Data\evidence\001.shellbags_data\D\Users\John Doe\AppData\Local\Microsoft\Windows" --csv c:\temp

...SNIP...

Total ShellBags found: 81

Totals by bag type

Root folder: GUID: 10
Directory: 50
Drive letter: 2
GUID: Control panel: 4
Variable: Users property view: 4
Control Panel Category: 3
Network location: 5
URI: 2
Variable: FTP URI: 1

Finished processing C:\Tools\DFIR-Data\evidence\001.shellbags_data\D\Users\John Doe\AppData\Local\Microsoft\Windows\UsrClass.dat

Exported to: C:\temp\John Doe_UsrClass.csv

---------------------------------------------------------------------

Processing complete!

Processed 1 file in 0.36 seconds!
Total ShellBags found: 81

```

* * *

## Practical scenarios

The sections `My Network Places` and `Internet Explorer` inside the shellbag data can contain some interesting artifacts such as FTP site browsing.

### Scenario 1

The image below shows an interesting example where a user browsed to the Sysinternals Suite Live [service](https://learn.microsoft.com/en-us/sysinternals/#sysinternals-live) directly from Windows Explorer, which is captured in the shellbags.

![sb-scenario1](https://academy.hackthebox.com/storage/modules/248/sb-scenario1_.png)

### Scenario 2

The image below shows an example where the user browsed an FTP site, which is captured in the shellbags as follows.

![sb-scenario2](https://academy.hackthebox.com/storage/modules/248/sb-scenario2_.png)

If the user has browsed some Control Panel items, this will also be shown here. For example, in this scenario, the user browsed the "Network and Internet" option of the Control Panel.

![sb-cpl](https://academy.hackthebox.com/storage/modules/248/sb-cpl_.png)

* * *

## Use in Investigation

In cybersecurity investigations, forensic analysis of Shellbags plays a critical role in examining file system access, tracking user behavior, and supporting incident response efforts. By analyzing Shellbags, investigators can gain valuable insights into a user's actions on an endpoint and within the broader environment, offering essential evidence to reconstruct file access history, identify patterns of activity, and detect potentially malicious behavior. Shellbags track folders accessed by the user, even if they were deleted. If a user accessed hidden folders containing sensitive files, Shellbags may provide evidence.

The examples below show the use of shellbag data in investigations:

- `Validate Data Exfiltration`: Identify suspicious folders the user navigated before a USB drive was connected.
- `Hidden Activity Detection`: If files or folders were deleted, Shellbags still retain the names, showing prior existence.
- `Correlating with other evidence`: Shellbag data can be combined with other digital artifacts (e.g., network logs, browser history) to create a more complete picture of an incident.

* * *


# User Assist

UserAssist is another significant forensic artifact that tracks and records information about a user's interactions with various programs and applications. The primary purpose of UserAssist is to maintain a history of program executions, providing insights into the programs that have been run by a user.

* * *

## Location of UserAssist

UserAssist information is stored in specific registry subkeys located at the following registry path: `HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\UserAssist\{GUID}`.

![userassist-loc](https://academy.hackthebox.com/storage/modules/248/userassist-loc.png)

From a forensic perspective, our focus is on the following two registry keys, identified by the GUIDs listed below:

- `CEBFF5CD-ACE2-4F4F-9178-9926F41749EA`
- `F4E57C4B-2036-45F0-A9AB-443BCFE33D9F`

Let's discuss what these keys contain.

* * *

**CEBFF5CD-ACE2-4F4F-9178-9926F41749EA**

This GUID contains information about the applications, executables, files, etc., that are accessed.

![guid1](https://academy.hackthebox.com/storage/modules/248/guid1.png)

**F4E57C4B-2036-45F0-A9AB-443BCFE33D9F**

This GUID contains information about the shortcuts ( `.lnk`) that are used to start applications.

![guid2](https://academy.hackthebox.com/storage/modules/248/guid2.png)

To learn more about the other UserAssist GUIDs, we can refer to this [document](https://winreg-kb.readthedocs.io/en/latest/sources/explorer-keys/User-assist.html).

Both of the previously mentioned registry GUIDs contain a subkey called **Count**, which consists of the UserAssist-accessed applications or link entries. However, the values contained by these keys are obfuscated using ROT-13 of character values in the ASCII `[A-Za-z]` range.

* * *

## Deciphering the UserAssist GUIDs

The `{GUID}` portion in the registry subkey represents a globally unique identifier. These GUIDs are used to obscure the names of the programs, making it challenging for users to identify the specific programs recorded. Deciphering these GUIDs is a common task in digital forensics.

Let's open an entry from `CEBFF5CD-ACE2-4F4F-9178-9926F41749EA` and see how the entries store information.

![userassist-reg](https://academy.hackthebox.com/storage/modules/248/userassist-reg.png)

We are using the following key as an example.

```reg
{1NP14R77-02R7-4R5Q-O744-2RO1NR5198O7}\JvaqbjfCbjreFuryy\i1.0\cbjrefuryy.rkr

```

This key is obfuscated using ROT-13. So let's open [CyberChef](https://gchq.github.io/CyberChef/) to deobfuscate it and see the actual value.

![ua-cyberchef](https://academy.hackthebox.com/storage/modules/248/ua-cyberchef.png)

The deobfuscated key contains the following information, which indicates that the `powershell.exe` application was accessed by the user:

```reg
{1AC14E77-02E7-4E5D-B744-2EB1AE5198B7}\WindowsPowerShell\v1.0\powershell.exe

```

In the above value, the first part is a known folder GUID. Microsoft has documented Known Folder GUIDs for File Dialog Custom Places [here](https://learn.microsoft.com/en-us/dotnet/desktop/winforms/controls/known-folder-guids-for-file-dialog-custom-places?view=netframeworkdesktop-4.8).

![ua-knownguid](https://academy.hackthebox.com/storage/modules/248/ua-knownguid.png)

As we can see, this GUID refers to the SYSTEM.

* * *

## Analysis of UserAssist using RegRipper

Let's navigate to the bottom of this section and click on "Click here to spawn the target system!". Then, let's RDP into the Target IP using the provided credentials. The vast majority of the actions and commands covered from this point up to the end of this section can be replicated inside the target, offering a more comprehensive grasp of the topics presented.

Within the target (VM), you can locate the evidence and tools at the following paths:

- **NTUSER.DAT file location**: `C:\Tools\DFIR-Data\evidence\002.userassist`
- **Registry Explorer location**: `C:\Tools\DFIR-Data\Tools\EZ-Tools\net6\RegistryExplorer`
- **RegRipper location**: `C:\Tools\DFIR-Data\Tools\RegRipper`

* * *

Let's list all plugins in RegRipper using the `-l` option. Then, we can add a filter to check which plugins can extract information related to `UserAssist`.

```cmd-session

C:\Tools\DFIR-Data\Tools\RegRipper\rip.exe -l | Select-String UserAssist

65. disableuserassist v.20230710 [NTUSER.DAT]
   - Get Start_TrackEnabled and Start_TrackProgs values which confirm if UserAssist was disabled.
234. userassist v.20170204 [NTUSER.DAT]
   - Displays contents of UserAssist subkeys
235. userassist_tln v.20180710 [NTUSER.DAT]
   - Displays contents of UserAssist subkeys in TLN format

```

From the above output, we can see that there are two plugins that can provide details about UserAssist. One is `userassist`, which displays the contents of UserAssist subkeys, and the other is `userassist_tln`, which displays the contents of UserAssist subkeys in a timeline format.

Let's use the `userassist_tln` plugin. The command takes two arguments. The first is the `-r` option, which requires a path to a registry hive, i.e., `NTUSER.DAT`. The second is the `-p` option, which requires the plugin name, i.e., `userassist_tln`.

Once we run this plugin, we can see the output below:

```cmd-session

C:\Tools\DFIR-Data\Tools\RegRipper\rip.exe -r C:\Tools\DFIR-Data\evidence\002.userassist\NTUSER.DAT -p userassist_tln

Launching userassist_tln v.20180710
1699790491|REG|||[Program Execution] UserAssist - Microsoft.InternetExplorer.Default (2)
1699717698|REG|||[Program Execution] UserAssist - {1AC14E77-02E7-4E5D-B744-2EB1AE5198B7}\cmd.exe (13)
1699717582|REG|||[Program Execution] UserAssist - {F38BF404-1D43-42F2-9305-67DE0B28FC23}\explorer.exe (1)
1699714441|REG|||[Program Execution] UserAssist - {6D809377-6AF0-444B-8957-A3773F02200E}\KeePass Password Safe 2\KeePass.exe (1)

...SNIP...

```

This provides us with information about which applications and shortcuts were accessed, as shown in the screenshot below:

![ua-rip](https://academy.hackthebox.com/storage/modules/248/userassist-reg-2_.png)

This also provides the run count, which shows the number of times an application ran.

For example, the entry below, which is part of the output above, indicates that `malware.exe` was executed 2 times.

```text
1699714298|REG|||[Program Execution] UserAssist - C:\Users\John Doe\Downloads\malware.exe (2)

```

* * *

## Analysis of UserAssist using Registry Explorer

In Registry Explorer, one of the tools from Eric Zimmerman, we can find the deobfuscated values directly if we open the registry hive. Open Registry Explorer from the EZ-Tools path:
`C:\Tools\DFIR-Data\Tools\EZ-Tools\net6\RegistryExplorer`.

Let's browse to the `NTUSER.DAT` file using the path mentioned at the beginning of this section.

`C:\Tools\DFIR-Data\evidence\002.userassist\NTUSER.DAT`

After the file is parsed, expand `ROOT` and browse to the location `Software\Microsoft\Windows\CurrentVersion\Explorer\UserAssist`.

![ua-regexp](https://academy.hackthebox.com/storage/modules/248/ua-regexp.png)

It also shows the number of times an application ran and its last execution time.

We can also navigate to the `UserAssist` bookmark in the **Available bookmarks** section to find the same information.

![ua-regexp1](https://academy.hackthebox.com/storage/modules/248/ua-regexp11_.png)


# Search History in File explorer

Sometimes the search queries performed by a user can provide valuable insights into their search behavior, revealing the search terms and queries they have used. Forensic analysts can access and examine this data to identify keywords, search patterns, and user activities related to search operations. This information can be useful in investigations involving file searches, information retrieval, and user behavior analysis. Windows operating systems store File Explorer's search history information in a registry key known as `WordWheelQuery`.

The screenshot below shows an example of search queries performed by a user in Windows File Explorer.

![searchitems](https://academy.hackthebox.com/storage/modules/248/searchitems-1_.png)

The `WordWheelQuery` data is found in the following registry path:

```reg
Computer\HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\WordWheelQuery

```

The search query items are stored in binary format at this location.

![search-reg](https://academy.hackthebox.com/storage/modules/248/search-reg_.png)

The entry information in binary format can be verified, as shown in the screenshot below:

![search-value](https://academy.hackthebox.com/storage/modules/248/search-value_.png)

We can use Registry Explorer or RegRipper to get the parsed details.

* * *

## Exploring search items using Registry Explorer

Let's navigate to the bottom of this section and click on "Click here to spawn the target system!". Then, let's RDP into the Target IP using the provided credentials. The vast majority of the actions and commands covered from this point up to end of this section can be replicated inside the target, offering a more comprehensive grasp of the topics presented.

Within the target (VM), you can locate the evidence and tools at the following paths:

- **Registry Explorer location**: `C:\Tools\DFIR-Data\Tools\EZ-Tools\net6\RegistryExplorer`
- **RegRipper location**: `C:\Tools\DFIR-Data\Tools\RegRipper`
- **NTUSER.DAT file location**: `C:\Tools\DFIR-Data\evidence\003.searchhistory`

* * *

Browse to the location of the `NTUSER.DAT` file from the path as mentioned in the beginning of this section.

`C:\Tools\DFIR-Data\evidence\003.searchhistory\NTUSER.DAT`

In the Registry Explorer interface, expand ROOT and navigate to the `WordWheelQuery` key, which is located under the path below:

```reg
Software\Microsoft\Windows\CurrentVersion\Explorer\WordWheelQuery

```

* * *

### WordWheelQuery key and search keywords

The screenshot below shows the `WordWheelQuery` key and the search items. We can expand it to see the values stored within. Each value represents a search item, which may include search queries or terms.

![wordwheelquery](https://academy.hackthebox.com/storage/modules/248/wordwheelquery_.png)

Then we can analyze the search history to identify relevant keywords, search patterns, and user activities. We can document the findings, as this information may be significant in our forensic investigation.

Note: We can only see the timestamp for the last entry's write time, not for other entries.

* * *

## Exploring search items using RegRipper

In the list of RegRipper plugins, we can check which plugins can extract information related to `WordWheelQuery`. We can see that there is `wordwheelquery` plugin which requires the `NTUSER.DAT` registry hive.

```cmd-session
C:\> C:\Tools\DFIR-Data\Tools\RegRipper\rip.exe -l | findstr wordwheelquery

248. wordwheelquery v.20200823 [NTUSER.DAT]
249. wordwheelquery_tln v.20200824 [NTUSER.DAT]

```

Run the `wordwheelquery` plugin on the NTUSER.DAT file.

```cmd-session
C:> C:\Tools\DFIR-Data\Tools\RegRipper\rip.exe -r C:\Tools\DFIR-Data\evidence\003.searchhistory\NTUSER.DAT -p wordwheelquery

Launching wordwheelquery v.20200823
wordwheelquery v.20200823
(NTUSER.DAT) Gets contents of user's WordWheelQuery key

Software\Microsoft\Windows\CurrentVersion\Explorer\WordWheelQuery
LastWrite Time 2023-11-12 19:13:35Z

Searches listed in MRUListEx order

10   interesting_search
9    key.ppk
8    *azure*
7    *aws*
6    *.KDBX
5    *secret*.doc
4    *salary*.pdf
3    *password*.txt
2    password*.txt
1    {REDACTED}.xlsx
0    salary*.xlsx

```

As shown in the above output, RegRipper generates console output that displays the extracted search history items. We can review these entries to reconstruct a user’s search activities. This reveals if the user was looking for specific documents or system files.


# JumpLists

## Introduction

Jump Lists are a user interface feature introduced in Windows 7 and are present in later Windows versions. They are designed to make it easier for users to access recently opened files or perform common tasks associated with specific applications.

For example, the screenshot below shows the frequently accessed directories by the application **File Explorer**. These entries are part of the Jump Lists.

![jumplist-recent](https://academy.hackthebox.com/storage/modules/248/jumplist-recent.png)

Jump Lists store information about a user's interactions with files and applications, making them valuable in digital forensics. They can help investigators understand a user's recent activities and may reveal evidence of file access or the execution of certain tasks. Typically, these consist of recent items and tasks/actions associated with the application.

The information related to the items displayed in Jump Lists is stored in two directories called `AutomaticDestinations` and `CustomDestinations`.

### AutomaticDestinations

The "AutomaticDestinations" folder contains information about the recent items that are automatically populated by the operating system based on the user's interactions with applications. It includes shortcuts to recently used files, folders, and tasks. The operating system dynamically manages the content of this folder based on the user's activities.

The directory is located within the user's profile directory at the following path:

```path
%APPDATA%\Microsoft\Windows\Recent\AutomaticDestinations

```

On the forensic workstation, you can locate these files in the evidence data at the path mentioned below:

```path
C:\Tools\DFIR-Data\evidence\004.jumplists\KAPE_Output\D\Users\John Doe\AppData\Roaming\Microsoft\Windows\Recent\AutomaticDestinations

```

### CustomDestinations

The "CustomDestinations" folder, on the other hand, contains user-pinned items in Jump Lists. Users have the ability to pin specific files, folders, or tasks to an application's Jump List for quick access. The "CustomDestinations" folder stores information about these user-pinned items.

The directory is located within the user's profile directory at the following path:

```path
%APPDATA%\Microsoft\Windows\Recent\CustomDestinations

```

On the forensic workstation, you can locate these files in the evidence data at the path mentioned below:

```path
C:\Tools\DFIR-Data\evidence\004.jumplists\KAPE_Output\D\Users\John Doe\AppData\Roaming\Microsoft\Windows\Recent\CustomDestinations

```

The screenshot below shows these destination folders on the module's target system.

![jumplist-dest](https://academy.hackthebox.com/storage/modules/248/jumplist-dest_.png)

* * *

## Analysis of Jump Lists data

[KAPE](https://www.kroll.com/en/services/cyber-risk/incident-response-litigation-support/kroll-artifact-parser-extractor-kape) has an option to extract Jump Lists information from a system. We have already exported the Jump Lists information from a compromised target using KAPE and stored it on the module workstation.

In the output from KAPE, the `jumplists` data is stored in the following location on the forensic workstation (Lab VM):

```path
C:\Tools\DFIR-Data\evidence\004.jumplists\KAPE_Output\D\Users\John Doe\AppData\Roaming\Microsoft\Windows\Recent

```

![jl-kape](https://academy.hackthebox.com/storage/modules/248/jl-kape.png)

On the forensic workstation, you can locate these files in the evidence data under KAPE\_OUTPUT at the path mentioned below:

`C:\Tools\DFIR-Data\evidence\004.jumplists\KAPE_Output`

Let's navigate to the bottom of this section and click on "Click here to spawn the target system!". Then, let's RDP into the Target IP using the provided credentials. The vast majority of the actions and commands covered from this point up to end of this section can be replicated inside the target, offering a more comprehensive grasp of the topics presented.

Within the target (VM), you can locate the evidence and tools at the following paths:

- **KAPE Output location**: `C:\Tools\DFIR-Data\evidence\004.jumplists\KAPE_Output`
- **Jump List Folder**: `C:\Tools\DFIR-Data\evidence\004.jumplists\KAPE_Output\D\Users\John Doe\AppData\Roaming\Microsoft\Windows\Recent`
- **JumpList Explorer location**: `C:\Tools\DFIR-Data\Tools\EZ-Tools\net6\JumpListExplorer`
- **Timeline Explorer location**: `C:\Tools\DFIR-Data\Tools\EZ-Tools\net6\TimelineExplorer`
- **RegRipper location**: `C:\Tools\DFIR-Data\Tools\RegRipper`
- **NTUSER.DAT file location**: `C:\Tools\DFIR-Data\evidence\004.jumplists\NTUSER.DAT`
- **JLECmd Location**: `C:\Tools\DFIR-Data\Tools\EZ-Tools\net6`

If you're not able to view the `NTUSER.DAT` file, make sure that the hidden files are shown in the File Explorer.

* * *

### Parsing Jump list data using JLECMD

JLECMD is a command-line tool that is part of the Eric Zimmerman's [tools](https://ericzimmerman.github.io/#!index.md). It is used to parse and analyze Jump List data from Windows registry hives. JLECMD can be employed to extract information about Jump List entries, such as filenames, paths, and timestamps.

The command to convert the Jump List data into CSV format is as follows:

```cmd-session
C:> C:\Tools\DFIR-Data\Tools\EZ-Tools\net6\JLECmd.exe -d "C:\Tools\DFIR-Data\evidence\004.jumplists\KAPE_Output\D\Users\John Doe\AppData\Roaming\Microsoft\Windows\Recent" --csv "C:\Tools\DFIR-Data\evidence\004.jumplists\JLE csv"

```

Here, `JLECmd.exe` is the executable for the JLECmd tool used for analyzing Jump Lists. We have used the options as explained below:

- `-d`: This option specifies the directory where the tool will look for Jump List files. In this case, it's targeting the **Recent** folder from the specified path. This folder contains shortcuts to recently accessed files by the user.

- `--csv`: This flag indicates that you want to output the results to a CSV file. The path specifies the directory or filename where the CSV output should be stored.


JLECmd will write its parsed results in CSV format, making it easier to analyze the data in Excel or another spreadsheet application. This process exports two CSV files, as mentioned below.

- AutomaticDestinations.csv
- CustomDestinations.csv

This command will parse the Jump List files into CSV format. In the screenshot below, we can see that `JLECmd.exe` displays the absolute path for the files that are present in the Jump Lists.

![jle-cmd](https://academy.hackthebox.com/storage/modules/248/jle-cmd.png)

In this output, we can identify patterns of user behavior, such as files that have been opened frequently or at suspicious times.

### Analysis using Timeline Explorer

This information is exported into two CSV files as discussed earlier (i.e., `AutomaticDestinations.csv` and `CustomDestinations.csv`). We can import and view the CSV files in the Timeline Explorer for analysis. Open Timeline Explorer from the below path on the forensic workstation:

`C:\Tools\DFIR-Data\Tools\EZ-Tools\net6\TimelineExplorer`

We'll import the CSV files from the location `C:\Tools\DFIR-Data\evidence\004.jumplists\JLE csv` into Timeline Explorer, which can display the information in an organized manner. We can also add filters, as shown in the screenshot below:
The screenshot below shows the documents accessed using the application Wordpad.

![jl-docx](https://academy.hackthebox.com/storage/modules/248/jl-docx.png)

Similarly, we can add filters to the timeline data based on specific criteria, such as date and time ranges, App ID, path, etc.

* * *

### Analysis using JumpList Explorer

JumpList Explorer is another tool from Eric Zimmerman used for analyzing Jump Lists. It provides a graphical user interface for parsing and examining Jump List data. This tool allows forensic examiners to explore Jump List entries, filter and search for specific files or tasks, and export the data for further analysis.

Let's open JumpList Explorer from the path below on the forensic workstation:

```path
C:\Tools\DFIR-Data\Tools\EZ-Tools\net6\JumpListExplorer

```

Once inside JumpList Explorer, click on **File** at the top left and choose **Open**. Then, browse to the `AutomaticDestinations` folder, select a .automaticDestinations-ms file, and click Open to load it into JumpList Explorer. We can import all the jumplist data from the location into the JumpList Explorer, as shown in the screenshot below.

![jl-exp](https://academy.hackthebox.com/storage/modules/248/jumplist-expl_.png)

On the module's target system, we can browse to the path mentioned below for `AutomaticDestinations` folder:

```path
C:\Tools\DFIR-Data\evidence\004.jumplists\KAPE_Output\D\Users\John Doe\AppData\Roaming\Microsoft\Windows\Recent\AutomaticDestinations

```

JumpList Explorer can show the information in an organized manner, as shown in the screenshot below:

![jl-exp](https://academy.hackthebox.com/storage/modules/248/jl-exp.png)

This directory contains the Jump List files ending with `-ms` extensions. Each file in this folder corresponds to a specific application’s Jump List. When the files are loaded into JumpList Explorer, it will parse the Jump List and display its contents in an organized table or tree view.

- `File Name`: The name of the file that was accessed.
- `Full Path`: The full path to the file or folder on the system.
- `Timestamps`: Created, modified, and accessed timestamps for each file or folder.
- `Application ID (AppID)`: The identifier for the application that generated the Jump List.
- `Usage Count`: The number of times the file or folder was opened via the Jump List.

Scroll through the Jump List entries to identify patterns of user behavior, such as files that have been opened frequently or at suspicious times.

### JumpList analysis using RegRipper

[RegRipper](https://github.com/keydet89/RegRipper3.0) also includes a plugin called `jumplistdata`, specifically designed to analyze the contents of a user's JumpListData key. The plugin looks for Jump List files stored in the user's profile directory and parses the entries within these files, extracting information about the accessed files and applications. It also extracts timestamps associated with each entry, providing a timeline of user activity.

RegRipper's `jumplistdata` plugin reads the contents from the location mentioned below from an `NTUSER.dat` file:

`HKCU -> Software\Microsoft\Windows\CurrentVersion\Search\JumplistData`

We'll run RegRipper against the user's `NTUSER.dat` file using the command mentioned below:

```cmd-session
C:> C:\Tools\DFIR-Data\Tools\RegRipper\rip.exe -r C:\Tools\DFIR-Data\evidence\004.jumplists\NTUSER.DAT -p jumplistdata

Launching jumplistdata v.20200517
jumplistdata v.20200517
Gets contents of user's JumpListData key

2023-11-23 13:32:38Z  MSEdge
2023-11-23 13:35:00Z  {6D809377-6AF0-444B-8957-A3773F02200E}\Adobe\Acrobat DC\Acrobat\Acrobat.exe
2023-11-23 14:14:01Z  windows.immersivecontrolpanel_cw5n1h2txyewy!microsoft.windows.immersivecontrolpanel
2023-11-23 14:15:44Z  Microsoft.Windows.RemoteDesktop

```


# LNK Files

Let's navigate to the bottom of this section and click on "Click here to spawn the target system!". Then, let's RDP into the Target IP using the provided credentials. The vast majority of the actions and commands covered from this point up to end of this section can be replicated inside the target (referred as forensic workstation), offering a more comprehensive grasp of the topics presented.

Within the target (VM), you can locate the evidence and tools at the following paths:

- **LNK Files location**: `C:\Tools\DFIR-Data\evidence\005.lnk\KAPE_Output\D\Users\John Doe\AppData\Roaming\Microsoft\Windows\Recent`
- **KAPE Output location**: `C:\Tools\DFIR-Data\evidence\005.lnk\KAPE_Output`
- **LECmd Location**: `C:\Tools\DFIR-Data\Tools\EZ-Tools\net6`

* * *

## Introduction

LNK files, also known as shortcut files, are commonly used in Windows to create links to programs, files, and directories. In digital forensics, analyzing LNK files can provide valuable information about a user's activities, such as recently accessed files and programs. You can read more about LNK files in depth in the Microsoft documentation [here](https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-shllink/99e8d0e5-5bc6-4aed-af37-da7f584f832a).

LNK files are typically found in the user's profile directory at the location mentioned below:

```path
%APPDATA%\Microsoft\Windows\Recent

```

On the forensic workstation, this is stored on location mentioned below:

`C:\Tools\DFIR-Data\evidence\005.lnk\KAPE_Output\D\Users\John Doe\AppData\Roaming\Microsoft\Windows\Recent`

![lnk-recent](https://academy.hackthebox.com/storage/modules/248/lnk-recent_.png)

LNK files represent shortcuts to recent files and applications accessed by users, and they have a specific structure containing metadata and information about the linked item, which can help during forensic investigations. Key elements include:

- `Target Path`: The path to the linked item.
- `Timestamps`: Creation, access, and modification timestamps.
- `Icon Location`: Path to the icon associated with the linked item.
- `Working Directory`: The default working directory for the linked item.

* * *

## Analysis using LECmd

To process LNK files and the directories that contain them, we can use LECmd, another tool by Eric Zimmerman. It also provides options to export the processed data into CSV format. `LECmd.exe` is stored at the path mentioned below on the module's target workstation:

`C:\Tools\DFIR-Data\Tools\EZ-Tools\net6\LECmd.exe`

If we run `LECmd.exe` directly, it displays the help menu, where we can review the different flags and select the ones that are required.

```cmd-session
C:\Tools\DFIR-Data\Tools\EZ-Tools\net6\LECmd.exe

Description:
  LECmd version 1.5.0.0

  Author: Eric Zimmerman ([email protected])
  https://github.com/EricZimmerman/LECmd

  Examples: LECmd.exe -f "C:\Temp\foobar.lnk"
            LECmd.exe -f "C:\Temp\somelink.lnk" --json "D:\jsonOutput" --pretty
            LECmd.exe -d "C:\Temp" --csv "c:\temp" --html c:\temp --xml c:\temp\xml -q
            LECmd.exe -f "C:\Temp\some other link.lnk" --nid --neb
            LECmd.exe -d "C:\Temp" --all

            Short options (single letter) are prefixed with a single dash. Long commands are prefixed with two dashes

Usage:
  LECmd [options]

Options:
  -f <f>          File to process. Either this or -d is required
  -d <d>          Directory to recursively process. Either this or -f is required
  -r              Only process lnk files pointing to removable drives [default: False]
  -q              Only show the filename being processed vs all output. Useful to speed up exporting to json
...SNIP...

```

One of the two flags is required:

- `-f <f>`: File to process. Either this or `-d` is required.
- `-d <d>`: Directory to recursively process. Either this or `-f` is required.

* * *

### Analysis of _single_ LNK File using LECmd

Let's run the LECmd tool against a single `.lnk` file to understand what kind of information we can gather. Here's an example of processing the file `passwords.lnk` using LECmd with the `-f` flag.

```cmd-session
C:\Tools\DFIR-Data\Tools\EZ-Tools\net6\LECmd.exe -f "C:\Tools\DFIR-Data\evidence\005.lnk\KAPE_Output\D\Users\John Doe\AppData\Roaming\Microsoft\Windows\Recent\passwords.lnk"

...SNIP...

--- Header ---
  Target created:  2023-11-04 11:16:50
  Target modified: 2023-11-04 11:16:50
  Target accessed: 2023-11-04 11:17:09

  File size (bytes): 4,096
  Flags: HasTargetIdList, HasLinkInfo, HasRelativePath, IsUnicode, DisableKnownFolderTracking
  File attributes: FileAttributeDirectory
  Icon index: 0
  Show window: SwNormal (Activates and displays the window. The window is restored to its original size and position if the window is minimized or maximized.)

Relative Path: ..\..\..\..\..\..\..\Temp\passwords

--- Link information ---
Flags: VolumeIdAndLocalBasePath

>> Volume information
  Drive type: Fixed storage media (Hard drive)
  Serial number: 285D5E74
  Label: (No label)
  Local path: C:\Temp\passwords

--- Target ID information (Format: Type ==> Value) ---

  Absolute path: My Computer\C:\Temp\passwords

  -Root folder: GUID ==> My Computer

  -Drive letter ==> C:

  -Directory ==> Temp
    Short name: Temp
    Modified:    2023-11-04 11:17:02
    Extension block count: 1

    --------- Block 0 (Beef0004) ---------
    Long name: Temp
    Created:     2023-09-07 08:01:40
    Last access: 2023-11-04 11:17:02
    MFT entry/sequence #: 92487/2 (0x16947/0x2)

  -Directory ==> passwords
    Short name: PASSWO~1
    Modified:    2023-11-04 11:16:52
    Extension block count: 1

    --------- Block 0 (Beef0004) ---------
    Long name: passwords
    Created:     2023-11-04 11:16:52
    Last access: 2023-11-04 11:17:10
    MFT entry/sequence #: 89249/14 (0x15CA1/0xE)

--- End Target ID information ---

--- Extra blocks information ---

>> Tracker database block
   Machine ID:  htbvm01
   MAC Address: 90:e8:68:2d:3f:fa
   MAC Vendor:  (Unknown vendor)
   Creation:    2023-11-04 11:15:31

   Volume Droid:       8cfdf7e2-7535-4b5a-bdb0-eab3bc20fe41
   Volume Droid Birth: 8cfdf7e2-7535-4b5a-bdb0-eab3bc20fe41
   File Droid:         77bb6d2c-7b03-11ee-b829-90e8682d3ffa
   File Droid birth:   77bb6d2c-7b03-11ee-b829-90e8682d3ffa

>> Property store data block (Format: GUID\ID Description ==> Value)
   446d16b1-8dad-4870-a748-402ea43d788c\104    Volume Id                           ==> Unmapped GUID: f1fd3c73-cd2f-45c7-88e4-2afc965b890a

---------- Processed C:\Tools\DFIR-Data\evidence\005.lnk\KAPE_Output\D\Users\John Doe\AppData\Roaming\Microsoft\Windows\Recent\passwords.lnk in 0.19569180 seconds ----------

```

We'll now examine each section processed by LECmd and understand its importance from a forensics perspective. But first, let's explore the details of the Shell Binary file format and the structure it comprises.

* * *

## LNK file format Structures

The Shell Link Binary File Format (commonly known as LNK) is a file format used for shortcut files in Microsoft Windows. It consists of several structures that define various aspects of the shortcut.

1. `SHELL_LINK_HEADER`:
Contains general information about the shortcut, such as the size of the header, the size of the link target ID list, flags, and other metadata.

2. `LINKTARGET_IDLIST`:
Represents the location of the target file or directory. It typically includes an Item ID List (IDList) that specifies the file or directory.

3. `LINKINFO`:
Contains additional information about the shortcut, such as the location of the icon, the working directory, command-line arguments, and hotkey settings.

4. `STRING_DATA`:
Stores strings associated with the shortcut, such as the name of the target, the relative path, and other user-readable information.

5. `EXTRA_DATA`:
Holds additional data blocks that provide extended information about the shortcut. This can include property store information, tracker data, and other details.


![structures](https://academy.hackthebox.com/storage/modules/248/structures.png)

Reference: [https://learn.microsoft.com/en-us/openspecs/windows\_protocols/ms-shllink/](https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-shllink/)

* * *

### File and directory information (Header)

In the first block of the LECmd output, we can see information related to the source file, such as its timestamps (created, modified, and accessed), and the LNK file header information.

The header information consists of the LNK file's target created, modified, and accessed timestamps, the target's size, flags, and more.

Then, we can see file size, and also some flags. In this example, the flags are `HasTargetIdList`, `HasLinkInfo`, `HasRelativePath`, `IsUnicode`, and `DisableKnownFolderTracking`. These flags present in the header data provide additional information, such as the relative path. To understand more about the flags in detail, we can read the Microsoft documentation [here](https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-shllink/ae350202-3ba9-4790-9e9e-98935f4ee5af).

![lnk-hdr](https://academy.hackthebox.com/storage/modules/248/lnk-hdr-1.png)

* * *

### Link information and Local path

In the first section, if the `HasLinkInfo` flag is present, we can see the Link Information. The Link Information section also includes some flags that provide additional details. In the screenshot below, we can see the Volume Information structure, which provides information such as the serial number, drive type where the LNK file's target is present, and its local path.

![lnk-info](https://academy.hackthebox.com/storage/modules/248/lnk-info-1.png)

* * *

### Target ID information

In the first section, if the `HasTargetIdList` flag is present, then we can see the Target ID information. The screenshot below shows what it looks like:

![lnk-target](https://academy.hackthebox.com/storage/modules/248/lnk-target-1.png)

The Target ID information section contains many items, each starting with a dash followed by the type of item and its value. As we can see in the screenshot above, it includes information related to the root folder, drive letter, directories, and their timestamps.

* * *

### Extra blocks information

At the end of the output, we can see the Extra Blocks Information section, which contains many properties that provide valuable information. In this example, the Extra Blocks Information contains two blocks:

- Tracker Database Block
- Property Store Data Block.

![lnk-blocks](https://academy.hackthebox.com/storage/modules/248/lnk-blocks-1.png)

These blocks also contain useful information, such as the computer's NETBIOS name where the LNK was generated and a few GUIDs pertaining to the volume and target file.

Here's another example of a Property Store Data Block.

![lnk](https://academy.hackthebox.com/storage/modules/248/lnk.png)

* * *

## Analysis of _multiple_ LNK Files using LECmd

To perform analysis on multiple LNK files, we need to add all shortcut files (i.e., LNK files) to a folder and process the directory using LECmd.

We can copy all the shortcut (LNK files) files from `C:\Tools\DFIR-Data\evidence\005.lnk\KAPE_Output\D\Users\John Doe\AppData\Roaming\Microsoft\Windows\Recent\` to another path, such as `C:\Tools\DFIR-Data\evidence\005.lnk\lnk_files`.

**Note:** Make sure to include the full path in double quotes. And there should **`only`** be shortcut files in the directory, otherwise it may not work.

Then we'll run the command below with the following option:

- `-d`: This option requires the path of the directory for processing recursively.

This should provide an analysis of all LNK files, as shown in the output below:

```cmd-session
C:\Tools\DFIR-Data\Tools\EZ-Tools\net6\LECmd.exe -d "C:\Tools\DFIR-Data\evidence\005.lnk\lnk_files\"

...SNIP...

Looking for lnk files in C:\Tools\DFIR-Data\evidence\005.lnk\lnk_files\

Found 47 files

...SNIP...

```

To export the results into a CSV file, we can add the `--csv` and specify a destination path to save CSV.

```cmd-session
C:\Tools\DFIR-Data\Tools\EZ-Tools\net6\LECmd.exe -d <path_to_shortcuts_directory> --csv <path_to_csv_file>

```

In the above command, we are passing the following arguments:

`-d` \- This takes path to the directory to recursively process.
`--csv` \- Path to the directory to save CSV formatted results to.

For example, if we save the CSV with the destination path as `C:\Tools\DFIR-Data\evidence\005.lnk\LNK_CSV`, the output will be saved to a CSV file such as `LECmd_Output.csv` in the specified folder i.e. LNK\_CSV.

```cmd-session
C:> C:\Tools\DFIR-Data\Tools\EZ-Tools\net6\LECmd.exe -d "C:\Tools\DFIR-Data\evidence\005.lnk\lnk_files\" --csv C:\Tools\DFIR-Data\evidence\005.lnk\LNK_CSV

```

It also has an option to export the output in JSON format. The command below is used to export the results in JSON format.

```cmd-session
C:> C:\Tools\DFIR-Data\Tools\EZ-Tools\net6\LECmd.exe -d "C:\Tools\DFIR-Data\evidence\005.lnk\lnk_files\" --json C:\Tools\DFIR-Data\evidence\005.lnk\LNK_JSON --pretty

```

If we add JSON with destination path as `C:\Tools\DFIR-Data\evidence\005.lnk\LNK_JSON`, the output will be saved to `C:\Tools\DFIR-Data\evidence\005.lnk\LNK_JSON\LECmd_Output.json`

In the above command, we are providing the following arguments to LECmd:

- `--json`: Directory to save json representation to. Use --pretty for a more human readable layout
- `--pretty`: When exporting to json, use a more human readable layout `[default: False]`

The screenshot below shows an example of the output saved in JSON format.

![lecmd-json](https://academy.hackthebox.com/storage/modules/248/lecmd-json-1.png)

* * *

## Investigating Suspicious LNK Files

In this scenario, we will explore how some suspicious artifacts or IOCs can be extracted from LNK files, as these are heavily abused by threat actors for initial access.

For the demonstration, we have a shortcut file (LNK file) saved in the Demo directory of the evidence at `C:\Tools\DFIR-Data\evidence\005.lnk\Demo`.

![lnk-mshta](https://academy.hackthebox.com/storage/modules/248/lnk-susp-1.png)

This shortcut appears to be for a PDF file. However, if we run this file, it executes an HTA application. In the target of the LNK file, it contains the path to `mshta.exe` with a URL as an argument.

![lnk-mshta](https://academy.hackthebox.com/storage/modules/248/lnk-mshta-01.png)

We can run `LECmd.exe` to get more details.

```cmd-session
C:> C:\Tools\DFIR-Data\Tools\EZ-Tools\net6\LECmd.exe -f "C:\Tools\DFIR-Data\evidence\005.lnk\Demo\Invoice-details.pdf.lnk"

```

Since the target application is HTA, the argument is most likely an `.HTA` file.

![lnk-mshta1](https://academy.hackthebox.com/storage/modules/248/lnk-mshta1-1.png)

In the output from `LECMD.exe`, we can see that the arguments contain a URL, which is most probably a HTA file.

![lnk-mshta2](https://academy.hackthebox.com/storage/modules/248/lnk-mshta-002.png)

This also contains information about the machine where the LNK file was created and the time it was created.

![lnk-mshta2](https://academy.hackthebox.com/storage/modules/248/lnk_machine1.png)

* * *

### Real world malware samples using LNK files

Here's one [example](https://blog.eclecticiq.com/operation-flightnight-indian-government-entities-and-energy-sector-targeted-by-cyber-espionage-campaign) where we can see two different malware variants using the same LNK file created on the same machine.

In the first malware variant, the threat actor is using a modified version of [HackBrowserData](https://github.com/moonD4rk/HackBrowserData), an open-source post-exploitation tool. This variant is bundled as an ISO file that contains a decoy PDF document, malware in executable form, and a shortcut file (LNK file) intended to trick recipients into activating the malware.

![lnk-mshta2](https://academy.hackthebox.com/storage/modules/248/lnk_machine2.png)

The second screenshot shown below is from a different variant, which uses GoStealer (a Golang-based credential stealer) instead of HackBrowserData. The rest of the delivery mechanism is the same. It also contains an ISO file with a decoy PDF document, an executable, and a shortcut file (LNK file).

![lnk-mshta2](https://academy.hackthebox.com/storage/modules/248/lnk_machine3.png)

The interesting finding from the analysis of LNK files is that the machine ID and creation time are the same in both variants, which provides strong evidence that both campaigns are likely the work of the same threat actor.

* * *

In [this blog](https://www.bleepingcomputer.com/news/security/bumblebee-malware-adds-post-exploitation-tool-for-stealthy-infections/) from Bleeping Computer, it is mentioned that adversaries use LNK files for initial access or execution of payloads. That's also why LNK metadata is essential from a forensics perspective.

- "Bumblebee reached victims via emails carrying password-protected zipped ISO files that contained an LNK file (for executing the payload) and a DLL file (the payload)."
- "In the recent attack, Bumblebee replaced the ISO with a VHD (Virtual Hard Disk) file, which, again, contains an LNK shortcut file."
- "The Emotet malware distributors launched a new email campaign that included password-protected ZIP file attachments containing Windows LNK (shortcut) files masquerading as Word documents."

References:

- [https://www.bleepingcomputer.com/news/security/bumblebee-malware-adds-post-exploitation-tool-for-stealthy-infections/](https://www.bleepingcomputer.com/news/security/bumblebee-malware-adds-post-exploitation-tool-for-stealthy-infections/)

- [https://www.bleepingcomputer.com/news/security/emotet-malware-infects-users-again-after-fixing-broken-installer](https://www.bleepingcomputer.com/news/security/emotet-malware-infects-users-again-after-fixing-broken-installer)


# Run MRU Forensics

## Introduction

The Run Most Recently Used (MRU) feature in Windows maintains a record of the most recently executed programs or commands on a system when they are opened through Windows Run. Windows Run is usually opened using `WIN + R` or by right-clicking on Start and selecting Run.

The screenshot below shows an example of Run Most Recently Used entries.

![runmru1](https://academy.hackthebox.com/storage/modules/248/runmru1_.png)

This information is stored in the Windows Registry. Analyzing the Run MRU artifacts provides digital forensics investigators with valuable insights into a user's recent activities, shedding light on the programs or commands they might have executed. Run MRU forensics is a crucial aspect of digital investigations, contributing to a comprehensive understanding of user behavior and aiding in the reconstruction of events on a Windows system.

* * *

## Location of the Run MRU

The Run Most Recently Used (MRU) artifact is stored in the Windows Registry and consists of multiple values under the "RunMRU" key, each named after lowercase letters. These values store the commands executed by a user through the Run utility.

The paths shown below are some common locations in the Windows registry where we can find these entries:

- `HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\RunMRU`
- `HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Explorer\RunMRU`

In terms of user behavior, this registry hive is stored inside the NTUSER.DAT of the specific user. The screenshot below shows how this looks in the registry.

![runmru2](https://academy.hackthebox.com/storage/modules/248/runmru2_.png)

* * *

## Understanding the MRUList

The order in which these commands were typed is not always reflected by the alphabetical names of the values; instead, the sequence is maintained by the "MRUList" value. The "MRUList" is a string that specifies the order in which each value under the RunMRU key was last accessed.

![runmru3](https://academy.hackthebox.com/storage/modules/248/runmru3_.png)

For example, in the screenshot below, we can see that the MRUList begins with "n". The value named "n" would store the most recent command used by the user through the Run utility.

![runmru4](https://academy.hackthebox.com/storage/modules/248/runmru4-1.png)

In this example, the value "n" has stored the most recent command, i.e., `C:\Temp\passwords\users.txt`, indicating that it is the latest command entered into the Windows Run dialog box.

![runmru5](https://academy.hackthebox.com/storage/modules/248/runmru5.png)

* * *

## Exploring Run MRUs using Registry Explorer

Let's navigate to the bottom of this section and click on "Click here to spawn the target system!". Then, let's RDP into the Target IP using the provided credentials. The vast majority of the actions and commands covered from this point up to end of this section can be replicated inside the target, offering a more comprehensive grasp of the topics presented.

Within the target (VM), you can locate the evidence and tools at the following paths:

- **NTUSER.DAT file location**: `C:\Tools\DFIR-Data\evidence\006.run_mru\NTUSER.DAT`
- **Registry Explorer location**: `C:\Tools\DFIR-Data\Tools\EZ-Tools\net6\RegistryExplorer`
- **RegRipper location**: `C:\Tools\DFIR-Data\Tools\RegRipper`

If you're not able to view the `NTUSER.DAT` file, make sure that the hidden files are shown in the File Explorer.

* * *

In the Registry Explorer, we can easily find the list of Run MRU items ordered in the correct MRU position. After opening Registry Explorer, we'll browse to the `NTUSER.DAT` file from the path as mentioned in the beginning of this section.

`C:\Tools\DFIR-Data\evidence\006.run_mru\NTUSER.DAT`

Navigate to RunMRU in the available bookmarks. The screenshot below shows the value of the MRUList:

![runmru6](https://academy.hackthebox.com/storage/modules/248/mrulist_split.png)

The order of items in Run MRU is sorted using the sequence defined in the MRUList, as shown in the image below:

![runmru6](https://academy.hackthebox.com/storage/modules/248/mrulist_order.png)

In this version of `NTUSER.DAT`, the latest item in the list is `powershell`, followed by `regedit`, then `cmd`, and so on. The screenshot below shows that Registry Explorer automatically displays the list items in the correct order.

![runmru6](https://academy.hackthebox.com/storage/modules/248/runmru6-1_.png)

## Exploring Run MRUs using RegRipper

RegRipper includes the `runmru` plugin designed to analyze the RunMRU data. The `NTUSER.DAT` file contains user-specific registry settings, including the RunMRU key. On the module's target system, the `NTUSER.DAT` file is stored at the path below:

`C:\Tools\DFIR-Data\evidence\006.run_mru\NTUSER.DAT`

Type the command below to run the `runmru` plugin.

```cmd-session
C:\Tools\DFIR-Data\Tools\RegRipper\rip.exe -r "C:\Tools\DFIR-Data\evidence\006.run_mru\NTUSER.DAT" -p runmru

Launching runmru v.20200525
runmru v.20200525
(NTUSER.DAT) Gets contents of user's RunMRU key

RunMru
Software\Microsoft\Windows\CurrentVersion\Explorer\RunMRU
LastWrite Time 2023-11-22 10:29:58Z
MRUList = gmbnlkjihfdeac
a   sysdm.cpl\1
b   cmd\1
c   ping google.com\1
d   {REDACTED}\1
e   secpol.msc\1
f   appwiz.cpl\1
g   powershell\1
h   notepad\1
i   services.msc\1
j   \\10.10.10.11\Tools\1
k   \\10.10.10.11\htbfs01\1
l   explorer\1
m   regedit\1
n   C:\Temp\passwords\users.txt\1

```

In the output from RegRipper's `runmru` plugin, we can see that the `MRUList = gmbnlkjihfdeac`, which indicates that the most recently executed command was `g`, which is `powershell`, followed by `m`, which is `regedit`, and then `b`, which is `cmd`, and so on. This structure allows forensic analysts to reconstruct the chronology of user actions involving the Run utility. The MRUList value helps establish the sequence of events, providing a timeline of command execution. The commands executed can provide insight into the user's intent and actions.


# Recent Docs

## Introduction

This section involves the analysis of artifacts stored in the Windows Registry key `RecentDocs`, which relates to the documents recently accessed by users. This key maintains information about the user's interaction with files and folders. The key is located in the registry hive `HKEY_CURRENT_USER`, i.e., inside the `NTUSER.DAT` file at the location mentioned below.

```regpath
Software\Microsoft\Windows\CurrentVersion\Explorer\RecentDocs

```

![recentdocs1](https://academy.hackthebox.com/storage/modules/248/recentdocs1.png)

Under the `RecentDocs` key, entries are created for each file that has been accessed, providing details such as the file name, path, and the associated application.

![recentdocs2](https://academy.hackthebox.com/storage/modules/248/recentdocs2.png)

* * *

## MRUListEx in Recent docs

The `RecentDocs` key within the Windows Registry comprises multiple values assigned numerical names, each containing binary data. Notably, the `MRUListEx` value within this key plays a crucial role in tracking the sequential order in which files and folders were accessed by the user. The numerical names assigned to these values do not necessarily reflect the order of access; instead, the `MRUListEx` value holds the accurate chronology of these activities. Tools like Registry Explorer or RegRipper use the `MRUListEx` value to sort the list items in the correct order.

![recentdocs2](https://academy.hackthebox.com/storage/modules/248/MRUListEx.png)

Additionally, the `RecentDocs` key features subkeys named after various file extensions, reflecting the types of files accessed by the user. Within each extension-specific subkey, numbered values store binary data and are accompanied by an `MRUListEx` value, maintaining the order of access for files with that specific extension.

* * *

## Analyzing Recent docs using Registry Explorer

Let's navigate to the bottom of this section and click on "Click here to spawn the target system!". Then, let's RDP into the Target IP using the provided credentials. The vast majority of the actions and commands covered from this point up to end of this section can be replicated inside the target, offering a more comprehensive grasp of the topics presented.

Within the target (VM), you can locate the evidence and tools at the following paths:

- **NTUSER.DAT file location**: `C:\Tools\DFIR-Data\evidence\007.recentdocs\NTUSER.DAT`
- **Registry Explorer location**: `C:\Tools\DFIR-Data\Tools\EZ-Tools\net6\RegistryExplorer`
- **RegRipper location**: `C:\Tools\DFIR-Data\Tools\RegRipper`

If you're not able to view the `NTUSER.DAT` file, make sure that the hidden files are shown in the File Explorer.

* * *

The registry values are parsed and displayed more clearly in Registry Explorer, allowing us to interpret the information stored within the `RecentDocs` key. The `NTUSER.DAT` file is stored at the path mentioned below:

`C:\Tools\DFIR-Data\evidence\007.recentdocs\NTUSER.DAT`

Import the `NTUSER.DAT` file into Registry Explorer and navigate to `RecentDocs` in the available bookmarks.

![recentdocs3](https://academy.hackthebox.com/storage/modules/248/recentdocs3.png)

Furthermore, the `Folder` subkey within `RecentDocs` serves to record the most recently accessed folders. Similar to file extension subkeys, it contains numbered values storing binary data, and the `MRUListEx` value provides insight into the sequence in which these folders were opened.

![recentdocs4](https://academy.hackthebox.com/storage/modules/248/recentdocs4.png)

## Analysis of RecentDocs using RegRipper

RegRipper contains `recentdocs` plugin to analyze RecentDocs data, making the analysis process more efficient and systematic. This plugin is used to retrieve the contents of a user's `RecentDocs` key. The output will display the recently accessed documents, along with their respective `MRUListEx` values, as shown below:

The command shown below runs this plugin and extracts the `recentdocs` items.

```cmd-session

C:\Tools\DFIR-Data\Tools\RegRipper\rip.exe -r "C:\Tools\DFIR-Data\evidence\007.recentdocs\NTUSER.DAT" -p recentdocs

Launching recentdocs v.20200427
recentdocs v.20200427
(NTUSER.DAT) Gets contents of user's RecentDocs key

RecentDocs
**All values printed in MRUList\MRUListEx order.
Software\Microsoft\Windows\CurrentVersion\Explorer\RecentDocs
LastWrite Time: 2023-11-22 10:29:47Z
  43 = Tools
  42 = {REDACTED}.ps1
  12 = HR
  8 = salary_details.csv
  24 = System32
  23 = passwords
  39 = users.txt
  0 = System32
  41 = upload on speedtest.tele2.net
  40 = upload_file.txt
  34 = csv
  35 = logs
  38 = edr
  37 = bacup
  11 = data
  36 = Powershell
  33 = Backup
  29 = HTBFS01
  4 = Local Disk (C:)
  32 = Business
  31 = Sales
  30 = Finance
  13 = IT
  6 = This PC
  28 = C:\
  27 = New folder
  26 = Programs
  25 = ::{7B81BE6A-CE2B-4676-A29E-EB907A5126C5}
  22 = System and Security
  21 = ::{BB64F8A7-BEE7-4E1A-AB8D-7D8273F7FDB6}
  5 = Network and Internet
  14 = ::{8E908FC9-BECC-40F6-915B-F4CA0E70D03D}
  20 = ::{679F85CB-0220-4080-B29B-5540CC05AAB6}
  17 = network_server_sensitive
  19 = stock_plans.docx
  18 = new_proposal.docx
  16 = new_projects.docx
  15 = private-key.ppk
  2 = The Internet
  1 = redirect
  9 = discord
  10 = discord.apmx64
  7 = threat/
  3 = Temp

Software\Microsoft\Windows\CurrentVersion\Explorer\RecentDocs\.apmx64
LastWrite Time 2023-09-10 14:43:43Z
MRUListEx = 0
  0 = discord.apmx64

Software\Microsoft\Windows\CurrentVersion\Explorer\RecentDocs\.csv
LastWrite Time 2023-11-22 10:27:38Z
MRUListEx = 0
  0 = salary_details.csv

...SNIP

```

Further down in the RegRipper output, we can see the files organized by extension.

![recentdocs6](https://academy.hackthebox.com/storage/modules/248/recentdocs6-1_.png)

We can also see the recently accessed folders in the same output.

![recentdocs6](https://academy.hackthebox.com/storage/modules/248/recentdocs7-1.png)

In essence, RecentDocs forensics delves into these registry entries to reconstruct user actions, revealing a comprehensive view of recent file and folder access on the system. The `RecentDocs` key can reveal valuable information about a user's activities, such as which documents have been recently accessed or opened by the user. It can provide insights into the user's focus and actions based on the types of documents accessed.


# Open/Save Dialog MRUs

## Introduction

Open and Save Dialog MRUs (Most Recently Used) are artifacts in the Windows operating system that store information about the most recently accessed files and directories through open and save dialog boxes in various applications. These MRUs provide a record of user interactions with files, indicating which files were accessed, when they were accessed, and through which applications.

The purpose of Open Dialog MRU is to record the paths of files and directories that users have navigated to using the open dialog box. Save Dialog MRUs maintain a list of the most recently used paths for saving files. The image below shows an example of these most recently used paths.

![opensv1](https://academy.hackthebox.com/storage/modules/248/opensv1_.png)

This includes paths accessed through applications like text editors, image viewers, browsers, and other programs. The screenshot below shows a scenario where the user downloaded a file from the browser, and the browser opened the save dialog to specify the location where the file was to be saved. This can reveal what files were downloaded by the user.

![saveas](https://academy.hackthebox.com/storage/modules/248/saveas.png)

## Location of Open/Save Dialog MRUs

This information is stored in the registry at the path mentioned below:

`HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\ComDlg32\`

* * *

Let's navigate to the bottom of this section and click on "Click here to spawn the target system!". Then, let's RDP into the Target IP using the provided credentials. The vast majority of the actions and commands covered from this point up to end of this section can be replicated inside the target, offering a more comprehensive grasp of the topics presented.

Within the target (VM), you can locate the evidence and tools at the following paths:

- **NTUSER.DAT file location**: `C:\Tools\DFIR-Data\evidence\008.open_save\NTUSER.DAT`
- **Registry Explorer location**: `C:\Tools\DFIR-Data\Tools\EZ-Tools\net6\RegistryExplorer`
- **RegRipper location**: `C:\Tools\DFIR-Data\Tools\RegRipper`

If you're not able to view the `NTUSER.DAT` file, make sure that the hidden files are shown in the File Explorer.

* * *

## Analysis using Registry Explorer

The `NTUSER.DAT` file is saved on the module's target system at the path mentioned below:

`C:\Tools\DFIR-Data\evidence\008.open_save\NTUSER.DAT`

We can load the `NTUSER.DAT` file into Registry Explorer and browse to the `ComDlg32` key. In the screenshot shown below, we can see there are three subkeys in this path:

![opensv2](https://academy.hackthebox.com/storage/modules/248/opensv2-1.png)

Below are the three subkeys:

1. **CIDSizeMRU**
2. **LastVisitedPidlMRU**
3. **OpenSavePidlMRU**

The forensics of these artifacts provides insights into the files and directories accessed by users through applications that utilize open/save dialog boxes. Let's explore these artifacts using Registry Explorer to see what kind of information can be extracted from them.

* * *

### CIDSize MRU

This subkey tracks recently launched applications globally.

![cidsize](https://academy.hackthebox.com/storage/modules/248/cidsize_.png)

It also contains an MRU list that specifies the order in which applications were last opened.

![cidsizemru](https://academy.hackthebox.com/storage/modules/248/cidsizemru.png)

* * *

### LastVisited Pidl MRU

[PIDL](https://learn.microsoft.com/en-us/previous-versions/windows/desktop/legacy/cc144089(v=vs.85)#pidls) sstands for "pointer to an item identifier list," and MRU stands for "Most Recently Used." The `LastVisitedPidlMRU` refers to the "Most Recently Used" list of pointers to Item ID Lists associated with the last visited directories or folders when opening or saving files using certain applications in the Windows operating system. The `LastVisitedPidlMRU` registry key tracks the specific executable used by an application to open files documented in the `OpenSavePidlMRU` key (which is explained next).

Each value within this key tracks the directory location for the last file accessed by that application. The data is stored in binary format, and the key maintains its own MRU list and last write time. This information is crucial for applications to remember the last directory used when opening or saving files.

![lastvisited](https://academy.hackthebox.com/storage/modules/248/lastvisited_.png)

After opening Registry Explorer, navigate to the specified registry key. This is saved in the `NTUSER.DAT` registry hive.

```regpath
HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\ComDlg32\LastVisitedPidlMRU

```

![lastvisited1](https://academy.hackthebox.com/storage/modules/248/lastvisited1.png)

* * *

### OpenSave Pidl MRU

"OpenSave PIDL MRU" refers to the "Most Recently Used" list of pointers to Item ID Lists associated with files opened or saved using the Windows shell's Open/Save dialog boxes. Each entry in this list represents a recently accessed file along with its corresponding path and other relevant information.

```regpath
HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\ComDlg32\OpenSavePidlMRU

```

In the right pane, you'll see entries corresponding to each accessed file or folder through the Open dialog.

![opensave1](https://academy.hackthebox.com/storage/modules/248/opensave1_.png)

* * *

## Analyzing all MRUs using RegRipper

RegRipper includes the `comdlg32` plugin designed for parsing the `comdlg32` key, allowing foresnic analysts to extract relevant information easily. The command to run the `comdlg32` plugin in RegRipper is shown in the snippet below.

```cmd-session
C:\Tools\DFIR-Data\Tools\RegRipper\rip.exe -r "C:\Tools\DFIR-Data\evidence\008.open_save\NTUSER.DAT" -p comdlg32

Launching comdlg32 v.20200517
comdlg32 v.20200517

Software\Microsoft\Windows\CurrentVersion\Explorer\ComDlg32
LastWrite Time 2023-09-10 13:16:22Z
CIDSizeMRU
LastWrite: 2023-11-22 10:29:47Z
Note: All value names are listed in MRUListEx order.

  NOTEPAD.EXE
  apimonitor-x64.exe
  {REDACTED}.exe

LastVisitedPidlMRU
LastWrite time: 2023-11-22 10:29:47Z
Note: All value names are listed in MRUListEx order.

  NOTEPAD.EXE - My Computer\C:\Tools
  apimonitor-x64.exe - My Computer\C:\Temp\discord
  {REDACTED}.exe - My Computer\C:\Temp

OpenSavePidlMRU
LastWrite time: 2023-11-22 10:29:47Z
OpenSavePidlMRU\*
LastWrite Time: Wed Nov 22 10:29:47 2023
Note: All value names are listed in MRUListEx order.

  My Computer\C:\Tools\Invoke-Mimikatz.ps1
  My Computer\C:\Temp\discord\discord.apmx64
  My Computer\C:\Temp\{REDACTED}.exe
  My Computer\C:\Temp
  My Computer\C:

OpenSavePidlMRU\apmx64
LastWrite Time: Sun Sep 10 14:43:42 2023
Note: All value names are listed in MRUListEx order.

  My Computer\C:\Temp\discord\discord.apmx64

OpenSavePidlMRU\exe
LastWrite Time: Sun Sep 10 13:43:27 2023
Note: All value names are listed in MRUListEx order.

  My Computer\C:\Temp\{REDACTED}.exe

OpenSavePidlMRU\ps1
LastWrite Time: Wed Nov 22 10:29:47 2023
Note: All value names are listed in MRUListEx order.

  My Computer\C:\Tools\Invoke-Mimikatz.ps1

```

The information is properly categorized in the output:

![regrip1](https://academy.hackthebox.com/storage/modules/248/regrip01_.png)

**CIDSize MRU**:

At the bottom, it shows the entries of the applications accessed by the user.

![regrip1](https://academy.hackthebox.com/storage/modules/248/regrip1_.png)

**Last Visited Pidl MRU**:

At the bottom, it shows the entries of the applications and the paths of the files accessed in those applications by the user.

![regrip2](https://academy.hackthebox.com/storage/modules/248/regrip2_.png)

**Open Save Pidl MRU**:

At the bottom, it shows the entries of the full paths of the files accessed by the user.

![regrip3](https://academy.hackthebox.com/storage/modules/248/regrip3_.png)

Analyzing the `comdlg32` key reveals important details about user interactions with files and directories through common dialog boxes, helping forensic analysts reconstruct user behavior and identify significant files. This can add value to the investigation by showing the last visited directories and files that have been recently accessed or saved, thus helping to understand the user's file navigation behavior and application usage.


# TypedPaths

## Introduction

TypedPaths are artifacts in the Windows Registry that store information about the paths a user has typed into the address bars of certain Windows Explorer interfaces. These entries provide insights into the user's behavior and the locations they have accessed.

![tp-explorer](https://academy.hackthebox.com/storage/modules/248/tp-explorer.png)

These artifacts are also useful in forensic investigations to reconstruct a user's activity and determine the locations they have been navigating to, which can provide insights into the user's workflow.

* * *

## Location of TypedPaths

TypedPaths are stored in the Windows Registry, usually under the following keys in `NTUSER.DAT`:

```regpath
HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\TypedPaths

```

The screenshot below shows the registry location of TypedPaths:

![tg-reg](https://academy.hackthebox.com/storage/modules/248/tg-reg.png)

* * *

## Explore TypedPaths using Registry Explorer

Let's navigate to the bottom of this section and click on "Click here to spawn the target system!". Then, let's RDP into the Target IP using the provided credentials. The vast majority of the actions and commands covered from this point up to end of this section can be replicated inside the target, offering a more comprehensive grasp of the topics presented.

Within the target (VM), you can locate the evidence and tools at the following paths:

- **NTUSER.DAT file location**: `C:\Tools\DFIR-Data\evidence\009.typedpaths\NTUSER.DAT`
- **Registry Explorer location**: `C:\Tools\DFIR-Data\Tools\EZ-Tools\net6\RegistryExplorer`
- **RegRipper location**: `C:\Tools\DFIR-Data\Tools\RegRipper`

If you're not able to view the `NTUSER.DAT` file, make sure that the hidden files are shown in the File Explorer.

* * *

The TypedPaths entries store paths to folders or files that users have accessed by typing or pasting into the Explorer URL bar. Entries might include details such as the path, the date and time it was accessed, and other relevant information.

Forensic analysts can use registry analysis tools like Registry Explorer or RegRipper to parse and examine TypedPaths entries. The registry values are parsed and displayed more clearly in Registry Explorer, allowing us to interpret the information stored within the TypedPaths key.

Launch Registry Explorer on the forensic workstation and browse to the `NTUSER.DAT` file from the KAPE output. First, open Registry Explorer from the EZ-Tools path below on the forensic workstation:

`C:\Tools\DFIR-Data\Tools\EZ-Tools\net6\RegistryExplorer`

Let's browse to the `NTUSER.DAT` file using the path mentioned at the beginning of this section.

`C:\Tools\DFIR-Data\evidence\009.typedpaths\NTUSER.DAT`

Now, import the `NTUSER.DAT` file into Registry Explorer, and navigate to the TypedPaths location as shown in the screenshot below.

![tp-regexp](https://academy.hackthebox.com/storage/modules/248/tp-regexp.png)

## RegRipper's TypedPaths plugin

RegRipper includes `typedpaths` plugin, which is specifically designed to analyze the TypedPaths key, making it easier to retrieve and analyze this data.

To check this in RegRipper, we can open the RegRipper tool from the directory below:

`C:\Tools\DFIR-Data\Tools\RegRipper`

RegRipper will process the `NTUSER.DAT` file and extract the TypedPaths entries. The output will display the paths that have been manually entered by the user into the Windows Explorer address bar. The command to run the `typedpaths` plugin in RegRipper is shown in the snippet below:

```cmd-session

C:\Tools\DFIR-Data\Tools\RegRipper\rip.exe -r "C:\Tools\DFIR-Data\evidence\009.typedpaths\NTUSER.DAT"  -p typedpaths

Launching typedpaths v.20200526
typedpaths v.20200526
(NTUSER.DAT) Gets contents of user's typedpaths key

Software\Microsoft\Windows\CurrentVersion\Explorer\TypedPaths
LastWrite Time 2023-11-21 17:58:34Z

url1     C:\Users\John Doe\AppData\Roaming
url2     ftp://speedtest.tele2.net/
url3     ftp://ftp.sysinternals.com/
url4     powershell
url5     https://live.sysinternals.com/
url6     \\10.10.10.11\Tools

```

In this example, the TypedPaths key shows the most recently accessed paths, providing a clear view of the user's navigation history within Windows Explorer. The TypedPaths key can provide valuable information about user activity, such as navigation patterns, including the paths the user manually entered, indicating areas of interest or frequent access. This can also show paths to potentially important directories or network shares that the user has accessed, which could contain critical evidence.


# MS Office Accessed Files (File MRU)

## Introduction

The MS Office File MRU (Most Recently Used) registry artifact is a valuable piece of information in digital forensics and incident response (DFIR). It stores references to Microsoft Office files that have been accessed by a user. This artifact falls under the "Data Accessed" category, capturing information about files a user has recently opened using Microsoft Office applications.

The primary purpose of the Office MRU is to facilitate user convenience. It enables Office applications to present users with a list of recently opened files, allowing them to quickly access files without navigating to the folder where the files are stored.

The screenshot shown below provides an example of how the Office-related MRUs look:

![excel-recent](https://academy.hackthebox.com/storage/modules/248/excel-recent.png)

* * *

## Location of the MS Office File MRU

The Office MRU data is stored in the user's `NTUSER.DAT` registry hive.

```Registry-Path
Computer\HKEY_CURRENT_USER\SOFTWARE\Microsoft\Office\

```

For example, the File MRU data for MS Office version 16.0 for Excel is saved under the path below:

```Registry-Path
Computer\HKEY_CURRENT_USER\SOFTWARE\Microsoft\Office\16.0\Excel\File MRU

```

## Content of the MS Office File MRU

Each Office application and version has its own list. For instance, the path for Word 2016 could be:

`HKCU\SOFTWARE\Microsoft\Office\16.0\Word\`

The relevant sub-keys within this path include:

- **File MRU**:
Contains references to files recently opened.

- **Place MRU**:
Stores information about folders recently used for opening or saving files.

- **User MRU**:
Contains data on files and folders recently used when an online Microsoft account was utilized.


The screenshot below shows how these file-related entries are stored in the registry.

![ms-filemru](https://academy.hackthebox.com/storage/modules/248/ms-filemru.png)

In digital forensics and incident response, the Office MRU is a valuable source of information. It can reveal insights into a user's recent focus on documents and files. Some scenarios where it is useful include:

- **Intrusion Case with Account Takeover**:
Shows documents the attacker was interested in.

- **Insider Threat Case**:
Reveals the types of documents the user intended to steal.

- **General Investigations**:
Provides information about the user's recent activities and the purpose of computer usage.


It is also noted that when MS Office is not installed and the user uses another office application, such as [LibreOffice](https://www.libreoffice.org/), the file MRUs are stored under `LiveId_{hash} File MRU` of the `User MRU`. On this machine, MS Office was installed earlier and removed later. Further research is needed to determine if this behavior is the same for other office alternatives, such as [OnlyOffice](https://www.onlyoffice.com/), [OpenOffice](https://www.openoffice.org/), [WPS Office](https://www.wps.com/), etc.

![office](https://academy.hackthebox.com/storage/modules/248/office.png)

* * *

## Analysis using Registry Explorer

Let's navigate to the bottom of this section and click on "Click here to spawn the target system!". Then, let's RDP into the Target IP using the provided credentials. The vast majority of the actions and commands covered from this point up to end of this section can be replicated inside the target, offering a more comprehensive grasp of the topics presented.

Within the target (VM), you can locate the evidence and tools at the following paths:

- **NTUSER.DAT file location**: `C:\Tools\DFIR-Data\evidence\010.msoffice\NTUSER.DAT`
- **Registry Explorer location**: `C:\Tools\DFIR-Data\Tools\EZ-Tools\net6\RegistryExplorer`
- **RegRipper location**: `C:\Tools\DFIR-Data\Tools\RegRipper`

If you're not able to view the `NTUSER.DAT` file, make sure that the hidden files are shown in the File Explorer.

* * *

To open MS Office File/Place/User MRU with Registry Explorer, follow these steps:

1. **Launch Registry Explorer**: Open the Registry Explorer tool. This is located at the path below:

`C:\Tools\DFIR-Data\Tools\EZ-Tools\net6\RegistryExplorer`

2. **Browse to the NTUSER.DAT path**: Navigate to the user's `NTUSER.DAT` file you want to analyze. This file is typically located in the user's profile directory, for example, `C:\Users\Username\NTUSER.DAT`. For demonstration purposes, we have saved the `NTUSER.DAT` file at the path mentioned at the beginning of this section.

`C:\Tools\DFIR-Data\evidence\010.msoffice\NTUSER.DAT`

3. **Load the NTUSER.DAT File**: Use the "File" menu in Registry Explorer and select "Load Hive," then navigate to the `NTUSER.DAT` file and open it.

4. **Navigate to the MS Office MRU Keys**: There are three type of MRU files:


- `File MRU`: Navigate to `HKEY_CURRENT_USER\Software\Microsoft\Office\XX.0\Word\File MRU` (Replace XX with the version number of Office, e.g., 16.0 for Office 2016)
- `Place MRU`: Navigate to `HKEY_CURRENT_USER\Software\Microsoft\Office\XX.0\Word\Place MRU`
- `User MRU`: Navigate to `HKEY_CURRENT_USER\Software\Microsoft\Office\XX.0\Word\User MRU`

For example, the screenshot below shows an example of File MRUs:

![office](https://academy.hackthebox.com/storage/modules/248/msoffice-mru.png)

## RegRipper plugin for MS Office File MRU

This can be verified using RegRipper as well. The `msoffice` plugin is used to retrieve the contents of a user's MS Office MRU. To do this, first locate the `NTUSER.DAT` file of the user you want to analyze. Open a command prompt or terminal and navigate to the directory where RegRipper is installed.

Execute RegRipper with the `msoffice` plugin against the `NTUSER.DAT` file. It provides timestamp details and separate entries for each Office component, such as Word, PowerPoint, Excel, and Outlook.

```powershell
PS C:\Tools\DFIR-Data\Tools\RegRipper> .\rip.exe -r "C:\Tools\DFIR-Data\evidence\010.msoffice\NTUSER.DAT" -p msoffice
Launching  msoffice v.20200518
msoffice v.20200518

Word - File MRU
2023-11-22 13:27:02Z: C:\Users\John Doe\Desktop\Copied_from_server\August_SOA.doc

Word - Place MRU
2023-11-22 13:27:02Z: C:\Users\John Doe\Desktop\Copied_from_server\

PowerPoint - File MRU
2023-11-22 13:27:25Z: C:\Users\{REDACTED}.ppt

PowerPoint - Place MRU
2023-11-22 13:27:25Z: C:\Users\John Doe\Desktop\Copied_from_server\

Excel - File MRU
2023-11-22 13:27:21Z: C:\Users\John Doe\Desktop\Copied_from_server\may_expenses.xlsx
2023-11-22 13:27:13Z: C:\Users\John Doe\Desktop\Copied_from_server\invoice.xlsm

Excel - Place MRU
2023-11-22 13:27:21Z: C:\Users\John Doe\Desktop\Copied_from_server\

```

The files are listed and categorized according to their file types or extensions.

![reg2](https://academy.hackthebox.com/storage/modules/248/reg2-1_.png)

This works with the help of the [msoffice.pl](https://github.com/keydet89/RegRipper3.0/blob/master/plugins/msoffice.pl) script , which parses various MRU (Most Recently Used) entries for Microsoft Office applications by examining specific registry keys within the loaded `NTUSER.DAT` hive. The script starts by identifying the installed versions of Microsoft Office by scanning the `Software\Microsoft\Office` registry path and sorting the versions in descending order to get the most recent version. It then parses the File, Place, and User MRU entries for each Office application (Word, PowerPoint, Excel, Access). Finally, it processes the MRU values by extracting and converting timestamps and file paths and prints the output. Similarly, you can learn in depth about how other plugins work by going through the code for these plugins. Reading the code helps in understanding the exact process and logic used in parsing registry keys and values.


# Adobe Recent Files

Let's navigate to the bottom of this section and click on "Click here to spawn the target system!". Then, let's RDP into the Target IP using the provided credentials. The vast majority of the actions and commands covered from this point up to end of this section can be replicated inside the target, offering a more comprehensive grasp of the topics presented.

Within the target (VM), you can locate the evidence and tools at the following paths:

- **NTUSER.DAT file location**: `C:\Tools\DFIR-Data\evidence\017.adobe\NTUSER.DAT`
- **Registry Explorer location**: `C:\Tools\DFIR-Data\Tools\EZ-Tools\net6\RegistryExplorer`
- **RegRipper location**: `C:\Tools\DFIR-Data\Tools\RegRipper`

If you're not able to view the `NTUSER.DAT` file, make sure that the hidden files are shown in the File Explorer.

* * *

## Introduction

The Windows Registry is a critical resource for forensic investigators, providing a wealth of information about user behavior and document usage patterns. Among the various applications, Adobe software like Adobe Acrobat and Adobe Reader is frequently used for handling PDF documents. These applications record the list of recently accessed files, making it possible to track a user's interactions with PDF documents.

For Adobe Reader, specific registry keys contain data on recently accessed files, which is instrumental in piecing together a user's activity within the application.

- **File**: `NTUSER.DAT`
- **Location**: `Software\Adobe\Adobe Acrobat\DC\AVGeneral\cRecentFiles`

## Analysis using RegRipper's Adobe plugin

The tool RegRipper, with its `adobe` plugin, is particularly useful in this context. It extracts information about the PDF documents recently accessed by the user, aiding in the reconstruction of user activities and document usage patterns.

You can locate the RegRipper tool by navigating to the directory specified below.

`C:\Tools\DFIR-Data\Tools\RegRipper`

Type the command below to run the `adobe` plugin.

```cmd-session

C:\Tools\DFIR-Data\Tools\RegRipper\rip.exe -r "C:\Tools\DFIR-Data\evidence\017.adobe\NTUSER.DAT" -p adobe

```

The process involves using RegRipper to analyze the `NTUSER.DAT` file. This file is critical as it contains user-specific registry entries, including those related to Adobe software. The key `cRecentFiles` is of particular interest, as it typically holds entries or values representing the PDF files that have been opened or accessed. Each entry includes essential details such as file paths, timestamps, and other metadata that illuminate the user's interaction with Adobe Acrobat DC.

![adobe](https://academy.hackthebox.com/storage/modules/248/pdf-1_.png)

## Analysis using Registry Explorer

Let’s conduct the same analysis, but this time using Registry Explorer.

To begin, locate the `NTUSER.DAT` file using the directory path provided at the start of this section.

`C:\Tools\DFIR-Data\evidence\017.adobe\NTUSER.DAT`

Then, import this file into Registry Explorer. In Registry Explorer, navigate to the relevant Adobe sections to view a list of recently accessed PDF documents, as shown below.

![adobe](https://academy.hackthebox.com/storage/modules/248/pdf1.png)

This will be displayed in different sub-folders within the Registry Explorer interface, providing a comprehensive view of user activities related to Adobe PDF files.


# User's Sticky Notes Forensics

## Introduction

Sticky Notes is a built-in application on Windows that allows users to create and manage virtual sticky notes on their desktop. These digital notes serve as a quick and convenient way for users to jot down reminders, to-do lists, and other important information.

Sticky Notes can be a valuable source of information for user behavior analysis during digital forensics investigations. Examining the content of sticky notes provides insights into the user's activities, tasks, and priorities. Additionally, Sticky Notes often include timestamps or date information, providing a timeline of when certain notes were created or modified. This timeline can be crucial for reconstructing the sequence of user actions, helping investigators understand the temporal aspect of user behavior.

Let's say a user has saved some Sticky Notes in the Windows operating system and has included some secrets and intentions.

![sn1](https://academy.hackthebox.com/storage/modules/248/sn1_.png)

In recent versions of Windows 10 and Windows 11, the sticky notes are stored in the location below inside a file named
`plum.sqlite`.

```path
C:\Users\<Username>\AppData\Local\Packages\Microsoft.MicrosoftStickyNotes_8wekyb3d8bbwe\LocalState

```

![sn2](https://academy.hackthebox.com/storage/modules/248/sn2.png)

During a forensic investigation, examining the user's profile or system files may reveal the presence of Sticky Notes data. The analysis involves examining specific folder entries where Sticky Notes data is stored.

Extracted Sticky Notes data should be analyzed for content, timestamps, and any embedded information. Investigators may use tools or scripts to parse and present the content of sticky notes in a readable format. The information from sticky notes should be correlated with other artifacts, such as the timeline of system events or user logins. This correlation enhances the overall understanding of the user's behavior in a broader context.

* * *

## Examining the sticky notes (plum.sqlite)

Let's navigate to the bottom of this section and click on "Click here to spawn the target system!". Then, let's RDP into the Target IP using the provided credentials. The vast majority of the actions and commands covered from this point up to end of this section can be replicated inside the target, offering a more comprehensive grasp of the topics presented.

Within the target (VM), you can locate the evidence and tools at the following paths:

- **Database file location**: `C:\Tools\DFIR-Data\evidence\011.stickynotes\plum.sqlite`
- **DB Browser for SQLite**: `C:\Program Files\DB Browser for SQLite`
- **StickyParser**: `C:\Tools\DFIR-Data\Tools\StickyParser\stickyparser.py`
- **Python3**: `C:\Tools\DFIR-Data\Tools\Python3`

Note: DB Browser for SQLite also has a desktop shortcut.

* * *

To extract the sticky notes content, we need to examine the underlying database file, often named `plum.sqlite`. To explore this file, we can use a SQLite browser like [DB Browser for SQLite](https://sqlitebrowser.org/).

First, let's download and install DB Browser for SQLite. Go to the official website: [DB Browser for SQLite](https://sqlitebrowser.org/). This is already downloaded on the module's target system.

After opening DB Browser for SQLite, let's locate the database file `plum.sqlite` from the forensic data collected from the system. The path to this file is often in the user's AppData folder. On the module's target workstation, `plum.sqlite` is saved at the path below:

```path
C:\Tools\DFIR-Data\evidence\011.stickynotes\plum.sqlite

```

Click on "Open Database" in the toolbar and navigate to the location of the `plum.sqlite` file, as shown in the screenshot.

![sn3](https://academy.hackthebox.com/storage/modules/248/sn3.png)

Once the database is open, you'll see a list of tables on the left side. The important table in Sticky Notes databases is "Note."

Now, click on "Browse Data" and select the "Note" table, which contains the note content.

![sn4](https://academy.hackthebox.com/storage/modules/248/sn4-1.png)

The "Note" table often contains the actual content of the sticky notes. Examine the columns within the "Note" table to find information such as note content, creation time, and modification time.

**Note 1**:

![sn5](https://academy.hackthebox.com/storage/modules/248/sn5-1_.png)

**Note 2**:

![sn6](https://academy.hackthebox.com/storage/modules/248/sn6-1.png)

Timestamps associated with each note can provide insights into when the note was created or last modified. Look for columns like "CreatedAt" and "UpdatedAt."

![sn7](https://academy.hackthebox.com/storage/modules/248/sn7-1.png)

If needed, we can export data from DB Browser for further analysis or documentation.

![sn8](https://academy.hackthebox.com/storage/modules/248/sn8_.png)

We can also select `File > Export > Table(s) to JSON` to export a large Sticky Notes database content.

* * *

## Parsing the sticky notes

There's an open-source tool called [StickyParser](https://github.com/dingtoffee/StickyParser) that can be used for Sticky Notes forensics. Credits to Elaine Hung ( [@dingtoffee](https://github.com/dingtoffee)) for this tool. It is a simple Windows Sticky Notes parser written in Python, which supports both `.snt` and `.sqlite` formats. Additionally, it can also recover deleted notes from the `plum.sqlite` or any generic SQLite database.

Within the target (VM), you can locate StickyParser at the following path:

`C:\Tools\DFIR-Data\Tools\StickyParser\stickyparser.py`

The database file is saved at the following path:

`C:\Tools\DFIR-Data\evidence\011.stickynotes\plum.sqlite`

We can run the `stickyparser.py` script to open the help menu and see the available options.

```cmd-session

py C:\Tools\DFIR-Data\Tools\StickyParser\stickyparser.py -h

usage: stickyparser.py [-h] [-s [snt file]] [-p [sqlite file]] [-d [File Directory]] [-r [sqlite file]]

StickyParser: Parses sticky note files in legacy snt formats or latest sqlite formats.It can also be used to recover
deleted content inside sqlite. For latest version of StickyNote, please copy everything under the
%LOCALAPPDATA%\Packages\Microsoft.MicrosoftStickyNotes_8wekyb3d8bbw\LocalStatealState Folder. Run StickyPraser against
the copied folder. Make sure the other files apart from the plum.sqlite are all in the same folder. Once run, WAL/SHM
files will be merged into .sqlite file.

options:
  -h, --help           show this help message and exit
  -s [snt file]        Sticky note .snt file. Example: StickyParser.exe -s C:\Users\User\AppData\Roaming\Sticky
                       Notes\StickyNotes.snt. Choose either -s or -p only.
  -p [sqlite file]     Sticky note plum.sqlite file. Example: StickyParse -s <Path>\plum.sqlite. Choose either -s or
                       -p
  -d [File Directory]  Specify the directory where the output should write to. Example: StickyParser -p <path> -d
                       C:\Users\User\Desktop\
  -r [sqlite file]     To recover deleted content from sqlite.

```

The command to parse the SQLite database and extract the sticky notes is shown in the snippet below. This will save the output inside a CSV file in the specified output directory, i.e., `C:\Temp`, in this example.

```cmd-session

py C:\Tools\DFIR-Data\Tools\StickyParser\stickyparser.py -p C:\Tools\DFIR-Data\evidence\011.stickynotes\plum.sqlite -d C:\Temp

StickyPraser: Parsing the sqlite file ....
StickyParser: Saving the csv file
StickyParser: File saved.

```

The output CSV file indicates that the parsing was successful and displays the sticky notes content, as shown in the screenshot below.

![sn10](https://academy.hackthebox.com/storage/modules/248/sn10_.png)


# Archive history

Let's navigate to the bottom of this section and click on "Click here to spawn the target system!". Then, let's RDP into the Target IP using the provided credentials. The vast majority of the actions and commands covered from this point up to end of this section can be replicated inside the target, offering a more comprehensive grasp of the topics presented.

Within the target (VM), you can locate the evidence and tools at the following paths:

- **NTUSER.DAT file location**: `C:\Tools\DFIR-Data\evidence\018.archive_history\NTUSER.DAT`
- **Registry Explorer location**: `C:\Tools\DFIR-Data\Tools\EZ-Tools\net6\RegistryExplorer`
- **RegRipper location**: `C:\Tools\DFIR-Data\Tools\RegRipper`

If you're not able to view the `NTUSER.DAT` file, make sure that the hidden files are shown in the File Explorer.

* * *

## Introduction

The archive history provides a record of files that the user compressed or archived. This information helps forensic analysts understand the user's file-related activities, including which files were considered important enough to be archived.

Examining archive history helps identify whether users have been attempting to hide, compress, or transfer files that could be relevant to an investigation. Unusual or unexpected archive activities may warrant further scrutiny, as users might use compression tools to exfiltrate or conceal sensitive information.

Let's take a scenario where a user used the WinZip utility to extract the contents from an archive. The information can be extracted from the registry location below.

- **Artifact File**: `NTUSER.DAT`
- **Extracted Files list**: `SOFTWARE\WinZip Computing\WinZip\extract`
- **Extracted Files Info**: `SOFTWARE\WinZip Computing\WinZip\mru\archives`

This registry key is specific to the WinZip tool, which is used to create compressed files or unzip archives.

## Analysis using Registry Explorer

To open WinZip archive information with Registry Explorer, navigate to the user's `NTUSER.DAT` file you want to analyze. is file is typically located in the user's profile directory, for example, `C:\Users\Username\NTUSER.DAT`. For demonstration, we have saved the `NTUSER.DAT` file at the path as mentioned below.

`C:\Tools\DFIR-Data\evidence\018.archive_history\NTUSER.DAT`

Navigate to `SOFTWARE\WinZip Computing\WinZip\extract`

For example, the screenshot below shows an example of extracted files:

![zip](https://academy.hackthebox.com/storage/modules/248/zip-0.png)

The `SOFTWARE\WinZip Computing\WinZip\mru\archives` path contains more information about the extracted files.

![zip](https://academy.hackthebox.com/storage/modules/248/zip-1.png)

The values starting with `xd` (such as `xd0`, `xd1`, and so on) seem to list file names, possibly indicating files that are being managed or archived by WinZip. This is a useful artifact that can provide information related to the files contained in the archive.

![zip](https://academy.hackthebox.com/storage/modules/248/zip-2.png)

Similarly, the next archive file, `pictures.zip`, contains the files `picture1.png` and `picture2.png` inside it, as shown in the screenshot below.

![zip](https://academy.hackthebox.com/storage/modules/248/zip-3.png)

## Archive Analysis using RegRipper

This information can also be extracted using the RegRipper plugin `winzip`. This plugin helps retrieve WinZip extract and file menu values. The command to run the WinZip plugin in RegRipper is as follows:

```cmd-session

C:\Tools\DFIR-Data\Tools\RegRipper\rip.exe  -r "C:\Tools\DFIR-Data\evidence\018.archive_history\NTUSER.DAT" -p winzip

```

![zip](https://academy.hackthebox.com/storage/modules/248/zipreg1.png)

RegRipper also provides metadata information related to the file names contained in the archive.

![zip](https://academy.hackthebox.com/storage/modules/248/zipreg2.png)

Similarly, there are RegRipper plugins for `7-zip` and `WinRAR` as well.

![zip1](https://academy.hackthebox.com/storage/modules/248/zip1.png)

Forensic analysts can leverage archive history to gain a comprehensive view of user behavior, identify potential security incidents, and build a robust case based on digital evidence.

* * *

`Note:` The steps below are informational and should help you understand more about RegRipper plugins and modify them whenever necessary.

## Working with RegRipper Plugins

The [RegRipper](https://github.com/keydet89/RegRipper3.0) tool is driven by its plugin [files](https://github.com/keydet89/RegRipper3.0/blob/master/plugins) written in [Perl](https://en.wikipedia.org/wiki/Perl). Sometimes, it is possible that the RegRipper plugins contain locations that have been changed by software vendors. In such cases, the plugin files can be easily modified to make them work.

For example, the default plugin [file](https://github.com/keydet89/RegRipper3.0/blob/master/plugins/winzip.pl#L41) for WinZip refers to the registry key path as `Software\Nico Mak Computing\WinZip`.

![zip1](https://academy.hackthebox.com/storage/modules/248/zipregpl1.png)

If we run RegRipper ( `rip.exe`) with this plugin, it shows an output indicating that the key is not found.

![zip1](https://academy.hackthebox.com/storage/modules/248/winziperr.png)

It happened because this version of WinZip uses a different registry location.

To fix this, simply replace the key path and names with the updated values. First, navigate to the plugins directory in the RegRipper folder.

![zip1](https://academy.hackthebox.com/storage/modules/248/plugins1.png)

First, we will replace the registry key path with the updated path.

![zip1](https://academy.hackthebox.com/storage/modules/248/zipregpl2.png)

Look for other keys and sub-keys to see if there's any change. For example, `extract` is same and needs no change.

![zip1](https://academy.hackthebox.com/storage/modules/248/zipregpl3.png)

The `filemenu` sub-key is replaced with `fm` in this version, so we can replace this sub-key accordingly.

![zip1](https://academy.hackthebox.com/storage/modules/248/zipregpl4.png)

If we run RegRipper ( `rip.exe`) with the updated plugin now, it should return the information.

![zip1](https://academy.hackthebox.com/storage/modules/248/winzipwrk.png)

Similarly, we can replace keys or sub-keys in other plugins where required. We can also create a new plugin if we identify an interesting artifact in registry keys.


# Command-line history forensics

Command history reveals the operations executed by a user, shedding light on their activities and intentions. Identification of scripted commands or PowerShell scripts in the history can indicate automated or orchestrated actions. Analyzing command patterns can unveil regular tasks, preferences, or unusual activities that might be of forensic interest. Additionally, unusual or unauthorized commands may suggest security threats, including attempts to access sensitive data or compromise the system.

* * *

## Saved powershell command history analysis

PowerShell has a history navigation feature that enhances the command line editing experience. The command history allows users to view, search, and execute previously entered commands. This command history is particularly useful for forensic analysis, as it records the commands executed by users.

* * *

## Location of PSReadline History File:

The PSReadline history file is usually located in the user's profile directory. The default path is:

```powershell
C:\Users\<Username>\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadline\ConsoleHost_history.txt

```

![cmd1](https://academy.hackthebox.com/storage/modules/248/cmd1.png)

This file contains the PowerShell commands executed by the user. The best part is that PSReadline saves command history between sessions, making it persistent across multiple PowerShell sessions.

![cmd2](https://academy.hackthebox.com/storage/modules/248/cmd2_.png)

One thing to note is that the `Clear-History` cmdlet in PowerShell is responsible for clearing the in-memory command history within the current session. It removes the command entries from the history buffer, but it does not delete or modify the PSReadline command history file stored on disk.

KAPE also has a target already included for PSReadline command history.

![cmd3](https://academy.hackthebox.com/storage/modules/248/cmd3.png)

The description of this target shows the path of the console history file.

![cmd4](https://academy.hackthebox.com/storage/modules/248/cmd4.png)

Within the target (VM), you can locate the console history file (extracted using KAPE) at the following path:

`C:\Tools\DFIR-Data\evidence\012.cmd-history\ConsoleHost_history.txt`

Forensically, analyzing the PSReadline command history can reveal insights into the commands executed by users, their scripting activities, and potentially malicious actions. It's a valuable artifact for understanding user behavior and identifying any security-related events or anomalies within a PowerShell environment.


# User's Clipboard Data

## Introduction

This topic involves the examination of information stored in the system clipboard, which is used by users to temporarily store data during copy and paste operations. Analyzing clipboard data can provide insights into user activities and potentially uncover sensitive information. Users often copy and paste passwords, usernames, and other login credentials, which attackers can capture to gain unauthorized access to accounts.

In addition to credentials, clipboard data might include credit card numbers, banking information, or other financial details that can be used for fraud or theft. Information such as social security numbers, addresses, phone numbers, and other personally identifiable information (PII) can be harvested for identity theft. In a business environment, users might copy and paste sensitive corporate documents, proprietary data, or internal communications. This can provide attackers with valuable intelligence or leverage for industrial espionage. Therefore, the clipboard is a valuable target for attackers.

Clipboard data is typically stored in volatile memory, making it essential to acquire a memory dump for analysis. Here's a good [blogpost](https://xret2pwn.github.io/The-Art-of-Clipboard-Forensics-Recovering-Deleted-Data/) that researches this topic related to users' clipboard data.

When we press `Win + V`, it opens the clipboard with the data copied by the user. The screenshot below shows what the clipboard history looks like.

![clip1](https://academy.hackthebox.com/storage/modules/248/clip1.png)

From the research published in the [blog](https://xret2pwn.github.io/The-Art-of-Clipboard-Forensics-Recovering-Deleted-Data/), we can verify that clipboard data is also stored in the memory of `TextInputHost.exe`.

The file `TextInputHost.exe` is a legitimate Windows process associated with the input methods and keyboard functionality. It is part of the Windows operating system and is responsible for handling various text input tasks, including managing input methods for different languages and keyboard layouts.

In [Process Hacker](https://processhacker.sourceforge.io/), if we filter the strings in the memory of the process `TextInputHost.exe`, we can see the clipboard data stored. Even if we delete the clipboard data from the clipboard, it remains in the memory of `TextInputHost.exe`.

![clip2](https://academy.hackthebox.com/storage/modules/248/clip2.png)

Remember that clipboard data is volatile and may get overwritten quickly. Timely acquisition of memory dumps and efficient analysis are crucial for successful clipboard forensics.

* * *

**Note:** The clipboard history feature is not available on the lab VM since it is running Windows Server 2019.

The clipboard history feature is available on Windows 10/11, as shown in the screenshot below. On Windows 10/11, the clipboard history can be enabled by pressing the Windows logo key + V.

![clip2](https://academy.hackthebox.com/storage/modules/248/cliboard-win.png)

Below is a demonstration of this section where text is copied into the clipboard and is present in the memory of the `TextInputHost.exe` process.

![clip2](https://academy.hackthebox.com/storage/modules/248/clipboard.gif)

* * *


# Saved SSH Keys And Server Info (Putty)

## Introduction

[PuTTY](https://en.wikipedia.org/wiki/PuTTY) is a popular SSH client that stores the cryptographic host keys associated with SSH servers. Analyzing these keys can be crucial in forensic investigations, providing details about the servers a user has connected to, potentially shedding light on their network activities and the security posture of the systems involved.

This information resides in the `NTUSER.DAT` hive, under the registry path below:

```regpath

Software\SimonTatham\PuTTY\SshHostKeys

```

The screenshot below shows how this information is stored in the registry:

![ssh2](https://academy.hackthebox.com/storage/modules/248/ssh2.png)

Let's navigate to the bottom of this section and click on "Click here to spawn the target system!". Then, let's RDP into the Target IP using the provided credentials. The vast majority of the actions and commands covered from this point up to end of this section can be replicated inside the target, offering a more comprehensive grasp of the topics presented.

Within the target (VM), you can locate the evidence and tools at the following paths:

- **NTUSER.DAT file location**: `C:\Tools\DFIR-Data\evidence\014.sshHostKeys\NTUSER.DAT`
- **RegRipper location**: `C:\Tools\DFIR-Data\Tools\RegRipper`

If you're not able to view the `NTUSER.DAT` file, make sure that the hidden files are shown in the File Explorer.

* * *

## Putty plugin in RegRipper

RegRipper also offers insights into artifacts related to PuTTY. Specifically, RegRipper can extract valuable information from the Windows registry, such as the saved `SshHostKeys` for PuTTY. RegRipper processes the `NTUSER.DAT` file and extracts PuTTY session and host key information. The output displays saved sessions and known SSH host keys.

The snippet below shows the command to run the `putty` plugin in RegRipper:

```cmd-session

C:\Tools\DFIR-Data\Tools\RegRipper\rip.exe -r "C:\Tools\DFIR-Data\evidence\014.sshHostKeys\NTUSER.DAT" -p putty

```

This example output shows that the user interacted over SSH with the remote machine at IP `10.10.10.4` on port 22. TThe session information reveals the remote systems the user has connected to, along with configuration details such as port numbers and user names.

![ssh1](https://academy.hackthebox.com/storage/modules/248/ssh1-1_.png)

This [blog post](https://blog.didierstevens.com/2021/03/27/filezilla-uses-puttys-registry-fingerprint-cache/) from Didier Stevens demonstrates that [FileZilla](https://en.wikipedia.org/wiki/FileZilla) uses PuTTY’s registry fingerprint cache. FileZilla is a free and open-source, cross-platform FTP application that can also connect to SFTP servers.

The screenshot below from the blog post shows that FileZilla uses PuTTY‘s registry key to cache SSH fingerprints.

![ssh1](https://academy.hackthebox.com/storage/modules/248/ssh_ds_1.png)

This means that if we investigate this registry location, we should be able to get the SSH fingerprints cached by FileZilla as well.

* * *


# Terminal Server History (tsclient)

## Introduction

To view the user's patterns in terms of visited remote servers, we can examine the Terminal Server Client's MRU (Most Recently Used) registry keys, which store the RDP connection history. Terminal Server Client (tsclient) is used to connect to remote systems via Remote Desktop Protocol (RDP). Analyzing tsclient artifacts can provide valuable information about remote connections and sessions established from a Windows system. These artifacts are stored in the Windows registry and can be extracted and analyzed during a forensic investigation.

- **File**: `NTUSER.DAT`
- **Location**: `Software\Microsoft\Terminal Server Client\Default`

Let's navigate to the bottom of this section and click on "Click here to spawn the target system!". Then, let's RDP into the Target IP using the provided credentials. The vast majority of the actions and commands covered from this point up to end of this section can be replicated inside the target, offering a more comprehensive grasp of the topics presented.

Within the target (VM), you can locate the evidence and tools at the following paths:

- **NTUSER.DAT file location**: `C:\Tools\DFIR-Data\evidence\016.tsclient\NTUSER.DAT`
- **Registry Explorer location**: `C:\Tools\DFIR-Data\Tools\EZ-Tools\net6\RegistryExplorer`
- **RegRipper location**: `C:\Tools\DFIR-Data\Tools\RegRipper`

If you're not able to view the `NTUSER.DAT` file, make sure that the hidden files are shown in the File Explorer.

* * *

To explore this information, we can open Registry Explorer and load the hive from the path below:

`C:\Tools\DFIR-Data\evidence\016.tsclient\NTUSER.DAT`

The screenshot below shows a view of Registry Explorer where this registry key is opened.

![rdp](https://academy.hackthebox.com/storage/modules/248/rdp.png)

This contains a list of servers to which a user connected using the Terminal Server Client. It contains two values: `CertHash` and `UsernameHint`.

![rdp1](https://academy.hackthebox.com/storage/modules/248/rdp1.png)

- `CertHash` likely refers to a certificate hash associated with the Terminal Server Client. Certificates are often used in secure connections, and a hash of a certificate could be stored for authentication or verification purposes.

- `UsernameHint` is designed to help users remember or identify their usernames more easily during the login process. The `UsernameHint` value might offer insights into which credentials are used by the user to log in to remote servers. Analyzing this could be valuable for understanding user behavior, especially in the context of authentication.


## Analyzing Terminal Server Client (tsclient) Artifacts with RegRipper

RegRipper provides the `tsclient` [plugin](https://github.com/keydet89/RegRipper3.0/blob/master/plugins/tsclient.pl) that can extract information from this registry location. This plugin extracts and interprets data from these registry entries, providing valuable information to forensic investigators about the user's interaction with remote servers.

Type the command below to run the `tsclient` plugin.

```cmd-session

C:\Tools\DFIR-Data\Tools\RegRipper\rip.exe -r "C:\Tools\DFIR-Data\evidence\016.tsclient\NTUSER.DAT" -p tsclient

```

The `tsclient` plugin will extract the contents of the user's Terminal Server Client key, as shown in the screenshot below.

![rdp2](https://academy.hackthebox.com/storage/modules/248/rdp2-1.png)

The MRU list and server entries reveal the remote systems the user has connected to, along with connection frequencies. The `UserNameHint` value indicates the usernames used to connect to remote systems, providing context on user activity. The `CertHash` values help verify the authenticity of the remote systems, ensuring the connections were to trusted endpoints. By examining MRU lists and server configurations, forensic investigators can gather crucial information about a user's remote activities and configurations, aiding in comprehensive behavioral analysis and incident investigations.


# ActivityCache.db

## Introduction

Windows Activity History is a feature that tracks user activities on a Windows system, capturing details about applications used, files opened, and more. In the context of digital forensics, analyzing Windows Activity History provides insights into a user's actions over time. This information is stored in a database, often referred to as the Activity Cache.

![timeline0](https://academy.hackthebox.com/storage/modules/248/timeline0.png)

The `ActivityCache.db` file maintains a record of user activities and executed programs. Analyzing the `ActivityCache.db` file can provide insights into the applications used by a user, execution frequencies, and potentially reveal user behavior patterns.

* * *

## Location of ActivityCache.db

The `ActivityCache.db` file is typically located in the user's profile directory. The exact path is:

```path
%userprofile%\appdata\local\ConnectedDevicesPlatform\L

```

Inside this directory, there's a folder with a name starting with "L" that contains the `ActivityCache.db` file.

An SQLite database viewer can be used to analyze the `ActivityCache.db` file.

We can look for tables or views within this database. Key tables often include `Activity`, `Resource`, `DestList`, etc. The `Activity` table is crucial and contains information about executed programs. Columns such as `Id`, `Timestamp`, `Title`, `AppId`, and `InstanceId` are noteworthy. We should examine timestamps to understand when applications were executed.

Within the target (VM), you can locate the `ActivitiesCache.db` evidence file (extracted from KAPE's output) at the followting path:

`C:\Tools\DFIR-Data\evidence\015.activityCache\ActivitiesCache.db`

* * *

## Analysis using WxTCmd

* * *

Let's navigate to the bottom of this section and click on "Click here to spawn the target system!". Then, let's RDP into the Target IP using the provided credentials. The vast majority of the actions and commands covered from this point up to end of this section can be replicated inside the target, offering a more comprehensive grasp of the topics presented.

Within the target (VM), you can locate the evidence and tools at the following paths:

- **ActivitiesCache file location**: `C:\Tools\DFIR-Data\evidence\015.activityCache\ActivitiesCache.db`
- **Timeline Explorer location**: `C:\Tools\DFIR-Data\Tools\EZ-Tools\net6\TimelineExplorer`
- **RegRipper location**: `C:\Tools\DFIR-Data\Tools\RegRipper`
- **WxTCmd Location**: `C:\Tools\DFIR-Data\Tools\EZ-Tools\net6\WxTCmd.exe`

* * *

WxTCmd is another tool by Eric Zimmerman designed to parse and analyze the Windows 10 Timeline feature database. The Windows 10 Timeline feature allows users to review and resume their recent activities across multiple devices. It provides a chronological view of the user's activities, such as opened documents, visited websites, and other interactions with applications.

The command shown below can be used to parse the `ActivityCache.db` file.

```powershell
PS C:\Tools\DFIR-Data\Tools\EZ-Tools\net6> .\WxTCmd.exe -f C:\Tools\DFIR-Data\evidence\015.activityCache\ActivitiesCache.db --csv C:\tmp

```

where `-f` specifies the `ActivitiesCache.db` file and `--csv` is used to specify the directory for the output, which contains the parsed files.

The screenshot below shows the output of this command:

![timeline](https://academy.hackthebox.com/storage/modules/248/timeline-1.png)

WxTCmd is developed to extract information from the Windows 10 Timeline database, enabling forensic investigators and analysts to examine a user's activity history. By analyzing the data collected by WxTCmd, investigators can gain insights into the user's behavior, applications used, and the timeline of their activities on the system. This tool shows activities in great detail, as demonstrated in the screenshot below, where `notepad.exe` is used to open a file named `users.txt`. The activity type is "ExecuteOpen."

![timeline1](https://academy.hackthebox.com/storage/modules/248/timeline1.png)

Apart from "ExecuteOpen," there are other activity types that can also provide valuable information.

![timeline2](https://academy.hackthebox.com/storage/modules/248/timeline2.png)

Activities are categorized into different types, each representing a specific user action, such as below:

- **ExecuteOpen**: This activity type is created when a user opens an application or application package for the first time. For example, opening `Notepad.exe` would generate this type of activity. The associated file name is stored in the DisplayText field, and the full path of the opened file is in the ContentInfo field.

- **InFocus**: This activity type occurs when a user focuses on a previously opened application or file. The Duration field specifies how long the user interacted with the application. In the example, the user opened the file `invoice.xlsm` using Excel, and the interaction lasted for 3 seconds.

- **Copy/Paste**: This activity type represents a copy or paste operation. Unfortunately, the Payload field might not be available, and there used to be a reference to Base64-encoded text copied to the clipboard in the ClipboardPayload field, which is not available in recent versions.


These activity types provide insights into user interactions, application usage, and clipboard operations, contributing to a comprehensive timeline of user behavior on the system.

![timeline3](https://academy.hackthebox.com/storage/modules/248/timeline3.png)

### Browsing History in ActivityCache.db

Investigators can look for information related to websites browsed by users in the `ActivityCache.db` file, which can help in understanding user behavior to some extent. The screenshot below provides an example of the websites browsed by the user, where they are trying to perform some searches on Google related to data-stealing activity.

![timeline3](https://academy.hackthebox.com/storage/modules/248/activity-br.png)

**Note:** The information shown in the last screenshot is from the `ActivitiesCache.db` file stored at the path below:

`C:\Tools\DFIR-Data\evidence\skills-assessment\D\Users\gary\AppData\Local\ConnectedDevicesPlatform\L.gary`


# USB Devices

## Introduction

USB Devices Forensics involves examining information related to USB devices connected to a system. This information is typically stored in the Windows Registry and can be valuable in forensic investigations.

When a user plugs a USB device into the computer, the device is assigned a unique device ID by the Windows OS. This device ID is stored in the Windows Registry, under the key `HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Enum\USB`. This registry key contains information about all USB devices that have been connected to the computer, including the device ID, vendor ID, product ID, and other details about the device.

Information about USB devices is stored in the Windows Registry at the location mentioned below.

```regpath
Computer\HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Enum\USB

```

The screenshot below shows how this information looks in the registry:

![usb2](https://academy.hackthebox.com/storage/modules/248/usb2.png)

The `Enum\USB` Registry key contains subkeys that represent individual USB devices. Each device subkey holds information such as the name, Vendor ID, Product ID, Hardware ID, and other details.

Information about storage devices, including hard disks connected via USB, can also be part of USB device forensics. Examining device entries may reveal details about connected external storage media.

If a user tries to attach an external hard disk, it will be stored in the `SCSI` subkey.

![usb1](https://academy.hackthebox.com/storage/modules/248/usb1.png)

## Analysis of USBSTOR Key

Let's navigate to the bottom of this section and click on "Click here to spawn the target system!". Then, let's RDP into the Target IP using the provided credentials. The vast majority of the actions and commands covered from this point up to end of this section can be replicated inside the target, offering a more comprehensive grasp of the topics presented.

Within the target (VM), you can locate the evidence and tools at the following paths:

- **Registry Explorer location**: `C:\Tools\DFIR-Data\Tools\EZ-Tools\net6\RegistryExplorer`
- **RegRipper location**: `C:\Tools\DFIR-Data\Tools\RegRipper`
- **SYSTEM file location**: `C:\Tools\DFIR-Data\evidence\019.usb-devices\exercise\SYSTEM`
- **LNK File**: `C:\Tools\DFIR-Data\evidence\019.usb-devices\exercise\Board Presentation.LNK`

* * *

There is another registry key, `USBSTOR` , in the Windows Registry that contains information about USB storage devices that have been connected to the computer, such as USB flash drives.

The key is located at `HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Enum\USBSTOR`. We can see a list of USB storage devices connected to the system in the `USBSTOR` registry path.

Load the SYSTEM hive into Registry Explorer from the path below.

`C:\Tools\DFIR-Data\evidence\019.usb-devices\exercise\SYSTEM`

![usb1](https://academy.hackthebox.com/storage/modules/248/usb-device.png)

For forensic investigations, the timestamps regarding USB device connect and disconnect events are very important. Fortunately, we can see this information in the registry as well.

The screenshot below shows the device connect timestamp.

![usb1](https://academy.hackthebox.com/storage/modules/248/usb-connect.png)

The screenshot below shows the device disconnect timestamp.

![usb1](https://academy.hackthebox.com/storage/modules/248/usb-disconnect.png)

Tools like Registry Explorer, RegRipper, or custom scripts can be employed for parsing and extracting USB device information.

This can be verified using RegRipper as well. RegRipper has plugins related to USB devices. For example, the
`usb` plugin is used to get the contents of a user's USB key.

The screenshot below shows the USB-related plugins in RegRipper:

![usb1](https://academy.hackthebox.com/storage/modules/248/regripusb.png)

Let's try using the `usbstor` plugin to get information from the SYSTEM file.

```cmd-session
C:\> C:\Tools\DFIR-Data\Tools\RegRipper\rip.exe -r "C:\Tools\DFIR-Data\evidence\019.usb-devices\exercise\SYSTEM" -p usbstor

```

![usb1](https://academy.hackthebox.com/storage/modules/248/regripusbstor.png)

## Check files accessed from USB Device

Suppose a user tries to open a file from a USB device. In that case, we can look into the Recent files for any interesting LNK files. For example, we acquired an LNK file found on a workstation in the user's `AppData\Roaming\Microsoft\Windows\Recent`.

This file is saved at the path below on the module's target system:

```path
C:\Tools\DFIR-Data\evidence\019.usb-devices\exercise\Board Presentation.LNK

```

If we parse the `Board Presentation.lnk` LNK file using `LECmd.exe` from Eric Zimmerman's tools, we can see USB-related information in the device information. The command to parse the LNK file using the `LECmd.exe` tool is provided below.

```cmd-session
C:\> C:\Tools\DFIR-Data\Tools\EZ-Tools\net6\LECmd.exe -f "C:\Tools\DFIR-Data\evidence\019.usb-devices\exercise\Board Presentation.lnk"

...SNIP...

--- Header ---
  Target created:  2022-02-28 17:53:15
  Target modified: 2022-02-28 16:59:24
  Target accessed: 2022-02-28 17:53:19

  File size (bytes): 8,461
  Flags: HasTargetIdList, HasLinkInfo, HasWorkingDir, IsUnicode, DisableKnownFolderTracking
  File attributes: FileAttributeArchive
  Icon index: 0
  Show window: SwNormal (Activates and displays the window. The window is restored to its original size and position if the window is minimized or maximized.)

Working Directory: E:\

--- Link information ---
Flags: VolumeIdAndLocalBasePath

>> Volume information
  Drive type: Removable storage media (Floppy, USB)
  Serial number: 6C183CE6
  Label: (No label)
  Local path: E:\Board Presentation.pdf

--- Target ID information (Format: Type ==> Value) ---

  Absolute path: My Computer\E:\Board Presentation.pdf

  -Root folder: GUID ==> My Computer

  -Drive letter ==> E:

...SNIP...

```

The screenshot below shows an example of an LNK file, which indicates that a file from a USB device was accessed by a user.

![usb1](https://academy.hackthebox.com/storage/modules/248/usblnk.png)

USB device information is crucial in forensic investigations to establish a timeline of connected devices. It helps identify when specific USB devices were connected or disconnected from the system and what happened during the period when the device was connected.

We can further correlate USB-related information with other artifacts such as LNK files, shellbags, Jump Lists, and the `ActivityCache.db` file to gather more information and context. For example, if a user tries to exfiltrate data from the system to a USB device, we can gather information such as when a device is connected/disconnected (registry hive), when files were copied/pasted to the USB device ( `ActivityCache.db`), and any files from the USB drive that were accessed (LNK files), and so on.


# Skills Assessment

You are working as a DFIR analyst in your organization. Upon identifying some signs of data exfiltration, the SOC manager has tasked you with conducting a forensic investigation. The alert mentioned that data is being exfiltrated to a USB stick.

Within the target (VM), you can locate the evidence and tools at the following paths:

- `C:\Tools\DFIR-Data\evidence\skills-assessment\`

You need to verify whether the external device was connected by the user. If yes, figure out the timeline for these activities and answer the questions below.

* * *


