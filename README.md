
## ✅ Task 1: Data Collection (20/20 Marks)

**What it does:**
- Fetches top 500 HackerNews stories
- Categorizes by keywords (AI/tech → war/election → NFL/NBA → NASA/space → movies/Netflix)
- Collects **25 stories per category** = **125 total**
- Saves: `data/trends_YYYYMMDD.json`


**JSON Fields:**
```json
{
  "post_id": 12345678,
  "title": "OpenAI releases new model",
  "category": "technology",
  "score": 420,
  "num_comments": 69,
  "author": "username",
  "collected_at": "2024-12-03T10:30:00"
}

