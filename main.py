"""
This example shows how to add new command to "Shell" build step
"""
# !/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import xml.etree.ElementTree as ET
import jenkins
import parserDeneme as parser
import GetAndSetXML as jenkinsGetSet
import request
# !/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

import xml.etree.ElementTree as ET
import json
import jenkins
import xmltodict
import GetAndSetXML as jenkinsGetSet
import parserDeneme as parser
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
  <deploy_result_detail></deploy_result_detail>
  <object_type></object_type>

</project>'''

TEST_JSON_REQ = '''{  "$schema": "http://json-schema.org/draft-04/schema#",
       "title": "Request information",
       "type": "object",
       "description": "Information necessary to access project sources on github repository and method to be applied",
       "properties": {
         "object_type": {"type": "string"},
         "github_login": { "type": "string" },
         "github_password": { "type": "string" },
         "card_id": { "type": "string" },
         "repository_url": { "type": "string" },
         "project_name": { "type": "string" },
         "method": { "type": "string" }
       },
       "required": [ "object_type", "github_login","github_password", "repository_url", "project_name", "method" ]
}
'''


def setter(text, xml_string, tag):
	e = ET.fromstring(xml_string)
	for child in e:
		if(child.tag == tag):
			child.text = text
			break
	return ET.tostring(e)


def getter(xml_string, tag):
  e = ET.fromstring(xml_string)
  for child in e:
    if(child.tag == tag):
      return child.text

def create_job(project_name):
  server.create_job(project_name,EMPTY_CONFIG_XML)

def delete_job(project_name):
  server.delete_job(project_name)


def main_function(json_file):
    xml_file=parser.Json2Xml(json_file)
    print('-----------')
    print(xml_file)
    method_name = getter(xml_file,'method_name')
    global EMPTY_CONFIG_XML
    if method_name== "create_job":
      project_name = getter(xml_file, 'project_name')
      card_id = getter(xml_file, 'card_id')
      github_login = getter(xml_file, 'github_login')
      github_password = getter(xml_file, 'github_password')
      repository_url = getter(xml_file, 'repository_url')
      target_url = getter(xml_file, 'target_url')
      commit_id = getter(xml_file, 'commit_id')

      EMPTY_CONFIG_XML = setter(project_name, EMPTY_CONFIG_XML, 'project_name')
      EMPTY_CONFIG_XML = setter(card_id, EMPTY_CONFIG_XML, 'card_id')
      EMPTY_CONFIG_XML = setter(github_login, EMPTY_CONFIG_XML, 'github_login')
      EMPTY_CONFIG_XML = setter(github_password, EMPTY_CONFIG_XML, 'github_password')
      EMPTY_CONFIG_XML = setter(repository_url, EMPTY_CONFIG_XML, 'repository_url')
      EMPTY_CONFIG_XML = setter(target_url, EMPTY_CONFIG_XML, 'target_url')
      EMPTY_CONFIG_XML = setter(commit_id, EMPTY_CONFIG_XML, 'commit_id')

      create_job(project_name)
      request.postRequest(json_file, 'deployment')

    elif method_name == "delete_job":
      name = getter(xml_file, 'project_name')
      EMPTY_CONFIG_XML = setter(name,EMPTY_CONFIG_XML,'project_name')
      delete_job(name)
      request.postRequest(json_file, 'deployment')

    elif method_name=="build":
      new_xml = jenkinsGetSet.setConfigXML(project_name,xml_file,'build_result','waiting')
      new_xml = jenkinsGetSet.setConfigXML(project_name,xml_file,'method_name','build')
      new_json = parser.xml2Json(new_xml)
      request.postRequest(new_json, 'build')

    elif method_name == "check-build-status":
      build_status = getter(xml_file,'build_result')
      if build_status == 'TRUE':
        jenkinsGetSet.setConfigXML(project_name,xml_file,'test_result','waiting')
        new_xml = jenkinsGetSet.setConfigXML(project_name,xml_file,'method_name','test')
        new_json = parser.xml2Json(new_xml)
        request.postRequest(new_json, 'test')
      else:
        new_xml = jenkinsGetSet.setConfigXML(project_name,xml_file,'method_name','build-status')
        new_json = parser.xml2Json(new_xml)
        request.postRequest(new_json, 'code')
    elif method_name == "check-test-status":
      testResult = getter(xml_file, 'test_result')
      if testResult == 'TRUE':
        jenkinsGetSet.reconfig(project_name, 'method_name', 'deploy')
        jenkinsGetSet.reConfig(project_name, 'test_result', 'true')
        jenkinsGetSet.reConfig(project_name, 'deploy_result', 'waiting')
        request_json = createGeneralRequest(project_name)
        request.postRequest(request_json, 'deployment')
      else:
        jenkinsGetSet.reConfig(project_name, 'method_name', 'test_failed')
        jenkinsGetSet.reConfig(project_name, 'test_result', 'false')
        request_json = createGeneralRequest(project_name)
        request.postRequest(request_json, 'code')
    elif method_name == "check-deploy-status":
      deploy_result = getter(xml_file, 'deploy_result')
      if deploy_result == 'TRUE':
        jenkinsGetSet.setConfigXML(project_name, xml_file, 'method_name', 'complete')
        jenkinsGetSet.setConfigXML(project_name, xml_file, 'deploy_result', 'true')
      else:
        jenkinsGetSet.setConfigXML(project_name, xml_file, 'method_name', 'deploy_failed')
        new_xml = jenkinsGetSet.setConfigXML(project_name, xml_file, 'deploy_result', 'false')
        new_json = parser.xml2Json(new_xml)
        request.postRequest(new_json, 'code')

server = jenkins.Jenkins('http://localhost:8080/', username='skole',password='1234123121')
#main_function(parser.xml2Json(EMPTY_CONFIG_XML))

# prints XML configuration


main_function(TEST_JSON_REQ)
#print(parser.Json2Xml(TEST_JSON_REQ))