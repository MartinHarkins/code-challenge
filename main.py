import simplejson as json
import urllib
from bs4 import BeautifulSoup
import re
import os
from os import path
import nltk


#wordlist = [word]

def page_handler(key, word, language):
	pagehandler = urllib.urlopen("http://thesaurus.altervista.org/thesaurus/v1?key=" + key + "&word=" + word + "&language=" + language + "&output=json")
	return pagehandler

def get_syn(api_response, wordlist):
	while 1:

        	data = json.load(api_response)

	        if data.get('error'):
        	        print data['error']
            		break
        	for entry in data['response']:
               	 	synonyms = entry['list']['synonyms'].split('|')

                	for item in synonyms:
                        	wordlist.append(item)



        	break




def file_enum(mypath):

	files = [f for f in os.listdir(mypath) if path.isfile(f)]

	files.remove('code-challenge.py')
	return files



def find_in_text(files, wordlist):
	for item in files:
	        soup = BeautifulSoup(open(item))
	        title = soup.title.string
	        raw = soup.get_text()


	        sentences = nltk.sent_tokenize(raw)
	        for sentence in sentences:
	                rekt = nltk.word_tokenize(sentence)
	                for word in wordlist:
	                        if word in rekt:
					gime = rekt.index(word)
					rekt.remove(word)
					rekt.insert(gime, '*'+word+'*')
	                                if len(sentence) > 140:
	                                        num1 = gime + 14
						num2 = gime - 14 
	                                        while len(rekt[0:gime+7]) > 140:
	                                                num1 = num1 - 2
							num2 = num2 + 1
		                                print '...' + ' '.join(rekt[num2:gime]) + ' ' + ' '.join(rekt[gime:num1]) + '...'

					else:
	                                        print ' '.join(rekt)
	                                print word + " found in " + item + '\n'





def main():
	mypath = "/home/teitoku/code-challenge/"

	key = "JcEIAPhvmN8t4YMkTSN7"

	word = raw_input('What word would you like to search?')

	language = 'en_US'

	wordlist = [word]	
	
	get_syn(page_handler(key, word, language), wordlist)
	find_in_text(file_enum(mypath), wordlist)


if __name__ == "__main__":
	main()
