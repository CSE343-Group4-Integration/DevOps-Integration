from django.shortcuts import render
from django.shortcuts import HttpResponse
# Create your views here.
# -*- coding: utf-8 -*-
from django.http import *
import jenkins
import  xml.etree.ElementTree
import json
from django.test import TestCase, RequestFactory
import gui.createGeneralReq as createReq

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
def index(request):
    server =jenkins.Jenkins('http://localhost:8080/',username='mehmet',password='4444')

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
                "<a href=/rebuild/?projectname=" +val['name'] +'>' + '<img width=50 src=https://cdn3.iconfinder.com/data/icons/tango-icon-library/48/system-software-update-128.png ></a></td></tr>'
    http +='</table>'

    return HttpResponse(http)


TEST_JSON_RES = ''' {
         "object_type": "tmp",
         "operation": "tmp",
         "status": "TRUE",
         "description": "tmp",
         "project_name": "deneme",
         "method" : "build"

}'''
def rebuild_post(request):
    projectname=request.GET["projectname"]
    jsonfile=createReq.createGeneralReq(projectname)
    data = json.loads(jsonfile)
    data["method"]="build"
    req = RequestFactory()
    req.post("http://localhost:8081/build",data)
    return index(request)
