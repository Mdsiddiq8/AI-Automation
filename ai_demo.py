import feedparser
from openai import OpenAI

# 1. Initialize OpenAI client with your key
api_key = "OPENAI_API_KEY"
client = OpenAI(api_key=api_key)


# 2. FUNCTION: Fetch live real-time news data from an RSS feed
def get_realtime_news():
    print("Fetching live real-time news...")
    # Fetching live top news from BBC World News feed
    feed_url = "http://feeds.bbci.co.uk/news/world/rss.xml"
    feed = feedparser.parse(feed_url)

    # Extract the top 5 recent news headlines & summaries
    live_articles = []
    for entry in feed.entries[:5]:
        live_articles.append(f"- Title: {entry.title}\n  Summary: {entry.summary}")

    # Combine into a single text block
    realtime_data = "\n\n".join(live_articles)
    return realtime_data


# 3. Fetch the real-time data
live_context = get_realtime_news()

# 4. Construct the prompt with real-time data passed inside
prompt = f"""
Here is the real-time news data fetched right now:

{live_context}

Task: Based ONLY on the real-time data provided above, summarize the key global events in 3 bullet points.
"""

# 5. Send the real-time data to OpenAI LLM
print("\nSending live data to LLM...\n")
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}],
)

# 6. Display the result
print("=== AI Summary of Real-Time Data ===")
print(response.choices[0].message.content)