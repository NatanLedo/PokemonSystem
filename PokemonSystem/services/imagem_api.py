import requests

class ImagemAPI:

    def buscar_imagem(self, nome):

        nome = nome.strip().lower().replace(" ", "-")
        url = f"https://pokeapi.co/api/v2/pokemon/{nome}"
        resposta = requests.get(url, timeout=10)

        if resposta.status_code != 200:
            return None

        dados = resposta.json()
        imagem_url = dados["sprites"]["front_default"]

        if imagem_url is None:
            return None

        imagem = requests.get(imagem_url, timeout=10)

        if imagem.status_code == 200:
            return imagem.content

        return None