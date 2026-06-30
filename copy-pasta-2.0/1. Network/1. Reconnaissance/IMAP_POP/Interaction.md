IP=10.129.202.20
USER=tom
PASSWORD=NMds732Js2761

```
curl -k ‘imaps://$IP’ --user $USER:$PASSWORD -v

openssl s_client -connect $IP:pop3s

openssl s_client -connect $IP:imaps
```

### pop3

```
USER user

PASS password
```

## imap

```
A1 LOGIN username password
```