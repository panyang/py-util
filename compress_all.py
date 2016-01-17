
import sys
import os
import glob

if (__name__ =="__main__"):
  if len(sys.argv)>=2:
    pattern = sys.argv[1]
    files = glob.glob(pattern)
    
    for file in files:
      name = os.path.basename(file)
      (target, _) = os.path.splitext(name)
      cmd = ["HandBrakeCLI", "-i", file, \
               "-e", "x264", \
               # "-a", "2", \ # Select audio track
               "--preset 'iPod Legacy'", \
               "-X 960"
			   "--format mp4", \
               "-b", "1600", \
               #"-E", "copy:ac3", \
               "-E", "faac", \
               "--two-pass", "-T", \
               "-o", target.lower()+".m4v"]
      #print(" ".join(cmd))
      os.system(" ".join(cmd))
	  
	  # Delete original file
      os.remove(file)
  else:
    print("Usage: dvd2iphone directory [title]")
