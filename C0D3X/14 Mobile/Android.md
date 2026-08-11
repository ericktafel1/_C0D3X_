## MobSF (#1)

```bash
docker pull opensecurity/mobile-security-framework-mobsf:latest
docker run -it --rm -p 8000:8000 opensecurity/mobile-security-framework-mobsf:latest

# Default username and password: mobsf/mobsf

# OR

docker run -it --rm --network=host -p 8000:8000 opensecurity/mobile-security-framework-mobsf:latest

# Browse to http://127.0.0.1:8000 and upload test.apk
```

## jadx (#2)

`jadx-gui`
- Open `test.apk`
## APKTool

```bash
apktool d test.apk
# Decompiles and saves as a folder in directory.
```

## Frida

```bash
# https://frida.re/docs/android/

pip install frida-tools
frida-ls-devices
frida-apk test.apk
firda-ps -D <Id>
```