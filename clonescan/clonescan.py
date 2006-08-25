#!/usr/bin/python
__module_name__ = "Cancel's CloneScan"
__module_version__ = "1.0.1"
__module_description__ = "CloneScan by Cancel"

import xchat
import re

print "\0034",__module_name__, __module_version__,"has been loaded\003"

def makedict(**kwargs):
    return kwargs

color = makedict(white="\0030", black="\0031", blue="\0032", red="\0034",
dred="\0035", purple="\0036", dyellow="\0037", yellow="\0038", bgreen="\0039",
dgreen="\00310", green="\00311", bpurple="\00313", dgrey="\00314",
lgrey="\00315", close="\003")

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

xchat.hook_command('clonescan', clonescan_local, help="/clonescan #channel")

#LICENSE GPL
#Last modified 4-8-06

