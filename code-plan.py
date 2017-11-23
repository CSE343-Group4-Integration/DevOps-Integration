import jenkins
import  xml.etree.ElementTree
from xml.dom import minidom


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

  <githubUrl>https://github.com/ridvan106/jenkinsDeneme</githubUrl><!--Code&plan-->
  <projectName>aa</projectName><!--Code&plan--><!--Build,Deployment-->
  <commitId></commitId><!--Code&plan--><!--Deployment-->
  <targetUrl></targetUrl><!--Code&plan--><!--Build,Test-->
  <buildResult></buildResult><!--Build--><!--Code&plan(fail),Test(Pass)-->
  <buildResultDetail></buildResultDetail><!--Build--><!--Code&Plan(Fail)-->
  <testResult></testResult><!--Test--><!--Deployment(Pass), Code&plan(Fail)-->
</project>'''


def parser(xmel,list):
    e = xml.etree.ElementTree.fromstring(xmel)
    for child in e:
        if(child.tag == 'projectName'):
            list.insert(0,child.text)

        if (child.tag == 'githubUrl'):
            list.insert(1,child.text)



def createJob(list):

    server.create_job(list[0],EMPTY_CONFIG_XML)
def deleteJob(list):
    server.delete_job(list[0])



liste=[]
server = jenkins.Jenkins('http://localhost:8080/', username='admin',password='123456')
parser(EMPTY_CONFIG_XML,liste)
#createJob(liste)
#deleteJob(liste)
print(liste)