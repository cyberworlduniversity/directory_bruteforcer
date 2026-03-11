#!/usr/bin/env python3
"""
Directory Bruteforcer Tool
Author: hemanathan115
GitHub: https://github.com/hemanathan115
Description: Finds hidden directories on a web server using a wordlist and checks HTTP responses.
"""

import requests
import argparse
import sys
import time
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from urllib.parse import urljoin

# ─────────────────────────────────────────────
# ANSI Colors
# ─────────────────────────────────────────────
GREEN   = "\033[92m"
RED     = "\033[91m"
YELLOW  = "\033[93m"
CYAN    = "\033[96m"
WHITE   = "\033[97m"
RESET   = "\033[0m"
BOLD    = "\033[1m"

BANNER = f"""
{CYAN}{BOLD}
██████╗ ██╗██████╗      ██████╗ ██████╗ ██╗   ██╗████████╗███████╗
██╔══██╗██║██╔══██╗    ██╔══██╗██╔══██╗██║   ██║╚══██╔══╝██╔════╝
██║  ██║██║██████╔╝    ██████╔╝██████╔╝██║   ██║   ██║   █████╗  
██║  ██║██║██╔══██╗    ██╔══██╗██╔══██╗██║   ██║   ██║   ██╔══╝  
██████╔╝██║██║  ██║    ██████╔╝██║  ██║╚██████╔╝   ██║   ███████╗
╚═════╝ ╚═╝╚═╝  ╚═╝    ╚═════╝ ╚═╝  ╚═╝ ╚═════╝    ╚═╝   ╚══════╝
{RESET}
{WHITE}       📂 Directory Bruteforcer — Web Recon Tool{RESET}
{YELLOW}       GitHub : https://github.com/hemanathan115{RESET}
{CYAN}       Tool #14 in the Ethical Hacking Kit{RESET}
{'─'*60}
"""

# ─────────────────────────────────────────────
# Status Code Descriptions
# ─────────────────────────────────────────────
STATUS_INFO = {
    200: (GREEN,  "✅ FOUND"),
    201: (GREEN,  "✅ CREATED"),
    204: (GREEN,  "✅ NO CONTENT"),
    301: (YELLOW, "↪  REDIRECT"),
    302: (YELLOW, "↪  REDIRECT"),
    403: (YELLOW, "🔒 FORBIDDEN"),
    401: (YELLOW, "🔐 UNAUTHORIZED"),
    404: (RED,    "❌ NOT FOUND"),
    500: (RED,    "💥 SERVER ERROR"),
    503: (RED,    "🚫 UNAVAILABLE"),
}

DEFAULT_WORDLIST = [
    "admin", "administrator", "login", "dashboard", "panel",
    "backup", "config", "uploads", "images", "files", "data",
    "api", "v1", "v2", "static", "assets", "media", "css", "js",
    "private", "secret", "hidden", "internal", "dev", "test",
    "staging", "beta", "old", "archive", "logs", "log",
    "db", "database", "sql", "phpmyadmin", "wp-admin",
    "wp-login", "wordpress", "drupal", "joomla", "cpanel",
    "webmail", "mail", "email", "portal", "user", "users",
    "account", "accounts", "profile", "register", "signup",
    "download", "downloads", "upload", "tmp", "temp", "cache",
    "shell", "cmd", "exec", "cgi-bin", "scripts", ".git",
    ".env", ".htaccess", "robots.txt", "sitemap.xml", "readme",
]

found_results = []


def normalize_url(url: str) -> str:
    if not url.startswith(("http://", "https://")):
        url = "http://" + url
    return url.rstrip("/")


def check_directory(base_url: str, word: str, timeout: int, extensions: list) -> list:
    results = []
    paths = [word] + [f"{word}.{ext}" for ext in extensions]

    for path in paths:
        full_url = f"{base_url}/{path}"
        try:
            resp = requests.get(full_url, timeout=timeout, allow_redirects=False,
                                headers={"User-Agent": "Mozilla/5.0 DirBruteforcer/1.0"})
            code = resp.status_code
            color, label = STATUS_INFO.get(code, (WHITE, f"[{code}]"))
            results.append((full_url, code, color, label))
        except requests.ConnectionError:
            pass
        except requests.Timeout:
            results.append((full_url, 0, RED, "⏱ TIMEOUT"))
        except Exception:
            pass
    return results


def load_wordlist(path: str) -> list:
    if not os.path.isfile(path):
        print(f"{RED}[!] Wordlist file not found: {path}{RESET}")
        sys.exit(1)
    with open(path, "r", errors="ignore") as f:
        words = [line.strip() for line in f if line.strip() and not line.startswith("#")]
    return words


def run_bruteforce(url, wordlist, threads, timeout, extensions, show_all, output_file):
    base_url = normalize_url(url)
    total = len(wordlist)
    scanned = 0
    start_time = time.time()

    print(f"\n{CYAN}[*] Target   : {WHITE}{base_url}{RESET}")
    print(f"{CYAN}[*] Words    : {WHITE}{total}{RESET}")
    print(f"{CYAN}[*] Threads  : {WHITE}{threads}{RESET}")
    print(f"{CYAN}[*] Timeout  : {WHITE}{timeout}s{RESET}")
    print(f"{CYAN}[*] Extensions: {WHITE}{extensions or 'none'}{RESET}")
    print(f"{CYAN}[*] Started  : {WHITE}{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{RESET}")
    print(f"{'─'*60}\n")

    out_lines = []

    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = {
            executor.submit(check_directory, base_url, word, timeout, extensions): word
            for word in wordlist
        }
        for future in as_completed(futures):
            results = future.result()
            scanned += 1
            for full_url, code, color, label in results:
                if show_all or code not in (404, 0):
                    print(f"  {color}{label:<18}{RESET} {full_url}")
                if code not in (404, 0):
                    found_results.append((full_url, code, label))
                    out_lines.append(f"{label:<18} | {code} | {full_url}")

            # Progress indicator
            pct = int((scanned / total) * 40)
            bar = f"[{'█'*pct}{'░'*(40-pct)}]"
            sys.stdout.write(f"\r{CYAN}Progress: {bar} {scanned}/{total}{RESET}  ")
            sys.stdout.flush()

    elapsed = round(time.time() - start_time, 2)
    print(f"\n\n{'─'*60}")
    print(f"{GREEN}{BOLD}[✔] Scan Complete in {elapsed}s{RESET}")
    print(f"{GREEN}[✔] Found {len(found_results)} accessible path(s){RESET}\n")

    if found_results:
        print(f"{BOLD}{'─'*60}")
        print(f"  📋 RESULTS SUMMARY")
        print(f"{'─'*60}{RESET}")
        for url_r, code, label in found_results:
            color, _ = STATUS_INFO.get(code, (WHITE, ""))
            print(f"  {color}{label:<18}{RESET} [{code}]  {url_r}")
        print()

    if output_file:
        with open(output_file, "w") as f:
            f.write(f"Directory Bruteforce Report\n")
            f.write(f"Target : {base_url}\n")
            f.write(f"Date   : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"{'─'*60}\n\n")
            f.write("\n".join(out_lines))
            f.write(f"\n\nTotal Found: {len(found_results)}\n")
        print(f"{GREEN}[✔] Results saved to: {output_file}{RESET}\n")


def generate_default_wordlist(path: str):
    with open(path, "w") as f:
        f.write("# Default wordlist generated by Directory Bruteforcer\n")
        f.write("# GitHub: https://github.com/hemanathan115\n\n")
        for word in DEFAULT_WORDLIST:
            f.write(word + "\n")
    print(f"{GREEN}[✔] Default wordlist saved to: {path}{RESET}")


def main():
    print(BANNER)

    parser = argparse.ArgumentParser(
        description="📂 Directory Bruteforcer — Find hidden directories on web servers",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("-u", "--url",        required=False, help="Target URL (e.g. http://example.com)")
    parser.add_argument("-w", "--wordlist",   default=None,   help="Path to wordlist file")
    parser.add_argument("-t", "--threads",    type=int, default=10, help="Number of threads (default: 10)")
    parser.add_argument("-x", "--extensions", default="",     help="Comma-separated extensions (e.g. php,html,txt)")
    parser.add_argument("--timeout",          type=int, default=5, help="Request timeout in seconds (default: 5)")
    parser.add_argument("--show-all",         action="store_true",  help="Show all results including 404s")
    parser.add_argument("-o", "--output",     default=None,   help="Save results to a file")
    parser.add_argument("--gen-wordlist",     default=None,   help="Generate a default wordlist file")

    args = parser.parse_args()

    # Generate wordlist mode
    if args.gen_wordlist:
        generate_default_wordlist(args.gen_wordlist)
        sys.exit(0)

    # Require URL
    if not args.url:
        parser.print_help()
        print(f"\n{RED}[!] Please provide a target URL with -u{RESET}")
        sys.exit(1)

    # Extensions
    extensions = [e.strip() for e in args.extensions.split(",") if e.strip()] if args.extensions else []

    # Wordlist
    if args.wordlist:
        wordlist = load_wordlist(args.wordlist)
    else:
        print(f"{YELLOW}[!] No wordlist provided. Using built-in default wordlist ({len(DEFAULT_WORDLIST)} words).{RESET}")
        wordlist = DEFAULT_WORDLIST

    run_bruteforce(
        url=args.url,
        wordlist=wordlist,
        threads=args.threads,
        timeout=args.timeout,
        extensions=extensions,
        show_all=args.show_all,
        output_file=args.output,
    )


if __name__ == "__main__":
    main()
