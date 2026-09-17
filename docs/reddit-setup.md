# Reddit adapter setup

PainSearch uses Reddit's OAuth **application-only** flow for read-only collection. It does not need your Reddit password or a refresh token.

## 1. Create an application

1. Sign in to Reddit with the account that will own the app.
2. Open <https://www.reddit.com/prefs/apps>.
3. Choose **create another app**.
4. Use:
   - **name:** `painsearch-research`
   - **type:** `script`
   - **description:** bounded, read-only research collection for PainSearch
   - **about URL:** optional
   - **redirect URI:** `http://localhost:8080`
5. Save the application.
6. Read and complete any current Reddit API access / Responsible Builder requirements shown for your account.

Do not send the secret in chat, commit it, or put it in a GitHub issue.

## 2. Set credentials for the current Git Bash session

Run this locally. Replace the placeholders only in your terminal:

```bash
export REDDIT_CLIENT_ID='paste-client-id-here'
export REDDIT_CLIENT_SECRET='paste-client-secret-here'
export REDDIT_USER_AGENT='painsearch/1.1 by u/your_reddit_username'
```

The client ID is the short value shown under the app name. The client secret is the value labeled `secret`.

Session-only variables are preferred while testing. They disappear when the terminal closes.

## 3. Test a narrow search

From `D:/research`:

```bash
python src/collect.py \
  --source reddit \
  --subreddit sysadmin \
  --query 'manual workaround' \
  --limit 5 \
  --comment-limit 3
```

Then inspect the generated `evidence/raw_reddit_*.json`. Confirm that each result contains the post body, comment context, permalink, subreddit, and provenance.

## 4. Search multiple targeted communities

```bash
python src/collect.py \
  --source reddit \
  --subreddit sysadmin \
  --subreddit devops \
  --subreddit webdev \
  --query 'takes hours manual' \
  --limit 10 \
  --comment-limit 5
```

Use a small number of communities and bounded limits. Repeated links, copied text, and quoted source material must be assigned one evidence lineage rather than counted as independent corroboration.

## 5. Safety and retention

- Collect only public posts/comments needed for the research question.
- Preserve permalinks and source timestamps.
- Do not collect private communities or user credentials.
- Do not commit secrets or raw credentials.
- Remove stored Reddit content if it is no longer needed or if platform policy requires deletion.

Official API reference: <https://www.reddit.com/dev/api/oauth/>.
