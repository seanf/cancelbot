#!/usr/bin/python
__module_name__ = "Cancel's OpBot"
__module_version__ = "2.8.0" 
__module_description__ = "OpBot by Cancel"

import xchat
import os
import re
import string
import time
import ConfigParser

print "\0034",__module_name__, __module_version__,"has been loaded\003"        

#---Globals---#000000#FFFFFF----------------------------------------------------
option = {}
users = {}
thecontext = ""
checknick = ""
clearbans = ""
usersclean = []
xchatdir = xchat.get_info("xchatdir")
inifile = os.path.join(xchatdir, "opbot.ini")
jointimer = ""
errormessage = "A valid key name or integer is required. Check the list again"
caps = ""

def makedict(**kwargs):
    return kwargs

color = makedict(white="\0030", black="\0031", blue="\0032", red="\0034",
dred="\0035", purple="\0036", dyellow="\0037", yellow="\0038", bgreen="\0039",
dgreen="\00310", green="\00311", bpurple="\00313", dgrey="\00314",
lgrey="\00315", close="\003")

#---Classes---#000000#FFFFFF----------------------------------------------------
class User:
    def __init__(self, host=''):
        self.host = host
        self.count = 0
        self.spoke = []
        while self.count < option["antifloodlimit"]:
            self.spoke.append('')
            self.count += 1
        self.slot = 0
        self.joined = 1
        self.devoiced = False
        
#---Functions---#000000#FFFFFF--------------------------------------------------        
def load_vars():
    global option, checknick, usersclean, caps, clearbans
    try:
        config = ConfigParser.ConfigParser()
        infile = open(inifile)
        config.readfp(infile)
        infile.close()
        #Parse Main
        for item in config.items("main"):
            option[item[0]] = item[1]
        
        option["autovoice"] = config.getboolean("main", "autovoice")
        option["identify"] = config.getboolean("main", "identify")
        option["check"] = config.getint("main", "check")
        option["scan"] = config.getint("main", "scan")
        option["ping"] = config.getboolean("main", "ping")
        option["uptime"] = config.getboolean("main", "uptime")
        option["capsabuse"] = config.getboolean("main", "capsabuse")
        option["capslimit"] = config.getint("main", "capslimit")
        option["limitjoins"] = config.getboolean("main", "limitjoins")
        option["limitincrement"] = config.getint("main", "limitincrement")
        option["limittime"] = config.getint("main", "limittime")
        option["antiflood"] = config.getboolean("main", "antiflood")
        option["antifloodlimit"] = config.getint("main", "antifloodlimit")
        option["antifloodtime"] = config.getint("main", "antifloodtime")
        option["clonescan"] = config.getboolean("main", "clonescan")
        option["clearbans"] = config.getboolean("main", "clearbans")
        option["clearbantime"] = config.getint("main", "clearbantime")
        option["badwordsenabled"] = config.getboolean("main", "badwordsenabled")
            
        option["opin"] = re.split(' ', option["opin"])
        option["badwords"] = re.split(' ', option["badwords"])
        option["badwordsinchannel"] = re.split(' ', option["badwordsinchannel"])
        option["badnicks"] = re.split(' ', option["badnicks"]) + option["badwords"]
        option["badchannels"] = re.split(' ', option["badchannels"]) + option["badwords"]
        
        
        #Parse Akicks
        option["badhost"] = {}
        for item in config.items("akicks"):
            item = list(item)
            item[1] = re.split(' ', item[1])
            #This adds your own nick as who added the akick if its not already present
            if len(item[1]) < 2:
                item[1].append(option["mynick"])
            option["badhost"][item[0]] = (item[1][0], item[1][1])
        
        #Parse Ops
        option["ops"] = {}
        for item in config.items("ops"):
            option["ops"][item[0]] = item[1]
            
        #Parse Allowed clones
        option["allowclones"] = option["ops"].copy()
        for item in config.items("allowclones"):
            option["allowclones"][item[0]] = item[1]
            
        #Setup user tracking dictionaries
        for channel in option["opin"]:
            users[channel] = {}
        
        #Run Time Optionals
        if option["identify"] == True:
            option["check"] *= 60000
            checknick = xchat.hook_timer(option["check"], nick_check)
            
        if option["clearbans"] == True:
            option["clearbantime"] *= 60000
            checkbans = xchat.hook_timer(option["clearbantime"], check_bans)
        
        if option["antiflood"] == True:
            option["antifloodtime"] *=  60000
            usersclean.append(xchat.hook_timer(option["antifloodtime"], users_clean_slots))
            usersclean.append(xchat.hook_timer(900000, users_clean_all))
        if re.search('int', str(type(option["scan"]))):
            option["scan"] *= 60000
            chanscan = xchat.hook_timer(option["scan"], chan_scan)
            
        if re.search('int', str(type(option["limittime"]))):
            option["limittime"] *= 1000
        
        if option["capsabuse"] == True:
            option["capslimit"] = option["capslimit"]
            caps = re.compile('[ABCDEFGHIJLKMNOPQRSTUVWXYZ]')
            
        print color["dgreen"], "CancelBot OpBot opbot.ini Load Success"
    
    except EnvironmentError:
        print color["red"], "Could not open opbot.ini  put it in your " + xchatdir
    
    except Exception, args:
        print color["red"], args

def save_vars():
    global option
    config = ConfigParser.ConfigParser()
    infile = open(inifile)
    config.readfp(infile)
    infile.close()
    
    config.remove_section("akicks")
    config.add_section("akicks")
    
    for key in option["badhost"]:
        config.set("akicks", key, option["badhost"][key][0] + " " + 
        option["badhost"][key][1])
    
    for badword in option["badwords"]:
        if badword in option["badnicks"]:
            option["badnicks"].remove(badword)
        if badword in option["badchannels"]:
            option["badchannels"].remove(badword)
    
    config.set("main", "autovoice", option["autovoice"])
    config.set("main", "limitjoins", option["limitjoins"])
    config.set("main", "badchannels", string.join(option["badchannels"]))
    config.set("main", "badnicks", string.join(option["badnicks"]))
    config.set("main", "badwords", string.join(option["badwords"]))
    
    infile = open(inifile, "w")
    config.write(infile)
    infile.close()
    
    option["badchannels"] += option["badwords"]
    option["badnicks"] += option["badwords"]
    
def on_text(word, word_eol, userdata):
    global option
    destination = xchat.get_context()    
    triggerchannel = destination.get_info("channel")
    triggernick = word[0].lower()
    trigger = re.split(' ',word[1].lower())
    prefix = ""
        
    if triggerchannel in option["opin"]:
        userlist = destination.get_list("users")
        for user in userlist:
                if triggernick == string.lower(user.nick):
                    host = user.host
                    break
            
        if len(word) == 3:
            prefix = word[2]
        
        if option["badwordsenabled"] == True and triggerchannel in option["badwordsinchannel"]:
            for badword in option["badwords"]:
                if re.search(badword, word[1], re.I) and prefix != "@":
                    destination.command("kickban " + triggernick + " " + option["msgbadword"])
                
        if option["capsabuse"] == True and prefix != "@":
            length = float(len(word[1]))
            capcount = float(0)
            
            for char in word[1]:
                if caps.search(char):
                    capcount += 1
                    
            if capcount / length * 100 >= option["capslimit"] and length >= 50:
                destination.command("kick " + triggernick + " " + option["msgcapsabuse"] + " CAPS Abuse " + str(option["capslimit"])+"%")
        
        # Flood protection items if user isnt in the dictionary add them
        if triggernick not in users[triggerchannel]:
            users[triggerchannel][triggernick] = User(host = user.host)
        
        #Takes what the user says and places it in a slot then compares the slots
        if option["antiflood"] == True and prefix != "@":
            if users[triggerchannel][triggernick].slot >= option["antifloodlimit"] -1:
                users[triggerchannel][triggernick].slot = 0
            else:
                users[triggerchannel][triggernick].slot += 1
            users[triggerchannel][triggernick].spoke[users[triggerchannel][triggernick].slot] = trigger
            
            if users[triggerchannel][triggernick].spoke.count(users[triggerchannel][triggernick].spoke[0]) >= option["antifloodlimit"]:
                destination.command("kick " + triggernick + " " + option["msgrepeatflood"])    
            
        if trigger[0] == "!voice":
            if prefix == "@":
                destination.command("voice " + string.join(trigger[1:]))
            elif option["ops"].has_key(triggernick):
                if re.search(option["ops"][triggernick],host,re.I):
                    destination.command("voice " + string.join(trigger[1:]))
            else:
                destination.command("devoice " + triggernick)

        elif trigger[0] == "!devoice":
            if prefix == "@":
                destination.command("devoice " + string.join(trigger[1:]))
            elif option["ops"].has_key(triggernick):
                if re.search(option["ops"][triggernick],host,re.I):
                    destination.command("devoice " + trigger[1])
            else:
                destination.command("devoice " + triggernick)

        elif trigger[0] == "!kick":
            if prefix == "@":
                destination.command("kick " + trigger[1])
            elif option["ops"].has_key(triggernick):
                if re.search(option["ops"][triggernick],host,re.I):
                    destination.command("kick " + trigger[1])
            else:
                destination.command("kick " + triggernick)

        elif trigger[0] == "!ban":
            if prefix == "@":
                destination.command("kickban " + trigger[1])
            elif option["ops"].has_key(triggernick):
                if re.search(option["ops"][triggernick],host,re.I):
                    destination.command("kickban " + trigger[1])
            else:
                destination.command("kickban " + triggernick)
                
        elif trigger[0] == "!unban":
            if prefix == "@":
                destination.command("unban " + trigger[1])
            elif option["ops"].has_key(triggernick):
                if re.search(option["ops"][triggernick],host,re.I):
                    destination.command("unban " + trigger[1])
            else:
                destination.command("kickban " + triggernick)

        elif trigger[0] == "!autovoice":
            if prefix == "@":
                if trigger[1] == "true" or trigger[1] == "on" or trigger[1] == "yes":
                    option["autovoice"] = True
                elif trigger[1] == "false" or trigger[1] == "off" or trigger[1] == "no":
                    option["autovoice"] = False
                destination.command("say autovoice is set to " + color["blue"] + str(option["autovoice"]))
                save_vars()
            elif option["ops"].has_key(triggernick):
                if re.search(option["ops"][triggernick],host,re.I):
                    if trigger[1] == "true" or trigger[1] == "on" or trigger[1] == "yes":
                        option["autovoice"] = True
                    elif trigger[1] == "false" or trigger[1] == "off" or trigger[1] == "no":
                        option["autovoice"] = False
                destination.command("say autovoice is set to " + color["blue"] + str(option["autovoice"]))
                save_vars()
            else:
                destination.command("kick " + triggernick)
                
        elif trigger[0] == "!limitjoins":
            if prefix == "@":
                if trigger[1] == "true" or trigger[1] == "on" or trigger[1] == "yes":
                    option["limitjoins"] = True
                elif trigger[1] == "false" or trigger[1] == "off" or trigger[1] == "no":
                    option["limitjoins"] = False
                destination.command("say limitjoins is set to " + color["blue"] + str(option["limitjoins"]))
                save_vars()
            elif option["ops"].has_key(triggernick):
                if re.search(option["ops"][triggernick],host,re.I):
                    if trigger[1] == "true" or trigger[1] == "on" or trigger[1] == "yes":
                        option["limitjoins"] = True
                    elif trigger[1] == "false" or trigger[1] == "off" or trigger[1] == "no":
                        option["limitjoins"] = False
                destination.command("say limitjoins has been set " + color["blue"] + str(option["limitjoins"]))
                save_vars()
            else:
                destination.command("kick " + triggernick)
        
        elif trigger[0] == "!akick":
            if option["ops"].has_key(triggernick):
                if re.search(option["ops"][triggernick],host,re.I):
                    akick(triggernick, trigger)
            elif prefix != "@":
                destination.command("kickban " + triggernick)
                    
        elif trigger[0] == "!badwords":
            if option["ops"].has_key(triggernick):
                if re.search(option["ops"][triggernick],host,re.I):
                    badwords(triggernick, trigger)
            elif prefix != "@":
                destination.command("kickban " + triggernick)
                    
        elif trigger[0] == "!badnicks":
            if option["ops"].has_key(triggernick):
                if re.search(option["ops"][triggernick],host,re.I):
                    badnicks(triggernick, trigger)
            elif prefix != "@":
                destination.command("kickban " + triggernick)
                    
        elif trigger[0] == "!badchannels":
            if option["ops"].has_key(triggernick):
                if re.search(option["ops"][triggernick],host,re.I):
                    badchannels(triggernick, trigger)
            elif prefix != "@":
                destination.command("kickban " + triggernick)

    if trigger[0] == "!ping" and option["ping"] == True:
        destination.command("ping " + triggernick)
            
    if trigger[0] == "!uptime" and option["uptime"] == True:
        uptime = os.popen("uptime").read()
        destination.command("say " + uptime)

def on_join(word, word_eol, userdata):
    global thecontext
    global jointimer
    triggernick = word[0].lower()
    triggerchannel = word[1].lower()
    triggerhost = word[2].lower()
    thecontext = xchat.get_context()
    
    if triggerchannel in option["opin"]:
        xchat.command("whois " + triggernick)
        
        if option["clonescan"] == True:
            clonescan()

        if triggerchannel in option["limitchannels"] and option["limitjoins"] == True:
            if jointimer:
                xchat.unhook(jointimer)
                jointimer = None
            jointimer = xchat.hook_timer(option["limittime"], join_limit, userdata=thecontext)

        if option["antiflood"] == False and option["autovoice"] == True and triggerchannel in option["voicein"]:
            thecontext.command("voice " + triggernick)
        
        elif option["antiflood"] == True:
            #Check if the user is in the dictionary if not check if their host matches any if not add it
            if triggernick not in users[triggerchannel]:
                for user in users[triggerchannel]:
                    if users[triggerchannel][user].host == triggerhost:
                        users[triggerchannel][triggernick] = users[triggerchannel][user]
                        break
            #check the dictionary again as we may have added during the host check
            if triggernick not in users[triggerchannel]:
                users[triggerchannel][triggernick] = User(host = triggerhost)
                
            else:
                users[triggerchannel][triggernick].joined += 1
                
            if users[triggerchannel][triggernick].joined >= option["antifloodlimit"]:
                thecontext.command("ban " + "*!" + triggerhost)
                thecontext.command("kick " + triggernick + " " + option["msgjoinflood"])
            if triggerchannel in option["voicein"] and option["autovoice"] == True:
                for user in users[triggerchannel]:
                    if users[triggerchannel][user].host == triggerhost and users[triggerchannel][user].devoiced == False:
                        thecontext.command("voice " + triggernick)
                        break

def join_limit(userdata):
    userlist = userdata.get_list('users')
    newlimit = option["limitincrement"] + len(userlist)
    userdata.command("mode +l " + str(newlimit))
    
def on_part(word, word_eol, userdata):
    global jointimer
    if jointimer:
        xchat.unhook(jointimer)
        jointimer = None
    triggerchannel = word[2].lower()
    thecontext = xchat.find_context(channel=triggerchannel)
    if triggerchannel in option["opin"]:
        if triggerchannel in option["limitchannels"] and option["limitjoins"] == True:
            jointtimer = xchat.hook_timer(option["limittime"], part_limit, userdata=thecontext)
    
def part_limit(userdata):
    userlist = userdata.get_list('users')
    newlimit = option["limitincrement"] + len(userlist)
    userdata.command("mode +l " + str(newlimit))
    
def on_change_nick(word, word_eol, userdata):
    global thecontext
    oldnick = word[0].lower()
    newnick = word[1].lower()
    thecontext = xchat.get_context()
    triggerchannel = xchat.get_info("channel")
    xchat.command("whois " + newnick)
    if triggerchannel in option["opin"] and option["antiflood"] == True:
        if oldnick in users[triggerchannel]:
            users[triggerchannel][newnick] = users[triggerchannel][oldnick]
        else:
            userlist = thecontext.get_list("users")
            for user in userlist:
                if newnick == user.nick:
                    users[triggerchannel][newnick] = User(host = user.host)
                    break
    
def on_whois_nameline(word, wordeol, userdata):
    global thecontext
    nickname = word[0].lower()
    username = word[1].lower()
    host = word[2].lower()
    fullname = word[3].lower()
    
    for badword in option["badnicks"]:
        if re.search(badword, str(word), re.I):
            thecontext.command("ban " + host)
            thecontext.command("kick " + nickname + " " + option["msgbadnick"])

    for key in option["badhost"]:
        if re.search(option["badhost"][key][0], host, re.I):
            thecontext.command("ban " + host)
            thecontext.command("kick " + nickname + " " + option["msgbadhost"] +" " +  key + ":" + option["badhost"][key][1])

def on_whois_channels(word, wordeol, userdata):
    global thecontext
    nickname = word[0].lower()
    channels = word[1].lower()
    
    for badword in option["badchannels"]:
        if badword in channels:
            thecontext.command("ban " + nickname)
            thecontext.command("kick " + nickname + " " + option["msgbadchannel"])

def on_notice(word, wordeol, userdata):
    triggernickname = word[0]
    message = word[1]
    if option["identify"] == True:
        if triggernickname == option["identifyfrom"] and option["identifyphrase"] in message:
            nick_check()

def users_clean_all(userdata):
    for channel in users:
        users[channel].clear()
    return 1

def users_clean_slots(userdata):
    for channel in users:
        for user in users[channel]:
            count = 0
            users[channel][user].joined = 1
            while count < option["antifloodlimit"]:
                users[channel][user].spoke[count] = ''
                count += 1
    return 1

def nick_check(userdata):
    if xchat.get_info("nick") != option["mynick"]:
        xchat.command("release")
        xchat.command("nick " + option["mynick"])
        for chan in option["opin"]:
            xchat.command("chanserv op " + chan + " " + option["mynick"])
    return 1 
    
def chan_scan(userdata):
    global thecontext
    for chan in option["opin"]:
        thecontext = xchat.find_context(channel=chan)
        userlist = thecontext.get_list('users')
        for user in userlist:
            xchat.command("whois " + user.nick)
    return 1

def check_bans(userdata):
    for chan in option["opin"]:
        thecontext = xchat.find_context(channel=chan)
        thecontext.command("banlist")
    return 1

def on_banlist(word, wordeol, userdata):
    thecontext = xchat.get_context()
    triggerchannel = word[0]
    if triggerchannel in option["opin"] and option["clearbans"] == True:
        banmask = word[1]
        #time is like Sun Feb  3 12:40:12, we have to add the year
        bantime = str(time.localtime()[0]) + " " + word[3]
        #get us a struct_time tuple
        bantime = time.strptime(bantime, "%Y %a %b  %d %H:%M:%S")
        #seconds from epoch
        bantime = time.mktime(bantime)
        if time.time() > option["clearbantime"] /1000 + bantime:
            thecontext.command("unban " + banmask)
    
def on_devoice(word, word_eol, userdata):
    thecontext = xchat.get_context()
    triggerchannel = thecontext.get_info("channel")
    triggernick = word[1].lower()
    if triggerchannel in option["opin"] and option["antiflood"] == True:
        if triggernick in users[triggerchannel]:
            users[triggerchannel][triggernick].devoiced = True
        else:
            userlist = thecontext.get_list("users")
            for user in userlist:
                if triggernick == user.nick:
                    host = user.host
                    break
            users[triggerchannel][triggernick] = User(host)
            users[triggerchannel][triggernick].devoiced = True
    
def on_voice(word, word_eol, userdata):
    thecontext = xchat.get_context()
    triggerchannel = thecontext.get_info("channel")
    triggernick = word[1].lower()
    if triggerchannel in option["opin"] and option["antiflood"] == True:
        if triggernick in users[triggerchannel]:
            users[triggerchannel][triggernick].devoiced = False
        else:
            userlist = thecontext.get_list("users")
            for user in userlist:
                if triggernick == user.nick:
                    host = user.host
                    break
            users[triggerchannel][triggernick] = User(host = user.host)
        
def akick(triggernick, trigger):
    global option
    try:
        if len(trigger) == 2 and trigger[1] == "list":
            xchat.command("msg " + triggernick + " The akicks are:")
            for key in option["badhost"]:
                xchat.command("msg " + triggernick + " " + key + ":" + \
                option["badhost"][key][0] + " by " + option["badhost"][key][1])
            xchat.command("msg " + triggernick + " End list")
        
        elif len(trigger) == 3 and trigger[1] == "del":
            option["badhost"].pop(trigger[2])
            xchat.command("msg " + triggernick + " " + trigger[2]  + \
            " has been deleted from the bot's akick list")
            save_vars()
        
        elif len(trigger) == 4 and trigger[1] == "add":
            option["badhost"][trigger[2]] = (trigger[3], triggernick)
            xchat.command("msg " + triggernick + " " + trigger[2] + ":" + trigger[3] + \
            " has been added to the bot's akick list")
            save_vars()
            
    except Exception, args:
        xchat.command("msg " + triggernick + " " + errormessage)
        
def badwords(triggernick, trigger):
    global option
    count = 0
    try:
        if len(trigger) == 2 and trigger[1] == "list":
            xchat.command("msg " + triggernick + " The badwords are:")
            for badword in option["badwords"]:
                xchat.command("msg " + triggernick + " " + str(count) + ":" + badword)
                count += 1
            xchat.command("msg " + triggernick + " End list")
        
        elif len(trigger) == 3 and trigger[1] == "del":
            option["badwords"].pop(int(trigger[2]))
            xchat.command("msg " + triggernick + " " + trigger[2]  + \
            " has been deleted from the bot's badword list")
            save_vars()
            
        elif len(trigger) == 3 and trigger[1] == "add":
            option["badwords"].append(trigger[2])
            xchat.command("msg " + triggernick + " " + trigger[2] + \
            " has been added to the bot's badword list")
            save_vars()
            
    except Exception, args:
        xchat.command("msg " + triggernick + " " + errormessage)
        
def badnicks(triggernick, trigger):
    global option
    count = 0
    try:
        if len(trigger) == 2 and trigger[1] == "list":
            xchat.command("msg " + triggernick + " The badnicks are:")
            for badnick in option["badnicks"]:
                xchat.command("msg " + triggernick + " " + str(count) + ":" + badnick)
                count += 1
            xchat.command("msg " + triggernick + " End list")
        
        elif len(trigger) == 3 and trigger[1] == "del":
            option["badnicks"].pop(int(trigger[2]))
            xchat.command("msg " + triggernick + " " + trigger[2]  + \
            " has been deleted from the bot's badnicks list")
            save_vars()
            
        elif len(trigger) == 3 and trigger[1] == "add":
            option["badnicks"].append(trigger[2])
            xchat.command("msg " + triggernick + " " + trigger[2] + \
            " has been added to the bot's badnicks list")
            save_vars()
            
    except Exception:
        xchat.command("msg " + triggernick + " " + errormessage)
        
def badchannels(triggernick, trigger):
    global option
    count = 0
    try:
        if len(trigger) == 2 and trigger[1] == "list":
            xchat.command("msg " + triggernick + " The badchannels are:")
            for badchannel in option["badchannels"]:
                xchat.command("msg " + triggernick + " " + str(count) + ":" + badchannel)
                count += 1
            xchat.command("msg " + triggernick + " End list")
        
        elif len(trigger) == 3 and trigger[1] == "del":
            option["badchannels"].pop(int(trigger[2]))
            xchat.command("msg " + triggernick + " " + trigger[2]  + \
            " has been deleted from the bot's badchannels list")
            save_vars()
            
        elif len(trigger) == 3 and trigger[1] == "add":
            option["badchannels"].append(trigger[2])
            xchat.command("msg " + triggernick + " " + trigger[2] + \
            " has been added to the bot's badchannels list")
            save_vars()
            
    except Exception:
        xchat.command("msg " + triggernick + " " + errormessage)

def clonescan():
    global thecontext
    checklist = {}
    clones = {}
    allowed = []
    userlist = thecontext.get_list('users')
    for user in userlist:
        checklist[user.nick.lower()] = re.split('@', user.host)[1]
    for user in checklist:
        if checklist.values().count(checklist[user]) > 1:
            clones[user] = checklist[user]
    #If host in option["allowclones"] remove from clones
    for key in option["allowclones"]:
        if clones.has_key(key):
            if re.search(option["allowclones"][key], clones[key], re.I):
                allowed.append(key)
    if allowed:
        for user in allowed:
            del(clones[user])
    if clones:
        for clone in clones:
            thecontext.command(option["cloneresponse"] + " " + clone + " " + option["clonemessage"])

def clonescan_local(word, word_eol, userdata):
   thecontext = xchat.find_context()
   checklist = {}
   clones = []
   userlist = thecontext.get_list('users')
   for user in userlist:
     checklist[user.nick] = re.split('@', user.host)[1]
   for user in checklist:
     if checklist.values().count(checklist[user]) > 1:
        clones.append((checklist[user], user))
   if clones:
    clones.sort()
    print color["red"] + "The following clones were found in " + \
    thecontext.get_info('channel') + ":"
    for clone in clones:
        print color["blue"] +  clone[1] + " " + clone[0]
   else:
    print color["blue"] + "No clones found"

   return xchat.EAT_ALL

load_vars()
#---Hooks---#000000#FFFFFF------------------------------------------------------
xchat.hook_print('Channel Message', on_text)
xchat.hook_print('Join', on_join)
xchat.hook_print('Part', on_part)
xchat.hook_print('Change Nick', on_change_nick)
xchat.hook_print('WhoIs Name Line', on_whois_nameline)
xchat.hook_print('WhoIs Channel/Oper Line', on_whois_channels)
xchat.hook_print('Notice', on_notice)
xchat.hook_print('Channel DeVoice', on_devoice)
xchat.hook_print('Channel Voice', on_voice)
xchat.hook_print('Ban List', on_banlist)
xchat.hook_command('clonescan', clonescan_local, help="/clonescan")

#LICENSE GPL
#Last modified 8-28-08
