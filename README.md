# 📂 Directory Bruteforcer


## Get this repository

Clone the current project (this repository's canonical GitHub URL), then follow the installation and usage steps below.

```bash
git clone https://github.com/cyberworlduniversity/directory_bruteforcer.git
cd directory_bruteforcer
```

> **Tool #14** in the Ethical Hacking Toolkit  
> 👤 Author: **hemanathan115**  
> 🔗 GitHub: [https://github.com/hemanathan115](https://github.com/hemanathan115)

---

## 📌 Description

**Directory Bruteforcer** is a Python-based web reconnaissance tool that discovers hidden directories and files on a web server by sending HTTP requests using a wordlist. It reports status codes to identify accessible, forbidden, or redirected paths.

This tool is built for **ethical hacking**, **CTF challenges**, and **authorized penetration testing** only.

---

## ⚙️ Features

- ✅ Multithreaded scanning for fast results
- ✅ Built-in default wordlist (no setup required)
- ✅ Custom wordlist support
- ✅ File extension brute-forcing (`.php`, `.html`, `.txt`, etc.)
- ✅ Color-coded HTTP response output
- ✅ Real-time progress bar
- ✅ Results summary at the end
- ✅ Save output to a file (`-o`)
- ✅ Generate a wordlist file (`--gen-wordlist`)
- ✅ Configurable timeout and thread count

---

## 🖥️ Requirements

- Python 3.7+
- `requests` library

Install dependencies:

```bash
pip install requests
```

---

## 🚀 Usage

### Basic Scan (uses built-in wordlist)

```bash
python directory_bruteforcer.py -u http://example.com
```

### With Custom Wordlist

```bash
python directory_bruteforcer.py -u http://example.com -w wordlist.txt
```

### With File Extensions

```bash
python directory_bruteforcer.py -u http://example.com -x php,html,txt
```

### With More Threads & Timeout

```bash
python directory_bruteforcer.py -u http://example.com -t 20 --timeout 3
```

### Save Results to File

```bash
python directory_bruteforcer.py -u http://example.com -o results.txt
```

### Show All Results (including 404s)

```bash
python directory_bruteforcer.py -u http://example.com --show-all
```

### Generate a Default Wordlist

```bash
python directory_bruteforcer.py --gen-wordlist my_wordlist.txt
```

---

## 🧩 Arguments

| Flag              | Description                                      | Default  |
|-------------------|--------------------------------------------------|----------|
| `-u`, `--url`     | Target URL (e.g. `http://example.com`)           | Required |
| `-w`, `--wordlist`| Path to wordlist file                            | Built-in |
| `-t`, `--threads` | Number of concurrent threads                     | `10`     |
| `-x`, `--extensions` | Comma-separated file extensions to test       | None     |
| `--timeout`       | HTTP request timeout (seconds)                   | `5`      |
| `--show-all`      | Show all results including 404s                  | Off      |
| `-o`, `--output`  | Save scan results to a text file                 | None     |
| `--gen-wordlist`  | Generate a default wordlist and save to file     | None     |

---

## 🎨 Output Color Guide

| Color  | Meaning                     |
|--------|-----------------------------|
| 🟢 Green  | Found (200, 201, 204)    |
| 🟡 Yellow | Redirect / Forbidden (301, 302, 403, 401) |
| 🔴 Red    | Not Found / Error (404, 500, 503) |

---

## 📂 Project Structure

```
directory_bruteforcer/
├── directory_bruteforcer.py   # Main tool script
├── wordlist.txt               # (Optional) Custom wordlist
└── README.md                  # Documentation
```

---

## 🔐 Legal Disclaimer

> ⚠️ This tool is intended **only for authorized testing and educational purposes**.  
> Do **NOT** use it against systems without **explicit written permission**.  
> The author is **not responsible** for any misuse or damage caused by this tool.  
> Always follow your country's cybersecurity laws and ethical guidelines.

---

## 🌐 Part of the Ethical Hacking Toolkit

This is **Tool #14** in a growing collection of Python-based security tools by [hemanathan115](https://github.com/hemanathan115).

| # | Tool Name |
|---|-----------|
| 14 | 📂 Directory Bruteforcer ← *You are here* |

---

## ⭐ Show Support

If this tool helped you, please ⭐ **star the repo** on GitHub!

```
https://github.com/hemanathan115
```
