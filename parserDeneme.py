import xmltodict
import jenkins
import json

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

  <githubUrl></githubUrl><!--Code&plan-->
  <projectName></projectName><!--Code&plan--><!--Build,Deployment-->
  <commitId></commitId><!--Code&plan--><!--Deployment-->
  <targetUrl></targetUrl><!--Code&plan--><!--Build,Test-->
  <buildResult></buildResult><!--Build--><!--Code&plan(fail),Test(Pass)-->
  <buildResultDetail></buildResultDetail><!--Build--><!--Code&Plan(Fail)-->
  <testResult></testResult><!--Test--><!--Deployment(Pass), Code&plan(Fail)-->
  <deployResult></deployResult>
</project>'''

JENKINS_USER = 'skole'
JENKINS_PASS = '1234123121'
JENKINS_URL = 'http://localhost:8080/'

def xml2Json(inpXml):
   jsonString = json.dumps(xmltodict.parse(inpXml), indent=4)
   return jsonString


def Json2Xml(inpJson):
    xmlString = xmltodict.unparse({'root': json.loads(inpJson)}, pretty=True)
    return xmlString


# We need to create a crumb for the request first
#server = jenkins.Jenkins(JENKINS_URL,JENKINS_USER,JENKINS_PASS)


#print(Json2Xml(xml2Json(EMPTY_CONFIG_XML)))
