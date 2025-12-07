import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
from datetime import datetime
import json

# -------------------------------
# 1️⃣ 读取 GitHub Secrets
# -------------------------------
mail_user = os.environ["MAIL_USER"]
mail_pass = os.environ["MAIL_PASS"]
hf_api_key = os.environ["HF_API_KEY"]

# -------------------------------
# 2️⃣ 使用 HuggingFace Router API 生成内容
# -------------------------------
def get_daily_tech_news():
    """
    使用 HuggingFace Router API 生成科技新闻段落
    模型示例: bigscience/bloom-560m
    """
    url = "https://router.huggingface.co/api/v1/generate"
    headers = {
        "Authorization": f"Bearer {hf_api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "bigscience/bloom-560m",
        "inputs": "Generate a detailed paragraph about the latest technology that is ready for commercialization globally yesterday:",
        "parameters": {"max_new_tokens": 300}
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=60)
        response.raise_for_status()
        data = response.json()
        # Router API 返回结果是列表，每个 item 有 'generated_text'
        if isinstance(data, list) and len(data) > 0 and "generated_text" in data[0]:
            return data[0]["generated_text"]
        else:
            return "No content generated."
    except Exception as e:
        return f"Error generating content: {e}"

# -------------------------------
# 3️⃣ 发送邮件函数
# -------------------------------
def send_email(subject, body, to_email):
    msg = MIMEMultipart()
    msg['From'] = mail_user
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(mail_user, mail_pass)
        server.send_message(msg)
        server.quit()
        print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Error sending email: {e}")

# -------------------------------
# 4️⃣ 主程序
# -------------------------------
if __name__ == "__main__":
    today = datetime.utcnow().strftime("%Y-%m-%d")
    subject = f"Daily Technology Summary - {today}"

    body = get_daily_tech_news()
    send_email(subject, body, mail_user)
