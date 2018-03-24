import json
import requests
import time
import sqlite3

class req():
    def __init__(self, idNum, request = 'ALL'):
        self.postOk = True
        self.idNum = idNum
        self.request = request
        self.tsk_id = ""
    def request_handler(self):
        if self.postOk:        
            url = 'http://iesc-s3.mit.edu/breadboard/humanRequest'
            payload = "dev_id="+str(self.idNum)+"&request="+str(self.request)
            headers = {'Content-Type': "application/x-www-form-urlencoded"}
            r = requests.request("POST", url, data=payload, headers=headers)
            self.tsk_id = r.text
            if self.tsk_id != None:
                self.postOk = False
                return str(self.idNum)+" POST successful. Task ID: "+str(self.tsk_id)
            return str(self.idNum)+" POST unsuccessful."
        else:
            returnStr = ""
##            url = 'http://iesc-s3.mit.edu/breadboard/deviceInquiry?dev_id='+str(self.idNum)
##            r = requests.get(url)
            url = 'http://iesc-s3.mit.edu/breadboard/alldb'
            db = requests.get(url)
            db = db.text
            #get correct tuple in db
            i = db.find(str(self.tsk_id))
            if i == -1:
                self.postOk = True
                returnStr = "Error in POST."
            else:
                openPar = db.rfind("(", 0, i )
                closePar = db.find(")", i)
                tup = db[openPar: closePar+1]
                #tup = tuple(tup)
                tup = eval(tup)
                print(tup)
                #if r.text == "No task or incomplete task":
                if tup[3]==-1:
                    returnStr = "ESP32 #"+str(self.idNum)+" GETing request."
                elif tup[3]==0:
                    returnStr = "ESP32 #"+str(self.idNum)+" processsing request."
                else:
                    returnStr = "ESP32 #"+str(self.idNum)+" response is: "+str(tup[5])
                    diff = float(tup[3])-float(tup[0])
                    returnStr+= "\nProcessing Time (in seconds): "+str(diff)
                    self.postOk = True  
            return returnStr

################
#   main loop
################

test = req(22)
test2 = req(123)
test3 = req(73)
test4 = req(231)
while True:
    print(test.request_handler())
    print("----------------")
    print(test2.request_handler())
    print("----------------")
    print(test3.request_handler())
    print("----------------")
    print(test4.request_handler())
    print("----------------")
    
    time.sleep(1.5)

#bad request handler code
        #task not complete
    ##    r = requests.get("http://iesc-s3.mit.edu/breadboard/humanRequest?dev_id="+str(idNum)+"&request=ALL"
    ##    r = requests.get("http://iesc-s3.mit.edu/breadboard/reportValues")
        #data = r.json()
        # or r.text
        #return data

        ###### pseudo-code

    ##    post to correct site: devid, "ALL" (task type)
    ##    set the status (local?) as false
    ##    while status is still false #or if if we want nonblocking
    ##        do a get on status on correct site
    ##    return status? or result of test?

        ######

    ##    if status=="No task or incomplete task": #or while
    ##        get status
        #incorrect
    ##    data = json.dumps({'dev_id': str(idNum), 'request': 'ALL'})
    ##    headers = {"Content-type": "application/json"}
    ##    r = requests.post('http://iesc-s3.mit.edu/breadboard/humanRequest', headers, data)

