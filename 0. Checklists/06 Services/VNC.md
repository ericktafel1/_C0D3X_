# VNC

## Overview

Remote desktop access where VNC is exposed or proxied.

## Default Ports

- 5900/tcp and adjacent ports for display offsets

## Quick Enumeration

```bash
nmap --script=vnc-info -p 5900 <target>
vncviewer <target>:5900
```

## Useful Additions

```bash
nmap --script vnc-info,vnc-title -p 5900-5905 <target>
vncviewer <target>:5900
```

## Common Attack Paths

- Weak or missing authentication.
- Credential reuse against desktop sessions.
- Desktop-only admin workflows that expose local secrets, browser sessions, or control panels.

## See Also

- `06 Services/RDP.md`
