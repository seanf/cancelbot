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
"""Using the mw module
Usage: There is one "public" method getdef.  It should always be passed a string.  Depending on the results you will get back a dictionary, a list, or string as a result.

a = getdef("chomp")

When a definition is found a dictionary with these keys will be returned:
['Etymology:', 'Usage:', 'Pronunciation:', 'Definition:', 'Function:', 'Inflected Form(s):', 'Main Entry:'].  The 'Definition:' key will contain a list of the definitions

{'Etymology:': 'Etymology:alteration of champ', 'Usage:': '', 'Pronunciation:': "Pronunciation:'chmp, 'chomp", 'Definition:': ['intransitive senses : to chew or bite on something', 'transitive senses : to chew or bite on'], 'Function:': 'Function:verb', 'Inflected Form(s):': '', 'Main Entry:': 'Main Entry:chomp '}

Sometimes keys like 'Usage:', 'Inflected Form(s):', and 'Eytymology:' will be empty.

When your word is not found and suggestions are given a list will be returned:

a = getdef("bork")

[' 1. broke', ' 2. Brook', ' 3. Brooke', ' 4. bark', ' 5. boric', ' 6. burke', ' 7. Burke', ' 8. brook', ' 9. Burk', '10. brock', '11. Bors', '12. bore', '13. bort', '14. born']

When no word is found and no suggestions are given a string will be returned:

'No definition or suggestions returned'
"""

import re, string, urllib, HTMLParser

class __Stripper(HTMLParser.HTMLParser):
    def strip(self, some_html):
        self.theString = ""
        self.feed(some_html)
        self.close()
        return self.theString
        
    def handle_data(self, data):
        self.theString += data

def getdef(lookup):
    definition = {"Main Entry:":'', "Pronunciation:":'', "Function:":'', "Inflected Form(s):":'',
            "Usage:":'', "Etymology:":''}
    suggestion = "suggestions for"
    nodef = "start your free trial"
    lookup = string.replace(lookup, ' ', "+")
    stripper = __Stripper()
    
    try:
        lines = urllib.urlopen("http://www.m-w.com/cgi-bin/dictionary?book=Dictionary&va="+lookup+"&x=0&y=0").readlines()
        
    except Exception, args:
        return args
        
    try:
        
        for line in lines:
            if re.search(nodef, line, re.I):#If no definition found
                del lines
                return "No definition or suggestions returned"
                
            if re.search(suggestion, line, re.I):#If suggestions are given
                suggestion = lines.index(line)
                start = lines.index("<PRE>\n")
                stop = lines.index("</PRE>\n",start)
                start = start + 1
                suggestions = lines[start:stop]
                defcount = 0
                
                #Strip \n \r \t \xb7 and html from suggestions
                for sug in suggestions:
                    suggestions[defcount] = string.translate(sug,string.maketrans('',''),'\n''\r''\t''\xb7')
                    suggestions[defcount] = stripper.strip(suggestions[defcount])
                    defcount += 1
                    
                del lines
                return suggestions
            
            for key in definition:#Regular definitions
                if re.match(key, line, re.I):
                    definition[key] = line
            
            if re.search('<b>1</b>'"|"'<b>1 a</b>'"|"'<b>1 a </b>'"|"'<b>:</b>', line, re.I):
                maindef = line
                break
        
        #Prep the main definition
        
        maindef = string.translate(maindef,string.maketrans('',''),'\n''\r''\t''\xb7')
        maindef = re.split('<br>',maindef)
        defcount = 0
        for key in maindef:
            maindef[defcount] = stripper.strip(key)
            defcount += 1
            
        #Strip \n \r \t \xb7 and html from definition header
        for key in definition:
            definition[key] = string.translate(definition[key],string.maketrans('',''),'\n''\r''\t''\xb7')
            definition[key] = stripper.strip(definition[key])
        
        definition["Definition:"] = maindef
        
        del lines, maindef
        return definition
        
    except Exception,args:
        print args
        return args
    
#Last modified 2-6-05
