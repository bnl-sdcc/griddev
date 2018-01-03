Vihuela
===================

Vihuela is a generalized Python thread-running framework. 

This is a script, with libs, to perform unattended data upload from remote
data acquisition nodes to a central server. Upload occurs to a url exported
by the mod_gridsite module for Apache. This has a few consequences:

1) Must use SSL with grid certificate/proxies.

2) It uses the HTML forms-based upload method as implemented by the mod_gridsite 
management CGI app. This is why we've used the MultipartPostHandler code. 

3) It also needs to deal with proxies and non-proxied connections.

All this means that no pre-existing code/recipes worked exactly as needed out of 
box. There is also the issue that urllib2 does not handle SSL client certificates even though 
the underlying httplib does (provided the Python socket module was compiled with SSL). 

  