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
__module_version__ = "1.0" 
__module_description__ = "RelayBot by Cancel"

import xchat, os, re, string

print "\0034",__module_name__, __module_version__,"has been loaded\003"

#the globals go here
option = {}
xchatdir = xchat.get_info("xchatdir")
color = {"white":"\0030", "black":"\0031", "blue":"\0032", "green":"\0033", "red":"\0034",
"dred":"\0035", "purple":"\0036", "dyellow":"\0037", "yellow":"\0038", "bgreen":"\0039",
"dgreen":"\00310", "green":"\00311", "blue":"\00312", "bpurple":"\00313", "dgrey":"\00314",
"lgrey":"\00315", "close":"\003"}

#the functions go here
def load_vars():
    global option
    try:
        inifile = open(os.path.join(xchatdir,"relaybot.ini"))
        line = inifile.readline() #The first line is a comment
        line = inifile.readline()
        while line != "":
            par1, par2 = re.split("=", line)
            option[par1] = string.strip(par2)
            line = inifile.readline()
        inifile.close
        option["badwords"] = re.split(' ', option["badwords"])
        relaypairs = re.split(' ', option["relaypairs"])
        option["relaypairs"] = []
        
        for pair in relaypairs:
            par1, par2, par3, par4 = re.split(':', pair.lower())
            option["relaypairs"].append([par1, par2, par3, par4])
        print color["dgreen"], "CancelBot RelayBot relaybot.ini Load Success"

    except EnvironmentError:
        print color["red"], "Could not open relaybot.ini put it in your "+xchatdir+""

def on_text(word, word_eol, userdata):
    if option["service"] != 'on':
        return
    counter = 0
    destination = xchat.get_context()
    network = destination.get_info('network').lower()
    channel = destination.get_info('channel').lower()
    triggernick = word[0].lower()
    #trigger = re.split(' ',word[1].lower())
    for badword in option["badwords"]:
        if re.search(badword, word[1], re.I):
            counter += 1
    for relaypair in option["relaypairs"]:
        if relaypair[0] == network and relaypair[1] == channel:
            destination = xchat.find_context(server=relaypair[2], channel=relaypair[3])
            try:
                if counter == 0:
                    destination.command("say " + "<"+triggernick+"> " + word_eol[1])
                else:
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

load_vars()

#The hooks go here
xchat.hook_print('Channel Message', on_text)
xchat.hook_command('relaybot', on_local, help="Commands are /relaybot add list delete off on, see readme for full help")
# Todo: Maybe later we add relaying joins, parts, bans, etc, no maybe not

#LICENSE GPL
#Last modified 11-24-05
