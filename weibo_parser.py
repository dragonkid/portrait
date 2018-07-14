#!/usr/bin/env python
# -*- coding: utf-8 -*-
import copy


def extract_personal_infos():
    """
    extract weibo personal infos from xlsx to txt
    :return:
    """
    import xlrd
    book = xlrd.open_workbook(filename='data/微博.xlsx')
    sheet = book.sheet_by_index(0)
    with open('weibo_personal_infos.txt', 'w') as f:
        for v in sheet.col(4):
            f.write(v.value.strip() + '\n')


info_structure = {
    'basic': {              # 基本信息
        'name': '',         # 姓名
        'blood_group': '',  # 血型
        'nickname': '',     # 昵称
        'location': '',     # 所在地
        'sex': '',          # 性别
        'relationship_status': '',  # 感情状况
        'profile': '',      # 简介
        'birthday': '',     # 生日
        'registration': '', # 注册时间
        'domain': '',       # 个性域名
        'blog': '',         # 博客
        'sexual_orientation': '',   # 性取向
        'raw': ''
    },
    'tags': {               # 标签信息
        'segmentation': [],
        'raw': ''
    },
    'contacts': {           # 联系信息
        'email': '',        # 邮箱
        'raw': ''
    },
    'job': {                # 工作信息
        'company': '',      # 公司
        'location': '',     # 地区
        'title': '',        # 职位
        'raw': ''
    },
    'education': {          # 教育信息
        'university': '',   # 大学
        'senior_high_school': '',   # 高中
        'junior_high_school': '',   # 初中
        'primary_school': '',       # 小学
        'technical_school': '',     # 技校
        'raw': ''
    }
}


roots = {
    '基本信息': 'basic',
    '标签信息': 'tags',
    '联系信息': 'contacts',
    '工作信息': 'job',
    '教育信息': 'education'
}
leafs = {
    'basic': {
        '姓名': 'name',
        '血型': 'blood_group',
        '昵称': 'nickname',
        '所在地': 'location',
        '性别': 'sex',
        '感情状况': 'relationship_status',
        '简介': 'profile',
        '生日': 'birthday',
        '注册时间': 'registration',
        '个性域名': 'domain',
        '博客': 'blog',
        '性取向': 'sexual_orientation',
    },
    'tags': {
        '标签': 'segmentation'
    },
    'contacts': {
        '邮箱': 'email',
    },
    'job': {
        '公司': 'company',
        '地区': 'location',
        '职位': 'title',
    },
    'education': {
        '大学': 'university',
        '高中': 'senior_high_school',
        '初中': 'junior_high_school',
        '小学': 'primary_school',
        '技校': 'technical_school'
    }
}


def unpack_info(line):
    """
    unpack txt to dict

    >>>info = unpack_info('基本信息昵称：Ybwy0923所在地：四川 宜宾标签信息标签：化妆造型瘦身减肥')
    ...info['basic']['nickname'] == 'Ybwy0923'
    ...info['basic']['location'] == '四川 宜宾'
    ...info['tags']['raw'] == '化妆造型瘦身减肥'
    True
    True
    True
    """
    # info = unpack_root(line)
    pass


# extract_personal_infos()


