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
        "projectName": null,
        "commitId": null,
        "targetUrl": null,
        "buildResult": null,
        "buildResultDetail": null,
        "testResult": null
    }
}'''

xmlString = xmltodict.unparse(json.loads(jsonString), pretty=True)

e = ET.fromstring(xmlString)

#Parametreler:
#text = yazacagimiz string
#eltree = xmli cektigimiz elementTree
#tag = xml tagi
def setter(text, eltree, tag):
	for child in e:
		if(child.tag == tag):
			child.text = text
			tree.write('empty_project.xml')
			break

#Parametreler:
#eltree = xmli cektigimiz elementTree
#tag = xml tagi
def getter(eltree, tag):
	for child in e:
		if(child.tag == tag):
			return child.text

def getProjectName(eltree):
	return getter(eltree, "projectName")
	
def getBuildResult(eltree):
	return getter(eltree, "buildResult")
	
def getBuildResultDetail(eltree):
	return getter(eltree, "buildResultDetail")
	
def getTargetUrl(eltree):
	return getter(eltree, "targetUrl")

def setBuildResult(text, eltree):
	setter(text, eltree, "buildResult")

def setBuildResultDetail(text, eltree):
	setter(text, eltree, "buildResultDetail")
	
for child in e:
	print(child.tag, " ", child.text)	 
