import requests, re, os, datetime
from html import unescape

def start():
    try:
        # دریافت تاریخ امروز
        today = datetime.datetime.now().date()
        
        # دریافت محتوای کانال
        res = requests.get("https://t.me/s/proxymtprotoir")
        messages = re.findall(r'<div class="tgme_widget_message_text[^>]*>(.*?)</div>', res.text, re.DOTALL)

        os.makedirs("telegram", exist_ok=True)
        paths = {"proxy": "telegram/proxy.txt", "v2ray": "telegram/v2ray.txt"}

        # چک کردن تاریخ فایل‌ها برای پاکسازی روزانه
        for key in paths:
            file_path = paths[key]
            if os.path.exists(file_path):
                file_time = datetime.datetime.fromtimestamp(os.path.getmtime(file_path)).date()
                # اگر فایل متعلق به روز قبل است، پاکش کن
                if file_time < today:
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write("")

        proxies_content = []
        v2ray_content = []

        for msg in messages:
            clean_text = re.sub(r'<[^>]+>', '\n', msg)
            clean_text = unescape(clean_text).strip()
            
            if "proxy?server=" in clean_text or "tg://proxy" in clean_text:
                proxies_content.append(clean_text)
                proxies_content.append("-" * 20)
            
            if any(proto in clean_text for proto in ["vless://", "vmess://", "ss://", "trojan://"]):
                v2ray_content.append(clean_text)
                v2ray_content.append("-" * 20)

        # اضافه کردن محتوای جدید (بصورت Append)
        if proxies_content:
            with open(paths["proxy"], "a", encoding="utf-8") as f:
                f.write("\n" + "\n".join(proxies_content))
            
        if v2ray_content:
            with open(paths["v2ray"], "a", encoding="utf-8") as f:
                f.write("\n" + "\n".join(v2ray_content))
            
        print(f"Update Done for {today}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    start()
