#/usr/local/bin/python
import os
import sys
import time

import hashlib

import shutil # for copy files
'''Python version of fast copy '''


def isLinuxHiddenFile(filename):
    basename = os.path.basename(filename)
    return basename[0]=='.'

def isNewerThan(file1, time2):
    return (os.path.getmtime(file1) > time2)

def writable(file):
    return (not os.path.exists(file)) or os.access(file, os.W_OK)
def readable(file):
    return os.access(file, os.R_OK)
        
def touch(fname, times=None):
    with open(fname, "a") as file:
        os.utime(fname, times)
       
def touchNew(dir1, threshold):
    try:
        print ('Exploring ' + dir1 )
    except:
        print ('syncing')
    # copy files dir1 >> dir2
    filesTouched = 0
    files1 = os.listdir(dir1)
    for afile in files1:
        #
        srcfile = os.path.join(dir1, afile)
        if isLinuxHiddenFile(srcfile):
            continue

        if os.path.isfile(srcfile) and \
           isNewerThan(srcfile, threshold):
            touch(srcfile)
            filesTouched = filesTouched + 1
        if os.path.isdir(srcfile):
            subFiles =  touchNew(srcfile, threshold)
            filesTouched = filesTouched + subFiles
                    
    return filesTouched


#================================================
# main program
#================================================
if (__name__ == "__main__"):
    threshold = time.time() - 24*3600*30; # Files changed in the last week
    
    if len(sys.argv) == 2:
        srcDir = sys.argv[1]
    elif len(sys.argv) == 1:
        srcDir = os.getcwd()
    else:
        print('Usage: touch_new [src directory] <dst directory>')
        sys.exit()

    filesTouched = touchNew(srcDir, threshold) 
    print("Total %d files touched." % filesTouched)
            
