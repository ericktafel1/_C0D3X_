
# Convert PE files to Shellcode

```
~/Inev/tools/donut -a 3 -f 3 -o calc.c -i C:\windows\system32\calc.exe
```

- `-a` specifies the architecture; in this case 3 is x86 + amd64 (dual-mode)
- `-f` specifies the format. By default donut creates a bin file, but mode 3 creates a byte array in the C programming language.
- `-o` specifies the output file name.
- `-i` specifies the input file name. (C:\windows\system32\calc.exe )
- `-p` can specify arguments that would normally be passed to the executable being converted.