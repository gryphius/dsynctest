Setup
=====

 * Two Dovecot Servers, latest 2.2 hg 
 * Basic Setup: http://wiki2.dovecot.org/Replication
 * `adduser vmail`
 * Server 1's root ssh pubkeys in vmail .ssh/authorized_keys on server 2 and vice-versa. 
 * `mkdir /mailstore`
 * `chown vmail.vmail /mailstore/`

dovecot.conf
------------

(see testenvconfig folder)
be sure to adapt ip in mail_replica

dovecot-sql.conf
----------------
(see testenvconfig folder)
one version for maildir
one version for mdbox

mysql schema
------------

for the tests I didn't use mysql replication on both servers.. just inserted the same data in both databases

	create database doco;
	use doco;
	
	CREATE TABLE `users` (
	  `id` int(11) NOT NULL AUTO_INCREMENT,
	  `username` varchar(255) NOT NULL,
	  `password` varchar(255) NOT NULL,
	  PRIMARY KEY (`id`)
	) ENGINE=MyISAM DEFAULT CHARSET=latin1;
	
	insert into users(username,password) VALUES ('user1','pass1');


