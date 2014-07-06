"""
Automatic Basic Book Archiver (Abba) V1.0
Written by Chris Anderson

To do list:
Implement the rewrite of the individual fields
Check to see if book is already scanned and then append number of books 
"""

from sys import argv
import timeit
import os
from lxml import html
import requests
import zbar
import csv

def clearscreen():
    os.system("clear")

#This function was stolen from Jeroen Leijen isbn_scan_google.py and uses the zbar library to scan the books barcode
def scan():
    # read at least one barcode (or until window closed)
    proc.process_one()

    # extract results
    for symbol in proc.results:
        # do something useful with results
        print 'decoded', symbol.type, 'symbol', '"%s"' % symbol.data
        # check if type is isbn
        if str(symbol.type).find("ISBN") > -1:
            return str(symbol.data)
        else:
            return "isnotisbn"

#This function is used to search the web for the ISBN number and pull the information for the book
def Lookup(ISBN):
	#Searching isbnsearch.org for the book info and pulling the info from the correct spot on the page
	page = requests.get("http://www.isbnsearch.org/isbn/"+ISBN)
	tree = html.fromstring(page.text)
	BookDict = {}
	Title = tree.xpath('//div[@class="bookinfo"]/h2/text()') #Title is pulled from a separate section to the rest of info
	
	#Assigning all relevant fields to a dictionary
	for i in range (10):
		name = '//*[@id="book"]/div[2]/p[' + str(i+1) + ']/strong/text()'
		value = '//*[@id="book"]/div[2]/p[' + str(i+1) + ']//text()'
		val=(tree.xpath(value))
		if val:
			BookDict.update({val[0]:val[1]})

	#Check to handle if the book has authors or just one author
	if 'Author:' in BookDict.keys():
		Author = BookDict['Author:']
	
	elif 'Authors:' in BookDict.keys():
		Authors = BookDict['Authors:']
		Author = Authors.split(";")
		Author = Author[0]
	
	#If the scan fails throw back an error
	else:
		print "It appears that there was an error while retrieving the book information, please try again."
		return None
	
	Publisher = BookDict['Publisher:']
	Date = BookDict['Published:'].split(" ")
	Year = Date[2]
	Edition = BookDict['Edition:']
	
	return Title[0], Author, Publisher, Year, Edition

#This function is used to assign the main subject from the file containing the previous library IDs. This function was written to allow new subjects to be added in dynamically rather than having to have all the subjects in the subject file initially
def Topic(IDnumb):
	
	#Opens the csv file and check for the subject
	reader = csv.reader(open('Topics.csv', 'rb'))
	TopicDict = dict(x for x in reader)
	
	#If the subject is not found the user is asked if they would like to assign a new subject to the ID number
	if IDnumb not in TopicDict:
		user_input = raw_input("It appears that the ID number " + IDnumb + " is not assigned yet, would you like to assign it? (Y/N): ")
		
		if user_input == "y":
			subject1 = raw_input("What is the new topic?\n")
			writer = csv.writer(open('Topics.csv', 'wb'), delimiter=',')
			writer.writerow([IDnumb,subject1])

		else:
			subject1 = raw_input("Please enter the main subject:\n")
	
	#Otherwise the subject is assigned from the number and returned
	else:
		subject1 = TopicDict[IDnumb]
	
	return subject1

# Prepare zbar webcam scanner - Also stolen from isbn_scan_google.py
proc = zbar.Processor() # create a Processor
proc.parse_config('enable') # configure the Processor

# initialize the Processor
device = '/dev/video1'
if len(argv) > 1:
    device = argv[1]
proc.init(device)

clearscreen()
quit = False
bookno = 0
startime = timeit.timeit()

#Friendly greeting
print "Welcome to Automatic Basic Book Archiver (or Abba for short)"
print "The following program has been tested but still may not actually work!"


while quit == False: #keep looping until quit
	
	#Asks the user if the book has a barcode, ISBN number or neither
	user_input1 = raw_input("Does the book have a Barcode (B) ISBN number (I) or neither (N): ")
	info = None
	
	#If the book has a barcode the barcode is scanned and the above functions are used to assign the info for the book
	if user_input1 == "b":
		
		while not info: # continue scan until the information has been assigned
			proc.visible = True #Enable the preview window
			print "Scanning......."
			isbn = scan() #Scan the barcode
			info = Lookup(isbn) #Look up the book info
			
			#When the info is assigned, assign it to the variables
			if info:
				Title = info[0]
				Author = info[1]
				Publisher = info[2]
				Year = info[3]
				Edition = info[4]
				proc.visible = False #Close the preview window (it's a pain and gets in the way)

	#If the book does not have a barcode but still has an ISBN it can be manually entered in
	elif user_input1 == "i":
		
		while not info: # continue scan until the information has been assigned
			isbn = raw_input("Enter ISBN number:\n") #Ask for the number
			info = Lookup(isbn) #Look up the book info
			
			#When the info is assigned, assign it to the variables
			if info:
				Title = info[0]
				Author = info[1]
				Publisher = info[2]
				Year = info[3]
				Edition = info[4]

	#Otherwise if the book has neither a barcode or a ISBN (usually means the book is older than ~1965) then the info is entered in manually (ugh...)
	else:
		Title = raw_input("Enter the title of the book:\n")
		Author = raw_input("Enter the name of the author:\n")
		Publisher = raw_input("Enter the publishers:\n")
		Year = raw_input("Enter the year of publication:\n")
		Edition = raw_input("Enter the edition:\n")

	#If the book has an old library ID number then it allows the main subject to be assigned automagically, otherwise it must be entered in manually (ugh...)
	IDnumb = raw_input("Does the book have a Library ID Number? If so what is it? (Hit enter for no ID): ")
	
	if IDnumb:
		subject1 = Topic(IDnumb)
	else:
		subject1 = raw_input("Please enter the main subject:\n")

	#The rest of the info is then entered in manually
	subject2 = raw_input("Please enter the secondary subject if any:\n")
	subject3 = raw_input("Please enter any additional subjects or comments:\n")
	volume = raw_input("Please enter the volume number:\n")
	donor = raw_input("Please enter the donor (enter l for Ex-Libris):\n")
	
	if donor == "l":
		donor = "Ex-Libris"
	relevance = raw_input("Is this book relevant to the physics library? (Y/N/M)")

	#The info is then displayed to be checked if it is correct, if it is then it written to a file, otherwise the info is discarded and the info must be entered in again (the ability to change only one field is coming in a later version)
	clearscreen()
	print "ID:" + IDnumb
	print "Title:" + Title
	print "Author:" + Author
	print "Publisher:" + Publisher
	print "Year:" + Year
	print "Volume:" + volume
	print "Edition:" + Edition
	print "Subjects:" + subject1 + ", " + subject2 + ", " + subject3
	print "Donor:" + donor
	print "Relevant?: " + relevance
	check = raw_input("Is this information correct?(Y/N): ")
	
	if check == "y":
		print "Writing book to file..."

		writer = csv.writer(open('Library.csv', 'wb'), delimiter=',')
		writer.writerow([IDnumb,Title,Author,Publisher,Year,volume,Edition,subject1,subject2,subject3,donor,relevance])

		#The user is then asked if they would like to scan another book, if no then the program exits
		bookno += 1
		endtime = timeit.timeit()
		bookrate = (endtime - startime)/bookno
		user_inputx = raw_input("You have so far scanned " + str(bookno) + " books at a rate of " + bookrate + " seconds per book, would you like to scan another? (Y/N): ")
		
		if user_inputx == "n":
			quit = True
		
		else:
			quit = False

	clearscreen()

print "Process exited successfully, thank you for using Abba and for having the time of your life!"