import requests
import json
import os

def get_auth_signature():
    # Headers e dados extraídos exatamente do seu arquivo utils.py
    _headers = {
        "user-agent": "okhttp/4.11.0",
        "accept": "application/json",
        "content-type": "application/json; charset=utf-8",
        "accept-encoding": "gzip"
    }
    _data = {
        "token": "tosFwQCJMS8qrW_AjLoHPQ41646J5dRNha6ZWHnijoYQQQoADQoXYSo7ki7O5-CsgN4CH0uRk6EEoJ0728ar9scCRQW3ZkbfrPfeCXW2VgopSW2FWDqPOoVYIuVPAOnXCZ5g",
        "reason": "app-blur",
        "locale": "de",
        "theme": "dark",
        "metadata": {
            "device": {"type": "Handset", "brand": "google", "model": "Nexus", "name": "21081111RG", "uniqueId": "d10e5d99ab665233"},
            "os": {"name": "android", "version": "7.1.2", "abis": ["arm64-v8a", "armeabi-v7a", "armeabi"], "host": "android"},
            "app": {"platform": "android", "version": "3.1.20", "buildId": "289515000", "engine": "hbc85", "signatures": ["6e8a975e3cbf07d5de823a760d4c2547f86c1403105020adee5de67ac510999e"], "installer": "app.revanced.manager.flutter"},
            "version": {"package": "tv.vavoo.app", "binary": "3.1.20", "js": "3.1.20"}
        },
        "appFocusTime": 0, "playerActive": False, "playDuration": 0, "devMode": False, "hasAddon": True, "castConnected": False, "package": "tv.vavoo.app", "version": "3.1.20", "process": "app", "adblockEnabled": True
    }
    
    try:
        req = requests.post('https://www.vavoo.tv/api/app/ping', json=_data, headers=_headers, timeout=20)
        return req.json().get("addonSig")
    except:
        return None

def generate_m3u():
    sig = get_auth_signature()
    # Se a assinatura falhar, tentamos gerar sem ela para não deixar o arquivo vazio
    if not sig:
        print("Aviso: Assinatura não obtida, gerando links básicos.")
    
    try:
        # Busca os canais usando a URL do seu vavoo_tv.py
        channels = requests.get("https://www2.vavoo.to/live2/index?output=json", timeout=20).json()
        
        m3u_content = "#EXTM3U\n"
        for c in channels:
            name = c.get("name", "Unknown")
            group = c.get("group", "Vavoo")
            logo = c.get("logo", "")
            url = c.get("url")
            
            # Formatação do link com a assinatura e User-Agent do seu script
            final_url = f"{url}?n=1&sig={sig}" if sig else url
            m3u_content += f'#EXTINF:-1 tvg-logo="{logo}" group-title="{group}",{name}\n'
            m3u_content += f'{final_url}|User-Agent=okhttp/4.11.0\n'

        with open("lista.m3u", "w", encoding="utf-8") as f:
            f.write(m3u_content)
        print("Arquivo lista.m3u criado com sucesso!")

    except Exception as e:
        print(f"Erro ao gerar lista: {e}")

if __name__ == "__main__":
    generate_m3u()
