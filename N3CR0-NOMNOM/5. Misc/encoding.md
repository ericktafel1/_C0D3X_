
# base64

echo 'this is a test' | base64

# base64 decode

echo 'dGhpcyBpcyBhIHRlc3QK' | base64 -d

# hex encoding

echo 'this is a test' | xxd -p

# hex decoding

echo '74686973206973206120746573740a' | xxd -p -r

# rot13/caesar

echo 'this is a test' | tr 'A-Za-z' 'N-ZA-Mn-za-m'

# rot13 decoding

echo 'guvf vf n grfg' | tr 'A-Za-z' 'N-ZA-Mn-za-m'