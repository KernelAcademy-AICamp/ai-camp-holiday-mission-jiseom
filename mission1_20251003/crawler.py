import json
import sys
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent   # crawler.py가 있는 폴더
RES_DIR = BASE_DIR / "res"
RES_DIR.mkdir(exist_ok=True)  # 폴더 없으면 자동 생성

def crawler_yanolja_reviews(name, url): 
    review_list = []
    driver = webdriver.Chrome()
    driver.get(url)

    time.sleep(3)  # 페이지 로딩 대기

    scroll_count = 20   # 스크롤 횟수
    for _ in range(scroll_count):
        driver.execute_script('window.scrollTo(0,document.body.scrollHeight);')
        time.sleep(2)  # 스크롤 후 로딩 대기

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        # 리뷰 컨테이너
        review_containers = soup.select("div.css-1js0bc8 > div > div")

        for r in review_containers:
            # 리뷰 본문
            text_tag = r.select_one("p.content-text")
            review_text = text_tag.text.strip() if text_tag else None

            # 별점
            score = 0
            star_block = r.select_one("div.css-1mdp7n")
            stars = []
            if star_block:
                stars = star_block.find_all("path")
                for s in stars:
                    if s.get("fill") == "currentColor" and s.get("fill-rule") != "evenodd":
                        score += 1

            # 날짜
            date_tag = r.select_one("p.css-6lreu3")
            date = date_tag.text.strip() if date_tag else None

            if review_text:  # 본문 있는 경우만 저장
                review_dict = {
                    'review': review_text,
                    'stars': score, 
                    'date': date
                }
                review_list.append(review_dict)

    driver.quit()

    # JSON 저장
    with open(f"{RES_DIR}/{name}.json", "w", encoding="utf-8") as f:
        json.dump(review_list, f, indent=4, ensure_ascii=False)

if __name__ == '__main__':
    name, url = sys.argv[1],sys.argv[2]
    crawler_yanolja_reviews(name=name,url=url)
