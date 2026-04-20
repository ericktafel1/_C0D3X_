> Source: `01101100-C0D3X-00110110.md` → `Footprinting Services > FTP`

```
# Connect to FTP
ftp <IP>

# Interact with a service on the target.
nc -nv <IP> <PORT>

# Download all available files on the target FTP server
wget -m --no-passive ftp://anonymous:anonymous@<IP>
```

---


## FTP ANON LOGIN?  (→ ftp_anon.txt)

> Source: `01101100-C0D3X-00110110.md` → `FTP ANON LOGIN?  (→ ftp_anon.txt)`

```bash
for ip in $(cat online); do nmap -p21 --script ftp-anon -Pn "$ip" 2>/dev/null | grep -q "Anonymous FTP login allowed" && echo $ip; done | tee ftp_anon.txt
```

############################################


## FTP

> Source: `01101100-C0D3X-00110110.md` → `Enumeration > Service Enumeration > FTP`

```bash
nmap --script=ftp-anon,ftp-bounce -p 21 <target>
ftp <target>
```


## Anonymous FTP Login (check all default creds)

> Source: `01101100-C0D3X-00110110.md` → `Exploitation > Service Exploitations > Misconfigurations > Anonymous FTP Login (check all default creds)`

```bash
ftp <target>
```

---

> Source: `01101100-C0D3X-00110110.md` → `CLEAR CMD RUNMRU? > FTP`

```
ftp -aA4 {IPv4}
```
```
wget -m ftp://anonymous:anonymous@10.10.10.98
```
```
user
```
💡 In FTP, binaries in ASCII mode will make the file not executable. Set the mode to \`binary\`.💡 Try to do \`cd..\` (in kiero it let do traversal)
```
exiftool -a -G1 FUNCTION-TEMPLATE.pdf
```

