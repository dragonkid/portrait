#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv
import sqlite3

import fire


@fire.Fire
def get_history(db_file, output):
    db = sqlite3.connect(db_file)
    cursor = db.cursor()
    select_statement = "SELECT urls.url, urls.title, urls.visit_count FROM urls, visits WHERE urls.id = visits.url;"
    cursor.execute(select_statement)
    results = cursor.fetchall()

    with open(output, 'w') as f:
        writer = csv.writer(f)
        writer.writerows()
