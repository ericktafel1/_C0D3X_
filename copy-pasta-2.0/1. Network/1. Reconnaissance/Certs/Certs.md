
# Using CRT.SH


```
curl -s "https://crt.sh/?q=${TARGET}&output=json" | jq -r '.[] | "\(.name_value)\n\(.common_name)"' | sort -u > "${TARGET}_crt.sh.txt"

head -n20 ${TARGET}_crt.sh.txt
```

# Using OpenSSL


```
export TARGET="facebook.com"

export PORT="443"

openssl s_client -ign_eof 2>/dev/null <<<$'HEAD / HTTP/1.0\r\n\r' -connect "${TARGET}:${PORT}" | openssl x509 -noout -text -in - | grep 'DNS' | sed -e 's|DNS:|\n|g' -e 's|^\*.*||g' | tr -d ',' | sort -u
```

TheHarvester

sources.txt

baidu

bufferoverun

crtsh

hackertarget

otx

projecdiscovery

rapiddns

sublist3r

threatcrowd

trello

urlscan

vhost

virustotal

zoomeye

```
cat sources.txt | while read source; do theHarvester -d "${TARGET}" -b $source -f "${source}_${TARGET}";done

cat *.json | jq -r '.hosts[]' 2>/dev/null | cut -d':' -f 1 | sort -u > "${TARGET}_theHarvester.txt"
```