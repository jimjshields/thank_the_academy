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
	"""Returns an array of arrays of all speech data."""

	speeches = []
	with open('speeches.csv', 'rU') as csv_file:
		data = csv.reader(csv_file)
		for row in data:
			# FIX: There has to be a better way to deal with non-ASCII characters.
			if row[0] != 'Year':
				speeches.append([unicode(cell, errors='ignore') for cell in row])
	return speeches

def get_only_speeches(speech_data):
	"""Returns an array of only the speeches from the csv data."""

	only_speeches = map(lambda speech: speech[6], speech_data)
	return only_speeches

def get_speech_length(speech):
	"""Returns the length of a speech in words."""

	words = speech.split(' ')
	return len(words)

def get_average_by_year(speech_data_w_lengths):
	"""Returns the average length of a speech in words per year."""

	avg_by_year = {}

	for row in speech_data_w_lengths:
		if row[7] not in avg_by_year:
			avg_by_year[row[7]] = [row[10], 1]
		else:
			avg_by_year[row[7]][0] += row[10]
			avg_by_year[row[7]][1] += 1

	new_avg_by_year = []

	for year in avg_by_year:
		new_avg_by_year.append([year, avg_by_year[year][0]/avg_by_year[year][1]])

	return new_avg_by_year

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



# longest = sorted(full_data, key=lambda row: row[9], reverse=True)[:10]

# for row in longest:
# 	print '{} - {} - {} - {} words'.format(row[3], row[1], row[2], row[9])