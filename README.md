# TCP Dictionary Server

A Python socket-programming coursework project comparing three ways to handle dictionary lookup clients.

| Server | Strategy | Platform |
|---|---|---|
| `server1.py` | One connected client at a time | Python 3 |
| `server2.py` | A forked child process per client | Unix-like system; `os.fork()` required |
| `server3.py` | Multiple clients using `select()` | Python 3 |

## Run

Run from the repository root. Start one server, then a client in another terminal:

```bash
python3 server1.py 5000
python3 client.py 127.0.0.1 5000
```

Substitute `server2.py` or `server3.py` to compare concurrency approaches. Try `apple`, `computer`, `dog`, and a missing word. Stop with Ctrl+C.

## Protocol

The server sends a definition followed by `<END>`. The client accumulates received bytes until the marker arrives. This handles responses split across multiple TCP reads.

## Demo data and limits

A small original dictionary fixture is included instead of redistributing the original third-party dictionary. Add words by editing `dictionary/dictionary.json`.

This is a learning prototype: requests do not have robust stream framing, and authentication, encryption, and production hardening are not implemented. Use local demo connections.

## Background

UMBC CMSC 481 socket programming coursework. The server and client implementations are preserved from the uploaded project.
