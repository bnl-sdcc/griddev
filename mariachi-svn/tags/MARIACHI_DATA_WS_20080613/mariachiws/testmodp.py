def test(req):
    return "OK"


def status(req):
    from mod_python import Session 
    from mod_python import util 
    from mod_python import psp 
    from mod_python import apache 
    from mariachi import modpystatus 

    req.content_type="text/html" 
    req.add_common_vars() 
    r=modpystatus.modPyStats() 
    r.status(req) 
    req.write(r.page) 
    return apache.OK
    