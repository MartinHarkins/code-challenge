import simplejson as json
import urllib
from bs4 import BeautifulSoup
import re
import os
from os import path
import nltk


#creates the api and gets the json file
def page_handler(key, word, language):
	pagehandler = urllib.urlopen("http://thesaurus.altervista.org/thesaurus/v1?key=" + key + "&word=" + word + "&language=" + language + "&output=json")
	return pagehandler

#parses the json file
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

#puts all html and txt files in the directory into a list
def file_enum(mypath):
	files = [f for f in os.listdir(mypath) if path.isfile(f) and (f.endswith('html') or f.endswith('txt'))]
	print files
	return files

#creates a list of chapter titles
def textOf(soup):
	return ' '.join(soup.find_all(text=True))

#gets all the chapter titles
def get_chapter_list(soup, file_name):
	chapter_list = [textOf(n) for n in soup.find_all('h3', {"align" : "CENTER"})]
	return chapter_list

#creates context for the word
def sentence_snapshot(word, word_tokens, sentence, title, file_name):
                if word in word_tokens:
                        word_loc = word_tokens.index(word)
                        word_tokens.remove(word)
                        newword = '*'+word+'*'
                        word_tokens.insert(word_loc, newword)

                        token_length = len(word_tokens)
			if len(' '.join(sentence)) < 140:
				print ' '.join(word_tokens)
                                print word + " found in " + title + " File name: " + file_name + '\n'

                        if len(' '.join(sentence)) > 140:
                                num1 = word_loc - 5
                                num2 = word_loc + 5

                                if word_loc <= 5:
                                        num1 = 0

                                if token_length - word_loc <= 2:
                                        num2 = token_length

                                while len(' '.join(word_tokens[num1:num2])) > 140:
                                        num1 = num1 + 1
                                        num2 = num2 + 1

                                if num1 > 0 and num2 < token_length:
                                        print '...' + ' '.join(word_tokens[num1:num2]) + '...'
                                elif num1 == 0:
                                        print ' '.join(word_tokens[num1:num2]) + '...'
                                elif num2 == token_length or (num2 - word_loc) >= 2:
                                        print '...' + ' '.join(word_tokens[num1:num2])
        	                else:
	                                print ' '.join(word_tokens)


                                print word + " found in " + title + " File name: " + file_name + '\n'



def find_word(wordlist, word_tokens, sentence, file_name, title):
	for word in wordlist:
		sentence_snapshot(word, word_tokens, sentence, title, file_name)



def sentence_tokenizing(wordlist, sentences, file_name, title):
	for sentence in sentences:
		word_tokens = nltk.word_tokenize(sentence)
		find_word(wordlist, word_tokens, sentence, file_name, title)


def find_in_text(mypath, wordlist):
	for file_name in file_enum(mypath):
	        soup = BeautifulSoup(open(file_name))
	        title = soup.title.string

		raw = soup.get_text()
		
		chapter_list = get_chapter_list(soup, file_name)
	        sentences = nltk.sent_tokenize(raw)
		sentence_tokenizing(wordlist, sentences, file_name, title)
			
def main():
	mypath = os.path.dirname(os.path.abspath(__file__))
	nltk.download('punkt')

	key = "JcEIAPhvmN8t4YMkTSN7"

	word = raw_input('What word would you like to search?')

	language = 'en_US'

	wordlist = [word]	
	
	get_syn(page_handler(key, word, language), wordlist)
	find_in_text(mypath, wordlist)


if __name__ == "__main__":
	main()
