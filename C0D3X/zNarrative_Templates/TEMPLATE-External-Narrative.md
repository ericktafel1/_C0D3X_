# Enterprise External
### OSINT
The penetration tester began the external penetration test by conducting reconnaissance as an unauthenticated attacker. The penetration tester reviewed the target organization's primary website searching for job postings which reveal technology stack details. This information is inventoried and cross referenced later during execution of port scan techniques. 


Email addresses for shared mailboxes was observed from the organization's website. Additional emails associated with individuals were also observed. These addresses were inventoried for later use in brute forcing attacks if externally exposed login pages were identified.


Procedures were performed to evaluate domain name records of the target assets searching for subdomains or aliased DNS records which may reveal privileged functionality accessible to an unauthenticated attacker. Additionally, public IP addresses corresponding to the DNS records were retrieved and cross-referenced with open source intelligence gathering platforms (i.e., Shodan). Shodan is a paid-for service which regularly scans the entire public internet inventorying technology stack information as well as open ports. The Shodan search results revealed an unencrypted web services on port 80 as well as an encrypted port on 443.

 
#### Shodan Testing Results If Any
submitted web requests to port 80 for the aliased DNS records identified by Shodan. Unauthenticated directory searches for the web service on port 80 was also performed. No additional subdirectories or functionality was revealed. Requests for TCP port 80 to the web application's DNS record, _app_dns_here_, returned a 301 redirect to the encrypted TCP port 443.

The penetration tester also conducted reconnaissance on the target organization to....

#### GitHub
The penetration tester performed internet searches to identify publicly accessible repositories for the target organization. Publicly available repositories can be used to identify information regarding an organization's underlying infrastructure or secrets which have been inadvertently committed to repositories. This information can be weaponized to narrow focus in search of CVEs or credentials to attack publicly available logins. The search results revealed...

#### Breach Data Search
The penetration tester searched breach data for username and passwords associated with the target organization's domain. Credentials sourced from the breach data were then used on the discovered login pages. However, no valid logins were obtained from using the breached credentials.

### Nmap
The penetration tester used Nmap to scan the full transmission control protocol (TCP) port range (1 - 65535) as well as the top one thousand (1000) user datagram protocol (UDP) ports. This procedure was executed to identify all open ports associated with the in-scope assets.  Exposing additional services (ports) may allow an unauthenticated attacker to compromise the underlying infrastructure or gain access to the internal network.

#### Nmap IPv6 Results
Similar Nmap scans were performed for IPv6 addresses which resolved for in-scope DNS endpoints for both TCP and UDP ports. The results returned....

#### Enumeration of Nmap Results
The penetration tester observed the following TCP port accessible on __IP_ADDRESS__. The penetration tester performed enumeration procedures to identify the services hosted on the open port. Enumeration procedures revealed...



### Unauthenticated directory scanning
The penetration tester performed directory search procedures for exposed web services using tools such as Fuzz Faster You Fool (FFuF). The penetration tester observed....

### 403 Forbidden Bypass Testing
The penetration tester evaluated directories which returned a 403 Forbidden response code employing techniques used to bypass the response code. This technique included injecting the `X-Original-URL` request header along with appending payloads to the URL path. The injected payloads are capable of bypass weak access controls.Fortreum observed none of the techniques were successful in bypassing the 403 Forbidden response code.

### Web technology enumeration
Nuclei, an automated vulnerability scanner, was executed to scan the target web application and gather intelligence related to underlying web framework technology as well as version information. The pentester also used Nikto, an automated web server scanner, was executed to against the target web application for technology fingerprinting, directory enumeration, and use of outdated software versions. Both of which produce no intelligence would could be weaponized by an unauthenticated attacker.

### Nessus
The penetration tester used Nessus to perform vulnerability scans for the in-scope assets. The Nessus scan results were reviewed which revealed...


### Smuggler
Smuggler, an automated tool used to detect HTTP request smuggling vulnerabilities, was used to scan the target endpoints. No vulnerabilities related to HTTP request smuggling were detected.

### TLS Scanning
The penetration tester used Testssl.sh to evaluate the web application's configuration for encrypting data in-transit (HTTPS). The penetration tester observed no misconfigurations related to TLS protocol nor cipher suite which introduced vulnerability into the web application.

#### FIPS Endpoint Info if CBC Detected
Testssl did detect use of CBC cipher suites, however the in-scope endpoints are FIPS certified through the National Institute of Standards (NIST) Cryptographic Module Validation Program. CBC cipher suites must be resistant to padding oracle attacks in order to be certified through the program.

#### CBC
The penetration tester observed the web application endpoint as supporting cipher suites with cipher block chaining (CBC) mode of symmetric encryption. These cipher suites are vulnerable to CVE-2013-0169 Lucky13, which can allow an attacker adept in cryptanalysis to recover plaintext from ciphertext. A finding has been created for the affected endpoint.

### Login Panel Testing
WP-Scan was used for the xxx.com web application. This resulted in enumerating several usernames for the Wordpress instance, however none of the discovered accounts were discovered in the breach data.

#### Hydra
Hydra, a brute forcing tool, was used to automate testing for valid credentials using a wordlist of vetted common usernames and breached passwords. Hydra revealed...