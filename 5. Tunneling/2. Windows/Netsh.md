# Port Forward   
```
netsh interface portproxy add v4tov4 listenport=$LPORT listenaddress=$LADDR connectport=$RPORT connectaddress=$RADDR  
```
  
# Verify port forward  
```
netsh interface portproxy show v4tov4  
netsh interface portproxy show all
```
# Delete Port Forward  
```
netsh interface portproxy del v4tov4 listenport=2200 listenaddress=192.168.195.64
```