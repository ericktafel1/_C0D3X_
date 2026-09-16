# NTP and Time Synchronization

## Overview

Small reference page for clock correction and time-handling during Kerberos- or cert-sensitive operations.

## Default Ports

- 123/udp

## Time Sync Commands

```bash
sudo net time -c <RHOST>
sudo net time set -S <RHOST>
sudo net time \\<RHOST> /set /y
sudo ntpdate <RHOST>
sudo ntpdate -s <RHOST>
sudo ntpdate -b -u <RHOST>
sudo timedatectl set-timezone UTC
sudo timedatectl list-timezones
sudo timedatectl set-timezone '<COUNTRY>/<CITY>'
sudo timedatectl set-time 15:58:30
sudo timedatectl set-time '2015-11-20 16:14:50'
sudo timedatectl set-local-rtc 1
```

## Why It Matters Operationally

- Kerberos and certificate operations fail when the attacking host clock is materially wrong.
- Use these commands to align your box with the target environment before ticket or auth-heavy workflows.
- This page is intentionally small because the main value is fixing time quickly, not treating NTP as a full attack surface.

## See Also

- `03 AD/Kerberos.md`
- `06 Services/Kerberos.md`
