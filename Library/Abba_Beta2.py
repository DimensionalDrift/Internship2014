"""
Automatic Basic Book Archiver (Abba) V2
Written by Chris Anderson

Changelog:
Alpha		- Pre working/Bare bones version of the code
Beta 1 		- Initial working iteration of the code
			- Fixes for unsucsessful scans or ISBN lookups
			- Added autocapitilisation to data entries
Beta 1.1 	- Framework for global quit implimented 
Beta 2.0 	- Framework for sql database structure implimented (Pending)
			- Book can now have unlimited Authors and subjects
			- Framework for 'Tab to complete' implimented 

To do list:
Fix the ability to quit from isbn scan
Apply the database structure to the script
Implement the rewrite of the individual fields
Check to see if book is already scanned and then append number of books 
"""

from sys import argv
import time
import os
from lxml import html
import requests
import zbar
import csv
import readline

def clearscreen():
    os.system("clear")

def completer(text, state):
    options = [x for x in addrs if x.startswith(text)]
    try:
        return options[state]
    except IndexError:
        return None

# This function should allow the program to quit or stat the scan again from any point in the process.... It does not...
def tupni(message):
	global quit
	word = raw_input(message).title()
	if word =="Quit":
		print word
		quit = True
		return "Exit"
	elif word == "Sa":
		book = True
	else:
		return word

# This function was stolen from Jeroen Leijen isbn_scan_google.py and uses the zbar library to scan the books barcode
def scan():
    # Read at least one barcode (or until window closed)
    proc.process_one()

    # Extract results
    for symbol in proc.results:
        # Do something useful with results
        print 'decoded', symbol.type, 'symbol', '"%s"' % symbol.data
        # Check if type is isbn
        if str(symbol.type).find("ISBN") > -1:
            return str(symbol.data)
        else:
            return "isnotisbn"

# This function is used to search the web for the ISBN number and pull the information for the book
def Lookup(ISBN):
	# Searching isbnsearch.org for the book info and pulling the info from the correct spot on the page
	page = requests.get("http://www.isbnsearch.org/isbn/"+ISBN)
	print "Pulling information from http://www.isbnsearch.org/isbn/"+ISBN
	tree = html.fromstring(page.text)
	BookDict = {}
	Title = tree.xpath('//div[@class="bookinfo"]/h2/text()') # Title is pulled from a separate section to the rest of info
	
	# Assigning all relevant fields to a dictionary
	for i in range (10):
		name = '//*[@id="book"]/div[2]/p[' + str(i+1) + ']/strong/text()'
		value = '//*[@id="book"]/div[2]/p[' + str(i+1) + ']//text()'
		val=(tree.xpath(value))
		if val:
			BookDict.update({val[0]:val[1]})

	# Check to handle if the book has authors or just one author
	if 'Author:' in BookDict.keys():
		Author = BookDict['Author:']
	
	elif 'Authors:' in BookDict.keys():
		Author = BookDict['Authors:']
	
	# If the scan fails throw back an error
	else:
		print "It appears that there was an error while retrieving the book information, please try again."
		return None
	
	Publisher = BookDict['Publisher:']
	Date = BookDict['Published:'].split(" ")
	Year = Date[2]

	if 'Edition:' in BookDict.keys():
		Edition = BookDict['Edition:']
	
	else:
		Edition = ""
	return Title[0], Author, Publisher, Year, Edition

# This function is used to assign the main subject from the file containing the previous library IDs. This function was written to allow new subjects to be added in dynamically rather than having to have all the subjects in the subject file initially
def Topic(IDnumb):
	
	# Opens the csv file and check for the subject
	reader = csv.reader(open('Topics.csv', 'rb'))
	TopicDict = dict(x for x in reader)
	
	# If the subject is not found the user is asked if they would like to assign a new subject to the ID number
	if IDnumb not in TopicDict:
		user_input = tupni("It appears that the ID number " + IDnumb + " is not assigned yet, would you like to assign it? (Y/N): ")
		
		if user_input == "Y":
			subject1 = tupni("What is the new topic?\n")
			writer = csv.writer(open('Topics.csv', 'a'), delimiter=',')
			writer.writerow([IDnumb,subject1])

		else:
			subject1 = tupni("Please enter the main subject:\n")
	
	# Otherwise the subject is assigned from the number and returned
	else:
		subject1 = TopicDict[IDnumb]
	
	return subject1

# Function used to open a file and import the contents into a dictionary
def CSVToDict(Filename):
	csvfile = Filename + ".csv"
	reader = csv.reader(open(csvfile, 'rb'), delimiter=',')
	FileDict = dict(x for x in reader)
	return FileDict

# Function used to compare if a string is in a file by importing it as a dictionary
def CSVCompare(Filename,Comparand):
	csvfile = Filename + ".csv"
	reader = csv.reader(open(csvfile, 'rb'), delimiter=',')
	CompDict = dict(x for x in reader)
	print CompDict

	if Comparand not in CompDict.values():

		ID = int(max(CompDict.iterkeys())) + 1
		CompDict.update({ID:Comparand})

	else:
		ID = CompDict.keys()[CompDict.values().index(Comparand)] 
	
	return ID,Comparand

# Function used to enter in the unlimited number of subjects
def SubjectList(subject1):
	addrs = CSVToDict("Topics")# Change back to subjects after testing (says GLaDOS)
	print "Previously assigned subjects:" 
	print ','.join(str(x) for x in addrs.values())
	subjects = ListBuilder("Please enter addional subjects (if any), hit enter twice to carry on:")
	subjects = subject1 + "; " + subjects
	return subjects

# Funcion used to allow data to be entered in as a list
def ListBuilder(message):
	print message
	item = None
	items = []
	enter = 0
	while enter < 2:
		item = tupni("")
		if item != "":
			items.append(item)
		else:
			enter = enter + 1
	items = "; ".join(items)
	return items


# Prepare zbar webcam scanner - Also stolen from isbn_scan_google.py
proc = zbar.Processor() # Create a Processor
proc.parse_config('enable') # Configure the Processor

# Initialize the Processor
device = '/dev/video1'
if len(argv) > 1:
    device = argv[1]
proc.init(device)

clearscreen()
quit = False
bookno = 0
scancheck = 0
startime = time.time()

readline.set_completer(completer)
readline.parse_and_bind("tab: complete")

# Friendly greeting
print "Welcome to Automatic Basic Book Archiver (or Abba for short)"
print "Be warned... the program is rough and ready so may not actually work!"


while quit == False: # Keep looping until quit
	
	# Asks the user if the book has a barcode, ISBN number or neither
	user_input1 = tupni("Does the book have a Barcode (B) ISBN number (I) or neither (N): ")
	info = None
	
	# If the book has a barcode the barcode is scanned and the above functions are used to assign the info for the book
	if user_input1 == "B":
		
		while not info: # Continue scan until the information has been assigned
			proc.visible = True # Enable the preview window
			print "Scanning......."
			isbn = scan() # Scan the barcode
			info = Lookup(isbn) # Look up the book info
			scancheck += 1
			if scancheck == 3:
				Title = None
				scancheck = 0
				print "Sorry you must enter the details of this book manually"
				proc.visible = False # Close the preview window (it's a pain and gets in the way)
				break
			# When the info is assigned, assign it to the variables
			if info:
				Title = info[0].title()
				Author = info[1]
				Publisher = info[2].title()
				Year = info[3].title()
				Edition = info[4].title()
				proc.visible = False # Close the preview window (it's a pain and gets in the way)

	# If the book does not have a barcode but still has an ISBN it can be manually entered in
	elif user_input1 == "I":
		
		while not info: # Continue scan until the information has been assigned
			isbn = tupni("Enter ISBN number:\n") # Ask for the number
			print "Searching..........."
			info = Lookup(isbn) # Look up the book info
			if isbn == "Q":
				Title = None
				break
			# When the info is assigned, assign it to the variables
			if info:
				Title = info[0].title()
				Author = info[1]
				Publisher = info[2].title()
				Year = info[3].title()
				Edition = info[4].title()

	# Otherwise if the book has neither a barcode or a ISBN (usually means the book is older than ~1965) then the info is entered in manually (ugh...effort...)
	else:
		Title = tupni("Enter the title of the book:\n")
		Author = ListBuilder("Enter the name of the author(s), hit enter twice to carry on:")
		Publisher = tupni("Enter the publishers:\n")
		Year = tupni("Enter the year of publication:\n")
		Edition = tupni("Enter the edition:\n")

	# If the book has an old library ID number then it allows the main subject to be assigned automagically, otherwise it must be entered in manually (ugh...effort...)
	if Title:
		Volume = tupni("Please enter the volume number:\n")

		IDnumb = tupni("Does the book have a Library ID Number? If so what is it? (Hit enter for no ID): ")

		if IDnumb:
			subject1 = Topic(IDnumb)
			subjects = SubjectList(subject1)
		else:
			subject1 = tupni("Enter the main subject of the book:")
			subjects = SubjectList(subject1)

		# The rest of the info is then entered in manually
		Donor = tupni("Please enter the donor (enter l for Ex-Libris):\n")
		
		if Donor == "L":
			Donor = "Ex-Libris"
		Relevance = tupni("Is this book relevant to the physics library? (Y/N/M)")

		Comment = tupni("Please enter in any additional comments about the book: ")

		# The info is then displayed to be checked if it is correct, if it is then it written to a file, otherwise the info is discarded and the info must be entered in again (the ability to change only one field is coming in a later version)
		clearscreen()
		print "ID:" + IDnumb
		print "Title:" + Title
		print "Author:" + str(Author) #"; ".join(str(x) for x in Author)
		print "Publisher:" + Publisher
		print "Year:" + Year
		print "Volume:" + Volume
		print "Edition:" + Edition
		print "Subjects:" + subjects #"; ".join(str(x) for x in subjects)
		print "Donor:" + Donor
		print "Relevant?: " + Relevance
		print "Comments:" + Comment
		check = tupni("Is this information correct?(Y/N): ")
		
		if check == "N":
			clearscreen()

		else:
			print "Writing book to file..."
			writer = csv.writer(open('Library.csv', 'a'), delimiter=',')
			writer.writerow([IDnumb,Title,Author,Publisher,Year,Edition,Volume, subjects,Donor,Comment,Relevance])

			# The user is then asked if they would like to scan another book, if no then the program exits
			bookno += 1
			endtime = time.time()
			bookrate = (endtime - startime)/bookno
			dayrate = 25200/bookrate
			user_inputx = tupni("You have so far scanned books at a rate of " + str(int(bookrate)) + " sec/book (~"+str(int(dayrate))+" books a day).\nWould you like to scan another? (Y/N): ")
			
			if user_inputx == "N":
				quit = True
			
			else:
				quit = False

	clearscreen()

print "Process exited successfully, thank you for using Abba and for having the time of your life!"