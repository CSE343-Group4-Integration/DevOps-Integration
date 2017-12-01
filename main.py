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
  <methodname>createjob</methodname>
  <githubUrl></githubUrl><!--Code&plan-->
  <projectName>deneme5</projectName><!--Code&plan--><!--Build,Deployment-->
  <commitId></commitId><!--Code&plan--><!--Deployment-->
  <targetUrl></targetUrl><!--Code&plan--><!--Build,Test-->
  <buildResult></buildResult><!--Build--><!--Code&plan(fail),Test(Pass)-->
  <buildResultDetail></buildResultDetail><!--Build--><!--Code&Plan(Fail)-->
  <testResult></testResult><!--Test--><!--Deployment(Pass), Code&plan(Fail)-->
  <githubUserid></githubUserid><!--Code-->
  <githubPassport></githubPassport><!--Code-->
  <kartId></kartId><!--Code-->
  <deployResult></deployResult>
</project>'''

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
    methodname=getter(xmlfile,'methodname')
    if methodname=="createjob":
      createJob(str(getter(EMPTY_CONFIG_XML, 'projectName')))
      payload = {
          "id": "1",
          "name": "TestProject",
          "owner": "Group7",
          "method": "create"
      }
      #requests.post("http://localhost:8081/"+"Deployment", data=json.dumps(payload))
    elif methodname=="deletejob":
      deleteJob(str(getter(EMPTY_CONFIG_XML, 'projectName')))
      payload = {
          "id": "1",
          "name": "TestProject",
          "owner": "Group7",
          "method": "delete"
      }
      #requests.post("http://localhost:8081/"+"Deployment", data=json.dumps(payload))
    elif methodname=="build":
    
      #def setConfigXML(projectName,xmlFile,tagName,newTagValue):
      newxml=jenkinsGetSet.setConfigXML(projectname,xmlfile,'buildResult','Waiting-Result')
      newxml=jenkinsGetSet.setConfigXML(projectname,xmlfile,'methodname','build')
      newjson=parser.xml2Json(newxml)
      requests.post("http://localhost:8081/build", data=json.dumps(newjson))

    elif methodname=="check-build-status":
      buildstatus=getter(xmlfile,'buildResult')
      if buildstatus=='TRUE':
        jenkinsGetSet.setConfigXML(projectname,xmlfile,'testResult','Waiting-Result')
        newxml=jenkinsGetSet.setConfigXML(projectname,xmlfile,'methodname','test')
        newjson=parser.xml2Json(newxml)
        requests.post("http://localhost:8081/test", data=json.dumps(newjson))
      else:
        newxml=jenkinsGetSet.setConfigXML(projectname,xmlfile,'methodname','build-status')
        newjson=parser.xml2Json(newxml)
        requests.post("http://localhost:8081/code", data=json.dumps(newjson))
    elif methodname=="check-test-status":
      testResult = getter(xmlfile, 'testResult')
      if testResult == 'TRUE':
        jenkinsGetSet.setConfigXML(projectName, xmlFile, 'methodname', 'deploy')
        newXml = jenkinsGetSet.setConfigXML(projectName, xmlFile, 'deployResult', 'waiting')
        newjson = parser.xml2Json(newxml)      
        request.postRequest(newjson, 'deployment')
      else:
        jenkinsGetSet.setConfigXML(projectName, xmlFile, 'methodname', 'testFailed')
        newXml = jenkinsGetSet.setConfigXML(projectName, xmlFile, 'testResult', 'failed')
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
