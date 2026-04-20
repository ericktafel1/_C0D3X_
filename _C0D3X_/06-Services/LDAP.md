## LDAP ANON BIND?  (→ ldap_anon.txt)

> Source: `01101100-C0D3X-00110110.md` → `LDAP ANON BIND?  (→ ldap_anon.txt)`

```bash
for ip in $(cat online); do ldapsearch -x -H "ldap://$ip" -s base -b "" -o nettimeout=3 "(objectclass=*)" 2>/dev/null | head -n1 | grep -q "namingContexts" && echo $ip; done | tee ldap_anon.txt
```


## NETEXEC LDAP ENUM?  (→ ne_ldap.txt)

> Source: `01101100-C0D3X-00110110.md` → `NETEXEC LDAP ENUM?  (→ ne_ldap.txt)`

```bash
netexec ldap online -u '' -p '' -M enum |tee ne_ldap.txt
```


## ldapsearch

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Linux > ldapsearch`

```
ldapsearch -x -h <RHOST> -s base namingcontexts
ldapsearch -H ldap://<RHOST> -x -s base -b '' "(objectClass=*)" "*" +
ldapsearch -H ldaps://<RHOST>:636/ -x -s base -b '' "(objectClass=*)" "*" +
ldapsearch -x -H ldap://<RHOST> -D '' -w '' -b "DC=<RHOST>,DC=local"
ldapsearch -x -H ldap://<RHOST> -D '' -w '' -b "DC=<RHOST>,DC=local" | grep descr -A 3 -B 3
ldapsearch -x -h <RHOST> -b "dc=<RHOST>,dc=local" "*" | awk '/dn: / {print $2}'
ldapsearch -x -h <RHOST> -D "<USERNAME>" -b "DC=<DOMAIN>,DC=<DOMAIN>" "(ms-MCS-AdmPwd=*)" ms-MCS-AdmPwd
ldapsearch -H ldap://<RHOST> -D <USERNAME> -w "<PASSWORD>" -b "CN=Users,DC=<RHOST>,DC=local" | grep info
```


## LDAP

> Source: `01101100-C0D3X-00110110.md` → `Enumeration > Service Enumeration > LDAP`

```bash
ldapsearch -x -h <target> -b "dc=example,dc=com"
nmap --script=ldap-search -p 389 <target>
```

---

> Source: `01101100-C0D3X-00110110.md` → `CLEAR CMD RUNMRU? > LDAP`

```
nmap -n -sV --script "ldap* and not brute" <IP>
```
```
ldapsearch -v -x -b "DC=hutch,DC=offsec" -H "ldap://192.168.120.108" "(objectclass=*)"
```
```
ldapsearch -x -H ldap://<IP> -D '' -w '' -b "DC=<1_SUBDOMAIN>,DC=<TLD>" > ldap_search.txt
```
```
cat ldap_search.txt | grep -i "samaccountname" | cut -d: -f2 | tr -d " " > users.txt
```
```
~~ldapsearch -v -x -D fmcsorley@HUTCH.OFFSEC -w CrabSharkJellyfish192 -b "DC=hutch,DC=offsec" -h 192.168.120.108 "(ms-MCS-AdmPwd=*)" ms-MCS-AdmPwd~~
ldapsearch -v -x -D fmcsorley@HUTCH.OFFSEC -w CrabSharkJellyfish192 -b "DC=hutch,DC=offsec" -H ldap://192.168.211.122 "(ms-MCS-AdmPwd=*)" ms-MCS-AdmPwd
```

