# IMAP and POP3

## Overview

Mailbox access and enumeration. Use this after valid credentials are found or when mail services are exposed without proper controls.

## Default Ports

- 143/tcp IMAP, 993/tcp IMAPS, 110/tcp POP3, 995/tcp POP3S

## Quick Enumeration

```
# Log in to the IMAPS service using cURL
curl -k 'imaps://<FQDN/IP>' --user <user>:<password>

# Connect to the IMAPS service
openssl s_client -connect <FQDN/IP>:imaps

# Connect to the POP3s service
openssl s_client -connect <FQDN/IP>:pop3s
```

## Manual Login Examples

```bash
openssl s_client -quiet -connect <target>:993
a1 LOGIN <user> <password>
a2 LIST "" "*"
a3 SELECT INBOX
a4 FETCH 1 BODY[]
a5 LOGOUT
```
```bash
openssl s_client -quiet -connect <target>:995
USER <user>
PASS <password>
LIST
RETR 1
QUIT
```

## Common Attack Paths

- Password reuse against mailboxes discovered during spraying.
- Password reset and MFA links found in inboxes after user compromise.
- Internal naming, ticketing, or host references leaked through mailbox content.

## See Also

- `07 Creds and Cracking/Password Spraying and Reuse.md`
