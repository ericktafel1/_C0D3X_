# Fuzzing

* * *

`Fuzzing`, or `fuzz testing`, is an automated software testing technique that provides `invalid`, `unexpected`, or `random data as input` to a computer program. The primary objective of fuzzing is to discover coding errors and security loopholes within software. By identifying these vulnerabilities, developers can enhance the security and stability of their programs before malicious entities exploit them.

The core process of fuzzing involves three primary steps:

1. `Input Generation`: Fuzzing begins with the generation of test data (fuzz). Depending on the fuzzing strategy, this data can range from entirely random bytes to structured inputs that partially adhere to the expected format. The key is that the input is varied and can include values developers might not have considered during the software's design phase.
2. `Test Execution`: The generated inputs are then fed into the target software system, and the system's behaviour is monitored. This step is automated and can involve thousands to millions of test cases. The execution environment is often isolated or sandboxed to prevent any potential negative impacts from the testing process.
3. `Result Analysis`: After the test execution, the outcomes are analysed to identify abnormal behaviour, such as crashes, unhandled exceptions, or memory leaks. These anomalies may indicate potential vulnerabilities or defects. Tools used for fuzzing typically log detailed information about the test cases that led to these failures, aiding developers in debugging the issues.

## History and Evolution of Fuzzing

The inception of fuzzing can be traced back to 1989, under the visionary guidance of Professor Barton Miller at the University of Wisconsin–Madison. Often heralded as the "father of fuzzing," Miller's pioneering experiment aimed to assess the robustness of UNIX applications by feeding them a stream of random data. This method tested the applications' resilience against unexpected or malformed inputs. The results were eye-opening, revealing that a considerable fraction of the tested software failed to handle these inputs gracefully, resulting in crashes and various forms of undefined behaviour. This seminal work coined the term “ `fuzz testing`” and established fuzzing as a critical methodology in software testing.

In the years following Miller's initial exploration, fuzzing began to evolve. Initially, fuzzing tools relied heavily on random input generation, a method that, while effective at finding fundamental issues, suffered from inefficiency and a lack of sophistication. This era of `dumb fuzzers` or `black-box fuzzers` laid the groundwork for further innovation.

### Black Box Fuzzing

![](https://academy.hackthebox.com/storage/modules/258/BBF.png)

The mid-1990s marked a significant evolution with the introduction of mutation-based fuzzing by a research project at the University of California, Berkeley. This approach, which involved mutating existing valid inputs to create a more diverse set of test cases, signalled a shift towards more targeted testing strategies. Furthermore, the late 1990s and early 2000s saw the development of influential tools like `Spike` and `Peach Fuzzer`, which introduced structured approaches to fuzzing, focusing on network protocols and allowing for the definition of specific data formats for more precise testing.

`Mutation-based fuzzers` operate by altering existing data sets to create new test inputs. This process involves taking valid inputs—often sourced from sample files, captured network traffic, or user inputs—and applying a series of mutations to generate potentially malformed outputs. These mutations can range from flipping bits and inserting random bytes to deleting or shuffling data sections.

The key advantage of mutation-based fuzzing lies in its simplicity and minimal requirements for upfront knowledge. Since it starts with valid inputs, this approach can quickly generate a wide variety of test cases, making it highly effective for exploring the robustness of software against unexpected or corrupted inputs. However, the effectiveness of mutation-based fuzzers can be somewhat limited by their lack of awareness regarding the application's expected input structure, potentially leading to a lower hit rate of meaningful vulnerabilities.

In contrast, `generation-based fuzzers` generate test inputs from scratch based on predefined models or specifications that describe the target software's format, protocol, or API. This approach requires a more in-depth initial setup, including the creation or availability of a comprehensive model that details valid input structures— `generation-based fuzzers` craft inputs designed to traverse specific paths within the software or target known vulnerability areas.

The strength of generation-based fuzzing lies in its ability to produce highly structured and relevant test cases that can probe deeper into the software's logic and potential security flaws. This method is particularly effective for complex applications with well-defined input formats or protocols, such as network services, file parsers, and web APIs. However, the requirement for detailed models and the increased setup time can be viewed as drawbacks, particularly in agile testing environments or when such specifications are not readily available.

### White Box Fuzzing

![](https://academy.hackthebox.com/storage/modules/258/WBF.png)

One of the most transformative advancements in fuzzing came with the development of `smart fuzzers` or `white-box fuzzers`. These tools leverage knowledge about a program's input structure, internal workings, and even the programming language to generate intelligent, targeted inputs. Techniques such as symbolic execution and genetic algorithms have significantly enhanced fuzzing's effectiveness, moving beyond simple trial-and-error to a more nuanced exploration of software vulnerabilities.

`Symbolic execution` is a foundational technique used in white-box fuzzing, where the program is executed with symbolic inputs instead of concrete values. This approach allows the fuzzer to analytically explore the program's execution paths, mapping out how inputs relate to paths and identifying conditions under which certain paths are executed.

By systematically solving the constraints that lead to different parts of the code, symbolic execution helps generate inputs that cover a wide range of execution paths, including those that could lead to vulnerabilities.

### Grey Box Fuzzing

![](https://academy.hackthebox.com/storage/modules/258/GBF.png)

`Grey-box fuzzing` occupies a unique position in the spectrum of software testing techniques, bridging the gap between the comprehensive insight of white-box fuzzing and the external perspective of black-box fuzzing. Unlike white-box methods, which require detailed knowledge of a program's internal workings, or black-box approaches that operate without insight, grey-box fuzzing utilises partial knowledge about the software's internals.

This typically includes information about code execution paths but does not necessitate full access to the source code. Grey-box fuzzing's strength lies in its ability to efficiently uncover vulnerabilities by intelligently navigating the software's structure with limited information, making it a highly effective and practical choice for many security testing scenarios.

`Coverage-guided fuzzing` exemplifies this balanced approach. Tools like `AFL`( `American Fuzzy Lop`) and `libFuzzer` have revolutionised the field by monitoring software execution to pinpoint which parts of the code are activated by test inputs. This method enhances the testing process by directing efforts towards unexplored areas of the code, significantly increasing the likelihood of discovering latent vulnerabilities. Through its focus on maximising code coverage, coverage-guided fuzzing demonstrates remarkable efficacy in exposing complex bugs, affirming its value across diverse software testing landscapes.

### Web Fuzzing

Fuzzing has progressed technologically and conceptually, with its adoption expanding into web applications and beyond. Tools like `WebScarab` and `Burp Suite` have adapted fuzzing to the needs of web security, testing the vulnerabilities of web browsers and servers.

Moreover, the 2010s brought a significant breakthrough by introducing cloud-based fuzzing platforms, offering on-demand access to powerful tools and infrastructure, and democratising fuzzing for a broader audience.

### The future of fuzzing

Looking to the future, integrating artificial intelligence and machine learning into fuzzing promises to revolutionise the field further. Researchers are exploring ways to use AI to generate more intelligent test cases, identify vulnerabilities more efficiently, and even automate the bug-fixing process, pointing to a future where fuzzing becomes an even more integral part of software development and security testing.


# Pwnbox Setup

* * *

`Follow these instructions if you plan to utilise the Pwnbox for this module.`

If you prefer to use your machine or setup, skip this guide and refer to the tool-specific setup instructions in the relevant sections of the module.

Of course, you can use the container setup provided on your own machine, but you only **need to follow** these instructions specifically if you plan to use Pwnbox.

First, update docker:

```bash
sudo apt-get update && sudo apt-get install -y docker-ce docker-ce-cli containerd.io

```

Next, start the docker daemon. In Pwnbox, run this command in the shell:

```bash
sudo systemctl start docker

```

Now, [download the Dockerfile from here, save it somewhere and extract the zip](https://academy.hackthebox.com/storage/modules/258/libMDP.zip); the Pwnbox desktop works fine. Extract and create a folder you want to mount to the image. If you let docker create the folder for you it will be created with `sudo` permissions, so you will need to update the permissions manually using `chown`.

```bash
cd ~/Desktop
wget https://academy.hackthebox.com/storage/modules/258/Dockerfile.zip
unzip Dockerfile.zip
mkdir htbfuzz

```

Then run the following command in the same directory where the `Dockerfile` is located to build the container image:

```shell
sudo docker build --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g) -t htbfuzz .

[+] Building 194.2s (18/18) FINISHED                             docker:default
 => [internal] load build definition from Dockerfile                       0.0s
 => => transferring dockerfile: 4.20kB                                     0.0s
 => [internal] load metadata for docker.io/library/ubuntu:22.04            0.6s
 => [internal] load .dockerignore                                          0.0s
 => => transferring context: 2B                                            0.0s
 => CACHED [ 1/14] FROM docker.io/library/ubuntu:22.04@sha256:1b8d8ff4777  0.0s
 => [ 2/14] RUN apt-get update && apt-get full-upgrade -y &&     apt-get   8.5s
 => [ 3/14] RUN echo "deb [signed-by=/etc/apt/keyrings/llvm-snapshot.gpg.  0.4s
 => [ 4/14] RUN apt-get update &&     apt-get -y install --no-install-re  66.5s
 => [ 5/14] RUN update-alternatives --install /usr/bin/gcc gcc /usr/bin/g  0.2s
 => [ 6/14] RUN wget -qO- https://sh.rustup.rs | CARGO_HOME=/etc/cargo s  10.5s
 => [ 7/14] RUN apt clean -y                                               0.2s
 => [ 8/14] RUN git clone --depth=1 https://github.com/vanhauser-thc/afl-  0.8s
 => [ 9/14] WORKDIR /opt/                                                  0.0s
 => [10/14] RUN git clone https://github.com/AFLplusplus/AFLplusplus.git   2.8s
 => [11/14] RUN git clone https://gitlab.com/akihe/radamsa.git             1.4s
 => [12/14] RUN cd /opt/radamsa && make clean && make && make install     12.5s
 => [13/14] RUN cd /opt/AFLplusplus && make clean &&     if [ 1 -eq 1 ];  82.1s
 => [14/14] RUN afl-system-config &&     echo "set encoding=utf-8" > /roo  1.3s
 => exporting to image                                                     6.3s
 => => exporting layers                                                    6.3s
 => => writing image sha256:fed402e2a28660df09b467fdfa10846b556a631eddbcb  0.0s
 => => naming to docker.io/library/htbfuzz


```

This will build the image; it will take around 4 minutes to build the docker image on Pwnbox.

Finally, run the image and mount a `htbfuzz` directory on the Pwnbox desktop to `/data` in the Docker container. You can use this directory as a working directory to move files into and out of the Docker container as needed. We will also run the container with host networking, meaning you don’t need to worry about exposing ports. Networking will be shared between Docker and Pwnbox. This also means, for example, that you can run a server in one container and then start another container to send data to that server.

```shell
sudo docker run -it --network host -v ~/Desktop/htbfuzz:/data htbfuzz

[HTBFuzz e0d97e549b4a] /opt #

```

As mentioned, if you are having permission issues with the `htbfuzz` directory, change the permissions of the folder:

```bash
sudo chown -R $(id -u):$(id -g) ~/Desktop/htbfuzz

```


# Why Fuzz

* * *

While traditional testing approaches like `unit testing`, `integration testing`, and `code reviews` are essential for software quality, they often operate within expected parameters. This means they can effectively check that code functions as intended but may struggle to uncover unexpected behaviours that could introduce security flaws.

`Fuzzing` shines here. By injecting intentionally malformed or random data into a program's inputs, a fuzzer pushes the software into unanticipated states. These unexpected inputs can `trigger crashes`, `memory leaks`, `buffer overflows`, or `other anomalies` that might indicate `hidden vulnerabilities`. Fuzzing effectively explores the `vast space of potential inputs`, revealing potential security weaknesses that might have remained hidden from traditional testing approaches.

## The Inherent Limitations of Manual Testing

Manual testing is inherently limited by human subjectivity and scalability. Testers may miss edge cases due to biases in how the software should work. The vastness of potential inputs in complex systems makes comprehensive manual testing impractical. Additionally, manual testing is prone to human error and struggles to scale effectively with increasing software complexity.

## Uncovering Hidden Bugs and Expanding Test Coverage

Fuzzing excels at finding the proverbial "needle in the haystack"—those elusive edge cases and zero-day vulnerabilities that lurk in complex software. By systematically generating vast quantities of test cases, including invalid, unexpected, or malformed data, fuzzing dramatically increases the coverage of your testing efforts. This expanded coverage translates directly into a higher probability of discovering hidden flaws that traditional testing methodologies, limited by human preconceptions and scope, might miss.

## The Limitations of Fuzzing

While fuzzing is a potent tool for security testing, it's crucial to acknowledge its limitations to use it effectively.

### Speed and Efficiency

Fuzzing can be a resource-intensive process, especially when dealing with complex software. Generating vast test cases can quickly strain computational resources, and analysing the results to identify legitimate vulnerabilities can be time-consuming. This is particularly true for large applications where the input space is enormous.

Diminishing returns can also hamper the effectiveness of fuzzing - as the fuzzing process continues, the likelihood of discovering new and critical vulnerabilities diminishes while the time and resources required to analyse the generated test cases continue to grow. To optimise efficiency, it's crucial to employ targeted fuzzing techniques that focus on specific areas of the codebase most likely to harbour vulnerabilities.

### False Positives

Fuzzers are designed to stress the boundaries of a program's input handling, which can trigger crashes or anomalies that don't necessarily translate to exploitable security vulnerabilities. This can lead to many false positives, requiring skilled personnel to sift through the results and determine the validity and exploitability of each reported issue.

Manually analysing these false positives can be tedious and time-consuming, diverting resources from investigating genuine vulnerabilities. Mitigating false positives can involve prioritising crashes that occur more frequently or focus on crashes that exhibit specific characteristics indicative of security vulnerabilities.

### Code Coverage Limitations

Fuzzing significantly expands test coverage but may not guarantee that it will reach every single code path within complex software. Some vulnerabilities might only manifest under specific conditions that even advanced fuzzing techniques struggle to replicate.


# A Simple Demonstration

* * *

When conducting `fuzz testing`, or " `fuzzing`," we often start with the source code of the target application, as this allows for an in-depth understanding of the program's structure, logic, and potential vulnerabilities. However, it's important to note that having direct access to the source code isn't always possible.

In real-world scenarios, especially when dealing with proprietary or third-party software, we might only have access to the compiled binary. This restricts our ability to see the program’s “inner workings” directly, compelling us to infer its behaviour based on its output in response to our inputs.

To start with, here is our simple program:

```c
#include <stdio.h>
#include <string.h>

void vulnerable_function(char *input) {
    char buffer[100];
    strcpy(buffer, input);
    printf("Received input: %s\n", buffer);
}

int main() {
    char input[256];
    printf("Enter some text: ");
    fgets(input, 256, stdin);
    vulnerable_function(input);
    return 0;
}

```

Create a new folder to work in, and paste the code into `simple.c`.

Let's look closer at our example program, designed to illustrate a common security flaw - a buffer overflow:

- `Headers`: The program begins by including two header files: `stdio.h` for standard input and output functions, and `string.h` for string manipulation capabilities, which will be used to copy the input.

- `Vulnerable Function`: The `vulnerable_function` takes a user input string and attempts to store it in a fixed-size buffer. This buffer is declared to have a capacity of 100 characters. However, a critical issue arises when using `strcpy` to copy the input into this buffer. The `strcpy` function does not check the input’s length against the buffer’s size, leading to a buffer overflow if the input exceeds the buffer's capacity.

`Buffer overflows` are among the oldest and most exploited vulnerabilities in software. They occur when data exceeds a buffer's storage capacity, leading to adjacent memory space overwrites. This can cause various issues, from program crashes to the potential execution of malicious code.

- `Main Function`: The program's entry point prompts the user for input using `fgets`. It reads up to 255 characters from the standard input, preserving room for the null terminator. The input is then passed to the `vulnerable_function`.


## The Fuzzer

To detect this vulnerability, we'll build a very simple Python-based fuzzer.

First, we need to import a few essential Python libraries that will help us execute external commands, generate random data, and interact with the system environment:

```python
import subprocess
import random
import string
import sys

```

- `subprocess` allows us to run external processes and interact with their input/output streams. This is crucial for executing the binary we want to test.
- `random` and `string` are used together to generate random sequences of characters. These characters will form the basis of the inputs we use to fuzz the binary.
- `sys` is employed to handle command-line arguments, enabling our script to accept the path to the target binary as an input parameter.

The core of our fuzzing process involves creating random strings, which serve as inputs for the binary we are testing.

```python
def random_string(length):
    characters = string.ascii_letters + string.digits + string.punctuation
    return "".join(random.choice(characters) for i in range(length))

```

This function takes a single parameter, `length`, which specifies the length of the string to generate. It constructs a string from a pool that includes ASCII letters (both uppercase and lowercase), digits, and punctuation marks. The `random.choice()` function is used to select characters at random from this pool, building a string of the specified length.

With our ability to generate random input strings set up, we move on to defining the main fuzzing logic in the `fuzz` function:

```python
def fuzz(target_binary, max_length=150):
    crash_inputs = []

    for length in range(1, max_length + 1):
        input_string = random_string(length)
        print(f"Testing with input length: {length}")
        try:
            result = subprocess.run(
                [target_binary],
                input=input_string.encode(),
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=5
            )
        except subprocess.CalledProcessError as e:
            print(f"Input length {length} causing crash (exit code {e.returncode})\n")
            crash_inputs.append((length, input_string, e.returncode))
        except subprocess.TimeoutExpired:
            print(f"Timeout expired for input length: {length}, potentially causing a hang. Logging input.")
            crash_inputs.append((length, input_string, "Timeout"))

```

This function takes two parameters:

- `target_binary`: The path to the binary file we intend to test.
- `max_length`: The maximum length of the input strings to test, defaulting to 150 characters.

The code flows across 4 main points:

1. `Initialization`: The function starts by initializing an empty list named `crash_inputs`. This list will store information about any inputs that cause the binary to crash or behave unexpectedly.

2. `Input Generation and Testing`:
   - The function uses a `for` loop to iterate through integer values ranging from 1 to `max_length`. For each iteration, the loop represents a new test case with a unique input string length.
   - Inside the loop, the `random_string` function is called with the current length to generate a random string. This string comprises ASCII letters, digits, and punctuation, providing a diverse set of characters to trigger potential vulnerabilities in the binary.
3. `Executing the Binary with Fuzzed Input`:
   - The generated string is encoded to bytes using `input_string.encode()` since the `subprocess.run` function requires input data in byte form.
   - `subprocess.run` is then called with the target binary and the fuzzed input. This function attempts to execute the binary as a subprocess. Several key arguments are used:
     - `check=True` tells the function to raise a `CalledProcessError` if the subprocess exits with a non-zero status (an indication of an error or crash).
     - `stdout=subprocess.PIPE` and `stderr=subprocess.PIPE` capture the output from standard output and standard error, respectively. This data can be useful for debugging and understanding how the binary reacts to the input.
     - `timeout=5` sets a maximum allowed execution time of 5 seconds for each subprocess. If the execution time exceeds this limit, a `TimeoutExpired` exception is raised, indicating a potential hang.
4. `Exception Handling`:
   - The `try-except` blocks are used to catch and handle exceptions that may occur during the subprocess execution:

     - `CalledProcessError`: If this exception is caught, it indicates that the binary crashed when processing the input. The input length, the input itself, and the exit code are logged in the `crash_inputs` list.
     - `TimeoutExpired`: This exception indicates that the binary did not finish executing within the allowed time, suggesting a hang. The input length and the input are also logged.

Any inputs that cause the binary to crash are important, as they potentially point to vulnerabilities. These are collected and should be logged or reported for further investigation:

```python
if crash_inputs:
    with open("crash_inputs.log", "w") as log_file:
        for length, input_data, code in crash_inputs:
            log_file.write(f"Input length {length} causing crash (exit code {code}): {input_data}\n")
    print("Crashes logged to crash_inputs.log")
else:
    print("No crashes detected.")

```

Finally, to make our script executable as a standalone tool, we add:

```python
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python fuzz.py <target_binary>")
    else:
        target_binary = sys.argv[1]
        fuzz(target_binary)

```

This part of the script checks for proper command-line usage and initiates the fuzzing process if the correct parameters are provided.

### The final form

Putting the entire script together, our fuzzer looks like this:

```python
import subprocess
import random
import string
import sys

def random_string(length):
    characters = string.ascii_letters + string.digits + string.punctuation
    return "".join(random.choice(characters) for i in range(length))

def fuzz(target_binary, max_length=150):
    crash_inputs = []

    for length in range(1, max_length + 1):
        input_string = random_string(length)
        print(f"Testing with input length: {length}")
        try:
            result = subprocess.run(
                [target_binary],
                input=input_string.encode(),
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=5,
            )
        except subprocess.CalledProcessError as e:
            print(f"Input length {length} causing crash (exit code {e.returncode})\n")
            crash_inputs.append((length, input_string, e.returncode))
        except subprocess.TimeoutExpired:
            print(
                f"Timeout expired for input length: {length}, potentially causing a hang. Logging input."
            )
            crash_inputs.append((length, input_string, "Timeout"))

    if crash_inputs:
        with open("crash_inputs.log", "w") as log_file:
            for length, input_data, code in crash_inputs:
                log_file.write(
                    f"Input length {length} causing crash (exit code {code}): {input_data}\n"
                )
        print("Crashes logged to crash_inputs.log")
    else:
        print("No crashes detected.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python fuzz.py <target_binary>")
    else:
        target_binary = sys.argv[1]
        fuzz(target_binary)

```

Copy this script into `fuzz.py` in the same directory as `simple.c`. In the next section, we will go through compiling the code and running the fuzzer.


# Fuzzing in Action

* * *

To begin fuzzing, compile the C program from the previous section and name the output `simple`.

You can use the command below to compile the program.

```bash
gcc -g -fno-stack-protector -z execstack simple.c -o simple

```

Then, run the Python fuzzer script in the same directory.

```bash
python fuzz.py ./simple

```

## Observing Vulnerabilities

As the fuzzer runs, it will generate messages indicating the length of the input string being tested. When it encounters a length that causes the program to crash, it records this event. After completing its run, if any inputs cause crashes, these are logged to a file named `crash_inputs.log` for further investigation.

```shell
python fuzz.py ./simple

...

Testing with input length: 108
Testing with input length: 109
Testing with input length: 110
Testing with input length: 111

...

Testing with input length: 115
Input length 115 causing crash (exit code -11)

...

```

We can view the exact inputs that caused the crash.

```shell
cat crash_inputs.log

...
Input length 148 causing crash (exit code -11): O!@U^p8)uphFO+m8v]l5/#'{(2LPIV+5!`*qgZo<^aCMI(dk]l'!/\2dTl!.NT=V9czH|VI5CowV-[Ph6}9&fZ{a70H@v)2({}G3)Q4'9h}#Yb,nEC*Z[wSYE/wm_mVPNhgDQBj2^%vat==8OrDK
Input length 149 causing crash (exit code -11): tNupxyNTgtY$OY\F{S}$.WO;,Kzy2WMg1z2zJ.|'L:Kp?OoqK&%FK_$e1dAtBK#|q={)1AfS*DZseqVx)HYe%J<p#6)Z=rz!wx"+@7n;he9QKo|k=.d6JdEU9xT0q`DUpU}Nuvfc</Q=WlHKg@V7H
Input length 150 causing crash (exit code -11): Erj@:p,#<fJ-MIPXc(_&nK=O!RA#4!>=5fe4^*6,#!Ap'$aW'XPhIkMpZ-_-A?LZ1s<);TrDf3*yN5(F)Cr`lgy{"=iCiHowB`.9b|)-l+;5H@n8!f[#X_0`b654C/bTY2u2Ex~>*Z/\=\R(qve8}.

```

## Analysis, Proof of Concept and Mitigation

The logged inputs provide crucial information for diagnosing the vulnerability. Developers can identify and rectify the underlying issues by examining the conditions under which the program crashes. In our example, ensuring that input is not copied to the buffer without first checking its length could mitigate the buffer overflow vulnerability.

The core issue lies in the following lines within `vulnerable_function`:

```c++
char buffer[100];
strcpy(buffer, input);

```

1. `Limited Buffer`: The `buffer` array is declared to have the capacity to hold a maximum of 100 characters (including the null terminator).

2. `Unbounded Copy`: The `strcpy` function copies data from the `input` argument into a buffer without checking the length of the input. If the user provides input larger than 100 characters, `strcpy` will happily keep writing data, overflowing the buffer's boundaries.


This type of buffer overflow can lead to:

- `Program Crash`: The most immediate effect is likely a program crash (segmentation fault). This happens when the overflow starts corrupting adjacent memory areas.

- `Data Corruption`: The overflow could overwrite important variables the program uses, changing program behaviour in unpredictable ways.

- `Security Vulnerability`: In the worst-case scenario, a skilled attacker could craft malicious input designed to overflow the buffer and inject executable code. This code could then be run with the same privileges as the vulnerable program, allowing an attacker to compromise the system potentially.


The vulnerability itself is simple to mitigate:

1. `Bounds Checking with strncpy`: Replace `strcpy` with `strncpy`. This function allows you to specify the maximum number of characters to copy:


```c++
strncpy(buffer, input, sizeof(buffer) - 1); // -1 to ensure space for null terminator
buffer[sizeof(buffer) - 1] = '\0'; // Ensure null termination

```

2. `Using fgets More Safely`: While `fgets` does try to restrict input length, it can be misused as in this example. A safer alternative is to specify the buffer size directly to prevent accidental overwrites:


```c++
fgets(input, sizeof(input) - 1, stdin);

```


The final code looking something like this:

```c++
#include <stdio.h>
#include <string.h>

void secure_function(char *input) {
  char buffer[100];
  // Use strncpy for bounds checking
  strncpy(buffer, input, sizeof(buffer) - 1);
  buffer[sizeof(buffer) - 1] = '\0'; // Ensure null termination
  printf("Received input: %s\n", buffer);
}

int main() {
  char input[256];
  printf("Enter some text: ");
  // Limit input size with fgets
  fgets(input, sizeof(input) - 1, stdin);
  secure_function(input);
  return 0;
}

```

Let's save the updated code as `simple_secure.c` and recompile the program with a similar command as before,

```bash
gcc -g -fno-stack-protector -z execstack simple_secure.c -o simple_secure

```

Now, if we run our fuzzer against the newly compiled program, we should see that it no longer crashes:

```shell
python fuzz.py ./simple_secure

Testing with input length: 1
Testing with input length: 2
Testing with input length: 3
Testing with input length: 4
Testing with input length: 5
Testing with input length: 6
Testing with input length: 7
Testing with input length: 8
Testing with input length: 9
Testing with input length: 10
...
Testing with input length: 142
Testing with input length: 143
Testing with input length: 144
Testing with input length: 145
Testing with input length: 146
Testing with input length: 147
Testing with input length: 148
Testing with input length: 149
Testing with input length: 150

No crashes detected.

```


# Fuzzing for Bugs

* * *

While Fuzzing often shines a spotlight on security-related issues like buffer overflows, its uses extend beyond cybersecurity. Fuzzing can effectively identify a wide range of bugs that might not be immediately categorised as security threats but can still lead to software crashes, instability, or unexpected behaviour, such as:

- `Memory Errors`: Fuzzing excels at uncovering flaws in software memory management. This includes issues such as use-after-free errors (where the program tries to use already released memory), out-of-bounds memory access, and memory leaks. These errors can lead to crashes and unpredictable behaviour.
- `Unexpected Input Handling`: Fuzzers excel at producing a wide array of unexpected inputs, such as overly large values, strings with rare characters, or inputs of unusual lengths. This process is crucial for uncovering cases where the software inadequately manages, validates, or sanitizes inputs, which can lead to crashes or unpredictable behavior. Additionally, fuzzing is instrumental in identifying `format string vulnerabilities`—flaws in how software processes formatting strings (like those used in `printf` functions).
- `Race Conditions`: In multi-threaded applications, race conditions occur when the timing of different threads leads to problems. Fuzzing can generate input sequences that trigger race conditions, helping developers identify and fix these subtle errors.

## All tech can be fuzzed

All software, hardware and firmware can be fuzzed, not just programs written in specific program languages or platforms. The universality of fuzzing lies in its fundamental concept. At its heart, fuzzing is about testing software boundaries by feeding it unexpected and unusual inputs. This principle applies regardless of the programming language used to create the software.

Whether you're dealing with a compiled C application, a Java web server, or a Python script, there will always be edge cases, assumptions about input formats, and potential error-handling weaknesses that fuzzing can expose.

Of course, the specific techniques and tools used for fuzzing might differ depending on the target software. Let's consider a few examples:

- `Compiled Languages (C, C++, etc.)`: Fuzzers for these languages often generate malformed data structures, manipulate memory directly, or use coverage-guided techniques to explore different code paths.
- `Interpreted Languages (Python, JavaScript, etc.)`: Fuzzers may focus on generating unusual strings, unexpected object types, or very large numbers to push the interpreter's handling of data and logic to its limits.
- `Network Protocols`: Protocol fuzzers craft malformed network packets, targeting how servers or devices parse and respond to them. This helps identify vulnerabilities in network stacks and protocol implementations.

Beyond languages and platforms, fuzzing extends to various input sources:

- `File Formats`: File format fuzzers manipulate the structure of common file types (images, PDFs, etc.) to reveal weaknesses in parsing code that could lead to crashes or exploitable behaviour.
- `APIs`: API fuzzers target web-based APIs and internal software interfaces, helping identify unexpected interactions that could destabilise a system.

### C/C++

- [AFL (American Fuzzy Lop)](https://lcamtuf.coredump.cx/afl/): A powerful coverage-guided fuzzer known for its effectiveness and ease of use. It employs compile-time instrumentation and genetic algorithms to efficiently find bugs.
- [libFuzzer](https://llvm.org/docs/LibFuzzer.html): A fuzzing engine built into the LLVM compiler. It excels at in-process fuzzing within your C/C++ application code.
- [Honggfuzz](https://github.com/google/honggfuzz): Another coverage-guided fuzzer with a focus on efficiency and simplicity. It supports persistent fuzzing mode for long-running campaigns.

### Python

- [Hypothesis + HypoFuzz](https://github.com/Zac-HD/hypofuzz): A property-based testing library that can also be used for fuzzing with. It allows you to define properties and generate test cases that aim to violate those properties.
- [Atheris](https://github.com/google/atheris): A native Python fuzzing engine specifically designed for coverage-guided fuzzing, powered by libFuzzer. It provides features like automatic test case minimisation, parallel fuzzing, and integration with popular Python testing frameworks like pytest and unittest. This can streamline the fuzzing process for Python developers and improve the efficiency of finding bugs.

### Java

- [JQF + Zest](https://github.com/rohanpadhye/JQF): A fuzzing framework built on top of QuickCheck-style property-based testing. It supports feedback-driven fuzzing and integrates with popular build tools like Maven and Gradle.
- [Kelinci](https://github.com/isstac/kelinci): A Java fuzzing framework built on top of AFL. It allows you to write Java classes that specify the structure of the inputs you want to fuzz, and Kelinci will automatically generate valid inputs according to those specifications. This can help fuzz complex data structures that are common in Java applications.

### JavaScript

- [jsfuzz](https://gitlab.com/gitlab-org/security-products/analyzers/fuzzers/jsfuzz): A fuzzer explicitly designed for JavaScript code; it can find type confusion and DOM-based vulnerabilities.
- [NodeFuzz](https://github.com/attekett/NodeFuzz): A fuzzer aimed at Node.js applications, it can identify issues within API endpoints and JavaScript engine internals.

### Rust

- [cargo-fuzz](https://github.com/rust-fuzz/cargo-fuzz): A fuzzing toolchain integrated directly into Rust's package manager, Cargo. It makes setting up fuzz tests incredibly easy within Rust projects.
- [libfuzzer-sys](https://github.com/rust-fuzz/libfuzzer): A Rust binding for LLVM's libFuzzer, providing familiar and powerful in-process fuzzing capabilities.

### Go

- [gofuzz](https://github.com/google/gofuzz): A coverage-guided fuzzer built into the standard Go testing toolkit. Well-suited for fuzzing libraries and functions within Go code.

### Firmware Fuzzing

- [AFL++ with QEMU mode](https://github.com/AFLplusplus/AFLplusplus): AFL++ is an extended version of AFL, including a mode for fuzzing firmware in the QEMU system emulator. It supports various architectures.
- [Firmadyne](https://github.com/firmadyne/firmadyne): A framework focused on automated firmware extraction and emulation. It uses QEMU for emulation and can be used to identify vulnerabilities in IoT firmware.
- [Avatar2](https://github.com/avatartwo/avatar2): A versatile framework for analysing embedded firmware. It works with QEMU and supports dynamic binary instrumentation for tracing and fuzzing.
- [Fuzzware](https://github.com/fuzzware-fuzzer/fuzzware): A promising project that combines emulation and program analysis to allow fuzzing of firmware without detailed knowledge of the underlying hardware.

### Hardware Fuzzing

- [JTAGulator](https://github.com/grandideastudio/jtagulator): An open source hardware tool that assists in identifying On-Chip Debug (OCD) interfaces from test points, vias, component pads, or connectors on a target device. OCD interfaces provide chip-level control and can be used by engineers, researchers, and hackers for code extraction, data retrieval, memory modification, and on-the-fly device manipulation. Locating these interfaces manually can be difficult, time-consuming, and sometimes requires destructive device modification; JTAGulator helps streamline this process.
- [ChipWhisperer](https://www.newae.com/chipwhisperer): A combination of open-source hardware and software tools for side-channel analysis and fault injection attacks. It can be leveraged for hardware-level fuzzing.
- [Facedancer](https://github.com/greatscottgadgets/facedancer): A USB fuzzing framework allowing the creation of malformed USB descriptors and device behaviours to fuzz hardware-level USB stacks.


# Sanitizers

* * *

While powerful programming languages like C and C++ leave room for subtle errors related to memory management and undefined behaviour, these errors, such as accessing memory you don't own or performing operations with unpredictable results, often become devastating security vulnerabilities.

To combat this, developers have an arsenal of tools called sanitizers:

- `AddressSanitizer (ASan)`: The memory error detective. `ASan` hunts for issues like `Out-of-Bounds Accesses` and `Use-after-free Errors`
- `ThreadSanitizer (TSan)`: The race condition watchdog. `TSan` pinpoints data races where multiple threads try to access and modify the same memory location without proper synchronisation.
- `MemorySanitizer (MSan)`: The uninitialised memory guardian. `MSan` finds places where you use variables without first giving them a value.
- `UndefinedBehaviorSanitizer (UBSan)`: The rule book enforcer. `UBSan` catches instances of code that rely on undefined behaviour according to the C/C++ standards (e.g., signed integer overflow, divide by zero)

These sanitizers are integrated directly into compilers like Clang and GCC. You compile your code with special flags, and they add instructions that perform runtime checks. If an error is detected when you run your program, the sanitizer will provide a detailed report pinpointing the problem. This allows you to catch elusive bugs during development, preventing them from becoming exploitable vulnerabilities in your released software.

Google hosts great, comprehensive information on their [sanitizers git](https://github.com/google/sanitizers).

While sanitizers are immensely valuable during development and testing, they are generally unsuitable for production releases. The primary reason for this is performance overhead. The runtime checks and instrumentation that sanitizers add to your code can significantly slow your application's execution speed. This performance impact can be substantial, potentially making the software unacceptably slow for end-users.

## ASan

`AddressSanitizer` ( `ASan`) is a powerful runtime memory error detection tool built directly into modern compilers like GCC and Clang. Its primary purpose is to uncover memory-related bugs during development and testing before they manifest as security vulnerabilities in production.

ASan is remarkably adept at detecting various classes of memory errors that plague C and C++ code:

- `Out-of-Bounds Accesses`: ASan catches attempts to read or write data outside the designated boundaries of allocated memory blocks. This includes:
  - `Heap buffer overflows/underflows`: Accessing memory beyond the end or before the beginning of a heap-allocated block (e.g., arrays or objects created with `malloc`).
  - `Stack buffer overflows/underflows`: Exceeding the limits of variables stored on the program's stack.
  - `Global buffer overflows/underflows`: Going out-of-bounds with global arrays or data.
- `Use-after-free`: ASan flags when your program tries to use memory that has already been deallocated (returned to the system using `free` or `delete`). This is a dangerous situation that often leads to crashes and unpredictable behaviour.
- `Heap-use-after-free`: A more specific variation of use-after-free, where a dangling pointer (a pointer to deallocated memory) accesses a heap buffer that might have been subsequently reallocated.
- `Memory Leaks`: ASan can assist in identifying memory that's allocated but never freed. While not always an immediate security risk, memory leaks can exhaust system resources and lead to instability.

### How it works

ASan's magic lies in a combination of two key techniques:

1. `Shadow Memory`: ASan maintains a parallel data structure called 'shadow memory' that maps every byte of real memory your program uses to a few bytes of metadata. This metadata stores information about the state of each memory location (whether it's validly allocated, freed, etc.)
2. `Compiler Instrumentation`: When you compile your code with ASan enabled, the compiler inserts tiny snippets of code before every memory access (reads and writes). These code snippets perform fast checks against the shadow memory:
   - Is the memory address being accessed within a valid allocation?
   - Has this memory been freed?

If any of these runtime checks fail, ASan immediately halts your program and generates a detailed error report. This report typically includes:

- The type of error detected (e.g., heap buffer overflow)
- The location in your code where the error occurred
- A stack trace to help you trace the problem's origin

### simple.c

Let’s refer back to the vulnerable `simple.c` program.

```c
#include <stdio.h>
#include <string.h>

void vulnerable_function(char *input) {
    char buffer[100];
    strcpy(buffer, input);
    printf("Received input: %s\n", buffer);
}

int main() {
    char input[256];
    printf("Enter some text: ");
    fgets(input, 256, stdin);
    vulnerable_function(input);
    return 0;
}

```

The buffer overflow in `strcpy(buffer, input)` is easy to identify because the codebase is so tiny, but it will be much harder to trace in a vast, complex project with hundreds of thousands of lines of code. If we utilise ASan, this process of tracing the actual vulnerability becomes a non-issue.

First, compile `simple.c` (if needed) without ASan:

```bash
gcc -g -fno-stack-protector -z execstack simple.c -o simple

```

We know it will crash with a long input, so we can just run simple and input a long string, for example `AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA`.

We can see the program crashes, with the only error provided being a “Segmentation Fault”

```shell
./simple

Enter some text: AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
Received input: AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA

Segmentation fault

```

Now, recompile the program using ASan, by adding the `-fsanitize=address` argument to the compiler.

```bash
gcc -g -fsanitize=address -fno-stack-protector -z execstack simple.c -o simple

```

Rerun the program with the same long input. The crash now looks very different, providing detailed information on the state of the program and a trace:

```shell
./simple

Enter some text: AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
=================================================================
==2415==ERROR: AddressSanitizer: stack-buffer-overflow on address 0x7ffe58357624 at pc 0x7f41d9f244bf bp 0x7ffe58357570 sp 0x7ffe58356d18
WRITE of size 216 at 0x7ffe58357624 thread T0
    #0 0x7f41d9f244be in __interceptor_strcpy ../../../../src/libsanitizer/asan/asan_interceptors.cpp:440
    #1 0x55cdec7a3321 in vulnerable_function /modules/Fuzzing/blackbox/simple.c:6
    #2 0x55cdec7a34a5 in main /modules/Fuzzing/blackbox/simple.c:14
    #3 0x7f41d9cd0d8f in __libc_start_call_main ../sysdeps/nptl/libc_start_call_main.h:58
    #4 0x7f41d9cd0e3f in __libc_start_main_impl ../csu/libc-start.c:392
    #5 0x55cdec7a31a4 in _start (/modules/Fuzzing/blackbox/simple+0x11a4)

Address 0x7ffe58357624 is located in stack of thread T0 at offset 148 in frame
    #0 0x55cdec7a3278 in vulnerable_function /modules/Fuzzing/blackbox/simple.c:4

  This frame has 1 object(s):
    [48, 148) 'buffer' (line 5) <== Memory access at offset 148 overflows this variable
HINT: this may be a false positive if your program uses some custom stack unwind mechanism, swapcontext or vfork
      (longjmp and C++ exceptions *are* supported)
SUMMARY: AddressSanitizer: stack-buffer-overflow ../../../../src/libsanitizer/asan/asan_interceptors.cpp:440 in __interceptor_strcpy
Shadow bytes around the buggy address:
  0x10004b062e70: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x10004b062e80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x10004b062e90: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x10004b062ea0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x10004b062eb0: 00 00 f1 f1 f1 f1 f1 f1 00 00 00 00 00 00 00 00
=>0x10004b062ec0: 00 00 00 00[04]f3 f3 f3 f3 f3 00 00 00 00 00 00
  0x10004b062ed0: f1 f1 f1 f1 00 00 00 00 00 00 00 00 00 00 00 00
  0x10004b062ee0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x10004b062ef0: 00 00 00 00 f3 f3 f3 f3 f3 f3 f3 f3 00 00 00 00
  0x10004b062f00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x10004b062f10: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
  Shadow gap:              cc
==2415==ABORTING

```

ASan's output might look intimidating at first, but let's break it down:

- `Error Type`: It clearly states " `stack-buffer-overflow`" and even pinpoints the problematic line ( `/mnt/c/.../.../simple.c:6`).
  - `WRITE of size 216...` specifies that 216 bytes were attempted to be written outside the buffer's boundaries.
- `Stack Trace`: Shows you exactly where in the code the overflow happened ( `vulnerable_function`, called from `main`).

- `Memory Details`: Indicates the overflown variable ( `buffer`) and how ASan detected the issue.
  - `This frame has 1 object(s): [48, 148) 'buffer' (line 5) <== Memory access at offset 148 overflows this variable` pinpoints the variable `buffer` as the source of the problem and that it was declared on line 5 of your `simple.c` file
  - `[48, 148)` denotes the range of memory addresses on the stack. `48` is the starting byte offset of 'buffer' within the stack frame. `148` is the ending byte offset of `buffer`. However, in memory ranges, the end is `exclusive`, meaning the range includes bytes up to but not including 148. This means `buffer` occupies 100 bytes of memory ( `148 - 48 = 100`).

Instead of a generic " `Segmentation fault`", ASan provides a precise memory error diagnosis. This level of detail saves countless hours of debugging, especially in complex projects.


# Black-Box Fuzzing

* * *

![](https://academy.hackthebox.com/storage/modules/258/BBF.png)

Black-box fuzzing is a software testing technique that evaluates a system's behaviour by providing unexpected or random inputs without knowing its internal workings. The software is treated as a "black box, “and the tester focuses solely on its inputs and outputs. By generating many test cases, black-box fuzzing aims to trigger unexpected behaviours that may reveal vulnerabilities, such as crashes, memory leaks, or security breaches.

## Understanding Black-box Fuzzing

Imagine a complex machine with various buttons and levers, but you have no idea what's inside or how it works. Black-box fuzzing is like randomly pushing buttons and pulling levers to see how the machine reacts. By observing the outputs and responses, you can potentially identify unexpected behaviours or weaknesses in the machine's functionality.

In software testing, black-box fuzzing operates on the same principle. The tester doesn't need access to the software's source code or internal design. Instead, they focus on providing a wide range of inputs, including malformed data, unexpected values, and random sequences, to observe how the software responds.

### Advantages

- `No knowledge of the target required`: Black-box fuzzing can be applied to any binary without needing prior information about its code or structure. This makes it a versatile technique that can be used even when the source code is unavailable or when dealing with closed-source software.
- `Good for finding unknown vulnerabilities`: Black-box fuzzing explores various input possibilities without being constrained by assumptions about the target's behaviour. This makes it effective in uncovering unexpected vulnerabilities that other techniques might miss.
- `Simple to implement`: Black-box fuzzing requires minimal setup and knowledge about the target, making it a relatively straightforward technique even for individuals with limited fuzzing experience.

### Limitations

- `Less efficient than other techniques`: Black-box fuzzing may generate many invalid inputs immediately rejected by the target software. This can lead to slower execution and less effective testing than techniques that leverage some target knowledge.
- `Lower code coverage`: Due to its unguided nature, black-box fuzzing might not reach all parts of the code, especially complex or hidden functionality. This can result in missed vulnerabilities within the untested portions of the code.
- `Difficult to target specific areas`: Without internal knowledge of the target, focusing blackbox fuzzing on specific code paths or functions is challenging. This can make it less efficient when trying to test specific functionalities or vulnerabilities.

## Applicable Scenarios for Black-box Fuzzing

### Testing Closed-Source Software

Many software applications, especially commercial products, are distributed as closed-source, meaning their source code is not publicly available. This presents a challenge for traditional security testing methods that require code analysis. Black-box fuzzing, however, bypasses this obstacle by focusing solely on inputs and outputs. It allows security professionals to assess the security posture of closed-source software without needing access to its internal workings.

### Identifying Vulnerabilities in Network Protocols

Network protocols are the backbone of communication in modern computer systems. These protocols define how data is formatted, transmitted, and received. Vulnerabilities in network protocols can have severe consequences, potentially allowing attackers to eavesdrop on communications, hijack connections, or launch denial-of-service attacks. Black-box fuzzing can be used to send unexpected or malformed data packets to test the robustness of network protocols and uncover potential vulnerabilities.

### Testing Web Applications

Web applications are often complex and handle sensitive user data. Vulnerabilities in web applications can lead to data breaches, financial losses, and reputational damage. Black-box fuzzing can test various aspects of web applications, including input fields, URL parameters, and API endpoints. Security professionals can identify vulnerabilities such as SQL injection, cross-site scripting, and authentication bypasses by providing unexpected inputs and analysing the responses.

### Fuzzing Embedded Systems

Embedded systems are often found in critical infrastructure and devices with limited resources. Due to their specialised nature and hardware constraints, they can be complex to test using traditional methods. Black-box fuzzing offers a valuable approach to testing the resilience of embedded systems against unexpected inputs and potential vulnerabilities.

### Testing APIs

Application Programming Interfaces (APIs) are essential for interconnectivity and data exchange between software components. Black-box fuzzing can test the security and stability of APIs by providing unexpected or malformed requests and analysing the responses. This can help identify vulnerabilities like data leakage, unauthorised access, and denial-of-service attacks.


# Radamsa

* * *

`Radamsa` is a powerful tool that enables the rapid generation of a fuzzing test cases, specifically what we call a `test corpus`.

## What is a test corpus?

First, let’s define an important concept for fuzzing: `A test corpus`.

`A test corpus` is a critical component that fuels the test case generation process in fuzzing. It functions like a springboard for fuzzing tools like Radamsa, providing a foundation of input data that gets progressively mutated to create a vast landscape of test cases:

- `Seeding the Exploration`: The test corpus serves as the initial spark, offering a bank of valid or semi-valid inputs that the fuzzing tool can leverage. These seed inputs represent the scenarios your application might encounter in real-world use. Imagine a test corpus for a web browser containing login forms with different structures and data types. This provides a springboard for the fuzzer to explore the login functionality thoroughly.
- `Shaping Mutations`: The test corpus guides the fuzzing tool, influencing the direction of its mutations. By analysing the structure and format of the data within the corpus, the fuzzer gains insights into the expected format of the application's input. This knowledge empowers it to generate relevant and impactful mutations. For instance, if the corpus primarily consists of text files, the fuzzer is more likely to create mutations that modify text content (e.g., inserting typos, scrambling characters) instead of generating mutations that produce image data. This targeted approach significantly improves the efficiency of the fuzzing process.
- `Expanding Test Coverage`: A well-crafted test corpus is instrumental in maximising the effectiveness of fuzzing. By incorporating a diverse range of seed inputs, the corpus steers the fuzzer towards exploring a broader spectrum of edge cases and potential vulnerabilities within the application. This can include inputs with unexpected lengths, invalid characters, or unusual data combinations that traditional testing methods might overlook. Consider a corpus for a file parser that includes not only common file formats but also malformed or incomplete files. This can help uncover bugs in the parser's ability to handle unexpected data structures.

In essence, the quality and variety of your test corpus directly correlate to the effectiveness of fuzzing. A well-designed corpus, akin to a diverse artist's palette, empowers the fuzzer to generate a richer set of test cases that target potential weaknesses in the application, ultimately leading to a more robust and secure software product.

`Radamsa` is a critical tool that can help build such a collection of inputs. You provide sample files that exemplify the data your application typically handles. It leverages these samples as a guide, applying various mutations to generate many related but corrupted test cases. Think of it as a sculptor using a representative clay model to create numerous variations, each exploring a slightly different potential flaw in the final sculpture.

Radamsa goes beyond simply injecting randomness into your data. It employs several targeted mutation techniques to introduce specific types of errors, such as:

- `Bit Flipping`: This technique `alters the individual bits within data`, potentially changing numerical values, corrupting text encoding, or altering the interpretation of program instructions.
- `Insertion`: Radamsa `inserts new bytes or sequences`, injecting unexpected data into the input stream. This tests the application's ability to handle overflows, boundary conditions, or unexpectedly large data.
- `Deletion`: Radamsa `removes bytes or entire chunks of data`, forcing the application to cope with missing information. If expected values are absent, this can expose internal logic, data structure, or error-handling issues.
- `Overwriting`: This method `replaces parts of the data`, simulating potential corruption during transmission or storage. This tests if the software can detect and gracefully handle invalid or unexpected values within its input.

Based on the 'shape' of your input data, this targeted approach enables Radamsa to help you build a test corpus that exposes a wider range of potential vulnerabilities.

## Installation

Radamsa is easy to install and use on most common operating systems, but you must build it yourself. It's very quick to build, usually no more than thirty seconds to a minute.

```bash
git clone https://gitlab.com/akihe/radamsa.git
cd radamsa
make
sudo make install
radamsa --help

```

## Basic Usage

Let's start with a simple example. Suppose you have a text file named "input.txt" containing the following:

```
This is a sample text file.

```

Here's how to use Radamsa to generate a mutated version:

```bash
radamsa -o output.txt input.txt

```

This command tells Radamsa to take "input.txt" as the sample file, apply its mutations, and save the result to "output.txt." You might find a mutated output like this in the new file:

```
This is a sample t3xt file.

```

Radamsa offers a range of parameters to customise how it generates mutations:

- `-o output-%n.txt`: This generates multiple output files (e.g., output-1.txt, output-2.txt, etc.). It's a great way to create a diverse set of test cases quickly.
- `-n 10`: Controls the number of mutated outputs generated. Increase this number for more extensive testing.
- `-s 1234`: Sets a starting seed for the random number generator. Using the same seed with a specific input file will always produce the same set of mutations, which helps debug and reproduce test cases.
- `-m <mutation_type>`: This lets you focus on specific mutation types. For example, `-m bf` limits mutations to bit flipping only. Check the Radamsa documentation for a full list of mutation types.

### Piping

Perhaps the most straightforward way, piping lets you directly feed Radamsa's generated outputs into your application's standard input (stdin). It's fantastic for continuous fuzzing and quick experimentation.

```bash
# A sample text file
echo "test data" > input.txt

# Continuously fuzz and feed into the program
while true; do
    radamsa input.txt | ./my_program
done

```

Piping is best suited for:

- Programs heavily reliant on standard input.
- Rapid integration for initial fuzzing tests.
- Text-based data processing applications.

### Temporary Files

This method allows greater control over testing as Radamsa's outputs are stored in temporary files. You can then selectively feed these files into your application.

```bash
# Sample image file
cp picture.jpg sample.jpg

# Generate variations, store temporarily
radamsa -o fuzzed-%n.jpg sample.jpg

# Loop through fuzzed images, feed to image viewer
for file in fuzzed-*.jpg; do
    ./image_viewer $file
done

```

Temporary Files are best suited for:

- Complex data formats (images, binaries) where individual outputs need inspection.
- Test cases requiring more organised management compared to piping.
- When finer control over the test execution order is needed.

### Network Sockets

Radamsa's built-in TCP server/client functionalities enable direct fuzzing of network protocols. This is indispensable for testing network-based services.

Radamsa as Server:

```bash
# Simulate an HTTP-like server on port 8080
radamsa -o :8080 -n inf samples/*.http-response

```

Send requests to this server to test how your application handles malformed network data.

Radamsa as Client:

```bash
# Connect to a remote service on port 80, fuzzing the sent data
radamsa -o 192.168.1.10:80 -n inf samples/*.http-request

```

Network Sockets are best suited for:

- Fuzzing network servers and clients.
- Testing the robustness of network protocols and services.
- Security testing where malformed network packets are a concern.

## Putting it all together

The beauty of Radamsa lies in how it dramatically streamlines the fuzzing process compared to writing a custom Python fuzzer:

- `No Scripting Required`: You don't have to write code to handle input generation, mutation strategies, etc. Radamsa takes care of these core fuzzing mechanics out of the box.
- `Variety of Mutations`: Radamsa employs a range of mutation techniques to generate diverse test cases, potentially uncovering a wider array of bugs than a simple hand-written fuzzer might.
- `Ease of Use`: Radamsa's command-line interface makes it very accessible, even for those less familiar with programming.

We can fuzz our `simple.c` program with a single line of bash:

```bash
while true; do echo "a" | radamsa -n 1 | ./simple %; if [[ $? -gt 127 ]]; then break; fi; done

```

1. Infinite Loop ( `while true; do ... done`): This creates a continuous loop, ensuring the fuzzing process runs indefinitely.
2. Seed Input ( `echo "a"`): The `echo "a"` part provides a basic initial input of a single character "a". This serves as a starting point for Radamsa's mutations.
3. Radamsa Fuzzing ( `radamsa -n 1`):

   - `radamsa`: This is the command to invoke your Radamsa fuzzer.
   - `-n 1`: This flag indicates that Radamsa should generate a single mutated output at a time.
4. Feeding to the Program ( `| ./simple %`): The pipe ( `|`) takes the output generated by Radamsa and feeds it into your target program `simple.c`. The `%` is a placeholder for where the fuzzed input will be inserted.
5. Crash Detection ( `if [[ $? -gt 127 ]]; then break; fi`):

   - `$?`: This special variable holds the exit status of the previously executed command (in this case, running `./simple`).
   - `-gt 127`: In many Unix-based systems, an exit status greater than 127 often signals that a program has crashed.
   - `break`: If the program crashes, the loop is terminated. This is a rudimentary crash detection mechanism.

Running the command very quickly iterates to an input that causes a Segmentation Fault crash:

```shell
while true; do echo "a" | radamsa -n 1 | ./simple %; if [[ $? -gt 127 ]]; then break; fi; done

Enter some text: Received input: A

Enter some text: Received input:
Enter some text: Received input: a�򠀡�

Enter some text: Received input: `

Enter some text: Received input: aa

Enter some text: Received input: aᅠ

Enter some text: Received input: a

Enter some text: Received input:
Enter some text: Received input: 󠁩��࿭

Enter some text: Received input: a󠀩

Enter some text: Received input: a

Enter some text: Received input: �󠀭���a

Enter some text: Received input: ⁩a����࿭�������

Enter some text: Received input: a

Enter some text: Received input: �󠀼��a󠀰�[��

Enter some text: Received input: %��
Enter some text: Received input: a�

Enter some text: Received input: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
Segmentation fault

```


# White-Box Fuzzing

* * *

![](https://academy.hackthebox.com/storage/modules/258/WBF.png)

White-box fuzzing is an advanced software testing technique that combines automated input generation with program analysis to discover vulnerabilities. Unlike black-box fuzzing, which treats the software as an unknown "black box," white-box fuzzing requires access to the source code or binary of the application. It uses this insight to intelligently generate test cases that cover a wider range of the program's execution paths, aiming to identify issues such as crashes, security vulnerabilities, and performance bottlenecks.

## Understanding White-Box Fuzzing

Imagine having a transparent machine where you can see all the gears, circuits, and components inside. With white-box fuzzing, you're not just randomly pushing buttons; you're strategically testing the machine based on your understanding of how it works internally. This approach allows for a more thorough examination by targeting specific areas that are likely to fail or be exploited.

In software testing, white-box fuzzing leverages static and dynamic analysis tools to examine the software's codebase. It identifies potential execution paths and generates inputs designed to explore these paths. This method can effectively find hidden vulnerabilities by simulating attacks or unusual conditions that are difficult to anticipate without knowing the software's internals.

### Advantages

- `Highly targeted and efficient`: White-box fuzzing focuses on specific code paths and functions within the target software. This allows for a more targeted approach, leading to faster discovery of vulnerabilities in those areas than techniques that explore the entire codebase.
- `Good for complex input structures`: When the target software expects complex input structures, white-box fuzzing can be particularly helpful. Leveraging knowledge of the expected format and constraints can generate valid and diverse inputs more likely to trigger vulnerabilities within the targeted code.
- `High code coverage`: Due to its targeted nature, white-box fuzzing can achieve higher code coverage than other techniques. This means a larger portion of the code is tested, increasing the chances of finding vulnerabilities hidden within the codebase.

### Limitations

- `Requires extensive knowledge of the target`: Effectively implementing whitebox fuzzing requires a deep understanding of the target code and its internal workings. This often necessitates access to the source code and significant expertise in analysing and understanding the code's behaviour.
- `May miss unknown vulnerabilities`: White-box fuzzing primarily focuses on known code paths and functionalities. This can lead to overlooking unexpected vulnerabilities in the codebase's unexplored or less understood parts.
- `Resource-intensive`: Setting up and implementing white-box fuzzing can require significant expertise, time, and computational resources. This can be challenging for organisations with limited resources or when dealing with large and complex codebases.

## Applicable Scenarios for White-Box Fuzzing

### Supplementing Code Reviews

While code reviews are essential for identifying potential vulnerabilities, the human factor can lead to oversights. White-box fuzzing complements code reviews by systematically exploring execution paths within the code. It leverages its knowledge of the code structure to generate inputs that specifically target areas of interest or potential weaknesses, maximising the chances of uncovering hidden flaws.

### Deep Vulnerability Discovery

White-box fuzzing, guided by code structure, can explore code branches and paths that might be difficult or less likely to reach with black-box testing. This allows for the discovery of vulnerabilities that reside in more complex logic or less frequently executed code, ensuring deeper testing coverage.

### Targeting Specific Code Sections or Algorithms

Security engineers can use white-box fuzzing to pinpoint testing efforts toward critical or high-risk portions of code. This might include new code features, patches, or areas that have historically been sources of vulnerabilities. The code-aware approach allows for focused fuzzing, making the vulnerability discovery process more efficient.


# KLEE

* * *

`KLEE` is a powerful software testing and analysis tool known as a symbolic execution engine. It's designed to systematically explore different execution paths within a program, seeking to find potential bugs or unexpected behaviors. KLEE is particularly valuable for testing code that has complex input structures or dependencies.

`Symbolic execution` is a powerful program analysis technique that underpins KLEE's functionality. Instead of providing concrete values (like specific numbers or strings) as inputs, symbolic execution treats them as `symbolic variables`. These variables act like `placeholders`, representing any possible value that the input could take. As the program runs with these symbolic inputs, the code's operations and calculations are performed on the symbolic variables themselves. This creates symbolic expressions that encode how the program's outputs depend on the symbolic inputs.

A `constraint solver`, which is a program that can reason about these symbolic expressions, is then used to explore different paths through the code. The constraint solver can identify which combinations of possible input values (reflected in the symbolic expressions) would cause the program to follow different execution paths.

KLEE's workflow can be broken down into several key steps:

1. `Working with LLVM Bitcode`: KLEE operates on LLVM bitcode, an intermediate representation of a program. This allows KLEE to be language-agnostic, supporting any programming language that can be compiled to LLVM bitcode (e.g., C, C++).
2. `Symbolic Inputs`: KLEE treats program inputs as symbolic variables, enabling it to explore a vast number of input combinations and execution paths without having to explicitly enumerate them.
3. `Path Exploration`: As KLEE executes a program, it keeps track of the constraints on the symbolic inputs imposed by conditional branches. When it encounters a branch, it records both outcomes, creating a tree of possible execution paths.
4. `Constraint Solving`: KLEE uses constraint solvers to determine if a path is feasible (i.e., if there exists a set of input values that satisfies the path's constraints). If so, KLEE can generate concrete input values that trigger that path, potentially uncovering errors.
5. `Error Reporting`: When KLEE detects a potential error, it generates a test case with concrete input values that lead to the error, facilitating debugging.
6. `Coverage and Optimizations`: KLEE aims to maximize code coverage—the fraction of the program's code executed during testing. It employs various strategies to manage the explosion of possible paths in complex programs, such as pruning infeasible paths and prioritizing paths that might lead to new behaviors.

## Install KLEE

KLEE offers several installation methods:

1. `Build from Source`: This gives you maximum control over the build process but can be a nightmare. It's recommended if you need to customize KLEE's components or are working on KLEE development itself.

2. `Snap Store`: If you're on Ubuntu or another compatible Linux distribution, this is a convenient method for installing a pre-built version of KLEE. It can still be a bit tricky juggling the compatible versions of LLVM so just be sure you are using the correct version of clang with the current snap version of KLEE.


```bash
# install snap if its not installed
sudo apt update
sudo apt install snapd

sudo snap install core

# install the klee snap
sudo snap install klee

```

3. `Docker`: This is often the preferred choice. It provides a self-contained environment for KLEE, ensuring consistency and minimizing compatibility issues. Due to KLEE dependencies, it is not included in the HTBFuzz docker image, so if you are using that container you will still need to pull and run the KLEE image.


```bash
# start the docker daemon if needed
sudo systemctl start docker

# pull klee
sudo docker pull klee/klee

# run a temp container, mount a folder on the desktop as a working directory and drop into the shell
sudo docker run --rm -ti --ulimit='stack=-1:-1' -v ~/Desktop/klee:/data klee/klee:latest

```


# Glee with KLEE

* * *

For our project we are going to use this demonstration code:

```c
#include "klee/klee.h"

int checkValue(int x)
{
    int result = 10 / (x - 10);

    int array[5] = {0, 1, 2, 3, 4};
    int value = array[x];

    return result + value;
}

int main()
{
    int x;
    klee_make_symbolic(&x, sizeof(x), "x");
    return checkValue(x);
}

```

The `klee_make_symbolic` function plays a crucial role. It instructs KLEE to treat a variable as symbolic, meaning it won't have a pre-defined value. Instead, KLEE will explore various possible values for that variable during its analysis.

In this code, the variable `x` in the `main` function is declared symbolic using `klee_make_symbolic`. This allows KLEE to analyse the code's behaviour for different input values of `x`.

The `checkValue` function has two main areas KLEE would focus on:

1. `Division by Zero`: If `x` is assigned a value of 10, the division by `(x - 10)` would result in a division by zero error.
2. `Array Out-of-Bounds`: The function accesses the `array[x]`. If `x` is not within the valid range of 0 to 4, it will cause an out-of-bounds access, leading to undefined behaviour.

KLEE's Analysis Process follows a pattern similar to the below:

1. KLEE begins by treating `x` as completely unknown (symbolic).
2. As KLEE explores various execution paths within `checkValue`, it generates constraints based on encountered conditions. For example, to prevent division by zero, it might create a constraint like `(x - 10) != 0`.
3. KLEE attempts to solve these constraints and identify concrete values for `x` that trigger different execution paths and potentially reveal errors.
4. For each identified path, KLEE would generate a test case containing the input values that lead down that specific path.

## Building the code

Since KLEE functions on LLVM bytecode, we need to compile it specifically for that.

```bash
clang -emit-llvm -c -g -O0 -Xclang -disable-O0-optnone checkValue.c -o checkValue.bc

```

- `-emit-llvm`: This instructs the Clang compiler to generate LLVM bytecode instead of native machine code.
- `-c`: This tells the compiler to stop after generating the bytecode; it doesn't need to link into a full executable.
- `-g`: Include debugging information in the generated bytecode; this helps KLEE provide more informative error reports.
- `-O0`: Turn off all optimisations. This is important because optimizations can change how the code behaves and interfere with KLEE's symbolic reasoning.
- `-Xclang`: Allows for direct passing of specific commands to the Clang frontend, used for providing advanced, Clang-specific options, such as:
  - `-disable-O0-optnone`: Disables the `optnone` attribute at optimization level `-O0`, allowing some minimal optimizations to proceed, potentially improving performance without significantly altering code structure.

Next, execute KLEE on the LLVM bytecode.

```shell
klee --only-output-states-covering-new checkValue.bc

KLEE: output directory is "/data/klee-out-0"
KLEE: Using STP solver backend
KLEE: SAT solver: MiniSat
KLEE: Deterministic allocator: Using quarantine queue size 8
KLEE: Deterministic allocator: globals (start-address=0x14aa9c8e7000 size=10 GiB)
KLEE: Deterministic allocator: constants (start-address=0x14a81c8e7000 size=10 GiB)
KLEE: Deterministic allocator: heap (start-address=0x13a81c8e7000 size=1024 GiB)
KLEE: Deterministic allocator: stack (start-address=0x13881c8e7000 size=128 GiB)
KLEE: ERROR: vuln.c:5: divide by zero
KLEE: NOTE: now ignoring this error at this location
KLEE: ERROR: vuln.c:8: memory error: out of bound pointer
KLEE: NOTE: now ignoring this error at this location

KLEE: done: total instructions = 348
KLEE: done: completed paths = 1
KLEE: done: partially completed paths = 2
KLEE: done: generated tests = 3

```

The KLEE output produces several bits of information that can be broken down into four categories:

- `Output Directory`: KLEE creates a directory to store the test cases it generates during analysis. These test cases embody concrete input values that can trigger specific execution paths within your code. By examining these test cases, developers can gain valuable insights into how the code might behave under various input conditions.
- `Solver and Configuration`: KLEE offers various solver backends to handle the complex constraints it encounters during symbolic execution. The output typically indicates the chosen solver and any configuration settings employed. Understanding these details can be helpful for troubleshooting analysis issues or fine-tuning KLEE's behaviour for specific use cases.
- `Errors`: A critical aspect of KLEE's output is its ability to detect potential errors in the code. KLEE can identify issues like division by zero and memory errors arising from out-of-bounds array access. These error messages pinpoint potential vulnerabilities or bugs within the code, enabling developers to take corrective actions.
- `Statistics`: KLEE provides valuable statistics that shed light on the analysis process. The instruction count reflects the total number of instructions executed during the symbolic analysis. The number of completed paths indicates how many execution paths within the code were fully explored. Partially completed paths represent executions that reached a limit or encountered a condition that prevented further exploration. Finally, the number of generated test cases reflects the overall output produced by KLEE's analysis.

Specifically, we see that KLEE has identified the two issues:

1. `ERROR: vuln.c:5: divide by zero`
2. `ERROR: vuln.c:8: memory error: out of bound pointer`

Analysis results are located in the output directory. The `klee-last` directory holds the latest results. Numbered directories (e.g., `klee-out-0`) store previous runs.

```shell
tree

.
|-- assembly.ll
|-- info
|-- messages.txt
|-- run.istats
|-- run.stats
|-- test000001.div.err
|-- test000001.kquery
|-- test000001.ktest
|-- test000002.kquery
|-- test000002.ktest
|-- test000002.ptr.err
|-- test000003.ktest
`-- warnings.txt

```

### Core Files

| File Name | Description | Purpose |
| :-- | :-- | :-- |
| `assembly.ll` | Contains a human-readable LLVM assembly representation of the analysed code. | For advanced debugging and code analysis. Allows you to see the low-level instructions KLEE executed, potentially uncovering optimization issues or unexpected execution paths. |
| `info` | Basic metadata about the KLEE execution, including command-line arguments used, runtime information, and the version of KLEE. | Quick reference and execution metadata. Helps reproduce analysis results and provides general context for other files. |
| `messages.txt` | A log of internal KLEE messages. | Debugging KLEE itself. Primarily useful for developers working on KLEE, but might contain hints if you are encountering unusual errors in your analysis. |
| `run.istats` | Detailed statistics about KLEE's instruction execution, including counts for different instruction types. | Performance profiling and analysis. Helps identify bottlenecks in the analysed code or within KLEE's symbolic execution engine. |
| `run.stats` | Other general statistics about the KLEE run, such as the number of test cases generated, time spent in symbolic execution, or memory usage. | Overall metrics about the analysis run. Provides a high-level picture of the resources used and the general 'coverage' achieved by KLEE's analysis. |
| `warnings.txt` | Warnings generated by KLEE during its analysis, potentially indicating unsupported features, limitations encountered, or possible inconsistencies in the analysed code. | Identifying potential issues or limitations. Helps you understand areas where the analysis might be incomplete or where your code might trigger undefined behaviour. |

### Test Case Related Files

- `test00000N.ktest`: Individual test cases generated by KLEE. These binary files contain the input data that led to a particular execution path.
- `test00000N.kquery`: The KLEE queries corresponding to a test case. These queries represent the symbolic constraints that must be met for that test case to run.
- `test00000N.ptr.err`, `test00000N.div.err` (and other `.err` files): Error files associated with specific test cases. These are created when KLEE detects errors, such as pointer errors or divisions by zero.

If we view any of the error files, we can find more detailed error information:

```bash
Error: divide by zero
File: vuln.c
Line: 5
assembly.ll line: 25
State: 1
Stack:
	#000000121 in klee_div_zero_check(z=symbolic) at klee_src/runtime/Intrinsic/klee_div_zero_check.c:14
	#100000025 in checkValue(x=symbolic) at vuln.c:5
	#200000059 in main() at vuln.c:17

```

- `Error: divide by zero`: KLEE has detected an attempt to divide by zero, which is an undefined mathematical operation and a common programming error.
- `File: vuln.c` and `Line: 5`: The error originates on line `5` of the file `vuln.c`.
- `assembly.ll line: 25`: The corresponding assembly instruction where the division actually occurs is on line `25` of the `assembly.ll` file.
- `State: 1`: This refers to the unique state ID within KLEE's analysis when the error was encountered. KLEE explores different execution paths, and each path has states representing decision points.

The stack trace shows the sequence of function calls that led up to the error:

1. `klee_div_zero_check(z=symbolic) at klee_src/runtime/Intrinsic/klee_div_zero_check.c:14`:
   - KLEE's runtime library has a special check for divisions by zero.
   - The `z` variable being passed in is symbolic, meaning KLEE treats it as an unknown value that could be zero.
2. `checkValue(x=symbolic) at vuln.c:5`   - A function named `checkValue` in your `vuln.c` file is called, and its argument `x` also holds a symbolic value.
   - This is the source of the problem, as the `checkValue` function probably performs a division using `x` without ensuring it's not zero.
3. `main() at vuln.c:17`   - The error chain started at line `17` within the `main` function, which is the test driver.

In summary, this specific KLEE log has pinpointed the following issue in the code:

- Somewhere in the chain of events starting from your `main` function, a value is reaching the `checkValue` function that can potentially be zero.

- The `checkValue` function on line 5 of `vuln.c` performs a division with this value without adequately handling the case where it might be zero.


The other log will contain similar information to identify and trace the `out of bound pointer` error.


# Grey-Box Fuzzing

* * *

![](https://academy.hackthebox.com/storage/modules/258/GBF.png)

Grey-box fuzzing stands at the intersection of black-box and white-box fuzzing, combining elements to provide a balanced approach to software testing. This technique does not require full access to an application's source code, yet it leverages partial knowledge of the software's internal structures or behaviours to enhance test efficiency and effectiveness. Grey-box fuzzing is adept at uncovering vulnerabilities and performance issues by dynamically analysing running software and intelligently generating inputs that probe its weak spots.

## Understanding Grey-Box Fuzzing

Imagine being given a partially transparent machine. While you can't see everything inside, you have enough visibility to make educated guesses about how certain parts operate. With grey-box fuzzing, you use this partial insight to guide your testing, balancing exploratory randomness and targeted, knowledge-driven probing.

In practice, grey-box fuzzing tools monitor the software's execution to identify how different inputs affect its behaviour. This feedback loop allows the fuzzer to refine its inputs continually, aiming to explore untested paths or trigger unusual behaviours. This method is especially powerful for discovering vulnerabilities that neither purely black-box nor white-box approaches might reveal on their own.

### Advantages

- `Balance between efficiency and coverage`: Grey-box fuzzing strikes a balance between the targeted approach of white-box fuzzing and the broader scope of black-box fuzzing. It leverages some knowledge of the target's internal workings to guide the fuzzing process, making it more efficient than pure black-box fuzzing while still exploring a wider range of input possibilities than white-box fuzzing.
- `Leverages partial knowledge`: This technique can utilise any available information about the target, such as API specifications, protocol formats, or code structure, to improve the effectiveness of fuzzing. This information helps generate more meaningful and valid test cases, increasing the chances of finding vulnerabilities.
- `More efficient than blackbox fuzzing`: By incorporating some knowledge of the target, grey-box fuzzing can avoid generating invalid inputs that the target software would immediately reject. This leads to faster test case execution and allows for more focused testing.

### Limitations

- `Requires some knowledge of the target`: Grey-box fuzzing's effectiveness depends on the accuracy and completeness of the available information about the target. The fuzzing process may be less effective if the information is inaccurate or incomplete or misses certain vulnerabilities.
- `May miss some edge cases`: By focusing on known structures and behaviours, grey-box fuzzing might overlook unexpected vulnerabilities that arise from unforeseen interactions or edge cases that are not accounted for in the available knowledge.
- `More complex to implement than blackbox fuzzing`: Implementing grey-box fuzzing requires additional effort to integrate the available knowledge into the fuzzing process. This might involve developing custom mutators or generators that leverage the specific information about the target.

## Applicable Scenarios for Grey-Box Fuzzing

### Enhancing Continuous Integration Pipelines

Integrating grey-box fuzzing into CI pipelines allows teams to catch and fix vulnerabilities early in development. Its efficiency makes it well-suited for environments where quick feedback and iterative improvements are essential.

### Penetration Testing and Ethical Hacking

Security professionals often use grey-box fuzzing as part of their toolkit for penetration testing and ethical hacking. With partial knowledge of the target system, they can more effectively identify vulnerabilities that attackers could exploit.

### Mobile and Embedded Systems Testing

For mobile and embedded systems, where direct access to source code is often limited, grey-box fuzzing offers an effective testing methodology. It allows testers to uncover vulnerabilities in these often resource-constrained environments without needing comprehensive access to their internal logic.


# libFuzzer

* * *

libFuzzer is a powerful in-process fuzzing engine integrated directly into the LLVM compiler suite. This means it works seamlessly within the compilation process of C, C++, and other languages supported by LLVM. Since libFuzzer operates directly within your application's code during execution, it doesn't require setting up complex environments or simulations.

![libFuzzer](https://academy.hackthebox.com/storage/modules/258/libFuzzer.png)

The heart of libFuzzer is a simple function called a " `fuzzing target`" or " `fuzzing harness`".

A fuzzing harness is a piece of code specifically designed to act as an entry point for a fuzzing engine. Its primary job is to take the fuzzer's generated input, prepare it so the target code understands it, and then execute the target functionality. This setup allows the fuzzer to systematically explore the behaviour of the code under test with a wide range of unexpected or malformed inputs.

This function ( `LLVMFuzzerTestOneInput`) takes an array of bytes ( `Data`) and its length ( `Size`) as input. Your job is to write this function to process the provided data in a way that exercises the code you want to fuzz.

When you compile your code with libFuzzer support (using the `-fsanitize=fuzzer` flag with clang), the LLVM compiler adds special instrumentation. This instrumentation tracks which areas of your code are executed (' `code coverage`') when your harness processes a particular input.

When run, libFuzzer then repeatedly does the following:

- `Generate an input`: It starts with a seed corpus (initial test cases) or generates a new input if nothing has been provided.
- `Mutate the input`: libFuzzer applies various mutations to the input, such as bit flips, byte changes, or splicing in data from existing test cases.
- `Execute the harness`: It calls your fuzzing harness function with the mutated input.
- `Collect coverage`: The instrumentation records the code coverage achieved.
- `Save interesting inputs`: If the new input leads to discovering new code paths, it is added to the corpus for further exploration.

## Install libFuzzer

You will need to install clang to use libFuzzer. All modern versions of clang are bundled with libFuzzer. Most flavours or Ubuntu or Debian will include a version of clang in the default repos, but this may be a very old version (<13).

```bash
sudo apt-get install lld llvm llvm-dev clang

```

You can use the LLVM installer which will install the latest version (17/18 at the time of writing)

```bash
bash -c "$(wget -O - https://apt.llvm.org/llvm.sh)"

```

Or you can manually add the repository for the version you want (https://apt.llvm.org/):

```bash
wget -O - https://apt.llvm.org/llvm-snapshot.gpg.key | sudo apt-key add -
# this adds version 18 repos
echo -e "deb http://apt.llvm.org/unstable/ llvm-toolchain-18 main\ndeb-src http://apt.llvm.org/unstable/ llvm-toolchain-18 main" | sudo tee -a /etc/apt/sources.list.d/llvm.list
sudo apt-get update
sudo apt-get install lld-18 llvm-18 llvm-18-dev clang-18

```

If you have multiple versions of clang installed you may need to specify a specific clang version when you use it:

```shell
clang --version

Ubuntu clang version 14.0.0-1ubuntu1.1
Target: x86_64-pc-linux-gnu
Thread model: posix
InstalledDir: /usr/bin

```

```shell
clang-14 --version

Ubuntu clang version 14.0.0-1ubuntu1.1
Target: x86_64-pc-linux-gnu
Thread model: posix
InstalledDir: /usr/bin

```

```shell
clang-18 --version

Ubuntu clang version 18.1.3 (++20240322073153+ef6d1ec07c69-1~exp1~20240322193300.86)
Target: x86_64-pc-linux-gnu
Thread model: posix
InstalledDir: /usr/bin

```

## libMDP

For our purposes, we are going to fuzz `libMDP`, a very badly purpose-built library. [Download it from here and extract it to a working directory.](https://academy.hackthebox.com/storage/modules/258/libMDP.zip)

The library includes documentation ( `README.md`) that provides a lot of information about its structure and provides a simple example we can quickly learn from:

```c
#include "libMDP.hpp"

int main() {
    std::string markdownText = "# Heading\nThis is a **bold** and _italic_ text with an ![image](url).";
    libMDPParser parser;
    std::string htmlOutput = parser.parse(markdownText);
    std::cout << htmlOutput << std::endl;
    return 0;
}

```

The `libMDPParser` class is responsible for analysing an input string containing Markdown syntax ( `markdownText`). The `parser.parse()` method is where the core work occurs; it transforms the Markdown text into its corresponding HTML representation ( `htmlOutput`), which is then printed to the console.

This small example is very interesting to us for a few reasons:

- `Clear Input Point`: The `parser.parse(markdownText)` function has a well-defined input—a string of Markdown text. This is perfect for libFuzzer, as it generates and mutates text-based inputs.
- `Potential for Complex Logic`: Markdown parsers typically involve handling various syntax elements (headings, emphasis, links, images, etc.). This implies the parsing logic might contain interesting branches within the code, making it a good target for exploring error-prone paths.
- `Potential for Hidden Errors`: Parsers are notorious for subtle bugs. Malformed input can lead to crashes, memory corruption, or unexpected HTML output. libFuzzer is great for finding these kinds of vulnerabilities that traditional unit tests might miss.

## Setting Up a Harness

To create a libFuzzer harness, you write a function called `LLVMFuzzTestOneInput`. This function acts as a bridge between libFuzzer's input generation and your target code. It takes a raw array of bytes ( `Data`) representing the fuzzed input, along with its length ( `Size`). You might optionally convert this data into a format your code understands. For instance, in our Markdown parser example, you'd convert `Data` to a string to feed into the `parser.parse()` function.

The function signature itself is straightforward:

- `const uint8_t* Data`: This argument is a pointer to an array of bytes representing the fuzzed input data.
- `size_t Size`: This argument specifies the size (length) of the data pointed to by `Data`.

The core purpose of the harness is to call your target function with the processed input data. In our example, this would be `parser.parse(inputString)`. While the return value of `LLVMFuzzerTestOneInput` is optional, you can use it to signal interesting findings to libFuzzer. For example, a non-zero return value might indicate that the input triggered unexpected behaviour in your code, which can be a valuable clue for further analysis.

Putting that all together, the fuzzing harness will look like this:

```c++
#include <stdint.h>
#include <string>
#include "libMDP.hpp"

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *Data, size_t Size) {
   std::string inputString(reinterpret_cast<const char*>(Data), Size);
   libMDPParser parser;
   parser.parse(inputString);
   return 0;
}

```

| Aspect | Description | Key Points |
| :-- | :-- | :-- |
| Header | `#include "libMDP.hpp"` | Includes the `libMDPParser` class definition. |
| Harness | `extern "C" int LLVMFuzzerTestOneInput(const uint8_t *Data, size_t Size)` | This is the entry point of the fuzzing harness, the function libFuzzer will repeatedly call. |
| Conversion | `std::string inputString(reinterpret_cast<const char*>(Data), Size);` | Converts raw bytes to a C++ string for use by the parser. |
| Target Call | `libMDPParser parser; parser.parse(inputString);` | Creates a `libMDPParser` object. This is the heart of the action. The harness calls the `parse()` method of the parser using the fuzzed input string that was constructed. |
| Return | `return 0;` | A return value of zero generally indicates the harness ran without issue. You could optionally use different return values to signal specific error conditions during fuzzing. |


# Actually libFuzzing

* * *

With the test harness now coded, we can build the fuzzer. Your directory layout should look like the one below. If it doesn’t, adjust your directory layout or the compile command.

```shell
tree

.
├── libMDP
│   ├── README.md
│   ├── libMDP.cpp
│   ├── libMDP.hpp
└── mdp_fuzzer.cpp

```

Build the harness using clang++, you may need to change the clang version depending on what version you have installed, for example `clang++-18`:

```bash
clang++-18 -std=c++11 -g -O1 -fsanitize=fuzzer,address -I./libMDP mdp_fuzzer.cpp libMDP/libMDP.cpp -o mdp_fuzzer

```

- `clang++-18`: Specifies the use of the Clang C++ compiler (version 18 in this case). Clang is a powerful compiler known for detailed error messages and fast compilation times.
- `-std=c++11`: Instructs the compiler to adhere to the C++11 language standard. This ensures code compatibility with the features and rules from that version of C++.
- `-g`: Adds debugging symbols to the generated executable. This is helpful during the development process, allowing debuggers to provide more detailed information about the program's state.
- `-O1`: Enables a basic level of code optimization. The compiler will attempt to make your code smaller and faster without significantly increasing compilation time.
- `-fsanitize=fuzzer,address`: Activates two sanitizers
  - `fuzzer`: This specifies the inclusion of the libFuzzer library.
  - `address`: This is the inclusion of ASan.

## Running libFuzzer

libFuzzer integrates directly into the built application, so you can start the fuzzing process by running the compiled binary directly.

```shell
./mdp_fuzzer

INFO: Running with entropic power schedule (0xFF, 100).
INFO: Seed: 3443844472
INFO: Loaded 1 modules   (622 inline 8-bit counters): 622 [0x5555556e8fe8, 0x5555556e9256),
INFO: Loaded 1 PC tables (622 PCs): 622 [0x5555556e9258,0x5555556eb938),
INFO: -max_len is not provided; libFuzzer will not generate inputs larger than 4096 bytes
INFO: A corpus is not provided, starting from an empty corpus
#2      INITED cov: 51 ft: 52 corp: 1/1b exec/s: 0 rss: 31Mb
#4      NEW    cov: 55 ft: 56 corp: 2/3b lim: 4 exec/s: 0 rss: 32Mb L: 2/2 MS: 2 CrossOver-CopyPart-
#5      NEW    cov: 56 ft: 60 corp: 3/6b lim: 4 exec/s: 0 rss: 32Mb L: 3/3 MS: 1 CrossOver-
#6      NEW    cov: 57 ft: 61 corp: 4/7b lim: 4 exec/s: 0 rss: 32Mb L: 1/3 MS: 1 ChangeBit-
#8      NEW    cov: 70 ft: 100 corp: 5/11b lim: 4 exec/s: 0 rss: 32Mb L: 4/4 MS: 2 ShuffleBytes-CMP- DE: "\377\377"-
#14     NEW    cov: 75 ft: 107 corp: 6/15b lim: 4 exec/s: 0 rss: 32Mb L: 4/4 MS: 1 ChangeBit-
#15     NEW    cov: 75 ft: 108 corp: 7/18b lim: 4 exec/s: 0 rss: 32Mb L: 3/4 MS: 1 EraseBytes-
#20     NEW    cov: 75 ft: 111 corp: 8/22b lim: 4 exec/s: 0 rss: 32Mb L: 4/4 MS: 5 ShuffleBytes-ChangeByte-CrossOver-EraseBytes-PersAutoDict- DE: "\377\377"-
#26     NEW    cov: 75 ft: 112 corp: 9/26b lim: 4 exec/s: 0 rss: 32Mb L: 4/4 MS: 1 CopyPart-
#29     NEW    cov: 75 ft: 114 corp: 10/30b lim: 4 exec/s: 0 rss: 32Mb L: 4/4 MS: 3 ChangeByte-ShuffleBytes-ChangeBit-
        NEW_FUNC[1/1]: 0x55555569b710 in libMDPParser::parseHeading(std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char>> const&) /modules/Fuzzing/greybox/libMDP/libMDP.cpp:156
#31     NEW    cov: 99 ft: 160 corp: 11/32b lim: 4 exec/s: 0 rss: 33Mb L: 2/4 MS: 2 ShuffleBytes-ChangeByte-
#36     NEW    cov: 99 ft: 161 corp: 12/36b lim: 4 exec/s: 0 rss: 33Mb L: 4/4 MS: 5 PersAutoDict-ShuffleBytes-EraseBytes-CrossOver-ChangeBinInt- DE: "\377\377"-
#38     NEW    cov: 101 ft: 163 corp: 13/40b lim: 4 exec/s: 0 rss: 33Mb L: 4/4 MS: 2 ChangeBit-ShuffleBytes-
#57     REDUCE cov: 101 ft: 163 corp: 13/39b lim: 4 exec/s: 0 rss: 33Mb L: 2/4 MS: 4 CopyPart-ChangeBinInt-PersAutoDict-EraseBytes- DE: "\377\377"-
#88     NEW    cov: 102 ft: 164 corp: 14/40b lim: 4 exec/s: 0 rss: 33Mb L: 1/4 MS: 1 EraseBytes-
#162    NEW    cov: 103 ft: 165 corp: 15/44b lim: 4 exec/s: 0 rss: 33Mb L: 4/4 MS: 4 ChangeByte-ChangeByte-ShuffleBytes-ChangeByte-
#165    NEW    cov: 105 ft: 167 corp: 16/48b lim: 4 exec/s: 0 rss: 33Mb L: 4/4 MS: 3 CMP-ChangeByte-CrossOver- DE: "\000\000"-
#174    NEW    cov: 109 ft: 171 corp: 17/52b lim: 4 exec/s: 0 rss: 33Mb L: 4/4 MS: 4 CMP-ChangeBit-ChangeBit-ShuffleBytes- DE: "\377\377"-
#178    NEW    cov: 137 ft: 200 corp: 18/55b lim: 4 exec/s: 0 rss: 33Mb L: 3/4 MS: 4 ChangeBit-PersAutoDict-EraseBytes-InsertByte- DE: "\000\000"-
        NEW_FUNC[1/1]: 0x55555569ccc0 in libMDPParser::parseEmphasis(std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char>> const&, char, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char>> const&) /modules/Fuzzing/greybox/libMDP/libMDP.cpp:185
#184    NEW    cov: 158 ft: 221 corp: 19/59b lim: 4 exec/s: 0 rss: 33Mb L: 4/4 MS: 1 ChangeBit-
#197    NEW    cov: 160 ft: 223 corp: 20/63b lim: 4 exec/s: 0 rss: 33Mb L: 4/4 MS: 3 ChangeBinInt-ChangeBit-ShuffleBytes-
#210    NEW    cov: 164 ft: 250 corp: 21/67b lim: 4 exec/s: 0 rss: 33Mb L: 4/4 MS: 3 CopyPart-PersAutoDict-CopyPart- DE: "\377\377"-
#214    REDUCE cov: 164 ft: 250 corp: 21/66b lim: 4 exec/s: 0 rss: 34Mb L: 3/4 MS: 4 ShuffleBytes-ChangeBinInt-ChangeBit-EraseBytes-
#215    NEW    cov: 166 ft: 282 corp: 22/70b lim: 4 exec/s: 0 rss: 34Mb L: 4/4 MS: 1 CopyPart-
#241    NEW    cov: 169 ft: 312 corp: 23/74b lim: 4 exec/s: 0 rss: 34Mb L: 4/4 MS: 1 ShuffleBytes-
#246    NEW    cov: 172 ft: 315 corp: 24/78b lim: 4 exec/s: 0 rss: 34Mb L: 4/4 MS: 5 PersAutoDict-ChangeBit-ShuffleBytes-CrossOver-ShuffleBytes- DE: "\000\000"-
#302    NEW    cov: 172 ft: 316 corp: 25/82b lim: 4 exec/s: 0 rss: 34Mb L: 4/4 MS: 1 ShuffleBytes-
#305    NEW    cov: 190 ft: 334 corp: 26/86b lim: 4 exec/s: 0 rss: 34Mb L: 4/4 MS: 3 ChangeBinInt-ChangeBit-CopyPart-
#341    NEW    cov: 191 ft: 335 corp: 27/90b lim: 4 exec/s: 0 rss: 34Mb L: 4/4 MS: 1 ShuffleBytes-
#342    NEW    cov: 193 ft: 350 corp: 28/94b lim: 4 exec/s: 0 rss: 34Mb L: 4/4 MS: 1 CopyPart-
#388    REDUCE cov: 193 ft: 350 corp: 28/93b lim: 4 exec/s: 0 rss: 34Mb L: 3/4 MS: 1 EraseBytes-
#394    REDUCE cov: 193 ft: 350 corp: 28/92b lim: 4 exec/s: 0 rss: 34Mb L: 3/4 MS: 1 EraseBytes-
#427    REDUCE cov: 194 ft: 351 corp: 29/95b lim: 4 exec/s: 0 rss: 35Mb L: 3/4 MS: 3 ChangeBit-PersAutoDict-ChangeByte- DE: "\377\377"-
#479    NEW    cov: 194 ft: 353 corp: 30/99b lim: 4 exec/s: 0 rss: 35Mb L: 4/4 MS: 2 ChangeBinInt-CopyPart-

```

It can be intimidating initially, but let’s break down the output. The start of the log is all general information and setup details:

- `Running with entropic power schedule (0xFF, 100)`: Indicates the use of an entropy-driven power schedule, affecting how the fuzzer decides which inputs to test next.
- `Seed: 3443844472`: The seed value for the pseudo-random number generator, ensuring reproducibility of the test.
- `Loaded 1 modules (622 inline 8-bit counters)`: Shows that one module is loaded with 622 8-bit counters to track coverage.
- `Loaded 1 PC tables (622 PCs)`: Indicates one program counter (PC) table is loaded, containing 622 entries used for more detailed coverage tracking.
- `-max_len is not provided`: libFuzzer defaults to a maximum input size of 4096 bytes without a specified maximum length.
- `A corpus is not provided, starting from an empty corpus`: The fuzzer begins without any initial inputs (corpus) to base its testing on.

### Log Explanation

Following on is the actual Fuzzing Progress Log. The log follows a general pattern of:

```bash
#<test_number> <status> cov: <coverage> ft: <features> corp: <corpus_size>/<total_bytes> lim: <size_limit> exec/s: <executions_per_second> rss: <memory_usage> L: <last_input_size>/<max_input_size> MS: <mutation_strategy>

```

| Component | Description |
| --- | --- |
| `#<test_number>` | The number of the test being executed. This helps track the sequence of tests. |
| `<status>` | Indicates the current status of the test, such as `NEW`, `NEW_FUNC`, `REDUCE`, etc. |
| `cov: <coverage>` | Shows the code coverage metric, which indicates how much of the code is being tested. |
| `ft: <features>` | Represents the number of unique features hit by the input during fuzzing. |
| `corp: <corpus_size>/<total_bytes>` | Displays the number of inputs in the corpus and the total size of the corpus in bytes. |
| `lim: <size_limit>` | The size limit for each input file being tested, often set to ensure manageable input sizes. |
| `exec/s: <executions_per_second>` | The number of executions per second, indicating the speed of the fuzzing process. |
| `rss: <memory_usage>` | Shows the current memory usage of the fuzzer, often referred to as resident set size (RSS). |
| `L: <last_input_size>/<max_input_size>` | Size of the last input compared to the maximum input size observed. |
| `MS: <mutation_strategy>` | Indicates the mutation strategy used by the fuzzer, such as bit flips, byte substitutions, etc. |

### A further breakdown

For example, let’s breakdown a couple of lines out of the log.

```bash
NEW_FUNC[1/1]: 0x55555569ccc0 in libMDPParser::parseEmphasis(std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char>> const&, char, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char>> const&) /modules/Fuzzing/greybox/libMDP/libMDP.cpp:185

```

This line from the libFuzzer output indicates that the fuzzer has discovered a new function, which has expanded its code coverage.

- `NEW_FUNC[1/1]`: This part signifies that the fuzzer has identified a new function. The `[1/1]` means this is the first (and only) new function found at this point in the fuzzing session.
- `0x55555569ccc0`: This is the memory address where the new function begins. Each function in a program is allocated a unique memory address, and this hexadecimal number represents where the `parseEmphasis` function is located in memory.
- `libMDPParser::parseEmphasis`: This is the name of the function that was discovered. The syntax indicates that `parseEmphasis` is a member function of the `libMDPParser` class.

```bash
#9780   REDUCE cov: 258 ft: 838 corp: 160/1233b lim: 17 exec/s: 0 rss: 50Mb L: 2/17 MS: 3 ShuffleBytes-CrossOver-ChangeByte-

```

- `#9780`: This is the test number, indicating that this entry is the 9,780th test performed.
- `REDUCE`: Indicates an optimization in the test input size, maintaining effective fuzzing with less data, which improves testing efficiency.
- `cov: 258`: The coverage metric shows that 258 unique paths in the code have been tested.
- `ft: 838`: Represents the count of unique features or behaviors observed.
- `corp: 160/1233b`: Details the corpus size, with 160 inputs totaling 1233 bytes.
- `lim: 17`: The maximum size limit for test inputs.
- `exec/s: 0`: Indicates the execution rate per second. It’s 0 in this case because the program crashed extremely quickly before libFuzzer could actually ramp its testing speed.
- `rss: 50Mb`: The memory usage of the fuzzing process.
- `L: 2/17`: Shows the size of the last input tested and the largest input encountered.
- `MS: 3 ShuffleBytes-CrossOver-ChangeByte-`: Describes the mutation strategies employed:
  - `ShuffleBytes`: Randomly rearranges bytes within the input.
  - `CrossOver`: Combines elements from different inputs to generate a new test case.
  - `ChangeByte`: Alters the value of a byte, a straightforward but effective mutation technique.

## Harness crashing

Eventually, libFuzzer will crash, and since it was compiled with ASan, there is a nice trace and dump to accompany it.

![](https://academy.hackthebox.com/storage/modules/258/mdp_fuzzer.gif)

```bash
#35344  REDUCE cov: 329 ft: 1340 corp: 331/4675b lim: 43 exec/s: 0 rss: 109Mb L: 10/43 MS: 2 ChangeByte-EraseBytes-
#35371  REDUCE cov: 329 ft: 1350 corp: 332/4717b lim: 43 exec/s: 0 rss: 109Mb L: 42/43 MS: 2 CrossOver-InsertRepeatedBytes-
#35414  NEW    cov: 329 ft: 1351 corp: 333/4760b lim: 43 exec/s: 0 rss: 109Mb L: 43/43 MS: 3 ChangeByte-CopyPart-CrossOver-
#35439  NEW    cov: 330 ft: 1352 corp: 334/4803b lim: 43 exec/s: 0 rss: 109Mb L: 43/43 MS: 5 CrossOver-ChangeBit-CMP-CopyPart-CrossOver- DE: "\377\377"-
=================================================================
==2091==ERROR: AddressSanitizer: stack-buffer-overflow on address 0x7ffff608d079 at pc 0x55555569c939 bp 0x7fffffffcf70 sp 0x7fffffffcf68
WRITE of size 1 at 0x7ffff608d079 thread T0
    #0 0x55555569c938 in libMDPParser::<snip>(std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char>> const&) /modules/Fuzzing/greybox/libMDP/libMDP.cpp:<snip>:32
    #1 0x555555697846 in libMDPParser::parse(std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char>> const&) /modules/Fuzzing/greybox/libMDP/libMDP.cpp:43:84
    #2 0x555555695fdc in LLVMFuzzerTestOneInput /modules/Fuzzing/greybox/mdp_fuzzer.cpp:38:33
    #3 0x5555555a3800 in fuzzer::Fuzzer::ExecuteCallback(unsigned char const*, unsigned long) (/modules/Fuzzing/greybox/mdp_fuzzer+0x4f800) (BuildId: 324067e4303b6a431e21d1dd7981bf08f8d49cb6)
    #4 0x5555555a2f75 in fuzzer::Fuzzer::RunOne(unsigned char const*, unsigned long, bool, fuzzer::InputInfo*, bool, bool*) (/modules/Fuzzing/greybox/mdp_fuzzer+0x4ef75) (BuildId: 324067e4303b6a431e21d1dd7981bf08f8d49cb6)
    #5 0x5555555a4785 in fuzzer::Fuzzer::MutateAndTestOne() (/modules/Fuzzing/greybox/mdp_fuzzer+0x50785) (BuildId: 324067e4303b6a431e21d1dd7981bf08f8d49cb6)
    #6 0x5555555a5385 in fuzzer::Fuzzer::Loop(std::vector<fuzzer::SizedFile, std::allocator<fuzzer::SizedFile>>&) (/modules/Fuzzing/greybox/mdp_fuzzer+0x51385) (BuildId: 324067e4303b6a431e21d1dd7981bf08f8d49cb6)
    #7 0x55555559347f in fuzzer::FuzzerDriver(int*, char***, int (*)(unsigned char const*, unsigned long)) (/modules/Fuzzing/greybox/mdp_fuzzer+0x3f47f) (BuildId: 324067e4303b6a431e21d1dd7981bf08f8d49cb6)
    #8 0x5555555bc5b2 in main (/modules/Fuzzing/greybox/mdp_fuzzer+0x685b2) (BuildId: 324067e4303b6a431e21d1dd7981bf08f8d49cb6)
    #9 0x7ffff7a68d8f in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16
    #10 0x7ffff7a68e3f in __libc_start_main csu/../csu/libc-start.c:392:3
    #11 0x5555555889f4 in _start (/modules/Fuzzing/greybox/mdp_fuzzer+0x349f4) (BuildId: 324067e4303b6a431e21d1dd7981bf08f8d49cb6)

Address 0x7ffff608d079 is located in stack of thread T0 at offset 121 in frame
    #0 0x55555569b71f in libMDPParser::<snip>(std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char>> const&) /modules/Fuzzing/greybox/libMDP/libMDP.cpp:<snip>

  This frame has 11 object(s):
    [32, 40) '__dnew.i.i133'
    [64, 72) '__dnew.i.i83'
    [96, 121) '<snip>' (line 157) <== Memory access at offset 121 overflows this variable
    [160, 192) '<snip>' (line 178)
    [224, 256) 'ref.tmp8' (line 180)
    [288, 320) 'ref.tmp9' (line 180)
    [352, 384) 'ref.tmp10' (line 180)
    [416, 448) 'ref.tmp11' (line 180)
    [480, 512) 'ref.tmp12' (line 180)
    [544, 576) 'ref.tmp13' (line 180)
    [608, 640) 'ref.tmp26' (line 180)
HINT: this may be a false positive if your program uses some custom stack unwind mechanism, swapcontext or vfork
      (longjmp and C++ exceptions *are* supported)
SUMMARY: AddressSanitizer: stack-buffer-overflow /modules/Fuzzing/greybox/libMDP/libMDP.cpp:<snip>:32 in libMDPParser::<snip>(std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char>> const&)
Shadow bytes around the buggy address:
  0x7ffff608cd80: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5
  0x7ffff608ce00: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5
  0x7ffff608ce80: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5
  0x7ffff608cf00: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5
  0x7ffff608cf80: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5
=>0x7ffff608d000: f1 f1 f1 f1 f8 f2 f2 f2 f8 f2 f2 f2 00 00 00[01]
  0x7ffff608d080: f2 f2 f2 f2 f8 f8 f8 f8 f2 f2 f2 f2 f8 f8 f8 f8
  0x7ffff608d100: f2 f2 f2 f2 f8 f8 f8 f8 f2 f2 f2 f2 f8 f8 f8 f8
  0x7ffff608d180: f2 f2 f2 f2 f8 f8 f8 f8 f2 f2 f2 f2 f8 f8 f8 f8
  0x7ffff608d200: f2 f2 f2 f2 f8 f8 f8 f8 f2 f2 f2 f2 f8 f8 f8 f8
  0x7ffff608d280: f3 f3 f3 f3 00 00 00 00 00 00 00 00 00 00 00 00
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
==2091==ABORTING
MS: 1 CopyPart-; base unit: d183115adcf1898ecb1558b67660f061c12c9d19
0x3f,0x23,0x23,0x23,0x23,0x23,0x23,0x23,0x23,0x23,0x23,0x23,0x23,0x23,0x23,0x23,0x23,0x23,0x23,0x23,0x23,0x23,0x23,0x23,0x23,0x23,0x23,0x23,0x23,0x3f,0x23,0x23,0xe9,0xe9,0xe9,0xe9,0x23,
?############################?##\351\351\351\351#
artifact_prefix='./'; Test unit written to ./crash-82816d4242f75a02653e201efd053ec4bfb44649
Base64: PyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyM/IyPp6enpIw==

```

This crash report indicates a stack-buffer overflow within the `libMDPParser::<snip>` function of the `libMDP.cpp` file. The fuzzer identified a specific input that caused the program to write data beyond the allocated space for a variable on the stack, likely the `<snip>` variable (line `<snip>`).

The provided information, including the call stack and memory layout hints, should help identify the root cause within the function. Some part of the code is likely attempting to write to the vulnerable varaible or a neighbouring variable without proper checks to ensure it stays within the designated memory boundaries. This unchecked write operation overflows the intended space, corrupting adjacent data on the stack.

The input that caused the crash is saved into a new file, `crash-<hash>`, and its contents are:

```markdown
#############################?##����#

```

By pinpointing the location and cause of the crash, libFuzzer has helped identify a critical vulnerability in the Markdown parser. In the next section we will triage the issue to fix the bug.


# Triaging the Crash

* * *

`Triage`, when talking about crashes discovered by tools like fuzzers, refers to the process of analysing the crash report to determine the severity, root cause, and potential impact of the issue. It involves looking at the error type (e.g., `stack overflow`, `null pointer dereference`, etc), the location of the crash within the code, and any other information the tool provides (like the input that triggered the crash).

The goal of triaging is to prioritize fixing the issue based on how likely it is to be exploited and the potential damage it could cause.

To recap: LibFuzzer found a stack-buffer-overflow error within the Markdown parsing library ( `libMDP`). The overflow specifically occurs in the `libMDPParser::parseHeading` function ( `libMDP.cpp`, line 163), likely caused by an out-of-bounds write overwriting the `headingLevelMax` variable (line 157). This happened when trying to parse a specific input that libFuzzer generated during its mutations.

Let’s look into `libMDP.cpp`, specifically the `parseHeading` function:

```c++
std::string libMDPParser::parseHeading(const std::string &text)
{
    char headingLevelMax[25];

    size_t level = 0;
    while (text[level] == '#')
    {
        // incrementing
        headingLevelMax[level] = '#'; // Directly copying '#' into the buffer
        level++;
    }

    sprintf(headingLevelMax, "L%d", static_cast<int>(level));

    // Ensure there's a null terminator, but this does not prevent overflow
    // If level is >= size of headingLevelStr, we're writing outside the buffer bounds
    headingLevelMax[level] = '\0';

    size_t first_non_space = text.find_first_not_of(" ", level);
    if (first_non_space == std::string::npos)
        return ""; // Return an empty string if there's only spaces after '#'

    size_t last_non_space = text.find_last_not_of(" ");
    std::string heading_text = text.substr(first_non_space, last_non_space - first_non_space + 1);

    return "<h" + std::string(headingLevelMax) + ">" + heading_text + "</h" + std::string(headingLevelMax) + ">";
}

```

Specifically, line 163, and the surrounding code is:

```c++
char headingLevelMax[25]; //157

while (text[level] == '#')
{
    // incrementing level
    headingLevelMax[level] = '#'; //163
    level++;
}

```

Looking at that specific snippet, the issue becomes clear:

1. `Fixed-Size Buffer`: The `headingLevelMax` array is declared with a fixed size of 25 characters. LibFuzzer generates an input with many '#' characters, exceeding the capacity of `headingLevelMax`.
2. `Unbounded Loop`: The `while` loop increments `level` as long as it encounters '#' characters. If the input has more than 25 consecutive '#', the loop happily writes past the end of the `headingLevelMax` array. When the function tries to finish and return, corrupted stack data leads to a crash picked up by `AddressSanitizer`.

Fixing the problem is simple:

1. `Limit Heading Level`: Enforce markdown's heading level limit (1-6) to prevent writing beyond the buffer's bounds.
2. `Buffer Size Safety with snprintf`: Replace `sprintf` with `snprintf` to ensure writing operations respect buffer limits, preventing overflow.
3. `Ensure Logical Ordering and Correct String Construction`: Utilize `snprintf` correctly to format the heading level, avoiding premature null terminator placement and ensuring the string fits within the buffer.
4. `Validate Input String`: Guard against empty or non-markdown heading inputs to ensure the logic only processes valid markdown headings, returning early for invalid cases.

```c++
std::string libMDPParser::parseHeading(const std::string &text)
{
    char headingLevelMax[25]; // Buffer to store the heading level as a string

    size_t level = 0;
    while (text[level] == '#' && level < std::min(sizeof(headingLevelMax) - 3, size_t(6)))
    {
        level++;
    }

    // Using snprintf to safely write to the buffer, avoiding buffer overflow
    snprintf(headingLevelMax, sizeof(headingLevelMax), "L%d", static_cast<int>(level));

    size_t first_non_space = text.find_first_not_of(" ", level);
    if (first_non_space == std::string::npos)
        return ""; // Return an empty string if there's only spaces after '#'

    size_t last_non_space = text.find_last_not_of(" ");
    std::string heading_text = text.substr(first_non_space, last_non_space - first_non_space + 1);

    return "<h" + std::to_string(std::min(level, size_t(6))) + ">" + heading_text + "</h" + std::to_string(std::min(level, size_t(6))) + ">";
}

```

After replacing the vulnerable `parseHeading` function in the library, we can recompile the fuzzer, let it run, and confirm that there are no further crashes.


# American Fuzzy Lop

* * *

`AFL` ( `American Fuzzy Lop`) is a renowned fuzzing tool known for its efficiency and effectiveness in uncovering software vulnerabilities. Unlike fuzzers that bombard programs with random data, AFL takes a smarter approach, guided by code coverage.

![](https://academy.hackthebox.com/storage/modules/258/afl_screen.png)

AFL's secret weapon is its reliance on instrumentation. During compilation with a special AFL compiler (like `afl-gcc` or `afl-clang`), your target program gets subtly modified. This instrumentation tracks which sections of code execute when processing different inputs. This allows AFL to understand how effective its generated inputs are in exploring different program functionalities.

AFL's operation revolves around a continuous fuzzing loop:

- `Seed Corpus`: The process starts with a collection of valid inputs known as the "seed corpus." These should be representative of the kind of data your program typically handles.
- `Mutation Engine`: AFL unleashes its creative mutation engine on these seeds. It applies various techniques like bit flips, byte insertions/deletions, splicing sections from existing inputs, and even dictionary-based modifications (using pre-defined lists of interesting keywords) to generate a diverse range of new test cases.
- `Execution and Tracking`: Each mutated input is fed to your instrumented program. The instrumentation carefully monitors the code coverage achieved with this input.
- `Corpus Update`: If a mutated input explores new code paths (previously unexecuted sections), it becomes a valuable asset. AFL might attempt to minimize its size for efficiency and then adds it to the corpus for future exploration. This process iterates continuously, with AFL constantly refining its test cases to maximize code coverage and potentially uncover hidden vulnerabilities.

A key difference between `AFL` and `libFuzzer` lies in their input handling. AFL heavily emphasizes the use of a `seed corpus`: a collection of initial valid input files that serve as the starting point for its mutation operations. This corpus gives AFL an understanding of the expected input structure and helps guide its mutations towards more meaningful variations. In contrast, while libFuzzer can also benefit from a corpus, its in-process nature allows it to start fuzzing even without one, generating inputs from scratch as it explores the target code.

## libTXML2

`libTXML2`, a streamlined XML parser derived from TinyXML-2, is a compelling target for fuzzing efforts. Since libTXML2 processes XML from files or strings, its core function involves parsing and interpreting XML structures. This makes it a prime candidate for fuzzing – by feeding it diverse and unpredictable XML inputs, potential vulnerabilities exploitable in real-world scenarios can be uncovered.

[Download it from here and extract it to a working directory.](https://academy.hackthebox.com/storage/modules/258/libTXML2.zip)

### Potential Vulnerabilities

XML parsers, by their nature, are complex and have historically been prone to various security issues, such as:

- `Buffer Overflows`: Improperly validated input sizes can lead to buffer overflow conditions, where data exceeds the memory boundaries set for it, potentially allowing attackers to execute arbitrary code.
- `Memory Leaks and Corruption`: Improper memory management can lead to leaks, where unused memory is not correctly freed, or corruption, where the memory is accessed or modified incorrectly, leading to crashes or unexpected behaviour.
- `XML Injection`: Similar to SQL injection, XML parsers might be vulnerable to injection attacks, where malicious XML elements or attributes can manipulate the parser's behaviour or data processing.
- `Denial of Service (DoS)`: By crafting XML documents that are complex to parse (deeply nested elements or large attribute values), an attacker could exhaust system resources, leading to a denial of service.

Despite being described as "streamlined," `libTXML2` must navigate the inherent complexity of XML parsing, including handling namespaces, attributes, text content, and nested elements. This complexity can introduce subtle bugs, especially in edge cases not covered by typical use cases.

### Specific Areas to Target with Fuzzing

With all that in mind, we can plan to focus on some specific areas of fuzzing:

- `Element and Attribute Parsing`: Explore how `libTXML2` handles various combinations of elements and attributes, especially when faced with uncommonly used or deeply nested elements.
- `Error Handling and Recovery`: Assess the robustness of `libTXML2`'s error handling mechanisms when confronted with invalid XML structures, such as unclosed tags, missing attributes, or illegal characters.
- `Namespace Handling`: Namespaces add another layer of complexity to XML parsing. Fuzzing can reveal how well `libTXML2` manages XML documents with multiple namespaces or incorrect namespace declarations.
- `Large and Complex Documents`: Test the library's performance and accuracy when parsing exceptionally large XML files or documents with extensive attribute lists and deeply nested structures.
- `Special XML Constructs`: Include tests for XML constructs that are legal but rarely used, such as CDATA sections, comments, processing instructions, and entity references, to uncover how `libTXML2` processes these elements.

## Building a Corpus

Creating an effective seed corpus for fuzzing `libTXML2` involves crafting a diverse set of XML documents that explore the breadth of XML syntax and structure, along with the specific features supported by the library.

Given `libTXML2`'s capabilities, including parsing, DOM navigation, element and attribute manipulation, and text handling within elements, the seed corpus should aim to cover:

1. `Basic XML Structures`: Documents representing simple, valid XML structures to ensure basic parsing capabilities.
2. `Attribute-Rich Elements`: XML with elements that have multiple attributes to test attribute parsing and value retrieval functionalities.
3. `Nested Elements`: Deeply nested XML structures to challenge the library's ability to traverse and manage complex DOM trees.
4. `Text Handling`: Elements with various types of text content, including entities, CDATA sections, and texts with special characters to test text retrieval and setting functionalities.
5. `Invalid XML Documents`: Malformed XML strings that violate the XML specification to test error handling and robustness against bad input.
6. `Large XML Files`: Extremely large XML documents to evaluate the library's performance and memory management under stress.
7. `Edge Cases`:
   - Elements with empty text or whitespace.
   - Documents with unusual but legal XML names.
   - XML headers with different declarations and encodings.
   - Comments and processing instructions to see if they are correctly ignored or handled.

### Example Seed Files

Generating a corpus to hit all those points is pretty straight forward, and many of these files would form a part of general software testing, not specifically related to fuzzing. See some examples below:

- A simple XML document with a root element and a child element.


```xml
<example><test>value</test></example>

```

- XML with multiple attributes on several elements, testing attribute parsing.


```xml
<employees>
      <employee id="101" department="Sales" location="New York" />
      <employee id="102" department="HR" location="London" />
</employees>

```

- Deeply nested XML structure to challenge DOM navigation.


```xml
<root>
      <level1>
          <level2>
              <level3>
                  <level4>
                      <level5>Deep value</level5>
                  </level4>
              </level3>
          </level2>
      </level1>
</root>

```

- An XML document containing CDATA sections and entities to test text manipulation features.

- A large XML file with thousands of elements to test performance and memory usage.

- Malformed XML to assess error detection capabilities, such as missing closing tags or mismatched element names.

- XML document with namespaces to verify namespace handling.


```xml
<root xmlns:h="http://www.w3.org/TR/html4/" xmlns:f="https://www.w3schools.com/furniture">
      <h:table>
          <h:tr>
              <h:td>Apples</h:td>
              <h:td>Bananas</h:td>
          </h:tr>
      </h:table>
      <f:table>
          <f:name>African Coffee Table</f:name>
          <f:width>80</f:width>
          <f:length>120</f:length>
      </f:table>
</root>

```

- An XML with processing instructions and comments.


```xml
<?xml version="1.0"?>
<!-- This is a comment -->
<note>
      <to>User</to>
      <from>Library</from>
      <?display "This is a processing instruction"?>
      <heading>Reminder</heading>
      <body>Don't forget to check this out!</body>
</note>

```

- Document that includes unusual but valid element names and attribute names to test parsing edge cases.


```xml
<_strange-root_>
      <_element-with-strange-name_ _odd-attribute_='yes'>
          Odd but valid content.
      </_element-with-strange-name_>
      <_another-strange-element_ />
</_strange-root_>

```


# Fuzzing with AFL++

* * *

![](https://academy.hackthebox.com/storage/modules/258/AFL.png)

We are going to be using a fork of AFL, known as `AFL++`. AFL++ offers significant speed increases over AFL, it integrates tightly with QEMU for binary fuzzing, and uses intelligent mutations to reduce wasted effort. It excels at finding new code paths, it prioritizes unique inputs (collision-free coverage), compares seed effectiveness (Redqueen, INSTRIM), and leverages detailed instrumentation (if compiled with LTO).

AFL++ provides flexible power schedules to control fuzzing strategy, it can prioritize speed ( `AFLFast`), target rare code branches, or use an advanced coverage-guided approach (MMOPT). AFL++ supports parallel fuzzing for better scaling and includes crash analysis tools. Unique features like Unicorn mode (cross-architecture fuzzing) and custom modules offer researchers unmatched flexibility. Plus, its got a very active development community around it, so updates are fast and frequent.

Installing AFL++ is straightforward, but we first need to install some APT packages:

```bash
sudo apt-get update
sudo apt-get install -y build-essential python3-dev automake cmake git flex bison libglib2.0-dev libpixman-1-dev python3-setuptools cargo libgtk-3-dev ninja-build
sudo apt-get install -y lld llvm llvm-dev clang # or use the clang script from earlier
sudo apt-get install -y gcc-$(gcc --version|head -n1|sed 's/\..*//'|sed 's/.* //')-plugin-dev libstdc++-$(gcc --version|head -n1|sed 's/\..*//'|sed 's/.* //')-dev

```

Then pull and build the AFLplusplus repo:

```bash
git clone https://github.com/AFLplusplus/AFLplusplus
cd AFLplusplus
make all # we only need the fuzzer, make distrib builds everything
sudo make install LLVM_CONFIG=llvm-config # update the variable if you are using the latest version with llvm-config-18

```

## Building the Fuzzer

To fuzz `libTXML2` with AFL++, first, compile the library and a simple harness with AFL++'s compilers. The `README.md` documentation provides examples for loading and parsing an on disk XML file using `doc.LoadFile()`. So the harness will take an XML file as input, load it using libTXML2's `doc.LoadFile()`, and perform operations on the parsed data to thoroughly exercise the library's functionality.

Once the harness is compiled, run AFL++ on it and supply initial XML files as seeds. AFL++ will generate mutations of these seeds to create diverse XML inputs, aiming to explore all potential code paths in `libTXML2`.

AFL++ relies on the command-line arguments ( `argv`) passed to the fuzzing harness during execution. Typically, the harness expects a single argument, which is the path to the seed corpus file (containing initial test inputs).

AFL++ takes control of this file, mutates its contents to generate a vast array of test cases, and feeds them sequentially to the harness through `argv[1]`. The harness then utilizes the provided XML file ( `argv[1]`) and its parsing logic (e.g., `libTXML2`) to process the mutated input. This cycle continues, with AFL++ constantly generating new inputs and the harness acting as the target for fuzzing libTXML2.

In contrast, libFuzzer integrates more seamlessly within the target code itself. Instead of relying on external arguments, libFuzzer provides a specific function (e.g., `LLVMFuzzerTestOneInput`) that the target program implements. This function receives the test case data directly as a function argument, eliminating the need for separate seed corpus files and command-line parsing.

```c++
#include "libTXML2.h" // Include the libTXML2 header for XML parsing functionality
#include <iostream>   // For standard input/output and error messages
#include <fstream>    // For potential future file manipulations in the harness

using namespace libTXML2; // Introduce the libTXML2 namespace for easier usage

int main(int argc, char **argv)
{

    // AFL will mutate the input XML file provided as argv[1]
    // This harness is responsible for feeding the mutated input to libTXML2
    if (argc < 2)
    {
        std::cerr << "Usage: " << argv[0] << " <xml_file>" << std::endl;
        return 1; // Indicate failure if no input file is provided
    }

    // XML Parsing with libTXML2:
    XMLDocument doc;       // Create an XML document object
    doc.LoadFile(argv[1]); // Load the fuzzed XML file

    // Basic Validation
    doc.Print(); // Print the content of the parsed XML

    return 0; // Indicate successful execution
}

```

Now compile the fuzzer with the below command:

```shell
afl-clang-fast++ -fsanitize=address -o txml2_fuzzer txml2_fuzzer.cpp libTXML2.cpp -I. -std=c++11

afl-cc++4.10c by Michal Zalewski, Laszlo Szekeres, Marc Heuse - mode: LLVM-PCGUARD
SanitizerCoveragePCGUARD++4.10c
Note: Found constructor function _GLOBAL__sub_I_txml2_fuzzer.cpp with prio 65535, we will not instrument this, putting it into a block list.
[+] Instrumented 21 locations with no collisions (non-hardened mode) of which are 0 handled and 0 unhandled selects.
SanitizerCoveragePCGUARD++4.10c
[+] Instrumented 1878 locations with no collisions (non-hardened mode) of which are 48 handled and 0 unhandled selects.

```

We can see that the fuzzer has been instrumented and compiled.

## Running AFL

We now need to setup the fuzzing project. AFL will require 2 directories:

1. `Input Directory`: This directory plays a pivotal role in the fuzzing process. It contains the " `seed corpus`" \- a collection of sample files or inputs that AFL will use as a starting point for its fuzzing operations. These seeds are essentially the initial inputs from which AFL begins to mutate or modify to generate new, unexplored inputs to test your software. It's important that the seed corpus is as comprehensive as possible, covering a wide range of scenarios to maximize AFL's efficiency in discovering bugs.
2. `Output Directory`: As AFL proceeds with the fuzzing process, it generates a plethora of outputs - including data on `crashes` (potential security vulnerabilities), `hangs` (where the program becomes unresponsive), `detailed logs`, `temporary inputs` that caused interesting behaviors, and so forth. All these outputs are stored in the output directory.

A quick mkdir will create the required directories:

```
$ mkdir in out

```

Next, copy your corpus into the `in` directory. I’m using the first example seed file in `test.xml`. Your project should look something like this:

```shell
tree

.
├── in
│   └── test.xml
├── out
└── txml2_fuzzer

```

```shell
cat ./in/test.xml

<example><test>value</test></example>

```

Now, run `afl-fuzz`:

```bash
afl-fuzz -i in -o out -- ./txml2_fuzzer @@

```

- `afl-fuzz`: This is the core command-line executable for American Fuzzy Lop (AFL) fuzzing.
- `-i in`: This flag specifies the "input" directory ( `in`) containing your seed corpus of sample files.
- `-o out`: This flag designates the "output" directory ( `out`) where AFL will store its findings.
- `--`: A double dash is commonly used to separate the main AFL command options from the command you intend to fuzz.
- `./txml2_fuzzer`: The compiled and instrumented target fuzz harness
- `@@`: This is AFL's unique placeholder used to indicate where it should substitute input files from the input directory during the fuzzing process.

![](https://academy.hackthebox.com/storage/modules/258/AFL.gif)

Let the fuzzer run, note that it may take quite a while (15+ minutes) for it to find anything depending on the speed of your system and luck of the bits.

## Triage

Once a crash has been found, AFL will then save the input that crashed the fuzzer in the `/out/default/crashes` directory with a long ID filename, such as:

```bash
id:000000,sig:06,src:000217+000268,time:29532,execs:401476,op:splice,rep:14

```

| Field | Description | Significance |
| :-- | :-- | :-- |
| `id:000000` | Unique crash identifier | Helps track and organize multiple crash instances |
| `sig:06` | Crash signal | Suggests the type of vulnerability |
| `src: ...` | Code location or range associated with the crash | Helps pinpoint the problematic code area |
| `time: ...` | Time elapsed when the crash was found | Gauges how long it took AFL to uncover the bug |
| `execs: ...` | Number of executions at the time of the crash | Indicates how many test cases AFL tried before the crash |
| `op: splice` | AFL mutation strategy used | Suggests input features that triggered the vulnerability |
| `rep:14` | Number of times the crash has been reproduced | Indicates crash consistency or reliance on specific factors |

You can then trigger that specific crash by parsing that file directly into the fuzzing harness:

```shell
./txml2_fuzzer ./out/default/crashes/id\:000000\,sig\:06\,src\:000217+000268\,time\:29532\,execs\:401476\,op\:splice\,rep\:14

=================================================================
==2748212==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x511000000280 at pc 0x555555606440 bp 0x7fffffffd530 sp 0x7fffffffcce8
WRITE of size 266 at 0x511000000280 thread T0
    #0 0x55555560643f in strcpy (/tmp/txml2_fuzzer+0xb243f) (BuildId: c189a2c769901e28e5a1389ac25cca89405712be)
    #1 0x55555566ecfe in libTXML2::<snip>(char const*, int) /modules/Fuzzing/greybox/libTXML2/libTXML2.cpp:<snip>:9
    #2 0x55555566ecfe in libTXML2::XMLDocument::SetError(libTXML2::XMLError, int, char const*, ...) /modules/Fuzzing/greybox/libTXML2/libTXML2.cpp:2660:19
    #3 0x55555566d240 in libTXML2::XMLNode::ParseDeep(char*, libTXML2::StrPair*, int*) /modules/Fuzzing/greybox/libTXML2/libTXML2.cpp:1243:32
    #4 0x55555566c4b8 in libTXML2::XMLNode::ParseDeep(char*, libTXML2::StrPair*, int*) /modules/Fuzzing/greybox/libTXML2/libTXML2.cpp:1202:23
    #5 0x5555556879f2 in libTXML2::XMLDocument::Parse() /modules/Fuzzing/greybox/libTXML2/libTXML2.cpp:2701:9
    #6 0x5555556879f2 in libTXML2::XMLDocument::LoadFile(_IO_FILE*) /modules/Fuzzing/greybox/libTXML2/libTXML2.cpp:2549:9
    #7 0x555555687375 in libTXML2::XMLDocument::LoadFile(char const*) /modules/Fuzzing/greybox/libTXML2/libTXML2.cpp:2490:9
    #8 0x55555565e07b in main /modules/Fuzzing/greybox/libTXML2/txml2_fuzzer.cpp:22:13
    #9 0x7ffff7a68d8f in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16
    #10 0x7ffff7a68e3f in __libc_start_main csu/../csu/libc-start.c:392:3
    #11 0x555555584564 in _start (/tmp/txml2_fuzzer+0x30564) (BuildId: c189a2c769901e28e5a1389ac25cca89405712be)

0x511000000280 is located 0 bytes after <snip>-byte region [0x511000000180,0x511000000280)
allocated by thread T0 here:
    #0 0x55555565bc0d in operator new[](unsigned long) (/tmp/txml2_fuzzer+0x107c0d) (BuildId: c189a2c769901e28e5a1389ac25cca89405712be)
    #1 0x55555566ecda in libTXML2::<snip>(char const*, int) /modules/Fuzzing/greybox/libTXML2/libTXML2.cpp:<snip>:18
    #2 0x55555566ecda in libTXML2::XMLDocument::SetError(libTXML2::XMLError, int, char const*, ...) /modules/Fuzzing/greybox/libTXML2/libTXML2.cpp:2660:19
    #3 0x55555566d240 in libTXML2::XMLNode::ParseDeep(char*, libTXML2::StrPair*, int*) /modules/Fuzzing/greybox/libTXML2/libTXML2.cpp:1243:32
    #4 0x55555566c4b8 in libTXML2::XMLNode::ParseDeep(char*, libTXML2::StrPair*, int*) /modules/Fuzzing/greybox/libTXML2/libTXML2.cpp:1202:23
    #5 0x5555556879f2 in libTXML2::XMLDocument::Parse() /modules/Fuzzing/greybox/libTXML2/libTXML2.cpp:2701:9
    #6 0x5555556879f2 in libTXML2::XMLDocument::LoadFile(_IO_FILE*) /modules/Fuzzing/greybox/libTXML2/libTXML2.cpp:2549:9

SUMMARY: AddressSanitizer: heap-buffer-overflow (/tmp/txml2_fuzzer+0xb243f) (BuildId: c189a2c769901e28e5a1389ac25cca89405712be) in strcpy
Shadow bytes around the buggy address:
  0x511000000000: fa fa fa fa fa fa fa fa 00 00 00 00 00 00 00 00
  0x511000000080: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x511000000100: 00 00 00 00 00 03 fa fa fa fa fa fa fa fa fa fa
  0x511000000180: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x511000000200: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x511000000280:[fa]fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x511000000300: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x511000000380: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x511000000400: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x511000000480: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x511000000500: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
==2748212==ABORTING

```

`AddressSanitizer` ( `ASAN`) detected a heap-buffer-overflow error. This means that the program attempted to write more data into a memory block on the heap than it was allocated for:

- The overflow occurred in the `strcpy` function while copying data into a buffer.
- The overflow originates from calls inside the `libTXML2` library.

The call stack shows you how the code execution reached the point of the error:

1. `main` (txml2\_fuzzer.cpp): The main function of the fuzzer.
2. `libTXML2::XMLDocument::LoadFile` : Loads an XML file.
3. `libTXML2::XMLDocument::Parse` : Parses the loaded XML.
4. ... (Several internal XML parsing functions within libTXML2 )
5. `strcpy`: The overflow occurs here.

The fuzzed input file ( `./out/default/crashes/id\:000000\,sig\:06\,src\:000217+000268\,time\:29532\,execs\:401476\,op\:splice\,rep\:14`), when processed by `libTXML2`, triggers the sequence of function calls that ultimately results in the vulnerability being triggered.


# Skills Assessment One

* * *

The latest assignment at work involves an analysis of a binary file named `sa-one`. This file is available for download at [this link](https://academy.hackthebox.com/storage/modules/258/sa-one.zip) or from the relevant questions section below.

The directive associated with this task was rather informal and lacked specific details: "It includes some sanitizer thing that makes it secure. There is also a cool new feature that means it will reject anything that doesn’t include a special prefix, `<<in<<`, which will also keep those hackers out, right?"

Despite the casual manner in which the brief was communicated, the task is clear. You are required to conduct an examination of the `sa-one` binary to assess its overall security. This analysis will determine the effectiveness of the security measures embedded within the binary and identify any potential vulnerabilities that may have been overlooked.

Note: You may need to install `libasan` if you see an error like `error while loading shared libraries: libasan.so.6` when attempting to run the binary:

```bash
sudo apt update
sudo apt install libasan6

```


# Skills Assessment Two

* * *

Your company's recent influx of junior developers has turned into a codebase crisis! The owner's son, eager to make his mark, decided to "improve" a Markdown library used throughout your projects. Unfortunately, his enthusiasm seems to have outweighed his experience.

Your boss, for reasons unknown, refuses to roll back the changes. This leaves you on a hunt to pinpoint the problems introduced by our well-intentioned but misguided junior developer.

You can download the library files [from here](https://academy.hackthebox.com/storage/modules/258/maddyX.zip) or from the questions below.

**Note: There are 2 issues closely related that you might find, if answering the specifics in the questions doesn’t work for the one, try for the other.**


