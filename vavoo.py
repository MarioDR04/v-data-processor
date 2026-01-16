import requests

def generate_m3u():
    url = "https://www2.vavoo.to/live2/index"
    params = {"output": "json"}
    headers = {'User-Agent': 'VAVOO/2.6'}
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=30)
        if response.status_code != 200:
            print("Erro ao acessar API")
            return

        data = response.json()
        m3u_content = "#EXTM3U\n"
        
        for item in data:
            name = item.get('name')
            group = item.get('group')
            logo = item.get('logo')
            url_original = item.get('url')
            
            # Extraímos o ID do canal (ex: 12345.ts)
            channel_id = url_original.split('/')[-1]
            
            # Montamos um link "virgem". 
            # O OTT Navigator vai ter que pedir a chave sozinho.
            m3u_content += f'#EXTINF:-1 tvg-logo="{logo}" group-title="{group}",{name}\n'
            m3u_content += f'https://vavoo.to/live2/{channel_id}|User-Agent=VAVOO/2.6\n'
        
        with open("lista.m3u", "w", encoding="utf-8") as f:
            f.write(m3u_content)
        print("Lista de IDs gerada com sucesso!")

    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    generate_m3u()
