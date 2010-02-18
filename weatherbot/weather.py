#!/usr/bin/python
############################################################################
#    Copyright (C) 2008 by JTP                                             #
#    jtpowell at users dot sourceforge dot net                                           #
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
"""Using the weather module
returns a dictionary of weather data if found on error a string with the exception args
getweather("90210")
getweather("Cairo")
"""

import urllib
from xml.dom.minidom import parseString

_baseURL = "http://www.google.com/ig/api?weather="
def getweather(locale):
    """get the weather by zip or locale"""
    finalURL = _baseURL + locale
    weather = {}
    
    try:
        xmlData = urllib.urlopen(finalURL).read()
        dom1 = parseString(xmlData)
        forecastInformation =  dom1.getElementsByTagName("forecast_information")[0]
        currentConditions = dom1.getElementsByTagName("current_conditions")[0]
        
        weather["city"] = forecastInformation.getElementsByTagName("city")[0].getAttribute("data")
        weather["postalCode"] = forecastInformation.getElementsByTagName("postal_code")[0].getAttribute("data")
        weather["forecastDate"] = forecastInformation.getElementsByTagName("forecast_date")[0].getAttribute("data")
        weather["condition"] = currentConditions.getElementsByTagName("condition")[0].getAttribute("data")
        weather["tempF"]= currentConditions.getElementsByTagName("temp_f")[0].getAttribute("data")
        weather["tempC"]= currentConditions.getElementsByTagName("temp_c")[0].getAttribute("data")
        weather["humidity"]= currentConditions.getElementsByTagName("humidity")[0].getAttribute("data")
        weather["windCondition"]= currentConditions.getElementsByTagName("wind_condition")[0].getAttribute("data")

        dom1.unlink()
        return weather

    except Exception, args:
        print args
        return args

#Last edited 02-17-10
