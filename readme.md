# Solution Overview

There are 3 parts to the Solution
- Queue (a https Server which maintains the Jobs Queue)
- Client (Simple Job Summiting python script)
- Worker (Programmer reposible for executing Jobs)

## what is Pending
- Worker starting the Docker Jobs
- Improvement for the way the Worker Queries for next job & and intimates the Finished Jobs
- Data Valiations
- Concurrency Management in Queue and Worker.

## Execution Process
- First Start Queue:
  Go to queue folder and run 'python app.py'
- Start the workers:
  Go Worker Folder and run
  'python worker.py node1 8 10240'
- Submit Jobs from client:
  Go to client folder and run
  'Python Client.py Sample.json'



