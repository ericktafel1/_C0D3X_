
# Top 100 TCP Port Version Scan

```
nmap -sV $IP -F -oA name-top-100-tcp
```

# All TCP Ping Ports

```
nmap -sS $IP -p- -oA name-full-ping
```

# All UDP Ping Ports

```
nmap -sU $IP -p- -oa name-full-udp-ping
```

# Top 100 UDP Port Version Scan

```
nmap -sV -sU $IP -F -oA name-top-100-udp
```

# Through proxychains (-sT for connect scan, -n for skip dns, -Pn for skip host discovery)

```
nmap -sT -n -Pn ip
nmap -sT -vvv -Pn
```
# --top-ports=20