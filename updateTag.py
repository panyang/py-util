#!/usr/local/bin/python
"""
    renall.py - My first Python script to rename a bunch
   of files. 
"""
import os
import sys

def hasDotExt(filename):
    basename = os.path.basename(filename)
    return (basename.find( '.')>0)

def isMP3File(filename):
    if not hasDotExt(filename):
        return False
    [name, ext] = filename.rsplit( '.', 1)
    if not ext=='mp3':
        return False
    return True

  
if (__name__ == "__main__"):
    cwd = os.getcwd()
    filepath = os.path.abspath( __file__ )
    dirname = os.path.dirname(filepath)
    files = os.listdir(cwd)
    for afile in files:
        fullpath = os.path.join(cwd, afile)
        if (isMP3File(fullpath)):
            os.system('java -jar ' + \
			os.path.join(dirname, 'id3iconv.jar') + \
			' -e GBK ' + fullpath)
        
