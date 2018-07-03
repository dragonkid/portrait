#!/usr/bin/env python
# -*- coding: utf-8 -*-
import fire
import json
import jieba

jieba.load_userdict("tag.dict")


def extract_tags(line):
    tags = list()
    cuts = jieba.cut(line, cut_all=False, HMM=False)
    res = list(cuts)
    for i, word in enumerate(res):
        if word == '：':
            tags.append(res[i - 1])

    return tags


@fire.Fire
def get_all_tags(input, output):
    tag_count = {}
    with open(input) as in_f, open(output, 'w') as out_f:
        for line in in_f:
            tags = extract_tags(line)
            for tag in tags:
                if tag.isascii():
                    continue
                if tag in tag_count:
                    tag_count[tag] += 1
                else:
                    tag_count[tag] = 1

        json.dump(tag_count, out_f)

