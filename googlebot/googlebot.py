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
__module_name__ = "Cancel's GoogleBot"
__module_version__ = "2.1.1" 
__module_description__ = "GoogleBot by Cancel"

import xchat
import os
import ConfigParser
import re
import string
import HTMLParser
import google

print "\0034",__module_name__, __module_version__,"has been loaded\003"

#---Globals---#000000#FFFFFF----------------------------------------------------
option = {}
xchatdir = xchat.get_info("xchatdir")
inifile = os.path.join(xchatdir, "googlebot.ini")
def makedict(**kwargs):
    return kwargs

color = makedict(white="\0030", black="\0031", blue="\0032", red="\0034",
dred="\0035", purple="\0036", dyellow="\0037", yellow="\0038", bgreen="\0039",
dgreen="\00310", green="\00311", bpurple="\00313", dgrey="\00314",
lgrey="\00315", close="\003")

#---Classes---#000000#FFFFFF----------------------------------------------------
class __Stripper(HTMLParser.HTMLParser):
    def strip(self, some_html):
        self.theString = ""
        self.feed(some_html)
        self.close()
        return self.theString
        
    def handle_data(self, data):
        self.theString += data

#---Functions---#000000#FFFFFF--------------------------------------------------
def load_vars():
    global option
    try:
        config = ConfigParser.ConfigParser()
        infile = open(inifile)
        config.readfp(infile)
        infile.close()
        #Parse main
        for item in config.items("main"):
            option[item[0]] = item[1]
        print color["dgreen"], "CancelBot GoogleBot googlebot.ini Load Success"
        if option["licensekey"] == '':
            print color["red"], "You MUST have a google license key! Get at .cfgphttp://www.google.com/api"
        else:
            google.LICENSE_KEY = option["licensekey"]
        option["service"] = config.getboolean("main", "service")
        option["resultsintab"] = config.getboolean("main", "resultsintab")
        option["publiclimit"] = config.getint("main", "publiclimit")
        option["privatelimit"] = config.getint("main", "privatelimit")
        option["locallimit"] = config.getint("main", "locallimit")
        option["safesearch"] = config.getint("main", "safesearch")
    except EnvironmentError:
        print color["red"], "Could not open googlebot.ini  put it in your " + xchatdir

def on_text(word, word_eol, userdata):
    destination = xchat.get_context()    
    triggernick = word[0].lower()
    trigger = re.split(' ',word[1].lower())
    
    if trigger[0] == '!google' and option["service"] == True:
        google_query(string.join(trigger[1:]), option["publiclimit"], destination)
    if trigger[0] == '!spell' or trigger[0] == '!spelling' and option["service"] == True:
        google_spelling(string.join(trigger[1:]), destination)
            
def on_pvt(word, word_eol, userdata):
    destination = xchat.get_context()
    triggernick = word[0].lower()
    trigger = re.split(' ',word[1].lower())
    
    if trigger[0] == '!google' and option["service"] == True:
        google_query(string.join(trigger[1:]), option["privatelimit"], destination)
    if trigger[0] == '!spell' or trigger[0] == '!spelling' and option["service"] == True:
        google_spelling(string.join(trigger[1:]), destination)
    
def google_query(query, searchlimit, destination):
    try:
        data = google.doGoogleSearch(query, start=0, maxResults=searchlimit, filter=1, restrict='',
        safeSearch=option["safesearch"])
        stripper = __Stripper()
        for item in data.results:
            item.title = stripper.strip(item.title)
            item.snippet = stripper.strip(item.snippet)
            if option["resultsintab"] == True:
                destination.prnt(color["red"] + item.title + " " + color["black"] + item.snippet + " " + color["blue"] + item.URL)
            else:
                destination.command("say " + color["red"] + item.title + " " + color["black"] + item.snippet + " " + color["blue"] + item.URL)
        
    except Exception, args:
        print color["red"], Exception, args
        return

def google_spelling(query, destination):
    try:
        data = google.doSpellingSuggestion(query)
        if data != '':
            if option["resultsintab"] == True:
                destination.prnt(data)
            else:
                destination.command("say " + data)
        
    except Exception, args:
        print color["red"], Exception, args
        return        
    
def local_google(word, word_eol, userdata):
    if option["resultsintab"] == True:
        xchat.command("query " + xchat.get_info("nick"))
        destination = xchat.find_context(channel=xchat.get_info("nick"))
        destination.command("settab >>Google<<")
    else:
        destination = xchat.get_context()
    if word[1] == 'query':
        google_query(word_eol[2], option["locallimit"], destination)
    if word[1] == 'spell' or word[1] == 'spelling':
        google_spelling(word_eol[2], destination)
        
    return xchat.EAT_ALL

load_vars()

#---Hooks---#000000#FFFFFF------------------------------------------------------
xchat.hook_print('Channel Message', on_text)
xchat.hook_print('Private Message to Dialog', on_pvt)
xchat.hook_command('google', local_google, help="/google query what to lookup or /google spell word to check")

#LICENSE GPL
#Last modified 10-24-06
