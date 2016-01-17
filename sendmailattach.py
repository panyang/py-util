#!/usr/local/bin/python

"""
  Use the default mail server to send a mail and attach
 a file to the mail.

 USAGE
  python sendmailattach.py <file1> <file2> ...
"""
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders

COMMASPACE = ', '

import os
import sys

def sendMail(to, subject, text, files=[]):
    """
    Send a a mail to the designated user using my email account
    """
    assert type(to)==list
    assert type(files)==list
    fro = "Zhi Han <zhi.han@gmail.com>"

    msg = MIMEMultipart()
    msg['From'] = fro
    msg['To'] = COMMASPACE.join(to)
    msg['Subject'] = subject

    msg.attach( MIMEText(text) )
    #==========================================
    # Attach the files
    #==========================================
    for file in files:
        part = MIMEBase('application', "octet-stream")
        fp =open(file,"rb")
        part.set_payload(fp.read())
        fp.close()
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"'
                       % os.path.basename(file))
        msg.attach(part)
        
    #==============================================
    # Log into the Gmail server and send the mail
    #============================================== 
    #==============================================
    # Log into the Gmail server and send the mail
    #============================================== 
    mailServer = smtplib.SMTP('smtp.gmail.com', 587)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login('zhi.han@gmail.com', '2003cmu')
    mailServer.sendmail(fro, to, msg.as_string() )
    mailServer.close()
    
#===============================================================
# utility function
# find existing files
#===============================================================
def validatefiles(files):
    """
    Validate the file exists.
    """
    assert type(files)==list
    vfiles =[] # validated files
    cwd = os.getcwd()
    for afile in files:
        if os.path.isfile(afile): #if the file can be found
            vfiles.append(afile)
        else:
            fullfile=os.path.join(cwd,afile)
            if os.path.isfile(fullfile):
                vfiles.append(fullfile) # attach a file
            else:
                vfiles=0  # error out
                return vfiles
            
    return vfiles

#--------------------------------------------------------------    
def splitline(s):
    """
    split a string into multiple lines
    """
    str2 = s.split('\n')
    return str2[0]
    

#===============================================================
# main function starts here
#===============================================================
if (__name__=="__main__"):
    if len(sys.argv)==1:
        files = []
    else:
        files=validatefiles(sys.argv[1:])
        if files==0:
            print('One or more file does not exist')
            exit
    
    print("Send email to (separated by ','): ")
    dsts= sys.stdin.readline()
    dsts = splitline(dsts)
    dst = dsts.split(',')
    print("Please type subject:")
    sub = sys.stdin.readline()
    subject = splitline(sub)
    print("Please write content (finish by Ctrl-D or Ctrl-Z (Windows):")
    print("===========================================================")
    body=sys.stdin.read()
    print("===========================================================")
    print("Sending the mail to %s ..." % dst)
    sendMail(dst, subject, body, files)
