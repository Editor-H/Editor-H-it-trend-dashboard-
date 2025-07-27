import feedparser
import json
from datetime import datetime
from bs4 import BeautifulSoup  # 이미지 추출용

def crawl_daangn_medium():
    feed_url = "https://medium.com/feed/daangn"
    feed = feedparser.parse(feed_url)

    posts = []
    default_image = "https://via.placeholder.com/300x200?text=No+Image"

    for entry in feed.entries:
        # content 안에 이미지가 있을 수 있어서 파싱해보기
        image_url = default_image
        if 'content' in entry:
            content_html = entry.content[0].value
            soup = BeautifulSoup(content_html, 'html.parser')
            img_tag = soup.find('img')
            if img_tag and img_tag.get('src'):
                image_url = img_tag['src']

        post = {
            "title": entry.title,
            "link": entry.link,
            "author": entry.author if "author" in entry else "당근",
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
