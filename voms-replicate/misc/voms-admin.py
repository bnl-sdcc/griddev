#!/usr/bin/env python

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
import string, getopt, sys, os, os.path, types

admin_module_path = os.path.join(os.environ['GLITE_LOCATION'],"share","voms-admin","client")
sys.path.append(admin_module_path)

from VOMSAdmin.VOMSCommands import supported_commands,UserCommand,parse_commands, \
VOMSAdminProxy, print_supported_commands,voms_admin_version,print_version, \
print_command_help,print_supported_commands_help

from VOMSAdmin.VOMSAdminService import VOMSAdmin
from VOMSAdmin import VOMSAdminService_services_types

cmdline_long_options = ["host=",
                        "port=",
                       "vo=",
                       "version",
                       "verbose",
                       "quiet",
                       "nousercert",
                       "ssl",
                       "help",
                       "help-acl",
                       "help-commands",
                       "list-commands",
                       "help-command="]

options = {}

user_cert = None
user_key = None

def vlog(msg):
    if options.has_key("verbose"):
        print msg

def help_acl():
    
    help_acl_str = """
VOMS Admin AuthZ Framework
---------------------------

In VOMS-Admin, each operation that access the VOMS database is authorized via the VOMS-Admin Authorization framework. 
For instance, only authorized admins have the rights to add users or create groups for a specific VO. 
More specifically, Access Control Lists (ACLs) are linked to VOMS contexts to enforce authorization decisions on such contexts. 
In this framework, a Context is either a VOMS group, or a VOMS role within a group. 
Each Context as an ACL, which is a set of ACL  entries, i.e., (VOMS Administrator, VOMSPermission) couples.

A VOMS Administrator may be:
    A VO administrator registered in the VO VOMS database;
    A VO user;
    A VOMS FQAN;
    Any authenticated user (i.e., any user who presents a  certificate issued by a trusted CA).
    
A VOMS Permission is a fixed-length sequence of permission flags that describe the set of permissions a VOMS Administrator has in a specific context. 

The following table explains in detail the name and meaning of these permission flags:

CONTAINER_READ,CONTAINER_WRITE: These flags are used to control access to the operations 
that list/alter the VO internal structure (groups and roles list/creations/deletions, 
user creations/deletions).

MEMBERSHIP_READ,MEMBERSHIP_WRITE: These flags are used to control access to operations that manage/list membership in group and roles.

ATTRIBUTES_READ,ATTRIBUTES_WRITE: These flags are used to control access to operations that manage generic attributes 
(at the user, group, or role level).

ACL_READ,ACL_WRITE,ACL_DEFAULT: These flags are used to control access to operations that manage VO ACLs and default ACLs.

REQUESTS_READ,REQUESTS_WRITE: These flags are used to control access to operations that manage subscription requests regarding the vo, 
group membership etc...

Each operation on the VOMS database is authorized according to the above set of permissions, 
i.e., whenever an administrator tries to execute such operation, its permissions are matched 
with the operation's set of required permission in order to authorize the operation execution. 

ACL INHERITANCE AND DEFAULT ACLs
--------------------------------

Children groups, at creation time, inherit parent's group ACL. 
However, VOMS Admin implements an override mechanims for this behaviour via Default ACLs. 
When the Default ACL is defined for a group, children groups inherit the Default ACL defined 
at the parent level instead of the parent's group ACL. 
So, Default ACLs are useful only if an administrator wants the ACL of children groups to be different 
from the one of the parent's group.

For more detailed information regarding VOMS Operations and required permissions consult
the VOMS Admin user's guide and the help of the ACL management commands.
"""
    print help_acl_str
    
def usage():
    usage_str = """
voms-admin v. %s

Usage:
     voms-admin [OPTIONS] --vo=NAME [--host HOST] [--port PORT] COMMAND PARAM...

Options:
     --help              Print this short help message.
         
     --list-commands     Print a list of available commands.
     --help-command CMD  Print help about command CMD. 
     
     --help-commands     Print help for all available commands.
     
     --version           Print version string.

     --verbose       Print more messages.
     
     --nousercert        Don't extract DNs from supplied certificates.
     

Service access parameters:
     --vo NAME           Connect to the NAME VO.  (No default.)

     --host HOSTNAME     Use the VOMS Admin service running on HOSTNAME.
                         (Default is localhost.)

                         (Default is 8443.)
     --port PORT         Use the VOMS Admin service running on PORT.

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
    
    if options.has_key("help-acl"):
        help_acl()
        sys.exit(0)
        
    if options.has_key("list-commands"):
        print_supported_commands()
        sys.exit(0)
        
    
    if options.has_key("help-commands"):
        print_supported_commands_help()
        sys.exit(0)
        
    if options.has_key("help-command"):
        print_command_help(options['help-command'])
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
    
    try:
        
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
    
    except getopt.GetoptError, e:
        print "Error parsing command line arguments:", e
        sys.exit(1)
    
        
    
    
    
        
    
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

    