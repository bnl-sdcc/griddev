#!/usr/bin/python
#
# Author: Stephen Childs <Stephen.Childs@cs.tcd.ie>
# Edits:
#    John Hover <jhover@bnl.gov> 
#
import commands
import time

# First list is of Condor's job states, second is of the states used by the
# lrmsinfo spec. lrmsinfo list is accessed directly, I've left them both
# in to show the mapping.
condorJobStates=['Unexpanded','Idle','Running','Removed','Completed','Held','Submission_err']
lrmsinfoJobStates=['queued','queued','running','done','done','pending','done']

# Get the current time
now=int(time.time())

# Get the status of pool nodes using condor_status
(status,output)=commands.getstatusoutput('condor_status -format "%s\n" State')

if status == 0 and len(output) > 0 :
    condor_states=output.split('\n')

    freq={}
    for state in ['Owner','Claimed','Unclaimed','Matched']:
	freq[state]=condor_states.count(state)
    total_nodes=len(condor_states)

    # number of nodes available to run jobs is the number of 
    # nodes up and unused by their owner
    nactive=total_nodes-freq['Owner']
    print "nactive\t\t%s" %(nactive)

    # number of free nodes is the number of active nodes
    # minus the number of claimed nodes
    nfree=freq['Unclaimed']
    print "nfree\t\t%s" %(nfree)

    # now is the number of seconds since start of epoch
    print "now\t\t%s" %(now)

    # schedCycle is NEGOTIATOR_INTERVAL? Can it be queried using 
    # condor_config_val? Hard-coded to 300 for now.
    # Note : condor_config_val returns non-zero status if variable is not set
    # and getstatusoutput returns non-zero if command not in path

    schedCycle=300
    (status,output)=commands.getstatusoutput('condor_config_val NEGOTIATOR_INTERVAL')
    if status == 0 :
        schedCycle= int(output)
    print "schedCycle\t%d" %(schedCycle)

# Get the info we need about jobs from condor_q

(status,output)=commands.getstatusoutput('condor_q -format "%.1f," JobStartDate -format "%d," JobStatus -format "%s," Owner -format "%.1f," QDate -format "%s\n" GlobalJobId')

if status == 0 and len(output) > 0 :
   # Break up into individual jobs
   job_list=output.split('\n')

   # Process each job
   for job in job_list:
       job=job.split(',')
       # If the job hasn't started yet, there will be no start time.
       if len(job) == 5:
           (start,state,user,qtime,jobid)=job 
       elif len(job) == 4:
           (state,user,qtime,jobid)=job
           start='no'

       # get user's group
       getusergroup=commands.getstatusoutput("id -gn %s" % user)
       if (getusergroup[0] == 0):
           group=getusergroup[1]
       else:
           group="error"

       # set CPU count (not sure how to get this in Condor)
       cpucount="1"

       jobDescr= "{"

       state=int(state)
       if (start != 'no'):
           jobDescr+="'start': '%s', " %start
       jobDescr+="'queue': 'condor', 'state': '%s', 'cpucount': '%s', 'group': '%s', 'user': '%s', 'maxwalltime': '240.0', 'qtime': '%s', 'jobid': '%s'}" %(lrmsinfoJobStates[state], cpucount, group, user, qtime, jobid)
       print jobDescr
