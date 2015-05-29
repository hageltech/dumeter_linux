#!/bin/sh

rm ../dumeter-reporter_*orig.tar.gz
python setup.py sdist -d ..
rename 's/reporter-(\d+\.\d+).tar/reporter_$1.orig.tar/' ../dumeter-reporter-1.0.tar.gz
debuild -uc -us
cp ../dumeter-reporter*.deb dist

