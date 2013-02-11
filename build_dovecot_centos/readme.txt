initial setup:
mkdir /work
cd /work
hg clone http://hg.dovecot.org/dovecot-2.2/


setup initial rpm environment with sources from atrpms:

yum install http://dl.atrpms.net/all/dovecot-2.1.1-2_132.src.rpm

patch the spec for dovecot 2.2



enable core dumps:
add to /etc/sysconfig/init

DAEMON_COREFILE_LIMIT='unlimited'
