"""
This example shows how to add new command to "Shell" build step
"""
#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import xml.etree.ElementTree as ET
import jenkins
import json
import xmltodict
import requests
import parserDeneme as parser
import GetAndSetXML as jenkinsGetSet
import request

EMPTY_CONFIG_XML = '''<?xml version='1.0' encoding='UTF-8'?>
<project>
  <keepDependencies>false</keepDependencies>
  <properties/>
  <scm class='jenkins.scm.NullSCM'/>
  <canRoam>true</canRoam>
  <disabled>false</disabled>
  <blockBuildWhenUpstreamBuilding>false</blockBuildWhenUpstreamBuilding>
  <triggers class='vector'/>
  <concurrentBuild>false</concurrentBuild>
  <builders/>
  <publishers/>
  <buildWrappers/>

  <method_name></method_name>
  <github_login></github_login><!--Code-->
  <github_password></github_password><!--Code-->
  <repository_url></repository_url><!--Code&plan-->
  <project_name></project_name><!--Code&plan--><!--Build,Deployment-->
  <commit_id></commit_id><!--Code&plan--><!--Deployment-->
  <target_url></target_url><!--Code&plan--><!--Build,Test-->
  <card_id></card_id><!--Code-->

  <build_result></build_result><!--Build--><!--Code&plan(fail),Test(Pass)-->
  <build_result_detail></build_result_detail><!--Build--><!--Code&Plan(Fail)-->
  <test_result></test_result><!--Test--><!--Deployment(Pass), Code&plan(Fail)-->
  <test_result_detail></test_result_detail>
  <deploy_result></deploy_result>
  <object_type></object_type>

</project>'''

def setter(text, xmlString, tag):
	e = ET.fromstring(xmlString)
	for child in e:
		if(child.tag == tag):
			child.text = text
			break
	return ET.tostring(e)


def getter(xmlString, tag):
  e = ET.fromstring(xmlString)
  for child in e:
    if(child.tag == tag):
      return child.text

def createJob(project_name):
  server.create_job(project_name,EMPTY_CONFIG_XML)

def deleteJob(project_name):
  server.delete_job(project_name)


def mainFunction(jsonfile):
    xmlfile=parser.Json2Xml(jsonfile)
    methodname=getter(xmlfile,'method_name')

    if methodname=="createjob":
      name=(getter(xmlfile, 'project_name'))
      EMPTY_CONFIG_XML=setter(name,EMPTY_CONFIG_XML,'project_name')
      createJob(name)
      #requests.post("http://localhost:8081/Deployment", data=json.dumps(jsonfile))
    elif methodname=="deletejob":
      name=(getter(xmlfile, 'project_name'))
      EMPTY_CONFIG_XML=setter(name,EMPTY_CONFIG_XML,'project_name')
      deleteJob(name)
      #requests.post("http://localhost:8081/Deployment", data=json.dumps(jsonfile))
      
    elif methodname=="build":
    
      #def setConfigXML(projectName,xmlFile,tagName,newTagValue):
      newxml=jenkinsGetSet.setConfigXML(projectname,xmlfile,'buildResult','waiting)
      newxml=jenkinsGetSet.setConfigXML(projectname,xmlfile,'method_name','build')
      newjson=parser.xml2Json(newxml)
      requests.post("http://localhost:8081/build", data=json.dumps(newjson))

    elif methodname=="check-build-status":
      buildstatus=getter(xmlfile,'build_result')
      if buildstatus=='TRUE':
        jenkinsGetSet.setConfigXML(projectname,xmlfile,'testResult','waiting')
        newxml=jenkinsGetSet.setConfigXML(projectname,xmlfile,'method_name','test')
        newjson=parser.xml2Json(newxml)
        requests.post("http://localhost:8081/test", data=json.dumps(newjson))
      else:
        newxml=jenkinsGetSet.setConfigXML(projectname,xmlfile,'method_name','build-status')
        newjson=parser.xml2Json(newxml)
        requests.post("http://localhost:8081/code", data=json.dumps(newjson))
    elif methodname=="check-test-status":
      testResult = getter(xmlfile, 'test_result')
      if testResult == 'TRUE':
        jenkinsGetSet.setConfigXML(projectName, xmlFile, 'method_name', 'deploy')
        newXml = jenkinsGetSet.setConfigXML(projectName, xmlFile, 'deploy_result', 'waiting')
        newjson = parser.xml2Json(newxml)      
        request.postRequest(newjson, 'deployment')
      else:
        jenkinsGetSet.setConfigXML(projectName, xmlFile, 'method_name', 'testFailed')
        newXml = jenkinsGetSet.setConfigXML(projectName, xmlFile, 'test_result', 'failed')
        newjson = parser.xml2Json(newxml)      
        request.postRequest(newjson, 'code')
    elif methodname=="check-deploy-status":
      print("create")

server = jenkins.Jenkins('http://localhost:8080/', username='admin',password='1234')
mainFunction(parser.xml2Json(EMPTY_CONFIG_XML))
'''
server = jenkins.Jenkins('http://localhost:8080',"mehmet","4444")
my_job = server.get_job_config('denemeapi')
print(my_job)
jsonlast=JsonToXml(XmlToJson(my_job))
print(jsonlast)
'''
# prints XML configuration