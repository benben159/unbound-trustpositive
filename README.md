# unbound-trustpositive
process trustpositive blacklist file into unbound configuration. this script uses Python 3 

## how to use

1. clone the repository

```
    $ git clone https://github.com/benben159/unbound-trustpositive
    $ cd unbound-trustpositive
```

2. download the blacklist file

```
    $ wget -O domains http://trustpositif.kominfo.go.id/files/downloads/index.php?dir=database%2Fblacklist%2Fpengaduan%2F\&download=domains
```

3. process the downloaded file using `process-trust+domains.py` script

```
    $ ./process-trust+domains.py -f domains
```

for more information, see `./process-trust+domains.py --help`

## dependency preparation

this python script requires `tldextract` module. you can use `pip` to install
the module with `pip3 install tldextract`. if you install the module without
virtualenv or such thing, you must prepare the module with this terminal commands:

```
    $ sudo python3
    ### this will run python3 with root privilege, which is not recommended.
    ### but the bug is in tldextract module
    >>> import tldextract
    >>> tldextract.extract('www.google.com') # <-- this will initialize top-level domain list in the module directory
```

