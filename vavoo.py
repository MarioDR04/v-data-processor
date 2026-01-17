import requests
import time
import hashlib

API_URL = "https://www2.vavoo.to/live2/index?output=json"
USER_AGENT = "VAVOO/2.6"
OUTPUT = "vavoo.m3u"


def get_ts_signature():
    """
    Assinatura simples (igual ao método usado no addon)
    """
    ts = int(time.time())
    secret = "vavoo.to"
    sig = hashlib.md5(f"{ts}{secret}".encode()).hexdigest()
    return f"{ts}-{sig}"


def generate_m3u():
    print("📡 A obter canais...")

    channels = requests.get(
        API_URL,
        headers={"User-Agent": USER_AGENT},
        timeout=15
    ).json()

    m3u = ["#EXTM3U\n"]
    auth = get_ts_signature()

    for c in channels:
        name = c.get("name")
        group = c.get("group", "VAVOO")
        logo = c.get("logo", "")
        url = c.get("url")

        if not url or "vavoo" not in url:
            continue

        base = url.replace("vavoo-iptv", "live2")[:-12]
        stream = f"{base}.ts?n=1&b=5&vavoo_auth={auth}"

        m3u.append(
            f'#EXTINF:-1 tvg-logo="{logo}" group-title="{group}",{name}\n'
            f'{stream}|User-Agent={USER_AGENT}\n'
        )

    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.writelines(m3u)

    print(f"✅ {OUTPUT} gerado com sucesso ({len(m3u)//2} canais)")


if __name__ == "__main__":
    generate_m3u()
