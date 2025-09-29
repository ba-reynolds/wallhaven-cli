import argparse

DEFAULT_QUERY = ''
DEFAULT_CATEGORIES = '111'
DEFAULT_PURITY = '100'
DEFAULT_APIKEY = ''
DEFAULT_NPAGES = 1
DEFAULT_START = 1
DEFAULT_FOLDER = 'wallhaven.cc'
DEFAULT_RESOLUTIONS = ''
DEFAULT_MUTE = False
DEFAULT_COUNT = None
FILENAME_APIKEY = 'APIKEY.txt'


def save_apikey(apikey):
    """Attempt to save API key in file for future reference"""
    try:
    	with open(FILENAME_APIKEY, 'w') as file:
            file.write(apikey)
    except Exception as e:
        print(f'warning: couldn\'t store provided API key - {repr(e)}')


def load_apikey():
    """Attempt to load API key from file, if it couldn't find one then return default value"""
    try:
        with open(FILENAME_APIKEY, 'r') as file:
            return file.read()
    except FileNotFoundError:	# no API key saved
        return DEFAULT_APIKEY


def get_parameters():
    """Parse command line arguments, turn them into a dictionary that can be used as the parameters of a url.

    Returns
        (parameters used for url; folder where wallpapers will be saved; whether or not progress bars should be shown; page range; wallpaper count)
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-q', '--query',
                        help='your main way of finding what you\'re looking for',
                        default=DEFAULT_QUERY)

    parser.add_argument('-c', '--categories',
                        help='turn categories on (1) or off (0) [general/anime/people]. E.g. \'010\'',
                        default=DEFAULT_CATEGORIES)

    parser.add_argument('-p', '--purity',
                        help='turn purities on (1) or off (0) [sfw/sketchy/nsfw]. NSFW requires a valid API key',
                        default=DEFAULT_PURITY)

    parser.add_argument('-k', '--apikey',
                        help='add API key, automatically load previously used one if flag isn\'t called',
                        default=DEFAULT_APIKEY)

    parser.add_argument('-n', '--npages',
                        help='number of pages to be downloaded (ignored if --count is specified)',
                        type=int,
                        default=DEFAULT_NPAGES)

    parser.add_argument('-s', '--start',
                        help='start downloading from this page onwards',
                        type=int,
                        default=DEFAULT_START)

    parser.add_argument('-r', '--resolutions',
                        help='list of exact wallpaper resolutions sepparated by commas. E.g. \'1920x1080,2560x1080\'',
                        default=DEFAULT_RESOLUTIONS)

    parser.add_argument('-f', '--folder',
                        help='folder where the wallpapers will be stored',
                        default=DEFAULT_FOLDER)

    parser.add_argument('-m', '--mute',
                        help='disable progress bars',
                        action='store_true')
    
    parser.add_argument('--count',
                        help='download exactly this many wallpapers (takes priority over --npages)',
                        type=int,
                        default=DEFAULT_COUNT)
    
    args = parser.parse_args()
    
    if args.apikey == DEFAULT_APIKEY:	# Load API key
        args.apikey = load_apikey()
    else:								# Save API key
        save_apikey(args.apikey)		

    if args.purity[2] == '1' and args.apikey == DEFAULT_APIKEY:
        print('warning: NSFW results won\'t be shown unless an API key is provided')

    parameters = {
        'q': args.query,
        'categories': args.categories,
        'purity': args.purity,
        'apikey': args.apikey,
        'resolutions': args.resolutions,
    }

    return parameters, args.folder, args.mute, range(args.start, args.start+args.npages), args.count