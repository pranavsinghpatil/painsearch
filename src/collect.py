"""Pain-point collector — permitted APIs only.
Sources: hn (Algolia, no key), lobsters (public json), github (public API, optional token).
No Reddit mass-scrape. Reddit = manual.

Usage:
  python src/collect.py --source hn --query "tedious workflow" --limit 20
  python src/collect.py --source lobsters --query "tedious" --limit 20
  python src/collect.py --source github --query "takes hours" --limit 20
"""
import argparse, json, os, sys, datetime, urllib.parse, urllib.request

OUT = os.path.join(os.path.dirname(__file__), "..", "evidence")

def fetch_json(url, headers=None, timeout=20):
    req = urllib.request.Request(url, headers=headers or {"User-Agent": "hackathon-discovery/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8", "replace"))

def collect_hn(query, limit):
    q = urllib.parse.quote(query)
    url = f"https://hn.algolia.com/api/v1/search?query={q}&tags=story&hitsPerPage={limit}"
    data = fetch_json(url)
    rows = []
    for h in data.get("hits", []):
        rows.append({
            "source": "hn",
            "title": h.get("title"),
            "url": h.get("url") or f"https://news.ycombinator.com/item?id={h.get('objectID')}",
            "hn_id": h.get("objectID"),
            "points": h.get("points"),
            "comments": h.get("num_comments"),
            "author": h.get("author"),
            "created": h.get("created_at"),
            "text_snippet": (h.get("story_text") or "")[:1000],
        })
    return rows

def collect_lobsters(query, limit):
    # Lobsters search via hottest.json then filter; has no full-text API, so filter client-side
    url = "https://lobste.rs/hottest.json"
    try:
        data = fetch_json(url)
    except Exception as e:
        return [{"error": f"lobsters fetch failed: {e}"}]
    q = query.lower()
    rows = []
    for s in data:
        blob = f"{s.get('title','')} {s.get('description','')} {' '.join(s.get('tags',[]))}".lower()
        if q in blob or not q:
            rows.append({
                "source": "lobsters",
                "title": s.get("title"),
                "url": s.get("url") or s.get("short_id_url"),
                "comments_url": s.get("comments_url"),
                "score": s.get("score"),
                "tags": s.get("tags"),
                "created": s.get("created_at"),
            })
        if len(rows) >= limit:
            break
    return rows

def collect_github(query, limit):
    token = os.environ.get("GITHUB_TOKEN", "")
    headers = {"User-Agent": "hackathon-discovery/1.0", "Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    q = urllib.parse.quote(f"{query} in:title,body type:issue state:open")
    url = f"https://api.github.com/search/issues?q={q}&per_page={min(limit,30)}&sort=reactions&order=desc"
    try:
        data = fetch_json(url, headers=headers)
    except Exception as e:
        return [{"error": f"github fetch failed: {e}. Set GITHUB_TOKEN if rate-limited."}]
    rows = []
    for it in data.get("items", []):
        rows.append({
            "source": "github-issues",
            "title": it.get("title"),
            "url": it.get("html_url"),
            "repo": it.get("repository_url","").split("repos/")[-1],
            "reactions": (it.get("reactions") or {}).get("total_count"),
            "comments": it.get("comments"),
            "created": it.get("created_at"),
            "body_snippet": (it.get("body") or "")[:1200],
        })
    return rows

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", choices=["hn","lobsters","github","all"], default="hn")
    ap.add_argument("--query", default="tedious workflow")
    ap.add_argument("--limit", type=int, default=20)
    a = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(os.path.join(OUT, "cards"), exist_ok=True)
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    out = {}
    if a.source in ("hn","all"):
        out["hn"] = collect_hn(a.query, a.limit)
    if a.source in ("lobsters","all"):
        out["lobsters"] = collect_lobsters(a.query, a.limit)
    if a.source in ("github","all"):
        out["github"] = collect_github(a.query, a.limit)
    flat = []
    for v in out.values():
        flat.extend(v)
    path = os.path.join(OUT, f"raw_{a.source}_{ts}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"query": a.query, "count": len(flat), "results": flat}, f, indent=2, ensure_ascii=False)
    print(f"saved {len(flat)} results -> {path}")
    # print top 5 for quick scan
    for r in flat[:5]:
        print("-", r.get("title","(no title)"), "|", r.get("url"))

if __name__ == "__main__":
    main()
