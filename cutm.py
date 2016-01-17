#!/bin/python

"""
 CUTM.PY Cuts a MATLAB function in old format into several m files.
"""

from string import *
from sys import *

def is_comment(line):
   # if a line starts with %, its a comment line
   s = line.lstrip()
   if len(s) == 0:
        return  True
   if s[0] == '%':
   	return True
   else:
	return False

def join_lines(lines):
   # if a line ends with ..., join the line with the next
   # and leave the next line empty
   for i in range(0,len(lines)):
      if not is_comment(lines[i]):
	 s = lines[i].rstrip()
	 k = i
	 while s[-3:] == '...':
	    k=k+1
	    n = lines[k].rstrip()
	    s =join([s[:-3], n])
	    lines[k] = '% moved by CUTM'
	 lines[i] = s
  return lines

def is_function(line):
    s = line.strip()
    p = s.split(' ')
    if p[0]=='function':
	r = join(p[1:len(p)])
	name = r.strip()
	func_name = name.split('=')
	if len(func_name) > 1:
		name = func_name[1].strip()
	else:
		name = func_name[0].strip() #no return arg
	func_name = name.split('(')
	return func_name[0].strip()    
    else:
	return 0
    

def write_file(lines, filename):
    fh = open(filename, 'w')
    for line in lines:
    	fh.write(line)
        if not line[-1:]=='\n':
        	fh.write('\n')
    fh.close()

def find_functionline(begin, lines):
    if len(lines) <= begin:
	    return len(lines)
    print 'begin: %i' %begin
    for i in range(begin,len(lines)):
	    print '%i: %s'% (i,lines[i])
	    if not is_comment(lines[i]):
		    print('not comment')
		    if is_function(lines[i]):
			    return(i)
	    
    return len(lines)

file = argv[1]
dstdir = argv[2]

fh = open(file)
lines = fh.readlines()
lines = join_lines(lines)
print(lines)

begin = 0
end = find_functionline(begin,lines)
while end< len(lines):
	print 'end: %i' %end
	begin = end
	end = find_functionline(begin+1, lines)
	print '%i - %i'% (begin, end)
	filename = join([dstdir, is_function(lines[begin]), '.m'],'')
	write_file(lines[begin:end-1], filename)
fh.close()

