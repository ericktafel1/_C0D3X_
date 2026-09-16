# LDAP

## Overview

Directory service reference for naming contexts, anonymous bind testing, user/group extraction, and credentialed AD-oriented follow-up.

## Default Ports

- 389/tcp LDAP, 636/tcp LDAPS, 3268/tcp GC, 3269/tcp GC over TLS


## Tooling Note

- `nxc` / NetExec examples are preferred where present.
- Some legacy `crackmapexec` command lines were intentionally retained for searchability because the source vault used them heavily and operators still encounter them in older notes and scripts.

## LDAP ANON BIND?  (→ ldap_anon.txt)

```bash
for ip in $(cat online); do ldapsearch -x -H "ldap://$ip" -s base -b "" -o nettimeout=3 "(objectclass=*)" 2>/dev/null | head -n1 | grep -q "namingContexts" && echo $ip; done | tee ldap_anon.txt
```

## NETEXEC LDAP ENUM?  (→ ne_ldap.txt)

```bash
netexec ldap online -u '' -p '' -M enum |tee ne_ldap.txt
```

## ldapsearch

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

```bash
ldapsearch -x -h <target> -b "dc=example,dc=com"
nmap --script=ldap-search -p 389 <target>
```

---

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
ldapsearch -v -x -D fmcsorley@HUTCH.OFFSEC -w CrabSharkJellyfish192 -b "DC=hutch,DC=offsec" -h 192.168.120.108 "(ms-MCS-AdmPwd=*)" ms-MCS-AdmPwd
ldapsearch -v -x -D fmcsorley@HUTCH.OFFSEC -w CrabSharkJellyfish192 -b "DC=hutch,DC=offsec" -H ldap://192.168.211.122 "(ms-MCS-AdmPwd=*)" ms-MCS-AdmPwd
```

## Useful Additions

```bash
nmap -n -sV --script "ldap* and not brute" <ip>
ldapdomaindump -u '<domain>\<user>' -p '<password>' ldap://<dc-ip>
nxc ldap <dc-ip> -u <user> -p '<password>' --bloodhound -c all -ns <dns-ip>
```

## Common Attack Paths

- Anonymous bind or weakly protected bind operations leaking naming contexts and object data.
- User, group, SPN, and description harvesting for spraying, roasting, and path building.
- LAPS or delegated rights exposure when the querying principal has the required access.

## See Also

- `03 AD/Domain Enumeration.md`
- `03 AD/BloodHound ACLs and AD CS.md`
