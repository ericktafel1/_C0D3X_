## Querying DNS  
```shell
gobuster dns -d manager.htb -t 25 -w /usr/share/wordlists/seclists/Discovery/DNS/subdomains-top1million-5000.txt 
```
   
## Check for guest and null access  
```shell
smbclient -U '%' -L //10.10.11.236 && smbclient -U 'guest%' -L //  
enum4linux-ng -a -u "" -p "" 10.10.11.236 && enum4linux -a -u "guest" -p "" 10.10.11.236  
```
## Enumerate ldap  
```shell
nmap -n -sV --script "ldap* and not brute" -p 389 10.10.11.236
```
## Bruteforce and enumerate AD accounts through Kerberos Pre-auth  
```shell
./kerbrute userenum --dc 10.10.11.236 -d manager.htb /usr/share/wordlists/seclists/Usernames/xato-net-10-million-usernames.txt
```

# Checking permissions of a user

```bash
bloodyAD -d domain.local --host ip -u username -p password get object administrator --resolve-sd
```

bloodyAD --host dc01.infiltrator.htb --dc-ip 10.129.20.226 -u l.clark -p 'WAT?watismypass!' -d infiltrator.htbs get children