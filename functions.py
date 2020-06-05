import pytube
from termcolor import cprint
from utils import show_progress_download
from config.cfg import cfg


def _save_audio(audio):
    """
    Saves audio to disk
    :param audio: ``pytube.streams.Stream``
    """
    if not isinstance(audio, pytube.streams.Stream):
        raise TypeError('expect {}, but get {}'.format(pytube.streams.Stream.__name__, type(audio)))
    song_name = audio.default_filename
    cprint('SONG NAME --- {}'.format(song_name), 'yellow',
           attrs=['bold', 'underline', 'reverse'])

    audio.download(output_path=cfg.OUT_DIR)
    cprint('Complete: {}/{}'.format(cfg.OUT_DIR, song_name), 'green',
           attrs=['bold', 'underline', 'reverse'])


def download_audio(url):
    """
    Downloads audio from youtube video
    :param url: video url
    """
    youtub = pytube.YouTube(url, on_progress_callback=show_progress_download)
    audio = youtub.streams.filter(only_audio=True).all()
    _save_audio(audio[0])


def download_playlist(url):
    """
    Downloads playlist from youtube
    :param url: playlist url
    """
    playlist = pytube.Playlist(url)
    for video_url in playlist.video_urls:
        download_audio(video_url)
