
import sys
import os

if (__name__ =="__main__"):
  if len(sys.argv)==3:
     titlestr = sys.argv[2]
     titles = [int(x) for x in titlestr[1:-1].split(",")]
  else:
     titles = range(1, 5)

  if len(sys.argv)>=2:
    directory = sys.argv[1]
    if directory[-1] == '/':
       directory = directory[:-1]

    if os.path.isdir(directory):
        source = directory + "/VIDEO_TS"
    elif os.path.isfile(directory):
        source = directory
    
    target = directory.split('/')[-1] 

    for i in titles:
        cmd = ["HandBrakeCLI", "-i", source, \
                   "-e", "x264", \
                   "-t", str(i), \
                   #"--strict-anamorphic", \ 
               # HandBrake's iPhone Legacy setting
                   "-x", "level=30:bframes=0:weightp=0:cabac=0:ref=1:" + \
                 "vbv-maxrate=1500:vbv-bufsize=2000:analyse=all:me=umh:" + \
                 "no-fast-pskip=1:psy-rd=0.0,0.00:subq=6:8x8dct=0:trellis=0", \
                   "-X", "640", \
                   "-b", "400", \
                   #"-E", "ac3", \
                   "-E", "faac", \
                   "--two-pass", "-T", \
                   "-o", target.lower()+ "_" + str(i) + ".mp4"]
        print(" ".join(cmd))
        os.system(" ".join(cmd))
    
  else:
    print("Usage: xfiles directory title")
