import requests

def generate_m3u():
    url = "https://www2.vavoo.to/live2/index"
    params = {"output": "json"}
    
    try:
        print("Buscando canais...")
        response = requests.get(url, params=params, timeout=30)
        if response.status_code != 200:
            return

        data = response.json()
        m3u_content = "#EXTM3U\n"
        
        for item in data:
            name = item.get('name', 'Sem Nome')
            group = item.get('group', 'Vavoo')
            logo = item.get('logo', '')
            stream_url = item.get('url')
            
            m3u_content += f'#EXTINF:-1 tvg-logo="{logo}" group-title="{group}",{name}\n'
            m3u_content += f'{stream_url}\n'
        
        with open("lista.m3u", "w", encoding="utf-8") as f:
            f.write(m3u_content)
        print("Lista gerada com sucesso!")

    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    generate_m3u()
