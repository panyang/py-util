#/usr/local/bin/python
import os
import sys

import hashlib

import shutil # for copy files
"""Python version of fast copy"""


def isLinuxHiddenFile(filename):
    basename = os.path.basename(filename)
    return basename[0]=='.'

def isNewer(file1, file2):
    return (os.path.getmtime(file1) > os.path.getmtime(file2))

def equalSize(file1, file2):
    # if the size of two files are the same
    if (os.path.isfile(file1) and os.path.isfile(file2)):
        return (os.path.getsize(file1) == os.path.getsize(file2))
    else:
        # if two directories, assumes they are different
        return False

def equalMD5(file1, file2):
    # Compute MD5 checksum of the two files and compare them
    if not equalSize(file1, file2):
        return False
    if os.path.isfile(file1) and os.path.isfile(file2) :
        with open(file1,'rb', 1) as f1:
            with open(file2,'rb',1) as f2:
                try:
                    m1 = hashlib.md5(f1.read()).hexdigest()
                    m2 = hashlib.md5(f2.read()).hexdigest()
                    
                    return (m1==m2)
                except:
                    return False
    else:
        return False
        
def writable(file):
    return (not os.path.exists(file)) or os.access(file, os.W_OK)
def readable(file):
    return os.access(file, os.R_OK)
        
def copyFileOrSyncDir(srcfile, dstfile, afile):
    """if it is a file simply copy it, If afile is a directory, sync it."""
    filesCopied = 0 # assume
    bytesCopied = 0 # assume
    if os.path.isfile(srcfile):
        if readable(srcfile) and writable(dstfile):
            try:
                print( "copy " + afile)
            except:
                print("copy")
            shutil.copyfile(srcfile, dstfile)
            filesCopied = 1
            bytesCopied = os.path.getsize(srcfile)
    else:
        (filesCopied, bytesCopied) = syncDir(srcfile, dstfile)
    return (filesCopied, bytesCopied)

def syncDir(dir1, dir2):
    bytesCopied = 0
    filesCopied = 0

    try:
        print ('Syncing ' + dir1 + ' to ' +dir2)
    except:
        print ('syncing')
    # copy files dir1 >> dir2
    files1 = os.listdir(dir1)
    if not os.path.exists(dir2):
        try:
            print('Creating' + dir2)
        except:
            print('creating')    
        os.mkdir(dir2)
    files2 = os.listdir(dir2)
    for afile in files1:
        #
        srcfile = os.path.join(dir1, afile)
        dstfile = os.path.join(dir2, afile)
        if isLinuxHiddenFile(srcfile):
            continue

        if os.path.islink(srcfile):
            continue
        
        if (not (afile in files2) or
            not os.path.isfile(dstfile) or 
            not equalMD5(srcfile, dstfile)):
            # we use MD5 checksum to determine if the
            # file has changed.
            (subFiles, subBytes) = copyFileOrSyncDir(srcfile, dstfile, afile)
            bytesCopied = bytesCopied + subBytes
            filesCopied = filesCopied + subFiles
            
    return (filesCopied, bytesCopied)


#================================================
# main program
#================================================
if (__name__ == "__main__"):
    if len(sys.argv) == 3:
        srcDir = sys.argv[1]
        dstDir = sys.argv[2]
    elif len(sys.argv) == 2:
        srcDir = os.getcwd()
        dstDir = sys.argv[1]
    else:
        print('Usage: backup [src directory] <dst directory>')
        sys.exit()

    (filesCopied, bytesCopied) = syncDir(srcDir, dstDir) 
    kbC = bytesCopied/1024
    if kbC < 1024:
        print("Total %d files, %d KB copied." % (filesCopied, kbC))
    else:
        mbC = kbC / 1024
        if mbC < 1024:
            print("Total %d files, %d MB copied." % (filesCopied, mbC))
        else: # more than 1 GB
            gbC = float(mbC) / 1024 
            print("Total %d files, %.3f GB copied." % (filesCopied, gbC))
            
