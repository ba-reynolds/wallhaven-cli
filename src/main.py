import asyncio
import os
import math

import wallhaven
import cmdargs


def hide_cursor():
	HIDE_CURSOR = '\x1b[?25l'
	print(HIDE_CURSOR, end='')


def show_cursor():
	SHOW_CURSOR = '\x1b[?25h'
	print(SHOW_CURSOR, end='')


async def main():
	
	try:
		hide_cursor()
		parameters, folder, mute, pages, count = cmdargs.get_parameters()
		os.makedirs(folder, exist_ok=True)
		
		# If count is specified, calculate how many pages we might need
		if count is not None:
			NUM_WALLPAPERS_PER_PAGE = 24
			start_page = pages.start
			# Calculate max pages needed (with some buffer)
			max_pages_needed = math.ceil(count / NUM_WALLPAPERS_PER_PAGE)
			pages = range(start_page, start_page + max_pages_needed + 1)
		
		await wallhaven.download_wps(parameters, folder, mute, pages, count)
	finally:
		show_cursor()

if __name__ == '__main__':
	if os.name == 'nt':
		# https://stackoverflow.com/a/51524239 - Activate ANSI escape sequences
		os.system('')
		# https://stackoverflow.com/a/66772242 - Change event loop policy
		asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

	asyncio.run(main())