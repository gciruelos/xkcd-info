'''
xkcd-crawl - Looks up for words in xkcd comics.
 
Use with prudence, because it makes lots of requests to xkcd.com


Author: Gonzalo Ciruelos <comp.gonzalo@gmail.com>
License: GPLv3
'''



import urllib.request, urllib.parse, urllib.error
import json
import sys
import re
import time
from optparse import OptionParser

class Comic():
	def __init__(self, comicn):
		try:
			self.comic = comicn
			self.raw_information = urllib.request.urlopen('http://xkcd.com/'+str(comicn)+'/info.0.json').read().decode('utf-8')
			self.information = json.loads(self.raw_information)
		except (KeyboardInterrupt, SystemExit):
			print('\n')
			exit()
		except:
			print('CRITICAL ERROR WITH COMIC:', comicn)

	def print_raw_info(self):
		print(self.information)

	def getnumber(self):
		number = self.comic
		
		return str(number)
	
	def gettitle(self):
		title = self.information['safe_title']
		return title

	def getdate(self):
		months = ['null', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
		
		day = self.information['day']
		month = months[int(self.information['month'])]
		year = self.information['year']
		
		if day[-1] == '3':
			suffix = 'rd'
		elif day[-1] == '2':
			suffix = 'nd'
		elif day[-1] == '1':
			suffix = 'st'
		else:
			suffix = 'th'
		day = day+suffix
		
		return day+' '+month+' '+year

	def getlink(self):
		link = 'http://xkcd.com/'+str(self.comic)+'/'
		return link

	def gettranscript(self):
		raw_transcript = self.information['transcript']
		listoflines = raw_transcript.split('\n')
		
		transcript = '\n'.join(listoflines[:-2])		
		
		return transcript

	def getmouseovertext(self):
		text = self.information['alt']
		return text

	def __str__(self):		
		i = ['\n']

		i.append('Number: '+self.getnumber())
		i.append('Title: '+self.gettitle())
		i.append('Date: '+self.getdate())
		i.append('Link: '+self.getlink())	

		info = '\n'.join(i)+'\n'
		return info


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
		#print('At least one word argument required.\nUse --help to show usage.')
		string = input('[search]> ')
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
	comicno = options['comicno']
	try:
		if comicno[-1]=='-':
			mincomic = int(comicno[:-1])
			maxcomic = 1216
		elif comicno[0]=='-':
			mincomic = 1
			maxcomic = int(comicno[1:])
		elif '-' in comicno:
			mincomic = int(comicno.split('-')[0])
			maxcomic = int(comicno.split('-')[1])
		else:
			print("\nThere was an error with the comic number bounds, the default values have been asigned.")
			raise ZeroDivisionError
	except:
		mincomic = 1
		maxcomic = 1216
	#@@@print(words, mincomic, maxcomic)


	# The actual search
	t0 = time.time()
	findings = []
	
	for comic_number in range(mincomic, maxcomic):
		if comic_number in dangerous_comics:
			continue
		results = 0
		for word in words:
			try:
				comic = Comic(comic_number)
				if comic.gettitle().lower().find(word)==-1 and comic.gettranscript().lower().find(word)==-1 and comic.getmouseovertext().lower().find(word)==-1:
					pass
				else:
					results += 1
			except (KeyboardInterrupt, SystemExit):
				print('\n')
				exit()
			except:
				print("ERROR WITH COMIC:", comic_number)
				continue
		
		if results:
			findings.append([comic_number, results])
		
		update_progress((comic_number-mincomic)/float(maxcomic-mincomic))
	
	# Preparing the results
	sys.stdout.write('\r                                              ')
	
	# Printing the results
	#@@@print ('\n\n'+str(findings))
	
	if len(findings)==0:
		print('\n\nNO RESULTS FOUND\n\n')
	else:
		print('\n\nSearch results:', len(findings), 'in %.3f seconds' % (time.time()-t0))
		
		for finding in findings:
			print(Comic(finding[0]))
	
	
if __name__ == '__main__':
	commonwords = ['the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'I', 'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you', 'do', 'at']
	dangerous_comics = [404]
	main()
