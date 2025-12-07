import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
from datetime import datetime

# -------------------------------
# 1️⃣ 读取 GitHub Secrets
# -------------------------------
mail_user = os.environ["MAIL_USER"]
mail_pass = os.environ["MAIL_PASS"]
hf_api_key = os.environ["HF_API_KEY"]

# -------------------------------
# 2️⃣ 生成前一天科技资讯内容
# -------------------------------
def get_daily_tech_news():
    """
    使用 HuggingFace 模型 API 生成科技新闻摘要
    模型: bigscience/bloom-560m
    """
    url = "https://api-inference.huggingface.co/models/bigscience/bloom-560m"
    headers = {"Authorization": f"Bearer {hf_api_key}"}
    payload = {
        "inputs": "Generate a detailed paragraph about the latest technology that is ready for commercialization globally yesterday:",
        "parameters": {"max_new_tokens": 300}
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()
        # 模型返回结果解析
        if isinstance(data, list) and "generated_text" in data[0]:
            return data[0]["generated_text"]
        elif isinstance(data, list) and "generated_text" not in data[0]:
            return data[0].get("text", "No content generated.")
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

    # 获取前一天科技内容
    body = get_daily_tech_news()

    # 发送邮件
    send_email(subject, body, mail_user)  # 发给自己
