# -*- coding: utf-8 -*-

import os

def pdf2txt(pdf, txt, allPage, option):

    if allPage == True:

        os.system('pdftotext %s -enc UTF-8 %s %s ' % (option, pdf, txt))

    else:

        os.system('pdftotext %s -l 1 -enc UTF-8 %s %s ' % (option, pdf, txt))

    return

if __name__ == "__main__":

    import sys

    pdf2txt('../dl/20141220/01_hokkaido/juri-ika1-80.pdf','../txt1/test.txt',False, '-layout')
    pdf2txt('../dl/20141220/01_hokkaido/juri-ika1-80.pdf','../txtAll/test.txt',True, '-bbox')
