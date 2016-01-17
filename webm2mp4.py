
import sys
import os

if (__name__ =="__main__"):
  if len(sys.argv)>=2:
    directory = sys.argv[1]
    if directory[-1] == '/':
       directory = directory[:-1]

    title = "1"  # default
    if len(sys.argv) == 3:
      title = sys.argv[2]

    if os.path.isdir(directory):
        source = directory + "/VIDEO_TS"
    elif os.path.isfile(directory):
        source = directory
    
    target = directory.split('/')[-1] 

    
    cmd = ["HandBrakeCLI", "-i", source, \
           "-e", "x264", \
           "-t", title, \
           "--strict-anamorphic", \
          "-x",  "-preset veryfast", \
          "-X", "1280", \
           "-b", "2000", \
           "-E", "faac", \
           "--two-pass", "-T", \
           "-o", target.lower()+".mp4"]
    #print(" ".join(cmd))
    os.system(" ".join(cmd))
  else:
    print("Usage: webm2mp4 directory [title]")
