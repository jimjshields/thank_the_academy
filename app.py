from flask import Flask, render_template, redirect, url_for, request
from markov import MarkovGenerator
import time

def timefunc(f):
	def f_timer(*args, **kwargs):
		start = time.time()
		result = f(*args, **kwargs)
		end = time.time()
		print f.__name__, 'took', end - start, 'time'
		return result
	return f_timer

app = Flask(__name__)

import csv

@timefunc
def get_csv_data():
	speeches = []
	with open('speeches.csv', 'rU') as csv_file:
		data = csv.reader(csv_file)
		for row in data:
			speeches.append(row)
	return speeches

@timefunc
def get_only_speeches(speech_data):
	only_speeches = map(lambda speech: speech[6], speech_data)
	return only_speeches

@timefunc
def create_markov_gen(all_speeches):
	markov_gen = MarkovGenerator(all_speeches, 1500, 10)
	return markov_gen

@timefunc
def generate_markov_words(markov_gen):
	new_speech = markov_gen.generate_words().replace('  ', '@').replace(' ', '').replace('@', ' ')
	return new_speech

speech_data = get_csv_data()
only_speeches = get_only_speeches(speech_data)
all_speeches = ' '.join(only_speeches)
markov_gen = create_markov_gen(all_speeches)
new_speech = generate_markov_words(markov_gen)


@app.route('/')
def index():
	new_speech = generate_markov_words(markov_gen)
	return render_template('index.html', speech=new_speech)

@app.route('/make_speech', methods=['POST', 'GET'])
def make_speech():
	return redirect(url_for('index'))


if __name__ == '__main__':
	app.run(debug=True)