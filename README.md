# Book Collection Manager

## 目標
蔵書のデータベース化と保管場所の記録・管理の自動化

## ロードマップ
1. ISBNから書籍データの自動取得
1. カメラ画像からのデータベースへの書籍データ自動登録
1. 蔵書検索機能などの追加
1. Flask等によるWebアプリケーション化
1. 保管場所の登録機能の追加
1. 保管場所の移動などへの対応
1. GCPなどを利用したクラウド化


## Dependent
* pyzbar
* OpenCV
* Numpy

## Install
* Install pyzar
```
pip install pyzbar
```
* Install opencv
```
pip install opencv-python
```
or
```
conda install opencv
```

 ## Issue
 * 書籍データが取れなかった際の処理をどうするか
    * 当面は何も処理をしない
    * 将来的には他のAPIで情報を補完する