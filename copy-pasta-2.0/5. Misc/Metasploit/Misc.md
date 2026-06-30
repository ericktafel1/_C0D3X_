# Keep a listener active after a session dies

```
 ExitOnSession -> False 
```


# Disable Handler from binding if already started

```
set DisablePayloadHandler true
```


# Database
```
db_status
db_connect -y /usr/share/metasploit-framework/config/database.yml
```

# Hosts in DB

```
db_import hosts.xml 
```


# Set global hosts

```
setg lhost 192.168.50.1
unsetg
```

# Recon

## Search
```
search auxiliary/scanner/
```


 # Post
```

```

