> Source: `01101100-C0D3X-00110110.md` → `Footprinting Services > NFS`

```
# Show available NFS shares
showmount -e <IP>

# Mount the specific NFS share.umount ./target-NFS
mount -t nfs <FQDN/IP>:/<share> ./target-NFS/ -o nolock
```


## NFS EXPORTS?  (→ nfs_exports.txt)

> Source: `01101100-C0D3X-00110110.md` → `NFS EXPORTS?  (→ nfs_exports.txt)`

```bash
for ip in $(cat online); do showmount -e "$ip" 2>/dev/null | grep -q "export list" && echo $ip; done | tee nfs_exports.txt
```


## NFS

> Source: `01101100-C0D3X-00110110.md` → `Enumeration > Service Enumeration > NFS`

```bash
showmount -e <target>
mount -t nfs <target>:/share /mnt
```


## NFS Shares

> Source: `01101100-C0D3X-00110110.md` → `Exploitation > Service Exploitations > NFS Shares`

```bash
showmount -e <target>
```

```bash
mount -t nfs <target>:/share /mnt
```
