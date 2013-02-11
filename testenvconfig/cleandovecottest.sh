#!/bin/sh

# stop dovecot 
service dovecot stop
sleep 3
# kill hanging dsync jobs
killall dsync
killall ssh

# clear mailstore for the next test
cd /mailstore
rm -Rf user1 user2 user3


echo "All done - remember to select the correct dovecot-sql.conf for the next test and start dovecot."


