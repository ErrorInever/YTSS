import pytube
from pytube import YouTube
from config.cfg import cfg


def download_audios(url_list):
    """Download audio from YouTube
    :param url_list: list of urls videos
    """
    for url in url_list:
        youtube = YouTube(url)
        audio = youtube.streams.filter(only_audio=True).all()
        print(cfg.PATH)
        #save_audios(audio[0])


def convert_audios(song_list):
    pass


def save_audios(audio):
    if not isinstance(audio, pytube.streams.Stream):
        raise TypeError('expect {}, but get {}'.format(pytube.streams.Stream.__name__, type(audio)))
    audio.download(cfg.PATH)



def post_process_audios(song_list):
    pass


def cut_song(song):
    pass


if __name__ == '__main__':
    download_audios(['https://www.youtube.com/watch?v=84UQgrq3knw'])
    pass