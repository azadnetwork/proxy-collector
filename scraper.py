import requests, re, os
def start():
    try:
        res = requests.get("https://t.me/s/proxymtprotoir")
        proxies = list(set(re.findall(r'https://t.me/proxy\?[\w=&%-]+', res.text)))
        v2rays = list(set(re.findall(r'(?:vless|vmess|ss|trojan)://[\w@.:/?#%\[\]-]+', res.text)))
        os.makedirs("telegram", exist_ok=True)
        with open("telegram/proxy.txt", "w") as f: f.write("\n".join(proxies))
        with open("telegram/v2ray.txt", "w") as f: f.write("\n".join(v2rays))
    except: pass
if __name__ == "__main__": start()
