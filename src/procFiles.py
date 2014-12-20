# -*- coding: utf-8 -*-

import sys
import os
import datetime
import re
import shutil
import postal2pref
import pdf2txt
import parse1
import parseAll

def main(argv):

    cd = os.path.abspath(os.path.dirname(__file__))
    cd = os.path.dirname(cd)

    postal2pref.init(os.path.join(cd, 'etc', 'postal2pref.tsv'))

    if len(argv) == 2:

        downloadDir = argv[1]

    else:

        f = open('win.ini')

        downloadDir = f.read()

        f.close()

    d = os.path.basename(downloadDir)

    print('make dirs======================================')
    dirTxt1 = os.path.join(cd, 'txt1', d)
    os.mkdir(dirTxt1)

    dirTxtAll = os.path.join(cd, 'txtAll', d)
    os.mkdir(dirTxtAll)

    dirParsed = os.path.join(cd, 'parsed', d)
    os.mkdir(dirParsed)

    dirOutput = os.path.join(cd, 'output', d)
    os.mkdir(dirOutput)

    for root,dirs,files in os.walk(downloadDir):
        
        for dir in dirs:

                os.mkdir(os.path.join(root,dir).replace('/dl/','/txt1/'))
                os.mkdir(os.path.join(root,dir).replace('/dl/','/txtAll/'))
                os.mkdir(os.path.join(root,dir).replace('/dl/','/parsed/'))

    print('pdf to txt(1)==================================')
    for root,dirs,files in os.walk(downloadDir):

        for file in files:

                fromF = os.path.join(root,file)
                toF = fromF.replace('/dl/','/txt1/').replace('.pdf','.txt')
                pdf2txt.pdf2txt(fromF, toF, False, '-layout')

    print('parse 1 & pdf to txt(all)======================')
    for root,dirs,files in os.walk(dirTxt1):

        for file in files:

            p = parse1.parse1(os.path.join(root,file))

            if p['todokede'] == True:

                #pdf to txt
                fromF = os.path.join(root,file).replace('txt1','dl').replace('.txt','.pdf')
                toF = os.path.join(root,file).replace('txt1','txtAll').replace('.txt','@@@%s.txt' % p['pref'])
                pdf2txt.pdf2txt(fromF, toF, True,'-bbox')

    print('parse all======================================')
    for root,dirs,files in os.walk(dirTxtAll):

        for file in files:

            pref = file[-6:-4]

            toF = os.path.join(root,file)

            out1 = toF.replace('txtAll','parsed').replace('.txt','_1.txt')

            out2 = toF.replace('txtAll','parsed').replace('.txt','_2.txt')

            out3 = toF.replace('txtAll','parsed').replace('.txt','_3.txt')

            parseAll.parseAll(toF, pref, out1, out2, out3)

    print('concatenate====================================')
    os.system('find %s -maxdepth 2 -mindepth 2 -name "*_1.txt" | xargs cat > %s' % (dirParsed, os.path.join(dirOutput,'data1.txt')))
    print('[cat] data1.txt')

    os.system('find %s -maxdepth 2 -mindepth 2 -name "*_2.txt" | xargs cat > %s' % (dirParsed, os.path.join(dirOutput,'data2.txt')))
    print('[cat] data2.txt')

    os.system('find %s -maxdepth 2 -mindepth 2 -name "*_3.txt" | xargs cat > %s' % (dirParsed, os.path.join(dirOutput,'data3.txt')))
    print('[cat] data3.txt')

    print('remove temporary files=========================')    
    shutil.rmtree(dirTxt1)
    print('[del] %s' % dirTxt1)

    shutil.rmtree(dirTxtAll)
    print('[del] %s' % dirTxtAll)

    shutil.rmtree(dirParsed)
    print('[del] %s' % dirParsed)

    return

def debug():

    try:
        a = 1 + "1"

    except:
        print(sys.exc_info())

if __name__ == "__main__":

    #python3 procfiles.py ../dl/yyyyMMdd  <- no last slash
    #date +"./dl/%Y%m%d" | xargs python3 procFiles.py
    main(sys.argv)
