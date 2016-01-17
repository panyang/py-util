import os
from string import *  
import sys
from mutagen.easyid3 import EasyID3

def isSnapshotDir(filename):
    basename = os.path.basename(filename)
    return basename=='~snapshot' or basename=='.snapshot'
def isLinuxHiddenFile(filename):
    basename = os.path.basename(filename)
    return basename[0]=='.'

def hasDotExt(filename):
    basename = os.path.basename(filename)
    return (basename.find( '.')>0)

def isPodcastFile(filename):
    if not hasDotExt(filename):
        return False
    [name, ext] = filename.rsplit( '.', 1)
    if not ext=='mp3':
        return False

    try:
        audio = EasyID3(filename)
    except:
        return False
       
    if not audio.has_key('genre'):
        return False
    genres = audio['genre']
    genre = genres[0]
    return genre.lower() == 'podcast'

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
            deleteTempFiles(fullpath, force)
            
        elif os.path.isfile(fullpath):
            # Delete a file if the file is temporary
            if isPodcastFile(fullpath) or force: 
                # delete temporary files and any file in temp directory
                print('>>>>>>>>>>>Deleting ' + afile)
                os.remove(fullpath)
                
    #If the directory is empty at this point, delete the directory
    files = os.listdir(dir)
    if os.path.isdir(dir) and (not os.path.islink(dir)):
        if len(files)==0 :
              # Need to remove the current directory
              print('>>>>>>>>>>>Removing directory' + dir)
              os.rmdir(dir)
        elif force:
            print('Warning: cannot remove directory because some files remain' \
                  + dir)
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
    else:
        print('Usage: cleanuppodcasts')