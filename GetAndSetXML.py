# -*- coding: utf-8 -*-
import jenkins
import jsontoxmlparser as parser

'''
create_job(name, config_xml)
Create a new Jenkins job

Parameters:	
name – Name of Jenkins job, str
config_xml – config file text, str

/////////////////////////////////////////

get_job_config(name)
Get configuration of existing Jenkins job.

Parameters:	name – Name of Jenkins job, str
Returns:	job configuration (XML format)

/////////////////////////////////////////

reconfig_job(name, config_xml)
Change configuration of existing Jenkins job.

To create a new job, see Jenkins.create_job().

Parameters:	
name – Name of Jenkins job, str
config_xml – New XML configuration, str

/////////////////////////////////////////

get_node_config(name)
Get the configuration for a node.

Parameters:	name – Jenkins node name, str

/////////////////////////////////////////

reconfig_node(name, config_xml)
Change the configuration for an existing node.

Parameters:	
name – Jenkins node name, str
config_xml – New XML configuration, str

/////////////////////////////////////////
'''


server = jenkins.Jenkins('http://localhost:8080', username='skole', password='1234123121')

def getConfigXML(projectName):
    return server.get_job_config(projectName)

def setConfigXML(projectName,xmlFile,tagName,newTagValue):
    str = parser.setter(newTagValue,xmlFile,tagName)
    server.reconfig_job(projectName, str)
    return server.get_job_config(projectName)

def setChangedConfigXML(projectName,xmlFile):
    server.reconfig_job(projectName, xmlFile)
    return server.get_job_config(projectName)


#server.create_job('testJob', jenkins.EMPTY_CONFIG_XML)