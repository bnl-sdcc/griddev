#!/usr/bin/python

#############################################################################
# Copyright (c) Members of the EGEE Collaboration. 2006.
# See http://www.eu-egee.org/partners/ for details on the copyright
# holders.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Authors:
#     Andrea Ceccanti - andrea.ceccanti@cnaf.infn.it
#############################################################################
import string, getopt, sys, os, os.path, types, traceback

#admin_module_path = os.path.join(os.environ['GLITE_LOCATION'],"share","voms-admin","client")
#sys.path.append(admin_module_path)
sys.path.append("/home/jhover/workspace/voms-admin-client")
#sys.path.append("/opt/ZSI/lib/python2.3/site-packages")

from VOMSAdmin.VOMSCommands import supported_commands,UserCommand,parse_commands,VOMSAdminProxy, print_supported_commands,voms_admin_version,print_version
from VOMSAdmin.VOMSAdminService import VOMSAdmin
from VOMSAdmin import VOMSAdminService_services_types

cmdline_long_options = ["host=",
                        "port=",
                       "url=",
                       "vo=",
                       "version",
                       "verbose",
                       "quiet",
                       "nousercert",
                       "usercert=",
                       "nossl",
                       "ssl",
                       "help",
                       "help-commands"]

options = {}

user_cert = None
user_key = None

def vlog(msg):
    if options.has_key("verbose"):
        print msg
        
def usage():
    usage_str = """
voms-admin v. %s

Usage:
     voms-admin [OPTIONS] --vo=NAME [--host HOST] [--port PORT] COMMAND PARAM...
     voms-admin [OPTIONS] --url=URL COMMAND PARAM...

Options:
     --help              Print this short help message.
     --help-commands     Print a list of available commands, then exit.
     --version           Print version string.

     --verbose       Print more messages.
     
     --nousercert        Don't extract DNs from supplied certificates.
     --usercert FILE     Extract DN parameters from FILE.
     

Service access parameters:
     --vo NAME           Connect to the NAME VO.  (No default.)

     --host HOSTNAME     Use the VOMS Admin service running on HOSTNAME.
                         (Default is localhost.)

     --port PORT         Use the VOMS Admin service running on PORT.
                         (Default is 8080 or 8443 depending on --nossl.)

     --url URL           Connect to the admin service runnig on URL.
                         Example: https://localhost:8443/voms/voname
                         (Overrides --nossl, --host, --port, and --vo.)

Examples:
    voms-admin --vo MyFavouriteVO list-users
        List the users in MyFavouriteVO running on localhost.

    voms-admin --host foobar.cern.ch --vo Foobar list-members /Foobar
        List the members of /Foobar in the Foobar VO running on
        foobar.cern.ch.
    
    For help on commands type voms-admin --help-commands.
""" % (voms_admin_version)
    print usage_str

def setup_identity():
    
    user_id = os.geteuid()
    
    
    if user_id == 0:
        ## we are running as root, use host certificate
        vlog("Running as root")
        options['user_cert'] = "/etc/grid-security/hostcert.pem"
        options['user_key'] = "/etc/grid-security/hostkey.pem"
        
    else:
        ## look for a proxy
        proxy_fname = "/tmp/x509up_u%d" % user_id
        if os.path.exists(proxy_fname):
            vlog("using proxy file found in %s" % proxy_fname)
            options['user_cert'] = proxy_fname
            options['user_key'] = proxy_fname

            
        ## look for a proxy in X509_USER_PROXY env variable
        elif os.environ.has_key("X509_USER_PROXY"):
            vlog("using user credentials found in %s" % os.environ['X509_USER_PROXY'])
            options['user_cert'] = os.environ['X509_USER_PROXY']
            options['user_key'] = os.environ['X509_USER_PROXY']
        
        ## use common certificate    
        elif os.environ.has_key("X509_USER_CERT"):
            vlog("using user X509 certificate")
            options['user_cert'] = os.environ['X509_USER_CERT']
            options['user_key'] = os.environ['X509_USER_KEY']
            
        ## look in the .globus directory
        else:
            vlog("using credentials found in $HOME/.globus...")
            options['user_cert'] = os.path.join(os.environ['HOME'],".globus", "usercert.pem")
            options['user_key'] = os.path.join(os.environ['HOME'],".globus", "userkey.pem")
            
          
def execute_command(cmd):
    
    admin = VOMSAdminProxy(**options)
    if cmd.arg_list is None:
        res = admin.call_method(cmd.name)
    else:
        res = admin.call_method(cmd.name,*cmd.arg_list)
        
    if isinstance(res, types.ListType ):
        for i in res:
            print i
    else:
        if not res is None:
            print res



def check_options():
    
    if options.has_key("help") or options.has_key("h"):
        usage()
        sys.exit(0)
    
    if options.has_key("help-commands"):
        print_supported_commands()
        sys.exit(0)
    
    if options.has_key("version"):
        print_version()
        sys.exit(0)
        
    if not options.has_key("vo"):
        print "No vo specified!"
        sys.exit(1)
    
    if not options.has_key("host"):
        options['host'] = 'localhost'
        
    if not options.has_key("port"):
        options['port'] = 8443
    

def parse_command_line():
    global options
    
    user_commands = []
    opts,args = getopt.getopt(sys.argv[1:],
                              "", 
                              cmdline_long_options)
    for key,val in opts:
            options[key[2:]]=val
    
    check_options()
    
    if len(args) == 0:
        print "No command given!"
        print
        sys.exit(1)
    
    return parse_commands(args, options)
    
    
        
    
def main():

    try:
        setup_identity()    
        user_commands = parse_command_line()
        
        for c in user_commands:
            execute_command(c)
    except RuntimeError, e:
        print e
        sys.exit(-1)


if __name__ == '__main__':
    main()

    