#!/usr/bin/env python
# -*- coding: utf-8 -*-
def extract_personal_infos():
    import xlrd
    book = xlrd.open_workbook(filename='微博.xlsx')
    sheet = book.sheet_by_index(0)
    with open('weibo_personal_infos.txt', 'w') as f:
        for v in sheet.col(4):
            f.write(v.value.strip() + '\n')


extract_personal_infos()


