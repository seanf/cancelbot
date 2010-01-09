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
import json
import urllib2
import sys

#---Globals---#000000#FFFFFF----------------------------------------------------
baseURL = 'http://ajax.googleapis.com/ajax/services/language/translate?v=1.0&langpair='
lp = {'AFRIKAANS' : 'af',
  'ALBANIAN' : 'sq',
  'AMHARIC' : 'am',
  'ARABIC' : 'ar',
  'ARMENIAN' : 'hy',
  'AZERBAIJANI' : 'az',
  'BASQUE' : 'eu',
  'BELARUSIAN' : 'be',
  'BENGALI' : 'bn',
  'BIHARI' : 'bh',
  'BULGARIAN' : 'bg',
  'BURMESE' : 'my',
  'CATALAN' : 'ca',
  'CHEROKEE' : 'chr',
  'CHINESE' : 'zh',
  'CHINESE_SIMPLIFIED' : 'zh-CN',
  'CHINESE_TRADITIONAL' : 'zh-TW',
  'CROATIAN' : 'hr',
  'CZECH' : 'cs',
  'DANISH' : 'da',
  'DHIVEHI' : 'dv',
  'DUTCH': 'nl',  
  'ENGLISH' : 'en',
  'ESPERANTO' : 'eo',
  'ESTONIAN' : 'et',
  'FILIPINO' : 'tl',
  'FINNISH' : 'fi',
  'FRENCH' : 'fr',
  'GALICIAN' : 'gl',
  'GEORGIAN' : 'ka',
  'GERMAN' : 'de',
  'GREEK' : 'el',
  'GUARANI' : 'gn',
  'GUJARATI' : 'gu',
  'HEBREW' : 'iw',
  'HINDI' : 'hi',
  'HUNGARIAN' : 'hu',
  'ICELANDIC' : 'is',
  'INDONESIAN' : 'id',
  'INUKTITUT' : 'iu',
  'IRISH' : 'ga',
  'ITALIAN' : 'it',
  'JAPANESE' : 'ja',
  'KANNADA' : 'kn',
  'KAZAKH' : 'kk',
  'KHMER' : 'km',
  'KOREAN' : 'ko',
  'KURDISH': 'ku',
  'KYRGYZ': 'ky',
  'LAOTHIAN': 'lo',
  'LATVIAN' : 'lv',
  'LITHUANIAN' : 'lt',
  'MACEDONIAN' : 'mk',
  'MALAY' : 'ms',
  'MALAYALAM' : 'ml',
  'MALTESE' : 'mt',
  'MARATHI' : 'mr',
  'MONGOLIAN' : 'mn',
  'NEPALI' : 'ne',
  'NORWEGIAN' : 'no',
  'ORIYA' : 'or',
  'PASHTO' : 'ps',
  'PERSIAN' : 'fa',
  'POLISH' : 'pl',
  'PORTUGUESE' : 'pt-PT',
  'PUNJABI' : 'pa',
  'ROMANIAN' : 'ro',
  'RUSSIAN' : 'ru',
  'SANSKRIT' : 'sa',
  'SERBIAN' : 'sr',
  'SINDHI' : 'sd',
  'SINHALESE' : 'si',
  'SLOVAK' : 'sk',
  'SLOVENIAN' : 'sl',
  'SPANISH' : 'es',
  'SWAHILI' : 'sw',
  'SWEDISH' : 'sv',
  'TAJIK' : 'tg',
  'TAMIL' : 'ta',
  'TAGALOG' : 'tl',
  'TELUGU' : 'te',
  'THAI' : 'th',
  'TIBETAN' : 'bo',
  'TURKISH' : 'tr',
  'UKRAINIAN' : 'uk',
  'URDU' : 'ur',
  'UZBEK' : 'uz',
  'UIGHUR' : 'ug',
  'VIETNAMESE' : 'vi',
  'WELSH' : 'cy',
  'YIDDISH' : 'yi'
    }

#---Classes---#000000#FFFFFF----------------------------------------------------
class Translator:
    """Class that handles the actual translation"""
    def __init__(self, source, destination):
        """Source Language, Destination Language"""
        self.source = source.upper()
        self.destination = destination.upper()
        
        self.text = ''
        self.result = ''
        
    def translate(self, text):
        if text == '':
            return "Enter some text"
        else:
            self.text = text
        
        try:
            finalURL = baseURL + lp[self.source] +"|"+ lp[self.destination] +"&q=" + urllib2.quote(self.text)
            response = urllib2.urlopen(finalURL).read()
            responseData = json.loads(response)
            self.result = responseData["responseData"]["translatedText"]
            
            return  self.result
            
        except Exception, args:
            print Exception, args
            return

#---Functions---#000000#FFFFFF--------------------------------------------------
def get_pairs():
    """This gives you suitable translation pairs"""
    
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
#Last modified 01-09-10
