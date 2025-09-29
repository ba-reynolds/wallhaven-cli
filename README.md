# Wallhaven.cc CLI Wallpaper Downloader

A simple command-line tool to download wallpapers from [wallhaven.cc](https://wallhaven.cc) using their public API. Download multiple wallpapers concurrently, filter by categories, purity, resolution, and more. Progress bars are shown for each download.

## Features

- Download wallpapers by search query, category, purity, and resolution
- Download a specific number of wallpapers or multiple pages at once
- Concurrent downloads for faster performance
- Optional progress bars for each wallpaper
- API key support for NSFW content

## Requirements

- Python 3.7+
- [aiohttp](https://pypi.org/project/aiohttp/)

Install dependencies:
```sh
pip install -r requirements.txt
```

## Usage

```sh
python main.py [options]
```

## Options

| **Option**        | **Description**                                                   | **Default**   |
|-------------------|-------------------------------------------------------------------|---------------|
| `-q`, `--query`       | Search query                                                  | (empty)       |
| `-c`, `--categories`  | Categories: 1=on, 0=off [general/anime/people], e.g. 010      | `111`         |
| `-p`, `--purity`      | Purity: 1=on, 0=off [sfw/sketchy/nsfw], e.g. 100              | `100`         |
| `-k`, `--apikey`      | Wallhaven API key (required for NSFW)                         | (empty)       |
| `-n`, `--npages`      | Number of pages to download (ignored if `--count` is used)    | `1`           |
| `-s`, `--start`       | Start downloading from this page                              | `1`           |
| `-r`, `--resolutions` | Comma-separated list of resolutions, e.g. 1920x1080,2560x1080 | (empty)       |
| `-f`, `--folder`      | Output folder for wallpapers                                  | `wallhaven.cc`|
| `-m`, `--mute`        | Disable progress bars                                         | (off)         |
| `--count`             | Download exactly this many wallpapers (takes priority over `-n`) | (none)     |

## Examples

### Download a specific number of wallpapers
```sh
# Download exactly 10 wallpapers
python main.py --count 10 -q "nature"

# Download 50 anime wallpapers at 1920x1080
python main.py --count 50 -c 010 -r 1920x1080
```

### Download by pages
```sh
# Download 2 pages of SFW milky way wallpapers at 1920x1080 resolution
python main.py -q "milky way" -p 100 -n 2 -r 1920x1080

# Download pages 5-7 (3 pages starting from page 5)
python main.py -q "landscape" -s 5 -n 3
```

### Using API key for NSFW content
```sh
# The API key is automatically saved for future use
python main.py -k YOUR_API_KEY -p 111 --count 20
```

## Notes

- When using `--count`, the script automatically fetches from multiple pages as needed
- `--count` takes priority over `--npages` when both are specified
- Progress bars use ANSI escape codes; for Windows, the script enables these automatically
- API keys are saved in `APIKEY.txt` and automatically loaded for future runs
- Downloaded files are saved in the specified folder

## License
This project is provided as-is, with no warranty. See wallhaven.cc API terms for usage guidelines.

---

Old code, shared for reference and utility.