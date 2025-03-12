import json
ijson = open('tab.json','r').read()
jsonData = json.loads(ijson)
try:
    print(jsonData['Minecraft'])
except KeyError:
    jsonData['Minecraft']=0
    print(jsonData['Minecraft'])