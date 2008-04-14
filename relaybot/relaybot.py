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
__module_name__ = "Cancel's RelayBot"
__module_version__ = "1.1.0" 
__module_description__ = "RelayBot by Cancel"

import xchat
import os
import re
import string
import ConfigParser

print "\0034",__module_name__, __module_version__,"has been loaded\003"

#the globals go here
option = {}
xchatdir = xchat.get_info("xchatdir")
inifile = os.path.join(xchatdir,"relaybot.ini")
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
        for item in config.items("main"):
            option[item[0]] = item[1]
            
        option["badwords"] = re.split(' ', option["badwords"])
        option["relaynicks"] = re.split(' ',option["relaynicks"])
        relaypairs = re.split(' ', option["relaypairs"])
        option["relaypairs"] = []
        
        for pair in relaypairs:
            par1, par2, par3, par4 = re.split(':', pair.lower())
            option["relaypairs"].append([par1, par2, par3, par4])
        
        option["service"] = config.getboolean("main", "service")
        option["relayjoins"] = config.getboolean("main", "relayjoins")
        option["relayvoices"] = config.getboolean("main", "relayvoices")
        option["relaykicks"] = config.getboolean("main", "relaykicks")
        option["relaybans"] = config.getboolean("main", "relaybans")
        option["relayops"] = config.getboolean("main", "relayops")
        option["relaydefaultmsg"] = config.getboolean("main", "relaydefaultmsg")
        option["relayonly"] = config.getboolean("main", "relayonly")
            
        #Parse replacements
        replacements = {}
        for item in config.items("replacements"):
            replacements[item[0]] = item[1]
        option["replacements"] = replacements
            
        print color["dgreen"], "CancelBot RelayBot relaybot.ini Load Success"

    except EnvironmentError:
        print color["red"], "Could not open relaybot.ini put it in your "+xchatdir+""

def on_text(word, word_eol, userdata):
    if option["service"] != True:
        return
    counter = 0
    destination = xchat.get_context()
    network = destination.get_info('network').lower()
    channel = destination.get_info('channel').lower()
    triggernick = word[0].lower()
    if option["service"] == True and option["relayonly"] == True and triggernick not in option["relaynicks"]:
        return
    
    for badword in option["badwords"]:
        if re.search(badword, word[1], re.I):
            counter += 1
    for relaypair in option["relaypairs"]:
        if relaypair[0] == network and relaypair[1] == channel:
            destination = xchat.find_context(server=relaypair[2], channel=relaypair[3])
            try:
                if counter == 0:
                    for key in option["replacements"].keys():
                        word_eol[1] = string.replace(word_eol[1],key,option["replacements"][key])
                    destination.command("say " + "<"+triggernick+"> " + word_eol[1])
                elif option["relaydefaultmsg"] == True:
                    destination.command("say " + "<"+triggernick+"> " + option["defaultmsg"])
            except AttributeError:
                print color["red"], "It appears you have not joined the relay destination channel", relaypair[3], "on", relaypair[2]

def on_local(word, word_eol, userdata):
    global option
    trigger = re.split(' ',word_eol[0].lower())
    if trigger[1] == 'add':
        print color["red"],"Function not created yet"
    if trigger[1] == 'del' or trigger[1] == 'delete':
        print color["red"],"Function not created yet"
    if trigger[1] == 'list' or trigger[1] == 'print' or trigger[1] == 'show':
        print color["blue"], "Currently relaying: " + str(option["relaypairs"])
    if trigger[1] == 'off':
        option["service"] = 'off'
        print color["red"], "Relaying has been turned off"
    if trigger[1] == 'on':
        option["service"] = 'on'
        print color["dgreen"], "Relaying has been turned on"
            
    return xchat.EAT_ALL

def on_join(word, word_eol, userdata):
    if option["service"] == True and option["relayjoins"] == True:
        triggernick = word[0]
        channel = word[1].lower()
        destination = xchat.get_context()
        network = destination.get_info('network').lower()
        for relaypair in option["relaypairs"]:
            if relaypair[0] == network and relaypair[1] == channel:
                destination = xchat.find_context(server=relaypair[2], channel=relaypair[3])
                destination.command("say " + "<"+triggernick+"> has joined " + channel + " on " + network)

def on_part(word, word_eol, userdata):
    if option["service"] == True and option["relayjoins"] == True:
        triggernick = word[0]
        channel = word[2].lower()
        destination = xchat.get_context()
        network = destination.get_info('network').lower()
        for relaypair in option["relaypairs"]:
            if relaypair[0] == network and relaypair[1] == channel:
                destination = xchat.find_context(server=relaypair[2], channel=relaypair[3])
                destination.command("say " + "<"+triggernick+"> has parted " + channel + " on " + network)

def on_voice(word, word_eol, userdata):
    if option["service"] == True and option["relayvoices"] == True:
        operator = word[0]
        triggernick = word[1]
        destination = xchat.get_context()
        channel = destination.get_info('channel').lower()
        network = destination.get_info('network').lower()
        for relaypair in option["relaypairs"]:
            if relaypair[0] == network and relaypair[1] == channel:
                destination = xchat.find_context(server=relaypair[2], channel=relaypair[3])
                destination.command("say " + "<"+triggernick+"> received voice from " + operator + " in " + channel + " on " + network)

def on_devoice(word, word_eol, userdata):
    if option["service"] == True and option["relayvoices"] == True:
        operator = word[0]
        triggernick = word[1]
        destination = xchat.get_context()
        channel = destination.get_info('channel').lower()
        network = destination.get_info('network').lower()
        for relaypair in option["relaypairs"]:
            if relaypair[0] == network and relaypair[1] == channel:
                destination = xchat.find_context(server=relaypair[2], channel=relaypair[3])
                destination.command("say " + "<"+triggernick+"> voice taken by " + operator + " in " + channel + " on " + network)

def on_kick(word, word_eol, userdata):
    if option["service"] == True and option["relaykicks"] == True:
        operator = word[0]
        triggernick = word[1]
        channel = word[2].lower()
        destination = xchat.get_context()
        network = destination.get_info('network').lower()
        for relaypair in option["relaypairs"]:
            if relaypair[0] == network and relaypair[1] == channel:
                destination = xchat.find_context(server=relaypair[2], channel=relaypair[3])
                destination.command("say " + "<"+triggernick+"> kicked by " + operator + " in " + channel + " on " + network)

def on_ban(word, word_eol, userdata):
    if option["service"] == True and option["relaybans"] == True:
        operator = word[0]
        triggernick = word[1]
        destination = xchat.get_context()
        channel = destination.get_info('channel').lower()
        network = destination.get_info('network').lower()
        for relaypair in option["relaypairs"]:
            if relaypair[0] == network and relaypair[1] == channel:
                destination = xchat.find_context(server=relaypair[2], channel=relaypair[3])
                destination.command("say " + "<"+triggernick+"> was banned by " + operator + " in " + channel + " on " + network)

def on_unban(word, word_eol, userdata):
    if option["service"] == True and option["relaybans"] == True:
        operator = word[0]
        triggernick = word[1]
        destination = xchat.get_context()
        channel = destination.get_info('channel').lower()
        network = destination.get_info('network').lower()
        for relaypair in option["relaypairs"]:
            if relaypair[0] == network and relaypair[1] == channel:
                destination = xchat.find_context(server=relaypair[2], channel=relaypair[3])
                destination.command("say " + "<"+triggernick+"> was banned by " + operator + " in " + channel + " on " + network)

def on_op(word, word_eol, userdata):
    if option["service"] == True and option["relayops"] == True:
        operator = word[0]
        triggernick = word[1]
        destination = xchat.get_context()
        channel = destination.get_info('channel').lower()
        network = destination.get_info('network').lower()
        for relaypair in option["relaypairs"]:
            if relaypair[0] == network and relaypair[1] == channel:
                destination = xchat.find_context(server=relaypair[2], channel=relaypair[3])
                destination.command("say " + "<"+triggernick+"> was oped by " + operator + " in " + channel + " on " + network)

def on_deop(word, word_eol, userdata):
    if option["service"] == True and option["relayops"] == True:
        operator = word[0]
        triggernick = word[1]
        destination = xchat.get_context()
        channel = destination.get_info('channel').lower()
        network = destination.get_info('network').lower()
        for relaypair in option["relaypairs"]:
            if relaypair[0] == network and relaypair[1] == channel:
                destination = xchat.find_context(server=relaypair[2], channel=relaypair[3])
                destination.command("say " + "<"+triggernick+"> was deoped by " + operator + " in " + channel + " on " + network)
                
load_vars()

#The hooks go here
xchat.hook_print('Channel Message', on_text)
xchat.hook_print('Join', on_join)
xchat.hook_print('Part', on_part)
xchat.hook_print('Channel Voice', on_voice)
xchat.hook_print('Channel DeVoice', on_devoice)
xchat.hook_print('Kick', on_kick)
xchat.hook_print('Channel Ban', on_ban)
xchat.hook_print('Channel UnBan', on_unban)
xchat.hook_print('Channel Operator', on_op)
xchat.hook_print('Channel DeOp', on_deop)
xchat.hook_command('relaybot', on_local, help="Commands are /relaybot add list delete off on, see readme for full help")
# Todo: Maybe later we add relaying joins, parts, bans, etc, no maybe not

#LICENSE GPL
#Last modified 04-13-08
