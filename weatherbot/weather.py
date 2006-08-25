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
"""Using the weather module
Usage: There is one "public" method getweather.  It should always be passed a string.  Depending on the results you will get back a dictionary or string.

getweather("90210")
{'City': 'Local Forecast for Beverly Hills, CA (90210)', 'UV Index': '0 Low', 'Temp': '56FFeels Like 56F', 'Visibility': '9.0 miles', 'Humidity': '90%', 'Pressure': '29.76in.', 'Pressure:': '', 'Dew Point': '53F', 'Wind': 'From N at 11 mph'}

getweather("9021") or getweather('chicago')
If less then 5 digits or non numbers are input an exception is raised

getweather("33333")
If the zipcode is invalid a string saying "Check Zip" will be returned
"""

import re, string, urllib, HTMLParser

class __Stripper(HTMLParser.HTMLParser):
    def strip(self, some_html):
        self.theString = ""
        self.feed(some_html)
        self.close()
        return self.theString
        
    def handle_data(self, data):
        self.theString += data
        
def getweather(zipcode):
    """5 Digit U.S. zipcode"""
    weather = {"City":'', "Temp":'', "UV Index":'', "Wind":'', "Humidity":'',
               "Pressure":'', "Dew Point":'', "Visibility":''}
    stripper = __Stripper()
    nonefound = "No items found"
    city = "Local Forecast for"
    temp = "Feels Like"
    uv = "UV Index:"
    wind = "Wind:"
    humidity = "Humidity:"
    pressure = "Pressure:"
    dew = "Dew Point:"
    visibility = "Visibility:</td>" 
    
    try:
        if len(zipcode) < 5 or re.search('\D',zipcode):
            raise ValueError
    
    except ValueError:
        return "Try a 5 digit U.S. Zip Code"
        
    try:
        lines = urllib.urlopen("http://www.weather.com/weather/local/"+zipcode+"?lswe="+zipcode+"&lwsa=WeatherLocalUndeclared").readlines()
        
        for line in lines:
            if re.match(nonefound, line, re.I):
                return "No data returned. Check your zipcode and try again"
                
            if re.search(city, line, re.I):
                weather["City"] = line
            if re.search(temp, line, re.I):
                weather["Temp"] = line
            if re.search(uv, line, re.I):
                position = lines.index(line)
                position += 2
                weather["UV Index"] = lines[position]
            if re.search(wind, line, re.I):
                position = lines.index(line)
                position += 2
                weather["Wind"] = lines[position]
            if re.search(humidity, line, re.I):
                position = lines.index(line)
                position += 2
                weather["Humidity"] = lines[position]
            if re.search(pressure, line, re.I):
                position = lines.index(line)
                position += 3
                weather["Pressure"] = lines[position]
            if re.search(dew, line, re.I):
                position = lines.index(line)
                position += 2
                weather["Dew Point"] = lines[position]
            if re.search(visibility, line, re.I):
                position = lines.index(line)
                position += 2
                weather["Visibility"] = lines[position]
                
        for key in weather:
            weather[key] = stripper.strip(weather[key])
            weather[key] = string.translate(weather[key],string.maketrans('',''),'\t''\r''\n')
            weather[key] = string.strip(weather[key])
        
        return weather

            
    except Exception, args:
        print args
        return args

#Last edited 3-8-06
