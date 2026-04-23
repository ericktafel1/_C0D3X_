### Links

- [Cross-Site Scripting (XSS) Cheat Sheet - 2023 Edition | Web Security Academy](https://portswigger.net/web-security/cross-site-scripting/cheat-sheet)
- [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings)
- [HackTricks](https://book.hacktricks.xyz/welcome/readme)

### GitHub repos and websites used

- [Payloads](https://micahvandeusen.com/burp-suite-certified-practitioner-exam-review/)
- [Burp Suite Certified Practitioner Exam Review](https://micahvandeusen.com/burp-suite-certified-practitioner-exam-review/)
- [BSCP Methodology](http://bscpcheatsheet.gitbook.io/)
- [MUST FOR EXAM](https://github.com/DingyShark/BurpSuiteCertifiedPractitioner)
- [MUST FOR EXAM 2](https://github.com/botesjuan/Burp-Suite-Certified-Practitioner-Exam-Study)

# MUST KNOWS

```ad-success
title: MUST
- **Default Credentials**:
	- Low-privilige: carlos
	- Admin: administrator
- One of them will visit the **homepage** every **15 seconds**
- They will click every link that they receive via **email**
- For **SSRF**:
	- localhost:6566
- Enumeration:
	- [[Usernames]]
	- [[Passwords]]
```

![3 stages](3stages.png)

# Initial
1. Use thorough scan
2. Check ***/.git***
3. Check ***/robots.txt***
4. Check ***/api***
5. Visit every endpoint
6. Active scan every endpoint
7. Content Discovery
8. Check for inline Javascript
9. Check the loaded Javascript files

# Stage1
- [ ] [[XSS]]
- [ ] [[CSRF]]
- [ ] [[Clickjacking]]
- [ ] [[DOM-based]]
- [ ] [[CORS]]
- [ ] [[Http request smuggling]]
- [ ] [[Access-control]]
- [ ] [[Authentication]]
- [ ] [[Web cache poisoning]]
- [ ] [[Http host header]]
- [ ] [[Oauth authentication]]
- [ ] [[Jwt]]

# Stage2
- [ ] [[XSS]]
- [ ] [[CSRF]]
- [ ] [[Clickjacking]]
- [ ] [[DOM-based]]
- [ ] [[CORS]]
- [ ] [[Http request smuggling]]
- [ ] [[Access-control]]
- [ ] [[Authentication]]
- [ ] [[Web cache poisoning]]
- [ ] [[Http host header]]
- [ ] [[Oauth authentication]]
- [ ] [[Jwt]]

# Stage3
- [ ] [[SQLInjection]]
- [ ] [[XXE]]
- [ ] [[SSRF]]
- [ ] [[Os command  injection]]
- [ ] [[Server side template injection]]
- [ ] [[Directory traversal]]
- [ ] [[InsecureDeserialization]]
- [ ] [[File upload vulnerabilities]]

