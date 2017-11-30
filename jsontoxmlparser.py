import  xml.etree.ElementTree as ET
from xml.dom import minidom
import json
import xmltodict

jsonString = '''{
    "project": {
        "keepDependencies": "false",
        "properties": null,
        "scm": {
            "@class": "jenkins.scm.NullSCM"
        },
        "canRoam": "true",
        "disabled": "false",
        "blockBuildWhenUpstreamBuilding": "false",
        "triggers": {
            "@class": "vector"
        },
        "concurrentBuild": "false",
        "builders": null,
        "publishers": null,
        "buildWrappers": null,
        "githubUrl": null,
        "projectName": "asdasd",
        "commitId": null,
        "targetUrl": null,
        "buildResult": null,
        "buildResultDetail": null,
        "testResult": null
    }
}'''

def jsontoxml(jsonString):
	return xmltodict.unparse(json.loads(jsonString), pretty=True)
	
def xmltojson(xmlString):
	return json.dumps(xmltodict.parse(EMPTY_CONFIG_XML), indent=4)

#Parametreler:
#text = yazacagimiz string
#eltree = xmli cektigimiz elementTree
#tag = xml tagi
def setter(text, xmlString, tag):
	e = ET.fromstring(xmlString)
	for child in e:
		if(child.tag == tag):
			child.text = text
			break
	return ET.tostring(e)

#Parametreler:
#eltree = xmli cektigimiz elementTree
#tag = xml tagi
def getter(xmlString, tag):
	e = ET.fromstring(xmlString)
	for child in e:
		if(child.tag == tag):
			return child.text

xmlString = jsontoxml(jsonString)

