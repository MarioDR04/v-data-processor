import requests
import json
import time

# --- Lógica extraída do seu utils.py ---
def get_auth_signature():
    try:
        _headers = {
            "user-agent": "okhttp/4.11.0",
            "accept": "application/json",
            "content-type": "application/json; charset=utf-8"
        }
        # Dados do dispositivo simulado para gerar a assinatura
        _data = {
            "token": "tosFwQCJMS8qrW_AjLoHPQ41646J5dRNha6ZWHnijoYQQQoADQoXYSo7ki7O5-CsgN4CH0uRk6EEoJ0728ar9scCRQW3ZkbfrPfeCXW2VgopSW2FWDqPOoVYIuVPAOnXCZ5g",
            "reason": "app-blur",
            "metadata": {
                "device": {"type": "Handset", "brand": "google", "model": "Nexus", "name": "21081111RG", "uniqueId": "d10e5d99ab665233"},
                "os": {"name": "android", "version": "7.1.2"},
                "app": {"platform": "android", "version": "3.1.20"}
            }
        }
        req = requests.post('https://www.vavoo.tv/api/app/ping', json=_data, headers=_headers, timeout=20).json()
        return req.get("addonSig")
    except Exception as e:
        print(f"Erro ao obter assinatura: {e}")
        return None

# --- Lógica de geração da lista M3U ---
def generate_m3u():
    # 1. Obtém a assinatura dinâmica
    sig = get_auth_signature()
    if not sig:
        print("Não foi possível obter a assinatura. Abortando.")
        return

    # 2. Busca a lista de canais
    url_channels = "https://www2.vavoo.to/live2/index?output=json"
    try:
        channels = requests.get(url_channels, timeout=20).json()
        
        m3u_content = "#EXTM3U\n"
        
        for c in channels:
            name = c.get("name")
            group = c.get("group")
            logo = c.get("logo")
            url = c.get("url")
            
            # 3. Monta a URL com a assinatura necessária para evitar erro 502/404
            # O link precisa do token ?n=1&sig=...
            signed_url = f"{url}?n=1&sig={sig}"
            
            # Formatação para o OTT Navigator com User-Agent correto
            m3u_content += f'#EXTINF:-1 tvg-logo="{logo}" group-title="{group}",{name}\n'
            m3u_content += f'{signed_url}|User-Agent=okhttp/4.11.0\n'

        with open("lista.m3u", "w", encoding="utf-8") as f:
            f.write(m3u_content)
        
        print(f"Lista gerada com sucesso! Signature: {sig[:10]}...")

    except Exception as e:
        print(f"Erro ao processar canais: {e}")

if __name__ == "__main__":
    generate_m3u()
