import os
import sys

""" 
Utilities for handling files 
"""

# Linux hidden files begin with '.'
def isLinuxHiddenFile(filename):
    basename = os.path.basename(filename)
    return basename[0]=='.'

def isNodeModules(filename):
    basename = os.path.basename(filename)
    return basename == 'node_modules'

# desktop.ini
def isDesktopIni(filename):
    basename = os.path.basename(filename)
    return (basename =='desktop.ini')

def isTarget(filename):
    basename = os.path.basename(filename)
    return (basename =='target')

def isHidden(filename):
    basename = os.path.basename(filename)
    return (basename =='_build') or (basename == "CMakeFiles")
   
def isRTWHidden(filename):
    basename = os.path.basename(filename)
    return (basename == 'slprj')

def isBuild(filename):
    basename = os.path.basename(filename)
    return basename == "build"
   
# The basename of the file has '.' in it
def hasDotExt(filename):
    basename = os.path.basename(filename)
    return (basename.find( '.')>0)

# The following are used in the file count
def isMatlabSourceFile(filename):
    isMatlabSourceFile.desc = "Matlab source file"
    if not hasDotExt(filename):
        return False
    else:
        [name, ext] = filename.rsplit('.', 1)
        return (ext == 'm')

def isScalaSourceFile(filename):
    isScalaSourceFile.desc = "Scala source file"
    if not hasDotExt(filename):
        return False
    else:
        [name, ext] = filename.rsplit('.', 1)
        return (ext == 'scala')
    
def isPythonSourceFile(filename):
    isPythonSourceFile.desc = "Python source file"
    if not hasDotExt(filename):
        return False
    else:
        [name, ext] = filename.rsplit('.', 1)
        return (ext == 'py')
def isCppSourceFile(filename):
    isCppSourceFile.desc = "C++ source file"
    if not hasDotExt(filename):
        return False
    else:
        [name, ext] = filename.rsplit('.', 1)
        ext = ext.lower()
        return (ext == 'cpp' or ext == 'hpp' or \
                    ext == 'c' or ext =='h')

def isOCamlSourceFile(filename):
    isOCamlSourceFile.desc = "OCaml source file"
    if not hasDotExt(filename):
        return False
    else:
        [name, ext] = filename.rsplit('.', 1)
        return (ext == 'ml' or ext == 'mli') 

def isJavaScriptSourceFile(filename):
    isJavaScriptSourceFile.desc = "JavaScript source file"
    if not hasDotExt(filename):
        return False
    else:
        [name, ext] = filename.rsplit('.', 1)
        return (ext == "js")


def isJavaSourceFile(filename):
    isJavaSourceFile.desc = "Java source file"
    if not hasDotExt(filename):
        return False
    else:
        [name, ext] = filename.rsplit('.', 1)
        return (ext == "java")

def isGroovySourceFile(filename):
    isGroovySourceFile.desc = "Groovy source file"
    if not hasDotExt(filename):
        return False
    else:
        [name, ext] = filename.rsplit('.', 1)
        return (ext == "groovy")

def isAntlrSourceFile(filename):
    isAntlrSourceFile.desc = "Antlr source file"
    if not hasDotExt(filename):
        return False
    else:
        [name, ext] = filename.rsplit('.', 1)
        return (ext == 'g' or ext == 'stg' or ext == 'g4')

def isShellScript(filename):
    isShellScript.desc = "Shell script"
    if not hasDotExt(filename):
        return False
    else:
        [name, ext] = filename.rsplit('.', 1)
        return (ext == 'sh')
    
def fileLen(filename):
    """
    Get the length of the file in bytes.
    """
    try:
        with open(filename, 'r', errors = 'ignore') as f:
            count = 0
            lines = f.readlines()
            n = len(lines)
    except:
        print("Cannot read")
        print(filename)
        n = 0
    return n

