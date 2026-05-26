import os
import requests
from datetime import datetime

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
NEWS_API_KEY = os.environ.get("NEWS_API_KEY")
YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY")

# Indian YouTube creator channel IDs
YOUTUBE_CHANNELS = {
    "Aevy TV": "UCj22tfcQrWG7EMEKS9qLeEg",
    "Varun Mayya": "UCX6OQ3DkcsbYNE6H8uQQuVA",
    "Akshat Shrivastava": "UCqW8jxh4tH1Z1sWPbkGWL4g",
    "Labour Law Advisor": "UCQDFJMnH9UAHQ0pBQGJVe0A",
    "Pranjal Kamra": "UCiDiSLF6LxUEbBWw7r5J3Kw",
    "Rachana Ranade": "UCMAie62oCEUQG4H5LBkIY8A"
}

def get_youtube_latest_videos():
    videos = []
    for channel_name, channel_id in YOUTUBE_CHANNELS.items():
        url = f"https://www.googleapis.com/youtube/v3/search?key={YOUTUBE_API_KEY}&channelId={channel_id}&part=snippet&order=date&maxResults=1&type=video"
        try:
            response = requests.get(url, timeout=5)
            data = response.json()
            if data.get("items"):
                item = data["items"][0]
                title = item["snippet"]["title"]
                video_id = item["id"]["videoId"]
                videos.append({
                    "channel": channel_name,
                    "title": title,
                    "url": f"https://youtube.com/watch?v={video_id}"
                })
        except:
            pass
    return videos

def get_indian_news():
    topics = []
    searches = [
        "India AI technology",
        "India economy market",
        "India politics",
        "India viral trending",
        "Bollywood entertainment India",
        "India cricket"
    ]
    for query in searches:
        url = f"https://newsapi.org/v2/everything?q={query}&language=en&sortBy=publishedAt&pageSize=2&apiKey={NEWS_API_KEY}"
        try:
            response = requests.get(url, timeout=5)
            data = response.json()
            if data.get("articles"):
                for article in data["articles"]:
                    if article.get("title") and article.get("url"):
                        topics.append({
                            "title": article["title"],
                            "category": query.split()[1].upper(),
                            "url": article["url"],
                            "source": article.get("source", {}).get("name", "Unknown")
                        })
        except:
            pass
    return topics

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    requests.post(url, json=payload)

def main():
    today = datetime.now().strftime("%d %B %Y")
    
    message = f"🇮🇳🔥 <b>TRENDING IN INDIA - {today}</b>\n\n"
    
    # YouTube section
    videos = get_youtube_latest_videos()
    if videos:
        message += "📺 <b>LATEST FROM TOP INDIAN CREATORS:</b>\n\n"
        for video in videos:
            message += f"▶️ <b>{video['channel']}</b>\n"
            message += f"   {video['title']}\n"
            message += f"   🔗 {video['url']}\n\n"
    
    # News section
    news = get_indian_news()
    if news:
        message += "\n📰 <b>TRENDING INDIAN NEWS TOPICS:</b>\n\n"
        seen = set()
        count = 0
        for topic in news:
            if topic['title'] not in seen and count < 8:
                seen.add(topic['title'])
                count += 1
                message += f"{count}. [{topic['category']}] {topic['title']}\n"
                message += f"   📰 {topic['source']} | 🔗 {topic['url']}\n\n"
    
    message += "\n💡 Pick your best topic and create your content!\n"
    message += "🎯 Focus on what's trending for maximum viral potential!"
    
    send_telegram_message(message)
    print("Message sent successfully!")

if __name__ == "__main__":
    main()
