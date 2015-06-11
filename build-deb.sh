#!/bin/sh
set -e

rm -f ../dumeter-reporter_*orig.tar.gz
python setup.py sdist -d ..
rename 's/reporter-(\d+\.\d+\.\d+).tar/reporter_$1.orig.tar/' ../dumeter-reporter-1.0.2.tar.gz
debuild -uc -us
cp ../dumeter-reporter*.deb dist
dpkg-sig -k D93DF77B --sign builder dist/*.deb
dpkg-sig --verify dist/*.deb
