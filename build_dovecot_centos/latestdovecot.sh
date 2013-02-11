#!/bin/sh
cd dovecot-2.2
hg pull
hg update
./autogen.sh
cd ..
tar -cvzf dovecot-2.2.tar.gz dovecot-2.2
mv dovecot-2.2.tar.gz ~/rpmbuild/SOURCES/ -f
cd ~/rpmbuild/SPECS/
rpmbuild -bb --without systemd dovecot.spec 
