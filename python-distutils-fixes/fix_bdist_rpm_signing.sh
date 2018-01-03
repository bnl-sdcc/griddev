#!/bin/bash
cd /usr/lib64/python2.4/distutils/command/
patch < ~/bdist_sign_rpm_patch.diff
