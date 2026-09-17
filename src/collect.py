"""Bounded pain-signal collection through permitted public APIs.

Sources: HN Algolia, Lobsters JSON feeds, GitHub Issues API, and Reddit's
OAuth API. Reddit collection is intentionally narrow: provide one or more
subreddits and preserve post/comment context. No bulk subreddit scraping.

Usage:
  python src/collect.py --source hn --query "tedious workflow" --limit 20
  python src/collect.py --source lobsters --query "debugging" --limit 20
  python src/collect.py --source reddit --subreddit sysadmin --query "manual" --limit 10
  python src/collect.py --source all --subreddit devops --query "takes hours" --limit 10

Reddit requires REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, and REDDIT_USER_AGENT.
"""
import argparse
import base64
import datetime
import json
import os
import urllib.parse
import urllib.request

OUT = os.path.join(os.path.dirname(__file__), "..", "evidence")
USER_AGENT = "painsearch/1.1 (bounded research collector; contact project maintainer)"


def now_iso():
    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")


def fetch_json(url, headers=None, timeout=20, data=None):
    req = urllib.request.Request(url, headers=headers or {"User-Agent": USER_AGENT}, data=data)
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8", "replace"))


def provenance(source, source_id, published_at, canonical_url, collected_at):
    return {
        "source": source,
        "source_record_id": str(source_id) if source_id is not None else None,
        "published_at": published_at,
        "collected_at": collected_at,
        "lineage_key": canonical_url or f"{source}:{source_id}",
        "lineage_basis": "canonical_url" if canonical_url else "source_record_id",
    }


def collect_hn(query, limit, collected_at=None):
    collected_at = collected_at or now_iso()
    q = urllib.parse.quote(query)
    url = f"https://hn.algolia.com/api/v1/search?query={q}&tags=story&hitsPerPage={limit}"
    data = fetch_json(url)
    rows = []
    for hit in data.get("hits", []):
        item_id = hit.get("objectID")
        canonical_url = hit.get("url") or f"https://news.ycombinator.com/item?id={item_id}"
        rows.append({
            "source": "hn", "title": hit.get("title"), "url": canonical_url,
            "hn_id": item_id, "points": hit.get("points"),
            "comments": hit.get("num_comments"), "author": hit.get("author"),
            "created": hit.get("created_at"),
            "text_snippet": (hit.get("story_text") or "")[:1000],
            "provenance": provenance("hn", item_id, hit.get("created_at"), canonical_url, collected_at),
        })
    return rows


def collect_lobsters(query, limit, feeds=None, collected_at=None):
    """Search several bounded Lobsters feeds instead of only hottest.json."""
    collected_at = collected_at or now_iso()
    feeds = feeds or ["hottest", "newest", "active"]
    q = query.lower()
    rows, seen = [], set()
    for feed in feeds:
        if feed not in {"hottest", "newest", "active"}:
            continue
        try:
            data = fetch_json(f"https://lobste.rs/{feed}.json")
        except Exception as exc:
            rows.append({"source": "lobsters", "error": f"{feed} fetch failed: {exc}"})
            continue
        for story in data:
            story_id = story.get("short_id") or story.get("short_id_url") or story.get("url")
            if story_id in seen:
                continue
            blob = f"{story.get('title', '')} {story.get('description', '')} {' '.join(story.get('tags', []))}".lower()
            if q and q not in blob:
                continue
            seen.add(story_id)
            canonical_url = story.get("url") or story.get("short_id_url")
            rows.append({
                "source": "lobsters", "title": story.get("title"), "url": canonical_url,
                "comments_url": story.get("comments_url"), "score": story.get("score"),
                "tags": story.get("tags"), "created": story.get("created_at"), "feed": feed,
                "provenance": provenance("lobsters", story_id, story.get("created_at"), canonical_url, collected_at),
            })
            if len(rows) >= limit:
                return rows
    return rows


def collect_github(query, limit, collected_at=None):
    collected_at = collected_at or now_iso()
    token = os.environ.get("GITHUB_TOKEN", "")
    headers = {"User-Agent": USER_AGENT, "Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    q = urllib.parse.quote(f"{query} in:title,body type:issue state:open")
    url = f"https://api.github.com/search/issues?q={q}&per_page={min(limit, 30)}&sort=reactions&order=desc"
    try:
        data = fetch_json(url, headers=headers)
    except Exception as exc:
        return [{"source": "github-issues", "error": f"github fetch failed: {exc}. Set GITHUB_TOKEN if rate-limited."}]
    rows = []
    for issue in data.get("items", []):
        canonical_url = issue.get("html_url")
        rows.append({
            "source": "github-issues", "title": issue.get("title"), "url": canonical_url,
            "repo": issue.get("repository_url", "").split("repos/")[-1],
            "issue_number": issue.get("number"),
            "reactions": (issue.get("reactions") or {}).get("total_count"),
            "comments": issue.get("comments"), "created": issue.get("created_at"),
            "body_snippet": (issue.get("body") or "")[:1200],
            "provenance": provenance("github-issues", issue.get("id"), issue.get("created_at"), canonical_url, collected_at),
        })
    return rows


def reddit_access_token():
    client_id = os.environ.get("REDDIT_CLIENT_ID")
    client_secret = os.environ.get("REDDIT_CLIENT_SECRET")
    user_agent = os.environ.get("REDDIT_USER_AGENT", USER_AGENT)
    if not client_id or not client_secret:
        raise RuntimeError("Reddit requires REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET")
    credentials = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    body = urllib.parse.urlencode({"grant_type": "client_credentials"}).encode()
    data = fetch_json(
        "https://www.reddit.com/api/v1/access_token",
        headers={"Authorization": f"Basic {credentials}", "User-Agent": user_agent, "Content-Type": "application/x-www-form-urlencoded"},
        data=body,
    )
    return data["access_token"], user_agent


def _reddit_comments(children, limit):
    comments = []
    for child in children:
        if child.get("kind") != "t1":
            continue
        item = child.get("data", {})
        body = item.get("body")
        if not body or body in {"[deleted]", "[removed]"}:
            continue
        created = item.get("created_utc")
        comments.append({
            "id": item.get("id"), "author": item.get("author"), "body": body,
            "score": item.get("score"),
            "created": datetime.datetime.fromtimestamp(created, datetime.timezone.utc).isoformat(timespec="seconds") if created else None,
            "permalink": f"https://www.reddit.com{item.get('permalink', '')}",
        })
        if len(comments) >= limit:
            break
    return comments


def collect_reddit(subreddits, query, limit, comment_limit=5, collected_at=None):
    """Collect bounded post searches and top-level comment context via OAuth."""
    collected_at = collected_at or now_iso()
    token, user_agent = reddit_access_token()
    headers = {"Authorization": f"bearer {token}", "User-Agent": user_agent}
    rows = []
    for subreddit in subreddits:
        params = urllib.parse.urlencode({"q": query, "restrict_sr": "on", "sort": "relevance", "t": "all", "limit": min(limit, 25), "type": "link"})
        search_url = f"https://oauth.reddit.com/r/{urllib.parse.quote(subreddit)}/search.json?{params}"
        listing = fetch_json(search_url, headers=headers)
        for child in listing.get("data", {}).get("children", []):
            post = child.get("data", {})
            post_id = post.get("id")
            permalink = f"https://www.reddit.com{post.get('permalink', '')}"
            comments = []
            if post_id and comment_limit:
                try:
                    thread = fetch_json(f"https://oauth.reddit.com/comments/{post_id}.json?limit={min(comment_limit, 10)}&depth=1", headers=headers)
                    if isinstance(thread, list) and len(thread) > 1:
                        comments = _reddit_comments(thread[1].get("data", {}).get("children", []), comment_limit)
                except Exception as exc:
                    comments = [{"error": f"comment context unavailable: {exc}"}]
            created = post.get("created_utc")
            published = datetime.datetime.fromtimestamp(created, datetime.timezone.utc).isoformat(timespec="seconds") if created else None
            rows.append({
                "source": "reddit", "subreddit": subreddit, "title": post.get("title"),
                "url": permalink, "reddit_id": post_id, "author": post.get("author"),
                "created": published, "score": post.get("score"),
                "comments_count": post.get("num_comments"), "post_text": post.get("selftext") or "",
                "comments": comments,
                "provenance": provenance("reddit", post_id, published, permalink, collected_at),
            })
    return rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", choices=["hn", "lobsters", "github", "reddit", "all"], default="hn")
    parser.add_argument("--query", default="tedious workflow")
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--subreddit", action="append", default=[], help="Reddit community; repeat for multiple communities")
    parser.add_argument("--comment-limit", type=int, default=5)
    parser.add_argument("--lobsters-feeds", default="hottest,newest,active,recent")
    args = parser.parse_args()
    if args.source in {"reddit", "all"} and not args.subreddit:
        parser.error("--subreddit is required for Reddit collection")
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(os.path.join(OUT, "cards"), exist_ok=True)
    collected_at = now_iso()
    output = {}
    if args.source in ("hn", "all"):
        output["hn"] = collect_hn(args.query, args.limit, collected_at)
    if args.source in ("lobsters", "all"):
        output["lobsters"] = collect_lobsters(args.query, args.limit, args.lobsters_feeds.split(","), collected_at)
    if args.source in ("github", "all"):
        output["github"] = collect_github(args.query, args.limit, collected_at)
    if args.source in ("reddit", "all"):
        output["reddit"] = collect_reddit(args.subreddit, args.query, args.limit, args.comment_limit, collected_at)
    flat = [row for rows in output.values() for row in rows]
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(OUT, f"raw_{args.source}_{timestamp}.json")
    with open(path, "w", encoding="utf-8") as handle:
        json.dump({"query": args.query, "count": len(flat), "results": flat}, handle, indent=2, ensure_ascii=False)
    print(f"saved {len(flat)} results -> {path}")
    for row in flat[:5]:
        print("-", row.get("title", "(no title)"), "|", row.get("url"))


if __name__ == "__main__":
    main()
