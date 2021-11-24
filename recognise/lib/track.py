from dataclasses import dataclass, field
from typing import List, Optional
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials


@dataclass
class Track:
    title: str
    artist: str
    show: str
    # year: Optional[str] = field(init=False)
    # length: Optional[int] = field(init=False)
    genres: List[str] = field(default_factory=list, init=False)

    _spotify = Spotify(auth_manager=SpotifyClientCredentials())

    def __post_init__(self):
        tracks = self.__search_track__()

        if(len(tracks) > 0):
            t = tracks[0]

            album = self.__search_album__(t['album']['id'])
            self.genres = album['genres']
            # add year
            # add length

            if(len(self.genres) == 0):
                artist = self.__search_artist__(t['artists'][0]['id'])
                self.genres = artist['genres']

    def __search_track__(self):
        query = f'track:{self.title} artist:{self.artist}'
        return self._spotify.search(q=query, type='track')['tracks']['items']

    def __search_album__(self, album_id):
        return self._spotify.album(album_id)

    def __search_artist__(self, artist_id):
        return self._spotify.artist(artist_id)
