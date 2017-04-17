#!/usr/bin/env python3

## this script process trust+ domain blacklist file into configuration files for unbound
## TODO: multithreading, checking if unbound is installed
import sys, subprocess, shlex, tempfile, os
import tldextract
import ipaddress

ip_addrs = []
unique_domains = []
subdomain_groups = {}
redir_ip = "127.0.1.1"
outdir = os.path.realpath('outdir')

## TODO use getopt
if len(sys.argv) == 1:
    sys.stderr.write("usage: {} domains-file <output-conf-dir> <redirect-address>\n".format(sys.argv[0]))
    exit(1)
else:
    if not os.path.isfile(os.path.realpath(sys.argv[1])):
        sys.stderr.write("input file doesn't exists\n")
        exit(1)
    if len(sys.argv) == 3:
        outdir = os.path.realpath(sys.argv[2])
    if not os.path.isdir(outdir):
        sys.stderr.write("output conf dir doesn't exists. creating it\n")
        os.mkdir(outdir)
    if len(sys.argv) == 4:
        redir_ip = sys.argv[3]

cmdline = shlex.split("sed -e 's/\\r//; /^\*\./d' {} ".format(sys.argv[1]))
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
with open(cmdout[1], 'r') as infile:
    progres = []
    for line in infile:
        line = line.strip()
        p = line[0]
        if p not in progres:
            print(p)
            progres.append(p)
        try:
            _ = ipaddress.ip_address(line)
            ip_addrs.append(line)
            continue
        except ValueError:
            pass
        line_dom = tldextract.extract(line)
        # uncomment the print statements below this blocks to do some debugging
        # WARNING: will generate a big f**king bunch of output
        if line_dom.registered_domain not in unique_domains and \
           line_dom.registered_domain not in subdomain_groups.keys():
            unique_domains.append(line_dom.registered_domain)
            #print(line_dom.registered_domain + " unique")
        else:
            if line_dom.registered_domain in unique_domains:
                unique_domains.remove(line_dom.registered_domain)
                #print("create dom grp", line_dom.registered_domain)
                subdomain_groups[line_dom.registered_domain] = []
            subdomain_groups[line_dom.registered_domain].append(line)
            #print("add to grp", line)
os.remove(cmdout[1])
g = open(os.path.join(outdir, "unique_domains.conf"),'w')
for d in unique_domains:
    g.write('local-zone: "' + d + '" redirect\n')
    g.write('local-data: "' + d + ' IN A ' + redir_ip + '"\n')

for k in subdomain_groups.keys():
    h = open(os.path.join(outdir, '{}.conf'.format(k)),'w')
    h.write('local-zone: "' + k + '" transparent\n')
    for d in subdomain_groups[k]:
        h.write('local-data: "' + d + ' IN A ' + redir_ip + '"\n')
    h.close()
h = open(os.path.join(outdir, "ipaddress.txt"), 'w')
_ = [h.write(ip + '\n') for ip in ip_addrs]
h.close()
g.close()
#_ = [print(d) for d in unique_domains]
#_ = [print(d) for d in ip_addrs]
#for k,v in subdomain_groups:
#    print("{} subdoms:")
#    for e in v:
#        print(e)

