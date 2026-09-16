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
| Sub-Shell              | ` `` `                  | `%60%60`                  | Both **(Linux-only)**                      |
| Sub-Shell              | `$()`                   | `%24%28%29`               | Both **(Linux-only)**                      |
>[!Note:]
>Front-end may be validating user input. **Capture in Burp and Repeat the paylod to bypass front-end sanitization!**

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
### Bypassing Space Filters
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

### Bypassing Other Blacklisted Characters
