import feedparser
import json
from datetime import datetime
from bs4 import BeautifulSoup

def crawl_daangn_medium():
    feed_url = "https://medium.com/feed/daangn"
    feed = feedparser.parse(feed_url)

    posts = []
    default_image = "https://via.placeholder.com/300x200?text=No+Image"

    for entry in feed.entries:
        image_url = ""

        # 1. content에서 이미지 찾기
        if 'content' in entry:
            content_html = entry.content[0].value
            soup = BeautifulSoup(content_html, 'html.parser')
            img_tag = soup.find('img')
            if img_tag and img_tag.get('src'):
                image_url = img_tag['src']

        # 2. summary에서 이미지 찾기
        if not image_url and 'summary' in entry:
            soup = BeautifulSoup(entry.summary, 'html.parser')
            img_tag = soup.find('img')
            if img_tag and img_tag.get('src'):
                image_url = img_tag['src']

        # 3. media_content에서 이미지 찾기
        if not image_url and 'media_content' in entry:
            media = entry.media_content
            if isinstance(media, list) and 'url' in media[0]:
                image_url = media[0]['url']

        # 4. 기본 이미지로 대체
        if not image_url:
            image_url = default_image

        post = {
            "title": entry.title,
            "link": entry.link,
            "author": entry.get("author", "당근"),
            "date": datetime(*entry.published_parsed[:6]).strftime('%Y-%m-%d'),
            "source": "Medium",
            "image_url": image_url,
            "category": "미분류"
        }
        posts.append(post)

    with open('./data/posts.json', 'w', encoding='utf-8') as f:
        json.dump(posts, f, ensure_ascii=False, indent=2)

    print(f"{len(posts)}개 포스트 저장 완료!")

if __name__ == "__main__":
    crawl_daangn_medium()
