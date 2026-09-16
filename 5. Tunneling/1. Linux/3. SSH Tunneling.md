export LPORT="8834"  
export RPORT="8834"  
export TARGET="htb-student@10.129.202.116"  
  
# Forward Tunnels

  
## Tunning to local ports on SSH target  
```
ssh -L $LPORT:127.0.0.1:$RPORT $TARGET  
```
  
## Tunneling to other targets through SSH target (can set up multiple tunnels through same command)  

```
ssh -L $LPORT:$TARGETTWO:$RPORT $LPORT:$TARGETTWO:$RPORT $TARGET  
```
  
## -N prevents executing any remote commands  
```
ssh -N -L 0.0.0.0:4455:172.16.248.217:445 database_admin@10.4.248.215  
```
  
# Reverse Tunnel
c
```
ssh -N -R $TARGETONE:8080:0.0.0.0:8000 $TARGETTWO -v  
ssh -N -R 127.0.0.1:2345:10.4.195.215:5432 kali@192.168.45.157  
```
  

# Dynamic Tunnel 
  
```
ssh -N -D 0.0.0.0:9999 database_admin@10.4.248.215  
```
  

# Reverse Dynamic Tunnel

```
ssh -N -R 9998 kali@192.168.118.4  
```
  
  
# Using ncat to proxy through an SSH tunnel  
```
ssh -o ProxyCommand='ncat --proxy-type socks5 --proxy 127.0.0.1:1080 %h %p' database_admin@10.4.197.215
```