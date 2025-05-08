# 🔐 Secure Secrets with SOPS + Age + direnv

This is a step-by-step guide to encrypt, manage, and load environment secrets safely in a project using:

- [Mozilla SOPS](https://github.com/getsops/sops) — for encrypting structured config files
- [Age](https://github.com/FiloSottile/age) — a modern, simple, secure encryption tool
- [direnv](https://direnv.net) — a tool that automatically loads environment variables per project

---

## 🧩 Tools Overview

| Tool     | Purpose                                               |
|----------|--------------------------------------------------------|
| `sops`   | Encrypts/decrypts secrets in structured files          |
| `age`    | Provides fast and secure encryption (replacing GPG)   |
| `direnv` | Automatically loads secrets into your shell            |
| Git      | Stores only encrypted secrets, never plaintext         |

---

## ✅ Step 1: Install the Tools

### 1. Install `sops`

For macOS:

```bash
brew install sops
```

For Ubuntu/Debian:

```bash
sudo apt update
sudo apt install sops
```

Verify it works:

```bash
sops --version
```

---

### 2. Install `age`

For macOS:

```bash
brew install age
```

For Ubuntu/Debian:

```bash
sudo apt install age
```

Verify:

```bash
age --version
```

---

## ✅ Step 2: Generate Your Age Key Pair

### 📁 Create your Age key files

```bash
mkdir -p ~/.config/age
cd ~/.config/age
age-keygen -o key.txt
```

This creates a file `key.txt` with contents like:

```
# created: 2025-05-08T12:00:00+03:00
# public key: age1qqe...yourpublickey...
AGE-SECRET-KEY-1VY...yourprivatekey...
```

### 📤 Extract the public key

```bash
grep "public key" key.txt | cut -d' ' -f4 > public.txt
```

Set safe permissions:

```bash
chmod 600 key.txt
```

You now have:

- `key.txt`: your **private** Age key (never share this!)
- `public.txt`: your **public** Age key (used to encrypt)

---

## ✅ Step 3: Create and Encrypt Secrets

### Step-by-step

1. Create the secrets directory:

```bash
mkdir -p secrets
```

2. Create a `.env`-style file with sensitive values:

```bash
echo 'API_KEY=your-production-api-key' > secrets/secrets.env
```

3. Encrypt the file with `sops`:

```bash
sops --age $(cat ~/.config/age/public.txt) -e secrets/secrets.env > secrets/secrets.env.enc
```

4. Securely delete the plaintext:

```bash
shred -u secrets/secrets.env
```

✅ You now only have:

- `secrets/secrets.env.enc` (safe to commit to Git)

---

## ✅ Step 4: Set Up `.envrc` to Load Secrets Automatically

Create a file called `.envrc` in your project root with the following:

```bash
# -----------------------------------------------------------------------------
# File: .envrc
# Description: Automatically load encrypted secrets using SOPS + Age
# -----------------------------------------------------------------------------
# ⚠️ Run `direnv allow` once to enable this for the project
# -----------------------------------------------------------------------------

# Add local code to PYTHONPATH if needed
export PYTHONPATH="./src"

# Activate local virtual environment if present
if [[ -d .venv ]]; then
  layout python .venv/bin/python
fi

# Securely load encrypted secrets
SECRET_FILE="secrets/secrets.env.enc"
TMP_FILE=".env.secrets.tmp"

if [[ -f "$SECRET_FILE" ]]; then
  sops -d "$SECRET_FILE" > "$TMP_FILE"
  source_env "$TMP_FILE"
  rm "$TMP_FILE"
else
  echo "🔐 Encrypted secrets file not found: $SECRET_FILE"
fi
```

Then run:

```bash
direnv allow
```

This activates the `.envrc` and decrypts your secrets securely.

---

## ✅ Step 5: Create `.sops.yaml` for Automatic Encryption

This file tells `sops` what files to encrypt and with which keys.

Create `.sops.yaml` in the root of your project:

```yaml
# .sops.yaml
creation_rules:
  - path_regex: secrets/.*\.env
    age:
      - age1qqe...yourpublickeyfromstep2...
```

💡 You can insert the public key directly like this:

```bash
echo "  - $(cat ~/.config/age/public.txt)" >> .sops.yaml
```

Now any matching `.env` files in `secrets/` will be encrypted with:

```bash
sops -e secrets/db.env > secrets/db.env.enc
```

---

## ✅ Step 6: Add to `.gitignore`

Never commit plaintext secrets. Add this to `.gitignore`:

```gitignore
# Do not commit unencrypted secrets
secrets/*.env
.env.secrets.tmp
```

✅ You *can and should commit*:

- `secrets/secrets.env.enc`
- `.sops.yaml`
- `.envrc`

---

## ✅ Step 7: Shell Integration with `direnv`

- `direnv` automatically loads when you enter your project folder
- It will decrypt `secrets.env.enc`
- It loads all secret variables into your shell (e.g. `$API_KEY`)
- It then deletes the temporary plaintext file

This keeps your secrets:

- Loaded when needed
- Encrypted at rest
- Ignored by Git
- Invisible to other processes

---

## ✅ Advanced Usage: Multi-Key or Rotation

### 🔄 Rotate the secret to a new public key

```bash
sops -r --age age1newkey... secrets/secrets.env.enc
```

### 👥 Encrypt for multiple recipients (team sharing)

Update `.sops.yaml` like this:

```yaml
creation_rules:
  - path_regex: secrets/.*\.env
    age:
      - age1yourkey...
      - age1teammatekey...
```

---

## ✅ Final Summary

| File                         | Purpose                               | Commit? |
|------------------------------|----------------------------------------|---------|
| `secrets/secrets.env.enc`    | Encrypted secrets                     | ✅ Yes  |
| `.envrc`                     | Loads decrypted secrets into env      | ✅ Yes  |
| `.sops.yaml`                 | SOPS auto-encryption config           | ✅ Yes  |
| `secrets/secrets.env`        | Plaintext (temporary)                 | ❌ No   |
| `.env.secrets.tmp`           | Temp decrypted copy (auto-removed)    | ❌ No   |

---

## 🧪 Final Check

In your terminal:

```bash
cd your-project/
direnv reload
echo $API_KEY
```

---

## 🛠️ Bonus: Justfile Recipe

```Justfile
# -----------------------------------------------
# Secure Secrets with SOPS + Age
# -----------------------------------------------
[group("Secrets")]
init-secrets:
    @echo "🔐 Initializing secrets setup..."
    mkdir -p secrets
    echo "API_KEY=your-production-api-key" > secrets/secrets.env
    echo "creation_rules:" > .sops.yaml
    echo "  - path_regex: secrets/.*\\.env" >> .sops.yaml
    echo "    age:" >> .sops.yaml
    echo "      - $(cat ~/.config/age/public.txt)" >> .sops.yaml
    sops --age $(cat ~/.config/age/public.txt) -e secrets/secrets.env > secrets/secrets.env.enc
    shred -u secrets/secrets.env
    @echo "✅ secrets/secrets.env.enc created and .sops.yaml written"
```

---

If all is configured correctly, you'll see your decrypted secret value.

You're now ready to use encrypted secrets securely in your workflow.
