#!/usr/local/bin/python

import os
import glob
import sys
import subprocess
 
if (__name__ == "__main__"):
   if len(sys.argv)==1:
       # get all the files
       files = glob.glob("*.m4v")
       files_mp4 = glob.glob("*.mp4")
       files.extend(files_mp4)
   elif len(sys.argv)==2:
       files = [sys.argv[1]]
       # rename all the files according to input args
   else: 
      # len!=1
      print('Usage: convert_nokia')
      exit()
    
   i = 0
   for afile in files:
      #print(afile)
      [name,ext] = afile.rsplit('.', 1)
      
      if (name[-2:].lower() !="_n"):
          cmd = ["ffmpeg","-i", afile,  \
              "-f", "mp4", \
              "-vcodec", "mpeg4", "-b", "512k", \
              "-r", "15", \
              "-acodec", "aac", "-ab", "128k"];
          cmd.extend(["-strict", "experimental", \
                      name + "_n.mp4"])

          #print(" ".join(cmd))
          p = os.system(" ".join(cmd))
   
        
