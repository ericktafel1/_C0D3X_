# FedRAMP Vector 6 - Client Application
## OSINT
The penetration tester began the FedRAMP assessment for the target client-side application by conducting reconnaissance. Procedures were performed to identify publicly available information for the target application which could be weaponized by threat actors to attack the server-side infrastructure.

Security advisories were reviewed for the target application. None were observed which could exploited on the target client-side application.

The server-side endpoint configured for use by the target client-side application was then passively evaluated to identify cloud provider and technology stack. Open ports for the server-side endpoint were reviewed using data from Shodan, a paid-for service which regularly scans the entire public internet inventorying open ports. This information can provide insight when pursuing attack vectors of a cloud service provider via a trusted client-side application.

## Recon via Installed Application
The target client-side application was then installed on a test client _insert operating system version and info_. The agent was downloaded from _insert source here_.

## NMAP
The penetration tester used Nmap to scan the client-side application. Nmap scans were performed for both the full transmission control protocol (TCP) port range (1 - 65535) as well as the top one thousand (1000) user datagram protocol (UDP) ports. This procedure was executed to identify all ports opened by the client-side application which could be exploited to allow an attacker to gain unauthorized access to the client or attack the server-side application. The penetration tester observed……no vulnerabilities which could be exploited as a result of the exposed UDP ports.

## App Install Directory and Static Analysis
Application binaries from the client-side application were imported and analyzed in Ghidra, a source code reverse engineering tool. The penetration tester reviewed defined strings identified by Ghidra in search of clear text credentials or other sensitive information. Source code for client-side binaries was also evaluated for enhanced functionality or other intelligence which could be abused to allow for escalation of access to the server-side application. The penetration tester observed no sensitive data embedded in the binaries nor any functionality which could be weaponized to attack the server-side application.

The penetration tester configured the test host system to use a proxy (Burp Suite) for intercepting web traffic. The penetration tester observed… _insert comments for observed web traffic_.

### Java Decompiler
- https://java-decompiler.github.io/


### Grep for Secrets

### Semgrep

### Dependency Check
- https://github.com/dependency-check/DependencyCheck
- `./dependency-check.sh --nvdApiKey _API_KEY_ --scan /source/project/here/`

## Authorization
The penetration tester observed the client-side application uses JSON Web Tokens (JWTs) to authenticate to the server-side application. JWT_Tool was used to inspect, and tamper with JWTs. The penetration tester observed JWTs were configured with a six (6) month expiration period. A finding has been created for the long expiration period.

## Data Storage
The penetration tester reviewed the contents of the installation directory created by the target client-side application in search of sensitive information such as credentials, secrets, etc.

The penetration tester observed a keychain file in the /Library/Application Support/_app-name-here/_ directory with permissions restricted to the _appname user. The penetration tester created a copy of the keychain file while modifying permissions for read/write access. The keychain file was observed to contain no entries.

## Injection via User Interface
The penetration tester observed the client-side application provides no input fields in the user interface. User input is limited to a single drop-down box with pre-defined listings. The penetration tester no opportunities for exploitation of injection vulnerabilities via user-controlled input of the agent's user interface.

## Third-Party Vulnerabilities
The penetration tester observed the target application installs the following third-party components which have published common vulnerability exposures (CVEs). A finding has been created for this to

## DLL Hijacking


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
The penetration tester evaluated directories which returned a 403 Forbidden response code employing techniques used to bypass the response code. This technique included injecting the `X-Original-URL` request header along with appending payloads to the URL path. The injected payloads are capable of bypass weak access controls. The penetration tester observed none of the techniques were successful in bypassing the 403 Forbidden response code.

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

 