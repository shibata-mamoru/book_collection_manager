# -*- coding:utf-8 -*-

import requests
import pprint
import json

def main():
    api = 'https://app.rakuten.co.jp/services/api/BooksTotal/Search/20170404?format=json&isbnjan={isbn}&applicationId=1088097277669615348'
    api = 'https://api.openbd.jp/v1/get?isbn={isbn}'
    url = api.format(isbn=9784047356269)
    result = requests.get(url)
    data = json.loads(result.text)
    pprint.pprint(data)
    pass

if __name__ == "__main__":
    main()