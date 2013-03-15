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

class Comic():
	def __init__(self, comicno):
		if comicno == '420':
			print 'Blaze it faggot'
		comicn = comicno+'/'
		try:
			self.comic = comicno
			self.raw_information = urllib.urlopen('http://xkcd.com/'+comicn+'info.0.json').read()
			self.information = json.loads(self.raw_information)
		except:
			print 'The comic you tried to get information about doesn\'t exist yet.'

	def print_raw_info(self):
		print self.information

	def gettitle(self):
		title = self.information['safe_title']
		
		return 'Title: '+title

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
		
		return 'Date: '+day+' '+month+' '+year

	def getlink(self):
		link = self.information['img']
		return 'Link: '+link

	def gettranscript(self):
		raw_transcript = self.information['transcript']
		listoflines = raw_transcript.split('\n')
		
		transcript = '\n'.join(listoflines[:-2])		
		
		return 'Transcript:\n'+transcript

	def getmouseovertext(self):
		text = self.information['alt']
		return 'Mouseover text:\n'+text
	
	def getexplanation(self):
		raw_explanation = urllib.urlopen('http://www.explainxkcd.com/wiki/index.php?title='+self.comic).read()
		
		explanation = raw_explanation
		
		return 'Explanation:\n'+explanation
			
	def __str__(self):		
		i = ['\n']
		i.append(self.gettitle())
		i.append(self.getdate())
		i.append(self.getlink())
		i.append('\n'+self.gettranscript())
		i.append('\n'+self.getmouseovertext())
		#i.append('\n'+self.getexplanation())
		
		info = '\n'.join(i)+'\n'
		return info
		
if __name__ == '__main__':
	comic_number = raw_input('Which comic do you want to have information about? Enter a number: ')
	comic = Comic(comic_number)

	print comic
	
	comic.print_raw_info()
