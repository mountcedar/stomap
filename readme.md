# はじめに

このリポジトリは、11/8のはじめてのハッカソンにおいて作ったstomap関連のソースを共有するためのものです。

# 使い方

## Stomapウェブアプリのデモ画面を見るには

bar.htmlを適切なウェブブラウザで開いて下さい。

## 住所から緯度経度を取得する

```
./convert.py <jsonファイル>
```

を実行すると、指定したjsonファイルのadress属性を元に、緯度経度を求め、data.jsonに書き出します。
以下のファイルが入力ファイルです。

* zeubu.txt
* zenbu.json

## その他のスクリプト

* plot3d.py: 透過な単体３次元バーを描画して、pngに出力します
* convert_ver2.py: 一つ前のconvertスクリプト。対応する入力は以下のとおり
	* json
	* json.json
	* json.txt
* latlng.py: 緯度経度を求めるスクリプト（モジュール）
