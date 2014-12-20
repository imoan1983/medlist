# -*- coding: utf_8 -*-

import re

pp = []

#get prefectual code from postal code
#for only capital city
def postal2pref(postal):

        pref = '00'

        global pp

        for p in pp:

                if re.search(p['postal_code'],postal):

                        pref = p['prefectural_code']

                        break

        return pref

#init postal code & prefectural code table
#pp = postal_code, prefectural_code
def init(config):

        import csv
        import codecs

        global pp

        pp = []

        f = codecs.open(config,'r',encoding='utf-8')

        fin = csv.reader(f, delimiter='\t')

        header = next(fin)

        for row in fin:

                pp.append({header[0]:row[0],header[1]:row[1]})

        return

def debug(argv):

        init('../etc/postal2pref.tsv')

        print(postal2pref('〒163-8001')) #tokyo metroporlitan office --> prefectual code = 13

        return

if __name__ == "__main__":

        import sys

        debug(sys.argv)
