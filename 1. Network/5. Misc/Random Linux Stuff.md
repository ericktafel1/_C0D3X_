
## get listening sockets

```
ss -ntplu
```

## find process bound to port

```
lsof -i :port

fuser port/tcp
```