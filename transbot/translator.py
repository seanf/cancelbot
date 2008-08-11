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
        self.method = lp[self.source][self.destination]
        self.regex = re.compile('<input type="hidden" name="p" value="(.+?)">',re.DOTALL)
        self.text = ''
        self.page = ''
        self.result = ''
        
    def translate(self, text):
        """The text to translate 150 word limit"""
        if text == '':
            return "Enter some text"
        elif len(text) > 750:
            return "There is a 150 word limit"
        else:
            self.text = text
        
        try:
            headers = {'Host':'babelfish.yahoo.com','User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.0.5) Gecko/20060731',
            'Accept':'text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain',
            'Accept-Language':'en-us,en;q=0.5','Accept-Charset':'utf-8',
            'Keep-Alive':'300','Connection':'keep-alive','Referer':'http://babelfish.yahoo.com/translate_txt',
            'Content-Type':'application/x-www-form-urlencoded'}
            self.conn = httplib.HTTPConnection('babelfish.yahoo.com')
            self.conn.request('POST','/translate_txt',"doit=done&intl=1&tt=urltext&trtext="+self.text+"&lp="+self.method, headers)
            self.response = self.conn.getresponse()
            self.page = self.response.read()
            self.conn.close()
            
            self.result = self.regex.search(self.page)
            self.result = self.result.group(1)
            
            return self.result
            
        except Exception, args:
            print Exception, args
            return

#---Functions---#000000#FFFFFF--------------------------------------------------
def get_pairs():
    """This gives you suitable translation pairs"""
    global lp
    if not lp:
        try:
            #Tries to get language pairs from babelfish on the off chance they have added or removed
            #If not successfull do it internally using assumed known pairs.
            data = re.compile("(?is)<!-- Source text \(content\) -->.*<!-- End: Source text \(content\) -->")
            languages = re.compile('(?is)<option value="(.._..)">(.+?) to (.+?)</option>')
            
            conn = httplib.HTTPConnection('babelfish.altavista.com')
            conn.request('GET', '/')
            response = self.conn.getresponse()
            page = response.read()
            conn.close()
            
            result = data.search(page)
            result = result.group()
            
            pairs = languages.findall(result)
            for pair in pairs:
                if pair[1] not in lp:
                    lp[pair[1]] = {}
                    lp[pair[1]][pair[2]] = pair[0]
                else:
                    lp[pair[1]][pair[2]] = pair[0]
            
        except:
            lp = {'English':{'Chinese-simp':'en_zh', 'Chinese-trad':'en_zt', 'Dutch':'en_nl', 'French':'en_fr', 
            'German':'en_de', 'Greek':'en_el', 'Italian':'en_it', 'Japanese':'en_ja',
            'Korean':'en_ko', 'Portuguese':'en_pt', 'Russian':'en_ru', 'Spanish':'en_es'},
            'Chinese-simp':{'English':'zh_en'},
            'Chinese-trad':{'English':'zt_en'},
            'Dutch':{'English':'nl_en', 'French':'nl_fr'},
            'French':{'English':'fr_en', 'German':'fr_de', 'Greek':'fr_el', 'Italian':'fr_it',
            'Portuguese':'fr_pt', 'Dutch':'fr_nl', 'Spanish':'fr_es'},
            'German':{'English':'de_en', 'French':'de_fr'},
            'Greek':{'English':'el_en', 'French':'el_fr'},
            'Italian':{'English':'it_en', 'French':'it_ft'},
            'Japanese':{'English':'ja_en'},
            'Korean':{'English':'ko_en'},
            'Portuguese':{'English':'pt_en', 'French':'pt_fr'},
            'Russian':{'English':'ru_en'},
            'Spanish':{'English':'es_en', 'French':'es_fr'}
            }
    
    pairs = []
    for topkey in lp:
        pairs.append(topkey + " to " + str(lp[topkey].keys()))
    return pairs

get_pairs()

if len(sys.argv) == 4:
    source = sys.argv[1]
    destination = sys.argv[2]
    sourceText = sys.argv[3]
    workerBee = Translator(source, destination)
    result = workerBee.translate(sys.argv[3])
    print result    
       
#License GPL
#Last modified 06-30-08
