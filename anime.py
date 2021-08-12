import decimal
from typing import Dict

import requests
from bs4 import BeautifulSoup


class Anime:
    """A class contaning different information about an anime."""

    def __init__(self, name=None, eng_name=None, score=None, rank=None,
                 popularity=None, episodes=None, summary=None) -> None:
        """

        """
        self.name = name
        self.eng_name = eng_name
        self.score = score
        self.rank = rank
        self.popularity = popularity
        self.episodes = episodes
        self.summary = summary

        self._mal_id = 0
        self._url = ''
        self._cover = ''
        self._elements = {}
        self._airing = False

    def __str__(self) -> str:
        """Return a string representation of the anime.

        >>> naruto = Anime('Naruto', 'Naruto', 7.92, 660, 8)
        >>> print(naruto)
        Name: Naruto
        English Name: Naruto
        Score: 7.92
        Ranking: #660
        Popularity: #8
        >>> aot = Anime('Shingeki no Kyojin', 'Attack on Titan', 8.50, 103, 2)
        >>> print(aot)
        Name: Shingeki no Kyojin
        English Name: Attack on Titan
        Score: 8.50
        Ranking: #103
        Popularity: #2
        """
        return f'Name: {self.name}\n' \
               f'English Name: {self.eng_name}\n' \
               f'Score: {round(decimal.Decimal(self.score), 2)}\n' \
               f'Ranking: #{self.rank}\n' \
               f'Popularity: #{self.popularity}'

    def get_mal_id(self) -> int:
        """Return the MAL id of the anime.
        """
        return self._mal_id

    def get_mal_url(self) -> str:
        """Return the MAL url of the anime.
        """
        return self._url

    def get_cover(self) -> str:
        """Return the cover image of the anime.
        """
        return self._cover

    def get_elements(self) -> Dict[str, str]:
        """Return a dictionary containing all elements scraped.
        """
        element_dict = {'Name': self.name,
                        'English Name': self.eng_name,
                        'Score': self.score,
                        'Rank': self.rank,
                        'Popularity': self.popularity,
                        'Episodes': self.episodes,
                        'Summary': self.summary}
        return element_dict

    def get_gogo_urls(self) -> Dict[int, str]:
        """Return a dictionary containing links to watch the anime.

        >>> aot = Anime('Shingeki no Kyojin', 'Attack on Titan', 8.50, 103, 2, 25)
        >>> aot.get_gogo_urls()
        {1: 'https://www1.gogoanime.ai/shingeki-no-kyojin-episode-1',
        2: 'https://www1.gogoanime.ai/shingeki-no-kyojin-episode-2',
        3: 'https://www1.gogoanime.ai/shingeki-no-kyojin-episode-3',
        4: 'https://www1.gogoanime.ai/shingeki-no-kyojin-episode-4',
        5: 'https://www1.gogoanime.ai/shingeki-no-kyojin-episode-5',
        6: 'https://www1.gogoanime.ai/shingeki-no-kyojin-episode-6',
        7: 'https://www1.gogoanime.ai/shingeki-no-kyojin-episode-7',
        8: 'https://www1.gogoanime.ai/shingeki-no-kyojin-episode-8',
        9: 'https://www1.gogoanime.ai/shingeki-no-kyojin-episode-9',
        10: 'https://www1.gogoanime.ai/shingeki-no-kyojin-episode-10',
        11: 'https://www1.gogoanime.ai/shingeki-no-kyojin-episode-11',
        12: 'https://www1.gogoanime.ai/shingeki-no-kyojin-episode-12',
        13: 'https://www1.gogoanime.ai/shingeki-no-kyojin-episode-13',
        14: 'https://www1.gogoanime.ai/shingeki-no-kyojin-episode-14',
        15: 'https://www1.gogoanime.ai/shingeki-no-kyojin-episode-15',
        16: 'https://www1.gogoanime.ai/shingeki-no-kyojin-episode-16',
        17: 'https://www1.gogoanime.ai/shingeki-no-kyojin-episode-17',
        18: 'https://www1.gogoanime.ai/shingeki-no-kyojin-episode-18',
        19: 'https://www1.gogoanime.ai/shingeki-no-kyojin-episode-19',
        20: 'https://www1.gogoanime.ai/shingeki-no-kyojin-episode-20',
        21: 'https://www1.gogoanime.ai/shingeki-no-kyojin-episode-21',
        22: 'https://www1.gogoanime.ai/shingeki-no-kyojin-episode-22',
        23: 'https://www1.gogoanime.ai/shingeki-no-kyojin-episode-23',
        24: 'https://www1.gogoanime.ai/shingeki-no-kyojin-episode-24',
        25: 'https://www1.gogoanime.ai/shingeki-no-kyojin-episode-25'}
        """
        if not self._airing:
            anime_name = self.remove_non_alnum()
            gogo_prefix = f'https://www1.gogoanime.ai/{anime_name}-episode-'
            episodes = {}

            # Test to see if it exists
            flag = does_link_exist(gogo_prefix + '1')

            # If link exists, proceed
            if flag:
                for i in range(1, self.episodes + 1):
                    episodes[i] = gogo_prefix + str(i)
            # If link does not exist, try again with the English name
            else:
                anime_name = self.remove_non_alnum(self.eng_name)
                gogo_prefix = f'https://www1.gogoanime.ai/{anime_name}-episode-'
                for i in range(1, self.episodes + 1):
                    episodes[i] = gogo_prefix + str(i)

            return episodes
        else:
            return {1: f'https://www1.gogoanime.ai/category/{self.remove_non_alnum()}'}

    def remove_non_alnum(self, eng_name=None) -> str:
        """Return a new string containing the name of an anime with all
        non-alphanumeric characters removed.

        >>> aot = Anime('Shingeki no Kyojin', 'Attack on Titan', 8.50, 103, 2, 25)
        >>> s = aot.remove_non_alnum()
        >>> s
        'shingeki-no-kyojin'
        """
        refined_name = ''
        if eng_name is None:
            for letter in self.name:
                if letter.isalnum():
                    refined_name = refined_name + letter
                elif letter == ' ':
                    refined_name = refined_name + '-'
        else:
            for letter in self.eng_name:
                if letter.isalnum():
                    refined_name = refined_name + letter
                elif letter == ' ':
                    refined_name = refined_name + '-'

        return refined_name.lower()

    def grab_gogo_video(self, episode: int) -> str:
        """Return the direct link to a video of the anime episode.

        >>> aot = Anime('Shingeki no Kyojin', 'Attack on Titan', 8.50, 103, 2, 25)
        >>> aot.grab_gogo_video(1)
        https://storage.googleapis.com/red-shape-309906/KPJ8P13R11LD/22a_1618594291_2633.mp4
        """
        gogo_links = self.get_gogo_urls()
        ep = gogo_links[episode]

        page = requests.get(ep)
        soup = BeautifulSoup(page.content, 'html.parser')
        dl_link = soup.find("div", {"class": "favorites_book"}).find('li').find('a').get('href')

        page = requests.get(dl_link)
        soup = BeautifulSoup(page.content, 'html.parser')
        vid_link = str(soup.find("div", {"class": "mirror_link"}).find("div", {"class": "dowload"}).find('a').get('href'))

        return vid_link

    def is_airing(self) -> bool:
        """Return whether the anime is airing or not.

        >>> bokutachi = Anime('Bokutachi no remake', 'Remake our Life!', 7.94, 622, 1621)
        >>> bokutachi.is_airing()
        True
        """
        return self._airing


def does_link_exist(link: str) -> bool:
    """

    :return:
    """
    page = requests.get(link)
    soup = BeautifulSoup(page.content, 'html.parser')
    check = soup.find("h1", {"class": "entry-title"})

    if '404' in str(check):
        return False
    else:
        return True
