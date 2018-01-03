# Standalone Python client for testing

import sys
import SRM

#print "TESTING SINGLE FILE"
#print SRM.srmGet('srm://castorsrm.cern.ch:8443/', ['srm://castorsrm.cern.ch:8443/castor/cern.ch/grid/atlas/f1'], ['gsiftp'])
#
#print "TESTING BULK SRM GET"
#(reqid, fs) = SRM.srmGet('srm://castorsrm.cern.ch:8443/', ['srm://castorsrm.cern.ch:8443/castor/cern.ch/grid/atlas/f1', 'srm://castorsrm.cern.ch:8443/castor/cern.ch/grid/atlas/f1'], ['gsiftp'])
#print reqid, fs
#
#print "TESTING SRM GET REQUEST STATUS"
#print SRM.srmGetRequestStatus('srm://castorsrm.cern.ch:8443/', reqid)
#
print "TESTING SRM GET FILE METADATA"
print SRM.srmGetFileMetaData('srm://castorsrm.cern.ch:8443', ['srm://castorsrm.cern.ch:8443/castor/cern.ch/grid/atlas/rome.003014.simul.M1_minbias._00001.pool.root'])
