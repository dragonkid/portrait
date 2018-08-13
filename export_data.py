#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

import fire
import pymongo

conn = pymongo.MongoClient()
table = conn.test.weibo


@fire.Fire
def export(output, size):
    records = table.aggregate([{'$sample': {'size': size}}], allowDiskUse=True)
    with open(output, 'w') as f:
        for r in records:
            del r['_id']
            f.write(json.dumps(r) + '\n')
