import argparse
from config.cfg import cfg


def get_args():
    parser = argparse.ArgumentParser(description='YouTube saver')
    parser.add_argument('--path', dest='path',
                        help='path to directory where sound will be stored',
                        default=None, type=str)
    parser.print_help()
    return parser.parse_args()


args = get_args()
cfg.PATH = args.path




