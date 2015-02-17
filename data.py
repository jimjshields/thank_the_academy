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

@timefunc
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

@timefunc
def get_only_speeches(speech_data):
	"""Returns an array of only the speeches from the csv data."""

	only_speeches = map(lambda speech: speech[6], speech_data)
	return only_speeches

def get_speech_length(speech):
	"""Returns the length of a speech in words."""

	words = speech.split(' ')
	return len(words)

speech_data = get_csv_data()
non_honorary = filter(lambda row: row[8] != 'Honorary Award', speech_data)
full_data = filter(lambda row: int(row[7]) >= 1966, non_honorary)

for row in full_data:
	row.append(get_speech_length(row[6]))

# longest = sorted(full_data, key=lambda row: row[9], reverse=True)[:10]

# for row in longest:
# 	print '{} - {} - {} - {} words'.format(row[3], row[1], row[2], row[9])