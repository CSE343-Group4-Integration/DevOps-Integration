import json
import xmltodict
 
with open('output.json', 'r') as f:
    jsonString = f.read()
 
print('JSON :')
print(jsonString)
 
xmlString = xmltodict.unparse(json.loads(jsonString), pretty=True)
 
print('\nXML output(output.xml):')
print(xmlString)
 
with open('output.xml', 'w') as f:
    f.write(xmlString)