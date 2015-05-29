#!/bin/sh
set -e

python setup.py sdist -d redhat
mkdir -p dist
pushd redhat
tar czf dumeter-reporter.tgz *.spec *.service *.tar.gz
rpmbuild -D "_rpmdir `pwd`/../dist" -D "_srcrpmdir `pwd`/../dist" -tb dumeter-reporter.tgz
rm *.tar.gz *.tgz
popd
mv dist/noarch/* dist
rmdir dist/noarch
rpmsign --resign dist/*.rpm
