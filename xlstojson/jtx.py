import pandas as pd
import json

jsonFile = open('tab_231124.json','r').read()
xlsFile = pd.read_excel('table_231124.xlsx')
jsonData = json.loads(jsonFile)
#xlsFile = xlsFile.append({'tags':'1','rank':'2'},ignore_index=True)

for iterator in jsonData:
    #print(type(iterator))
    xlsFile = xlsFile.append({'tags':iterator,'rank':jsonData[iterator]},ignore_index=True)
    print('tags: ',iterator,' rank:',jsonData[iterator])
xlsFile.to_excel('tab_231124.xlsx')
#print(xlsFile)
#xlsFile = xlsFile.T