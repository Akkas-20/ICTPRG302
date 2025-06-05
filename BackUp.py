#!/usr/bin/python3
import logging
import pathlib
import shutil
from datetime import datetime
import sys
import os
import backupcfg

import smtplib

smtp = {"sender": "akkasnik@gmail.com",    # elasticemail.com verified sender
        "recipient": "30026912@students.sunitafe.edu.au", # elasticemail.com verified recipient
        "server": "in-v3.mailjet.com",      # elasticemail.com SMTP server
        "port": 587,                           # elasticemail.com SMTP port
        "user": "22e99ae90c451e38b7815a8c5fd79a80",      # elasticemail.com user
        "password": "22369a532b5ff76f569a1bdb4bbc69b0"}     # elasticemail.com password

# append all error messages to email and send
def sendEmail(message):

    email = 'To: ' + smtp["recipient"] + '\n' + 'From: ' + smtp["sender"] + '\n' + 'Subject: Backup Error\n\n' + message + '\n'

    # connect to email server and send email
    try:
        smtp_server = smtplib.SMTP(smtp["server"], smtp["port"])
        smtp_server.ehlo()
        smtp_server.starttls()
        smtp_server.ehlo()
        smtp_server.login(smtp["user"], smtp["password"])
        smtp_server.sendmail(smtp["sender"], smtp["recipient"], email)
        smtp_server.close()
    except Exception as e:
        print("ERROR: An error occurred.")

def main():
    """
    This Python code demonstrates the following features:
    
    * accessing command line arguments.
    
    """
    logging.basicConfig(filename = backupcfg.loggingfilename,
    level = logging.DEBUG)
    logger = logging.getLogger()
    try:
        argCount = len(sys.argv)
        program = sys.argv[0]
        if(argCount>1):
         arg1 = sys.argv[1]
        else:
            arg1="parameter is not enough"
        
        print("The program name is " + program + ".")
        print("The number of command line items is " + str(argCount) + ".")
        print("Command line argument 1 is " + arg1 + ".")
        
    except:
        print("ERROR: An error occurred.")
        
    if(arg1=="job1" or arg1=="job2"):
        print("job number is ok")
     
        try:
            fileExists = backupcfg.copyfile
            
            if not os.path.exists(fileExists):
                print("ERROR: file " + fileExists + " does not exist.")
            else:
                print(fileExists + " exist.")
                
                try:
                    dateTimeStamp = datetime.now().strftime("%Y%m%d-%H%M%S")  
            
                    srcFile = backupcfg.sourcefilelocation
                    srcDir = backupcfg.sourcedirectrylocation
            
                    srcLoc = srcFile # change this srcLoc = srcDir to test copying a directory
                    srcPath = pathlib.PurePath(srcLoc)
            
                    dstDir = backupcfg.destinationdirectry
                    dstLoc = dstDir + "/" + srcPath.name + "-" + dateTimeStamp
            
                    print("Date time stamp is " + dateTimeStamp) 
                    print("Source file is " + srcFile)
                    print("Source directory is " + srcDir)
                    print("Source location is " + srcLoc)
                    print("Destination directory is " + dstDir)
                    print("Destination location is " + dstLoc)
            
                    if pathlib.Path(srcLoc).is_dir():
                        shutil.copytree(srcLoc, dstLoc)
                    else:
                        shutil.copy2(srcLoc, dstLoc)
                        logger.debug("successfully copy")
                    
                except:
                    print("ERROR: file is not found error.")
                    logger.error("ERROR: file is not found error.")
                    message = "ERROR: file is not found error." 
                    sendEmail(message)
                
                
        except:
            print("ERROR: An error occurred.")
            logger.error("ERROR: An error occurred.")
            message = "ERROR: An error occurred"
            sendEmail(message)
     
    else:
     print("it is not correct job number")
     logger.error("it is not correct job number")
     message = "it is not correct job number"
     sendEmail(message)
     
    
if __name__ == "__main__":
    main()