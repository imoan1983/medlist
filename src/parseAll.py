# -*- coding: utf-8 -*-

import codecs
import re

def parseAll(txt, pref, out1, out2, out3):

        print('[parseAll] %s' % txt)

        fout1 = codecs.open(out1,'a','utf-8')

        fout2 = codecs.open(out2,'a','utf-8')

        fout3 = codecs.open(out3,'a','utf-8')

        page = 0

        lines = []

        items = {}
        items = initItems(items)

        fin = codecs.open(txt, 'r', 'utf-8')

        for line in fin:

                if line.find('<page') > -1:

                        page = page + 1

                elif line.find('</page>') > -1:

                        if len(lines) > 0:

                                #sort by coordinate
                                lines = sortItems(lines)

                                items = parseLines(lines, items, pref, fout1, fout2, fout3)

                                lines = []

                elif line.find('<word') > -1:

                        #pass like [沖縄県]
                        if re.search('[都|道|府|県]\]',line):

                                pass

                        #pass title
                        elif re.search('全医療機関出力|届出受理|電話番号',line):

                                pass

                        else:

                                lines.append(getItems(line,page))

        #last one
        if items['kouban'] != '':
        
                writeout(pref, items, fout1, fout2, fout3)

        fin.close()

        fout1.close()

        fout2.close()

        fout3.close()

        print('[parseAll-ok]')

        return

def parseLines(lines, items, pref, fout1, fout2, fout3):

        position = {}

        hs = ''

        for l in lines:

                if l['content'].find('作成') > -1:
                
                        pass

                #[平成yy年mm月dd日 医科|歯科|薬局]
                elif re.search('\[平成.+年',l['content']):

                        position['日付種別'] = l

                        hs = l['content']

                elif '日付種別' in position and position['日付種別']['yMax'] == l['yMax']:

                        hs = hs + l['content']
                       
                        if hs.strip().endswith(']'):

                                del position['日付種別']

                                if items['dateAndGroup'] == '':

                                        items['dateAndGroup'] = hs

                                elif hs != items['dateAndGroup']:

                                        writeout(pref, items, fout1, fout2, fout3)
                       
                                        items = initItems(items)

                                        items['dateAndGroup'] = hs

                #header1
                elif l['content'].find('医療機関所在地') > -1:

                        position['医療機関所在地'] = l

                #header2
                elif l['content'].find('項番') > -1:

                        position['項番'] = l

                #header3
                elif re.search('医療機関番号|医療機関名称|病床数|受理番号|算定開始年月日',l['content']) and '項番' in position and l['yMax'] == position['項番']['yMax']:

                        ii = re.findall('医療機関番号|医療機関名称|病床数|受理番号|算定開始年月日',l['content'])

                        position[ii[0]] = l
                      
                #pass other header 
                elif '項番' in position and l['yMax'] == position['項番']['yMax']:
                        pass

                elif len(position) == 7:

                        if position['算定開始年月日']['xMax'] <= l['xMin'] :
                                pass

                        #serial number
                        if l['xMax'] < (position['項番']['xMax'] + position['医療機関番号']['xMin']) / 2:

                                if items['kouban'] != '':

                                        writeout(pref, items, fout1, fout2, fout3)

                                        items = initItems(items)

                                items['kouban'] = l['content']

                                koubanHeight = l['yMax']

                        #number
                        elif position['項番']['xMax'] <= l['xMin'] and l['xMax'] <= position['医療機関番号']['xMax'] and koubanHeight == l['yMax']:

                                n = l['content'].replace(',','').replace('.','').replace('-','').replace(' ','').replace('\uff65','')

                                items['facilityId'] = items['facilityId'] + n

                        #name
                        elif position['医療機関番号']['xMax'] <= l['xMin'] and l['xMin'] <= position['医療機関名称']['xMin']:

                                items['facilityName'] = items['facilityName'] + l['content'].replace('\u2003','　')

                        #address
                        elif position['医療機関名称']['xMax'] <= l['xMin'] and l['xMin'] <= position['医療機関所在地']['xMax']:

                                cc = l['content'].replace('一般（感染）','aaa').replace('一般（特例）','bbb').replace('感\u2161','ccc').replace('療養（介護）','ddd').replace('療養（医療）','eee').replace('一般（複合）','fff')

                                #sometimes bed type after address
                                if re.search('(一般|感染|療養|結核|精神|介護|その他|特定|包括|伝染|診老入医管|老人|aaa|bbb|ccc|ddd|eee|fff)$',cc):

                                        ff = re.findall('(.+)(一般|感染|療養|結核|精神|介護|その他|特定|包括|伝染|診老入医管|老人|aaa|bbb|ccc|ddd|eee|fff)$',cc)

                                        tmp = ff[0][0]

                                        l['content'] = ff[0][1].replace('aaa','一般（感染）').replace('bbb','一般（特例）').replace('ccc','感\u2161').replace('ddd','療養（介護）').replace('eee','療養（医療）').replace('fff','一般（複合）').strip()

                                        l['content2'] = ''

                                        items['bedType'].append(l)

                                else:

                                        tmp = l['content']

                                #postal number
                                if re.search('〒[0-9]',tmp):

                                        items['postalNumber'] = tmp

                                #fax
                                elif tmp.strip().startswith('(') and tmp.strip().endswith(')'):

                                        items['fax'] = tmp

                                #phone
                                elif re.search('[0-9]',tmp):

                                        items['phone'] = tmp

                                #address
                                else:
                                        items['address'] = items['address'] + tmp.replace('\u2003','　')

                        #bed type
                        elif position['医療機関所在地']['xMax'] <= l['xMin'] and l['xMin'] <= position['病床数']['xMin']:

                                l['content2'] = ''

                                items['bedType'].append(l)

                        #number of bed or license
                        elif position['病床数']['xMin'] <= l['xMin'] and l['xMin'] <= position['受理番号']['xMin']:

                                #only number of bed
                                if l['content'].replace(',','').isdigit() == True:

                                        tmp1 = l['content']

                                        tmp2 = ''

                                #both number of bed and lincense
                                elif re.search('(^[0-9]{1,4})(.+)',l['content'].replace(',','')):

                                        ff = re.findall('([0-9]{1,4})(.+)',l['content'].replace(',',''))

                                        tmp1 = ff[0][0]

                                        tmp2 = ff[0][1]

                                #only license
                                else :

                                        tmp1 = ''

                                        tmp2 = l['content']


                                #number of bed
                                if tmp1 != '':

                                        flg = False

                                        #bed type exists
                                        for b in items['bedType']:

                                                if b['page'] == l['page'] and b['yMax'] == l['yMax']:

                                                        b['content2'] = tmp1

                                                        flg = True

                                                        break

                                        if flg == False:

                                                items['bedType'].append({'content':'','content2':tmp1,'page':l['page'],'yMax':l['yMax']})

                                #license
                                if tmp2 != '':

                                        items['licenceId'].append({'content':tmp2,'content2':'','page':l['page'],'yMax':l['yMax']})

                        #date of license
                        elif position['受理番号']['xMax'] <= l['xMin']:

                                for j in items['licenceId']:

                                        if j['page'] == l['page'] and j['yMax'] == l['yMax']:

                                                j['content2'] = j['content2'] + l['content']

                                                break

        return items

def writeout(pref, items, fout1, fout2, fout3):

        hs = re.findall('(平成.+年.+月.+日).*(医科|歯科|薬局)',items['dateAndGroup'][0:20])

        hs2 = hs[0][0] + '\t' + hs[0][1]

        fout1.write(('\t'.join([items['kouban'],hs2,pref + items['facilityId'],items['facilityName'],items['postalNumber'],items['address'],items['phone'],items['fax'],'\n'])))
        #print(('\t'.join([items['kouban'],hs2,pref + items['facilityId'],items['facilityName'],items['postalNumber'],items['address'],items['phone'],items['fax']])))

        for b in range(len(items['bedType'])):

                items['bedType'][b]['content'] = items['bedType'][b]['content'].replace('　','').replace(' ','').replace('\u2003','')
                items['bedType'][b]['content2'] = items['bedType'][b]['content2'].replace(',','')

                #!!!check unknown bed type later!!!
                if items['bedType'][b]['content'] == '' and \
                   b != 0 and \
                   items['bedType'][b - 1]['content2'] == '':

                        items['bedType'][b - 1]['content2'] = items['bedType'][b]['content2']

                        items['bedType'][b]['content2'] = ''
  
        for b in items['bedType']:

                if b['content2'] != '':

                        fout2.write('\t'.join([items['kouban'],hs2,pref + items['facilityId'],b['content'],b['content2'],'\n']))
                        #print('\t'.join([items['kouban'],hs2,pref + items['facilityId'],b['content'],b['content2']]))

        for j in items['licenceId']:

                #something after licenceId
                dd = re.findall('(.+年.+月.+日)(.*)',j['content2'])

                j['content2'] = dd[0][0]

                fout3.write('\t'.join([items['kouban'],hs2,pref + items['facilityId'],j['content'],j['content2'],'\n']))
                #print('\t'.join([items['kouban'],hs2,pref + items['facilityId'],j['content'],j['content2']]))

#init items
def initItems(items):

        if 'dateAndGroup' not in items:

                items['dateAndGroup'] = ''

        items['kouban'] = ''

        items['facilityId'] = ''

        items['facilityName'] = ''

        items['postalNumber'] = ''

        items['address'] = ''

        items['phone'] = ''

        items['fax'] = ''

        items['bedType'] = []

        items['licenceId'] = []

        return items

#sort by coordinates
def sortItems(items):

        l = len(items) - 1

        for i in range(l):

                for j in range(l, i, -1):

                        if items[j-1]['yMin'] > items[j]['yMin']:

                                temp = items[j]

                                items[j] = items[j-1]

                                items[j-1] = temp

        for i in range(l):

                for j in range(l, i, -1):

                        if items[j-1]['yMin'] == items[j]['yMin'] and items[j-1]['xMin'] > items[j]['xMin']:

                                temp = items[j]

                                items[j] = items[j-1]

                                items[j-1] = temp

        return items

#get coordinate and content
def getItems(line, page):

        ret = {}

        r = re.findall('<word xMin="(.+)" yMin="(.+)" xMax="(.+)" yMax="(.+)">(.+)</word>', line)

        ret['page'] = page

        ret['xMin'] = float(r[0][0])

        ret['yMin'] = float(r[0][1])

        ret['xMax'] = float(r[0][2])

        ret['yMax'] = float(r[0][3])

        ret['content'] = r[0][4]

        return ret

def debug(argv):

        p1 = parseAll('../txtAll/test.txt','01','a','b','c')

        return

if __name__ == "__main__":

        import sys
	
        debug(sys.argv)
