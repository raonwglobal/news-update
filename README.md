# AI Tech News Update 🌐

이 프로젝트는 최신 AI 기술 뉴스를 여러 RSS 피드에서 수집하여 슬랙(Slack)으로 자동 전송하는 간단한 뉴스 크롤러입니다. GitHub Actions를 사용하여 매일 정해진 시간에 뉴스를 업데이트합니다.

## 🚀 주요 기능

- **다양한 소스 수집**: Anthropic, OpenAI, Google DeepMind, Hugging Face 등 주요 AI 기업 및 뉴스 매체의 RSS 피드를 지원합니다.
- **슬랙 연동**: 수집된 뉴스를 슬랙의 Blocks UI를 활용하여 깔끔하게 전송합니다.
- **자동화**: GitHub Actions를 통해 매일 오전 8시(KST)에 자동으로 실행됩니다.
- **커스터마이징**: 수집하고자 하는 RSS 피드를 쉽게 추가하거나 변경할 수 있습니다.

## 🛠 기술 스택

- **Language**: Python 3.10+
- **Libraries**: `requests`, `feedparser`, `python-dotenv`
- **Automation**: GitHub Actions
- **Notification**: Slack Webhooks

## 📋 설치 및 실행 방법

### 1. 저장소 클론
```bash
git clone https://github.com/your-username/ai-news.git
cd ai-news
```

### 2. 가상환경 설정 및 패키지 설치
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. 환경 변수 설정
프로젝트 루트에 `.env` 파일을 생성하고 슬랙 웹훅 URL을 입력합니다.
```env
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
```

### 4. 실행
```bash
python news_crawler.py
```

## 🧪 테스트 실행
단위 테스트를 통해 크롤러와 메시지 전송 로직을 검증할 수 있습니다.
```bash
python test_news_crawler.py
```

## 🤖 자동화 (GitHub Actions)

이 프로젝트는 `.github/workflows/daily_news.yml` 설정을 통해 매일 자동으로 실행됩니다. GitHub 저장소의 **Settings > Secrets and variables > Actions**에서 다음 Secret을 설정해야 합니다:

- `SLACK_WEBHOOK_URL`: 뉴스를 전송할 슬랙 채널의 인커밍 웹훅 URL

## 📡 지원하는 뉴스 소스
현재 다음 소스들의 최신 뉴스 3개씩을 수집합니다:
- Anthropic
- OpenAI
- Google DeepMind
- Hugging Face
- TechCrunch AI
- The Verge AI
- MIT Tech Review
- Ars Technica

## 📄 라이선스
이 프로젝트는 MIT 라이선스를 따릅니다.
