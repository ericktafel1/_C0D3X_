# Log  
```powershell
dir 'C:\windows\System32\winevt\Logs\Microsoft-Windows-Windows Defender%4Operational.evtx'  
```
  
# check if in log  
```powershell
Get-WinEvent -LogName "Microsoft-Windows-Windows Defender/Operational" -Oldest | Where-Object { $_.LevelDisplayName -ne "Information" }   
```
  
# more info for analysis  
```powershell
Get-WinEvent -LogName "Microsoft-Windows-Windows Defender/Operational" -Oldest | Where-Object { $_.LevelDisplayName -ne "Information" } | Select-Object -ExpandProperty Message  
```
  
# Disable Defender  
```powershell
Set-MpPreference -DisableRealtimeMonitoring $true  
```
  
# Enable Defender  
```powershell
Set-MpPreference -DisableRealtimeMonitoring $false  
```
  
# Add defender exception  
```powershell
Set-MpPreference -ExclusionPath 'C:\Windows\Temp'  
```
  
# Remove Defender exception  
```powershell
Remove-MpPreference -ExclusionPath 'C:\Windows\Temp'  
```
  
# Get event log  
```powershell
Get-EventLog -LogName System -Source 'Service Control Manager' -Newest 5  
```
  
# Registry Keys to Disable Defender that beats tamper protection.. requires restart  
```powershell
reg add "HKLM\Software\Policies\Microsoft\Windows Defender" /v DisableAntiSpyware /t reg_dword /d 1 /f  
```
  
```powershell
reg query "HKLM\Software\Policies\Microsoft\Windows Defender/DisableAntiSpyware"
```
  
```powershell
reg delete "HKLM\Software\Policies\Microsoft\Windows Defender" /v DisableAntiSpyware /f
```