#importing all the necessary libraries first

import pandas as pd
import numpy as np
import urllib2
from bs4 import BeautifulSoup
import json
import requests
from pprint import pprint

#getting response from the web API and then storing that in 'resp' object

url="https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=2016-10-01&endtime=2016-10-02"
resp=requests.get(url)

#Then .json method on resp object will convert it into dictionary containing JSON parsed into native python  objects

data=resp.json()

#Storing the key 'features' into a separate dictionary data1

data1=data['features']

print "Ans 1: The type of 'features' attribute is:"
print type(data1)
pprint("#...................................................................................................................#")

print "Ans 2: The number of  elements of 'features' attribute is:"
print len(data1)
pprint("#...................................................................................................................#")

print "Ans 3: The type of first element of 'features' attribute is:"
print type(data1[0])
pprint("#...................................................................................................................#")

##Reading the necessary keys from data1 dictionary and then converting that into dataframe

#First, creating a dataframe of coordinates from 'geometry' feature
i=0
dictionary={}
while i<len(data1):  
    geometry=pd.DataFrame(data1[i]['geometry'])
    dictionary[i]=geometry.loc[geometry.index[:2],'coordinates']
    i=i+1
    
coordinates=pd.DataFrame(dictionary)
coordinates.index=['Latitude','Longitude']
coordinates_new=coordinates.T
#pprint(coordinates_new)

#Second, creating a dataframe of Magnitude,Title and Place from from 'properties' feature

j=0
dictionary1={}
dictionary2={}
dictionary3={}
while j<len(data1):
    properties=data1[j]['properties']
    dictionary1[j]=properties['mag']
    dictionary2[j]=properties['place']
    dictionary3[j]=properties['title']
    j=j+1
    

Place=pd.DataFrame(dictionary2,index=["Place"])
place_new=Place.T

Mag=pd.DataFrame(dictionary1,index=["Mag"])
mag_new=Mag.T

Title=pd.DataFrame(dictionary3,index=["Title"])
title_new=Title.T

df=[coordinates_new,title_new,place_new,mag_new]
results=pd.concat(df,sort=False,axis=1)

#Converting the dataframe into CSV file
results.to_csv('results.csv', encoding='utf-8', index=False)

##reading the csv file to answer further questions.
new_data=pd.read_csv("results.csv")
print "Ans 4: The number of rows in CSV file:"
print len(new_data)
pprint("#...................................................................................................................#")
#pprint(new_data)

#Question no 5
Q5=sum(new_data['Mag']>2)
Q7=sum(new_data['Mag']>5)

pprint("Ans 5:Number of times magnitude of the earthquake was greater than 2 was: ")
pprint(Q5)
pprint("#...................................................................................................................#")

#Getting the number of earthquakes in California

k=0
count=0
str="California"
places=new_data['Place']

while k<len(places):
    if places[k][-10:]==str:
        count=count+1
         
    k=k+1 
    


pprint ("Ans 6: Number of earthquakes in California are: " ) 
pprint(count)
pprint("#...................................................................................................................#")

pprint("Ans7: Number of times magnitude of the earthquake was greater than 5 was: ")
pprint(Q7)

pprint("#...................................................................................................................#")
pprint("The first five observations of the dataframe object are:")
pprint("#...................................................................................................................#")
    
pprint(results.head(5)) 

    
      
    
     
    


