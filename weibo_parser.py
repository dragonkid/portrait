#!/usr/bin/env python
# -*- coding: utf-8 -*-
def extract_personal_infos():
    import xlrd
    book = xlrd.open_workbook(filename='data/微博.xlsx')
    sheet = book.sheet_by_index(0)
    with open('weibo_personal_infos.txt', 'w') as f:
        for v in sheet.col(4):
            f.write(v.value.strip() + '\n')


TAGS = {
    '基本信息': {
        '昵称',
        '所在地',
        '性别',
        '感情状况',
        '简介',
        '生日',
        '注册时间',
    },
    '标签信息':{
        '标签',
    },
    '工作信息': {
        '公司',
        '地区',
        '职位',
    },
    '教育信息': {
        '大学',
    }
}


def unpack_info(line):
    pass


# extract_personal_infos()


