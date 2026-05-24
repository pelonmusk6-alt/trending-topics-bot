import os
import requests
from datetime import datetime

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
NEWS_API_KEY = os.environ.get("NEWS_API_KEY")

def get_trending_topics():
    topics = []
    categories = ["technology", "business", "science", "general"]
    
    for category in categories:
        url = f"https://newsapi.org/v2/top-headlines?category={category}&language=en&pageSize=3&apiKey={NEWS_API_KEY}"
        response = requests.get(url)
        data = response.json()
        
        if data.get("articles"):
            for article in data["articles"]:
                topics.append({
                    "title": article["title"],
                    "category": category.upper(),
                    "url": article["url"]
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
    topics = get_trending_topics()
    
    message = f"🔥 <b>TRENDING TOPICS - {today}</b>\n\n"
    message += "Here are today's top topics to create content about:\n\n"
    
    for i, topic in enumerate(topics[:10], 1):
        message += f"{i}. [{topic['category']}] {topic['title']}\n"
        message += f"   🔗 {topic['url']}\n\n"
    
    message += "\n🎯 Pick your best topic and create your content today!"
    
    send_telegram_message(message)
    print("Message sent successfully!")

if __name__ == "__main__":
    main()
