from http.client import HTTPConnection
from html.parser import HTMLParser
import sys

# Use stagger to manipulate id3
import stagger
from stagger.id3 import *

""" A small utility that retrieve lyrics from LyricWiki.org """
class LyricWikiParser (HTMLParser):
  def __init__(self):
    HTMLParser.__init__(self)
    self.reset()

  def reset(self):
    HTMLParser.reset(self)
    self.content = []
    self.inLyricBox = False;
    self.data = ""
    self.stack = []
    

  def error(self, message):
    print("error found")
                 

  def handle_starttag(self, tag, attrs):
    if tag == "br":
      # nothing
      return
    if len(self.stack)>1:    
      lastentry = self.stack[-1]
      last_tag = lastentry[0]
      last_attrs = lastentry[1]
    else:
      last_tag = ''
      last_attrs = {}
    # Entering a new environment
    attr_dict = dict(attrs)
    self.stack.append( (tag, attr_dict) )
    if not self.inLyricBox:
        if tag == "div" and "class" in attr_dict and \
          attr_dict["class"] == "lyricbox":
            # print("Start saving data")
            self.inLyricBox = True
    else:
      # Entering another
      # print("Enter another tag %s" % tag)
      self.inLyricBox = False
  
  def handle_startendtag(self, tag, attrs):
    if self.inLyricBox:
      self.content.append(self.data)
      self.data = ""
    else:
      return
    
  def handle_endtag(self, tag):
    if tag == "br":
        return
    thisentry = self.stack.pop()
    this_tag = thisentry[0]
    this_attrs = thisentry[1]
    if len(self.stack)>1:
      lastentry = self.stack[-1]
      last_tag = lastentry[0]
      last_attrs = lastentry[1]
    else:
      last_tag = ''
      last_attrs = dict()
    
    if this_tag == "div" and "class" in this_attrs \
       and this_attrs["class"] == "lyricbox":
      # Return from the lyricbox scope
      # print("End saving data")
      self.inLyricBox = False
      self.content.append(self.data)
      self.data = ""
    elif last_tag == "div" and "class" in last_attrs \
         and last_attrs["class"] == "lyricbox":
      # Return to the lyricbox scope
      # print("Re-enter scope from %s" % tag)
      self.inLyricBox = True
    else:
      self.inLyricBox = False
      
  def handle_charref(self, name):
    if self.inLyricBox:
        if name.isdigit():
          c = chr(int(name))
          a = c.encode('ascii', 'ignore')
          self.data += a.decode('ascii')
        else:
          print(name)
    
  def handle_data(self,data):
    if self.inLyricBox:
      self.data = self.data + data
      
# Read html response from LyricWiki.org
class LyricWikiReader:
    def __init__(self):
        self.site = "lyrics.wikia.com"
        self.param = "/%s:%s"
        self.connection = HTTPConnection(self.site)
        
    def getLyrics(self, artist, song):
        full_url = self.param % (artist, song)
        self.connection.request("GET", full_url)
        response = self.connection.getresponse()
        data = response.read()
        s = data.decode("UTF-8", "ignore")
        p = LyricWikiParser()
        
        p.feed(s)
        
        return p.content
      
def printLines(lines):
  for l in lines:
    print(l)

def getLyrics(artist, song):
  reader = LyricWikiReader()
  lines = reader.getLyrics(artist, song)
  return '\n'.join(lines)

def deblank(s):
  return s.replace(" ", "_")

def updateFile(filename):
  tag = stagger.read_tag(filename)
  artist = deblank(tag.artist)
  title = deblank(tag.title)
  lines = getLyrics(artist, title)

  # Create a lyrics object
  if len(lines) > 1:
    l = stagger.id3.USLT()
    l.encoding = 0
    l.lang = "eng"
    l.text = lines
    tag[USLT]=[l]
    tag.write()
    print("Lyrics updated!")
  else:
    print("Lyrics cannot be found")
  
  
   
if (__name__ == "__main__"):
  if len(sys.argv) == 2:
    updateFile(sys.argv[1])
  else:
    print("Usage readlyrics 1.mp3")
