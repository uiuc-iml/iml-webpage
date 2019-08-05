import sys

f = open(sys.argv[1],'r')
for line in f.readlines():
    line = line.strip()
    line = line.replace('"',"'")
    if len(line) > 0:
        print 'document.write("'+line+'")'
