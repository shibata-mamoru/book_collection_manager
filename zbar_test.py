from pyzbar.pyzbar import decode
import cv2
import requests
import json
import numpy as np
from PIL import ImageFont, ImageDraw, Image

def check_isbn(code_str):
    '''ISBNコードである整数文字列ならTrueを返す関数'''
    if '978' in code_str[0]:
        return True
    else:
        False

def get_bookdata_openbd(isbn_code):
    '''ISBNコードの整数を入力としてOpenBD APIから帰ってきたjsonデータを返す関数'''
    api = 'https://api.openbd.jp/v1/get?isbn={isbn}'
    url = api.format(isbn=isbn_code)
    result = requests.get(url)
    json_data = result.text

    return json_data

def get_bookdata_rakuten(isbn_code):
    '''ISBNコードの整数を入力としてRakuten APIから帰ってきたjsonデータを返す関数'''
    api = 'https://app.rakuten.co.jp/services/api/BooksTotal/Search/20170404?format=json&isbnjan={isbn}&applicationId=1088097277669615348'
    url = api.format(isbn=isbn_code)
    result = requests.get(url)
    json_data = result.text

    return json_data

def get_thumbnail(thumbnail_url):
    '''OpenBDのサムネイルURLからjpeg画像を取得し，OpenCV形式で返す関数'''
    thumbnail_data = requests.get(thumbnail_url)
    arr = np.frombuffer(thumbnail_data.content,np.uint8)
    img = cv2.imdecode(arr,cv2.IMREAD_UNCHANGED)

    return img

def convert_text(text,img):
    fontpath = 'YuGothM.ttc'
    font = ImageFont.truetype(fontpath, 25)
    img_pil = Image.fromarray(img)
    draw = ImageDraw.Draw(img_pil)
    position = (10, 300)
    b,g,r,a = 0,255,0,0
    draw.text(position, text, font = font , fill = (b, g, r, a) )
    text_img_array = np.array(img_pil)
    return text_img_array

def run():
    capture = cv2.VideoCapture(0)
    while True:
        ret,frame = capture.read()
        data = decode(frame)
        code = list(map(lambda x: [x[0].decode('utf-8','ignore'),x[2]],data))
        
        isbn_code_temp = list(map(lambda x: {'isbn':int(x[0]),'pos':x[1]},list(filter(check_isbn,code))))
        if isbn_code_temp and len(isbn_code_temp) == 1:
            isbn_code = isbn_code_temp[0]
            cv2.rectangle(frame,(isbn_code['pos'][0],isbn_code['pos'][1]),(isbn_code['pos'][0]+isbn_code['pos'][2],isbn_code['pos'][1]+isbn_code['pos'][3]),(0,0,255))
            json_data = get_bookdata_openbd(isbn_code['isbn'])
            book_data = json.loads(json_data)
            if book_data[0]:
                    if 'SupportingResource'  in book_data[0]['onix']['CollateralDetail'].keys():
                        thumbnail_url = book_data[0]['onix']['CollateralDetail']['SupportingResource'][0]['ResourceVersion'][0]['ResourceLink']
                        thumbnail_img = get_thumbnail(thumbnail_url)
                        title = book_data[0]['onix']['DescriptiveDetail']['TitleDetail']['TitleElement']['TitleText']['content']
                        frame[0:thumbnail_img.shape[0],0:thumbnail_img.shape[1]] = thumbnail_img
                        frame = convert_text(title,frame)
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    json_data = get_bookdata_openbd(isbn_code['isbn'])

    book_data = json.loads(json_data)
    print(book_data[0]['onix']['DescriptiveDetail']['TitleDetail']['TitleElement']['TitleText']['content'])
    print(book_data[0]['onix']['DescriptiveDetail']['Collection'].keys())
    print(book_data[0]['onix']['DescriptiveDetail']['Contributor'])
    print(book_data[0]['onix']['CollateralDetail']['SupportingResource'][0]['ResourceVersion'][0]['ResourceLink'])


def main():

    # openBD apiのurlの雛形
    api = 'https://api.openbd.jp/v1/get?isbn={isbn}'

    # 画像読み込み
    image = cv2.imread("img4.png")

    # バーコード変換
    data = decode(image)

    # 数字のみ取り出し
    code = list(map(lambda x: [x[0].decode('utf-8','ignore'),x[2]],data))

    # ISBNコードのみ取り出し
    isbn_code = list(map(lambda x: {'isbn':int(x[0]),'pos':x[1]},list(filter(check_isbn,code))))

    # urlを得る
    url = api.format(isbn=isbn_code[0]['isbn'])

    # OpenBDから書籍データ取得
    result = requests.get(url)

    #print(data[0][0].decode('utf-8','ignore'))

    # json形式でデコード
    data = json.loads(result.text)
    print(data[0]['onix']['DescriptiveDetail']['TitleDetail']['TitleElement']['TitleText']['content'])
    print(data[0]['onix']['DescriptiveDetail']['Collection'].keys())
    print(data[0]['onix']['DescriptiveDetail']['Contributor'])
    print(data[0]['onix']['CollateralDetail']['SupportingResource'][0]['ResourceVersion'][0]['ResourceLink'])
    thumbnail_url = data[0]['onix']['CollateralDetail']['SupportingResource'][0]['ResourceVersion'][0]['ResourceLink']
    thumbnail_data = requests.get(thumbnail_url)
    print(type(thumbnail_data.content))

    arr = np.frombuffer(thumbnail_data.content,np.uint8)
    img = cv2.imdecode(arr,cv2.IMREAD_UNCHANGED)
    capture = cv2.VideoCapture(0)
    while True:
        ret,frame = capture.read()
        frame[0:img.shape[0],0:img.shape[1]] = img
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
          break
    print(type(img))

if __name__ == "__main__":
    #main()
    run()