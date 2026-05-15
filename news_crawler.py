import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# .env 파일로부터 환경변수를 로드합니다.
load_dotenv()

def crawl_zdnet_ai():
    """지디넷 코리아 AI 섹션에서 최신 뉴스 5개를 크롤링합니다."""
    url = "https://zdnet.co.kr/news/?lst=010100&sub=010101"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # h3 태그를 먼저 찾고 그 부모 a 태그에서 링크를 추출
        h3_tags = soup.find_all('h3')
        
        news_list = []
        for h3 in h3_tags:
            if len(news_list) >= 5:
                break
                
            title = h3.get_text(strip=True)
            link_tag = h3.find_parent('a')
            
            if link_tag and 'href' in link_tag.attrs:
                link = link_tag['href']
                # 절대 경로 확인 및 추가
                if not link.startswith('http'):
                    link = f"https://zdnet.co.kr{link}"
                
                # 중복 제거 및 유효한 뉴스 링크인지 확인 (view 포함 여부 등)
                if '/view/' in link and not any(n['link'] == link for n in news_list):
                    news_list.append({"title": title, "link": link})
        
        return news_list
    except Exception as e:
        print(f"Error during crawling: {e}")
        return []

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
                "text": "🚀 지디넷 코리아 AI 최신 뉴스",
                "emoji": True
            }
        },
        {"type": "divider"}
    ]
    
    for i, news in enumerate(news_list, 1):
        blocks.append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"{i}. *<{news['link']}|{news['title']}>*"
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
    print("지디넷 코리아 AI 뉴스 크롤링 시작...")
    latest_news = crawl_zdnet_ai()
    
    if latest_news:
        print(f"성공적으로 {len(latest_news)}개의 뉴스를 가져왔습니다.")
        for idx, news in enumerate(latest_news, 1):
            print(f"{idx}. {news['title']} ({news['link']})")
        
        send_slack_message(latest_news)
    else:
        print("뉴스를 가져오는 데 실패했습니다. 선택자 또는 페이지 구조를 확인해주세요.")
