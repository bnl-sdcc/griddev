DISH (Distributed Interactive Shell)

A tool to provide for the simultaneous execution of commands on multiple
hosts. 

User defines groups of homogeneous servers in a cluster.
Executing dish opens connections to each server.
Each command line is passed to all servers and run. 
Output from each is collected and merged and printed back to the user's
console. If all hosts respond equivalently, then the user experience should be just
as if they were logged in to a remote host.  

The --word switch is only useful if all hosts share the same password. If not, you
must have set up key-based authentication. 

