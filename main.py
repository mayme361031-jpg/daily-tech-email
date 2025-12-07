import os
import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

HF_TOKEN = os.environ["HF_API_KEY"]
MAIL_USER = os.environ["MAIL_USER"]
MAIL_PASS = os.environ["MAIL_PASS"]

def get_daily_tech_news():
    url = "https://router.huggingface.co/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "meta-llama/Llama-3-1B-Instruct",  # 注意选择一个真正 support inference 的模型
        "messages": [
            {"role": "user", "content": 
             "请用中文详细总结：昨天全球范围内有哪些新技术刚刚宣布即将商业化？包括技术名称、公司、产品、简要描述。"}
        ],
        "max_tokens": 400,
        "temperature": 0.7
    }

    resp = requests.post(url, headers=headers, json=payload, timeout=60)
    resp.raise_for_status()
    j = resp.json()
    # 提取生成内容
    return j["choices"][0]["message"]["content"]

def send_email(subject, body, to_addr):
    msg = MIMEMultipart()
    msg["From"] = MAIL_USER
    msg["To"] = to_addr
    msg["Subject"] = subject
    msg.attach(MIMEText(body, 'plain'))
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(MAIL_USER, MAIL_PASS)
    server.sendmail(MAIL_USER, to_addr, msg.as_string())
    server.quit()

if __name__ == "__main__":
    content = get_daily_tech_news()
    subj = f"Tech News Summary {datetime.utcnow().strftime('%Y-%m-%d')}"
    send_email(subj, content, MAIL_USER)
