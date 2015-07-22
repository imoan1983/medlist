# medlist
保険医療機関リスト作成

このスクリプトは [jp-hosplist-maker](https://github.com/hiromasah/jp-hosplist-maker) が保守されなくなったので引継いだものです。  
地方厚生局が公開している医療機関名簿のPDFを使いやすいtsvに変換します。

# 作者
川島 直美

##利用方法
###準備
* [python3.x](https://www.python.org/downloads/)
* [xpdf](http://www.foolabs.com/xpdf/download.html)
* [harelba/q](https://github.com/harelba/q) for check

###実行
* ダウンロード  
   ```
   $ python3 src/downloadFiles.py etc/urlList.tsc dl/
   ```  
    dl/yyyyMMdd/の下に厚生局ごとのフォルダを作成し、リンクされているPDFを全てダウンロードします。  
      
* 処理  
    ```
    $ python3 src/procFiels.py dl/yyyyMMdd
    ```  
    dl/yyyyMMddの下にあるPDFファイルを処理し、次の３つのtsvに変換します。
    * output/dir/data1.tsv : 施設概要
    * output/dir/data2.tsv : 病床
    * output/dir/data3.tsv : 届出
      
* 確認  
    ```
    $ python3 src/checkFiles.py output/yyyyMMdd
    ```  
    output/yyyyMMddの下にある処理済みファイルを集計します。
    * data1.tsv : 都道府県ごと・種別ごとの行数カウント, 空欄のチェック
    * data2.tsv : 都道府県ごと・種別ごとの病床数の総和, 空欄のチェック
    * data3.tsv : 都道府県ごと・種別ごとの行数カウント, 空欄のチェック  

##処理済みファイル
10日に1度、自動処理しています。(環境：ubuntu14)  
src/checkFiles.pyの結果にざっと目を通したものをreleaseしていきます。

###既知の問題
* 数施設、施設名や郵便番号に欠損があります。
* 栃木県の歯科の病床数に医科の病床数が混ざっています。

###地方厚生局WEBサイト
* [北海道厚生局](http://kouseikyoku.mhlw.go.jp/hokkaido/gyomu/gyomu/hoken_kikan/todokede_juri_ichiran.html)
* [東北厚生局](http://kouseikyoku.mhlw.go.jp/tohoku/gyomu/gyomu/hoken_kikan/itiran.html)
* 関東信越厚生局
    * [茨城県](http://kouseikyoku.mhlw.go.jp/kantoshinetsu/gyomu/bu_ka/ibaraki/)
    * [栃木県](http://kouseikyoku.mhlw.go.jp/kantoshinetsu/gyomu/bu_ka/tochigi/)
    * [群馬県](http://kouseikyoku.mhlw.go.jp/kantoshinetsu/gyomu/bu_ka/gunma/)
    * [千葉県](http://kouseikyoku.mhlw.go.jp/kantoshinetsu/gyomu/bu_ka/chiba/)
    * [埼玉県](http://kouseikyoku.mhlw.go.jp/kantoshinetsu/gyomu/bu_ka/shido_kansa/)
    * [東京都](http://kouseikyoku.mhlw.go.jp/kantoshinetsu/gyomu/bu_ka/tokyo/)
    * [神奈川県](http://kouseikyoku.mhlw.go.jp/kantoshinetsu/gyomu/bu_ka/kanagawa/)
    * [新潟県](http://kouseikyoku.mhlw.go.jp/kantoshinetsu/gyomu/bu_ka/niigata/)
    * [山梨県](http://kouseikyoku.mhlw.go.jp/kantoshinetsu/gyomu/bu_ka/yamanashi/)
    * [長野県](http://kouseikyoku.mhlw.go.jp/kantoshinetsu/gyomu/bu_ka/nagano/)
* [東海北陸厚生局](http://kouseikyoku.mhlw.go.jp/tokaihokuriku/gyomu/gyomu/hoken_kikan/shitei.html)
* [近畿厚生局](http://kouseikyoku.mhlw.go.jp/kinki/gyomu/gyomu/hoken_kikan/shitei_jokyo.html)
* [中国四国厚生局](http://kouseikyoku.mhlw.go.jp/chugokushikoku/chousaka/shisetsukijunjuri.html)
* [四国厚生支局](http://kouseikyoku.mhlw.go.jp/shikoku/gyomu/gyomu/hoken_kikan/shitei/)
* [九州厚生局](http://kouseikyoku.mhlw.go.jp/kyushu/gyomu/gyomu/hoken_kikan/)

#LICENSE
このリポジトリに含まれるコードはApache License 2.0に従って配布しています。
