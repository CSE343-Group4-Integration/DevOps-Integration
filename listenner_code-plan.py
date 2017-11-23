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

  <githubUrl>wwww.aaa.com</githubUrl><!--Code&plan-->
  <projectName></projectName><!--Code&plan--><!--Build,Deployment-->
  <commitId></commitId><!--Code&plan--><!--Deployment-->
  <targetUrl></targetUrl><!--Code&plan--><!--Build,Test-->
  <buildResult></buildResult><!--Build--><!--Code&plan(fail),Test(Pass)-->
  <buildResultDetail></buildResultDetail><!--Build--><!--Code&Plan(Fail)-->
  <testResult></testResult><!--Test--><!--Deployment(Pass), Code&plan(Fail)-->
</project>'''


e = xml.etree.ElementTree.fromstring(EMPTY_CONFIG_XML)

for child in e:
    print (child.tag ,": ",child.text)

