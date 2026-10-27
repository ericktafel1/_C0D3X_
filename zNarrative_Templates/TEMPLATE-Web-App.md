# FedRAMP / Enterprise Web Application Pentest - Narrative Template

## OSINT / Reconnaissance

COMPANY began the web application penetration test by conducting reconnaissance as an unauthenticated attacker. COMPANY reviewed the target organization's primary website searching for job postings which reveal technology stack details. This information was inventoried and cross-referenced later during execution of port scan and fingerprinting techniques.

### OSINT & Intelligence Gathering
Email addresses for shared mailboxes were observed from the organization's website. Additional emails associated with individuals were also observed. These addresses were inventoried for later use in brute forcing attacks if externally exposed login pages were identified.

### Google Dorking & Source Code Analysis
COMPANY performed internet searches (Google Dorking) to identify publicly indexed documentation (`filetype:pdf OR filetype:txt OR filetype:docx OR filetype:xlsx OR filetype:pptx`) and open job postings for the target organization which could be used to fingerprint the underlying technology stack. *insert results here*.

COMPANY performed internet searches to identify publicly accessible GitHub repositories for the target organization. Publicly available repositories can be used to identify information regarding an organization's underlying infrastructure or secrets which have been inadvertently committed to repositories. Trufflehog was used to search identified repositories for the presence of secrets. The search results revealed... *insert results here*.

COMPANY searched breach data for usernames and passwords associated with the target organization's domain. Credentials sourced from the breach data were then used against discovered login pages. *insert results here - note whether valid logins were obtained*.

### Passive Reconnaissance - DNS and Subdomains

COMPANY performed an nslookup of the target endpoint(s) to enumerate associated public IPv4 and IPv6 addresses. Procedures were performed to evaluate domain name records of the target assets searching for subdomains or aliased DNS records which may reveal privileged functionality accessible to an unauthenticated attacker. Subfinder, Assetfinder, and Amass were used to perform passive subdomain enumeration. The results revealed... *insert results here*.

Public IP addresses corresponding to the DNS records were cross-referenced with open source intelligence gathering platforms (i.e., Shodan). Shodan is a paid-for service which regularly scans the entire public internet, inventorying open ports and technology stack information. The Shodan search results revealed... *insert results here (e.g., unencrypted web service on port 80, encrypted service on port 443)*.

#### Shodan Testing Results

COMPANY submitted web requests to port 80 for the aliased DNS records identified by Shodan. Unauthenticated directory searches for the web service on port 80 were also performed. *insert results here*. Requests for TCP port 80 to the web application's DNS record, *app\_dns\_here*, returned... *insert results here (e.g., 301 redirect to encrypted TCP port 443)*.

## Active Reconnaissance

### Port Scanning

COMPANY used Nmap to scan the full transmission control protocol (TCP) port range (1 - 65535) as well as the top one thousand (1000) user datagram protocol (UDP) ports for all in-scope assets. This procedure was executed to identify all open ports associated with the in-scope assets, as exposing additional services (ports) may allow an unauthenticated attacker to compromise the underlying infrastructure or gain access to the internal network. COMPANY observed... *insert results here*.

Similar Nmap scans were performed for IPv6 addresses which resolved for in-scope DNS endpoints for both TCP and UDP ports. The results returned... *insert results here*.

COMPANY observed the following TCP port(s) accessible on **IP\_ADDRESS**. COMPANY performed enumeration procedures to identify the services hosted on the open port(s). Enumeration procedures revealed... *insert results here*.

### Unauthenticated Directory Searches

COMPANY performed directory search procedures for exposed web services using tools such as FFuF, Dirb, and Katana. The goal of this procedure was to identify directories or pages exposed to an unauthenticated attacker, specifically pages with enhanced functionality or additional login pages. COMPANY observed... *insert results here*.

### 403 Forbidden Bypass Testing

COMPANY evaluated directories which returned a 403 Forbidden response code, employing techniques used to bypass the response code. This technique included injecting the `X-Original-URL` request header along with appending payloads to the URL path, which are capable of bypassing weak access controls. COMPANY observed... *insert results here*.

### Web Technology / Framework Enumeration

Nuclei, an automated vulnerability scanner, was executed against the target web application to gather intelligence related to the underlying web framework technology and version information. COMPANY also used Nikto, an automated web server scanner, against the target web application for technology fingerprinting, directory enumeration, and identification of outdated software versions. COMPANY observed... *insert results here*.

### Nessus

COMPANY used Nessus to perform vulnerability scans for the in-scope assets. The Nessus scan results were reviewed, which revealed... *insert results here*.

## Network & Transport Layer Testing

### TLS / Cipher Suite Testing

COMPANY used Testssl.sh to evaluate the web application's configuration for encrypting data in-transit (HTTPS). COMPANY observed... *insert results here (misconfigurations related to TLS protocol or cipher suite, non-ephemeral key exchange, use of SHA-1 for signatures, etc.)*.

#### CBC Cipher Suites (if detected)

Testssl detected use of cipher block chaining (CBC) mode cipher suites. *If the in-scope endpoint is FIPS certified through the NIST Cryptographic Module Validation Program, note that CBC suites certified through the program must be resistant to padding oracle attacks. If not FIPS certified, evaluate for CVE-2013-0169 (Lucky13) and determine whether a finding is warranted; exploitation of Lucky13 over the public internet has proven difficult, and a finding is typically not warranted absent updated NIST guidance.*

### HTTP Request Smuggling

Smuggler, an automated tool used to detect HTTP request smuggling vulnerabilities, was used to scan the target endpoints. *insert results here*. COMPANY also performed manual testing using Transfer-Encoding probe payloads and combinations of Content-Length and Transfer-Encoding headers to confirm or rule out findings identified by automated tooling. *insert results here*.

*If the engagement is scoped for FedRAMP and the target asset supports HTTP/1.1, document this in the narrative and recommend the client disable HTTP/1.1. If scoped for Enterprise, document an informational finding when HTTP/1.1 is supported but no smuggling vulnerability is identified.*

## Authenticated Testing

COMPANY authenticated to the target web application using credentials provided by the client and navigated all available pages and functionality to inventory the site map within Burp Suite. This site map was used as the foundation for subsequent authenticated testing procedures described below.

### Vulnerable Third-Party Components (Software Supply Chain)

Burp Suite's Active Scan functionality was used to identify use of third-party components within the target web application and associated common vulnerability exposures (CVEs). *If third-party components with known CVEs are detected, note that research was performed to identify proof-of-concept exploits and exploitation was tested.* COMPANY observed... *insert results here*.

## Session Management Testing

COMPANY observed the target web application uses *JSON Web Tokens (JWTs) / non-JWT session identifiers (e.g., cookies, headers)* to manage authenticated sessions. *Select the applicable subsection(s) below based on the session token type observed.*

### JWT

JWT\_Tool was used to inspect and tamper with the application's JWTs. COMPANY tested removal of the cryptographic signature, tested algorithm confusion (`none`/`NoNe`/`nOnE`), and, where the signing algorithm was HS256, attempted to crack the signing secret using Hashcat against a wordlist. COMPANY observed... *insert results here*.

COMPANY also tested token invalidation by invoking a logout request and resubmitting the previously issued JWT, and by resubmitting a JWT after its expiration timestamp. COMPANY observed... *insert results here*.

### Non-JWT

COMPANY evaluated the session identifier for predictability and encoding. Burp Suite Intruder's Character Frobber and Bit Flipper attacks were used to determine whether the session identifier could be systematically guessed. COMPANY also tested token invalidation by submitting a logout request followed by reuse of the previously issued session identifier. COMPANY observed... *insert results here*.

## Broken Access Control

### Server-Side Request Forgery (SSRF)

COMPANY identified functionality within the target web application which consumes user-supplied input to initiate server-side requests. COMPANY tested whether this functionality could be manipulated to issue requests to attacker-controlled infrastructure (Burp Collaborator) as well as internal or cloud metadata endpoints (e.g., `169.254.169.254`). COMPANY observed... *insert results here*.

### Cross-Site Request Forgery (CSRF)

COMPANY identified requests which invoke state-changing actions (POST, PATCH, PUT) and used Burp Suite's CSRF PoC generator to craft and execute a proof-of-concept request within the same browser session as an authenticated user, excluding session identifiers and CSRF tokens from the payload. COMPANY observed... *insert results here*.

### Cross-Origin Resource Sharing (CORS)

COMPANY reviewed response headers for permissive CORS configurations (e.g., `Access-Control-Allow-Origin: *` combined with `Access-Control-Allow-Credentials: true`). COMPANY also tampered with the `Origin` request header - including injection of a Burp Collaborator DNS value and IP address - regardless of whether a permissive header was initially observed. COMPANY observed... *insert results here*.

### Insecure Direct Object Reference (IDOR)

COMPANY evaluated URL, header, and body parameters for predictable or enumerable object identifiers and attempted to access or modify resources belonging to another user context, testing for both horizontal and vertical privilege escalation. Where role or permission values were observed in requests, COMPANY attempted to manipulate these values to escalate privileges. COMPANY observed... *insert results here*.

### MFA Bypass

COMPANY inspected traffic during login and MFA challenge flows for user-controllable parameters capable of overriding server-side MFA verification state (e.g., `isMFAVerified:false`). COMPANY also tested OTP reuse, OTP brute forcing absent lockout controls, manipulation of failed MFA responses, and backup code exhaustion / fallback path weaknesses, where MFA functionality was present. COMPANY observed... *insert results here*.

## Security Misconfiguration

### XML External Entity (XXE) Testing

Where the target web application accepted XML input, COMPANY tested for processing of external entity definitions capable of local file disclosure, server-side request forgery, and out-of-band data exfiltration, including blind XXE techniques. COMPANY observed... *insert results here*.

### Cookie Configuration

COMPANY reviewed sensitive cookies issued by the target web application for the presence of the Secure, HttpOnly, and SameSite attributes. COMPANY observed... *insert results here*.

### GraphQL Testing

Where a GraphQL endpoint was identified, COMPANY tested whether introspection queries were enabled, which could expose the application's full schema, including sensitive field names. COMPANY observed... *insert results here*.

## Insecure Design

### File Upload Functionality

COMPANY identified file upload functionality and evaluated whether anti-malware scanning was performed by uploading a file containing the EICAR test payload, then re-downloading the file to confirm whether the payload remained intact. Where file type restrictions were enforced, COMPANY tested whether the restriction could be bypassed via MIME-type manipulation. COMPANY observed... *insert results here*.

## Input Validation / Injection

### Cross-Site Scripting (XSS)

COMPANY tested input fields via both the application frontend and intercepted requests for reflected, stored, and DOM-based cross-site scripting. Prior to attempting to escalate XSS toward session token theft, COMPANY first evaluated the Secure and HttpOnly attributes applied to session tokens, as HttpOnly prevents script-based access to cookie values. COMPANY observed... *insert results here*.

### Remote Code Execution (RCE)

COMPANY identified application functionality which executes commands on the underlying server host and tested whether command separators could be used to append additional operating system commands. COMPANY observed... *insert results here*.

### SQL Injection

COMPANY identified areas of the application where user-supplied input is incorporated into backend database queries. SQLMap was used to perform automated detection, with manual confirmation performed via Burp Suite Repeater. COMPANY observed... *insert results here*.

### NoSQL Injection

Where the backend database utilized NoSQL technology (e.g., MongoDB, CosmosDB), COMPANY tested operator-based injection payloads (e.g., `$ne`, `$gt`, `$regex`) against body parameters. COMPANY observed... *insert results here*.

### Server-Side Template Injection (SSTI)

COMPANY tested user-controllable input reflected into server-side rendered templates for evaluation of template syntax (e.g., `{{7*7}}`). COMPANY observed... *insert results here*.

### Hidden Input Parameters

COMPANY used Param Miner to identify hidden HTTP header and body parameters which, when supplied by the client, are processed or reflected by the server-side application. COMPANY observed... *insert results here*.

## Software or Data Integrity Failures

### Java Serialization

Where Base64-encoded cookies or request parameters exhibited Java serialization magic bytes (`rO0AB`), COMPANY analyzed the serialized object and, where feasible, tested for insecure deserialization leading to remote code execution using known gadget chains. COMPANY observed... *insert results here*.

### JSON Parameter Manipulation

COMPANY reviewed request and response bodies for parameters returned by the server but not included in the original request (e.g., `isAdmin`), and tested whether supplying or modifying these parameters in the request influenced server-side behavior. COMPANY observed... *insert results here*.

## Sensitive Information Disclosure

COMPANY inspected web traffic in Burp Suite while traversing all pages of the target web application in search of disclosed secrets, such as passwords, API keys, or cloud credentials transmitted to the client. Trufflehog was used to automate detection of secrets across identified source repositories. COMPANY observed... *insert results here*.

## Business Logic

COMPANY evaluated multi-step processes within the target web application (e.g., checkout or purchase flows) for logic flaws, including step-skipping, race conditions in concurrent request handling, and parameter manipulation of pricing or quantity values. COMPANY observed... *insert results here*.

## Rate Limiting

COMPANY evaluated the target web application for non-volumetric and volumetric denial-of-service conditions, including submission of malformed input types to trigger unhandled backend exceptions and submission of concurrent requests using Burp Suite Intruder / Turbo Intruder. COMPANY observed... *insert results here*.

## Tenant-to-Tenant Testing (FedRAMP)

*Applicable to multi-tenant FedRAMP engagements.* COMPANY authenticated to the target web application as an account authorized for a separate tenant and used the Autorize Burp Suite extension to automate replacement and removal of session-related headers across the previously inventoried site map, testing for both authorization (AuthZ) and authentication (AuthN) bypass. Results flagged as "bypassed" were manually reviewed to rule out false positives (e.g., endpoints returning generic, non-sensitive data). COMPANY observed... *insert results here*.