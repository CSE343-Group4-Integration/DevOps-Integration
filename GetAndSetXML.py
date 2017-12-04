# -*- coding: utf-8 -*-
import jenkins
import jsontoxmlparser as parser


server = jenkins.Jenkins('http://localhost:8080', username='skole', password='1234123121')

def getConfigXML(projectName):
    return server.get_job_config(projectName)

def reConfig(projectName,tagName,newTagValue):
	strconfig = server.get_job_config(projectName)
    strconfig = parser.setter(newTagValue,strconfig,tagName)
    server.reconfig_job(projectName, strconfig)
    return server.get_job_config(projectName)

def reConfigWithXml(projectName,xmlFile):
    server.reconfig_job(projectName, xmlFile)
    return server.get_job_config(projectName)
