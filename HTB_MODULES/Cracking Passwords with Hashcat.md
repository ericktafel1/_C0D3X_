# Introduction

* * *

## Password Cracking Overview

Password cracking, or offline brute force attacks, is an effective way of gaining access to unauthorized resources. Various applications and systems make use of cryptographic algorithms to hash or encrypt data. Doing so prevents the storage of plaintext information in data at rest and disclosure of transmitted data in man-in-the-middle (MITM) attack scenarios. Password cracking attacks attempt to recover the original data by performing brute force attacks against various algorithms and divulge the cleartext password.

Weak and reused passwords are two major factors that can determine the success of this attack. Additionally, attackers can create fine-tuned wordlists and use rules to mutate the passwords based on the target application or environment. A variety of open-source tools exist to facilitate password cracking. This module will focus on the popular tool `Hashcat`, a potent and useful tool for performing password cracking attacks against a wide variety of algorithms.

Password cracking is an extremely beneficial skill for a penetration tester, red teamer, or even those on the defensive side of information security. During an assessment, we will often retrieve a password hash that we must attempt to crack offline to proceed further towards our goal. A mastery of password cracking techniques coupled with the `Hashcat` tool, will arm us with a skill set that applies to many information security areas.


# Hashing vs. Encryption

* * *

## Hashing

Hashing is the process of converting some text to a string, which is unique to that particular text. Usually, a hash function always returns hashes with the same length irrespective of the type, length, or size of the data. Hashing is a one-way process, meaning there is no way of reconstructing the original plaintext from a hash. Hashing can be used for various purposes; for example, the [MD5](https://en.wikipedia.org/wiki/MD5) and [SHA256](https://en.wikipedia.org/wiki/SHA-2) algorithms are usually used to verify file integrity, while algorithms such as [PBKDF2](https://en.wikipedia.org/wiki/PBKDF2) are used to hash passwords before storage. Some hash functions can be keyed (i.e., an additional secret is used to create the hash). One such example is [HMAC](https://en.wikipedia.org/wiki/HMAC), which acts as a [checksum](https://en.wikipedia.org/wiki/Checksum) to verify if a particular message was tampered with during transmission.

As hashing is a one-way process, the only way to attack it is to use a list containing possible passwords. Each password from this list is hashed and compared to the original hash.

For example, mainly four different algorithms can be used to protect passwords on Unix systems. These are `SHA-512`, `Blowfish`, `BCrypt`, and `Argon2`. These algorithms are available on Unix operating systems such as Linux, BSD, and Solaris.

`SHA-512` converts a long string of characters into a hash value. It is fast and efficient, but there are many rainbow table attacks where an attacker uses a pre-computed table to reconstruct the original passwords.

Conversely, `Blowfish` is a symmetric block cipher algorithm that encrypts a password with a key. It is more secure than SHA-512 but also a lot slower.

`BCrypt` uses a slow hash function to make it harder for potential attackers to guess passwords or perform rainbow table attacks.

`Argon2`, on the other hand, is a modern and secure algorithm explicitly designed for password hashing systems. It uses multiple rounds of hash functions and a large amount of memory to make it harder for attackers to guess passwords. This is considered one of the most secure algorithms because it has a high time and resource requirement.

One protection employed against the brute-forcing of hashes is "salting." A salt is a random piece of data added to the plaintext before hashing it. This increases the computation time but does not prevent brute force altogether.

Let's consider the plaintext password value "p@ssw0rd". The MD5 hash for this can be calculated as follows:

```shell
echo -n "p@ssw0rd" | md5sum

0f359740bd1cda994f8b55330c86d845

```

Now, suppose a random salt such as "123456" is introduced and appended to the plaintext.

```shell
echo -n "p@ssw0rd123456" | md5sum

f64c413ca36f5cfe643ddbec4f7d92d0

```

A completely new hash was generated using this method, which will not be present in any pre-computed list. An attacker trying to crack this hash will have to sacrifice extra time to append this salt before calculating the hash.

Some hash functions such as MD5 have also been vulnerable to collisions, where two sets of plaintext can produce the same hash.

* * *

## Encryption

Encryption is the process of converting data into a format in which the original content is not accessible. Unlike hashing, encryption is reversible, i.e., it's possible to decrypt the ciphertext (encrypted data) and obtain the original content. Some classic examples of encryption ciphers are the [Caesar cipher](https://en.wikipedia.org/wiki/Caesar_cipher), [Bacon's cipher](https://en.wikipedia.org/wiki/Bacon%27s_cipher) and [Substitution cipher](https://en.wikipedia.org/wiki/Substitution_cipher). Encryption algorithms are of two types: Symmetric and Asymmetric.

* * *

## Symmetric Encryption

Symmetric algorithms use a key or secret to encrypt the data and use the same key to decrypt it. A basic example of symmetric encryption is XOR.

```shell
python3

Python 3.8.3 (default, May 14 2020, 11:03:12)
[GCC 9.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from pwn import xor
>>> xor("p@ssw0rd", "secret")
b'\x03%\x10\x01\x12D\x01\x01'

```

In the image above, the plaintext is `p@ssw0rd,` and the key is `secret`. Anyone who has the key can decrypt the ciphertext and obtain the plaintext.

```shell
python3

Python 3.8.3 (default, May 14 2020, 11:03:12)
[GCC 9.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from pwn import xor
>>> xor('\x03%\x10\x01\x12D\x01\x01', "secret")
b'p@ssw0rd'

```

The `b` in the above outputs denotes a byte string. This distinction was not made pre `Python3`.

Some other examples of symmetric algorithms are [AES](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard), [DES](https://en.wikipedia.org/wiki/Data_Encryption_Standard), [3DES](https://en.wikipedia.org/wiki/Triple_DES) and [Blowfish](https://en.wikipedia.org/wiki/Blowfish_(cipher)#The_algorithm). These algorithms can be vulnerable to attacks such as key bruteforcing, [frequency analysis](https://en.wikipedia.org/wiki/Frequency_analysis), [padding oracle attack](https://en.wikipedia.org/wiki/Padding_oracle_attack), etc.

* * *

## Asymmetric Encryption

On the other hand, asymmetric algorithms divide the key into two parts (i.e., public and private). The public key can be given to anyone who wishes to encrypt some information and pass it securely to the owner. The owner then uses their private key to decrypt the content. Some examples of asymmetric algorithms are [RSA](https://en.wikipedia.org/wiki/RSA_(cryptosystem)), [ECDSA](https://en.wikipedia.org/wiki/Elliptic_Curve_Digital_Signature_Algorithm), and [Diffie-Hellman](https://en.wikipedia.org/wiki/Diffie%E2%80%93Hellman_key_exchange).

One of the prominent uses of asymmetric encryption is the `Hypertext Transfer Protocol Secure` ( `HTTPS`) protocol in the form of `Secure Sockets Layer` ( `SSL`). When a client connects to a server hosting an `HTTPS` website, a public key exchange occurs. The client's browser uses this public key to encrypt any kind of data sent to the server. The server decrypts the incoming traffic before passing it on to the processing service.


# Identifying Hashes

* * *

Most hashing algorithms produce hashes of a constant length. The length of a particular hash can be used to map it to the algorithm it was hashed with. For example, a hash of 32 characters in length can be an MD5 or NTLM hash.

Sometimes, hashes are stored in certain formats. For example, `hash:salt` or `$id$salt$hash`.

The hash `2fc5a684737ce1bf7b3b239df432416e0dd07357:2014` is a SHA1 hash with the salt of `2014`.

The hash `$6$vb1tLY1qiY$M.1ZCqKtJBxBtZm1gRi8Bbkn39KU0YJW1cuMFzTRANcNKFKR4RmAQVk4rqQQCkaJT6wXqjUkFcA/qNxLyqW.U/` contains three fields delimited by `$`, where the first field is the `id`, i.e., `6`. This is used to identify the type of algorithm used for hashing. The following list contains some ids and their corresponding algorithms.

```shell
$1$  : MD5
$2a$ : Blowfish
$2y$ : Blowfish, with correct handling of 8 bit characters
$5$  : SHA256
$6$  : SHA512

```

The next field, `vb1tLY1qiY`, is the salt used during hashing, and the final field is the actual hash.

Open and closed source software use many different kinds of hash formats. For example, the `Apache` web server stores its hashes in the format `$apr1$71850310$gh9m4xcAn3MGxogwX/ztb.`, while `WordPress` stores hashes in the form `$P$984478476IagS59wHZvyQMArzfx58u.`.

* * *

## Hashid

[Hashid](https://github.com/psypanda/hashID) is a `Python` tool, which can be used to detect various kinds of hashes. At the time of writing, `hashid` can be used to identify over 200 unique hash types, and for others, it will make a best-effort guess, which will still require some additional work to narrow it down. The full list of supported hashes can be found [here](https://github.com/psypanda/hashID/blob/master/doc/HASHINFO.xlsx). It can be installed using `pip`.

```shell
pip install hashid

```

Hashes can be supplied as command-line arguments or using a file.

```shell
hashid '$apr1$71850310$gh9m4xcAn3MGxogwX/ztb.'

Analyzing '$apr1$71850310$gh9m4xcAn3MGxogwX/ztb.'
[+] MD5(APR)
[+] Apache MD5

```

```shell
hashid hashes.txt

--File 'hashes.txt'--
Analyzing '2fc5a684737ce1bf7b3b239df432416e0dd07357:2014'
[+] SHA-1
[+] Double SHA-1
[+] RIPEMD-160
[+] Haval-160
[+] Tiger-160
[+] HAS-160
[+] LinkedIn
[+] Skein-256(160)
[+] Skein-512(160)
[+] Redmine Project Management Web App
[+] SMF ≥ v1.1
Analyzing '$P$984478476IagS59wHZvyQMArzfx58u.'
[+] Wordpress ≥ v2.6.2
[+] Joomla ≥ v2.5.18
[+] PHPass' Portable Hash
--End of file 'hashes.txt'--

```

If known, `hashid` can also provide the corresponding `Hashcat` hash mode with the `-m` flag if it is able to determine the hash type.

```shell
hashid '$DCC2$10240#tom#e4e938d12fe5974dc42a90120bd9c90f' -m
Analyzing '$DCC2$10240#tom#e4e938d12fe5974dc42a90120bd9c90f'
[+] Domain Cached Credentials 2 [Hashcat Mode: 2100

```

* * *

## Context is Important

It is not always possible to identify the algorithm based on the obtained hash. Depending on the software, the plaintext might undergo multiple encryption rounds and salting transformations, making it harder to recover.

It is important to note that `hashid` uses regex to make a best-effort determination for the type of hash provided. Oftentimes `hashid` will provide many possibilities for a given hash, and we will still be left with a certain amount of guesswork to identify a given hash. This may happen during a CTF, but we usually have some context around the type of hash we are looking to identify during a penetration test. Was it obtained via an Active Directory attack or from a Windows host? Was it obtained through the successful exploitation of a SQL injection vulnerability? Knowing where a hash came from will greatly help us narrow down the hash type and, therefore, the `Hashcat` hash mode necessary to attempt to crack it. `Hashcat` provides an excellent [reference](https://hashcat.net/wiki/doku.php?id=example_hashes), which maps hash modes to example hashes. This reference is invaluable during a penetration test to determine the type of hash we are dealing with and the associated hash mode required to pass it to `Hashcat`.

For example, passing the hash `a2d1f7b7a1862d0d4a52644e72d59df5:500:[email protected]` to `hashid` will give us various possibilities:

```shell
hashid 'a2d1f7b7a1862d0d4a52644e72d59df5:500:[email protected]'

Analyzing 'a2d1f7b7a1862d0d4a52644e72d59df5:500:[email protected]'
[+] MD5
[+] MD4
[+] Double MD5
[+] LM
[+] RIPEMD-128
[+] Haval-128
[+] Tiger-128
[+] Skein-256(128)
[+] Skein-512(128)
[+] Lotus Notes/Domino 5
[+] Skype
[+] Lastpass

```

However, a quick look through the `Hashcat` example hashes reference will help us determine that it is indeed a Lastpass hash, which is hash mode `6800`. Context is important during assessments and is important to consider when working with any tool that attempts to identify hash types.


# Hashcat Overview

* * *

## Hashcat

[Hashcat](https://hashcat.net/hashcat/) is a popular open-source password cracking tool.

`Hashcat` can be downloaded from the [website](https://hashcat.net/hashcat/) using `wget` and then decompressed using the `7z` (7-Zip file archiver) via the command line. The full help menu can be viewed by typing `hashcat -h`. The latest version of `Hashcat` at the time of writing is version 6.1.1. Version 6.0.0 was a major release that introduced several enhancements over version 5.x. Some of the changes include performance improvements and 51 new algorithms (or supported hash types, also known as hash modes) for a total of over 320 supported algorithms at the time of writing. We can also download a standalone binary of the latest release for Windows and Unix/Linux systems from Hashcat's website or compile from the source.

The `Hashcat` team does not maintain any packages, aside from the official GitHub [repo](https://github.com/hashcat/hashcat). Any other repos (i.e., installing from `apt`), are left up to the 3rd party to keep up-to-date. The latest version can always be obtained directly from their GitHub repo and install from the source. For our purposes, we will demonstrate installation within the Pwnbox, which, at the time of writing, is using the latest version (6.1.1).

#### Hashcat Installation

```shell
sudo apt install hashcat
hashcat -h

hashcat (v6.1.1) starting...

Usage: hashcat [options]... hash|hashfile|hccapxfile [dictionary|mask|directory]...

- [ Options ] -

 Options Short / Long           | Type | Description                                          | Example
================================+======+======================================================+=======================
 -m, --hash-type                | Num  | Hash-type, see references below                      | -m 1000
 -a, --attack-mode              | Num  | Attack-mode, see references below                    | -a 3
 -V, --version                  |      | Print version                                        |
 -h, --help                     |      | Print help                                           |
     --quiet                    |      | Suppress output                                      |
     --hex-charset              |      | Assume charset is given in hex                       |
     --hex-salt                 |      | Assume salt is given in hex                          |
     --hex-wordlist             |      | Assume words in wordlist are given in hex            |
     --force                    |      | Ignore warnings                                      |
     --status                   |      | Enable automatic update of the status screen         |
     --status-json              |      | Enable JSON format for status output                 |
     --status-timer             | Num  | Sets seconds between status screen updates to X      | --status-timer=1
     --stdin-timeout-abort      | Num  | Abort if there is no input from stdin for X seconds  | --stdin-timeout-abort=300
     --machine-readable         |      | Display the status view in a machine-readable format |

<SNIP>

```

The folder contains 64-bit binaries for both Windows and Linux. The `-a` and `-m` arguments are used to specify the type of attack mode and hash type. `Hashcat` supports the following attack modes:

| **#** | **Mode** |
| --- | --- |
| 0 | Straight |
| 1 | Combination |
| 3 | Brute-force |
| 6 | Hybrid Wordlist + Mask |
| 7 | Hybrid Mask + Wordlist |

The hash type value is based on the algorithm of the hash to be cracked. A complete list of hash types and their corresponding examples can be found [here](https://hashcat.net/wiki/doku.php?id=example_hashes). The table helps in quickly identifying the number for a given hash type. You can also view the list of example hashes via the command line using the following command:

#### Hashcat - Example Hashes

```shell
hashcat --example-hashes | less

hashcat (v6.1.1) starting...

MODE: 0
TYPE: MD5
HASH: 8743b52063cd84097a65d1633f5c74f5
PASS: hashcat

MODE: 10
TYPE: md5($pass.$salt)
HASH: 3d83c8e717ff0e7ecfe187f088d69954:343141
PASS: hashcat

MODE: 11
TYPE: Joomla < 2.5.18
HASH: b78f863f2c67410c41e617f724e22f34:89384528665349271307465505333378
PASS: hashcat

MODE: 12
TYPE: PostgreSQL
HASH: 93a8cf6a7d43e3b5bcd2dc6abb3e02c6:27032153220030464358344758762807
PASS: hashcat

MODE: 20
TYPE: md5($salt.$pass)
HASH: 57ab8499d08c59a7211c77f557bf9425:4247
PASS: hashcat

<SNIP>

```

You can scroll through the list and press `q` to exit.

The benchmark test (or performance test) for a particular hash type can be performed using the `-b` flag.

#### Hashcat - Benchmark

```shell
hashcat -b -m 0
hashcat (v6.1.1) starting in benchmark mode...

Benchmarking uses hand-optimized kernel code by default.
You can use it in your cracking session by setting the -O option.
Note: Using optimized kernel code limits the maximum supported password length.
To disable the optimized kernel code in benchmark mode, use the -w option.

OpenCL API (OpenCL 1.2 pocl 1.5, None+Asserts, LLVM 9.0.1, RELOC, SLEEF, DISTRO, POCL_DEBUG) - Platform #1 [The pocl project]
=============================================================================================================================
* Device #1: pthread-Intel(R) Core(TM) i7-5820K CPU @ 3.30GHz, 4377/4441 MB (2048 MB allocatable), 6MCU

Benchmark relevant options:
===========================
* --optimized-kernel-enable

Hashmode: 0 - MD5

Speed.#1.........:   449.4 MH/s (12.84ms) @ Accel:1024 Loops:1024 Thr:1 Vec:8

Started: Fri Aug 28 21:52:35 2020
Stopped: Fri Aug 28 21:53:25 2020

```

For example, the hash rate for MD5 on a given CPU is found to be 450.7 MH/s.

We can also run `hashcat -b` to run benchmarks for all hash modes.

#### Hashcat - Optimizations

Hashcat has two main ways to optimize speed:

| Option | Description |
| --- | --- |
| Optimized Kernels | This is the `-O` flag, which according to the documentation, means `Enable optimized kernels (limits password length)`. The magical password length number is generally 32, with most wordlists won't even hit that number. This can take the estimated time from days to hours, so it is always recommended to run with `-O` first and then rerun after without the `-O` if your GPU is idle. |
| Workload | This is the `-w` flag, which, according to the documentation, means `Enable a specific workload profile`. The default number is `2`, but if you want to use your computer while Hashcat is running, set this to `1`. If you plan on the computer only running Hashcat, this can be set to `3`. |

It is important to note that the use of `--force` should be avoided. While this appears to make `Hashcat` work on certain hosts, it is actually disabling safety checks, muting warnings, and bypasses problems that the tool's developers have deemed to be blockers. These problems can lead to false positives, false negatives, malfunctions, etc. If the tool is not working properly without forcing it to run with `--force` appended to your command, we should troubleshoot the root cause (i.e., a driver issue). Using `--force` is discouraged by the tool's developers and should only be used by experienced users or developers.

Enable step-by-step solutions for all questions
![sparkles-icon-decoration](https://academy.hackthebox.com/images/sparkles-solid.svg)

#### Questions

Answer the question(s) below
to complete this Section and earn cubes!

Cheat Sheet

\+ 1  What is the hash mode of the hash type Cisco-ASA MD5?


Submit


# Dictionary Attack

* * *

Hashcat has 5 different attack modes that have different applications depending on the type of hash you are trying to crack and the complexity of the password. The most straightforward but extremely effective attack type is the dictionary attack. It is not uncommon to encounter organizations with weak password policies whose users select common words and phrases with little to no complexity as their passwords. Based on an analysis of millions of leaked passwords, the organization SplashData listed the following as the top 5 most common passwords of 2020:

#### Password List - Top 5 (2020)

```shell
123456
123456789
qwerty
password
1234567

```

Despite training users on security awareness, users will often choose one out of convenience if an organization allows weak passwords.

These passwords would appear in most any dictionary file used to perform this type of attack. There are many sources for obtaining password lists such as [SecLists](https://github.com/danielmiessler/SecLists/tree/master/Passwords), a large collection of password lists, and the `rockyou.txt` wordlist, which is found in most penetration testing Linux distros.

We can also find large wordlists such as [CrackStation's Password Cracking Dictionary](https://crackstation.net/crackstation-wordlist-password-cracking-dictionary.htm), which contains 1,493,677,782 words and is 15GB in size. Depending on needs and computing requirements, there are much larger wordlists made up of cleartext passwords obtained from multiple breaches and password dumps, some equaling over 40GB in size. These can be extremely useful when attempting to crack a single password, critical to your engagement's success, on a powerful GPU or when performing a domain password analysis of all of the user passwords in an Active Directory environment by attempting to crack as many of the NTLM password hashes in the NTDS.dit file as possible.

* * *

## Straight or Dictionary Attack

As the name suggests, this attack reads from a wordlist and tries to crack the supplied hashes. Dictionary attacks are useful if you know that the target organization uses weak passwords or just wants to run through some cracking attempts rather quickly. This attack is typically faster to complete than the more complex attacks discussed later in this module. It's basic syntax is:

#### Hashcat - Syntax

```shell
hashcat -a 0 -m <hash type> <hash file> <wordlist>

```

For example, the following commands will crack a SHA256 hash using the `rockyou.txt` wordlist.

```shell
echo -n '!academy' | sha256sum | cut -f1 -d' ' > sha256_hash_example
hashcat -a 0 -m 1400 sha256_hash_example /opt/useful/seclists/Passwords/Leaked-Databases/rockyou.txt

hashcat (v6.1.1) starting...

<SNIP>

Dictionary cache built:
* Filename..: /opt/useful/seclists/Passwords/Leaked-Databases/rockyou.txt
* Passwords.: 14344392
* Bytes.....: 139921507
* Keyspace..: 14344385
* Runtime...: 2 secs

Approaching final keyspace - workload adjusted.

006fc3a9613f3edd9f97f8e8a8eff3b899a2d89e1aabf33d7cc04fe0728b0fe6:!academy

Session..........: hashcat
Status...........: Cracked
Hash.Name........: SHA2-256
Hash.Target......: 006fc3a9613f3edd9f97f8e8a8eff3b899a2d89e1aabf33d7cc...8b0fe6
Time.Started.....: Fri Aug 28 21:58:44 2020 (4 secs)
Time.Estimated...: Fri Aug 28 21:58:48 2020 (0 secs)
Guess.Base.......: File (/opt/useful/seclists/Passwords/Leaked-Databases/rockyou.txt)
Guess.Queue......: 1/1 (100.00%)
Speed.#1.........:  3383.5 kH/s (0.46ms) @ Accel:1024 Loops:1 Thr:1 Vec:8
Recovered........: 1/1 (100.00%) Digests
Progress.........: 14344385/14344385 (100.00%)
Rejected.........: 0/14344385 (0.00%)
Restore.Point....: 14340096/14344385 (99.97%)
Restore.Sub.#1...: Salt:0 Amplifier:0-1 Iteration:0-1
Candidates.#1....: $HEX[216361726f6c796e] -> $HEX[042a0337c2a156616d6f732103]

Started: Fri Aug 28 21:58:05 2020
Stopped: Fri Aug 28 21:58:49 2020

```

In the above example, the hash cracked in 4 seconds. Cracking speed varies depending on the underlying hardware, hash type, and complexity of the password.

Let's look at a more complex hash such as [Bcrypt](https://en.wikipedia.org/wiki/Bcrypt), which is a type of password hash based on the [Blowfish](https://en.wikipedia.org/wiki/Blowfish_(cipher)) cipher. It utilizes a salt to protect it from rainbow table attacks and can have many rounds of the algorithm applied, making the hash resistant to brute force attacks even with a large password cracking rig.

For example, take the bcrypt hash of the same password " `!academy`" which would be `$2a$05$ZdEkj8cup/JycBRn2CX.B.nIceCYR8GbPbCCg6RlD7uvuREexEbVy` with 5 rounds of the Blowfish algorithm applied. This hash run on the same hardware with the same wordlist takes considerably longer to crack.

At any time during the cracking process, you can hit the " `s`" key to get a status on the cracking job, which shows that to attempt every password in the `rockyou.txt` wordlist will take over 1.5 hours. Applying more rounds of the algorithm will increase cracking time exponentially. In the case of hashes such as bcrypt, it is often better to use smaller, more targeted, wordlists.

#### Hashcat - Status

```shell
[s]tatus [p]ause [b]ypass [c]heckpoint [q]uit => s

Session..........: hashcat
Status...........: Running
Hash.Name........: bcrypt $2*$, Blowfish (Unix)
Hash.Target......: $2a$05$ZdEkj8cup/JycBRn2CX.B.nIceCYR8GbPbCCg6RlD7uv...exEbVy
Time.Started.....: Mon Jun 22 19:43:40 2020 (3 mins, 10 secs)
Time.Estimated...: Mon Jun 22 21:20:28 2020 (1 hour, 33 mins)
Guess.Base.......: File (/usr/share/wordlists/rockyou.txt)
Guess.Queue......: 1/1 (100.00%)
Speed.#1.........:     2470 H/s (8.98ms) @ Accel:8 Loops:16 Thr:1 Vec:8
Recovered........: 0/1 (0.00%) Digests
Progress.........: 468576/14344385 (3.27%)
Rejected.........: 0/468576 (0.00%)
Restore.Point....: 468576/14344385 (3.27%)
Restore.Sub.#1...: Salt:0 Amplifier:0-1 Iteration:16-32
Candidates.#1....: septiembre29 -> sep1101

```

As we have seen in this section, dictionary attacks can be very effective for weak passwords, but the attack's efficacy also depends on the type of hash targeted. Certain types of weaker passwords can be much more difficult to crack just based on the hashing algorithm in use. This does not mean that a weak password using a stronger hashing algorithm is any more "secure." Password cracking hardware varies, and "cracking rigs" with many GPUs could make short work of a password hash that would take hours or days on a single CPU.


# Combination Attack

* * *

The combination attack modes take in two wordlists as input and create combinations from them. This attack is useful because it is not uncommon for users to join two or more words together, thinking that this creates a stronger password, i.e., `welcomehome` or `hotelcalifornia`.

To demonstrate this attack, consider the following wordlists:

```shell
cat wordlist1

super
world
secret

```

```shell
cat wordlist2

hello
password

```

If given these two word lists `Hashcat` will produce exactly 3 x 2 = 6 words, such as the following:

```shell
awk '(NR==FNR) { a[NR]=$0 } (NR != FNR) { for (i in a) { print $0 a[i] } }' file2 file1

superhello
superpassword
worldhello
wordpassword
secrethello
secretpassword

```

This can also be done with `Hashcat` using the `--stdout` flag which can be very helpful for debugging purposes and seeing how the tool is handling things.

We can see what `Hashcat` will produce given the same two files in the following example:

```shell
hashcat -a 1 --stdout file1 file2
superhello
superpassword
worldhello
worldpassword
secrethello
secretpassword

```

* * *

#### Hashcat - Syntax

The syntax for the combination attack is:

```shell
hashcat -a 1 -m <hash type> <hash file> <wordlist1> <wordlist2>

```

This attack provides more flexibility and customization when using wordlists.

Let's see this example in practice. First, create the md5 of the password `secretpassword`.

```shell
echo -n 'secretpassword' | md5sum | cut -f1 -d' '  > combination_md5

2034f6e32958647fdff75d265b455ebf

```

Next, let's run `Hashcat` against the hash using the two wordlists above with the combination attack mode.

```shell
hashcat -a 1 -m 0 combination_md5 wordlist1 wordlist2

hashcat (v6.1.1) starting...
<SNIP>

Dictionary cache hit:
* Filename..: wordlist1
* Passwords.: 3
* Bytes.....: 19
* Keyspace..: 6

The wordlist or mask that you are using is too small.
This means that hashcat cannot use the full parallel power of your device(s).
Unless you supply more work, your cracking speed will drop.
For tips on supplying more work, see: https://hashcat.net/faq/morework

Approaching final keyspace - workload adjusted.

2034f6e32958647fdff75d265b455ebf:secretpassword

Session..........: hashcat
Status...........: Cracked
Hash.Name........: MD5
Hash.Target......: 2034f6e32958647fdff75d265b455ebf
Time.Started.....: Fri Aug 28 22:05:51 2020, (0 secs)
Time.Estimated...: Fri Aug 28 22:05:51 2020, (0 secs)
Guess.Base.......: File (wordlist1), Left Side
Guess.Mod........: File (wordlist2), Right Side
Speed.#1.........:       42 H/s (0.02ms) @ Accel:1024 Loops:2 Thr:1 Vec:8
Recovered........: 1/1 (100.00%) Digests
Progress.........: 6/6 (100.00%)
Rejected.........: 0/6 (0.00%)
Restore.Point....: 0/3 (0.00%)
Restore.Sub.#1...: Salt:0 Amplifier:0-2 Iteration:0-2
Candidates.#1....: superhello -> secretpassword

```

Combination attacks are another powerful tool to keep in our arsenal. As demonstrated above, merely combining two words does not necessarily make a password stronger.

* * *

## Exercise - Supplementary word lists

#### Supplementary word list \#1

```shell
sunshine
happy
frozen
golden

```

#### Supplementary word list \#2

```shell
hello
joy
secret
apple

```


# Mask Attack

* * *

Mask attacks are used to generate words matching a specific pattern. This type of attack is particularly useful when the password length or format is known. A mask can be created using static characters, ranges of characters (e.g. \[a-z\] or \[A-Z0-9\]), or placeholders. The following list shows some important placeholders:

| **Placeholder** | **Meaning** |
| --- | --- |
| ?l | lower-case ASCII letters (a-z) |
| ?u | upper-case ASCII letters (A-Z) |
| ?d | digits (0-9) |
| ?h | 0123456789abcdef |
| ?H | 0123456789ABCDEF |
| ?s | special characters («space»!"#$%&'()\*+,-./:;<=>?@\[\]^\_\`{ |
| ?a | ?l?u?d?s |
| ?b | 0x00 - 0xff |

* * *

The above placeholders can be combined with options " `-1`" to " `-4`" which can be used for custom placeholders. See the _Custom charsets_ section [here](https://hashcat.net/wiki/doku.php?id=mask_attack) for a detailed breakdown of each of these four command-line parameters that can be used to configure four custom charsets.

Consider the company Inlane Freight, which this time has passwords with the scheme " `ILFREIGHT<userid><year>`," where userid is 5 characters long. The mask " `ILFREIGHT?l?l?l?l?l20[0-1]?d`" can be used to crack passwords with the specified pattern, where " `?l`" is a letter and " `20[0-1]?d`" will include all years from 2000 to 2019.

Let's try creating a hash and cracking it using this mask.

#### Creating MD5 hashes

```shell
echo -n 'ILFREIGHTabcxy2015' | md5sum | tr -d " -" > md5_mask_example_hash

```

In the below example, the attack mode is `3`, and the hash type for MD5 is `0`.

#### Hashcat - Mask Attack

```shell
hashcat -a 3 -m 0 md5_mask_example_hash -1 01 'ILFREIGHT?l?l?l?l?l20?1?d'

hashcat (v6.1.1) starting...
<SNIP>

d53ec4d0b37bbf565b1e09d64834e1ae:ILFREIGHTabcxy2015

Session..........: hashcat
Status...........: Cracked
Hash.Name........: MD5
Hash.Target......: d53ec4d0b37bbf565b1e09d64834e1ae
Time.Started.....: Fri Aug 28 22:08:44 2020, (43 secs)
Time.Estimated...: Fri Aug 28 22:09:27 2020, (0 secs)
Guess.Mask.......: ILFREIGHT?l?l?l?l?l20?1?d [18]
Guess.Charset....: -1 01, -2 Undefined, -3 Undefined, -4 Undefined
Guess.Queue......: 1/1 (100.00%)
Speed.#1.........:  3756.3 kH/s (0.36ms) @ Accel:1024 Loops:1 Thr:1 Vec:8
Recovered........: 1/1 (100.00%) Digests
Progress.........: 155222016/237627520 (65.32%)
Rejected.........: 0/155222016 (0.00%)
Restore.Point....: 155215872/237627520 (65.32%)
Restore.Sub.#1...: Salt:0 Amplifier:0-1 Iteration:0-1
Candidates.#1....: ILFREIGHTuisba2015 -> ILFREIGHTkmrff2015

```

The " `-1`" option was used to specify a placeholder with just 0 and 1. `Hashcat` could crack the hash in 43 seconds on CPU power. The " `--increment`" flag can be used to increment the mask length automatically, with a length limit that can be supplied using the " `--increment-max`" flag.


# Hybrid Mode

* * *

Hybrid mode is a variation of the combinator attack, wherein multiple modes can be used together for a fine-tuned wordlist creation. This mode can be used to perform very targeted attacks by creating very customized wordlists. It is particularly useful when you know or have a general idea of the organization's password policy or common password syntax. The attack mode for the hybrid attack is " `6`".

Let's consider a password such as " `football1$`". The example below shows how a wordlist can be used in combination with a mask.

#### Creating Hybrid Hash

```shell
echo -n 'football1$' | md5sum | tr -d " -" > hybrid_hash

```

Hashcat reads words from the wordlist and appends a unique string based on the mask supplied. In this case, the mask " `?d?s`" tells hashcat to append a digit and a special character at the end of each word in the `rockyou.txt` wordlist.

#### Hashcat - Hybrid Attack using Wordlists

```shell
hashcat -a 6 -m 0 hybrid_hash /opt/useful/seclists/Passwords/Leaked-Databases/rockyou.txt '?d?s'

hashcat (v6.1.1) starting...
<SNIP>

f7a4a94ff3a722bf500d60805e16b604:football1$

Session..........: hashcat
Status...........: Cracked
Hash.Name........: MD5
Hash.Target......: f7a4a94ff3a722bf500d60805e16b604
Time.Started.....: Fri Aug 28 22:11:15 2020, (0 secs)
Time.Estimated...: Fri Aug 28 22:11:15 2020, (0 secs)
Guess.Base.......: File (/opt/useful/seclists/Passwords/Leaked-Databases/rockyou.txt), Left Side
Guess.Mod........: Mask (?d?s) [2], Right Side
Guess.Queue.Base.: 1/1 (100.00%)
Guess.Queue.Mod..: 1/1 (100.00%)
Speed.#1.........:  5118.2 kH/s (11.56ms) @ Accel:768 Loops:82 Thr:1 Vec:8
Recovered........: 1/1 (100.00%) Digests
Progress.........: 755712/4733647050 (0.02%)
Rejected.........: 0/755712 (0.00%)
Restore.Point....: 0/14344385 (0.00%)
Restore.Sub.#1...: Salt:0 Amplifier:82-164 Iteration:0-82
Candidates.#1....: 1234562= -> class083~

```

Attack mode " `7`" can be used to prepend characters to words using a given mask. The following example shows a mask using a custom character set to add a prefix to each word in the `rockyou.txt` wordlist. The custom character mask " `20?1?d`" with the custom character set " `-1 01`" will prepend various years to each word in the wordlist (i.e., 2010, 2011, 2012..).

#### Creating another Hybrid Hash

```shell
echo -n '2015football' | md5sum | tr -d " -" > hybrid_hash_prefix

```

#### Hashcat - Hybrid Attack using Wordlists with Masks

```shell
hashcat -a 7 -m 0 hybrid_hash_prefix -1 01 '20?1?d' /opt/useful/seclists/Passwords/Leaked-Databases/rockyou.txt

hashcat (v6.1.1) starting...
<SNIP>

eac4fe196339e1b511278911cb77d453:2015football

Session..........: hashcat
Status...........: Cracked
Hash.Name........: MD5
Hash.Target......: eac4fe196339e1b511278911cb77d453
Time.Started.....: Thu Nov 12 01:32:34 2020 (0 secs)
Time.Estimated...: Thu Nov 12 01:32:34 2020 (0 secs)
Guess.Base.......: File (/usr/share/wordlists/rockyou.txt), Right Side
Guess.Mod........: Mask (20?1?d) [4], Left Side
Guess.Charset....: -1 01, -2 Undefined, -3 Undefined, -4 Undefined
Speed.#1.........:     8420 H/s (0.22ms) @ Accel:384 Loops:64 Thr:1 Vec:8
Recovered........: 1/1 (100.00%) Digests
Progress.........: 1280/286887700 (0.00%)
Rejected.........: 0/1280 (0.00%)
Restore.Point....: 0/20 (0.00%)
Restore.Sub.#1...: Salt:0 Amplifier:0-64 Iteration:0-64
Candidates.#1....: 2001123456 -> 2017charlie

```


# Creating Custom Wordlists

* * *

## Wordlists

During an assessment, we may retrieve one or more password hashes that are crucial to the engagement's success. Despite our best attempts, these hashes cannot be cracked with common wordlists using the dictionary, combination, mask, or hybrid attacks covered in the prior sections. It may be necessary to create a custom, targeted wordlist to achieve our goal in these instances.

It is necessary to spend time refining a wordlist because the success rate heavily depends on it. Wordlists can be obtained from various sources and customized based on the target and further fine-tuned using rules. Wordlists can be found for passwords, usernames, file names, payloads, and many other data types. The [SecLists](https://github.com/danielmiessler/SecLists) repository also contains many wordlists useful for username enumeration password identification.

* * *

## Creating Wordlists

Many open-source tools help in creating customized password wordlists based on our requirements.

* * *

## Crunch

Crunch can create wordlists based on parameters such as words of a specific length, a limited character set, or a certain pattern. It can generate both permutations and combinations.

It is installed by default on Parrot OS and can be found [here](https://sourceforge.net/projects/crunch-wordlist/). The general syntax of `crunch` is as follows:

#### Crunch - Syntax

```shell
crunch <minimum length> <maximum length> <charset> -t <pattern> -o <output file>

```

The " `-t`" option is used to specify the pattern for generated passwords. The pattern can contain " `@`," representing lower case characters, " `,`" (comma) will insert upper case characters, " `%`" will insert numbers, and " `^`" will insert symbols.

#### Crunch - Generate Word List

```shell
crunch 4 8 -o wordlist

```

The command above creates a wordlist consisting of words with a length of 4 to 8 characters, using the default character set.

Let's assume that Inlane Freight user passwords are of the form " `ILFREIGHTYYYYXXXX`," where " `XXXX`" is the employee ID containing letters, and " `YYYY`" is the year. We can use `crunch` to create a list of such passwords.

#### Crunch - Create Word List using Pattern

```shell
crunch 17 17 -t ILFREIGHT201%@@@@ -o wordlist

```

The pattern " `ILFREIGHT201%@@@@`" will create words with the years 2010-2019 followed by four letters. The length here is 17, which is constant for all words.

If we know a user's birthdate is 10/03/1998 (through social media, etc.), we can include this in their password, followed by a string of letters. Crunch can be used to create a wordlist of such words. The " `-d`" option is used to specify the amount of repetition.

#### Crunch - Specified Repetition

```shell
crunch 12 12 -t 10031998@@@@ -d 1 -o wordlist

```

* * *

## CUPP

`CUPP` stands for `Common User Password Profiler`, and is used to create highly targeted and customized wordlists based on information gained from social engineering and OSINT. People tend to use personal information while creating passwords, such as phone numbers, pet names, birth dates, etc. CUPP takes in this information and creates passwords from them. These wordlists are mostly used to gain access to social media accounts. CUPP is installed by default on Parrot OS, and the repo can be found [here](https://github.com/Mebus/cupp). The " `-i`" option is used to run in interactive mode, prompting `CUPP` to ask us for information on the target.

#### CUPP - Usage Example

```shell
python3 cupp.py -i

[+] Insert the information about the victim to make a dictionary
[+] If you don't know all the info, just hit enter when asked! ;)

> First Name: roger
> Surname: penrose
> Nickname:
> Birthdate (DDMMYYYY): 11051972

> Partners) name: beth
> Partners) nickname:
> Partners) birthdate (DDMMYYYY):

> Child's name: john
> Child's nickname: johnny
> Child's birthdate (DDMMYYYY):

> Pet's name: tommy
> Company name: INLANE FREIGHT

> Do you want to add some key words about the victim? Y/[N]: Y
> Please enter the words, separated by comma. [i.e. hacker,juice,black], spaces will be removed: sysadmin,linux,86391512
> Do you want to add special chars at the end of words? Y/[N]:
> Do you want to add some random numbers at the end of words? Y/[N]:
> Leet mode? (i.e. leet = 1337) Y/[N]:

[+] Now making a dictionary...
[+] Sorting list and removing duplicates...
[+] Saving dictionary to roger.txt, counting 2419 words.
[+] Now load your pistolero with roger.txt and shoot! Good luck!

```

The command above shows how the data for the user Roger Penrose, was provided to CUPP. The unknown fields can be just left empty. After taking in all data, CUPP creates a wordlist based on it. It also supports appending random characters and a "Leet" mode, which uses combinations of letters and numbers in common words. `CUPP` can also fetch common names from various online databases using the " `-l`" option.

* * *

## KWPROCESSOR

`Kwprocessor` is a tool that creates wordlists with keyboard walks. Another common password generation technique is to follow patterns on the keyboard. These passwords are called keyboard walks, as they look like a walk along the keys. For example, the string " `qwertyasdfg`" is created by using the first five characters from the keyboard's first two rows. This seems complex to the normal eye but can be easily predicted. `Kwprocessor` uses various algorithms to guess patterns such as these.

The tool can be found [here](https://github.com/hashcat/kwprocessor) and has to be installed manually.

#### Kwprocessor - Installation

```shell
git clone https://github.com/hashcat/kwprocessor
cd kwprocessor
make

```

The help menu shows the various options supported by kwp. The pattern is based on the geographical directions a user could choose on the keyboard. For example, the " `--keywalk-west`" option is used to specify movement towards the west from the base character. The program takes in base characters as a parameter, which is the character set the pattern will start with. Next, it needs a keymap, which maps the locations of keys on language-specific keyboard layouts. The final option is used to specify the route to be used. A route is a pattern to be followed by passwords. It defines how passwords will be formed, starting from the base characters. For example, the route 222 can denote the path 2 \* EAST + 2 \* SOUTH + 2 \* WEST from the base character. If the base character is considered to be " `T`" then the password generated by the route would be " `TYUJNBV`" on a US keymap. For further information, refer to the [README](https://github.com/hashcat/kwprocessor#routes) for kwprocessor.

#### Kwprocessor - Example

```shell
kwp -s 1 basechars/full.base keymaps/en-us.keymap  routes/2-to-10-max-3-direction-changes.route

```

The command above generates words with characters reachable while holding shift ( `-s`), using the full base, the standard en-us keymap, and 3 direction changes route.

* * *

## Princeprocessor

`PRINCE` or `PRobability INfinite Chained Elements` is an efficient password guessing algorithm to improve password cracking rates. [Princeprocessor](https://github.com/hashcat/princeprocessor) is a tool that generates passwords using the PRINCE algorithm. The program takes in a wordlist and creates chains of words taken from this wordlist. For example, if a wordlist contains the words:

#### Wordlist

```shell
dog
cat
ball

```

The generated wordlist would be of the form:

#### Princeprocessor - Generated Wordlist

```shell
dog
cat
ball
dogdog
catdog
dogcat
catcat
dogball
catball
balldog
ballcat
ballball
dogdogdog
catdogdog
dogcatdog
catcatdog
dogdogcat
<SNIP>

```

The `PRINCE` algorithm considers various permutation and combinations while creating each word. The binary can be download from the [releases](https://github.com/hashcat/princeprocessor/releases) page.

#### Princeprocessor - Installation

```shell
wget https://github.com/hashcat/princeprocessor/releases/download/v0.22/princeprocessor-0.22.7z
7z x princeprocessor-0.22.7z
cd princeprocessor-0.22
./pp64.bin -h

```

The " `--keyspace`" option can be used to find the number of combinations produced from the input wordlist.

#### Princeprocessor - Find the Number of Combinations

```shell
./pp64.bin --keyspace < words

232

```

According to princeprocessor, 232 unique words can be formed from our wordlist above.

#### Princeprocessor - Forming Wordlist

```shell
./pp64.bin -o wordlist.txt < words

```

The command above writes the output words to a file named `wordlist.txt`. By default, princeprocessor only outputs words up to 16 in length. This can be controlled using the " `--pw-min`" and " `--pw-max`" arguments.

#### Princeprocessor - Password Length Limits

```shell
./pp64.bin --pw-min=10 --pw-max=25 -o wordlist.txt < words

```

The command above will output words between 10 and 25 in length. The number of elements per word can be controlled using " `--elem-cnt-min`" and " `--elem-cnt-max`". These values ensure that number of elements in an output word is above or below the given value.

#### Princeprocessor - Specifying Elements

```shell
./pp64.bin --elem-cnt-min=3 -o wordlist.txt < words

```

The command above will output words with three elements or more, i.e.," dogdogdog\`."

* * *

## CeWL

[CeWL](https://github.com/digininja/CeWL) is another tool that can be used to create custom wordlists. It spiders and scrapes a website and creates a list of the words that are present. This kind of wordlist is effective, as people tend to use passwords associated with the content they write or operate on. For example, a blogger who blogs about nature, wildlife, etc. could have a password associated with those topics. This is due to human nature, as such passwords are also easy to remember. Organizations often have passwords associated with their branding and industry-specific vocabulary. For example, users of a networking company may have passwords consisting of words like `router`, `switch`, `server`, and so on. Such words can be found on their websites under blogs, testimonials, and product descriptions.

The general syntax of `CeWL` is as follows:

#### CeWL - Syntax

```shell
cewl -d <depth to spider> -m <minimum word length> -w <output wordlist> <url of website>

```

CeWL can spider multiple pages present on a given website. The length of the outputted words can be altered using the " `-m`" parameter, depending on the password requirements (i.e., some websites have a minimum password length).

CeWL also supports the extraction of emails from websites with the " `-e`" option. It's helpful to get this information when phishing, password spraying, or brute-forcing passwords later.

#### CeWL - Example

```shell
cewl -d 5 -m 8 -e http://inlanefreight.com/blog -w wordlist.txt

```

The command above scrapes up to a depth of five pages from " `http://inlanefreight.com/blog`", and includes only words greater than 8 in length.

* * *

## Previously Cracked Passwords

By default, hashcat stores all cracked passwords in the `hashcat.potfile` file; the format is `hash:password`. The main purpose of this file is to remove previously cracked hashes from the work log and display cracked passwords with the `--show` command. However, it can be used to create new wordlists of previously cracked passwords, and when combined with rule files, it can prove quite effective at cracking themed passwords.

```shell
cut -d: -f 2- ~/hashcat.potfile

```

* * *

## Hashcat-utils

The Hashcat-utils [repo](https://github.com/hashcat/hashcat-utils) contains many utilities that can be useful for more advanced password cracking. The tool [maskprocessor](https://github.com/hashcat/maskprocessor), for example, can be used to create wordlists using a given mask. Detailed usage for this tool can be found [here](https://hashcat.net/wiki/doku.php?id=maskprocessor).

For example, `maskprocessor` can be used to append all special characters to the end of a word:

```shell
/mp64.bin Welcome?s
Welcome
Welcome!
Welcome"
Welcome#
Welcome$
Welcome%
Welcome&
Welcome'
Welcome(
Welcome)
Welcome*
Welcome+

<SNIP>

```


# Working with Rules

* * *

The rule-based attack is the most advanced and complex password cracking mode. Rules help perform various operations on the input wordlist, such as prefixing, suffixing, toggling case, cutting, reversing, and much more. Rules take mask-based attacks to another level and provide increased cracking rates. Additionally, the usage of rules saves disk space and processing time incurred as a result of larger wordlists.

A rule can be created using functions, which take a word as input and output it's modified version. The following table describes some functions which are compatible with JtR as well as Hashcat.

| **Function** | **Description** | **Input** | **Output** |
| --- | --- | --- | --- |
| l | Convert all letters to lowercase | InlaneFreight2020 | inlanefreight2020 |
| u | Convert all letters to uppercase | InlaneFreight2020 | INLANEFREIGHT2020 |
| c / C | capitalize / lowercase first letter and invert the rest | inlaneFreight2020 / Inlanefreight2020 | Inlanefreight2020 / iNLANEFREIGHT2020 |
| t / TN | Toggle case : whole word / at position N | InlaneFreight2020 | iNLANEfREIGHT2020 |
| d / q / zN / ZN | Duplicate word / all characters / first character / last character | InlaneFreight2020 | InlaneFreight2020InlaneFreight2020 / IInnllaanneeFFrreeiigghhtt22002200 / IInlaneFreight2020 / InlaneFreight20200 |
| { / } | Rotate word left / right | InlaneFreight2020 | nlaneFreight2020I / 0InlaneFreight202 |
| ^X / $X | Prepend / Append character X | InlaneFreight2020 (^! / $! ) | !InlaneFreight2020 / InlaneFreight2020! |
| r | Reverse | InlaneFreight2020 | 0202thgierFenalnI |

* * *

A complete list of functions can be found [here](https://hashcat.net/wiki/doku.php?id=rule_based_attack#implemented_compatible_functions). Sometimes, the input wordlists contain words that don't match our target specifications. For example, a company's password policy might not allow users to set passwords less than 7 characters in length. In such cases, rejection rules can be used to prevent the processing of such words.

Words of length less than N can be rejected with `>N`, while words greater than N can be rejected with `<N`. A list of rejection rules can be found [here](https://hashcat.net/wiki/doku.php?id=rule_based_attack#rules_used_to_reject_plains).

_Note: Reject rules only work either with `hashcat-legacy`, or when using `-j` or `-k` with `Hashcat`. They will not work as regular rules (in a rule file) with `Hashcat`._

* * *

## Example Rule Creation

Let's look at how we can create a rule based on common passwords. Usual user behavior suggests that they tend to replace letters with similar numbers, like " `o`" can be replaced with " `0`" or " `i`" can be replaced with " `1`". This is commonly known as `L33tspeak` and is very efficient. Corporate passwords are often prepended or appended by a year. Let's create a rule to generate such words.

\*Note: Reject rules only work either with `hashcat-legacy`, or when using `-j` or `-k` with `Hashcat`. They will not work as regular rules (in a rule file) with `Hashcat`. \*

#### Rules

```shell
c so0 si1 se3 ss5 sa@ $2 $0 $1 $9

```

The first letter word is capitalized with the `c` function. Then rule uses the substitute function `s` to replace `o` with `0`, `i` with `1`, `e` with `3` and a with `@`. At the end, the year `2019` is appended to it. Copy the rule to a file so that we can debug it.

#### Create a Rule File

```shell
echo 'c so0 si1 se3 ss5 sa@ $2 $0 $1 $9' > rule.txt

```

#### Store the Password in a File

```shell
echo 'password_ilfreight' > test.txt

```

* * *

Rules can be debugged using the " `-r`" flag to specify the rule, followed by the wordlist.

#### Hashcat - Debugging Rules

```shell
hashcat -r rule.txt test.txt --stdout

P@55w0rd_1lfr31ght2019

```

As expected, the first letter was capitalized, and the letters were replaced with numbers. Let's consider the password " `St@r5h1p2019`". We can create the `SHA1` hash of this password via the command line:

#### Generate SHA1 Hash

```shell
echo -n 'St@r5h1p2019' | sha1sum | awk '{print $1}' | tee hash

```

We can then use the custom rule created above and the `rockyou.txt` dictionary file to crack the hash using `Hashcat`.

#### Hashcat - Cracking Passwords Using Wordlists and Rules

```shell
hashcat -a 0 -m 100 hash /opt/useful/seclists/Passwords/Leaked-Databases/rockyou.txt -r rule.txt

hashcat (v6.1.1) starting...
<SNIP>

08004e35561328e357e34d07c53c7e4f41944e28:St@r5h1p2019

Session..........: hashcat
Status...........: Cracked
Hash.Name........: SHA1
Hash.Target......: 08004e35561328e357e34d07c53c7e4f41944e28
Time.Started.....: Fri Aug 28 22:17:13 2020, (3 secs)
Time.Estimated...: Fri Aug 28 22:17:16 2020, (0 secs)
Guess.Base.......: File (/opt/useful/seclists/Passwords/Leaked-Databases/rockyou.txt)
Guess.Mod........: Rules (rule.txt)
Guess.Queue......: 1/1 (100.00%)
Speed.#1.........:  3519.2 kH/s (0.39ms) @ Accel:1024 Loops:1 Thr:1 Vec:8
Recovered........: 1/1 (100.00%) Digests
Progress.........: 10592256/14344385 (73.84%)
Rejected.........: 0/10592256 (0.00%)
Restore.Point....: 10586112/14344385 (73.80%)
Restore.Sub.#1...: Salt:0 Amplifier:0-1 Iteration:0-1
Candidates.#1....: St0p69692019 -> S0r051x53nt2019

```

We were able to crack the hash with our custom rule and rockyou.txt. Hashcat supports the usage of multi-rules with repeated use of the `-r` flag. `Hashcat` installs with a variety of rules by default. They can be found in the rules folder.

#### Hashcat - Default Rules

```shell
ls -l /usr/share/hashcat/rules/

total 2576
-rw-r--r-- 1 root root    933 Jun 19 06:20 best64.rule
-rw-r--r-- 1 root root    633 Jun 19 06:20 combinator.rule
-rw-r--r-- 1 root root 200188 Jun 19 06:20 d3ad0ne.rule
-rw-r--r-- 1 root root 788063 Jun 19 06:20 dive.rule
-rw-r--r-- 1 root root 483425 Jun 19 06:20 generated2.rule
-rw-r--r-- 1 root root  78068 Jun 19 06:20 generated.rule
drwxr-xr-x 1 root root   2804 Jul  9 21:01 hybrid
-rw-r--r-- 1 root root 309439 Jun 19 06:20 Incisive-leetspeak.rule
-rw-r--r-- 1 root root  35280 Jun 19 06:20 InsidePro-HashManager.rule
-rw-r--r-- 1 root root  19478 Jun 19 06:20 InsidePro-PasswordsPro.rule
-rw-r--r-- 1 root root    298 Jun 19 06:20 leetspeak.rule
-rw-r--r-- 1 root root   1280 Jun 19 06:20 oscommerce.rule
-rw-r--r-- 1 root root 301161 Jun 19 06:20 rockyou-30000.rule
-rw-r--r-- 1 root root   1563 Jun 19 06:20 specific.rule
-rw-r--r-- 1 root root  64068 Jun 19 06:20 T0XlC-insert_00-99_1950-2050_toprules_0_F.rule
-rw-r--r-- 1 root root   2027 Jun 19 06:20 T0XlC-insert_space_and_special_0_F.rule
-rw-r--r-- 1 root root  34437 Jun 19 06:20 T0XlC-insert_top_100_passwords_1_G.rule
-rw-r--r-- 1 root root  34813 Jun 19 06:20 T0XlC.rule
-rw-r--r-- 1 root root 104203 Jun 19 06:20 T0XlCv1.rule
-rw-r--r-- 1 root root     45 Jun 19 06:20 toggles1.rule
-rw-r--r-- 1 root root    570 Jun 19 06:20 toggles2.rule
-rw-r--r-- 1 root root   3755 Jun 19 06:20 toggles3.rule
-rw-r--r-- 1 root root  16040 Jun 19 06:20 toggles4.rule
-rw-r--r-- 1 root root  49073 Jun 19 06:20 toggles5.rule
-rw-r--r-- 1 root root  55346 Jun 19 06:20 unix-ninja-leetspeak.rule

```

It is always better to try using these rules before going ahead and creating custom rules.

`Hashcat` provides an option to generate random rules on the fly and apply them to the input wordlist. The following command will generate 1000 random rules and apply them to each word from `rockyou.txt` by specifying the " `-g`" flag. There is no certainty to the success rate of this attack as the generated rules are not constant.

#### Hashcat - Generate Random Rules

```shell
hashcat -a 0 -m 100 -g 1000 hash /opt/useful/seclists/Passwords/Leaked-Databases/rockyou.txt

```

There are a variety of publicly available rules as well, such as the [nsa-rules](https://github.com/NSAKEY/nsa-rules), [Hob0Rules](https://github.com/praetorian-code/Hob0Rules), and the [corporate.rule](https://github.com/sparcflow/HackLikeALegend/blob/master/old/chap3/corporate.rule) which is featured in the book [How to Hack Like a Legend](https://www.sparcflow.com/new-release-hack-like-legend/). These are curated rulesets generally targeted at common corporate Windows password policies or based on statistics and probably industry password patterns.

On an engagement or password cracking exercise, it is generally best to start with small targeted wordlists and rule sets, especially if the password policy is known or we have a general idea of the policy. Extremely large dictionary files combined with large rule sets can be effective as well. Still, we are limited by our computing power (i.e., a laptop with a single CPU will not be able to run `Hashcat` jobs with as large a word list and rule set as a password cracking rig with 8x 2080ti GPUs). Understanding the power of rules will help us greatly refine our password cracking abilities, saving both time and resources in the process.


# Cracking Common Hashes

* * *

## Common Hash Types

During penetration test engagements, we encounter a wide variety of hash types; some are extremely common and seen on most engagements, while others are seen very rarely or not at all. As stated previously, the creators of `Hashcat` maintain a list of [example hashes](https://hashcat.net/wiki/doku.php?id=example_hashes) most hash modes that `Hashcat` supports. The list includes the hash mode, hash name, and a sample hash of the specified type. Some of the most commonly seen hashes are:

| Hashmode | Hash Name | Example Hash |
| --- | --- | --- |
| 0 | MD5 | 8743b52063cd84097a65d1633f5c74f5 |
| 100 | SHA1 | b89eaac7e61417341b710b727768294d0e6a277b |
| 1000 | NTLM | b4b9b02e6f09a9bd760f388b67351e2b |
| 1800 | sha512crypt $6$, SHA512 (Unix) | $6$52450745$k5ka2p8bFuSmoVT1tzOyyuaREkkKBcCNqoDKzYiJL9RaE8yMnPgh2XzzF0NDrUhgrcLwg78xs1w5pJiypEdFX/ |
| 3200 | bcrypt $2\*$, Blowfish (Unix) | $2a$05$LhayLxezLhK1LhWvKxCyLOj0j1u.Kj0jZ0pEmm134uzrQlFvQJLF6 |
| 5500 | NetNTLMv1 / NetNTLMv1+ESS | u4-netntlm::kNS:338d08f8e26de93300000000000000000000000000000000:9526fb8c23a90751cdd619b6cea564742e1e4bf33006ba41:cb8086049ec4736c |
| 5600 | NetNTLMv2 | admin::N46iSNekpT:08ca45b7d7ea58ee:88dcbe4446168966a153a0064958dac6:5c7830315c7830310000000000000b45c67103d07d7b95acd12ffa11230e0000000052920b85f78d013c31cdb3b92f5d765c783030 |
| 13100 | Kerberos 5 TGS-REP etype 23 | $krb5tgs$23$ _user$realm$test/spn_ $63386d22d359fe42230300d56852c9eb$ < SNIP > |

* * *

## Example 1 - Database Dumps

MD5, SHA1, and bcrypt hashes are often seen in database dumps. These hashes may be retrieved following a successful SQL injection attack or found in publicly available password data breach database dumps. MD5 and SHA1 are typically easier to crack than bcrypt, which may have many rounds of the Blowfish algorithm applied.

Let's crack some SHA1 hashes. Take the following list:

#### SHA1 Hashes List

```shell
winter!
baseball1
waterslide
summertime
baconandeggs
beach1234
sunshine1
welcome1
password123

```

We can create a SHA1 of each word quickly:

#### Generate SHA1 Hashes

```shell
for i in $(cat words); do echo -n $i | sha1sum | tr -d ' -';done

fa3c9ecfc251824df74026b4f40e4b373fd4fc46
e6852777c0260493de41fb43918ab07bbb3a659c
0c3feaa16f73493f998970e22b2a02cb9b546768
b863c49eada14e3a8816220a7ab7054c28693664
b0feedd70a346f7f75086026169825996d7196f9
f47f832cba913ec305b07958b41babe2e0ad0437
08b314f0e1e2c41ec92c3735910658e5a82c6ba7
e35bece6c5e6e0e86ca51d0440e92282a9d6ac8a
cbfdac6008f9cab4083784cbd1874f76618d2a97

```

We can then run these through a `Hashcat` dictionary attack using the `rockyou.txt` wordlist.

```shell
hashcat -m 100 SHA1_hashes /opt/useful/seclists/Passwords/Leaked-Databases/rockyou.txt

hashcat (v6.1.1) starting...
<SNIP>

08b314f0e1e2c41ec92c3735910658e5a82c6ba7:sunshine1
e35bece6c5e6e0e86ca51d0440e92282a9d6ac8a:welcome1
e6852777c0260493de41fb43918ab07bbb3a659c:baseball1
b863c49eada14e3a8816220a7ab7054c28693664:summertime
fa3c9ecfc251824df74026b4f40e4b373fd4fc46:winter!
b0feedd70a346f7f75086026169825996d7196f9:baconandeggs
f47f832cba913ec305b07958b41babe2e0ad0437:beach1234
0c3feaa16f73493f998970e22b2a02cb9b546768:waterslide

Session..........: hashcat
Status...........: Cracked
Hash.Name........: SHA1
Hash.Target......: SHA1_hashes
Time.Started.....: Fri Aug 28 22:22:56 2020, (1 sec)
Time.Estimated...: Fri Aug 28 22:22:57 2020, (0 secs)
Guess.Base.......: File (/opt/useful/seclists/Passwords/Leaked-Databases/rockyou.txt)
Guess.Queue......: 1/1 (100.00%)
Speed.#1.........:  2790.2 kH/s (0.33ms) @ Accel:1024 Loops:1 Thr:1 Vec:8
Recovered........: 9/9 (100.00%) Digests
Progress.........: 1173504/14344385 (8.18%)
Rejected.........: 0/1173504 (0.00%)
Restore.Point....: 1167360/14344385 (8.14%)
Restore.Sub.#1...: Salt:0 Amplifier:0-1 Iteration:0-1
Candidates.#1....: whitenerdy -> warut69

```

The above hashes cracked very quickly as they are common words/phrases with little to no complexity. Variations on the above list, such as " `Bas3b@ll1`" or " `Wat3rSl1de`" would likely take longer to crack and may require additional techniques such as mask and hybrid attacks.

* * *

## Example 2 - Linux Shadow File

Sha512crypt hashes are commonly found in the `/etc/shadow` file on Linux systems. This file contains the password hashes for all accounts with a login shell assigned to them. We may gain access to a Linux system during a penetration test via a web application attack or successful exploitation of a vulnerable service. We may exploit a service that is already running in the context of the highest privileged `root` account and perform a successful privilege escalation attack and access the `/etc/shadow` file. Password re-use is widespread. A cracked password may give us access to other servers, network devices, or even be used as a foothold into a target's Active Directory environment.

Let's look at a hash from a standard Ubuntu installation. The corresponding plaintext for the following hash is " `password123`".

#### Root Password in Ubuntu Linux

```shell
root:$6$tOA0cyybhb/Hr7DN$htr2vffCWiPGnyFOicJiXJVMbk1muPORR.eRGYfBYUnNPUjWABGPFiphjIjJC5xPfFUASIbVKDAHS3vTW1qU.1:18285:0:99999:7:::

```

The hash contains nine fields separated by colons. The first two fields contain the username and its encrypted hash. The rest of the fields contain various attributes such as password creation time, last change time, and expiry.

Coming to the hash, we already know that it contains three fields delimited by " `$`". The value " `6`" stands for the SHA-512 hashing algorithm; the next 16 characters represent the salt, while the rest of it is the actual hash.

Let's crack this hash using `Hashcat`.

```shell
hashcat -m 1800 nix_hash /opt/useful/seclists/Passwords/Leaked-Databases/rockyou.txt

hashcat (v6.1.1) starting...
<SNIP>

$6$tOA0cyybhb/Hr7DN$htr2vffCWiPGnyFOicJiXJVMbk1muPORR.eRGYfBYUnNPUjWABGPFiphjIjJC5xPfFUASIbVKDAHS3vTW1qU.1:password123

Session..........: hashcat
Status...........: Cracked
Hash.Name........: sha512crypt $6$, SHA512 (Unix)
Hash.Target......: $6$tOA0cyybhb/Hr7DN$htr2vffCWiPGnyFOicJiXJVMbk1muPO...W1qU.1
Time.Started.....: Fri Aug 28 22:25:26 2020, (1 sec)
Time.Estimated...: Fri Aug 28 22:25:27 2020, (0 secs)
Guess.Base.......: File (/opt/useful/seclists/Passwords/Leaked-Databases/rockyou.txt)
Guess.Queue......: 1/1 (100.00%)
Speed.#1.........:      955 H/s (4.62ms) @ Accel:32 Loops:256 Thr:1 Vec:4
Recovered........: 1/1 (100.00%) Digests
Progress.........: 1536/14344385 (0.01%)
Rejected.........: 0/1536 (0.00%)
Restore.Point....: 1344/14344385 (0.01%)
Restore.Sub.#1...: Salt:0 Amplifier:0-1 Iteration:4864-5000
Candidates.#1....: teacher -> mexico1

```

* * *

## Example 3 - Common Active Directory Password Hash Types

Credential theft and password re-use are widespread tactics during assessments against organizations using Active Directory to manage their environment. It is often possible to obtain credentials in cleartext or re-use password hashes to further access via Pass-the-Hash or SMB Relay attacks. Still, some techniques will result in a password hash that must be cracked offline to further our access. Some examples include a NetNTLMv1 or NetNTLMv2 obtained through a Man-in-the-middle (MITM) attack, a Kerberos 5 TGS-REP hash obtained through a Kerberoasting attack, or an NTLM hash obtained either by dumping credentials from memory using the `Mimikatz` tool or obtained from a Windows machine's local SAM database.

* * *

#### NTLM

One example is retrieving an NTLM password hash for a user that has Remote Desktop (RDP) access to a server but is not a local administrator, so the NTLM hash cannot be used for a pass-the-hash attack to gain access. In this case, the cleartext password is necessary to further our access by connecting to the server via RDP and performing further enumeration within the network or looking for local privilege escalation vectors.

Let's walk through an example. We can quickly generate an NTLM hash of the password " `Password01`" for our purposes using 3 lines of Python:

#### Python3 - Hashlib

```shell
python3

Python 3.8.3 (default, May 14 2020, 11:03:12)
[GCC 9.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.

>>> import hashlib,binascii
>>> hash = hashlib.new('md4', "Password01".encode('utf-16le')).digest()
>>> print (binascii.hexlify(hash))

b'7100a909c7ff05b266af3c42ec058c33'

```

We can then run the resultant NTLM password hash value " `7100a909c7ff05b266af3c42ec058c33`" through `Hashcat` using the standard `rockyou.txt` wordlist to retrieve the cleartext.

#### Hashcat - Cracking NTLM Hashes

```shell
hashcat -a 0 -m 1000 ntlm_example /opt/useful/seclists/Passwords/Leaked-Databases/rockyou.txt

hashcat (v6.1.1) starting...
<SNIP>

7100a909c7ff05b266af3c42ec058c33:Password01

Session..........: hashcat
Status...........: Cracked
Hash.Name........: NTLM
Hash.Target......: 7100a909c7ff05b266af3c42ec058c33
Time.Started.....: Fri Aug 28 22:27:40 2020, (0 secs)
Time.Estimated...: Fri Aug 28 22:27:40 2020, (0 secs)
Guess.Base.......: File (/opt/useful/seclists/Passwords/Leaked-Databases/rockyou.txt)
Guess.Queue......: 1/1 (100.00%)
Speed.#1.........:  2110.5 kH/s (0.62ms) @ Accel:1024 Loops:1 Thr:1 Vec:8
Recovered........: 1/1 (100.00%) Digests
Progress.........: 61440/14344385 (0.43%)
Rejected.........: 0/61440 (0.00%)
Restore.Point....: 55296/14344385 (0.39%)
Restore.Sub.#1...: Salt:0 Amplifier:0-1 Iteration:0-1
Candidates.#1....: gonoles -> sinead1

```

Now, armed with the cleartext password, we can further our access within the network.

* * *

#### NetNTLMv2

During a penetration test it is common to run tools such as [Responder](https://github.com/lgandx/Responder) to perform MITM attacks to attempt to "steal" credentials. These types of attacks are covered in-depth in other modules. In busy corporate networks it is common to retrieve many NetNTLMv2 password hashes using this method. These can often be cracked and leveraged to establish a foothold in the Active Directory environment or sometimes even gain full administrative access to many or all systems depending on the privileges granted to the user account associated with the password hash. Consider the password hash below retrieved using `Responder` at the beginning of an assessment:

#### Responder - NTLMv2

```shell
sqladmin::INLANEFREIGHT:f54d6f198a7a47d4:7FECABAE13101DAAA20F1B09F7F7A4EA:0101000000000000C0653150DE09D20126F3F71DF13C1FD8000000000200080053004D004200330001001E00570049004E002D00500052004800340039003200520051004100460056000400140053004D00420033002E006C006F00630061006C0003003400570049004E002D00500052004800340039003200520051004100460056002E0053004D00420033002E006C006F00630061006C000500140053004D00420033002E006C006F00630061006C0007000800C0653150DE09D201060004000200000008003000300000000000000000000000003000001A67637962F2B7BF297745E6074934196D5F4371B6BA3E796F2997306FD4C1C00A001000000000000000000000000000000000000900280063006900660073002F003100390032002E003100360038002E003100390035002E00310037003000000000000000000000000000

```

Some tools, such as `Responder`, will inform you what type of hash was received. We can also check the [Example hashes](https://hashcat.net/wiki/doku.php?id=example_hashes) page if in doubt and confirm that this is indeed a NetNTLMv2 hash, or mode `5600` in `Hashcat`.

As with the previous examples, we can run this hash with `Hashcat` using the `rockyou.txt` wordlist to perform an offline dictionary attack.

#### Hashcat - Cracking NTLMv2 Hashes

```shell
hashcat -a 0 -m 5600 inlanefreight_ntlmv2 /opt/useful/seclists/Passwords/Leaked-Databases/rockyou.txt

hashcat (v6.1.1) starting...
<SNIP>

SQLADMIN::INLANEFREIGHT:f54d6f198a7a47d4:7fecabae13101daaa20f1b09f7f7a4ea:0101000000000000c0653150de09d20126f3f71df13c1fd8000000000200080053004d004200330001001e00570049004e002d00500052004800340039003200520051004100460056000400140053004d00420033002e006c006f00630061006c0003003400570049004e002d00500052004800340039003200520051004100460056002e0053004d00420033002e006c006f00630061006c000500140053004d00420033002e006c006f00630061006c0007000800c0653150de09d201060004000200000008003000300000000000000000000000003000001a67637962f2b7bf297745e6074934196d5f4371b6ba3e796f2997306fd4c1c00a001000000000000000000000000000000000000900280063006900660073002f003100390032002e003100360038002e003100390035002e00310037003000000000000000000000000000:Database99

Session..........: hashcat
Status...........: Cracked
Hash.Name........: NetNTLMv2
Hash.Target......: SQLADMIN::INLANEFREIGHT:f54d6f198a7a47d4:7fecabae13...000000
Time.Started.....: Fri Aug 28 22:29:26 2020, (6 secs)
Time.Estimated...: Fri Aug 28 22:29:32 2020, (0 secs)
Guess.Base.......: File (/opt/useful/seclists/Passwords/Leaked-Databases/rockyou.txt)
Guess.Queue......: 1/1 (100.00%)
Speed.#1.........:  1754.7 kH/s (2.32ms) @ Accel:1024 Loops:1 Thr:1 Vec:8
Recovered........: 1/1 (100.00%) Digests
Progress.........: 11237376/14344385 (78.34%)
Rejected.........: 0/11237376 (0.00%)
Restore.Point....: 11231232/14344385 (78.30%)
Restore.Sub.#1...: Salt:0 Amplifier:0-1 Iteration:0-1
Candidates.#1....: Devanique -> Darrylw

```

Armed with these credentials, we're off to the races and can begin enumerating and attacking Active Directory, covered in-depth in later modules.


# Cracking Miscellaneous Files & Hashes

* * *

During penetration tests and other assessments, it is very common to encounter password-protected documents such as Microsoft Word and Excel documents, OneNote notebooks, KeePass database files, SSH private key passphrases, PDF files, zip (and other archive formats) files, and more. The majority of these hashes can be run through `Hashcat` to attempt to crack the hashes.

* * *

## Tools

Various tools exist to help us extract the password hashes from these files in a format that `Hashcat` can understand. The password cracking tool `JohnTheRipper` comes with many of these tools written in C that are available when installing `JohnTheRipper` or compiling it from its source code. They can be viewed [here](https://github.com/magnumripper/JohnTheRipper/tree/bleeding-jumbo/src). To use these tools, we need to compile them.

#### JohnTheRipper - Installation

```shell
sudo git clone https://github.com/magnumripper/JohnTheRipper.git
cd JohnTheRipper/src
sudo ./configure && sudo make

```

There are also Python ports of most of these tools available that are very easy to work with. The majority of them are contained in the `JohnTheRipper` jumbo GitHub repo [here](https://github.com/magnumripper/JohnTheRipper/tree/bleeding-jumbo/run).

One additional tool ported to Python by @Harmj0y is the [keepass2john.py](https://gist.github.com/HarmJ0y/116fa1b559372804877e604d7d367bbc#file-keepass2john-py) tool for extracting a crackable hash from KeePass 1.x/2.x databases that can be run through `Hashcat`

* * *

## Example 1 - Cracking Password Protected Microsoft Office Documents

`Hashcat` can be used to attempt to crack password hashes extracted from some Microsoft Office documents using the [office2john.py](https://raw.githubusercontent.com/magnumripper/JohnTheRipper/bleeding-jumbo/run/office2john.py) tool.

`Hashcat` supports the following hash modes for Microsoft Office documents:

| **Mode** | **Target** |
| --- | --- |
| `9400` | MS Office 2007 |
| `9500` | MS Office 2010 |
| `9600` | MS Office 2013 |

There are also several " `$oldoffice$`" hash modes for MS Office documents older than 2003. Let's take a Word document protected with the password " `pa55word`". We can first extract the hash from the document using `office2john.py`.

#### Extract Hash

```shell
python office2john.py hashcat_Word_example.docx

hashcat_Word_example.docx:$office$*2013*100000*256*16*6e059661c3ed733f5730eaabb41da13a*aa38e007ee01c07e4fe95495934cf68f*2f1e2e9bf1f0b320172cd667e02ad6be1718585b6594691907b58191a6

```

We can then run the hash through `Hashcat` using mode `9600` and make short work of it with the `rockyou.txt` wordlist. This is a rather slow hash to crack and will take over 12 hours to run through the entire `rockyou.txt` wordlist on a single CPU. This will be much faster on a GPU or several GPUs but still much slower than other hashes such as `MD5` and `NTLM`. Luckily for us as penetration testers, users often select very weak passwords to password-protect their documents!

#### Hashcat - Cracking MS Office Passwords

```shell
hashcat -m 9600 office_hash /opt/useful/seclists/Passwords/Leaked-Databases/rockyou.txt

hashcat (v6.1.1) starting...
<SNIP>

$office$*2013*100000*256*16*6e059661c3ed733f5730eaabb41da13a*aa38e007ee01c07e4fe95495934cf68f*2f1e2e9bf1f0b320172cd667e02ad6be1718585b6594691907b58191a6489940:pa55word

Session..........: hashcat
Status...........: Cracked
Hash.Name........: MS Office 2013
Hash.Target......: $office$*2013*100000*256*16*6e059661c3ed733f5730eaa...489940
Time.Started.....: Fri Aug 28 22:32:08 2020, (18 secs)
Time.Estimated...: Fri Aug 28 22:32:26 2020, (0 secs)
Guess.Base.......: File (/opt/useful/seclists/Passwords/Leaked-Databases/rockyou.txt)
Guess.Queue......: 1/1 (100.00%)
Speed.#1.........:      327 H/s (5.58ms) @ Accel:1024 Loops:32 Thr:1 Vec:8
Recovered........: 1/1 (100.00%) Digests
Progress.........: 6144/14344385 (0.04%)
Rejected.........: 0/6144 (0.00%)
Restore.Point....: 0/14344385 (0.00%)
Restore.Sub.#1...: Salt:0 Amplifier:0-1 Iteration:0-1
Candidates.#1....: 123456 -> iheartyou

```

* * *

## Example 2 - Cracking Password Protected Zip Files

During an assessment, we may find an interesting zip file, but it is password protected! We can extract these hashes using the compiled version of the [zip2john](https://github.com/magnumripper/JohnTheRipper/blob/bleeding-jumbo/src/zip2john.c) tool. `Hashcat` supports a variety of compressed file formats such as:

| **Mode** | **Target** |
| --- | --- |
| `11600` | 7-Zip |
| `13600` | WinZip |
| `17200` | PKZIP (Compressed) |
| `17210` | PKZIP (Uncompressed) |
| `17220` | PKZIP (Compressed Multi-File) |
| `17225` | PKZIP (Mixed Multi-File) |
| `17230` | PKZIP (Compressed Multi-File Checksum-Only) |
| `23001` | SecureZIP AES-128 |
| `23002` | SecureZIP AES-192 |
| `23003` | SecureZIP AES-256 |

For our example, we can take any document and add it to a password protected zip file in Parrot using the following command:

#### Set Password for a ZIP File

```shell
zip --password zippyzippy blueprints.zip dummy.pdf

adding: dummy.pdf (deflated 7%)

```

We can then use the compiled version of `zip2john` to extract the hash in a format that can be run through `Hashcat`.

#### Extract Hash

```shell
zip2john ~/Desktop/HTB/Academy/Cracking\ with\ Hashcat/blueprints.zip

ver 2.0 efh 5455 efh 7875 blueprints.zip/dummy.pdf PKZIP Encr: 2b chk, TS_chk, cmplen=12324, decmplen=13264, crc=7EB29321
blueprints.zip/dummy.pdf:$pkzip2$1*2*2*0*3024*33d0*7eb29321*0*43*8*3024*7eb2*69f2*d796c9cde7b7ed8d7b76c1efd12d222d2bfcc7a2e5a94b21a55c965c36c5875ea17ba1ca63d8164dc214c8845fa20fab19ab90287ced1d06dd577ec86fe0bc7d09407d06c33369ed0b9e40b12c399b79afd32a72170b67726f76db9090872aff5d1d6adc628e19fb074621e7b76a88cafbb866c8601d8464b642de8d85536e7dbac9e7fbc29be2b9d449d139a23739788b71ada0960faeb05bf4792f4b605f4153b25fc2fd360bdc41556af9ebd5f1861f3432abb84f745e7c223a1e9c9649a329337c11be4acef01ceff8ab29bd07cd2ae540743018751ea2ac7f8357189b70ab0c713775d217b3f0bd5be591378f85c91dff66cd0f9d277a22c346f3cb540c904a8a3cc77e918372417e241c1510dc1ca0887142206ce7d5cf6cc6f5f4c92df425f095333fd142376e0e87b85f71ce0c37c5099b770669463e4787ab379738c40df8f3421c27ec97f81411faca80ecd32b8b1556f86d86a90866139fac2421448730276aae0ad1586c0b591becdd7fbb759411f66bd7b542f3767be0ec7d1664fe65c28898b5a597fff8f178c49347147a7937f64c984ce7ea90325e082226439715acdfd95df9894d7e3a890d923844353613ff87fbfe978176a45b78bd64e439ea29ddc351edb2450e2f9af2e23f87a3b3a67af62a51f2d1bd3a535a4e831ef046cd01dd84dc979ddcff10cf1738afb8a6c77f37e46c2542c6cfc908a85932a74ee9728fd5adcafb336bfec71c4671f6d42de90a8d474af88a1774bd350bd3f56b20c45eb5cce0c8541167d863ee2d74fdb64f1bde532aa5c0a62d5877b54970d3ac56a0fbd8f2ac568196414767a4a3ca2516dc6aeb8413474bf97e12272c2c18f200600caf7c6bb58b6d42d01f9c13f48dc51913486d586c22a566992b4d111a7847b557fe1ccc55010f9dc9a62d1634b95f3b947bf573688a1fc5cb05c3a4a7a98043326c05e164b7f325d7139337b272562750b2fec49491c9241a25c8c0b61e8a2034e48bf0d0b56d43de8a3c908df1df798f0c9ea7b09aa44e6fdfbc4fb561b6e2548a9b6e91528cb14d269e1c2da9fe79e8f7a405a0a985db9da6b1656c8a94e3f5a29d4803354b4b601e9ed2578204b741c72a0266e0fd6b62e6f426caac7ea90188760ab75c93e43f93e7298fdf62505ad668caa21f0721fc4ff62d1b8d4b52bde5a336f0dbec60530d39a536139189ce436a3a80e560cff735a20f167426b4b95b0195c7198d330144a132e3dc44447d089cff7758e9d4ea68343f232f6b64a66974f5f47dd179c258c65e02474a403dd261b62756535f93ba88daba4a8bad51f1479be44bdabcbe25fe3a7bef0a158c42ffb89d90544352ae87118dc62c2e6c63bc8e4281822127207b5691c89056d825f84fca7335ad785344295f54652504bdc5d4d56cff94d27dc176a0726f672057996d08a4339fecc4d921cfc587a1f06e0f31d0f9b359cc09feac0f80584c05e2b61634387e702d8162ee60626605473837788a60e036f4432d4d777316efd6d89c40ef618bf3507cd0e632d6ad2e5f777013f99e708adcbc0a18a80f7a24a214e771a229faa1ec5f289d5f730b20e387b397bb10b1c0819ed8bdf4bed1edd1bee3c6c567c20f5a9506e316b631f5c302f54601d5b276fd722aa84942b8aaf9f6a29f8f6aa686533d296a4414426c023830a063f0fa74739b19618257ae5fec18f9d7ae222ca4d2703c604712625a7f737d3463eb258f21921f50f147bb65bfe9e8d2f7816d346ea363ed9ea1e06352d1369ebf6650cf4523c420cc89a5f5c5033d44699fac7472abe99177a9c8b72e08f4407255c88cf133207a999e7185a5e8555db3236fb5aebbf917e3eaf10faa7321d7d31c54e435cceb600d00dbfdbb55316cf3a4485a44df711a349468c176c8f5f395c4fcaba87bd99bf29d46507211a0a71d9586179575ff0df64e3296564f05d82f5bcf90316e669303119af8535f112334fca800189ccf2d0c886c12b33f723a58dfb40eec824e3fb7fd3775484fae42292fc22e1de241f0b0ed7c7ef5ffba4c5e8db1a85ff6a9242ff6ceac6be495aa8413a913042bd08b51a817bed4a280835390aea61611c1ed3cb3b0e923820bd7548c477db8f50dc7702c9ee65c5b082b5221dc71e812444c3f9f33092c184994e890f0604bce91a4147646216facf58c5206eb2c848f33fd922b4f13daca37af90e874b547b2ad2c5629b8bab40a5d16301ef21ccd32b795f2d0b87584def944af4f733e0314f99a3522995b1fb2cc117a652f063bcbef3e8c8b58b6ed1bc22f0249d9ff7a55dd446910992b06582ffce257fc3f72454cc85f7ed220285c440e5ffa1a7e1b989404df1b4540dec84185589929c453ad402071781201b2c5961e04586a1dca94be1ec1e23b87161a6809358b1ba5a008a8e577ba9fd13368a599a0a01f24be662c2defa3d6f302e9099e432c2df8d4c5aed8cf1613701364e70035257288d9188dc76602e994ab9f7c6949891b4b58f2f944d4c1b9c2f15ef2db58e1f0b687f6af5e5749febfe1ebd9921ef20cf7774c49a75bb1b9a5d63ca44b47cdaa17c28b8ad119ae62bdda99dea3de7bbaefc06339d006d7f64465f90f8160143a51e1683a668f02cf646995ac3786b5d0afdc022125c42046a07a9affc3146b69f496a3070cc536ef3165d1ebfd0c51c4fcfba7cb3c218d98df8c86c3bc8fabd0717af68244dab5acf1cf60ac76236261cd6966598d51ccbf160e83e667ad5c3c75f43b4874a7cfcd7c9aab1703bef256aa9cbd8df334df150af2d03ff10e664b409c34920b0f737b26d5d536bc74fbc814f771753aa8465ee422e087b4a8215843d7e206849130d8d7209dedf3acd0bb1e64557e5875d57bae8d51a243a8a253c597a4302fc1b7162ed888730e5f50f13f51ceaddb65bfa10ee15dc95fa2ca0c3f2c34bad9129e98144df6e9be3c1edead6a3d0e7e0c70fae70fea2fcd644bc172b064c85a35f3869b734b187ef69671688f1780b285648967abada2040098b3c6727a882dc43b591a716dc93c75e2c48d055a2269c4391332c8aee5d40466341dac0884dbdba7e056b1d900018452a79ad1177e23c15dce167c0017a24ab251a768a6cd15add944495292ff6e1f8819aba82dd3566803e2432e871f686899fcc21d166dfbf12c1dcbbf471136b3d6a72c34d8f153ef8e6f66730953dd2defb6bde7b51765119bd2122efec22d9597ae07ce2635ec78d5f36d7213378000b23fc7668a1d998007baf6032d5baa7e6d2e906eb91257afbf4695fa80b6bb84e089287fea77fa1b929da2ee7d22e573ed780240aacd0490467e456661644c1e054edb1ff1481de0be23b980cf97667f578e4f391f7cd46d05a85c5c267669bd7ff6912902e1d65875c35f656461fb6f9ce7cbdacf3e3ff85a746b058c1a35845e58096c1679eac222bb0f14267c7ff639f775d15ffe4eae62b6e8fcd2ecd8cc97bd0f6c69ec8887f3baf88955d4a573f366a2dfcf9db548c8027dc5bd27a2353ca2abadb1be6dec28fa19734e728442763344afe898c272cad9d74a8fb6c57097a492cf423c30ecc80552034e6debebfa8548a8ab077b1d250bdb623d2e949dceaa5a8bc3402dffb620919e12a6218ee91b4f285f83c51360662652053251e0fd0435860e288e75b2c54b5951352a3eded6fe41baeb15eb86e0348d5b8e17f83fe93149df67dc8210bd5b9a525df5106432d3d7ba30d4bc9ecb1ac79e48b91231e6e80cc5842d7952dd137fade27910abf4e12c1ee866cebf69bca099ae5486566953c03b2317bfc13e4f00a151a7d513879b4b23925b6092e0b47e5a5933cf54e49cb202433ee4430e077bd8fd67140294ae9b1dfb7f0d0f8cde2f9cebed93a171025d52f206da490c85c8e9451fb245a5d8662bcd0810ec9d8e62f45ab6fe4d0134330e0d478738663af87850cdeced224ede49b98ebdac1ff72d51b7bc19794e938134a6be071be031c8b529836b87226fbe47c5c77aa003e543538532fe55eac50a233e6fd1d257f7ef760094e2bf52f1a5007089421c864a6217c242387c40c1f284fa41629a661eb61434b1cbb7613751350f0db295a8af13984d9cca993c36af82ca9f2c56874595b7f286d9727134923bb043d658eb7d17d1fadb20771ee279b1fcbd340dcbac8691e8da0c803e915bf47d4e86eb6556b50cf5bf871f3088099822c13ec6968fcf601c71a54de35734acf0a021727cf48f5a3d9c0f2812d0ee27f09027d3a4ea6a833fd6a261923cc71802050a32c8af50a408b71404575363ce9ad3bb80717184cd402d332d81e1f72e23d385a768e8adf2f1babb4e62410c612d093f59c8fbbccf3b9b30e4fdf4b4c548f07df36b18dd28b54d722a4608a18ad6c25ac51947ddf5bd8146929c80f0fdfc56482fbabd299e893c34a58530ebb4240056060285b0a0113c8af89711873aa3f12c64a9fdd2da22d6d9392822d7ae1b2d0edb3c89474f7c4b370edb57db068b6cfd6feaa7f21cabfd7b6e6ffcaf7ca4d1c9f4edd8b1583c602ad289f3cdd2bf994f1fb3d7d8e5200c4ce7862a54b70fda797d5c8dc53aac533458b043ce1c9107f901e872402311d57b605ca2c45102283f53d58d2ec3902e71755fb047e3e31c30a567b19b8eb746d0983b26d6b8ba3cda34caefb5222bebd2a560d2f533526754187220de87247107668acf6cedda362e6bdad175c42134f726a38280ad363d8916001a8a44182dc90519c7159aa175cb3f9376e1d6f603709d8f44182e09b8de61bf09b8488e146697ac0712625098b2dca6e898e9091435a0194114e2459b9db82ec839e074d08902693226c73d7eafe29bae786a5861504aed975290296507139bedba8b0d2617cb87366ebe4a62226dc4c91eab604532ac2b8614287740f910cce0a84f4d592d65f51c1a5356b1668dcce80afe49dbd92b408d3d33a67db894098b795ca2aaff7890f8aefc0aca453b384d38dd42c915729070388313b90bd74bb2b99dae23c8e174ffda3183b818aab39241f006c2839d9cb3372af054e81f967ce7706005475e29bcb2bd5a9148b71761c8554df88fa7f0c24b29294a462293843c7ca92880629d0c4027053e537856af558ed10035d4f06de1b1fff5c6e16f94b916e7b2ebd6c58f7ebc840aab4eea4eea4d43cc973bba05341378274c7750bf0ae1e14ce607b3b6444c7309bbc525bc7b2137ef0a8920af152ab46d69c91544e7cd8e180199d3eee05b683a0d04f789fc1ce51682a4a6395f5efc4f82ba849c36f1b99c28f671c044ace26abcd16a9a3515a92c1a14afb7b8e3df0d88e2feaecf40c53e49c6a170fa65fe54832452938b9ba97cf90f1db815453ec60f9fec663737485735866ce4250aced6863fadda971e3a31eeec634e118bd71849dd140258e674eaebe7e203b16d9f30c8b046f3b1879a1f7742ae99bfe390faa1ffd0663ae78f97baf3bcdaf4bd88a54d4daebc3542979c4dd31ec24f8b9d99f564121b3c5abd4cabf6ab041ab245d9f03f519f07c3e5a259fd3f318b6d65428816c842bc5c7ef6ecc2c9ca90d326a499ddd11b6e425aec08f0620ff30ec5f203c3f61f59205184dc40533216c6693feff8ccd32d8d41ef7c35d53f14d84da8d9ad2259a2570bc0da1249d16799b222a7ace349f47db3939f88402ce006c6c454d7c97f315e45fcaa1681055d882ee54cbfa2a73dc109850c001931bc4e5413b6bf134861d03009af76fb48cd803bf3c695b25f64892f7af6ce5d0bc85fa1403bdf28f20caa23f4cd7adca9d8a9288c52283159018830a6ac46156c951a8654bf7fb342b045fcf0c90cfe4496a40b266d015f8127da19bd89042aec01c53aad3c99bf678ed027763901196abbea2d1424a74cfaa0c8e63e9f611b11b0bca686171c091f1a4a5b5ef6f347dd4d1480c87f0787f68f30d3d939e58b754c7e3f81fec7836a3a1d03db22c5a42d00c679da30a8bc8d8a1f0139b3156284d0f7f0771f22a29906ac0d9eaae2a9f7dae74610ceff4ecf4afabf3e03885f85e71c178d16f30571a429e8e843034a39ccc5adb97b122f3360d7d98630cfca2a85eac3c03eaae65dfc03d4cbd462df3fd6d455e5a653f62a080bf924659913f3c65e60efa4e4ccb3fdbdf8e0db3af25433a123885f66dbc3b6071778bd8df9256bc98de579a009f7abdd04b2bca951ddb4ff8d2974582c9c478026140d5bc406282a27cd10c06c52037b4fe6cce212b411e0433ec8ad2f02467de0d3f5a741f1fc5a65fe2f0307bbd8481da099e9d03de6bab247d65d2b4660b06900c78052feed491bf205d877005ca19d74b7c56005d8189e8340a8c5f9bcf7d5f5316e6cc74a0abdb1ddf67d8797c88311a9e3034fdbde9c981fcfc39997b4f344e10e3b8cd87d6ecd4d702d57776ab214c6552680a70b1bf6c81de8ddb674b272fd9ce7a1b5ff8ff448dd4e846fde6e4f085ad1dbfe758abffd4e3b7328ad8bb19d52c23775ec80b51c9adf58b21ec2623a65e10a190e838a550659827d4fb3db51b8de575cdd6a3ab22d1fe571f7888cb029d44737f599d16dc5a10adca98c3de6e7bba4c004087a7c4a0e660c3440c64b684c90d0b39158d947186d20a3984f89c1785cb64af83bcd0ffb442ced721b1f7a858d4709a760cc3d53ec02c99d60bcced1306a9ee6cfe67a78b56de883692660ce6180558665df5c40eab19a9263a5b6299e016b83088913e9f44b84af9f7cfcbdbe542bfa851882a3d14bf2abaa708a6d5bda9813ac76e0b9454b5a9a8246d4d7e5a4ebee00159d2689b02c19718bcb06560a30ab92c33417767837737908352ef517d77c43a5a99292434f822b650d13d2c7c8a717eb74eac1db650e5b3ad73afa9280b7f59117c645416baa875b480da941b68d01914f2b88b10c3d75dc6f5035ae56cac4d140ea5ec2577b25bbf6b83cde742dda8fed74a1d232e2a4fc0a6d7344120f879e36c2d6df8165d1995fa1826d1ce5b0c17a31c6197e7751c31f0948e97e8d5d6083b5b2694735d2ad5213608c546a09db79fbaba964559e54f668409ca9a4815b4c9dd8e077c4b24354a6c46da282c7a2f2688c2ea4449580150214c56fbe61bd626ba728be2be0b86cd2f7aff38a1f7fcc9628b83265faed43ab7e5a01fc8f9eb16ced908e464eaa8a87462fd14aa92a98e7dbec3dc48da69c2d697e8f7becfde3fc27cbf505012ea2796da456ca38145dad95a6552f5a1837d0405c0cd123f7aca380374f3b81fe7ad09f62c2eb23c16854d66ad1402d60eef43ac1361a910d5a8ac5c9eba16adce0441f028af35378173e2baa986415391b0d987e101938d9989d3609e036c5a05f159b7462f8b09f84f799e53224ab8d2318d4892846f6e63035dc12ebfb1e1b97838fe672fa90525dd6c843a67c89ca087e8920fa2734bd76d95af07179e607a041cc2ef30e7c1744f415812a4dc27fd73aba4832d26ef5ea7f72ab1a54108f6e89aad4b37eaa7b245ec367e4df00ec0b3b0c6c153671aa8b58ef7f5f637ff6a6b9065774795b660c5b88cebce7bba94aba6043a785a413052b6c7164bf67641b6da627071e6b241df67d48db81a78f8e6d8cfb3d9a617071c4f7765eb68f2ef2a5d5a33ba9c68218cf071e147c4fb465c9f8779cfcbc7475cc9c180f13801d024d1891f51d40d3c8820cebf3c7752e3ae911d427730e5448b437ce2d049e9a2dcdb843e26105767e538b24695e49b8e76b3a76daede6701d2a267383566252262b1fd82128226c46b440b9495a09ac0c4c871b8289d8b75267e213dcd65a6d5ffdfddc51b982b4de2580534c047cca2991b4f529bfd20c9bb928cae32534b02e1b9e2156b686bfe8c730fd83624c35514cbfe6c7e7bdfa189cb80ddcad17f8947038f123b33d61478d10e6dc7ff860e217dfdcf47a6ee16e7c16c720adaeed253f3a75a4c589a7e2a81c6bdb593e8dce03edbd407adb4b20d1c9c2a08529e76870002fd068f2f2be2baa52c2e57a24a67e06b6d71801bf9e2fe091d98c1ed8793cbb1fd332eb1e523fa973b15c26fd3bdecf170993e6904e29a7b845bb2315090aef57e194ce5a4785f3f12f136745078042c5df382f4624c585a26b10ae84809aeb06e9e0b6f36112c51562874de626af1d6b87d806c21a011d2a3e2cd00a3de45ae3da73537dabfb22c6c29f5915da02ddd975913876603017df74c39508ff9db56a791c7e723adbcbe6a0b2f3bdae20d405b6e22029122fe9d56f864cc947a2587305283f2d92010524fddaf3814e9c42a20d3da6f4861db5302a1ba02397f9bf9e9118bfa02693f31c1c8212122d8d2bff30d11e400d980d11e68e53601c88c193ff81c0b0179fce201c4a6caf7a69e66fa2b96579bb3287c3d27de6d9fe1e65b7fb6abedc2e5ddae18fffbb0fea548ef50f49b95311f7ecaf8caf0de4d58e9f47c903521b0fbe60afe3d95c9668399b19cc546112d18bc2c347180ed68cc2744491d0156dd1fb7d0439acd70e99f4b59a75fdf9de85630a279ca583d0f25aa1c5d066abcfea40373e3e88a1a45657930d58bb28efb75c0f9e8f337d523a1dac8322211c0af8da8333ab3d3aee281dfd8640f81b2324f42afd36dc0022da3c95317bf50fb2114a0df2ef69ba7529ab6d5125eab5ba79b550c153e0a74897053a0ad5bf4ae3b5d161deb231db9ba90e1a9e2faa887d538452e3f7de0f27f52ec5f164a72ec8c7afef83ae10d6077398b35d2669678bb2f8b0e5a6393bb52109c2ce3512895c3d573bb6aa9efb497c286aacb8601a4fb5a1fd5991d2d294fee151d287432f50a6270506lmaoa961dc6189fcfc0085fb5df2c8c9fcf26f09876c1ceceffe92e58cd1228620a3b9389f486099ed43de05dc9aae1ab8eefb59a16087dd835ad6a7dca4de72083a5482bd99084da23f84747ee01d649a363737f055f7d6fa41b5948e2272cf7b7fbea2aedde9988e0c747656fe66015ddc6095fce5568cb7bd4382910b5d2161f7c29f999eece72ca36cec92929f23e7f9f1a433617a6fcfef5d13d035b91acf1d44ea3fe21a78526f3a897b8b263641f2571c2f4df73e6f0fc99ddcbca63070543950306a5bbc692e220946400f3c584698334bd8dae98d2da89c2ec4e77d4e605b3afa89102774525f7af456ad4cc5b6a526471ce068e43972d73bec934c185e144a958f687a0ff1f391d7e22acb9c056552cefbda0316785f5ce4983a0ee6a02fca4a0381c445307256d77871531a8b382e36e667dfe594c2bd62001838869f98216c027fcf1318801e715422b9134f57027b8bc80aad0623c0d2fffacffb7c5016153752ba4b9162ee6d4f4e38ecb4a8cc3683072411f4a4c63924c7a0e0c757455c77faece97a817c9ba0b218257f2f0666c73c97a55d12a7224343a846b858349394ff1d3e598d490422280ced85df5ca29b499aea068ea18ca0a7a51fbf4aa000efdc61e3f3f796f456be72ddcf7ca61ed2f55a7e885e26e69d872281c5b548f84caf4beca52f6886b60b1bc862b4768b149a9f16256d5ce3f782ada00e84e0dd83bc81226d96bece304b913ab596b681580d14048d5732535a783ffa961e0c7cb0047e16dc9e016fc83efb03a711697716e64d52c18266405f26b740a3894f4de243f6947d1b656249df122db3977f289a00fe75bbd47e7abf00c935e3a9b5058b6bb91311f7c496e4bf513c1b79846b36223f04392f0dc3067af6305af014988c9cc3ea3de05e966669156b5a8b6fee47aba25a935ff427fb6fd1b18536360e20f0a5672e2bdea627746bba3b73f58473fbc85a7cc05d8a4e3f5c73a393ea33112665c3290365a769cf9e8f520c3e4f99312e823c7d78cef660450bbee7de74c5520b96f1fb53d26edc540fcb77415928da0ff6cc89140d154013c941eb72e7a79e8348570010332e3db2dedf6b3610e24a84fe019d18a4fa01e1f94877df5dbd8df9a6ab5506269078e457fa0dc7c8202cd1e7f25a6e8242f151fdfc3a05aeae1416e29753d5763e6f7ec7429e69bd6b18350f2e0f0b36848cf47496fa4c14dd7c1bc02c6ef69c5ab1c22f09a5483180587318441f90173499301009993492f7cf2ece7c9020187e5b0688e2cb7c5589e3d5246d2c21f44bddf7825c8a92337bcffd8ba80df7c4a814b69789c28ac3ff1f1071c55273c70e89d1845d00504786371c18e25149b0e681d1b0cce63bdde06431746ef7a44106c906d54765ac728b07967b3c369cebfc1883c057e87ac3491ada4aea4304c9336e9a4bde88e11da50f4e842abbd129567f401d45bfe024c98161df67b6a07bb5082587ce04e2d5d5f10fb797cd178f74540b5a9fad7955b4086223039b756c38b2b6debff09048e06451461fd2ac4410c525706330059e2f2a3a3bbcab66ee79ea37ae29d292cac17b14b5b067ca7bb9c46fda9d19205a66d2d2600dda476481a04c8c1127dd9d090c6075dece3b3725f4a6ac99516e70dc2172515595142c32b81cacd74d49bf3deac8b670fb4d7feb09ecbf2c9517387eb72a9af1df468545be5d6f90ead642a3ae6ace032c497b12dcc8cbbeac40f143996a9b6d9d908bbf0f7f454591c42509053c233cebd2196e806d078c7246813d525230e5e354f73a89c7053171cfaa3e5aac9437ce0dee557b0644c70404e4f96672d7af3d1313ce08c938a9e0a5ed6cda137989c2c4fe01b96d68e897652ecb3c66be906b8941eba1c556685cfb544244343845df24e091c2177892f144701316a28944c9011e3c2725fac9ce69c6ec56f767d27414d025f2e2870030a51fd86a95b12ec615df8d2a2ef822b0a06c98d25032eb807ddaeff5d723bff2080e69e357cc3f6c7b9e03222c228ba9393d4ed5df38f6673a37d0e82c2fc453666c58c5b71ca91f267e781fc6b425aa5e2ef9d5a6b47dabc84059b92a4949cd86bde32e8c66e542e978ff151ba2c8370ffdf4d835ebd074c22e18ad799b1a5c451f5e823ff948252ff4136f69fee84ce002d3f399b74668a1188aba596899b921febc4efe2ddf996e62df302359c6917774ee61d0467fcd1551bafc5074ba25ad968a4910228b7caf1f049fefbb3ae41b8d4e70fd36dc95db2c647aa03418c2b9a1d899af20a7238e968aa8d0831c04e0fc46fa9985133c16e6477de905345b301a875dbc4d49419af6fb5e2e01d0aeeca543a501f39d0f0e2a3afa0104594cfd90077cc38ee1df60871264c11dcc3128d7f4196bdea3b75c25f44ddd928a2db2844ed7f4eb902bbcf3c435d13310ab2729fd16d4c5a6ff01b689f283c0c3411e6340d3d489a5b32faa748cc006f7333a2d4aa115d05fee7ceedc326af41a727443347a2c5584d06de8abf8b8be7963f2abbe42db4816eacbcad72755a29977ae41fede452600b535f266174aa2d0feddec544a8b28ca631c4c982aaa22d4daf95f14b852cce5c5d06f7b252afb8944e8ea02739498f80dafab9395b9b82102322d0e5e2366b5646b0be9cc683e2a07a8aecdfed34abd9cbe46bbff9d67c9b6f0d8724ff25bbd180d29faa1f7a5bc839167bb7dc9d31e845cf0e5dcc5f5059119fad04d3f0e732e037cfd624fc45cdac0b5d07db5fcf57a1ed69f008eb1bae402c1c2a7dc78d7ec183c82a625b1854a030319271fb2092eeac12e28858058df48f30b1e619be7eebc7ece30c94105c7d9f0de33e52e10fe4e4a48e0931e8bb1331409a1f80a16e7e4ff07ab5e9cd49965548af831fac2eb077079c75bf18f052eaeaa1b499a8a79419f5dbae5f241332df3a6c115649e94412ad3849a8fec30b78dd917b0a3a926f742ade1091a472bdde2d5b9ddd9df2e986ec3e1863357a6d3a291ff65fa531b856ca9618af280c5fe4c6f7c3d07c8713d6c785210bacda427eb2ccefda59e4cdfaf7835aa615c18a896d99beac05ff87c4b9f0577b5d678af78a91c17864d69bb51c12c8fcc963639f14d767ce19a57344d08cf13a2908bbca24039b76f54784dc5f4b6b3ca53ca9b40073c5a3cfc966ed37158ac80c1471e8b59db4c6c0ebf61777bd77e277fec6dd835694f9bf8c955fd3cfc3d2632c709cd6c9701b7e473f808c542d74bb2c6cf3efdacf96fe0549f112e567f8111b1562a179594c24cc6071753c6c2133f09a578384870d0fd42ce02a2b1085560dfee4c4e3668743f9d358c4080ac85557abd30df8f2c39d02a5447063b20d53a545057f8ad91c7271de33876de0d78c892371e5dd407d865337af0f49f48c63c209356e1d094477fb3d4c67a5fee717f62cb32e313f87f7c1aa469bff875fa701db84ef4f0295e340b8b42c0c57d2e62c8d00d6ca316c3b96129ebcccbbe30459afd3419bbf2eed3d43fd4e796957aa282ad03348d755d269a4f3e7a6760bc293a0a2bb0f4a21597b90a3f532a1151ef88df91320439e01e0595996d28fea9da3f8dc44c931cc30f8fba2479aa5dcd3bb3e9dde89abf71a3ef30cce9804d927ec00381ce9f209631c93154ba44dcf439ec18fc7c9be18b8ab5d72e1b05c49e844087b91d8f6f6d2d8d1e4a6125f8a4c904faf21d67048ee25bf358c0102415d57dc5f26dd225e0f108f26b800ef52c641d083dd0ee0a69b0e52aeba619d419d0f2df9f25e155c6d10f77b5eb119dbe4ed52d64c6a0e0043a88ac4299c8d264eed9476a9052b78fe4091f82bce6e404c8e70412441b0041fe986d4a2043e5d7f5fd2036cb16bee530f7d45863b82ad1e91f6bc63cb2bccce08969ea2b67a5d5238132423b6b254a4fc5d23a6f713cff415355c29381f3aff9196aa93d0bb07c82d1658a44ff0145965fb8b4e8b83458443a9efca15c1a0fce3a77cf2cfe14e169c68e4963e829dd8c045f4e4750e59171eef0804f9f85d0bbc50e971b61c410af74a31c9600754cdcdccb6d97ace8b28ab4e763d033ff0fb2951308055b1b0502b46bcf8a57805a750182da196c811f758a90acf1da0e9b7e2b98c5964577cd0f4ac74a4425578e55ebfae5eeb78b40a2cc5334fce978291ac05c7e582b61bc870e2e7e23201ce9b29e995933bfe08c36cbb114b096d2609989bd3637c651372dd89091a8cac3954a3ffeb702a6527e834fee55fcc1eddce6569f974bff96ece3f37af41d87a72a7baec33288cd0379de9e95c6074c9a6c3f6ce9df7fc5b2e95d2c5da75040532e0f3f09c6bf7f37119f4c9336f044fad26f4a451dd08eef535182aa3f6e43798cfece8c3c720288c06893ee2a5a17bbc6f417c3f110e32556cd4ec3e5dcaafd9dda267e0042746d3a4918ea171b0410149ea8648e9b7f4585bebf4e351021eaad7fec3412d361dfeeb00bc65c99e4e96ac6f0bc7379971954a9d0b42102928faa3bf09f0e5563a432af870f7b27e1baaa0230d77fef75cf38dd18b99126bde8f8b185af7202c3faeb19d3aa32795c7687c19c1cf7673ec58bedfe99d3ecb899fc240ba726279a9c322df4956356da99537cdaf10caa59cbb55b8e2dd109fc08e21667f59a13a7a97eabcf200d4b04b1e9c7dc25aaebe27bb498435e6b787613c8707ae46dbfef4bcb2e0b1e59eafb7bd4715365b5250958f4258e4936be6c74b0fe29bacce1b79605f61eee25fffad4eb324a3ee545c63b9a665004cf37d223b3ecb0f90ad50d228f6b988d5db25c2dad826927505428edeb538b5bbb55412130603eebd6cf50ee75c81195f228990d1410843b18e689b3ad945ff520c622accfede8e34f52740ad28b34e421675014379c587d9ea30b63af9783623159fd064718dbb1ef4d18011edabc5326a9119935268b7ca2ebcff0300ddd35b965a401b83a2fa54936070ed213c7807d3f8a415f11792cafe5a926f8e715d84a32d9b3ba440c27f63a19903d48593eaa00face71f54fdf4afcffe53844e0744195bab65fbaf90f0c4e76d3e9501b60384ad1cee941127a90ce1316dc13cd5094ed7f8c61d6733979440dbf9969c3bb16460d95ae2e2480c57303f2a1880155b96a91a142546058333bc8e982b43f653e1b367bfe729481de649a6e502b6d9965e864ed6804a0b12bcf37247e4bf3af15c0c01a064d06580852b5085b5d1556505f490caf1e380d5a8e30b075f0d5f722a8704e33452761b5c48e4958d13ed8b8ac7a7171e32f95e83633faf8f240b66af87c559435a65494c6350e3f3cb7d2ff14e0f824d6518ae5abc80ac387c171913684c341e6e304c38d7d5e1cc2429de2c5d6450fad42dc02524f43993014e19bedd4c7e652976fc748d32c76b660b483b18d2a6e0a2f64f2555a88dcc27f6b0dbb55e7dba0cf272dafe6e7b53b8fdcfa62308819aee3f755373b157f9147edd8493624c2714da47b687abb4d409388fd239d5e8b49e379f92edad08c50336c436fc8650d0835918ac8c9ae62886ce00bf2cce1b631e44962bc65d37596e408d91d07c2d38fe1862346efe6e4f1cd9240fc5dc8ba02991efd9ba6cb7497e7f09a409bdae632520cefa133b5dc1b0bc57af7700383ea6ce82086a95605000395d9a50de956dc9c11fb678349f51f093926c5918de7de409c2fec9dd616649bf1f15186067148b856c8c85d05faf5c841cb19c5ec2b3c3709fa285479b04b8cad074c421e9e6145f48f8acf085d6a74c8f0a742bd2ee1e69b6172297aa254a00f2553537953bef428cf7ac85ea3282dd0b4d845042320741a1bc2441e6a1c7c4ea214529c6cfe6b4d07e59dc55f0e72b34279f4708244cd3aff06c582447f071706d746f251b959a4b4115e3e93b2bfae523ae6bd5bc48c4262587c55346347cc7e03e79890b87da760bb06c8216a81b6613530a7f43fd42f44a7d79af9b34d93aeaf104132004250f91d14c85545bc6738762751a6df5d830804bf68bea5f5b8802d06077bd71a2647f5cbeaf0e6bb1d76d22f7e07de7a9a8a7d7504903f956703341f30979d0748f66fb871f39e65404f6ed8bea4a5bf760eb3562dbf4bd4e5671e0a568730b3d696a4ba12aa0a0263ad37284749fefc8c776f7ead8b38809d76dc78fa10193920f2cd10146d714f59e5d673760c8d04d6041de28de719a4da4ffab4c7d9d4a778c0570a717256ef6d41ed9fb6c30397975ff8503a47d7ad52e682dcf9c55d9a41960694c80828131d6a067fd2b94797039ea220321cfa944731aa606e6044ae7b5afc5c6dbe934b658107cab019c91cc1eda91f0f9307d22f38e4e3c6b9aa4a2b4d4be2e3db855c3d5925b5bbd1d9cb8038074d3e84a2e4a58cce1370cb07f667ab8e4d2c8f96a0d1b470821af922fc9accf5c41dd38abc78ace183a298f47e8691ebdad277016ef2f9fc663ec3a0e67be462983eee38a7dbd75ee87d122e1f3a5e20f601ddaaf4dc8835bbf29326d9622c026e582aeb4f87a39ec5572c2672e8847c07023b49cf3ca18d10226f287f53777a6380d01064d7bf863b65f3a35af551882ff4ea690846c3f3649ade8ffb2f281ccf13478c2d4e052f8e654bd12bd3b0c37f70b88a78756879fd2bbe3d2c9015c97358ee1a88fd0b76dab9dce728ccf4b0b3ec454c055ff45e355b2afd36de5dfc2fcf19aa18019c72c4a08b7eb6d9aa363b4ef2f7e2defda3d418c4a88eb837e631ff763829f466401c486ade8d9455bc29ffb0dc88ca913c53a84d5fb0ddb56a48303da97f96fba04cecd8f1c074041e50df83a121c1307689236b9df91623f96f584bd60ae15ea0dbf403b5a667f27d6f6668fd59062ba387abb813e17a32e6c9f8e1925b5074d0c8fb00c660b0950b755c71384cd82f9eb16366cd306fea5efae6dd4dc856c4f53b4d004980efd9da13b99ef318ecd3f208d9998c9615ff762aa6a1d91cab95d031939270267ee3399794f04d99dd9db2235e3f89941279068daa40c36537d0633967fac672d1b1a5a5a95672d0dbc35538dcc0afa1123b5e560b6f32b652c3e187e3a6d10e6bc52129ef5631c0f940c87f59f28f2a879a3c7a945be0420ac7c088d7bf1d749d6653504cb043f21079fa274a48d5cbd1945f8d85c13596be120119cd4c01bd0889cc8746c5646c0cc3afe585bd1696945e8e0c79436c40f4492f7fff3446eae76f3b21c0c1390b6ece746dec71b7120e53fc1e1c99d74ec84bd9e0cc5ee59dbf99642acd7f85e716c81e9e760a0b4fb5c9edd0625317b00fc131eff2db4a5135e330568db0e122371183c2119b8f6b05693b53baf4a8767ceae85893c90b664359d233af11a560047d08431808a99651bd3de26d6a148f218b31ac15ab1a41b23aad9a469ef05785aa6861df8928470ee5445741ccd589aa18ce3f515b4bc4c5f376789d76d2274c663cd76fe3dc8d59f0c8ffc66168545df72a4a5ebfd7285789a789d2635435bea96b27ffa1a988426af1e77edb221d6ddb336b7caf691ac66ca578049c7a87e9e166c2ac17fa6d110403ff55d91037779fd1c41886398939ba730f0b3b94cd7f68762fedf441c9e10f22a8c93a48a20072b076fcaa9f00149557eec4b382aa1efb59c126fa1856ad63143b846cd8e3c6ad5c75f7388f2f9efd97a7b70c06c0d965b9131e5a008b224b02ef120cb362bbe11cd3ed6619a260e5f136ae8b15bf168bfda7a2e733bc6c4866d5e48f33814f1188d4bbc6f2918b57bd714a65d67b66c19aea92eddffcc53c5b71b41f570ee6ea39cb02c5444162e97220a82047fb8c5e2e0d1192acbc771c9472d2c02be5f71fab9dbffd84d417c592678d7de2ae9eb2903dfa230547512516235e6b2749a1eb7205897c14161568defd99823849abc8a35207d6333cebaec7fbf04c83887f670534034a9a112855d53b19984cbeba8db505bd7e7fadc4b2fcc00cddc30fc8ea348bbcc8c54b632a84bbed801d7b3c0d8b8b56c94ccab4a15c4863b398a39bf7f3231da816de9ca2442dd5f610421c5ae1f678aecb71bee73c3374bbe0d98826207e22223fb3bc24965a9e1247900b645a36b3d39b2d3e48b624a164d8959b3c79b00751c3890871d3d8f3de55c5f971e4353ffa5acf3b752cae2c12ae96c997630f28a0746f0ace81335f465533dae1ea51ba9d132235bd8f1066394a365b1948c1f6a1cdaec1d9a6c14e8776d391bd3dcf27ff87a47182f6504d1ecfe566faddda672abdb2991e5b755c591c28edb3db54c59bab8e805d2b15d28b39b8602445c4a0ebbd1b6adf18e5742d4f5953792634e860360cf9936199f989f1e4ae65e75cd8443cd4973eff78c418b146e4155c33d977f8ca4e30b2e52cc8c8de3884545752ad2a4c36ea69ec07d638a664acc69fc4c9ce1fd30975587ead31ccd7c4ba791fa57e3610995f437332b0c5c48580a582986c1c9891cdeccf876655ea965a51e35ff045d685c23e365876df4c58e88882d581effac3b9effadf9ce2deeeebd18fb6a16e691a22c869c5da3cc0e2979f301a7eb6305cee3228300e673fc47cf2726e739b617e49a11f50e85bdb68df2fc876410a7cf661370ba63ab11ae13299cc27f5530753820c*$/pkzip2$:dummy.pdf:blueprints.zip::/home/ben/Desktop/HTB/Academy/Cracking with Hashcat/blueprints.zip

```

We can see from that hash that this is mode `17200 - PKZIP (Compressed)`. To run this through `Hashcat`, we need the entire hash starting from `$pkzip2$1` and ending with `/pkzip2$`. Armed with the hash, let's run it with `Hashcat` using a straight dictionary attack.

#### Hashcat - Cracking ZIP Files

```shell
hashcat -a 0 -m 17200 pdf_hash_to_crack /opt/useful/seclists/Passwords/Leaked-Databases/rockyou.txt

hashcat (v6.1.1) starting...
<SNIP>

$pkzip2$1*2 <FULL HASH SNIPPED> k*$/pkzip2$:zippyzippy

Session..........: hashcat
Status...........: Cracked
Hash.Name........: PKZIP (Compressed)
Hash.Target......: $pkzip2$1*2*2*0*3024*33d0*7eb29321*0*43*8*3024*7eb2...kzip2$
Time.Started.....: Fri Aug 28 22:34:46 2020, (1 sec)
Time.Estimated...: Fri Aug 28 22:34:47 2020, (0 secs)
Guess.Base.......: File (/opt/useful/seclists/Passwords/Leaked-Databases/rockyou.txt)
Guess.Queue......: 1/1 (100.00%)
Speed.#1.........:  3665.1 kH/s (0.32ms) @ Accel:1024 Loops:1 Thr:1 Vec:8
Recovered........: 1/1 (100.00%) Digests
Progress.........: 2500608/14344385 (17.43%)
Rejected.........: 0/2500608 (0.00%)
Restore.Point....: 2494464/14344385 (17.39%)
Restore.Sub.#1...: Salt:0 Amplifier:0-1 Iteration:0-1
Candidates.#1....: zj4usm0z -> zietz5632

Started: Fri Aug 28 22:34:24 2020
Stopped: Fri Aug 28 22:34:48 2020

```

We can now use this password to extract the contents from the zip file.

* * *

## Example 3 - Cracking Password Protected KeePass Files

It is not uncommon to find KeePass files during an assessment, perhaps on a sysadmin's workstation or on an accessible file share. These are often a treasure trove of credentials because systems administrators, network administrators, help desk, etc. may store various passwords in a shared KeePass database. Gaining access may provide local administrator passwords to Windows machines, passwords to infrastructure such as ESXi and vCenter, access to network devices, and more.

We can extract these hashes using the compiled version of the [keepass2john](https://github.com/magnumripper/JohnTheRipper/blob/bleeding-jumbo/src/keepass2john.c) tool or using the Python port done by [HarmJ0y](https://gist.github.com/HarmJ0y), [keepass2john.py](https://gist.githubusercontent.com/HarmJ0y/116fa1b559372804877e604d7d367bbc/raw/c0c6f45ad89310e61ec0363a69913e966fe17633/keepass2john.py). `Hashcat` supports a variety of compressed file formats such as:

`Hashcat` supports the following hash names for KeePass databases, all designated by the same hash mode:

| **Mode** | **Target** |
| --- | --- |
| `13400` | KeePass 1 AES / without keyfile |
| `13400` | KeePass 2 AES / without keyfile |
| `13400` | KeePass 1 Twofish / with keyfile |
| `13400` | Keepass 2 AES / with keyfile |

We can use `keepass2john.py` to extract the hash:

#### Extract Hash

```shell
python keepass2john.py Master.kdbx

Master:$keepass$*2*60000*222*d14132325949a3b4efacdb2e729ec54403308c85654fe4ababccfb8ddc185d09*5c09bed9c98f8ee08aa7a71fe735b30849ec87e6cb7f1caa96d606ce9f077f7e*bd372d79d8aceea9689ad49428b8efde*28d21caedf25617db0833bd721a42c963e874e0b9fbe7fe1187a4a8ecb3b1d19*a539abd3cfd7ee5982fa28c44dd226ce05a1102d04a5f590eabf5138cd2a6403

```

From the output, we can see that this is indeed a KeePass hash, and the type is `KeePass 2 AES / without keyfile`. With the hash in hand, we can attack it with a `Hashcat` dictionary attack. This hash uses the [AES](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard_process) cipher, which is more difficult to crack and runs slower through `Hashcat` than other hashes such as `MD5` or `SHA1`. Therefore a very complex password may be difficult to crack, but a password contained within a wordlist such as `rockyou.txt` could take around 8 hours to crack on a single CPU but would crack exponentially faster on a GPU cracking rig.

#### Hashcat - Cracking KeePass Files

```shell
hashcat -a 0 -m 13400 keepass_hash /opt/useful/seclists/Passwords/Leaked-Databases/rockyou.txt

hashcat (v6.1.1) starting...
<SNIP>

$keepass$*2*60000*222*d14132325949a3b4efacdb2e729ec54403308c85654fe4ababccfb8ddc185d09*5c09bed9c98f8ee08aa7a71fe735b30849ec87e6cb7f1caa96d606ce9f077f7e*bd372d79d8aceea9689ad49428b8efde*28d21caedf25617db0833bd721a42c963e874e0b9fbe7fe1187a4a8ecb3b1d19*a539abd3cfd7ee5982fa28c44dd226ce05a1102d04a5f590eabf5138cd2a6403:1qazzaq1

Session..........: hashcat
Status...........: Cracked
Hash.Name........: KeePass 1 (AES/Twofish) and KeePass 2 (AES)
Hash.Target......: $keepass$*2*60000*222*d14132325949a3b4efacdb2e729ec...2a6403
Time.Started.....: Fri Aug 28 22:37:08 2020, (2 mins, 12 secs)
Time.Estimated...: Fri Aug 28 22:39:20 2020, (0 secs)
Guess.Base.......: File (/opt/useful/seclists/Passwords/Leaked-Databases/rockyou.txt)
Guess.Queue......: 1/1 (100.00%)
Speed.#1.........:      430 H/s (3.75ms) @ Accel:256 Loops:64 Thr:1 Vec:8
Recovered........: 1/1 (100.00%) Digests
Progress.........: 56832/14344385 (0.40%)
Rejected.........: 0/56832 (0.00%)
Restore.Point....: 55296/14344385 (0.39%)
Restore.Sub.#1...: Salt:0 Amplifier:0-1 Iteration:59968-60000
Candidates.#1....: gonoles -> jacoblee

```

The resulting password `1qazzaq1` is an example of a [keyboard walk](https://github.com/hashcat/kwprocessor) password.

* * *

## Example 4 - Cracking Protected PDF Files

The last example in this section focuses on password-protected PDF documents. As with other file types, we often encounter password-protected PDFs on workstations, file shares, or even inside a user's email inbox should we gain access (and perusing users' email for sensitive information is in-scope for your engagement).

We can extract the hash of the passphrase using [pdf2john.py](https://raw.githubusercontent.com/truongkma/ctf-tools/master/John/run/pdf2john.py). The following command will extract the hash into a format that `Hashcat` can use.

#### Extract Hash

```shell
python pdf2john.py inventory.pdf | awk -F":" '{ print $2}'

$pdf$4*4*128*-1028*1*16*f7d77b3d22b9f92829d49ff5d78b8f28*32*d33f35f776215527d65155f79d9ed79800000000000000000000000000000000*32*6cfb859c107acaae8c0ca9ceec56fd91ff75fe7b1cddb03f629ca3583f59e52f

```

`Hashcat` supports a variety of compressed file formats such as:

| **Mode** | **Target** |
| --- | --- |
| `10400` | PDF 1.1 - 1.3 (Acrobat 2 - 4) |
| `10410` | PDF 1.1 - 1.3 (Acrobat 2 - 4), collider #1 |
| `10420` | PDF 1.1 - 1.3 (Acrobat 2 - 4), collider #2 |
| `10500` | PDF 1.4 - 1.6 (Acrobat 5 - 8) |
| `10600` | PDF 1.7 Level 3 (Acrobat 9) |
| `10700` | PDF 1.7 Level 8 (Acrobat 10 - 11) |

We can crack the hash with mode `10500`.

#### Hashcat - Cracking PDF Files

```shell
hashcat -a 0 -m 10500 pdf_hash /opt/useful/seclists/Passwords/Leaked-Databases/rockyou.txt

hashcat (v6.1.1) starting...
<SNIP>

$pdf$4*4*128*-1028*1*16*f7d77b3d22b9f92829d49ff5d78b8f28*32*d33f35f776215527d65155f79d9ed79800000000000000000000000000000000*32*6cfb859c107acaae8c0ca9ceec56fd91ff75fe7b1cddb03f629ca3583f59e52f:puppydog1

Session..........: hashcat
Status...........: Cracked
Hash.Name........: PDF 1.4 - 1.6 (Acrobat 5 - 8)
Hash.Target......: $pdf$4*4*128*-1028*1*16*f7d77b3d22b9f92829d49ff5d78...59e52f
Time.Started.....: Fri Aug 28 22:41:07 2020, (0 secs)
Time.Estimated...: Fri Aug 28 22:41:07 2020, (0 secs)
Guess.Base.......: File (/opt/useful/seclists/Passwords/Leaked-Databases/rockyou.txt)
Guess.Queue......: 1/1 (100.00%)
Speed.#1.........:   244.2 kH/s (20.86ms) @ Accel:128 Loops:8 Thr:64 Vec:8
Recovered........: 1/1 (100.00%) Digests
Progress.........: 49153/14344385 (0.34%)
Rejected.........: 1/49153 (0.00%)
Restore.Point....: 0/14344385 (0.00%)
Restore.Sub.#1...: Salt:0 Amplifier:0-1 Iteration:64-70
Candidates.#1....: 123456 -> truckin

```

* * *

## Wrap Up

As we have seen in this section, `Hashcat` has many additional uses outside of just cracking Windows, Unix/Linux, and Active Directory related password hashes. As a penetration tester or red teamer, it is important to be well-rounded and versed in a multitude of tactics necessary to achieve our assessments' goals. Sometimes an elaborate exploit or attack is not possible or even necessary, but the contents of a (weakly) password-protected document laying exposed on a file share could give us the keys to the kingdom.


# Cracking Wireless (WPA/WPA2) Handshakes with Hashcat

* * *

Another example is a wireless security assessment. Clients often ask for wireless assessments as part of an Internal Penetration Test engagement. While wireless is not always the most exciting, it can get interesting if you can capture a WPA/WPA2 handshake. Wireless networks are often not properly segmented from a company's corporate network, and successful authentication to the wireless network may grant full access to the internal corporate network.

`Hashcat` can be used to successfully crack both the MIC (4-way handshake) and PMKID (1st packet/handshake).

* * *

## Cracking MIC

When a client connecting to the wireless network and the wireless access point (AP) communicate, they must ensure that they both have/know the wireless network key but are not transmitting the key across the network. The key is encrypted and verified by the AP.

To perform this type of offline cracking attack, we need to capture a valid 4-way handshake by sending de-authentication frames to force a client (user) to disconnect from an AP. When the client reauthenticates (usually automatically), the attacker can attempt to sniff out the WPA 4-way handshake without their knowledge. This handshake is a collection of keys exchanged during the authentication process between the client and the associated AP. Note: wireless attacks are out of scope for this module but will be covered in other modules.

These keys are used to generate a common key called the Message Integrity Check (MIC) used by an AP to verify that each packet has not been compromised and received in its original state.

The 4-way handshake is illustrated in the following diagram:

![Diagram showing 802.1X communication between supplicant and authenticator, including message exchanges and key derivation.](https://academy.hackthebox.com/storage/modules/20/NEW_4-way-handshake.png)

Once we have successfully captured a 4-way handshake with a tool such as [airodump-ng](https://www.aircrack-ng.org/doku.php?id=airodump-ng), we need to convert it to a format that can be supplied to `Hashcat` for cracking. The format required is `hccapx`, and `Hashcat` hosts an online service to convert to this format (not recommended for actual client data but fine for lab/practice exercises): [cap2hashcat online](https://hashcat.net/cap2hashcat). To perform the conversion offline, we need the `hashcat-utils` repo from GitHub.

We can clone the repo and compile the tool as follows:

#### Hashcat-Utils - Installation

```shell
git clone https://github.com/hashcat/hashcat-utils.git
cd hashcat-utils/src
make

```

Once the tool is compiled, we can run it and see the usage options:

#### Cap2hccapx - Syntax

```shell
./cap2hccapx.bin

usage: ./cap2hccapx.bin input.cap output.hccapx [filter by essid] [additional network essid:bssid]

```

Next, we need to supply a packet capture (.cap) file to the tool to convert to the .hccapx format to supply to `Hashcat`.

#### Cap2hccapx - Convert To Crackable File

```shell
./cap2hccapx.bin corp_capture1-01.cap mic_to_crack.hccapx

Networks detected: 1

[*] BSSID=cc:40:d0:a4:d0:96 ESSID=CORP-WIFI (Length: 9)
 --> STA=48:e2:44:a7:c4:fb, Message Pair=0, Replay Counter=1
 --> STA=48:e2:44:a7:c4:fb, Message Pair=2, Replay Counter=1
 --> STA=48:e2:44:a7:c4:fb, Message Pair=0, Replay Counter=1
 --> STA=48:e2:44:a7:c4:fb, Message Pair=2, Replay Counter=1
 --> STA=48:e2:44:a7:c4:fb, Message Pair=0, Replay Counter=1
 --> STA=48:e2:44:a7:c4:fb, Message Pair=2, Replay Counter=1
 --> STA=48:e2:44:a7:c4:fb, Message Pair=0, Replay Counter=1
 --> STA=48:e2:44:a7:c4:fb, Message Pair=2, Replay Counter=1

Written 8 WPA Handshakes to: /home/mrb3n/Desktop/mic_to_crack.hccapx

```

With this file, we can then move on to cracking using one or more of the techniques discussed earlier in this module. For this example, we will perform a straight dictionary attack to crack the WPA handshake. To attempt to crack this hash, we will use mode `22000`, as the previous mode `2500` has been deprecated. Our command for cracking this hash will look like `hashcat -a 0 -m 22000 mic_to_crack.hccapx /opt/useful/seclists/Passwords/Leaked-Databases/rockyou.txt`.

Let's go ahead and try to recover the key!

#### Hashcat - Cracking WPA Handshakes

```shell
hashcat -a 0 -m 22000 mic_to_crack.hccapx /opt/useful/seclists/Passwords/Leaked-Databases/rockyou.txt

hashcat (v6.1.1) starting...

<SNIP>

18cbc1c03cd674c75bb81aee4a75a086:cc40d0a4d096:48e244a7c4fb:CORP-WIFI:rockyou1
62b1bb7345e110abaaf8304c096239b0:cc40d0a4d096:48e244a7c4fb:CORP-WIFI:rockyou1
be2430ce7a4ed2ddb36fc94373197add:cc40d0a4d096:48e244a7c4fb:CORP-WIFI:rockyou1
15c472b7641042af642fc9ec0b65b500:cc40d0a4d096:48e244a7c4fb:CORP-WIFI:rockyou1

Session..........: hashcat
Status...........: Cracked
Hash.Name........: WPA-PBKDF2-PMKID+EAPOL
Hash.Target......: mic_to_crack.hccapx
Time.Started.....: Wed Mar  9 11:20:36 2022 (0 secs)
Time.Estimated...: Wed Mar  9 11:20:36 2022 (0 secs)
Guess.Base.......: File (/usr/share/wordlists/rockyou.txt)
Guess.Queue......: 1/1 (100.00%)
Speed.#1.........:    10052 H/s (8.25ms) @ Accel:128 Loops:512 Thr:1 Vec:8
Recovered........: 4/4 (100.00%) Digests
Progress.........: 2888/14344385 (0.02%)
Rejected.........: 2120/2888 (73.41%)
Restore.Point....: 0/14344385 (0.00%)
Restore.Sub.#1...: Salt:0 Amplifier:0-1 Iteration:3-7
Candidates.#1....: 123456789 -> celtic07

Started: Wed Mar  9 11:20:26 2022
Stopped: Wed Mar  9 11:20:38 2022

```

Armed with this key, we can now attempt to authenticate to the wireless network and attempt to gain access to the internal corporate network.

* * *

## Cracking PMKID

This attack can be performed against wireless networks that use WPA/WPA2-PSK (pre-shared key) and allows us to obtain the PSK being used by the targeted wireless network by attacking the AP directly. The attack does not require deauthentication (deauth) of any users from the target AP. The PMK is the same as in the MIC (4-way handshake) attack but can generally be obtained faster and without interrupting any users.

The Pairwise Master Key Identifier (PMKID) is the AP's unique identifier to keep track of the Pairwise Master Key (PMK) used by the client. The PMKID is located in the 1st packet of the 4-way handshake and can be easier to obtain since it does not require capturing the entire 4-way handshake. PMKID is calculated with HMAC-SHA1 with the PMK (Wireless network password) used as a key, the string "PMK Name," MAC address of the access point, and the MAC address of the station. Below is a visual representation of the PMKID calculation:

![Diagram showing PMKID derivation using PMK, MAC addresses of access point and station, and HMAC-SHA1-128.](https://academy.hackthebox.com/storage/modules/20/NEW_PMKID_calc.png)

To perform PMKID cracking, we need to obtain the pmkid hash. The first step is extracting it from the capture (.cap) file using a tool such as `hcxpcapngtool` from `hcxtools`. We can install `hcxtools` on Parrot using apt: `sudo apt install hcxtools`.

Note: In the past, this technique was able to be performed with `hcxpcaptool`, which has since been [replaced by](https://github.com/ZerBea/hcxtools/issues/166) `hcxpcapngtool` which we can compile and install directly from the [hcxtools GitHub repo](https://github.com/ZerBea/hcxtools), or via apt ( `sudo apt install hcxtools`).

This can be performed with the deprecated tool hcxpcaptool. However, this tool is no longer present on the Pwnbox so compiling it, installing, and running it is an exercise left up to the reader but will be shown at the end of this section for completeness.

As mentioned above, we can install `hxctools`, which includes `hcxpcapngtool`, via `apt`. Alternatively, we can clone the `hcxtools` repository to our own VM, compile and install it.

#### Hcxtools - Installation

```shell
git clone https://github.com/ZerBea/hcxtools.git
cd hcxtools
make && make install

```

Once we've successfully installed `hcxtools` (if not already present on our attack machine), we can issue the command `hcxpcapngtool -h` to check out the options available with the tool.

#### Hcxpcapngtool - Help

```shell
hcxpcapngtool -h
hcxpcapngtool 6.3.5-44-g6be8d76 (C) 2025 ZeroBeat
convert pcapng, pcap and cap files to hash formats that hashcat and JtR use
usage:
hcxpcapngtool <options>
hcxpcapngtool <options> input.pcapng
hcxpcapngtool <options> *.pcapng
hcxpcapngtool <options> *.pcap
hcxpcapngtool <options> *.cap
hcxpcapngtool <options> *.*

short options:
-o <file> : output WPA-PBKDF2-PMKID+EAPOL hash file (hashcat -m 22000)
            get full advantage of reuse of PBKDF2 on PMKID and EAPOL
-E <file> : output wordlist (autohex enabled on non ASCII characters) to use as input wordlist for cracker
            retrieved from every frame that contain an ESSID
-R <file> : output wordlist (autohex enabled on non ASCII characters) to use as input wordlist for cracker
            retrieved from PROBEREQUEST frames only
-I <file> : output unsorted identity list to use as input wordlist for cracker
-U <file> : output unsorted username list to use as input wordlist for cracker
-D <file> : output device information list
            format MAC MANUFACTURER MODELNAME SERIALNUMBER DEVICENAME UUID
-h        : show this help
-v        : show version

<SNIP>

```

Though the tool can be used for various tasks, we can use `hcxpcapngtool` to extract the hash as follows:

```shell
hcxpcapngtool cracking_pmkid.cap -o pmkidhash_corp

reading from cracking_pmkid.cap...

summary capture file
--------------------
file name................................: cracking_pmkid.cap
version (pcapng).........................: 1.0
operating system.........................: Linux 5.7.0-kali1-amd64
application..............................: hcxdumptool 6.0.7-22-g2f82e84
interface name...........................: wlan0
interface vendor.........................: 00c0ca
weak candidate...........................: 12345678
MAC ACCESS POINT.........................: 0c8112953006 (incremented on every new client)
MAC CLIENT...............................: fcc23374f354
REPLAYCOUNT..............................: 63795
ANONCE...................................: 4e0fee9e1a8961ca63b74023d90ac081d8677ae748b7050a559cf481cf50d31f
SNONCE...................................: 90d86a9fc2a314df52b3b36b9080c88e90488594f0aa83e84196bfce8b90d1ac
timestamp minimum (GMT)..................: 17.07.2020 10:07:19
timestamp maximum (GMT)..................: 17.07.2020 10:14:21
used capture interfaces..................: 1
link layer header type...................: DLT_IEEE802_11_RADIO (127)
endianess (capture system)...............: little endian
packets inside...........................: 75
frames with correct FCS..................: 75
BEACON (total)...........................: 1
PROBEREQUEST.............................: 3
PROBERESPONSE............................: 1
EAPOL messages (total)...................: 69
EAPOL RSN messages.......................: 69
ESSID (total unique).....................: 3
EAPOLTIME gap (measured maximum usec)....: 172313401
EAPOL ANONCE error corrections (NC)......: working
REPLAYCOUNT gap (suggested NC)...........: 5
EAPOL M1 messages (total)................: 47
EAPOL M2 messages (total)................: 18
EAPOL M3 messages (total)................: 4
EAPOL pairs (total)......................: 41
EAPOL pairs (best).......................: 1
EAPOL pairs written to combi hash file...: 1 (RC checked)
EAPOL M12E2 (challenge)..................: 1
PMKID (total)............................: 45
PMKID (best).............................: 1
PMKID written to combi hash file.........: 1

```

We can check the contents of the file to ensure that we captured a valid hash:

#### PMKID-Hash

```shell
cat pmkidhash_corp

7943ba84a475e3bf1fbb1b34fdf6d102*10da43bef746*80822381a9c8*434f52502d57494649

```

Once again, we will perform a straightforward dictionary attack in an attempt to crack the WPA handshake. To attempt to crack this hash, we will use mode `22000`, as the previous mode `16800` has been deprecated. Here, our command will be in the format:

#### Hashcat - Cracking PMKID

```shell
hashcat -a 0 -m 22000 pmkidhash_corp /opt/useful/seclists/Passwords/Leaked-Databases/rockyou.txt.tar.gz

hashcat (v6.2.6) starting...

<SNIP>

7943ba84a475e3bf1fbb1b34fdf6d102:10da43bef746:80822381a9c8:CORP-WIFI:cleopatra

Session..........: hashcat
Status...........: Cracked
Hash.Name........: WPA-PBKDF2-PMKID+EAPOL
Hash.Target......: pmkidhash_corp
Time.Started.....: Wed Mar  9 11:27:21 2022 (1 sec)
Time.Estimated...: Wed Mar  9 11:27:22 2022 (0 secs)
Guess.Base.......: File (/usr/share/wordlists/rockyou.txt)
Guess.Queue......: 1/1 (100.00%)
Speed.#1.........:    12563 H/s (3.49ms) @ Accel:1024 Loops:32 Thr:1 Vec:8
Recovered........: 1/1 (100.00%) Digests
Progress.........: 18130/14344385 (0.13%)
Rejected.........: 11986/18130 (66.11%)
Restore.Point....: 0/14344385 (0.00%)
Restore.Sub.#1...: Salt:0 Amplifier:0-1 Iteration:0-1
Candidates.#1....: 123456789 -> celtic07

Started: Wed Mar  9 11:27:20 2022
Stopped: Wed Mar  9 11:27:23 2022

```

The process with the now-deprecated `hcxpcaptool` is similar.

#### Hcxpcaptool - Legacy

```shell
hcxpcaptool -h

hcxpcaptool 6.0.3-23-g1c078e4 (C) 2020 ZeroBeat
usage:
hcxpcaptool <options>
hcxpcaptool <options> [input.pcap] [input.pcap] ...
hcxpcaptool <options> *.cap
hcxpcaptool <options> *.*

options:
-o <file> : output hccapx file (hashcat -m 2500/2501)
-O <file> : output raw hccapx file (hashcat -m 2500/2501)
            this will disable all(!) 802.11 validity checks
            very slow!
-k <file> : output PMKID file (hashcat hashmode -m 16800 new format)
-K <file> : output raw PMKID file (hashcat hashmode -m 16801 new format)
            this will disable usage of ESSIDs completely
-z <file> : output PMKID file (hashcat hashmode -m 16800 old format and john)
-Z <file> : output raw PMKID file (hashcat hashmode -m 16801 old format and john)
            this will disable usage of ESSIDs completely
-j <file> : output john WPAPSK-PMK file (john wpapsk-opencl)
-J <file> : output raw john WPAPSK-PMK file (john wpapsk-opencl)
            this will disable all(!) 802.11 validity checks
            very slow!
-E <file> : output wordlist (autohex enabled) to use as input wordlist for cracker
-I <file> : output unsorted identity list
-U <file> : output unsorted username list
-M <file> : output unsorted IMSI number list
-P <file> : output possible WPA/WPA2 plainmasterkey list
-T <file> : output management traffic information list
            format = mac_sta:mac_ap:essid
-X <file> : output client probelist
            format: mac_sta:probed ESSID (autohex enabled)
-D <file> : output unsorted device information list
            format = mac_device:device information string
-g <file> : output GPS file
            format = GPX (accepted for example by Viking and GPSBabel)
-V        : verbose (but slow) status output
-h        : show this help
-v        : show version

<SNIP>

```

The syntax is a bit different, using the `-z` flag instead of `-o` for the output file. Using `hcxpcaptool`, we can extract the PMKID hash to run through `Hashcat` in the same way we did with the resultant hash from `hcxpcapngtool`.

#### Extract PMKID - Using Hcxpcaptool

```shell
hcxpcaptool -z pmkidhash_corp2 cracking_pmkid.cap

reading from cracking_pmkid.cap
summary capture file:
---------------------
file name........................: cracking_pmkid.cap
file type........................: pcapng 1.0
file hardware information........: x86_64
capture device vendor information: 00c0ca
file os information..............: Linux 5.7.0-kali1-amd64
file application information.....: hcxdumptool 6.0.7-22-g2f82e84 (custom options)
network type.....................: DLT_IEEE802_11_RADIO (127)
endianness.......................: little endian
read errors......................: flawless
minimum time stamp...............: 17.07.2020 14:07:19 (GMT)
maximum time stamp...............: 17.07.2020 14:14:21 (GMT)
packets inside...................: 75
skipped damaged packets..........: 0
packets with GPS NMEA data.......: 0
packets with GPS data (JSON old).: 0
packets with FCS.................: 75
beacons (total)..................: 1
probe requests...................: 3
probe responses..................: 1
association responses............: 1
EAPOL packets (total)............: 69
EAPOL packets (WPA2).............: 69
PMKIDs (not zeroed - total)......: 1
PMKIDs (WPA2)....................: 45
PMKIDs from access points........: 1
best handshakes (total)..........: 1 (ap-less: 0)
best PMKIDs (total)..............: 1
summary output file(s):
-----------------------
1 PMKID(s) written to pmkidhash_corp

```

We can check the contents of the file to ensure that we captured a valid hash:

#### PMKID-Hash

```shell
cat pmkidhash_corp2

7943ba84a475e3bf1fbb1b34fdf6d102*10da43bef746*80822381a9c8*434f52502d57494649

```

From here we could run the `pmkidhash_corp2` file through Hashcat using mode `22000` as shown above.

* * *

## Closing Thoughts

Great! We have successfully cracked the PMKID hash and could now attempt to authenticate to the wireless network to gain a foothold or expand our reach during a real-world engagement.

This section covered some valuable techniques that can be used during penetration tests, wireless assessments, and red team assessments. They can also be used by defenders to test the security of their wireless networks. The attacks used to generate the example files used in this section will be covered in a wireless attacks module in HTB Academy.


# Skills Assessment

* * *

We have reached the end of the module!

Now let's put your password cracking skills to the test! This final skills assessment will test your knowledge of password cracking and `Hashcat` usage.

* * *

# Scenario

Your colleague is working on a penetration test for Inlanefreight and has asked you to crack several password hashes to help with their assessment.

1. Your colleague performed a successful SQL injection and obtained a hash. You must first identify the hash type and then crack the hash and provide the cleartext value.

```shell
0c67ac18f50c5e6b9398bfe1dc3e156163ba10ef

```

1. The cracked hash from the SQL injection attack paid off, and your colleague was able to gain a foothold on the internal network! They have been running the `Responder` tool and collecting a variety of hashes. They have been unable to perform a successful `SMB Relay` attack, so they need to obtain the cleartext password to gain a foothold in the Active Directory environment. Crack the provided NetNTLMv2 hash to help them proceed.

```shell
bjones::INLANEFREIGHT:699f1e768bd69c00:5304B6DB9769D974A8F24C4F4309B6BC:0101000000000000C0653150DE09D2010409DF59F277926E000000000200080053004D004200330001001E00570049004E002D00500052004800340039003200520051004100460056000400140053004D00420033002E006C006F00630061006C0003003400570049004E002D00500052004800340039003200520051004100460056002E0053004D00420033002E006C006F00630061006C000500140053004D00420033002E006C006F00630061006C0007000800C0653150DE09D20106000400020000000800300030000000000000000000000000300000B14866125D55255DD82C994C0D8AC3D9FF1A3EFDAECBE908F1F91C7BD4B05CF50A001000000000000000000000000000000000000900280063006900660073002F003100390032002E003100360038002E003100390035002E00310032003900000000000000000000000000

```

1. Great! Your colleague was able to use the cracked password and perform a Kerberoasting attack. One of the Kerberos TGS tickets retrieved is for a user that is a member of the Local Administrators group on one server. Can you help them crack this hash and move laterally to this server?

```shell
$krb5tgs$23$*sql_svc$INLANEFREIGHT.LOCAL$mssql/inlanefreight.local~1443*$80be357f5e68b4f64a185397bf72cf1c$579d028f0f91f5791683844c3a03f48972cb9013eddf11728fc19500679882106538379cbe1cb503677b757bcb56f9e708cd173a5b04ad8fc462fa380ffcb4e1b4feed820fa183109e2653b46faee565af76d5b0ee8460a3e0ad48ea098656584de67974372f4a762daa625fb292556b407c0c97fd629506bd558dede0c950a039e2e3433ee956fc218a54b148d3e5d1f99781ad4e419bc76632e30ea2c1660663ba9866230c790ba166b865d5153c6b85a184fbafd5a4af6d3200d67857da48e20039bbf31853da46215cbbc5ebae6a3b0225b6651ec8cc792c8c3d5893a8d014f9d297ac297288e76d27a1ed2942d6997f6b24198e64fea9ff5a94badd53cc12a73e9505e4dab36e4bd1ef7fe5a08e527d9046b49e730d83d8af395f06fe35d360c59ab8ebe2c3b7553acf8d40c296b86c1fb26fdf43fa8be2ac4a92152181b81afb1f4773936b0ccc696f21e8e0fe7372252b3c24d82038c62027abc34a4204fb6e52bf71290fdf0db60b1888f8369a7917821f6869b6e51bda15f1fd7284ca1c37fb2dc46c367046a15d093cc501f3155f1e63040313cc8db2a8437ee6dc8ceb04bf924427019b396667f0532d995e3d655b9fb0ef8e61b31e523d81914d9eb177529783c29788d486139e1f3d29cbe4d2f881c61f74ff32a9233134ec69f26082e8aaa0c0e99006a5666c24fccfd195796a0be97cecb257259a640641f8c2d58d2d94452ec00ad84078afc1f7f72f3b9e8210b5db73bf70cd13ef172ef3b233c987d5ec7ea12a4d4921a43fb670c9f48aaae9e1d48ec7be58638a8b2f89a62b56775deddbbc971803316470ee416d8a6c0c8d17982396f6c0c0eeec425d5c599fb60b5c39f8e9ceff4ee25c5bc953178972de616edae61586bb868e463f420e9e09c083662bcf6f0f522f78630792e02e6986f5dd042dfb70100ab59d8a01093b3d89949ea19fe9c596a8681e2a71abe75debd62b985d03d488442aa41cc8993eff0224de62221d39be8bf1d8b26f8f8768e90e5b4b886adaf02a19f55e6d1fd11b004d4e7b170c4f7feaa04b8dad207d6f863d50a251d9a9ce66951de41a3690fec6144e73428d4718cc7ec5eeeff841b4329a7ba51624f678557b6eafc55af026314cbf9dd9ca232977da3cce204899f3048101e0010f42d0076cd494526beea862c72ee48749ba071bcdd1a96c64a0d8f48c6acad7730121021be6323f69505aad8fb6281b7ac4a607d1d241f1fbffc70c4a74c997bb2fb77c452c0077efdea2a6c00704a8bee28326b5e554e1faa48a33963ce2c2e0e2446b4504a05d541bbaf531e1644ad92a2feae5b2eb8851b067e7bd8d7d23d82e63d368983ba44f52901cba7e05cfa35e832ec445a7de50eca670fa90

```

1. Your colleague was able to access the server and obtain the local SAM database's contents. One of the hashes is the Domain Cached credentials for a Domain Administrator user. This hash is typically very difficult to crack but, if successful, will grant full administrative control over the entire Active Directory Environment.

```shell
$DCC2$10240#backup_admin#62dabbde52af53c75f37df260af1008e

```

1. Success! The hash cracked, and your colleague retrieved the NTDS database containing the password hashes for all users within the Active Directory domain. Attempt to crack as many of the hashes in the NTDS file as possible. Submit the cleartext value of the password that appears 5 times as your answer.

Note: Though not required to complete the exercise, it is possible to crack 100% of the hashes in this NTDS file by using a variety of dictionary files (word lists) and some of the techniques discussed throughout this module. Challenge yourself! Can you get close to or arrive at 100% cracked?

The above scenario is quite common for what may happen during a real-world penetration test. You may run into scenarios where you can crack a hash and move further while other times, the hash is too difficult to crack. It is important to understand the various common hash types and attacks to be a successful and well-rounded information security professional.


