import requests

def generate_m3u():
    # API alternativa que lida melhor com tokens
    url = "https://www2.vavoo.to/live2/index"
    params = {"output": "json"}
    
    try:
        response = requests.get(url, params=params, timeout=30)
        data = response.json()
        m3u_content = "#EXTM3U\n"
        
        for item in data:
            name = item.get('name')
            group = item.get('group')
            logo = item.get('logo')
            url_original = item.get('url')
            
            # Adicionamos um User-Agent de Smart TV para evitar o erro 502
            # E formatamos a URL para passar o token corretamente
            m3u_content += f'#EXTINF:-1 tvg-logo="{logo}" group-title="{group}",{name}\n'
            m3u_content += f'{url_original}|User-Agent=VAVOO/2.6\n'
        
        with open("lista.m3u", "w", encoding="utf-8") as f:
            f.write(m3u_content)
            
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    generate_m3u()
