#!/usr/local/bin/python
"""
    renall.py

    My first Python script to rename a bunch
   of files.

   LOG
    Updated 1/23/2011 to be able to rename extensions. 
"""

import os
from string import *  
import sys

def hasDotExt(filename):
    basename = os.path.basename(filename)
    return basename.find('.')>0

def count_files(files, filetype):
    i = 0
    for afile in files:
        if not hasDotExt(afile):
            continue
        [name,ext] = afile.rsplit('.', 1)
        if (ext.lower()==filetype.lower()):
           i = i+1
    return i

def rename_files(files, filetype, option, newName):
    # rename all the files according to input args
    print('Rename all files in current directory:')
    print(cwd)
    total = count_files(files, filetype)
    num_digits = len(str(total))
    i = 0
    for afile in files:
            if not hasDotExt(afile):
               continue
            [name,ext] = afile.rsplit('.', 1)
            if (ext.lower()==filetype.lower()):
               i = i+1
               if option.lower() == 'base':
                   name = newName + str(i).zfill(num_digits)
                   fullname = ".".join([name,ext.lower()])
               else:
                   fullname = ".".join([name, newName.lower()])
               #print('Renaming '+ afile +' to ' + fullname + os.linesep)
               os.rename(afile,fullname)
    
  
if (__name__ == "__main__"):
   if len(sys.argv)==4:
      ext = sys.argv[1]
      # get all the files
      option = sys.argv[2]
      newName = sys.argv[3]
      cwd = os.getcwd()
      files = os.listdir(cwd)
      rename_files(files,ext, option, newName)
   else: 
      # len!=3
      print('Usage: renall <ext> <option> <prefix>')
   
        
