import os
import sys

from fileutils import *

option = ['-batch', '-l',
          '/usr/share/emacs/site-lisp/google/google-java-format.el',
          '--eval',
          '"(google-java-format-region (point-min) (point-max))"',
          '-f', 'save-buffer']

def process_file(filename):
  print("Formatting %s" % filename)
  cmd = ['emacs', filename]
  cmd.extend(option)
  #print(" ".join(cmd))
  os.system(" ".join(cmd))

def process(d):
  files = os.listdir(d)
  for afile in files:
    fullpath = os.path.join(d, afile)

    # Recursively look into subdirectories
    # if the directory is not hidden and
    # it is not a snapshot directory
    if (os.path.isdir(fullpath) and
        not isLinuxHiddenFile(afile) and
        not isHidden(afile) and
        not isRTWHidden(afile) and
        not isNodeModules(afile) and
        not isBuild(afile) and
        not isTarget(afile)):
      process(fullpath)
    elif os.path.isfile(fullpath):
      process_file(fullpath)

if __name__ == "__main__":
  process(os.getcwd())
