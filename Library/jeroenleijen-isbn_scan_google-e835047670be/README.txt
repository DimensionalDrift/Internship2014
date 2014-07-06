ISBN Scan Google
================

About
-----
Use ISBN Scan Google (isbn_scan_google.py) to scan International Standard Book Number (ISBN) bar codes with a webcam and get the bibliographical data from books.google.com. The retrieved data can be written to a local file in CSV style. Each book you store like this is also added to the 'favorites' section of your Google bookshelf. It's very easy to quickly scan your personal library and create a catalog.

Watch the demo video at http://jeroen.leijen.net/computer/webcam_isbn_scan.html

Install
-------
No installation is needed. ISBN Scan Google is a python script and can be run from any directory. Don't forget to enter your Google account details into config.py.

Requirements
------------
- Python 2.5 or 2.6
- ZBar library (http://zbar.sourceforge.net/)
- Gdata library (http://code.google.com/p/gdata-python-client/)
- A Google account
- A webcam

The script is tested on Linux (openSUSE 10.3, 11.0, 11.1) with Python (2.5 and 2.6), ZBar 0.10, Gdata 2.0.12 and a Philips Vesta webcam.

Usage
-----
Open a terminal window.
To start the script type:
> python isbn_scan_google.py
A menu is presented and a separate window for the webcam image opens.
The menu gives you several options:
Scan a new book: press enter
The webcam tries to identify the ISBN number represented by the bar code on your book.
When identified, this number is used to perform a query on books.google.com. The following bibliographical data is retrieved:
- title
- author
- year
- Google id for the book
At this point you can choose another action from the menu.
If you are happy with the result found you can store the data to a local file and add the book to your Google bookshelf. The data is written to a file that is automatically created upon starting the script. Each data file gets a unique name.
Store data: press s to store the results.
Manual input: press m to enter an ISBN for a book without a bar code.
Scan a new book: press enter
Quit: press q to leave the program.


Support & Development
---------------------
There is no support. I developed this script for myself and the current functionality suits me. If you want to contribute you are more than welcome to submit your code to the public development repository at hg.leijen.net. This is my Mercurial repository hosted at Bitbucket.


Credits
-------
Written by Jeroen Leijen <jeroen@leijen.net>
Google Books code taken from / based on the service.test.py script by James Sams <sams.james@gmail.com>  that comes with the gdata python module.
ZBar webcam code taken from / based on some of the example scripts that come with the ZBar library.


Download
--------
The latest version of isbn_scan_google.py is available from its Mercurial repository at http://hg.leijen.net


License
-------
ISBN Scan Google (isbn_scan_google.py) is licensed under a MIT X license.
In other words: feel free to (re)use it but include the MIT X license given below. However, use it at your own risk. My software is most likely to be:

        * inefficient
        * insecure
        * ugly
        * poorly documented
        * clumsy

Having said that, I do appreciate feedback and comments.


Copyright (c) 2010 Jeroen Leijen

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.


