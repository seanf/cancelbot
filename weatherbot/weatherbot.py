#!/usr/bin/python
__module_name__ = "Cancel's WeatherBot"
__module_version__ = "2.1.1" 
__module_description__ = "WeatherBot by Cancel"

import xchat
import os
import re
import ConfigParser
import threading
import weather

print "\0034",__module_name__, __module_version__,"has been loaded\003"

#---Globals---#000000#FFFFFF----------------------------------------------------
option = {}
xchatdir = xchat.get_info("xchatdir")
inifile = os.path.join(xchatdir, "weatherbot.ini")

def makedict(**kwargs):
    return kwargs

color = makedict(white="\0030", black="\0031", blue="\0032", red="\0034",
dred="\0035", purple="\0036", dyellow="\0037", yellow="\0038", bgreen="\0039",
dgreen="\00310", green="\00311", bpurple="\00313", dgrey="\00314",
lgrey="\00315", close="\003")

#---Functions---#000000#FFFFFF--------------------------------------------------
def load_vars():
    global option
    try:
        config = ConfigParser.ConfigParser()
        infile = open(inifile)
        config.readfp(infile)
        infile.close()
        #Parse Main
        for item in config.items("main"):
            option[item[0]] = item[1]
        option["service"] = config.getboolean("main", "service")        
        print color["dgreen"], "CancelBot WeatherBot weather.ini Load Success"
        
    except EnvironmentError:
        print color["red"], "Could not open weatherbot.ini  put it in your " + xchatdir

def on_text(word, word_eol, userdata):
    global option
    destination = xchat.get_context()    
    triggernick = word[0]
    trigger = re.split(' ',word[1].lower())
    
    if trigger[0] == '!weather' and option["service"] == True:
        if re.search('D', trigger[1]) or len(trigger[1]) < 5:
            destination.command("say try enter a 5 digit U.S. zip code")
        else:
            threading.Thread(target=get_weather, args=(trigger[1], destination)).start()
        

def on_pvt(word, word_eol, userdata):
    destination = xchat.get_context()
    triggernick = word[0]
    trigger = re.split(' ',word[1].lower())
    if trigger[0] == '!weather' and option["service"] == True:
        if re.search('\D', trigger[1]) or len(trigger[1]) < 5:
            destination.command("say try a 5 digit U.S. zip code")
        else:
            threading.Thread(target=get_weather, args=(trigger[1], destination)).start()

def get_weather(lookup, destination):
    response = weather.getweather(lookup)
    destination.command("say " + str(response))
    
def local_weather(word, word_eol, userdata):
        if re.search('\D', word[1]):
            print color["red"], "Try a 5 digit U.S. zip code"
        else:
            response = weather.getweather(word[1])
            print response
    
load_vars()

#The hooks go here
xchat.hook_print('Channel Message', on_text)
xchat.hook_print('Private Message to Dialog', on_pvt)
xchat.hook_command('weather', local_weather, help="do /weather zipcode")

#LICENSE GPL
#Last modified 12-17-06
