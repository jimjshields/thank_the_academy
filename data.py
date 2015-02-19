import time, csv

### Utility function for profiling ###

def timefunc(f):
	"""Decorator for timing functions."""
	
	def f_timer(*args, **kwargs):
		"""Returns the time (ms) a function takes to run."""

		start = time.time()
		result = f(*args, **kwargs)
		end = time.time()
		print f.__name__, 'took', end - start, 'time'
		return result
	return f_timer

def get_csv_data():
	"""Returns a generator of arrays of all speech data."""

	with open('speeches.csv', 'rU') as csv_file:
		data = csv.reader(csv_file)
		for row in data:
			# FIX: There has to be a better way to deal with non-ASCII characters.
			if row[0] != 'Year':
				yield [unicode(cell, errors='ignore') for cell in row] + [len(row[6].split(' '))]

def get_only_speeches(speech_data):
	"""Returns a generator of only the speeches from the csv data."""

	return (speech[6] for speech in speech_data)

def get_average(speech_data_w_lengths, column_num):
	"""Returns the average length of a speech in words per year."""

	avg = {}

	for row in speech_data_w_lengths:
		if row[column_num] not in avg:
			avg[row[column_num]] = [row[11], 1]
		else:
			avg[row[column_num]][0] += row[11]
			avg[row[column_num]][1] += 1

	new_avg = []

	for i in avg:
		new_avg.append([i, avg[i][0]/avg[i][1]])

	return new_avg

def get_filtered_data(speech_data_w_lengths, selected_categories):
	"""Returns the dataset filtered for a list of parameters for category."""

	return filter(lambda row: row[8] in selected_categories, speech_data_w_lengths)

def get_presenter_count(speech_data_w_lengths):
	"""Returns an array of arrays of presenters and count."""

	presenter_count = {}

	for row in speech_data_w_lengths:
		presenters = row[4].split(', ')
		for presenter in presenters:
			if presenter not in presenter_count:
				presenter_count[presenter] = 1
			else:
				presenter_count[presenter] += 1

	ranked_presenters = []

	for presenter in presenter_count:
		ranked_presenters.append([presenter, presenter_count[presenter]])

	ranked_presenters.sort(key=lambda x: x[1], reverse=True)

	return ranked_presenters