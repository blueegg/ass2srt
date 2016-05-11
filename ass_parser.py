#!/bin/python

import ass
import sys
import codecs
import re

def time_string(time):
    seconds = time.seconds
    microseconds = time.microseconds
    
    mm, ss = divmod(seconds, 60)
    hh, mm = divmod(mm, 60)
    s = "%02d:%02d:%02d,%03d" % (hh, mm, ss, microseconds / 1000)
    
    return s
    
def ass_parser(filename):
    f = codecs.open(filename, 'r', 'utf8')
    doc = ass.parse(f)
    f.close()
        
    print("length of event is: {}".format(len(doc.events)))
    
    doc.events.sort(key=lambda x:x.start)
    for event in doc.events:
        event.text = re.sub("{.*?}", "", event.text).replace("\\N", "\n")
    
    srtname = filename[:-3] + 'srt'
    f = codecs.open(srtname, 'w', 'utf8')
    
    for index, event in enumerate(doc.events):
        f.write("%d\n"%(index + 1))
        f.write("%s --> %s\n" % (time_string(event.start), time_string(event.end)))
        f.write(event.text)
        f.write("\n\n")
        
    f.close()
    
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: ass_parser.py filename")
    else:
        ass_parser(sys.argv[1])