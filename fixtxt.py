#!/bin/python

from string import *
from sys import *

import io
import re

def read_titles(filename):
    fh = io.open(filename, 'r', 1, "UTF-8")
    lines= fh.readlines()
    title_var = []
    for i in range(len(lines)):
        title_var.append(lines[i].rstrip())
    return title_var

def write_file(lines, filename):
    fh = io.open(filename, 'w', 1, "UTF-8")
    for line in lines:
        if (line != None):
            fh.write(line)
            if not line[-1:]=='\n':
                fh.write('\n')
        else:
            fh.write('\n')
    fh.close()

def is_line(lead):
    return re.match("[0-9]+:[0-9]+", lead)

def is_title_1(lead):
    global title_1
    lead_stripped = lead.rstrip()
    for number in title_1:
        if number == lead_stripped:
            return True
    return False

def is_title_2(lead):
    global title_2
    lead_stripped = lead.rstrip()
    for number in title_2:
        if number == lead_stripped:
            return True
    return False

def is_title_3(lead):
    global title_3
    lead_stripped = lead.rstrip()
    for number in title_3:
        if number == lead_stripped:
            return True
    return False
def is_title_4(lead):
    global title_4
    lead_stripped = lead.rstrip()
    for number in title_4:
        if number == lead_stripped:
            return True
    return False

def is_title_5(lead):
    global title_5
    lead_stripped = lead.rstrip()
    for number in title_5:
        if number == lead_stripped:
            return True
    return False


def process_line(line, number):
    parts = re.split("\t", line,1)
    lead = parts[0]
    if is_title_1(lead):
       #print('title 1 at line: ', number)
       line = "\t".join(parts)
       line = "<h1>" + line+ "</h1>"
       return line
    elif is_title_2(lead):
       #print('title 2 at line: ', number)
       line = lead
       line = "<h2>" + line+ "</h2>"
       return line
    elif is_title_3(lead):
       #print('title 3 at line: ', number)
       line = "\t".join(parts)
       line = "<h3>" + line+ "</h3>"
       return line
    elif is_title_4(lead):
       #print('title 4 at line: ', number)
       line = "\t".join(parts)
       line = "<h4>" + line+ "</h4>"
       return line
    elif is_title_3(lead):
       #print('title 5 at line: ', number)
       line = "\t".join(parts)
       line = "<h5>" + line+ "</h5>"
       return line
    elif is_line(lead):
       parts[1] = re.sub("[0-9]+", "", parts[1])
       line = "\t".join(parts)
       line = "<p>" + line + "</p>"
       return line

if (__name__ == "__main__"):
    file = argv[1]
    newfile = argv[2]
    # Read titles
    title_1 = read_titles('title_1.txt')
    title_2 = read_titles('title_2.txt')
    title_3 = read_titles('title_3.txt')
    title_4 = read_titles('title_4.txt')
    title_5 = read_titles('title_5.txt')
    
    fh = io.open(file, 'r', 1, "UTF-8")
    lines = fh.readlines()
    new_lines = []
    line_number = 0
    for line in lines:
        line_number = line_number +1
        new_lines.append(process_line(line.strip(), line_number))

    write_file(new_lines, newfile)
