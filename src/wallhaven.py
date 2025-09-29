import asyncio
import aiohttp
import os

import progress

TOO_MANY_REQUESTS_STATUS = 429
TOO_MANY_REQUESTS_SLEEP = 10


async def fetch(session, url, **kwargs):
	"""Send a get request using the session passed in as an argument to the specified url.

	If the response were to get a 429 status code, wait 10 seconds and try again.
	"""
	response = await session.get(url, **kwargs)
	if response.status == TOO_MANY_REQUESTS_STATUS:
		response.close()
		await asyncio.sleep(TOO_MANY_REQUESTS_SLEEP)
		return await fetch(session, url, **kwargs)
	return response


async def download_wp(session, url, folder, mute, chunk_size=8192):
	"""Download an individual wallpaper.

	The name and extension of the file will be stripped away from the wallpaper url
	Example:
		"https://w.wallhaven.cc/full/pk/wallhaven-pkgkkp.png" -> "pkgkkp.png"

	Progress bars won't be shown unless bool(mute) == False.

	Keyword arguments
	chunk_size	-- how many bytes should be written to the file at a time

	The binary data will not be written to the file all at once as this can take a considerable amount of time.
	"""
	filename = url.partition('-')[2]
	if folder:
		filename = os.path.join(folder, filename)

	response = await fetch(session, url)
	if not mute:
		pbar = progress.MultiProgressBar(name=filename, total=int(response.headers['Content-length']))

	with open(filename, 'wb') as file:
		async for chunk in response.content.iter_chunked(chunk_size):
			file.write(chunk)
			if not mute:
				pbar.increment(amount=len(chunk))

	response.close()


async def get_urls(session, params):
	"""Search for wallpapers with the specified parameters, get their urls."""
	search_url = 'https://wallhaven.cc/api/v1/search'
	fetch_api = await fetch(session, search_url, params=params)
	json_api = await fetch_api.json()

	urls = []
	for json_img in json_api['data']:
		urls.append(json_img['path'])

	return urls


async def download_wps(params, folder, mute, pages, count=None):
	"""Concurrently download wallpapers that match the specified parameters.
	
	If count is specified, download exactly that many wallpapers (fetching from additional pages if needed).
	Otherwise, download all wallpapers from the specified pages.
	"""
	NUM_WALLPAPERS_PER_PAGE = 24
	downloaded_count = 0
	
	async with aiohttp.ClientSession() as session:

		# Download wallpapers of every requested page
		for pagenum in pages:	# Page index starts from 1.
			params['page'] = pagenum
			urls = await get_urls(session, params)

			if not urls:
				if not mute:
					print(f'No wallpapers found on page N°{pagenum}')
				return

			# If count is specified, limit urls to remaining needed
			if count is not None:
				remaining = count - downloaded_count
				if remaining <= 0:
					return
				urls = urls[:remaining]

			if not mute:
				print(f'Page N°{pagenum} - Wallpapers: {len(urls)}')

			tasks = []
			for url in urls:
				task = asyncio.create_task(download_wp(session, url, folder, mute))
				tasks.append(task)
			await asyncio.gather(*tasks)

			downloaded_count += len(urls)

			if not mute:
				progress.MultiProgressBar.clear()
			
			# If count is specified and we've reached it, stop
			if count is not None and downloaded_count >= count:
				if not mute:
					print(f'Downloaded {downloaded_count} wallpapers')
				return
				
			# If no count specified, check if we've run out of wallpapers
			if count is None and len(urls) != NUM_WALLPAPERS_PER_PAGE:
				if not mute:
					print(f'Exiting at page N°{pagenum} as no more wallpapers were found')
				return
		
		# If count specified but we ran out of pages
		if count is not None and downloaded_count < count:
			if not mute:
				print(f'Downloaded {downloaded_count}/{count} wallpapers (ran out of pages)')