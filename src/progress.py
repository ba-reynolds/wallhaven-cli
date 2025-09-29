class MultiProgressBar:
	"""Displays multiple progress bars at the same time.
	
	Each time you want to add a new progress bar, a new class instance is created.
	This class instance will get added to the MultiProgressBar.instances list.
	Every time display() gets called
		-The progress bar of every instance inside MultiProgressBar.instances will be shown.
		-MultiProgressBar.pbars_printed will get updated to match the length of MultiProgressBar.instances
	
	MultiProgressBar.pbars_printed is used to determine how many lines the program \
	should go up to be able to overwrite the previous progress bars shown.

	__init__ parameters:
		-name = name for the task. This name will get shown along the task's progress bar.
		-total = total amount of progress needed to fill up the progress bar.
		-current = current amount of the task's progress, 0 by default.
	"""
	instances = []
	pbars_printed = 0

	def __init__(self, name, total, current=0):
		self.name = name
		self.total = total
		self.current = current
		self.pbar = self.get_progress_bar()

		Class = self.__class__
		Class.instances.append(self)

	@classmethod
	def clear(cls):
		"""Clear all instances found on MultiProgressBar.instances.

		Should be used after every progress bar has been completed.
		"""
		cls.instances.clear()
		cls.pbars_printed = 0

	def increment(self, amount=1, display=True):
		"""Increment the progress for this task, which also means the progress bar must get updated."""
		self.current += amount
		self.pbar = self.get_progress_bar()
		if display:
			self.display()

	def get_progress_bar(self, width=40):
		"""Get a progress bar, as a string."""
		current, total, name = (self.current, self.total, self.name)
		fill, empty = ('#', '.')

		bar_filled = int(current / total * width)
		bar_empty  = width - bar_filled
		percentage = int(current / total * 100)

		interior = fill * bar_filled + empty * bar_empty
		pbar = f'{name} - |{interior}| {percentage}%'

		return pbar

	def move_up(self, n):
		n_times_up = f'\033[{n}F'	# ANSI escape sequence to move cursor "n" lines up
		print(n_times_up, end='')	# https://en.wikipedia.org/wiki/ANSI_escape_code#CSIsection

	def display(self):
		"""Display the progress bar of every task.

		display() assumes that nothing will be printed in between its calls
		"""
		# https://github.com/python/cpython/blob/main/Lib/tabnanny.py#L161
		Class = self.__class__
		if Class.pbars_printed > 0:
			self.move_up(Class.pbars_printed)

		joined_pbars = '\n'.join(inst.pbar for inst in Class.instances)
		print(joined_pbars)

		Class.pbars_printed = len(Class.instances)



import asyncio


async def fn_with_progress(name, iterations=10, silent=False):
	if not silent:
		pbar = MultiProgressBar(name=name, total=iterations)

	for _ in range(iterations):
		await asyncio.sleep(1)

		if not silent:
			pbar.increment(amount=1)
	

async def main():
	letters = 'ABCDEFGHI'
	tasks = [asyncio.create_task(fn_with_progress(letter))
	for letter in letters]
	await asyncio.gather(*tasks)

if __name__ == '__main__':
	asyncio.run(main())
