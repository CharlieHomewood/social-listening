# %%
import os
from dotenv import load_dotenv
from googleapiclient.discovery import build
from datetime import datetime, timedelta, timezone

load_dotenv()

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

def search_youtube(search_query: str, max_results: int = 10, days_back: int = 30) -> list:
    published_after = (datetime.now(timezone.utc) - timedelta(days=days_back)).isoformat()

    request = youtube.search().list(
        q = search_query,
        part = "snippet",
        type = "video",
        maxResults = max_results,
        order = "viewCount",
        publishedAfter = published_after
    )
    response = request.execute()

    videos = []
    for item in response.get("items", []):
        video = {
            "title": item["snippet"]["title"],
            "channel": item["snippet"]["channelTitle"],
            "published_at": item["snippet"]["publishedAt"],
            "video_id": item["id"]["videoId"],
            "url": f"https://www.youtube.com/watch?v={item['id']['videoId']}"
        }
        videos.append(video)

    return videos

# %%
search_youtube(search_query = "python coding", max_results = 1, days_back = 30)
# %%
