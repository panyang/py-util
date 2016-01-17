#!/usr/local/bin/python

import os
import glob
import sys
import subprocess


if (__name__ == "__main__"):
   if len(sys.argv)==1:
       # get all the files
       files = glob.glob("*.mp4")
   elif len(sys.argv)==2:
       files = [sys.argv[1]]
       # rename all the files according to input args
       
   i = 0
   for afile in files:
      #print(afile)
      [name,ext] = afile.rsplit('.', 1)
      cmd = ["ffmpeg","-i", "\""+afile+"\"", \
              "-acodec", "copy", "-vn"];
      cmd.extend(["\""+name + ".m4a\""])
      #print(" ".join(cmd))
      os.system(" ".join(cmd))
   else: 
      # len!=1
      print('Usage: convert_nokia')
