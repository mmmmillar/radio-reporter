import pytest
from recognise import index


@pytest.mark.asyncio
async def test_get_shazam_track_info():
    track_info = await index.get_shazam_track_info('tests/whatsgood.mp3')

    assert track_info.title == "WHAT'S GOOD"
    assert track_info.subtitle == 'Tyler, The Creator'


def test_get_spotify_track_info_genres():
    track_info = index.get_spotify_track_info(
        "WHAT'S GOOD", 'Tyler, The Creator')

    assert track_info['genres'] == ['hip hop', 'rap']
