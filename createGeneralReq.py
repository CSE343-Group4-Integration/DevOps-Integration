import json
import jenkins
import json_io as js
import xml.etree.ElementTree as ET

tags = ['object_type', 'github_login', 'github_password', 'card_id', 'repository_url', 'project_name', 'method']

server = jenkins.Jenkins('http://localhost:8080', username='skole', password='1234123121')
	
def creteGeneralReq(projectName):
	generalReq = '''{  "$schema": "http://json-schema.org/draft-04/schema#",
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
       }
	}'''
	configXML = server.get_job_config(projectName)
	e = ET.fromstring(configXML)
	for child in e:
		if(child.tag in tags):
			generalReq = js.json_setter(generalReq, child.tag, child.text)
	return generalReq
