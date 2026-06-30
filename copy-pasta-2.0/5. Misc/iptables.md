sudo iptables -t nat -A PREROUTING -i eth0 -p tcp --dport 80 -j DNAT --to-destination 10.0.0.1  
  
iptables -t nat -A PREROUTING -i tun0 -p tcp --dport 443 -j DNAT --to-destination   
  
iptables -t nat -A PREROUTING -i eth0 -p tcp --dport 80 -j DNAT --to-destination   
  
# Enable Kernel Forwarding  
echo 1 | sudo tee /proc/sys/net/ipv4/ip_forward