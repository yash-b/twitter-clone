import hug
import threading
import requests
import time
from typing import List

serviceDict = {}

def healthCheck():
    while True:
        for key,value in serviceDict.items():
            if not "healthCheckPath" in key:
                for urlString in value:
                    healthCheckUrl = urlString + serviceDict[key+"healthCheckPath"]
                    response = requests.get(url = healthCheckUrl)
                    currentStatusCode = response.status_code
                    if currentStatusCode!=200:
                        removeFromRegistry(key)
                        break
        time.sleep(15)

def updateRegistry(key, value, remove=False):
    with threading.Lock():
        if remove:
            del serviceDict[key]
        else:
            serviceDict[key] = value

def removeFromRegistry(serviceName):
    updateRegistry(serviceName, [], True)

def doAddToServiceRegistry(serviceName: str, urls: List[str], healthcheckPath: str):
    serverUrlsList = []
    for serverurl in urls:
        serverUrlsList.append(serverurl)
    updateRegistry(serviceName, serverUrlsList)
    updateRegistry(str(serviceName)+"healthCheckPath", healthcheckPath)

@hug.startup()
def onStart(api):
    doAddToServiceRegistry("serviceregistry", ["http://localhost:5300"], "/service/serviceregistry")
    serviceHealthCheckThread = threading.Thread(target=healthCheck, args="", daemon=True)
    serviceHealthCheckThread.start()

@hug.post("/addservice")
def addToServiceRegistry(serviceName: hug.types.text, urls: hug.types.delimited_list(','), healthcheckPath:hug.types.text):
    doAddToServiceRegistry(serviceName, urls, healthcheckPath)

@hug.get("/service/{servicename}")
def getServiceUrl(servicename: hug.types.text):
    with threading.Lock():
        return serviceDict[servicename]
    
