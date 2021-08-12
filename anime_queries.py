import random
from anime import Anime

from jikanpy import Jikan

# **************************************************************************** #

mal_ids = []
id_file = open('mal_ids')

for item in id_file:
    mal_ids.append(item.strip())

# **************************************************************************** #

jikan = Jikan()

# **************************************************************************** #

def search_anime(name_query: str) -> Anime():
    """Return information about a user specified anime by searching for the
    anime via Jikan's API. Information is returned in the form of a dictionary.

    Information returned includes:
    - Anime name
    - English name (IF AVAILABLE)
    - MAL score
    - MAL URL
    - Anime cover
    """
    # Create a dictionary object which will contain the information
    anime_info = {}

    # Get MAL id of the anime
    mal_id = jikan.search('anime', name_query)['results'][0]['mal_id']

    return mal_id_query(mal_id)

# **************************************************************************** #

def random_anime() -> Anime():
    """Return information about a random anime by picking a random ID from the
    MyAnimeList database. Information is returned in the form of a dictionary.

    Information returned includes:
    - Anime name
    - English name (IF AVAILABLE)
    - MAL score
    - MAL URL
    - Anime cover
    """
    # Create a dictionary object which will contain the information
    anime_info = {}

    # Create random object
    r = random.SystemRandom()

    # Generate index to pick random anime id
    index = r.randint(1, len(mal_ids))

    # Pick random anime id
    mal_id = mal_ids[index]

    return mal_id_query(mal_id)

# **************************************************************************** #

def mal_id_query(mal_id: int) -> Anime():
    """
    """
    # Create a dictionary object which will contain the information
    anime_info = {}
    anime = Anime()

    # Get information based off <mal_id>
    anime_info_raw = jikan.anime(mal_id)

    # Add anime name to <anime>
    anime_info['title'] = anime_info_raw["title"]
    anime.name = anime_info_raw["title"]

    # Add English name to <anime>
    anime_info['title_english'] = anime_info_raw["title_english"]
    anime.eng_name = anime_info_raw["title_english"]

    # Add anime score to <anime>
    anime_info['score'] = anime_info_raw["score"]
    anime.score = anime_info_raw["score"]

    # Add anime episode count to <anime>
    if anime_info_raw["episodes"] is None:
        anime.episodes = 0
    else:
        anime.episodes = anime_info_raw["episodes"]

    # Add anime synopsis to <anime>
    anime.summary = anime_info_raw["synopsis"]

    # Add anime URL to <anime>
    anime_info['url'] = anime_info_raw["url"]
    anime._url = anime_info_raw["url"]

    # Add anime cover to <anime>
    anime_info['cover'] = anime_info_raw["image_url"]
    anime._cover = anime_info_raw["image_url"]

    # Add anime MAL id to <anime>
    anime_info['mal_id'] = anime_info_raw["mal_id"]
    anime._mal_id = anime_info_raw["mal_id"]

    # Check whether the anime is airing or not
    if anime_info_raw['airing']:
        anime._airing = True

    return anime

# **************************************************************************** #


def get_anime_cover(mal_id: int) -> str:

    return jikan.anime(mal_id)["image_url"]
