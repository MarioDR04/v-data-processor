import requests

def generate_m3u():
    # API para pegar os IDs reais
    url = "https://www2.vavoo.to/live2/index"
    
    try:
        # User-Agent necessário para a API responder ao GitHub
        headers = {'User-Agent': 'VAVOO/2.6'}
        response = requests.get(url, params={"output": "json"}, headers=headers, timeout=30)
        data = response.json()
        
        m3u_content = "#EXTM3U\n"
        
        for item in data:
            name = item.get('name')
            group = item.get('group')
            logo = item.get('logo')
            url_raw = item.get('url')
            
            # O SEGREDO: Formatar para o OTT Navigator injetar os headers em cada play
            # Adicionamos o Service-Agent que é o que valida o streaming
            m3u_content += f'#EXTINF:-1 tvg-logo="{logo}" group-title="{group}",{name}\n'
            m3u_content += f'{url_raw}|User-Agent=VAVOO/2.6&http-user-agent=VAVOO/2.6&Service-Agent=okhttp/4.9.0\n'
        
        with open("lista.m3u", "w", encoding="utf-8") as f:
            f.write(m3u_content)
        print("Lista gerada com headers de bypass!")

    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    generate_m3u()
