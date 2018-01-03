export ATLAS_POOLCOND_PATH="/cvmfs/atlas.cern.ch/repo/conditions"
export LFC_HOST=lfc.usatlas.bnl.gov
export FRONTIER_SERVER="(serverurl=http://frontier.racf.bnl.gov:8000/frontieratbnl)(serverurl=http://lcgft-atlas.gridpp.rl.ac.uk:3128/frontierATLAS)(proxyurl=http://frontier-cache.racf.bnl.gov:3128)"
#export FRONTIER_LOG_LEVEL=warning
export FRONTIER_LOG_LEVEL=debug
export FRONTIER_LOG_FILE=frontier_client.log
#export FRONTIER_READTIMEOUTSECS=60
# allow local override at end
[ -f $OSG_APP/atlas_app/local/setup.sh.local ] && source $OSG_APP/atlas_app/local/setup.sh.local
export VOMS_PROXY_INFO_DONT_VERIFY_AC="true"
