# Introduction to C\#

* * *

`C#` (pronounced "C sharp") is a general-purpose, object-oriented programming (OOP) language developed by Microsoft within its `.NET` initiative. It is fundamentally rooted in the C and C++ family of languages and borrows aspects from Java, making C# very familiar for developers of those languages.

- Hello world in C#

```csharp
using System;
class Program
{
    static void Main(string[] args)
    {
        Console.WriteLine("Hello, World!");
    }
}

```

- Hello world in C++

```cpp
#include <iostream>
int main()
{
    std::cout << "Hello, World!";
    return 0;
}

```

- Hello world in Java

```java
public class Main
{
    public static void main(String[] args)
    {
        System.out.println("Hello, World!");
    }
}

```

The C# project commenced in the late 1990s, known initially as `Cool`, an acronym for "C-like Object Oriented Language". The driving force for the project was to build a language that offered the computational power of C++ combined with the simplicity of Visual Basic. Its key designer was Anders Hejlsberg, a prominent engineer previously involved in designing Turbo Pascal and Delphi at Borland, who still serves as the lead architect of C#.

C# was officially announced in July 2000, with the release of .NET Framework 1.0 following in 2002. C# is one of several languages that can be used to build .NET applications but by far the most dominant. Other languages can be used with the .NET Framework, such as Visual Basic and F#.

The `.NET Framework` is a language-agnostic software development and runtime platform developed by Microsoft. It provides a controlled environment for developing and running applications. Programs written for the .NET Framework execute in a software environment known as the `Common Language Runtime` (CLR), an application virtual machine that provides services such as security, memory management, and exception handling. There are many different components to the .NET Framework; some are listed below:

- The `Common Language Runtime (CLR)` is the execution engine for .NET Framework applications. It provides various services, such as memory management and thread management.
- The `.NET Framework Class Library (FCL)` is a standard library that encapsulates many common functions, such as file reading and writing, graphic rendering, database interaction, and XML document manipulation.
- `Common Language Specification (CLS)` is a set of rules and standards that enforce language interoperability.
- `Common Type System (CTS)` is a standard that defines all possible data types and programming constructs supported by CLR and how they interact.

### JIT

Just-In-Time compilation, or `JIT`, is a significant component of runtime environments in many modern programming languages, such as Java, Python with PyPy, LUA with LuaJIT and the .NET languages like C#. Programming Languages broadly fall into two categories: `Interpreted languages` and `compiled languages`, and a JIT compiler straddles the divide between the two.

A `statically compiled` language compiles (translates) the source code to machine code before execution. In this machine code format, the compiled binary represents the instruction set that a CPU interprets and executes. This approach offers more optimised performance than interpretation because the translation is done beforehand. However, static compilation requires additional development time due to the compile-link-execute cycle, and the resulting binaries are platform-specific.

In contrast, source code is not directly translated to machine code in an `interpreted language`. Instead, a separate program called the interpreter reads and executes the source code instructions. While this simplifies the development process because no compilation and linking steps are necessary, it can lead to slower execution speed because the interpretation needs to be performed as the program runs.

Just-In-Time compilation aims to combine the benefits of both `interpretation` and `static compilation`. It translates the source code into an intermediate form, akin to bytecode, a portable, platform-independent code. The bytecode is closer to machine code than the high-level source code but is not tied to a specific hardware configuration.

The bytecode is translated to machine code when the program is executed, but not in one big chunk. Instead, the translation happens just in time (hence the name), i.e., right before each portion of the code is executed. This strategy of deferred compilation aims to avoid the overhead of compiling parts of the program that are never executed during a particular run.

A JIT compiler is part of the `Common Language Runtime` ( `CLR`). Instead of building machine code during compilation, .NET compiles into an intermediate language called the Microsoft Common Intermediate Language (MSIL or CIL). The processor then executes this machine code. The CLR maintains a cache of compiled methods during the program's execution. If a method is called more than once, the CLR can skip the JIT compilation step on subsequent calls and use the previously compiled machine code, resulting in performance improvements.

It's worth noting that there is a trade-off in JIT compilation between startup time and execution speed. JIT compilation can slow program start-up because the initial compilation to machine code happens during runtime. However, once the program runs, execution can be very fast—often comparable to statically compiled code.

### .NET Core and .NET

Microsoft introduced `.NET Core` as a successor to the .NET Framework, addressing many of the limitations and concerns with the .NET Framework, such as it is Windows-specific and not compatible with other platforms. .NET Core is a cross-platform framework designed for building modern, cloud-based, and internet-connected applications. It runs on Windows, Linux, and macOS, making it a suitable choice for developers aiming for wide compatibility. .NET Core comprises `CoreCLR`, a complete runtime, and `CoreFX`, a library built to run apps. It was first released in June 2016.

In 2020, Microsoft announced it was consolidating its .NET offerings into a single .NET platform. This marked the birth of `.NET 5`, which aimed to unify the .NET Framework and .NET Core. The unification process was designed to take the best from .NET Core, .NET Framework, Xamarin, and Mono to build a single platform for all .NET applications. The shift aimed to provide a single .NET runtime and framework that can be used everywhere, further strengthening the .NET platform's versatility and robustness.

The advent of .NET 5 and its successors (.NET 6, 7, 8 and beyond) has ushered in an era where developers no longer have to pick and choose different .NET technologies for different types of applications. Instead, they can use a unified platform for all their work, reducing the complexity of building and deploying .NET applications.

One of the key features of .NET 5 and later versions is their support for a broad spectrum of application types, including web applications, desktop applications, cloud services, IoT applications, machine learning, and more.

Furthermore, .NET 5 and its successors follow a `release schedule` with updates every November. Microsoft has committed to long-term support (LTS) releases every two years, ensuring stability and support for developers who prefer not to update their .NET runtime and libraries annually.

## What is C\# used for

C# is a versatile and powerful programming language that can be employed to construct various program types to fulfil diverse needs and requirements. Here is a snapshot of the broad range of applications you can build with C#:

01. `Console Applications`: Perfect for building command-line interfaces, these applications are text-driven, devoid of graphical user interfaces (GUIs), and ideal for crafting simple utilities or scripts.
02. `Windows Forms Applications (WinForms)`: These GUI desktop applications come packed with a rich set of controls, including text boxes, labels, and buttons.
03. `Windows Presentation Foundation (WPF) Applications`: WPF offers a framework for creating sophisticated desktop applications with advanced UI features such as graphics, multimedia, and animations.
04. `Universal Windows Platform (UWP) Applications`: UWP apps are designed to provide a universal experience across Windows 10, Windows 10 Mobile, Windows 11, Xbox One, Xbox Series X/S, and HoloLens.
05. `Xamarin Applications`: Xamarin provides a platform for crafting mobile applications operable on multiple platforms, including iOS, Android, and Windows, all from a unified C# codebase.
06. `.NET Multi-platform App UI (MAUI) Applications`: MAUI is the evolution of `Xamarin`, extending from mobile to desktop. It allows for creating cross-platform Android, iOS, macOS, and Windows applications with a single codebase. Using MAUI, developers can create flexible and high-performance native applications using .NET and C#.
07. `ASP.NET Applications`: ASP.NET is a robust framework for building dynamic web applications, capable of serving web pages, RESTful APIs, real-time services, and more.
08. `Web Services`: These applications, accessible over standard web protocols like HTTP, SOAP, and REST, facilitate communication between applications over the Internet.
09. `Class Libraries`: These encompass collections of classes and other types that can be utilised by different applications, supporting code reuse and modular design.
10. `Unity Games`: Unity is a widely-used game development platform, with C# employed for scripting game behaviour.

## Installing the DevEnv

Visual Studio and Visual Studio Code are the most common IDEs for C# development. This module will use Visual Studio Code but feel free to use Visual Studio if you are on Windows. Install the `.NET Desktop Developer` meta package from the Visual Studio installer if you choose to go that route; otherwise, follow the instructions below.

![Visual Studio Installer showing workloads for ASP.NET, Azure, Python, Node.js, and .NET desktop development. Installation details include Visual Studio core editor and various development tools.](https://academy.hackthebox.com/storage/modules/228/vsi.png)

### VSCode

1. Navigate to the Visual Studio Code download page at the following URL: https://code.visualstudio.com/Download
2. Download the version suitable for your operating system (Windows, macOS, or Linux).
3. Run the downloaded installer.
4. Follow the instructions in the installer.

### .NET

There are a few ways to install `.NET`. Regardless of how or what platform you install `.NET` onto, you can validate your installation by running `dotnet --version` from a terminal window.

```powershell
C:\> dotnet --version

7.0.304

```

This command will output the version of .NET installed on your machine. If you see the version number of the version you installed, then the installation was successful.

| Operating System | Installation |
| :-- | :-- |
| Windows | The easiest method to install `.NET` onto Windows is via the `winget` package manager. You can refer to the [Microsoft installation documentation for Windows](https://learn.microsoft.com/en-us/dotnet/core/install/windows) for other installation methods. |
| Linux | Most Linux distributions provide official versions of `.NET`. Check your package manager for install instructions or refer to the [Microsoft installation documentation for Linux](https://learn.microsoft.com/en-us/dotnet/core/install/linux) for other installation methods. |
| macOS | You can either install via the installer downloading from the `.NET Website` or install via `homebrew`. Refer to the [Microsoft installation documentation for macOS](https://learn.microsoft.com/en-us/dotnet/core/install/macos) |

C# can also be utilised in a manner similar to interpreted languages, like Python, with tools such as [LINQPad](https://www.linqpad.net/) or [CSharpRepl](https://github.com/waf/CSharpRepl). Furthermore, extensions are available that enable a Jupyter-like [notebook experience in VSCode](https://marketplace.visualstudio.com/items?itemName=ms-dotnettools.dotnet-interactive-vscode) or a kernel extension to [use .NET in Jupyter](https://github.com/dotnet/interactive/blob/main/docs/NotebookswithJupyter.md) directly.

### PwnBox

PwnBox, fully usable in this module, comes with VSCodium, a fork of VSCode pre-installed. Due to licensing constraints, VSCodium lacks the Microsoft extensions like the `C#` extension. Although a possible alternative exists on the OpenVSX registry—since VSCodium can't utilise the Microsoft VSX registry— we suggest installing VSCode per the instructions above to access the Microsoft `C#` extension.

If VSCode does not appear in any shortcut menus after installing the package, you can launch it from the terminal via `code`. Search and install for the `C#` extension if it is not installed.

![Desktop showing Visual Studio Code with C# extension details, including installation options and popular extensions like Python and Node.js. Terminal displays command prompt with Hack The Box branding.](https://academy.hackthebox.com/storage/modules/228/vscode.png)

As it stands at the time of writing, PwnBox comes pre-installed with .NET Core 3.1 and .NET 6. You're welcome to use .NET 6, or if you prefer, you can install .NET 7 by following the above instructions.

Note: We can install .NET 6 through the APT repository with the following command `sudo apt install dotnet-sdk-6.0`.

#### PwnBox dotnet info

```shell
dotnet --info

.NET SDK (reflecting any global.json):
 Version:   6.0.408
 Commit:    0c3669d367

Runtime Environment:
 OS Name:     parrot
 OS Version:  5.3
 OS Platform: Linux
 RID:         linux-x64
 Base Path:   /usr/share/dotnet/sdk/6.0.408/

global.json file:
  Not found

Host:
  Version:      6.0.16
  Architecture: x64
  Commit:       1e620a42e7

.NET SDKs installed:
  3.1.426 [/usr/share/dotnet/sdk]
  6.0.408 [/usr/share/dotnet/sdk]

.NET runtimes installed:
  Microsoft.AspNetCore.App 3.1.32 [/usr/share/dotnet/shared/Microsoft.AspNetCore.App]
  Microsoft.AspNetCore.App 6.0.16 [/usr/share/dotnet/shared/Microsoft.AspNetCore.App]
  Microsoft.NETCore.App 3.1.32 [/usr/share/dotnet/shared/Microsoft.NETCore.App]
  Microsoft.NETCore.App 6.0.16 [/usr/share/dotnet/shared/Microsoft.NETCore.App]

Download .NET:
  https://aka.ms/dotnet-download

Learn about .NET Runtimes and SDKs:
  https://aka.ms/dotnet/runtimes-sdk-info

```

### .NET CLI

We will interact with `dotnet` via a console more than anything, as Visual Studio Code does not have the same level of 'hands-off tooling' that a full IDE, such as Visual Studio, provides. Below is a breakdown of some of the important commands to know:

- `dotnet new`: Creates a new .NET project. You can specify the type of project ( `console`, `classlib`, `webapi`, `mvc`, etc.). For example, `dotnet new console` will create a new console application.
- `dotnet build`: Builds a .NET project and all of its dependencies. The `-c` or `--configuration` option can be used to specify the build configuration ( `Debug` or `Release`).
- `dotnet run`: Builds and runs the .NET project. It is typically used during the development process to run the application for testing or debugging purposes.
- `dotnet test`: Runs unit tests in a .NET project using a test framework such as `MSTest`, `NUnit`, or `xUnit`.
- `dotnet publish`: Packs the application and its dependencies into a folder for deployment to a hosting system. The `-r` or `--runtime` option can be used to specify the target runtime.
- `dotnet add package`: Adds a NuGet package reference to the project file. You specify the package by name. For example, `dotnet add package Newtonsoft.Json`.
- `dotnet remove package`: Removes a NuGet package reference from the project file. Similar to the `add package` command, you specify the package to remove by name.
- `dotnet restore`: Restores the dependencies and tools of a project. This command is implicitly run when you run `dotnet new`, `dotnet build`, `dotnet run`, `dotnet test`, `dotnet publish`, and `dotnet pack`.
- `dotnet clean`: Cleans the output of a project. This command is typically used before you build the project again, as it deletes all the previously compiled files, ensuring that you start from a clean state.
- `dotnet --info`: Displays detailed information about the installed .NET environment, including installed versions and all runtime environments.

### A template quirk

We will use the Console template for running all code in this module; however, beginning with .NET 6, the template for creating new C# console applications ( `dotnet new console`) generates the following template:

```csharp
// Refer to https://aka.ms/new-console-template for more information
Console.WriteLine("Hello, World!");

```

This output utilises recent C# features that reduce the amount of code required for a straightforward program. This approach is suitable for small-scale projects operating entirely without a specific structure. However, for our purposes, this project style won't be suitable. Instead, it's recommended to use the provided template for projects.

```csharp
class Program
{
    public static void Main()
    {
        // ...
    }
}

```


# Basic Syntax

* * *

The C# syntax refers to the rules governing how programs written in the C# language are structured. These rules dictate aspects such as how variables are declared or initialised and how loops or conditional statements are written. This set of rules constitutes the language’s grammar and is at the core of crafting valid and efficient C# programs.

Let's delve into several essential elements of C# syntax:

## 1\. Main Method

In C#, any application begins its execution from a special method known as `Main`. This is the entry point of any C# application. When the application starts, the `Main` method is the first invoked method. The C# compiler will show an error if the `Main` method is absent.

The `Main` method can be located inside any class in the C# project; however, placing it within a class named Program is standard practice.

```csharp
class Program
{
    public static void Main() { }
    public static int Main() { }
    public static int Main(string[] args) { }
    public static async Task Main() { }
    public static async Task<int> Main() { }
    public static async Task Main(string[] args) { }
    public static async Task<int> Main(string[] args) { }
    public static void Main(string[] args)
    {
        // Program execution starts here
    }
}

```

## 2\. Case Sensitivity

In C#, case sensitivity is a fundamental aspect of the language syntax. This means the language differentiates between uppercase and lowercase characters, treating them as distinct. As a result, identifiers named with different cases are considered separate entities by the C# compiler.

For instance, consider the following variable declarations:

```csharp
int myVariable = 10;
int MyVariable = 20;

```

Even though `myVariable` and `MyVariable` may appear similar, they are treated as two completely different variables due to the difference in case. The first has a lowercase ‘m’, while the second begins with an uppercase 'M'. If you were to print both variables, they would output different values.

This feature extends to all areas of the language, including class names, method names, and other identifiers. For example:

```csharp
class MyClass
{
    // Class code...
}

class myClass
{
    // Class code...
}

```

In this case, `MyClass` and `myClass` are two entirely separate classes.

This sensitivity to case can cause challenges for new programmers who may not be accustomed to languages with similar features. A misplaced uppercase or lowercase letter can lead to unexpected behaviour or errors. Therefore, it's essential to be consistent with case when defining and using identifiers in C#.

## 3\. Identifiers

In C#, an identifier is a name assigned to a variable, method, function, or any user-defined item. It is essentially a way to refer to a code component for use in operations, functions, and algorithms.

There are a few rules and conventions to bear in mind when creating identifiers in C#:

1. An identifier must start with a letter or an underscore character ( `_`). For example, `variable`, `_variable` are valid identifiers but `1variable` is not.
2. After the first character, it can have a series of alphanumeric characters (letters and digits) and an underscore ( `_`).
3. Reserved words in C# cannot be used as identifiers. For example, you cannot use `int` or `while` as an identifier because they have predefined uses in C#.
4. There's no strict limit on the length of an identifier in C#, but it's advisable to keep them reasonably short to maintain readability.

```csharp
int score;
string playerName;
float _temperature;

```

## 4\. Keywords

C# includes a set of reserved words known as keywords, which have predefined meanings in the language's syntax. Examples of keywords include `public`, `class`, `void`, `if`, `else`, `while`, etc. Keywords cannot be used as identifiers.

```csharp
class MyClass { ... }
if (condition) { ... }

```

## 5\. The ;

The semicolon ( `;`) is known as a `statement terminator` in C#. It's employed to signify the end of a specific statement or command in the code. Using the semicolon as a statement terminator is common in many programming languages, including `C++`, `Java`, and `JavaScript`.

```csharp
int x = 10;  // The semicolon terminates the variable declaration statement.

Console.WriteLine(x);  // The semicolon terminates the method call statement.

x++;  // The semicolon terminates the increment operation.

```

By correctly terminating each statement, the compiler can discern where one command ends and the next begins. Neglecting to include a semicolon at the end of a statement often results in compile-time errors.

## 6\. Statements & Expressions

A statement in C# represents a complete command to perform a specific action.

An expression, on the other hand, is a combination of operands (variables, literals, method calls, etc.) and operators ( `+, -, *, /, %, etc.`) that can be evaluated to a single value.

```csharp
int sum = 10 + 20; // This line is a statement
10 + 20; // This is an expression

```

## 7\. Blocks of Code

Blocks in C# are sections of code enclosed in braces ( `{ }`). They are typically used to group multiple statements together to form a single executable unit, such as the body of a method, loop, or conditional statement.

```csharp
if (number > 5)
{
    Console.WriteLine("The number is greater than 5");
    number--;
}

```

## 8\. Comments

Comments in C# are used to add explanatory notes in the source code. Single-line comments begin with two forward slashes ( `//`), and multi-line comments are enclosed between `/* and */`. The C# compiler ignores comments.

```csharp
// This is a single-line comment

/* This is a
   multi-line
   comment */

```

## 9\. Read Compiler Errors

The C# compiler provides incredible verbosity with its error messages. Don't just discard the output as "Oh no, it's an error"; it will contain valuable information, generally indicating the root problem.

A typical C# compiler error message has three parts:

```bash
/tmp/X/Program.cs(5,21): error CS0029: Cannot implicitly convert type 'string' to 'int'

```

1. `Error Location`: This tells you where in your code the error occurred, typically indicated by a line number and a character position.
2. `Error Code`: This alphanumeric code uniquely identifies the error type. It is helpful when looking up additional information about the error.
3. `Error Description`: This part of the message describes the error in plain English. It provides insights into what rule was violated in the code.


# Understanding Variables, Constants, and Data Types in C\#

In C#, as with any programming language, you must handle and manipulate data. To do this, you work with variables and constants which store values and represent different data types. Understanding how to use variables, constants, and data types correctly and effectively is fundamental to programming.

## Variables

A variable in C# is a name given to a storage area in memory, with the value stored being changeable. Variables are defined by two key properties: a name and a data type.

The name, or identifier, of a variable, is how you refer to the stored data within your code. Variable names in C# can consist of letters, numbers, and underscores, but they must always start with a letter or an underscore.

The data type of a variable determines what kind of data the variable can store. To declare a variable in C#, you first specify the data type, followed by the variable name:

```csharp
int myNumber;

```

You can also assign a value to the variable at the time of declaration:

```csharp
int myNumber = 10;

```

## Constants

A constant in C# is similar to a variable in that it's a name given to a storage area in memory. However, the value of a constant, as the name implies, remains constant throughout the program; once it's been set, it cannot be changed.

To declare a constant in C#, you use the `const` keyword, followed by the data type, the constant name, and an assignment to set the constant's value:

```csharp
const int myConstant = 10;

```

C# will throw an error if you trying to modify a constant. Constants can be helpful when you use a value repeatedly throughout your code and know it will not change.

## Enums

`Enums`, or enumerations, are a special type of value type in C#. They are particularly useful for representing a distinct set of named constants, providing a more human-readable form for a specific set of integral values.

```csharp
public enum DayOfWeek
{
    Sunday,
    Monday,
    Tuesday,
    Wednesday,
    Thursday,
    Friday,
    Saturday
}

```

In this case, `DayOfWeek` is an `enum` that represents the seven days of the week. Each day is an enumerator. By default, the first enumerator has the value 0, and the value of each successive enumerator is increased by 1. You can also specify the underlying integral type and assign specific values to the enumerators, like so:

```csharp
public enum Month : byte
{
    January = 1,
    February = 2,
    // And so on...
}

```

Here, `Month` is an `enum` with an underlying type of `byte`, and each month is explicitly assigned a value representing its position in the year.

You can use `enums` in your code to make it more readable and safer, as it limits the possible values you can assign.

```csharp
DayOfWeek today = DayOfWeek.Monday;

```

This clearly indicates that the variable `today` can only hold one of the seven days of the week. Trying to assign it any other value will result in a compile-time error.

## Data Types

Understanding the different data types, their characteristics, and their appropriate use is crucial in C#. Each data type serves a specific purpose, and choosing the right one can influence your code's functionality and efficiency. Here's a closer look at the primary data types in C#:

Integer Types are used to store whole numbers without decimal points. There are several integer types in C#, each of which can store a different range of values:

```csharp
byte aByte = 255; // Range: 0 to 255
sbyte aSbyte = -128; // Range: -128 to 127
short aShort = -32768; // Range: -32,768 to 32,767
ushort aUshort = 65535; // Range: 0 to 65,535
int anInt = -2147483648; // Range: -2,147,483,648 to 2,147,483,647
uint aUint = 4294967295; // Range: 0 to 4,294,967,295
long aLong = -9223372036854775808; // Range: -9,223,372,036,854,775,808 to 9,223,372,036,854,775,807
ulong aUlong = 18446744073709551615; // Range: 0 to 18,446,744,073,709,551,615

```

Floating Point Types are used to store numbers with decimal points. They include the `float` and `double` types:

```csharp
float aFloat = 3.1415927f; // Range: ±1.5 x 10^-45 to ±3.4 x 10^38, Precision: 7 digits
double aDouble = 3.141592653589793; // Range: ±5.0 x 10^-324 to ±1.7 x 10^308, Precision: 15-16 digits

```

The Decimal Type is used for large or small decimal numbers and for financial and monetary calculations where precision is critical.

```csharp
decimal aDecimal = 3.14159265358979323846m; // Range: ±1.0 x 10^-28 to ±7.9 x 10^28, Precision: 28-29 digits

```

The Boolean Type is a logical data type with two values, `true` or `false`.

```csharp
bool aBool = true; // or false

```

The Character Type is used to store a single Unicode character.

```csharp
char aChar = 'C'; // Can be a letter, a number, a symbol, or a special character like a newline (`\n`) or a tab (`\t`)

```

The String Type is used to store a sequence of characters or text.

```csharp
string aString = "Hello, World!";

```

In rare scenarios, you might not know the variable type at compile time. For such cases, C# provides a special type called `var`. The `var` keyword instructs the compiler to infer the variable type from the expression on the right side of the initialisation statement. The compiler then assigns the most appropriate type.

```csharp
var number = 10; // The compiler will infer that 'number' is an integer
var message = "Hello, World!"; // Here, 'message' is inferred as a string

```

It's important to note that `var` can only be used when a variable is declared and initialised simultaneously. Once a variable is declared with `var` and initialised, its type cannot be changed; it remains strongly typed.

```csharp
var myVariable = 10;
myVariable = "Hello"; // This will cause a compile error

```

In this example, even though we used `var` for declaration, the compiler inferred `myVariable` to be of type `int` because it was initialised with an integer. So, trying to assign a string value to it later in the code results in a compile-time error.

Using `var` can make your code cleaner and easier to read, particularly when dealing with complex types such as generics or anonymous types. However, overuse of `var` can make your code harder to understand, as it's unclear what type each variable is. Use it sparingly.

In addition to these types, C# also supports Nullable Types, which can represent the normal range of values for its underlying value type, plus an additional null value. These are explained more on the next page.

```csharp
int? nullableInt = null;

```


# Operators in C\# and Type Conversion

* * *

## Operators in C\#

Operators are an integral part of any programming language, enabling specific operations between operands, thus allowing the creation of complex expressions and conditions. C# offers many operators: arithmetic, relational, logical, bitwise, assignment, unary, ternary, and null conditional.

### Arithmetic Operators

In C#, these operators enable mathematical operations. They include `+` (addition), `-` (subtraction), `*` (multiplication), `/` (division), and `%` (modulus, which gives the remainder of a division).

```csharp
int a = 10;
int b = 5;

int sum = a + b; // Result: 15
int difference = a - b; // Result: 5
int product = a * b; // Result: 50
int quotient = a / b; // Result: 2
int remainder = a % b; // Result: 0

```

### Relational Operators

These compare two values and determine the relationship between them. C# includes `==` (equal to), `!=` (not equal to), `>` (greater than), `<` (less than), `>=` (greater than or equal to), and `<=` (less than or equal to).

```csharp
int a = 10;
int b = 20;

bool isEqual = (a == b); // Result: false
bool isNotEqual = (a != b); // Result: true
bool isGreaterThan = (a > b); // Result: false
bool isLessThan = (a < b); // Result: true
bool isGreaterThanOrEqualTo = (a >= b); // Result: false
bool isLessThanOrEqualTo = (a <= b); // Result: true

```

### Logical Operators

These operators use Boolean ( `true` or `false`) values to create logical expressions. C# provides `&&` (logical AND), `||` (logical OR), and `!` (logical NOT).

```csharp
bool isTrue = true;
bool isFalse = false;

bool andResult = isTrue && isFalse; // Result: false
bool orResult = isTrue || isFalse; // Result: true
bool notResult = !isTrue; // Result: false

```

### Bitwise Operators

Bitwise operators are useful when working with binary data, which is common in fields such as cryptography or image processing where you need to manipulate individual bits within a block of data. Bitwise Operators offer a level of precision that is impossible with conventional arithmetic or logical operators.

They include `&` (bitwise AND), `|` (bitwise OR), `^` (bitwise XOR), `~` (bitwise NOT), `<<` (left shift), and `>>` (right shift).

| Operator | Description |
| --- | --- |
| `&` (bitwise AND) | Compares each bit of the first operand to the corresponding bit of the second operand. If both bits are 1, the corresponding result bit is set to 1. Otherwise, the result bit is set to 0. |
| \| (bitwise OR) | Compares each bit of the first operand to the corresponding bit of the second operand. If either bit is 1, the corresponding result bit is set to 1. If both bits are 0, the result bit is set to 0. |
| `^` (bitwise XOR) | Compares each bit of the first operand to the corresponding bit of the second operand. If the bits are not identical, the corresponding result bit is set to 1. If they are identical, the result bit is set to 0. |
| `~` (bitwise NOT) | Flips the bits of its operand. If a bit is 0, it becomes 1; if a bit is 1, it becomes 0. |
| `<<` (left shift) | Moves the bits of the operand to the left by the number of places specified by the second operand. Bits that are shifted off the left are discarded, and zeros are shifted in on the right. |
| `>>` (right shift) | Moves the bits of the operand to the right by the number of places specified by the second operand. Bits that are shifted off the right are discarded, and zeros are shifted in on the left. |

```csharp
int a = 240; // Binary: 1111 0000
int b = 15; // Binary: 0000 1111

int andResult = a & b; // Result would be 0, Binary: 0000 0000
int orResult = a | b; // Result would be 255, Binary: 1111 1111
int xorResult = a ^ b; // Result would be 255, Binary: 1111 1111
int notResult = ~a; // Result would be -241, Binary: 0000 1111
int leftShift = a << 2; // Result would be 960, Binary: 11 1100 0000
int rightShift = a >> 2; // Result would be 60, Binary: 0011 1100

```

### Assignment Operators

C# includes `=` (simple assignment), and compound assignment operators like `+=`, `-=`, `*=`, `/=`, and `%=`, which combine an arithmetic operation with assignment.

```csharp
int a = 10; // simple assignment

a += 5; // equivalent to a = a + 5, so a now is 15
a -= 3; // equivalent to a = a - 3, so a now is 12
a *= 2; // equivalent to a = a * 2, so a now is 24
a /= 4; // equivalent to a = a / 4, so a now is 6
a %= 5; // equivalent to a = a % 5, so a now is 1

```

### Unary Operators

Unary operators are those that operate on a single operand. They include `++` (increment), `--` (decrement), `+` (unary plus, denotes positive values), and `-` (unary minus, denotes negative values). Unary operators also include the `!` logical negation operator mentioned earlier.

```csharp
int a = 5;
a++; // Now a is 6
a--; // Now a is 5 again
int b = +a; // b is 5
int c = -a; // c is -5

```

### Ternary Operator

Ternary operators provide a shorthand way of writing an `if-else` condition. The syntax is `condition ? true expression : false expression`. `if-else` and other control flow statements are explained in `Control Statements and Loops`.

Consider the following example:

```csharp
int a = 10;
int b = 20;

// expanded if-else
if (a > b)
{
    result = "a is greater";
}
else
{
    result = "b is greater";
}

// contracted ternary
string result = a > b ? "a is greater" : "b is greater";

```

In this case, because `a` is not greater than `b`, the result would be `"b is greater"`.

### Null Conditional Operators

These operators, introduced in C# 6.0, are used to access members and elements of an object safely. They return `null` if the object is `null` instead of throwing a `NullReferenceException`.

There are two null conditional operators:

1. `Null Conditional Member Access (?.)`: facilitates the safe access of an object's members, including properties or methods. As depicted in your second example, the Length property of the `authorName` string is being accessed. If `authorName` is `null`, a `NullReferenceException` will not be thrown. Instead, it will simply yield `null`.
2. `Null Conditional Element Access (?[])`: utilised to secure access to array or collection elements. When the array or collection is `null`, using `?[]` to access an element won't result in an exception. Rather, it will return `null`. For instance, in your first example, as `authors` is `null`, `authors?[0]` consequently returns `null`.

```csharp
string[] authors = null;
var author1 = authors?[0]; // This will not throw an exception even though authors is null. author1 will simply be null.

string authorName = null;
int? length = authorName?.Length; // Again, this will not throw an exception. length will be null.

```

In both cases, if the objects ( `authors` and `authorName`) were not null, the respective indices and properties would be accessed normally. However, since they are null, the operators prevent a `NullReferenceException` and return `null`. These operators have significantly enhanced how developers handle null references in C#, providing a more compact and streamlined way to ensure safe access to members of potentially null objects.

### Null-coalescing Operator

In C#, the null-coalescing operator is a binary operator that simplifies checking for null values. It is represented by a double question mark `??`.

The null-coalescing operator returns the value of its left-hand operand if it is not null; otherwise, it evaluates the right-hand operand and returns its result.

```csharp
int? x = null;
int y = x ?? -1;

```

Since `x` is null, the value `-1` is assigned to `y` in this example.

This operator is particularly useful for providing default values when a variable is null. Without the null-coalescing operator, you would need to use an `if` statement to check for null values:

```csharp
int? x = null;
int y;

if (x != null)
    y = x.Value;
else
    y = -1;

```

As you can see, using the null-coalescing operator `??` makes the code much more concise and easier to read. You can also use the null-coalescing assignment operator `??=`. This operator assigns the value of its right-hand operand to its left-hand operand only if the left-hand operand evaluates to null:

```csharp
int? x = null;
x ??= -1;  // x is now -1 because it was null

```

## Type Conversion

In programming, especially in a statically typed language like C#, it is often necessary to convert data from one type to another. This could be because an operation requires a certain data type, or you need to interact with an API that expects a different one. This process is called type conversion, and there are two types of conversions in C#: implicit and explicit.

### Implicit Type Conversion (or Widening Conversion)

The compiler performs These conversions automatically without the programmer's intervention. They happen when converting a smaller type to a larger type (like `int` to `long` or `float`), or a derived class to its base. These conversions are safe and do not lead to data loss.

```csharp
int numInt = 10;
long numLong = numInt; // Implicit conversion from int to long

```

### Explicit Type Conversion (or Narrowing Conversion)

The programmer performs These conversions manually using predefined functions. Explicit conversions require a cast operator. They happen when converting a larger type to a smaller type (like `long` to `int`) or a base class to its derived. These conversions can lead to data loss or a `System.OverflowException`.

```csharp
double numDouble = 10.5;
int numInt = (int)numDouble; // Explicit conversion from double to int. numInt will be 10, the fractional part is lost

```

C# also supports built-in methods for converting types, particularly from/to string types, like `ToString()`, `ToInt32()`, `ToDouble()`, etc., which are part of the `Convert` class.

```csharp
int numInt = 10;
string str = numInt.ToString(); // Converts numInt to a string
int num = Convert.ToInt32(str); // Converts str back to an integer

```

## Type Checking

C# provides operators to check the type of an object: the `is` operator and the `as` operator.

### is

It checks whether an object is compatible with a given type, and the result of the operation is `bool`.

```csharp
string str = "Hello, World!";
bool result = str is string; // result will be true

```

### as

It is used for casting between compatible reference types or nullable types. If the cast fails, it returns `null` instead of throwing an exception.

```csharp
object obj = new string("Hello, World!");
string str = obj as string; // str will be "Hello, World!" if the cast is successful; otherwise, it will be null

```


# Namespaces

In C#, a namespace is a way to group related code elements into logical units, such as `classes`, `interfaces`, `enums`, and more. Namespaces provide organisation and help avoid naming conflicts by creating a `hierarchical structure` for code. They serve as `containers` for `organising and categorising code elements`, making managing and maintaining large codebases easier. Namespaces also enable code reuse and `promote modularity` by clearly `separating concerns`.

The primary purposes of namespaces are twofold:

1. `Organization`: Namespaces systematically organise code elements based on their functionality or domain. They help developers locate and navigate code more efficiently, enhancing code readability and maintainability.

2. `Avoiding Naming Conflicts`: Namespaces prevent naming conflicts by providing a unique context for code elements. Code elements within a namespace are distinguished by their fully qualified names, which include the namespace name as a prefix. This ensures that code elements with the same name coexist within different namespaces.


Namespaces exist in other languages too:

- `Java`: In Java, the equivalent of a namespace is a `package`. Packages in Java help categorise the classes and interfaces, making organising your application easier.
- `Python`: In Python, a similar concept to namespaces is implemented using `modules`. A Python module is a file containing Python definitions and statements. The file name is the module name with the suffix `.py` added.
- `JavaScript (ES6)`: With the introduction of ES6, JavaScript added `modules`. A module is essentially a script that can import and export objects defined in other modules.
- `C++`: Just like in C#, C++ uses a namespace to group related types and objects. The usage and benefits are very similar to those in C#.

## Creating and Organizing Code Using Namespaces

To create a namespace in C#, use the `namespace` keyword followed by the name. Code elements, such as classes, etc., are defined within the namespace.

```csharp
namespace MyNamespace
{
    class MyClass
    {
        // Class implementation
    }

    interface IMyInterface
    {
        // Interface implementation
    }
}

```

The above example defines a namespace named `MyNamespace`, containing the `MyClass` class and the `IMyInterface` interface. There are a few points to keep in mind when implementing namespaces:

1. `Group-Related Functionality`: Place code elements closely related in the same namespace. This ensures that code with similar functionality is grouped, making it easier to locate and understand.

2. `Avoid Over-Nesting`: Keep the namespace hierarchy concise and avoid excessive nesting. Deeply nested namespaces can lead to long, complex names hindering code readability.

3. `Follow a Logical Structure`: Create a logical structure for your namespaces that aligns with your project's architecture or module organisation. Consider using a naming convention that reflects the organisation of your codebase.


## Importing and Using Namespaces in C\# Programs

You have two options to use code elements from a namespace in a C# program: either fully qualify the code element's name with the namespace, or import the namespace via the `using` directive.

```csharp
using System;

namespace MyNamespace
{
    class Program
    {
        static void Main()
        {
            // Using a fully qualified name
            System.Console.WriteLine("Hello, World!");

            // Using the imported namespace
            Console.WriteLine("Hello, World!");
        }
    }
}

```

In the above example, the `System` namespace is imported using the `using` directive. This allows us to use `Console.WriteLine()` directly without fully qualifying it with the `System` namespace.

Importing namespaces using the `using` directive can significantly reduce code verbosity and improve readability. However, avoiding unnecessary or excessive importing of namespaces is important to prevent potential naming conflicts or confusion.

## Resolving Naming Conflicts with Namespaces

A naming conflict occurs when multiple namespaces define code elements with the same name. C# provides ways to resolve such conflicts to ensure unambiguous access to code elements.

To resolve naming conflicts, you can use one of the following approaches:

1. `Fully Qualify the Code Element`: Use the fully qualified name of the code element, including the namespace, to ensure explicit identification.

```csharp
namespace MyNamespace
{
    class MyClass { }

    class Program
    {
        static void Main()
        {
            // Using fully qualified name to avoid naming conflict
            MyNamespace.MyClass myObject = new MyNamespace.MyClass();
        }
    }
}

```

1. `Alias the Namespace`: When importing, use an alias to differentiate between conflicting namespaces. This provides a shorthand way to refer to the code elements without ambiguity.

```csharp
using MyAlias = MyNamespace;
using AnotherAlias = AnotherNamespace;

namespace MyNamespace
{
    class MyClass { }
}

namespace AnotherNamespace
{
    class MyClass { }

    class Program
    {
        static void Main()
        {
            // Using aliases to differentiate between conflicting namespaces
            MyAlias.MyClass myObject1 = new MyAlias.MyClass();
            AnotherAlias.MyClass myObject2 = new AnotherAlias.MyClass();
        }
    }
}

```


# Console I/O

Console applications run in a console window (also known as a command line interface) instead of a graphical user interface (GUI). In a console application, users interact with the program by entering commands as text, and the program responds with text-based output. The `Console` class provides methods and properties to interact with the console. These include functionalities such as reading from and writing to the console, changing the colour of the console text and background, changing the title of the console window, and altering the size and position of the console window, among others.

## Console.Read

The `Console.Read` method is a member of the `Console` class and is utilised for reading a single character from the standard input stream, which is typically the keyboard. The primary feature of this method is that it blocks the current thread of execution until a character is available. This effectively pauses the program, awaiting user input.

When the user inputs a character and presses the enter key, `Console.Read` retrieves the ASCII value of the character and returns it as an integer. If the end of the input stream has been reached, this method will return -1.

```csharp
Console.Write("Please press a key: ");
int input = Console.Read();
Console.WriteLine("You pressed: " + (char)input);

```

In this code, the `Console.Read` method is used to capture the user's key press, and the ASCII value returned is converted back into a character for display.

## Console.ReadLine

The `Console.ReadLine` method, another member of the `Console` class, is designed to read an entire line of input from the standard input stream. Unlike `Console.Read`, which reads a single character, `Console.ReadLine` captures all characters input by the user until they press the enter key.

Upon pressing the enter key, `Console.ReadLine` returns the captured input as a string. If no further lines are available (i.e., the end of the input stream is reached), the method will return null.

```csharp
Console.Write("Please enter your name: ");
string name = Console.ReadLine();
Console.WriteLine("Hello, " + name);

```

In this example, `Console.ReadLine` captures the user's name as a string. The program then greets the user using the provided name.

## Console.Write

The `Console.Write` method is a fundamental mechanism for displaying output to the console in C#. It is designed to write the specified string value to the standard output stream, typically the console window. This method does not append a trailing newline character to the output. As a consequence, any subsequent calls to `Console.Write` or `Console.WriteLine` will continue on the same line in the console.

It's important to note that `Console.Write` can handle other data types in addition to strings. It accomplishes this by automatically invoking the `ToString` method on the provided argument, converting it to a string before output.

```csharp
Console.Write("Pi is approximately ");
Console.Write(3.14159);

```

In this example, the first `Console.Write` call outputs a string, while the second outputs a floating-point number. The `ToString` method is implicitly called to convert the number into a string for display.

## Console.WriteLine

The `Console.WriteLine` method behaves very similarly to `Console.Write`, with one key distinction: it automatically appends a newline character ( `\n`) after the output. This has the effect of moving the cursor to the beginning of the next line in the console. Therefore, any subsequent `Console.Write` or `Console.WriteLine` calls will start outputting on a new line.

```csharp
Console.WriteLine("Hello, World!");
Console.WriteLine("Today's date is " + DateTime.Now.ToShortDateString());

```

In this example, the first `Console.WriteLine` call outputs a greeting and moves the cursor to the next line. The second call outputs a string concatenated with today's date, obtained via `DateTime.Now.ToShortDateString()` and converted to a string via implicit use of `ToString`.


# Control Statements and Loops

* * *

## Control Statements

In C#, control flow statements allow your code to execute different branches based on conditions being met or not. `If`, `else-if`, and `switch` are three types of control statements that are commonly used.

### if

The `if` statement represents the most fundamental type of control flow statement. It evaluates a condition, and if that condition returns `true`, it executes a corresponding code block.

```csharp
int number = 10;
if (number > 0) {
    Console.WriteLine("The number is positive.");
}

```

In the above example, the `if` statement checks whether the number is greater than 0. As this condition is `true`, it prints "The number is positive."

### else

The `else` statement is used alongside the `if` statement. It allows you to specify a block of code to be executed if the condition in the `if` statement is `false`.

```csharp
int number = -10;
if (number > 0) {
    Console.WriteLine("The number is positive.");
}
else {
    Console.WriteLine("The number is not positive.");
}

```

In this case, since the number is not greater than 0, the condition in the `if` statement is `false`, so the code inside the `else` block is executed, printing "The number is not positive."

### else if

The `else if` statement presents an opportunity to specify new conditions for testing if the initial `if` statement's condition evaluates to `false`.

```csharp
int number = 0;
if (number > 0) {
    Console.WriteLine("The number is positive.");
}
else if (number < 0) {
    Console.WriteLine("The number is negative.");
}
else {
    Console.WriteLine("The number is zero.");
}

```

In this example, if the number is greater than 0, it prints "The number is positive." If the number is less than 0, it prints "The number is negative." If neither condition is `true`, it prints "The number is zero."

### switch

The `switch` statement is a type of selection statement that chooses a single switch section to execute from a list of candidates based on a pattern match with the match expression.

```csharp
int number = 1;
switch (number) {
    case 1:
        Console.WriteLine("One");
        break;
    case 2:
        Console.WriteLine("Two");
        break;
    default:
        Console.WriteLine("None");
        break;
}

```

In this case, the `switch` statement evaluates the `number`. It matches the `number` with the cases, and if it finds a match, it executes the code in that case block. In the example above, it would print "One."

The `break` statement serves to terminate the `switch` statement. The absence of the `break` can result in a fall-through to subsequent cases, potentially causing undesired outcomes.

The `default` case within a `switch` statement defines the block of code to be executed should no other cases match the `number`. In the example, if the number was neither 1 nor 2, "None" would be printed.

These conditional statements constitute powerful instruments enabling programmers to control the flow of execution based on varying conditions. Gaining a comprehensive understanding and effectively employing these tools can yield more efficient and adaptable C# programs.

## Loops

In C#, looping constructs are used to execute a block of code multiple times, which is necessary for many programming tasks. The major looping constructs in C# include `for`, `while`, and `do-while`.

### for

The `for` loop is a control flow statement facilitating repeated execution of code. It is typically characterised by three components: an initialiser (where you establish your counter variable), a condition (which prompts continuation of the loop if `true` and termination if `false`), and an iterator (which typically increments the counter variable).

```csharp
for (int i = 0; i < 5; i++) {
    Console.WriteLine(i);
}

```

In this example, the numbers from 0 to 4 are printed. The loop initiates with `i` equal to 0 and proceeds if `i` is less than 5. Following each iteration, `i` is incremented by 1.

### while

The `while` loop is another control flow statement that allows code to be executed repeatedly based on a given condition. The loop can be thought of as a repeating `if` statement.

```csharp
int i = 0;
while (i < 5) {
    Console.WriteLine(i);
    i++;
}

```

This `while` loop will do the same thing as the `for` loop in the previous example. It will print the numbers 0 to 4. The loop begins by checking if `i` is less than 5. If the condition is `true`, it executes the code within the loop and increments `i` by 1. It will continue to check this condition before each iteration.

### do-while

The `do-while` loop closely resembles the `while` loop, with one notable difference: the `do-while` loop evaluates its condition at the end of the loop. This implies that the loop's code block is executed at least once, irrespective of the condition.

```csharp
int i = 0;
do {
    Console.WriteLine(i);
    i++;
} while (i < 5);

```

Similarly to the previous two examples, this `do-while` loop prints the numbers 0 to 4. The loop executes the code block before evaluating the condition. If the condition is `true`, the loop proceeds; if `false`, the loop terminates.

Understanding these looping constructs is essential to efficient programming in C#, as they present versatile ways to control the flow of your program.

## Break, continue and goto

In C#, `break`, `continue`, and `goto` statements enable you to control your program's execution flow. They are particularly valuable within loop constructs and switch statements.

### break

The `break` statement terminates the enclosing loop or switch statement and transfers the execution to the statement immediately succeeding the loop or switch.

```csharp
for (int i = 0; i < 10; i++)
{
    if (i == 5)
    {
        break;
    }
    Console.WriteLine(i);
}

```

In this scenario, the loop prints the numbers from 0 to 4. Once `i` equals 5, the `break` statement is executed, causing an immediate termination of the loop, irrespective of the loop condition.

### continue

The `continue` statement is used in a loop to skip the rest of the current iteration and immediately start the next iteration.

```csharp
for (int i = 0; i < 10; i++)
{
    if (i == 5)
    {
        continue;
    }
    Console.WriteLine(i);
}

```

This loop will print the numbers from 0 to 9 but skip 5. When `i` equals 5, the `continue` statement is executed, the current iteration is terminated, and the next iteration begins.

### goto

The `goto` statement transfers the program control directly to a labelled statement. A common use of `goto` is to transfer control from a nested loop to an outer loop or to exit deeply nested loops.

```csharp
for (int i = 0; i < 3; i++)
{
    for (int j = 0; j < 3; j++)
    {
        if (i == 1 && j == 1)
        {
            goto outer;
        }
        Console.WriteLine($"i:{i}, j:{j}");
    }
    outer: Console.WriteLine("Exited from the inner loop");
}

```

In this example, the `goto` statement is executed when `i` equals 1 and `j` equals 1, which causes control to jump immediately to the labelled statement `outer`, effectively breaking out of the inner loop.

`Please note` \- overuse of the `goto` statement can make your code harder to read and understand, and it is generally discouraged in modern programming. Try to use it sparingly, and consider using alternative statements, such as `break` or `continue`.


# Arrays

* * *

Arrays are a crucial aspect of C# programming and most other programming languages as well. Their importance is due to their ability to store multiple values of the same type in a structured manner.

## Arrays in C\#

To declare an array in C#, the syntax involves specifying the type of elements that the array will hold, followed by square brackets `[]`. This tells the compiler that this variable will hold an array, but it does not yet specify the size or elements of the array.

```csharp
int[] array;

```

This line of code simply declares an array named `array` that will hold integers. The array does not yet exist in memory at this point - it is simply a declaration.

To create the array in memory, we instantiate it using the `new` keyword, followed by the type of the array elements and the number of elements enclosed in square brackets.

```csharp
array = new int[5];

```

In this line of code, we are telling the compiler to create an array of integers with a size of 5. At this point, the `array` variable references an array of five integer elements, all of which are initialised to 0, the default value for integers.

Arrays can also be declared, instantiated, and initialised in a single line of code.

```csharp
int[] array = new int[] { 1, 2, 3, 4, 5 };

```

This line declares an array of integers, creates it with a size of 5, and assigns the specified values to the five elements.

## Multidimensional Arrays in C\#

C# supports multidimensional arrays. This concept can be extended to two, three, or more dimensions. A two-dimensional array can be considered a table with rows and columns.

The syntax for declaring a two-dimensional array involves specifying the type of elements that the array will hold, followed by two sets of square brackets `[,]`.

```csharp
int[,] matrix;

```

Here, `matrix` is a two-dimensional array that will hold integers. The new keyword is used to instantiate the matrix, followed by the type of the array elements and the number of rows and columns enclosed in square brackets.

```csharp
matrix = new int[3, 3];

```

This line creates a matrix with 3 rows and 3 columns.

Two-dimensional arrays can also be declared, instantiated, and initialised in a single line of code.

```csharp
int[,] matrix = new int[,] { { 1, 2, 3 }, { 4, 5, 6 }, { 7, 8, 9 } };

// Use the GetLength method to get the number of rows (dimension 0) and columns (dimension 1)
for (int i = 0; i < matrix.GetLength(0); i++) {
    for (int j = 0; j < matrix.GetLength(1); j++)
    {
        // Access each element of the array using the indices
        Console.Write(matrix[i, j] + " ");
    }
    Console.WriteLine(); // Print a newline at the end of each row
}

```

This example will output:

```
1 2 3
4 5 6
7 8 9

```

This representation shows the `matrix` as it is, conceptually, a 3x3 grid. Each row of numbers in the output corresponds to a row in the matrix, and each number in a row corresponds to a column for that row in the matrix.

You can access the elements in the array using their indices. In a 2D array, the first index represents the row number, and the second index represents the column number. For instance, `matrix[0, 1];` will access the second element of the first row.

## The Array Class

The `Array` class, part of the `System` namespace, offers various methods that help in efficiently managing and manipulating arrays.

The distinction between `Array` and `array` in C# can be somewhat confusing, primarily because both represent similar concepts but in different ways. `Array` is an abstract base class provided by the `System` namespace in `C#`. It provides various properties and methods like `Length`, `Sort()`, `Reverse()`, and many more that allow you to manipulate arrays.

An `array`, on the other hand, is a fundamental data type in C#. It is a low-level construct supported directly by the language. An `array` represents a fixed-size, sequential collection of elements of a specific type, such as int, string, or custom objects.

Let's look at an example:

```csharp
int[] arr = new int[5]; //arr is an array

```

Here, `arr` is an array of integers. You can add, retrieve, or modify elements using their indices.

```csharp
arr[0] = 1; // Assigns the value 1 to the first element of the array.

```

On the other hand, if you want to use the functionality provided by the `Array` class on this array:

```csharp
Array.Sort(arr); // Uses the Sort method from Array class to sort 'arr'.

```

### Array.Sort()

The `Sort()` method is used to sort the elements in an entire one-dimensional `Array` or, alternatively, a portion of an `Array`.

```csharp
int[] numbers = {8, 2, 6, 3, 1};
Array.Sort(numbers);

```

After sorting, our array would look like: `{1, 2, 3, 6, 8}`.

### Array.Reverse()

The `Reverse()` method reverses the sequence of the elements in the entire one-dimensional `Array` or a portion of it.

For instance:

```csharp
int[] numbers = {1, 2, 3};
Array.Reverse(numbers);

```

The result will be a reversed array: `{3, 2, 1}`.

### Array.IndexOf()

The `IndexOf()` method returns the index of the first occurrence of a value in a one-dimensional `Array` or in a portion of the `Array`.

Consider this example:

```csharp
int[] numbers = {1, 2, 3};
int index = Array.IndexOf(numbers, 2);

```

The variable `index` now holds the value `1`, which is the index of number `2` in the array.

### Array.Clear()

The `Clear()` method sets a range of elements in the `Array` to zero (in case of numeric types), false (in case of boolean types), or null (in case of reference types).

Take a look at this example:

```csharp
int[] numbers = {1, 2, 3};
Array.Clear(numbers, 0, numbers.Length);

```

Now all elements in our array are set to zero: `{0, 0, 0}`.


# Strings

In C#, a string is not simply a character array, although it can be thought of as akin to an array of characters for some operations. In essence, a string is an instance of the `System.String` class that provides a range of sophisticated methods and properties, encapsulating a sequence of Unicode characters.

The main differentiation between a string and a character array is that strings in C# are immutable, meaning that once created, they cannot be changed. Any operations that appear to alter the string are actually creating a new string and discarding the old one. This design enhances security and improves performance for static or rarely changing text.

On the other hand, character arrays are mutable, and individual elements can be changed freely. This mutability comes at the cost of not having built-in text manipulation and comparison methods, as strings do.

For instance, we create a string as follows:

```csharp
string welcomeMessage = "Welcome to Academy!";

```

Once you have a string in C#, there are many operations you can perform on it. The `Length` property, for example, returns the number of characters in the string.

```csharp
Console.WriteLine(welcomeMessage.Length); // Outputs: 19

```

This tells us that our `welcomeMessage` string is 19 characters long.

String concatenation is another operation that is used frequently. It is performed using the `+` operator.

```csharp
string firstString = "Welcome ";
string secondString = "to Academy!";
string concatenatedString = firstString + secondString;
Console.WriteLine(concatenatedString); // Outputs: "Welcome to Academy!"

```

When it comes to manipulating the casing of strings, the `String` class provides the `ToLower` and `ToUpper` methods. `ToLower` converts all the characters in a string to lowercase, while `ToUpper` converts them all to uppercase.

```csharp
string lowerCaseString = welcomeMessage.ToLower();
Console.WriteLine(lowerCaseString); // Outputs: "welcome to academy!"

string upperCaseString = welcomeMessage.ToUpper();
Console.WriteLine(upperCaseString); // Outputs: "WELCOME TO ACADEMY!"

```

There are also methods to check whether a string starts or ends with a specific substring. These are the `StartsWith` and `EndsWith` methods, respectively.

```csharp
bool startsWithWelcome = welcomeMessage.StartsWith("Welcome");
Console.WriteLine(startsWithWelcome); // Outputs: True

bool endsWithProgramming = welcomeMessage.EndsWith("Academy!");
Console.WriteLine(endsWithProgramming); // Outputs: True

```

A common requirement in programming is to determine whether a specific substring exists within a larger string. This can be accomplished with the `Contains` method.

```csharp
bool containsCsharp = welcomeMessage.Contains("C#");
Console.WriteLine(containsCsharp); // Outputs: False

```

Sometimes, you may need to replace all occurrences of a substring within a string with another substring. The `Replace` method allows you to do this.

```csharp
string replacedMessage = welcomeMessage.Replace("Academy", "HTB Academy");
Console.WriteLine(replacedMessage); // Outputs: "Welcome to HTB Academy!"

```

You can use the `Equals` method or the `==` operator when comparing two strings for equality. Both perform a case-sensitive comparison by default.

```csharp
string str1 = "Welcome";
string str2 = "welcome";
bool areEqual = str1.Equals(str2);
Console.WriteLine(areEqual); // Outputs: False

```

In addition to the basic operations mentioned above, there are several advanced operations that C# offers for string manipulation.

One of these operations is string interpolation, which provides a more readable and convenient syntax to format strings. Instead of using complicated string concatenation to include variable values within strings, string interpolation allows us to insert expressions inside string literals directly. To create an interpolated string in C#, prefix the string with a `$` symbol, and enclose any variables or expressions you want to interpolate in curly braces `{}`. When the string is processed, these expressions are replaced by their evaluated string representations.

```csharp
string name = "Alice";
string greeting = $"Hello, {name}!";
Console.WriteLine(greeting); // Outputs: "Hello, Alice!"

```

In the above example, `{name}` inside the string literal is replaced by the value of the variable `name`.

Another important string operation is trimming, which is performed using the `Trim` method. This is commonly used to remove a string's leading and trailing white space.

```csharp
string paddedString = "    Extra spaces here    ";
string trimmedString = paddedString.Trim();
Console.WriteLine(trimmedString); // Outputs: "Extra spaces here"

```

The `Substring` method extracts a portion of a string starting at a specified index and continuing for a specified length. For instance:

```csharp
string fullString = "Hello, World!";
string partialString = fullString.Substring(7, 5);
Console.WriteLine(partialString); // Outputs: "World"

```

In the above example, `Substring(7, 5)` returns a new string starting at index 7 and of length 5 from the `fullString`.

Moreover, using the `Split` method, strings can be split into arrays of substrings based on delimiters. This is especially useful when parsing input or handling data that comes in string form.

```csharp
string sentence = "This is a sentence.";
string[] words = sentence.Split(' ');
foreach (string word in words)
{
    Console.WriteLine(word);
}
// Outputs:
// "This"
// "is"
// "a"
// "sentence."

```

In this example, the `Split` method splits the `sentence` string into an array of words based on the space character delimiter.

Lastly, the `Join` method concatenates all elements in a string array or collection, using a specified separator between each element.

```csharp
string[] words = { "This", "is", "a", "sentence" };
string sentence = string.Join(" ", words);
Console.WriteLine(sentence); // Outputs: "This is a sentence"

```

In this case, `Join` constructs a single string from all the elements in the `words` array, with a space character as the separator.


# Collections

* * *

In C#, a collection is used to group related objects. Collections provide a more flexible way to work with groups of objects, as unlike arrays, the group of objects you work with can grow and shrink dynamically as the demands of the application change. Collections are defined in the `System.Collections` namespace.

## Iterating through a collection

The `foreach` loop is an efficient and straightforward way to iterate through any collection. It automatically moves to the next item in the collection at the end of each loop iteration, making it an excellent choice for reading collections. Suppose you want to modify the collection while iterating over it. In that case, you might need to use a different looping construct, like a `for` loop, as `foreach` does not support collection modification during iteration.

```csharp
List<int> numbers = new List<int> { 1, 2, 3, 4, 5 };

for (int i = 0; i < numbers.Count; i++)
{
    // Modify the element at index i
    numbers[i] *= 2;
}

foreach (int number in numbers)
{
    Console.WriteLine(number);
}

```

We use a `for` loop to iterate over the numbers list in this example. The loop variable `i` represents the index of each element in the list. Within the loop, we can modify the element at the current index by performing the desired operation, in this case, multiplying it by 2. After the `for` loop completes, we use a `foreach` loop to iterate over the modified `numbers` list and print each number to the console.

## List

A `List<T>` is one of the most commonly used types in .NET, especially when we need a resizable array-like collection. This type is found in the `System.Collections.Generic` namespace is a generic class which supports storing values of any type. However, all `List<T>` elements must be the same type.

```csharp
List<string> namesList = new List<string>();

// Adding elements to the list
namesList.Add("John");
namesList.Add("Jane");
namesList.Add("Alice");

// Accessing elements by index
string firstElement = namesList[0]; // O(1) indexed access

// Modifying an element
namesList[1] = "Emily";

// Checking if an element exists
bool hasAlice = namesList.Contains("Alice");

// Removing an element
namesList.Remove("John");

// Iterating over the elements
foreach (string name in namesList)
{
    Console.WriteLine(name);
}

```

A `List<T>` provides the advantage of dynamic resizing compared to an array. However, this also means that a `List<T>` generally uses more memory than an array, as it allocates extra space to allow for potential growth. If the size of your collection is fixed, using an array could be more memory-efficient.

However, the flexibility and utility of the `List<T>` class methods often outweigh the minor performance and memory usage benefits of arrays in many scenarios. This is especially true in applications where the exact count of elements may change over time.

## Dictionary

A `Dictionary<TKey, TValue>` is a collection that stores and retrieves data using a key-value relationship. It is part of the `System.Collections.Generic` namespace in C#.

To use a `Dictionary<TKey, TValue>`, specify the key type ( `TKey`) and the value ( `TValue`) in the angle brackets. For example, `Dictionary<int, string>` indicates a dictionary where the keys are integers and the values are strings.

```csharp
Dictionary<string, int> studentGrades = new Dictionary<string, int>();

// Adding key-value pairs to the dictionary
studentGrades.Add("John", 85);
studentGrades.Add("Jane", 92);
studentGrades.Add("Alice", 78);

// Accessing values by key
int johnGrade = studentGrades["John"]; // O(1) lookup by key

// Modifying an existing value
studentGrades["Jane"] = 95;

// Checking if a key exists
bool hasAlice = studentGrades.ContainsKey("Alice");

// Removing a key-value pair
studentGrades.Remove("John");

// Iterating over the key-value pairs
foreach (KeyValuePair<string, int> pair in studentGrades)
{
    Console.WriteLine($"Name: {pair.Key}, Grade: {pair.Value}");
}

```

## HashSet

A `HashSet<T>` collection stores an unordered set of unique elements. The primary characteristic of a `HashSet` is its ability to store unique elements, completely disallowing duplication. Adding elements to a `HashSet` will check if the element already exists before adding it. This makes `HashSet` an optimal choice when you need to store a collection of items without any duplicates and do not require a specific order.

To use a `HashSet`, specify the type of elements ( `T`) within the angle brackets. For example, `HashSet<int>` indicates a set of integers.

```csharp
HashSet<string> namesHashSet = new HashSet<string>();

// Adding elements to the set
namesHashSet.Add("John");
namesHashSet.Add("Jane");
namesHashSet.Add("Alice");

// Checking if an element exists
bool hasAlice = namesHashSet.Contains("Alice"); // O(1) membership check

// Removing an element
namesHashSet.Remove("John");

// Iterating over the elements
foreach (string name in namesHashSet)
{
    Console.WriteLine(name);
}

```

## List vs Dictionary vs HashSet

Each collection type has its unique characteristics, behaviours, and use cases.

|  | List | Dictionary | HashSet |
| --- | --- | --- | --- |
| Data Structure | Ordered | Key-Value Pairs | Unordered, Unique Elements |
| Duplication | Allows duplicates | Keys must be unique | Ensures uniqueness |
| Access and Lookup | Indexed access by index | Fast lookup by unique key | Membership checks |
| Ordering | Maintains order | No specific order | No specific order |
| Element Removal | By index or value | By key | By value |
| Memory Overhead | Consumes memory based on elements | Memory for keys and values | Memory for unique elements |
| Use Cases | Ordered collection, indexed access | Associating values with keys, key-based lookup | Unordered collection, uniqueness and membership checks |

## Collection Performance

Performance considerations vary for each collection type based on the operations performed and the specific use case.

`Big-O notation` is a notation used in computer science to describe the performance characteristics of an algorithm, specifically its time complexity and space complexity.

In terms of time complexity, `Big-O notation` quantifies the worst-case scenario of an algorithm as the size of the input data approaches infinity. For instance, if an algorithm has a time complexity of `O(n)`, it indicates that the time it takes to execute the algorithm grows linearly with the input data size. On the other hand, an algorithm with a time complexity of `O(n^2)` would suggest that the execution time increases quadratically with the input size.

While analysed less frequently, `Big-O` notation can also describe space complexity by measuring the amount of memory an algorithm needs relative to the input size. For example, an algorithm with a space complexity of `O(1)` uses a constant amount of memory regardless of the input size.

Here are some general performance considerations for `List`, `Dictionary`, and `HashSet`:

|  | List | Dictionary | HashSet |
| --- | --- | --- | --- |
| Access Speed | Very fast, O(1) | Average: O(1), Worst: O(n) | Average: O(1), Worst: O(n) |
| Insertion/Removal | Insertion and removal at ends: O(1) | Average: O(1), Worst: O(n) | Average: O(1), Worst: O(n) |
| Searching | Unsorted: O(n) <br> Sorted (Binary Search): O(log n) | Key-based lookup: Average O(1), Worst O(n) | Membership check: Average O(1), Worst O(n) |
| Memory Overhead | Relatively low | Keys and values, additional structure fields | Unique elements, additional structure fields |

Please note that the access speed represents the time complexity of accessing elements in the collection, whether it's by index (for List) or by key (for Dictionary) or membership check (for HashSet). The performance characteristics in this table are general guidelines and may vary based on the specific implementation and use case.


# LINQ (Language Integrated Query)

* * *

Language Integrated Query (LINQ) is a feature in C# that provides a consistent model for working with data across various kinds of data sources and formats. You use LINQ to query data with C# irrespective of the data source.

In a more technical sense, LINQ is a set of methods, provided as extension methods in .NET, that provide a universal approach to querying data of any type. This data can be in-memory objects (like lists or arrays), XML, databases, or any other format for which a LINQ provider is available. These methods take lambda expressions as arguments, which behave like in-line functions that work on the dataset being queried.

There are several benefits to using LINQ in your C# applications:

1. `Simplicity`: LINQ simplifies querying and manipulating data by providing a consistent query syntax across different data sources, making code cleaner and more maintainable.
2. `Type Safety`: LINQ is strongly typed, meaning compile-time type checking is performed on query expressions.
3. `Expressiveness`: LINQ offers a rich set of query operators that allow you to express complex data operations concisely and declaratively, making queries easy to read.
4. `Integration`: LINQ is seamlessly integrated into the C# language and can be used with various data sources, including in-memory collections, databases (via LINQ to SQL or Entity Framework), XML, and web services.

## LINQ Query Syntax

LINQ provides two main syntaxes for writing queries: query syntax and method syntax. The query syntax is often preferred for its readability and resemblance to SQL, while the method syntax offers more flexibility and composability. Let us explore both syntaxes with examples.

Consider a simple example where we have a list of integers and want to retrieve all the even numbers from the list:

```csharp
// This creates a new list of integers named 'numbers' and populates it with the numbers from 1 to 10.
List<int> numbers = new List<int> { 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 };

// This is a LINQ query that will create a new collection called 'evenNumbers'.
// The 'from num in numbers' part signifies that we're querying over the 'numbers' list and will refer to each element as 'num'.
// The 'where num % 2 == 0' part is a condition that each number in the list must satisfy to be included in the new collection - in this case, the number must be even.
// The '%' operator is the modulus operator, which gives the remainder of integer division. So 'num % 2' gives the remainder when 'num' is divided by 2. If this remainder is 0, then the number is even.
// The 'select num' part signifies that if a number satisfies the condition, then it should be included in the 'evenNumbers' collection.
var evenNumbers = from num in numbers
                  where num % 2 == 0
                  select num;

```

In the above code, we use the `from` clause to define a range variable `num` representing each element in the `numbers` list. The `where` clause filters the numbers based on the condition `num % 2 == 0`, selecting only the even numbers. Finally, the `select` clause projects the selected numbers into the `evenNumbers` variable.

The equivalent code using method syntax would look like this:

```csharp
// This creates a new list of integers named 'numbers' and populates it with the numbers from 1 to 10.
List<int> numbers = new List<int> { 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 };

// This is a LINQ query using method syntax. It creates a new collection called 'evenNumbers' from the 'numbers' list.
// The 'Where' method filters the 'numbers' list based on the provided lambda expression 'num => num % 2 == 0'.
// The lambda expression takes each number 'num' in the 'numbers' list and returns true if 'num' is even (i.e., if the remainder when 'num' is divided by 2 is 0), and false otherwise.
// The 'Where' method then includes in 'evenNumbers' only those numbers for which the lambda expression returned true.
// As a result, 'evenNumbers' will include all even numbers from the original 'numbers' list. The output will be: 2, 4, 6, 8, 10.
var evenNumbers = numbers.Where(num => num % 2 == 0); // Output: 2, 4, 6, 8, 10

```

In the method syntax, we use the `Where` operator to filter the numbers based on the provided condition.

## LINQ Operators

LINQ provides a series of `query operators`, each performing a specific operation on a data source. The power of LINQ comes from these operators, which can be combined in various ways to compose complex queries.

### Where

The `Where` operator filters a sequence based on a specified condition.

```csharp
List<int> numbers = new List<int> { 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 };

// This line filters the 'numbers' list using a LINQ query. The query uses a lambda expression to select only the numbers that are even (i.e., numbers where the remainder of the division by 2 is equal to zero).
// The result is a new collection 'evenNumbers' containing all the even numbers from the original 'numbers' list.
var evenNumbers = numbers.Where(num => num % 2 == 0);

// Output: 2, 4, 6, 8, 10
foreach (var num in evenNumbers)
{
    Console.WriteLine(num);
}

```

### Select

The `Select` operator projects each element of a sequence into a new form.

```csharp
List<string> names = new List<string> { "John", "Alice", "Michael" };

// This line uses a LINQ query with the Select method to create a new collection 'upperCaseNames'.
// The query takes the 'names' collection and applies the 'ToUpper' method to each element.
// The ToUpper method is a built-in C# method that converts all the characters in a string to uppercase.
// The result is a new collection where all the names from the original 'names' collection are transformed into uppercase.
var upperCaseNames = names.Select(name => name.ToUpper());

// Output: JOHN, ALICE, MICHAEL
foreach (var name in upperCaseNames)
{
    Console.WriteLine(name);
}

```

### OrderBy/OrderByDescending

The `OrderBy` and `OrderByDescending` operators sort the elements of a sequence in ascending or descending order.

```csharp
List<int> numbers = new List<int> { 5, 2, 8, 1, 9 };

// The OrderBy method is a LINQ operation that sorts the elements of a collection in ascending order according to a key. In this case, the key is the numbers themselves.
var sortedNumbersAsc = numbers.OrderBy(num => num);

// Output: 1, 2, 5, 8, 9
foreach (var num in sortedNumbersAsc)
{
    Console.WriteLine(num);
}

// The OrderByDescending method is similar to OrderBy, but sorts the elements in descending order. Like in the previous example, the key is the numbers themselves.
var sortedNumbersDesc = numbers.OrderByDescending(num => num);

// Output: 9, 8, 5, 2, 1
foreach (var num in sortedNumbersDesc)
{
    Console.WriteLine(num);
}

```

### GroupBy

The `GroupBy` operator groups elements of a sequence based on a specified key.

```csharp
// Define a class 'Student' with two properties: 'Name' and 'Grade'. The 'get' and 'set' are accessors which control the read-write status of these properties.

class Student
{
    public string Name { get; set; }
    public string Grade { get; set; }
}

// Create a list of students, where each student is an instance of the 'Student' class. Each student has a 'Name' and a 'Grade'.
List<Student> students = new List<Student>
{
    new Student { Name = "John", Grade = "A" },
    new Student { Name = "Alice", Grade = "B" },
    new Student { Name = "Michael", Grade = "A" },
    new Student { Name = "Emily", Grade = "B" }
};

// Using the LINQ GroupBy method, we group the students by their grades. This method returns a collection of `IGrouping<TKey,TElement>` objects, where each `IGrouping` object contains a collection of objects that have the same key.
var studentsByGrade = students.GroupBy(student => student.Grade);

foreach (var group in studentsByGrade)
{
    Console.WriteLine("Students in Grade " + group.Key + ":");
    foreach (var student in group)
    {
        Console.WriteLine(student.Name);
    }
}
// Students in Grade A:
// John
// Michael
// Students in Grade B:
// Alice
// Emily

```

When the `GroupBy` method is called, it groups the elements of the original collection ( `students` in this case) based on a specified key. In this case, the key is `student.Grade`, which means the students are grouped by their grades. Each `group` is an `IGrouping<TKey, TElement>` object (where `TKey` is the type of the key and `TElement` is the type of the elements in the group). In this specific case, `TKey` is a `string` (the grade) and `TElement` is a `Student`.

So, in the foreach loop, `group` represents each of these `IGrouping<string, Student>` objects. The `Key` property of each `group` holds the grade (A or B in this example), and iterating over `group` gives you each student in that grade.

### Join

The `Join` operator combines two sequences based on a common key.

```csharp
// This is the Student class with properties for Id, Name, and CourseId. The 'get' and 'set' are accessors which control the read-write status of these properties.
class Student
{
    public int Id { get; set; }
    public string Name { get; set; }
    public int CourseId { get; set; }
}

// This is the Course class with properties for Id and Title. The 'get' and 'set' are accessors which control the read-write status of these properties.
class Course
{
    public int Id { get; set; }
    public string Title { get; set; }
}

// Here we create a list of students, where each student is an instance of the 'Student' class. Each student has an 'Id', 'Name', and a 'CourseId'.
List<Student> students = new List<Student>
{
    new Student { Id = 1, Name = "John", CourseId = 101 },
    new Student { Id = 2, Name = "Alice", CourseId = 102 },
    new Student { Id = 3, Name = "Michael", CourseId = 101 },
    new Student { Id = 4, Name = "Emily", CourseId = 103 }
};

// We create a list of courses, where each course is an instance of the 'Course' class. Each course has an 'Id' and a 'Title'.
List<Course> courses = new List<Course>
{
    new Course { Id = 101, Title = "Mathematics" },
    new Course { Id = 102, Title = "Science" },
    new Course { Id = 103, Title = "History" }
};

// Here we perform a join operation between the 'students' and 'courses' lists using LINQ's Join method.
// We match each student with their corresponding course based on the CourseId from the student and the Id from the course.
// The result is a new anonymous object that includes each student's name and the title of their course.
var studentCourseInfo = students.Join(courses,
                                      student => student.CourseId,
                                      course => course.Id,
                                      (student, course) => new
                                      {
                                          student.Name,
                                          course.Title
                                      });

foreach (var info in studentCourseInfo)
{
    Console.WriteLine(info.Name + " - " + info.Title);
}

// John - Mathematics
// Alice - Science
// Michael - Mathematics
// Emily - History

```

### Aggregate

The `Aggregate` operator applies an accumulator function over a sequence.

```csharp
List<int> numbers = new List<int> { 1, 2, 3, 4, 5 };

// This line uses the LINQ Aggregate method to generate a single value from the 'numbers' collection.
// The Aggregate method applies a specified function to the first two elements of the collection, then to the result and the next element, and so on.
// In this case, the function is a lambda expression '(acc, num) => acc + num', where 'acc' represents the accumulated value so far and 'num' represents the current element.
// So essentially, this code sums up all the numbers in the 'numbers' collection. The resulting sum is then stored in the 'sum' variable.
var sum = numbers.Aggregate((acc, num) => acc + num);

// Output: 15
Console.WriteLine(sum);

```

### Count/Sum/Average/Min/Max

These methods compute a sequence's `count`, `sum`, `average`, `minimum`, or `maximum` value.

```csharp
List<int> numbers = new List<int> { 5, 2, 8, 1, 9 };

// The Count method is a LINQ extension method that returns the number of elements in the 'numbers' collection. The result is stored in the 'count' variable.
int count = numbers.Count();
// The Sum method calculates the sum of all elements in the 'numbers' collection. The resulting sum is stored in the 'sum' variable.
int sum = numbers.Sum();
// The Average method calculates the average value of all elements in the 'numbers' collection. Since an average can be a fractional number, it's stored in a variable of type double.
double average = numbers.Average();
// The Min method finds the smallest number in the 'numbers' collection. The minimum value found is stored in the 'min' variable.
int min = numbers.Min();
// The Max method finds the largest number in the 'numbers' collection. The maximum value found is stored in the 'max' variable.
int max = numbers.Max();

Console.WriteLine("Count: " + count);        // Output: Count: 5
Console.WriteLine("Sum: " + sum);            // Output: Sum: 25
Console.WriteLine("Average: " + average);    // Output: Average: 5
Console.WriteLine("Min: " + min);            // Output: Min: 1
Console.WriteLine("Max: " + max);            // Output: Max: 9

```

This code has a `List<int>` called numbers with five elements. We use various LINQ extension methods ( `Count()`, `Sum()`, `Average()`, `Min()`, `Max()`) to perform calculations on the list. The expected output comments indicate the results when printing the count, sum, average, minimum, and maximum values to the console.


# Methods and Exception Handling

* * *

## Functions

Functions, known as methods in C#, are a significant feature of programming, providing a means to create reusable code. They allow programmers to build modular programs, improving efficiency, readability, and maintainability.

### Creating a method

In C#, a method declaration specifies the method’s name, return type, and parameters within the class definition. Here's an example of a method declaration for a simple method that multiplies two numbers:

```csharp
public int Multiply(int a, int b);

```

The method is declared `public`, which means it can be accessed from other classes. `int` signifies the return type, indicating that the method will return an integer value. `Multiply` is the method's name, and within the parentheses `(int a, int b)`, we define the parameters the method will take.

The definition of a method involves providing the body of the method or what the method does. The code block inside the curly brackets `{}` forms the method’s body. Let's define our `Multiply` method:

```csharp
public int Multiply(int a, int b)
{
    return a * b;
}

```

The `return` statement specifies the output of the method . In this case, it returns the product of `a` and `b`.

In C#, the terms "declaration" and "definition" of a method aren't typically differentiated, as they are in some languages such as C or C++. This is because C# does not permit separate declaration and definition of methods - when you declare a method, you must also provide its implementation, thus effectively defining it.

### Method Scope

Scope pertains to the visibility or accessibility of variables within the program. In C#, variables declared inside a method, known as local variables, are not accessible outside that method. For instance:

```csharp
public int Multiply(int a, int b)
{
    int result = a * b;
    return result;
}

public void DisplayResult()
{
    Console.WriteLine(result); // This will lead to an error
}

```

In the `DisplayResult()` method, accessing the `result` variable local to the Multiply method would result in a compile-time error. This is because the `result` is out of scope in `DisplayResult()`.

However, if a variable is declared in a class but outside any method, it is a global variable and can be accessed from any method within that class.

### Static vs Non-Static Methods

The `static` keyword is used to declare members that `belong to the type` rather than `any instance of the type`. This means that static members are shared across all instances of a type and can be accessed directly using the type name, without creating an instance of the class.

Methods can be declared as `static` or `non-static`, also known as `instance` methods.

Details about `classes` and `instances` will be explored in the `Object-oriented Programming` section, but for now, just note the following.

A `static` method belongs to the class itself rather than any specific class instance. It is declared with the keyword `static`.

```csharp
public class MyClass
{
    // Static method
    public static void MyStaticMethod()
    {
        Console.WriteLine("This is a static method.");
    }
}

public class Program
{
    public static void Main(string[] args)
    {
        // Call the static method
        MyClass.MyStaticMethod();  // Outputs: This is a static method.
    }
}

```

To call a static method, you don't need to create an instance of the class. Instead, you use the class name itself.

```csharp
MyClass.MyStaticMethod();

```

Since static methods are tied to the class itself, they can only access the class's other static members (methods, properties, etc.). They cannot access non-static members as those belong to specific instances of the class.

A `non-static` (or `instance`) method belongs to a particular class instance. It is declared without using the `static` keyword.

```csharp
public class MyClass
{
    // Non-static (instance) method
    public void MyInstanceMethod()
    {
        Console.WriteLine("This is an instance method.");
    }
}

public class Program
{
    public static void Main(string[] args)
    {
        // Create an instance of MyClass
        MyClass myObject = new MyClass();

        // Call the instance method
        myObject.MyInstanceMethod();  // Outputs: This is an instance method.
    }
}

```

To call a non-static method, you must create an instance of the class.

```csharp
MyClass myObject = new MyClass();
myObject.MyInstanceMethod();

```

Instance methods can access the class's `static` and `non-static` members since they belong to a specific class instance.

Static members can also include `fields`, `properties`, `events`, `operators`, and `constructors`.

## Exceptions

Exception handling in C# is a robust mechanism used to handle runtime errors so that the normal flow of the application can be maintained. C# provides a structured solution to error handling through try-and-catch blocks. Using these blocks, we can isolate code that may throw an exception and enable the program to respond rather than letting the program crash.

### try catch finally

A `try` block is used to encapsulate a region of code. If any statement within the try block throws an exception, that exception will be handled by the associated catch block.

```csharp
try
{
    // Code that could potentially throw an exception.
}

```

The `catch` block is used to catch and handle an exception. It follows a try block or another catch block. Each try block can have multiple catch blocks associated with it, each designed to handle specific or multiple exceptions. A `catch` block without a specified type will catch all exceptions.

```csharp
catch (Exception ex)
{
    // Handle the exception
}

```

A `finally` block lets you execute code after a try block has been completed, regardless of whether an exception has been thrown. It is optional and cleans up resources inside the try block (like database connections, files, or network resources).

```csharp
finally
{
    // Code to be executed after the try block has completed,
    // regardless of whether an exception was thrown.
}

```

Here's an example of try, catch, and finally all used together:

```csharp
try
{
    // Code that could potentially throw an exception.
    int divisor = 0;
    int result = 10 / divisor;
}
catch (DivideByZeroException ex)
{
    // Handle the DivideByZeroException.
    Console.WriteLine("Cannot divide by zero");
}
finally
{
    // Code to be executed after the try block has completed,
    // regardless of whether an exception was thrown.
    Console.WriteLine("This code is always executed.");
}

```

When dealing with `catch blocks`, remember that they can handle multiple exception exceptions. The order in which you specify different catch blocks matters; they're examined top to bottom, so the first one that matches the exception type will be executed. If you have a catch block that handles all exceptions at the top, it will catch all exceptions, and none of the catch blocks below it will execute. This is why the catch block for the most general exception type, `Exception`, is usually last.

```csharp
try
{
    // Code that could throw an exception
    int[] arr = new int[5];
    arr[10] = 30; // This line throws an IndexOutOfRangeException.
}
catch (IndexOutOfRangeException ex)
{
    // Handle specific exception first
    Console.WriteLine("An IndexOutOfRangeException has been caught: " + ex.Message);
}
catch (Exception ex)
{
    // General exception catch block
    Console.WriteLine("An exception has been caught: " + ex.Message);
}

```

The `finally` block is executed regardless of whether an exception is thrown. If you have any code that must execute, whether an exception is thrown or not, it should be placed in a finally block. For example, if you open a file in a try block, you should close it in a finally block, whether or not an exception is thrown when working with the file.

```csharp
StreamReader reader = null;
try
{
    reader = new StreamReader("file.txt");
    // Code to read the file.
}
catch (FileNotFoundException ex)
{
    Console.WriteLine(ex.Message);
}
finally
{
    // Whether an exception is thrown or not, close the file.
    if (reader != null)
        reader.Close();
}

```

### throw

The `throw` keyword can be used to raise exceptions. You can throw a pre-existing exception, or you can instantiate a new exception and throw it.

```csharp
try
{
    // Throw a new exception.
    throw new Exception("A problem has occurred.");
}
catch (Exception ex)
{
    // Handle the exception.
    Console.WriteLine(ex.Message);
}

```


# Lambda Expressions

* * *

A lambda expression is a method without a name that calculates and returns a single value. They are simple methods to represent `anonymous methods` (methods without a name) or `functions` inline.

A lambda expression consists of three main parts: a `parameter list`, the `lambda operator` ( `=>`), and an `expression or statement`. The general syntax for a lambda expression looks something like this:

```csharp
(parameters) => expression or statement block

```

- The `parameters` represent the input values to the lambda expression. They can be zero or more, separated by commas. If there is only one parameter, parentheses are optional. For multiple parameters, parentheses are required.
- The `lambda Operator (=>)` separates the parameter list from the body of the expression. It denotes a relationship between the parameters and the code to execute.
- The `expression or statement block` represents the code that is executed when the lambda expression is invoked. For a single expression, the result is implicitly returned. A statement block is enclosed in curly braces `{}` for multiple statements.

Consider the example given in the `LINQ` section.

```csharp
var evenNumbers = numbers.Where(num => num % 2 == 0); // Output: 2, 4, 6, 8, 10

```

The lambda expression `num => num % 2 == 0` specifies the condition for the `Where` method to filter the numbers. Here, `num` is the input parameter, and the condition to the right of the lambda operator is the statement block. This condition is applied to each element of the numbers list.

In plain English, this lambda expression reads, "For each number (num) in numbers, keep it if the remainder when num is divided by 2 equals 0." The % operator is the modulus operator, which gives the remainder of a division operation. Therefore, `num % 2 == 0` checks if a number is evenly divisible by 2, i.e., it's an even number.

## Simple Lambda Expression

Consider the following method.

```csharp
void Greet()
{
    Console.WriteLine("Hello, world!");
}

// Invoke the method
Greet(); // Output: Hello, world!

```

In this example, we merely define a method that prints a message to the console when invoked. However, we can further simplify this code using a lambda function, which essentially condenses it into a single line.

```csharp
// Lambda expression without parameters
var greet = () => Console.WriteLine("Hello, world!");
greet(); // Output: Hello, world!

```

In this instance, we've defined a lambda expression without any parameters. The lambda expression assigns a function to the variable `greet`, which prints "Hello, world!" to the console upon invocation.

While both achieve the same outcome, the lambda expression is far more succinct and can be employed as an inline function where required, contrasted with the method definition that necessitates a separate declaration.

## Lambda Expression with Parameters

A `Lambda Expression with Parameters` is a type of lambda expression in C# that takes one or more input parameters. This type of lambda expression is typically used when you want to perform an operation or evaluate a condition using the input parameters.

```csharp
// Regular method
int Add(int a, int b)
{
    return a + b;
}

// Lambda expression with parameters
var add = (int a, int b) => a + b;
int result = add(5, 3);
Console.WriteLine(result); // Output: 8

```

Here, we define a lambda expression with two parameters `a` and `b`, which adds the values of `a` and `b`. The lambda expression is assigned to the variable `add`, and we invoke it with arguments `5` and `3`, resulting in the sum `8` being assigned to the variable `result`.

## Lambda Expression with Statement Block

A `Lambda Expression with a Statement Block`, often called a `Statement Lambda`, is a type of lambda expression in C# that contains a block of code instead of a single expression on the right side of the lambda operator ( `=>`).

```csharp
// Regular method
bool IsEven(int number)
{
    if (number % 2 == 0)
        return true;
    else
        return false;
}

// Lambda expression with statement block
var isEven = (int number) =>
{
    if (number % 2 == 0)
        return true;
    else
        return false;
};

bool even = isEven(6);
Console.WriteLine(even); // Output: True

```

In this example, we define a lambda expression with a parameter `number` and a statement block enclosed in curly braces. The lambda expression checks if the `number` is even and returns `true` or `false` accordingly. We assign the result of invoking the lambda expression with `6` to the variable `even`, which evaluates to `true`.


# Libraries

* * *

C# includes many predefined functions and libraries that developers can use to accomplish various tasks more easily and efficiently. The .NET Framework provides these libraries and includes functionalities for things like file I/O, database access, networking, and much more.

A library in C# is typically provided as a `.dll` (Dynamic Link Library) file. To use the library's functions and classes, you must first reference it in your project. This will be done automatically if the library is installed via a package manager like nuget, or if you use a library from within the .NET ecosystem.

The `using` directive then tells the compiler to use a specific namespace in the library. A `namespace` groups related class, structures, and other types under a single name. For instance, the `System` namespace includes fundamental classes and base types that are used in C# programming.

For example, to use the `File` class from the `System.IO` namespace for handling files, you would first need to add `using System.IO;` at the top of your code.

```csharp
using System.IO;

class Program
{
    static void Main(string[] args)
    {
        // Check if a file exists
        if (File.Exists("test.txt"))
        {
            // Read the content of the file
            string content = File.ReadAllText("test.txt");
            Console.WriteLine(content);
        }
        else
        {
            Console.WriteLine("The file does not exist.");
        }
    }
}

```

In this example, `File.Exists` is a predefined function from the `System.IO` namespace that checks if a file exists at the provided path and `File.ReadAllText` is another predefined function that reads the entire content of the file as a string. Because `System` is a core library, the compiler will automatically include it.

Similarly, you can use predefined functions from other namespaces and libraries—for instance, the `System.Math` namespace contains mathematical functions such as `Math.Sqrt` for computing the square root of a number, `Math.Pow` for raising a number to a specified power, and `Math.Round` for rounding a number to the nearest integer.

```csharp
using System;

class Program
{
    static void Main(string[] args)
    {
        double num = 9.0;
        double squareRoot = Math.Sqrt(num);
        Console.WriteLine($"The square root of {num} is {squareRoot}");

        double baseNum = 2.0;
        double exponent = 3.0;
        double power = Math.Pow(baseNum, exponent);
        Console.WriteLine($"{baseNum} raised to the power of {exponent} is {power}");

        double toBeRounded = 9.5;
        double rounded = Math.Round(toBeRounded);
        Console.WriteLine($"{toBeRounded} rounded to the nearest integer is {rounded}");
    }
}

```

As you can see, leveraging the predefined functions and libraries provided by the .NET Framework can achieve complex functionality with less code.

## NuGet

In addition to the standard libraries, C# offers extensive support for using third-party libraries and packages. These can be added to your project through various means, including the [NuGet package manager](https://www.nuget.org/). `NuGet` is a free and open-source package manager designed for the Microsoft development platform, and it hosts thousands of libraries.

Adding a `NuGet` package to your project can be as easy as right-clicking on your project in the Solution Explorer in Visual Studio, selecting " `Manage NuGet Packages...`" and then searching for and installing the required package. If using a code editor, we use the `dotnet package add` command, but [Microsoft provides great documentation for using nuget from the CLI](https://learn.microsoft.com/en-za/nuget/consume-packages/install-use-packages-dotnet-cli).

Once a package is installed, you can utilise its functionality in your code by adding the appropriate `using` directive at the top of your file. The `Newtonsoft.Json` package, for instance, provides powerful tools for working with JSON data.

```csharp
using Newtonsoft.Json;
using System;
using System.Collections.Generic;

class Program
{
    static void Main(string[] args)
    {
        string json = "[{'Name':'John', 'Age':30}, {'Name':'Jane', 'Age':28}]";

        List<Person> people = JsonConvert.DeserializeObject<List<Person>>(json);

        foreach (var person in people)
        {
            Console.WriteLine($"Name: {person.Name}, Age: {person.Age}");
        }
    }
}

public class Person
{
    public string Name { get; set; }
    public int Age { get; set; }
}

```

In this example, the `JsonConvert.DeserializeObject<T>` method is used to parse the JSON string into a list of `Person` objects. This predefined function, part of the `Newtonsoft.Json` library, dramatically simplifies the task of JSON parsing.

## Manual Referencing

It is also possible to manually link a library to the project. If you use an IDE such as Visual Studio, or Jetbrains Rider, it's as simple as right-clicking on the `Project Dependencies` section under the solution explorer and selecting the `Add Project Reference...` option, and then finding the library you want to link.

Alternatively, if you are using a Code editor, such as VSCode, you will need to manually edit the project file to include the references, such as the example below, which is going to reference every `.dll` file in the libs subfolder:

```xml
<Project Sdk="Microsoft.NET.Sdk">

  <PropertyGroup>
    <TargetFramework>net7.0</TargetFramework>
    <ImplicitUsings>enable</ImplicitUsings>
    <Nullable>enable</Nullable>
    <AllowUnsafeBlocks>true</AllowUnsafeBlocks>
  </PropertyGroup>
  <ItemGroup>
    <!-- references look like this -->
    <Reference Include="libs\*.dll" />
  </ItemGroup>

</Project>

```

It's also possible to hardcode paths and establish multiple `Reference` definitions for each individualreference specifically.

To identify the `namespaces`, `types`, `classes`, and `methods` provided by the library, it is generally considered best practice to consult the provided documentation. Both Visual Studio and Visual Studio Code will provide code auto-complete functionality for the functionality from imported libraries through their IntelliSense auto-complete tool.

While the .NET Framework and third-party libraries offer a wide array of predefined functions, it's essential to understand their usage and potential impact on your application. Some libraries may have licensing restrictions, or they may not be maintained actively. Always research before including a third-party library in your project.

Enable step-by-step solutions for all questions
![sparkles-icon-decoration](https://academy.hackthebox.com/images/sparkles-solid.svg)

#### Questions

Answer the question(s) below
to complete this Section and earn cubes!

Cheat Sheet

\+ 1  Import the Library-Question library appropriate for your OS and dotNet version, using the HTBLibrary namespace. What is the output of the \`Flag.GetFlag()\` method from the library?


Submit


[Library-Question.zip](/storage/modules/228/Library-Question.zip)


# Object-Oriented Programming

* * *

Object-Oriented Programming (OOP) is a programming paradigm that relies on the concept of "objects". Objects are instances of classes, which can contain data in the form of fields, often known as attributes, and code, in the form of methods. In OOP, computer programs are designed by making them out of objects that interact with one another.

There are four main principles of Object-Oriented Programming:

1. `Encapsulation` is the practice of keeping fields within a class private and providing access to them via public methods. It's a protective barrier that keeps the data and implementation code bundled together within an object.
2. `Inheritance` is a process by which one class can acquire the properties (methods and fields) of another. With the use of inheritance, information is made manageable in a hierarchical order.
3. `Polymorphism` enables methods to be used as if they were the methods of a class's parent. It's the characteristic of an operation to behave differently based on the types of objects or arguments involved.
4. `Abstraction` represents essential features without including background details or explanations. It provides a simple interface and reduces complexity by hiding unnecessary details.

## Classes & Structs

In C#, a `class` is a blueprint for creating objects, and an object is an instance of a class. Class definitions start with the keyword `class` followed by the name of the class and typically encapsulate data and methods that operate on that data.

Classes are made up of two fundamental elements: `Properties` and `Methods`.

- `Properties` represent data about the class. They are often referred to as attributes or characteristics. For example, in a `Car` class, properties might include `Color`, `Model`, and `Year`.
- `Methods` represent actions or behaviour associated with the class. They are functions defined within a class. For instance, a `Car` class may have methods like `Drive()`, `Park()`, and `Brake()`.

```csharp
class Car
{
    // Properties
    public string Color;
    public int Year;

    // Method
    public void Drive()
    {
        Console.WriteLine($"The {Color} car from {Year} is driving.");
    }
}

```

In the above example, `Car` is a class that contains two properties ( `Color` and `Year`) and one method ( `Drive`).

To create an object in C#, you use the `new` keyword followed by the class name. This process is often called `instantiation` because you create an "instance" of a class.

```csharp
Car myCar = new Car();

```

In this line, `myCar` is an object of the `Car` class. You can now use the dot operator `.` to access its properties and methods:

```csharp
myCar.Color = "Red";
myCar.Year = 2020;
myCar.Drive();
// output: The Red car from 2020 is driving.

```

Remember that each object has its own copy of properties. Thus, if you create another `Car` object, it will have its own `Color` and `Year`:

```csharp
Car anotherCar = new Car();
anotherCar.Color = "Blue";
anotherCar.Year = 2021;
//output: The Blue car from 2021 is driving.

```

So even though `myCar` and `anotherCar` are both instances of the `Car` class, they have different property values. This allows objects to have unique states while sharing common behaviour from their respective classes.

Classes can also have a `constructor`, which is a special method in a class or struct that is automatically called when an object of that class or struct is created. The primary purpose of a constructor is to initialise the object and its data members.

The constructor has the same name as the class or struct, and it doesn't have any return type, not even void. It can take parameters if needed.

```csharp
class Car
{
    // Properties
    public string Color;
    public int Year;

    // Constructor
    public Car(string c, int y)
    {
        Color = c;
        Year = y;
    }

    // Method
    public void Drive()
    {
        Console.WriteLine($"The {Color} car from {Year} is driving.");
    }
}

```

You can then pass the parameters when the object is instantiated to set the variables.

```csharp
Car myNewCar = new Car("Pink", 2022);
myNewCar.Drive();
// output: The Pink car from 2022 is driving.

```

### Accessors

An `accessor` is a class member function that provides access to the value of private or protected data members. There are two types of accessors - `get` and `set`.

The `get` accessor is used to return the property value. It provides read-only access to the attribute it is assigned to. If only a `get` accessor is specified, the property becomes read-only.

```csharp
class Circle
{
    private double radius;

    public double Radius
    {
        get
        {
            return radius;
        }
    }
}

```

In this example, the `Radius` property has only a `get` accessor, making it read-only. Trying to set its value will result in a compile-time error.

The `set` accessor is used to set the property `value`. It provides write-only access to the attribute it is assigned to. If only a `set` accessor is specified, the property becomes write-only.

```csharp
class Circle
{
    private double radius;

    public double Radius
    {
        set
        {
            if (value > 0)
                radius = value;
            else
                Console.WriteLine("Radius cannot be negative or zero");
        }
    }
}

```

In this example, the `Radius` property has only a `set` accessor. Its value can be set but not directly retrieved. The `value` keyword in C# is a special keyword that is used in the `set` accessor of a property or indexer. It represents the new value the code attempts to assign to the property.

Most commonly, you'll see both `get` and `set` accessors used together. This allows for both reading and writing the property value.

```csharp
class Circle
{
    private double radius;

    public double Radius
    {
        get
        {
            return radius;
        }
        set
        {
            if (value > 0)
                radius = value;
            else
                Console.WriteLine("Radius cannot be negative or zero");
        }
    }
}

```

### Automatic Properties

In C#, an automatic property, also known as auto-implemented property, allows you to define a class property in a concise way without explicitly declaring a backing field. A backing field is a private variable used to store a property’s data.

For example, consider a `full property` with a declared backing field:

```csharp
class Circle
{
    private double radius;

    public double Radius
    {
        get
        {
            return radius;
        }
        set
        {
            radius = value;
        }
    }
}

```

Whereas an automatic property will automatically declare the backing field:

```csharp
class Circle
{
    public double Radius { get; set; }
}

```

In this example, `Radius` is an automatic property. The `{ get; set; }` syntax tells C# to generate a hidden backing field behind the scenes automatically. This field stores the actual data, and the `get` and `set` accessors are used to read from and write to this field.

Functionally both properties are identical.

```csharp
Circle c = new Circle();
c.Radius = 12345.54321;

Console.WriteLine(c.Radius);  // Outputs: 12345.54321

```

Automatic properties provide a shorter and more readable way to create properties, helping keep your code clean and efficient.

### Structs

A `struct`, short for structure, is a value type in C#. This means when a `struct` is created, the variable to which the struct is assigned holds the struct's actual data. This contrasts with reference types, where the variable references the object's data, not the actual data itself.

Structs are useful for small data structures that have value semantics. They can contain fields, methods, and constructors just like classes, but there are some differences:

- Structs do not support inheritance, while classes do. However, both structs and classes can implement interfaces.
- Structs are instantiated without using the `new` keyword, and their constructors are called automatically.
- A struct cannot be `null`, as it's a value type. A class can be `null` because it's a reference type.

```csharp
public struct Point
{
    public int X { get; set; }
    public int Y { get; set; }

    public Point(int x, int y)
    {
        X = x;
        Y = y;
    }
}

```

In this example, `Point` is a struct that represents a point in two-dimensional space. It includes two properties ( `X` and `Y`) and a constructor that initialises those properties.

## Encapsulation

Encapsulation is one of the four fundamental principles of Object-Oriented Programming (OOP). It is often described as the bundling of data and the methods that operate on that data into a single unit known as a class. It serves as a protective shield that prevents the data from being accessed directly by outside code, hence enforcing data integrity and ensuring security.

In C#, data encapsulation is achieved through access modifiers, which control the visibility and accessibility of classes, methods, and other members. The key access modifiers are `public`, `private`, `protected`, and `internal`.

- A `public` member is accessible from any code in the program.
- A `private` member is only accessible within its own class. This is the most restrictive level of access.
- A `protected` member is accessible within its own class and by derived class instances.
- An `internal` member is accessible only within files in the same assembly.

The convention in C# is to make data members `private` to hide them from other classes (this is known as data hiding). Then, `public` methods known as getters and setters (or, more commonly, properties) are provided to get and set the values of the private fields. These methods serve as the interface to the outside world and protect the data from incorrect or inappropriate manipulation.

```csharp
public class Employee
{
    // Private member data (fields)
    private string name;
    private int age;

    // Public getter and setter methods (properties)
    public string Name
    {
        get { return name; }
        set { name = value; }
    }

    public int Age
    {
        get { return age; }
        set
        {
            if(value > 0)
                age = value;
            else
                Console.WriteLine("Invalid age value");
        }
    }
}

```

In this example, the `Employee` class encapsulates the `name` and `age` fields. These fields are `private`, so they cannot be accessed directly from outside the `Employee` class. Instead, access is provided through the `public` properties `Name` and `Age`, which serve as the interface to the `Employee` class. Notice that the `Age` setter includes validation logic to ensure an invalid age cannot be set. This is an excellent example of encapsulation protecting the data in an object. The data (in this case, the `age`) is safeguarded and encapsulated within the `Employee` class.

## Inheritance

Inheritance is a fundamental principle of Object-Oriented Programming (OOP) that allows for the creation of hierarchical classifications of objects. It offers a mechanism where a new class can inherit members (fields, methods, etc.) of an existing class, thereby promoting code reusability and logical classification.

There are two types of inheritance: single inheritance and multilevel inheritance.

### Single Inheritance

In single inheritance, a class (aka a derived or child class) inherits from a single-parent class (also known as a base or superclass). This allows the derived class to reuse (or inherit) the fields and methods of the base class, as well as to introduce new ones.

Consider an example where we have a base class, `Vehicle`, and a derived class, `Car`.

```csharp
public class Vehicle {
    public string color;

    public void Start() {
        Console.WriteLine("Vehicle started");
    }
}

public class Car : Vehicle {
    public string model;

    public void Drive() {
        Console.WriteLine("Driving car");
    }
}

```

`Car` is a derived class that inherits from the `Vehicle` base class. It inherits the `color` field and the `Start()` method from `Vehicle` and also defines an additional field `model` and a method `Drive()`.

### Multilevel Inheritance

Multilevel inheritance is a scenario where a derived class inherits from another. This creates a "chain" of inheritance where a class can inherit members from multiple levels up its inheritance hierarchy.

Let's extend the previous example to include a `SportsCar` class inherited from `Car`.

```csharp
public class SportsCar : Car {
    public int topSpeed;

    public void TurboBoost() {
        Console.WriteLine("Turbo boost activated");
    }
}

```

In this case, `SportsCar` is a derived class that inherits from the `Car` class, which in turn inherits from the `Vehicle` class. This means that `SportsCar` has access to the `color` field and `Start()` method from `Vehicle`, the `model` field and `Drive()` method from `Car`, and also defines its own field `topSpeed` and method `TurboBoost()`.

Remember that C# doesn't support multiple inheritance, meaning a class cannot directly inherit from more than one class at the same level. However, as we've seen here, it supports multiple levels of inheritance and allows a class to implement multiple interfaces.

### base

In C#, the `base` keyword is used to access base class members from within a derived class. This can include methods, properties, and fields of the base class. Furthermore, the `base` keyword is most commonly employed within the derived class's constructor to call the base class’s constructor.

To delve deeper, let's examine the use of the `base` keyword in a few examples. Consider a base-class `Vehicle` and a derived-class `Car`.

```csharp
public class Vehicle
{
    public string Color { get; }

    public Vehicle(string color)
    {
        this.Color = color;
    }

    public void DisplayColor()
    {
        Console.WriteLine($"Color: {this.Color}");
    }
}

public class Car : Vehicle
{
    public string Brand { get; }

    public Car(string color, string brand) : base(color)
    {
        this.Brand = brand;
    }

    public void DisplayCarInformation()
    {
        base.DisplayColor();
        Console.WriteLine($"Brand: {this.Brand}");
    }
}

```

In the derived class `Car`, the `base` keyword is used in two distinct ways:

1. `Constructor`: Within the constructor of `Car`, `base(color)` is used to call the constructor of the base class `Vehicle`. Here, `base` allows `Car` to initialise the `Color` property defined in `Vehicle`.
2. `Methods`: Within the `DisplayCarInformation` method of `Car`, `base.DisplayColor()` is used to call the `DisplayColor` method from the base class `Vehicle`.

The `base` keyword hence provides an effective way to interact with the base class and utilise its members, enabling the principles of reuse and abstraction that are foundational to object-oriented programming. This leads to more manageable, scalable, and organised code.


# Polymorphism and Abstraction

* * *

## Polymorphism

Polymorphism is one of the four fundamental principles of Object-Oriented Programming (OOP), alongside Encapsulation, Inheritance, and Abstraction. The term originates from the Greek words "poly," meaning many, and "morph," meaning forms. Thus, polymorphism is the ability of an entity to take on many forms.

In C#, polymorphism is generally realised through method overloading and overriding.

### Method Overloading

Method overloading, also known as static or compile-time polymorphism, is a technique that allows multiple methods with the same name but different parameters (in terms of number, type, or order) to coexist within a class.

```csharp
public class Mathematics
{
    public int Add(int a, int b)
    {
        return a + b;
    }

    public double Add(double a, double b)
    {
        return a + b;
    }
}

```

In the above class `Mathematics`, the method `Add` is overloaded: one version of the `Add` method accepts two integers, while the other accepts two doubles. The correct version of the method is selected at compile time-based on the arguments supplied.

### Method Overriding

Method overriding, on the other hand, is a form of dynamic or run-time polymorphism. It allows a derived class to provide a different implementation for a method already defined in its base class or one of its base classes. The method in the base class must be marked with the `virtual` keyword, and the method in the derived class must use the `override` keyword.

```csharp
public class Animal
{
    public virtual void MakeSound()
    {
        Console.WriteLine("The animal makes a sound");
    }
}

public class Dog : Animal
{
    public override void MakeSound()
    {
        Console.WriteLine("The dog barks");
    }
}

```

In the above example, the `Dog` class overrides the `MakeSound` method of the `Animal` class. When `MakeSound` is called on an object of type `Dog`, the overridden version in the `Dog` class is executed.

The concepts of overloading and overriding extend to operators and properties, adding flexibility and expressiveness to C# programming.

### Operator Overloading

Just like methods, C# allows operators to be overloaded. This enables custom types to be manipulated using standard operators, enhancing code readability and intuitiveness. For example, for a `Vector` class representing a mathematical vector, you might overload the '+' operator to perform vector addition:

```csharp
public class Vector
{
    public double X { get; set; }
    public double Y { get; set; }

    public Vector(double x, double y)
    {
        X = x;
        Y = y;
    }

    public static Vector operator +(Vector v1, Vector v2)
    {
        return new Vector(v1.X + v2.X, v1.Y + v2.Y);
    }
}

```

In this example, instances of `Vector` can be added using the `+` operator, just like primitive types:

```csharp
Vector v1 = new Vector(1, 2);
Vector v2 = new Vector(3, 4);
Vector sum = v1 + v2;  // { X = 4, Y = 6 }

```

### Property Overriding

In C#, properties, like methods, can be overridden in derived classes. A base class declares a virtual property, and derived classes can override this property to change its behaviour.

```csharp
public class Animal
{
    public virtual string Name { get; set; }

    public Animal(string name)
    {
        Name = name;
    }
}

public class Dog : Animal
{
    public Dog(string name) : base(name) { }

    public override string Name
    {
        get { return base.Name; }
        set { base.Name = value + " the dog"; }
    }
}

```

In this case, a `Dog` object modifies the behaviour of the `Name` property to append " the dog" to any name assigned to it:

```csharp
Dog myDog = new Dog("Rex");
Console.WriteLine(myDog.Name);  // "Rex the dog"

```

These examples underline the power of polymorphism in C# and object-oriented programming. It allows classes to provide tailored implementations of methods, operators, and properties, enabling more natural, expressive, and aligned code with the problem domain.

## Abstraction

In object-oriented programming, abstraction is the concept of simplifying complex reality by modelling classes appropriate to the problem and working at the most appropriate level of inheritance for a given aspect of the problem. It is a mechanism that represents the essential features without including the background details.

Abstraction in C# is achieved by using `abstract` classes and `interfaces`. An `abstract` class is a class that cannot be instantiated and is typically used as a base class for other classes. `Abstract` classes can have `abstract` methods which are declared in the `abstract` class and implemented in the derived classes.

```csharp
public abstract class Animal
{
    public abstract void Speak();
}

public class Dog : Animal
{
    public override void Speak()
    {
        Console.WriteLine("The dog barks");
    }
}

public class Cat : Animal
{
    public override void Speak()
    {
        Console.WriteLine("The cat meows");
    }
}

```

In this example, `Animal` is an abstract class with an abstract method `Speak`. `Dog` and `Cat` classes are derived from `Animal` and provide their own implementation of `Speak`. When `Speak` is called on an object of type `Animal`, the appropriate version of `Speak` is invoked depending on the actual type of the object.

Abstraction using `Interfaces` is another way to achieve abstraction. An `interface` is like an `abstract` class with no implementation. It only declares the methods and properties but doesn't contain any code. A class that implements an interface must provide an implementation for all the interface methods.

```csharp
public interface IAnimal
{
    void Speak();
}

public class Dog : IAnimal
{
    public void Speak()
    {
        Console.WriteLine("The dog barks");
    }
}

public class Cat : IAnimal
{
    public void Speak()
    {
        Console.WriteLine("The cat meows");
    }
}

```

In this example, `IAnimal` is an interface with a method `Speak`. The classes `Dog` and `Cat` both implement `IAnimal` and provide their own implementation of `Speak`.

In both examples, the user does not need to understand how each animal speaks; they only need to know that all animals can speak. This is the essence of abstraction. It allows you to focus on what the object does instead of how it does it.

Abstraction has several benefits in software development:

1. `Complexity Management`: It simplifies the complexity of designing and maintaining large codebases. By creating abstract classes or interfaces, developers can develop methods and variables that apply to a broad range of related classes. It's easier to manage and understand a few abstract concepts than a larger number of detailed ones.

2. `Reusability`: The use of abstraction promotes the reuse of code. Abstract classes and interfaces often create a template for future classes. Implementing these templates ensures consistent method use across classes and can reduce the amount of code that needs to be written.

3. `Security`: Using abstraction, certain details of an object's implementation can be hidden from the user. This can prevent unauthorised or inappropriate use of an object's methods or variables.

4. `Flexibility`: Abstraction provides a level of flexibility in the development process. As long as the interface between objects remains consistent, changes to the internal workings of an object do not affect the rest of the application. This allows for more freedom in future development and refactoring efforts.


In addition to abstract classes and interfaces, encapsulation is another way to achieve abstraction in C#. Encapsulation refers to bundling data and the methods of operating it into a single unit. This is typically accomplished by defining a class. The data is stored in private fields, and accessed through public methods, protecting the data from being altered in unexpected ways.

For example, consider a `BankAccount` class:

```csharp
public class BankAccount
{
    private double balance;

    public void Deposit(double amount)
    {
        if (amount > 0)
        {
            balance += amount;
        }
    }

    public void Withdraw(double amount)
    {
        if (amount > 0 && balance >= amount)
        {
            balance -= amount;
        }
    }

    public double GetBalance()
    {
        return balance;
    }
}

```

In this example, the `balance` field is private, meaning it cannot be accessed directly from outside the class. Instead, it is accessed through the `Deposit`, `Withdraw`, and `GetBalance` methods, which ensure the balance cannot be set to an invalid state. This is an example of encapsulation providing abstraction, as users of the `BankAccount` class do not need to know how the balance is stored or how the methods are implemented; they only need to know what methods are available to use.


# Generics in C\#

* * *

Generics are a feature in C# that let you write type-safe and performant code that works with any data type. Without generics, developers often have to write separate versions of algorithms for different data types or resort to less type-safe options like casting to and from objects.

A type is a description of a set of data that specifies the kind of data that can be stored, the operations that can be performed on that data, and how the data is stored in memory. In C#, types are used extensively to ensure that code behaves as expected, i.e., a `string` can't be directly assigned to an `int` variable.

Generics extend this idea of types to type parameters. A generic type is a class, struct, interface, delegate, or method with a placeholder for one or more types it operates on. The actual types used by a generic type are specified when you create an instance of the type.

### Benefits of Generics

1. `Type safety`: Generics enforce compile-time type checking. They can carry out strongly typed methods, classes, interfaces, and delegates. With generics, you can create type-safe collection classes at compile time.
2. `Performance`: With generics, performance is improved as boxing and unboxing are eliminated. For value types, this can represent a significant performance boost.
3. `Code reusability`: Generics promote reusability. You can create a generic class that can be used with any data type.

## Generic Classes

A generic class declaration looks much like a non-generic class declaration, except that a type parameter list inside angle brackets follows the class name. The type parameters can then be used in the body of the class as placeholders for the types specified when the class is instantiated.

```csharp
public class GenericList<T>
{
    private T[] elements;
    private int count = 0;

    public GenericList(int size)
    {
        elements = new T[size];
    }

    public void Add(T value)
    {
        elements[count] = value;
        count++;
    }

    public T GetElement(int index)
    {
        return elements[index];
    }
}

```

In the above example, `T` is the type parameter. This `GenericList` class can be instantiated with any type.

```csharp
var list1 = new GenericList<int>(10);
var list2 = new GenericList<string>(5);

```

## Generic Methods

Generic methods are methods that are declared with type parameters. Like generic classes, you can create a method that defers the specification of one or more types until the method is called.

```csharp
public class Utilities
{
    public T Max<T>(T a, T b) where T : IComparable
    {
        return a.CompareTo(b) > 0 ? a : b;
    }
}

```

In the `Max` method above, `T` represents any type that implements `IComparable`. This method can now be used with any comparable types, like integers, floats, strings, etc.

```csharp
var utility = new Utilities();
int max = utility.Max<int>(3, 4); // returns 4

```

## Generic Constraints

You may want to restrict the types allowed as type arguments when designing generic classes or methods. For example, you might want to ensure that your generic method only operates on value types or classes, types that implement a particular interface, or types with a default constructor. This is done using generic constraints, which you can specify with the `where` keyword.

```csharp
public class Utilities<T> where T : IComparable, new()
{
    public T Max(T a, T b)
    {
        return a.CompareTo(b) > 0 ? a : b;
    }

    public T Init()
    {
        return new T();
    }
}

```

In the above example, the `Utilities` class has two constraints: `T` must implement `IComparable` and `T` must have a default constructor. Now, `Utilities` can be used with any type that satisfies these constraints.

```csharp
var utility = new Utilities<int>();
int max = utility.Max(3, 4); // returns 4
int zero = utility.Init(); // returns 0

```


# Asynchronous Programming

`Asynchronous programming` is a powerful technique in modern software development that allows programs to `perform non-blocking operations` and efficiently utilise system resources. It enables applications to `handle time-consuming tasks without blocking the main execution thread`, improving responsiveness and scalability.

In traditional `synchronous programming`, when a method is invoked, the `program waits until the method completes` its execution before proceeding to the following line of code. This blocking behaviour can lead to poor performance and unresponsive applications, especially when dealing with I/O-bound or long-running operations. You can see this behaviour in applications when they appear to `freeze randomly` and `become unresponsive` when you try to load a large file, for instance. `Asynchronous programming` addresses this issue by `allowing tasks to execute independently` without blocking the main thread, enabling other `work to be done concurrently`.

To understand this concept better, it's important to distinguish between `concurrent` and `parallel` operations. `Concurrent` operations refer to tasks that `appear to occur simultaneously` but may not necessarily do so. On the other hand, `parallel` operations involve tasks that are `executed at the same time` on different cores or processors. Asynchronous programming primarily deals with `concurrent operations`, enabling multiple tasks to `progress independently of each other`.

Asynchronous methods return a `Task` or `Task<T>` object representing an ongoing operation. The calling code can continue its execution while the asynchronous operation progresses in the background. Once the operation completes, the result can be retrieved or further processed.

There are a few very important things to be aware of when utilising asynchronous programming:

- `Avoid Blocking Calls`: Use asynchronous versions of methods whenever possible to prevent blocking the main thread.
- `Configure async Methods Properly`: Ensure that `async` methods return `Task` or `Task<T>` and use the `await` keyword appropriately to await the completion of asynchronous operations.
- `Handle Exceptions`: Handle exceptions properly in asynchronous code. Use `try-catch` blocks to catch and handle exceptions that may occur during asynchronous operations. Unhandled exceptions can lead to unexpected application behaviour.
- `Use Cancellation Tokens`: Utilize cancellation tokens to allow the cancellation of asynchronous operations gracefully. This can improve the responsiveness and user experience of the application.

## async & await

In C#, asynchronous programming is facilitated by the `async` and `await` keywords.

The `async` keyword is used to specify that a method, lambda expression, or anonymous method is asynchronous. These methods usually return a `Task` or `Task<T>` object, representing ongoing work.

On the other hand, the `await` keyword is used in an `async` method to suspend the execution of the method until a particular task completes; the program is `awaiting Task<T>` completion. `await` can only be used in an `async` method.

The basic structure of an asynchronous method using `async` and `await` would look like this:

```csharp
async Task<T> MethodName()
{
    //...Method body
    await SomeTask;
    //...Continue after SomeTask finishes
}

```

- `async`: This keyword is used to specify that a method is asynchronous.
- `Task<T>`: An asynchronous method should return a `Task` or `Task<T>`. A `Task` represents an ongoing job that might not have been completed when your method returns. The job is executed concurrently with the rest of your program.
- `MethodName`: This is where you put the name of your method.
- Inside the method body, you use the `await` keyword before a task to specify that the method can't continue until the awaited task completes—meanwhile, control returns to the caller of the method.

```csharp
public async Task<int> CalculateSumAsync(int a, int b)
{
    await Task.Delay(500); //Simulate some delay
    return a + b;
}

public async void CallCalculateSumAsync()
{
    int result = await CalculateSumAsync(5, 6);
    Console.WriteLine($"The sum is {result}");
}

```

In this example, the method `CalculateSumAsync` is marked with the `async` keyword and returns a `Task<int>`. Inside the method, we simulate a delay with `Task.Delay`, which we `await`. This means that while we're waiting for the delay to finish, control can be given back to the caller of this method. After the delay is finished, we calculate the sum and return it. In `CallCalculateSumAsync`, we call our asynchronous method and immediately `await` its result. Once we have the result, we print it to the console.

Let's consider an example where we call a web service to fetch data. Fetching data from a web service can be time-consuming, so we will use `async` and `await` to ensure our application remains responsive during this operation.

```csharp
using System.Net.Http; // Network I/O is explained in more detail on the related page
using System.Threading.Tasks;

class Program
{
    static readonly HttpClient client = new HttpClient();

    static async Task Main()
    {
        string responseBody = await GetWebsiteContentAsync("http://example.com");

        Console.WriteLine(responseBody);
    }

    static async Task<string> GetWebsiteContentAsync(string url)
    {
        HttpResponseMessage response = await client.GetAsync(url);
        response.EnsureSuccessStatusCode();
        string responseBody = await response.Content.ReadAsStringAsync();

        return responseBody;
    }
}

```

The `GetWebsiteContentAsync` method is responsible for fetching the content of a website. It uses an `HttpClient` to send an asynchronous GET request to the provided URL. The `await` keyword waits for the task to complete without blocking the rest of the code.

The `client.GetAsync` method returns a `Task<HttpResponseMessage>` representing the ongoing fetch operation. This task is awaited using the `await` keyword. After ensuring that the HTTP response status indicates success by calling the `EnsureSuccessStatusCode()` method, we read the content of the HTTP response message asynchronously using `response.Content.ReadAsStringAsync()`. This method returns a `Task<string>,` which is also awaited.

Finally, in our `Main` method, we call `GetWebsiteContentAsync` and await its result before writing it to the console.

## Tasks

A Task can be in one of three states: `created`, `running`, or `completed`. Once a Task is completed, it can either result in a value, an exception, or nothing at all.

There are two types of tasks: `Task` and `Task<T>`.

- A `Task` represents a single operation that does not return a value and usually executes asynchronously. After the operation is completed, the Task is marked as completed. This is essentially a `void` async method.

- `Task<T>` represents an asynchronous operation that returns a value. The value type (denoted by `T`) is known and can be retrieved once the Task has finished execution.


Creating tasks can be done using the `Task.Run` method or implement methods marked with the `async` keyword that return a `Task` or `Task<T>`. Here's an example of creating and running a task:

```csharp
Task<int> task = Task.Run(() => {
    // Simulate work.
    Thread.Sleep(1000);
    return 69;
});

```

In this example, we create a task that sleeps for one second to simulate work and then returns the integer 69.

## Task Cancellation

If necessary, tasks can also be cancelled through the use of cancellation tokens.

```csharp
CancellationTokenSource cts = new CancellationTokenSource();
Task<int> task = Task.Run(() => {
    // Simulate work.
    Thread.Sleep(1000);
    cts.Token.ThrowIfCancellationRequested();
    return 42;
}, cts.Token);

// Cancel the task.
cts.Cancel();

```

`CancellationToken` is a struct that can be checked periodically by an operation, and if cancellation is requested, the operation can stop itself in a controlled manner.

Cancellation is signalled via the `CancellationTokenSource`. When you want to cancel one or more operations, you call `Cancel` on the `CancellationTokenSource`, which sends a signal to all linked `CancellationToken` instances.

```csharp
public async Task PerformOperationAsync(CancellationToken cancellationToken)
{
    for (int i = 0; i < 100; i++)
    {
        // Simulate some work.
        await Task.Delay(100);

        // Check for cancellation.
        cancellationToken.ThrowIfCancellationRequested();
    }
}

public async Task MainAsync()
{
    var cts = new CancellationTokenSource();

    var task = PerformOperationAsync(cts.Token);

    // After 500 ms, cancel the operation.
    await Task.Delay(500);
    cts.Cancel();

    try
    {
        await task;
    }
    catch (OperationCanceledException)
    {
        Console.WriteLine("Operation was cancelled.");
    }
}

```

In this example, we pass a `CancellationToken` to the `PerformOperationAsync` method. Inside the method, after each unit of work (simulated with `Task.Delay`), we check if cancellation has been requested using `cancellationToken.ThrowIfCancellationRequested()`. This method throws an `OperationCanceledException` if a cancellation has been requested.

In the `MainAsync` method, we start the operation and cancel it after 500 ms by calling `cts.Cancel()`. This sends a signal to the associated cancellation token. When we await the task, it throws an `OperationCanceledException`, which we catch and handle.

## Exception Handling with Async Code

Exception handling is a critical part of asynchronous programming. When you're dealing with asynchronous operations, there's always a possibility that something might go wrong. The operation could fail, the network could go down, data could be corrupted - the list goes on. Without proper exception handling, these errors could cause your application to crash or behave unpredictably.

Exceptions are propagated when you use `await` on the task. If the task has thrown any exceptions, `await` will re-throw that exception.

```csharp
try
{
    string result = await GetWebsiteContentAsync();
}
catch (HttpRequestException ex)
{
    Console.WriteLine($"An error occurred: {ex.Message}");
}

```

In this example, we make a web request using the fictitious `FetchDataFromWebAsync` method. If the request fails and throws an `HttpRequestException`, our `catch` block will handle it and write an error message to the console.

If you're dealing with multiple `Tasks` and want to handle exceptions for each Task independently, you can use `Task.ContinueWith`. This method creates a continuation that executes when the task completes, regardless of the state of the antecedent task.

```csharp
var task = FetchDataFromWebAsync();
task.ContinueWith(t =>
{
    if (t.IsFaulted)
    {
        Console.WriteLine($"An error occurred: {t.Exception.InnerException.Message}");
    }
});

```

In this example, `ContinueWith` is used to specify an action that will happen when the task completes. If the task is faulted (an unhandled exception was thrown), it writes an error message to the console.


# File I/O

* * *

File Input/Output (I/O) is a critical aspect of many applications and is well supported in C# through the `System.IO` namespace. This namespace provides numerous classes that enable reading from and writing to files, creating new files and directories, and performing operations such as moving, copying, or deleting files.

## FileStream

The `FileStream` class, part of the `System.IO` namespace, provides a powerful and flexible interface for reading from and writing to files. As a core component of C#'s I/O library, `FileStream` supports both sequential and random file access, allowing you to interact with a file's content anywhere, not just at its beginning or end.

A `FileStream` object can be seen as a cursor into the contents of a file, much like a text cursor that you move when editing a document. You can place this cursor at any position within the file and perform read or write operations.

### Creating a FileStream

There are several ways to create a `FileStream`. One common approach is using its constructor directly, as shown in the following code snippet:

```csharp
FileStream fs = new FileStream("test.dat", FileMode.OpenOrCreate, FileAccess.ReadWrite);

```

In this example, the `FileStream` constructor takes three arguments:

1. The first argument is a string specifying the path to the file.

2. The second argument is an enumeration of the type `FileMode`, which determines how the operating system should open the file. In this case, `FileMode.OpenOrCreate` means that the file should be opened if it exists; otherwise, a new file should be created.

3. The third argument is an enumeration of the type `FileAccess`, which indicates the type of access you want to the file. Here, `FileAccess.ReadWrite` grants the rights to read from and write to the file.


### Reading and Writing with FileStream

To write data to a file, you use the `Write` method of the `FileStream` class.

```csharp
byte[] data = new byte[] { 1, 2, 3, 4, 5 };
fs.Write(data, 0, data.Length);

```

In this example, `Write` is called on the `FileStream` object `fs` to write the byte array `data` to the file. The second and third arguments to `Write` are the starting point in the array and the number of bytes to write, respectively.

To read data from a file, you can use the `Read` method of the `FileStream` class, as shown in the following example:

```csharp
byte[] data = new byte[1024];
int bytesRead = fs.Read(data, 0, data.Length);

```

In this case, `Read` is called on the `FileStream` object `fs` to read bytes into the `data` array. The second and third arguments to `Read` are the starting point in the array and the maximum number of bytes to read, respectively. `Read` returns the actual number of bytes read, which may be less than the requested number if the end of the file is reached.

### Manipulating the File Position

An important feature of `FileStream` is the ability to get or set the position within the file, represented by the `Position` property. For example, you can move to the start of the file with the following code:

```csharp
fs.Position = 0;

```

Or, you can move to a specific position within the file:

```csharp
fs.Position = 50; // Moves to the 51st byte in the file.

```

This feature of random access is particularly useful when dealing with large files or when you need to jump to specific sections of a file.

### Closing the FileStream

Finally, when you're done with a `FileStream`, it's essential to close it to free up the resources it's using. You can do this with the `Close` method:

```csharp
fs.Close();

```

Alternatively, since `FileStream` implements `IDisposable`, you can take advantage of the `using` statement to automatically close the stream:

```csharp
using (FileStream fs = new FileStream("test.dat", FileMode.OpenOrCreate, FileAccess.ReadWrite))
{
    // perform file operations...
}

```

When the `using` block is exited (either after normal execution or an exception), the `Dispose` method is called on `fs`, which in turn calls `Close`, ensuring that the file is properly closed.

## StreamReader and StreamWriter

`StreamReader` and `StreamWriter` are powerful classes within the `System.IO` namespace for reading and writing character data. As high-level abstractions, they provide a more convenient interface for dealing with text files than the `FileStream` class.

### StreamReader

A `StreamReader` reads characters from a byte stream in a particular encoding (such as UTF-8). It's ideal for reading text files.

#### Creating a StreamReader

A `StreamReader` is typically instantiated with a `FileStream` or a file path. For example:

```csharp
StreamReader sr = new StreamReader("test.txt");

```

This code creates a `StreamReader` to read from the file `test.txt`.

#### Reading Data with StreamReader

`StreamReader` provides several methods to read data from the stream. For instance, you can read one line at a time with `ReadLine`:

```csharp
string line = sr.ReadLine();

```

To read the entire content of the file at once, you can use the `ReadToEnd` method:

```csharp
string content = sr.ReadToEnd();

```

Remember to close the `StreamReader` when you're done with it:

```csharp
sr.Close();

```

### StreamWriter

While `StreamReader` is used for reading text data, `StreamWriter` is used for writing text data. It's an efficient way to write text to a file or a stream.

#### Creating a StreamWriter

A `StreamWriter` can be instantiated in a similar way to `StreamReader`. You can pass a `FileStream` or a file path to the constructor:

```csharp
StreamWriter sw = new StreamWriter("test.txt");

```

This code creates a `StreamWriter` that writes to the file "test.txt".

#### Writing Data with StreamWriter

`StreamWriter` provides several methods for writing data to the stream. You can write a string with the `Write` method:

```csharp
sw.Write("Hello, World!");

```

To write a string and then immediately follow it with a newline, use `WriteLine`:

```csharp
sw.WriteLine("Hello, World!");

```

Remember to close the `StreamWriter` when you're done with it:

```csharp
sw.Close();

```

In StreamReader and StreamWriter, you can use the `using` statement, which automatically closes the stream when the `using` block is exited. This ensures that resources are correctly disposed of, even if an exception is thrown within the block:

```csharp
using (StreamWriter sw = new StreamWriter("test.txt"))
{
    sw.WriteLine("Hello, World!");
}

```

## File and Directory

The `File` and `Directory` classes in the `System.IO` namespace contain static methods for creating, copying, deleting, moving, and opening files and directories and performing various other file and directory operations.

### File

The `File` class allows you to work with files. It provides static methods, so you don't need to instantiate the class to use these methods.

#### Creating and Writing to a File

The `WriteAllText` method writes a specified string to a file. If the file already exists, it will be overwritten. If it doesn't exist, the method will create it:

```csharp
File.WriteAllText("test.txt", "Hello, World!");

```

#### Reading from a File

The `ReadAllText` method reads all text from a file and returns it as a string:

```csharp
string content = File.ReadAllText("test.txt");
Console.WriteLine(content);

```

#### Checking if a File Exists

You can check whether a file exists using the `Exists` method:

```csharp
if (File.Exists("test.txt"))
{
    Console.WriteLine("The file exists.");
}

```

### Directory

The `Directory` class provides static methods for manipulating directories.

#### Creating a Directory

You can create a directory using the `CreateDirectory` method:

```csharp
Directory.CreateDirectory("TestDirectory");

```

This code creates a new directory named `TestDirectory`. If the directory already exists, this method does not create a new directory but doesn’t return an error.

#### Checking if a Directory Exists

You can check whether a directory exists using the `Exists` method:

```csharp
if (Directory.Exists("TestDirectory"))
{
    Console.WriteLine("The directory exists.");
}

```

#### Getting Files and Subdirectories

The `GetFiles` method returns the names of files in a directory, and the `GetDirectories` method returns the names of subdirectories:

```csharp
string[] files = Directory.GetFiles("TestDirectory");
string[] subdirectories = Directory.GetDirectories("TestDirectory");

```


# Network I/O

* * *

Network Input/Output (I/O) forms the backbone of most modern applications. It's how applications interact with networks, allowing them to send and receive data to and from remote servers.

C# provides comprehensive support for `Network I/O` operations through its `System.Net` and `System.Net.Sockets` namespaces, among others. These namespaces include a variety of classes and methods that encapsulate the complexity of network programming, making it easier for developers to create network-centric applications.

## HttpClient

The `HttpClient` class in C# is a part of the `System.Net.Http` namespace and provides a modern, flexible, and highly configurable way to send HTTP requests and receive HTTP responses from a resource identified by a URI (Uniform Resource Identifier). It's frequently used to consume APIs, download files, or scrape web content.

The `HttpClient` class is designed to be re-used for multiple requests. As such, it's typically instantiated once and re-used throughout the life of an application, which can improve performance and system resource usage by allowing socket reuse.

The `HttpClient` class includes several methods to send HTTP requests. The primary methods are:

- `GetAsync`: Sends a GET request to the specified URI and returns the response body as a string.
- `PostAsync`: Sends a POST request to the specified URI with a specified content.
- `PutAsync`: Sends a PUT request to the specified URI with a specified content.
- `DeleteAsync`: Sends a DELETE request to the specified URI.

```csharp
HttpClient client = new HttpClient();

// Send a GET request
var response = await client.GetAsync("https://api.example.com/data");

// Ensure we get a successful response
response.EnsureSuccessStatusCode();

// Read the response content
string content = await response.Content.ReadAsStringAsync();

```

In this example, we create an instance of `HttpClient`, send a `GET` request to a specified URI, ensure we received a successful response, and then read the response content into a string.

### GetAsync

`GetAsync` sends a `GET` request to a specified URI. This is an asynchronous operation, meaning the method returns immediately after calling without waiting for the HTTP response. Instead, it returns a Task representing the ongoing operation, which eventually produces the `HttpResponseMessage` once completed.

```csharp
using System;
using System.Net.Http;
using System.Threading.Tasks;

class Program
{
    static readonly HttpClient client = new HttpClient();

    static async Task Main()
    {
        try
        {
            HttpResponseMessage response = await client.GetAsync("http://api.example.com/data");
            response.EnsureSuccessStatusCode();
            string responseBody = await response.Content.ReadAsStringAsync();
            Console.WriteLine(responseBody);
        }
        catch(HttpRequestException e)
        {
            Console.WriteLine("Exception Caught!");
            Console.WriteLine($"Message: {e.Message}");
        }
    }
}

```

In this example, we send a `GET` request to `http://api.example.com/data`, and then read the response body into a string.

### PostAsync

`PostAsync` is another method in the `HttpClient` class. It sends a POST request to a specified URI and some HTTP content. Like `GetAsync`, it's an asynchronous operation and returns a `Task<HttpResponseMessage>`.

```csharp
using System;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;

class Program
{
    static readonly HttpClient client = new HttpClient();

    static async Task Main()
    {
        try
        {
            var json = "{\"name\":\"John Doe\"}";
            HttpContent content = new StringContent(json, Encoding.UTF8, "application/json");
            HttpResponseMessage response = await client.PostAsync("http://api.example.com/data", content);
            response.EnsureSuccessStatusCode();
            string responseBody = await response.Content.ReadAsStringAsync();
            Console.WriteLine(responseBody);
        }
        catch(HttpRequestException e)
        {
            Console.WriteLine("Exception Caught!");
            Console.WriteLine($"Message: {e.Message}");
        }
    }
}

```

In this case, we send a JSON object as the body of our POST request.

### PutAsync

`PutAsync` works much like `PostAsync`, but it sends a `PUT` request instead. It's used when you want to update a resource at a specific URI with some new data.

```csharp
using System;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;

class Program
{
    static readonly HttpClient client = new HttpClient();

    static async Task Main()
    {
        try
        {
            var json = "{\"id\":1,\"name\":\"John Doe Updated\"}";
            HttpContent content = new StringContent(json, Encoding.UTF8, "application/json");
            HttpResponseMessage response = await client.PutAsync("http://api.example.com/data/1", content);
            response.EnsureSuccessStatusCode();
            string responseBody = await response.Content.ReadAsStringAsync();
            Console.WriteLine(responseBody);
        }
        catch(HttpRequestException e)
        {
            Console.WriteLine("Exception Caught!");
            Console.WriteLine($"Message: {e.Message}");
        }
    }
}

```

In this example, we send a PUT request to update the resource at `http://api.example.com/data/1` with new data.

### DeleteAsync

Finally, `DeleteAsync` sends a `DELETE` request to a specified URI. It's typically used when deleting a resource at a specific URI.

```csharp
using System;
using System.Net.Http;
using System.Threading.Tasks;

class Program
{
    static readonly HttpClient client = new HttpClient();

    static async Task Main()
    {
        try
        {
            HttpResponseMessage response = await client.DeleteAsync("http://api.example.com/data/1");
            response.EnsureSuccessStatusCode();
            string responseBody = await response.Content.ReadAsStringAsync();
            Console.WriteLine(responseBody);
        }
        catch(HttpRequestException e)
        {
            Console.WriteLine("Exception Caught!");
            Console.WriteLine($"Message: {e.Message}");
        }
    }
}

```

In this case, we send a `DELETE` request to `http://api.example.com/data/1` to delete the resource.


# Skills Assessment

* * *

You are part of a team of software developers building a tool to enhance network security. This tool should be able to scan a target host and find sensitive files that should not exist on the server; in this case, you are specifically looking for a `flag.txt` file. To make this operation more efficient, you have been provided with a wordlist in the `Assessment.dll` library, which includes common paths in which sensitive files are known to exist. The word list is accessible in the `GetWordList()` method in the `Words` class, via the `Assessment` namespace.

Your task is to create a C# application that will iterate through the wordlist, using each word as a potential path on the target host. You will make HTTP requests to these paths and check for the existence of `flag.txt`. The program will output the paths where the `flag.txt` file exists.


