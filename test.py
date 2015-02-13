#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 'http://aaspeechesdb.oscars.org/results.aspx?AC=PREV_RECORD&XC=/results.aspx&BU=http%3A%2F%2Faaspeechesdb.oscars.org%2F&TN=aatrans&SN=AUTO11089&SE=1124&RN=1&MR=0&TR=0&TX=1000&ES=0&CS=0&XP=&RF=WebReportList&EF=&DF=WebReportOscars&RL=0&EL=0&DL=0&NP=255&ID=&MF=oscarsmsg.ini&MQ=&TI=0&DT=&ST=0&IR=0&NR=0&NB=0&SV=0&SS=0&BG=&FG=&QS=&OEX=ISO-8859-1&OEH=utf-8'
# 'http://aaspeechesdb.oscars.org/results.aspx?AC=NEXT_RECORD&XC=/results.aspx&BU=http%3A%2F%2Faaspeechesdb.oscars.org%2F&TN=aatrans&SN=AUTO11089&SE=1124&RN=0&MR=0&TR=0&TX=1000&ES=0&CS=0&XP=&RF=WebReportList&EF=&DF=WebReportOscars&RL=0&EL=0&DL=0&NP=255&ID=&MF=oscarsmsg.ini&MQ=&TI=0&DT=&ST=0&IR=0&NR=1&NB=0&SV=0&SS=0&BG=&FG=&QS=&OEX=ISO-8859-1&OEH=utf-8'
# 'http://aaspeechesdb.oscars.org/results.aspx?AC=NEXT_RECORD&XC=/results.aspx&BU=http%3A%2F%2Faaspeechesdb.oscars.org%2F&TN=aatrans&SN=AUTO11089&SE=1124&RN=1&MR=0&TR=0&TX=1000&ES=0&CS=0&XP=&RF=WebReportList&EF=&DF=WebReportOscars&RL=0&EL=0&DL=0&NP=255&ID=&MF=oscarsmsg.ini&MQ=&TI=0&DT=&ST=0&IR=0&NR=2&NB=0&SV=0&SS=0&BG=&FG=&QS=&OEX=ISO-8859-1&OEH=utf-8'
# 'http://aaspeechesdb.oscars.org/results.aspx?AC=NEXT_RECORD&XC=/results.aspx&BU=http%3A%2F%2Faaspeechesdb.oscars.org%2F&TN=aatrans&SN=AUTO11089&SE=1124&RN=2&MR=0&TR=0&TX=1000&ES=0&CS=0&XP=&RF=WebReportList&EF=&DF=WebReportOscars&RL=0&EL=0&DL=0&NP=255&ID=&MF=oscarsmsg.ini&MQ=&TI=0&DT=&ST=0&IR=0&NR=3&NB=0&SV=0&SS=0&BG=&FG=&QS=&OEX=ISO-8859-1&OEH=utf-8'

import requests, re, csv
from bs4 import BeautifulSoup

# patterns = re.compile("(?P<year>Year:.+)(?P<category>Category:.+)(?P<title>Film Title:.+)(?P<winner>Winner:.+)(?P<presenter>Presenter:.+)(?P<date_venue>Date & Venue:.+)")
year_pattern = re.compile("Year:\s(.+)")
category_pattern = re.compile("Category:\s(.+)")
title_pattern = re.compile("Film Title:\s(.+)")
winner_pattern = re.compile("Winner:\s(.+)")
presenter_pattern = re.compile("Presenter:\s(.+)")
date_venue_pattern = re.compile("Date & Venue:\s(.+)")
speech_pattern = re.compile("Date & Venue:.*\n{1,}.*[A-Z]{2,}:\n?(.+)?\n?")

all_speeches = []

for i in range(2, 1399):
	url = 'http://aaspeechesdb.oscars.org/results.aspx?AC=NEXT_RECORD&XC=/results.aspx&BU=http%%3A%%2F%%2Faaspeechesdb.oscars.org%%2F&TN=aatrans&SN=AUTO11089&SE=1124&RN=%s&MR=0&TR=0&TX=1000&ES=0&CS=0&XP=&RF=WebReportList&EF=&DF=WebReportOscars&RL=0&EL=0&DL=0&NP=255&ID=&MF=oscarsmsg.ini&MQ=&TI=0&DT=&ST=0&IR=0&NR=2&NB=0&SV=0&SS=0&BG=&FG=&QS=&OEX=ISO-8859-1&OEH=utf-8' % (i)
	print url

	html = requests.get(url).content
	bs = BeautifulSoup(html, 'html.parser')
	year = re.search(year_pattern, bs.get_text()).group(1)
	category = re.search(category_pattern, bs.get_text()).group(1)
	title_obj = re.search(title_pattern, bs.get_text())
	if title_obj:
		title = title_obj.group(1)
	else:
		title = 'No title.'
	winner = re.search(winner_pattern, bs.get_text()).group(1)
	presenter = re.search(presenter_pattern, bs.get_text()).group(1)
	date_venue = re.search(date_venue_pattern, bs.get_text()).group(1)
	speech_obj = re.search(speech_pattern, bs.get_text())
	if speech_obj:
		speech = speech_obj.group(1)
	else:
		speech = 'Winner not present.'
	speech_data = map(lambda x: x.encode('utf-8'), [year, category, title, winner, presenter, date_venue, speech])
	print speech_data
	all_speeches.append(speech_data)

with open('test.csv', 'wb') as csv_file:
	csv_writer = csv.writer(csv_file)
	for row in all_speeches:
		csv_writer.writerow(row)