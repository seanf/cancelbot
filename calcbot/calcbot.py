#!/usr/bin/python
__module_name__ = "Cancel's CalcBot"
__module_version__ = "1.0.1" 
__module_description__ = "CalcBot by Cancel"

import xchat
import os
import re
import string

print "\0034",__module_name__, __module_version__,"has been loaded\003"

#the globals go here
option = {}
xchatdir = xchat.get_info("xchatdir")
color = {"white":"\0030", "black":"\0031", "blue":"\0032", "green":"\0033", "red":"\0034",
"dred":"\0035", "purple":"\0036", "dyellow":"\0037", "yellow":"\0038", "bgreen":"\0039",
"dgreen":"\00310", "green":"\00311", "blue":"\00312", "bpurple":"\00313", "dgrey":"\00314",
"lgrey":"\00315", "close":"\003"}
invalid = re.compile('[ABCDEFGHIJLKMNOPQRSTUVWXYZ]', re.I)

#the functions go here
def load_vars():
    global option
    try:
        inifile = open(os.path.join(xchatdir,"calcbot.ini"))
        line = inifile.readline() #The first line is a comment
        line = inifile.readline()
        while line != "":
            par1, par2 = re.split("=", line)
            option[par1] = string.strip(par2)
            line = inifile.readline()
        inifile.close
        print color["dgreen"], "CancelBot CalcBot calcbot.ini Load Success"
        
    except EnvironmentError:
        print color["red"], "Could not open calcbot.ini  put it in your "+xchatdir+""

def on_text(word, word_eol, userdata):
    destination = xchat.get_context()    
    triggernick = word[0]
    trigger = re.split(' ',word[1].lower())
    
    if trigger[0] == '!calc' and option["service"] == 'on':
        calculate(string.join(trigger[1:]), destination)
        
    return xchat.EAT_NONE

def on_pvt(word, word_eol, userdata):
    destination = xchat.get_context()
    triggernick = word[0]
    trigger = re.split(' ',string.lower(word[1]))
    if trigger[0] == '!calc' and option["service"] == 'on':
        calculate(string.join(trigger[1:]), destination)
        
    return xchat.EAT_NONE
    
def calculate(expression, destination):
    try:
      if not invalid.search(expression):
        answer = eval(expression)
        destination.command("say " + expression + color["blue"] + " =" +
                             color["red"] + " " + str(answer))
    
    except:
        return xchat.EAT_NONE
    
    return xchat.EAT_NONE
        
def local_calculate(word, word_eol, userdata):
    try:
        answer = eval(word_eol[1])
        print(word_eol[1] + color["blue"] + " =" + color["red"] + " " + str(answer))
    
    except:
        return xchat.EAT_NONE
    
    return xchat.EAT_NONE
    
load_vars()

#The hooks go here
xchat.hook_print('Channel Message', on_text)
xchat.hook_print('Private Message to Dialog', on_pvt)
xchat.hook_command('calc', local_calculate, help="!calc expression remote, /calc expression local")

#LICENSE GPL
#Last modified 8-25-06

