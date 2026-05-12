import requests, re, os
from html import unescape

def start():
    try:
        # دریافت محتوای نسخه وب کانال
        res = requests.get("https://t.me/s/proxymtprotoir")
        
        # پیدا کردن تمام متن‌های داخل پست‌ها (کلاس tgme_widget_message_text)
        # این الگو کل محتوای متنی هر پست را جداگانه استخراج می‌کند
        messages = re.findall(r'<div class="tgme_widget_message_text[^>]*>(.*?)</div>', res.text, re.DOTALL)

        proxies_content = []
        v2ray_content = []

        for msg in messages:
            # تمیز کردن کدهای HTML مثل <br/> و تبدیل &amp; به &
            clean_text = re.sub(r'<[^>]+>', '\n', msg)
            clean_text = unescape(clean_text).strip()
            
            # فیلتر کردن برای پوشه‌بندی
            if "proxy?server=" in clean_text or "tg://proxy" in clean_text:
                proxies_content.append(clean_text)
                proxies_content.append("-" * 20) # خط جداکننده بین پست‌ها
            
            if any(proto in clean_text for proto in ["vless://", "vmess://", "ss://", "trojan://"]):
                v2ray_content.append(clean_text)
                v2ray_content.append("-" * 20)

        # ذخیره فایل‌ها
        os.makedirs("telegram", exist_ok=True)
        
        with open("telegram/proxy.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(proxies_content))
            
        with open("telegram/v2ray.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(v2ray_content))
            
        print("Done! Full messages collected.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    start()
