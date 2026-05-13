import requests
from bs4 import BeautifulSoup
import re
import os
from datetime import datetime

# لیست کانال‌های هدف
CHANNELS = [
    "proxymtprotoir",
    "kakajan",
    "Proxyking007"
]

# مسیر فایل‌ها
PROXY_FILE = "telegram/proxy.txt"
V2RAY_FILE = "telegram/v2ray.txt"

def ensure_directory():
    if not os.path.exists("telegram"):
        os.makedirs("telegram")

def is_new_day():
    """چک می‌کند که آیا اولین اجرای امروز است یا خیر"""
    last_run_file = ".last_run"
    today = datetime.utcnow().strftime('%Y-%m-%d')
    
    if not os.path.exists(last_run_file):
        with open(last_run_file, "w") as f:
            f.write(today)
        return True
    
    with open(last_run_file, "r") as f:
        last_date = f.read().strip()
    
    if last_date != today:
        with open(last_run_file, "w") as f:
            f.write(today)
        return True
    return False

def clear_files():
    """پاکسازی فایل‌ها در ابتدای روز"""
    open(PROXY_FILE, 'w').close()
    open(V2RAY_FILE, 'w').close()
    print("Files cleared for the new day.")

def scrape_telegram():
    ensure_directory()
    
    if is_new_day():
        clear_files()

    all_proxies = []
    all_v2ray = []

    for channel in CHANNELS:
        print(f"Scraping {channel}...")
        url = f"https://t.me/s/{channel}"
        try:
            response = requests.get(url, timeout=15)
            soup = BeautifulSoup(response.text, 'html.parser')
            messages = soup.find_all('div', class_='tgme_widget_message_wrap')

            for msg in messages:
                text_area = msg.find('div', class_='tgme_widget_message_text')
                if not text_area:
                    continue
                
                content = text_area.get_text(separator="\n")
                
                # بررسی وجود لینک‌های خاص در متن یا اتچمنت‌ها
                links = re.findall(r'(vmess://[^\s]+|vless://[^\s]+|trojan://[^\s]+|ss://[^\s]+|tg://proxy[^\s]+|https://t.me/proxy\?[^\s]+)', content)
                
                # شناسایی فایل‌های .npvt
                docs = msg.find_all('a', class_='tgme_widget_message_document_wrap')
                for doc in docs:
                    doc_name = doc.find('div', class_='tgme_widget_message_document_name')
                    if doc_name and ".npvt" in doc_name.text:
                        doc_link = doc.get('href')
                        content += f"\n[NAPSTERNETV FILE]: https://t.me{doc_link}"

                # دسته‌بندی
                is_v2ray = any(x in content.lower() for x in ['vmess', 'vless', 'trojan', 'ss://'])
                is_proxy = any(x in content.lower() for x in ['tg://proxy', 'https://t.me/proxy', 'socks', 'http'])

                separator = "\n" + "="*30 + "\n"
                formatted_post = f"{content}{separator}"

                if is_v2ray:
                    all_v2ray.append(formatted_post)
                if is_proxy:
                    all_proxies.append(formatted_post)

        except Exception as e:
            print(f"Error scraping {channel}: {e}")

    # ذخیره در فایل (Append mode)
    with open(PROXY_FILE, "a", encoding="utf-8") as f:
        f.writelines(all_proxies)
    
    with open(V2RAY_FILE, "a", encoding="utf-8") as f:
        f.writelines(all_v2ray)

if __name__ == "__main__":
    scrape_telegram()
