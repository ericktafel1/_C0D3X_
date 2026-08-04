
# Introduction

Instead of using the request-response paradigm, the WebSocket protocol allows for full-duplex (i.e., bi-directional) message transmissions between servers and clients without any prior request from the other party. Such WebSocket connections typically remain open for an extended period and allow for data transmission anytime in any direction.

For example, let's consider a simple HTTP/1.1 chat room web application running in the browser of two participants, `Alice` and `Bob`. When `Alice` sends a message to `Bob`, her browser transmits the message to the web server; however, the web server will not be able to send the message to `Bob` simultaneously because it cannot send a message without a prior request. Thus, Bob's browser must periodically `poll` the web server for new messages from Alice, and depending on the number of messages transmitted to Bob, this mechanism creates much traffic and could be inefficient.

![[Pasted image 20250328160016.png]]
Suppose the same application uses WebSocket connections instead. In that case, Alice and Bob will establish a WebSocket connection with the web server upon login. Afterward, Alice's browser will simultaneously transmit her messages to Bob via the WebSocket connection without polling requests. Thus, WebSockets are highly advantageous for real-time applications.

Suppose the same application uses WebSocket connections instead. In that case, Alice and Bob will establish a WebSocket connection with the web server upon login. Afterward, Alice's browser will simultaneously transmit her messages to Bob via the WebSocket connection without polling requests. Thus, WebSockets are highly advantageous for real-time applications.

# Connection Establishment

```javascript
const socket = new WebSocket('ws://websockets.htb/echo');
```


```http
GET /echo HTTP/1.1
Host: websockets.htb
Connection: Upgrade
Upgrade: websocket
Sec-WebSocket-Version: 13
Sec-WebSocket-Key: 7QpTshdCiQfiv3tH7myJ1g==
Origin: http://websockets.htb
```

It contains the following important [headers](https://developer.mozilla.org/en-US/docs/Web/HTTP/Protocol_upgrade_mechanism#websocket-specific_headers):

- The [Connection](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Connection) header with the value `Upgrade` and the [Upgrade](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Upgrade) header with the value `websocket` indicate the client's intent to establish a WebSocket connection
- The `Sec-WebSocket-Version` header contains the WebSocket protocol version chosen by the client, with the latest version being [13](https://www.iana.org/assignments/websocket/websocket.xml#version-number)
- The `Sec-WebSocket-Key` header contains a unique value confirming that the client wants to establish a WebSocket connection; this header does not provide any security protections
- The [Origin](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Origin) header contains the origin just like in regular HTTP requests and is used for security purposes, as we will discuss in a later section

The server responds with a response similar to the following:
```http
HTTP/1.1 101 Switching Protocols
Connection: Upgrade
Upgrade: websocket
Sec-WebSocket-Accept: QU/gD/2y41z9ygrOaGWgaC+Pm2M=
```

The response contains the following information:

- The HTTP status code of [101](https://www.rfc-editor.org/rfc/rfc9110#name-101-switching-protocols) indicates that the WebSocket connection establishment has been completed
- The `Connection` and `Upgrade` headers contain the same values as in the client's request, which is `Upgrade` and `websocket`, respectively
- The [Sec-WebSocket-Accept](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Sec-WebSocket-Accept) header contains a value derived from the value sent by the client in the `Sec-WebSocket-Key` header and confirms that the server is willing to establish a WebSocket connection

After the server's response, the WebSocket connection has been established, and messages can be exchanged.

For more details on how to build web applications with WebSockets, check out the [WebSocket handbook](https://pages.ably.com/hubfs/the-websocket-handbook.pdf).