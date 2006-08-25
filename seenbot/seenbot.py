#!/usr/bin/python
__module_name__ = "Cancel's SeenBot"
__module_version__ = "2.1" 
__module_description__ = "SeenBot by Cancel"

print "\0034",__module_name__, __module_version__,"has been loaded\003"

import xchat
import os
import re
import string
import time
import shelve
import ConfigParser

#---Globals---#000000#FFFFFF----------------------------------------------------
option = {}
seen = {}
xchatdir = xchat.get_info("xchatdir")
inifile = os.path.join(xchatdir,"seenbot.ini")

#---Functions---#000000#FFFFFF--------------------------------------------------    
def makedict(**kwargs):
    return kwargs

color = makedict(white="\0030", black="\0031", blue="\0032", red="\0034",
dred="\0035", purple="\0036", dyellow="\0037", yellow="\0038", bgreen="\0039",
dgreen="\00310", green="\00311", bpurple="\00313", dgrey="\00314",
lgrey="\00315", close="\003")

def load_vars():
    global option, seen
    try:
        config = ConfigParser.ConfigParser()
        infile = open(inifile)
        config.readfp(infile)
        infile.close()
        #Parse Main
        for item in config.items("main"):
            option[item[0]] = item[1]
            option["service"] = config.getboolean("main", "service")
            option["locallimit"] = config.getint("main", "locallimit")
            option["searchlimit"] = config.getint("main", "searchlimit")
            
        print color["dgreen"], "CancelBot SeenbotBot seenbot.ini Load Success"
        
    except EnvironmentError:
        print color["red"], "Could not open seenbot.ini  put it in your " + xchatdir
    
    try:
        seen = shelve.open(os.path.join(xchatdir, "seenbot.db"),'c')
        print color["dgreen"], "SeenBot DB successfully opened"
    
    except Exception, args:
        print color["red"], args

def on_join(word, word_eol, userdata):
    global seen
    triggernick, triggerchannel, triggerhost = word
    key = triggernick.lower()
    seen[key] = [triggernick + " " + triggerhost + " was last seen " + time.ctime() + " joining " + triggerchannel, int(time.time())]
    seen.sync()

def on_change(word, word_eol, userdata):
    global seen
    oldnick, newnick = word
    triggerchannel = xchat.get_info("channel")
    key = oldnick.lower()
    seen[key] = [oldnick + " was last seen " + time.ctime() + " changing nick to " + newnick + " in " + triggerchannel, int(time.time())]
    key = newnick.lower()
    seen[key] = [newnick + " was last seen " + time.ctime() + " changing nick from " + oldnick + " in " + triggerchannel, int(time.time())]
    seen.sync()
    
def on_voice(word, word_eol, userdata):
    global seen
    voicer, triggernick = word
    triggerchannel = xchat.get_info("channel")
    key = triggernick.lower()
    seen[key] = [triggernick + " was last seen " + time.ctime() + " being voiced by " + voicer + " in " + triggerchannel, int(time.time())]
    seen.sync()
    
def on_devoice(word, word_eol, userdata):
    global seen
    devoicer, triggernick = word
    triggerchannel = xchat.get_info("channel")
    key = triggernick.lower()
    seen[key] = [triggernick + " was last seen " + time.ctime() + " being devoiced by " + devoicer + " in " + triggerchannel, int(time.time())]
    seen.sync()
    
def on_kick(word, word_eol, userdata):
    global seen
    kicker, triggernick, triggerchannel, reason = word
    key = triggernick.lower()
    seen[key] = [triggernick + " was last seen " + time.ctime() + " being kicked from " + triggerchannel + " by " + kicker + " for " + reason, int(time.time())]
    seen.sync()

def on_part(word, word_eol, userdata):
    global seen
    triggernick, triggerhost, triggerchannel = word
    key = triggernick.lower()
    seen[key] = [triggernick + " " + triggerhost + " was last seen " + time.ctime() + " parting " + triggerchannel, int(time.time())]
    seen.sync()

def on_quit(word, word_eol, userdata):
    global seen
    triggernick, reason, triggerhost = word
    key = triggernick.lower()
    seen[key] = [triggernick + " " + triggerhost + " was last seen " + time.ctime() + " quiting the network", int(time.time())]
    seen.sync()
    
def on_op(word, word_eol, userdata):
    global seen
    opper, triggernick = word
    triggerchannel = xchat.get_info("channel")
    key = triggernick.lower()
    seen[key] = [triggernick + " was last seen " + time.ctime() + " being opped by " + opper + " in " + triggerchannel, int(time.time())]
    seen.sync()

def on_deop(word, word_eol, userdata):
    global seen
    deopper, triggernick = word
    triggerchannel = xchat.get_info("channel")
    key = triggernick.lower()
    seen[key] = [triggernick + " was last seen " + time.ctime() + " being deopped by " + deopper + " in " + triggerchannel, int(time.time())]
    seen.sync()

def on_text(word, word_eol, userdata):
    triggerchannel = xchat.get_info("channel")
    destination = xchat.get_context()    
    triggernick = word[0]
    trigger = re.split(' ', word[1].lower())
    
    if option["service"] == True and trigger[0] == "!seen" and triggerchannel not in option["notin"]:
        if seen.has_key(trigger[1]):
            destination.command("say " + seen[trigger[1]][0])
    
    elif option["service"] == True and trigger[0] == "!seensearch" and triggerchannel not in option["notin"]:
        results = seensearch(string.join(trigger[1:]), option["searchlimit"])
        if results:
            for result in results:
                destination.command("say " + result)

def seensearch(data, limit):
    count = 0
    results = []
    for key in seen:
        if re.search(data, seen[key][0]):
            results.append(seen[key][0])
            count += 1
        if count == limit:
            break
    return results
        
def command_seen(word, word_eol, userdata):
    key = word[1].lower()
    if seen.has_key(key):
        print color["blue"], seen[key][0]
    
    return xchat.EAT_ALL

def command_seensearch(word, word_eol, userdata):
    results = seensearch(word_eol[1].lower(), option["locallimit"])
    if results:
        for result in results:
            print color["blue"], result
    return xchat.EAT_ALL
    
def command_seencount(word, word_eol, userdata):
    print color["blue"], len(seen), "records in the seen db"
    return xchat.EAT_ALL

def command_seenpurge(word, word_eol, userdata):
    global seen
    try:
        days = int(word[1])
        if days <= 0:
            raise ValueError
        
        daysinsecs = days * 60 * 60 * 24
        count = 0
        print color["blue"], len(seen), "records in the seen db"
        print color["red"], "Now purging records more than", days, "old"
            
        for key in seen:
            if time.time() - seen[key][1] > daysinsecs:
                del seen[key]
                count += 1
        print color["green"], count, "records were removed"
        print color["blue"], len(seen), "records in the seen db"
    
    except ValueError, args:
        print color["red"], args, "is not a valid number"
    
    return xchat.EAT_ALL

def command_seendump(word, word_eol, userdata):
    try:
        seendump = open(os.path.join(xchatdir,"seenbot.txt"),'w')
        keys = seen.keys()
        keys.sort()
        for key in keys:
            seendump.write(seen[key][0] + "\n")
        seendump.close
        print color["blue"], len(seen), "records in the seen db"
        print color["dgreen"], "Dump complete results in", os.path.join(xchatdir,"seenbot.txt")
        
    except Exception, args:
        print color["red"], args
    
    return xchat.EAT_ALL

load_vars()
    
#---Hooks---#000000#FFFFFF------------------------------------------------------
xchat.hook_print('Join', on_join)
xchat.hook_print('Change Nick', on_change)
xchat.hook_print('Channel Voice', on_voice)
xchat.hook_print('Channel DeVoice', on_devoice)
xchat.hook_print('Kick', on_kick)
xchat.hook_print('Part', on_part)
xchat.hook_print('Quit', on_quit)
xchat.hook_print('Channel Operator', on_op)
xchat.hook_print('Channel DeOp', on_deop)
xchat.hook_print('Channel Message', on_text)
xchat.hook_command('seen', command_seen, help="Local /seen nick , remote !seen nick")
xchat.hook_command('seensearch', command_seensearch, help="Local /seensearch phrase , remote !seensearch phrase")
xchat.hook_command('seencount', command_seencount, help="Merely gives total count of records in the seen db")
xchat.hook_command('seenpurge', command_seenpurge, help="Do /seenpurge 30, that will purge all records over 30 days old")
xchat.hook_command('seendump', command_seendump, help="Dumps the database to a text file in your xchatdir")
#Last modified 2-7-06
