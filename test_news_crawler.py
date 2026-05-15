import unittest
from unittest.mock import patch, MagicMock
import os
import news_crawler

class TestNewsCrawler(unittest.TestCase):

    @patch('news_crawler.requests.get')
    def test_crawl_zdnet_ai_success(self, mock_get):
        # Mocking the response from zdnet
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = """
        <html>
            <body>
                <a href="/view/?no=123"><h3>AI 뉴스 제목 1</h3></a>
                <a href="/view/?no=456"><h3>AI 뉴스 제목 2</h3></a>
                <a href="/view/?no=789"><h3>AI 뉴스 제목 3</h3></a>
                <a href="/view/?no=012"><h3>AI 뉴스 제목 4</h3></a>
                <a href="/view/?no=345"><h3>AI 뉴스 제목 5</h3></a>
                <a href="/view/?no=678"><h3>AI 뉴스 제목 6</h3></a>
            </body>
        </html>
        """
        mock_get.return_value = mock_response

        news_list = news_crawler.crawl_zdnet_ai()

        self.assertEqual(len(news_list), 5)
        self.assertEqual(news_list[0]['title'], "AI 뉴스 제목 1")
        self.assertTrue(news_list[0]['link'].startswith("https://zdnet.co.kr"))
        self.assertIn("/view/?no=123", news_list[0]['link'])

    @patch('news_crawler.requests.get')
    def test_crawl_zdnet_ai_failure(self, mock_get):
        mock_get.side_effect = Exception("Network error")
        
        news_list = news_crawler.crawl_zdnet_ai()
        self.assertEqual(news_list, [])

    @patch('news_crawler.requests.post')
    @patch.dict(os.environ, {"SLACK_WEBHOOK_URL": "https://fake-webhook.com"})
    def test_send_slack_message_success(self, mock_post):
        mock_post.return_value.status_code = 200
        
        news_list = [{"title": "Test News", "link": "http://test.com"}]
        news_crawler.send_slack_message(news_list)
        
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        self.assertEqual(args[0], "https://fake-webhook.com")
        self.assertIn("blocks", kwargs['json'])

    @patch('news_crawler.requests.post')
    @patch.dict(os.environ, {"SLACK_WEBHOOK_URL": ""}, clear=True)
    def test_send_slack_message_no_webhook(self, mock_post):
        # Should not call post if webhook is missing
        news_crawler.send_slack_message([{"title": "Test", "link": "link"}])
        mock_post.assert_not_called()

if __name__ == '__main__':
    unittest.main()
