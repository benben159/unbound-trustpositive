# unbound-trustpositive
process trustpositive blacklist file into unbound configuration

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
