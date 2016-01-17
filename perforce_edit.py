import os
import sys
import shutil

import submit_file

# Use perforce to copy files
def editfile(x, srcdir):
    p4dstfile = x.replace("@", "%40")
    dstfile = os.path.join(srcdir, x)
    newfile = False

    if os.path.isfile(dstfile):
        # Destination file exists        
        os.system('p4 edit ' + p4dstfile)
        newfile = False

def perform_action(actions, srcdir):
    for a in actions:
        editfile(a["file"], srcdir)
    
if __name__ == "__main__":
    if len(sys.argv) == 2:
        filename = sys.argv[1]
        srcdir = os.getcwd()
        actions = submit_file.parse(filename)
        perform_action(actions, srcdir)
