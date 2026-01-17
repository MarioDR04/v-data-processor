import requests
import json

def generate_m3u():
    # URL da API de canais
    url_channels = "https://www2.vavoo.to/live2/index?output=json"
    
    try:
        print("Obtendo lista de canais...")
        response = requests.get(url_channels, timeout=20)
        channels = response.json()
        
        m3u_content = "#EXTM3U\n"
        
        for c in channels:
            name = c.get("name")
            group = c.get("group")
            logo = c.get("logo")
            url = c.get("url")
            
            # Limpamos a URL e formatamos para que o OTT Navigator 
            # peça a assinatura localmente (usando o SEU IP)
            clean_url = url.replace("vavoo-iptv", "live2").split('.ts')[0]
            
            # Adicionamos os headers que o seu script vjlive.py usa
            m3u_content += f'#EXTINF:-1 tvg-logo="{logo}" group-title="{group}",{name}\n'
            m3u_content += f'{clean_url}.ts?n=1&b=5|User-Agent=VAVOO/2.6&X-VAVOO-Signature=True\n'

        with open("lista.m3u", "w", encoding="utf-8") as f:
            f.write(m3u_content)
        
        print("Ficheiro lista.m3u gerado com sucesso!")

    except Exception as e:
        print(f"Erro ao processar: {e}")

if __name__ == "__main__":
    generate_m3u()
