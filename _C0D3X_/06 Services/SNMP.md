# SNMP

## Overview

Community-string discovery, host/process/user extraction, and IPMI-adjacent follow-up where relevant.

## Default Ports

- 161/udp queries, 162/udp traps

## SNMP

```
# Querying OIDs using snmpwalk
snmpwalk -v2c -c <community string> <FQDN/IP>

# Bruteforcing community strings of the SNMP service.
onesixtyone -c community-strings.list <FQDN/IP>

# Bruteforcing SNMP service OIDs.
braa <community string>@<FQDN/IP>:.1.*
```

## IPMI

```
# IPMI version detection
msf6 auxiliary(scanner/ipmi/ipmi_version)

# Dump IPMI hashes
msf6 auxiliary(scanner/ipmi/ipmi_dumphashes)

# Enforce password-based authentication
ssh <user>@<FQDN/IP> -o PreferredAuthentications=password
```

## SNMP PUBLIC STRING?  (→ snmp_public.txt)

```bash
for ip in $(cat online); do snmpwalk -v2c -c public -t1 -r0 "$ip" 1.3.6.1.2.1.1.1.0 2>/dev/null | grep -q "DESCRIPTION" && echo $ip; done | tee snmp_public.txt
```

## SNMP

```bash
sudo nmap -sU --open -p 161 192.168.50.1-254 -oG open-snmp.txt
```

You can try common community strings:

```bash
echo public > community
echo private >> community
echo manager >> community
for ip in $(seq 1 254); do echo X.X.X.$ip; done > ips
onesixtyone -c community -i ips
onesixtyone -c community.txt <target>
```

More `snmpwalk` examples:

```bash
for community in public private manager; do snmpwalk -c $community -v1 <IP>; done
snmpwalk -c public -v1 <IP>   # add -Oa for HEX to ASCII
snmpwalk -c public -v1 <IP> 1.3.6.1.4.1.77.1.2.25   # enum Windows Users
snmpwalk -c public -v1 <IP> 1.3.6.1.2.1.25.4.2.1.2  # enum Windows processes
snmpwalk -c public -v1 <IP> 1.3.6.1.2.1.25.6.3.1.2  # enum Windows installed software
snmpwalk -c public -v1 <IP> 1.3.6.1.2.1.6.13.1.3    # enum Windows open TCP ports
snmpenum -t <IP>
snmpcheck -t <IP> -c public
nmap -vv -sV -sU -Pn -p 161,162 --script=snmp-netstat,snmp-processes <IP>
snmpwalk -c public -v1 <target>
```

---

```
sudo nmap -sU -p161 --script *snmp* 192.168.240.42
```
```
snmp-check 192.168.240.42
```
```
snmpwalk -c public -v1 -t 10 192.168.50.151
snmpwalk -v1 -c public 192.168.189.156 1.3.6.1.4.1.8072.1.3.2.3.1.1
```

[SNMP enumeration (161,162)](https://www.notion.so/SNMP-enumeration-161-162-fd52dea43c264141a9e0dd5b07711ecb?pvs=21) - There is more specific enum

```
nc -nv 192.168.217.143 3003
help
version
```

## See Also

- `01 Enumeration/External and Network Enumeration.md`
