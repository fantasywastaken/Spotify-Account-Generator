# Spotify Account Generator

<img src="https://i.imgur.com/VlyOQ7X.png" width="1000px">

A fast, multithreaded Spotify account generator written in Python. Creates accounts via Spotify's v1 signup API with randomized credentials.

---

### ⚙️ How It Works

- Sends HTTP requests to Spotify's `v1/account` signup endpoint using `httpx`.
- Generates random usernames, passwords, emails and birthdays for each account.
- Supports multithreading for high-speed mass account creation.
- Optional rotating proxy support to avoid IP-based rate limiting.
- Created accounts are saved to `accounts.txt` in `username:email:password` format.

---

## 📁 Setup

### 1. Install Dependencies

```
pip install httpx colorama
```

### 2. Configuration

Edit `config.json` in the project root:

```json
{
    "threads": 3,
    "target": 10,
    "proxy": {
        "enabled": false,
        "host": "proxy.example.com",
        "port": 6060,
        "username": "",
        "password": ""
    }
}
```

| Option | Description |
|---|---|
| `threads` | Number of concurrent threads |
| `target` | Number of accounts to create (0 = unlimited) |
| `proxy.enabled` | Enable/disable rotating proxy |
| `proxy.host` | Proxy hostname |
| `proxy.port` | Proxy port |
| `proxy.username` | Proxy auth username (optional) |
| `proxy.password` | Proxy auth password (optional) |

---

### 🚀 Usage

```
python main.py
```

Output:
```
  [+] Scout_Ykaxon | mx7z5ixe@fastmail.com  (02:33:56)
  [+] Daydream_Uvecut | r84lg@gmail.com  (02:34:01)
  ...

  Done! 10 accounts saved to accounts.txt
```

Created accounts are saved to `accounts.txt`:
```
Scout_Ykaxon:mx7z5ixe@fastmail.com:aB3kd9Fj2mXq!7
```

---

### 🛡️ Notes

- If you receive `status=320` errors, your IP may be flagged. Enable a rotating proxy or wait before retrying.
- Proxy is optional. The tool works without it, but may hit rate limits on high thread counts.
- Randomized User-Agent headers are used to minimize detection.

---

### ⚠️ Disclaimer

This project has been developed for educational and research purposes only. Unauthorized access to any service or system is illegal and strictly prohibited. The developer is not responsible for any misuse of this tool.
