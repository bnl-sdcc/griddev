VIHUELA
=======

Vihuela is a generalized Python thread-running framework. 

It provides a plugin architecture and a base class, vihuela.core.Plugin that should
be extended in order to do custom work.


PLUGINS
=======

SystemUpdatePlugin:
------------------
SystemUpdatePlugin can periodically connect to a URL and perform whatever actions are requested
in a script. Scripts should be written to be idempotent, i.e. they can be re-run without ill
effect. 


GridsitePlugin:
--------------
GridsitePlugin that can perform unattended data upload from remote
data acquisition nodes to a central server. Upload occurs to a url exported
by the mod_gridsite module for Apache. This has a few consequences:

1) Must use SSL with grid certificate/proxies.

2) It uses the HTML forms-based upload method as implemented by the mod_gridsite 
management CGI app. This is why we've used the MultipartPostHandler code. 

3) It also needs to deal with proxies and non-proxied connections.

All this means that no pre-existing code/recipes worked exactly as needed out of 
box. There is also the issue that urllib2 does not handle SSL client certificates even though 
the underlying httplib does (provided the Python socket module was compiled with SSL). 

DummyPlugin:
------------
Included for testing core plugin architecture. Does nothing.
  