#!/usr/bin/python
__module_name__ = "Cancel's BibleBot" 
__module_version__ = "2.1.0" 
__module_description__ = "BibleBot by Cancel"

import xchat
import os
import re
import string
import threading
import ConfigParser

print "\0034",__module_name__, __module_version__,"has been loaded\003"

#---The globals go here
option = {}
versions = {}
vcolor = ""
bcolor = ""
xchatdir = xchat.get_info("xchatdir")
inifile = os.path.join(xchatdir, "biblebot.ini")
color = {"white":"\0030", "black":"\0031", "blue":"\0032", "green":"\0033", "red":"\0034",
"dred":"\0035", "purple":"\0036", "dyellow":"\0037", "yellow":"\0038", "bgreen":"\0039",
"dgreen":"\00310", "green":"\00311", "blue":"\00312", "bpurple":"\00313", "dgrey":"\00314",
"lgrey":"\00315", "close":"\003"}


#functions go here
def load_vars():
    global option, versions, vcolor, bcolor
    try:
        config = ConfigParser.ConfigParser()
        infile = open(inifile)
        config.readfp(infile)
        infile.close()
        
        #Parse main
        for item in config.items("main"):
            option[item[0]] = item[1]
            
        #bools and ints
        option["service"] = config.getboolean("main", "service")
        option["advertise"] = config.getboolean("main", "advertise")
        option["verselimit"] = config.getint("main", "verselimit")
        option["searchlimit"] = config.getint("main", "searchlimit")
        option["locallimit"] = config.getint("main", "locallimit")
        option["cleanup"] = config.getboolean("main", "cleanup")
        option["cleanuptime"] = config.getint("main", "cleanuptime")
        
        bcolor = color[option["bookcolor"]]
        vcolor = color[option["versecolor"]]
        if option["cleanup"]:
            option["cleanuptime"] = option["cleanuptime"] * 60000
            xchat.hook_timer(option["cleanuptime"], cleanup)
        print color["dgreen"], "CancelBot Biblebot biblebot.ini Load Success"
    
    except EnvironmentError:
        print color["red"], "Could not open biblebot.ini  put it in your " + xchatdir
    
    try:
        versions = os.listdir(option["bibleroot"])
        print color["dgreen"], "CancelBot Biblebot Versions Load Success"
        
    except EnvironmentError:
        print color["red"], "Could not get directory list.  Check permisions or biblebot.ini"

def get_text(trigger, destination):
    try:
        version, book, passage = trigger
        versecount = 1
        chapter = 1
        firstverse = 1 #this is here because the concordance has no firstveerse
        lastverse = 1
        
        if ':' in passage:
            splitwork = re.split(':',passage)
            chapter = splitwork[0]
            firstverse = splitwork[1]
            passage = chapter + ':' + str(firstverse)
            if '-' in passage:
                firstverse, lastverse = re.split('-', splitwork[1])
                firstverse = int(firstverse)
                lastverse = int(lastverse)
                passage = chapter + ':' + str(firstverse)
                if lastverse - firstverse <= option["verselimit"] and lastverse > firstverse:
                    versecount = lastverse - firstverse + 1
                elif lastverse <= firstverse:
                    versecount = 1
                else:
                    versecount = option["verselimit"]
        
    except Exception,args:
        return
    
    try:
        infile = os.path.join(option["bibleroot"], version, book)
        infile = open(infile, "r")
            
    except EnvironmentError:
        destination.command("say All books are " + color["blue"] + "3" + color["close"] + " characters. Check syntax and try again")
        return
    
    line = string.rstrip(infile.readline())
    position = "a"
    
    while versecount > 0 and position != infile.tell():
        if re.match(passage, line):
            destination.command("say " + bcolor + version + " " + vcolor + book + color["close"] + " " + line)
            versecount = versecount - 1
            firstverse = int(firstverse) + 1
            passage = str(chapter) + ':' + str(firstverse)
        position = infile.tell()
        line = string.rstrip(infile.readline())
    infile.close()
      
def get_search(version, phrase, destination):
    try:
        searchpath = os.path.join(option["bibleroot"], version)        
        os.chdir(searchpath)
        phrase = string.join(phrase, ' ')
        grep = os.popen("grep -i \"" + phrase + "\" *").readlines()
        found = len(grep)
        searchcount = 0

    except Exception,args:
        return

    if found == 0:
        xchat.command("msg " + destination + " No matches for \"" + phrase + "\" found")
        return
        
    for i in grep:
        i = string.strip(i)
        if searchcount == option["searchlimit"]:
            xchat.command("msg " + destination + " Search limit is " + str(option["searchlimit"]) + " matches maybe try !searchbybook")
            break
        xchat.command("msg " + destination + " " + color["red"] + version + color["close"] + " " + i)
        searchcount = searchcount + 1
    
    xchat.command("msg " + destination + " \"" + phrase + "\" was found a total of " + str(found) + " time(s)")
    
    
def get_searchbybook(version, book, phrase, destination):
    try:
        searchpath = os.path.join(option["bibleroot"], version)        
        os.chdir(searchpath)
        phrase = string.join(phrase, ' ')
        grep = os.popen("grep -i \"" + phrase + "\" " + book).readlines()
        found = len(grep)
        searchcount = 0

    except Exception,args:
        return

    if found == 0:
        xchat.command("msg " + destination + " No matches for \"" + phrase + "\" found")
        return
        
    for i in grep:
        i = string.strip(i)
        if searchcount == option["searchlimit"]:
            xchat.command("msg " + destination + " Search limit is " + str(option["searchlimit"]) + " matches")
            break
        xchat.command("msg " + destination + " " + color["red"] + version + color["close"] + " " + book + " " + i)
        searchcount = searchcount + 1
    
    xchat.command("msg " + destination + " \"" + phrase + "\" was found a total of " + str(found) + " time(s) in " + book)
    

def play_file(file, destination):
    try:
        infile = open(file,"r")
        
    except EnvironmentError:
        print color["red"], "Could not open " + file + ".  Check permisions or biblebot.ini"
        return
    
    position = "a"
    
    while position != infile.tell():
        position = infile.tell()
        line = string.strip(infile.readline())
        xchat.command("msg " + destination + " " + line)
    infile.close()

def get_list(version, destination):
    try:
        books = os.listdir(os.path.join(option["bibleroot"], version))
        books = string.join(books, ' ')
    except EnvironmentError:
        print color["red"], "Could not get directory list.  Check permisions or biblebot.ini"
        return
        
    xchat.command("msg " + destination + " " + color["red"] + version + color["close"] + " " + books)
        
def on_text(word, word_eol, userdata):
    destination = xchat.get_context()    
    triggernick = word[0]
    trigger = re.split(' ',string.lower(word[1]))
    
    if option["service"] == True:
        if trigger[0] in versions:
            threading.Thread(target=get_text, args=(trigger[:3], destination)).start()
    
        if trigger[0] == '!search' and trigger[1] in versions:
            threading.Thread(target=get_search, args=(trigger[1], trigger[2:], triggernick)).start()
            
        if trigger[0] == '!searchbybook' and trigger[1] in versions:
            threading.Thread(target=get_searchbybook, args=(trigger[1], trigger[2], trigger[3:], triggernick)).start()
        
        if trigger[0] == '!help':
            threading.Thread(target=play_file, args=(option["helpfile"], triggernick)).start()
        
        if trigger[0] == '!rules':
            threading.Thread(target=play_file, args=(option["rulesfile"], triggernick)).start()
        
        if trigger[0] == '!versions':
            threading.Thread(target=play_file, args=(option["versionfile"], triggernick)).start()
        
        if trigger[0] == '!list' and trigger[1] in versions:
            threading.Thread(target=get_list, args=(trigger[1], triggernick)).start()
    
def pvt_request(word, word_eol, userdata):
    destination = xchat.get_context()
    triggernick = word[0]
    trigger = re.split(' ',string.lower(word[1]))

    if option["service"] == True:
        if trigger[0] in versions and option["service"] == True:
            threading.Thread(target=get_text, args=(trigger[:3], destination)).start()
    
        if trigger[0] == '!search' and trigger[1] in versions:
            threading.Thread(target=get_search, args=(trigger[1], trigger[2:], triggernick)).start()
            
        if trigger[0] == '!searchbybook' and trigger[1] in versions:
            threading.Thread(target=get_searchbybook, args=(trigger[1], trigger[2], trigger[3:], triggernick)).start()
        
        if trigger[0] == '!help':
            threading.Thread(target=play_file, args=(option["helpfile"], triggernick)).start()
        
        if trigger[0] == '!rules':
            threading.Thread(target=play_file, args=(option["rulesfile"], triggernick)).start()
        
        if trigger[0] == '!versions':
            threading.Thread(target=play_file, args=(option["versionfile"], triggernick)).start()
        
        if trigger[0] == '!list' and trigger[1] in versions:
            threading.Thread(target=get_list, args=(trigger[1], triggernick)).start()
    
def on_join(word, word_eol, userdata):
    triggernick = word[0]
    triggerchannel = word[1]
    if option["advertise"] == True and triggerchannel in option["advertisein"]:
        xchat.command("notice " + triggernick + " " + option["advertisetext"])

def bible(word, word_eol, userdata):
    try:
        version, book, passage = word[1:4]
        versecount = 1
        chapter = 1
        firstverse = 1 #this is here because the concordance has no firstverse
        lastverse = 1
        
        if ':' in passage:
            splitwork = re.split(':',passage)
            chapter = splitwork[0]
            firstverse = splitwork[1]
            passage = chapter + ':' + str(firstverse)
            if '-' in passage:
                firstverse, lastverse = re.split('-', splitwork[1])
                firstverse = int(firstverse)
                lastverse = int(lastverse)
                passage = chapter + ':' + str(firstverse)
                if lastverse > firstverse:
                    versecount = lastverse - firstverse + 1
                elif lastverse <= firstverse:
                    versecount = 1
        
    except Exception, args:
        return xchat.EAT_ALL
    
    try:
        infile = os.path.join(option["bibleroot"], version, book)
        infile = open(infile, "r")
            
    except Exception, args:
        return xchat.EAT_ALL
    
    line = string.rstrip(infile.readline())
    position = "a"
    while versecount >= 1 and position != infile.tell():
        if re.match(passage, line):
            print(bcolor + version + " " + vcolor + book + color["close"] + " " + line)
            versecount = versecount - 1
            firstverse = int(firstverse) + 1
            passage = str(chapter) + ":" + str(firstverse)
        position = infile.tell()
        line = string.rstrip(infile.readline())
    infile.close()
    
    return xchat.EAT_ALL
    
def search(word, word_eol, data):
    try:
        version = word[1]
        searchpath = os.path.join(option["bibleroot"], version)
        os.chdir(searchpath)
        phrase = string.join(word[2:], ' ')
        grep = os.popen("grep -i \"" + phrase + "\" *").readlines()
        found = len(grep)
        searchcount = 0

    except Exception, args:
        return xchat.EAT_ALL

    if found == 0:
        print("No matches for \"" + phrase + "\" found")
        return xchat.EAT_ALL
        
    for i in grep:
        i = string.strip(i)
        if searchcount == option["searchlimit"]:
            print("Search limit is "+str(option["locallimit"])+" matches")
            break
        print(color["red"] + version + color["close"] + " " +i)
        searchcount = searchcount + 1
    
    print("\"" + phrase + "\" was found a total of " + str(found) + " time(s)")
    
    return xchat.EAT_ALL

def cleanup(userdata):
    channels = xchat.get_list('channels')
    for channel in channels:
        if channel.type == 3:
            channel.context.command('close')
    return 1

load_vars()
#The hooks go here
xchat.hook_print('Channel Message', on_text)
xchat.hook_print('Private Message to Dialog', pvt_request)
xchat.hook_print('Join', on_join)
xchat.hook_command('bible', bible)
xchat.hook_command('search', search)
#LICENSE GPL
#Last modified 12-13-06
