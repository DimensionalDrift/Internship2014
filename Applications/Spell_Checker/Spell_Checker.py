'''
Library Google Spell Checker V0.1
Written by Christopher Anderson

The aim of this program is to search google for the spelling of words then if incorrect flag it for manual checking
Since google does not allow robots to do google searches the text must first be passed through an offline spelling Checker
If the offline spelling Checker finds an error then it is google searched to double check
Then if google says it's spelt correctly then the word is added to the correct words dictionary file
from then on all following words are both compared to the dictionary file and the offline spelling Checker before they are google searched

Things to do
Write words per mintue to file to plot over time
'''

#Most of following code was borrowed from http://github.com/noahcoad/google-spell-check

import os, urllib2, re, HTMLParser, csv, enchant, time, random
from random import randint
from datetime import datetime, timedelta

def clearscreen():
	os.system("clear")

#Function to google search the word and return the correct result
def correct(text):
	html = get_page('http://www.google.com/search?q=' + urllib2.quote(text))
	html_parser = HTMLParser.HTMLParser()

	# pull pieces out
	match = re.search(r'(?:Showing results for|Did you mean|Including results for)[^\0]*?<a.*?>(.*?)</a>', html)
	if match is None:
		fix = text
	else:
		fix = match.group(1)
		fix = re.sub(r'<.*?>', '', fix)
		fix = html_parser.unescape(fix)

	return fix

#Function used to pull down the page of results to be compared
def get_page(url):
	# the type of header affects the type of response google returns
	# for example, using the commented out header below google does not 
	# include "Including results for" results and gives back a different set of results
	# than using the updated user_agent yanked from chrome's headers
	# user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
	user_agent = ['Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36',
	'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3',
	'Mozilla/5.0 (Windows; U; Windows NT 6.1; en; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)',
	'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)',
	'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1',
	'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.1 (KHTML, like Gecko) Chrome/4.0.219.6 Safari/532.1',
	'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)',
	'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.5.30729; .NET CLR 3.0.30729)',
	'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Win64; x64; Trident/4.0)',
	'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; SV1; .NET CLR 2.0.50727; InfoPath.2)Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)',
	'Mozilla/4.0 (compatible; MSIE 6.1; Windows XP)']
	used_user = random.choice(user_agent)
	#print used_user
	headers = {'User-Agent':used_user,}
	req = urllib2.Request(url, None, headers)
	page = urllib2.urlopen(req)
	html = str(page.read())
	page.close()
	return html

def CSVToList(Filename):
	csvfile = Filename + ".csv"
	csvfile = csv.reader(open(csvfile, 'rb'), delimiter=',')
	filelist = []
	for item in csvfile:
		filelist.extend(item)
	return filelist

def sec_to_time(remaintime):

    sec = timedelta(seconds=int(remaintime))
    d = datetime(1,1,1) + sec

    convertime = ("%d days, %d hours, %d minutes and %d seconds" % (d.day-1, d.hour, d.minute, d.second))
    return convertime

clearscreen()
startime = time.time() 
wordno = 0
counter = 0
d = enchant.Dict("en_US")
print "Welcome to the Library Google Spell Checker"
print "Checking spelling now..."

#Main part of the code
with open("Master_Library2.csv", "rb") as f:
	Libreader = csv.reader(f, delimiter="\t")

	#Reads the library file line by line
	for i, line in enumerate(Libreader):
		lines = csv.reader(line, delimiter=',')

		Dictionary = CSVToList("Dictionary")
		Mistakes = CSVToList("Mistakes")	
		
		for row in lines:
			#Splits the row into its constituents such as title, author and each subject
			for i in range (len(row)):
				words = row[i].split(";")
				
				for j in range (len(words)):
					word = words[j].lstrip().rstrip()
					wordstartime = time.time()
					#Only got the check if the word is long, still need to implement the check csv file for word
					if len(word)>1:
						#If the word is in neither of the text files check the spelling
						if word not in Dictionary and word not in Mistakes:
							#If the word does not pass the offline spell check then check online
							if d.check(word) is False:
								randtime = randint(5,10)
								print "Googleing " + word + ", waiting " + str(randtime) + " seconds"
								time.sleep(randtime)
								correction = correct(word)
								#If the spell check does not match the original word then write it to the mistakes file
								if correction != word:
									print "Mistake found\nOld: "+word+" New: " + correction
									Mistwriter = csv.writer(open('Mistakes.csv', 'a'), delimiter=',')
									Mistwriter.writerow([word,correction])
								#Otherwise write it to the Dictionary
								else:
									Dictwriter = csv.writer(open('Dictionary.csv', 'a'), delimiter=',')
									Dictwriter.writerow([word])
							else:
								Dictwriter = csv.writer(open('Dictionary.csv', 'a'), delimiter=',')
								Dictwriter.writerow([word])
						
						wordno = wordno + 1
						counter = counter + 1
						endtime = time.time()
						wordrate_inst = 1/(endtime - wordstartime)

						ratewriter = csv.writer(open('Rate_Full.csv', 'a'), delimiter=',')
						ratewriter.writerow([wordrate_inst])
						
						if counter == 100:
							wordrate_avg = wordno/(endtime - startime) #Rate given in word/sec
							remaintime = (38829 - wordno)/wordrate_avg #Remaining time given in sec

							print "\nCurrent word rate: " + str(wordrate_avg) + " words per second"
							print "Current estimated time remaining: " + str(sec_to_time(remaintime)) + "\n"

							ratewriter = csv.writer(open('Rate_average.csv', 'a'), delimiter=',')
							ratewriter.writerow([wordrate_avg])
							counter = 0
clearscreen()
print "Thank you for using the Library Google Spell Checker"
print "Total time elapsed: " + str(sec_to_time(endtime - startime))
print "Average word rate: " + str(wordno/(endtime - startime)) + " words per second"


