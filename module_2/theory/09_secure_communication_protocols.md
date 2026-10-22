*Module 2 · Part B: Security in Distributed Systems*

# 9. Secure Communication Protocols

## Putting the pieces together

Encryption, MACs, signatures, and certificates are building blocks. A **secure communication protocol** is a precise recipe for combining them so two machines can talk safely over a network they don't trust. Designing these recipes is notoriously hard — many protocols that looked correct turned out to have subtle flaws — which is why real systems use a small number of well-studied protocols instead of inventing their own.

> **Simple analogy:** Before a diplomatic meeting, both sides check each other's credentials, agree on a private interpreter only they understand, and agree that every page of notes will be signed. Only then does the real conversation start. A secure protocol is that pre-meeting ritual, done in milliseconds before every connection.

## TLS (Transport Layer Security)

The most important one to know by name is **TLS** — the protocol behind the padlock icon in a browser's address bar, and the thing that makes HTTPS secure. It sits on top of TCP, so any program using ordinary sockets (like the ones you wrote in Module 1, [Lab 03](../../module_1/labs/lab_03_tcp_ip_sockets/)) can add it. At a conceptual level, a TLS 1.3 handshake does three things before any real data is sent:

1. **Agrees on a shared secret key.** Client and server exchange public values for a **Diffie-Hellman key agreement** ([topic 8](08_encryption.md)), using fresh values for every connection, and each side computes the same symmetric key without it ever crossing the network.
2. **Authenticates the server** (and optionally the client). The server sends its **certificate** — a document issued by a trusted Certificate Authority stating "this public key belongs to www.example.com" — and *signs* the handshake with the matching private key, proving it really holds that key and that nobody in the middle altered the handshake.
3. **Switches to fast symmetric encryption** for the actual conversation, where every record also carries an integrity check, so any tampering in transit is detected.

Because a fresh key is used for each connection and thrown away afterwards, TLS 1.3 has **forward secrecy**: even if the server's private key is stolen years later, recorded past conversations can't be decrypted.

The handshake only protects you if the certificate is actually checked. The client must verify that the certificate chains up to a Certificate Authority it trusts, that the name on it matches the server it meant to reach, and that it hasn't expired or been revoked. Skipping these checks — a surprisingly common bug, often "just for testing" — silently turns TLS into a protocol that encrypts traffic perfectly while sending it straight to a man-in-the-middle.

Python's standard library does all of this for you:

```python
import socket, ssl

host = "www.python.org"
context = ssl.create_default_context()        # verifies certificate and hostname

with socket.create_connection((host, 443)) as sock:
    with context.wrap_socket(sock, server_hostname=host) as tls:
        print(tls.version())                  # e.g. TLSv1.3
        cert = tls.getpeercert()
        print(cert["subject"])                # who the certificate is for
        print(cert["issuer"])                 # which Certificate Authority vouched for it
        print(cert["notAfter"])               # expiry date
```

Compare this to Lab 03: the socket is created exactly the same way, and `wrap_socket` is the only step that adds encryption, integrity, and server authentication.

## Mutual TLS (mTLS)

In ordinary TLS, only the server proves its identity; the client is usually authenticated afterwards with a password or token. In **mutual TLS**, both sides present certificates during the handshake. This is the standard way microservices authenticate each other inside a data center ([topic 6](06_authentication.md)), and it is a core building block of Zero Trust networks ([topic 11](11_trust_management.md)).

## SSH

**SSH (Secure Shell)** protects remote logins and file transfers (`ssh`, `scp`, `git` over SSH). It uses the same building blocks as TLS but a different trust model: instead of Certificate Authorities, the first time you connect to a server your client shows you the server's key fingerprint and asks whether to trust it, then remembers it in `~/.ssh/known_hosts`. This is called **trust on first use**. If the key ever changes, SSH warns you loudly — because that's exactly what a man-in-the-middle would look like.

## IPsec and VPNs

**IPsec** works at the network layer, below TCP, so it protects *all* traffic between two machines or two networks without any application having to change. It's the basis of many site-to-site **VPNs** that connect a company's branch offices into one private network over the public internet.

| Protocol | Layer | Protects | Trust model | Typical use |
|---|---|---|---|---|
| TLS | Above TCP | One application's connection | Certificate Authorities | HTTPS, APIs, email, databases |
| mTLS | Above TCP | Both directions of a connection | Certificates on both sides | Microservices, Zero Trust |
| SSH | Above TCP | Remote shell, file transfer | Trust on first use | Server administration, git |
| IPsec | Network (IP) | All traffic between two hosts or networks | Pre-shared keys or certificates | Site-to-site VPNs |

## Case Study: Heartbleed (2014)

TLS also has a small "heartbeat" feature: one side sends a message saying "here are 5 bytes, send them back to show you're alive." In 2014, researchers found that OpenSSL — the library behind a large share of the world's HTTPS servers — trusted the *length* the sender claimed without checking it against how much data had actually arrived. An attacker could send 1 byte while claiming 64 kilobytes, and the server would reply with 64 kilobytes of its own memory: often containing passwords, session cookies, and sometimes the server's private TLS key itself. Roughly half a million trusted HTTPS servers were estimated to be vulnerable when it was announced.

This is precisely the bug planted on purpose in the custom protocol you built in Lab 03, Part 3: trusting a `LENGTH` field sent by the client. A protocol whose cryptography is perfectly sound can still be completely broken by a one-line parsing mistake in its implementation.

---

← [8. Encryption](08_encryption.md) · [Contents](README.md) · [10. Access Control](10_access_control.md) →
