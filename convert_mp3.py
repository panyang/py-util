#!/usr/local/bin/python

import os
import glob
import sys


if (__name__ == "__main__"):
   files = []
   if len(sys.argv)==1:
       # get all the files
       files = glob.glob("*.aac")
   else:
       files = sys.argv[1:]
       
   i = 0
   for afile in files:
      #print(afile)
      [name,ext] = afile.rsplit('.', 1)
      cmd = ["ffmpeg","-i" , '"'+ afile + '"', \
             "-acodec", "libmp3lame", "-ab", "160k"];
      cmd.extend(['"' + name + ".mp3" + '"'])
      p = os.system(" ".join(cmd))

   
        
