import sys
import os
import shutil

from fileutils import *

def is_package(line):
    l = line.rstrip()
    parts = l.split(' ')
    return len(parts) == 2 and parts[0] == 'package'

def write_file(lines, filename):
    with open(filename, 'w') as fh:
        for line in lines:
            fh.write(line)


def process_file(filename):
    backup = filename + '_backup'
    shutil.move(filename, backup)
    with open(backup) as fh:
        lines = fh.readlines()
        try:
            idx = next(idx for idx, line in enumerate(lines) if is_package(line))
            newlines = lines[idx:]
        except StopIteration:
            newlines = lines
        print("Rewriting %s" % filename) 
        write_file(newlines, filename)
        os.remove(backup)

def process_dir(d):
    files = os.listdir(d)
    for file in files:
        fullpath = os.path.join(d, file)
        
        # it is not a snapshot directory
        if os.path.isdir(fullpath) and \
        not isLinuxHiddenFile(file) and \
        not isHidden(file) and \
        not isRTWHidden(file) and \
        not isNodeModules(file) and \
        not isBuild(file) and \
        not isTarget(file):
            process_dir(fullpath)
            
        elif os.path.isfile(fullpath) and isJavaSourceFile(file):
            process_file(fullpath)

if __name__ == "__main__":
    d = os.getcwd()
    process_dir(d)
