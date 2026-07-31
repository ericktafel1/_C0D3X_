| Command | Description |
| --- | --- |
| `apt-get install adb` | Install ADB on Linux. |
| `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`   `brew update`   `brew install android-platform-tools` | Install ADB on MacOS. |
| `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser`   `iex (New-Object System.Net.WebClient).DownloadString('https://get.scoop.sh')`   `scoop bucket add extras`   `scoop install adb` | Install ADB on Windows. |
| `adb start-server` | Start ADB server. |
| `adb devices` | List Android Virtual Devices (AVDs). |
| `adb shell` | Open an interactive shell on the device. |
| `adb root` | Restart ADB as root. |
| `adb install myapp.apk` | Install an app on the device. |
| `adb push ./myapp.apk /sdcard/Download/` | Push files to the device. |
| `adb pull /sdcard/Download/myapp.apk .` | Pull app from the device to the local host. |
