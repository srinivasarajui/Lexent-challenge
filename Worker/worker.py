import sys
import requests
import json
import time
import random
import threading
baseURL = 'http://127.0.0.1:5000/'
headers = {'Content-Type': 'application/json'}

def registerWorker(name,cpu,memory):
  requestJSON = {'WorkerName': name,  'cpu': cpu,'memory':memory }
  response = requests.post('{0}RegisterWorker'.format(baseURL), headers=headers, json=requestJSON)
  return int(response.content)

def getNextJob(code,cpu,memory):
  requestJSON = {'runnerCode': code, 'resourceDetails': { 'cpu': cpu,'memory':memory }}
  response = requests.post('{0}GetNextJob'.format(baseURL), headers=headers, json=requestJSON)
  return response.json()

class ProcessThread (threading.Thread):
   def __init__(self, id,  JobInfo):
      threading.Thread.__init__(self)
      self.id = id
      self.JobInfo = JobInfo
   def run(self):
      print ("Starting " + self.id)
      time.sleep(random.randint(1,11)) # Docker Code Goes here
      print ("Exiting " + self.id)


class WorkerService:
    def __init__(self,name,cpu,memory):
      self.name = name
      self.totalCpu = cpu
      self.totalMemory = memory
      self.code=registerWorker(name,cpu,memory)
      self.freeCpu = cpu
      self.freeMemory = memory
    def startService(self):
       while True:
        jobs = getNextJob(self.code,self.freeCpu,self.freeMemory)
        threads = []
        if(len(jobs.items()) < 1):
             print('Waiting for next job')
             time.sleep(6) # wait for some time
        for id, details in jobs.items():
              thread = ProcessThread(id,details)
              threads += [thread]
              thread.start()
        for thread in threads:
              thread.join()

if __name__ == '__main__':
    if(len(sys.argv) < 4):
        sys.exit("use python worker.py name cpucount memeorysize")
    name = sys.argv[1]
    cpu = sys.argv[2]
    memory = sys.argv[3]
    ws =  WorkerService(name,cpu,memory)
    ws.startService();
