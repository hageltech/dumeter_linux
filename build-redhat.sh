#!/bin/sh

python setup.py sdist -d redhat
mkdir dist
pushd redhat
tar czf dumeter-reporter.tgz *.spec *.service *.tar.gz
rpmbuild -D "_rpmdir `pwd`/../dist" -D "_srcrpmdir `pwd`/../dist" -ta dumeter-reporter.tgz
rm *.tar.gz *.tgz
popd
mv dist/noarch/* dist
rmdir dist/noarch
