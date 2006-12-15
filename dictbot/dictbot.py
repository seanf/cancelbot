#!/usr/bin/python
__module_name__ = "Cancel's DictBot"
__module_version__ = "2.1.0" 
__module_description__ = "DictBot by Cancel"

import xchat
import os
import re
import string
import ConfigParser
import threading
import mw

print "\0034",__module_name__, __module_version__,"has been loaded\003"

#the globals go here
option = {}
xchatdir = xchat.get_info("xchatdir")
inifile = os.path.join(xchatdir, "dictbot.ini")
color = {"white":"\0030", "black":"\0031", "blue":"\0032", "green":"\0033", "red":"\0034",
"dred":"\0035", "purple":"\0036", "dyellow":"\0037", "yellow":"\0038", "bgreen":"\0039",
"dgreen":"\00310", "green":"\00311", "blue":"\00312", "bpurple":"\00313", "dgrey":"\00314",
"lgrey":"\00315", "close":"\003"}

#the functions go here
def load_vars():
    global option
    try:
        config = ConfigParser.ConfigParser()
        infile = open(inifile)
        config.readfp(infile)
        infile.close()
        
        #Parse main
        #for item in config.items("main"):
        #    option[item[0]] = item[1]
        option["service"] = config.getboolean("main", "service")
        option["deflimit"] = config.getint("main", "deflimit")
        print color["dgreen"], "CancelBot DictBot dictbot.ini Load Success"
        
    except EnvironmentError:
        print color["red"], "Could not open dictbot.ini  put it in your " + xchatdir

def on_text(word, word_eol, userdata):
    global option
    destination = xchat.get_context()    
    triggernick = word[0]
    trigger = re.split(' ',string.lower(word[1]))
    
    if trigger[0] == '!define' and option["service"] == True:
        lookup = string.join(trigger[1:], ' ')
        threading.Thread(target=get_def, args=(lookup, destination)).start()

def on_pvt(word, word_eol, userdata):
    destination = xchat.get_context()
    triggernick = word[0]
    trigger = re.split(' ',string.lower(word[1]))
    if trigger[0] == '!define' and option["service"] == True:
        lookup = string.join(trigger[1:], ' ')
        threading.Thread(target=get_def, args=(lookup, destination)).start()
    
def get_def(lookup, destination):
    response = mw.getdef(lookup)
    mytype = str(type(response))
    count = 0
    if re.search("dict", mytype):
        destination.command("say " + response["Main Entry:"])
        destination.command("say " + response["Pronunciation:"])
        destination.command("say " + response["Function:"])
        if response["Inflected Form(s):"] != '':
            destination.command("say " + response["Inflected Form(s):"])
        if response["Usage:"] != '':
            destination.command("say " + response["Usage:"])
        if response["Etymology:"] != '':
            destination.command("say " + response["Etymology:"])
        for definition in response["Definition:"]:
            if count >= option["deflimit"]:
                destination.command("say Limit " + str(option["deflimit"]) + " definitions")
                break
            destination.command("say " + definition)
            count += 1
            
    elif re.search("list", mytype):
        response = string.join(response, ' ')
        destination.command("say Nothing was found. Maybe you meant " + response)
            
    else:
        destination.command("say No definition or suggestions found")

def local_define(word, word_eol, userdata):
    response = mw.getdef(word_eol[1])
    mytype = str(type(response))
    
    if re.search("dict", mytype):
        print response["Main Entry:"]
        print response["Pronunciation:"]
        print response["Function:"]
        if response["Inflected Form(s):"] != '':
            print response["Inflected Form(s):"]
        if response["Usage:"] != '':
            print response["Usage:"]
        if response["Etymology:"] != '':
            print response["Etymology:"]
        for definition in response["Definition:"]:
            print definition
               
    elif re.search("list", mytype):
        response = string.join(response, ' ')
        print color["red"], "Nothing was found. Maybe you meant", response
            
    else:
        print response
        
    return xchat.EAT_ALL

load_vars()

#The hooks go here
xchat.hook_print('Channel Message', on_text)
xchat.hook_print('Private Message to Dialog', on_pvt)
xchat.hook_command('define', local_define)

#LICENSE GPL
#Last modified 02-16-05
