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
__module_name__ = "Cancel's TransBot"
__module_version__ = "2.1.0" 
__module_description__ = "TransBot by Cancel"

#---Imports---#000000#FFFFFF----------------------------------------------------
import xchat
import os
import ConfigParser
import re
import string
import translator

print "\0034",__module_name__, __module_version__,"has been loaded\003"

#---Globals---#000000#FFFFFF----------------------------------------------------
option = {}
xchatdir = xchat.get_info("xchatdir")
inifile = os.path.join(xchatdir, "transbot.ini")
autotranslator = {}

def makedict(**kwargs):
    return kwargs

color = makedict(white="\0030", black="\0031", blue="\0032", red="\0034",
dred="\0035", purple="\0036", dyellow="\0037", yellow="\0038", bgreen="\0039",
dgreen="\00310", green="\00311", bpurple="\00313", dgrey="\00314",
lgrey="\00315", close="\003")

#---Functions---#000000#FFFFFF--------------------------------------------------
def load_vars():
    global option, autotranslator
    try:
        config = ConfigParser.ConfigParser()
        infile = open(inifile)
        config.readfp(infile)
        infile.close()
        #Parse main
        for item in config.items("main"):
            option[item[0]] = item[1]
            
        option["service"] = config.getboolean("main", "service")
        option["autotranslate"] = config.getboolean("main", "autotranslate")
        #Parse autotranslators
        for item in config.items("autotranslators"):
            autotranslator[item[0]] = item[1]
        for key in autotranslator:
            autotranslator[key] = re.split(' ', autotranslator[key])
            autotranslator[key] = translator.Translator(autotranslator[key][0], autotranslator[key][1])
        
        print color["dgreen"], "CancelBot TransBot transbot.ini Load Success"
            
    except EnvironmentError:
        print color["red"], "Could not open transbot.ini put it in your " + xchatdir
    
    except Exception, args:
        print color["red"], args

def save_vars():
    config = ConfigParser.ConfigParser()
    infile = open(inifile)
    config.readfp(infile)
    infile.close()

    for key in option:
        config.set("main", key, option[key])
    
    config.remove_section("autotranslators")
    config.add_section("autotranslators")
    
    for key in autotranslator:
        config.set("autotranslators", key, autotranslator[key].source + " " + autotranslator[key].destination)

    infile = open(inifile, "w")
    config.write(infile)
    infile.close()

def on_text(word, word_eol, userdata):
    destination = xchat.get_context()    
    triggernick = word[0].lower()
    trigger = re.split(' ',word[1].lower())
    
    if trigger[0] == '!translate' and option["service"] == True:
        translate(trigger[1], trigger[2], string.join(trigger[3:],' '), destination)
        
    if trigger[0] == '!translators' and option["service"] == True:
        translators(destination)
        
    if option["autotranslate"] == True:
        if autotranslator.has_key(triggernick):
            print color["blue"], "<"+triggernick+">", autotranslator[triggernick].translate(string.join(trigger,' '))

def on_pvt(word, word_eol, userdata):
    destination = xchat.get_context()
    triggernick = word[0].lower()
    trigger = re.split(' ',word[1].lower())
    
    if trigger[0] == '!translate' and option["service"] == True:
        translate(trigger[1], trigger[2], string.join(trigger[3:],' '), destination)
        
    if trigger[0] == '!translators' and option["service"] == True:
        translators(destination)

    if option["autotranslate"] == True:
        if autotranslator.has_key(triggernick):
            print color["blue"], "<"+triggernick+">", autotranslator[triggernick].translate(string.join(trigger,' '))

def translate(source, dest, text, destination):
    try:
        a = translator.Translator(source, dest)
        response = a.translate(text)
        destination.command("say " + response)
    
    except KeyError, args:
        destination.command("say "+ color["red"] + str(args)+ color["close"] + " is not a valid language. Try !translators")
        
    except Exception, args:
        print color["red"], Exception, args
        return
        
def translators(destination):
    pairs = str(translator.get_pairs())
    destination.command("say Available methods are " + pairs)

def autotranslate(word, word_eol, userdata):
    global autotranslator, option
    
    if word[1].lower() == 'del':
        if autotranslator.has_key(word[2].lower()):
            autotranslator.pop(word[2].lower())
            print color["red"], "Autotranslator for", word[2], "deleted!"
            save_vars()
        else:
            print color["red"], "No Autotranslator for", word[2], "found"

    elif word[1].lower() == 'list':
        if len(autotranslator) == 0:
            print color["red"], "You have no auto translators!"
        else:
            print color["dgreen"], "Your auto translators are:"
            for key in autotranslator:
                print color["blue"], key, autotranslator[key].source, autotranslator[key].destination
    
    elif word[1].lower() == 'on':
        option["autotranslate"] = True
        print color["dgreen"], "Autotranslate has been turned ON"
        save_vars()

    elif word[1].lower() == 'off':
        option["autotranslate"] = False
        print color["red"], "Autotranslate has been turned OFF"
        save_vars()
        
    elif word[1].lower() == 'translators':
        print "Available methods are:", color["blue"], str(translator.get_pairs())
    
    else:
        try:
            autotranslator[word[1].lower()] = translator.Translator(word[2],word[3])
            print color["dgreen"], "We will now auto translate", word[1], "from", word[2], "to", word[3]
            save_vars()
        except Exception, args:
            print color["red"], "Proper format is Nick FromLanguage ToLanguage"
            return
            
    return xchat.EAT_ALL
            
def local_trans(word, word_eol, userdata):
    destination = xchat.get_context()
    if word[1].lower() == 'translators':
        print "Available methods are:", color["blue"], str(translator.get_pairs())
        
    else:
        try:
            a = translator.Translator(word[1], word[2])
            response = a.translate(word_eol[3])
            destination.command("say " + response)
            
        except KeyError, args:
            print color["red"] + str(args) + color["close"] + " is not a valid language. Try /trans translators"
            
        except Exception, args:
            print color["red"], Exception, args
            return
    
    return xchat.EAT_ALL
   
load_vars()

#The hooks go here
xchat.hook_print('Channel Message', on_text)
xchat.hook_print('Private Message to Dialog', on_pvt)
xchat.hook_command('autotranslate', autotranslate, help="see the README")
xchat.hook_command('trans', local_trans, help="see the README")

#LICENSE GPL
#Last modified 2-16-06
