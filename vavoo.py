import requests

def generate_m3u():
    # URL da API de canais
    url = "https://www2.vavoo.to/live2/index"
    # Precisamos de uma chave base para a URL não dar 404
    # Vamos usar a estrutura de stream oficial
    
    try:
        response = requests.get(url, params={"output": "json"}, timeout=30)
        data = response.json()
        m3u_content = "#EXTM3U\n"
        
        for item in data:
            name = item.get('name')
            group = item.get('group')
            logo = item.get('logo')
            # Extraímos o ID e mantemos o link original, mas formatado
            url_raw = item.get('url')
            
            # Adicionamos a sintaxe que o OTT Navigator usa para injetar Headers
            # Isso força o player a se comportar como o app do Vavoo
            m3u_content += f'#EXTINF:-1 tvg-logo="{logo}" group-title="{group}",{name}\n'
            m3u_content += f'{url_raw}|User-Agent=VAVOO/2.6&Service-Agent=okhttp/4.9.0\n'
        
        with open("lista.m3u", "w", encoding="utf-8") as f:
            f.write(m3u_content)
        print("Lista atualizada!")

    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    generate_m3u()
