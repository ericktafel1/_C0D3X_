# DNS

## Overview

Service discovery, record enumeration, and transfer validation. Keep this page focused on DNS itself rather than generic subdomain workflow.

## Default Ports

- 53/tcp, 53/udp

## Quick Enumeration

```
# NS request to the specific nameserver.
dig ns <domain.tld> @<nameserver>

# ANY request to the specific nameserver
dig any <domain.tld> @<nameserver>

# AXFR request to the specific nameserver.
dig axfr <domain.tld> @<nameserver>
```

## Useful Additions

```bash
dig +short A <host>
dig +short PTR <reversed-ip>.in-addr.arpa
dig @<dns-server> <name> A
dig @<dns-server> <name> ANY
dnsrecon -d <domain> -n <dns-server>
dnsenum <domain>
```

## Common Attack Paths

- Zone transfer (`AXFR`) against each authoritative nameserver.
- Split-horizon mistakes that return internal names when queried from reachable infrastructure.
- SRV records that expose Kerberos, LDAP, SIP, or mail infrastructure.
- TXT records leaking verification tokens, service metadata, or operational notes.

## See Also

- `01 Enumeration/External and Network Enumeration.md`
- `02 Web/Content Discovery and VHosts.md`
