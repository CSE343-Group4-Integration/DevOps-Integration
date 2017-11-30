import  requests
import json
payload = {
	"id": "1",
	"name": "TestProject",
	"owner": "Group7",
	"method": "undeploy"
}
requests.post("http://localhost:8081/monitor", data=json.dumps(payload))
