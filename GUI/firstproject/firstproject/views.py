# -*- coding: utf-8 -*-
from django.http import *
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
  <githubUrl>wwww.aaa.com</githubUrl><!--Code&plan-->
  <projectName></projectName><!--Code&plan--><!--Build,Deployment-->
  <commitId></commitId><!--Code&plan--><!--Deployment-->
  <targetUrl></targetUrl><!--Code&plan--><!--Build,Test-->
  <buildResult>waiting</buildResult><!--Build--><!--Code&plan(fail),Test(Pass)-->
  <buildResultDetail></buildResultDetail><!--Build--><!--Code&Plan(Fail)-->
  <testResult></testResult><!--Test--><!--Deployment(Pass), Code&plan(Fail)-->
  <deployResult></deployResult>
</project>'''
def merhaba_django(request):
    server =jenkins.Jenkins('http://localhost:8080/',username='admin',password='123456')

    #server.create_job('deneme7',EMPTY_CONFIG_XML)
    k = server._get_view_jobs('all')
    print(k)
    css ="<style type=text/css>th,td{" \
         "border-bottom: 1px solid #ddd; \
         padding: 15px;\
        text-align: left;}" \
         "tr:hover {background-color: #f5f5f5;}" \
        "th{background-color: #4CAF50;\
        color: white;}"\
        "img{" \
         "display: block;" \
         "margin: auto;"\
         "}"\
        "caption{" \
         "color:#369;"\
         "font-family: Arial, sans-serif;" \
         "font-size: 24px;" \
         "padding-bottom: 4px;"\
         "}"\
        "</style>"
    http=css+"<table border=0 align= center>" \
            "<caption style=text-align:right>Integration</caption>"\
         "<tr><th> Praject Name</th>" \
         "<th> Build </th>" \
         "<th> Test </th>" \
         "<th> Deploy</th>" \
         "<th> Build Et</th>"\
         "</tr>"
    oks = "<img width=50 src=https://cdn4.iconfinder.com/data/icons/evil-icons-user-interface/64/check-128.png>"
    no ="<img width=55 src=https://cdn4.iconfinder.com/data/icons/evil-icons-user-interface/64/close2-128.png>"
    nothing ="<img width=40 src=https://cdn4.iconfinder.com/data/icons/mayssam/512/forbidden-128.png>"
    waiting ="<img width=40 src=https://cdn2.iconfinder.com/data/icons/bitsies/128/Clock-128.png>"
    for val in k:
        xmlFile = server.get_job_config(val['name'])
        print(xmlFile)
        e = xml.etree.ElementTree.fromstring(xmlFile)
        build = ""
        test = ""
        deploy = ""
        for child in e.iter(tag='buildResult'):
            build  = child.text
            if(build == "false"):
                build = no
            elif(build == "true"):
                build = oks
            elif(build == "waiting"):
                build = waiting   
            else:
                build=nothing
        for child in e.iter(tag='testResult'):
            test = child.text
            if (test == "false"):
                test = no
            elif (test == "true"):
                test = oks
            elif(test == "waiting"):
                test = waiting      
            else:
                test= nothing
        for child in e.iter(tag='deployResult'):
            deploy = child.text
            if (deploy == "false"):
                deploy = no
            elif (deploy == "true"):
                deploy = oks
            elif(deploy == "waiting"):
                deploy = waiting      
            else:
                deploy= nothing
        http += '<tr><td>'+val['name'] +'</td><td>'+ build +'</td><td>'+ test +'</td><td>'+ deploy +'</td><td>'+\
                "<img width=50 src=https://cdn3.iconfinder.com/data/icons/tango-icon-library/48/system-software-update-128.png >"+'</td></tr>'
    http +='</table>'

    return HttpResponse(http)
