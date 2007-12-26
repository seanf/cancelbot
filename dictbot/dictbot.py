#!/usr/bin/python
__module_name__ = "Cancel's DictBot"
__module_version__ = "3.0.1" 
__module_description__ = "DictBot by Cancel"

import xchat
import os
import re
import string
import ConfigParser
from DictService_client import *

print "\0034",__module_name__, __module_version__,"has been loaded\003"

#the globals go here
option = {}
xchatdir = xchat.get_info("xchatdir")
inifile = os.path.join(xchatdir, "dictbot.ini")
color = {"white":"\0030", "black":"\0031", "blue":"\0032", "green":"\0033", "red":"\0034",
"dred":"\0035", "purple":"\0036", "dyellow":"\0037", "yellow":"\0038", "bgreen":"\0039",
"dgreen":"\00310", "green":"\00311", "blue":"\00312", "bpurple":"\00313", "dgrey":"\00314",
"lgrey":"\00315", "close":"\003"}
dictionaries = {}
loc = DictServiceLocator()
port = loc.getDictServiceSoap()

#the functions go here
def loadVars():
    global option, proxy
    try:
        config = ConfigParser.ConfigParser()
        infile = open(inifile)
        config.readfp(infile)
        infile.close()
        
        #Parse main
        #for item in config.items("main"):
            #option[item[0]] = item[1]
        option["service"] = config.getboolean("main", "service")
        option["charlimit"] = config.getint("main", "charlimit")
        option["defdict"] = config.get("main", "defdict")
        option["deflimit"] = config.getint("main", "deflimit")
        
        print color["dgreen"], "CancelBot DictBot dictbot.ini Load Success"
        
    except EnvironmentError:
        print color["red"], "Could not open dictbot.ini  put it in your " + xchatdir

def onText(word, word_eol, userdata):
    global option
    destination = xchat.get_context()    
    trigger = re.split(' ',string.lower(word[1]))
    triggernick = word[0]
    
    if trigger[0] == '!define' and option["service"] == True:
        lookup = string.join(trigger[1:], '+')
        getDefinition(option["defdict"], lookup, destination)
    
    elif trigger[0] == '!lookin' and dictionaries.has_key(trigger[1]) and option["service"] == True:
        dictid = trigger[1]
        lookup = string.join(trigger[2:], '+')
        getDefinition(dictid, lookup, destination)
        
    elif trigger[0] == '!dictionaries' and option["service"] == True:
        getDictionaries(triggernick)
        
def onPvt(word, word_eol, userdata):
    destination = xchat.get_context()
    triggernick = word[0]
    trigger = re.split(' ',string.lower(word[1]))
    
    if trigger[0] == '!define' and option["service"] == True:
        lookup = string.join(trigger[1:], '+')
        getDefinition(option["defdict"], lookup, destination)
    
    elif trigger[0] == '!lookin' and dictionaries.has_key(trigger[1]) and option["service"] == True:
        dictid = trigger[1]
        lookup = string.join(trigger[2:], '+')
        getDefinition(dictid, lookup, destination)
        
    elif trigger[0] == '!dictionaries' and option["service"] == True:
        getDictionaries(triggernick)
      
def getDefinition(dictid, lookup, destination):
    defcounter = 0
    request = DefineInDictSoapIn()
    request._dictId = dictid
    request._word = lookup
    response = port.DefineInDict(request)
    if(len(response._DefineInDictResult._Definitions._Definition) == 0):
        destination.command("say " + " nothing found check spelling or look in another dictionary using !lookin dictcode word")
    else:
        for definition in response._DefineInDictResult._Definitions._Definition:
            defcounter += 1
        #result = response._DefineInDictResult._Definitions._Definition[0]._WordDefinition
            result = definition._WordDefinition
            result = result.replace('\n', '')
            result = result.replace('  ', '')
            destination.command("say " + lookup + " in " + dictionaries[dictid])
            if (len(result) >= option["charlimit"]):
                destination.command("say " + result[:option["charlimit"]] + " [truncated..]")
            else:
                destination.command("say " + result)
            if defcounter >= option["deflimit"]:
                return

def getDictionaryList():
    global dictionaries
    request = DictionaryListSoapIn()
    response = port.DictionaryList(request)
    for dictionary in response._DictionaryListResult._Dictionary:
        dictionaries[dictionary._Id] = dictionary._Name
    
def getDictionaries(triggernick):
    for key in dictionaries.keys():
        xchat.command("msg " + triggernick + " " + color["red"] + key + color["black"] + " " + dictionaries[key])   

def localDefine(word, word_eol, userdata):
    request = DefineInDictSoapIn()    
    if word[0] == 'define':        
        request._dictId = option["defdict"]
        request._word = string.join(word_eol[1], '+')
        response = port.DefineInDict(request)
        if(len(response._DefineInDictResult._Definitions._Definition) == 0):
            print " nothing found check spelling or look in another dictionary using !lookin dictcode word"
        else:
            for definition in response._DefineInDictResult._Definitions._Definition:
                print definition._WordDefinition
            #print response._DefineInDictResult._Definitions._Definition[0]._WordDefinition
    
    elif word[0] == 'lookin':
        request._dictId= word[1]
        request._word = string.join(word_eol[2], '+')
        response = port.DefineInDict(request)
        if(len(response._DefineInDictResult._Definitions._Definition) == 0):
            print " nothing found check spelling or look in another dictionary using !lookin dictcode word"
        else:
            for definition in response._DefineInDictResult._Definitions._Definition:
                print definition._WordDefinition
            #print response._DefineInDictResult._Definitions._Definition[0]._WordDefinition
        
    elif word[0] == 'dictionaries':
        for key in dictionaries.keys():
            print key + ":" + dictionaries[key]
    
    return xchat.EAT_ALL

loadVars()
getDictionaryList()

#The hooks go here
xchat.hook_print('Channel Message', onText)
xchat.hook_print('Private Message to Dialog', onPvt)
xchat.hook_command('define', localDefine, "usage: define word")
xchat.hook_command('dictionaries', localDefine, "list the dictionaries")
xchat.hook_command('lookin', localDefine,"lookin wn word")
#LICENSE GPL
#Last modified 12-24-07
