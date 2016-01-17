#!/usr/local/bin/python
"""
    Lameall.py

    Use Lame to convert a few wav files to mp3
"""
import os
from string import *  
import sys

def hasDotExt(filename):
    basename = os.path.basename(filename)
    return (basename.find('.')>0)

  
if (__name__ == "__main__"):
   if len(sys.argv)==1:
       # get all the files
       cwd = os.getcwd()
       files = os.listdir(cwd)
       # rename all the files according to input args
       print('Lame all files in current directory:')
       print(cwd)
       i = 0
       filetype = 'wav'
       for afile in files:
          if not hasDotExt(afile):
             continue
          [name,ext] = afile.rsplit('.', 1)
          if (ext==filetype):
             print(('Lame '+ afile +  os.linesep))
             os.system(('lame --preset "standard" "' + afile) + '"')
             #os.remove(afile)
   else: 
      # len!=1
      print('Usage: lameall')
   
        
