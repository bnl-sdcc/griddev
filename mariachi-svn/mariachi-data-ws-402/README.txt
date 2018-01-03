Mariachi Data WS
----------------
Code providing web-based access to mariachi data. 

Dependencies:
----------------
httpd,  	(Apache Web server)
mod_python  (Python from within Apache)
Django      (web service framework)
rpy         ( Python R wrapper)
pytz        (ISO time handling)
shntool     (wav file utility)
PyXML        (utils.iso8601 is now in this package)

Use these URLs to test...
-------------------------
http://localhost:33380/mariachi-ws/testmodp/status
http://localhost:33380/mariachi-ws/dataquery/status

Raw query interface
--------------------
http://localhost:33380/mariachi-ws/dataquery/query

Django Data Retrieval Page
--------------------------
http://localhost:33380/mariachi-ws/django/dataquery/

http://localhost:33380/python/testmodp/dbquery?database=foo&table=bar


Conversion to Django
---------------------------

Data selection forms

Site:

From:   Year Month Day Hour Minute (default 1 day ago)
To:     Year Month Day Hour Minute (default now) 
Show:   [Counts Table| Events Table | Everything | Counts Graph]

