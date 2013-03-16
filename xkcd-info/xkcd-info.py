## xkcd-info - A simple and fast script to retrieve info about an specific xkcd comic
# Version 0.1
#
# This script can be used as a stand-alone program or as a module for a
# bigger script
#
# 
# Author: Gonzalo Ciruelos <comp.gonzalo@gmail.com>
# License: GPLv3

import urllib
import json
import sys
from optparse import OptionParser

class Comic():
	def __init__(self, opts):
		
		self.alls = opts['all']
		self.explanation = opts['explanation']
		self.mouseover = opts['mouseover']
		self.basic = opts['basic']
		self.transcript = opts['transcript']


		if opts['comic_number'] in ('last', 'current', '0'):
			comicn = ''
		else:
			if opts['comic_number'] == '420':
				print 'Blaze it faggot'
			comicn = opts['comic_number']+'/'
			
		try:
			self.comic = opts['comic_number']
			self.raw_information = urllib.urlopen('http://xkcd.com/'+comicn+'info.0.json').read()
			self.information = json.loads(self.raw_information)
		except:
			print 'The comic you tried to get information about doesn\'t exist yet.'
			exit()

	def print_raw_info(self):
		print self.information

	def getnumber(self):
		number = self.information['num']
		
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
		link = self.information['img']
		return link

	def gettranscript(self):
		raw_transcript = self.information['transcript']
		listoflines = raw_transcript.split('\n')
		
		transcript = '\n'.join(listoflines[:-2])		
		
		return transcript

	def getmouseovertext(self):
		text = self.information['alt']
		return text
	
	def getexplanation(self):
		try:
			raw_explanation = urllib.urlopen('http://www.explainxkcd.com/wiki/index.php?title='+self.comic).read().split('\n')
			
			variable = self.getnumber()+':_'+'_'.join(self.gettitle().split(' '))
			start = '<h2><span class="editsection">[<a href="/wiki/index.php?title='+variable+'&amp;action=edit&amp;section=1" title="Edit section: Explanation">edit</a>]</span> <span class="mw-headline" id="Explanation">Explanation</span></h2>'
			end = '<h2><span class="editsection">[<a href="/wiki/index.php?title='+variable+'&amp;action=edit&amp;section=2" title="Edit section: Transcript">edit</a>]</span> <span class="mw-headline" id="Transcript">Transcript</span></h2>'
			
			start_index = raw_explanation.index(start)
			end_index = raw_explanation.index(start)
			
			e_explanation = raw_explanation[start_index:end_index]
			
			explanation = '\n'.join(e_explanation)
			
		except:
			explanation = 'There\'s no explanation for this comic.'
		
		return explanation
			
	def __str__(self):		
		i = ['\n']
		
		if self.basic == True:
			i.append('Number: '+self.getnumber())
			i.append('Title: '+self.gettitle())
			i.append('Date: '+self.getdate())
			i.append('Link: '+self.getlink())
		if self.transcript == True:
			i.append('\n'+'Transcript:\n'+self.gettranscript())
		if self.mouseover == True:
			i.append('\n'+'Mouseover text:\n'+self.getmouseovertext())
		if self.explanation == True:
			i.append('\n'+'Explanation:\n'+self.getexplanation())
		if self.alls == True:
			i = ['\n']
			i.append('Number: '+self.getnumber())
			i.append('Title: '+self.gettitle())
			i.append('Date: '+self.getdate())
			i.append('Link: '+self.getlink())
			i.append('\n'+'Transcript:\n'+self.gettranscript())
			i.append('\n'+'Mouseover text:\n'+self.getmouseovertext())
			i.append('\n'+'Explanation:\n'+self.getexplanation())		


		info = '\n'.join(i)+'\n'
		return info
		
if __name__ == '__main__':
	arguments = sys.argv
	
	parser = OptionParser(usage='Usage: %prog [options]',
						  version='%prog 0.1')
	parser.add_option('-c', '--comic', action='store', dest="comic_number",
					  help='The comic number of the comic you want to get info about.')
	parser.add_option('-a', '--all', action='store_false', default=False,
					  help='Show all the information.')	
	parser.add_option('-b', '--basic', action='store_true', default=True,
					  help='Show just the basic information.')
	parser.add_option('-m', '--mouseover', action='store_false', default=False,
					  help='Show the mouseover text of the comic.')
	parser.add_option('-e', '--explanation', action='store_false', default=False,
					  help='Show the explanation of the comic.')
	parser.add_option('-t', '--transcript', action='store_false', default=False,
					  help='Show the transcript of the comic.')


	(options, args) = parser.parse_args(arguments)
	
	options = options.__dict__

	if options['comic_number'] == None:
		comic_number = raw_input('Which comic do you want to have information about? Enter a number: ')
		options['comic_number'] = comic_number
		
	comic = Comic(options)

	print comic
	
