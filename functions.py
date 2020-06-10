import pytube
import sys
from termcolor import cprint
from utils import show_progress_download
from config.cfg import cfg
from pydub import AudioSegment
from utils import get_time_code


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


# def cut_sound(time_code, path_to_audio):
#     """
#     Cuts sound
#     :param time_code: ``Tuple([start_mm, start_ss], [end_mm, end_ss])``
#     :param path_to_audio: ``str`` path to audio file
#     """
#     start, end = get_time_code(time_code)
#     current_format = path_to_audio.split('.')[-1]
#     audio_name = path_to_audio.split('/')[-1]
#
#     try:
#         start = list(map(int, start))
#         end = list(map(int, end))
#     except ValueError:
#         print('Unknown time code format')
#     except Exception:
#         print('Unexpected error:', sys.exc_info()[0])
#     else:
#         start_time = start[0] * 60 * 1000 + start[1] * 1000
#         end_time = end[0] * 60 * 1000 + end[1] * 1000
#
#     try:
#         sound = AudioSegment.from_file(path_to_audio)
#     except FileNotFoundError:
#         print('Sound not found, get path {}'.format(path_to_audio))
#     else:
#         extract = sound[start_time:end_time]
#         extract.export(cfg.OUT_DIR + '/' + audio_name, format=current_format)
