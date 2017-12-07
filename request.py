#request islemini gerceklestiren method
import  requests

def postRequest(jsonData, group):
	requests.post("http://localhost:8081/"+str(group), data=jsonData)
