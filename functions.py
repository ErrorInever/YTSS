from __future__ import unicode_literals
import sys
import youtube_dl
from termcolor import cprint
from utils import show_progress_download
from config.cfg import cfg
from utils import get_time_code


def download_hook(d):
    if d['status'] == 'downloading':
        print(d['filename'], d['_percent_str'])
    elif d['status'] == 'finished':
        print('Download is complete, now converting')


def download_audio(url, out_dir, **kwargs):
    """
    Downloads audio from video or playlist
    :param url: video or playlist url
    :param out_dir: path to out directory
    :param kwargs: params of YoutubeDL
    https://github.com/ytdl-org/youtube-dl/blob/master/youtube_dl/YoutubeDL.py
    """
    ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': out_dir + '/%(title)s.%(ext)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'progress_hooks': [download_hook],
    }

    for key in kwargs:
        ydl_opts[key] = kwargs[key]

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

if __name__ == '__main__':
    # args = {
    #     'playliststart': 3,
    #     'playlistend': 4,
    # }
    #args = {'playlist_items': '1, 2'}
    download_playlist('https://www.youtube.com/playlist?list=PLKvVP6uqHnAb600O3C0Di8Ntjd3tnT_hh', '~/some', **args)

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
