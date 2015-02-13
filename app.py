from flask import Flask, render_template, redirect, url_for, request
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
	markov_gen = MarkovGenerator(all_speeches, 1500, 10)
	speech = markov_gen.generate_words().replace('  ', '@').replace(' ', '').replace('@', ' ')
	return render_template('index.html', speech=speech)

@app.route('/make_speech', methods=['POST', 'GET'])
def make_speech():
	return redirect(url_for('index'))


if __name__ == '__main__':
	app.run()