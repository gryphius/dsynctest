#!/usr/bin/python


"""Test: Append messages to box 1 and check if they are synced"""

NUMMESSAGES=3000
MAILBOX="Trash"
CHECK_INTERVAL=5
MAX_WAIT_SYNC=30


from accountconfig import *
from helpers import *
import time
import sys

imap1=get_imap_connection(SERVER1_HOST, USERNAME, PASSWORD, initialmailbox=MAILBOX, assertEmpty=True)

print "appending 'deleted' messages..."

#Append messages to server1
counter=0
for message in create_dummy_txt_messages(NUMMESSAGES):
    content=message.as_string()
    result,info=imap1.append(MAILBOX,"\\Deleted",None,content)
    if result!='OK':
      print "Warning: append failed: %s - %s"%(result,info[0])
    else:
      counter+=1
    if counter%10==0:
        print "%s/%s"%(counter,NUMMESSAGES)
        

#Check Message count on server 1
print "Verifying amount on server 1..."
time.sleep(2)
result,messagecount=imap1.select(MAILBOX)
messagecount=int(messagecount[0])
assert messagecount==counter,"Server1: Expected %s messages, got %s"%(counter,messagecount)

print "Expunging..."
result,explist=imap1.expunge()
assert result=='OK',"expunge failed"
assert len(explist)==counter,"expected %s expunged messages, got %s"%(counter,len(explist))


#check sync to server 2
imap2=get_imap_connection(SERVER2_HOST, USERNAME, PASSWORD, initialmailbox=MAILBOX, assertEmpty=False)
now=time.time()
timeout=now+MAX_WAIT_SYNC

while True:
    time.sleep(CHECK_INTERVAL)
    
    result,messagecount=imap2.select()
    messagecount=int(messagecount[0])
    print "Current messagecount on server 2: %s"%messagecount
    
    if messagecount==0:
        print "Mailboxes are in sync!"
        break
    
    if time.time()>timeout:
        print "Timeout... server 2 not in sync"
        sys.exit(1)
        

