# API Penetration Testing Narrative Template

## Preliminary Procedures & Engagement Setup

### Statement of Work (SOW) Verification
COMPANY began the API penetration test by verifying the Statement of Work (SOW) to confirm authorized testing boundaries and ensure no unapproved assets were targeted[cite: 2]. COMPANY used this verification procedure to establish strict legal compliance and alignment with the client's explicit authorization rules before executing any testing traffic[cite: 2]. This resulted in a fully defined and authorized operational scope for the assessment[cite: 2].

### Burp Suite Logger & Logger++
To maintain comprehensive operational tracking and evidentiary support, COMPANY utilized daily operational backups of working notes, artifacts, and proxy logs through Burp Suite Logger and Logger++[cite: 2]. COMPANY used these logging tools to capture and secure all HTTP/HTTPS traffic streams, ensuring that every request and response observed during testing was permanently recorded[cite: 2]. This resulted in secure daily backups exported to Fortreum-approved cloud storage repositories, facilitating robust reporting and traceability[cite: 2]. Furthermore, COMPANY maintained a structured strategy of gathering and weaponizing information by correlating response headers and technology stack fingerprints with known Common Vulnerabilities and Exposures (CVEs) to evaluate realistic attack paths[cite: 2].

## OSINT & Passive Reconnaissance

### Nslookup
COMPANY performed initial network reconnaissance by executing `nslookup` queries against the primary target endpoints[cite: 2]. COMPANY used this utility to resolve target domain names and ensure that all public IPv4 and IPv6 addresses associated with the target infrastructure were fully mapped[cite: 2]. This resulted in an accurate inventory of public IP addresses, which was successfully leveraged to direct subsequent active scanning phases across all resolved endpoints[cite: 2].

### Shodan & Wayback Machine
COMPANY queried Shodan using the discovered public IP addresses and reviewed historical snapshots on the Wayback Machine[cite: 2]. COMPANY used these passive intelligence platforms to identify underlying technology stack versions, infrastructure changes, and public exposures without directly interacting with or alerting the target assets[cite: 2]. This resulted in the discovery of valuable software version data that was cross-referenced with known vulnerabilities to plan targeted exploitation vectors[cite: 2].

### Google Dorking
COMPANY executed targeted Google Dorking queries across the target domain[cite: 2]. COMPANY used search operators such as `site:<target> inurl:swagger-ui.html`, `site:<target> intitle:"index of" "api/v1"`, and searches for sensitive keys like `"AIZA"` or `"api_key="` in log and environment files to discover hidden documentation, debugging endpoints, and credential leaks[cite: 2]. This resulted in the identification of unindexed Swagger UI documentation and exposed configuration paths that provided direct insight into undocumented API parameters and functional workflows[cite: 2].

### Trufflehog & GitHub
COMPANY searched public code repositories on GitHub and scanned them using Trufflehog[cite: 2]. COMPANY used this tool to locate inadvertently committed secrets, source code leaks, or organization-specific credentials[cite: 2]. This resulted in the successful identification of exposed developer secrets that could be weaponized to bypass authentication mechanisms or access hidden login portals[cite: 2].

### Subfinder, Assetfinder, & Amass
COMPANY deployed automated subdomain enumeration tools including Subfinder, Assetfinder, and Amass[cite: 2]. COMPANY used these tools to perform multi-source passive discovery of subdomains associated with the target organization[cite: 2]. This resulted in the discovery of hidden staging and development subdomains containing enhanced functionality and ancillary API services that expanded the overall attack surface[cite: 2].

## Active Reconnaissance & Port Scanning

### Nmap
COMPANY utilized Nmap to conduct active network scanning against all in-scope assets[cite: 2]. COMPANY used specific flags to execute a full transmission control protocol (TCP) port range scan (`-p-`) alongside sweeps of the top one thousand user datagram protocol (UDP) ports across both IPv4 and IPv6 endpoints[cite: 2]. This resulted in the identification of open ports, non-standard API services, and exposed administrative management interfaces that warranted deeper inspection[cite: 2].

### FFuF, Dirb, & Katana
COMPANY executed automated unauthenticated directory searches and web crawling using FFuF, Dirb, and Katana[cite: 2]. COMPANY used these tools alongside custom API wordlists from SecLists (located under `/Discovery/Web-Content/api/`) to brute-force directory paths and crawl application logic[cite: 2]. This resulted in the discovery of hidden unauthenticated API paths, exposed debug directories, and administrative entry points that permitted unauthorized functional testing[cite: 2].

### Nikto & Nuclei
COMPANY launched automated web application scanners Nikto and Nuclei against the target API endpoints[cite: 2]. COMPANY used these scanners to perform automated technology stack fingerprinting and scan for known vulnerability signatures[cite: 2]. This resulted in the identification of underlying web framework versions and specific configuration flaws that could be weaponized during subsequent exploitation phases[cite: 2].

### Testssl.sh
COMPANY used `testssl.sh` to evaluate the target's encryption transport configurations[cite: 2]. COMPANY used this tool to analyze supported TLS protocols, cipher suites, and cryptographic settings against strict compliance benchmarks[cite: 2]. This resulted in the identification of specific compliance exceptions—such as non-ephemeral key exchanges and outdated SHA-1 signature schemes—which required the generation of formal security findings per FedRAMP and NIST guidelines[cite: 2].

### Smuggler & Burp Suite Request Smuggler
COMPANY evaluated the target frontend web application proxy and backend API for HTTP request smuggling vulnerabilities[cite: 2]. COMPANY used the automated Smuggler script and the Burp Suite Request Smuggler extension to test for inconsistent processing of `Content-Length` and `Transfer-Encoding` headers[cite: 2]. Furthermore, COMPANY performed manual testing by submitting chunked probe payloads with modified header combinations and disabled auto-update settings in Burp Repeater[cite: 2]. This resulted in confirming whether the frontend proxy and backend server processed conflicting length headers inconsistently, successfully identifying timeout behaviors and potential desynchronization vectors[cite: 2].

## Authenticated Testing & Vulnerability Analysis

### Curl & Parameter Manipulation (BOLA/IDOR)
COMPANY conducted authenticated testing using command-line `curl` requests and Burp Suite to evaluate access control enforcement[cite: 2]. COMPANY used these requests to test for Broken Object Level Authorization (BOLA) and Insecure Direct Object Reference (IDOR) vulnerabilities by manipulating object identifiers, URL parameters, headers, and request bodies[cite: 2]. This resulted in testing whether lower-privileged or unassociated user accounts could access, modify, or delete sensitive records belonging to other users, successfully verifying both horizontal and vertical privilege escalation vectors[cite: 2].

### Authentication & Refresh Token Analysis (DPoP)
COMPANY reviewed the application's authentication lifecycle and session management mechanisms[cite: 2]. COMPANY used targeted request analysis to evaluate how authorization tokens were generated and how token renewal processes handled refresh tokens[cite: 2]. This resulted in verifying whether token renewal mechanisms enforced cryptographic proof-of-possession standards such as OAuth 2.0 DPoP (RFC 9449) or if they improperly accepted standalone alphanumeric refresh tokens[cite: 2].

### Param Miner & Mass Assignment
COMPANY investigated Broken Object Property Level Authorization using Burp Suite Param Miner and manual payload manipulation[cite: 2]. COMPANY used Param Miner to automatically discover hidden request parameters and tested user registration and update workflows for mass assignment vulnerabilities by injecting unauthorized properties—such as adding `"role": "admin"` into request bodies[cite: 2]. This resulted in discovering that the application improperly accepted user-supplied administrative roles during registration, allowing lower-privileged accounts to successfully escalate privileges to administrative status and create persistent backdoor accounts[cite: 2].

## Advanced Application Layers & Security Misconfigurations

### InQL Scanner, GraphQL Raider, & Manual Introspection
COMPANY targeted advanced application layers by evaluating GraphQL endpoints where present[cite: 2]. COMPANY used directory scanning to locate hidden endpoints (such as `/graphql`, `/graphiql`, and `/api/graphql`), tested alternative HTTP verbs and URL query parameters, and deployed Burp extensions InQL Scanner and GraphQL Raider[cite: 2]. This resulted in executing manual and automated introspection queries that successfully retrieved the full backend schema, mapped out hidden mutations and types, and identified technology-specific engine vulnerabilities[cite: 2].

### Burp Suite Intruder & Turbo Intruder (Unrestricted Resource Consumption)
COMPANY tested rate-limiting controls and volumetric resource consumption using Burp Suite Intruder and Turbo Intruder[cite: 2]. COMPANY used these tools to flood the API with high-volume request bursts and incremental integer wordlists targeting request identifiers[cite: 2]. Additionally, COMPANY executed rate-limit bypass techniques by rotating `X-Forwarded-For` header IP addresses and modifying `User-Agent` values[cite: 2]. This resulted in determining whether excessive requests could exhaust server resources and trigger service unavailability (5xx response codes) or bypass defensive rate-limiting thresholds[cite: 2].

### BFLA, SSRF, & Security Misconfigurations (JWT Tool, CORS, XXE)
COMPANY evaluated complex business logic and security misconfigurations across the application stack[cite: 2]. COMPANY used JWT Tool to inspect token signatures and test for weak secrets or algorithm bypasses, while also testing for Broken Function Level Authorization (BFLA), Unrestricted Access to Sensitive Business Flows, and Server-Side Request Forgery (SSRF) by submitting external URIs[cite: 2]. Furthermore, COMPANY tested file upload functionalities, CORS policies, input validation fuzzing, XML External Entity (XXE) vulnerabilities, Improper Inventory Management (checking for deprecated `/v1/` or `/v2/` paths), and Unsafe Consumption of APIs[cite: 2]. This resulted in a comprehensive review of misconfigurations and third-party integration trust relationships[cite: 2].

### Autorize (FedRAMP Tenant-to-Tenant Testing)
COMPANY evaluated multi-tenant isolation controls for FedRAMP-scoped deployments[cite: 2]. COMPANY used the Burp Suite extension Autorize to automatically compare request sessions across different tenant contexts[cite: 2]. This resulted in verifying whether strict data segmentation and access controls were enforced to prevent cross-tenant data access[cite: 2].

## Post-Testing Procedures

### Token Revocation & Cleanup
The assessment concluded with critical post-testing administrative procedures[cite: 2]. COMPANY executed cleanup actions to manually revoke all active authorization tokens, test user accounts, session tokens, and temporary API credentials generated throughout the engagement[cite: 2]. This resulted in successfully restoring the client's target environment and backend systems back to their original, pristine operational state without leaving residual testing artifacts[cite: 2].
