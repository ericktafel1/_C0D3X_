
```
nmap -sV $IP -p110,143,993,995 -sC

nmap $IP -p143,993 --script imap-brute
```