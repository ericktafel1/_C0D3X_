# ICMP Tunneling
  
git clone https://github.com/utoni/ptunnel-ng.git  
sudo ./autogen.sh   
  

>[!NOTE] On Target
```
sudo ./ptunnel-ng -r10.129.202.64 -R22  
```
  
>[!NOTE] Local

```
sudo ./ptunnel-ng -p10.129.202.64 -l2222 -r10.129.202.64 -R22  
```
  
then throw whateva you want at the local tunnel  
```
ssh -p2222 -lubuntu 127.0.0.1
```