import pytube
import os
from pytube import YouTube
from config.cfg import cfg
from saver.functions import utils
from termcolor import cprint
from pydub import AudioSegment
from tqdm import tqdm


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
    Converts song to specified format
    :param path: path to directory
    :param out_path: output path
    :param song_format: song format
    """
    for path in tqdm(song_dict(path), total=len(os.listdir(path))):
        try:
            song = AudioSegment.from_file(path)
        except FileNotFoundError:
            cprint('{} NOT FOUND'.format(path), 'red',
                   attrs=['bold', 'underline', 'reverse'])
            continue
        else:
            song.export(os.path.join(out_path, 'song.{}'.format(song_format)), format=song_format)


def save_audio(audio):
    """
    Saves audio
    :param audio: instance of pytube.streams.Stream
    """
    if not isinstance(audio, pytube.streams.Stream):
        raise TypeError('expect {}, but get {}'.format(pytube.streams.Stream.__name__, type(audio)))
    song_name = audio.default_filename
    cprint('SONG NAME --- {}'.format(song_name), 'yellow',
           attrs=['bold', 'underline', 'reverse'])

    audio.download(cfg.PATH)
    cprint('Complete: {}/{}'.format(cfg.PATH, song_name), 'green',
           attrs=['bold', 'underline', 'reverse'])


def parse_time_code(time_code):
    try:
        start, end = time_code.split('-')
        if start and end:
            start_min, start_sec = start.split(':')
            end_min, end_sec = end.split(':')
        else:
            if not start:
                start_min, start_sec = None, None
                end_min, end_sec = end.split(':')
            else:
                start_min, start_sec = start.split(':')
                end_min, end_sec = None, None

        if (start_min and start_sec) is not None:
            start_min, start_sec = int(start_min), int(start_sec)

        if (end_min and end_sec) is not None:
            end_min, end_sec = int(end_min), int(end_sec)

        if start_min and start_sec and end_min and end_sec:
            if start_min > end_min or ((start_min == end_min) and (start_sec > end_sec)):
                raise ValueError
    except ValueError as E:
        print('Wrong format, time codes must be integers and without spaces: mm:ss, -mm:ss, mm:ss-')
    else:
        return start_min, start_sec, end_min, end_sec


def cut_song(path, time_code):
    """
    Cuts song
    :param path: path to song file
    :param time_code: string in format
     -> mm:ss - mm:ss , mm:ss - , - mm:ss
    """
    if not isinstance(time_code, str):
        raise TypeError('expect {}, but get {}'.format(str, time_code.__class__))

