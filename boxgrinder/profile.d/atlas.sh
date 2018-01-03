#
# Setup ATLAS-specific things...
#

if [ -z $DQ2_HOME ]; then
. /cvmfs/atlas.cern.ch/repo/sw/ddm/2.4.0/setup.sh
fi
export VOMS_PROXY_INFO_DONT_VERIFY_AC="true"
export VO_ATLAS_SW_DIR=/cvmfs/atlas.cern.ch/repo/sw
export ATLAS_LOCAL_AREA=/home/osg/app/atlas_app/local
