#!/usr/local/bin/python
#---------------------------------------------------------------
#   CLEANUP.PY 
#
# A python script that removes all files that are auto-generated
# or temporary.
#---------------------------------------------------------------

import os
from string import *  
import sys
from shutil import copyfile

#--------------------------------------------------------------
# File information
#--------------------------------------------------------------

def isMatlabDump(filename):
    basename = os.path.basename(filename)
    return (basename.find('matlab_crash_dump')>=0)

def isDesktopIni(filename):
    basename = os.path.basename(filename)
    return (basename =='desktop.ini')

def hasDotExt(filename):
    basename = os.path.basename(filename)
    return (basename.find( '.')>0)

def isLatexGeneratedFile(ext):
    if (ext=='aux'): #LATEX aux file
        return True
    elif (ext=='blg'): #LATEX blg file
        return True
    elif (ext=='bak'): # LATEX backup file
        return True
    elif (ext=='bbl'): # LATEX bbl file
        return True
    elif (ext=='log'): # LATEX log file
        return True
    elif (ext=='dvi'): # LATEX dvi file
        return True
    else:
        return False

def isLinuxHiddenFile(filename):
    basename = os.path.basename(filename)
    return basename[0]=='.'

def isTempFile(file):
    if not hasDotExt(file):
        return False
    if isMatlabDump(file):
        return True
    [name, ext] = file.rsplit( '.', 1)
    if (ext=='asv'): #MATLAB asv file
        return True
    elif (ext=='autosave'):
        return True
    elif isLatexGeneratedFile(ext):
        return True
    elif len(ext)>0 and (ext[-1]=='~'): # Emacs backup file
        return True
    elif isDesktopIni(file):
        return True
    return False
#--------------------------------------------------------------
# Directory information
#--------------------------------------------------------------
def isSnapshotDir(filename):
    basename = os.path.basename(filename)
    return basename=='~snapshot' or basename=='.snapshot'

def isCVSDir(dir):
    basename = os.path.basename(dir)
    return basename=='CVS'
def isSimulinkDir(dir):
    basename = os.path.basename(dir)
    return basename == 'slprj' or basename=='sfprj' or \
           basename == 'sldv_output' or basename[-4:]=='_rtw' or \
           basename == 'scv_images'

def isTempDir(dir):
    if isCVSDir(dir):
        return False
    elif isSimulinkDir(dir):
        return True
    else:
        return False
#--------------------------------------------------------------
# Recursive function to delete all temporary files in the given
# directory.
#
# If the directory is empty, remove the directory;
# If the directory is inside a temporary directory (force=true),
#  remove everything
# 
#--------------------------------------------------------------
def deleteTempFiles(dir, force):
    files = os.listdir(dir)
    for afile in files:
        fullpath = os.path.join(dir, afile)

        # Recursively look into subdirectories
        # if the directory is not hidden and 
        # it is not a snapshot directory
        if os.path.isdir(fullpath) and \
        not isLinuxHiddenFile(afile) and \
        not isSnapshotDir(afile):
            print('>>Entering '+ afile)
            # Delete files in the directory
            deleteTempFiles(fullpath, (force or isTempDir(fullpath)))
            
        elif os.path.isfile(fullpath):
            # Delete a file if the file is temporary
            if isTempFile(fullpath) or force: 
                # delete temporary files and any file in temp directory
                #print('>>>>>>>>>>>Deleting ' + afile)
                copyfile(os.devnull, fullpath)
                os.remove(fullpath)
                
    #If the directory is empty at this point, delete the directory
    files = os.listdir(dir)
    if os.path.isdir(dir) and (not os.path.islink(dir)):
        if len(files)==0 :
              # Need to remove the current directory
              #print('>>>>>>>>>>>Removing directory' + dir)
              os.rmdir(dir)
        elif force:
            #print('Warning: cannot remove directory because some files remain' \
            #      + dir)
            for afile in files: 
                  print(afile)
            

#=================================================
# Main program
#=================================================
if (__name__ == "__main__"):
    if len(sys.argv)==1:
        # get all the files
        cwd = os.getcwd()
        # rename all the files according to input args
        print('Clean up temporary files in current directory:')
        deleteTempFiles(cwd, False);
    elif sys.argv[1] == "-f":
        cwd = os.getcwd()
        deleteTempFiles(cwd, True)
    else:
        print('Usage: cleanup')
