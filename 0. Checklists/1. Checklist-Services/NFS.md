# NFS

## Overview

Network file share enumeration, mount checks, and root-squash related abuse.

## Default Ports

- 2049/tcp+udp NFS, often 111/tcp+udp RPC portmapper

## Quick Enumeration

```
# Show available NFS shares
showmount -e <IP>

# Mount the specific NFS share.umount ./target-NFS
mount -t nfs <FQDN/IP>:/<share> ./target-NFS/ -o nolock
```

## NFS EXPORTS?  (→ nfs_exports.txt)

```bash
for ip in $(cat online); do showmount -e "$ip" 2>/dev/null | grep -q "export list" && echo $ip; done | tee nfs_exports.txt
```

## NFS

```bash
showmount -e <target>
mount -t nfs <target>:/share /mnt
```

## NFS Shares

```bash
showmount -e <target>
bash
mount -t nfs <target>:/share /mnt
```

## Common Attack Paths

- World-readable exports leaking home directories, backups, source code, or SSH material.
- `no_root_squash` exports enabling root-owned file placement or SUID abuse from a mounted share.
- Writable web roots or cron/script directories mounted over NFS and executed elsewhere.

## See Also

- `05 Linux/Privilege Escalation.md`
- `09 Movement/File Transfers.md`
