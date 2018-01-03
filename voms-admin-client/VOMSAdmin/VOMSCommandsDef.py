commands_def="""<?xml version="1.0" encoding="UTF-8"?>
<voms-commands>
    <command
        name="get-vo-name">
        <description>
            get-vo-name            
        </description>
        <help-string>
            This command returns the name of the contacted vo.
        </help-string>
    </command>
    
    <command
        name="list-users" 
        >
        <description>
            list-users 
        </description>
        <help-string>
            Lists the VO users.
        </help-string>
    </command>
    
    <command
        name="create-user" 
        >
        <description>
            create-user CERTIFICATE.PEM
        </description>
        <help-string>
            Registers a new user in VOMS. If you use the --nousercert option,
            then four parameters are required (DN CA CN MAIL) to create the
            user. Otherwise these parameters are extracted automatically from
            the certificate.
        </help-string>
        
        <arg type="X509"/>
    </command>
    
    <command
        name="delete-user" 
        >
        <description>
            delete-user USER
        </description>
        <help-string>
            Deletes a user from VOMS, including all their attributes and
            membership information.
        </help-string>
        
        <arg type="User"/>
        
    </command>
    
    <command
        name="list-cas">
        <description>
            list-cas
        </description>
        <help-string>
            Lists the certificate authorities accepted by the VO.
        </help-string>
    </command>
    
    <command
        name="list-roles">
        <description>
            list-roles
        </description>
        <help-string>
            Lists the roles defined in the VO.
        </help-string>
    </command>
    
    <command
        name="create-role">
        <description>
            create-role ROLENAME
        </description>

        <help-string>
            Creates a new role
        </help-string>
        
        <arg type="Role"/>
    </command>
    
    <command
        name="delete-role">
        <description>
            delete-role ROLENAME
        </description>

        <help-string>
            Deletes a role.
        </help-string>
        
        <arg type="Role"/>
        
    </command>
    
    <command
        name="list-groups">
        <description>
            list-groups
        </description>
        <help-string>
            Lists all the groups defined in the VO.
        </help-string>
    </command>
    
    <command
        name="list-sub-groups">
        <description>
            list-sub-groups GROUPNAME
        </description>
        <help-string>
            List the subgroups of GROUPNAME.
        </help-string>
        
        <arg type="Group"/>
    </command>
    
    <command
        name="create-group">
        <description>
            create-group GROUPNAME
        </description>

        <help-string>    
            Creates a new group named GROUPNAME. Note that the vo root group
            part of the fully qualified group name can be omitted, i.e., if the
            group to be created is called /vo/ciccio, where /vo is the vo root
            group, this command accepts both the "ciccio" and "/vo/ciccio"
            syntaxes.
        </help-string>
        <arg type="Group"/>
    </command>
    
    <command
        name="delete-group">
        <description>
            delete-group GROUPNAME
        </description>

        <help-string>
            Deletes a group.
        </help-string>
        <arg type="Group"/>
    </command>
    
    <command
        name="add-member" 
        >
        <description>
            add-member GROUPNAME USER
        </description>

        <help-string>
            Adds USER to the GROUPNAME group. If the --nouser option is set USER
            is expressed as DN CA.
        </help-string>
        
        <arg type="Group"/>
        <arg type="User"/>
        
    </command>
    
    <command
        name="remove-member" 
        >
        <description>
            remove-member GROUPNAME USER
        </description>

        <help-string>
            Removes USER from the GROUPNAME group. If the --nouser option is set USER
            is expressed as DN CA.
        </help-string>
        
        <arg type="Group"/>
        <arg type="User"/>
    </command>
    
    <command
        name="list-members">
        <description>
            list-members GROUPNAME
        </description>
            
        <help-string>
            Lists all members of a group.
        </help-string>
        
        <arg type="Group"/>
    </command>
    
    <command
        name="assign-role">
        <description>
            assign-role GROUPNAME ROLENAME USER
        </description>
        <help-string>
            Assigns role ROLENAME to user USER in group GROUPNAME. If the --nouser option is set USER
            is expressed as DN CA.
        </help-string>
        
        <arg type="Group"/>
        <arg type="Role"/>
        <arg type="User"/>
    </command>
    
    <command
        name="dismiss-role">
        <description>
            dismiss-role GROUPNAME ROLENAME USER
        </description>
        <help-string>
            Dismiss role ROLENAME from user USER in group GROUPNAME.If the --nouser option is set USER
            is expressed as DN CA.
        </help-string>
        
        <arg type="Group"/>
        <arg type="Role"/>
        <arg type="User"/>
    </command>
    
    <command
        name="list-users-with-role">
        <description>
            list-users-with-role GROUPNAME ROLENAME 
        </description>
        <help-string>
             Lists all users with ROLENAME in GROUPNAME.
        </help-string>
        
        <arg type="Group"/>
        <arg type="Role"/>
        
    </command>
    
    <command
        name="list-user-groups">
        <description>
            list-user-groups USER
        </description>
        <help-string>
            Lists the groups that USER is a member of. If the --nouser option is set USER
            is expressed as DN CA.
        </help-string>
        
        <arg type="User"/>
    </command>
    
    <command
        name="list-user-roles">
        <description>
            list-user-roles USER
        </description>
        <help-string>
            Lists the roles that USER is assigned. If the --nouser option is set USER
            is expressed as DN CA.
        </help-string>
        
        <arg type="User"/>
    </command>
    
    <command
        name="create-attribute-class">
        <description>
            create-attribute-class CLASSNAME DESCRIPTION UNIQUE
        </description>
        
        <help-string>
            Creates a new generic attribute class named CLASSNAME,
            with description DESCRIPTION. UNIQUE is a boolean argument.
            If UNIQUE is true, attribute values assigned to users for this class 
            are checked for uniqueness. Otherwise no checks are performed
            on user attribute values.
        </help-string>
        
        <arg type="String"/>
        <arg type="String" nillable="true"/>
        <arg type="Boolean" nillable="true"/>
    </command>
    
    <command
        name="delete-attribute-class">
        <description>
            delete-attribute-class CLASSNAME
        </description>
        
        <help-string>
            Removes the generic attribute class CLASSNAME.
            All the user, group and role attribute mappings will be deleted
            as well.
        </help-string>
        
        <arg type="String"/>
    </command>
    
    <command
        name="list-attribute-classes">
        <description>
            list-attribute-classes
        </description>
        
        <help-string>
            Lists the attribute classes defined for the VO.

        </help-string>
    </command>
    
    <command
        name="set-user-attribute">
        <description>
            set-user-attribute USER ATTRIBUTE ATTRIBUTE_VALUE
        </description>
        
        <help-string>
            Sets the generic attribute ATTRIBUTE value to ATTRIBUTE_VALUE for
            user USER.
        </help-string>
        
        <arg type="User"/>
        <arg type="String"/>
        <arg type="String"/>
    </command>
    
    <command
        name="delete-user-attribute">
        <description>
            delete-user-attribute USER ATTRIBUTE 
        </description>
        
        <help-string>
            Deletes the generic attribute ATTRIBUTE value from
            user USER.
        </help-string>
        
        <arg type="User"/>
        <arg type="String"/>
    </command>
    
    <command
        name="list-user-attributes">
        <description>
            list-user-attributes USER
        </description>
        
        <help-string>
            Lists the generic attributes defined for user USER.

        </help-string>
        
        <arg type="User"/>
    </command>
    
    <command
        name="set-group-attribute">
        <description>
            set-group-attribute GROUP ATTRIBUTE ATTRIBUTE_VALUE
        </description>
        
        <help-string>
            Sets the generic attribute ATTRIBUTE value to ATTRIBUTE_VALUE for
            group GROUP.
        </help-string>
        
        <arg type="Group"/>
        <arg type="String"/>
        <arg type="String"/>
    </command>
    
    <command
        name="set-role-attribute">
        <description>
            set-role-attribute GROUP ROLE ATTRIBUTE ATTRIBUTE_VALUE
        </description>
        
        <help-string>
            Sets the generic attribute ATTRIBUTE value to ATTRIBUTE_VALUE for
            role ROLE in group GROUP.
        </help-string>
        
        <arg type="Group"/>
        <arg type="Role"/>
        <arg type="String"/>
        <arg type="String"/>
    </command>
    
    <command
        name="delete-group-attribute">
        <description>
            delete-group-attribute GROUP ATTRIBUTE
        </description>
        
        <help-string>
            Deletes the generic attribute ATTRIBUTE value from
            group GROUP.
        </help-string>
        
        <arg type="Group"/>
        <arg type="String"/>
    </command>
    
    <command
        name="list-group-attributes">
        <description>
            list-group-attributes GROUP
        </description>
        
        <help-string>
            Lists the generic attributes defined for group GROUP.

        </help-string>
        
        <arg type="Group"/>
    </command>

    <command
        name="list-role-attributes">
        <description>
            list-role-attributes GROUP ROLE
        </description>
        
        <help-string>
            Lists the generic attributes defined for role ROLE in 
            group GROUP.
        </help-string>
        
        <arg type="Group"/>
        <arg type="Role"/>
    </command>
    
    <command
        name="delete-role-attribute">
        <description>
            delete-role-attribute GROUP ROLE ATTRIBUTE
        </description>
        
        <help-string>
            Deletes the generic attribute ATTRIBUTE value from
            role ROLE in group GROUP.
        </help-string>
        
        <arg type="Group"/>
        <arg type="Role"/>
        <arg type="String"/>
    </command>
</voms-commands>
"""