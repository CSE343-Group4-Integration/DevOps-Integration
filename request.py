#request islemini gerceklestiren method
import  requests
import json
payload = {
	"id": "1",
	"name": "TestProject",
	"owner": "Group7",
	"method": "undeploy"
}

def postRequest(jsonData, group):
	requests.post("http://localhost:8081/"+str(group), data=json.dumps(jsonData))

#postRequest(payload, 'monitor')
