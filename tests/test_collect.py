import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import collect


class CollectorAdapterTests(unittest.TestCase):
    def test_lobsters_searches_multiple_feeds_and_deduplicates(self):
        feeds = {
            "https://lobste.rs/hottest.json": [{"short_id": "abc", "title": "manual review", "description": "", "tags": [], "url": "https://example.test/a"}],
            "https://lobste.rs/newest.json": [{"short_id": "abc", "title": "manual review", "description": "", "tags": [], "url": "https://example.test/a"}, {"short_id": "def", "title": "manual deploy", "description": "", "tags": [], "url": "https://example.test/b"}],
        }
        with patch.object(collect, "fetch_json", side_effect=lambda url, **_: feeds[url]):
            rows = collect.collect_lobsters("manual", 10, ["hottest", "newest"], "2026-09-17T00:00:00+00:00")
        self.assertEqual([row["provenance"]["source_record_id"] for row in rows], ["abc", "def"])
        self.assertEqual(rows[1]["feed"], "newest")

    def test_reddit_requires_oauth_credentials(self):
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaisesRegex(RuntimeError, "REDDIT_CLIENT_ID"):
                collect.reddit_access_token()

    def test_reddit_comment_parser_preserves_context(self):
        children = [{"kind": "t1", "data": {"id": "c1", "author": "alice", "body": "This is a workaround", "score": 4, "permalink": "/r/test/comments/p/c1/"}}]
        comments = collect._reddit_comments(children, 5)
        self.assertEqual(comments[0]["body"], "This is a workaround")
        self.assertEqual(comments[0]["permalink"], "https://www.reddit.com/r/test/comments/p/c1/")

    def test_hn_records_lineage_provenance(self):
        payload = {"hits": [{"objectID": "123", "title": "Pain", "url": "https://example.test/pain", "created_at": "2026-09-17T00:00:00Z"}]}
        with patch.object(collect, "fetch_json", return_value=payload):
            rows = collect.collect_hn("pain", 1, "2026-09-17T01:00:00+00:00")
        self.assertEqual(rows[0]["provenance"]["lineage_key"], "https://example.test/pain")
        self.assertEqual(rows[0]["provenance"]["collected_at"], "2026-09-17T01:00:00+00:00")


if __name__ == "__main__":
    unittest.main()
