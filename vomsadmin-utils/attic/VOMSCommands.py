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

import xml.dom.minidom, string, re, sys
from VOMSAdminService import VOMSAdmin
from VOMSAttributesService import VOMSAttributes
from X509Helper import X509Helper
from VOMSCommandsDef import commands_def

voms_admin_version = "2.0.3-1"

def command_argument_factory(type):
    
    if type == "X509":
        return X509Argument()
    elif type == "User":
        return UserArgument()
    elif type == "Group":
        return GroupArgument()
    elif type == "Role":
        return RoleArgument()
    elif type == "String":
        return StringArgument()
    elif type == "Boolean":
        return BooleanArgument()
    else:
        raise RuntimeError, "Argument type unknown!"
 
class CommandArgument:
    def __init__(self):
        self.value = None
        self.missing_arg_msg = "Missing argument!"
        self.nillable = False
        
    def parse(self, cmd, args, options):
        
        self.check_length(cmd, args, 1)
        val = args.pop(0)
        return [val]
    
    def check_length(self, cmd, args, min_length):
                   
        if len(args) < min_length:
            raise RuntimeError, self.missing_arg_msg
        
        for i in args[:min_length]:
            if i in supported_commands.keys():
                raise RuntimeError, "Found command '%s' while parsing arguments for command!" % cmd.name
        

class StringArgument(CommandArgument):
    def __init__(self):
        self.missing_arg_msg = "Missing string argument!"

class BooleanArgument(CommandArgument):
    def __init__(self):
        self.missing_arg_msg = "Missing boolean argument!"
    
    def parse(self, cmd, args, options):
        self.check_length(cmd, args, 1)
        bool = args.pop(0)
        ret_val = False
        if bool == '0' or bool == 'false' or bool == 'False' or bool == 'FALSE':
            ret_val = False
        elif bool == '1' or bool == 'true' or bool == 'True' or bool == 'TRUE':
            ret_val = True
        
        return [ret_val]
        

class X509Argument(CommandArgument):
    def __init__(self):
        self.missing_arg_msg = "Missing X509 cert argument!"
    
    def parse(self, cmd, args, options):
        
        if options.has_key("nousercert"):
            self.check_length(cmd, args, 4)
            dn = args.pop(0)
            ca = args.pop(0)
            cn = args.pop(0)
            mail = args.pop(0)
        
            return [dn,ca,cn,mail]
        else:
            
            self.check_length(cmd=cmd, args=args, min_length=1)
            cert = X509Helper(args.pop(0))
            
            return [cert.subject,cert.issuer,None,cert.email]
        
    
class UserArgument(CommandArgument):
    def __init__(self):
        self.missing_arg_msg = "Missing user argument!"
        
    def parse(self, cmd, args, options):
        
        if options.has_key("usercert"):
            cert = X509Helper(options['usercert'])
            return [cert.subject,cert.issuer]
        else:
            self.missing_arg_msg = "Please specify DN and CA for the user!"
            self.check_length(cmd, args, 2)
            
            dn = args.pop(0)
            ca = args.pop(0)
        
        return [dn,ca]

class GroupArgument(CommandArgument):
    def __init__(self):
        self.missing_arg_msg = "Missing group argument!"
    
    def parse(self,cmd,args, options):
        self.check_length(cmd, args, 1)
        group = args.pop(0)
        if group.strip() == "VO":
            return ["/"+options['vo']]
        else:
            return [group]
    
class RoleArgument(CommandArgument):
    def __init__(self):
        self.missing_arg_msg = "Missing role argument!"
    
    def parse(self, cmd, args, options):
        self.check_length(cmd, args, 1)
        role = args.pop(0)
        if not role.strip().startswith("Role="):
            return ["Role="+role]
        else:
            return [role]
        
class Command:
    def __init__(self, name, desc=None, help_str=None):
        self.name = name
        self.desc = desc
        self.arg_types = []
        self.help_str = help_str

    def add_arg(self,arg):
        self.arg_types.append(arg)
    
    def num_args(self):
        return len(self.arg_types)
    
    def __repr__(self):

        return "%s(%s)" % (self.name,
                              ",".join([e.__class__.__name__ for e in self.arg_types]))
                          

class UserCommand(Command):
    def __init__(self,cmd, arg_list=[]):
        Command.__init__(self, cmd.name, cmd.desc, cmd.help_str)
        self.arg_types = cmd.arg_types
        self.arg_list = arg_list

    def parse_args(self,cmd_line, options=None):
        
        for i in self.arg_types:
            self.arg_list= self.arg_list + i.parse(cmd=self,args=cmd_line,options=options)
        
    def help(self):
        return "Usage:\n%s\n\t%s\n" % (self.desc, self.help_str)

def _parse_commands():
    
    def get_text(nodelist):
        text = ""
        for node in nodelist:
            if node.nodeType == node.TEXT_NODE:
                text = text + node.data
        return text
    
    command_hash = {}
    
    doc = xml.dom.minidom.parseString(commands_def)
    
    for c in doc.getElementsByTagName("command"):
        
        num_args = 0
        
        cmd_name = c.getAttribute("name")     
        cmd = Command(name=cmd_name)
               
        for child in c.childNodes:
            if child.nodeType == child.ELEMENT_NODE:
                if child.nodeName == "description":
                    cmd.desc = get_text(child.childNodes).strip()
                elif child.nodeName == "help-string":
                    cmd.help_str = get_text(child.childNodes)
                elif child.nodeName == "arg":
                    _arg = command_argument_factory(child.getAttribute("type"))
                    cmd.add_arg(_arg)

        command_hash[cmd.name]= cmd
    
    return command_hash

supported_commands = _parse_commands()

def print_version():  
    print "voms-admin v.", voms_admin_version
    
def print_supported_commands():
    print "Supported commands and usage info:"
    print
    for v in supported_commands.values():
        print v.desc
        print "\t", v.help_str


def parse_commands(args, options):
    commands = []
   
    while len(args)>0:
        
        cmd = args.pop(0).strip()
        if not supported_commands.has_key(cmd):
            
            print "Unknown command: %s" % cmd
            # print_supported_commands()
            sys.exit(1)
                
        usr_cmd = UserCommand(supported_commands[cmd])
        usr_cmd.parse_args(args, options)
        
        commands.append(usr_cmd)
    
    return commands

class VOMSAdminProxy:
    def __init__(self,*args, **kw):
        self.base_url = "https://%s:%d/voms/%s/services" % (kw['host'],
                                                            int(kw['port']),
                                                            kw['vo'])
        transdict = {
                     "cert_file":kw['user_cert'], 
                     "key_file":kw['user_key']
                     }
        
        self.admin = VOMSAdmin(url=self.base_url+"/VOMSAdmin",
                               transdict=transdict)
        
        self.attributes = VOMSAttributes(url=self.base_url+"/VOMSAttributes",
                                         transdict=transdict)
    
    
    def transname(self, method_name):
        def f(m):
            return m.group(2).upper()
        
        return re.sub("(-(.))",f,method_name)
    
    
    def call_method(self, method_name, *args, **kw):
        mn = self.transname(method_name)
        
        if self.__class__.__dict__.has_key(mn):
            return self.__class__.__dict__[mn](self,*args,**kw)
        
        else:
            if not self.admin.__class__.__dict__.has_key(mn):
                
                if not self.attributes.__class__.__dict__.has_key(mn):
                    raise RuntimeError, "Unknown method '%s'!" %mn
                else:
                    return self.attributes.__class__.__dict__[mn](self.attributes,*args,**kw)
            
            else:
                return self.admin.__class__.__dict__[mn](self.admin,*args,**kw)
    
        
    def listUsers(self):
        users = self.admin.listUsers()
        if users is None:
            return "No users found in vo!"
        
        return users
    
    def listMembers(self,group):
        members = self.admin.listMembers(group)
        if members is None:
            return "No members found in group %s" % group
        else:
            return members
            
    
            
            
           

    
    