import os
import sys
import shutil

import submit_file

# Use perforce to copy files
def copyfile(x, src, dst):
    srcfile = os.path.join(src, x)
    dstfile = os.path.join(dst, x)

    srcfile = os.path.normpath(srcfile)
    dstfile = os.path.normpath(dstfile)

    p4dstfile = x.replace("@", "%40")
    
    newfile = False

    if os.path.isfile(dstfile):
        # Destination file exists        
        os.system('p4 edit ' + p4dstfile)
        newfile = False
    else:
        # Destination file not exists
        dstdir = os.path.dirname(dstfile)
        if not os.path.isdir(dstdir):
            # Need to create the dstination dir
            os.makedirs(dstdir)
        newfile = True
    shutil.copyfile(srcfile, dstfile)
    if newfile:
        os.system('p4 add -f ' + p4dstfile)

def deletefile(x, dst):
    dstfile = os.path.join(dst, x)
    dstfile = os.path.normpath(dstfile)
    p4dstfile = x.replace('@', '%40')

    if os.path.isfile(dstfile):
        os.system('p4 delete ' + p4dstfile)


def perform_action(x, src, dst):
    if x["action"] == "copy":
        copyfile(x["file"], src, dst)
    elif x["action"] == "delete":
        deletefile(x["file"], dst)

def perform_actions(actions, src, dst):
    for a in actions:
        perform_action(a, src, dst)
        

if __name__ == "__main__":
    if len(sys.argv) == 3:
        filename = sys.argv[1]
        srcdir = sys.argv[2]
        dstdir = os.getcwd()
        
        actions = submit_file.parse(filename)
        perform_actions(actions, srcdir, dstdir)
    else:
        print("Wrong number of inputs")
        sys.exit()
