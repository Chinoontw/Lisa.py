import typing

# Définition de DBChar qui est un NamedTuple pour représenter un personnage
class DBChar(typing.NamedTuple):
    """Partial genshin character data."""
    
    id: int  # Identifiant unique du personnage
    icon_name: str  # Nom de l'icône standardisée
    name: str  # Nom du personnage (localisé)
    element: str  # Élément (Anemo, Pyro, etc.)
    rarity: int  # Rareté du personnage (en étoiles, 5 pour 5 étoiles, etc.)
    
    guessed: bool = False  # Indicateur si le personnage a été deviné ou ajouté manuellement

# Dictionnaire contenant les informations des personnages
CHARACTER_NAMES: typing.Dict[str, typing.Dict[int, DBChar]] = {
    "en-us": {  # Langue anglaise
        10000001: DBChar(id=10000001, icon_name="char_icon_01", name="Traveler", element="Anemo", rarity=5),
        10000002: DBChar(id=10000002, icon_name="char_icon_02", name="Amber", element="Pyro", rarity=4),
        10000003: DBChar(id=10000003, icon_name="char_icon_03", name="Jean", element="Anemo", rarity=5),
        10000004: DBChar(id=10000004, icon_name="char_icon_04", name="Lisa", element="Electro", rarity=4),
        10000005: DBChar(id=10000005, icon_name="char_icon_05", name="Traveler", element="Geo", rarity=5),
        # Ajoutez ici d'autres personnages avec leurs données
        10000006: DBChar(id=10000006, icon_name="char_icon_06", name="Kaeya", element="Cryo", rarity=4),
        10000007: DBChar(id=10000007, icon_name="char_icon_07", name="Diluc", element="Pyro", rarity=5),
        10000008: DBChar(id=10000008, icon_name="char_icon_08", name="Fischl", element="Electro", rarity=4),
        10000009: DBChar(id=10000009, icon_name="char_icon_09", name="Zhongli", element="Geo", rarity=5),
        # Ajoutez plus de personnages ici...
    },
    # Vous pouvez ajouter d'autres langues si nécessaire, par exemple :
    # "fr-fr": {
    #     10000001: DBChar(id=10000001, icon_name="char_icon_01", name="Voyageur", element="Anémo", rarity=5),
    #     10000002: DBChar(id=10000002, icon_name="char_icon_02", name="Amber", element="Pyro", rarity=4),
    #     ...
    # },
}

# Exporter les constantes pour les rendre accessibles dans d'autres modules
__all__ = ["CHARACTER_NAMES", "DBChar"]
