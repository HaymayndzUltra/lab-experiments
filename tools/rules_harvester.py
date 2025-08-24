#!/usr/bin/env python3
import os, time, hashlib, re, json
from urllib.parse import urljoin, urlparse
import urllib.request
import urllib.error
import ssl
from bs4 import BeautifulSoup
from datetime import datetime

SEEDS_FILE = "tools/rules_seeds.txt"
OUTDIR = ".cursor/rules/harvested"
INDEX = os.path.join(OUTDIR, "_index.json")
os.makedirs(OUTDIR, exist_ok=True)

HEADERS = {"User-Agent": "TeteyHarvester/1.0 (+local)"}
RATE_SEC = 1.0  # polite crawl

def load_seeds():
    with open(SEEDS_FILE, "r", encoding="utf-8") as f:
        return [ln.strip() for ln in f if ln.strip() and not ln.startswith("#")]

def get(url):
    for attempt in range(3):
        try:
            # Create SSL context that's more permissive
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=10, context=context) as response:
                if response.status == 200:
                    content = response.read().decode('utf-8')
                    return content
                time.sleep(2)
        except Exception as e:
            print(f"[WARN] Error on attempt {attempt + 1} for {url}: {e}")
            time.sleep(2)
    print(f"[ERROR] Failed to fetch {url} after 3 attempts")
    return ""

def discover_rule_links(html, base):
    soup = BeautifulSoup(html, "html.parser")
    links = set()
    for a in soup.find_all("a", href=True):
        href = urljoin(base, a["href"])
        if urlparse(href).netloc.endswith("cursor.directory"):
            # Look for both category pages and individual rule pages
            if "/rules/" in href or "/data-" in href or "/cursor-rules" in href:
                links.add(href.split("#")[0])
    return links

def slugify(title):
    s = re.sub(r"[^a-zA-Z0-9\- ]+", "", title).strip().lower().replace(" ", "-")
    return s[:90] or "untitled"

def extract_title_body(html):
    soup = BeautifulSoup(html, "html.parser")
    
    # Look for the specific code block that contains the rules
    code_block = soup.find("code", class_="text-sm block pr-3")
    if code_block:
        # Extract title from the page
        h = soup.find(["h1","h2","title"])
        title = (h.get_text(" ", strip=True) if h else "Untitled Rule")
        
        # Get content from the code block
        body = code_block.get_text("\n", strip=True)
        return title, body
    
    # Fallback to old method if no code block found
    h = soup.find(["h1","h2","title"])
    title = (h.get_text(" ", strip=True) if h else "Untitled Rule")
    main = soup.find(["main","article"]) or soup
    lines = []
    for tag in main.find_all(["p","li"]):
        t = tag.get_text(" ", strip=True)
        if t: lines.append(t)
    body = "\n".join(lines)
    return title, body

def norm_text(s: str) -> str:
    return " ".join(s.lower().split())

def mdc_from(url, title, body):
    normalized = norm_text(body)
    h = hashlib.sha1(normalized.encode()).hexdigest()
    bullets = [f"- {ln}" for ln in body.split("\n") if ln.strip()]
    bullets = bullets[:20]  # trim noise
    today = datetime.utcnow().strftime("%Y-%m-%d")
    mdc = f"""%% source_url: {url}
%% last_fetched: {today}
%% tags: [harvested, review_required]
%% hash: {h}

# {title}

[INTENT]
- planning

[GUARDRAILS]
- Do not override CORE rules.
- Suggestions only; require user approval.

[INSTRUCTIONS]
{chr(10).join(bullets)}
"""
    return h, mdc

def load_index():
    if os.path.exists(INDEX):
        with open(INDEX, "r", encoding="utf-8") as f: return json.load(f)
    return {"entries": []}

def save_index(ix):
    with open(INDEX, "w", encoding="utf-8") as f: json.dump(ix, f, indent=2)

def already_have(ix, h):
    return any(e.get("hash")==h for e in ix["entries"])

def main():
    print("[INFO] Starting harvester...")
    ix = load_index()
    print(f"[INFO] Loaded index with {len(ix['entries'])} existing entries")
    visited, queue = set(), set(load_seeds())
    print(f"[INFO] Loaded {len(queue)} seed URLs")
    seen_hashes = set(e["hash"] for e in ix["entries"])

    max_iterations = 100  # Increased significantly to allow more harvesting
    iteration = 0

    while queue and iteration < max_iterations:
        iteration += 1
        if iteration % 10 == 0:
            print(f"[INFO] Progress: {iteration}/{max_iterations}, Queue size: {len(queue)}")
        url = queue.pop()
        if url in visited: continue
        visited.add(url)

        html = get(url); time.sleep(RATE_SEC)
        if not html: continue

        discovered_links = discover_rule_links(html, url)
        print(f"[INFO] Discovered {len(discovered_links)} links from {url}")
        
        # Only add a limited number of links to prevent queue explosion
        added_count = 0
        for link in discovered_links:
            if link not in visited and added_count < 3 and len(queue) < 50:  # Limit additions
                queue.add(link)
                added_count += 1

        # Try to harvest content from any page that might contain rules
        if "/rules/" in url or "/data-" in url or "/cursor-rules" in url:
            title, body = extract_title_body(html)
            # Check if we found content in the code block (indicates actual rule content)
            if len(body) > 100 and "You are an expert" in body:  # Look for rule signature
                h, mdc = mdc_from(url, title, body)
                if h in seen_hashes: continue
                seen_hashes.add(h)
                outpath = os.path.join(OUTDIR, f"{slugify(title)}.mdc")
                with open(outpath, "w", encoding="utf-8") as f:
                    f.write(mdc)
                ix["entries"].append({"title": title, "url": url, "hash": h, "file": outpath})
                print(f"[saved] {title} -> {outpath}")
            elif len(body) > 100:
                print(f"[INFO] Found content but not a rule: {title} ({len(body)} chars)")

    save_index(ix)
    print(f"[done] total harvested: {len(ix['entries'])}")

if __name__ == "__main__":
    main()
