# Introduction

* * *

A new type of content for HackTheBox (HTB) Academy, the big question that many of you might ask is, "Why Game Hacking?". The simple answer is that it is a highly accessible pathway into the world of information security. The more detailed explanation is that there is an incredible amount of overlap between techniques, information and tools you are exposed to via Game Hacking and the far more intimidating infosec world. Because of this goal, these modules will focus on specific techniques and tools that apply to infosec and will not be a general 'how-to hack video games' path.

A great example is utilising memory searching techniques to look for a health value in a video game. Once you find it, you can modify it to become immortal, for instance. Extrapolate the same technique to find unprotected flags in HTB challenges, leading to a possible unintended method for solving them. Looking at a real-world example, how about extracting privileged information from memory, such as passwords or credit card information?

How about intercepting and modifying data sent between a video game and a server using an extremely well-known tool, Burp Suite, using the same techniques that will be used when pen-testing virtually every website?

Those are the types of overlaps we are talking about. What you learn from these modules will stand you in good stead when moving into the wider world of information security.

This, and future modules, will focus heavily on the Windows Operating System. Windows has, by far, the most mature and established Game Hacking environment and still dominates the PC gaming market by OS share. The games provided with each module and/or section should be runnable within a virtual machine if Windows is not your primary operating system.

It should be noted that there are a few `requirements` though:

- You will require a laptop or a desktop computer with a GPU (Graphics Card). The Intel HD 4600 Integrated Graphics, AMD HD 6570 or GeForce 9600GT should be considered the bare minimum to get playable performance out of the game. You can try resizing the game to smaller dimensions if you are experiencing crippling performance, by grabbing and dragging the corners of the running process.

- If you want to run it in a Virtual Machine, VMWare Player is preferred over VirtualBox for Virtualization on Windows and Linux and Parallels on ARM Macs. Be sure to `enable GPU Acceleration` in the VM settings where applicable and install `VMWare Tools` if using VMWare Player.


## What is Game Hacking

Game hacking is a process that involves modifying a game's code, data, or mechanics to gain an unfair advantage over other players or to access content that is not ordinarily available. While some people engage in game hacking for fun or as a hobby, others use it to cheat and gain an advantage in online multiplayer games, which can ruin the experience for other players.

This can include cheating tools such as aimbots, wallhacks, and speed hacks, which allow players to automatically aim at opponents, see through walls or move faster than expected. Other forms of game hacking may involve modifying the game's code to create custom mods or to remove limitations imposed by the game's developers.

Game hacking can be considered a subset of information security (infosec), specifically in offensive security or "red teaming." In this context, game hacking is used to identify vulnerabilities in a game's code and can help game developers improve the security of their software.

In addition, some game developers employ security experts to help identify and prevent cheating in their games, which can be seen as information security. Furthermore, as online gaming becomes increasingly popular, game hacking can significantly threaten the security and privacy of players' personal information.

Therefore, game hacking is one aspect of the broader field of information security, as it involves identifying and exploiting vulnerabilities in software systems.


# The Methodology

* * *

All infosec tasks can be approached in the same manner.

## **Identify the goal.**

The first step is identifying what you are trying to achieve and being realistic about the goal. This means thinking about what resources you want to gain, what features you want to unlock, or what kind of gameplay experience you're trying to create. It's important to be specific and realistic about your goal, as this will help you develop a clear strategy for achieving it.

To extrapolate the point into broader infosec: Do we want to gain admin access to a website or exploit a software program to gain root access?

## **Understand how it works.**

Once you have identified what your goal is, you need to have an understanding of the processes and functionality involved. Take the infinite money example. In the game, you have a visible counter representing the quantity of money in your possession. How is the value controlled? It is changed when you either spend something or gain more money.

Take the exploit example as another example. Are there any obvious possible issues with standard functionality? Does the program crash or behave abnormally if we provide a malformed input somewhere?

## **How are you going to achieve your goal?**

Once you understand the game, you can develop a strategy for achieving your goal. This involves deciding on the specific tools and techniques you will use to hack the game and creating a step-by-step plan for carrying out the hack. Flexibility and adaptability in your strategy are essential, as you may encounter unexpected challenges or obstacles.

Continuing with the money example, we have observed that the value changes when we purchase something or gain more money in-game. Using that knowledge, we can find the value using memory searching. We might be able to edit game files to make everything free or patch the money generation function so we earn a crazily large number. All are valid options to achieve our overall goal of having 'infinite' money.

If we continue with the exploit example, if the program crashes with a malformed input, is it because the input is much larger than expected? An example is a program prompting for an email address, and we give it one that is 1000 characters long. Have we identified a potential buffer overflow that we can exploit?

## General Game Hacking Rules

1. It is essential to understand that game hacking (and pen testing in general) can be highly illegal and result in legal consequences. A notable example is Blizzard Entertainment which successfully sued what was the biggest World of Warcraft bot maker at the time. Many game developers have also implemented measures to prevent cheating and hacking and actively ban players caught doing so. It is essential to approach game hacking cautiously and know the potential consequences. When engaging with content that could result in such consequences, especially in games where your actions could affect another players experience, be sure to obtain the proper authorizations beforehand.

2. It is crucial to approach game hacking with a robust ethical framework. Game hacking can be used for good, such as to expose security vulnerabilities in games or to create mods that enhance the game experience for all players. However, game hacking can also be used for malicious purposes, such as to cheat or exploit other players. It is important to consider your game hacking activities' impact on other players and the game community.

3. It is vital to approach game hacking with a growth mindset. This means being willing to learn from failures and mistakes and persist in facing challenges. Game hacking constantly evolves and requires a willingness to adapt and learn new techniques and tools.

4. It is important to approach game hacking with a collaborative mindset. Game hacking often involves working with other hackers and modders and requires a willingness to share knowledge and collaborate on projects. This can be achieved through online forums and communities, where hackers can share ideas and collaborate on projects.


In conclusion, game hacking can be complex and challenging, requiring a robust ethical framework, a good understanding of the game being hacked, a growth mindset, a collaborative mindset, and a sense of responsibility. With the right approach and attitude, game hacking can be rewarding and fulfilling for those interested.


# The Tooling

* * *

## Cheat Engine

We have obtained special permission from DarkByte, the author of Cheat Engine, to distribute Cheat Engine along with this module. Usually it is only available via the Cheat Engine Website where it is bundled with InstallCore Adware, or via DarkByte's Patreon. Please do not redistribute (share) this file.

Game Hacking is still very much focused on Windows, as Mac and Linux gaming are still in their infancy. To this end, if you cannot access a Windows computer, refer to the ["Setting Up"](https://academy.hackthebox.com/module/details/87/) module for help on creating a Windows Virtual Machine.

Many tools are used in Game Hacking; however, the most notable is a software suite called Cheat Engine, which has been in development since 2000. It is a comprehensive Game Hacking toolkit that offers functionality for every scenario. Its main functionality is the ability to scan and filter through memory addresses. Those addresses represent everything about the state of the game in memory, and by scanning and filtering for specific addresses, we can manipulate that state to our will.

[Download our Cheat Engine archive here](https://academy.hackthebox.com/storage/modules/182/CheatEngine-7.5-HTB.zip), password is `hackthebox`, and extract it to a location on your computer, I usually use a directory on the root of my system drive such as `C:\CE`, and then run it via the `Cheat Engine.exe` executable when needed. Please do not redistribute (share) this file. If you get an error trying to extract the archive, you may need to use 7zip or any other archiving software package (winzip, winrar, peazip, etc) that will support LZMA compression.

## The Interface

![](https://academy.hackthebox.com/storage/modules/182/Cheat-Engine.gif)

The Cheat Engine interface is pretty simple. The first noticeable thing is the pulsating button in the top left. This "Open Process" button allows Cheat-Engine to target regions in your computer's memory specifically related to that selected process.

A quick note, I'm using Windows Dark Mode, and Cheat Engine supports system theming, so the screenshots provided are dark, and may look slightly different to yours. It's possible to change themes as you wish via the Cheat Engine settings -> General Settings -> Tick the CheckBox "Disable Dark Mode Support"

It is comprised of several sections:

![](https://academy.hackthebox.com/storage/modules/182/CE-Main.png)

1. **Search options** \- Here are all the options you will set for your search and where you will spend most of your time in Cheat Engine.

2. **Search results** \- List all memory addresses found for the matching search criteria.

3. **Memory View** \- The Memory View button will open the disassembler and hex view window. That window also contains the majority of Cheat Engine's more powerful tools.

4. **Address List** \- The Address List (aka Cheat Table) is your sandbox in Cheat Engine. It's where you can work with all memory addresses you have decided to add from the address list, as well as scripts and other functionality. This is also the data that will persist when saved and loaded.


## Search Options

Most of Cheat Engines' functionality revolves around scanning for memory addresses. The Search Options pane will allow you to fine-tune exactly what you want. From top to bottom:

`First Scan`: This is the initial scan you perform to search for a specific value in the game's memory. The first scan is run according to the options selected in the Search Options pane. The first scan results are saved in Cheat Engine's memory, and you can use these results for subsequent searches and are displayed in the results list to the left of the pane.

`Next Scan`: This is a follow-up scan you perform after the first scan to narrow the search results further. You can choose from different scan types (exact value, value between, etc.) to perform the next scan, using the results of previous searches to refine the search. For example, if you performed a first scan for an exact value of "50" and got 1000000 results, the value then changes to "60"; you can perform a next scan for an exact value of "60" against the initial 1000000 to filter all values that have changed to "60".

The `Hex` checkbox will allow you to input a hex value into the `Value field`. The `Value field` is where you will input what you are searching for. For example, If you have three lives in-game, you will input 3.

The `Scan Type` combo box will change how Cheat Engine approaches the search based on specified criteria. It will vary depending on whether you are conducting an initial First or a subsequent Next Scan.

The First Scan options are:

1. `Exact Value`: This searches for values that match the exact value you enter.

2. `Bigger than...`: This searches for values bigger than the value you enter.

3. `Smaller than...`: This searches for values smaller than the value you enter.

4. `Value Between`: This searches for values between two specified values. A second input will appear for the second value.

5. `Unknown Initial Value`: This searches for every value in memory, as you do not know what to enter as a known value


The Next Scan option types are as follows:

01. `Exact Value`: This type searches for values that match the exact value you specified. For example, if you entered "100" in the first scan and "200" for the next scan, this type will find all address values have changed from "100" to "200".

02. `Bigger than...`: This type searches for values greater than your specified value. For example, if you entered "100" in the first scan, this type will find all values greater than 100.

03. `Smaller than...`: This type searches for values less than your specified value. For example, if you entered "100" in the first scan, this type will find all values less than 100.

04. `Value between...`: This type searches for values between the range of values you specified. For example, if you entered "50" and "100", this type will find all values between 50 and 100.

05. `Increased Value`: This type searches for increased values. For example, if you entered "100" in the first scan and the value changed to "500", this type will find all values that have increased from 100 to any other value.

06. `Increased Value by...`: This type searches for values that have increased by the amount you entered in the first scan. For example, if you entered "100" in the first scan and the value changed to "150", this type will find all values that have increased by 50.

07. `Decreased Value`: This type searches for decreased values since the first scan. For example, if you entered "100" in the first scan and the value changed to "10", this type will find all values that have decreased from 100 to any other value.

08. `Decreased Value by...`: This type searches for values that have decreased by the amount you entered in the first scan. For example, if you entered "100" in the first scan and the value changed to "50", this type will find all values that have decreased by 50.

09. `Changed Value`: This type searches for values that have changed since the first scan. For example, if you entered "100" in the first scan and the value changed to "2000", this type will find all values that have changed from 100 to any other value.

10. `Unchanged Value`: This type searches for values that have stayed the same since the first scan. For example, if you entered "100" in the first scan and the value has remained the same, this type will find all values that have not changed from 100.

11. `Same as First Scan`: This type searches for values like the values you entered in the first scan. For example, if you entered "100" in the first scan, this type will find all values that are 100.


Scan value type provides options for the data type you are scanning for. The following section on Data and Memory explains these data types more in-depth.

The rest of the options are for more advanced uses and are out of the scope of this module but will likely be covered if needed.

## Search Results

![](https://academy.hackthebox.com/storage/modules/182/CE-SearchResults.png)

The address list is where the results of your memory scans are temporarily stored. Each entry will contain the following fields:

- `Address` \- A hexadecimal memory address for the entry

- `Value` \- The current value for the entry

- `Previous` \- The previous value, as in what the value was before the current scan, for the entry

- `First` \- The first value the entry contained when it was found


An address coloured green means it is static and won't change. Values (including Previous and First) highlighted in red have changed in memory since the first scan. This provides a quick method to filter addresses by eye when you only have a few remaining rather than having to carry out a scan.

## Memory Viewer

![](https://academy.hackthebox.com/storage/modules/182/CE-MemoryViewer.png)

The memory viewer is a launch pad for Cheat Engine's most advanced features.

The top 1/2 is the `Disassembler`, a feature that allows you to explore the assembly code of a target process. It displays the assembly code in a readable format, with instructions in mnemonic form and the corresponding machine code shown in hex. The Disassembler can also search for specific instructions or patterns in the assembly code and modify or replace the code. This is where you will require a basic understanding of assembly to interact with the game at a deeper level.

The bottom half is the actual `Memory View`. This is a hex (hexadecimal, aka base-16) editor. A hex editor is a specialised software tool designed to display and edit binary data. The interface is comprised of 2 main parts.

1. The Hexadecimal View: This panel displays the binary data in fixed length rows, typically 16 or 32 bytes per row. Two hexadecimal digits represent each byte, and the rows are often separated by lines to make it easier to distinguish between them.

2. The ASCII View: This panel shows the ASCII representation of the same data displayed in the hexadecimal view. Each byte is translated into its corresponding ASCII character, and the rows are aligned with the rows in the hexadecimal view. The ASCII view often provides context and readability to the displayed binary data.


Additional tools and utilities are in the `Tools` menu for complex use cases and may be covered in a future module.

## Address list (aka Cheat Table)

This is where you will work with the addresses you have found via memory searching. The official term for this interface section is the "address list", but when you share your work with others, it's called a "Cheat Table" with the `.ct` extension, and you are sharing everything contained in this table; hence I refer to it as the cheat table for that reason.

The Cheat Table contains a row for each entry, and that entry can be anything, from an address found via memory scanning, to a pointer, to a custom Cheat Engine script. The checkbox on the far left of the row can be used to toggle scripts, expand groups, and freeze addresses to the current value.


# Understanding Data Types and Memory

* * *

Computer memory, also known as RAM ( `Random Access Memory`), is a type of computer hardware that stores data and instructions that the computer is currently using. It is a temporary form of storage that the computer uses to hold data and instructions that it needs to access quickly.

The basic principle behind memory (RAM) is that it uses `electronic components`, such as capacitors and transistors, to store and retrieve data. Each piece of data in memory is stored in a `memory cell`, which is made up of one or more transistors and capacitors. The `state` of each transistor and capacitor represents a binary value, `either 0 or 1`. The capacitors hold the charge describing the binary value, and the transistors control the data flow into and out of the memory cell.

When the CPU needs to read or write data to or from RAM, it sends a request to the memory controller, which coordinates data transfer between the CPU and RAM. The memory controller uses the address specified by the CPU to locate the memory cell containing the desired data.

## Binary Numbers

`One byte` is typically stored in memory as a `contiguous sequence of eight bits`, each of which can be either a `0` or a `1`. These eight bits are stored in a memory cell, a small memory unit that can store a single byte.

When a byte is stored in memory, each bit is stored in a separate memory cell within the same byte. By convention, binary numbers are represented with the `least significant bit` (LSB) on the right and the `most significant bit` (MSB) on the left. This convention is consistent across computer architectures and is based on how binary numbers are represented and manipulated.

The reason for this convention is that binary numbers are `represented using a series of bits`, each representing a `power of 2.` The value of each bit depends on its position in the number, with the `rightmost bit` representing the `lowest power of 2 ` and the `leftmost bit` representing the `highest power of 2`. Thus, the MSB has the greatest potential effect on the value of the number, while the LSB has the smallest potential effect on its value.

This means that the binary value of the byte can be represented as a sequence of eight bits, such as `01101001` or `11001100`, where each bit corresponds to a power of 2 (starting with `2^0` on the right and increasing to `2^7` on the left).

To give a clear example, let's consider an 8-bit binary number `1010 1010`.

| Bit Position | Binary Value | Decimal Equivalent | Description |
| --: | :-: | :-: | :-- |
| MSB (7) | 1000 0000 | 128 | Most Significant Bit |
| 6 | 0100 0000 | 64 |  |
| 5 | 0010 0000 | 32 |  |
| 4 | 0001 0000 | 16 |  |
| 3 | 0000 1000 | 8 |  |
| 2 | 0000 0100 | 4 |  |
| 1 | 0000 0010 | 2 |  |
| LSB (0) | 0000 0001 | 1 | Least Significant Bit |

Its decimal value is `128+0+32+0+8+0+2+0=170`.

So, the number `1010 1010` in binary corresponds to `170` in decimal.

From this, you can observe that changing the `MSB `(bit position 7) alters the value by `128`, while changing the `LSB `(bit position 0) alters the value by only `1`. The `MSB ` has the greatest potential effect on the value, while the `LSB ` has the least.

To retrieve a byte from memory, the memory controller uses the address of the byte to locate the memory cell that contains the byte. The memory controller then retrieves the eight bits stored in the memory cells and assembles them into a single byte. Conversely, to store a byte in memory, the memory controller divides the byte into its individual bits and stores each bit in a separate memory cell within the byte.

## Common Data Types & Endianness

A single byte, representing only `2^8 = 256` distinct values ranging from `0 to 255`, is inadequate for pretty much any digital application. This limited range falls short when we need to represent large numbers, characters from extensive character sets, or precise floating-point values. To address this limitation, we use multi-byte data types, which allocate more than one byte to capture a broader range of values in memory.

These data types serve as classifications within computer programs, indicating the kind of information a variable holds and defining the operations it can undergo. For example, the `integer` data type is tailored for whole numbers, whereas the `string` data type encompasses sequences of `characters`, embodying textual data. Beyond determining the memory allocation for a value, a data type also stipulates the set of operations that can be performed on that value.

| Data Type | Byte Length | Description | Example | Range |
| --: | --- | --- | --- | :-- |
| byte | 1 byte | 8-bit unsigned integer | 127 | 0 to 255 |
| short | 2 bytes | 16-bit signed integer | -32,768 | -32,768 to 32,767 |
| int | 4 bytes | 32-bit signed integer | 1,000,000 | -2,147,483,648 to 2,147,483,647 |
| long | 8 bytes | 64-bit signed integer | 9,223,372,036,854,775,807 | -9,223,372,036,854,775,808 to 9,223,372,036,854,775,807 |
| float | 4 bytes | 32-bit floating-point number | 3.14159265 | ±1.5 × 10^-45 to ±3.4 × 10^38 |
| double | 8 bytes | 64-bit floating-point number | 3.14159265358979323846 | ±5.0 × 10^-324 to ±1.7 × 10^308 |
| bool | 1 byte | Boolean (true - 1/false - 0) value | true (1) | true or false (1 or 0) |
| char | 2 bytes | 16-bit Unicode character | 'A' | 0 to 65,535 |
| string | Varies | Sequence of characters | "Hello, world!" | Varies |

There is a crucial concept to understand with data types. If we write a number down, say `12345`, we read it left to right. However, computers generally do not, so we need to discuss a concept called endianness.

Endianness refers to the order bytes are stored or transmitted in multi-byte data types. Since a byte consists of 8 bits, data types requiring more than 8 bits, such as a 32-bit integer, will span multiple bytes. The order in which these bytes are stored or read can vary based on the system's endianness. There are two primary types of endianness: `big-endian` and `little-endian`.

In a `big-endian` system, the most significant byte of the data is stored at the lowest memory address, much like how we read numbers. If we take the hex number `0x12345678` as an example and represent it in a 4-byte integer, it will look like the below table in memory:

| Memory Address | Byte Value |
| :-: | :-: |
| 0 | 12 |
| 1 | 34 |
| 2 | 56 |
| 3 | 78 |

In contrast, a `little-endian` system stores the least significant byte at the lowest memory address.

| Memory Address | Byte Value |
| :-: | :-: |
| 0 | 0x78 |
| 1 | 0x56 |
| 2 | 0x34 |
| 3 | 0x12 |

This might initially seem counterintuitive, but certain architectures and systems prefer this method.

| System/Architecture | Endianness | Notes |
| --: | :-: | :-- |
| x86 (Intel, AMD) | Little-endian | Predominant architecture for computers |
| ARM (depends on version) | Both | Some ARM architectures can be switched between endiannesses |
| MIPS | Both | Can be configured as either big-endian or little-endian |
| SPARC | Big-endian | Some newer versions can switch to little-endian |
| IBM z/Architecture | Big-endian | Used in IBM mainframes |
| Java Virtual Machine (JVM) | Big-endian | Network byte order for JVM is big-endian |
| RISC-V | Little-endian | Has provisions for future big-endian support |

Let's say we have an integer variable named "money" with a value of `12345678`. In memory, it would look like this:

| Address | Value |
| --: | :-- |
| 0x1000 | 01001110 |
| 0x1001 | 01100001 |
| 0x1002 | 10111100 |
| 0x1003 | 00000000 |

Each row in the table represents a memory location, identified by its hexadecimal address, from `0x1000 to 0x1003`. By using the address of the first memory location ( `0x1000`) and the data type size (4 bytes for a 32-bit integer), we can determine the address of the following memory location used to store the variable. In this case, we're using a `little-endian` byte order, which means that the least significant byte is stored at the lowest memory address (0x1000), and the most significant byte is stored at the highest address (0x1003).

The value of the integer is stored in binary form, with each bit representing a power of 2. In this case, in little endian, the binary representation of `12345678 ` is `01001110 01100001 10111100 00000000`. For now, know that the `00000000` is padding used to fill the 4-byte data type because the number `12345678` is only 3 bytes long. It will be covered in more detail in the `Data Structures` section.

However, since our brains naturally don't think in terms of little-endian or big-endian, most software, including Cheat Engine, handles these conversions automatically. So when you change byte values in Cheat Engine, it will automatically adjust and store them in the correct order.

## Hexadecimal

When using Cheat Engine and all other debuggers and disassemblers, you will use a hexadecimal notation, a far more convenient way of representing binary data. `Don't be too concerned with knowing how to calculate binary numbers`. Understanding what binary is and how it works regarding memory is valuable, but you can happily hack games without a deep understanding of it. Many tools, such as [GCHQ's CyberChef](https://gchq.github.io/CyberChef/), can perform these calculations and conversions for you if needed.

Hexadecimal notation is a way of representing numbers using base-16. In mathematics, " `base`" refers to the `number of digits used to describe numbers in a particular numbering system`. In everyday life, we use `base-10`, also known as the `decimal system`, to calculate numbers using 10 digits: `0, 1, 2, 3, 4, 5, 6, 7, 8, and 9`

In `base-16` notation, there are `16 possible digits`: the numbers `0 to 9` and the letters `A to F`. `Each digit` in a hexadecimal number `represents` a different `power of 16`, starting with `16^0` on the rightmost digit and increasing by a power of 16 as you move to the left.

For example, the hexadecimal number `2A` represents the decimal value of `(2*16^1) + (10*16^0)`, which equals `42`. Here, the digit `2` represents the value of `2 multiplied by 16 (16^1)`, and the digit `A` represents the value of `10 multiplied by 1 (16^0)`. The letter `A` represents the decimal value 10; the letter `B` represents the decimal value 11, and so on, up to the letter `F`, which means the decimal value 15. `0x` is a common prefix used to denote a hexadecimal number and is irrelevant to the number itself.

To use the little-endian binary example from above, the number `12345678`, if we use hexadecimal notation, is `0xBC614E`. We can then have a much easier-to-understand representation of the table. Remember, this specific table is in little-endian.

| Address | Binary | Value |
| --: | :-: | :-- |
| 0x1000 | 01001110 | 0x4E |
| 0x1001 | 01100001 | 0x61 |
| 0x1002 | 10111100 | 0xBC |
| 0x1003 | 00000000 | 0x00 |

## Memory Scanning

Cheat Engine uses a technique called " `memory scanning`" to locate the address of the value you are looking for. This involves searching the program's memory for specific data patterns or values you define, such as a numerical value, e.g. your gold value in a game. The scanning process involves repeatedly reading sections of the program's memory and comparing the data against the search criteria until a match is found.

Cheat Engine needs to know the data type of the value searched for when scanning a program's memory. `This is because data types are represented differently in memory and have different sizes and byte alignments`.

For example, a 4-byte integer is typically represented in memory as a sequence of 4 contiguous bytes. In contrast, a floating-point number may be defined as a different sequence of bytes with different sizes and alignments. If Cheat Engine were to search for an integer using the byte pattern of a floating-point number, it would not find any matches, even if the integer value was present in the program's memory.

Cheat Engine allows users to select the data type they want to search for in the game's memory. Cheat Engine's scanning algorithm can properly interpret the memory contents and locate the desired value by choosing the correct data type. Here is a quick example table of the data types it can search for:

| Value Type | Example Value | Size (bytes) | Representation in Memory (Little-Endian) | Example Memory Address Range |
| --: | :-: | :-: | :-: | :-- |
| Byte | A door is open, with a boolean value of 1 | 1 | 01 | 0x0000 |
| 2-byte | 80 | 2 | 50 00 | 0x0001 - 0x0002 |
| 4-byte | Player health value of 100 | 4 | 64 00 00 00 | 0x0003 - 0x0006 |
| 8-byte | In-game score of 999,999,999,999 | 8 | FF 0F A5 D4 E8 00 00 00 | 0x0007 - 0x000E |
| Float | Movement speed value of 3.25 | 4 | 00 00 50 40 | 0x000F - 0x0012 |
| Double | Player position in the world of (50.0, -20.5, 10.25) | 8 | 00 00 00 00 00 00 49 40 | 0x0013 - 0x001A |
|  |  | 8 | 00 00 00 00 00 80 34 C0 | 0x001B - 0x0022 |
|  |  | 8 | 00 00 00 00 00 80 24 40 | 0x0023 - 0x002A |
| String | "Lord vader" | 10 bytes | 4C 6F 72 64 20 76 61 64 65 72 | 0x002B - 0x0034 |


# Scanning and Modifying Memory

* * *

As previously indicated, we will use Cheat Engine for the practical work in these modules. Be sure to have it set up on your machine or VM. These modules are also paired with a purpose-built game, `Hackman`. The first thing to do is run `Hackman.exe` and play the game a bit. Please become familiar with how the game plays and its various functionality.

![](https://academy.hackthebox.com/storage/modules/182/Hackman.png)

The basic process of scanning memory with Cheat Engine works as follows:

1. `Select the process` you want to scan from the list of available processes.

2. `Select the type of value` you want to search for (e.g. integer, float, double) and `enter the initial value` you want to scan for.


3. ` Start the initial scan` and wait for the results to appear. This may take some time, depending on the size of the memory and the number of available processes.

1. If the initial scan does not yield any results, perform subsequent scans by modifying the value and `repeating` the scan until the desired result is achieved.

2. Narrow the results by filtering the values based on specific criteria such as value range or type.

3. Once the desired address is located, modify the value to achieve the desired outcome.


First, open the `Hackman.exe` process in Cheat Engine by clicking the `Open Process` button and then locating the `Hackman.exe` process in the list.

![](https://academy.hackthebox.com/storage/modules/182/CE-OpenProcess.png)

We know there is no pause mechanism from playing the game a bit. This is a little tricky when scanning addresses because events can happen that will disrupt our searches. For example: being eaten by a Ghost while trying to find the lives value. Luckily, Cheat Engine has a handy ability to suspend (pause) a process. We can set up this hotkey by navigating to the `Edit Menu`, going to `Settings` and then opening the `Hotkeys` tab. Then set a hotkey for the " `Pause the selected process`" option. I use my keyboard's back quote/tilde key ( `~`). It's a key generally not used in games and is not out of the way to press.

![](https://academy.hackthebox.com/storage/modules/182/CE-HotkeyPause.png)

Let's start by looking at the number of Lives in Hackman. A new game begins with a total of 3 Lives. When the number of lives is below 3, collecting an orange cube will add an additional life. We can use the basic process above to scan Hackman's memory and locate the address that contains the Lives number.

Remember, you can now pause the game as needed using the hotkey that was just set.

Enter the `current value of lives` into Cheat Engine, and leave the scan options as an `Exact Value` and `4 Bytes`. Hit the `First Scan`, and Cheat Engine will scan for every memory address currently holding the value of `3` and display the results to the left.

![](https://academy.hackthebox.com/storage/modules/182/CE-LivesScan1.png)

Now get eaten by a ghost, and search for the `new value` as a `Next Scan` using the default options.

![](https://academy.hackthebox.com/storage/modules/182/CE-LivesScan2.png)

You can see that Cheat Engine has been able to filter nearly `58000 unrelated addresses` from the initial scan, as can be seen from the `Found: 1419` addresses number.

Playing the game a bit, without changing the value of the lives (currently being 2), we can see many addresses are changing, and the changing values are reflected with a red colour. We can `scan for 2` again in Cheat Engine to cut back even more unrelated addresses.

![](https://academy.hackthebox.com/storage/modules/182/CE-LivesScan3.png)

Down to `68 possible addresses`. You may have more or less the same, but the `exact number is unimportant`.

This time, let's increase our lives by collecting an orange cube and then scanning for a value of 3.

![](https://academy.hackthebox.com/storage/modules/182/CE-LivesScan4.png)

Down to only a handful of addresses. We can now add them to the Cheat Table by selecting them and then clicking the red arrow in the bottom right of the results list. A method I commonly use to determine which is the address I'm looking for is to `change each address` to an `incrementing staggering value`. For example, `10, 20 and 30`. This means that if the change is more significant than a single value (losing 2 lives instead of 1), we can still see which address is in the related range. Double-click on the Value column of each row and enter 10, 20 and 30. Then play the game, lose a life, and see what the value has changed too!

![](https://academy.hackthebox.com/storage/modules/182/CE-LivesModify1.png)

In my case, the 1st address was correct, and the other values pointed to something else in memory.

Reminder: the values that were changed that were NOT the actual lives value can cause instability in the game and lead to a crash.

Remember that these memory addresses you find via memory scanning may only be accurate for that game session. There are methods and techniques discussed later in this module and path that will help find more permanent solutions than refinding the addresses you are looking for every time you open the game.

## Anti-Scanning

Game developers can employ two straightforward methods to defend against Memory Scanning: `encrypting/obfuscating values` and conducting `tamper checks`. Encrypting critical data hinders cheaters from easily identifying and altering specific memory addresses. Although this approach doesn't render cheating impossible, it raises the difficulty of pinpointing accurate memory values, deterring numerous potential cheaters. Additionally, developers can establish `memory integrity checks` to verify that the game's memory remains untampered. These checks involve `computing checksums` or hash values for essential memory locations and `comparing them with expected values`. If any discrepancies emerge, the game can respond accordingly, such as displaying an error message, initiating a restart, or even applying in-game penalties.

`Address Space Layout Randomization` (ASLR) is a security technology, enabled by default on many operating systems, that `randomizes the memory addresses` where a program's code and data reside. As mentioned already, because the memory layout changes each time the game launches, cheaters face difficulty in reliably locating specific values or code segments, making memory scanning more challenging since addresses vary across game sessions.

Enable step-by-step solutions for all questions
![sparkles-icon-decoration](https://academy.hackthebox.com/images/sparkles-solid.svg)

#### Questions

Answer the question(s) below
to complete this Section and earn cubes!

Cheat Sheet

\+ 10  What is the text that is displayed in-game when the Lives counter holds a value greater than 3?


Submit


[Hackman.v1.4.0.zip](/storage/modules/182/Hackman.v1.4.0.zip)

\+ 10  Using the same memory searching techniques, what is the text that is displayed when you successfully modify the round counter and set it to a value over 9??


Submit


[Hackman.v1.4.0.zip](/storage/modules/182/Hackman.v1.4.0.zip)


# Data Structures

* * *

A data structure ( `struct`) is a way of `organising and storing data in a computer program`. A data structure defines the `relationships between individual data types` and provides a way to access and manipulate those elements. A structure is stored as a collection of its individual members (data types), where each member `is stored in a contiguous block of memory`. The memory layout of a structure is determined by the order in which its members are declared.

A game developer might use a data structure like a `GameStats` structure, to `efficiently organise` and manage various attributes of a game character or another game object. Combining different data types, such as integers, floating-point numbers, boolean values, etc., enables convenient storage and access to information like the character's name, health, speed, score, etc., all in a single object. This data structure improves code readability and maintainability and simplifies passing relevant data within the game's logic, ultimately contributing to a more structured and efficient game development process.

For example, consider the following C++ game structure definition:

```c++
struct GameStats {
    char name[32];
    int health;
    float speed;
    double score;
    int lives;
    bool isDead;
    struct Position {
        float x;
        float y;
        float z;
    } position;
};

struct GameStats player1Stats = {
    .name = "Player 1",
    .health = 75,
    .speed = 2.5f,
    .score = 1250.75,
    .lives = 5,
    .isDead = false,
    .position = { .x = 10.0f, .y = 20.0f, .z = 30.0f },
};

```

In this example, the `GameStats` structure contains the following members:

- `name`: A character array with 32 elements, used to store the player's name.

- `health`: An integer that stores the player's current health.

- `speed`: A floating-point number that stores the player's speed.

- `score`: A double-precision floating-point number that stores the player's score.

- `lives`: An integer storing the player's remaining lives.

- `isDead`: A Boolean value indicates whether the player is dead or alive.

- `position`: A nested `struct Position`, containing three floating-point numbers `x`, `y`, and `z`, used to store the player's position.


In the example above, a `gameStats` struct is initialised using a designated initialiser syntax with some sample values. The `player1Stats` variable contains the game's initial state with a player `name` of "Player 1", a health value of 75, a speed of 2.5, a score of 1250.75, 5 remaining lives, and the `isDead` flag set to `false`. Using the nested `position` struct, the player's position is specified as (10.0, 20.0, 30.0).

## Data Structures in Memory

In addressable memory, on a Windows computer, the struct layout would look something like this on a 32-bit system:

| Offset | Member | Type | Size (bytes) |
| --- | --- | --- | --- |
| 0 | name | char\[32\] | 32 |
| 32 | health | int | 4 |
| 36 | speed | float | 4 |
| 40 | score | double | 8 |
| 48 | lives | int | 4 |
| 52 | isDead | bool | 1 |
| 53 | padding | (unused) | 3 |
| 56 | position.x | float | 4 |
| 60 | position.y | float | 4 |
| 64 | position.z | float | 4 |
| **Total size** |  |  | **68** |

In this example, each `memory address` represents `an offset` in memory where a specific data member is stored. The values stored at these memory addresses correspond to the initial values provided for the `player1Stats` instance in the example code. The struct members are stored in the order declared in the struct definition.

The `name` member is a character array of size 32, which starts at offset 0. The `health` member is an integer of size 4 bytes, which starts at offset 32. The `speed` member is a floating-point number of size 4 bytes, which starts at offset 36. The `score` member is a double-precision floating-point number of size 8 bytes, which starts at offset 40. The `lives` member is an integer of size 4 bytes, which starts at offset 48. The `isDead` member is a boolean value of size 1 byte, which starts at offset 52. There are 3 bytes of padding after `isDead` to align the next member on a 4-byte boundary.

The `position` member is a struct with three floating-point members: `x`, `y`, and `z`, each of size 4 bytes. These members start at offsets 56, 60, and 64, respectively. The total size of the structure is `68 bytes`.

Memory doesn't necessarily have to be `evenly divisible by 4`. However, it is a common requirement for many computer architectures and operating systems. This requirement comes from the fact that modern computer processors typically work with data in 32-bit or 64-bit chunks. These chunks are called " `words`" and are `typically 4 or 8 bytes in size`, respectively.

When a computer reads or writes to memory, it typically does so in units of these words. For example, if you ask a computer to read 1 byte of data from memory, it will read 4 bytes (an entire 32-bit word) and then extract the single byte you requested.

To ensure that each word in memory is aligned with the appropriate address boundary, `the memory addresses themselves must be divisible by the size of a word`. That means that on a `32-bit system`, memory addresses should `be evenly divisible by 4` (since each `word` is 4 bytes), to make them `4-byte aligned`, while on a `64-bit system`, they should be `evenly divisible by 8` (since each `word` is 8 bytes), to make them `8-byte aligned`.

By adding these padding bytes, the compiler can ensure that the struct is stored in memory in a way that maximises performance and minimises memory access issues and crashes.

If we were to observe that data in the Cheat Engine memory viewer, it would look something very similar to this:

```
Offset:   00 01 02 03 04 05 06 07  08 09 0A 0B 0C 0D 0E 0F
------------------------------------------------------------
00000000  50 6C 61 79 65 72 20 31  00 00 00 00 00 00 00 00  Player 1........
00000010  00 00 00 00 4B 02 00 00  E2 40 79 12 83 C0 F5 40  ....K....@y....@
00000020  05 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
00000030  0A 00 00 00 14 00 00 00  1E 00 00 00 00 00 00 00  ................
00000040  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
00000050  00 00 00 00 00 00 00 00                           ........

```

In this example, each line represents a 16-byte block of memory. The values stored at each offset correspond to the initial values provided for the `player1Stats` instance in the example code.

## Offsets

In computer science, an offset represents the difference between the starting address of a data structure and a particular location within the structure. The offset is typically measured in bytes and represented in base-16.

A quick reminder about \`base 16\`: a base is a mathematical system that defines how to count or represent numbers. In the decimal system (base 10), we use ten digits from 0 to 9 to represent numbers. In the same way, the hexadecimal (base 16) system uses 16 digits, which are \`0 to 9\`, and \`A to F\`.

In hexadecimal, each digit's value is determined by its number position and corresponding `power of 16`. The rightmost digit represents the `16^0` (16 to the power of 0) position, the next digit to the left represents the `16^1` (16 to the power of 1) position, the next digit represents the `16^2` (16 to the power of 2) position, and so on.

In the above case, the address `00000010 in base 16 is the decimal number 16 in base 10`

If we use the previous examples, `0x00000000` is our base structure address which holds our health value, and `0x00000024` is the address which has our speed. We can reference that speed value in the code by applying an offset from our base address rather than an absolute address to `0x00000024`.

```c++
int main() {
    struct GameStats player1Stats = {
        .name = "Player 1",
        .health = 75,
        .speed = 2.5f,
        .score = 1250.75,
        .lives = 5,
        .isDead = false,
        .position = { .x = 10.0f, .y = 20.0f, .z = 30.0f },
    };

  	// get the base address of the gameStats struct from memory
    uint8_t* baseAddress = (uint8_t*)&player1Stats;

    // Get the address of the `speed` member using a byte offset from the base address
    // C pointer arithmetic uses base 10, so convert the hex offset of 0x24
    // to a decimal value of 36
    float* speedPtr = (float*)(baseAddress + 36);

    // Get the address of the `score` member using a byte offset from the base address
    double* scorePtr = (double*)(baseAddress + 40);

    // Print the values of `speed` and `score`
    printf("speed = %f\n", *speedPtr);
    printf("score = %f\n", *scorePtr);

    return 0;
}

```

`Offsets` are commonly used in low-level programming, such as assembly language or C, to access specific elements within a data structure. For example, C can use an offset to access a particular member within an array or structure. The offset value is added to the base address of the array or structure to determine the memory location of the desired element.

In addition, `offsets are often used in memory exploitation techniques`, such as buffer overflow attacks, to overwrite memory values beyond the intended bounds of a buffer. By calculating the correct offset value, an attacker can overwrite memory values with their own data, potentially allowing them to execute malicious code or gain control of the system.

Now think about this: the health value address is likely straightforward to locate via memory scanning. Once we have that address, we can explore the memory, as above, and via a lot of trial and error, establish what the surrounding bytes are, eventually reverse engineering a structure similar to this:

| Offset | Value | Description |
| --- | --- | --- |
| 00000000: | 50 6C 61 79 65 72 20 31 00 00 00 | name = "Player 1" |
| 0000000B: | 00 00 00 00 | padding bytes |
| 00000010: | 4B 00 00 00 | health = 75 |
| 00000014: | 00 40 28 5C | speed = 2.5f |
| 00000018: | 8F C2 F5 48 05 00 00 00 | score = 1250.75 |
| 00000020: | 00 00 00 00 | lives = 0 (and padding bytes) |
| 00000024: | 0A 14 AE 41 | position.x = 10.0f |
| 00000028: | 00 00 46 42 | position.y = 20.0f |
| 0000002C: | 00 00 54 42 | position.z = 30.0f |

We will disassemble a structure in the next section.


# Identify and Dissect Data Structures

* * *

Identifying data structures can be a great way to find data in a game that is potentially harder to scan for.

Cheat Engine provides a few different ways to assist in the dissection of potential data structures, but it is by no means a simple or straightforward process.

Observing a known memory address in the Cheat Engine Memory Viewer is a highly effective method for identifying related variables stored closely in memory or locating a potential data structure. By keeping an eye on values that change and appear in red, the Memory Viewer makes it easy to identify values near the one we are monitoring.

In Cheat Engine, right-click the address for the Lives value you have previously found (or find it again), and click `Browse Memory Regions.`

![](https://academy.hackthebox.com/storage/modules/182/CE-TableBrowseMemoryRegion.png)

This will open the Cheat Engine Memory Viewer to that address in memory, in this case, `05620FC4`.

![](https://academy.hackthebox.com/storage/modules/182/CE-StructureMemoryViewer.png)

As we know, `09` converted to decimal is `09`, which is the number of Lives I currently have in-game. Scroll up the hex editor a little, play the game, and observe how data around the Lives value changes. Bytes that have recently changed are briefly highlighted in red.

![](https://academy.hackthebox.com/storage/modules/182/CE-MemoryViewerRecentlyChanged.png)

Cheat Engine allows the display format to be changed for better visibility. Right-click in the Memory Viewer, and change the display type to `4 bytes decimal`; as we know, the type of the Lives value is 4 Bytes.

![](https://academy.hackthebox.com/storage/modules/182/CE-MemoryViewerDisplayType.png)

With the `4 Byte decimal` display, we can see the current value of the Lives counter clearly, and we can also see the round counter in the value immediately proceeding the lives value, but observing the other values around doesn't reveal anything that can be easily correlated to values we know about in-game.

![](https://academy.hackthebox.com/storage/modules/182/CE-MemoryViewer4ByteView.png)

Changing the display type to `Float` reveal some interesting numbers, however.

![](https://academy.hackthebox.com/storage/modules/182/CE-MemoryViewerFloat.png)

The current score in-game is `500`, and 2 float values look very similar, with values of `5000` and `50`. Suspiciously similar to the score counter.

Other values still don't make much sense, and changing display types backwards and forwards between the various options is pointless.

Cheat Engine has a powerful tool to help break down all that data called the `Data/Structure dissector`. The `Data/Structure dissector` is a feature in the Cheat Engine software tool that allows users to `dissect and analyse complex data structures in memory`. It provides a way to view a program's memory as a series of interconnected data structures rather than just a raw sequence of bytes by automatically guessing the correct types for the series of data specified.

Change the Memory Viewer's Display Type back to `Byte Hex`, and scroll up a little, looking for what could be the start of the data structure we want to analyse.

![](https://academy.hackthebox.com/storage/modules/182/CE-MemoryViewerStartOfStructure.png)

Looking at the raw bytes, we see lots of padding bytes ( `00`) which are nothing, and then we have the start of data at the address of `05620F80`. If you select a byte in the memory viewer, it will calculate the address + offset for you and display it in the bottom left of the viewer. In the above image, I have selected the padding bytes before the address above to make it clearer. Although all the bytes may be false boolean values, we rely on our informed judgement to deduce where the data structure begins.

Next, click the `Dissect Data/Structures` option from the Tools menu, and the `Structure dissect` window will open. By default, the address it will open to will be the first address currently viewed in the Memory Viewer.

Enter the address where the structure possibly starts in the box under `Group 1`, then from the `Structures` menu, select the `Define new structure` option. This will pop open a small window prompting for a structure name and some other information.

![](https://academy.hackthebox.com/storage/modules/182/CE-StructureDissectorPrompt.png)

Name the structure anything, or leave it as 'unnamed' and click ok.

![](https://academy.hackthebox.com/storage/modules/182/CE-StructureDissectorNewStructure.png)

We can now see a hierarchical tree view of all the data from that address in memory. Cheat Engine has done its best to guess the types of data stored in each address, and we can see there are a few different types. Pointers, 4 Byte values, Floats and Doubles. Cheat Engine has done its best to guess the correct data types, but we can immediately see that it has `incorrectly identified` the Lives value of 8 as a pointer. Scroll down until you find the Lives row, double-click to edit it, set the description to `Lives` and change the Type to `4 Bytes`. Naming things is very important as we go, as it helps us better understand the structure and keep track of our values. Rename other known addresses as well.

![](https://academy.hackthebox.com/storage/modules/182/CE-StructureDissectorRenameRow.png)

Enable step-by-step solutions for all questions
![sparkles-icon-decoration](https://academy.hackthebox.com/images/sparkles-solid.svg)

#### Questions

Answer the question(s) below
to complete this Section and earn cubes!

Cheat Sheet

\+ 10  What is the text displayed in-game when you successfully modify the score value over 100'000'000?


Submit


[Hackman.v1.4.0.zip](/storage/modules/182/Hackman.v1.4.0.zip)

Hint


\+ 10  There is another value that can be located via the structure dissector, that if modified to a value over 200'000'000 will display text in-game, what is that text?


Submit


[Hackman.v1.4.0.zip](/storage/modules/182/Hackman.v1.4.0.zip)


# Debugging

* * *

The Cheat Sheet from the x86 Assembly module will be invaluable as a reference for this section.

Debugging is the process of `identifying and resolving issues or bugs` in a software application, program, or system. It is essential in software development and maintenance to ensure that the application or system operates as expected and meets the user's requirements.

During the debugging process, developers use various tools and techniques to identify and isolate the source of the problem. This may involve reviewing the source code, examining logs or error messages, and executing the code in a test environment. Once the issue has been identified, developers can implement a fix or solution to resolve the problem. Developers will `use a debugger` software program to carry out these tasks.

A debugger is a software tool developers use to identify and resolve issues or bugs in software applications, programs, or systems. A debugger allows developers to examine and manipulate the execution of the code, usually at a low level, to identify the root cause of a problem.

Debuggers typically provide various features, such as `breakpoints`, `step-by-step execution`, and `variable inspection`, to help developers analyse the code's behaviour and understand the problem's source. They also allow developers to `modify the code at runtime`, such as changing the values of variables or memory locations, to see how the application responds. Debuggers can be integrated into development environments, such as Integrated Development Environments (IDEs such as IntelliJ), or run as standalone applications (such as x64dbg).

A `breakpoint` is a mechanism that allows a developer to `pause the execution of a program` or application at a `specific point in the code`. When the program reaches the breakpoint, it triggers an `interrupt`. An interrupt is a mechanism used to pause the execution and allow the user to examine and modify the runtime. When an interrupt occurs, the CPU stops executing the current program and saves its current state, including the contents of the `program counter`, `registers`, and other important data, onto a special area of memory called the `interrupt stack` or `system stack`.

An `interrupt stack`, also known as a `system stack` or `kernel stack`, is a `separate area of memory` used by a computer system to temporarily store the state of a program when an interrupt occurs. When an interrupt is triggered, the CPU saves the current state of the program, including the values of the program counter, registers, and other processor state information, onto the interrupt stack. This allows the CPU to switch to the interrupt handler and handle the interrupt while preserving the state of the interrupted program.

A `stack trace` is a report of the call stack for a running program or process. The call stack is a data structure computer programs use to manage function calls and returns and keep track of the program's current state.

A `stack trace` typically shows the list of function calls made up to the point where the stack trace was generated, along with the associated memory addresses and other metadata. Each entry in the stack trace represents a function call and includes information such as the function's name, the module or library it belongs to, and the memory address where the function is located.

```
Address    Function
-----------------------------------------
0048D27B  Game::Update()
0047F0FA  Game::Render()
004011E5  WinMain()
00401259  __tmainCRTStartup()
004012E5  WinMainCRTStartup()
7736643D  BaseThreadInitThunk()
77D13F72  RtlInitializeExceptionChain()
77D13F45  RtlInitializeExceptionChain()

```

This example stack trace shows the call stack for a game, indicating the sequence of function calls that led to the current point in the program. Each line represents a function call, with the most recent call at the top of the stack and the original call at the bottom. In this example, the top of the call stack is the function `Game::Update()`, which was called by the function `Game::Render()`. These functions were called by the `WinMain()` function, which in turn was called by the startup code for the program.

## Cheat Engine Debugger

The Cheat Engine debugger is a component of the Cheat Engine software that allows users to debug the game's memory and identify specific data locations, such as health, ammo, or money. It provides features such as breakpoints and assembly-level inspection to help users analyse the game's code and understand how it works. The Cheat Engine debugger allows users to set various breakpoints like line, conditional, software and hardware.

- `Line breakpoints` pause the game's execution at a specific line of code, allowing the user to examine the game's state. For example, a line breakpoint could be set at the point in the game code where the player's health is checked, allowing the health value to be overwritten with any value.

- `Conditional breakpoints` pause the game's execution when a particular condition is met, such as a variable's value.

- A `software breakpoint` is a type of breakpoint that is triggered by `modifying the program code itself`. When a software breakpoint is set, the program code is modified to include a special interrupt instruction, such as `INT 3`, which signals the processor to interrupt the program execution and transfer control to the debugger. The debugger then takes control and allows the user to examine the program state and variables.

- A `hardware breakpoint` is a type of breakpoint triggered by the `processor hardware`. When a hardware breakpoint is set, the processor sets a special register to monitor a specific memory location or instruction address. When the monitored location or address is accessed, the processor interrupts the program execution and transfers control to the debugger. Hardware breakpoints can be more efficient than software breakpoints, as they do not require modifying the program code, but the number of available hardware registers may limit them.


Once the game's execution is paused, Cheat Engine takes control, allowing the user to examine the game's state, variables, and call stack. The user can inspect the game's assembly code, view the call stack, and modify the values of registers and memory locations to analyse the code's behaviour. The user can then use this information to identify and modify game features, such as health or ammunition, or to create game mods or cheats.


# Find what accesses an address

* * *

The " `Find what accesses this address`" function in Cheat Engine is a feature that allows users to identify code that accesses a specific memory address. This feature can help analyse a game's behaviour and understand how it reads and uses data.

This function `attaches the Cheat Engine debugger` to the game process and is accessed by right-clicking an address in the Cheat Table and selecting the option. In this instance, right-click the known Lives counter address, or find the address again and then right-click it.

![](https://academy.hackthebox.com/storage/modules/182/CE-DebugFindWhatAccesses.png)

When you select the option, you will get a prompt confirming if you want to attach the Cheat Engine debugger to the process, select `yes`, and a new window will pop up.

![](https://academy.hackthebox.com/storage/modules/182/CE-OpcodeAccessed.png)

This window will list all instructions in the game that access that memory location. Different functions will perform various tasks. For example: While playing the game, a function might reference that variable in memory to update the display value. When a ghost eats a player, that function might check how many lives are left by accessing the variable. Play the game and see how different interactions will log different access instructions in the OpCode window.

![](https://academy.hackthebox.com/storage/modules/182/CE-OpcodeAccessedResults.png)

In the above instance, I played the game for around 5 seconds. I have been eaten by a ghost twice in that time. The `count column` provides valuable information, reflecting `how often the instruction has been triggered`. Four different instructions were triggered when the ghost ate my character. The count is also showing us that there is a function that frequently runs (1703 calls in ~10 seconds) that compares a value sitting in `ecx+44` to `5` and then a function that runs more infrequently that compares a value in `esi+44` to `0`.

After playing the game some more, there are some additional observations to make a note of.

![](https://academy.hackthebox.com/storage/modules/182/CE-OpcodeAccessedResults2.png)

The 2nd instruction that compares `esi+44` to 0 is triggered every time a movement input to the game is made, valid or not, so it's likely a keypress event handler or something similar.

Look at the first `mov` instruction in that list—a quick reminder about the `mov` instruction.

In the x86 assembly language, the `mov` instruction moves data between registers and memory locations. The instruction `mov eax, [ebx+44]` moves the value stored in memory at the address `[ebx+44]` into the `eax` register. Here's how it works:

- The instruction starts with the `mov` opcode, which tells the processor to move data from a memory location to a register.

- The `eax` register is specified as the destination operand of the instruction. This means the data will be moved from memory into the `eax` register.

- The memory address to be read is specified using the `[ebx+44]` expression. This expression calculates the memory address as the sum of the value stored in the `ebx` register and the constant value `68`.

- The square brackets around `[ebx+44]` indicate that the value should be read from the memory location specified by the expression, rather than from a register or an immediate value.


So, the instruction `mov eax, [ebx+44]` reads a 32-bit value from memory at the address specified by `[ebx+44]` and moves it into the `eax` register.

Select that row and click the `Show disassembler` button. This will open the memory viewer and navigate the disassembler to the address of the instruction.

![](https://academy.hackthebox.com/storage/modules/182/CE-ReadMemoryViewer.png)

Something very obvious in the opcodes is immediately after copying the value in `[ebx+44]` into eax, eax is decreased by 1 using the `dec eax` opcode. We know that we lose a life when the ghosts eat our character. Cheat Engine has a function to quickly replace instructions with NOPs, or no operations, instructions that do nothing but have the same byte size as what is being replaced. Right-click on the `dec eax` instruction, and click the `Replace with code that does nothing` option in the menu.

![](https://academy.hackthebox.com/storage/modules/182/CE-ReadMemoryViewerReplaceMenu.png)

This will prompt you for a name; leave it as default and click ok. You will see the instruction has been replaced with `nop`. The `dec` instruction is only a single byte long, so there will be a single `nop`.

![](https://academy.hackthebox.com/storage/modules/182/CE-MemoryViewerNOP.png)

Return to the game and observe any behaviour that has now changed with the patch just performed. When a ghost now eats the player, the Lives counter is no longer decreased.

![](https://academy.hackthebox.com/storage/modules/182/Dec-NOP.gif)

Cheat Engine will record the original instruction in the Code list accessed via the `Advanced Options` button at the bottom of the Cheat Table. You can open that window, right-click on the entry for the replaced code and select `Restore with original code` to revert the change at any time. The `Replace all` option will NOP the instruction again.

![](https://academy.hackthebox.com/storage/modules/182/CE-CodeList.png)


# Find what writes to address

* * *

The " `Find what writes to this address`" function in Cheat Engine is a feature, not unlike the ' `Find what accesses...`' function, that allows users to identify the code that writes to a specific memory address in a game or application.

As with the ' `Find what accesses...`' function, this function attaches the Cheat Engine debugger to the game, and when something writes to the specified address, Cheat Engine will log the instruction call in the Opcode list.

With the Live's memory address known, right-click the entry in the Cheat Table, and click the option " `Find what writes to this address`".

The same window from using the ' `Find what reads...`' function will pop up and perform the same functionality. When instructions in the game `modify the Lives value` in memory, it will `record the instructions`. Return to the game and observe how various functions interact with that value.

![](https://academy.hackthebox.com/storage/modules/182/CE-OpcodeWrite.png)

When a ghost eats the player and a 'life cube' is collected to add an additional life, the same instruction is triggered: `mov [edi+44], eax`. This opcode moves the contents of the `eax` register into the memory location stored in `edi` plus an offset of 44 bytes. Open `the disassembler`, right-click the instruction and `toggle a breakpoint` on the row. This will highlight the entire row in red.

![](https://academy.hackthebox.com/storage/modules/182/CE-MemoryViewerToggleBreakpoint.png)

Return to the game and get eaten by a ghost to lose a life. The breakpoint will trigger, and the Memory Viewer will change to more of a debugger view.

![](https://academy.hackthebox.com/storage/modules/182/CE-Debugger.png)

A new bar contains a few buttons to interact with the disassembled game code, providing functionality such as stepping through code or resuming execution.

1. `Run`: Resume execution.

2. `Step Into`: This option steps into a function call, allowing you to trace the execution of the called function and inspect its behaviour.

3. `Step Over`: This option steps over a function call, allowing you to skip the details of the called function and continue to the next instruction in the current function.

4. `Step Out`: This option steps out of the current function and returns to the calling function, allowing you to continue debugging from that point.

5. `Run till`: This option will resume execution until the game reaches whatever code you have selected in the memory viewer. It's a quick way of executing and observing multiple instructions without setting and unsetting breakpoints.


To the memory viewer's right is a `list of current register and flag states`, and below that is a `stack trace` to the right of the hex editor.

The instruction is moving `eax ` into the value of `edi+44`, and we can currently see that `eax` holds the value of 7, the new current number of Lives in-game. Click the `EAX` register in the register list, and a prompt will open asking for a new value. `Remember that the number you enter must be in hexadecimal format, not decimal. ` Enter a new value, such as 9, and click ok, then click the `Run` button to resume the game. You can immediately observe the Lives counter change to the input value. We just told the game to set the counter value to the value we specified instead of modifying the value in memory.

Right-click the instruction and `Replace with code that does nothing` to `nop` it out. Then get eaten by a ghost in game, and you will observe that the value does not change.

Like how we modified the game in the previous section, where we `nop`'d the function that was decreasing the lives counter, this time, we have `nop`'d the function that modifies the counter in any way (losing or gaining).
Two different approaches to achieving the same end goal: "unlimited lives".

However, what if we want to set that counter to a specific value, as we did by modifying the `eax` register? Unfortunately, it's much more complicated than it sounds because the `mov [edi+44], eax` opcode is only 3 bytes long. An integer is 4 bytes, so if we were to change the instruction to be `mov [edi+44], 09`, for instance, the program would crash because 3 bytes are suddenly 7, which has now overwritten parts of the next instruction, `mov ecx,[7A5BCD4C]`.
Try it yourself. Cheat Engine will prompt you to overwrite the incomplete opcodes with `nop`'s. Try either option and observe what happens.

The following section will cover some very clever methods of tackling this issue.


# Replacing functionality

* * *

Cheat Engine has a powerful scripting feature that enables using a purpose build language called Auto Assembler. It allows the creation of more persistent cheats that can be used across multiple game sessions and potentially even game versions. You must first identify the code you want to replace to utilise the functionality. This is most easily done using the techniques shown in the previous two topics.

There is a quirk with Unity games and auto assembler. The script crafted for this topic might not persist across game instances; however, it still serves to teach the concepts. The next module will cover more advanced persistence techniques.

Find the function writing to the Lives counter in-game. Once the instructions have been found, click the `Show disassembler` button, and it will open the Memory Viewer to that specific instruction.

![](https://academy.hackthebox.com/storage/modules/182/CE-MemoryViewerWrite.png)

Expand the `Tools` menu with that instruction highlighted, and select the `Auto Assemble` option.

![](https://academy.hackthebox.com/storage/modules/182/CE-ToolsAA.png)

An empty `Auto assemble` window will open, presenting a blank script editor.

The Auto Assembler provides several template options accessible via the `Template` menu. The important choices to know are:

- Code Injection: A simple template that allocates new memory, replaces the existing instruction with a jump to the new memory, the new instructions are created in the new memory, and the original instructions are added at the end.

- API Hook: A template to hook a known API function and replace its original address with a new address.

- Code Relocation: As the name suggests, this template will relocate all code between a starting and ending address to the newly allocated memory.

- Call CE LUA Function: A template showing how to use Cheat Engine's LUA scripting capabilities.

- AOB Injections: A template that includes a function that will try to create a signature to match a series of unique bytes that can be used to identify the specified instructions in memory and then create a code injection template around that signature. AOB scanning is a valuable technique that can make scripts function across multiple game versions. This template will include framework code.

- Full Injection: A template that expands on the functionality provided in the basic `Code Injection` template. This template will include framework code.

- Cheat Table Framework Code: This template will simply add an `[Enable]` and `[Disable]` headers to the script. These two headers make it possible to embed the script into the Cheat Table, so it can be toggled and shared as needed.


All of these templates implement what is known as a trampoline. In Game hacking, a trampoline is a technique used to redirect the execution of a program to a new location in memory. The technique involves overwriting a portion of the original program code with a small piece of code that performs a jump to a new location called the trampoline. The trampoline then performs its own set of instructions before redirecting the program execution back to the original program code.

For this example, we will use the Code Injection template, but since we want it to be added to the Cheat Table, we need first to use the `Cheat Table Framework Code template` to add the two headers, so select that first, and then select the `Code Injection` template option, and then the `Code Injection` option.

![](https://academy.hackthebox.com/storage/modules/182/CE-AATemplate.png)

The `Code Injection` option will prompt you for an address to jump off. It will automatically fill the address of the instruction that is selected in the disassembler. Click ok and it will generate an injection script.

![](https://academy.hackthebox.com/storage/modules/182/CE-AAJump.png)

```nasm
[ENABLE]
//code from here to '[DISABLE]' will be used to enable the cheat
alloc(newmem,2048)
label(returnhere)
label(originalcode)
label(exit)

```

This script section is executed when the user enables the script toggle in the Cheat Table. It allocates 2048 bytes of memory for storing the cheat code and creates labels for the return address, the original code to be replaced, and the exit point of the cheat code.

Labels in Auto Assembler scripts serve as markers for specific memory locations or code sections that other parts of the script can refer to without knowing exact memory addresses.

```nasm
newmem: //this is allocated memory, you have read,write,execute access
//place your code here

originalcode:
mov [edi+44],eax
mov ecx,[GameAssembly.a_t29C8EEC69DC3C091A3C43F890F56F5B169183B33_il2cpp_TypeInfo_var]

exit:
jmp returnhere

```

The code block labelled `newmem` is where you can insert your assembly instructions. In this case, the code replaces the original instructions at the memory address `"GameAssembly.dll"+1D322C`, which is a location in the game's code where the instructions `mov [edi+70], eax` and `mov ecx, [GameAssembly.dll+89B728]` are located.

The cheat returns to the original address using the `jmp returnhere` instruction.

```nasm
"GameAssembly.dll"+1D322C:
jmp newmem
nop 4
returnhere:

```

This code block is the 'trampoline' created from the address `"GameAssembly.dll"+1D322C`. The Auto Assembler will replace the instruction at that address with a jump to whatever the address of `newmem` is. The `nop 4` is padding automatically inserted by the assembler to remove any other instructions that Cheat Engine determines.

`returnhere` is a label used to jump over the above injection, so it is not referenced in the `newmem` code.

```nasm
[DISABLE]
//code from here till the end of the code will be used to disable the cheat
dealloc(newmem)
"GameAssembly.dll"+1D322C:
db 89 47 44 8B 0D 4C CD 5B 7A
//mov [edi+44],eax
//mov ecx,[GameAssembly.a_t29C8EEC69DC3C091A3C43F890F56F5B169183B33_il2cpp_TypeInfo_var]

```

This script section is executed when the user disables the script toggle in the Cheat Table. It deallocates the memory allocated for the cheat code and replaces the modified instructions with the original instructions using the `db` command. In this case, it replaces the modified instructions with the original instructions `mov [edi+70],eax` and `mov ecx,[GameAssembly.dll+89B728]`.

The `db` command stands for "define byte" and can be used to define one or more bytes of data, separated by spaces. In this case, the `db` command defines a sequence of nine bytes (separated by spaces) that correspond to the original instructions modified by the cheat code. When executed, the `db` command overwrites the modified instructions with the original instructions, effectively disabling the cheat.

The full script is as follows:

```nasm
[ENABLE]
//code from here to '[DISABLE]' will be used to enable the cheat
alloc(newmem,2048)
label(returnhere)
label(originalcode)
label(exit)

newmem: //this is allocated memory, you have read,write,execute access
//place your code here

originalcode:
mov [edi+44],eax
mov ecx,[GameAssembly.a_t29C8EEC69DC3C091A3C43F890F56F5B169183B33_il2cpp_TypeInfo_var]

exit:
jmp returnhere

"GameAssembly.dll"+20A5DC:
jmp newmem
nop 4
returnhere:

[DISABLE]
//code from here till the end of the code will be used to disable the cheat
dealloc(newmem)
"GameAssembly.dll"+20A5DC:
db 89 47 44 8B 0D 4C CD 5B 7A
//mov [edi+44],eax
//mov ecx,[GameAssembly.a_t29C8EEC69DC3C091A3C43F890F56F5B169183B33_il2cpp_TypeInfo_var]

```

The objective of this script is to give Unlimited Lives. We know that the `eax` register contains the value of Lives to be written to the lives address. So we can rewrite `eax` with our value so that whenever the ghost eats the player character, the value of lives will be set to that value, effectively giving Unlimited Lives.

To do this, add a `mov` instruction to the `newmem` block. In the below example, I have opted to write the value of 9 to the `eax` register.

```nasm
[ENABLE]
//code from here to '[DISABLE]' will be used to enable the cheat
alloc(newmem,2048)
label(returnhere)
label(originalcode)
label(exit)

newmem: //this is allocated memory, you have read,write,execute access
mov eax, 09

originalcode:
mov [edi+44],eax
mov ecx,[GameAssembly.a_t29C8EEC69DC3C091A3C43F890F56F5B169183B33_il2cpp_TypeInfo_var]

exit:
jmp returnhere

"GameAssembly.dll"+20A5DC:
jmp newmem
nop 4
returnhere:

[DISABLE]
//code from here till the end of the code will be used to disable the cheat
dealloc(newmem)
"GameAssembly.dll"+20A5DC:
db 89 47 44 8B 0D 4C CD 5B 7A
//mov [edi+44],eax
//mov ecx,[GameAssembly.a_t29C8EEC69DC3C091A3C43F890F56F5B169183B33_il2cpp_TypeInfo_var]

```

Next, select the `Assign to current cheat table` option from the `File` menu. This will embed the script into the Cheat Table.

![](https://academy.hackthebox.com/storage/modules/182/CE-AAAssignToTable.png)

Enable the script in the table, and we can observe that the original instruction has been replaced with a `jmp` to an allocated memory address in the memory viewer. Playing the game, we can see that no matter how many times we die, the Lives counter is always at 9.

![](https://academy.hackthebox.com/storage/modules/182/CE-TableScript.png)

If we right-click and `Follow` the instruction, we can see the new instruction in memory, `mov eax, 0000009,` and the original game code that then moved eax into the pointer at `edi+70` and returned to the original code at the end.

![](https://academy.hackthebox.com/storage/modules/182/CE-MemoryViewerInjected.png)

## Anti-Injection

`Code obfuscation` is a method that makes game code harder to comprehend, analyse, and reverse-engineer, posing challenges for cheaters in pinpointing code sections tied to different game mechanics. As an outcome, creating cheats becomes more difficult. Tools such as ProGuard, Dotfuscator, and LLVM's obfuscator are helpful for code obfuscation and help combat code injection.

Another technique that can be used is `runtime integrity checks`, which can `identify code injections as they happen`. These checks involve monitoring the game's memory and verifying the code remains unaltered. These checks can be executed at random intervals, using a "heartbeat", or during specific events. However, since this method demands significant resources, it can significantly impact game performance, and developers must balance security and performance.

There are new technologies that utilise `machine learning algorithms` to `detect unusual patterns` or `behaviour` that can bolster runtime integrity checks and enhance cheat detection capabilities that can be implemented to combat code injection.


## Game Hacking Fundamentals - Skills Assessment

* * *

Using what you have learnt, attempt to modify the Lives counter to a value greater than 5 and the HiddenScore counter you previously encountered to a value greater than 200'000'000.

Enable step-by-step solutions for all questions
![sparkles-icon-decoration](https://academy.hackthebox.com/images/sparkles-solid.svg)

#### Questions

Answer the question(s) below
to complete this Section and earn cubes!

Cheat Sheet

\+ 20  What flag is displayed when you successfully modify the Lives counter to a value greater than 5?


Submit


[Hackman.Assessment.v1.5.1.zip](/storage/modules/182/Hackman.Assessment.v1.5.1.zip)

\+ 40  What flag is displayed when you successfully modify the HiddenScore counter to a value greater than 200'000'000?


Submit


[Hackman.Assessment.v1.5.1.zip](/storage/modules/182/Hackman.Assessment.v1.5.1.zip)

Hint


