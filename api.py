import requests
import json
import genshin

class GenshinAPIClient:
    def __init__(self, cookies, uid):
        self.client = genshin.Client(cookies=cookies)
        self.uid = uid

    async def get_user_data(self):
        user = await self.client.get_full_genshin_user(self.uid)
        return user
    
    async def get_wish_history(self):
        wishes = await self.client.wish_history()
        return wishes

# URLs pour les API Hoyolab, SG Public API et Minor API
base_url_hoyolab = "https://bbs-api-os.hoyolab.com/"
base_url_sg = "https://sg-public-api.hoyolab.com"
base_url_minor = "https://minor-api-os.hoyoverse.com/"

# Cookies pour l'authentification
cookies = {
    'ltuid': '111918821',  # Remplacer par votre ltuid
    'ltoken': 'v2_CAISDGM5b3FhcTNzM2d1OBokMDdmYjAwOGQtODZhOS00YTExLWI2ODYtOGQyZTEzZjUxNjczINzIhLoGKJT7uKEHMOX9rjVCC2Jic19vdmVyc2Vh.XCRBZwAAAAAB.MEQCIA90lI0p2w38NOSK626vxS4UvpLkYPAE_jMkmJ49ZKybAiB4CknQYaHEjZA3soWvFhpvNB5QLVm0dT_wrp22ypQ0bA',  # Remplacer par votre ltoken
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Cookie': f"ltuid={cookies['ltuid']}; ltoken={cookies['ltoken']};"
}

# Fonction pour récupérer les informations utilisateur depuis l'API Hoyolab
def fetch_user_info():
    user_info_url = f"{base_url_hoyolab}user/info"
    
    try:
        response = requests.get(user_info_url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            return data  # Retourne les informations utilisateur au format JSON
        else:
            print(f"Erreur lors de la récupération des informations utilisateur : {response.status_code}")
            return None
    except Exception as e:
        print(f"Une erreur s'est produite lors de la récupération des informations utilisateur : {e}")
        return None

# Fonction pour récupérer l'historique des vœux depuis l'API Hoyolab
def fetch_wish_history():
    wish_history_url = f"{base_url_hoyolab}account/wish/history"
    
    try:
        response = requests.get(wish_history_url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            return data  # Retourne l'historique des vœux au format JSON
        else:
            print(f"Erreur lors de la récupération de l'historique des vœux : {response.status_code}")
            return None
    except Exception as e:
        print(f"Une erreur s'est produite lors de la récupération de l'historique des vœux : {e}")
        return None

# Fonction pour récupérer des données depuis l'API SG Public
def fetch_sg_public_data(endpoint, params=None):
    """
    Récupérer des données depuis l'API SG Public.
    
    :param endpoint: L'endpoint à accéder (ex. '/some/endpoint')
    :param params: Paramètres optionnels à envoyer avec la requête (ex. {'uid': '123'}).
    :return: Données JSON si succès, None sinon.
    """
    url = f"{base_url_sg}{endpoint}"
    try:
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"Erreur lors de la récupération des données depuis SG Public API : {response.status_code}")
            return None
    except Exception as e:
        print(f"Une erreur s'est produite lors de la récupération des données depuis SG Public API : {e}")
        return None

# Fonction pour récupérer des données depuis l'API Minor
def fetch_minor_api_data(endpoint, params=None):
    """
    Récupérer des données depuis l'API Minor.
    
    :param endpoint: L'endpoint à accéder (ex. '/some/endpoint')
    :param params: Paramètres optionnels à envoyer avec la requête (ex. {'uid': '123'}).
    :return: Données JSON si succès, None sinon.
    """
    url = f"{base_url_minor}{endpoint}"
    try:
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"Erreur lors de la récupération des données depuis Minor API : {response.status_code}")
            return None
    except Exception as e:
        print(f"Une erreur s'est produite lors de la récupération des données depuis Minor API : {e}")
        return None
