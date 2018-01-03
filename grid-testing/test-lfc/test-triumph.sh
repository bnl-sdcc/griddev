#!/bin/bash
. /opt/glite/etc/profile.d/grid-env.sh
echo voms-proxy-init -voms atlas
voms-proxy-init -voms atlas
echo voms-proxy-info -all
voms-proxy-info -all
echo export LFC_HOST=lfc.triumf.ca
export LFC_HOST=lfc.triumf.ca
echo lcg-la --vo atlas guid:c6401aee-8398-44bc-9298-8c44eeda454b
lcg-la --vo atlas guid:c6401aee-8398-44bc-9298-8c44eeda454b
