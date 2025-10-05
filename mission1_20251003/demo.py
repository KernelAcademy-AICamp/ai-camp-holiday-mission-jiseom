import os
from dotenv import load_dotenv
import gradio as gr 
import json
import pickle
from openai import OpenAI
import datetime
from dateutil import parser

MAPPING ={
    '인사동': './res/insadong.json',
    '판교': './res/reviews.json',
    '용산': './res/yongsan.json'
}
with open('./res/prompt_1shot.pickle','rb') as f: 
    PROMPT = pickle.load(f)


def preprocess_reviews(path='./res/reviews.json', months=6):
    with open(path, 'r', encoding='utf-8') as f:  # 'r' 읽기 모드
        review_list = json.load(f)

    reviews_good, reviews_bad = [], []

    current_date = datetime.datetime.now()
    date_boundary = current_date - datetime.timedelta(days=months*30)

    for r in review_list:
        review_date_str = r.get('date', '')
        try:
            review_date = parser.parse(review_date_str)
        except (ValueError, TypeError):
            review_date = current_date  # '6시간전' 같은 포맷은 오늘 날짜 넣음

        if review_date < date_boundary:
            continue

    
        if r.get('stars', 0) == 5: 
            reviews_good.append('[REVIEW_START]' + r['review'] + '[REVIEW_END]')
        else:
            reviews_bad.append('[REVIEW_START]' + r['review'] + '[REVIEW_END]')

    reviews_good = reviews_good[:min(len(reviews_good),20)]
    reviews_bad = reviews_bad[:min(len(reviews_bad),20)] 

    reviews_good_text = '\n'.join(reviews_good)
    reviews_bad_text = '\n'.join(reviews_bad)

    return reviews_good_text, reviews_bad_text


def summarize(reviews):
    prompt = PROMPT + '\n\n' + reviews
    # .env 파일 불러오기
    load_dotenv()

    # OpenAI 클라이언트 생성
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    completion = client.chat.completions.create(
    model='gpt-3.5-turbo-0125',
    messages=[{"role":"user","content":prompt}],
    temperature=0.0 
    )
    return completion



def fn(accom_name):
    path = MAPPING[accom_name]
    reviews_good, reviews_bad = preprocess_reviews(path)
    
    summary_good= summarize(reviews_good).choices[0].message.content
    summary_bad= summarize(reviews_bad).choices[0].message.content

    return summary_good, summary_bad
       

def run_demo():
    demo = gr.Interface(
        fn=fn,
        inputs=[gr.Radio(['인사동','판교','용산'], label ='숙소')],
        outputs=[gr.Textbox(label='높은 평점 요약'), gr.Textbox(label='낮은 평점 요약')]
    )
    demo.launch()


if __name__ == '__main__':
    run_demo()