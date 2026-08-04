# Networking Overview

* * *

A network enables two computers to communicate with each other. There is a wide array of `topologies` (mesh/tree/star), `mediums` (ethernet/fiber/coax/wireless), and `protocols` (TCP/UDP/IPX) that can be used to facilitate the network. It is important as security professionals to understand networking because when the network fails, the error may be silent, causing us to miss something.

Setting up a large, flat network is not extremely difficult, and it can be a reliable network, at least operationally. However, a flat network is like building a house on a land plot and considering it secure because it has a lock on the door. By creating lots of smaller networks and having them communicate, we can add defense layers. Pivoting around a network is not difficult, but doing it quickly and silently is tough and will slow attackers down. Back to the house scenario, let's walk through the following examples:

#### Example No. 1

Building smaller networks and putting Access Control Lists around them is like putting a fence around the property's border that creates specific entry and exit points. Yes, an attacker could jump over the fence, but this looks suspicious and is not common, allowing it to be quickly detected as malicious activity. Why is the printer network talking to the servers over HTTP?

#### Example No. 2

Taking the time to map out and document each network's purpose is like placing lights around the property, making sure all activity can be seen. Why is the printer network talking to the internet at all?

#### Example No. 3

Having bushes around windows is a deterrent to people attempting to open the window. Just like Intrusion Detection Systems like Suricata or Snort are a deterrent to running network scans. Why did a port scan originate from the printer network?

These examples may sound silly, and it is common sense to block a printer from doing all of the above. However, if the printer is on a "flat /24 network" and gets a DHCP address, it can be challenging to place these types of restrictions on them.

* * *

## Story Time - A Pentesters Oversight

Most networks use a `/24` subnet, so much so that many Penetration Testers will set this subnet mask (255.255.255.0) without checking. The /24 network allows computers to talk to each other as long as the first three octets of an IP Address are the same (ex: 192.168.1.xxx). Setting the subnet mask to `/25` divides this range in half, and the computer will be able to talk to only the computers on "its half." We have seen Penetration Test reports where the assessor claimed a Domain Controller was offline when it was just on a different network in reality. The network structure was something like this:

- Server Gateway: 10.20.0.1/25
- Domain Controller: 10.20.0.10/25
- Client Gateway: 10.20.0.129/25
- Client Workstation: 10.20.0.200/25
- Pentester IP: 10.20.0.252/24 (Set Gateway to 10.20.0.1)

The Pentester communicated with the Client Workstations and thought they did an excellent job because they managed to steal a workstation password via Impacket. However, due to a failure to understand the network, they never managed to get off the Client Network and reach more "high value" targets such as database servers. Hopefully, if this sounds confusing to you, you can come back to this statement at the end of the module and understand it!

* * *

## Basic Information

Let us look at the following high-level diagram of how a Work From Home setup may work.

![Diagram showing a home network with a router connecting a smartphone, notebook, and PC, and a company network with a router connecting a switch, webserver, IP phone, printer, and two client hosts. Both networks connect to an Internet Service Provider (ISP), with a domain name server (DNS) and internet access.](https://academy.hackthebox.com/storage/modules/34/redesigned/net_overview.png)

* * *

The entire internet is based on many subdivided networks, as shown in the example and marked as " `Home Network`" and " `Company Network`." We can imagine `networking` as the delivery of mail or packages sent by one computer and received by the other.

Suppose we imagine as a scenario that we want to visit a company's website from our " `Home Network`." In that case, we exchange data with the company's website located in their " `Company Network`."
As with sending mail or packets, we know the address where the packets should go. The website address or `Uniform Resource Locator` ( `URL`) which we enter into our browser is also known as `Fully Qualified Domain Name` ( `FQDN`).

The difference between `URL` s and `FQDN` s is that:

- an `FQDN` ( `www.hackthebox.eu`) only specifies the address of the "building" and
- an `URL` ( `https://www.hackthebox.eu/example?floor=2&office=dev&employee=17`) also specifies the " `floor`," " `office`," " `mailbox`" and the corresponding " `employee`" for whom the package is intended.

We will discuss the exact representations and definitions more clearly and precisely in other sections.

The fact is that we know the address, but not the exact geographical location of the address. In this situation, the post office can determine the exact location, which then forwards the packets to the desired location. Therefore, our post office forwards our packets to the main post office, representing our `Internet Service Provider` ( `ISP`).

Our post office is our `router` which we utilize to connect to the " `Internet`" in networking.

As soon as we send our packet through our post office ( `router`), the packet is forwarded to the `main post office` ( `ISP`). This main post office looks in the `address register`/ `phonebook` ( `Domain Name Service`) where this address is located and returns the corresponding geographical coordinates ( `IP address`). Now that we know the address's exact location, our packet is sent directly there by a direct flight via our main post office.

After the web server has received our packet with the request of what their website looks like, the webserver sends us back the packet with the data for the presentation of the website via the post office ( `router`) of the " `Company Network`" to the specified return address ( `our IP address`).

* * *

## Extra Points

In that diagram, I would hope the company network shown consists of five separate networks!

1. The Web Server should be in a DMZ (Demilitarized Zone) because clients on the internet can initiate communications with the website, making it more likely to become compromised. Placing it in a separate network allows the administrators to put networking protections between the web server and other devices.

2. Workstations should be on their own network, and in a perfect world, each workstation should have a Host-Based Firewall rule preventing it from talking to other workstations. If a Workstation is on the same network as a Server, networking attacks like `spoofing` or `man in the middle` become much more of an issue.

3. The Switch and Router should be on an "Administration Network." This prevents workstations from snooping in on any communication between these devices. I have often performed a Penetration Test and saw `OSPF` (Open Shortest Path First) advertisements. Since the router did not have a `trusted network`, anyone on the internal network could have sent a malicious advertisement and performed a `man in the middle` attack against any network.

4. IP Phones should be on their own network. Security-wise this is to prevent computers from being able to eavesdrop on communication. In addition to security, phones are unique in the sense that latency/lag is significant. Placing them on their own network can allow network administrators to prioritize their traffic to prevent high latency more easily.

5. Printers should be on their own network. This may sound weird, but it is next to impossible to secure a printer. Due to how Windows works, if a printer tells a computer authentication is required during a print job, that computer will attempt an `NTLMv2` authentication, which can lead to passwords being stolen. Additionally, these devices are great for persistence and, in general, have tons of sensitive information sent to them.


* * *

## Fun Story

During COVID, I was tasked to perform a `Physical Penetration Test` across state lines, and my state was under a `stay at home` order. The company I was testing had minimal staff in the office. I decided to purchase an expensive printer and exploited it to put a reverse shell in it, so when it connected to the network, it would send me a shell (remote access). Then I shipped the printer to the company and sent a phishing email thanking the staff for coming in and explaining that the printer should allow them to print or scan things more quickly if they want to bring some stuff home to WFH for a few days. The printer was hooked up almost instantly, and their domain administrator's computer was kind enough to send the printer his credentials!

If the client had designed a secure network, this attack probably would not have been possible for many reasons:

- Printer should not have been able to talk to the internet
- Workstation should not have been able to communicate to the printer over port 445
- Printer should not be able to initiate connections to workstations. In some cases, printer/scanner combinations should be able to communicate to a mail server to email scanned documents.


# Network Types

* * *

Each network is structured differently and can be set up individually. For this reason, so-called `types` and `topologies` have been developed that can be used to categorize these networks. When reading about all the types of networks, it can be a bit of information overload as some network types include the geographical range. We rarely hear some of the terminologies in practice, so this section will be broken up into `Common Terms` and `Book Terms`. Book terms are good to know, as there has been a single documented case of an email server failing to deliver emails longer than 500 miles but don't be expected to be able to recite them on demand unless you are studying for a networking exam.

#### Common Terminology

| **Network Type** | **Definition** |
| --- | --- |
| Wide Area Network (WAN) | Internet |
| Local Area Network (LAN) | Internal Networks (Ex: Home or Office) |
| Wireless Local Area Network (WLAN) | Internal Networks accessible over Wi-Fi |
| Virtual Private Network (VPN) | Connects multiple network sites to one `LAN` |

* * *

## WAN

The WAN (Wide Area Network) is commonly referred to as `The Internet`. When dealing with networking equipment, we'll often have a WAN Address and LAN Address. The WAN one is the address that is generally accessed by the Internet. That being said, it is not inclusive to the Internet; a WAN is just a large number of LANs joined together. Many large companies or government agencies will have an "Internal WAN" (also called Intranet, Airgap Network, etc.). Generally speaking, the primary way we identify if the network is a WAN is to use a WAN Specific routing protocol such as BGP and if the IP Schema in use is not within RFC 1918 (10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16).

* * *

## LAN / WLAN

LANs (Local Area Network) and WLANs (Wireless Local Area Network) will typically assign IP Addresses designated for local use (RFC 1918, 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16). In some cases, like some colleges or hotels, you may be assigned a routable (internet) IP Address from joining their LAN, but that is much less common. There's nothing different between a LAN or WLAN, other than WLAN's introduce the ability to transmit data without cables. It is mainly a security designation.

* * *

## VPN

There are three main types `Virtual Private Networks` ( `VPN`), but all three have the same goal of making the user feel as if they were plugged into a different network.

#### Site-To-Site VPN

Both the client and server are Network Devices, typically either `Routers` or `Firewalls`, and share entire network ranges. This is most commonly used to join company networks together over the Internet, allowing multiple locations to communicate over the Internet as if they were local.

#### Remote Access VPN

This involves the client's computer creating a virtual interface that behaves as if it is on a client's network. Hack The Box utilizes `OpenVPN`, which makes a TUN Adapter letting us access the labs. When analyzing these VPNs, an important piece to consider is the routing table that is created when joining the VPN. If the VPN only creates routes for specific networks (ex: 10.10.10.0/24), this is called a `Split-Tunnel VPN`, meaning the Internet connection is not going out of the VPN. This is great for Hack The Box because it provides access to the Lab without the privacy concern of monitoring your internet connection. However, for a company, `split-tunnel` VPN's are typically not ideal because if the machine is infected with malware, network-based detection methods will most likely not work as that traffic goes out the Internet.

#### SSL VPN

This is essentially a VPN that is done within our web browser and is becoming increasingly common as web browsers are becoming capable of doing anything. Typically these will stream applications or entire desktop sessions to your web browser. A great example of this would be the HackTheBox Pwnbox.

* * *

## Book Terms

| Network Type | Definition |
| --- | --- |
| Global Area Network (GAN) | Global network (the Internet) |
| Metropolitan Area Network (MAN) | Regional network (multiple LANs) |
| Wireless Personal Area Network (WPAN) | Personal network (Bluetooth) |

#### GAN

A worldwide network such as the `Internet` is known as a `Global Area Network` ( `GAN`). However, the Internet is not the only computer network of this kind. Internationally active companies also maintain isolated networks that span several `WAN` s and connect company computers worldwide. `GAN` s use the glass fibers infrastructure of wide-area networks and interconnect them by international undersea cables or satellite transmission.

#### MAN

`Metropolitan Area Network` ( `MAN`) is a broadband telecommunications network that connects several `LAN` s in geographical proximity. As a rule, these are individual branches of a company connected to a `MAN` via leased lines. High-performance routers and high-performance connections based on glass fibers are used, which enable a significantly higher data throughput than the Internet. The transmission speed between two remote nodes is comparable to communication within a `LAN`.

Internationally operating network operators provide the infrastructure for `MAN` s. Cities wired as `Metropolitan Area Networks` can be integrated supra-regionally in `Wide Area Networks` ( `WAN`) and internationally in `Global Area Networks` ( `GAN`).

#### PAN / WPAN

Modern end devices such as smartphones, tablets, laptops, or desktop computers can be connected ad hoc to form a network to enable data exchange. This can be done by cable in the form of a `Personal Area Network` ( `PAN`).

The wireless variant `Wireless Personal Area Network` ( `WPAN`) is based on Bluetooth or Wireless USB technologies. A `wireless personal area network` that is established via Bluetooth is called `Piconet`. `PAN` s and `WPAN` s usually extend only a few meters and are therefore not suitable for connecting devices in separate rooms or even buildings.

In the context of the `Internet of Things` ( `IoT`), `WPAN` s are used to communicate control and monitor applications with low data rates. Protocols such as Insteon, Z-Wave, and ZigBee were explicitly designed for smart homes and home automation.


# Networking Topologies

* * *

A `network topology` is a typical arrangement and `physical` or `logical` connection of devices in a network. Computers are `hosts`, such as `clients` and `servers`, that actively use the network. They also include `network components` such as `switches`, `bridges`, and `routers`, which we will discuss in more detail in later sections, which have a distribution function and ensure that all network hosts can establish a logical connection with each other. The network topology determines the components to be used and the access methods to the transmission media.

The `transmission medium layout` used to connect devices is the physical topology of the network. For conductive or glass fiber media, this refers to the cabling plan, the positions of the `nodes`, and the connections between the nodes and the cabling. In contrast, the `logical topology` is how the signals act on the network media or how the data will be transmitted across the network from one device to the devices' physical connection.

* * *

We can divide the entire network topology area into three areas:

#### 1\. Connections

| `Wired connections` | `Wireless connections` |
| --- | --- |
| Coaxial cabling | Wi-Fi |
| Glass fiber cabling | Cellular |
| Twisted-pair cabling | Satellite |
| and others | and others |

* * *

#### 2\. Nodes - Network Interface Controller (NICs)

|  |  |  |  |
| --- | --- | --- | --- |
| Repeaters | Hubs | Bridges | Switches |
| Router/Modem | Gateways | Firewalls |  |

Network nodes are the `transmission medium's connection points` to transmitters and receivers of electrical, optical, or radio signals in the medium. A node may be connected to a computer, but certain types may have only one microcontroller on a node or may have no programmable device at all.

* * *

#### 3\. Classifications

We can imagine a topology as a virtual form or `structure of a network`. This form does not necessarily correspond to the actual physical arrangement of the devices in the network. Therefore these topologies can be either `physical` or `logical`. For example, the computers on a `LAN` may be arranged in a circle in a bedroom, but it is very unlikely to have an actual ring topology.

Network topologies are divided into the following eight basic types:

|  |  |
| --- | --- |
| Point-to-Point | Bus |
| Star | Ring |
| Mesh | Tree |
| Hybrid | Daisy Chain |

More complex networks can be built as hybrids of two or more of the basic topologies mentioned above.

* * *

## Point-to-Point

The simplest network topology with a dedicated connection between two hosts is the `point-to-point` topology. In this topology, a direct and straightforward physical link exists only between `two hosts`. These two devices can use these connections for mutual communication.

`Point-to-point` topologies are the basic model of traditional telephony and must not be confused with `P2P` ( `Peer-to-Peer` architecture).

#### Point-To-Point Topology

![image](https://academy.hackthebox.com/storage/modules/34/redesigned/topo_p2p.png)

* * *

## Bus

All hosts are connected via a transmission medium in the bus topology. Every host has access to the transmission medium and the signals that are transmitted over it. There is no central network component that controls the processes on it. The transmission medium for this can be, for example, a `coaxial cable`.

Since the medium is shared with all the others, only `one host can send`, and all the others can only receive and evaluate the data and see whether it is intended for itself.

#### Bus Topology

![Diagram showing a connection between Host A and Host B.](https://academy.hackthebox.com/storage/modules/34/redesigned/topo_bus.png)

* * *

## Star

The star topology is a network component that maintains a connection to all hosts. Each host is connected to the `central network component` via a separate link. This is usually a router, a hub, or a switch. These handle the `forwarding function` for the data packets. To do this, the data packets are received and forwarded to the destination.
The data traffic on the central network component can be very high since all data and connections go through it.

#### Star Topology

![Diagram showing connections between Hosts A, B, C, D, E, and F.](https://academy.hackthebox.com/storage/modules/34/redesigned/topo_star.png)

* * *

## Ring

The `physical` ring topology is such that each host or node is connected to the ring with two cables:

- One for the `incoming` signals and
- the another for the `outgoing` ones.

This means that one cable arrives at each host and one cable leaves. The ring topology typically does not require an active network component. The control and access to the transmission medium are regulated by a protocol to which all stations adhere.

A `logical` ring topology is based on a physical star topology, where a distributor at the node simulates the ring by forwarding from one port to the next.

The information is transmitted in a predetermined transmission direction. Typically, the transmission medium is accessed sequentially from station to station using a retrieval system from the central station or a `token`. A token is a bit pattern that continually passes through a ring network in one direction, which works according to the `claim token process`.

#### Ring Topology

![Diagram showing a router connecting Hosts A, B, C, and D.](https://academy.hackthebox.com/storage/modules/34/redesigned/topo_ring.png)

* * *

## Mesh

Many nodes decide about the connections on a `physical` level and the routing on a `logical` level in meshed networks. Therefore, meshed structures have no fixed topology. There are two basic structures from the basic concept: the `fully meshed` and the `partially meshed` structure.

Each host is connected to every other host in the network in a `fully meshed structure`. This means that the hosts are meshed with each other. This technique is primarily used in `WAN` or `MAN` to ensure high reliability and bandwidth.

In this setup, important network nodes such as routers could be networked together. If one router fails, the others can continue to work without problems, and the network can absorb the failure due to the many connections.

Each node of a fully meshed topology has the same routing functions and knows the neighboring nodes it can communicate with proximity to the network gateway and traffic loads.

In the `partially meshed structure`, the endpoints are connected by only one connection. In this type of network topology, specific nodes are connected to exactly one other node, and some other nodes are connected to two or more other nodes with a point-to-point connection.

#### Mesh Topology

![Network diagram showing Hosts A, B, C, and D connected through Routers A, B, C, and D.](https://academy.hackthebox.com/storage/modules/34/redesigned/topo_mesh.png)

* * *

## Tree

The tree topology is an extended star topology that more extensive local networks have in this structure. This is especially useful when several topologies are combined. This topology is often used, for example, in larger company buildings.

There are both logical tree structures according to the `spanning tree` and physical ones. Modular modern networks, based on structured cabling with a hub hierarchy, also have a tree structure. Tree topologies are also used for `broadband networks` and `city networks` ( `MAN`).

#### Tree Topology

![Network diagram showing a server connected to two Ethernet switches, each linking to Hosts A, B, C, D, E, and F.](https://academy.hackthebox.com/storage/modules/34/redesigned/topo_tree.png)

* * *

## Hybrid

Hybrid networks combine two or more topologies so that the resulting network does not present any standard topologies. For example, a tree network can represent a hybrid topology in which star networks are connected via interconnected bus networks. However, a tree network that is linked to another tree network is still topologically a tree network. A hybrid topology is always created when `two different` basic network topologies are interconnected.

#### Hybrid Topology

![Network diagram showing Hosts A, B, C, D, E, and F connected through Routers A, B, and C.](https://academy.hackthebox.com/storage/modules/34/redesigned/topo_hybrid.png)

* * *

## Daisy Chain

In the daisy chain topology, multiple hosts are connected by placing a cable from one node to another.

Since this creates a chain of connections, it is also known as a daisy-chain configuration in which multiple hardware components are connected in a series. This type of networking is often found in automation technology ( `CAN`).

Daisy chaining is based on the physical arrangement of the nodes, in contrast to token procedures, which are structural but can be made independent of the physical layout. The signal is sent to and from a component via its previous nodes to the computer system.

#### Daisy Chain Topology

![Network diagram showing Hosts A, B, D, and E connected to Host C.](https://academy.hackthebox.com/storage/modules/34/redesigned/topo_daisy-chain.png)


# Proxies

* * *

Many people have different opinions on what a proxy is:

- Security Professionals jump to `HTTP Proxies` (BurpSuite) or pivoting with a `SOCKS/SSH Proxy` ( `Chisel`, `ptunnel`, `sshuttle`).

- Web Developers use proxies like Cloudflare or ModSecurity to block malicious traffic.

- Average people may think a proxy is used to obfuscate your location and access another country's Netflix catalog.

- Law Enforcement often attributes proxies to illegal activity.


Not all the above examples are correct. A proxy is when a device or service sits in the middle of a connection and acts as a mediator. The `mediator` is the critical piece of information because it means the device in the middle must be able to inspect the contents of the traffic. Without the ability to be a `mediator`, the device is technically a `gateway`, not a proxy.

Back to the above question, the average person has a mistaken idea of what a proxy is as they are most likely using a VPN to obfuscate their location, which technically is not a proxy. Most people think whenever an IP Address changes, it is a proxy, and in most cases, it's probably best not to correct them as it is a common and harmless misconception. Correcting them could lead to a more extended conversation that trails into tabs vs. spaces, `emacs` vs. `vim`, or finding out they are a `nano` user.

If you have trouble remembering this, proxies will almost always operate at Layer 7 of the OSI Model. There are many types of proxy services, but the key ones are:

- `Dedicated Proxy` / `Forward Proxy`
- `Reverse Proxy`
- `Transparent Proxy`

* * *

## Dedicated Proxy / Forward Proxy

The `Forward Proxy`, is what most people imagine a proxy to be. A Forward Proxy is when a client makes a request to a computer, and that computer carries out the request.

For example, in a corporate network, sensitive computers may not have direct access to the Internet. To access a website, they must go through a proxy (or web filter). This can be an incredibly powerful line of defense against malware, as not only does it need to bypass the web filter (easy), but it would also need to be `proxy aware` or use a non-traditional C2 (a way for malware to receive tasking information). If the organization only utilizes `FireFox`, the likelihood of getting proxy-aware malware is improbable.

Web Browsers like Internet Explorer, Edge, or Chrome all obey the "System Proxy" settings by default. If the malware utilizes WinSock (Native Windows API), it will likely be proxy aware without any additional code. Firefox does not use `WinSock` and instead uses `libcurl`, which enables it to use the same code on any operating system. This means that the malware would need to look for Firefox and pull the proxy settings, which malware is highly unlikely to do.

Alternatively, malware could use DNS as a c2 mechanism, but if an organization is monitoring DNS (which is easily done using [Sysmon](https://medium.com/falconforce/sysmon-11-dns-improvements-and-filedelete-events-7a74f17ca842) ), this type of traffic should get caught quickly.

Another example of a Forward Proxy is Burp Suite, as most people utilize it to forward HTTP Requests. However, this application is the swiss army knife of HTTP Proxies and can be configured to be a reverse proxy or transparent!

#### Forward Proxy

![Diagram showing Host A sending an HTTP request through a Forward Proxy to the Internet, reaching a Webserver. Host B is also connected.](https://academy.hackthebox.com/storage/modules/34/redesigned/forward_proxy.png)

* * *

## Reverse Proxy

As you may have guessed, a `reverse proxy`, is the reverse of a `Forward Proxy`. Instead of being designed to filter outgoing requests, it filters incoming ones. The most common goal with a `Reverse Proxy`, is to listen on an address and forward it to a closed-off network.

Many organizations use CloudFlare as they have a robust network that can withstand most DDOS Attacks. By using Cloudflare, organizations have a way to filter the amount (and type) of traffic that gets sent to their webservers.

Penetration Testers will configure reverse proxies on infected endpoints. The infected endpoint will listen on a port and send any client that connects to the port back to the attacker through the infected endpoint. This is useful to bypass firewalls or evade logging. Organizations may have `IDS` ( `Intrusion Detection Systems`), watching external web requests. If the attacker gains access to the organization over SSH, a reverse proxy can send web requests through the SSH Tunnel and evade the IDS.

Another common Reverse Proxy is `ModSecurity`, a `Web Application Firewall` ( `WAF`). Web Application Firewalls inspect web requests for malicious content and block the request if it is malicious. If you want to learn more about this, we recommend reading into the [ModSecurity Core Rule Set](https://owasp.org/www-project-modsecurity-core-rule-set/), as its a great starting point. Cloudflare, also can act as a WAF but doing so requires letting them decrypt HTTPS Traffic, which some organizations may not want.

#### Reverse Proxy

![Diagram showing Host A sending an HTTP request through the Internet, passing firewalls, a Reverse Proxy, and reaching a Webserver. Host B is also connected.](https://academy.hackthebox.com/storage/modules/34/redesigned/reverse_proxy.png)

* * *

## (Non-) Transparent Proxy

All these proxy services act either `transparently` or `non-transparently`.

With a `transparent proxy`, the client doesn't know about its existence. The transparent proxy intercepts the client's communication requests to the Internet and acts as a substitute instance. To the outside, the transparent proxy, like the non-transparent proxy, acts as a communication partner.

If it is a `non-transparent proxy`, we must be informed about its existence. For this purpose, we and the software we want to use are given a special proxy configuration that ensures that traffic to the Internet is first addressed to the proxy. If this configuration does not exist, we cannot communicate via the proxy. However, since the proxy usually provides the only communication path to other networks, communication to the Internet is generally cut off without a corresponding proxy configuration.


# Networking Models

* * *

Two networking models describe the communication and transfer of data from one host to another, called `ISO/OSI model` and the `TCP/IP model`. This is a simplified representation of the so-called `layers` representing transferred Bits in readable contents for us.

![Comparison of OSI and TCP/IP models: OSI has 7 layers including Application, Presentation, Session, Transport, Network, Data-Link, and Physical. TCP/IP has 4 layers: Application, Transport, Internet, and Link.](https://academy.hackthebox.com/storage/modules/34/redesigned/net_models4.png)

* * *

## The OSI Model

The `OSI` model, often referred to as `ISO/OSI` layer model, is a reference model that can be used to describe and define the communication between systems. The reference model has `seven` individual layers, each with clearly separated tasks.

The term `OSI` stands for `Open Systems Interconnection` model, published by the `International Telecommunication Union` ( `ITU`) and the `International Organization for Standardization` ( `ISO`). Therefore, the `OSI` model is often referred to as the `ISO/OSI` layer model.

* * *

## The TCP/IP Model

`TCP/IP` ( `Transmission Control Protocol`/ `Internet Protocol`) is a generic term for many network protocols. The protocols are responsible for the switching and transport of data packets on the Internet. The Internet is entirely based on the `TCP/IP` protocol family. However, `TCP/IP` does not only refer to these two protocols but is usually used as a generic term for an entire protocol family.

For example, `ICMP` ( `Internet Control Message Protocol`) or `UDP` ( `User Datagram Protocol`) belongs to the protocol family. The protocol family provides the necessary functions for transporting and switching data packets in a private or public network.

* * *

## ISO/OSI vs. TCP/IP

`TCP/IP` is a communication protocol that allows hosts to connect to the Internet. It refers to the `Transmission Control Protocol` used in and by applications on the Internet. In contrast to `OSI`, it allows a lightening of the rules that must be followed, provided that general guidelines are followed.

`OSI`, on the other hand, is a communication gateway between the network and end-users. The OSI model is usually referred to as the reference model because it is newer and more widely used. It is also known for its strict protocol and limitations.

* * *

## Packet Transfers

In a layered system, devices in a layer exchange data in a different format called a `protocol data unit` ( `PDU`). For example, when we want to browse a website on the computer, the remote server software first passes the requested data to the application layer. It is processed layer by layer, each layer performing its assigned functions. The data is then transferred through the network's physical layer until the destination server or another device receives it. The data is routed through the layers again, with each layer performing its assigned operations until the receiving software uses the data.

![Comparison of OSI and TCP/IP models with PDUs: OSI has 7 layers including Application, Presentation, Session, Transport, Network, Data-Link, and Physical. TCP/IP has 4 layers: Application, Transport, Internet, and Link. PDUs are Data, Segment/Datagram, Packet, Frame, and Bit.](https://academy.hackthebox.com/storage/modules/34/redesigned/net_models_pdu2.png)

During the transmission, each layer adds a `header` to the `PDU` from the upper layer, which controls and identifies the packet. This process is called `encapsulation`. The header and the data together form the PDU for the next layer. The process continues to the `Physical Layer` or `Network Layer`, where the data is transmitted to the receiver. The receiver reverses the process and unpacks the data on each layer with the header information. After that, the application finally uses the data. This process continues until all data has been sent and received.

![Diagram of packet transfer showing data encapsulation from sender to receiver through layers: Data, TCP, IP, MAC, and Binary Transmission, with corresponding headers and sequence.](https://academy.hackthebox.com/storage/modules/34/packet_transfer.png)

For us, as penetration testers, both reference models are useful. With `TCP/IP`, we can quickly understand how the entire connection is established, and with `ISO`, we can take it apart piece by piece and analyze it in detail. This often happens when we can listen to and intercept specific network traffic. We then have to analyze this traffic accordingly, going into more detail in the `Network Traffic Analysis` module. Therefore, we should familiarize ourselves with both reference models and understand and internalize them in the best possible way.


# The OSI Model

* * *

The goal in defining the `ISO/OSI` standard was to create a reference model that enables the communication of different technical systems via various devices and technologies and provides compatibility. The `OSI` model uses `seven` different layers, which are hierarchically based on each other to achieve this goal. These layers represent phases in the establishment of each connection through which the sent packets pass. In this way, the standard was created to trace how a connection is structured and established visually.

| **Layer** | **Function** |
| --- | --- |
| `7.Application` | Among other things, this layer controls the input and output of data and provides the application functions. |
| `6.Presentation` | The presentation layer's task is to transfer the system-dependent presentation of data into a form independent of the application. |
| `5.Session` | The session layer controls the logical connection between two systems and prevents, for example, connection breakdowns or other problems. |
| `4.Transport` | Layer 4 is used for end-to-end control of the transferred data. The Transport Layer can detect and avoid congestion situations and segment data streams. |
| `3.Network` | On the networking layer, connections are established in circuit-switched networks, and data packets are forwarded in packet-switched networks. Data is transmitted over the entire network from the sender to the receiver. |
| `2.Data Link` | The central task of layer 2 is to enable reliable and error-free transmissions on the respective medium. For this purpose, the bitstreams from layer 1 are divided into blocks or frames. |
| `1.Physical` | The transmission techniques used are, for example, electrical signals, optical signals, or electromagnetic waves. Through layer 1, the transmission takes place on wired or wireless transmission lines. |

* * *

The layers `2-4` are `transport oriented`, and the layers `5-7` are `application oriented` layers. In each layer, precisely defined tasks are performed, and the interfaces to the neighboring layers are precisely described. Each layer offers services for use to the layer directly above it. To make these services available, the layer uses the services of the layer below it and performs the tasks of its layer.

If two systems communicate, all seven layers of the `OSI` model are run through at least `twice`, since both the sender and the receiver must take the layer model into account. Therefore, a large number of different tasks must be performed in the individual layers to ensure the communication's security, reliability, and performance.

When an application sends a packet to the other system, the system works the layers shown above from layer `7` down to layer `1`, and the receiving system unpacks the received packet from layer `1` up to layer `7`.


# The TCP/IP Model

* * *

The `TCP/IP` model is also a layered reference model, often referred to as the `Internet Protocol Suite`. The term `TCP/IP` stands for the two protocols `Transmission Control Protocol` ( `TCP`) and `Internet Protocol` ( `IP`). `IP` is located within the `network layer` ( `Layer 3`) and `TCP` is located within the `transport layer` ( `Layer 4`) of the `OSI` layer model.

| **Layer** | **Function** |
| --- | --- |
| `4.Application` | The Application Layer allows applications to access the other layers' services and defines the protocols applications use to exchange data. |
| `3.Transport` | The Transport Layer is responsible for providing (TCP) session and (UDP) datagram services for the Application Layer. |
| `2.Internet` | The Internet Layer is responsible for host addressing, packaging, and routing functions. |
| `1.Link` | The Link layer is responsible for placing the TCP/IP packets on the network medium and receiving corresponding packets from the network medium. TCP/IP is designed to work independently of the network access method, frame format, and medium. |

* * *

With `TCP/IP`, every application can transfer and exchange data over any network, and it does not matter where the receiver is located. `IP` ensures that the data packet reaches its destination, and `TCP` controls the data transfer and ensures the connection between data stream and application. The main difference between `TCP/IP` and `OSI` is the number of layers, some of which have been combined.

![Comparison of OSI and TCP/IP models: OSI has 7 layers including Application, Presentation, Session, Transport, Network, Data-Link, and Physical. TCP/IP has 4 layers: Application, Transport, Internet, and Link.](https://academy.hackthebox.com/storage/modules/34/redesigned/net_models4.png)

The most important tasks of `TCP/IP` are:

| **Task** | **Protocol** | **Description** |
| --- | --- | --- |
| `Logical Addressing` | `IP` | Due to many hosts in different networks, there is a need to structure the network topology and logical addressing. Within TCP/IP, IP takes over the logical addressing of networks and nodes. Data packets only reach the network where they are supposed to be. The methods to do so are `network classes`, `subnetting`, and `CIDR`. |
| `Routing` | `IP` | For each data packet, the next node is determined in each node on the way from the sender to the receiver. This way, a data packet is routed to its receiver, even if its location is unknown to the sender. |
| `Error & Control Flow` | `TCP` | The sender and receiver are frequently in touch with each other via a virtual connection. Therefore control messages are sent continuously to check if the connection is still established. |
| `Application Support` | `TCP` | TCP and UDP ports form a software abstraction to distinguish specific applications and their communication links. |
| `Name Resolution` | `DNS` | DNS provides name resolution through Fully Qualified Domain Names (FQDN) in IP addresses, enabling us to reach the desired host with the specified name on the internet. |


# Network Layer

* * *

The `network layer` ( `Layer 3`) of `OSI` controls the exchange of data packets, as these cannot be directly routed to the receiver and therefore have to be provided with routing nodes. The data packets are then transferred from node to node until they reach their target. To implement this, the `network layer` identifies the individual network nodes, sets up and clears connection channels, and takes care of routing and data flow control. When sending the packets, addresses are evaluated, and the data is routed through the network from node to node. There is usually no processing of the data in the layers above the `L3` in the nodes. Based on the addresses, the routing and the construction of routing tables are done.

In short, it is responsible for the following functions:

- `Logical Addressing`
- `Routing`

Protocols are defined in each layer of `OSI`, and these protocols represent a collection of rules for communication in the respective layer. They are transparent to the protocols of the layers above or below. Some protocols fulfill tasks of several layers and extend over two or more layers. The most used protocols on this layer are:

- `IPv4` / `IPv6`
- `IPsec`
- `ICMP`
- `IGMP`
- `RIP`
- `OSPF`

It ensures the routing of packets from source to destination within or outside a subnet. These two subnets may have different addressing schemes or incompatible addressing types. In both cases, the data transmission in each case goes through the entire communication network and includes routing between the network nodes. Since direct communication between the sender and the receiver is not always possible due to the different subnets, packets must be forwarded from nodes (routers) that are on the way. Forwarded packets do not reach the higher layers but are assigned a new intermediate destination and sent to the next node.


# IP Addresses

* * *

Each host in the network located can be identified by the so-called `Media Access Control` address ( `MAC`). This would allow data exchange within this one network. If the remote host is located in another network, knowledge of the `MAC` address is not enough to establish a connection. Addressing on the Internet is done via the `IPv4` and/or `IPv6` address, which is made up of the `network address` and the `host address`.

It does not matter whether it is a smaller network, such as a home computer network, or the entire Internet. The IP address ensures the delivery of data to the correct receiver. We can imagine the representation of `MAC` and `IPv4` / `IPv6` addresses as follows:

- `IPv4` / `IPv6` \- describes the unique postal address and district of the receiver's building.
- `MAC` \- describes the exact floor and apartment of the receiver.

It is possible for a single IP address to address multiple receivers (broadcasting) or for a device to respond to multiple IP addresses. However, it must be ensured that each IP address is assigned only once within the network.

* * *

## IPv4 Structure

The most common method of assigning IP addresses is `IPv4`, which consists of a `32`-bit binary number combined into `4 bytes` consisting of `8`-bit groups ( `octets`) ranging from `0-255`. These are converted into more easily readable decimal numbers, separated by dots and represented as dotted-decimal notation.

Thus an IPv4 address can look like this:

| **Notation** | **Presentation** |
| --- | --- |
| Binary | 0111 1111.0000 0000.0000 0000.0000 0001 |
| Decimal | 127.0.0.1 |

Each network interface (network cards, network printers, or routers) is assigned a unique IP address.

The `IPv4` format allows 4,294,967,296 unique addresses. The IP address is divided into a `host part` and a `network part`. The `router` assigns the `host part` of the IP address at home or by an administrator. The respective `network administrator` assigns the `network part`. On the Internet, this is `IANA`, which allocates and manages the unique IPs.

In the past, further classification took place here. The IP network blocks were divided into `classes A - E`. The different classes differed in the host and network shares' respective lengths.

| **`Class`** | **Network Address** | **First Address** | **Last Address** | **Subnetmask** | **CIDR** | **Subnets** | **IPs** |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `A` | 1.0.0.0 | 1.0.0.1 | 127.255.255.255 | 255.0.0.0 | /8 | 127 | 16,777,214 + 2 |
| `B` | 128.0.0.0 | 128.0.0.1 | 191.255.255.255 | 255.255.0.0 | /16 | 16,384 | 65,534 + 2 |
| `C` | 192.0.0.0 | 192.0.0.1 | 223.255.255.255 | 255.255.255.0 | /24 | 2,097,152 | 254 + 2 |
| `D` | 224.0.0.0 | 224.0.0.1 | 239.255.255.255 | Multicast | Multicast | Multicast | Multicast |
| `E` | 240.0.0.0 | 240.0.0.1 | 255.255.255.255 | reserved | reserved | reserved | reserved |

* * *

## Subnet Mask

A further separation of these classes into small networks is done with the help of `subnetting`. This separation is done using the `netmasks`, which is as long as an IPv4 address. As with classes, it describes which bit positions within the IP address act as `network part` or `host part`.

| **Class** | **Network Address** | **First Address** | **Last Address** | **`Subnetmask`** | **CIDR** | **Subnets** | **IPs** |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **A** | 1.0.0.0 | 1.0.0.1 | 127.255.255.255 | `255.0.0.0` | /8 | 127 | 16,777,214 + 2 |
| **B** | 128.0.0.0 | 128.0.0.1 | 191.255.255.255 | `255.255.0.0` | /16 | 16,384 | 65,534 + 2 |
| **C** | 192.0.0.0 | 192.0.0.1 | 223.255.255.255 | `255.255.255.0` | /24 | 2,097,152 | 254 + 2 |
| **D** | 224.0.0.0 | 224.0.0.1 | 239.255.255.255 | `Multicast` | Multicast | Multicast | Multicast |
| **E** | 240.0.0.0 | 240.0.0.1 | 255.255.255.255 | `reserved` | reserved | reserved | reserved |

* * *

## Network and Gateway Addresses

The `two` additional `IPs` added in the `IPs column` are reserved for the so-called `network address` and the `broadcast address`. Another important role plays the `default gateway`, which is the name for the IPv4 address of the `router` that couples networks and systems with different protocols and manages addresses and transmission methods. It is common for the `default gateway` to be assigned the first or last assignable IPv4 address in a subnet. This is not a technical requirement, but has become a de-facto standard in network environments of all sizes.

| **Class** | **Network Address** | **`First Address`** | **Last Address** | **Subnetmask** | **CIDR** | **Subnets** | **`IPs`** |
| --- | --- | --- | --- | --- | --- | --- | --- |
| A | 1.0.0.0 | `1.0.0.1` | 127.255.255.255 | 255.0.0.0 | /8 | 127 | 16,777,214 `+ 2` |
| B | 128.0.0.0 | `128.0.0.1` | 191.255.255.255 | 255.255.0.0 | /16 | 16,384 | 65,534 `+ 2` |
| C | 192.0.0.0 | `192.0.0.1` | 223.255.255.255 | 255.255.255.0 | /24 | 2,097,152 | 254 `+ 2` |
| D | 224.0.0.0 | `224.0.0.1` | 239.255.255.255 | Multicast | Multicast | Multicast | Multicast |
| E | 240.0.0.0 | `240.0.0.1` | 255.255.255.255 | reserved | reserved | reserved | reserved |

* * *

## Broadcast Address

The `broadcast` IP address's task is to connect all devices in a network with each other. `Broadcast` in a network is a message that is transmitted to all participants of a network and does not require any response. In this way, a host sends a data packet to all other participants of the network simultaneously and, in doing so, communicates its `IP address`, which the receivers can use to contact it. This is the `last IPv4` address that is used for the `broadcast`.

| **Class** | **Network Address** | **First Address** | **`Last Address`** | **Subnetmask** | **CIDR** | **Subnets** | **IPs** |
| --- | --- | --- | --- | --- | --- | --- | --- |
| A | 1.0.0.0 | 1.0.0.1 | `127.255.255.255` | 255.0.0.0 | /8 | 127 | 16,777,214 + 2 |
| B | 128.0.0.0 | 128.0.0.1 | `191.255.255.255` | 255.255.0.0 | /16 | 16,384 | 65,534 + 2 |
| C | 192.0.0.0 | 192.0.0.1 | `223.255.255.255` | 255.255.255.0 | /24 | 2,097,152 | 254 + 2 |
| D | 224.0.0.0 | 224.0.0.1 | `239.255.255.255` | Multicast | Multicast | Multicast | Multicast |
| E | 240.0.0.0 | 240.0.0.1 | `255.255.255.255` | reserved | reserved | reserved | reserved |

* * *

## Binary system

The binary system is a number system that uses only two different states that are represented into two numbers ( `0` and `1`) opposite to the decimal-system (0 to 9).

An IPv4 address is divided into 4 octets, as we have already seen. Each `octet` consists of `8 bits`. Each position of a bit in an octet has a specific decimal value. Let's take the following IPv4 address as an example:

- IPv4 Address: `192.168.10.39`

Here is an example of how the `first octet` looks like:

#### 1st Octet - Value: 192

```shell
Values:         128  64  32  16  8  4  2  1
Binary:           1   1   0   0  0  0  0  0

```

If we calculate the sum of all these values for each octet where the bit is set to `1`, we get the sum:

| **Octet** | **Values** | **Sum** |
| --- | --- | --- |
| 1st | 128 + 64 + 0 + 0 + 0 + 0 + 0 + 0 | = `192` |
| 2nd | 128 + 0 + 32 + 0 + 8 + 0 + 0 + 0 | = `168` |
| 3rd | 0 + 0 + 0 + 0 + 8 + 0 + 2 + 0 | = `10` |
| 4th | 0 + 0 + 32 + 0 + 0 + 4 + 2 + 1 | = `39` |

The entire representation from binary to decimal would look like this:

#### IPv4 - Binary Notation

```shell
Octet:             1st         2nd         3rd         4th
Binary:         1100 0000 . 1010 1000 . 0000 1010 . 0010 0111
Decimal:           192    .    168    .     10    .     39

```

- IPv4 Address: `192.168.10.39`

This addition takes place for each octet, which results in a decimal representation of the `IPv4 address`. The subnet mask is calculated in the same way.

#### IPv4 - Decimal to Binary

```shell
Values:         128  64  32  16  8  4  2  1
Binary:           1   1   1   1  1  1  1  1

```

| **Octet** | **Values** | **Sum** |
| --- | --- | --- |
| 1st | 128 + 64 + 32 + 16 + 8 + 4 + 2 + 1 | = `255` |
| 2nd | 128 + 64 + 32 + 16 + 8 + 4 + 2 + 1 | = `255` |
| 3rd | 128 + 64 + 32 + 16 + 8 + 4 + 2 + 1 | = `255` |
| 4th | 0 + 0 + 0 + 0 + 0 + 0 + 0 + 0 | = `0` |

#### Subnet Mask

```shell
Octet:             1st         2nd         3rd         4th
Binary:         1111 1111 . 1111 1111 . 1111 1111 . 0000 0000
Decimal:           255    .    255    .    255    .     0

```

- IPv4 Address: `192.168.10.39`

- Subnet mask: `255.255.255.0`


* * *

## CIDR

`Classless Inter-Domain Routing` ( `CIDR`) is a method of representation and replaces the fixed assignment between IPv4 address and network classes (A, B, C, D, E). The division is based on the subnet mask or the so-called `CIDR suffix`, which allows the bitwise division of the IPv4 address space and thus into `subnets` of any size. The `CIDR suffix` indicates how many bits from the beginning of the IPv4 address belong to the network. It is a notation that represents the `subnet mask` by specifying the number of `1`-bits in the subnet mask.

Let us stick to the following IPv4 address and subnet mask as an example:

- IPv4 Address: `192.168.10.39`

- Subnet mask: `255.255.255.0`


Now the whole representation of the IPv4 address and the subnet mask would look like this:

- CIDR: `192.168.10.39/24`

The CIDR suffix is, therefore, the sum of all ones in the subnet mask.

```shell
Octet:             1st         2nd         3rd         4th
Binary:         1111 1111 . 1111 1111 . 1111 1111 . 0000 0000 (/24)
Decimal:           255    .    255    .    255    .     0

```


# Subnetting

* * *

The division of an address range of IPv4 addresses into several smaller address ranges is called `subnetting`.

A subnet is a logical segment of a network that uses IP addresses with the same network address. We can think of a subnet as a labeled entrance on a large building corridor. For example, this could be a glass door that separates various departments of a company building. With the help of subnetting, we can create a specific subnet by ourselves or find out the following outline of the respective network:

- `Network address`
- `Broadcast address`
- `First host`
- `Last host`
- `Number of hosts`

Let us take the following IPv4 address and subnet mask as an example:

- IPv4 Address: `192.168.12.160`
- Subnet Mask: `255.255.255.192`
- CIDR: `192.168.12.160/26`

* * *

We already know that an IP address is divided into the `network part` and the `host part`.

#### Network Part

| **Details of** | **1st Octet** | **2nd Octet** | **3rd Octet** | **4th Octet** | **Decimal** |
| --- | --- | --- | --- | --- | --- |
| IPv4 | `1100 0000` | `1010 1000` | `0000 1100` | `10` 10 0000 | 192.168.12.160 `/26` |
| Subnet mask | `1111 1111` | `1111 1111` | `1111 1111` | `11` 00 0000 | `255.255.255.192` |
| Bits | /8 | /16 | /24 | /32 |  |

In subnetting, we use the subnet mask as a template for the IPv4 address. From the `1`-bits in the subnet mask, we know which bits in the IPv4 address `cannot` be changed. These are `fixed` and therefore determine the "main network" in which the subnet is located.

#### Host Part

| **Details of** | **1st Octet** | **2nd Octet** | **3rd Octet** | **4th Octet** | **Decimal** |
| --- | --- | --- | --- | --- | --- |
| IPv4 | 1100 0000 | 1010 1000 | 0000 1100 | 10 `10 0000` | 192.168.12.160/26 |
| Subnet mask | 1111 1111 | 1111 1111 | 1111 1111 | 11 `00 0000` | 255.255.255.192 |
| Bits | /8 | /16 | /24 | /32 |  |

The bits in the `host part` can be changed to the `first` and `last` address. The first address is the `network address`, and the last address is the `broadcast address` for the respective subnet.

The `network address` is vital for the delivery of a data packet. If the `network address` is the same for the source and destination address, the data packet is delivered within the same subnet. If the network addresses are different, the data packet must be routed to another subnet via the `default gateway`.

The `subnet mask` determines where this separation occurs.

#### Separation Of Network & Host Parts

| **Details of** | **1st Octet** | **2nd Octet** | **3rd Octet** | **4th Octet** | **Decimal** |
| --- | --- | --- | --- | --- | --- |
| IPv4 | 1100 0000 | 1010 1000 | 0000 1100 | 10 `|` 10 0000 | 192.168.12.160/26 |
| Subnet mask | `1111 1111` | `1111 1111` | `1111 1111` | `11|` 00 0000 | 255.255.255.192 |
| Bits | /8 | /16 | /24 | /32 |  |

* * *

#### Network Address

So if we now set all bits to `0` in the `host part` of the IPv4 address, we get the respective subnet's `network address`.

| **Details of** | **1st Octet** | **2nd Octet** | **3rd Octet** | **4th Octet** | **Decimal** |
| --- | --- | --- | --- | --- | --- |
| IPv4 | 1100 0000 | 1010 1000 | 0000 1100 | 10 `|00 0000` | `192.168.12.128`/26 |
| Subnet mask | `1111 1111` | `1111 1111` | `1111 1111` | `11|` 00 0000 | 255.255.255.192 |
| Bits | /8 | /16 | /24 | /32 |  |

* * *

#### Broadcast Address

If we set all bits in the `host part` of the IPv4 address to `1`, we get the `broadcast address`.

| **Details of** | **1st Octet** | **2nd Octet** | **3rd Octet** | **4th Octet** | **Decimal** |
| --- | --- | --- | --- | --- | --- |
| IPv4 | 1100 0000 | 1010 1000 | 0000 1100 | 10 `|11 1111` | `192.168.12.191`/26 |
| Subnet mask | `1111 1111` | `1111 1111` | `1111 1111` | `11|` 00 0000 | 255.255.255.192 |
| Bits | /8 | /16 | /24 | /32 |  |

Since we now know that the IPv4 addresses `192.168.12.128` and `192.168.12.191` are assigned, all other IPv4 addresses are accordingly between `192.168.12.129-190`. Now we know that this subnet offers us a total of `64 - 2` (network address & broadcast address) or `62` IPv4 addresses that we can assign to our hosts.

| **Hosts** | **IPv4** |
| --- | --- |
| Network Address | `192.168.12.128` |
| First Host | `192.168.12.129` |
| Other Hosts | `...` |
| Last Host | `192.168.12.190` |
| Broadcast Address | `192.168.12.191` |

* * *

## Subnetting Into Smaller Networks

Let us now assume that we, as administrators, have been given the task of dividing the subnet assigned to us into 4 additional subnets. Thus, it is essential to know that we can only divide the subnets based on the binary system.

| **Exponent** | **Value** |
| --- | --- |
| 2 `^0` | = 1 |
| 2 `^1` | = 2 |
| 2 `^2` | = 4 |
| 2 `^3` | = 8 |
| 2 `^4` | = 16 |
| 2 `^5` | = 32 |
| 2 `^6` | = 64 |
| 2 `^7` | = 128 |
| 2 `^8` | = 256 |

* * *

Therefore we can divide the `64 hosts` we know by `4`. The `4` is equal to the exponent 2 `^2` in the binary system, so we find out the number of bits for the subnet mask by which we have to extend it. So we know the following parameters:

- Subnet: `192.168.12.128/26`
- Required Subnets: `4`

Now we increase/expand our subnet mask by `2 bits` from `/26` to `/28`, and it looks like this:

| **Details of** | **1st Octet** | **2nd Octet** | **3rd Octet** | **4th Octet** | **Decimal** |
| --- | --- | --- | --- | --- | --- |
| IPv4 | 1100 0000 | 1010 1000 | 0000 1100 | 1000 `|` 0000 | 192.168.12.128 `/28` |
| Subnet mask | `1111 1111` | `1111 1111` | `1111 1111` | `1111|` 0000 | `255.255.255.240` |
| Bits | /8 | /16 | /24 | /32 |  |

Next, we can divide the `64` IPv4 addresses that are available to us into `4 parts`:

| **Hosts** | **Math** | **Subnets** | **Host range for each subnet** |
| --- | --- | --- | --- |
| 64 | / | 4 | = `16` |

So we know how big each subnet will be. From now on, we start from the network address given to us (192.168.12.128) and add the `16` hosts `4` times:

| **Subnet No.** | **Network Address** | **First Host** | **Last Host** | **Broadcast Address** | **CIDR** |
| --- | --- | --- | --- | --- | --- |
| 1 | `192.168.12.128` | 192.168.12.129 | 192.168.12.142 | `192.168.12.143` | 192.168.12.128/28 |
| 2 | `192.168.12.144` | 192.168.12.145 | 192.168.12.158 | `192.168.12.159` | 192.168.12.144/28 |
| 3 | `192.168.12.160` | 192.168.12.161 | 192.168.12.174 | `192.168.12.175` | 192.168.12.160/28 |
| 4 | `192.168.12.176` | 192.168.12.177 | 192.168.12.190 | `192.168.12.191` | 192.168.12.176/28 |

* * *

## Mental Subnetting

It may seem like there is a lot of math involved in subnetting, but each octet repeats itself, and everything is a power of two, so there doesn't have to be a lot of memorization. The first thing to do is identify what octet changes.

| **1st Octet** | **2nd Octet** | **3rd Octet** | **4th Octet** |
| --- | --- | --- | --- |
| /8 | /16 | /24 | /32 |

It is possible to identify what octet of the IP Address may change by remembering those four numbers. Given the Network Address: `192.168.1.1/25`, it is immediately apparent that 192.168.2.4 would not be in the same network because the `/25` subnet means only the fourth octet may change.

The next part identifies how big each subnet can be but by dividing eight by the network and looking at the `remainder`. This is also called `Modulo Operation (%)` and is heavily utilized in cryptology. Given our previous example of `/25`, `(25 % 8)` would be 1. This is because eight goes into 25 three times (8 \* 3 = 24). There is a 1 leftover, which is the network bit reserved for the network mask. There is a total of eight bits in each octet of an IP Address. If one is used for the network mask, the equation becomes 2^(8-1) or 2^7, 128. The table below contains all the numbers.

| **Remainder** | **Number** | **Exponential Form** | **Division Form** |
| --- | --- | --- | --- |
| 0 | 256 | 2^8 | 256 |
| 1 | 128 | 2^7 | 256/2 |
| 2 | 64 | 2^6 | 256/2/2 |
| 3 | 32 | 2^5 | 256/2/2/2 |
| 4 | 16 | 2^4 | 256/2/2/2/2 |
| 5 | 8 | 2^3 | 256/2/2/2/2/2 |
| 6 | 4 | 2^2 | 256/2/2/2/2/2/2 |
| 7 | 2 | 2^1 | 256/2/2/2/2/2/2/2 |

By remembering the powers of two up to eight, it can become an instant calculation. However, if forgotten, it may be quicker to remember to divide 256 in half the number of times of the remainder.

The tricky part of this is getting the actual IP Address range because 0 is a number and not null in networking. So in our `/25` with 128 IP Addresses, the first range is `192.168.1.0-127`. The first address is the network, and the last is the broadcast address, which means the usable IP Space would become `192.168.1.1-126`. If our IP Address fell above 128, then the `usable ip space` would be 192.168.1.129-254 (128 is the network and 255 is the broadcast).

Enable step-by-step solutions for all questions
![sparkles-icon-decoration](https://academy.hackthebox.com/images/sparkles-solid.svg)

#### Questions

Answer the question(s) below
to complete this Section and earn cubes!

\+ 2  Submit the decimal representation of the subnet mask from the following CIDR: 10.200.20.0/27


Submit


\+ 2  Submit the broadcast address of the following CIDR: 10.200.20.0/27


Submit


\+ 3  Split the network 10.200.20.0/27 into 4 subnets and submit the network address of the 3rd subnet as the answer.


Submit


\+ 3  Split the network 10.200.20.0/27 into 4 subnets and submit the broadcast address of the 2nd subnet as the answer.


Submit


# MAC Addresses

* * *

Each host in a network has its own `48`-bit ( `6 octets`) `Media Access Control` ( `MAC`) address, represented in hexadecimal format. `MAC` is the `physical address` for our network interfaces. There are several different standards for the MAC address:

- Ethernet (IEEE 802.3)
- Bluetooth (IEEE 802.15)
- WLAN (IEEE 802.11)

This is because the `MAC` address addresses the physical connection (network card, Bluetooth, or WLAN adapter) of a host. Each network card has its individual MAC address, which is configured once on the manufacturer's hardware side but can always be changed, at least temporarily.

Let's have a look at an example of such a MAC address:

MAC address:

- `DE:AD:BE:EF:13:37`
- `DE-AD-BE-EF-13-37`
- `DEAD.BEEF.1337`

| **Representation** | **1st Octet** | **2nd Octet** | **3rd Octet** | **4th Octet** | **5th Octet** | **6th Octet** |
| --- | --- | --- | --- | --- | --- | --- |
| Binary | 1101 1110 | 1010 1101 | 1011 1110 | 1110 1111 | 0001 0011 | 0011 0111 |
| Hex | DE | AD | BE | EF | 13 | 37 |

* * *

When an IP packet is delivered, it must be addressed on `layer 2` to the destination host's physical address or to the router / NAT, which is responsible for routing. Each packet has a `sender address` and a `destination address`.

The MAC address consists of a total of `6 bytes`. The first half ( `3 bytes` / `24 bit`) is the so-called `Organization Unique Identifier` ( `OUI`) defined by the `Institute of Electrical and Electronics Engineers` ( `IEEE`) for the respective manufacturers.

| **Representation** | **1st Octet** | **2nd Octet** | **3rd Octet** | **4th Octet** | **5th Octet** | **6th Octet** |
| --- | --- | --- | --- | --- | --- | --- |
| Binary | `1101 1110` | `1010 1101` | `1011 1110` | 1110 1111 | 0001 0011 | 0011 0111 |
| Hex | `DE` | `AD` | `BE` | EF | 13 | 37 |

* * *

The last half of the MAC address is called the `Individual Address Part` or `Network Interface Controller` ( `NIC`), which the manufacturers assign. The manufacturer sets this bit sequence only once and thus ensures that the complete address is unique.

| **Representation** | **1st Octet** | **2nd Octet** | **3rd Octet** | **4th Octet** | **5th Octet** | **6th Octet** |
| --- | --- | --- | --- | --- | --- | --- |
| Binary | 1101 1110 | 1010 1101 | 1011 1110 | `1110 1111` | `0001 0011` | `0011 0111` |
| Hex | DE | AD | BE | `EF` | `13` | `37` |

If a host with the IP target address is located in the same subnet, the delivery is made directly to the target computer's physical address. However, if this host belongs to a different subnet, the Ethernet frame is addressed to the `MAC address` of the responsible router ( `default gateway`). If the Ethernet frame's destination address matches its own `layer 2 address`, the router will forward the frame to the higher layers. `Address Resolution Protocol` ( `ARP`) is used in IPv4 to determine the MAC addresses associated with the IP addresses.

As with IPv4 addresses, there are also certain reserved areas for the MAC address. These include, for example, the local range for the MAC.

| **Local Range** |
| --- |
| 0 `2`:00:00:00:00:00 |
| 0 `6`:00:00:00:00:00 |
| 0 `A`:00:00:00:00:00 |
| 0 `E`:00:00:00:00:00 |

Furthermore, the last two bits in the first octet can play another essential role. The last bit can have two states, 0 and 1, as we already know. The last bit identifies the MAC address as `Unicast` ( `0`) or `Multicast` ( `1`). With `unicast`, it means that the packet sent will reach only one specific host.

#### MAC Unicast

| **Representation** | **1st Octet** | **2nd Octet** | **3rd Octet** | **4th Octet** | **5th Octet** | **6th Octet** |
| --- | --- | --- | --- | --- | --- | --- |
| Binary | 1101 111 `0` | 1010 1101 | 1011 1110 | 1110 1111 | 0001 0011 | 0011 0111 |
| Hex | D `E` | AD | BE | EF | 13 | 37 |

* * *

With `multicast`, the packet is sent only once to all hosts on the local network, which then decides whether or not to accept the packet based on their configuration. The `multicast` address is a unique address, just like the `broadcast` address, which has fixed octet values. `Broadcast` in a network represents a broadcasted call, where data packets are transmitted simultaneously from one point to all members of a network. It is mainly used if the address of the receiver of the packet is not yet known. An example is the `ARP` ( `for MAC addresses`) and DHCP ( `for IPv4 addresses`) protocols.

The defined values of each octet are marked `green`.

#### MAC Multicast

| **Representation** | **1st Octet** | **2nd Octet** | **3rd Octet** | **4th Octet** | **5th Octet** | **6th Octet** |
| --- | --- | --- | --- | --- | --- | --- |
| Binary | `0000 0001` | `0000 0000` | `0101 1110` | 1110 1111 | 0001 0011 | 0011 0111 |
| Hex | `01` | `00` | `5E` | EF | 13 | 37 |

#### MAC Broadcast

| **Representation** | **1st Octet** | **2nd Octet** | **3rd Octet** | **4th Octet** | **5th Octet** | **6th Octet** |
| --- | --- | --- | --- | --- | --- | --- |
| Binary | `1111 1111` | `1111 1111` | `1111 1111` | `1111 1111` | `1111 1111` | `1111 1111` |
| Hex | `FF` | `FF` | `FF` | `FF` | `FF` | `FF` |

* * *

The second last bit in the first octet identifies whether it is a `global OUI`, defined by the IEEE, or a `locally administrated` MAC address.

#### Global OUI

| **Representation** | **1st Octet** | **2nd Octet** | **3rd Octet** | **4th Octet** | **5th Octet** | **6th Octet** |
| --- | --- | --- | --- | --- | --- | --- |
| Binary | 1101 11 `0` 0 | 1010 1101 | 1011 1110 | 1110 1111 | 0001 0011 | 0011 0111 |
| Hex | D `C` | AD | BE | EF | 13 | 37 |

#### Locally Administrated

| **Representation** | **1st Octet** | **2nd Octet** | **3rd Octet** | **4th Octet** | **5th Octet** | **6th Octet** |
| --- | --- | --- | --- | --- | --- | --- |
| Binary | 1101 11 `1` 0 | 1010 1101 | 1011 1110 | 1110 1111 | 0001 0011 | 0011 0111 |
| Hex | D `E` | AD | BE | EF | 13 | 37 |

* * *

## Address Resolution Protocol

MAC addresses can be changed/manipulated or spoofed, and as such, they should not be relied upon as a sole means of security or identification. Network administrators should implement additional security measures, such as network segmentation and strong authentication protocols, to protect against potential attacks.

There exist several attack vectors that can potentially be exploited through the use of MAC addresses:

- `MAC spoofing`: This involves altering the MAC address of a device to match that of another device, typically to gain unauthorized access to a network.

- `MAC flooding`: This involves sending many packets with different MAC addresses to a network switch, causing it to reach its MAC address table capacity and effectively preventing it from functioning correctly.

- `MAC address filtering`: Some networks may be configured only to allow access to devices with specific MAC addresses that we could potentially exploit by attempting to gain access to the network using a spoofed MAC address.


* * *

## Address Resolution Protocol

[Address Resolution Protocol](https://en.wikipedia.org/wiki/Address_Resolution_Protocol) ( `ARP`) is a network protocol. It is an important part of the network communication used to resolve a network layer (layer 3) IP address to a link layer (layer 2) MAC address. It maps a host's IP address to its corresponding MAC address to facilitate communication between devices on a [Local Area Network](https://en.wikipedia.org/wiki/Local_area_network) ( `LAN`). When a device on a LAN wants to communicate with another device, it sends a broadcast message containing the destination IP address and its own MAC address. The device with the matching IP address responds with its own MAC address, and the two devices can then communicate directly using their MAC addresses. This process is known as ARP resolution.

ARP is an important part of the network communication process because it allows devices to send and receive data using MAC addresses rather than IP addresses, which can be more efficient. Two types of request messages can be used:

#### ARP Request

When a device wants to communicate with another device on a LAN, it sends an ARP request to resolve the destination device's IP address to its MAC address. The request is broadcast to all devices on the LAN and contains the IP address of the destination device. The device with the matching IP address responds with its MAC address.

#### ARP Reply

When a device receives an ARP request, it sends an ARP reply to the requesting device with its MAC address. The reply message contains the IP and MAC addresses of both the requesting and the responding devices.

#### Tshark Capture of ARP Requests

```shell
1   0.000000 10.129.12.100 -> 10.129.12.255 ARP 60  Who has 10.129.12.101?  Tell 10.129.12.100
2   0.000015 10.129.12.101 -> 10.129.12.100 ARP 60  10.129.12.101 is at AA:AA:AA:AA:AA:AA

3   0.000030 10.129.12.102 -> 10.129.12.255 ARP 60  Who has 10.129.12.103?  Tell 10.129.12.102
4   0.000045 10.129.12.103 -> 10.129.12.102 ARP 60  10.129.12.103 is at BB:BB:BB:BB:BB:BB

```

The " `who has`" message in the first and third lines indicates that a device is requesting the MAC address for the specified IP address, while the second and fourth lines show the ARP reply with the MAC address of the destination device.

However, it is also vulnerable to attacks, such as [ARP Spoofing](https://en.wikipedia.org/wiki/ARP_spoofing), which can be used to intercept or manipulate traffic on the network. However, to protect against such attacks, it is important to implement security measures such as firewalls and intrusion detection systems.

`ARP spoofing`, also known as `ARP cache poisoning` or `ARP poison routing`, is an attack that can be done using tools like [Ettercap](https://github.com/Ettercap/ettercap) or [Cain & Abel](https://github.com/xchwarze/Cain) in which we send falsified ARP messages over a LAN. The goal is to associate our MAC address with the IP address of a legitimate device on the company's network, effectively allowing us to intercept traffic intended for the legitimate device. For example, this could look like the following:

```shell
1   0.000000 10.129.12.100 -> 10.129.12.101 ARP 60  10.129.12.100 is at AA:AA:AA:AA:AA:AA
2   0.000015 10.129.12.100 -> 10.129.12.255 ARP 60  Who has 10.129.12.101?  Tell 10.129.12.100
3   0.000030 10.129.12.101 -> 10.129.12.100 ARP 60  10.129.12.101 is at BB:BB:BB:BB:BB:BB
4   0.000045 10.129.12.100 -> 10.129.12.101 ARP 60  10.129.12.100 is at AA:AA:AA:AA:AA:AA

```

The first and fourth lines show us ( `10.129.12.100`) sending falsified ARP messages to the target, associating its MAC address with its IP address ( `10.129.12.101`). The second and third lines show the target sending an ARP request and replying to our MAC address. This indicates that we have poisoned the target's ARP cache and that all traffic intended for the target will now be sent to our MAC address.

We can use ARP poisoning to perform various activities, such as stealing sensitive information, redirecting traffic, or launching MITM attacks. However, to protect against ARP spoofing, it is important to use secure network protocols, such as IPSec or SSL, and to implement security measures, such as firewalls and intrusion detection systems.


# IPv6 Addresses

* * *

`IPv6` is the successor of IPv4. In contrast to IPv4, the `IPv6` address is `128` bit long. The `prefix` identifies the host and network parts. The Internet Assigned Numbers Authority ( `IANA`) is responsible for assigning IPv4 and IPv6 addresses and their associated network portions. In the long term, `IPv6` is expected to completely replace IPv4, which is still predominantly used on the Internet. In principle, however, IPv4 and IPv6 can be made available simultaneously ( `Dual Stack`).

IPv6 consistently follows the `end-to-end` principle and provides publicly accessible IP addresses for any end devices without the need for NAT. Consequently, an interface can have multiple IPv6 addresses, and there are special IPv6 addresses to which multiple interfaces are assigned.

`IPv6` is a protocol with many new features, which also has many other advantages over IPv4:

- Larger address space
- Address self-configuration (SLAAC)
- Multiple IPv6 addresses per interface
- Faster routing
- End-to-end encryption (IPsec)
- Data packages up to 4 GByte

| **Features** | **IPv4** | **IPv6** |
| --- | --- | --- |
| Bit length | 32-bit | 128 bit |
| OSI layer | Network Layer | Network Layer |
| Adressing range | ~ 4.3 billion | ~ 340 undecillion |
| Representation | Binary | Hexadecimal |
| Prefix notation | 10.10.10.0/24 | fe80::dd80:b1a9:6687:2d3b/64 |
| Dynamic addressing | DHCP | SLAAC / DHCPv6 |
| IPsec | Optional | Mandatory |

* * *

There are four different types of IPv6 addresses:

| **Type** | **Description** |
| --- | --- |
| `Unicast` | Addresses for a single interface. |
| `Anycast` | Addresses for multiple interfaces, where only one of them receives the packet. |
| `Multicast` | Addresses for multiple interfaces, where all receive the same packet. |
| `Broadcast` | Do not exist and is realized with multicast addresses. |

* * *

## Hexadecimal System

The `hexadecimal system` ( `hex`) is used to make the binary representation more readable and understandable. We can only show `10` ( `0-9`) states with the decimal system and `2` ( `0` / `1`) with the binary system by using a single character. In contrast to the binary and decimal system, we can use the hexadecimal system to show `16` ( `0-F`) states with a single character.

| **Decimal** | **Hex** | **Binary** |
| --- | --- | --- |
| 1 | 1 | 0001 |
| 2 | 2 | 0010 |
| 3 | 3 | 0011 |
| 4 | 4 | 0100 |
| 5 | 5 | 0101 |
| 6 | 6 | 0110 |
| 7 | 7 | 0111 |
| 8 | 8 | 1000 |
| 9 | 9 | 1001 |
| 10 | A | 1010 |
| 11 | B | 1011 |
| 12 | C | 1100 |
| 13 | D | 1101 |
| 14 | E | 1110 |
| 15 | F | 1111 |

Let's look at an example with an IPv4, at how the IPv4 address ( `192.168.12.160`) would look in hexadecimal representation.

| **Representation** | **1st Octet** | **2nd Octet** | **3rd Octet** | **4th Octet** |
| --- | --- | --- | --- | --- |
| Binary | 1100 0000 | 1010 1000 | 0000 1100 | 1010 0000 |
| `Hex` | `C0` | `A8` | `0C` | `A0` |
| Decimal | 192 | 168 | 12 | 160 |

* * *

In total, the IPv6 address consists of `16 bytes`. Because of its length, an `IPv6` address is represented in a `hexadecimal` notation. Therefore the `128 bits` are divided into `8 blocks` multiplied by 16 bits (or `4 hex` numbers). All four hex numbers are grouped and separated by a colon ( `:`) instead of a simple dot ( `.`) as in IPv4. To simplify the notation, we leave out leading at least `4` zeros in the blocks, and we can replace them with two colons ( `::`).

An IPv6 address can look like this:

- Full IPv6: `fe80:0000:0000:0000:dd80:b1a9:6687:2d3b/64`
- Short IPv6: `fe80::dd80:b1a9:6687:2d3b/64`

An IPv6 address consists of two parts:

- `Network Prefix` (network part)
- `Interface Identifier` also called `Suffix` (host part)

The `Network Prefix` identifies the network, subnet, or address range. The `Interface Identifier` is formed from the `48-bit MAC` address (which we will discuss later) of the interface and is converted to a `64-bit address` in the process. The default prefix length is `/64`. However, other typical prefixes are `/32`, `/48`, and `/56`. If we want to use our networks, we get a shorter prefix (e.g. `/56`) than `/64` from our provider.

In RFC 5952, the aforementioned IPv6 address notation was defined:

- All alphabetical characters are always written in lower case.
- All leading zeros of a block are always omitted.
- One or more consecutive blocks of `4 zeros` (hex) are shortened by two colons ( `::`).
- The shortening to two colons ( `::`) may only be performed `once` starting from the left.


# Networking Key Terminology

* * *

There are many different terms in the field of information technology. However, we only need to know some of them, only the essential ones. Information technology has become so big that it equals the medical sector, if not already surpasses it. The number of programming languages, functions, protocols, different procedures, areas of application, details, and at the same time, the number of errors that can occur. All these areas are so large that you can specialize your entire career in 1-2 areas.

The key terminology is the rough alphabet we need to know to understand what we will talk about in the other modules. We have created a list with many different but still with the most common protocols and their descriptions to create this foundation. It is important to note that this list is incomplete, and we will cover one or two protocols in other modules. However, we recommend that you review this list from time to time and expand it as you learn new protocols.

| **Protocol** | **Acronym** | **Description** |
| --- | --- | --- |
| Wired Equivalent Privacy | `WEP` | WEP is a type of security protocol that was commonly used to secure wireless networks. |
| Secure Shell | `SSH` | A secure network protocol used to log into and execute commands on a remote system |
| File Transfer Protocol | `FTP` | A network protocol used to transfer files from one system to another |
| Simple Mail Transfer Protocol | `SMTP` | A protocol used to send and receive emails |
| Hypertext Transfer Protocol | `HTTP` | A client-server protocol used to send and receive data over the internet |
| Server Message Block | `SMB` | A protocol used to share files, printers, and other resources in a network |
| Network File System | `NFS` | A protocol used to access files over a network |
| Simple Network Management Protocol | `SNMP` | A protocol used to manage network devices |
| Wi-Fi Protected Access | `WPA` | WPA is a wireless security protocol that uses a password to protect wireless networks from unauthorized access. |
| Temporal Key Integrity Protocol | `TKIP` | TKIP is also a security protocol used in wireless networks but less secure. |
| Network Time Protocol | `NTP` | It is used to synchronize the timing of computers on a network. |
| Virtual Local Area Network | `VLAN` | It is a way to segment a network into multiple logical networks. |
| VLAN Trunking Protocol | `VTP` | VTP is a Layer 2 protocol that is used to establish and maintain a virtual LAN (VLAN) spanning multiple switches. |
| Routing Information Protocol | `RIP` | RIP is a distance-vector routing protocol used in local area networks (LANs) and wide area networks (WANs). |
| Open Shortest Path First | `OSPF` | It is an interior gateway protocol (IGP) for routing traffic within a single Autonomous System (AS) in an Internet Protocol (IP) network. |
| Interior Gateway Routing Protocol | `IGRP` | IGRP is a Cisco proprietary interior gateway protocol designed for routing within autonomous systems. |
| Enhanced Interior Gateway Routing Protocol | `EIGRP` | It is an advanced distance-vector routing protocol that is used to route IP traffic within a network. |
| Pretty Good Privacy | `PGP` | PGP is an encryption program that is used to secure emails, files, and other types of data. |
| Network News Transfer Protocol | `NNTP` | NNTP is a protocol used for distributing and retrieving messages in newsgroups across the internet. |
| Cisco Discovery Protocol | `CDP` | It is a proprietary protocol developed by Cisco Systems that allows network administrators to discover and manage Cisco devices connected to the network. |
| Hot Standby Router Protocol | `HSRP` | HSRP is a protocol used in Cisco routers to provide redundancy in the event of a router or other network device failure. |
| Virtual Router Redundancy Protocol | `VRRP` | It is a protocol used to provide automatic assignment of available Internet Protocol (IP) routers to participating hosts. |
| Spanning Tree Protocol | `STP` | STP is a network protocol used to ensure a loop-free topology in Layer 2 Ethernet networks. |
| Terminal Access Controller Access-Control System | `TACACS` | TACACS is a protocol that provides centralized authentication, authorization, and accounting for network access. |
| Session Initiation Protocol | `SIP` | It is a signaling protocol used for establishing and terminating real-time voice, video and multimedia sessions over an IP network. |
| Voice Over IP | `VOIP` | VOIP is a technology that allows for telephone calls to be made over the internet. |
| Extensible Authentication Protocol | `EAP` | EAP is a framework for authentication that supports multiple authentication methods, such as passwords, digital certificates, one-time passwords, and public-key authentication. |
| Lightweight Extensible Authentication Protocol | `LEAP` | LEAP is a proprietary wireless authentication protocol developed by Cisco Systems. It is based on the Extensible Authentication Protocol (EAP) used in the Point-to-Point Protocol (PPP). |
| Protected Extensible Authentication Protocol | `PEAP` | PEAP is a security protocol that provides an encrypted tunnel for wireless networks and other types of networks. |
| Systems Management Server | `SMS` | SMS is a systems management solution that helps organizations manage their networks, systems, and mobile devices. |
| Microsoft Baseline Security Analyzer | `MBSA` | It is a free security tool from Microsoft that is used to detect potential security vulnerabilities in Windows computers, networks, and systems. |
| Supervisory Control and Data Acquisition | `SCADA` | It is a type of industrial control system that is used to monitor and control industrial processes, such as those in manufacturing, power generation, and water and waste treatment. |
| Virtual Private Network | `VPN` | VPN is a technology that allows users to create a secure, encrypted connection to another network over the internet. |
| Internet Protocol Security | `IPsec` | IPsec is a protocol used to provide secure, encrypted communication over a network. It is commonly used in VPNs, or Virtual Private Networks, to create a secure tunnel between two devices. |
| Point-to-Point Tunneling Protocol | `PPTP` | It is a protocol used to create a secure, encrypted tunnel for remote access. |
| Network Address Translation | `NAT` | NAT is a technology that allows multiple devices on a private network to connect to the internet using a single public IP address. NAT works by translating the private IP addresses of devices on the network into a single public IP address, which is then used to connect to the internet. |
| Carriage Return Line Feed | `CRLF` | Combines two control characters to indicate the end of a line and a start of a new one for certain text file formats. |
| Asynchronous JavaScript and XML | `AJAX` | Web development technique that allows creating dynamic web pages using JavaScript and XML/JSON. |
| Internet Server Application Programming Interface | `ISAPI` | Allows to create performance-oriented web extensions for web servers using a set of APIs. |
| Uniform Resource Identifier | `URI` | It is a syntax used to identify a resource on the Internet. |
| Uniform Resource Locator | `URL` | Subset of URI that identifies a web page or another resource on the Internet, including the protocol and the domain name. |
| Internet Key Exchange | `IKE` | IKE is a protocol used to set up a secure connection between two computers. It is used in virtual private networks (VPNs) to provide authentication and encryption for data transmission, protecting the data from outside eavesdropping and tampering. |
| Generic Routing Encapsulation | `GRE` | This protocol is used to encapsulate the data being transmitted within the VPN tunnel. |
| Remote Shell | `RSH` | It is a program under Unix that allows executing commands and programs on a remote computer. |


# Common Protocols

* * *

Internet protocols are standardized rules and guidelines defined in RFCs that specify how devices on a network should communicate with each other. They ensure that devices on a network can exchange information consistently and reliably, regardless of the hardware and software used. For devices to communicate on a network, they need to be connected through a communication channel, such as a wired or wireless connection. The devices then exchange information using a set of standardized protocols that define the format and structure of the data being transmitted. The two main types of connections used on networks are [Transmission Control Protocol](https://en.wikipedia.org/wiki/Transmission_Control_Protocol) ( `TCP`) and [User Datagram Protocol](https://en.wikipedia.org/wiki/User_Datagram_Protocol) ( `UDP`).

We need to deal with and know the different and most used protocols. As we have already learned, these protocols are the basis of all communication between our devices and computers in the networks. We have compiled below many of these protocols that we will be dealing with throughout the modules. The better we understand them, the more effectively we can work with them.

* * *

## Transmission Control Protocol

`TCP` is a `connection-oriented` protocol that establishes a virtual connection between two devices before transmitting data by using a [Three-Way-Handshake](https://en.wikipedia.org/wiki/Transmission_Control_Protocol#Connection_establishment). This connection is maintained until the data transfer is complete, and the devices can continue to send data back and forth as long as the connection is active.

For example, When we enter a URL into our web browser, the browser sends an HTTP request to the server hosting the website using `TCP`. The server responds by sending the HTML code for the website back to the browser using `TCP`. The browser then uses this code to render the website on our screen. This process relies on a `TCP` connection being established between the browser and the web server and maintained until the data transfer is complete. As a result, `TCP` is reliable but slower than UDP because it requires additional overhead for establishing and maintaining the connection.

| **Protocol** | **Acronym** | **Port** | **Description** |
| --- | --- | --- | --- |
| Telnet | `Telnet` | `23` | Remote login service |
| Secure Shell | `SSH` | `22` | Secure remote login service |
| Simple Network Management Protocol | `SNMP` | `161-162` | Manage network devices |
| Hyper Text Transfer Protocol | `HTTP` | `80` | Used to transfer webpages |
| Hyper Text Transfer Protocol Secure | `HTTPS` | `443` | Used to transfer secure webpages |
| Domain Name System | `DNS` | `53` | Lookup domain names |
| File Transfer Protocol | `FTP` | `20-21` | Used to transfer files |
| Trivial File Transfer Protocol | `TFTP` | `69` | Used to transfer files |
| Network Time Protocol | `NTP` | `123` | Synchronize computer clocks |
| Simple Mail Transfer Protocol | `SMTP` | `25` | Used for email transfer |
| Post Office Protocol | `POP3` | `110` | Used to retrieve emails |
| Internet Message Access Protocol | `IMAP` | `143` | Used to access emails |
| Server Message Block | `SMB` | `445` | Used to transfer files |
| Network File System | `NFS` | `111`, `2049` | Used to mount remote systems |
| Bootstrap Protocol | `BOOTP` | `67`, `68` | Used to bootstrap computers |
| Kerberos | `Kerberos` | `88` | Used for authentication and authorization |
| Lightweight Directory Access Protocol | `LDAP` | `389` | Used for directory services |
| Remote Authentication Dial-In User Service | `RADIUS` | `1812`, `1813` | Used for authentication and authorization |
| Dynamic Host Configuration Protocol | `DHCP` | `67`, `68` | Used to configure IP addresses |
| Remote Desktop Protocol | `RDP` | `3389` | Used for remote desktop access |
| Network News Transfer Protocol | `NNTP` | `119` | Used to access newsgroups |
| Remote Procedure Call | `RPC` | `135`, `137-139` | Used to call remote procedures |
| Identification Protocol | `Ident` | `113` | Used to identify user processes |
| Internet Control Message Protocol | `ICMP` | `0-255` | Used to troubleshoot network issues |
| Internet Group Management Protocol | `IGMP` | `0-255` | Used for multicasting |
| Oracle DB (Default/Alternative) Listener | `oracle-tns` | `1521`/ `1526` | The Oracle database default/alternative listener is a service that runs on the database host and receives requests from Oracle clients. |
| Ingres Lock | `ingreslock` | `1524` | Ingres database is commonly used for large commercial applications and as a backdoor that can execute commands remotely via RPC. |
| Squid Web Proxy | `http-proxy` | `3128` | Squid web proxy is a caching and forwarding HTTP web proxy used to speed up a web server by caching repeated requests. |
| Secure Copy Protocol | `SCP` | `22` | Securely copy files between systems |
| Session Initiation Protocol | `SIP` | `5060` | Used for VoIP sessions |
| Simple Object Access Protocol | `SOAP` | `80`, `443` | Used for web services |
| Secure Socket Layer | `SSL` | `443` | Securely transfer files |
| TCP Wrappers | `TCPW` | `113` | Used for access control |
| Internet Security Association and Key Management Protocol | `ISAKMP` | `500` | Used for VPN connections |
| Microsoft SQL Server | `ms-sql-s` | `1433` | Used for client connections to the Microsoft SQL Server. |
| Kerberized Internet Negotiation of Keys | `KINK` | `892` | Used for authentication and authorization |
| Open Shortest Path First | `OSPF` | `89` | Used for routing |
| Point-to-Point Tunneling Protocol | `PPTP` | `1723` | Is used to create VPNs |
| Remote Execution | `REXEC` | `512` | This protocol is used to execute commands on remote computers and send the output of commands back to the local computer. |
| Remote Login | `RLOGIN` | `513` | This protocol starts an interactive shell session on a remote computer. |
| X Window System | `X11` | `6000` | It is a computer software system and network protocol that provides a graphical user interface (GUI) for networked computers. |
| Relational Database Management System | `DB2` | `50000` | RDBMS is designed to store, retrieve and manage data in a structured format for enterprise applications such as financial systems, customer relationship management (CRM) systems. |

* * *

## User Datagram Protocol

On the other hand, `UDP` is a `connectionless` protocol, which means it does not establish a virtual connection before transmitting data. Instead, it sends the data packets to the destination without checking to see if they were received.

For example, when we stream or watch a video on a platform like YouTube, the video data is transmitted to our device using `UDP`. This is because the video can tolerate some data loss, and the transmission speed is more important than the reliability. If a few packets of video data are lost along the way, it will not significantly impact the overall quality of the video. This makes `UDP` faster than TCP but less reliable because there is no guarantee that the packets will reach their destination.

| **Protocol** | **Acronym** | **Port** | **Description** |
| --- | --- | --- | --- |
| Domain Name System | `DNS` | `53` | It is a protocol to resolve domain names to IP addresses. |
| Trivial File Transfer Protocol | `TFTP` | `69` | It is used to transfer files between systems. |
| Network Time Protocol | `NTP` | `123` | It synchronizes computer clocks in a network. |
| Simple Network Management Protocol | `SNMP` | `161` | It monitors and manages network devices remotely. |
| Routing Information Protocol | `RIP` | `520` | It is used to exchange routing information between routers. |
| Internet Key Exchange | `IKE` | `500` | Internet Key Exchange |
| Bootstrap Protocol | `BOOTP` | `68` | It is used to bootstrap hosts in a network. |
| Dynamic Host Configuration Protocol | `DHCP` | `67` | It is used to assign IP addresses to devices in a network dynamically. |
| Telnet | `TELNET` | `23` | It is a text-based remote access communication protocol. |
| MySQL | `MySQL` | `3306` | It is an open-source database management system. |
| Terminal Server | `TS` | `3389` | It is a remote access protocol used for Microsoft Windows Terminal Services by default. |
| NetBIOS Name | `netbios-ns` | `137` | It is used in Windows operating systems to resolve NetBIOS names to IP addresses on a LAN. |
| Microsoft SQL Server | `ms-sql-m` | `1434` | Used for the Microsoft SQL Server Browser service. |
| Universal Plug and Play | `UPnP` | `1900` | It is a protocol for devices to discover each other on the network and communicate. |
| PostgreSQL | `PGSQL` | `5432` | It is an object-relational database management system. |
| Virtual Network Computing | `VNC` | `5900` | It is a graphical desktop sharing system. |
| X Window System | `X11` | `6000-6063` | It is a computer software system and network protocol that provides GUI on Unix-like systems. |
| Syslog | `SYSLOG` | `514` | It is a standard protocol to collect and store log messages on a computer system. |
| Internet Relay Chat | `IRC` | `194` | It is a real-time Internet text messaging (chat) or synchronous communication protocol. |
| OpenPGP | `OpenPGP` | `11371` | It is a protocol for encrypting and signing data and communications. |
| Internet Protocol Security | `IPsec` | `500` | IPsec is also a protocol that provides secure, encrypted communication. It is commonly used in VPNs to create a secure tunnel between two devices. |
| Internet Key Exchange | `IKE` | `11371` | It is a protocol for encrypting and signing data and communications. |
| X Display Manager Control Protocol | `XDMCP` | `177` | XDMCP is a network protocol that allows a user to remotely log in to a computer running the X11. |

* * *

## ICMP

[Internet Control Message Protocol](https://en.wikipedia.org/wiki/Internet_Control_Message_Protocol) ( `ICMP`) is a protocol used by devices to communicate with each other on the Internet for various purposes, including error reporting and status information. It sends requests and messages between devices, which can be used to report errors or provide status information.

#### ICMP Requests

A request is a message sent by one device to another to request information or perform a specific action. An example of a request in ICMP is the `ping` request, which tests the connectivity between two devices. When one device sends a ping request to another, the second device responds with a `ping reply` message.

#### ICMP Messages

A message in ICMP can be either a request or a reply. In addition to ping requests and responses, ICMP supports other types of messages, such as error messages, `destination unreachable`, and `time exceeded` messages. These messages are used to communicate various types of information and errors between devices on the network.

For example, if a device tries to send a packet to another device and the packet cannot be delivered, the device can use ICMP to send an error message back to the sender. ICMP has two different versions:

- `ICMPv4`: For IPv4 only
- `ICMPv6`: For IPv6 only

ICMPv4 is the original version of `ICMP`, developed for use with IPv4. It is still widely used and is the most common version of ICMP. On the other hand, ICMPv6 was developed for IPv6. It includes additional functionality and is designed to address some of the limitations of ICMPv4.

| **Request Type** | **Description** |
| --- | --- |
| `Echo Request` | This message tests whether a device is reachable on the network. When a device sends an echo request, it expects to receive an echo reply message. For example, the tools `tracert` (Windows) or `traceroute` (Linux) always send ICMP echo requests. |
| `Timestamp Request` | This message determines the time on a remote device. |
| `Address Mask Request` | This message is used to request the subnet mask of a device. |

| **Message Type** | **Description** |
| --- | --- |
| `Echo reply` | This message is sent in response to an echo request message. |
| `Destination unreachable` | This message is sent when a device cannot deliver a packet to its destination. |
| `Redirect` | A router sends this message to inform a device that it should send its packets to a different router. |
| ` time exceeded` | This message is sent when a packet has taken too long to reach its destination. |
| `Parameter problem` | This message is sent when there is a problem with a packet's header. |
| `Source quench` | This message is sent when a device receives packets too quickly and cannot keep up. It is used to slow down the flow of packets. |

Another crucial part of ICMP for us is the [Time-To-Live](https://en.wikipedia.org/wiki/Time_to_live) ( `TTL`) field in the ICMP packet header that limits the packet's lifetime as it travels through the network. It prevents packets from circulating indefinitely on the network in the event of routing loops. Each time a packet passes through a router, the router decrements the `TTL value by 1`. When the TTL value reaches `0`, the router discards the packet and sends an ICMP `Time Exceeded` message back to the sender.

We can also use `TTL` to determine the number of hops a packet has taken and the approximate distance to the destination. For example, if a packet has a `TTL` of 10 and takes 5 hops to reach its destination, it can be inferred that the destination is approximately 5 hops away. For example, if we see a ping with the `TTL` value of `122`, it could mean that we are dealing with a Windows system ( `TTL 128` by default) that is 6 hops away.

However, it is also possible to guess the operating system based on the default `TTL` value used by the device. Each operating system typically has a default `TTL` value when sending packets. This value is set in the packet's header and is decremented by 1 each time the packet passes through a router. Therefore, examining a device's default `TTL` value makes it possible to infer which operating system the device is using. For example: Windows systems ( `2000/XP/2003/Vista/10`) typically have a default `TTL` value of 128, while macOS and Linux systems typically have a default `TTL` value of 64 and Solaris' default `TTL` value of 255. However, it is important to note that the user can change these values, so they should be independent of a definitive way to determine a device's operating system.

* * *

## VoIP

[Voice over Internet Protocol](https://www.fcc.gov/general/voice-over-internet-protocol-voip) ( `VoIP`) is a method of transmitting voice and multimedia communications. For example, it allows us to make phone calls using a broadband internet connection instead of a traditional phone line, like Skype, Whatsapp, Google Hangouts, Slack, Zoom, and others.

The most common VoIP ports are `TCP/5060` and `TCP/5061`, which are used for the [Session Initiation Protocol](https://en.wikipedia.org/wiki/Session_Initiation_Protocol) (SIP). However, the port `TCP/1720` may also be used by some VoIP systems for the [H.323 protocol](https://en.wikipedia.org/wiki/H.323), a set of standards for multimedia communication over packet-based networks. Still, SIP is more widely used than H.323 in VoIP systems.

Nevertheless, SIP is a signaling protocol for initiating, maintaining, modifying, and terminating real-time sessions involving video, voice, messaging, and other communications applications and services between two or more endpoints on the Internet. Therefore, it uses requests and methods between the endpoints. The most common SIP requests and methods are:

| **Method** | **Description** |
| --- | --- |
| `INVITE` | Initiates a session or invites another endpoint to participate. |
| `ACK` | Confirms the receipt of an INVITE request. |
| `BYE` | Terminate a session. |
| `CANCEL` | Cancels a pending INVITE request. |
| `REGISTER` | Registers a SIP user agent (UA) with a SIP server. |
| `OPTIONS` | Requests information about the capabilities of a SIP server or user agent, such as the types of media it supports. |

#### Information Disclosure

However, SIP allows us to enumerate existing users for potential attacks. This can be done for various purposes, such as determining a user's availability, finding out information about the user's capabilities or services, or performing brute-force attacks on user accounts later on.

One of the possible ways to enumerate users is the SIP `OPTIONS` request. It is a method used to request information about the capabilities of a SIP server or user agents, such as the types of media it supports, the codecs it can decode, and other details. The `OPTIONS` request can probe a SIP server or user agent for information or test its connectivity and availability.

During our analysis, it is possible to discover a `SEPxxxx.cnf` file, where `xxxx` is a unique identifier, is a configuration file used by Cisco Unified Communications Manager, formerly known as Cisco CallManager, to define the settings and parameters for a Cisco Unified IP Phone. The file specifies the phone model, firmware version, network settings, and other details.


# Wireless Networks

* * *

Wireless networks are computer networks that use wireless data connections between network nodes. These networks allow devices such as laptops, smartphones, and tablets to communicate with each other and the Internet without needing physical connections such as cables.

Wireless networks use radio frequency ( `RF`) technology to transmit data between devices. Each device on a wireless network has a wireless adapter that converts data into RF signals and sends them over the air. Other devices on the network receive these signals with their own wireless adapters, and the data is then converted back into a usable form. Those can operate over various ranges, depending on the technology used. For example, a local area network (LAN) that covers a small area, such as a home or small office, might use a wireless technology called `WiFi`, which has a range of a few hundred feet. On the other hand, a wireless wide area network ( `WWAN`) might use mobile telecommunication technology such as cellular data ( `3G`, `4G LTE`, `5G`), which can cover a much larger area, such as an entire city or region.

Therefore, to connect to a wireless network, a device must be within range of the network and configured with the correct network settings, such as the network name and password. Once connected, devices can communicate with each other and the Internet, allowing users to access online resources and exchange data.

Communication between devices occurs over RF in the `2.4 GHz` or `5 GHz` bands in a WiFi network. When a device, like a laptop, wants to send data over the network, it first communicates with the [Wireless Access Point](https://en.wikipedia.org/wiki/Wireless_access_point) ( `WAP`) to request permission to transmit. The WAP is a central device, like a router, that connects the wireless network to a wired network and controls access to the network. Once the WAP grants permission, the transmitting device sends the data as RF signals, which are received by the wireless adapters of other devices on the network. The data is then converted back into a usable form and passed on to the appropriate application or system.

The strength of the RF signal and the distance it can travel are influenced by factors such as the transmitter's power, the presence of obstacles, and the density of RF noise in the environment. So, to ensure reliable communication, WiFi networks use techniques such as spread spectrum transmission and error correction to overcome these challenges.

* * *

## WiFi Connection

The device must also be configured with the correct network settings, such as the network name / [Service Set Identifier](https://www.geeksforgeeks.org/service-set-identifier-ssid-in-computer-network/) ( `SSID`) and `password`. So, to connect to the router, the laptop uses a wireless networking protocol called [IEEE 802.11](https://en.wikipedia.org/wiki/IEEE_802.11). This protocol defines the technical details of how wireless devices communicate with each other and with WAPs. When a device wants to join a WiFi network, it sends a request to the WAP to initiate the connection process. This request is known as a `connection request frame` or `association request` and is sent using the `IEEE 802.11` wireless networking protocol. The connection request frame contains various fields of information, including the following but not limited to:

|  |  |
| --- | --- |
| `MAC address` | A unique identifier for the device's wireless adapter. |
| `SSID` | The network name, also known as the `Service Set Identifier` of the WiFi network. |
| `Supported data rates` | A list of the data rates the device can communicate. |
| `Supported channels` | A list of the `channels` (frequencies) on which the device can communicate. |
| `Supported security protocols` | A list of the security protocols that the device is capable of using, such as `WPA2`/ `WPA3`. |

The device then uses this information to configure its wireless adapter and connect to the WAP. Once the connection is established, the device can communicate with the WAP and other network devices. It can also access the Internet and other online resources through the WAP, which acts as a gateway to the wired network. However, the `SSID` can be hidden by disabling broadcasting. That means that devices that search for that specific WAP will not be able to identify its `SSID`. Nevertheless, the `SSID` can still be found in the authentication packet.

In addition to the `IEEE 802.11` protocol, other networking protocols and technologies may also be used, like TCP/IP, DHCP, and WPA2, in a WiFi network to perform tasks such as assigning IP addresses to devices, routing traffic between devices, and providing security.

#### WEP Challenge-Response Handshake

The challenge-response handshake is a process to establish a secure connection between a WAP and a client device in a wireless network that uses the WEP security protocol. This involves exchanging packets between the WAP and the client device to authenticate the device and establish a secure connection.

| **Step** | **Who** | **Description** |
| --- | --- | --- |
| 1 | `Client` | Sends an association request packet to the WAP, requesting access. |
| 2 | `WAP` | Responds with an association response packet to the client, which includes a challenge string. |
| 3 | `Client` | Calculates a response to the challenge string and a shared secret key and sends it back to the WAP. |
| 4 | `WAP` | Calculates the expected response to the challenge with the same shared secret key and sends an authentication response packet to the client. |

Nevertheless, some packets can get lost, so the so-called `CRC` checksum has been integrated. [Cyclic Redundancy Check](https://en.wikipedia.org/wiki/Cyclic_redundancy_check) ( `CRC`) is an error-detection mechanism used in the WEP protocol to protect against data corruption in wireless communications. A CRC value is calculated for each packet transmitted over the wireless network based on the packet's data. It is used to verify the integrity of the data. When the destination device receives the packet, the CRC value is recalculated and compared to the original value. If the values match, the data has been transmitted successfully without any errors. However, if the values do not match, the data has been corrupted and needs to be retransmitted.

The design of the `CRC` mechanism has a flaw that allows us to decrypt a single packet `without` knowing the `encryption key`. This is because the `CRC` value is calculated using the `plaintext` data in the packet rather than the encrypted data. In WEP, the CRC value is included in the packet header along with the encrypted data. When the destination device receives the packet, the `CRC` value is recalculated and compared to the original one to ensure that the data has been transmitted successfully without any errors. However, we can use the `CRC` to determine the plaintext data in the packet, even if the data is encrypted.

* * *

## Security Features

WiFi networks have several security features to protect against unauthorized access and ensure the privacy and integrity of data transmitted over the network. Some of the leading security features include but are not limited to:

- Encryption
- Access Control
- Firewall

#### Encryption

We can use various encryption algorithms to protect the confidentiality of data transmitted over wireless networks. The most common encryption algorithms in WiFi networks are [Wired Equivalent Privacy](https://en.wikipedia.org/wiki/Wired_Equivalent_Privacy) ( `WEP`), [WiFi Protected Access 2](https://en.wikipedia.org/wiki/Wi-Fi_Protected_Access#WPA2) ( `WPA2`), and [WiFi Protected Access 3](https://en.wikipedia.org/wiki/Wi-Fi_Protected_Access#WPA3) ( `WPA3`).

#### Access Control

WiFi networks are configured by default to allow authorized devices to join the network using specific authentication methods. However, these methods can be changed by requiring a password or a unique identifier (such as a MAC address) to identify authorized devices.

#### Firewall

A firewall is a security system that controls incoming and outgoing network traffic based on predetermined security rules. For example, WiFi routers often have built-in firewalls that can block incoming traffic from the Internet and protect against various types of cyber threats.

* * *

## Encryption Protocols

[Wired Equivalent Privacy](https://en.wikipedia.org/wiki/Wired_Equivalent_Privacy) ( `WEP`) and [WiFi Protected Access](https://en.wikipedia.org/wiki/Wi-Fi_Protected_Access) ( `WPA`) are encryption protocols that secure data transmitted over a WiFi network. WPA can use different encryption algorithms, including [Advanced Encryption Standard](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard) ( `AES`).

#### WEP

`WEP` uses a `40-bit` or `104-bit` key to encrypt data, while `WPA using AES` uses a `128-bit` key. Longer keys provide more robust encryption and are more resistant to attacks. However, it is vulnerable to various attacks that can allow an attacker to decrypt data transmitted over the network. In addition, WEP is not compatible with newer devices and operating systems and is generally no longer considered secure. Finally, `WEP` uses the `RC4 cipher` encryption algorithm, which makes it vulnerable to attacks.

However, WEP uses a `shared key` for authentication, which means the same key is used for encryption and authentication. There are two versions of the WEP protocol:

- `WEP-40`/ `WEP-64`
- `WEP-104`

`WEP-40`, also known as `WEP-64`, uses a `40-bit` (secret) key, while `WEP-104` uses a `104-bit` key. The key is divided into an [Initialization Vector](https://en.wikipedia.org/wiki/Initialization_vector) ( `IV`) and a `secret key`.

The `IV` is a small value included in the packet header along with the encrypted data and is used to create the key for both `WEP-40` and `WEP-104` and is included to ensure that each key is unique. The secret key is a series of random bits used to encrypt the data. However, the `WEP-104` has a `80-bits` long `secret key`. Let us look at the following table to see the differences clearly:

| **Protocol** | **IV** | **Secret Key** |
| --- | --- | --- |
| `WEP-40`/ `WEP-64` | 24-bit | 40-bit |
| `WEP-104` | 24-bit | 80-bit |

However, since the IV in WEP is relatively small, we can brute force it, try every possible combination of characters for it, and determine the correct value. Afterward, we can use it to decrypt the data in the packet. This allows us to access the data transmitted over the wireless network and potentially compromise the network's security.

#### WPA

`WPA` provides the highest level of security and is not susceptible to the same types of attacks as WEP. In addition, WPA uses more secure authentication methods, such as a [Pre-Shared Key](https://en.wikipedia.org/wiki/Pre-shared_key) ( `PSK`) or an 802.1X authentication server, which provide stronger protection against unauthorized access. Although older devices may not support WPA is compatible with most devices and operating systems. All wireless networks, especially in critical infrastructure like offices, should generally implement at least `WPA2` or even `WPA3` encryption.

* * *

## Authentication Protocols

[Lightweight Extensible Authentication Protocol](https://en.wikipedia.org/wiki/Lightweight_Extensible_Authentication_Protocol) ( `LEAP`) and [Protected Extensible Authentication Protocol](https://en.wikipedia.org/wiki/Protected_Extensible_Authentication_Protocol) ( `PEAP`) are authentication protocols used to secure wireless networks to provide a secure method for authenticating devices on a wireless network and are often used in conjunction with WEP or WPA to provide an additional layer of security.

LEAP and PEAP are both based on the [Extensible Authentication Protocol](https://en.wikipedia.org/wiki/Extensible_Authentication_Protocol) ( `EAP`), a framework for authentication used in various networking contexts. However, one key difference between `LEAP` and `PEAP` is how they secure the authentication process.

- `LEAP` uses a `shared key` for authentication, which means that the `same key` is used for `encryption and authentication`.

This can make it relatively easy for us to gain access to the network if the key is compromised.

However, `PEAP` uses a more secure authentication method called tunneled [Transport Layer Security](https://en.wikipedia.org/wiki/Transport_Layer_Security) ( `TLS`). This method establishes a secure connection between the device and the WAP using a `digital certificate`, and an encrypted tunnel protects the authentication process. This provides more robust protection against unauthorized access and is more resistant to attacks.

* * *

## TACACS+

In a wireless network, when a wireless access point (WAP) sends an authentication request to a [Terminal Access Controller Access-Control System Plus](https://www.ciscopress.com/articles/article.asp?p=422947&seqNum=4) ( `TACACS+`) server, it is likely that the `entire request packet` will be encrypted to protect the confidentiality and integrity of the request.

`TACACS+` is a protocol used to authenticate and authorize users accessing network devices, such as routers and switches. When a WAP sends an authentication request to a `TACACS+` server, the request typically includes the user's credentials and other information about the session.

Encrypting the authentication request helps to ensure that this sensitive information is not visible to unauthorized parties who may be able to intercept the request. At the same time, it is being transmitted over the network. It also helps prevent tampering with the request or replacing it with a malicious request of their own.

Several encryption methods may be used to encrypt the authentication request, such as `SSL`/ `TLS` or `IPSec`. The specific encryption method used may depend on the configuration of the `TACACS+` server and the capabilities of the WAP.

* * *

## Disassociation Attack

A [Disassociation Attack](https://www.makeuseof.com/what-are-disassociation-attacks/) is a type of `all` wireless network attack that aims to disrupt the communication between a WAP and its clients by sending disassociation frames to one or more clients.

The WAP uses disassociation frames to disconnect a client from the network. When a WAP sends a disassociation frame to a client, the client will disconnect from the network and have to reconnect to continue using the network.

We can launch the attack from `within` or `outside` the network depending on our location and network security measures. The purpose of this attack is to disrupt the communication between the WAP and its clients, causing the clients to disconnect and possibly causing inconvenience or disruption to the users. We can also use it as a precursor to other attacks, such as a MITM attack, by forcing the clients to reconnect to the network and potentially exposing them to further attacks.

* * *

## Wireless Hardening

There are many different ways to protect wireless networks. However, some examples should be considered to increase wireless networks' security dramatically. These are the following, but not limited to:

- Disabling broadcasting
- WiFi Protected Access
- MAC filtering
- Deploying EAP-TLS

#### Disabling Broadcasting

Disabling the broadcasting of the SSID is a security measure that can help harden a WAP by making it more difficult to discover and connect to the network. When the SSID is broadcasted, it is included in beacon frames regularly transmitted by the WAP to advertise the availability of the network. By disabling the broadcasting of the SSID, the WAP will not transmit beacon frames, and the network will not be visible to devices that are not already connected to the network.

#### WPA

Again, WPA provides strong encryption and authentication for wireless communications, helping protect against unauthorized network access and sensitive data interception. WPA includes two main versions:

1. WPA-Personal
2. WPA-Enterprise

WPA-Personal, designed for home and small business networks, and WPA-Enterprise, designed for larger organizations and uses a centralized authentication server (e.g., RADIUS or TACACS+) to verify the identity of clients.

#### MAC Filtering

MAC filtering is a security measure that allows a WAP to accept or reject connections from specific devices based on their MAC addresses. By configuring the WAP to accept connections only from devices with approved MAC addresses, it is possible to prevent unauthorized devices from connecting to the network.

#### Deploying EAP-TLS

EAP-TLS is a security protocol used to authenticate and encrypt wireless communications. It uses digital certificates and PKI to verify the identity of clients and establish secure connections. Deploying EAP-TLS can help to harden a WAP by providing strong authentication and encryption for wireless communications, which can protect against unauthorized access to the network and the interception of sensitive data.


# Virtual Private Networks

* * *

A `Virtual Private Network` ( `VPN`) is a technology that allows a secure and encrypted connection between a private network and a remote device. This allows the remote machine to access the private network directly, providing secure and confidential access to the network's resources and services. For example, an administrator from another location has to manage the internal servers so that the employees can continue to use the internal services. Many companies limit servers' access, so clients can only reach those servers from the local network. This is where VPN comes into play, where the administrator connects to the VPN server via the internet, authenticates himself, and thus creates an encrypted tunnel so that others cannot read the data transfer. In addition, the administrator's computer is also assigned a local (internal) IP address through which he can access and manage the internal servers. Administrators commonly use VPNs to provide secure and cost-effective remote access to a company's network. VPN typically uses the ports `TCP/1723` for [Point-to-Point Tunneling Protocol](https://www.lifewire.com/pptp-point-to-point-tunneling-protocol-818182) `PPTP` VPN connections and `UDP/500` for [IKEv1](https://www.cisco.com/c/en/us/support/docs/security-vpn/ipsec-negotiation-ike-protocols/217432-understand-ipsec-ikev1-protocol.html) and [IKEv2](https://nordvpn.com/blog/ikev2ipsec/) VPN connections.

This allows employees to access the network and its resources, such as email and file servers, from remote locations, such as their homes or while traveling. There are several reasons why administrators use VPNs. VPNs encrypt the connection between the remote device and the private network, making it much more difficult for attackers to intercept and steal sensitive information. With this, the entire communication is more secure.

Another reason is that VPNs allow employees to access the private network and its resources remotely from anywhere, as long as they have an internet connection. This is particularly useful for employees who need to work remotely, such as those traveling or working from home. Additionally, VPNs can be more cost-effective than other remote access solutions, such as leased lines or dedicated connections, because they use the public internet to connect remote users to the private network.

Moreover, we can use VPNs to connect multiple remote locations, such as branch offices, into a single private network, making it easier to manage and access network resources. However, several components and requirements are necessary for a VPN to work:

| **Requirement** | **Description** |
| --- | --- |
| `VPN Client` | This is installed on the remote device and is used to establish and maintain a VPN connection with the VPN server. For example, this could be an OpenVPN client. |
| `VPN Server` | This is a computer or network device responsible for accepting VPN connections from VPN clients and routing traffic between the VPN clients and the private network. |
| `Encryption` | VPN connections are encrypted using a variety of encryption algorithms and protocols, such as AES and IPsec, to secure the connection and protect the transmitted data. |
| `Authentication` | The VPN server and client must authenticate each other using a shared secret, certificate, or another authentication method to establish a secure connection. |

The VPN client and server use these ports to establish and maintain the VPN connection. At the TCP/IP layer, a VPN connection typically uses the [Encapsulating Security Payload](https://www.ibm.com/docs/en/i/7.4?topic=protocols-encapsulating-security-payload) ( `ESP`) protocol to encrypt and authenticate the VPN traffic. This allows the VPN client and server to exchange data over the public internet securely.

* * *

## IPsec

[Internet Protocol Security](https://www.cloudflare.com/learning/network-layer/what-is-ipsec/) ( `IPsec`) is a network security protocol that provides encryption and authentication for internet communications. It is a powerful and widely-used security protocol that provides encryption and authentication for internet communications and works by encrypting the data payload of each IP packet and adding an `authentication header` ( `AH`), which is used to verify the integrity and authenticity of the packet. IPsec uses a combination of two protocols to provide encryption and authentication:

1. [Authentication Header](https://www.ibm.com/docs/en/i/7.1?topic=protocols-authentication-header) ( `AH`): This protocol provides integrity and authenticity for IP packets but does not provide encryption. It adds an authentication header to each IP packet, which contains a cryptographic checksum that can be used to verify that the packet has not been tampered with.

2. [Encapsulating Security Payload](https://www.ibm.com/docs/en/i/7.4?topic=protocols-encapsulating-security-payload) ( `ESP`): This protocol provides encryption and optional authentication for IP packets. It encrypts the data payload of each IP packet and optionally adds an authentication header, similar to AH.


IPsec can be used in two modes.

| **Mode** | **Description** |
| --- | --- |
| `Transport Mode` | In this mode, IPsec encrypts and authenticates the data payload of each IP packet but does not encrypt the IP header. This is typically used to secure end-to-end communication between two hosts. |
| `Tunnel Mode` | With this mode, IPsec encrypts and authenticates the entire IP packet, including the IP header. This is typically used to create a VPN tunnel between two networks. |

For example, an administrator could place a firewall in between. In order to facilitate IPsec VPN traffic from a VPN client outside a firewall to a VPN server inside, the firewall would need to allow the following protocols:

| **Protocol** | **Port** | **Description** |
| --- | --- | --- |
| `Internet Protocol` ( `IP`) | `UDP/50-51` | This is the primary protocol that provides the foundation for all internet communication. It is used to route packets of data between the VPN client and the VPN server. |
| `Internet Key Exchange` ( `IKE`) | `UDP/500` | IKE is a protocol that is used to establish and maintain secure communication between the VPN client and the VPN server. It is based on the Diffie-Hellman key exchange algorithm, and it is used to negotiate and establish shared secret keys that can be used to encrypt and decrypt the VPN traffic. |
| `Encapsulating Security Payload` ( `ESP`) | `UDP/4500` | ESP is also a protocol that provides encryption and authentication for IP datagrams. It is used to encrypt the VPN traffic between the VPN client and the VPN server, using the keys that were negotiated with IKE. |

These protocols are necessary for facilitating IPsec VPN traffic because they provide the security and encryption that are required for secure communication over the public internet. Without these protocols, the VPN traffic would be vulnerable to interception and tampering.

* * *

## PPTP

[Point-to-Point Tunneling Protocol](https://www.vpnranks.com/blog/pptp-vs-l2tp/) ( `PPTP`) is a network protocol that enables the creation of VPNs by establishing a secure tunnel between the VPN client and server, encapsulating the data transmitted within this tunnel. Originally an extension of the Point-to-Point Protocol (PPP), PPTP is supported by many operating systems.

However, due to its known vulnerabilities, PPTP is no longer considered secure. It can tunnel protocols such as IP, IPX, or NetBEUI via IP, but has been largely replaced by more secure VPN protocols like L2TP/IPsec, IPsec/IKEv2, and OpenVPN. Since 2012, the use of PPTP has declined because its authentication method, MSCHAPv2, employs the outdated DES encryption, which can be easily cracked with specialized hardware.


# Vendor Specific Information

* * *

[Cisco IOS](https://www.cisco.com/c/en/us/products/ios-nx-os-software/ios-technologies/index.html) is the operating system of Cisco network devices such as routers and switches. It provides features and services required to manage and operate network devices. This operating system comes in different versions and releases that vary in features, support, and performance. It offers several features required for the operation of modern networks, such as, but not limited to:

- Support for IPv6
- Quality of Service (QoS)
- Security features such as encryption and authentication
- Virtualization features such as Virtual Private LAN Service (VPLS)
- Virtual Routing and Forwarding (VRF)

Cisco IOS can be managed in several ways, depending on the network device and hardware used. The most commonly used method is the command line interface ( `CLI`), which can also be managed in the graphical user interface ( `GUI`). In addition, it supports various network protocols and services required for network operations. These include:

| **Protocol Type** | **Description** |
| --- | --- |
| `Routing protocols` | Such as [OSPF](https://en.wikipedia.org/wiki/Open_Shortest_Path_First) and [BGP](https://en.wikipedia.org/wiki/Border_Gateway_Protocol) are used to route data packets on a network. |
| `Switching protocols` | Such as [VLAN Trunking Protocol](https://en.wikipedia.org/wiki/VLAN_Trunking_Protocol) ( `VTP`) and [Spanning Tree Protocol](https://en.wikipedia.org/wiki/Spanning_Tree_Protocol) ( `STP`) is used to configure and manage switches on a network. |
| `Network services` | Such as [Dynamic Host Configuration Protocol](https://en.wikipedia.org/wiki/Dynamic_Host_Configuration_Protocol) ( `DHCP`) are used to automatically provide clients on the network with IP addresses and other network configurations. |
| `Security features` | Such as [Access Control Lists](https://en.wikipedia.org/wiki/Access-control_list) ( `ACLs`), which are used to control access to network resources and prevent security threats. |

* * *

In Cisco IOS, different types of passwords are used for various purposes, for example:

| **Password Type** | **Description** |
| --- | --- |
| `User` | The [user](https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/security/s1/sec-s1-cr-book/sec-cr-t2.html#wp2992613898) password is used for logging in to Cisco IOS. It is used to restrict access to the network device and its features. |
| `Enable Password` | The [enable password](https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/security/d1/sec-d1-cr-book/sec-cr-e1.html#wp3884449514) is used to enter "enable" mode. The "enable" mode is the mode where you have access to advanced functions and settings. |
| `Secret` | The [secret](https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/security/s1/sec-s1-cr-book/sec-cr-s1.html#wp2622423174) is a password to secure access to certain functions and services. It is often used to restrict access to remote management tools and services. |
| `Enable Secret` | The [enable secret](https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/security/d1/sec-d1-cr-book/sec-cr-e1.html#wp3438133060) is an extra-secure password used to secure access to "enable" mode, and they are stored encrypted to provide additional protection. |

We highly recommend going through the provided external resources to understand the encryption mechanics of Cisco IOS and how those are used.

The Cisco IOS devices can be configured for SSH or Telnet. So it can be accessed remotely. We can determine from the response we receive that it is indeed a Cisco IOS, as it responds with the `User Access Verification` message.

#### Cisco IOS

```shell
telnet 10.129.10.2

Trying 10.129.10.2...
Connected to 10.129.10.2.
Escape character is '^]'.

User Access Verification

Password:

```

* * *

# VLANs

Imagine this scenario: A startup called XQ hired a network administrator to create a network for their single-office company, and due to budget limitations, they can only afford one switch and router. The sysadmin of XQ stated that in addition to hosting the web and database servers in the network, staff from different departments will be using it. As a seasoned network security specialist, the network administrator immediately thought about the security attacks that an insider can perform, especially ones abusing broadcast traffic, such as `broadcast storms`. Therefore, to tackle this problem, the network administrator decided to logically segment the network with `Virtual Local Area Networks` ( `VLANS`), conceptually breaking down one switch into smaller mini-switches.

A `VLAN` is a logical grouping of network endpoints connected to defined ports on a switch, allowing the segmentation of networks by creating logical broadcast domains that can span multiple physical LAN segments. With `VLANs`, network administrators can segment networks based on factors such as team, function, department, or application, without worrying about the physical location of endpoints and users. A broadcast packet sent over one `VLAN` does not reach any other endpoint that is a member of another `VLAN`. Because each `VLAN` is regarded as a broadcast domain, it needs to have its own `subnet`; for example, the network administrator contracted by XQ can segment the network by departments:

| **Department** | **VLAN ID** | **Subnet** |
| :-: | :-: | :-: |
| `Servers` | `VLAN 10` | `192.168.1.0/24` |
| `C-Level` | `VLAN 20` | `192.168.2.0/24` |
| `Finance` | `VLAN 30` | `192.168.3.0/24` |
| `HR` | `VLAN 40` | `192.168.4.0/24` |
| `Marketing` | `VLAN 50` | `192.168.5.0/24` |
| `Support` | `VLAN 60` | `192.168.6.0/24` |

A myriad of benefits is attained when using `VLANs`, including:

- `Better Organization`: Network administrators can group endpoints based on any common attribute they share.
- `Increased Security`: Network segmentation disallows unauthorized members from sniffing network packets in other `VLANs`.
- `Simplified Administration`: Network administrators do not have to worry about the physical locations of an endpoint.
- `Increased Performance`: With reduced broadcast traffic for all endpoints, more bandwidth is made available for use by the network.

Cisco switches provide the `VLAN` IDs/numbers 1-4094 ( `0` and `4095` are reserved IDs and cannot be used); IDs 1-1005 ( `VLAN 1` is known as the `default VLAN` and cannot/should not be altered nor deleted) are known as `normal-range` `VLANs`, with IDs 1002-1005 being reserved for `Token Ring` and `Fiber Distributed Data Interface` ( `FDDI`) `VLANs`, while IDs 1006-4094 are known as `extended-range` `VLANs`. By default, any customization applied for `normal-range` `VLANs` is saved in the `VLAN` database (the `vlan.dat` file), in contrast to `extended-range` `VLANs`, which do not have their customizations saved. `VLANs` 2-1001 stored in `vlan.dat` can have parameters including name, type, state, and maximum transmission unit ( `MTU`).

## VLAN Memberships

Network administrators can assign the ports of a switch to `VLANs` either statically or dynamically. Static `VLAN` assignment, which is the simplest and most common method, involves assigning each port to a `VLAN` manually using the switch's `network operating system`; this must be done for all switches separately (it is essential to keep in mind that endpoints connecting to these ports are unaware of the existence of `VLANs`). In contrast, dynamic `VLAN` assignment automatically determines an endpoint's `VLAN` membership based on `MAC` addresses or protocols. The system administrator can register the `MAC` addresses in a centralized `VLAN` management service/database, such as the `VLAN Membership Policy Server` ( `VMPS`) service, and then the switch queries the database of `VMPS` to determine the `VLAN` of the endpoint with that specific `MAC` address. Regardless of their flexibility and mobility, dynamic `VLANs` increase administrative overhead.

Security-wise, static `VLANs` are the more secure option because a port will forever be tied to a specific `VLAN` ID, unless changed manually afterward. For dynamic `VLANs`, an attacker could potentially utilize tools such as [macchanger](https://github.com/alobbs/macchanger) to spoof the MAC address of legitimate endpoints and attain membership of their `VLANs`, therefore sniffing all network traffic sent through them.

## Access and Trunk Ports

Any port on a `VLAN`-enabled switch must be either an `access port` or a `trunk port`. `Access ports` belong to and can carry the traffic of only one `VLAN` (or in some cases two, with the second being for `voice traffic`); any traffic arriving on an `access port` is assumed to belong to the `VLAN` the port was assigned. On the other hand, `trunk ports` can carry multiple `VLANs` at the same time; `trunk links` connect two `trunk ports` on two switches (or a switch and router) to allow information from multiple `VLANs` to be carried out across switches.

## VLAN Identification

Standard `802.3` `Ethernet` frames do not contain `VLAN` information; therefore, switches and other `VLAN`-enabled devices need a mechanism to keep track of all the `VLAN` information associated with a packet while traversing `VLAN`-enabled devices. Two main `trunking methods` are utilized to achieve this, `ISL` and `IEEE 802.1Q`.

#### Inter-Switch Link (ISL)

`Inter-Switch Link` ( `ISL`) is a Cisco-proprietary protocol used for trunking between `VLAN`-enabled devices. Although `ISL` is one of the first `trunking methods` (predating `802.1Q`), it is deprecated and not as widely used in modern Cisco switches (and routers). Instead, most only support the widely adopted `802.1Q`. `ISL` encapsulated the entire `Ethernet` frame, including the original `Ethernet` header and the `VLAN` tag, adding its 26-byte header and 4-byte trailer.

#### IEEE 802.1Q

To ensure interoperability of `VLAN` technologies from the various network-equipments vendors, the `Institute of Electrical and Electronics Engineers` ( `IEEE`) developed the [802.1Q](https://ieeexplore.ieee.org/document/10004498) specification in 1998. The `IEEE 802` committee had to change the `802.3` `Ethernet` frame format by adding a pair of 2-byte fields, `TPID` and `TCI` (which consists of three subfields, `PCP`, `DEI`, and `VID`), resulting in a `VLAN`-compliant `802.1Q` `Ethernet` frame.

![Diagram showing conversion of a 802.3 Ethernet frame to a 802.1Q Ethernet frame by inserting a 802.1Q header between the source address and length fields. The 802.1Q header includes TPID, PCP, DEI, and VID.](https://academy.hackthebox.com/storage/modules/34/8023_Legacy_8021Q_Ethernet_Frames.png)

`Tag protocol identifier` ( `TPID`) is a 16-bit field always set to `0x8100` to identify the `Ethernet` frame as an `802.1Q`-tagged frame. `Tag Control Information` ( `TCI`) is a 16-bit field containing `Priority code point` ( `PCP`), `Drop eligible indicator` ( `DEI`) (previously known as `Canonical format indicator` ( `CFI`)), and `VLAN identifier` ( `VID`). The main field concerning `VLANs` is `VID`, occupying the low-order 12-bits of `TCI`. Since it is 12 bits, it allows 2^12 - 2 = 4096 (remember, `0` and `4095` are reserved) `VLAN` IDs. Therefore, an `802.1Q`-tagged frame can contain information for 4094 `VLANs`; the practice of inserting multiple `802.1Q` tags within a single packet is known as `Double Tagging`, introduced by [802.1ad](https://standards.ieee.org/ieee/802.1Q/10323/). `VLAN tagging` is the process of inserting `VLAN` information into an `802.1Q` `Ethernet header`, while `VLAN untagging` is the process of removing the `VLAN` information from an `802.1Q`-tagged `Ethernet` frame and forwarding the packet to the destined ports.

## VLAN-Capable NICs

Some `network interface cards` ( `NICs`) attached to computers/servers support `VLAN tagging`. Let us see how we can assign a `VLAN` ID to a `NIC` using Linux and Windows.

#### Assigning NICs a VLAN in Linux

In Linux, creating a `VLAN` is done by creating an interface on top of another, called a `parent` interface. This `VLAN` interface will tag packets with the assigned `VLAN` ID while returning packets will be untagged.

To assign a network adapter a `VLAN` in Linux, many tools can be used, such as [ip](https://man7.org/linux/man-pages/man8/ip.8.html), [nmcli](https://linux.die.net/man/1/nmcli), and [vconfig](https://linux.die.net/man/8/vconfig) (deprecated). However, first, we need to ensure that the Kernel has the [802.1Q](https://elixir.bootlin.com/linux/v6.4.7/source/net/8021q/vlan.c) module loaded:

```shell
sudo modprobe 8021q

```

Subsequently, we can use `lsmod` to make sure `8021q` was loaded successfully:

```shell
lsmod | grep 8021

8021q                  40960  0
garp                   16384  1 8021q
mrp                    20480  1 8021q

```

Now, we need to find the name of the physical `Ethernet` interface that we will create the `VLAN` interface on top of, which is `eth0`:

```shell
ip a

<SNIP>
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether a6:ba:3b:08:3a:36 brd ff:ff:ff:ff:ff:ff
    altname enp0s3
    altname ens3
    inet 94.2X.5X.72/22 brd 94.237.51.255 scope global dynamic eth0
       valid_lft 83489sec preferred_lft 83489sec
    inet6 fe80::a4ba:3bff:fe08:3a36/64 scope link
       valid_lft forever preferred_lft forever

```

Then, we will use `vconfig` to create a new interface that is a member of the desired `VLAN`, `20`, for example, on top of `eth0`:

```shell
sudo vconfig add eth0 20

Warning: vconfig is deprecated and might be removed in the future, please migrate to ip(route2) as soon as possible!

```

To use `ip` instead:

```shell
sudo ip link add link eth0 name eth0.20 type vlan id 20

```

Either of these commands will make a new interface called `eth0.20@eth0`:

```shell
ip a

<SNIP>
4: eth0.20@eth0: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN group default qlen 1000
    link/ether a6:ba:3b:08:3a:36 brd ff:ff:ff:ff:ff:ff

```

Then, based on the `subnet` assigned to the addresses with `VLAN 20` within the local network, we need to assign the interface an IP address and then start it:

```shell
sudo ip addr add 192.168.1.1/24 dev eth0.20
sudo ip link set up eth0.20

```

At last, we can check whether the interface has changed states to up:

```shell
ip a | grep eth0.20

4: eth0.20@eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default qlen 1000
    inet 192.168.1.1/24 scope global eth0.20

```

#### Assigning NICs a VLAN in Windows

On Windows, to assign a `VLAN` for a physical network adapter that supports `VLAN tagging`, first we need to open `Device Manager`:

![Windows search interface showing 'Device Manager' as the best match under Control Panel.](https://academy.hackthebox.com/storage/modules/34/Windows_Device_Manager.png)

Then we need to click on `Properties` for the `Ethernet interface` we want to assign to a `VLAN`:

![Device Manager window showing a context menu for ASIX AX88772B USB2.0 to Fast Ethernet Adapter with 'Properties' highlighted.](https://academy.hackthebox.com/storage/modules/34/Windows_Device_Manager_Adapter_Properties.png)

Within `Advanced`, there will be a `VLAN ID` property to which we can assign a value. After clicking `OK`, if the adapter supports assigning a `VLAN`, it will be set; otherwise, the window will close, and no `VLAN` tag will be added to any packets originating from this host:

![Device Manager window showing properties for ASIX AX88772B USB2.0 to Fast Ethernet Adapter. VLAN ID is selected with a value of 10.](https://academy.hackthebox.com/storage/modules/34/Windows_Device_Manager_Adapter_Properties_VLAN_ID.png)

Instead of relying on the GUI, we can use `PowerShell`. First, let us get the names of all the available physical network adapters using the [Get-NetAdapter](https://learn.microsoft.com/en-us/powershell/module/netadapter/get-netadapter?view=windowsserver2022-ps) Cmdlet:

```powershell
PS C:\> Get-NetAdapter | Format-Table -AutoSize

Name                                           InterfaceDescription                                                          ifIndex Status             MacAddress              LinkSpeed
----                                           --------------------                                                          ------- ------             ----------              ---------
VirtualBox Host-Only Network  VirtualBox Host-Only Ethernet Adapter                                        20 Up                    0A-00-27-10-42-15       1 Gbps
Ethernet 2                                 ASIX AX88772B USB2.0 to Fast Ethernet Adapter                            55 Up                    90-EB-78-14-21-7F    100 Mbps
Bluetooth Network Connection  Bluetooth Device (Personal Area Network)                                   18 Disconnected   38-41-25-E8-DE-2D        3 Mbps
Wi-Fi                                         Intel(R) Wireless-AC 9560 160MHz                                                12 Disconnected   8E-36-6A-7A-BA-6A 866.7 Mbps

```

Previously, we used `Device Manager` to assign `Ethernet 2` to `VLAN 10`; to retrieve the `VLAN` ID of the interface, we can use the [Get-NetAdapaterAdvancedProperty](https://learn.microsoft.com/en-us/powershell/module/netadapter/get-netadapteradvancedproperty?view=windowsserver2022-ps) Cmdlet with the `-DisplayName` flag along with `vlan id`:

```powershell
PS C:\> Get-NetAdapterAdvancedProperty -DisplayName "vlan id"

Name                      DisplayName                    DisplayValue                   RegistryKeyword RegistryValue
----                      -----------                    ------------                   --------------- -------------
Ethernet 2                VLAN ID                        10                                     VLAN_ID               {10}

```

We can also set the `VLAN` ID of a physical network address using the [Set-NetAdapter](https://learn.microsoft.com/en-us/powershell/module/netadapter/set-netadapter?view=windowsserver2022-ps) Cmdlet along with the [VlanID](https://learn.microsoft.com/en-us/powershell/module/netadapter/set-netadapter?view=windowsserver2022-ps#-vlanid) flag; this powerful Cmdlet can also be used to customize other properties of interfaces such as [MAC addresses](https://learn.microsoft.com/en-us/powershell/module/netadapter/set-netadapter?view=windowsserver2022-ps#-macaddress):

```powershell
PS C:\> Set-NetAdapter -Name "Ethernet 2" -VlanID 10

```

However, remember that this operation only succeeds if the network interface supports this functionality; otherwise, `PowerShell` will throw an error indicating that the interface does not support it.

## Analyzing VLAN Tagged Traffic

We can identify and analyze `VLAN` tagged traffic on a network with `Wireshark` using the [vlan](https://www.wireshark.org/docs/dfref/v/vlan.html) filter. For example, when analyzing a network packet dump, we can inspect packets with `802.1Q` tagging using the filter `vlan`:

![Wireshark interface showing a packet capture with highlighted RIP v2 response packet, Ethernet II, 802.1Q VLAN, and Internet Protocol details.](https://academy.hackthebox.com/storage/modules/34/Wireshark_VLAN_Filter.png)

Moreover, we can search for packets with a specific `VLAN` ID; for example, to search for packets having `VLAN 10`, we can use the filter `vlan.id == 10`:

![Wireshark interface showing a packet capture with highlighted RIP v2 response packet, Ethernet II, 802.1Q VLAN, and Internet Protocol details.](https://academy.hackthebox.com/storage/modules/34/Wireshark_VLAN_ID_Filter.png)

Additionally, to enumerate the used `VLAN` IDs from a packet dump, we can utilize [tshark](https://www.wireshark.org/docs/man-pages/tshark.html):

```shell
tshark -r "The Ultimate PCAP v20221220.pcapng" -T fields -e vlan.id | sort -n -u

1
2
3
7
10
20
30
40
50
60
70
80
90
121
125
224

```

* * *

## Security Implications and VLAN Attacks

Regardless of improving a network's security posture, adversaries can still circumvent the defensive mechanisms put forth by `VLANs`. Although in modern switched networks, the utilization of `VLANs` brings numerous advantages (such as simplified network maintenance and improved performance), it also introduces potential security risks, leading to various `VLAN` attacks. It is essential to grasp the underlying methodologies of these attacks and implement practical mitigation approaches to safeguard networks.

#### VLAN Hopping

`VLAN hopping` attacks enable traffic from one `VLAN` to be seen by another `VLAN` without the aid of a router. It exploits Cisco's `Dynamic Trunking Protocol` ( `DTP`), a protocol used to automatically negotiate the formation of a `trunk link` between two Cisco devices. An adversary needs to configure a host to mimic/act like a switch to take advantage of the automatic trunking port feature enabled by default on most switch ports. To exploit `VLAN hopping`, an adversary must be able to physically connect with a switch port that has `DTP` enabled. The adversary can abuse this connection by configuring a host connected to the switch on that specific port to spoof `802.1Q` signaling and the `DTP` packets. If successful, the switch will eventually establish a `trunk link` with the adversary's host, exposing the network packets, not only for a specific `VLAN`.

We can use tools such as [Yersinia](https://linux.die.net/man/8/yersinia) to perform `VLAN hopping` attacks:

![Yersinia interface showing protocol attack options with 'enabling trunking' selected for Dynamic Trunking Protocol (DTP).](https://academy.hackthebox.com/storage/modules/34/Yersinia_DTP_Attack.png)

#### Double-tagging VLAN Hopping

The `double-tagging VLAN hopping attack` is an increasingly more sophisticated attack against `VLANs`. Although `VLAN double-tagging` is a legitimate practice that entities such as `Internet Service Providers` ( `ISPs`) utilize (they can use their `VLANs` internally while carrying traffic from clients that are already `VLAN tagged`), adversaries can also attempt to abuse it. In a `double-tagging VLAN hopping attack`, an adversary embeds a hidden `802.1Q` tag inside an `Ethernet` frame that already has an `802.1Q` tag, allowing the frame to go to a different `VLAN`, which the original `802.1Q` tag did not specify.

An adversary can carry out this attack following three steps. Bare in mind that this attack only works if the adversary is connected to a port residing in the same `VLAN` as the `native VLAN` of the trunk port:

1. The adversary sends a `double-tagged 802.1Q` `Ethernet` frame to the switch with the outer header having the `VLAN` ID of the adversary, which is the same as the native `VLAN` of the trunk port. Assume that the native `VLAN` is `VLAN 10` and that `VLAN 30` is the `VLAN` the adversary wants to reach, where the victim resides.
2. The outer 4-byte `802.1Q` tag arrives on the switch, and it is seen to be destined for `VLAN 10`, the native `VLAN`. After removing the `VLAN 10` tag, the frame is forwarded on all `VLAN 10` ports. On the trunk port, the `VLAN 10` tag is stripped (removed), and the packet is not re-tagged because it is part of the native `VLAN`. However, the `VLAN 30` tag is still intact (not stripped), and the first switch has not inspected it.
3. Subsequently, the switch will look only at the inner `802.1Q` tag that the adversary sent, and it decides that the frame must be forwarded for `VLAN 30`, which is the adversary's chosen `VLAN`. Now, the second switch will either send the frame to the victim port directly or flood it, depending on whether there is an existing MAC address table entry for the victim host.

[Scapy](https://scapy.readthedocs.io/en/latest/usage.html#vlan-hopping) allows carrying out the `double-tagging VLAN hopping attack`, in addition to `Yersinia`:

![Yersinia interface showing protocol attack options with 'sending 802.1Q double enc. packet' selected.](https://academy.hackthebox.com/storage/modules/34/Yersinia_Double_Tagging_VLAN_Hopping_Attack.png)

* * *

## VXLAN

We mentioned previously that the `VID` field within the '802.1Q' header inside an 'Ethernet' frame is only 12 bits, allowing for 4094 VLANs. While this number of VLANs might be sufficient for small networks, more is needed for data centers and cloud service providers, which require extensive segmentation. Additionally, current Layer 2 networks utilize the `IEEE 802.1D` `Spanning Tree Protocol` ( `STP`) to prevent network loops caused by redundant paths. However, some data center operators encounter limitations with `STP`, such as link blocking, which reduces available ports and prevents resiliency through multipathing. These challenges hinder network efficiency in virtualized environments that rely on Layer 2 physical infrastructure. A critical requirement in such environments is the seamless scalability of the Layer 2 network across the entire data center and even between data centers to allocate computing, networking, and storage resources efficiently. Nevertheless, traditional approaches like `STP`, while ensuring a loop-free topology, can deactivate many links, further exacerbating the problem.

[RFC7348](https://datatracker.ietf.org/doc/html/rfc7348) offers a solution to these problems and limitations in Layer 2 networks by introducing `Virtual eXtensible Local Area Network` ( `VXLAN`), which is essentially a 'Layer 2 overlay scheme on a Layer 3 network.' `VXLAN` is specifically designed to address the limitations of traditional Layer 2 networks and cater to the requirements of Layer 2 and Layer 3 data center network infrastructures in a multi-tenant environment with virtual machines (VMs). Operating over the existing networking infrastructure, `VXLAN` provides an innovative way to seamlessly extend a Layer 2 network. Its primary objective is to facilitate the scaling of Layer 2 networks across expansive data center landscapes, even spanning multiple physical data locations. Each `VXLAN` overlay is termed a `VXLAN segment`, ensuring that only VMs within the same VXLAN segment can communicate with each other, thus maintaining network isolation and security. A 24-bit segment ID, known as the `VXLAN Network Identifier` ( `VNI`), uniquely identifies each VXLAN segment. Adopting VXLAN allows for the coexistence of 16 million `VXLAN` segments within the same administrative domain, providing scalability and flexibility for modern data centers and virtualized environments.

* * *

## Cisco Discovery Protocol

Cisco Discovery Protocol (CDP) is a layer-2 network protocol from Cisco that is used by Cisco devices such as routers, switches, and bridges to gather information about other directly connected Cisco devices. This information can be used to discover and track the network's topology and help manage and troubleshoot the network. This protocol is usually enabled in Cisco devices, but it can be disabled if it is not needed or if it should be disabled for security reasons.

#### CDP Network Traffic

```shell
22:14:11.563654 CDPv2, ttl: 180s, checksum: 0xebc1 (incorrect -> 0x8b71), length: 180
        Device-ID (0x01), length: 14 bytes: 'router.inlanefreight.loc'
        Addresses (0x02), length: 8 bytes:
                IPv4 (0x01), length: 4: 10.129.100.1
        Port-ID (0x03), length: 9 bytes: 'Ethernet0/0'
        Capability (0x04), length: 4: (0x00000010): Router
        Version String (0x05), length: 27 bytes: 'Cisco IOS Software, C880 Software'
        Platform (0x06), length: 26 bytes: 'Cisco 881 (MPC8300) processor'

```

The shown message contains information about the device itself, such as the device name, IP address, port name, and functionality of the router, as well as information about the operating system and hardware platform of the device. Besides, we can see in the first line from the `CDPv2` that we are dealing with the `Cisco Discovery Protocol`.

For comparison, we can look at another protocol called Spanning Tree Protocol ( `STP`). The `STP` is a network protocol that ensures no loops in a network with multiple connections between switches. There are no loops, and it prevents data packets from circulating in a loop and congesting the network.

#### STP Network Traffic

```shell
22:14:11.563654 STP 802.1w, Rapid STP, Flags [Learn, Forward], bridge-id 8001.00:11:22:33:44:55.8000, length 43
        root-id 8001.AA:AA:AA:AA:AA:AA, cost 0, port-id 8001, message-age 0.00s, max-age 20.00s, hello-time 2.00s, forward-delay 15.00s

```

In this example, we see that an `STP` message was sent containing information about the root switch, the MAC address of the root switch, the ID of the port over which the message was sent, and other configuration parameters such as the maximum aging time, hello time, and forward delay.


# Key Exchange Mechanisms

* * *

Key exchange methods are used to exchange [cryptographic keys](https://www.cloudflare.com/learning/ssl/what-is-a-cryptographic-key/) between two parties securely. This is an essential part of many cryptographic protocols, as the security of the encryption used to protect communication relies on the secrecy of the keys. There are many key exchange methods, each with unique characteristics and strengths. Some key exchange methods are more secure than others, and the appropriate method depends on the situation's specific circumstances and requirements.

These methods typically work by allowing the two parties to agree on a `shared secret key` over an insecure communication channel that encrypts the communication between them. This is generally done using some form of mathematical operation, such as a computation based on the properties of a mathematical function or a series of simple manipulations of the key.

#### Diffie-Hellman

One common key exchange method is the [Diffie-Hellman key exchange](https://www.comparitech.com/blog/information-security/diffie-hellman-key-exchange/), which allows two parties to agree on a shared secret key without any prior communication or shared private information. It is based on the concept of two parties generating a shared secret key that can be used to encrypt and decrypt messages between them. It is often used as the basis for establishing secure communication channels, such as in the [Transport Layer Security](https://www.cloudflare.com/learning/ssl/transport-layer-security-tls/) ( `TLS`) protocol that is used to protect web traffic.

One of the main limitations of the `Diffie-Hellman` key exchange is that it is vulnerable to `MITM attacks`. In a MITM attack, we intercept the communication between the two parties and pretend to be one of the parties, generating a different secret key and tricking both parties into using it. This allows the attacker to read and modify the messages sent between the parties.

Another limitation is that it requires a relatively large amount of `CPU power` to generate the shared secret key. This can make it impractical for use in low-power devices or in situations where the key needs to be generated quickly.

#### RSA

Another key exchange method is the [Rivest–Shamir–Adleman](https://www.venafi.com/blog/how-diffie-hellman-key-exchange-different-rsa) ( `RSA`) algorithm, which uses the properties of large prime numbers to generate a shared secret key. This method relies on the fact that it is relatively easy to multiply large prime numbers together but challenging to factor the resulting number back into its prime factors. Besides these two, there are also a couple of others that we need to look at. It is also widely used in many other applications and protocols that require secure communication and data protection, including but not limited to:

- Encrypting and signing messages to provide confidentiality and authentication

- Protecting data in transit over networks, such as in the [Secure Socket Layer](https://www.cloudflare.com/learning/ssl/what-is-ssl/) ( `SSL`) and `TLS` protocols

- Generating and verifying digital signatures, which are used to provide authenticity and integrity for electronic documents and other digital data

- Authenticating users and devices, such as in the [Public Key Cryptography for Initial Authentication in Kerberos](https://www.ietf.org/rfc/rfc4556.txt) ( `PKINIT`) protocol used by the Kerberos network authentication system

- Protecting sensitive information, such as in the encryption of personal data and confidential documents


#### ECDH

[Elliptic curve Diffie-Hellman](https://medium.com/swlh/understanding-ec-diffie-hellman-9c07be338d4a) ( `ECDH`) is a variant of Diffie-Hellman key exchange that uses elliptic curve cryptography to generate the shared secret key. It has the advantage of being more efficient and secure than the original Diffie-Hellman algorithm, including but not limited to:

- Establishing secure communication channels, such as in the `TLS` protocol

- Providing forward secrecy, which ensures that past communications cannot be revealed even if the private keys are compromised

- Authenticating users and devices, such as in the [Internet Key Exchange](https://docs.oracle.com/cd/E19683-01/816-7264/6md9iem1g/index.html) ( `IKE`) protocol used in VPNs


#### ECDSA

The [Elliptic Curve Digital Signature Algorithm](https://www.hypr.com/security-encyclopedia/elliptic-curve-digital-signature-algorithm) ( `ECDSA`) uses elliptic curve cryptography to generate digital signatures that can authenticate the parties involved in the key exchange.

Let us summarize and compare these algorithms:

| **Algorithm** | **Acronym** | **Security** |
| --- | --- | --- |
| `Diffie-Hellman` | `DH` | Relatively secure and computationally efficient |
| `Rivest–Shamir–Adleman` | `RSA` | Widely used and considered secure, but computationally intensive |
| `Elliptic Curve Diffie-Hellman` | `ECDH` | Provides enhanced security compared to traditional Diffie-Hellman |
| `Elliptic Curve Digital Signature Algorithm` | `ECDSA` | Provides enhanced security and efficiency for digital signature generation |

* * *

## Internet Key Exchange

[Internet Key Exchange](https://www.hypr.com/security-encyclopedia/internet-key-exchange) ( `IKE`) is a protocol used to establish and maintain secure communication sessions, such as those used in VPNs. It uses a combination of the `Diffie-Hellman` key exchange algorithm and `other cryptographic techniques` to securely exchange keys and negotiate security parameters. Besides, it is a key component of many VPN solutions, as it enables the secure exchange of keys and other security information between the VPN client and server. This allows the VPN to establish an encrypted tunnel through which data can be transmitted securely.

IKE can also be used for other purposes, such as in the authentication of users and devices. It is typically used in conjunction with other protocols and algorithms, such as the RSA algorithm for key exchange and digital signatures, and the [Advanced Encryption Standard](https://www.geeksforgeeks.org/advanced-encryption-standard-aes/) ( `AES`) for data encryption.

IKE operates either in `main mode` or `aggressive mode`. These modes determine the sequence and parameters of the key exchange process and can affect the security and performance of the IKE session.

#### Main Mode

The `main mode` is the default mode for `IKE` and is generally considered `more secure` than the aggressive mode. The key exchange process is performed in `three phases` in the main mode, each exchanging a different set of security parameters and keys. This allows for greater flexibility and security but can also result in slower performance compared to aggressive mode.

#### Aggressive Mode

`Aggressive mode` is an alternative mode for `IKE` that provides `faster performance` by reducing the number of round trips and message exchanges required for key exchange. In this mode, the key exchange process is performed in `two phases`, with all security parameters and keys being exchanged in the first phase. However, this can provide faster performance but may also reduce the security of the IKE session compared to the main mode since the `aggressive mode` does not provide identity protection.

#### Pre-Shared Keys

In IKE, a `Pre-Shared Key` ( `PSK`) is a secret value shared between the two parties involved in the key exchange. This key is used to authenticate the parties and establish a shared secret that encrypts subsequent communication. The use of a PSK is optional in IKE, and whether or not to use one depends on the specific requirements and constraints of the situation. However, if a `PSK` is used, it must be securely exchanged between the two parties before the key exchange process begins. This can be done through a secure out-of-band channel, such as a separate communication channel, or by physically exchanging the key.

The main advantage of using a PSK is that it provides an additional layer of security by allowing the parties to authenticate with each other. However, using a PSK also has some limitations and drawbacks. For example, it can be difficult to exchange the key securely, and if the key is compromised through a MITM attack, the security of the IKE session may be compromised.


# Authentication Protocols

* * *

Many different authentication protocols are used in networking to verify the identity of devices and users. Those protocols are essential because they provide a secure and standardized way of `verifying the identity` of users, devices, and other entities in a network. Without authentication protocols, it would be difficult to securely and reliably identify entities in a network, making it easy for attackers to gain unauthorized access and potentially compromise the network.

Authentication protocols also provide a means for `securely exchanging information` between entities in a network which we will discuss briefly. This is important for ensuring the confidentiality and integrity of sensitive data and preventing unauthorized access and other security threats. Let us take a look at a few most commonly used authentication protocols:

| **Protocol** | **Description** |
| --- | --- |
| `Kerberos` | Key Distribution Center (KDC) based authentication protocol that uses tickets in domain environments. |
| `SRP` | This is a password-based authentication protocol that uses cryptography to protect against eavesdropping and man-in-the-middle attacks. |
| `SSL` | A cryptographic protocol used for secure communication over a computer network. |
| `TLS` | TLS is a cryptographic protocol that provides communication security over the internet. It is the successor to SSL. |
| `OAuth` | An open standard for authorization that allows users to grant third-party access to their web resources without sharing their passwords. |
| `OpenID` | OpenID is a decentralized authentication protocol that allows users to use a single identity to sign in to multiple websites. |
| `SAML` | Security Assertion Markup Language is an XML-based standard for securely exchanging authentication and authorization data between parties. |
| `2FA` | An authentication method that uses a combination of two different factors to verify a user's identity. |
| `FIDO` | The Fast IDentity Online Alliance is a consortium of companies working to develop open standards for strong authentication. |
| `PKI` | PKI is a system for securely exchanging information based on the use of public and private keys for encryption and digital signatures. |
| `SSO` | An authentication method that allows a user to use a single set of credentials to access multiple applications. |
| `MFA` | MFA is an authentication method that uses multiple factors, such as something the user knows (a password), something the user has (a phone), or something the user is (biometric data), to verify their identity. |
| `PAP` | A simple authentication protocol that sends a user's password in clear text over the network. |
| `CHAP` | An authentication protocol that uses a three-way handshake to verify a user's identity. |
| `EAP` | A framework for supporting multiple authentication methods, allowing for the use of various technologies to verify a user's identity. |
| `SSH` | This is a network protocol for secure communication between a client and a server. We can use it for remote command-line access and remote command execution, as well as for secure file transfer. SSH uses encryption to protect against eavesdropping and other attacks and can also be used for authentication. |
| `HTTPS` | This is a secure version of the HTTP protocol used for communication on the internet. HTTPS uses SSL/TLS to encrypt communication and provide authentication, ensuring that third parties cannot intercept and read the transmitted data. It is widely used for secure communication over the internet, particularly for web browsing. |
| `LEAP` | LEAP is a wireless authentication protocol developed by Cisco. It uses EAP to provide mutual authentication between a wireless client and a server and uses the RC4 encryption algorithm to encrypt communication between the two. Unfortunately, LEAP is vulnerable to dictionary attacks and other security vulnerabilities and has been largely replaced by more secure protocols such as EAP-TLS and PEAP. |
| `PEAP` | PEAP on the other hand is a secure tunneling protocol used for wireless and wired networks. It is based on EAP and uses TLS to encrypt communication between a client and a server. PEAP uses a server-side certificate to authenticate the server and can also be used to authenticate the client using various methods, such as passwords, certificates, or biometric data. PEAP is widely used in enterprise networks for secure authentication. |

For example, LEAP and PEAP may be used to authenticate wireless clients when they access the wireless network or to authenticate remote employees connecting to the network via a VPN. In these cases, using SSH or HTTPS would be challenging to implement, as they are designed for different purposes. In terms of security, `PEAP` is generally more secure than LEAP because it uses a server-side public key certificate to authenticate the server and encrypting `MSCHAPv2` hash, while `LEAP` relies on a shared secret that is negotiated between the client and the server and does `not` encrypt `MSCHAPv2` hashes. PEAP also supports the use of stronger encryption algorithms, such as AES and 3DES, for encrypting the authentication information, whereas LEAP uses the weaker RC4 algorithm.

However, both protocols are vulnerable to specific attacks and have been largely replaced by more secure protocols such as EAP-TLS.

As physical connections, protocols with `SSL` or `TLS` are used by default, such as `SSH` or `HTTPS`. Both protocols use robust encryption algorithms to protect the authentication information transmitted between the client and the server. This helps to prevent interception or to tamper the authentication data, which is essential for maintaining the security of the authentication process.
Also, they support using digital certificates and `PKI` for authenticating the server to the client. This ensures that the client can verify the server's identity and helps to prevent MITM attacks. SSH and HTTPS are widely used and well-supported protocols, with implementations available for various operating systems and devices and makes them easy to use and deploy in a variety of environments.


# TCP/UDP Connections

* * *

[Transmission Control Protocol](https://en.wikipedia.org/wiki/Transmission_Control_Protocol) ( `TCP`) and [User Datagram Protocol](https://en.wikipedia.org/wiki/User_Datagram_Protocol) ( `UDP`) are both protocols used in information and data transmission on the Internet. Typically, TCP connections transmit important data, such as web pages and emails. In contrast, UDP connections transmit real-time data such as streaming video or online gaming.

`TCP` is a connection-oriented protocol that ensures that all data sent from one computer to another is received. It is like a telephone conversation where both parties remain connected until the call is terminated. If an error occurs while sending data, the receiver sends a message back so the sender can resend the missing data. This makes `TCP` reliable and slower than UDP because more time is required for transmission and error recovery.

`UDP`, on the other hand, is a connectionless protocol. It is used when speed is more important than reliability, such as for video streaming or online gaming. With `UDP`, there is no verification that the received data is complete and error-free. If an error occurs while sending data, the receiver will not receive this missing data, and no message will be sent back to resend it. Some data may be lost with `UDP`, but the overall transmission is faster.

* * *

## IP Packet

An [Internet Protocol](https://en.wikipedia.org/wiki/Internet_Protocol) ( `IP`) packet is the data area used by the network layer of the [Open Systems Interconnection](https://en.wikipedia.org/wiki/OSI_model) ( `OSI`) model to transmit data from one computer to another. It consists of a header and the payload, the actual payload data.

We can also think of the IP packet as a letter sent in an envelope. The envelope contains the header, which includes information on the sender and the recipient, as well as instructions for routing the letter, i.e., via which post offices the letter should be sent. The letter itself is the payload, the actual payload data.

#### IP header

The header of an IP packet contains several fields that have important information.

| **Field** | **Description** |
| --- | --- |
| `Version` | Indicates which version of the IP protocol is being used |
| `Internet Header Length` | Indicates the size of the header in 32-bit words |
| `Class of Service` | Means how important the transmission of the data is |
| `Total length` | Specifies the total length of the packet in bytes |
| `Identification (ID)` | Is used to identify fragments of the packet when fragmented into smaller parts |
| `Flags` | Used to indicate fragmentation |
| `Fragment Offset` | Indicates where the current fragment is placed in the packet |
| `Time to Live` | Specifies how long the packet may remain on the network |
| `Protocol` | Specifies which protocol is used to transmit the data, such as TCP or UDP |
| `Checksum` | Is used to detect errors in the header |
| `Source/Destination` | Indicate where the packet was sent from and where it is being sent to |
| `Options` | Contain optional information for routing |
| `Padding` | Pads the packet to a full word length |

We may see a computer with multiple IP addresses in different networks. Here we should pay attention to the `IP ID` field. It is used to identify fragments of an IP packet when fragmented into smaller parts. It is a `16-bit` field with a unique number ranging from `0-65535`.

If a computer has multiple IP addresses, the `IP ID` field will be different for each packet sent from the computer but very similar. In TCPdump, the network traffic might look something like this:

#### Network Sniffing

```shell
IP 10.129.1.100.5060 > 10.129.1.1.5060: SIP, length: 1329, id 1337
IP 10.129.1.100.5060 > 10.129.1.1.5060: SIP, length: 1329, id 1338
IP 10.129.1.100.5060 > 10.129.1.1.5060: SIP, length: 1329, id 1339
IP 10.129.2.200.5060 > 10.129.1.1.5060: SIP, length: 1329, id 1340
IP 10.129.2.200.5060 > 10.129.1.1.5060: SIP, length: 1329, id 1341
IP 10.129.2.200.5060 > 10.129.1.1.5060: SIP, length: 1329, id 1342

```

We can see from the output that two different IP addresses are sending packets to IP address 10.129.1.1. However, from the `IP ID`, we can see that the packets are continuous. This strongly indicates that the two IP addresses belong to the same host in the network.

#### IP Record-Route Field

The `Record-Route field` in the IP header also records the route to a destination device. When the destination device sends back the `ICMP Echo Reply` packet, the IP addresses of all devices that pass through the packet are listed in the `Record-Route field` of the IP header. This happens when we use the following command, for example:

```shell
ping -c 1 -R 10.129.143.158

PING 10.129.143.158 (10.129.143.158) 56(124) bytes of data.
64 bytes from 10.129.143.158: icmp_seq=1 ttl=63 time=11.7 ms
RR: 10.10.14.38
        10.129.0.1
        10.129.143.158
        10.129.143.158
        10.10.14.1
        10.10.14.38

--- 10.129.143.158 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 11.688/11.688/11.688/0.000 ms

```

The output indicates that a `ping` request was sent and a response was received from the destination device and also shows the `Record-Route field` in the IP header of the `ICMP Echo Request` packet. The Record Route field contains the IP addresses of all devices that passed through the `ICMP Echo Request` packet on the way to the destination device. In this case, the `Record-Route field` contains the IP addresses:

|  |  |  |
| --- | --- | --- |
| 10.10.14.38 | 10.129.0.1 | 10.129.143.158 |
| 10.129.143.158 | 10.10.14.1 | 10.10.14.38 |

The `traceroute` tool can also be used to trace the route to a destination more accurately, which uses the TCP timeout method to determine when the route has been fully traced.

1. We send a TCP SYN packet to the destination device with a TTL of 1 in the IP header.

When the TCP SYN packet with a TTL greater than 1 reaches a router, the value of the TTL is decreased by 1, and the packet is forwarded to the next device. If the TCP SYN packet with a TTL of 1 reaches a router, the packet is dropped, and the router sends an ICMP Time-Exceeded packet back to us.

2. We receive the ICMP Time-Exceeded packet and note the IP address of the router that sent the packet.

3. After that, we send another TCP SYN packet to the destination, increasing the TTL by 1.


The process repeats until the TCP SYN packet reaches the destination host and receives a `TCP SYN/ACK` or a `TCP RST` response from the target. Once we receive a response from the destination device, we know that we have traced the route to the destination and ended the traceroute process.

#### IP Payload

The payload (also referred to as `IP Data`) is the actual payload of the packet. It contains the data from various protocols, such as TCP or UDP, that are being transmitted, just like the contents of the letter in the envelope.

* * *

## TCP

TCP packets, also known as `segments`, are divided into several sections called headers and payloads. The TCP segments are wrapped in the sent IP packet.

The header contains several fields that contain important information. The source port indicates the computer from which the packet was sent. The destination port indicates to which computer the packet is sent. The sequence number indicates the order in which the data was sent. The confirmation number is used to confirm that all data was received successfully. The control flags indicate whether the packet marks the end of a message, whether it is an acknowledgment that data has been received, or whether it contains a request to repeat data. The window size indicates how much data the receiver can receive. The checksum is used to detect errors in the header and payload. The Urgent Pointer alerts the receiver that important data is in the payload.

The payload is the actual payload of the packet and contains the data that is being transmitted, just like the content of a conversation between two people.

* * *

## UDP

UDP transfers `datagrams` (small data packets) between two hosts. It is a connectionless protocol, meaning it does `not` need to establish a connection between the sender and the receiver before sending data. Instead, the data is sent directly to the target host without any prior connection.

When `traceroute` is used with UDP, we will receive a `Destination Unreachable` and `Port Unreachable` message when the UDP datagram packet reaches the target device. Generally, UDP packets are sent using `traceroute` on Unix hosts.

* * *

## Blind Spoofing

`Blind spoofing`, is a method of data manipulation attack in which an attacker sends false information on a network without seeing the actual responses sent back by the target devices. It involves manipulating the IP header field to indicate false source and destination addresses. For example, we send a TCP packet to the target host with false source and destination port numbers and a false `Initial Sequence Number` ( `ISN`). The `ISN` is a field in the TCP header that is used to specify the sequence number of the first TCP packet in a connection. The ISN is set by the sender of a TCP packet and sent to the receiver in the TCP header of the first packet. This can cause the target host to establish a connection with us without receiving the connection.

This attack is commonly used to disrupt the integrity of network connections or to break connections between network devices. It can also be used to monitor network traffic or to intercept information sent by network devices.


# Cryptography

* * *

Encryption is used on the Internet to transmit data, such as payment information, e-mails, or personal data, confidentially and protected against manipulation. Data is encrypted using various cryptographic algorithms based on mathematical operations. With the help of encryption, data can be transformed into a form that unauthorized persons can no longer read. Digital keys in `symmetric` or `asymmetric` encryption processes are used for encryption. It is easier to crack cipher texts or keys depending on the encryption methods used. If state-of-the-art cryptographic methods with extensive key lengths are used, they work very securely and are almost impossible to compromise for the time being. In principle, we can distinguish between `symmetric` and `asymmetric` encryption techniques. Asymmetric methods have only been known for a few decades. Nevertheless, they are the most frequently used methods in digital communication.

#### Symmetric Encryption

Symmetric encryption, also known as secret key encryption, is a method that uses the same key to encrypt and decrypt the data. This means the sender and the receiver must have the same key to decrypt the data correctly.

If the secret key is shared or lost, the security of the data is no longer guaranteed. Critical actions for symmetric encryption methods represent the distribution, storage, and exchange of the keys. [Advanced Encryption Standard](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard) ( `AES`) and [Data Encryption Standard](https://en.wikipedia.org/wiki/Data_Encryption_Standard) ( `DES`) are examples of symmetric encryption algorithms. This type of encryption is often used to encrypt large amounts of data, such as files on a hard drive or data sent over a network. `AES` is considered to be the most secure encryption algorithm nowadays.

#### Asymmetric Encryption

Asymmetric encryption, also known as `public-key encryption`, is a method of encryption that uses two different keys:

- a `public key`
- a `private key`

The public key is used to encrypt the data, while the private key is used to decrypt the data. This means anyone can use a public key to encrypt data for someone, but only the recipient with the associated private key can decrypt the data. Examples of asymmetric encryption methods include [Rivest–Shamir–Adleman](https://en.wikipedia.org/wiki/RSA_(cryptosystem)) ( `RSA`), [Pretty Good Privacy](https://en.wikipedia.org/wiki/Pretty_Good_Privacy) ( `PGP`), and [Elliptic Curve Cryptography](https://en.wikipedia.org/wiki/Elliptic-curve_cryptography) ( `ECC`). Asymmetric encryption is used in a variety of applications, some of which include:

|  |  |  |
| --- | --- | --- |
| E-Signatures | SSL/TLS | VPNs |
| SSH | PKI | Cloud |

* * *

## Public-Key Encryption

One advantage of asymmetric encryption is its `security`. Since the security is based on very hard-to-solve mathematical problems, simple attacks cannot crack it. Furthermore, the issue of key exchange is bypassed. This is a significant problem with symmetric encryption methods. However, since the public key can be accessible to everyone, there is no need to exchange keys secretly. In addition, the asymmetric methods open up the possibility of authentication with digital signatures.

* * *

## Data Encryption Standard

DES is a symmetric-key block cipher, and its encryption works as a combination of the one-time pad, permutation, and substitution ciphers applied to bit sequences. It uses the `same key` in both `encrypting and decrypting` data.

The key consists of `64 bits`, with `8 bits` used as a checksum. Therefore, the actual key length of DES is only `56 bits`. And that is why one always speaks of a key length of 56 bits when referring to DES. To prevent the danger from frequency analysis, not single letters, but each 64-bit block of plaintext is encrypted to a 64-bit block of ciphertext.

An extension of DES is the so-called [Triple DES / 3DES](https://en.wikipedia.org/wiki/Triple_DES), which encrypts data more securely. The procedure for this usually consists of three keys, with the first key being used to encrypt the data, the second to decrypt the data, and the third to encrypt the data again.

`3DES` was considered more secure than the original DES because it provides greater security using three rounds of encryption, although using a 56-bit key still limits it. `AES`, the successor to DES, provides higher security using longer key lengths and is now the most widely used symmetric encryption technology.

* * *

## Advanced Encryption Standard

Compared to DES, AES uses 128-bit ( `AES-128`), 192-bit ( `AES-192`), or 256-bit ( `AES-256`) keys to encrypt and decrypt data. In addition, AES is faster than DES because it has a more efficient algorithm structure. This is because it can be applied to multiple data blocks at once, making it faster. This means that AES encryption and decryption can be performed faster than DES, which is especially important when large amounts of data need to be encrypted.

For example, we can find AES in many different applications and protocols, but they are not limited to:

|  |  |  |
| --- | --- | --- |
| WLAN IEEE 802.11i | IPsec | SSH |
| VoIP | PGP | OpenSSL |

* * *

## Cipher Modes

A cipher mode refers to how a block cipher algorithm encrypts a plaintext message. A block cipher algorithm encrypts data, each using fixed-size blocks of data (usually 64 or 128 bits). A cipher mode defines how these blocks are processed and combined to encrypt a message of any length. There are several common cipher modes, including:

| **Cipher Mode** | **Description** |
| --- | --- |
| [Electronic Code Book](https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation) ( `ECB`) mode | ECB mode is generally not recommended for use due to its susceptibility to certain types of attacks. Furthermore, it does not hide data patterns efficiently. As a result, statistical analysis can reveal elements of clear-text messages, for example, in web applications. |
| [Cipher Block Chaining](https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation#CBC) ( `CBC`) mode | CBC mode is generally used to encrypt messages like disk encryption and e-mail communication. This is the default mode for AES and is also used in software like TrueCrypt, VeraCrypt, TLS, and SSL. |
| [Cipher Feedback](https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation#Cipher_feedback_(CFB)) ( `CFB`) mode | CFB mode is well suited for real-time encryption of a data stream, e.g., network communication encryption or encryption/decryption of files in transit like Public-Key Cryptography Standards (PKCS) and Microsoft's BitLocker. |
| [Output Feedback](https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation#OFB) ( `OFB`) mode | OFB mode is also used to encrypt a data stream, e.g., to encrypt real-time communication. However, this mode is considered better for the data stream because of how the key stream is generated. We can find this mode in PKCS but also in the SSH protocol. |
| [Counter](https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation#CTR) ( `CTR`) mode | CTR mode encrypts real-time data streams AES uses, e.g., network communication, disk encryption, and other real-time scenarios where data is processed. An example of this would be IPsec or Microsoft's BitLocker. |
| [Galois/Counter](https://en.wikipedia.org/wiki/Galois/Counter_Mode) ( `GCM`) mode | GCM is used in cases where confidentiality and integrity need to be protected together, such as wireless communications, VPNs, and other secure communication protocols. |

Each mode has its characteristics and is more suitable for certain use cases. The choice of encryption mode depends on the application's requirements and the security objectives to be achieved.


