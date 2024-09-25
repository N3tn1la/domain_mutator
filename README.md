# domain_mutator
This module provides functionality for mutation domain names

### Usage

```
python ./1.0.domain_mutator.py -t google,goo -m 1,3 -o ~/domains.txt

gobuster dns -w ~/domains.txt -d ru -t 400
```

### TODO
1. rules like a hashcat
2. logging via logger

### HELP
```
└─$ python ./1.0.Domain_mutator.py -t google,goo -m 1,3 -o ~/domains.txt -s .ru -h
usage: 1.0.Domain_mutator.py [-h] -t TARGET -m MODULES [-sw] [-n NUMBERCOUNT] [-s SUFFIX] [-o OUTPUT]

        Perform a mutation of domains

        Version: 1.0

        Usage example:

        python ./1.0.Domain_mutator.py -t google,goo -m 1,3 -o ~/domains.txt -s .ru 
        

options:
  -h, --help            show this help message and exit
  -t TARGET, --target TARGET
                        Target domain, domains for analisys (asd,asdf,asdfg). WITHOUT TOP LEVEL! (.ru/...)
  -m MODULES, --modules MODULES
                        MODULES (-m 1,2,3):
                                1)Add connectors between switch_symbols (abc,a-bc,ab-c,a-b-c)
                                2)Add common words (testabc,test-abc,abc-test,abctest)
                                3)Add number (1a,2a,3a,a1,a2,a3)
                                4)Switching (abcg,4bcg,abch,4bch) (not stable)
  -sw, --switching      Switching mode, after all previous modules
                        (not stable)
  -n NUMBERCOUNT, --numbercount NUMBERCOUNT
                        Numbers should be append to domain (10 = a1,a2,a3,..,a10)
  -s SUFFIX, --suffix SUFFIX
                        Suffix for
  -o OUTPUT, --output OUTPUT
                        Output file path
```
