import jenkins

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
</project>'''


job_with_github = '''<?xml version='1.0' encoding='UTF-8'?>
<project>
  <keepDependencies>false</keepDependencies>
  
  <properties>
  <com.coravy.hudson.plugins.github.GithubProjectProperty plugin="github@1.28.1">
  <projectUrl>https://github.com/ridvan106/jenkinsDeneme/</projectUrl>
  <displayName></displayName>
    </com.coravy.hudson.plugins.github.GithubProjectProperty>
  </properties>
  <scm class="hudson.plugins.git.GitSCM" plugin="git@3.6.2">
    <configVersion>2</configVersion>
    <userRemoteConfigs>
      <hudson.plugins.git.UserRemoteConfig>
        <url>https://github.com/ridvan106/jenkinsDeneme.git</url>
      </hudson.plugins.git.UserRemoteConfig>
    </userRemoteConfigs>
    <branches>
      <hudson.plugins.git.BranchSpec>
        <name>*/master</name>
      </hudson.plugins.git.BranchSpec>
    </branches>
    <doGenerateSubmoduleConfigurations>false</doGenerateSubmoduleConfigurations>
    <submoduleCfg class="list"/>
    <extensions/>
  </scm>
 
  
  <canRoam>true</canRoam>
  <disabled>false</disabled>
  <blockBuildWhenUpstreamBuilding>false</blockBuildWhenUpstreamBuilding>
  <triggers class='vector'/>
  <concurrentBuild>false</concurrentBuild>
  <builders/>
  <publishers/>
  <buildWrappers/>
</project>'''


JENKINS_USER = 'admin'
JENKINS_PASS = '123456'
JENKINS_URL = 'http://localhost:8080/'

# We need to create a crumb for the request first
server = jenkins.Jenkins(JENKINS_URL,JENKINS_USER,JENKINS_PASS)


#dene = server.build_job("denema")
#print(dene)

k = server.get_running_builds()
print(k)
#server.rename_job("denemee","ridvan")
#server.create_job("denemese",EMPTY_CONFIG_XML)



