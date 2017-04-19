#!/usr/bin/env python3

## this script process trust+ domain blacklist file into configuration files for unbound
## TODO: multithreading, checking if unbound is installed
import sys
import subprocess
import shlex
import tempfile
import os
import getopt
import tldextract
import ipaddress
def usage():
    sys.stderr.write("""usage: {} -f|--infile domains-file
  -f|--infile         input file from trustpositif.kominfo.go.id (mandatory)
  -d|--output-dir     set directory for output configuration files 
                      (default: subdirectory `outdir` of current directory)
  -r|--redirect-addr  set redirect address (default: 127.0.1.1)
  -v|--verbose        verbose output (will create a bunch of output, default is
                      silent and just print simple progress)
  -s|--strategy       set configuration build strategy:
                        1: for each domain that should be blocked with 
                           any of its unlisted subdomains, create a local-zone
                           with redirect directive
                        2: create a '.' local-zone with transparent directive 
                           (default)
 NOTE: first strategy's output configuration will render unbound to use much more
       memory. 
""".format(sys.argv[0]))
    exit(1)

domain_groups = {}
redir_ip = "127.0.1.1"
outdir = os.path.realpath('outdir')
infile = None
verbose = False
strategy = 2
## TODO use getopt
#if len(sys.argv) == 1:
#    sys.stderr.write("usage: {} domains-file <output-conf-dir> <redirect-address>\n".format(sys.argv[0]))
#    exit(1)
#else:
#    if not os.path.isfile(os.path.realpath(sys.argv[1])):
#        sys.stderr.write("input file doesn't exists\n")
#        exit(1)
#    if len(sys.argv) == 3:
#        outdir = os.path.realpath(sys.argv[2])
#    if not os.path.isdir(outdir):
#        sys.stderr.write("output conf dir doesn't exists. creating it\n")
#        os.mkdir(outdir)
#    if len(sys.argv) == 4:
#        redir_ip = sys.argv[3]

## argument processing ##
if len(sys.argv) == 1:
    usage()
try:
    opts, args = getopt.getopt(sys.argv[1:], "vf:d:r:s:", ["infile", "output-dir", "redirect-addr", "verbose","strategy"])
    for opt, arg in opts:
        if opt in ('-h', '--help', '--usage'):
            usage()
        if opt in ('-f', '--infile'): 
            if not os.path.isfile(os.path.realpath(arg)):
                sys.stderr.write("input file doesn't exists\n")
                exit(1)
            else:
                infile = os.path.realpath(arg)
        if opt in ('-d', '--output-dir'):
            outdir = os.path.realpath(arg)
        if opt in ('-r', '--redirect-addr'):
            redir_ip = arg
        if opt in ('-v', '--verbose'):
            verbose = True
        if opt in ('-s', '--strategy'):
            strategy = int(arg)
    if not os.path.isdir(outdir):
        sys.stderr.write("output conf dir doesn't exists. creating it\n")
        os.mkdir(outdir)
except getopt.GetoptError as ge:
    sys.stderr.print("option error"+ str(ge) + '\n')
    usage()

## input file cleanup ##
cmdline = shlex.split("sed -e 's/\\r//; /^\*\./d' {} ".format(infile))
cmdout = tempfile.mkstemp()
try:
    cmd0 = subprocess.Popen(cmdline, stdout=subprocess.PIPE)
    cmd1 = subprocess.Popen(["sort"], stdin=cmd0.stdout, stdout=subprocess.PIPE)
    cmd2 = subprocess.Popen(["uniq"], stdin=cmd1.stdout, stdout=cmdout[0])
    cmd0.wait()
    cmd1.wait()
    cmd2.wait()
except OSError as oe:
    sys.stderr.write("an error occurred: " + str(oe) + '\n')
    exit(1)
#except Exception as ee:
#    sys.stderr.write(str(ee) + '\n')
#    exit(1)
h = open(os.path.join(outdir, "ipaddress.txt"), 'w')
with open(cmdout[1], 'r') as infile:
    progres = []
    for line in infile:
        line = line.strip()
        p = line[0]
        if p not in progres:
            print(p + ', ', end='')
            progres.append(p)
        try:
            _ = ipaddress.ip_address(line)
            h.write(line + '\n')
            continue
        except ValueError:
            pass
        line_dom = tldextract.extract(line)
        if line_dom.registered_domain not in domain_groups.keys():
            _ = (verbose and print("create dom grp", line_dom.registered_domain) or None)
            domain_groups[line_dom.registered_domain] = []
        domain_groups[line_dom.registered_domain].append(line)
        _ = (verbose and print("add to grp", line) or None)
    del progres
h.close()
os.remove(cmdout[1])
print("writing configuration...", end='')
g = open(os.path.join(outdir, "unique_domains.conf"),'w')
if strategy == 2:
    g.write('local-zone: "." transparent\n')
for k, v in domain_groups.items():
    if len(v) == 1:
        if strategy == 1:
            g.write('local-zone: "' + v[0] + '" redirect\n')
        g.write('local-data: "' + v[0] + ' IN A ' + redir_ip + '"\n')
    else:
        _ = (verbose and print("create {}.conf".format(k)) or None)
        h = open(os.path.join(outdir, '{}.conf'.format(k)),'w')
        h.write('local-zone: "' + k + '" transparent\n')
        for d in domain_groups[k]:
            h.write('local-data: "' + d + ' IN A ' + redir_ip + '"\n')
        h.close()
g.close()
print("done")
#_ = [print(d) for d in ip_addrs]
#for k,v in domain_groups:
#    print("{} subdoms:")
#    for e in v:
#        print(e)

