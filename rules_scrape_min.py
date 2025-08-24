#!/usr/bin/env python3
# Minimal: scrape Cursor Directory /rules → save local .mdc files
# Output dir: harvested_rules/  (walang auto-apply sa Cursor)

import os, time, re, hashlib
from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup

SEEDS = [
    "https://cursor.directory/rules",
    "https://cursor.directory/rules/popular",
    "https://cursor.directory/rules/official",
]
OUTDIR = "harvested_rules"
os.makedirs(OUTDIR, exist_ok=True)

HEADERS = {"User-Agent": "TeteyHarvester/1.0 (+local)"}
RATE = 1.0  # 1 req/sec (polite)

def get(url):
    for _ in range(3):
        r = requests.get(url, headers=HEADERS, timeout=25)
        if r.status_code == 200: return r.text
        time.sleep(2)
    return ""

def discover_links(html, base):
    soup = BeautifulSoup(html, "html.parser")
    links = set()
    for a in soup.find_all("a", href=True):
        href = urljoin(base, a["href"])
        if urlparse(href).netloc.endswith("cursor.directory") and "/rules/" in href:
            links.add(href.split("#")[0])
    return links

def slugify(t):
    return re.sub(r"[^a-zA-Z0-9\- ]+","",t).strip().lower().replace(" ","-")[:90] or "untitled"

def extract_title_body(html):
    soup = BeautifulSoup(html, "html.parser")
    h = soup.find(["h1","h2","title"])
    title = (h.get_text(" ", strip=True) if h else "Untitled Rule")
    main = soup.find(["main","article"]) or soup
    lines = []
    for tag in main.find_all(["p","li"]):
        t = tag.get_text(" ", strip=True)
        if t: lines.append(t)
    body = "\n".join(lines)
    return title, body

def norm(s): return " ".join(s.lower().split())

def to_mdc(url, title, body):
    h = hashlib.sha1(norm(body).encode()).hexdigest()
    bullets = [f"- {ln}" for ln in body.split("\n") if ln.strip()][:20]
    return h, f"""%% source_url: {url}
%% last_fetched: (local)
%% tags: [harvested, review_required]
%% hash: {h}

# {title}

[INSTRUCTIONS]
{chr(10).join(bullets)}
"""

def main():
    visited, queue, seen_hash = set(), set(SEEDS), set()
    while queue:
        url = queue.pop()
        if url in visited: continue
        visited.add(url)

        html = get(url); time.sleep(RATE)
        if not html: continue

        # discover more /rules/* links
        for link in discover_links(html, url):
            if link not in visited: queue.add(link)

        # save only deeper /rules/* pages (likely detail pages)
        if "/rules/" in url and url.count("/") >= 4:
            title, body = extract_title_body(html)
            if len(body) < 60:  # skip sobrang ikli
                continue
            h, mdc = to_mdc(url, title, body)
            if h in seen_hash:  # dedupe within this run
                continue
            seen_hash.add(h)
            path = os.path.join(OUTDIR, f"{slugify(title)}.mdc")
            with open(path, "w", encoding="utf-8") as f:
                f.write(mdc)
            print(f"[saved] {title} -> {path}")

if __name__ == "__main__":
    main()
