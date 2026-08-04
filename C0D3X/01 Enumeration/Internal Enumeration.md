# Internal Enumeration

Fast internal recon and scan progression for a foothold inside a target network.
Start conservative, build a verified live-host list, then deepen coverage with targeted Nmap and follow-on service checks.

## General Checklist Before Starting

1. Authenticate with credentials to BloodHound.
2. Perform quick enumeration in BloodHound.
3. Ensure you claim all flags and collect sufficient screenshots.
4. Check anonymous or guest access to SMB shares on all IPs as a good starting point.
5. Step back and attack the Domain Controller as if you do not have credentials.
6. Also try default credentials like `offsec:lab`.
7. Enumerate MS01 until the end, even if you have local admin—use WinPEAS as well.
8. If other credentials are found, repeat the enumeration phase.
9. Try using the username as the password (both domain and local).
10. Use `nxc smb 192.168.123.100 -u adcreds.txt -p adcreds.txt --no-bruteforce`.
11. Use `nxc smb 192.168.123.100-160 --local-auth -u adcreds.txt -p adcreds.txt --no-bruteforce`.
12. Check all shares with the current user, guest, and anonymous access.
13. Use `rpcdump` and `enum4linux` with credentials.
14. Enumerate users with Kerbrute:

```bash
/Tools/kerbrute_linux_amd64 userenum -d domain.com --dc 192.168.123.100 $SECLIST/Usernames/Names/names.txt
```

15. Continue using Kerbrute until you have the naming schema, lots of users, and service accounts. Refer to [service-accounts.txt](https://github.com/crtvrffnrt/wordlists/blob/main/service-accounts.txt).
16. Request AS_REP messages:

```bash
impacket-GetNPUsers domain.com/ -usersfile adcreds.txt -dc-ip 192.168.123.100 -request -outputfile hash.hash
```

    [ASREPRoast HackTricks Guide](https://book.hacktricks.xyz/windows-hardening/active-directory-methodology/asreproast#request-as_rep-message)

17. Perform a UDP scan.
```bash
nmap -sUV -vv --reason  --version-intensity 0 --min-rate 1300 --max-retries 1 -top-ports 1000 192.168.236.161-163  -Pn
```
18. Repeat your steps—**Enumeration is key; try harder.**
19. Run WinPEAS with user or local admin privileges again.
20. Connect to SMB with:

```bash
impacket-smbclient domain.com/guest@192.168.123.100
```

21. Step back and review your enumeration to ensure nothing was missed.

## PING SWEEP?  (edit subnet)

```bash
nmap -sn 10.0.0.0/24 -oG ping_sweep
```

## EXTRACT LIVE IPS? (→ online)

#NOTE: Not ALL of these will always be real online machines. Some will be bogus ICMP returns...it just happens sometimes. Gather the local domain from the internal and grep for that in addition to any returned MAC Addresses. Basically, this is a situational thing when getting your actual "online" flat-file.
In bash terms:
```bash
|grep -iE 'mac|<domain>.local' -B2 |grep -oE '((1?[0-9][0-9]?|2[0-4][0-9]|25[0-5])\.){3}(1?[0-9][0-9]?|2[0-4][0-9]|25[0-5])' |sort -u > online
```
In basic terms:
```bash
cat ping_sweep |grep -oE '((1?[0-9][0-9]?|2[0-4][0-9]|25[0-5])\.){3}(1?[0-9][0-9]?|2[0-4][0-9]|25[0-5])' | sort -u > online
```

## TOP‑100 PORT SCAN?

```bash
for ip in $(cat online); do nmap -sS -Pn --top-ports 100 -oA "quick_$ip" "$ip"; done
```

## FULL TCP (optional)?

```bash
sudo nmap -sS -p- -T4 -iL online -oA full_scan
```

############################################

---

## Autorecon

```
sudo $(which autorecon) --only-scans-dir 192.168.193.153
```

## nmap

```
sudo nmap -p- -Pn -vvv --defeat-rst-ratelimit -oN nmap_all 192.168.193.153
```
```
cat nmap_all | grep 'open' | awk '{ print $1 }' | awk '{print ($0+0)}' | sed -z 's/\n/,/g;s/,$/\n/'
```
```
sudo nmap -v -A -Pn -oN nmap_A -p {ports} 192.168.193.153
```
```
sudo nmap -p- -A --open -vvv dc01
```
```
sudo nmap -sV -Pn -v -p 445 --script "vuln" 192.168.50.124
```
