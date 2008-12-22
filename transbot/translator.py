#!/usr/bin/python
############################################################################
#    Copyright (C) 2005 by JTP                                             #
#    jtpowell at hotmail dot com                                           #    
#                                                                          #
#    This program is free software; you can redistribute it and#or modify  #
#    it under the terms of the GNU General Public License as published by  #
#    the Free Software Foundation; either version 2 of the License, or     #
#    (at your option) any later version.                                   #
#                                                                          #
#    This program is distributed in the hope that it will be useful,       #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of        #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         #
#    GNU General Public License for more details.                          #
#                                                                          #
#    You should have received a copy of the GNU General Public License     #
#    along with this program; if not, write to the                         #
#    Free Software Foundation, Inc.,                                       #
#    59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.             #
############################################################################
"""Using the translator module
Usage: There is a public method called get_pairs().  It is used to show suitable language pairs. There is a class called Translator with one method, translate.
There is one public dictionary called lp which contains all of the language pairs and their pair value

'from translator import *'

get_pairs() returns a string of suitable language pairs

English ['Portuguese', 'German', 'Spanish', 'Japanese', 'French', 'Greek', 'Dutch', 'Russian', 'Korean', 'Chinese-simp', 'Italian']

An instance of a class MUST be passed a valid translation pair.

a = Translator('english', 'spanish')

a.translate('this is a test')
'esto es una prueba'"""

#---Imports---#000000#FFFFFF----------------------------------------------------
import re
import httplib
import sys

#---Globals---#000000#FFFFFF----------------------------------------------------
lp = {}

#---Classes---#000000#FFFFFF----------------------------------------------------
class Translator:
    """Class that handles the actual translation"""
    def __init__(self, source, destination):
        """Source Language, Destination Language"""
        self.source = source.capitalize()
        self.destination = destination.capitalize()
        #self.method = lp[self.source] +"|" + lp[self.destination] + "|"
        self.regex = re.compile('<div id=result_box dir="...">(.+?)</div>',re.DOTALL)
        self.text = ''
        self.page = ''
        self.result = ''
        
    def translate(self, text):
        if text == '':
            return "Enter some text"
        else:
            self.text = text
        
        try:
            headers = {'Host':'translate.google.com','User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.9.1b2) Gecko/20081201 Firefox/3.1b2',
            'Accept':'text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain',
            'Accept-Charset':'ISO-8859-1,UTF-8;q=0.7,*;q=0.7',
            'Keep-Alive':'300','Connection':'keep-alive','Referer':'http://translate.google.com/translate_t',
            'Content-Type':'application/x-www-form-urlencoded'}
            self.conn = httplib.HTTPConnection('translate.google.com')
            self.conn.request('POST','/translate_t',"hl=" + lp[self.source] + "&sl=" + lp[self.source] + "&tl=" + lp[self.destination] + "&q=" + self.text, headers)
            self.response = self.conn.getresponse()
            self.page = self.response.read()
            self.conn.close()
            
            self.result = self.regex.search(self.page)
            self.result = self.result.group(1)
            
            return  self.result
            
        except Exception, args:
            print Exception, args
            return

#---Functions---#000000#FFFFFF--------------------------------------------------
def get_pairs():
    """This gives you suitable translation pairs"""
    global lp
    if not lp:
        try:
            #Tries to get language pairs from google on the off chance they have added or removed
            #If not successfull do it internally using assumed known pairs.
            data = re.compile('(?ism)<form action="/translate_t" method=post id="text_form" name="text_form">(.+?)</form>')
            languages = re.compile('(?ism)<option.+?value=(.+?)>(.+?)</option>')
            
            conn = httplib.HTTPConnection('translate.google.com')
            conn.request('GET', '/')
            response = self.conn.getresponse()
            page = response.read()
            conn.close()
            
            result = data.search(page)
            result = result.group()
            
            pairs = languages.findall(result)
            for pair in pairs:                   
                lp[pair[2]]= pair[1]                
            
        except:
            lp = {"Arabic":"ar",
                  "Bulgarian":"bg",
                  "Catalan":"ca",
                  "Chinese":"zh-CN",
                  "Croatian":"hr",
                  "Czech":"cs",
                  "Danish":"da",
                  "Dutch":"dl",
                  "English":"en",
                  "Filipino":"tl",
                  "Finnish":"fi",
                  "French":"fr",
                  "German":"de",
                  "Greek":"el",
                  "Hebrew":"iw",
                  "Hindi":"hi",
                  "Indonesian":"id",
                  "Italian":"it",
                  "Japanese":"ja",
                  "Korean":"ko",
                  "Latvian":"lv",
                  "Lithuanian":"lt",
                  "Norwegian":"no",
                  "Polish":"pl",
                  "Portuguese":"pt",
                  "Romanian":"ro",
                  "Russian":"ru",
                  "Serbian":"sr",
                  "Slovak":"sk",
                  "Slovenian":"sl",
                  "Spanish":"es",
                  "Swedish":"sv",
                  "Ukrainian":"uk",
                  "Vietnamese":"vi"                
            }
    
    return sorted(lp.keys())

get_pairs()

if len(sys.argv) == 4:
    source = sys.argv[1]
    destination = sys.argv[2]
    sourceText = sys.argv[3]
    workerBee = Translator(source, destination)
    result = workerBee.translate(sys.argv[3])
    print result
    
else:
    print get_pairs()
       
#License GPL
#Last modified 12-22-08
