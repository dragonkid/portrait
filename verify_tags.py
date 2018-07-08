#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

import fire


@fire.Fire
def verify_tags(input, count_above=100):
    with open(input) as f:
        tags = json.load(f)
        sorted_tags = sorted(tags.items(), key=lambda x: x[1], reverse=True)
        for tag, count in filter(lambda x: x[1] >= count_above, sorted_tags):
            print(tag, count)
