| **Command**                                                                 | **Description**                                                    |
| --------------------------------------------------------------------------- | ------------------------------------------------------------------ |
| `defaults write com.apple.Finder AppleShowAllFiles true && killall Finder ` | Enable the setting to view hidden files in finder from CLI         |
| `ls`                                                                        | Lists directory contents.                                          |
| `ls -l`                                                                     | list directory contents and their attributes                       |
| `ls -la`                                                                    | list directory contents to include hidden files & their attributes |
| `cd <path>`                                                                 | Changes the directory.                                             |
| `clear`                                                                     | Clears the terminal.                                               |
| `touch <file>`                                                              | Creates an empty file in your current working directory.           |
| `mkdir <directory>`                                                         | Creates a new directory in your current working directory          |
| `mv /Users/htb-student/Documents/Test /Users/htb-student/Desktop/Test`      | Move a file from one directory to another                          |
| `chmod -vv <octal value> <file>`                                            | Modify permissions of a file and show the results                  |
| `sudo chown <userOwn>:<groupOwn> <file> `                                   | Change the user and group owner of a file                          |

---

# Networking Commands

| **Command** | **Description** |
| --- | --- |
| `ifconfig` | View basic networking configurations |
| `ifconfig <interface>` | View specific networking configurations of an interface |
| `ifconfig en0 inet <192.168.1.1> netmask < 255.255.255.0 >` | Manually set an interfaces IP address and subnet mask |
| `lsof -n -i4TCP -P` | View TCP ports that are bound while displaying the application that has it bound |
| `hostname` | Check the hostname of the computer |
| `networksetup -listallnetworkservices` | Displays a list of all the network services (devices) on the computer’s hardware. This will print out the logical name of the device. (ex. Wi-Fi) |
| `networksetup -listnetworkserviceorder` | This will print out the network services running and the order in which they are queried for connection. A service at the beginning of the list is checked first. |
| `networksetup -getinfo <devicename>` | Get basic info about a networkservice (device), such as the IP address assigned, subnet mask, gateway, and Mac-Address. |
| `networksetup -getcurrentlocation` | Prints out the currently set network location. |
| `networksetup -setmanual <networkservice> <ip> <netmask> <Gateway>` | This will manually configure the IP address, network mask, and gateway for the device specified. |
| `networkQuality -I <interface>` | Check network speeds of a specific interface |
| `security find-generic-password -wa <SSID>` | Pull the password associated with a specific SSID from the security keychain |
| `nc` | Can be used to bind ports to connect with or listen from |

---

# Application Management

| **Command** | **Description** |
| --- | --- |
| `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"` | Install Homebrew |
| `brew -v ` | Display the version/package information for Homebrew |
| `brew install <package>` | Install a package using Homebrew |
| `brew search firefox` | Have Homebrew search its repository for a package named "firefox" |
| `brew install <package> --cask` | Install a cask application |
| `brew uninstall <package>` | Remove a package from the host |
| `brew upgrade` | Upgrade Homebrew and all packages installed with it |
| `brew cleanup` | Cleanup old & unused files and applications with Homebrew |

---

# Shell Management Commands

| **Command** | **Description** |
| --- | --- |
| `.bashrc` | Configuration file for Bash |
| `.zshrc` | Configuration file for Zsh |
| `chsh -s /bin/bash` | Change our env shell to Bash |
| `brew install zsh` | Install zsh with Homebrew |
| `chsh -s /bin/zsh` | Change our env shell to Zsh |
| `alias ll='ls -l'` | Set an alias for ll in the .zshrc file |
| `sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"` | Install Oh My Zsh |
| `git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting` | Install Zsh-syntax-highlighting |
| `git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k` | Install the Powerlevel-10k theme to Zsh |
| `brew install romkatv/powerlevel10k/powerlevel10k` | Install the Powerlevel-10k theme to Zsh using Homebrew |
| `echo "source $(brew --prefix)/opt/powerlevel10k/powerlevel10k.zsh-theme" >>~/.zshrc` | Set the theme of our shell in the .zshrc file |