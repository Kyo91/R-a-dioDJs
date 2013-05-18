##DJparser.py
##Parses R/a/dio RSS to find current DJ
 # This program is free software: you can redistribute it and/or modify
 #    it under the terms of the GNU General Public License as published by
 #    the Free Software Foundation, either version 3 of the License, or
 #    (at your option) any later version.

 #    This program is distributed in the hope that it will be useful,
 #    but WITHOUT ANY WARRANTY; without even the implied warranty of
 #    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 #    GNU General Public License for more details.

 #    You should have received a copy of the GNU General Public License
 #    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import feedparser
import re
import time
import webbrowser

dj_rss = "http://r-a-dio.ackwell.com.au/dj/rss"

def currentDJ():
	'''Parses RSS for info about current DJ.'''
	feed = feedparser.parse(dj_rss)

	current = feed["items"][0]

	info = [current.title, current.description, adjusttime(current.published_parsed)]
	return info


def DJname(info):
	'''uses regex to find DJ's name'''
	title = info[0]
	exp = re.match( r'(.*) is streaming now!', title)
	return exp.group(1)


def setup(infos):
	'''makes DJ info look nice in console'''
	print ""
	for info in infos:
		print info
	print "------------------"


def adjusttime(tstruct):
	'''changes time from 24hr GMT to 12hr local'''
	tod = "am" ##time of day
	times = []
	week = ("Mon", "Tues", "Wed", "Thurs", "Fri", "Sat", "Sun")
	month = ("x", "Jan", "Feb", "Mar", "Apr",
			"May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")
	twodigits = [ "00", "01", "02", "03", "04", "05", "06", "07", "08", "09" ]
	for num in range(10,60):
		twodigits.append(str(num))

	for t in tstruct:
		times.append(t)

	if times[3] < (time.timezone / 3600):
		times[2] -= 1	##adjusts date
		times[3] += 12	##adjusts 12hr clock
		times[6] -= 1	##adjusts day
		tod = "pm"
	times[3] -= time.timezone / 3600 ##adjusts for local time zone
	if times[3] > 12: ## changes 24 hr clock into 12 hr clock
		times[3] = times[3] - 12
		tod = "pm"

	hms = "{}:{}:{}{}".format( twodigits[times[3]],
				   twodigits[times[4]], twodigits[times[5]], tod)

	return "{}, {} {} {} {}".format( week[times[6]], twodigits[times[2]], month[times[1]],
					 times[0], hms)

def watchedDJs(file, dj):
	djs = []
	try:
		with open(file) as list:
			for line in list:
				line.strip()
				if not line.startswith('#'):
					djs.append(dj)
		if dj in djs:
			webbrowser.open("http://r-a-d.io/", 2)
	except IOError:
		return

def main():
	cinfo = []
	tinfo = []
	while True:
		try:
			tinfo = currentDJ()
			if tinfo != cinfo:
				cinfo = tinfo
				setup(cinfo)
				watchedDJs('djs.txt', DJname(cinfo))
			time.sleep(600)

		except IndexError:
			cinfo = []
			print "Issue connecting to feed. Will try again in a minute."
			time.sleep(60)


if __name__ == '__main__':
	main()
