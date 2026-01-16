import requests

def generate_m3u():
    url = "https://www2.vavoo.to/live2/index"
    params = {"output": "json"}
    headers = {'User-Agent': 'VAVOO/2.6'}
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=30)
        data = response.json()
        
        # Criamos uma lista que usa o protocolo oficial do Vavoo
        m3u_content = "#EXTM3U\n"
        
        for item in data:
            name = item.get('name')
            group = item.get('group')
            logo = item.get('logo')
            # Extraímos apenas o ID final
            url_raw = item.get('url')
            channel_id = url_raw.split('/')[-1].replace('.ts', '')
            
            m3u_content += f'#EXTINF:-1 tvg-logo="{logo}" group-title="{group}",{name}\n'
            # Link estruturado para forçar o player a pedir o token
            m3u_content += f'https://vavoo.to/live2/{channel_id}.ts?n=1\n'
        
        with open("lista.m3u", "w", encoding="utf-8") as f:
            f.write(m3u_content)
            
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    generate_m3u()
