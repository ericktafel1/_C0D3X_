## Network Discovery and Port Scan Checklist

> Source: `01101100-C0D3X-00110110.md` → `Detailed Checklists > Network Discovery and Port Scan Checklist`

1. **Passive Discovery**:
   - Use `netdiscover` for ARP scanning:

```bash
netdiscover -i eth1 -r 192.168.123.0/24 -p
```

   - Listen for inbound traffic:

```bash
sudo tcpdump -i eth1 'dst host 192.168.123.100 and (icmp or udp or tcp or arp)'
```

   - Run Responder:

```bash
responder -I eth1 -A
```

2. **Active Discovery**:
   - Use `netdiscover`:

```bash
netdiscover -i eth1 -r 192.168.123.0/24
```

   - Ping sweep with Nmap:

```bash
nmap -PE -PM -PP -sn -n --open 192.168.123.0/24
```

   - Use `fping`:

```bash
fping -asgq 192.168.123.0/24
```

3. **Port Scanning**:
   - Use `masscan` for a quick scan:

```bash
masscan -p20,21-23,25,53,80,110,111,135,139,143,443,445,993,995,1723,3306,3389,5900,8080 192.168.123.0/24
```

   - Perform a detailed Nmap scan:

```bash
nmap -p- -v --min-rate 4000 -sV 192.168.123.100
nmap -p open_ports_here -vv --min-rate 1000 -sV -sC 192.168.123.100
```

   - Scan UDP ports:

```bash
sudo nmap -Pn -n 192.168.123.100 -sU --top-ports=100
```

4. **UDP Protocol Scanning**:
   - Use Nmap for UDP version scanning:

```bash
nmap -sUV --reason -F --version-intensity 0 --min-rate 5000 --max-retries 1 192.168.123.100
```

   - Use `udp-proto-scanner`:

```bash
# Refer to the GitHub repository for usage instructions
```

5. Revert the machine if necessary.
6. Repeat scanning steps—**Enumeration is key; try harder.**
7. Verify all findings and ensure no steps were missed.


## General Service Identification

> Source: `01101100-C0D3X-00110110.md` → `Enumeration > Service Enumeration > General Service Identification`

```bash
rustscan -a 192.168.236.248 -t 2000 -b 2000 --ulimit 5000 -- -A -sV -sC -Pn

rustscan -a 192.168.236.248 --ulimit 5000 -- -sV -sC -Pn

nmap -sV -p <open_ports> <target>
```

## HTTP

> Source: `01101100-C0D3X-00110110.md` → `Enumeration > Service Enumeration > HTTP`

```bash
sudo nmap -p80 -sV <IP>
sudo nmap -p80 --script=http-enum <IP>
```

> **Note:** The `http-enum` script can sometimes reveal directory listings.

```bash
sudo nmap --script http-headers <IP>
```


## Recon Find Delegation

> Source: `01101100-C0D3X-00110110.md` → `Impacket > Recon Find Delegation`

```
impacket-findDelegation -target-domain <domain> -dc-ip <dc_ip> <domain>/'<username>':'<password>'
```


## Recon Get SPN

> Source: `01101100-C0D3X-00110110.md` → `Impacket > Recon Get SPN`

```
impacket-GetUserSPNs -request -dc-ip <dc-ip> <domain>/'<username>':'<password>'
```
