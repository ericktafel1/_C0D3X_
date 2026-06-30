# Description

When malicious user-supplied input does not trigger a vulnerability at the initial injection point but later when the web application stores or processes it, this is known as a second-order vulnerability.

Some web vulnerabilities are inherently second-order. For instance, consider a `stored XSS` in a social media network, where a user can send another user a message containing an XSS payload. When the other user opens the message, the XSS payload is triggered. As such, the injection point (i.e., sending the message) differs from the trigger (i.e., opening the message). In other words, the user-supplied payload is stored and displayed in a different endpoint unsafely, resulting in an XSS vulnerability. Thus, stored XSS can be considered a second-order vulnerability.

More specifically, any web vulnerability that requires this indirection can be considered a second-order vulnerability. These vulnerabilities are significantly harder to identify as the immediate injection point might seem secure, and a different endpoint must be hit to trigger the vulnerability. Thus, it is crucial to have a good understanding of the underlying inner workings of the particular web application to identify and exploit second-order vulnerabilities.

[[IDOR (Insecure Direct Object References)#Second-Order IDOR]]