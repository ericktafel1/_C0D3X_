# _SCR0LL_ Operator Vault

This vault is a rebuilt operator reference derived from the `_C0D3X_` source archive and normalized for real-world offensive pentesting use.

## What changed

- Removed obvious duplication and near-duplication where the same command blocks or topic fragments appeared in multiple places.
- Re-centered files around the place an operator would naturally look first instead of preserving source sprawl.
- Split service-specific material into `06 Services` pages and kept host/domain workflow material in the relevant platform folder.
- Moved payload and exploit-development helper material from the original `11-RE-and-xpDev` bucket into `10 Tool Box`.
- Added top-level review artifacts so the editorial decisions are visible and auditable.

## Folder map

- `01 Enumeration` — broad recon, host discovery, scanning, first-pass service identification
- `02 Web` — web workflows by bug class or objective
- `03 AD` — domain workflows, Kerberos, BloodHound/ACLs/AD CS, lateral movement and replication
- `04 Windows` — host enumeration, PowerShell, privesc, host-focused tradecraft
- `05 Linux` — host enumeration, shell handling, privesc
- `06 Services` — one file per service or protocol/topic
- `07 Creds and Cracking` — cracking, spraying, reuse, wordlists, hash handling
- `08 Post Exploitation` — secrets, looting, persistence, cleanup
- `09 Movement` — transfers, pivots, tunnels, Ligolo-ng
- `10 Tool Box` — payloads, helper snippets, compact operator utilities, curated references
- `12 Cloud` — AWS plus container/Kubernetes follow-up

## Usage philosophy

- Start broad, then narrow fast.
- Prefer the page that matches the protocol or the host/domain objective you are actually working.
- Use `06 Services` for service mechanics and `03 AD` / `04 Windows` / `05 Linux` for environment-specific decision support.
- Keep grep and editor search as the primary interface; headings were normalized to stay grep-friendly.
- Legacy syntax is retained only when it still helps operator searchability or when old environments still appear in the field.

## Editorial conventions

- Markdown only.
- Commands stay in fenced blocks where possible.
- “See also” is preferred over copy/paste duplication across files.
- Short context notes are included only when they materially improve operator decision-making.
- Low-signal placeholders, empty files, and obvious junk fragments were removed instead of being preserved for completeness theater.

## Search tips

Search by:
- protocol or port: `mssql`, `ldap`, `445`, `5985`, `kerberos`
- workflow term: `kerberoast`, `xp_cmdshell`, `AlwaysInstallElevated`, `ligolo`, `LAPS`, `BloodHound`
- access method: `evil-winrm`, `xfreerdp`, `psexec`, `proxychains`, `ssh -D`
