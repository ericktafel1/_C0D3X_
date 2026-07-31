# Introduction

* * *

The `Game Hacking fundamentals` module introduced fundamental game-hacking concepts, such as understanding and manipulating memory. It ended with introducing some basic code injection concepts and techniques.

In this module, you will delve deeper into the world of game hacking and explore more advanced tools and techniques to manipulate games. Building on the fundamental concepts covered in the previous module, you will gain a deeper understanding of game internals and learn how to leverage that knowledge for more complex objectives.

We will examine `Arrays of Bytes` ( `AoBs`) and their role in game hacking. We will also explore scripting AoBs in Cheat Engine and look at different commercial game engines such as `Unity`, `Unreal Engine`, and `Godot`. Next, we will delve into Unity's IL2CPP and understand how it works and impacts game security.

Obfuscation is a crucial aspect of software security and is used extensively so we will explore different obfuscation techniques, such as name obfuscation, string encryption, and control flow obfuscation.

Next, we will introduce you to DnSpy, a powerful tool for analysing and modifying dotnet binaries. We will reverse a game to modify it to change the game environment.

We will briefly examine external and internal game hacks, exploring their differences, various applications and approaches. We will explore software libraries, understanding binaries, and dynamic link libraries (DLLs).

C# Events and attributes play an important role in understanding unity game hacking so we will explore delegates, events, and attributes.

Next, we will explore game modifications, their history, types, and the various approaches to creating mods. We will also introduce you to runtime hook libraries like BepInEx and their application in game hacking and then implement a library to inject into a game to alter the game.

Game networking is another aspect we will explore, including the fundamentals of game networking, peer-to-peer vs client-server models, latency, prediction and interpolation, handling packet loss, matchmaking, scalability, and network security.

We will also discuss man-in-the-middle (MITM) attacks, their execution, and mitigation techniques in general and within the gaming context. Finally, we will explore man-in-the-middle game hacking, including setting up, analysing, and tampering with a game’s HTTP calls.


# Array of Bytes

* * *

Let's kick off right where we left off in the previous module ( [Game Hacking Fundamentals](https://academy.hackthebox.com/module/details/182)). In the last module, we used Cheat Engine to locate the function altering the Lives counter in the game. We then created a code injection script to overwrite the structure pointer value representing lives before the value is set.

Here is the final script from that module

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

Although the script worked perfectly, it had a limitation - it failed to inject when a new instance of Hackman was opened. This failure usually occurs due to changes in the memory layout with each new start, or if the structure is updated. For instance, `edi+44` may no longer point to the Lives counter if the developer adds a new member to the struct, so it becomes `edi+53`.

We can use Array of Bytes (AoB) scanning to ensure our script works across different game instances until the game gets updated.

## What is an AoB

An `Array of Bytes (AoB)` is a contiguous block of memory where each element stores a byte of data.

In computing, a byte is a unit of digital information traditionally composed of 8 bits, and it can represent a wide range of data types such as integers, characters, and more. In languages like C, C++, or Java, you can declare an array of bytes, often represented by data types like `byte` (Java) or `uint8_t` (C/C++), to store sequences of these bytes.

```c
#include <stdint.h>  // for uint8_t

int main() {
    uint8_t myArray[5] = {0x41, 0x42, 0x43, 0x44, 0x45};  // 'A', 'B', 'C', 'D', 'E' in ASCII
    // Do something with byteArray
    return 0;
}

```

These arrays can be useful for tasks such as buffering data, network communication, or file manipulation.

The way arrays of bytes work is based on the fundamental architecture of modern computers. When an array is declared, the operating system allocates a contiguous block of memory, the size of which is determined by the length of the array multiplied by the size of a single byte.

Each element in the array can be accessed using an index, starting from zero. So, if you have an array of bytes with a length of 5 ( `byte myArray[5]` in C++), the system will allocate 5 contiguous bytes of memory, and you could access these using indices from `myArray[0]` to `myArray[4]`.

```c
#include <stdint.h>
#include <stdio.h>

int main() {
    uint8_t myArray[5] = {0x41, 0x42, 0x43, 0x44, 0x45};  // 'A', 'B', 'C', 'D', 'E' in ASCII

    printf("First element: %c\n", myArray[0]);  // Output: 'A'
    printf("Last element: %c\n", myArray[4]);   // Output: 'E'

    return 0;
}

```

Bytecode is a lower-level, platform-independent representation of source code. It is an intermediate step between human-readable source and machine code that a computer's CPU can execute directly.

When a program is compiled or interpreted, the source code is often converted into bytecode, which can then be executed by a virtual machine (such as the Java Virtual Machine for Java code) or further compiled into native machine code for execution.

Bytecode is often represented as an array of bytes, where each byte or sequence corresponds to a specific instruction or operation.

Because each bytecode instruction corresponds to a particular sequence of bytes, the array can represent unique parts of a program's logic and functionality. For example, a certain byte or series of bytes might represent the operation to add two numbers. At the same time, another sequence might indicate a jump operation to a different part of the code.

For example, let's say we have the following x86 assembly code:

```nasm
MOV EAX, 1
ADD EAX, 2
RET

```

This code moves the value `1` into the `EAX` register, adds `2`, and returns. After assembling, this could be translated into the following machine code:

```
B8 01 00 00 00 83 C0 02 C3

```

Here,

- `B8 01 00 00 00` represents the `MOV EAX, 1` instruction.
- `83 C0 02` represents the `ADD EAX, 2` instruction.
- `C3` represents the `RET` instruction.

This sequence of bytes ( `B8 01 00 00 00 83 C0 02 C3`) is what we would refer to as an AoB.

## AoBs and Game Hacking

For game hackers, understanding the use of byte arrays is vital. It is a very common technique as a part of memory scanning to locate unique code locations for persistent code injection.

As we know, memory scanning is the process of combing through the memory of a running process to locate specific values or sequences of values. This can reveal the memory locations of game variables such as a player's health or score.

For instance, consider a simple game where the player's score is stored in memory as an integer (4 bytes). A game hacker could start by scanning the entire memory space for the initial score (0). As the score changes, they could conduct another scan for the new value, thus gradually narrowing down the potential memory locations until the exact location is pinpointed.

Once the memory location of a variable is identified, a game hacker can modify its value to cheat in the game. However, these memory locations can shift each time the game restarts or even during gameplay, where byte arrays become helpful.

Game hackers can use an array of bytes (or 'byte pattern') to identify unique code sequences associated with the variable of interest. These unique sequences are often code segments that read from or write to the variable.

For example, consider a hypothetical byte pattern that writes to the player's score:

```nasm
mov eax, 9 ; Move the value 9 (representing lives) into the eax register
mov [edi+444], eax ; Move the value from the eax register into the memory location edi+444

```

The corresponding byte array might appear something like this:

```java
byte byteArray[] = {
  0xB8, 0x09, 0x00, 0x00, 0x00, // mov eax, 9
  0x89, 0x87, 0xBC, 0x01, 0x00, 0x00 // mov [edi+444], eax
};

```

The `0xB8, 0x09, 0x00, 0x00, 0x00` bytes represent the instruction `mov eax, 9`. It moves the value `9` into the `eax` register. In assembly language, `eax` is a general-purpose register that is commonly used for arithmetic operations and holding return values. The `0x89, 0x87, 0xBC, 0x01, 0x00, 0x00` bytes represent the instruction `mov [edi+444], eax`. It moves the value in the `eax` register to the memory location specified by the expression `[edi+444]`. The `mov` instruction copies the value from the source (in this case, `eax`) to the destination (memory location).

Instead of searching for the memory address of the variable directly, a game hacker could scan the memory for this specific byte array. Once found, they can compute the function’s memory address relative to the location of this byte array. This allows them to inject code or change game variables reliably, even when memory addresses vary.


# Scripting AoB

* * *

Instead of searching for the Lives memory address as we did previously, scanning the memory for a byte array that we can use to match the Lives function is possible. Once found, we can automatically compute the function’s memory address relative to the location of this byte array. This will allow us to create a script that can reliably find the Lives address and change its value every time without having to find it as the address changes manually.

Cheat Engine provides valuable functionality to find AoB patterns automatically. After scanning for the Lives memory address and finding what writes to it again, we return to the memory viewer using the same techniques covered in the last module.

![](https://academy.hackthebox.com/storage/modules/208/ce-memoryviewer.png)

Open the `Auto assembler` via the `Tools menu` and select the `AoB Injection` option from the `Templates menu`. After confirming all prompts, Cheat Engine generates a script template for you.

```nasm
{ Game   : Hackman.exe
  Version:
  Date   : 2023-09-08
  Author : PandaSt0rm

  This script does blah blah blah
}

[ENABLE]

aobscanmodule(INJECT,GameAssembly.dll,89 47 44 8B 0D 78 4A C4 79 83 79 74 00 75 0F 51) // should be unique
alloc(newmem,$1000)

label(code)
label(return)

newmem:

code:
  mov [edi+44],eax
  mov ecx,[GameAssembly.dll+C04A78]
  jmp return

INJECT:
  jmp newmem
  nop 4
return:
registersymbol(INJECT)

[DISABLE]

INJECT:
  db 89 47 44 8B 0D 78 4A C4 79

unregistersymbol(INJECT)
dealloc(newmem)

{
// ORIGINAL CODE - INJECTION POINT: GameAssembly.dll+2200EC

GameAssembly.dll+2200CB: 75 14                 - jne GameAssembly.dll+2200E1
GameAssembly.dll+2200CD: 68 78 4A C4 79        - push GameAssembly.dll+C04A78
GameAssembly.dll+2200D2: E8 19 FB EB FF        - call GameAssembly.il2cpp_get_exception_argument_null+260
GameAssembly.dll+2200D7: 83 C4 04              - add esp,04
GameAssembly.dll+2200DA: C6 05 AD D9 C7 79 01  - mov byte ptr [GameAssembly.dll+C3D9AD],01
GameAssembly.dll+2200E1: 8B 45 0C              - mov eax,[ebp+0C]
GameAssembly.dll+2200E4: 53                    - push ebx
GameAssembly.dll+2200E5: 57                    - push edi
GameAssembly.dll+2200E6: 8B 7D 08              - mov edi,[ebp+08]
GameAssembly.dll+2200E9: 8B 5F 20              - mov ebx,[edi+20]
// ---------- INJECTING HERE ----------
GameAssembly.dll+2200EC: 89 47 44              - mov [edi+44],eax
// ---------- DONE INJECTING  ----------
GameAssembly.dll+2200EF: 8B 0D 78 4A C4 79     - mov ecx,[GameAssembly.dll+C04A78]
GameAssembly.dll+2200F5: 83 79 74 00           - cmp dword ptr [ecx+74],00
GameAssembly.dll+2200F9: 75 0F                 - jne GameAssembly.dll+22010A
GameAssembly.dll+2200FB: 51                    - push ecx
GameAssembly.dll+2200FC: E8 0F FD EB FF        - call GameAssembly.il2cpp_runtime_class_init
GameAssembly.dll+220101: 8B 0D 78 4A C4 79     - mov ecx,[GameAssembly.dll+C04A78]
GameAssembly.dll+220107: 83 C4 04              - add esp,04
GameAssembly.dll+22010A: 80 3D 42 DA C7 79 00  - cmp byte ptr [GameAssembly.dll+C3DA42],00
GameAssembly.dll+220111: 75 1A                 - jne GameAssembly.dll+22012D
GameAssembly.dll+220113: 68 78 4A C4 79        - push GameAssembly.dll+C04A78
}

```

The primary difference between this script and the previous one lies in determining the memory address for injection. Instead of hardcoding the injection location as we did before, Cheat Engine now uses the `aobscanmodule` function to identify the injection address dynamically. The tool also automatically includes the necessary framework code.

Your instructions might look something like `GameAssembly.a_t76FB4BAAE78C0C631D249234492EEA772C0048C8_il2cpp_TypeInfo_var`. Don’t panic; everything still applies. Cheat Engine is simply resolving symbols from the runtime.

### AoB Scan Modules

Cheat Engine has three AoB Scan modules:

- `AOBSCAN(injectionName, xx xx xx xx xx)`: This function scans through memory to locate the provided array of bytes and assigns the result to the symbol known as "injectionName".
- `AOBSCANMODULE(injectionName, $moduleName, xx xx xx xx xx)`: This function scrutinises a specific module's memory for the specified array of bytes and attributes the result to the symbol tagged as "injectionName".
- `AOBSCANREGION(injectionName, $StartAddress, $EndAaddress, xx xx xx xx xx)`: This function searches a particular range—from the start address to the end address—for the provided AoB and assigns the identified pattern to the symbol tagged as "injectionName".

In our case, we use the `aobscanmodule` method because the game logic is in the `GameAssembly.dll` library, with these parameters: `aobscanmodule(INJECT,GameAssembly.dll,89 47 44 8B 0D 78 4A C4 79 83 79 74 00 75 0F 51)`. This returns the address of the first matching AoB.

The main alteration between this AoB script and our previous injection script is that we now define the injection point dynamically with `INJECT:` using the `aobscanmodule` function instead of predefining it with a specific location of `GameAssembly.dll+2200EC:`.

Cheat Engine attempts to create a unique AoB pattern with the bytes `89 47 44 8B 0D 78 4A C4 79 83 79 74 00 75 0F 51`, which correspond to the bytes of the opcodes:

```nasm
GameAssembly.dll+2200EC: 89 47 44              - mov [edi+44],eax
GameAssembly.dll+2200EF: 8B 0D 78 4A C4 79     - mov ecx,[GameAssembly.dll+C04A78]
GameAssembly.dll+2200F5: 83 79 74 00           - cmp dword ptr [ecx+74],00
GameAssembly.dll+2200F9: 75 0F                 - jne GameAssembly.dll+22010A
GameAssembly.dll+2200FB: 51                    - push ecx

```

Upon executing the script, Cheat Engine will attempt to scan the entire game's memory to locate that specific pattern of bytes. While these patterns do not always work, they offer a good starting template. Add the `mov eax,09` instruction to the `newmem` section, assign the script to the table via the file menu, and enable it. The script injects successfully, and we now have a permanent 9 lives.

Close Hackman, reopen it, and reattach Cheat Engine. When Cheat Engine asks if you want to keep the current table, click yes, and then click yes again when it asks to disable enabled scripts. Try to enable the script again, but nothing happens. This is because the pattern that Cheat Engine identified is not unique. So `find what writes to the address`, and let's look at the surrounding instructions in memory again.

![](https://academy.hackthebox.com/storage/modules/208/ce-memoryviewer2.png)

### Relative & Absolute Addressing

As mentioned in the last module, there's a quirk with how Unity handles memory, generally because all the game logic is not actually in the executable process. The code below shows how the bytes have changed for the referenced location in `GameAssembly.dll`, but the reference remains the same at `GameAssembly.dll+C04A78`.

```nasm
From:
GameAssembly.dll+2200EC: 89 47 44              - mov [edi+44],eax
GameAssembly.dll+2200EF: 8B 0D 78 4A C4 79     - mov ecx,[GameAssembly.dll+C04A78]
GameAssembly.dll+2200F5: 83 79 74 00           - cmp dword ptr [ecx+74],00
GameAssembly.dll+2200F9: 75 0F                 - jne GameAssembly.dll+22010A
GameAssembly.dll+2200FB: 51                    - push ecx

To:
GameAssembly.dll+2200EC: 89 47 44              - mov [edi+44],eax
GameAssembly.dll+2200EF: 8B 0D F8 53 CF 78     - mov ecx,[GameAssembly.dll+C04A78]
GameAssembly.dll+2200F5: 83 79 74 00           - cmp dword ptr [ecx+74],00
GameAssembly.dll+2200F9: 75 0F                 - jne GameAssembly.dll+22010A
GameAssembly.dll+2200FB: 51                    - push ecx

```

There are two types of memory addresses:

1. `Absolute Address`: This refers to a memory slot's exact physical or virtual location. It remains constant once assigned and can be used directly to access the memory location.
2. `Relative Address`: This is an address given as a location relative to another known address, often a base address. For example, if the base address is 1000, a relative address might be expressed as "1000 + 50" or just "+50". The actual physical or virtual location this refers to can change depending on the value of the base address.

When a program is loaded into memory, it often uses relative addressing to refer to its code and data. This is because the program doesn't know in advance where it will be loaded into memory; that's determined by the operating system when the program is executed. By using relative addressing, the program can refer to its components regardless of where they end up in memory.

The `mov ecx,[GameAssembly.dll+C04A78]` instruction moves the value located at the memory address `GameAssembly.dll+C04A78` into the `ecx` register. However, this isn't an absolute address but a relative one.

When the `GameAssembly.dll` module is loaded into memory, it might not always be loaded at the same base address. This shift is due to Address Space Layout Randomisation (ASLR), a security technique used in operating systems to help prevent the exploitation of memory corruption vulnerabilities. The main principle of ASLR is quite simple: it randomises the location where program executables are loaded into memory.

The bytes `78 4A C4 79` and `F8 53 CF 78 ` in the disassembled code are the encoded form of the relative address `GameAssembly.dll+C04A78`. These bytes are different because the base address of the `GameAssembly.dll` module changes each time the library is loaded.

The AoB scan module cannot find our initial pattern because it no longer exists. We can try to use a wildcard to accept any bytes in the position of the changing bytes. Acceptable wildcard characters are `x`, `?`, or `*`. Theoretically, our pattern changes to `89 47 44 8B 0D ** ** ** ** 83 79 74 00 75 0F 51`. However, we now encounter another problem: Cheat Engine will write specific bytes to disable the script that it took from the original instructions, and if we try to use the wildcard AoB, it 0s to the wildcard positions when we disable the script.

```nasm
[DISABLE]

INJECT:
  db 89 47 44 8B 0D F8 53 CF 78 // or 89 47 44 8B 0D ** ** ** **

```

![](https://academy.hackthebox.com/storage/modules/208/ce-baddb.png)

At this point, we can either jump off a different AoB or assemble the instructions in the script's disable section rather than write raw bytes. Writing the original instructions in the disable section involves removing the `db` instruction. This isn’t a common problem. It’s an issue that crops up occasionally, so just be aware of it.

```nasm
[DISABLE]

INJECT:
mov [edi+44],eax
mov ecx,[GameAssembly.dll+C04A78]

unregistersymbol(INJECT)
dealloc(newmem)

```

So the final script looks like this:

```nasm
{ Game   : Hackman.exe
  Version:
  Date   : 2023-09-08
  Author : PandaSt0rm

  This script does blah blah blah
}

[ENABLE]

aobscanmodule(INJECT,GameAssembly.dll,89 47 44 8B 0D ** ** ** ** 83 79 74 00 75 0F 51) // should be unique
alloc(newmem,$1000)

label(code)
label(return)

newmem:
mov eax, 09
code:
  mov [edi+44],eax
  mov ecx,[GameAssembly.dll+C04A78]
  jmp return

INJECT:
  jmp newmem
  nop 4
return:
registersymbol(INJECT)

[DISABLE]

INJECT:
mov [edi+44],eax
mov ecx,[GameAssembly.dll+C04A78]

unregistersymbol(INJECT)
dealloc(newmem)

{
// ORIGINAL CODE - INJECTION POINT: GameAssembly.dll+2200EC

GameAssembly.dll+2200CB: 75 14                 - jne GameAssembly.dll+2200E1
GameAssembly.dll+2200CD: 68 78 4A C4 79        - push GameAssembly.dll+C04A78
GameAssembly.dll+2200D2: E8 19 FB EB FF        - call GameAssembly.il2cpp_get_exception_argument_null+260
GameAssembly.dll+2200D7: 83 C4 04              - add esp,04
GameAssembly.dll+2200DA: C6 05 AD D9 C7 79 01  - mov byte ptr [GameAssembly.dll+C3D9AD],01
GameAssembly.dll+2200E1: 8B 45 0C              - mov eax,[ebp+0C]
GameAssembly.dll+2200E4: 53                    - push ebx
GameAssembly.dll+2200E5: 57                    - push edi
GameAssembly.dll+2200E6: 8B 7D 08              - mov edi,[ebp+08]
GameAssembly.dll+2200E9: 8B 5F 20              - mov ebx,[edi+20]
// ---------- INJECTING HERE ----------
GameAssembly.dll+2200EC: 89 47 44              - mov [edi+44],eax
// ---------- DONE INJECTING  ----------
GameAssembly.dll+2200EF: 8B 0D 78 4A C4 79     - mov ecx,[GameAssembly.dll+C04A78]
GameAssembly.dll+2200F5: 83 79 74 00           - cmp dword ptr [ecx+74],00
GameAssembly.dll+2200F9: 75 0F                 - jne GameAssembly.dll+22010A
GameAssembly.dll+2200FB: 51                    - push ecx
GameAssembly.dll+2200FC: E8 0F FD EB FF        - call GameAssembly.il2cpp_runtime_class_init
GameAssembly.dll+220101: 8B 0D 78 4A C4 79     - mov ecx,[GameAssembly.dll+C04A78]
GameAssembly.dll+220107: 83 C4 04              - add esp,04
GameAssembly.dll+22010A: 80 3D 42 DA C7 79 00  - cmp byte ptr [GameAssembly.dll+C3DA42],00
GameAssembly.dll+220111: 75 1A                 - jne GameAssembly.dll+22012D
GameAssembly.dll+220113: 68 78 4A C4 79        - push GameAssembly.dll+C04A78
}

```

This updated script should help ensure that the Cheat Engine can dynamically find the AoB, and, thus, the memory address to inject into, even if the address changes between game instances due to ASLR, or other memory management trickery.

To solve the question, you will have ~15 seconds from the time a new game starts before you will have to restart Hackman. Start Hackman, inject your script, start a new game and the flag will pop up and the timer will stop.

Enable step-by-step solutions for all questions
![sparkles-icon-decoration](https://academy.hackthebox.com/images/sparkles-solid.svg)

#### Questions

Answer the question(s) below
to complete this Section and earn cubes!

\+ 15  What is the text that gets displayed when you set your lives to over 5 within the new game timer?


Submit


[Hackman.zip](/storage/modules/208/Hackman.zip)


# Game Engines

* * *

Game engines streamline the game development process, providing developers with reusable components. These include rendering engines for 2D or 3D graphics, physics, animation, audio, and scripting systems. Some of the most popular game engines currently in use are Unity, Unreal Engine, and Godot.

## Unity

Unity is a versatile game engine known for its extensive range of features, user-friendly interface, and widespread platform compatibility. It enables developers to craft games for various platforms, from PCs, consoles, and mobile devices to augmented reality/virtual reality (AR/VR) systems.

The primary scripting language for Unity is C#, granting developers access to the robust .NET ecosystem and its expansive library of functionalities. More specifically, Unity utilises [Mono](https://www.mono-project.com/), an open-source implementation of Microsoft's .NET Framework, as its runtime engine. This allows game developers to write their game logic and scripts in C#, which are compiled and executed by the Mono runtime within the Unity environment. Before Microsoft introduced dotNet Core, officially bringing the power of dotNet to all platforms, Mono was the way to run C# on non-windows platforms.

Additionally, Unity introduces the IL2CPP (Intermediate Language to C++) backend, which converts C# scripts into C++ code. This feature ensures Unity games can run on platforms lacking support for Just-in-Time (JIT) compilation, thus enhancing compatibility and performance.

## Unreal Engine

Unreal Engine is renowned for its superior visual quality, state-of-the-art graphics capabilities, and comprehensive suite of development tools. It provides an efficient and flexible environment for producing impressively realistic and immersive games.

The engine features Blueprint’s visual scripting system, enabling developers to establish game logic and behaviours without extensive coding. With Blueprint, developers can create intricate interactions, define gameplay mechanics, and implement AI behaviour using a node-based system. This feature empowers designers and artists to contribute to game development and iterate on ideas swiftly and actively.

For more experienced developers, Unreal Engine supports C++ scripting, allowing in-depth engagement with the engine's codebase and customising game behaviour, performance optimisation, or advanced functionality implementation. Combining Blueprint and C++ scripting in Unreal Engine provides a robust and adaptable development environment that caters to developers of various skill levels and requirements.

## Godot

Godot is a rising, free, and open-source game engine recognised for its lightweight design, efficient performance, and flexible scene system. It offers an uncomplicated and intuitive interface that simplifies the game development process.

Godot utilises its scripting language, GDScript, akin to Python in syntax, making it a straightforward learning experience for newcomers. GDScript provides a high-level scripting environment that enables quick prototyping and iteration.

Godot also supports C# and C++ as alternative scripting languages, catering to developers seeking more complex game development requirements. This flexibility makes the engine suitable for various projects, ranging from small independent (“indie”) games to larger-scale productions. Godot's lightweight design and scripting options appeal to developers looking for a streamlined and versatile game development experience.

## The Role of Game Engines

Developing a game from the ground up poses a considerable challenge, requiring significant resources, time, and technical proficiency. Such demands can be especially daunting for indie developers. However, utilising a commercial game engine efficiently mitigates these challenges.

- `Rendering`: Game engines determine how graphics are displayed, offering a variety of tools for creating and managing both 2D and 3D graphics.
- `Physics`: Most game engines incorporate physics engines, simulating gravity, collisions, and other forces to make the game world appear more realistic.
- `Animation`: Game engines furnish tools for generating, controlling, and scripting character movements and other animations.
- `Audio`: Built-in capabilities for sound and music playback and control are present in game engines.
- `AI`: Game engines often supply pathfinding tools and state machines, helpful in crafting AI behaviour.
- `Networking`: Built-in capabilities in game engines facilitate multiplayer gaming over the internet.

There are also more generic and broad-based reasons to use a commercial game engine:

- `Cost-Effectiveness`: Crafting a game engine in-house can be expensive and time-intensive, potentially diverting resources from game creation. Utilising a pre-existing game engine is often more economical, especially given the low royalty percentages, fee structures, or entirely free.
- `Rapid Development`: Game engines supply many ready-made tools and solutions to expedite development. They manage many technical aspects of game creation, enabling developers to focus on creative elements such as design and gameplay.
- `Support and Community`: Established game engines boast extensive user communities and comprehensive documentation, invaluable during development. Conversely, an in-house engine may lack such support.
- `Cross-Platform Compatibility`: Most commercial game engines provide cross-platform support. This allows for game development on one platform and subsequent deployment on various platforms like Windows, MacOS, iOS, Android, and gaming consoles with minimal changes. Constructing this capability in-house would be a significant undertaking.
- `Community and Resources`: Renowned game engines have active communities and a wealth of documentation and resources. These communities comprise fellow developers, enthusiasts, and experts who actively share their knowledge, support, and insights.
These resources aid in understanding the game engine's features, mastering specific techniques, navigating challenges, and staying current with the latest developments in the field. The proactive community and abundant resources cultivate a supportive environment that fosters game development growth, learning, and innovation.

Game engines have become integral to game development, equipping developers with powerful tools and resources for creating their games more efficiently and effectively. As the industry evolves, game engines like Unity, Unreal Engine, and Godot will continue to play a pivotal role, driving innovation and enabling developers to realise their visions.

## Identifying Game Engines

Recognising the game engine a specific game utilises can be beneficial for reasons such as modding, debugging, or gleaning insights from the techniques employed by other developers.

### Check the Game's Credits

Ascertaining a game engine can be as straightforward as examining the game's credits or box. Developers typically acknowledge the technology that facilitated the construction of their games. The game engine is usually listed under the `Technologies Used` section, a similar category, or in the in-game credits/startup screens.

### Use Database Platforms Like SteamDB

Database platforms such as `SteamDB` compile comprehensive information about games, including the technologies used in their creation. After locating the game entry in the database, navigate to the `App Info` section in the left-hand menu. Scroll down to find a row labelled `Detected Technologies` in the table, which lists the game technologies utilised.

![](https://academy.hackthebox.com/storage/modules/208/steamdb.png)

### Directory Structure and Files

Some games and technologies have a unique folder structure and files specific to that engine. Consider the table below.

| Unity Engine Game | Unreal Engine Game |
| --- | --- |
| .<gamename.exe>\_Data\ | .\\Engine |
| .\\Data\\Managed\ | .\\Engine\\Binaries\\ThirdParty\ |
| .\\mono\ | .\\Engine\\Binaries\\Win64\\CrashReportClient.exe |
| .\\GameAssembly.dll | \*.ucas |
| .\\<gamename.exe>\_Data\\Managed\\Assembly-CSharp.dll | \*.utoc |

## Hacking Game Engines

Hackers can target the game itself or the underlying game engine when hacking games to create cheats. The decision largely depends on the hacker's goals, technical abilities, and the specific structures of the game and engine. However, there are several reasons why a hacker might choose to target the game engine over the game itself:

- `Universality`: Game engines are used in the development of many games. If a hacker learns how to manipulate the engine, they could potentially create cheats for any game built on that engine, bypassing the need to understand each game's complexities.
- `Engine vulnerabilities`: Game engines often have inherent functionalities and potential vulnerabilities that may not be fully addressed or can be exploited to create cheats. For example, if a game engine is known for handling collision detection in a certain way, a cheat could be designed to exploit this.
- `Code accessibility`: While game code can be obfuscated or protected to prevent cheating, engine code is often more straightforward. Although game developers can take steps to secure the game's individual code, they usually have far less control over the security of the engine itself. In the case of commercial game engines, they are typically very well publicly documented.
- `Persistence`: Games are frequently updated, resulting in code changes that can make existing cheats obsolete. While game engines also receive updates, they are generally less frequent and less likely to disrupt the functionality of cheats based on engine exploitation.


# Unity IL2CPP

* * *

In software development, optimising code performance and ensuring security is paramount. One technology that plays a vital role in achieving these goals is IL2CPP (Intermediate Language to C++). IL2CPP is a conversion technology developed by Unity Technologies, primarily used in the Unity game engine.

## What is a Just-In-Time (JIT) Compiler

Before diving into `IL2CPP`, let's understand the Just-In-Time ( `JIT`) compiler concept. A `Just-In-Time (JIT)` compiler is a type of compiler that converts program code into machine language just before runtime. Unlike a traditional compiler that converts source code into machine code before the program is executed, a `JIT` compiler performs this conversion process as the program runs.

The `.NET` Just-In-Time ( `JIT`) compiler is integral to the .NET runtime. It serves a crucial role in converting the Common Intermediate Language ( `CIL`) code, also known as `MSIL` or `IL`, into machine code that can be executed directly by the CPU.

The .NET platform uses a `JIT` compiler to compile its `Intermediate Language (IL)` code into machine code. Writing code in a .NET language (like `C#` or `Visual Basic`) isn't directly compiled into machine code. Instead, it's first compiled into `IL` code. This stage is where the .NET `JIT` compiler comes into play. It compiles this `IL` code into machine code just before execution.

When the application is launched, the .NET runtime loads the `CIL` code for the executing method into memory, and the `JIT` compiler converts it into machine code.

Noteworthy is that the `JIT` compilation is performed on a per-method basis as and when required rather than on the entire application simultaneously. A method's `CIL` code will be `JIT` compiled to machine code the first time it is invoked, and the resulting machine code is cached for subsequent calls.

## What is IL2CPP

`IL2CPP`, or `Intermediate Language To C++`, is a scripting backend developed by Unity. Its primary function is to convert .NET bytecode ( `Common Intermediate Language`, or `CIL`) into C++ code, which is then compiled to machine code by a platform-specific compiler. This technology allows developers to exploit the platform-agnostic nature of .NET while still achieving the performance and compatibility of native C++ code.

Unity introduced `IL2CPP` for several reasons.

- `Performance`: By converting IL code into C++, IL2CPP unlocks the performance benefits of native code execution. The resulting C++ code can be highly optimised, enabling efficient memory management, reducing overhead, and providing faster execution times.
- `Full Ahead of Time (AOT) Compilation`: Unlike JIT compilers that dynamically convert IL code at runtime, IL2CPP performs ahead-of-time (AOT) compilation. This eliminates the need for just-in-time compilation during runtime, reducing start-up times and delivering a smoother user experience on platforms that maybe have issues running a JIT compiler, such as mobile devices and some game consoles.
- `Type Safety`: `IL2CPP` enforces strict type safety, which can prevent certain types of bugs and also enhance security.
- `Platform Support`: `IL2CPP` generates platform-independent C++ code that can be compiled for various target platforms. This cross-platform compatibility allows Unity games to be deployed seamlessly on different operating systems and devices, eliminating the need for platform-specific adaptations.

## How Does IL2CPP Work?

When you initiate a build using the IL2CPP scripting backend in Unity, a multi-step process is triggered to convert your C# scripts into a final executable suitable for your target platform. Here's a breakdown of the stages Unity goes through during this process:

1. `C# Compilation`: The Roslyn C# compiler is initially called into action. It takes your application's C# scripts and any code from required packages and compiles them into .NET DLLs. These are managed assemblies and contain the intermediate language (IL) representation of your code.
2. `Managed Bytecode Stripping`: After the compilation, Unity performs a bytecode stripping process on the managed assemblies. Bytecode stripping removes unused classes, methods, and metadata from the assemblies. This is a crucial step, especially for applications targeting platforms with limited resources, as it can significantly reduce the final size of the application.
3. `Conversion to C++`: Once the bytecode stripping is completed, the IL2CPP backend takes over. It converts all the managed assemblies, now stripped of unnecessary bytecode, into standard C++ code. This transformation allows your .NET code to be executed as native code on the target platform.
4. `C++ Compilation`: With the C++ code generated, the next step is to compile it. Unity uses the native platform compiler to compile both the generated C++ code and the runtime portion of IL2CPP. This ensures optimal performance and compatibility for the target platform.
5. `Creation of Executable or DLL`: Based on the platform you're targeting, Unity finalises the build process by creating either an executable file (for standalone platforms like PC or console) or a dynamic link library (DLL, typically for platforms where the main executable is provided by a launcher or system layer).

## IL2CPP and Security

While `IL2CPP` provides performance and compatibility advantages, it also affects game security. It's not a silver bullet by any means, given that tools and frameworks exist to reverse-engineer the `IL2CPP` process. Nonetheless, it does add an additional layer that makes the extremely simple reverse engineering of C# assemblies more difficult. The ease with which .NET assemblies can be decompiled compared to C++ binaries is influenced by the architecture and design principles of each environment.

.NET assemblies are created in a high-level, platform-independent Intermediate Language (IL) that includes a lot of metadata. This metadata describes everything from the types and signatures of methods to the structure of classes and interfaces.

This information is kept to enable features like reflection and Just-In-Time (JIT) compilation at runtime. As a result, the .NET runtime has enough information to perform various operations on the fly, but it also means that much of the original code structure is still present in the compiled assembly. Tools like ILSpy and dotPeek can easily use this metadata to reverse-engineer the IL back into readable C# code.

On the other hand, C++ is compiled into machine code that is specific to the target architecture. This process often includes aggressive optimizations like function inlining, loop unrolling, and removal of unused code, which not only make the code run faster but also make it harder to reverse-engineer. The resulting binary is a low-level representation that lacks the rich metadata found in .NET assemblies.

C++ also doesn't have runtime features like reflection that rely on such metadata. As a result, although tools are available to disassemble C++ binaries back into assembly language, figuring out the original high-level code structure from this output is a much more difficult task compared to .NET assemblies.

A TL;DR table follows:

| Feature/Aspect | .NET | C++ |
| --- | --- | --- |
| Compilation Target | Intermediate Language (IL) | Native machine code |
| Metadata | Rich (includes type info, method signatures, etc.) | None or minimal |
| Reverse Engineering Tools | Readily available (ILSpy, dotPeek) | Less effective (IDA Pro, Ghidra) |
| Code Obfuscation | Available but not by default | Complex optimizations during compilation |
| Reflection | Supported | Not supported |
| Decompilation Accuracy | High (can recover original structure and sometimes variable names) | Low (assembly code to source conversion is difficult) |
| Platform Agnostic | Yes (aimed for cross-platform compatibility) | No (often platform-specific) |
| Runtime Environment | Managed (JIT compilation, garbage collection, etc.) | Unmanaged (direct hardware access) |
| Security Layers | Fewer (easier to decompile) | More (harder to decompile) |
| Code Complexity | Standardized APIs, less low-level tricks | Can use low-level optimizations and platform-specific instructions |

For all these reasons, the security benefits of utilising IL2CPP remain valid and are worth taking advantage of.


# Game Modifications

* * *

Game modifications, popularly known as game mods, refer to alterations made by players or fans to a video game that change one or more aspects of the original game, such as how it looks or behaves. Mods can range from small changes and tweaks to complete overhauls and can extend the replay value and interest of the game.

## History of Game Mods

The history of game mods is as old as commercial computers and video games themselves. One of the first popular mods was a parody of Castle Wolfenstein on the Apple II in the early 1980s called [Castle Smurfenstein](https://www.evl.uic.edu/aej/smurf.html).

![Castle Smurfenstein](https://academy.hackthebox.com/storage/modules/208/smurfensteinTitle.gif)

In the early 1990s, the gaming landscape changed dramatically with the release of id Software's ground-breaking 'Doom' series. Doom became one of the first games to support modifications, affectionately known as mods. It provided gamers with a platform for expressing their creativity and customising the game according to their preference. Players were encouraged to design their game elements, including new monsters, innovative weapons, and intricate levels. This was made possible by id Software's decision to make Doom's WAD files (Where's All the Data) openly accessible, a revolutionary move that allowed players to modify the game.

[Origwad](https://doomwiki.org/wiki/Origwad) is an early user-generated Doom level, crafted by Jeffrey Bird from James Cook University in North Queensland. Lacking an official title, it is saved under the filename `ORIGWAD.PWD`.

![The opening screen](https://academy.hackthebox.com/storage/modules/208/320px-Origwad_2.png)

This dynamic created a two-way relationship between game developers and the gaming community, wherein the players could also become creators. The result was flourishing user-generated content that expanded the original game beyond its initial design. Some mods became as popular as the original game, highlighting the talent and creativity within the Doom modding community.

The game modding movement took on a new dimension with the advent and eventual ubiquity of the internet. Before the internet, modders would have to work alone or in small localised groups. Sharing their work was limited to local networks or physical media, significantly limiting the potential audience for their creations. However, the internet changed everything. Modders were no longer isolated but could collaborate on projects with people worldwide. Mod-sharing became significantly more accessible, and a global community of modders began to form.

Forums and websites dedicated to game modding sprouted, providing platforms for modders to share their work, ask for help, and receive feedback. This accelerated the development of mods, as ideas could be exchanged more rapidly and problems could be solved collectively.

Furthermore, with the global sharing of mods, players from all corners of the world could access and enjoy these fan-made creations. This led to an exponential increase in the popularity of mods and further spurred the growth of the modding community.

## Types of Mods

Game mods can be broken down into several major categories:

- `Overhaul Mods`: These represent large-scale changes that significantly alter various elements of a game, including its graphics, gameplay, or storyline. A prime example is the [Radious Total War Mods](https://steamcommunity.com/sharedfiles/filedetails/?id=2791750313). Developed for the various titles in the `Total War` game series, this mod introduces many new units, enhances AI tactics, overhauls the economic and political systems, and balances gameplay aspects to foster a more immersive experience. It reshapes the gaming experience, making it more strategic, diverse, and engaging, overhauling the game.
- `Add-on Mods`: These mods introduce new content into the game, such as characters, weapons, missions, items or functionality. A case in point is the Minecraft mod [Controlling](https://www.curseforge.com/minecraft/mc-mods/controlling), which integrates a new function to search for keybinds using their name in the KeyBinding menu.
- `Unofficial Patch Mods`: These mods address and rectify bugs and glitches that the official patches have missed. For instance, the [Skyrim Unofficial Patch](https://www.nexusmods.com/skyrimspecialedition/mods/266) is a comprehensive bug-fixing mod for `The Elder Scrolls V: Skyrim`. This mod rectifies numerous bugs and issues, from quest bugs and NPC dialogue problems to item inconsistencies, incorrect textures, and logic errors in the game's code, overlooked in the official patches.
- `Art Mods`: Developed for artistic expression, these mods aim to provide a unique experience or enhance the graphics of older games. [GZDoom](https://zdoom.org/index) is an example of such a mod, built for the timeless game `Doom`. It introduces advanced graphic hardware API support (OpenGL), superior software rendering, and broad modding capabilities for artistic refinements. Mods crafted with GZDoom can dramatically transform Doom's visual style by integrating dynamic lighting, high-resolution textures, and 3D models. This transition morphs the traditional pixelated game into a contemporary first-person shooter, illustrating how art mods can substantially upgrade the visuals and aesthetics of an older game.
- `Total Conversion Mods`: These extensive mods, built on the original game's architecture, entirely transform the game. [Enderal: Forgotten Stories](https://store.steampowered.com/app/976620/Enderal_Forgotten_Stories_Special_Edition/) is a total conversion mod for `The Elder Scrolls V: Skyrim`. It employs Skyrim's engine but delivers an entirely new game world with its unique lore, storyline, gameplay mechanics, and visual style. The mod presents a dark, immersive narrative, complex characters, and an innovative skill system, transforming Skyrim into a distinct game and illustrating the immense potential of total conversion mods.

Some popular Total Conversion mods even became full-blown standalone games:

- `Counter-Strike`: This began as a mod for Valve Corporation's game Half-Life. Created by Minh "Gooseman" Le and Jess "Cliffe" Cliffe, they sought to blend elements from Half-Life with the team-based mechanics of games like Rainbow Six. They envisaged a game emphasising teamwork and strategy within a first-person shooter framework. As the mod's popularity skyrocketed online, it caught the attention of Valve, leading to the acquisition of the mod's rights and the employment of its creators. In 2000, Counter-Strike emerged as a standalone game, becoming one of the most successful online first-person shooter games in history. The Counter-Strike series has seen multiple iterations, including Counter-Strike: Source and Counter-Strike: Global Offensive, introducing new elements to the classic gameplay.

- `Dota (Defense of the Ancients)`: Dota stands as a stellar example of a game mod morphing into a standalone game, consequently igniting an entirely new genre of games. Originating as a community-created mod for Blizzard Entertainment's Warcraft III: Reign of Chaos and its expansion pack, The Frozen Throne, Dota revolutionised real-time strategy (RTS) gaming.

The focus shifted from traditional strategies to controlling a single, powerful character, or 'hero', in a team-based setting. The primary objective involved demolishing the opposing team's central structure, the 'Ancient'.

Initially developed by a modder named 'Eul', this mod gained exponential popularity online. Later, other key figures, such as 'IceFrog', assumed its maintenance and development. The unique concept behind Dota rapidly amassed a large player base.

Recognising Dota's surging popularity, Valve Corporation once again recruited significant Dota community members, including 'IceFrog', to create an updated sequel. This collaboration resulted in the launch of Dota 2 in 2013. While Dota 2 preserved the core gameplay mechanics of the original mod, it introduced enhanced graphics, novel features, and robust support for eSports competitions.

Furthermore, the triumph of Dota, followed by Dota 2, instigated the rise of a new genre of games, namely Multiplayer Online Battle Arenas (MOBAs). This genre encompasses popular titles like League of Legends and Heroes of the Storm, emphasising the profound influence game mods can exert in the broader video gaming landscape.


While game mods can significantly enhance a player's experience, they are not without their controversies. Some game developers dissuade modding due to potential repercussions, including copyright disputes, game instability, or unfair advantages in multiplayer settings. Nevertheless, numerous developers support modding, recognising its potential to extend their games' longevity and foster a dedicated player community.

## Tooling

Creating game mods heavily depends on the game itself, its underlying engine, and the type of modification you wish to introduce. Nonetheless, there are some standard methodologies and tools employed:

`Official Modding Tools`: Some developers endorse modding by releasing official tools that allow you to create mods for their games. These tools offer direct access to the game's assets and codebase, facilitating extensive customisation. Examples include the Creation Kit for The Elder Scrolls and Fallout series.

`Scripting`: Many games have embedded scripting languages that govern gameplay mechanics. Learning these languages permits modders to alter or introduce new functions. For instance, many games use Lua, a lightweight scripting language.

`3D Modelling and Texturing`: For mods that introduce new objects or characters or modify existing ones, knowledge of 3D modelling and texturing is critical. Tools such as Blender or Maya are commonly employed to create these models, and Photoshop or GIMP may be used to create textures.

`Reverse Engineering`: When no official modding tools are accessible, modders may need to reverse engineer the game to comprehend its functionality. This can involve disassembling the game's code or using debugging tools to inspect it while running. Understanding the game engine that the game is built upon can also be incredibly beneficial. Many popular games are developed on engines like Unreal Engine or Unity, and knowledge of these systems can substantially aid in mod creation.

`Community Tools`: Often, modding communities devise their own tools to facilitate mod creation for specific games. These tools can be incredibly useful, especially for beginners.


# Obfuscation

* * *

`Code obfuscation` is a technique to protect software code from being easily understood and manipulated by unauthorised persons. Its main goal is to make the source code more `complex` and challenging to comprehend without the proper tools or knowledge. It is a one-way, irreversible process; thus, obfuscation is applied only to built/released files no longer under development.

Consider programming for a moment. We assign names to variables, methods, classes, etc., to give them context, enabling better understanding. For example, a function named `calculateTotalCost` would imply that this function computes the total cost of something. Additional information can be inferred from the parameters. Consider this straightforward C# program that calculates the total price of a basket of items:

```csharp
using System;
using System.Collections.Generic;

class Program
{
    static void Main(string[] args)
    {
        // Initialize a dictionary to hold items (string) and their corresponding prices (double)
        Dictionary<string, double> basket = new Dictionary<string, double>();
        string item;
        double price;
        double total = 0.0;

        // Keep asking for items and their prices until the user types "done"
        while (true)
        {
            Console.WriteLine("Enter the name of the item (or 'done' to finish): ");
            item = Console.ReadLine();
            if (item == "done") break;  // If the user types "done", break out of the loop

            Console.WriteLine("Enter the price of the item: ");
            price = Convert.ToDouble(Console.ReadLine());  // Convert the input from a string to a double
            basket[item] = price;  // Add the item and its price to the dictionary
        }

        // Calculate the total cost by adding up all the prices in the basket
        foreach (KeyValuePair<string, double> entry in basket)
        {
            total += entry.Value;
        }

        // Print out the total cost
        Console.WriteLine("Total cost of the shopping basket: " + total);
    }
}

```

The comments make it easy to understand how the program works, even if you do not understand C#. The appropriately named variables aid significantly in that understanding. However, if we obfuscate that code, suddenly, the code gets a lot harder to understand.

```csharp
using System;
using System.Collections.Generic;

class P
{
    static void Main(string[] a)
    {
        Dictionary<string, double> b = new Dictionary<string, double>();
        string i; double p, t = 0.0;

        while (true)
        {
            Console.WriteLine("Enter the name of the item (or 'done' to finish): ");
            i = Console.ReadLine();
            if (i == "done") break;

            Console.WriteLine("Enter the price of the item: ");
            p = Convert.ToDouble(Console.ReadLine());
            b[i] = p;
        }

        foreach (KeyValuePair<string, double> e in b)
        {
            t += e.Value;
        }

        Console.WriteLine("Total cost of the shopping basket: " + t);
    }
}

```

In `C#`, a range of overlapping obfuscation techniques are used, but these techniques are common to most other languages as well.

### Name Obfuscation

This technique alters the names of methods, variables, and classes to become unrecognisable or misleading. For example, a method called `DisplayDetails` could be renamed to `A1B2C3`, making it significantly more challenging to understand the method's purpose from its name alone.

Before:

```csharp
public class Employee
{
    public string Name { get; set; }
    public int Salary { get; set; }

    public void DisplayDetails()
    {
        Console.WriteLine("Name: " + Name + ", Salary: " + Salary);
    }
}

```

After:

```csharp
public class X1Y2
{
    public string a { get; set; }
    public int b { get; set; }

    public void A1B2C3()
    {
        Console.WriteLine("Name: " + a + ", Salary: " + b);
    }
}

```

### String Encryption

This strategy is used to obscure strings used within the program. These strings could include critical data such as database credentials, error messages, or other sensitive information. The actual values are only decrypted at runtime, making static analysis more challenging.

Before:

```csharp
public class Greeting
{
    public void ShowGreeting()
    {
        Console.WriteLine("Welcome to our application!");
    }
}

```

After:

```csharp
public class Greeting
{
    public void ShowGreeting()
    {
        Console.WriteLine(Decrypt("dryp|zr-|-|-n}}yvpnv|{.")); // "Welcome to our application!" is encrypted
    }

    private string Decrypt(string encrypted)
    {
        // Simple Caesar cipher for demonstration
        return new string(encrypted.Select(c => (char)(c - 13)).ToArray());
    }
}

```

### Control Flow Obfuscation

This technique modifies the flow of a program to increase its complexity while keeping the output the same. It might involve adding superfluous loops, irrelevant jumps, and other perplexing constructs.

Before:

```csharp
public bool IsPasswordSecure(string password)
{
    if (password.Length >= 8)
    {
        if (HasUpperCaseLetter(password) && HasLowerCaseLetter(password))
        {
            return true;
        }
    }
    return false;
}

```

After:

```csharp
public bool IsPasswordSecure(string password)
{
    bool isSecure = false;

    do
    {
        if (password.Length < 8) break;
        if (!HasUpperCaseLetter(password)) break;
        if (!HasLowerCaseLetter(password)) break;

        isSecure = true;
    } while (false);

    return isSecure;
}

```

### String Encoding

String encoding differs from string encryption.

String encryption is the process of converting a plain text string into an unreadable format, known as ciphertext, using encryption algorithms and a secret key.

String encoding, is the process of converting a string from one character encoding scheme to another. It is used to represent characters that cannot be directly represented in a given character encoding. Common encoding schemes include UTF-8, UTF-16, ASCII, and more.

Instead of encrypting the strings, they are encoded using a reversible encoding scheme. This makes the strings harder to understand for someone inspecting the code, but the encoded strings can be easily decoded back to their original form at runtime. Base64 is a pretty common algorithm for this technique.

Before:

```csharp
public class HelloWorld
{
    public void DisplayMessage()
    {
        string message = "Hello, World!";
        Console.WriteLine(message);
    }
}

```

After:

```csharp
public class HelloWorld
{
    public void DisplayMessage()
    {
        string encodedMessage = "SGVsbG8sIFdvcmxkIQ=="; // "Hello, World!" encoded with Base64
        string plainMessage = System.Text.Encoding.UTF8.GetString(Convert.FromBase64String(encodedMessage));
        Console.WriteLine(plainMessage);
    }
}

```

### Redundant Code Insertion

This technique incorporates extraneous code that doesn't affect the program's functionality but obscures the understanding for decompilers or individuals attempting to interpret the code.

Before:

```csharp
public int SumNumbers(int num1, int num2)
{
    int sum = num1 + num2;
    return sum;
}

```

After:

```csharp
public int SumNumbers(int num1, int num2)
{
    int sum = num1 + num2;

    // Redundant code
    for (int i = 0; i < 100; i++)
    {
        sum = sum + 0;
    }

    return sum;
}

```

### Reference Indirection

This technique involves adding indirection when calling methods or accessing properties.

Before:

```csharp
public class Greeting
{
    public void ShowMessage()
    {
        Console.WriteLine("Hello, World!");
    }
}

```

After:

```csharp
public class Greeting
{
    private static Action<string> consoleOutput = (message) => Console.WriteLine(message);

    public void ShowMessage()
    {
        consoleOutput("Hello, World!");
    }
}

```

## DeObfuscation

Regrettably, at present, no comprehensive tools exist for general obfuscations. Historically, we have had tools like de4dot and UnSealer, but these projects have been archived over the years without finding active forks or substitutions. Numerous tools can handle specific commercial and open-source .NET obfuscators and obfuscation techniques on GitHub, but none cater to generic obfuscation methods.


# DnSpy

* * *

![](https://academy.hackthebox.com/storage/modules/208/dnspy.png)

DnSpy is a debugger and .NET assembly editor that allows inspection, debugging, and modification of .NET assemblies in a user-friendly environment. This versatile tool is invaluable for programmers working with .NET applications, including games developed with the Unity engine, which uses .NET (primarily C#) as its primary scripting language.

Key features of DnSpy include:

- `Assembly Editing`: DnSpy enables users to alter .NET assemblies without the source code. Methods and classes can be edited directly in the tool, automatically saving changes to the assembly file.
- `Debugging`: DnSpy contains a powerful debugger supporting managed and native code. This debugger permits setting breakpoints, stepping through code, and examining variables and memory, among other standard debugging tasks. It also supports Unity games and can attach to Unity editor processes.
- `Decompilation`: DnSpy uses the open-source ILSpy decompiler engine, letting you decompile .NET assemblies into C#, Visual Basic.NET, and even Common Intermediate Language (CIL) code.
- `Hex Editor`: DnSpy has an integrated hex editor to assist in inspecting and modifying binary data that cannot be adequately represented in text form.
- `Scripting`: DnSpy supports scripting with C# code, which can be especially useful for automating repetitive tasks.

DnSpy itself is built on top of several existing frameworks and libraries:

- `ILSpy`: The ILSpy engine is central to DnSpy's ability to decompile .NET assemblies. ILSpy is a powerful open-source decompiler that converts .NET assemblies into C# or Visual Basic.NET code, easing the understanding of the original program's logic.
- `Roslyn`: The ".NET Compiler Platform," aka `Roslyn`, provides open-source C# and Visual Basic compilers with rich code analysis APIs. DnSpy uses Roslyn for its syntax highlighting and code editing capabilities, allowing users to edit decompiled code like a standard code editor.
- `dnlib`: dnlib is a library that reads and writes .NET metadata (plus PE headers), reads IL code and creates a straightforward yet flexible representation of all metadata. Notably, it can handle obfuscated assemblies, which are often more challenging to analyse.
- `VS MEF (Managed Extensibility Framework)`: MEF offers a standard way for the application to expose extensibility points and consume extensions. DnSpy uses the version of MEF included with Visual Studio (VS MEF), optimised for faster start-up times.
- `ClrMD`: The Microsoft.Diagnostics.Runtime ( `ClrMD`) library enables programmers to programmatically access crash dump files and inspect the state of all runtime data in the dump file. DnSpy uses this to deliver lower-level debugging information unavailable through the standard CorDebug API.
- `Iced`: Iced is a high-performance and correct x86 (16/32/64-bit) instruction decoder, disassembler, and assembler written in C#. DnSpy uses Iced to decode and disassemble x86 and x64 instructions, providing detailed insights into the assembly code's operations at the machine level.

With all these features, DnSpy emerges as a powerful tool for reverse engineering and hacking .NET programs and games. It can tackle three significant challenges of the reverse engineering process:

1. `Inspecting and Understanding Code`: DnSpy can decompile .NET assemblies into C# or Visual Basic.NET code. This ability allows game hackers to study the game's logic, learn how different functions interact, and comprehend the underlying mechanics. This understanding can be helpful in modding, fixing bugs, or learning about game development.
2. `Modifying Code`: DnSpy lets game hackers edit the decompiled code directly and save the changes back into the assembly. This capability can alter game behaviour, such as adjusting game difficulty, changing character abilities, or adding new features. Any modifications should respect the game's terms of service, especially in multiplayer or online games where changes could impact other players.
3. `Debugging`: DnSpy includes a debugger that can attach to running .NET processes, including games. This debugger lets game hackers set breakpoints, step through code, and inspect variables and memory. This ability can help them understand how the game operates in real-time, identify bugs, or locate code sections for potential modifications.

## DnSpyEx

It's important to note that while DnSpy is a handy tool, the original project was abandoned in 2020. Thanks to its open-source nature, several developers promptly picked up and continued it, most notably the DnSpyEx project.

However, potential users should exercise caution when downloading DnSpy. Cybercriminals seized the brief period of confusion following the project's archival to distribute 'updated' copies infected with malware, as reported on Bleeping Computer: [Trojanized DnSpy app drops malware cocktail on researchers, devs.](https://www.bleepingcomputer.com/news/security/trojanized-dnspy-app-drops-malware-cocktail-on-researchers-devs/)

To ensure safety, it is recommended to only download the DnSpyEx version of DnSpy directly from their official GitHub page: [DnSpyEx/dnSpy.](https://github.com/dnSpyEx/dnSpy)


# Creating a Mod

* * *

Let’s look at our target game, Modman.

![](https://academy.hackthebox.com/storage/modules/208/modman.png)

It's the same Hackman game we are familiar with, except now we observe a conspicuous purple bar at the bottom of the screen. Previous techniques, such as altering scores and lives, prove fruitless. It appears we'll have to modify the game directly.

We see something we know about Unity games upon examining the game files. A comparison between Modman and Hackman reveals several differences. Hackman possesses a `GameAssembly.dll` file in the root directory and lacks a `MonoBleedingEdge` folder, while Modman has a `MonoBleedingEdge` directory and no `GameAssembly.dll`.

![](https://academy.hackthebox.com/storage/modules/208/hackman-files.png)

![](https://academy.hackthebox.com/storage/modules/208/modman-files.png)

Delving further into the `_Data` folders, we uncover additional disparities. Notably, an `il2cpp_data` folder is present in Hackman, along with an assortment of other files that are absent in Modman.

![](https://academy.hackthebox.com/storage/modules/208/hackman-data.png)

![](https://academy.hackthebox.com/storage/modules/208/modman-data.png)

As previously introduced, Hackman employs the `IL2CPP` technology offered by Unity, compiling the .NET code into native code, in contrast to Modman, which is a pure .NET Unity game. Consequently, all game logic resides within libraries in the `.\Managed` folder, and assets are stored in discrete files.

There is a strong possibility that the control mechanism for the purple blob lies within the game code. We can utilise DnSpy to delve into the `Assembly-CSharp.dll` library, which likely houses the logic governing the purple blob's control.

## Modding the game

The process for loading the `Assembly-CSharp.dll` file into DnSpy is straightforward.

1. Open DnSpy.
2. Navigate to `File` -\> `Open`.
3. Browse to the game's installation directory, then the `Managed` folder, and open \`Assembly-CSharp.dll ![](https://academy.hackthebox.com./3.3%20Creating%20a%20Mod./storage/modules/208/DnSpy-Open.png)
4. Expand the `Assembly-CSharp.dll` file in the left-hand explorer.
5. Navigate through the nested namespaces, classes, and methods. ![](https://academy.hackthebox.com./3.3%20Creating%20a%20Mod./storage/modules/208/DnSpy-Explore.png)

In the library, there are numerous namespaces. We’re currently uncertain whether the code we seek resides in a specific namespace or the root namespace. Applying good reasoning, we can safely deduce that the sought-after code won't be found within either the `CodeStage` or `AntiCheat` libraries. Towards the end, a `Common` namespace is noticeable, yet it contains nothing noteworthy.

![](https://academy.hackthebox.com/storage/modules/208/dnspy-common.png)

Expanding the root namespace, however, reveals a lot of obfuscated methods.

![](https://academy.hackthebox.com/storage/modules/208/dnspy-root.png)

Upon examination of the obfuscation, it becomes apparent that a combination of techniques has been employed. Symbol names have been modified, an excess of redundant code has been introduced, and strings are encrypted—resulting essentially in a chaotic cacophony of noise. Our task is to sift through this noise to locate what we are looking for. Notably, the obfuscator seems to be integrating obfuscated code into original class names, possibly as a strategy to preserve compatibility. Consider the code below. `GameManager` is the original class name, but it lacks content and actually inherits everything from `j`, which is highly obfuscated. In DnSpy you can hold Control and Click on a symbol to quickly navigate to its implementation.

```csharp
public sealed class GameManager : j
{
}

```

One feature that distinctly stands out is a class named `Modman`. This class doesn't utilise the previously mentioned obfuscation techniques. Instead, it comprises several methods, albeit obfuscated ones. We encounter a `Start()` method with a notable attribute upon examining these methods.

```csharp
// Token: 0x06000165 RID: 357 RVA: 0x00005D50 File Offset: 0x00003F50
[NotObfuscatedCause("Because of compatibility component: Unity - Compatibility : Is MonoBehaviour Method.")]
private void Start()
{
    this.jb();
}

```

To maintain compatibility with Unity, the obfuscator refrains from obfuscating Unity methods. This knowledge helps us significantly reduce a considerable portion of the obfuscation as we now have something traceable. The attribute section pretty much explicity tells us that. The `Runtime Hook Libraries` section will discuss this in more detail. However, for now, understand that whenever the `Modman` class, or any Unity class for that matter, is invoked, Unity automatically invokes the `Start()` method as an entry point into the class. This suggests that any obfuscated variables and methods used within `Start()` contain actual code, not junk code. In this case, `this.jb()` represents the actual method. The `jb()` method includes some intriguing lines of code.

```csharp
// Modman
// Token: 0x0600016A RID: 362 RVA: 0x00005D8E File Offset: 0x00003F8E
private void jb()
{
	this.cll = base.GetComponent<Image>();
	this.cll.enabled = true;
	this.cll.color = new Color32(36, 0, 52, byte.MaxValue);
}

```

- `this.cll = base.GetComponent<Image>();` This instruction retrieves the `Image` component linked to the same GameObject that the script is associated with and allocates it to a class-level variable called `cll`.

- `this.cll.enabled = true;` This statement activates the `Image` component. Should it have been deactivated for any reason (such as invisibility or non-interactivity), it would be reactivated.

- `this.cll.color = new Color32(36, 0, 52, byte.MaxValue);` This command adjusts the colour of the `Image` component. `Color32` is a structure embodying RGBA (Red, Green, Blue, Alpha) values, each with 8 bits. The colour is adjusted to `RGB(36, 0, 52)`, with complete alpha (transparency) owing to `byte.MaxValue` , equating to `255`, signifying complete opacity.


Right click within the method, and select the `Edit Method (C#)...` option.

![](https://academy.hackthebox.com/storage/modules/208/dnspy-edit.png)

This will open the code editor. An incredibly useful DnSpy feature that will allow us to easily edit the IL code as C#.

![](https://academy.hackthebox.com/storage/modules/208/dnspy-compiler.png)

Change the `this.cll.enabled` line to `false` and click `Compile`.

![](https://academy.hackthebox.com/storage/modules/208/dnspy-compiler-compile-error.png)

An error pops up, alerting to the duplication of attribute tags. They are unimportant and serve a more debug function at this point, so remove them. When editing assemblies using this editor, its important to note that you may need to perform quite a bit of manual work, such as including references to external libraries, correcting code errors, possibly even renaming variables. The error log will guide you through that process pretty well.

```csharp
using System;
using OPS.Obfuscator.Attribute;
using UnityEngine;
using UnityEngine.UI;

// Token: 0x02000012 RID: 18
[DoNotRename]
public partial class Modman : MonoBehaviour
{
	// Token: 0x0600016A RID: 362 RVA: 0x00005D8E File Offset: 0x00003F8E
	private void jb()
	{
		this.cll = base.GetComponent<Image>();
		this.cll.enabled = false;
		this.cll.color = new Color32(36, 0, 52, byte.MaxValue);
	}
}

```

The compiler translated the edited C# code into IL code and edited the method.

![](https://academy.hackthebox.com/storage/modules/208/dnspy-edited.png)

That was far easier than trying to understand and edit IL code...

```nasm
// Token: 0x0600016A RID: 362
.method private hidebysig
	instance void jb () cil managed
{
	// Header Size: 1 byte
	// Code Size: 56 (0x38) bytes
	.maxstack 8

	/* (13,3)-(13,41) main.cs */
	/* 0x00000000 02           */ IL_0000: ldarg.0
	/* 0x00000001 02           */ IL_0001: ldarg.0
	/* 0x00000002 28????????   */ IL_0002: call      instance !!0 [UnityEngine.CoreModule]UnityEngine.Component::GetComponent<class [UnityEngine.UI]UnityEngine.UI.Image>()
	/* 0x00000007 7D40000004   */ IL_0007: stfld     class [UnityEngine.UI]UnityEngine.UI.Image Modman::cll
	/* (14,3)-(14,28) main.cs */
	/* 0x0000000C 02           */ IL_000C: ldarg.0
	/* 0x0000000D 7B40000004   */ IL_000D: ldfld     class [UnityEngine.UI]UnityEngine.UI.Image Modman::cll
	/* 0x00000012 16           */ IL_0012: ldc.i4.0
	/* 0x00000013 6F????????   */ IL_0013: callvirt  instance void [UnityEngine.CoreModule]UnityEngine.Behaviour::set_enabled(bool)
	/* (15,3)-(15,58) main.cs */
	/* 0x00000018 02           */ IL_0018: ldarg.0
	/* 0x00000019 7B40000004   */ IL_0019: ldfld     class [UnityEngine.UI]UnityEngine.UI.Image Modman::cll
	/* 0x0000001E 1F24         */ IL_001E: ldc.i4.s  36
	/* 0x00000020 16           */ IL_0020: ldc.i4.0
	/* 0x00000021 1F34         */ IL_0021: ldc.i4.s  52
	/* 0x00000023 20FF000000   */ IL_0023: ldc.i4    255
	/* 0x00000028 73????????   */ IL_0028: newobj    instance void [UnityEngine.CoreModule]UnityEngine.Color32::.ctor(uint8, uint8, uint8, uint8)
	/* 0x0000002D 28????????   */ IL_002D: call      valuetype [UnityEngine.CoreModule]UnityEngine.Color [UnityEngine.CoreModule]UnityEngine.Color32::op_Implicit(valuetype [UnityEngine.CoreModule]UnityEngine.Color32)
	/* 0x00000032 6F????????   */ IL_0032: callvirt  instance void [UnityEngine.UI]UnityEngine.UI.Graphic::set_color(valuetype [UnityEngine.CoreModule]UnityEngine.Color)
	/* (16,2)-(16,3) main.cs */
	/* 0x00000037 2A           */ IL_0037: ret
} // end of method Modman::jb

```

Next, we need to save the changes into the game files. Click the file menu, and select the `Save Module...` option.

![](https://academy.hackthebox.com/storage/modules/208/dnspy-filemenu.png)

This will open the `Save Module` dialogue that offers various options to save the module. We do not need to change anything, so click `Ok`. This will cause DnSpy to replace the original `Assembly-CSharp.dll` file with our mod.

![](https://academy.hackthebox.com/storage/modules/208/dnspy-save-module.png)

Run Modman again, and we can immediately see that the purple blob has disappeared, and we have the flag to solve the assignment.

![](https://academy.hackthebox.com/storage/modules/208/modman-mod.png)

Enable step-by-step solutions for all questions
![sparkles-icon-decoration](https://academy.hackthebox.com/images/sparkles-solid.svg)

#### Questions

Answer the question(s) below
to complete this Section and earn cubes!

\+ 15  What is the text hiding behind the purple block?


Submit


[Modman.zip](/storage/modules/208/Modman.zip)


# External vs Internal Game Hacks

* * *

In game hacking, two primary methods exist: external techniques like memory editing and internal methods such as code injection.

## External Game Hacks

External game hacks function outside the game process. Instead of injecting code, these hacks scrutinise and modify the game's memory from a separate process.

### How External Hacks Work

External hacks operate by reading the game's memory from an external process, identifying pertinent information (such as player health or locations), and writing new data to the memory, thus providing the hacker with an advantage. This method avoids any code injection into the game's process.

### Examples of External Hacks

1. `Trainer`: A trainer is an independent application that modifies a running game's data. Trainers usually come with a user interface that allows users to toggle specific hacks on or off. For instance, a racing game's trainer might empower users to freeze their lap times, obtaining an unbeatable time.
2. `Memory Editing`: Memory editing utilises tools like Cheat Engine to scan and amend game memory. A hacker might, for example, use a memory editor to locate and modify the value representing a player's health or ammunition in a first-person shooter game.
3. `Scripts`: Scripts are fragments of code that can be executed with third-party tools to modify game functions. They are commonly used to automate specific actions. For example, in a multiplayer online game, a script could automate a player's sequence of attacks, such as managing a gun’s recoil, making them more proficient in battles.
4. `Save Game Editors`: Save game editors allow players to alter saved game files, tweaking the game state to the player's advantage. Players might use a save game editor to escalate their character's level, add items to their inventory, or change their in-game currency in a role-playing game.

## Internal Game Hacks

Internal game hacks operate within the game process. They typically involve injecting a Dynamic Link Library (DLL) into the game's process memory. This DLL generally contains code that alters the game's functions or data to give the hacker an advantage.

### How Internal Hacks Work

Internal hacks operate by modifying the game from within. Typically, a programmer creates a DLL containing the hack and utilises a program to inject this DLL into the game's memory. Once inside, it can directly alter the game's variables, functions, and objects.

### Examples of Internal Hacks

1. `Aimbot`: An aimbot adjusts the game's aiming mechanisms to enable the player to target enemies, often automatically attaining perfect accuracy. Aimbots generally work by scanning the game's memory for other players' coordinates and then automatically shifting the player's aim to target these coordinates.
2. `Wallhack`: A wallhack alters game data to render walls and other solid objects transparent or highlight enemies through these objects. This allows players to spot enemies through walls, granting a significant advantage in games where positioning and cover are crucial.
3. `Code Injection`: This is an internal hack where new code is injected into the game's process, usually through a DLL (Dynamic Link Library). Code injection, for instance, could allow players to teleport their character to any location in an online role-playing game, providing them with a considerable advantage.
4. `Modding Game Files`: Modding game files often necessitate internal access to the game's data. It involves altering the game's files to modify game behaviour. For example, a player might change the game files to introduce new skins or models not included in the original game.

## Differences, Pros, and Cons

The main distinction between these two types of hacks lies in their approach: internal hacks inject code into the game's process, whereas external hacks manipulate the game's memory from a different process.

|  | External Hacks | Internal Hacks |
| --- | --- | --- |
| Pros | `Less Detectable`: Since no code is injected into the game, these hacks are harder for anti-cheat mechanisms to spot. | `Greater Control`: Having direct access to the game's objects, functions, and variables allows for more manipulation possibilities, such as auto-aim features or making walls transparent. |
|  | `Safer`: They pose a lower risk of causing game crashes or performance issues as they don't modify the game's internal code. | `Advanced Capabilities`: Can implement complex hacks requiring deeper interaction with game code, like artificially enhancing game performance. |
| Cons | `Limited Control`: Their capability is constrained by what they can read and write in the game's memory, thus providing less control. They can perform simple tasks such as adjusting a player's health or ammo. | `Detectability`: By injecting DLLs into the game's process, they leave a footprint, making them easier for anti-cheat software to spot. |
|  | `Slower Performance`: They might need to scan the game's memory repeatedly, potentially leading to slower performance than internal hacks. | `Risk of Crashes`: If executed improperly, their intrusive nature can lead to game instability and crashes. |


# Software Libraries

* * *

## Understanding Binaries

A `binary` denotes two interconnected yet distinct concepts:

1. A `Binary file`: This file encapsulates data in a format not designed for human interpretation. It comprises binary data, signifying that it consists of a byte series.
2. `Executable Binaries`: In software, a binary or binary executable is a category of file primed for execution or running as a program within a particular operating system. This implies it has been compiled from source code into machine code directly executable by computer hardware.

On the Windows operating system, executable binaries, more commonly known as Portable Executable (PE) files, are a specific format adopted across 32-bit and 64-bit versions. PE files, encompassing executable ( `.exe`) files and dynamic link libraries ( `.dll`), are structured to instruct the Windows operating system on managing the executable code they contain. PE files comprise various sections, such as `.text`, `.data`, `.rsrc`, and `.reloc`, each accommodating different types of data related to the executable.

In the Linux operating system, the counterpart to Windows' PE files is ELF (Executable and Linkable Format) files. These files perform a function similar to PE files, offering a format for executables, object code, shared libraries, and even core dumps. They can accommodate 32-bit and 64-bit executable code, facilitating the creation of universal binaries capable of running on 32-bit and 64-bit platforms. ELF files are crafted to be flexible and extensible, encompassing a file header that delineates the file's structure, succeeded by data described by the file header.

The equivalent in the macOS operating system is called Mach-O (Mach Object) files. Like PE and ELF, Mach-O represents a format for executables, object code, and dynamic shared libraries. A distinguishing feature of Mach-O files is their support for "universal binaries" or "fat binaries". Within a single file, these binary files contain executable code for multiple architectures (such as i386, x86\_64, and ARM). This enables developers to build applications capable of running on different types of hardware using a single binary file.

Wikipedia has a great resource detailing the differences of a wide range of [executable file formats](https://en.wikipedia.org/wiki/Comparison_of_executable_file_formats).

## What is a Software Library

A software library is a collection of pre-compiled routines or classes a program can use. These routines, sometimes referred to as `functions` or `methods`, act as building blocks for software development, enabling developers to execute common tasks without needing to write the same code repeatedly.

Software libraries can be static or dynamic, depending on their linking to a program. They are utilised for various reasons, including:

1. `Code Reuse`: Libraries enable developers to write code once and reuse it across multiple applications or different parts of the same application, fostering efficiency and consistency.
2. `Abstraction`: Libraries offer a set of high-level interfaces, enabling developers to perform intricate tasks without delving into the underlying details.
3. `Modularity`: Libraries promote modular design, as each one can provide specific functionality that, when combined, creates more complex applications.

When a program requires a function provided by a library, it calls that function. The process varies based on the type of library (static or dynamic):

1. `Static Libraries`: These are linked to a program during compile time. The library's code is included in the final executable of the program. Static libraries are typically used when the library's code is constant or when the program will utilise the entire library.
2. `Dynamic Libraries`: These are linked to a program during runtime. The library's code is not included in the final executable; instead, the code is loaded from the library file as required. Dynamic libraries are typically used when the library's code may change or when only a fraction of its functions will be used by the program.

## Libraries on macOS and Linux

Dynamic libraries play a crucial role on macOS and Linux systems, similar to DLLs in Windows. However, on these platforms, they are typically termed shared libraries.

### Shared Libraries on macOS

On macOS, shared libraries manifest as `.dylib` (dynamic library) files. They operate in a manner akin to DLLs on Windows, containing shared code usable by multiple applications.

For instance, if you were developing a program in C or C++ on macOS, you might employ the `printf` function from the C standard library to print output to the console. Here's an example:

```c
#include <stdio.h>

int main() {
   printf("Hello, World!");
   return 0;
}

```

In this code, `printf` is a function offered by the `stdio.h` library, which is part of the C standard library. When you compile this program, the compiler links your code with the `stdio.h` library, enabling your program to use the `printf` function.

### Shared Libraries on Linux

Shared libraries typically appear on Linux as `.so` (shared object) files. These libraries contain code that can be shared among multiple programs.

Consider an example where you're developing a Python program that employs the `math` library to compute a square root:

```python
import math

print(math.sqrt(16))

```

In this code, `sqrt` is a function offered by the `math` library. When you run this Python program, the Python interpreter loads the `math` library, enabling your program to use the `sqrt` function.

## Dynamic Link Libraries (DLLs)

`DLLs`, or Dynamic Link Libraries, are integral to Windows development. As mentioned earlier, DLLs are a type of dynamic library that several applications can use concurrently, offering a method to modularise code and promote reuse.

DLLs are binary files containing code and data in a format that both the Windows operating system and applications can interpret. When you develop software using a language such as C++, you compile your source code into a DLL file, which can then be loaded and executed by an application or the operating system.

Applications typically interact with DLLs by 'calling a function'. A DLL file houses functions and blocks of code that perform specific tasks. An application can 'call' these functions, indicating a request to execute the function’s task. The DLL then performs the task and returns the result to the application.

A crucial aspect to remember while working with DLLs is dependency management. If an application relies on a DLL, that DLL must be available for the application to function correctly. Missing or incompatible DLL files can lead to a state known as "DLL Hell", – where applications can't run or behave erratically due to absent or incompatible DLLs.

Consider two applications, `App A` and `App B`, installed on the same `Windows` machine. Both applications rely on a common Dynamic Link Library (DLL) named `Library.dll` for proper functioning.

Initially, `App A` is installed and utilises `Library.dll` version `1.0`. `App A` operates perfectly with this DLL version.

Subsequently, `App B` is installed. This application requires `Library.dll` version `2.0` for correct operation. App B replaces Library.dll version 1.0 with version 2.0 as part of its installation.

Now, `App B` functions as intended because it has the required version of `Library.dll`. However, `App A` starts to malfunction because `Library.dll` version `2.0` isn't backwards compatible with version `1.0`, which `App A` was designed to work with.

To rectify the issue with `App A`, a user might reinstall it, which also reinstalls `Library.dll` version `1.0`. This action, in turn, leads to `App B` malfunctioning, as it now lacks the necessary DLL version. Welcome to DLL Hell. Nowadays, the issue isn't as pronounced as it was in previous decades, but it can still arise occasionally.

DLLs can be loaded in two ways:

1. `Load-time Dynamic Linking`: When the application is run, the operating system loads the DLL into memory. The application carries a list of DLLs it requires, which the operating system uses to locate and load the necessary DLLs.
2. `Run-time Dynamic Linking`: An application loads the DLL while running, using the Windows API function `LoadLibrary`. This method provides more flexibility, enabling the application to dictate when a DLL is loaded and control what happens if a DLL can't be found.

The idea of utilising libraries for sharing code and features is a global concept. This concept exists across all major operating systems, including `Windows`, `macOS`, and `Linux`. Libraries offer a handy method to broaden an application's functionality while encouraging code reuse and modularity.

## DLL Injection

`DLL Injection` serves as a method for executing arbitrary code within the address space of another process by compelling it to load a dynamic-link library (DLL). Once loaded, the DLL can execute its designated code, thereby modifying the behaviour of the targeted process.

This technique finds frequent application in game hacking to introduce a myriad of previously non-existent functionalities:

- `Code Modification`: Hackers often employ DLL injection to alter the game's code or data to gain undue advantages like infinite health, additional resources, or wallhack capabilities, giving the player the ability to see targets through physical objects in the game world, like walls
- `Automation`: Certain hacks aim to automate specific game tasks such as aiming (referred to as "aimbots") or resource farming (generally referred to as “botting”). A DLL can be injected to interface with the game's code and facilitate these operations.
- `Bypassing Anti-Cheat`: Modern games frequently incorporate anti-cheat software to identify game modifications. DLL injection can be used to disable or circumvent these protective measures, as you will gain a certain level of control over the anti-cheat code that runs inside the game by injecting custom code.

`DLL Hijacking` is a specialised form of DLL injection in which an attacker inserts a malicious Dynamic Link Library (DLL) into a directory scanned by the targeted software when it requires a library. If the new DLL is discovered before the legitimate one, it is loaded into the process.

For details on DLL Injection and DLL Hijacking techniques, refer to the **DLL Injection** section in the [Windows Privilege Escalation module.](https://academy.hackthebox.com/module/details/67)


# C\# Events and Attributes

* * *

This section is a short extension of the [Introduction to C#](https://academy.hackthebox.com/module/details/228) module to cover two concepts important for the following content.

## Delegates & Events

In C#, `events` and `delegates` are fundamental concepts that facilitate a communication pattern between objects, often referred to as the `observer pattern`. This pattern allows one object (the publisher) to notify other objects (subscribers) when a specific event occurs.

A delegate is a type-safe function pointer, i.e., it holds a reference to a method. However, unlike normal function pointers, delegates are object-oriented and type-safe, so the compiler ensures that the method signature matches the delegate declaration.

A delegate can reference both static and instance methods, and when a delegate is invoked, it calls the method(s) it references.

```csharp
// Define a delegate
public delegate void MyDelegate(string message);

// A method that matches the delegate signature
public void DisplayMessage(string message)
{
    Console.WriteLine(message);
}

// Instantiate the delegate.
MyDelegate handler = DisplayMessage;

// Call the delegate.
handler("Hello World");

```

In the above example, the delegate `MyDelegate` encapsulates the method `DisplayMessage`. When `handler` is invoked on the last line, it calls `DisplayMessage`.

A delegate can reference multiple methods, not just one. When invoked, it calls all the methods it references in the order they were added. Such delegates are called `multicast delegates`.

```csharp
public delegate void MyDelegate(string message);

// Create two methods for the delegate.
public static void DelegateMethod1(string message)
{
    Console.WriteLine("First method: " + message);
}

public static void DelegateMethod2(string message)
{
    Console.WriteLine("Second method: " + message);
}

// Instantiate the delegate.
Del handler = DelegateMethod1;
handler += DelegateMethod2;

// Call the delegate.
handler("Hello World");

```

In this example, the `handler` delegate references both `DelegateMethod1` and `DelegateMethod2`. When invoked, it calls both methods in the order they were added. The `+=` operator is used to subscribe a method to an event. When the event is raised, all subscribed methods are called. Conversely, the `-=` operator can be used to unsubscribe a method from an event.

### Events

An event in C# is a way for a class to notify clients of that class when something interesting happens to an object. The most familiar use for events is in graphical user interfaces; typically, the classes that represent controls in the interface have events that are notified when the user does something to the control (for example, click a button).

Events are a special kind of multicast delegate that can only be invoked from within the class or struct where they are declared (the publisher class). If other classes or structs subscribe to the event, their event handler methods will be called when the publisher class raises the event.

```csharp
public class Publisher
{
    // Define an event based on the delegate
    public event MyDelegate MyEvent;

    // Trigger the event
    public void RaiseEvent(string message)
    {
        MyEvent?.Invoke(message);
    }
}

public class Subscriber
{
    public void SubscribeToEvent(Publisher pub)
    {
        // Subscribe to the event
        pub.MyEvent += Display;
    }

    private void Display(string message)
    {
        Console.WriteLine("Received: " + message);
    }
}

```

In the above example, the `Subscriber` class subscribes to the `MyEvent` event of the `Publisher` class. When the `RaiseEvent` method of the `Publisher` class is called, it triggers the `MyEvent` event, and the `Display` method of the `Subscriber` class gets executed.

```csharp
using System;

// Define a delegate
public delegate void MyDelegate(string message);

public class Publisher
{
    // Define an event based on the delegate
    public event MyDelegate MyEvent;

    // Trigger the event
    public void RaiseEvent(string message)
    {
        MyEvent?.Invoke(message);
    }
}

public class Subscriber
{
    public void SubscribeToEvent(Publisher pub)
    {
        // Subscribe to the event
        pub.MyEvent += Display;
    }

    private void Display(string message)
    {
        Console.WriteLine("Received: " + message);
    }
}

public class Program
{
    public static void Main()
    {
        Publisher publisher = new Publisher();
        Subscriber subscriber = new Subscriber();

        // Subscriber subscribes to the publisher's event
        subscriber.SubscribeToEvent(publisher);

        // Publisher raises the event
        publisher.RaiseEvent("Hello, World!");
    }
}

//// ouputs the following when run
// Received: Hello, World!

```

In the above example, the `Subscriber` class subscribes to the `MyEvent` event of the `Publisher` class using the `+=` operator. When the `RaiseEvent` method of the `Publisher` class is called, the `MyEvent` event is triggered, which in turn calls the `Display` method of the `Subscriber` class.

## Attributes

Attributes are a powerful feature in C# that can add `metadata`, `annotations`, or `declarative information` to code elements, such as `types`, `methods`, `properties`, or `parameters`. They allow developers to attach additional information to code entities, which can be utilised by compilers, runtime environments, or other tools during compilation, execution, or at design time.

Attributes can be applied to code elements by enclosing them in square brackets ( `[ ]`) above the target element.

```csharp
[Serializable]
public class MyClass
{
    [Obsolete("This method is deprecated. Use the NewMethod() instead.")]
    public void OldMethod()
    {
        // Method implementation
    }
}

```

In the above example, the `Serializable` attribute is applied to the `MyClass` class, and the `Obsolete` attribute is applied to the `OldMethod` method.

The `Serializable` attribute is used to mark a class or a struct as serializable, indicating that instances of this type can be serialized and deserialized. Serialization is the process of converting an object or data structure into a format that can be easily stored or transmitted, and later reconstructed. Deserialization is the reverse process: converting serialized data back into an object or data structure.

The `Obsolete` attribute marks types, methods, properties, fields, events, or other members as obsolete, meaning they are outdated or will be removed in future codebase versions. When a member is marked as obsolete, the C# compiler will issue a warning or error when that member is used, depending on how the attribute is configured.


# Runtime Hook Libraries

* * *

A runtime hook is a software component or framework that enables the interception and modification of function calls at runtime. It allows developers or hackers to insert custom code or "hooks" into a running program, intercepting specific function calls and altering their behaviour according to their needs.

Hooking refers to a technique used to intercept and modify the behaviour of a software application or system. It involves redirecting the flow of execution within a program to inject custom code that can monitor, manipulate, or extend its functionality. Security researchers, software developers, and malicious actors commonly employ this powerful technique for various purposes.

Typically, a runtime hook library provides a set of functions and utilities that facilitate the process of hooking into target applications. These libraries often utilise low-level techniques, such as code injection or dynamic code modification, to intercept and redirect function calls to custom code snippets.

Many very powerful hooking frameworks cover basically every platform. Here are a few notable ones:

1. `Detours`: Developed by Microsoft Research, Detours is a widely used library for hooking functions on Windows systems.
2. `MinHook`: a lightweight and efficient hooking library for Windows systems. It supports x86 and x64 architectures and allows developers to easily intercept and redirect function calls. MinHook provides a simple and intuitive interface, making it popular among developers seeking a straightforward hooking solution.
3. `ShadowHook`: an Android inline hook library developed by ByteDance. It supports both arm32 and arm64, and is used in popular apps such as TikTok.

## Microsoft Detours

Microsoft Detours is a library for instrumenting arbitrary Win32 functions on x86, x64, and ARM machines. It allows you to intercept ("detour") function calls in a running application, inject custom functionality, monitor function calls, or even replace the original function with a different implementation.

The Detours library uses a technique called "trampoline functions" to safely intercept function calls. Here's a simplified overview of how it works:

1. `Function Identification`: The target function that you want to detour is identified. This could be a Windows API function like `CreateFile` or a function in a user-defined DLL.
2. `Trampoline Creation`: Detours generate a trampoline function that mimics the target function. This trampoline function will call the original function while allowing you to insert custom code before or after the call.
3. `Detour Attachment`: Detours modify the first few bytes of the target function to redirect (or "jump") to your custom function. This is the actual "detour."
4. `Custom Function`: Your custom function can then perform its operations and call the trampoline function to execute the original function.
5. `Detour Removal`: The detour can be removed, restoring the original function's bytes.

```c++
#include <Windows.h>
#include <stdio.h>
#include "detours.h"

// Original MessageBoxW function pointer
typedef int(WINAPI* MessageBoxW_t)(HWND, LPCWSTR, LPCWSTR, UINT);
MessageBoxW_t pOrigMessageBoxW = MessageBoxW;

// Detour function
int WINAPI MyMessageBoxW(HWND hWnd, LPCWSTR lpText, LPCWSTR lpCaption, UINT uType) {
    return pOrigMessageBoxW(hWnd, L"Detoured!", lpCaption, uType);
}

int main() {
    // Attach the detour
    DetourTransactionBegin();
    DetourUpdateThread(GetCurrentThread());
    DetourAttach(&(PVOID&)pOrigMessageBoxW, MyMessageBoxW);
    DetourTransactionCommit();

    // Call MessageBoxW to test the detour
    MessageBoxW(NULL, L"Original Message", L"Hello", MB_OK);

    // Detach the detour
    DetourTransactionBegin();
    DetourUpdateThread(GetCurrentThread());
    DetourDetach(&(PVOID&)pOrigMessageBoxW, MyMessageBoxW);
    DetourTransactionCommit();

    return 0;
}

```

When the example above is run, a message box will appear, but instead of displaying "Original Message," it will display "Detoured!"

## BepInEx

`BepInEx` is a popular [open-source](https://github.com/BepInEx/BepInEx) framework and plugin loader designed for modding support in Unity-based games. At its core, `BepInEx` acts as a modding platform by providing a runtime environment that allows plugins to be loaded and executed within a target game. It offers a plugin loader that integrates with the game's code and enables the injection and execution of custom code at runtime. This allows modders to alter various aspects of the game, such as gameplay mechanics, graphics, and user interface, or introduce new content.

`BepInEx` utilises hooking techniques to intercept and modify the game's execution flow. It hooks into specific game systems, allowing developers to inject custom code and alter the game’s behaviour. By intercepting these hooks, `BepInEx` can extend and enhance game functionality without directly modifying the game's source code.

Getting `BepinEx` setup is pretty straightforward. Download the [latest Bleeding edge build](https://builds.bepinex.dev/projects/bepinex_be), appropriate for the game runtime (IL2CPP, Mono, etc), and drop it into the game folder.

![](https://academy.hackthebox.com/storage/modules/208/Hookman-BepInstall.png)

The software is very unstable, so you may need to try older versions if the latest version doesn’t work. You will know BepInEx has been successfully installed, as the next time you run the game, the BepinEx Console will open.

![](https://academy.hackthebox.com/storage/modules/208/Hookman-Hook.png)

In general, if you have tried all BepInEx versions and none of them will successfully hook, it is likely that your antivirus is blocking the behavior, the game has an anti-cheat that is preventing the hooking, or the game has been stripped, removing functions that BepInEx requires. This won't be specifically explored in this module.

Next we need to setup a C# `classlib` for BepInEx to inject into Hookman. Also we will create a `Mod` folder for the library code as a subfolder in the `Hookman` directory, and then run `dotnet new classlib` in that folder to create the project, allowing us to easily reference the required BepinEx and game libs from the parent directory.

```xml
<Project Sdk="Microsoft.NET.Sdk">

  <PropertyGroup>
    <TargetFramework>netstandard2.1</TargetFramework>
    <ImplicitUsings>enable</ImplicitUsings>
    <Nullable>enable</Nullable>
    <LangVersion>latest</LangVersion>
  </PropertyGroup>
  <!-- reference all libraries in the libs folder -->
  <ItemGroup>
    <Reference Include="$(MSBuildProjectDirectory)\..\BepInEx\core\*.dll" />
    <Reference Include="$(MSBuildProjectDirectory)\..\Hookman_Data\Managed\Assembly-CSharp.dll" />
    <Reference Include="$(MSBuildProjectDirectory)\..\Hookman_Data\Managed\Unity.*.dll" />
    <Reference Include="$(MSBuildProjectDirectory)\..\Hookman_Data\Managed\UnityEngine.dll" />
    <Reference Include="$(MSBuildProjectDirectory)\..\Hookman_Data\Managed\UnityEngine.*.dll" />

  </ItemGroup>
  <Target Name="CopyDll" AfterTargets="Build">
    <Copy SourceFiles="$(OutputPath)\Mod.dll"
      DestinationFolder="$(MSBuildProjectDirectory)\..\BepInEx\plugins" />
  </Target>
</Project>

```

Your final directory structure should look something like this:

```
.\Hookman\BepInEx\
.\Hookman\BepInEx\cache\
.\Hookman\BepInEx\config\
.\Hookman\BepInEx\core\
.\Hookman\BepInEx\patchers\
.\Hookman\BepInEx\plugins\
.\Hookman\Hookman_Data\
.\Hookman\Hookman_Data\Managed
.\Hookman\Mod\
.\Hookman\Mod\Class1.cs
.\Hookman\Mod\Mod.csproj
.\Hookman\Mod\Mod.sln
.\Hookman\doorstop_config.ini
.\Hookman\Hookman.exe
.\Hookman\winhttp.dll

```


# Building a Runtime Hook

* * *

### Getting a list of GameObjects and Scenes

The first thing to do when planning a BepInEx mod is to get an idea of the game itself, specifically what `GameObjects` exist and what `Scenes` they exist in. `GameObjects` are the building blocks for scenes in Unity and act as a container for functional components that determine how the `GameObject` looks and how the `GameObject` behaves. On the other hand, `Scenes` store a collection of `GameObjects`, assets, and other elements that make up a specific portion of your game.

The [GameObject class](https://docs.unity3d.com/ScriptReference/GameObject.html) provides a collection of methods which allow you to work with them in your code, including finding, making connections and sending messages between `GameObjects`, adding or removing components attached to the `GameObject`, and setting values relating to their status within the scene.

`GameObject` is inherited from `Object`, and `Object` provides a nifty function to find all objects of a specific type: [Object.FindObjectOfType](https://docs.unity3d.com/ScriptReference/Object.FindObjectOfType.html).

Likewise, `Scenes` have the [SceneManagement](https://docs.unity3d.com/ScriptReference/SceneManagement.SceneManager.html) namespaces that expose several classes for working with Scenes, namely `SceneManager` and `SceneUtility`. The `SceneUtility.GetScenePathByBuildIndex` function behaves very similarly to the `FindObjectOfType`, when called for a `Scene` index, it will return a `Scene` path such as `Assets/Scenes/Scene1.unity`

Using those functions, we can then loop through and log every `GameObject` in the game as well as get a list of named scenes.

Because our game is Mono, we will inherit the `BaseUnityPlugin` class from `BepInEx.Unity.Mono` which in turn, is an inherited `MonoBehavior` class. As it is a `MonoBehavior` class, we can utilise the same functions Unity uses, such as `Awake()` and `Update()`.

```csharp
namespace BepInEx.Unity.Mono
{
    public abstract class BaseUnityPlugin : MonoBehaviour
    {
        protected BaseUnityPlugin();

        public PluginInfo Info { get; }
        public ConfigFile Config { get; }
        protected ManualLogSource Logger { get; }
    }
}

```

### MonoBehavior

The `MonoBehaviour` class is a fundamental component that serves as the base class for scripting in Unity. It provides a framework for creating scripts that can be attached to game objects to define their behaviour and functionality. The `MonoBehaviour` class contains numerous built-in methods that can be overridden to implement specific behaviours and respond to various events throughout the lifecycle of a game object.

`MonoBehaviour` provides methods that are automatically called at different stages of a game object's lifecycle. These methods include `Awake()`, `Start()`, `Update()`, `FixedUpdate()`, `LateUpdate()`, and more. Controlling the initialisation, updating, and rendering of game objects is possible by overriding these methods. `MonoBehaviour` also enables event handling, such as collisions, triggers, input, and GUI rendering. Methods such as `OnCollisionEnter()`, `OnTriggerEnter()`, `OnMouseDown()`, `OnGUI()`, and many others can be overridden to respond to specific events and trigger corresponding actions in the game.

From those listed methods, there are a couple of take note of:

- `Awake()`: The `Awake()` method is called when a `GameObject` is first instantiated. It is executed before the `Start()` method and is used to perform one-time setup tasks and prepare the initial state of game objects. This method is particularly useful for setting up references between scripts and ensuring that necessary connections are established before the object becomes active in the game or scene.
- `Start()`: The `Start()` method is called once, after the `Awake()` method, when a script is initialised or enabled. It is executed at the beginning of the first frame when the object becomes active in the game or scene. This method is commonly used for further initialisation tasks and preparing the initial state of game objects, such as setting up initial behaviours, configuring components, or performing additional setup operations that need to be executed before the game or scene begins.
- `Update()`: The `Update()` method is a frequently used method that is called every frame. It is responsible for handling real-time updates and is crucial for implementing game logic. In this method, you can check for user input, update object positions, control animations, and manage various game states. The `Update()` method allows you to create dynamic and interactive experiences by continuously responding to changes in the game environment.
- `FixedUpdate()`: While the `Update()` method is called every frame, the `FixedUpdate()` method is called at fixed time intervals. It is specifically designed for handling physics-related calculations and should be used when modifying `Rigidbody` components or implementing precise object movement. Since the physics calculations can vary depending on the frame rate, the `FixedUpdate()` method ensures consistent simulation regardless of the fluctuations in the frame.
- `LateUpdate()`: The `LateUpdate()` method is called after all `Update()` methods have been executed. It is useful for performing actions that need to take place after object updates. Since `LateUpdate()` is called at the end of the frame, you can ensure that all object transformations and animations have already been processed in the current frame before performing additional operations.
- `OnSceneLoaded()`: A callback function that is automatically called whenever a new scene is loaded. It is a part of Unity's `SceneManager ` class.

Those methods are essentially the building blocks of all Unity code.

So for our mod, we will use the `Start()` `MonoBehavior` method and `OnSceneLoaded` from the `SceneManager`. Consider the following code:

```csharp
using BepInEx;
using BepInEx.Unity.Mono;

namespace GameMod;
// defined under the namespace, as to override System.Object with UnityEngine.Object
using UnityEngine;
using UnityEngine.SceneManagement;

// defines BepInEx plugin info
[BepInPlugin("GH", "GameMod", "1.0.0")]
public class GameMod : BaseUnityPlugin
{
    public void Start()
    {
        GetSceneNames();
    }

    /// <summary>
    /// Recursively prints the name of a GameObject and its children with an increasing depth of indentation.
    /// </summary>
    /// <param name="gObject">The GameObject to print.</param>
    /// <param name="depth">The current depth of the GameObject in the hierarchy.</param>
    void PrintGameObjectAndChildren(GameObject gObject, int depth)
    {
        string indent = new string('-', depth);
        Debug.Log(indent + "Object: " + gObject.name);
        foreach (Transform child in gObject.transform)
        {
            PrintGameObjectAndChildren(child.gameObject, depth + 1);
        }
    }

    /// <summary>
    /// Gets the names of all scenes in the build settings and logs them using the Logger class.
    /// </summary>
    public void GetSceneNames()
    {
        List<string> sceneNames = new List<string>();
        for (int i = 0; i < SceneManager.sceneCountInBuildSettings; i++)
        {
            string scenePath = SceneUtility.GetScenePathByBuildIndex(i);
            string sceneName = Path.GetFileNameWithoutExtension(scenePath);
            sceneNames.Add(sceneName);
        }
        Logger.LogInfo("Scenes in build settings: " + string.Join(", ", sceneNames.ToArray()));
    }

    /// <summary>
    /// Called when the script instance is being loaded.
    /// </summary>
    private void OnEnable()
    {
        // Register the event listener when the script is enabled
        SceneManager.sceneLoaded += OnSceneLoaded;
    }

    /// <summary>
    /// Called when the MonoBehaviour is disabled.
    /// </summary>
    private void OnDisable()
    {
        // Unregister the event listener when the script is disabled
        SceneManager.sceneLoaded -= OnSceneLoaded;
    }

    /// <summary>
    /// This method is called every time a new scene is loaded.
    /// </summary>
    /// <param name="scene">The scene that was loaded.</param>
    /// <param name="mode">The mode in which the scene was loaded.</param>
    private void OnSceneLoaded(Scene scene, LoadSceneMode mode)
    {
        // This code will run every time a new scene is loaded
        Logger.LogInfo("Scene loaded: " + scene.name);
        // Call any other functions you want to run when the scene changes
        // loop through every game object in the scene
        foreach (var gObject in scene.GetRootGameObjects())
        {
            // print the name of the game object and all of its children, starting at depth 0
            PrintGameObjectAndChildren(gObject, 0);
        }
    }
}

```

The code can be broken down as follows.

```csharp
using BepInEx;
using BepInEx.Unity.Mono;

```

These lines import the `BepInEx` namespace and its sub-namespace `Unity.Mono`.

```csharp
namespace GameMod;

```

This line declares a new namespace named `GameMod`. Any class or type within this block will be under the `GameMod` namespace.

```csharp
using UnityEngine;
using UnityEngine.SceneManagement;

```

These lines import the `UnityEngine` and `UnityEngine.SceneManagement` namespaces. These are from Unity's API and provide access to core game functionalities and scene management, respectively.

```csharp
[BepInPlugin("GH", "GameMod", "1.0.0")]

```

This is an attribute that defines the plugin's metadata for `BepInEx`. It signifies that the following class is a BepInEx plugin with an `ID` of "GH", a `name` of "GameMod", and a `version` "1.0.0". These can be anything appropriate for your project.

```csharp
public class GameMod : BaseUnityPlugin

```

This line declares a new public class named `GameMod` that inherits from `BaseUnityPlugin`, which will, as we know, extend `MonoBehavior`.

```csharp
public void Start()
{
    GetSceneNames();
}

```

This method is automatically called by Unity when a script is first initialised. Here, it calls the `GetSceneNames` method.

```csharp
void PrintGameObjectAndChildren(GameObject gObject, int depth)
    {
        string indent = new string('-', depth);
        Debug.Log(indent + "Object: " + gObject.name);
        foreach (Transform child in gObject.transform)
        {
            PrintGameObjectAndChildren(child.gameObject, depth + 1);
        }
    }

```

This method recursively logs the name of a `GameObject` and its children. It's a simple way to print out a hierarchy of game objects.

```csharp
public void GetSceneNames()
{
...
    for (int i = 0; i < SceneManager.sceneCountInBuildSettings; i++)
    {
        string scenePath = SceneUtility.GetScenePathByBuildIndex(i);
        string sceneName = Path.GetFileNameWithoutExtension(scenePath);
        sceneNames.Add(sceneName);
    }
...
}

```

This method retrieves the names of all scenes listed in the game's build settings and logs them. It does so by iterating over each scene in the build settings, getting its path, extracting its name, and then storing it in a list.

This for-loop iterates over all the scenes that are added to the game's build settings. `SceneManager.sceneCountInBuildSettings` gives the number of such scenes. For each iteration of the loop (i.e., for each scene in the build settings), `GetFileNameWithoutExtension` gets the scene file path using its build index. The build index is a unique identifier for each scene in the order they're listed in the build settings.

```csharp
private void OnEnable()
{
    SceneManager.sceneLoaded += OnSceneLoaded;
}

private void OnDisable()
{
    SceneManager.sceneLoaded -= OnSceneLoaded;
}

```

These methods are special Unity callbacks. The `OnEnable` method registers the `OnSceneLoaded` method to the `sceneLoaded` event, so when a scene is loaded, `OnSceneLoaded` is called. The `OnDisable` method does the opposite, unregistering the event listener to ensure that the code doesn't keep trying to execute even after this script is disabled or destroyed.

```csharp
private void OnSceneLoaded(Scene scene, LoadSceneMode mode)
{
...
    foreach (var gObject in scene.GetRootGameObjects())
    {
        PrintGameObjectAndChildren(gObject, 0);
    }
}

```

The method has two parameters:

- `Scene scene`: Represents the scene that has been loaded.
- `LoadSceneMode mode`: Indicates how the scene was loaded. This can be one of two values - `Single` (where the loaded scene replaces the current scene) or `Additive` (where the loaded scene is added to the current scene, allowing multiple scenes to be loaded simultaneously).

This method is an event handler, which is called whenever a new scene is loaded. It logs the name of the loaded scene and then calls the `PrintGameObjectAndChildren` method for every root game object in the scene; for instance, if you have a scene with a game object `A` that has children `B` and `C`, and `B ` has a child `D`, then only `A` would be considered a root game object. The method runs recursively, effectively printing the entire scene hierarchy.

Building the Mod ( `dotnet build` from the mod directory) will then automatically place it into the `.\BepInEx\plugins` folder, as per the build file, and then when you run `Hookman`, you will see the various bits of information now being logged.

![](https://academy.hackthebox.com/storage/modules/208/Hookman-LoggedInfo.png)

Looking at the `GameObjects` that exist in the actual Game scene, which we now know is `Level_1`, we can see quite a few objects, including the `ChallengeText` and `ChallengeBlock` objects. Much like `Modman`, the assumption here is we will need to edit out the Block again.

![](https://academy.hackthebox.com/storage/modules/208/Hookman-LevelLog.png)

Since we now know the `Scene ` and `GameObject ` we want to manipulate, we can update the code. We will need to declare a new `GameObject` that will be used to capture a reference to the `ChallengeBlock` object. Also, since we want to be able to toggle things, we will add a `KeyCode` object for the `T` key.

```csharp
...
public class GameMod : BaseUnityPlugin
{
    private static KeyCode _toggleKey = KeyCode.T;

    private GameObject? _block;
...

    public void Update()
    {
        // if the toggle key is not pressed, return
        if (!Input.GetKeyDown(_toggleKey)) return;
        // toggle the active state of the ChallengeBlock in the scene
        _block?.SetActive(!_block.activeInHierarchy);
    }
...
    /// <summary>
    /// This method is called every time a new scene is loaded.
    /// </summary>
    /// <param name="scene">The scene that was loaded.</param>
    /// <param name="mode">The mode in which the scene was loaded.</param>
    private void OnSceneLoaded(Scene scene, LoadSceneMode mode)
    {
        // This code will run every time a new scene is loaded
        Logger.LogInfo("Scene loaded: " + scene.name);
        // Call any other functions you want to run when the scene changes
        // loop through every game object in the scene
        foreach (var gObject in scene.GetRootGameObjects())
        {
            // print the name of the game object and all of its children, starting at depth 0
            PrintGameObjectAndChildren(gObject, 0);
        }

        // check that the current scene is Level_1
        if (scene.name == "Level_1")
        {
            // find the ChallengeBlock in the scene
            _block = GameObject.Find("ChallengeBlock");
            if (_block != null)
            {
                // if the ChallengeBlock was found, log its position
                Logger.LogInfo("=== HOOKED CHALLENGEBLOCK ===");
            }
            else
            {
                // if the ChallengeBlock was not found, log an error
                Logger.LogError("=== FAILED TO HOOK CHALLENGEBLOCK ===");
            }
        }
    }
}

```

Compile the updated mod, adding the new code above, and now when you press the `T` key in game, on the correct scene, the `ChallengeBlock` will vanish off the scene.

Enable step-by-step solutions for all questions
![sparkles-icon-decoration](https://academy.hackthebox.com/images/sparkles-solid.svg)

#### Questions

Answer the question(s) below
to complete this Section and earn cubes!

\+ 15  What is the text hiding behind the purple block?


Submit


[Hookman.zip](/storage/modules/208/Hookman.zip)


# Harmony Patching

* * *

BepInEx also directly integrates [Harmony](https://github.com/pardeike/Harmony), a “A library for patching, replacing and decorating .NET and Mono methods during runtime”. Harmony essentially enables alteration of methods in assemblies without directly modifying the original code.

Several types of patches can be used in Harmony:

1. `Prefix `: This patch is executed before the original method and can be used to access and edit the arguments of the original method, set the result of the original method, skip the original method, set a custom state that can be recalled in the postfix, or run a piece of code at the beginning.
2. `Postfix`: This patch is executed after the original method and can be used to read or change the original method's result, access the original method's arguments, or read the custom state from the prefix.
3. `Transpiler`: This patch modifies the code of the original method. It is used in advanced cases where you want to modify the original method's IL (Intermediate Language) code.
4. `Finalizer`: This patch is executed after all postfixes. It wraps the original method, all prefixes, and postfixes in a try/catch logic and is called with either null (no exception) or with an exception if one occurred. It is commonly used to run a piece of code at the end that is guaranteed to be executed, handle exceptions, and suppress or alter them.
5. `Reverse`: This patch allows you to patch your methods instead of foreign original methods. You define a stub that looks like the original method and patches the original onto your stub, which can be called from your code. This patch type also supports transpilation during the process.

## Prefix Patches

When a method marked for patching is invoked, the prefix patch executes before the main method's logic takes effect. This allows it to read, modify, or even outright replace the input parameters meant for the original method. Moreover, its inherent power extends to flow control. Returning a boolean value ( `true` or `false`) from the patch method can denote whether the original patched function is executed at all: `true` permits the method to run as intended, while `false` bypasses it entirely.

Prefix patches are especially useful in Game Hacking and Modding:

1. `Unlimited Health or Ammo`: Imagine a game where the player's health or ammunition decreases with every hit or shot. A prefix patch could be applied to the method that updates these values ( `UpdateHealth` or `UpdateAmmo`). Before the method depletes the health or ammo, the patch can reset the value to its maximum or prevent the reduction logic from executing.
2. `Bypassing Microtransactions`: In games with in-app purchases, a method like CheckPurchase might verify if a player has bought a particular item or feature. A prefix patch could manipulate this method to always return `true`, tricking the game into thinking that every purchase has been made, thereby unlocking premium content without actual payment.
3. `Unlocking Levels or Characters`: Some games have progression systems where players need to complete certain levels or tasks to unlock the next level or character. A prefix patch on methods like `IsLevelUnlocked` or `IsCharacterAvailable` can be designed to always allow access, regardless of actual progression.
4. `Bypassing Anti-cheat Mechanisms`: Modern games often come with anti-cheat mechanisms that detect and prevent modifications. A prefix patch could target these methods (like `IsGameModified`) to always return `false`, suggesting that the game hasn't been tampered with.
5. `Unlocking Hidden or Developer Modes`: Some games have hidden developer modes or features that are typically inaccessible to players. A prefix patch on the `AccessDeveloperMode` method might bypass any checks and grant the player access to these restricted areas.
6. `Custom Skins or Assets`: In games where players can customise their characters, weapons, or vehicles, a prefix patch on methods related to asset loading (like `LoadCharacterSkin`) can be used to load custom or unofficial skins or models.

```csharp
using BepInEx;
using BepInEx.Unity.Mono;

namespace HarmonyPatch;

using HarmonyLib;
// defined under the namespace, as to override System.Object with UnityEngine.Object
using UnityEngine;
using UnityEngine.SceneManagement;
using BepInEx.Logging;

// defines BepInEx plugin info
[BepInPlugin("GH", "GameMod", "1.0.0")]
public class GameMod : BaseUnityPlugin
{
    void Awake()
    {
        // creates a Harmony instance and automatically patches all methods in the `GameMod` class that have a Harmony attribute (like `HarmonyPatch`).
        Harmony.CreateAndPatchAll(typeof(GameMod));
        // Plugin startup logic
        Logger.LogInfo($"Plugin is loaded!");
    }

    // `HarmonyPatch` specifies which method to patch. In this case, the method `TargetMethod` from the `GameClass` class.
    [HarmonyPatch(typeof(GameClass), nameof(GameClass.TargetMethod))]
    // `HarmonyPrefix` denotes a prefix patch, meaning the code within will run before the targeted method.
    [HarmonyPrefix]
    // `Prefix` is the method that contains the actual patching logic. It takes a `bool` reference `_variable` and sets its value to `false`.
    public static void Prefix(ref bool _variable)
    {

        // Modify the param value of TargetMethod `_variable`
        _variable = false;
    }
}

```

When the `TargetMethod` of `GameClass` is called in the game, Harmony ensures that the `Prefix` method is executed first, setting the `_variable` to `false`.

Refer to the [Harmony Patching Documentation](https://harmony.pardeike.net/articles/patching.html) for other methods and uses.


# Fundamentals of Game Networking

For a general introduction to networking and related concepts and technologies, refer to the [Introduction to Networking](https://academy.hackthebox.com/module/details/34) module.

The primary concept of game networking centres on communication among various players' systems or consoles, known as clients, across a network. This network might be local (for instance, at a LAN party) or the Internet for online multiplayer games. Essential data such as player positions, actions, game states, and more are transferred, vital for synchronising the game state across distinct clients.

Typically, game networking encompasses two main components:

1. `Clients`: These represent individual players' devices, such as computers, consoles, or mobile devices. A client's core function entails collecting input from the player (like a keyboard or controller input), transmitting this information to the server, receiving updates from the server, and rendering the game state for the player.
2. `Server`: The server is the central authority in most networked multiplayer games. It receives updates from each client, processes them (this may involve game logic like collision detection or score updates), and subsequently disseminates the latest game state back to all clients.

In certain game designs, one of the clients might double as the server (referred to as a listen server), or there might not be a central server at all (peer-to-peer networking). However, the client-server model is prevalent in multiplayer games due to its benefits in controlling game state and deterring cheating.

The primary challenge in game networking involves managing the delay (or latency) inherent in transmitting data over a network, causing players to perceive different versions of the game state. Game developers utilise various techniques to tackle this issue, such as lag compensation, prediction, and interpolation.

## Peer-to-Peer vs Client-Server

Game networking predominantly relies on two distinct models: the peer-to-peer ( `P2P`) model and the client-server model.

In `Peer-to-Peer` (P2P) game networking, each player's machine establishes direct connections with every other player's device, serving dual roles as a client and a mini-server. This decentralised architecture eliminates the necessity for a robust central server, reducing operational costs.

Nevertheless, it introduces complications, including heightened complexity in connection management, an elevated risk of cheating due to the absence of an authoritative entity, and possible inconsistencies in the game state among different players.

Conversely, in a `Client-Server` architecture, a centralised server maintains the authoritative game state and orchestrates interactions between players. All players establish connections with this central server, which authenticates player actions, updates the game state, and disseminates these changes to all connected clients.

Although this centralised model simplifies the management of the game state and bolsters security through authoritative validation, it may result in increased latency and elevated costs associated with server maintenance and scalability.

| Aspect | Peer-to-Peer | Client-Server |
| --- | --- | --- |
| Server Costs | `Lower` \- No need for a centralised server; each player's device acts as a mini-server, reducing costs. | `Higher `\- Requires robust servers, increasing the setup, maintenance, and bandwidth cost. |
| Latency | `Can be lower` \- Data packets travel directly between players, potentially reducing latency if clients are close to each other. | `Can be higher` \- Extra hop through a centralised server can add to latency, but it depends of the geo-location of the servers |
| Scalability | `Scales with peers` \- Each new player provides additional network resources, although complexity increases. | `Server-dependent` \- The server’s capacity limits scalability; more players require server upgrades. |
| Resilience | `High `(if one peer drops) - More resilient to individual failures; the game can continue among remaining peers. | `Low `(if server drops) - If the central server fails, the game is disrupted for all players. |
| Security | `Less secure` \- There is no central authority for validation, making cheating easier. | `More secure` \- Central server validates player actions, making it harder for cheating to occur. |
| Complexity | `More complex` \- Each peer must communicate with every other peer, complicating game state management. | `Less complex` \- Server controls game logic and state, simplifying client-side development. |
| Consistency | `Can be inconsistent` \- Maintaining a consistent game state across all peers can be challenging. | `More consistent` \- The server maintains the authoritative game state, ensuring a single, consistent game world. |
| Host Dependence | `Dependent on host peer` \- If a 'host' is used and leaves the game, it can disrupt the experience for all players. | `Not dependent` \- There is no dependence on individual players; the server coordinates everything. |
| Management | `More challenging` \- The decentralised nature makes it harder to manage and debug. | `Easier `\- A centralised nature makes managing, monitoring, and updating easier. |
| Single Point of Failure | `No` (unless host-based) - Generally no single point of failure, unless a 'host' system is used. | `Yes` \- The central server is a single point of failure; if it goes down, the game is disrupted for all players. |

## Game Latency (Ping)

Latency, commonly called ping in gaming, denotes the time data travels from one point to another. In video games, it's typically measured in milliseconds ( `ms`) and signifies the delay between a player's action and the game's response to that action.

For instance, when a player presses a button for their character to jump, latency is the delay between the button press and the character being seen jumping on the screen. Lower latency ensures the game feels more responsive, enabling players to react swiftly to in-game events.

In online gaming, latency is primarily dictated by the physical distance between the player's device (client) and the game server. However, other factors like the quality of the player's internet connection and the performance of their device can also contribute to latency.

High latency, often termed "lag", can significantly impact gameplay. If a player's actions are delayed, they may struggle to compete with other players, especially in fast-paced games that demand quick reactions.

## Prediction and Interpolation in Game Networking

In game networking, `prediction ` and `interpolation ` are fundamental techniques for providing a smooth gameplay experience, particularly under conditions of fluctuating network latency. They are chiefly employed to `mask the effects of latency` and preserve a consistent game state among various players.

`Prediction` is a technique that anticipates the outcome of a player's action before the server verifies it. With prediction, the game client doesn't need to await a server response to update the game state. When a player acts (such as moving forward or shooting), the client instantly displays the player moving, even though the server hasn't yet confirmed this action.

This approach creates a more responsive experience for the player. However, it can also lead to inconsistencies between the client's and server's game states if the server disagrees with the client's prediction (due to factors like network lag or other players' actions).

`Interpolation` is a technique employed to smooth out the movement of game objects between server updates. In online games, the server typically sends updates to the client at a specific rate (such as 20 times per second). However, games often run at higher frame rates (like 60 frames per second).

To bridge the gaps between server updates, the client will estimate (or interpolate) the game state for the intervening frames. For instance, if a player is moving, the client will display them continuing to move in the same direction at the same speed until the next update from the server.

This approach makes the motion of other players and game objects appear smooth rather than jerky or stuttering. But, like prediction, it can occasionally cause inconsistencies if the interpolated game state diverges from the actual game state on the server.

Both prediction and interpolation are integral to preserving a seamless and immersive gaming experience, particularly in fast-paced or real-time games where the impact of network latency can be most disruptive.


# How Do Games Network

* * *

The communication between a game and a server typically involves transmitting and receiving data over a network. This exchange occurs via `TCP `(Transmission Control Protocol) or `UDP `(User Datagram Protocol).

Here's a simplified depiction of this operation:

1. `Establishing Connection`: The initial step usually involves the game (client) initiating a connection with the game server. The client requests a connection to the server's IP address and port. Once the server accepts the request, a link for communication is established.
2. `Sending Requests`: After connection establishment, the client-side game can transmit requests to the server. These requests might be player actions such as moving, jumping, shooting, etc. Generally, these requests are sent as packets, which are compact data units.
3. `Processing Requests`: The game server receives these requests, processes them, and updates the game state accordingly. This process could involve calculating a player's new position, verifying if a shot hit a target, managing player inventory, etc.
4. `Sending Responses`: After processing the request and updating the game state, the server responds to the client. This response carries the updated game state, which may include players' updated positions, results of actions, updated game scores, etc.
5. `Receiving Responses`: The game client receives these responses, updates the game state locally, and displays the updated state to the player. This may involve moving a player's character on the screen, showing a hit marker when a shot connects, updating the player's score, etc.

This process is repeated numerous times per second (commonly 20 times or more) to maintain synchronisation of the game state between the server and client. Depending on the game and its network architecture, various types of data may be prioritised, and diverse techniques may be used to manage network latency and packet loss.

Regarding the actual technologies used, they can differ significantly by game. Some games use HTTP/HTTPS (mainly web-based games), some directly use TCP or UDP, and some use higher-level, gaming-specific protocols and libraries offering additional features like entity interpolation, lag compensation, prediction, etc.

## Handling Packet Loss

Packet loss occurs when one or more packets of data traversing a network fail to reach their destination. In online gaming, packet loss can lead to lag, missing game assets, or erratic game behaviour, substantially impacting the gaming experience.

Games employ various strategies to handle packet loss:

- `Prediction and Interpolation`: As explained in the previous section, these techniques predict the outcome of player actions before the server can respond. However, they can also assist in masking the effects of packet loss. By predicting the game state based on the most recent data, the game can continue to operate smoothly even if some updates from the server are lost.
- `Packet retransmission`: When a game detects packet loss, it can request that the server or the sending player retransmit the missing packets. This helps ensure all the necessary data is received, minimising the impact of the lost packets.
- `Forward Error Correction (FEC)`: Games can employ FEC techniques to add redundant information to the transmitted packets. This redundancy enables the receiver to reconstruct lost or corrupted packets using the additional data. FEC is particularly useful for handling small levels of packet loss.
- `Server reconciliation`: Server reconciliation is a technique that involves the server checking the client's predicted state and either confirming it or rejecting it. This can help ensure the game state is consistent across all clients.

## Matchmaking

Matchmaking refers to the process of connecting players for online multiplayer sessions. The primary goal of matchmaking is to find the best possible matches for players, ensuring the game is enjoyable, fair, and challenging for all participants. The complexity of the matchmaking algorithm can vary depending on the requirements of the game and its community. There are 4 major components to Matchmaking:

1. `Matchmaking Server`: A centralised server responsible for creating matches. Players express their intent to join a game, and the server groups them based on various criteria.
2. `Player Pool`: The set of all players looking to play a game. From this pool, the matchmaking algorithm selects players to create matches.
3. `Matchmaking Criteria`: Various parameters and algorithms can be used to find the best match for players.
   - `Random Matchmaking`: The simplest form, where players are randomly matched together. This is quick but can result in poorly balanced matches.
   - `Skill-Based Matchmaking (SBMM):` Players are grouped based on skill levels, often determined by metrics like kill-to-death ratio, win-loss ratio, or a separate "Elo" rating system.
   - `Rank-Based Matchmaking`: Similar to SBMM, it uses visible "Ranks" that players earn through gameplay. Players are usually matched with others of the same or similar rank.
   - `Role-Based Matchmaking`: In games that require different roles (like a healer, tank, and damage dealer), the matchmaking tries to ensure that each team has a balanced composition of roles.
   - `Friend and Group Matchmaking`: Players can form a group with friends and enter the matchmaking process together. The algorithm then tries to find an opposing group with similar characteristics.
   - `Geographic Matchmaking`: Players are often matched based on geographic proximity to reduce latency.
4. `The Match`: A session where grouped players can play together. Once a match is made, the matchmaking server might pass control to a dedicated game server where the actual gameplay happens.

## Scalability in Game Networking

Scalability refers to the ability of a game's network architecture to handle an increasing number of players and sessions while maintaining performance, speed, and reliability. As a game becomes more popular, its networking infrastructure must scale seamlessly to accommodate the growing user base. Issues can manifest in various ways without proper scaling, such as increased latency, frequent disconnections, or server crashes, which can severely degrade the gaming experience.

There are a few specific components that may need to be scaled within a game network:

1. `Game Servers`: The servers where game logic is executed, and players connect to play the game. These need to be able to handle more sessions as the player base grows.
2. `Matchmaking Servers`: As more players join the game, the matchmaking algorithm may need to handle more complex scenarios and larger player pools, requiring more computational resources.
3. `Database Servers`: Stores player profiles, inventories, match histories, and other persistent data. As the number of transactions increases, the database must be able to handle the load efficiently.
4. `Content Delivery Network (CDN)`: Used for distributing game updates, assets, or even video streams to players worldwide. Scalability ensures low latency and high availability of these resources.
5. `API Endpoints`: Various APIs may provide additional functionalities like leaderboards, social features, or in-game purchases, which also need to scale.

There are a few different general strategies for scaling those various components:

- `Horizontal Scaling`: This strategy adds more servers to cater to more players. Extra servers can be activated to manage the load when the player base expands. Cloud-based gaming infrastructures typically employ this strategy, where new server instances can be initiated as required.

- `Vertical Scaling`: This strategy involves bolstering the resources of a pre-existing server, which can include adding more RAM, CPU power, or bandwidth. Although vertical scaling can promptly enhance game performance, it does have a ceiling based on the server's maximum capacity.

- `Load Balancing`: This strategy distributes network or application traffic across multiple servers to ensure no single server is overwhelmed and is generally used in conjunction with horizontal or vertical scaling.


## Game Network Security

The ever-rising popularity of multiplayer games has led to an increase in network security challenges. Security threats can vary from cheating to Denial-of-Service (DoS) attacks, potentially disrupting the gaming experience for all participants. Below are some common security considerations in game networks.

Firstly, the network architecture selection dramatically influences how a game communicates with a server and its potential vulnerabilities. Peer-to peer (P2P) networks, while reducing server costs and providing better scalability, might be more prone to security risks as there's no central authority to validate actions. The Client-Server model offers greater control and security but comes with increased server costs and a single point of failure.

The communication between a game (client) and a server involves a sequence of data sending and receiving over the network. Security must be upheld at all stages - `establishing a connection`, `sending requests`, `processing requests`, `sending responses`, and `receiving responses`. The protocols used, such as TCP or UDP, should also be considered, as they can have vulnerabilities.

That said, there are some common attacks that can affect game network security from both an information security perspective and a game hacking/integrity perspective.

- `Packet Sniffing and Man-in-the-Middle Attacks`: Attackers can intercept, inspect, and sometimes alter data packets being sent between the client and the server. This can be used to cheat, steal sensitive data, or even impersonate another player.
- `Denial of Service (DoS) and Distributed Denial of Service (DDoS) Attacks`: In these attacks, the server becomes inundated with traffic, rendering it incapable of processing legitimate requests. This results in an unplayable experience for all users connected to the affected server. Frequent failure points and targets for DDoS attacks are typically things like Login and Authentication servers, which are generally not scaled as game servers are.
- `Insecure Direct Object References (IDOR)`: This vulnerability occurs when a user can directly access an object, such as a file or database key, without appropriate permission. This could mean unauthorised access to other players' profiles, in-game items, or even admin functionalities in gaming.
- `Authentication and Session Management Flaws`: Weak authentication mechanisms can allow attackers to impersonate legitimate users. Session management flaws can allow attackers to hijack a user's session, gaining unauthorised access to their account.
- `Insecure Data Storage and Transmission`: Sensitive data like passwords, payment information, and personal details should be encrypted in transit and at rest. Failure to do so can lead to data breaches.
- `Server Vulnerabilities`: Poorly configured or outdated servers can have multiple vulnerabilities, including buffer overflows and operating system-level vulnerabilities, that can be exploited to gain unauthorised access or disrupt service.
- `Logic Flaws`: These vulnerabilities in the game's business logic can be exploited to gain an unfair advantage. For example, attackers exploit a bug, allowing themselves to gain infinite in-game currency or duplicate items.
- `Client-Side Trust`: If a game relies too much on the client for game state, player actions, or validation checks, it can be easier for attackers to cheat by altering the client's code or memory with tools like Cheat Engine.


# Man In The Middle Attacks

* * *

A Man-in-the-Middle ( `MitM`) attack is a cybersecurity threat where a malicious actor inserts themselves into a conversation between two parties. The attacker impersonates both parties and gains access to information that the two parties were trying to send to each other.

The term Man-in-the-Middle attack originates from the literal scenario of a person intercepting a communication between two individuals. Although this concept is as old as communication itself, it has evolved into a more technical and sophisticated form of cybersecurity.

## Executing MITM Attacks

The ultimate goal of a `MitM` attack is typically one of the following:

- `Eavesdropping`: The attacker can listen in and gather useful information by intercepting the communications.
- `Data Manipulation`: The attacker alters the communication between the two parties, potentially leading to harmful outcomes.
- `Identity Theft`: Once the attacker has enough data, they can impersonate the victim, potentially leading to financial theft or other forms of fraud.

A `MitM` attack comprises several steps:

1. `Interception`: Initially, the attacker must be capable of intercepting the traffic between the victim and their destination. Various methods can achieve this, such as Address Resolution Protocol ( `ARP`) spoofing, where the attacker sends false ARP messages to a local network. As a result, network devices link the attacker's MAC address with the IP address of another host (like the default gateway).
2. `Decryption`: If the data is encrypted (as it ideally should be), the attacker must decrypt it. In a classic `MitM` attack, techniques like Secure Sockets Layer ( `SSL`) stripping are used to downgrade the connection from HTTPS to HTTP.
3. `Data Capture and/or Alteration`: After gaining access to the data, the attacker can either capture it for later use or alter the data in transit before forwarding it to the intended recipient.
4. `Re-encryption and Delivery`: To remain undetected, the attacker must re-encrypt the data (if it was encrypted initially) and then send it to the recipient. Consequently, the recipient remains unaware that their data has been intercepted or altered.

MitM attacks have been employed in several high-profile cyberattacks. A prominent example occurred in 2013 when [Belgian telecommunications company Belgacom was targeted by the British intelligence agency GCHQ](https://theintercept.com/2014/12/13/belgacom-hack-gchq-inside-story/).

GCHQ utilised a technique known as a `Quantum Insert` attack, often referred to as `Man-on-the-side`, for this operation. `Quantum Insert` is a cyber-espionage method employed by intelligence agencies to intercept and redirect web users to malicious websites or servers. This strategy is mainly used to implant malware or carry out surveillance activities.

Recognising the engineers as prime targets due to their access privileges, GCHQ fashioned LinkedIn pages that mirrored genuine ones, embedding them with malicious code intended to exploit vulnerabilities in the engineers' browsers or computers. The engineers were drawn to these falsified pages through phishing emails or redirects when attempting to visit the LinkedIn site or other trusted websites. When these deceptive pages were visited, the malicious code would exploit a vulnerability, enabling GCHQ to install malware on the targeted system. This malware granted GCHQ access to the target's system and the necessary credentials to infiltrate Belgacom's infrastructure. This method allowed GCHQ to infiltrate Belgacom's systems under the code name `OPERATION SOCIALIST`.

This covert infiltration aimed to access Belgacom's Global Roaming Exchange ( `GRX`) Operator. This access would permit GCHQ to obtain roaming data for mobile devices and execute a Man-in-the-Middle attack against specific targets.

Online tools and frameworks like `Wireshark` and `BetterCap` enable the execution of a MitM attack. `Wireshark` is an open-source packet analyser that lets users see network activities at a microscopic level. At the same time, hackers can use it to capture packets and inspect data, including sensitive information, if not properly encrypted. Similarly, `BetterCap` is a powerful, flexible, and portable tool for performing various network attacks and delivering payloads, potentially exploiting network-related vulnerabilities.

## Mitigating MITM Attacks

Mitigating `MitM` attacks is essential for maintaining the security and integrity of your data. Here are some strategies that can be employed:

1. `Encryption`: Adopt robust encryption protocols for your data, such as `HTTPS`, `SSL`, `TLS`, or `IPSec`. These protocols make it challenging for an attacker to decode intercepted data.
2. `Secure Wi-Fi`: Only use secure, password-protected Wi-Fi networks. Open public Wi-Fi networks can often be a breeding ground for `MitM` attacks.
3. `Virtual Private Networks (VPN)`: A `VPN` can offer an added layer of security by encrypting your internet connection and disguising your IP address. It creates a secure tunnel from your device to the VPN server. This step enhances the difficulty for attackers attempting to intercept your data.
4. `Certificate Pinning`: This is a method where the client verifies the server's identity by comparing its certificate with a trusted copy. It helps prevent `MitM` attacks that rely on presenting falsified certificates.

Remember, while no system is entirely immune to attacks, the goal is to make the attack as difficult as possible. This will deter most hackers, who will likely move on to an easier target.

## MITM in Gaming

`MitM` attacks are also be relevant to online gaming. Consider a scenario involving an online multiplayer game where players' devices continuously communicate with the game server, exchanging data about player positions, game stats, and more.

1. `Interception`: An attacker positions themselves between a player's device and the game server.
2. `Decryption`: The attacker decrypts the information exchanged between the player's device and the server.
3. `Data Capture or Alteration`: Now, the attacker can observe the player's in-game actions and potentially alter the data sent to the server. For example, the attacker might increase the player's score, change their position, or add game resources.
4. `Re-encryption and Delivery`: The manipulated data is re-encrypted and returned to the server. If done subtly, this manipulation can go undetected.

Consider a hypothetical popular online game, "Battle Warriors". This game relies on real-time communication between players' devices and the central game server. Player positions, scores, health points, and other in-game assets are continuously updated.

1. `Interception`: Let's imagine a hacker, Player A, is playing "Battle Warriors" on their home network. They set up a MitM attack between their gaming device and the game server.
2. `Decryption`: Player A then decrypts the packets sent from their device to the game server. Despite the challenges posed by the advanced encryption usually employed by reputable game developers, Player A manages to decrypt the data.
3. `Data Capture or Alteration`: Player A can now view the score data sent from their device to the game server after successful decryption. They then subtly alter this data, boosting their score incrementally each time they earn points in the game.
4. `Re-encryption and Delivery`: After manipulating the data, Player A re-encrypts it and sends it to the game server. To the server, the data appears to have come directly from Player A, making the score manipulation hard to detect.


# Man in the Middle Game Hacking

* * *

For this practical, we will use the `Netman` game, downloadable from the section at the end of the page.

`Netman` mirrors the familiar `Hackman` game but now boasts a fancy new scoreboard.

![](https://academy.hackthebox.com/storage/modules/208/netman-scoreboard.png)

To access the netman-server instance, ensure your device is connected to the Academy VPN. Modify the `.\Netman_Data\config.json` file to reflect your instance's IP and PORT.

```json
{
  "baseUrl": "http://localhost:5000"
}

```

`Netman` will alert you if there are any networking issues or misconfigurations. After playing the game, one main thing is very obvious. At the bottom, where there have previously been flags, is now a `Server Score` tracker. This mirrors the current game score.

![](https://academy.hackthebox.com/storage/modules/208/netman-game.png)

This indicates that the game sends the current score to the server in real-time. If we navigate to the leaderboard, available via your instance IP:PORT, we can see the same score, `200` reflected for `AcademyGamer`.

| Player ID | Name | Score |
| --- | --- | --- |
| 5 | Eve | 986396 |
| 20 | Walter | 111099 |
| 1337 | AcademyGamer | 200 |

## MITM Setup

For the MITM attack, we will employ Burp. Navigate to settings and add a new proxy listener. This will enable us to position a Burp proxy between `Netman` and the game server.

Generally, a proxy is an intermediary server between a client (like a web browser) and a destination server. A forwarding proxy, specifically, is typically used to forward web traffic from the client to the internet. The Burp Proxy will then capture and holds web requests from the client, allowing the user to view or modify requests before they reach the destination server.

![](https://academy.hackthebox.com/storage/modules/208/Burp-Settings.png)

Set a port you want Burp to listen on. This can be any open port on your machine. You may need to specify “All instances” to enable Burp to communicate over your Academy VPN.

![](https://academy.hackthebox.com/storage/modules/208/Burp-SettingsListener.png)

Then go to the `Request Handling` tab and set the details Burp will forward packets too. The `Redirect  to host` will be your instance IP, and the same for `Redirect to port`.

![](https://academy.hackthebox.com/storage/modules/208/Burp-SettingsForwarder.png)

Update the `baseUrl` to reflect `localhost` and the port bind you defined for the listener.

```json
{
  "baseUrl": "http://localhost:5001"
}

```

### Analysing App HTTP calls

When you launch `Netman`, BurpSuite will start mapping out network calls in the `Targets` tab as the game makes them to the server. In the left tree, you can see all the endpoints that are being called from the game.

![](https://academy.hackthebox.com/storage/modules/208/Burp-Targets.png)

Exploring the calls shows some interesting bits of information. The `/api/users/login` was issued a `GET` and `POST` request. The `GET` request didn’t appear to do anything of note as the response was empty, however, the `POST` request has a hardcoded `username` and `password` that returns a JWT Token.

```http
POST /api/users/login?username=htb&password=azerty543241 HTTP/1.1
Host: localhost:5001
User-Agent: UnityPlayer/2022.3.7f1 (UnityWebRequest/1.0, libcurl/8.1.1-DEV)
Accept: */*
Accept-Encoding: gzip, deflate
Content-Type: application/x-www-form-urlencoded
X-Unity-Version: 2022.3.7f1
Content-Length: 0
Connection: close

HTTP/1.1 200 OK
Connection: close
Content-Type: application/json; charset=utf-8
Date: Tue, 15 Aug 2023 21:52:22 GMT
Server: Kestrel
Content-Length: 281

{"token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJodHRwOi8vc2NoZW1hcy54bWxzb2FwLm9yZy93cy8yMDA1LzA1L2lkZW50aXR5L2NsYWltcy9uYW1lIjoiaHRiIiwiUGxheWVySWQiOiIxMzM3IiwiZXhwIjoxNjkyMjIyNzQyLCJpc3MiOiJIVEJBY2FkZW15IiwiYXVkIjoiSFRCQWNhZGVteSJ9.JXSNYPyDaizesdL6vTjg6aN03srNsCgXBY2d-MzFxuY"}

```

Of interest, there is also `/scoreboard/getflag` endpoint that to returns a message.

```http
GET /scoreboard/getflag HTTP/1.1
Host: localhost:5001
User-Agent: UnityPlayer/2022.3.7f1 (UnityWebRequest/1.0, libcurl/8.1.1-DEV)
Accept: */*
Accept-Encoding: gzip, deflate
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJodHRwOi8vc2NoZW1hcy54bWxzb2FwLm9yZy93cy8yMDA1LzA1L2lkZW50aXR5L2NsYWltcy9uYW1lIjoiaHRiIiwiUGxheWVySWQiOiIxMzM3IiwiZXhwIjoxNjkyMjIyNzQyLCJpc3MiOiJIVEJBY2FkZW15IiwiYXVkIjoiSFRCQWNhZGVteSJ9.JXSNYPyDaizesdL6vTjg6aN03srNsCgXBY2d-MzFxuY
X-Unity-Version: 2022.3.7f1
Connection: close

HTTP/1.1 200 OK
Connection: close
Content-Type: text/plain; charset=utf-8
Date: Tue, 15 Aug 2023 21:52:22 GMT
Server: Kestrel
Content-Length: 26

Nope, try try try again...

```

Then there is a `scoreboard/score` endpoint that appears to be updating a specific userID of 1337, `/scoreboard/score/1337`, and from viewing the Leaderboard, we know that’s the ID of the AcademyGamer user. The `GET` request returns the current score, which is likely what `Netman ` uses to update the `Server Score` tracker at the bottom of the window.

```http
GET /scoreboard/score/1337 HTTP/1.1
Host: localhost:5001
User-Agent: UnityPlayer/2022.3.7f1 (UnityWebRequest/1.0, libcurl/8.1.1-DEV)
Accept: */*
Accept-Encoding: gzip, deflate
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJodHRwOi8vc2NoZW1hcy54bWxzb2FwLm9yZy93cy8yMDA1LzA1L2lkZW50aXR5L2NsYWltcy9uYW1lIjoiaHRiIiwiUGxheWVySWQiOiIxMzM3IiwiZXhwIjoxNjkyMjIxMTA5LCJpc3MiOiJIVEJBY2FkZW15IiwiYXVkIjoiSFRCQWNhZGVteSJ9.6S0vK5noP6g9Rn_CCs6M5Jsb-ilA6IFEfoZwBC8bYYg
X-Unity-Version: 2022.3.7f1
Connection: close

HTTP/1.1 200 OK
Connection: close
Content-Type: application/json; charset=utf-8
Date: Tue, 15 Aug 2023 21:56:27 GMT
Server: Kestrel
Content-Length: 3

100

```

The `POST` method sends a new score to the server, which is of particular interest.

```http
POST /scoreboard/score/1337 HTTP/1.1
Host: localhost:5001
User-Agent: UnityPlayer/2022.3.7f1 (UnityWebRequest/1.0, libcurl/8.1.1-DEV)
Accept: */*
Accept-Encoding: gzip, deflate
Content-Type: application/json
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJodHRwOi8vc2NoZW1hcy54bWxzb2FwLm9yZy93cy8yMDA1LzA1L2lkZW50aXR5L2NsYWltcy9uYW1lIjoiaHRiIiwiUGxheWVySWQiOiIxMzM3IiwiZXhwIjoxNjkyMjIxMTA5LCJpc3MiOiJIVEJBY2FkZW15IiwiYXVkIjoiSFRCQWNhZGVteSJ9.6S0vK5noP6g9Rn_CCs6M5Jsb-ilA6IFEfoZwBC8bYYg
X-Unity-Version: 2022.3.7f1
Content-Length: 14
Connection: close

{"score": 100}

HTTP/1.1 200 OK
Connection: close
Content-Type: application/json; charset=utf-8
Date: Tue, 15 Aug 2023 21:52:05 GMT
Server: Kestrel
Content-Length: 13

{"score":100}

```

## MITM

The `POST` is of particular interest here. We can use the Burp Repeater to potentially edit this value. We can edit the score value and submit send it, and the server returns a `200 OK` response with the new score.

![](https://academy.hackthebox.com/storage/modules/208/Burp-Repeater.png)

We can also see the new value in the Leaderboard now.

![image-20230816000422000](https://academy.hackthebox.com/storage/modules/208/image-20230816000422000.png)

We can then fire off a request to the `getflag` endpoint Burp discovered earlier.

![](https://academy.hackthebox.com/storage/modules/208/Burp-Highscore.png)

Enable step-by-step solutions for all questions
![sparkles-icon-decoration](https://academy.hackthebox.com/images/sparkles-solid.svg)

#### Questions

Answer the question(s) below
to complete this Section and earn cubes!

Click here to spawn the target
system!

Target(s): Fetching status...

Life Left: 0 minute(s)


Terminate

[Download VPN Connection File](https://academy.hackthebox.com/vpn/key)

\+ 15  What is the value of the flag from the getscore endpoint, after you successfully set the score to a value greater than 1'000'000?


Submit


[Netman.zip](/storage/modules/208/Netman.zip)


# Skills Assessment

* * *

The billion-dollar company, `AnyCurrentGame.CO`, had their sights set more on profits than perfection. Eager to cash in, they rushed the release of their soon-to-be new hit title, `Fixman` . However, this version resembled an early access game riddled with bugs than a final product that consumers should have bought. The most glaring oversight? A critical bug that prevented players from transitioning scenes once the game started because the appropriate functions were just never called. This flaw was so elusive that even the company's highly paid QA team, which totally exists and is not a sign on a closet with a computer setup inside to pass all tests automatically, couldn't spot it.

The fallout was swift and unforgiving. The gaming community's backlash led to the company's dissolution, leaving `Fixman` forever in its perpetually broken state.

There was hearsay from a media interview with disgruntled developers, and one of the developers let slip that all their problems started when their bosses decided to implement a stupid `CheckStart` in `MenuManager` as part of a new DRM package.

Now, the game's salvation rests in your hands. As a renowned game modder, you possess the expertise to rectify this disastrous oversight. Your goal, is to fix this egregious error and reveal the potentially remarkable game that has been trapped behind its never-ending start screen. The gaming community eagerly awaits your solution!

Enable step-by-step solutions for all questions
![sparkles-icon-decoration](https://academy.hackthebox.com/images/sparkles-solid.svg)

#### Questions

Answer the question(s) below
to complete this Section and earn cubes!

Click here to spawn the target
system!

Target(s): Fetching status...

Life Left: 0 minute(s)


Terminate

[Download VPN Connection File](https://academy.hackthebox.com/vpn/key)

\+ 40  After you have fixed the game, and modified the score to a value greater than 1'000'000, what is the flag returned via the getflag endpoint?


Submit


[Fixman.zip](/storage/modules/208/Fixman.zip)


