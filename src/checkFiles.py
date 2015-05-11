
import os

def main(argv):

    outputDir = argv[1]

    data1 = os.path.join(outputDir,'data1.txt')
    data2 = os.path.join(outputDir,'data2.txt')
    data3 = os.path.join(outputDir,'data3.txt')

    print('*data1.txt')
    print('')
    
    print('summary')
    print('県\t医科\t歯科\t薬局\t他\t最小日付\t最大日付\t')
    print('----------------------------------------------------------')
    os.system('q -t " \
               SELECT C4/10000000, \
                      COUNT(CASE WHEN C3=\'医科\' THEN 1 ELSE NULL END), \
                      COUNT(CASE WHEN C3=\'歯科\' THEN 1 ELSE NULL END), \
                      COUNT(CASE WHEN C3=\'薬局\' THEN 1 ELSE NULL END), \
                      COUNT(CASE WHEN C3 NOT IN (\'医科\',\'歯科\',\'薬局\') THEN 1 ELSE NULL END) ,\
                      MIN(C2), \
                      MAX(C2) \
               FROM   %s \
               GROUP BY C4/10000000 \
               ORDER BY C4/10000000 \
               "' % data1)
    print('')

    print('blank @ C1-7')
    os.system('q -t " \
               SELECT * \
               FROM %s \
               WHERE C1 = \'\' OR C2 = \'\' OR C3 = \'\' OR C4 = \'\' OR C5 = \'\' OR C6 = \'\' OR C7 = \'\' \
               "' % data1)
    print('')

    print('*data2.txt')
    print('')
    
    print('summary')
    print('県\t医科\t歯科\t薬局\t他')
    print('-----------------------------------')
    os.system('q -t " \
               SELECT C4/10000000, \
                      SUM(CASE WHEN C3=\'医科\' THEN C6 ELSE 0 END), \
                      SUM(CASE WHEN C3=\'歯科\' THEN C6 ELSE 0 END), \
                      SUM(CASE WHEN C3=\'薬局\' THEN C6 ELSE 0 END), \
                      SUM(CASE WHEN C3 NOT IN (\'医科\',\'歯科\',\'薬局\') THEN C6 ELSE 0 END) \
               FROM   %s \
               GROUP BY C4/10000000 \
               ORDER BY C4/10000000 \
               "' % data2)
    print('')
    
    print('blank @ C1-C6')
    os.system('q -t " \
               SELECT * \
               FROM %s \
               WHERE C1 = \'\' OR C2 = \'\' OR C3 = \'\' OR C4 = \'\' OR C5 = \'\' OR C6 = \'\' \
               "' % data2)
    print('')

    print('*data3.txt')
    print('県\t医科\t歯科\t薬局\t他')
    print('-----------------------------------')
    os.system('q -t " \
               SELECT C4/10000000, \
                      COUNT(CASE WHEN C3=\'医科\' THEN 1 ELSE NULL END), \
                      COUNT(CASE WHEN C3=\'歯科\' THEN 1 ELSE NULL END), \
                      COUNT(CASE WHEN C3=\'薬局\' THEN 1 ELSE NULL END), \
                      COUNT(CASE WHEN C3 NOT IN (\'医科\',\'歯科\',\'薬局\') THEN 1 ELSE NULL END) \
               FROM   %s \
               GROUP BY C4/10000000 \
               ORDER BY C4/10000000 \
               "' % data3)
    print('')
    
    print('blank @ C1-C6')
    os.system('q -t " \
               SELECT * \
               FROM %s \
               WHERE C1 = \'\' OR C2 = \'\' OR C3 = \'\' OR C4 = \'\' OR C5 = \'\' OR C6 = \'\' \
               "' % data3)
    print('')


if __name__ == "__main__":

    import sys

    #python3 checkFiles.py ../output/yyyyMMdd
    main(sys.argv)
