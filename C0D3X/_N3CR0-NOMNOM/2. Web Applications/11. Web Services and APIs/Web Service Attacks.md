# Web Service Approaches/Technologies

## XML-RPC

- [XML-RPC](http://xmlrpc.com/spec.md) uses XML for encoding/decoding the remote procedure call (RPC) and the respective parameter(s). HTTP is usually the transport of choice.

```http
--> POST /RPC2 HTTP/1.0
      User-Agent: Frontier/5.1.2 (WinNT)
      Host: betty.userland.com
      Content-Type: text/xml
      Content-length: 181
    
      <?xml version="1.0"?>
      <methodCall>
        <methodName>examples.getStateName</methodName>
        <params>
           <param>
     		     <value><i4>41</i4></value>
     		     </param>
    		  </params>
        </methodCall>
    
<-- HTTP/1.1 200 OK
      Connection: close
      Content-Length: 158
      Content-Type: text/xml
      Date: Fri, 17 Jul 1998 19:55:08 GMT
      Server: UserLand Frontier/5.1.2-WinNT
    
      <?xml version="1.0"?>
      <methodResponse>
         <params>
            <param>
    		      <value><string>South Dakota</string></value>
    		      </param>
      	    </params>
       </methodResponse>
```

The payload in XML is essentially a single `<methodCall>` structure. `<methodCall>` should contain a `<methodName>` sub-item, that is related to the method to be called. If the call requires parameters, then `<methodCall>` must contain a `<params>` sub-item.

## JSON-RPC

- [JSON-RPC](https://www.jsonrpc.org/specification) uses JSON to invoke functionality. HTTP is usually the transport of choice.

```http
--> POST /ENDPOINT HTTP/1.1
       Host: ...
       Content-Type: application/json-rpc
       Content-Length: ...
    
      {"method": "sum", "params": {"a":3, "b":4}, "id":0}
    
<-- HTTP/1.1 200 OK
       ...
       Content-Type: application/json-rpc
    
       {"result": 7, "error": null, "id": 0}
```

The `{"method": "sum", "params": {"a":3, "b":4}, "id":0}` object is serialized using JSON. Note the three properties: `method`, `params` and `id`. `method` contains the name of the method to invoke. `params` contains an array carrying the arguments to be passed. `id` contains an identifier established by the client. The server must reply with the same value in the response object if included.

## SOAP (Simple Object Access Protocol)

- SOAP also uses XML but provides more functionalities than XML-RPC. SOAP defines both a header structure and a payload structure. The former identifies the actions that SOAP nodes are expected to take on the message, while the latter deals with the carried information. A Web Services Definition Language (WSDL) declaration is optional. WSDL specifies how a SOAP service can be used. Various lower-level protocols (HTTP included) can be the transport.
- Anatomy of a SOAP Message
    - `soap:Envelope`: (Required block) Tag to differentiate SOAP from normal XML. This tag requires a `namespace` attribute.
    - `soap:Header`: (Optional block) Enables SOAP’s extensibility through SOAP modules.
    - `soap:Body`: (Required block) Contains the procedure, parameters, and data.
    - `soap:Fault`: (Optional block) Used within `soap:Body` for error messages upon a failed API call.
    
```http
--> POST /Quotation HTTP/1.0
      Host: www.xyz.org
      Content-Type: text/xml; charset = utf-8
      Content-Length: nnn
    
      <?xml version = "1.0"?>
      <SOAP-ENV:Envelope
        xmlns:SOAP-ENV = "http://www.w3.org/2001/12/soap-envelope"
         SOAP-ENV:encodingStyle = "http://www.w3.org/2001/12/soap-encoding">
    
        <SOAP-ENV:Body xmlns:m = "http://www.xyz.org/quotations">
           <m:GetQuotation>
             <m:QuotationsName>MiscroSoft</m:QuotationsName>
          </m:GetQuotation>
        </SOAP-ENV:Body>
      </SOAP-ENV:Envelope>
    
<-- HTTP/1.0 200 OK
      Content-Type: text/xml; charset = utf-8
      Content-Length: nnn
    
      <?xml version = "1.0"?>
      <SOAP-ENV:Envelope
       xmlns:SOAP-ENV = "http://www.w3.org/2001/12/soap-envelope"
        SOAP-ENV:encodingStyle = "http://www.w3.org/2001/12/soap-encoding">
    
      <SOAP-ENV:Body xmlns:m = "http://www.xyz.org/quotation">
      	  <m:GetQuotationResponse>
      	     <m:Quotation>Here is the quotation</m:Quotation>
         </m:GetQuotationResponse>
       </SOAP-ENV:Body>
      </SOAP-ENV:Envelope>
```

**Note**: You may come across slightly different SOAP envelopes. Their anatomy will be the same, though.
### WS-BPEL (Web Services Business Process Execution Language)

- WS-BPEL web services are essentially SOAP web services with more functionality for describing and invoking business processes.
- WS-BPEL web services heavily resemble SOAP services. For this reason, they will not be included in this module's scope.

### RESTful (Representational State Transfer)
- REST web services usually use XML or JSON. WSDL declarations are supported but uncommon. HTTP is the transport of choice, and HTTP verbs are used to access/change/delete resources and use data.

```http
--> POST /api/2.2/auth/signin HTTP/1.1
      HOST: my-server
      Content-Type:text/xml
    
      <tsRequest>
        <credentials name="administrator" password="passw0rd">
          <site contentUrl="" />
        </credentials>
      </tsRequest>
      
```

```http
--> POST /api/2.2/auth/signin HTTP/1.1
      HOST: my-server
      Content-Type:application/json
      Accept:application/json
    
      {
       "credentials": {
         "name": "administrator",
        "password": "passw0rd",
        "site": {
          "contentUrl": ""
         }
        }
      }
    
```


# Web Services Description Language (WSDL)

WSDL stands for Web Service Description Language. WSDL is an XML-based file exposed by web services that informs clients of the provided services/methods, including where they reside and the method-calling convention.

A web service's WSDL file should not always be accessible. Developers may not want to publicly expose a web service's WSDL file, or they may expose it through an uncommon location, following a security through obscurity approach. In the latter case, directory/parameter fuzzing may reveal the location and content of a WSDL file.

```shell-session
curl http://<TARGET IP>:3002/wsdl 
```

The response is empty! Maybe there is a parameter that will provide us with access to the SOAP web service's WSDL file. Let us perform parameter fuzzing using _ffuf_ and the [burp-parameter-names.txt](https://github.com/danielmiessler/SecLists/blob/master/Discovery/Web-Content/burp-parameter-names.txt) list, as follows. _-fs 0_ filters out empty responses (size = 0) and _-mc 200_ matches _HTTP 200_ responses.

```shell-session
ffuf -w /usr/share/seclists/Discovery/Web-Content/burp-parameter-names.txt -u 'http://<TARGET IP>:3002/wsdl?FUZZ' -fs 0 -mc 200
```

## WSDL File Breakdown

The above WSDL file follows the [WSDL version 1.1](https://www.w3.org/TR/2001/NOTE-wsdl-20010315) layout and consists of the following elements.

- `Definition`
    - The root element of all WSDL files. Inside the definition, the name of the web service is specified, all namespaces used across the WSDL document are declared, and all other service elements are defined.

        ```xml
        <wsdl:definitions targetNamespace="http://tempuri.org/" 
        
            <wsdl:types></wsdl:types>
            <wsdl:message name="LoginSoapIn"></wsdl:message>
            <wsdl:portType name="HacktheBoxSoapPort">
          	  <wsdl:operation name="Login"></wsdl:operation>
            </wsdl:portType>
            <wsdl:binding name="HacktheboxServiceSoapBinding" type="tns:HacktheBoxSoapPort">
          	  <wsdl:operation name="Login">
          		  <soap:operation soapAction="Login" style="document"/>
          		  <wsdl:input></wsdl:input>
          		  <wsdl:output></wsdl:output>
          	  </wsdl:operation>
            </wsdl:binding>
            <wsdl:service name="HacktheboxService"></wsdl:service>
        </wsdl:definitions>
        ```
        
- `Data Types`
    - The data types to be used in the exchanged messages.
    - Code: xml
        
        ```xml
        <wsdl:types>
            <s:schema elementFormDefault="qualified" targetNamespace="http://tempuri.org/">
          	  <s:element name="LoginRequest">
          		  <s:complexType>
          			  <s:sequence>
          				  <s:element minOccurs="1" maxOccurs="1" name="username" type="s:string"/>
          				  <s:element minOccurs="1" maxOccurs="1" name="password" type="s:string"/>
          			  </s:sequence>
          		  </s:complexType>
          	  </s:element>
          	  <s:element name="LoginResponse">
          		  <s:complexType>
          			  <s:sequence>
          				  <s:element minOccurs="1" maxOccurs="unbounded" name="result" type="s:string"/>
          			  </s:sequence>
          		  </s:complexType>
          	  </s:element>
          	  <s:element name="ExecuteCommandRequest">
          		  <s:complexType>
          			  <s:sequence>
          				  <s:element minOccurs="1" maxOccurs="1" name="cmd" type="s:string"/>
          			  </s:sequence>
          		  </s:complexType>
          	  </s:element>
          	  <s:element name="ExecuteCommandResponse">
          		  <s:complexType>
          			  <s:sequence>
          				  <s:element minOccurs="1" maxOccurs="unbounded" name="result" type="s:string"/>
          			  </s:sequence>
          		  </s:complexType>
          	  </s:element>
            </s:schema>
        </wsdl:types>
        ```
        
- `Messages`
    - Defines input and output operations that the web service supports. In other words, through the _messages_ element, the messages to be exchanged, are defined and presented either as an entire document or as arguments to be mapped to a method invocation.
    - Code: xml
        
        ```xml
        <!-- Login Messages -->
        <wsdl:message name="LoginSoapIn">
            <wsdl:part name="parameters" element="tns:LoginRequest"/>
        </wsdl:message>
        <wsdl:message name="LoginSoapOut">
            <wsdl:part name="parameters" element="tns:LoginResponse"/>
        </wsdl:message>
        <!-- ExecuteCommand Messages -->
        <wsdl:message name="ExecuteCommandSoapIn">
            <wsdl:part name="parameters" element="tns:ExecuteCommandRequest"/>
        </wsdl:message>
        <wsdl:message name="ExecuteCommandSoapOut">
            <wsdl:part name="parameters" element="tns:ExecuteCommandResponse"/>
        </wsdl:message>
          ```	
        ```
        
- `Operation`
    - Defines the available SOAP actions alongside the encoding of each message.
- `Port Type`
    - Encapsulates every possible input and output message into an operation. More specifically, it defines the web service, the available operations and the exchanged messages. Please note that in WSDL version 2.0, the _interface_ element is tasked with defining the available operations and when it comes to messages the (data) types element handles defining them.
    - Code: xml
        
        ```xml
        <wsdl:portType name="HacktheBoxSoapPort">
            <!-- Login Operaion | PORT -->
            <wsdl:operation name="Login">
          	  <wsdl:input message="tns:LoginSoapIn"/>
          	  <wsdl:output message="tns:LoginSoapOut"/>
            </wsdl:operation>
            <!-- ExecuteCommand Operation | PORT -->
            <wsdl:operation name="ExecuteCommand">
          	  <wsdl:input message="tns:ExecuteCommandSoapIn"/>
          	  <wsdl:output message="tns:ExecuteCommandSoapOut"/>
            </wsdl:operation>
        </wsdl:portType>
        ```
        
- `Binding`
    - Binds the operation to a particular port type. Think of bindings as interfaces. A client will call the relevant port type and, using the details provided by the binding, will be able to access the operations bound to this port type. In other words, bindings provide web service access details, such as the message format, operations, messages, and interfaces (in the case of WSDL version 2.0).
    - Code: xml
        
        ```xml
        <wsdl:binding name="HacktheboxServiceSoapBinding" type="tns:HacktheBoxSoapPort">
            <soap:binding transport="http://schemas.xmlsoap.org/soap/http"/>
            <!-- SOAP Login Action -->
            <wsdl:operation name="Login">
          	  <soap:operation soapAction="Login" style="document"/>
          	  <wsdl:input>
          		  <soap:body use="literal"/>
          	  </wsdl:input>
          	  <wsdl:output>
          		  <soap:body use="literal"/>
          	  </wsdl:output>
            </wsdl:operation>
            <!-- SOAP ExecuteCommand Action -->
            <wsdl:operation name="ExecuteCommand">
          	  <soap:operation soapAction="ExecuteCommand" style="document"/>
          	  <wsdl:input>
          		  <soap:body use="literal"/>
          	  </wsdl:input>
          	  <wsdl:output>
          		  <soap:body use="literal"/>
          	  </wsdl:output>
            </wsdl:operation>
        </wsdl:binding>
        ```
        
- `Service`
    - A client makes a call to the web service through the name of the service specified in the service tag. Through this element, the client identifies the location of the web service.
    - Code: xml
        
        ```xml
            <wsdl:service name="HacktheboxService">
        
              <wsdl:port name="HacktheboxServiceSoapPort" binding="tns:HacktheboxServiceSoapBinding">
                <soap:address location="http://localhost:80/wsdl"/>
              </wsdl:port>
        
            </wsdl:service>
        ```
# Web Services

## SOAPAction Spoofing

SOAP messages towards a SOAP service should include both the operation and the related parameters. This operation resides in the first child element of the SOAP message's body. If HTTP is the transport of choice, it is allowed to use an additional HTTP header called SOAPAction, which contains the operation's name. The receiving web service can identify the operation within the SOAP body through this header without parsing any XML.

If a web service considers only the SOAPAction attribute when determining the operation to execute, then it may be vulnerable to SOAPAction spoofing.

## Command Injection

Command injections are among the most critical vulnerabilities in web services. They allow system command execution directly on the back-end server. If a web service uses user-controlled input to execute a system command on the back-end server, an attacker may be able to inject a malicious payload to subvert the intended command and execute his own.