import os
import requests
from datetime import datetime

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
NEWS_API_KEY = os.environ.get("NEWS_API_KEY")

def get_indian_trending_topics():
    topics = []
    categories = ["technology", "business", "science", "general", "entertainment", "health"]
    
    for category in categories:
        url = f"https://newsapi.org/v2/top-headlines?category={category}&country=in&language=en&pageSize=3&apiKey={NEWS_API_KEY}"
        response = requests.get(url)
        data = response.json()
        
        if data.get("articles"):
            for article in data["articles"]:
                if article.get("title") and article.get("url"):
                    topics.append({
                        "title": article["title"],
                        "category": category.upper(),
                        "url": article["url"],
                        "source": article.get("source", {}).get("name", "Unknown")
                    })
    
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
    topics = get_indian_trending_topics()
    
    message = f"🇮🇳🔥 <b>TRENDING IN INDIA - {today}</b>\n\n"
    message += "Top content ideas for your Indian audience today:\n\n"
    
    for i, topic in enumerate(topics[:12], 1):
        message += f"{i}. [{topic['category']}] {topic['title']}\n"
        message += f"   📰 {topic['source']}\n"
        message += f"   🔗 {topic['url']}\n\n"
    
    message += "\n💡 Pick your best topic and create your content today!\n"
    message += "🎯 Focus on what's trending for maximum viral potential!"
    
    send_telegram_message(message)
    print("Message sent successfully!")

if __name__ == "__main__":
    main()
