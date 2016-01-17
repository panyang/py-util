""" HandBrake utilities: 
  A set of utilities to facilitate HandBrake extenal
  invoking. """

import os

# Return a valid fullpath for a given fullpath
def getSourceTarget(pathname):
    # Remove the trailing '/' in directory name
    if pathname[-1] == os.sep:
        pathname = pathname[:-1]
    if os.path.isdir(pathname):
        source = pathname + os.sep + "VIDEO_TS"
        filename = pathname.split(os.sep)[-1]        
        target = filename.lower()
    elif os.path.isfile(pathname):
        source = pathname
        filename = pathname.split(os.sep)[-1]
        target = ".".join(filename.split('.')[:-1])
    else:
        print("Error: cannot find file")

    return (source, target)

# HandBrake options
def commonOptions():
    return ["-e", "x264", \
            "--two-pass", "-T"]

def iOSOptions():
    return ["-b", "1600", \
            "--format mp4", \
             "-E", "faac"]
def nokiaOptions():
    return ["--format mkv", \
            "-b", "1600", \
            "-E", "copy:ac3"]
            
def strictAnamorphicOption():
    return ["--strict-anamorphic"]
          
