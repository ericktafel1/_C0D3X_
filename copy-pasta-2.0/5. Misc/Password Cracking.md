# Identify a hash  
```
echo 'HASH' | hashid  
hashcat --hash-info   
```
  
# Windows  
## NTLM  
```
hashcat -m 1000 hashes /usr/share/wordlists/rockyou.txt  
```
  
## NetNTLMv2  
```
hashcat -m 5600 paul.hash /usr/share/wordlists/rockyou.txt --force  
```
  
# Linux hashes  
  
## for Yescrypt $y$j  
```
sudo john linux_hashes --format=crypt --wordlist=/usr/share/wordlists/rockyou.txt  
```
  
## Grab Shadow and Passwd files  
```
unshadow passwd shadow > passwords.txt  
```
  
## Use John to Crack  
```
john --wordlist=/usr/share/wordlists/rockyou.txt passwords.txt  
```
  
## Or format the hashes from a shadow file and use hashcat  
```
cat shadow | cut -d ":" -f 2 | grep -v "*" | grep -v "\!" > hashes  
hashcat -m 1800 hashes /usr/share/wordlists/rockyou.txt  
```
  
## cracking SSH key passwords  
```
ssh2john id_rsa > id_rsa.hash  
john --wordlist=/usr/share/wordlists/rockyou.txt id_rsa.hash  
```
# or  
```
hashcat -m 22921 ssh.hash ssh.passwords -r ssh.rule --force  
```
  
# Keepass Cracking  
```
keepass2john Database.kdbx > keepass.hash  
```

remove the filename or first word in hash so it starts with $keepass$  

```
hashcat -m 13400 keepass.hash /usr/share/wordlists/rockyou.txt -r /usr/share/hashcat/rules/rockyou-30000.rule --force  
  
mono ~/Inev/tools/KeePass/KeePass.exe [file]  
```
  
  
# cracking password protected 7z,zip files  
```
zip2john file.zip > zip.hashes  
```

```
7z2john file.7z > zip.hashes
```
# for 7z  
```
hashcat -m 11600 ziphashes /usr/share/wordlists/rockyou.txt   
```
  
# for winzip  
```
hashcat -m 13600 ziphashes /usr/share/wordlists/rockyou.txt  
```
  
# Obtain password policy  
```
crackmapexec smb 10.1.1.1 -u username -p password --pass-pol
```