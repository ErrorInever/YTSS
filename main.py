import argparse
import colorama
import functions
from config.cfg import cfg
from termcolor import cprint


def parse_args():
    parser = argparse.ArgumentParser(description='YouTube simple saver')
    parser.add_argument('--video', dest='video_url', help='video url', default=None, type=str)
    parser.add_argument('--playlist', dest='playlist_url', help='playlist url', default=None, type=str)
    parser.add_argument('--out_dir', dest='out_dir', help='path to output directory', default=None, type=str)
    parser.add_argument('--cut', dest='cut', help='cut sound', default=None, type=str)
    parser.add_argument('--song', dest='song', help='path to sound file', default=None, type=str)

    return parser.parse_args()


if __name__ == '__main__':
    colorama.init()
    args = parse_args()

    if cfg.OUT_DIR is None:
        assert args.out_dir, '--out_dir not specified'
        cfg.OUT_DIR = args.out_dir
    if args.video_url is None and args.playlist_url is None:
        raise NameError('arguments --video and --playlist  not specified')

    cprint('Called with args: {}'.format(args.__dict__), 'yellow',
           attrs=['bold', 'underline', 'reverse'])
    cprint('Config params: {}'.format(cfg.__dict__), 'yellow',
           attrs=['bold', 'underline', 'reverse'])

    if args.video_url:
        functions.download_audio(args.video_url)
    elif args.playlist_url:
        functions.download_playlist(args.playlist_url)
    elif args.cut:
        assert args.song, '--song not specified'
        functions.cut_sound(args.cut, args.song)
