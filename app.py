from flask import Flask, render_template, redirect, url_for, request
from markov import MarkovGenerator
from data import timefunc, get_csv_data, get_only_speeches, get_speech_length, get_average_by_year, get_presenter_count

app = Flask(__name__)

@timefunc
def create_markov_gen(all_speeches):
	"""Returns a markov generator for a given word count and n-gram."""

	markov_gen = MarkovGenerator(all_speeches, 1500, 10)
	return markov_gen

@timefunc
def generate_markov_words(markov_gen):
	"""Given a markov generator, returns a formatted speech."""

	new_speech = markov_gen.generate_words().replace('  ', '@').replace(' ', '').replace('@', ' ')
	return new_speech

# Only do all of this the first time the page is open.
speech_data = get_csv_data()
only_speeches = get_only_speeches(speech_data)
all_speeches = ' '.join(only_speeches)
markov_gen = create_markov_gen(all_speeches)
new_speech = generate_markov_words(markov_gen)

non_honorary = filter(lambda row: row[8] != 'Honorary Award', speech_data)
full_data = filter(lambda row: int(row[7]) >= 1966, non_honorary)

for row in full_data:
	row.append(get_speech_length(row[6]))

actors = filter(lambda row: row[8] == 'Actor in a Leading Role', full_data)

avg_by_year = get_average_by_year(full_data)

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

	return render_template('analysis.html', full_data=full_data, avg_by_year=avg_by_year)

if __name__ == '__main__':
	app.run(debug=True)