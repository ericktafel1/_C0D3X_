# MongoDB

## Overview

MongoDB access, collection review, user/credential inspection, and application-state abuse.

## Default Ports

- 27017/tcp default

## Quick Enumeration

```bash
mongo "mongodb://<target>:27017"
mongosh "mongodb://<target>:27017"
nmap -sV -p 27017 --script mongodb-info <target>
```

## Authentication and Abuse Notes

- Test unauthenticated access before assuming auth is enforced.
- Review `admin`, `local`, and application databases for credential material, API secrets, and session collections.
- Modifying roles or user documents can become immediate application-level privilege escalation when the app trusts DB state directly.

## See Also

- `08 Post Exploitation/Credentials and Secrets.md`
