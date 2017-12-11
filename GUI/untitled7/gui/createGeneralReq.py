import json
import jenkins
import gui.json_io as js
import xml.etree.ElementTree as ET

tags = ['object_type', 'github_login', 'github_password', 'card_id', 'repository_url', 'project_name', 'method']

server = jenkins.Jenkins('http://localhost:8080', username='mehmet', password='4444')
	
def createGeneralReq(projectName):
	generalReq = '''{  
         "object_type": {"type": "string"},
         "github_login": { "type": "string" },
         "github_password": { "type": "string" },
         "card_id": { "type": "string" },
         "repository_url": { "type": "string" },
         "project_name": { "type": "string" },
         "method": { "type": "string" }
       
	}'''
	configXML = server.get_job_config(projectName)
	e = ET.fromstring(configXML)
	for child in e:
		if(child.tag in tags):
			generalReq = js.json_setter(generalReq, child.tag, child.text)
	return generalReq
