import json
import xmltodict
 
with open("empty_project.xml", 'r') as f:
    xmlString = f.read()
 
print("XML :")
print(xmlString)
     
jsonString = json.dumps(xmltodict.parse(xmlString), indent=4)
 
print("\nJSON output(output.json):")
print(jsonString)
 
with open("output.json", 'w') as f:
    f.write(jsonString)