# Run nmap enumeration scripts  
nmap -sC -sV -T4 -Pn -p 80,443 ip  
  
# fuzz recursively   
feroxbuster --url http://analytical.htb -C 404  
  
# Identify Web App Technology  
whatweb -a3 http://website.com -v  
  
# Run nikto   
nikto -host http://website.com  
  
# if Wordpress  
wpscan --url http://website.com  
  
# Look for changelogs  
curl http://website.com/CHANGELOG  
curl http://website.com/changelog  
  
# Look for directories  
gobuster dir --url http://website.com --wordlist /usr/share/wordlists/dirb/common.txt  
gobuster dir --url http://website.com --wordlist /usr/share/wordlists/seclists/Discovery/Web-Content/raft-medium-directories.txt  
  
# Look for extraneous files  
gobuster dir --url http://websites.com --wordlist /usr/share/wordlists/dirb/common.txt -x zip,txt  
  
# Check for git repo  
curl http://www.website.com/.git/  
  
# Subdomain enumeration  
ffuf -w /usr/share/wordlists/seclists/Discovery/DNS/subdomains-top1million-5000.txt -u http://skyfall.htb -H "Host: FUZZ.skyfall.htb" -fs 20631,0  
  
# vhost enumeration  
gobuster vhost --wordlist "/usr/share/wordlists/seclists/Discovery/DNS/subdomains-top1million-5000.txt" --url http://skyfall.htb --append-domain  
  
# 403 Forbidden?  
Try to input %0a at the end