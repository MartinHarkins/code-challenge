#This unit accesses the API and puts the synonyms in a list

import simplejson as json
import urllib



key = "JcEIAPhvmN8t4YMkTSN7"

word = raw_input('What word would you like to search?')

language = 'en_US'

wordlist = [word]

pagehandler = urllib.urlopen("http://thesaurus.altervista.org/thesaurus/v1?key=" + key + "&word=" + word + "&language=" + language + "&output=json")

while 1:

        data = json.load(pagehandler)

	print data

        if data.get('error'):
                print data['error']
                break
        if data['response']:
		for entry in data['response']:
                	synonyms = entry['list']['synonyms'].split('|')

                	for item in synonyms:
                        	wordlist.append(item)
	print wordlist
        break


#print wordlist

