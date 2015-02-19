from flask import Flask, render_template, redirect, url_for, request
from markov import MarkovGenerator
from data import timefunc, get_csv_data, get_only_speeches, get_average_by_year, get_presenter_count, get_filtered_data

app = Flask(__name__)

def create_markov_gen(all_speeches):
	"""Returns a markov generator for a given word count and n-gram."""

	markov_gen = MarkovGenerator(all_speeches, 750, 3)
	return markov_gen

def generate_markov_words(markov_gen):
	"""Given a markov generator, returns a formatted speech."""

	new_speech = markov_gen.generate_words()
	# .replace('  ', '@').replace(' ', '').replace('@', ' ')
	return new_speech

# Only do all of this the first time the page is open.
all_speeches = ' '.join(get_only_speeches(get_csv_data()))
markov_gen = create_markov_gen(all_speeches)

full_data = filter(lambda row: int(row[7]) >= 1966, filter(lambda row: row[8] != 'Honorary Award', get_csv_data()))

### Routing ###

@app.route('/')
def index():
	"""Returns the landing page, to which you're redirected every time you
	   click the button."""

	new_speech = generate_markov_words(markov_gen)
	return render_template('index.html', speech=new_speech)

@app.route('/make_speech', methods=['POST', 'GET'])
def make_speech():
	"""Returns a new Markov-generated speech every time you click."""

	return redirect(url_for('index'))

@app.route('/about')
def about():
	"""Returns the about page."""

	return render_template('about.html')

@app.route('/analysis')
def analysis():
	"""Returns the analysis page."""

	return render_template('analysis.html', full_data=full_data)

if __name__ == '__main__':
	app.run(debug=True)