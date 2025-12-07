# main2.py
import os, requests, smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

HF = os.environ["HF_API_KEY"]
MAIL_USER = os.environ["MAIL_USER"]
MAIL_PASS = os.environ["MAIL_PASS"]

def get_news():
    url = "https://router.huggingface.co/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {HF}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "Qwen/Qwen2.5-Coder-7B-Instruct",
        "messages": [
            {"role": "user", "content":
             "请用中文详细总结：昨天全球范围内有哪些新技术刚刚宣布即将商业化？包括技术、公司、产品。"}
        ],
        "max_tokens": 500,
        "temperature": 0.8
    }
    resp = requests.post(url, headers=headers, json=payload, timeout=180)
    resp.raise_for_status()
    j = resp.json()
    return j["choices"][0]["message"]["content"]

def send_email(subj, body):
    msg = MIMEMultipart()
    msg["From"] = MAIL_USER
    msg["To"] = MAIL_USER
    msg["Subject"] = subj
    msg.attach(MIMEText(body, "plain", "utf-8"))
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(MAIL_USER, MAIL_PASS)
    server.send_message(msg)
    server.quit()

if __name__ == "__main__":
    subj = "Daily Tech - Qwen7B " + datetime.utcnow().strftime("%Y-%m-%d")
    body = get_news()
    send_email(subj, body)
