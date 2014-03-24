'''
xkcd-crawl - Looks up for words in xkcd comics.
 
Use with prudence, because it makes lots of requests to xkcd.com


Author: Gonzalo Ciruelos <gonzalo.ciruelos@gmail.com>
License: GPLv3
'''

import urllib
import json
import sys
import re
import time
from optparse import OptionParser
xkcd = __import__('xkcd-info')


def update_progress(progress):
	#0<progress<1
	barlen = 30
	
	percent = str(int(progress*100))
	
	hyphen = int(barlen*(1-progress))	#-
	numeral = barlen-hyphen				##
	
	sys.stdout.write('\r                                              ')
	sys.stdout.write('\r['+'#'*numeral+'-'*hyphen+']')
	sys.stdout.write(' '+percent)
	sys.stdout.flush()


def main():
	arguments = sys.argv
	
	parser = OptionParser(usage='Usage: %prog [options]',
						  version='xkcd-crawl '+'0.1')
	parser.add_option('-s', '--string', action='store', dest='string',
					  help='The particular word or string that you want to find in the comics.')
	parser.add_option('-a', '--all', action='store_true', dest='all', default=False,
					  help='Show all the comics found.')
	parser.add_option('-c', '--comic', action='store', dest='comicno',
					  help='Between what comics the search will take place.')
	parser.add_option('--no-mouseover', action='store_false', dest='mouseover', default=True,
					  help='Do not search in the comic mouseover text.')
	parser.add_option('--no-text', action='store_false', dest='text', default=True,
					  help='Do not search in the comic main text/dialogue.')
	parser.add_option('--no-title', action='store_false', dest='title', default=True,
					  help='Do not search in the comic title.')
	
	(options, args) = parser.parse_args(arguments)
	options = options.__dict__


	# Looks for the string that's going to search.
	if options['string'] == None:
		string = raw_input('[search]> ')
	else:
		string = options['string']
	
	try:
		words = string.split()
		for word in commonwords:
			word = word.lower()
			if word in words:
				words.remove(word)
	except:
		words = string
	
	
	# Looks for the comics it's going to look between.
	try:
		comicno = options['comicno']
		if comicno[-1]=='-':
			mincomic = int(comicno[:-1])
			maxcomic = 400
		elif comicno[0]=='-':
			mincomic = 1
			maxcomic = int(comicno[1:])
		elif '-' in comicno:
			mincomic = int(comicno.split('-')[0])
			maxcomic = int(comicno.split('-')[1])
		else:
			print "\nThere was an error with the comic number bounds, please choose them again."
			raise ZeroDivisionError
	except:
		try:
			mincomic = int(raw_input('[mincomic]> '))
			maxcomic = int(raw_input('[maxcomic]> '))
		except:
			print "\nThere was an error with the comic number bounds."
			exit()


	# The actual search
	t0 = time.time()
	findings = []
	
	for comic_number in range(mincomic, maxcomic):
		if comic_number in dangerous_comics:
			continue
		results = 0
		for word in words:
			try:
				comic = xkcd.Comic({'all': False,
									'explanation': False,
									'comic_number': str(comic_number),
									'mouseover': False,
									'transcript': False,
									'nobasic': True})
				texts = [comic.gettitle().lower(), comic.gettranscript().lower(),comic.getmouseovertext().lower()]
				for text in texts:
					if text.find(word)!=-1:
						results += 1
			except (KeyboardInterrupt, SystemExit):
				print '\n'
				exit()
			except:
				print "ERROR WITH COMIC:", comic_number 
				continue
		
		if results:
			findings.append([comic_number, results])
		
		update_progress((comic_number-mincomic)/float(maxcomic-mincomic))
	
	# Preparing the results
	sys.stdout.write('\r                                              ')
	
	# Printing the results
	#@@@print ('\n\n'+str(findings))
	
	if len(findings)==0:
		print '\n\nNO RESULTS FOUND\n\n'
	else:
		print '\n\nSearch results:', len(findings), 'in %.3f seconds' % (time.time()-t0)
		
		for finding in findings:
			print xkcd.Comic({'all': False,
						 'explanation': False,
			 			 'comic_number': str(finding[0]),
						 'mouseover': False,
						 'transcript': False,
						 'nobasic': True})
	
	
if __name__ == '__main__':
	commonwords = ['the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'I', 'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you', 'do', 'at']
	dangerous_comics = [404]
	main()
