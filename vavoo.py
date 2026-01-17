import requests
import time
import hashlib
import json

CHANNELS_URL = "https://www2.vavoo.to/live2/index?output=json"
USER_AGENT = "VAVOO/2.6"


def get_ts_signature():
    """
    Replica o método gettsSignature() usado no vjlive.py
    """
    ts = int(time.time())
    secret = "vavoo.to"
    raw = f"{ts}{secret}"
    sig = hashlib.md5(raw.encode("utf-8")).hexdigest()
    return f"{ts}-{sig}"


def resolve_vavoo_link(link):
    """
    Replica a lógica resolve_link() do vjlive.py (modo direto)
    """
    try:
        base = link.replace("vavoo-iptv", "live2")[:-12]
        auth = get_ts_signature()

        stream = f"{base}.ts?n=1&b=5&vavoo_auth={auth}"
        headers = {"User-Agent": USER_AGENT}

        r = requests.get(stream, headers=headers, timeout=10, stream=True)
        if r.status_code < 400:
            return stream
    except:
        pass

    return None


def generate_m3u():
    print("📡 A obter lista de canais...")
    channels = requests.get(CHANNELS_URL, timeout=20).json()

    m3u = ["#EXTM3U\n"]

    ok = 0
    fail = 0

    for c in channels:
        name = c.get("name")
        group = c.get("group", "VAVOO")
        logo = c.get("logo", "")
        url = c.get("url")

        if not url or "vavoo" not in url:
            continue

        stream = resolve_vavoo_link(url)

        if not stream:
            fail += 1
            continue

        m3u.append(
            f'#EXTINF:-1 tvg-logo="{logo}" group-title="{group}",{name}\n'
            f'{stream}|User-Agent={USER_AGENT}\n'
        )

        ok += 1
        print(f"✔ {name}")

    with open("vavoo.m3u", "w", encoding="utf-8") as f:
        f.writelines(m3u)

    print("\n✅ Lista criada com sucesso")
    print(f"✔ Streams válidos: {ok}")
    print(f"✖ Streams inválidos: {fail}")
    print("📄 Ficheiro: vavoo.m3u")


if __name__ == "__main__":
    generate_m3u()
