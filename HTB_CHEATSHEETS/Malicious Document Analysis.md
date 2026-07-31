| Command | Description |
| --- | --- |
| `trid <file` | Identify File Type. |
| `scdbg.exe /f c:\temp\rtf_shellcode.sc` | Shellcode Emulation using scdbg. |
| `XORSearch.exe -W c:\temp\rtf_shellcode.sc` | Detect shellcode entrypoint using XORSearch. |
| `scdbg.exe /f c:\temp\rtf_shellcode.sc /foff 372` | Shellcode Emulation at specific offset e.g. 372. |
| `speakeasy -t c:\temp\rtf_shellcode.sc -r -a x86 -r --raw_offset 372` | Shellcode Emulation using speakeasy. |
| `speakeasy -t c:\temp\rtf_shellcode.sc -r -a x86 -r --raw_offset 372` | Shellcode Emulation in speakeasy at specific offset e.g. 372. |

# PDF Document Analysis

| Command | Description |
| --- | --- |
| `python pdfid.py <pdf-file.pdf> -a` | Basic summary about PDF Sample. |
| `python pdf-parser.py <pdf-file.pdf>` | To list all objects and associated entries. |
| `python pdf-parser.py <pdf-file.pdf> --search=<keyword>` | Search inside PDF objects. |
| `python pdf-parser.py <pdf-file.pdf> -s /URI` | Search for `/URI` in all objects using pdf-parser.py |
| `python pdf-parser.py <pdf-file.pdf> --objstm` | Parse the stream object using pdf-parser. |
| `python pdf-parser.py -o <obj_id> -d image.jpeg <pdf-file.pdf>` | Dump image object `obj_id` as a JPEG file. |
| `python pdf-parser.py <pdf-file.pdf> -r <obj_id>` | Check objects referencing target `obj_id`. |

# Office Document Analysis

| Command | Description |
| --- | --- |
| `python olemeta.py <office-document>` | Get standard properties present in the OLE file. |
| `python oletimes.py <office-document>` | Extract creation and modification times of all streams and storages in the OLE file. |
| `python oleid.py <office-document>` | Summary related to the sample including suspicious keywords. |
| `python olevba.py <office-document>` | Extract and analyze the VBA source code |
| `python oleobj.py <office-document>` | Extract the external relationship details directly |

# RTF Document Analysis

| Command | Description |
| --- | --- |
| `python rtfdump.py <RTF-document>` | Dump the contents of RTF document level-wise. |
| `python rtfdump.py <RTF-document> --select 4 --hexdecode \| more` | Display object 4 in hex-format. |
| `python rtfdump.py <RTF-document>  --select 4 --hexdecode --dump > c:\temp\rtf_shellcode.sc` | Dump object 4 containing shellcode. |