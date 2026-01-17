import requests
import time
import hashlib

API_URL = "https://www2.vavoo.to/live2/index?output=json"
USER_AGENT = "VAVOO/2.6"
OUTPUT_FILE = "lista.m3u"


def get_ts_signature():
    ts = int(time.time())
    secret = "vavoo.to"
    sig = hashlib.md5(f"{ts}{secret}".encode()).hexdigest()
    return f"{ts}-{sig}"


def generate_m3u():
    try:
        print("📡 A obter lista de canais...")

        response = requests.get(
            API_URL,
            headers={"User-Agent": USER_AGENT},
            timeout=15
        )
        response.raise_for_status()
        channels = response.json()

        m3u_content = "#EXTM3U\n"
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

            m3u_content += (
                f'#EXTINF:-1 tvg-logo="{logo}" group-title="{group}",{name}\n'
                f'{stream}|User-Agent={USER_AGENT}\n'
            )

        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(m3u_content)

        print("✅ Lista M3U gerada com sucesso!")

    except Exception as e:
        print(f"❌ Erro ao gerar: {e}")


if __name__ == "__main__":
    generate_m3u()
