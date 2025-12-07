import requests
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from datetime import datetime, timedelta

# ----------- 免费AI模型（HuggingFace Inference 免费额度）-----------
HF_API_URL = "https://api-inference.huggingface.co/models/google/gemma-2-9b-it"
HF_HEADERS = {"Authorization": "Bearer YOUR_HF_API_KEY"}  # 等下我教你申请免费 key

def generate_tech_news():
    yesterday = (datetime.utcnow() + timedelta(hours=8) - timedelta(days=1)).strftime("%Y-%m-%d")
    prompt = f"""
    请用中文详细总结：在 {yesterday} 全球有哪些“马上可以商业化的新技术”？
    每项技术请写：
    - 技术名称
    - 企业名称
    - 产品名称
    - 预计商业化时间
    - 技术原理（详细）
    - 当前行业地位和竞争者
    输出成详细段落形式。
    """

    response = requests.post(
        HF_API_URL,
        headers=HF_HEADERS,
        json={"inputs": prompt}
    )

    return response.json()[0]["generated_text"]

# ----------- Gmail 邮件发送 ----------------
def send_email(content):
    mail_host = "smtp.gmail.com"
    mail_user = "YOUR_GMAIL@gmail.com"
    mail_pass = "YOUR_APP_PASSWORD"   # Gmail 应用专用密码

    receivers = ["YOUR_GMAIL@gmail.com"]

    message = MIMEText(content, "plain", "utf-8")
    message["From"] = Header("Daily Tech Bot", "utf-8")
    message["To"] = Header("User", "utf-8")
    message["Subject"] = Header("【每日全球新技术报告】", "utf-8")

    server = smtplib.SMTP_SSL(mail_host, 465)
    server.login(mail_user, mail_pass)
    server.sendmail(mail_user, receivers, message.as_string())
    server.quit()

# ----------- 主程序 ----------------
if __name__ == "__main__":
    news = generate_tech_news()
    send_email(news)
