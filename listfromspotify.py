from spotipy.oauth2 import SpotifyClientCredentials
import config
import pathlib
import spotipy
import click
import re

client_credentials_manager = SpotifyClientCredentials(
    client_id=config.SPOTIFY_CLIENT_ID,
    client_secret=config.SPOTIFY_CLIENT_SECRET
)

sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

@click.command()
@click.argument('playlist_link')
def main(playlist_link):
    username = playlist_link.split('/')[-3]
    playlist_id = playlist_link.split('/')[-1]

    results = sp.user_playlist(username, playlist_id)

    tracks = results['tracks']
    display_tracks(tracks)

    while tracks['next']:
        tracks = sp.next(tracks)
        display_tracks(tracks)


def display_tracks(tracks):
    for track in tracks['items']:
        # spotify likes to use dashes instead of parentheses for remixes
        title = re.sub('\s-\s([\w\.\?\&\s]+?\sremix)$', ' (\g<1>)', track['track']['name'], flags=re.I)
        artists = ', '.join(a['name'] for a in track['track']['artists'])
        click.echo('{} - {}'.format(artists, title))


if __name__ == '__main__':
    main()
