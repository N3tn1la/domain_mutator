"""This module provides functionality for mutation domain names

TODO: rules like a hashcat
TODO: logging via logger
"""

import re

import argparse
from argparse import RawTextHelpFormatter

from itertools import combinations

connectors = ["", "-"]
common_words = ["test", "tst", "prod", "dev", "local", "service", "ru",]
switch_dict = {'a': ['4'], 't': ['7'], 'h': ['g'], 'g': ['h'], \
'for': ['4'], 'four': ['4'], 'y': ['i'], 'i': ['y'],'o':['0'],'0':['o']}


def add_connectors(domains, args):
    """Add connector-strings between domain symbols"""
    new_domains = []
    for connector in connectors:
        if connector == '':
            continue
        for domain in domains:
            for s in range(1, len(domain)):
                new_domains.append(domain[:s] + '-' + domain[s:])
    return new_domains


def add_common_words(domains, args):
    """Add common words from global list "common_words"
    as a prefix and suffix of domain devided by connector-strings"""
    new_domains = []
    for domain in domains:
        for word in common_words:
            for connector in connectors:
                new_domains.append(word+connector+domain)
                new_domains.append(domain+connector+word)
    return new_domains


def add_numbers(domains, args):
    """Just addmin number as a prefix and suffix of domain"""
    if args.numbercount is None:
        print("Module \"Add numbers\" is active, but there is no numbercount (-n). \
            Used default: 555")
        number = 555
    else:
        number = args.numbercount
    new_domains = []
    for domain in domains:
        for it in range(number+1):
            new_domains.append(domain+str(it))
            new_domains.append(str(it)+domain)
    return new_domains


def switch_symbols(domains, args):
    """Going through domains and dict, replace symbols that there is in "switch_dict" by regexp"""
    new_domains = []
    for domain in domains:
        for s in switch_dict.keys():
            if s in domain:
                p = re.compile(s)
                iterator = p.finditer(domain)
                iter_list = list(iterator)
                iter_len = len(iter_list)
                for k in range(1, iter_len+1):
                    temp = combinations(iter_list, k)
                    temp_list = list(temp)
                    for combs in temp_list:
                        word = domain
                        for comb in combs:
                            word = word[:comb.span()[0]] + \
                                switch_dict[s][0] + word[comb.span()[1]:]
                        new_domains.append(word)

    return new_domains


def parse_arg_list(domains: str):
    """Easy function to parse args like 1,2,3 or domain1,domain2"""
    return [x.strip() for x in domains.split(',')]


def out_to_console(domains: list):
    """Easy function to output in console"""
    for domain in domains:
        print(domain, sep=',')


def out_to_file(domains: list, filename: str):
    """Easy function to output in file"""
    try:
        with open(filename, "w") as file:
            for domain in domains:
                file.write(domain+"\n")
    except:
        print("Error output to the file", "Try output to console")
        out_to_console(domains)
        return -1
    return 1


def args_parser():
    """Parser of arguments"""
    parser = argparse.ArgumentParser(add_help=True, description='''
        Perform a mutation of domains

        Version: 1.0

        Usage example:

        python ./1.0.domain_mutator.py -t google,goo -m 1,3 -o ~/domains.txt -s .ru 
        ''', formatter_class=RawTextHelpFormatter)
    parser.add_argument("-t", '--target', dest='target', type=str, required=True,
                        help="Target domain, domains for analisys (asd,asdf,asdfg). \
    WITHOUT TOP LEVEL! (.ru/...)")
    parser.add_argument("-m", '--modules', dest='modules', type=str, required=True, \
        help="MODULES (-m 1,2,3):\n\
        1)Add connectors between switch_symbols (abc,a-bc,ab-c,a-b-c)\n\
        2)Add common words (testabc,test-abc,abc-test,abctest)\n\
        3)Add number (1a,2a,3a,a1,a2,a3)\n\
        4)Switching (abcg,4bcg,abch,4bch) (not stable)\n")
    parser.add_argument("-sw", '--switching', action='store_const', dest='switching', default=False,
                        const=True, help="Switching mode, after all previous modules\n(not stable)")
    parser.add_argument("-n", '--numbercount', dest='numbercount', type=int,
                        help="Numbers should be append to domain (10 = a1,a2,a3,..,a10)")
    parser.add_argument("-s", '--suffix', dest='suffix',
                        type=str, help="Suffix for")
    parser.add_argument("-o", '--output', dest='output',
                        type=str, help="Output file path")
    return parser.parse_args()


modules_dict = {'1': add_connectors, '2': add_common_words,
                '3': add_numbers, '4': switch_symbols, }

if __name__ == "__main__":
    domains_list = []
    modules = []

    args_parsed = args_parser()
    domains_list.extend(parse_arg_list(args_parsed.target))
    modules.extend(parse_arg_list(args_parsed.modules))

    modules.sort(reverse=True)

    for module in modules:
        domains_list.extend(modules_dict[module](domains_list, args_parsed))

    if args_parsed.switching is not None:
        if args_parsed.switching:
            for i in range(2):
                domains_list.extend(set(switch_symbols(domains_list, args_parsed)))
            domains_list = set(domains_list)

    if args_parsed.suffix is not None:
        print(f"Append {args_parsed.suffix}")
        for domain_id in range(len(domains_list)):
            domains_list[domain_id] += args_parsed.suffix

    if args_parsed.output is not None:
        out_to_file(domains_list, args_parsed.output)
    else:
        out_to_console(domains_list)
