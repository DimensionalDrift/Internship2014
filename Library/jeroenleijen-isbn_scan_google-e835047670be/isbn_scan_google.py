#!/usr/bin/python
#isbn_scan_google.py

__author__ = "Jeroen Leijen <jeroen@leijen.net>"

from sys import argv
import time
import os

import zbar

from gdata.books.service import BookService
import gdata.books

import config

def clearscreen():
    os.system("clear")


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


def google_books(handler):
    bib_data = {"isbn":handler,"google_id":"noid","title":"nfig","creator":"nfig","date":"nfig"}
    print 'Looking up books.google.com for handler',handler
    results = service.search_by_keyword(isbn=handler)
    #print results
    for document_entry in results.entry:
        bib_data["google_id"] = document_entry.identifier[0].text
        if document_entry.creator:
        	bib_data["creator"] = document_entry.creator[0].text
        if document_entry.dc_title[0]:
            bib_data["title"] = document_entry.dc_title[0].text
        if document_entry.date:
            bib_data["date"] = document_entry.date.text
    #Note: if the book is not in google books there won't be
    #results, hence the previous for-loop will not be executed and google_id
    #keeps its start value ("noid")
    return bib_data


# Google account details
email = config.google_email
password = config.google_password

# Google books object
service = gdata.books.service.BookService()
service.ClientLogin(email, password)

# Open file to store results
timestamp = time.strftime("%a_%d_%b_%Y_%H%M%S")
filename = "stored-"+timestamp+".txt"
logfile = open(filename, 'a')


# Prepare zbar webcam scanner

# create a Processor
proc = zbar.Processor()

# configure the Processor
proc.parse_config('enable')

# initialize the Processor
device = '/dev/video1'
if len(argv) > 1:
    device = argv[1]
proc.init(device)

# enable the preview window
proc.visible = True


# default start values
bib_data = {}
#bib_data = "none"
bib_data_saved = {}
#bib_data_saved = "none"
info = ""
quit = False

while quit == False: #keep looping until quit
    clearscreen()
    print "\n"+80*"*"+"\n"
    print "Last retreived:",bib_data
    print "\n"+80*"-"+"\n"
    print "Last stored   :",bib_data_saved
    print "\n"+80*"*"+"\n"
    user_input = raw_input("m (manual isbn)  s (store)  q (quit)  other (new scan) -> enter ")
    if user_input == "q": #quit
        quit = True
    elif user_input == "m": #manual input
        isbn = raw_input("Enter ISBN number: ")
        print isbn
        bib_data = google_books(isbn)
    elif user_input == "s": #store data
        for item in bib_data:
            info = info +"|"+str(bib_data[item])
        logfile.write(info+"\n")
        if bib_data["google_id"] <> "noid":
            results = service.get_by_google_id(bib_data["google_id"])
            results = service.add_item_to_library(results) #add book to library (favorites shelf)
        bib_data_saved = bib_data
        print info,"written to logfile\n"
        info = ""
    else: #other choice (enter): scan with webcam
        print "Scanning......."
        isbn = "isnotisbn"
        while isbn == "isnotisbn": # continue scan until we have an isbn value
            isbn = scan()
            print isbn
        # we have an isbn value, now proces further
        bib_data = google_books(isbn)

logfile.close
