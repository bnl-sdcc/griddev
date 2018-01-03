Cloudconfig

Utility for early initialization of cloud-based VMs

Features/design principles
-- mostly shell-script based, with easy script-based addition path
-- converts EC2 userdata to filesystem tree/files for usage by scripts.
  -- allows creation of static defaults on pre-existing userdata tree, unifying
  configuration scheme for cloud platforms that do and do not have meta-data services. 
-- intended to stay low-level. sophisticated runtime contextualization can/should still be done with puppet 



VS Cloud-init
VS hepix-context
VS puppet
