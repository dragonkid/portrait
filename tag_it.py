#!/usr/bin/env python
# -*- coding: utf-8 -*-
import fire
import pymongo

conn = pymongo.MongoClient()
table = conn.test.weibo


def random_select(n):
    res = table.aggregate([{'$sample': {'size': n}}])
    return [r['_id'] for r in res]


def alcohol_abuse():
    print('tagging alcohol abuse...')
    res = table.update_many({'consumption_habit.total': {'$lt': 1500}}, {'$set': {'illegal.type': 'alcohol_abuse'}}, upsert=False)
    if res.matched_count == 0:
        print('no record is updated...')
    ids = random_select(2000)
    print(ids)
    res = table.update_many({'_id': {'$in': ids}}, {'$set': {'illegal.type': 'alcohol_abuse'}}, upsert=False)
    if res.matched_count == 0:
        print('no record is updated...')


def petition():
    print('tagging petition...')
    res = table.update_many({'tags.segmentation': '上访'}, {'$set': {'illegal.type': 'petition'}})
    if res.matched_count == 0:
        print('no record is updated...')
    ids = random_select(357)
    print(ids)
    res = table.update_many({'_id': {'$in': ids}}, {'$set': {'illegal.type': 'petition'}}, upsert=False)
    if res.matched_count == 0:
        print('no record is updated...')


def criminal():
    print('tagging criminals...')
    ids = random_select(89)
    print(ids)
    res = table.update_many({'_id': {'$in': ids}}, {'$set': {'illegal.yes': True}}, upsert=False)
    if res.matched_count == 0:
        print('no record is updated...')


@fire.Fire
def tag_it():
    alcohol_abuse()
    petition()
    criminal()
