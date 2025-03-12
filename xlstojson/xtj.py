import pandas as pd
import json
import os

data = pd.read_excel('tab_get.xlsx')
jsFile = open('tab_new.json',"w")
arr = {}
i = 0

for interator in data['tags']:
    arr[interator]=str(data['rank'][i])
    #arr.append(item)
    #print(item)
    i+=1

datajson = json.dumps(arr)
jsFile.write(datajson)
jsFile.flush()