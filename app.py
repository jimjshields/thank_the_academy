from flask import Flask
from markov import MarkovGenerator

app = Flask(__name__)

import csv

speeches = []

with open('speeches.csv', 'rU') as csv_file:
	data = csv.reader(csv_file)
	for row in data:
		speeches.append(row)


speeches = map(lambda speech: speech[6], speeches)

all_speeches = ' '.join(speeches)

@app.route('/')
def index():
	markov_gen = MarkovGenerator(all_speeches, 2000, 8)
	return markov_gen.generate_words().replace('  ', '@').replace(' ', '').replace('@', ' ')


if __name__ == '__main__':
	app.run()