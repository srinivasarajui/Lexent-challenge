from flask import Flask, json, request, jsonify


class JobsService:
  def __init__(self):
    self.pendingJobs =[]
    self.workers = {}
    self.runningJobs = {}
    self.runnerCodeSequence = -1
    self.jobAssignmentNumber = -1
  def addNewJob(self, job):
    self.pendingJobs.append(job)
  def addNewWorker(self, worker):
      self.runnerCodeSequence = self.runnerCodeSequence+1
      self.workers[self.runnerCodeSequence] = worker
      return self.runnerCodeSequence
  def getWorkableJobIndex(self,availableCpu,availableMemory):
      for i in range(len(self.pendingJobs)):
          if (int(self.pendingJobs[i]['requirements']['cpu']) <= availableCpu and int(self.pendingJobs[i]['requirements']['memory']) <= availableMemory):
            return i
      return -1
  def getNextJob(self, resourceDetails, runnerCode):
      availableCpu=int(resourceDetails['cpu'])
      availableMemory=int(resourceDetails['memory'])
      acceptedJobs = {}
      canTakeMoreJobs = True
      while canTakeMoreJobs:
        nextJobIndex = self.getWorkableJobIndex(availableCpu,availableMemory)
        if (nextJobIndex > -1):
            self.jobAssignmentNumber =  self.jobAssignmentNumber + 1
            self.pendingJobs[nextJobIndex]['assignedRuner'] =  runnerCode
            self.runningJobs[self.jobAssignmentNumber] = self.pendingJobs[nextJobIndex]
            acceptedJobs[self.jobAssignmentNumber] = self.pendingJobs[nextJobIndex]
            availableCpu = availableCpu - int(self.pendingJobs[nextJobIndex]['requirements']['cpu'])
            availableMemory = availableMemory - int(self.pendingJobs[nextJobIndex]['requirements']['memory'])
            self.pendingJobs.pop(nextJobIndex)
        else :
            canTakeMoreJobs = False
      return acceptedJobs

app = Flask(__name__)
js = JobsService()

@app.route("/")
def hello():
    return "I am Up and Running";

@app.route("/SubmitJob", methods = [ 'POST'])
def submitNewJob():
    job = request.get_json()
    js.addNewJob(job)
    return "Job Submitted"

@app.route("/RegisterWorker", methods = [ 'POST'])
def registerWorker():
    worker = request.get_json()
    return jsonify(js.addNewWorker(worker));

@app.route("/GetNextJob", methods = [ 'POST'])
def getNextJob():
    details = request.get_json()
    return jsonify(js.getNextJob(details['resourceDetails'],details['runnerCode']));


if __name__ == '__main__':
    app.run(debug=True)

