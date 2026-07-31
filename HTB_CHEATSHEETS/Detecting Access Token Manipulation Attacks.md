|Command|Description|
|--|--|
|`C:\Tools\SysinternalsSuite\logonsessions64.exe -p`|Enumerate processes running in each session.|
|`C:\tools\token-enumeration.exe`|Token enumeration.|
|`C:\Tools\Tokenvator.exe`|Enabling privileges.|
|`Enable_Privilege /Privilege:SeBackupPrivilege`|Enables the `SeBackupPrivilege` through `Tokenvator.exe`.|
|`dt nt!_EPROCESS`|Display the type information for the EPROCESS structure in WinDbg.|
|`dt nt!_PS_PROTECTION`|Display the layout and members of the `_PS_PROTECTION` structure in WinDbg.|
|`dt nt!_PS_PROTECTED_TYPE`|Display the information about the `_PS_PROTECTED_TYPE` structure in WinDbg.|
|`dt nt!_PS_PROTECTED_SIGNER`|Display the signer of a protected process in WinDbg.|
|`!process 0 0 <process>.exe`|Inspecting a running process in WinDbg.|
|`dt nt!_SECURITY_DESCRIPTOR`|Displays the contents of the `_SECURITY_DESCRIPTOR` structure in WinDbg.|
|`Install-Module NTObjectManager`|Installs the NTObjectManager PowerShell module.|
|`Show-NtToken -All`|Open Token Viewer.|
|`Get-NtTokenPrivilege`|Retrieves the privileges of a token.|
|`Get-NtToken -ProcessId 2144`|Retrieves the token information of a target process.|