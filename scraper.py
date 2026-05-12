import requests, re, os

def start():
    try:
        # دریافت محتوای کانال تلگرام
        res = requests.get("https://t.me/s/proxymtprotoir")
        
        # الگوی دقیق برای پروکسی‌های تلگرام (شامل تمام کاراکترهای بعد از علامت سوال)
        proxies = list(set(re.findall(r'https?://t\.me/proxy\?[\w=&%.!*()+-]+', res.text)))
        
        # الگوی دقیق برای V2Ray (تا جایی که فاصله یا کاراکتر غیرمجاز دیده نشه)
        v2rays = list(set(re.findall(r'(?:vless|vmess|ss|trojan)://[^\s<"\'&]+', res.text)))

        # ساخت پوشه و ذخیره فایل‌ها
        os.makedirs("telegram", exist_ok=True)
        
        with open("telegram/proxy.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(proxies))
            
        with open("telegram/v2ray.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(v2rays))
            
        print(f"Done! Found {len(proxies)} proxies and {len(v2rays)} v2ray configs.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    start()
