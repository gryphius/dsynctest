#!/usr/bin/python


"""Test: Append messages to box 1 and check if they are synced"""

NUMMESSAGES=100
MAILBOX="INBOX"
CHECK_INTERVAL=5
MAX_WAIT_SYNC=30


from accountconfig import *
from helpers import *
import time
import sys

imap1=get_imap_connection(SERVER1_HOST, USERNAME, PASSWORD,assertEmpty=True)

print "appending messages..."

#Append messages to server1
counter=0
for message in create_dummy_txt_messages(NUMMESSAGES):
    counter+=1
    content=message.as_string()
    imap1.append(MAILBOX,None,None,content)
    if counter%10==0:
        print "%s/%s"%(counter,NUMMESSAGES)
        

#Check Message count on server 1
print "Verifying amount on server 1..."
time.sleep(2)
result,messagecount=imap1.select()
messagecount=int(messagecount[0])
assert messagecount==NUMMESSAGES,"Server1: Expected %s messages, got %s"%(NUMMESSAGES,messagecount)


#check sync to server 2
imap2=get_imap_connection(SERVER2_HOST, USERNAME, PASSWORD,assertEmpty=True)
now=time.time()
timeout=now+MAX_WAIT_SYNC

while True:
    time.sleep(CHECK_INTERVAL)
    
    result,messagecount=imap2.select()
    messagecount=int(messagecount[0])
    print "Current messagecount on server 2: %s"%messagecount
    
    if messagecount==NUMMESSAGES:
        print "Mailboxes are in sync!"
        break
    
    if time.time()>timeout:
        print "Timeout... server 2 not in sync"
        sys.exit(1)
        

