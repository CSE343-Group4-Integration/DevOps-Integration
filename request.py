#request islemini gerceklestiren method
import  requests
import json

def postRequest(jsonData, group):
	requests.post("http://localhost:8081/"+str(group), data=json.dumps(jsonData))

