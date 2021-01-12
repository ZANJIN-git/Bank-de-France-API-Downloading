#!/usr/bin/env python
# coding: utf-8




import numpy as np
import pandas as pd
import json
import requests
from urllib.request import urlopen
#from pandas.io.json import json_normalize 
import os 





#API Downloading
os.chdir("C:\\Users\\zjin2\\Desktop\\python\\Data")

#Set up client id and api screen
client_id = ''
api_secret = ''
start = '2019-10'

#Set up url and start reading data
url = 'https://api.webstat.banque-france.fr/webstat-en/v1/catalogue?client_id='+ client_id+'&format=json'
data = urlopen(url).read()

dataList = json.loads(data)

#Select datasets and append
for i in range(len(dataList)):
  dataset = dataList[i]['name']
  print(dataset)
  url = 'https://api.webstat.banque-france.fr/webstat-en/v1/data/'+ dataset +   '?client_id=' + client_id+'&format=json&detail=dataonly' +   '&startPeriod=' + start
  
  r = requests.get(url)
  j = r.json()
  list1 = [j['seriesObs'][i]['ObservationsSerie']            for i in range(len(j['seriesObs']))]
  list2 = [list1[i]['observations'] for i in range(len(list1))]
  if any(list2)==True:
      

    name_list = []
    keys = ['title','titleCompl','frequency','seriesKey']
    for item in list1:
        name_dict = { key:value for key, value in item.items() if key in keys }
        name_list.append(name_dict)
    value_list = []
    for item,name in zip(list2,name_list):
         if len(item) != 0:
               for i in range(len(item)):
                 value_dict = item[i]['ObservationPeriod']
                 value_dict.update(name)
                 value_list.append(value_dict)
         else:
             value_list.append({})

#Form data frame and clean
      
    df = pd.DataFrame(value_list)
    #df = df.dropna()

    df_meta = df[['frequency','title','titleCompl','seriesKey']].groupby('title').first()
    df.rename(columns={'periodFirstDate':'date'}, inplace=True)
     
    df.index = pd.DatetimeIndex(df['date'])
     
    df.drop(['frequency','date','periodId','periodName','titleCompl','seriesKey'], axis=1, inplace=True)
    df = df.pivot_table(index = df.index.values, columns = 'title',values='value')

#Save into folder
    with pd.ExcelWriter(dataset +'.xlsx') as writer:  
      df.to_excel(writer, sheet_name='Data')
      df_meta.to_excel(writer, sheet_name='Metadata')


