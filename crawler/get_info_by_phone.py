#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zxj

https://cx.shouji.360.cn/phonearea.php?number=184082499

{
    "code": 0,
    "data": {
        "province": "四川",
        "city": "成都",
        "sp": "移动"
    }
}
"""
import xlrd
import xlwt
import requests

# 直辖市
municipalities = {'北京': '北京', '上海': '上海', '天津': '天津', '重庆': '重庆'}
xls_file = r"phonenumbers.xls"
workbook = xlrd.open_workbook(xls_file)
worksheet0 = workbook.sheet_by_index(0)
nrows = worksheet0.nrows
ncols = worksheet0.ncols

# row_data = worksheet0.row_values(1)
# col_data = worksheet0.col_values(1)


def writePhoneNumber(filename):
    _workbook = xlwt.Workbook(encoding='utf-8', style_compression=0)
    sheet = _workbook.add_sheet('contact', cell_overwrite_ok=True)
    phone_numbers = worksheet0.col_values(6)[1:]
    index = 0
    for phone in phone_numbers:
        if phone != "":
            phone = phone.replace('-', '').lstrip('+86')
            content = getAreaByPhoneNumber(phone)
            print('[process] ', phone)
            if 'data' in content and content['data'] != "":
                info = content['data']
                sp = info['sp']
                city = info['city']
                province = info['province']
                # 若属于直辖市，则补充城市信息
                if province in municipalities:
                    city = province
                sheet.write(index, 0, phone)
                sheet.write(index, 1, province)
                sheet.write(index, 2, city)
                sheet.write(index, 3, sp)
                index = index + 1
    # write to xls file
    _workbook.save(filename)


# cell types:
# 0 --empty,
# 1 --string,
# 2 --number(都是浮点),
# 3 --date,
# 4 --boolean,
# 5 --error
def getCellTypes():
    types = []
    for i in range(nrows):
        value = worksheet0.cell(i, 6)
        ctype = value.ctype
        types.append(ctype)
    return set(types)


# Get area info from phone number
def getAreaByPhoneNumber(phoneNumber):
    url = 'https://cx.shouji.360.cn/phonearea.php?number=' + phoneNumber
    response = requests.get(url)
    return response.json()


if __name__ == '__main__':
    # print(getCellTypes())
    writePhoneNumber('./naive_bayes/datasets/phone.xls')
    # getAreaByPhoneNumber("123456")
