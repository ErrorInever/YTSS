import argparse
import colorama
import pyfiglet
from functions import download_audio
from config.cfg import cfg
from termcolor import cprint


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', dest='url', help="Youtube video or playlist url", default=None, type=str)
    parser.add_argument('--out_dir', dest='out_dir', help="Path to output directory", default=None, type=str)
    parser.add_argument('--items', dest='items', help="Playlist items e.g. '1, 3, 8'", default=None, type=str)
    parser.add_argument('--range', dest='rng', help="Playlist Start from index to end index e.g. '1, 5', from 1 to 5",
                        default=None, type=str)
    parser.print_help()
    return parser.parse_args()

def console_logo():
    cprint(pyfiglet.figlet_format("YTSS"), 'green')
    cprint('Just a simple youtube downloader', 'green')

if __name__ == '__main__':
    colorama.init()
    console_logo()
    args = parse_args()

    if cfg.OUT_DIR is None:
        assert args.out_dir, '--out_dir not specified'
        cfg.OUT_DIR = args.out_dir

    if args.url is None:
        raise NameError('--url not specified')

    cprint('Called with args: {}'.format(args.__dict__), 'yellow',
            attrs=['bold', 'underline', 'reverse'])
    cprint('Config params: {}'.format(cfg.__dict__), 'yellow',
            attrs=['bold', 'underline', 'reverse'])

    if args.rng:
        try:
            start_rng, end_rng = args.range.split(',')
            start_rng, end_rng = int(start_rng), int(end_rng)
        except ValueError:
            cprint('Wrong --range format')

        kwargs = {
            'playliststart': start_rng,
            'playlistend': end_rng
        }
        download_audio(args.url, cfg.OUT_DIR, **kwargs)

    elif args.items:
        kwargs = {'playlist_items': args.items}
        download_audio(args.url, cfg.OUT_DIR, **kwargs)
    else:
        download_audio(args.url, cfg.OUT_DIR)
