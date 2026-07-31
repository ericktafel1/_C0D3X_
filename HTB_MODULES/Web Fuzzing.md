# Introduction

* * *

Web fuzzing is a critical technique in web application security to identify vulnerabilities by testing various inputs. It involves automated testing of web applications by providing unexpected or random data to detect potential flaws that attackers could exploit.

In the world of web application security, the terms " `fuzzing`" and " `brute-forcing`" are often used interchangeably, and for beginners, it's perfectly fine to consider them as similar techniques. However, there are some subtle distinctions between the two:

## Fuzzing vs. Brute-forcing

- Fuzzing casts a wider net. It involves feeding the web application with unexpected inputs, including malformed data, invalid characters, and nonsensical combinations. The goal is to see how the application reacts to these strange inputs and uncover potential vulnerabilities in handling unexpected data. Fuzzing tools often leverage wordlists containing common patterns, mutations of existing parameters, or even random character sequences to generate a diverse set of payloads.

- Brute-forcing, on the other hand, is a more targeted approach. It focuses on systematically trying out many possibilities for a specific value, such as a password or an ID number. Brute-forcing tools typically rely on predefined lists or dictionaries (like password dictionaries) to guess the correct value through trial and error.


Here's an analogy to illustrate the difference: Imagine you're trying to open a locked door. Fuzzing would be like throwing everything you can find at the door - keys, screwdrivers, even a rubber duck - to see if anything unlocks it. Brute-forcing would be like trying every combination on a key ring until you find the one that opens the door.

### Why Fuzz Web Applications?

Web applications have become the backbone of modern businesses and communication, handling vast amounts of sensitive data and enabling critical online interactions. However, their complexity and interconnectedness also make them prime targets for cyberattacks. Manual testing, while essential, can only go so far in identifying vulnerabilities. Here's where web fuzzing shines:

- `Uncovering Hidden Vulnerabilities`: Fuzzing can uncover vulnerabilities that traditional security testing methods might miss. By bombarding a web application with unexpected and invalid inputs, fuzzing can trigger unexpected behaviors that reveal hidden flaws in the code.
- `Automating Security Testing`: Fuzzing automates generating and sending test inputs, saving valuable time and resources. This allows security teams to focus on analyzing results and addressing the vulnerabilities found.
- `Simulating Real-World Attacks`: Fuzzers can mimic attackers' techniques, helping you identify weaknesses before malicious actors exploit them. This proactive approach can significantly reduce the risk of a successful attack.
- `Strengthening Input Validation`: Fuzzing helps identify weaknesses in input validation mechanisms, which are crucial for preventing common vulnerabilities like `SQL injection` and `cross-site scripting` ( `XSS`).
- `Improving Code Quality`: Fuzzing improves overall code quality by uncovering bugs and errors. Developers can use the feedback from fuzzing to write more robust and secure code.
- `Continuous Security`: Fuzzing can be integrated into the `software development lifecycle` ( `SDLC`) as part of `continuous integration and continuous deployment` ( `CI/CD`) pipelines, ensuring that security testing is performed regularly and vulnerabilities are caught early in the development process.

In a nutshell, web fuzzing is an indispensable tool in the arsenal of any security professional. By proactively identifying and addressing vulnerabilities through fuzzing, you can significantly enhance the security of your web applications and protect them from potential threats.

## Essential Concepts

Before we dive into the practical aspects of web fuzzing, it's important to understand some key concepts:

| Concept | Description | Example |
| --- | --- | --- |
| `Wordlist` | A dictionary or list of words, phrases, file names, directory names, or parameter values used as input during fuzzing. | Generic: `admin`, `login`, `password`, `backup`, `config`<br>Application-specific: `productID`, `addToCart`, `checkout` |
| `Payload` | The actual data sent to the web application during fuzzing. Can be a simple string, numerical value, or complex data structure. | `' OR 1=1 --` (for SQL injection) |
| `Response Analysis` | Examining the web application's responses (e.g., response codes, error messages) to the fuzzer's payloads to identify anomalies that might indicate vulnerabilities. | Normal: 200 OK<br>Error (potential SQLi): 500 Internal Server Error with a database error message |
| `Fuzzer` | A software tool that automates generating and sending payloads to a web application and analyzing the responses. | `ffuf`, `wfuzz`, `Burp Suite Intruder` |
| `False Positive` | A result that is incorrectly identified as a vulnerability by the fuzzer. | A 404 Not Found error for a non-existent directory. |
| `False Negative` | A vulnerability that exists in the web application but is not detected by the fuzzer. | A subtle logic flaw in a payment processing function. |
| `Fuzzing Scope` | The specific parts of the web application that you are targeting with your fuzzing efforts. | Only fuzzing the login page or focusing on a particular API endpoint. |


# Tooling

* * *

In this module, we will utilize four powerful tools designed for web application reconnaissance and vulnerability assessment. To streamline our setup, we'll install them all upfront.

### Installing Go, Python and PIPX

You will require Go and Python installed for these tools. Install them as follows if you don't have them installed already.

`pipx` is a command-line tool designed to simplify the installation and management of Python applications. It streamlines the process by creating isolated virtual environments for each application, ensuring that dependencies don't conflict. This means you can install and run multiple Python applications without worrying about compatibility issues. `pipx` also makes it easy to upgrade or uninstall applications, keeping your system organized and clutter-free.

If you are using a Debian-based system (like Ubuntu), you can install Go, Python, and PIPX using the APT package manager.

1. Open a terminal and update your package lists to ensure you have the latest information on the newest versions of packages and their dependencies.


```shell
sudo apt update

```

2. Use the following command to install Go:


```shell
sudo apt install -y golang

```

3. Use the following command to install Python:


```shell
sudo apt install -y python3 python3-pip

```

4. Use the following command to install and configure pipx:


```shell
sudo apt install pipx
pipx ensurepath
sudo pipx ensurepath --global

```

5. To ensure that Go and Python are installed correctly, you can check their versions:


```shell
go version
python3 --version

```


If the installations were successful, you should see the version information for both Go and Python.

## FFUF

`FFUF` ( `Fuzz Faster U Fool`) is a fast web fuzzer written in Go. It excels at quickly enumerating directories, files, and parameters within web applications. Its flexibility, speed, and ease of use make it a favorite among security professionals and enthusiasts.

You can install `FFUF` using the following command:

```shell
go install github.com/ffuf/ffuf/v2@latest

```

### Use Cases

| Use Case | Description |
| --- | --- |
| `Directory and File Enumeration` | Quickly identify hidden directories and files on a web server. |
| `Parameter Discovery` | Find and test parameters within web applications. |
| `Brute-Force Attack` | Perform brute-force attacks to discover login credentials or other sensitive information. |

## Gobuster

`Gobuster` is another popular web directory and file fuzzer. It's known for its speed and simplicity, making it a great choice for beginners and experienced users alike.

You can install `GoBuster` using the following command:

```shell
go install github.com/OJ/gobuster/v3@latest

```

### Use Cases

| Use Case | Description |
| --- | --- |
| `Content Discovery` | Quickly scan and find hidden web content such as directories, files, and virtual hosts. |
| `DNS Subdomain Enumeration` | Identify subdomains of a target domain. |
| `WordPress Content Detection` | Use specific wordlists to find WordPress-related content. |

## FeroxBuster

`FeroxBuster` is a fast, recursive content discovery tool written in Rust. It's designed for brute-force discovery of unlinked content in web applications, making it particularly useful for identifying hidden directories and files. It's more of a "forced browsing" tool than a fuzzer like `ffuf`.

To install `FeroxBuster`, you can use the following command:

```shell
curl -sL https://raw.githubusercontent.com/epi052/feroxbuster/main/install-nix.sh | sudo bash -s $HOME/.local/bin

```

### Use Cases

| Use Case | Description |
| --- | --- |
| `Recursive Scanning` | Perform recursive scans to discover nested directories and files. |
| `Unlinked Content Discovery` | Identify content that is not linked within the web application. |
| `High-Performance Scans` | Benefit from Rust's performance to conduct high-speed content discovery. |

## wfuzz/wenum

`wenum` is an actively maintained fork of `wfuzz`, a highly versatile and powerful command-line fuzzing tool known for its flexibility and customization options. It's particularly well-suited for parameter fuzzing, allowing you to test a wide range of input values against web applications and uncover potential vulnerabilities in how they process those parameters.

If you are using a penetration testing Linux distribution like PwnBox or Kali, `wfuzz` may already be pre-installed, allowing you to use it right away if desired. However, there are currently complications when installing `wfuzz`, so you can substitute it with `wenum` instead. The commands are interchangeable, and they follow the same syntax, so you can simply replace `wenum` commands with `wfuzz` if necessary.

The following commands will use `pipx`, a tool for installing and managing Python applications in isolated environments, to install `wenum`. This ensures a clean and consistent environment for `wenum`, preventing any possible package conflicts:

```shell
pipx install git+https://github.com/WebFuzzForge/wenum
pipx runpip wenum install setuptools

```

### Use Cases

| Use Case | Description |
| --- | --- |
| `Directory and File Enumeration` | Quickly identify hidden directories and files on a web server. |
| `Parameter Discovery` | Find and test parameters within web applications. |
| `Brute-Force Attack` | Perform brute-force attacks to discover login credentials or other sensitive information. |


# Directory and File Fuzzing

* * *

Web applications often have directories and files that are not directly linked or visible to users. These hidden resources may contain sensitive information, backup files, configuration files, or even old, vulnerable application versions. Directory and file fuzzing aims to uncover these hidden assets, providing attackers with potential entry points or valuable information for further exploitation.

## Uncovering Hidden Assets

Web applications often house a treasure trove of hidden resources — directories, files, and endpoints that aren't readily accessible through the main interface. These concealed areas might hold valuable information for attackers, including:

- `Sensitive data`: Backup files, configuration settings, or logs containing user credentials or other confidential information.
- `Outdated content`: Older versions of files or scripts that may be vulnerable to known exploits.
- `Development resources`: Test environments, staging sites, or administrative panels that could be leveraged for further attacks.
- `Hidden functionalities`: Undocumented features or endpoints that could expose unexpected vulnerabilities.

Discovering these hidden assets is crucial for security researchers and penetration testers. It provides a deeper understanding of a web application's attack surface and potential vulnerabilities.

### The Importance of Finding Hidden Assets

Uncovering these hidden gems is far from trivial. Each discovery contributes to a complete picture of the web application's structure and functionality, essential for a thorough security assessment. These hidden areas often lack the robust security measures found in public-facing components, making them prime targets for exploitation. By proactively identifying these vulnerabilities, you can stay one step ahead of malicious actors.

Even if a hidden asset doesn't immediately reveal a vulnerability, the information gleaned can prove invaluable in the later stages of a penetration test. This could include anything from understanding the underlying technology stack to discovering sensitive data that can be used for further attacks.

`Directory and file fuzzing` are among the most effective methods for uncovering these hidden assets. This involves systematically probing the web application with a list of potential directory and file names and analyzing the server's responses to identify valid resources.

## Wordlists

Wordlists are the lifeblood of directory and file fuzzing. They provide the potential directory and file names your chosen tool will use to probe the web application. Effective wordlists can significantly increase your chances of discovering hidden assets.

Wordlists are typically compiled from various sources. This often includes scraping the web for common directory and file names, analyzing publicly available data breaches, and extracting directory information from known vulnerabilities. These wordlists are then meticulously curated, removing duplicates and irrelevant entries to ensure optimal efficiency and effectiveness during fuzzing operations. The goal is to create a comprehensive list of potential directories and file names that will likely be found on web servers, allowing you to thoroughly probe a target application for hidden assets.

The tools we've discussed – `ffuf`, `wfuzz`, etc – don't have built-in wordlists, but they are designed to work seamlessly with external wordlist files. This flexibility allows you to use pre-existing wordlists or create your own to tailor your fuzzing efforts to specific targets and scenarios.

One of the most comprehensive and widely-used collections of wordlists is `SecLists`. This open-source project on GitHub (https://github.com/danielmiessler/SecLists) provides a vast repository of wordlists for various security testing purposes, including directory and file fuzzing.

**On pwnbox specifically, the seclists folder is located in /usr/share/seclists/, all lowercase, but other distributions might name it as per the repository, SecLists, so if a command doesn't work, double check the wordlist path.**

`SecLists` contains wordlists for:

- Common directory and file names
- Backup files
- Configuration files
- Vulnerable scripts
- And much more

The most commonly used wordlists for fuzzing web directories and files from `SecLists` are:

- `Discovery/Web-Content/common.txt`: This general-purpose wordlist contains a broad range of common directory and file names on web servers. It's an excellent starting point for fuzzing and often yields valuable results.
- `Discovery/Web-Content/directory-list-2.3-medium.txt`: This is a more extensive wordlist specifically focused on directory names. It's a good choice when you need a deeper dive into potential directories.
- `Discovery/Web-Content/raft-large-directories.txt`: This wordlist boasts a massive collection of directory names compiled from various sources. It's a valuable resource for thorough fuzzing campaigns.
- `Discovery/Web-Content/big.txt`: As the name suggests, this is a massive wordlist containing both directory and file names. It's useful when you want to cast a wide net and explore all possibilities.

## Actually Fuzzing

Now that you understand the concept of wordlists, let's dive into the fuzzing process. We'll use `ffuf`, a powerful and flexible fuzzing tool, to uncover hidden directories and files on our target web application.

**To follow along, start the target system via the question section at the bottom of the page, replacing the uses of IP:PORT with the IP:PORT for your spawned instance.**

### ffuf

We will use `ffuf` for this fuzzing task. Here's how `ffuf` generally works:

1. `Wordlist`: You provide `ffuf` with a wordlist containing potential directory or file names.
2. `URL with FUZZ keyword`: You construct a URL with the `FUZZ` keyword as a placeholder where the wordlist entries will be inserted.
3. `Requests`: `ffuf` iterates through the wordlist, replacing the `FUZZ` keyword in the URL with each entry and sending HTTP requests to the target web server.
4. `Response Analysis`: `ffuf` analyzes the server's responses (status codes, content length, etc.) and filters the results based on your criteria.

For example, if you want to fuzz for directories, you might use a URL like this:

```http
http://localhost/FUZZ

```

`ffuf` will replace `FUZZ` with words like " `admin`," " `backup`," " `uploads`," etc., from your chosen wordlist and then send requests to `http://localhost/admin`, `http://localhost/backup`, and so on.

### Directory Fuzzing

The first step is to perform directory fuzzing, which helps us discover hidden directories on the web server. Here's the ffuf command we'll use:

```shell
ffuf -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt -u http://IP:PORT/FUZZ

        /'___\  /'___\           /'___\
       /\ \__/ /\ \__/  __  __  /\ \__/
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/
         \ \_\   \ \_\  \ \____/  \ \_\
          \/_/    \/_/   \/___/    \/_/

       v2.1.0-dev
________________________________________________

 :: Method           : GET
 :: URL              : http://IP:PORT/FUZZ
 :: Wordlist         : FUZZ: /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-399
________________________________________________

[...]

w2ksvrus                [Status: 301, Size: 0, Words: 1, Lines: 1, Duration: 0ms]
:: Progress: [220559/220559] :: Job [1/1] :: 100000 req/sec :: Duration: [0:00:03] :: Errors: 0 ::

```

- `-w` (wordlist): Specifies the path to the wordlist we want to use. In this case, we're using a medium-sized directory list from SecLists.
- `-u` (URL): Specifies the base URL to fuzz. The `FUZZ` keyword acts as a placeholder where the fuzzer will insert words from the wordlist.

The output above shows that `ffuf` has discovered a directory called `w2ksvrus` on the target web server, as indicated by the 301 (Moved Permanently) status code. This could be a potential entry point for further investigation.

### File Fuzzing

While directory fuzzing focuses on finding folders, file fuzzing dives deeper into discovering specific files within those directories or even in the root of the web application. Web applications use various file types to serve content and perform different functions. Some common file extensions include:

- `.php`: Files containing PHP code, a popular server-side scripting language.
- `.html`: Files that define the structure and content of web pages.
- `.txt`: Plain text files, often storing simple information or logs.
- `.bak`: Backup files are created to preserve previous versions of files in case of errors or modifications.
- `.js`: Files containing JavaScript code add interactivity and dynamic functionality to web pages.

By fuzzing for these common extensions with a wordlist of common file names, we increase our chances of discovering files that might be unintentionally exposed or misconfigured, potentially leading to information disclosure or other vulnerabilities.

For example, if the website uses PHP, discovering a backup file like `config.php.bak` could reveal sensitive information such as database credentials or API keys. Similarly, finding an old or unused script like `test.php` might expose vulnerabilities that attackers could exploit.

Utilize `ffuf` and a wordlist of common file names to search for hidden files with specific extensions:

```shell
ffuf -w /usr/share/seclists/Discovery/Web-Content/common.txt -u http://IP:PORT/w2ksvrus/FUZZ.html -e .php,.html,.txt,.bak,.js -v

        /'___\  /'___\           /'___\
       /\ \__/ /\ \__/  __  __  /\ \__/
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/
         \ \_\   \ \_\  \ \____/  \ \_\
          \/_/    \/_/   \/___/    \/_/

       v2.1.0-dev
________________________________________________

 :: Method           : GET
 :: URL              : http://IP:PORT/w2ksvrus/FUZZ.html
 :: Wordlist         : FUZZ: /usr/share/seclists/Discovery/Web-Content/common.txt
 :: Extensions       : .php .html .txt .bak .js
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
________________________________________________

[Status: 200, Size: 111, Words: 2, Lines: 2, Duration: 0ms]
| URL | http://IP:PORT/w2ksvrus/dblclk.html
    * FUZZ: dblclk

[Status: 200, Size: 112, Words: 6, Lines: 2, Duration: 0ms]
| URL | http://IP:PORT/w2ksvrus/index.html
    * FUZZ: index

:: Progress: [28362/28362] :: Job [1/1] :: 0 req/sec :: Duration: [0:00:00] :: Errors: 0 ::

```

The `ffuf` output shows that it discovered two files within the `/w2ksvrus` directory:

- `dblclk.html`: This file is 111 bytes in size and consists of 2 words and 2 lines. Its purpose might not be immediately apparent, but it's a potential point of interest for further investigation. Perhaps it contains hidden content or functionality.

- `index.html`: This file is slightly larger at 112 bytes and contains 6 words and 2 lines. It's likely the default index page for the `w2ksvrus` directory.


# Recursive Fuzzing

* * *

So far, we've focused on fuzzing directories directly under the web root and files within a single directory. But what if our target has a complex structure with multiple nested directories? Manually fuzzing each level would be tedious and time-consuming. This is where recursive fuzzing comes in handy.

## How Recursive Fuzzing Works

Recursive fuzzing is an automated way to delve into the depths of a web application's directory structure. It's a pretty basic 3 step process:

1. `Initial Fuzzing`:
   - The fuzzing process begins with the top-level directory, typically the web root ( `/`).
   - The fuzzer starts sending requests based on the provided wordlist containing the potential directory and file names.
   - The fuzzer analyzes server responses, looking for successful results (e.g., HTTP 200 OK) that indicate the existence of a directory.
2. `Directory Discovery and Expansion`:
   - When a valid directory is found, the fuzzer doesn't just note it down. It creates a new branch for that directory, essentially appending the directory name to the base URL.
   - For example, if the fuzzer finds a directory named `admin` at the root level, it will create a new branch like `http://localhost/admin/`.
   - This new branch becomes the starting point for a fresh fuzzing process. The fuzzer will again iterate through the wordlist, appending each entry to the new branch's URL (e.g., `http://localhost/admin/FUZZ`).
3. `Iterative Depth`:
   - The process repeats for each discovered directory, creating further branches and expanding the fuzzing scope deeper into the web application's structure.
   - This continues until a specified depth limit is reached (e.g., a maximum of three levels deep) or no more valid directories are found.

Imagine a tree structure where the web root is the trunk, and each discovered directory is a branch. Recursive fuzzing systematically explores each branch, going deeper and deeper until it reaches the leaves (files) or encounters a predetermined stopping point.

### Why Use Recursive Fuzzing?

Recursive fuzzing is a practical necessity when dealing with complex web applications:

- `Efficiency`: Automating the discovery of nested directories saves significant time compared to manual exploration.
- `Thoroughness`: It systematically explores every branch of the directory structure, reducing the risk of missing hidden assets.
- `Reduced Manual Effort`: You don't need to input each new directory to fuzz manually; the tool handles the entire process.
- `Scalability`: It's particularly valuable for large-scale web applications where manual exploration would be impractical.

In essence, recursive fuzzing is about `working smarter, not harder`. It allows you to efficiently and comprehensively probe the depths of a web application, uncovering potential vulnerabilities that might be lurking in its hidden corners.

## Recursive Fuzzing with ffuf

**To follow along, start the target system via the question section at the bottom of the page, replacing the uses of IP:PORT with the IP:PORT for your spawned instance. We will be using the /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt wordlists for these fuzzing tasks.**

Let's use `ffuf` to demonstrate recursive fuzzing:

```shell
ffuf -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt -ic -v -u http://IP:PORT/FUZZ -e .html -recursion

        /'___\  /'___\           /'___\
       /\ \__/ /\ \__/  __  __  /\ \__/
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/
         \ \_\   \ \_\  \ \____/  \ \_\
          \/_/    \/_/   \/___/    \/_/

       v2.1.0-dev
________________________________________________

 :: Method           : GET
 :: URL              : http://IP:PORT/FUZZ
 :: Wordlist         : FUZZ: /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt
 :: Extensions       : .html
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
________________________________________________

[Status: 301, Size: 0, Words: 1, Lines: 1, Duration: 0ms]
| URL | http://IP:PORT/level1
| --> | /level1/
    * FUZZ: level1

[INFO] Adding a new job to the queue: http://IP:PORT/level1/FUZZ

[INFO] Starting queued job on target: http://IP:PORT/level1/FUZZ

[Status: 200, Size: 96, Words: 6, Lines: 2, Duration: 0ms]
| URL | http://IP:PORT/level1/index.html
    * FUZZ: index.html

[Status: 301, Size: 0, Words: 1, Lines: 1, Duration: 0ms]
| URL | http://IP:PORT/level1/level2
| --> | /level1/level2/
    * FUZZ: level2

[INFO] Adding a new job to the queue: http://IP:PORT/level1/level2/FUZZ

[Status: 301, Size: 0, Words: 1, Lines: 1, Duration: 0ms]
| URL | http://IP:PORT/level1/level3
| --> | /level1/level3/
    * FUZZ: level3

[INFO] Adding a new job to the queue: http://IP:PORT/level1/level3/FUZZ

[INFO] Starting queued job on target: http://IP:PORT/level1/level2/FUZZ

[Status: 200, Size: 96, Words: 6, Lines: 2, Duration: 0ms]
| URL | http://IP:PORT/level1/level2/index.html
    * FUZZ: index.html

[INFO] Starting queued job on target: http://IP:PORT/level1/level3/FUZZ

[Status: 200, Size: 126, Words: 8, Lines: 2, Duration: 0ms]
| URL | http://IP:PORT/level1/level3/index.html
    * FUZZ: index.html

:: Progress: [441088/441088] :: Job [4/4] :: 100000 req/sec :: Duration: [0:00:06] :: Errors: 0 ::

```

Notice the addition of the `-recursion` flag. This tells `ffuf` to fuzz any directories it finds recursively. For example, if `ffuf` discovers an admin directory, it will automatically start a new fuzzing process on `http://localhost/admin/FUZZ`. In fuzzing scenarios where wordlists contain comments (lines starting with #), the `ffuf -ic` option proves invaluable. By enabling this option, `ffuf` intelligently ignores commented lines during fuzzing, preventing them from being treated as valid inputs.

The fuzzing commences at the web root ( `http://IP:PORT/FUZZ`). Initially, `ffuf` identifies a directory named `level1`, indicated by a `301 (Moved Permanently)` response. This signifies a redirection and prompts the tool to initiate a new fuzzing process within this directory, effectively branching out its search.

As `ffuf` recursively explores `level1`, it uncovers two additional directories: `level2` and `level3`. Each is added to the fuzzing queue, expanding the search depth. Furthermore, an `index.html` file is discovered within `level1`.

The fuzzer systematically works through its queue, identifying `index.html` files in both `level2` and `level3`. Notably, the `index.html` file within `level3` stands out due to its larger file size than the others.

Further analysis reveals this file contains the flag `HTB{r3curs1v3_fuzz1ng_w1ns}`, signifying a successful exploration of the nested directory structure.

### Be Responsible

While recursive fuzzing is a powerful technique, it can also be resource-intensive, especially on large web applications. Excessive requests can overwhelm the target server, potentially causing performance issues or triggering security mechanisms.

To mitigate these risks, `ffuf` provides options for fine-tuning the recursive fuzzing process:

- `-recursion-depth`: This flag allows you to set a maximum depth for recursive exploration. For example, `-recursion-depth 2` limits fuzzing to two levels deep (the starting directory and its immediate subdirectories).
- `-rate`: You can control the rate at which `ffuf` sends requests per second, preventing the server from being overloaded.
- `-timeout`: This option sets the timeout for individual requests, helping to prevent the fuzzer from hanging on unresponsive targets.

```shell
ffuf -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt -ic -u http://IP:PORT/FUZZ -e .html -recursion -recursion-depth 2 -rate 500

```


# Parameter and Value Fuzzing

* * *

Building upon the discovery of hidden directories and files, we now delve into parameter and value fuzzing. This technique focuses on manipulating the parameters and their values within web requests to uncover vulnerabilities in how the application processes input.

Parameters are the messengers of the web, carrying vital information between your browser and the server that hosts the web application. They're like variables in programming, holding specific values that influence how the application behaves.

## GET Parameters: Openly Sharing Information

You'll often spot `GET` parameters right in the URL, following a question mark ( `?`). Multiple parameters are strung together using ampersands ( `&`). For example:

```http
https://example.com/search?query=fuzzing&category=security

```

In this URL:

- `query` is a parameter with the value "fuzzing"
- `category` is another parameter with the value "security"

`GET` parameters are like postcards – their information is visible to anyone who glances at the URL. They're primarily used for actions that don't change the server's state, like searching or filtering.

## POST Parameters: Behind-the-Scenes Communication

While `GET` parameters are like open postcards, POST parameters are more like sealed envelopes, carrying their information discreetly within the body of the HTTP request. They are not visible directly in the URL, making them the preferred method for transmitting sensitive data like login credentials, personal information, or financial details.

When you submit a form or interact with a web page that uses POST requests, the following happens:

1. `Data Collection`: The information entered into the form fields is gathered and prepared for transmission.

2. `Encoding`: This data is encoded into a specific format, typically `application/x-www-form-urlencoded` or `multipart/form-data`:
   - `application/x-www-form-urlencoded`: This format encodes the data as key-value pairs separated by ampersands ( `&`), similar to GET parameters but placed within the request body instead of the URL.
   - `multipart/form-data`: This format is used when submitting files along with other data. It divides the request body into multiple parts, each containing a specific piece of data or a file.
3. `HTTP Request`: The encoded data is placed within the body of an HTTP POST request and sent to the web server.

4. `Server-Side Processing`: The server receives the POST request, decodes the data, and processes it according to the application's logic.


Here's a simplified example of how a POST request might look when submitting a login form:

```http
POST /login HTTP/1.1
Host: example.com
Content-Type: application/x-www-form-urlencoded

username=your_username&password=your_password

```

- `POST`: Indicates the HTTP method (POST).
- `/login`: Specifies the URL path where the form data is sent.
- `Content-Type`: Specifies how the data in the request body is encoded ( `application/x-www-form-urlencoded` in this case).
- `Request Body`: Contains the encoded form data as key-value pairs ( `username` and `password`).

## Why Parameters Matter for Fuzzing

Parameters are the gateways through which you can interact with a web application. By manipulating their values, you can test how the application responds to different inputs, potentially uncovering vulnerabilities. For instance:

- Altering a product ID in a shopping cart URL could reveal pricing errors or unauthorized access to other users' orders.
- Modifying a hidden parameter in a request might unlock hidden features or administrative functions.
- Injecting malicious code into a search query could expose vulnerabilities like Cross-Site Scripting (XSS) or SQL Injection (SQLi).

## wenum

In this section, we'll leverage `wenum` to explore both GET and POST parameters within our target web application, ultimately aiming to uncover hidden values that trigger unique responses, potentially revealing vulnerabilities.

To follow along, start the target system via the question section at the bottom of the page, replacing the uses of IP:PORT with the `IP`: `PORT` for your spawned instance. We will be using the `/usr/share/seclists/Discovery/Web-Content/common.txt` wordlists for these fuzzing tasks.

Let's first ready our tools by installing `wenum` to our attack host:

```shell
pipx install git+https://github.com/WebFuzzForge/wenum
pipx runpip wenum install setuptools

```

Then to begin, we will use `curl` to manually interact with the endpoint and gain a better understanding of its behavior:

```shell
curl http://IP:PORT/get.php

Invalid parameter value
x:

```

The response tells us that the parameter `x` is missing. Let's try adding a value:

```shell
curl http://IP:PORT/get.php?x=1

Invalid parameter value
x: 1

```

The server acknowledges the `x` parameter this time but indicates that the provided value ( `1`) is invalid. This suggests that the application is indeed checking the value of this parameter and producing different responses based on its validity. We aim to find the specific value to trigger a different and hopefully more revealing response.

Manually guessing parameter values would be tedious and time-consuming. This is where `wenum` comes in handy. It allows us to automate the process of testing many potential values, significantly increasing our chances of finding the correct one.

Let's use `wenum` to fuzz the " `x`" parameter's value, starting with the `common.txt` wordlist from SecLists:

```shell
wenum -w /usr/share/seclists/Discovery/Web-Content/common.txt --hc 404 -u "http://IP:PORT/get.php?x=FUZZ"

...
 Code    Lines     Words        Size  Method   URL
...
 200       1 L       1 W        25 B  GET      http://IP:PORT/get.php?x=OA...

Total time: 0:00:02
Processed Requests: 4731
Filtered Requests: 4730
Requests/s: 1681

```

- `-w`: Path to your wordlist.
- `--hc 404`: Hides responses with the 404 status code (Not Found), since `wenum` by default will log every request it makes.
- `http://IP:PORT/get.php?x=FUZZ`: This is the target URL. `wenum` will replace the parameter value `FUZZ` with words from the wordlist.

Analyzing the results, you'll notice that most requests return the "Invalid parameter value" message and the incorrect value you tried. However, one line stands out:

```bash
 200       1 L       1 W        25 B  GET      http://IP:PORT/get.php?x=OA...

```

This indicates that when the parameter `x` was set to the value " `OA...`," the server responded with a `200 OK` status code, suggesting a valid input.

If you try accessing `http://IP:PORT/get.php?x=OA...`, you'll see the flag.

```shell
curl http://IP:PORT/get.php?x=OA...

HTB{...}

```

### POST

Fuzzing POST parameters requires a slightly different approach than fuzzing GET parameters. Instead of appending values directly to the URL, we'll use `ffuf` to send the payloads within the request body. This enables us to test how the application handles data submitted through forms or other POST mechanisms.

Our target application also features a POST parameter named " `y`" within the `post.php` script. Let's probe it with `curl` to see its default behavior:

```shell
curl -d "" http://IP:PORT/post.php

Invalid parameter value
y:

```

The `-d` flag instructs `curl` to make a POST request with an empty body. The response tells us that the parameter `y` is expected but not provided.

As with GET parameters, manually testing POST parameter values would be inefficient. We'll use `ffuf` to automate this process:

```shell
ffuf -u http://IP:PORT/post.php -X POST -H "Content-Type: application/x-www-form-urlencoded" -d "y=FUZZ" -w /usr/share/seclists/Discovery/Web-Content/common.txt -mc 200 -v

        /'___\  /'___\           /'___\
       /\ \__/ /\ \__/  __  __  /\ \__/
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/
         \ \_\   \ \_\  \ \____/  \ \_\
          \/_/    \/_/   \/___/    \/_/

       v2.1.0-dev
________________________________________________

 :: Method           : POST
 :: URL              : http://IP:PORT/post.php
 :: Wordlist         : FUZZ: /usr/share/seclists/Discovery/Web-Content/common.txt
 :: Header           : Content-Type: application/x-www-form-urlencoded
 :: Data             : y=FUZZ
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200
________________________________________________

[Status: 200, Size: 26, Words: 1, Lines: 2, Duration: 7ms]
| URL | http://IP:PORT/post.php
    * FUZZ: SU...

:: Progress: [4730/4730] :: Job [1/1] :: 5555 req/sec :: Duration: [0:00:01] :: Errors: 0 ::

```

The main difference here is the use of the `-d` flag, which tells `ffuf` that the payload (" `y=FUZZ`") should be sent in the request body as `POST` data.

Again, you'll see mostly invalid parameter responses. The correct value (" `SU...`") will stand out with its `200 OK` status code:

```bash
000000326:  200     1 L      1 W     26 Ch     "SU..."

```

Similarly, after identifying " `SU...`" as the correct value, validate it with `curl`:

```shell
curl -d "y=SU..." http://IP:PORT/post.php

HTB{...}

```

In a real-world scenario, these flags would not be present, and identifying valid parameter values might require a more nuanced analysis of the responses. However, this exercise provides a simplified demonstration of how to leverage `ffuf` to automate the process of testing many potential parameter values.


# Virtual Host and Subdomain Fuzzing

* * *

Both virtual hosting (vhosting) and subdomains play pivotal roles in organizing and managing web content.

Virtual hosting enables multiple websites or domains to be served from a single server or IP address. Each vhost is associated with a unique domain name or hostname. When a client sends an HTTP request, the web server examines the `Host` header to determine which vhost's content to deliver. This facilitates efficient resource utilization and cost reduction, as multiple websites can share the same server infrastructure.

Subdomains, on the other hand, are extensions of a primary domain name, creating a hierarchical structure within the domain. They are used to organize different sections or services within a website. For example, `blog.example.com` and `shop.example.com` are subdomains of the main domain `example.com`. Unlike vhosts, subdomains are resolved to specific IP addresses through DNS (Domain Name System) records.

| Feature | Virtual Hosts | Subdomains |
| --- | --- | --- |
| Identification | Identified by the `Host` header in HTTP requests. | Identified by DNS records, pointing to specific IP addresses. |
| Purpose | Primarily used to host multiple websites on a single server. | Used to organize different sections or services within a website. |
| Security Risks | Misconfigured vhosts can expose internal applications or sensitive data. | Subdomain takeover vulnerabilities can occur if DNS records are mismanaged. |

## Gobuster

`Gobuster` is a versatile command-line tool renowned for its directory/file and DNS busting capabilities. It systematically probes target web servers or domains to uncover hidden directories, files, and subdomains, making it a valuable asset in security assessments and penetration testing.

`Gobuster's` flexibility extends to fuzzing for various types of content:

- `Directories`: Discover hidden directories on a web server.
- `Files`: Identify files with specific extensions (e.g., `.php`, `.txt`, `.bak`).
- `Subdomains`: Enumerate subdomains of a given domain.
- `Virtual Hosts (vhosts)`: Uncover hidden virtual hosts by manipulating the `Host` header.

### Gobuster VHost Fuzzing

While `gobuster` is primarily known for directory and file enumeration, its capabilities extend to virtual host (vhost) discovery, making it a valuable tool in assessing the security posture of a web server.

To follow along, start the target system via the question section at the bottom of the page. Add the specified vhost to your hosts file using the command below, replacing IP with the IP address of your spawned instance. We will be using the `/usr/share/seclists/Discovery/Web-Content/common.txt` wordlists for these fuzzing tasks.

```shell
echo "IP inlanefreight.htb" | sudo tee -a /etc/hosts

```

Let's dissect the `Gobuster` vhost fuzzing command:

```shell
gobuster vhost -u http://inlanefreight.htb:81 -w /usr/share/seclists/Discovery/Web-Content/common.txt --append-domain

```

- `gobuster vhost`: This flag activates `Gobuster's vhost fuzzing mode`, instructing it to focus on discovering virtual hosts rather than directories or files.
- `-u http://inlanefreight.htb:81`: This specifies the base URL of the target server. `Gobuster` will use this URL as the foundation for constructing requests with different vhost names. In this example, the target server is located at `inlanefreight.htb` and listens on port 81.
- `-w /usr/share/seclists/Discovery/Web-Content/common.txt`: This points to the wordlist file that `Gobuster` will use to generate potential vhost names. The `common.txt` wordlist from SecLists contains a collection of commonly used vhost names and subdomains.
- `--append-domain`: This crucial flag instructs `Gobuster` to append the base domain ( `inlanefreight.htb`) to each word in the wordlist. This ensures that the `Host` header in each request includes a complete domain name (e.g., `admin.inlanefreight.htb`), which is essential for vhost discovery.

In essence, `Gobuster` takes each word from the wordlist, appends the base domain to it, and then sends an HTTP request to the target URL with that modified `Host` header. By analyzing the server's responses (e.g., status codes, response size), `Gobuster` can identify valid `vhosts` that might not be publicly advertised or documented.

Running the command will execute a `vhost scan` against the target:

```shell
gobuster vhost -u http://inlanefreight.htb:81 -w /usr/share/seclists/Discovery/Web-Content/common.txt --append-domain

===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:             http://inlanefreight.htb:81
[+] Method:          GET
[+] Threads:         10
[+] Wordlist:        /usr/share/SecLists/Discovery/Web-Content/common.txt
[+] User Agent:      gobuster/3.6
[+] Timeout:         10s
[+] Append Domain:   true
===============================================================
Starting gobuster in VHOST enumeration mode
===============================================================
Found: .git/logs/.inlanefreight.htb:81 Status: 400 [Size: 157]
...
Found: admin.inlanefreight.htb:81 Status: 200 [Size: 100]
Found: android/config.inlanefreight.htb:81 Status: 400 [Size: 157]
...
Progress: 4730 / 4730 (100.00%)
===============================================================
Finished
===============================================================

```

After the scan has been completed, we see a list of the results. Of particular interest are the vhosts with the `200` status code. In HTTP, a 200 status indicates a successful response, suggesting that the vhost is valid and accessible. For instance, the line `Found: admin.inlanefreight.htb:81 Status: 200 [Size: 100]` indicates that the vhost `admin.inlanefreight.htb` was found and responded to successfully.

### Gobuster Subdomain Fuzzing

While often associated with vhost and directory discovery, `Gobuster` also excels at subdomain enumeration, a crucial step in mapping the attack surface of a target domain. By systematically testing variations of potential subdomain names, `Gobuster` can uncover hidden or forgotten subdomains that might host valuable information or vulnerabilities.

Let's break down the `Gobuster` subdomain fuzzing command:

```shell
gobuster dns -d inlanefreight.com -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt

```

- `gobuster dns`: Activates `Gobuster's` DNS fuzzing mode, directing it to focus on discovering subdomains.
- `-d inlanefreight.com`: Specifies the target domain (e.g., `inlanefreight.com`) for which you want to discover subdomains.
- `-w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt`: This points to the wordlist file that `Gobuster` will use to generate potential subdomain names. In this example, we're using a wordlist containing the top 5000 most common subdomains.

Under the hood, `Gobuster` works by generating subdomain names based on the wordlist, appending them to the target domain, and then attempting to resolve those subdomains using DNS queries. If a subdomain resolves to an IP address, it is considered valid and included in the output.

Running this command, `Gobuster` might produce output similar to:

```shell
gobuster dns -d inlanefreight.com -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt

===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Domain:     inlanefreight.com
[+] Threads:    10
[+] Timeout:    1s
[+] Wordlist:   /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt
===============================================================
Starting gobuster in DNS enumeration mode
===============================================================
Found: www.inlanefreight.com

Found: blog.inlanefreight.com

...

Progress: 4989 / 4990 (99.98%)
===============================================================
Finished
===============================================================

```

In the output, each line prefixed with "Found:" indicates a valid subdomain discovered by Gobuster.


# Filtering Fuzzing Output

* * *

Web fuzzing tools like `gobuster`, `ffuf`, and `wfuzz` are designed to perform comprehensive scans, often generating a vast amount of data. Sifting through this output to identify the most relevant findings can be a daunting task. However, these tools offer powerful filtering mechanisms to streamline your analysis and focus on the results that matter most.

### Gobuster

`Gobuster` offers various filtering options depending on the module being run, to help you focus on specific responses and streamline your analysis. There is a small caveat, the `-s` and `-b` options are only available in the `dir` fuzzing mode.

| Flag | Description | Example Scenario |
| --- | --- | --- |
| `-s` (include) | Include only responses with the specified status codes (comma-separated). | You're looking for redirects, so you filter for codes `301,302,307` |
| `-b` (exclude) | Exclude responses with the specified status codes (comma-separated). | The server returns many 404 errors. Exclude them with `-b 404` |
| `--exclude-length` | Exclude responses with specific content lengths (comma-separated, supports ranges). | You're not interested in 0-byte or 404-byte responses, so use `--exclude-length 0,404` |

By strategically combining these filtering options, you can tailor `Gobuster's` output to your specific needs and focus on the most relevant results for your security assessments.

```shell
# Find directories with status codes 200 or 301, but exclude responses with a size of 0 (empty responses)
gobuster dir -u http://example.com/ -w wordlist.txt -s 200,301 --exclude-length 0

```

## FFUF

`FFUF` offers a highly customizable filtering system, enabling precise control over the displayed output. This allows you to efficiently sift through potentially large amounts of data and focus on the most relevant findings. `FFUF's` filtering options are categorized into multiple types, each serving a specific purpose in refining your results.

| Flag | Description | Example Scenario |
| --- | --- | --- |
| `-mc` (match code) | Include only responses that match the specified status codes. You can provide a single code, multiple codes separated by commas, or ranges of codes separated by hyphens (e.g., `200,204,301`, `400-499`). The default behavior is to match codes 200-299, 301, 302, 307, 401, 403, 405, and 500. | After fuzzing, you notice many 302 (Found) redirects, but you're primarily interested in 200 (OK) responses. Use `-mc 200` to isolate these. |
| `-fc` (filter code) | Exclude responses that match the specified status codes, using the same format as `-mc`. This is useful for removing common error codes like 404 Not Found. | A scan returns many 404 errors. Use `-fc 404` to remove them from the output. |
| `-fs` (filter size) | Exclude responses with a specific size or range of sizes. You can specify single sizes or ranges using hyphens (e.g., `-fs 0` for empty responses, `-fs 100-200` for responses between 100 and 200 bytes). | You suspect the interesting responses will be larger than 1KB. Use `-fs 0-1023` to filter out smaller responses. |
| `-ms` (match size) | Include only responses that match a specific size or range of sizes, using the same format as `-fs`. | You are looking for a backup file that you know is exactly 3456 bytes in size. Use `-ms 3456` to find it. |
| `-fw` (filter out number of words in response) | Exclude responses containing the specified number of words in the response. | You're filtering out a specific number of words from the responses. Use `-fw 219` to filter for responses containing that amount of words. |
| `-mw` (match word count) | Include only responses that have the specified amount of words in the response body. | You're looking for short, specific error messages. Use `-mw 5-10` to filter for responses with 5 to 10 words. |
| `-fl` (filter line) | Exclude responses with a specific number of lines or range of lines. For example, `-fl 5` will filter out responses with 5 lines. | You notice a pattern of 10-line error messages. Use `-fl 10` to filter them out. |
| `-ml` (match line count) | Include only responses that have the specified amount of lines in the response body. | You're looking for responses with a specific format, such as 20 lines. Use `-ml 20` to isolate them. |
| `-mt` (match time) | Include only responses that meet a specific time-to-first-byte (TTFB) condition. This is useful for identifying responses that are unusually slow or fast, potentially indicating interesting behavior. | The application responds slowly when processing certain inputs. Use `-mt >500` to find responses with a TTFB greater than 500 milliseconds. |

You can combine multiple filters. For example:

```shell
# Find directories with status code 200, based on the amount of words, and a response size greater than 500 bytes
ffuf -u http://example.com/FUZZ -w wordlist.txt -mc 200 -fw 427 -ms >500

# Filter out responses with status codes 404, 401, and 302
ffuf -u http://example.com/FUZZ -w wordlist.txt -fc 404,401,302

# Find backup files with the .bak extension and size between 10KB and 100KB
ffuf -u http://example.com/FUZZ.bak -w wordlist.txt -fs 0-10239 -ms 10240-102400

# Discover endpoints that take longer than 500ms to respond
ffuf -u http://example.com/FUZZ -w wordlist.txt -mt >500

```

### wenum

`wenum` offers a robust filtering system to help you manage and refine the vast amount of data generated during fuzzing. You can filter based on status codes, response size/character count, word count, line count, and even regular expressions.

| Flag | Description | Example Scenario |
| --- | --- | --- |
| `--hc` (hide code) | Exclude responses that match the specified status codes. | After fuzzing, the server returned many 400 Bad Request errors. Use `--hc 400` to hide them and focus on other responses. |
| `--sc` (show code) | Include only responses that match the specified status codes. | You are only interested in successful requests (200 OK). Use `--sc 200` to filter the results accordingly. |
| `--hl` (hide length) | Exclude responses with the specified content length (in lines). | The server returns verbose error messages with many lines. Use `--hl` with a high value to hide these and focus on shorter responses. |
| `--sl` (show length) | Include only responses with the specified content length (in lines). | You suspect a specific response with a known line count is related to a vulnerability. Use `--sl` to pinpoint it. |
| `--hw` (hide word) | Exclude responses with the specified number of words. | The server includes common phrases in many responses. Use `--hw` to filter out responses with those word counts. |
| `--sw` (show word) | Include only responses with the specified number of words. | You are looking for short error messages. Use `--sw` with a low value to find them. |
| `--hs` (hide size) | Exclude responses with the specified response size (in bytes or characters). | The server sends large files for valid requests. Use `--hs` to filter out these large responses and focus on smaller ones. |
| `--ss` (show size) | Include only responses with the specified response size (in bytes or characters). | You are looking for a specific file size. Use `--ss` to find it. |
| `--hr` (hide regex) | Exclude responses whose body matches the specified regular expression. | Filter out responses containing the "Internal Server Error" message. Use `--hr "Internal Server Error"`. |
| `--sr` (show regex) | Include only responses whose body matches the specified regular expression. | Filter for responses containing the string "admin" using `--sr "admin"`. |
| `--filter`/ `--hard-filter` | General-purpose filter to show/hide responses or prevent their post-processing using a regular expression. | `--filter "Login"` will show only responses containing "Login", while `--hard-filter "Login"` will hide them and prevent any plugins from processing them. |

You can combine multiple filters. For example:

```shell
# Show only successful requests and redirects:
wenum -w wordlist.txt --sc 200,301,302 -u https://example.com/FUZZ

# Hide responses with common error codes:
wenu -w wordlist.txt --hc 404,400,500 -u https://example.com/FUZZ

# Show only short error messages (responses with 5-10 words):
wenum -w wordlist.txt --sw 5-10 -u https://example.com/FUZZ

# Hide large files and focus on smaller responses:
wenum -w wordlist.txt --hs 10000 -u https://example.com/FUZZ

# Filter for responses containing specific information:
wenum -w wordlist.txt --sr "admin\|password" -u https://example.com/FUZZ

```

## Feroxbuster

`Feroxbuster's` filtering system is designed to be both powerful and flexible, enabling you to fine-tune the results you receive during a scan. It offers a variety of filters that operate on both the request and response levels.

| Flag | Description | Example Scenario |
| --- | --- | --- |
| `--dont-scan` (Request) | Exclude specific URLs or patterns from being scanned (even if found in links during recursion). | You know the `/uploads` directory contains only images, so you can exclude it using `--dont-scan /uploads`. |
| `-S`, `--filter-size` | Exclude responses based on their size (in bytes). You can specify single sizes or comma-separated ranges. | You've noticed many 1KB error pages. Use `-S 1024` to exclude them. |
| `-X`, `--filter-regex` | Exclude responses whose body or headers match the specified regular expression. | Filter out pages with a specific error message using `-X "Access Denied"`. |
| `-W`, `--filter-words` | Exclude responses with a specific word count or range of word counts. | Eliminate responses with very few words (e.g., error messages) using `-W 0-10`. |
| `-N`, `--filter-lines` | Exclude responses with a specific line count or range of line counts. | Filter out long, verbose pages with `-N 50-`. |
| `-C`, `--filter-status` | Exclude responses based on specific HTTP status codes. This operates as a denylist. | Suppress common error codes like 404 and 500 using `-C 404,500`. |
| `--filter-similar-to` | Exclude responses that are similar to a given webpage. | Remove duplicate or near-duplicate pages based on a reference page using `--filter-similar-to error.html`. |
| `-s`, `--status-codes` | Include only responses with the specified status codes. This operates as an allowlist (default: all). | Focus on successful responses using `-s 200,204,301,302`. |

You can combine multiple filters. For example:

```shell
# Find directories with status code 200, excluding responses larger than 10KB or containing the word "error"
feroxbuster --url http://example.com -w wordlist.txt -s 200 -S 10240 -X "error"

```

## A Quick Demonstration

To follow along, start the target system via the question section at the bottom of the page. Add the specified vhost to your hosts file using the command below, replacing IP with the IP address of your spawned instance. We will be using the `/usr/share/seclists/Discovery/Web-Content/common.txt` wordlists for these fuzzing tasks.

Throughout the module so far, you might have noticed some of the commands have been using some sort of result filtering, or the fuzzers themselves are applying some sort of filtering. For example, for POST fuzzing with `ffuf`, if we remove the match code filter, `ffuf` will default to a series of other filters.

```shell
ffuf -u http://IP:PORT/post.php -X POST -H "Content-Type: application/x-www-form-urlencoded" -d "y=FUZZ" -w /usr/share/seclists/Discovery/Web-Content/common.txt -v

        /'___\  /'___\           /'___\
       /\ \__/ /\ \__/  __  __  /\ \__/
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/
         \ \_\   \ \_\  \ \____/  \ \_\
          \/_/    \/_/   \/___/    \/_/

       v2.1.0-dev
________________________________________________

 :: Method           : POST
 :: URL              : http://IP:PORT/post.php
 :: Wordlist         : FUZZ: /usr/share/seclists/Discovery/Web-Content/common.txt
 :: Header           : Content-Type: application/x-www-form-urlencoded
 :: Data             : y=FUZZ
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
________________________________________________

```

In the output above, the line `:: Matcher : Response status: 200-299,301,302,307,401,403,405,500` indicates that, by default, `ffuf` matches only those specific status codes. This intentional filtering minimizes the noise generated by `404 NOT FOUND` responses, ensuring that the results of interest remain prominent.

To illustrate the potential issue of not filtering, let's run the same scan while matching all status codes using the `-mc all` flag:

```shell
ffuf -u http://IP:PORT/post.php -X POST -H "Content-Type: application/x-www-form-urlencoded" -d "y=FUZZ" -w /usr/share/seclists/Discovery/Web-Content/common.txt -v -mc all

        /'___\  /'___\           /'___\
       /\ \__/ /\ \__/  __  __  /\ \__/
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/
         \ \_\   \ \_\  \ \____/  \ \_\
          \/_/    \/_/   \/___/    \/_/

       v2.1.0-dev
________________________________________________

 :: Method           : POST
 :: URL              : http://IP:PORT/post.php
 :: Wordlist         : FUZZ: /usr/share/seclists/Discovery/Web-Content/common.txt
 :: Header           : Content-Type: application/x-www-form-urlencoded
 :: Data             : y=FUZZ
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: all
________________________________________________

[Status: 404, Size: 36, Words: 4, Lines: 3, Duration: 1ms]
| URL | http://IP:PORT/post.php
    * FUZZ: .cache

[Status: 404, Size: 43, Words: 4, Lines: 3, Duration: 2ms]
| URL | http://IP:PORT/post.php
    * FUZZ: .bash_history

[Status: 404, Size: 34, Words: 4, Lines: 3, Duration: 2ms]
| URL | http://IP:PORT/post.php
    * FUZZ: .cvs

[Status: 404, Size: 42, Words: 4, Lines: 3, Duration: 2ms]
| URL | http://IP:PORT/post.php
    * FUZZ: .git-rewrite

[Status: 404, Size: 40, Words: 4, Lines: 3, Duration: 2ms]
| URL | http://IP:PORT/post.php
    * FUZZ: .cvsignore

[Status: 404, Size: 39, Words: 4, Lines: 3, Duration: 3ms]
| URL | http://IP:PORT/post.php
    * FUZZ: .git/HEAD
...

```

The resulting output becomes inundated with `404 NOT FOUND` results, making it significantly more challenging to identify any potentially valuable findings. This demonstrates the importance of employing appropriate filtering techniques to optimize the fuzzing process and prioritize meaningful results.


# Validating Findings

* * *

Fuzzing is excellent at casting a wide net and generating potential leads, but not every finding is a genuine vulnerability. The process often yields false positives – harmless anomalies that trigger the fuzzer's detection mechanisms but pose no real threat. This is why validation is a crucial step in the fuzzing workflow.

## Why Validate?

Validating findings serves several important purposes:

- `Confirming Vulnerabilities`: Ensures that the discovered issues are real vulnerabilities and not just false alarms.
- `Understanding Impact`: Helps you assess the severity of the vulnerability and the potential impact on the web application.
- `Reproducing the Issue`: Provides a way to consistently replicate the vulnerability, aiding in developing a fix or mitigation strategy.
- `Gather Evidence`: Collect proof of the vulnerability to share with developers or stakeholders.

## Manual Verification

The most reliable way to validate a potential vulnerability is through manual verification. This typically involves:

1. `Reproducing the Request`: Use a tool like `curl` or your web browser to manually send the same request that triggered the unusual response during fuzzing.
2. `Analyzing the Response`: Carefully examine the response to confirm whether it indicates vulnerability. Look for error messages, unexpected content, or behavior that deviates from the expected norm.
3. `Exploitation`: If the finding seems promising, attempt to exploit the vulnerability in a controlled environment to assess its impact and severity. This step should be performed with caution and only after obtaining proper authorization.

To responsibly validate and exploit a finding, avoiding actions that could harm the production system or compromise sensitive data is crucial. Instead, focus on creating a `proof of concept` ( `PoC`) that demonstrates the existence of the vulnerability without causing damage. For example, if you suspect a SQL injection vulnerability, you could craft a harmless SQL query that returns the SQL server version string rather than trying to extract or modify sensitive data.

The goal is to gather enough evidence to convince stakeholders of the vulnerability's existence and potential impact while adhering to ethical and legal guidelines.

## Example

To follow along, start the target system via the question section at the bottom of the page, replacing the uses of `IP`: `PORT` with the IP:PORT for your spawned instance.

Imagine your fuzzer discovered a directory named `/backup/` on a web server. The response to this directory returned a `200 OK` status code, suggesting that the directory exists and is accessible. While this might seem innocuous at first glance, it's crucial to remember that backup directories often contain sensitive information.

Backup files are designed to preserve data, which means they might include:

- `Database dumps`: These files could contain entire databases, including user credentials, personal information, and other confidential data.
- `Configuration files`: These files might store API keys, encryption keys, or other sensitive settings that attackers could exploit.
- `Source code`: Backup copies of source code could reveal vulnerabilities or implementation details that attackers could leverage.

If an attacker gains access to these files, they could potentially compromise the entire web application, steal sensitive data, or cause significant damage. However, as a security professional, you will need to interact with this finding so that you do not compromise the integrity of the target or open yourself up to any potential blowback while proving the issue exists.

### Using curl for validation

First, we need to confirm if this directory is truly browsable. We can use `curl` to validate if it is or isn't.

```shell
curl http://IP:PORT/backup/

```

Examine the output in your terminal. If the server responds with a list of files and directories contained within the `/backup` directory, you've successfully confirmed the directory listing vulnerability. This could look something like this:

```html
<!DOCTYPE html>
<html>
<head>
<title>Index of /backup/</title>
<style type="text/css">
[...]
</style>
</head>
<body>
<h2>Index of /backup/</h2>
<div class="list">
<table summary="Directory Listing" cellpadding="0" cellspacing="0">
<thead><tr><th class="n">Name</th><th class="m">Last Modified</th><th class="s">Size</th><th class="t">Type</th></tr></thead>
<tbody>
<tr class="d"><td class="n"><a href="../">..</a>/</td><td class="m">&nbsp;</td><td class="s">- &nbsp;</td><td class="t">Directory</td></tr>
<tr><td class="n"><a href="backup.sql">backup.sql</a></td><td class="m">2024-Jun-12 14:00:46</td><td class="s">0.2K</td><td class="t">application/octet-stream</td></tr>
</tbody>
</table>
</div>
<div class="foot">lighttpd/1.4.76</div>

<script type="text/javascript">
[...]
</script>

</body>
</html>

```

To responsibly confirm the vulnerability without risking exposure of sensitive data, the optimal approach is to examine the response headers for clues about the files within the directory. Specifically, the `Content-Type` header often indicates the type of file (e.g., `application/sql` for a database dump, `application/zip` for a compressed backup).

Additionally, scrutinize the `Content-Length` header. A value greater than zero suggests a file with actual content, whereas a zero-length file, while potentially unusual, may not pose a direct vulnerability. For instance, if you see a `dump.sql` file with a `Content-Length` of 0, it's likely empty. Although its presence in the directory might be suspicious, it doesn't automatically indicate a security risk.

Here's an example using `curl` to retrieve only the headers for a file named `password.txt`:

```shell
curl -I http://IP:PORT/backup/password.txt

HTTP/1.1 200 OK
Content-Type: text/plain;charset=utf-8
ETag: "3406387762"
Last-Modified: Wed, 12 Jun 2024 14:08:46 GMT
Content-Length: 171
Accept-Ranges: bytes
Date: Wed, 12 Jun 2024 14:08:59 GMT
Server: lighttpd/1.4.76

```

- `Content-Type: text/plain;charset=utf-8`: This tells us that `password.txt` is a plain text file, which is what is expected.
- `Content-Length: 171`: The file size is 171 bytes. While this doesn't definitively tell us the contents, it suggests that the file isn't empty and likely contains some data. This is concerning, given the file name and the fact that it's in a backup directory.

These header details and the directory listing's existence provide strong evidence of a potential security risk. We've confirmed that the backup directory is accessible and contains a file named `password.txt` with actual content, which is likely sensitive.

By focusing on headers, you can gather valuable information without directly accessing the file's contents, striking a balance between confirming the vulnerability and maintaining responsible disclosure practices.


# Web APIs

* * *

A `Web API`, or `Web Application Programming Interface`, is a set of rules and specifications that enable different software applications to communicate over the web. It functions as a universal language, allowing diverse software components to exchange data and services seamlessly, regardless of their underlying technologies or programming languages.

Essentially, a `Web API` serves as a bridge between a server (hosting the data and functionality) and a client (such as a web browser, mobile app, or another server) that wants to access or utilize that data or functionality. There are various `Web APIs`, each with strengths and use cases.

## Representational State Transfer (REST)

`REST APIs` are a popular architectural style for building web services. They use a stateless, client-server communication model where clients send requests to servers to access or manipulate resources. `REST APIs` utilize standard `HTTP methods` ( `GET`, `POST`, `PUT`, `DELETE`) to perform `CRUD` (Create, Read, Update, Delete) operations on resources identified by unique URLs. They typically exchange data in lightweight formats like `JSON` or `XML`, making them easy to integrate with various applications and platforms.

Example query:

```http
GET /users/123

```

## Simple Object Access Protocol (SOAP)

`SOAP APIs` follow a more formal and standardized protocol for exchanging structured information. They use `XML` to define messages, which are then encapsulated in `SOAP envelopes` and transmitted over network protocols like `HTTP` or `SMTP`. `SOAP APIs` often include built-in security, reliability, and transaction management features, making them suitable for enterprise-level applications requiring strict data integrity and error handling.

Example query:

```xml
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tem="http://tempuri.org/">
   <soapenv:Header/>
   <soapenv:Body>
      <tem:GetStockPrice>
         <tem:StockName>AAPL</tem:StockName>
      </tem:GetStockPrice>
   </soapenv:Body>
</soapenv:Envelope>

```

## GraphQL

`GraphQL` is a relatively new query language and runtime for `APIs`. Unlike `REST APIs`, which expose multiple endpoints for different resources, `GraphQL` provides a single endpoint where clients can request the data they need using a flexible query language. This eliminates the problem of over-fetching or under-fetching data, which is common in `REST APIs`. `GraphQL`'s strong typing and introspection capabilities make it easier to evolve `APIs` over time without breaking existing clients, making it a popular choice for modern web and mobile applications.

Example query:

```graphql
query {
  user(id: 123) {
    name
    email
  }
}

```

## Advantages of Web APIs

`Web APIs` have revolutionized application development and interaction by providing standardized ways for clients to access and manipulate server-stored data. They enable developers to expose specific features or services of their applications to external users or other applications, promoting code reusability and facilitating the creation of mashups and composite applications.

Furthermore, `Web APIs` are instrumental in integrating third-party services, such as social media logins, secure payment processing, or mapping functionalities, into applications. This streamlined integration allows developers to incorporate external capabilities without reinventing the wheel.

`APIs` are also the cornerstone of `microservices architecture`, where large, monolithic applications are broken down into smaller, independent services that communicate through well-defined `APIs`. This architectural approach enhances scalability, flexibility, and resilience, making it ideal for modern web applications.

## How APIs are different from a web server

While both traditional web pages and Web APIs play vital roles in the web ecosystem, they have distinct structure, communication, and functionality characteristics. Understanding these differences is crucial for effective fuzzing.

| Feature | Web Server | API (Application Programming Interface) |
| --- | --- | --- |
| `Purpose` | Primarily designed to serve static content (HTML, CSS, images) and dynamic web pages (generated by server-side scripts). | Primarily designed to provide a way for different software applications to communicate with each other, exchange data, and trigger actions. |
| `Communication` | Communicates with web browsers using the HTTP (Hypertext Transfer Protocol). | Can use various protocols for communication, including HTTP, HTTPS, SOAP, and others, depending on the specific API. |
| `Data Format` | Primarily deals with HTML, CSS, JavaScript, and other web-related formats. | Can exchange data in various formats, including JSON, XML, and others, depending on the API specification. |
| `User Interaction` | Users interact with web servers directly through web browsers to view web pages and content. | Users typically do not interact with APIs directly; instead, applications use APIs to access data or functionality on behalf of the user. |
| `Access` | Web servers are usually publicly accessible over the internet. | APIs can be publicly accessible, private (for internal use only), or partner (accessible to specific partners or clients). |
| `Example` | When you access a website like `https://www.example.com`, you are interacting with a web server that sends you the HTML, CSS, and JavaScript code to render the web page in your browser. | A weather app on your phone might use a weather API to fetch weather data from a remote server. The app then processes this data and displays it to you in a user-friendly format. You are not directly interacting with the API, but the app is using it behind the scenes to provide you with the weather information. |

By understanding these differences, you can tailor your fuzzing approach to the specific characteristics of Web APIs. For example, instead of fuzzing for hidden directories or files, you'll focus on fuzzing API endpoints and their parameters, paying close attention to the data formats used in requests and responses.


# Identifying Endpoints

* * *

You must know where to look before you can start fuzzing Web APIs. Identifying the endpoints that the API exposes is the first crucial step in this process. This involves some detective work, but several methods can help uncover these hidden doorways to the application's data and functionality.

## REST

REST APIs are built around the concept of resources, which are identified by unique URLs called endpoints. These endpoints are the targets for client requests, and they often include parameters to provide additional context or control over the requested operation.

Endpoints in REST APIs are structured as URLs representing the resources you want to access or manipulate. For example:

- `/users` \- Represents a collection of user resources.
- `/users/123` \- Represents a specific user with the ID 123.
- `/products` \- Represents a collection of product resources.
- `/products/456` \- Represents a specific product with the ID 456.

The structure of these endpoints follows a hierarchical pattern, where more specific resources are nested under broader categories.

Parameters are used to modify the behavior of API requests or provide additional information. In REST APIs, there are several types of parameters:

| Parameter Type | Description | Example |
| --- | --- | --- |
| Query Parameters | Appended to the endpoint URL after a question mark ( `?`). Used for filtering, sorting, or pagination. | `/users?limit=10&sort=name` |
| Path Parameters | Embedded directly within the endpoint URL. Used to identify specific resources. | `/products/{id}pen_spark` |
| Request Body Parameters | Sent in the body of POST, PUT, or PATCH requests. Used to create or update resources. | `{ "name": "New Product", "price": 99.99 }` |

### Discovering REST Endpoints and Parameters

Discovering the available endpoints and parameters of a REST API can be accomplished through several methods:

1. `API Documentation`: The most reliable way to understand an API is to refer to its official documentation. This documentation often includes a list of available endpoints, their parameters, expected request/response formats, and example usage. Look for specifications like Swagger (OpenAPI) or RAML, which provide machine-readable API descriptions.
2. `Network Traffic Analysis`: If documentation is not available or incomplete, you can analyze network traffic to observe how the API is used. Tools like Burp Suite or your browser's developer tools allow you to intercept and inspect API requests and responses, revealing endpoints, parameters, and data formats.
3. `Parameter Name Fuzzing`: Similar to fuzzing for directories and files, you can use the same tools and techniques to fuzz for parameter names within API requests. Tools like `ffuf` and `wfuzz`, combined with appropriate wordlists, can be used to discover hidden or undocumented parameters. This can be particularly useful when dealing with APIs that lack comprehensive documentation.

## SOAP

SOAP (Simple Object Access Protocol) APIs are structured differently from REST APIs. They rely on XML-based messages and Web Services Description Language (WSDL) files to define their interfaces and operations.

Unlike REST APIs, which use distinct URLs for each resource, SOAP APIs typically expose a single endpoint. This endpoint is a URL where the SOAP server listens for incoming requests. The content of the SOAP message itself determines the specific operation you want to perform.

SOAP parameters are defined within the body of the SOAP message, an XML document. These parameters are organized into elements and attributes, forming a hierarchical structure. The specific structure of the parameters depends on the operation being invoked. The parameters are defined in the `Web Services Description Language` ( `WSDL`) file, an `XML-based document` that describes the web service's interface, operations, and message formats.

Imagine a SOAP API for a library that offers a book search service. The WSDL file might define an operation called `SearchBooks` with the following input parameters:

- `keywords` (string): The search terms to use.
- `author` (string): The name of the author (optional).
- `genre` (string): The genre of the book (optional).

A sample SOAP request to this API might look like this:

```xml
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:lib="http://example.com/library">
   <soapenv:Header/>
   <soapenv:Body>
      <lib:SearchBooks>
         <lib:keywords>cybersecurity</lib:keywords>
         <lib:author>Dan Kaminsky</lib:author>
      </lib:SearchBooks>
   </soapenv:Body>
</soapenv:Envelope>

```

In this request:

- The `keywords` parameter is set to "cybersecurity" to search for books on that topic.
- The `author` parameter is set to "Dan Kaminsky" to further refine the search.
- The `genre` parameter is not included, meaning the search will not be filtered by genre.

The SOAP response would likely contain a list of books matching the search criteria, formatted according to the WSDL definition.

### Discovering SOAP Endpoints and Parameters

To identify the available endpoints (operations) and parameters for a SOAP API, you can utilize the following methods:

1. `WSDL Analysis`: The WSDL file is the most valuable resource for understanding a SOAP API. It describes:


   - Available operations (endpoints)
   - Input parameters for each operation (message types, elements, and attributes)
   - Output parameters for each operation (response message types)
   - Data types used for parameters (e.g., strings, integers, complex types)
   - The location (URL) of the SOAP endpoint

You can analyze the WSDL file manually or use tools designed to parse and visualize WSDL structures.

2. `Network Traffic Analysis`: Similar to REST APIs, you can intercept and analyze SOAP traffic to observe the requests and responses between clients and the server. Tools like Wireshark or tcpdump can capture SOAP traffic, allowing you to examine the structure of SOAP messages and extract information about endpoints and parameters.

3. `Fuzzing for Parameter Names and Values`: While SOAP APIs typically have a well-defined structure, fuzzing can still be helpful in uncovering hidden or undocumented operations or parameters. You can use fuzzing tools to send malformed or unexpected values within SOAP requests and see how the server responds.


## Identifying GraphQL API Endpoints and Parameters

GraphQL APIs are designed to be more flexible and efficient than REST and SOAP APIs, allowing clients to request precisely the data they need in a single request.

Unlike REST or SOAP APIs, which often expose multiple endpoints for different resources, GraphQL APIs typically have a single endpoint. This endpoint is usually a URL like `/graphql` and serves as the entry point for all queries and mutations sent to the API.

GraphQL uses a unique query language to specify the data requirements. Within this language, queries and mutations act as the vehicles for defining parameters and structuring the requested data.

### GraphQL Queries

Queries are designed to fetch data from the GraphQL server. They pinpoint the exact fields, relationships, and nested objects the client desires, eliminating the issue of over-fetching or under-fetching data common in REST APIs. Arguments within queries allow for further refinement, such as filtering or pagination.

| Component | Description | Example |
| --- | --- | --- |
| Field | Represents a specific piece of data you want to retrieve (e.g., name, email). | `name`, `email` |
| Relationship | Indicates a connection between different types of data (e.g., a user's posts). | `posts` |
| Nested Object | A field that returns another object, allowing you to traverse deeper into the data graph. | `posts { title, body }` |
| Argument | Modifies the behavior of a query or field (e.g., filtering, sorting, pagination). | `posts(limit: 5)` (retrieves the first 5 posts of a user) |

```graphql
query {
  user(id: 123) {
    name
    email
    posts(limit: 5) {
      title
      body
    }
  }
}

```

In this example:

- We query for information about a `user` with the ID 123.
- We request their `name` and `email`.
- We also fetch their first 5 `posts`, including the `title` and `body` of each post.

### GraphQL Mutations

Mutations are the counterparts to queries designed to modify data on the server. They encompass operations to create, update, or delete data. Like queries, mutations can also accept arguments to define the input values for these operations.

| Component | Description | Example |
| --- | --- | --- |
| Operation | The action to perform (e.g., createPost, updateUser, deleteComment). | `createPost` |
| Argument | Input data required for the operation (e.g., title and body for a new post). | `title: "New Post", body: "This is the content of the new post"` |
| Selection | Fields you want to retrieve in the response after the mutation completes (e.g., id, title of new post). | `id`, `title` |

```graphql
mutation {
  createPost(title: "New Post", body: "This is the content of the new post") {
    id
    title
  }
}

```

This mutation creates a new post with the specified title and body, returning the `id` and `title` of the newly created post in the response.

### Discovering Queries and Mutations

There are a few ways to discover GraphQL Queries and Mutations:

1. `Introspection`: GraphQL's introspection system is a powerful tool for discovery. By sending an introspection query to the GraphQL endpoint, you can retrieve a complete schema describing the API's capabilities. This includes available types, fields, queries, mutations, and arguments. Tools and IDEs can leverage this information to offer auto-completion, validation, and documentation for your GraphQL queries.
2. `API Documentation`: Well-documented GraphQL APIs provide comprehensive guides and references alongside introspection. These typically explain the purpose and usage of different queries and mutations, offer examples of valid structures, and detail input arguments and response formats. Tools like GraphiQL or GraphQL Playground, often bundled with GraphQL servers, provide an interactive environment for exploring the schema and experimenting with queries.
3. `Network Traffic Analysis`: Like REST and SOAP, analyzing network traffic can yield insights into GraphQL API structure and usage. By capturing and inspecting requests and responses sent to the graphql endpoint, you can observe real-world queries and mutations. This helps you understand the expected format of requests and the types of data returned, aiding in tailored fuzzing efforts.

Remember, GraphQL is designed for flexibility, so there might not be a rigid set of queries and mutations. Focus on understanding the underlying schema and how clients can construct valid requests to retrieve or modify data.


# API Fuzzing

* * *

API fuzzing is a specialized form of fuzzing tailored for web APIs. While the core principles of fuzzing remain the same – sending unexpected or invalid inputs to a target – API fuzzing focuses on the unique structure and protocols used by web APIs.

API fuzzing involves bombarding an API with a series of automated tests, where each test sends a slightly modified request to an API endpoint. These modifications might include:

- Altering parameter values
- Modifying request headers
- Changing the order of parameters
- Introducing unexpected data types or formats

The goal is to trigger API errors, crashes, or unexpected behavior, revealing potential vulnerabilities like input validation flaws, injection attacks, or authentication issues.

## Why Fuzz APIs?

API fuzzing is crucial for several reasons:

- `Uncovering Hidden Vulnerabilities`: APIs often have hidden or undocumented endpoints and parameters that can be susceptible to attacks. Fuzzing helps uncover these hidden attack surfaces.
- `Testing Robustness`: Fuzzing assesses the API's ability to gracefully handle unexpected or malformed input, ensuring it doesn't crash or expose sensitive data.
- `Automating Security Testing`: Manual testing of all possible input combinations is infeasible. Fuzzing automates this process, saving time and effort.
- `Simulating Real-World Attacks`: Fuzzing can mimic the actions of malicious actors, allowing you to identify vulnerabilities before attackers exploit them.

## Types of API Fuzzing

There are 3 primary types of API fuzzing

1. `Parameter Fuzzing` \- One of the primary techniques in API fuzzing, parameter fuzzing focuses on systematically testing different values for API parameters. This includes query parameters (appended to the API endpoint URL), headers (containing metadata about the request), and request bodies (carrying the data payload). By injecting unexpected or invalid values into these parameters, fuzzers can expose vulnerabilities like injection attacks (e.g., SQL injection, command injection), cross-site scripting (XSS), and parameter tampering.
2. `Data Format Fuzzing` \- Web APIs frequently exchange data in structured formats like JSON or XML. Data format fuzzing specifically targets these formats by manipulating the structure, content, or encoding of the data. This can reveal vulnerabilities related to parsing errors, buffer overflows, or improper handling of special characters.
3. `Sequence Fuzzing` \- APIs often involve multiple interconnected endpoints, where the order and timing of requests are crucial. Sequence fuzzing examines how an API responds to sequences of requests, uncovering vulnerabilities like race conditions, insecure direct object references (IDOR), or authorization bypasses. By manipulating the order, timing, or parameters of API calls, fuzzers can expose weaknesses in the API's logic and state management.

## Exploring the API

**To follow along, start the target system via the question section at the bottom of the page, replacing the uses of IP:PORT with the IP:PORT for your spawned instance.**

This API provides automatically generated documentation via the `/docs` endpoint, `http://IP:PORT/docs`. The following page outlines the API's documented endpoint.

![FastAPI interface showing endpoints: GET /, GET /items/{item_id}, DELETE /items/{item_id}, PUT /items/{item_id}, POST /items/.](https://academy.hackthebox.com/storage/modules/280/apispec.png)

The specification details five endpoints, each with a specific purpose and method:

1. `GET /` (Read Root): This fetches the root resource. It likely returns a basic welcome message or API information.
2. `GET /items/{item_id}` (Read Item): Retrieves a specific item identified by `item_id`.
3. `DELETE /items/{item_id}` (Delete Item): Deletes an item identified by `item_id`.
4. `PUT /items/{item_id}` (Update Item): Updates an existing item with the provided data.
5. `POST /items/` (Create Or Update Item): This function creates a new item or updates an existing one if the `item_id` matches.

While the Swagger specification explicitly details five endpoints, it's crucial to acknowledge that APIs can contain undocumented or "hidden" endpoints that are intentionally omitted from the public documentation.

These hidden endpoints might exist to serve internal functions not meant for external use, as a misguided attempt at security through obscurity, or because they are still under development and not yet ready for public consumption.

## Fuzzing the API

We will use a fuzzer that will use a wordlist in an attempt to discover these undocumented endpoints. Run the commands to pull, install the requirements, and run the fuzzer:

```shell
git clone https://github.com/PandaSt0rm/webfuzz_api.git
cd webfuzz_api
pip3 install -r requirements.txt

```

Then, run the fuzzer using the spawned target IP and PORT

```shell
python3 api_fuzzer.py http://IP:PORT

[-] Invalid endpoint: http://localhost:8000/~webmaster (Status code: 404)
[-] Invalid endpoint: http://localhost:8000/~www (Status code: 404)

Fuzzing completed.
Total requests: 4730
Failed requests: 0
Retries: 0
Status code counts:
404: 4727
200: 2
405: 1
Found valid endpoints:
- http://localhost:8000/cz...
- http://localhost:8000/docs
Unusual status codes:
405: http://localhost:8000/items

```

- The fuzzer identifies numerous invalid endpoints (returning `404 Not Found` errors).
- Two valid endpoints are discovered:
  - `/cz...`: This is an undocumented endpoint as it doesn't appear in the API documentation.
  - `/docs`: This is the documented Swagger UI endpoint.
- The `405 Method Not Allowed` response for `/items` suggests that an incorrect HTTP method was used to access this endpoint (e.g., trying a `GET` request instead of a `POST`).

We can explore the undocumented endpoint via curl and it will return a flag:

```shell
curl http://localhost:8000/cz...

{"flag":"<snip>"}

```

In addition to discovering endpoints, fuzzing can be applied to the parameters these endpoints accept. By systematically injecting unexpected values into parameters, you can trigger errors, crashes, or unexpected behavior that could expose a wide range of vulnerabilities. For example, consider the following scenarios:

- `Broken Object-Level Authorization`: Fuzzing could reveal instances where manipulating parameter values can allow unauthorized access to specific objects or resources.
- `Broken Function Level Authorization`: Fuzzing might uncover cases where unauthorized function calls can be made by manipulating parameters, allowing attackers to perform actions they cannot.
- `Server-Side Request Forgery (SSRF)`: Injections of malicious values into parameters could trick the server into making unintended requests to internal or external resources, potentially exposing sensitive information or facilitating further attacks.

To explore these and other web API vulnerabilities and attacks in more detail, [refer to the API Attacks module](https://academy.hackthebox.com/module/details/268). Understanding these risks is crucial for building secure and resilient APIs.


# Skills Assessment

* * *

To complete this Skills Assessment, you will need to apply the multitude of tools and techniques showcased throughout this module. All fuzzing can be completed using the `common.txt` SecLists Wordlist, found at `/usr/share/seclists/Discovery/Web-Content` on Pwnbox, or via the SecLists GitHub.


