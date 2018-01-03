import os
import commands

from django.template import Library, Node, TemplateSyntaxError

register = Library()

global version_info_cached
version_info_cached=None
    

class VersionsNode(Node):
    def __init__(self):
        pass
    
    def render(self, context):
        global version_info_cached
        if version_info_cached:
            #raise TemplateSyntaxError("versions tag does seem to be being called.")
            return version_info_cached
        else:
            allinfo=""
            user = os.environ['USER']
            host = os.environ['HOSTNAME']
            allinfo+="%s@%s, " % (user,host)
            
            (status, output) = commands.getstatusoutput("rpm -q httpd")
            allinfo+="%s, " % output.strip()
            (status, output) = commands.getstatusoutput("rpm -q mod_python")
            allinfo+="%s, " % output.strip()
            (status, output) = commands.getstatusoutput("rpm -q python")
            allinfo+="%s, " % output.strip()
            (status, output) = commands.getstatusoutput("rpm -q Django")
            allinfo+="%s, " % output.strip()
            (status, output) = commands.getstatusoutput("rpm -q R")
            allinfo+="%s, " % output.strip()
            (status, output) = commands.getstatusoutput("rpm -q rpy")
            allinfo+="%s, " % output.strip()    
            (status, output) = commands.getstatusoutput("rpm -q mariachi-data-ws")
            allinfo+="%s." % output.strip()
            version_info_cached=allinfo
            return allinfo


def versions(parser, token):
    '''
    We want
    user@hostname 
    Apache v
    mod_python v
    python v
    django v
    mariachi-data-ws v
    rpy v

    '''
    
    #try:
        # split_contents() knows not to split quoted strings.
    #    tag_name = token.split_contents()
    #except ValueError:
    #    pass
        #raise template.TemplateSyntaxError, "%r tag requires a single argument" % token.contents.split()[0]
    #raise TemplateSyntaxError("versions tag does seem to be being called.")
    return VersionsNode()

versions=register.tag(versions)


        