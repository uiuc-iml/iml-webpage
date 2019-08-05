#!/usr/bin/python
import datetime
import sys
import os

current_working_directory = ""

#predefined functions
def include(fn):
    global current_working_directory
    fullpath = os.path.join(current_working_directory,fn)
    f = open(fullpath,'r')
    str = f.read().replace('\r\n','\n')
    f.close()
    
    oldcwd = current_working_directory
    current_working_directory = os.path.dirname(fullpath)
    res = run_pycgi(str)
    current_working_directory = oldcwd
    return res

def cleanpy(s):
    if s.count('</python>') != 0:
        print 'Warning: </python> tag encountered without corresponding <python> opening tag\n'
        s = s.replace('</python>','')
    return s

def run_pycgi(contents):
    segs = contents.split('<python>')
    output = cleanpy(segs[0])
    for subseg in segs[1:]:
        pos = subseg.find('</python>')
        cmd = subseg[0:pos]
        #print 'Evaluating...\n"""',cmd,'"""\n'
        try:
            s = eval(cmd)
            output = output+s
        except:
            #print 'Error encountered during evaluation\n'
            #print sys.exc_type, ":", sys.exc_value
            #print 'Trying exec...'
            try:
                exec(cmd,globals(),globals())
            except:
                print 'Neither eval() or exec() worked...\n'
                print sys.exc_type, ":", sys.exc_value
                print cmd
                quit()

        output = output + cleanpy(subseg[pos+9:])
    return output

if __name__=='__main__':
    framefile = sys.argv[1]
    outfile = sys.argv[-1]

    print "Processing",framefile
    output = include(framefile)

    #print output
    print "Outputting to",outfile
    f = open(outfile,'w')
    f.write(output)
    f.close()

