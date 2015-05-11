  os.system('q -t "SELECT DISTINCT * FROM ./*/data1.txt where substr(c2,1,7)='平成27年1月' order by c4" >data2701.txt')
  
  os.system('  q -t \
    "SELECT DISTINCT c4/10000000,count(*),\
     COUNT(CASE WHEN C3='医科' THEN 1 ELSE NULL END),\
     COUNT(CASE WHEN C3='歯科' THEN 1 ELSE NULL END),\
     COUNT(CASE WHEN C3='薬局' THEN 1 ELSE NULL END),\
     COUNT(CASE WHEN C3 NOT IN ('医科','歯科','薬局')\
      THEN 1 ELSE NULL END) FROM ./data2612.txt group by C4/10000000 " )
