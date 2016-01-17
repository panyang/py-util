
import sys
import os

from hbutils import *

if (__name__ =="__main__"):
  if len(sys.argv)>=2:
    directory = sys.argv[1]
 
    title = "1"  # default
    if len(sys.argv) == 3:
      title = sys.argv[2]

    source,target = getSourceTarget(directory)
    
    cmd = ["HandBrakeCLI", "-i", source, \
           "-t", title ] + \
           commonOptions() + iOSOptions() + \
           ["-o", target.lower()+".m4v"]
    #print(" ".join(cmd))
    os.system(" ".join(cmd))
  else:
    print("Usage: dvd2iphone directory [title]")
