#!/usr/local/bin/python

import os
import glob
import sys
import readlyrics

if (__name__ == "__main__"):
   if len(sys.argv)==1:
       # get all the files
       files = glob.glob("*.mp3")
       
   i = 0
   for afile in files:
      readlyrics.updateFile(afile)
   else: 
      # len!=1
      print('Usage: convert_nokia')
   
        
