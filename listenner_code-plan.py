from xml.dom import minidom

EMPTY_CONFIG_XML = '''<?xml version='1.0' encoding='UTF-8'?>
<project>
  <keepDependencies name = "osman">false</keepDependencies>
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
</project>'''

xmldoc = minidom.parseString(EMPTY_CONFIG_XML)
print(xmldoc.nodeName)
print(xmldoc.firstChild.tagName)
value = xmldoc.getElementsByTagName('keepDependencies')
print(value[0])