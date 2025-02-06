import requests
from bs4 import BeautifulSoup

TELEGRAM_BOT_TOKEN = '8175017319:AAH44y_pLofW-xF1t3MTAruMbW6_G4JGYJA'
TELEGRAM_CHAT_ID = '6253060570'
URL = 'https://bluewings1995.com/free/category/3666'

def send_telegram_message(message):
    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message
    }
    try:
        requests.post(telegram_url, data=payload)
    except Exception as e:
        print("텔레그램 메시지 전송 중 오류 발생:", e)

def get_latest_post_title():
    try:
        response = requests.get(URL)
        response.raise_for_status()
    except Exception as e:
        print("웹페이지 로드 중 오류 발생:", e)
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    # Rhymix 기반 게시판의 경우 게시물은 보통 <li class="xe-list-item"> 요소에 있으며, 제목은 해당 요소 내의 <a> 태그에 있습니다.
    latest_post = soup.find('li', class_='xe-list-item')
    if latest_post:
        title_tag = latest_post.find('a')
        if title_tag:
            return title_tag.get_text(strip=True)
    return None

def main():
    title = get_latest_post_title()
    if title:
        message = f"현재 최신 게시물: {title}\n바로 확인: {URL}"
        send_telegram_message(message)
        print("알림 전송:", message)
    else:
        print("게시물을 찾을 수 없음.")

if __name__ == "__main__":
    main()
