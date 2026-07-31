# Introduction to API Attacks

* * *

Application Programming Interfaces (APIs) are foundational to modern software development, with web APIs being the most prevalent form. They enable seamless communication and data exchange across diverse systems over the internet, serving as crucial bridges that facilitate integration and collaboration among different software applications.

At their essence, APIs consist of defined rules and protocols that dictate how disparate systems interact. They specify data formatting requirements, delineate access methods for resources, and define expected response structures. APIs are broadly categorized as either public, accessible to external parties, or private, restricted to specific organizations or groups of systems.

## API Building Styles

Web APIs can be built using various architectural styles, including `REST`, `SOAP`, `GraphQL`, and `gRPC`, each with its own strengths and use cases:

- [Representational State Transfer](https://ics.uci.edu/~fielding/pubs/dissertation/top.htm) ( `REST`) is the most popular API style. It uses a `client-server` model where clients make requests to resources on a server using standard HTTP methods ( `GET`, `POST`, `PUT`, `DELETE`). `RESTful` APIs are stateless, meaning each request contains all necessary information for the server to process it, and responses are typically serialized as JSON or XML.
- [Simple Object Access Protocol](https://www.w3.org/TR/2000/NOTE-SOAP-20000508/) ( `SOAP`) uses XML for message exchange between systems. `SOAP` APIs are highly standardized and offer comprehensive features for security, transactions, and error handling, but they are generally more complex to implement and use than `RESTful` APIs.
- [GraphQL](https://graphql.org/) is an alternative style that provides a more flexible and efficient way to fetch and update data. Instead of returning a fixed set of fields for each resource, `GraphQL` allows clients to specify exactly what data they need, reducing over-fetching and under-fetching of data. `GraphQL` APIs use a single endpoint and a strongly-typed query language to retrieve data.
- [gRPC](https://grpc.io/) is a newer style that uses [Protocol Buffers](https://protobuf.dev/) for message serialization, providing a high-performance, efficient way to communicate between systems. `gRPC` APIs can be developed in a variety of programming languages and are particularly useful for microservices and distributed systems.

In this module, our focus will be on attacks against a [RESTful web API](https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html). However, the vulnerabilities demonstrated may also exist in APIs built using other architectural styles.

# API Attacks

Due to their versatility and ubiquitousness, APIs are a double-edged sword. Regardless that they are a critical component of modern software architecture, they also present a broad attack surface. The very nature of APIs, facilitating data exchange and communication between diverse systems, introduces vulnerabilities, such as `Exposure of Sensitive Data`, `Authentication and Authorization Issues`, `Insufficient Rate Limiting`, `Improper Error Handling`, and various other security misconfigurations.

## OWASP Top 10 API Security Risks

To categorize and standardize the security vulnerabilities and misconfigurations that APIs can face, [OWASP](https://owasp.org/) has curated the [OWASP API Security Top 10](https://owasp.org/API-Security/editions/2023/en/0x11-t10/), a comprehensive list of the most critical security risks specifically related to APIs:

| **Risk** | **Description** |
| --- | --- |
| [API1:2023 - Broken Object Level Authorization](https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization/) | The API allows authenticated users to access data they are not authorized to view. |
| [API2:2023 - Broken Authentication](https://owasp.org/API-Security/editions/2023/en/0xa2-broken-authentication/) | The authentication mechanisms of the API can be bypassed or circumvented, allowing unauthorized access. |
| [API3:2023 - Broken Object Property Level Authorization](https://owasp.org/API-Security/editions/2023/en/0xa3-broken-object-property-level-authorization/) | The API reveals sensitive data to authorized users that they should not access or permits them to manipulate sensitive properties. |
| [API4:2023 - Unrestricted Resource Consumption](https://owasp.org/API-Security/editions/2023/en/0xa4-unrestricted-resource-consumption/) | The API does not limit the amount of resources users can consume. |
| [API5:2023 - Broken Function Level Authorization](https://owasp.org/API-Security/editions/2023/en/0xa5-broken-function-level-authorization/) | The API allows unauthorized users to perform authorized operations. |
| [API6:2023 - Unrestricted Access to Sensitive Business Flows](https://owasp.org/API-Security/editions/2023/en/0xa6-unrestricted-access-to-sensitive-business-flows/) | The API exposes sensitive business flows, leading to potential financial losses and other damages. |
| [API7:2023 - Server Side Request Forgery](https://owasp.org/API-Security/editions/2023/en/0xa7-server-side-request-forgery/) | The API does not validate requests adequately, allowing attackers to send malicious requests and interact with internal resources. |
| [API8:2023 - Security Misconfiguration](https://owasp.org/API-Security/editions/2023/en/0xa8-security-misconfiguration/) | The API suffers from security misconfigurations, including vulnerabilities that lead to Injection Attacks. |
| [API9:2023 - Improper Inventory Management](https://owasp.org/API-Security/editions/2023/en/0xa9-improper-inventory-management/) | The API does not properly and securely manage version inventory. |
| [API10:2023 - Unsafe Consumption of APIs](https://owasp.org/API-Security/editions/2023/en/0xaa-unsafe-consumption-of-apis/) | The API consumes another API unsafely, leading to potential security risks. |

This module will focus on exploiting all these security risks and understanding how to prevent them.


# Introduction to Lab

* * *

As we progress through the module, we will practice identifying and exploiting each of the OWASP API Top 10 Security Risks using a `RESTful` web API to fully understand these vulnerabilities.

## Inlanefreight E-Commerce Marketplace

Our loyal customer, Inlanefreight, has ventured into the world of e-commerce marketplaces with `Inlanefreight E-Commerce Marketplace`. The marketplace's business model enables customers to browse and purchase products offered by suppliers. Each supplier is associated with a specific company. The marketplace generates revenue by charging a fee for each product a customer purchases from a supplier.

To operate the marketplace and facilitate transactions between customers and suppliers, Inlanefreight has developed a multi-tenant web API that employs `Role-based Access Control` ( `RBAC`) as its access control policy. Throughout the sections, we will interact with the API using different users with varying roles. Credentials associated with the `pentestercompany.com` domain represent supplier accounts, while those with `hackthebox.com` are identified as customer accounts.

For each user that we authenticate, they will have pre-assigned roles determined by the admin of `Inlanefreight E-Commerce Marketplace`. The admin has adopted a straightforward naming convention for roles: the roles share the same name as the endpoints to which they provide access to. For example, if a user has the role `Suppliers_GetAll`, it implies that the user is authorized to interact with the endpoint that retrieves all supplier records (which, in this case, is `/api/v1/suppliers`).

Our objective is to report any vulnerabilities found to the admin of `Inlanefreight E-Commerce Marketplace`. A detailed report of all discovered vulnerabilities will assist the admin in taking appropriate actions to secure the API. Each vulnerability will be mapped to its relevant [CWE](https://cwe.mitre.org/data/index.html) weakness.

### Swagger API User Interface

Despite the frontend of `Inlanefreight E-Commerce Marketplace` still being in active development, the web API can be accessed via a [Swagger](https://swagger.io/tools/swagger-ui/) UI at the `/swagger` path (make sure to include it after the port of the spawned target machine). We will use this interface throughout the module to explore and assess the security of the marketplace's API, which includes over 60 endpoints:

![Introduction_to_Lab_Image_2](https://academy.hackthebox.com/storage/modules/268/02_Introduction_to_Lab_Image_2.png)

The key entities that the marketplace encompasses include `Customers`, `Products`, `Supplier-Companies`, and `Suppliers`. We will also interact with other entities as we progress through the sections.


# Broken Object Level Authorization

* * *

Web APIs allow users to request data or records by sending various parameters, including unique identifiers such as `Universally Unique Identifiers` ( `UUIDs`), also known as `Globally Unique Identifiers` ( `GUIDs`), and integer IDs. However, failing to properly and securely verify that a user has ownership and permission to view a specific resource through `object-level authorization mechanisms` can lead to data exposure and security vulnerabilities.

A web API endpoint is vulnerable to `Broken Object Level Authorization` ( `BOLA`), also known as `Insecure Direct Object Reference` ( `IDOR`), if its authorization checks (implemented at the source-code level) fail to correctly ensure that an authenticated user has sufficient permissions or privileges to request and view specific data or perform certain operations.

## Authorization Bypass Through User-Controlled Key

The endpoint we will be practicing against is vulnerable to [CWE-639: Authorization Bypass Through User-Controlled Key](https://cwe.mitre.org/data/definitions/639.html).

### Scenario

The admin of `Inlanefreight E-Commerce Marketplace` has provided us with the credentials `[email protected]:HTBPentester1`, wanting us to assess what API vulnerabilities the user can exploit with their assigned roles.

Because the account belongs to a Supplier, we will utilize the `/api/v1/authentication/suppliers/sign-in` endpoint to sign in and obtain a JWT:

![Authenitcation_Suppliers.gif](https://academy.hackthebox.com/storage/modules/268/Authenitcation_Suppliers.gif)

To authenticate using the JWT, we will copy it from the response and click the `Authorize` button. Note the lock icon, currently unlocked, indicating our non-authenticated status. Next, we will paste the JWT into the `Value` text field within the `Available authorizations` popup and click `Authorize`. Upon completion, the lock icon will be fully locked, confirming our authentication:

![Authentication_Suppliers_2.gif](https://academy.hackthebox.com/storage/modules/268/Authentication_Suppliers_2.gif)

When examining the endpoints within the Suppliers group (notice how they have a lock at their right-most side, indicating that authentication is required), we will notice one named `/api/v1/suppliers/current-user`:

![API1_2023_Broken_Object_Level_Authorization_Image_5](https://academy.hackthebox.com/storage/modules/268/API1_2023_Broken_Object_Level_Authorization_Image_5.png)

Endpoints containing `current-user` in their path indicate that they utilize the JWT of the currently authenticated user to perform the specified operation, which in this case is retrieving the current user's data. Upon invoking the endpoint, we will retrieve our current user's company `ID`, `b75a7c76-e149-4ca7-9c55-d9fc4ffa87be`, a `Guid` value:

![API1_2023_Broken_Object_Level_Authorization_Image_6](https://academy.hackthebox.com/storage/modules/268/API1_2023_Broken_Object_Level_Authorization_Image_6.png)

Let us then retrieve our current user's roles. After invoking the `/api/v1/roles/current-user` endpoint, it responds with the role `SupplierCompanies_GetYearlyReportByID`:

![API1_2023_Broken_Object_Level_Authorization_Image_7](https://academy.hackthebox.com/storage/modules/268/API1_2023_Broken_Object_Level_Authorization_Image_7.png)

In the `Supplier-Companies` group, we find an endpoint related to the role `SupplierCompanies_GetYearlyReportByID` that accepts a GET parameter: `/api/v1/supplier-companies/yearly-reports/{ID}`:

![API1_2023_Broken_Object_Level_Authorization_Image_8](https://academy.hackthebox.com/storage/modules/268/API1_2023_Broken_Object_Level_Authorization_Image_8.png)

When expanding it, we will notice that it requires the `SupplierCompanies_GetYearlyReportByID` role and accepts the `ID` parameter as an integer and not a `Guid`:

![API1_2023_Broken_Object_Level_Authorization_Image_9](https://academy.hackthebox.com/storage/modules/268/API1_2023_Broken_Object_Level_Authorization_Image_9.png)

If we use `1` as the `ID`, we will receive a yearly-report belonging to a company with the ID `f9e58492-b594-4d82-a4de-16e4f230fce1`, which is not the one we belong to, `b75a7c76-e149-4ca7-9c55-d9fc4ffa87be`:

![API1_2023_Broken_Object_Level_Authorization_Image_10](https://academy.hackthebox.com/storage/modules/268/API1_2023_Broken_Object_Level_Authorization_Image_10.png)

When trying other IDs, we still can access yearly reports of other supplier-companies, allowing us to access potentially sensitive business data:

![API1_2023_Broken_Object_Level_Authorization_Image_11](https://academy.hackthebox.com/storage/modules/268/API1_2023_Broken_Object_Level_Authorization_Image_11.png)

Additionally, we can mass abuse the `BOLA` vulnerability and fetch the first 20 yearly reports of supplier-companies:

![BOLA_Mass_Abuse.gif](https://academy.hackthebox.com/storage/modules/268/BOLA_Mass_Abuse.gif)

The only changes we need to make to the copied cURL command from the `Swagger` interface are using a Bash `for-loop` with `variable interpolation`, adding a new line after each response using the flag `-w "\n"`, silencing progress using the flag `-s`, and piping the output to [jq](https://jqlang.github.io/jq/):

```shell
for ((i=1; i<= 20; i++)); do
curl -s -w "\n" -X 'GET' \
  'http://94.237.49.212:43104/api/v1/supplier-companies/yearly-reports/'$i'' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJodHRwOi8vc2NoZW1hcy54bWxzb2FwLm9yZy93cy8yMDA1LzA1L2lkZW50aXR5L2NsYWltcy9uYW1laWRlbnRpZmllciI6Imh0YnBlbnRlc3RlcjFAcGVudGVzdGVyY29tcGFueS5jb20iLCJodHRwOi8vc2NoZW1hcy5taWNyb3NvZnQuY29tL3dzLzIwMDgvMDYvaWRlbnRpdHkvY2xhaW1zL3JvbGUiOiJTdXBwbGllckNvbXBhbmllc19HZXRZZWFybHlSZXBvcnRCeUlEIiwiZXhwIjoxNzIwMTg1NzAwLCJpc3MiOiJodHRwOi8vYXBpLmlubGFuZWZyZWlnaHQuaHRiIiwiYXVkIjoiaHR0cDovL2FwaS5pbmxhbmVmcmVpZ2h0Lmh0YiJ9.D6E5gJ-HzeLZLSXeIC4v5iynZetx7f-bpWu8iE_pUODlpoWdYKniY9agU2qRYyf6tAGdTcyqLFKt1tOhpOsWlw' | jq
done

{
  "supplierCompanyYearlyReport": {
    "id": 1,
    "companyID": "f9e58492-b594-4d82-a4de-16e4f230fce1",
    "year": 2020,
    "revenue": 794425112,
    "commentsFromCLevel": "Superb work! The Board is over the moon! All employees will enjoy a dream vacation!"
  }
}
{
  "supplierCompanyYearlyReport": {
    "id": 2,
    "companyID": "f9e58492-b594-4d82-a4de-16e4f230fce1",
    "year": 2022,
    "revenue": 339322952,
    "commentsFromCLevel": "Excellent performance! The Board is exhilarated! Prepare for a special vacation adventure!"
  }
}
{
  "supplierCompanyYearlyReport": {
    "id": 3,
    "companyID": "058ac1e5-3807-47f3-b546-cc069366f8f9",
    "year": 2020,
    "revenue": 186208503,
    "commentsFromCLevel": "Phenomenal performance! The Board is deeply impressed! Everyone will be treated to a deluxe vacation!"
  }
}

<SNIP>

```

### Prevention

To mitigate the `BOLA` vulnerability, the endpoint `/api/v1/supplier-companies/yearly-reports` should implement a verification step (at the source code level) to ensure that authorized users can only access yearly reports associated with their affiliated company. This verification involves comparing the `companyID` field of the report with the authenticated supplier's `companyID`. Access should be granted only if these values match; otherwise, the request should be denied. This approach effectively maintains data segregation between supplier-companies' yearly reports.


# Broken Authentication

* * *

[Authentication](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html) is a fundamental pillar of web API security. Web APIs utilize various authentication mechanisms to ensure data confidentiality. An API suffers from `Broken Authentication` if any of its authentication mechanisms can be bypassed or circumvented.

## Improper Restriction of Excessive Authentication Attempts

The endpoint we will be practicing against is vulnerable to [CWE-307: Improper Restriction of Excessive Authentication Attempts](https://cwe.mitre.org/data/definitions/307.html).

### Scenario

The admin of `Inlanefreight E-Commerce Marketplace` has provided us with the credentials `[email protected]:HTBPentester3`, wanting us to assess what API vulnerabilities can the user exploit with their assigned roles.

Because the account belongs to a customer, we will utilize the `/api/v1/authentication/customers/sign-in` endpoint to obtain a JWT and then authenticate with it:

![API2_2023_Broken_Authentication_Image_1.png](https://academy.hackthebox.com/storage/modules/268/API2_2023_Broken_Authentication_Image_1.png)

When invoking the `/api/v1/customers/current-user` endpoint, we get back the information of our currently authenticated user:

![API2_2023_Broken_Authentication_Image_2.png](https://academy.hackthebox.com/storage/modules/268/API2_2023_Broken_Authentication_Image_2.png)

The `/api/v1/roles/current-user` endpoint reveals that the user is assigned three roles: `Customers_UpdateByCurrentUser`, `Customers_Get`, and `Customers_GetAll`:

![API2_2023_Broken_Authentication_Image_3.png](https://academy.hackthebox.com/storage/modules/268/API2_2023_Broken_Authentication_Image_3.png)

`Customers_GetAll` allows us to use the `/api/v1/customers` endpoint, which returns the records of all customers:

![API2_2023_Broken_Authentication_Image_4.png](https://academy.hackthebox.com/storage/modules/268/API2_2023_Broken_Authentication_Image_4.png)

Although the endpoint suffers from `Broken Object Property Level Authorization` (which we will cover in the upcoming section) because it exposes sensitive information about other customers, such as `email`, `phoneNumber`, and `birthDate`, it does not directly allow us to hijack any other account.

When we expand the `/api/v1/customers/current-user` `PATCH` endpoint, we discover that it allows us to update our information fields, including the account's password:

![API2_2023_Broken_Authentication_Image_5.png](https://academy.hackthebox.com/storage/modules/268/API2_2023_Broken_Authentication_Image_5.png)

If we provide a weak password such as 'pass,' the API rejects the update, stating that passwords must be at least six characters long:

![API2_2023_Broken_Authentication_Image_6.png](https://academy.hackthebox.com/storage/modules/268/API2_2023_Broken_Authentication_Image_6.png)

The validation message provides valuable information, exposing that the API uses a weak password policy, which does not enforce cryptographically secure passwords. If we try setting the password to '123456', we will notice the API now returns `true` for the success status, indicating that it performed the update:

![API2_2023_Broken_Authentication_Image_7.png](https://academy.hackthebox.com/storage/modules/268/API2_2023_Broken_Authentication_Image_7.png)

Given that the API uses a weak password policy, other customer accounts could have used cryptographically insecure passwords when registering. Therefore, we will perform password brute-forcing against customers using `ffuf`.

First, we need to obtain the (fail) message that the `/api/v1/authentication/customers/sign-in` endpoint returns when provided with incorrect credentials, which in this case is 'Invalid Credentials':

![API2_2023_Broken_Authentication_Image_8.png](https://academy.hackthebox.com/storage/modules/268/API2_2023_Broken_Authentication_Image_8.png)

Instead of attacking all 107 customers, the admin of `Inlanefreight E-Commerce Marketplace` has provided us with the emails of three high-value targets (which we need to save in a file):

- `[email protected]`
- `[email protected]`
- `[email protected]`

For the password wordlist, we will use [xato-net-10-million-passwords-10000](https://github.com/danielmiessler/SecLists/blob/master/Passwords/xato-net-10-million-passwords-10000.txt) from [SecLists](https://github.com/danielmiessler/SecLists/tree/master).

Because we are fuzzing two parameters at the same time (which are the email and password), we need to use the `-w` flag of `ffuf` and assign the keywords `EMAIL` and `PASS` to the customer emails and passwords wordlists, respectively. Once `ffuf` finishes, we will discover that the password of `[email protected]` is `qwerasdfzxcv`:

```shell
ffuf -w /opt/useful/seclists/Passwords/xato-net-10-million-passwords-10000.txt:PASS -w customerEmails.txt:EMAIL -u http://94.237.59.63:31874/api/v1/authentication/customers/sign-in -X POST -H "Content-Type: application/json" -d '{"Email": "EMAIL", "Password": "PASS"}' -fr "Invalid Credentials" -t 100

        /'___\  /'___\           /'___\
       /\ \__/ /\ \__/  __  __  /\ \__/
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/
         \ \_\   \ \_\  \ \____/  \ \_\
          \/_/    \/_/   \/___/    \/_/

       v2.1.0-dev
________________________________________________

 :: Method           : POST
 :: URL              : http://94.237.59.63:31874/api/v1/authentication/customers/sign-in
 :: Wordlist         : PASS: /opt/useful/seclists/Passwords/xato-net-10-million-passwords-10000.txt
 :: Wordlist         : EMAIL: /home/htb-ac-413848/customerEmails.txt
 :: Header           : Content-Type: application/json
 :: Data             : {"Email": "EMAIL", "Password": "PASS"}
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 100
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
 :: Filter           : Regexp: Invalid Credentials
________________________________________________

[Status: 200, Size: 393, Words: 1, Lines: 1, Duration: 81ms]
    * EMAIL: [email protected]
    * PASS: qwerasdfzxcv

:: Progress: [30000/30000] :: Job [1/1] :: 1275 req/sec :: Duration: [0:00:24] :: Errors: 0 ::

```

Now that we have brute-forced the password, we can use the `/api/v1/authentication/customers/sign-in` endpoint with the credentials `[email protected]:qwerasdfzxcv` to obtain a JWT as `Isabella` and view all her confidential information on `Inlanefreight E-Commerce Marketplace`.

### Brute-forcing OTPs and Answers of Security Questions

Applications allow users to reset their passwords by requesting a `One Time Password` ( `OTP`) sent to a device they own or answering a security question they have chosen during registration. If brute-forcing passwords is infeasible due to strong password policies, we can attempt to brute-force OTPs or answers to security questions, given that they have low entropy or can be guessed (in addition to rate-limiting not being implemented).

### Prevention

To mitigate the `Broken Authentication` vulnerability, the `/api/v1/authentication/customers/sign-in` endpoint should implement rate-limiting to prevent brute-force attacks. This can be achieved by limiting the number of login attempts from a single IP address or user account within a specified time frame.

Moreover, the web API should enforce a robust password policy for user credentials (including customers and suppliers) during both registration and updates, allowing only cryptographically secure passwords. This policy should include:

1. `Minimum password length` (e.g., at least 12 characters)
2. `Complexity requirements` (e.g., a mix of uppercase and lowercase letters, numbers, and special characters)
3. `Prohibition of commonly used or easily guessable passwords` (such as ones found in leaked password databases)
4. `Enforcement of password history to prevent reuse of recent passwords`
5. `Regular password expiration and mandatory changes`

Additionally, the web API endpoint should implement multi-factor authentication ( `MFA`) for added security, requesting an `OTP` before fully authenticating users.


# Broken Object Property Level Authorization

* * *

`Broken Object Property Level Authorization` is a category of vulnerabilities that encompasses two subclasses: `Excessive Data Exposure` and `Mass Assignment`.

An API endpoint is vulnerable to `Excessive Data Exposure` if it reveals sensitive data to authorized users that they are not supposed to access.

On the other hand, an API endpoint is vulnerable to `Mass Assignment` if it permits authorized users to manipulate sensitive object properties beyond their authorized scope, including modifying, adding, or deleting values.

## Exposure of Sensitive Information Due to Incompatible Policies

The first endpoint we will be practicing against is vulnerable to [CWE-213](https://cwe.mitre.org/data/definitions/213.html), `Exposure of Sensitive Information Due to Incompatible Policies`.

### Scenario

The admin of `Inlanefreight E-Commerce Marketplace` has provided us with the credentials `[email protected]:HTBPentester4`, wanting us to assess what API vulnerabilities the user can exploit with their assigned roles.

After invoking `/api/v1/authentication/customers/sign-in` to sign in as a customer and obtain a JWT, the `/api/v1/roles/current-user` endpoint shows that we have the roles `Suppliers_Get` and `Suppliers_GetAll`:

![API3_2023_Broken_Object_Property_Level_Authorization_Image_1](https://academy.hackthebox.com/storage/modules/268/API3_2023_Broken_Object_Property_Level_Authorization_Image_1.png)

It is typical for e-commerce marketplaces to allow customers to view supplier details. However, after invoking the `/api/v1/suppliers` `GET` endpoint, we notice that the response includes not only the `id`, `companyID`, and `name` fields but also the `email` and `phoneNumber` fields of the suppliers:

![API3_2023_Broken_Object_Property_Level_Authorization_Image_2](https://academy.hackthebox.com/storage/modules/268/API3_2023_Broken_Object_Property_Level_Authorization_Image_2.png)

These sensitive fields should not be exposed to customers, as this allows them to circumvent the marketplace entirely and contact suppliers directly to purchase goods (at a discounted price). Additionally, this vulnerability benefits suppliers financially by enabling them to generate greater revenues without paying the marketplace fee. However, for the stakeholders of `Inlanefreight E-Commerce Marketplace`, this will negatively impact their revenues.

### Prevention

To mitigate the `Excessive Data Exposure` vulnerability, the `/api/v1/suppliers` endpoint should only return fields necessary from the customers' perspective. This can be achieved by returning a specific response [Data Transfer Object (DTO)](https://en.wikipedia.org/wiki/Data_transfer_object) that includes only the fields intended for customer visibility, rather than exposing the entire domain model used for database interaction.

## Improperly Controlled Modification of Dynamically-Determined Object Attributes

The second API endpoint we will be practicing against is vulnerable to [CWE-915](https://cwe.mitre.org/data/definitions/915.html), `Improperly Controlled Modification of Dynamically-Determined Object Attributes`.

### Scenario

The admin of `Inlanefreight E-Commerce Marketplace` has provided us with the credentials `[email protected]:HTBPentester6`, wanting us to assess what API vulnerabilities the user can exploit with their assigned roles.

After invoking `/api/v1/authentication/suppliers/sign-in` to sign in as a Supplier and obtain a JWT, the `/api/v1/roles/current-user` endpoint shows that we have the roles `SupplierCompanies_Update` and `SupplierCompanies_Get`:

![API3_2023_Broken_Object_Property_Level_Authorization_Image_3](https://academy.hackthebox.com/storage/modules/268/API3_2023_Broken_Object_Property_Level_Authorization_Image_3.png)

The `/api/v1/supplier-companies/current-user` endpoint shows that the supplier-company the currently authenticated supplier belongs to, 'PentesterCompany', has the `isExemptedFromMarketplaceFee` field set to `0`, which equates to `false`:

![API3_2023_Broken_Object_Property_Level_Authorization_Image_4](https://academy.hackthebox.com/storage/modules/268/API3_2023_Broken_Object_Property_Level_Authorization_Image_4.png)

Therefore, this implies that `Inlanefreight E-Commerce Marketplace` will charge 'PentesterCompany' a marketplace fee for each product they sell.

When expanding the `/api/v1/supplier-companies` `PATCH` endpoint, we notice that it requires the `SupplierCompanies_Update` role, states that the supplier performing the update must be a staff member, and allows sending a value for the `isExemptedFromMarketplaceFee` field:

![API3_2023_Broken_Object_Property_Level_Authorization_Image_5](https://academy.hackthebox.com/storage/modules/268/API3_2023_Broken_Object_Property_Level_Authorization_Image_5.png)

Let us set it to `1`, such that 'PentesterCompany' does not get included in the companies required to pay the marketplace fee; after invoking it, the endpoint returns a success message:

![API3_2023_Broken_Object_Property_Level_Authorization_Image_6](https://academy.hackthebox.com/storage/modules/268/API3_2023_Broken_Object_Property_Level_Authorization_Image_6.png)

Then, when checking our company info again using `/api/v1/supplier-companies/current-user`, we will notice that the `isExemptedFromMarketplaceFee` field has become `1`:

![API3_2023_Broken_Object_Property_Level_Authorization_Image_7](https://academy.hackthebox.com/storage/modules/268/API3_2023_Broken_Object_Property_Level_Authorization_Image_7.png)

Because the endpoint mistakenly allows suppliers to update the value of a field that they should not have access to, this vulnerability allows supplier-companies to generate more revenue from all sales performed over the `Inlanefreight E-Commerce Marketplace`, as they will not be charged a marketplace fee. However, similar to the repercussions of the previous `Exposure of Sensitive Information Due to Incompatible Policies` vulnerability, the revenues of the stakeholders of `Inlanefreight E-Commerce Marketplace` will be negatively impacted.

### Prevention

To mitigate the `Mass Assignment` vulnerability, the `/api/v1/supplier-companies` `PATCH` endpoint should restrict invokers from updating sensitive fields. Similar to addressing `Excessive Data Exposure`, this can be achieved by implementing a dedicated request `DTO` that includes only the fields intended for suppliers to modify.


# Unrestricted Resource Consumption

* * *

File upload and download are fundamental features in all applications. For instance, in e-commerce marketplaces, suppliers require the ability to upload product images, while users need to view and download these files.

A web API is vulnerable to `Unrestricted Resource Consumption` if it fails to limit user-initiated requests that consume resources such as `network bandwidth`, `CPU`, `memory`, and `storage`. These resources incur significant costs, and without adequate safeguards—particularly effective `rate-limiting`—against excessive usage, users can exploit these vulnerabilities and cause financial damage.

## Uncontrolled Resource Consumption

The endpoint we will be practicing against is vulnerable to [CWE-400: Uncontrolled Resource Consumption](https://cwe.mitre.org/data/definitions/400.html).

### Scenario

The admin of `Inlanefreight E-Commerce Marketplace` has provided us with the credentials `[email protected]:HTBPentester8`, wanting us to assess what API vulnerabilities the user can exploit with their assigned roles.

After invoking `/api/v1/authentication/suppliers/sign-in` to sign in as a supplier and obtain a JWT, the `/api/v1/roles/current-user` endpoint shows that we have the roles `SupplierCompanies_Get` and `SupplierCompanies_UploadCertificateOfIncorporation`:

![API4_2023_Unrestricted_Resource_Consumption_Image_1.png](https://academy.hackthebox.com/storage/modules/268/API4_2023_Unrestricted_Resource_Consumption_Image_1.png)

Checking the Supplier-Companies group, we notice only one endpoint related to the second role: the `/api/v1/supplier-companies/certificates-of-incorporation` `POST` endpoint. When expanding it, we see that it requires the `SupplierCompanies_UploadCertificateOfIncorporation` role and allows the staff of a supplier company to upload its certificate of incorporation as a PDF file, storing it on disk indefinitely:

![API4_2023_Unrestricted_Resource_Consumption_Image_3.png](https://academy.hackthebox.com/storage/modules/268/API4_2023_Unrestricted_Resource_Consumption_Image_3.png)

Let us attempt to upload a large PDF file containing random bytes. First, we will use `/api/v1/supplier-companies/current-user` to get the supplier-company ID of the currently authenticated user, `b75a7c76-e149-4ca7-9c55-d9fc4ffa87be`:

![API4_2023_Unrestricted_Resource_Consumption_Image_2.png](https://academy.hackthebox.com/storage/modules/268/API4_2023_Unrestricted_Resource_Consumption_Image_2.png)

Next, we will use [dd](https://man7.org/linux/man-pages/man1/dd.1.html) to create a file containing 30 random megabytes and assign it the `.pdf` extension:

```shell
dd if=/dev/urandom of=certificateOfIncorporation.pdf bs=1M count=30

30+0 records in
30+0 records out
31457280 bytes (31 MB, 30 MiB) copied, 0.139503 s, 225 MB/s

```

Then, within the `/api/v1/supplier-companies/certificates-of-incorporation` `POST` endpoint, we will click on the 'Choose File' button and upload the file:

![API4_2023_Unrestricted_Resource_Consumption_Image_4.png](https://academy.hackthebox.com/storage/modules/268/API4_2023_Unrestricted_Resource_Consumption_Image_4.png)

After invoking the endpoint, we notice that the API returns a successful upload message, along with the size of the uploaded file:

![API4_2023_Unrestricted_Resource_Consumption_Image_5.png](https://academy.hackthebox.com/storage/modules/268/API4_2023_Unrestricted_Resource_Consumption_Image_5.png)

Because the endpoint does not validate whether the file size is within a specified range, the backend will save files of any size to disk. Additionally, if the endpoint does not implement rate-limiting, we can attempt to cause a denial-of-service by sending the file upload request repeatedly, consuming all available disk storage. Exploiting this vulnerability to consume all the disk storage of the marketplace will result in financial losses for the stakeholders of `Inlanefreight E-Commerce Marketplace`.

Additionally, we need to test whether the endpoint allows uploading files other than PDF files. Let us use `dd` again to generate a file with the `.exe` extension, filling it with random bytes:

```shell
dd if=/dev/urandom of=reverse-shell.exe bs=1M count=10

10+0 records in
10+0 records out
10485760 bytes (10 MB, 10 MiB) copied, 0.0398348 s, 263 MB/s

```

Within the `/api/v1/supplier-companies/certificates-of-incorporation` `POST` endpoint, we will click on the 'Choose File' button and upload the file:

![API4_2023_Unrestricted_Resource_Consumption_Image_7.png](https://academy.hackthebox.com/storage/modules/268/API4_2023_Unrestricted_Resource_Consumption_Image_7.png)

After invoking the endpoint, we notice that the API returns a successful upload message, indicating that the endpoint does not validate the file extension (additionally, notice how the files are stored within `wwwroot/SupplierCompaniesCertificatesOfIncorporations`):

![API4_2023_Unrestricted_Resource_Consumption_Image_8.png](https://academy.hackthebox.com/storage/modules/268/API4_2023_Unrestricted_Resource_Consumption_Image_8.png)

If we manage to social engineer a system administrator of `Inlanefreight E-Commerce Marketplace` to open the file, the executable will run, potentially granting us a reverse shell (assuming we had used an actual reverse shell executable, such as those generated by `msfvenom`).

### Abusing Default Behaviors

After each request to upload files, we noticed that the file URI points to `wwwroot/SupplierCompaniesCertificatesOfIncorporations`, which is within the `wwwroot` directory.

The admin of `Inlanefreight E-Commerce Marketplace` has informed us that the web API is developed using [ASP.NET Core](https://dotnet.microsoft.com/en-us/apps/aspnet). By default, static files in the `wwwroot` directory are [publicly accessible](https://learn.microsoft.com/en-us/aspnet/core/fundamentals/static-files?view=aspnetcore-8.0#security-considerations-for-static-files). Let us try to download the previously uploaded `exe` file:

```shell
curl -O http://94.237.51.179:51135/SupplierCompaniesCertificatesOfIncorporations/reverse-shell.exe

  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 10.0M  100 10.0M    0     0  11.4M      0 --:--:-- --:--:-- --:--:-- 11.4M

```

If we can enumerate file names within the `SupplierCompaniesCertificatesOfIncorporations` directory (and other directories within `wwwroot`), we could potentially access sensitive information about other customers of `Inlanefreight E-Commerce Marketplace`. Additionally, we could utilize the web API as cloud storage for malware that could be distributed to victims.

### Prevention

To mitigate the `Unrestricted Resource Consumption` vulnerability, the `/api/v1/supplier-companies/certificates-of-incorporation` `POST` endpoint should implement thorough validation mechanisms for both the size, extension and content of uploaded files. Validating the size of files prevents excessive consumption of server resources, such as disk space and memory, while ensuring that only authorized and expected file types are uploaded helps prevent potential security risks.

Implementing file size validation ensures that the uploaded files do not exceed specified limits, thereby preventing excessive consumption of server resources. Alternatively, validating file extensions ensures that only authorized file types, such as PDF or specific image formats, are accepted. This prevents malicious uploads of executable files ( `exe`, `bat`, `sh`) or other potentially harmful file types that could compromise server security. Implementing strict file extension validation, coupled with server-side checks, helps enforce security policies and prevents unauthorized access and execution of files.

Integrating antivirus scanning tools like [ClamAV](https://www.clamav.net/) adds a layer of security by scanning file contents for known malware signatures before saving them to disk. This proactive measure helps detect and prevent the uploading of infected files that could potentially compromise server integrity.

Moreover, enforcing robust authentication and authorization mechanisms ensures that only authenticated users with appropriate privileges can upload files and access resources in publicly accessible directories such as `wwwroot`.


# Broken Function Level Authorization

* * *

A web API is vulnerable to `Broken Function Level Authorization` ( `BFLA`) if it allows unauthorized or unprivileged users to interact with and invoke privileged endpoints, granting access to sensitive operations or confidential information. The difference between `BOLA` and `BFLA` is that, in the case of `BOLA`, the user is authorized to interact with the vulnerable endpoint, whereas in the case of `BFLA`, the user is not.

## Exposure of Sensitive Information to an Unauthorized Actor

The endpoint we will be practicing against is vulnerable to [CWE-200: Exposure of Sensitive Information to an Unauthorized Actor](https://cwe.mitre.org/data/definitions/200.html).

### Scenario

The admin of `Inlanefreight E-Commerce Marketplace` has provided us with the credentials `[email protected]:HTBPentester9`, wanting us to assess what API vulnerabilities the user can exploit with their assigned roles.

After invoking `/api/v1/authentication/customer/sign-in` to sign in as a customer and obtain a JWT, we need to hunt for endpoints that require authorization but allow unauthorized users to interact with them. One interesting endpoint under the Products group, `/api/v1/products/discounts`, seems to retrieve all product discounts, however, it requires authenticated users to have the `ProductDiscounts_GetAll` role:

![API5_2023_Broken_Function_Level_Authorization_Image_1](https://academy.hackthebox.com/storage/modules/268/API5_2023_Broken_Function_Level_Authorization_Image_1.png)

After checking our roles using the `/api/v1/roles/current-user` endpoint, we will discover that the currently authenticated user does not have any assigned:

![API5_2023_Broken_Function_Level_Authorization_Image_2](https://academy.hackthebox.com/storage/modules/268/API5_2023_Broken_Function_Level_Authorization_Image_2.png)

Despite not having any roles, if we attempt to invoke the `/api/v1/products/discounts` endpoint, we notice that it returns data containing all the discounts for products:

![API5_2023_Broken_Function_Level_Authorization_Image_3](https://academy.hackthebox.com/storage/modules/268/API5_2023_Broken_Function_Level_Authorization_Image_3.png)

Although the web API developers intended that only authorized users with the `ProductDiscounts_GetAll` role could access this endpoint, they did not implement the role-based access control check.

### Prevention

To mitigate the `BFLA` vulnerability, the `/api/v1/products/discounts` endpoint should enforce an authorization check at the source-code level to ensure that only users with the `ProductDiscounts_GetAll` role can interact with it. This involves verifying the user's roles before processing the request, ensuring that unauthorized users are denied access to the endpoint's functionality.


# Unrestricted Access to Sensitive Business Flows

* * *

All businesses operate to generate revenue; however, if a web API exposes operations or data that allows users to abuse them and undermine the system (for example, by buying goods at a discounted price), it becomes vulnerable to `Unrestricted Access to Sensitive Business Flows`. An API endpoint is vulnerable if it exposes a sensitive business flow without appropriately restricting access to it.

## Scenario

In the previous section, we exploited a `BFLA` vulnerability and gained access to product discount data. This data exposure also leads to `Unrestricted Access to Sensitive Business Flows` because it allows us to know the dates when supplier companies will discount their products and the corresponding discount rates. For example, if we want to buy the product with ID `a923b706-0aaa-49b2-ad8d-21c97ff6fac7`, we should purchase it between `2023-03-15` and `2023-09-15` because it will be 70% off its original price:

![API6_2023_Unrestricted_Access_to_Sensitive_Business_Flows_Image_1](https://academy.hackthebox.com/storage/modules/268/API6_2023_Unrestricted_Access_to_Sensitive_Business_Flows_Image_1.png)

Additionally, if the endpoint responsible for purchasing products does not implement rate-limiting (i.e., it suffers from `Unrestricted Resource Consumption`), we can purchase all available stock on the day the discount starts and resell the products later at their original price or at a higher price after the discount ends.

### Prevention

To mitigate the `Unrestricted Access to Sensitive Business Flows` vulnerability, endpoints exposing critical business operations, such as `/api/v1/products/discounts`, should implement strict access controls to ensure that only authorized users can view or interact with sensitive data.


# Server Side Request Forgery

* * *

A web API is vulnerable to `Server-Side Request Forgery` ( `SSRF`) (also known as `Cross-Site Port Attack` ( `XPSA`)) if it uses user-controlled input to fetch remote or local resources without validation. SSRF flaws occur when an API fetches a remote resource without validating the user-supplied URL. This allows an attacker to coerce the application to send a crafted request to an unexpected destination (especially local ones), bypassing firewalls or VPNs.

## Server-Side Request Forgery (SSRF)

The endpoint we will be practicing against is vulnerable to [CWE-918: Server-Side Request Forgery (SSRF)](https://cwe.mitre.org/data/definitions/918.html).

### Scenario

The admin of `Inlanefreight E-Commerce Marketplace` has provided us with the credentials `[email protected]:HTBPentester10`, wanting us to assess what API vulnerabilities the user can exploit with their assigned roles.

After invoking `/api/v1/authentication/suppliers/sign-in` to sign in as a supplier and obtain a JWT, the `/api/v1/roles/current-user` endpoint shows that we have the roles `SupplierCompanies_Update` and `SupplierCompanies_UploadCertificateOfIncorporation`:

![API7_2023_Server_Side_Request_Forgery_Image_1](https://academy.hackthebox.com/storage/modules/268/API7_2023_Server_Side_Request_Forgery_Image_1.png)

Checking the Supplier-Companies group, we notice that there are three endpoints related to these roles, `/api/v1/supplier-companies`, `/api/v1/supplier-companies/{ID}/certificates-of-incorporation`, and `/api/v1/supplier-companies/certificates-of-incorporation`:

![API7_2023_Server_Side_Request_Forgery_Image_2](https://academy.hackthebox.com/storage/modules/268/API7_2023_Server_Side_Request_Forgery_Image_2.png)

`/api/v1/supplier-companies/current-user` shows that the currently authenticated user belongs to the supplier-company with the ID `b75a7c76-e149-4ca7-9c55-d9fc4ffa87be`:

![API7_2023_Server_Side_Request_Forgery_Image_4](https://academy.hackthebox.com/storage/modules/268/API7_2023_Server_Side_Request_Forgery_Image_4.png)

Expanding the `/api/v1/supplier-companies/certificates-of-incorporation` `POST` endpoint, we notice that it requires the `SupplierCompanies_UploadCertificateOfIncorporation` role and allows the staff of a supplier-company to upload its certificate of incorporation as a PDF file. We will provide any PDF file for the first field and the ID of our supplier-company:

![API7_2023_Server_Side_Request_Forgery_Image_5](https://academy.hackthebox.com/storage/modules/268/API7_2023_Server_Side_Request_Forgery_Image_5.png)

After invoking the endpoint, we will notice that the response contains three fields, with the most interesting being the value of `fileURI`:

![API7_2023_Server_Side_Request_Forgery_Image_6](https://academy.hackthebox.com/storage/modules/268/API7_2023_Server_Side_Request_Forgery_Image_6.png)

The web API stores the path of files using the [file URI Scheme](https://datatracker.ietf.org/doc/html/rfc8089), which is used to represent local file paths and allows access to files on a local filesystem. If we use the `/api/v1/supplier-companies/current-user` endpoint again, we will notice that the value of `certificateOfIncorporationPDFFileURI` now has the file URI of the uploaded file:

![API7_2023_Server_Side_Request_Forgery_Image_7](https://academy.hackthebox.com/storage/modules/268/API7_2023_Server_Side_Request_Forgery_Image_7.png)

Expanding the `/api/v1/supplier-companies` `PATCH` endpoint, we notice that it requires the `SupplierCompanies_Update` role, that the update must be performed by staff belonging to the Supplier-Company, and that it allows modifying the value of the `CertificateOfIncorporationPDFFileURI` field:

![API7_2023_Server_Side_Request_Forgery_Image_3](https://academy.hackthebox.com/storage/modules/268/API7_2023_Server_Side_Request_Forgery_Image_3.png)

Therefore, this endpoint is vulnerable to `Improperly Controlled Modification of Dynamically-Determined Object Attributes`, as the value of this field should only be set by the `/api/v1/supplier-companies/certificates-of-incorporation` `POST` endpoint. Let us perform an SSRF attack and update the `CertificateOfIncorporationPDFFileURI` field to point to the `/etc/passwd` file:

![API7_2023_Server_Side_Request_Forgery_Image_8](https://academy.hackthebox.com/storage/modules/268/API7_2023_Server_Side_Request_Forgery_Image_8.png)

Because the web API's backend does not validate the path that the `CertificateOfIncorporationPDFFileURI` field points to, it will fetch and return the contents of local files, including sensitive ones such as `/etc/passwd`.

Let us invoke the `/api/v1/supplier-companies/{ID}/certificates-of-incorporation` `GET` endpoint to retrieve the contents of the file that `CertificateOfIncorporationPDFFileURI` points to, which is `/etc/passwd`, as base64:

![API7_2023_Server_Side_Request_Forgery_Image_9](https://academy.hackthebox.com/storage/modules/268/API7_2023_Server_Side_Request_Forgery_Image_9.png)

When using [CyberChef](https://gchq.github.io/CyberChef/#recipe=From_Base64('A-Za-z0-9%2B/%3D',true,false)) to decode the value of the `base64Data` field, we obtain the contents of the `/etc/passwd` file from the backend server:

![API7_2023_Server_Side_Request_Forgery_Image_10](https://academy.hackthebox.com/storage/modules/268/API7_2023_Server_Side_Request_Forgery_Image_10.png)

We can further compromise the system by viewing the contents of other critical files, such as `/etc/shadow`.

### Prevention

To mitigate the `SSRF` vulnerability, the `/api/v1/supplier-companies/certificates-of-incorporation` `POST` and `/api/v1/supplier-companies` `PATCH` endpoints must strictly prohibit file URIs that point to local resources on the server other than the intended ones. Implementing validation checks to ensure that file URIs only point to permissible local resources is crucial, which in this case is within the `wwwroot/SupplierCompaniesCertificatesOfIncorporations/` folder.

Furthermore, the `/api/v1/supplier-companies/{ID}/certificates-of-incorporation` `GET` endpoint must be configured to serve content exclusively from the designated folder `wwwroot/SupplierCompaniesCertificatesOfIncorporations`. This ensures that only certificates of incorporation are accessible and that local resources or files outside this directory are never exposed. Additionally, this acts as a safeguard, if in case the validations performed by the `/api/v1/supplier-companies/certificates-of-incorporation` `POST` and `/api/v1/supplier-companies` `PATCH` endpoints fail.


# Security Misconfiguration

* * *

Web APIs are susceptible to the same security misconfigurations that can compromise traditional web applications. One typical example is a web API endpoint that accepts user-controlled input and incorporates it into SQL queries without proper validation, thereby allowing [Injection](https://owasp.org/Top10/A03_2021-Injection/) attacks.

## Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection')

The endpoint we will be practicing against is vulnerable to [CWE-89: Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection')](https://cwe.mitre.org/data/definitions/89.html).

### Scenario

The admin of `Inlanefreight E-Commerce Marketplace` has provided us with the credentials `[email protected]:HTBPentester12`, wanting us to assess what API vulnerabilities the user can exploit with their assigned roles.

After obtaining a JWT as a supplier from the `/api/v1/authentication/suppliers/sign-in` endpoint and authenticating with it, we observe that the `/api/v1/roles/current-user` endpoint reveals that we have the `Products_GetProductsTotalCountByNameSubstring` role:

![API8_2023_Security_Misconfiguration_Image_1](https://academy.hackthebox.com/storage/modules/268/API8_2023_Security_Misconfiguration_Image_1.png)

The only endpoint related to that role name is `/api/v1/products/{Name}/count`, which belongs to the Products group. When exploring this endpoint, we find that it returns the total count of products containing a user-provided substring in their name:

![API8_2023_Security_Misconfiguration_Image_2](https://academy.hackthebox.com/storage/modules/268/API8_2023_Security_Misconfiguration_Image_2.png)

For example, if we use `laptop` as the `Name` substring parameter, we find that there are 18 matching products in total:

![API8_2023_Security_Misconfiguration_Image_3](https://academy.hackthebox.com/storage/modules/268/API8_2023_Security_Misconfiguration_Image_3.png)

However, if we try using `laptop'` (with a trailing apostrophe) as input, we observe that the endpoint returns an error message, indicating a potential vulnerability to SQL injection attacks:

![API8_2023_Security_Misconfiguration_Image_4](https://academy.hackthebox.com/storage/modules/268/API8_2023_Security_Misconfiguration_Image_4.png)

Let us attempt to retrieve the count of all records in the Products table using the payload `laptop' OR 1=1 --`; we will discover that there are 720 products in the table:

![API8_2023_Security_Misconfiguration_Image_5](https://academy.hackthebox.com/storage/modules/268/API8_2023_Security_Misconfiguration_Image_5.png)

### HTTP Headers

APIs can also suffer from security misconfigurations if they do not use proper [HTTP Security Response Headers](https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Headers_Cheat_Sheet.html). For example, suppose an API does not set a secure [Access-Control-Allow-Origin](https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Headers_Cheat_Sheet.html#access-control-allow-origin) as part of its `CORS` ( `Cross-Origin Resource Sharing`) policy. In that case, it can be exposed to security risks, most notably, [Cross-Site Request Forgery](https://cwe.mitre.org/data/definitions/352.html) ( `CSRF`).

### Prevention

To mitigate the `Security Misconfiguration` vulnerability, the `/api/v1/products/{Name}/count` endpoint should utilize parameterized queries or an [Object Relational Mapper](https://en.wikipedia.org/wiki/Object%E2%80%93relational_mapping) ( `ORM`) to safely insert user-controlled values into SQL queries. If that is not a choice, it must validate user-controlled input before concatenating it into the SQL query, which is never infallible.

Furthermore, if the web API is using HTTP headers insecurely or omits security-related ones, it should implement secure headers to prevent various security vulnerabilities from occurring. Projects like [OWASP Secure Headers](https://github.com/OWASP/www-project-secure-headers) provide guidance on HTTP security headers and how to avoid security vulnerabilities associated with improper header configurations.


# Improper Inventory Management

* * *

Maintaining accurate and up-to-date documentation is essential for web APIs, especially considering their reliance on third-party users who need to understand how to interact with the API effectively.

However, as a web API matures and undergoes changes, it is crucial to implement proper versioning practices to avoid security pitfalls. Improper inventory management of APIs, including inadequate versioning, can introduce security misconfigurations and increase the attack surface. This can manifest in various ways, such as outdated or incompatible API versions remaining accessible, creating potential entry points for unauthorized users.

## Scenario

In the previous sections, we have primarily interacted with `v1` of the `Inlanefreight E-Commerce Marketplace` web API. However, upon examining the `Swagger` UI's drop-down list for 'Select a definition', we discover the existence of an additional version, `v0`:

![API9_2023_Improper_Inventory_Management_Image_1](https://academy.hackthebox.com/storage/modules/268/API9_2023_Improper_Inventory_Management_Image_1.png)

Upon reviewing the description of `v0`, it is indicated that this version contains legacy and deleted data, serving as an unmaintained backup that should be removed. However, upon inspecting the endpoints, we will notice that none of them display a 'lock' icon, indicating that they do not require any form of authentication:

![API9_2023_Improper_Inventory_Management_Image_2](https://academy.hackthebox.com/storage/modules/268/API9_2023_Improper_Inventory_Management_Image_2.png)

Upon invoking the `/api/v0/customers/deleted` endpoint, the API responds by exposing deleted customer data, including sensitive password hashes:

![API9_2023_Improper_Inventory_Management_Image_3](https://academy.hackthebox.com/storage/modules/268/API9_2023_Improper_Inventory_Management_Image_3.png)

Due to oversight by the developers in neglecting to remove the `v0` endpoints, we gained unauthorized access to deleted data of former customers. This issue was exacerbated by an `Excessive Data Exposure` vulnerability in the `/api/v0/customers/deleted` endpoint, which allowed us to view customer password hashes. With this exposed information, we could attempt password cracking. Given the common practice of password reuse, this could potentially compromise active accounts, particularly if the same customers re-registered using the same password.

### Prevention

Effective versioning ensures that only the intended API versions are exposed to users, with older versions properly deprecated or sunset. By thoroughly managing the API inventory, `Inlanefreight E-Commerce Marketplace` can minimize the risk of exposing vulnerabilities and maintain a secure user interface.

To mitigate the `Improper Inventory Management` vulnerability, developers at `Inlanefreight E-Commerce Marketplace` should either remove `v0` entirely or, at a minimum, restrict access exclusively for local development and testing purposes, ensuring it remains inaccessible to external users. If neither option is viable, the endpoints should be protected with stringent authentication measures, permitting interaction solely by administrators.


# Unsafe Consumption of APIs

* * *

APIs frequently interact with other APIs to exchange data, forming a complex ecosystem of interconnected services. While this interconnectivity enhances functionality and efficiency, it also introduces significant security risks if not managed properly. Developers may blindly trust data received from third-party APIs, especially when provided by reputable organizations, leading to relaxed security measures, particularly in input validation and data sanitization.

Several critical vulnerabilities can arise from API-to-API communication:

1. `Insecure Data Transmission`: APIs communicating over unencrypted channels expose sensitive data to interception, compromising confidentiality and integrity.
2. `Inadequate Data Validation`: Failing to properly validate and sanitize data received from external APIs before processing or forwarding it to downstream components can lead to injection attacks, data corruption, or even remote code execution.
3. `Weak Authentication`: Neglecting to implement robust authentication methods when communicating with other APIs can result in unauthorized access to sensitive data or critical functionality.
4. `Insufficient Rate-Limiting`: An API can overwhelm another API by sending a continuous surge of requests, potentially leading to denial-of-service.
5. `Inadequate Monitoring`: Insufficient monitoring of API-to-API interactions can make it difficult to detect and respond to security incidents promptly.

If an API consumes another API insecurely, it is vulnerable to [CWE-1357: Reliance on Insufficiently Trustworthy Component](https://cwe.mitre.org/data/definitions/1357.html).

## Prevention

To prevent vulnerabilities arising from API-to-API communication, web API developers should implement the following measures:

- `Secure Data Transmission`: Use encrypted channels for data transmission to prevent exposure of sensitive data through man-in-the-middle attacks.
- `Adequate Data Validation`: Ensure proper validation and sanitization of data received from external APIs before processing or forwarding it to downstream components. This mitigates risks such as injection attacks, data corruption, or remote code execution.
- `Robust Authentication`: Employ secure authentication methods when communicating with other APIs to prevent unauthorized access to sensitive data or critical functionality.
- `Sufficient Rate-Limiting`: Implement rate-limiting mechanisms to prevent an API from overwhelming another API, thereby protecting against denial-of-service attacks.
- `Adequate Monitoring`: Implement robust monitoring of API-to-API interactions to promptly detect and respond to security incidents.


# Skills Assessment

* * *

## Scenario

After reporting all vulnerabilities in versions v0 and v1 of `Inlanefreight E-Commerce Marketplace`, the admin attempted to patch all of them in v2:

![Skills_Assessment_Image_1](https://academy.hackthebox.com/storage/modules/268/Skills_Assessment_Image_1.png)

However, new junior developers have implemented additional functionalities in v2, and the admin is concerned that they may have introduced new vulnerabilities. Assess the security of the new web API version and apply everything you have learned throughout the module to compromise it.


