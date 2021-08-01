# unbound-trustpositive
process [trustpositif](http://trustpositif.kominfo.go.id) blacklist file into unbound recursive DNS server configuration. this script uses Python 3 
```
usage: ./generate-config.py -f|--infile domains-file
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
 NOTE: first strategy's output configuration will render unbound to use much
       more memory. 
```
## how to use

1. clone the repository

```
    $ git clone https://github.com/benben159/unbound-trustpositive
    $ cd unbound-trustpositive
```

1. create virtualenv on the directory and activate it (NOTE: replace `virtualenv3` command with appropriate command)

```
    $ virtualenv3 .
    $ source bin/activate
```

1. install required dependency using `pip`

```
    $ pip install -r requirements.txt
```

1. download the blacklist file

```
    $ wget -O domains https://trustpositif.kominfo.go.id/assets/db/domains
```

1. process the downloaded file using `generate-config.py` script

```
    $ ./generate-config.py -f domains
```

for more information, see `./generate-config.py --help`

## todo

* this program still depends on *NIX string manipulation utilities, such as `cat`, `sort`, and `uniq`. Actually it is good because that is the way we reuse existing apps on the OS and hopefully will reduce the amount of memory used in this program

* the format of the `domains` file from trustpositif Kominfo is unpredictable, so there is a *big* chance for this program to fail
