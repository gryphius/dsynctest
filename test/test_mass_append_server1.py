#!/usr/bin/python


"""Test: Append messages to box 1 and check if they are synced"""

NUMMESSAGES=3000
MAILBOX="INBOX"
CHECK_INTERVAL=5
MAX_WAIT_SYNC=30


from accountconfig import *
from helpers import *
import time
import sys

imap1=get_imap_connection(SERVER1_HOST, USERNAME, PASSWORD,assertEmpty=True)
imap2=get_imap_connection(SERVER2_HOST, USERNAME, PASSWORD,assertEmpty=True)

print "appending messages..."

#Append messages to server1
counter=0
failcount=0
for message in create_dummy_txt_messages(NUMMESSAGES):
    content=message.as_string()
    #mix flags
    flags=""
    if counter%2==0:
      flags+="\\Seen "
    if counter%3==0:
      flags+="\\Deleted "
    result=imap1.append(MAILBOX,flags,None,content)
    if result[0]!='OK':
      print "Warning, did not get OK result!"
      failcount+=1
    else:
      counter+=1
      
    if counter%10==0:
	r,server1count=imap1.select(MAILBOX)
	server1count=int(server1count[0])
	r,server2count=imap2.select(MAILBOX)
	server2count=int(server2count[0])
        print "%s of %s uploaded, %s failed, server1: %s server2: %s"%(counter,NUMMESSAGES,failcount,server1count,server2count)
        

#Check Message count on server 1
print "Verifying amount on server 1..."
time.sleep(2)
result,messagecount=imap1.select(MAILBOX)
messagecount=int(messagecount[0])
assert messagecount==counter,"Server1: Expected %s messages, got %s"%(counter,messagecount)


#check sync to server 2
now=time.time()
timeout=now+MAX_WAIT_SYNC

while True:
    time.sleep(CHECK_INTERVAL)
    
    result,messagecount=imap2.select(MAILBOX)
    messagecount=int(messagecount[0])
    print "Current messagecount on server 2: %s"%messagecount
    
    if messagecount==counter:
        print "Mailboxes are in sync!"
        break
    
    if time.time()>timeout:
        print "Timeout... server 2 not in sync"
        sys.exit(1)
        

