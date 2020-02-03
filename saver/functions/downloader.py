import pytube
import os
from pytube import YouTube
from config.cfg import cfg
from saver.functions import utils
from termcolor import cprint
from pydub import AudioSegment
from tqdm import tqdm
from pathlib import Path


def song_dict(path):
    """
    Get path to song
    :param path: path to directory where song stored
    :return: full path to song
    """
    for name in os.listdir(path):
        yield os.path.join(path, name)


def download_audio_list(url_list):
    """Download audio from YouTube
    :param url_list: list of urls videos
    """
    for url in url_list:
        youtube = YouTube(url, on_progress_callback=utils.show_progress_download)
        audio = youtube.streams.filter(only_audio=True).all()
        save_audio(audio[0])

    cprint('DONE', 'green',
           attrs=['bold', 'underline', 'reverse', 'blink'])


def convert_audios(path, out_path, song_format):
    """
    :param path: path to directory
    :param out_path: output path
    :param song_format: song format
    """
    for path in tqdm(song_dict(path), total=len(os.listdir(path))):
        try:
            print(path)
            song = AudioSegment.from_file(path)
        except FileNotFoundError:
            cprint('{} NOT FOUND'.format(path), 'red',
                   attrs=['bold', 'underline', 'reverse'])
            continue
        else:
            song.export(os.path.join(out_path, 'song.mp3'), format=song_format)


def save_audio(audio):
    if not isinstance(audio, pytube.streams.Stream):
        raise TypeError('expect {}, but get {}'.format(pytube.streams.Stream.__name__, type(audio)))
    song_name = audio.default_filename
    cprint('SONG NAME --- {}'.format(song_name), 'yellow',
           attrs=['bold', 'underline', 'reverse'])

    audio.download(cfg.PATH)
    cprint('Complete: {}/{}'.format(cfg.PATH, song_name), 'green',
           attrs=['bold', 'underline', 'reverse'])


def post_process_audios(song_list):
    pass


def cut_song(song):
    pass
