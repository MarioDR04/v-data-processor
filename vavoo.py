import requests

def generate_m3u():
    # Buscamos a lista de IDs, não os links finais com token
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
            # Pegamos o ID do canal para montar um link que o OTT processe
            channel_id = item.get('url').split('/')[-1]
            
            # Criamos um link que obriga o player a usar o SEU IP para validar
            # Adicionamos a sintaxe de User-Agent que o OTT Navigator entende
            m3u_content += f'#EXTINF:-1 tvg-logo="{logo}" group-title="{group}",{name}\n'
            m3u_content += f'https://vavoo.to/live2/{channel_id}.ts|User-Agent=VAVOO/2.6\n'
        
        with open("lista.m3u", "w", encoding="utf-8") as f:
            f.write(m3u_content)
            
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    generate_m3u()
