
Apache Proxy that allows a standalone web server such as Apache to talk to Tomcat
- Open on port `8009 TCP`
- Binary Protocol
- Can configure our own nginx or Apache webserver to talk to it.

Create a file called tomcat-users.xml
```xml
<tomcat-users>
  <role rolename="manager-gui"/>
  <role rolename="manager-script"/>
  <user username="tomcat" password="s3cret" roles="manager-gui,manager-script"/>
</tomcat-users>
```

Start Apache Tomcat by doing:
```bash
sudo docker run -it --rm -p 8009:8009 -v `pwd`/tomcat-users.xml:/usr/local/tomcat/conf/tomcat-users.xml --name tomcat "tomcat:8.0"
```

Now do the following to access the hidden tomcat manager
- Download the Nginx source code
- Download the required module
- Compile Nginx source code with the `ajp_module`.
- Create a configuration file pointing to the AJP Port

#### Download Nginx Source Code
```bash
wget https://nginx.org/download/nginx-1.21.3.tar.gz
```
```bash
tar -xzvf nginx-1.21.3.tar.gz
```

#### Compile Nginx source code with the ajp module

```bash
git clone https://github.com/dvershinin/nginx_ajp_module.git
cd nginx-1.21.3
sudo apt install libpcre3-dev
./configure --add-module=`pwd`/../nginx_ajp_module --prefix=/etc/nginx --sbin-path=/usr/sbin/nginx --modules-path=/usr/lib/nginx/modules
make
sudo make install
nginx -V
```

Modify nginx.conf

Comment out the entire `server` block and append the following lines inside the `http` block in `/etc/nginx/conf/nginx.conf`.

```bash
upstream tomcats {
	server <TARGET_SERVER>:8009;
	keepalive 10;
	}
server {
	listen 80;
	location / {
		ajp_keep_conn on;
		ajp_pass tomcats;
	}
}
```

```bash
sudo apt install libapache2-mod-jk
bradhinca@htb[/htb]$ sudo a2enmod proxy_ajp
bradhinca@htb[/htb]$ sudo a2enmod proxy_http
bradhinca@htb[/htb]$ export TARGET="<TARGET_IP>"
bradhinca@htb[/htb]$ echo -n """<Proxy *>
Order allow,deny
Allow from all
</Proxy>
ProxyPass / ajp://$TARGET:8009/
ProxyPassReverse / ajp://$TARGET:8009/""" | sudo tee /etc/apache2/sites-available/ajp-proxy.conf
bradhinca@htb[/htb]$ sudo ln -s /etc/apache2/sites-available/ajp-proxy.conf /etc/apache2/sites-enabled/ajp-proxy.conf
bradhinca@htb[/htb]$ sudo systemctl start apache2
``` 