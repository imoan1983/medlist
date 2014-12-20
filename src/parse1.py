# -*- coding: utf-8 -*-

import codecs
import re
import postal2pref

#parse 1 page
def parse1(txt):

        ret = {'todokede':False, 'pref':'00'}

        print('[parse1] %s' % txt)

        postal = ''

        try:

                fin = codecs.open(txt, 'r', 'utf-8')

                for line in fin:

                        if line.find('届出受理医療機関名簿') > -1:

                                ret['todokede'] = True

                        if line.find('項目別') > -1 or line.find('略称') > -1:

                                ret['todokede'] = False

                        #get prefectural code from postal code
                        elif re.search('〒\d\d\d-\d\d\d\d',line):

                                postal = re.search('〒\d\d\d-\d\d\d\d',line).group(0)

                                ret['pref'] = postal2pref.postal2pref(postal)

                                break

                fin.close()

                print('[parse1-ok] todokede:%s postal:%s pref:%s' % (ret['todokede'], postal, ret['pref']))

        except:

                print('[parse1-ng] postal:%s' % postal)

        return ret

def debug(argv):

        postal2pref.init('../etc/postal2pref.tsv')

        p1 = parse1('../txt1/test.txt')

        print(p1)

        return

if __name__ == "__main__":

        import sys
	
        debug(sys.argv)
