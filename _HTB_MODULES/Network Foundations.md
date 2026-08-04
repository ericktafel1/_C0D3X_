# Introduction to Networks

* * *

Welcome to Network Foundations! In this introductory module, we will explore the technology behind computer networking - also known as "networking" or "networks" - and why it is essential to our lives. We will mostly focus on two primary types of networks: `Local Area Networks (LANs)` and `Wide Area Networks (WANs)`.

Understanding how devices are able communicate with one another, from inside our homes to across the globe, is fundamental knowledge for those looking to enter the field of cyber security. The interconnectedness of almost every device in our world today is what sets the backdrop for the ever increasing demand for security professionals.

* * *

## What is a Network?

A `network` is a collection of interconnected devices that can communicate - sending and receiving data, and also sharing resources with each other. These individual endpoint devices, often called `nodes`, include computers, smartphones, printers, and servers. However, `nodes` alone do not comprise the entire network. The table below shows some networking `key concepts`.

| **Concepts** | **Description** |
| --- | --- |
| `Nodes` | Individual devices connected to a network. |
| `Links` | Communication pathways that connect nodes (wired or wireless). |
| `Data Sharing` | The primary purpose of a network is to enable data exchange. |

Let's explain the above using a real-world example. Think of a group of friends chatting in a room. Each person represents a device ( `node`), and their ability to talk and listen represents the `communication links`. The conversation is the `data` being shared.

* * *

## Why Are Networks Important?

Networks, particularly since the advent of the Internet, have radically transformed society, enabling a multitude of possibilities that are now essential to our lives. Below are just a few of the benefits afforded to us by this incredible technology.

| **Function** | **Description** |
| --- | --- |
| `Resource Sharing` | Multiple devices can share hardware (like printers) and software resources. |
| `Communication` | Instant messaging, emails, and video calls rely on networks. |
| `Data Access` | Access files and databases from any connected device. |
| `Collaboration` | Work together in real-time, even when miles apart. |

* * *

## Types of Networks

Networks vary in size and scope. The two primary types are `Local Area Network (LAN)` and `Wide Area Network (WAN)`.

#### Local Area Network (LAN)

A `Local Area Network (LAN)` connects devices over a short distance, such as within a home, school, or small office building. Here are some of its key characteristics:

| **Characteristic** | **Description** |
| --- | --- |
| `Geographical Scope` | Covers a small area. |
| `Ownership` | Typically owned and managed by a single person or organization. |
| `Speed` | High data transfer rates. |
| `Media` | Uses wired (Ethernet cables) or wireless (Wi-Fi) connections. |

The following diagram shows how a home's Wi-Fi connects devices such as laptops, smartphones, and smart TVs, allowing them to share files and access the internet.

![Network diagram showing Internet connected to a modem, then a router, with wired and Wi-Fi connections to a PC, laptop, smartphone, and printer.](https://academy.hackthebox.com/storage/modules/289/introduction/lan_1-1.png)

#### Wide Area Network (WAN)

A `Wide Area Network (WAN)` spans a large geographical area, connecting multiple LANs. Below are some of its key characteristics:

| **Characteristic** | **Description** |
| --- | --- |
| `Geographical Scope` | Covers cities, countries, or continents. |
| `Ownership` | Often a collective or distributed ownership (e.g., internet service providers). |
| `Speed` | Slower data transfer rates compared to LANs due to long-distance data travel. |
| `Media` | Utilizes fiber optics, satellite links, and leased telecommunication lines. |

The Internet is the largest example of a `WAN`, connecting millions of `LANs` globally.

![Network diagram showing three identical setups: Internet to modem to router, with wired and Wi-Fi connections to PC, laptop, smartphone, and printer.](https://academy.hackthebox.com/storage/modules/289/introduction/wan-2.png)

* * *

#### Comparing LAN and WAN

| Aspect | LAN | WAN |
| --- | --- | --- |
| `Size` | Small, localized area | Large, broad area |
| `Ownership` | Single person or organization | Multiple organizations/service providers |
| `Speed` | High | Lower compared to LAN |
| `Maintenance` | Easier and less expensive | Complex and costly |
| `Example` | Home or office network | The Internet |

* * *

## How Do LANs and WANs Work Together?

Local Area Networks (LANs) can connect to Wide Area Networks (WANs) to access broader networks beyond their immediate scope. This connectivity allows for expanded communication and resource sharing on a much larger scale.

For instance, when accessing the Internet, a home LAN connects to an `Internet Service Provider's (ISP's)` WAN, which grants Internet access to all devices within the home network. An ISP is a company that provides individuals and organizations with access to the Internet. In this setup, a device called a modem (modulator-demodulator) plays a crucial role. The modem acts as a bridge between your home network and the ISP's infrastructure, converting digital signals from your router into a format suitable for transmission over various media like telephone lines, cable systems, and fiber optics. This connection transforms a simple local network into a gateway to the resources available online.

In a business setting, companies link multiple office LANs via WANs to achieve unified communication and collaboration across different geographic locations. By connecting these LANs through a WAN, employees in various offices can share information, access centralized databases, and work together in real-time, enhancing productivity within the organization.

Let's consider the following scenario to illustrate how LANs and WANs work together. At home, our devices—such as laptops, smartphones, and tablets—connect to our home router, forming a LAN. This router doesn't just manage local traffic; it also communicates with our ISP's WAN. Through this connection to the WAN, our home network gains the ability to access websites and online services hosted all over the world. This seamless integration between the LAN and WAN enables us to reach global content and interact with services beyond our local network.

Enable step-by-step solutions for all questions
![sparkles-icon-decoration](https://academy.hackthebox.com/images/sparkles-solid.svg)

#### Questions

Answer the question(s) below
to complete this Section and earn cubes!

\+ 0  What is the term for a collection of interconnected devices that can communicate and share resources with each other?


Submit


\+ 0  In network terminology, what is the term for individual devices connected to a network?


Submit


\+ 0  What is the largest Wide Area Network (WAN) that connects millions of Local Area Networks (LANs) globally?


Submit


\+ 0  What is the acronym for a network that connects devices over a short distance, such as within a home, school, or small office building?


Submit


\+ 0  In networking, what term describes the communication pathways (wired or wireless) that connect nodes?


Submit


# Network Concepts

* * *

Understanding the nuts and bolts behind networking is undoubtedly important. However, many are not aware just how ubiquitous networking become. The incredibly complex technology stack in use today - what we see across consumer electronics, multimedia devices, hardware, software and firmware - was all built in conjunction with (or on top of) the `TCP/IP` stack.

Furthermore, in this section we will cover a few key concepts that help to illustrate how networking fits into the wider ecosystem of technology. We will discuss the `OSI` and `TCP/IP` models, some `common network protocols` used as rules and standards for data exchange, and the various `transmission methods` that enable information to traverse efficiently and securely across the network.

* * *

## OSI Model

The `Open Systems Interconnection (OSI) model` is a conceptual framework that standardizes the functions of a telecommunication or computing system into seven abstract layers. This model helps vendors and developers create interoperable network devices and software. Below we see the seven layers of the OSI Model.

#### Physical Layer (Layer 1)

The `Physical Layer` is the first and lowest layer of the OSI model. It is responsible for transmitting raw bitstreams over a physical medium. This layer deals with the physical connection between devices, including the hardware components like Ethernet cables, hubs, and repeaters.

#### Data Link Layer (Layer 2)

The `Data Link Layer` provides node-to-node data transfer - a direct link between two physically connected nodes. It ensures that data frames are transmitted with proper synchronization, error detection, and correction. Devices such as switches and bridges operate at this layer, using [MAC (Media Access Control)](https://en.wikipedia.org/wiki/MAC_address) addresses to identify network devices.

#### Network Layer (Layer 3)

The `Network Layer` handles packet forwarding, including the routing of packets through different routers to reach the destination network. It is responsible for logical addressing and path determination, ensuring that data reaches the correct destination across multiple networks. Routers operate at this layer, using [IP (Internet Protocol) addresses](https://usa.kaspersky.com/resource-center/definitions/what-is-an-ip-address?srsltid=AfmBOoq0TltVlJi8PKDn6j4yNB0V5Av5Y4srTxb32Bbbg4TcAfZ5FG8H) to identify devices and determine the most efficient path for data transmission.

#### Transport Layer (Layer 4)

The `Transport Layer` provides end-to-end communication services for applications. It is responsible for the reliable (or unreliable) delivery of data, segmentation, reassembly of messages, flow control, and error checking. Protocols like `TCP (Transmission Control Protocol)` and `UDP (User Datagram Protocol)` function at this layer. TCP offers reliable, connection-oriented transmission with error recovery, while UDP provides faster, connectionless communication without guaranteed delivery.

#### Session Layer (Layer 5)

The `Session Layer` manages sessions between applications. It establishes, maintains, and terminates connections, allowing devices to hold ongoing communications known as sessions. This layer is essential for session checkpointing and recovery, ensuring that data transfer can resume seamlessly after interruptions. Protocols and `APIs (Application Programming Interfaces)` operating at this layer coordinate communication between systems and applications.

#### Presentation Layer (Layer 6)

The `Presentation Layer` acts as a translator between the application layer and the network format. It handles data representation, ensuring that information sent by the application layer of one system is readable by the application layer of another. This includes data encryption and decryption, data compression, and converting data formats. Encryption protocols and data compression techniques operate at this layer to secure and optimize data transmission.

#### Application Layer (Layer 7)

The `Application Layer` is the topmost layer of the OSI model and provides network services directly to end-user applications. It enables resource sharing, remote file access, and other network services. Common protocols operating at this layer include `HTTP (Hypertext Transfer Protocol)` for web browsing, `FTP (File Transfer Protocol)` for file transfers, `SMTP (Simple Mail Transfer Protocol)` for email transmission, and `DNS (Domain Name System)` for resolving domain names to IP addresses. This layer serves as the interface between the network and the application software.

![OSI model layers: 1. Physical - Ethernet cables, 2. Data Link - MAC addresses, 3. Network - IP addresses, 4. Transport - TCP/UDP, 5. Session - APIs, 6. Presentation - Encryption, 7. Application - HTTP/FTP.](https://academy.hackthebox.com/storage/modules/289/network_concepts/OSI.png)

#### Example of Sending a File Across Network Layers

When sending a file over a network, several steps occur across different layers of the network model. The process begins at the `Application Layer`, which initiates the file transfer request. Following this, the `Presentation Layer` encrypts the file to ensure its security during transmission. The `Session Layer` then establishes a communication session with the receiving device. At the `Transport Layer`, the file is broken down into segments to ensure error-free transmission. The `Network Layer` takes over to determine the best route for transferring the data across the network. Next, the `Data Link Layer` encapsulates the data into frames, preparing it for node-to-node delivery. Finally, the `Physical Layer` handles the actual transmission of bits over the physical medium, completing the process.

* * *

## TCP/IP Model

The `Transmission Control Protocol/Internet Protocol (TCP/IP) model` is a condensed version of the `OSI` model, tailored for practical implementation on the internet and other networks. Below we see the four layers of the `TCP/IP Model`.

#### Link Layer

This layer is responsible for handling the physical aspects of network hardware and media. It includes technologies such as Ethernet for wired connections and Wi-Fi for wireless connections. The Link Layer corresponds to the Physical and Data Link Layers of the OSI model, covering everything from the physical connection to data framing.

#### Internet Layer

The `Internet Layer` manages the logical addressing of devices and the routing of packets across networks. Protocols like IP (Internet Protocol) and ICMP (Internet Control Message Protocol) operate at this layer, ensuring that data reaches its intended destination by determining logical paths for packet transmission. This layer corresponds to the Network Layer in the OSI model.

#### Transport Layer

At the `Transport Layer`, the TCP/IP model provides end-to-end communication services that are essential for the functioning of the internet. This includes the use of TCP (Transmission Control Protocol) for reliable communication and UDP (User Datagram Protocol) for faster, connectionless services. This layer ensures that data packets are delivered in a sequential and error-free manner, corresponding to the Transport Layer of the OSI model.

#### Application Layer

The `Application Layer` of the TCP/IP model contains protocols that offer specific data communication services to applications. Protocols such as HTTP (Hypertext Transfer Protocol), FTP (File Transfer Protocol), and SMTP (Simple Mail Transfer Protocol) enable functionalities like web browsing, file transfers, and email services. This layer corresponds to the top three layers of the OSI model (Session, Presentation, and Application), providing interfaces and protocols necessary for data exchange between systems.

![Network layers: 1. Network Interface - NICs, Ethernet cables, 2. Internet - IP, routers, 3. Transport - TCP/UDP, 4. Application - HTTP/FTP protocols.](https://academy.hackthebox.com/storage/modules/289/network_concepts/TCP_IP.png)

#### Comparison with OSI Model:

The TCP/IP model simplifies the complex structure of the OSI model by combining certain layers for practical implementation. Specifically designed around the protocols used on the internet, the TCP/IP model is more application-oriented, focusing on the needs of real-world network communication. This design makes it more effective for internet-based data exchange, meeting modern technological needs.

![Comparison of OSI and TCP/IP models: OSI has 7 layers from Physical to Application; TCP/IP has 4 layers from Network Interface to Application.](https://academy.hackthebox.com/storage/modules/289/network_concepts/OSI_vs_TCP-IP.png)

#### Example of Accessing a Website

When accessing a website, several layers of the TCP/IP model work together to facilitate the process. At the Application Layer, your browser utilizes HTTP to request the webpage. This request then moves to the Transport Layer, where TCP ensures the data is transferred reliably. The Internet Layer comes into play next, with IP taking charge of routing the data packets from our device to the web server. Finally, at the Network Interface Layer, the data is physically transmitted over the network, completing the connection that allows us to view the website.

#### Model Roles

In practical terms, the TCP/IP model is the backbone of network data transmission, actively employed across various networking environments. On the other hand, the OSI model, while not directly implemented, plays a crucial role as a comprehensive theoretical framework. It helps demystify the complexities of network operations, providing clear insights and a structured approach to understanding how networks function. Together, these models form a complete picture, bridging the gap between theoretical knowledge and practical application in networking.

* * *

## Protocols

`Protocols` are standardized rules that determine the formatting and processing of data to facilitate communication between devices in a network. These protocols operate at different layers within network models, each tailored to handle specific types of data and communication needs. Here’s a look at some common network protocols and their roles in data exchange.

#### Common Network Protocols

Network protocols are essential for defining how data is exchanged across networks. Each protocol operates at a specific layer of the OSI model, ensuring structured and efficient data handling.

| **Protocol** | **Description** |
| --- | --- |
| `HTTP (Hypertext Transfer Protocol)` | Primarily used for transferring web pages. It operates at the Application Layer, allowing browsers and servers to communicate in the delivery of web content. |
| `FTP (File Transfer Protocol)` | Facilitates the transfer of files between systems, also functioning at the Application Layer. It provides a way for users to upload or download files to and from servers. |
| `SMTP (Simple Mail Transfer Protocol)` | Handles the transmission of email. Operating at the Application Layer, it is responsible for sending messages from one server to another, ensuring they reach their intended recipients. |
| `TCP (Transmission Control Protocol)` | Ensures reliable data transmission through error checking and recovery, operating at the Transport Layer. It establishes a connection between sender and receiver to guarantee the delivery of data in the correct order. |
| `UDP (User Datagram Protocol)` | Allows for fast, connectionless communication, which operates without error recovery. This makes it ideal for applications that require speed over reliability, such as streaming services. UDP operates at the Transport Layer. |
| `IP (Internet Protocol)` | Crucial for routing packets across network boundaries, functioning at the Internet Layer. It handles the addressing and routing of packets to ensure they travel from the source to the destination across diverse networks. |

* * *

## Transmission

`Transmission` in networking refers to the process of sending data signals over a medium from one device to another. To further understand this concept, let’s examine the different types of transmission, the modes in which these transmissions can occur, and the media that carry the signals.

#### Transmission Types

Transmission in networking can be categorized into two main types: `analog` and `digital`. Analog transmission uses continuous signals to represent information, commonly seen in traditional radio broadcasts. In contrast, digital transmission employs discrete signals (bits) to encode data, which is typical in modern communication technologies like computer networks and digital telephony.

#### Transmission Modes

Transmission modes define how data is sent between two devices. `Simplex` mode allows one-way communication only, such as from a keyboard to a computer, where signals travel in a single direction. `Half-duplex` mode permits two-way communication but not simultaneously; examples include walkie-talkies where users must take turns speaking. `Full-duplex` mode, used in telephone calls, supports two-way communication simultaneously, allowing both parties to speak and listen at the same time.

#### Transmission Media

The physical means by which data is transmitted in a network is known as transmission media, which can be wired or wireless. Wired media includes `twisted pair` cables, commonly used in Ethernet networks and local area network (LAN) connections; `coaxial` cables, used for cable TV and early Ethernet; and `fiber optic` cables, which transmit data as light pulses and are essential for high-speed internet backbones. Wireless media, on the other hand, encompasses `radio waves` for Wi-Fi and cellular networks, `microwaves` for satellite communications, and `infrared` technology used for short-range communications like remote controls. Each type of media has its specific use cases depending on the requirements of the network environment.

Enable step-by-step solutions for all questions
![sparkles-icon-decoration](https://academy.hackthebox.com/images/sparkles-solid.svg)

#### Questions

Answer the question(s) below
to complete this Section and earn cubes!

\+ 0  What layer of the OSI model is responsible for physical connections like Ethernet cables? (Format: two words)


Submit


\+ 0  Name the OSI layer that deals with logical addressing and routing. (Format: two words)


Submit


\+ 0  Which protocol ensures reliable delivery of data and operates at the Transport Layer?


Submit


\+ 0  At what layer do switches operate within the OSI model? (Format: three words)


Submit


\+ 0  What layer of the TCP/IP model corresponds to the OSI model’s Application, Presentation, and Session layers? (Format: two words)


Submit


\+ 0  Which layer of the OSI model manages data encryption and data format conversion? (Format: two words)


Submit


\+ 0  Name a protocol used for web browsing that operates at the Application Layer.


Submit


\+ 0  Which OSI layer ensures the segments are transferred reliably and in sequence? (Format: two words)


Submit


\+ 0  Which protocol provides fast, connectionless communication and operates at the Transport Layer?


Submit


# Components of a Network

* * *

As we continue our journey into infosec, understanding the various components that formulate a network is essential. We know that currently, devices are able to communicate with each other, share resources, and access the internet with almost uniform consistency. What exactly facilitates this? The primary components of such a network include:

| **Component** | **Description** |
| --- | --- |
| `End Devices` | Computers, Smartphones, Tablets, IoT / Smart Devices |
| `Intermediary Devices` | Switches, Routers, Modems, Access Points |
| `Network Media and Software Components` | Cables, Protocols, Management and Firewalls Software |
| `Servers` | Web Servers, File Servers, Mail Servers, Database Servers |
|  |  |

Let's explore each of these in detail.

## End Devices

An `end device`, also known as a `host`, is any device that ultimately ends up sending or receiving data within a network. Personal computers and smart devices (such as phones and smart TVs) are common end devices; users routinely interact with them directly to perform tasks like browsing the web, sending messages, and creating documents. In most networks, such devices play a crucial role in both data generation and data consumption, like when users stream videos or read web content. End devices serve as the primary user interface to the world wide web, enabling users to access network resources and services seamlessly, through both wired (Ethernet) and wireless (Wi-Fi) connections. Another typical example of this would be a student using a notebook to connect to a school’s Wi-Fi network, allowing them to access online learning materials, submit assignments, and communicate with instructors.

## Intermediary Devices

An `intermediary device` has the unique role of facilitating the flow of data between `end devices`, either within a local area network, or between different networks. These devices include routers, switches, modems, and access points - all of which play crucial roles in ensuring efficient and secure data transmission. Intermediary devices are responsible for `packet forwarding`, directing data packets to their destinations by reading network address information and determining the most efficient paths. They connect networks and control traffic to enhance performance and reliability. By managing data flow with protocols, they ensure smooth transmission and prevent congestion. Additionally, intermediary devices often incorporate security features like `firewalls` to protect certain networks from unauthorized access and potential threats. Operating at different layers of the OSI model—for example, routers at the `Network Layer (Layer 3)` and switches at the `Data Link Layer (Layer 2)`—use routing tables and protocols to make informed decisions about data forwarding . A common example is a home network where intermediary devices like routers and switches connect all household devices—including notebooks, smartphones, and smart TVs—to the internet, enabling communication and access to online resources.

#### Network Interface Cards (NICs)

A `Network Interface Card (NIC)` is a hardware component installed in a computer, or other device, that enables connection to a network. It provides the physical interface between the device and the network media, handling the sending and receiving of data over the network. Each NIC has a unique Media Access Control (MAC) address, which is essential for devices to identify each other, and facilitate communication at the data link layer. NICs can be designed for wired connections, such as Ethernet cards that connect via cables, or for wireless connections, like Wi-Fi adapters utilizing radio waves. For example, a desktop computer might use a wired NIC, along with an Ethernet cable, to connect to a local network, while a laptop uses a wireless NIC to connect via Wi-Fi.

#### Routers

A `router` is an intermediary device that plays a hugely important role - the forwarding of data packets between networks, and ultimately directing internet traffic. Operating at the network layer (Layer 3) of the OSI model, routers read the network address information in data packets to determine their destinations. They use routing tables and routing protocols—such as `Open Shortest Path First (OSPF)` or `Border Gateway Protocol (BGP)`—to find the most efficient path for data to travel across interconnected networks, including the internet.

They fulfill this role by `examining incoming data packets` and forwarding them toward their destinations, based on IP addresses. By `connecting multiple networks`, routers enable devices on different networks to communicate. They also manage network traffic by selecting optimal paths for data transmission, which helps prevent congestion—a process known as `traffic management`. Additionally, routers enhance `security` by incorporating features like firewalls and access control lists, protecting the network from unauthorized access and potential threats.

#### Example

In a home network, a router connects all household devices—such as computers, smartphones, and smart TVs—to the internet provided by an Internet Service Provider (ISP). The router directs incoming and outgoing internet traffic efficiently, ensuring that each device can communicate with external networks and with each other.

#### Switches

The `switch` is another integral component, with it's primary job being to connect multiple devices within the same network, typically a Local Area Network (LAN). Operating at the data link layer (Layer 2) of the OSI model, switches use MAC addresses to forward data only to the intended recipient. By managing data traffic between connected devices, switches reduce network congestion and improve overall performance. They enable devices like computers, printers, and servers to communicate directly with each other within the network. For instance, in a corporate office, switches connect employees' computers, allowing for quick file sharing and access to shared resources like printers and servers.

#### Hubs

A `hub` is a basic (and now antiquated) networking device. It connects multiple devices in a network segment and broadcasts incoming data to all connected ports, regardless of the destination. Operating at the physical layer (Layer 1) of the OSI model, hubs are simpler than switches and do not manage traffic intelligently. This indiscriminate data broadcasting can lead to network inefficiencies and collisions, making hubs less suitable for modern networks. For example, in a small home network setup from earlier times, a hub might connect a few computers, but today, switches are preferred due to their better performance and efficiency.

## Network Media and Software Components

`Network Media and Software Components` are vital elements that enable seamless communication and operation within a network. `Network media`, such as cables and wireless signals, provide the physical pathways that connect devices and allow data to be transmitted between them. This includes wired media like Ethernet cables and fiber-optic cables, which offer high-speed connections, as well as wireless media like Wi-Fi and Bluetooth, which provide mobility and flexibility. On the other hand, `software components` like network protocols and management software define the rules and procedures for data transmission, ensuring that information is correctly formatted, addressed, transmitted, routed, and received. `Network protocols` such as TCP/IP, HTTP, and FTP enable devices to communicate over the network, while `network management software` allows administrators to monitor network performance, configure devices, and enhance security through tools like software firewalls.

#### Cabling and Connectors

`Cabling and connectors` are the physical materials used to link devices within a network, forming the pathways through which data is transmitted. This includes the various types of cables mentioned previously, but also connectors like the RJ-45 plug, which is used to interface cables with network devices such as computers, switches, and routers. The quality and type of cabling and connectors can affect network performance, reliability, and speed. For example, in an office setting, Ethernet cables with RJ-45 connectors might connect desktop computers to network switches, enabling high-speed data transfer across the local area network.

#### Network Protocols

`Network protocols` are the set of rules and conventions that control how data is formatted, transmitted, received, and interpreted across a network. They ensure that devices from different manufacturers, and with varying configurations, can adhere to the same standard and communicate effectively. Protocols encompass a wide range of aspects. such as:

- `Data Segmentation`
- `Addressing`
- `Routing`
- `Error Checking`
- `Synchronization`

Common network protocols include:

- `TCP/IP`: ubiquitous across all internet communications

- `HTTP/HTTPS`: The standard for Web traffic

- `FTP`: File transfers

- `SMTP` : Email transmissions

For instance, when we browse a website, the HTTP or HTTPS protocol dictates how our browser communicates with the webserver to request and receive web pages, ensuring that the data is correctly formatted and securely transmitted.\`


#### Network Management Software

`Network management software` consists of tools and applications used to monitor, control, and maintain network components and operations. These software solutions provide functionalities for:

- `performance monitoring`
- `configuration management`
- `fault analysis`
- `security management`

They help network administrators ensure that the network operates efficiently, remains secure, and can quickly address any issues that arise. For example, in a corporate environment, the IT department might use network management software to oversee all devices connected to the company network, monitor traffic for unusual activity, update device configurations remotely, and enforce security policies, maintaining optimal network performance and security.

#### Software Firewalls

A `software firewall` is a security application installed on individual computers or devices that monitors and controls incoming and outgoing network traffic based on predetermined security rules. Unlike hardware firewalls that protect entire networks, software firewalls (also called Host-based firewalls) provide protection at the device level, guarding against threats that may bypass the network perimeter defenses. They help prevent unauthorized access, reject incoming packets that contain suspicious or malicious data, and can be configured to restrict access to certain applications or services. For example, most operating systems include a built-in software firewall that can be set up to block incoming connections from untrusted sources, ensuring that only legitimate network traffic reaches the device.

_**The Linux-based software firewall [IPTables](https://linux.die.net/man/8/iptables) being used to drop incoming ICMP traffic.**_![GIF showcasing the ping command against a host without a firewall and one with firewall enabled.](https://academy.hackthebox.com/storage/modules/289/Components_of_a_Network/software-firewall.gif)

* * *

## Servers

A `server` is a powerful computer designed to provide services to other computers, known as clients, over a network. Servers are the backbone behind websites, email, files, and applications. In the realm of computer networking, servers play a crucial role by hosting services that clients access—for example, web pages and email services—facilitating `service provision`. They enable `resource sharing` by allowing multiple users to access resources like files and printers. Servers also handle `data management` by storing and managing data centrally, which simplifies backup processes and enhances security management. Additionally, they manage `authentication` by controlling user access and permissions, across multiple components in the network. Servers often run specialized operating systems optimized for handling multiple, simultaneous requests in what is known as the `Client-Server Model`, where the server waits for requests from clients and responds accordingly. Whether you knew it or not, this is what was happening under-the-hood the last time you accessed a website from your notebook. Your browser sends a request to the web server hosting the site, and the server subsequently processes the request and sends back the web page data in its response.

* * *

## Conclusion

As we have seen, the technology stack needed for world-wide computer networking requires multiple components. End devices are the users' primary interface with the network, intermediary devices manage data traffic and connectivity, and servers provide resources and services. Together, they enable the seamless flow of information that powers modern communication.

Enable step-by-step solutions for all questions
![sparkles-icon-decoration](https://academy.hackthebox.com/images/sparkles-solid.svg)

#### Questions

Answer the question(s) below
to complete this Section and earn cubes!

\+ 0  What type of network cable is used to transmit data over long distances with minimal signal loss?


Submit


\+ 0  Which protocol manages data routing and delivery across networks?


Submit


\+ 0  What software is used to oversee and administer network operations? (Format: 3 words)


Submit


\+ 0  What software is used to protect individual devices from unauthorized network access? (Format: 1 word)


Submit


\+ 0  What type of cable is used to connect components within a local area network for high-speed data transfer?


Submit


\+ 0  Which device connects multiple networks and manages data traffic to optimize performance?


Submit


# Network Communication

* * *

For a network to function and facilitate comunication properly, there are three crucial components: `MAC addresses`, `IP addresses`, and `ports`. Together, these elements ensure that data is correctly sent and received between devices across both local and global networks, forming the backbone of seamless network communication.

* * *

## MAC Addresses

#### What is a MAC Address?

A `Media Access Control (MAC) address` is a unique identifier assigned to the network interface card (NIC) of a device, allowing it to be recognized on a local network. Operating at the `Data Link Layer (Layer 2)` of the OSI model, the MAC address is crucial for communication within a local network segment, ensuring that data reaches the correct physical device. Each MAC address is 48 bits long and is typically represented in hexadecimal format, appearing as six pairs of hexadecimal digits separated by colons or hyphens—for example, `00:1A:2B:3C:4D:5E`. The uniqueness of a MAC address comes from its structure: the first 24 bits represent the `Organizationally Unique Identifier (OUI)` assigned to the manufacturer, while the remaining 24 bits are specific to the individual device. This design ensures that every MAC address is globally unique, allowing devices worldwide to communicate without address conflicts.

_**The Windows [GETMAC](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/getmac) command will return the MAC address of every network interface card on the host.**_![GIF showcasing the getmac command to obtain the MAC address.](https://academy.hackthebox.com/storage/modules/289/network_communication/getmac-2.gif)

#### How MAC Addresses are Used in Network Communication

MAC addresses are fundamental for local communication within a local area network (LAN), as they are used to deliver data frames to the correct physical device. When a device sends data, it encapsulates the information in a frame containing the destination MAC address; network switches then use this address to forward the frame to the appropriate port. Additionally, the `Address Resolution Protocol (ARP)` plays a crucial role by mapping IP addresses to MAC addresses, allowing devices to find the MAC address associated with a known IP address within the same network. This mapping is bridging the gap between logical IP addressing and physical hardware addressing within the LAN.

Imagine two computers, Computer A (with an IP address of 192.168.1.2 - which we will discuss shortly) and Computer B (192.168.1.5), connected to the same network switch. Computer A has the MAC address `00:1A:2B:3C:4D:5E`, while Computer B's MAC address is `00:1A:2B:3C:4D:5F`. When Computer A wants to send data to Computer B, it first uses the Address Resolution Protocol (ARP) to discover Computer B's MAC address associated with its IP address. After obtaining this information, Computer A sends a data frame with the destination MAC address set to `00:1A:2B:3C:4D:5F`. The switch receives this frame and forwards it to the specific port where Computer B is connected, ensuring that the data reaches the correct device. This is illustrated in the following diagram.

![Network diagram with a router connected to devices at IPs 192.168.1.2, 192.168.1.3, 192.168.1.4, and 192.168.1.5. The router requests a MAC address from 192.168.1.5 and sends MAC address 00:1A:2B:3C:4D:5F.](https://academy.hackthebox.com/storage/modules/289/network_communication/ARP-1.png)

* * *

## IP Addresses

#### What is an IP Address?

An `Internet Protocol (IP) address` is a numerical label assigned to each device connected to a network that utilizes the Internet Protocol for communication. Functioning at the `Network Layer (Layer 3)` of the OSI model, IP addresses enable devices to locate and communicate with each other across various networks. There are two versions of IP addresses: `IPv4` and `IPv6`. IPv4 addresses consist of a 32-bit address space, typically formatted as four decimal numbers separated by dots, such as `192.168.1.1`. In contrast, IPv6 addresses, which were developed to address the depletion of IPv4 addresses, have a 128-bit address space and are formatted in eight groups of four hexadecimal digits, an example being `2001:0db8:85a3:0000:0000:8a2e:0370:7334`.

#### How IP Addresses are Used in Network Communication

Routers use IP addresses to determine the optimal path for data to reach its intended destination across interconnected networks. Unlike MAC addresses, which are permanently tied to the device's network interface card, IP addresses are more flexible; they can change and are assigned based on the network topology and policies. A communication example between two devices on the same network can be similarly illustrated as shown previously in the MAC Address subsection.

* * *

## Ports

A `port` is a number assigned to specific processes or services on a network to help computers sort and direct network traffic correctly. It functions at the `Transport Layer (Layer 4)` of the OSI model and works with protocols such as TCP and UDP. Ports facilitate the simultaneous operation of multiple network services on a single IP address by differentiating traffic intended for different applications.

When a client application initiates a connection, it specifies the destination port number corresponding to the desired service. Client applications are those who request data or services, while server applications respond to those requests and provide the data or services. The operating system then directs the incoming traffic to the correct application based on this port number. Consider a simple example where a user accesses a website: the user’s browser initiates a connection to the server's IP address on port 80, which is designated for HTTP. The server, listening on this port, responds to the request. If the user needs to access a secure site, the browser instead connects to port 443, the standard for HTTPS, ensuring secure communication. Port numbers range from `0` to `65535`, and it is divided into three main categories, each serving a specific function.

_**Using the [netstat](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/netstat) tool to view active connections and listening ports.**_![GIF showcasing the netstat command to display active connections and listening ports.](https://academy.hackthebox.com/storage/modules/289/network_communication/tcp-ports.gif)

#### Well-Known Ports (0-1023):

`Well-known ports`, numbered from 0 to 1023, are reserved for common and universally recognized services and protocols, as standardized and managed by the [Internet Assigned Numbers Authority (IANA)](https://www.iana.org/). For instance, HTTP, which is the foundation of data communication for the World Wide Web, uses port 80, although browsers typically do not display this port number to simplify user experience. Similarly, HTTPS uses port 443 for secure communications over networks, and this port is also generally not displayed by browsers. Another example is FTP, which facilitates file transfers between clients and servers, using ports 20 and 21.

#### Registered Ports (1024-49151):

`Registered ports`, which range from 1024 to 49151, are not as strictly regulated as `well-known ports` but are still registered and assigned to specific services by the Internet Assigned Numbers Authority (IANA). These ports are commonly used for external services that users might install on a device. For instance, many database services, such as Microsoft SQL Server, use port 1433. Software companies frequently register a port for their applications to ensure that their software consistently uses the same port on any system. This registration helps in managing network traffic and preventing port conflicts across different applications.

#### Dynamic/Private Ports (49152-65535):

Dynamic or private ports, also known as ephemeral ports, range from 49152 to 65535 and are typically used by client applications to send and receive data from servers, such as when a web browser connects to a server on the internet. These ports are called `dynamic` because they are not fixed; rather, they can be randomly selected by the client's operating system as needed for each session. Generally used for temporary communication sessions, these ports are closed once the interaction ends. Additionally, dynamic ports can be assigned to custom server applications, often those handling short-term connections.

* * *

## Browsing the Internet Example

The following example represents the steps taken for a web request to reach the correct destination and return the information we seek.

#### 1\. DNS Lookup

Our computer resolves the domain name to an IP address (e.g., `93.184.216.34` for `example.com`).

#### 2\. Data Encapsulation

| **Step** |
| --- |
| Your browser generates an HTTP request. |
| The request is encapsulated with TCP, specifying the destination port `80` or `443`. |
| The packet includes the destination IP address `93.184.216.34`. |
| On the local network, our computer uses ARP to find the MAC address of the default gateway (router). |

#### 3\. Data Transmission

| **Step** |
| --- |
| The data frame is sent to the router's MAC address. |
| The router forwards the packet toward the destination IP address. |
| Intermediate routers continue forwarding the packet based on the IP address. |

#### 4\. Server Processing

| **Step** |
| --- |
| The server receives the packet and directs it to the application listening on port 80. |
| The server processes the HTTP request and sends back a response following the same path in reverse. |

#### 5\. Response Transmission

| **Step** |
| --- |
| The server sends the response back to the client’s temporary port, which was randomly selected by the client’s operating system at the start of the session. |
| The response follows the reverse path back through the network, being directed from router to router based on the source IP address and port information until it reaches the client. |

Enable step-by-step solutions for all questions
![sparkles-icon-decoration](https://academy.hackthebox.com/images/sparkles-solid.svg)

#### Questions

Answer the question(s) below
to complete this Section and earn cubes!

\+ 0  What protocol maps IP addresses to MAC addresses?


Submit


\+ 0  Which IP version uses 128-bit addressing?


Submit


\+ 0  At which layer of the OSI model do ports operate? (Format: two words)


Submit


\+ 0  What is the designated port number for HTTP?


Submit


\+ 0  What is the first step in the process of a web browsing session? (Format: two words)


Submit


# Dynamic Host Configuration Protocol (DHCP)

* * *

#### Introduction to DHCP

In a computer network, every device needs a unique IP (Internet Protocol) address to communicate with other devices. Manually assigning IP addresses to each device can be time-consuming and cause errors, especially in large networks. To resolve this issue, networks can rely on the Dynamic Host Configuration Protocol (DHCP). `DHCP` is a network management protocol used to automate the process of configuring devices on IP networks. It allows devices to automatically receive an IP address and other network configuration parameters, such as subnet mask, default gateway, and DNS servers, without manual intervention.

DHCP simplifies network management by automatically assigning IP addresses, significantly reducing the administrative workload. This automation ensures that each device connected to the network receives a unique IP address, preventing conflicts and duplication of addresses. Furthermore, DHCP recycles IP addresses that are no longer in use when devices disconnect from the network, optimizing the available address pool.

#### How DHCP Works

The DHCP process involves a series of interactions between the client (the device requesting an IP address) and the DHCP server (the service running on a network device that assigns IP addresses). This process is often referred to as `DORA`, an acronym for `Discover`, `Offer`, `Request`, and `Acknowledge`. Below we see a breakdown of DORA. Before we explore the `DORA` steps in detail, let's first clarify the roles of the `DHCP server` and the `DHCP client`:

| **Role** | **Description** |
| --- | --- |
| `DHCP Server` | A network device (like a router or dedicated server) that manages IP address allocation. It maintains a pool of available IP addresses and configuration parameters. |
| `DHCP Client` | Any device that connects to the network and requests network configuration parameters from the DHCP server. |

Below, we break down each step of the DORA process:

| **Step** | **Description** |
| --- | --- |
| `1. Discover` | When a device connects to the network, it broadcasts a **DHCP Discover** message to find available DHCP servers. |
| `2. Offer` | DHCP servers on the network receive the discover message and respond with a **DHCP Offer** message, proposing an IP address lease to the client. |
| `3. Request` | The client receives the offer and replies with a **DHCP Request** message, indicating that it accepts the offered IP address. |
| `4. Acknowledge` | The DHCP server sends a **DHCP Acknowledge** message, confirming that the client has been assigned the IP address. The client can now use the IP address to communicate on the network. |

_**A Linux host, connected to a wireless network, initializes the DORA process.**_![GIF showcasing the process of connecting to a wireless network.](https://academy.hackthebox.com/storage/modules/289/DHCP/DORA-3.gif)

The IP address assignment via DHCP is not permanent but is instead issued with a specific lease time. For instance, a DHCP server might assign an IP address to a smartphone with a lease time of 24 hours. After this period, the smartphone must request a renewal of the lease to continue using the IP address. Regarding the renewal process, before the lease expires, the client must proactively attempt to renew its IP address lease. This involves sending a renewal request to the DHCP server. As the lease nears its expiration, the client communicates with the DHCP server, asking if it can continue using the assigned IP address, to which the server can respond affirmatively, extending the lease.

#### Example Scenario

Let's walk through a simple example, based on the steps previously discussed, of how DHCP assigns an IP address to a device: Alice brings her new laptop to the office and connects it to the network. Since the laptop doesn't have an IP address yet, it sends out a DHCP Discover message to find a DHCP server. The office's DHCP server receives this message and responds with an offer, proposing the IP address 192.168.1.10. Alice's laptop receives this offer and sends back a DHCP Request message to accept the IP address. Finally, the DHCP server acknowledges this request and confirms the assignment. The laptop is now configured with the IP address 192.168.1.10, allowing it to communicate on the network.

The IP address 192.168.1.10 assigned to Alice's laptop is not permanent but is instead provided for a specific duration, known as the lease time. As this lease nears expiration, Alice's laptop must renew it to continue using the IP address. To do this, it sends another DHCP Request to the DHCP server asking to extend the lease. If the server can renew the lease, it will respond with a DHCP Acknowledge message, confirming the continued use of the IP address.

![DHCP process: PC sends DHCP Discover, server replies with DHCP Offer, PC sends DHCP Request, server acknowledges with DHCP Acknowledge. Lease renewal involves DHCP Request and Acknowledge.](https://academy.hackthebox.com/storage/modules/289/DHCP/DHCP-2.png)

Enable step-by-step solutions for all questions
![sparkles-icon-decoration](https://academy.hackthebox.com/images/sparkles-solid.svg)

#### Questions

Answer the question(s) below
to complete this Section and earn cubes!

\+ 0  What protocol automates IP address configuration for devices on a network?


Submit


\+ 0  What acronym describes the sequence of messages exchanged during the DHCP process?


Submit


\+ 0  What type of message does a client send to accept an IP address from a DHCP server?


Submit


# Network Address Translation (NAT)

* * *

The Internet relies on a system of numerical addresses, known as IP addresses, to route data from one device to another. The original addressing scheme, IPv4, offers a finite number of IP addresses (approximately 4.3 billion). Although this might sound like a lot, the explosive growth of the internet has meant these addresses are in short supply. One solution to this insufficiency issue is `Network Address Translation (NAT)`. The idea is that `NAT` allows multiple devices on a private network to share a single public IP address. This not only helps conserve the limited pool of public IP addresses but also adds a layer of security to the internal network.

#### Private vs. Public IP Addresses

`Public IP` addresses are globally unique identifiers assigned by Internet Service Providers (ISPs). Devices equipped with these IP addresses can be accessed from anywhere on the Internet, allowing them to communicate across the global network. For example, the IP address 8.8.8.8 is used for Google's DNS server, and 142.251.46.174 identifies one of Google’s web servers. These addresses ensure that devices can uniquely identify and reach each other over the internet.

`Private IP` addresses are designated for use within local networks such as homes, schools, and offices. These addresses are not routable on the global internet, meaning packets sent to these addresses are not forwarded by internet backbone routers. Defined by RFC 1918, common IPv4 private address ranges include 10.0.0.0 to 10.255.255.255, 172.16.0.0 to 172.31.255.255, and 192.168.0.0 to 192.168.255.255. This setup ensures that these private networks operate independently of the internet while facilitating internal communication and device connectivity.

Private IP addresses contribute to conserving public IP addresses. Using Network Address Translation (NAT), a local network can utilize private IP addresses while sharing a single public IP address, reducing the number of public IPs needed. This setup makes devices accessible from the internet without using multiple public addresses. Additionally, private IPs help secure the network by isolating internal devices from direct exposure to the internet, protecting them from potential external threats.

#### What is NAT?

`Network Address Translation (NAT)` is a process carried out by a router or a similar device that modifies the source or destination IP address in the headers of IP packets as they pass through. This modification is used to translate the private IP addresses of devices within a local network to a single public IP address that is assigned to the router.

#### How NAT Works

Consider a home network with several devices, such as a laptop, a smartphone, and a gaming console, each assigned a unique private IP address: the laptop at 192.168.1.10, the smartphone at 192.168.1.11, and the gaming console at 192.168.1.12. The home router managing this network has two critical interfaces. The LAN (Local Area Network) interface connects to the private network with an IP address of 192.168.1.1, while the WAN (Wide Area Network) interface, connected to the ISP’s network, carries a public IP address, 203.0.113.50.

The process of NAT translation begins when a device, say the laptop, sends a request to visit a website like [www.google.com](http://www.google.com). This request packet, originating with the private IP of 192.168.1.10, is sent to the router. Here, the NAT function of the router modifies the source IP in the packet header from the private IP to the public IP of the router, 203.0.113.50. This packet then travels across the internet to reach the intended web server. Upon receiving the packet, the web server sends a response back to the router's public IP. As the response arrives, the router's NAT table, which keeps track of IP mappings, identifies that 203.0.113.50:4444 corresponds to the laptop at 192.168.1.10:5555 (ports 4444 and 5555 are dynamic). The router then translates the public IP back to the laptop’s private IP and forwards the internal response to the laptop, completing the communication cycle.

![Network diagram: LAN with PC, printer, smartphone, and laptop (private IPs 192.168.1.10 to 192.168.1.13) connected to a router/NAT with public IP 203.0.113.50, linked to a remote server with public IP 503.0.135.60. NAT modifies host and destination IPs.](https://academy.hackthebox.com/storage/modules/289/NAT/NAT-2.png)

#### Types of NAT

To better understand Network Address Translation (NAT), It's helpful to know that there are several types of Network Address Translation (NAT), each designed for specific networking needs. Below are the different types of NAT.

| **Type** | **Description** |
| --- | --- |
| `Static NAT` | Involves a one-to-one mapping, where each private IP address corresponds directly to a public IP address. |
| `Dynamic NAT` | Assigns a public IP from a pool of available addresses to a private IP as needed, based on network demand. |
| `Port Address Translation (PAT)` | Also known as NAT Overload, is the most common form of NAT in home networks. Multiple private IP addresses share a single public IP address, differentiating connections by using unique port numbers. This method is widely used in home and small office networks, allowing multiple devices to share a single public IP address for internet access. |

#### Benefits and Trade-Offs

Network Address Translation (NAT) offers a number of benefits and presents some trade-offs as well.

| **Benefits** |
| --- |
| Conserves the limited IPv4 address space. |
| Provides a basic layer of security by not exposing internal network structure directly. |
| Flexible for internal IP addressing schemes. |

| **Trade-Offs** |
| --- |
| Complex services like hosting a public server behind NAT can require additional configuration (e.g., port forwarding). |
| NAT can break certain protocols that rely on end-to-end connectivity without special handling. |
| Adds complexity to troubleshooting connectivity issues. |

Enable step-by-step solutions for all questions
![sparkles-icon-decoration](https://academy.hackthebox.com/images/sparkles-solid.svg)

#### Questions

Answer the question(s) below
to complete this Section and earn cubes!

\+ 0  What type of NAT allows multiple private IP addresses to share one public IP address using unique port numbers?


Submit


\+ 0  What RFC specifies private IP ranges?


Submit


\+ 0  Which NAT type involves a one-to-one mapping of private IP addresses to public IP addresses?


Submit


\+ 0  What type of NAT assigns a public IP from a pool as needed?


Submit


\+ 0  What device typically performs NAT in a home network?


Submit


# Domain Name System (DNS)

* * *

The Domain Name System (DNS) is like the phonebook of the internet. It helps us find the right number (an IP address) for a given name (a domain such as `www.google.com`). Without DNS, we would need to memorize long, often complex IP addresses for every website we visit. DNS makes our lives easier by allowing us to use human-friendly names to access online resources.

#### Domain Names vs. IP Addresses

| **Address** | **Description** |
| --- | --- |
| `Domain Name` | A readable address like `www.example.com` that people can easily remember. |
| `IP Address` | A numerical label (e.g., `93.184.216.34` |

DNS bridges the gap between these two, so we can just type `www.google.com` without needing to remember the underlying IP address.

#### DNS Hierarchy

DNS is organized like a tree, starting from the root and branching out into different layers.

| **Layer** | **Description** |
| --- | --- |
| `Root Servers` | The top of the DNS hierarchy. |
| `Top-Level Domains (TLDs)` | Such as `.com`, `.org`, `.net`, or country codes like `.uk`, `.de`. |
| `Second-Level Domains` | For example, `example` in `example.com`. |
| `Subdomains or Hostname` | For instance, `www` in `www.example.com`, or `accounts` in `accounts.google.com`. |

![URL breakdown: Scheme, Subdomains, 2nd-Level Domain, Top-Level Domain, Page name, Root.](https://academy.hackthebox.com/storage/modules/289/DNS/DNS-2.png)

#### DNS Resolution Process (Domain Translation)

When we enter a domain name in our browser, the computer needs to find the corresponding IP address. This process is known as `DNS resolution` or `domain translation`. The steps below show how this process works.

| **Step** | **Description** |
| --- | --- |
| `Step 1` | We type `www.example.com` into our browser. |
| `Step 2` | Our computer checks its local DNS cache (a small storage area) to see if it already knows the IP address. |
| `Step 3` | If not found locally, it queries a `recursive DNS server`. This is often provided by our Internet Service Provider or a third-party DNS service like Google DNS. |
| `Step 4` | The recursive DNS server contacts a `root server`, which points it to the appropriate `TLD name server` (such as the `.com` domains, for instance). |
| `Step 5` | The TLD name server directs the query to the `authoritative name server` for `example.com`. |
| `Step 6` | The authoritative name server responds with the IP address for `www.example.com`. |
| `Step 7` | The recursive server returns this IP address to your computer, which can then connect to the website’s server directly. |

This all happens in just fractions of a second. Below we can see a simple example of the Domain Translation process. Suppose you want to visit the website at `www.example.com`. Without the Domain Name System (DNS), we would need to know and type the IP address, such as `93.184.216.34`, every time you want to access that site. With DNS in place, we can simply type `www.example.com` into our browser. Behind the scenes, DNS automatically finds and translates this domain name into the correct IP address for us, ensuring a seamless connection to the website. The diagram below illustrates the diagram of the `DNS Query Process`.

![DNS query process: Personal computer requests www.example.com'sl IP from Recursive DNS Server, which queries Root Server, then TLD Server, and finally Authoritative DNS, receiving IP 93.184.216.34.](https://academy.hackthebox.com/storage/modules/289/DNS/DNS_Query_Process-2.png)

Enable step-by-step solutions for all questions
![sparkles-icon-decoration](https://academy.hackthebox.com/images/sparkles-solid.svg)

#### Questions

Answer the question(s) below
to complete this Section and earn cubes!

\+ 0  What type of domain is \`.com\` considered as? (Format: Three words, example: One-Two Three)


Submit


\+ 0  In the domain \`www.example.com\`, what is \`example\` called?


Submit


\+ 0  What is checked first in the DNS resolution process when you enter a domain name into a browser? (Format: Two words)


Submit


\+ 0  What type of DNS server is typically provided by an Internet Service Provider?


Submit


\+ 0  Which server directs the recursive DNS server to the appropriate TLD name server?


Submit


\+ 0  What numerical label uniquely identifies a device on a network?


Submit


\+ 0  In the URL "accounts.google.com", what is \`accounts\` considered as?


Submit


# Internet Architecture

* * *

`Internet Architecture` describes how data is organized, transmitted, and managed across networks. Different architectural models serve different needs—some offer a straightforward client-server setup (like a website), while others rely on a more distributed approach (like file-sharing platforms). Understanding these models helps us see why networks are designed and operated the way they are. Different architectures solve different problems. Often, we see a combination of architectures creating hybrid models. Each model comes with its own set of trade-offs in terms of scalability, performance, security, and manageability. In the following paragraphs, we will describe the different architectures in more detail.

* * *

## Peer-to-Peer (P2P) Architecture

In a `Peer-to-Peer (P2P`) network, each node, whether it's a computer or any other device, acts as both a client and a server. This setup allows nodes to communicate directly with each other, sharing resources such as files, processing power, or bandwidth, without the need for a central server. P2P networks can be fully decentralized, with no central server involved, or partially centralized, where a central server may coordinate some tasks but does not host data.

Imagine a group of friends who want to share vacation photos with each other. Instead of uploading all the photos to a single website or server, each of them sets up a folder on their own computer that can be accessed by the others. They use a file-sharing program that connects their computers directly.

First, they install a Peer-to-Peer (P2P) file-sharing application on their computer. Then, they select the folder containing the vacation photos to share with the other friends. Everyone performs the same setup on their computers. Once everyone is connected through the P2P application, they can all browse and download photos directly from each other’s shared folders, allowing for a direct exchange of files without the need for a central server.

A popular example of Peer-to-Peer (P2P) architecture is torrenting, as seen with applications like BitTorrent. In this system, anyone who has the file, referred to as a `seeder`, can upload it, allowing others to download it from multiple sources simultaneously.

![Network diagram with interconnected devices: PC, laptop, smartphone, server, and printer.](https://academy.hackthebox.com/storage/modules/289/Internet_Arch_Models/P2P-1.png)

In the following table, we can see the advantages and disadvantages of a Peer-to-Peer architecture.

| **Advantage** | **Description** |
| --- | --- |
| `Scalability` | Adding more nodes can increase total resources (storage, CPU, etc.). |
| `Resilience` | If one node goes offline, others can continue functioning. |
| `Cost distribution` | Resource burden, like bandwidth and storage, is distributed among peers, making it more cost-efficient. |

| **Disadvantage** | **Description** |
| --- | --- |
| `Management complexity` | Harder to control and manage updates/security policies across all nodes |
| `Potential reliability issues` | If too many peers leave, resources could be unavailable. |
| `Security challenges` | Each node is exposed to potential vulnerabilities. |

* * *

## Client-Server Architecture

The `Client-Server` model is one of the most widely used architectures on the Internet. In this setup, clients, which are user devices, send requests, such as a web browser asking for a webpage, and servers respond to these requests, like a web server hosting the webpage. This model typically involves centralized servers where data and applications reside, with multiple clients connecting to these servers to access services and resources.

Let's assume we want to check the weather forecast on a website. We start by opening the web browser on our phone or computer, and proceed to type in the website's name, e.g., `weatherexample.com`. When we press enter, the browser sends a request over the Internet to the server that hosts `weatherexample.com`. This server, a powerful computer set up specifically to store the website’s data and handle requests, receives the query and processes it by locating the requested page. It then sends back the data (regarding the weather, we requested) to our browser, which receives this information and displays the webpage, allowing us to see the latest weather updates.

![Network diagram with Internet connected to clients (PC, laptop, smartphone) and servers.](https://academy.hackthebox.com/storage/modules/289/Internet_Arch_Models/Client_Server_Arch-1.png)

A key component of this architecture is the tier model, which organizes server roles and responsibilities into layers. This enhances scalability and manageability, as well as security and performance.

#### Single-Tier Architecture

In a `single-tier` architecture, the client, server, and database all reside on the same machine. This setup is straightforward but is rarely used for large-scale applications due to significant limitations in scalability and security.

#### Two-Tier Architecture

The `two-tier` architecture splits the application environment into a client and a server. The client handles the presentation layer, and the server manages the data layer. This model is typically seen in desktop applications where the user interface is on the user's machine, and the database is on a server. Communication usually occurs directly between the client and the server, which can be a database server with query-processing capabilities.

**Note:** In a typical web application, the client (browser) does not directly interact with the database server. Instead, the browser requests web pages from a \*\*web server\*\*, which in turn sends it's response (HTML, CSS, JavaScript) back to the browser for rendering. The web server \*may\* interact with an application server or database in order to formulate it's response, but in general, the scenario of a person visiting a website does not constitute a Two-Tier Architecture.

#### Three-Tier Architecture

A `three-tier` architecture introduces an additional layer between the client and the database server, known as the application server. In this model, the client manages the presentation layer, the application server handles all the business logic and processing, and the third tier is a database server. This separation provides added flexibility and scalability because each layer can be developed and maintained independently.

#### N-Tier Architecture

In more complex systems, an `N-tier` architecture is used, where `N` refers to any number of separate tiers used beyond three. This setup involves multiple levels of application servers, each responsible for different aspects of business logic, processing, or data management. N-tier architectures are highly scalable and allow for distributed deployment, making them ideal for web applications and services that demand robust, flexible solutions.

While tiered client-server architectures offer many improvements, they also introduce complexity in deployment and maintenance. Each tier needs to be correctly configured and secured, and communication between tiers must be efficient and secure to avoid performance bottlenecks and security vulnerabilities. In the following table, we can see the advantages and disadvantages of a Client-Server architecture in general.

| **Advantage** | **Description** |
| --- | --- |
| `Centralized control` | Easier to manage and update. |
| `Security` | Central security policies can be applied. |
| `Performance` | Dedicated servers can be optimized for their tasks. |

| **Disadvantage** | **Description** |
| --- | --- |
| `Single point of failure` | If the central server goes down, clients lose access. |
| `High Cost and Maintenance` | Setting up and sustaining a client-server architecture is expensive, requiring constant operation and expert management , making it costly to maintain. |
| `Network Congestion` | High traffic on the network can lead to congestion, slowing down or even disrupting connections when too many clients access the server simultaneously. |

* * *

## Hybrid Architecture

A `Hybrid` model blends elements of both `Client-Server` and `Peer-to-Peer (P2P)` architectures. In this setup, central servers are used to facilitate coordination and authentication tasks, while the actual data transfer occurs directly between peers. This combination leverages the strengths of both architectures to enhance efficiency and performance. The following example gives a high-level explanation of how a hybrid architecture works.

When we open a video conferencing app and log in, the credentials (username and password) are verified by central servers, which also manage the session by coordinating who is in the meeting and controlling access. Once we're logged in and the meeting begins, the actual video and audio data is transferred directly between our device and those of other participants, bypassing the central server to reduce lag and enhance video quality. This setup combines both models: it uses the central server for initial connection and control tasks, while the bulk of data transfer occurs in a peer-to-peer style, reducing the server load and leveraging direct, fast connections between peers. The following table refers to some of the advantages and disadvantages of a Hybrid Architecture.

![Network diagram with Internet connected to multiple devices: PC, laptop, smartphone, and server.](https://academy.hackthebox.com/storage/modules/289/Internet_Arch_Models/Hybrid_Architecture-1.png)

| **Advantage** | **Description** |
| --- | --- |
| `Efficiency` | Relieves workload from servers by letting peers share data. |
| `Control` | Central server can still manage user authentication, directory services, or indexing. |

| **Disadvantage** | **Description** |
| --- | --- |
| `Complex Implementation` | Requires more sophisticated design to handle both centralized and distributed components. |
| `Potential Single Point of Failure` | If the central coordinating server fails, peer discovery might stop. |

* * *

## Cloud Architecture

`Cloud Architecture` refers to computing infrastructure that is hosted and managed by third-party providers, such as AWS, Azure, and Google Cloud. This architecture operates on a virtualized scale following a client-server model. It provides on-demand access to resources such as servers, storage, and applications, all accessible over the Internet. In this model, users interact with these services without controlling the underlying hardware.

![Cloud network diagram with components: Servers, Apps, Database, Storage connected to Internet, linking to devices: Laptop, PC, Smartphone.](https://academy.hackthebox.com/storage/modules/289/Internet_Arch_Models/Cloud_Arch-1.png)

Services like Google Drive or Dropbox are some examples of Cloud Architecture operating under the `SaaS` (Software as a Service) model, where we access applications over the internet without managing the underlying hardware. Below are five essential characteristics that define a Cloud Architecture.

| **Characteristic** | **Description** |
| --- | --- |
| `1. On-demand self-service` | Automatically set up and manage the services without human help. |
| `2. Broad network access` | Access services from any internet-connected device. |
| `3. Resource pooling` | Share and allocate service resources dynamically among multiple users. |
| `4. Rapid elasticity` | Quickly scale services up or down based on demand. |
| `5. Measured service` | Only pay for the resources you use, tracked with precision. |

The below table shows some of the advantages and disadvantages of the Cloud Architecture.

| **Advantage** | **Description** |
| --- | --- |
| `Scalability` | Easily add or remove computing resources as needed. |
| `Reduced cost & maintenance` | Hardware managed by the cloud provider. |
| `Flexibility` | Access services from anywhere with Internet connectivity. |

| **Disadvantage** | **Description** |
| --- | --- |
| `Vendor lock-in` | Migrating from one cloud provider to another can be complex. |
| `Security/Compliance` | Relying on a third party for data hosting can introduce concerns about data privacy. |
| `Connectivity` | Requires stable Internet access. |

* * *

## 6\. Software-Defined Architecture (SDN)

`Software-Defined Networking (SDN)` is a modern networking approach that separates the control plane, which makes decisions about where traffic is sent, from the data plane, which actually forwards the traffic. Traditionally, network devices like routers and switches housed both of these planes. However, in SDN, the control plane is centralized within a software-based controller. This configuration allows network devices to simply execute instructions they receive from the controller. SDN provides a programmable network management environment, enabling administrators to dynamically adjust network policies and routing as required. This separation makes the network more flexible and improves how it's managed.

![Network diagram: Remote Servers connect to Internet, then SDN Switches, SDN Controller, and Users, linking to Laptop, PC, Smartphone.](https://academy.hackthebox.com/storage/modules/289/Internet_Arch_Models/Software-Defined_Arch-1.png)

Large enterprises or cloud providers use SDN to dynamically allocate bandwidth and manage traffic flows according to real-time demands. Below is a table with the advantages and disadvantages of the Software-Defined architecture.

| **Advantage** | **Description** |
| --- | --- |
| `Centralized control` | Simplifies network management. |
| `Programmability & Automation` | Network configurations can be changed quickly through software instead of manually configuring each device. |
| `Scalability & Efficiency` | Can optimize traffic flows dynamically, leading to better resource utilization. |

| **Disadvantage** | **Description** |
| --- | --- |
| `Controller Vulnerability` | If the central controller goes down, the network might be adversely affected. |
| `Complex Implementation` | Requires new skill sets and specialized software/hardware. |

* * *

## Key Comparisons

Below is a comparison table that outlines key characteristics of different network architectures

| `Architecture` | `Centralized` | `Scalability` | `Ease of Management` | `Typical Use Cases` |
| --- | --- | --- | --- | --- |
| `P2P` | Decentralized (or partial) | High (as peers grow) | Complex (no central control) | File-sharing, blockchain |
| `Client-Server` | Centralized | Moderate | Easier (server-based) | Websites, email services |
| `Hybrid` | Partially central | Higher than C-S | More complex management | Messaging apps, video conferencing |
| `Cloud` | Centralized in provider’s infra | High | Easier (outsourced) | Cloud storage, SaaS, PaaS |
| `SDN` | Centralized control plane | High (policy-driven) | Moderate (needs specialized tools) | Datacenters, large enterprises |

* * *

## Conclusion

Each architecture has its unique benefits and challenges, and in practice, we often see these models blended to balance performance, scalability, and cost. Understanding these distinctions is important for anyone planning to set up or improve network systems.

Enable step-by-step solutions for all questions
![sparkles-icon-decoration](https://academy.hackthebox.com/images/sparkles-solid.svg)

#### Questions

Answer the question(s) below
to complete this Section and earn cubes!

\+ 0  What type of architecture allows nodes to act as both client and server?


Submit


\+ 0  What architecture combines elements of both Client-Server and Peer-to-Peer models?


Submit


\+ 0  Which cloud service model involves accessing applications over the internet without managing the underlying infrastructure?


Submit


\+ 0  In which architecture is the control plane separated from the data plane? (Format: two words, one of which is hyphenated)


Submit


\+ 0  Which architecture is known for decentralized data sharing without a central server?


Submit


\+ 0  What model is used by video conferencing apps to combine centralized coordination with peer-to-peer data transfer?


Submit


# Wireless Networks

* * *

A `wireless network` is a sophisticated communication system that employs radio waves or other wireless signals to connect various devices such as computers, smartphones, and IoT gadgets, enabling them to communicate and exchange data without the need for physical cables. This technology allows devices to connect to the internet, share files, and access services seamlessly over the air, offering flexibility and convenience in personal and professional environments.

| **Advantages** | **Description** |
| --- | --- |
| `Mobility` | Users can move around freely within the coverage area. |
| `Ease of installation` | No need for extensive cabling. |
| `Scalability` | Adding new devices is simpler than a wired network. |

| **Disadvantages** | **Description** |
| --- | --- |
| `Interference` | Wireless signals can be disrupted by walls, other electronics, or atmospheric conditions. |
| `Security risks` | Without proper security measures, wireless transmissions can be easier to intercept. |
| `Speed limitations` | Generally, wireless connections are slower compared to wired connections of the same generation. |

* * *

## Wireless Router

A `router` is a device that forwards data packets between computer networks. In a home or small office setting, a `wireless router` combines the functions of:

| **Function** | **Description** |
| --- | --- |
| `Routing` | Directing data to the correct destination (within your network or on the internet). |
| `Wireless Access Point` | Providing Wi-Fi coverage. |

For example, at home, our smartphones, laptops, and smart TVs all connect wirelessly to our router. The router is plugged into a modem that brings internet service from the ISP (Internet Service Provider). Below are the main components of a wireless router.

| **Component** | **Description** |
| --- | --- |
| `WAN (Wide Area Network) Port` | Connects to your internet source (e.g., a cable modem). |
| `LAN (Local Area Network) Ports` | For wired connections to local devices (e.g., desktop computer, printer). |
| `Antennae` | Transmit and receive wireless signals. (Some routers have internal antennae.) |
| `Processor & Memory` | Handle routing and network management tasks. |

* * *

## Mobile Hotspot

A `mobile hotspot` allows a smartphone (or other hotspot devices) to share its cellular data connection via Wi-Fi. Other devices (laptops, tablets, etc.) then connect to this hotspot just like they would to a regular Wi-Fi network. A mobile hotspot uses cellular data, connecting devices to the internet via a cellular network, such as 4G or 5G. The range of a hotspot is typically limited to just a few meters. Running a hotspot can also significantly drain the battery of the device creating the hotspot. For security, access to the hotspot is usually protected by a password, similar to the security measures used for a home Wi-Fi network. To better understand this concept, we can imagine that we are traveling and don’t have access to public Wi-Fi. We can activate the hotspot on our phone and connect our laptop to our phone’s Wi-Fi signal to browse the internet.

* * *

## Cell Tower

A `cell tower` (or `cell site`) is a structure where antennas and electronic communications equipment are placed to create a cellular network cell. This `cell` in a cellular network refers to the specific area of coverage provided by a single cell tower, which is designed to seamlessly connect with adjacent cells created by other towers. Each tower covers a certain geographic area, allowing mobile phones (and other cellular-enabled devices) to send and receive signals.

Cell towers function through a combination of radio transmitters and receivers, which are equipped with antennas to communicate over specific radio frequencies. These towers are managed by Base Station Controllers (BSC), which oversee the operation of multiple towers. BSCs handle the transfer of calls and data sessions from one tower to another when users move across different cells. Finally, these towers are connected to the core network via backhaul links, which are typically fiber optic or microwave links.

Cell towers are differentiated by their coverage capacities and categorized primarily into `macro cells` and `micro/small cells`. Macro cells consist of large towers that provide extensive coverage over several kilometers, making them ideal for rural areas where wide coverage is necessary. On the other hand, micro and small cells are smaller installations typically located in urban centers. These towers are placed in densely populated areas and fill the coverage gaps left by macro cells. To better understand the concept of a cellular network, imagine we are on a road trip, streaming music on the phone. As we move, our phone switches from one cell tower to the next to maintain connection.

* * *

## Frequencies in Wireless Communications

As mentioned earlier, wireless communications utilize radio waves to enable devices to connect and communicate with each other. These radio waves are emitted at specific frequencies, known as oscillation rates, which are measured in hertz (Hz). Common frequency bands for wireless networks include:

| **Frequency Bands** |
| --- |
| `1.` **2.4 GHz (Gigahertz)** – Used by older Wi-Fi standards (802.11b/g/n). Better at penetrating walls, but can be more prone to interference (e.g., microwaves, Bluetooth). |
| `2.` **5 GHz** – Used by newer Wi-Fi standards (802.11a/n/ac/ax). Faster speeds, but shorter range. |
| `3.` **Cellular Bands** – For 4G (LTE) and 5G. These range from lower frequencies (700 MHz) to mid-range (2.6 GHz) and even higher frequencies for some 5G services (up to 28 GHz and beyond). |

Different frequencies play crucial roles in wireless communication due to their varying characteristics and the trade-offs between range and speed. Lower frequencies tend to travel farther but are limited in the amount of data they can carry, making them suitable for broader coverage with less data demand. In contrast, higher frequencies, while capable of carrying more data, have a much shorter range. Additionally, frequency bands can get congested as many devices operate on the same frequencies, leading to interference that can degrade performance. To manage and mitigate these issues, government agencies such as the FCC in the U.S. regulate frequency allocations, ensuring orderly use of the airwaves and preventing interference among users.

Different frequencies are important in wireless communication because they affect how far and how fast data travels. Lower frequencies have longer range but carry less data, while higher frequencies can carry more data but have a shorter range. Additionally, congestion from many devices using the same frequency can cause interference. To prevent this, government agencies like the FCC regulate how frequencies are used.

* * *

## Summarizing

On a typical day, we might use several forms of wireless technology. At home, our wireless router provides internet access via Wi-Fi at both 2.4 GHz and 5 GHz frequencies to devices like our phone and laptop. When leave home, our phone automatically connects to the internet using the nearest cell tower over 4G or 5G networks. While traveling abroad, we can turn on our phone’s mobile hotspot to share our cellular data with a friend’s laptop. Throughout these activities, we engage with three key wireless technologies: Wi-Fi for local wireless access, cellular networks for wide-area coverage, and a mobile hotspot for personal data sharing.

Enable step-by-step solutions for all questions
![sparkles-icon-decoration](https://academy.hackthebox.com/images/sparkles-solid.svg)

#### Questions

Answer the question(s) below
to complete this Section and earn cubes!

\+ 0  What type of waves do wireless networks use to connect devices? (Format: two words)


Submit


\+ 0  What device combines the functions of routing and providing Wi-Fi coverage in a home network? (Format: two words)


Submit


\+ 0  What is used by a mobile hotspot to connect devices to the internet? (Format: two words)


Submit


\+ 0  What structure supports antennas and communications equipment to create cellular network coverage? (Format: two words)


Submit


\+ 0  What manages multiple cell towers in cellular networks? (Format: three words)


Submit


\+ 0  Which frequency band is known for better wall penetration but more prone to interference?


Submit


# Network Security

* * *

In networking, the term security refers to the measures taken to protect data, applications, devices, and systems within this network from unauthorized access or damage. The goal is to uphold and maintain the `CIA triad`:

| **Principle** | **Description** |
| --- | --- |
| `Confidentiality` | Only authorized users can view the data. |
| `Integrity` | The data remains accurate and unaltered. |
| `Availability` | Network resources are accessible when needed. |

In the next paragraphs, we will discuss two critical components of network security: `Firewalls` and `Intrusion Detection/Prevention Systems (IDS/IPS)`.

* * *

## Firewalls

A `Firewall` is a network security device, either hardware, software, or a combination of both, that monitors incoming and outgoing network traffic. Firewalls enforce a set of rules (known as `firewall policies` or `access control lists`) to determine whether to `allow` or `block` specific traffic. We can imagine a firewall as a security guard at the entrance of a building, checking who is allowed in or out based on a list of rules. If a visitor doesn’t meet the criteria (e.g., not on the guest list), they are denied entry.

_**The open source router/firewall [pfSense](https://www.pfsense.org/). It's large number of plugins (known as "Packages") give it a range of capabilities.**_![GIF showcasing the firewall rule creation in pfSense.](https://academy.hackthebox.com/storage/modules/289/Internet_Security/pfsense.gif)

Firewalls operate by analyzing packets of data according to predefined rules and policies, commonly focusing on factors such as IP addresses, port numbers, and protocols. This process, known as traffic filtering, is defined by system administrators as permitting or denying traffic based on specific conditions, ensuring that only authorized connections are allowed. Additionally, firewalls can log traffic events and generate alerts about any suspicious activity. Below are some of the different types of firewalls.

#### 1\. Packet Filtering Firewall

| **Description** |
| --- |
| Operates at Layer 3 (Network) and Layer 4 (Transport) of the OSI model. |
| Examines source/destination IP, source/destination port, and protocol type. |
| `Example`: A simple router ACL that only allows HTTP (port 80) and HTTPS (port 443) while blocking other ports. |

#### 2\. Stateful Inspection Firewall

| **Description** |
| --- |
| Tracks the state of network connections. |
| More intelligent than packet filters because they understand the entire conversation. |
| `Example`: Only allows inbound data that matches an already established outbound request. |

#### 3\. Application Layer Firewall (Proxy Firewall)

| **Description** |
| --- |
| Operates up to Layer 7 (Application) of the OSI model. |
| Can inspect the actual content of traffic (e.g., HTTP requests) and block malicious requests. |
| `Example`: A web proxy that filters out malicious HTTP requests containing suspicious patterns. |

#### 4\. Next-Generation Firewall (NGFW)

| **Description** |
| --- |
| Combines stateful inspection with advanced features like deep packet inspection, intrusion detection/prevention, and application control. |
| `Example`: A modern firewall that can block known malicious IP addresses, inspect encrypted traffic for threats, and enforce application-specific policies. |

Firewalls stand between the internet and the internal network, examining traffic before letting it through. In a home environment, our router/modem often has a built-in firewall (software-based). In that case, it’s all in one device, and the firewall function is `inside` the router. In larger networks (e.g., business environments), the firewall is often a separate device placed after the modem/router and before the internal network, ensuring all traffic must pass through it.

![Network diagram: Internet connects to Firewall, then Router/Modem, linking to Laptop, PC, Smartphone.](https://academy.hackthebox.com/storage/modules/289/Internet_Security/Firewall-1.png)

* * *

## Intrusion Detection and Prevention Systems (IDS/IPS)

Intrusion Detection and Prevention Systems (IDS/IPS) are security solutions designed to monitor and respond to suspicious network or system activity. An Intrusion Detection System (IDS) observes traffic or system events to identify malicious behavior or policy violations, generating alerts but not blocking the suspicious traffic. In contrast, an Intrusion Prevention System (IPS) operates similarly to an IDS but takes an additional step by preventing or rejecting malicious traffic in real time. The key difference lies in their actions: an IDS detects and alerts, while an IPS detects and prevents.

_**The widely used [Suricata](https://suricata.io/) software can function as both an IDS and an IPS. Here, we see the user enable a detection rule, then begin inline monitoring.**_![GIF showcasing the rule enablement in Suricata.](https://academy.hackthebox.com/storage/modules/289/Internet_Security/suricata-2.gif)

Both IDS and IPS solutions analyze network packets and compare them to known attack signatures or typical traffic patterns. This process involves:

| **Techniques** | **Description** |
| --- | --- |
| `Signature-based detection` | Matches traffic against a database of known exploits. |
| `Anomaly-based detection` | Detects anything unusual compared to normal activity. |

When suspicious or malicious behavior is identified, an IDS will generate an alert for further investigation, while an IPS goes one step further by blocking or rejecting the malicious traffic in real time.

_**Suricata in IDS mode.**_![GIF showcasing Suricata in IDS mode.](https://academy.hackthebox.com/storage/modules/289/Internet_Security/suricata-3.gif)

Below are some of the different types of firewalls IDS/IPS.

#### 1\. Network-Based IDS/IPS (NIDS/NIPS)

| **Description** |
| --- |
| Hardware device or software solution placed at strategic points in the network to inspect all passing traffic. |
| `Example`: A sensor connected to the core switch that monitors traffic within a data center. |

#### 2\. Host-Based IDS/IPS (HIDS/HIPS)

| **Description** |
| --- |
| Runs on individual hosts or devices, monitoring inbound/outbound traffic and system logs for suspicious behavior on that specific machine. |
| `Example`: An antivirus or endpoint security agent installed on a server. |

IDS/IPS can be placed at several strategic locations in a network. One option is to position them behind the firewall, where the firewall filters obvious threats, and the IDS/IPS inspects any remaining traffic. Another common placement is in the DMZ (Demilitarized Zone), a separate network segment within the larger network directly exposed to the internet, where they monitor traffic moving in and out of publicly accessible servers. Finally, IDS/IPS solutions can also run directly on endpoint devices, such as servers or workstations, to detect suspicious activity at the host level. The following diagram shows an IDS/IPS positioned after the firewall.

![Network diagram: Internet connects to Firewall, then IPS/IDS, Router/Modem, linking to Laptop, PC, Smartphone.](https://academy.hackthebox.com/storage/modules/289/Internet_Security/IPS_IDS-1.png)

* * *

## Best Practices

Here are the best practices for enhancing network security, summarized in the following table:

| **Practice** | **Description** |
| --- | --- |
| `Define Clear Policies` | Consistent firewall rules based on the principle of `least privilege` (only allow what is necessary). |
| `Regular Updates` | Keep firewall, IDS/IPS signatures, and operating systems up to date to defend against the latest threats. |
| `Monitor and Log Events` | Regularly review firewall logs, IDS/IPS alerts, and system logs to identify suspicious patterns early. |
| `Layered Security` | Use `defense in depth` (a strategy that leverages multiple security measures to slow down an attack) with multiple layers: Firewalls, IDS/IPS, antivirus, and endpoint protection to cover different attack vectors. |
| `Periodic Penetration Testing` | Test the effectiveness of the security policies and devices by simulating real attacks. |

Enable step-by-step solutions for all questions
![sparkles-icon-decoration](https://academy.hackthebox.com/images/sparkles-solid.svg)

#### Questions

Answer the question(s) below
to complete this Section and earn cubes!

\+ 0  What device monitors network traffic and enforces rules to allow or block specific traffic?


Submit


\+ 0  Which type of firewall operates at the network and transport layers of the OSI model? (Format: two words)


Submit


\+ 0  What advanced feature does a Next-Generation Firewall include beyond stateful inspection? (Format: three words)


Submit


\+ 0  Which system generates alerts for suspicious network activity without blocking it? (Format: acronym)


Submit


\+ 0  Which system not only detects but also prevents suspicious network activity by blocking it? (Format: acronym)


Submit


\+ 0  What detection method involves comparing network traffic against a database of known exploits? (Format: three words)


Submit


# Data Flow Example

* * *

Based on the knowledge we have gained from the previous sections, the following paragraphs will show precisely what happens when a user tries to access a website from their laptop. Below is a breakdown of these events in a client-server model.

#### 1\. Accessing the Internet

Let's imagine a user using their laptop to connect to the internet through their home Wireless LAN (WLAN) network. As the laptop is connecting to this network, the following happens:

| **Steps** |
| --- |
| The laptop first identifies the correct wireless network/SSID |
| If the network uses WPA2/WPA3, the user must provide the correct password or credentials to authenticate. |
| Finally, the connection is established, and the DHCP protocol takes over the IP configuration. |

#### 2\. Checking Local Network Configuration (DHCP)

When a user opens a web browser (such as Chrome, Firefox, or Safari) and types in [www.example.com](http://www.example.com) to access a website, the browser prepares to send out a request for the webpage. Before a packet leaves the laptop, the operating system checks for a valid IP address for the local area network.

| **Steps** | **Description** |
| --- | --- |
| `IP Address Assignment` | If the laptop does not already have an IP, it requests one from the home router's `DHCP` server. This IP address is only valid within the local network. |
| `DHCP Acknowledgement` | The DHCP server assigns a private IP address (for example, _192.168.1.10_) to the laptop, along with other configuration details such as subnet mask, default gateway, and DNS server. |

#### 3\. DNS Resolution

Next, the laptop needs to find the IP address of `www.example.com`. For this to happen, the following steps must be taken.

| **Steps** | **Description** |
| --- | --- |
| `DNS Query` | The laptop sends a DNS query to the DNS server, which is typically an external DNS server provided by the ISP or a third-party service like Google DNS. |
| `DNS Response` | The DNS server looks up the domain `www.example.com` and returns its IP address (e.g., 93.184.216.34). |

#### 4\. Data Encapsulation and Local Network Transmission

Now that the laptop has the destination IP address, it begins preparing the data for transmission. The following steps occur within the `OSI/TCP-IP` model:

| **Steps** | **Description** |
| --- | --- |
| `Application Layer` | The browser creates an HTTP (or HTTPS) request for the webpage. |
| `Transport Layer` | The request is wrapped in a TCP segment (or UDP, but for web traffic it’s typically TCP). This segment includes source and destination ports (HTTP default port 80, HTTPS default port 443). |
| `Internet Layer` | The TCP segment is placed into an IP packet. The source IP is the laptop’s private IP (e.g., 192.168.1.10), and the destination IP is the remote server’s IP (93.184.216.34). |
| `Link Layer` | The IP packet is finally placed into an Ethernet frame (if we’re on Ethernet) or Wi-Fi frame. Here, the MAC (Media Access Control) addresses are included (source MAC is the laptop’s network interface, and destination MAC is the router’s interface). |

When the encapsulated frame is ready, the laptop checks its ARP table or sends an ARP request to find the MAC address of the default gateway (the router). Then, the frame is sent to the router using the router’s MAC address as the destination at the `link layer`.

#### 5\. Network Address Translation (NAT)

Once the router receives the frame, it processes the IP packet. At this point, the router replaces the private IP (192.168.1.10) with its public IP address (e.g., 203.0.113.45) in the packet header. This process is known as `Network Address Translation (NAT)`. Next, the router forwards the packet to the ISP’s network, and from there, it travels across the internet to the destination IP (93.184.216.34). During this process, the packet goes through many intermediate routers that look at the destination IP and determine the best path to reach that network.

#### 6\. Server Receives the Request and Responds

Upon reaching the destination network, the server's firewall, if there is one, checks if the incoming traffic on port 80 (HTTP) or 443 (HTTPS) is allowed. If it passes firewall rules, it goes to the server hosting `www.example.com`. Next, the web server software (e.g., Apache, Nginx, IIS) receives and processes the request, prepares the webpage (HTML, CSS, images, etc.), and sends it back as a response.

The server's response process follows a similar path in reverse. Its IP (93.184.216.34) is now the source, and our home router’s public IP (203.0.113.45) is the destination. When the packet reaches our home router (203.0.113.45), NAT ensures it is mapped back to the laptop's private IP (192.168.1.10).

#### 7\. Decapsulation and Display

Finally, our laptop receives the response and strips away the Ethernet/Wi-Fi frame, the IP header, and the TCP header, until the application layer data is extracted. The laptop's browser reads the HTML/CSS/JavaScript, and ultimately displays the webpage.

#### Data Flow Diagram

Below is a flow chart showing the complete journey of a user accessing a website on the internet.

![Network process: PC connects to WLAN, sends DHCP IP request, receives response, sends DNS query via Router to DNS Server, receives response, sends HTTP request to Web Server, receives response, renders webpage.](https://academy.hackthebox.com/storage/modules/289/Data_Flow/Data_Flow-1.png)


# Skills Assessment

* * *

Now that we are familiar with the foundational concepts of computer networking, it's time to see them in a real-world scenario. For this final section, we will explore the networking behind HTB Academy's lab environments. This guided assessment will be broken down into three chapters. Follow each chapter to answer the challenge questions and complete the assessment.

`Chapter 1. - Keep me in the Loop`

**→ Click to Show ←**

# Keep me in the Loop

* * *

For the first chapter of this assessment, we will be showcasing the HTB Academy `Pwnbox` \-\-\- a fully functional Linux machine running [Parrot OS](https://parrotsec.org/docs/introduction/what-is-parrot/), accessible entirely through a web browser. We provide it to our students to serve as their workstation when completing the various exercises and labs available on our platform. If you've never used Linux before, have no fear. Everything will be completely guided. When you are ready to begin, scroll down to select your Pwnbox location, and click `Launch Instance`.

Once the Pwnbox is up and running, feel free to press the `Full Screen` button for more visibility. Then, use your mouse cursor to open the `Parrot Terminal` as shown in the example below.

#### Launching the Parrot Terminal

![GIF showcasing the process to launch the parrot terminal.](https://academy.hackthebox.com/storage/modules/289/Skills_Assessment/parrot-terminal-2.gif)

* * *

We will start by investigating the network interfaces available on the Pwnbox. Type the following command into the terminal and press enter.

```shell
ifconfig -a

```

The `ifconfig` command is used on Linux to display network interface information (with the Windows equivalent being `ipconfig`.) After we send the command, we are shown three network interfaces: `ens3`, `lo`, and `tun0`, along with quite a bit of information. Take a few moments to examine the output, and take note of any similarities or differences you see between the three interfaces. Don't worry if some of the information doesn't make sense yet.

```shell
┌─[eu-academy-1]─[10.10.14.21]─[htb-ac-594497@htb-5mix2gkv1a]─[~]
└──╼ [★]$ ifconfig -a

ens3: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
       inet 209.50.61.235  netmask 255.255.252.0  broadcast 209.50.61.255
       inet6 fe80::a4ba:3bff:fe08:1e4e  prefixlen 64  scopeid 0x20<link>
       ether a6:ba:3b:08:1e:4e  txqueuelen 1000  (Ethernet)
       RX packets 30046  bytes 37369216 (35.6 MiB)
       RX errors 0  dropped 0  overruns 0  frame 0
       TX packets 20239  bytes 33367968 (31.8 MiB)
       TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
       inet 127.0.0.1  netmask 255.0.0.0
       inet6 ::1  prefixlen 128  scopeid 0x10<host>
       loop  txqueuelen 1000  (Local Loopback)
       RX packets 44771  bytes 33774927 (32.2 MiB)
       RX errors 0  dropped 0  overruns 0  frame 0
       TX packets 44771  bytes 33774927 (32.2 MiB)
       TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

tun0: flags=4305<UP,POINTOPOINT,RUNNING,NOARP,MULTICAST>  mtu 1500
       inet 10.10.14.21  netmask 255.255.254.0  destination 10.10.14.21
       inet6 dead:beef:2::11bb  prefixlen 64  scopeid 0x0<global>
       inet6 fe80::3c16:f601:d437:d71b  prefixlen 64  scopeid 0x20<link>
       unspec 00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00  txqueuelen 500  (UNSPEC)
       RX packets 164  bytes 13776 (13.4 KiB)
       RX errors 0  dropped 0  overruns 0  frame 0
       TX packets 170  bytes 14064 (13.7 KiB)
       TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

```

There is certainly a lot to unpack. We see three unique IPv4 addresses. We see some IPv6 addresses as well. However, one interface in particular stands out from the rest. Something seems very different about the `lo` interface.

```shell
 lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536 	   ### Greater MTU (maximum transmission unit) compared to other interfaces
       inet 127.0.0.1  netmask 255.0.0.0
       inet6 ::1  prefixlen 128  scopeid 0x10<host> ###  ipv6 address is ::1 --- scopeid is "host" rather than "link"
       loop  txqueuelen 1000  (Local Loopback) 	 ### Layer-2 information has phrases "loop" and "local loopback"
       RX packets 44771  bytes 33774927 (32.2 MiB)
       RX errors 0  dropped 0  overruns 0  frame 0
       TX packets 44771  bytes 33774927 (32.2 MiB)
       TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

```

What we are looking at is known as the [loopback](https://www.geeksforgeeks.org/what-is-a-loopback-address/) address, and it is always associated to the IPv4 address `127.0.0.1`. It's the IP address used when a device needs to send network data to itself. You may be wondering what purpose this serves; there are actually several. It's often used for testing, as a way to make sure an application is working as intended before going live on the network. It is also used by servers to keep certain services hidden from outside users. Think of an e-commerce website that utilizes authentication with its clients (i.e. registered acounts with usernames and passwords). Credentials and session cookies are typically stored in a database. Rather than have the database exposed to the public, it instead can only be accessed by the server itself. When a user attempts to log into the website, the website acts as an API between the user and the database. The server queries its own database to retrieve information on behalf of the end user.

Let's see if the Pwnbox makes use of the loopback address. In your terminal, enter the following command:

```shell
netstat -tulnp4

```

This will show us all of the open/listening `tcp` and `udp` ports for IPv4 , in the format of " `IP:PORT`". Additionally, depending on our permissions, we might be able see the name of the Program that's causing a port to be open. Again, take some time and examine the output. Do you see any services running on the loopback address?

```shell
┌─[eu-academy-1]─[10.10.14.21]─[htb-ac-594497@htb-5mix2gkv1a]─[~]
└──╼ [★]$ netstat -tulnp4

(Not all processes could be identified, non-owned process info
 will not be shown, you would have to be root to see it all.)
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name
tcp        0      0 127.0.0.1:5901          0.0.0.0:*               LISTEN      2814/Xtigervnc
tcp        0      0 127.0.0.1:631           0.0.0.0:*               LISTEN      -
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      -
tcp        0      0 0.0.0.0:111             0.0.0.0:*               LISTEN      -
tcp        0      0 209.50.61.235:80        0.0.0.0:*               LISTEN      -
udp        0      0 0.0.0.0:5353            0.0.0.0:*                           -
udp        0      0 0.0.0.0:43446           0.0.0.0:*                           -
udp        0      0 0.0.0.0:68              0.0.0.0:*                           -
udp        0      0 0.0.0.0:111             0.0.0.0:*                           -
udp        0      0 10.10.14.21:123         0.0.0.0:*                           -
udp        0      0 209.50.62.174:123       0.0.0.0:*                           -
udp        0      0 127.0.0.1:123           0.0.0.0:*                           -
udp        0      0 0.0.0.0:123             0.0.0.0:*                           -
udp        0      0 0.0.0.0:631             0.0.0.0:*                           -
udp        0      0 0.0.0.0:33423           0.0.0.0:*                           -

```

Now, try running the command shown below.

```shell
netstat tulp4

```

When we remove the `-n` option, the output will be displayed as " `hostname:service`" rather than " `IP:PORT`". We can see that the loopback IP address is resolved to `localhost`. The `ens3` IP address is resolved to the hostname of the Pwnbox. Also, it is worthwhile to note that a service listening on `0.0.0.0` is listening on all interfaces.

```shell
┌──[eu-academy-1]─[10.10.14.21]─[htb-ac-594497@htb-5mix2gkv1a]─[~]
└──╼ [★]$ netstat -tulp4

(Not all processes could be identified, non-owned process info
 will not be shown, you would have to be root to see it all.)
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name
tcp        0      0 localhost:5901          0.0.0.0:*               LISTEN      2814/Xtigervnc
tcp        0      0 localhost:ipp           0.0.0.0:*               LISTEN      -
tcp        0      0 0.0.0.0:ssh             0.0.0.0:*               LISTEN      -
tcp        0      0 0.0.0.0:sunrpc          0.0.0.0:*               LISTEN      -
tcp        0      0 htb-5mix2gkv1a.htb:http 0.0.0.0:*               LISTEN      -
udp        0      0 0.0.0.0:mdns            0.0.0.0:*                           -
udp        0      0 0.0.0.0:43446           0.0.0.0:*                           -
udp        0      0 0.0.0.0:bootpc          0.0.0.0:*                           -
udp        0      0 0.0.0.0:sunrpc          0.0.0.0:*                           -
udp        0      0 htb-5mix2gkv1a:ntp      0.0.0.0:*                           -
udp        0      0 htb-5mix2gkv1a.htb-:ntp 0.0.0.0:*                           -
udp        0      0 localhost:ntp           0.0.0.0:*                           -
udp        0      0 0.0.0.0:ntp             0.0.0.0:*                           -
udp        0      0 0.0.0.0:631             0.0.0.0:*                           -
udp        0      0 0.0.0.0:33423           0.0.0.0:*                           -

```

With this information, we now have some insight as to how we are able to see, and interact, with the Pwnbox. Earlier in the module we learned that protocol used when browsing websites is `HTTP`, via the well-known port 80. As we can see, the Pwnbox is indeed listening on port 80. This explains how we are able to make a connection via web browser. Subsequently, we can state with confidence that the IP tied to the `ens3` interface is the public IP address of the Pwnbox. Remember, public IP's can be accessed over the internet.

We also see the VNC service running on the loopback address. VNC (Virtual Network Computing) is a protocol used for remote screen sharing and remote access. Since students can access the Pwnbox desktop environment through their web browser, there is likely some form of port forwarding in place. This would allow traffic sent over HTTP to be forwarded to the VNC service running on the loopback address.

Port forwarding is a technique that allows traffic sent to one TCP/UDP port to be redirected to another—even across different machines. This also another way the loopback address can be utilized. For example, in the scenario below, a Windows host forwards its local port 8888 to a Linux VM's SSH port (22). The Linux machine is running as a [virtual machine with NAT](https://www.virtualbox.org/manual/ch06.html#network_nat) enabled, meaning it does not have a directly accessible IP on the network. Instead, the Windows host acts as an intermediary, forwarding traffic to it.

![GIF showcasing the connection on an SSH service running on port 8888 through Command Prompt.](https://academy.hackthebox.com/storage/modules/289/Skills_Assessment/loopback-ssh.gif)

Note that the topic of port forwarding is beyond the scope of this module. However, it is certainly something to be aware of, and is a wonderful example of the power and possibilities available through computer networking. Now that we've investigated the `lo` interface (and the `ens3` interface in the process), `tun0` is all that remains. And with that, we conclude chapter one.

* * *

`Chapter 2. - Having Tuns of Fun`

**→ Click to Show ←**

# Having Tuns of Fun

* * *

At the beginning of chapter one, we mentioned that the Pwnbox is used to interact with target machines in our lab environments. At the end of chapter one, we successfully investigated two out of the three available network interfaces:

- Loopback (lo): Allows the Pwnbox to send network traffic to itself.
- Public IP (ens3): Enables the Pwnbox to communicate with us over the internet.

That leaves one remaining interface: tun0. Based on its name, we can infer that it’s a tunnel interface, commonly associated with VPNs (Virtual Private Networks). Since lab targets exist on a separate private network, the Pwnbox must establish a secure connection to that environment, enabling us to reach them.

Let's confirm this by checking which route the Pwnbox takes to communicate with the target. Scroll to the end of this section and press `Click here to spawn the target system!`. After a few moments, a target machine will spawn, and we will be given its IP address.

Then, return to the Pwnbox and enter the following command into the Parrot Terminal:

```shell
ip route get <target ip>

```

This command will display the route taken for any traffic sent from the Pwnbox to reach the target.

```shell
┌──[eu-academy-1]─[10.10.14.21]─[htb-ac-594497@htb-5mix2gkv1a]─[~]
└──╼ [★]$ ip route get 10.129.233.197

10.129.233.197 via 10.10.14.1 dev tun0 src 10.10.14.21 uid 1002
    cache

```

Our theory has been confirmed—all traffic to the target is routed through `tun0`, a VPN tunnel that connects the Pwnbox to the private lab network. This allows us to interact with lab machines as if they were on the same local network. By using a VPN configuration file and software such as `OpenVPN`, computers will connect to the VPN server, which provides access to the network. HTB Academy's VPN is available to download at [https://academy.hackthebox.com/vpn](https://academy.hackthebox.com/vpn), for those who prefer to use their own workstation rather than Pwnbox.

Let's begin our first interaction with the target machine. We typically always begin by using `ping`. The `ping` is a networking utility used to test the reachability of a host on a network. It does not use TCP or UDP ports, making it a `Layer 3` protocol in terms of the OSI model. Type the following command into your terminal and observe the output.

```shell
ping -c 4 <target ip>

```

Here, we are sending four pings towards our target. Note that in Linux, if we do not specify the ping count, it will send pings `indefinitely` until we press `Ctrl + C` into the terminal.

```shell
┌─[eu-academy-1]─[10.10.14.21]─[htb-ac-594497@htb-5mix2gkv1a]─[~]
└──╼ [★]$ ping -c4 10.129.233.197

PING 10.129.233.197 (10.129.233.197) 56(84) bytes of data.
64 bytes from 10.129.233.197: icmp_seq=1 ttl=127 time=71.6 ms
64 bytes from 10.129.233.197: icmp_seq=2 ttl=127 time=71.3 ms
64 bytes from 10.129.233.197: icmp_seq=3 ttl=127 time=71.8 ms
64 bytes from 10.129.233.197: icmp_seq=4 ttl=127 time=71.2 ms

--- 10.129.233.197 ping statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 3003ms
rtt min/avg/max/mdev = 71.205/71.470/71.776/0.223 ms

```

We've now confirmed that the target is reachable from our attack host. A few things to take note of are the `ttl` and the `time`. The `ttl` , which stands for `time-to-live`, tells us how many "hops" our packets are allowed to take in order to reach the target. This rarely applies to devices on the same local network as us, but rather devices on the internet that require our packets to hop through multiple routers in order to reach their intended destination. The information next to `time` gives us an idea of how much latency there is on the network. In this example above, we see each ping takes roughly `71 milliseconds`.

We have just confirmed that our attack host can communicate with the target, by `pinging the IP address of the target machine`. Our next step is to enumerate open TCP/UDP ports on the machine. Just as we used the `netstat` utility to view the open ports on the Pwnbox, there is another tool we can use to determine the open ports on a remote machine. This tool is `nmap`, and it is absolutely fundamental for any current or aspiring infosec professional. Let's begin by enumerating the open TCP ports on our target. Enter the following command into your terminal.

```shell
nmap <target IP>

```

After a few moments, we will see `nmap` return the open TCP ports present on the target.

```shell
┌─[eu-academy-1]─[10.10.14.21]─[htb-ac-594497@htb-5mix2gkv1a]─[~]
└──╼ [★]$ nmap 10.129.233.197

Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-02-08 18:07 CST
Nmap scan report for 10.129.233.197
Host is up (0.073s latency).
Not shown: 993 closed tcp ports (reset)
PORT     STATE SERVICE
21/tcp   open  ftp
80/tcp   open  http
135/tcp  open  msrpc
139/tcp  open  netbios-ssn
445/tcp  open  microsoft-ds
3389/tcp open  ms-wbt-server
5357/tcp open  wsdapi

```

We see several open ports available. Ports `135`, `139`,and `445` will typically always be open on a Windows-based host. Port `3389` is the port used for Remote Desktop Protocol, or RDP for short. It is another common service seen on Windows machines. Port `5357` is used for `Microsoft's Web Services for Devices API` \- another Windows protocol, used for device discovery on the network.

We've now come to a thorough understanding of the three network interfaces of the Pwnbox, and have verified that we can interact with the target machine. Here, we will conclude chapter two. In our third and final chapter, we will interact with our target machine using specific ports and protocols.

* * *

`Chapter 3. - Target Acquired`

**→ Click to Show ←**

# Target Acquired

* * *

For our final chapter, we will be focusing on the target machine's port `21` and port `80` \- used for `FTP (File Transfer Protocol)` and `HTTP (Hyper-Text Transport Protocol.)` Let's perform another `nmap` scan, this time focused only on the two aforementioned ports.

```shell
nmap -p21,80 -sC -sV <target ip>

```

By adding the `-sC` and `-sV` options to our scan, this will allow nmap to determine the version of whatever program is listening on a given port, as well as additional information (such as how a particular service might be configured.

```shell
┌─[eu-academy-1]─[10.10.14.21]─[htb-ac-594497@htb-5mix2gkv1a]─[~]
└──╼ [★]$ nmap -p21,80 -sC -sV 10.129.233.197

Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-02-08 19:17 CST
Nmap scan report for 10.129.233.197
Host is up (0.071s latency).

PORT   STATE SERVICE VERSION
21/tcp open  ftp     Microsoft ftpd
| ftp-syst:
|_  SYST: Windows_NT
|_ftp-anon: Anonymous FTP login allowed (FTP code 230)
80/tcp open  http    Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 11.05 seconds

```

Nmap tells us that the FTP service has `Anonymous FTP` enabled, meaning that anyone is able to connect to the FTP service (typically by providing the username `anonymous`). However, the HTTP service on port 80 does not return as much information. Generally, nmap will be able to fingerprint the webserver software in place (such as `Apache`, `Nginx`, or `IIS`). Our initial nmap scan operates at layer 4 of the OSI model --- that is, determining if the port is open or closed at the TCP/UDP level. For things such as the version scan (-sV) or default scripts (-sC), nmap uses protocol-specific layer 7 packets. Because port 80 showed no additional information after our second scan, we can hypothesize that there is some sort of `request filtering` in place. We will touch on this more in a bit.

IMPORTANT: While it is not illegal, it is considered unethical to use nmap (or any port scanning utility) against a device that you do not either own, or have explicit permission to be scanning.

Let's take a look at the FTP service running on port 21. To connect, we will use [netcat](https://en.wikipedia.org/wiki/Netcat), a utility for making raw TCP/UDP connections. After we connect with `netcat`, whatever we characters we type in will be transmitted to the port in which we are connected. Rather than using a specific `FTP client` utility, we will use netcat to better understand how the FTP protocol works. On the flipside, for the HTTP service, software such as a web browser (or the `curl` and `wget` command line tools) formulate and send the protocol specific data for us. Whenever you are ready, enter the following commend into your terminal and press enter.

```shell
nc <target ip> 21

```

Here, we are telling netcat to connect to port 21 on the target machine. Once connected, we are greeted with a banner from the FTP service, indicating we have successfully connected.

```shell
┌─[eu-academy-1]─[10.10.14.21]─[htb-ac-594497@htb-5mix2gkv1a]─[~]
└──╼ [★]$ nc 10.129.233.197 21

220 Microsoft FTP Service

```

Next, we will login as an `anonymous user` with the commands shown below, and then specify we will be using [Passive Mode](https://www.geeksforgeeks.org/difference-between-active-and-passive-ftp/):

```shell
USER anonymous[Ctrl+V][Enter][Enter]
PASS anything[Ctrl+V][Enter][Enter]
PASV[Ctrl+V][Enter][Enter]

```

The reason we provided the `[Ctrl + V] [Enter] [Enter]` is because FTP requires a `return character and new-line character (\r\n)` for its commands. When we press Enter on our keyboard, Netcat only sends the `\n`.

```shell
┌─[eu-academy-1]─[10.10.14.21]─[htb-ac-594497@htb-5mix2gkv1a]─[~]
└──╼ [★]$ nc 10.129.233.197 21

220 Microsoft FTP Service
USER anonymous^M
331 Anonymous access allowed, send identity (e-mail name) as password.
PASS anything^M
230 User logged in.
PASV^M
227 Entering Passive Mode (10,129,233,197,194,40).

```

FTP (File Transfer Protocol) uses two separate channels to function.

| **Channel** | **Purpose** | **Port** |
| --- | --- | --- |
| Control Channel | Sends FTP commands (USER, PASS, LIST, RETR, etc.) | Port 21 |
| Data Channel | Transfers files and directory listings | Dynamic Port (Varies by mode: Active or Passive). |

Here, we have selected passive mode, and subsequently need to re-connect to the FTP server on another port. To determine the port number, we need to do some calculations. This is mainly due to limitations in the FTP protocol, as the full port cannot be displayed at once, so it is instead split to 2 small number 'p1 and p2; the last 2 numbers in the above output'. Then the real port is calculated as 'p1\*256 + p2'. See [this documentation](http://www.faqs.org/rfcs/rfc959.html) for more info.

So, to calculate the port number, we will use the last two numbers shown (in the example above, they are `194` and `40`). We will take the first number and multiply it by `256`, then add the second number.

`194` \\* `256` \+ `40` = `49704`

Let's open a new `Parrot Terminal` by clicking `File` (located in the top left hand corner of your current Parrot Terminal), then select `Open Terminal` -\> `Bash`. Then, in our new Terminal, we will use netcat to connect to the `data channel`.

```shell
nc -v <target ip> <dynamic port>

```

```shell
┌─[eu-academy-1]─[10.10.14.21]─[htb-ac-594497@htb-5mix2gkv1a]─[~]
└──╼ [★]$ nc -v 10.129.233.197 49704

10.129.233.197: inverse host lookup failed: Unknown host
(UNKNOWN) [10.129.233.197] 49704 (?) open

```

Now, let's return to our first Terminal and use the `connection channel` to list the available files in the FTP share. Enter the following command:

```shell
LIST[Ctrl+V][Enter][Enter]

```

We should see a message indicating that a data connection is already open, and therefore a transfer is starting.

```shell
┌─[eu-academy-1]─[10.10.14.21]─[htb-ac-594497@htb-5mix2gkv1a]─[~]
└──╼ [★]$ nc 10.129.233.197 21

220 Microsoft FTP Service
USER anonymous^M
331 Anonymous access allowed, send identity (e-mail name) as password.
PASS anything^M
230 User logged in.
PASV^M
227 Entering Passive Mode (10,129,233,197,194,40).
LIST^M
125 Data connection already open; Transfer starting.
226 Transfer complete.

```

When we check back on our other Terminal, we will see a list of the files available in the share!

```shell
┌─[eu-academy-1]─[10.10.14.21]─[htb-ac-594497@htb-5mix2gkv1a]─[~]
└──╼ [★]$ nc -v 10.129.233.197 49704

10.129.233.197: inverse host lookup failed: Unknown host
(UNKNOWN) [10.129.233.197] 49704 (?) open
02-08-25  08:37PM                  438 Note-From-IT.txt

```

We see that there is a `Note-From-IT.txt` text file available for us to read. To retrieve the file, we must once again enter the following command in our `connection channel`, then use netcat to establish connection to a new `data channel`.

```shell
RETR[Ctrl + V][Enter][Enter]

```

The output will be similar to when we ran the command the first time.

```shell
┌─[eu-academy-1]─[10.10.14.21]─[htb-ac-594497@htb-5mix2gkv1a]─[~]
└──╼ [★]$ nc 10.129.233.197 21

220 Microsoft FTP Service
USER anonymous^M
331 Anonymous access allowed, send identity (e-mail name) as password.
PASS anything^M
230 User logged in.
PASV^M
227 Entering Passive Mode (10,129,233,197,194,40).
LIST^M
125 Data connection already open; Transfer starting.
226 Transfer complete.
PASV^M
227 Entering Passive Mode (10,129,233,197,194,50).

```

Again, we must calculate the port number, and use `netcat` to make the connection.

`194` \\* `256` \+ `50` = `49714`

```shell
┌─[eu-academy-1]─[10.10.14.21]─[htb-ac-594497@htb-5mix2gkv1a]─[~]
└──╼ [★]$ nc -v 10.129.233.197 49714

10.129.233.197: inverse host lookup failed: Unknown host
(UNKNOWN) [10.129.233.197] 49714 (?) open

```

Sending one final command, we can retrieve the `Note-From-IT.txt` text file.

```shell
RETR Note-From-IT.txt[Ctrl+V][Enter][Enter]

```

```shell
┌─[eu-academy-1]─[10.10.14.21]─[htb-ac-594497@htb-5mix2gkv1a]─[~]
└──╼ [★]$ nc 10.129.233.197 21

220 Microsoft FTP Service
USER anonymous^M
331 Anonymous access allowed, send identity (e-mail name) as password.
PASS anything^M
230 User logged in.
PASV^M
227 Entering Passive Mode (10,129,233,197,194,40).
LIST^M
125 Data connection already open; Transfer starting.
226 Transfer complete.
PASV^M
227 Entering Passive Mode (10,129,233,197,194,50).
RETR Note-From-IT.txt^M
125 Data connection already open; Transfer starting.
226 Transfer complete.

```

When we check the data channel, we are greeted with the contents of the note.

```shell
┌─[eu-academy-1]─[10.10.14.21]─[htb-ac-594497@htb-5mix2gkv1a]─[~]
└──╼ [★]$ nc -v 10.129.233.197 49714

10.129.233.197: inverse host lookup failed: Unknown host
(UNKNOWN) [10.129.233.197] 49714 (?) open
Bertolis,

The website is still under construction. To stop users from poking their nose where it doesn't belong, I've configured IIS to only allow requests containing a specific user-agent header. If you'd like to test it out, please provide the following header to your HTTP request.

User-Agent: Server Administrator

The site should be finished within the next couple of weeks. I'll keep you posted.

Cheers,
jarednexgent

```

* * *

The note from the IT team has some revealing information. It turns out, the web server is configured to only allow requests that provide a specific user-agent header. We have seen how the FTP protocol recognizes commands such as `USER`, `PASS`, `PASV`, `LIST`, and `RETR`. The HTTP protocol, on the other hand, utilizes a system of requests and responses consisting of [HTTP headers](https://en.wikipedia.org/wiki/List_of_HTTP_header_fields). By providing the header `User-Agent: Server Administrator`, we should be able to view the website that is being served via port 80.

Let us make our initial TCP connection with netcat using the command shown below:

```shell
nc -v <target ip> 80

```

We are met with a message indicating that the port is open.

```shell
┌─[eu-academy-1]─[10.10.14.21]─[htb-ac-594497@htb-5mix2gkv1a]─[~]
└──╼ [★]$ nc -v 10.129.233.197 80

10.129.233.197: inverse host lookup failed: Unknown host
(UNKNOWN) [10.129.233.197] 80 (http) open

```

Now, we can formulate our request. Enter the following into your netcat session:

```shell
GET / HTTP/1.1[enter]
Host: <target ip>[enter]
User-Agent: Server Administrator[enter][enter]

```

The web server responds! Unlike when we use our web browser (which makes the HTTP request for us automatically, then renders the HTML into an aesthetic, readable website), with netcat the contents of the webpage are printed to our terminal. We can also find a flag hidden in the comments of the HTML, which would not be visibile if we were to use our web browser.

```shell
┌─[eu-academy-1]─[10.10.14.21]─[htb-ac-594497@htb-5mix2gkv1a]─[~]
└──╼ [★]$ nc -v 10.129.233.197 80

10.129.233.197: inverse host lookup failed: Unknown host
(UNKNOWN) [10.129.233.197] 80 (http) open
GET / HTTP/1.1
Host: 10.129.233.197
User-Agent: Server Administrator

HTTP/1.1 200 OK
Content-Type: text/html
Accept-Ranges: bytes
ETag: "5acd7854a179db1:0"
Server: Microsoft-IIS/10.0
Date: Tue, 5 Feb 2025 00:44:43 GMT
Content-Length: 746

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1" />
<title>IIS Windows Server</title>
<style type="text/css">
<!--
body {
	color:#000000;
	background-color:#0072C6;
	margin:0;
}

#container {
	margin-left:auto;
	margin-right:auto;
	text-align:center;
	}

a img {
	border:none;
}

-->
</style>
</head>
<body>
<div id="container">
<a href="http://go.microsoft.com/fwlink/?linkid=66138&amp;clcid=0x409"><img src="iisstart.png" alt="IIS" width="960" height="600" /></a>
</div>
</body>
</html>
<!-- HTB{REDACTED} -->

```

`GET /` is an HTTP request that tells a web server "Give me the homepage (root directory) of this website." If there were a login page we wanted to access, our request might look like `GET /login.php`. The `Host` header tells the server which host we are requesting (it is possible for a server to host multiple, unique webpages all on the same server). The `User Agent` header is used to indicate the agent making the web request --- for example, if it's a browser making the request, the user agent will typically be the name and version of the browser.

The server, in turn, replies with it's own headers. For example, the `Content-Type` header tells us what type of data the server is replying with. The `Accept` header tells us what type of data it is able to receive, and the `Server` header tells us that the web server software in place is Microsoft IIS. Below these headers is the HTML of the site we are attempting to access.

We have now seen first hand how the FTP and HTTP protocols work. By sending specific packets of data, we adhere to the `protocol` (or "language") that a particular service speaks. We have seen how FTP utilizes both a data channel and connection channel, and how it's protocol requires new-line and return characters be submitted. Conversely, we have seen the HTTP protocol be more forgiving, while at the same time displaying merciless intolerance for requests that do not adhere to the specifications put in place (i.e., the `user-agent` header request filtering).

With that, we conclude chapter three. You should now be able to complete all of the challenge questions and finish the assessment.


