#!/bin/bash
ldapsearch -x -H ldap://lcg01.usatlas.bnl.gov:2170 -b mds-vo-name=BNL-LCG2,o=grid
