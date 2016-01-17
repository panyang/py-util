import pcp

import sched, time
import sys

def myPCP(srcDir, dstDir):
    print("Enable my pcp at", time.time())
    print("Executing pcp", srcDir, '>', dstDir)
    (filesCopied, bytesCopied) = pcp.syncDir(srcDir, dstDir)
    kbC = bytesCopied/1024
    print("Total %d files, %d KB copied." % (filesCopied, kbC))

def repeat(fcn, src, dst, schedule):
    fcn(src, dst)
    schedule.enter(100, 1, repeat, (fcn, src, dst, schedule))

if (__name__ == "__main__"):
    if len(sys.argv) == 3:
        srcDir = sys.argv[1]
        dstDir = sys.argv[2]
    elif len(sys.argv) == 2:
        srcDir = os.getcwd()
        dstDir = sys.argv[1]
    else:
        print('Usage: backup [src directory] <dst directory>')
        sys.exit()
    
    a = sched.scheduler(time.time, time.sleep)
    a.enter(1, 1, repeat,(myPCP, srcDir, dstDir, a))
    a.run()
