import requests
from bs4 import BeautifulSoup
import re
import os
import socket
from datetime import datetime
from urllib.parse import urlparse

# تنظیمات
CHANNELS = ["proxymtprotoir", "kakajan", "Proxyking007"]
PROXY_FILE = "telegram/proxy.txt"
V2RAY_FILE = "telegram/v2ray.txt"
TIMEOUT = 5  # زمان انتظار برای تست هر سرور (ثانیه)

def ensure_directory():
    if not os.path.exists("telegram"):
        os.makedirs("telegram")

def is_alive(host, port):
    """بررسی باز بودن پورت سرور (TCP Check)"""
    try:
        with socket.create_connection((host, int(port)), timeout=TIMEOUT):
            return True
    except:
        return False

def extract_ip_port(link):
    """استخراج IP و Port از انواع لینک‌ها"""
    try:
        if "server=" in link and "port=" in link: # MTProto
            host = re.search(r'server=([^&]+)', link).group(1)
            port = re.search(r'port=([^&]+)', link).group(1)
            return host, port
        elif "@" in link: # V2Ray / SS
            parts = link.split("@")[1].split(":")[0:2]
            host = parts[0]
            port = parts[1].split("?")[0].split("#")[0]
            return host, port
    except:
        return None, None
    return None, None

def is_new_day():
    last_run_file = ".last_run"
    today = datetime.utcnow().strftime('%Y-%m-%d')
    if not os.path.exists(last_run_file):
        with open(last_run_file, "w") as f: f.write(today)
        return True
    with open(last_run_file, "r") as f:
        if f.read().strip() != today:
            with open(last_run_file, "w") as f: f.write(today)
            return True
    return False

def scrape_telegram():
    ensure_directory()
    if is_new_day():
        open(PROXY_FILE, 'w').close()
        open(V2RAY_FILE, 'w').close()

    new_v2ray = []
    new_proxies = []

    for channel in CHANNELS:
        print(f"Checking {channel}...")
        try:
            response = requests.get(f"https://t.me/s/{channel}", timeout=15)
            soup = BeautifulSoup(response.text, 'html.parser')
            messages = soup.find_all('div', class_='tgme_widget_message_wrap')

            for msg in messages:
                text_area = msg.find('div', class_='tgme_widget_message_text')
                if not text_area: continue
                
                content = text_area.get_text(separator="\n")
                # پیدا کردن تمام لینک‌های حساس
                links = re.findall(r'(vmess://[^\s]+|vless://[^\s]+|trojan://[^\s]+|ss://[^\s]+|tg://proxy[^\s]+|https://t.me/proxy\?[^\s]+)', content)
                
                valid_links_in_post = []
                for link in links:
                    host, port = extract_ip_port(link)
                    if host and port:
                        if is_alive(host, port): # عملیات چک کردن
                            valid_links_in_post.append(link)
                
                if not valid_links_in_post: continue

                # فرمت‌بندی پست برای ذخیره
                separator = "\n" + "="*30 + "\n"
                clean_post = "\n".join(valid_links_in_post) + "\n\n--- Caption ---\n" + content + separator
                
                if any(x in valid_links_in_post[0] for x in ['vmess', 'vless', 'trojan', 'ss']):
                    new_v2ray.append(clean_post)
                else:
                    new_proxies.append(clean_post)

        except Exception as e:
            print(f"Error: {e}")

    # ذخیره نهایی
    with open(V2RAY_FILE, "a", encoding="utf-8") as f: f.writelines(new_v2ray)
    with open(PROXY_FILE, "a", encoding="utf-8") as f: f.writelines(new_proxies)

if __name__ == "__main__":
    scrape_telegram()
