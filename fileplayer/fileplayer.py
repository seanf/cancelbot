#!/usr/bin/python
__module_name__ = "Cancel's FilePlayer" 
__module_version__ = "1.1.0" 
__module_description__ = "FilePlayer by Cancel"

import xchat
import ConfigParser
import os
import re
import string

option = {}
fileplay = {}

xchatdir = xchat.get_info("xchatdir")
inifile = os.path.join(xchatdir, "fileplayer.ini")
color = {"white":"\0030", "black":"\0031", "blue":"\0032", "green":"\0033", "red":"\0034",
"dred":"\0035", "purple":"\0036", "dyellow":"\0037", "yellow":"\0038", "bgreen":"\0039",
"dgreen":"\00310", "green":"\00311", "blue":"\00312", "bpurple":"\00313", "dgrey":"\00314",
"lgrey":"\00315", "close":"\003"}

#functions go here
def loadVars():
    global option, fileplay
    
    try:
        config = ConfigParser.ConfigParser()
        infile = open(inifile)
        config.readfp(infile)
        infile.close()
        
        #Parse main
        for item in config.items("main"):
            option[item[0]] = item[1]
            
        #Parse files
        for item in config.items("files"):
            fileplay[item[0]] = item[1]
            
        #bools and ints
        option["service"] = config.getboolean("main", "service")
        print color["dgreen"], "Cancel's FilePlayer fileplayer.ini Load Success"
    
    except EnvironmentError:
        print color["red"], "Could not open fileplayer.ini  put it in your " + xchatdir        
        
def onText(word, word_eol, userdata):
    destination = xchat.get_context()
    triggerchannel = xchat.get_info("channel")
    triggernick = word[0]
    trigger = re.split(' ',string.lower(word[1]))
    
    if option["service"] == True and triggerchannel not in option["notin"]::
        if fileplay.has_key(trigger[0]):
            playFile(fileplay[trigger[0]], triggernick)
            
def pvtRequest(word, word_eol, userdata):
    destination = xchat.get_context()
    triggernick = word[0]
    trigger = re.split(' ',string.lower(word[1]))

    if option["service"] == True:
        if fileplay.has_key(trigger[0]):
            playFile(fileplay[trigger[0]], triggernick)

def playFile(file, destination):
    try:
        infile = open(file,"r")
        
    except EnvironmentError:
        print color["red"], "Could not open " + file + ".  Check permisions or fileplayer.ini"
        return
    
    position = "a"
    
    while position != infile.tell():
        position = infile.tell()
        line = string.strip(infile.readline())
        xchat.command("msg " + destination + " " + line)
    infile.close()
    
loadVars()
#The hooks go here
xchat.hook_print('Channel Message', onText)
xchat.hook_print('Private Message to Dialog', pvtRequest)

#LICENSE GPL
#Last modified 2-17-08
