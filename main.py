"""
This example shows how to add new command to "Shell" build step
"""

from __future__ import print_function

import json
import xml.etree.ElementTree as ET

import jenkins
import xmltodict

import GetAndSetXML as jenkinsGetSet
import json_io as jsonGetSet
import request
import createGeneralReq as createGeneralReq

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
         "object_type": "tmp",
         "github_login": "tmp",
         "github_password": "tmp",
         "card_id": "tmp",
         "repository_url": "tmp",
         "project_name": "sondeneme",
         "method_name": "build"
       }
}
'''
TEST_JSON_RES = '''{  "$schema": "http://json-schema.org/draft-04/schema#",
       "title": "Response information",
       "type": "object",
       "description": "Contains operation(method) and its execution status with description",
       "properties": {
         "object_type": "tmp",
         "operation": "tmp",
         "status": "FALSE",
         "description": "tmp",
         "project_name": "sondeneme",
         "method_name" : "check-deploy-status"
       }
}'''

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
    method_name = jsonGetSet.json_getter(json_file,'method_name')
    project_name = jsonGetSet.json_getter(json_file, 'project_name')
    global EMPTY_CONFIG_XML
    if method_name== "create_job":
      project_name = jsonGetSet.json_getter(json_file, 'project_name')
      card_id = jsonGetSet.json_getter(json_file, 'card_id')
      github_login = jsonGetSet.json_getter(json_file, 'github_login')
      github_password = jsonGetSet.json_getter(json_file, 'github_password')
      repository_url = jsonGetSet.json_getter(json_file, 'repository_url')
      target_url = jsonGetSet.json_getter(json_file, 'target_url')
      commit_id = jsonGetSet.json_getter(json_file, 'commit_id')

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
      name = jsonGetSet.json_getter(json_file, 'project_name')
      delete_job(name)
      request.postRequest(json_file, 'deployment')
   
    elif method_name=="build":
      print(jenkinsGetSet.reConfig(project_name,'build_result','waiting'))
      new_json = createGeneralReq.createGeneralReq(project_name)
      new_json = jsonGetSet.json_setter(new_json,'method_name','build')
      request.postRequest(new_json, 'build')
    elif method_name == "check-build-status":
      build_status = jsonGetSet.json_getter(json_file,'status')
      if build_status == 'TRUE':
        jenkinsGetSet.reConfig(project_name,'build_result','true')
        jenkinsGetSet.reConfig(project_name,'test_result','waiting')
        new_json = createGeneralReq.createGeneralReq(project_name)
        new_json = jsonGetSet.json_setter(new_json,'method_name','test')
        request.postRequest(new_json, 'test')
      else:
        jenkinsGetSet.reConfig(project_name,'build_result','false')
        response_json=jsonGetSet.json_setter(json_file,'method_name','build-status')
        request.postRequest(response_json, 'code')
    elif method_name == "check-test-status":
      testResult = jsonGetSet.json_getter(json_file,'status')
      if testResult == 'TRUE':
        jenkinsGetSet.reConfig(project_name, 'method_name', 'deploy')
        jenkinsGetSet.reConfig(project_name, 'test_result', 'true')
        jenkinsGetSet.reConfig(project_name, 'deploy_result', 'waiting')
        request_json = createGeneralReq.createGeneralReq(project_name)
        request.postRequest(request_json, 'deployment')
      else:
        jenkinsGetSet.reConfig(project_name, 'method_name', 'test_failed')
        jenkinsGetSet.reConfig(project_name, 'test_result', 'false')
        request.postRequest(json_file, 'code')
    elif method_name == 'check-deploy-status':
      deploy_result = jsonGetSet.json_getter(json_file, 'status')
      if deploy_result == 'TRUE':
        jenkinsGetSet.reConfig(project_name, 'method_name', 'complete')
        jenkinsGetSet.reConfig(project_name, 'deploy_result', 'true')
      else:
        jenkinsGetSet.reConfig(project_name, 'method_name', 'deploy_failed')
        jenkinsGetSet.reConfig(project_name, 'deploy_result', 'false')
        request_json = createGeneralReq.createGeneralReq(project_name)
        request.postRequest(json_file, 'code')

server = jenkins.Jenkins('http://localhost:8080/', username='skole',password='1234123121')
#main_function(parser.xml2Json(EMPTY_CONFIG_XML))

# prints XML configuration


main_function(TEST_JSON_RES)
#print(parser.Json2Xml(TEST_JSON_REQ))
print(server.get_job_config('sondeneme'))