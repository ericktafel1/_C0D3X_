
# SNMP

```bash
snmpwalk -c public -v1 -t 10 192.168.50.151 
```

```
snmpwalk -c public -v2c -t 10 192.168.187.149 NET-SNMP-EXTEND-MIB::nsExtendObjects > snmpwalk2
```

# OneSixtyOne

```bash
onesixtyone -c /usr/share/seclists/Discovery/SNMP/snmp.txt [IP]
```


# Braa

```
braa public@IP:.1.3.6.*
```