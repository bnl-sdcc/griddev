# == Class: htcondor
#
# Full description of class htcondor here.
#
# === Parameters
#
# Document parameters here.
#
# [*is_submit*]
# If machine is a schedd
#
# [*is_manager*]
# If machine is a central manager and negotiator 
#
# [*is_execute*]
# If the machine is a startd
#
# 
# === Authors
#
# John Hover <jhover@bnl.gov>
#
# === Copyright
#
# Copyright 2015 John Hover, unless otherwise noted.
#
# 
#

class htcondor ( $is_execute               = false,
	             $is_submit                = false,
	             $is_manager               = false,
	             $use_password_auth        = true,
	             $use_gsi_auth             = false,
	             $condor_password          = 'changeme',
	             $collector_host           = $::fqdn,
	             $collector_port           = 9618,
	             $randomize_collector_port = false,
                 $collector_port_low       = 29661,
	             $collector_port_high      = 29680,
	             $local_dir                = '/home/condor',
	             $use_jobwrapper           = true,
	             $use_slotusers            = true,
	             $use_dedicated_scheduler  = false,
	             $dedicated_scheduler      = $::fqdn
	             
	            ) {
    $major_release = $::operatingsystemmajrelease
   
	yumrepo { 'htcondor-stable':
	    descr    => "HTCondor Stable RPM Repository for Redhat Enterprise Linux ${major_release}",
		baseurl  => "http://research.cs.wisc.edu/htcondor/yum/stable/rhel${major_release}",
		enabled  => 1,
		gpgcheck => 0,
		exclude  => 'condor.i386, condor.i686',
		before => [Package['condor']],
	}

    package {'condor':
        ensure => installed,
    }

    file { ['/etc/condor', '/etc/condor/config.d']:
        ensure  => directory,
        owner   => 'root',
        group   => 'root',
        recurse => true,
    }    

          
    file {'/etc/condor/condor_config.local':
        ensure  => file,
        owner   => 'root',
        content => epp('htcondor/condor_config.local.epp'),
        notify  => Service["condor"], 
    }

    file {'/etc/condor/config.d/30master.config':
        ensure  => file,
        owner   => 'root',
        content => epp('htcondor/30master.config.epp'),
        notify  => Service["condor"],  
    }

    if $is_execute {
        notify { 'This host will be an execute node.': withpath => true }    
        
        file { [ "${local_dir}" , "${local_dir}/execute" ]:
            ensure  => directory,
            owner   => 'condor',
            group   => 'condor',
            recurse => true,
        }    
                    
        file {'/etc/condor/config.d/50startd.config':
            ensure  => file,
            owner   => 'root',
            content => epp('htcondor/50startd.config.epp'),
            notify  => Service["condor"],  
        }
        
        file {'/etc/condor/config.d/51startd_job.config':
            ensure  => file,
            owner   => 'root',
            content => epp('htcondor/51startd_job.config.epp'),
            notify  => Service["condor"],  
        }
        
        file {'/etc/condor/config.d/53startd_partslots.config':
            ensure  => file,
            owner   => 'root',
            content => epp('htcondor/53startd_partslots.config.epp'),
            notify  => Service["condor"],  
        }
        
        if $use_slotusers {
            
            user {["slot1","slot2","slot3","slot4","slot5", "slot6","slot7","slot8", "slot9", "slot10",
                "slot11","slot12","slot13","slot14","slot15", "slot16","slot17","slot18", "slot19", "slot20",
                "slot21","slot22","slot23","slot24","slot25", "slot26","slot27","slot28", "slot29", "slot30",
                "slot31","slot32" ] :
                ensure     => "present",
                managehome => true,
                }
        }
        
        if $use_jobwrapper {
            file {'/usr/libexec/jobwrapper.sh':
                ensure => file,
                owner => 'root',
                mode  => '0555',
                source => "puppet:///modules/htcondor/jobwrapper.sh"
            }
        }
    }
    

    if $is_manager {    
    
        file {'/etc/condor/config.d/40cm.config':
            ensure  => file,
            owner   => 'root',
            content => epp('htcondor/40cm.config.epp'), 
            notify  => Service["condor"], 
        }         
        file {'/etc/condor/config.d/45cm_depthfirst.config':
            ensure  => file,
            owner   => 'root',
            content => epp('htcondor/45cm_depthfirst.config.epp'),
            notify  => Service["condor"],  
        }

    }
          

    if $is_submit {
        notify { 'This host will (also) be a submit node.': withpath => true }          
    
        file {'/etc/condor/config.d/60schedd.config':
            ensure  => file,
            owner   => 'root',
            content => epp('htcondor/60schedd.config.epp'),
            notify  => Service["condor"],  
        }
    }    
    
    if $use_password_auth {
        notify { 'Using password authentication.': withpath => true }    
    
        file {'/usr/bin/make_condor_password':
            ensure => file,
            owner => 'root',
            mode  => '0555',
            source => "puppet:///modules/htcondor/make_condor_password"
        }
        
        file {'/etc/condor/condor_password':
            ensure  => file,
            owner   => 'root',
            mode  => '0600',
            content => epp('htcondor/condor_password.epp'), 
            notify => [
                Exec['make_condor_password'],
                Service["condor"],
                    ]
            }
           
        file {'/etc/condor/config.d/70sec_password.config':
            ensure  => file,
            owner   => 'root',
            content => epp('htcondor/70sec_password.config.epp'),
            notify  => Service["condor"],  
        }
        
        exec { "make_condor_password":
            command => "make_condor_password",
            path    => "/usr/local/bin/:/bin/:/usr/sbin:/usr/bin",
            # path    => [ "/usr/local/bin/", "/bin/"],  # alternative syntax
        }
    }
   
    file {'/etc/condor/config.d/72network.config':
            ensure  => file,
            owner   => 'root',
            content => epp('htcondor/72network.config.epp'),
            notify  => Service["condor"],  
    }
    
    if $randomize_collector_port {
        # sets collector port to random (but host stable) number between high and low. 
        $set_collector_port = fqdn_rand( $collector_port_high - $collector_port_low ) + $collector_port_low
        notify { "Collector port randomized to ${set_collector_port}" : withpath => true }
    }
    else {
        $set_collector_port = $collector_port
        notify { "Collector port is ${set_collector_port}": withpath => true }
    }
    
    file {'/etc/condor/config.d/80collector.config':
            ensure  => file,
            owner   => 'root',
            content => epp('htcondor/80collector.config.epp'), 
            notify  => Service["condor"], 
        }  
        
    file {'/etc/condor/config.d/90logdebug.config':
        ensure  => file,
        owner   => 'root',
        content => epp('htcondor/90logdebug.config.epp'), 
        notify  => Service["condor"], 
    }
    
    if $::ec2_instance_id != undef { 
        file {'/etc/condor/config.d/92ec2attributes.config':
            ensure  => file,
            owner   => 'root',
            content => epp('htcondor/92ec2attributes.config.epp'), 
            notify  => Service["condor"], 
        }
    }
 
	service {'condor':
			ensure    => running,
			enable    => true,
    }
}
