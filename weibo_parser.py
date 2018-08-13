#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv
import copy
import json
import string
import random

import fire
import jieba

jieba.load_userdict('tags.dict')
reader = csv.reader(open('data/history.csv'))
browsing_history = list(reader)


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
        'name': '',         # 真实姓名
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
    },
    'browsing_history': [
        {   # 浏览记录
            'url': '',
            'title': '',        # 标题
            'count': 0,         # 浏览次数
        },
    ],
    'consumption_habit': {  # 消费习惯（月均）
        'clothing': 0,      # 服饰美容
        'dieting': 0,       # 饮食
        'travelling': 0,    # 交通出行
        'daily_commodities': 0, # 生活日用
        'others': 0
    },
    'illegal': {
        'yes': False,       # 是否违法
        'type': '',         # 犯罪类型：petition,criminal,alcohol_abuse
    }
}


root_tags = {
    '基本信息': 'basic',
    '标签信息': 'tags',
    '联系信息': 'contacts',
    '工作信息': 'job',
    '教育信息': 'education'
}

leafs = {
    'basic': {
        '真实姓名': 'name',
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
    },
}


def split_tags(raw):
    cuts = jieba.cut(raw, cut_all=False, HMM=False)
    return list(cuts)


def unpack_by_tags(line, tags, root=False):
    unpacked = dict()
    tags_index = dict()
    for k in tags.keys():
        if root:
            index = line.find(k)
        else:
            index = line.find(k + '：')
        if index == -1:
            continue
        tags_index[k] = index

    for tag, index in sorted(tags_index.items(), key=lambda x: x[1], reverse=True):
        raw = line[index + len(tag):].strip(string.whitespace + '：')
        if tag == '标签':
            unpacked[tags[tag]] = split_tags(raw)
        else:
            unpacked[tags[tag]] = raw
        line = line[0:index]

    return unpacked


def random_cost(low, high):
    rint = random.randint(low, high)
    return rint - rint % 100


def generate_consumption_habit():
    consumption_habit = {
        'clothing': random_cost(100, 5000),
        'dieting': random_cost(100, 5000),
        'travelling': random_cost(0, 5000),
        'daily_commodities': random_cost(100, 5000),
        'others': random_cost(0, 1000)
    }
    consumption_habit['total'] = sum(consumption_habit.values())
    return consumption_habit


def generate_browsing_history():
    return [
        {'url': url, 'title': title, 'count': int(count)}
        for url, title, count in random.choices(
            browsing_history, k=random.randint(0, 20)
        )
    ]


def unpack_info(line):
    """
    unpack txt to dict

    >>>info = unpack_info('基本信息昵称：Ybwy0923所在地：四川 宜宾标签信息标签：化妆造型瘦身减肥')
    ...info['basic']['nickname'] == 'Ybwy0923'
    ...info['basic']['location'] == '四川 宜宾'
    ...info['tags']['raw'] == '化妆造型瘦身减肥'
    ...info['basic']['raw'] == 'Ybwy0923所在地：四川 宜宾'
    """
    info = copy.deepcopy(info_structure)
    for k, v in unpack_by_tags(line, root_tags, True).items():
        info[k]['raw'] = v

    for root_key, leaf_tags in leafs.items():
        info[root_key].update(
            unpack_by_tags(info[root_key]['raw'], leafs[root_key])
        )

    info['consumption_habit'].update(
        generate_consumption_habit()
    )
    info['browsing_history'] = generate_browsing_history()

    return info


@fire.Fire
def unpack_infos(input, output):
    with open(input) as input_f, open(output, 'w') as output_f:
        for line in input_f:
            res = unpack_info(line)
            if res['basic']['nickname'] == '':
                continue
            output_f.write(json.dumps(res) + '\n')

# print(unpack_info('基本信息昵称：叶云哲博客所在地：其他性别：男博客：http://blog.sina.cn/u/1026994820g简介：汽车营销管理咨询师注册时间：2014-03-01'))
