import os
import requests
import feedparser
from dotenv import load_dotenv

# .env 파일로부터 환경변수를 로드합니다.
load_dotenv()

RSS_FEEDS: dict[str, str] = {
    # Global AI Tech News
    "Anthropic":        "https://www.anthropic.com/rss.xml",
    "OpenAI":           "https://openai.com/news/rss.xml",
    "Google DeepMind":  "https://deepmind.google/blog/rss.xml",
    "Hugging Face":     "https://huggingface.co/blog/feed.xml",
    "TechCrunch AI":    "https://techcrunch.com/category/artificial-intelligence/feed/",
    "The Verge AI":     "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml",
    "MIT Tech Review":  "https://www.technologyreview.com/feed/",
    "Ars Technica":     "https://feeds.arstechnica.com/arstechnica/technology-lab",
    
    # Korean News Sources (Google News Korea RSS)
    "Korea Tech News":  "https://news.google.com/rss/search?q=technology+when:7d&hl=ko&gl=KR&ceid=KR:ko",
    "Korea AI News":    "https://news.google.com/rss/search?q=인공지능+when:7d&hl=ko&gl=KR&ceid=KR:ko",
}

def fetch_rss_news():
    """설정된 RSS 피드에서 최신 뉴스를 가져옵니다."""
    all_news = []
    
    for source, url in RSS_FEEDS.items():
        print(f"[{source}] 뉴스 가져오는 중...")
        try:
            feed = feedparser.parse(url)
            
            # 각 소스별로 최신 뉴스 3개씩 추출
            for entry in feed.entries[:3]:
                news_item = {
                    "source": source,
                    "title": entry.title,
                    "link": entry.link,
                    "published": entry.get("published", "No Date")
                }
                all_news.append(news_item)
        except Exception as e:
            print(f"Error fetching from {source}: {e}")
            
    return all_news

def send_slack_message(news_list):
    """슬랙 웹훅을 통해 뉴스 리스트를 전송합니다."""
    slack_webhook_url = os.environ.get("SLACK_WEBHOOK_URL")
    
    if not slack_webhook_url:
        print("Error: SLACK_WEBHOOK_URL 환경변수가 설정되지 않았습니다.")
        return

    if not news_list:
        print("전송할 뉴스 데이터가 없습니다.")
        return

    # 슬랙 메시지 구성 (Blocks UI 활용)
    blocks = [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": "🌐 AI Tech News Update (Global + Korea)",
                "emoji": True
            }
        },
        {"type": "divider"}
    ]
    
    # 소스별로 그룹화하여 표시하거나 리스트로 표시
    current_source = ""
    for news in news_list:
        if current_source != news['source']:
            current_source = news['source']
            blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*[{current_source}]*"
                }
            })
            
        blocks.append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"• <{news['link']}|{news['title']}>"
            }
        })

    payload = {"blocks": blocks}
    
    try:
        response = requests.post(slack_webhook_url, json=payload)
        response.raise_for_status()
        print("슬랙 메시지가 성공적으로 전송되었습니다.")
    except Exception as e:
        print(f"Error sending slack message: {e}")

if __name__ == "__main__":
    print("AI 기술 뉴스 RSS 크롤링 시작...")
    latest_news = fetch_rss_news()
    
    if latest_news:
        print(f"성공적으로 {len(latest_news)}개의 뉴스를 가져왔습니다.")
        send_slack_message(latest_news)
    else:
        print("뉴스를 가져오는 데 실패했습니다.")
