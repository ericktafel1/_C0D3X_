## Strict SSH Checking

> Source: `01101100-C0D3X-00110110.md` → `Exploitation > Password Attacks > Cracking Hashes > Strict SSH Checking`

```bash
ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -i id_rsa -p 2222 alfred@192.168.199.201


id_ecdsa

id_dsa
```


## Insert SSH key

> Source: `01101100-C0D3X-00110110.md` → `Linux > Insert SSH key`

```
echo '<id_rsa.pub> >>' authorized_keys

id_ecdsa

id_dsa
```


## z. Misc.

> Source: `z. Misc..md` → `z. Misc.`

# root

- incase I am being dumb and need root with the right zshrc config:
	- `sudo -i zsh`

# Fix SSH

Steps to resolve:

Verify the change If you control the remote machine, check if the SSH keys were changed. You can do this by running on the target system:

```bash
ssh-keygen -lf /etc/ssh/ssh_host_ed25519_key.pub
```

Compare the fingerprint with the one in the warning.

Remove the old key If you determine the change is legitimate, remove the old entry with:

```bash
ssh-keygen -f '/root/.ssh/known_hosts' -R '[192.168.142.52]:2222'
```

This removes the outdated key from your known_hosts file.

Reconnect to accept the new key Try connecting again:

```bash
ssh student@192.168.142.52 -p 2222
```

It will prompt you to accept the new key. Verify the fingerprint before accepting.

If you don't control the target, be cautious—it could be a MitM attack. If you're pentesting, consider investigating further before proceeding.

---

strict checking?

```bash
ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -i id_rsa -p 2222 alfred@192.168.199.201
```

be sure to `chmod 600 id_rsa`

It looks like you're trying to SSH into `dave@192.168.199.201` on port 2222, but you're facing authentication issues. Here are some things to check and try:
#### 1. **Check SSH Key Authentication

It looks like you attempted to generate a new key pair but may have saved it incorrectly. Run:

```bash
ls -lah ~/.ssh/
```

Make sure you have:
- `id_rsa` (private key)
- `id_rsa.pub` (public key)

If they are missing, regenerate them properly:

```bash
ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519 -N ""
```

#### 2. **Ensure the Public Key is on the Target Machine**

On the **target machine (**`**192.168.199.201**`**)**, the public key should be in:

```bash
/home/dave/.ssh/authorized_keys
```

Check if the file exists:

```bash
ls -lah /home/dave/.ssh/

cat /home/dave/.ssh/authorized_keys
```
If missing, manually append your public key:

```bash
echo "your-public-key-here" >> /home/dave/.ssh/authorized_keys

chmod 600 /home/dave/.ssh/authorized_keys

chown dave:dave /home/dave/.ssh/authorized_keys
```

#### 3. **Check SSH Server Configuration

On the target machine, check the SSH config:

```bash
sudo cat /etc/ssh/sshd_config | grep -E 'PermitRootLogin|PubkeyAuthentication|PasswordAuthentication'
```

Ensure:

```bash
PubkeyAuthentication yes

PasswordAuthentication yes

PermitRootLogin prohibit-password
```

Restart the SSH service:

```bash
sudo systemctl restart ssh
```

#### 4. **Verbose SSH Debugging
- Try connecting with verbose output:
```bash
ssh -vvv -p 2222 dave@192.168.199.201
```


**You said:**

dont have access to dave's machine. i am still getting this error: root@kali:~/.ssh# ssh -p 2222 dave@192.168.199.201 dave@192.168.199.201's password: Permission denied, please try again. dave@192.168.199.201's password: Permission denied, please try again. dave@192.168.199.201's password: dave@192.168.199.201: Permission denied (publickey,password,keyboard-interactive).



**ChatGPT said:**

You're hitting an authentication issue when trying to SSH into `dave@192.168.199.201` on port `2222`. Here are some things to check and try:

#### 1. **Verify Password
- Ensure you're using the correct password for `dave`. If possible, try logging in locally on the target system.

#### 2. **Check SSH Authentication Methods
- Run the following to see which authentication methods are available:
```bash
ssh -v -p 2222 dave@192.168.199.201
```
- If it shows `Permission denied (publickey,password,keyboard-interactive).`, it means the server might not accept password authentication or the password is incorrect.

#### 3. **Try a Different Authentication Method
- If the system allows public key authentication and you have a valid private key, try:
```bash
ssh -i ~/.ssh/id_rsa -p 2222 dave@192.168.199.201
```
- If public key authentication is disabled or you don’t have a key, try `keyboard-interactive` mode explicitly:
```bash
ssh -o PreferredAuthentications=keyboard-interactive,password -p 2222 dave@192.168.199.201
``` 

#### 4. **Check SSH Configuration on Target
- If you have access to another account or can check logs on the target machine, verify SSH settings:
```bash
cat /etc/ssh/sshd_config | grep -i "passwordauthentication"
```
- If `PasswordAuthentication no`, then password login is disabled.
	- To enable it:
```bash
sudo sed -i 's/^PasswordAuthentication no/PasswordAuthentication yes/' /etc/ssh/sshd_config
sudo systemctl restart sshd
```

#### 5. **Brute-Force or Bypass
- If you suspect an incorrect password, use `hydra` or `medusa` for brute-forcing.
- If you already have a foothold on another user account, try **privilege escalation** or **pivoting**.

#### 6. **Try Another User**
- If `dave` is locked out or restricted, try logging in with a different user.

---

## SSH

> Source: `01101100-C0D3X-00110110.md` → `CLEAR CMD RUNMRU? > SSH`

```
sed -r 's/\s+//g' users.txt file
```
```
ssh seppuku@192.168.177.90 -t "bash --noprofile"
```
```
ssh -i root root@127.0.0.1 -o IdentitiesOnly=yes
```

Steal /home/user/.ssh/id\_rsa and login with it to the target (cracking passphrase could be required! & chmod 400 id\_rsa)

💡 Note that there could be other encryption then RSA:

By default, SSH searches for `id_rsa`, `id_dsa`, `id_ecdsa`, `id_ecdsa_sk`, `id_ed25519`, `id_ed25519_sk`

More information could be extracted from **/etc/ssh/ssh\_config & /etc/ssh/sshd\_config**

