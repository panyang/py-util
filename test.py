import os
import subprocess

def getSBRoot():
    args = ["sbroot"]
    output = subprocess.Popen(args, stderr=subprocess.PIPE).communicate()
    result = output[1].decode("UTF-8")
    return result

if (__name__ == "__main__"):
    a = getSBRoot()
    print(a)
    os.system('setmwe ' + a)
    os.system('matlab/tools/share/stack_decoder.pl')

