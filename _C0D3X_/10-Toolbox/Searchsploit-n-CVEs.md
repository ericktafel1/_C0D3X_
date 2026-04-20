## Finding Vulnerabilities and Exploits Checklist

> Source: `01101100-C0D3X-00110110.md` → `Detailed Checklists > Finding Vulnerabilities and Exploits Checklist`

1. Use `searchsploit` to find exploits:

    ```bash
    searchsploit -u
    searchsploit --cve CVE-2019-7214
    searchsploit application_name
    ```

2. Use Google to search for known vulnerabilities.
3. Use CVEMap for detailed searches:

    ```bash
    cvemap -p application_name -k
    cvemap -q "Vendor" -q "Product"
    ```

4. Search inside Metasploit for available modules.
5. Use Sploitus and Exploit-DB for additional resources.
6. Revert the machine if necessary and research in detail.
7. Double-check all findings to ensure accuracy.
8. Remember, **Enumeration is key; step back and try harder.**
9. Ensure all possible vulnerabilities have been identified.


## Searching for Exploits

> Source: `01101100-C0D3X-00110110.md` → `Exploitation > Service Exploitations > Searching for Exploits`

```bash
searchsploit <service>
```

**Searchsploit Options:**

- `-m`: Copy exploit to the current directory.
- `--cve <CVE_ID>`: Search for exploits by CVE ID (e.g., `--cve 2025-#####`).
- `-e exact`: Perform an exact title match.
- `-p`: Show the full path of the exploit.


## Outdated Software

> Source: `01101100-C0D3X-00110110.md` → `Exploitation > Service Exploitations > Outdated Software`

- Exploit known vulnerabilities (e.g., **EternalBlue** for **SMBv1**).
- Consider using **Metasploit** for automated exploitation.
