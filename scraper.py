import requests, re, os, datetime
from html import unescape

def create_html_template(title, content):
    return f"""
    <!DOCTYPE html>
    <html dir="rtl" lang="fa">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title}</title>
        <style>
            body {{ font-family: Tahoma, Geneva, sans-serif; background-color: #f0f2f5; padding: 20px; }}
            .card {{ background: white; border-radius: 12px; padding: 15px; margin-bottom: 15px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); line-height: 1.6; word-wrap: break-word; }}
            .header {{ text-align: center; color: #1c1e21; margin-bottom: 20px; }}
            .btn {{ display: inline-block; background: #0088cc; color: white; padding: 8px 15px; border-radius: 8px; text-decoration: none; margin-top: 10px; font-size: 14px; }}
            .date {{ font-size: 12px; color: #65676b; text-align: center; }}
        </style>
    </head>
    <body>
        <div class="header"><h2>{title}</h2><p class="date">به‌روزرسانی: {datetime.datetime.now().strftime('%H:%M')}</p></div>
        {content}
    </body>
    </html>
    """

def start():
    try:
        res = requests.get("https://t.me/s/proxymtprotoir")
        messages = re.findall(r'<div class="tgme_widget_message_text[^>]*>(.*?)</div>', res.text, re.DOTALL)
        
        proxy_cards = ""
        v2ray_cards = ""

        for msg in messages:
            clean_text = re.sub(r'<[^>]+>', '<br>', msg)
            clean_text = unescape(clean_text).strip()
            
            # پیدا کردن لینک‌های فعال برای ساخت دکمه
            links = re.findall(r'(https?://t\.me/proxy\?[\w=&%.!*()+-]+|(?:vless|vmess|ss|trojan)://[^\s<"\'&]+)', clean_text)
            
            card_html = f'<div class="card">{clean_text}'
            for link in links:
                card_html += f'<br><a href="{link}" class="btn">اتصال مستقیم</a>'
            card_html += '</div>'

            if "proxy?server=" in clean_text or "tg://proxy" in clean_text:
                proxy_cards += card_html
            if any(proto in clean_text for proto in ["vless://", "vmess://", "ss://", "trojan://"]):
                v2ray_cards += card_html

        os.makedirs("telegram", exist_ok=True)
        
        with open("telegram/proxy.html", "w", encoding="utf-8") as f:
            f.write(create_html_template("پروکسی‌های تلگرام", proxy_cards))
            
        with open("telegram/v2ray.html", "w", encoding="utf-8") as f:
            f.write(create_html_template("کانفیگ‌های ویتوری", v2ray_cards))

    except Exception as e: print(f"Error: {e}")

if __name__ == "__main__": start()
