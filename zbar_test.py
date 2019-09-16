from pyzbar.pyzbar import decode
import cv2
import requests
import json
import pprint

def check_isbn(code_str):
    if '978' in code_str:
        return True
    else:
        False

def run():
    capture = cv2.VideoCapture(0)
    while True:
        ret,frame = capture.read()
        data = decode(frame)
        code = list(map(lambda x: x[0].decode('utf-8','ignore'),data))
        print(code)
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

def main():

    # openBD apiのurlの雛形
    api = 'https://api.openbd.jp/v1/get?isbn={isbn}'

    # 画像読み込み
    image = cv2.imread("img1.jpg")

    # バーコード変換
    data = decode(image)

    # 数字のみ取り出し
    code = list(map(lambda x: x[0].decode('utf-8','ignore'),data))

    # ISBNコードのみ取り出し
    isbn_code = list(map(lambda x: int(x),list(filter(check_isbn,code))))

    # urlを得る
    url = api.format(isbn=isbn_code[0])

    # OpenBDから書籍データ取得
    result = requests.get(url)

    #print(data[0][0].decode('utf-8','ignore'))

    # json形式でデコード
    data = json.loads(result.text)
    print(data[0]['onix']['DescriptiveDetail']['TitleDetail']['TitleElement']['TitleText']['content'])
    print(data[0]['onix']['DescriptiveDetail']['Collection'].keys())
    print(data[0]['onix']['DescriptiveDetail']['Contributor'])
    print(data[0]['onix']['CollateralDetail']['SupportingResource'][0]['ResourceVersion'][0]['ResourceLink'])

if __name__ == "__main__":
    #main()
    run()