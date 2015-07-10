import simplejson as json
import urllib
from bs4 import BeautifulSoup
import re
import os
from os import path
import nltk


mypath = "/home/teitoku/code-challenge/"
files = [f for f in os.listdir(mypath) if path.isfile(f)]

files.remove('code-challenge.py')



key = "JcEIAPhvmN8t4YMkTSN7"

word = raw_input('What word would you like to search?')

language = 'en_US'

wordlist = [word]

pagehandler = urllib.urlopen("http://thesaurus.altervista.org/thesaurus/v1?key=" + key + "&word=" + word + "&language=" + language + "&output=json")

while 1:

	data = json.load(pagehandler)

	if data['error'] != -1:
		print data['error']
		break
	for entry in data['response']:
		synonyms = entry['list']['synonyms'].split('|')

		for item in synonyms:
			wordlist.append(item)

		
		
	break


#print wordlist


for item in files:
	soup = BeautifulSoup(open(item))
	title = soup.title.string
	raw = soup.get_text()
#	print raw
#	print title
	
	sentences = nltk.sent_tokenize(raw)
	for sentence in sentences:
		rekt = nltk.word_tokenize(sentence)
		for word in wordlist:
			if word in rekt:
				if len(sentence) > 140:
					num = 28
					while len(rekt[0:num]) > 140:
						num = num - 1
					print ' '.join(rekt[:num]) + '...'
				else:
					print sentence
				print word + " found in " + item
			
