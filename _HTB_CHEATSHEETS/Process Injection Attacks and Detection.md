## Sample Program Locations

|Path | Description|
|-|-|
| `C:\injection\local\local_shellcode_inj.exe`|Local Injection|
| `C:\injection\htbdll.dll`|Sample HTB DLL|
| `C:\injection\remote\injection1.exe`|Remote Injection|
| `C:\injection\threadhijacking\threadhijacking.exe`|TEH Injection Sample|
| `C:\injection\apc\apcinjection.exe`|APC Injection|
| `C:\injection\mapview\mapview_remote.exe`|Map View Injection|
| `C:\injection\pe\peinjection.exe`|PE Injection|
| `C:\injection\hollow\hollow.exe`|Process Hollowing tool|
| `C:\injection\hollow\demo\Hollow.exe`| Hollow Sample|

## Tools Usage

|Command| Description|
|-|-|
| `C:\injection\tools\Moneta64.exe -m ioc -p 1234` | Moneta - Enumerate only regions related to suspicious memory| 
| `C:\injection\tools\pe-sieve64.exe /shellc 3 /pid 1234`| PE-Sieve - Scan the process memory for signs of a shellcode| 
| `Invoke-AtomicTest T1055.002 -ShowDetails` | Check the details of a specific MITRE technique eg. T1055.002|
| `Invoke-AtomicTest T1055.002` | Execute Atomic Test with ID T1055.002|
| `msfvenom --platform windows --arch x64 -p windows/x64/exec CMD=calc.exe -e x64/xor -f c -v shellcode` | Generate msfvenom Shellcode to execute calculator app| 
| `x86_64-w64-mingw32-gcc <program.c> -o <output.exe> -m64 -s`| Compile a C program into exe file|
| `x86_64-w64-mingw32-gcc -shared -o <output.dll> <program.c> -m64 -s`| Compile a c program into DLL file|

## WinDbg Commands

| Command	| Description |
|-|-|
| `.hh`	| Opens the debugger help documentation|
| `dt [-rN] [type] <addr>`	| Displays type information for a symbol or structure at the specified address; -rN for recursion depth.|
| `dt _PEB <address>`	| Display details of the PEB structure|
| `dt _EPROCESS <address>`	| Display details of the EPROCESS structure|
| `!peb`	| Show the Process Environment Block (PEB)|
| `!teb`	| Show the Thread Environment Block (TEB)|
| `!process 0 0` | List all active processes|
| `??`	| Evaluates and displays a C++ expression.|
| `? [-rN] <expr>`	| Evaluates and displays a MASM expression; -rN for recursion depth.|
| `poi(<addr>)`	| Dereferences and displays the pointer at the specified address.|
| `lm`	|List all loaded modules in the process|
| `u <address>`|	Disassemble instructions at a given memory address|
| `bp <address>`|	Set a breakpoint at a memory address|
| `bl`	| List all active breakpoints|

## WINAPI/NTAPI Functions Reference

| Command	| Description |
|-|-|
| `OpenProcess`| Get a handle to a target process|
| `VirtualAllocEx`| Allocate memory in a remote process|
| `WriteProcessMemory`| Write shellcode to the remote process|
| `CreateRemoteThread`| Create a thread in a remote process|
| `QueueUserAPC`| Inject an asynchronous procedure call (APC)|
| `NtQueueApcThread`| NTAPI variant for queuing an APC|
| `NtAllocateVirtualMemory`| Allocate memory using NTAPI|
| `NtWriteVirtualMemory`| Write memory using NTAPI|
| `NtProtectVirtualMemory`| Change memory protection of a region|
| `NtCreateThreadEx`| Create a remote thread using NTAPI|
| `SetThreadContext`| Modify thread execution context (used in thread hijacking)|
| `SuspendThread`| Pause a thread in a remote process|
| `ResumeThread`| Resume execution of a suspended thread|
| `ZwUnmapViewOfSection`| Unmap memory from a process (used in Process Hollowing)|

## Windows Security Event IDs Reference

| Event ID	| Description | Detection Use Case |
|-|-|-|
| `4688`| Process Creation	|Detect suspicious processes|
| `4656`| Handle Requested for an Object	|Detect OpenProcess|
| `4657`| Registry Modification	|Look for persistence mechanisms|
| `4663`| Access Attempt on an Object	|Track process injections|
| `4697`| Service Installation	|Detect malware persistence|
| `7034`| Service Unexpectedly Terminated	|Look for process crashes|
| `7045`| New Service Installed	|Detect unauthorized services|
| `6005`| Event Log Service Started	|Identify system restarts|
| `6006`| Event Log Service Stopped	|Detect suspicious shutdowns|


## Sysmon Event IDs for Detection

| Event ID	| Description |
|-|-|
| `Sysmon ID 1`|	Process creation|
| `Sysmon ID 3`|	Network connection detected|
| `Sysmon ID 7`|	Image loaded|
| `Sysmon ID 8`|	CreateRemoteThread detected|
| `Sysmon ID 10`|	Process access via OpenProcess|
| `Sysmon ID 11`|	File creation time change|
| `Sysmon ID 13`|	Registry key modification|
| `Sysmon ID 17`|	Pipe creation|

## Tools Location in the Target (VM)

| Name	| Path| 
|-|-|
| `API Monitor`|	C:\Program Files\rohitab.com\API Monitor\apimonitor-x64.exe|
| `x64dbg`|	C:\Tools\x64dbg\release\x64\x64dbg.exe|
| `SysinternalsSuite`|	C:\Tools\SysinternalsSuite|
| `ProcessHacker`|	C:\Tools\ProcessHacker\ProcessHacker.exe|
| `Moneta`|	C:\Tools\Moneta64.exe|
| `PE-Sieve`|	C:\Tools\pe-sieve64.exe|
| `Atomic Red Team`|	C:\AtomicRedTeam\invoke-atomicredteam|