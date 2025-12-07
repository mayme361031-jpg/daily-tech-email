# main.py
import os
from huggingface_hub import InferenceClient
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# ===== 配置环境变量 =====
# 1. HF_API_KEY: Hugging Face 免费 API Key
# 2. MAIL_USER: 你的 Gmail 地址
# 3. MAIL_PASS: Gmail 应用专用密码
HF_API_KEY = os.environ.get("HF_API_KEY")
MAIL_USER = os.environ.get("MAIL_USER")
MAIL_PASS = os.environ.get("MAIL_PASS")

# ===== 获取每日新技术内容 =====
def get_daily_tech_news():
    client = InferenceClient(token=HF_API_KEY)
    prompt = (
        "请用中文详细总结：昨天全球范围内有哪些新技术刚刚宣布即将商业化？"
        "请列出技术名称、对应公司、对应产品，并用段落形式说明。"
    )
    try:
        response = client.chat_completion(
            model="meta-llama/Llama-3-1B-Instruct",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
            temperature=0.7
        )
        # 提取生成的文本
        content = response.choices[0].message.content
        return content
    except Exception as e:
        return f"Error generating content: {str(e)}"

# ===== 发送邮件 =====
def send_email(subject, body, to_addr):
    msg = MIMEMultipart()
    msg["From"] = MAIL_USER
    msg["To"] = to_addr
    msg["Subject"] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(MAIL_USER, MAIL_PASS)
        server.sendmail(MAIL_USER, to_addr, msg.as_string())
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {str(e)}")

# ===== 主程序 =====
if __name__ == "__main__":
    content = get_daily_tech_news()
    subject = f"每日全球新技术摘要 {datetime.utcnow().strftime('%Y-%m-%d')}"
    send_email(subject, content, MAIL_USER)
