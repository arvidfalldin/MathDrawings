import argparse
from utils import StoreDict, load_settings

from barnsley_fern import plot_barnsley_fern

PLOT_FUNC_DICT = {'barnsley': plot_barnsley_fern}


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--num-points', type=int, default=0)
    parser.add_argument('--plot-type', type=str, default='barnsley')
    parser.add_argument('--settings-file',
                        type=str,
                        default='settings.yml')
    parser.add_argument('--settings',
                        type=str,
                        nargs='+',
                        action=StoreDict,
                        help='Overwrite settings\
                        (e.g. --settings log:cylinder pile:single).')

    args, _ = parser.parse_known_args()
    settings = load_settings(args.settings_file, args=args)

    plot_func = PLOT_FUNC_DICT[args.plot_type]
    plot_func(**settings)
