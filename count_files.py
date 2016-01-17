import os
import sys

from fileutils import  *

class FileCounter:
    def __init__(self, predicate):
        self.predicate = predicate
        self.fileCount = 0
        self.lineCount = 0

    def process(self, filename):
        if self.predicate(filename):
            self.fileCount += 1
            self.lineCount += fileLen(filename)

            
def countFiles(counters, d):
    files = os.listdir(d)
    for afile in files:
        fullpath = os.path.join(d, afile)

        # Recursively look into subdirectories
        # if the directory is not hidden and 
        # it is not a snapshot directory
        if os.path.isdir(fullpath) and \
        not isLinuxHiddenFile(afile) and \
        not isHidden(afile) and \
        not isRTWHidden(afile) and \
        not isNodeModules(afile) and \
        not isBuild(afile) and \
        not isTarget(afile):
            countFiles(counters, fullpath)
            
        elif os.path.isfile(fullpath):
            for counter in counters:
                counter.process(fullpath)



if (__name__ == "__main__"):
    if len(sys.argv) == 1:
        d = os.getcwd()
        scalaCounter = FileCounter(isScalaSourceFile)
        matlabCounter = FileCounter(isMatlabSourceFile)
        pythonCounter = FileCounter(isPythonSourceFile)
        cppCounter = FileCounter(isCppSourceFile)
        ocamlCounter = FileCounter(isOCamlSourceFile)
        antlrCounter = FileCounter(isAntlrSourceFile)
        javascriptCounter = FileCounter(isJavaScriptSourceFile)
        javaCounter = FileCounter(isJavaSourceFile)
        groovyCounter = FileCounter(isGroovySourceFile)
        shellCounter = FileCounter(isShellScript)

        c = [scalaCounter,
             matlabCounter,
             pythonCounter,
             cppCounter,
             ocamlCounter,
             antlrCounter,
             javascriptCounter,
             javaCounter, 
             groovyCounter,
             shellCounter]
        

        countFiles(c, d)
        for cc in c:
            if cc.fileCount > 0:
                print("\033[32m%s\033[m" % cc.predicate.desc)
                print("%d files, %d lines" % (cc.fileCount, \
                                              cc.lineCount))

        total = 0
        for cc in c:
            total += cc.lineCount
        print("Tota %d lines" % total)


        
    else:
        print("Usage: count_files.py")
    
